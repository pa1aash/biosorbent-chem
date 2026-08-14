<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# ORCA PRODUCTION QUEUE — LAUNCH RECORD

**Current as of 2026-08-14, 11:45 IST (S05 relaunch).** The S04 launch section is
retained below for the record; where the two disagree, this section is current.

> ## ⚠ THE INSTANCE MUST BE DESTROYED AFTER HARVEST
>
> **Vultr instance `65.20.67.245` bills at `$0.493/hr`.**
> **STOPPING THE INSTANCE DOES NOT HALT BILLING. ONLY DESTROYING IT DOES.**
>
> At $0.493/hr this is **$11.83/day**, accruing whether or not any job is running.
> The moment `scripts/dft_harvest.sh` has pulled back all seventeen jobs and the
> outputs have been verified, **destroy the instance**.

---

## 0. S05 RELAUNCH — 2026-08-14, 11:40 IST

### What went wrong with the S04 queue

**The S04 queue dispatched 3 of 17 jobs and then exited cleanly, reporting no failures.**
It sat idle for roughly fifteen hours before this was noticed.

**Root cause: a shared stdin file offset.** `run_queue.sh` v1 fed the job list to its dispatch
loop on stdin (`done < "$ORDER"`) and invoked ORCA without redirecting stdin
(`"$ORCA" "$job.inp" > "$job.out" 2>&1`). Each backgrounded job therefore inherited file
descriptor 0 pointing at `JOB_ORDER.txt`, **sharing its file offset with the parent loop**.
ORCA's `mpirun` reads stdin, consumed the remaining fourteen job lines, and advanced the shared
offset to end-of-file. The parent's next `read` returned EOF, the loop exited normally, `wait`
drained the two running jobs, and the queue logged a clean `QUEUE END`. **Nothing failed —
fourteen jobs were simply never dispatched.**

### A second, independent defect found while fixing the first

**`ORCA TERMINATED NORMALLY` is not a valid completion test, and S04 used it as one.** ORCA
prints that banner even when the geometry optimiser exhausts its iteration cap and the frequency
calculation never runs at all.

`pb_P0_cplx` did exactly that: **102 optimisation cycles, no convergence, no frequencies, no
`.hess` file — and a clean normal-termination banner.** 102 is precisely ORCA's default cap of
3 × N_atoms for a 34-atom species. `cu_P0_cplx` converged at 88 of the same 102, so the margin
was one job wide.

**The true S04 result is therefore 2 complete jobs, not 3.** The completion test in
`run_queue.sh`, `scripts/dft_status.sh` and `scripts/dft_harvest.sh` now requires all three of:
normal termination, the `VIBRATIONAL FREQUENCIES` section, and the `.hess` file on disk.

### What changed in the launcher

| Change | Why |
|---|---|
| Job list read on **file descriptor 3**, never stdin | A child that reads stdin cannot reach it |
| ORCA invoked with **`< /dev/null`** | No child has a readable stdin at all |
| Logs **`DISPATCH COMPLETE \| lines read N of M`** | The line that would have caught this in seconds rather than fifteen hours |
| **Skip on a three-part completion test** | Safely re-runnable; never re-runs finished work, never skips an unfinished job |
| **Scheduling by total cores**, not job count | Lets 4-core and 8-core jobs share the machine without a barrier |
| `--dry-run` mode | The skip logic was verified before launch, not after |

### Concurrency

**4 cores for the six small species, 8 cores for the complexes, scheduled against a 16-core cap.**
Memory is unchanged and the invariant is exact: ORCA runs one MPI process per core, the scheduler
caps total cores at 16, so peak nominal memory is 1500 MB × 16 = **24 GB against 29 GB available,
for any mix of job sizes**. Verified live after launch: **CPU 1594% of 1600%, total ORCA RSS
2.4 GB.**

The gain is throughput: ORCA's parallel efficiency at 8 cores for ~330-basis-function systems is
roughly 55–70%, against 80–90% at 4 cores, so four 4-core jobs do appreciably more useful work
than two 8-core jobs. The complexes keep 8 cores because they have more work per unit of
communication, and because per-job latency matters — the §3.7 denticity checkpoint cannot run
until individual complexes finish.

