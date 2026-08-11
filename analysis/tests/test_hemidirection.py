"""Unit tests for the hemidirection descriptors.

The central test is a geometry worked by hand, so the implementation is checked against arithmetic
rather than against its own output.

THE HAND-WORKED CASE
--------------------
Metal at the origin. Three donors at 2.5 A along +x, +y and +z::

    r_1 = (2.5, 0, 0)   r_2 = (0, 2.5, 0)   r_3 = (0, 0, 2.5)

*Centroid.*  c = (1/3)(r_1 + r_2 + r_3) = (2.5/3)(1, 1, 1)

*Displacement.*  d = |0 - c| = (2.5/3) * sqrt(3) = 2.5/sqrt(3) = 1.443375673...

*Mean bond length.*  every donor is 2.5 A away, so <|r_i - r_M|> = 2.5 exactly.

*Normalised displacement.*  d~ = (2.5/sqrt(3)) / 2.5 = 1/sqrt(3) = 0.577350269...

*Void direction.*  the unit vectors are the Cartesian axes, so sum u_i = (1, 1, 1) and

    v = -(1, 1, 1)/sqrt(3)

*Void angle.*  for each donor, v . u_i = -1/sqrt(3), so

    theta_void = arccos(-1/sqrt(3)) = 125.264389683... degrees

identical for all three by symmetry, so the minimum is that value.

*Asymmetry.*  |sum u_i| / n = sqrt(3)/3 = 0.577350269...
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import hemidirection as hd  # noqa: E402

SQRT3 = math.sqrt(3.0)

# The hand-worked geometry described in the module docstring.
TRIAD_METAL = [0.0, 0.0, 0.0]
TRIAD_DONORS = [[2.5, 0.0, 0.0], [0.0, 2.5, 0.0], [0.0, 0.0, 2.5]]

EXPECTED_DISPLACEMENT = 2.5 / SQRT3          # 1.4433756729740643
EXPECTED_NORMALISED = 1.0 / SQRT3            # 0.5773502691896258
EXPECTED_VOID_ANGLE = math.degrees(math.acos(-1.0 / SQRT3))   # 125.26438968275465

OCTAHEDRON = [
    [2.5, 0.0, 0.0], [-2.5, 0.0, 0.0],
    [0.0, 2.5, 0.0], [0.0, -2.5, 0.0],
    [0.0, 0.0, 2.5], [0.0, 0.0, -2.5],
]


# ---------------------------------------------------------------------------
# The hand-worked case
# ---------------------------------------------------------------------------

def test_displacement_matches_hand_calculation():
    assert hd.centroid_displacement(TRIAD_METAL, TRIAD_DONORS) == pytest.approx(
        EXPECTED_DISPLACEMENT, abs=1e-12
    )
    assert hd.centroid_displacement(TRIAD_METAL, TRIAD_DONORS) == pytest.approx(1.4433756729740643)


def test_void_angle_matches_hand_calculation():
    assert hd.void_hemisphere_angle(TRIAD_METAL, TRIAD_DONORS) == pytest.approx(
        EXPECTED_VOID_ANGLE, abs=1e-10
    )
    assert hd.void_hemisphere_angle(TRIAD_METAL, TRIAD_DONORS) == pytest.approx(125.26438968275465)


def test_void_direction_matches_hand_calculation():
    v = hd.void_direction(TRIAD_METAL, TRIAD_DONORS)
    assert v == pytest.approx(np.array([-1, -1, -1]) / SQRT3, abs=1e-12)
    assert np.linalg.norm(v) == pytest.approx(1.0, abs=1e-12)


def test_analyse_reproduces_every_hand_worked_quantity():
    r = hd.analyse(TRIAD_METAL, TRIAD_DONORS)
    assert r.n_donors == 3
    assert r.mean_bond_length == pytest.approx(2.5, abs=1e-12)
    assert r.displacement == pytest.approx(EXPECTED_DISPLACEMENT, abs=1e-12)
    assert r.normalised_displacement == pytest.approx(EXPECTED_NORMALISED, abs=1e-12)
    assert r.asymmetry == pytest.approx(SQRT3 / 3.0, abs=1e-12)
    assert r.void_angle == pytest.approx(EXPECTED_VOID_ANGLE, abs=1e-10)
    assert r.holodirected is False
    assert r.verdict == "hemidirected"


# ---------------------------------------------------------------------------
# Symmetric donor sets must be reported as holodirected, not given a spurious angle
# ---------------------------------------------------------------------------

def test_regular_octahedron_is_holodirected():
    r = hd.analyse([0, 0, 0], OCTAHEDRON)
    assert r.holodirected is True
    assert r.void_angle is None
    assert r.void_vector is None
    assert r.displacement == pytest.approx(0.0, abs=1e-12)
    assert r.asymmetry == pytest.approx(0.0, abs=1e-12)
    assert r.verdict == "holodirected"


def test_square_planar_is_holodirected():
    """Square planar has two voids, so no single void direction exists. It must not be
    reported as hemidirected on the strength of an arbitrary choice between them."""
    donors = [[2.0, 0, 0], [-2.0, 0, 0], [0, 2.0, 0], [0, -2.0, 0]]
    r = hd.analyse([0, 0, 0], donors)
    assert r.holodirected is True
    assert r.void_angle is None


def test_trigonal_planar_is_holodirected():
    donors = [
        [2.2 * math.cos(a), 2.2 * math.sin(a), 0.0]
        for a in (0.0, 2 * math.pi / 3, 4 * math.pi / 3)
    ]
    r = hd.analyse([0, 0, 0], donors)
    assert r.holodirected is True


# ---------------------------------------------------------------------------
# Invariances the descriptors must obey to be comparable across metals
# ---------------------------------------------------------------------------

def test_descriptors_are_translation_invariant():
    shift = np.array([13.7, -4.2, 0.9])
    a = hd.analyse(TRIAD_METAL, TRIAD_DONORS)
    b = hd.analyse(np.array(TRIAD_METAL) + shift, np.array(TRIAD_DONORS) + shift)
    assert b.displacement == pytest.approx(a.displacement, abs=1e-12)
    assert b.void_angle == pytest.approx(a.void_angle, abs=1e-10)


def test_descriptors_are_rotation_invariant():
    theta = 0.7913
    c, s = math.cos(theta), math.sin(theta)
    # Rotation about z composed with one about x, so no axis is left unmoved.
    rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    rot = rx @ rz
    a = hd.analyse(TRIAD_METAL, TRIAD_DONORS)
    b = hd.analyse(rot @ np.array(TRIAD_METAL), (rot @ np.array(TRIAD_DONORS).T).T)
    assert b.displacement == pytest.approx(a.displacement, abs=1e-12)
    assert b.normalised_displacement == pytest.approx(a.normalised_displacement, abs=1e-12)
    assert b.void_angle == pytest.approx(a.void_angle, abs=1e-10)


def test_normalised_displacement_is_scale_invariant():
    """The point of normalising: a longer-bonded metal must not score higher for that reason
    alone. Without this, Pb would outscore Cu as an artefact of ionic radius."""
    small = hd.analyse([0, 0, 0], [[2.0, 0, 0], [0, 2.0, 0], [0, 0, 2.0]])
    large = hd.analyse([0, 0, 0], [[2.6, 0, 0], [0, 2.6, 0], [0, 0, 2.6]])
    assert large.displacement > small.displacement          # raw value does scale
    assert large.normalised_displacement == pytest.approx(  # normalised value does not
        small.normalised_displacement, abs=1e-12
    )
    assert large.void_angle == pytest.approx(small.void_angle, abs=1e-10)


# ---------------------------------------------------------------------------
# Ordering behaviour: the descriptors must respond monotonically to a real distortion
# ---------------------------------------------------------------------------

def _cone(half_angle_deg, n=4, r=2.5):
    """n donors evenly spaced in azimuth on a cone of the given half-angle about +z."""
    a = math.radians(half_angle_deg)
    return [
        [r * math.sin(a) * math.cos(2 * math.pi * i / n),
         r * math.sin(a) * math.sin(2 * math.pi * i / n),
         r * math.cos(a)]
        for i in range(n)
    ]


def test_progressive_angular_clustering_increases_both_descriptors():
    """Gather four donors onto a progressively tighter cone about +z. The donor set becomes
    increasingly one-sided, so both descriptors must increase monotonically.

    Hand-checkable: for a cone of half-angle a, the centroid sits at 2.5*cos(a) along +z, so the
    displacement is 2.5*cos(a); and the void direction is -z, giving a void angle of
    arccos(-cos a) = 180 - a degrees.
    """
    prev_disp, prev_angle = -1.0, -1.0
    for half_angle in (75.0, 60.0, 45.0, 30.0):
        r = hd.analyse([0, 0, 0], _cone(half_angle))
        assert r.displacement == pytest.approx(2.5 * math.cos(math.radians(half_angle)), abs=1e-10)
        assert r.void_angle == pytest.approx(180.0 - half_angle, abs=1e-10)
        assert r.displacement > prev_disp
        assert r.void_angle > prev_angle
        prev_disp, prev_angle = r.displacement, r.void_angle


def test_void_angle_is_blind_to_purely_radial_asymmetry():
    """A documented limitation, not a defect.

    Stretching three of six octahedral donors outward leaves every metal-to-donor UNIT vector
    unchanged, so the void-angle descriptor -- which is purely angular -- still reports a
    symmetric donor set. The centroid displacement does respond.

    This is why both descriptors are reported. Angular clustering and radial asymmetry are
    different distortions and one number cannot capture both. Report section 3.5 states this.
    """
    donors = [
        [2.5, 0, 0], [-4.0, 0, 0],
        [0, 2.5, 0], [0, -4.0, 0],
        [0, 0, 2.5], [0, 0, -4.0],
    ]
    r = hd.analyse([0, 0, 0], donors)
    assert r.holodirected is True          # angular measure: symmetric, correctly
    assert r.void_angle is None
    # Centroid sits at ((2.5-4.0)/6) along each axis, i.e. -0.25, so d = 0.25*sqrt(3).
    assert r.displacement == pytest.approx(0.25 * SQRT3, abs=1e-10)
    assert r.displacement > 0.4            # radial measure: responds


# ---------------------------------------------------------------------------
# Input validation: fail loudly rather than return a plausible wrong number
# ---------------------------------------------------------------------------

def test_rejects_too_few_donors():
    with pytest.raises(ValueError, match="at least two donor"):
        hd.analyse([0, 0, 0], [[2.5, 0, 0]])


def test_rejects_donor_coincident_with_metal():
    with pytest.raises(ValueError, match="coincides"):
        hd.analyse([0, 0, 0], [[0, 0, 0], [2.5, 0, 0], [0, 2.5, 0]])


def test_rejects_wrong_shape():
    with pytest.raises(ValueError, match=r"shape \(n, 3\)"):
        hd.analyse([0, 0, 0], [[2.5, 0], [0, 2.5]])


# ---------------------------------------------------------------------------
# XYZ reading
# ---------------------------------------------------------------------------

def test_from_xyz_reproduces_the_hand_worked_case(tmp_path):
    p = tmp_path / "triad.xyz"
    p.write_text(
        "4\n"
        "hand-worked triad; charge 2 multiplicity 1\n"
        "Pb 0.000000 0.000000 0.000000\n"
        "O  2.500000 0.000000 0.000000\n"
        "O  0.000000 2.500000 0.000000\n"
        "O  0.000000 0.000000 2.500000\n"
    )
    r = hd.from_xyz(p, "Pb")
    assert r.n_donors == 3
    assert r.displacement == pytest.approx(EXPECTED_DISPLACEMENT, abs=1e-9)
    assert r.void_angle == pytest.approx(EXPECTED_VOID_ANGLE, abs=1e-8)


def test_from_xyz_raises_when_the_cutoff_excludes_donors(tmp_path):
    """A cutoff that silently drops a genuine donor would manufacture asymmetry. It must raise."""
    p = tmp_path / "far.xyz"
    p.write_text(
        "4\n\n"
        "Pb 0.0 0.0 0.0\n"
        "O  2.5 0.0 0.0\n"
        "O  0.0 9.0 0.0\n"
        "O  0.0 0.0 9.0\n"
    )
    with pytest.raises(ValueError, match="check the cutoff"):
        hd.from_xyz(p, "Pb", cutoff=3.2)
