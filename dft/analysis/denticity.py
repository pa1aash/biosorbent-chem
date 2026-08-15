#!/usr/bin/env python3
"""PHASE 3 -- geometry, denticity and the number of waters displaced.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

DFT_PROTOCOL.md §3.7, attack A31.  Denticity is MEASURED on every optimised
complex, never assumed, and the two M-O(galloyl) distances are reported
INDIVIDUALLY -- averaging is exactly what would hide a monodentate structure.

The first-shell cutoffs and the oxygen classification are imported from
structures/geom_utils.py so that the production verdicts are directly comparable
with the GFN2-xTB pre-screen verdicts, as §3.7 requires.

Cutoffs are ELEMENT-SPECIFIC: Pb 3.20 A, Cu 2.80 A, Zn 2.80 A.  A single 2.80 A
cutoff applied to lead would be wrong -- Pb-O distances run appreciably longer
than Cu-O for purely ionic-radius reasons, and a cutoff that excluded a genuine
Pb donor would manufacture the very asymmetry the hemidirection analysis exists
to measure.  Because one Pb contact (pb_P0_cplx, 2.936 A) falls between the two
cutoffs, BOTH verdicts are printed and the sensitivity is stated rather than
buried.

    python dft/analysis/denticity.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

DFT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DFT / "structures"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from geom_utils import M_O_CUTOFF, METALS, classify_oxygens, read_xyz  # noqa: E402
from qc_checkpoint import phenolic_oxygens  # noqa: E402
from orca_parse import OUTPUTS  # noqa: E402

COMPLEXES = ["pb_P0_cplx", "pb_P1_cplx", "pb_P2_cplx",
             "cu_P0_cplx", "cu_P1_cplx", "cu_P2_cplx",
             "zn_P0_cplx", "zn_P1_cplx", "zn_P2_cplx"]
AQUO = ["pb_aquo6", "pb_aquo8", "cu_aquo6", "zn_aquo6"]

UNIFORM_CUTOFF = 2.80   # the value quoted in the S05 checkpoint note
PSTATE = {"P0": "P0 (LH2, neutral)", "P1": "P1 (LH-, mono-deprot.)",
          "P2": "P2 (L2-, bis-deprot.)"}


def measure(name: str) -> dict:
    """Full first-shell description of one optimised structure."""
    syms, xyz, _ = read_xyz(OUTPUTS / name / f"{name}.xyz")
    metal = next(s for s in syms if s in METALS)
    m = syms.index(metal)
    kinds = classify_oxygens(syms, xyz)
    cutoff = M_O_CUTOFF[metal]

    def dist(o: int) -> float:
        return float(np.linalg.norm(xyz[o] - xyz[m]))

    phen = sorted(phenolic_oxygens(syms, xyz), key=dist)
    galloyl = [(o, dist(o), kinds[o]) for o in phen]

    all_o = sorted(((dist(o), o, kinds[o]) for o in kinds))
    shell = [t for t in all_o if t[0] < cutoff]
    shell_u = [t for t in all_o if t[0] < UNIFORM_CUTOFF]

    n_water_cluster = sum(1 for v in kinds.values() if v == "OH2")
    n_water_shell = sum(1 for d, o, k in shell if k == "OH2")
    n_lig_shell = len(shell) - n_water_shell

    n_bound = sum(1 for _, d, _ in galloyl if d < cutoff)
    n_bound_u = sum(1 for _, d, _ in galloyl if d < UNIFORM_CUTOFF)
    verdict = {2: "bidentate", 1: "MONODENTATE", 0: "DISSOCIATED"}.get(min(n_bound, 2))
    verdict_u = {2: "bidentate", 1: "MONODENTATE", 0: "DISSOCIATED"}.get(min(n_bound_u, 2))

    return dict(
        name=name, metal=metal, cutoff=cutoff, galloyl=galloyl,
        all_o=all_o, shell=shell, shell_uniform=shell_u,
        cn=len(shell), cn_uniform=len(shell_u),
        n_water_cluster=n_water_cluster, n_water_shell=n_water_shell,
        n_lig_shell=n_lig_shell, denticity=verdict,
        denticity_uniform=verdict_u, n_bound=n_bound,
        second_shell=[t for t in all_o if t[0] >= cutoff and t[2] == "OH2"],
    )


def main() -> int:
    print("=" * 118)
    print("PHASE 3 — GEOMETRY AND DENTICITY (DFT_PROTOCOL.md §3.7, attack A31)")
    print("Distances reported INDIVIDUALLY and never averaged.")
    print("=" * 118)

    res = {n: measure(n) for n in COMPLEXES + AQUO}

    # ── 3a. the aquo reference states ────────────────────────────────────────
    print("\n### 3a. THE AQUO REFERENCE STATES — first shell as OPTIMISED, not as built")
    print("-" * 118)
    print(f"{'species':<11} {'metal':>5} {'H2O in cluster':>15} {'cutoff':>7} "
          f"{'CN (first shell)':>17}   M–O distances / Å (all cluster oxygens)")
    print("-" * 118)
    for n in AQUO:
        r = res[n]
        ds = " ".join(f"{d:.3f}" for d, _, _ in r["all_o"])
        print(f"{n:<11} {r['metal']:>5} {r['n_water_cluster']:>15} "
              f"{r['cutoff']:>7.2f} {r['cn']:>17}   {ds}")
    print("-" * 118)
    for n in AQUO:
        r = res[n]
        if r["cn"] < r["n_water_cluster"]:
            lost = r["n_water_cluster"] - r["cn"]
            outer = ", ".join(f"{d:.3f} Å" for d, _, _ in r["second_shell"])
            print(f"  ** {n}: {lost} water(s) relaxed OUT of the first shell during "
                  f"optimisation — now at {outer}.")
            print(f"     The cluster still contains {r['n_water_cluster']} waters, so the "
                  f"stoichiometry is unchanged; the FIRST-SHELL coordination number is "
                  f"{r['cn']}, not {r['n_water_cluster']}.")

    # ── 3b. the nine complexes ───────────────────────────────────────────────
    print("\n\n### 3b. THE NINE METAL–LIGAND COMPLEXES")
    print("=" * 118)
    for n in COMPLEXES:
        r = res[n]
        st = n.split("_")[1]
        print(f"\n{n}   metal {r['metal']}   {PSTATE[st]}   "
              f"first-shell cutoff {r['cutoff']:.2f} Å")
        for i, (o, d, k) in enumerate(r["galloyl"], 1):
            tag = "within" if d < r["cutoff"] else "OUTSIDE"
            role = "chelating pair" if i <= 2 else "distal 5-OH"
            print(f"    galloyl O#{i} (atom {o:>2}, {k:<8}) {r['metal']}–O = {d:7.3f} Å  "
                  f"[{tag} first shell]   {role}")
        print(f"    DENTICITY VERDICT      : {r['denticity']}")
        print(f"    first-shell composition: {r['cn']} O total "
              f"= {r['n_lig_shell']} galloyl + {r['n_water_shell']} water")
        print(f"    coordination number    : {r['cn']}")
        print(f"    waters IN THE CLUSTER  : {r['n_water_cluster']}   "
              f"(fixes the reaction stoichiometry)")
        print(f"    waters IN FIRST SHELL  : {r['n_water_shell']}", end="")
        if r["n_water_shell"] < r["n_water_cluster"]:
            outer = ", ".join(f"{d:.3f} Å" for d, _, _ in r["second_shell"])
            print(f"   ** {r['n_water_cluster'] - r['n_water_shell']} water(s) expelled to "
                  f"{outer} **")
        else:
            print()

    # ── 3c. denticity summary and x ──────────────────────────────────────────
    print("\n\n" + "=" * 118)
    print("### 3c. DENTICITY TABLE AND x, THE NUMBER OF WATERS DISPLACED")
    print("=" * 118)
    print(f"{'metal':<6} {'state':<6} {'M–O gall #1':>12} {'M–O gall #2':>12} "
          f"{'denticity':>12} {'CN':>4} {'H2O 1st':>8} {'x_stoich':>9} "
          f"{'Δn':>4} {'x_shell':>8}")
    print("-" * 118)
    rows = []
    for met, aq in (("Pb", "pb_aquo6"), ("Cu", "cu_aquo6"), ("Zn", "zn_aquo6")):
        n_w_aq = res[aq]["cn"]
        for st in ("P0", "P1", "P2"):
            n = f"{met.lower()}_{st}_cplx"
            r = res[n]
            g1, g2 = r["galloyl"][0][1], r["galloyl"][1][1]
            # x_stoich is fixed by the composition of the clusters that were
            # actually computed: 6 waters in the reactant, 4 in the product.
            x_stoich = res[aq]["n_water_cluster"] - r["n_water_cluster"]
            dn = x_stoich - 1
            # x_shell is the MEASURED change in first-shell water count.
            x_shell = n_w_aq - r["n_water_shell"]
            print(f"{met:<6} {st:<6} {g1:12.3f} {g2:12.3f} {r['denticity']:>12} "
                  f"{r['cn']:4d} {r['n_water_shell']:8d} {x_stoich:9d} "
                  f"{dn:+4d} {x_shell:8d}")
            rows.append((met, st, r))
    print("-" * 118)
    print("x_stoich = waters released in the balanced equation AS COMPUTED, from the cluster")
    print("           compositions: [M(H2O)6]2+ (6 waters) -> [M(L)(H2O)4]q (4 waters).")
    print("           It is 2 for all nine, and Δn = +1 for all nine, because those are the")
    print("           only species that exist as completed jobs. No [M(L)(H2O)5]q was computed.")
    print("x_shell  = MEASURED change in the number of waters inside the first-shell cutoff,")
    print("           reactant aquo ion -> product complex. This is the chemical quantity;")
    print("           it does NOT alter the atom balance or the standard-state term.")

    # ── 3d. cutoff sensitivity ───────────────────────────────────────────────
    print("\n\n" + "=" * 118)
    print("### 3d. CUTOFF SENSITIVITY — element-specific (Pb 3.20) vs uniform 2.80 Å")
    print("=" * 118)
    print(f"{'species':<12} {'closest galloyl':>16} {'2nd galloyl':>13} "
          f"{'verdict @ element':>18} {'verdict @ 2.80':>16}  {'changes?':>9}")
    print("-" * 118)
    changed = []
    for n in COMPLEXES:
        r = res[n]
        g1, g2 = r["galloyl"][0][1], r["galloyl"][1][1]
        diff = r["denticity"] != r["denticity_uniform"]
        if diff:
            changed.append(n)
        print(f"{n:<12} {g1:16.3f} {g2:13.3f} {r['denticity']:>18} "
              f"{r['denticity_uniform']:>16}  {'YES' if diff else 'no':>9}")
    print("-" * 118)
    if changed:
        for n in changed:
            r = res[n]
            print(f"  ** {n}: closest galloyl contact is {r['galloyl'][0][1]:.3f} Å, which "
                  f"straddles the two cutoffs.")
            print(f"     At the element-specific Pb cutoff of 3.20 Å the verdict is "
                  f"{r['denticity']}; at a uniform 2.80 Å it would be "
                  f"{r['denticity_uniform']}.")
            print("     The element-specific cutoff is the one used, because it is the one the "
                  "GFN2-xTB")
            print("     pre-screen used, and §3.7 requires the two to be directly comparable.")
    else:
        print("  No verdict changes between the two cutoffs.")

    # ── 3e. comparison validity ──────────────────────────────────────────────
    print("\n\n" + "=" * 118)
    print("### 3e. WHICH CROSS-METAL COMPARISONS ARE DENTICITY-MATCHED")
    print("=" * 118)
    print(f"{'state':<6} {'Pb':>13} {'Cu':>13} {'Zn':>13}   "
          f"{'Pb–Cu':>12} {'Pb–Zn':>12} {'Cu–Zn':>12}")
    print("-" * 118)
    validity: dict[tuple[str, str], bool] = {}
    for st in ("P0", "P1", "P2"):
        d = {m: res[f"{m.lower()}_{st}_cplx"]["denticity"] for m in ("Pb", "Cu", "Zn")}
        pairs = {}
        for a, b in (("Pb", "Cu"), ("Pb", "Zn"), ("Cu", "Zn")):
            ok = d[a] == d[b]
            pairs[(a, b)] = ok
            validity[(st, f"{a}-{b}")] = ok
        print(f"{st:<6} {d['Pb']:>13} {d['Cu']:>13} {d['Zn']:>13}   "
              f"{'MATCHED' if pairs[('Pb','Cu')] else 'mismatched':>12} "
              f"{'MATCHED' if pairs[('Pb','Zn')] else 'mismatched':>12} "
              f"{'MATCHED' if pairs[('Cu','Zn')] else 'mismatched':>12}")
    print("-" * 118)
    print("MATCHED    — like-for-like; the two reactions differ only in the metal. Quotable.")
    print("mismatched — the ligand binds through a different number of donors on the two")
    print("             metals. The atom balance and Δn are still identical, so ΔG_ss and the")
    print("             water terms still cancel exactly; what differs is the product's")
    print("             first-shell coordination number. The comparison must carry a stated")
    print("             caveat in the table itself, not only in a footnote.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
