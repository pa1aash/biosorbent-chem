<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# scripts/ — Build, validation and compliance tooling

## What belongs here

- `emit_numbers.py`, `verify_dois.py`, `check_placeholders.py`, `check_numbers.py`, `check_compliance.py`, `ingest.py`, `log_session.py`, `new_figure.py`, `install_hooks.sh`, `env.sh`.
- Every script sources `env.sh`.

## What must never go here

- A script that silently coerces or repairs bad input. Scripts report mismatches; humans decide.
- A check that can be skipped in the `final` build target.
