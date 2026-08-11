<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# 03 — DECISION LOG

Dated record of every judgement call, with rationale. Decisions recorded here are binding on the
report; where a decision changes, the old entry is struck through rather than deleted, so the
reasoning trail survives.

---

## 2026-08-11 — Phase 4 interview: ANSWERED (partial)

25 questions, grouped, ordered by consequence. Answer in this file or in session; either way the
answers and their rationale are recorded here before Phase 5 proceeds.

**Status: Q1–Q7, Q9, Q10, Q19, Q20, Q22, Q24, Q25 ANSWERED 2026-08-11 22:10 IST. Phase 5 onward
unblocked. Q8, Q11–Q18, Q21, Q23 OPEN — carried as `\TODOPAL` markers in the build.**

> **FOLLOW-UP REQUIRED, disqualification-adjacent — see Q4 below.** The answer "yes, declared
> already" establishes a **prior submission exists**. The Stage-1 outline (`ST Y Chem.pdf`)
> contains no such declaration, so the declaration was made elsewhere. Before the report is
> submitted the Acknowledgement must state, verbatim: **what** was submitted, **to which**
> competition/fair/journal, **when**, **how the present report differs**, and confirmation that the
> submission was **past and not concurrent** (concurrent submission means the report is not
> accepted at all). Carried as `\TODOPAL` in `acknowledgement.tex`.

### Context Palaash needs before answering

Two findings from the Phase 3 audit are not questions but must be known:

1. **PbSO₄ supersaturation.** The competitor salts are sulfates (CuSO₄·5H₂O, ZnSO₄·7H₂O) and the
   lead salt is a nitrate. In both ternary compositions the solution is supersaturated with respect
   to anglesite, PbSO₄, at a saturation index of about **+1.0** (activity-corrected). Every sample
   is filtered at 0.45 µm, so any precipitate would be counted as sorption. See audit **B10.1**.
2. **Molar-basis inversion.** Converting the capacities to mmol g⁻¹ gives Pb 0.194, Cu 0.399,
   Zn 0.258 — the ordering **inverts** to Cu > Zn > Pb, and the same inversion appears in the
   ternary uptake. The selectivity factors α **survive intact** because α is a ratio of distribution
   coefficients and is invariant to the mass-or-molar basis. The capacity-ordering claim does not
   survive and must be recast. See audit **B10.2**.

### A. The two answers that can change what the report claims

| # | Question | Answer | Rationale |
|---|---|---|---|
| 1 | **Ternary composition: equal-mass or truly equimolar?** (audit B3) | **(a) EQUAL-MASS — 50/50/50 mg L⁻¹ as written in protocol §8.4.** | The protocol's "Equimolar" heading (§8.4, §6) is a **naming error**, corrected to "equal-mass ternary" everywhere in protocol v2 and never repeated in the report. **The molar-deficit argument stands**: Pb at 0.2413 mM against Cu 0.7868 mM (3.26×) and Zn 0.7648 mM (3.17×), 6.4:1 combined. **The outline's abstract is correct as published and needs no amendment.** Table 2.3 carries mg L⁻¹ and mmol L⁻¹ side by side. Amendment A-09 CLOSED. |
| 2 | **Was a sorbent-free ternary blank run? Was any turbidity or white precipitate seen?** (B10.1) | **(b) No sorbent-free ternary blank was run. Solutions were visibly clear and this was noted at the time.** | Attack **A22** becomes **ACCEPTED RISK WITH MITIGATION**, not armour. The report will: (i) publish the computed saturation index (SI ≈ +1.0 at 50/50/50, ≈ +1.3 at 25/100/100) in Appendix G rather than omit it; (ii) report the contemporaneous visual observation that the solutions remained clear, as supporting evidence — **the laboratory note recording this must be supplied for Appendix H**; (iii) state in §5.3 that a sorbent-free ternary blank was not run and that precipitation cannot be excluded by measurement, only by calculation and observation; (iv) name Cu(NO₃)₂ / Zn(NO₃)₂ as the correct design in §5.4 Future work. **Publishing SI = +1.0 and then explaining it is a far stronger position than staying silent and being found out.** |
| 3 | **Promote the 25/100/100 minority-target run to the headline competitive result?** (B3) | **(a) YES — the 25/100/100 minority-target run leads §4.4 and Fig 4.7.** | Pb at a 4:1 mass and ~13:1 per-metal molar disadvantage (25.7:1 against the combined competitor pool) — four times more adverse than the equal-mass run. Leading with the most adverse condition answers "did you load the deck?" before it is asked. The 50/50/50 run becomes the supporting condition in the same figure. |

### B. Compliance and disqualification exposure

