<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# ORCA PRODUCTION QUEUE — LAUNCH RECORD

> ## ⚠ THE INSTANCE MUST BE DESTROYED AFTER HARVEST
>
> **Vultr instance `65.20.67.245` bills at `$0.493/hr`.**
> **STOPPING THE INSTANCE DOES NOT HALT BILLING. ONLY DESTROYING IT DOES.**
>
> At $0.493/hr this is **$11.83/day**, accruing whether or not any job is running.
> The moment `scripts/dft_harvest.sh` has pulled back all seventeen jobs and the
> outputs have been verified, **destroy the instance**.

---

## 1. LAUNCH

| | |
|---|---|
| **Launched** | **2026-08-13, 21:12 IST** (15:42 UTC) |
| Session | S04 |
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

## 6. PROJECTED COMPLETION — AN ESTIMATE, TO BE REVISED

**Every figure in this section is an order-of-magnitude estimate and must be revised the moment the
first large complex finishes.** The only measured production datapoints so far are `water`
(3 atoms, 15 s) and the observed rate of ~2 min per geometry optimisation cycle for the 34-atom
complexes.

| Job class | Atoms | ≈ basis functions | Estimated wall-clock, 8 cores |
|---|---|---|---|
| `water` | 3 | 43 | **15 s — measured, complete** |
| aquo6 ions | 19 | ~330 | 1–2 h |
| free ligands | 19–21 | ~350 | 1–2 h |
| `pb_aquo8` | 25 | ~430 | 1.5–3 h |
| **complexes** | **32–34** | **~665** | **3–8 h each** |

| Scenario | Serial work | Wall-clock at 2 concurrent | Finishes |
|---|---|---|---|
| Optimistic (3 h/complex) | ~38 h | ~19 h | **Fri 14 Aug, ~16:00 IST** |
| **Central (5 h/complex)** | **~56 h** | **~28 h** | **Sat 15 Aug, ~01:00 IST** |
| Pessimistic (9 h/complex) | ~95 h | ~48 h | **Sat 15 Aug, ~21:00 IST** |

**The central estimate lands early Saturday 15 August, comfortably before midday. The pessimistic
branch does not — it runs into Saturday night.**

### Longest pole

**`cu_P0_cplx`.** It is the largest species (34 atoms), it is open-shell UKS — roughly double the SCF
work of a closed shell, and d⁹ SCF convergence is frequently slow — and it is the one species whose
coordination mode may change during the optimisation (attack **A31**, ruling **D-02**: at GFN2-xTB
the neutral ligand opened to monodentate on Cu). A ligand arm swinging out costs many extra
optimisation cycles. It is running first, which is the correct scheduling.

### If it overruns — what to do, in order

1. **Re-tune concurrency, before cutting any science.** For the twelve small jobs (ligands, aquo
   ions) **4 concurrent jobs × 4 cores each** will almost certainly out-throughput 2 × 8, because
   ORCA's parallel efficiency at 8 cores is well below linear. Memory is unchanged (4 × 4 × 1500 =
   24 GB). Edit `MAXPAR` and `%pal` and restart the queue for the remaining jobs only. **This costs
   nothing scientifically and should be tried first.**
2. **Drop `pb_aquo8`.** It is already last and is not a headline quantity. Cost: the §6 Pb–O
   validation covers only the six-coordinate ion, and the CN = 8 limitation in §2.2 rests on the
   GFN2-xTB screen alone rather than on a DFT comparison. Cheap.
3. **Drop the P0 protonation state** (`{pb,cu,zn}_P0_cplx`, 3 × 34 atoms — the most expensive tier,
   worth roughly half the remaining wall-clock). **This is a real scientific loss and is the last
   resort.** It weakens §1.3's three-state sensitivity design, which is the move that converts the
   protonation assumption from a liability into a result. It is nevertheless the least-bad cut,
   because P0 is already the compromised state: at pre-screen Cu(II) P0 went monodentate while Pb and
   Zn stayed bidentate, so under §3.8 Case B the P0 cross-metal row may not be a like-for-like
   comparison in any case, whereas P1 and P2 both retained bidentate coordination for all three
   metals. If this cut is made, the report must say plainly that P0 was not computed and why —
   not quietly present a two-state design as though it had always been the plan.

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
