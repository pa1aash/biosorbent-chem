<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# Session record — S01, 11 August 2026

**Tool:** Claude Opus 5 (`claude-opus-5[1m]`), via Claude Code
**Stage:** repository setup and build infrastructure
**Duration:** 11 August 2026, approximately 10:20–23:50 IST
**Corresponding row:** `logs/ai_use_log.csv`, session `S01`

---

> ## ⚠ THIS FILE IS A SESSION *RECORD*, NOT THE VERBATIM CHAT EXPORT
>
> The 2026 AI Usage Rules require **chat records** to be attached as an appendix for Organising
> Committee verification. This document is an accurate account of what the session did, written
> from the working record, but it is **not** the verbatim transcript.
>
> **Palaash must export the verbatim session transcript from the Claude Code client and place it
> alongside this file** before Appendix A is assembled. Do not submit this summary in place of the
> transcript.
>
> `\TODOPAL{export the verbatim S01 transcript to logs/sessions/ and reference it here}`

---

## What the session was asked to do

Build the complete working repository for the Chem-151 Stage-2 submission: directory skeleton,
specification extraction, protocol audit, data contract, environment, computational plan, LaTeX
skeleton and build tooling. **Explicitly: no report prose.**

## What was produced

| Phase | Output |
|---|---|
| 1 | 56-directory tree, each with a README stating what belongs there and what never does; local git identity |
| 2 | `docs/00_SPEC.md` (38 compliance assertions, figure and table registries, attack surface, rubric); `docs/01_ATTACK_REGISTER.md`; `CLAUDE.md` |
| 3 | `docs/02_PROTOCOL_AUDIT.md` — coverage of 20 experiments, 9 specified gaps plus 17 found, 25 outline claims marked unverified, and the audit's own arithmetic |
| 4 | 25-question interview; answers and consequences recorded in `docs/03_DECISIONS.md` |
| 5 | `docs/EXPERIMENTAL_PROTOCOL_v2.md` (19 marked amendments); `docs/DATA_REQUEST.md` (24 datasets); 26 CSV templates; `data/CANONICAL_NUMBERS.yaml` (295 keys, all null and PENDING) |
| 6 | `biosorb` Python environment; 6 TeX packages installed without sudo; PDF utilities; genuine JINST style obtained and vendored |
| 7 | `dft/DFT_PROTOCOL.md`; Hetzner provisioning and job scripts; `analysis/src/hemidirection.py` with 17 passing tests |
| 8 | Full LaTeX skeleton, compiling clean to 45 A4 pages with 84 visible placeholders |
| 9 | Eight scripts, figure house style, Makefile |
| 10 | Pushed to `git@github.com:pa1aash/biosorbent-chem.git` |

## What was NOT produced, by instruction

- **No report prose.** Section files contain structure, captions, placeholders and comment-block
  checklists only.
- **No numeric values of any kind.** All 295 canonical-number entries are `null` with status
  `PENDING`. No experimental value, no literature value and no computed value was written into any
  file.
- **No references.** `refs/library.bib` is empty by design; no citation enters it until it resolves
  against Crossref and Palaash confirms he has read it.
- **No calculations were run.** The DFT protocol is designed; nothing has been computed.

## Substantive findings of the session

Two findings from the protocol audit change what the report can claim. Both were derived by
recomputing from the protocol and the outline, and both were independently cross-checked:

1. **PbSO₄ supersaturation in both ternary runs.** The competitor salts are sulfates and the lead
   salt is a nitrate. Hand calculation with Davies activity corrections gave a saturation index of
   **+1.01** for anglesite; PHREEQC with full ion-pairing speciation independently gave **+0.86**.
   Every sample was filtered at 0.45 µm, so any precipitate would have been counted as sorption.

2. **The capacity ordering inverts on a molar basis.** Converting the outline's capacities from
   mg g⁻¹ to mmol g⁻¹ reverses Pb > Cu > Zn to Cu > Zn > Pb, and the same inversion appears in the
   ternary uptake. The selectivity factors are unaffected, because α is a ratio of distribution
   coefficients and the molar mass cancels — verified algebraically and numerically.

The audit also reproduced the outline's α values exactly (3.628 and 7.029 against the published 3.63
and 7.03) from its own removal percentages, establishing that they were computed from data rather
than asserted.

## How the outputs were verified

- Every arithmetic claim in the audit was computed, not estimated; the saturation indices were
  cross-checked against PHREEQC.
- The hemidirection descriptors were unit-tested against a hand-worked geometry with values derived
  on paper (d = 1.4433756729740643 Å, θ_void = 125.26438968275465°).
- The built PDF was **measured**: A4 page size, margins by rasterising sample pages, three-level TOC,
  font embedding, running header and absence of journal furniture. Nothing about the output was
  assumed from the settings that were supposed to produce it.
- The commit-msg hook was tested against a real commit carrying attribution lines.
- Every toolchain version in the handoff table was obtained by running the tool.

Six LaTeX bugs were found and fixed during bring-up. One of them — `jinstpub` setting `\hoffset`
and `\voffset` to −1in, which left the built document with a **zero left margin** against a
mandatory 2.5 cm — would have been a formatting failure at submission.

## Declaration

No AI tool was used to conceive the research topic, design the experiments, generate or alter any
experimental or computational datum, produce any figure from data it was not given, draft the
substantive argument of the Results and Discussion, or generate references.
