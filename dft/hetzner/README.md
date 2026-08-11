<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# dft/hetzner/ — provisioning, job submission, sizing

## What belongs here
`provision.sh` (fresh Debian/Ubuntu x86-64 → working ORCA) · `upload_orca.sh` · `submit.sh` ·
`sync_results.sh` · instance sizing notes and **measured** wall-clock per job class.

## What must never go here
API tokens, SSH private keys, or any secret — these are gitignored, and leaking one is worse than
losing the compute. The ORCA tarball itself: it is licence-restricted and must not be redistributed.

---

# THE VERDICT — READ THIS FIRST

**It is late on 11 August. Results are wanted by 14 August. That is roughly 2.5 working days.**

**ORCA is not downloaded, and it cannot be downloaded automatically.** Registration at the ORCA
forum is manually approved and takes anywhere from a few hours to a couple of days. **That approval,
not the compute, is the critical path.** No amount of instance sizing fixes it.

So the honest position is:

> **The DFT arm does not reliably complete by 14 August on the ORCA path. Plan for the PySCF path
> and treat ORCA as an upgrade if the approval clears in time.**

**PySCF is already installed and working on this machine.** It needs no registration, no download and
no approval. It runs PBE0-D3(BJ)/def2-TZVP with the def2-ECP on Pb, in implicit solvent, with
analytic Hessians. It is slower than ORCA and its SMD implementation differs in detail, but **it is
available right now**, and a completed calculation at a slightly less convenient level of theory
beats an uncompleted one at the preferred level.

**Act on this today, in this order:**

1. **Register at https://orcaforum.kofo.mpg.de/ now.** Five minutes. The clock starts on approval,
   so start it tonight. Same logic as the principal's signature.
2. **Start the PySCF path in parallel tonight**, on the cheap jobs — water, the three ligand
   protonation states, the aquo ions. These are needed for *every* reaction and are independent of
   which program runs the complexes.
3. **Run the CREST conformer pre-pass now.** `xtb` and `crest` are installed and working. The
   galloyl ligand's conformers are cheap at the semi-empirical level and the result feeds whichever
   DFT path runs. This is not blocked on anything.
4. **Decide on 13 August.** If ORCA has not arrived by the morning of 13 August, commit to PySCF and
   do not look back. A protocol switch on 15 August is how the computational arm gets abandoned.

---

## What fits in the window

| Tier | Scope | Verdict |
|---|---|---|
| **Tier 1 — MINIMAL** | Methyl gallate, **one** protonation state, 3 metals + 3 aquo ions + ligand + water. ~8 opt+freq jobs. | **Achievable** by 14 August if compute starts 12 August. **This is the realistic target.** |
| **Tier 2 — FULL SENSITIVITY** | All **three** protonation states (P0/P1/P2), 3 metals. 17 opt+freq jobs, per `../DFT_PROTOCOL.md` §8. | **Achievable only if compute starts on 12 August across ≥4 instances in parallel.** Marginal. The protonation sensitivity set is the strongest single defensive feature of the model, so protect it by cutting elsewhere first. |
| **Tier 3 — BIS-GALLOYL POCKET** | Two galloyl arms converging on one metal. | **NOT achievable. Already cut** in `../DFT_PROTOCOL.md` §9. Do not attempt. State it in §5.3 as a limitation and §5.4 as future work. |

**If you must cut inside Tier 2, cut in this order:**
1. The ωB97X-D4 functional cross-check *(already flagged as first out)*.
2. The P0 neutral-ligand state — keep P1 and P2, which bracket the chemically interesting range.
3. `[Pb(H₂O)₈]²⁺` — assume six-coordinate Pb and **say that you assumed it**.
4. The counterpoise correction on all but one representative case.

**Never cut:** the frequency calculations (without them there is no free energy, no minimum
confirmation, and no thermal correction — the whole arm becomes uninterpretable), or ⟨S²⟩ reporting
for Cu.

---

## Instance sizing

Hetzner **CCX** line — dedicated AMD EPYC vCPU. Shared-vCPU (CX/CPX) instances are false economy for
quantum chemistry: the steal time on a 10-hour job is unpredictable and the job may simply not
finish. **Use dedicated vCPU.**

| Instance | vCPU | RAM | Suits |
|---|---|---|---|
| CCX23 | 4 | 16 GB | water, ligand states, single-metal aquo ions |
| **CCX33** | **8** | **32 GB** | **the workhorse — one complex opt+freq per instance** |
| CCX43 | 16 | 64 GB | the largest complexes; roughly halves the frequency step |

**Recommendation: 4 × CCX33, one job per instance, run in parallel.** ORCA's parallel scaling on
hybrid-DFT frequencies is sublinear past about 8–16 cores for a system this size, so **four 8-core
instances beat one 32-core instance** for a queue of independent jobs. Memory: request roughly
3–4 GB per core in `%maxcore` and leave headroom; an ORCA job that swaps does not finish.

**Cost.** At Hetzner's CCX33 rate, four instances for three days is of the order of **€30–50**.
Verify current pricing — it changes. The cost is not the constraint here; time is.

### Wall-clock estimates — **estimates, to be replaced by measurement**

PBE0-D3(BJ)/def2-TZVP, SMD water, RIJCOSX, analytic frequencies, on 8 dedicated cores:

| Job class | Atoms | ~Basis fns | Opt | **Freq** | Total |
|---|---|---|---|---|---|
| H₂O | 3 | ~45 | minutes | minutes | < 15 min |
| Ligand LH₂ / LH⁻ / L²⁻ | 21 | ~500 | 0.5–2 h | 1–3 h | 2–5 h |
| [M(H₂O)₆]²⁺ | 19 | ~450 | 0.5–2 h | 1–3 h | 2–5 h |
| **[M(L)(H₂O)₄]^q complex** | ~33 | ~800 | **2–6 h** | **6–20 h** | **8–26 h** |

**The frequency step dominates and it is where the schedule is won or lost.** Treat these numbers as
order-of-magnitude only until the first complex has actually run — **then replace this table with
measured times.** Anyone who tells you a hybrid-DFT Hessian on 33 atoms will take a predictable
number of hours has not run one.

**Anti-optimism note.** The Cu(II) complexes are unrestricted and open-shell. Expect them to take
**noticeably longer than the closed-shell Zn and Pb analogues**, and expect SCF convergence trouble
on at least one of them. Budget for it; do not be surprised by it.

---

## Workflow

```bash
# 1. provision (on the instance, as root)
bash provision.sh

# 2. install ORCA (from your laptop) — the tarball you downloaded yourself
bash upload_orca.sh <ip> ~/Downloads/orca_6_x_x_linux_x86-64_shared_openmpi41.tar.xz

# 3. submit one job per instance
bash submit.sh pb_p1_complex.inp 8

# 4. pull results back; the script checks termination, imaginary modes and <S^2>
bash sync_results.sh <ip>
```

`sync_results.sh` transfers only the text outputs and structures that are evidence, and prints a
sanity table. **A job that did not terminate normally, or a structure reported as a minimum that
still carries an imaginary mode, is not usable** — and every Cu species must show ⟨S²⟩, because its
absence means the job ran closed-shell and attack **A02** lands.

---

## Compute declaration

Assertion **C-023** and attack **A18** require the report to declare where the DFT ran and who set it
up. Record here as jobs complete: instance type, region, number of instances, total core-hours, ORCA
or PySCF version, and the fact that the provisioning scripts in this directory were used.

`\TODOPAL{instance type, count and total core-hours actually used — required for the compute
declaration in the Acknowledgement}`
