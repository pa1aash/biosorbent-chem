<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# 00 — BUILD SPECIFICATION

The Report Bible (`YHSA_Asia_Winning_Report_Bible.md`) distilled into a greppable, machine-actionable
build spec. This file is the **authority on what the report must be**. Where this file and the Bible
disagree, the Bible wins and this file is a bug.

**Amendments.** This file is a faithful extraction of the Bible and is not edited to reflect project
reality. Where project reality departs from the Bible — instruments unavailable, protocol errors,
superseded methods — the departure is ruled on in [`02_PROTOCOL_AUDIT.md`](02_PROTOCOL_AUDIT.md) and
recorded in the amendment log at the foot of this file. `STATUS` cells in the registries below are
updated to point at the ruling.

| | |
|---|---|
| Registration number | Chem-151 |
| Deadline | 17 August 2026, 23:59 HKT = **21:29 IST 17 Aug 2026**. Target 16 August. |
| Today | 11 August 2026 |
| Stage | 2 — referee assessment; ≥2 anonymous referees, 6 of the 7 criteria |
| Field | ~57 Chemistry teams → ≤10 oral defence slots → ≤5 awards. No Chemistry Gold in 2024 or 2025. |

---

## 1. MANDATORY CONTENT BLOCKS — EXACT REQUIRED ORDER

From Bible §2.2 (rules requirement) reconciled with §6 (convergent winner template). The order is
not negotiable and is not a place to innovate.

| # | Block | Page | Requirement |
|---|---|---|---|
| M1 | **Cover page** | unnumbered | Team member name(s), school, city, country; supervising teacher name, position, school/institution, city, country; **registration number**; title of report; date. Layout per Bible §14.1. |
| M2 | **Title (repeated) + author line + ABSTRACT + KEYWORDS** | i | Abstract **must not exceed one page**. Keywords 5–8. |
| M3 | **Acknowledgement** | ii | *All* assistance and contribution received, **plus** the four declarations of §4 below. |
| M4 | **Commitments on Academic Honesty and Integrity** | iii | Official 2026 form, signed by team member(s), supervising teacher, **and school principal**. |
| M5 | **Table of Contents** | iv | Three levels, dot leaders, page numbers. |
| M6 | List of Figures | v | Not required by the rules; included — 20+ figures makes it materially navigable. |
| M7 | List of Tables | vi | As M6. |
| M8 | List of Abbreviations and Symbols | vii | As M6; Bible §12 requires it above ~15 abbreviations. |
| M9 | **Section I — Introduction** | 1… | |
| M10 | **Section II — Experimental / Methodology** | | |
| M11 | **Section III — Computational Methodology** | | |
| M12 | **Section IV — Results and Discussion** | | |
| M13 | **Section V — Conclusion and Future Work** | | |
| M14 | **Appendix** | | A–J per §7 below. |
| M15 | **References** | | Clear citations for all existing methods and conclusions. 35–60 entries. |
| M16 | Supplementary documents as applicable | separate | Experiment videos, text/graphic materials, **AI chat records**. Zip with the PDF or supply a download link. |

**Pagination.** Front matter lower-case Roman (i, ii, iii, iv…); body Arabic restarting at 1.
**Running header on every page:** `Research Report` (left) · `2026 S.T. Yau High School Science Award (Asia)` (right).
**Numbering.** Sections in Roman numerals. Subsections decimal, tied to section number (2.1, 2.3.1).
Figures and tables **numbered by section** — Figure 4.3, Table 4.2.

---

## 2. COMPLIANCE CONSTRAINTS AS CHECKABLE ASSERTIONS

Each row is an assertion that must evaluate TRUE before submission. `scripts/check_compliance.py`
prints a PASS/FAIL table against these IDs.

