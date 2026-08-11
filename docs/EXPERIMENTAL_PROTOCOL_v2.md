<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# EXPERIMENTAL PROTOCOL v2

`Lab Protocol (1) (1).pdf` (v1, 8 June 2026) restated at **report-Methods granularity**, with every
Phase 3 audit amendment and every Phase 4 decision incorporated. **This document is the source text
for Section II of the report.**

**Execution date: July 2026.** The v1 protocol was written 8 June 2026 and executed in July 2026 in
a laboratory maintained at 25 °C.

**How to read the markings.**

| Marking | Meaning |
|---|---|
| **[AMENDED v2]** | Present in v1, changed. The justification is stated inline. |
| **[NEW v2]** | Absent from v1 entirely. |
| **[DESIGNED OUT]** | In the Bible's plan, removed with a stated reason. |
| **[UNCHANGED]** | Palaash's committed parameter, preserved verbatim. |
| `\TODOPAL` | Awaiting Palaash's answer; not to be written as fact. |

**Committed parameters preserved unchanged unless an audit item overrode them:** batch dose 0.1 g
in 50 mL (2 g L⁻¹) · 120 min contact · 0.50–1.00 mm sieved fraction · 5% w/v tannic acid bath at
pH 5.0 for 12–16 h · 10 mm ID column · 4.0 g bed · 8 BV h⁻¹ downflow service · 3 BV of 0.1 M HCl
counter-current at 4 BV h⁻¹ · n = 3 on the headline point.

---

## 2.1 Materials

All reagents ACS reagent grade or equivalent, used as received unless stated. Water: deionised
throughout. `\TODOPAL{resistivity or conductivity of the DI water, and the supplier or system}`

| Reagent | Formula | Specification | Role |
|---|---|---|---|
| Tannic acid | C₇₆H₅₂O₄₆ | ACS, ≥ 95%, M = 1701.2 g mol⁻¹ | Galloyl O-donor ligand |
| Lead(II) nitrate | Pb(NO₃)₂ | ACS | Pb stock, all phases and the column feed |
| Copper(II) sulfate pentahydrate | CuSO₄·5H₂O | ACS | Cu competitor stock |
| Zinc sulfate heptahydrate | ZnSO₄·7H₂O | ACS | Zn competitor stock |
| Hydrochloric acid | HCl | 37% conc. | pH adjustment; batch desorption; column regeneration (0.1 M) |
| Sodium hydroxide | NaOH | pellets, ACS | pH adjustment; functionalisation bath to pH 5.0 |
| Nitric acid | HNO₃ | 1 M | Stock preservation; 5% glassware acid wash |
| Sodium chloride | NaCl | ACS | 0.01 M background electrolyte, pH_PZC only |
| Gallic acid | C₇H₆O₅ | ACS | **[NEW v2]** Calibration standard for the leaching assay (§2.4.6) |
| pH buffers | — | pH 4, 7, 10 | Three-point meter calibration |
| Glass wool | — | acid-washed borosilicate | Column bed support and top cap |

`\TODOPAL{supplier and lot number for each reagent — Table 2.1 requires grade AND supplier}`

**[AMENDED v2] Counter-ion composition, and why it matters.** Pb enters as the **nitrate**; Cu and
Zn each enter as **sulfates**. In single-metal work this is immaterial. In the ternary work it is
not: the competitors carry sulfate into a solution containing Pb²⁺, and PbSO₄ (anglesite) is
sparingly soluble. Both ternary compositions are computed to be supersaturated with respect to
anglesite (§2.9, Appendix G). This is reported, not concealed. *Justification for the amendment:*
audit **B10.1**; attack **A22**. A repeat of this work should use Cu(NO₃)₂ and Zn(NO₃)₂ so that all
three metals share a non-complexing, non-precipitating counter-ion; this is stated in §5.4 Future
work.

---

## 2.2 Source and conditioning of the ossein
**[AMENDED v2 — retitled.]** v1 §7.2 was "Ossein conditioning"; the Bible's plan assumed
"Preparation of ossein from fish scales" with a demineralisation protocol and a reported yield.

**No demineralisation was performed in this work.** Demineralised fish-scale ossein was **purchased
commercially from Nizona Marine Products Pvt. Ltd.** and supplied in bulk (approximately 25 g).
*Justification:* Phase 4 answer Q5. The report states the source explicitly in Materials and in the
Acknowledgement, and does not describe a preparation that was not carried out. `\TODOPAL{fish
species, and any specification sheet Nizona supplied — the report should name the species if known}`

**Consequences carried through the report:** the yield of demineralisation is not reported because
no demineralisation was performed; **Figure 2.1** is redefined as *supplied ossein → sized fraction
→ TA-OSS* rather than *raw scale → ossein → TA-OSS*; and **novelty claim 1** is worded to say that
the material is waste-derived while the waste stream was processed by the supplier, not by the
author. Overstating provenance is exactly what unravels under oral examination.

**Conditioning procedure [UNCHANGED]:**
1. The supplied ossein was rinsed three times with 500 mL portions of deionised water.
2. Dried in an oven at 60 °C to constant mass (Δm < 0.5% over 1 h). Dry mass recorded.
3. Ground with a mortar and pestle.
4. Sieved through a 1.0 mm screen and then a 0.5 mm screen; the **0.50–1.00 mm** fraction (passing
   1.0 mm, retained on 0.5 mm) was collected and its mass recorded.
5. Portioned: 18 g for functionalisation, 5 g for the RAW-OSS control and the ash and FTIR samples,
   remainder (~2 g) held in reserve.

**Rationale for the particle fraction [UNCHANGED]:** 0.50–1.00 mm gives D_c/d_p ≈ 10–20 at the 10 mm
column internal diameter, suppressing wall channelling while remaining easy to pack and recover.

`\TODOPAL{mass actually collected in the 0.50-1.00 mm fraction, and the mass lost to fines — the
sizing yield belongs in the report (Q14)}`

---

## 2.3 Galloyl functionalisation with tannic acid

### 2.3.1 Grafting protocol [UNCHANGED]

**TA-OSS.** 18 g of tannic acid was dissolved in 360 mL of deionised water (**5% w/v**) with gentle
warming to ≤ 50 °C where dissolution was slow. The bath was adjusted to **pH 5.0** with 1 M NaOH
added dropwise, and the volume of NaOH recorded. 18 g of the sized ossein was added, the beaker
covered with Parafilm, and the mixture stirred on a magnetic stirrer at moderate speed
(≈ 300–400 rpm) for **12–16 h**. Stirrer speed was kept moderate: excessive speed pulverises the
granules into fines that foul the column packing.

**RAW-OSS control [UNCHANGED].** 5 g of sized ossein in 100 mL deionised water at pH 5.0, stirred
identically for the same period. Identical processing without tannic acid isolates the effect of
functionalisation.

