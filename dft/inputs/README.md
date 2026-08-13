<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# dft/inputs/ — Production ORCA input files

## What this is

Seventeen ORCA 6.1.1 input files, one per species, each in its own directory. These are the files
that were uploaded to the compute box and launched on **13 August 2026**. They are the record of
what was actually run, at what level of theory, with what charge and multiplicity.

**Every file is generated. None is hand-written, and none may be hand-edited.**

```bash
python dft/make_orca_inputs.py            # regenerate all 17 + JOB_ORDER.txt
python dft/make_orca_inputs.py --check    # audit only, writes nothing
```

`make_orca_inputs.py` is the sole writer of this directory. It deletes and rewrites each job
directory on every run, so a hand edit is silently destroyed on the next regeneration — which is the
intended behaviour. If a setting is wrong, fix the generator.

---

## Where every setting comes from

Nothing in these files was chosen at generation time. Every level-of-theory setting is transcribed
from [`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md), and the section reference is carried into the
comment header of each `.inp` so a reader never has to take it on trust.

| Setting | Value | Protocol section |
|---|---|---|
| Functional | PBE0 (25% exact exchange) | §3 "Functional" |
| Dispersion | D3(BJ) | §3 "Dispersion" |
| Basis, all elements | def2-TZVP | §3.1 |
| **Pb core** | **def2-ECP = Stuttgart–Cologne ECP60MDF, 60 core electrons, 22 in valence** | §3.1 |
| Cu, Zn, C, H, O | all-electron | §3.1 |
| Auxiliary basis | def2/J | §3.1, §3.4 |
| Acceleration | RIJCOSX | §3.4 |
| Solvation | SMD, water, applied **during** the optimisation | §3.3 |
| Geometry convergence | TightOPT | §3.4 |
| SCF convergence | TightSCF | §3.4 |
| Integration grid | DefGrid3 | §3.4 |
| Frequencies | analytic, same level, same solvent | §3.4 |
| Opt + freq | one combined job per species (17 total) | §8 |

Which becomes, in every file:

```
! PBE0 D3BJ def2-TZVP def2/J RIJCOSX TightSCF DefGrid3 {RKS|UKS}
! Opt Freq TightOPT
```

### The two settings that are pointers rather than transcriptions

Both are recorded here because a reader will otherwise look for them in the input and not find them.

1. **Opt+freq as one job** is stated in the protocol as a job *count* (§8: "Total opt+freq jobs =
   17"), not as a keyword directive. One combined `! Opt Freq` job per species is the only reading
   consistent with 17 jobs and 17 species. This is a derivation from §8, not a choice.

2. **The quasi-RRHO treatment is NOT in these inputs, and that is deliberate.** Protocol §3.4 fixes
   298.15 K, 1 atm, RRHO with Grimme's quasi-RRHO for modes below 100 cm⁻¹.
   [`../REACTIONS.md`](../REACTIONS.md) §5.1 assigns the computation of `G_thermal,qRRHO` to
   `analysis/thermo.py`, built from the frequency list the job prints. Putting a quasi-RRHO keyword
   in the input as well would risk ORCA's own default entropy treatment being silently
   double-counted — the same hazard already tracked as open item **C-01** for the SMD `G_CDS` term.
   So ORCA prints frequencies, and `thermo.py` does the thermochemistry.

---

## Charge and multiplicity — attack A02

**Charge and multiplicity are read verbatim from the `key=value` provenance header of the
corresponding [`../structures/`](../structures/) `.xyz` file and are never inferred, defaulted or
re-derived.** A structure whose header is missing or unparseable is a hard error that aborts the
entire generation run; no input file is written for it and no default is supplied.

The generator additionally refuses to proceed if a header contradicts itself — if `mult ≠ uhf + 1`,
or if `uks` disagrees with `mult > 1`. These are consistency checks on the header, not
re-derivations of its content.

**All four Cu(II) species carry multiplicity 2 and the explicit `UKS` keyword.** If Cu(II) were
treated closed-shell the entire computational arm would be invalid, so the input states it rather
than relying on ORCA inferring it from the multiplicity.

| Cu species | charge | mult | keyword |
|---|---|---|---|
| `cu_aquo6` | +2 | 2 | `UKS` |
| `cu_P0_cplx` | +2 | 2 | `UKS` |
| `cu_P1_cplx` | +1 | 2 | `UKS` |
| `cu_P2_cplx` | 0 | 2 | `UKS` |

⟨S²⟩ is printed by ORCA for each and is reported with its deviation from the ideal 0.750, per
protocol §3.2.

## The Pb ECP — attack A03

`! def2-TZVP` already assigns the def2-ECP to Pb automatically. The five Pb-containing inputs
nevertheless declare it explicitly:

```
%basis
  NewGTO Pb "def2-TZVP" end
  NewECP Pb "def2-ECP"  end
end
```

so that the relativistic treatment is visible **in the input file itself** and not only inferable
from the output. Verified on the compute box before launch — ORCA reports:

```
Group 1, Type Pb ECP Def2-ECP (replacing 60 core electrons, lmax=3)
```

which is ECP60MDF: 60 core electrons replaced, 22 in the valence space, scalar-relativistic effects
entering through the ECP parameterisation. ORCA's own citation block for this ECP gives
**B. Metz, H. Stoll, M. Dolg, *J. Chem. Phys.* 2000, *113*, 2563–2569**, which is the reference
protocol §3.1 names. It still has to clear `verify_dois.py` and be read before it enters
`refs/library.bib`.

---

## Geometry source

Each input carries the coordinates of the **lowest-energy verified conformer** retained by the S02
conformer screen ([`../structures/CONFORMER_SCREEN.md`](../structures/CONFORMER_SCREEN.md)),
pre-optimised at GFN2-xTB/ALPB(water). Coordinates are inlined into the `.inp` rather than
referenced by an external `xyzfile`, so each job directory is self-contained and the geometry that
was actually submitted is preserved in the same file as the settings it was submitted with.

**No pre-screen energy is a report quantity.** The GFN2-xTB stage exists only so that no ORCA job
starts from a sketch.

---

## Job list and queue order

`JOB_ORDER.txt` is the queue order consumed by `run_queue.sh` on the compute box. It is
**longest-processing-time-first**, which minimises the makespan tail on a depth-limited queue, with
two deliberate departures:

- **`water` runs first.** It is trivially cheap and exercises every element of the production
  keyword line end to end, so a fault surfaces in seconds rather than after a multi-hour complex has
  died.
- **`pb_aquo8` runs last.** It is the limitations-discussion alternative and half of the §6 Pb–O
  validation, not a headline quantity ([`../REACTIONS.md`](../REACTIONS.md) §3.1). Placed last on a
  depth-2 queue it can never delay a headline job.

| Order | Job | Atoms | Charge | Mult | UKS | Role |
|---|---|---|---|---|---|---|
| 1 | `water` | 3 | 0 | 1 | no | released product, ×2 per equation |
| 2 | `cu_P0_cplx` | 34 | +2 | 2 | **yes** | product, P0 |
| 3 | `pb_P0_cplx` | 34 | +2 | 1 | no | product, P0 |
| 4 | `zn_P0_cplx` | 34 | +2 | 1 | no | product, P0 |
| 5 | `cu_P1_cplx` | 33 | +1 | 2 | **yes** | product, P1 |
| 6 | `pb_P1_cplx` | 33 | +1 | 1 | no | product, P1 |
| 7 | `zn_P1_cplx` | 33 | +1 | 1 | no | product, P1 |
| 8 | `cu_P2_cplx` | 32 | 0 | 2 | **yes** | product, P2 |
| 9 | `pb_P2_cplx` | 32 | 0 | 1 | no | product, P2 |
| 10 | `zn_P2_cplx` | 32 | 0 | 1 | no | product, P2 |
| 11 | `lig_P0_LH2` | 21 | 0 | 1 | no | reactant, P0 |
| 12 | `lig_P1_LH1m` | 20 | −1 | 1 | no | reactant, P1 |
| 13 | `lig_P2_L2m` | 19 | −2 | 1 | no | reactant, P2 |
| 14 | `cu_aquo6` | 19 | +2 | 2 | **yes** | reactant |
| 15 | `pb_aquo6` | 19 | +2 | 1 | no | reactant, **headline Pb reference state** |
| 16 | `zn_aquo6` | 19 | +2 | 1 | no | reactant |
| 17 | `pb_aquo8` | 25 | +2 | 1 | no | **alternative** — §6 validation and limitations only |

Sixteen headline jobs plus one alternative, matching the [`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md)
§8 inventory and the seventeen structures in [`../structures/`](../structures/) exactly.

---

## Resource settings

These are hardware settings. They do not come from the protocol and they do not affect any computed
quantity.

| Setting | Value | Reason |
|---|---|---|
| `%pal nprocs 8 end` | 8 | 16 vCPU box, 2 concurrent jobs |
| `%maxcore 1500` | 1500 MB per process | 1500 × 8 × 2 = 24 GB nominal against 29 GB available. ORCA's own sizing rule is ~75% of RAM ÷ total cores = 29000 × 0.75 / 16 ≈ 1400. |

The S04 brief originally specified `%maxcore 3000`, which is 3000 × 8 × 2 = **48 GB against 29 GB
available** — a 1.65× overcommit that would leave a multi-hour job at the mercy of the OOM killer.
Raised before launch and **ruled down to 1500 by Palaash on 2026-08-13**.

## What must never happen here

- An input file hand-edited rather than regenerated.
- A charge or multiplicity that does not match the `.xyz` provenance header it came from.
- A Pb species without the ECP declared.
- A Cu species without `UKS` and multiplicity 2.
- A level-of-theory setting that cannot be traced to a section of `DFT_PROTOCOL.md`.
