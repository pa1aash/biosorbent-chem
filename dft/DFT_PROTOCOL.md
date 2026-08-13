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

**The pK_a that motivates this whole design is not yet sourced.**

`\TODOPAL{source this pKa value before it is used in the report. The three-state P0/P1/P2 design
rests on the claim that the galloyl group is predominantly protonated at pH 5, and that claim rests
on a phenolic pKa. This document previously asserted "gallic acid's most acidic phenolic OH has pKa
approximately 8.5" with NO citation, and that assertion has been withdrawn rather than retained.
STRONGEST SOURCE: a compound-level NMR study of methyl gallate's microscopic phenolic pKa values, if
one exists -- search terms "methyl gallate" microscopic pKa NMR ellagitannin deprotonation. That
would be both compound-specific and position-specific, and position-specific matters here because
the model chelates through a particular vicinal pair. ACCEPTABLE FALLBACK: a generic gallic acid
phenolic pKa (values around 8.7 appear in standard compilations), but ONLY if cited to a real,
verified source AND accompanied by the caveat that methyl gallate lacks the carboxylic acid group
present in gallic acid, so the value may not transfer exactly. Per the reference rule, whatever is
used must resolve against Crossref and must have been read.}`

Until that citation exists, the following statement is **carried as an unsourced premise and must not
be repeated in the report**: that at pH 5.0 the galloyl group is predominantly protonated, on the
grounds that its most acidic phenolic OH has a pK_a well above 5.

**The three-state design does not collapse if the premise is wrong** — it is what makes the premise
unnecessary. Metal binding at catechol-type sites commonly proceeds with metal-induced deprotonation,
so assuming either extreme would be a bare assumption of exactly the kind the Bible §3.1 warns
against. The pK_a determines only which state is described as the *expected* dominant one; all three
are computed regardless, and the reported claim is the one that survives all three.

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

#### 1.3.1 The P1 deprotonation site is a STATED ASSUMPTION, not a resolved result

**This is a labelled assumption. It must be described as one wherever P1 results appear.**

This protocol fixes the *charge* of the LH⁻ state. It does not fix **which** of the three phenolic
hydroxyls loses its proton, and methyl gallate has three, so LH⁻ is three distinct isomers. The
structures carried forward are deprotonated at the **4-OH**, chosen because that oxygen is one of the
chelating vicinal pair and because the resulting phenolate is conjugated *para* to the
electron-withdrawing ester.

**A screen was run and it could not settle the question.** All three mono-deprotonated isomers were
optimised at GFN2-xTB/ALPB(water), giving the 4-OH isomer lowest and the 3-OH isomer **3.30 kJ mol⁻¹**
above it. That signal is **five times smaller** than the **16.96 kJ mol⁻¹** conformational effect
subsequently found *within the same species* by the conformer search — so the isomer comparison,
which used one conformer per isomer, cannot discriminate between the two candidate sites. It
establishes only that the 5-OH isomer is the poor one.

**Consequence:** the site is an assumption pending resolution, not a screened result, and the report
says so rather than implying the screen decided it. Resolving it requires a conformer search per
isomer followed by confirmation at the production level of theory — two additional jobs. **Not
attempted in the current scope.** Full detail and the numbers in
[`structures/MODEL_JUSTIFICATION.md`](structures/MODEL_JUSTIFICATION.md) §3.1 and
[`structures/CONFORMER_SCREEN.md`](structures/CONFORMER_SCREEN.md). Ruling **D-03** of 13 August 2026.

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

### 2.1 Coordination number of the aquo ion — RULED, 13 August 2026

**n = 6 for all three metals. [Pb(H₂O)₆]²⁺ is the reference state for the headline ΔG_exchange
comparison.** This supersedes the earlier provision that the lower-free-energy Pb structure would be
adopted as the reference, which contradicted §3.5 and is withdrawn.

**[Pb(H₂O)₈]²⁺ is retained** — the structure, its pre-screen energy and its production job all stand.
Its **role is reclassified**: it is a computed alternative for the limitations discussion and for the
§6 validation of the Pb–O bond length, **not** the headline reference state.

**Why six, when the GFN2-xTB screen prefers eight.** The screen does prefer the eight-coordinate ion,
and that preference is not disputed here. It is set aside for two reasons.

1. **The screening result is not decisive for a question this subtle.** It is a semi-empirical
   tight-binding energy, and the comparison it makes is between species of different composition.
   A coordination-number preference for a heavy post-transition ion in water is not something a
   GFN2-xTB screen settles.
