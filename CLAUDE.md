# CLAUDE.md — standing instructions for every session in this repository

These rules are binding on every session, without exception, and override any default behaviour.
Read this file and [`docs/00_SPEC.md`](docs/00_SPEC.md) before doing anything else.

---

## 1. PROJECT IDENTITY

| | |
|---|---|
| Project | **Overcoming the Irving–Williams Preference in a Galloyl–Ossein Biosorbent through Experimentally and Computationally Driven Hemidirected Lead(II) Selectivity** |
| Competition | S.T. Yau High School Science Award (Asia) 2026 — Chemistry |
| Registration number | **Chem-151** |
| Author | Palaash Gang — Indus International School, Pune — Pune, India |
| Supervising teacher | Yogita Hastak Menon, Head of Senior School |
| Stage | 2 — referee assessment (Stage-1 outline passed) |
| **Deadline** | **17 August 2026, 23:59 HKT = 21:29 IST.** Target submission **16 August 2026**. |
| Submit to | `yauaward@ashk.org.hk` |
| Deliverable | ONE PDF, A4, named exactly `Chem-151-Research Report.pdf` |

**The specification is [`docs/00_SPEC.md`](docs/00_SPEC.md).** It is the authority on what the
report must be — mandatory blocks, compliance assertions, page budgets, figure and table
registries, the referee attack surface, the writing rules. Where the spec and the Report Bible
disagree, the Bible wins and the spec is a bug.

Other standing documents: [`docs/01_ATTACK_REGISTER.md`](docs/01_ATTACK_REGISTER.md) (live issue
register) · [`docs/02_PROTOCOL_AUDIT.md`](docs/02_PROTOCOL_AUDIT.md) (what is wrong and what was
ruled) · [`docs/03_DECISIONS.md`](docs/03_DECISIONS.md) (dated decision log) ·
[`docs/EXPERIMENTAL_PROTOCOL_v2.md`](docs/EXPERIMENTAL_PROTOCOL_v2.md) (source text for Section II) ·
[`docs/DATA_REQUEST.md`](docs/DATA_REQUEST.md) (what data is still needed).

---

## 2. GIT IDENTITY — EVERYWHERE, WITHOUT EXCEPTION

```
Name    Palaash Gang
Email   palaashgang@gmail.com
GitHub  pa1aash
Remote  git@github.com:pa1aash/biosorbent-chem.git
```

Set **locally** in this repository. Never modify the global git config.

### 2.1 ABSOLUTE RULE — ATTRIBUTION

**No commit, tag, branch, pull-request body, code comment, file header or generated document may
attribute authorship or co-authorship to Claude, Claude Code, Anthropic, "AI", or any assistant.**

Not as a `Co-Authored-By:` trailer. Not as a "Generated with" line. Not as a robot emoji. Not in a
comment. **Every commit is authored by Palaash Gang alone.**

Enforced in three layers:
1. `.claude/settings.json` in this repository sets empty commit and PR attribution.
2. This instruction.
3. A `commit-msg` hook that strips any offending line. Reinstall after a fresh clone with
   `bash scripts/install_hooks.sh`.

This rule is about **authorship attribution in the repository**. It does **not** conflict with the
competition's AI-disclosure requirement, which is a separate and equally binding obligation: the
report's Acknowledgement must contain a full, truthful AI declaration generated from
`logs/ai_use_log.csv`, and the chat records must be attached as Appendix A. Suppressing attribution
in git metadata and declaring AI assistance in the report are both required. Never trade one for
the other.

Commit messages are imperative mood. Commit after every meaningful unit of work, and always before
the session closes.

---

## 3. ABSOLUTE RULE — DATA

**Never invent, estimate, interpolate, back-calculate or "reasonably assume" an experimental value.**

If a number is needed and it is not in `data/CANONICAL_NUMBERS.yaml` with status `VERIFIED`:

1. Emit a **visible** placeholder — `\PENDING{key}{what is needed}`.
2. Add the requirement to [`docs/DATA_REQUEST.md`](docs/DATA_REQUEST.md).
3. Say so plainly in the session summary.

**An empty placeholder is a correct answer. A plausible invented number ends this project.**

