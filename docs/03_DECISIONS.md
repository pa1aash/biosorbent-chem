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

---

## 2026-08-13 — Computational arm: cluster model, structures and reaction definitions

Session S02. All structure preparation done locally in the `biosorb` environment; ORCA was still
transferring to the compute box, so nothing was submitted and no DFT input file was written.

### Decisions taken by the auditor (reversible on request)

| Date | Decision | Rationale |
|---|---|---|
| 2026-08-13 | **The full protocol species set was built — 17 structures, not the 6 originally scoped for the session.** | `DFT_PROTOCOL.md` §1.3 fixes **three** protonation states, not one, and §2 requires **both** Pb aquo coordination numbers. Building only six would have meant choosing a protonation state by default, which §1.3 exists to prevent. The 17 built match the §8 job inventory exactly. |
| 2026-08-13 | **Metal coordination spheres built as ideal, undistorted polyhedra. No hemidirected distortion imposed on any Pb starting geometry.** | Hemidirection is a quantity this work *measures* (§5, attack A14). Building it into the input would beg the question the calculation exists to answer. The single exception is a Jahn–Teller axial elongation on Cu(II), because an undistorted octahedron is a saddle point for d⁹. |
| 2026-08-13 | **GFN2-xTB pre-optimisation performed with the ALPB water model rather than in gas phase.** | §3.3 fixes solution-phase geometries throughout. Gas-phase relaxation of a dianionic ligand or a bare dication produces structures that do not exist in water. |
| 2026-08-13 | **Charge and multiplicity written into every `.xyz` header as machine-readable `key=value` fields**, not only into a separate table. | Attack A02. The ORCA input generator reads them off the structure file and can never infer them. All six Cu species carry `mult=2 uhf=1 uks=true`. |
| 2026-08-13 | **CREST replaced by systematic torsion enumeration plus seeded water-orientation sampling plus unpruned distance-geometry embedding.** | CREST 3.0.2 is non-functional on this machine — see below. The replacement is documented, reproducible and verified, and it is stronger than CREST for this system in one respect: it samples coordinated-water orientation, which has no rotatable covalent torsion and which CREST's torsion-driven metadynamics does not target. |
| 2026-08-13 | **CREST's reference-topology check disabled (`--noreftopo`) and replaced by an explicit per-structure connectivity and first-shell coordination check.** | CREST's check fired on every species including the already-optimised free ligand, flagging all atoms; direct comparison showed 21 bonds before and after with no difference. Disabling a safety check is only defensible if something replaces it, so a stricter check was written. |
| 2026-08-13 | **The P1 deprotonation site set to the 4-OH as a stated assumption, not as a screened result.** | The screen ran, but cannot discriminate: the conformational effect (16.96 kJ mol⁻¹) is five times the isomer gap (3.30 kJ mol⁻¹). Recorded honestly rather than presented as settled. Carried as **D-03**. |
| 2026-08-13 | **No ORCA input file written, and no functional, basis set or ECP choice made beyond what `DFT_PROTOCOL.md` §3 already fixes.** | Per the session brief. The protocol's choices are confirmed against the compute box before any input is generated. |

### Findings requiring Palaash's ruling

| Ref | Finding |
|---|---|
| **D-01** | **`DFT_PROTOCOL.md` contradicts itself on the Pb coordination number.** §2 adopts the lower-free-energy Pb aquo ion as the exchange reference; §3.5 states Δn = +1, which requires a six-coordinate reactant and two released waters. If [Pb(H₂O)₈]²⁺ is lower, x = 4 for Pb against x = 2 for Cu and Zn, and ΔΔG stops being isodesmic. **This blocks submission of every exchange job.** Three options and a recommendation in `dft/REACTIONS.md` §3.1. |
| **D-02** | At GFN2-xTB level the neutral P0 ligand relaxes to **monodentate** coordination on Cu(II) (second O at 3.24 Å) while Pb and Zn stay bidentate. If this survives DFT, the P0 comparison is not stoichiometrically matched. |
| **D-03** | The P1 deprotonation site is not settled — see above. |
| **D-04** | `DFT_PROTOCOL.md` §1.3 asserts gallic acid pK_a ≈ 8.5 **with no citation**, and that value motivates the entire three-state design. Per the reference rule it must be sourced or removed. |