| ID | Assertion | Check method | Severity |
|---|---|---|---|
| **C-001** | Page size is A4 (595 × 842 pt, 210 × 297 mm) on every page | `pdfinfo` → `Page size` | disqualification risk |
| **C-002** | Margins ≥ 2.5 cm on **all four** sides | `geometry` package setting, loaded after the JINST style so it wins; visual check | disqualification risk |
| **C-003** | Body text at 1.5 line spacing (or double) | `\onehalfspacing` applied to body | disqualification risk |
| **C-004** | Single spacing appears **only** in quotations, footnotes, references and captions | `\singlespacing` scoped to those environments only | disqualification risk |
| **C-005** | Submission is **ONE single PDF file** | count of files in `admin/submission/` for the report body = 1 | disqualification risk |
| **C-006** | Filename is exactly `Chem-151-Research Report.pdf` | string equality, including the single space and the hyphens | disqualification risk |
| **C-007** | Language is English throughout | manual | disqualification risk |
| **C-008** | Sent to `yauaward@ashk.org.hk` | correspondence record in `admin/correspondence/` | disqualification risk |
| **C-009** | If the bundle exceeds 5 MB it is sent as a **download link**, not an attachment | `du -h`; warn above 5 MB | disqualification risk |
| **C-010** | Submitted before 17 Aug 2026 23:59 HKT = 21:29 IST | sent-mail timestamp | disqualification risk |
| **C-011** | Abstract occupies **at most one page** | page-break position of `abstract.tex` | high |
| **C-012** | All fonts embedded | `pdffonts` → every font shows `emb yes` | high |
| **C-013** | Numbered body pages fall in the **42–55** band | `check_compliance.py` page arithmetic | high |
| **C-014** | Cover page carries all Bible §14.1 fields including the registration number | manual against template | disqualification risk |
| **C-015** | Commitments page bears **three** signature parties: team member, supervising teacher, school principal | visual on the scanned insert | disqualification risk |
| **C-016** | Commitments form is the **2026** version (contains the new AI clause, item 5) | compare against `admin/official/` original | disqualification risk |
| **C-017** | Signature scan is ≥ 300 dpi and not photographed at an angle | image metadata + visual | medium |
| **C-018** | AI declaration states, for every tool: **name and version**, **stages and purposes**, **timing and frequency** | generated from `logs/ai_use_log.csv` | disqualification risk |
| **C-019** | AI chat records are attached as Appendix A | file present in bundle | disqualification risk |
| **C-020** | Supervising teacher's **prior** written approval of AI use exists and predates submission | `admin/correspondence/` | disqualification risk |
| **C-021** | Prior-and-concurrent-submission declaration is present and explicit either way | grep the Acknowledgement | disqualification risk |
| **C-022** | Instrumentation/facility declaration names every instrument not personally operated and every operator | grep the Acknowledgement | high |
| **C-023** | Compute declaration states where DFT ran and who set it up | grep the Acknowledgement | medium |
| **C-024** | Commercial-interaction declaration present; no profit-making training/education institution engaged | grep the Acknowledgement | disqualification risk |
| **C-025** | No part of the research was executed by a university/institute researcher on the team's behalf | manual | disqualification risk |
| **C-026** | Similarity below 10% | school plagiarism tool | disqualification risk |
| **C-027** | Reference count in the range **35–60** | count `library.bib` entries cited | high |
| **C-028** | **Every** DOI resolves against Crossref and matches on title/authors/year/volume/pages | `scripts/verify_dois.py`, exit 0 | disqualification risk |
| **C-029** | Every cited work has been read by the author (at minimum abstract and figures) | `read_confirmed` column of `refs/VERIFICATION_LOG.csv` | high |
| **C-030** | Zero surviving `\PENDING`, `\NEEDSDATA`, `\TODOPAL`, `TODO`, `XX`, `TBD` in the final build | `scripts/check_placeholders.py`, exit 0 | high |
| **C-031** | No numeric result is hard-coded in any `.tex` file; all arrive via `\num{key}` | `scripts/check_numbers.py` | high |
| **C-032** | Every headline number is **identical** in abstract, results and conclusion | `scripts/check_numbers.py` consistency audit | high |
| **C-033** | Figures ≥ 300 dpi; every axis labelled with quantity **and** unit | `figures/STYLE.md` enforced in `analysis/src/style.py` | medium |
| **C-034** | Pb, Cu and Zn each have **one** colour, unvarying across the whole document | `analysis/src/style.py` single source | medium |
| **C-035** | Capacities reported in **mg/g and mmol/g**; energies in **kJ/mol** throughout | `check_numbers.py` unit audit | medium |
| **C-036** | No use of "significantly" without an accompanying p-value | `check_numbers.py` lint | medium |
| **C-037** | Three-level table of contents renders with dot leaders and page numbers | visual on built PDF | medium |
| **C-038** | No journal furniture (SISSA/IOP logo, PUBLISHED BY line, Received/Revised/Accepted block, DOI line, copyright line, article-ID footer) | grep the built PDF text layer | high |

---

## 3. PAGE AND WORD BUDGETS

### 3.1 Global (Bible §7.1)
**Target 42–55 numbered body pages**, plus front matter and appendices. Under-length signals thin
work; over 70 pages signals padding. This project has two full methodological arms where the 2025
Chemistry Silver (35 pp) had one.

### 3.2 Allocation (Bible §7.2)

| Block | Pages | Words | Note |
|---|---|---|---|
| Cover | 1 | — | Template exact |
| Abstract + keywords | 1 | 450–600 | **Must not exceed one page** |
| Acknowledgement (+ AI declaration) | 1–1.5 | 350–550 | AI declaration is most of it |
| Commitments (signed) | 1–2 | — | Official form |
| Table of contents | 1–2 | — | Three levels deep |
| **I. Introduction** | **6–8** | 2600–3600 | Includes literature review |
| **II. Experimental** | **6–8** | 2200–3000 | Heavy on figures/photos |
| **III. Computational Methodology** | **4–5** | 1600–2200 | Full reproducibility |
| **IV. Results and Discussion** | **20–26** | 7000–9500 | The core; ~55% of the body |
| **V. Conclusion and Future Work** | **3–4** | 1300–1800 | Numeric, structured |
| References | 3–4 | — | 35–60 entries |
| Appendices | 8–20 | — | Data, AI logs, spectra |

### 3.3 Results and Discussion sub-allocation (Bible §7.3) — the decisive block

