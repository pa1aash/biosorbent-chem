<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# JINST typography — provenance

## Which route succeeded: **ROUTE 2**

| Route | Attempted | Result |
|---|---|---|
| **1. Local TeX distribution** | `kpsewhich jinstpub.sty`, `kpsewhich JINST.cls`, `kpsewhich JHEP3.cls`; `tlmgr search --global jinst` | **FAILED.** JINST is not distributed with TeX Live 2026. All three lookups returned nothing. |
| **2. Official JINST author template** | Fetched from the SISSA/JINST author-help pages at `jinst.sissa.it/jinst/help/JINST/TeXclass/` | **✅ SUCCEEDED.** Obtained the genuine `jinstpub.sty` **v.1.1638, dated 2020/09/18**, Copyright 2015 SISSA Medialab, together with the official `jinst-latex-sample.tex`. |
| **3. Reimplementation on `article`** | — | **Not needed.** Not attempted, and no reimplementation is in use. |

The report therefore uses **the real JINST style**, not an imitation.

---

## Files

| File | What it is |
|---|---|
| `vendor/jinst/jinstpub.sty` | **The pristine original, byte-for-byte as distributed by SISSA Medialab.** Never edited. Retained so the derivation can be verified by `diff`. |
| `vendor/jinst/jinst-latex-sample.tex` | The official sample document, for reference. |
| `report/preamble/yhsa-jinst.sty` | **The derived work actually loaded by the report.** |

## Licence position

`jinstpub.sty` is distributed under the **LaTeX Project Public License v1.3 or later**, which permits
modification **provided the modified file is renamed**. It is renamed `yhsa-jinst`. The derived file
carries a header stating its origin, its licence, and that SISSA Medialab is not its maintainer and
bears no responsibility for it. The original is redistributed unmodified alongside, as the LPPL
contemplates.

---

## Exactly what was changed, and why

`diff vendor/jinst/jinstpub.sty report/preamble/yhsa-jinst.sty` shows the header block plus **two**
substantive edits. Nothing else differs.

### 1. `natbib` is not loaded — the only functional change

The original loads natbib unconditionally:

```latex
\ifnatbibsort\RequirePackage[numbers,sort&compress]{natbib}\else\RequirePackage[numbers,compress]{natbib}\fi
```

**natbib is incompatible with biblatex**, and this report requires biblatex with the biber backend
and the `chem-acs` style — ACS referencing is the standard for a chemistry report and is specified in
`docs/00_SPEC.md` §13. Loading both raises a hard incompatibility error.

The line is commented out and marked `[YHSA]`, with the original text preserved in the comment so
that the change is visible rather than silent. Bibliography formatting is supplied by
`report/preamble/04_refs.tex`.

### 2. TOC dot leaders are restored

The original suppresses dot leaders in the table of contents with `\renewcommand{\@dotsep}{10000}`.
The competition format requires a three-level table of contents **with dot leaders**
(`docs/00_SPEC.md` M5, C-037). The suppression is commented out and the leaders are restored in
`00_compliance.tex`.

### 3. `\ProvidesPackage` renamed

`jinstpub` → `yhsa-jinst`, as the LPPL requires.

---

## What is reproduced, and what is deliberately not

### Reproduced exactly — this is the JINST look

- **The serif text face and matching mathematics**: `newtxtext` + `newtxmath`, with `newtxtt` for
  monospace. This is the single largest component of the JINST appearance.
- **Sans-serif headings** against the serif body.
- **Section head style** — the `\@startsection` parameters, verbatim.
- **Float placement parameters** — `topnumber`, `topfraction`, `bottomfraction`, `totalnumber`,
  `textfraction`, `floatpagefraction`. These govern the in-text figure behaviour that gives JINST
  papers their characteristic density.
- **Equation numbering by section**, `\theequation = \thesection.\arabic{equation}`.
- **Bibliography environment formatting** — small, ragged-right, with JINST's item spacing.
- Table and array spacing: `\arraycolsep`, `\tabcolsep`, `\arrayrulewidth`, `\doublerulesep`.
- Penalties and line-breaking parameters.
- `amsthm`, `amsmath`, `graphicx`, `wrapfig`, `T1` font encoding.

### Overridden by `00_compliance.tex`, which loads *after* and therefore wins

| JINST setting | Overridden with | Why |
|---|---|---|
| `\textwidth .72\paperwidth`, `\oddsidemargin .14\paperwidth`, `\topmargin .05\paperheight` | `\usepackage[a4paper,margin=2.5cm]{geometry}` | **JINST sets its own page geometry.** Its top margin computes to about 1.5 cm, **below the mandatory 2.5 cm**. Assertion **C-002** is a hard rule and a disqualification risk. |
| `\renewcommand{\baselinestretch}{1.1}` | `\onehalfspacing` (setspace) | **C-003** requires 1.5 line spacing for body text. JINST's 1.1 does not satisfy it. |
| `\ps@myplain` — page number as `-- N --`, no header | `fancyhdr` running header on every page | The competition format requires `Research Report` / `2026 S.T. Yau High School Science Award (Asia)` on every page. |
| `\@dotsep = 10000` | dot leaders restored | **C-037**. |
| `colorlinks=true`, all links blue, `pdfa=true` | `\hypersetup` in `05_crossref.tex` | Softer link colours for print, and `pdfa` disabled because it conflicts with `pdfpages` inclusion of the scanned Commitments form. |

### Never used — the journal furniture

**This is a competition report, not a journal submission, and it must not be dressed to look like a
published paper.** `docs/00_SPEC.md` assertion **C-038** checks for this.

`yhsa-jinst.sty` defines `\maketitle` as a journal title block. **It is never called.** The report
uses the official YHSA(Asia) cover page from `report/frontmatter/cover.tex`. Consequently none of the
following is ever typeset:

- the first-page header `Prepared for submission to JINST` (`\@fpheader`) — additionally blanked in
  `00_compliance.tex` so it cannot appear by accident;
- the `\subheader`, `\proceeding` and `\collaboration` fields;
- the arXiv ePrint line;
- the `\dedicated` block;
- the JINST/SISSA affiliation and e-mail block.

There is **no SISSA or IOP logo, no "PUBLISHED BY IOP AND SISSA" line, no Received/Revised/Accepted
block, no DOI line, no copyright line and no article-ID footer** anywhere in this style file — the
v1.1638 preprint style does not contain them, so there is nothing of that kind to strip. This was
verified by searching the file for each of those strings.

---

## Verification

```bash
diff vendor/jinst/jinstpub.sty report/preamble/yhsa-jinst.sty   # shows header + 2 edits, nothing else
grep -n 'YHSA' report/preamble/yhsa-jinst.sty                    # every edit is marked
grep -ci 'sissa\|logo\|published by' report/build/main.log       # journal furniture in the build
```
