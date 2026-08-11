#!/usr/bin/env python3
r"""Scaffold figures/src/NAME.py preloaded with the house style.

    python scripts/new_figure.py fig4_5_isotherms
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "figures" / "src"

TEMPLATE = '''"""{name}

Owning script for a figure in the Chem-151 report. See figures/FIGURE_REGISTER.md
for the registry entry this satisfies.

RULES (figures/STYLE.md, enforced by analysis/src/style.py):
  - one fixed colour per metal, identical in EVERY figure in the document
  - every axis labelled with quantity AND unit
  - error bars mandatory, or an explicit stated reason for their absence
  - multi-panel labels (a) (b) (c) under one unified caption
  - >= 300 dpi
  - never a software screenshot; everything is re-plotted from data

This script READS data and WRITES exactly one figure. It holds no data of its
own and no hard-coded results.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis" / "src"))
import style  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "figures" / "out" / "{name}.pdf"


def main() -> None:
    fig, ax = style.figure()

    # ------------------------------------------------------------------
    # Load from data/provided/ or data/processed/ -- never inline numbers.
    #
    #   import pandas as pd
    #   df = pd.read_csv(ROOT / "data" / "provided" / "..." / "....csv")
    #
    # If the dataset has not been supplied yet, DO NOT invent plausible data
    # to see what the figure looks like. Leave this script unrun; the report
    # carries a NEEDSDATA placeholder until the file arrives.
    # ------------------------------------------------------------------

    ax.set_xlabel("QUANTITY / UNIT")
    ax.set_ylabel("QUANTITY / UNIT")

    style.save(fig, OUT)


if __name__ == "__main__":
    main()
'''


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    name = sys.argv[1]
    if name.endswith(".py"):
        name = name[:-3]
    path = SRC / f"{name}.py"
    if path.exists():
        print(f"new_figure: {path.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1
    SRC.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(name=name))
    print(f"new_figure: created {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