| Subsection | Pages |
|---|---|
| 4.1 Synthesis and functionalisation confirmation | 4–5 |
| 4.2 Single-metal equilibrium: isotherms and capacities | 3–4 |
| 4.3 Kinetics and mechanism of uptake | 2–3 |
| 4.4 Binary/ternary competitive sorption and selectivity factors | 3–4 |
| 4.5 Thermodynamics (ΔH°, ΔS°, ΔG°) — the entropy-driven signature | 2 |
| 4.6 DFT: geometries, binding free energies, ordering reproduction | 3–4 |
| 4.7 EDA + NOCV: falsifying the electrostatic explanation | 3–4 |
| 4.8 Fixed-bed column and regeneration/recovery | 2–3 |
| 4.9 Benchmarking against literature | 1–2 |

### 3.4 Figure and table counts
**Target 20–26 figures and 12–16 tables.** Current registry: **24 figures** (4.3 designed out, 4.18 added) and **18 tables** (4.13, 4.14 added). The table count sits two above the Bible's band; the overage is deliberate and both additions carry load-bearing evidence. Every figure needs a caption understandable without the
body text.

---

## 4. THE FOUR MANDATORY DECLARATIONS

All four are explicit paragraphs in the Acknowledgement (page ii). None may be implied.

1. **Prior and concurrent submission.** Concurrent submission to another competition means the
   report is **not accepted**. Past submission is allowed **only if declared**. Undeclared past
   submission → disqualification. State it either way, verbatim.
2. **Facility and assistance.** Name every instrument not personally operated, every facility that
   ran a measurement, every person who advised, and exactly who operated each technique.
   Under-declaring is a disqualification risk; over-declaring costs nothing.
3. **Compute.** Where the DFT ran (school machine / cloud tier / rented instance / borrowed
   hardware) and who set it up.
4. **AI usage.** Per Bible §3.4: names and versions of every tool; specific stages and purposes;
   timing and frequency. Plus the explicit negative statement of what AI was *not* used for, and a
   pointer to the Appendix A chat records. Governing principle: **assistance rather than
   substitution**.

**Prohibited AI use (Bible §3.3):** ghost-writing the main body · generating fabricated literature ·
falsifying experimental data · failing to declare usage · uploading confidential or unauthorised data.

---

## 5. REPORT SKELETON (Bible §20) — NUMBERED TREE

```
COVER PAGE                                                          [Bible §14.1]

  i    Title / Author / Abstract / Keywords
  ii   Acknowledgement          [AI · facility · prior-submission · commercial declarations]
  iii  Commitments on Academic Honesty and Integrity   [official form, 3 signatures]
  iv   Table of Contents
  v    List of Figures
  vi   List of Tables
  vii  List of Abbreviations and Symbols

SECTION I — INTRODUCTION                                                  6–8 pp
  1.1  Trace Pb(II) in mixed-metal aqueous streams                       0.75–1 pp
  1.2  The Irving–Williams trap in non-specific biosorbents              1–1.5 pp
  1.3  Existing research                                                 2–2.5 pp
       1.3.1  Polyphenol and tannin sorbents for divalent metals
       1.3.2  Collagen and ossein scaffolds
       1.3.3  Pb(II) coordination and the stereochemically active 6s² lone pair
       1.3.4  Computational treatment of metal–polyphenol binding
  1.4  Hypothesis, aim and original contributions        [NOVELTY BOX]    1 pp
  1.5  Structure of this report                                          0.25 pp

SECTION II — EXPERIMENTAL                                                 6–8 pp
  2.1  Materials                                          [Table 2.1]
  2.2  Preparation of ossein from fish scales             [Fig 2.1 photo series]
  2.3  Galloyl functionalisation with tannic acid         [Fig 2.2 scheme]
       2.3.1  Grafting protocol
       2.3.2  Quantification of galloyl loading
       2.3.3  Conditions screened and rejected
  2.4  Characterisation                                   [Table 2.2 instruments]
       2.4.1  ATR-FTIR
       2.4.2  SEM and SEM-EDX
       2.4.3  TGA                                         [see amendment A-01]
       2.4.4  Surface area and porosimetry                [see amendment A-01]
       2.4.5  Point of zero charge
       2.4.6  XPS
  2.5  Batch sorption protocols                           [Fig 2.4 speciation]
       2.5.1  Solution preparation and pH control
       2.5.2  Elemental analysis and quality control
       2.5.3  Controls, blanks and replication
  2.6  Competitive sorption design                        [Table 2.3 mg/L and mmol/L]
       2.6.1  Definition of the selectivity factor
  2.7  Fixed-bed column operation                         [Fig 2.5 schematic]
  2.8  Regeneration and recovery

SECTION III — COMPUTATIONAL METHODOLOGY                                   4–5 pp
  3.1  Cluster model construction and truncation
  3.2  Level of theory, basis sets and relativistic treatment   [Table 3.1]
  3.3  Thermochemistry and reference state
  3.4  Energy decomposition and NOCV analysis
  3.5  Geometric descriptors of hemidirection
  3.6  Validation of the computational protocol

SECTION IV — RESULTS AND DISCUSSION                                     20–26 pp
  4.1  Confirmation of galloyl functionalisation   [Figs 4.1–4.4; Table 4.1]   → FINDING 1
  4.2  Single-metal sorption equilibria            [Fig 4.5; Tables 4.2, 4.3]
  4.3  Sorption kinetics and rate-limiting step    [Fig 4.6; Table 4.4]
  4.4  Competitive sorption and selectivity        [Fig 4.7; Table 4.5]        → FINDING 2
  4.5  Sorption thermodynamics                     [Fig 4.8; Table 4.6]        → FINDING 3
  4.6  DFT binding free energies                   [Fig 4.10; Tables 4.7, 4.9]
       4.6.1  Optimised coordination geometries
       4.6.2  Reproduction of the experimental ordering
       4.6.3  Comparison of computed and experimental free-energy differences
                                                                              → FINDING 4
  4.7  Energy decomposition and the origin of selectivity
       4.7.1  Failure of the purely electrostatic rationale   [Fig 4.11; Table 4.8]
       4.7.2  Orbital covalency and the Pb 6p acceptor manifold  [Fig 4.12]
       4.7.3  Hemidirected accommodation of the 6s² lone pair   [Fig 4.13]
       4.7.4  Desolvation penalties and the entropic signature  [Table 4.10]
       4.7.5  A unified mechanistic picture                     [Fig 4.9 MASTER]
                                                                              → FINDING 5
  4.8  Fixed-bed performance and metal recovery    [Figs 4.14–4.16; Table 4.11]
  4.9  Benchmarking against reported sorbents      [Table 4.12]

SECTION V — CONCLUSION AND FUTURE WORK                                    3–4 pp
  5.1  Summary of findings
  5.2  Unified mechanistic statement
  5.3  Limitations
  5.4  Future work
  5.5  Transferability of the design principle

APPENDIX
  A  AI tool usage records and log                            [MANDATORY, 2026 rules]
  B  Experimental data tables
  C  Calibration curves and analytical quality control
  D  Full spectra
  E  Computational supporting information (XYZ coordinates, energies, EDA/NOCV data)
  F  Representative input files
  G  Speciation calculations
  H  Notebook extracts and process photographs
  I  Experiment video
  J  Risk assessment and waste-handling protocol

REFERENCES                                     [35–60, ACS style, every DOI verified by hand]
```

