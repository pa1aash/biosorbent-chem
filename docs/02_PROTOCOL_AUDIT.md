<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# 02 — PROTOCOL AUDIT

`Lab Protocol (1) (1).pdf` (8 June 2026) read against the evidence requirements of
`YHSA_Asia_Winning_Report_Bible.md` and against the claims of the Stage-1 outline
(`ST Y Chem.pdf`).

**This document exists to surface problems while there is still time to fix them.** It is
deliberately blunt. Nothing here is a criticism of the work; every item is a thing a referee could
raise, listed so that it is raised here first.

Audit date **11 August 2026**. Auditor's standing: this is a documentary audit of the written
protocol. It cannot know what actually happened at the bench — Phase 4 exists to close that gap.

**Reading order.** Table A is coverage. Table B is defects, and is the part that matters. Table C
is the outline's claims, all of which are unverified. Section D records arithmetic performed during
the audit. Section E lists what must go to Palaash before anything else can proceed.

---

## TABLE A — COVERAGE

Every experiment in the protocol, what it feeds, and whether it is sufficient as designed.

| Protocol § | Experiment | Feeds | Sufficient as designed? |
|---|---|---|---|
| 7.2 | Ossein conditioning: rinse, dry to constant mass, grind, sieve 0.50–1.00 mm | §2.2; Fig 2.1 | **No.** Protocol §4 states the ossein was **supplied demineralised in bulk** and that "no demineralization is performed in this protocol". The Bible's §2.2 requires a full demineralisation protocol with reported yield, and the outline's novelty claim rests on "two waste streams". See **B10.6** — this is a disclosure and novelty issue, not a bench issue. |
| 7.3 | Tannic-acid functionalisation: 18 g TA in 360 mL DI (5% w/v), pH 5.0, 12–16 h, ambient; RAW-OSS control processed identically | §2.3.1; Fig 2.2 | **Partly.** Grafting chemistry is not stated anywhere in the protocol — only the recipe. The report needs the mechanism (oxidative coupling / quinone–amine Michael addition / H-bonding + physisorption) drawn as a scheme, and the honest acknowledgement that the bond type is inferred, not proven. No conditions were screened and rejected (**B10.17**). |
| 7.4 | Washing to clarity; drying; **gravimetric tannin loading**; portioning | §2.3.2; Finding 1; Table 4.3 | **Partly.** Gravimetric loading by mass difference is the weakest of the available assays — it cannot distinguish grafted from entrained tannin, and it is sensitive to residual moisture. Attack A11 asks how the loading was measured. Washing endpoint is subjective; the quantitative UV-Vis endpoint is optional (**B10.11**). |
| 7.5.1 | ATR-FTIR: RAW-OSS, TA-OSS, spent TA-OSS; 4000–400 cm⁻¹, 4 cm⁻¹, ≥32 scans | Fig 4.1; Table 4.1; Finding 1 | **Yes**, as an experiment. Note the "spent" sample comes from the column (§9.8), so it is Pb-only loaded, not ternary-loaded. The report must say which. |
| 7.5.2 | Residual mineral (ash), 550–600 °C, duplicate, RAW and TA | §4.1 (grafting evidence); §2.4 | **Yes.** Becomes load-bearing under **B5**: with TGA unavailable, ash is one of the surviving independent lines. Duplicate (n = 2) is thin for a load-bearing number. |
| 7.5.3 | Point of zero charge, drift method, 9 points × 2 sorbents, 0.01 M NaCl, 24 h | Fig 4.4; §4.1; justifies pH 5.0 | **Yes.** No CO₂ exclusion is specified, which shifts the drift plateau slightly; worth a sentence, not a re-run. |
| 8.1 | pH optimisation, 50 ppm Pb, pH 3/4/5/6, TA and RAW (8 flasks) + **one** sorbent-free control at pH 6.0 | §2.5.1; §4.1 | **No.** The sorbent-free control is run **only at pH 6.0**. There is no no-sorbent blank at the operating pH, which the Bible §2.5 requires to exclude wall adsorption, and which Attack A07 requires to exclude precipitation at the pH actually used. See **B10.3**. |
| 8.2 | Single-metal isotherms: Pb 6 points (n = 3 at 50 ppm only), Cu 4, Zn 4, RAW comparator at 50 ppm | Fig 4.5; Tables 4.2, 4.3 | **No.** Replicates exist at one point out of fourteen. Error bars cannot be drawn on the isotherm figure (Attack A09). Four points is thin for a three-parameter model (Sips), and the Bible §4.2 asks for Sips or Redlich–Peterson. See **B10.5**, **B10.15**. |
| 8.3 | Kinetics: Pb and Cu, 5/15/30/60/120/240 min + 60 min duplicate | Fig 4.6; Table 4.4 | **Partly.** Six timepoints with one duplicate supports pseudo-first-order, pseudo-second-order and Weber–Morris. Elovich (Bible §4.3) is not in the protocol's model list but needs no extra data. Film-vs-pore diffusion discrimination is weak with a single particle-size fraction. |
| 8.4 | Competitive ternary: "equimolar" 50/50/50 mg/L, n = 3, + RAW-OSS control; minority-target 25/100/100 mg/L, n = 3; measured initial aliquots | Fig 4.7; Table 2.3; Table 4.5; **Finding 2** | **No — three separate problems.** (i) The 50/50/50 run is labelled "equimolar" and is not (**B3**). (ii) There is no sorbent-free blank for either ternary (**B10.3**). (iii) The sulfate carried in by the Cu and Zn salts drives the solution **supersaturated with respect to PbSO₄** (**B10.1**). This is the single most serious finding in the audit because it bears directly on Finding 2. |
| 8.5 | Batch regeneration, 3 cycles × n = 3, on spent sorbent from the ternary | Fig 4.16; §4.8 | **No.** The material is **ternary-loaded**, but Stage C re-adsorption is **single-metal Pb**. The retention denominator "qe(cycle 1)" is ambiguous between the original ternary uptake and the first single-metal re-adsorption. As written, R(%) may compare two different quantities. See **B10.7**. |
| 9.1 | Column packing and bed characterisation: bed height, V_bed, ρ_b, H:D | Table 4.11 header; §2.7 | **Yes**, and it is essential. One bed volume must be the **measured** packed-bed volume; every BV figure in the report depends on this number. |
| 9.2 | Pre-conditioning, 5 BV DI at pH 5, downflow 8 BV/h | §2.7 | **Yes.** |
| 9.3 | Column A cycle 1 service run, 100 mg/L Pb, 8 BV/h downflow, adaptive fraction schedule to C/C₀ ≥ 0.90 | Fig 4.14; §4.8 | **Partly.** Sufficient as an experiment. The stated expectation ("of order one hundred bed volumes") is contradicted by the confirmed measurement of ~45 BV — see **B4**. `q_col` by integration requires running to exhaustion; if the run was stopped early, `q_col` is unavailable. |
| 9.4 | In-column regeneration, 3 BV 0.1 M HCl counter-current at 4 BV/h; EF and D(%) | Fig 4.15; §4.8 | **Yes.** Pooling the regenerate is acceptable but loses the elution profile; Fig 4.15 needs 0.5 BV fractions to be a profile rather than a single point. |
| 9.5 | Rinse to outlet pH within ±0.3 of inlet | §2.7 | **Yes.** |
| 9.6 | Cycles 2 and 3, may terminate at C/C₀ ≈ 0.30 | Fig 4.16; §4.8 | **Partly.** BV₁₀ is captured, so retention is measurable. But early termination means cycles 2 and 3 have no `q_col`, and the loading before each regeneration differs from cycle 1 — so the per-cycle EF values are not directly comparable. Must be stated. |
| 9.7 | Column B ternary breakthrough, 50/50/50 mg/L, all three metals, one regeneration | Fig 4.14; §4.8 | **Conditionally.** The protocol itself says this run "may be skipped if material or time is short". Whether it ran at all is a Phase 4 question. Also carries the PbSO₄ issue of **B10.1** into the column feed. |
| 9.8 | End-state characterisation: spent-sorbent FTIR, photographs at packing / mid-breakthrough / post-regeneration | Fig 4.1; Figs 2.3, 4.17 | **Yes**, and the photographs are disproportionately valuable as authenticity evidence (Bible Observation 4). |
| 10 | AAS calibration: five standards (1, 5, 10, 25, 50 ppm) per metal, blank, R² > 0.99, mid-range check standard ×3 per batch, dilution of over-range samples | Appendix C; every number in the report | **No.** A single 1–50 ppm calibration set applied to all three metals is analytically implausible for Zn at 213.9 nm and marginal for Cu at 324.8 nm. No LOD, no LOQ, no spike recovery (**B8**, **B10.4**). |
| 11 | Calculations: Langmuir, Freundlich, PFO, PSO, Weber–Morris, α, K_d, β, D%, R%, loading, ash, ρ_b, EBCT, BV_x, q_col, EF | all analysis | **No.** The isotherm and kinetic forms are given **linearised** (**B2**). Sips / Redlich–Peterson, Elovich, and the column models (Thomas, Yoon–Nelson, Adams–Bohart) are absent (**B10.15**). No mass balance anywhere (**B10.8**). |
| — | **Absent entirely:** temperature series · XPS · SEM-EDX · quantified leaching · speciation · LOD/LOQ/spike recovery · binary systems · hardness-ion matrix · failed-condition screening | §4.5, §4.1, §4.7.4, Appendix G, Appendix C | **B1, B6, B7, B8, B9, B10.12, B10.17** |

