"""P1 manual three-plate geometry proof.

Coordinate convention follows P0: rods run on X, Y runs from the ESC pads
toward the bend, and Z is up.  The complete concept assembly is lifted 20 mm
so the removable pusher can withdraw along its unobstructed +Y/-Z 45 degree
path without crossing the assembly floor.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Pos, Rot, Shape
from cadgen import srgb

from .geometry import (
    build_esc_reference,
    build_fc_reference,
    build_wire_reference,
    build_xt60_reference,
)
from .mechanism import PointYZ, solve_mechanism
from .parameters import DEFAULT_PARAMETERS


Side = Literal["left", "right"]


@dataclass(frozen=True, slots=True)
class SimpleP1Parameters:
    wire_gauge: int = 12
    rod_diameter: float = 4.0
    rod_length: float = 50.0
    rod_bore_diameter: float = 4.3
    clear_span: float = 38.0
    plate_thickness: float = 4.0
    assembly_z_lift: float = 20.0
    manual_withdrawal: float = 11.0
    large_base_y_min: float = -8.0
    hard_stop_y: float = 18.0
    large_base_z_max: float = 12.0
    large_top_z: float = 36.0

    def __post_init__(self) -> None:
        if self.wire_gauge != 12:
            raise ValueError("P1 manual geometry proof supports 12 AWG only")
        if self.rod_diameter != 4.0 or self.rod_length != 50.0:
            raise ValueError("P1 uses exactly three purchased 4 x 50 mm rods")

    @property
    def outer_span(self) -> float:
        return self.clear_span + 2.0 * self.plate_thickness

    @property
    def plate_center_x(self) -> float:
        return (self.clear_span + self.plate_thickness) / 2.0

    @property
    def withdrawal_component(self) -> float:
        return self.manual_withdrawal / sqrt(2.0)


P1_SIMPLE_DEFAULTS = SimpleP1Parameters()


def _label(shape: Shape, label: str, color: str | None = None) -> Shape:
    shape.label = label
    if color:
        shape.color = srgb(color)
    return shape


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def closed_contact_centers(
    params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS,
) -> dict[str, PointYZ]:
    solved = solve_mechanism(wire_gauge=12, closure=1.0, upper_index=1, lower_index=1)
    lift = params.assembly_z_lift
    return {
        "upper": PointYZ(solved.upper_rod_center.y, solved.upper_rod_center.z + lift),
        "lower": PointYZ(solved.lower_rod_center.y, solved.lower_rod_center.z + lift),
        "moving": PointYZ(solved.moving_rod_center.y, solved.moving_rod_center.z + lift),
    }


def build_large_side_plate(
    side: Side,
    params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS,
) -> Shape:
    """One broad L plate with exactly two paired Ø4.3 reaction-rod bores."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.plate_center_x
    lift = params.assembly_z_lift

    # Complementary L corner: the manual pusher tab occupies Y>=18, Z<=12.
    base = Pos(
        x,
        (params.large_base_y_min + params.hard_stop_y) / 2.0,
        lift + params.large_base_z_max / 2.0,
    ) * Box(
        params.plate_thickness,
        params.hard_stop_y - params.large_base_y_min,
        params.large_base_z_max,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    upright = Pos(
        x,
        (12.0 + 24.0) / 2.0,
        lift + (params.large_base_z_max + params.large_top_z) / 2.0,
    ) * Box(
        params.plate_thickness,
        12.0,
        params.large_top_z - params.large_base_z_max,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    body = base + upright

    centers = closed_contact_centers(params)
    bores = [
        _x_cylinder(
            params.rod_bore_diameter,
            params.plate_thickness + 2.0,
            x,
            centers[name].y,
            centers[name].z,
        )
        for name in ("upper", "lower")
    ]
    return _label(
        body - bores,
        f"{side}_large_fixed_L_plate_two_4p3_bores_12awg",
        "#3F6B4F",
    )


def build_center_pusher(
    params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS,
) -> Shape:
    """One rigid bridge plus two small L tabs, each with one moving-rod bore."""

    centers = closed_contact_centers(params)
    moving = centers["moving"]
    # Both tab solids occupy the complementary quadrant and touch the large
    # plates only at the Y=18 and Z=lift+12 hard-stop faces.
    tab_parts: list[Shape] = []
    for sign in (-1.0, 1.0):
        x = sign * params.plate_center_x
        horizontal = Pos(x, 24.0, params.assembly_z_lift + 8.0) * Box(
            params.plate_thickness,
            12.0,
            8.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        toe = Pos(x, 27.0, params.assembly_z_lift + 4.0) * Box(
            params.plate_thickness,
            6.0,
            8.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        tab = horizontal + toe
        bore = _x_cylinder(
            params.rod_bore_diameter,
            params.plate_thickness + 2.0,
            x,
            moving.y,
            moving.z,
        )
        tab_parts.append(tab - bore)

    # The low forward bridge joins both end tabs without entering the wire
    # bend envelope.  It is intentionally part of the same fused printable.
    bridge = Pos(0.0, 27.0, params.assembly_z_lift + 2.0) * Box(
        params.outer_span,
        6.0,
        4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    pusher = bridge + tab_parts
    return _label(
        pusher,
        "manual_geometry_proof_only_rigid_center_pusher_two_small_L_tabs",
        "#E0A323",
    )


def build_reference_rod(name: str, center: PointYZ, params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS) -> Shape:
    return _label(
        _x_cylinder(params.rod_diameter, params.rod_length, 0.0, center.y, center.z),
        f"reference_user_4x50_{name}_rod",
        "#C9D0D4",
    )


def build_three_rods(params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS) -> Compound:
    centers = closed_contact_centers(params)
    return Compound(
        children=[build_reference_rod(name, centers[name], params) for name in ("upper", "lower", "moving")],
        label="reference_exactly_three_user_4x50_rods",
    )


def _workpiece_references(params: SimpleP1Parameters) -> list[Shape]:
    solved = solve_mechanism(wire_gauge=12, closure=1.0, upper_index=1, lower_index=1)
    lift = params.assembly_z_lift
    esc = Pos(0, -24.0, 8.5 + lift) * build_esc_reference()
    esc.label = "reference_bottom_ESC"
    esc.color = srgb("#22262B")
    fc = Pos(0, -24.0, 25.0 + lift) * build_fc_reference()
    fc.label = "reference_upper_FC"
    fc.color = srgb("#4D5963")
    wires = Compound(
        children=[
            Pos(0, 0, lift) * build_wire_reference(x, wire_gauge=12, closure=1.0)
            for x in (-4.0, 4.0)
        ],
        label="reference_two_horizontal_R6_90deg_vertical_12awg_leads",
    )
    for index, child in enumerate(wires.children):
        child.color = srgb("#D64536" if index == 0 else "#17191C")
    endpoint = solved.wire_endpoint
    xt60 = Pos(0, endpoint.y, endpoint.z + lift) * build_xt60_reference(DEFAULT_PARAMETERS)
    xt60.label = "reference_vertical_XT60"
    xt60.color = srgb("#E8B923")
    return [esc, fc, wires, xt60]


def build_loaded_closed(params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_large_side_plate("left", params),
            build_large_side_plate("right", params),
            build_center_pusher(params),
            build_three_rods(params),
            *_workpiece_references(params),
        ],
        label="p1_simple_three_plate_loaded_closed_manual_geometry_proof_only",
    )


def build_loaded_open(params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS) -> Compound:
    delta = params.withdrawal_component
    pusher = Pos(0, delta, -delta) * build_center_pusher(params)
    pusher.label = "manual_pusher_withdrawn_11mm_on_45deg_removal_path"
    centers = closed_contact_centers(params)
    moving = PointYZ(centers["moving"].y + delta, centers["moving"].z - delta)
    rods = Compound(
        children=[
            build_reference_rod("upper", centers["upper"], params),
            build_reference_rod("lower", centers["lower"], params),
            build_reference_rod("moving_withdrawn", moving, params),
        ],
        label="reference_three_rods_open_state",
    )
    return Compound(
        children=[
            build_large_side_plate("left", params),
            build_large_side_plate("right", params),
            pusher,
            rods,
            *_workpiece_references(params),
        ],
        label="p1_simple_three_plate_loaded_open_manual_removal_path",
    )


def _on_bed(shape: Shape, x: float, y: float, rotate_plate: bool = False) -> Shape:
    oriented = Rot(0, 90, 0) * shape if rotate_plate else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: SimpleP1Parameters = P1_SIMPLE_DEFAULTS) -> Compound:
    left = _on_bed(build_large_side_plate("left", params), 0.0, 0.0, True)
    left.label = "print_left_large_L_plate"
    right = _on_bed(build_large_side_plate("right", params), 55.0, 0.0, True)
    right.label = "print_right_large_L_plate"
    pusher = _on_bed(build_center_pusher(params), 100.0, 0.0, False)
    pusher.label = "print_one_piece_center_pusher"
    return Compound(children=[left, right, pusher], label="p1_print_kit_exactly_three_printed_solids")


__all__ = [
    "P1_SIMPLE_DEFAULTS",
    "SimpleP1Parameters",
    "build_center_pusher",
    "build_large_side_plate",
    "build_loaded_closed",
    "build_loaded_open",
    "build_print_kit",
    "build_reference_rod",
    "build_three_rods",
    "closed_contact_centers",
]