### New job order — by dependency, not by size

The S04 order was longest-processing-time-first, which starts with the jobs whose results nothing
else needs. **Every reaction free energy needs the three aquo ions and the ligand at its
protonation state**, so those six small, fast species now run first and gate everything downstream.

| Group | Jobs | Cores |
|---|---|---|
| 0 — complete, skipped | `water`, `cu_P0_cplx` | — |
| 1 — gates everything | `cu_aquo6`, `pb_aquo6`, `zn_aquo6`, `lig_P0_LH2`, `lig_P1_LH1m`, `lig_P2_L2m` | 4 |
| 2 — completes P0 | **`pb_P0_cplx` (RE-RUN)**, `zn_P0_cplx` | 8 |
| 3 — the P1 row | `cu_P1_cplx`, `pb_P1_cplx`, `zn_P1_cplx` | 8 |
| 4 — the P2 row | `cu_P2_cplx`, `pb_P2_cplx`, `zn_P2_cplx` | 8 |
| 5 — lowest priority | `pb_aquo8` | 4 |

`pb_P0_cplx` moved from group 0 to group 2: it is not complete, but it is a complex and gates
nothing, so it runs after the six species that do.

### Two protocol-adjacent changes, both recorded as decisions

1. **`%geom MaxIter 300`** added to every input that had not already completed. This is a
   **resource cap, not a convergence criterion** — it does not touch the TightOPT thresholds fixed
   by §3.4, only how long the optimiser may search for the same minimum. Applied uniformly so no
   species is treated differently from another.
2. **`pb_P0_cplx` restarts from its own S04 final geometry**, not from the S02 conformer. The S04
   attempt left the energy converged to ~5 × 10⁻⁵ Eh; discarding it would repeat three hours of
   work from a worse starting point. This is a continuation of the same trajectory at the same
   level of theory, and the provenance chain is written into the input file's header.

**`water` and `cu_P0_cplx` inputs are FROZEN at their S04 form** and regenerate byte-for-byte, so
they remain accurate provenance for the two finished calculations. Both converged far inside the
default cap (4 and 88 cycles), so `MaxIter` could not have changed either result.

### ⚠ RISK CARRIED FORWARD — TightOPT on floppy aquo complexes

`pb_P0_cplx` did not fail for lack of cycles alone. Its **energy** was converged to ~5 × 10⁻⁵ Eh
while its **`MAX step`** criterion oscillated — 0.023 → 0.215 → 0.254 → 0.075 → 0.097 → 0.046
against a 0.001 tolerance, with 1.9–3.7° dihedral swings. That is a floppy degree of freedom
(coordinated waters rotating on a flat plateau), exactly what `CONFORMER_SCREEN.md` §5
limitations 2 and 3 predicted.

**More cycles may not be enough.** `cu_P0_cplx` converged at 88, so the problem is not universal,
but if a complex reaches ~150 cycles it is probably oscillating rather than converging —
`scripts/dft_status.sh` now flags that. **If it recurs, the convergence criteria themselves need a
ruling from Palaash**, because loosening TightOPT is a protocol change and would have to be
applied to all three metals to keep the comparison controlled. No such change has been made.

---

## 1. LAUNCH (S04 — superseded by §0 above)

| | |
|---|---|
| **S04 launched** | 2026-08-13, 21:12 IST (15:42 UTC) — **queue stalled after 3 dispatches** |
| **S05 relaunched** | **2026-08-14, 11:40 IST (06:10 UTC)** |
| Session | S04, then S05 |
| Instance | `65.20.67.245`, Vultr, 16 vCPU / 30 GiB RAM / 469 GB disk |
| Remote path | `/opt/dft-jobs/` |
| tmux session | **`dft-queue`** — detached, survives SSH disconnection |
| Launcher | `/opt/dft-jobs/run_queue.sh` (tracked as `dft/run_queue.sh`) |
| Queue order | `/opt/dft-jobs/JOB_ORDER.txt` (tracked as `dft/inputs/JOB_ORDER.txt`) |
| Queue log | `/opt/dft-jobs/queue.log` |
| Concurrency | **2 jobs**, 8 cores each |
| Jobs submitted | **17** — 16 headline + 1 alternative (`pb_aquo8`) |

