"""P2 mirrored manual corner-clamp geometry proof.

This module intentionally does not call the P0 kinematic solver.  Its wire
path and three contact datums are derived directly from the frozen mirrored
side-view contract.

Axes: rods run on X, Y points right toward the ESC, and Z points up.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt
from typing import Literal

from build123d import (
    Align,
    Box,
    BuildLine,
    BuildSketch,
    CenterArc,
    Circle,
    Compound,
    Cylinder,
    Line,
    Plane,
    Pos,
    Rot,
    Shape,
    Wire,
    sweep,
)
from cadgen import srgb


Side = Literal["left", "right"]


@dataclass(frozen=True, slots=True)
class PointYZ:
    y: float
    z: float

    def distance_to(self, other: "PointYZ") -> float:
        return sqrt((self.y - other.y) ** 2 + (self.z - other.z) ** 2)


@dataclass(frozen=True, slots=True)
class P2Parameters:
    wire_gauge: int = 12
    wire_diameter: float = 4.3
    rod_diameter: float = 4.0
    rod_length: float = 50.0
    rod_bore_diameter: float = 4.3
    clear_span: float = 38.0
    plate_thickness: float = 4.0

    bend_radius: float = 6.0
    available_lead: float = 44.0
    horizontal_z: float = 30.0
    pad_y: float = 28.0
    horizontal_tangent_y: float = 6.0
    vertical_y: float = 0.0
    vertical_tangent_z: float = 36.0

    fixed_bottom_y: float = 12.0
    fixed_bottom_z: float = 25.85
    fixed_left_y: float = -4.15
    fixed_left_z: float = 42.0
    moving_closed_y: float = 4.691852455
    moving_closed_z: float = 34.691852455
    diagonal_stroke: float = 11.0

    fixed_y_min: float = -12.0
    fixed_y_max: float = 25.0
    fixed_z_min: float = 20.0
    fixed_z_max: float = 55.0
    stop_y: float = 0.0
    stop_z: float = 30.0

    def __post_init__(self) -> None:
        if self.wire_gauge != 12 or self.wire_diameter != 4.3:
            raise ValueError("P2 corner-clamp geometry is frozen for 12 AWG only")
        if self.rod_diameter != 4.0 or self.rod_length != 50.0:
            raise ValueError("P2 uses exactly three 4 x 50 mm rods")

    @property
    def wire_radius(self) -> float:
        return self.wire_diameter / 2.0

    @property
    def rod_radius(self) -> float:
        return self.rod_diameter / 2.0

    @property
    def rho(self) -> float:
        return self.wire_radius + self.rod_radius

    @property
    def outer_span(self) -> float:
        return self.clear_span + 2.0 * self.plate_thickness

    @property
    def plate_center_x(self) -> float:
        return (self.clear_span + self.plate_thickness) / 2.0

    @property
    def horizontal_length(self) -> float:
        return self.pad_y - self.horizontal_tangent_y

    @property
    def arc_length(self) -> float:
        return pi * self.bend_radius / 2.0

    @property
    def vertical_length(self) -> float:
        return self.available_lead - self.horizontal_length - self.arc_length

    @property
    def vertical_endpoint_z(self) -> float:
        return self.vertical_tangent_z + self.vertical_length

    @property
    def withdrawal_component(self) -> float:
        return self.diagonal_stroke / sqrt(2.0)

    @property
    def moving_open(self) -> PointYZ:
        d = self.withdrawal_component
        return PointYZ(self.moving_closed_y + d, self.moving_closed_z + d)


P2_DEFAULTS = P2Parameters()


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
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


def contact_points(params: P2Parameters = P2_DEFAULTS) -> dict[str, PointYZ]:
    q = PointYZ(
        6.0 - 6.0 / sqrt(2.0),
        36.0 - 6.0 / sqrt(2.0),
    )
    return {
        "bottom": PointYZ(params.fixed_bottom_y, params.horizontal_z),
        "left": PointYZ(params.vertical_y, params.fixed_left_z),
        "moving": q,
    }


def rod_centers(params: P2Parameters = P2_DEFAULTS) -> dict[str, PointYZ]:
    return {
        "bottom": PointYZ(params.fixed_bottom_y, params.fixed_bottom_z),
        "left": PointYZ(params.fixed_left_y, params.fixed_left_z),
        "moving": PointYZ(params.moving_closed_y, params.moving_closed_z),
    }


def build_wire_centerline(
    x: float = 0.0,
    params: P2Parameters = P2_DEFAULTS,
) -> Wire:
    with BuildLine(Plane.YZ) as path:
        Line((params.pad_y, params.horizontal_z), (params.horizontal_tangent_y, params.horizontal_z))
        CenterArc(
            (params.horizontal_tangent_y, params.vertical_tangent_z),
            params.bend_radius,
            -90.0,
            -90.0,
        )
        Line((params.vertical_y, params.vertical_tangent_z), (params.vertical_y, params.vertical_endpoint_z))
    return Pos(x, 0.0, 0.0) * Wire(path.line.edges())


def build_wire(
    x: float,
    color: str,
    params: P2Parameters = P2_DEFAULTS,
) -> Shape:
    centerline = build_wire_centerline(x, params)
    start_plane = Plane(
        origin=(x, params.pad_y, params.horizontal_z),
        x_dir=(1, 0, 0),
        z_dir=(0, -1, 0),
    )
    with BuildSketch(start_plane) as profile:
        Circle(params.wire_radius)
    return _label(
        sweep(profile.sketch, centerline),
        f"reference_12awg_R6_mirrored_wire_{x:+.1f}",
        color,
    )


def build_wires(params: P2Parameters = P2_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_wire(-4.0, "#D64536", params),
            build_wire(4.0, "#17191C", params),
        ],
        label="reference_two_mirrored_12awg_R6_leads",
    )


def build_fixed_plate(side: Side, params: P2Parameters = P2_DEFAULTS) -> Shape:
    """Large lower-left L with exactly two Ø4.3 reaction bores."""

    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.plate_center_x
    vertical = Pos(
        x,
        (params.fixed_y_min + params.stop_y) / 2.0,
        (params.fixed_z_min + params.fixed_z_max) / 2.0,
    ) * Box(
        params.plate_thickness,
        params.stop_y - params.fixed_y_min,
        params.fixed_z_max - params.fixed_z_min,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    horizontal = Pos(
        x,
        (params.fixed_y_min + params.fixed_y_max) / 2.0,
        (params.fixed_z_min + params.stop_z) / 2.0,
    ) * Box(
        params.plate_thickness,
        params.fixed_y_max - params.fixed_y_min,
        params.stop_z - params.fixed_z_min,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    centers = rod_centers(params)
    bores = [
        _x_cylinder(
            params.rod_bore_diameter,
            params.plate_thickness + 2.0,
            x,
            centers[name].y,
            centers[name].z,
        )
        for name in ("left", "bottom")
    ]
    return _label(
        (vertical + horizontal) - bores,
        f"{side}_large_fixed_lower_left_L_two_4p3_bores_12awg",
        "#3F6B4F",
    )


def build_pusher(params: P2Parameters = P2_DEFAULTS) -> Shape:
    """One bridge and two upper-right L jaws with the moving-axis bores."""

    moving = rod_centers(params)["moving"]
    tabs: list[Shape] = []
    for sign in (-1.0, 1.0):
        x = sign * params.plate_center_x
        horizontal = Pos(x, 7.0, 35.0) * Box(
            params.plate_thickness,
            14.0,
            10.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        upright = Pos(x, 12.0, 40.0) * Box(
            params.plate_thickness,
            4.0,
            20.0,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        bore = _x_cylinder(
            params.rod_bore_diameter,
            params.plate_thickness + 2.0,
            x,
            moving.y,
            moving.z,
        )
        tabs.append((horizontal + upright) - bore)

    bridge = Pos(0.0, 12.0, 48.0) * Box(
        params.outer_span,
        4.0,
        4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    return _label(
        bridge + tabs,
        "manual_geometry_proof_only_one_piece_upper_right_corner_pusher",
        "#E0A323",
    )


def build_reference_rod(name: str, center: PointYZ, params: P2Parameters = P2_DEFAULTS) -> Shape:
    return _label(
        _x_cylinder(params.rod_diameter, params.rod_length, 0.0, center.y, center.z),
        f"reference_user_4x50_{name}_rod",
        "#C9D0D4",
    )


def build_rods(
    moving_center: PointYZ | None = None,
    params: P2Parameters = P2_DEFAULTS,
) -> Compound:
    centers = rod_centers(params)
    if moving_center is not None:
        centers["moving"] = moving_center
    return Compound(
        children=[build_reference_rod(name, centers[name], params) for name in ("left", "bottom", "moving")],
        label="reference_exactly_three_user_4x50_rods",
    )


def build_esc(params: P2Parameters = P2_DEFAULTS) -> Shape:
    return _label(
        Pos(0.0, 46.0, 26.0) * Box(36.0, 36.0, 3.0),
        "reference_bottom_ESC_right_side",
        "#22262B",
    )


def build_fc(params: P2Parameters = P2_DEFAULTS) -> Shape:
    return _label(
        Pos(0.0, 46.0, 42.0) * Box(30.5, 30.5, 2.0),
        "reference_FC_above_ESC_right_side",
        "#4D5963",
    )


def build_xt60(params: P2Parameters = P2_DEFAULTS) -> Shape:
    body = Pos(0.0, 0.0, params.vertical_endpoint_z + 5.0) * Box(
        15.9,
        8.1,
        20.5,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cups = [
        Pos(x, 0.0, params.vertical_endpoint_z + 2.5) * Cylinder(1.5, 5.0)
        for x in (-4.0, 4.0)
    ]
    return _label(body + cups, "reference_vertical_XT60_above_bend", "#E8B923")


def _fixed_children(params: P2Parameters) -> list[Shape]:
    return [
        build_fixed_plate("left", params),
        build_fixed_plate("right", params),
        build_esc(params),
        build_fc(params),
        build_wires(params),
        build_xt60(params),
    ]


def build_loaded_closed(params: P2Parameters = P2_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            build_pusher(params),
            build_rods(params=params),
            build_esc(params),
            build_fc(params),
            build_wires(params),
            build_xt60(params),
        ],
        label="p2_corner_clamp_three_rod_loaded_closed_12awg_manual_only",
    )


def build_loaded_open(params: P2Parameters = P2_DEFAULTS) -> Compound:
    d = params.withdrawal_component
    pusher = Pos(0.0, d, d) * build_pusher(params)
    pusher.label = "manual_pusher_open_upper_right_11mm_diagonal"
    return Compound(
        children=[
            build_fixed_plate("left", params),
            build_fixed_plate("right", params),
            pusher,
            build_rods(params.moving_open, params),
            build_esc(params),
            build_fc(params),
            build_wires(params),
            build_xt60(params),
        ],
        label="p2_corner_clamp_three_rod_loaded_open_workpiece_visible",
    )


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P2Parameters = P2_DEFAULTS) -> Compound:
    left = _on_bed(build_fixed_plate("left", params), 0.0, 0.0, Rot(0, 90, 0))
    left.label = "print_left_large_fixed_L"
    right = _on_bed(build_fixed_plate("right", params), 50.0, 0.0, Rot(0, 90, 0))
    right.label = "print_right_large_fixed_L"
    pusher = _on_bed(build_pusher(params), 100.0, 0.0, Rot(180, 0, 0))
    pusher.label = "print_one_piece_upper_right_corner_pusher"
    return Compound(
        children=[left, right, pusher],
        label="p2_print_kit_exactly_three_printed_solids",
    )


__all__ = [
    "P2_DEFAULTS",
    "P2Parameters",
    "PointYZ",
    "build_esc",
    "build_fc",
    "build_fixed_plate",
    "build_loaded_closed",
    "build_loaded_open",
    "build_print_kit",
    "build_pusher",
    "build_reference_rod",
    "build_rods",
    "build_wire",
    "build_wire_centerline",
    "build_wires",
    "build_xt60",
    "contact_points",
    "rod_centers",
]

