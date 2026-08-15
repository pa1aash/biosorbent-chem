<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# THE COMPOSITION OF G — WHAT EXACTLY IS SUMMED, AND FROM WHICH PRINTED LINE

**Written 2026-08-15 (S07), from real output, after the C-01 identity was re-verified on a charged
metal complex and on an open-shell species.** This document is the auditable specification of
`dft/analysis/thermo.py`. It exists so that a referee — or a future session — can reconstruct every
free energy in the report from the `.out` files without guessing which of ORCA's several printed
energies was used.

Generated and checked by [`verify_c01.py`](verify_c01.py). Re-run it to reproduce every identity
below.

---

## 1. THE QUANTITY USED AS G

For every species *i*, in aqueous solution at 298.15 K:

```
  G_i(aq, 1 mol/L)  =  E_final(i)  +  G_thermal,qRRHO(i)  +  dG_ss(i)
```

| Term | ORCA's printed line | Symbol in REACTIONS.md §5.1 |
|---|---|---|
| `E_final` | **`FINAL SINGLE POINT ENERGY`** — last occurrence in the file | `E_SCF,SMD` **+** `G_CDS` (see §2 — they are already summed) |
| `G_thermal,qRRHO` | **`G-E(el)`** — last occurrence, in the `GIBBS FREE ENERGY` block | `G_thermal,qRRHO` |
| `dG_ss` | not printed by ORCA; computed by `thermo.py` from R, T and the stated concentrations | `dG_standard-state` |

`E_final + G_thermal,qRRHO` is numerically identical to ORCA's own **`Final Gibbs free energy`**
line, verified to 0.0 Eh residual on all seventeen jobs (identity 4 below). The sum is written out
term-by-term anyway, because the report must state what G contains rather than name a line in an
output file.

**The standard-state term is applied at the reaction level, not per species**, since it depends only
on the change in the number of species and on which species are waters. See §4.

---

## 2. WHAT `FINAL SINGLE POINT ENERGY` ALREADY CONTAINS — OPEN ITEM C-01, CLOSED

This was the single most dangerous open question in the computational arm: a double-counted `G_CDS`
would shift every free energy in the report by tens of kJ/mol, silently and in the same direction.

**ORCA 6.1.1 prints the final energy with the SMD non-electrostatic term and the D3(BJ) dispersion
correction ALREADY ADDED.**

```
  FINAL SINGLE POINT ENERGY  =  E(SCF, incl. SMD electrostatics)  +  G_CDS  +  E_D3BJ
```

Worked on `pb_P0_cplx` — **charged (+2), solvated, ECP element, 34 atoms**:

```
  Total energy after final integration    -1183.596340322 Eh    SCF incl. CPCM dielectric
  SMD CDS (Gcds)                             +0.017674342 Eh
  Total Energy after SMD CDS correction   -1183.578665981 Eh    = sum of the two above
  Dispersion correction                      -0.033676744 Eh    D3BJ
  FINAL SINGLE POINT ENERGY               -1183.612342725 Eh    = sum of the two above
```

Worked on `cu_P0_cplx` — **charged (+2), OPEN SHELL doublet (UKS), 34 atoms**:

```
  Total energy after final integration    -2630.947990443 Eh
  SMD CDS (Gcds)                             +0.017677379 Eh
  Total Energy after SMD CDS correction   -2630.930313065 Eh
  Dispersion correction                      -0.033656596 Eh
  FINAL SINGLE POINT ENERGY               -2630.963969660 Eh
```

Both identities close to **below 1e-9 Eh** — the printed precision of the components. **`thermo.py`
must NOT add `G_CDS` again, and must NOT add the dispersion correction again.**

`G_CDS` is **+46.4 kJ/mol** for a complex of this size and **+6.1 kJ/mol** for water; `E_D3BJ` is
**−88.4 kJ/mol** for a complex. Those are the magnitudes that would have been double-counted.

**The identity was verified on all seventeen jobs, not on two.** Charges from −2 to +2, closed shell
and open shell, ECP and all-electron. Full sweep in the `verify_c01.py` output.

---

## 3. WHICH THERMAL CORRECTION THE OUTPUT ACTUALLY REPORTS — AND A CORRECTION TO A PRIOR RULING

**ORCA 6.1.1 applied the quasi-RRHO treatment BY DEFAULT, on every one of the seventeen jobs.** Its
thermochemistry block prints, verbatim:

```
  Quasi RRHO          ...     True
  Cut-Off Frequency   ...     1.00 cm^-1
  ...
  Vibrational entropy computed according to the QRRHO of S. Grimme
  Chem.Eur.J. 2012 18 9955 using a reference frequency of 100.0 cm-1
```

**That is exactly the treatment `DFT_PROTOCOL.md` §3.4 specifies** — Grimme's quasi-RRHO with a
100 cm⁻¹ reference frequency. No `%freq` block was supplied and none was needed; the default already
matched the protocol.

