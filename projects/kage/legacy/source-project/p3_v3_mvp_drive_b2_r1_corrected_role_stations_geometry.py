"""BREP geometry for the isolated B2-R1 corrected three-role drive stations."""

from __future__ import annotations

from copy import deepcopy
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as r4
import p3_v3_mvp_mount_b1_r1_raised_nut_rails_geometry as b1
from p3_v3_mvp_drive_b2_r1_corrected_role_stations_spec import NAMESPACE, SPEC


P = SPEC.purchased


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    if left is None or right is None:
        return 0.0
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def _one(shape, label: str):
    solids = list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one fused solid, got {len(solids)}")
    result = solids[0]
    if not result.is_valid or result.volume <= 0:
        raise RuntimeError(f"{label} must be a valid positive-volume solid")
    result.label = label
    return result


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
    return _one(
        vertical_cylinder(angle, radius, tangent, od, z0, height).cut(
            vertical_cylinder(angle, radius, tangent, bore, z0-0.05, height+0.1)
        ),
        f"{NAMESPACE}_ring_witness",
    )


def spur_gear_shape(angle: float, radius: float, z0: float):
    root = Cylinder(P.spur_root_radius_mm, P.spur_face_mm, align=(Align.CENTER, Align.CENTER, Align.MIN))
    teeth = []
    for index in range(P.spur_tooth_count):
        teeth.append(
            Box(
                P.spur_tip_radius_mm-P.spur_root_radius_mm,
                1.25,
                P.spur_face_mm,
                align=(Align.MIN, Align.CENTER, Align.MIN),
            ).moved(Location((P.spur_root_radius_mm-0.1, 0.0, 0.0))).rotate(
                Axis.Z, index*360.0/P.spur_tooth_count
            )
        )
    gear = root.fuse(*teeth).cut(
        Cylinder(P.spur_bore_diameter_mm/2.0, P.spur_face_mm+0.1, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((0.0, 0.0, -0.05))
        )
    ).moved(Location((*local_point(angle, radius), z0)))
    return _one(gear, f"{NAMESPACE}_purchased_16T_output_pinion")


def role_index(role: str) -> int:
    if role not in SPEC.station_roles:
        raise ValueError(f"unknown role {role!r}")
    return SPEC.station_roles.index(role)


def _motor_m2_axes() -> tuple[tuple[float, float], ...]:
    """Two lower face screws; the upper pair is above the frozen Z=-5.2 interface."""
    lower_z = SPEC.motor_input_axis_z_mm-P.motor_face_pitch_mm/2.0
    return tuple((tangent, lower_z) for tangent in (-P.motor_face_pitch_mm/2.0, P.motor_face_pitch_mm/2.0))


