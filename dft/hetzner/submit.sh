#!/usr/bin/env bash
# Submit one ORCA job on the instance, under tmux so it survives disconnection.
#     bash submit.sh <job.inp> [ncores]
#
# There is no queue system here. One job per instance, sized to the instance. Running two
# 16-core jobs on a 16-core instance halves the speed of both and roughly doubles the memory
# pressure; ORCA jobs that swap do not finish.
set -euo pipefail

INP="${1:?usage: submit.sh <job.inp> [ncores]}"
NCORES="${2:-$(nproc)}"
BASE="$(basename "$INP" .inp)"
: "${ORCA_EXE:=/opt/orca/orca}"
: "${ORCA_SCRDIR:=/scratch}"

[ -x "$ORCA_EXE" ] || { echo "ORCA not found at $ORCA_EXE — see vendor/README_ORCA.md" >&2; exit 1; }

# Keep %pal in the input file authoritative; warn if it disagrees with the request.
FILE_PAL="$(grep -ioE '^\s*%pal\s+nprocs\s+[0-9]+' "$INP" | grep -oE '[0-9]+' | head -1 || true)"
if [ -n "$FILE_PAL" ] && [ "$FILE_PAL" != "$NCORES" ]; then
    echo "NOTE: $INP requests %pal nprocs $FILE_PAL; you asked for $NCORES. The file wins." >&2
    NCORES="$FILE_PAL"
fi

WORK="$ORCA_SCRDIR/$BASE"
mkdir -p "$WORK"
cp "$INP" "$WORK/"
[ -f "${INP%.inp}.xyz" ] && cp "${INP%.inp}.xyz" "$WORK/"

echo "==> $BASE on $NCORES cores, scratch $WORK"
tmux new-session -d -s "$BASE" \
    "cd '$WORK' && '$ORCA_EXE' '$BASE.inp' > '$BASE.out' 2>&1; echo \$? > '$BASE.exit'"
echo "    tmux attach -t $BASE      # watch"
echo "    tail -f $WORK/$BASE.out   # or follow the output"