**[NEW v2] Grafting chemistry to be stated in the report.** v1 gives the recipe but never states the
chemistry. Section 2.3 of the report must present a reaction scheme (Fig 2.2) and must be honest
about what is and is not demonstrated: at pH 5.0 in air, galloyl groups undergo partial oxidation to
*ortho*-quinones, which can couple to collagen lysine ε-amino and N-terminal amine groups by Michael
addition or Schiff-base formation; hydrogen bonding and hydrophobic association between polyphenol
and collagen also occur and are well documented. **The relative contribution of covalent grafting
versus strong physisorption is not resolved by the measurements made here.** The leaching test
(§2.4.6) bounds it; the FTIR (§2.4.1) evidences the presence of the aromatic system; neither
identifies the bond. Saying this is a rigour point; asserting a covalent bond that was not
demonstrated is not.

### 2.3.2 Washing and quantification of galloyl loading [AMENDED v2]

**Washing.** Both batches were vacuum-filtered through a Büchner funnel and washed with successive
200 mL portions of deionised water.

**[AMENDED v2] Wash endpoint.** v1 specified "until the filtrate is water-clear (typically 5–8
washes)", with a quantitative UV-Vis endpoint at 276 nm as optional. **The quantitative endpoint is
primary in v2: wash until the filtrate absorbance at 276 nm falls below 0.05**, with the visual
check as a fallback only. RAW-OSS received the same number of washes as TA-OSS.
*Justification:* v1's own §7.4 "Critical" note states that insufficient washing leaves free tannic
acid that leaches, complexes metals in solution and **falsely raises apparent removal**. A defect
that serious should not have a subjective endpoint. Audit **B10.11**.
`\TODOPAL{how many washes were actually run, and was the 276 nm absorbance measured? (Q13)}`

**Drying.** Both batches dried at 50 °C for 6–8 h to constant mass; both dry masses recorded.

**Loading [UNCHANGED]:**

> tannin loading (%) = (m_func − m_raw,eq) / m_raw,eq × 100

where m_func is the dry mass after functionalisation and m_raw,eq the equivalent dry mass of
unfunctionalised ossein. Acceptance range 4–8 wt%. Reported as mean ± SD from n ≥ 3.

**[NEW v2] Stated limitation of the gravimetric method.** Mass difference cannot distinguish grafted
tannin from tannin entrained in the matrix, and it is sensitive to residual moisture. This is
declared in §4.1, and the leaching test of §2.4.6 is what bounds the entrained fraction. Attack
**A11** is answered by giving the method **and** its limitation, not by giving the number alone.

### 2.3.3 Conditions screened and rejected
**[NEW v2 — source outstanding.]** v1 screened nothing: one grafting recipe, one eluent, one
particle fraction. The Bible's Observation 3 is that reporting failure is reporting competence, and
the 2025 Chemistry Silver devoted multiple panels to conditions that destroyed its material.

`\TODOPAL{Q11 — which steps did not go as written, and what actually happened? Any batch that
leached, bath that gelled, column that channelled, fraction ground too fine, calibration that failed
R^2, or eluent tried and abandoned. If genuinely nothing failed, this subsection and Fig 4.17 are
dropped.}`

### 2.3.4 Portioning [UNCHANGED]
TA-OSS: ≥ 30 pre-weighed 0.1 g vials for batch work; one 4.0 g vial for Column A; one 4.0 g vial for
Column B; ~1 g for ash; a portion for FTIR. Stored in a desiccator. RAW-OSS: ≥ 12 pre-weighed 0.1 g
vials, ~1 g for ash, a portion for FTIR. RAW-OSS and TA-OSS were photographed side by side to
document the colour change.

---

## 2.4 Characterisation

### 2.4.0 Techniques designed out [DESIGNED OUT]

**Thermogravimetric analysis and nitrogen physisorption (BET) were not available for this study.**
Neither instrument was accessible. Consequently no thermogram is reported (the Bible's Fig 4.3 is
withdrawn), **no specific surface area or pore structure is reported**, and capacity is reported per
unit mass throughout rather than per unit area. ICP-MS was likewise unavailable; all metal analysis
is by flame AAS.

*Justification:* audit **B5**, amendment **A-01**. A missing measurement that is explained is a
limitation; one silently absent is a hole. The evidence for grafting instead rests on six
independent lines — FTIR band assignment, gravimetric loading, the pH_PZC shift, residual mineral
content, the quantified leaching test, and XPS. The last two are **new in v2** and are stronger
evidence than TGA mass loss and BET area would have been, because TGA and BET are indirect whereas
XPS Pb 4f is a direct observation of the binding event. This is a design choice and is stated as
one.

### 2.4.1 ATR-FTIR [UNCHANGED]
Spectra recorded for RAW-OSS, TA-OSS and spent TA-OSS. Sample pressed onto the ATR crystal;
**4000–400 cm⁻¹, 4 cm⁻¹ resolution, ≥ 32 scans**; each spectrum exported and a labelled overlay
produced. Instrument make and model, and operator, to be tabulated (Table 2.2).

Bands of interest: aromatic C=C ≈ 1600–1620 cm⁻¹ and galloyl ester C–O / C=O ≈ 1700–1730 cm⁻¹
(new on functionalisation); collagen Amide I ≈ 1630, Amide II ≈ 1540, Amide III ≈ 1235 cm⁻¹
(expected preserved); phosphate ≈ 1030 cm⁻¹ (residual mineral). The spent sample is expected to show
shifts of the carbonyl/ester features and dampening of the phenolic O–H band.

**Note on the spent sample:** it comes from the column (§2.7.6), so it is **Pb-only loaded**, not
ternary-loaded. The report states which.

### 2.4.2 Scanning electron microscopy and EDX [NEW v2]
Absent from v1 although the instrument was available. *Justification:* audit **B6**, amendment
**A-03**.

**Samples:** RAW-OSS, fresh TA-OSS, Pb-loaded TA-OSS; spent post-column TA-OSS if material remains.

**SEM:** at least three magnifications per sample (low ≈ 100×, mid ≈ 1000×, high ≈ 5000×), from the
same region where practicable so that before/after comparison is meaningful. Recorded per image:
accelerating voltage, working distance, detector (SE/BSE), magnification, and the **conductive
coating element**. The coating matters — a carbon coat interferes with the EDX carbon signal and a
gold coat overlaps the Pb M lines. **Scale bar burned in by the instrument**, never added afterwards.

**EDX:** elemental maps for C, N, O, **Pb**, plus Ca and P (residual mineral) on the Pb-loaded
sample; point and area spectra with the instrument's quantification table where produced.
Accelerating voltage ≥ 15 kV for the Pb L lines; live time and count rate recorded.