def printed_station_sled(role: str, q_mm: float = 0.0, angle_deg: float = 0.0):
    role_index(role)
    if abs(q_mm) > max(abs(v) for v in SPEC.service_q_mm) + 1e-9:
        raise ValueError("q outside B1 service range")

    base = b1.motor_sled_shape()
    half_frame = P.motor_frame_mm/2.0
    wall_inner = half_frame + SPEC.cradle_clearance_mm
    wall_outer = wall_inner + SPEC.cradle_wall_mm
    body_bottom = SPEC.motor_input_axis_z_mm-half_frame

    # Clear the small portion of the B1 foot occupied by the motor envelope.
    body_pocket = local_box(
        0.0,
        SPEC.motor_rear_radius_nominal_mm-SPEC.cradle_clearance_mm,
        SPEC.motor_face_radius_nominal_mm+SPEC.cradle_clearance_mm,
        -wall_inner,
        wall_inner,
        body_bottom-SPEC.cradle_clearance_mm,
        b1.SPEC.screw_under_head_z_mm-(body_bottom-SPEC.cradle_clearance_mm)+0.1,
    )
    foundation_z = b1.SPEC.screw_under_head_z_mm-0.25
    cradle_height = SPEC.printed_max_z_mm-foundation_z
    cradle_walls = (
        local_box(
            0.0,
            SPEC.motor_rear_radius_nominal_mm-0.5,
            SPEC.bracket_plane_radius_nominal_mm,
            wall_inner,
            wall_outer,
            foundation_z,
            cradle_height,
        ),
        local_box(
            0.0,
            SPEC.motor_rear_radius_nominal_mm-0.5,
            SPEC.bracket_plane_radius_nominal_mm,
            -wall_outer,
            -wall_inner,
            foundation_z,
            cradle_height,
        ),
    )

    bracket = local_box(
        0.0,
        SPEC.bracket_inward_radius_nominal_mm,
        SPEC.bracket_plane_radius_nominal_mm,
        -half_frame-1.0,
        half_frame+1.0,
        body_bottom-0.2,
        SPEC.printed_max_z_mm-(body_bottom-0.2),
    )
    pilot_tool = radial_cylinder(
        0.0,
        SPEC.bracket_inward_radius_nominal_mm-0.1,
        0.0,
        SPEC.motor_input_axis_z_mm,
        P.motor_pilot_diameter_mm+2*SPEC.fit_clearance_mm,
        SPEC.motor_pilot_outer_face_radius_nominal_mm-(SPEC.bracket_inward_radius_nominal_mm-0.1)+0.1,
    )
    m2_tools = tuple(
        radial_cylinder(
            0.0,
            SPEC.bracket_inward_radius_nominal_mm-0.2,
            tangent,
            z,
            SPEC.m2_clearance_diameter_mm,
            SPEC.bracket_thickness_mm+0.4,
        )
        for tangent, z in _motor_m2_axes()
    )

    # Crop the nominal D15 tower at the specified R117.9 inward pocket datum.
    tower_full = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        SPEC.tower_outer_diameter_mm,
        foundation_z,
        SPEC.printed_max_z_mm-foundation_z,
    )
    tower_crop = local_box(
        0.0,
        0.0,
        SPEC.tower_pocket_inward_radius_nominal_mm,
        -50.0,
        50.0,
        foundation_z-0.1,
        SPEC.printed_max_z_mm-foundation_z+0.2,
    )
    tower = tower_full.cut(tower_crop)

    # A lower bridge joins the bracket, B1 rib, and tower without entering the
    # D16.2 pilot opening or the corrected input-bevel service window.
    lower_bridge = local_box(
        0.0,
        SPEC.bracket_plane_radius_nominal_mm,
        SPEC.shaft_radius_nominal_mm+P.bearing_od_mm/2.0,
        -half_frame-1.0,
        half_frame+1.0,
        foundation_z,
        1.20,
    )

    shaft_tool = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        P.spur_bore_diameter_mm,
        foundation_z-0.1,
        SPEC.printed_max_z_mm-foundation_z+0.2,
    )
    lower_pocket = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        P.bearing_pocket_diameter_mm,
        SPEC.lower_bearing_z_mm[0]-0.05,
        SPEC.lower_shim_z_mm[1]-(SPEC.lower_bearing_z_mm[0]-0.05)+0.1,
    )
    upper_pocket = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        P.bearing_pocket_diameter_mm,
        SPEC.upper_shim_z_mm[0]-0.05,
        SPEC.printed_max_z_mm-(SPEC.upper_shim_z_mm[0]-0.05)+0.1,
    )
    collar_cavity = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        P.collar_od_mm+2*SPEC.fit_clearance_mm,
        foundation_z-0.1,
        SPEC.lower_shim_z_mm[1]-(foundation_z-0.1)+0.1,
    )
    output_bevel_cavity = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        2*(SPEC.shaft_radius_nominal_mm-SPEC.output_bevel_inward_tooth_radius_nominal_mm)+2*SPEC.fit_clearance_mm,
        SPEC.miter_z_mm[0]-SPEC.fit_clearance_mm,
        P.miter_face_mm+2*SPEC.fit_clearance_mm,
    )
    miter_window = local_box(
        0.0,
        SPEC.tower_window_radial_mm[0],
        SPEC.tower_window_radial_mm[1],
        -SPEC.tower_window_tangential_mm/2.0,
        SPEC.tower_window_tangential_mm/2.0,
        SPEC.tower_window_z_mm[0],
        SPEC.tower_window_z_mm[1]-SPEC.tower_window_z_mm[0],
    )
    m2_driver_tools = tuple(
        radial_cylinder(
            0.0,
            SPEC.bracket_inward_radius_nominal_mm-0.2,
            tangent,
            z,
            SPEC.m3_tool_diameter_mm,
            21.0,
        )
        for tangent, z in _motor_m2_axes()
    )
    b1_driver_tools = tuple(
        vertical_cylinder(
            0.0,
            radius,
            tangent,
            SPEC.m3_tool_diameter_mm,
            b1.SPEC.screw_under_head_z_mm-0.05,
            SPEC.printed_max_z_mm-b1.SPEC.screw_under_head_z_mm+0.1,
        )
        for radius in b1.SPEC.motor_axis_radii_mm
        for tangent in b1.SPEC.motor_tangent_offsets_mm
    )
    detached_tab_reliefs = (
        local_box(
            0.0,
            SPEC.bracket_inward_radius_nominal_mm-0.1,
            SPEC.bracket_plane_radius_nominal_mm+0.1,
            5.9,
            half_frame+1.1,
            body_bottom+3.45,
            SPEC.printed_max_z_mm-(body_bottom+3.45)+0.1,
        ),
        local_box(
            0.0,
            SPEC.bracket_inward_radius_nominal_mm-0.1,
            SPEC.bracket_plane_radius_nominal_mm+0.1,
            -half_frame-1.1,
            -5.9,
            body_bottom+3.45,
            SPEC.printed_max_z_mm-(body_bottom+3.45)+0.1,
        ),
    )

    printed = base.cut(body_pocket).fuse(*cradle_walls, bracket, tower, lower_bridge).cut(
        pilot_tool,
        *m2_tools,
        shaft_tool,
        lower_pocket,
        upper_pocket,
        collar_cavity,
        output_bevel_cavity,
        miter_window,
        *m2_driver_tools,
        *b1_driver_tools,
        *detached_tab_reliefs,
    )
    if len(printed.solids()) != 1:
        details = [
            (
                round(float(s.volume), 3),
                tuple(round(float(v), 3) for v in (
                    s.bounding_box().min.X, s.bounding_box().max.X,
                    s.bounding_box().min.Y, s.bounding_box().max.Y,
                    s.bounding_box().min.Z, s.bounding_box().max.Z,
                )),
            )
            for s in printed.solids()
        ]
        raise RuntimeError(f"{role} station sled fusion fragments: {details}")
    printed = _one(printed, f"{NAMESPACE}_{role}_printed_station_sled")
    if q_mm:
        printed = printed.moved(Location((q_mm, 0.0, 0.0)))
    if angle_deg:
        printed = printed.rotate(Axis.Z, angle_deg)
    printed.label = f"{NAMESPACE}_{role}_printed_station_sled_q{q_mm:+.2f}_A{angle_deg:03.0f}"
    return printed


