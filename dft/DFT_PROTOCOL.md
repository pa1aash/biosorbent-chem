<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# COMPUTATIONAL PROTOCOL

**This document becomes Table 3.1 and Section III of the report verbatim.** Every field is decided
and justified here so that nothing is decided at writing time.

**Nothing has been computed.** Because nothing is fixed, the protocol is chosen for **defensibility**,
not to reproduce the Stage-1 outline. The outline's ΔG°_bind values (−145.2 / −110.4 / −85.6 kJ mol⁻¹)
have **no stated reference state** and are **not carried forward** (attack A04). `f_orb = 0.38` is
**not carried forward** either: the decomposition scheme had not been chosen when it was written
(attacks A01, A13).

> **If defensible numbers differ from the outline's, the report changes and the abstract is amended.
> Correctness beats consistency with the outline.**

---

## 1. CLUSTER MODEL

### 1.1 What the pocket is
Tannic acid (C₇₆H₅₂O₄₆) is a decagalloyl glucose. The oxygen-donor site responsible for metal
binding is the **galloyl group — 3,4,5-trihydroxybenzoyl** — whose *vicinal* hydroxyls form a
catechol-type chelating pair.

### 1.2 The model, and its truncation
**Model: methyl gallate** — methyl 3,4,5-trihydroxybenzoate, C₈H₈O₅.

| Truncation decision | Justification |
|---|---|
| One galloyl unit, not the whole tannic acid molecule | 76 heavy atoms is not tractable at hybrid-DFT + frequency in this timeframe, and the electronic structure of the binding event is local to the chelating diol. |
| The ester link to glucose is capped with a **methyl group** | The glucose core is an sp³ polyol spectator. A methyl ester preserves the electron-withdrawing carboxylate ester on the ring — which is what tunes the phenolic acidity — while removing 60 spectator atoms. Capping with **H** (giving gallic acid) would change the ring substituent from an ester to a carboxylic acid and shift the pK_a; capping with methyl is the smaller perturbation. |
| Dangling bonds | None are created. The cut is made at the ester C–O bond and satisfied with a methyl carbon, so no radical centres and no link-atom artefacts arise. |
| Only one galloyl coordinates the metal | Stated as a limitation. In the real material two galloyl units on adjacent depside arms could converge on one metal. A bis-galloyl model is **explicitly cut** from this project's scope (§7 below) and named in §5.3 and §5.4 of the report. |

**This truncation is defensible because the comparison is internal.** All three metals see the same
model at the same level of theory. The quantity that carries the argument is the **difference**
between metals, not the absolute binding energy — and truncation errors that are common to all three
largely cancel in ΔΔG.

**Figure requirement:** the model is shown with atom labels as part of Fig 4.10.

### 1.3 Deprotonation state at pH 5 — a sensitivity set, not an assumption
Gallic acid's most acidic phenolic OH has pK_a ≈ 8.5, so **at pH 5.0 the galloyl group is
predominantly protonated**. Metal binding at catechol-type sites nevertheless commonly proceeds with
metal-induced deprotonation. Assuming either extreme would be a bare assumption of exactly the kind
the Bible §3.1 warns against.

**Three states are therefore computed for every metal**, and the *ordering* is tested across all
three:

| State | Ligand | Complex charge | Comment |
|---|---|---|---|
| **P0** | LH₂ — neutral, fully protonated | +2 | The dominant solution species at pH 5 |
| **P1** | LH⁻ — mono-deprotonated | +1 | Metal-induced single deprotonation |
| **P2** | L²⁻ — bis-deprotonated chelate | 0 | The classical catecholate chelation mode |

**The reported claim is the one that survives all three.** If the Pb > Cu > Zn ordering holds across
P0, P1 and P2, it is robust to the protonation assumption and the report says so. If it does not,
the report reports that instead. This *is* the sensitivity check, and it converts the single most
attackable assumption in the model into a result.

---

## 2. THE REACTION — AQUO-LIGAND EXCHANGE

**Attack A04, rated 🔴 CRITICAL.** Naked-ion binding energies are physically meaningless: they
measure the energy of an ion that does not exist in water. **The naked-ion form is never computed as
the headline quantity.**

The reaction is written as **charge-conserving aquo-ligand exchange**, one per protonation state:

```
  P0:  [M(H2O)6]2+  +  LH2   ->  [M(LH2)(H2O)4]2+  +  2 H2O
  P1:  [M(H2O)6]2+  +  LH-   ->  [M(LH)(H2O)4]+    +  2 H2O
  P2:  [M(H2O)6]2+  +  L2-   ->  [M(L)(H2O)4]      +  2 H2O
```

Three properties make this the defensible choice:

1. **Charge is conserved** on both sides, so the (large, convention-laden) Born solvation error
   largely cancels.
2. **No free proton appears.** The solvated-proton free energy is the single most convention-
   dependent quantity in aqueous computational thermochemistry; a reaction that avoids it avoids the
   argument.
3. **The number and type of species is matched across the three metals**, so the metal-to-metal
   difference ΔΔG — the quantity that actually carries the argument — is close to isodesmic.

**Coordination number of the aquo ion.** Six is used for Cu(II) and Zn(II). **Pb(II) is the
exception**: its hydration number is not firmly six, and the 6s² lone pair distorts the shell.
Both **[Pb(H₂O)₆]²⁺** and **[Pb(H₂O)₈]²⁺** are computed and the lower-free-energy structure is used
as the reference, with the choice reported. Silently assuming six for Pb is exactly the sort of
detail a computational referee looks for.

---

## 3. LEVEL OF THEORY

| Field | Decision | Justification |
|---|---|---|
| **Functional** | **PBE0** (25% exact exchange) | A global hybrid with a moderate exact-exchange fraction. For **Cu(II) d⁹**, pure GGAs over-delocalise the singly-occupied orbital and functionals with high HF exchange over-localise it; 25% is the standard compromise for 3d transition-metal complexes. PBE0 is also well behaved for main-group and post-transition systems, so a **single functional serves all three metals** — which matters, because the argument depends on an internally consistent comparison, not on the best possible number for any one metal. |
| **Dispersion** | **D3 with Becke–Johnson damping**, D3(BJ) | Required: the galloyl ring stacks against the aquo shell and dispersion is not negligible at these distances. Cite Grimme et al. 2010 (already outline ref [8]) and Grimme, Ehrlich & Goerigk 2011 for BJ damping. |
| **Cross-check** *(if time allows)* | **ωB97X-D4** single points at the PBE0 geometries | A range-separated functional from a different family. If the ordering is unchanged, that is reported as a functional-robustness check. **This is optional and is cut first** if the schedule slips. |

### 3.1 Basis sets and relativistic treatment — attack A03, 🔴 CRITICAL

| Element | Basis | Core treatment |
|---|---|---|
| **Pb** | **def2-TZVP** | **def2-ECP** — the Stuttgart–Cologne **ECP60MDF** small-core relativistic effective core potential, 60 core electrons, 22 in valence. **Scalar-relativistic effects are included through the ECP parameterisation.** |
| **Cu, Zn** | **def2-TZVP** | all-electron |
| **C, H, O** | **def2-TZVP** | all-electron |
| Auxiliary | **def2/J** for RIJCOSX | |

**The ECP is named, not implied.** "def2-ECP" alone is insufficient — the report states
**ECP60MDF, 60 core electrons**, and cites the def2 basis paper (Weigend & Ahlrichs 2005) and the
Pb ECP paper (Metz, Stoll & Dolg 2000). A Pb calculation with no relativistic treatment is a fatal
and easily spotted flaw; naming the ECP and its core size closes attack A03 completely.

*Alternative if an all-electron treatment is preferred:* **ZORA** with the SARC/ZORA-def2 basis sets,
which ORCA supports. The ECP route is chosen for cost, and because the def2-ECP is extremely well
validated for Pb(II) coordination chemistry.

### 3.2 Charge and multiplicity for EVERY species — attack A02, 🔴 CRITICAL

**Every row appears in Table 3.1. Nothing is left to inference.**

| Species | Charge | Multiplicity | Config | ⟨S²⟩ |
|---|---|---|---|---|
| H₂O | 0 | 1 | closed shell | — |
| LH₂ (methyl gallate) | 0 | 1 | closed shell | — |
| LH⁻ | −1 | 1 | closed shell | — |
| L²⁻ | −2 | 1 | closed shell | — |
| [Pb(H₂O)₆]²⁺ / [Pb(H₂O)₈]²⁺ | +2 | **1** | 6s², closed shell | — |
| **[Cu(H₂O)₆]²⁺** | +2 | **2** | **d⁹, OPEN SHELL DOUBLET** | **report; ideal 0.750** |
| [Zn(H₂O)₆]²⁺ | +2 | **1** | d¹⁰, closed shell | — |
| [Pb(LHₙ)(H₂O)₄]^q | +2/+1/0 | **1** | | — |
| **[Cu(LHₙ)(H₂O)₄]^q** | +2/+1/0 | **2** | **d⁹, OPEN SHELL DOUBLET** | **report** |
| [Zn(LHₙ)(H₂O)₄]^q | +2/+1/0 | **1** | | — |

