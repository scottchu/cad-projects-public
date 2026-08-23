"""STEP-first KAGE P3 V2 three-ring comparison geometry."""

from __future__ import annotations

from math import cos, pi, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Face, Location, Plane, Polygon, BuildPart, BuildSketch, extrude
from cadgen import srgb

from p3_v2_three_ring_comparison_spec import P3V2ThreeRingComparisonSpec, P3_V2


def _annulus(inner_radius: float, outer_radius: float, height: float, z0: float):
    outer = Cylinder(outer_radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))
    inner = Cylinder(inner_radius, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0 - 0.2)))
    return outer.cut(inner)


def _frame(spec: P3V2ThreeRingComparisonSpec = P3_V2):
    frame = _annulus(spec.frame_inner_radius, spec.frame_outer_radius, spec.frame_z[1] - spec.frame_z[0], spec.frame_z[0])
    frame.label = "p3_v2_stationary_300mm_reference_frame"
    frame.color = srgb("#D8D0C2")
    return frame


def _pointed_fin(
    radius: float,
    angle: float,
    root_z: float,
    height: float,
    radial_width: float,
    tangential_width: float,
):
    x0 = radius - radial_width / 2.0
    points = ((x0, root_z), (x0 + radial_width, root_z), (radius, root_z + height))
    with BuildPart() as builder:
        with BuildSketch(Plane.XZ):
            Polygon(*points)
        extrude(amount=tangential_width / 2.0, both=True)
    return builder.part.rotate(Axis.Z, angle)


def _radial_root_arm(
    fin_radius: float,
    carrier_radius: float,
    carrier_inner_radius: float,
    angle: float,
    z0: float,
    tangential_width: float,
    spec: P3V2ThreeRingComparisonSpec,
):
    if abs(fin_radius - carrier_radius) < 1e-9:
        return None
    outer_radius = carrier_inner_radius + spec.root_arm_carrier_overlap
    inner_radius = fin_radius
    length = outer_radius - inner_radius
    arm = Box(
        length,
        tangential_width,
        spec.root_arm_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((inner_radius + outer_radius) / 2.0, 0.0, z0)))
    return arm.rotate(Axis.Z, angle)


def _carrier_with_fin(
    role_index: int,
    carrier_radius: float,
    fin_radius: float,
    z0: float,
    spec: P3V2ThreeRingComparisonSpec = P3_V2,
):
    half_width = spec.carrier_radial_width / 2.0
    carrier = _annulus(
        carrier_radius - half_width,
        carrier_radius + half_width,
        spec.carrier_thickness,
        z0,
    )
    fin = _pointed_fin(
        fin_radius,
        spec.display_angles[role_index],
        z0 + spec.carrier_thickness - spec.fin_root_sink,
        spec.fin_heights[role_index],
        spec.fin_radial_width,
        spec.fin_tangential_widths[role_index],
    )
    arm = _radial_root_arm(
        fin_radius,
        carrier_radius,
        carrier_radius - half_width,
        spec.display_angles[role_index],
        z0 + spec.carrier_thickness - spec.root_arm_thickness,
        spec.fin_tangential_widths[role_index],
        spec,
    )
    body = carrier.fuse(fin) if arm is None else carrier.fuse(arm).fuse(fin)
    role = spec.roles[role_index]
    body.label = f"p3_v2_{role}_carrier_and_staggered_fin"
    body.color = srgb(spec.role_colors[role_index])
    return body


def make_stacked_three_ring(spec: P3V2ThreeRingComparisonSpec = P3_V2):
    children = [_frame(spec)]
    for index, (z0, fin_radius) in enumerate(zip(spec.stacked_z_starts, spec.stacked_fin_radii)):
        children.append(_carrier_with_fin(index, spec.stacked_carrier_radius, fin_radius, z0, spec))
    return Compound(children=children, label="p3_v2_axially_stacked_three_ring_visualization")


def make_concentric_three_ring(spec: P3V2ThreeRingComparisonSpec = P3_V2):
    children = [_frame(spec)]
    for index, carrier_radius in enumerate(spec.concentric_carrier_radii):
        children.append(_carrier_with_fin(index, carrier_radius, carrier_radius, spec.concentric_z, spec))
    return Compound(children=children, label="p3_v2_radially_extended_three_ring_visualization")


def make_side_by_side_comparison(spec: P3V2ThreeRingComparisonSpec = P3_V2):
    stacked = make_stacked_three_ring(spec).moved(Location((-170.0, 0.0, 0.0)))
    stacked.label = "p3_v2_left_axially_stacked"
    concentric = make_concentric_three_ring(spec).moved(Location((170.0, 0.0, 0.0)))
    concentric.label = "p3_v2_right_radially_extended"
    return Compound(children=[stacked, concentric], label="p3_v2_three_ring_architecture_comparison")


THREE_RING_FACTORIES = (
    ("stacked_three_ring", make_stacked_three_ring),
    ("concentric_three_ring", make_concentric_three_ring),
    ("side_by_side_comparison", make_side_by_side_comparison),
)