def tower_actual_solid(role: str, q_mm: float = 0.0, angle_deg: float = 0.0):
    """Actual corrected tower material, isolated for pilot-clearance evidence."""
    role_index(role)
    foundation_z = b1.SPEC.screw_under_head_z_mm-0.25
    tower = vertical_cylinder(
        0.0,
        SPEC.shaft_radius_nominal_mm,
        0.0,
        SPEC.tower_outer_diameter_mm,
        foundation_z,
        SPEC.printed_max_z_mm-foundation_z,
    ).cut(
        local_box(
            0.0, 0.0, SPEC.tower_pocket_inward_radius_nominal_mm,
            -50.0, 50.0, foundation_z-0.1,
            SPEC.printed_max_z_mm-foundation_z+0.2,
        ),
        vertical_cylinder(
            0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.spur_bore_diameter_mm,
            foundation_z-0.1, SPEC.printed_max_z_mm-foundation_z+0.2,
        ),
        vertical_cylinder(
            0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.bearing_pocket_diameter_mm,
            SPEC.lower_bearing_z_mm[0]-0.05,
            SPEC.lower_shim_z_mm[1]-(SPEC.lower_bearing_z_mm[0]-0.05)+0.1,
        ),
        vertical_cylinder(
            0.0, SPEC.shaft_radius_nominal_mm, 0.0,
            P.collar_od_mm+2*SPEC.fit_clearance_mm,
            foundation_z-0.1,
            SPEC.lower_shim_z_mm[1]-(foundation_z-0.1)+0.1,
        ),
        vertical_cylinder(
            0.0, SPEC.shaft_radius_nominal_mm, 0.0,
            2*(SPEC.shaft_radius_nominal_mm-SPEC.output_bevel_inward_tooth_radius_nominal_mm)+2*SPEC.fit_clearance_mm,
            SPEC.miter_z_mm[0]-SPEC.fit_clearance_mm,
            P.miter_face_mm+2*SPEC.fit_clearance_mm,
        ),
        vertical_cylinder(
            0.0, SPEC.shaft_radius_nominal_mm, 0.0, P.bearing_pocket_diameter_mm,
            SPEC.upper_shim_z_mm[0]-0.05,
            SPEC.printed_max_z_mm-(SPEC.upper_shim_z_mm[0]-0.05)+0.1,
        ),
        local_box(
            0.0,
            SPEC.tower_window_radial_mm[0], SPEC.tower_window_radial_mm[1],
            -SPEC.tower_window_tangential_mm/2.0, SPEC.tower_window_tangential_mm/2.0,
            SPEC.tower_window_z_mm[0],
            SPEC.tower_window_z_mm[1]-SPEC.tower_window_z_mm[0],
        ),
    )
    if q_mm:
        tower = tower.moved(Location((q_mm, 0.0, 0.0)))
    if angle_deg:
        tower = tower.rotate(Axis.Z, angle_deg)
    tower.label = f"{NAMESPACE}_{role}_actual_tower_material"
    return tower


