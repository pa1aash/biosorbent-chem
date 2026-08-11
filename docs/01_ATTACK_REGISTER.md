<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# 01 — REFEREE ATTACK REGISTER

The Bible §11 attack surface as a **live issue register**. Every row is an open issue until the
armour exists in the built PDF and the evidence column names the artefact that supplies it.

**Working rule.** For every 🔴 row the answer must be visible in the report *without the referee
having to ask*. Pre-emption is worth more than correctness discovered under interrogation.

**Status values.** `OPEN` · `IN PROGRESS` · `ARMOURED` (text written, evidence exists) ·
`VERIFIED` (armour present in the built PDF and checked against the evidence) · `ACCEPTED RISK`
(cannot be armoured; stated as a limitation, with the statement located).

**Note on the count.** The Bible's table contains **seven** 🔴 rows, not five: attacks 1–5 are the
computational cluster and attacks 19–20 the integrity cluster. All seven are pinned below.

Last reviewed: **11 August 2026**.

---

## 🔴 CRITICAL — pinned

| ID | Attack | Severity | Required armour | Where answered | Status | Evidence |
|---|---|---|---|---|---|---|
| **A01** | "Which EDA/NOCV implementation? ETS-NOCV is an ADF method." If the report says ORCA and ETS-NOCV in the same breath without explanation, credibility collapses. | 🔴 Critical | Name the software, its version, and the exact decomposition scheme. ADF → say so and cite it. ORCA + external analyser → name the route precisely. **Since nothing is computed yet, choose a scheme that can be named honestly, and name it.** | §3.4; Table 3.1 | **OPEN** | — Blocked on the Phase 6 tool survey and the Phase 7 protocol decision. `vendor/README_EDA.md` states the constraint. |
| **A02** | "Was Cu(II) treated as open-shell doublet?" | 🔴 Critical | Charge and multiplicity for **every** species in Table 3.1; Cu(II) explicitly d⁹ doublet; ⟨S²⟩ reported with a comment on spin contamination. | §3.1; §3.2; Table 3.1; Appendix E | **OPEN** | — Specified in `dft/DFT_PROTOCOL.md` (Phase 7); ⟨S²⟩ values come from the calculations. |
| **A03** | "Was a relativistic ECP used for Pb?" A Pb calculation without a relativistic treatment is a fatal, easily spotted flaw. | 🔴 Critical | Name the ECP (def2-ECP / SDD) or the all-electron relativistic treatment (ZORA / DKH), per element. | §3.2; Table 3.1 | **OPEN** | — Decided in `dft/DFT_PROTOCOL.md` (Phase 7). |
| **A04** | "Are these naked-ion binding energies?" Naked-ion binding energies are physically meaningless and a referee will say so. | 🔴 Critical | Write the reaction as **aquo-ligand exchange**, [M(H₂O)ₙ]²⁺ + L → [ML(H₂O)ₙ₋ₓ]²⁺ + xH₂O. Never compute the naked-ion form as the headline quantity. | §3.3; §4.6 | **OPEN** | — Locked into the protocol design in Phase 7. The outline's −145.2 / −110.4 / −85.6 kJ/mol values have no stated reference state and are **not** carried forward. |
| **A05** | "Computed ΔΔG (~35 kJ/mol) is an order of magnitude larger than experimental ΔΔG from α (~3 kJ/mol)." | 🔴 Critical | Confront it in §4.6 **before** the referee does, with the intrinsic-single-site vs ensemble argument: the cluster computes an idealised single-site preference; the measured α reflects site heterogeneity, partial accessibility, competitive occupancy, transport limitation and activity effects. Expect the calculation to reproduce **ordering and mechanism, not magnitude**. | §4.6.3; Table 4.9 | **OPEN** | — Table 4.9 (computed vs experimental ΔΔG with % deviation) is the armour. Cannot be populated until both arms produce numbers. |
| **A19** | "Did AI write this?" | 🔴 Critical | Complete AI declaration (name, version, stages, purposes, timing, frequency) + chat-log appendix + process photographs + failed-experiment reporting + hand-verified references. | Acknowledgement; Appendix A; Figs 2.1, 2.3, 4.17 | **IN PROGRESS** | `logs/ai_use_log.csv` created and logged from session 1. Photographs and failed-condition reporting outstanding. Ms Menon's prior written approval outstanding. |
| **A20** | "Has this been submitted elsewhere?" Undeclared prior submission is a disqualification trigger. Concurrent submission means the report is not accepted at all. | 🔴 Critical | Explicit declaration **either way**, verbatim, in the Acknowledgement. | Acknowledgement | **OPEN** | — Requires Palaash's answer (Phase 4 interview). |

---

## 🟠 HIGH