**[NEW v2] Stated limitation.** EDX on a rough, low-atomic-number, coated biological material is
**semi-quantitative at best**. EDX is presented as evidence of the *spatial distribution* of Pb
across the surface and confirmation of its *presence*. **EDX weight percentages are not quoted as a
measurement of loading.** Saying this pre-empts the objection; quoting EDX wt% as quantitative
invites it.

### 2.4.3 X-ray photoelectron spectroscopy [NEW v2]
Absent from v1 although the instrument was available. XPS Pb 4f is the single strongest direct
evidence of Pb–O coordination and oxidation state and merits its own subsection. *Justification:*
audit **B6**, amendment **A-03**.

**Samples (three required):** RAW-OSS · fresh TA-OSS · **Pb-loaded TA-OSS**, from a single-metal Pb
equilibration at pH 5.0, **washed with deionised water** to remove physisorbed Pb and dried at
50 °C. The wash step is not optional: unwashed material shows surface Pb salt rather than
coordinated Pb, and a referee will ask. Wash volume and number recorded. *Recommended fourth
sample:* ternary-loaded TA-OSS, which would put Pb 4f, Cu 2p and Zn 2p on one surface and give a
direct surface-composition measurement of the competitive result.

**Regions per sample:**

| Region | Purpose |
|---|---|
| Survey, 0–1200 eV | Elemental inventory; confirms no unexpected contamination |
| **Pb 4f** | The primary measurement. The 4f₇/₂ position distinguishes Pb(II)–O carboxylate/phenolate coordination from PbO, Pb(OH)₂, PbCO₃ and metallic Pb |
| O 1s | Resolves lattice/carbonyl, hydroxyl/phenolic, and adsorbed-water components; the phenolic component is expected to change on Pb binding |
| C 1s | The charge reference, and the aromatic/carboxyl inventory that changes on grafting |
| N 1s | Collagen amide nitrogen — confirms the protein scaffold survived, and tests whether N participates in binding |
| Cu 2p, Zn 2p *(ternary sample only)* | Cu 2p₃/₂ shake-up satellite structure confirms Cu(II) rather than Cu(I)/Cu(0) |

**Acquisition parameters to record:** instrument make and model; X-ray source (Al Kα, 1486.6 eV;
monochromated or not); spot size; base pressure; survey pass energy (typically 100–200 eV) and
high-resolution pass energy (typically 20–50 eV); step size (survey ~1 eV, high-resolution
0.05–0.1 eV); dwell time; number of sweeps; whether charge neutralisation (flood gun) was used.

**Charge referencing:** **adventitious C 1s set to 284.8 eV.** Stated explicitly — binding energies
are meaningless without a named reference.

**Peak fitting:** Shirley background; Gaussian–Lorentzian line shape with the GL mixing ratio
stated; FWHM constrained equal across components within a region; **Pb 4f doublet constrained to
4.87 eV spin–orbit splitting and 4:3 area ratio**; the number of components stated and justified on
chemical grounds, **not** chosen to improve the residual.

**[NEW v2] Beam-damage check.** Pb compounds can reduce under prolonged X-ray exposure. Pb 4f is
acquired early in the sequence and, where time allows, re-acquired at the end to demonstrate the
spectrum is unchanged. One extra scan forecloses an entire line of questioning.

**Status:** the measurements **have been run**; the numeric data has not yet been released by the
laboratory. `\NEEDSDATA{Fig 4.18, Table 4.13}{XPS binding-energy/intensity CSVs, all regions, all
samples}`

### 2.4.4 Residual mineral (ash) content [UNCHANGED]
~1 g each of RAW-OSS and TA-OSS dried to constant mass at 60 °C and weighed into tared crucibles
(m_dry); ashed at **550–600 °C for ≥ 4 h** to constant mass; cooled in a desiccator and weighed
(m_ash). Residual mineral (%) = m_ash/m_dry × 100. **Run in duplicate.** Acceptance: a few weight
percent, consistent with the ≈ 1030 cm⁻¹ FTIR phosphate band.

### 2.4.5 Point of zero charge [UNCHANGED]
0.01 M NaCl prepared; 50 mL dispensed into nine flasks with initial pH set across 2–10 in one-unit
steps; a parallel set of nine prepared for RAW-OSS. 0.1 g of the appropriate sorbent added to each
and stirred **24 h**. Final pH measured and plotted against initial pH; pH_PZC is the plateau.

**[NEW v2] Caveat to state:** the determination was carried out without exclusion of atmospheric
CO₂, which shifts the drift plateau slightly. This is noted in §4.1 rather than corrected.

A lower pH_PZC for TA-OSS than for RAW-OSS confirms enrichment of acidic surface groups from
functionalisation and is an independent, *functional* line of evidence for grafting — not merely a
spectroscopic one. **v2 promotes it in §4.1 accordingly** (audit B5, evidence line 3).

### 2.4.6 Quantified tannic-acid leaching [AMENDED v2 — was optional, now mandatory]
v1 §5.1 listed the UV-Vis spectrophotometer as "(optional)" and gave only a wash *endpoint*, not a
leaching *test*. *Justification:* audit **B7**, amendment **A-04**; attack **A10**. With TGA
unavailable, this is the **only** evidence that distinguishes grafted tannin from adsorbed tannin,
and it is therefore load-bearing for the central claim that this is a functionalised material rather
than a tannin-coated one.

| Field | Specification |
|---|---|
| Conditions | **pH 5.0** (the operating pH) and **pH 2.0** (stress condition bracketing the regeneration environment) |
| Matrix | Deionised water adjusted with HCl/NaOH; no metal present |
| Dose and time | 2 g L⁻¹ and 120 min, matching the batch work so the number is directly comparable to a sorption run; **additionally a 24 h point** where material allows, since 120 min understates equilibrium release |
| Replicates | **n ≥ 3**, mean ± SD |
| Measurement | Released phenolics by UV-Vis at 276 nm against a **gallic-acid calibration curve** (≥ 5 points, R² > 0.99, run in the same session) |
| Reporting | **As a number:** mg gallic-acid-equivalent released per g sorbent, **and** as a percentage of the measured grafted loading. The percentage answers the attack |
| Controls | RAW-OSS blank at each pH, establishing that the signal is not from the collagen scaffold itself |

**Second use of the same measurement.** The pH 2 result is direct evidence for the *mechanism* of
capacity loss across regeneration cycles (attack **A16**). Small leaching at pH 2 attributes the
loss to site blocking or structural change rather than ligand loss — an evidenced attribution rather
than an asserted one. **One experiment closes two attacks.**

**Stated limitation:** quantifying tannic acid against a gallic-acid standard yields a
**gallic-acid-equivalent** value, not an absolute tannic-acid mass.

---

## 2.5 Batch sorption protocols

### 2.5.1 Solution preparation and pH control [UNCHANGED]

