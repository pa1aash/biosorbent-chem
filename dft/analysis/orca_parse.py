#!/usr/bin/env python3
"""Single-source ORCA 6.1.1 output parser for the computational arm.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

Every downstream consumer -- the integrity gate, the denticity checkpoint, the
thermochemistry assembly, the hemidirection descriptors -- reads its numbers
through this module, so that no two of them can disagree about what a given
output file says.

WHY A HAND-WRITTEN PARSER.  cclib 1.8.1 does not parse ORCA 6.1.1 output; it
aborts in the SCF convergence block.  The DFT_PROTOCOL.md §3.4 all-real-frequency
gate must not depend on a parser that fails silently, so the frequency table,
the thermochemistry block and the SMD energy decomposition are all read from
ORCA's own printed text.

EVERY QUANTITY IS TAKEN FROM THE LAST OCCURRENCE IN THE FILE.  An optimisation
prints one SCF summary per cycle; only the final one describes the converged
structure, and the frequency job's own single point is the one the
thermochemistry block refers to.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

DFT = Path(__file__).resolve().parent.parent
OUTPUTS = DFT / "outputs"

# Constants, not measurements.  REACTIONS.md §5.4.
HARTREE_KJ = 2625.499639
KCAL_KJ = 4.184
KCAL_HARTREE = KCAL_KJ / HARTREE_KJ

# The seventeen production jobs.  The pb_*_atom82.out files are ORCA's atomic
# reference calculations for the ECP element and are NOT jobs; they are cited as
# machine evidence for attack A03 and never parsed as species.
JOBS = [
    "water",
    "lig_P0_LH2", "lig_P1_LH1m", "lig_P2_L2m",
    "pb_aquo6", "pb_aquo8", "cu_aquo6", "zn_aquo6",
    "pb_P0_cplx", "pb_P1_cplx", "pb_P2_cplx",
    "cu_P0_cplx", "cu_P1_cplx", "cu_P2_cplx",
    "zn_P0_cplx", "zn_P1_cplx", "zn_P2_cplx",
]

OPEN_SHELL = {"cu_aquo6", "cu_P0_cplx", "cu_P1_cplx", "cu_P2_cplx"}


def _last_float(pattern: str, text: str) -> float | None:
    """Value from the LAST match of a single-capture-group pattern."""
    hits = re.findall(pattern, text, re.M)
    return float(hits[-1]) if hits else None


@dataclass
class Job:
    """One parsed ORCA output."""

    name: str
    path: Path
    text: str = field(repr=False)

    # --- termination and optimisation -------------------------------------
    terminated: bool = False
    opt_converged: bool = False
    n_cycles: int = 0
    n_atoms: int | None = None
    charge: int | None = None
    mult: int | None = None

    # --- energies, all Hartree --------------------------------------------
    e_scf_smd: float | None = None          # after final integration, incl. CPCM dielectric
    g_cds: float | None = None              # SMD cavity-dispersion-solvent-structure
    e_after_cds: float | None = None
    e_disp: float | None = None             # D3(BJ)
    e_final: float | None = None            # FINAL SINGLE POINT ENERGY

    # --- thermochemistry, all Hartree -------------------------------------
    thermo_e_el: float | None = None        # electronic energy as used by the thermo block
    zpe: float | None = None
    thermal_corr: float | None = None       # U(T) - U(0), excludes ZPE
    enthalpy: float | None = None
    entropy_term: float | None = None       # T*S, positive
    gibbs: float | None = None              # ORCA "Final Gibbs free energy"
    g_minus_eel: float | None = None        # ORCA "G-E(el)": the thermal correction to G
    quasi_rrho: bool | None = None
    qrrho_ref_freq: float | None = None
    thermo_cutoff: float | None = None

    # --- vibrations --------------------------------------------------------
    has_freq: bool = False
    has_hess: bool = False
    freqs: np.ndarray | None = field(default=None, repr=False)
    n_imag: int | None = None
    imag_values: list[float] = field(default_factory=list)
    lowest_real: float | None = None

    # --- open shell --------------------------------------------------------
    s2: float | None = None

    @property
    def complete(self) -> bool:
        """The three-part completion test ruled in S05.

        A normal-termination banner alone is not a completion test: ORCA prints
        it even when the optimiser exhausts its cycle cap and no frequency
        calculation ever runs.
        """
        return bool(self.terminated and self.has_freq and self.has_hess
                    and self.opt_converged)

    @property
    def n_low_modes(self) -> int | None:
        """Real modes below the 100 cm-1 quasi-RRHO reference frequency."""
        if self.freqs is None:
            return None
        real = self.freqs[self.freqs > 1.0]
        return int((real < 100.0).sum())

    @property
    def s2_deviation_pct(self) -> float | None:
        return None if self.s2 is None else (self.s2 - 0.750) / 0.750 * 100.0


def parse(name: str, outputs: Path = OUTPUTS) -> Job:
    d = outputs / name
    out = d / f"{name}.out"
    if not out.exists():
        raise FileNotFoundError(out)
    txt = out.read_text(errors="replace")

    j = Job(name=name, path=out, text=txt)
    j.terminated = "ORCA TERMINATED NORMALLY" in txt
    j.opt_converged = "THE OPTIMIZATION HAS CONVERGED" in txt
    j.n_cycles = txt.count("GEOMETRY OPTIMIZATION CYCLE")
    j.has_hess = (d / f"{name}.hess").exists()

    n = _last_float(r"Number of atoms\s+\.+\s+(\d+)", txt)
    j.n_atoms = int(n) if n is not None else None
    c = _last_float(r"Total Charge\s+Charge\s+\.+\s+(-?\d+)", txt)
    j.charge = int(c) if c is not None else None
    m = _last_float(r"Multiplicity\s+Mult\s+\.+\s+(\d+)", txt)
    j.mult = int(m) if m is not None else None

    # --- SMD / dispersion energy decomposition -----------------------------
    j.e_scf_smd = _last_float(
        r"Total energy after final integration\s*:\s*(-?\d+\.\d+)", txt)
    # High-precision Gcds from the TOTAL SCF ENERGY components table.
    j.g_cds = _last_float(r"SMD CDS \(Gcds\)\s*:\s*(-?\d+\.\d+)", txt)
    j.e_after_cds = _last_float(
        r"Total Energy after SMD CDS correction =\s*(-?\d+\.\d+)", txt)
    j.e_disp = _last_float(r"^Dispersion correction\s+(-?\d+\.\d+)\s*$", txt)
    j.e_final = _last_float(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", txt)

    # --- thermochemistry ----------------------------------------------------
    if "THERMOCHEMISTRY AT" in txt:
        block = txt.rsplit("THERMOCHEMISTRY AT", 1)[1]
        j.quasi_rrho = re.search(r"Quasi RRHO\s*\.+\s*(\w+)", block) is not None and \
            re.search(r"Quasi RRHO\s*\.+\s*(\w+)", block).group(1).lower() == "true"
        j.thermo_cutoff = _last_float(r"Cut-Off Frequency\s*\.+\s*(-?\d+\.\d+)", block)
        rf = re.search(r"reference frequency of\s*(\d+\.?\d*)\s*cm-1", block)
        j.qrrho_ref_freq = float(rf.group(1)) if rf else None
        j.thermo_e_el = _last_float(r"Electronic energy\s*\.+\s*(-?\d+\.\d+)", block)
        j.zpe = _last_float(r"Zero point energy\s*\.+\s*(-?\d+\.\d+)", block)
        j.thermal_corr = _last_float(
            r"Total thermal correction\s*(-?\d+\.\d+)", block)
        j.enthalpy = _last_float(r"Total Enthalpy\s*\.+\s*(-?\d+\.\d+)", block)
        j.entropy_term = _last_float(r"Final entropy term\s*\.+\s*(-?\d+\.\d+)", block)
        j.gibbs = _last_float(r"Final Gibbs free energy\s*\.+\s*(-?\d+\.\d+)", block)
        j.g_minus_eel = _last_float(r"G-E\(el\)\s*\.+\s*(-?\d+\.\d+)", block)

    # --- vibrational frequencies -------------------------------------------
    if "VIBRATIONAL FREQUENCIES" in txt:
        j.has_freq = True
        vb = txt.rsplit("VIBRATIONAL FREQUENCIES", 1)[1].split("NORMAL MODES", 1)[0]
        vals = [float(x) for x in
                re.findall(r"^\s*\d+:\s+(-?\d+\.\d+)\s*cm\*\*-1", vb, re.M)]
        if vals:
            arr = np.asarray(vals, dtype=float)
            j.freqs = arr
            # The six translations and rotations of a non-linear molecule are
            # printed as 0.00.  Only a genuinely NEGATIVE value is imaginary.
            j.n_imag = int((arr < -1e-6).sum())
            j.imag_values = [float(x) for x in arr[arr < -1e-6]]
            real = arr[arr > 1.0]
            j.lowest_real = float(real.min()) if real.size else None

    # --- <S^2> --------------------------------------------------------------
    j.s2 = _last_float(r"Expectation value of <S\*\*2>\s*:\s*(-?\d+\.\d+)", txt)

    return j


def parse_all(jobs: list[str] | None = None, outputs: Path = OUTPUTS) -> dict[str, Job]:
    return {n: parse(n, outputs) for n in (jobs or JOBS)}


if __name__ == "__main__":  # pragma: no cover
    for n, j in parse_all().items():
        print(f"{n:14s} complete={j.complete} imag={j.n_imag} "
              f"S2={j.s2} G={j.gibbs}")
