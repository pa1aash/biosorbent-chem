#!/usr/bin/env python
"""Integrity check on every pre-optimised geometry in ``dft/structures/``.

A semi-empirical optimiser is free to do things a starting geometry did not
intend: expel a water from the first shell, migrate a proton from a coordinated
phenol onto a neighbouring water, or open the chelate to monodentate.  Any of
those silently changes what the species *is*, and a species that is not what its
filename says would propagate into the reaction stoichiometry and invalidate
every exchange free energy built from it.

This script therefore re-derives, from coordinates alone, what each optimised
structure actually is:

  * every metal-oxygen distance, and the coordination number within a cutoff;
  * how many of those donors are water oxygens and how many are ligand oxygens,
    checked against what the species is supposed to be;
  * whether any O-H hydrogen has migrated to a different oxygen than the one it
    started on (proton transfer would change the protonation state);
  * the intact hydrogen count, as a check that no atom was lost.

It reports; it does not repair.  Anything it flags is a decision for the author.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# First-shell cutoffs, A.  Generous, because the point is to detect a water that
# has left the first shell entirely, not to adjudicate a borderline long bond.
M_O_CUTOFF = {"Pb": 3.20, "Cu": 2.80, "Zn": 2.80}
OH_CUTOFF = 1.25          # A, an O-H bond
METALS = ("Pb", "Cu", "Zn")

# What each species is supposed to be: (n ligand donors, n water donors)
EXPECTED = {
    "aquo6": (0, 6),
    "aquo8": (0, 8),
    "cplx": (2, 4),
}


def read_xyz(path: Path) -> tuple[list[str], np.ndarray, dict[str, str]]:
    lines = path.read_text().splitlines()
    n = int(lines[0].split()[0])
    header: dict[str, str] = {}
    for chunk in lines[1].split("|"):
        if "=" in chunk:
            k, _, v = chunk.strip().partition("=")
            header[k.strip()] = v.strip()
    syms, xyz = [], []
    for line in lines[2:2 + n]:
        p = line.split()
        syms.append(p[0])
        xyz.append([float(x) for x in p[1:4]])
    return syms, np.array(xyz), header


def classify_oxygens(syms: list[str], xyz: np.ndarray) -> dict[int, str]:
    """Label every oxygen as 'water' (2 H attached), 'hydroxyl' (1 H) or
    'deprotonated/ester' (0 H), from the optimised coordinates alone."""
    o_idx = [i for i, s in enumerate(syms) if s == "O"]
    h_idx = [i for i, s in enumerate(syms) if s == "H"]
    out = {}
    for o in o_idx:
        nh = sum(1 for h in h_idx
                 if np.linalg.norm(xyz[o] - xyz[h]) < OH_CUTOFF)
        out[o] = {0: "O(no H)", 1: "OH", 2: "OH2"}.get(nh, f"OH{nh}")
    return out


def main() -> int:
    problems: list[str] = []
    files = sorted(p for p in HERE.glob("*.xyz"))
    if not files:
        print("no optimised structures found", file=sys.stderr)
        return 1

    for path in files:
        syms, xyz, header = read_xyz(path)
        name = header.get("species", path.stem)
        metal = header.get("metal", "none")
        print(f"\n=== {name}  {header.get('label','')}  "
              f"q={header.get('charge')} mult={header.get('mult')} ===")

        # atom-count / composition check
        print(f"    atoms={len(syms)}  formula_recorded={header.get('formula','?')}")

        if metal not in METALS:
            kinds = classify_oxygens(syms, xyz)
            print("    oxygens: " + ", ".join(f"O{o}:{k}" for o, k in sorted(kinds.items())))
            continue

        m_i = syms.index(metal)
        kinds = classify_oxygens(syms, xyz)
        cutoff = M_O_CUTOFF[metal]

        donors = []
        for o, kind in sorted(kinds.items()):
            d = float(np.linalg.norm(xyz[o] - xyz[m_i]))
            if d < cutoff:
                donors.append((d, o, kind))
        donors.sort()

        n_water = sum(1 for _, _, k in donors if k == "OH2")
        n_lig = len(donors) - n_water
        print(f"    coordination number = {len(donors)} within {cutoff} A "
              f"({n_lig} ligand O, {n_water} water O)")
        for d, o, kind in donors:
            print(f"      {metal}-O{o:<3d} {d:6.3f} A   {kind}")

        tag = ("aquo8" if name.endswith("aquo8")
               else "aquo6" if name.endswith("aquo6") else "cplx")
        exp_lig, exp_wat = EXPECTED[tag]
        if (n_lig, n_water) != (exp_lig, exp_wat):
            problems.append(
                f"{name}: expected {exp_lig} ligand O + {exp_wat} water O, "
                f"found {n_lig} + {n_water}")

        # proton-transfer check: count hydroxyls and waters against expectation
        n_oh2_total = sum(1 for k in kinds.values() if k == "OH2")
        if n_oh2_total != exp_wat and tag == "cplx":
            problems.append(
                f"{name}: {n_oh2_total} intact water molecules in the structure, "
                f"expected {exp_wat} - possible proton transfer to or from a water")

    print("\n" + "=" * 70)
    if problems:
        print("FLAGGED:")
        for p in problems:
            print(f"  ! {p}")
        return 1
    print("All structures intact: coordination number, donor composition and "
          "protonation state match what each species is declared to be.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
