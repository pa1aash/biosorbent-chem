<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# Energy decomposition analysis — what we may and may not call it

**This is attack A01, rated 🔴 CRITICAL, and the most likely single kill shot from a computational
referee.** Read this before writing one word of §3.4 or §4.7.

---

## The plain statement

**ETS-NOCV is a method of the ADF / AMS program (SCM, Amsterdam).** It is the Extended Transition
State scheme of Ziegler and Rauk combined with Natural Orbitals for Chemical Valence, as developed
by Mitoraj, Michalak and Ziegler, and it is implemented there.

**ORCA does not implement ETS-NOCV.**

Therefore: **unless ADF/AMS actually produces the numbers, the report must NOT describe the analysis
as "ETS-NOCV".** Writing "ORCA" and "ETS-NOCV" in the same breath, without explanation, is the kind
of error that ends a computational referee's confidence in the entire paper — and it cannot be
recovered by arguing that the schemes are similar, because the referee's objection is not about
similarity, it is about whether the author knows what they ran.

The Stage-1 outline reports `f_orb = 0.38` from "Energy-decomposition analysis (EDA)" and a "NOCV"
analysis. **Nothing has been computed.** There is no output file behind those numbers. Because we
are computing from scratch, we are free to choose a scheme we can name honestly — and we name it.

---

## Availability, honestly stated

| Software | Scheme | Licence | Status here |
|---|---|---|---|
| **ADF / AMS** (SCM) | **ETS-NOCV** — the genuine article | **Commercial.** Free academic trials exist but require institutional application and are not obtainable in this project's timeframe. | **NOT AVAILABLE.** Do not claim ETS-NOCV. |
| **ORCA** | LED (for DLPNO-CCSD(T)); interfaces to external analysers | Free for academic use, registration required | See `README_ORCA.md`. Available with manual action. |
| **Multiwfn** | Charge decomposition analysis (CDA); orbital-interaction analysis; EDA-type partitioning of ORCA output | Free binary | See `README_MULTIWFN.md`. The realistic route. |
| **PySCF** | Programmatic access; can be scripted for energy partitioning | Free, open source, pip/conda | Installed as cross-check and fallback. |

---

## The rule this project follows

1. **Name the software, its exact version, and the exact decomposition scheme, in Table 3.1 and in
   §3.4.** Not "EDA". Not "energy decomposition analysis". The name of the scheme and the name and
   version of the program that produced it.
2. **If the scheme is not ETS-NOCV, do not call it ETS-NOCV.** Call it what it is.
3. **If the analysis is a charge-decomposition or orbital-interaction analysis rather than a true
   ETS partition, say so**, and state what the terms mean in that scheme.
4. **Define f_orb explicitly** as f_orb = ΔE_orb / (ΔE_elstat + ΔE_orb), and state in the report that
   this is **a ratio of decomposition terms and is scheme-dependent** — internally comparable across
   the three metals under identical settings, but **not** directly transferable to values from other
   studies using other schemes. Saying this is a rigour signal and it closes attack A13 at the same
   time.
5. **Define the fragmentation** used: metal fragment versus ligand fragment, with the charge and spin
   state of each fragment stated.

---

## Why this does not weaken the argument

The falsification argument at the centre of this report is:

> Electrostatic stabilisation is largest for the most compact, hardest ion. A purely electrostatic
> model therefore predicts the wrong selectivity order. The orbital-interaction fraction is largest
> for Pb. Selectivity is therefore not a charge-density effect.

**That argument needs an internally consistent partition of the interaction energy into
electrostatic and orbital components across three metals computed at an identical level of theory.
It does not need ETS specifically.** Any defensible scheme, honestly named and consistently applied,
supports it — provided the report is explicit that the comparison is internal.

A report that names a modest scheme accurately is far stronger than one that names a prestigious
scheme it did not run. The first is rigour; the second is an integrity finding.

---

## Decision record

The scheme actually chosen, and the reasoning, is recorded in
[`../dft/DFT_PROTOCOL.md`](../dft/DFT_PROTOCOL.md) §Decomposition, and becomes Table 3.1 of the
report verbatim. Until that decision is made and a calculation has run, attack **A01** stays `OPEN`
in [`../docs/01_ATTACK_REGISTER.md`](../docs/01_ATTACK_REGISTER.md) and every decomposition number in
the report is a `\PENDING` marker.
