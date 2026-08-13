#!/usr/bin/env python
"""GFN2-xTB pre-optimisation of every starting geometry.

Purpose.  A pre-optimisation, and nothing else.  ORCA time on the compute box is
the scarce resource, so no DFT job should ever start from a hand-built sketch
with eclipsed waters and a flat aromatic ring.  Every structure is relaxed at
GFN2-xTB with the ALPB water model first, and the resulting geometry is what the
production ORCA optimisation will start from.

What the numbers here are, and are not.  The energies written to
``xtb_prescreen.csv`` are semi-empirical tight-binding energies.  They are a
sanity-check reference: they confirm each optimisation converged, they let a
later run detect that a structure has silently changed, and they order
conformers within one species.  They are **not** report quantities, they do not
enter ``data/CANONICAL_NUMBERS.yaml``, and no thermodynamic claim is made from
them.  GFN2-xTB energies for different species are not comparable to each other
in any chemically meaningful way once charge differs.

Solvation.  ALPB(water) is used rather than gas phase because
``dft/DFT_PROTOCOL.md`` §3.3 fixes geometries as solution-phase throughout, and
because gas-phase relaxation of a dianionic ligand or a bare dication produces
structures that do not exist in water.  ALPB is the xtb-level analogue of that
decision, not a substitute for the production SMD treatment.

Run with the ``biosorb`` environment active.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INITIAL = HERE / "initial"
LOGS = HERE / "xtb_logs"
CSV_PATH = HERE / "xtb_prescreen.csv"

HARTREE_TO_KJ = 2625.499639  # CODATA; unit conversion, not a measured quantity


def parse_header(path: Path) -> dict[str, str]:
    """Read the key=value comment line written by build_structures.py."""
    line = path.read_text().splitlines()[1]
    out: dict[str, str] = {}
    for chunk in line.split("|"):
        if "=" in chunk:
            k, _, v = chunk.strip().partition("=")
            out[k.strip()] = v.strip()
    return out


def run_xtb(xyz: Path, charge: int, uhf: int, workdir: Path) -> tuple[Path, str]:
    """Optimise one structure.  Returns (optimised xyz path, stdout)."""
    shutil.copy(xyz, workdir / "in.xyz")
    cmd = [
        "xtb", "in.xyz",
        "--gfn", "2",
        "--opt", "tight",
        "--chrg", str(charge),
        "--uhf", str(uhf),
        "--alpb", "water",
    ]
    proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=3600)
    return workdir / "xtbopt.xyz", proc.stdout + proc.stderr


def extract(stdout: str) -> dict[str, str]:
    out = {"E_total_Eh": "", "gradient_norm": "", "homo_lumo_gap_eV": "",
           "converged": "false", "normal_termination": "false"}
    m = re.search(r"\|\s*TOTAL ENERGY\s+(-?\d+\.\d+)\s+Eh", stdout)
    if m:
        out["E_total_Eh"] = m.group(1)
    m = re.search(r"\|\s*GRADIENT NORM\s+(-?\d+\.\d+)\s+Eh", stdout)
    if m:
        out["gradient_norm"] = m.group(1)
    m = re.search(r"\|\s*HOMO-LUMO GAP\s+(-?\d+\.\d+)\s+eV", stdout)
    if m:
        out["homo_lumo_gap_eV"] = m.group(1)
    if "GEOMETRY OPTIMIZATION CONVERGED" in stdout:
        out["converged"] = "true"
    if "normal termination of xtb" in stdout:
        out["normal_termination"] = "true"
    return out


def rewrite_with_header(src: Path, dst: Path, header: dict[str, str], energy: str) -> None:
    """Copy the optimised geometry out, restoring the provenance comment line.

    xtb overwrites line 2 of xtbopt.xyz with its own energy string, which would
    destroy the charge/multiplicity header the ORCA input generator depends on.
    """
    lines = src.read_text().splitlines()
    n = lines[0].strip()
    fields = [f"{k}={v}" for k, v in header.items() if k != "builder"]
    fields.append("preopt=GFN2-xTB/ALPB(water)/opt-tight")
    fields.append(f"E_xtb_Eh={energy}")
    fields.append("preopt_is_not_a_report_quantity=true")
    fields.append("builder=build_structures.py+run_xtb_preopt.py")
    body = lines[2:2 + int(n)]
    dst.write_text("\n".join([n, " | ".join(fields), *body]) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="restrict to these species names")
    args = ap.parse_args()

    LOGS.mkdir(parents=True, exist_ok=True)
    targets = sorted(INITIAL.glob("*.xyz"))
    if args.only:
        targets = [t for t in targets if t.stem in set(args.only)]

    rows = []
    failures = []
    for xyz in targets:
        header = parse_header(xyz)
        charge = int(header["charge"])
        uhf = int(header["uhf"])
        name = header["species"]
        print(f"[xtb] {name:<20s} q={charge:+d} uhf={uhf} ...", flush=True)

        with tempfile.TemporaryDirectory() as td:
            wd = Path(td)
            try:
                opt_xyz, log = run_xtb(xyz, charge, uhf, wd)
            except subprocess.TimeoutExpired:
                failures.append((name, "timeout after 3600 s"))
                continue
            (LOGS / f"{name}.xtblog").write_text(log)
            info = extract(log)
            if not opt_xyz.exists() or info["converged"] != "true":
                failures.append((name, f"converged={info['converged']} "
                                       f"normal_termination={info['normal_termination']}"))
                print(f"       FAILED: {failures[-1][1]}")
                continue
            rewrite_with_header(opt_xyz, HERE / f"{name}.xyz", header, info["E_total_Eh"])

        rows.append({
            "species": name,
            "label": header.get("label", ""),
            "formula": header.get("formula", ""),
            "role": header.get("role", ""),
            "protonation": header.get("protonation", ""),
            "metal": header.get("metal", ""),
            "charge": header["charge"],
            "multiplicity": header["mult"],
            "unpaired_electrons": header["uhf"],
            "unrestricted": header.get("uks", ""),
            "n_atoms": xyz.read_text().splitlines()[0].strip(),
            "method": "GFN2-xTB",
            "solvation": "ALPB(water)",
            "opt_level": "tight",
            "E_total_Eh": info["E_total_Eh"],
            "E_total_kJ_per_mol": (f"{float(info['E_total_Eh']) * HARTREE_TO_KJ:.3f}"
                                   if info["E_total_Eh"] else ""),
            "gradient_norm_Eh": info["gradient_norm"],
            "homo_lumo_gap_eV": info["homo_lumo_gap_eV"],
            "converged": info["converged"],
            "normal_termination": info["normal_termination"],
            "log": f"xtb_logs/{name}.xtblog",
        })
        print(f"       E = {info['E_total_Eh']} Eh   gap = {info['homo_lumo_gap_eV']} eV")

    if rows:
        # The CSV is regenerated from the structure headers by
        # emit_prescreen_csv.py, which is the single writer of that file.  Doing
        # it there rather than here keeps the table from describing a geometry
        # that a later stage has since replaced.
        print(f"\n{len(rows)} structures optimised. "
              f"Run emit_prescreen_csv.py to refresh {CSV_PATH.name}.")

    if failures:
        print("\nFAILURES:")
        for name, why in failures:
            print(f"  {name}: {why}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
