#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# run_queue.sh -- ORCA production queue for the computational arm.  VERSION 2.
#
#   /opt/dft-jobs/run_queue.sh --dry-run    # show the plan, run nothing
#   /opt/dft-jobs/run_queue.sh              # run it
#
# Started inside a detached tmux session so it survives SSH disconnection:
#   ssh root@<box> "tmux new-session -d -s dft-queue /opt/dft-jobs/run_queue.sh"
#
# -----------------------------------------------------------------------------
# WHY VERSION 2 EXISTS -- READ THIS BEFORE EDITING
# -----------------------------------------------------------------------------
# Version 1 dispatched 3 of 17 jobs and then exited cleanly, reporting no
# failures, and the queue sat idle for fifteen hours before anyone noticed.
#
# The cause was that version 1 fed the job list to the dispatch loop on STDIN:
#
#     while IFS= read -r line; do ... run_one "$job" & ... done < "$ORDER"
#
# and invoked ORCA without redirecting stdin:
#
#     "$ORCA" "$job.inp" > "$job.out" 2>&1        # stdin left inherited
#
# Each backgrounded job therefore inherited file descriptor 0 pointing at
# JOB_ORDER.txt, SHARING ITS FILE OFFSET with the parent loop. ORCA's mpirun
# reads stdin, consumed the remaining job lines, and advanced the shared offset
# to end-of-file. The parent's next `read` returned EOF, the loop exited
# normally, `wait` drained the two running jobs, and the queue logged a clean
# QUEUE END. Nothing failed; fourteen jobs were simply never dispatched.
#
# THREE INDEPENDENT DEFENCES NOW PREVENT THIS:
#   1. The job list is read on FILE DESCRIPTOR 3, never on stdin. A child that
#      reads stdin cannot touch it.
#   2. ORCA is invoked with `< /dev/null`, so no child has a readable stdin at
#      all.
#   3. The loop counts the lines it read and logs DISPATCH COMPLETE with that
#      count. If the count ever disagrees with the job list, it is visible in
#      queue.log immediately instead of fifteen hours later.
#
# Any future edit that reintroduces `done < "$ORDER"` or drops the `</dev/null`
# reintroduces the bug.
# -----------------------------------------------------------------------------

# NOT set -e. A failing ORCA job must never abort the queue -- sixteen good jobs
# are not thrown away because one diverged.
set -uo pipefail

JOBROOT=/opt/dft-jobs
ORCA=/opt/orca/orca
ORDER="$JOBROOT/JOB_ORDER.txt"
QLOG="$JOBROOT/queue.log"

# The queue schedules by TOTAL CORES, not by job count, so a mix of 4-core and
# 8-core jobs keeps the machine full without a barrier between them. ORCA runs
# one MPI process per core, so total processes never exceeds TOTAL_CORES and
# peak nominal memory is maxcore x TOTAL_CORES = 1500 MB x 16 = 24 GB, inside
# the 29 GB available, FOR ANY MIX OF JOB SIZES.
TOTAL_CORES=16
DEFAULT_CORES=8

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

# ── Environment ──────────────────────────────────────────────────────────────
# A tmux session started over SSH inherits a NON-LOGIN, NON-INTERACTIVE shell.
# On this box that shell has neither OpenMPI on PATH nor LD_LIBRARY_PATH set,
# and OpenMPI 4.1.8 refuses outright to run as root. Without these four exports
# every job aborts in "Startup" within seconds.
export PATH=/opt/openmpi-4.1.8/bin:$PATH
export LD_LIBRARY_PATH=/opt/openmpi-4.1.8/lib:/opt/orca:${LD_LIBRARY_PATH:-}
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