### 5.1 Architecture rule for Section IV
**Each subsection = one claim = one figure or table = one closing verdict sentence that states what
has now been established.** Never leave a figure without a verdict. Implemented as the `\verdict{}`
macro; `check_placeholders.py` warns on any Results subsection lacking one.

---

## 6. FIGURE REGISTRY (Bible §9.1)

`STATUS` legend: `PENDING` (no data, no script) · `SCRIPTED` (script exists, awaiting data) ·
`DRAFTED` (rendered from partial data) · `FINAL` (rendered from VERIFIED data) ·
`DESIGNED-OUT` (removed, with a stated reason in the audit).

| ID | Title | Type | Purpose | Data source | Owning script | STATUS |
|---|---|---|---|---|---|---|
| 1.1 | Irving–Williams series with Pb(II) placed outside it | Schematic | Sets up the central problem visually on page 2 | literature (cited) | `figures/src/fig1_1_irving_williams.py` | PENDING |
| 1.2 | Holodirected vs hemidirected coordination geometry | Schematic | Makes the key concept concrete early | literature + own DFT geometries | `figures/src/fig1_2_holo_hemi.py` | PENDING |
| 2.1 | Fish scale → ossein → galloyl–ossein process flow, with real photographs | Photo series | Authenticity evidence | `figures/photos/` | `figures/src/fig2_1_process_flow.py` | PENDING |
| 2.2 | Tannic acid grafting reaction scheme | Chemical scheme | Shows command of the chemistry | drawn | `figures/schemes/` | PENDING |
| 2.3 | Photographs of the actual apparatus / student at work | Photo | Authenticity evidence (Bible Obs. 4) | `figures/photos/` | `figures/src/fig2_3_apparatus.py` | PENDING |
| 2.4 | Pb(II) speciation diagram vs pH with pH 5.0 marked | Computed plot | Pre-empts the hydrolysis objection (Attack 7) | `analysis/src/speciation.py` | `figures/src/fig2_4_speciation.py` | PENDING |
| 2.5 | Fixed-bed column and counter-current regeneration schematic | Schematic | Clarity | drawn | `figures/schemes/` | PENDING |
| 4.1 | ATR-FTIR overlay with annotated bands | Spectra | Functionalisation proof | `data/provided/characterisation/ftir/` | `figures/src/fig4_1_ftir.py` | PENDING |
| 4.2 | SEM before/after + EDX maps | Micrographs | Morphology and elemental confirmation | `data/provided/characterisation/sem_edx/` | `figures/src/fig4_2_sem_edx.py` | PENDING |
| 4.3 | ~~TGA overlay~~ | — | — | — | — | **DESIGNED-OUT** — instrument unavailable; amendment **A-01**, audit B5. Replaced by the six-line evidence set and by Fig 4.18. |
| 4.4 | pH_PZC determination plot | Plot | Justifies the pH choice | `data/provided/characterisation/ph_pzc/` | `figures/src/fig4_4_ph_pzc.py` | PENDING |
| 4.5 | Single-metal isotherms, three metals, functionalised vs control, non-linear fits with residuals | Plot | Core equilibrium data | `data/provided/batch/` | `figures/src/fig4_5_isotherms.py` | PENDING |
| 4.6 | Kinetic fits + Weber–Morris plot | Plot | Rate-limiting step | `data/provided/kinetics/` | `figures/src/fig4_6_kinetics.py` | PENDING |
| 4.7 | **Grouped bar chart: ternary removal % and α values, functionalised vs unfunctionalised, with error bars** | Plot | **The money figure** — the most persuasive image in the paper | `data/provided/competitive/` | `figures/src/fig4_7_selectivity.py` | PENDING |
| 4.8 | Van 't Hoff plot | Plot | Thermodynamics | `data/provided/thermodynamics/` | `figures/src/fig4_8_vant_hoff.py` | PENDING |
| 4.9 | **Master mechanism schematic** — galloyl pocket + Pb lone-pair void + NOCV donation arrow + desolvation cartoon + EDA bar comparison, one panel | Composite | **The single image that carries the thesis** | composite of own results | `figures/src/fig4_9_master.py` | PENDING |
| 4.10 | Optimised DFT geometries, Pb/Cu/Zn side by side, labelled | Structures | Computational core | `dft/structures/` | `figures/src/fig4_10_geometries.py` | PENDING |
| 4.11 | EDA stacked bar: ΔE_elstat, ΔE_orb, ΔE_Pauli, ΔE_disp for three metals + f_orb overlay | Plot | **The falsification figure** | `dft/analysis/` | `figures/src/fig4_11_eda.py` | PENDING |
| 4.12 | Deformation-density isosurfaces with channel energies | Isosurface plots | Localises the covalency | `dft/analysis/` | `figures/src/fig4_12_nocv.py` | PENDING |
| 4.13 | Hemidirection descriptor illustration with the void hemisphere shaded | Structure | Converts a claim into a measurement (Attack 14) | `analysis/src/hemidirection.py` | `figures/src/fig4_13_hemidirection.py` | PENDING |
| 4.14 | Breakthrough curve with Thomas / Yoon–Nelson fits | Plot | Process performance | `data/provided/column_A/`, `column_B/` | `figures/src/fig4_14_breakthrough.py` | PENDING |
| 4.15 | Elution profile showing the concentration factor | Plot | Recovery | `data/provided/column_A/` | `figures/src/fig4_15_elution.py` | PENDING |
| 4.16 | Three-cycle capacity retention bar chart with error bars | Plot | Durability | `data/provided/column_A/`, `regeneration/` | `figures/src/fig4_16_retention.py` | PENDING |
| 4.17 | Failed conditions gallery (rejected grafting ratios / failed eluents) | Photo/plot | Authenticity + competence (Bible Obs. 3) | `figures/photos/` | `figures/src/fig4_17_failed.py` | PENDING — source depends on the Phase 4 answer (audit B10.17) |
| 4.18 | **XPS high-resolution Pb 4f, O 1s, C 1s, N 1s with fitted components**, RAW-OSS / fresh TA-OSS / Pb-loaded TA-OSS | Spectra | **The strongest direct evidence of Pb–O coordination and oxidation state.** Added by amendment **A-03** | `data/provided/characterisation/xps/` | `figures/src/fig4_18_xps.py` | PENDING |

