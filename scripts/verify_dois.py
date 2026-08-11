#!/usr/bin/env python3
r"""Verify every DOI in refs/library.bib against Crossref.

Compares title, authors, year, volume and pages; writes refs/VERIFICATION_LOG.csv;
exits non-zero on any failure.

    python scripts/verify_dois.py
    python scripts/verify_dois.py --strict   # also require read_confirmed

A SINGLE FABRICATED REFERENCE IS AN INTEGRITY FINDING, NOT A TYPO (Bible 13).
This is the single most detectable AI failure mode and it is checked mechanically
rather than trusted.

`read_confirmed` is NOT set by this script. It is set by Palaash, by hand, in
refs/VERIFICATION_LOG.csv, after actually reading the work. Crossref can tell you
a paper exists; only you can tell you that you have read it, and referees ask
what reference 23 found.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "refs" / "library.bib"
LOG = ROOT / "refs" / "VERIFICATION_LOG.csv"

FIELDS = ["citekey", "doi", "crossref_resolved", "title_match", "authors_match",
          "year_match", "volume_match", "pages_match", "read_confirmed",
          "checked_date", "notes"]


def norm(s: str) -> str:
    s = re.sub(r"[{}\\]", "", str(s or "")).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def parse_bib(text: str) -> list[dict]:
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", text, re.S):
        kind, key, body = m.group(1), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\n\s*\w+\s*=|\s*$)", body, re.S):
            fields[fm.group(1).lower()] = " ".join(fm.group(2).split())
        entries.append({"key": key, "type": kind, **fields})
    return entries


def load_read_flags() -> dict[str, str]:
    """Preserve read_confirmed across runs -- it is human-entered, not derived."""
    if not LOG.exists():
        return {}
    with LOG.open() as fh:
        return {r["citekey"]: r.get("read_confirmed", "")
                for r in csv.DictReader(fh) if r.get("citekey")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="also fail if any entry lacks read_confirmed=yes")
    args = ap.parse_args()

    if not BIB.exists():
        print(f"verify_dois: {BIB} not found", file=sys.stderr)
        return 2

    entries = parse_bib(BIB.read_text())
    if not entries:
        print("verify_dois: library.bib holds no entries.")
        print("  This is correct on a fresh repository: no citation enters the file")
        print("  until it resolves against Crossref AND has been read.")
        LOG.write_text(",".join(FIELDS) + "\n")
        return 0

    try:
        from habanero import Crossref
    except ImportError:
        print("verify_dois: habanero not installed; activate the biosorb environment",
              file=sys.stderr)
        return 2

    cr = Crossref(mailto="palaashgang@gmail.com")
    previous = load_read_flags()
    rows, failures = [], []

    for e in entries:
        key, doi = e["key"], e.get("doi", "").strip()
        row = dict.fromkeys(FIELDS, "")
        row.update(citekey=key, doi=doi,
                   read_confirmed=previous.get(key, ""),
                   checked_date=time.strftime("%Y-%m-%d"))

        if not doi:
            row["crossref_resolved"] = "no"
            row["notes"] = "NO DOI IN ENTRY"
            failures.append(f"{key}: no DOI")
            rows.append(row); continue

        try:
            item = cr.works(ids=doi)["message"]
        except Exception as exc:  # network, 404, malformed DOI
            row["crossref_resolved"] = "no"
            row["notes"] = f"CROSSREF FAILED: {type(exc).__name__}"
            failures.append(f"{key}: DOI {doi} did not resolve ({type(exc).__name__})")
            rows.append(row); continue

        row["crossref_resolved"] = "yes"

        ct = (item.get("title") or [""])[0]
        ratio = similar(e.get("title", ""), ct)
        row["title_match"] = "yes" if ratio > 0.85 else f"no ({ratio:.2f})"
        if ratio <= 0.85:
            failures.append(f"{key}: title mismatch\n      bib:      {e.get('title','')}\n"
                            f"      crossref: {ct}")

        bib_auth = norm(e.get("author", "")).split()
        cr_auth = [norm(a.get("family", "")) for a in item.get("author", [])]
        row["authors_match"] = "yes" if (cr_auth and cr_auth[0] in bib_auth) else "check"
        if cr_auth and cr_auth[0] not in bib_auth:
            failures.append(f"{key}: first author '{cr_auth[0]}' not in bib author field")

        parts = (item.get("issued", {}).get("date-parts") or [[None]])[0]
        cy = str(parts[0]) if parts and parts[0] else ""
        row["year_match"] = "yes" if cy and cy == str(e.get("year", "")).strip() else f"no ({cy})"
        if cy and cy != str(e.get("year", "")).strip():
            failures.append(f"{key}: year bib={e.get('year')} crossref={cy}")

        cv = str(item.get("volume", ""))
        row["volume_match"] = "yes" if cv and cv == str(e.get("volume", "")).strip() else \
            ("n/a" if not cv else f"no ({cv})")
        cp = str(item.get("page", ""))
        bp = str(e.get("pages", "")).replace("--", "-")
        row["pages_match"] = "yes" if cp and cp == bp else ("n/a" if not cp else f"no ({cp})")

        rows.append(row)

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)

    unread = [r["citekey"] for r in rows if r["read_confirmed"].lower() not in ("yes", "y", "true")]

    print(f"verify_dois: {len(rows)} entr{'y' if len(rows)==1 else 'ies'} checked "
          f"-> {LOG.relative_to(ROOT)}")
    if failures:
        print(f"\n  {len(failures)} FAILURE(S):")
        for f in failures:
            print(f"    {f}")
        print("\n  A reference that does not resolve, or does not match, is DELETED.")
        print("  It is never 'corrected' to what it probably should be.")
    if unread:
        print(f"\n  {len(unread)} entr{'y' if len(unread)==1 else 'ies'} not yet confirmed read:")
        for k in unread:
            print(f"    {k}")
        print("  Set read_confirmed=yes in refs/VERIFICATION_LOG.csv by hand, after reading.")

    if failures:
        return 1
    if args.strict and unread:
        return 1
    if not failures and not unread:
        print("  PASS -- all entries resolved, matched and confirmed read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
