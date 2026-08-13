<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# CONFORMER SCREENING — METHOD, OUTCOME, AND WHAT WAS CARRIED FORWARD

**Status.** Source material for report §3.1 and §5.3. Written at report precision.

**No quantity in this document is a report number.** Every energy below is a semi-empirical
GFN2-xTB pre-screen value used to *order* structures. None enters `data/CANONICAL_NUMBERS.yaml`;
none is quoted in the report as a thermodynamic result. The conformer *selection* they support is
what carries forward, and that selection is re-tested at the production level of theory.

---

## 1. WHY A CONFORMER SEARCH IS NOT OPTIONAL HERE

Methyl gallate carries four rotatable torsions — a methyl ester and three phenolic hydroxyls — and
the hydroxyls form an intramolecular hydrogen-bond network whose pattern differs between rotamers.
The metal complexes add the orientation of every coordinated water about its own metal–oxygen axis.

The question is whether that matters at the scale of the effect being measured. **It does, and by a
wide margin.** The table below compares the energy of each structure as first pre-optimised from its
built starting geometry against the lowest conformer found by the search:

| Species | Lowering achieved by the search / kJ mol⁻¹ |
|---|---|
| `zn_P0_cplx` | **33.20** |
| `pb_P0_cplx` | **31.92** |
| `lig_P1_LH1m` | **16.96** |
| `cu_P1_cplx` | 9.40 |
| `cu_P2_cplx` | 8.02 |
| `cu_P0_cplx` | 5.95 |
| `pb_aquo8` | 5.34 |
| `cu_aquo6` | 2.53 |
| `pb_P2_cplx` | 1.70 |
| `pb_aquo6` | 0.54 |
| `zn_P2_cplx` | 0.46 |
| `zn_aquo6` | 0.20 |
| `lig_P0_LH2` | 0.11 |
| `pb_P1_cplx`, `zn_P1_cplx`, `lig_P2_L2m`, `water` | ≤ 0.03 |

**The decisive observation is not the size of the lowering but its unevenness.** In the P0 state the
search lowered the Zn complex by 33.20 kJ mol⁻¹ and the Pb complex by 31.92 kJ mol⁻¹, but the Cu
complex by only 5.95 kJ mol⁻¹. Had the search been skipped, roughly **26 kJ mol⁻¹ of pure
conformational artefact** would have entered the Pb-versus-Cu comparison in the P0 state — a
quantity of the same order as the selectivity difference the report exists to measure, and pointing
in a direction determined by nothing more than which starting geometry happened to be built.

A conformer search is therefore a precondition for the ΔΔG comparison meaning anything, not a
refinement of it.

---

## 2. METHOD

### 2.1 CREST was attempted first, and failed