2. **Six is required for a controlled comparison.** The argument the report advances is a
   *difference between metals*. That difference is interpretable only if the three reactions are of
   the same class — same denticity, same number of waters displaced, same Δn, same species count on
   each side. Fixing n = 6 across all three metals makes the comparison isodesmic, so that any energy
   difference found is attributable to **the metal** rather than to comparing reactions of different
   order. Allowing Pb alone to react from an eight-coordinate reactant would release four waters
   against two for Cu and Zn, and the extra water terms would not cancel in ΔΔG. The Pb preference
   would then be contaminated by the hydration-number difference rather than measuring it.

**Pb's preference for variable and higher coordination numbers is not being denied.** It is a real
consequence of the stereochemically active 6s² lone pair, and it is exactly the chemistry this report
is about. It is being **set aside as a controlled-comparison decision** and stated as a limitation —
see §2.2. Silently assuming six for Pb would be the flaw a computational referee looks for; assuming
six, saying so, giving the reason and computing the alternative anyway is not.

### 2.2 LIMITATION — the fixed Pb coordination number

*Reusable near-verbatim in report §5.3.*

> The lead(II) aquo ion was modelled as six-coordinate, [Pb(H₂O)₆]²⁺, to match the six-coordinate
> reference states used for copper(II) and zinc(II). This was a deliberate choice in favour of a
> controlled comparison: holding the coordination number, the denticity and the number of displaced
> water molecules constant across the three metals makes the three exchange reactions isodesmic, so
> that the computed differences between them are attributable to the identity of the metal rather
> than to a difference in the reaction being computed.
>
> The choice is nevertheless a simplification, and the present study's own screening indicates as
> much: at the GFN2-xTB level the eight-coordinate ion [Pb(H₂O)₈]²⁺ is favoured. Lead(II) is known to
> adopt variable and often higher coordination numbers, a consequence of the same stereochemically
> active 6s² lone pair that produces the hemidirected geometry this work reports. Constraining it to
> six therefore describes the lead centre less faithfully than it describes the two transition-metal
> comparators, and the absolute lead binding free energy reported here should be read with that in
> mind. The *relative* quantity that carries the argument is less affected, because the constraint is
> applied identically in every reaction entering the comparison.
>
> Two directions would resolve it. The first is a direct comparison of lead at both coordination
> numbers at the density-functional level rather than at the semi-empirical level used for screening,
> which would establish whether the eight-coordinate preference survives a proper treatment. The
> second is an assessment of which coordination number is favoured **in water** rather than in the
> gas phase, with the implicit solvation model applied to both, since the hydration free energy of
> the additional water molecules is precisely what the gas-phase screen omits. Both are named as
> future work in §5.4.

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

### 3.7 QC CHECKPOINT — denticity is measured on every optimised complex, never assumed

**Attack A31.** A specification for a check that runs once jobs exist. It is written now so that it
is not improvised later.

**The starting geometry is not constrained.** The GFN2-xTB pre-screen showed the neutral P0 ligand
opening to **monodentate** coordination on Cu(II) — the second galloyl oxygen relaxing to 3.24 Å —
while the Pb and Zn P0 complexes retained bidentate coordination. **The DFT starting geometry is
deliberately not constrained to force the bidentate mode.** Imposing a restraint would decide the
chemistry rather than measure it, in exactly the way §5 forbids for hemidirection. The optimiser is
allowed to find whatever mode the level of theory supports, and the mode it finds is a result.

**Required of the harvesting script**, for **every** metal × protonation-state combination, not for
Cu P0 alone and not sampled:

| Reported quantity | Definition |
|---|---|
| M–O(galloyl) distance, **both** oxygens | Distance from the metal to each of the two vicinal galloyl oxygens O3 and O4, in Å, individually — never averaged, because averaging is what would hide a monodentate structure. |
| Denticity verdict | **bidentate** if both galloyl oxygens lie within the first-shell cutoff; **monodentate** if one does; **dissociated** if neither does. |
| First-shell donor count | Total oxygens within the cutoff, and the split into galloyl and water oxygens. |
| Flag | Set whenever the verdict differs from bidentate, **or** differs from the verdict for the same protonation state on another metal. |

**This is not optional, and the result is not assumed uniform.** Report **Table 4.7 carries a
denticity and first-shell-donor-count column for every metal-protonation-state combination**, filled
from the measured geometry. A table that reports one coordination mode as though it applied to all
nine species would be asserting the thing the checkpoint exists to test.

The same cutoffs and the same first-shell logic already used at the pre-screening stage are reused,
so the pre-screen and production verdicts are directly comparable:
[`structures/geom_utils.py`](structures/geom_utils.py) and
[`structures/check_geometries.py`](structures/check_geometries.py).

