<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# FIGURE HOUSE STYLE

Binding on every figure in the report. Locked in code by
[`analysis/src/style.py`](../analysis/src/style.py), which every script in
[`src/`](src/) imports. **No script sets a colour, a font or a dpi of its own.**

Winners are visual. The 2025 Chemistry Silver carries ~13 multi-panel figures and 9 tables in ~35
pages. Target for this report: **20–26 figures, 12–16 tables**; current registry 24 and 18.

---

## 1. The metal colours are fixed and never vary

| Metal | Colour | Hex | Marker |
|---|---|---|---|
| **Pb(II)** | deep red | `#B2182B` | circle `o` |
| **Cu(II)** | deep blue | `#2166AC` | square `s` |
| **Zn(II)** | amber | `#E08214` | triangle `^` |

A referee reading twenty-odd figures must never re-read a legend to know which series is lead.

The three differ in **lightness as well as hue**, so a photocopied or greyscale printout still
separates them, and so do the marker shapes. That redundancy is deliberate: colour alone fails for
readers with colour-vision deficiency and fails again on a black-and-white printer.

**Always use `style.metal_style(metal, sorbent)`** rather than passing colours by hand. That is what
makes the palette impossible to drift.

## 2. The control is plotted on the same axes as the functionalised material

Bible anti-pattern 9. The α values for RAW-OSS are among the strongest data in this project, and a
control that is *mentioned* but not *plotted alongside* is worth very little. TA-OSS is solid line
with filled markers; RAW-OSS is dashed with open markers, same colour per metal.

## 3. Every axis carries a quantity AND a unit

`q_e / mg g⁻¹`, not `q_e`. Not `Concentration`. **`style.save()` refuses to write a figure with an
unlabelled axis** — the most common figure defect, and trivially preventable.

## 4. Error bars are mandatory

Every plotted mean carries an error bar, or the caption states explicitly why it does not.
Replication in this project is **n = 3 at the 40 mg/L isotherm point and n = 2 elsewhere**, so
measurement error bars are available throughout. State `n` in every caption.

Where a bar shows regression uncertainty rather than measurement scatter — a fitted parameter's 95%
confidence interval — **say which**. They are different quantities and conflating them is the kind
of thing a rigorous referee notices.

## 5. Multi-panel figures

Labelled **(a) (b) (c)** by `style.panel_labels()`, under **one unified caption**. Not several
captions, not a caption per panel.

## 6. Captions stand alone

A caption states **what is plotted, under what conditions, with what n, and what the reader should
see**. A reader who reads only the figure and its caption should understand the claim. This is why
the captions in the skeleton are already long: they are doing work, not decorating.

## 7. Resolution and format

- Vector **PDF** wherever the figure is drawn from data.
- Raster only for micrographs and photographs, at **≥ 300 dpi**; `style.py` writes at **400 dpi**.
- Fonts embedded as TrueType (`pdf.fonttype = 42`), never Type 3 — compliance assertion **C-012**.
- A blurry SEM image reads as carelessness.

## 8. Typeface

Serif, matching the report body face (newtx / Times-like), at 9 pt. A figure set in the matplotlib
default sans-serif reads as pasted in from somewhere else.

## 9. Never a software screenshot

Everything is re-plotted from data. No instrument-software windows, no spreadsheet screenshots, no
photographs of a monitor. Scale bars on micrographs are **burned in by the instrument**, never added
afterwards.

## 10. Never invent data to see what a figure looks like

If a dataset has not been supplied, the script stays unrun and the report carries its `\NEEDSDATA`
placeholder. A figure drawn from plausible-looking invented numbers is the single most dangerous
artefact this project could produce, because it looks exactly like a real one.

---

## Sizing

`style.figure(width_frac=1.0)` spans the full text block (16.0 cm = A4 less two 2.5 cm margins).
`width_frac=0.48` gives a half-width figure that sits beside another.

## Adding a figure

```bash
python scripts/new_figure.py fig4_7_selectivity     # scaffolds with the house style
```

Then register it in [`FIGURE_REGISTER.md`](FIGURE_REGISTER.md) and place it in the section file as a
float with its full caption.
