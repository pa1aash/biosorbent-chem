#!/usr/bin/env python3
"""Generate the production ORCA input files from the locked protocol.

Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang

Single writer of dft/inputs/. Reads every structure in dft/structures/*.xyz and
emits dft/inputs/<jobname>/<jobname>.inp plus dft/inputs/JOB_ORDER.txt.

TWO RULES GOVERN THIS SCRIPT.

1. EVERY level-of-theory setting is transcribed from dft/DFT_PROTOCOL.md and is
   traceable to a named section. Nothing is chosen here. The section reference
   travels into the generated file as a comment so that a reader of the .inp
   never has to take the setting on trust.

2. CHARGE AND MULTIPLICITY ARE READ FROM THE .xyz PROVENANCE HEADER AND ARE
   NEVER INFERRED, DEFAULTED OR RE-DERIVED. A structure whose header is missing
   or unparseable is a hard error that aborts the whole run. This is attack A02:
   if Cu(II) were silently treated closed-shell the entire computational arm
   would be invalid.

Usage
-----
    python dft/make_orca_inputs.py            # write dft/inputs/
    python dft/make_orca_inputs.py --check    # audit only, write nothing
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

DFT = Path(__file__).resolve().parent
STRUCTURES = DFT / "structures"
INPUTS = DFT / "inputs"
REPO = DFT.parent

# ── Resource settings ─────────────────────────────────────────────────────────
# These are hardware settings, not level-of-theory settings. They do not come
# from DFT_PROTOCOL.md and they do not affect any computed quantity.

# Cores per job. The box has 16 vCPU and the queue schedules by TOTAL CORES, so
# the number of concurrent jobs varies with their sizes and the machine stays
# full. ORCA runs one MPI process per core, so total processes never exceeds 16
# and the memory ceiling is MAXCORE x 16 = 24 GB regardless of the mix.
#
# Small species get 4 cores because ORCA's parallel efficiency at 8 cores for
# ~330-basis-function systems is well below linear (typically 55-70%, against
# 80-90% at 4 cores). Four 4-core jobs therefore do appreciably more useful work
# than two 8-core jobs. The complexes keep 8 cores: they have more work per unit
# of communication, and per-job latency matters because the denticity checkpoint
# of protocol §3.7 cannot start until individual complexes finish.
CORES_SMALL = 4
CORES_LARGE = 8

# MAXCORE is ORCA's *per-process* memory ceiling in MB. Read the arithmetic
# before changing it:
#
#     MAXCORE x NPROCS x (concurrent jobs)  =  peak nominal demand
#     1500    x 8      x 2                  =  24 GB
#
# The box reports 30 GiB total and 29 GiB available. 24 GB nominal therefore
# leaves roughly 5 GB of headroom. ORCA is documented to overshoot maxcore in
# some modules (the Hessian in particular), so the nominal figure is a floor on
# the risk rather than a ceiling, and the headroom is not decorative.
#
# 1500 is ORCA's own sizing rule -- about 75% of RAM divided by the total cores
# in use, 29000 x 0.75 / 16 = 1360, rounded up.
#
# The S04 session brief originally specified 3000, which is 3000 x 8 x 2 =
# 48 GB against 29 GB available, a 1.65x overcommit that would put a multi-hour
# job at the mercy of the OOM killer. Raised as a question and RULED DOWN TO
# 1500 by Palaash on 2026-08-13 before launch. Recorded in JOB_QUEUE_STATUS.md.
MAXCORE = 1500

# ── Geometry-optimiser iteration cap ─────────────────────────────────────────
# ORCA's DEFAULT cap is 3 x N_atoms, which is 102 for a 34-atom complex. In S04
# pb_P0_cplx hit exactly that cap, stopped without converging, NEVER RAN THE
# FREQUENCY CALCULATION, and still printed "ORCA TERMINATED NORMALLY" -- three
# hours of compute that produced no usable free energy. cu_P0_cplx converged at
# 88 of the same 102, so the margin was one job wide.
#
# This is a RESOURCE CAP, not a convergence criterion. It does not change the
# level of theory, the stationary point sought, or the TightOPT thresholds fixed
# by DFT_PROTOCOL.md §3.4 -- it only governs how long the optimiser is allowed
# to look for the same minimum. Set uniformly so that no species is treated
# differently from another (the comparison across metals depends on that).
MAXITER = 300

# ── Inputs frozen at their S04 form ──────────────────────────────────────────
# These jobs COMPLETED under S04 inputs that had no %geom block. Their .inp is
# the provenance of a finished calculation, so it must keep reproducing exactly
# what ran. Both converged far inside the default cap (water 4 cycles,
# cu_P0_cplx 88 of 102), so MAXITER could not have altered either result.
FROZEN_AT_S04 = {"water", "cu_P0_cplx"}

# ── Jobs restarting from a previous optimisation ─────────────────────────────
# pb_P0_cplx is re-run from the last geometry of its S04 attempt rather than
# from the S02 conformer. That attempt did 102 optimisation cycles and left the
# energy converged to ~5e-5 Eh; discarding it and starting over would repeat
# three hours of work for a worse starting point. This is a continuation of the
# same optimisation trajectory at the same level of theory, and the chain is
# recorded in the generated file's header.
RESTART_FROM = {
    "pb_P0_cplx": DFT / "outputs" / "pb_P0_cplx" / "pb_P0_cplx.xyz",
}

# ── Level of theory — every line traceable to DFT_PROTOCOL.md ────────────────

PROTOCOL = [
    # (label,                value,                     protocol section)
    ("Functional",           "PBE0 (25% exact exchange)",              "§3 'Functional'"),
    ("Dispersion",           "D3(BJ) — D3 with Becke–Johnson damping", "§3 'Dispersion'"),
    ("Basis, all elements",  "def2-TZVP",                              "§3.1"),
    ("Pb core treatment",    "def2-ECP = Stuttgart–Cologne ECP60MDF, "
                             "60 core electrons, 22 in valence",       "§3.1"),
    ("Cu, Zn, C, H, O",      "all-electron",                           "§3.1"),
    ("Auxiliary basis",      "def2/J",                                 "§3.1, §3.4"),
    ("Acceleration",         "RIJCOSX",                                "§3.4"),
    ("Solvation",            "SMD, solvent = water, applied during "
                             "the optimisation",                       "§3.3"),
    ("Geometry convergence", "TightOPT",                               "§3.4"),
    ("SCF convergence",      "TightSCF",                               "§3.4"),
    ("Integration grid",     "DefGrid3",                               "§3.4"),
    ("Frequencies",          "analytic, same level, same solvent",     "§3.4"),
    ("Opt+freq",             "one combined job per species (17 total)", "§8"),
]

# The ORCA keyword lines. Assembled from the table above and from nowhere else.
KEYWORDS_MAIN = "PBE0 D3BJ def2-TZVP def2/J RIJCOSX TightSCF DefGrid3"
KEYWORDS_RUN = "Opt Freq TightOPT"

# ── Queue order ───────────────────────────────────────────────────────────────
# ORDERED BY DEPENDENCY, revised 2026-08-14 (S05).
#
# The S04 order was longest-processing-time-first, which minimises the makespan
# tail but starts with the jobs whose results nothing else needs. That was the
# wrong objective. EVERY reaction free energy needs the three aquo ions and the
# ligand at its protonation state (REACTIONS.md §2), so those six small, fast
# species gate every downstream quantity. They run first.
#
# Group 1 also has a diagnostic value the old order did not: six species that
# each finish in an hour or two give six independent confirmations that the
# protocol behaves, long before a five-hour complex would.
#
# (jobname, cores, group, note)
JOB_SPEC = [
    # ── ALREADY COMPLETE (S04). Kept in the list so it stays a full inventory
    #    of all seventeen species; the launcher skips them on the normal-
    #    termination banner. Their core counts record what ACTUALLY ran.
    ("water",       CORES_LARGE, 0, "COMPLETE S04 — 15 s, 4 cycles, freq done"),
    ("cu_P0_cplx",  CORES_LARGE, 0, "COMPLETE S04 — 4h37m, 88 cycles, freq done"),

    # ── Group 1: gate everything downstream. Small and fast.
    ("cu_aquo6",    CORES_SMALL, 1, "19 atoms, UKS — reactant in all 3 Cu reactions"),
    ("pb_aquo6",    CORES_SMALL, 1, "19 atoms — headline Pb reference state"),
    ("zn_aquo6",    CORES_SMALL, 1, "19 atoms — reactant in all 3 Zn reactions"),
    ("lig_P0_LH2",  CORES_SMALL, 1, "21 atoms — reactant in all 3 P0 reactions"),
    ("lig_P1_LH1m", CORES_SMALL, 1, "20 atoms — reactant in all 3 P1 reactions"),
    ("lig_P2_L2m",  CORES_SMALL, 1, "19 atoms — reactant in all 3 P2 reactions"),

    # ── Group 2: completes the P0 set. Cu P0 is done; Pb P0 is NOT -- its S04
    #    run hit the optimiser cap and produced no frequencies, so it is re-run
    #    here from its own last geometry. It sits AFTER group 1 because it is a
    #    complex and gates nothing downstream, and because at 8 cores it would
    #    otherwise occupy half the machine ahead of the jobs that do.
    ("pb_P0_cplx",  CORES_LARGE, 2, "34 atoms — RE-RUN from S04 geometry, S04 attempt hit MaxIter"),
    ("zn_P0_cplx",  CORES_LARGE, 2, "34 atoms — last P0 complex"),

    # ── Group 3: the P1 row, complete.
    ("cu_P1_cplx",  CORES_LARGE, 3, "33 atoms, UKS"),
    ("pb_P1_cplx",  CORES_LARGE, 3, "33 atoms, ECP60MDF"),
    ("zn_P1_cplx",  CORES_LARGE, 3, "33 atoms"),

    # ── Group 4: the P2 row, complete.
    ("cu_P2_cplx",  CORES_LARGE, 4, "32 atoms, UKS"),
    ("pb_P2_cplx",  CORES_LARGE, 4, "32 atoms, ECP60MDF"),
    ("zn_P2_cplx",  CORES_LARGE, 4, "32 atoms"),

    # ── Group 5: not a headline quantity. Lowest priority, and the first thing
    #    to drop if the schedule slips (REACTIONS.md §3.1).
    ("pb_aquo8",    CORES_SMALL, 5, "25 atoms — limitations discussion and §6 validation only"),
]

JOB_ORDER = [j for j, _c, _g, _n in JOB_SPEC]
JOB_CORES = {j: c for j, c, _g, _n in JOB_SPEC}
TOTAL_CORES = 16


# ── Structure reading ─────────────────────────────────────────────────────────


class HeaderError(RuntimeError):
    """Raised when a .xyz provenance header is missing or unparseable."""


def parse_structure(path: Path) -> dict:
    """Read one .xyz and return its provenance header plus its coordinates.

    Raises HeaderError rather than supplying any default. There is no default
    charge and no default multiplicity in this project.
    """
    lines = path.read_text().splitlines()
    if len(lines) < 3:
        raise HeaderError(f"{path.name}: fewer than three lines")

    try:
        natoms = int(lines[0].strip())
    except ValueError as exc:
        raise HeaderError(f"{path.name}: line 1 is not an atom count") from exc

    header = {}
    for field in lines[1].split("|"):
        if "=" not in field:
            continue
        key, _, value = field.partition("=")
        header[key.strip()] = value.strip()

    for required in ("charge", "mult", "uhf", "uks", "species"):
        if required not in header:
            raise HeaderError(
                f"{path.name}: provenance header has no '{required}' field. "
                "Charge and multiplicity are never inferred (attack A02)."
            )

    try:
        charge = int(header["charge"])
        mult = int(header["mult"])
        uhf = int(header["uhf"])
    except ValueError as exc:
        raise HeaderError(f"{path.name}: charge/mult/uhf not integer-valued") from exc

    uks_raw = header["uks"].lower()
    if uks_raw not in ("true", "false"):
        raise HeaderError(f"{path.name}: uks={header['uks']!r} is not true/false")
    uks = uks_raw == "true"

    # Internal consistency of the header itself. These are not re-derivations of
    # charge or multiplicity; they check that the header does not contradict
    # itself, which would mean the file cannot be trusted at all.
    if mult != uhf + 1:
        raise HeaderError(
            f"{path.name}: mult={mult} and uhf={uhf} are inconsistent "
            f"(expected mult = uhf + 1)"
        )
    if uks != (mult > 1):
        raise HeaderError(
            f"{path.name}: uks={uks} contradicts mult={mult}"
        )

    coords = [ln.rstrip() for ln in lines[2 : 2 + natoms] if ln.strip()]
    if len(coords) != natoms:
        raise HeaderError(
            f"{path.name}: header declares {natoms} atoms, found {len(coords)}"
        )

    elements = {ln.split()[0] for ln in coords}

    return {
        "jobname": path.stem,
        "path": path,
        "natoms": natoms,
        "charge": charge,
        "mult": mult,
        "uhf": uhf,
        "uks": uks,
        "elements": elements,
        "coords": coords,
        "header": header,
    }


# ── Input-file rendering ──────────────────────────────────────────────────────


def render_input(s: dict) -> str:
    job = s["jobname"]
    h = s["header"]
    has_pb = "Pb" in s["elements"]
    spin_kw = "UKS" if s["uks"] else "RKS"
    nprocs = JOB_CORES[job]

    w = []
    a = w.append

    a("# " + "=" * 76)
    a("# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang")
    a("#")
    a("# PRODUCTION ORCA INPUT -- GENERATED FILE, DO NOT EDIT BY HAND.")
    a("# Regenerate with:  python dft/make_orca_inputs.py")
    a("#")
    a(f"# Job            {job}")
    a(f"# Species        {h.get('label', '(no label in header)')}")
    a(f"# Formula        {h.get('formula', '(no formula in header)')}")
    a(f"# Role           {h.get('role', '?')}"
      f" | protonation {h.get('protonation', '?')}"
      f" | metal {h.get('metal', '?')}")
    if h.get("role_note"):
        a("#")
        a("# ROLE NOTE")
        for chunk in _wrap(h["role_note"], 70):
            a(f"#   {chunk}")
    a("#")
    a("# GEOMETRY SOURCE")
    if job in RESTART_FROM:
        a(f"#   dft/outputs/{job}/{job}.xyz  -- RESTART")
        a("#   This is the LAST GEOMETRY of the S04 optimisation attempt, not the")
        a("#   S02 conformer. That attempt ran 102 cycles, reached ORCA's default")
        a("#   iteration cap without satisfying TightOPT, and therefore never ran")
        a("#   its frequency calculation. The energy was converged to ~5e-5 Eh but")
        a("#   the step criterion was still oscillating on a flat dihedral plateau.")
        a("#   This run CONTINUES that trajectory at the same level of theory with")
        a("#   a raised iteration cap. Provenance chain:")
        a("#     S02 conformer screen -> dft/structures/pb_P0_cplx.xyz")
        a("#       -> S04 partial optimisation (102 cycles, not converged)")
        a("#       -> dft/outputs/pb_P0_cplx/pb_P0_cplx.xyz -> this job")
    else:
        a(f"#   dft/structures/{job}.xyz")
        a("#   The lowest-energy conformer retained by the S02 conformer screen,")
        a("#   pre-optimised at GFN2-xTB/ALPB(water). The pre-screen energy is NOT a")
        a("#   report quantity; this geometry is a starting point only and is")
        a("#   re-optimised in full below.")
    a("#")
    a("# LEVEL OF THEORY -- every setting fixed by dft/DFT_PROTOCOL.md.")
    for label, value, section in PROTOCOL:
        first, *rest = _wrap(f"{value}", 44) or [""]
        a(f"#   {label:<20} {first:<46}{section}")
        for chunk in rest:
            a(f"#   {'':<20} {chunk}")
    a("#")
    a("# THERMOCHEMISTRY")
    a("#   Protocol §3.4 fixes 298.15 K, 1 atm, RRHO with Grimme's quasi-RRHO")
    a("#   treatment of modes below 100 cm-1. That treatment is applied in")
    a("#   post-processing by analysis/thermo.py from the frequency list printed")
    a("#   below, per REACTIONS.md §5.1, NOT by an ORCA keyword -- so that ORCA's")
    a("#   own default entropy treatment cannot be silently double-counted.")
    a("#")
    a("# CHARGE AND MULTIPLICITY")
    a("#   Read verbatim from the .xyz provenance header written in S02. Never")
    a("#   inferred, never defaulted. Attack A02, rated CRITICAL.")
    a(f"#     charge = {s['charge']:+d}   multiplicity = {s['mult']}   "
      f"unpaired electrons = {s['uhf']}   {spin_kw}")
    if s["uks"]:
        a("#   OPEN-SHELL DOUBLET. <S^2> is reported for this species with its")
        a("#   deviation from the ideal 0.750 stated (protocol §3.2).")
    a("# " + "=" * 76)
    a("")
    a(f"%pal nprocs {nprocs} end")
    a(f"%maxcore {MAXCORE}")
    a("")
    a(f"! {KEYWORDS_MAIN} {spin_kw}")
    a(f"! {KEYWORDS_RUN}")
    a("")

    if has_pb:
        a("# Pb: def2-TZVP carries the def2-ECP automatically, but the ECP is")
        a("# declared explicitly here so that the relativistic treatment is")
        a("# visible in the input file itself and not only in the output.")
        a("# def2-ECP for Pb IS the Stuttgart-Cologne ECP60MDF: 60 core")
        a("# electrons replaced, 22 electrons in the valence space, scalar-")
        a("# relativistic effects entering through the ECP parameterisation.")
        a("# Protocol §3.1 -- attack A03, rated CRITICAL.")
        a("%basis")
        a('  NewGTO Pb "def2-TZVP" end')
        a('  NewECP Pb "def2-ECP"  end')
        a("end")
        a("")

    if job not in FROZEN_AT_S04:
        a("# Geometry-optimiser iteration cap. ORCA's default is 3 x N_atoms")
        a(f"# ({3 * s['natoms']} here). In S04 pb_P0_cplx hit that default, stopped without")
        a("# converging, and never ran its frequency calculation -- while still")
        a("# printing a normal-termination banner. This is a resource cap only:")
        a("# it does not alter the TightOPT thresholds of protocol §3.4.")
        a("%geom")
        a(f"  MaxIter {MAXITER}")
        a("end")
        a("")
    a("# SMD, water. Geometries are optimised IN SOLUTION -- never optimised in")
    a("# gas phase and single-pointed in solvent. Protocol §3.3.")
    a("%cpcm")
    a("  smd        true")
    a('  SMDsolvent "water"')
    a("end")
    a("")
    a(f"* xyz {s['charge']} {s['mult']}")
    for line in s["coords"]:
        parts = line.split()
        a("  {:<3s} {:>16s} {:>16s} {:>16s}".format(*parts[:4]))
    a("*")
    a("")
    return "\n".join(w)


def _wrap(text: str, width: int) -> list[str]:
    out, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        out.append(cur)
    return out


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="audit only; write nothing")
    args = ap.parse_args()

    xyz_files = sorted(STRUCTURES.glob("*.xyz"))
    if not xyz_files:
        print(f"ERROR: no .xyz files in {STRUCTURES}", file=sys.stderr)
        return 1

    structures, errors = {}, []
    for path in xyz_files:
        try:
            s = parse_structure(path)
        except HeaderError as exc:
            errors.append(str(exc))
            continue
        structures[s["jobname"]] = s

    if errors:
        print("HEADER ERRORS -- no input file is written for these species:",
              file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    missing = [j for j in JOB_ORDER if j not in structures]
    extra = [j for j in structures if j not in JOB_ORDER]
    if missing or extra:
        print("JOB_ORDER does not match dft/structures/:", file=sys.stderr)
        for j in missing:
            print(f"  in JOB_ORDER but no structure: {j}", file=sys.stderr)
        for j in extra:
            print(f"  structure present but not queued: {j}", file=sys.stderr)
        return 1

    # Substitute restart geometries. Charge and multiplicity still come from the
    # S02 provenance header -- only the coordinates change.
    for job, geom in RESTART_FROM.items():
        if job not in structures:
            continue
        if not geom.exists():
            print(f"ERROR: restart geometry {geom} missing for {job}", file=sys.stderr)
            return 1
        gl = geom.read_text().splitlines()
        n = int(gl[0].strip())
        if n != structures[job]["natoms"]:
            print(f"ERROR: {geom} has {n} atoms, {job} expects "
                  f"{structures[job]['natoms']}", file=sys.stderr)
            return 1
        structures[job]["coords"] = [ln.rstrip() for ln in gl[2:2 + n] if ln.strip()]

    if not args.check:
        for job in JOB_ORDER:
            d = INPUTS / job
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            (d / f"{job}.inp").write_text(render_input(structures[job]))

        groups = {
            0: "ALREADY COMPLETE (S04) -- opt converged AND frequencies ran",
            1: "gate everything downstream: aquo ions + ligands, small and fast",
            2: "completes the P0 set -- pb_P0_cplx is a RE-RUN, see JOB_SPEC",
            3: "the P1 row",
            4: "the P2 row",
            5: "not a headline quantity -- drop first if the schedule slips",
        }
        lines = [
            "# Chem-151 | queue order consumed by run_queue.sh",
            "# FORMAT: <jobname> <cores>   -- the launcher schedules by TOTAL CORES",
            f"# Total cores available: {TOTAL_CORES}. ORCA runs one MPI process per",
            "# core, so total processes never exceeds that and peak memory is",
            "# maxcore x cores. Ordered BY DEPENDENCY, not by size -- see",
            "# make_orca_inputs.py JOB_SPEC for the reasoning.",
        ]
        last = None
        for j, c, g, note in JOB_SPEC:
            if g != last:
                lines.append("")
                lines.append(f"# -- group {g}: {groups[g]}")
                last = g
            lines.append(f"{j:<14s} {c}    # {note}")
        (INPUTS / "JOB_ORDER.txt").write_text("\n".join(lines) + "\n")

    # ── Self-audit table ─────────────────────────────────────────────────────
    hdr = ("jobname", "charge", "mult", "UKS", "atoms", "nprocs",
           "functional", "basis", "Pb ECP")
    rows = []
    for job in JOB_ORDER:
        s = structures[job]
        has_pb = "Pb" in s["elements"]
        rows.append((
            job,
            f"{s['charge']:+d}",
            str(s["mult"]),
            "yes" if s["uks"] else "no",
            str(s["natoms"]),
            str(JOB_CORES[job]),
            "PBE0-D3BJ",
            "def2-TZVP",
            "ECP60MDF" if has_pb else "n/a (no Pb)",
        ))

    widths = [max(len(str(r[i])) for r in (hdr, *rows)) for i in range(len(hdr))]
    line = "  ".join("-" * w for w in widths)
    print("  ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    print(line)
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))
    print(line)
    peak = MAXCORE * TOTAL_CORES / 1000
    print(f"{len(rows)} jobs | 16 headline + 1 alternative (pb_aquo8)")
    print(f"scheduling: by total cores, cap {TOTAL_CORES} | maxcore {MAXCORE} MB/process"
          f" | peak nominal memory {peak:.0f} GB")

    blanks = [r[0] for r in rows if any(str(c).strip() in ("", "?") for c in r)]
    if blanks:
        print(f"\nBLANK OR PLACEHOLDER CELLS -- these jobs must not launch: "
              f"{', '.join(blanks)}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
