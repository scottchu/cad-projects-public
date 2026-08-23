"""BREP geometry for the isolated B2-R0 three-role drive-station stage."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as r4
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1
from p3_v3_mvp_drive_b2_r0_role_stations_spec import NAMESPACE, SPEC


P = SPEC.purchased


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    if left is None or right is None:
        return 0.0
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def local_point(angle_deg: float, radius_mm: float, tangent_mm: float = 0.0) -> tuple[float, float]:
    a = radians(angle_deg)
    return (
        radius_mm * cos(a) - tangent_mm * sin(a),
        radius_mm * sin(a) + tangent_mm * cos(a),
    )


def local_box(angle: float, r0: float, r1: float, t0: float, t1: float, z0: float, height: float):
    return Box(r1-r0, t1-t0, height, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((r0, t0, z0))
    ).rotate(Axis.Z, angle)


def vertical_cylinder(angle: float, radius: float, tangent: float, diameter: float, z0: float, height: float):
    x, y = local_point(angle, radius, tangent)
    return Cylinder(diameter/2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, y, z0))
    )


def radial_cylinder(angle: float, r0: float, tangent: float, z: float, diameter: float, length: float):
    shape = Cylinder(diameter/2.0, length, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(Axis.Y, 90.0)
    return shape.moved(Location((r0, tangent, z))).rotate(Axis.Z, angle)


def ring_shape(angle: float, radius: float, tangent: float, od: float, bore: float, z0: float, height: float):
    return vertical_cylinder(angle, radius, tangent, od, z0, height).cut(
        vertical_cylinder(angle, radius, tangent, bore, z0-0.05, height+0.1)
    )


def spur_gear_shape(angle: float, radius: float, z0: float):
    root = Cylinder(P.spur_root_radius_mm, P.spur_face_mm, align=(Align.CENTER, Align.CENTER, Align.MIN))
    teeth = []
    tooth_tangent = 1.25
    for index in range(P.spur_tooth_count):
        tooth = Box(
            P.spur_tip_radius_mm-P.spur_root_radius_mm,
            tooth_tangent,
            P.spur_face_mm,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((P.spur_root_radius_mm-0.1, 0.0, 0.0))).rotate(
            Axis.Z, index*360.0/P.spur_tooth_count
        )
        teeth.append(tooth)
    gear = root.fuse(*teeth).cut(
        Cylinder(P.spur_bore_diameter_mm/2.0, P.spur_face_mm+0.1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((0.0, 0.0, -0.05))
        )
    ).moved(Location((*local_point(angle, radius), z0)))
    gear.label = f"{NAMESPACE}_purchased_16T_output_pinion"
    return gear


def role_index(role: str) -> int:
    if role not in SPEC.station_roles:
        raise ValueError(f"unknown role {role!r}")
    return SPEC.station_roles.index(role)


def printed_station_sled(role: str, q_mm: float = 0.0, angle_deg: float = 0.0):
    role_index(role)
    if abs(q_mm) > max(abs(v) for v in SPEC.service_q_mm) + 1e-9:
        raise ValueError("q outside B1 service range")
    base = b1.motor_sled_shape()
    half_frame = P.motor_frame_mm/2.0
    wall_inner = half_frame + SPEC.cradle_clearance_mm
    wall_outer = wall_inner + SPEC.cradle_wall_mm
    bottom = SPEC.motor_input_axis_z_mm-half_frame

    body_pocket = local_box(
        0.0, SPEC.motor_rear_radius_nominal_mm-0.2, SPEC.motor_face_radius_nominal_mm+0.2,
        -wall_inner, wall_inner, bottom-0.1,
        b1.SPEC.screw_under_head_z_mm-(bottom-0.1)+0.1,
    )
    cradle_walls = (
        local_box(0.0, SPEC.motor_rear_radius_nominal_mm-0.5, SPEC.motor_face_radius_nominal_mm-0.2,
                  wall_inner, wall_outer, b1.SPEC.screw_under_head_z_mm, SPEC.printed_max_z_mm-b1.SPEC.screw_under_head_z_mm),
        local_box(0.0, SPEC.motor_rear_radius_nominal_mm-0.5, SPEC.motor_face_radius_nominal_mm-0.2,
                  -wall_outer, -wall_inner, b1.SPEC.screw_under_head_z_mm, SPEC.printed_max_z_mm-b1.SPEC.screw_under_head_z_mm),
    )
    bracket_r0 = SPEC.motor_face_radius_nominal_mm + 0.05
    bracket = local_box(
        0.0, bracket_r0, bracket_r0+SPEC.bracket_thickness_mm,
        -half_frame-1.0, half_frame+1.0,
        bottom-0.2, SPEC.printed_max_z_mm-(bottom-0.2),
    )
    pilot_tool = radial_cylinder(
        0.0, bracket_r0-0.1, 0.0, SPEC.motor_input_axis_z_mm,
        P.motor_pilot_diameter_mm+2*SPEC.fit_clearance_mm,
        SPEC.bracket_thickness_mm+0.2,
    )
    lower_hole_z = SPEC.motor_input_axis_z_mm-P.motor_face_pitch_mm/2.0
    m2_tools = tuple(
        radial_cylinder(
            0.0, bracket_r0-0.2, tangent, lower_hole_z,
            SPEC.m2_clearance_diameter_mm, SPEC.bracket_thickness_mm+2.0,
        )
        for tangent in (-P.motor_face_pitch_mm/2.0, P.motor_face_pitch_mm/2.0)
    )

    tower = vertical_cylinder(
        0.0, SPEC.shaft_radius_nominal_mm, 0.0, SPEC.tower_outer_diameter_mm,
        b1.SPEC.screw_under_head_z_mm, SPEC.printed_max_z_mm-b1.SPEC.screw_under_head_z_mm,
    )
    shaft_tool = vertical_cylinder(
        0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.spur_bore_diameter_mm,
        b1.SPEC.screw_under_head_z_mm-0.1,
        SPEC.printed_max_z_mm-b1.SPEC.screw_under_head_z_mm+0.2,
    )
    lower_pocket = vertical_cylinder(
        0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.bearing_pocket_diameter_mm,
        SPEC.lower_bearing_z_mm[0]-0.05, P.bearing_pocket_depth_mm,
    )
    upper_pocket = vertical_cylinder(
        0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.bearing_pocket_diameter_mm,
        SPEC.upper_bearing_z_mm[0]-0.05, P.bearing_pocket_depth_mm,
    )
    collar_cavity = vertical_cylinder(
        0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.collar_od_mm+2*SPEC.fit_clearance_mm,
        SPEC.lower_collar_z_mm[0]-0.05,
        SPEC.lower_collar_z_mm[1]-SPEC.lower_collar_z_mm[0]+0.1,
    )
    miter_window = local_box(
        0.0,
        SPEC.shaft_radius_nominal_mm-SPEC.tower_outer_diameter_mm/2.0-0.2,
        SPEC.miter_center_radius_nominal_mm+P.miter_envelope_radius_mm+0.3,
        -SPEC.tower_window_tangential_mm/2.0,
        SPEC.tower_window_tangential_mm/2.0,
        SPEC.miter_z_mm[0]-0.2,
        SPEC.miter_z_mm[1]-SPEC.miter_z_mm[0]+0.4,
    )

    printed = base.cut(body_pocket).fuse(*cradle_walls, bracket, tower).cut(
        pilot_tool, *m2_tools, shaft_tool, lower_pocket, upper_pocket, collar_cavity, miter_window
    )
    solids = list(printed.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{role} station sled must be one fused solid, got {len(solids)}")
    printed = solids[0]
    if q_mm:
        printed = printed.moved(Location((q_mm, 0.0, 0.0)))
    if angle_deg:
        printed = printed.rotate(Axis.Z, angle_deg)
    printed.label = f"{NAMESPACE}_{role}_printed_station_sled_q{q_mm:+.2f}_A{angle_deg:03.0f}"
    return printed


def motor_body_witness(angle: float, q: float):
    half = P.motor_frame_mm/2.0
    shape = local_box(
        angle,
        SPEC.motor_rear_radius_nominal_mm+q,
        SPEC.motor_face_radius_nominal_mm+q,
        -half, half,
        SPEC.motor_input_axis_z_mm-half,
        P.motor_frame_mm,
    )
    shape.label = f"{NAMESPACE}_purchased_motor_20p3x39p3"
    return shape


def motor_pilot_witness(angle: float, q: float):
    shape = radial_cylinder(
        angle, SPEC.motor_face_radius_nominal_mm+q, 0.0, SPEC.motor_input_axis_z_mm,
        P.motor_pilot_diameter_mm, P.motor_pilot_height_mm,
    )
    shape.label = f"{NAMESPACE}_purchased_motor_pilot_D16"
    return shape


def motor_shaft_witness(angle: float, q: float):
    shape = radial_cylinder(
        angle, SPEC.motor_face_radius_nominal_mm+q, 0.0, SPEC.motor_input_axis_z_mm,
        P.motor_shaft_diameter_mm, P.motor_shaft_length_mm,
    )
    shape.label = f"{NAMESPACE}_purchased_motor_D4x7_shaft"
    return shape


def wire_keepout_witness(angle: float, q: float):
    shape = local_box(
        angle,
        SPEC.motor_rear_radius_nominal_mm+q-SPEC.wire_keepout_radial_mm,
        SPEC.motor_rear_radius_nominal_mm+q,
        -SPEC.wire_keepout_tangential_mm/2.0,
        SPEC.wire_keepout_tangential_mm/2.0,
        SPEC.motor_input_axis_z_mm-SPEC.wire_keepout_axial_mm/2.0,
        SPEC.wire_keepout_axial_mm,
    )
    shape.label = f"{NAMESPACE}_motor_wire_keepout"
    return shape


def output_stack_witnesses(role: str, angle: float, q: float) -> tuple:
    i = role_index(role)
    radius = SPEC.shaft_radius_nominal_mm+q
    pinion_z0, pinion_z1 = SPEC.role_pinion_z_mm[i]
    collar_z0, collar_z1 = SPEC.role_upper_collar_z_mm[i]
    shaft = vertical_cylinder(
        angle, radius, 0.0, P.shaft_min_diameter_mm,
        SPEC.lower_collar_z_mm[0], SPEC.role_shaft_length_mm[i],
    ); shaft.label = f"{NAMESPACE}_{role}_purchased_output_shaft_L{SPEC.role_shaft_length_mm[i]:.0f}"
    lower_collar = ring_shape(angle, radius, 0.0, P.collar_od_mm, P.collar_bore_mm+SPEC.fit_clearance_mm,
                              SPEC.lower_collar_z_mm[0], P.collar_width_mm)
    lower_collar.label = f"{NAMESPACE}_{role}_purchased_lower_collar"
    lower_bearing = ring_shape(angle, radius, 0.0, P.bearing_od_mm, P.bearing_bore_mm,
                               SPEC.lower_bearing_z_mm[0], P.bearing_width_mm)
    lower_bearing.label = f"{NAMESPACE}_{role}_purchased_lower_MR84ZZ"
    lower_shim = ring_shape(angle, radius, 0.0, P.shim_od_mm, P.shim_id_mm,
                            SPEC.lower_shim_z_mm[0], P.shim_thickness_mm)
    lower_shim.label = f"{NAMESPACE}_{role}_purchased_lower_shim"
    vertical_miter = ring_shape(angle, radius, 0.0, 2*P.miter_envelope_radius_mm, P.spur_bore_diameter_mm,
                                SPEC.miter_z_mm[0], P.miter_face_mm)
    vertical_miter.label = f"{NAMESPACE}_{role}_purchased_vertical_miter_1to1"
    upper_shim = ring_shape(angle, radius, 0.0, P.shim_od_mm, P.shim_id_mm,
                            SPEC.upper_shim_z_mm[0], P.shim_thickness_mm)
    upper_shim.label = f"{NAMESPACE}_{role}_purchased_upper_shim"
    upper_bearing = ring_shape(angle, radius, 0.0, P.bearing_od_mm, P.bearing_bore_mm,
                               SPEC.upper_bearing_z_mm[0], P.bearing_width_mm)
    upper_bearing.label = f"{NAMESPACE}_{role}_purchased_upper_MR84ZZ"
    spacer = ring_shape(angle, radius, 0.0, P.collar_od_mm, P.spur_bore_diameter_mm,
                        SPEC.upper_bearing_z_mm[1], SPEC.role_spacer_length_mm[i])
    spacer.label = f"{NAMESPACE}_{role}_purchased_role_spacer_L{SPEC.role_spacer_length_mm[i]:.1f}"
    pinion = spur_gear_shape(angle, radius, pinion_z0)
    pinion.label = f"{NAMESPACE}_{role}_purchased_16T_output_pinion"
    upper_collar = ring_shape(angle, radius, 0.0, P.collar_od_mm, P.collar_bore_mm+SPEC.fit_clearance_mm,
                              collar_z0, collar_z1-collar_z0)
    upper_collar.label = f"{NAMESPACE}_{role}_purchased_upper_collar"
    return (shaft, lower_collar, lower_bearing, lower_shim, vertical_miter, upper_shim, upper_bearing, spacer, pinion, upper_collar)


def horizontal_miter_witness(angle: float, q: float):
    shape = radial_cylinder(
        angle,
        SPEC.miter_center_radius_nominal_mm+q-P.miter_face_mm/2.0,
        0.0,
        SPEC.motor_input_axis_z_mm,
        2*P.miter_envelope_radius_mm,
        P.miter_face_mm,
    ).cut(radial_cylinder(
        angle,
        SPEC.miter_center_radius_nominal_mm+q-P.miter_face_mm/2.0-0.05,
        0.0,
        SPEC.motor_input_axis_z_mm,
        P.spur_bore_diameter_mm,
        P.miter_face_mm+0.1,
    ))
    shape.label = f"{NAMESPACE}_purchased_horizontal_miter_1to1"
    return shape


def station_purchased_witnesses(role: str, angle: float, q: float = 0.0) -> tuple:
    rows = [
        motor_body_witness(angle, q), motor_pilot_witness(angle, q), motor_shaft_witness(angle, q),
        wire_keepout_witness(angle, q), horizontal_miter_witness(angle, q),
    ]
    rows.extend(output_stack_witnesses(role, angle, q))
    return tuple(rows)


def ring_witness(role: str):
    i = role_index(role)
    z0, z1 = SPEC.role_pinion_z_mm[i]
    outer = Cylinder(SPEC.ring_witness_outer_radius_mm, z1-z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,z0)))
    inner = Cylinder(SPEC.ring_witness_inner_radius_mm, z1-z0+0.1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0,0,z0-0.05)))
    witness = outer.cut(inner)
    witness.label = f"{NAMESPACE}_{role}_260T_m1_ring_envelope_REFERENCE"
    return witness


def mount_hardware_all_stations() -> tuple:
    rows = []
    for angle in SPEC.station_angles_deg:
        for radius in b1.SPEC.motor_axis_radii_mm:
            for tangent in b1.SPEC.motor_tangent_offsets_mm:
                screw = b1.m3_screw_shape(angle, radius, tangent)
                screw.label = f"{NAMESPACE}_M3x8_motor_A{angle:03.0f}_R{radius:.0f}_T{tangent:+.0f}"
                nut = b1.m3_nut_shape(angle, radius, tangent, -30.0)
                nut.label = f"{NAMESPACE}_M3_nut_motor_A{angle:03.0f}_R{radius:.0f}_T{tangent:+.0f}"
                rows.extend((screw, nut))
    for angle, radius, tangents, role in (
        (60.0, b1.SPEC.fixed_center_radius_mm, b1.SPEC.fixed_axis_tangent_offsets_mm, "fixed"),
        (b1.SPEC.spine_angle_deg, b1.SPEC.spine_center_radius_mm, b1.SPEC.spine_axis_tangent_offsets_mm, "spine"),
    ):
        for tangent in tangents:
            rows.extend((b1.m3_screw_shape(angle, radius, tangent), b1.m3_nut_shape(angle, radius, tangent)))
    return tuple(rows)


def printable_occurrences() -> tuple[dict[str, object], ...]:
    shapes = [*(b1.named_quadrant(i) for i in range(1,5))]
    shapes.extend(printed_station_sled(role) for role in SPEC.station_roles)
    shapes.extend((b1.fixed_riser_shape(), b1.spine_riser_shape()))
    names = ("quadrant_Q1","quadrant_Q2","quadrant_Q3","quadrant_Q4","hour_station_sled","minute_station_sled","second_station_sled","reusable_fixed_riser","spine_riser")
    rows = []
    for name, shape in zip(names, shapes):
        min_z = float(shape.bounding_box().min.Z)
        printable = shape.moved(Location((0,0,-min_z)))
        printable.label = f"{NAMESPACE}_{name}_print_orientation"
        rows.append({"name":name,"shape":printable,"orientation":"minimum_z_on_bed","label":printable.label})
    return tuple(rows)


def assembled_shape(q_mm: float = 0.0):
    children = [b1.named_quadrant(i) for i in range(1,5)]
    children.extend((b1.fixed_riser_shape(60.0), b1.spine_riser_shape()))
    for role, angle in zip(SPEC.station_roles, SPEC.station_angles_deg):
        children.append(printed_station_sled(role, q_mm, angle))
        children.extend(station_purchased_witnesses(role, angle, q_mm))
        children.append(ring_witness(role))
    children.extend(deepcopy(row["shape"]) for row in r4.hardware_occurrences())
    children.extend(mount_hardware_all_stations())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_q{q_mm:+.2f}")


def exploded_assembly_order_shape():
    children = [b1.named_quadrant(i) for i in range(1,5)]
    children.extend((b1.fixed_riser_shape(60.0).moved(Location((0,0,20))), b1.spine_riser_shape().moved(Location((0,0,26)))))
    for station_index, (role, angle) in enumerate(zip(SPEC.station_roles, SPEC.station_angles_deg)):
        sled = printed_station_sled(role, 0.0, angle).moved(Location((0,0,18+station_index*4)))
        children.append(sled)
        for part_index, part in enumerate(station_purchased_witnesses(role, angle, 0.0)):
            dx, dy = local_point(angle, (part_index+1)*7.0, 0.0)
            moved = part.moved(Location((dx,dy,30+part_index*5+station_index*2)))
            moved.label = part.label
            children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_exploded_assembly_order")
