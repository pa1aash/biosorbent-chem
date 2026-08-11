#!/usr/bin/env python3
r"""Fail the final build on any surviving placeholder.

Scans report/ for \PENDING, \NEEDSDATA, \TODOPAL and the bare markers TODO, XX
and TBD, and lists each with its file and line.

    python scripts/check_placeholders.py           # report only, exit 0
    python scripts/check_placeholders.py --strict  # exit 1 if any remain

A placeholder is resolved by SUPPLYING THE EVIDENCE, never by deleting the
marker (CLAUDE.md section 4).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"

# Bare markers. Word-boundary anchored so that 'XX' does not match inside a word
# and TODO does not match TODOPAL, which is reported under its own name.
PATTERNS = [
    ("PENDING",   re.compile(r"\\PENDING\b")),
    ("NEEDSDATA", re.compile(r"\\NEEDSDATA\b")),
    ("TODOPAL",   re.compile(r"\\TODOPAL\b")),
    ("TODO",      re.compile(r"(?<!\\)\bTODO\b(?!PAL)")),
    ("XX",        re.compile(r"(?<![\w\\])XX(?![\w])")),
    ("TBD",       re.compile(r"(?<![\w\\])TBD(?![\w])")),
]

# preamble/ is typesetting machinery: it DEFINES the placeholder macros, it does
# not use them. Counting those definitions would inflate the tally and make it
# disagree with the build's own count.
SKIP_DIRS = {"build", "preamble"}


def strip_comment(line: str) -> str:
    """Remove a LaTeX comment, respecting \\%."""
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2]); i += 2; continue
        if c == "%":
            break
        out.append(c); i += 1
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="exit non-zero if any remain")
    ap.add_argument("--include-comments", action="store_true",
                    help="also scan LaTeX comments (they hold the build checklists)")
    args = ap.parse_args()

    findings = []
    for path in sorted(REPORT.rglob("*.tex")):
        if any(p in SKIP_DIRS for p in path.relative_to(REPORT).parts):
            continue
        if path.name == "numbers.tex":
            continue
        for lineno, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
            line = raw if args.include_comments else strip_comment(raw)
            for name, pat in PATTERNS:
                if pat.search(line):
                    findings.append((name, path.relative_to(ROOT), lineno, raw.strip()[:100]))

    if not findings:
        print("check_placeholders: PASS -- no placeholders remain.")
        return 0

    counts = {}
    for name, *_ in findings:
        counts[name] = counts.get(name, 0) + 1

    print(f"check_placeholders: {len(findings)} placeholder(s) outstanding\n")
    for name in ("PENDING", "NEEDSDATA", "TODOPAL", "TODO", "XX", "TBD"):
        if name in counts:
            print(f"  {name:<10} {counts[name]}")
    print()
    for name, path, lineno, text in findings:
        print(f"  {name:<10} {path}:{lineno}")
        print(f"             {text}")

    print("\n  Each of these is remaining work, quantified. Resolve a placeholder by")
    print("  supplying the evidence behind it -- never by deleting the marker.")
    print("  See docs/DATA_REQUEST.md and docs/03_DECISIONS.md.")

    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
