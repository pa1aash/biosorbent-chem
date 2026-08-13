#!/usr/bin/env python
"""Regenerate ``xtb_prescreen.csv`` from the structure files themselves.

Single source of truth.  Each ``.xyz`` in this directory carries its charge,
multiplicity, method and pre-screen energy in its provenance header, and that
header travels with the coordinates.  Deriving the CSV from the headers rather
than accumulating it as the jobs run means the table cannot describe a geometry
that has since been replaced -- which it otherwise would, because the conformer
search overwrites each structure with its lowest conformer and a new energy.

Run this after any stage that rewrites a structure.

**The energies in this table are not report quantities.**  They are GFN2-xTB
tight-binding values recorded so that the pre-screen is auditable and so that a
later run can detect a structure having silently changed.  Production energies
come from ORCA and from nowhere else.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from geom_utils import normalise_header, read_xyz  # noqa: E402

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "xtb_prescreen.csv"
HARTREE_TO_KJ = 2625.499639

FIELDS = ["species", "label", "formula", "role", "protonation", "metal",
          "charge", "multiplicity", "unpaired_electrons", "unrestricted",
          "n_atoms", "method", "solvation", "opt_level",
          "conformer_search", "conformers_unique", "conformers_within_3kcal",
          "E_xtb_Eh", "E_xtb_kJ_per_mol", "is_report_quantity", "source_file"]


def main() -> int:
    rows = []
    for path in sorted(HERE.glob("*.xyz")):
        normalise_header(path)
        syms, _, h = read_xyz(path)
        energy = h.get("E_xtb_Eh", "")
        rows.append({
            "species": h.get("species", path.stem),
            "label": h.get("label", ""),
            "formula": h.get("formula", ""),
            "role": h.get("role", ""),
            "protonation": h.get("protonation", ""),
            "metal": h.get("metal", "none"),
            "charge": h.get("charge", ""),
            "multiplicity": h.get("mult", ""),
            "unpaired_electrons": h.get("uhf", ""),
            "unrestricted": h.get("uks", ""),
            "n_atoms": len(syms),
            "method": "GFN2-xTB",
            "solvation": "ALPB(water)",
            "opt_level": "tight",
            "conformer_search": h.get("conformer_search", "none"),
            "conformers_unique": h.get("conformers_unique", ""),
            "conformers_within_3kcal": h.get("conformers_within_3kcal", ""),
            "E_xtb_Eh": energy,
            "E_xtb_kJ_per_mol": f"{float(energy) * HARTREE_TO_KJ:.3f}" if energy else "",
            "is_report_quantity": "no",
            "source_file": path.name,
        })

    with CSV_PATH.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {len(rows)} rows to {CSV_PATH.relative_to(HERE.parents[1])}")
    missing = [r["species"] for r in rows if not r["E_xtb_Eh"]]
    if missing:
        print(f"WARNING: no pre-screen energy recorded for: {', '.join(missing)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
