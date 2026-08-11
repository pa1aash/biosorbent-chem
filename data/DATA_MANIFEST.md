<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# DATA MANIFEST

What exists, where it came from, when it was ingested, and what it feeds. Updated by
`scripts/ingest.py` on every successful validation, and by hand for provenance notes.

**This project holds cleaned data only.** Tidied spreadsheets exported as CSV. There is **no
raw-data tier**: no instrument-native exports are held and none are claimed. Appendix B of the
report is titled "Experimental data tables", not "Raw data".

**Provenance of everything below:** experiments carried out by Palaash Gang in **July 2026**, in a
laboratory maintained at 25 °C. All instruments operated by Palaash Gang himself
(`\TODOPAL{facility for each technique — Q24}`). Starting material purchased from **Nizona Marine
Products Pvt. Ltd.**

---

## Status

| DS | Dataset | Destination | Ingested | Rows | Schema | Feeds |
|---|---|---|---|---|---|---|
| DS-01 | Ternary minority-target 25/100/100 | `provided/competitive/` | — | — | `ternary_minority_target.csv` | Fig 4.7, Table 4.5, Finding 2 |
| DS-02 | Ternary equal-mass 50/50/50 | `provided/competitive/` | — | — | `ternary_equal_mass.csv` | Fig 4.7, Table 2.3 |
| DS-03 | AAS calibration | `provided/calibration/` | — | — | `aas_calibration.csv` | Appendix C, everything |
| DS-04 | AAS quality control | `provided/calibration/` | — | — | `aas_qc.csv` | Appendix C |
| DS-05 | Single-metal isotherms | `provided/batch/` | — | — | `isotherm_single_metal.csv` | Fig 4.5, Tables 4.2–4.3 |
| DS-06 | Column A bed characterisation | `provided/column_A/` | — | — | `column_A_bed.csv` | Table 4.11 |
| DS-07 | Column A fractions | `provided/column_A/` | — | — | `column_A_fractions.csv` | Figs 4.14, 4.16 |
| DS-08 | Column A regenerate | `provided/column_A/` | — | — | `column_A_regenerate.csv` | Fig 4.15 |
| DS-09 | Temperature series | `provided/thermodynamics/` | — | — | `temperature_series.csv` | Fig 4.8, Table 4.6, Finding 3 |
| DS-10 | Kinetics | `provided/kinetics/` | — | — | `kinetics.csv` | Fig 4.6, Table 4.4 |
| DS-11 | Tannin loading | `provided/characterisation/loading/` | — | — | `tannin_loading.csv` | Finding 1 |
| DS-12 | ATR-FTIR spectra | `provided/characterisation/ftir/` | — | — | `ftir_TEMPLATE.csv` | Fig 4.1, Table 4.1 |
| DS-13 | pH optimisation | `provided/batch/` | — | — | `ph_optimisation.csv` | §4.1 |
| DS-14 | Batch regeneration | `provided/regeneration/` | — | — | `batch_regeneration.csv` | Fig 4.16 |
| DS-15 | Column B ternary breakthrough | `provided/column_B/` | — | — | `column_B_fractions.csv` | Fig 4.14 |
| DS-16 | Point of zero charge | `provided/characterisation/ph_pzc/` | — | — | `ph_pzc.csv` | Fig 4.4 |
| DS-17 | Leaching test | `provided/characterisation/leaching/` | — | — | `leaching.csv` | Table 4.14, attack A10 |
| DS-18 | Gallic-acid calibration | `provided/characterisation/leaching/` | — | — | `gallic_acid_calibration.csv` | Appendix C |
| DS-19 | Ash content | `provided/characterisation/ash/` | — | — | `ash_content.csv` | §4.1 |
| DS-20 | Photographs | `figures/photos/` | — | — | `photo_manifest.csv` | Figs 2.1, 2.3, 4.17 |
| DS-21 | LOD/LOQ blanks | `provided/calibration/` | — | — | `lod_blanks.csv` | Table 2.2 |
| DS-22 | Spike recovery | `provided/calibration/` | — | — | `spike_recovery.csv` | Appendix C |
| DS-23 | XPS | `provided/characterisation/xps/` | **BLOCKED** | — | `xps_TEMPLATE.csv` | Fig 4.18, Table 4.13 |
| DS-24 | SEM-EDX | `provided/characterisation/sem_edx/` | **BLOCKED** | — | `sem_edx_manifest.csv` | Fig 4.2 |

**Ingested = —** means the file has not yet been supplied. Phase 4 answer Q19 establishes that all
datasets except DS-23 and DS-24 exist; they have not yet been transferred into these schemas.

---

## Known absences, recorded so they are never mistaken for oversights

| Absent | Reason | Where stated in the report |
|---|---|---|
| TGA thermograms | Instrument unavailable. Designed out, amendment A-01. | §2.4, §5.3 |
| BET / porosimetry | Instrument unavailable. No surface area or pore data is reported. | §2.4, §5.3 |
| ICP-MS | Unavailable. All metal analysis is flame AAS. | §2.5.2 |
| Sorbent-free ternary blanks | Not run (Phase 4 answer Q2). Solutions observed visibly clear. | §2.5.3, §5.3 |
| Binary Pb/Cu and Pb/Zn systems | Not run. | §5.3, §5.4 |
| Hardness-ion (Ca/Mg/Na) matrix | Not run. | §5.3, §5.4 |
| Instrument-native raw exports | This project holds cleaned data only. | §2.5.3, Appendix B |
| Demineralisation yield | No demineralisation was performed; the ossein was purchased. | §2.2 |