| ID | Attack | Severity | Required armour | Where answered | Status | Evidence |
|---|---|---|---|---|---|---|
| **A06** | "Is the selectivity a mass-vs-mole artefact?" | 🟠 High | Tabulate the ternary composition in mg/L **and mmol/L** so the molar ratio is a number, not a claim. Discuss explicitly. Ideally hold both a mass-matched and a mole-matched run. | §2.6; Table 2.3; §4.4 | **OPEN** | — **Blocked on the Phase 4 ruling** (audit B3): whether the ternary was equal-mass or truly equimolar determines which argument the report can make. The 25/100/100 minority-target run is the stronger result either way. |
| **A07** | "How do you know Pb didn't precipitate at pH 5?" | 🟠 High | Computed Pb(II) speciation diagram vs pH under the exact ionic conditions, with saturation indices, **plus** the sorbent-free blank. | Fig 2.4; §2.5.1; Appendix G | **OPEN** | — `analysis/src/speciation.py` (Phase 6/9). Sorbent-free control exists in the protocol at pH 6.0 only; audit B9. |
| **A08** | "Were isotherms fitted by linearisation?" | 🟠 High | Non-linear regression throughout; report parameter confidence intervals, R², reduced χ², RMSE and AIC; cite Tran et al. 2017 and state that linearisation was avoided because it distorts the error structure. | §2.5; §4.2; §4.3; Table 4.2 | **IN PROGRESS** | Amendment A-02 recorded. Appendix comparison of linearised vs non-linear fits proposed as a cheap rigour signal (audit B2). |
| **A09** | "Where are the replicates and uncertainties?" | 🟠 High | n stated everywhere; error bars on every plot or an explicit stated reason; SD in every table. | throughout | **OPEN** | — Replicate structure is a required field of every dataset in `docs/DATA_REQUEST.md`. |
| **A10** | "Is the tannic acid grafted or just adsorbed?" | 🟠 High | **Quantified** leaching test: TA-OSS soaked in blank at pH 5 and pH 2, released phenolics against a gallic-acid calibration, reported as a number with n ≥ 3. Combined with the FTIR band evidence. | §2.8; §4.1 | **OPEN** | — The Lab Protocol makes the UV-Vis 276 nm check optional. Amendment A-04 makes it mandatory. Dataset required. |
| **A11** | "How was 5.5 wt% measured?" | 🟠 High | Give the assay and the calibration curve; report ± SD from n ≥ 3. | §2.3.2; §4.1 | **OPEN** | — Gravimetric loading is the primary route (protocol §7.4). Any orthogonal assay strengthens it. The outline's ~5.5 wt% is a **claim to be tested**, not an input. |

---

## 🟡 MEDIUM

| ID | Attack | Severity | Required armour | Where answered | Status | Evidence |
|---|---|---|---|---|---|---|
| **A12** | "Which hydration free-energy scale?" Absolute single-ion values are convention-dependent. | 🟡 Medium | Cite the source for each value and state the convention/scale; prefer **relative** values. | §4.7.4; Table 4.10 | **OPEN** | — Table 4.10 carries source and convention per row. |
| **A13** | "f_orb is scheme-dependent — is the comparison valid?" | 🟡 Medium | Acknowledge scheme-dependence in the text; assert internal comparability across the three metals under identical settings; do not compare across studies. | §3.4; §4.7.1 | **OPEN** | — Definition and caveat written into `dft/DFT_PROTOCOL.md`. |
| **A14** | "Is hemidirection asserted or measured?" | 🟡 Medium | A numerical descriptor reported for **all three** metals: metal displacement from the donor-set centroid and/or the void-hemisphere angle after Shimoni-Livny et al. | §3.5; §4.7.3; Table 4.7; Fig 4.13 | **OPEN** | — `analysis/src/hemidirection.py`, unit-tested against a hand-worked geometry (Phase 7). |
| **A15** | "What about competing hardness ions (Ca²⁺, Mg²⁺, Na⁺)?" | 🟡 Medium | At minimum discuss; ideally one experiment on a synthetic hardness matrix. | §5.3 limitations; §4.8 if run | **OPEN** | — No such experiment in the Lab Protocol. Likely an ACCEPTED RISK stated as a limitation. |
| **A16** | "Only 3 regeneration cycles?" | 🟡 Medium | Acknowledge as a limitation; state the mechanism of the capacity loss (site blocking / tannic-acid leaching / structural collapse) and give **evidence** for the attribution — post-cycle FTIR or leachate analysis. | §4.8; §5.3 | **OPEN** | — The leaching test (A10) doubles as the evidence base for the attribution. |
| **A17** | "Who ran the FTIR / SEM-EDX / AAS / XPS?" | 🟡 Medium | Full disclosure in the Acknowledgement: instrument, facility, operator, per technique. A rules requirement independent of the attack. | Acknowledgement; Table 2.2 | **OPEN** | — Requires Palaash's answer (Phase 4 interview). |
| **A18** | "Where did the DFT compute run and who set it up?" | 🟡 Medium | Declare the hardware, the provider and who performed the setup. | Acknowledgement §compute | **OPEN** | — Rented Hetzner CPU instances; provisioning scripts in `dft/hetzner/` are part of the evidence. |

---

## Register maintenance

- A row moves to `ARMOURED` only when the armour text exists **and** the evidence column names a
  real artefact — a file, a table ID, a figure ID or a declaration paragraph.
- A row moves to `VERIFIED` only after the armour has been read in the **built PDF**.
- A row may be closed as `ACCEPTED RISK` only if the limitation is stated in §5.3 and the location
  is recorded here.
- New attacks discovered during the audit or the build are appended with IDs `A21`, `A22`, …
- Review this register at the end of every session, before `make check`.