| # | Question | Answer | Rationale |
|---|---|---|---|
| 4 | **Has any part of this work been submitted to any other competition, fair, exhibition or journal, ever?** (A20) | **Yes — a prior submission exists and has been declared.** | **FOLLOW-UP REQUIRED.** Specifics needed for the Acknowledgement: what, where, when, how the present report differs, and confirmation it was past rather than concurrent. Undeclared prior submission is a disqualification trigger; concurrent submission means the report is not accepted. Carried as `\TODOPAL` in `acknowledgement.tex` and as attack **A20**, status **IN PROGRESS**. |
| 5 | **Who supplied or prepared the ossein?** (B10.6 / A24) | **(a) Purchased commercially from Nizona Marine Products Pvt. Ltd.** | **No third-party-execution exposure** (rule 2.3) — buying a starting material is not research completed on the author's behalf. **No commercial-interaction exposure** either; the prohibition covers profit-making training and education institutions, not suppliers. Consequences: §2.1 Materials names the supplier; **§2.2 is retitled "Source and conditioning of the ossein"** and does not describe a demineralisation; **Fig 2.1 is redefined** as supplied ossein → sized 0.50–1.00 mm fraction → TA-OSS (the raw-scale panel is dropped); **novelty claim 1 is reworded** — the material is waste-derived but the waste stream was not processed by the author, and the claim must say so. Amendment A-14 confirmed. Attack **A24** → armourable. |
| 6 | **Has Ms Menon's written AI approval gone out? Has the principal's signature request gone out?** | **Yes — both have gone out.** | Ms Menon's written AI approval satisfies Commitments item 5 and assertion **C-020**; the principal's signature request removes the longest-lead-time risk in the project. **Both pieces of correspondence must be filed in `admin/correspondence/` as dated PDFs** — they are the evidence, not the memory of having sent them. |
| 7 | **Has any paid or commercial service been engaged at any stage?** | **No commercial or profit-making training/education service was engaged at any stage.** | Commercial-interaction declaration (**C-024**) can be written affirmatively. |

### C. The thermodynamics dataset

| # | Question | Answer | Rationale |
|---|---|---|---|
| 8 | **Which temperatures, how controlled, measured or setpoint?** (B1) | **OPEN** | Blocks Fig 4.8, Table 4.6 and Finding 3. The temperature values themselves are the x-axis of the van 't Hoff plot — nothing in §4.5 can be built without them. `\TODOPAL`. |
| 9 | **Which metals, and what concentration structure at each temperature?** (B1) | **(a) Full isotherm at each temperature.** | K comes from the fitted Langmuir K_L rather than a single-point K_d — the stronger of the two routes, and it lets ΔH° carry a regression uncertainty. **Which metal(s) is still open (Q8/Q9 partial):** Pb only, or Pb + Cu + Zn? All three at matched temperatures would let §4.7.4 compare desolvation penalties experimentally across the series. Carried as `\TODOPAL`. |
| 10 | **Replicates, and was it the same sorbent batch?** (B1 / B10.14) | **n = 3, same sorbent batch.** | No batch-to-batch loading confounder in the van 't Hoff analysis. n = 3 supports an error bar on ΔH° and ΔS°. |

### D. What actually happened at the bench — **STILL OPEN**

Not answered in the 2026-08-11 session. Every row below is carried as a `\TODOPAL` marker in the
build. **Q11 is the most valuable of the group**: Fig 4.17 (failed conditions) and §2.3.3
(conditions screened and rejected) currently have no source, and the Bible is explicit that a report
with no reported failures reads as either lucky or synthetic (Observation 3, anti-pattern 10).

| # | Question | Answer | Rationale |
|---|---|---|---|
| 11 | **Open question: which steps did not go as written, and what actually happened?** (B10.17 / A29) | | |
| 12 | **Functionalisation bath — deviations?** | | |
| 13 | **Washing endpoint — visual or UV-Vis?** (B10.11) | | |
| 14 | **Sieved fraction actually obtained, and yield?** | | |
| 15 | **Bed packing — measured bed height, V_bed, ρ_b, H:D?** | | |
| 16 | **Did Column B run at all?** | | |
| 17 | **Were cycles 2 and 3 terminated early at C/C₀ ≈ 0.30?** | | |
| 18 | **Was any run repeated or discarded?** | | |

### E. Data holdings, replicates and analytical quality

| # | Question | Answer | Rationale |
|---|---|---|---|
| 19 | **Which datasets exist right now versus which are still to be produced?** | **All datasets exist**, except the XPS and SEM-EDX numeric data — see Q25. | The data request is therefore a **transfer specification**, not a work list: the task is getting existing files into the schemas of `data/provided/templates/` rather than generating new data. |
| 20 | **What n was actually run at each isotherm and kinetic point?** (B10.5) | **n = 3 at the 40 ppm point; n = 2 everywhere else.** | **Better than the protocol specified** — §8.2 required n = 3 at one point only and was silent elsewhere. n ≥ 2 throughout means **measurement error bars are available on every isotherm and kinetic point**, closing attack **A09** properly rather than falling back on regression confidence intervals. **DISCREPANCY TO RESOLVE:** protocol §8.2 lists the Pb isotherm as 10/25/50/100/200/300 ppm with n = 3 at **50** ppm; the answer says **40** ppm. Either the concentration series differs from the protocol or this is a slip. The CSV templates are written to accept the actual nominal concentrations rather than the protocol's, so this does not block ingestion — but the real series must be confirmed. Carried as `\TODOPAL`. |
| 21 | **AAS calibration: standards, wavelengths, fit form, R² per metal per batch?** (B10.4 / A25) | **OPEN** | Attack A25. Zn at 213.9 nm with a 50 ppm top standard sits far above the typical linear range, and Zn concentrations propagate into α(Pb/Zn). Needed for Appendix C and Table 2.2. `\TODOPAL`. |
| 22 | **Was laboratory temperature recorded at all?** (B10.10) | **Laboratory held at 25 °C. Experiments run in July 2026; the protocol was written in June 2026.** | The protocol PDF's own creation date (8 June 2026) is consistent. The report states "experiments were carried out in July 2026 in a laboratory maintained at 25 °C". **Open:** whether 25 °C was logged or is the air-conditioning setpoint. If logged, the range is reported; if not, the report says "maintained at 25 °C" without implying a measured mean, and it goes in §5.3. Do **not** write "25.0 °C". |
| 23 | **Which quantity is 80.1% — batch q_e retention or column BV₁₀ retention? What was the cycle-1 denominator?** (C14 / B10.7) | **OPEN** | Two different quantities are currently conflated. Default applied unless corrected: cycle 1 = the **first single-metal re-adsorption** after the initial desorption (amendment A-15). `\TODOPAL`. |

