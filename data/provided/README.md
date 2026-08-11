<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# data/provided/ — Cleaned experimental data supplied by Palaash Gang

## What belongs here

- Tidy CSVs exported from Palaash's cleaned spreadsheets, one dataset per file, matching a schema in `templates/`.
- Files land here by being validated through `scripts/ingest.py` against their template.
- Every file is read-only evidence once ingested.

## What must never go here

- Analysis output. Fits, parameters and derived quantities belong in `data/processed/`.
- Hand-edited values. If a value changes, the correction is made upstream in the source spreadsheet and the file is re-ingested, with the change noted in `DATA_MANIFEST.md`.
- Any file whose provenance cannot be stated.