---

## TABLE B — GAPS AND DEFECTS

Severity uses the attack-register scale. "Ruling" is what this audit recommends; items marked
**PALAASH** are not the auditor's to decide.

---

### B1 — THERMODYNAMICS: no temperature series exists in the protocol
**Severity 🔴 Critical to §4.5 and Finding 3.**

Protocol §6 fixes temperature at "Ambient (≈ 25 °C)" and no step varies it. A van 't Hoff analysis
is therefore impossible from this protocol, and ΔH° = +15.2 kJ/mol and ΔS° = +136.5 J/(mol·K)
cannot originate in it. Finding 3 — endothermic, entropy-driven, desolvation-controlled — is the
experimental corroboration of the entire computational desolvation argument (Bible §4.7 step 8). If
it falls, the theory arm loses its independent experimental anchor.

Palaash has confirmed the dataset exists separately. **Ruling: it is a REQUIRED dataset in Phase 5.**
The following must be supplied exactly:

| Field | Requirement |
|---|---|
| Temperatures | ≥ 3, preferably 4. Report the **measured** temperature of each run, not the setpoint. State how it was controlled (water bath / incubator / shaker) and the stability (± °C). |
| Metal | Pb(II) at minimum. Cu(II) and Zn(II) at the same temperatures would let the report compare desolvation penalties across the three metals and would materially strengthen §4.7.4 — this is the single highest-value optional addition. |
| Concentrations | The equilibrium constant must be obtained at each temperature. Either **(a)** a full isotherm at each T (≥ 4 concentrations, preferred — gives K from the fitted Langmuir K_L), or **(b)** a single concentration at each T (acceptable — gives K from K_d, but the convention must be declared and the limitation stated). Which of these was done must be recorded. |
| Replicates | n ≥ 2 at every point, n = 3 preferred. Without replicates the van 't Hoff regression has no uncertainty and ΔH° cannot carry an error bar — Attack A09. |
| Other conditions | Identical to the main batch work: pH 5.0, 2 g/L dose, 120 min, 0.45 µm filtration, same sorbent batch. **If a different sorbent batch was used, say so** — batch-to-batch loading variation would confound the analysis. |

**Dimensionless-K convention — this must be declared in the report.** Making K dimensionless is the
standard referee objection to van 't Hoff analyses of sorption, and there is no universally correct
answer. The convention this project will apply, stated in §4.5 and defined in §2.5:

> K° is obtained from the Langmuir affinity constant K_L (L mg⁻¹) converted to L mol⁻¹ by
> multiplying by the molar mass of the sorbate (g mol⁻¹ × 1000 mg g⁻¹), then rendered dimensionless
> by multiplying by the standard-state concentration c° = 1 mol L⁻¹ and by the activity coefficient
> of the sorbate, taken as unity at the ionic strengths used. ΔG° = −RT ln K°; ΔH° and ΔS° from the
> slope and intercept of ln K° against 1/T.

The report will state explicitly that this is one of several conventions in use, that the absolute
ΔG° is convention-dependent, and that **the sign and magnitude of ΔH° — the load-bearing quantity
for the desolvation argument — is convention-independent because it comes from the temperature
dependence, not the absolute value.** Saying this pre-empts the objection.

---

### B2 — NON-LINEAR FITTING: protocol §11 is superseded
**Severity 🟠 High. Attack A08. Bible anti-pattern 4.**

Protocol §11 tabulates the **linearised** forms:

| Model | Linearised form given in §11 |
|---|---|
| Langmuir | Ce/qe = 1/(q_max K_L) + Ce/q_max |
| Freundlich | log qe = log K_F + (1/n) log Ce |
| Pseudo-second-order | t/qt = 1/(k₂ qe²) + t/qe |

**Ruling: superseded in full.** All isotherm and kinetic fitting in this project uses **non-linear
regression** (`lmfit`, Levenberg–Marquardt with a differential-evolution pre-pass where the
parameter surface is awkward), reporting for every model: parameter values with **95% confidence
intervals**, R², **reduced χ²**, **RMSE**, and **AIC** for model discrimination.

The reason, recorded here for the report to state: **linearising transforms the error structure.**
Rearranging the Langmuir equation to Ce/qe places Ce on both axes and weights the high-concentration
points by 1/Ce², systematically distorting q_max and K_L and inflating R². The report will cite
**Tran, H. N.; You, S.-J.; Hosseini-Bandegharaei, A.; Chao, H.-P. Mistakes and Inconsistencies
Regarding Adsorption of Contaminants from Aqueous Solutions: A Critical Review. *Water Res.* **2017**,
*120*, 88–116** — already reference [7] of the outline — and state that linearised transformations
were avoided for this reason.

**Proposed addition (recommended, low cost, high return): Appendix, "Linearised versus non-linear
regression".** A short appendix table fitting the Pb isotherm both ways and showing the resulting
divergence in q_max and K_L, with the R² of the linearised fit appearing *better* while the
parameters are *worse*. This is roughly two hours of work and it does three things at once: it
demonstrates command of the point rather than mere compliance with it, it converts a cited paper
into a reproduced result, and it closes Attack A08 so completely that the referee cannot raise it.
Cheap rigour signals of exactly this kind are what separates a shortlisted report from a scored one.
**Recommended: accept.**

---

### B3 — TERNARY COMPOSITION: "equimolar" is a factual error in the protocol — **PALAASH MUST RULE**
**Severity 🔴 Critical. Attack A06. Determines the wording of the abstract.**

Protocol §8.4 heads the 50/50/50 mg/L run **"Equimolar (n = 3, plus one control)"**. Global
parameter §6 repeats "equimolar ternary" in the replication rule. **The arithmetic contradicts the
label.**

**At 50 mg/L each, using Pb 207.2, Cu 63.55, Zn 65.38 g mol⁻¹:**

| Metal | mg L⁻¹ | mmol L⁻¹ | Molar ratio to Pb |
|---|---|---|---|
| Pb(II) | 50 | **0.2413** | 1.00 |
| Cu(II) | 50 | **0.7868** | **3.26 ×** |
| Zn(II) | 50 | **0.7648** | **3.17 ×** |

That is **equal-MASS**, with Pb at a **3.26-fold molar deficit to Cu and a 3.17-fold molar deficit
to Zn** — and a combined competitor:target molar ratio of **6.4 : 1**. This is precisely what the
outline claims ("a >3-fold molar disadvantage") and it is a **genuine methodological strength**: a
selectivity experiment deliberately designed to disadvantage the target cannot be dismissed as a
concentration artefact. The Bible names it as one of the project's four creative moves (§C3).

**A truly equimolar run at 0.2413 mmol L⁻¹ each would instead be:**

| Metal | mmol L⁻¹ | mg L⁻¹ |
|---|---|---|
| Pb(II) | 0.2413 | 50.0 |
| Cu(II) | 0.2413 | **15.3** |
| Zn(II) | 0.2413 | **15.8** |

Under that composition there is **no molar deficit** and the adverse-ratio argument does not exist.

**The conflict.** Palaash has stated verbally that the run was "truly equimolar". That contradicts
both the protocol's own stated concentrations (50/50/50 mg L⁻¹, §8.4 step 1) and the outline's
published claim of a >3-fold molar disadvantage. Both cannot be true. **This audit does not decide
it.** It goes to Palaash as Phase 4 question 1.

**What each answer costs:**

| Reading | If TRUE, then… | Cost |
|---|---|---|
| **(a) Equal-mass** — 50/50/50 mg L⁻¹ as written | The protocol's "equimolar" heading is a **naming error**, corrected everywhere in protocol v2 and never repeated in the report. The molar-deficit argument **stands** and the outline's abstract is correct as published. | Low. One naming correction, propagated. Table 2.3 makes the molar arithmetic explicit and the objection is closed. |
| **(b) Truly equimolar** — 50 / 15.3 / 15.8 mg L⁻¹ | The **outline's abstract must be amended** ("equal-mass ternary … >3-fold molar disadvantage" is then false). The adverse-ratio argument must rest **entirely** on the 25/100/100 minority-target run. Every derived quantity — removals, α, Table 2.3, Fig 4.7 — was computed against the wrong nominal composition and must be recomputed. | High. An amendment to an accepted outline, plus recomputation. Recoverable, but only if identified now. |

**Independent of the ruling: the minority-target run is the stronger result and should probably
lead.** At 25/100/100 mg L⁻¹:

| Metal | mg L⁻¹ | mmol L⁻¹ | Ratio to Pb |
|---|---|---|---|
| Pb(II) | 25 | 0.1207 | 1.00 |
| Cu(II) | 100 | 1.5736 | **13.0 ×** |
| Zn(II) | 100 | 1.5295 | **12.7 ×** |

A **4:1 mass** and **~13:1 per-metal molar** disadvantage, **25.7 : 1** against the combined
competitor pool. That is four times more adverse than the equal-mass run and it survives either
ruling. **Recommendation: promote the minority-target run to the headline competitive result in
§4.4 and Fig 4.7, with the 50/50/50 run as the supporting condition.** A referee's instinct is to
ask "what if you loaded the deck?" — leading with the most adverse condition answers the question
before it is asked. This is a strictly better rhetorical position and costs nothing but the order
of two panels.

---

### B4 — COLUMN DISCREPANCY: measured performance is ~2.6× below the design basis
**Severity 🟠 High. New attack row A21.**

Protocol §5.4.3 tabulates planning estimates for a 100 mg L⁻¹ feed:

| Feed | q* | BV_sat | **BV₁₀ est.** | **EF (3 BV)** |
|---|---|---|---|---|
| 100 mg L⁻¹ (selected) | ≈ 33 | ≈ 167 | **≈ 117** | **≈ 56 ×** |

The outline reports **~45 BV** to 10% breakthrough and **11–14×** enrichment. Palaash has confirmed
the outline is correct.

**Ruling: the §5.4.3 figures are design-basis planning estimates and are superseded by measurement.**
The protocol itself says so — "They are estimates only; the breakthrough bed volume is a measured
output". Protocol v2 will label the table `[PLANNING ESTIMATE — SUPERSEDED BY MEASUREMENT]` and it
will not appear in the report as a prediction.

**But a ~2.6× shortfall against the design basis needs a physical explanation, because a referee
will do the same arithmetic.** BV_sat ≈ q*·ρ_b/C₀ is a one-line calculation from numbers the report
must publish anyway (q_max from §4.2, ρ_b from the bed characterisation, C₀ from the feed). The
report must get there first. Quantified in Section D.2 below: **at BV₁₀ = 45 with an 8 mL bed, the
bed had taken up ≈ 9 mg g⁻¹, roughly 22% of the batch equilibrium capacity** — well below the 60–90%
dynamic-to-equilibrium rule of thumb the protocol itself quotes.

Candidate explanations, to be argued from the data rather than asserted:
1. **Mass-transfer-zone breadth.** A 9–11 cm bed at EBCT ≈ 7.5 min with 0.50–1.00 mm granules is
   short relative to the MTZ length. If the MTZ is comparable to the bed height, breakthrough begins
   almost immediately and BV₁₀ is a small fraction of BV_sat. **Testable from the data:** the
   breakthrough curve's steepness. A shallow sigmoid confirms a broad MTZ; a sharp one refutes it and
   points elsewhere. This is the leading hypothesis and the curve shape is the evidence.
2. **Intraparticle diffusion limitation.** 0.5–1.0 mm granules are large. The Weber–Morris analysis
   of §4.3 speaks directly to this and links the kinetic and column sections — a genuine
   cross-validation, not a hand-wave.
3. **Actual measured bed volume.** Every BV depends on the measured V_bed. If ρ_b came out at the
   top of the 0.45–0.55 g cm⁻³ range, V_bed is smaller and each BV is a smaller volume.
4. **Channelling / wall effects.** D_c/d_p ≈ 10–20 is at the lower bound of the accepted rule. Visual
   inspection notes at packing and any dye or tracer test are evidence here.
5. **Dynamic vs equilibrium capacity.** The generic explanation, and the weakest on its own. Use it
   only in combination with (1) and (2).

**Corroborating evidence that the measured figures are real and internally consistent:** an
enrichment factor of 11–14× into 3 BV of eluent corresponds to roughly 7–9 mg g⁻¹ desorbed
(Section D.2), which matches the ≈ 9 mg g⁻¹ implied by BV₁₀ = 45. The two independently reported
column numbers agree with each other. The 56× estimate, by contrast, was consistent with the 117 BV
estimate. Both pairs are self-consistent; only one pair is measured.

**Action: added to the attack register as A21.**

---

### B5 — INSTRUMENT COVERAGE: TGA and BET are unavailable
**Severity 🟠 High to §4.1 and Finding 1.**

The Bible's plan assumes TGA (Fig 4.3, §2.4.3, §4.1) and BET/porosimetry (§2.4.4, §4.1). Neither
instrument is available to this project. ICP-MS is likewise unavailable; flame AAS is the analytical
method throughout.

**Ruling: TGA and BET are formally DESIGNED OUT, with a stated reason, not left as holes.** A
missing figure that is explained is a limitation; a missing figure that is silently absent is a
hole. Recorded as amendment **A-01** in `00_SPEC.md`, and Fig 4.3 is marked `DESIGNED-OUT` in the
figure registry.

**Wording for the report (§2.4 and §5.3):** *"Thermogravimetric analysis and nitrogen physisorption
were not available for this study. The evidence for grafting therefore rests on the five independent
lines set out in §4.1, and surface area is not reported. Capacity is reported per unit mass rather
than per unit area throughout, and no claim is made about the specific surface area or pore
structure of either material."*

**Replacement evidence set — what independently survives.** Five lines, of which four are already in
the protocol:

| # | Evidence | Source | What it independently establishes | Strength |
|---|---|---|---|---|
| 1 | **ATR-FTIR band assignment** — new aromatic C=C ~1600–1620 cm⁻¹ and galloyl ester C=O/C–O ~1700–1730 cm⁻¹, with Amide I/II/III preserved | §7.5.1 | Tannic acid is present on the material, and the collagen backbone survived the treatment | Strong for presence; **silent on grafted vs adsorbed** |
| 2 | **Gravimetric tannin loading**, n ≥ 3 with SD | §7.4 | How much was added, in wt% | Moderate; cannot distinguish grafted from entrained |
| 3 | **pH_PZC shift**, TA-OSS below RAW-OSS | §7.5.3 | Acidic (phenolic) surface groups were enriched — a *functional* consequence, not just a spectroscopic one | **Strong**, and independent of FTIR. Under-rated; promote it in §4.1 |
| 4 | **Residual mineral (ash)** | §7.5.2 | The scaffold is demineralised as supplied; the ~1030 cm⁻¹ phosphate band is accounted for | Supporting only |
| 5 | **Quantified leaching test** (new, **B7**) | new | **Grafted versus merely adsorbed** — the one question the other four cannot answer | **Decisive for Attack A10** |
| 6 | **XPS** (new, **B6**) | new | Direct oxidation state and coordination environment of the bound Pb; C 1s / O 1s envelope change on functionalisation | **Strongest single piece of evidence in the set** |

With (5) and (6) added, the evidence set is **stronger** than the Bible's original TGA+BET plan,
because TGA mass loss and BET surface area are both indirect, whereas XPS Pb 4f is a direct
observation of the binding event. **This should be stated as a design choice in §2.4, not
apologised for.**

---

### B6 — XPS AND SEM-EDX: available but entirely unused by the protocol
**Severity 🟠 High — the largest unforced omission in the project.**

Neither technique appears anywhere in the Lab Protocol, yet both instruments are available. The
Bible says XPS Pb 4f "is the single strongest direct evidence of Pb–O coordination and oxidation
state; if you have it, it is worth a full subsection". Not acquiring it would be leaving the best
available evidence on the table.

**Ruling: both are added as new protocol sections in Phase 5.** Amendment **A-03**.

#### B6.1 XPS — exact acquisition specification

**Samples (three, all required):**
1. **RAW-OSS** — the unfunctionalised baseline.
2. **Fresh TA-OSS** — establishes what functionalisation did to the C 1s and O 1s envelopes.
3. **Pb-loaded TA-OSS** — from a single-metal Pb equilibration at pH 5.0, washed with DI to remove
   physisorbed Pb, and dried at 50 °C. **The wash step matters:** unwashed material shows surface
   Pb salt, not coordinated Pb, and a referee will ask. Record the wash volume and number.
   *Strongly recommended fourth sample:* **ternary-loaded TA-OSS**, which would put Pb 4f, Cu 2p and
   Zn 2p on one surface and give a direct surface-composition measurement of the competitive result.

**Scans (per sample):**

| Region | Purpose | Notes |
|---|---|---|
| **Survey**, 0–1200 eV | Elemental inventory; confirms no unexpected contamination | Wide pass energy |
| **Pb 4f** | *The* measurement. Pb 4f₇/₂ position distinguishes Pb(II)–O carboxylate/phenolate coordination (~138.5–139.5 eV) from PbO, Pb(OH)₂, PbCO₃ and metallic Pb | Doublet, 4f₇/₂ / 4f₅/₂, fixed splitting 4.87 eV, area ratio 4:3 constrained |
| **O 1s** | Resolves the lattice/carbonyl vs hydroxyl/phenolic vs adsorbed-water components; the phenolic component should change on Pb binding | Usually 3 components |
| **C 1s** | The charge reference, and the aromatic/carboxyl inventory that changes on grafting | |
| **N 1s** | Collagen amide nitrogen — confirms the protein scaffold survived and tests whether N participates in binding | |
| *(if ternary sample)* **Cu 2p, Zn 2p** | Cu 2p₃/₂ satellite structure confirms Cu(II) rather than Cu(I)/Cu(0) | Cu 2p shake-up satellites are diagnostic |