**Check status at any time, from any fresh session, with no prior context:**

```bash
bash scripts/dft_status.sh
```

**Harvest results (safe, incremental, re-runnable):**

```bash
bash scripts/dft_harvest.sh
```

---

## 2. LEVEL OF THEORY ACTUALLY USED

This is what is in the launched input files, not what was planned. Every setting is traceable to a
section of [`DFT_PROTOCOL.md`](DFT_PROTOCOL.md); the generator
[`make_orca_inputs.py`](make_orca_inputs.py) carries the section reference into each `.inp`.

```
! PBE0 D3BJ def2-TZVP def2/J RIJCOSX TightSCF DefGrid3 {RKS|UKS}
! Opt Freq TightOPT
```

| Field | Value | Protocol |
|---|---|---|
| Program | **ORCA 6.1.1 RELEASE** (GIT `487d211c`, built 2025-11-21) | — |
| Functional | PBE0, 25% exact exchange | §3 |
| Dispersion | D3(BJ) | §3 |
| Basis, all elements | def2-TZVP | §3.1 |
| **Pb core** | **def2-ECP = ECP60MDF, 60 core electrons, 22 in valence, scalar-relativistic** | §3.1 |
| Cu, Zn, C, H, O | all-electron | §3.1 |
| Auxiliary basis | def2/J | §3.1 |
| Acceleration | RIJCOSX | §3.4 |
| Solvation | SMD, water, applied **during** the optimisation | §3.3 |
| Geometry convergence | TightOPT | §3.4 |
| SCF convergence | TightSCF | §3.4 |
| Integration grid | DefGrid3 | §3.4 |
| Frequencies | **analytic** — confirmed: ORCA prints `SCF HESSIAN` + `POPLE LINEAR EQUATION SOLVER`, not a numerical displacement loop | §3.4 |
| Thermochemistry | quasi-RRHO below 100 cm⁻¹, applied in post-processing by `thermo.py`, **not** by an ORCA keyword — see [`inputs/README.md`](inputs/README.md) | §3.4 / REACTIONS.md §5.1 |
| `%pal nprocs` | 8 | hardware |
| `%maxcore` | **1500 MB** per process | hardware |

**On `%maxcore`.** The S04 brief specified 3000. That is 3000 × 8 procs × 2 concurrent jobs = **48 GB
nominal against 29 GB available**, a 1.65× overcommit that would have left multi-hour jobs at the
mercy of the OOM killer. ORCA's own sizing rule is ~75% of RAM ÷ total cores = 29000 × 0.75 / 16 ≈
1400. Raised before launch and **ruled down to 1500 by Palaash on 2026-08-13**. 1500 × 8 × 2 = 24 GB,
leaving ~5 GB headroom.

---

## 3. JOBS SUBMITTED

Queue order is longest-processing-time-first, with `water` first (cheap end-to-end validation) and
`pb_aquo8` last (not a headline job, so it can delay nothing).

