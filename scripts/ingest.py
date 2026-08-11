#!/usr/bin/env python3
r"""Validate a CSV dropped into data/provided/ against its template schema.

REPORTS MISMATCHES; NEVER SILENTLY COERCES. A file that does not match its
schema is rejected with an explanation, because a quietly repaired dataset is
indistinguishable from a correct one and this project cannot afford that.

    python scripts/ingest.py                       # validate everything present
    python scripts/ingest.py data/provided/batch/isotherm_single_metal.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDED = ROOT / "data" / "provided"
TEMPLATES = PROVIDED / "templates"


def template_for(path: Path) -> Path | None:
    exact = TEMPLATES / path.name
    if exact.exists():
        return exact
    for cand in TEMPLATES.glob("*.csv"):
        stem = cand.stem.replace("_TEMPLATE", "")
        if path.stem.startswith(stem) or stem.startswith(path.stem.split("_")[0]):
            return cand
    return None


def headers(p: Path) -> list[str]:
    with p.open(newline="") as fh:
        return next(csv.reader(fh), [])


def validate(path: Path) -> tuple[bool, list[str]]:
    msgs = []
    tpl = template_for(path)
    if tpl is None:
        return False, [f"no template found in {TEMPLATES.relative_to(ROOT)} for {path.name}",
                       "  add one, or rename the file to match an existing template"]
    want, got = headers(tpl), headers(path)
    missing = [c for c in want if c not in got]
    extra = [c for c in got if c not in want]

    if missing:
        msgs.append(f"MISSING column(s): {', '.join(missing)}")
    if extra:
        msgs.append(f"extra column(s) (kept, not an error): {', '.join(extra)}")
    if got[:len(want)] != want and not missing:
        msgs.append("column ORDER differs from the template (accepted; read by name)")

    with path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        msgs.append("file has a header but NO DATA ROWS")

    # Empty cells are legitimate: an unrecorded value is left blank, never guessed.
    blanks = {c: sum(1 for r in rows if not (r.get(c) or "").strip()) for c in want if c in got}
    filled = [f"{c}:{len(rows)-n}/{len(rows)}" for c, n in blanks.items() if n and n < len(rows)]
    allblank = [c for c, n in blanks.items() if rows and n == len(rows)]
    if allblank:
        msgs.append(f"entirely empty column(s): {', '.join(allblank)}")

    ok = not missing and bool(rows)
    msgs.insert(0, f"template: {tpl.name}   rows: {len(rows)}   columns: {len(got)}")
    return ok, msgs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()

    targets = [Path(f) for f in args.files] if args.files else \
        [p for p in sorted(PROVIDED.rglob("*.csv")) if TEMPLATES not in p.parents]

    if not targets:
        print("ingest: no data files present in data/provided/ yet.")
        print("  This is expected. See docs/DATA_REQUEST.md for what to send and in")
        print("  what order; empty templates with the exact headers are in")
        print(f"  {TEMPLATES.relative_to(ROOT)}/")
        return 0

    bad = 0
    for path in targets:
        ok, msgs = validate(path)
        state = "OK  " if ok else "FAIL"
        print(f"[{state}] {path.relative_to(ROOT)}")
        for m in msgs:
            print(f"         {m}")
        if not ok:
            bad += 1
    print(f"\ningest: {len(targets)-bad} valid, {bad} rejected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