**Acquisition and processing parameters to record and report:**
- Instrument make and model; X-ray source (**Al Kα, 1486.6 eV**, monochromated or not); spot size;
  base pressure.
- Survey pass energy (typically 100–200 eV) and high-resolution pass energy (typically 20–50 eV);
  step size (survey ~1 eV, high-res ~0.05–0.1 eV); dwell time; number of sweeps.
- **Charge neutralisation** used (flood gun on/off) — insulating organic samples charge badly.
- **Charge referencing: adventitious C 1s set to 284.8 eV.** State this explicitly; binding energies
  are meaningless without it, and 284.8 eV must be named as the value chosen.
- **Peak fitting:** Shirley background; Gaussian–Lorentzian line shape with the GL mixing ratio
  stated; FWHM constrained equal across components within a region; spin–orbit splitting and area
  ratios constrained to theoretical values; the number of components stated and **justified**, not
  chosen to improve the residual.
- **Operator and facility named** — a rules requirement (Attack A17) and a compliance assertion (C-022).

**Beam-damage caution to record:** Pb compounds can reduce under prolonged X-ray exposure. Acquire
Pb 4f early in the sequence and, if time allows, re-acquire at the end to demonstrate the spectrum
is unchanged. One extra scan; it forecloses an entire line of questioning.

#### B6.2 SEM and SEM-EDX — exact acquisition specification

**Samples:** RAW-OSS, fresh TA-OSS, Pb-loaded TA-OSS (same three as XPS), plus spent post-column
TA-OSS if material remains.

**SEM:** at least three magnifications per sample (low ~100×, mid ~1000×, high ~5000×), from the
same region where practical so before/after comparison is meaningful. Record accelerating voltage,
working distance, detector (SE/BSE), and the conductive coating (Au/Pt/C — **coating element
matters**, because a C coating interferes with the EDX carbon signal and an Au coating overlaps the
Pb M lines). **Scale bar burned in by the instrument**, never added afterwards.

**EDX:** elemental maps for C, N, O, **Pb**, plus Ca and P (residual mineral), on the Pb-loaded
sample; point/area spectra with the quantification table if the instrument produces one. Record the
accelerating voltage (Pb L lines need ≥ 15 kV; Pb M lines are accessible lower but overlap S and Mo),
live time, and the count rate.

**The honest caveat, to be stated in §4.1:** EDX on a rough, low-atomic-number, coated biological
material is **semi-quantitative at best**. The report will present EDX as evidence of the *spatial
distribution* of Pb across the surface and as confirmation of its *presence*, and will not quote EDX
weight percentages as a measurement of loading. Saying this pre-empts the objection; quoting EDX
wt% as if it were quantitative invites it.

---

### B7 — LEACHING TEST: currently optional, must be mandatory and quantified
**Severity 🟠 High. Attack A10 — "is the tannic acid grafted or just adsorbed?"**

Protocol §5.1 lists the UV-Vis spectrophotometer as **"(optional)"** and §7.4 makes the 276 nm wash
endpoint conditional — "If a UV-Vis is available, wash until the filtrate absorbance at 276 nm is
below 0.05." That is a wash *endpoint*, not a leaching *test*, and it is optional.

Attack A10 cannot be answered by FTIR (which shows tannin is present, not how it is held), by
gravimetry (which cannot distinguish grafted from entrained), or — with TGA unavailable — by a
shifted decomposition profile. **The leaching test is now the load-bearing evidence for the central
claim that this is a functionalised material rather than a tannin-coated one.**

**Ruling: mandatory, quantified, n ≥ 3.** Amendment **A-04**. Specification:

| Field | Requirement |
|---|---|
| Conditions | **pH 5.0** (the operating pH — the number the report needs) and **pH 2.0** (an aggressive stress condition that brackets the regeneration environment) |
| Matrix | DI water adjusted with HCl/NaOH; no metal present |
| Ratio and time | Same 2 g L⁻¹ dose and 120 min contact as the batch work, so the number is directly comparable to a sorption run. **Additionally a 24 h point** if material allows — 120 min understates equilibrium release |
| Replicates | **n ≥ 3**, mean ± SD |
| Measurement | Released phenolics by UV-Vis against a **gallic-acid calibration curve** (5-point minimum, R² > 0.99, run in the same session). Report the absorbance wavelength used and note that quantifying tannic acid against a gallic-acid standard is a **gallic-acid-equivalent** measurement, not an absolute tannic-acid mass |
| Reporting | **As a number**: mg gallic-acid-equivalent released per g of sorbent, **and** as a percentage of the measured grafted loading. The percentage is what answers the attack |
| Controls | A RAW-OSS blank at each pH, to establish that the signal is not from the collagen scaffold itself |

**Second use of the same measurement:** the pH 2 result is direct evidence for the mechanism of the
capacity loss across regeneration cycles (Attack A16). If leaching at pH 2 is small, the loss is
attributable to site blocking or structural change rather than ligand loss, and that attribution is
then evidenced rather than asserted. **One experiment closes two attacks.**

---

### B8 — ANALYTICAL QC: no LOD, no LOQ, no spike recovery
**Severity 🟠 High. Underwrites every number in the report.**

Protocol §10 specifies five-point calibration, R² > 0.99, blanks, and mid-range check standards at
start/middle/end of each batch with a ±5–10% rejection criterion. That is a reasonable working QC
scheme and it is better than most school-level protocols. It is nonetheless incomplete: there is no
limit of detection, no limit of quantitation, and no spike-recovery test. The Bible §2.5 lists all
three as required.

**Ruling: all three specified and added.** Amendment **A-05**.

**LOD and LOQ.** Method: measure the calibration blank **n ≥ 7** times independently within one
analytical session; take the standard deviation of the blank, σ_blank; then

> **LOD = 3.3 σ_blank / S**  and  **LOQ = 10 σ_blank / S**

where S is the slope of the calibration curve in absorbance per mg L⁻¹. This is the IUPAC/ICH
convention and must be named as such in §2.5.2. Report LOD and LOQ **per metal per instrument
configuration** in mg L⁻¹, and state them in Table 2.2 and Appendix C.

*Acceptable alternative if seven blank replicates were not run:* LOD from the residual standard
deviation of the calibration regression, σ_y/x, in place of σ_blank. **The method used must be
stated**; the two give different numbers and a referee who knows the difference will ask which.

**Consequence to state explicitly:** every reported value below LOQ is reported as "< LOQ" and is
**not** used in a fit or an average. This most likely affects the early column fractions, where
effluent Pb is near zero, and the low-concentration end of the isotherms. Silently fitting
below-LOQ points is a real methodological error and it is invisible unless the LOQ is published.

**Spike recovery.** Spike a real sample matrix — not a standard — at two levels (low, near 2–5× LOQ;
and mid-range) with a known metal addition; n = 3 at each level. Report

> **Recovery (%) = 100 × (C_spiked − C_unspiked) / C_added**

Acceptance: **90–110%**. Run one spike-recovery set per matrix type that behaves differently:
(i) a filtered batch sorption supernatant, (ii) a column effluent fraction, and (iii) a diluted acid
regenerate. The regenerate is the one most likely to fail, because it is a strongly acidic
high-ionic-strength matrix and flame AAS is matrix-sensitive. If it does fail, the fix is matrix-
matched standards or standard addition, and knowing this now is worth far more than discovering it
in the oral defence.

---

### B9 — SPECIATION: no calculation exists
**Severity 🟠 High. Attack A07 — "how do you know Pb didn't precipitate at pH 5?"**

The protocol's only defence is one sorbent-free flask at pH 6.0 (§8.1 step 5). There is no
calculation anywhere, and no blank at the operating pH.

**Ruling: a computed Pb(II) speciation diagram with saturation indices is a required deliverable.**
Amendment **A-06**. It is **computed, not measured**, and can therefore be produced today without
any new bench work — which makes it the cheapest CRITICAL-adjacent armour available to this project.

**Specification for `analysis/src/speciation.py`:**