| # | Job | Atoms | Charge | Mult | UKS | ECP | Role |
|---|---|---|---|---|---|---|---|
| 1 | `water` | 3 | 0 | 1 | no | — | released product, ×2 per equation |
| 2 | `cu_P0_cplx` | 34 | +2 | **2** | **yes** | — | product P0 |
| 3 | `pb_P0_cplx` | 34 | +2 | 1 | no | **ECP60MDF** | product P0 |
| 4 | `zn_P0_cplx` | 34 | +2 | 1 | no | — | product P0 |
| 5 | `cu_P1_cplx` | 33 | +1 | **2** | **yes** | — | product P1 |
| 6 | `pb_P1_cplx` | 33 | +1 | 1 | no | **ECP60MDF** | product P1 |
| 7 | `zn_P1_cplx` | 33 | +1 | 1 | no | — | product P1 |
| 8 | `cu_P2_cplx` | 32 | 0 | **2** | **yes** | — | product P2 |
| 9 | `pb_P2_cplx` | 32 | 0 | 1 | no | **ECP60MDF** | product P2 |
| 10 | `zn_P2_cplx` | 32 | 0 | 1 | no | — | product P2 |
| 11 | `lig_P0_LH2` | 21 | 0 | 1 | no | — | reactant P0 |
| 12 | `lig_P1_LH1m` | 20 | −1 | 1 | no | — | reactant P1 |
| 13 | `lig_P2_L2m` | 19 | −2 | 1 | no | — | reactant P2 |
| 14 | `cu_aquo6` | 19 | +2 | **2** | **yes** | — | reactant |
| 15 | `pb_aquo6` | 19 | +2 | 1 | no | **ECP60MDF** | reactant, **headline Pb reference state** |
| 16 | `zn_aquo6` | 19 | +2 | 1 | no | — | reactant |
| 17 | `pb_aquo8` | 25 | +2 | 1 | no | **ECP60MDF** | **alternative** — §6 validation and limitations only |

Charge and multiplicity in every row are read verbatim from the `.xyz` provenance header written in
S02 and are never inferred (attack **A02**). All four Cu(II) species carry the explicit `UKS`
keyword and multiplicity 2. All five Pb species declare the ECP explicitly.

---

## 4. WHAT WAS CAUGHT BEFORE LAUNCH

Recorded because each would have destroyed the run silently.

| Finding | Consequence had it not been caught |
|---|---|
| **OpenMPI 4.1.8 refuses to run as root** without `OMPI_ALLOW_RUN_AS_ROOT` + `..._CONFIRM`. | **Every one of the 17 jobs would have aborted in "Startup" within seconds**, logging failures that look like ORCA faults and are not. Fixed by exporting both variables inside `run_queue.sh` — a job-local environment setting, not a change to the box. |
| **A tmux session inherits a non-login shell**, which on this box has no OpenMPI on `PATH` and an empty `LD_LIBRARY_PATH`. | Same outcome. Fixed by exporting both explicitly in `run_queue.sh`. |
| **`%maxcore 3000` overcommits memory 1.65×.** | OOM kill at an arbitrary point, potentially hours into a job. Ruled down to 1500 before launch. |

All three were found by direct probe on the box before uploading, not by reasoning about it.

---

## 5. FREE RESULT — OPEN ITEM C-01 IS ANSWERED

`REACTIONS.md` §5.1 carried an open implementation check: *does ORCA's printed final energy already
include the SMD `G_CDS` term, or must `thermo.py` add it?* Adding it twice would corrupt every free
energy in the report. The completed `water` job answers it from real output:

```
Total energy after final integration   -76.392878377      SCF incl. SMD electrostatics
SMD CDS (Gcds)                         +0.002304539
Total Energy after SMD CDS correction  -76.390573837      = sum of the two above
Dispersion correction                  -0.000276877
FINAL SINGLE POINT ENERGY              -76.390850714      = sum of the two above
```

**`FINAL SINGLE POINT ENERGY` = E(SCF, SMD electrostatic) + G_CDS + E_D3BJ.** The CDS term is
already included. **`thermo.py` must NOT add it again.** Both arithmetic identities close exactly.

To be re-confirmed against a metal complex before `thermo.py` is finalised — the identity should hold
identically, but it is cheap to check and this is the term that would silently corrupt everything.

---

## 6. PROJECTED COMPLETION — REVISED ON MEASURED TIMINGS

**Superseding the S04 estimates, which were guesses.** These use the real S04 wall-clock and the
measured cost split of the one complex that finished.

### Measured