def motor_body_witness(angle: float, q: float):
    half = P.motor_frame_mm/2.0
    shape = local_box(
        angle,
        SPEC.motor_rear_radius_nominal_mm+q,
        SPEC.motor_face_radius_nominal_mm+q,
        -half,
        half,
        SPEC.motor_input_axis_z_mm-half,
        P.motor_frame_mm,
    )
    return _one(shape, f"{NAMESPACE}_purchased_motor_20p3x39p3")


def motor_pilot_witness(angle: float, q: float):
    return _one(
        radial_cylinder(
            angle,
            SPEC.motor_face_radius_nominal_mm+q,
            0.0,
            SPEC.motor_input_axis_z_mm,
            P.motor_pilot_diameter_mm,
            P.motor_pilot_height_mm,
        ),
        f"{NAMESPACE}_purchased_motor_pilot_D16",
    )


def motor_shaft_witness(angle: float, q: float, maximum: bool = False):
    length = (
        SPEC.motor_shaft_max_endpoint_radius_nominal_mm-SPEC.motor_face_radius_nominal_mm
        if maximum else P.motor_shaft_length_mm
    )
    suffix = "maximum_envelope" if maximum else "nominal"
    return _one(
        radial_cylinder(
            angle,
            SPEC.motor_face_radius_nominal_mm+q,
            0.0,
            SPEC.motor_input_axis_z_mm,
            P.motor_shaft_diameter_mm,
            length,
        ),
        f"{NAMESPACE}_purchased_motor_D4_shaft_{suffix}",
    )


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
    return _one(shape, f"{NAMESPACE}_motor_wire_connector_keepout_rolled_tangentially")


def input_bevel_witness(angle: float, q: float):
    hub_length = 2.50
    outer = radial_cylinder(
        angle,
        SPEC.input_bevel_rear_radius_nominal_mm+q,
        0.0,
        SPEC.motor_input_axis_z_mm,
        6.0,
        hub_length,
    )
    bore = radial_cylinder(
        angle,
        SPEC.input_bevel_rear_radius_nominal_mm+q-0.05,
        0.0,
        SPEC.motor_input_axis_z_mm,
        P.spur_bore_diameter_mm,
        hub_length+0.1,
    )
    tooth_lug = local_box(
        angle,
        SPEC.input_bevel_rear_radius_nominal_mm+q+hub_length-0.1,
        SPEC.input_bevel_front_radius_nominal_mm+q,
        2.05,
        2.50,
        SPEC.motor_input_axis_z_mm-0.4,
        0.8,
    )
    return _one(outer.cut(bore).fuse(tooth_lug), f"{NAMESPACE}_purchased_input_bevel_1to1")


