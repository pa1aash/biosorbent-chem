#!/usr/bin/env bash
# Pull finished ORCA output back into dft/outputs/ .
#     bash sync_results.sh <host> [remote-scratch]
#
# Transfers the text outputs and structures that are evidence, and leaves behind the large
# regenerable binaries (.gbw, .tmp, densities) which are gitignored anyway.
set -euo pipefail

HOST="${1:?usage: sync_results.sh <host> [remote-scratch]}"
REMOTE="${2:-/scratch}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST="$ROOT/dft/outputs"
mkdir -p "$DEST"

echo "==> syncing $HOST:$REMOTE -> $DEST"
rsync -avP \
    --include='*/' \
    --include='*.out' --include='*.inp' --include='*.xyz' \
    --include='*.hess' --include='*.engrad' --include='*.property.txt' \
    --include='*.molden' --include='*.molden.input' --include='*.exit' \
    --exclude='*' \
    "root@$HOST:$REMOTE/" "$DEST/"

echo
echo "==> convergence and sanity check"
python3 - "$DEST" <<'PY'
import sys, pathlib, re
root = pathlib.Path(sys.argv[1])
outs = sorted(root.rglob("*.out"))
if not outs:
    print("  no output files found"); raise SystemExit
print(f"  {'job':<34}{'terminated':<12}{'imag modes':<12}{'<S^2>'}")
for o in outs:
    t = o.read_text(errors="ignore")
    ok = "ORCA TERMINATED NORMALLY" in t
    imag = len(re.findall(r"^\s*\d+:\s+-\d+\.\d+\s+cm\*\*-1\s+\*\*\*imaginary", t, re.M))
    s2 = re.findall(r"<S\*\*2>\s*[:=]\s*([\d.]+)", t)
    print(f"  {o.stem:<34}{('yes' if ok else 'NO'):<12}{imag:<12}{(s2[-1] if s2 else '-')}")
print()
print("  Any job with terminated=NO, or with imaginary modes on a structure reported as a")
print("  minimum, is NOT usable. Re-optimise along the imaginary mode and re-run frequencies.")
print("  Every Cu species MUST show <S^2>; its absence means it was run closed-shell (attack A02).")
PY
