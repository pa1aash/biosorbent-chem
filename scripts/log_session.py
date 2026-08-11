#!/usr/bin/env python3
r"""Append a session to logs/ai_use_log.csv.

The Acknowledgement's AI declaration and Appendix A are GENERATED from this
file. The 2026 rules require names and versions, specific stages and purposes,
and timing and frequency, with chat records attached for verification.

This log exists so the declaration is accurate rather than reconstructed on
16 August. An inaccurate declaration is a live disqualification vector.

    python scripts/log_session.py \
        --tool "Claude Opus 5" --version "claude-opus-5" \
        --stage "repository setup and build infrastructure" \
        --purpose "specification extraction, protocol audit, ..." \
        --output-use "reviewed and committed; all numbers left as placeholders" \
        --verification "compiled the document; ran the unit tests; ..." \
        --transcript "2026-08-11_session01.md"
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs" / "ai_use_log.csv"
SESSIONS = ROOT / "logs" / "sessions"

FIELDS = ["date", "tool_and_version", "session_id", "project_stage",
          "specific_purpose", "what_was_done_with_output", "how_verified",
          "transcript_filename"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=time.strftime("%Y-%m-%d"))
    ap.add_argument("--tool", required=True)
    ap.add_argument("--version", default="")
    ap.add_argument("--session-id", default="")
    ap.add_argument("--stage", required=True)
    ap.add_argument("--purpose", required=True)
    ap.add_argument("--output-use", required=True,
                    help="what was actually done with the output")
    ap.add_argument("--verification", required=True,
                    help="how the output was verified -- REQUIRED by the rules")
    ap.add_argument("--transcript", required=True,
                    help="filename in logs/sessions/")
    ap.add_argument("--show", action="store_true", help="print the log and exit")
    args = ap.parse_args()

    LOG.parent.mkdir(parents=True, exist_ok=True)
    SESSIONS.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        with LOG.open("w", newline="") as fh:
            csv.writer(fh).writerow(FIELDS)

    if args.show:
        print(LOG.read_text())
        return 0

    n = max(0, len(LOG.read_text().splitlines()) - 1)
    sid = args.session_id or f"S{n+1:02d}"
    tool = f"{args.tool} ({args.version})" if args.version else args.tool

    with LOG.open("a", newline="") as fh:
        csv.writer(fh).writerow([
            args.date, tool, sid, args.stage, args.purpose,
            args.output_use, args.verification, args.transcript,
        ])

    print(f"log_session: appended {sid} to {LOG.relative_to(ROOT)}")
    tpath = SESSIONS / args.transcript
    if not tpath.exists():
        print(f"  REMINDER: {tpath.relative_to(ROOT)} does not exist yet.")
        print("  Export the transcript now. Do not reconstruct it later --")
        print("  the chat records are submitted for verification (Appendix A).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