def output_bevel_witness(angle: float, q: float):
    output_tooth_radius = SPEC.shaft_radius_nominal_mm-SPEC.output_bevel_inward_tooth_radius_nominal_mm
    shape = ring_shape(
        angle,
        SPEC.shaft_radius_nominal_mm+q,
        0.0,
        2*output_tooth_radius,
        P.spur_bore_diameter_mm,
        SPEC.miter_z_mm[0],
        P.miter_face_mm,
    )
    tooth_lug = local_box(
        angle,
        SPEC.output_bevel_inward_tooth_radius_nominal_mm+q,
        SPEC.output_bevel_inward_tooth_radius_nominal_mm+q+1.5,
        2.05,
        2.50,
        SPEC.motor_input_axis_z_mm-0.4,
        0.8,
    )
    shape = _one(shape.fuse(tooth_lug), f"{NAMESPACE}_purchased_output_bevel_1to1")
    shape.label = f"{NAMESPACE}_purchased_output_bevel_1to1"
    return shape


def motor_m2_screw_witnesses(angle: float, q: float) -> tuple:
    rows = []
    for tangent, z in _motor_m2_axes():
        screw = radial_cylinder(
            angle,
            SPEC.bracket_inward_radius_nominal_mm+q,
            tangent,
            z,
            P.motor_mount_screw_diameter_mm,
            P.motor_mount_screw_length_mm,
        )
        screw.label = f"{NAMESPACE}_purchased_M2x4_motor_mount_T{tangent:+.1f}"
        rows.append(screw)
    return tuple(rows)


def output_stack_witnesses(role: str, angle: float, q: float) -> tuple:
    i = role_index(role)
    radius = SPEC.shaft_radius_nominal_mm+q
    pinion_z0, _ = SPEC.role_pinion_z_mm[i]
    collar_z0, collar_z1 = SPEC.role_upper_collar_z_mm[i]
    shaft = vertical_cylinder(
        angle,
        radius,
        0.0,
        P.shaft_max_diameter_mm,
        SPEC.lower_collar_z_mm[0],
        SPEC.role_shaft_length_mm[i],
    )
    shaft.label = f"{NAMESPACE}_{role}_purchased_output_shaft_L{SPEC.role_shaft_length_mm[i]:.0f}"
    lower_collar = ring_shape(angle, radius, 0.0, P.collar_od_mm, P.collar_bore_mm+SPEC.fit_clearance_mm,
                              SPEC.lower_collar_z_mm[0], P.collar_width_mm)
    lower_collar.label = f"{NAMESPACE}_{role}_purchased_lower_collar"
    lower_bearing = ring_shape(angle, radius, 0.0, P.bearing_od_mm, P.bearing_bore_mm,
                               SPEC.lower_bearing_z_mm[0], P.bearing_width_mm)
    lower_bearing.label = f"{NAMESPACE}_{role}_purchased_lower_MR84ZZ"
    lower_shim = ring_shape(angle, radius, 0.0, P.shim_od_mm, P.shim_id_mm,
                            SPEC.lower_shim_z_mm[0], P.shim_thickness_mm)
    lower_shim.label = f"{NAMESPACE}_{role}_purchased_lower_shim"
    vertical_miter = output_bevel_witness(angle, q)
    vertical_miter.label = f"{NAMESPACE}_{role}_purchased_output_bevel_1to1"
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
    return (
        shaft,
        lower_collar,
        lower_bearing,
        lower_shim,
        vertical_miter,
        upper_shim,
        upper_bearing,
        spacer,
        pinion,
        upper_collar,
    )


