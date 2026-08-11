<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# DATA REQUEST

Every dataset the report needs, with its exact schema. **Ordered by what to send first.**

Phase 4 answer Q19 establishes that **all datasets exist** except the XPS and SEM-EDX numeric
data, which the laboratory has not yet released. This document is therefore a **transfer
specification**, not a work list: the task is getting existing files into these schemas.

## How to supply a dataset

1. Export one CSV per dataset below, with **exactly** the column headers given. Extra columns are
   fine and are preserved; missing or renamed columns are reported as errors.
2. **One row per replicate. Never supply a mean** — means, SDs and every derived quantity are
   computed by `analysis/src/` so that they cannot drift from the underlying data.
3. Leave a cell **empty** if the value was not recorded. Do not fill it with a guess, a zero or a
   nominal value. An empty cell is correct information; an invented one is not.
4. Drop the file into the directory named in its row and run `python scripts/ingest.py`. It
   validates against the template and **reports mismatches rather than silently coercing them**.
5. Empty templates with the exact headers are in [`data/provided/templates/`](../data/provided/templates/).

**Tags.** `REQUIRED` — the report fails without it. `STRONG` — materially strengthens the case.
`OPTIONAL` — nice to have. `BLOCKED` — required, but outside Palaash's control.

---

## Send order at a glance

| # | ID | Dataset | Tag | Feeds |
|---|---|---|---|---|
| 1 | **DS-01** | Ternary competition — minority-target (25/100/100), the HEADLINE result | `REQUIRED` | Fig 4.7 (money figure) |
| 2 | **DS-02** | Ternary competition — equal-mass (50/50/50), supporting condition | `REQUIRED` | Fig 4.7 |
| 3 | **DS-03** | AAS calibration curves — per metal, per analytical batch | `REQUIRED` | Appendix C |
| 4 | **DS-04** | AAS quality control — check standards and blanks | `REQUIRED` | Appendix C |
| 5 | **DS-05** | Single-metal isotherms — Pb, Cu, Zn on TA-OSS plus the RAW-OSS comparator | `REQUIRED` | Fig 4.5 |
| 6 | **DS-06** | Column A — bed characterisation header, one row per column per cycle | `REQUIRED` | Table 4.11 |
| 7 | **DS-07** | Column A — effluent fractions, all three cycles | `REQUIRED` | Fig 4.14 |
| 8 | **DS-08** | Column A — pooled regenerate, one row per cycle | `REQUIRED` | Fig 4.15 |
| 9 | **DS-09** | Temperature series for the van 't Hoff analysis | `REQUIRED` | Fig 4.8 |
| 10 | **DS-10** | Sorption kinetics — Pb and Cu time courses | `REQUIRED` | Fig 4.6 |
| 11 | **DS-11** | Galloyl loading — gravimetric | `REQUIRED` | Finding 1 |
| 12 | **DS-12** | ATR-FTIR spectra — one two-column CSV per sample | `REQUIRED` | Fig 4.1 |
| 13 | **DS-13** | pH optimisation series | `REQUIRED` | §4.1 |
| 14 | **DS-14** | Batch regeneration cycling | `REQUIRED` | Fig 4.16 |
| 15 | **DS-15** | Column B — ternary breakthrough, bed header and fractions | `STRONG` | Fig 4.14 |
| 16 | **DS-16** | Point of zero charge | `STRONG` | Fig 4.4 |
| 17 | **DS-17** | Tannic-acid leaching test | `STRONG` | Table 4.14 |
| 18 | **DS-18** | Gallic-acid calibration for the leaching assay | `STRONG` | Appendix C |
| 19 | **DS-19** | Residual mineral (ash) content | `STRONG` | §4.1 |
| 20 | **DS-20** | Photograph shot list | `STRONG` | Fig 2.1 |
| 21 | **DS-21** | LOD/LOQ blank replicates | `REQUIRED` | Appendix C |
| 22 | **DS-22** | Spike recovery | `REQUIRED` | Appendix C |
| 23 | **DS-23** | XPS — survey and high-resolution regions | `BLOCKED` | Fig 4.18 |
| 24 | **DS-24** | SEM micrographs and EDX maps/spectra | `BLOCKED` | Fig 4.2 |

