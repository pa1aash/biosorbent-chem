<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# dft/hetzner/ — Compute provisioning and job management

## What belongs here

- Provisioning script taking a fresh Debian/Ubuntu x86-64 instance to a working ORCA installation.
- Job-submission wrapper and results-sync script.
- Instance sizing notes and measured wall-clock per job class.

## What must never go here

- Credentials, API tokens, SSH private keys or any secret. These are gitignored; leaking one is worse than losing the compute.
- The ORCA tarball itself — it is licence-restricted and must not be redistributed.