---

## 7. TABLE REGISTRY (Bible §9.2)

| ID | Title | Purpose | Data source | Owning script | STATUS |
|---|---|---|---|---|---|
| 2.1 | Reagents: grade and supplier | Reproducibility | `docs/EXPERIMENTAL_PROTOCOL_v2.md` | `tables/src/tab2_1_reagents.py` | PENDING |
| 2.2 | Instrument list with models and parameters | Reproducibility | protocol v2 + facility disclosure | `tables/src/tab2_2_instruments.py` | PENDING |
| 2.3 | Ternary composition in mg/L **and mmol/L** | Makes the molar disadvantage explicit (Attack 6) | `data/provided/competitive/` | `tables/src/tab2_3_ternary_composition.py` | PENDING |
| 3.1 | Full computational protocol: functional, basis, ECP, solvation, software + version, charge/multiplicity per species | Reproducibility; Attacks 1, 2, 3 | `dft/DFT_PROTOCOL.md` | `tables/src/tab3_1_protocol.py` | PENDING |
| 4.1 | FTIR band assignments with references | Evidence | `data/provided/characterisation/ftir/` + literature | `tables/src/tab4_1_ftir_bands.py` | PENDING |
| 4.2 | Langmuir / Freundlich / Sips parameters with R², χ²_red, RMSE, AIC — all metals, both sorbents | Rigour (Attack 8) | `data/processed/` | `tables/src/tab4_2_isotherm_params.py` | PENDING |
| 4.3 | q_max in mg/g **and mmol/g** | Chemical meaning — the molar ordering may narrow or change | `data/processed/` | `tables/src/tab4_3_qmax.py` | PENDING |
| 4.4 | Kinetic model parameters | Mechanism | `data/processed/` | `tables/src/tab4_4_kinetics.py` | PENDING |
| 4.5 | Removal % and α values, functionalised vs control, mean ± SD | Core claim | `data/processed/` | `tables/src/tab4_5_selectivity.py` | PENDING |
| 4.6 | Thermodynamic parameters at each T with uncertainties | Rigour | `data/processed/` | `tables/src/tab4_6_thermo.py` | PENDING |
| 4.7 | DFT energetics: ΔG_bind, ΔE_int, ΔE_prep, bond lengths, CN, hemidirection descriptor | Computational core | `dft/analysis/` | `tables/src/tab4_7_dft.py` | PENDING |
| 4.8 | Decomposition terms and f_orb per metal | Falsification | `dft/analysis/` | `tables/src/tab4_8_eda.py` | PENDING |
| 4.9 | **Computed ΔΔG vs experimental ΔΔG from α, with % deviation and explanation** | Validation (Bible Obs. 7; Attack 5) | `dft/analysis/` + `data/processed/` | `tables/src/tab4_9_validation.py` | PENDING |
| 4.10 | Hydration free energies used, with sources and convention | Pre-empts Attack 12 | literature (cited) | `tables/src/tab4_10_hydration.py` | PENDING |
| 4.11 | Column model parameters (Thomas, Yoon–Nelson, Adams–Bohart) | Process rigour | `data/processed/` | `tables/src/tab4_11_column_models.py` | PENDING |
| 4.12 | **Literature benchmark table** — 10–18 named published sorbents | Winner signature (Bible Obs. 2) | `refs/library.bib` + `data/processed/` | `tables/src/tab4_12_benchmark.py` | PENDING |
| 4.13 | XPS binding energies, assignments and fitted component areas | Direct coordination evidence; amendment **A-03** | `data/provided/characterisation/xps/` | `tables/src/tab4_13_xps.py` | PENDING |
| 4.14 | Tannic-acid leaching at pH 5 and pH 2, and the galloyl site balance | Answers Attack A10 with a number; amendment **A-04**; audit D.3 | `data/provided/characterisation/leaching/` | `tables/src/tab4_14_leaching.py` | PENDING |

