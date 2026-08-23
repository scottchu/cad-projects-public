"""STEP-first geometry for the simplified KAGE P3 V3 mechanism.

The moving carriers retain the accepted 260T teeth, four-quadrant service
split, outward fins, and H/M/S axial bands.  The only moving-ring guide is a
compact smooth rear bead captured by nine direct-running spools on three inner
towers.  Each motor station is one connected open printed yoke.
"""

from __future__ import annotations

from copy import deepcopy
from math import cos, pi, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude
from cadgen import srgb

from p3_v3_full_ring_r2_geometry import (
    _annulus,
    _polar,
    _quarter_annulus,
    make_fin,
    make_frame_segments,
    make_outer_front_ring_posts,
    make_outer_front_ring_segments,
    make_output_pinion,
    make_seam_hardware,
)
from p3_v3_roller_tower_geometry import (
    _canonical_quadrant as _roller_canonical_quadrant,
    _full_role_ring as _roller_full_role_ring,
    make_roller as _make_roller,
    make_tower_hardware_references as _make_tower_hardware_references,
    make_tower_spacers as _make_tower_spacers,
    make_tower_thrust_washers as _make_tower_thrust_washers,
)
from p3_v3_simplified_drive_guidance_spec import (
    P3V3SimplifiedDriveGuidanceSpec,
    P3_V3_SIMPLIFIED,
)
from p3_v3_transmission_r1_geometry import (
    make_bearing as r1_make_bearing,
    make_miter_pair as r1_make_miter_pair,
    make_motor_body as r1_make_motor_body,
    make_motor_shaft as r1_make_motor_shaft,
    make_output_shaft as r1_make_output_shaft,
)


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids()) if shape else 0.0


def _radial_slot_tool(center_radius, tangent, travel, diameter, z0, height):
    radius = diameter / 2.0
    ends = [
        Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((center_radius + sign * travel / 2.0, tangent, z0))
        )
        for sign in (-1.0, 1.0)
    ]
    bridge = Box(travel, diameter, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius, tangent, z0))
    )
    return ends[0].fuse(bridge).fuse(ends[1])


def _x_cylinder(diameter: float, x0: float, x1: float, y: float, z: float):
    return Cylinder(
        diameter / 2.0,
        x1 - x0,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(Location(((x0 + x1) / 2.0, y, z)))


def _z_cylinder(diameter: float, z0: float, z1: float, x: float, y: float = 0.0):
    return Cylinder(
        diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))


def _translated_station(part, role_index: int, spec: P3V3SimplifiedDriveGuidanceSpec):
    return part.moved(
        Location((spec.station_radial_translation, 0.0, spec.role_shift_z(role_index)))
    ).rotate(Axis.Z, spec.motor_station_angles[role_index])


