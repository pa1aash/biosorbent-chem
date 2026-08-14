#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# watchdog.sh -- restart the ORCA queue if, and only if, it has genuinely died
# with work left to do.
#
# Run from cron every 15 minutes:
#   */15 * * * * /opt/dft-jobs/watchdog.sh >/dev/null 2>&1
#
# -----------------------------------------------------------------------------
# WHAT THIS SCRIPT WILL NEVER DO
# -----------------------------------------------------------------------------
#   * It never kills, signals or restarts a running calculation. There is no
#     kill, no pkill and no tmux kill-session anywhere in this file.
#   * It never touches a job directory or an input file.
#   * It never starts anything while an ORCA process is alive.
#   * It never modifies run_queue.sh. (Editing a running bash script can corrupt
#     its execution, because bash reads the file incrementally.)
#
# It only ever appends to logs and, in one narrow circumstance, starts
# run_queue.sh in a fresh tmux session.
#
# -----------------------------------------------------------------------------
# WHY A RESTART IS SAFE
# -----------------------------------------------------------------------------
# run_queue.sh skips any job passing the three-part completion test -- normal
# termination AND the frequency section AND the .hess file. A restart therefore
# RESUMES; it does not redo finished work, and it does not skip a job that
# produced no frequencies. run_queue.sh also holds an flock, so even a spurious
# start cannot produce two concurrent queues.
#
# -----------------------------------------------------------------------------
# THE RESTART CONDITION, AND THE CAP
# -----------------------------------------------------------------------------
# Restart only when ALL of:
#   1. at least one job is incomplete,
#   2. zero ORCA driver processes are running,
#   3. run_queue.sh itself is not running,
#   4. conditions 1-3 have held continuously for more than 15 minutes
#      (confirmed across two cron ticks, never on a single observation), and
#   5. the watchdog has not given up.
#
# Give up permanently, writing a FAILURE banner, when any of:
#   * the queue died again within 30 minutes of the previous restart,
#   * a restart produced no additional completed job, or
#   * MAX_RESTARTS restarts have been made.
# =============================================================================

set -uo pipefail

JOBROOT=/opt/dft-jobs
HB="$JOBROOT/heartbeat.log"
QLOG="$JOBROOT/queue.log"
STATE="$JOBROOT/.watchdog"

IDLE_CONFIRM=900      # 15 min of continuous idle before acting
DIED_FAST=1800        # a restart that dies within 30 min counts as failed
MAX_RESTARTS=5

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# shellcheck source=/dev/null
. "$JOBROOT/lib_jobstate.sh"

mkdir -p "$STATE"
now=$(date +%s)
ts() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }

note()   { printf '%s | WATCHDOG | %s\n' "$(ts)" "$*" >> "$HB"; }
shout()  {
    printf '%s | WATCHDOG | %s\n' "$(ts)" "$*" >> "$HB"
    printf '%s | ######## WATCHDOG: %s ########\n' "$(ts)" "$*" >> "$QLOG"
}

rd() { [ -f "$STATE/$1" ] && cat "$STATE/$1" || echo ""; }
wr() { printf '%s\n' "$2" > "$STATE/$1"; }

# ── Observe ──────────────────────────────────────────────────────────────────
read -r n_complete n_incomplete n_total <<EOF
$(js_counts)
EOF
n_orca=$(js_orca_procs)

# ── Everything finished: nothing to guard ────────────────────────────────────
if [ "$n_incomplete" -eq 0 ]; then
    rm -f "$STATE/first_idle"
    [ -f "$STATE/all_done_logged" ] || {
        shout "all $n_total jobs complete -- watchdog idle, nothing further to do"
        wr all_done_logged "$now"
    }
    exit 0
fi

# ── Healthy: jobs are running, or the driver is alive between jobs ───────────
if [ "$n_orca" -gt 0 ] || js_queue_driver_running; then
    rm -f "$STATE/first_idle"
    exit 0
fi