---

## 8. REFEREE ATTACK SURFACE (Bible §11) — VERBATIM, WITH SEVERITIES

Live tracking in [`01_ATTACK_REGISTER.md`](01_ATTACK_REGISTER.md).

| # | Attack | Severity | Required armour |
|---|---|---|---|
| 1 | **"Which EDA/NOCV implementation? ETS-NOCV is an ADF method."** If the report says ORCA and ETS-NOCV in the same breath without explanation, credibility collapses. | 🔴 Critical | State software, version, and exact decomposition scheme. If ADF was used, say so and cite it. If ORCA + an external analyser, name the route precisely. |
| 2 | **"Was Cu(II) treated as open-shell doublet?"** | 🔴 Critical | State charge/multiplicity for every species in Table 3.1; report ⟨S²⟩. |
| 3 | **"Was a relativistic ECP used for Pb?"** | 🔴 Critical | Name the ECP (def2-ECP / SDD) or the all-electron relativistic treatment (ZORA/DKH). |
| 4 | **"Are these naked-ion binding energies?"** | 🔴 Critical | Recast as aquo-ligand exchange, or explicitly label the reference state and discuss its limits. |
| 5 | **"Computed ΔΔG (~35 kJ/mol) is an order of magnitude larger than experimental ΔΔG from α (~3 kJ/mol)."** | 🔴 Critical | Confront it in §4.6 with the intrinsic-site vs ensemble argument. Never let them find it first. |
| 6 | **"Is the selectivity a mass-vs-mole artefact?"** | 🟠 High | Tabulate molar concentrations; ideally run an equimolar ternary; discuss explicitly. |
| 7 | **"How do you know Pb didn't precipitate at pH 5?"** | 🟠 High | Speciation diagram + no-sorbent blank + saturation index calculation. |
| 8 | **"Were isotherms fitted by linearisation?"** | 🟠 High | Non-linear regression, report χ²/RMSE, cite Tran et al. |
| 9 | **"Where are the replicates and uncertainties?"** | 🟠 High | n stated everywhere; error bars on every plot; SD in every table. |
| 10 | **"Is the tannic acid grafted or just adsorbed?"** | 🟠 High | Leaching test: soak functionalised sorbent in blank at pH 5 and 2, measure released phenolics; combine with FTIR evidence. |
| 11 | **"How was 5.5 wt% measured?"** | 🟠 High | Give the assay and calibration curve. |
| 12 | **"Which hydration free-energy scale?"** Absolute single-ion values are convention-dependent. | 🟡 Medium | Cite the source and state the convention; better, use *relative* values. |
| 13 | **"f_orb is scheme-dependent — is the comparison valid?"** | 🟡 Medium | Acknowledge scheme-dependence; assert internal comparability under identical settings. |
| 14 | **"Is hemidirection asserted or measured?"** | 🟡 Medium | Report a numerical descriptor for all three metals. |
| 15 | **"What about competing hardness ions (Ca²⁺, Mg²⁺, Na⁺)?"** | 🟡 Medium | At minimum discuss; ideally one experiment. |
| 16 | **"Only 3 regeneration cycles?"** | 🟡 Medium | Acknowledge as a limitation; state the mechanism of the capacity loss with evidence. |
| 17 | **"Who ran the ICP/SEM/XPS?"** | 🟡 Medium | Full disclosure in the Acknowledgement; a rules requirement anyway. |
| 18 | **"Where did the DFT compute run and who set it up?"** | 🟡 Medium | Declare it. |
| 19 | **"Did AI write this?"** | 🔴 Critical | Complete AI declaration + chat-log appendix + process photographs + failed-experiment reporting + hand-verified references. |
| 20 | **"Has this been submitted elsewhere?"** | 🔴 Critical | Explicit declaration either way. |

