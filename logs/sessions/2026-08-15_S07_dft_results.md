<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# SESSION RECORD — S07, 15 August 2026

> ## ⚠ THIS IS NOT THE VERBATIM TRANSCRIPT
>
> This file is an **assistant-written account** of what the session did. It is **not** a chat log and
> **must not** be submitted as one. CLAUDE.md §7.1 is binding: a session record is never a substitute
> for the client export, and Appendix A is assembled from **exports**, not from records.
>
> `\TODOPAL{Export the verbatim S07 transcript from the Claude Code client and save it to
> logs/sessions/ alongside this record. Until that file exists this session has NO Appendix A entry.
> This marker is cleared only when the real export is present — never because this record looks
> complete.}`

**Session ID** S07 · **Stage** computational arm — extraction of scientific results
**Tool** Claude Opus 5 (`claude-opus-5[1m]`, Claude Code)
**Scope** Analysis only. No job re-run, no structure re-optimised, no report prose, no number adjusted.

---

## 1. WHAT THE SESSION WAS ASKED TO DO

Extract the scientific results from the seventeen completed ORCA jobs, in eight phases: an integrity
gate; re-verification of the C-01 energy identity on a charged and an open-shell species; geometry
and denticity; reaction free energies; the ordering question; hemidirection; the Pb coordination
number; then population of the canonical-numbers file, the results summary, the attack register and a
plain-language report of what was found.

The brief was explicit that an honest negative result was wanted if that is what the numbers gave,
and that no subset of the data was to be selected to produce a preferred answer.

---

## 2. WHAT WAS BUILT

Nine new files in `dft/analysis/`, all committed:

| File | Role |
|---|---|
| `orca_parse.py` | single-source ORCA 6.1.1 parser; every downstream consumer reads through it |
| `integrity_gate.py` | Phase 1 — the four-part completion test and the all-real-frequency gate |
| `verify_c01.py` | Phase 2 — four energy identities, on all seventeen jobs |
| `denticity.py` | Phase 3 — denticity and first-shell composition, measured |
| `thermo.py` | Phase 4 — the exchange free energies, implementing `REACTIONS.md` §5 |
| `selectivity.py` | Phase 5 — the ordering, and the gap against the outline's α |
| `run_hemidirection.py` | Phase 6 — drives `analysis/src/hemidirection.py` over all thirteen centres |
| `pb_coordination.py` | Phase 7 — the CN = 6 versus CN = 8 comparison |
| `emit_canonical.py` | Phase 8 — writes the results into `data/CANONICAL_NUMBERS.yaml` |
| `G_COMPOSITION.md` | the auditable specification of what G contains |
| `RESULTS_SUMMARY.md` | every table from Phases 1–7 |

A hand-written parser was necessary because **cclib 1.8.1 still cannot read ORCA 6.1.1 output** — the
same limitation recorded in S05.

---

## 3. WHAT THE CALCULATIONS FOUND

### The result the project did not want

**The computed ordering does not reproduce Pb > Cu > Zn at any protonation state.** Lead is preferred
over copper only at P0 (ΔΔG = −17.8 kJ/mol); at P1 and P2 copper is preferred over lead by +11.2 and
+10.0 kJ/mol. All three ΔΔG(Pb−Cu) values are denticity-matched, so none can be discounted on
comparability grounds. The ordering is **Pb > Zn > Cu at P0** and **Cu > Pb > Zn at P1 and P2** — it
inverts on deprotonation. Only **Pb > Zn** survives all three states.

This was reported as the headline of `RESULTS_SUMMARY.md` rather than placed after the supporting
results, and a new 🔴 Critical attack row (**A34**) was opened for it.

### What the calculations do support

* **Every structure is a true minimum.** All seventeen jobs terminated normally, converged, ran
  analytic frequencies, and carry **zero imaginary modes**.
* **No spin contamination.** ⟨S²⟩ = 0.7514–0.7522 across the four Cu(II) species, +0.19% to +0.29%
  from the ideal 0.750, far below the 0.80 flagging threshold. This discharges A02's residual.
* **Hemidirection is unambiguous.** d̃ = 0.37–0.47 for lead against 0.00–0.18 for copper and
  0.001–0.08 for zinc; θ_void 95–100° against 24–83°. Insensitive to the cutoff.
* **The Pb CN = 8 preference does not survive DFT.** ΔG = +51.2 kJ/mol in favour of CN = 6, a
  127 kJ/mol swing from GFN2, driven by the entropy of binding two extra waters.

---

## 4. THINGS FOUND THAT WERE NOT ASKED FOR, AND WERE REPORTED RATHER THAN SMOOTHED OVER

1. **ORCA 6.1.1 applied quasi-RRHO by default**, with a 100 cm⁻¹ reference frequency — exactly what
   protocol §3.4 requires. **This falsifies the premise of the S04 ruling** that quasi-RRHO would be
   applied in post-processing. `thermo.py` therefore consumes ORCA's own `G-E(el)` rather than
   re-deriving it, which would have either downgraded the treatment or reproduced ORCA's arithmetic
   less reliably.