**Glassware acid wash.** All glassware soaked in ~5% HNO₃ (50 mL of 1 M HNO₃ made to 1 L) for
10–15 min, rinsed three times with DI, air-dried.

**Stock solutions, 1000 mg L⁻¹ of the metal**, each dissolved in ~800 mL DI in a 1 L volumetric
flask, 1 mL of 1 M HNO₃ added, made to the mark:

| Metal | Salt | Mass per litre | Check |
|---|---|---|---|
| Pb | Pb(NO₃)₂ | 1.599 g | M = 331.21; 331.21/207.2 = 1.5985 ✔ |
| Cu | CuSO₄·5H₂O | 3.929 g | M = 249.68; 249.68/63.55 = 3.9289 ✔ |
| Zn | ZnSO₄·7H₂O | 4.398 g | M = 287.54; 287.54/65.38 = 4.3980 ✔ |

*(Audit D.4 verified all three; no error.)*

**pH adjustment solutions:** 0.1 M and 1 M HCl; 0.1 M and 1 M NaOH. pH meter calibrated at three
points (pH 4, 7, 10) before each session.

**Operating pH 5.0**, established by the optimisation of §2.5.4 and justified by three independent
arguments in the report: the measured optimum; the pH_PZC of the functionalised sorbent (§2.4.5);
and the computed speciation showing Pb²⁺ dominant and below the onset of hydrolysis (§2.9).

### 2.5.2 Elemental analysis and quality control [AMENDED v2]

**Instrument [UNCHANGED]:** flame atomic absorption spectrometry, air–acetylene, hollow-cathode
lamps. Lines: **Pb 283.3 nm, Cu 324.8 nm, Zn 213.9 nm**. One element per aspiration; each ternary
and Column B sample aspirated three times.

**Calibration [UNCHANGED]:** five standards per metal plus a blank, each matrix-matched with 0.1 mL
of 1 M HNO₃ per 100 mL. Every curve must reach **R² > 0.99** before any sample is run. A mid-range
check standard at the start, middle and end of every analytical batch; any batch where the check
deviates by more than ±5–10%, or where the curve fails R² > 0.99, is rejected and re-run. All
samples filtered through 0.45 µm before analysis. Over-range samples diluted into range with every
dilution factor recorded.

**[AMENDED v2] Calibration range must be reported per metal.** v1 applied the same
1 / 5 / 10 / 25 / 50 mg L⁻¹ standard set to all three metals. Typical flame AAS linear ranges are
approximately Pb 283.3 nm ~20 mg L⁻¹, Cu 324.8 nm ~5 mg L⁻¹, **Zn 213.9 nm ~1 mg L⁻¹** — figures to
be confirmed against this instrument's own specification. A 50 mg L⁻¹ Zn standard at 213.9 nm would
sit well above the linear range. *Justification:* audit **B10.4**, attack **A25**; Zn concentrations
propagate directly into α(Pb/Zn), a headline number. Acceptable resolutions, all requiring
declaration: dilution of Zn samples into a 0.1–1 mg L⁻¹ working range; use of the less sensitive
**Zn 307.6 nm** line; or a stated quadratic calibration. What is not acceptable is a fit
extrapolated through a rolled-over region with the roll-over unreported.
`\TODOPAL{Q21 — actual standard concentrations, wavelengths, fit form and R^2 per metal per batch}`

**[NEW v2] Limit of detection and limit of quantitation.** *Justification:* audit **B8**, amendment
**A-05**. The calibration blank is measured **n ≥ 7** times independently within one analytical
session; with σ_blank its standard deviation and S the calibration slope (absorbance per mg L⁻¹):

> **LOD = 3.3 σ_blank / S**    **LOQ = 10 σ_blank / S**

named in the report as the IUPAC/ICH convention, and reported **per metal per instrument
configuration** in mg L⁻¹ (Table 2.2, Appendix C). *Acceptable alternative if seven blank replicates
were not run:* the residual standard deviation of the calibration regression, σ_y/x, substituted for
σ_blank — **the method used must be stated**, because the two give different numbers.

**Consequence, stated explicitly in the report:** every value below LOQ is reported as "< LOQ" and
is **not** used in a fit or an average. This most likely affects the early column fractions, where
effluent Pb is near zero, and the low-concentration end of the isotherms. Silently fitting below-LOQ
points is a real methodological error and is invisible unless the LOQ is published.

**[NEW v2] Spike recovery.** A real sample matrix — not a standard — spiked at two levels (low, near
2–5× LOQ; and mid-range), n = 3 at each:

> **Recovery (%) = 100 × (C_spiked − C_unspiked) / C_added**, acceptance **90–110%**

Run on each matrix type that behaves differently: (i) a filtered batch sorption supernatant,
(ii) a column effluent fraction, (iii) a diluted acid regenerate. **The regenerate is the one most
likely to fail** — strongly acidic, high ionic strength, and flame AAS is matrix-sensitive. If it
fails, the remedy is matrix-matched standards or standard addition.

### 2.5.3 Controls, blanks and replication [AMENDED v2]

**Controls [UNCHANGED]:** RAW-OSS, processed identically without tannic acid, as the negative
control, run alongside TA-OSS in the pH optimisation, at the 40 ppm isotherm point, and in the
ternary competition.

**[AMENDED v2] Sorbent-free blanks.** v1 ran a single sorbent-free flask, at pH 6.0 only (§8.1
step 5). The Bible requires a no-sorbent blank to exclude wall adsorption, and attack **A07**
requires one at the pH actually used. *Justification:* audit **B10.3**, amendment **A-10**. Required
set: pH 5.0 at 50 and 300 mg L⁻¹ single-metal Pb, **and both ternary compositions**.

> **STATUS: NOT RUN.** Phase 4 answer Q2 confirms no sorbent-free ternary blank was performed. The
> solutions were observed to remain visibly clear and this was recorded at the time. The report
> therefore (i) publishes the computed saturation indices (§2.9, Appendix G), (ii) reports the
> contemporaneous visual observation as supporting evidence, (iii) states in §5.3 that precipitation
> cannot be excluded by measurement — only by calculation and observation — and (iv) names the
> nitrate-salt design as the correction in §5.4. Attack **A22** is an **accepted risk with stated
> mitigation**, not armour.
> `\TODOPAL{supply the dated laboratory note recording that the ternary solutions remained clear —
> it is the evidence for (ii) and belongs in Appendix H}`

**[NEW v2] Recognised limitation of the analytical scheme.** Every sample is filtered at 0.45 µm
before analysis. **Any metal removed as a solid — hydroxide, sulfate, or carbonate from atmospheric
CO₂ — is retained by that filter and recorded as sorption.** The speciation calculation of §2.9 and
the sorbent-free blanks are the only defences against this, and one of the two is absent. Stated in
§2.5.3 of the report and again in §5.3.