### F. Instruments, facilities and provenance

| # | Question | Answer | Rationale |
|---|---|---|---|
| 24 | **Who operated the FTIR, SEM-EDX, AAS and XPS, at which facility, on what dates?** (A17 / C-022) | **Palaash Gang operated every instrument himself — FTIR, SEM-EDX, AAS and XPS.** | Strong for authenticity and for criterion C4. **FOLLOW-UP:** the Acknowledgement must still name the **facility** for each technique even where the author operated the instrument, and Q25 indicates a laboratory is holding the XPS/SEM-EDX data — so that facility, and any supervision received there, must be named. Assertion **C-022** requires facility-level disclosure, not only operator-level. Carried as `\TODOPAL`. |
| 25 | **Have XPS and SEM-EDX measurements actually been made, or are they still to acquire?** (B6) | **XPS and SEM-EDX have been run. Images will be supplied. The numeric data has not yet been released by the laboratory.** | **Both datasets are carried as `\NEEDSDATA` placeholders throughout the build** — Fig 4.2, Fig 4.18, Table 4.13, and the §4.1 text that depends on them. No XPS binding energy and no EDX composition is written until the files arrive. Images, once supplied, populate the SEM panels of Fig 4.2 independently of the numeric data. **This is the largest single block of outstanding evidence in the project and it is outside Palaash's control — chase the laboratory today.** |

---

## Decisions already taken by the auditor (not requiring Palaash's ruling)

Recorded so they can be reversed on request.

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-11 | **All isotherm and kinetic fitting is non-linear regression.** Linearised forms of Lab Protocol §11 superseded. | Linearisation distorts the error structure (Tran et al. 2017, already cited in the outline). Attack A08, Bible anti-pattern 4. Amendment A-02. |
| 2026-08-11 | **TGA and BET formally DESIGNED OUT** with a stated reason, replaced by a six-line evidence set. | Instruments unavailable. A missing figure that is explained is a limitation; one silently absent is a hole. Amendment A-01. |
| 2026-08-11 | **XPS promoted to a full characterisation subsection** with a new figure and table. | Pb 4f is the strongest direct evidence of Pb–O coordination and oxidation state, and the instrument is available. Amendment A-03. |
| 2026-08-11 | **Quantified leaching test made mandatory** (was optional). | With TGA gone, it is the only evidence that distinguishes grafted from adsorbed tannin. Attack A10. Amendment A-04. |
| 2026-08-11 | **LOD, LOQ and spike recovery added**, with the IUPAC 3.3σ/10σ convention named. | Underwrites every reported concentration; values below LOQ must not be silently fitted. Amendment A-05. |
| 2026-08-11 | **Computed speciation with saturation indices added.** | Attack A07; costs no bench time; became urgent once B10.1 was found. Amendment A-06. |
| 2026-08-11 | **The outline's numbers are claims, not inputs.** They live in audit Table C and nowhere else; they do not seed `CANONICAL_NUMBERS.yaml` and do not influence the computational protocol. | Correctness beats consistency with the outline. |
| 2026-08-11 | **The outline's ΔG°_bind values (−145.2 / −110.4 / −85.6 kJ mol⁻¹) and f_orb = 0.38 are not carried forward.** | No stated reference state (Attack A04); the decomposition scheme is not yet chosen (A01, A13). Nothing has been computed. |
| 2026-08-11 | **Attribution suppression and the commit-msg hook installed in Phase 1** rather than Phase 10. | The absolute attribution rule applies to *every* commit, including the first. |
| 2026-08-11 | **LICENSE is split: MIT for code, all rights reserved for research content.** | Not specified in the brief. A competition submission under assessment should not be openly licensed; the tooling reasonably can be. **Reversible on request.** |
| 2026-08-11 | **The three source documents remain at the repository root under their original filenames**, untouched. | They are Palaash's files; renaming or moving them silently would be a surprise. Referenced by path from `README.md`. |