def make_ring_quadrant(role_index: int, quadrant_index: int, spec=P3_V3_SIMPLIFIED):
    """Accepted V3 quadrant with the compact smooth guide bead and outer fin."""

    if not 0 <= role_index < 3 or not 0 <= quadrant_index < 4:
        raise ValueError("role/quadrant outside accepted V3 ranges")
    quadrant = deepcopy(_roller_canonical_quadrant(role_index)).rotate(
        Axis.Z, quadrant_index * spec.quadrant_angle_degrees
    )
    fin_quadrant = int(spec.display_fin_angles[role_index] // spec.quadrant_angle_degrees)
    if quadrant_index == fin_quadrant:
        quadrant = quadrant.fuse(make_fin(role_index, spec))
    quadrant.label = (
        f"p3_v3_simplified_{spec.roles[role_index]}_M1_260T_"
        f"quadrant_Q{quadrant_index + 1}_65T_smooth_guide_bead"
    )
    quadrant.color = srgb(spec.role_colors[role_index])
    return quadrant


def make_ring_quadrants(role_index: int, spec=P3_V3_SIMPLIFIED):
    return tuple(make_ring_quadrant(role_index, q, spec) for q in range(4))


def make_full_role_ring_reference(role_index: int, spec=P3_V3_SIMPLIFIED):
    ring = deepcopy(_roller_full_role_ring(role_index))
    ring.label = f"p3_v3_simplified_{spec.roles[role_index]}_full_260T_validation_ring"
    ring.color = srgb(spec.role_colors[role_index])
    return ring


def make_fin_360_sweep(role_index: int, spec=P3_V3_SIMPLIFIED):
    r0, r1 = spec.fin_blade_radial_ranges[role_index]
    z0, z1 = spec.fin_blade_start_zs[role_index], spec.fin_tip_zs[role_index]
    sweep = _annulus(r0, r1, z1 - z0, z0)
    root_r = spec.fin_root_radial_ranges[role_index]
    root_z = spec.fin_root_z_ranges[role_index]
    if root_r is not None and root_z is not None:
        sweep = sweep.fuse(_annulus(root_r[0], root_r[1], root_z[1] - root_z[0], root_z[0]))
    sweep.label = f"p3_v3_simplified_{spec.roles[role_index]}_fin_360_sweep"
    return sweep


def make_roller(role_index: int, tower_index: int, axis_radius=None, spec=P3_V3_SIMPLIFIED):
    roller = _make_roller(role_index, tower_index, axis_radius, spec)
    roller.label = (
        f"p3_v3_simplified_tower_{tower_index + 1}_{spec.roles[role_index]}_"
        "direct_running_flanged_spool_D4_finished_bore"
    )
    return roller


def make_tower_spacers(tower_index: int, axis_radius=None, spec=P3_V3_SIMPLIFIED):
    parts = list(_make_tower_spacers(tower_index, axis_radius, spec))
    for index, part in enumerate(parts):
        part.label = f"p3_v3_simplified_tower_{tower_index + 1}_role_spacer_{index + 1}"
    return tuple(parts)


def make_tower_thrust_washers(tower_index: int, axis_radius=None, spec=P3_V3_SIMPLIFIED):
    parts = list(_make_tower_thrust_washers(tower_index, axis_radius, spec))
    for index, part in enumerate(parts):
        part.label = f"p3_v3_simplified_tower_{tower_index + 1}_{('lower','upper')[index]}_thrust_washer"
    return tuple(parts)


def make_tower_hardware_references(tower_index: int, axis_radius=None, spec=P3_V3_SIMPLIFIED):
    parts = list(_make_tower_hardware_references(tower_index, axis_radius, spec))
    for part in parts:
        part.label = part.label.replace("p3_v3_roller", "p3_v3_simplified")
        part.label = part.label.replace("4x20_smooth_pin", "D4x24_polished_axle")
    return tuple(parts)


def make_roller_tower_yoke(tower_index: int, axis_radius=None, spec=P3_V3_SIMPLIFIED):
    """One connected two-sided yoke; only tower 3 has radial slots."""

    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    angle = spec.roller_tower_angles[tower_index]
    z0, z1 = spec.tower_base_z_range
    r0, r1 = spec.tower_base_radial_range
    base = Box(r1 - r0, spec.tower_base_tangential_width, z1 - z0,
               align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location(((r0 + r1) / 2.0, 0.0, z0))
    )
    lower_bottom = spec.roller_range(0)[0]
    lower_socket = Cylinder(
        spec.tower_post_outer_diameter / 2.0,
        lower_bottom - z1 - spec.tower_post_top_clearance,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z1)))
    yoke = base.fuse(lower_socket)

    bridge_z0, bridge_z1 = spec.tower_top_bridge_z_range
    for tangent in spec.tower_backbone_tangent_offsets:
        backbone = Box(
            spec.tower_backbone_section,
            spec.tower_backbone_section,
            bridge_z1 - z1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.tower_backbone_radius, tangent, z1)))
        yoke = yoke.fuse(backbone)
    bridge_r0, bridge_r1 = spec.tower_top_bridge_radial_range
    bridge = Box(
        bridge_r1 - bridge_r0,
        spec.tower_top_bridge_tangential_width,
        bridge_z1 - bridge_z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((bridge_r0, 0.0, bridge_z0)))
    upper_z0, upper_z1 = spec.tower_upper_bushing_z_range
    upper_bushing = _z_cylinder(
        spec.tower_upper_bushing_outer_diameter,
        upper_z0,
        upper_z1,
        axis,
    ).cut(_z_cylinder(
        spec.tower_upper_bushing_bore_diameter,
        upper_z0 - 0.2,
        upper_z1 + 0.2,
        axis,
    ))
    yoke = yoke.fuse(bridge).fuse(upper_bushing)
    yoke = yoke.cut(_z_cylinder(
        spec.tower_axle_clearance_diameter,
        spec.tower_axle_z0 - 0.1,
        spec.tower_axle_z0 + spec.tower_lower_socket_depth + 0.1,
        axis,
    ))

    for tangent in spec.tower_mount_tangent_offsets:
        if spec.tower_is_adjustable(tower_index):
            tool = _radial_slot_tool(
                spec.tower_mount_axis_radius,
                tangent,
                spec.tower_preload_slot_travel,
                spec.tower_mount_clearance_diameter,
                z0 - 0.2,
                z1 - z0 + 0.4,
            )
        else:
            tool = _z_cylinder(
                spec.tower_mount_clearance_diameter,
                z0 - 0.2,
                z1 + 0.2,
                spec.tower_mount_axis_radius,
                tangent,
            )
        yoke = yoke.cut(tool)

    yoke = yoke.rotate(Axis.Z, angle)
    mode = "adjustable_plus_minus_0p25" if spec.tower_is_adjustable(tower_index) else "fixed_round_mounts"
    yoke.label = f"p3_v3_simplified_inner_tower_{tower_index + 1}_{mode}_connected_two_sided_yoke"
    yoke.color = srgb("#69737A")
    return yoke


