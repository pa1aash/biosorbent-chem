<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# data/ — All experimental evidence and everything derived from it

## What belongs here

- `provided/` — Palaash's cleaned CSVs. This is the EVIDENCE TIER of the project.
- `processed/` — script-generated fitted parameters and derived quantities.
- `CANONICAL_NUMBERS.yaml` — the single source of truth for every number the report states.
- `DATA_MANIFEST.md` — what exists, what is missing, what feeds what.

## What must never go here

- A raw-data tier. THERE IS NO RAW-DATA TIER IN THIS PROJECT. Data is held in cleaned form only. Do not create `data/raw/` and do not describe instrument-native exports as if they exist.
- Any value that was estimated, interpolated, back-calculated or assumed. If a number is not measured, it does not enter this directory.
