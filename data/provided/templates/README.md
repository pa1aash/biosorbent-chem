<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# data/provided/templates/ — Empty CSVs defining the exact required schema

## What belongs here

- One header-only CSV per required dataset, generated in Phase 5 from `docs/DATA_REQUEST.md`.
- Column headers carry units explicitly, e.g. `C0_mg_per_L`, `qe_mg_per_g`.
- These are the contract `scripts/ingest.py` validates against.

## What must never go here

- Data rows. Templates are headers only.
- Schemas that are not also documented in `docs/DATA_REQUEST.md`.