def make_roller_tower_module(tower_index: int, spec=P3_V3_SIMPLIFIED):
    children = [make_roller_tower_yoke(tower_index, spec=spec)]
    children.extend(make_tower_spacers(tower_index, spec=spec))
    children.extend(make_tower_thrust_washers(tower_index, spec=spec))
    children.extend(make_roller(role, tower_index, spec=spec) for role in range(3))
    children.extend(make_tower_hardware_references(tower_index, spec=spec))
    return Compound(children=children, label=f"p3_v3_simplified_inner_tower_{tower_index + 1}_module")


def _bearing_bridge(role_index: int, which: str, spec=P3_V3_SIMPLIFIED):
    bearing_z = spec.lower_bearing_z(role_index) if which == "lower" else spec.upper_bearing_z(role_index)
    # The bridge is exactly bearing-thick. Axial location is set by the shaft
    # collars/spacer; printed lips would collide with those retained parts.
    z0, z1 = bearing_z
    x0, x1 = spec.unibody_bearing_bridge_x
    y0, y1 = spec.unibody_bearing_bridge_y
    bridge = Box(x1 - x0, y1 - y0, z1 - z0,
                 align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((x0, y0, z0)))
    pocket = _z_cylinder(
        spec.unibody_bearing_pocket_diameter,
        z0 - 0.05,
        z1 + 0.05,
        spec.output_axis_radius,
    )
    slot = Box(
        spec.unibody_bearing_install_mouth_x - spec.output_axis_radius + 0.2,
        spec.unibody_bearing_install_slot_width,
        z1 - z0 + 0.10,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((spec.output_axis_radius - 0.1, 0.0, bearing_z[0] - 0.05)))
    shaft_passage = _z_cylinder(
        spec.output_shaft_diameter + 0.20,
        z0 - 0.2,
        z1 + 0.2,
        spec.output_axis_radius,
    )
    return bridge.cut(pocket).cut(slot).cut(shaft_passage)