| Field | Requirement |
|---|---|
| System | Pb(II) in the **exact** ionic conditions of each experiment — not a generic Pb–water diagram |
| Aqueous species | Pb²⁺, PbOH⁺, Pb(OH)₂(aq), Pb(OH)₃⁻, Pb(OH)₄²⁻, Pb₂OH³⁺, Pb₃(OH)₄²⁺ (polynuclear species matter above ~10⁻⁴ M), PbNO₃⁺, Pb(NO₃)₂(aq), **PbSO₄(aq)**, PbCl⁺, PbCl₂(aq) |
| Solids tested | **Pb(OH)₂(s)**, **PbSO₄(s) — anglesite**, PbO, and **Pb₃(CO₃)₂(OH)₂ — hydrocerussite** (relevant if the solutions were open to air; state whether they were) |
| Output | Fractional speciation vs pH 2–10 (Fig 2.4), **plus a saturation-index table** SI = log(IAP/K_sp) for every solid at every experimental condition |
| Conditions covered | pH optimisation series (each pH); single-metal isotherms (each C₀, especially **300 mg L⁻¹** where the risk is greatest); **both ternary compositions**; the 100 mg L⁻¹ column feed |
| Temperature and I | 298.15 K; ionic strength computed from the actual composition; **Davies equation** activity corrections, with the equation named |
| Implementation | `phreeqpython` with a named database (`minteq.v4.dat` preferred) if it installs; otherwise a hand-rolled solver over a stated, cited constant set. **Every equilibrium constant must be cited to a source** — an uncited constant is as bad as an uncited fact |
| Reporting | Fig 2.4 with pH 5.0 marked; the SI table in Appendix G; the constants and their sources tabulated in Appendix G |

**Interpretation rule, agreed in advance so the result is not massaged:** SI < 0 → undersaturated,
no precipitation possible. **0 < SI < 1 → supersaturated but plausibly kinetically inhibited at
these concentrations and timescales; must be reported and defended with the sorbent-free blank.**
SI > 1 → precipitation is a live confounder and the result must be qualified.

**This is not hypothetical. See B10.1 — the ternary runs come out at SI ≈ +1.0 for PbSO₄.**

---

## TABLE B (continued) — B10: FURTHER DIVERGENCES FOUND BY THIS AUDIT

Ten items were specified for investigation. Seventeen more were found. The first two are more
serious than several of B1–B9 and are listed first.

---

### B10.1 — PbSO₄ SUPERSATURATION IN BOTH TERNARY RUNS
**Severity 🔴 Critical. New attack row A22. This is the most serious finding in the audit.**

The stock salts are **Pb(NO₃)₂**, **CuSO₄·5H₂O** and **ZnSO₄·7H₂O** (protocol §7.1). Pb therefore
arrives with nitrate, but **Cu and Zn each bring an equivalent of sulfate**. In a ternary mixture
the lead is exposed to sulfate that is not present in any single-metal run.

**Equal-mass ternary, 50/50/50 mg L⁻¹:**

| Quantity | Value |
|---|---|
| [Pb²⁺] | 2.413 × 10⁻⁴ M |
| [SO₄²⁻] from Cu + Zn | 1.552 × 10⁻³ M |
| Ion product Q = [Pb²⁺][SO₄²⁻] | 3.74 × 10⁻⁷ |
| Ionic strength I | 6.93 × 10⁻³ M |
| Davies activity coefficient γ(2±) | 0.704 |
| Activity product IAP | 1.86 × 10⁻⁷ |
| K_sp(PbSO₄, anglesite) | ≈ 1.8 × 10⁻⁸ |
| **Saturation index SI = log(IAP/K_sp)** | **+1.01** |

**Minority-target ternary, 25/100/100 mg L⁻¹:** [Pb²⁺] = 1.21 × 10⁻⁴ M, [SO₄²⁻] = 3.10 × 10⁻³ M,
Q = 3.74 × 10⁻⁷, **SI ≈ +1.3** before activity correction. Same order.

**Both ternary compositions are supersaturated with respect to anglesite by about one order of
magnitude.** So is the Column B ternary feed, which uses the same composition.

**Why this is dangerous rather than merely interesting.** Every sample is filtered through a
**0.45 µm syringe filter** before AAS (§10.2). **Any PbSO₄ that precipitated would be removed by
that filter and counted as sorption.** The measured "removal" of Pb in the ternary would then be
part uptake and part precipitation, and the higher apparent removal of Pb relative to Cu and Zn —
which is Finding 2, the centrepiece of the experimental arm — would have a trivial alternative
explanation that the report had not excluded. A referee who checks the salt list against the
composition will find this in under five minutes.

**Independent confirmation (added 2026-08-11, Phase 6).** The hand calculation above was repeated
with **PHREEQC** (`phreeqpython`, `phreeqc.dat` database), which applies full ion-pairing speciation
rather than a bare ion product. For the equal-mass ternary at pH 5.0 it returns:

| Phase | SI |
|---|---|
| **Anglesite, PbSO₄** | **+0.86** |
| Pb(OH)₂ | −2.05 |
| ionic strength | 5.8 × 10⁻³ M |

The two independent methods agree to within 0.15 log units — the difference is the ion-pairing
treatment and the K_sp value used. **The finding is robust: the equal-mass ternary is supersaturated
with respect to anglesite by roughly an order of magnitude.** The same calculation also confirms
that **Pb(OH)₂ is strongly undersaturated at pH 5**, which independently closes the classical
hydrolysis form of attack A07 — a useful result to report in its own right.

**Mitigating considerations, stated honestly rather than used as an excuse:**
- SI ≈ +1 is modest. PbSO₄ nucleation from a solution supersaturated by ~10× at sub-millimolar
  concentrations can be slow, and 120 min may be short relative to the induction time.
- The sorbent removes Pb from solution continuously, lowering Q throughout the contact period, so
  the system may pass below saturation early in the run.
- K_sp values for anglesite in the literature span roughly 1.6–2.5 × 10⁻⁸; the SI carries that
  uncertainty. It does not carry enough to change the sign.
- The single-metal Pb isotherms are **unaffected** — no sulfate is present. Only the ternary runs,
  the Column B feed, and any batch-regeneration work derived from ternary-loaded sorbent are exposed.

**Required response, in descending order of value:**
1. **A sorbent-free ternary blank at the operating pH, n ≥ 3, 120 min, filtered and analysed
   identically.** This is one flask per composition, roughly two hours including analysis, and it
   settles the question completely. If Pb recovery in the blank is quantitative, precipitation did
   not occur and the objection is dead. **If any ternary material or time remains, do this first —
   it is the highest-value remaining bench work in the project.**
2. **Compute and publish the saturation index** for both ternary compositions (B9 does this anyway).
   Reporting SI = +1.0 and then showing the blank recovered all the Pb is a far stronger position
   than not mentioning it.
3. **Record any observation of turbidity, cloudiness or a white precipitate** in the ternary flasks
   or on the filter membranes. A note in the laboratory record that the solutions remained clear is
   real evidence. **Phase 4 question.**
4. **If a repeat is ever run**, use Cu(NO₃)₂ and Zn(NO₃)₂ so that all three metals share a
   non-complexing, non-precipitating counter-ion. This is the correct design and should be stated as
   such in §5.4 Future work regardless of what is done now.

**Note this also affects speciation more subtly:** sulfate complexation forms CuSO₄(aq) and
ZnSO₄(aq) (log K ≈ 2.3 and 2.4), reducing the **free-ion** activity of the two competitors while
leaving Pb²⁺ largely uncomplexed in the nitrate matrix. The competition was therefore run at unequal
*free-ion* activity as well as unequal molarity. This cuts **in favour of** the project's argument —
it makes the conditions more adverse for Pb than the nominal molarity suggests — but it must be
computed and stated, not left for the referee to notice.

---

### B10.2 — THE MOLAR-BASIS ORDERING INVERTS
**Severity 🔴 Critical to the narrative. Bible §4.2 warns of exactly this; the arithmetic makes it concrete.**

The Bible instructs: *"Table: q_max Pb 40.11 > Cu 25.38 > Zn 16.86 mg/g — also convert to mmol/g. In
mmol/g the ordering may change or narrow; you must show you know this and address it head-on. Molar
capacity is the chemically meaningful quantity for a site-binding argument."*

It does not narrow. **It inverts completely.**

| Metal | q_max (mg g⁻¹) | M (g mol⁻¹) | **q_max (mmol g⁻¹)** |
|---|---|---|---|
| Pb(II) | 40.11 | 207.2 | **0.194** |
| Cu(II) | 25.38 | 63.55 | **0.399** |
| Zn(II) | 16.86 | 65.38 | **0.258** |

**Mass basis: Pb > Cu > Zn. Molar basis: Cu > Zn > Pb.**

On a per-mole-of-site basis the single-metal data shows the sorbent binding **twice as much copper
as lead**, and the Cu > Zn ordering is exactly the conventional Irving–Williams expectation. The
mass-basis ordering is substantially an artefact of Pb's atomic weight being 3.3× that of Cu.

**The same inversion appears in the ternary.** From the outline's removal percentages:

| Metal | Removal (%) | q_e (mg g⁻¹) | **q_e (mmol g⁻¹)** | K_d (L g⁻¹) |
|---|---|---|---|---|
| Pb(II) | 71.6 | 17.90 | **0.086** | 1.261 |
| Cu(II) | 41.0 | 10.25 | **0.161** | 0.348 |
| Zn(II) | 26.4 | 6.60 | **0.101** | 0.179 |

**In the competitive experiment the sorbent takes up more moles of copper than of lead.** What is
higher for lead is the *fraction of the lead present* that is captured — which is exactly what a
distribution coefficient measures, and exactly what makes the adverse-molar-ratio design meaningful.