def station_purchased_witnesses(role: str, angle: float, q: float = 0.0) -> tuple:
    rows = [
        motor_body_witness(angle, q),
        motor_pilot_witness(angle, q),
        motor_shaft_witness(angle, q),
        wire_keepout_witness(angle, q),
        input_bevel_witness(angle, q),
        *motor_m2_screw_witnesses(angle, q),
    ]
    rows.extend(output_stack_witnesses(role, angle, q))
    return tuple(rows)


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
            screw = b1.m3_screw_shape(angle, radius, tangent)
            screw.label = f"{NAMESPACE}_M3x8_{role}_T{tangent:+.0f}"
            nut = b1.m3_nut_shape(angle, radius, tangent)
            nut.label = f"{NAMESPACE}_M3_nut_{role}_T{tangent:+.0f}"
            rows.extend((screw, nut))
    return tuple(rows)


def printable_occurrences() -> tuple[dict[str, object], ...]:
    shapes = [*(b1.named_quadrant(i) for i in range(1, 5))]
    shapes.extend(printed_station_sled(role) for role in SPEC.station_roles)
    shapes.extend((b1.fixed_riser_shape(), b1.spine_riser_shape()))
    names = (
        "quadrant_Q1",
        "quadrant_Q2",
        "quadrant_Q3",
        "quadrant_Q4",
        "hour_station_sled",
        "minute_station_sled",
        "second_station_sled",
        "reusable_fixed_riser",
        "spine_riser",
    )
    rows = []
    for name, shape in zip(names, shapes):
        min_z = float(shape.bounding_box().min.Z)
        printable = shape.moved(Location((0, 0, -min_z)))
        printable.label = f"{NAMESPACE}_{name}_print_orientation"
        rows.append({"name": name, "shape": printable, "orientation": "minimum_z_on_bed", "label": printable.label})
    return tuple(rows)


def assembled_shape(q_mm: float = 0.0):
    children = [b1.named_quadrant(i) for i in range(1, 5)]
    children.extend((b1.fixed_riser_shape(60.0), b1.spine_riser_shape()))
    for role, angle in zip(SPEC.station_roles, SPEC.station_angles_deg):
        children.append(printed_station_sled(role, q_mm, angle))
        children.extend(station_purchased_witnesses(role, angle, q_mm))
    children.extend(deepcopy(row["shape"]) for row in r4.hardware_occurrences())
    children.extend(mount_hardware_all_stations())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_q{q_mm:+.2f}")


def exploded_assembly_order_shape():
    children = []
    for index in range(1, 5):
        quadrant = b1.named_quadrant(index)
        quadrant.label = f"{NAMESPACE}_assembly_step_01_base_quadrant_Q{index}"
        children.append(quadrant)
    fixed = b1.fixed_riser_shape(60.0).moved(Location((0, 0, 18)))
    fixed.label = f"{NAMESPACE}_assembly_step_02_fixed_riser"
    spine = b1.spine_riser_shape().moved(Location((0, 0, 24)))
    spine.label = f"{NAMESPACE}_assembly_step_03_spine_riser"
    children.extend((fixed, spine))
    for station_index, (role, angle) in enumerate(zip(SPEC.station_roles, SPEC.station_angles_deg)):
        radial_offset = 20.0+station_index*8.0
        dx, dy = local_point(angle, radial_offset)
        sled = printed_station_sled(role, 0.0, angle).moved(Location((dx, dy, 32+station_index*8)))
        sled.label = f"{NAMESPACE}_assembly_step_{4+station_index:02d}_{role}_printed_sled"
        children.append(sled)
        for part_index, part in enumerate(station_purchased_witnesses(role, angle, 0.0)):
            px, py = local_point(angle, radial_offset+(part_index+1)*5.0)
            moved = part.moved(Location((px, py, 48+part_index*4+station_index*6)))
            moved.label = f"{NAMESPACE}_assembly_step_{7+part_index:02d}_{role}_{part.label.split(NAMESPACE+'_')[-1]}"
            children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_exploded_assembly_order")


def model_only_shape():
    return Compound(
        children=[deepcopy(row["shape"]) for row in printable_occurrences()],
        label=f"{NAMESPACE}_nine_printed_objects_model_only",
    )