**[AMENDED v2] Replication.** v1 §6 specified "n = 3 on headline points, n = 2 minimum elsewhere"
but §8.2 named only one point. Phase 4 answer Q20 establishes what was actually run:

> **n = 3 at the 40 mg L⁻¹ isotherm point; n = 2 everywhere else.** All values reported as
> **mean ± SD**, with n stated in every caption and every table.

This is better than v1 specified and **restores measurement error bars on every isotherm and kinetic
point**, closing attack **A09** with replication rather than with regression confidence intervals
alone.
`\TODOPAL{Q20 discrepancy — protocol §8.2 lists the Pb isotherm as 10/25/50/100/200/300 ppm with
n=3 at 50 ppm; the answer says 40 ppm. Confirm the actual concentration series.}`

### 2.5.4 pH optimisation [UNCHANGED]
500 mL of 50 mg L⁻¹ Pb prepared from stock; 50 mL distributed into four flasks set to pH 3.0, 4.0,
5.0, 6.0; an identical four-flask RAW-OSS set prepared. 0.1 g of the appropriate sorbent added to
each; stirred at moderate speed for 120 min; filtered through 0.45 µm; final pH and residual Pb
measured. One sorbent-free 50 mg L⁻¹ Pb flask at pH 6.0 as a precipitation control.

Removal (%) = (C₀ − C_e)/C₀ × 100 and q_e = (C₀ − C_e)V/m. The pH giving the highest TA-OSS removal
is the operating pH. Uptake is expected to rise from pH 3 to 5 as galloyl groups deprotonate;
operation above pH 6 is excluded because Pb hydroxide can precipitate.

### 2.5.5 Single-metal isotherms [UNCHANGED conditions, AMENDED fitting]
At the operating pH, 120 min contact, 0.1 g sorbent in 50 mL (**2 g L⁻¹**), ambient 25 °C.

- **Pb:** six concentrations (10, 25, 50, 100, 200, 300 mg L⁻¹ as written in v1 — **see the Q20
  `\TODOPAL` above**), with **n = 3** at the headline point and **n = 2** elsewhere. One RAW-OSS
  comparator at the headline point.
- **Cu and Zn:** four concentrations each (10, 50, 100, 300 mg L⁻¹), **n = 2**.

Stirred 120 min, filtered through 0.45 µm, residual metal by AAS.

### 2.5.6 Sorption kinetics [UNCHANGED]
Two time-courses, Pb and Cu, at the operating pH, 50 mg L⁻¹, 2 g L⁻¹ dose. 50 mL distributed into
six sacrificial flasks per metal, sorbent added at staggered start times so that all are sampled at
the same clock time while representing contact times of **5, 15, 30, 60, 120, 240 min**. A duplicate
of the 60 min point in each series. Each sample filtered immediately through 0.45 µm and analysed.
This series also validates the 120 min contact time used throughout.

### 2.5.7 Temperature series for van 't Hoff analysis [NEW v2]
Absent from v1 entirely — v1 §6 fixes temperature at ambient and no step varies it. *Justification:*
audit **B1**, amendment **A-07**. Without this dataset there is no §4.5, no Table 4.6, no Fig 4.8
and no Finding 3, and the computational desolvation argument loses its independent experimental
anchor.

Established by Phase 4 answers Q9 and Q10:

| Field | Specification |
|---|---|
| Design | **Full isotherm at each temperature** — K is obtained from the fitted Langmuir K_L, not from a single-point K_d. The stronger of the two available routes |
| Replicates | **n = 3** |
| Sorbent | **Same batch** as the main campaign — no batch-to-batch loading confounder |
| Temperatures | `\TODOPAL{Q8 — which temperatures, how controlled (water bath / incubator / shaker), stability in ±°C, and measured or setpoint. These values are the x-axis of Fig 4.8.}` |
| Metals | `\TODOPAL{Q9 — Pb only, or Pb + Cu + Zn? All three at matched temperatures would let §4.7.4 compare desolvation penalties experimentally across the series.}` |
| Other conditions | Identical to §2.5.5: pH 5.0, 2 g L⁻¹, 120 min, 0.45 µm filtration |

**Dimensionless-K convention — declared in the report, because this is the standard referee
objection to van 't Hoff analyses of sorption:**

> K° is obtained from the Langmuir affinity constant K_L (L mg⁻¹), converted to L mol⁻¹ by
> multiplying by the sorbate molar mass (g mol⁻¹ × 1000 mg g⁻¹), and rendered dimensionless by
> multiplying by the standard-state concentration c° = 1 mol L⁻¹, with the sorbate activity
> coefficient taken as unity at the ionic strengths used. ΔG° = −RT ln K°; ΔH° and ΔS° from the
> slope and intercept of ln K° against 1/T.

The report states explicitly that this is **one of several conventions in use**, that the absolute
ΔG° is convention-dependent, and that **the sign and magnitude of ΔH° — the load-bearing quantity
for the desolvation argument — is convention-independent, because it derives from the temperature
dependence rather than from the absolute value.** Stating this pre-empts the objection entirely.

---

## 2.6 Competitive sorption design

**[AMENDED v2 — terminology corrected.]** v1 §8.4 and §6 label the 50/50/50 mg L⁻¹ run
**"equimolar"**. It is not. Phase 4 answer Q1 confirms the composition was equal-**mass** as written.
The term "equimolar" is **struck throughout** and replaced with **"equal-mass ternary"**.
*Justification:* audit **B3**, amendment **A-09**, now closed. The molar-deficit argument stands and
the Stage-1 outline's abstract is correct as published.

### Composition, in both units [NEW v2 presentation — Table 2.3]

**Equal-mass ternary**

| Metal | mg L⁻¹ | mmol L⁻¹ | Molar ratio to Pb |
|---|---|---|---|
| Pb(II) | 50 | 0.2413 | 1.00 |
| Cu(II) | 50 | 0.7868 | **3.26 ×** |
| Zn(II) | 50 | 0.7648 | **3.17 ×** |
| combined competitors | 100 | 1.5516 | **6.43 ×** |

**Minority-target ternary — [AMENDED v2] promoted to the headline competitive condition** (Phase 4
answer Q3)

| Metal | mg L⁻¹ | mmol L⁻¹ | Molar ratio to Pb |
|---|---|---|---|
| Pb(II) | 25 | 0.1207 | 1.00 |
| Cu(II) | 100 | 1.5736 | **13.04 ×** |
| Zn(II) | 100 | 1.5295 | **12.68 ×** |
| combined competitors | 200 | 3.1031 | **25.71 ×** |

A 4:1 mass and ~13:1 per-metal molar disadvantage — four times more adverse than the equal-mass run.
Leading §4.4 and Fig 4.7 with the most adverse condition answers "did you load the deck?" before it
is asked.

