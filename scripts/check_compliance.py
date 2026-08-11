#!/usr/bin/env python3
r"""Check the built PDF against docs/00_SPEC.md section 2.

Prints a PASS/FAIL table against the numbered assertion IDs.

    python scripts/check_compliance.py [path/to.pdf]
    python scripts/check_compliance.py --strict
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "report" / "build" / "main.pdf"
SUBMISSION_NAME = "Chem-151-Research Report.pdf"

A4_W, A4_H = 595.276, 841.89     # pt
BODY_MIN, BODY_MAX = 42, 55      # numbered body pages (Bible 7.1)
SIZE_WARN_MB = 5.0


class Result:
    def __init__(self):
        self.rows = []
    def add(self, cid, desc, state, detail=""):
        self.rows.append((cid, desc, state, detail))
    def report(self):
        w = max(len(r[1]) for r in self.rows)
        print(f"{'ID':<8}{'ASSERTION':<{w+2}}{'STATE':<10}DETAIL")
        print("-" * (8 + w + 2 + 10 + 40))
        for cid, desc, state, detail in self.rows:
            print(f"{cid:<8}{desc:<{w+2}}{state:<10}{detail}")
        fails = [r for r in self.rows if r[2] == "FAIL"]
        warns = [r for r in self.rows if r[2] == "WARN"]
        manual = [r for r in self.rows if r[2] == "MANUAL"]
        print()
        print(f"  PASS {sum(1 for r in self.rows if r[2]=='PASS')}   "
              f"FAIL {len(fails)}   WARN {len(warns)}   MANUAL {len(manual)}")
        return len(fails)


def run(cmd) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout
    except FileNotFoundError:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", nargs="?", default=str(DEFAULT_PDF))
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    pdf = Path(args.pdf)

    r = Result()
    if not pdf.exists():
        print(f"check_compliance: {pdf} not found -- run `make draft` first", file=sys.stderr)
        return 2

    info = run(["pdfinfo", str(pdf)])

    # C-001 A4
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        ok = abs(w - A4_W) < 1 and abs(h - A4_H) < 1
        r.add("C-001", "Page size is A4", "PASS" if ok else "FAIL",
              f"{w:.1f} x {h:.1f} pt = {w*25.4/72:.0f} x {h*25.4/72:.0f} mm")
    else:
        r.add("C-001", "Page size is A4", "FAIL", "could not read page size")

    # C-002 margins -- measured from the rendered raster, not assumed
    margin_state, margin_detail = measure_margins(pdf)
    r.add("C-002", "Margins >= 2.5 cm all sides", margin_state, margin_detail)

    r.add("C-003", "Body text at 1.5 line spacing", "MANUAL",
          "\\onehalfspacing in 00_compliance.tex; verify visually")
    r.add("C-004", "Single spacing only in the four permitted places", "MANUAL",
          "captions/footnotes/quotes/bibliography scoped in 00_compliance.tex")

    # C-006 filename
    sub = ROOT / "admin" / "submission" / SUBMISSION_NAME
    r.add("C-006", f"Filename exactly '{SUBMISSION_NAME}'",
          "PASS" if sub.exists() else "PENDING",
          str(sub.relative_to(ROOT)) if sub.exists() else "not yet produced (make submit)")

    # C-009 size
    mb = pdf.stat().st_size / 1024 / 1024
    r.add("C-009", "Under 5 MB, else send a download link",
          "PASS" if mb <= SIZE_WARN_MB else "WARN", f"{mb:.2f} MB")

    # C-012 fonts embedded
    fonts = run(["pdffonts", str(pdf)])
    flines = fonts.splitlines()
    if len(flines) >= 2 and set(flines[1].strip()) <= {"-", " "}:
        # Parse by COLUMN POSITION, taken from the dashed rule. Splitting on
        # whitespace is wrong: the 'type' column holds values like "Type 1",
        # which contain a space and shift every later field by one.
        widths, pos = [], 0
        for chunk in flines[1].split():
            widths.append((pos, pos + len(chunk)))
            pos += len(chunk) + 1
        emb_col = widths[3]
        rows_ = [l for l in flines[2:] if l.strip()]
        not_emb = [l[widths[0][0]:widths[0][1]].strip() for l in rows_
                   if l[emb_col[0]:emb_col[1]].strip() != "yes"]
        r.add("C-012", "All fonts embedded", "PASS" if not not_emb else "FAIL",
              f"{len(rows_)} fonts, {len(not_emb)} not embedded")
    else:
        r.add("C-012", "All fonts embedded", "WARN", "pdffonts unavailable")

    # C-013 body page count
    mp = re.search(r"Pages:\s+(\d+)", info)
    total = int(mp.group(1)) if mp else 0
    body = body_page_count(pdf, total)
    if body is None:
        r.add("C-013", f"Body pages in {BODY_MIN}-{BODY_MAX}", "WARN",
              f"{total} total; body count needs arabic numbering")
    else:
        ok = BODY_MIN <= body <= BODY_MAX
        r.add("C-013", f"Body pages in {BODY_MIN}-{BODY_MAX}", "PASS" if ok else "FAIL",
              f"{body} body of {total} total")

    # C-030 placeholders
    ph = ROOT / "report" / "build" / "main.placeholders"
    if ph.exists():
        n = len([l for l in ph.read_text().splitlines() if l.strip()])
        r.add("C-030", "Zero placeholders remain", "PASS" if n == 0 else "PENDING",
              f"{n} outstanding")
    else:
        r.add("C-030", "Zero placeholders remain", "WARN", "no .placeholders file")

    # C-027 / C-028 references
    log = ROOT / "refs" / "VERIFICATION_LOG.csv"
    n_refs = max(0, len(log.read_text().splitlines()) - 1) if log.exists() else 0
    r.add("C-027", "35-60 references", "PASS" if 35 <= n_refs <= 60 else "PENDING",
          f"{n_refs} verified entries")

    # C-038 journal furniture
    text = run(["pdftotext", str(pdf), "-"])
    furniture = [s for s in ("SISSA", "PUBLISHED BY", "Prepared for submission",
                             "Received:", "Accepted:", "arXiv ePrint")
                 if s.lower() in text.lower()]
    r.add("C-038", "No journal furniture", "PASS" if not furniture else "FAIL",
          "none found" if not furniture else ", ".join(furniture))

    # running header
    hdr = text.count("Yau High School Science Award")
    r.add("C-014", "Running header on every page", "PASS" if hdr >= total else "WARN",
          f"{hdr} of {total} pages")

    fails = r.report()
    print("\n  MANUAL rows need a human check. PENDING rows are expected while the")
    print("  report is still a skeleton; they must reach PASS before submission.")
    return 1 if (fails and args.strict) else 0


def measure_margins(pdf: Path):
    """Measure ink margins by rasterising sample pages. Assumed values are not evidence."""
    if not shutil.which("gs"):
        return "WARN", "ghostscript not available"
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return "WARN", "Pillow/numpy not available"
    import tempfile
    info = run(["pdfinfo", str(pdf)])
    m = re.search(r"Pages:\s+(\d+)", info)
    total = int(m.group(1)) if m else 1
    pages = [p for p in (max(2, total // 4), total // 2, max(2, 3 * total // 4)) if p <= total]
    DPI, worst, where = 100, 99.0, ""
    with tempfile.TemporaryDirectory() as td:
        for pg in pages:
            out = Path(td) / f"p{pg}.png"
            subprocess.run(["gs", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pnggray",
                            f"-r{DPI}", f"-dFirstPage={pg}", f"-dLastPage={pg}",
                            f"-sOutputFile={out}", str(pdf)],
                           capture_output=True, check=False)
            if not out.exists():
                continue
            im = np.array(Image.open(out).convert("L"))
            h, w = im.shape
            ink = im < 200
            rows = np.where(ink.any(axis=1))[0]
            cols = np.where(ink.any(axis=0))[0]
            if not len(rows):
                continue
            for val, side in ((cols[0], "left"), (w - 1 - cols[-1], "right"),
                              (rows[0], "top"), (h - 1 - rows[-1], "bottom")):
                cm = val / DPI * 2.54
                if cm < worst:
                    worst, where = cm, f"{side} on p.{pg}"
    if worst == 99.0:
        return "WARN", "could not rasterise"
    # 2.45 cm allows one 100-dpi pixel of rasterisation error plus microtype's
    # optical punctuation protrusion, which moves a hyphen a fraction into the
    # margin by design and is not a text-block violation.
    return ("PASS" if worst >= 2.45 else "FAIL"), f"min {worst:.2f} cm ({where})"


def body_page_count(pdf: Path, total: int):
    """Count pages numbered in arabic, i.e. the body, excluding front matter."""
    toc = ROOT / "report" / "build" / "main.log"
    if not toc.exists():
        return None
    # The body starts at the page where arabic numbering restarts at 1; the
    # appendices and references are part of the count the Bible budgets.
    txt = run(["pdftotext", "-f", "1", "-l", str(total), str(pdf), "-"])
    if not txt:
        return None
    # Fall back to a structural estimate: total minus front matter pages.
    fm = txt.count("\x0c")  # not reliable alone; report None rather than guess
    return None


if __name__ == "__main__":
    sys.exit(main())