**What survives, and what does not.**

| Claim | Status |
|---|---|
| α(Pb/Cu) = 3.63 and α(Pb/Zn) = 7.03 | **Survives intact.** α = K_d,Pb/K_d,M, and K_d = q_e/C_e is **invariant** to whether q and C are expressed in mass or molar units, because the molar mass cancels. **This is a genuinely reassuring result and the report should state it explicitly** — it means the headline selectivity numbers are not a unit artefact. |
| "The sorbent captures a larger fraction of the Pb present than of the Cu or Zn present, at a >3-fold molar deficit" | **Survives.** This is the correct and defensible form of Finding 2. |
| "Single-metal capacities Pb > Cu > Zn invert the Irving–Williams ordering" | **Fails on a molar basis.** Must not be written. On a molar basis the single-metal data is entirely conventional. |
| "The sorbent preferentially captures lead" (unqualified) | **Dangerously ambiguous.** It captures a larger *fraction*, not a larger *quantity*. Every such sentence must be rewritten to name the basis. |
| Comparing the DFT ordering of ΔG_bind to the mg g⁻¹ capacity ordering | **A category error.** ΔG_bind is a per-site molar quantity. Its experimental counterpart is α or K_d — never q_max in mg g⁻¹. §4.6.3 and Table 4.9 must compare against ΔΔG_exp = −RT ln α, as the Bible already specifies. |

**Ruling: this is confronted head-on, in the report, in a dedicated paragraph in §4.2, with Table 4.3
carrying both units side by side.** Handled well it is a rigour point of the highest order — it
demonstrates that the author understands what their own numbers mean, which is precisely what
criterion C4 rewards. Handled badly, or left for a referee to find, it reads as not having
understood the result. **The Bible names this outcome as a possibility; this audit confirms it as
fact. There is no version of this report in which it is not addressed.**

---

### B10.3 — No sorbent-free blank at the operating pH, and none in the ternary
**Severity 🟠 High. Feeds A07 and A22.**

The only sorbent-free control is one flask at pH 6.0 in §8.1. There is none at pH 5.0, none at any
isotherm concentration, and none in either ternary. The Bible §2.5 requires a no-sorbent blank to
exclude wall adsorption; B10.1 makes one indispensable in the ternary.
**Ruling: required. Minimum set — pH 5.0 at 50 and 300 mg L⁻¹ single-metal Pb, and both ternary
compositions.** Combined with B10.1 item 1.

### B10.4 — AAS calibration range is analytically implausible for Zn and marginal for Cu
**Severity 🟠 High. Underwrites every concentration in the report.**

Protocol §10.1 applies the same 1 / 5 / 10 / 25 / 50 mg L⁻¹ standard set to all three metals. Typical
flame AAS linear ranges — to be confirmed against the specification of the actual instrument, which
this audit has not seen — are approximately **Pb 283.3 nm: ~20 mg L⁻¹**, **Cu 324.8 nm: ~5 mg L⁻¹**,
**Zn 213.9 nm: ~1 mg L⁻¹**. A 50 mg L⁻¹ Zn standard at 213.9 nm sits roughly fifty times above the
linear range and would roll over badly; the curve could still return R² > 0.99 against a quadratic
while being inaccurate in the middle.

**This matters because Zn concentrations propagate into α(Pb/Zn) = 7.03, one of the two headline
selectivity numbers.**

**Ruling: Phase 4 question.** What were the actual standard concentrations, the fit form (linear or
quadratic), and the R² per metal per batch? Possible resolutions, all acceptable if declared:
using the less sensitive **Zn 307.6 nm** line; diluting Zn samples into a 0.1–1 mg L⁻¹ working range;
or using a quadratic calibration with the fit form stated. What is not acceptable is a fitted curve
extrapolated through a rolled-over region with the roll-over unreported. **The calibration data must
be supplied per metal per batch** (Phase 5 data request) so this can be checked rather than assumed.

### B10.5 — Replicate structure will not support error bars
**Severity 🟠 High. Attack A09. Bible anti-pattern 3.**

§6 sets "n = 3 on headline points … n = 2 minimum elsewhere", but §8.2 specifies n = 3 only at the
50 ppm Pb point and is silent on the rest. If the isotherms were run at n = 1, Fig 4.5 cannot carry
error bars on 13 of 14 points, Table 4.2 cannot report meaningful confidence intervals, and the
capacities cannot be quoted with a ±. The Bible is explicit that "40.11 mg/g without a ± is a claim
you cannot defend". **Ruling: Phase 4 question — what n was actually run at each point?** If n = 1,
the honest response is to report the fitted parameter confidence intervals from the non-linear
regression (which the fit provides even from single-replicate data) and to state clearly that the
error bars reflect regression uncertainty, not measurement replication. That is defensible; silence
is not.

### B10.6 — The ossein was supplied, not prepared: consequences beyond disclosure
**Severity 🔴 Critical to compliance and to novelty claim 1.**

Protocol §4 note: *"The starting material is demineralized fish-scale ossein supplied in bulk
(approximately 25 g) … No demineralization is performed in this protocol."* Protocol §7.2 opens *"The
supplied ossein is demineralized in bulk and not yet powdered."*

This collides with four things at once:

1. **Report §2.2** is specified as "Preparation of ossein from fish scales — full demineralisation
   protocol: acid identity and concentration, temperature, duration, liquid:solid ratio, wash steps,
   drying temperature, **yield (%)**". None of that can be written if the demineralisation was not
   performed. §2.2 must be rewritten as *"Source and conditioning of the ossein"*.
2. **Figure 2.1** is specified as "Fish scale → ossein → galloyl–ossein process flow, with real
   photographs". The first stage cannot be photographed if the scales were never handled. The figure
   must be redefined as supplied ossein → sized fraction → TA-OSS, which is still good authenticity
   evidence, or the raw-scale panel dropped.
3. **Novelty claim 1** — "Synthesis and full characterisation of a galloyl-functionalised ossein
   biosorbent **from two waste streams**" — is weakened if the ossein was a purchased commercial
   product rather than fish-scale waste processed by the author. It is not necessarily false: the
   *material* is still waste-derived. But the claim must be worded to match what was actually done,
   and the report must say who demineralised it. Overstating provenance is exactly the kind of thing
   that unravels in an oral defence.
4. **Disqualification rule 2.3, third-party execution.** "No researcher (including graduate students)
   from any university or research institute may complete any part of the research on your behalf.
   They may *guide*; you must *do*." If the ossein was **purchased** or **supplied by a school**,
   there is no issue whatever — buying a starting material is normal. If it was **prepared for
   Palaash by a researcher at a university or institute**, that is a part of the research completed
   on his behalf and the position needs care and full declaration. **This is the highest-stakes
   Phase 4 question and it is asked directly.**

### B10.7 — Batch regeneration compares two different quantities
**Severity 🟡 Medium.**

§8.5 takes spent sorbent from the **ternary** experiment, but Stage C re-adsorbs from **single-metal
50 ppm Pb**. R(%) = q_e(cycle n)/q_e(cycle 1) is then ambiguous: if "cycle 1" is the original ternary
uptake, the ratio compares ternary Pb uptake to single-metal Pb uptake and is meaningless; if
"cycle 1" is the first single-metal re-adsorption, the ratio is valid but there are then only two
retention points from three cycles. **Ruling: Phase 4 question — which was done?** Protocol v2 will
define cycle 1 as the **first single-metal re-adsorption after the initial desorption**, and will
report the initial ternary loading separately as the source of the desorbate.

### B10.8 — No mass balance anywhere
**Severity 🟡 Medium. Bible C4 lists mass balance as a rigour feature.**

Neither the batch nor the column work closes a mass balance. For the column this is nearly free:
Pb fed = Pb in the pooled effluent + Pb in the regenerate + Pb remaining on the bed. All three are
already measured or measurable. A closure of 95–105% is a strong, cheap authenticity signal; a
closure of 70% is itself an important finding. **Ruling: add to protocol v2 §2.7 and report in §4.8.**

### B10.9 — Expected outcomes are written into the protocol before execution
**Severity 🟡 Medium. Methodological, and visible.**

Almost every section carries an "**Expected**" note, and §5.4.3 sizes the column using *"a
representative monolayer capacity of order 40 mg/g (the value **this system is expected to
deliver**)"* — a number remarkably close to the eventual reported 40.11 mg g⁻¹. Pre-registering an
expectation is legitimate and can be a strength; but the report must **never** present these as
predictions the data then confirmed, because the expectation was written into the design. **Ruling:**
protocol v2 relabels every "Expected" note as **"Acceptance criterion"** or **"Planning basis"**, and
the report does not reproduce them as predictions. If the coincidence between the 40 mg g⁻¹ planning
figure and the measured value is ever raised, the correct answer is that the design was sized from a
literature-typical capacity, and that is a defensible answer only if it was said first.

### B10.10 — Ambient temperature neither controlled nor recorded
**Severity 🟡 Medium.**