**All Cu species are unrestricted (UKS).** ⟨S²⟩ is reported for every one, with the deviation from
the ideal 0.750 stated and commented on. **If Cu(II) were treated closed-shell, the entire
computational arm would be invalid** — so the report states explicitly that it was not.

### 3.3 Solvation
**SMD**, solvent = water, at the same level as the geometry optimisation. Cite **Marenich, Cramer &
Truhlar, *J. Phys. Chem. B* 2009, *113*, 6378** — already outline ref [9].

Geometries are optimised **in solution**, not optimised in gas phase and single-pointed in solvent.
Gas-phase optimisation of a dication with anionic ligands produces geometries that do not exist in
water, and the P2 state (a dianionic ligand) is the case where it matters most.

**Stated limitation (§5.3):** implicit solvation cannot represent specific hydrogen bonding into the
vacant hemisphere of a hemidirected Pb(II) centre. This is precisely the region the mechanism claims
is empty, so the limitation is directly relevant and is stated rather than hidden.

### 3.4 Convergence, grids, frequencies

| Setting | Value |
|---|---|
| Geometry convergence | `TightOPT` |
| SCF convergence | `TightSCF` |
| Integration grid | `DefGrid3` (ORCA 6) — a dense grid is needed for reliable SMD and for the d⁹ centre |
| Approximation | RIJCOSX with def2/J |
| **Frequencies** | **Analytic, at the same level and in the same solvent, on every optimised structure** |
| Minimum confirmation | **All frequencies real.** Any structure with an imaginary mode is re-optimised along that mode and re-checked. The report states that all reported structures are true minima. |
| Thermal corrections | 298.15 K, 1 atm, rigid-rotor / harmonic-oscillator, with **low frequencies below 100 cm⁻¹ treated by the quasi-RRHO approximation of Grimme** — cite it; raw RRHO entropies for floppy aquo complexes are unreliable |

### 3.5 Standard-state corrections
Stated explicitly, because it is a standard referee probe.

- Software thermochemistry is for **1 atm ideal gas**. A correction of **RT ln(24.46) = 7.91 kJ mol⁻¹
  per mole of species** converts to a **1 mol L⁻¹** solution standard state, applied according to the
  change in the number of species (Δn = +1 for the exchange reactions as written).
- **Water is referenced to its pure-liquid standard state, 55.34 mol L⁻¹**, not 1 mol L⁻¹. For the
  two water molecules released this contributes **−2RT ln(55.34) = −19.9 kJ mol⁻¹**.
- Both corrections are stated numerically in §3.3 of the report and shown in the thermochemical
  assembly table in Appendix E.

### 3.6 Basis-set superposition error
**Counterpoise-corrected interaction energies are reported** for the metal–ligand fragmentation.
For the **exchange free energies** the correction is expected to be small and largely cancelling,
because the reactant and product complexes are of similar size and composition; the counterpoise
correction is computed for one representative case per metal and the magnitude reported, rather than
asserted to be negligible. Asserting negligibility without a number is what invites the question.

---

## 4. DECOMPOSITION ANALYSIS — attack A01, 🔴 CRITICAL

> **Read [`../vendor/README_EDA.md`](../vendor/README_EDA.md) before writing §3.4 or §4.7.**

**ETS-NOCV is a method of ADF/AMS. ADF is commercial and is NOT available to this project.
Therefore the report does NOT use the term "ETS-NOCV".** Whatever runs, it is called by its real
name, with the program and version, in Table 3.1.

### 4.1 The scheme chosen

**Primary route: charge decomposition analysis and fragment-density electrostatics, on the ORCA
wavefunctions, in Multiwfn x.x.**

