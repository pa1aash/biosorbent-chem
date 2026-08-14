<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# Session record — S05, 14 August 2026

**Tool:** Claude Opus 5 (`claude-opus-5[1m]`), via Claude Code
**Stage:** computational arm — stalled queue diagnosed, launcher rebuilt, queue relaunched
**Duration:** 14 August 2026, from approximately 11:23 IST; queue relaunched 11:40 IST
**Corresponding row:** `logs/ai_use_log.csv`, session `S05`

---

> ## ⚠ THIS FILE IS A SESSION *RECORD*, NOT THE VERBATIM CHAT EXPORT
>
> Per `CLAUDE.md` §7.1, a session record is **never** a substitute for the verbatim client export.
> This document is an accurate account of what the session did; it is **not** the chat log.
>
> **Palaash must export the verbatim transcript from the Claude Code client into
> `logs/sessions/`.** Appendix A is assembled from the exports, not from these records.
>
> `\TODOPAL{export the verbatim S05 transcript to logs/sessions/ and reference it here}`

---

## What the session was asked to do

Diagnose why the S04 production queue stopped after 3 of 17 jobs with zero failures and a clean
`QUEUE END`, fix it, reorder the remaining jobs by dependency, retune concurrency, relaunch, and
harvest and analyse what had already completed.

## Root cause

**A shared stdin file offset — in the launcher the assistant wrote in S04.**

`run_queue.sh` v1 fed the job list to its dispatch loop on stdin (`done < "$ORDER"`) and invoked
ORCA without redirecting stdin. Each backgrounded job inherited file descriptor 0 pointing at
`JOB_ORDER.txt`, **sharing its file offset with the parent loop**. ORCA's `mpirun` reads stdin,
consumed the remaining fourteen job lines, and advanced the shared offset to end-of-file. The
parent's next `read` returned EOF, the loop exited normally, `wait` drained the two running jobs,
and the queue logged a clean `QUEUE END`. Nothing failed; fourteen jobs were never dispatched.

The hypothesis supplied in the brief was **correct in mechanism and wrong in detail** — it proposed
`xargs`, and there was no `xargs`. This was checked against the actual source rather than assumed,
and the queue-log timeline was read to confirm that no job started after the third dispatch.

## The second defect, which was worse

Found while fixing the first: **`ORCA TERMINATED NORMALLY` is not a completion test, and S04 used
it as one.** ORCA prints that banner even when the geometry optimiser exhausts its cycle cap and
the frequency calculation never runs.

`pb_P0_cplx` had been logged as FINISHED after 3h06m. It had in fact run **102 optimisation cycles
without converging, produced no frequencies and no `.hess` file**, and printed the banner anyway.
102 is exactly ORCA's default cap of 3 × N_atoms for 34 atoms; `cu_P0_cplx` converged at 88 of the
same 102, so the margin was one job wide.

**The true S04 result was 2 complete jobs, not 3.** Had the new skip logic shipped with the old
test, the relaunch would have skipped a job that produced no free energy. The completion test now
requires normal termination **and** the frequency section **and** the `.hess` file, in
`run_queue.sh`, `scripts/dft_status.sh` and `scripts/dft_harvest.sh`.

Both defects were in code the assistant wrote in S04. The second fails silently in the direction of
appearing successful, which is the more dangerous kind.

## What was changed

| Change | Why |
|---|---|
| Job list read on **fd 3**; ORCA invoked with **`< /dev/null`** | Two independent defences against the stdin fault |
| Launcher logs **`DISPATCH COMPLETE \| lines read N of M`** | Observability was the real gap — this surfaces the fault in seconds, not fifteen hours |
| **Three-part completion test** | A job with no frequencies has no free energy, whatever the banner says |
| **Scheduling by total cores** (cap 16); 4 cores for small species, 8 for complexes | ~35–40% more throughput on the small group; memory invariant unchanged at 24 GB |
| **Reordered by dependency** — aquo ions and ligands first | They gate every reaction free energy; the S04 order optimised makespan, the wrong objective |
| **`%geom MaxIter 300`** on every not-yet-complete input | A resource cap, not a convergence criterion; does not touch TightOPT |
| **`pb_P0_cplx` restarts from its S04 final geometry** | Preserves three hours of optimisation; same trajectory, same level of theory |
| **`water` and `cu_P0_cplx` inputs frozen** at their S04 form | Their `.inp` is provenance for a finished calculation and must keep describing what ran |