> **This supersedes the S04 ruling** that "the quasi-RRHO treatment is applied in post-processing by
> `thermo.py`" (`03_DECISIONS.md`, 2026-08-13). That ruling was made to avoid ORCA's *raw RRHO*
> entropy being silently double-treated. The premise was wrong: ORCA 6.1.1 does not default to raw
> RRHO. Re-deriving the entropy in `thermo.py` would now either **downgrade** the treatment (if
> naive RRHO were used) or **reproduce ORCA's own arithmetic less reliably** (if qRRHO were
> re-implemented). `thermo.py` therefore consumes ORCA's `G-E(el)` directly. The frequency list is
> still parsed and reported, so the low-mode population is visible rather than assumed.

**The 1.00 cm⁻¹ "Cut-Off Frequency" is a different quantity from the 100 cm⁻¹ qRRHO reference
frequency and must not be confused with it in the report.** The cut-off discards modes below
1 cm⁻¹ from the sum entirely; the reference frequency is the qRRHO interpolation parameter. No
species has a real mode below 1 cm⁻¹, so the cut-off removes nothing.

### 3.1 Why the quasi-RRHO treatment matters here — the low-mode population

**Sixteen of the seventeen species have their lowest real vibrational mode below 100 cm⁻¹.** Only
`water` (lowest mode 1596.16 cm⁻¹) does not. The lowest mode in the set is **14.75 cm⁻¹**
(`pb_aquo8`); `cu_P0_cplx` sits at 28.65 cm⁻¹, as noted in S05.

Every metal complex carries **6–9 real modes below 100 cm⁻¹**, and the eight-coordinate lead aquo
ion carries **nine**, three of them below 50 cm⁻¹. These are the coordinated waters librating on a
near-flat potential — the same flat dihedral plateau that made `pb_P0_cplx` hard to converge (D-07).

A harmonic-oscillator entropy diverges as the frequency goes to zero, so a raw RRHO treatment of a
14.75 cm⁻¹ mode would place an unphysically large entropy on it. **A quasi-RRHO treatment is
therefore not optional for this species set, and it was applied.** Full per-species mode census in
[`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md) §1b.

---

## 4. THE STANDARD-STATE CORRECTION

Recomputed from R, T and the stated concentrations by `thermo.py`, never hard-coded, per
`REACTIONS.md` §5.2.

| Term | Formula | Value at 298.15 K |
|---|---|---|
| Ideal gas, 1 atm → 1 mol L⁻¹ solution, per mole of species | `RT ln(24.46)` | **+7.925 kJ/mol** |
| Water referenced to its pure-liquid standard state, 55.34 mol L⁻¹, per water released | `−RT ln(55.34)` | **−9.949 kJ/mol** |

For a reaction releasing *x* waters with a change of Δn in the number of species:

```
  dG_ss  =  dn * RT ln(24.46)  -  x * RT ln(55.34)
```

**`dG_ss` is NOT constant across the nine reactions**, because Phase 3 measured x = 1 for some
species and x = 2 for others. The value is computed per reaction from the measured x and the Δn that
follows from it. The protocol's stated −12.0 kJ/mol applies only to the x = 2, Δn = +1 case.

`thermo.py` asserts that its recomputed `RT ln(24.46)` and `2 RT ln(55.34)` agree with the
protocol's stated 7.91 and 19.9 kJ/mol to within 0.02 kJ/mol, so a silent divergence between the
code and Table 3.1 cannot survive.

---

## 5. WHAT IS NOT IN G

Stated so that no reader infers a correction that was not applied.

| Not included | Why |
|---|---|
| Basis-set superposition (counterpoise) correction | Computed separately for one representative case per metal, per protocol §3.6; **not run in this session** and not folded into any reported ΔG. |
| Conformational free energy beyond the single lowest conformer | One conformer per species, per `CONFORMER_SCREEN.md`. The spread across the retained window is a stated uncertainty, not a correction. |
| Explicit second solvation shell | Formally cut, protocol §9. |
| Any empirical scaling of frequencies | None applied; ORCA's harmonic frequencies are used unscaled. |
| Spin-orbit coupling on Pb | Scalar-relativistic effects enter through the ECP60MDF parameterisation only. |

---

## 6. THE FOUR IDENTITIES, AND WHERE THEY ARE CHECKED

All four are asserted for all seventeen jobs by `verify_c01.py`, which exits non-zero on any
failure.

| # | Identity | Residual tolerance |
|---|---|---|
| 1 | `E(SCF,SMD) + G_CDS = E(after CDS)` | 1e-8 Eh |
| 2 | `E(after CDS) + E_D3BJ = FINAL SINGLE POINT ENERGY` | 1e-8 Eh |
| 3 | thermochemistry block's `E(el)` = `FINAL SINGLE POINT ENERGY` | 1e-7 Eh |
| 4 | `E(el) + G-E(el)` = `Final Gibbs free energy` | 1e-7 Eh |

Identity 3 is the one that is easy to omit and expensive to get wrong: it establishes that the
thermal correction is being added to **the same electronic energy that was decomposed in identities
1 and 2**, rather than to some earlier optimisation cycle's energy.