| Term | How it is obtained | Honest name |
|---|---|---|
| ΔE_int | Counterpoise-corrected interaction energy of the metal-aquo and ligand fragments at the complex geometry | interaction energy |
| ΔE_elstat | Coulomb interaction between the **unrelaxed, superimposed fragment densities** | frozen-density electrostatic interaction |
| ΔE_orb | The remainder after the frozen-density term, i.e. the energy lowering on relaxing the fragment densities in each other's field | orbital relaxation / charge-transfer term |
| charge transfer | **NPA** charges and **CDA** donation / back-donation | natural population analysis; charge decomposition analysis |
| deformation density | Density difference between the complex and the superimposed prepared fragments | **"density difference"** — **not** "NOCV channels" unless NOCV orbitals are genuinely generated |

**f_orb is defined explicitly** in the report as

> **f_orb = ΔE_orb / (ΔE_elstat + ΔE_orb)**

with the statement that **this is a ratio of decomposition terms and is scheme-dependent**:
internally comparable across the three metals computed under identical settings, and **not**
transferable to values from other studies using other schemes. Saying this closes attack **A13** at
the same time as A01.

### 4.2 Fragmentation, stated
Fragment 1 = the metal with its retained aquo ligands, at the complex geometry.
Fragment 2 = the galloyl ligand in its complex-geometry conformation.
**Fragment charges and spin states are tabulated** — for Cu the metal fragment is a doublet and the
ligand fragment a singlet.

### 4.3 The fallback, decided in advance
**If Multiwfn is not obtained in time, the report does NOT contain f_orb.** It contains ΔG_exchange,
the optimised geometries, the hemidirection descriptors and the NPA charge-transfer analysis, and
§4.7 argues the covalency case from charge transfer and orbital composition alone, with the absence
of a full energy partition stated as a limitation.

**A missing decomposition, honestly declared, costs a fraction of what an invented one costs.** This
is a pre-committed decision so that it is not made under deadline pressure on 15 August.

### 4.4 What the argument actually needs
The falsification at the centre of the report is:

> Electrostatic stabilisation is largest for the most compact, hardest ion. A purely electrostatic
> model therefore predicts the **wrong** selectivity order. The orbital-interaction fraction is
> largest for Pb. Selectivity is therefore not a charge-density effect.

That needs an **internally consistent partition across three metals at one level of theory**. It
does **not** need ETS specifically. A modest scheme named accurately is stronger than a prestigious
scheme not run.

---

## 5. HEMIDIRECTION — MEASURED, NEVER ASSERTED

**Attack A14.** Implemented in [`../analysis/src/hemidirection.py`](../analysis/src/hemidirection.py),
unit-tested against a hand-worked geometry.

Let **r_M** be the metal position and **{r_i}** the positions of the *n* coordinating donor atoms.
Let **û_i = (r_i − r_M)/|r_i − r_M|**.

**Descriptor 1 — centroid displacement**

> **d = | r_M − (1/n) Σᵢ rᵢ |**  (Å)
> **d̃ = d / ⟨|rᵢ − r_M|⟩**  (dimensionless, comparable across metals with different bond lengths)

Zero for a symmetric (holodirected) donor set; large when the donors are gathered on one side.
**d̃ is the primary reported quantity** because it removes the trivial dependence on ionic radius —
without normalisation Pb would score higher simply for having longer bonds, which would be an
artefact, not a result.

**Descriptor 2 — void-hemisphere angle**, after Shimoni-Livny, Glusker & Bock

> **v̂ = − (Σᵢ ûᵢ) / |Σᵢ ûᵢ|**    (the void direction — where no donor is)
> **θ_void = min_i arccos( v̂ · ûᵢ )**    (degrees)

θ_void is the angular clearance of the empty hemisphere. **Larger means a more pronounced void**, and
the void is where the stereochemically active 6s² lone pair sits. When |Σ ûᵢ| ≈ 0 the donor set is
symmetric, no void direction exists, and the geometry is **holodirected** — the function returns that
verdict rather than an arbitrary angle.

**All three metals are measured and tabulated** (Table 4.7). The expectation is d̃ and θ_void largest
for Pb; **if the calculation does not show that, the report reports what it shows.**

---

## 6. PROTOCOL VALIDATION
Short, cheap, and disproportionately credibility-generating (Bible §3.6).

**Validation job: the Pb–O bond length of the aquo ion.** [Pb(H₂O)₆]²⁺ and [Pb(H₂O)₈]²⁺ are
optimised **under the exact production protocol** and the mean Pb–O distance compared against
published experimental (EXAFS / X-ray diffraction) and high-level computed hydration structures for
aqueous Pb(II). The deviation is reported in Å and as a percentage.

**Validation must run at the production level of theory.** A validation at a different level
validates nothing — it is a common and easily spotted mistake.