| Job | Atoms | Cores | Wall-clock | Cycles | Outcome |
|---|---|---|---|---|---|
| `water` | 3 | 8 | **15 s** | 4 | complete |
| `cu_P0_cplx` | 34 | 8 | **4h37m** | 88 | complete |
| `pb_P0_cplx` | 34 | 8 | **3h06m** | 102 | **no frequencies — cap hit** |

**Cost split of `cu_P0_cplx` (4h37m), from ORCA's own timing table:**

| Module | Time | Share |
|---|---|---|
| SCF iterations | 2h32m | 54.8% |
| SCF gradient | 54m | 19.6% |
| SCF response (CPSCF, the analytic Hessian) | 32m | 11.6% |
| Property integrals | 21m | 7.7% |
| Property calculations | 9m | 3.4% |
| Startup | 8m | 2.9% |

Which resolves to two numbers that drive everything below:

- **~140 s per geometry-optimisation cycle** for a 34-atom complex at 8 cores
  (`pb_P0_cplx`, closed-shell, was cheaper at ~110 s/cycle)
- **~1h03m for the analytic Hessian and thermochemistry**, largely independent of cycle count

### Projection

Group 1 started 06:10 UTC. Complexes begin as cores free up, from roughly 08:00 UTC.

| Scenario | Per complex | 8 complexes at 2 concurrent | **Queue finishes** |
|---|---|---|---|
| Optimistic — ~70 cycles | ~3.7 h | ~13.5 h | **15 Aug, ~03:00 IST** |
| **Central — ~90 cycles** | **~4.5 h** | **~17 h** | **15 Aug, ~06:30 IST** |
| Pessimistic — ~140 cycles | ~6.5 h | ~25 h | **15 Aug, ~14:30 IST** |

**The central and optimistic cases land comfortably before midday Saturday 15 August. Only the
pessimistic case crosses it, and then by about two hours.**

`pb_P0_cplx` is treated as cheaper than a fresh complex (~2.5 h) because it restarts from a
near-converged geometry.

### Longest pole, and the real risk

The longest pole is no longer a single job — it is **the possibility of another `MaxIter`-style
non-convergence**. At ~140 s/cycle a complex that runs to the new 300-cycle cap burns **11.7 hours
and produces no free energy**, which is worse than the failure it replaced. The mitigations are:

1. `scripts/dft_status.sh` flags any job past 150 cycles.
2. The cap is 300, so a pathological job is bounded rather than endless.
3. If it recurs, the convergence criteria need a ruling — see the risk note in §0.

### If it slips past midday Saturday

1. **Drop `pb_aquo8`** — already last, not a headline quantity, costs nothing scientifically.
2. **Do not drop a protonation state without discussing it.** The P0 row has become more
   interesting, not less, since the denticity result in §9 below.

---

## 7. DISK

| | |
|---|---|
| Free on `/` (contains `/opt`) at launch | **431 GB** |
| Observed per-job scratch, 34-atom complex, during optimisation | ~400–500 MB |
| Estimated peak per large job including the analytic Hessian | 5–20 GB |
| Peak with 2 concurrent large jobs | 10–40 GB |
| **Headroom** | **roughly 10–40×** |

ORCA writes scratch **alongside the input file**, so each directory under `/opt/dft-jobs` grows
during its run. That is accounted for above. Disk is not a constraint on this box — the margin is
large enough that it needs no further monitoring, though `scripts/dft_status.sh` reports it anyway.

---

## 8. AFTER THE QUEUE FINISHES

1. `bash scripts/dft_status.sh` — confirm 17 DONE, 0 FAILED, and **no imaginary modes**. Any
   structure with an imaginary mode is not a minimum; per protocol §3.4 it is re-optimised along that
   mode and re-checked, and **its energy enters no sum until it is clean**.
2. `bash scripts/dft_harvest.sh` — pull back `.out`, `.xyz`, `.hess`, `.gbw` and property files.
3. Run the **denticity checkpoint** of protocol §3.7 on every optimised complex — both M–O(galloyl)
   distances individually, never averaged. This decides whether §3.8 Case A, B or C applies.
