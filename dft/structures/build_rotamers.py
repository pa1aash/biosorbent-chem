#!/usr/bin/env python
"""Conformer generation without CREST.

Why this exists.  ``dft/DFT_PROTOCOL.md`` §8 calls for a CREST conformer pre-pass.
CREST 3.0.2 as installed in the ``biosorb`` environment cannot run on this
machine: its metadynamics driver aborts with a LAPACK factorisation failure
(``Factorisation of matrix failed lapack_sytrf``) for every species tried, at
GFN2 and at GFN-FF, in gas phase and in ALPB water, on one thread and on eight.
The plain xtb binary from the same environment optimises all seventeen structures
without complaint, so the failure is confined to the CREST driver.  The evidence
is recorded in ``crest/ligands_results.json`` and the CREST logs.

A conformer search is not optional here.  Methyl gallate carries a rotatable
methyl ester and three rotatable phenolic hydroxyls whose intramolecular
hydrogen-bond network differs between rotamers by more than the metal-to-metal
free-energy differences the report is trying to resolve, so starting the DFT
optimisation from an arbitrary embedded conformer would make every downstream
number an accident of that choice.  This module therefore replaces the CREST
pre-pass with an explicit search:

**Free ligands** -- distance-geometry sampling.  ``ETKDGv3`` generates a large
random-but-chemically-sensible conformer set, MMFF94 relaxes it, and every
surviving structure is re-optimised at GFN2-xTB/ALPB(water), the same level as
the rest of the preparation stage.  This samples the same degrees of freedom
CREST would have sampled; it explores them by random embedding rather than by
metadynamics, which is slower to find rare conformers but entirely adequate for
a molecule with four rotatable torsions.

**Metal complexes** -- systematic torsion enumeration.  Chelation locks the two
donor oxygens onto the metal, so the residual conformational freedom is small
and enumerable: the methyl ester torsion and the orientation of each phenolic
hydroxyl not bound to the metal.  Every combination is built, optimised and
deduplicated.  Enumeration is preferable to random embedding here because the
space is small enough to cover exhaustively, and because random embedding would
destroy the coordination geometry.

Both routes end in the same place: a deduplicated ensemble, an energy window, and
a single lowest structure carried forward.  No energy produced here is a report
quantity.

Run with the ``biosorb`` environment active.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_structures import (METHYL_GALLATE_SMILES, build_complex,  # noqa: E402
                              ligand_states, write_xyz)
from geom_utils import (METALS, coordination_signature, covalent_bonds,  # noqa: E402
                        parse_header, read_xyz)

HERE = Path(__file__).resolve().parent
ROT = HERE / "rotamers"

HARTREE_TO_KJ = 2625.499639
HARTREE_TO_KCAL = 627.5094740631
WINDOW_KCAL = 3.0                 # the retention window fixed for this screen
RMSD_DEDUP = 0.25                 # A, heavy atoms
ENERGY_DEDUP_KJ = 0.10            # kJ/mol


# ── xtb driver ────────────────────────────────────────────────────────────────
def xtb_opt(syms: list[str], xyz: np.ndarray, charge: int, uhf: int
            ) -> tuple[float, np.ndarray] | None:
    """Optimise one geometry; returns (energy_Eh, coords) or None if it failed."""
    with tempfile.TemporaryDirectory() as td:
        wd = Path(td)
        lines = [str(len(syms)), "rotamer"]
        lines += [f"{s:<2s} {c[0]:14.8f} {c[1]:14.8f} {c[2]:14.8f}"
                  for s, c in zip(syms, xyz)]
        (wd / "in.xyz").write_text("\n".join(lines) + "\n")
        try:
            proc = subprocess.run(
                ["xtb", "in.xyz", "--gfn", "2", "--opt", "tight",
                 "--chrg", str(charge), "--uhf", str(uhf), "--alpb", "water"],
                cwd=wd, capture_output=True, text=True, timeout=1800)
        except subprocess.TimeoutExpired:
            return None
        if "GEOMETRY OPTIMIZATION CONVERGED" not in proc.stdout:
            return None
        energy = None
        for line in proc.stdout.splitlines():
            if "TOTAL ENERGY" in line:
                energy = float(line.split()[3])
        out = (wd / "xtbopt.xyz").read_text().splitlines()
        n = int(out[0].split()[0])
        coords = np.array([[float(v) for v in l.split()[1:4]] for l in out[2:2 + n]])
        return (energy, coords) if energy is not None else None


# ── deduplication ─────────────────────────────────────────────────────────────
def heavy_rmsd(syms: list[str], a: np.ndarray, b: np.ndarray) -> float:
    keep = [i for i, s in enumerate(syms) if s != "H"]
    p, q = a[keep].copy(), b[keep].copy()
    p -= p.mean(0)
    q -= q.mean(0)
    u, _, vt = np.linalg.svd(p.T @ q)
    d = np.sign(np.linalg.det(u @ vt))
    rot = u @ np.diag([1.0, 1.0, d]) @ vt
    return float(np.sqrt((((rot.T @ p.T).T - q) ** 2).sum(1).mean()))


def dedup(cands: list[dict], syms: list[str]) -> list[dict]:
    cands = sorted(cands, key=lambda c: c["E_Eh"])
    kept: list[dict] = []
    for c in cands:
        dup = False
        for k in kept:
            de = abs(c["E_Eh"] - k["E_Eh"]) * HARTREE_TO_KJ
            if de < ENERGY_DEDUP_KJ and heavy_rmsd(syms, c["xyz"], k["xyz"]) < RMSD_DEDUP:
                dup = True
                break
        if not dup:
            kept.append(c)
    return kept


# ── torsion machinery for the complexes ───────────────────────────────────────
def side_atoms(bonds: set[tuple[int, int]], n: int, anchor: int, moving: int) -> list[int]:
    """Atoms reachable from ``moving`` without passing back through ``anchor``."""
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for i, j in bonds:
        adj[i].append(j)
        adj[j].append(i)
    seen = {anchor, moving}
    order = deque([moving])
    out = [moving]
    while order:
        cur = order.popleft()
        for nb in adj[cur]:
            if nb not in seen:
                seen.add(nb)
                out.append(nb)
                order.append(nb)
    return out


def rotate_about(xyz: np.ndarray, a: int, b: int, movers: list[int], deg: float) -> np.ndarray:
    axis = xyz[b] - xyz[a]
    axis = axis / np.linalg.norm(axis)
    th = np.deg2rad(deg)
    k = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    rot = np.eye(3) + np.sin(th) * k + (1 - np.cos(th)) * (k @ k)
    out = xyz.copy()
    for m in movers:
        if m == b:
            continue
        out[m] = xyz[b] + rot @ (xyz[m] - xyz[b])
    return out


def torsion_sites(syms: list[str], xyz: np.ndarray, metal: str
                  ) -> list[tuple[int, int, list[int], list[float]]]:
    """Rotatable torsions of a chelated complex: the ester and each free hydroxyl."""
    bonds = covalent_bonds(syms, xyz)
    n = len(syms)
    donors = {o for _, o, _ in
              (metal_first_shell(syms, xyz, metal) if metal in METALS else [])}
    adj: dict[int, set[int]] = {i: set() for i in range(n)}
    for i, j in bonds:
        adj[i].add(j)
        adj[j].add(i)

    sites = []
    # Free phenolic hydroxyls: rotate H about its C-O bond.
    for o, s in enumerate(syms):
        if s != "O" or o in donors:
            continue
        hs = [h for h in adj[o] if syms[h] == "H"]
        cs = [c for c in adj[o] if syms[c] == "C"]
        if len(hs) == 1 and len(cs) == 1:
            sites.append((cs[0], o, [o, hs[0]], [0.0, 180.0]))
    # Methyl ester: rotate the whole ester about the ring-carbon/carbonyl-carbon bond.
    for c, s in enumerate(syms):
        if s != "C":
            continue
        dbl_o = [o for o in adj[c] if syms[o] == "O" and len(adj[o]) == 1]
        est_o = [o for o in adj[c] if syms[o] == "O" and len(adj[o]) == 2]
        ring_c = [r for r in adj[c] if syms[r] == "C" and len(adj[r]) == 3]
        if dbl_o and est_o and ring_c:
            movers = side_atoms(bonds, n, ring_c[0], c)
            sites.append((ring_c[0], c, movers, [0.0, 180.0]))
            break
    return sites


def metal_first_shell(syms, xyz, metal):
    from geom_utils import metal_donors
    return metal_donors(syms, xyz, metal)


def water_rotation_seeds(syms: list[str], xyz: np.ndarray, metal: str,
                         n: int, seed: int = 0xC151) -> list[np.ndarray]:
    """Randomly reorient every coordinated water about its own metal-oxygen axis.

    A coordinated water can rotate about the M-O axis at little cost, and the
    resulting hydrogen-bond network between neighbouring waters is what
    distinguishes one aquo-ion conformer from another.  That freedom is invisible
    to torsion enumeration over covalent bonds -- an aquo ion has no rotatable
    covalent torsion at all -- yet the aquo ion is a reactant in every exchange
    reaction, so its conformer energy shifts every reported free energy directly.

    The space is sampled rather than enumerated: with six independent rotors a
    two-point grid is already 64 combinations, and the minima are not at
    predictable angles the way a phenolic hydroxyl's are.  The generator is
    seeded, so the sample is reproducible.
    """
    if metal not in METALS:
        return []
    rng = np.random.default_rng(seed)
    m = syms.index(metal)
    bonds = covalent_bonds(syms, xyz)
    adj: dict[int, set[int]] = {i: set() for i in range(len(syms))}
    for i, j in bonds:
        adj[i].add(j)
        adj[j].add(i)

    waters = [(o, sorted(adj[o])) for _, o, kind in metal_first_shell(syms, xyz, metal)
              if kind == "OH2"]
    if not waters:
        return []

    out = []
    for _ in range(n):
        cur = xyz.copy()
        for o, hs in waters:
            angle = float(rng.uniform(0.0, 360.0))
            cur = rotate_about(cur, m, o, [o, *hs], angle)
        out.append(cur)
    return out


# ── the two search routes ─────────────────────────────────────────────────────
def etkdg_seeds(name: str, header: dict, ref_syms: list[str], n_embed: int
                ) -> list[np.ndarray]:
    """Supplementary distance-geometry starting geometries for a free ligand.

    Pruning is disabled deliberately.  RDKit prunes on heavy-atom RMSD, and the
    hydroxyl rotations that dominate this molecule's conformational energetics
    move no heavy atom at all, so the default pruning collapses the entire set to
    a single conformer.  Redundancy is removed after optimisation instead, on
    energy *and* geometry together.
    """
    proto = header["protonation"]
    mol = Chem.AddHs(Chem.MolFromSmiles(METHYL_GALLATE_SMILES))
    params = AllChem.ETKDGv3()
    params.randomSeed = 0xC151
    params.pruneRmsThresh = -1.0
    AllChem.EmbedMultipleConfs(mol, numConfs=n_embed, params=params)
    AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=2000)

    from build_structures import build_methyl_gallate
    _, km = build_methyl_gallate()
    drop = {"P0": set(), "P1": {km["H4"]}, "P2": {km["H3"], km["H4"]}}[proto]
    keep_idx = [i for i in range(mol.GetNumAtoms()) if i not in drop]
    syms = [mol.GetAtomWithIdx(i).GetSymbol() for i in keep_idx]
    if syms != ref_syms:
        raise RuntimeError(f"{name}: ETKDG atom ordering diverged from the reference")
    return [np.array(c.GetPositions())[keep_idx] for c in mol.GetConformers()]


def search(name: str, n_embed: int, n_water_samples: int) -> dict:
    """Enumerate, optimise, verify, deduplicate.

    The primary route is the same for both ligands and complexes: every
    rotatable torsion the structure actually has is enumerated over its minima
    and each combination is optimised.  For methyl gallate those torsions are the
    three phenolic hydroxyls and the methyl ester, which is the whole of its
    conformational space; for a chelated complex the donor oxygens are locked to
    the metal and only the free hydroxyls and the ester remain.  Free ligands are
    additionally seeded with distance-geometry embeddings as a check that the
    torsion grid has not missed a basin.
    """
    src = HERE / f"{name}.xyz"
    ref_syms, ref_xyz, header = read_xyz(src)
    charge, uhf = int(header["charge"]), int(header["uhf"])
    metal = header.get("metal", "none")
    is_complex = metal in METALS

    ref_bonds = covalent_bonds(ref_syms, ref_xyz)
    ref_coord = coordination_signature(ref_syms, ref_xyz, metal) if is_complex else None

    sites = torsion_sites(ref_syms, ref_xyz, metal)
    combos = list(itertools.product(*[s[3] for s in sites])) if sites else [()]
    starts = []
    for combo in combos:
        xyz = ref_xyz.copy()
        for (a, b, movers, _), ang in zip(sites, combo):
            if ang:
                xyz = rotate_about(xyz, a, b, movers, ang)
        starts.append(xyz)
    n_torsion_starts = len(starts)

    # Distance-geometry seeding applies to the free galloyl ligand only; the water
    # monomer is rigid and the metal complexes would be destroyed by re-embedding.
    n_seeds = 0
    if header.get("role") == "ligand" and n_embed > 0:
        seeds = etkdg_seeds(name, header, ref_syms, n_embed)
        n_seeds = len(seeds)
        starts.extend(seeds)

    water_seeds = water_rotation_seeds(ref_syms, ref_xyz, metal, n_water_samples)
    starts.extend(water_seeds)

    cands, failed, rejected = [], 0, 0
    for xyz in starts:
        res = xtb_opt(ref_syms, xyz, charge, uhf)
        if res is None:
            failed += 1
            continue
        e, coords = res
        if covalent_bonds(ref_syms, coords) != ref_bonds:
            rejected += 1
            continue
        if is_complex and coordination_signature(ref_syms, coords, metal) != ref_coord:
            rejected += 1
            continue
        cands.append({"E_Eh": e, "xyz": coords})

    method = (f"systematic torsion enumeration ({len(sites)} torsions, "
              f"{n_torsion_starts} start geometries)")
    if n_seeds:
        method += f" + RDKit ETKDGv3 ({n_seeds} unpruned embeddings) + MMFF94"
    if water_seeds:
        method += f" + {len(water_seeds)} seeded random water reorientations"
    method += " + GFN2-xTB/ALPB(water) opt-tight"

    return finish(name, header, ref_syms, cands, failed, rejected, method,
                  extra={"n_torsions": len(sites),
                         "n_torsion_start_geometries": n_torsion_starts,
                         "n_etkdg_seeds": n_seeds,
                         "n_water_orientation_samples": len(water_seeds),
                         "n_start_geometries_total": len(starts)})


def finish(name, header, syms, cands, failed, rejected, method, extra) -> dict:
    result = {
        "species": name,
        "label": header.get("label", ""),
        "charge": header.get("charge", ""),
        "multiplicity": header.get("mult", ""),
        "metal": header.get("metal", "none"),
        "method": method,
        "energy_window_kcal": WINDOW_KCAL,
        "n_optimisations_failed": failed,
        "n_rejected_topology_or_coordination": rejected,
        **extra,
    }
    if not cands:
        result["status"] = "no valid conformer"
        return result

    unique = dedup(cands, syms)
    e0 = unique[0]["E_Eh"]
    for c in unique:
        c["rel_kcal"] = (c["E_Eh"] - e0) * HARTREE_TO_KCAL
    within = [c for c in unique if c["rel_kcal"] <= WINDOW_KCAL]

    result.update({
        "status": "ok",
        "n_optimisations_converged": len(cands),
        "n_unique_conformers": len(unique),
        "n_within_window": len(within),
        "E_lowest_Eh": f"{e0:.8f}",
        "rel_energies_kcal": [round(c["rel_kcal"], 3) for c in within],
        "rel_energies_kJ": [round(c["rel_kcal"] * 4.184, 2) for c in within],
    })

    ROT.mkdir(parents=True, exist_ok=True)
    out = []
    for c in within:
        out.append(str(len(syms)))
        out.append(f"E_Eh={c['E_Eh']:.8f} rel_kcal={c['rel_kcal']:.3f} "
                   f"rel_kJ_per_mol={c['rel_kcal'] * 4.184:.2f}")
        out += [f"{s:<2s} {v[0]:14.8f} {v[1]:14.8f} {v[2]:14.8f}"
                for s, v in zip(syms, c["xyz"])]
    (ROT / f"{name}_ensemble.xyz").write_text("\n".join(out) + "\n")

    # Carry the lowest conformer forward as the DFT starting geometry.
    # Drop every field this stage is about to rewrite, so a rerun replaces its
    # own provenance rather than appending a second copy of it.
    stale = {"builder", "E_xtb_Eh", "preopt", "preopt_is_not_a_report_quantity"}
    fields = [f"{k}={v}" for k, v in header.items()
              if k not in stale and not k.startswith("conformer")]
    fields += [
        "preopt=GFN2-xTB/ALPB(water)/opt-tight",
        f"conformer_search={method}",
        f"conformers_unique={len(unique)}",
        f"conformers_within_{WINDOW_KCAL:g}kcal={len(within)}",
        f"E_xtb_Eh={e0:.8f}",
        "preopt_is_not_a_report_quantity=true",
        "builder=build_structures.py+run_xtb_preopt.py+build_rotamers.py",
    ]
    lines = [str(len(syms)), " | ".join(fields)]
    lines += [f"{s:<2s} {v[0]:14.8f} {v[1]:14.8f} {v[2]:14.8f}"
              for s, v in zip(syms, within[0]["xyz"])]
    (HERE / f"{name}.xyz").write_text("\n".join(lines) + "\n")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("species", nargs="+")
    ap.add_argument("--embeddings", type=int, default=60)
    ap.add_argument("--water-samples", type=int, default=16)
    ap.add_argument("--tag", default="rotamers")
    args = ap.parse_args()

    ROT.mkdir(parents=True, exist_ok=True)
    out_path = ROT / f"{args.tag}_results.json"
    results = json.loads(out_path.read_text()) if out_path.exists() else []
    results = [r for r in results if r["species"] not in set(args.species)]

    for name in args.species:
        print(f"[conf] {name} ...", flush=True)
        r = search(name, args.embeddings, args.water_samples)
        results.append(r)
        print(f"       {r.get('status')}  unique={r.get('n_unique_conformers', 0)} "
              f"within_{WINDOW_KCAL:g}kcal={r.get('n_within_window', 0)} "
              f"rejected={r.get('n_rejected_topology_or_coordination', 0)}", flush=True)
        out_path.write_text(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
