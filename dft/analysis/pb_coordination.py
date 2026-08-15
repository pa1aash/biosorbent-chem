#!/usr/bin/env python3
"""PHASE 7 -- the lead(II) coordination number at DFT level. Limitations material.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

Ruling D-01 fixed n = 6 for all three metals so that the nine exchange reactions
are isodesmic, and named the CN question as a stated limitation (DFT_PROTOCOL.md
§2.2, attack A33).  The limitation paragraph asks for exactly two things:

  1. a comparison of both lead coordination numbers at the DENSITY-FUNCTIONAL
     level rather than the semi-empirical level used for screening;
  2. an assessment of which is favoured IN WATER rather than in the gas phase,
     with implicit solvation applied to both.

Both are now available, because pb_aquo6 and pb_aquo8 were optimised under the
production protocol with SMD throughout.  This script reports them.

THIS IS SECTION 5.3 MATERIAL, NOT A HEADLINE RESULT.  The reference state for
every reported exchange free energy remains [Pb(H2O)6]2+.

    python dft/analysis/pb_coordination.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

DFT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DFT / "structures"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from geom_utils import M_O_CUTOFF, METALS, classify_oxygens, read_xyz  # noqa: E402
from orca_parse import HARTREE_KJ, OUTPUTS, parse_all  # noqa: E402
from thermo import DG_GAS_TO_1M, DG_WATER_REF, gibbs  # noqa: E402


def pb_o(name: str) -> list[float]:
    syms, xyz, _ = read_xyz(OUTPUTS / name / f"{name}.xyz")
    m = syms.index(next(s for s in syms if s in METALS))
    return sorted(float(np.linalg.norm(xyz[o] - xyz[m]))
                  for o in classify_oxygens(syms, xyz))


def xtb_energies() -> dict[str, float]:
    out = {}
    with open(DFT / "structures" / "xtb_prescreen.csv") as fh:
        for row in csv.DictReader(fh):
            out[row["species"]] = float(row["E_xtb_kJ_per_mol"])
    return out


def main() -> int:
    jobs = parse_all()
    G = gibbs(jobs)
    E = {n: jobs[n].e_final * HARTREE_KJ for n in jobs}
    Gt = {n: jobs[n].g_minus_eel * HARTREE_KJ for n in jobs}
    x = xtb_energies()

    print("=" * 108)
    print("PHASE 7 — Pb(II) COORDINATION NUMBER AT DFT LEVEL")
    print("DFT_PROTOCOL.md §2.1, §2.2, §6 · ruling D-01 · attack A33")
    print("LIMITATIONS MATERIAL FOR REPORT §5.3 — NOT A HEADLINE RESULT")
    print("=" * 108)

    # ── 7a. the hydration reaction ──────────────────────────────────────────
    print("\n### 7a. THE HYDRATION REACTION, AT BOTH LEVELS OF THEORY")
    print("-" * 108)
    print("    [Pb(H2O)6]2+  +  2 H2O   ->   [Pb(H2O)8]2+        Δn = -2, 2 waters CONSUMED")
    print("    Negative ΔG favours CN = 8.  Positive ΔG favours CN = 6.")
    print("-" * 108)

    # GFN2-xTB: total electronic energies only, gas-phase-style, ALPB(water).
    d_xtb = x["pb_aquo8"] - x["pb_aquo6"] - 2 * x["water"]

    d_e = E["pb_aquo8"] - E["pb_aquo6"] - 2 * E["water"]
    d_th = Gt["pb_aquo8"] - Gt["pb_aquo6"] - 2 * Gt["water"]
    # dn = -2 species; 2 waters are CONSUMED, so the water-reference term
    # enters with the opposite sign to the exchange reactions.
    d_ss = (-2) * DG_GAS_TO_1M - (-2) * DG_WATER_REF
    d_g = d_e + d_th + d_ss

    print(f"  GFN2-xTB / ALPB(water)   ΔE (electronic only)     "
          f"{d_xtb:+10.2f} kJ/mol   ->  favours CN = "
          f"{'8' if d_xtb < 0 else '6'}")
    print(f"  PBE0-D3BJ / def2-TZVP / SMD(water):")
    print(f"      ΔE  electronic (incl. SMD + D3BJ)            {d_e:+10.2f} kJ/mol"
          f"   ->  favours CN = {'8' if d_e < 0 else '6'}")
    print(f"      ΔG_thermal  (ZPE + thermal + -TS, quasi-RRHO) {d_th:+10.2f} kJ/mol")
    print(f"      ΔG_ss       standard-state                    {d_ss:+10.2f} kJ/mol")
    print(f"      " + "-" * 62)
    print(f"      ΔG  TOTAL                                    {d_g:+10.2f} kJ/mol"
          f"   ->  favours CN = {'8' if d_g < 0 else '6'}")
    print("-" * 108)
    print(f"  DOES THE GFN2 CN = 8 PREFERENCE SURVIVE AT DFT WITH SMD?  "
          f"{'YES' if d_g < 0 else 'NO'}")
    print(f"  Swing between the two levels: {d_g - d_xtb:+.1f} kJ/mol.")
    print("\n  Where the reversal comes from: the DFT ELECTRONIC energy agrees with GFN2 in")
    print(f"  direction ({d_e:+.1f} kJ/mol, favouring CN = 8) but at roughly half the magnitude.")
    print(f"  It is the thermal and entropic term ({d_th:+.1f} kJ/mol) that reverses the")
    print("  preference: binding two additional waters into the cluster costs their")
    print("  translational and rotational entropy, and the GFN2 screen compared electronic")
    print("  energies only and therefore could not see that cost.")

    # ── 7b. geometry ────────────────────────────────────────────────────────
    print("\n\n### 7b. THE OPTIMISED GEOMETRIES — WHAT THE OPTIMISER DID WITH EIGHT WATERS")
    print("-" * 108)
    for n in ("pb_aquo6", "pb_aquo8"):
        d = pb_o(n)
        cut = M_O_CUTOFF["Pb"]
        inner = [v for v in d if v < cut]
        outer = [v for v in d if v >= cut]
        print(f"\n  {n}   waters in cluster: {len(d)}")
        print(f"    all Pb–O distances / Å : " + "  ".join(f"{v:.3f}" for v in d))
        print(f"    within {cut:.2f} Å        : {len(inner)}  "
              f"(mean {np.mean(inner):.3f} Å, range {min(inner):.3f}–{max(inner):.3f} Å)")
        if outer:
            print(f"    BEYOND {cut:.2f} Å        : {len(outer)}  at "
                  + ", ".join(f"{v:.3f} Å" for v in outer)
                  + "  — second shell")
    print("\n  ** The eight-water cluster does not stay eight-coordinate. Two waters relax")
    print("     beyond the first-shell cutoff to 3.793 Å and 4.089 Å, leaving a SIX-coordinate")
    print("     first shell. This is independent structural evidence for the same conclusion")
    print("     the free energy reaches: at this level of theory, in this solvation model,")
    print("     lead(II) does not hold eight waters in its inner sphere.")
    print("\n  ** The six-water cluster is not six-coordinate either: one water sits at 4.005 Å,")
    print("     giving a FIVE-coordinate first shell. The composition [Pb(H2O)6]2+ is what fixes")
    print("     the reaction stoichiometry; the first-shell coordination number is a measured")
    print("     property of the optimised structure and is 5.")

    # ── 7c. §6 validation ───────────────────────────────────────────────────
    print("\n\n### 7c. PROTOCOL VALIDATION — THE Pb–O BOND LENGTH (DFT_PROTOCOL.md §6)")
    print("-" * 108)
    for n in ("pb_aquo6", "pb_aquo8"):
        d = pb_o(n)
        inner = [v for v in d if v < M_O_CUTOFF["Pb"]]
        print(f"  {n:<10}  mean first-shell Pb–O = {np.mean(inner):.3f} Å  "
              f"(n = {len(inner)}, SD {np.std(inner, ddof=1):.3f} Å, "
              f"range {min(inner):.3f}–{max(inner):.3f} Å)")
    print("\n  The comparison against published EXAFS / X-ray hydration structures REQUIRES A")
    print("  VERIFIED CITATION and is NOT made here. Per CLAUDE.md §3 and §6, no literature")
    print("  value is quoted from recollection. The computed numbers above stand; the")
    print("  deviation in Å and in per cent cannot be computed until a reference resolves")
    print("  against Crossref and has been read. Carried to docs/DATA_REQUEST.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