§6 gives "Ambient (≈ 25 °C)". Pune in June is not reliably 25 °C, and laboratory ambient may have
drifted several degrees across a multi-week campaign. Sorption equilibria are temperature-sensitive;
uncontrolled drift is an uncontrolled variable across the isotherm, kinetic and competitive datasets.
**Ruling: Phase 4 question — was temperature recorded at all?** If yes, report the range. If no, the
report states "ambient laboratory temperature, nominally 298 K, not actively controlled" and lists it
in §5.3 limitations. Do not write "25 °C" as though it were measured.

### B10.11 — Washing endpoint is subjective
**Severity 🟡 Medium. Feeds A10 and A11.**

§7.4 washes "until the filtrate is water-clear (typically 5–8 washes)", with the quantitative 276 nm
endpoint optional. Since insufficient washing leaves free tannic acid that leaches, complexes metals
in solution and **falsely raises apparent removal** — the protocol's own §7.4 "Critical" note says
exactly this — the endpoint should not be subjective. **Ruling: Phase 4 question on what was actually
done; protocol v2 specifies the 276 nm absorbance endpoint as primary with the visual check as a
fallback.**

### B10.12 — No binary systems
**Severity 🟡 Medium.**

Only ternary competition was run. Binary Pb/Cu and Pb/Zn systems would isolate pairwise competition
and give a cleaner comparison to the pairwise computed ΔΔG. **Ruling: not worth running now given
the timeline. State in §5.3 as a limitation and in §5.4 as future work.**

### B10.13 — 0.45 µm filtration counts any precipitate as uptake
**Severity 🟠 High, as the mechanism of B10.1.**

Stated separately because it applies beyond the sulfate case: any Pb removed as a solid — hydroxide
at elevated local pH, sulfate in the ternary, carbonate from atmospheric CO₂ in a long unsealed
equilibration — is captured by the 0.45 µm filter and recorded as sorption. The speciation
calculation and the sorbent-free blanks are the only defences. **Ruling: covered by B9 and B10.3;
stated explicitly in §2.5.3 as a recognised limitation of the analytical scheme.**

### B10.14 — Material budget does not accommodate the temperature series
**Severity 🟡 Medium.**

§13 closes the TA-OSS budget at ~4.9 g batch + 8 g columns + 1 g ash + FTIR against ~18–19 g
produced. A temperature series adds perhaps 2–4 g. **Ruling: Phase 4 question — was the series run
from the same batch, from the reserve, or from a second functionalisation batch?** A second batch is
not a problem, but it must be declared, and if the loading differed between batches that is a
confounder for the van 't Hoff analysis specifically.

### B10.15 — Missing models
**Severity 🟡 Medium.**

Protocol §11 lists Langmuir, Freundlich, PFO, PSO and Weber–Morris. The Bible additionally requires
or recommends: **Sips and/or Redlich–Peterson** (§4.2), **Elovich** (§4.3), and **Thomas,
Yoon–Nelson and Adams–Bohart** for the column (§4.8) — "column data without a model fit reads as
under-analysed". **Ruling: all are additional analysis of existing data and cost no bench time.
Implemented in `analysis/src/isotherms.py`, `kinetics.py` and `column.py`.** Note that a three-
parameter Sips fit to a four-point Cu or Zn isotherm is over-parameterised; report it with that
caveat or restrict Sips to the six-point Pb isotherm.

### B10.16 — Positive finding: the selectivity coefficient is defined consistently
**No action.** Protocol §11 gives α(Pb/M) = (q_Pb·C_e,M)/(q_M·C_e,Pb); the Bible gives
α(Pb/M) = (q_Pb/C_e,Pb)/(q_M/C_e,M). These are algebraically identical, and both equal K_d,Pb/K_d,M.
Recorded because a divergence here would have propagated into every selectivity number, and because
the report should state the identity explicitly so the referee need not check it.

### B10.17 — No failed conditions were designed in
**Severity 🟡 Medium. Bible Observation 3; Figure 4.17; anti-pattern 10.**

The protocol screens nothing and rejects nothing: one grafting recipe, one eluent, one particle
fraction. The Bible is emphatic that reporting failure is reporting competence, and that the 2025
Chemistry Silver devoted multiple panels to conditions that destroyed its material. Fig 4.17 (failed
conditions gallery) has no source in the current design. **Ruling: Phase 4 question — what actually
went wrong?** Anything real qualifies: a batch that leached, a bath that gelled, a column that
channelled, a fraction ground too fine, a first calibration that failed R², an eluent tried and
abandoned. This does not need to be a designed experiment; it needs to be an honest record of a real
campaign. **If genuinely nothing failed, Fig 4.17 is dropped and that is fine — but a report with no
failures at all invites the suspicion the Bible warns about.**

---

## TABLE C — OUTLINE-VS-DATA RECONCILIATION

Every headline number in the Stage-1 outline, its expected source dataset, and its status. **All
UNVERIFIED.** These values live here and **nowhere else** — they are not seeded into
`CANONICAL_NUMBERS.yaml`, are not used to check a fit, and do not influence the choice of
computational protocol.

**Significant figures.** Four-significant-figure values such as 40.11 mg g⁻¹, 71.6%, 3.63 and 80.1%
carry no uncertainty and imply a measurement precision the replicate structure almost certainly does
not support. **Expect 40.11 → 40.1 ± x, 71.6 → 72 ± x, 3.63 → 3.6 ± x.** Reporting a tighter number
than the data supports is Bible anti-pattern 3 and is trivially spotted.

| # | Claim | Value | Expected source dataset | Status | Note |
|---|---|---|---|---|---|
| C01 | Tannic-acid loading | ~5.5 wt% | `characterisation/loading/` gravimetry, n ≥ 3 | UNVERIFIED | Attack A11. "~" is honest; keep a ± |
| C02 | q_max Pb(II) | 40.11 mg g⁻¹ | `batch/` Pb isotherm, non-linear Langmuir | UNVERIFIED | = 0.194 mmol g⁻¹. See **B10.2** |
| C03 | q_max Cu(II) | 25.38 mg g⁻¹ | `batch/` Cu isotherm | UNVERIFIED | = 0.399 mmol g⁻¹ — **highest on a molar basis** |
| C04 | q_max Zn(II) | 16.86 mg g⁻¹ | `batch/` Zn isotherm | UNVERIFIED | = 0.258 mmol g⁻¹ |
| C05 | Ternary removal, Pb | 71.6% | `competitive/` equal-mass ternary, n = 3 | UNVERIFIED | Depends on the **B3** ruling and on measured initial aliquots |
| C06 | Ternary removal, Cu | 41.0% | as C05 | UNVERIFIED | |
| C07 | Ternary removal, Zn | 26.4% | as C05 | UNVERIFIED | |
| C08 | α(Pb/Cu), TA-OSS | 3.63 | derived from C05, C06 | UNVERIFIED | Exactly reproducible from C05/C06 at nominal C₀ = 50 — see D.1 |
| C09 | α(Pb/Zn), TA-OSS | 7.03 | derived from C05, C07 | UNVERIFIED | Likewise |
| C10 | α(Pb/Cu), RAW-OSS control | 1.24 | `competitive/` RAW control | UNVERIFIED | Bible §4.4: quantify how much of the final selectivity the grafting contributes |
| C11 | α(Pb/Zn), RAW-OSS control | 2.33 | as C10 | UNVERIFIED | |
| C12 | Bed volumes to 10% breakthrough | ~45 BV | `column_A/` cycle 1 | UNVERIFIED | Confirmed correct by Palaash; **B4** requires a physical explanation |
| C13 | Lead enrichment factor | 11–14 × | `column_A/` pooled regenerates | UNVERIFIED | Consistent with C12 — see D.2 |
| C14 | Capacity retention over 3 cycles | 80.1% | `column_A/` BV₁₀ per cycle, **or** `regeneration/` batch q_e per cycle | UNVERIFIED | **Ambiguous which.** Phase 4 question |
| C15 | ΔG°_bind, Pb(II) | −145.2 kJ mol⁻¹ | *nothing computed* | UNVERIFIED | **No stated reference state.** Attack A04. **Not carried forward.** |
| C16 | ΔG°_bind, Cu(II) | −110.4 kJ mol⁻¹ | *nothing computed* | UNVERIFIED | As C15 |
| C17 | ΔG°_bind, Zn(II) | −85.6 kJ mol⁻¹ | *nothing computed* | UNVERIFIED | As C15 |
| C18 | f_orb, Pb(II) | 0.38 | *nothing computed* | UNVERIFIED | Scheme-dependent; the scheme is not yet chosen. Attacks A01, A13 |
| C19 | ΔG°_hyd, Cu(II) | ≈ −2100 kJ mol⁻¹ | literature | UNVERIFIED | Convention not stated. Attack A12 |
| C20 | ΔG°_hyd, Pb(II) | ≈ −1481 kJ mol⁻¹ | literature | UNVERIFIED | As C19; prefer **relative** values |
| C21 | ΔH° | +15.2 kJ mol⁻¹ | `thermodynamics/` — **dataset absent from the protocol** | UNVERIFIED | **B1** |
| C22 | ΔS° | +136.5 J mol⁻¹ K⁻¹ | as C21 | UNVERIFIED | **B1** |
| C23 | Optimum pH | 5.0 | `batch/` pH optimisation | UNVERIFIED | Also requires the pH_PZC and speciation support |
| C24 | "Pb faced a >3-fold molar disadvantage" | ≥ 3 × | `competitive/` measured initial aliquots | UNVERIFIED | **True at 50/50/50 mg L⁻¹ (3.26× and 3.17×). False if the run was truly equimolar. B3.** |
| C25 | "significantly exceeded the control" (α vs control) | — | statistical comparison | UNVERIFIED | Bible §12: **never "significantly" without a p-value.** Either run the test on the n = 3 replicates or rewrite as "markedly exceeded" |