### Procedure [UNCHANGED]
1. 50 mL of the ternary solution prepared at the operating pH.
2. **Before adding sorbent, a 5 mL aliquot withdrawn and the actual initial concentration of all
   three metals measured.** Nominal values are not assumed. *(This matters: audit D.1 shows the
   outline's α values were computed against nominal C₀ = 50 mg L⁻¹, so recomputation against the
   measured initials will shift them.)*
3. 0.1 g TA-OSS added, stirred 120 min, filtered through 0.45 µm, all three residual metals measured.
   **n = 3.**
4. One parallel flask with 0.1 g RAW-OSS as the control, for each composition.
5. **The spent sorbent from the equal-mass ternary was retained** under DI water in sealed vials for
   the batch regeneration of §2.8.1.

Each ternary sample is aspirated three times, once per lamp.

### 2.6.1 Definition of the selectivity factor [UNCHANGED — verified]

> **α(Pb/M) = (q_Pb · C_e,M) / (q_M · C_e,Pb) = K_d,Pb / K_d,M**,  where **K_d = q_e / C_e** (L g⁻¹)

**[NEW v2] Two properties to state explicitly in the report**, because both pre-empt an objection:

1. The form used here is **algebraically identical** to the Bible's α(Pb/M) = (q_Pb/C_e,Pb)/(q_M/C_e,M).
   Verified in audit B10.16.
2. **α is invariant to whether q and C are expressed on a mass or a molar basis**, because the molar
   mass cancels in the ratio. **The headline selectivity numbers are therefore not a unit artefact.**
   This is worth one sentence in §4.4 and it disarms attack **A23** at the point of definition.

### 2.6.2 Basis of reporting — mass and mole [NEW v2]
*Justification:* audit **B10.2**, amendment **A-16**; attack **A23**.

Capacities are reported in **mg g⁻¹ and mmol g⁻¹ throughout**, side by side, in Table 4.3 and
Table 4.5. **On a molar basis the capacity ordering inverts**, and the report says so in a dedicated
paragraph in §4.2 rather than leaving it to be discovered. Three consequences are binding:

- No sentence claims that the **capacities** invert the Irving–Williams ordering. On a molar basis
  they do not.
- No unqualified sentence says the sorbent "preferentially captures lead". It captures a larger
  **fraction** of the lead present, not a larger **quantity**. Every such sentence names the basis.
- **The DFT binding free energies are never compared against mg g⁻¹ capacities.** ΔG_bind is a
  per-site molar quantity; its experimental counterpart is ΔΔG = −RT ln α (§4.6.3, Table 4.9).

---

## 2.7 Fixed-bed column operation

### 2.7.1 Column and bed [UNCHANGED]
Borosilicate chromatography column, **internal diameter 10 mm**, length 250 mm, PTFE frit at base,
adjustable PTFE top adapter. Two units: **Column A** for the single-metal Pb cycles, **Column B**
for the ternary run. Peristaltic pump, 0.1–10 mL min⁻¹. PTFE tubing on the 0.1 M HCl line;
Tygon/Norprene (1.6 mm ID) for feed and rinse.

**Design basis [AMENDED v2 — labelled].** The v1 §5.4.3 table of expected breakthrough
(BV_sat ≈ 167, BV₁₀ ≈ 117, EF ≈ 56× at 100 mg L⁻¹) is a **PLANNING ESTIMATE, SUPERSEDED BY
MEASUREMENT**. *Justification:* audit **B4**, amendment **A-08**. It is reproduced in the report only
if the shortfall is being discussed, and never as a prediction the data confirmed. The v1 arithmetic
is itself correct (audit D.5 verified BV_sat = 33 × 0.5 / 0.1 = 165); it is the input assumption of
q* ≈ 33 mg g⁻¹ under dynamic conditions that the measurement contradicts.

### 2.7.2 Packing and bed characterisation [UNCHANGED]
1. 1 cm plug of acid-washed glass wool above the frit.
2. **4.0 g of TA-OSS** (0.50–1.00 mm) wet-packed as a DI slurry, added in increments with gentle
   tapping to settle; trapped air and channels avoided. 0.5 cm glass-wool plug on top; adjustable
   adapter seated directly on the bed with no headspace.
3. Settled bed height measured. V_bed = A × height with A = π(0.5 cm)² = 0.785 cm²; cross-checked by
   water displacement where feasible.
4. ρ_b = m/V_bed and H:D computed. **BV ≡ V_bed in mL.**

**Every bed-volume figure in the report depends on the measured V_bed.** Recorded per column per
cycle: ρ_b, V_bed, bed height, H:D. Expected ρ_b ≈ 0.45–0.55 g cm⁻³, bed height ≈ 9–11 cm,
H:D ≈ 9:1 to 11:1, D_c/d_p ≈ 10–20.
`\TODOPAL{Q15 — measured bed height, V_bed, rho_b and H:D for each column and each cycle}`

### 2.7.3 Pre-conditioning [UNCHANGED]
5 BV of DI water at the operating pH downflow at 8 BV h⁻¹; effluent pH confirmed stable within ±0.3
of the inlet before the service run.

### 2.7.4 Service run and breakthrough [UNCHANGED]
Feed **100 mg L⁻¹ Pb**, single metal, at the operating pH, **8 BV h⁻¹ downflow** (≈ 1.0 mL min⁻¹ for
an ~8 mL bed; EBCT ≈ 7.5 min — audit D.5 verified both). Effluent fractions collected every 0.5 BV
for the first 10 BV, then every 2 BV until C/C₀ ≈ 0.5, then every 5 BV until C/C₀ ≥ 0.90. Volume and
cumulative BV recorded for each fraction; each fraction analysed for Pb, prioritising the
breakthrough region.

Metrics: **BV₁₀, BV₅₀, BV₉₀** from the curve; dynamic column capacity
q_col = [∫(C₀ − C) dV] / m by numerical integration.

### 2.7.5 Regeneration, rinse and cycling [UNCHANGED]
Feed stopped and column drained to just above the bed. **≈ 3 BV of 0.1 M HCl counter-current
(upflow) at 4 BV h⁻¹** (~45 min), collected as a pooled sample or in 0.5 BV fractions where time
permitted. Pb measured in the regenerate (also Cu and Zn for Column B).

> **D (%) = (mass desorbed / mass adsorbed in the prior service run) × 100**
> **EF = C_Pb,regenerate / C_Pb,feed**

Rinsed with DI water (pH ≈ 5) downflow at 8 BV h⁻¹ until outlet pH returned to within ±0.3 of the
service pH. Cycles 2 and 3 repeated identically; per-cycle BV₁₀ is the retention metric,
R_col (%) = BV₁₀(cycle n)/BV₁₀(cycle 1) × 100.

