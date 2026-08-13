#!/usr/bin/env python
"""Build every starting geometry for the computational arm of Chem-151.

Provenance
----------
This script is the sole origin of every ``.xyz`` file in ``dft/structures/``.
Nothing here is hand-edited afterwards.  The pipeline is

    build_structures.py  ->  initial/*.xyz  ->  xtb GFN2/ALPB(water) opt  ->  *.xyz

and the GFN2-xTB stage is a *pre-optimisation only*.  No energy produced by this
script or by the xtb stage is a report quantity; the xtb energies exist solely as
a sanity-check reference recorded in ``xtb_prescreen.csv``.  Production energies
come from ORCA at the level of theory fixed in ``dft/DFT_PROTOCOL.md`` §3 and
from nowhere else.

Scope
-----
Species set is taken verbatim from ``dft/DFT_PROTOCOL.md`` §8 (job inventory),
§1.3 (three protonation states P0/P1/P2), §2 (aquo-ligand exchange, Pb tested at
both n = 6 and n = 8) and §3.2 (charge and multiplicity for every species).

Starting geometries are deliberately *symmetric*: the metal coordination sphere
is built as an ideal polyhedron.  No hemidirected distortion is imposed on any
Pb starting structure.  Hemidirection is a quantity to be measured from the
optimised geometry (§5, attack A14), so building it into the input would beg the
question the calculation is supposed to answer.

Run with the ``biosorb`` environment active.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

HERE = Path(__file__).resolve().parent
INITIAL = HERE / "initial"

# ── Geometry constants ────────────────────────────────────────────────────────
# Starting-guess bond lengths only.  These are conventional coordination-chemistry
# starting values, refined immediately by GFN2-xTB and then by DFT; they are never
# reported and never enter CANONICAL_NUMBERS.yaml.
R_OH = 0.958          # A, water O-H
A_HOH = 104.5         # deg, water H-O-H

M_O_AQUO = {          # metal - O(water) starting guess, A
    "Pb": 2.55,
    "Cu": 2.00,       # equatorial; axial elongated below
    "Zn": 2.10,
}
CU_AXIAL_ELONGATION = 0.33   # A, Jahn-Teller axial elongation starting guess for d9

M_O_LIGAND = {        # metal - O(phenolate/phenol) starting guess, A
    "Pb": 2.40,
    "Cu": 1.95,
    "Zn": 2.00,
}

METAL_MULT = {"Pb": 1, "Cu": 2, "Zn": 1}   # DFT_PROTOCOL.md §3.2
METAL_CONFIG = {
    "Pb": "6s2, closed shell",
    "Cu": "d9, OPEN SHELL DOUBLET (UKS)",
    "Zn": "d10, closed shell",
}

# Methyl gallate: methyl 3,4,5-trihydroxybenzoate, C8H8O5.  DFT_PROTOCOL.md §1.2.
METHYL_GALLATE_SMILES = "COC(=O)c1cc(O)c(O)c(O)c1"


# ── Small vector helpers ──────────────────────────────────────────────────────
def unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        raise ValueError("cannot normalise a null vector")
    return v / n


def any_perpendicular(d: np.ndarray) -> np.ndarray:
    """Return some unit vector perpendicular to ``d``."""
    ref = np.array([0.0, 0.0, 1.0])
    if abs(float(np.dot(unit(d), ref))) > 0.9:
        ref = np.array([1.0, 0.0, 0.0])
    return unit(np.cross(d, ref))


def water_at(metal: np.ndarray, direction: np.ndarray, r_mo: float,
             perp: np.ndarray | None = None) -> list[tuple[str, np.ndarray]]:
    """Place one water with its oxygen at ``metal + r_mo * direction``.

    The H-O-H bisector points *away* from the metal, so the oxygen lone-pair
    density points at the metal.  That is the correct starting orientation for a
    dative aquo ligand and saves the pre-optimiser from having to rotate six
    waters through 180 deg.
    """
    d = unit(direction)
    o = metal + r_mo * d
    p = any_perpendicular(d) if perp is None else unit(perp - float(np.dot(perp, d)) * d)
    half = math.radians(A_HOH / 2.0)
    h1 = o + R_OH * (math.cos(half) * d + math.sin(half) * p)
    h2 = o + R_OH * (math.cos(half) * d - math.sin(half) * p)
    return [("O", o), ("H", h1), ("H", h2)]


# ── Species record ────────────────────────────────────────────────────────────
@dataclass
class Species:
    name: str
    label: str            # chemical formula as written in the protocol
    charge: int
    mult: int
    atoms: list[tuple[str, np.ndarray]]
    note: str
    config: str = ""
    role: str = ""        # reactant / product / ligand / solvent
    protonation: str = "" # P0 / P1 / P2 / n-a
    metal: str = ""
    donor_indices: list[int] = field(default_factory=list)  # 0-based, into atoms

    @property
    def uhf(self) -> int:
        """Number of unpaired electrons, which is what xtb and ORCA both need."""
        return self.mult - 1

    def formula(self) -> str:
        counts: dict[str, int] = {}
        for sym, _ in self.atoms:
            counts[sym] = counts.get(sym, 0) + 1
        order = ["C", "H", "N", "O"]
        keys = [k for k in order if k in counts] + sorted(k for k in counts if k not in order)
        return "".join(f"{k}{counts[k]}" for k in keys)


def comment_line(sp: Species, extra: str = "") -> str:
    """The XYZ comment line.  Machine-readable key=value, so the ORCA input
    generator reads charge and multiplicity directly off the structure file and
    never has to infer them (attack A02)."""
    fields = [
        f"charge={sp.charge:+d}",
        f"mult={sp.mult}",
        f"uhf={sp.uhf}",
        f"uks={'true' if sp.mult > 1 else 'false'}",
        f"species={sp.name}",
        f"label={sp.label}",
        f"formula={sp.formula()}",
        f"role={sp.role}",
        f"protonation={sp.protonation or 'n-a'}",
        f"metal={sp.metal or 'none'}",
    ]
    if sp.config:
        fields.append(f"config={sp.config}")
    if extra:
        fields.append(extra)
    fields.append("builder=build_structures.py")
    return " | ".join(fields)


def write_xyz(path: Path, sp: Species, extra: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [str(len(sp.atoms)), comment_line(sp, extra)]
    for sym, xyz in sp.atoms:
        lines.append(f"{sym:<2s} {xyz[0]:14.8f} {xyz[1]:14.8f} {xyz[2]:14.8f}")
    path.write_text("\n".join(lines) + "\n")


def read_xyz_coords(path: Path) -> list[tuple[str, np.ndarray]]:
    lines = path.read_text().splitlines()
    n = int(lines[0].split()[0])
    out = []
    for line in lines[2:2 + n]:
        parts = line.split()
        out.append((parts[0], np.array([float(x) for x in parts[1:4]])))
    return out


# ── Ligand construction ───────────────────────────────────────────────────────
def build_methyl_gallate() -> tuple[list[tuple[str, np.ndarray]], dict[str, int]]:
    """Embed methyl gallate and return coordinates plus a map of the key oxygens.

    The map identifies the three phenolic oxygens by ring position:
      ``O4`` para to the ester-bearing carbon, ``O3`` and ``O5`` the two
      positions flanking it.  ``H3``/``H4``/``H5`` are their hydroxyl protons.
    """
    mol = Chem.AddHs(Chem.MolFromSmiles(METHYL_GALLATE_SMILES))
    params = AllChem.ETKDGv3()
    params.randomSeed = 0xC151          # deterministic: the build must be reproducible
    if AllChem.EmbedMolecule(mol, params) != 0:
        raise RuntimeError("ETKDG embedding of methyl gallate failed")
    AllChem.MMFFOptimizeMolecule(mol, maxIters=2000)

    # Locate the ester-bearing aromatic carbon: aromatic C bonded to the carbonyl C.
    ester_c = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != "C" or atom.GetIsAromatic():
            continue
        has_dbl_o = any(b.GetBondType() == Chem.BondType.DOUBLE and
                        b.GetOtherAtom(atom).GetSymbol() == "O" for b in atom.GetBonds())
        aro_nb = [nb for nb in atom.GetNeighbors() if nb.GetIsAromatic()]
        if has_dbl_o and aro_nb:
            ester_c = aro_nb[0].GetIdx()
            break
    if ester_c is None:
        raise RuntimeError("could not locate the ester-bearing ring carbon")

    ring = [a.GetIdx() for a in mol.GetAtoms() if a.GetIsAromatic()]
    # Walk the ring to get positions relative to the ester carbon.
    order = [ester_c]
    while len(order) < 6:
        last = order[-1]
        nxt = [nb.GetIdx() for nb in mol.GetAtomWithIdx(last).GetNeighbors()
               if nb.GetIdx() in ring and nb.GetIdx() not in order]
        order.append(nxt[0])
    # order = C1, C2, C3, C4, C5, C6 going one way round the ring
    c1, _c2, c3, c4, c5, _c6 = order

    def hydroxyl_on(cidx: int) -> tuple[int, int]:
        for nb in mol.GetAtomWithIdx(cidx).GetNeighbors():
            if nb.GetSymbol() == "O" and nb.GetTotalNumHs(includeNeighbors=True) == 1:
                h = [x.GetIdx() for x in nb.GetNeighbors() if x.GetSymbol() == "H"][0]
                return nb.GetIdx(), h
        raise RuntimeError(f"no hydroxyl on ring carbon {cidx}")

    o3, h3 = hydroxyl_on(c3)
    o4, h4 = hydroxyl_on(c4)
    o5, h5 = hydroxyl_on(c5)
    if not (mol.GetBondBetweenAtoms(c3, c4) and mol.GetBondBetweenAtoms(c4, c5)):
        raise RuntimeError("ring walk did not produce a 3,4,5-trihydroxy pattern")

    conf = mol.GetConformer()
    atoms = [(a.GetSymbol(), np.array(list(conf.GetAtomPosition(a.GetIdx()))))
             for a in mol.GetAtoms()]
    keymap = {"C1": c1, "C3": c3, "C4": c4, "C5": c5,
              "O3": o3, "O4": o4, "O5": o5, "H3": h3, "H4": h4, "H5": h5,
              "ring": ring}
    return atoms, keymap


def ligand_states() -> list[Species]:
    """LH2 / LH- / L2-, DFT_PROTOCOL.md §1.3.

    Deprotonation site.  The protocol fixes the *charge* of each state but not
    which hydroxyl loses its proton.  The site is chosen here on two grounds and
    the choice is recorded in MODEL_JUSTIFICATION.md:

      P1  the 4-OH, para to the ester.  It is the most acidic phenol of the
          galloyl triad (the ester is electron-withdrawing and para-conjugated to
          it) and it is one of the two oxygens of the chelating vicinal pair.
      P2  the 3-OH and 4-OH together, giving the 3,4-catecholate that is the
          classical catechol-type chelate named in §1.1.

    The 3,4 and 4,5 pairs are related by the local mirror plane of the galloyl
    group, so choosing 3,4 rather than 4,5 is a labelling choice, not a chemical
    one.
    """
    atoms, km = build_methyl_gallate()
    out = []

    out.append(Species(
        name="lig_P0_LH2", label="LH2 (methyl gallate, neutral)",
        charge=0, mult=1, atoms=list(atoms),
        note="Fully protonated galloyl model; dominant solution species at pH 5.",
        role="ligand", protonation="P0",
        donor_indices=[km["O3"], km["O4"]],
    ))

    # P1: remove the 4-OH proton
    drop1 = {km["H4"]}
    idx1 = [i for i in range(len(atoms)) if i not in drop1]
    remap1 = {old: new for new, old in enumerate(idx1)}
    out.append(Species(
        name="lig_P1_LH1m", label="LH- (mono-deprotonated at the 4-OH)",
        charge=-1, mult=1, atoms=[atoms[i] for i in idx1],
        note="Metal-induced single deprotonation; 4-OH is the most acidic phenol.",
        role="ligand", protonation="P1",
        donor_indices=[remap1[km["O3"]], remap1[km["O4"]]],
    ))

    # P2: remove the 3-OH and 4-OH protons -> 3,4-catecholate
    drop2 = {km["H3"], km["H4"]}
    idx2 = [i for i in range(len(atoms)) if i not in drop2]
    remap2 = {old: new for new, old in enumerate(idx2)}
    out.append(Species(
        name="lig_P2_L2m", label="L2- (3,4-bis-deprotonated catecholate)",
        charge=-2, mult=1, atoms=[atoms[i] for i in idx2],
        note="Classical catecholate chelation mode.",
        role="ligand", protonation="P2",
        donor_indices=[remap2[km["O3"]], remap2[km["O4"]]],
    ))
    return out


# ── Aquo ions ─────────────────────────────────────────────────────────────────
def octahedron_directions() -> list[np.ndarray]:
    return [np.array(v, dtype=float) for v in
            [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]


def square_antiprism_directions() -> list[np.ndarray]:
    """Ideal square-antiprism vertex directions (polar angle 59.26 deg)."""
    alpha = math.radians(59.26)
    dirs = []
    for k in range(4):
        phi = math.radians(90.0 * k)
        dirs.append(np.array([math.sin(alpha) * math.cos(phi),
                              math.sin(alpha) * math.sin(phi),
                              math.cos(alpha)]))
    for k in range(4):
        phi = math.radians(90.0 * k + 45.0)
        dirs.append(np.array([math.sin(math.pi - alpha) * math.cos(phi),
                              math.sin(math.pi - alpha) * math.sin(phi),
                              math.cos(math.pi - alpha)]))
    return dirs


def build_aquo(metal: str, n: int) -> Species:
    m = np.zeros(3)
    atoms: list[tuple[str, np.ndarray]] = [(metal, m)]
    donors: list[int] = []

    if n == 6:
        dirs = octahedron_directions()
        radii = [M_O_AQUO[metal]] * 6
        if metal == "Cu":
            # d9 Jahn-Teller: elongate the z axis.  A starting guess only, but an
            # undistorted octahedron is a saddle point for d9 and starting there
            # wastes optimiser steps.
            radii[4] = radii[5] = M_O_AQUO[metal] + CU_AXIAL_ELONGATION
        geom = "octahedral"
    elif n == 8:
        dirs = square_antiprism_directions()
        radii = [M_O_AQUO[metal] + 0.10] * 8   # 8-coordinate: slightly longer bonds
        geom = "square antiprismatic"
    else:
        raise ValueError(f"unsupported coordination number {n}")

    # Stagger the water planes so no two start eclipsed.
    for i, (d, r) in enumerate(zip(dirs, radii)):
        p = any_perpendicular(d)
        ang = math.radians(37.0 * i)
        dd = unit(d)
        q = unit(np.cos(ang) * p + np.sin(ang) * np.cross(dd, p))
        trio = water_at(m, d, r, perp=q)
        donors.append(len(atoms))
        atoms.extend(trio)

    return Species(
        name=f"{metal.lower()}_aquo{n}",
        label=f"[{metal}(H2O){n}]2+",
        charge=2, mult=METAL_MULT[metal], atoms=atoms,
        note=f"Ideal {geom} starting geometry; no distortion imposed.",
        config=METAL_CONFIG[metal], role="reactant", protonation="n-a", metal=metal,
        donor_indices=donors,
    )


def build_water() -> Species:
    d = np.array([0.0, 0.0, 1.0])
    trio = water_at(np.array([0.0, 0.0, -2.0]), d, 2.0)   # geometry only; monomer
    atoms = [(s, x - trio[0][1]) for s, x in trio]
    return Species(
        name="water", label="H2O", charge=0, mult=1, atoms=atoms,
        note="Free water monomer; the released species in the exchange reaction.",
        role="product", protonation="n-a",
    )


# ── Product complexes ─────────────────────────────────────────────────────────
def build_complex(metal: str, lig: Species, lig_atoms: list[tuple[str, np.ndarray]],
                  n_water: int = 4) -> Species:
    """Chelate ``metal`` across the vicinal O3/O4 pair and complete the octahedron
    with ``n_water`` aquo ligands.

    The metal is placed in the aromatic plane, outside the ring, on the bisector
    of the O3...O4 vector.  The remaining four coordination sites are the ideal
    octahedral positions left over once two cis vertices are taken by the chelate.
    """
    o3_i, o4_i = lig.donor_indices
    o3 = lig_atoms[o3_i][1]
    o4 = lig_atoms[o4_i][1]

    # Ring centroid, used only to decide which side of the O...O vector is "outward".
    ring_pos = [lig_atoms[i][1] for i, (s, _) in enumerate(lig_atoms) if s == "C"]
    ring_c = np.mean(np.array(ring_pos), axis=0)

    mid = 0.5 * (o3 + o4)
    outward = unit(mid - ring_c)
    half_oo = 0.5 * float(np.linalg.norm(o4 - o3))
    r_target = M_O_LIGAND[metal]
    if r_target <= half_oo:
        raise ValueError(f"{metal}-O target {r_target} A is shorter than half the O...O separation")
    height = math.sqrt(r_target ** 2 - half_oo ** 2)
    m_pos = mid + height * outward

    u = unit(o3 - m_pos)
    v = unit(o4 - m_pos)
    e1 = unit(u + v)                 # bisector, points at the chelate
    e3 = unit(np.cross(u, v))        # normal to the chelate plane
    e2 = unit(np.cross(e3, e1))

    inv_root2 = 1.0 / math.sqrt(2.0)
    # The four octahedral vertices not taken by the chelate.
    sites = [
        (-(e1 + e2) * inv_root2, "eq"),
        (-(e1 - e2) * inv_root2, "eq"),
        (e3, "ax"),
        (-e3, "ax"),
    ][:n_water]

    atoms = [(metal, m_pos)] + [(s, x.copy()) for s, x in lig_atoms]
    donors = [1 + o3_i, 1 + o4_i]
    for i, (d, kind) in enumerate(sites):
        r = M_O_AQUO[metal]
        if metal == "Cu" and kind == "ax":
            r += CU_AXIAL_ELONGATION
        p = any_perpendicular(d)
        ang = math.radians(41.0 * i)
        dd = unit(d)
        q = unit(math.cos(ang) * p + math.sin(ang) * np.cross(dd, p))
        trio = water_at(m_pos, d, r, perp=q)
        donors.append(len(atoms))
        atoms.extend(trio)

    charge = 2 + lig.charge
    lig_tag = {"P0": "LH2", "P1": "LH", "P2": "L"}[lig.protonation]
    charge_tag = "0" if charge == 0 else f"{charge}+"
    return Species(
        name=f"{metal.lower()}_{lig.protonation}_cplx",
        label=f"[{metal}({lig_tag})(H2O){n_water}]{charge_tag}",
        charge=charge, mult=METAL_MULT[metal], atoms=atoms,
        note=("Bidentate chelation across the vicinal 3,4-dioxygen pair; the four "
              "remaining octahedral sites carry water.  Ideal octahedral starting "
              "geometry, no hemidirected distortion imposed."),
        config=METAL_CONFIG[metal], role="product", protonation=lig.protonation,
        metal=metal, donor_indices=donors,
    )


# ── Driver ────────────────────────────────────────────────────────────────────
def main() -> None:
    INITIAL.mkdir(parents=True, exist_ok=True)
    built: list[Species] = []

    ligs = ligand_states()
    built.extend(ligs)
    built.append(build_water())
    built.append(build_aquo("Pb", 6))
    built.append(build_aquo("Pb", 8))
    built.append(build_aquo("Cu", 6))
    built.append(build_aquo("Zn", 6))

    for sp in built:
        write_xyz(INITIAL / f"{sp.name}.xyz", sp)

    # Complexes are built from the *pre-optimised* ligand where that already
    # exists, otherwise from the freshly embedded one.  Stage 2 of the driver
    # rebuilds them once the ligand xtb optimisations have finished.
    for metal, lig in itertools.product(("Pb", "Cu", "Zn"), ligs):
        opt = HERE / f"{lig.name}.xyz"
        lig_atoms = read_xyz_coords(opt) if opt.exists() else lig.atoms
        cplx = build_complex(metal, lig, lig_atoms)
        src = "xtb-preoptimised ligand" if opt.exists() else "ETKDG/MMFF ligand"
        write_xyz(INITIAL / f"{cplx.name}.xyz", cplx, extra=f"ligand_source={src}")
        built.append(cplx)

    for sp in built:
        print(f"{sp.name:<20s} {sp.formula():<12s} q={sp.charge:+d} mult={sp.mult} "
              f"uhf={sp.uhf}  n_atoms={len(sp.atoms)}")


if __name__ == "__main__":
    main()