def make_unibody_drive_yoke(role_index: int, spec=P3_V3_SIMPLIFIED):
    """One connected open yoke with integral motor face, foot and MR84 seats."""

    shift = spec.role_shift_z(role_index)
    # The foot bolts on top of the chassis rather than occupying the chassis
    # volume.  This is the only stationary printed-to-printed interface here.
    foot_z0 = spec.chassis_z[1]
    foot_z1 = foot_z0 + spec.unibody_foot_thickness
    fx0, fx1 = spec.unibody_foot_x
    fy0, fy1 = spec.unibody_foot_y
    # Two narrow chassis rails keep the motor/shaft service corridor open while
    # remaining one printed body through the side columns and motor face.
    yoke = None
    for rail_y in spec.unibody_chassis_mount_y:
        rail = Box(
            fx1 - fx0,
            spec.unibody_foot_rail_width,
            foot_z1 - foot_z0,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((fx0, rail_y, foot_z0)))
        yoke = rail if yoke is None else yoke.fuse(rail)

    # Two side columns support both integral bearing bridges while leaving the
    # central/+X bearing-install chamber open.
    upper0, upper1 = spec.upper_bearing_z(role_index)
    column_top = upper1
    cx0, cx1 = spec.unibody_column_x
    for y in spec.unibody_column_y:
        column = Box(
            cx1 - cx0,
            spec.unibody_column_width,
            column_top - foot_z1,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((cx0, y, foot_z1 - 0.05)))
        yoke = yoke.fuse(column)
    yoke = yoke.fuse(_bearing_bridge(role_index, "lower", spec))
    yoke = yoke.fuse(_bearing_bridge(role_index, "upper", spec))

    # Integral motor face.  Its four M2 clearances and central shaft/miter
    # aperture follow the supplied NEMA8 drawing.
    motor_z = spec.miter_center_z(role_index)
    face_x0 = spec.motor_face_radius
    face_x1 = face_x0 + spec.unibody_motor_face_thickness
    face = Box(
        face_x1 - face_x0,
        spec.motor_face_size,
        spec.motor_face_size,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
    ).moved(Location((face_x0, 0.0, motor_z)))
    face = face.cut(_x_cylinder(
        spec.unibody_motor_face_aperture,
        face_x0 - 0.2,
        face_x1 + 0.2,
        0.0,
        motor_z,
    ))
    half = spec.unibody_motor_mount_pitch / 2.0
    for y in (-half, half):
        for z in (motor_z - half, motor_z + half):
            face = face.cut(_x_cylinder(
                spec.unibody_motor_mount_clearance,
                face_x0 - 0.2,
                face_x1 + 0.2,
                y,
                z,
            ))
    yoke = yoke.fuse(face)

    # Side ribs join the motor face to the bearing columns and down to the
    # chassis foot; there are no detachable bars, gates or bridge plates.
    face_bottom = motor_z - spec.motor_face_size / 2.0
    for y in (-spec.motor_face_size / 2.0 + 0.25, spec.motor_face_size / 2.0 - 0.25):
        link = Box(
            cx0 - face_x0 + 0.5,
            spec.unibody_column_width,
            spec.motor_face_size,
            align=(Align.MIN, Align.CENTER, Align.CENTER),
        ).moved(Location((face_x0, y, motor_z)))
        leg = Box(
            4.0,
            spec.unibody_column_width,
            max(0.4, face_bottom - foot_z1 + 0.2),
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((face_x0, y, foot_z1 - 0.1)))
        yoke = yoke.fuse(link).fuse(leg)

    for x in spec.unibody_chassis_mount_x:
        for y in spec.unibody_chassis_mount_y:
            yoke = yoke.cut(_z_cylinder(
                spec.unibody_chassis_mount_clearance,
                foot_z0 - 0.2,
                foot_z1 + 0.2,
                x,
                y,
            ))

    # Keep the central chamber clear for the complete miter pair.  A simple,
    # conservative envelope is used rather than offsetting involute faces.
    horizontal, vertical = r1_make_miter_pair()
    for moving in (
        horizontal.moved(Location((spec.station_radial_translation, 0.0, shift))),
        vertical.moved(Location((spec.station_radial_translation, 0.0, shift))),
    ):
        box = moving.bounding_box()
        c = spec.unibody_moving_clearance
        clearance = Box(
            box.size.X + 2.0 * c,
            box.size.Y + 2.0 * c,
            box.size.Z + 2.0 * c,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location(box.center()))
        yoke = yoke.cut(clearance)

    yoke = yoke.rotate(Axis.Z, spec.motor_station_angles[role_index])
    yoke.label = (
        f"p3_v3_simplified_{spec.roles[role_index]}_ONE_CONNECTED_open_yoke_"
        "integral_motor_face_chassis_foot_two_MR84_seats"
    )
    yoke.color = srgb("#69737A")
    return yoke


