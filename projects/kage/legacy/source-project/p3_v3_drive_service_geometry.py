"""Staged CAD for the serviceable KAGE V3 minute drive station."""

from __future__ import annotations

from copy import deepcopy

from build123d import Align, Axis, Box, Compound, Cylinder, Location
from cadgen import srgb

from p3_v3_drive_service_spec import P3V3DriveServiceSpec, P3_V3_DRIVE_SERVICE
from p3_v3_full_ring_r2_geometry import _full_role_ring, make_output_pinion
from p3_v3_full_ring_r2_spec import P3_V3_FULL_RING_R2
from p3_v3_transmission_r1_geometry import (
    _d_prism_z,
    make_bearing as r1_make_bearing,
    make_miter_pair as r1_make_miter_pair,
    make_motor_body as r1_make_motor_body,
    make_motor_shaft as r1_make_motor_shaft,
    make_output_shaft as r1_make_output_shaft,
)


def _x_cylinder(diameter: float, length: float, x0: float, y: float, z: float):
    return Cylinder(
        diameter / 2.0,
        length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(Location((x0 + length / 2.0, y, z)))


def _z_cylinder(diameter: float, height: float, x: float, y: float, z0: float):
    return Cylinder(
        diameter / 2.0,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))


def _shift_r1(part, spec: P3V3DriveServiceSpec):
    shifted = deepcopy(part).moved(Location((0.5, 0.0, -2.15)))
    shifted.label = part.label.replace("p3_v3_r1", "p3_v3_drive_service_minute")
    return shifted