### Repository finding

| Ref | Finding |
|---|---|
| — | **`.gitignore` line 25 ignores `*.out` globally** (a LaTeX rule). The block at lines 48–58 is written on the assumption that ORCA `.out` files are kept — its own comment says "Keep .out, .xyz, .hess and property files" — but the global rule overrides it, so **every ORCA output file would be silently untracked**. Since the report requires every quoted energy to be traceable to a file in `dft/outputs/`, this must be fixed with a negation rule before the first production run. Not fixed in this session because it touches build behaviour outside the session's scope. |

---

## 2026-08-13 — Computational arm: four rulings applied (D-01 to D-04)

Session S03. Documentation, decision-recording and repository hygiene only. No structures built, no
ORCA input written, no calculation run. All four rulings below were **decided by Palaash** and are
recorded here so they are never re-litigated under deadline pressure.

### D-01 — Pb coordination number: **RULED, n = 6. CLOSED.**

**Decision.** Lead(II) uses **CN = 6**, matching Cu(II) and Zn(II). **[Pb(H₂O)₆]²⁺ is the reference
state for the headline ΔG_exchange comparison.** The earlier §2 provision — adopt whichever Pb aquo
ion is lower in free energy — is **withdrawn**; it contradicted §3.5 (Δn = +1) and the contradiction
was live, because the GFN2-xTB screen does favour the eight-coordinate ion.

**Rationale, as ruled.**
1. The GFN2-xTB CN = 8 preference is **gas-phase and semi-empirical**, and is **not treated as
   decisive** for a coordination-number question this subtle.
2. More importantly, **CN = 6 is required for a controlled isodesmic comparison** across all three
   metals — same denticity, same Δn, same reaction class — so that any energy difference found is
   **attributable to the metal** rather than to comparing reactions of different order.
3. Pb's known preference for variable, higher coordination numbers — a direct consequence of its
   stereochemically active 6s² lone pair — **is not being denied**. It is **set aside as a
   controlled-comparison decision and flagged explicitly as a limitation**.

**Consequences applied.** `dft/DFT_PROTOCOL.md` §2.1 states the ruling and §2.2 carries the
limitation paragraph in a form reusable near-verbatim in report §5.3; §8 job inventory relabelled.
`dft/REACTIONS.md` §3.1 records the decision as locked, with all **nine** headline equations
(3 metals × P0/P1/P2) confirmed on `pb_aquo6` / `cu_aquo6` / `zn_aquo6`, **x = 2 uniformly**,
**Δn = +1 uniformly**. **`pb_aquo8` is retained, not discarded** — structure, pre-screen energy and
production job all stand; its `role` is relabelled `alternative` with an explicit `role_note` in the
`.xyz` header and in `xtb_prescreen.csv`, marking it limitations-discussion and §6 validation only.

### D-02 — Cu(II) P0 monodentate collapse: **RULED, do not force geometry; measure post-DFT.**

**Decision.** The DFT starting geometry is **not** constrained to force bidentate coordination.
Constraining it would decide the chemistry rather than measure it — the same principle already
applied to hemidirection in §5.

