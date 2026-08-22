"""STEP-first geometry for the P3 V3 stacked three-motor KAGE prototype."""

from __future__ import annotations

from math import cos, pi, sin

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cone,
    Cylinder,
    Face,
    Location,
    Plane,
    Polygon,
    Vector,
    Wire,
    BuildPart,
    BuildSketch,
    extrude,
)
from cadgen import srgb

from p3_v3_stacked_three_motor_90deg_spec import P3V3StackedThreeMotor90DegSpec, P3_V3


def _polar(radius: float, angle_degrees: float) -> tuple[float, float]:
    angle = angle_degrees * pi / 180.0
    return radius * cos(angle), radius * sin(angle)


def _annulus(inner: float, outer: float, height: float, z0: float):
    outside = Cylinder(outer, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0)))
    inside = Cylinder(inner, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, z0 - 0.2)))
    return outside.cut(inside)


def _internal_tooth_wire(spec: P3V3StackedThreeMotor90DegSpec):
    pitch = 2.0 * pi / spec.internal_gear_teeth
    half_pitch = pitch / 2.0
    tip_half = spec.internal_material_tooth_thickness / (2.0 * spec.internal_pitch_radius)
    points = []
    for tooth in range(spec.internal_gear_teeth):
        center = tooth * pitch
        stations = (
            (center - half_pitch, spec.internal_root_radius),
            (center - 1.6 * tip_half, spec.internal_root_radius),
            (center - tip_half, spec.internal_tip_radius),
            (center + tip_half, spec.internal_tip_radius),
            (center + 1.6 * tip_half, spec.internal_root_radius),
            (center + half_pitch, spec.internal_root_radius),
        )
        points.extend(Vector(radius * cos(angle), radius * sin(angle), 0.0) for angle, radius in stations)
    # Inner wires run opposite the outer circular boundary.
    return Wire.make_polygon(list(reversed(points)), close=True)


def make_internal_gear_carrier(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    z0, z1 = spec.carrier_layers[role_index]
    outer = Wire.make_circle(spec.carrier_radii[1])
    face = Face(outer, [_internal_tooth_wire(spec)])
    carrier = extrude(face, amount=z1 - z0).moved(Location((0, 0, z0)))
    role = spec.roles[role_index]
    carrier.label = f"p3_v3_{role}_259T_internal_gear_carrier"
    carrier.color = srgb(spec.role_colors[role_index])
    return carrier


def _upright_fin(role_index: int, spec: P3V3StackedThreeMotor90DegSpec):
    """Constant-section stalk/blade from its carrier root to the optical tip.

    The previous full-height triangle made the bottom and middle fins look as
    though they leaned across the radial lanes.  This vertical prism preserves
    the exact 1.20 mm radial lane and the role-specific tangential width over
    its complete height.  The physical shadow test can later justify a small
    rounded cap without changing the frozen optical tip plane.
    """

    radius = spec.fin_lane_centers[role_index]
    base = (
        spec.direct_top_fin_base_z
        if role_index == spec.direct_top_fin_role
        else spec.fin_bases[role_index]
    )
    tip = spec.fin_tip_zs[role_index]
    fin = Box(
        spec.fin_radial_width,
        spec.fin_tangential_widths[role_index],
        tip - base,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((radius, 0.0, base)))
    return fin.rotate(Axis.Z, spec.display_fin_angles[role_index])


def _root_arm(role_index: int, spec: P3V3StackedThreeMotor90DegSpec):
    if role_index == spec.direct_top_fin_role:
        raise ValueError("the top fin mounts directly to its carrier and has no root arm")
    outer = spec.fin_lane_centers[role_index]
    inner = spec.root_arm_inner_radius
    arm = Box(
        outer - inner,
        spec.fin_tangential_widths[role_index],
        spec.root_arm_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((inner + outer) / 2.0, 0.0, spec.fin_bases[role_index])))
    return arm.rotate(Axis.Z, spec.display_fin_angles[role_index])