def make_chassis_reference(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    chassis = Box(42.0, 40.0, 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((118.0, 0.0, spec.chassis_z[0]))
    )
    chassis.label = "p3_v3_drive_service_EXISTING_chassis_datum_REFERENCE"
    chassis.color = srgb("#58656D")
    return chassis


def _motor_plate(spec: P3V3DriveServiceSpec):
    plate = Box(
        spec.motor_plate_thickness,
        24.0,
        24.0,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
    ).moved(Location((spec.motor_face_x, 0.0, spec.motor_axis_z)))
    plate = plate.cut(
        _x_cylinder(
            spec.motor_center_aperture,
            spec.motor_plate_thickness + 0.4,
            spec.motor_face_x - 0.2,
            0.0,
            spec.motor_axis_z,
        )
    )
    half = spec.motor_mount_pitch / 2.0
    for y in (-half, half):
        for z in (spec.motor_axis_z - half, spec.motor_axis_z + half):
            plate = plate.cut(
                _x_cylinder(2.4, spec.motor_plate_thickness + 0.4, spec.motor_face_x - 0.2, y, z)
            )
    return plate


def make_motor_cartridge_bracket(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    x0, x1 = spec.motor_flange_x
    z0, z1 = spec.flange_z
    flange = Box(x1 - x0, 2.0 * spec.flange_half_width, z1 - z0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((x0, 0.0, z0))
    )
    plate = _motor_plate(spec)
    # Two short triangular-function gussets represented by robust rectangular ribs.
    for y in (-11.6, 11.6):
        rib = Box(6.0, 1.2, 8.0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
            Location((108.0, y, z1 - 0.5))
        )
        plate = plate.fuse(rib)
    bracket = flange.fuse(plate)
    for y in spec.chassis_fastener_y:
        bracket = bracket.cut(
            _z_cylinder(spec.chassis_clearance_hole, z1 - z0 + 0.4, 105.0, y, z0 - 0.2)
        )
    bracket.label = "p3_v3_drive_service_motor_cartridge_bracket_M2_face_M3_chassis"
    bracket.color = srgb("#7B858B")
    return bracket


def make_motor_mount_screw_references(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    screws = []
    half = spec.motor_mount_pitch / 2.0
    for index, (y, z) in enumerate(
        (tuple((y, z) for y in (-half, half) for z in (spec.motor_axis_z - half, spec.motor_axis_z + half)))
    ):
        screw = _x_cylinder(2.0, spec.motor_mount_screw_length, spec.motor_face_x - 2.0, y, z)
        head = _x_cylinder(3.8, 1.5, spec.motor_face_x + spec.motor_plate_thickness, y, z)
        screw = screw.fuse(head)
        screw.label = f"p3_v3_drive_service_M2x4_motor_face_screw_{index + 1}_REFERENCE"
        screw.color = srgb("#B6BDC0")
        screws.append(screw)
    return tuple(screws)


def make_gearbox_frame(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    x0, x1 = spec.gearbox_flange_x
    z0, z1 = spec.flange_z
    frame = Box(x1 - x0, 2.0 * spec.flange_half_width, z1 - z0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((x0, 0.0, z0))
    )
    # Lower bearing cup is fused to the gearbox foot.
    lower0, lower1 = spec.lower_bearing_range
    cup = _z_cylinder(14.0, (lower1 - lower0) + spec.bearing_shoulder, spec.output_axis_x, 0.0, lower0 - spec.bearing_shoulder)
    pocket = _z_cylinder(spec.bearing_pocket_diameter, spec.bearing_width + 0.10, spec.output_axis_x, 0.0, lower0 - 0.05)
    aperture = _z_cylinder(spec.bearing_aperture_diameter, spec.bearing_shoulder + 0.4, spec.output_axis_x, 0.0, lower0 - spec.bearing_shoulder - 0.2)
    frame = frame.fuse(cup.cut(pocket).cut(aperture))
    # Two low webs connect the cup to the foot while remaining below both the
    # horizontal miter and the removable lower collar service envelope.
    for y in (-6.0, 6.0):
        web = Box(14.0, 2.0, 1.9, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((spec.output_axis_x, y, -25.70))
        )
        frame = frame.fuse(web)
    # Two side columns leave the complete miter envelope and fin lane open.
    for y in (-spec.tower_column_y, spec.tower_column_y):
        column_z0 = z1 - 0.20
        column = Box(
            spec.tower_column_x[1] - spec.tower_column_x[0],
            spec.tower_column_width,
            spec.bridge_z[0] - column_z0,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((spec.tower_column_x[0], y, column_z0)))
        frame = frame.fuse(column)
        frame = frame.cut(
            _z_cylinder(spec.bridge_insert_pilot, spec.bridge_insert_depth, spec.output_axis_x, y, spec.bridge_z[0] - spec.bridge_insert_depth)
        )
    # Four short M3 chassis holes; M2 remains exclusive to the motor face.
    for y in spec.chassis_fastener_y:
        frame = frame.cut(
            _z_cylinder(spec.chassis_clearance_hole, z1 - z0 + 0.4, 131.0, y, z0 - 0.2)
        )
    # Clear the shaft/collar service corridor through the foot.
    frame = frame.cut(_z_cylinder(11.0, z1 - z0 + 0.4, spec.output_axis_x, 0.0, z0 - 0.2))
    # The proven horizontal miter passes close to the lower cup.  Cut a
    # deterministic 0.20 mm six-direction clearance cloud around its true BREP
    # instead of pretending the bearing cup is a closed cylinder.
    horizontal, _ = r1_make_miter_pair()
    horizontal = _shift_r1(horizontal, spec)
    clearance = horizontal
    for delta in ((0.60, 0.0, 0.0), (-0.60, 0.0, 0.0), (0.0, 0.60, 0.0), (0.0, -0.60, 0.0), (0.0, 0.0, 0.60), (0.0, 0.0, -0.60)):
        clearance = clearance.fuse(horizontal.moved(Location(delta)))
    frame = frame.cut(clearance)
    frame.label = "p3_v3_drive_service_two_sided_bearing_gearbox_frame"
    frame.color = srgb("#606C73")
    return frame


def make_upper_bearing_bridge(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    z0, z1 = spec.bridge_z
    bridge = Box(16.0, 24.0, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((spec.output_axis_x, 0.0, z0))
    )
    upper0, upper1 = spec.upper_bearing_range
    bridge = bridge.cut(
        _z_cylinder(spec.bearing_pocket_diameter, spec.bearing_width + 0.10, spec.output_axis_x, 0.0, upper0 - 0.05)
    )
    bridge = bridge.cut(
        _z_cylinder(spec.bearing_aperture_diameter, z1 - upper1 + 0.25, spec.output_axis_x, 0.0, upper1 - 0.10)
    )
    for y in (-spec.tower_column_y, spec.tower_column_y):
        bridge = bridge.cut(
            _z_cylinder(spec.bridge_clearance_hole, z1 - z0 + 0.4, spec.output_axis_x, y, z0 - 0.2)
        )
    bridge.label = "p3_v3_drive_service_removable_upper_MR84_bridge_two_M3"
    bridge.color = srgb("#96A0A5")
    return bridge


def make_chassis_screw_references(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    screws = []
    for x in spec.chassis_fastener_x:
        for y in spec.chassis_fastener_y:
            screw = _z_cylinder(3.0, 8.0, x, y, -29.0)
            screw.label = f"p3_v3_drive_service_M3x8_chassis_screw_x{x:g}_y{y:g}_REFERENCE"
            screw.color = srgb("#B6BDC0")
            screws.append(screw)
    return tuple(screws)


def make_bridge_screw_references(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    screws = []
    for index, y in enumerate((-spec.tower_column_y, spec.tower_column_y)):
        screw = _z_cylinder(3.0, 8.0, spec.output_axis_x, y, spec.bridge_z[0] - 4.0)
        screw.label = f"p3_v3_drive_service_M3x8_upper_bridge_screw_{index + 1}_REFERENCE"
        screw.color = srgb("#B6BDC0")
        screws.append(screw)
    return tuple(screws)


def make_existing_drive_references(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    horizontal, vertical = r1_make_miter_pair()
    parts = (
        _shift_r1(r1_make_motor_body(), spec),
        _shift_r1(r1_make_motor_shaft(), spec),
        _shift_r1(horizontal, spec),
        _shift_r1(vertical, spec),
        _shift_r1(r1_make_output_shaft(), spec),
        _shift_r1(r1_make_bearing("lower"), spec),
        _shift_r1(r1_make_bearing("upper"), spec),
    )
    return parts


def _d_bored_cylinder(od: float, z0: float, z1: float, label: str, color: str, spec: P3V3DriveServiceSpec):
    part = _z_cylinder(od, z1 - z0, spec.output_axis_x, 0.0, z0).cut(
        _d_prism_z(spec.output_axis_x, z0 - 0.2, z1 + 0.2, spec.d_bore_diameter, spec.d_bore_across_flat)
    )
    part.label = label
    part.color = srgb(color)
    return part


def make_lower_datum_collar(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    return _d_bored_cylinder(
        spec.collar_od, *spec.lower_collar_z,
        "p3_v3_drive_service_purchased_4mm_split_lower_datum_collar_REFERENCE",
        "#AEB5B9", spec,
    )


def make_role_spacer(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    spacer = _z_cylinder(6.0, spec.spacer_z[1] - spec.spacer_z[0], spec.output_axis_x, 0.0, spec.spacer_z[0]).cut(
        _z_cylinder(4.15, spec.spacer_z[1] - spec.spacer_z[0] + 0.4, spec.output_axis_x, 0.0, spec.spacer_z[0] - 0.2)
    )
    spacer.label = "p3_v3_drive_service_minute_height_spacer_loose_on_4mm_shaft"
    spacer.color = srgb("#D8D0C2")
    return spacer


def make_lower_inner_race_spacer(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    z0, z1 = spec.lower_inner_race_spacer_z
    spacer = _z_cylinder(6.0, z1 - z0, spec.output_axis_x, 0.0, z0).cut(
        _z_cylinder(4.15, z1 - z0 + 0.4, spec.output_axis_x, 0.0, z0 - 0.2)
    )
    spacer.label = "p3_v3_drive_service_lower_inner_race_datum_spacer"
    spacer.color = srgb("#D8D0C2")
    return spacer


def make_safety_collar(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    return _d_bored_cylinder(
        spec.collar_od, *spec.safety_collar_z,
        "p3_v3_drive_service_purchased_4mm_split_upper_safety_collar_REFERENCE",
        "#AEB5B9", spec,
    )


def make_service_knob_shell(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    z0, z1 = spec.safety_collar_z
    knob = _z_cylinder(spec.service_knob_od, z1 - z0, spec.output_axis_x, 0.0, z0).cut(
        _z_cylinder(spec.collar_od + 0.30, z1 - z0 + 0.4, spec.output_axis_x, 0.0, z0 - 0.2)
    )
    # Six scallops make the removable shell hand-grippable without pretending
    # the smooth steel shaft is threaded.
    for index in range(6):
        scallop = _z_cylinder(3.0, z1 - z0 + 0.4, spec.output_axis_x + 7.0, 0.0, z0 - 0.2).rotate(
            Axis((spec.output_axis_x, 0.0, 0.0), (0.0, 0.0, 1.0)), index * 60.0
        )
        knob = knob.cut(scallop)
    knob.label = "p3_v3_drive_service_printed_hand_grip_over_commercial_split_collar"
    knob.color = srgb("#6E8B70")
    return knob


def make_minute_output_pinion(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    # Role 0 is already the canonical +X station.  Translate its identical
    # 16T geometry into the minute face plane rather than undoing role 1's
    # station rotation (which would retain the wrong coupled tooth phase).
    canonical = deepcopy(make_output_pinion(0))
    dz = spec.output_pinion_face[0] - P3_V3_FULL_RING_R2.pinion_face_ranges[0][0]
    pinion = canonical.moved(Location((0.0, 0.0, dz)))
    pinion.label = "p3_v3_drive_service_EXISTING_minute_16T_output_pinion_canonical_station"
    return pinion


def make_minute_ring_arc_reference(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    ring = deepcopy(_full_role_ring(spec.role_index))
    crop = Box(34.0, 64.0, 14.0, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((112.0, 0.0, 0.0)))
    pieces = ring.intersect(crop)
    if not pieces:
        raise ValueError("minute ring service crop produced no solid")
    arc = max(pieces, key=lambda part: part.volume)
    arc.label = "p3_v3_drive_service_EXISTING_minute_260T_ring_arc_REFERENCE"
    arc.color = srgb("#E38B48")
    return arc


def make_stage_1_motor(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    refs = make_existing_drive_references(spec)
    return Compound(
        children=[make_chassis_reference(spec), make_motor_cartridge_bracket(spec), refs[0], refs[1], *make_motor_mount_screw_references(spec)],
        label="p3_v3_drive_service_STAGE_1_mount_NEMA8_with_four_M2x4",
    )


def make_stage_2_gearbox(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    refs = make_existing_drive_references(spec)
    return Compound(
        children=[make_stage_1_motor(spec), make_gearbox_frame(spec), refs[2], *make_chassis_screw_references(spec)],
        label="p3_v3_drive_service_STAGE_2_mount_frame_and_horizontal_miter",
    )


def make_stage_3_shaft(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    refs = make_existing_drive_references(spec)
    return Compound(
        children=[make_stage_2_gearbox(spec), refs[3], refs[4], refs[5], refs[6], make_lower_datum_collar(spec), make_lower_inner_race_spacer(spec), make_upper_bearing_bridge(spec), *make_bridge_screw_references(spec)],
        label="p3_v3_drive_service_STAGE_3_insert_keyed_shaft_miter_two_MR84_and_bridge",
    )


def make_stage_4_pinion(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    return Compound(
        children=[make_stage_3_shaft(spec), make_role_spacer(spec), make_minute_output_pinion(spec), make_safety_collar(spec), make_service_knob_shell(spec), make_minute_ring_arc_reference(spec)],
        label="p3_v3_drive_service_STAGE_4_set_minute_pinion_height_and_external_retainer",
    )


def make_exploded_service(spec: P3V3DriveServiceSpec = P3_V3_DRIVE_SERVICE):
    refs = list(make_existing_drive_references(spec))
    offsets = {
        0: (-20.0, 0.0, 0.0),  # motor
        1: (-10.0, 0.0, 0.0),  # motor shaft
        2: (-4.0, 0.0, 0.0),   # horizontal miter
        3: (0.0, 0.0, 5.0),    # vertical miter
        4: (0.0, 0.0, 16.0),   # output shaft
        5: (0.0, 0.0, -5.0),   # lower bearing
        6: (0.0, 0.0, 8.0),    # upper bearing
    }
    exploded_refs = [part.moved(Location(offsets[index])) for index, part in enumerate(refs)]
    upper = make_upper_bearing_bridge(spec).moved(Location((0.0, 0.0, 14.0)))
    spacer = make_role_spacer(spec).moved(Location((0.0, 0.0, 21.0)))
    pinion = make_minute_output_pinion(spec).moved(Location((0.0, 0.0, 28.0)))
    collar = make_safety_collar(spec).moved(Location((0.0, 0.0, 34.0)))
    knob = make_service_knob_shell(spec).moved(Location((0.0, 0.0, 40.0)))
    return Compound(
        children=[make_chassis_reference(spec), make_motor_cartridge_bracket(spec), make_gearbox_frame(spec), *exploded_refs, make_lower_datum_collar(spec), make_lower_inner_race_spacer(spec).moved(Location((0.0, 0.0, -3.0))), upper, spacer, pinion, collar, knob, make_minute_ring_arc_reference(spec)],
        label="p3_v3_drive_service_EXPLODED_installation_order",
    )


PRIMARY_FACTORIES = (
    ("stage_1_motor", make_stage_1_motor),
    ("stage_2_gearbox", make_stage_2_gearbox),
    ("stage_3_shaft", make_stage_3_shaft),
    ("stage_4_complete", make_stage_4_pinion),
    ("exploded", make_exploded_service),
)