### 3.8 CONTINGENCY — if Cu(II) P0 is genuinely monodentate at DFT level

*Decided in advance, on 13 August 2026, so that it does not have to be decided under deadline
pressure. Written out in full for that reason.*

**Case A — the P0 complex optimises to bidentate for all three metals.** The GFN2 result was a
semi-empirical artefact. Nothing changes: x = 2 holds for all nine reactions, the P0 row of the
comparison is reported without qualification, and the pre-screen discrepancy is noted in one sentence
as an example of why the denticity checkpoint exists.

**Case B — Cu(II) P0 remains monodentate while Pb and Zn P0 are bidentate.** This is **a finding, not
a failure**, and it is reported as one:

1. **State it as a result.** Copper(II) cannot maintain the same coordination mode as lead(II) and
   zinc(II) toward the neutral galloyl ligand at this protonation state. The interpretation offered
   is the one the geometry supports — a neutral catechol is a weak donor, and the Jahn–Teller
   distortion of a d⁹ centre disfavours a sixth short bond — stated with that basis rather than
   asserted.
2. **The stoichiometry is no longer matched.** A monodentate Cu product displaces **one** water where
   the bidentate Pb and Zn products displace two. The P0 Cu reaction is then

   ```
   [Cu(H2O)6]2+  +  LH2  ->  [Cu(LH2)(H2O)5]2+  +  1 H2O        x = 1,  dn = 0
   ```

   against x = 2 and Δn = +1 for Pb and Zn. **The standard-state correction differs, and the water
   terms no longer cancel in ΔΔG.**
3. **The P0 cross-metal comparison carries an explicit caveat and is not presented as directly
   comparable.** The P0 row of Table 4.9 and every statement of P0 selectivity is marked with the
   denticity mismatch, in the table itself and not only in a footnote. **ΔΔG(Pb − Cu) at P0 is not
   quoted as a like-for-like selectivity figure.** Quoting it without qualification would compare
   reactions of different order and attribute the difference to the metal, which is precisely the
   error the n = 6 ruling of §2.1 exists to prevent — the same principle applies here.
4. **The argument does not depend on P0.** The report's claim is the one that survives all three
   protonation states (§1.3). P1 and P2 both retained bidentate coordination for all three metals at
   the pre-screen stage, so the ordering can still be tested on a matched basis at those states, and
   the P0 result enters as supporting evidence with its caveat rather than as a headline number.
5. **What is *not* done.** The Cu P0 complex is **not** re-optimised under a restraint to force
   bidentate coordination in order to restore comparability. A restrained geometry is not a minimum,
   its frequencies are not meaningful, and its free energy would be a number with no physical
   referent. If a matched comparison is wanted at P0, the correct route is to compute the
   **monodentate form for all three metals** as a second, internally matched set — and that is named
   as future work rather than attempted before the deadline.

**Case C — Pb or Zn P0 also goes monodentate.** If all three go monodentate, comparability is
restored at x = 1 and the P0 row is reported on that matched basis, with the change of reaction class
stated. If the pattern is mixed in some other way, Case B applies to whichever metals differ.

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
| 3 | [Pb(H₂O)₆]²⁺, [Pb(H₂O)₈]²⁺ | 2 | 2 | **n = 6 is the reference state (§2.1). n = 8 is computed as the limitations-discussion alternative and for the §6 validation — it is not the headline reference.** |
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
| xtb available | ✅ xtb 6.7.1, working — all 17 structures pre-optimised at GFN2-xTB/ALPB(water) |
| **CREST available** | ❌ **installed but NON-FUNCTIONAL on this machine.** CREST 3.0.2 aborts in its metadynamics driver (`Factorisation of matrix failed lapack_sytrf`) at GFN2 and GFN-FF, in gas phase and in solvent, on one thread and on eight. Characterised and worked around — see `structures/CONFORMER_SCREEN.md` §2.1. |
| Conformer screening | ✅ **complete for all 17 species** by systematic torsion enumeration plus seeded water-orientation sampling plus distance-geometry embedding — `structures/CONFORMER_SCREEN.md` |
| Structures built | ✅ **all 17**, charge and multiplicity in every file header — `structures/` |
| Reaction definitions | ✅ `REACTIONS.md` — **but see its §3.1, an unresolved conflict over the Pb coordination number that blocks job submission** |
| Hetzner instances | ⬜ not yet provisioned; scripts ready in `hetzner/` |
| Any DFT calculation run | ❌ **none** |