2. **The S06 log entry's "x = 1, Δn = 0 at P0" describes a reaction for which no calculation
   exists.** Every complex cluster holds four waters; no `[M(L)(H₂O)₅]^q` species was built or run.
   The monodentate complexes are five-coordinate because a galloyl oxygen dangles, not because a
   fifth water was kept. **This is more favourable than S06 assumed** — identical stoichiometry
   across all nine means ΔG_ss and the water terms cancel exactly in every ΔΔG.
3. **One denticity verdict is cutoff-sensitive.** `pb_P0_cplx`'s single galloyl contact at 2.936 Å
   reads MONODENTATE at the Pb cutoff of 3.20 Å and DISSOCIATED at a uniform 2.80 Å. It is bidentate
   under neither. Reported rather than left implicit.
4. **Neither lead aquo ion holds all its waters in the inner sphere.** `pb_aquo6` expels one to
   4.005 Å (five-coordinate first shell); `pb_aquo8` expels two (six-coordinate). A genuine
   limitation, distinct from the CN = 8 one that A33 has been carrying.
5. **Lead's hemidirection is intrinsic to the aqueous ion, not induced by the galloyl pocket** —
   d̃ = 0.4132 in `pb_aquo6`, essentially unchanged in the complexes, while the copper and zinc aquo
   ions are holodirected and all their complex asymmetry is ligand-induced. This constrains what the
   mechanism section may claim.
6. **Ruling "D-08", cited in the session brief, does not exist** in `docs/03_DECISIONS.md`, which
   runs D-01 to D-07. Its substance was followed and the absence was flagged.
7. **S06 has no `ai_use_log.csv` row and no session record**, although it has two commits. Flagged;
   **not reconstructed**, because the assistant was not present in that session and inventing an
   account of it would be exactly the misrepresentation CLAUDE.md §7.1 forbids.

---

## 5. WHAT WAS DELIBERATELY NOT DONE

* **No report prose was written.**
* **No number was adjusted** to improve agreement with the outline or with experiment.
* **The outline's α values were NOT written into `CANONICAL_NUMBERS.yaml`.** The −RT ln α arithmetic
  is reported for the §4.6 comparison, but `ddg_pb_cu_exp_kJ_per_mol` and `ddg_pb_zn_exp_kJ_per_mol`
  stay `PENDING` until α comes from the AAS data (YAML rule 3, CLAUDE.md §3).
* **The Pb–O validation deviation was NOT computed.** It needs a literature value that has cleared
  `verify_dois.py` and been read. No citation was added to `refs/library.bib`.
* **No energy decomposition, no f_orb.** Multiwfn is still not installed; A01 stays OPEN and §4.3's
  pre-committed fallback binds.
* **No counterpoise correction and no ωB97X-D4 cross-check** were run.
* **No structure was re-optimised under a restraint.**

---

## 6. HOW THE OUTPUT WAS VERIFIED

Every gate is a script that exits non-zero on failure, and each was run.

* The **C-01 identity was checked four ways on all seventeen jobs**, not on the two named in the
  brief — including the identity that the thermochemistry block's `E(el)` equals the decomposed
  `FINAL SINGLE POINT ENERGY`, which is the one that is easy to omit and expensive to get wrong.
  Residuals below 1e−9 Eh.
* The **quasi-RRHO claim was read from the output files**, not inferred from the ORCA version.
* **Denticity was measured from the optimised coordinates** with the same cutoffs and the same
  first-shell logic as the pre-screen, both M–O(galloyl) distances individually and never averaged.
* **Cluster compositions were counted from the `.xyz` files** rather than taken from the reaction
  document, which is how the S06 x-value discrepancy was found.
* **Hemidirection was recomputed at a second, uniform cutoff** to confirm no descriptor depends on
  the choice.
* **Standard-state terms were recomputed from R, T and the stated concentrations** and asserted
  against the protocol's printed values, per `REACTIONS.md` §5.2.
* The **canonical-numbers file was re-parsed as YAML** after rewriting, every VERIFIED key checked to
  have both a value and a source file, and `emit_numbers.py` run end to end (129 verified emitted).
* **`make check` run**: FAIL 0, and `check_numbers` reports exactly the nine pre-existing issues in
  `report/sections/`, unchanged.

---

## 7. WHAT NOW NEEDS PALAASH'S RULING

| Ref | Item |
|---|---|
| **D-13 / A34** | How §4.7, §5.3, the abstract and the title's framing present a computational arm that does not reproduce the central ordering claim. |
| **D-12 / A32** | The phenolic pK_a is now load-bearing: it selects between two contradictory computed answers. §1.3's "the three-state design makes the premise unnecessary" no longer holds. |
| **D-11 / A05** | Attack A05's pre-written armour answers a magnitude gap; two of six comparisons disagree in **sign**. §4.6.3 must be rewritten. |
| **D-09** | `DFT_PROTOCOL.md` §2.2 understates the position and must be rewritten — the CN = 8 preference was tested and does not survive. |
| **D-10** | The S06 log entry's x-value framing should be corrected. |
| — | Whether ruling "D-08" exists. |
| — | Whether an S06 log row and session record should be reconstructed **by Palaash**, who was present. |