---

## Specifications

### 1. DS-01 — Ternary competition — minority-target (25/100/100), the HEADLINE result
**Tag** `REQUIRED` · **Protocol** v2 §2.6 · **Destination** `data/provided/competitive/ternary_minority_target.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | unique row key, e.g. TMIN-R1 |
| `replicate` | 1, 2 or 3 |
| `sorbent` | TA-OSS or RAW-OSS |
| `sorbent_mass_g` | actual weighed mass, 4 d.p. |
| `volume_mL` | actual solution volume |
| `pH_initial` | measured before contact |
| `pH_final` | measured after contact |
| `contact_time_min` | actual, not nominal |
| `temperature_C` | measured lab temperature |
| `C0_Pb_measured_mg_per_L` | MEASURED initial aliquot — not nominal 25 |
| `C0_Cu_measured_mg_per_L` | MEASURED initial aliquot — not nominal 100 |
| `C0_Zn_measured_mg_per_L` | MEASURED initial aliquot — not nominal 100 |
| `Ce_Pb_mg_per_L` | equilibrium concentration |
| `Ce_Cu_mg_per_L` | — |
| `Ce_Zn_mg_per_L` | — |
| `dilution_factor_Pb` | 1 if undiluted |
| `dilution_factor_Cu` | — |
| `dilution_factor_Zn` | — |
| `aas_batch_id` | links to the calibration batch in DS-03 |
| `date` | YYYY-MM-DD |
| `notes` | free text, including any observation of turbidity |

**Replicate structure.** n = 3 on TA-OSS; n = 1 RAW-OSS control (confirm)

**Record alongside.** measured initial aliquots for all three metals; both pH values; the AAS batch

**Feeds.** Fig 4.7 (money figure) · Table 2.3 · Table 4.5 · Finding 2 · abstract

---

### 2. DS-02 — Ternary competition — equal-mass (50/50/50), supporting condition
**Tag** `REQUIRED` · **Protocol** v2 §2.6 · **Destination** `data/provided/competitive/ternary_equal_mass.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `replicate` | — |
| `sorbent` | TA-OSS or RAW-OSS |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `pH_initial` | — |
| `pH_final` | — |
| `contact_time_min` | — |
| `temperature_C` | — |
| `C0_Pb_measured_mg_per_L` | MEASURED — not nominal 50 |
| `C0_Cu_measured_mg_per_L` | MEASURED |
| `C0_Zn_measured_mg_per_L` | MEASURED |
| `Ce_Pb_mg_per_L` | — |
| `Ce_Cu_mg_per_L` | — |
| `Ce_Zn_mg_per_L` | — |
| `dilution_factor_Pb` | — |
| `dilution_factor_Cu` | — |
| `dilution_factor_Zn` | — |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | record ANY turbidity or white precipitate — bears on attack A22 |

**Replicate structure.** n = 3 on TA-OSS; n = 1 RAW-OSS control

**Record alongside.** as DS-01. The spent sorbent from this run feeds DS-08

**Feeds.** Fig 4.7 · Table 2.3 · Table 4.5

---

### 3. DS-03 — AAS calibration curves — per metal, per analytical batch
**Tag** `REQUIRED` · **Protocol** v2 §2.5.2 · **Destination** `data/provided/calibration/aas_calibration.csv`