4. Confirm ⟨S²⟩ for all four Cu species and record the deviation from 0.750.
5. Re-confirm the §5 `G_CDS` identity on a metal complex before `thermo.py` sums anything.
6. **DESTROY THE VULTR INSTANCE.** See the banner at the top of this file.

---

## 9. QC CHECKPOINT RESULTS — AND THE A31 DENTICITY FINDING

Produced by [`analysis/qc_checkpoint.py`](analysis/qc_checkpoint.py), which implements protocol
§3.2, §3.4 and §3.7 and reuses the first-shell cutoffs of
[`structures/geom_utils.py`](structures/geom_utils.py) so pre-screen and production verdicts are
directly comparable.

### `water` — COMPLETE
9 modes, **0 imaginary**, lowest real 1596.16 cm⁻¹. `FINAL SINGLE POINT ENERGY` −76.39085071 Eh.

### `cu_P0_cplx` — COMPLETE
102 modes (3 × 34), **0 imaginary**, lowest real **28.65 cm⁻¹**. Optimisation converged in 88
cycles. `FINAL SINGLE POINT ENERGY` −2630.96396966 Eh.

> The lowest real mode at 28.65 cm⁻¹ is far below the 100 cm⁻¹ quasi-RRHO threshold of §3.4, which
> is direct evidence that the quasi-RRHO treatment is doing real work rather than being a formality.
> A raw RRHO entropy would badly mistreat that mode.

**§3.2 ⟨S²⟩ = 0.7518** against the ideal 0.750 — a deviation of **+0.0018, or 0.24%**. Spin
contamination is negligible; the d⁹ doublet is clean.

### A31 — Cu(II) P0 IS MONODENTATE AT THE PRODUCTION LEVEL OF THEORY

**Attack A31 / ruling D-02, OPEN since S03, is now resolved for copper.** Distances reported
individually and never averaged, per §3.7:

| Species | Cu–O(galloyl) #1 | Cu–O(galloyl) #2 | Cutoff | Verdict |
|---|---|---|---|---|
| `cu_P0_cplx` | **2.048 Å** — bound | **3.692 Å** — not bound | 2.80 Å | **MONODENTATE** |

First shell: **5 oxygens — 1 ligand + 4 water.** The third phenolic oxygen sits at 5.875 Å.

**The GFN2-xTB pre-screen was right, and DFT makes it more pronounced**, not less: the pre-screen
gave 2.30 / 3.24 Å, production gives 2.048 / 3.692 Å. This was not a semi-empirical artefact.

**This is protocol §3.8 Case B**, which was written out in advance on 13 August precisely so it
would not have to be decided under deadline pressure. Its consequences now bind:

- The P0 Cu reaction displaces **one** water, not two: `x = 1, Δn = 0` against `x = 2, Δn = +1`
  for a bidentate product. The standard-state correction differs and the water terms **no longer
  cancel** in ΔΔG.
- **ΔΔG(Pb − Cu) at P0 must not be quoted as a like-for-like selectivity figure.**
- The P0 row of Table 4.9 carries the denticity mismatch **in the table itself**, not in a footnote.
- The Cu P0 complex is **not** re-optimised under a restraint to force bidentate coordination.
- The argument does not depend on P0: the claim is the one that survives all three protonation
  states, and P1/P2 both retained bidentate coordination at pre-screen for all three metals.

### `pb_P0_cplx` — PROVISIONAL, NOT A RESULT

| Species | Pb–O(galloyl) #1 | Pb–O(galloyl) #2 | Cutoff | Provisional verdict |
|---|---|---|---|---|
| `pb_P0_cplx` | 2.845 Å — bound | 3.842 Å — not bound | 3.20 Å | *monodentate* |

**This geometry is NOT converged** — it is the last point of an optimisation that hit its cycle cap
and never ran frequencies. **It is not a finding and must not be reported as one.** It is recorded
only because it raises a live possibility that changes which contingency applies:

> If lead(II) P0 is *also* monodentate once converged, this is **not** §3.8 Case B (Cu alone
> differing) but **Case C** — and if zinc follows, comparability at P0 is *restored* at `x = 1`
> on a matched basis, which is a materially better position than Case B.