def make_carrier_with_fin(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    carrier = make_internal_gear_carrier(role_index, spec)
    fin = _upright_fin(role_index, spec)
    if role_index == spec.direct_top_fin_role:
        body = carrier.fuse(fin)
        mount = "DIRECT_TOP_OUTER_BAND"
    else:
        body = carrier.fuse(_root_arm(role_index, spec)).fuse(fin)
        mount = "OUTBOARD_ROOT_ARM"
    role = spec.roles[role_index]
    body.label = f"p3_v3_{role}_carrier_fin_{mount}"
    body.color = srgb(spec.role_colors[role_index])
    return body


def make_frame(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    frame = _annulus(spec.frame_radii[0], spec.frame_radii[1], spec.frame_z[1] - spec.frame_z[0], spec.frame_z[0])
    frame.label = "p3_v3_stationary_300mm_reference_frame"
    frame.color = srgb("#D8D0C2")
    return frame


def make_motor_body(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    length = spec.motor_face_radius - spec.motor_inward_radius
    body = Box(
        length,
        spec.motor_keepout[0],
        spec.motor_keepout[1],
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((spec.motor_inward_radius, 0.0, spec.motor_body_z[0])))
    body = body.rotate(Axis.Z, spec.motor_station_angles[role_index])
    body.label = f"p3_v3_{spec.roles[role_index]}_NEMA8_20p6x20p6x39p3_PROVISIONAL"
    body.color = srgb("#4B5054")
    return body


def make_motor_shaft(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    shaft = Cylinder(
        spec.motor_shaft_diameter / 2.0,
        spec.motor_shaft_length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90).moved(
        Location(((spec.motor_face_radius + spec.output_axis_radius) / 2.0, 0.0, spec.motor_shaft_center_z))
    ).rotate(Axis.Z, spec.motor_station_angles[role_index])
    # Preserve the purchased 10 mm shaft envelope, but remove the impossible
    # material at the orthogonal output-shaft junction.  The remaining shaft
    # seats inside the bored horizontal bevel envelope without crossing the
    # vertical output shaft.
    x, y = _polar(spec.output_axis_radius, spec.motor_station_angles[role_index])
    vertical_keepout = Cylinder(
        spec.output_shaft_diameter / 2.0 + spec.shaft_envelope_clearance,
        spec.motor_shaft_diameter + 4.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((x, y, spec.motor_shaft_center_z)))
    shaft = shaft.cut(vertical_keepout)
    shaft.label = f"p3_v3_{spec.roles[role_index]}_motor_radial_shaft_TRUNCATED_AT_JUNCTION"
    shaft.color = srgb("#B7BCC0")
    return shaft


def _bevel_envelope(horizontal: bool, spec: P3V3StackedThreeMotor90DegSpec):
    gear = Cone(
        spec.miter_envelope_radius,
        spec.miter_envelope_radius * 0.45,
        spec.miter_face_width,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    bore = Cylinder(
        spec.output_shaft_diameter / 2.0 + spec.shaft_envelope_clearance,
        spec.miter_face_width + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    gear = gear.cut(bore)
    if horizontal:
        gear = gear.rotate(Axis.Y, 90).moved(Location((spec.output_axis_radius - spec.miter_face_width / 2.0, 0.0, spec.motor_shaft_center_z)))
    else:
        gear = gear.moved(Location((spec.output_axis_radius, 0.0, spec.motor_shaft_center_z + spec.miter_face_width / 2.0)))
    return gear


def make_miter_pair(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    angle = spec.motor_station_angles[role_index]
    horizontal = _bevel_envelope(True, spec)
    vertical = _bevel_envelope(False, spec)
    # Remove the perpendicular shaft corridors from the opposite gear.  Then
    # partition the two provisional pitch envelopes so they meet at a shared
    # contact boundary instead of occupying the same material volume.
    vertical_output_keepout = Cylinder(
        spec.output_shaft_diameter / 2.0 + spec.shaft_envelope_clearance,
        spec.miter_envelope_radius * 3.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((spec.output_axis_radius, 0.0, spec.motor_shaft_center_z)))
    radial_shaft_keepout = Cylinder(
        spec.motor_shaft_diameter / 2.0 + spec.shaft_envelope_clearance,
        spec.motor_shaft_length + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(
        Location(((spec.motor_face_radius + spec.output_axis_radius) / 2.0, 0.0, spec.motor_shaft_center_z))
    )
    horizontal = horizontal.cut(vertical_output_keepout)
    vertical = vertical.cut(radial_shaft_keepout)
    horizontal = horizontal.cut(vertical)
    horizontal = horizontal.rotate(Axis.Z, angle)
    vertical = vertical.rotate(Axis.Z, angle)
    role = spec.roles[role_index]
    horizontal.label = f"p3_v3_{role}_10T_horizontal_miter_ENVELOPE"
    vertical.label = f"p3_v3_{role}_10T_vertical_miter_ENVELOPE"
    horizontal.color = vertical.color = srgb("#D6A64B")
    return horizontal, vertical


def make_output_shaft(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    x, y = _polar(spec.output_axis_radius, spec.motor_station_angles[role_index])
    shaft = Cylinder(
        spec.output_shaft_diameter / 2.0,
        spec.output_shaft_z[1] - spec.output_shaft_z[0],
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, spec.output_shaft_z[0])))
    shaft.label = f"p3_v3_{spec.roles[role_index]}_vertical_output_shaft_keepout"
    shaft.color = srgb("#B7BCC0")
    return shaft


def _external_pinion_wire(spec: P3V3StackedThreeMotor90DegSpec):
    pitch = 2.0 * pi / spec.pinion_teeth
    half_pitch = pitch / 2.0
    tooth_half = spec.internal_material_tooth_thickness / (2.0 * spec.pinion_pitch_radius)
    points = []
    for tooth in range(spec.pinion_teeth):
        center = tooth * pitch
        stations = (
            (center - half_pitch, spec.pinion_root_radius),
            (center - 1.35 * tooth_half, spec.pinion_root_radius),
            (center - tooth_half, spec.pinion_outer_radius),
            (center + tooth_half, spec.pinion_outer_radius),
            (center + 1.35 * tooth_half, spec.pinion_root_radius),
            (center + half_pitch, spec.pinion_root_radius),
        )
        points.extend(Vector(radius * cos(angle), radius * sin(angle), 0.0) for angle, radius in stations)
    return Wire.make_polygon(points, close=True)


def make_pinion(role_index: int, spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    layer = spec.carrier_layers[role_index]
    z0 = (layer[0] + layer[1] - spec.pinion_face_width) / 2.0
    pinion = extrude(Face(_external_pinion_wire(spec)), amount=spec.pinion_face_width).moved(Location((0, 0, z0)))
    bore = Cylinder(
        spec.pinion_bore_radius,
        spec.pinion_face_width + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, z0 - 0.2)))
    pinion = pinion.cut(bore)
    x, y = _polar(spec.output_axis_radius, spec.motor_station_angles[role_index])
    pinion = pinion.rotate(Axis.Z, spec.pinion_phase_angles[role_index]).moved(Location((x, y, 0.0)))
    # These are explicit contact-envelope teeth, not a claim of manufacturing
    # involute performance.  Trim the visualization against its own carrier to
    # enforce a disjoint, zero-volume mesh interface.
    pinion = pinion.cut(make_internal_gear_carrier(role_index, spec))
    pinion.label = f"p3_v3_{spec.roles[role_index]}_12T_vertical_pinion"
    pinion.color = srgb("#D6A64B")
    return pinion


def make_bearing_plate(z_range: tuple[float, float], spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    z0, z1 = z_range
    plate = _annulus(spec.bearing_plate_radii[0], spec.bearing_plate_radii[1], z1 - z0, z0)
    for angle in spec.motor_station_angles:
        x, y = _polar(spec.output_axis_radius, angle)
        plate = plate.cut(Cylinder(spec.bearing_outer_radius + 0.2, z1 - z0 + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0 - 0.2))))
    plate.label = f"p3_v3_stationary_bearing_support_plate_z{z0:g}"
    plate.color = srgb("#8F969B")
    return plate


def make_bearing(role_index: int, z_range: tuple[float, float], spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    x, y = _polar(spec.output_axis_radius, spec.motor_station_angles[role_index])
    bearing = _annulus(spec.bearing_bore_radius, spec.bearing_outer_radius, z_range[1] - z_range[0], z_range[0]).moved(Location((x, y, 0.0)))
    bearing.label = f"p3_v3_{spec.roles[role_index]}_bearing_reference_z{z_range[0]:g}"
    bearing.color = srgb("#6E7478")
    return bearing


def make_rear_mount(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    mount = _annulus(68.0, 130.0, 2.0, spec.rear_plane_z)
    mount.label = "p3_v3_rear_mount_reference_plane_z_minus25p5"
    mount.color = srgb("#9AA0A3")
    return mount


def make_assembled(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    children = [
        make_frame(spec),
        make_rear_mount(spec),
        make_bearing_plate(spec.lower_bearing_support_z, spec),
        make_bearing_plate(spec.upper_bearing_support_z, spec),
        *(make_carrier_with_fin(i, spec) for i in range(3)),
    ]
    for index in range(3):
        children.extend((make_motor_body(index, spec), make_motor_shaft(index, spec)))
        children.extend(make_miter_pair(index, spec))
        children.append(make_output_shaft(index, spec))
        children.append(make_pinion(index, spec))
        children.append(make_bearing(index, spec.lower_bearing_support_z, spec))
        children.append(make_bearing(index, spec.upper_bearing_support_z, spec))
    return Compound(children=children, label="p3_v3_preferred_stacked_three_motor_90deg_assembly")


def make_transmission_exploded(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    children = []
    for index in range(3):
        angle = spec.motor_station_angles[index]
        radial_shift = Location((*_polar(-24.0, angle), -8.0))
        children.append(make_motor_body(index, spec).moved(radial_shift))
        children.append(make_motor_shaft(index, spec))
        horizontal, vertical = make_miter_pair(index, spec)
        children.append(horizontal)
        children.append(vertical.moved(Location((0, 0, 6.0))))
        children.append(make_output_shaft(index, spec).moved(Location((0, 0, 12.0))))
        children.append(make_pinion(index, spec).moved(Location((0, 0, 20.0))))
    return Compound(children=children, label="p3_v3_three_station_motor_transmission_exploded")


def make_fins_rings_closeup(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    return Compound(
        children=[make_frame(spec), *(make_carrier_with_fin(i, spec) for i in range(3))],
        label="p3_v3_stacked_259T_rings_and_outboard_fins_closeup",
    )


def make_coincident_fins_closeup(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    """Put all three fins at the same clock angle to expose radial lane gaps."""

    children = [make_frame(spec)]
    for role_index in range(3):
        body = make_carrier_with_fin(role_index, spec).rotate(
            Axis.Z, -spec.display_fin_angles[role_index]
        )
        body.label = f"p3_v3_{spec.roles[role_index]}_carrier_fin_COINCIDENT_ANGLE"
        children.append(body)
    return Compound(children=children, label="p3_v3_coincident_fin_lane_clearance_closeup")


def make_axial_side_section(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    # A local drive-station section is materially easier to read than a full
    # 300 mm diameter slice: retain the complete Z stack and the angle-0 motor
    # while cropping the empty opposite half of the clock.
    slab = Box(100.0, 0.6, 80.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(
        Location((105.0, 0.0, -2.0))
    )
    children = []
    for child in make_assembled(spec).children:
        for fragment in child.intersect(slab) or []:
            if fragment.volume > 1e-8:
                fragment.label = f"{child.label}_section"
                fragment.color = child.color
                children.append(fragment)
    return Compound(children=children, label="p3_v3_angle0_axial_side_section")


def make_gear_mesh_coupon(spec: P3V3StackedThreeMotor90DegSpec = P3_V3):
    gear = make_internal_gear_carrier(0, spec)
    coupon_box = Box(22.0, 38.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((128.5, 0.0, 2.3)))
    ring_fragments = gear.intersect(coupon_box)
    ring_segment = Compound(list(ring_fragments))
    ring_segment.label = "p3_v3_coupon_259T_internal_gear_segment"
    ring_segment.color = srgb(spec.role_colors[0])
    pinion = make_pinion(0, spec)
    pinion.label = "p3_v3_coupon_12T_pinion"
    return Compound(children=[ring_segment, pinion], label="p3_v3_m1_259T_12T_mesh_coupon_100_cycle_gate")


def positive_intersection_volume(a, b) -> float:
    total = 0.0
    for sa in a.solids():
        for sb in b.solids():
            total += sum(max(0.0, float(piece.volume)) for piece in (sa.intersect(sb) or []))
    return total


PRIMARY_FACTORIES = (
    ("assembled", make_assembled),
    ("transmission_exploded", make_transmission_exploded),
    ("axial_side_section", make_axial_side_section),
    ("fins_rings_closeup", make_fins_rings_closeup),
    ("coincident_fins_closeup", make_coincident_fins_closeup),
    ("gear_mesh_coupon", make_gear_mesh_coupon),
)