**[NEW v2] Consequence of early termination, to be stated.** Cycles 2 and 3 were permitted to
terminate at C/C₀ ≈ 0.30. Where this was done, BV₁₀ remains measurable but **q_col by integration
exists only for cycle 1**, and the loading before each regeneration differs between cycles, so the
per-cycle enrichment factors are **not directly comparable**. `\TODOPAL{Q17 — were cycles 2 and 3
actually terminated early?}`

**[NEW v2] Mass balance.** *Justification:* audit **B10.8**, amendment **A-11**; attack **A27**.

> **Pb fed = Pb in the pooled effluent + Pb in the regenerate + Pb remaining on the bed**

All three terms are already measured or measurable. The closure percentage is reported in §4.8. A
closure of 95–105% is a strong and nearly free authenticity signal; a closure of 70% is itself an
important finding and is reported as one.

### 2.7.6 Column B and end-state characterisation [UNCHANGED]
Column B packed identically (4.0 g TA-OSS, characterised as in §2.7.2), pre-conditioned, and fed the
**equal-mass ternary at 50 mg L⁻¹ each** at the operating pH, downflow at 8 BV h⁻¹. Fractions
collected on the same schedule and **all three metals** measured in a representative subset;
continued until Pb reached C/C₀ ≥ 0.90. Any transient overshoot (C/C₀ > 1) of Cu or Zn recorded as
measured — **it is the signature of competitive displacement by Pb, not an error.** Regenerated once
and all three metals measured in the pooled regenerate.
`\TODOPAL{Q16 — did Column B run at all? Were all three metals measured per fraction, and was Cu/Zn
overshoot observed?}`

After the final cycle the column was unpacked, a portion of the spent TA-OSS dried at 50 °C and its
FTIR spectrum recorded (the third FTIR sample of §2.4.1). The column was photographed at packing,
mid-breakthrough and post-regeneration, and the spent sorbent photographed.

---

## 2.8 Regeneration and recovery

### 2.8.1 Batch regeneration cycling [AMENDED v2 — cycle 1 defined]
Spent TA-OSS from the **equal-mass ternary** experiment, three cycles in triplicate, using three
separate 0.1 g aliquots so that each cycle is n = 3.

- **Stage A — desorption (30 min).** 0.1 g spent sorbent in 50 mL of 0.1 M HCl, stirred 30 min,
  filtered; Pb, Cu and Zn measured in the acid filtrate.
- **Stage B — wash and dry (~1.5 h).** Three 50 mL DI washes; dried at 50 °C for ~1 h.
- **Stage C — re-adsorption (120 min).** Regenerated sorbent placed in fresh 50 mL of 50 mg L⁻¹ Pb at
  the operating pH, stirred 120 min, filtered, residual Pb measured.

**[AMENDED v2] Definition of cycle 1.** v1 gave R(%) = q_e(cycle n)/q_e(cycle 1) without defining
cycle 1. Because the material is **ternary-loaded** but Stage C re-adsorbs from **single-metal Pb**,
taking "cycle 1" to mean the original ternary uptake would compare two different quantities.
*Justification:* audit **B10.7**, amendment **A-15**; attack **A30**.

> **Cycle 1 is the first single-metal Pb re-adsorption following the initial desorption.** The
> initial ternary loading is reported separately, as the source of the first desorbate, and is not
> used as a retention denominator.

`\TODOPAL{Q23 — is the reported 80.1% retention the batch q_e retention or the column BV_10
retention? And what denominator was actually used?}`

Reported: desorption efficiency D(%), capacity retention R(%), and cumulative recovery from the
pooled desorbates.

### 2.8.2 Failed eluents [NEW v2 — source outstanding]
v1 screened one eluent. `\TODOPAL{Q11 — was any other eluent tried and abandoned? Reporting a
rejected eluent with its reason is evidence of competence; a silently absent one is what referees
hunt for.}`

---

## 2.9 Speciation calculations [NEW v2]
Absent from v1 entirely. *Justification:* audit **B9**, amendment **A-06**; attack **A07**. This is
**computed, not measured**, and therefore requires no bench time — making it the cheapest available
armour in the project, and the only remaining defence against **A22** now that the sorbent-free
ternary blank is confirmed absent.

| Field | Specification |
|---|---|
| System | Pb(II) under the **exact** ionic conditions of each experiment — not a generic Pb–water diagram |
| Aqueous species | Pb²⁺, PbOH⁺, Pb(OH)₂(aq), Pb(OH)₃⁻, Pb(OH)₄²⁻, Pb₂OH³⁺, Pb₃(OH)₄²⁺, PbNO₃⁺, Pb(NO₃)₂(aq), **PbSO₄(aq)**, PbCl⁺, PbCl₂(aq) |
| Solids tested | **Pb(OH)₂(s)**, **PbSO₄(s) anglesite**, PbO, and Pb₃(CO₃)₂(OH)₂ hydrocerussite (relevant if solutions were open to air — state whether they were) |
| Output | Fractional speciation vs pH 2–10 with pH 5.0 marked (**Fig 2.4**), **and a saturation-index table** SI = log(IAP/K_sp) for every solid at every experimental condition (**Appendix G**) |
| Conditions covered | Each pH of the optimisation series; each isotherm C₀, especially 300 mg L⁻¹ where risk is greatest; **both ternary compositions**; the 100 mg L⁻¹ column feed |
| T and I | 298.15 K; ionic strength computed from the actual composition; **Davies equation** activity corrections, named in the report |
| Implementation | `phreeqpython` with a named database (`minteq.v4.dat` preferred); otherwise a hand-rolled solver over a stated, cited constant set. **Every equilibrium constant cited to a source** — an uncited constant is as bad as an uncited fact |

**Interpretation rule, fixed in advance so the result cannot be massaged:** SI < 0 → undersaturated,
precipitation impossible. **0 < SI < 1 → supersaturated but plausibly kinetically inhibited at these
concentrations and timescales; reported and defended.** SI > 1 → precipitation is a live confounder
and the result is qualified.

**Known outcome to be reported, not buried:** the equal-mass ternary computes to **SI ≈ +1.0** with
respect to anglesite (activity-corrected; audit B10.1) and the minority-target ternary to **≈ +1.3**.
A secondary consequence also to be computed and reported: sulfate complexation forms CuSO₄(aq) and
ZnSO₄(aq), lowering the **free-ion** activity of the two competitors while Pb²⁺ remains largely
uncomplexed in its nitrate matrix. **This cuts in favour of the project's argument** — the
competition ran at conditions more adverse to Pb than the nominal molarity indicates — but it is
computed and stated rather than left for the referee to notice.

---

## 2.10 Data analysis and model fitting [AMENDED v2]

