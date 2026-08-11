<!-- Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang -->
# ORCA — installation

**Status on this machine: NOT INSTALLED. This is a Phase 7 blocker.**

ORCA is **free for academic use** but is distributed only after **individual registration**, and the
download is behind an authenticated portal. **It cannot be scripted, curl-ed, or automated.** A
human must register and download it. There is no way around this and no point pretending otherwise.

**ORCA must not be redistributed.** It is not committed to this repository, and `vendor/orca/` is
gitignored. The Hetzner provisioning script uploads the tarball you download; it does not fetch it.

---

## What to do

### 1. Register (once, ~5 minutes, then wait for approval)
- Go to **https://orcaforum.kofo.mpg.de/**
- Register for a forum account with an academic or school email address.
- Approval is manual and typically takes anywhere from a few hours to a couple of days.
  **Do this first, today** — the waiting period is the long pole, exactly as with the principal's
  signature.

### 2. Download the correct build
Once approved, the download links are in the forum's Downloads area.

**Download the `Linux_x86-64` shared-library build**, e.g.
`orca_6_x_x_linux_x86-64_shared_openmpi41.tar.xz`.

**Not** the macOS build, and specifically **not** an ARM build. This machine is Apple Silicon
(`arm64`), but **all production calculations run on Hetzner x86-64 Linux instances**, so the Linux
x86-64 build is the one that matters. A local macOS build is optional and useful only for smoke
tests.

Note the **exact version number**. It goes into Table 3.1 of the report and must be cited alongside
Neese's ORCA reference — attack A01 requires the version, not just the name.

### 3. Install locally (optional, for smoke tests only)
```bash
mkdir -p vendor/orca
tar -xf ~/Downloads/orca_6_x_x_*.tar.xz -C vendor/orca --strip-components=1
```
ORCA's parallel execution requires a **matching OpenMPI version** — the one named in the tarball
filename. A mismatched OpenMPI is the single most common ORCA installation failure. Serial runs work
without it.

### 4. Install on Hetzner (where the real work happens)
```bash
bash dft/hetzner/provision.sh          # prepares a fresh Debian/Ubuntu x86-64 instance
bash dft/hetzner/upload_orca.sh ~/Downloads/orca_6_x_x_linux_x86-64_shared_openmpi41.tar.xz
```
See [`../dft/hetzner/`](../dft/hetzner/).

### 5. Put it on PATH
`scripts/env.sh` adds `vendor/orca` to `PATH` and `LD_LIBRARY_PATH` if present. Every other script
sources it.

---

## Verifying the install
```bash
source scripts/env.sh
orca --version          # or: orca | head
which orca              # ORCA needs its FULL PATH to launch parallel jobs
```
ORCA is launched by **absolute path** when running in parallel — `$(which orca) job.inp` — because
the MPI wrapper re-executes it. A bare `orca job.inp` silently runs serial.

---

## What goes in the report

Table 3.1 must state:

| Field | Value |
|---|---|
| Program | ORCA |
| **Version** | the exact `x.y.z` — not "ORCA 6" |
| Citation | Neese, F. *WIREs Comput. Mol. Sci.* — cite the version-appropriate paper; the outline currently has the 2012 reference |
| Parallelism | number of cores, MPI implementation and version |
| Hardware | Hetzner instance type — required by assertion C-023, the compute declaration |

`\TODOPAL{ORCA version actually installed — needed for Table 3.1 and the compute declaration}`
