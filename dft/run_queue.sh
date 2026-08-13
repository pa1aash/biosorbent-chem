#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# run_queue.sh -- ORCA production queue for the computational arm.
#
# Runs every job listed in JOB_ORDER.txt, at most MAXPAR at a time, logging a
# start and a finish line per job to queue.log. A job that fails does NOT abort
# the queue; the next job starts regardless.
#
# Deployed to /opt/dft-jobs/run_queue.sh and started inside a detached tmux
# session named "dft-queue" so the queue survives SSH disconnection:
#
#     ssh root@<box> "tmux new-session -d -s dft-queue /opt/dft-jobs/run_queue.sh"
#
# Check status from anywhere with  scripts/dft_status.sh  in this repository.
# =============================================================================

# NOT set -e. A failing ORCA job must never abort the queue -- 16 good jobs are
# not thrown away because one diverged.
set -uo pipefail

JOBROOT=/opt/dft-jobs
ORCA=/opt/orca/orca
ORDER="$JOBROOT/JOB_ORDER.txt"
QLOG="$JOBROOT/queue.log"
MAXPAR=2                    # 16 vCPU / 8 per job

# ── Environment ──────────────────────────────────────────────────────────────
# READ THIS BEFORE CHANGING ANYTHING BELOW.
#
# A tmux session started over SSH inherits a NON-LOGIN, NON-INTERACTIVE shell.
# On this box that shell has neither OpenMPI on PATH nor LD_LIBRARY_PATH set --
# both are configured only for login shells. And OpenMPI 4.1.8 refuses outright
# to run as root without an explicit override.
#
# Without these four exports EVERY job aborts in "Startup" within seconds, with
# the queue reporting failures that look like ORCA faults and are not. Verified
# by direct probe on 2026-08-13 before launch.
export PATH=/opt/openmpi-4.1.8/bin:$PATH
export LD_LIBRARY_PATH=/opt/openmpi-4.1.8/lib:/opt/orca:${LD_LIBRARY_PATH:-}
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

ts()   { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
qlog() { printf '%s | %s\n' "$(ts)" "$*" >> "$QLOG"; }

# ── One queue at a time ──────────────────────────────────────────────────────
# Two concurrent queues would run 4 ORCA jobs on 16 cores with 2x the memory
# budget, and would interleave their writes into the same job directories.
exec 9>"$JOBROOT/.queue.lock"
if ! flock -n 9; then
    echo "run_queue.sh: another queue already holds the lock; refusing to start" >&2
    exit 1
fi

# ── Run one job ──────────────────────────────────────────────────────────────
run_one() {
    local job=$1
    local dir="$JOBROOT/$job"
    local t0 t1 rc

    # ORCA writes scratch relative to the current working directory, so each
    # job must run from inside its own directory. This function always runs in
    # a background subshell, so the cd is local to that job.
    cd "$dir" || { qlog "FAILED   | $job | cannot cd to $dir"; return 0; }

    qlog "START    | $job | nprocs=8 | maxcore=1500MB"
    t0=$(date +%s)

    # ORCA is invoked by ABSOLUTE PATH and is NEVER wrapped in mpirun. ORCA
    # spawns its own MPI processes from the %pal block in the input file;
    # wrapping it would double-parallelise and corrupt the run.
    "$ORCA" "$job.inp" > "$job.out" 2>&1
    rc=$?

    t1=$(date +%s)

    if grep -q 'ORCA TERMINATED NORMALLY' "$job.out" 2>/dev/null; then
        qlog "FINISHED | $job | exit=$rc | elapsed=$((t1 - t0))s | ORCA TERMINATED NORMALLY"
    else
        qlog "FAILED   | $job | exit=$rc | elapsed=$((t1 - t0))s | no normal-termination banner"
    fi
    return 0
}

# ── Main loop ────────────────────────────────────────────────────────────────
if [[ ! -f "$ORDER" ]]; then
    qlog "ABORT | no $ORDER"
    echo "run_queue.sh: $ORDER not found" >&2
    exit 1
fi

njobs=$(grep -cvE '^\s*(#|$)' "$ORDER")
qlog "======== QUEUE START | $njobs jobs | maxpar=$MAXPAR | orca=$ORCA ========"

while IFS= read -r line || [[ -n "$line" ]]; do
    job="${line%%#*}"                       # strip trailing comment
    job="${job//[[:space:]]/}"              # strip all whitespace
    [[ -z "$job" ]] && continue

    if [[ ! -f "$JOBROOT/$job/$job.inp" ]]; then
        qlog "SKIP     | $job | no $job.inp under $JOBROOT/$job"
        continue
    fi

    # Block until a slot frees up.
    while (( $(jobs -rp | wc -l) >= MAXPAR )); do
        wait -n
    done

    run_one "$job" &
done < "$ORDER"

wait
qlog "======== QUEUE END ========"