| Column | Units / meaning |
|---|---|
| `aas_batch_id` | the key every other dataset references |
| `date` | — |
| `metal` | Pb, Cu or Zn |
| `wavelength_nm` | 283.3 / 324.8 / 213.9 — or 307.6 if the alternative Zn line was used |
| `standard_mg_per_L` | nominal concentration of the standard |
| `absorbance` | measured |
| `fit_form` | linear or quadratic |
| `r_squared` | of the fitted curve |
| `slope_abs_per_mg_per_L` | needed for LOD/LOQ |
| `intercept` | — |
| `blank_absorbance` | — |
| `notes` | — |

**Replicate structure.** one row per standard per metal per batch, including the blank

**Record alongside.** wavelength and fit form are mandatory — see attack A25 on the Zn linear range

**Feeds.** Appendix C · Table 2.2 · underwrites EVERY concentration in the report

---

### 4. DS-04 — AAS quality control — check standards and blanks
**Tag** `REQUIRED` · **Protocol** v2 §2.5.2 · **Destination** `data/provided/calibration/aas_qc.csv`

| Column | Units / meaning |
|---|---|
| `aas_batch_id` | — |
| `date` | — |
| `metal` | — |
| `qc_type` | blank / check_standard |
| `position_in_batch` | start / middle / end |
| `nominal_mg_per_L` | — |
| `measured_mg_per_L` | — |
| `deviation_pct` | (measured-nominal)/nominal*100 |
| `accepted` | TRUE/FALSE |
| `notes` | — |

**Replicate structure.** 3 check standards per batch minimum

**Record alongside.** any batch rejected and re-run must appear here with accepted=FALSE — a rejected batch reported is evidence of competence

**Feeds.** Appendix C

---

