#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# dft_harvest.sh -- pull ORCA results back into dft/outputs/.
#
#   bash scripts/dft_harvest.sh              # harvest whatever is finished
#   bash scripts/dft_harvest.sh --all        # include jobs still running
#   bash scripts/dft_harvest.sh --dry-run    # show what would transfer
#
# SAFE TO RE-RUN. It is incremental: run it whenever a few more jobs finish and
# it will fetch only what has changed. It never deletes anything locally and it
# never modifies anything on the compute box.
#
# By default it harvests only jobs whose .out carries ORCA's normal-termination
# banner, because a half-written .out from a running job would land in
# dft/outputs/ looking like a result. --all overrides that.
#
# WHAT IS TRANSFERRED
#   .out            the primary output -- every energy in the report must be
#                   traceable to one of these
#   .xyz  _trj.xyz  optimised geometry and the optimisation trajectory
#   .hess           the Hessian, for the frequency and thermochemistry analysis
#   .gbw            the converged wavefunction, needed by Multiwfn for the
#                   decomposition analysis (protocol §4). Binary and gitignored
#                   by design, but kept locally.
#   .property.txt .engrad .opt .smd .cpcm .cpcm_corr .bibtex
#
# WHAT IS EXCLUDED -- scratch, and large regenerable intermediates
#   *.tmp *.tmp.* *_atom*.out *.densities *.densitiesinfo *.bas* *.ges
#   and every ORCA gridfile
#
# After harvesting, verify nothing is missing, then DESTROY the Vultr instance.
# It bills at $0.493/hr and stopping does not halt billing.
# =============================================================================

set -uo pipefail

HOST="${DFT_HOST:-root@65.20.67.245}"
JOBROOT="${DFT_JOBROOT:-/opt/dft-jobs}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$REPO/dft/outputs"

ONLY_FINISHED=1
RSYNC_EXTRA=()
for arg in "$@"; do
    case "$arg" in
        --all)     ONLY_FINISHED=0 ;;
        --dry-run) RSYNC_EXTRA+=(--dry-run) ;;
        -h|--help) sed -n '2,45p' "${BASH_SOURCE[0]}"; exit 0 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

mkdir -p "$DEST"

echo "=== dft_harvest.sh ==="
echo "from : $HOST:$JOBROOT"
echo "to   : $DEST"
if [ "$ONLY_FINISHED" -eq 1 ]; then
    echo "mode : finished jobs only (--all to include running jobs)"
else
    echo "mode : ALL jobs, including any still running"
fi
echo

# ── Which jobs are ready? Decided on the box, from the .out banner. ──────────
mapfile -t JOBS < <(
    ssh -o ConnectTimeout=15 "$HOST" JOBROOT="$JOBROOT" ONLY_FINISHED="$ONLY_FINISHED" 'bash -s' <<'REMOTE'
cd "$JOBROOT" 2>/dev/null || exit 1
while read -r job; do
    job="${job%%#*}"; job="${job//[[:space:]]/}"
    [ -z "$job" ] && continue
    out="$job/$job.out"
    [ -f "$out" ] || continue
    if [ "$ONLY_FINISHED" -eq 1 ]; then
        grep -qa 'ORCA TERMINATED NORMALLY' "$out" || continue
    fi
    echo "$job"
done < JOB_ORDER.txt
REMOTE
)

if [ "${#JOBS[@]}" -eq 0 ]; then
    echo "Nothing to harvest yet -- no job has terminated normally."
    echo "Check progress with:  bash scripts/dft_status.sh"
    exit 0
fi

echo "harvesting ${#JOBS[@]} job(s): ${JOBS[*]}"
echo

for job in "${JOBS[@]}"; do
    mkdir -p "$DEST/$job"
    rsync -az --info=name1 "${RSYNC_EXTRA[@]}" \
        --prune-empty-dirs \
        --include='*/' \
        --include='*.out' \
        --include='*.xyz' \
        --include='*.hess' \
        --include='*.gbw' \
        --include='*.property.txt' \
        --include='*.engrad' \
        --include='*.opt' \
        --include='*.smd' \
        --include='*.smd.grd' \
        --include='*.cpcm' \
        --include='*.cpcm_corr' \
        --include='*.bibtex' \
        --include='*.inp' \
        --exclude='*_atom*.out' \
        --exclude='*.tmp' \
        --exclude='*.tmp.*' \
        --exclude='*.densities' \
        --exclude='*.densitiesinfo' \
        --exclude='*.bas*' \
        --exclude='*.ges' \
        --exclude='*' \
        "$HOST:$JOBROOT/$job/" "$DEST/$job/" \
        && printf '  %-14s ok\n' "$job" \
        || printf '  %-14s TRANSFER FAILED\n' "$job"
done

# The queue log is evidence of what ran, when, and for how long.
rsync -az "${RSYNC_EXTRA[@]}" "$HOST:$JOBROOT/queue.log" "$DEST/queue.log" 2>/dev/null \
    && echo "  queue.log      ok"

echo
echo "=== harvested ==="
for job in "${JOBS[@]}"; do
    n=$(find "$DEST/$job" -type f 2>/dev/null | wc -l | tr -d ' ')
    sz=$(du -sh "$DEST/$job" 2>/dev/null | cut -f1)
    term=$(grep -qa 'ORCA TERMINATED NORMALLY' "$DEST/$job/$job.out" 2>/dev/null && echo 'TERMINATED NORMALLY' || echo '*** NO NORMAL TERMINATION ***')
    imag=$(grep -ac '\*\*\*imaginary mode\*\*\*' "$DEST/$job/$job.out" 2>/dev/null || echo 0)
    extra=""
    [ "$imag" -gt 0 ] 2>/dev/null && extra="  *** $imag IMAGINARY MODE(S) -- NOT A MINIMUM ***"
    printf '  %-14s %2s files  %6s  %s%s\n' "$job" "$n" "$sz" "$term" "$extra"
done

echo
echo "Local total: $(du -sh "$DEST" 2>/dev/null | cut -f1) in $DEST"
echo
echo "NEXT"
echo "  1. Re-run this script as more jobs finish -- it is incremental."
echo "  2. When all 17 are harvested, verify, then DESTROY the Vultr instance."
echo "     It bills at \$0.493/hr and STOPPING DOES NOT HALT BILLING."
