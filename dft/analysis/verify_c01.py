#!/usr/bin/env python3
"""PHASE 2 -- re-verify the C-01 energy identity on charged and open-shell species.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

S04 established, from the completed `water` job, that ORCA's FINAL SINGLE POINT
ENERGY already contains the SMD G_CDS term and the D3(BJ) dispersion correction,
so thermo.py must not add either again.  That check was made on a three-atom
neutral closed-shell molecule.

REACTIONS.md §5.1 and JOB_QUEUE_STATUS.md §5 both require it re-confirmed on a
metal complex before any free energy is assembled, because a double-counted
G_CDS would corrupt every number in the computational arm silently and in the
same direction.

This script re-runs the decomposition on:

  pb_P0_cplx   +2 charged, solvated, ECP element, 34 atoms
  cu_P0_cplx   +2 charged, solvated, OPEN SHELL doublet (UKS), 34 atoms

and on every other species as a sweep, so the identity is shown to close for all
seventeen rather than for two.

    python dft/analysis/verify_c01.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from orca_parse import HARTREE_KJ, JOBS, parse, parse_all  # noqa: E402

# Tolerance: ORCA prints the components to 9 decimal places and the final energy
# to 12, so the identity should close to well inside a micro-Hartree.  1e-8 Eh is
# 2.6e-5 kJ/mol -- six orders of magnitude below anything reported.
TOL = 1e-8


def show(name: str) -> bool:
    j = parse(name)
    print(f"\n{'=' * 100}")
    print(f"{name}   charge {j.charge:+d}   multiplicity {j.mult}   "
          f"{j.n_atoms} atoms" +
          ("   [OPEN SHELL, UKS]" if j.mult and j.mult > 1 else "   [closed shell]"))
    print("=" * 100)

    a = j.e_scf_smd      # Total energy after final integration (incl. CPCM dielectric)
    b = j.g_cds          # SMD CDS (Gcds)
    c = j.e_after_cds    # Total Energy after SMD CDS correction
    d = j.e_disp         # D3(BJ) dispersion correction
    e = j.e_final        # FINAL SINGLE POINT ENERGY

    print("  ORCA's own printed components, last occurrence in the file:\n")
    print(f"    Total energy after final integration    {a:+.9f} Eh   "
          f"(SCF incl. SMD electrostatics / CPCM dielectric)")
    print(f"    SMD CDS (Gcds)                          {b:+.9f} Eh   "
          f"(cavity-dispersion-solvent-structure)")
    print(f"    Total Energy after SMD CDS correction   {c:+.9f} Eh")
    print(f"    Dispersion correction                   {d:+.9f} Eh   (D3BJ)")
    print(f"    FINAL SINGLE POINT ENERGY               {e:+.9f} Eh")

    r1 = a + b
    r2 = c + d
    ok1 = abs(r1 - c) < TOL
    ok2 = abs(r2 - e) < TOL

    print("\n  Identity 1 —  E(SCF,SMD) + G_CDS  =  E(after CDS)")
    print(f"    {a:+.9f}  {b:+.9f}  =  {r1:+.9f}")
    print(f"    printed                            =  {c:+.9f}")
    print(f"    residual = {r1 - c:+.3e} Eh   ->  {'CLOSES' if ok1 else '*** DOES NOT CLOSE ***'}")

    print("\n  Identity 2 —  E(after CDS) + E_D3BJ  =  FINAL SINGLE POINT ENERGY")
    print(f"    {c:+.9f}  {d:+.9f}  =  {r2:+.9f}")
    print(f"    printed                            =  {e:+.9f}")
    print(f"    residual = {r2 - e:+.3e} Eh   ->  {'CLOSES' if ok2 else '*** DOES NOT CLOSE ***'}")

    # The thermochemistry block's "Electronic energy" is the quantity ORCA adds
    # its thermal correction to.  If it is not the FINAL SINGLE POINT ENERGY,
    # then G would be built on a different electronic energy than the one being
    # decomposed here, and the decomposition would be irrelevant.
    ok3 = abs(j.thermo_e_el - e) < 1e-7
    print("\n  Identity 3 —  the thermochemistry block's E(el)  =  FINAL SINGLE POINT ENERGY")
    print(f"    thermo E(el)                       =  {j.thermo_e_el:+.9f} Eh")
    print(f"    FINAL SINGLE POINT ENERGY          =  {e:+.9f} Eh")
    print(f"    residual = {j.thermo_e_el - e:+.3e} Eh   ->  "
          f"{'CLOSES' if ok3 else '*** DOES NOT CLOSE ***'}")

    ok4 = abs((j.thermo_e_el + j.g_minus_eel) - j.gibbs) < 1e-7
    print("\n  Identity 4 —  E(el) + G_thermal(qRRHO)  =  ORCA 'Final Gibbs free energy'")
    print(f"    {j.thermo_e_el:+.9f}  {j.g_minus_eel:+.9f}  =  "
          f"{j.thermo_e_el + j.g_minus_eel:+.9f}")
    print(f"    printed                            =  {j.gibbs:+.9f}")
    print(f"    residual = {(j.thermo_e_el + j.g_minus_eel) - j.gibbs:+.3e} Eh   ->  "
          f"{'CLOSES' if ok4 else '*** DOES NOT CLOSE ***'}")

    print(f"\n  G_CDS in energy units:  {b * HARTREE_KJ:+.3f} kJ/mol   "
          f"— the magnitude that would be double-counted if added again.")
    print(f"  D3BJ  in energy units:  {d * HARTREE_KJ:+.3f} kJ/mol")

    return ok1 and ok2 and ok3 and ok4


def main() -> int:
    print("=" * 100)
    print("PHASE 2 — C-01 ENERGY IDENTITY, RE-VERIFIED ON A CHARGED METAL COMPLEX")
    print("           AND ON AN OPEN-SHELL SPECIES")
    print("REACTIONS.md §5.1 · JOB_QUEUE_STATUS.md §5")
    print("=" * 100)

    named = ["pb_P0_cplx", "cu_P0_cplx"]
    all_ok = all(show(n) for n in named)

    print(f"\n{'=' * 100}")
    print("SWEEP — the same four identities across all seventeen jobs")
    print("=" * 100)
    print(f"{'job':<13} {'chg':>4} {'mult':>5} {'id1':>6} {'id2':>6} {'id3':>6} "
          f"{'id4':>6} {'G_CDS / kJ/mol':>15} {'D3BJ / kJ/mol':>14}")
    print("-" * 100)
    sweep_ok = True
    for name, j in parse_all().items():
        i1 = abs((j.e_scf_smd + j.g_cds) - j.e_after_cds) < TOL
        i2 = abs((j.e_after_cds + j.e_disp) - j.e_final) < TOL
        i3 = abs(j.thermo_e_el - j.e_final) < 1e-7
        i4 = abs((j.thermo_e_el + j.g_minus_eel) - j.gibbs) < 1e-7
        sweep_ok &= i1 and i2 and i3 and i4
        tick = lambda b: "ok" if b else "FAIL"  # noqa: E731
        print(f"{name:<13} {j.charge:>+4d} {j.mult:>5d} {tick(i1):>6} {tick(i2):>6} "
              f"{tick(i3):>6} {tick(i4):>6} {j.g_cds * HARTREE_KJ:>15.3f} "
              f"{j.e_disp * HARTREE_KJ:>14.3f}")

    print("\n" + "=" * 100)
    if all_ok and sweep_ok:
        print("C-01 RE-CONFIRMED.  FINAL SINGLE POINT ENERGY = E(SCF,SMD electrostatic)")
        print("                    + G_CDS + E_D3BJ, on charged, open-shell and ECP species alike.")
        print("thermo.py MUST NOT add G_CDS or the dispersion correction again.")
        print("=" * 100)
        return 0
    print("*** C-01 IDENTITY DOES NOT CLOSE — STOP.  NO FREE ENERGY MAY BE ASSEMBLED. ***")
    print("=" * 100)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