### 5. DS-05 — Single-metal isotherms — Pb, Cu, Zn on TA-OSS plus the RAW-OSS comparator
**Tag** `REQUIRED` · **Protocol** v2 §2.5.5 · **Destination** `data/provided/batch/isotherm_single_metal.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `metal` | Pb, Cu or Zn |
| `sorbent` | TA-OSS or RAW-OSS |
| `replicate` | — |
| `C0_nominal_mg_per_L` | the series actually run — see the Q20 query on 40 vs 50 ppm |
| `C0_measured_mg_per_L` | if the initial was measured; leave blank if only nominal is available |
| `Ce_mg_per_L` | — |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `pH_initial` | — |
| `pH_final` | — |
| `contact_time_min` | — |
| `temperature_C` | — |
| `dilution_factor` | — |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** n = 3 at the 40 mg/L point; n = 2 elsewhere (Phase 4 answer Q20)

**Record alongside.** one row PER REPLICATE — never a mean. Means are computed, not supplied

**Feeds.** Fig 4.5 · Table 4.2 · Table 4.3 · §4.2 · abstract

---

### 6. DS-06 — Column A — bed characterisation header, one row per column per cycle
**Tag** `REQUIRED` · **Protocol** v2 §2.7.2 · **Destination** `data/provided/column_A/column_A_bed.csv`

| Column | Units / meaning |
|---|---|
| `column_id` | A |
| `cycle` | 1, 2 or 3 |
| `sorbent_mass_g` | 4.0 nominal — give the actual weighed mass |
| `bed_height_cm` | MEASURED settled height |
| `Vbed_mL` | MEASURED — every BV in the report depends on this |
| `rho_b_g_per_cm3` | = m/Vbed |
| `H_to_D` | bed height / 1.0 cm |
| `feed_C0_mg_per_L` | — |
| `feed_pH` | — |
| `flow_BV_per_h` | — |
| `flow_mL_per_min` | — |
| `EBCT_min` | — |
| `date_start` | — |
| `date_end` | — |
| `terminated_early` | TRUE if stopped at C/C0 ~ 0.30 rather than 0.90 |
| `notes` | — |

**Replicate structure.** one row per cycle

**Record alongside.** V_bed MUST be the measured packed-bed volume, not the 8 mL design figure

**Feeds.** Table 4.11 · §2.7 · §4.8 · every BV figure in the report

---

### 7. DS-07 — Column A — effluent fractions, all three cycles
**Tag** `REQUIRED` · **Protocol** v2 §2.7.4 · **Destination** `data/provided/column_A/column_A_fractions.csv`

| Column | Units / meaning |
|---|---|
| `column_id` | A |
| `cycle` | — |
| `fraction_number` | — |
| `cumulative_volume_mL` | — |
| `cumulative_BV` | = cumulative volume / measured Vbed |
| `elapsed_time_min` | — |
| `Ce_Pb_mg_per_L` | — |
| `C_over_C0` | = Ce/C0 |
| `outlet_pH` | if recorded |
| `dilution_factor` | — |
| `below_LOQ` | TRUE/FALSE |
| `aas_batch_id` | — |
| `notes` | — |

**Replicate structure.** no replication — this is a time series

**Record alongside.** fraction-level data is the evidence; a curve reduced to BV10 is not

**Feeds.** Fig 4.14 · Fig 4.16 · Table 4.11 · §4.8

---

### 8. DS-08 — Column A — pooled regenerate, one row per cycle
**Tag** `REQUIRED` · **Protocol** v2 §2.7.5 · **Destination** `data/provided/column_A/column_A_regenerate.csv`

| Column | Units / meaning |
|---|---|
| `column_id` | A |
| `cycle` | — |
| `eluent` | 0.1 M HCl |
| `direction` | counter-current upflow |
| `flow_BV_per_h` | — |
| `volume_BV` | — |
| `volume_mL` | — |
| `C_Pb_regenerate_mg_per_L` | — |
| `dilution_factor` | regenerates can reach thousands of mg/L |
| `mass_desorbed_mg` | — |
| `mass_adsorbed_prior_mg` | — |
| `Pb_remaining_on_bed_mg` | if measured — needed for the mass balance, attack A27 |
| `aas_batch_id` | — |
| `notes` | — |

**Replicate structure.** one row per cycle

**Record alongside.** the mass-balance terms are what close attack A27

**Feeds.** Fig 4.15 · Table 4.11 · §4.8 · enrichment factor

---

### 9. DS-09 — Temperature series for the van 't Hoff analysis
**Tag** `REQUIRED` · **Protocol** v2 §2.5.7 · **Destination** `data/provided/thermodynamics/temperature_series.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `metal` | Pb — and Cu/Zn if run |
| `temperature_C_measured` | MEASURED, not setpoint |
| `temperature_control_method` | water bath / incubator / shaker |
| `temperature_stability_C` | ± value |
| `replicate` | 1, 2 or 3 |
| `C0_mg_per_L` | — |
| `Ce_mg_per_L` | — |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `sorbent_batch` | confirm same batch as the main campaign |
| `pH_initial` | — |
| `pH_final` | — |
| `contact_time_min` | — |
| `dilution_factor` | — |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** n = 3 (Phase 4 answer Q10); full isotherm at each temperature (answer Q9)

**Record alongside.** this dataset is absent from Lab Protocol v1 entirely. Without it there is no §4.5, no Fig 4.8, no Table 4.6 and no Finding 3

**Feeds.** Fig 4.8 · Table 4.6 · Finding 3 · §4.7.4 desolvation closure · abstract

---

