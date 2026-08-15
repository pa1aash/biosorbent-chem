#!/usr/bin/env python3
"""PHASE 6 -- hemidirection descriptors on every optimised metal centre.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

DFT_PROTOCOL.md §5, attack A14: "Is hemidirection asserted or measured?"  This
script measures it, on all nine complexes and all four aquo ions, using
analysis/src/hemidirection.py -- the module unit-tested against a hand-worked
geometry.

Two descriptors, both reported, because one number cannot capture both
distortions:

  d~        normalised centroid displacement, |r_M - centroid| / <M-O>.
            Responds to radial asymmetry. Normalised so that Pb does not score
            higher merely for having longer bonds, which would be an artefact.
  theta_void  angular clearance of the donor-free hemisphere, after
            Shimoni-Livny, Glusker & Bock. Purely angular.

THE DONOR SET IS THE MEASURED FIRST SHELL, using the same element-specific
cutoffs as the Phase 3 denticity checkpoint (Pb 3.20 A, Cu 2.80 A, Zn 2.80 A),
so that the two analyses describe the same coordination sphere.  Because a
cutoff that excluded a genuine Pb donor would MANUFACTURE the asymmetry this
module exists to measure, the sensitivity to the cutoff is reported too.

    python dft/analysis/run_hemidirection.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
DFT = ROOT / "dft"
sys.path.insert(0, str(ROOT / "analysis" / "src"))
sys.path.insert(0, str(DFT / "structures"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hemidirection import HEMIDIRECTED_THRESHOLD, analyse  # noqa: E402
from geom_utils import M_O_CUTOFF, METALS, classify_oxygens, read_xyz  # noqa: E402
from orca_parse import OUTPUTS  # noqa: E402

AQUO = ["pb_aquo6", "pb_aquo8", "cu_aquo6", "zn_aquo6"]
COMPLEXES = ["pb_P0_cplx", "pb_P1_cplx", "pb_P2_cplx",
             "cu_P0_cplx", "cu_P1_cplx", "cu_P2_cplx",
             "zn_P0_cplx", "zn_P1_cplx", "zn_P2_cplx"]


def donors(name: str, cutoff: float | None = None):
    syms, xyz, _ = read_xyz(OUTPUTS / name / f"{name}.xyz")
    metal = next(s for s in syms if s in METALS)
    m = syms.index(metal)
    cut = M_O_CUTOFF[metal] if cutoff is None else cutoff
    ox = [o for o in classify_oxygens(syms, xyz)
          if float(np.linalg.norm(xyz[o] - xyz[m])) < cut]
    return metal, xyz[m], xyz[ox], cut


def row(name: str, cutoff: float | None = None):
    metal, mpos, dpos, cut = donors(name, cutoff)
    r = analyse(mpos, dpos)
    return metal, cut, r


def main() -> int:
    print("=" * 116)
    print("PHASE 6 — HEMIDIRECTION, MEASURED (DFT_PROTOCOL.md §5, attack A14)")
    print("analysis/src/hemidirection.py · donor set = measured first shell")
    print("=" * 116)

    print("\n### 6a. THE FOUR AQUO IONS")
    print("-" * 116)
    hdr = (f"{'species':<12} {'metal':>5} {'cutoff':>7} {'n donors':>9} "
           f"{'<M-O> / Å':>10} {'d / Å':>8} {'d~':>8} {'asym':>8} "
           f"{'θ_void / °':>11}  {'verdict'}")
    print(hdr)
    print("-" * 116)
    res = {}
    for n in AQUO:
        metal, cut, r = row(n)
        res[n] = r
        void = f"{r.void_angle:.2f}" if r.void_angle is not None else "n/a"
        print(f"{n:<12} {metal:>5} {cut:>7.2f} {r.n_donors:>9} "
              f"{r.mean_bond_length:>10.4f} {r.displacement:>8.4f} "
              f"{r.normalised_displacement:>8.4f} {r.asymmetry:>8.4f} "
              f"{void:>11}  {r.verdict}")

    print("\n\n### 6b. THE NINE COMPLEXES")
    print("-" * 116)
    print(hdr)
    print("-" * 116)
    for n in COMPLEXES:
        metal, cut, r = row(n)
        res[n] = r
        void = f"{r.void_angle:.2f}" if r.void_angle is not None else "n/a"
        print(f"{n:<12} {metal:>5} {cut:>7.2f} {r.n_donors:>9} "
              f"{r.mean_bond_length:>10.4f} {r.displacement:>8.4f} "
              f"{r.normalised_displacement:>8.4f} {r.asymmetry:>8.4f} "
              f"{void:>11}  {r.verdict}")
    print("-" * 116)
    print(f"  Verdict threshold: d~ >= {HEMIDIRECTED_THRESHOLD} is called hemidirected; "
          f"the measurement, not the verdict, is the result.")

    # ── 6c. is Pb measurably hemidirected relative to Cu and Zn? ─────────────
    print("\n\n### 6c. IS Pb MEASURABLY HEMIDIRECTED RELATIVE TO Cu AND Zn?")
    print("=" * 116)
    print(f"{'state':<8} {'Pb d~':>9} {'Cu d~':>9} {'Zn d~':>9}   "
          f"{'Pb-Cu':>8} {'Pb-Zn':>8}   {'Pb θ_void':>10} {'Cu θ_void':>10} "
          f"{'Zn θ_void':>10}")
    print("-" * 116)
    for st in ("P0", "P1", "P2"):
        p, c, z = (res[f"{m}_{st}_cplx"] for m in ("pb", "cu", "zn"))
        va = lambda r: f"{r.void_angle:.2f}" if r.void_angle is not None else "n/a"  # noqa: E731
        print(f"{st:<8} {p.normalised_displacement:9.4f} "
              f"{c.normalised_displacement:9.4f} {z.normalised_displacement:9.4f}   "
              f"{p.normalised_displacement - c.normalised_displacement:+8.4f} "
              f"{p.normalised_displacement - z.normalised_displacement:+8.4f}   "
              f"{va(p):>10} {va(c):>10} {va(z):>10}")
    print("-" * 116)
    ap, ac, az = res["pb_aquo6"], res["cu_aquo6"], res["zn_aquo6"]
    va = lambda r: f"{r.void_angle:.2f}" if r.void_angle is not None else "n/a"  # noqa: E731
    print(f"{'aquo6':<8} {ap.normalised_displacement:9.4f} "
          f"{ac.normalised_displacement:9.4f} {az.normalised_displacement:9.4f}   "
          f"{ap.normalised_displacement - ac.normalised_displacement:+8.4f} "
          f"{ap.normalised_displacement - az.normalised_displacement:+8.4f}   "
          f"{va(ap):>10} {va(ac):>10} {va(az):>10}")

    # ── 6d. complexes vs aquo ions ──────────────────────────────────────────
    print("\n\n### 6d. IS THE EFFECT LARGER IN THE COMPLEXES THAN IN THE AQUO IONS?")
    print("=" * 116)
    print(f"{'metal':<6} {'aquo d~':>9}   {'P0 d~':>8} {'P1 d~':>8} {'P2 d~':>8}   "
          f"{'ΔP0':>8} {'ΔP1':>8} {'ΔP2':>8}   larger in complexes?")
    print("-" * 116)
    for m, aq in (("Pb", "pb_aquo6"), ("Cu", "cu_aquo6"), ("Zn", "zn_aquo6")):
        a = res[aq].normalised_displacement
        vals = [res[f"{m.lower()}_{s}_cplx"].normalised_displacement
                for s in ("P0", "P1", "P2")]
        deltas = [v - a for v in vals]
        n_up = sum(1 for d in deltas if d > 0)
        print(f"{m:<6} {a:9.4f}   {vals[0]:8.4f} {vals[1]:8.4f} {vals[2]:8.4f}   "
              f"{deltas[0]:+8.4f} {deltas[1]:+8.4f} {deltas[2]:+8.4f}   "
              f"{n_up} of 3 states")

    # ── 6e. cutoff sensitivity ──────────────────────────────────────────────
    print("\n\n### 6e. CUTOFF SENSITIVITY — element-specific vs a uniform 3.20 Å")
    print("=" * 116)
    print("  A cutoff that excluded a genuine Pb donor would manufacture asymmetry, so the")
    print("  descriptors are recomputed at a single generous 3.20 Å for every metal.")
    print("-" * 116)
    print(f"{'species':<12} {'n@element':>10} {'d~@element':>11} {'θ@element':>10}   "
           f"{'n@3.20':>7} {'d~@3.20':>9} {'θ@3.20':>8}  {'changes?'}")
    print("-" * 116)
    for n in AQUO + COMPLEXES:
        _, c1, r1 = row(n)
        _, c2, r2 = row(n, cutoff=3.20)
        v1 = f"{r1.void_angle:.2f}" if r1.void_angle is not None else "n/a"
        v2 = f"{r2.void_angle:.2f}" if r2.void_angle is not None else "n/a"
        ch = "YES" if r1.n_donors != r2.n_donors else "no"
        print(f"{n:<12} {r1.n_donors:>10} {r1.normalised_displacement:>11.4f} "
              f"{v1:>10}   {r2.n_donors:>7} {r2.normalised_displacement:>9.4f} "
              f"{v2:>8}  {ch}")
    print("-" * 116)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
