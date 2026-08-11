<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# report/ — The LaTeX document

## What belongs here

- `main.tex`, `preamble/`, `frontmatter/`, `sections/`, `appendices/`, `build/`.
- Compiles to `Chem-151-Research Report.pdf` — that exact filename is a compliance requirement.

## What must never go here

- Any hard-coded numeric result. Every number reaches LaTeX through `\num{key}`, generated from `data/CANONICAL_NUMBERS.yaml` by `scripts/emit_numbers.py`.
- A silently filled placeholder. `\PENDING`, `\NEEDSDATA` and `\TODOPAL` render as loud red boxes in draft and hard-fail the final build.