[`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §8 specifies a CREST conformer pre-pass. **CREST 3.0.2 as
installed in the `biosorb` environment cannot run on this machine.** The failure was characterised
before it was worked around:

| Attempt | Result |
|---|---|
| GFN2-xTB, ALPB water, 8 threads | Aborted: "Change in topology detected", flagging **all** atoms |
| Same, with `--noreftopo` | Aborted in the metadynamics: `Factorisation of matrix failed lapack_sytrf`, after six automatic MD restarts with reducing time step and SHAKE disabled |
| Same, single-threaded | Identical LAPACK failure |
| GFN2-xTB, gas phase | Aborted at the initial geometry optimisation |
| GFN-FF, ALPB water | Aborted at the initial geometry optimisation |

**The initial topology warning was verified to be a false positive.** The input handed to CREST had
already been tight-optimised at GFN2-xTB/ALPB(water) — the identical level CREST then re-optimised it
at — so it should not have moved. Direct comparison of the input and CREST's own optimised geometry
gives **21 covalent bonds before and 21 after, with no difference in the bond list**; the largest
atomic displacement, 1.83 Å, is a hydroxyl proton rotation. The connectivity did not change.

The underlying failure is nonetheless fatal and is not a property of these molecules: the plain `xtb`
binary from the same environment optimised all seventeen structures without complaint, and the
failure reproduces at two different Hamiltonians, in gas phase and in solvent, on one thread and on
eight. **It is an installation-level fault in the CREST metadynamics driver.** Logs are retained in
[`crest/`](crest/) and the machine-readable outcome in `crest/ligands_results.json`.

### 2.2 What replaced it

The fallback is not a token gesture at a handful of hand-drawn rotamers. Two generators are used,
chosen to match the structure of the conformational space in each case, and both feed the same
verification and deduplication pipeline.

**Systematic torsion enumeration — the primary route for every species.** Each rotatable torsion is
identified from the connectivity, and every combination of its minima is built and optimised. For
methyl gallate the rotatable set is the three phenolic hydroxyls and the methyl ester; both are
near-planar systems with two minima each, so a two-point grid per torsion covers the space
exhaustively rather than approximately. In the complexes the two donor oxygens are locked to the
metal by chelation, leaving only the free hydroxyls and the ester.

**Seeded random water reorientation — for every metal species.** A coordinated water rotates about
its M–O axis at little cost, and the resulting hydrogen-bond network between neighbouring waters is
what distinguishes one aquo-ion conformer from another. This freedom has **no rotatable covalent
torsion at all**, so torsion enumeration is blind to it — yet the aquo ion is a reactant in every
exchange reaction, so its conformer energy shifts every reported free energy directly. With six
independent rotors a two-point grid is already 64 combinations and the minima are not at predictable
angles, so the space is **sampled** rather than enumerated, from a fixed seed for reproducibility.

**Distance-geometry embedding — supplementary, free ligands only.** ETKDGv3 embeddings, MMFF94
relaxed, added as a check that the torsion grid has not missed a basin. Pruning is disabled
deliberately: RDKit prunes on heavy-atom RMSD, and hydroxyl rotations move no heavy atom, so the
default pruning collapses the entire set to a single conformer — it returned exactly one conformer
from forty embeddings before this was corrected. Redundancy is removed after optimisation instead,
on energy and geometry together.

All starting geometries were optimised at **GFN2-xTB with the ALPB water model, `--opt tight`**,
matching the rest of the preparation stage.

### 2.3 Verification and deduplication

Every optimised structure was checked against the reference for that species before being admitted:

- **Covalent connectivity of the non-metal framework must match exactly.** This catches proton
  migration and bond formation. Metals are excluded from the connectivity fingerprint on purpose, so
  that a dative M–O contact crossing an arbitrary radius sum cannot register as a bond change — that
  being the same false positive that made CREST's own check unusable.
- **For metal complexes, the first-shell donor count and its ligand/water split must match.** This
  catches water loss and chelate opening.

Structures failing either test were **rejected and counted**, not silently dropped. Survivors were
deduplicated on energy (within 0.10 kJ mol⁻¹) *and* heavy-atom RMSD after Kabsch alignment (within
0.25 Å) together; a pair had to be close on both to count as one conformer.

**Retention window: 3.0 kcal mol⁻¹ (12.55 kJ mol⁻¹)** above the lowest conformer, as specified.

---

## 3. RESULTS, PER SPECIES

`torsions` = rotatable torsions found · `starts` = starting geometries optimised (torsion grid +
water samples + embeddings) · `unique` = distinct conformers after deduplication · `≤3 kcal` =
conformers retained in the window · `rejected` = failed the connectivity or coordination check ·
`spread` = energy range across the retained window.

| Species | Torsions | Starts | Unique | ≤3 kcal | Rejected | Spread / kJ mol⁻¹ | Carried forward |
|---|---|---|---|---|---|---|---|
| `lig_P0_LH2` | 4 | 76 | 22 | 13 | 0 | 10.28 | lowest |
| `lig_P1_LH1m` | 3 | 68 | 10 | 2 | 0 | 0.02 | lowest |
| `lig_P2_L2m` | 2 | 64 | 4 | 2 | 0 | 0.51 | lowest |
| `water` | 0 | 1 | 1 | 1 | 0 | 0.00 | the monomer; rigid |
| `pb_aquo6` | 0 | 21 | 17 | 17 | 0 | 2.24 | lowest |
| `pb_aquo8` | 0 | 21 | 21 | 21 | 0 | 9.74 | lowest |
| `cu_aquo6` | 0 | 21 | 16 | 16 | 0 | 8.94 | lowest |
| `zn_aquo6` | 0 | 21 | 4 | 4 | 0 | 4.74 | lowest |
| `pb_P0_cplx` | 2 | 16 | 11 | 2 | 0 | 0.69 | lowest |
| `pb_P1_cplx` | 2 | 16 | 12 | 12 | 0 | 11.38 | lowest |
| `pb_P2_cplx` | 2 | 16 | 15 | 15 | 0 | 12.02 | lowest |
| **`cu_P0_cplx`** | **3** | **20** | **10** | **9** | **4** | 11.83 | lowest — **see §4** |
| `cu_P1_cplx` | 2 | 16 | 14 | 12 | 0 | 9.58 | lowest |
| `cu_P2_cplx` | 2 | 16 | 15 | 12 | 0 | 11.73 | lowest |
| `zn_P0_cplx` | 2 | 16 | 9 | 4 | 0 | 3.15 | lowest |
| `zn_P1_cplx` | 2 | 16 | 9 | 9 | 0 | 9.56 | lowest |
| `zn_P2_cplx` | 2 | 16 | 11 | 10 | 0 | 12.53 | lowest |

**Totals across the seventeen species: 441 starting geometries optimised, 437 converged and passed
verification, 0 failed to converge, 4 rejected by the connectivity or coordination check, 201 unique
conformers, 161 retained within the 3 kcal mol⁻¹ window.**

In every case the structure carried forward as the DFT starting geometry is **the lowest-energy
conformer that passed verification.** The retained window is kept in
[`rotamers/<species>_ensemble.xyz`](rotamers/) so the selection can be audited and so the
conformational spread can be quoted as an uncertainty alongside the production free energies.

### 3.1 A note on the "unique" counts

The deduplication aligns structures by rotation and translation but not by reflection, so a pair of
mirror-image conformers — identical in energy, distinct in coordinates — is counted twice. This
inflates the `unique` column slightly for the more symmetric species and has no effect on which
conformer is carried forward. It is stated because the count is reported.

---

## 4. THE ONE SPECIES THAT BEHAVED DIFFERENTLY — `cu_P0_cplx`

`cu_P0_cplx` is the only species with a non-zero rejection count, and the only one whose torsion
count differs from its Pb and Zn analogues. Both facts have the same cause.

At GFN2-xTB level the **neutral** ligand LH₂ does not hold bidentate coordination on Cu(II): the
second phenolic oxygen relaxes to 3.24 Å while the first stays at 2.30 Å, leaving a five-coordinate
monodentate complex. The corresponding Pb and Zn P0 complexes both retained bidentate coordination.
Because a phenolic oxygen is then free rather than metal-bound, the structure has a **third**
rotatable hydroxyl, which is why it has three torsions and twenty starting geometries where its
analogues have two and sixteen. The four rejections are starting geometries that relaxed to a
different first-shell composition again.

This is chemically reasonable — a neutral catechol is a weak donor, and the Jahn–Teller distortion of
d⁹ Cu(II) disfavours a sixth short bond. **It is not yet known whether it survives at the production
level of theory, and no decision is taken on it here.** It matters because a monodentate Cu product
displaces one water where the bidentate Pb and Zn products displace two, which would break the
matched stoichiometry the metal comparison depends on. Carried as an open item in
[`../REACTIONS.md`](../REACTIONS.md) §3.2 and [`MODEL_JUSTIFICATION.md`](MODEL_JUSTIFICATION.md) §6.

---

## 5. LIMITATIONS, STATED

1. **The conformer search is semi-empirical.** GFN2-xTB orders the conformers; it does not settle
   them. The ordering is re-tested at the production level of theory on the retained window before
   any free energy is quoted, and where the window is narrow — `lig_P1_LH1m` spans 0.02 kJ mol⁻¹
   across two conformers, `pb_P1_cplx` 11.38 kJ mol⁻¹ across twelve — the DFT re-ranking may not
   agree with the GFN2 one.
2. **The aquo-ion search samples rather than enumerates.** Twenty seeded random water orientations do
   not exhaust a six-rotor space. The search is reproducible and it found a 2.24–9.74 kJ mol⁻¹ spread,
   but it cannot be claimed to have found the global minimum.
3. **Coordination-sphere isomerism was not searched.** Each metal complex was built from an ideal
   octahedron with the chelate in a fixed position, and the search explored torsions and water
   orientations around that arrangement. Alternative first-shell arrangements — in particular a
   different Jahn–Teller axis for Cu(II), or a holodirected versus hemidirected basin for Pb(II) —
   were not systematically enumerated. **This is the most consequential limitation in this list**,
   because hemidirection is the mechanism the report advances; the optimiser was allowed to find the
   distortion from a deliberately undistorted start rather than being steered into it, but a basin it
   did not reach from that start would not have been found. Stated in report §5.3.
4. **GFN2-xTB is not parameterised for coordination-compound conformational energetics**, and the
   Cu(II) Jahn–Teller description in particular is unreliable at this level — the pre-optimised
   `cu_aquo6` shows a *compressed* rather than the expected *elongated* octahedron. The DFT
   optimisation is what decides this; the pre-screen geometry must not be read as a result.

---

## 6. REPRODUCING THIS

```bash
conda activate biosorb
python dft/structures/build_structures.py       # build all 17 starting geometries
python dft/structures/run_xtb_preopt.py         # GFN2-xTB/ALPB(water) pre-optimisation
python dft/structures/build_rotamers.py <species> ...   # conformer search
python dft/structures/check_geometries.py       # integrity verification
python dft/structures/emit_prescreen_csv.py     # regenerate xtb_prescreen.csv from the headers
```

Every random seed is fixed. `run_crest.py` is retained so that the CREST attempt, and its failure,
remain reproducible rather than merely asserted.