This applies to every kind of number, without softening:
- experimental values, uncertainties, replicate counts, instrument parameters;
- values quoted from the literature — those need a verified citation, not a recollection;
- computed values — nothing is quoted until the calculation has actually run and the output file exists;
- numbers from the Stage-1 outline (`ST Y Chem.pdf`). **These are claims to be reproduced from
  data, not inputs.** They live in `docs/02_PROTOCOL_AUDIT.md` Table C and nowhere else. Do not
  seed `CANONICAL_NUMBERS.yaml` from them, do not use them to "check" a fit, and do not let them
  influence the choice of computational protocol.

**Evidence tiers.** Data is held in **cleaned form only** — tidied spreadsheets exported as CSV.
There is **no raw-data tier** in this project. Do not build one, do not refer to instrument-native
exports, and do not let the report imply that raw instrument files exist. Appendix B is
"experimental data tables", not "raw data".

**Instruments available:** ATR-FTIR, SEM-EDX, flame AAS, XPS.
**Not available, formally designed out:** TGA, BET/porosimetry, ICP-MS. Never write a method,
figure or sentence that assumes one of these.

---

## 4. PLACEHOLDER CONVENTIONS

Three markers, three meanings. **Never silently fill any of the three.**

| Macro | Use for | Example |
|---|---|---|
| `\PENDING{key}{what is needed}` | A missing **number** | `\PENDING{qmax_pb_mg_g}{Langmuir q_max for Pb from the non-linear fit, with 95\% CI}` |
| `\NEEDSDATA{fig/table ID}{which dataset}` | A missing **figure or table** | `\NEEDSDATA{Fig 4.8}{temperature series, data/provided/thermodynamics/}` |
| `\TODOPAL{question}` | Something **only Palaash can answer** | `\TODOPAL{Who operated the XPS, at which facility?}` |

In **draft** mode all three render as loud red boxes. In **final** mode (`\finaltrue`) their
presence **hard-fails the build** with an error naming every offender, via
`scripts/check_placeholders.py`.

Filling a placeholder is a deliberate act that requires the underlying evidence to exist. Removing
a placeholder without supplying the evidence is the single worst thing that can be done in this
repository.

---

## 5. CANONICAL-NUMBERS RULE

**No numeric result may be hard-coded in any `.tex` file.**

Every number reaches LaTeX through `\num{key}`, generated from `data/CANONICAL_NUMBERS.yaml` by
`scripts/emit_numbers.py` into `report/preamble/numbers.tex`.

```
data/provided/  →  analysis/src/  →  data/processed/  →  CANONICAL_NUMBERS.yaml  →  numbers.tex  →  \num{key}
```

- Each entry carries `value`, `uncertainty`, `n`, `units`, `source_dataset`, `status`.
- `status` is `PENDING` until the value is derived from a real dataset, then `VERIFIED`.
- `emit_numbers.py` **refuses to emit a PENDING value** except under `--draft`, where it renders a
  red marker instead.
- `scripts/check_numbers.py` flags bare numeric literals in `.tex` that should be `\num{}`, and
  cross-checks that every headline number appears **identically** in the abstract, the results and
  the conclusion.

Significant figures are matched to measurement precision. If the replicate SD is ±2 mg/g, the value
is 40.1 ± 2.0 — never 40.11. Over-precise numbers are a classic tell of unexamined output.

---

## 6. REFERENCE RULE

**No citation enters `refs/library.bib` until both conditions hold:**

1. `scripts/verify_dois.py` resolves it against Crossref and the title, authors, year, volume and
   pages all match; **and**
2. Palaash confirms he has read it — at minimum the abstract and the figures.

Both states are recorded in `refs/VERIFICATION_LOG.csv`. `verify_dois.py` exits non-zero on any
failure and `make final` will not complete.

**A single fabricated reference is an integrity finding, not a typo.** Referees ask what reference
23 found. Never produce a citation from memory, never infer a DOI, never "correct" a reference to
what it probably should be. If a work cannot be verified, it is deleted.

Style ACS. Target 35–60 entries, numbered in order of first appearance, ≥40% from the last 8 years.

---

## 7. SESSION PROTOCOL

At the end of **every** session, in this order:

1. **Append a row to `logs/ai_use_log.csv`** via `python scripts/log_session.py` — date · tool and
   version · session ID · project stage · specific purpose · what was done with the output · how it
   was verified · transcript filename.
