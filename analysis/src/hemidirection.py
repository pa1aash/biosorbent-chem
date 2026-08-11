"""Geometric descriptors of hemidirected coordination.

Attack A14 asks whether hemidirection is asserted or measured. This module measures it.

A divalent post-transition ion with a stereochemically active ns2 lone pair — Pb(II) being the
canonical case — can adopt a coordination geometry in which the donor atoms are gathered into one
hemisphere, leaving a void occupied by the lone pair. Shimoni-Livny, Glusker and Bock termed this
*hemidirected*, as opposed to *holodirected* where donors surround the metal evenly.

Two descriptors are computed here.

**Centroid displacement.** The distance of the metal from the centroid of its donor set::

    d  = | r_M - (1/n) * sum_i r_i |                        (angstrom)
    d~ = d / mean_i |r_i - r_M|                             (dimensionless)

``d~`` is the primary reported quantity. Normalising by the mean bond length removes the trivial
dependence on ionic radius: without it, Pb would score higher than Cu simply for having longer
bonds, which would be an artefact rather than a result.

**Void-hemisphere angle.** With unit vectors ``u_i`` from metal to donor::

    v = - sum_i u_i / | sum_i u_i |                         (the void direction)
    theta_void = min_i arccos( v . u_i )                    (degrees)

``theta_void`` is the angular clearance of the empty hemisphere; larger means a more pronounced
void. When ``| sum_i u_i |`` is near zero the donor set is symmetric, no void direction exists, and
the geometry is holodirected — reported as such rather than as an arbitrary angle.

**The two descriptors are complementary and both are reported.** ``d~`` responds to radial
asymmetry (donors at unequal distances); ``theta_void`` is purely angular and by construction does
not. A donor set that is angularly symmetric but radially uneven is correctly reported as
holodirected by ``theta_void`` while ``d~`` is non-zero. One number cannot capture both
distortions, which is why Table 4.7 carries both.

Reference for the concept:
    Shimoni-Livny, L.; Glusker, J. P.; Bock, C. W. Lone Pair Functionality in Divalent Lead
    Compounds. *Inorg. Chem.* **1998**, *37* (8), 1853-1867.

The descriptors implemented here are this project's own operationalisation of that concept; the
definitions above are stated in the report rather than assumed (report section 3.5).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "HemidirectionResult",
    "analyse",
    "centroid_displacement",
    "void_direction",
    "void_hemisphere_angle",
    "from_xyz",
]

# Below this, the sum of donor unit vectors is indistinguishable from zero and the donor set is
# treated as symmetric. 1e-6 would be numerical noise; 0.05 is a physically meaningful threshold
# that tolerates small distortions of a genuinely holodirected shell.
SYMMETRY_TOLERANCE = 0.05

# Normalised displacement above which the geometry is called hemidirected. Reported alongside the
# raw numbers so that a reader can apply a different threshold; the verdict is a convenience, the
# measurement is the result.
HEMIDIRECTED_THRESHOLD = 0.15


@dataclass
class HemidirectionResult:
    """Descriptors for one metal centre. All lengths in angstrom, angles in degrees."""

    n_donors: int
    bond_lengths: np.ndarray = field(repr=False)
    mean_bond_length: float
    displacement: float
    normalised_displacement: float
    asymmetry: float
    """|sum of donor unit vectors| / n. Zero for a perfectly symmetric donor set."""
    void_vector: np.ndarray | None = field(repr=False, default=None)
    void_angle: float | None = None
    holodirected: bool = False

    @property
    def verdict(self) -> str:
        if self.holodirected:
            return "holodirected"
        return (
            "hemidirected"
            if self.normalised_displacement >= HEMIDIRECTED_THRESHOLD
            else "weakly hemidirected"
        )

    def summary(self) -> str:
        void = "n/a (symmetric donor set)" if self.void_angle is None else f"{self.void_angle:.2f} deg"
        return (
            f"n donors           {self.n_donors}\n"
            f"mean M-L distance  {self.mean_bond_length:.4f} A\n"
            f"displacement d     {self.displacement:.4f} A\n"
            f"normalised d~      {self.normalised_displacement:.4f}\n"
            f"asymmetry          {self.asymmetry:.4f}\n"
            f"void angle         {void}\n"
            f"verdict            {self.verdict}"
        )


def _as_array(metal, donors) -> tuple[np.ndarray, np.ndarray]:
    m = np.asarray(metal, dtype=float).reshape(3)
    d = np.asarray(donors, dtype=float)
    if d.ndim != 2 or d.shape[1] != 3:
        raise ValueError(f"donors must have shape (n, 3); got {d.shape}")
    if d.shape[0] < 2:
        raise ValueError("at least two donor atoms are required")
    if np.any(np.linalg.norm(d - m, axis=1) < 1e-8):
        raise ValueError("a donor atom coincides with the metal position")
    return m, d


def centroid_displacement(metal, donors) -> float:
    """Distance of the metal from the centroid of its donor set, in angstrom."""
    m, d = _as_array(metal, donors)
    return float(np.linalg.norm(m - d.mean(axis=0)))


def void_direction(metal, donors) -> np.ndarray | None:
    """Unit vector pointing into the donor-free hemisphere, or None if the set is symmetric."""
    m, d = _as_array(metal, donors)
    v = d - m
    u = v / np.linalg.norm(v, axis=1, keepdims=True)
    s = u.sum(axis=0)
    if np.linalg.norm(s) < SYMMETRY_TOLERANCE:
        return None
    return -s / np.linalg.norm(s)


def void_hemisphere_angle(metal, donors) -> float | None:
    """Smallest angle (degrees) between the void direction and any metal-to-donor vector."""
    m, d = _as_array(metal, donors)
    vhat = void_direction(m, d)
    if vhat is None:
        return None
    v = d - m
    u = v / np.linalg.norm(v, axis=1, keepdims=True)
    # Clip guards against |cos| marginally exceeding 1 through floating-point error.
    cos = np.clip(u @ vhat, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos)).min())


def analyse(metal, donors) -> HemidirectionResult:
    """Compute every descriptor for one metal centre."""
    m, d = _as_array(metal, donors)
    v = d - m
    lengths = np.linalg.norm(v, axis=1)
    u = v / lengths[:, None]
    s = u.sum(axis=0)
    asym = float(np.linalg.norm(s) / len(d))

    disp = float(np.linalg.norm(m - d.mean(axis=0)))
    mean_len = float(lengths.mean())

    if np.linalg.norm(s) < SYMMETRY_TOLERANCE:
        return HemidirectionResult(
            n_donors=len(d),
            bond_lengths=lengths,
            mean_bond_length=mean_len,
            displacement=disp,
            normalised_displacement=disp / mean_len,
            asymmetry=asym,
            void_vector=None,
            void_angle=None,
            holodirected=True,
        )

    vhat = -s / np.linalg.norm(s)
    cos = np.clip(u @ vhat, -1.0, 1.0)
    return HemidirectionResult(
        n_donors=len(d),
        bond_lengths=lengths,
        mean_bond_length=mean_len,
        displacement=disp,
        normalised_displacement=disp / mean_len,
        asymmetry=asym,
        void_vector=vhat,
        void_angle=float(np.degrees(np.arccos(cos)).min()),
        holodirected=False,
    )


def from_xyz(path, metal_symbol, donor_symbols=("O", "N"), cutoff=3.2) -> HemidirectionResult:
    """Read an XYZ file and analyse the first atom matching ``metal_symbol``.

    Donors are every atom whose symbol is in ``donor_symbols`` and which lies within ``cutoff``
    angstrom of the metal. The cutoff is deliberately explicit: Pb-O distances run appreciably
    longer than Cu-O, and a cutoff that excludes a genuine Pb donor would manufacture the very
    asymmetry this module exists to measure. Always check ``n_donors`` against the optimised
    structure before reporting.
    """
    symbols, coords = [], []
    with open(path) as fh:
        lines = fh.read().splitlines()
    n = int(lines[0].split()[0])
    for line in lines[2 : 2 + n]:
        parts = line.split()
        symbols.append(parts[0])
        coords.append([float(x) for x in parts[1:4]])
    symbols = np.array(symbols)
    coords = np.asarray(coords, dtype=float)

    idx = np.flatnonzero(symbols == metal_symbol)
    if idx.size == 0:
        raise ValueError(f"no atom {metal_symbol!r} in {path}")
    m = coords[idx[0]]

    mask = np.isin(symbols, list(donor_symbols))
    mask[idx[0]] = False
    within = np.linalg.norm(coords - m, axis=1) <= cutoff
    donors = coords[mask & within]
    if len(donors) < 2:
        raise ValueError(
            f"only {len(donors)} donor(s) found within {cutoff} A of {metal_symbol} in {path}; "
            "check the cutoff before reporting"
        )
    return analyse(m, donors)


if __name__ == "__main__":  # pragma: no cover
    print("Three mutually orthogonal donors at 2.5 A (hand-worked case):\n")
    print(analyse([0, 0, 0], [[2.5, 0, 0], [0, 2.5, 0], [0, 0, 2.5]]).summary())
    print("\nRegular octahedron at 2.5 A:\n")
    oct_donors = [[2.5, 0, 0], [-2.5, 0, 0], [0, 2.5, 0], [0, -2.5, 0], [0, 0, 2.5], [0, 0, -2.5]]
    print(analyse([0, 0, 0], oct_donors).summary())
