<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# THE AQUO-LIGAND EXCHANGE REACTIONS

**Status.** Source material for report §3.2 and the specification that
[`analysis/thermo.py`](analysis/thermo.py) implements. Written before any energy exists, so that the
assembly of ΔG is fixed by design rather than settled after the numbers are in.

**Nothing has been computed.** Every free energy referred to below is a quantity to be produced by
ORCA at the level of theory fixed in [`DFT_PROTOCOL.md`](DFT_PROTOCOL.md) §3. No value appears here.

---

## 1. WHY THE REACTION IS WRITTEN THIS WAY

Attack **A04**, rated CRITICAL. A naked-ion binding energy — M²⁺ + L → ML²⁺ — measures the energy of
an ion that does not exist in water, and is not computed as a headline quantity anywhere in this
work. The reaction is instead written as **charge-conserving aquo-ligand exchange**, in which the
incoming galloyl ligand displaces water from the metal's first coordination sphere.

Three properties make this the defensible form, per [`DFT_PROTOCOL.md`](DFT_PROTOCOL.md) §2:

1. **Charge is conserved across the equation**, so the large, convention-laden Born solvation error
   largely cancels.
2. **No free proton appears.** The solvated-proton free energy is the most convention-dependent
   quantity in aqueous computational thermochemistry, and a reaction that never invokes it never has
   to defend a choice of scale.
3. **The number and type of species is matched across the three metals**, so that ΔΔG — the quantity
   that actually carries the argument — is close to isodesmic.

Property 3 is the one that constrains the stoichiometry, and it is the subject of §3 below.

---

## 2. THE NINE BALANCED EQUATIONS

Three metals × three protonation states. **M ∈ {Pb, Cu, Zn}.** The ligand L is methyl gallate,
C₈H₈O₅ in its neutral form; see [`structures/MODEL_JUSTIFICATION.md`](structures/MODEL_JUSTIFICATION.md).

### P0 — neutral ligand, LH₂

```
[M(H2O)6]2+  +  C8H8O5      ->   [M(C8H8O5)(H2O)4]2+   +  2 H2O
```

### P1 — mono-deprotonated ligand, LH⁻

```
[M(H2O)6]2+  +  C8H7O5(-)   ->   [M(C8H7O5)(H2O)4]+    +  2 H2O
```

### P2 — bis-deprotonated catecholate ligand, L²⁻

```
[M(H2O)6]2+  +  C8H6O5(2-)  ->   [M(C8H6O5)(H2O)4]0    +  2 H2O
```

### 2.1 Balance, verified explicitly

| State | Charge, left | Charge, right | Atoms, left | Atoms, right |
|---|---|---|---|---|
| **P0** | (+2) + (0) = **+2** | (+2) + 2(0) = **+2** | M + C₈H₈O₅ + H₁₂O₆ | M + C₈H₈O₅ + H₈O₄ + H₄O₂ |
| **P1** | (+2) + (−1) = **+1** | (+1) + 2(0) = **+1** | M + C₈H₇O₅ + H₁₂O₆ | M + C₈H₇O₅ + H₈O₄ + H₄O₂ |
| **P2** | (+2) + (−2) = **0** | (0) + 2(0) = **0** | M + C₈H₆O₅ + H₁₂O₆ | M + C₈H₆O₅ + H₈O₄ + H₄O₂ |

Charge balances in all three. Atoms balance in all three: the six reactant waters (H₁₂O₆) are
partitioned into four retained (H₈O₄) and two released (H₄O₂), with the ligand carried across
unchanged.

### 2.2 Spin is conserved on both sides

| Metal | Reactant aquo ion | Product complex | Multiplicity change |
|---|---|---|---|
| Pb(II), 6s² | singlet | singlet | none |
| **Cu(II), d⁹** | **doublet, UKS** | **doublet, UKS** | **none — doublet on both sides** |
| Zn(II), d¹⁰ | singlet | singlet | none |

**All Cu species are unrestricted, on both sides of the equation.** ⟨S²⟩ is reported for each, with
its deviation from the ideal 0.750 stated. No spin-state change accompanies the exchange, so no
spin-crossover term enters ΔG. Attack **A02**.

---

## 3. x — THE NUMBER OF WATERS DISPLACED

**x = 2, identically, for all three metals and all three protonation states, as written above.**

This is not incidental. It is the condition that makes the comparison between metals mean anything,
and it must hold exactly:

- Each equation has **two reactant species and three product species**, so **Δn = +1** for every one
  of the nine. The standard-state correction of §5.2 is therefore identical across all nine and
  **cancels exactly** in every ΔΔG.
- Each equation releases **the same two water molecules**, so the water terms — both the free energy
  of water itself and its pure-liquid standard-state correction — **cancel exactly** in ΔΔG.
- Each equation retains **four waters** on the metal in the product, so the product complexes are
  six-coordinate for every metal and the coordination number does not vary across the comparison.

What survives the cancellation in ΔΔG(Pb − Cu) and ΔΔG(Pb − Zn) is the difference between metals in
how strongly the galloyl ligand is preferred over two waters. That difference is the result the
report advances.

### 3.1 UNRESOLVED — the Pb coordination number conflicts with x = 2

**This must be ruled on before any ORCA job is submitted. It is not decided here.**

[`DFT_PROTOCOL.md`](DFT_PROTOCOL.md) contains two statements that cannot both be honoured:

> **§2:** "Six is used for Cu(II) and Zn(II). **Pb(II) is the exception**: … Both **[Pb(H₂O)₆]²⁺** and
> **[Pb(H₂O)₈]²⁺** are computed and the lower-free-energy structure is used as the reference."

> **§3.5:** "…applied according to the change in the number of species (**Δn = +1** for the exchange
> reactions as written)."

Δn = +1 requires exactly two waters to be released, which requires a six-coordinate reactant aquo ion
and a four-water product. **If [Pb(H₂O)₈]²⁺ turns out to be the lower-free-energy Pb aquo ion and is
adopted as the reference, then for Pb:**

```
[Pb(H2O)8]2+  +  L  ->  [Pb(L)(H2O)4]q  +  4 H2O          x = 4,  Δn = +3
```

and x is no longer identical across the three metals. Two extra water-release terms and two extra
standard-state corrections would then enter ΔG(Pb) and *not* ΔG(Cu) or ΔG(Zn), and they would not
cancel in ΔΔG. The metal comparison would no longer be isodesmic, and the magnitude of the Pb
preference would be contaminated by the hydration-number difference rather than measuring it.

**The three ways out, with their consequences. None is adopted here.**

| Option | What it does | Cost |
|---|---|---|
| **A. Fix n = 6 for all three metals in the exchange reaction.** Report the [Pb(H₂O)₆]²⁺ ⇌ [Pb(H₂O)₈]²⁺ free-energy difference separately, as a hydration-structure result and as the §6 validation job. | Keeps x = 2 and Δn = +1 everywhere; ΔΔG stays isodesmic; §3.5 stands unaltered. | The Pb reactant is not the lowest-free-energy Pb aquo species, and the report must say so and quote the difference rather than bury it. |
| **B. Adopt the lower-energy Pb aquo ion and accept x = 4 for Pb.** | Uses the physically preferred Pb reactant. | ΔΔG is no longer isodesmic; §3.5 must be rewritten with a per-metal Δn; two extra water terms carry their full error into the Pb result. Weakens the central comparison. |
| **C. Make the Pb product eight-coordinate**, [Pb(L)(H₂O)₆]²⁺, restoring x = 2. | Keeps x = 2 and Δn = +1. | Breaks matching on the *product* side instead: the Pb complex would have six retained waters against four for Cu and Zn, so the product species are no longer of matched composition. Also requires re-deriving the hemidirection descriptors against a different donor count. |

**Both Pb aquo structures have been built and pre-optimised** (`pb_aquo6.xyz`, `pb_aquo8.xyz`), so
the §6 validation job is unaffected by this ruling and can proceed either way. Only the choice of
*reactant for the exchange reaction* is blocked.

> **Recommendation, offered but not applied: Option A.** It preserves the property the whole reaction
> design exists to secure, and it converts the awkwardness into a reported result — the hydration
> preference of Pb(II) — rather than a hidden inconsistency. **Palaash's ruling is required.**

### 3.2 A second condition on x — the Cu P0 chelation mode

x = 2 also assumes the ligand binds **bidentate**, displacing two waters. At GFN2-xTB level the
neutral P0 ligand relaxed to **monodentate** coordination on Cu(II) but stayed bidentate on Pb and Zn
— see [`structures/MODEL_JUSTIFICATION.md`](structures/MODEL_JUSTIFICATION.md) §6. A monodentate Cu
product displaces **one** water, not two.

