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

NPROCS = 8  # 16 vCPU box, 2 concurrent jobs -> 8 cores each

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
# Longest-processing-time-first, which minimises the makespan tail on a
# depth-limited queue, with two deliberate departures:
#
#   * water runs FIRST. It is trivially cheap and it exercises every element of
#     the production keyword line end to end, so a syntax or environment fault
#     surfaces in seconds rather than after a multi-hour complex has died.
#   * pb_aquo8 runs LAST. It is the limitations-discussion alternative and half
#     of the §6 Pb-O validation, not a headline quantity (REACTIONS.md §3.1).
#     Placed last it can never delay a headline job on a depth-2 queue.

JOB_ORDER = [
    "water",         # cheap end-to-end validation of the production input
    "cu_P0_cplx",    # 34 atoms, UKS d9, and the species whose denticity is in question
    "pb_P0_cplx",    # 34 atoms, ECP60MDF
    "zn_P0_cplx",    # 34 atoms
    "cu_P1_cplx",    # 33 atoms, UKS
    "pb_P1_cplx",    # 33 atoms
    "zn_P1_cplx",    # 33 atoms
    "cu_P2_cplx",    # 32 atoms, UKS
    "pb_P2_cplx",    # 32 atoms
    "zn_P2_cplx",    # 32 atoms
    "lig_P0_LH2",    # 21 atoms
    "lig_P1_LH1m",   # 20 atoms
    "lig_P2_L2m",    # 19 atoms
    "cu_aquo6",      # 19 atoms, UKS
    "pb_aquo6",      # 19 atoms — headline Pb reference state
    "zn_aquo6",      # 19 atoms
    "pb_aquo8",      # 25 atoms — NOT headline; last so it delays nothing
]


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
    a(f"%pal nprocs {NPROCS} end")
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

    if not args.check:
        for job in JOB_ORDER:
            d = INPUTS / job
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            (d / f"{job}.inp").write_text(render_input(structures[job]))

        (INPUTS / "JOB_ORDER.txt").write_text(
            "# Chem-151 | queue order consumed by run_queue.sh\n"
            "# Longest-processing-time-first. water first (cheap end-to-end\n"
            "# validation), pb_aquo8 last (not a headline job, delays nothing).\n"
            + "".join(f"{j}\n" for j in JOB_ORDER)
        )

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
            str(NPROCS),
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
    print(f"{len(rows)} jobs | 16 headline + 1 alternative (pb_aquo8) | "
          f"maxcore {MAXCORE} MB/core x {NPROCS} cores")

    blanks = [r[0] for r in rows if any(str(c).strip() in ("", "?") for c in r)]
    if blanks:
        print(f"\nBLANK OR PLACEHOLDER CELLS -- these jobs must not launch: "
              f"{', '.join(blanks)}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