**Consequences applied.** `dft/DFT_PROTOCOL.md` **§3.7** specifies a mandatory QC checkpoint: the
harvesting script must report **both** M–O(galloyl) distances individually — never averaged, because
averaging is what would hide a monodentate structure — plus a denticity verdict and first-shell donor
count, **for every metal × protonation-state combination**, and **Table 4.7 carries a denticity
column** rather than assuming uniformity. **§3.8** writes out the contingency in full, in advance:
Case A (all bidentate — GFN2 artefact, nothing changes); **Case B** (Cu P0 genuinely monodentate —
reported as a **finding**: Cu(II) cannot maintain the same coordination mode as Pb/Zn at this
protonation state; x = 1 and Δn = 0 for Cu against x = 2 and Δn = +1 for Pb/Zn, so the water terms no
longer cancel; the P0 cross-metal row carries an **explicit caveat in the table itself** and
ΔΔG(Pb−Cu) at P0 is **not** quoted as a like-for-like selectivity figure; the complex is **not**
re-optimised under restraint); Case C (mixed pattern). Tracked as attack **A31**, status OPEN.

### D-03 — P1 deprotonation site: **stated assumption, not a resolved result. Documented, not resolved.**

**Decision.** The site remains at the 4-OH and is **labelled as an assumption** wherever P1 results
appear. Not resolved computationally in this scope.

**Rationale.** The GFN2 site screen gives a 4-OH/3-OH gap of **3.30 kJ mol⁻¹**, which is **five times
smaller** than the **16.96 kJ mol⁻¹** conformational effect found in the same species by the later
conformer search. The screen used one conformer per isomer, so it confounds isomer identity with
conformer choice and cannot discriminate. It establishes only that the 5-OH isomer is the poor one.

**Consequences applied.** The framing already existed verbatim in
`dft/structures/MODEL_JUSTIFICATION.md` §3.1 but was **absent from both documents named in the
handoff**; added to `dft/DFT_PROTOCOL.md` **§1.3.1** and `dft/structures/CONFORMER_SCREEN.md` §3.1.

### D-04 — Gallic acid pK_a: **UNSOURCED ASSERTION WITHDRAWN. Citation outstanding.**

**Decision.** The bare "pK_a ≈ 8.5" is **not retained as though sourced**. It is replaced by a
visible `\TODOPAL` and reads as pending until Palaash supplies or confirms a real citation.

**Consequences applied.** `dft/DFT_PROTOCOL.md` §1.3 now carries a `\TODOPAL` naming the preferred
source (a compound-level NMR study of methyl gallate's *microscopic* phenolic pK_a values — both
compound- and position-specific) and the acceptable fallback (a generic gallic acid phenolic pK_a,
values around 8.7 in standard compilations, **only** if cited to a real verified source **and**
carrying the caveat that methyl gallate lacks the carboxylic acid group present in gallic acid, so
the value may not transfer exactly). The planning comment in `report/sections/03_computational.tex`
is marked **do-not-uncomment**. §1.3 also records that the three-state design **makes the premise
unnecessary** — the pK_a determines only which state is described as expected, and all three are
computed regardless. Tracked as attack **A32**, status OPEN.

### Repository defect fixed

| Date | Fix | Rationale |
|---|---|---|
| 2026-08-13 | **`.gitignore`: LaTeX artefact rules scoped from repo-wide to `report/**`.** | A bare `*.out` (a LaTeX/hyperref rule) also matched **ORCA's primary output files** — the evidence every reported energy must be traceable to — and would have silently untracked the entire computational evidence base. Verified: `git check-ignore` on `dft/outputs/*.out` now prints nothing (tracked), on `report/build/*.out` still matches (ignored), and on `dft/outputs/*_atom*.out` still matches (correctly discarded). An explicit `!dft/outputs/**/*.out` negation was tried and **deliberately removed**: it makes `git check-ignore` report a match for those files, which obscures the very check that verifies the invariant. |

### Process rule added

| Date | Rule | Rationale |
|---|---|---|
| 2026-08-13 | **`CLAUDE.md` §7.1: a session record is never a substitute for the verbatim client export**, and the assistant must never generate, reconstruct or simulate a transcript. | Neither S01 nor S02 has a real export; both directories hold assistant-written records only. Appendix A is assembled from **exports**, not records. Submitting a written account as though it were a chat log would misrepresent evidence to the Organising Committee — a worse finding than a missing file. |