*Second validation if time allows:* the **relative** hydration free energies of Pb²⁺, Cu²⁺ and Zn²⁺,
compared against a stated literature scale. **Relative**, not absolute — see §7.

---

## 7. HYDRATION FREE ENERGIES — attack A12

Absolute single-ion hydration free energies are **convention-dependent**: they depend on the choice
of absolute proton hydration free energy and on whether the real or the surface-corrected potential
is used. Different tabulations differ by tens of kJ mol⁻¹, and a referee will know this.

**The report therefore:**
1. Cites **the source for every value used**, with the tabulation named.
2. **States the convention/scale explicitly** (e.g. Marcus, or Tissandier's cluster-pair scale).
3. **Prefers relative values** — ΔΔG_hyd(Pb − Cu) and ΔΔG_hyd(Pb − Zn) — because the convention
   cancels in the difference, and the desolvation argument only ever needs the difference.
4. Presents all of this in **Table 4.10**, one row per ion, with source and convention as columns.

The outline's ≈ −2100 kJ mol⁻¹ (Cu) and ≈ −1481 kJ mol⁻¹ (Pb) are **claims with no cited source or
convention** and are not carried forward until traced to a paper that has been read.

---

## 8. JOB INVENTORY

| # | Species | States | Jobs | Notes |
|---|---|---|---|---|
| 1 | H₂O | 1 | 1 | trivial |
| 2 | Ligand LH₂ / LH⁻ / L²⁻ | 3 | 3 | CREST conformer pre-pass, lowest conformer optimised |
| 3 | [Pb(H₂O)₆]²⁺, [Pb(H₂O)₈]²⁺ | 2 | 2 | both, lower used as reference |
| 4 | [Cu(H₂O)₆]²⁺, [Zn(H₂O)₆]²⁺ | 2 | 2 | Cu unrestricted doublet |
| 5 | Complexes, 3 metals × 3 protonation states | 9 | 9 | the expensive set |
| 6 | Validation | — | included in 3 | |
| | **Total opt+freq jobs** | | **17** | |
| | Counterpoise single points | | 3 | one per metal, P-state chosen |
| | Decomposition post-processing | | 9 | Multiwfn, cheap |

---

## 9. SCOPE CUTS — DECIDED NOW, NOT UNDER DEADLINE PRESSURE

**Cut immediately. Do not attempt.**

| Cut | Why |
|---|---|
| **Bis-galloyl / two-arm pocket model** | Roughly doubles the atom count; analytic Hessians scale steeply. Not achievable by 14 August. Stated in §5.3 as a limitation and §5.4 as future work. |
| **Explicit second solvation shell** | Adds conformational sampling that cannot be converged in the time available. |
| **QM/MM or periodic model of the fibre surface** | Named in §5.4 Future work only. |
| **Free-energy perturbation for the ΔΔG magnitude gap** | Named in §5.4 only. This is the honest answer to attack A05 and it is a *future work* answer, not a this-week answer. |
| **ωB97X-D4 functional cross-check** | Optional. **First thing cut** if the schedule slips. |
| **CCSD(T) or DLPNO-CCSD(T) reference** | Out of scope at this system size and timeframe. |

---

## 10. WHAT GOES INTO TABLE 3.1

The report's Table 3.1 is generated from this document by `tables/src/tab3_1_protocol.py` and
contains, at minimum: program and **version** · functional · dispersion correction · basis set per
element · **named ECP with core size** · solvation model and solvent · geometry and SCF convergence ·
integration grid · frequency treatment and quasi-RRHO cutoff · standard-state corrections ·
**charge and multiplicity for every species** · ⟨S²⟩ for open-shell species · decomposition scheme
**and the program that implemented it** · hardware.

`\TODOPAL{ORCA version and Multiwfn version once installed — both are required fields of Table 3.1}`

---

## 11. STATUS

| Item | Status |
|---|---|
| Protocol decided | ✅ this document |
| ORCA installed | ❌ **BLOCKER** — registration required, see `../vendor/README_ORCA.md` |
| Multiwfn installed | ❌ **BLOCKER** — manual download, see `../vendor/README_MULTIWFN.md` |
| PySCF available | ✅ installed and working — the insurance path, §see `hetzner/README.md` |
| xtb / CREST available | ✅ installed — conformer pre-pass can start today |
| Hetzner instances | ⬜ not yet provisioned; scripts ready in `hetzner/` |
| Any calculation run | ❌ **none** |
