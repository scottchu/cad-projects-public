"""P9 minimal four-disc / three-rod motion proof.

There are exactly four principal plates: one fixed circular guide disc and one
rotating circular cam disc at each rod end.  The inverse slots preserve the P7
0..70 degree closing law and 70..80 degree dwell.  P9 deliberately adds no
frame, cage, spider, linkage, gearing, or cosmetic enclosure.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, hypot, pi, radians, sin
from typing import Literal

from build123d import Align, Box, Compound, Cylinder, Pos, Rot, Shape, Sphere
from cadgen import srgb

from xt60_bend_jig.p2_corner_clamp import PointYZ, build_wires as _p2_build_wires, build_xt60 as _p2_build_xt60
from xt60_bend_jig.p7_three_rod_scroll import (
    P7Parameters, _rotate_about_shaft,
    _straight_slot_solid_x, _x_cylinder, _x_hex_prism,
    build_cap as _p7_build_cap, inverse_slot_point, rod_center, slot_path,
    smoothstep01, travel_at_angle,
)


RodName = Literal["upright", "bottom", "diagonal"]
Side = Literal["left", "right"]
ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")


@dataclass(frozen=True, slots=True)
class P9Parameters(P7Parameters):
    # Dense path sampling proves that the requested 52 mm / (-1.113,28.887)
    # combination merges two 4.4 mm cam slots and puts the shaft through the
    # XT60 removal prism.  The audited P7 datum with a 64 mm circle preserves
    # 2.015 mm inter-slot web, 3.498 mm outer rim, and shaft-corridor clearance.
    shaft_y: float = -7.5
    shaft_z: float = 32.5
    scroll_diameter: float = 64.0
    fixed_plate_thickness: float = 3.0
    scroll_plate_thickness: float = 2.5
    clear_span: float = 32.0
    scroll_axial_clearance: float = 0.30
    guide_slot_width: float = 4.4
    scroll_slot_width: float = 4.4
    clamp_flat_width_y: float = 18.0
    clamp_flat_height_z: float = 4.0
    lock_radius: float = 15.5
    lock_local_angle_deg: float = 200.0


P9_DEFAULTS = P9Parameters()


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def lock_local_point(params: P9Parameters = P9_DEFAULTS) -> PointYZ:
    angle = radians(params.lock_local_angle_deg)
    return PointYZ(
        params.shaft_y + params.lock_radius * cos(angle),
        params.shaft_z + params.lock_radius * sin(angle),
    )


def lock_world_point(params: P9Parameters = P9_DEFAULTS) -> PointYZ:
    local = lock_local_point(params)
    dy, dz = local.y - params.shaft_y, local.z - params.shaft_z
    angle = radians(params.end_angle)
    return PointYZ(
        params.shaft_y + cos(angle) * dy - sin(angle) * dz,
        params.shaft_z + sin(angle) * dy + cos(angle) * dz,
    )


def _disc(x: float, thickness: float, params: P9Parameters) -> Shape:
    return _x_cylinder(params.scroll_diameter, thickness, x, params.shaft_y, params.shaft_z)


def build_cam_slot_tool(
    name: RodName,
    side: Side = "right",
    params: P9Parameters = P9_DEFAULTS,
    extra_depth: float = 2.0,
) -> Compound:
    """True swept polyline slot as overlapping capsules, never a closed fill.

    P7's generic polygon-offset helper closes a curved polyline and can fill
    the region between its endpoints.  That is unacceptable here because it
    merges nominally separated holes.  A compound of consecutive capsules is
    the actual 4.4 mm swept slot and preserves the measured webs.
    """
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.scroll_plate_center_x
    depth = params.scroll_plate_thickness + extra_depth
    points = slot_path(name, params)
    return Compound(children=[
        _straight_slot_solid_x(a, b, params.scroll_slot_width, x, depth)
        for a, b in zip(points, points[1:])
    ], label=f"{side}_{name}_actual_4p4_inverse_cam_slot_tool")


def build_fixed_disc(side: Side, params: P9Parameters = P9_DEFAULTS) -> Shape:
    """Plain circular guide plate with three straight slots and one tiny flat."""
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.fixed_plate_center_x
    depth = params.fixed_plate_thickness
    disc = _disc(x, depth, params)
    # Integral bottom clamp flat, fused to the circle; it is not another part.
    bottom = params.shaft_z - params.scroll_diameter / 2.0
    flat = Pos(x, params.shaft_y, bottom + 1.0) * Box(
        depth, params.clamp_flat_width_y, params.clamp_flat_height_z,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    tools: list[Shape] = []
    for name in ROD_NAMES:
        tools.append(_straight_slot_solid_x(
            rod_center(name, 0.0, params), rod_center(name, params.end_angle, params),
            params.guide_slot_width, x, depth + 2.0,
        ))
    tools.append(_x_cylinder(params.shaft_bore_diameter, depth + 2.0, x, params.shaft_y, params.shaft_z))
    lock = lock_world_point(params)
    tools.append(_x_cylinder(params.end_lock_pin_diameter + 0.2, depth + 2.0, x, lock.y, lock.z))
    return _label(disc + flat - tools, f"{side}_fixed_plain_circular_guide_disc_three_straight_slots", "#3E7151")


def build_cam_disc(side: Side, params: P9Parameters = P9_DEFAULTS) -> Shape:
    """Plain circular rotating plate with the three calculated inverse slots."""
    if side not in ("left", "right"):
        raise ValueError("side must be left or right")
    sign = -1.0 if side == "left" else 1.0
    x = sign * params.scroll_plate_center_x
    depth = params.scroll_plate_thickness
    tools: list[Shape] = [build_cam_slot_tool(name, side, params) for name in ROD_NAMES]
    tools.append(_x_hex_prism(
        params.scroll_hex_socket_across_corners, depth + 2.0, x, params.shaft_y, params.shaft_z))
    lock = lock_local_point(params)
    tools.append(_x_cylinder(params.end_lock_pin_diameter + 0.2, depth + 2.0, x, lock.y, lock.z))
    return _label(_disc(x, depth, params) - tools,
                  f"{side}_rotating_plain_circular_cam_disc_three_inverse_slots", "#D69B16")


def build_principal_plates(angle_deg: float, params: P9Parameters = P9_DEFAULTS) -> Compound:
    return Compound(children=[
        build_fixed_disc("left", params),
        _rotate_about_shaft(build_cam_disc("left", params), angle_deg, params),
        build_fixed_disc("right", params),
        _rotate_about_shaft(build_cam_disc("right", params), angle_deg, params),
    ], label="exactly_four_principal_discs_two_fixed_two_synchronized_rotating")


def build_rod(name: RodName, angle_deg: float, params: P9Parameters = P9_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, params)
    return _label(_x_cylinder(params.rod_diameter, params.rod_length, 0.0, point.y, point.z),
                  f"purchased_304_stainless_{name}_rod_4x50", "#BEC7CC")


def build_rods(angle_deg: float, params: P9Parameters = P9_DEFAULTS) -> Compound:
    return Compound(children=[build_rod(name, angle_deg, params) for name in ROD_NAMES],
                    label=f"exactly_three_purchased_4x50_rods_at_{angle_deg:g}deg")


def build_cap(side: Side, point: PointYZ, params: P9Parameters = P9_DEFAULTS) -> Shape:
    cap = _p7_build_cap(side, point, params)
    cap.label = ("left_3p90_press_fit_trial_retainer_requires_print_test" if side == "left" else
                 "right_4p10_keeper_3p60_snap_throat_requires_print_test")
    return cap


def build_caps(angle_deg: float, params: P9Parameters = P9_DEFAULTS) -> Compound:
    parts: list[Shape] = []
    for name in ROD_NAMES:
        point = rod_center(name, angle_deg, params)
        parts.extend((build_cap("left", point, params), build_cap("right", point, params)))
    return Compound(children=parts, label="six_simple_rod_retainers")


def build_keyed_shaft(angle_deg: float, params: P9Parameters = P9_DEFAULTS) -> Shape:
    main = _x_hex_prism(params.shaft_diameter, 47.0, 0.0, params.shaft_y, params.shaft_z)
    head = _x_cylinder(9.0, 2.0, 24.5, params.shaft_y, params.shaft_z)
    return _label(_rotate_about_shaft(main + head, angle_deg, params),
                  "single_shared_keyed_shaft_with_integral_right_head", "#262B2D")


def build_lock_pin(params: P9Parameters = P9_DEFAULTS) -> Shape:
    point = lock_world_point(params)
    shaft = _x_cylinder(params.end_lock_pin_diameter, 10.0, 20.0, point.y, point.z)
    head = _x_cylinder(5.5, 2.0, 26.0, point.y, point.z)
    return _label(shaft + head, "single_optional_indexed_3mm_lock_pin_exact_80deg", "#9B3434")


def build_esc_pad_references() -> Compound:
    esc = _label(Pos(0.0, 46.0, 25.75) * Box(
        36.0, 36.0, 3.5, align=(Align.CENTER, Align.CENTER, Align.CENTER)),
        "reference_bottom_ESC", "#24282A")
    fc = _label(Pos(0.0, 46.0, 42.0) * Box(
        30.5, 30.5, 2.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)),
        "reference_FC_above_ESC", "#4D5963")
    children: list[Shape] = [esc, fc]
    for x, name in ((-4.0, "negative"), (4.0, "positive")):
        pad = Pos(x, 30.5, 27.675) * Box(5.0, 5.0, 0.35, align=(Align.CENTER, Align.CENTER, Align.CENTER))
        solder = Pos(x, 28.0, 28.2) * Sphere(2.2)
        children.extend((
            _label(pad, f"copper_{name}_pad_top_Z27p85", "#D7982D"),
            _label(solder, f"solder_reference_{name}", "#BFC5C7"),
        ))
    return Compound(children=children, label="reference_ESC_FC_two_copper_pads_and_solder")


def build_closed_workpiece() -> Compound:
    wires = _p2_build_wires()
    wires.label = "physical_closed_two_12AWG_44mm_R6_exact_90deg_leads"
    xt60 = _p2_build_xt60()
    xt60.label = "reference_closed_vertical_XT60"
    return Compound(children=[build_esc_pad_references(), wires, xt60],
                    label="closed_reference_bottom_ESC_horizontal_R6_vertical_XT60")


def build_open_xt60_removal_reference() -> Shape:
    return _label(Pos(0.0, 0.0, 44.25) * Box(
        15.9, 8.1, 20.5, align=(Align.CENTER, Align.CENTER, Align.CENTER)),
        "reference_XT60_vertical_open_removal_corridor", "#E8B923")


def build_loaded(angle_deg: float, params: P9Parameters = P9_DEFAULTS) -> Compound:
    children: list[Shape] = [*build_principal_plates(angle_deg, params).children,
                             *build_rods(angle_deg, params).children,
                             *build_caps(angle_deg, params).children,
                             build_keyed_shaft(angle_deg, params)]
    if abs(angle_deg - params.end_angle) <= 1e-9:
        children.extend((build_lock_pin(params), build_closed_workpiece()))
    elif abs(angle_deg) <= 1e-9:
        children.append(build_open_xt60_removal_reference())
    return Compound(children=children, label=f"p9_minimal_four_disc_three_rod_loaded_{angle_deg:g}deg")


def build_loaded_open(params: P9Parameters = P9_DEFAULTS) -> Compound:
    return build_loaded(0.0, params)


def build_loaded_closed(params: P9Parameters = P9_DEFAULTS) -> Compound:
    return build_loaded(params.end_angle, params)


def build_exploded(params: P9Parameters = P9_DEFAULTS) -> Compound:
    # Ordered exactly left-to-right as the physical stack is assembled.
    children: list[Shape] = []
    for index, name in enumerate(ROD_NAMES):
        point = rod_center(name, 0.0, params)
        children.append(Pos(-24.0, 0.0, index * 7.0) * build_cap("left", point, params))
    children.extend((
        Pos(-16.0, 0.0, 0.0) * build_cam_disc("left", params),
        Pos(-8.0, 0.0, 0.0) * build_fixed_disc("left", params),
    ))
    for index, name in enumerate(ROD_NAMES):
        children.append(Pos(0.0, 0.0, 16.0 + index * 7.0) * build_rod(name, 0.0, params))
    children.extend((
        Pos(8.0, 0.0, 0.0) * build_fixed_disc("right", params),
        Pos(16.0, 0.0, 0.0) * build_cam_disc("right", params),
    ))
    for index, name in enumerate(ROD_NAMES):
        point = rod_center(name, 0.0, params)
        children.append(Pos(24.0, 0.0, index * 7.0) * build_cap("right", point, params))
    children.extend((
        Pos(0.0, -10.0, -16.0) * build_keyed_shaft(0.0, params),
        Pos(12.0, -10.0, -16.0) * build_lock_pin(params),
    ))
    return Compound(children=children, label="p9_exploded_left_retainers_cam_fixed_rods_fixed_cam_right_retainers_shaft_lock")


def _on_bed(shape: Shape, x: float, y: float, rotation: Rot | None = None) -> Shape:
    oriented = rotation * shape if rotation is not None else shape
    bounds = oriented.bounding_box()
    return Pos(x - bounds.min.X, y - bounds.min.Y, -bounds.min.Z) * oriented


def build_print_kit(params: P9Parameters = P9_DEFAULTS) -> Compound:
    parts: list[Shape] = [
        _on_bed(build_fixed_disc("left", params), 0.0, 0.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_cam_disc("left", params), 70.0, 0.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_fixed_disc("right", params), 0.0, 70.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_cam_disc("right", params), 70.0, 70.0, Rot(0.0, 90.0, 0.0)),
        _on_bed(build_keyed_shaft(0.0, params), 140.0, 0.0, Rot(0.0, 90.0, 0.0)),
    ]
    origin = PointYZ(0.0, 0.0)
    for index in range(3):
        parts.extend((
            _on_bed(build_cap("left", origin, params), 158.0 + index * 11.0, 0.0, Rot(0.0, 90.0, 0.0)),
            _on_bed(build_cap("right", origin, params), 158.0 + index * 11.0, 13.0, Rot(0.0, 90.0, 0.0)),
        ))
    parts.append(_on_bed(build_lock_pin(params), 195.0, 0.0, Rot(0.0, 90.0, 0.0)))
    for index, part in enumerate(parts):
        part.label = f"print_{index:02d}_{part.label}"
    return Compound(children=parts, label="p9_print_kit_four_discs_shaft_six_retainers_one_lock_pin")


__all__ = [
    "P9_DEFAULTS", "P9Parameters", "build_cam_disc", "build_cam_slot_tool", "build_cap",
    "build_caps", "build_closed_workpiece", "build_esc_pad_references",
    "build_exploded", "build_fixed_disc", "build_keyed_shaft", "build_loaded",
    "build_loaded_closed", "build_loaded_open", "build_lock_pin",
    "build_open_xt60_removal_reference", "build_principal_plates",
    "build_print_kit", "build_rod", "build_rods", "inverse_slot_point",
    "lock_local_point", "lock_world_point", "rod_center", "slot_path",
    "smoothstep01", "travel_at_angle",
]
