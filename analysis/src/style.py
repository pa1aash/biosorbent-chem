"""House figure style for the Chem-151 report.

THE SINGLE SOURCE OF TRUTH FOR FIGURE APPEARANCE. Every script in figures/src/
imports this module; nothing sets a colour, a font or a dpi of its own.

The rule that matters most (Bible section 9.3): **Pb, Cu and Zn each have one
colour, and it never varies across the document.** A referee reading twenty-odd
figures should never have to re-read a legend to know which series is lead.
Defining the palette in one importable place is what makes that true mechanically
rather than by discipline.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

__all__ = ["METAL_COLOURS", "METAL_MARKERS", "SORBENT_STYLES", "figure", "save",
           "panel_labels", "metal_style"]

# ---------------------------------------------------------------------------
# The metal palette. FIXED. Do not override these anywhere.
#
# Chosen to be distinguishable in greyscale and under the common forms of
# colour-vision deficiency: the three differ in lightness as well as in hue, so
# a printed monochrome copy still separates them.
# ---------------------------------------------------------------------------
METAL_COLOURS = {
    "Pb": "#B2182B",   # deep red     — the target ion, the darkest of the three
    "Cu": "#2166AC",   # deep blue    — the principal competitor
    "Zn": "#E08214",   # amber        — the second competitor
}

# Marker shape carries the same information as colour, so the figures survive
# being photocopied.
METAL_MARKERS = {"Pb": "o", "Cu": "s", "Zn": "^"}

# Functionalised versus control. The control is ALWAYS plotted on the same axes
# as the functionalised material (Bible anti-pattern 9): a control mentioned but
# not plotted alongside is worth very little.
SORBENT_STYLES = {
    "TA-OSS":  {"linestyle": "-",  "markerfacecolor": "full",  "alpha": 1.00},
    "RAW-OSS": {"linestyle": "--", "markerfacecolor": "none",  "alpha": 0.85},
}

# Column widths of the report text block: A4 minus 2 x 2.5 cm margins.
TEXT_WIDTH_CM = 16.0
_CM = 1 / 2.54

DPI = 400          # above the 300 dpi minimum, with margin for scaling
FONT_SIZE = 9


def _rc() -> dict:
    """Match the body face. The report is set in newtx (Times-like); a figure in
    the default sans-serif reads as pasted in from somewhere else."""
    return {
        "figure.dpi": 120,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "Liberation Serif",
                       "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": FONT_SIZE,
        "axes.labelsize": FONT_SIZE,
        "axes.titlesize": FONT_SIZE,
        "xtick.labelsize": FONT_SIZE - 1,
        "ytick.labelsize": FONT_SIZE - 1,
        "legend.fontsize": FONT_SIZE - 1,
        "legend.frameon": False,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "lines.linewidth": 1.3,
        "lines.markersize": 4.5,
        "errorbar.capsize": 2.5,
        "axes.grid": False,
        "figure.autolayout": False,
        "pdf.fonttype": 42,        # embed as TrueType, not Type 3 — C-012
        "ps.fonttype": 42,
    }


mpl.rcParams.update(_rc())


def figure(ncols: int = 1, nrows: int = 1, width_frac: float = 1.0,
           aspect: float = 0.68, **kwargs):
    """Create a figure sized to the report's text block.

    width_frac=1.0 spans the full text width; 0.48 gives a half-width figure that
    sits beside another.
    """
    w = TEXT_WIDTH_CM * width_frac * _CM
    h = w * aspect * (nrows / max(ncols, 1)) ** 0.5 if nrows > 1 else w * aspect
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, h),
                             constrained_layout=True, **kwargs)
    return fig, axes


def metal_style(metal: str, sorbent: str = "TA-OSS") -> dict:
    """Plot kwargs for one metal on one sorbent. Use this rather than passing
    colours by hand, so that the palette cannot drift between figures."""
    if metal not in METAL_COLOURS:
        raise KeyError(f"unknown metal {metal!r}; expected one of {sorted(METAL_COLOURS)}")
    if sorbent not in SORBENT_STYLES:
        raise KeyError(f"unknown sorbent {sorbent!r}; expected one of {sorted(SORBENT_STYLES)}")
    s = SORBENT_STYLES[sorbent]
    colour = METAL_COLOURS[metal]
    return {
        "color": colour,
        "marker": METAL_MARKERS[metal],
        "linestyle": s["linestyle"],
        "alpha": s["alpha"],
        "markerfacecolor": colour if s["markerfacecolor"] == "full" else "none",
        "markeredgecolor": colour,
        "label": f"{metal} ({sorbent})",
    }


def panel_labels(axes, labels=None, x=-0.02, y=1.04, weight="bold"):
    """Label multi-panel figures (a) (b) (c), under ONE unified caption."""
    axes = list(axes.flat) if hasattr(axes, "flat") else list(axes)
    labels = labels or [f"({c})" for c in "abcdefgh"]
    for ax, lab in zip(axes, labels):
        ax.text(x, y, lab, transform=ax.transAxes, fontweight=weight,
                fontsize=FONT_SIZE, va="bottom", ha="right")


def save(fig, path) -> Path:
    """Write the figure and refuse silently-wrong output.

    Checks that every axis carries BOTH an x and a y label, because an unlabelled
    axis is the single most common figure defect and it is trivially preventable.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    missing = []
    for i, ax in enumerate(fig.axes):
        if not ax.get_xlabel().strip():
            missing.append(f"axis {i}: no x label")
        if not ax.get_ylabel().strip():
            missing.append(f"axis {i}: no y label")
    if missing:
        raise ValueError(
            f"{path.name}: every axis needs a quantity AND a unit.\n  "
            + "\n  ".join(missing)
        )

    fig.savefig(path)
    plt.close(fig)
    print(f"style.save: wrote {path} at {DPI} dpi")
    return path
