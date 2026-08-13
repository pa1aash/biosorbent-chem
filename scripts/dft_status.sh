#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# dft_status.sh -- what is the ORCA queue doing right now?
#
#   bash scripts/dft_status.sh
#
# Safe to run at any time, as often as you like. It only reads. It never
# starts, stops or modifies a job.
#
# You do not need any prior context to read the output. Each job is one line:
#
#   DONE      finished, and ORCA printed its normal-termination banner
#   RUNNING   an ORCA process for this job exists right now
#   FAILED    it stopped without the normal-termination banner -- needs a look
#   QUEUED    not started yet
#
# The instance is 65.20.67.245 and it bills at $0.493/hr whether or not the
# jobs are running. STOPPING IT DOES NOT HALT BILLING -- ONLY DESTROYING IT
# DOES. Destroy it once scripts/dft_harvest.sh has pulled everything back.
# =============================================================================

set -uo pipefail

HOST="${DFT_HOST:-root@65.20.67.245}"
JOBROOT="${DFT_JOBROOT:-/opt/dft-jobs}"

ssh -o ConnectTimeout=15 "$HOST" JOBROOT="$JOBROOT" 'bash -s' <<'REMOTE'
set -uo pipefail
cd "$JOBROOT" 2>/dev/null || { echo "cannot reach $JOBROOT"; exit 1; }

now=$(date -u +%s)

printf '=== ORCA QUEUE STATUS ===  %s\n' "$(date -u '+%Y-%m-%d %H:%M:%SZ') / $(TZ=Asia/Kolkata date '+%H:%M IST')"
printf 'host %s   jobroot %s\n\n' "$(hostname)" "$JOBROOT"

if tmux has-session -t dft-queue 2>/dev/null; then
    echo "tmux session 'dft-queue' : ALIVE"
else
    echo "tmux session 'dft-queue' : GONE  (queue finished, or died)"
fi
nrun=$(pgrep -fc '/opt/orca/orca .*\.inp' 2>/dev/null); nrun=${nrun:-0}
echo "ORCA jobs running now    : $nrun"
echo

printf '%-14s %-9s %-11s %-8s %s\n' JOB STATUS ELAPSED SCRATCH STAGE
printf '%-14s %-9s %-11s %-8s %s\n' -------------- --------- ----------- -------- ---------------------------

ndone=0; nfail=0; nrunning=0; nqueued=0

while read -r job; do
    job="${job%%#*}"; job="${job//[[:space:]]/}"
    [ -z "$job" ] && continue
    out="$job/$job.out"

    # Tolerant of the column padding in queue.log: match on the job field, not
    # on a fixed number of spaces after the verb.
    start=$(grep -E "\| *START *\| *$job *\|" queue.log 2>/dev/null | tail -1 | cut -d' ' -f1)
    fin=$(grep -E "\| *(FINISHED|FAILED) *\| *$job *\|" queue.log 2>/dev/null | tail -1)

    scratch=$(du -sh "$job" 2>/dev/null | cut -f1); scratch=${scratch:--}

    if [ ! -f "$out" ]; then
        printf '%-14s %-9s %-11s %-8s %s\n' "$job" QUEUED - "$scratch" "not started"
        nqueued=$((nqueued+1)); continue
    fi

    # Elapsed. For a finished job the queue log already recorded the authoritative
    # figure as "elapsed=NNNs"; use it. For a running job, measure from its START
    # stamp to now.
    el='-'
    if [ -n "$fin" ]; then
        d=$(echo "$fin" | sed -n 's/.*elapsed=\([0-9]*\)s.*/\1/p')
    elif [ -n "$start" ]; then
        s=$(date -u -d "$start" +%s 2>/dev/null || echo "")
        [ -n "$s" ] && d=$((now - s)) || d=""
    else
        d=""
    fi
    [ -n "$d" ] && el=$(printf '%dh%02dm' $((d/3600)) $(((d%3600)/60)))

    # Stage: the most recent thing ORCA said it was doing.
    stage=$(grep -aE 'GEOMETRY OPTIMIZATION CYCLE|ORCA (SCF |)HESSIAN|VIBRATIONAL FREQUENCIES|THERMOCHEMISTRY|HURRAY' "$out" 2>/dev/null \
            | tail -1 | tr -s ' ' | sed 's/^ *//;s/ *$//' | cut -c1-40)
    # grep -c already prints 0 when there is no match; a "|| echo 0" here would
    # append a SECOND zero and break the integer tests below.
    cyc=$(grep -ac 'GEOMETRY OPTIMIZATION CYCLE' "$out" 2>/dev/null); cyc=${cyc:-0}
    [ -n "$stage" ] || stage='starting up'
    case "$stage" in *"OPTIMIZATION CYCLE"*) stage="opt cycle $cyc";; *HESSIAN*) stage="analytic Hessian";; *VIBRATIONAL*) stage="frequencies";; *THERMOCHEM*) stage="thermochemistry";; *HURRAY*) stage="opt converged -> Hessian";; esac

    if grep -qa 'ORCA TERMINATED NORMALLY' "$out" 2>/dev/null; then
        nimag=$(grep -ac '\*\*\*imaginary mode\*\*\*' "$out" 2>/dev/null); nimag=${nimag:-0}
        note="opt cycles $cyc"
        [ "$nimag" -gt 0 ] && note="$note | *** $nimag IMAGINARY MODE(S) ***"
        printf '%-14s %-9s %-11s %-8s %s\n' "$job" DONE "$el" "$scratch" "$note"
        ndone=$((ndone+1))
    elif pgrep -f "/opt/orca/orca $job.inp" >/dev/null 2>&1; then
        printf '%-14s %-9s %-11s %-8s %s\n' "$job" RUNNING "$el" "$scratch" "$stage"
        nrunning=$((nrunning+1))
    else
        printf '%-14s %-9s %-11s %-8s %s\n' "$job" FAILED "$el" "$scratch" "stopped at: $stage"
        nfail=$((nfail+1))
    fi
done < JOB_ORDER.txt

echo
echo "DONE $ndone | RUNNING $nrunning | QUEUED $nqueued | FAILED $nfail   (17 total)"
[ "$nfail" -gt 0 ] && echo "!! inspect a failure with:  ssh $(whoami)@<host> 'tail -50 $JOBROOT/<job>/<job>.out'"

echo
echo "=== DISK ==="
df -h /opt | tail -1
echo "job directories total: $(du -sh "$JOBROOT" 2>/dev/null | cut -f1)"
echo "memory:"; free -g | head -2

echo
echo "=== queue.log (last 15) ==="
tail -15 queue.log 2>/dev/null || echo "(no queue.log yet)"

echo
echo "REMINDER: instance bills at \$0.493/hr. Stopping does NOT halt billing."
echo "          Harvest with scripts/dft_harvest.sh, then DESTROY the instance."
REMOTE
