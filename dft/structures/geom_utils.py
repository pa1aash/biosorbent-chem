#!/usr/bin/env python
"""Shared geometry utilities for the structure-preparation stage.

Kept in one place because two different consumers need exactly the same
definition of "is this structure still the species it claims to be":
``check_geometries.py`` applies it to the pre-optimised structures, and
``run_crest.py`` applies it to every member of a conformer ensemble.  If the two
used different connectivity rules, a conformer could pass one check and fail the
other for no chemical reason.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

# Covalent radii, A.  Cordero et al. scale; used only for connectivity
# perception, never for a reported distance.
COVALENT_RADII = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66,
                  "Cu": 1.32, "Zn": 1.22, "Pb": 1.46}

BOND_TOLERANCE = 1.25     # a pair is bonded below this multiple of the radius sum
OH_CUTOFF = 1.25          # A, an O-H bond
METALS = ("Pb", "Cu", "Zn")

# First-shell cutoffs, A.  Deliberately generous: the purpose is to notice a
# water that has left the first shell, not to adjudicate a long bond.
M_O_CUTOFF = {"Pb": 3.20, "Cu": 2.80, "Zn": 2.80}


def parse_header(source) -> dict[str, str]:
    """Read the ``key=value | key=value`` provenance line written by the builder.

    A ``Path`` is read from disk; a ``str`` is parsed as the header line itself.
    The distinction is made on type rather than by testing whether the string
    happens to name an existing file: a header line is long enough to overflow
    the filesystem's name limit, and probing it as a path raises rather than
    returning False.

    Later keys win, so a header that accumulated a duplicate key across reruns
    parses to the most recent value.  ``normalise_header`` rewrites such a file.
    """
    line = Path(source).read_text().splitlines()[1] if isinstance(source, Path) else str(source)
    out: dict[str, str] = {}
    for chunk in line.split("|"):
        if "=" in chunk:
            k, _, v = chunk.strip().partition("=")
            out[k.strip()] = v.strip()
    return out


def read_xyz(path: Path) -> tuple[list[str], np.ndarray, dict[str, str]]:
    lines = Path(path).read_text().splitlines()
    n = int(lines[0].split()[0])
    header = parse_header(lines[1])
    syms = [l.split()[0] for l in lines[2:2 + n]]
    xyz = np.array([[float(v) for v in l.split()[1:4]] for l in lines[2:2 + n]])
    return syms, xyz, header


def read_multi_xyz(path: Path) -> list[tuple[float, list[str], np.ndarray]]:
    """Read a CREST-style concatenated XYZ ensemble."""
    if not Path(path).exists():
        return []
    lines = Path(path).read_text().splitlines()
    out, i = [], 0
    while i < len(lines) and lines[i].strip():
        n = int(lines[i].split()[0])
        try:
            energy = float(lines[i + 1].split()[0])
        except (ValueError, IndexError):
            energy = float("nan")
        block = lines[i + 2:i + 2 + n]
        syms = [l.split()[0] for l in block]
        xyz = np.array([[float(v) for v in l.split()[1:4]] for l in block])
        out.append((energy, syms, xyz))
        i += n + 2
    return out


def covalent_bonds(syms: list[str], xyz: np.ndarray) -> set[tuple[int, int]]:
    """Connectivity of the non-metal framework.

    Metals are excluded on purpose.  A dative metal-oxygen contact is not a
    covalent bond, and including it would make the connectivity fingerprint
    change whenever a bond length crossed an arbitrary radius sum -- which is
    precisely the false positive that makes CREST's own topology check unusable
    for these complexes.  Metal coordination is checked separately, by distance.
    """
    idx = [i for i, s in enumerate(syms) if s not in METALS]
    bonds = set()
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            i, j = idx[a], idx[b]
            limit = BOND_TOLERANCE * (COVALENT_RADII[syms[i]] + COVALENT_RADII[syms[j]])
            if float(np.linalg.norm(xyz[i] - xyz[j])) < limit:
                bonds.add((i, j))
    return bonds


def classify_oxygens(syms: list[str], xyz: np.ndarray) -> dict[int, str]:
    """Label each oxygen by how many hydrogens are attached: OH2 / OH / O(no H)."""
    h_idx = [i for i, s in enumerate(syms) if s == "H"]
    out = {}
    for o, s in enumerate(syms):
        if s != "O":
            continue
        nh = sum(1 for h in h_idx if float(np.linalg.norm(xyz[o] - xyz[h])) < OH_CUTOFF)
        out[o] = {0: "O(no H)", 1: "OH", 2: "OH2"}.get(nh, f"OH{nh}")
    return out


def metal_donors(syms: list[str], xyz: np.ndarray, metal: str
                 ) -> list[tuple[float, int, str]]:
    """Sorted (distance, oxygen index, protonation label) for the first shell."""
    m = syms.index(metal)
    kinds = classify_oxygens(syms, xyz)
    cutoff = M_O_CUTOFF[metal]
    donors = [(float(np.linalg.norm(xyz[o] - xyz[m])), o, kind)
              for o, kind in kinds.items()
              if float(np.linalg.norm(xyz[o] - xyz[m])) < cutoff]
    return sorted(donors)


def coordination_signature(syms: list[str], xyz: np.ndarray, metal: str
                           ) -> tuple[int, int]:
    """(number of ligand oxygens, number of water oxygens) in the first shell."""
    donors = metal_donors(syms, xyz, metal)
    n_water = sum(1 for _, _, k in donors if k == "OH2")
    return len(donors) - n_water, n_water


# Canonical field order for a structure header.  Anything not listed keeps its
# relative order after these.
HEADER_ORDER = ["charge", "mult", "uhf", "uks", "species", "label", "formula",
                "role", "protonation", "metal", "config", "ligand_source",
                "preopt", "conformer_search", "conformers_unique",
                "conformers_within_3kcal", "E_xtb_Eh",
                "preopt_is_not_a_report_quantity", "builder"]


def normalise_header(path: Path) -> bool:
    """Rewrite a structure's header in canonical order with duplicates collapsed.

    Reruns of a stage append their provenance fields, so a file re-processed
    twice can carry the same key twice.  Parsing is last-wins so the values stay
    correct, but a file that lists two different conformer counts is misleading
    to read and worse to cite.  Returns True if the file changed.
    """
    lines = Path(path).read_text().splitlines()
    header = parse_header(lines[1])
    ordered = [k for k in HEADER_ORDER if k in header]
    ordered += [k for k in header if k not in HEADER_ORDER]
    rebuilt = " | ".join(f"{k}={header[k]}" for k in ordered)
    if rebuilt == lines[1]:
        return False
    lines[1] = rebuilt
    Path(path).write_text("\n".join(lines) + "\n")
    return True