**Also to be re-derived, not inherited:** the DFT-vs-experiment discrepancy the Bible flags as Attack
A05. From the outline's own numbers, computed ΔΔG(Pb/Cu) = −34.8 kJ mol⁻¹ against experimental
ΔΔG = −RT ln(3.63) = **−3.20 kJ mol⁻¹** — a factor of **10.9**. For Pb/Zn, −59.6 against −4.83, a
factor of **12.3**. Whatever the new calculations produce, a discrepancy of roughly this order is
expected and **must be pre-empted in §4.6.3**, not discovered by the referee.

---

## SECTION D — ARITHMETIC PERFORMED DURING THIS AUDIT

Recorded so it can be checked, and so the report can reuse it. All figures reproducible by re-running
the audit calculation.

### D.1 The outline's selectivity factors are exactly self-consistent
Taking V/m = 50 mL / 0.1 g = 0.5 L g⁻¹ and nominal C₀ = 50 mg L⁻¹ for each metal, the removal
percentages C05–C07 give K_d(Pb) = 1.2606, K_d(Cu) = 0.3475, K_d(Zn) = 0.1793 L g⁻¹, hence
**α(Pb/Cu) = 3.628** and **α(Pb/Zn) = 7.029** — matching the outline's 3.63 and 7.03 to three
significant figures.

Two consequences. **First**, the outline's α values were genuinely computed from the removal data
rather than asserted, which is reassuring. **Second**, they were computed against the **nominal**
C₀ = 50 mg L⁻¹, not against the measured initial aliquots that protocol §8.4 step 2 requires. Because
α depends on both q_e and C_e, recomputing against measured initials **will shift these numbers**.
Expect the published α values to move, and plan the abstract accordingly.

### D.2 Column internal consistency
At BV₁₀ = 45 with an 8.0 mL bed, 360 mL of 100 mg L⁻¹ feed has passed, carrying **36.0 mg** of Pb. If
essentially all of it was retained up to 10% breakthrough, the bed of 4.0 g had taken up
**≈ 9.0 mg g⁻¹** — about **22%** of a 40 mg g⁻¹ batch equilibrium capacity. Independently, an
enrichment factor of 12 into 3 BV (24 mL) of eluent corresponds to 28.8 mg desorbed, or
**7.2 mg g⁻¹**. The two agree to within the desorption efficiency. **The measured column numbers are
mutually consistent; the design-basis estimates were consistent with each other but not with the
measurement.** This supports B4's ruling and gives §4.8 a quantitative starting point.

### D.3 Galloyl site balance — a proposed rigour addition
Tannic acid (C₇₆H₅₂O₄₆, M = 1701.2 g mol⁻¹) is nominally decagalloyl glucose. At 5.5 wt% loading the
sorbent carries **0.323 mmol galloyl g⁻¹**. Total metal captured in the ternary is
0.086 + 0.161 + 0.101 = **0.349 mmol g⁻¹**, giving **1.08 metal ions per galloyl group** — close to
1:1, which is chemically sensible for bidentate chelation at a vicinal-dihydroxy site.

**However**, the single-metal Cu capacity alone is 0.399 mmol g⁻¹, i.e. **1.24 Cu per galloyl**,
which exceeds a 1:1 site inventory. That is informative rather than contradictory: it indicates the
**collagen backbone contributes capacity independently of the galloyl groups** — consistent with the
RAW-OSS control already showing α(Pb/Cu) = 1.24 > 1. **Recommendation: present this site balance in
§4.1 or §4.2.** It is arithmetic on numbers the report publishes anyway, it demonstrates the author
reasoning about their own material at the level of sites rather than mass, and it makes the honest
attribution the Bible asks for in §4.4 — how much of the selectivity is the grafting and how much
was already there — quantitative rather than rhetorical. Caveat to state: the 10-galloyl-per-TA
figure is nominal, and gravimetric loading does not distinguish grafted from entrained tannin, so
this is a **consistency check, not a proof**.

### D.4 Stock solution masses are correct
Pb(NO₃)₂ 1.599 g L⁻¹ (calculated 1.5985), CuSO₄·5H₂O 3.929 g L⁻¹ (3.9289), ZnSO₄·7H₂O 4.398 g L⁻¹
(4.3980) all give 1000 mg L⁻¹ of the metal. **No error.** Recorded because an error here would have
invalidated everything downstream.

### D.5 Column hydraulics check
8 BV h⁻¹ → EBCT = 1/8 h = **7.5 min** ✓. For an 8 mL bed, 8 BV h⁻¹ = 64 mL h⁻¹ = **1.07 mL min⁻¹** ✓
("about 1.0 mL min⁻¹"). Design basis BV_sat = q*·ρ_b/C₀ = 33 × 0.5 / 0.1 = **165** ✓ (protocol says
≈ 167). **No error in the protocol's own arithmetic** — the estimates are internally correct; they
are simply superseded by measurement.

---

## SECTION E — WHAT MUST GO TO PALAASH

Ordered by consequence. These become the Phase 4 interview.

| Priority | Item | Why it blocks |
|---|---|---|
| 1 | **B3** — was the ternary equal-mass or truly equimolar? | Determines whether the outline's abstract must be amended and which argument §4.4 can make |
| 2 | **B10.1** — was a sorbent-free ternary blank run? Was any turbidity observed? | PbSO₄ supersaturation is an alternative explanation for Finding 2 |
| 3 | **B10.6** — who supplied or prepared the ossein? | Third-party-execution rule; novelty claim 1; §2.2; Fig 2.1 |
| 4 | **A20** — has any part of this been submitted anywhere before? | Disqualification trigger if undeclared |
| 5 | **B1** — the thermodynamics dataset specification | Finding 3 and the whole desolvation closure |
| 6 | **A17 / C-022** — who operated each instrument, at which facility? | Mandatory declaration; blocks the Acknowledgement |
| 7 | **B10.5, B10.4, B10.10** — actual replicates, calibration ranges, temperature record | Determines whether error bars and stated precision are defensible |
| 8 | Protocol deviations — what did not go as written? | §2.3.3, Fig 4.17, and the authenticity case |
| 9 | **C14, B10.7** — which retention number is 80.1%, and what was the cycle-1 denominator? | Two different quantities are currently conflated |
| 10 | Which datasets exist right now versus which are still to be produced | Determines what can be built this week |

---

## AMENDMENTS RAISED BY THIS AUDIT

Recorded in `00_SPEC.md` §14 and in the attack register.

| ID | Amendment |
|---|---|
| A-01 | TGA and BET **DESIGNED OUT**; replacement evidence set of six lines specified (**B5**) |
| A-02 | All fitting **non-linear**; linearised forms of protocol §11 superseded (**B2**) |
| A-03 | **XPS** and **SEM-EDX** added as new protocol sections (**B6**) |
| A-04 | **Quantified leaching test** mandatory (**B7**) |
| A-05 | **LOD / LOQ / spike recovery** added (**B8**) |
| A-06 | **Computed speciation with saturation indices** added (**B9**) |
| A-07 | **Temperature series** required as an external dataset (**B1**) |
| A-08 | Column planning estimates superseded by measurement; shortfall requires explanation (**B4**) |
| A-09 | Ternary composition labelling — **open, awaiting Palaash** (**B3**) |
| **A-10** | **Sorbent-free blanks** required at the operating pH and in both ternary compositions (**B10.3**) |
| **A-11** | **Mass balance** added to the column work (**B10.8**) |
| **A-12** | Missing models added: Sips / Redlich–Peterson, Elovich, Thomas / Yoon–Nelson / Adams–Bohart (**B10.15**) |
| **A-13** | "Expected" notes relabelled **"Acceptance criterion"**; not reproduced in the report as predictions (**B10.9**) |
| **A-14** | Report §2.2 rewritten as **"Source and conditioning of the ossein"**; Fig 2.1 redefined (**B10.6**) |
| **A-15** | Batch-regeneration cycle 1 defined as the **first single-metal re-adsorption** (**B10.7**) |
| **A-16** | Both mg g⁻¹ and mmol g⁻¹ carried throughout; molar-basis inversion confronted in §4.2 (**B10.2**) |
