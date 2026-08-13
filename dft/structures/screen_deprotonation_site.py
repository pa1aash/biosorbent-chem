#!/usr/bin/env python
"""Which hydroxyl is removed in the P1 (mono-deprotonated) ligand state?

``dft/DFT_PROTOCOL.md`` §1.3 fixes the *charge* of each protonation state but not
the *site*.  Methyl gallate has three phenolic hydroxyls, so LH- is three
distinct isomers, and picking one by assertion would be exactly the kind of bare
assumption the protocol was written to avoid.

The three isomers are therefore built and pre-screened here at GFN2-xTB with the
ALPB water model.  The screen is semi-empirical and is used only to order the
isomers and to check that the ordering is not marginal; the site carried into the
production calculations is confirmed at the DFT level before any free energy is
quoted from it.  No number produced by this script is a report quantity.

Isomer labels follow the 3,4,5-trihydroxybenzoate numbering, with C1 bearing the
methyl ester:

    P1-4OH  deprotonated at the 4-position, para to the ester
    P1-3OH  deprotonated at the 3-position (equivalent to the 5-position by the
            local mirror plane of the galloyl group)

Run with the ``biosorb`` environment active.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_structures import build_methyl_gallate, write_xyz, Species  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "screens"
HARTREE_TO_KJ = 2625.499639


def build_isomer(site: str) -> Species:
    atoms, km = build_methyl_gallate()
    hkey = {"4OH": "H4", "3OH": "H3", "5OH": "H5"}[site]
    drop = km[hkey]
    idx = [i for i in range(len(atoms)) if i != drop]
    remap = {old: new for new, old in enumerate(idx)}
    return Species(
        name=f"lig_P1_{site}", label=f"LH- deprotonated at the {site[0]}-position",
        charge=-1, mult=1, atoms=[atoms[i] for i in idx],
        note="P1 deprotonation-site screen.", role="ligand", protonation="P1",
        donor_indices=[remap[km["O3"]], remap[km["O4"]]],
    )


def xtb_energy(path: Path, charge: int, uhf: int) -> float:
    with tempfile.TemporaryDirectory() as td:
        wd = Path(td)
        (wd / "in.xyz").write_text(path.read_text())
        proc = subprocess.run(
            ["xtb", "in.xyz", "--gfn", "2", "--opt", "tight",
             "--chrg", str(charge), "--uhf", str(uhf), "--alpb", "water"],
            cwd=wd, capture_output=True, text=True, timeout=1800)
        if "GEOMETRY OPTIMIZATION CONVERGED" not in proc.stdout:
            raise RuntimeError(f"xtb did not converge for {path.name}")
        (OUT / f"{path.stem}.xtblog").write_text(proc.stdout)
        (OUT / f"{path.stem}_opt.xyz").write_text((wd / "xtbopt.xyz").read_text())
        for line in proc.stdout.splitlines():
            if "TOTAL ENERGY" in line:
                return float(line.split()[3])
    raise RuntimeError("no total energy found")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for site in ("4OH", "3OH", "5OH"):
        sp = build_isomer(site)
        p = OUT / f"{sp.name}.xyz"
        write_xyz(p, sp)
        e = xtb_energy(p, sp.charge, sp.uhf)
        results.append({"isomer": sp.name, "site": site, "E_Eh": e})
        print(f"{sp.name:<14s} E = {e:.8f} Eh", flush=True)

    e0 = min(r["E_Eh"] for r in results)
    for r in results:
        r["rel_kJ_per_mol"] = round((r["E_Eh"] - e0) * HARTREE_TO_KJ, 2)
    results.sort(key=lambda r: r["rel_kJ_per_mol"])

    print("\nRelative energies (GFN2-xTB/ALPB(water), pre-screen only):")
    for r in results:
        print(f"  {r['isomer']:<14s} {r['rel_kJ_per_mol']:+8.2f} kJ/mol")

    (OUT / "p1_deprotonation_site.json").write_text(json.dumps(
        {"method": "GFN2-xTB/ALPB(water)/opt-tight",
         "is_a_report_quantity": False,
         "purpose": "order the three LH- isomers; DFT confirmation required",
         "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
