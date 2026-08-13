<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# THE CLUSTER MODEL — WHAT IT REPRESENTS, HOW IT WAS TRUNCATED, AND WHY THAT IS DEFENSIBLE

**Status.** Source material for report §3.1. Written at report precision. The protocol decisions
recorded here were fixed in [`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §1; this document states how
they were carried into actual coordinates, and records the two points at which the protocol fixed a
*set* of options rather than a single one.

**No quantity in this document is a report number.** Every energy quoted below is a semi-empirical
GFN2-xTB pre-screen value. None enters `data/CANONICAL_NUMBERS.yaml`, and none is quoted in the
report. They are recorded because a screening decision that cannot be audited is not a decision.

---

## 1. WHAT THE MODEL REPRESENTS

The biosorbent is ossein functionalised with tannic acid. Tannic acid (C₇₆H₅₂O₄₆) is a decagalloyl
glucose: a central D-glucose core esterified at its hydroxyls by galloyl and digalloyl (depside)
arms. Metal binding is not a property of the glucose core. It is a property of the **galloyl group —
3,4,5-trihydroxybenzoyl** — whose *vicinal* hydroxyl pair forms a catechol-type chelating site.

The cluster model represents **one galloyl arm of the tannic acid graft, together with the ester
linkage through which that arm is attached to the polyol core.** It does not represent the ossein
peptide, the glucose core, or the second coordination sphere.

---

## 2. THE TRUNCATION, STATED EXACTLY

**Model compound: methyl gallate — methyl 3,4,5-trihydroxybenzoate, C₈H₈O₅.**

Ring numbering used throughout: **C1** bears the ester; **C3, C4, C5** bear the phenolic hydroxyls;
**C4** is *para* to the ester. The chelating pair used in every complex is the vicinal **O3/O4** pair.

### 2.1 Where the cut was made

One bond was cut. The galloyl arm is attached to the glucose core through an **ester linkage**, and
the cut was made at the **ester C(alkyl)–O bond** — that is, between the ester oxygen and the glucose
carbon it esterifies. Everything on the glucose side of that bond was removed: the entire D-glucose
core and the nine remaining galloyl and digalloyl arms, some 68 heavy atoms.

### 2.2 How the cut was capped

The severed valence on the **ester oxygen** was satisfied with a **methyl group**, per
[`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §1.2. The glucose carbon that was removed was an sp³
carbon bearing hydrogens and further hydroxyls; a methyl carbon is the smallest group that reproduces
its hybridisation and its σ-donating character.

### 2.3 Dangling bonds: none are created

This is the property that makes the truncation clean, and it is worth stating plainly because
link-atom artefacts are a standard referee probe. **The cut was made at a single σ bond between two
closed-shell fragments, and the severed valence was immediately satisfied by a real methyl carbon.**
Consequently:

- **No radical centre exists** in the model. The model is a closed-shell neutral molecule.
- **No link atom, no capping hydrogen with a scaled bond length, and no boundary-region charge
  redistribution** is used anywhere. There is no QM/MM boundary in this work.
- The model is a **complete, chemically real molecule** — methyl gallate is an isolable compound, not
  a computational construct. Its geometry is not constrained to mimic a fragment.

### 2.4 Why methyl and not hydrogen

Capping with hydrogen instead of methyl would give **gallic acid**, and that is a worse model, for a
reason that bears directly on the chemistry being studied. The ring substituent at C1 tunes the
acidity and the donor strength of the phenolic oxygens through its electron-withdrawing effect.

| Cap | Resulting C1 substituent | Consequence |
|---|---|---|
| Methyl | **Methyl ester**, –C(=O)OCH₃ | An ester, as in the real material. Electron-withdrawing character preserved. |
| Hydrogen | **Carboxylic acid**, –C(=O)OH | Introduces a fourth ionisable proton that does not exist in the graft, and changes the electronic character of the C1 substituent. |

In the real material the galloyl arm is attached **as an ester**, and it is never a free carboxylic
acid. Capping with hydrogen would therefore introduce an ionisable group that the material does not
have, and at pH 5 that group would be substantially deprotonated — which would change the total
charge of the ligand, change the reaction stoichiometry, and change the phenolic pK values through
the ring. **Methyl is the smaller perturbation, and it is the chemically faithful one.**

### 2.5 What was verified about the built structure

The model was built from its SMILES string, embedded, force-field relaxed and then pre-optimised at
GFN2-xTB; the resulting connectivity was re-derived from the coordinates and confirmed to be a
3,4,5-trihydroxybenzoate bearing one methyl ester, with 21 atoms and 21 bonds and no radical centre.

---

## 3. PROTONATION STATES

[`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §1.3 fixes **three** states, computed for every metal, so
that the metal ordering can be tested for robustness against the protonation assumption rather than
resting on it:

| State | Ligand | Ligand charge | Built as |
|---|---|---|---|
| **P0** | LH₂ — fully protonated | 0 | `lig_P0_LH2.xyz` |
| **P1** | LH⁻ — mono-deprotonated | −1 | `lig_P1_LH1m.xyz` |
| **P2** | L²⁻ — bis-deprotonated catecholate | −2 | `lig_P2_L2m.xyz` |

### 3.1 Which hydroxyl is deprotonated — a choice the protocol did not make

The protocol fixes the *charge* of each state. It does not fix **which** of the three phenolic
hydroxyls is removed. Methyl gallate has three, so LH⁻ is three distinct isomers, and choosing one by
assertion would be precisely the kind of bare assumption the three-state sensitivity design exists to
avoid.

**The choice made, and its basis:**

- **P1 — deprotonated at the 4-position.** The 4-OH is one of the two oxygens of the chelating vicinal
  pair, so deprotonation there is the event relevant to chelation; and the resulting phenolate is
  conjugated *para* to the electron-withdrawing ester, which stabilises it.
- **P2 — deprotonated at the 3- and 4-positions**, giving the 3,4-catecholate. This is the classical
  catechol-type chelate named in the protocol §1.1. The 3,4 and 4,5 pairs are related by the local
  mirror symmetry of the galloyl group, so choosing 3,4 is a labelling convention, not a chemical
  decision.

**The P1 site was screened rather than asserted.** All three mono-deprotonated isomers were built and
optimised at GFN2-xTB/ALPB(water):

| Isomer | Relative energy / kJ mol⁻¹ (GFN2-xTB pre-screen) |
|---|---|
| Deprotonated at 4-OH | 0.00 |
| Deprotonated at 3-OH | +3.30 |
| Deprotonated at 5-OH | +31.66 |

**This screen does not settle the choice, and the subsequent conformer search showed why.** Each
isomer above was optimised as a **single** conformer, so the comparison confounds isomer identity
with conformer choice. When the conformer search of
[`CONFORMER_SCREEN.md`](CONFORMER_SCREEN.md) was then run on the 4-OH isomer, it found a conformer
**16.96 kJ mol⁻¹** below the single-conformer structure used in the table — **five times the
3.30 kJ mol⁻¹ gap the table reports between the 4-OH and 3-OH isomers.** The conformational effect is
therefore much larger than the effect being screened for, and the table cannot discriminate between
the two candidate sites. It establishes only that the 5-OH isomer is the poor one.

A further caveat on the 5-OH result: the 3-OH and 5-OH positions are *not* equivalent in this
molecule, because the ester group lies in the ring plane and breaks the mirror symmetry that would
otherwise relate them. The large 5-OH gap is consistent with a hydrogen-bonding effect rather than an
inductive one, and is likewise single-conformer.

**Required before any P1 result is quoted:**

1. Re-run the site comparison **with a full conformer search per isomer**, so that each isomer is
   represented by its own lowest conformer rather than an arbitrary one.
2. Confirm the outcome at the production level of theory by optimising the 4-OH and 3-OH isomers
   under the full protocol.

Until both are done, the P1 site is a **stated assumption, not a screened result**, and the report
must describe it as such. Recorded in [`../../docs/DATA_REQUEST.md`](../../docs/DATA_REQUEST.md).

---

## 4. WHY THIS TRUNCATION IS DEFENSIBLE

The defence does not rest on the claim that methyl gallate reproduces the absolute binding energy of
the real material. It does not, and the report does not claim it does.

**The argument is carried by a difference, not by an absolute.** The quantity the report advances is
ΔΔG between metals — the extent to which Pb(II) is preferred over Cu(II) and Zn(II) — and the model
enters that quantity three times, identically:

1. **All three metals see the same ligand model**, at the same level of theory, in the same
   protonation state, with the same coordination number and the same number of retained waters.
2. **Truncation error is therefore common to all three metals** and cancels to first order in the
   difference. What survives the cancellation is the metal-dependent part of the interaction, which is
   what the mechanism claims is responsible for the selectivity.
3. **The comparison is internal.** No absolute binding free energy computed here is compared against
   an experimental absolute value, so no claim depends on the truncation being quantitatively
   faithful.

**The chelating unit is retained in full.** The truncation removes spectator atoms — an sp³ polyol
core and nine further arms — and retains every atom of the chelating site itself: both donor oxygens,
the aromatic ring that conjugates them, the third hydroxyl that modulates them, and the ester that
withdraws from them. The electronic structure of the binding event is local to that unit.

---

## 5. WHAT THE MODEL CANNOT REPRESENT

Stated here so that §5.3 of the report can state it, rather than being asked it.

| Limitation | Consequence | Where it is handled |
|---|---|---|
| **One galloyl unit only.** In the real material two galloyl units on adjacent depside arms could converge on a single metal centre. | A bis-galloyl site would bind more strongly than this model predicts, and the effect need not be equal across the three metals. | Formally cut from scope in protocol §9. Stated as a limitation in report §5.3, named as future work in §5.4. |
| **No glucose core, no ossein peptide.** | Any contribution from backbone carbonyls, amide nitrogens or neighbouring hydroxyls to the first or second coordination sphere is absent. | Report §5.3. |
| **No explicit second solvation shell.** Solvation is implicit (SMD). | Implicit solvation cannot represent specific hydrogen bonding into the vacant hemisphere of a hemidirected Pb(II) centre — and that vacant hemisphere is exactly what the mechanism claims exists. | Protocol §3.3; report §5.3. This is the most directly relevant limitation in the list and is stated, not hidden. |
| **The graft is modelled as a free molecule**, not as a species tethered to a solid surface. | No steric constraint from the fibre, and no restriction on the ligand's conformational freedom. | Report §5.3. |
| **A single chelation mode is imposed** — bidentate through the vicinal O3/O4 pair. Monodentate and bridging modes were not searched. | The computed complexes are the bidentate chelate, and the report must describe them as such rather than as "the" complex. | See §6 below — this is not purely hypothetical. The *starting* mode is imposed; the *optimised* mode is measured, not assumed — `../DFT_PROTOCOL.md` §3.7. |
| **Lead(II) is constrained to six-coordinate** to match the Cu and Zn reference states, although the GFN2-xTB screen favours the eight-coordinate aquo ion. | The lead centre is modelled less faithfully than the two comparators, and the absolute Pb binding free energy should be read with that in mind. The *relative* quantity carrying the argument is less affected, because the constraint applies identically in every reaction entering the comparison. | Ruling **D-01** of 2026-08-13. Limitation written out in full in `../DFT_PROTOCOL.md` §2.2, reusable near-verbatim in report §5.3. Attack **A33**, ACCEPTED RISK. |

---

## 6. AN OBSERVED CONSEQUENCE OF THE MODEL, RECORDED NOW

At GFN2-xTB level the imposed bidentate chelation **did not survive for one species**: in
`cu_P0_cplx`, the neutral ligand LH₂ opened to **monodentate** coordination on Cu(II), the second
phenolic oxygen relaxing to 3.24 Å while the first remained at 2.30 Å. The corresponding Pb and Zn
P0 complexes both retained bidentate coordination.

This is chemically reasonable — a neutral catechol is a weak donor, and the Jahn-Teller distortion of
d⁹ Cu(II) disfavours a sixth short bond — but it matters for the reaction scheme, because a
5-coordinate monodentate Cu product is **not** the same species as the 6-coordinate bidentate Pb and
Zn products, and the ΔΔG comparison assumes matched species on both sides.

**It is not yet known whether this survives at the production level of theory.** Ruled 13 August
2026 (**D-02**): the DFT starting geometry is **not** constrained to force bidentate coordination.
Imposing a restraint would decide the chemistry rather than measure it, and a restrained geometry is
not a minimum — its frequencies and its free energy would have no physical referent. Denticity is
instead **measured** on every optimised complex by the QC checkpoint in
[`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §3.7, which reports both M–O(galloyl) distances
individually for every metal-protonation-state combination, and the contingency for a confirmed
mismatch is written out in advance in §3.8. Tracked as attack **A31**.

---

## 7. CONSTRUCTION AND PROVENANCE

Every structure is generated by script; none is hand-edited.

| Stage | Method | Owner of the method |
|---|---|---|
| Molecular graph | SMILES `COC(=O)c1cc(O)c(O)c(O)c1` | — |
| 3D embedding | ETKDGv3 distance geometry, fixed random seed | Riniker and Landrum, implemented in RDKit |
| Force-field relaxation | MMFF94 | Halgren |
| Conformer search | Systematic torsion enumeration plus seeded distance-geometry embedding — see [`CONFORMER_SCREEN.md`](CONFORMER_SCREEN.md) | this work |
| Pre-optimisation | GFN2-xTB with the ALPB water model, `--opt tight` | Bannwarth, Ehlert and Grimme (GFN2-xTB); Ehlert, Stahn, Spicher and Grimme (ALPB) |
| Integrity verification | Connectivity and first-shell coordination re-derived from coordinates | this work, [`check_geometries.py`](check_geometries.py) |

**Metal coordination spheres were built as ideal polyhedra** — octahedral for the six-coordinate
species, square antiprismatic for [Pb(H₂O)₈]²⁺. **No hemidirected distortion was imposed on any Pb
starting geometry.** This is deliberate and it protects the central result: hemidirection is a
quantity this work *measures* from the optimised geometry (protocol §5), so building it into the
input would beg the question the calculation exists to answer. The one starting-geometry bias that
was applied is a Jahn-Teller axial elongation on the Cu(II) species, because an undistorted
octahedron is a saddle point for a d⁹ ion and starting there wastes optimiser steps rather than
producing an unbiased result.

**Pre-optimisation is not production.** The GFN2-xTB stage exists so that no ORCA job starts from a
sketch. Every geometry is re-optimised at the level of theory fixed in protocol §3, in solution, with
analytic frequencies confirming a true minimum, and only those geometries and energies are reported.

---

## 8. CITATIONS REQUIRED BEFORE THIS TEXT ENTERS THE REPORT

Per the reference rule, no citation enters `refs/library.bib` until `verify_dois.py` resolves it
against Crossref **and** it has been read. The following are named in this document by method owner
and must be resolved to verified entries:

| Needed for | Work |
|---|---|
| GFN2-xTB | Bannwarth, Ehlert & Grimme, the GFN2-xTB method paper |
| ALPB solvation | Ehlert, Stahn, Spicher & Grimme, the ALPB implicit solvation paper |
| ETKDGv3 | Riniker & Landrum, experimental-torsion distance geometry |
| MMFF94 | Halgren, the MMFF94 series |
| Tannic acid structure and galloyl chelation | a verified source for the decagalloyl glucose structure |
| **Phenolic pK_a** | **Resolved as far as it can be without Palaash: the unsourced assertion has been withdrawn.** [`../DFT_PROTOCOL.md`](../DFT_PROTOCOL.md) §1.3 previously stated "pK_a ≈ 8.5" with no citation; it now carries a `\TODOPAL` naming the preferred source — a compound-level NMR study of **methyl gallate's** *microscopic* phenolic pK_a values, which is both compound- and position-specific — and the acceptable fallback of a generic gallic acid phenolic pK_a, cited to a real verified source and carrying the caveat that methyl gallate **lacks the carboxylic acid group** present in gallic acid so the value may not transfer exactly. Ruling **D-04**, attack **A32**. **Awaiting Palaash's citation.** |

---

## 9. OPEN ITEMS

All three were ruled on 13 August 2026. None now blocks work; each remains open only in the sense
noted.

| Ref | Item | State after the ruling |
|---|---|---|
| **D-03** | P1 deprotonation site (§3.1). | **Carried as a labelled stated assumption**, not a result. Resolving it needs a conformer search per isomer plus production-level confirmation — two jobs, out of current scope. |
| **D-02** | Cu P0 chelation mode (§6). | **Measured, not forced.** No restraint applied; QC checkpoint specified and contingency pre-written. Resolvable only once the DFT geometry exists. Attack **A31**. |
| **D-04** | Phenolic pK_a citation (§8). | **Assertion withdrawn**, `\TODOPAL` in place. **Requires Palaash to supply or confirm a citation.** Attack **A32**. |
| **D-01** | Pb coordination number (§5). | **CLOSED — CN = 6.** Retained as a stated limitation, not an open question. Attack **A33**, ACCEPTED RISK. |
