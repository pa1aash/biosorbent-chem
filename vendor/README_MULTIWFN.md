<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# Multiwfn — installation

**Status on this machine: NOT INSTALLED. This is a Phase 7 blocker, alongside ORCA.**

Multiwfn is **free**, but the binary is distributed from the author's own site behind a short
registration form. Like ORCA, **it cannot be scripted** — a human must download it. It is not
committed here and `vendor/multiwfn/` is gitignored.

**Why it matters:** with ADF/AMS unavailable (see [`README_EDA.md`](README_EDA.md)), Multiwfn is the
realistic route to a **charge-decomposition and orbital-interaction analysis of ORCA output**. It is
the tool that makes the §4.7 falsification argument computable at all. Without it the report has
ΔG_bind values but no decomposition, and Finding 5 — the intellectual centrepiece — has no evidence.

---

## What to do

1. Go to **http://sobereva.com/multiwfn/** (Tian Lu, Beijing Kein Research Center).
2. Complete the short download form and download the **Linux binary** package
   (`Multiwfn_x.x_bin_Linux*.zip`) for the Hetzner instances, and optionally the macOS binary for
   local work. Note that the macOS build is **x86-64**; on this Apple Silicon machine it runs under
   Rosetta 2, which is fine for inspection but slow.
3. Unpack:
   ```bash
   mkdir -p vendor/multiwfn
   unzip ~/Downloads/Multiwfn_*.zip -d vendor/multiwfn
   chmod +x vendor/multiwfn/Multiwfn
   ```
4. `scripts/env.sh` puts it on `PATH` and exports `Multiwfnpath` if `settings.ini` is present.
   Multiwfn needs `Multiwfnpath` set to find its `settings.ini`; without it, defaults silently
   differ from what you configured.
5. **Note the exact version.** It goes into Table 3.1 and is cited alongside Lu & Chen,
   *J. Comput. Chem.* **2012**, *33*, 580–592.

---

## Feeding it from ORCA

Multiwfn reads **`.molden`** files. ORCA writes `.gbw`, which must be converted:

```bash
orca_2mkl basename -molden          # produces basename.molden.input
mv basename.molden.input basename.molden
Multiwfn basename.molden
```

`orca_2mkl` ships with ORCA. For an open-shell species — **Cu(II) is d⁹, doublet** — check that the
alpha and beta orbital sets are both carried through; a decomposition performed on a restricted
reading of an unrestricted wavefunction is silently wrong, and is exactly the kind of thing attack
A02 probes.

---

## What it can and cannot give

| Wanted | Multiwfn | Honest name for it |
|---|---|---|
| Charge transfer between fragments | **Yes** — charge decomposition analysis (CDA) | "Charge decomposition analysis (CDA) as implemented in Multiwfn x.x" |
| Orbital-interaction inspection | **Yes** — orbital composition, fragment orbital analysis | name the specific module used |
| Deformation-density-like visualisation | **Yes** — density difference between the complex and prepared fragments | **"density difference" or "deformation density"**, *not* "NOCV deformation density channels" unless NOCV orbitals were actually generated |
| **True ETS partition into ΔE_Pauli / ΔE_elstat / ΔE_orb** | **No** | ETS is ADF's. Do not claim it. |
| **ETS-NOCV channel decomposition with eigenvalues** | **No** | Do not claim it. |

**Read [`README_EDA.md`](README_EDA.md) before writing §3.4 or §4.7.** The scheme actually used must
be named exactly, in Table 3.1, with the program and its version — attack **A01**, rated 🔴 CRITICAL.
Whatever this project ends up running, the report calls it by its real name.

`\TODOPAL{Multiwfn version actually installed — needed for Table 3.1}`