**Resolving this needs two things, both queued now:** the `pb_P0_cplx` re-run, and `zn_P0_cplx`.
Until both are converged with real frequencies, the P0 denticity pattern is **open**, and the
report says Cu is monodentate and says nothing about the pattern.

### Still outstanding

| Item | State |
|---|---|
| ⟨S²⟩ for `cu_aquo6`, `cu_P1_cplx`, `cu_P2_cplx` | pending — running or queued |
| Denticity for the remaining 8 complexes | pending — §3.7 requires all nine |
| `G_CDS` identity re-confirmed on a metal complex | pending |

---

## 10. WATCHDOG — added 2026-08-14, 20:00 IST (S06)

Cron-based, deliberately lightweight. **No systemd migration**, and nothing that was running was
touched: `cu_P1_cplx` and `pb_P1_cplx` were hours into their calculations when this was installed.

| | |
|---|---|
| `dft/heartbeat.sh` → `/opt/dft-jobs/heartbeat.sh` | every **10 min**, appends one line to `heartbeat.log` |
| `dft/watchdog.sh` → `/opt/dft-jobs/watchdog.sh` | every **15 min**, restarts the queue only if it has genuinely died |
| `dft/lib_jobstate.sh` → `/opt/dft-jobs/lib_jobstate.sh` | shared job-state predicates, so the completion test cannot drift again |

Heartbeat line format:

```
2026-08-14T14:31:09Z | complete 10/17 | incomplete  7 | orca 2 | disk 430G free | ram 17G free | queue ALIVE
```

### What the watchdog will never do

It contains **no `kill`, no `pkill`, no `tmux kill-session`**. It never touches a job directory, an
input file, or `run_queue.sh`. It never starts anything while an ORCA process is alive. Its only
side effects are appended log lines and, in one narrow case, a `tmux new-session`.

**`run_queue.sh` is never edited while it may be running.** Bash reads a script incrementally, so
editing a running script can corrupt its execution mid-queue. That is why the shared predicates live
in a separate file that `run_queue.sh` does not source.

### When it restarts

All five must hold:

1. at least one job is incomplete (three-part test: normal termination **and** frequency section
   **and** `.hess`),
2. zero ORCA driver processes,
3. `run_queue.sh` is not running — tested via the flock it holds, not via `pgrep`,
4. 1–3 have held **continuously for more than 15 minutes**, confirmed across two cron ticks rather
   than on a single observation, and
5. the watchdog has not given up.

A restart is safe because the three-part completion test makes `run_queue.sh` **resume rather than
redo**, and its flock prevents two concurrent queues even if the watchdog were wrong.

### When it gives up

It writes a loud `WATCHDOG FAILURE` banner to `heartbeat.log` and `queue.log`, sets a `disabled`
flag and stops, if any of:

- the queue died again **within 30 minutes** of the previous restart,
- a restart produced **no additional completed job**, or
- **5 restarts** have been made.

`scripts/dft_status.sh` surfaces that banner at the top of its watchdog section. Re-arm after fixing
the cause with `rm -rf /opt/dft-jobs/.watchdog`.

### A bug caught before installation

The first version counted ORCA processes with `pgrep -f '/opt/orca/orca .*\.inp'`. That **also
matches any other process whose command line contains the pattern** — including the ssh command used
to check it, which made the heartbeat report `orca 3` when two jobs were running.

**That false positive is in the dangerous direction**: it makes a dead queue look busy and would
suppress exactly the restart the watchdog exists to make. Both process checks were changed to be
immune to command-line matching — `pgrep -c -x orca` matches the process *name*, and the queue-driver
test uses the flock rather than a pattern.

---

## 11. THE P0 DENTICITY PATTERN IS COMPLETE — AND IT IS NOT CASE B

**2026-08-14, 20:15 IST.** All three P0 complexes are now converged with all frequencies real. This
**supersedes the provisional reading in §9**, which was based on an unconverged `pb_P0_cplx`
geometry and on the §3.8 Case B assumption that copper alone would differ.