ts()   { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
qlog() {
    if [ "$DRY_RUN" -eq 1 ]; then printf 'DRY | %s\n' "$*"
    else printf '%s | %s\n' "$(ts)" "$*" | tee -a "$QLOG"; fi
}

# ── Is this job already finished? ────────────────────────────────────────────
# "ORCA TERMINATED NORMALLY" IS NOT A SUFFICIENT TEST AND MUST NEVER BE USED
# ALONE. ORCA prints that banner even when the geometry optimisation hit its
# MaxIter cap and the frequency calculation never ran at all. pb_P0_cplx did
# exactly that in S04: 102 cycles, no convergence, no Hessian, no .hess file --
# and a clean normal-termination banner. A skip test based on the banner would
# have silently accepted a job that produced no frequencies and therefore no
# free energy.
#
# A job is complete only if ALL THREE hold:
#   1. ORCA terminated normally,
#   2. the frequency module actually ran, and
#   3. the Hessian file exists on disk.
is_complete() {
    local job=$1 out="$JOBROOT/$1/$1.out" hess="$JOBROOT/$1/$1.hess"
    [ -f "$out" ]  || return 1
    [ -f "$hess" ] || return 1
    grep -qa 'ORCA TERMINATED NORMALLY' "$out" || return 1
    grep -qa 'VIBRATIONAL FREQUENCIES'  "$out" || return 1
    return 0
}

# ── One queue at a time ──────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 0 ]; then
    exec 9>"$JOBROOT/.queue.lock"
    if ! flock -n 9; then
        echo "run_queue.sh: another queue already holds the lock; refusing to start" >&2
        exit 1
    fi
fi

# ── Slot accounting ──────────────────────────────────────────────────────────
declare -A PID_CORES=()
used_cores=0

reap_finished() {
    local p
    for p in "${!PID_CORES[@]}"; do
        if ! kill -0 "$p" 2>/dev/null; then
            used_cores=$(( used_cores - ${PID_CORES[$p]} ))
            unset "PID_CORES[$p]"
        fi
    done
    (( used_cores < 0 )) && used_cores=0
    return 0
}

# ── Run one job ──────────────────────────────────────────────────────────────
run_one() {
    local job=$1 cores=$2
    local dir="$JOBROOT/$job"
    local t0 t1 rc

    # ORCA writes scratch relative to the working directory, so each job runs
    # from inside its own directory. This function always runs in a background
    # subshell, so the cd is local to that job.
    cd "$dir" || { qlog "FAILED   | $job | cannot cd to $dir"; return 0; }

    qlog "START    | $job | cores=$cores | maxcore=1500MB"
    t0=$(date +%s)

    # ORCA is invoked by ABSOLUTE PATH and is NEVER wrapped in mpirun -- it
    # spawns its own MPI processes from the %pal block in the input file.
    #
    # `< /dev/null` IS LEAD-BEARING. See the header. Do not remove it.
    "$ORCA" "$job.inp" > "$job.out" 2>&1 < /dev/null
    rc=$?

    t1=$(date +%s)
    local el=$(( t1 - t0 ))
    local hms; hms=$(printf '%dh%02dm%02ds' $((el/3600)) $(((el%3600)/60)) $((el%60)))

    if grep -qa 'ORCA TERMINATED NORMALLY' "$job.out" 2>/dev/null; then
        local nimag; nimag=$(grep -ac '\*\*\*imaginary mode\*\*\*' "$job.out" 2>/dev/null)
        nimag=${nimag:-0}
        if [ "$nimag" -gt 0 ]; then
            qlog "FINISHED | $job | exit=$rc | elapsed=${el}s ($hms) | ORCA TERMINATED NORMALLY | *** $nimag IMAGINARY MODE(S) -- NOT A MINIMUM ***"
        else
            qlog "FINISHED | $job | exit=$rc | elapsed=${el}s ($hms) | ORCA TERMINATED NORMALLY | all frequencies real"
        fi
    else
        qlog "FAILED   | $job | exit=$rc | elapsed=${el}s ($hms) | no normal-termination banner"
    fi
    return 0
}

# ── Plan ─────────────────────────────────────────────────────────────────────
if [ ! -f "$ORDER" ]; then
    echo "run_queue.sh: $ORDER not found" >&2
    exit 1
fi

n_total=0; n_skip=0; n_todo=0
while read -r -u 3 line || [ -n "$line" ]; do
    line="${line%%#*}"
    # shellcheck disable=SC2086
    set -- $line
    [ $# -eq 0 ] && continue
    n_total=$(( n_total + 1 ))
    if is_complete "$1"; then n_skip=$(( n_skip + 1 )); else n_todo=$(( n_todo + 1 )); fi
done 3< "$ORDER"

qlog "======== QUEUE START | job list $n_total | already complete $n_skip | to run $n_todo | core cap $TOTAL_CORES ========"

# ── Dispatch ─────────────────────────────────────────────────────────────────
lines_read=0; dispatched=0; skipped=0

while read -r -u 3 line || [ -n "$line" ]; do
    line="${line%%#*}"
    # shellcheck disable=SC2086
    set -- $line
    [ $# -eq 0 ] && continue

    job=$1
    cores=${2:-$DEFAULT_CORES}
    case "$cores" in ''|*[!0-9]*) qlog "NOTE     | $job | core count '${2:-}' unreadable, using $DEFAULT_CORES"; cores=$DEFAULT_CORES ;; esac
    [ "$cores" -gt "$TOTAL_CORES" ] && cores=$TOTAL_CORES
    [ "$cores" -lt 1 ] && cores=1

    lines_read=$(( lines_read + 1 ))

    if [ ! -f "$JOBROOT/$job/$job.inp" ]; then
        qlog "SKIP     | $job | no $job.inp under $JOBROOT/$job"
        continue
    fi

    if is_complete "$job"; then
        qlog "SKIP     | $job | already complete (ORCA TERMINATED NORMALLY present)"
        skipped=$(( skipped + 1 ))
        continue
    fi

    if [ "$DRY_RUN" -eq 1 ]; then
        qlog "WOULD RUN| $job | cores=$cores"
        dispatched=$(( dispatched + 1 ))
        continue
    fi

    # Block until enough cores are free.
    while (( used_cores + cores > TOTAL_CORES )); do
        wait -n 2>/dev/null
        reap_finished
    done

    run_one "$job" "$cores" &
    PID_CORES[$!]=$cores
    used_cores=$(( used_cores + cores ))
    dispatched=$(( dispatched + 1 ))
done 3< "$ORDER"

# THE LINE THAT WOULD HAVE CAUGHT THE VERSION-1 BUG IMMEDIATELY.
qlog "DISPATCH COMPLETE | lines read $lines_read of $n_total | dispatched $dispatched | skipped $skipped"
if [ "$lines_read" -ne "$n_total" ]; then
    qlog "!!!!!!!! WARNING | read $lines_read job lines but the list has $n_total. The job list was NOT fully consumed. !!!!!!!!"
fi

[ "$DRY_RUN" -eq 1 ] && { qlog "dry run only -- nothing was executed"; exit 0; }

wait
qlog "======== QUEUE END | dispatched $dispatched | skipped $skipped ========"