> **Rule.** For every 🔴 item, the answer must be visible in the report *without the referee having
> to ask*. Pre-emption is worth more than correctness discovered under interrogation.

---

## 9. THE FIVE NUMBERED FINDINGS (Bible §10)

Labelled in bold at the point they are established, and recalled by number in the Conclusion. This
gives the referee a skeleton to score against and gives the author a defence structure for the
oral round. Rendered by the `\finding{n}{text}` macro.

- **Finding 1.** Galloyl grafting on ossein is achieved at `\PENDING{loading_wt_pct}` wt% with the
  collagen Amide I–III architecture intact.
- **Finding 2.** The functionalised sorbent inverts the expected competitive ordering, retaining
  Pb(II) preferentially even at a molar deficit.
- **Finding 3.** Sorption is endothermic and entropy-driven, indicating desolvation control.
- **Finding 4.** DFT reproduces the experimental ordering Pb > Cu > Zn without parameter fitting.
- **Finding 5.** Energy decomposition falsifies the electrostatic rationale; selectivity is
  localised to orbital covalency into Pb 6p and to hemidirected accommodation of the 6s² lone pair.

> Findings 2–5 are stated here as the Bible's target claims. **None is asserted in the report until
> the corresponding dataset reaches status VERIFIED.** If the data does not support a finding, the
> finding changes. Correctness beats consistency with the plan.

### 9.1 The three originality devices (Bible §10)
Criterion C7 contains a literal instruction — "clear distinction between background materials and
original contributions". Implemented mechanically:
- **Device 1 — the novelty box** in §1.4 (`\noveltybox`).
- **Device 2 — origin tagging** throughout Sections III and IV (`\origin{owner}{text}`): name the
  owner of every existing method in the sentence that uses it; mark every original move explicitly.
- **Device 3 — numbered Findings** (`\finding{n}{text}`).

---

## 10. THE TWELVE ANTI-PATTERNS (Bible §18)

1. **Framing as engineering, not chemistry.** The Chemistry panel is not the Environmental Science panel.
2. **A results section that describes figures instead of arguing from them.** Every subsection must end in a verdict.
3. **Over-precise numbers with no uncertainty.** 40.11 mg/g without a ± is a claim that cannot be defended.
4. **Linearised isotherm fits** — the single most cited methodological error in the sorption literature, and the paper that says so is already cited here.
5. **Naked-ion or unspecified-reference-state binding energies.**
6. **Asserting hemidirection instead of measuring it.**
7. **Hiding the computed-vs-experimental magnitude discrepancy.** Referees find it. Pre-empt it and it becomes a strength.
8. **A thin reference list.** 10 references is an outline; 45 is a report.
9. **No control sorbent, or a control mentioned but not plotted alongside.** The α control values are among the strongest data — put them *on the same axes*.
10. **No failed experiments reported.** Reads as either lucky or synthetic.
11. **Vague AI declaration.** In 2026 this is a live disqualification vector, not a formality.
12. **Missing principal signature / wrong filename / two files instead of one / emailed >5 MB attachment.** Losing on formatting after doing real science is the worst possible outcome.

---

## 11. SELF-REFEREE RUBRIC (Bible §17)

Score each 1–5 before submitting. **Anything below 3 must be fixed. Anything below 4 on a 🔴 row
must be fixed.** Interpretation: below 40/60 → not competitive · 40–48 → likely shortlisted for
defence · 49+ → prize contention.

| # | Criterion | Question | Score of 1 | Score of 5 | Score |
|---|---|---|---|---|---|
| R1 | Relevance (C1) | Would a coordination chemist say this is a chemistry paper? | Reads as environmental engineering | Central question is electronic structure and coordination geometry | — |
| R2 | Originality (C2) 🔴 | Can a referee state the novelty in one sentence after reading page 8? | Novelty implied | Explicit numbered novelty list, benchmarked against named prior work | — |
| R3 | Creativity (C3) 🔴 | Is this more than routine application of standard methods? | Standard sorption study + standard DFT | Falsification design; adverse-ratio competition; theory→experiment prediction closed | — |
| R4 | Rigour (C4) 🔴 | Could a referee find an unaddressed hole in 10 minutes? | No replicates, linearised fits, undefined terms | n stated, error bars everywhere, non-linear fits, every symbol defined, limitations pre-empted | — |
| R5 | Impact (C5) | Does the finding generalise beyond this one material? | "Useful adsorbent" | Explicit transferable design descriptor for lone-pair-active ions | — |
| R6 | Literature (C6) | Does the review read as thorough? | <20 refs, no comparison table | 35–60 refs, four organised strands with gap statements, benchmark table | — |
| R7 | Scholarship (C7) | Is background clearly separated from original work? | Blended | Novelty box + origin tagging + numbered Findings | — |
| R8 | Authenticity 🔴 | Would a suspicious referee believe a student did this? | No photos, no failures, no data appendix | Process photos, failed conditions, data appendix, complete AI declaration | — |
| R9 | Compliance 🔴 | Any disqualification exposure? | Missing signature / undeclared AI / >5 MB emailed | All blocks present, all declarations explicit, format exact | — |
| R10 | Visual quality | Do the figures carry the argument alone? | Screenshots, unlabelled axes | 20+ purpose-built figures, consistent colour code, standalone captions | — |
| R11 | Internal consistency | Do all numbers match across sections? | Drift between abstract and results | Canonical number table enforced throughout | — |
| R12 | Defensibility | Could 15 minutes of hostile questions be answered? | Would have to guess on the DFT protocol | Can state functional, ECP, reference state, and why the ΔΔG magnitudes differ | — |

