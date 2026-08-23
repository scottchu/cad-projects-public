"""STEP-first P3 V1 six-lobe PETG/TPU wheel geometry and assembly."""

from __future__ import annotations

from math import cos, pi, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Face, Location, Vector, Wire, extrude
from cadgen import srgb

from p3_v0_motor_outer_ring_spec import P3_V0
from p3_v0_motor_outer_ring_geometry import (
    make_carrier_segment,
    make_frame_quadrant,
    make_frame_splice_plate,
    make_hall_bracket,
    make_hall_module_reference,
    make_hall_spacer_pad,
    make_motor_slide_cradle,
    make_official_motor_reference,
    placed_joint_key,
)
from p3_v1_motor_outer_ring_multimaterial_spec import (
    P3V1MotorOuterRingMultimaterialSpec,
    P3_V1,
)


def _polar(radius: float, angle_degrees: float) -> tuple[float, float]:
    angle = angle_degrees * pi / 180.0
    return radius * cos(angle), radius * sin(angle)


def _cylinder(radius: float, height: float, z0: float):
    return Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    )


def _lobed_prism(
    crest_radius: float,
    valley_radius: float,
    z0: float,
    height: float,
    spec: P3V1MotorOuterRingMultimaterialSpec,
):
    count = spec.lobe_count * spec.lobe_samples_per_lobe
    midpoint = (crest_radius + valley_radius) / 2.0
    amplitude = (crest_radius - valley_radius) / 2.0
    points = []
    for index in range(count):
        theta = 2.0 * pi * index / count
        radius = midpoint + amplitude * cos(spec.lobe_count * theta)
        points.append(Vector(radius * cos(theta), radius * sin(theta), 0.0))
    face = Face(Wire.make_polygon(points, close=True))
    return extrude(face, amount=height).moved(Location((0.0, 0.0, z0)))


def lobe_interface_radius(
    theta_radians: float,
    crest_radius: float,
    valley_radius: float,
    spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1,
) -> float:
    midpoint = (crest_radius + valley_radius) / 2.0
    amplitude = (crest_radius - valley_radius) / 2.0
    return midpoint + amplitude * cos(spec.lobe_count * theta_radians)