def _split_collar(role_index: int, which: str, spec=P3_V3_SIMPLIFIED):
    z0, z1 = spec.lower_collar_z(role_index) if which == "lower" else spec.upper_collar_z(role_index)
    collar = _z_cylinder(
        spec.lower_split_collar_outer_diameter if which == "lower" else spec.upper_split_collar_outer_diameter,
        z0,
        z1,
        spec.output_axis_radius,
    ).cut(_z_cylinder(
        spec.split_collar_bore_diameter,
        z0 - 0.2,
        z1 + 0.2,
        spec.output_axis_radius,
    ))
    screw_z = (z0 + z1) / 2.0
    pilot = Cylinder(
        spec.split_collar_set_screw_pilot / 2.0,
        spec.split_collar_set_screw_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.Y, 90.0).moved(
        Location((spec.output_axis_radius, 0.0, screw_z))
    )
    collar = collar.cut(pilot)
    collar = collar.rotate(Axis.Z, spec.motor_station_angles[role_index])
    collar.label = f"p3_v3_simplified_{spec.roles[role_index]}_purchased_D4_{which}_split_collar_REFERENCE"
    collar.color = srgb("#AEB5B9")
    return collar


def make_role_spacer(role_index: int, spec=P3_V3_SIMPLIFIED):
    z0, z1 = spec.role_spacer_z(role_index)
    spacer = _z_cylinder(spec.role_spacer_outer_diameter, z0, z1, spec.output_axis_radius).cut(
        _z_cylinder(spec.role_spacer_bore_diameter, z0 - 0.2, z1 + 0.2, spec.output_axis_radius)
    ).rotate(Axis.Z, spec.motor_station_angles[role_index])
    spacer.label = f"p3_v3_simplified_{spec.roles[role_index]}_ONLY_role_height_spacer"
    spacer.color = srgb("#D8D0C2")
    return spacer


def make_motor_station_parts(role_index: int, spec=P3_V3_SIMPLIFIED):
    """Minimal retained drive stack plus the integral printed yoke."""

    horizontal, vertical = r1_make_miter_pair()
    refs = [
        _translated_station(r1_make_motor_body(), role_index, spec),
        _translated_station(r1_make_motor_shaft(), role_index, spec),
        _translated_station(horizontal, role_index, spec),
        _translated_station(vertical, role_index, spec),
        _translated_station(r1_make_output_shaft(), role_index, spec),
        _translated_station(r1_make_bearing("lower"), role_index, spec),
        _translated_station(r1_make_bearing("upper"), role_index, spec),
        make_role_spacer(role_index, spec),
        make_output_pinion(role_index, spec),
        _split_collar(role_index, "lower", spec),
        _split_collar(role_index, "upper", spec),
        make_unibody_drive_yoke(role_index, spec),
    ]
    roles = (
        "NEMA8_REFERENCE",
        "NEMA8_D4x7_shaft_REFERENCE",
        "horizontal_16T_miter",
        "vertical_16T_miter",
        "D4x40_output_shaft_REFERENCE",
        "lower_MR84ZZ_REFERENCE",
        "upper_MR84ZZ_REFERENCE",
        "ONLY_role_height_spacer",
        "16T_output_pinion",
        "lower_datum_split_collar_REFERENCE",
        "upper_safety_split_collar_REFERENCE",
        "ONE_CONNECTED_printed_open_unibody_yoke",
    )
    for part, role_name in zip(refs, roles):
        part.label = f"p3_v3_simplified_{spec.roles[role_index]}_{role_name}"
    return tuple(refs)