## Verification before and after launch

- The corrected skip logic was proved by a **`--dry-run` before anything was launched**: 2 skipped,
  15 to run, `pb_P0_cplx` correctly not skipped, **17 of 17 lines read**.
- After launch: 4 driver processes + 16 MPI ranks, **CPU 1594% of 1600%**, **ORCA RSS 2.4 GB
  against 28 GB available**, all four `.out` files growing.
- A `rsync --delete` used during the upload was **audited immediately afterwards** to confirm it had
  not destroyed any completed output. It had not — excluded files are protected from deletion by
  default — but the check was run rather than assumed.
- Three defects in the operator scripts were found and fixed while testing them: `mapfile` is absent
  from macOS's bash 3.2, macOS ships `openrsync` which rejects `--info=name1`, and the new
  two-column `JOB_ORDER.txt` broke a job-name parser that stripped all whitespace.

## Results from the completed jobs

`dft/analysis/qc_checkpoint.py` was written to implement protocol §3.2, §3.4 and §3.7, reusing the
first-shell cutoffs of `structures/geom_utils.py`. It parses frequencies **natively** because
**cclib 1.8.1 cannot parse ORCA 6.1.1 output** — it aborts in the SCF convergence block — and the
mandatory all-real check must not depend on a parser that fails silently.

- **`water`** — 9 modes, 0 imaginary.
- **`cu_P0_cplx`** — 102 modes, **0 imaginary**, lowest real 28.65 cm⁻¹ (well below the 100 cm⁻¹
  quasi-RRHO threshold, which shows that treatment is doing real work). **⟨S²⟩ = 0.7518** against
  the ideal 0.750, a deviation of 0.24%.

### A31 partly resolved

**Cu(II) P0 is monodentate at the production level of theory**: Cu–O(galloyl) **2.048 Å** and
**3.692 Å** against a 2.80 Å cutoff, first shell 5 O (1 ligand + 4 water). The GFN2-xTB pre-screen
was **not an artefact** — DFT makes the split more pronounced. **Protocol §3.8 Case B binds.**

The unconverged `pb_P0_cplx` geometry is also provisionally monodentate (2.845 / 3.842 Å). **This
was explicitly not reported as a finding**, because the geometry did not converge. If it survives
the re-run, and if zinc follows, this is §3.8 **Case C** rather than Case B — which would restore
comparability at P0 on a matched basis.

## What was NOT done

- **No report prose.** No number added to `data/CANONICAL_NUMBERS.yaml`; no citation added to
  `refs/library.bib`.
- **The convergence criteria were not touched.** Loosening TightOPT would be a protocol change
  requiring the author's ruling and would have to apply to all three metals. Raised as **D-07**.
- **No verbatim transcript was generated, reconstructed or simulated.**
- The instance was not destroyed or reconfigured; `vendor/orca/` was not touched.

## Outstanding

| Item | State |
|---|---|
| **Verbatim exports for S01–S05** | **ALL FIVE STILL OWED.** Appendix A is assembled from exports, not records. |
| **D-07** — TightOPT on floppy aquo complexes | Live risk. Needs a ruling only if it recurs at the 300-cycle cap. |
| Denticity for the remaining 8 complexes | §3.7 requires all nine |
| ⟨S²⟩ for the other three Cu species | Running or queued |
| Multiwfn | Still not installed; **A01 OPEN** |
| **Instance destruction** | **$0.493/hr; stopping does not halt billing.** Destroy after harvest. |
