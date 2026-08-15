#!/usr/bin/env python3
"""PHASE 5 -- does the computed ordering reproduce Pb > Cu > Zn?

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

This script answers the question the computational arm exists to answer, and it
answers it from the numbers rather than from the expectation.  DFT_PROTOCOL.md
§1.3 and §5 both pre-commit to this: "if the calculation does not show that, the
report reports what it shows."

It also sizes the gap against the Stage-1 outline's claimed selectivity factors
via dG = -RT ln(alpha).  Those alpha values are CLAIMS TO BE TESTED, held in
docs/02_PROTOCOL_AUDIT.md Table C; they are not inputs and they do not seed
CANONICAL_NUMBERS.yaml.

    python dft/analysis/selectivity.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from thermo import REACTIONS, RT, dg_exchange, gibbs  # noqa: E402
from orca_parse import parse_all  # noqa: E402

# Stage-1 outline claims. docs/02_PROTOCOL_AUDIT.md Table C. NOT inputs.
ALPHA_CLAIMED = {"Pb/Cu": 3.63, "Pb/Zn": 7.03}


def main() -> int:
    G = gibbs(parse_all())
    dg = {(r.metal, r.state): dg_exchange(r, G)["total"] for r in REACTIONS}

    print("=" * 112)
    print("PHASE 5 — THE ORDERING, STATED PLAINLY")
    print("=" * 112)

    # ── Q1 ───────────────────────────────────────────────────────────────────
    print("\n### Q1. DOES THE COMPUTED ORDERING REPRODUCE Pb > Cu > Zn?")
    print("-" * 112)
    orders = {}
    for st in ("P0", "P1", "P2"):
        ranked = sorted((("Pb", dg[("Pb", st)]), ("Cu", dg[("Cu", st)]),
                         ("Zn", dg[("Zn", st)])), key=lambda t: t[1])
        orders[st] = [m for m, _ in ranked]
    target = ["Pb", "Cu", "Zn"]

    print(f"{'state':<6} {'ΔG(Pb)':>10} {'ΔG(Cu)':>10} {'ΔG(Zn)':>10}   "
          f"{'computed order':<20} {'= Pb > Cu > Zn?':<16} {'Pb over Cu?':<12} {'Pb over Zn?'}")
    print("-" * 112)
    for st in ("P0", "P1", "P2"):
        o = orders[st]
        print(f"{st:<6} {dg[('Pb', st)]:10.2f} {dg[('Cu', st)]:10.2f} "
              f"{dg[('Zn', st)]:10.2f}   {' > '.join(o):<20} "
              f"{('YES' if o == target else 'NO'):<16} "
              f"{('yes' if dg[('Pb', st)] < dg[('Cu', st)] else 'NO'):<12} "
              f"{('yes' if dg[('Pb', st)] < dg[('Zn', st)] else 'NO')}")
    print("-" * 112)
    n_hit = sum(1 for st in orders if orders[st] == target)
    print(f"  Pb > Cu > Zn is reproduced at {n_hit} of 3 protonation states.")

    # ── Q2 ───────────────────────────────────────────────────────────────────
    print("\n\n### Q2. MAGNITUDE OF THE COMPUTED PREFERENCE, kJ/mol")
    print("-" * 112)
    print(f"{'state':<6} {'ΔΔG(Pb-Cu)':>12} {'direction':<28} "
          f"{'ΔΔG(Pb-Zn)':>12} {'direction':<28} {'denticity'}")
    print("-" * 112)
    for st in ("P0", "P1", "P2"):
        pc = dg[("Pb", st)] - dg[("Cu", st)]
        pz = dg[("Pb", st)] - dg[("Zn", st)]
        dc = "Pb preferred over Cu" if pc < 0 else "Cu preferred over Pb"
        dz = "Pb preferred over Zn" if pz < 0 else "Zn preferred over Pb"
        dent = ("Pb/Cu matched, Pb/Zn MISMATCHED" if st == "P0"
                else "all matched")
        print(f"{st:<6} {pc:12.2f} {dc:<28} {pz:12.2f} {dz:<28} {dent}")
    print("-" * 112)

    # ── Q3 ───────────────────────────────────────────────────────────────────
    print("\n\n### Q3. IS THE ORDERING CONSISTENT ACROSS PROTONATION STATES?")
    print("-" * 112)
    unique = {tuple(o) for o in orders.values()}
    for st in ("P0", "P1", "P2"):
        print(f"    {st}:  {' > '.join(orders[st])}")
    print(f"\n  Distinct orderings across the three states: {len(unique)}.")
    print(f"  CONSISTENT: {'yes' if len(unique) == 1 else 'NO — the ordering CHANGES with deprotonation'}")
    print("\n  Pb over Cu:  " + ", ".join(
        f"{st} {'yes' if dg[('Pb', st)] < dg[('Cu', st)] else 'NO'}"
        for st in ("P0", "P1", "P2")))
    print("  Pb over Zn:  " + ", ".join(
        f"{st} {'yes' if dg[('Pb', st)] < dg[('Zn', st)] else 'NO'}"
        for st in ("P0", "P1", "P2")))

    # ── §4.6 material: what ΔΔG the outline's alpha would require ────────────
    print("\n\n### Q4. WHAT ΔΔG WOULD THE OUTLINE'S SELECTIVITY FACTORS REQUIRE?")
    print("=" * 112)
    print("  ΔΔG = -RT ln(alpha) at 298.15 K.  RT = %.5f kJ/mol." % RT)
    print("  The alpha values are Stage-1 OUTLINE CLAIMS (docs/02_PROTOCOL_AUDIT.md Table C),")
    print("  not measured inputs, and they are not carried into CANONICAL_NUMBERS.yaml.")
    print("-" * 112)
    required = {}
    for pair, a in ALPHA_CLAIMED.items():
        required[pair] = -RT * math.log(a)
        print(f"  alpha({pair}) = {a:.2f}   ->   ΔΔG required = -RT ln({a:.2f}) "
              f"= {required[pair]:+7.3f} kJ/mol")

    print("\n  Computed against required — SIZE OF THE DISCREPANCY")
    print("-" * 112)
    print(f"{'pair':<8} {'state':<6} {'computed':>10} {'required':>10} "
          f"{'difference':>11} {'ratio':>9} {'sign agrees?':>13}  {'denticity'}")
    print("-" * 112)
    for pair, key in (("Pb/Cu", "Cu"), ("Pb/Zn", "Zn")):
        for st in ("P0", "P1", "P2"):
            comp = dg[("Pb", st)] - dg[(key, st)]
            req = required[pair]
            ratio = comp / req
            same = (comp < 0) == (req < 0)
            dent = ("MISMATCHED" if (st == "P0" and key == "Zn") else "matched")
            print(f"{pair:<8} {st:<6} {comp:10.2f} {req:10.2f} "
                  f"{comp - req:11.2f} {ratio:8.2f}x {('yes' if same else 'NO'):>13}  {dent}")
    print("-" * 112)
    print("  ratio > 1 with the same sign = computed preference LARGER than the experimental")
    print("  claim requires. A NEGATIVE ratio means the computed preference points the OTHER WAY")
    print("  from the claim: the calculation does not merely overshoot, it disagrees in sign.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
