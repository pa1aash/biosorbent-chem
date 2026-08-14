#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# lib_jobstate.sh -- shared job-state predicates for the box-side scripts.
#
# Sourced by heartbeat.sh and watchdog.sh. NOT sourced by run_queue.sh, which is
# deliberately self-contained: it is the thing that must keep working when
# everything else is broken, and it is often already running when these files
# are edited.
#
# THE COMPLETION TEST LIVES HERE SO IT CANNOT DRIFT. It has already been wrong
# once. In S04 "ORCA TERMINATED NORMALLY" was used alone, and pb_P0_cplx was
# recorded as finished after 102 optimisation cycles with no convergence, no
# frequency calculation and no .hess file -- ORCA prints that banner anyway.
# =============================================================================

JOBROOT="${JOBROOT:-/opt/dft-jobs}"
ORDER="$JOBROOT/JOB_ORDER.txt"

# A job is complete only if ALL THREE hold:
#   1. ORCA terminated normally,
#   2. the frequency module actually ran, and
#   3. the Hessian file exists on disk.
js_is_complete() {
    local job=$1 out="$JOBROOT/$1/$1.out" hess="$JOBROOT/$1/$1.hess"
    [ -f "$out" ]  || return 1
    [ -f "$hess" ] || return 1
    grep -qa 'ORCA TERMINATED NORMALLY' "$out" || return 1
    grep -qa 'VIBRATIONAL FREQUENCIES'  "$out" || return 1
    return 0
}

# Emit the job names listed in JOB_ORDER.txt, one per line.
# The file is two columns ("<jobname> <cores>  # note"), so take field 1 only.
js_jobs() {
    [ -f "$ORDER" ] || return 0
    while read -r line; do
        line="${line%%#*}"
        # shellcheck disable=SC2086
        set -- $line
        [ $# -eq 0 ] && continue
        echo "$1"
    done < "$ORDER"
}

# js_counts -> "<complete> <incomplete> <total>"
js_counts() {
    local c=0 i=0 t=0 job
    for job in $(js_jobs); do
        t=$(( t + 1 ))
        if js_is_complete "$job"; then c=$(( c + 1 )); else i=$(( i + 1 )); fi
    done
    echo "$c $i $t"
}

# How many ORCA driver processes are alive right now.
#
# MATCH ON THE PROCESS NAME (-x), NOT THE COMMAND LINE (-f). A `pgrep -f` for a
# pattern like '/opt/orca/orca .*\.inp' also matches any OTHER process whose
# command line happens to contain that text -- including the very shell running
# this check, or an ssh command that mentions it. That false positive is in the
# DANGEROUS direction: it makes the queue look busy when it is dead, and would
# suppress exactly the restart this watchdog exists to make.
#
# -x matches comm exactly, so it counts the ORCA drivers and not the
# orca_leanscf_mpi / orca_startup_mpi workers they spawn (whose comm differs).
js_orca_procs() {
    local n
    n=$(pgrep -c -x orca 2>/dev/null)
    echo "${n:-0}"
}

js_queue_alive() {
    tmux has-session -t dft-queue 2>/dev/null
}

# Is the queue driver itself alive? Combined with zero ORCA processes this is
# the true "queue is dead" test: the S04 failure was run_queue.sh EXITING, not
# hanging. Checking for the driver also avoids restarting during the brief gap
# between one job finishing and the next starting.
#
# Tested via the flock that run_queue.sh holds for its entire life, NOT via
# pgrep -f, for the same self-matching reason given above. If we can take the
# lock, no queue holds it. Opened append-only so an existing lock file is never
# truncated.
js_queue_driver_running() {
    exec 7>>"$JOBROOT/.queue.lock" 2>/dev/null || return 1
    if flock -n 7 2>/dev/null; then
        exec 7>&-        # we got it, so nobody else holds it
        return 1
    fi
    exec 7>&-
    return 0
}
