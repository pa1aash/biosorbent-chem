<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# dft/structures/ — Molecular geometries

## What belongs here

- Starting cluster models and optimised geometries as XYZ files, one per species.
- A stated charge and multiplicity for every structure, in the XYZ comment line.
- The full set is reproduced verbatim in Appendix E of the report.

## What must never go here

- Geometries with no provenance. Every file states which input produced it.
- Hand-edited coordinates presented as optimised output.

## What is here

**Documents — source material for report §3.1 and §5.3**

| File | Contents |
|---|---|
| [`MODEL_JUSTIFICATION.md`](MODEL_JUSTIFICATION.md) | What the cluster model represents, exactly where it was truncated, how the cut was capped, why that is defensible, and what it cannot represent. |
| [`CONFORMER_SCREEN.md`](CONFORMER_SCREEN.md) | Conformer search method and outcome per species, the CREST failure and what replaced it, and the limitations. |

**Structures** — seventeen species, one `.xyz` each, matching the job inventory of
[`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §8. Each carries a machine-readable provenance header
giving **charge, multiplicity, unpaired-electron count and whether the species is unrestricted**, so
the ORCA input generator reads them off the structure and never infers them (attack A02).
`initial/` holds the pre-optimisation starting geometries; `rotamers/` holds the retained conformer
ensembles; `xtb_logs/`, `crest/` and `screens/` hold the evidence for each screening step.

**Scripts** — run in this order, with the `biosorb` environment active:

| Script | Role |
|---|---|
| [`build_structures.py`](build_structures.py) | Builds all seventeen starting geometries. Sole origin of everything in `initial/`. |
| [`run_xtb_preopt.py`](run_xtb_preopt.py) | GFN2-xTB/ALPB(water) pre-optimisation. |
| [`build_rotamers.py`](build_rotamers.py) | Conformer search; overwrites each structure with its lowest verified conformer. |
| [`run_crest.py`](run_crest.py) | Retained so the CREST attempt and its failure stay reproducible rather than merely asserted. |
| [`screen_deprotonation_site.py`](screen_deprotonation_site.py) | Orders the three P1 mono-deprotonated isomers. |
| [`check_geometries.py`](check_geometries.py) | Verifies every structure is still the species its filename claims. Reports; never repairs. |
| [`emit_prescreen_csv.py`](emit_prescreen_csv.py) | Regenerates `xtb_prescreen.csv` from the structure headers. The single writer of that file. |
| [`geom_utils.py`](geom_utils.py) | Shared connectivity and coordination logic, so every consumer applies the same definition. |

**`xtb_prescreen.csv` energies are not report quantities.** They are semi-empirical GFN2-xTB values
recorded so the pre-screen is auditable. Every row carries `is_report_quantity=no`. Production
energies come from ORCA and from nowhere else.
