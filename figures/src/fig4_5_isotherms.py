"""fig4_5_isotherms

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
OUT = ROOT / "figures" / "out" / "fig4_5_isotherms.pdf"


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