### 10. DS-10 — Sorption kinetics — Pb and Cu time courses
**Tag** `REQUIRED` · **Protocol** v2 §2.5.6 · **Destination** `data/provided/kinetics/kinetics.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `metal` | Pb or Cu |
| `contact_time_min` | 5/15/30/60/120/240 |
| `replicate` | the 60 min point is duplicated |
| `C0_mg_per_L` | — |
| `Ct_mg_per_L` | — |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `pH_initial` | — |
| `pH_final` | — |
| `temperature_C` | — |
| `dilution_factor` | — |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** n = 2 (Phase 4 answer Q20); duplicate at 60 min

**Record alongside.** sorbent mass and volume per flask so q_t is recomputable from first principles

**Feeds.** Fig 4.6 · Table 4.4 · §4.3 · justifies the 120 min contact time · feeds the §4.8 intraparticle-diffusion argument

---

### 11. DS-11 — Galloyl loading — gravimetric
**Tag** `REQUIRED` · **Protocol** v2 §2.3.2 · **Destination** `data/provided/characterisation/loading/tannin_loading.csv`

| Column | Units / meaning |
|---|---|
| `batch_id` | — |
| `replicate` | — |
| `m_func_dry_g` | dry mass after functionalisation |
| `m_raw_eq_dry_g` | equivalent dry mass of unfunctionalised ossein |
| `loading_wt_pct` | = (m_func - m_raw_eq)/m_raw_eq * 100 |
| `drying_temp_C` | — |
| `drying_time_h` | — |
| `constant_mass_confirmed` | TRUE/FALSE |
| `n_washes` | how many 200 mL DI washes |
| `wash_endpoint_A276` | final filtrate absorbance at 276 nm, if measured |
| `date` | — |
| `notes` | — |

**Replicate structure.** n >= 3, mean ± SD

**Record alongside.** the wash record is part of this dataset — insufficient washing falsely raises apparent removal

**Feeds.** Finding 1 · §4.1 · §2.3.2 · attack A11 · the site-balance calculation

---

### 12. DS-12 — ATR-FTIR spectra — one two-column CSV per sample
**Tag** `REQUIRED` · **Protocol** v2 §2.4.1 · **Destination** `data/provided/characterisation/ftir/ftir_<sample>.csv`

| Column | Units / meaning |
|---|---|
| `wavenumber_cm-1` | 4000 to 400 |
| `absorbance` | or transmittance — state which in the filename or a header comment |

**Replicate structure.** one file each: ftir_raw_oss.csv, ftir_ta_oss.csv, ftir_spent_ta_oss.csv (and ftir_tannic_acid.csv if recorded)

**Record alongside.** record alongside: instrument model, resolution (4 cm-1), number of scans (>=32), operator, date, and whether any baseline correction or normalisation was applied

**Feeds.** Fig 4.1 · Table 4.1 · Finding 1 · §4.1

---

### 13. DS-13 — pH optimisation series
**Tag** `REQUIRED` · **Protocol** v2 §2.5.4 · **Destination** `data/provided/batch/ph_optimisation.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `sorbent` | TA-OSS / RAW-OSS / none (the sorbent-free control) |
| `pH_target` | 3.0 / 4.0 / 5.0 / 6.0 |
| `pH_initial_measured` | — |
| `pH_final_measured` | — |
| `replicate` | — |
| `C0_mg_per_L` | — |
| `Ce_Pb_mg_per_L` | — |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `contact_time_min` | — |
| `temperature_C` | — |
| `dilution_factor` | — |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** n = 2 (answer Q20); the sorbent-free control at pH 6.0 is n = 1

**Record alongside.** the sorbent-free row is the precipitation control and must be present even though it is a single flask

**Feeds.** §4.1 · justifies the operating pH · supports attack A07

---