Whether this survives DFT optimisation is not yet known and is not assumed either way here. **It must
be checked on the optimised P0 complexes before any P0 ΔΔG is reported**, and if it survives, the P0
row of the comparison must either be re-written with a matched monodentate reference for all three
metals or be reported as not comparable. The P1 and P2 states are unaffected: both retained bidentate
coordination for all three metals.

---

## 4. WHAT IS COMPARED

For each protonation state P ∈ {P0, P1, P2}:

```
  ΔΔG(Pb - Cu)|P  =  ΔG_exchange(Pb)|P  -  ΔG_exchange(Cu)|P
  ΔΔG(Pb - Zn)|P  =  ΔG_exchange(Pb)|P  -  ΔG_exchange(Zn)|P
```

A negative ΔΔG means the galloyl site prefers Pb(II) over the competitor, which is the direction the
Irving–Williams series does **not** predict for Cu(II).

**The reported claim is the one that survives all three protonation states.** If the Pb-preferred
ordering holds at P0, P1 and P2, it is robust to the protonation assumption and the report says so.
If it does not hold across all three, the report reports that instead. This is the sensitivity check
fixed in [`DFT_PROTOCOL.md`](DFT_PROTOCOL.md) §1.3, and it is not optional.

---

## 5. HOW ΔG_exchange IS ASSEMBLED

**This section is the specification for [`analysis/thermo.py`](analysis/thermo.py).** It is written
now, before the script exists, so that the assembly is not improvised around whatever ORCA happens to
print.

### 5.1 The free energy of one species

For every species i in the equation, in aqueous solution at 298.15 K:

```
  G_i(aq)  =  E_SCF,SMD(i)  +  G_CDS(i)  +  G_thermal,qRRHO(i)  +  ΔG_standard-state(i)
```

| Term | What it is | Where it comes from |
|---|---|---|
| **E_SCF,SMD** | Self-consistent-field electronic energy at the SMD-optimised geometry, including the electrostatic solvation contribution. | The solution-phase geometry optimisation. Geometries are optimised **in solution**, never in gas phase and single-pointed — protocol §3.3. |
| **G_CDS** | The SMD non-electrostatic cavity–dispersion–solvent-structure term. | Reported by ORCA alongside the SCF energy. **Implementation check: establish whether the printed final energy already contains this term before adding it, or it will be double-counted.** |
| **G_thermal,qRRHO** | H_corr − T·S, from analytic frequencies computed at the same level and in the same solvent, at 298.15 K and 1 atm, rigid-rotor/harmonic-oscillator, with modes below 100 cm⁻¹ treated by Grimme's quasi-RRHO approximation. | The frequency job. Raw RRHO entropies for floppy aquo complexes are unreliable, which is why the quasi-RRHO treatment is fixed in protocol §3.4 rather than left to the default. |
| **ΔG_standard-state** | Conversion from the 1 atm ideal-gas reference of the software's thermochemistry to the solution reference. | §5.2 below. |

**Two gates, applied per species before its energy is used:**

- **All frequencies real.** Any structure carrying an imaginary mode is re-optimised along that mode
  and re-checked. No energy from a structure with an imaginary frequency enters any sum. Protocol §3.4.
- **⟨S²⟩ recorded for every Cu species**, with its deviation from the ideal 0.750 stated. Protocol §3.2.

### 5.2 Standard-state corrections

Applied per [`DFT_PROTOCOL.md`](DFT_PROTOCOL.md) §3.5, and stated numerically in the report because
it is a standard referee probe.

- **Ideal gas at 1 atm → 1 mol L⁻¹ solution**, per mole of species: **RT ln(24.46) = 7.91 kJ mol⁻¹**.
  Applied according to the change in the number of species, **Δn = +1** for every equation in §2.
- **Water is referenced to its pure-liquid standard state, 55.34 mol L⁻¹**, not 1 mol L⁻¹. For the two
  waters released this contributes **−2 RT ln(55.34) = −19.9 kJ mol⁻¹**.

Net standard-state contribution to each of the nine reactions as written:

```
  ΔG_ss  =  (+1) x RT ln(24.46)  -  2 x RT ln(55.34)
          =  +7.91  -  19.9  =  -12.0 kJ/mol
```

**`thermo.py` must recompute both terms from R, T and the stated concentrations rather than
hard-coding them**, and assert that the recomputed values agree with the protocol's stated 7.91 and
19.9 kJ mol⁻¹. A silent divergence between the number in the code and the number in Table 3.1 is
exactly the kind of inconsistency a referee finds.

