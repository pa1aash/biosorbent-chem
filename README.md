# Chem-151 — S.T. Yau High School Science Award (Asia) 2026

**Overcoming the Irving–Williams Preference in a Galloyl–Ossein Biosorbent through Experimentally and Computationally Driven Hemidirected Lead(II) Selectivity**

| | |
|---|---|
| Registration number | **Chem-151** |
| Team member | Palaash Gang — Indus International School, Pune — Pune, India |
| Supervising teacher | Yogita Hastak Menon, Head of Senior School — Indus International School, Pune |
| Stage | 2 — Referee assessment (Stage 1 outline passed) |
| Deadline | **17 August 2026, 23:59 HKT** = 21:29 IST. Target submission **16 August 2026**. |
| Submit to | `yauaward@ashk.org.hk` |
| Deliverable | ONE PDF, A4, named exactly `Chem-151-Research Report.pdf` |

This repository is the working infrastructure for the Stage-2 research report: specification, data
contract, analysis code, computational protocol, figure and table generation, and the LaTeX build.

---

## Governing documents

Three source documents sit at the repository root and are the inputs to everything else.

| File | Authority over |
|---|---|
| `YHSA_Asia_Winning_Report_Bible.md` | **What the report must be** — structure, page budgets, figure/table plan, referee attack surface, compliance rules, timeline. Distilled into [docs/00_SPEC.md](docs/00_SPEC.md). |
| `ST Y Chem.pdf` | The accepted Stage-1 research outline. Its numbers are **claims to be reproduced from data**, not inputs. Tracked in [docs/02_PROTOCOL_AUDIT.md](docs/02_PROTOCOL_AUDIT.md) Table C. |
| `Lab Protocol (1) (1).pdf` | **What was done at the bench.** Contains known errors; corrected in [docs/EXPERIMENTAL_PROTOCOL_v2.md](docs/EXPERIMENTAL_PROTOCOL_v2.md). |

Start at [CLAUDE.md](CLAUDE.md) for the standing rules, then [docs/00_SPEC.md](docs/00_SPEC.md).

---

## Two rules that override everything else

**ATTRIBUTION.** Every commit, tag, branch, PR body, code comment, file header and generated
document is authored by Palaash Gang alone. No attribution or co-attribution to any assistant,
tool or company appears anywhere in this repository. Enforced by `.claude/settings.json`, by
[CLAUDE.md](CLAUDE.md), and by the `commit-msg` hook installed by `scripts/install_hooks.sh`.

**DATA.** No experimental value is ever invented, estimated, interpolated, back-calculated or
reasonably assumed. If a number is needed and is not in `data/CANONICAL_NUMBERS.yaml` with
status `VERIFIED`, a visible `\PENDING` placeholder is emitted and the requirement is added to
[docs/DATA_REQUEST.md](docs/DATA_REQUEST.md). An empty placeholder is a correct answer.

---

## Evidence tiers

This project holds experimental data in **cleaned form only** — tidied spreadsheets exported to
CSV. There is **no raw-data tier**: no instrument-native exports are held, and none are claimed.

| Tier | Location | Produced by |
|---|---|---|
| Cleaned evidence | `data/provided/` | Palaash Gang, validated through `scripts/ingest.py` |
| Derived quantities | `data/processed/` | scripts in `analysis/src/` |
| Reportable numbers | `data/CANONICAL_NUMBERS.yaml` | curated from `data/processed/`, status-tracked |
| Report | `report/` | `\num{key}` only — never a hard-coded literal |

Instruments available to this project: **ATR-FTIR, SEM-EDX, flame AAS, XPS**.
Not available, and formally designed out: **TGA, BET/porosimetry, ICP-MS**.

---

## Layout

```
docs/       specification, attack register, protocol audit, decisions, protocol v2, data request
admin/      official forms, signatures, correspondence, the submitted bundle
data/       provided (cleaned CSVs) · processed (script output) · CANONICAL_NUMBERS.yaml
dft/        protocol, structures, inputs, outputs, analysis, validation, Hetzner provisioning
analysis/   importable package (isotherms, kinetics, thermo, selectivity, column, speciation,
            eda, hemidirection) and its tests
figures/    one script per figure, rendered output, laboratory photographs, schemes
tables/     one script per table, generated .tex fragments
refs/       library.bib, Crossref verification log, PDFs of every cited work
report/     main.tex, preamble, front matter, sections I–V, appendices A–J, build
scripts/    emit_numbers, verify_dois, check_placeholders, check_numbers, check_compliance,
            ingest, log_session, new_figure, install_hooks, env
logs/       ai_use_log.csv and exported session transcripts (Appendix A evidence)
vendor/     ORCA / Multiwfn / EDA installation notes, JINST class files
```

Every directory carries its own `README.md` stating what belongs there and what must never go there.

---

## Build

```bash
make setup      # environment
make numbers    # CANONICAL_NUMBERS.yaml -> report/preamble/numbers.tex
make figures    # figures/src/*.py -> figures/out/
make tables     # tables/src/*.py  -> tables/out/
make draft      # placeholders render as loud red boxes
make check      # placeholder, number-consistency, DOI and compliance checks
make final      # fails on any surviving placeholder or unverified DOI
make submit     # produces admin/submission/Chem-151-Research Report.pdf
make log        # append this session to logs/ai_use_log.csv
```

---

## Session protocol

At the end of every working session, without exception:

1. Append a row to `logs/ai_use_log.csv`.
2. Export the transcript to `logs/sessions/`.
3. Run `make check`.
4. Commit.

The Acknowledgement's AI declaration and Appendix A are generated from that record. They are not
reconstructed from memory on 16 August.
