#!/usr/bin/env python3
"""PHASE 1 -- integrity gate over all seventeen production jobs.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

Nothing downstream of this script may run if any row fails.  The gates are
those fixed in DFT_PROTOCOL.md §3.2 and §3.4 and REACTIONS.md §5.1:

  * normal termination AND the frequency section AND the .hess file AND
    optimiser convergence -- the four-part completion test.  "ORCA TERMINATED
    NORMALLY" alone is not a completion test (S05 defect X-02).
  * ZERO imaginary frequencies.  A structure with an imaginary mode is a saddle
    point, not a minimum, and its energy enters no sum.
  * <S^2> reported for every open-shell Cu species with its deviation from the
    ideal 0.750.
  * lowest real mode reported per species, because modes below the 100 cm-1
    quasi-RRHO reference frequency are where the harmonic entropy is unreliable.

    python dft/analysis/integrity_gate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from orca_parse import HARTREE_KJ, JOBS, OPEN_SHELL, parse_all  # noqa: E402


def main() -> int:
    jobs = parse_all()

    print("=" * 132)
    print("PHASE 1 — INTEGRITY GATE — 17 production jobs")
    print("DFT_PROTOCOL.md §3.2, §3.4 · REACTIONS.md §5.1")
    print("=" * 132)
    hdr = (f"{'job':<13} {'term':>5} {'optconv':>8} {'n_imag':>7} "
           f"{'lowest real':>12} {'<S^2>':>9} {'E_final / Eh':>18} "
           f"{'G_therm / Eh':>13} {'cycles':>7} {'atoms':>6}")
    print(hdr)
    print("-" * 132)

    failures: list[str] = []
    for name in JOBS:
        j = jobs[name]
        s2 = f"{j.s2:.6f}" if j.s2 is not None else "—"
        low = f"{j.lowest_real:9.2f}" if j.lowest_real is not None else "—"
        print(f"{name:<13} {str(j.terminated):>5} {str(j.opt_converged):>8} "
              f"{j.n_imag if j.n_imag is not None else '—':>7} "
              f"{low:>12} {s2:>9} {j.e_final:18.8f} "
              f"{j.g_minus_eel:13.8f} {j.n_cycles:7d} {j.n_atoms:6d}")

        if not j.terminated:
            failures.append(f"{name}: did not terminate normally")
        if not j.opt_converged:
            failures.append(f"{name}: optimiser did not converge")
        if not j.has_freq:
            failures.append(f"{name}: no VIBRATIONAL FREQUENCIES section")
        if not j.has_hess:
            failures.append(f"{name}: no .hess file")
        if j.n_imag is None or j.n_imag > 0:
            failures.append(f"{name}: {j.n_imag} imaginary mode(s) "
                            f"{j.imag_values} — NOT A MINIMUM, EXCLUDED")
        if name in OPEN_SHELL and j.s2 is None:
            failures.append(f"{name}: open-shell species with no <S^2>")

    print("-" * 132)
    print("Lowest real mode is the smallest frequency above 1 cm^-1; the six "
          "translations/rotations print as 0.00 and are not modes.")
    print("G_therm is ORCA's own 'G-E(el)' — the thermal correction to the Gibbs "
          "free energy, quasi-RRHO treated (see §1c below).")

    # ── 1a. spin contamination ───────────────────────────────────────────────
    print("\n" + "=" * 132)
    print("1a. SPIN CONTAMINATION — the four open-shell Cu(II) d9 species "
          "(DFT_PROTOCOL.md §3.2, attack A02)")
    print("=" * 132)
    print(f"{'species':<13} {'charge':>7} {'mult':>5} {'<S^2>':>10} "
          f"{'ideal':>7} {'deviation':>11} {'% deviation':>13}  verdict")
    print("-" * 132)
    for name in [n for n in JOBS if n in OPEN_SHELL]:
        j = jobs[name]
        dev = j.s2 - 0.750
        pct = j.s2_deviation_pct
        verdict = ("clean" if j.s2 < 0.80 else
                   "*** CONTAMINATED — above 0.80 ***")
        print(f"{name:<13} {j.charge:>7} {j.mult:>5} {j.s2:10.6f} "
              f"{0.750:7.3f} {dev:+11.6f} {pct:+12.3f}%  {verdict}")
    mx = max(jobs[n].s2 for n in OPEN_SHELL)
    print("-" * 132)
    print(f"Largest <S^2> across the four Cu species: {mx:.6f}. "
          f"Threshold for flagging: 0.80.")

    # ── 1b. low-frequency modes ──────────────────────────────────────────────
    print("\n" + "=" * 132)
    print("1b. LOW-FREQUENCY MODES — reliability of the harmonic entropy")
    print("=" * 132)
    print(f"{'species':<13} {'n modes':>8} {'lowest real':>12} "
          f"{'modes < 100':>12} {'modes < 50':>11}  {'flag':<8}")
    print("-" * 132)
    n_below_100 = 0
    for name in JOBS:
        j = jobs[name]
        real = j.freqs[j.freqs > 1.0]
        lo100 = int((real < 100.0).sum())
        lo50 = int((real < 50.0).sum())
        flag = "LOW" if j.lowest_real < 100.0 else ""
        if j.lowest_real < 100.0:
            n_below_100 += 1
        print(f"{name:<13} {real.size:8d} {j.lowest_real:12.2f} "
              f"{lo100:12d} {lo50:11d}  {flag:<8}")
    print("-" * 132)
    print(f"Species whose LOWEST real mode falls below 100 cm^-1: "
          f"{n_below_100} of {len(JOBS)}.")

    # ── 1c. what thermal correction ORCA actually reported ───────────────────
    print("\n" + "=" * 132)
    print("1c. WHICH THERMAL CORRECTION THE OUTPUT ACTUALLY REPORTS")
    print("=" * 132)
    print(f"{'species':<13} {'Quasi RRHO':>11} {'ref freq / cm^-1':>17} "
          f"{'cut-off / cm^-1':>16}")
    print("-" * 132)
    for name in JOBS:
        j = jobs[name]
        print(f"{name:<13} {str(j.quasi_rrho):>11} "
              f"{j.qrrho_ref_freq if j.qrrho_ref_freq is not None else '—':>17} "
              f"{j.thermo_cutoff if j.thermo_cutoff is not None else '—':>16}")

    # ── verdict ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 132)
    if failures:
        print("*** INTEGRITY GATE FAILED — DOWNSTREAM ANALYSIS MUST NOT RUN ***")
        for f in failures:
            print("   " + f)
        print("=" * 132)
        return 1
    print("INTEGRITY GATE PASSED — all 17 jobs terminated normally, all "
          "optimisations converged,")
    print("all frequency calculations ran, every .hess is on disk, and NO "
          "species carries an imaginary mode.")
    print("=" * 132)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
