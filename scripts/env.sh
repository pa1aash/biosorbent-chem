#!/usr/bin/env bash
# Chem-151 — environment activation. EVERY other script sources this file.
#
#     source scripts/env.sh
#
# Sets: the biosorb Python environment, ORCA and Multiwfn on PATH, TeX on PATH,
# and CHEM151_ROOT. Safe to source repeatedly.

# Resolve the repository root regardless of where this is sourced from.
if [ -n "${BASH_SOURCE[0]}" ]; then
    _CHEM151_SELF="${BASH_SOURCE[0]}"
else
    _CHEM151_SELF="$0"
fi
CHEM151_ROOT="$(cd "$(dirname "$_CHEM151_SELF")/.." && pwd)"
export CHEM151_ROOT
unset _CHEM151_SELF

# ── Python environment ────────────────────────────────────────────────────────
# Prefer the conda env's bin directly: it needs no shell hook and works in
# non-interactive contexts, cron and Makefiles.
CHEM151_PYENV="${CHEM151_PYENV:-/opt/homebrew/Caskroom/miniforge/base/envs/biosorb}"
if [ -x "$CHEM151_PYENV/bin/python" ]; then
    export PATH="$CHEM151_PYENV/bin:$PATH"
    export CHEM151_PYTHON="$CHEM151_PYENV/bin/python"
else
    echo "env.sh: WARNING — biosorb environment not found at $CHEM151_PYENV" >&2
    echo "env.sh:           run 'mamba env create -f environment.yml'" >&2
    export CHEM151_PYTHON="$(command -v python3 || echo python3)"
fi

# ── TeX ───────────────────────────────────────────────────────────────────────
for _d in /Library/TeX/texbin /usr/local/texlive/2026basic/bin/universal-darwin; do
    [ -d "$_d" ] && case ":$PATH:" in *":$_d:"*) ;; *) export PATH="$_d:$PATH" ;; esac
done
unset _d

# ── ORCA ──────────────────────────────────────────────────────────────────────
# NOT redistributed. Register at https://orcaforum.kofo.mpg.de/ and unpack into
# vendor/orca/. See vendor/README_ORCA.md.
CHEM151_ORCA="${CHEM151_ORCA:-$CHEM151_ROOT/vendor/orca}"
if [ -x "$CHEM151_ORCA/orca" ]; then
    export PATH="$CHEM151_ORCA:$PATH"
    export LD_LIBRARY_PATH="$CHEM151_ORCA:${LD_LIBRARY_PATH:-}"
    export DYLD_LIBRARY_PATH="$CHEM151_ORCA:${DYLD_LIBRARY_PATH:-}"
    # ORCA must be launched by ABSOLUTE PATH for parallel jobs; the MPI wrapper
    # re-executes it. A bare `orca job.inp` silently runs serial.
    export ORCA_EXE="$CHEM151_ORCA/orca"
fi

# ── Multiwfn ──────────────────────────────────────────────────────────────────
# Free binary, manual download. See vendor/README_MULTIWFN.md.
CHEM151_MULTIWFN="${CHEM151_MULTIWFN:-$CHEM151_ROOT/vendor/multiwfn}"
if [ -d "$CHEM151_MULTIWFN" ]; then
    export PATH="$CHEM151_MULTIWFN:$PATH"
    [ -f "$CHEM151_MULTIWFN/settings.ini" ] && export Multiwfnpath="$CHEM151_MULTIWFN"
fi

# ── Reproducibility ───────────────────────────────────────────────────────────
export MPLBACKEND="${MPLBACKEND:-Agg}"     # figures render headless
export PYTHONHASHSEED=0                     # deterministic dict ordering
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1755000000}"  # reproducible PDF timestamps

# ── Status ────────────────────────────────────────────────────────────────────
chem151_status() {
    printf '%-14s %s\n' "root"     "$CHEM151_ROOT"
    printf '%-14s %s\n' "python"   "$($CHEM151_PYTHON --version 2>&1)"
    printf '%-14s %s\n' "latexmk"  "$(command -v latexmk || echo 'NOT FOUND')"
    printf '%-14s %s\n' "biber"    "$(command -v biber   || echo 'NOT FOUND')"
    printf '%-14s %s\n' "orca"     "$(command -v orca    || echo 'NOT INSTALLED — see vendor/README_ORCA.md')"
    printf '%-14s %s\n' "Multiwfn" "$(command -v Multiwfn || echo 'NOT INSTALLED — see vendor/README_MULTIWFN.md')"
    printf '%-14s %s\n' "xtb"      "$(command -v xtb     || echo 'NOT FOUND')"
}

[ "${CHEM151_ENV_QUIET:-0}" = "1" ] || echo "env.sh: biosorb ready at $CHEM151_ROOT (chem151_status for detail)"