def make_chassis_segments(spec=P3_V3_SIMPLIFIED):
    parts = []
    for q in range(4):
        part = _quarter_annulus(*spec.chassis_radii, *spec.chassis_z, q)
        for tower_index, angle in enumerate(spec.roller_tower_angles):
            rad = radians(angle)
            for tangent in spec.tower_mount_tangent_offsets:
                if spec.tower_is_adjustable(tower_index):
                    local_tool = _radial_slot_tool(
                        spec.tower_mount_axis_radius,
                        tangent,
                        spec.tower_preload_slot_travel,
                        spec.tower_mount_clearance_diameter,
                        spec.chassis_z[0] - 0.2,
                        spec.chassis_z[1] - spec.chassis_z[0] + 0.4,
                    ).rotate(Axis.Z, angle)
                else:
                    x = spec.tower_mount_axis_radius * cos(rad) - tangent * sin(rad)
                    y = spec.tower_mount_axis_radius * sin(rad) + tangent * cos(rad)
                    local_tool = _z_cylinder(
                        spec.tower_mount_clearance_diameter,
                        spec.chassis_z[0] - 0.2,
                        spec.chassis_z[1] + 0.2,
                        x,
                        y,
                    )
                part = part.cut(local_tool)
        # Matching M3 clearance holes for the three integral drive-yoke feet.
        # Points are defined in each station's local radial/tangential frame.
        for station_angle in spec.motor_station_angles:
            angle_rad = radians(station_angle)
            for local_x in spec.unibody_chassis_mount_x:
                for local_y in spec.unibody_chassis_mount_y:
                    x = local_x * cos(angle_rad) - local_y * sin(angle_rad)
                    y = local_x * sin(angle_rad) + local_y * cos(angle_rad)
                    part = part.cut(_z_cylinder(
                        spec.unibody_chassis_mount_clearance,
                        spec.chassis_z[0] - 0.2,
                        spec.chassis_z[1] + 0.2,
                        x,
                        y,
                    ))
        part.label = f"p3_v3_simplified_rear_chassis_Q{q + 1}_two_fixed_one_adjustable_tower"
        part.color = srgb("#59636A")
        parts.append(part)
    return tuple(parts)


def make_stationary_module(spec=P3_V3_SIMPLIFIED):
    children = [*make_chassis_segments(spec), *make_frame_segments(spec)]
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(make_outer_front_ring_segments(spec))
    for tower in range(3):
        children.extend(make_roller_tower_module(tower, spec).children)
    children.extend(make_unibody_drive_yoke(role, spec) for role in range(3))
    return Compound(children=children, label="p3_v3_simplified_stationary_structure")


def make_role_module(role_index: int, spec=P3_V3_SIMPLIFIED):
    children = [*make_ring_quadrants(role_index, spec)]
    children.extend(make_seam_hardware(role_index, spec))
    # The yoke is stationary and already belongs to the stationary module.
    children.extend(make_motor_station_parts(role_index, spec)[:-1])
    return Compound(children=children, label=f"p3_v3_simplified_{spec.roles[role_index]}_moving_drive_module")


def make_assembled(spec=P3_V3_SIMPLIFIED):
    children = list(make_stationary_module(spec).children)
    for role in range(3):
        children.extend(make_role_module(role, spec).children)
    return Compound(children=children, label="p3_v3_simplified_COMPLETE_three_ring_drive_guidance")


def make_service_exploded(spec=P3_V3_SIMPLIFIED):
    children = [*make_chassis_segments(spec), *make_frame_segments(spec)]
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(part.moved(Location((0.0, 0.0, 60.0))) for part in make_outer_front_ring_segments(spec))
    for tower in range(3):
        angle = spec.roller_tower_angles[tower]
        dx, dy = _polar(12.0, angle)
        children.append(make_roller_tower_yoke(tower, spec=spec))
        children.extend(part.moved(Location((dx, dy, 18.0))) for part in make_tower_spacers(tower, spec=spec))
        children.extend(part.moved(Location((dx, dy, 18.0))) for part in make_tower_thrust_washers(tower, spec=spec))
        children.extend(make_roller(role, tower, spec=spec).moved(Location((dx, dy, 18.0))) for role in range(3))
        children.extend(part.moved(Location((dx, dy, 34.0))) for part in make_tower_hardware_references(tower, spec=spec))

    for role in range(3):
        radial = spec.exploded_role_radial_offsets[role]
        z_lift = spec.exploded_role_z_offsets[role]
        children.extend(part.moved(Location((radial, 0.0, z_lift))) for part in make_ring_quadrants(role, spec))
        children.extend(part.moved(Location((radial, 0.0, z_lift))) for part in make_seam_hardware(role, spec))
        angle = radians(spec.motor_station_angles[role])
        inward = spec.exploded_station_inward_offsets[role]
        dx, dy = -inward * cos(angle), -inward * sin(angle)
        for index, part in enumerate(make_motor_station_parts(role, spec)):
            extra_z = 12.0 if index == 11 else 4.0 * max(0, index - 4)
            children.append(part.moved(Location((dx, dy, extra_z))))
    return Compound(children=children, label="p3_v3_simplified_COMPLETE_service_exploded")


PRIMARY_FACTORIES = (
    ("assembled", make_assembled),
    ("service_exploded", make_service_exploded),
)