# ── Idle with work outstanding ───────────────────────────────────────────────
if [ -f "$STATE/disabled" ]; then
    exit 0                     # already gave up; stay quiet
fi

first_idle=$(rd first_idle)
if [ -z "$first_idle" ]; then
    wr first_idle "$now"
    note "queue idle with $n_incomplete job(s) outstanding -- starting the ${IDLE_CONFIRM}s confirmation clock, no action yet"
    exit 0
fi

idle_for=$(( now - first_idle ))
if [ "$idle_for" -lt "$IDLE_CONFIRM" ]; then
    exit 0                     # not confirmed yet
fi

# Race guard: re-observe immediately before acting.
if [ "$(js_orca_procs)" -gt 0 ] || js_queue_driver_running; then
    rm -f "$STATE/first_idle"
    exit 0
fi

# ── Stall confirmed. Should we restart, or give up? ──────────────────────────
last_restart=$(rd last_restart)
last_complete=$(rd last_restart_complete)
restart_count=$(rd restart_count); restart_count=${restart_count:-0}

give_up() {
    wr disabled "$now"
    {
        printf '\n'
        printf '%s\n' "================================================================"
        printf '%s | WATCHDOG FAILURE -- GIVING UP\n' "$(ts)"
        printf '%s\n' "================================================================"
        printf '  reason        : %s\n' "$1"
        printf '  restarts made : %s\n' "$restart_count"
        printf '  complete      : %s/%s   incomplete: %s\n' "$n_complete" "$n_total" "$n_incomplete"
        printf '  THE QUEUE IS STOPPED AND THE WATCHDOG WILL NOT RESTART IT AGAIN.\n'
        printf '  A human must look at this. Start with:\n'
        printf '    bash scripts/dft_status.sh\n'
        printf '    ssh root@65.20.67.245 "tail -50 /opt/dft-jobs/queue.log"\n'
        printf '  To re-arm the watchdog after fixing the cause:\n'
        printf '    ssh root@65.20.67.245 "rm -rf /opt/dft-jobs/.watchdog"\n'
        printf '  The instance still bills at $0.493/hr while stopped.\n'
        printf '%s\n' "================================================================"
        printf '\n'
    } >> "$HB"
    printf '%s | ######## WATCHDOG FAILURE -- GIVING UP: %s ########\n' "$(ts)" "$1" >> "$QLOG"
}

if [ -n "$last_restart" ] && [ $(( first_idle - last_restart )) -lt "$DIED_FAST" ]; then
    give_up "the queue died again $(( (first_idle - last_restart) / 60 )) min after the previous restart (threshold ${DIED_FAST}s)"
    exit 0
fi

if [ -n "$last_complete" ] && [ "$n_complete" -le "$last_complete" ]; then
    give_up "the previous restart produced no additional completed job (still $n_complete complete)"
    exit 0
fi

if [ "$restart_count" -ge "$MAX_RESTARTS" ]; then
    give_up "reached MAX_RESTARTS=$MAX_RESTARTS"
    exit 0
fi

# ── Restart ──────────────────────────────────────────────────────────────────
restart_count=$(( restart_count + 1 ))

session=dft-queue
if tmux has-session -t "$session" 2>/dev/null; then
    session="dft-queue-r${restart_count}"      # never touch an existing session
fi

shout "RESTART #$restart_count -- queue idle ${idle_for}s with $n_incomplete of $n_total job(s) outstanding; starting run_queue.sh in tmux session '$session'"

if tmux new-session -d -s "$session" "$JOBROOT/run_queue.sh" 2>>"$HB"; then
    wr last_restart "$now"
    wr last_restart_complete "$n_complete"
    wr restart_count "$restart_count"
    rm -f "$STATE/first_idle"
    sleep 20
    shout "RESTART #$restart_count issued -- $(js_orca_procs) ORCA process(es) alive 20s later"
else
    shout "RESTART #$restart_count FAILED -- tmux new-session returned non-zero"
    wr last_restart "$now"
    wr restart_count "$restart_count"
fi
