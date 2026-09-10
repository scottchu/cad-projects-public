"""Print-kit-only composition for the frozen P20 R4 CAD candidate.

This module applies rigid bed-layout transforms to copies of the authoritative
P20 R4 solids.  It does not change parent geometry or waive its blockers.
"""

from __future__ import annotations

from copy import copy
from hashlib import sha256
from pathlib import Path

from build123d import Compound, Pos, Rot, Shape

from . import p20_r4_custom_profile_full_cad as parent


P20R4Parameters = parent.P20R4Parameters
P20_R4_DEFAULTS = parent.P20_R4_DEFAULTS
PARENT_SOURCE_SHA256 = "3eb9187ec7ad9205a2a1ced5e15e5a87a2a5a24e6c76282193ed086fb776d5b8"

PRINT_OBJECT_LABELS: tuple[str, ...] = (
    "print_fixed_left_inner_R20_blue_orange_rails_green_round_bore",
    "print_fixed_right_inner_R20_blue_orange_rails_green_round_bore",
    "print_rotating_left_outer_R22p5_three_inverse_rails_fixed_axle_arc",
    "print_rotating_right_outer_R22p5_three_inverse_rails_fixed_axle_arc",
    "print_fixed_stepped_axle_A_y-10_z-10_L44p90",
    "print_fixed_left_permanent_outer_keeper",
    "print_fixed_right_permanent_outer_keeper",
    "print_left_bottom_permanent_cap_H9p05",
    "print_right_bottom_permanent_cap_H9p05",
    "print_left_diagonal_permanent_cap_H9p05",
    "print_right_diagonal_permanent_cap_H9p05",
    "print_left_upright_permanent_cap_H9p05",
    "print_right_upright_permanent_cap_H9p05",
)

PRINT_LAYOUT_CENTERS_MM: tuple[tuple[float, float], ...] = (
    (-78.0, 42.0),
    (-22.0, 42.0),
    (42.0, 42.0),
    (108.0, 42.0),
    (-56.0, -28.0),
    (10.0, -28.0),
    (26.0, -28.0),
    (-34.0, -78.0),
    (48.0, -78.0),
    (-20.0, -78.0),
    (62.0, -78.0),
    (-6.0, -78.0),
    (76.0, -78.0),
)


def _place_print_part(
    source: Shape,
    label: str,
    center_xy: tuple[float, float],
    *,
    lay_x_axis_on_bed: bool,
) -> Shape:
    """Orient and place a copied frozen source solid without changing geometry."""

    oriented = Rot(0.0, -90.0, 0.0) * copy(source) if lay_x_axis_on_bed else copy(source)
    bounds = oriented.bounding_box()
    center_x = (float(bounds.min.X) + float(bounds.max.X)) / 2.0
    center_y = (float(bounds.min.Y) + float(bounds.max.Y)) / 2.0
    placed = Pos(
        center_xy[0] - center_x,
        center_xy[1] - center_y,
        -float(bounds.min.Z),
    ) * oriented
    placed.label = label
    placed.color = source.color
    return placed


def build_print_source_parts(
    p: P20R4Parameters = P20_R4_DEFAULTS,
) -> tuple[tuple[Shape, bool], ...]:
    """Frozen parent solids paired with whether their X axis is laid flat."""

    if parent.source_revision_sha256() != PARENT_SOURCE_SHA256:
        raise ValueError("parent P20 R4 source fingerprint changed")
    return (
        (parent.build_inner_plate("left", p), True),
        (parent.build_inner_plate("right", p), True),
        (parent.build_outer_plate("left", 0.0, p), True),
        (parent.build_outer_plate("right", 0.0, p), True),
        (parent.build_center_axle(p), False),
        (parent.build_keeper("left", p), True),
        (parent.build_keeper("right", p), True),
        (parent.build_cap("left", "bottom", 0.0, p), True),
        (parent.build_cap("right", "bottom", 0.0, p), True),
        (parent.build_cap("left", "diagonal", 0.0, p), True),
        (parent.build_cap("right", "diagonal", 0.0, p), True),
        (parent.build_cap("left", "upright", 0.0, p), True),
        (parent.build_cap("right", "upright", 0.0, p), True),
    )


def build_print_parts(p: P20R4Parameters = P20_R4_DEFAULTS) -> tuple[Shape, ...]:
    """Return the exact 13 frozen printable solids in deterministic bed order."""

    return tuple(
        _place_print_part(source, label, center, lay_x_axis_on_bed=lay_flat)
        for (source, lay_flat), label, center in zip(
            build_print_source_parts(p),
            PRINT_OBJECT_LABELS,
            PRINT_LAYOUT_CENTERS_MM,
            strict=True,
        )
    )


def build_print_kit(p: P20R4Parameters = P20_R4_DEFAULTS) -> Compound:
    """Blocked-test, model-only print layout; exactly 13 separate solids."""

    return Compound(
        children=list(build_print_parts(p)),
        label="P20_R4_BLOCKED_TEST_PRINT_KIT_13_OBJECTS_NO_RODS_XT60_OR_WIRE",
    )


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


__all__ = [
    "PARENT_SOURCE_SHA256",
    "PRINT_LAYOUT_CENTERS_MM",
    "PRINT_OBJECT_LABELS",
    "build_print_kit",
    "build_print_parts",
    "build_print_source_parts",
    "source_revision_sha256",
]