2. **Export the transcript** to `logs/sessions/`, named to match the log row.
3. **Run `make check`.**
4. **Commit.**

### 7.1 ABSOLUTE RULE — A SESSION RECORD IS NOT A TRANSCRIPT

**Two separate artefacts are required for every session, and one cannot stand in for the other.**

| Artefact | Who produces it | What it is |
|---|---|---|
| **Session record** — `logs/sessions/<date>_<ID>_<slug>.md` | The assistant | An accurate written account of what the session did. **Not a chat log.** |
| **Verbatim transcript** | **Palaash, exported from the Claude Code client** | The actual chat record the 2026 rules require as Appendix A. |

**The assistant must never generate, reconstruct, simulate or "reproduce from the working record" a
verbatim transcript.** A written account of a conversation is not a record of that conversation, and
submitting one as though it were would misrepresent the evidence to the Organising Committee — which
is a far worse finding than a missing file. If the export does not exist, the correct state is a
**visible, outstanding `\TODOPAL`**, not a plausible substitute.

Every session record therefore carries, at the top, a banner stating that it is not the verbatim
export, and a `\TODOPAL` naming the export still owed. **Those markers are cleared only when the real
export file is present in `logs/sessions/`** — never because the record looks complete.

**Appendix A is assembled from the exports, not from the records.** The records are supporting
context. A session with no export has no Appendix A entry.

This is not bookkeeping. The Acknowledgement's AI declaration and Appendix A are **generated from
this record**. The 2026 rules require names and versions, specific stages and purposes, and timing
and frequency, with chat records attached for verification. The log exists so that the declaration
is accurate rather than reconstructed on 16 August. An inaccurate declaration is a live
disqualification vector.

---

## 8. WRITING RULES (Bible §12) — BINDING ON ALL GENERATED TEXT

- **Voice.** Single-author team. **Measured passive past tense for methods** ("The scales were
  demineralised…"). **Present tense for interpretation.** Use **"this work"** or **"the present
  study"** for claims. Avoid "we" — it reads oddly for one person.
- **Tense.** Methods and results past. Established facts and interpretation present. Conclusions present.
- **Hedging.** State findings assertively. State interpretations with a stated confidence basis.
- **Never write "significantly" without a p-value.** Use "markedly" or "substantially" if no test
  was run.
- **No promotional adjectives** — never "remarkable", "revolutionary", "unprecedented", "novel" as
  self-praise. No rhetorical questions. No exclamation marks. Restraint is a status signal.
- **Significant figures matched to measurement precision.**
- **Units.** SI throughout. Capacities in **mg/g AND mmol/g**. Energies in **kJ/mol** throughout —
  never mix in kcal/mol from software output.
- **Terminology.** Biosorbent · sorption · sorbate / sorbent · "adsorption" only with evidence of
  surface confinement · "complexation" for the coordination event · "uptake" as the neutral term.
  **Never "absorption".**
- **Abbreviations** defined at first use, then used consistently.
- **Sentence length.** Methods short and declarative. Discussion may run longer for causal chains,
  never more than two clauses of subordination.
- **Every Results subsection ends in a `\verdict{}` sentence** stating what has now been established.
- **Origin tagging.** Name the owner of every existing method in the sentence that uses it
  (`\origin{Marenich et al.}{...}`); mark every original move explicitly.
- **Triple-anchoring.** Every headline number appears identically in the abstract, in Results and in
  the Conclusion.

---

## 9. WHAT THIS REPOSITORY DOES NOT DO

- It does not write report prose ahead of the data that supports it.
- It does not describe the energy decomposition as "ETS-NOCV" unless ADF/AMS actually produced it.
  See `vendor/README_EDA.md`. This is attack A01, rated CRITICAL.
- It does not use linearised isotherm or kinetic fits as the production route. All fitting is
  non-linear regression with lmfit, reporting confidence intervals, R², reduced χ², RMSE and AIC.
  Linearised forms appear only in the appendix comparison.
- It does not quote a naked-ion binding energy as a headline quantity. The reaction is written as
  aquo-ligand exchange.
- It does not commit secrets. No API tokens, no SSH keys, no `.env`.
- It does not redistribute licence-restricted software. `vendor/` holds installation notes only.
