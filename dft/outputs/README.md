<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->

# dft/outputs/ — Raw calculation output

## What belongs here

- ORCA/PySCF output files, synced back from the Hetzner instances by `hetzner/sync_results.sh`.
- Frequency output confirming all-real modes for every optimised minimum.
- <S^2> values for every open-shell species (Cu(II) is d9, doublet — Attack #2).

## What must never go here

- Large binary scratch files (.gbw, .tmp, .densities) — these are gitignored.
- Outputs from an aborted or non-converged job, unless explicitly retained and labelled as such.