### 5.3 The exchange free energy

```
  ΔG_exchange  =  [ G(complex) + x·G(H2O) ]  -  [ G(aquo ion) + G(ligand) ]  +  ΔG_ss
```

with x = 2 subject to §3.1 and §3.2. Where a species has more than one conformer within the retained
window, the **lowest-free-energy conformer at the production level of theory** is used, and the
spread across the retained window is reported as a conformational uncertainty — see
[`structures/CONFORMER_SCREEN.md`](structures/CONFORMER_SCREEN.md).

### 5.4 Units and reporting

- **All energies in kJ mol⁻¹ throughout.** ORCA reports Hartree and some post-processing reports
  kcal mol⁻¹; both are converted on read, and **kcal mol⁻¹ never appears in the report.**
- Conversion factors are constants, not measurements: 1 Hartree = 2625.499639 kJ mol⁻¹;
  1 kcal mol⁻¹ = 4.184 kJ mol⁻¹ exactly.
- Significant figures are matched to the method's resolution, not to the printed precision of the
  output file. A ΔΔG quoted to 0.01 kJ mol⁻¹ from DFT would be a claim the method cannot support.
- Every reported ΔG and ΔΔG is traceable to an output file in [`outputs/`](outputs/), per
  [`README.md`](README.md).

### 5.5 Counterpoise

Counterpoise-corrected interaction energies are reported for the metal–ligand fragmentation, per
protocol §3.6. For the **exchange** free energies the basis-set superposition error is expected to be
small and largely cancelling, because reactant and product complexes are of similar size and
composition — but **the correction is computed for one representative case per metal and its magnitude
reported**, rather than asserted to be negligible. Asserting negligibility without a number is what
invites the question.

---

## 6. THE SPECIES INVENTORY THIS REQUIRES

Every species below exists as a pre-optimised structure in [`structures/`](structures/) with its
charge and multiplicity written into the file header.

| # | Species | Charge | Mult | Role | File |
|---|---|---|---|---|---|
| 1 | H₂O | 0 | 1 | released product, ×2 per equation | `water.xyz` |
| 2 | LH₂ | 0 | 1 | reactant, P0 | `lig_P0_LH2.xyz` |
| 3 | LH⁻ | −1 | 1 | reactant, P1 | `lig_P1_LH1m.xyz` |
| 4 | L²⁻ | −2 | 1 | reactant, P2 | `lig_P2_L2m.xyz` |
| 5 | [Pb(H₂O)₆]²⁺ | +2 | 1 | reactant | `pb_aquo6.xyz` |
| 6 | [Pb(H₂O)₈]²⁺ | +2 | 1 | §3.1 / §6 validation | `pb_aquo8.xyz` |
| 7 | **[Cu(H₂O)₆]²⁺** | +2 | **2** | reactant, **UKS** | `cu_aquo6.xyz` |
| 8 | [Zn(H₂O)₆]²⁺ | +2 | 1 | reactant | `zn_aquo6.xyz` |
| 9–11 | [Pb(LHₙ)(H₂O)₄]^q | +2 / +1 / 0 | 1 | products | `pb_P{0,1,2}_cplx.xyz` |
| 12–14 | **[Cu(LHₙ)(H₂O)₄]^q** | +2 / +1 / 0 | **2** | products, **UKS** | `cu_P{0,1,2}_cplx.xyz` |
| 15–17 | [Zn(LHₙ)(H₂O)₄]^q | +2 / +1 / 0 | 1 | products | `zn_P{0,1,2}_cplx.xyz` |

Seventeen optimisation-plus-frequency jobs, matching the inventory in
[`DFT_PROTOCOL.md`](DFT_PROTOCOL.md) §8.

---

## 7. OPEN ITEMS BLOCKING SUBMISSION OF THE ORCA JOBS

1. **§3.1 — the Pb coordination number.** Options A/B/C above. **Requires Palaash's ruling.**
2. **§3.2 — the Cu P0 chelation mode.** Check on the DFT-optimised structures; no assumption made.
3. **§5.1 — whether ORCA's printed final energy already includes the SMD G_CDS term.** Must be
   established against actual output before `thermo.py` sums anything.
4. **The P1 deprotonation site**, per [`structures/MODEL_JUSTIFICATION.md`](structures/MODEL_JUSTIFICATION.md) §3.1.