| Species | M–O(galloyl) #1 | M–O(galloyl) #2 | Cutoff | Verdict | Cycles | Imag. |
|---|---|---|---|---|---|---|
| `pb_P0_cplx` | **2.936 Å** bound | **4.166 Å** not bound | 3.20 Å | **MONODENTATE** | 119 | 0 |
| `cu_P0_cplx` | **2.048 Å** bound | **3.692 Å** not bound | 2.80 Å | **MONODENTATE** | 88 | 0 |
| `zn_P0_cplx` | **2.180 Å** bound | **2.215 Å** bound | 2.80 Å | **bidentate** | 60 | 0 |

**Zinc is the outlier, not copper.** This is the mixed-pattern branch of protocol §3.8 Case C —
"if the pattern is mixed in some other way, Case B applies to whichever metals differ" — and the
metal that differs is **Zn**.

### What this changes, and it is favourable

§3.8 Case B was written on the assumption that Cu alone would go monodentate, and concluded that
**ΔΔG(Pb − Cu) at P0 must not be quoted as a like-for-like figure**. The measurement inverts that:

| Comparison at P0 | Reaction classes | Status |
|---|---|---|
| **ΔΔG(Pb − Cu)** | both x = 1, Δn = 0 | **MATCHED — like-for-like, quotable** |
| ΔΔG(Pb − Zn) | x = 1 vs x = 2, Δn = 0 vs +1 | **NOT matched — carries the caveat** |
| ΔΔG(Cu − Zn) | x = 1 vs x = 2, Δn = 0 vs +1 | **NOT matched — carries the caveat** |

**The comparison that carries the Irving–Williams argument is the Pb/Cu one, and at P0 it is
matched.** That is a materially better position than Case B anticipated.

### Consequences that now bind

1. **The P0 reaction for Pb and Cu is not the one written in `REACTIONS.md` §2.** It is

   ```
   [M(H2O)6]2+  +  LH2  ->  [M(LH2)(H2O)5]2+  +  1 H2O        x = 1,  dn = 0
   ```

   **`REACTIONS.md` §3's claim of "x = 2, identically, for all three metals and all three
   protonation states" is falsified at P0 for Pb and Cu** and must be qualified. §3.2 of that
   document anticipated exactly this check and required it before any P0 ΔΔG is reported.
2. The standard-state correction differs between the Pb/Cu pair and Zn at P0: ΔG_ss = 0 for the
   monodentate pair against −12.0 kJ/mol for Zn. **The water terms do not cancel in ΔΔG(Pb − Zn).**
3. **Table 4.7 carries the measured denticity and first-shell donor count for every species**, as
   §3.7 requires. Table 4.9's P0 row marks the Zn mismatch **in the table itself**, not a footnote.
4. **No complex is re-optimised under a restraint** to force bidentate coordination (§3.8 point 5).
   Computing the monodentate form for all three metals as a matched second set remains **future
   work**, not a this-week action.

### Interpretation — offered with its basis, not asserted

The pattern is what the geometry supports and it is chemically coherent: **both metals that shed a
donor have an electronic reason to**. Cu(II) d⁹ is Jahn–Teller distorted and disfavours a sixth
short bond; Pb(II) has a stereochemically active 6s² lone pair that occupies one hemisphere, which
is the same feature the report's central mechanism rests on. Zn(II) d¹⁰ has no ligand-field
preference and no lone pair, and retains the chelate. **A neutral catechol is a weak donor**, so at
P0 the electronic cost of the second bond is not repaid for Pb or Cu.

This is stated as an interpretation with that basis. It is **not** presented as established, and it
must be tested against the P1 and P2 rows before it enters the report as a mechanism.

### Still open

The P1 and P2 denticity pattern. `cu_P1_cplx` and `pb_P1_cplx` are running now. **Nothing about the
headline claim rests on P0** — the reported claim is the one that survives all three protonation
states (§1.3).
