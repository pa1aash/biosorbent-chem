#!/usr/bin/env python3
r"""Two audits of the numbers in the report.

1. BARE NUMERIC LITERALS. Flags numbers hard-coded in .tex that should arrive
   through \num{key}. Numbers that are part of the METHOD -- a concentration in
   a protocol sentence, a temperature, an instrument setting -- are legitimate
   and are whitelisted by context; numbers that are RESULTS are not.

2. CONSISTENCY AUDIT (Bible section 12). Every headline number must appear
   IDENTICALLY in the abstract, in Results and in the Conclusion. Mismatched
   numbers across sections are the fastest way to lose a referee's trust.

    python scripts/check_numbers.py
    python scripts/check_numbers.py --strict
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"

# Contexts in which a numeric literal is legitimate: it is a setting, not a result.
SAFE_CONTEXT = re.compile(
    r"\\(?:SI|SIrange|qty|qtyrange|num|sinum|numrange|ang|si|unit|label|ref|cref|Cref|"
    r"cite|includegraphics|input|include|usepackage|documentclass|setcounter|"
    r"addtocounter|setlength|addtolength|vspace|hspace|parbox|rule|scalebox|"
    r"multirow|multicolumn|arraystretch|columnwidth|linewidth|textwidth|"
    r"definecolor|colorbox|textcolor|fbox|pagenumbering|thepage|ce|setstretch|"
    r"begin|end|section|subsection|subsubsection|caption|footnote)\b"
)

# A numeral that is immediately a LENGTH or a structural coordinate is layout,
# not a result.
LAYOUT_SUFFIX = re.compile(r"^\s*(?:\\linewidth|\\textwidth|\\columnwidth|"
                           r"mm|cm|pt|em|ex|in|\]|\}|%)")

NUMBER = re.compile(r"(?<![\w.\\])(\d+\.\d+|\d{2,})(?![\w.])")

PLACEHOLDER_LINE = re.compile(r"\\(?:PENDING|NEEDSDATA|TODOPAL|verdict|finding)\b")

# The Bible's headline-number list, generalised: any number appearing in the
# abstract must reappear in Results and Conclusion.
SECTION_FILES = {
    "abstract":   REPORT / "frontmatter" / "abstract.tex",
    "results":    REPORT / "sections" / "04_results.tex",
    "conclusion": REPORT / "sections" / "05_conclusion.tex",
}


def strip_comment(line: str) -> str:
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2]); i += 2; continue
        if c == "%":
            break
        out.append(c); i += 1
    return "".join(out)


def numeric_tokens(text: str) -> set[str]:
    """Numbers reaching the reader, i.e. those inside \num{} -- the only legal route."""
    return set(re.findall(r"\\num\{([A-Za-z0-9_]+)\}", text))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    problems = 0

    # --- audit 1: bare numeric literals -------------------------------------
    print("=" * 74)
    print("AUDIT 1 -- bare numeric literals that should be \\num{key}")
    print("=" * 74)
    # SCOPE: only where RESULTS are stated. The preamble is typesetting
    # machinery; the cover and the abstract head carry the registration number
    # and the year; the abbreviation list defines symbols. None of those is a
    # result, and auditing them produces noise that hides the real finding.
    audit_paths = sorted((REPORT / "sections").glob("*.tex"))
    hits = []
    for path in audit_paths:
        if "build" in path.parts or path.name == "numbers.tex":
            continue
        for lineno, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
            line = strip_comment(raw)
            if not line.strip():
                continue
            # Placeholder text is SCAFFOLDING, not report content: it carries
            # registry IDs ("registry 4.11"), dataset IDs ("DS-08") and section
            # references. It is guaranteed gone from the final build by
            # check_placeholders.py, so auditing its numerals is noise.
            if PLACEHOLDER_LINE.search(line):
                continue
            for m in NUMBER.finditer(line):
                window = line[max(0, m.start() - 40):m.start()]
                if SAFE_CONTEXT.search(window):
                    continue
                if LAYOUT_SUFFIX.match(line[m.end():]):
                    continue
                hits.append((path.relative_to(ROOT), lineno, m.group(1), line.strip()[:90]))
    if hits:
        for path, lineno, tok, text in hits:
            print(f"  {path}:{lineno}  '{tok}'")
            print(f"      {text}")
        print(f"\n  {len(hits)} bare literal(s). Each is either a METHOD setting (fine --")
        print("  wrap it in \\SI{} so it is recognised) or a RESULT (not fine -- route it")
        print("  through data/CANONICAL_NUMBERS.yaml and \\num{key}).")
        problems += len(hits)
    else:
        print("  PASS -- no bare numeric literals outside safe contexts.")

    # --- audit 2: triple-anchoring ------------------------------------------
    print()
    print("=" * 74)
    print("AUDIT 2 -- consistency: every abstract number in Results AND Conclusion")
    print("=" * 74)
    present = {}
    for name, path in SECTION_FILES.items():
        if not path.exists():
            print(f"  {name}: {path.relative_to(ROOT)} missing -- skipped")
            present[name] = set()
            continue
        present[name] = numeric_tokens(path.read_text(errors="replace"))

    abstract_keys = present.get("abstract", set())
    if not abstract_keys:
        print("  Abstract states no \\num{} keys yet -- nothing to cross-check.")
        print("  (Expected while the abstract is still a placeholder; the abstract is")
        print("   written last, from the finished report.)")
    else:
        missing = defaultdict(list)
        for key in sorted(abstract_keys):
            for where in ("results", "conclusion"):
                if key not in present[where]:
                    missing[key].append(where)
        if missing:
            for key, wheres in missing.items():
                print(f"  '{key}' in abstract but NOT in: {', '.join(wheres)}")
            print(f"\n  {len(missing)} headline number(s) not triple-anchored.")
            problems += len(missing)
        else:
            print(f"  PASS -- all {len(abstract_keys)} abstract number(s) appear in both.")

    # --- audit 3: forbidden word --------------------------------------------
    print()
    print("=" * 74)
    print("AUDIT 3 -- 'significantly' without a p-value (Bible section 12)")
    print("=" * 74)
    sig = []
    for path in sorted(REPORT.rglob("*.tex")):
        if "build" in path.parts:
            continue
        for lineno, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
            line = strip_comment(raw)
            if re.search(r"\bsignificant(ly)?\b", line, re.I) and not re.search(r"\bp\s*[=<]", line):
                sig.append((path.relative_to(ROOT), lineno, line.strip()[:90]))
    if sig:
        for path, lineno, text in sig:
            print(f"  {path}:{lineno}\n      {text}")
        print("\n  Use 'markedly' or 'substantially' unless a test was run.")
        problems += len(sig)
    else:
        print("  PASS")

    print()
    print("=" * 74)
    if problems:
        print(f"check_numbers: {problems} issue(s)")
        return 1 if args.strict else 0
    print("check_numbers: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
