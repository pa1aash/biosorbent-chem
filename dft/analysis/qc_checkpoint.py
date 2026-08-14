#!/usr/bin/env python3
"""QC checkpoint for every harvested ORCA job.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

Implements the mandatory checks of DFT_PROTOCOL.md:

  §3.4  every frequency real -- no energy from a structure with an imaginary
        mode enters any sum
  §3.2  <S^2> reported for every Cu(II) species with its deviation from 0.750
  §3.7  DENTICITY MEASURED, NEVER ASSUMED -- both M-O(galloyl) distances
        reported INDIVIDUALLY for every metal x protonation-state combination.
        Never averaged: averaging is exactly what would hide a monodentate
        structure. This is attack A31.

The first-shell cutoffs and the connectivity logic are imported from
structures/geom_utils.py so that the pre-screen and production verdicts are
directly comparable, as §3.7 requires.

    python dft/analysis/qc_checkpoint.py            # all harvested jobs
    python dft/analysis/qc_checkpoint.py cu_P0_cplx # one job
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

DFT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DFT / "structures"))

from geom_utils import (  # noqa: E402
    COVALENT_RADII, BOND_TOLERANCE, M_O_CUTOFF, METALS,
    classify_oxygens, covalent_bonds, read_xyz,
)

OUTPUTS = DFT / "outputs"
HARTREE_KJ = 2625.499639


# ── Ligand-oxygen identification ─────────────────────────────────────────────

def phenolic_oxygens(syms: list[str], xyz: np.ndarray) -> list[int]:
    """Indices of the ring-bound (phenolic / phenolate) oxygens.

    These are the galloyl donors. Identified from connectivity rather than from
    atom order, so the result does not depend on how the builder happened to
    write the file:

      an oxygen is phenolic if it is bonded to exactly one carbon, and that
      carbon is itself bonded to two or more other carbons (i.e. a ring carbon).

    This deliberately excludes both ester oxygens: the carbonyl O is bonded to a
    carbon that has only one carbon neighbour, and the ether O is bonded to two
    carbons.
    """
    bonds = covalent_bonds(syms, xyz)
    nbr: dict[int, list[int]] = {i: [] for i in range(len(syms))}
    for i, j in bonds:
        nbr[i].append(j)
        nbr[j].append(i)

    out = []
    for o, s in enumerate(syms):
        if s != "O":
            continue
        c_nbrs = [n for n in nbr[o] if syms[n] == "C"]
        if len(c_nbrs) != 1:
            continue
        c = c_nbrs[0]
        if sum(1 for n in nbr[c] if syms[n] == "C") >= 2:
            out.append(o)
    return out


def analyse_geometry(path: Path) -> dict | None:
    """Denticity and first-shell composition from an optimised geometry."""
    syms, xyz, _ = read_xyz(path)
    metal = next((s for s in syms if s in METALS), None)
    if metal is None:
        return None

    m = syms.index(metal)
    cutoff = M_O_CUTOFF[metal]
    kinds = classify_oxygens(syms, xyz)

    def d(o: int) -> float:
        return float(np.linalg.norm(xyz[o] - xyz[m]))

    phen = sorted(phenolic_oxygens(syms, xyz), key=d)
    galloyl = [(o, d(o), kinds[o]) for o in phen]

    first_shell = sorted((d(o), o, kinds[o]) for o in kinds if d(o) < cutoff)
    n_water = sum(1 for _, _, k in first_shell if k == "OH2")
    n_lig = len(first_shell) - n_water

    bound = [g for g in galloyl if g[1] < cutoff]
    verdict = {2: "bidentate", 1: "MONODENTATE", 0: "DISSOCIATED"}.get(
        min(len(bound), 2), "bidentate")
    if len(bound) > 2:
        verdict = f"{len(bound)} galloyl O bound (unexpected)"

    return {
        "metal": metal, "cutoff": cutoff, "galloyl": galloyl,
        "n_first_shell": len(first_shell), "n_lig": n_lig, "n_water": n_water,
        "verdict": verdict,
        "shortest_water": min((x for x in first_shell if x[2] == "OH2"),
                              default=(float("nan"), -1, ""))[0],
    }


# ── Output parsing ───────────────────────────────────────────────────────────

def analyse_output(job: str) -> dict:
    d = OUTPUTS / job
    out = d / f"{job}.out"
    res: dict = {"job": job, "ok": out.exists()}
    if not out.exists():
        return res

    txt = out.read_text(errors="replace")
    res["terminated"] = "ORCA TERMINATED NORMALLY" in txt
    res["has_freq"] = "VIBRATIONAL FREQUENCIES" in txt
    res["has_hess"] = (d / f"{job}.hess").exists()
    res["opt_converged"] = "THE OPTIMIZATION HAS CONVERGED" in txt
    res["n_cycles"] = txt.count("GEOMETRY OPTIMIZATION CYCLE")

    # ── Frequencies: parsed natively from the output ────────────────────────
    # cclib 1.8.1 does not fully parse ORCA 6.1.1 output (it aborts in the SCF
    # convergence block), so the MANDATORY §3.4 all-real check must not depend
    # on it. Parse ORCA's own VIBRATIONAL FREQUENCIES table directly; cclib is
    # kept below only as a cross-check on the quantities it does return.
    if res["has_freq"]:
        block = txt.split("VIBRATIONAL FREQUENCIES", 1)[1].split("NORMAL MODES", 1)[0]
        freqs = [float(m.group(1)) for m in
                 re.finditer(r"^\s*\d+:\s+(-?\d+\.\d+)\s*cm\*\*-1", block, re.M)]
        if freqs:
            arr = np.asarray(freqs)
            # The first six modes of a non-linear molecule are translations and
            # rotations, printed as 0.00. Only a genuinely NEGATIVE value is an
            # imaginary mode.
            res["n_freq"] = int(arr.size)
            res["n_imag"] = int((arr < -1e-6).sum())
            res["lowest_freq"] = float(arr[arr > 1.0].min()) if (arr > 1.0).any() else float(arr.min())
            res["imag_values"] = [float(x) for x in arr[arr < -1e-6]]
        res["n_imag_banner"] = txt.count("***imaginary mode***")

    for key, pat in (("G_Eh", r"Final Gibbs free energy\s*\.*\s*(-?\d+\.\d+)"),
                     ("H_Eh", r"Total Enthalpy\s*\.*\s*(-?\d+\.\d+)")):
        m = re.search(pat, txt)
        if m:
            res[key] = float(m.group(1))

    # cclib for the electronic-structure quantities
    try:
        import cclib
        data = cclib.io.ccread(str(out))
    except Exception as exc:                       # noqa: BLE001
        data = None
        res["cclib_error"] = str(exc)

    if data is not None:
        if getattr(data, "scfenergies", None) is not None and len(data.scfenergies):
            # cclib >=1.8 returns eV
            res["E_scf_eV"] = float(data.scfenergies[-1])
        for attr, key in (("freeenergy", "G_Eh"), ("enthalpy", "H_Eh")):
            v = getattr(data, attr, None)
            if v is not None and key not in res:
                res[key] = float(v)
        vib = getattr(data, "vibfreqs", None)
        if vib is not None and len(vib) and "n_freq" not in res:
            v = np.asarray(vib, dtype=float)
            res["n_freq"] = int(v.size)
            res["n_imag"] = int((v < 0).sum())
            res["lowest_freq"] = float(v.min())
        if getattr(data, "atomcoords", None) is not None:
            res["n_atoms"] = int(data.atomcoords[-1].shape[0])

    # <S^2>: ORCA prints "<S**2>" for unrestricted references.
    s2 = [ln for ln in txt.splitlines() if "<S**2>" in ln]
    if s2:
        for ln in reversed(s2):
            for tok in ln.replace("=", " ").split():
                try:
                    res["S2"] = float(tok)
                    break
                except ValueError:
                    continue
            if "S2" in res:
                break

    # FINAL SINGLE POINT ENERGY, the value thermo.py consumes
    fsp = [ln for ln in txt.splitlines() if "FINAL SINGLE POINT ENERGY" in ln]
    if fsp:
        res["E_final_Eh"] = float(fsp[-1].split()[-1])

    geom = d / f"{job}.xyz"
    if geom.exists():
        try:
            res["geom"] = analyse_geometry(geom)
        except Exception as exc:                   # noqa: BLE001
            res["geom_error"] = str(exc)
    return res


def main() -> int:
    jobs = sys.argv[1:] or sorted(
        p.name for p in OUTPUTS.iterdir()
        if p.is_dir() and (p / f"{p.name}.out").exists())
    if not jobs:
        print("no harvested jobs in dft/outputs/")
        return 1

    print("=" * 78)
    print("QC CHECKPOINT — DFT_PROTOCOL.md §3.2, §3.4, §3.7")
    print("=" * 78)

    for job in jobs:
        r = analyse_output(job)
        print(f"\n### {job}")
        if not r.get("ok"):
            print("  no output file")
            continue

        complete = r.get("terminated") and r.get("has_freq") and r.get("has_hess")
        print(f"  status         : {'COMPLETE' if complete else '*** INCOMPLETE ***'}"
              f"  (terminated={r.get('terminated')} freq={r.get('has_freq')}"
              f" hess={r.get('has_hess')} opt_converged={r.get('opt_converged')}"
              f" cycles={r.get('n_cycles')})")

        if "E_final_Eh" in r:
            print(f"  FINAL SP energy: {r['E_final_Eh']:.8f} Eh"
                  f"   ({r['E_final_Eh'] * HARTREE_KJ:,.1f} kJ/mol)")
        if "G_Eh" in r:
            print(f"  Gibbs (ORCA)   : {r['G_Eh']:.8f} Eh"
                  "   [not used directly — thermo.py rebuilds G with quasi-RRHO]")

        if "n_freq" in r:
            flag = "" if r["n_imag"] == 0 else "   *** NOT A MINIMUM ***"
            print(f"  frequencies    : {r['n_freq']} modes, "
                  f"{r['n_imag']} imaginary, lowest real {r['lowest_freq']:.2f} cm^-1"
                  f"{flag}")
            if r.get("imag_values"):
                print(f"                   imaginary: "
                      f"{', '.join(f'{v:.2f}' for v in r['imag_values'])} cm^-1")
            print(f"  §3.4 all real  : {'YES' if r['n_imag'] == 0 else 'NO'}")
        else:
            print("  frequencies    : NONE — frequency calculation did not run")

        if "S2" in r:
            dev = r["S2"] - 0.750
            print(f"  §3.2 <S^2>     : {r['S2']:.4f}   ideal 0.750   "
                  f"deviation {dev:+.4f} ({abs(dev) / 0.750 * 100:.2f}%)")

        g = r.get("geom")
        if g:
            print(f"  §3.7 DENTICITY CHECKPOINT  (metal {g['metal']}, "
                  f"first-shell cutoff {g['cutoff']:.2f} Å)")
            for i, (o, dist, kind) in enumerate(g["galloyl"], 1):
                inside = "within" if dist < g["cutoff"] else "OUTSIDE"
                print(f"    galloyl O#{i} (atom {o:>2}, {kind:<7}) "
                      f"{g['metal']}–O = {dist:6.3f} Å   [{inside} first shell]")
            print(f"    VERDICT      : {g['verdict']}")
            print(f"    first shell  : {g['n_first_shell']} O "
                  f"({g['n_lig']} ligand + {g['n_water']} water)")
        elif "geom_error" in r:
            print(f"  geometry error : {r['geom_error']}")

    print("\n" + "=" * 78)
    print("Distances are reported INDIVIDUALLY and are never averaged — averaging")
    print("is what would hide a monodentate structure (§3.7, attack A31).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