**[AMENDED v2] All fitting is non-linear regression.** The linearised forms tabulated in v1 §11 —
Langmuir as C_e/q_e vs C_e, Freundlich as log q_e vs log C_e, pseudo-second-order as t/q_t vs t —
are **superseded in full**. *Justification:* audit **B2**, amendment **A-02**; attack **A08**; Bible
anti-pattern 4. **Linearising transforms the error structure**: rearranging the Langmuir equation to
C_e/q_e places C_e on both axes and weights the high-concentration points by 1/C_e², systematically
distorting q_max and K_L while *inflating* R². The report cites **Tran et al. 2017** (already
reference [7] of the outline) and states that linearised transformations were avoided for this
reason.

Implementation: `lmfit`, Levenberg–Marquardt with a differential-evolution pre-pass where the
parameter surface is awkward. **Reported for every model:** parameter values with **95% confidence
intervals**, R², **reduced χ²**, **RMSE**, and **AIC** for model discrimination.

### Models fitted [AMENDED v2 — set extended]
*Justification:* audit **B10.15**, amendment **A-12**. All are additional analysis of existing data
and cost no bench time.

| Class | v1 models | **Added in v2** |
|---|---|---|
| Isotherm | Langmuir, Freundlich | **Sips**, **Redlich–Peterson**; **R_L separation factor** |
| Kinetic | pseudo-first-order, pseudo-second-order, Weber–Morris | **Elovich** |
| Column | *(none)* | **Thomas**, **Yoon–Nelson**, **Adams–Bohart** |

**Caveat to state:** a three-parameter Sips or Redlich–Peterson fit to a **four-point** Cu or Zn
isotherm is over-parameterised. Either report it with that caveat explicit, or restrict the
three-parameter models to the six-point Pb isotherm. Fitting three parameters to four points and
reporting the R² without comment is exactly the kind of thing the Tran et al. review criticises.

**[NEW v2] Appendix comparison: linearised versus non-linear.** *Justification:* audit **B2**,
recommended and accepted. A short appendix table fitting the Pb isotherm both ways, showing the
divergence in q_max and K_L and the fact that the linearised fit's R² appears *better* while its
parameters are *worse*. Roughly two hours of work. It converts a cited paper into a reproduced
result, demonstrates command of the point rather than compliance with it, and closes attack **A08**
so completely the referee cannot raise it.

### Derived quantities [UNCHANGED unless noted]

| Quantity | Definition |
|---|---|
| Removal | (C₀ − C_e)/C₀ × 100 |
| Equilibrium capacity | q_e = (C₀ − C_e)V/m |
| Time-point capacity | q_t = (C₀ − C_t)V/m |
| Distribution coefficient | K_d = q_e/C_e |
| Selectivity factor | α(Pb/M) = (q_Pb·C_e,M)/(q_M·C_e,Pb) = K_d,Pb/K_d,M |
| Separation factor | β_i/j = K_d,i / K_d,j |
| Desorption efficiency | D(%) = (mass desorbed / mass adsorbed) × 100 |
| Batch capacity retention | R(%) = q_e(cycle n)/q_e(cycle 1) × 100 **[cycle 1 defined in §2.8.1]** |
| Tannin loading | (m_func − m_raw,eq)/m_raw,eq × 100 |
| Residual mineral | m_ash/m_dry × 100 |
| Packed-bed density | ρ_b = m/V_bed |
| Empty-bed contact time | EBCT = V_bed/Q = 1/(BV per hour) |
| Breakthrough bed volume | BV_x at C/C₀ = x, for x = 0.10, 0.50, 0.90 |
| Dynamic column capacity | q_col = (1/m)∫₀^V_exh (C₀ − C) dV |
| Column capacity retention | R_col(%) = BV₁₀(cycle n)/BV₁₀(cycle 1) × 100 |
| Enrichment factor | EF = C_Pb,regenerate / C_Pb,feed |
| **Mass balance closure [NEW v2]** | **(Pb_effluent + Pb_regenerate + Pb_on bed) / Pb_fed × 100** |
| **Galloyl site balance [NEW v2]** | mmol metal captured per mmol galloyl, from the measured loading and M(tannic acid) = 1701.2 with 10 galloyl groups per molecule |

**[NEW v2] "Expected" notes relabelled.** *Justification:* audit **B10.9**, amendment **A-13**;
attack **A28**. v1 carries an "Expected" note in almost every section, and §5.4.3 sized the column
using "a representative monolayer capacity of order 40 mg/g (the value this system is expected to
deliver)". These are **acceptance criteria and planning bases, not predictions**, and the report does
not reproduce them as predictions the data confirmed. If the closeness of the 40 mg g⁻¹ planning
figure to the measured capacity is ever raised, the answer is that the design was sized from a
literature-typical capacity — a defensible answer only if it is given first.

---

## Amendment index

| ID | Amendment | Section | Source |
|---|---|---|---|
| A-01 | TGA and BET designed out; six-line replacement evidence set | 2.4.0 | audit B5 |
| A-02 | All fitting non-linear; v1 §11 linearised forms superseded | 2.10 | audit B2 |
| A-03 | XPS and SEM-EDX added as full subsections | 2.4.2, 2.4.3 | audit B6 |
| A-04 | Quantified leaching test mandatory | 2.4.6 | audit B7 |
| A-05 | LOD, LOQ and spike recovery added | 2.5.2 | audit B8 |
| A-06 | Computed speciation with saturation indices | 2.9 | audit B9 |
| A-07 | Temperature series specified as a required dataset | 2.5.7 | audit B1 |
| A-08 | Column planning estimates labelled superseded | 2.7.1 | audit B4 |
| A-09 | "Equimolar" corrected to "equal-mass ternary" — **CLOSED, Q1(a)** | 2.6 | audit B3 |
| A-10 | Sorbent-free blanks required — **NOT RUN; accepted risk, Q2(b)** | 2.5.3 | audit B10.3 |
| A-11 | Mass balance added to the column work | 2.7.5 | audit B10.8 |
| A-12 | Sips, Redlich–Peterson, Elovich, Thomas, Yoon–Nelson, Adams–Bohart added | 2.10 | audit B10.15 |
| A-13 | "Expected" notes relabelled acceptance criteria | 2.10 | audit B10.9 |
| A-14 | §2.2 retitled "Source and conditioning"; Fig 2.1 redefined; novelty claim 1 reworded | 2.2 | audit B10.6, Q5 |
| A-15 | Batch regeneration cycle 1 defined as the first single-metal re-adsorption | 2.8.1 | audit B10.7 |
| A-16 | mg g⁻¹ and mmol g⁻¹ carried throughout; molar inversion confronted in §4.2 | 2.6.2 | audit B10.2 |
| A-17 | Wash endpoint quantitative (276 nm) rather than visual | 2.3.2 | audit B10.11 |
| A-18 | Grafting chemistry stated, with honest limits on what was demonstrated | 2.3.1 | audit Table A |
| A-19 | Minority-target ternary promoted to the headline competitive condition | 2.6 | Q3(a) |