### 14. DS-14 — Batch regeneration cycling
**Tag** `REQUIRED` · **Protocol** v2 §2.8.1 · **Destination** `data/provided/regeneration/batch_regeneration.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `cycle` | cycle 1 = the FIRST single-metal Pb re-adsorption, per amendment A-15 |
| `replicate` | — |
| `stage` | desorption / readsorption |
| `eluent` | 0.1 M HCl, desorption rows only |
| `desorbate_Pb_mg_per_L` | — |
| `desorbate_Cu_mg_per_L` | — |
| `desorbate_Zn_mg_per_L` | — |
| `readsorption_C0_mg_per_L` | — |
| `readsorption_Ce_mg_per_L` | — |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `contact_time_min` | — |
| `mass_adsorbed_mg` | — |
| `mass_desorbed_mg` | — |
| `dilution_factor` | — |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** 3 cycles x n = 3

**Record alongside.** the initial ternary loading is reported separately as the source of the first desorbate, NOT as a retention denominator

**Feeds.** Fig 4.16 · §4.8 · capacity retention

---

### 15. DS-15 — Column B — ternary breakthrough, bed header and fractions
**Tag** `STRONG` · **Protocol** v2 §2.7.6 · **Destination** `data/provided/column_B/column_B_bed.csv and column_B_fractions.csv`

| Column | Units / meaning |
|---|---|
| `column_id` | B |
| `fraction_number` | — |
| `cumulative_volume_mL` | — |
| `cumulative_BV` | — |
| `elapsed_time_min` | — |
| `Ce_Pb_mg_per_L` | — |
| `Ce_Cu_mg_per_L` | — |
| `Ce_Zn_mg_per_L` | — |
| `C_over_C0_Pb` | — |
| `C_over_C0_Cu` | — |
| `C_over_C0_Zn` | values > 1 are REAL — record them |
| `outlet_pH` | — |
| `dilution_factor` | — |
| `aas_batch_id` | — |
| `notes` | — |

**Replicate structure.** no replication — time series. Bed header as DS-06

**Record alongside.** all three metals per fraction. Cu/Zn overshoot above C/C0 = 1 is the signature of competitive displacement by Pb, not an error

**Feeds.** Fig 4.14 · §4.8 · the strongest single demonstration of competitive displacement

---

### 16. DS-16 — Point of zero charge
**Tag** `STRONG` · **Protocol** v2 §2.4.5 · **Destination** `data/provided/characterisation/ph_pzc/ph_pzc.csv`

| Column | Units / meaning |
|---|---|
| `sorbent` | TA-OSS or RAW-OSS |
| `pH_initial` | 2 through 10 in unit steps |
| `pH_final` | — |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `electrolyte` | 0.01 M NaCl |
| `equilibration_time_h` | 24 |
| `date` | — |
| `notes` | — |

**Replicate structure.** 9 points each sorbent, 18 rows total

**Record alongside.** the plateau must be visible in the data — a single asserted pH_PZC value is not evidence

**Feeds.** Fig 4.4 · §4.1 · justifies pH 5.0 · evidence line 3 for grafting

---

### 17. DS-17 — Tannic-acid leaching test
**Tag** `STRONG` · **Protocol** v2 §2.4.6 · **Destination** `data/provided/characterisation/leaching/leaching.csv`

| Column | Units / meaning |
|---|---|
| `run_id` | — |
| `sorbent` | TA-OSS or RAW-OSS (the blank) |
| `pH` | 5.0 or 2.0 |
| `contact_time_min` | 120, and 24 h if run |
| `replicate` | — |
| `absorbance_276nm` | — |
| `gallic_acid_equiv_mg_per_L` | — |
| `released_mg_GAE_per_g_sorbent` | — |
| `pct_of_measured_loading` | the number that answers attack A10 |
| `sorbent_mass_g` | — |
| `volume_mL` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** n >= 3 at each pH, plus the RAW-OSS blank at each pH

**Record alongside.** the gallic-acid calibration curve is a separate file: gallic_acid_calibration.csv

**Feeds.** Table 4.14 · §4.1 · attack A10 (grafted vs adsorbed) · attack A16 (mechanism of capacity loss)

---

### 18. DS-18 — Gallic-acid calibration for the leaching assay
**Tag** `STRONG` · **Protocol** v2 §2.4.6 · **Destination** `data/provided/characterisation/leaching/gallic_acid_calibration.csv`

| Column | Units / meaning |
|---|---|
| `standard_mg_per_L` | — |
| `absorbance_276nm` | — |
| `r_squared` | — |
| `slope` | — |
| `intercept` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** >= 5 standards, R^2 > 0.99, run in the same session as the samples

**Record alongside.** without this curve the leaching numbers are absorbances, not concentrations

**Feeds.** Appendix C · underwrites DS-17

---

### 19. DS-19 — Residual mineral (ash) content
**Tag** `STRONG` · **Protocol** v2 §2.4.4 · **Destination** `data/provided/characterisation/ash/ash_content.csv`

| Column | Units / meaning |
|---|---|
| `sorbent` | TA-OSS or RAW-OSS |
| `replicate` | 1 or 2 |
| `crucible_tare_g` | — |
| `m_dry_g` | — |
| `m_ash_g` | — |
| `ash_pct` | = m_ash/m_dry*100 |
| `furnace_temp_C` | 550-600 |
| `hold_time_h` | >= 4 |
| `date` | — |
| `notes` | — |

**Replicate structure.** duplicate each sorbent

**Record alongside.** supply the masses, not only the percentage — the percentage is derived

**Feeds.** §4.1 · supports the ~1030 cm-1 FTIR phosphate band · evidence line 4

---

### 20. DS-20 — Photograph shot list
**Tag** `STRONG` · **Protocol** v2 §2.2, §2.3.4, §2.7.6 · **Destination** `figures/photos/ plus photo_manifest.csv`

| Column | Units / meaning |
|---|---|
| `filename` | — |
| `figure_id` | 2.1 / 2.3 / 4.17 / colour comparison |
| `subject` | — |
| `date_taken` | keep EXIF intact |
| `stage` | which protocol step |
| `notes` | — |

**Replicate structure.** n/a

**Record alongside.** REQUIRED SHOTS — Fig 2.1: supplied ossein, sized 0.50-1.00 mm fraction, TA-OSS (NOT raw fish scale, per Q5). Fig 2.3: apparatus, stirrer array, packed column, AAS. Fig 4.17: any failed condition. Plus RAW-OSS vs TA-OSS colour comparison side by side.

**Feeds.** Fig 2.1 · Fig 2.3 · Fig 4.17 · Appendix H · authenticity evidence (Bible Observation 4)

---

### 21. DS-21 — LOD/LOQ blank replicates
**Tag** `REQUIRED` · **Protocol** v2 §2.5.2 · **Destination** `data/provided/calibration/lod_blanks.csv`

| Column | Units / meaning |
|---|---|
| `aas_batch_id` | — |
| `metal` | — |
| `blank_replicate` | 1 to 7 or more |
| `absorbance` | — |
| `concentration_mg_per_L` | back-calculated through the calibration |
| `date` | — |
| `notes` | — |

**Replicate structure.** n >= 7 independent blanks per metal

**Record alongside.** if 7 blanks were not run, supply nothing here and the alternative sigma_y/x route is used and declared instead

**Feeds.** Appendix C · Table 2.2 · every 'below LOQ' statement in the report

---

### 22. DS-22 — Spike recovery
**Tag** `REQUIRED` · **Protocol** v2 §2.5.2 · **Destination** `data/provided/calibration/spike_recovery.csv`

| Column | Units / meaning |
|---|---|
| `matrix` | batch supernatant / column effluent / diluted regenerate |
| `metal` | — |
| `spike_level` | low or mid |
| `replicate` | — |
| `C_unspiked_mg_per_L` | — |
| `C_added_mg_per_L` | — |
| `C_spiked_mg_per_L` | — |
| `recovery_pct` | = 100*(C_spiked-C_unspiked)/C_added |
| `aas_batch_id` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** n = 3 at each level on each matrix

**Record alongside.** the diluted acid regenerate is the matrix most likely to fail — flame AAS is matrix-sensitive

**Feeds.** Appendix C · analytical credibility for every number

---

### 23. DS-23 — XPS — survey and high-resolution regions
**Tag** `BLOCKED` · **Protocol** v2 §2.4.3 · **Destination** `data/provided/characterisation/xps/xps_<region>_<sample>.csv`

| Column | Units / meaning |
|---|---|
| `binding_energy_eV` | — |
| `intensity_cps` | counts per second |

**Replicate structure.** one file per region per sample

**Record alongside.** REQUIRED PER FILE: sample (raw_oss / ta_oss / pb_loaded_ta_oss / ternary_loaded), region (survey / Pb4f / O1s / C1s / N1s / Cu2p / Zn2p), source (Al Ka 1486.6 eV), pass energy, step size, dwell, sweeps, flood gun on/off, and the CHARGE REFERENCE (adventitious C 1s = 284.8 eV). Binding energies without a stated charge reference are meaningless.

**Feeds.** Fig 4.18 · Table 4.13 · §4.1 · the strongest direct evidence of Pb-O coordination

---

### 24. DS-24 — SEM micrographs and EDX maps/spectra
**Tag** `BLOCKED` · **Protocol** v2 §2.4.2 · **Destination** `data/provided/characterisation/sem_edx/ plus sem_edx_manifest.csv`

| Column | Units / meaning |
|---|---|
| `filename` | — |
| `sample` | raw_oss / ta_oss / pb_loaded_ta_oss / spent |
| `type` | micrograph / edx_map / edx_spectrum |
| `magnification` | — |
| `accelerating_voltage_kV` | — |
| `working_distance_mm` | — |
| `detector` | SE or BSE |
| `coating_element` | Au / Pt / C — this matters for the EDX interpretation |
| `elements_mapped` | — |
| `date` | — |
| `notes` | — |

**Replicate structure.** 3 magnifications per sample minimum

**Record alongside.** scale bar must be burned in by the instrument, never added afterwards. EDX spectra as two-column energy_keV/counts CSVs alongside the images

**Feeds.** Fig 4.2 · §4.1 · morphology and spatial distribution of Pb

---

## Not requested, and why

| Dataset | Reason |
|---|---|
| TGA thermograms | Instrument unavailable. Formally designed out — amendment A-01, audit B5. |
| BET / porosimetry | Instrument unavailable. No surface area or pore structure is reported. |
| ICP-MS | Unavailable. All metal analysis is flame AAS. |
| Sorbent-free ternary blanks | Confirmed not run (Q2). Handled as an accepted risk with the computed saturation index and the contemporaneous visual observation as mitigation. |
| Binary Pb/Cu and Pb/Zn systems | Not run. Stated as a limitation in §5.3 and as future work in §5.4. |
| Hardness-ion (Ca/Mg/Na) matrix | Not run. Attack A15 handled by discussion. |
| Instrument-native raw exports | **This project holds cleaned data only.** There is no raw-data tier and none is claimed. |

## Still needed as answers, not files

Carried as `\TODOPAL` markers in the build.

| Ref | Question |
|---|---|
| Q4 | Prior submission — what, where, when, how the present report differs, and confirmation it was past and not concurrent. **Disqualification-adjacent.** |
| Q8 | Which temperatures for the van 't Hoff series, how controlled, measured or setpoint. **Blocks Fig 4.8 entirely.** |
| Q9 | Which metals in the temperature series — Pb only, or all three. |
| Q11–Q18 | What did not go as written: bath, washing, sizing yield, bed packing, Column B, early termination, repeats and discards. **Blocks §2.3.3 and Fig 4.17.** |
| Q20 | The isotherm concentration series — the answer says n = 3 at 40 ppm, the protocol says 50 ppm. |
| Q21 | AAS calibration standards, wavelengths, fit form and R² per metal per batch. |
| Q23 | Which quantity is 80.1% — batch q_e retention or column BV₁₀ retention. |
| Q24 | The facility for each technique, and any supervision received, even where Palaash operated the instrument himself. |
| — | The dated laboratory note recording that the ternary solutions remained visibly clear (Appendix H). |
