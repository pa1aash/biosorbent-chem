#!/usr/bin/env python3
r"""data/CANONICAL_NUMBERS.yaml -> report/preamble/numbers.tex

THE CANONICAL-NUMBERS RULE (CLAUDE.md section 5): no numeric result may be
hard-coded in any .tex file. Every number reaches LaTeX through \num{key},
generated here.

Refuses to emit a PENDING value except under --draft, where it emits nothing for
that key so that \num{} renders a visible missing-number marker instead.

    python scripts/emit_numbers.py --draft    # tolerant; used by `make draft`
    python scripts/emit_numbers.py            # strict; used by `make final`
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "CANONICAL_NUMBERS.yaml"
OUT = ROOT / "report" / "preamble" / "numbers.tex"

REQUIRED_FIELDS = {"value", "uncertainty", "n", "units", "source_dataset", "status"}


def sigfig_pair(value: float, uncertainty: float | None) -> str:
    """Render value +- uncertainty with the value rounded to the uncertainty.

    Bible section 12 and anti-pattern 3: a capacity of 40.11 mg/g implies four
    significant figures, which the measurement must support. If the replicate SD
    is +-2, the value is 40.1 +- 2.0. Over-precise numbers are a classic tell of
    unexamined output, so the rounding is done here, once, rather than left to
    whoever types the sentence.
    """
    if uncertainty is None or uncertainty == 0:
        return _plain(value)
    # Round the uncertainty to one significant figure (two if it starts with 1),
    # then round the value to the same decimal place.
    exp = math.floor(math.log10(abs(uncertainty)))
    lead = uncertainty / 10 ** exp
    digits = 2 if lead < 2.0 else 1
    dp = -(exp - (digits - 1))
    u = round(uncertainty, dp)
    v = round(value, dp)
    if dp <= 0:
        return rf"{int(v)} \pm {int(u)}"
    return rf"{v:.{dp}f} \pm {u:.{dp}f}"


def _plain(value) -> str:
    if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
        return str(int(value))
    return f"{value:g}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--draft", action="store_true",
                    help="tolerate PENDING entries; emit nothing for them")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"emit_numbers: {SRC} not found", file=sys.stderr)
        return 2

    data = yaml.safe_load(SRC.read_text()) or {}

    verified, pending, malformed = [], [], []
    for key, entry in data.items():
        if not isinstance(entry, dict):
            malformed.append((key, "entry is not a mapping"))
            continue
        missing = REQUIRED_FIELDS - set(entry)
        if missing:
            malformed.append((key, f"missing field(s): {', '.join(sorted(missing))}"))
            continue
        status = str(entry["status"]).upper()
        if status == "VERIFIED":
            if entry["value"] is None:
                malformed.append((key, "status VERIFIED but value is null"))
                continue
            verified.append((key, entry))
        elif status == "PENDING":
            pending.append(key)
        else:
            malformed.append((key, f"unknown status {entry['status']!r}"))

    if malformed:
        print("emit_numbers: MALFORMED ENTRIES", file=sys.stderr)
        for k, why in malformed:
            print(f"  {k}: {why}", file=sys.stderr)
        return 2

    if pending and not args.draft:
        print(f"emit_numbers: REFUSING TO EMIT -- {len(pending)} key(s) still PENDING.",
              file=sys.stderr)
        print("  A PENDING number has no evidence behind it. Supply the dataset, derive",
              file=sys.stderr)
        print("  the value, set status: VERIFIED. Do not hand-edit a value in.",
              file=sys.stderr)
        for k in sorted(pending)[:20]:
            print(f"    {k}", file=sys.stderr)
        if len(pending) > 20:
            print(f"    ... and {len(pending) - 20} more", file=sys.stderr)
        print("  Use --draft to build a draft with visible markers instead.", file=sys.stderr)
        return 1

    lines = [
        "% ==========================================================================",
        "% numbers.tex -- GENERATED FILE. DO NOT EDIT.",
        "%",
        "% Written by scripts/emit_numbers.py from data/CANONICAL_NUMBERS.yaml.",
        "% Edit the YAML, then run `make numbers`.",
        "%",
        f"% VERIFIED keys emitted : {len(verified)}",
        f"% PENDING keys skipped  : {len(pending)}",
        "%",
        "% A key that is still PENDING is deliberately absent, so that \\num{key}",
        "% renders a visible missing-number marker rather than silently nothing.",
        "% ==========================================================================",
        "",
    ]
    for key, e in sorted(verified):
        rendered = sigfig_pair(float(e["value"]),
                               float(e["uncertainty"]) if e["uncertainty"] is not None else None)
        note = f"  % {e['units']}"
        if e.get("n"):
            note += f", n = {e['n']}"
        note += f", from {e['source_dataset']}"
        lines.append(rf"\DeclareNum{{{key}}}{{\ensuremath{{{rendered}}}}}{note}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")

    mode = "draft" if args.draft else "final"
    print(f"emit_numbers [{mode}]: {len(verified)} verified emitted, "
          f"{len(pending)} pending skipped -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