---

## 12. WRITING RULES (Bible §12) — BINDING

- **Voice.** Single-author team. Measured **passive past tense for methods** ("The scales were
  demineralised…"); **present tense for interpretation**. Use **"this work" / "the present study"**
  for claims. Avoid "we" — it reads oddly for one person.
- **Tense.** Methods and results past. Established facts and interpretation present. Conclusions present.
- **Hedging.** State findings assertively; state interpretations with a stated confidence basis.
- **Never write "significantly" without a p-value.** Use "markedly" or "substantially" if no test was run.
- **Significant figures matched to measurement precision.** If the replicate SD is ±2 mg/g, report
  40.1 ± 2.0, not 40.11. Over-precise numbers are a classic tell of unexamined output.
- **Units.** SI. Capacities in **mg/g AND mmol/g**. Energies in **kJ/mol** throughout — never mix in
  kcal/mol from software output.
- **Terminology.** Biosorbent · sorption · sorbate/sorbent · "adsorption" only with evidence of
  surface confinement · "complexation" for the coordination event · "uptake" as the neutral term.
  **Never "absorption".**
- **Abbreviations** defined at first use, then used consistently; list in the front matter.
- **No rhetorical questions, no exclamation marks, no promotional adjectives** ("remarkable",
  "revolutionary", "unprecedented"). Restraint is a status signal.
- **Sentence length.** Methods short and declarative. Discussion may run longer for causal chains,
  never more than two clauses of subordination.
- **Triple-anchoring.** Every headline number appears identically in the abstract, in Results, and
  in the Conclusion (Bible Obs. 6). Enforced by `scripts/check_numbers.py`.

---

## 13. REFERENCING STANDARD (Bible §13)

- **Style** ACS. **Count 35–60.** Numbering in order of first appearance.
- **Composition target:** 8–12 Pb/heavy-metal remediation and biosorption · 8–12 tannin/polyphenol
  and collagen/protein sorbents · 6–10 Pb(II) coordination, lone-pair stereoactivity, hemidirection ·
  6–10 computational methodology · 4–8 isotherm/kinetic/column modelling · 4–6 thermodynamics,
  hydration free energies, HSAB.
- **Recency:** ≥40% from the last 8 years. Classic anchors (Irving & Williams 1953, Langmuir 1918,
  Shimoni-Livny 1998) are expected and fine.
- **Verification is mandatory.** Open every DOI; confirm title, authors, year, volume, pages. Delete
  anything that does not resolve. **A single fabricated reference is an integrity finding, not a typo.**
- **Never cite a paper not read** at least to abstract and figures. Referees ask what reference 23 found.

---

## 14. AMENDMENT LOG

Departures from the Bible, each ruled on in [`02_PROTOCOL_AUDIT.md`](02_PROTOCOL_AUDIT.md).

| ID | Amendment | Affects | Ruled in | Date |
|---|---|---|---|---|
| A-01 | TGA (Fig 4.3, §2.4.3) and BET/porosimetry (§2.4.4) **DESIGNED OUT** — instruments not available to this project. Replacement evidence set specified. | Fig 4.3, §2.4.3, §2.4.4, §4.1 | audit B5 | 2026-08-11 |
| A-02 | All isotherm and kinetic fitting is **non-linear regression**. The linearised forms of Lab Protocol §11 are superseded. | §2.5, §4.2, §4.3, Table 4.2 | audit B2 | 2026-08-11 |
| A-03 | **XPS** promoted to a full characterisation subsection and a new figure/table pair; instrument is available and Pb 4f is the strongest direct evidence of Pb–O coordination. | §2.4.6, §4.1 | audit B6 | 2026-08-11 |
| A-04 | **Quantified leaching test** made mandatory (was optional in the Lab Protocol). | §2.8, §4.1, Attack 10 | audit B7 | 2026-08-11 |
| A-05 | **LOD, LOQ and spike recovery** added to the analytical QC. | §2.5.2, Appendix C | audit B8 | 2026-08-11 |
| A-06 | **Computed Pb(II) speciation** with saturation indices added (Fig 2.4). | §2.5.1, Appendix G, Attack 7 | audit B9 | 2026-08-11 |
| A-07 | **Temperature series** for the van 't Hoff analysis is a required external dataset; the Lab Protocol runs everything at ambient. | §2.5, §4.5, Table 4.6 | audit B1 | 2026-08-11 |
| A-08 | Column planning estimates of Lab Protocol §5.4.3 (BV10 ≈ 117, EF ≈ 56×) are **design-basis estimates, superseded by measurement**. The shortfall requires a physical explanation in §4.8. | §4.8, new attack row A21 | audit B4 | 2026-08-11 |
| A-09 | Ternary composition labelling — **open, awaiting Palaash's ruling in Phase 4.** | §2.6, Table 2.3, §4.4, abstract | audit B3 | open |
