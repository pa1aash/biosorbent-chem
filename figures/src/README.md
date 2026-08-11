<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# figures/src/ — One script per figure

## What belongs here

- `figNN_name.py`, scaffolded by `scripts/new_figure.py`, importing the house style from `analysis/src/style.py`.
- Each script reads `data/provided/` and/or `data/processed/` and writes exactly one figure into `out/`.

## What must never go here

- Data. Scripts read data; they do not contain it.
- Colours chosen ad hoc. Pb, Cu and Zn have one fixed colour each across the entire document.
