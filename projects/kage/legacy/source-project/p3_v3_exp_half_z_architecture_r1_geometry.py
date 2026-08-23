"""Repair-round communication geometry for the KAGE half-Z experiment.

Only architecture D is a complete candidate.  Architecture E is retained as a
rejected comparison so the previous concept is not silently promoted.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from math import cos, radians, sin

import py_gearworks as pgw
from build123d import (
    Align,
    Axis,
    Box,
    Color,
    Compound,
    Cone,
    Cylinder,
    Location,
    Solid,
)

from p3_v3_transmission_r1_geometry import make_miter_pair as make_locked_real_miter_pair

from p3_v3_exp_half_z_architecture_r1_spec import (
    P3_V3_EXP_HALF_Z_ARCHITECTURE_R1 as P,
)


def _tag(shape, label: str, color: str):
    shape.label = label
    shape.color = Color(color)
    return shape


def _annulus(inner_radius: float, outer_radius: float, z0: float, z1: float):
    outer = Cylinder(outer_radius, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    )
    inner = Cylinder(inner_radius, z1 - z0 + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0 - 0.2))
    )
    return outer.cut(inner)


def _polar(radius: float, angle_degrees: float) -> tuple[float, float]:
    angle = radians(angle_degrees)
    return radius * cos(angle), radius * sin(angle)


def _bounds(shape) -> tuple[float, float, float, float, float, float]:
    box = shape.bounding_box()
    return (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z)


def envelope_z(shape) -> tuple[float, float]:
    box = shape.bounding_box()
    return box.min.Z, box.max.Z


def locked_step_sha256() -> str:
    return sha256(P.locked_step.read_bytes()).hexdigest()


def _radial_box(r0: float, r1: float, tangential: float, z0: float, z1: float, angle: float):
    part = Box(
        r1 - r0,
        tangential,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((r0 + r1) / 2.0, 0.0, z0)))
    return part.rotate(Axis.Z, angle)


def _cylinder_x(radius: float, length: float, x_center: float, y: float, z: float):
    """Cylinder whose axis is the local +X motor axis."""

    return Cylinder(
        radius,
        length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(Location((x_center, y, z)))


@lru_cache(maxsize=1)
def _D_real_miter_reference_pair():
    """Real 16T straight-miter teeth reused from the accepted transmission source."""

    horizontal, vertical = make_locked_real_miter_pair()
    shift = Location((P.d_miter_translation_x, 0.0, P.d_miter_translation_z))
    horizontal = horizontal.moved(shift)
    vertical = vertical.moved(shift)
    return horizontal, vertical


def _D_real_miter_pair(role_index: int):
    horizontal_ref, vertical_ref = _D_real_miter_reference_pair()
    angle = P.motor_station_angles[role_index]
    horizontal = Solid(horizontal_ref.wrapped).rotate(Axis.Z, angle)
    vertical = Solid(vertical_ref.wrapped).rotate(Axis.Z, angle)
    role = P.roles[role_index]
    horizontal = _tag(
        horizontal,
        f"D_{role}_REAL_16T_straight_miter_horizontal_D_bore",
        "#C99B38",
    )
    vertical = _tag(
        vertical,
        f"D_{role}_REAL_16T_straight_miter_vertical_D_bore",
        "#E3B94D",
    )
    return horizontal, vertical


def _ring_and_pinion(
    *,
    role_index: int,
    teeth: int,
    pitch_radius: float,
    output_axis_radius: float,
    radial_envelope: tuple[float, float],
    layer: tuple[float, float],
    fin_radius: float,
    fin_tip_z: float,
    architecture: str,
):
    role = P.roles[role_index]
    color = P.role_colors[role_index]
    z0, z1 = layer
    face_z0, face_z1 = (
        P.d_pinion_face_range(role_index)
        if architecture == "D"
        else layer
    )
    phase = 180.0 / teeth
    ring_wrapper = pgw.SpurRingGear(
        number_of_teeth=teeth,
        module=P.module,
        height=face_z1 - face_z0,
        center=[0.0, 0.0, face_z0],
        backlash=0.10,
    )
    teeth_shape = ring_wrapper.build_part().solid().rotate(Axis.Z, phase)
    body_inner = pitch_radius + 1.6
    body_outer = radial_envelope[1]
    body = _annulus(body_inner, body_outer, z0, z1)

    blade_r0 = fin_radius - P.fin_radial_thickness / 2.0
    blade_r1 = fin_radius + P.fin_radial_thickness / 2.0
    root_r0 = min(body_outer - 1.0, blade_r0)
    root_r1 = max(body_outer, blade_r1)
    angle = P.display_fin_angles[role_index]
    root = _radial_box(root_r0, root_r1, P.fin_root_tangential_width, z0, z1, angle)
    blade = _radial_box(
        blade_r0,
        blade_r1,
        P.fin_tangential_widths[role_index],
        z1 - 0.20,
        fin_tip_z,
        angle,
    )
    carrier = teeth_shape.fuse(body).fuse(root).fuse(blade)
    carrier = _tag(
        carrier,
        f"{architecture}_{role}_complete_M1_{teeth}T_carrier_with_integral_fin",
        color,
    )

    pinion_wrapper = pgw.SpurGear(
        number_of_teeth=P.pinion_teeth,
        module=P.module,
        height=face_z1 - face_z0,
        center=[output_axis_radius, 0.0, face_z0],
        pressure_angle=radians(P.pressure_angle_degrees),
        backlash=0.10,
        tip_truncation=0.10,
        enable_undercut=True,
    )
    pinion_wrapper.mesh_to(ring_wrapper, target_dir=pgw.RIGHT, backlash=P.backlash)
    pinion = pinion_wrapper.build_part().solid()
    hub = Cylinder(3.6, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((output_axis_radius, 0.0, z0))
    )
    pinion = pinion.fuse(hub)
    station_angle = P.motor_station_angles[role_index]
    local_spin = (phase - station_angle) * teeth / P.pinion_teeth
    pinion = pinion.rotate(
        Axis((output_axis_radius, 0.0, 0.0), (0.0, 0.0, 1.0)),
        local_spin,
    ).rotate(Axis.Z, station_angle)
    pinion = _tag(
        pinion,
        f"{architecture}_{role}_real_M1_16T_positive_drive_pinion",
        "#D9A441",
    )
    return carrier, pinion


def _motor_station(
    *,
    role_index: int,
    output_axis_radius: float,
    ring_layer: tuple[float, float],
    motor_z: tuple[float, float],
    rear_limit: float,
    architecture: str,
):
    """Finite horizontal NEMA8 package and serviceable positive drive station."""

    role = P.roles[role_index]
    station_angle = P.motor_station_angles[role_index]
    body_x1 = output_axis_radius - P.motor_shaft_gap_to_output_axis
    body_x0 = body_x1 - P.motor_body_length
    shaft_z = sum(motor_z) / 2.0
    body_local = Box(
        P.motor_body_length,
        P.motor_face_size,
        motor_z[1] - motor_z[0],
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((body_x0 + body_x1) / 2.0, 0.0, motor_z[0])))
    if architecture == "D":
        # Four actual NEMA8 face holes are centred on the true motor axis.  The
        # holes are shallow tapped-bore references rather than through holes.
        for y in (-P.motor_mount_pitch / 2.0, P.motor_mount_pitch / 2.0):
            for z in (shaft_z - P.motor_mount_pitch / 2.0, shaft_z + P.motor_mount_pitch / 2.0):
                bore = _cylinder_x(
                    P.motor_face_clearance_diameter / 2.0,
                    P.motor_face_thread_depth + 0.2,
                    body_x1 - P.motor_face_thread_depth / 2.0 + 0.1,
                    y,
                    z,
                )
                body_local = body_local.cut(bore)
    body = body_local.rotate(Axis.Z, station_angle)
    body = _tag(body, f"{architecture}_{role}_NEMA8_20p3x39p3_PURCHASED_ENVELOPE_4xM2_FACE", "#18232D")

    horizontal_shaft = Cylinder(
        P.motor_shaft_diameter / 2.0,
        output_axis_radius - body_x1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.Y, 90.0).moved(Location((body_x1, 0.0, shaft_z))).rotate(Axis.Z, station_angle)
    horizontal_shaft = _tag(horizontal_shaft, f"{architecture}_{role}_horizontal_motor_shaft", "#8C9297")

    axis_x, axis_y = _polar(output_axis_radius, station_angle)
    output_shaft = Cylinder(
        P.output_shaft_diameter / 2.0,
        ring_layer[1] - motor_z[0],
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis_x, axis_y, motor_z[0])))
    output_shaft = _tag(output_shaft, f"{architecture}_{role}_vertical_output_shaft", "#8C9297")

    if architecture != "D":
        # E is intentionally retained as a rejected layout comparison.  Its
        # smooth cones are labelled as non-functional references and are not a
        # release claim.
        vertical_bevel = Cone(7.5, 3.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((axis_x, axis_y, shaft_z - 4.0))
        )
        vertical_bevel = _tag(
            vertical_bevel,
            f"E_REJECTED_{role}_vertical_miter_LAYOUT_REFERENCE_NOT_TEETH",
            "#C99B38",
        )
        horizontal_bevel = Cone(7.5, 3.0, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
            Axis.Y, 90.0
        ).moved(Location((output_axis_radius - 4.0, 0.0, shaft_z))).rotate(Axis.Z, station_angle)
        horizontal_bevel = _tag(
            horizontal_bevel,
            f"E_REJECTED_{role}_horizontal_miter_LAYOUT_REFERENCE_NOT_TEETH",
            "#C99B38",
        )
        ledges = []
        for tangent in (-P.motor_face_size / 2.0 - 1.5, P.motor_face_size / 2.0 + 1.5):
            ledges.append(Box(
                P.motor_body_length + 3.0,
                3.0,
                0.70,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location(((body_x0 + body_x1) / 2.0, tangent, rear_limit))).rotate(Axis.Z, station_angle))
        tray = _tag(Compound(children=ledges), f"E_REJECTED_{role}_layout_motor_ledges", "#596771")
        return (body, horizontal_shaft, output_shaft, vertical_bevel, horizontal_bevel, tray)

    horizontal_bevel, vertical_bevel = _D_real_miter_pair(role_index)

    # One positive, removable U-cradle: rear tray, two side rails, a square
    # NEMA8 face frame with central miter clearance, and two chassis feet.
    side_center = P.motor_face_size / 2.0 + P.motor_cradle_running_clearance + P.motor_cradle_side_thickness / 2.0
    tray = Box(
        P.motor_body_length + 1.5,
        2.0 * (side_center + P.motor_cradle_side_thickness / 2.0),
        motor_z[0] - rear_limit,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(((body_x0 + body_x1) / 2.0, 0.0, rear_limit)))
    rails = []
    for tangent in (-side_center, side_center):
        rails.append(Box(
            P.motor_body_length + 1.5,
            P.motor_cradle_side_thickness,
            motor_z[1] - rear_limit,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((body_x0 + body_x1) / 2.0, tangent, rear_limit))))

    face_x0 = body_x1 + 0.20
    face_x1 = face_x0 + P.motor_yoke_radial_thickness
    face = Box(
        face_x1 - face_x0,
        P.motor_face_size,
        P.motor_face_size,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location(((face_x0 + face_x1) / 2.0, 0.0, shaft_z)))
    face = face.cut(_cylinder_x(
        P.motor_yoke_center_clearance_radius,
        face_x1 - face_x0 + 0.4,
        (face_x0 + face_x1) / 2.0,
        0.0,
        shaft_z,
    ))
    face_screws = []
    for y in (-P.motor_mount_pitch / 2.0, P.motor_mount_pitch / 2.0):
        for z in (shaft_z - P.motor_mount_pitch / 2.0, shaft_z + P.motor_mount_pitch / 2.0):
            face = face.cut(_cylinder_x(
                P.motor_face_clearance_diameter / 2.0,
                face_x1 - face_x0 + 0.4,
                (face_x0 + face_x1) / 2.0,
                y,
                z,
            ))
            screw = _cylinder_x(
                P.motor_face_clearance_diameter / 2.0 - 0.05,
                face_x1 - body_x1 + P.motor_face_thread_depth,
                (face_x1 + body_x1 - P.motor_face_thread_depth) / 2.0,
                y,
                z,
            )
            head = _cylinder_x(
                2.0,
                0.70,
                face_x1 + 0.35,
                y,
                z,
            )
            face_screws.append(screw.fuse(head))

    foot_x0, foot_x1 = face_x0, P.motor_chassis_screw_radius + 4.0
    foot_y = P.motor_chassis_screw_pitch_y / 2.0
    feet = []
    chassis_screws = []
    for y in (-foot_y, foot_y):
        foot = Box(
            foot_x1 - foot_x0,
            5.0,
            0.80,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((foot_x0 + foot_x1) / 2.0, y, 0.0)))
        hole = Cylinder(
            P.motor_chassis_screw_diameter / 2.0,
            1.20,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((P.motor_chassis_screw_radius, y, -0.2)))
        feet.append(foot.cut(hole))
        screw = Cylinder(
            P.motor_chassis_screw_diameter / 2.0 - 0.05,
            6.8,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((P.motor_chassis_screw_radius, y, -6.0)))
        head = Cylinder(3.0, 0.70, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((P.motor_chassis_screw_radius, y, 0.80))
        )
        chassis_screws.append(screw.fuse(head))

    yoke_local = tray.fuse(*rails, face, *feet)
    yoke = _tag(
        yoke_local.rotate(Axis.Z, station_angle),
        f"D_{role}_positive_serviceable_U_cradle_4xM2_face_2xM3_chassis",
        "#596771",
    )
    face_screws = [
        _tag(s.rotate(Axis.Z, station_angle), f"D_{role}_NEMA8_face_M2_fastener_{i}", "#73797D")
        for i, s in enumerate(face_screws, start=1)
    ]
    chassis_screws = [
        _tag(s.rotate(Axis.Z, station_angle), f"D_{role}_cradle_chassis_M3_fastener_{i}", "#73797D")
        for i, s in enumerate(chassis_screws, start=1)
    ]
    return (
        body,
        horizontal_shaft,
        output_shaft,
        horizontal_bevel,
        vertical_bevel,
        yoke,
        *face_screws,
        *chassis_screws,
    )


def _plate_with_motor_cutouts(
    *,
    inner_radius: float,
    output_axis_radii: tuple[float, float, float],
    architecture: str,
):
    plate = _annulus(inner_radius, P.plate_outer_radius, *P.plate_z)
    for role_index, axis_radius in enumerate(output_axis_radii):
        body_x1 = axis_radius - P.motor_shaft_gap_to_output_axis
        body_x0 = body_x1 - P.motor_body_length
        if architecture == "D":
            cutout_x1 = body_x1 + 0.20 + P.motor_yoke_radial_thickness + 0.30
            side_center = P.motor_face_size / 2.0 + P.motor_cradle_running_clearance + P.motor_cradle_side_thickness / 2.0
            cutout_y = 2.0 * (side_center + P.motor_cradle_side_thickness / 2.0 + 0.15)
        else:
            cutout_x1 = body_x1 + 0.70
            cutout_y = P.motor_face_size + 1.4
        tool = Box(
            cutout_x1 - (body_x0 - 0.70),
            cutout_y,
            P.plate_z[1] - P.plate_z[0] + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location(((body_x0 - 0.70 + cutout_x1) / 2.0, 0.0, P.plate_z[0] - 0.2))).rotate(
            Axis.Z, P.motor_station_angles[role_index]
        )
        plate = plate.cut(tool)
        if architecture == "D":
            for y in (-P.motor_chassis_screw_pitch_y / 2.0, P.motor_chassis_screw_pitch_y / 2.0):
                x, y_world = _polar(P.motor_chassis_screw_radius, P.motor_station_angles[role_index])
                tangent_x, tangent_y = _polar(y, P.motor_station_angles[role_index] + 90.0)
                hole = Cylinder(
                    P.motor_chassis_screw_diameter / 2.0,
                    P.plate_z[1] - P.plate_z[0] + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ).moved(Location((x + tangent_x, y_world + tangent_y, P.plate_z[0] - 0.2)))
                plate = plate.cut(hole)
    if architecture == "D":
        # Each guide tower has a positive through-chassis interface and a
        # shallow integral boss.  The removable post/cap remains a separate
        # service part.
        for angle in P.d_guide_angles:
            x, y = _polar(P.d_guide_axis_radius, angle)
            through = Cylinder(
                P.d_guide_shaft_diameter / 2.0 + 0.10,
                P.plate_z[1] - P.plate_z[0] + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, P.plate_z[0] - 0.2)))
            plate = plate.cut(through)
            # Rear-access counterbore fully clears the D6 retaining collar.
            # Its roof at z=-4.40 is the positive axial stop for the collar;
            # the collar remains removable from the flat rear face.
            rear_counterbore = Cylinder(
                P.d_guide_rear_counterbore_diameter / 2.0,
                P.d_guide_rear_counterbore_z[1] - P.d_guide_rear_counterbore_z[0],
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, P.d_guide_rear_counterbore_z[0])))
            plate = plate.cut(rear_counterbore)
            boss = Cylinder(
                P.d_guide_chassis_boss_diameter / 2.0,
                P.d_guide_chassis_boss_z[1] - P.d_guide_chassis_boss_z[0],
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, P.d_guide_chassis_boss_z[0])))
            boss = boss.cut(Cylinder(
                P.d_guide_shaft_diameter / 2.0 + 0.10,
                P.d_guide_chassis_boss_z[1] - P.d_guide_chassis_boss_z[0] + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, P.d_guide_chassis_boss_z[0] - 0.2))))
            anchor_tunnel = _cylinder_x(
                P.d_guide_anchor_screw_diameter / 2.0 + 0.10,
                P.d_guide_chassis_boss_diameter / 2.0 - P.d_guide_shaft_diameter / 2.0 + 0.4,
                P.d_guide_axis_radius + (
                    P.d_guide_chassis_boss_diameter / 2.0 + P.d_guide_shaft_diameter / 2.0
                ) / 2.0,
                0.0,
                -0.25,
            ).rotate(Axis.Z, angle)
            boss = boss.cut(anchor_tunnel)
            plate = plate.fuse(boss)
    return _tag(plate, f"{architecture}_300mm_OD_6mm_chassis_with_three_motor_service_cutouts", P.plate_color)


@lru_cache(maxsize=1)
def make_D_complete() -> Compound:
    children = [_plate_with_motor_cutouts(inner_radius=P.d_plate_inner_radius, output_axis_radii=P.d_pinion_axes, architecture="D")]
    radial_envelope = (P.d_ring_pitch_radius - 1.0, P.d_ring_body_outer_radius)
    for role_index in range(3):
        carrier, pinion = _ring_and_pinion(
            role_index=role_index,
            teeth=P.d_ring_teeth,
            pitch_radius=P.d_ring_pitch_radius,
            output_axis_radius=P.d_output_axis_radius,
            radial_envelope=radial_envelope,
            layer=P.d_carrier_layers[role_index],
            fin_radius=P.d_fin_radii[role_index],
            fin_tip_z=P.d_fin_tip_zs[role_index],
            architecture="D",
        )
        children.extend((carrier, pinion))
        children.extend(_motor_station(
            role_index=role_index,
            output_axis_radius=P.d_output_axis_radius,
            ring_layer=P.d_carrier_layers[role_index],
            motor_z=P.d_motor_z,
            rear_limit=P.d_rear_limit_z,
            architecture="D",
        ))

    # Three shared towers.  Each post inserts from the rear through the
    # chassis, seats on a positive collar, is locked by a boss set screw, and
    # receives three independent spools plus a removable keeper cap.
    for tower_index, angle in enumerate(P.d_guide_angles, start=1):
        x, y = _polar(P.d_guide_axis_radius, angle)
        shaft = Cylinder(
            P.d_guide_shaft_diameter / 2.0,
            P.d_guide_shaft_z[1] - P.d_guide_shaft_z[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, P.d_guide_shaft_z[0])))
        lower_collar = Cylinder(
            P.d_guide_rear_collar_diameter / 2.0,
            P.d_guide_rear_collar_z[1] - P.d_guide_rear_collar_z[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, P.d_guide_rear_collar_z[0])))
        post = shaft.fuse(lower_collar)
        children.append(_tag(
            post,
            f"D_shared_guide_tower_{tower_index}_D4_post_with_rear_stop_collar",
            "#69767E",
        ))
        # Radial M2 grub screw begins at the D4 post surface and engages the
        # integral chassis boss; it does not float above the plate.
        anchor_local = _cylinder_x(
            P.d_guide_anchor_screw_diameter / 2.0 - 0.05,
            P.d_guide_chassis_boss_diameter / 2.0 - P.d_guide_shaft_diameter / 2.0,
            P.d_guide_axis_radius + (
                P.d_guide_chassis_boss_diameter / 2.0 + P.d_guide_shaft_diameter / 2.0
            ) / 2.0,
            0.0,
            -0.25,
        ).rotate(Axis.Z, angle)
        children.append(_tag(
            anchor_local,
            f"D_shared_guide_tower_{tower_index}_M2_boss_grub_screw",
            "#73797D",
        ))
        for role_index, (z0, z1) in enumerate(P.d_carrier_layers):
            # Locked direct-race contact: the D6 hub spans the carrier and
            # clears the R129 tooth tips; only the D12.1 land reaches the
            # smooth 0.80 mm race below the tooth face.  Wide flanges capture
            # axially outside the carrier without rolling on teeth.
            spool_z0 = z0 - (
                P.d_guide_flange_axial_clearance + P.d_guide_flange_thickness
            )
            spool_z1 = z1 + (
                P.d_guide_flange_axial_clearance + P.d_guide_flange_thickness
            )
            hub = Cylinder(
                P.d_guide_hub_diameter / 2.0,
                spool_z1 - spool_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, spool_z0)))
            running_z0 = z0 + P.d_guide_running_z_offset[0]
            running_z1 = z0 + P.d_guide_running_z_offset[1]
            running = Cylinder(
                P.d_guide_running_diameter / 2.0,
                running_z1 - running_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, running_z0)))
            lower = Cylinder(
                P.d_guide_flange_diameter / 2.0,
                P.d_guide_flange_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, spool_z0)))
            upper = Cylinder(
                P.d_guide_flange_diameter / 2.0,
                P.d_guide_flange_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, z1 + P.d_guide_flange_axial_clearance)))
            spool = hub.fuse(running).fuse(lower).fuse(upper)
            spool_bore = Cylinder(
                P.d_guide_spool_bore_diameter / 2.0,
                spool_z1 - spool_z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, spool_z0 - 0.2)))
            spool = spool.cut(spool_bore)
            children.append(_tag(
                spool,
                f"D_shared_guide_tower_{tower_index}_{P.roles[role_index]}_independent_flanged_spool_D4p2_axial_bore",
                "#7A858B",
            ))
        cap = Cylinder(
            P.d_guide_keeper_cap_diameter / 2.0,
            P.d_guide_keeper_cap_z[1] - P.d_guide_keeper_cap_z[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, P.d_guide_keeper_cap_z[0])))
        cap = cap.cut(Cylinder(
            P.d_guide_shaft_diameter / 2.0 + 0.10,
            P.d_guide_keeper_cap_z[1] - P.d_guide_keeper_cap_z[0] + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, P.d_guide_keeper_cap_z[0] - 0.2))))
        children.append(_tag(
            cap,
            f"D_shared_guide_tower_{tower_index}_removable_keeper_cap_D4p2_bore",
            "#535D63",
        ))
        keeper_screw = _cylinder_x(
            0.95,
            P.d_guide_keeper_cap_diameter / 2.0 - P.d_guide_shaft_diameter / 2.0,
            P.d_guide_axis_radius + (
                P.d_guide_keeper_cap_diameter / 2.0 + P.d_guide_shaft_diameter / 2.0
            ) / 2.0,
            0.0,
            sum(P.d_guide_keeper_cap_z) / 2.0,
        ).rotate(Axis.Z, angle)
        children.append(_tag(
            keeper_screw,
            f"D_shared_guide_tower_{tower_index}_keeper_M2_set_screw",
            "#73797D",
        ))
    return Compound(children=children, label="D_REPAIRED_COMPLETE_compact_split_plane_locked_stack")


@lru_cache(maxsize=1)
def make_E_complete() -> Compound:
    children = [_plate_with_motor_cutouts(inner_radius=P.e_plate_inner_radius, output_axis_radii=P.e_pinion_axis_radii, architecture="E")]
    for role_index in range(3):
        carrier, pinion = _ring_and_pinion(
            role_index=role_index,
            teeth=P.e_ring_teeth[role_index],
            pitch_radius=P.e_pitch_radii[role_index],
            output_axis_radius=P.e_pinion_axis_radii[role_index],
            radial_envelope=P.e_radial_envelopes[role_index],
            layer=P.e_carrier_layer,
            fin_radius=P.e_fin_radii[role_index],
            fin_tip_z=P.e_fin_tip_zs[role_index],
            architecture="E",
        )
        children.extend((carrier, pinion))
        children.extend(_motor_station(
            role_index=role_index,
            output_axis_radius=P.e_pinion_axis_radii[role_index],
            ring_layer=P.e_carrier_layer,
            motor_z=P.e_motor_z,
            rear_limit=P.e_rear_limit_z,
            architecture="E",
        ))

    # Each stationary radial bar carries three radially separate free spools.
    for bar_index, angle in enumerate(P.e_guide_angles, start=1):
        bar = _radial_box(
            8.0,
            P.e_spool_outer_radius,
            8.0,
            P.e_guide_bar_z[0],
            P.e_guide_bar_z[1],
            angle,
        )
        children.append(_tag(bar, f"E_stationary_radial_guide_bar_{bar_index}", "#5E6A72"))
        for role_index, radius in enumerate(P.e_spool_center_radii):
            x, y = _polar(radius, angle)
            lower_z = P.e_carrier_layer[0] - (P.e_spool_groove_width - P.ring_thickness) / 2.0
            upper_z = P.e_carrier_layer[1] + (P.e_spool_groove_width - P.ring_thickness) / 2.0
            running = Cylinder(
                P.e_spool_running_diameter / 2.0,
                upper_z - lower_z,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, lower_z)))
            lower = Cylinder(
                P.e_spool_flange_diameter / 2.0,
                P.e_spool_flange_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((x, y, lower_z)))
            upper = Cylinder(
                P.e_spool_flange_diameter / 2.0,
                P.e_spool_flange_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, upper_z)))
            spool = running.fuse(lower).fuse(upper)
            children.append(_tag(
                spool,
                f"E_guide_bar_{bar_index}_{P.roles[role_index]}_independent_D5_D6_spool",
                "#7A858B",
            ))
    return Compound(
        children=children,
        label="E_REJECTED_COMPARISON_coplanar_radial_lanes_not_a_complete_drive",
    )


def make_D_led_keepout_reference() -> Compound:
    """Separate non-manufacturing central LED/optical keep-out reference.

    This cone is deliberately not part of the primary D STEP or its physical
    Z envelope.  It verifies that the complete mechanical candidate leaves the
    centre open while documenting that the LED module itself remains excluded.
    """

    keepout = Cone(
        P.d_led_keepout_bottom_radius,
        P.d_led_keepout_top_radius,
        P.d_led_keepout_top_z - P.d_led_keepout_bottom_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, P.d_led_keepout_bottom_z)))
    keepout = _tag(
        keepout,
        "REFERENCE_ONLY_D_LED_OPTICAL_KEEP_OUT_NOT_A_PURCHASED_OR_PRINTED_PART",
        "#FFD56A",
    )
    return Compound(children=[keepout], label="D_LED_KEEP_OUT_VALIDATION_REFERENCE_LED_MODULE_EXCLUDED")


def make_D_exploded() -> Compound:
    """True installation-order explosion derived from the repaired assembly."""

    rows = []
    for child in make_D_complete().children:
        label = child.label or "unnamed"
        if "chassis" in label:
            dz = 0.0
        elif "U_cradle" in label or "NEMA8" in label or "chassis_M3" in label:
            dz = -28.0
        elif "horizontal_motor_shaft" in label or "REAL_16T_straight_miter" in label:
            dz = -14.0
        elif "vertical_output_shaft" in label or "positive_drive_pinion" in label:
            dz = 12.0
        elif "carrier_with_integral_fin" in label:
            role = next((i for i, name in enumerate(P.roles) if f"_{name}_" in label), 0)
            dz = 28.0 + 12.0 * role
        elif "independent_flanged_spool" in label:
            role = next((i for i, name in enumerate(P.roles) if f"_{name}_" in label), 0)
            dz = 28.0 + 12.0 * role
        elif "guide_tower" in label and "post_with" in label:
            dz = 18.0
        elif "keeper" in label:
            dz = 66.0
        else:
            dz = -14.0
        moved = child.moved(Location((0.0, 0.0, dz)))
        moved.label = f"INSTALL_ORDER_dz_{dz:+05.1f}_{label}"
        moved.color = child.color
        rows.append(moved)
    return Compound(children=rows, label="D_TRUE_EXPLODED_INSTALLATION_ORDER")


def _true_side_section(source: Compound, label: str) -> Compound:
    cutter = Box(320.0, 18.0, 50.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    rows = []
    for child in source.children:
        section = child.intersect(cutter)
        if not section or not section.solids():
            continue
        for solid_index, source_solid in enumerate(section.solids(), start=1):
            solid = Solid(source_solid.wrapped)
            solid.label = f"{label}_CUT_{child.label}_{solid_index:02d}"
            solid.color = child.color
            rows.append(solid)
    return Compound(children=rows, label=label)


def make_D_true_side_section() -> Compound:
    return _true_side_section(make_D_complete(), "D_REPAIRED_TRUE_SIDE_SECTION_from_complete_geometry")


def make_E_true_side_section() -> Compound:
    return _true_side_section(make_E_complete(), "E_REJECTED_TRUE_SIDE_SECTION_comparison_only")


def make_side_by_side() -> Compound:
    d = make_D_complete().moved(Location((-180.0, 0.0, 0.0)))
    d.label = "D_REPAIRED_COMPLETE_at_left"
    e = make_E_complete().moved(Location((180.0, 0.0, 0.0)))
    e.label = "E_REJECTED_COMPARISON_at_right"
    return Compound(children=[d, e], label="D_COMPLETE_vs_E_REJECTED_SIDE_BY_SIDE_non_overlapping")
