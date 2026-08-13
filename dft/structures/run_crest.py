#!/usr/bin/env python
"""CREST conformer screening, with the topology check done here rather than by CREST.

Why this exists.  ``dft/DFT_PROTOCOL.md`` §8 specifies a CREST conformer pre-pass
with the lowest conformer carried into the DFT optimisation.  Optimising an
arbitrary embedded conformer instead would make every downstream free energy an
accident of the starting geometry: methyl gallate has a rotatable methyl ester
and three rotatable hydroxyls, and the intramolecular hydrogen-bond pattern
between adjacent phenols differs between rotamers by more than the metal-to-metal
differences the report is trying to resolve.

Method.  iMTD-GC at GFN2-xTB with the ALPB water model, matching the
pre-optimisation.  Charge and unpaired-electron count are read from the XYZ
provenance header, so an open-shell species cannot be screened as a closed shell
by accident.

Why ``--noreftopo`` is used, and what replaces it.  CREST 3.0.2 aborts on every
species in this set with "Change in topology detected", flagging *all* atoms,
including the free ligand whose input geometry was already tight-optimised at the
identical level of theory.  Direct comparison of the input and the CREST
initial-optimisation geometry shows the covalent connectivity is unchanged
(21 bonds in, 21 bonds out, no difference) and the largest atomic displacement is
a hydroxyl proton rotation.  The check is a false positive, and it is fatal, so
it is disabled.

Disabling a safety check is only defensible if something replaces it, so every
member of every returned ensemble is verified here instead:

  * the covalent connectivity of the non-metal framework must match the reference
    structure exactly (this catches proton migration and bond formation);
  * for metal complexes, the first-shell donor count and its split into ligand
    and water oxygens must match the reference (this catches water loss and
    chelate opening, which CREST's own connectivity model handles badly anyway).

Conformers failing either test are rejected and counted, not silently dropped.

Run with the ``biosorb`` environment active.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from geom_utils import (METALS, coordination_signature, covalent_bonds,  # noqa: E402
                        parse_header, read_multi_xyz, read_xyz)

HERE = Path(__file__).resolve().parent
CREST_DIR = HERE / "crest"
HARTREE_TO_KCAL = 627.5094740631   # unit conversion
ENERGY_WINDOW_KCAL = 3.0           # the cutoff fixed for this screen


def run_one(name: str, threads: int, timeout: int) -> dict:
    src = HERE / f"{name}.xyz"
    if not src.exists():
        return {"species": name, "status": "missing input"}

    ref_syms, ref_xyz, header = read_xyz(src)
    metal = header.get("metal", "none")
    ref_bonds = covalent_bonds(ref_syms, ref_xyz)
    ref_coord = coordination_signature(ref_syms, ref_xyz, metal) if metal in METALS else None

    wd = CREST_DIR / name
    if wd.exists():
        shutil.rmtree(wd)
    wd.mkdir(parents=True)
    shutil.copy(src, wd / "in.xyz")

    cmd = ["crest", "in.xyz", "--gfn2", "--alpb", "water",
           "--chrg", header["charge"].lstrip("+"), "--uhf", header["uhf"],
           "--noreftopo", "-T", str(threads)]
    t0 = time.time()
    log, status = "", "ok"
    try:
        proc = subprocess.run(cmd, cwd=wd, capture_output=True, text=True, timeout=timeout)
        log = proc.stdout + proc.stderr
        if proc.returncode != 0:
            status = f"crest exit {proc.returncode}"
    except subprocess.TimeoutExpired as exc:
        log = (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        status = f"timeout after {timeout} s"
    elapsed = time.time() - t0
    (wd / "crest.xtblog").write_text(log)
    (wd / "crest_command.txt").write_text(" ".join(cmd) + "\n")

    ensemble = read_multi_xyz(wd / "crest_conformers.xyz")
    rotamers = read_multi_xyz(wd / "crest_rotamers.xyz")

    kept, rejected = [], []
    for k, (energy, syms, xyz) in enumerate(ensemble):
        reasons = []
        if syms != ref_syms:
            reasons.append("atom ordering or composition changed")
        elif covalent_bonds(syms, xyz) != ref_bonds:
            reasons.append("covalent connectivity changed")
        if ref_coord is not None and not reasons:
            sig = coordination_signature(syms, xyz, metal)
            if sig != ref_coord:
                reasons.append(f"first shell {sig} != reference {ref_coord}")
        (kept if not reasons else rejected).append(
            {"index": k, "E_Eh": energy, "reasons": reasons})

    result = {
        "species": name,
        "label": header.get("label", ""),
        "charge": header.get("charge", ""),
        "multiplicity": header.get("mult", ""),
        "metal": metal,
        "status": status,
        "wall_seconds": round(elapsed, 1),
        "method": "iMTD-GC / GFN2-xTB / ALPB(water) / --noreftopo",
        "n_rotamers_returned": len(rotamers),
        "n_conformers_returned": len(ensemble),
        "n_conformers_rejected_by_topology_check": len(rejected),
        "n_conformers_valid": len(kept),
        "energy_window_kcal": ENERGY_WINDOW_KCAL,
    }
    if rejected:
        result["rejection_reasons"] = rejected[:10]

    if kept:
        e0 = min(c["E_Eh"] for c in kept)
        for c in kept:
            c["rel_kcal"] = round((c["E_Eh"] - e0) * HARTREE_TO_KCAL, 3)
        kept.sort(key=lambda c: c["rel_kcal"])
        within = [c for c in kept if c["rel_kcal"] <= ENERGY_WINDOW_KCAL]
        result["E_lowest_Eh"] = f"{e0:.8f}"
        result["n_within_window"] = len(within)
        result["rel_energies_kcal"] = [c["rel_kcal"] for c in within]
        result["carried_forward"] = f"{name}.xyz (lowest valid conformer)"

        # Write the lowest valid conformer back as the DFT starting geometry,
        # preserving the provenance header.
        _, syms, xyz = ensemble[kept[0]["index"]]
        fields = [f"{k}={v}" for k, v in header.items()
                  if k not in ("builder", "E_xtb_Eh", "preopt")]
        fields += [
            "preopt=GFN2-xTB/ALPB(water)/opt-tight",
            "conformer_search=CREST iMTD-GC/GFN2-xTB/ALPB(water)",
            f"conformers_valid={len(kept)}",
            f"conformers_within_{ENERGY_WINDOW_KCAL:g}kcal={len(within)}",
            f"E_xtb_Eh={kept[0]['E_Eh']:.8f}",
            "preopt_is_not_a_report_quantity=true",
            "builder=build_structures.py+run_xtb_preopt.py+run_crest.py",
        ]
        lines = [str(len(syms)), " | ".join(fields)]
        lines += [f"{s:<2s} {c[0]:14.8f} {c[1]:14.8f} {c[2]:14.8f}"
                  for s, c in zip(syms, xyz)]
        (HERE / f"{name}.xyz").write_text("\n".join(lines) + "\n")

        # Keep the surviving window as an auditable ensemble.
        out = []
        for c in within:
            _, s2, x2 = ensemble[c["index"]]
            out.append(str(len(s2)))
            out.append(f"E_Eh={c['E_Eh']:.8f} rel_kcal={c['rel_kcal']:.3f}")
            out += [f"{s:<2s} {v[0]:14.8f} {v[1]:14.8f} {v[2]:14.8f}"
                    for s, v in zip(s2, x2)]
        (wd / "valid_within_window.xyz").write_text("\n".join(out) + "\n")

    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("species", nargs="+")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=7200)
    ap.add_argument("--tag", default="crest")
    args = ap.parse_args()

    CREST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CREST_DIR / f"{args.tag}_results.json"
    results = json.loads(out_path.read_text()) if out_path.exists() else []
    results = [r for r in results if r["species"] not in set(args.species)]

    for name in args.species:
        print(f"[crest] {name} ...", flush=True)
        r = run_one(name, args.threads, args.timeout)
        results.append(r)
        print(f"        {r['status']}  returned={r.get('n_conformers_returned', 0)} "
              f"valid={r.get('n_conformers_valid', 0)} "
              f"within_{ENERGY_WINDOW_KCAL:g}kcal={r.get('n_within_window', 0)} "
              f"({r.get('wall_seconds', 0)} s)", flush=True)
        out_path.write_text(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