def make_drive_split_tool(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    return Box(
        3.6,
        0.6,
        spec.wheel_width + 0.4,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((2.0, 0.0, spec.drive_z[0] - 0.2)))


def make_drive_pinch_tool(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    return Cylinder(
        P3_V0.drive_pinch_hole_diameter / 2.0,
        10.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.X, 90).moved(
        Location((4.0, -5.2, spec.drive_z[0] + spec.wheel_width / 2.0))
    )


def _wheel_material_pair(
    *,
    role: str,
    z0: float,
    contact_radius: float,
    crest_radius: float,
    valley_radius: float,
    bore_diameter: float,
    spec: P3V1MotorOuterRingMultimaterialSpec,
):
    center_z0 = z0 + spec.center_z_local[0]
    center_height = spec.center_width
    # The rigid hub keeps a valley-radius core through the full width.  Its
    # six-lobe center grows outward only between the two end-lock bands.
    # This leaves annular TPU lips from valley -> contact radius at both ends,
    # so the flexible tread is mechanically captured in Z instead of being a
    # center-only sleeve that could peel off axially.
    core = _cylinder(valley_radius, spec.wheel_width, z0)
    lobed_center = _lobed_prism(crest_radius, valley_radius, center_z0, center_height, spec)
    petg = core.fuse(lobed_center)

    lower_lip = _cylinder(contact_radius, spec.end_band_width, z0).cut(
        _cylinder(valley_radius, spec.end_band_width, z0)
    )
    upper_lip = _cylinder(
        contact_radius,
        spec.end_band_width,
        z0 + spec.center_z_local[1],
    ).cut(
        _cylinder(
            valley_radius,
            spec.end_band_width,
            z0 + spec.center_z_local[1],
        )
    )
    outer_center = _cylinder(contact_radius, center_height, center_z0)
    center_tread = outer_center.cut(lobed_center)
    tpu = lower_lip.fuse(center_tread).fuse(upper_lip)

    bore = _cylinder(bore_diameter / 2.0, spec.wheel_width + 0.4, z0 - 0.2)
    petg = petg.cut(bore)

    if role == "drive":
        # Preserve the V0 provisional shaft clearance, split-clamp slot, and
        # transverse pinch-bolt hole on PETG only. V0 does not yet encode a
        # measured D-flat, so V1 intentionally does not invent one. TPU remains
        # an uninterrupted tread.
        petg = petg.cut(make_drive_split_tool(spec)).cut(make_drive_pinch_tool(spec))

    petg.label = f"p3_v1_{role}_PETG_six_lobe_hub"
    tpu.label = f"p3_v1_{role}_TPU_tread_with_end_lock_lips"
    petg.color = srgb(spec.petg_display_color)
    tpu.color = srgb(spec.tpu_display_color)
    return petg, tpu


def make_drive_material_pair(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    return _wheel_material_pair(
        role="drive",
        z0=spec.drive_z[0],
        contact_radius=spec.drive_contact_radius,
        crest_radius=spec.drive_crest_radius,
        valley_radius=spec.drive_valley_radius,
        bore_diameter=spec.drive_bore_diameter,
        spec=spec,
    )


def make_idler_material_pair(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    return _wheel_material_pair(
        role="idler",
        z0=spec.idler_z[0],
        contact_radius=spec.idler_contact_radius,
        crest_radius=spec.idler_crest_radius,
        valley_radius=spec.idler_valley_radius,
        bore_diameter=spec.idler_bore_diameter,
        spec=spec,
    )


def make_drive_wheel_compound(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    petg, tpu = make_drive_material_pair(spec)
    return Compound(children=[petg, tpu], label="p3_v1_drive_wheel_PETG_TPU_aligned")


def make_idler_wheel_compound(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    petg, tpu = make_idler_material_pair(spec)
    return Compound(children=[petg, tpu], label="p3_v1_idler_wheel_PETG_TPU_aligned")


def _place_at_polar(shape, radius: float, angle: float):
    return shape.moved(Location((*_polar(radius, angle), 0.0)))


def make_assembled(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    v0 = P3_V0
    children = [make_frame_quadrant(index, v0) for index in range(4)]
    children.extend(make_frame_splice_plate(v0).rotate(Axis.Z, angle) for angle in v0.frame_seam_angles)
    children.extend(make_carrier_segment(index, v0) for index in range(3))
    children.extend(placed_joint_key(angle, v0) for angle in v0.seam_angles)
    children.append(
        make_motor_slide_cradle(v0).moved(
            Location((*_polar(v0.motor_axis_radius_start - v0.motor_axis_radius_nominal, v0.motor_angle), 0.0))
        )
    )
    children.append(_place_at_polar(make_official_motor_reference(v0), v0.motor_axis_radius_start, v0.motor_angle))
    drive_petg, drive_tpu = make_drive_material_pair(spec)
    children.extend(
        _place_at_polar(part, spec.drive_axis_radius, v0.motor_angle)
        for part in (drive_petg, drive_tpu)
    )
    for angle in v0.idler_angles:
        idler_petg, idler_tpu = make_idler_material_pair(spec)
        children.extend(
            _place_at_polar(part, spec.idler_axis_radius, angle)
            for part in (idler_petg, idler_tpu)
        )
    children.extend([make_hall_bracket(v0), make_hall_spacer_pad(v0), make_hall_module_reference(v0)])
    return Compound(children=children, label="p3_v1_motor_outer_ring_multimaterial_assembly")


def make_material_exploded(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    drive_petg, drive_tpu = make_drive_material_pair(spec)
    idler_petg, idler_tpu = make_idler_material_pair(spec)
    children = [
        drive_petg.moved(Location((-18.0, 0.0, 0.0))),
        drive_tpu.moved(Location((-18.0, 0.0, 8.0))),
        idler_petg.moved(Location((18.0, 0.0, 0.0))),
        idler_tpu.moved(Location((18.0, 0.0, 8.0))),
    ]
    return Compound(children=children, label="p3_v1_material_interface_exploded")


def make_axial_section(spec: P3V1MotorOuterRingMultimaterialSpec = P3_V1):
    drive_petg, drive_tpu = make_drive_material_pair(spec)
    slab = Box(16.0, 0.35, 8.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(
        Location((0.0, 0.0, sum(spec.drive_z) / 2.0))
    )
    children = []
    for source in (drive_petg, drive_tpu):
        for fragment in source.intersect(slab) or []:
            if fragment.volume > 1e-8:
                fragment.color = source.color
                fragment.label = f"{source.label}_axial_section"
                children.append(fragment)
    return Compound(children=children, label="p3_v1_drive_wheel_axial_section")


def positive_intersection_volume(a, b) -> float:
    return sum(float(fragment.volume) for fragment in (a.intersect(b) or []) if fragment.volume > 0.0)


MULTIMATERIAL_FACTORIES = (
    ("drive_wheel_multimaterial", make_drive_wheel_compound),
    ("idler_wheel_multimaterial", make_idler_wheel_compound),
)
