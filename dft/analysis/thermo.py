#!/usr/bin/env python3
"""PHASE 4 -- assembly of the aquo-ligand exchange free energies.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

Implements REACTIONS.md §5 exactly.  The specification was written before any
energy existed, so the assembly is fixed by design rather than improvised around
whatever ORCA happened to print.

  G_i(aq)      = E_final(i) + G_thermal,qRRHO(i)          [ dft/analysis/G_COMPOSITION.md ]
  dG_exchange  = [ G(complex) + x G(H2O) ] - [ G(aquo) + G(ligand) ] + dG_ss

Both standard-state terms are RECOMPUTED from R, T and the stated
concentrations and asserted against the protocol's printed values, per
REACTIONS.md §5.2 -- a silent divergence between the code and Table 3.1 is
exactly the inconsistency a referee finds.

    python dft/analysis/thermo.py
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from orca_parse import HARTREE_KJ, parse_all  # noqa: E402

R = 8.314462618e-3        # kJ / (mol K), CODATA
T = 298.15                # K
RT = R * T

# Ideal gas at 1 atm occupies 24.46 L/mol at 298.15 K.
V_IDEAL_GAS_L = 24.46
# Pure liquid water, mol/L.
C_WATER = 55.34

DG_GAS_TO_1M = RT * math.log(V_IDEAL_GAS_L)      # per mole of species
DG_WATER_REF = RT * math.log(C_WATER)            # per mole of water released

# REACTIONS.md §5.2 / DFT_PROTOCOL.md §3.5 print these.  Assert agreement rather
# than hard-code, so the code and Table 3.1 cannot drift apart silently.
assert abs(DG_GAS_TO_1M - 7.91) < 0.05, DG_GAS_TO_1M
assert abs(2 * DG_WATER_REF - 19.9) < 0.05, 2 * DG_WATER_REF


@dataclass
class Reaction:
    label: str
    metal: str
    state: str
    aquo: str
    ligand: str
    complex: str
    x: int                # waters released
    denticity: str
    cn: int

    @property
    def dn(self) -> int:
        """Change in the number of species: 2 reactants -> 1 complex + x waters."""
        return (1 + self.x) - 2

    @property
    def dg_ss(self) -> float:
        """kJ/mol.  Recomputed, never hard-coded."""
        return self.dn * DG_GAS_TO_1M - self.x * DG_WATER_REF


# Denticity and CN as MEASURED in Phase 3 (dft/analysis/denticity.py).
# x is the stoichiometric water count fixed by the composition of the clusters
# that were actually computed: [M(H2O)6]2+ has six waters, [M(L)(H2O)4]q has
# four, so two are released.  No [M(L)(H2O)5]q species was ever computed, so no
# x = 1 reaction can be evaluated from this job set.
LIGAND = {"P0": "lig_P0_LH2", "P1": "lig_P1_LH1m", "P2": "lig_P2_L2m"}
MEASURED = {
    ("Pb", "P0"): ("MONODENTATE", 5), ("Pb", "P1"): ("bidentate", 5),
    ("Pb", "P2"): ("bidentate", 4),
    ("Cu", "P0"): ("MONODENTATE", 5), ("Cu", "P1"): ("bidentate", 6),
    ("Cu", "P2"): ("bidentate", 5),
    ("Zn", "P0"): ("bidentate", 6), ("Zn", "P1"): ("bidentate", 6),
    ("Zn", "P2"): ("bidentate", 6),
}

REACTIONS: list[Reaction] = []
for metal, aquo in (("Pb", "pb_aquo6"), ("Cu", "cu_aquo6"), ("Zn", "zn_aquo6")):
    for state in ("P0", "P1", "P2"):
        d, cn = MEASURED[(metal, state)]
        REACTIONS.append(Reaction(
            label=f"{metal} {state}", metal=metal, state=state, aquo=aquo,
            ligand=LIGAND[state], complex=f"{metal.lower()}_{state}_cplx",
            x=2, denticity=d, cn=cn))

# The limitations-discussion alternative: lead from the eight-coordinate ion.
# x = 4, dn = +3 -- the extra water terms do NOT cancel against Cu and Zn.
REACTIONS_PB8 = [
    Reaction(label=f"Pb {s} [aquo8]", metal="Pb", state=s, aquo="pb_aquo8",
             ligand=LIGAND[s], complex=f"pb_{s}_cplx", x=4,
             denticity=MEASURED[("Pb", s)][0], cn=MEASURED[("Pb", s)][1])
    for s in ("P0", "P1", "P2")
]


def gibbs(jobs) -> dict[str, float]:
    """G per species in kJ/mol, from E_final + G_thermal,qRRHO."""
    out = {}
    for name, j in jobs.items():
        g = j.e_final + j.g_minus_eel
        assert abs(g - j.gibbs) < 1e-7, name    # identity 4 of G_COMPOSITION.md
        out[name] = g * HARTREE_KJ
    return out


def dg_exchange(rxn: Reaction, G: dict[str, float]) -> dict[str, float]:
    products = G[rxn.complex] + rxn.x * G["water"]
    reactants = G[rxn.aquo] + G[rxn.ligand]
    raw = products - reactants
    return {"raw": raw, "ss": rxn.dg_ss, "total": raw + rxn.dg_ss}


def main() -> int:
    jobs = parse_all()
    G = gibbs(jobs)

    print("=" * 116)
    print("PHASE 4 — AQUO-LIGAND EXCHANGE FREE ENERGIES")
    print("REACTIONS.md §5 · DFT_PROTOCOL.md §3.5 · G composition in dft/analysis/G_COMPOSITION.md")
    print("=" * 116)

    print("\n### 4a. STANDARD-STATE CORRECTION — recomputed from R, T and the stated "
          "concentrations")
    print("-" * 116)
    print(f"  R  = {R * 1000:.6f} J/(mol K)      T = {T} K      RT = {RT:.5f} kJ/mol")
    print(f"  Ideal gas 1 atm -> 1 mol/L, per species :  RT ln({V_IDEAL_GAS_L}) "
          f"= {DG_GAS_TO_1M:+.4f} kJ/mol   (protocol prints 7.91)")
    print(f"  Water -> pure liquid {C_WATER} mol/L, per water: -RT ln({C_WATER}) "
          f"= {-DG_WATER_REF:+.4f} kJ/mol   (protocol prints -9.95)")
    print(f"  For x = 2, dn = +1 :  dG_ss = (+1)({DG_GAS_TO_1M:.4f}) - 2({DG_WATER_REF:.4f}) "
          f"= {1 * DG_GAS_TO_1M - 2 * DG_WATER_REF:+.3f} kJ/mol   (protocol prints -12.0)")
    print(f"  For x = 4, dn = +3 :  dG_ss = (+3)({DG_GAS_TO_1M:.4f}) - 4({DG_WATER_REF:.4f}) "
          f"= {3 * DG_GAS_TO_1M - 4 * DG_WATER_REF:+.3f} kJ/mol   [pb_aquo8 alternative]")

    print("\n\n### 4b. G PER SPECIES  (kJ/mol, = E_final + G_thermal,qRRHO)")
    print("-" * 116)
    print(f"{'species':<14} {'E_final / Eh':>18} {'G_therm / Eh':>14} "
          f"{'G / Eh':>18} {'G / kJ/mol':>18}")
    print("-" * 116)
    for name in jobs:
        j = jobs[name]
        print(f"{name:<14} {j.e_final:18.8f} {j.g_minus_eel:14.8f} "
              f"{j.e_final + j.g_minus_eel:18.8f} {G[name]:18.3f}")

    print("\n\n### 4c. dG_exchange — THE NINE HEADLINE REACTIONS")
    print("=" * 116)
    print("  [M(H2O)6]2+ + L  ->  [M(L)(H2O)4]q + 2 H2O        x = 2, dn = +1 for all nine")
    print("-" * 116)
    print(f"{'metal':<6} {'state':<6} {'denticity':>12} {'CN':>4} {'x':>3} {'Δn':>4} "
          f"{'ΔG_raw':>11} {'ΔG_ss':>8} {'ΔG_exchange':>13}  comparison validity")
    print("-" * 116)
    dg: dict[tuple[str, str], float] = {}
    for r in REACTIONS:
        d = dg_exchange(r, G)
        dg[(r.metal, r.state)] = d["total"]
        note = ("Pb/Cu matched; Zn mismatched" if r.state == "P0"
                else "all three matched")
        print(f"{r.metal:<6} {r.state:<6} {r.denticity:>12} {r.cn:4d} {r.x:3d} "
              f"{r.dn:+4d} {d['raw']:11.2f} {d['ss']:8.2f} {d['total']:13.2f}  {note}")
    print("-" * 116)
    print("  All energies kJ/mol at 298.15 K.  Negative = exchange is favourable.")

    print("\n\n### 4d. ΔΔG — THE CROSS-METAL COMPARISONS")
    print("=" * 116)
    print("  ΔΔG(Pb-M) = ΔG_exchange(Pb) - ΔG_exchange(M).  Negative = the galloyl site")
    print("  prefers Pb(II) over the competitor.")
    print("-" * 116)
    print(f"{'state':<6} {'ΔG(Pb)':>10} {'ΔG(Cu)':>10} {'ΔG(Zn)':>10} "
          f"{'ΔΔG(Pb-Cu)':>12} {'matched?':>10} {'ΔΔG(Pb-Zn)':>12} {'matched?':>10}")
    print("-" * 116)
    ddg = {}
    for st in ("P0", "P1", "P2"):
        pc = dg[("Pb", st)] - dg[("Cu", st)]
        pz = dg[("Pb", st)] - dg[("Zn", st)]
        ddg[st] = (pc, pz)
        m_pc = "YES" if st != "P0" or True else ""
        m_pz = "YES" if st != "P0" else "NO — caveat"
        print(f"{st:<6} {dg[('Pb', st)]:10.2f} {dg[('Cu', st)]:10.2f} "
              f"{dg[('Zn', st)]:10.2f} {pc:12.2f} {'YES':>10} {pz:12.2f} {m_pz:>10}")
    print("-" * 116)
    print("  ΔΔG(Pb-Cu) is denticity-MATCHED at all three states: Pb and Cu are both")
    print("  monodentate at P0 and both bidentate at P1 and P2.")
    print("  ΔΔG(Pb-Zn) is denticity-MATCHED at P1 and P2 and MISMATCHED at P0, where Pb is")
    print("  monodentate and Zn bidentate. The P0 Pb-Zn row carries a stated caveat.")

    print("\n  Cu-Zn, for completeness:")
    for st in ("P0", "P1", "P2"):
        cz = dg[("Cu", st)] - dg[("Zn", st)]
        tag = "mismatched (Cu mono, Zn bi)" if st == "P0" else "matched"
        print(f"    ΔΔG(Cu-Zn)|{st} = {cz:+8.2f} kJ/mol   [{tag}]")

    print("\n\n### 4e. THE SAME, USING [Pb(H2O)8]2+ AS THE LEAD REFERENCE STATE")
    print("=" * 116)
    print("  [Pb(H2O)8]2+ + L  ->  [Pb(L)(H2O)4]q + 4 H2O       x = 4, dn = +3")
    print("  LIMITATIONS MATERIAL ONLY (DFT_PROTOCOL.md §2.2, ruling D-01). The two extra")
    print("  water-release terms and two extra standard-state terms enter ΔG(Pb) and NOT")
    print("  ΔG(Cu) or ΔG(Zn), so these ΔΔG values are NOT isodesmic and are NOT the")
    print("  headline comparison.")
    print("-" * 116)
    print(f"{'state':<6} {'ΔG(Pb) aquo8':>14} {'ΔG(Pb) aquo6':>14} {'shift':>9} "
          f"{'ΔΔG(Pb-Cu)':>12} {'ΔΔG(Pb-Zn)':>12}")
    print("-" * 116)
    for r in REACTIONS_PB8:
        d = dg_exchange(r, G)
        base = dg[("Pb", r.state)]
        print(f"{r.state:<6} {d['total']:14.2f} {base:14.2f} {d['total'] - base:9.2f} "
              f"{d['total'] - dg[('Cu', r.state)]:12.2f} "
              f"{d['total'] - dg[('Zn', r.state)]:12.2f}")
    print("-" * 116)

    print("\n\n### 4f. ORDERING")
    print("=" * 116)
    for st in ("P0", "P1", "P2"):
        vals = sorted((("Pb", dg[("Pb", st)]), ("Cu", dg[("Cu", st)]),
                       ("Zn", dg[("Zn", st)])), key=lambda t: t[1])
        order = " < ".join(f"{m} ({v:.1f})" for m, v in vals)
        print(f"  {st}:  most favourable first:  {order}")
        print(f"        preference order (strongest binder first): "
              f"{' > '.join(m for m, _ in vals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
