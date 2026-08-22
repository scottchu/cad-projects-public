"""KAGE P3 V3 three-tower direct-spool correction geometry."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, pi, radians, sin

import py_gearworks as pgw
from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude
from cadgen import srgb

from p3_v3_roller_tower_spec import P3V3RollerTowerSpec, P3_V3_ROLLER_TOWER
from p3_v3_full_ring_r2_geometry import (
    _annulus,
    _polar,
    _quarter_annulus,
    make_fin,
    make_frame_segments,
    make_outer_front_ring_posts,
    make_outer_front_ring_segments,
    make_motor_station_parts as base_make_motor_station_parts,
    make_station_support as base_make_station_support,
    make_seam_hardware,
)


def _radial_slot_tool(center_radius, tangent, travel, diameter, z0, height):
    radius = diameter / 2.0
    left = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius - travel / 2.0, tangent, z0))
    )
    right = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius + travel / 2.0, tangent, z0))
    )
    bridge = Box(travel, diameter, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius, tangent, z0))
    )
    return left.fuse(bridge).fuse(right)


@lru_cache(maxsize=3)
def _full_role_ring(role_index: int):
    """Accepted carrier with only the rear guide land locally simplified."""

    spec = P3_V3_ROLLER_TOWER
    layer_z0, layer_z1 = spec.carrier_layers[role_index]
    face_z0, face_z1 = spec.pinion_face_ranges[role_index]
    teeth = pgw.SpurRingGear(
        number_of_teeth=spec.ring_teeth,
        module=spec.module,
        height=face_z1 - face_z0,
        center=[0.0, 0.0, face_z0],
        backlash=0.10,
    ).build_part().solid().rotate(Axis.Z, spec.tooth_phase_offset_degrees)
    body = _annulus(
        spec.ring_body_inner_radius,
        spec.ring_body_outer_radius,
        layer_z1 - layer_z0,
        layer_z0,
    )
    head_z0, head_z1 = spec.guide_head_range(role_index)
    head = _annulus(
        spec.guide_head_radii[0],
        spec.guide_head_radii[1],
        head_z1 - head_z0,
        head_z0,
    )
    neck_z0, neck_z1 = spec.guide_neck_range(role_index)
    neck = _annulus(
        spec.guide_neck_radii[0],
        spec.guide_neck_radii[1],
        neck_z1 - neck_z0,
        neck_z0,
    )
    ring = teeth.fuse(body).fuse(neck).fuse(head)
    for angle in (
        spec.joint_hole_edge_angle_degrees,
        spec.quadrant_angle_degrees - spec.joint_hole_edge_angle_degrees,
    ):
        x, y = _polar(spec.joint_hole_radius, angle)
        ring = ring.cut(
            Cylinder(
                spec.joint_hole_diameter / 2.0,
                layer_z1 - head_z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, head_z0 - 0.2)))
        )
    for angle in (0.0, 90.0, 180.0, 270.0):
        x, y = _polar(spec.registration_dowel_radius, angle)
        ring = ring.cut(
            Cylinder(
                spec.registration_dowel_diameter / 2.0,
                layer_z1 - layer_z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, layer_z0 - 0.2)))
        )
    return ring


@lru_cache(maxsize=3)
def _canonical_quadrant(role_index: int):
    spec = P3_V3_ROLLER_TOWER
    _, z1 = spec.carrier_layers[role_index]
    guide_z0, _ = spec.guide_head_range(role_index)
    size = spec.ring_outer_radius + 1.0
    crop = Box(
        size,
        size,
        z1 - guide_z0 + 0.8,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((0.0, 0.0, guide_z0 - 0.4)))
    pieces = _full_role_ring(role_index).intersect(crop)
    if not pieces:
        raise ValueError("260T ring quadrant crop produced no solid")
    return max(pieces, key=lambda shape: shape.volume)


def make_ring_quadrant(role_index, quadrant_index, spec=P3_V3_ROLLER_TOWER):
    if not 0 <= quadrant_index < spec.quadrant_count:
        raise ValueError("quadrant index outside 0..3")
    quadrant = deepcopy(_canonical_quadrant(role_index)).rotate(
        Axis.Z, quadrant_index * spec.quadrant_angle_degrees
    )
    fin_quadrant = int(spec.display_fin_angles[role_index] // spec.quadrant_angle_degrees)
    if quadrant_index == fin_quadrant:
        quadrant = quadrant.fuse(make_fin(role_index, spec))
    quadrant.label = (
        f"p3_v3_roller_{spec.roles[role_index]}_M1_260T_"
        f"quadrant_Q{quadrant_index + 1}_65T"
    )
    quadrant.color = srgb(spec.role_colors[role_index])
    return quadrant


def make_ring_quadrants(role_index, spec=P3_V3_ROLLER_TOWER):
    return tuple(make_ring_quadrant(role_index, q, spec) for q in range(4))


def make_fin_360_sweep(role_index, spec=P3_V3_ROLLER_TOWER):
    blade_r0, blade_r1 = spec.fin_blade_radial_ranges[role_index]
    blade = _annulus(
        blade_r0,
        blade_r1,
        spec.fin_tip_zs[role_index] - spec.fin_blade_start_zs[role_index],
        spec.fin_blade_start_zs[role_index],
    )
    root_r = spec.fin_root_radial_ranges[role_index]
    root_z = spec.fin_root_z_ranges[role_index]
    if root_r is not None and root_z is not None:
        blade = blade.fuse(_annulus(root_r[0], root_r[1], root_z[1] - root_z[0], root_z[0]))
    blade.label = f"p3_v3_roller_{spec.roles[role_index]}_fin_exact_360_sweep_envelope"
    return blade


def make_roller(role_index, tower_index, axis_radius=None, spec=P3_V3_ROLLER_TOWER):
    """One replaceable direct-running flanged spool on the common D4 pin."""

    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    running_z0, running_z1 = spec.roller_running_range(role_index)
    z0, z1 = spec.roller_range(role_index)
    spool = Cylinder(
        spec.roller_hub_outer_diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z0))).fuse(Cylinder(
        spec.roller_running_outer_diameter / 2.0,
        running_z1 - running_z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, running_z0))))
    for flange_z0, flange_z1 in spec.roller_flange_ranges(role_index):
        spool = spool.fuse(
            Cylinder(
                spec.roller_flange_outer_diameter / 2.0,
                flange_z1 - flange_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((axis, 0.0, flange_z0)))
        )
    spool = spool.cut(
        Cylinder(
            spec.roller_bore_diameter / 2.0,
            z1 - z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, z0 - 0.2)))
    ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
    spool.label = (
        f"p3_v3_roller_tower_{tower_index + 1}_{spec.roles[role_index]}_"
        f"independent_direct_flanged_spool_{spec.roller_material}"
    )
    spool.color = srgb(spec.role_colors[role_index])
    return spool


def make_tower_base(tower_index, axis_radius=None, spec=P3_V3_ROLLER_TOWER):
    """One connected two-sided tower with symmetric radial setup slots."""

    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    angle = spec.roller_tower_angles[tower_index]
    z0, z1 = spec.tower_base_z_range
    base = Box(
        spec.tower_base_radial_range[1] - spec.tower_base_radial_range[0],
        spec.tower_base_tangential_width,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((sum(spec.tower_base_radial_range) / 2.0, 0.0, z0)))
    lower_roller_bottom = spec.roller_range(0)[0]
    sleeve = Cylinder(
        spec.tower_post_outer_diameter / 2.0,
        lower_roller_bottom - z1 - spec.tower_post_top_clearance,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z1)))
    tower = base.fuse(sleeve)

    bridge_z0, bridge_z1 = spec.tower_top_bridge_z_range
    for tangent in spec.tower_backbone_tangent_offsets:
        tower = tower.fuse(
            Box(
                spec.tower_backbone_section,
                spec.tower_backbone_section,
                bridge_z1 - z1,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.tower_backbone_radius, tangent, z1)))
        )
    bridge_r0, bridge_r1 = spec.tower_top_bridge_radial_range
    bridge = Box(
        bridge_r1 - bridge_r0,
        spec.tower_top_bridge_tangential_width,
        bridge_z1 - bridge_z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((bridge_r0, 0.0, bridge_z0)))
    upper_z0, upper_z1 = spec.tower_upper_bushing_z_range
    bushing = Cylinder(
        spec.tower_upper_bushing_outer_diameter / 2.0,
        upper_z1 - upper_z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, upper_z0))).cut(
        Cylinder(
            spec.tower_upper_bushing_bore_diameter / 2.0,
            upper_z1 - upper_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, upper_z0 - 0.2)))
    )
    tower = tower.fuse(bridge).fuse(bushing)
    tower = tower.cut(
        Cylinder(
            spec.tower_axle_clearance_diameter / 2.0,
            spec.tower_lower_socket_depth + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, spec.tower_axle_z0 - 0.1)))
    )
    for tangent in spec.tower_mount_tangent_offsets:
        tower = tower.cut(
            _radial_slot_tool(
                spec.tower_mount_axis_radius,
                tangent,
                spec.tower_preload_slot_travel,
                spec.tower_mount_clearance_diameter,
                z0 - 0.2,
                z1 - z0 + 0.4,
            )
        )
    tower = tower.rotate(Axis.Z, angle)
    tower.label = (
        f"p3_v3_roller_tower_{tower_index + 1}_symmetric_radial_slots_"
        "single_connected_two_sided_yoke"
    )
    tower.color = srgb("#69737A")
    return tower


def make_tower_spacers(tower_index, axis_radius=None, spec=P3_V3_ROLLER_TOWER):
    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    parts = []
    ranges = [spec.roller_range(role) for role in range(3)]
    for index in range(2):
        z0 = ranges[index][1]
        z1 = z0 + spec.roller_spacer_lengths[index]
        spacer = Cylinder(
            spec.roller_spacer_outer_diameter / 2.0,
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, z0))).cut(
            Cylinder(
                spec.roller_spacer_bore_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((axis, 0.0, z0 - 0.2)))
        ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
        spacer.label = f"p3_v3_roller_tower_{tower_index + 1}_spacer_{index + 1}"
        spacer.color = srgb("#D8D0C2")
        parts.append(spacer)
    return tuple(parts)


def make_tower_thrust_washers(tower_index, axis_radius=None, spec=P3_V3_ROLLER_TOWER):
    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    parts = []
    for name, (z0, z1) in (
        ("lower", spec.lower_thrust_washer_range),
        ("upper", spec.upper_thrust_washer_range),
    ):
        washer = Cylinder(
            spec.roller_thrust_washer_outer_diameter / 2.0,
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, z0))).cut(
            Cylinder(
                spec.roller_thrust_washer_bore_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((axis, 0.0, z0 - 0.2)))
        ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
        washer.label = f"p3_v3_roller_tower_{tower_index + 1}_{name}_thrust_washer"
        washer.color = srgb("#D8D0C2")
        parts.append(washer)
    return tuple(parts)


def _outward_radial_cylinder(axis, z, angle, diameter, length, start_offset=0.0):
    """Cylinder running radially outward from the local tower axis."""

    tool = Cylinder(diameter / 2.0, length, align=(Align.CENTER, Align.CENTER, Align.MIN))
    tool = tool.rotate(Axis.Y, 90.0).moved(Location((axis + start_offset, 0.0, z)))
    return tool.rotate(Axis.Z, angle)


def _hex_prism(center_x, center_y, z0, across_flats, height):
    radius = across_flats / (3.0 ** 0.5)
    points = [
        (
            center_x + radius * cos(pi / 6.0 + index * pi / 3.0),
            center_y + radius * sin(pi / 6.0 + index * pi / 3.0),
        )
        for index in range(6)
    ]
    return extrude(Polygon(*points), amount=height).moved(Location((0.0, 0.0, z0)))


def make_tower_hardware_references(tower_index, axis_radius=None, spec=P3_V3_ROLLER_TOWER):
    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    angle = spec.roller_tower_angles[tower_index]
    axle = Cylinder(
        spec.tower_axle_nominal_diameter / 2.0,
        spec.tower_axle_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, spec.tower_axle_z0))).rotate(Axis.Z, angle)
    axle.label = f"p3_v3_roller_tower_{tower_index + 1}_4x20_smooth_pin_REFERENCE"
    axle.color = srgb("#59636A")

    collar_z0, collar_z1 = spec.tower_retainer_collar_z_range
    collar_height = collar_z1 - collar_z0
    collar = Cylinder(
        spec.tower_retainer_collar_outer_diameter / 2.0,
        collar_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, collar_z0))).cut(
        Cylinder(
            spec.tower_retainer_collar_bore_diameter / 2.0,
            collar_height + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, collar_z0 - 0.2)))
    )
    set_z = (collar_z0 + collar_z1) / 2.0
    collar = collar.rotate(Axis.Z, angle).cut(
        _outward_radial_cylinder(
            axis,
            set_z,
            angle,
            spec.tower_collar_set_screw_pilot_diameter,
            (
                spec.tower_retainer_collar_outer_diameter
                - spec.tower_retainer_collar_bore_diameter
            )
            / 2.0
            + 0.4,
            spec.tower_retainer_collar_bore_diameter / 2.0 - 0.2,
        )
    )
    collar.label = (
        f"p3_v3_roller_tower_{tower_index + 1}_purchased_D4x10x4_"
        "metal_M2_set_screw_collar_REFERENCE"
    )
    collar.color = srgb("#59636A")
    set_screw = _outward_radial_cylinder(
        axis,
        set_z,
        angle,
        spec.tower_collar_set_screw_nominal_diameter,
        spec.tower_collar_set_screw_length,
        0.0,
    )
    set_screw.label = f"p3_v3_roller_tower_{tower_index + 1}_M2_collar_set_screw_REFERENCE"
    set_screw.color = srgb("#59636A")
    parts = [axle, collar, set_screw]
    for index, tangent in enumerate(spec.tower_mount_tangent_offsets):
        shaft_z0 = spec.chassis_z[0]
        screw_shaft = Cylinder(
            spec.tower_mount_bolt_diameter / 2.0,
            spec.tower_mount_bolt_length,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.tower_mount_axis_radius, tangent, shaft_z0)))
        screw_head = Cylinder(
            spec.tower_mount_socket_head_diameter / 2.0,
            spec.tower_mount_socket_head_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(
            Location(
                (
                    spec.tower_mount_axis_radius,
                    tangent,
                    shaft_z0 - spec.tower_mount_socket_head_height,
                )
            )
        )
        screw = screw_shaft.fuse(screw_head).rotate(Axis.Z, angle)
        screw.label = f"p3_v3_roller_tower_{tower_index + 1}_M3_mount_screw_{index + 1}_REFERENCE"
        screw.color = srgb("#59636A")
        parts.append(screw)
        washer = Cylinder(
            spec.tower_mount_washer_outer_diameter / 2.0,
            spec.tower_mount_washer_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.tower_mount_axis_radius, tangent, spec.tower_base_z_range[1])))
        washer = washer.cut(
            Cylinder(
                spec.tower_mount_clearance_diameter / 2.0,
                spec.tower_mount_washer_thickness + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(
                Location(
                    (
                        spec.tower_mount_axis_radius,
                        tangent,
                        spec.tower_base_z_range[1] - 0.2,
                    )
                )
            )
        ).rotate(Axis.Z, angle)
        washer.label = f"p3_v3_roller_tower_{tower_index + 1}_M3_washer_{index + 1}_REFERENCE"
        washer.color = srgb("#59636A")
        parts.append(washer)
        nut_z0 = spec.tower_base_z_range[1] + spec.tower_mount_washer_thickness
        nut = _hex_prism(
            spec.tower_mount_axis_radius,
            tangent,
            nut_z0,
            spec.tower_mount_hex_nut_across_flats,
            spec.tower_mount_hex_nut_thickness,
        ).cut(
            Cylinder(
                spec.tower_mount_bolt_diameter / 2.0,
                spec.tower_mount_hex_nut_thickness + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.tower_mount_axis_radius, tangent, nut_z0 - 0.2)))
        ).rotate(Axis.Z, angle)
        nut.label = f"p3_v3_roller_tower_{tower_index + 1}_M3_hex_nut_{index + 1}_REFERENCE"
        nut.color = srgb("#59636A")
        parts.append(nut)
    return tuple(parts)


def make_capture_cheeks(role_index, tower_index, spec=P3_V3_ROLLER_TOWER):
    return ()


def make_tower_module(tower_index, axis_radius=None, spec=P3_V3_ROLLER_TOWER):
    children = [make_tower_base(tower_index, axis_radius, spec)]
    children.extend(make_tower_spacers(tower_index, axis_radius, spec))
    children.extend(make_tower_thrust_washers(tower_index, axis_radius, spec))
    children.extend(make_roller(role, tower_index, axis_radius, spec) for role in range(3))
    children.extend(make_tower_hardware_references(tower_index, axis_radius, spec))
    return Compound(children=children, label=f"p3_v3_roller_tower_{tower_index + 1}_complete_module")


def make_motor_station_parts(role_index, spec=P3_V3_ROLLER_TOWER):
    return base_make_motor_station_parts(role_index, spec)


def make_station_support(role_index, spec=P3_V3_ROLLER_TOWER):
    return base_make_station_support(role_index, spec)


def make_chassis_segments(spec=P3_V3_ROLLER_TOWER):
    parts = []
    for q in range(4):
        part = _quarter_annulus(*spec.chassis_radii, *spec.chassis_z, q)
        for angle in spec.roller_tower_angles:
            rad = radians(angle)
            for tangent in spec.tower_mount_tangent_offsets:
                local_x = spec.tower_mount_axis_radius
                hx = local_x * cos(rad) - tangent * sin(rad)
                hy = local_x * sin(rad) + tangent * cos(rad)
                part = part.cut(
                    Cylinder(
                        spec.tower_mount_clearance_diameter / 2.0,
                        spec.chassis_z[1] - spec.chassis_z[0] + 0.4,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    ).moved(Location((hx, hy, spec.chassis_z[0] - 0.2)))
                )
        part.label = f"p3_v3_roller_rear_chassis_Q{q + 1}_with_symmetric_tower_M3_slots"
        part.color = srgb("#59636A")
        parts.append(part)
    return tuple(parts)


def make_stationary_module(spec=P3_V3_ROLLER_TOWER):
    children = [*make_chassis_segments(spec), *make_frame_segments(spec)]
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(make_outer_front_ring_segments(spec))
    for tower in range(3):
        children.extend(make_tower_module(tower, spec=spec).children)
    return Compound(children=children, label="p3_v3_roller_stationary_chassis_and_three_towers")


def make_role_module(role_index, spec=P3_V3_ROLLER_TOWER):
    children = [*make_ring_quadrants(role_index, spec)]
    children.extend(make_seam_hardware(role_index, spec))
    children.extend(make_motor_station_parts(role_index, spec))
    children.append(make_station_support(role_index, spec))
    return Compound(children=children, label=f"p3_v3_roller_{spec.roles[role_index]}_role_module")


def make_assembled(spec=P3_V3_ROLLER_TOWER):
    children = list(make_stationary_module(spec).children)
    for role in range(3):
        children.extend(make_role_module(role, spec).children)
    return Compound(children=children, label="p3_v3_roller_COMPLETE_three_ring_three_motor_assembly")


def make_stationary_service_module(spec=P3_V3_ROLLER_TOWER):
    children = [*make_chassis_segments(spec)]
    children.extend(part.moved(Location((0.0, 0.0, 4.0))) for part in make_frame_segments(spec))
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(part.moved(Location((0.0, 0.0, 58.0))) for part in make_outer_front_ring_segments(spec))
    for tower in range(3):
        angle = spec.roller_tower_angles[tower]
        dx, dy = _polar(12.0, angle)
        children.append(make_tower_base(tower, spec=spec))
        children.extend(part.moved(Location((dx, dy, 16.0))) for part in make_tower_spacers(tower, spec=spec))
        children.extend(part.moved(Location((dx, dy, 16.0))) for part in make_tower_thrust_washers(tower, spec=spec))
        for role in range(3):
            children.append(make_roller(role, tower, spec=spec).moved(Location((dx, dy, 16.0))))
        children.extend(
            part.moved(Location((dx, dy, 30.0)))
            for part in make_tower_hardware_references(tower, spec=spec)
        )
    return Compound(children=children, label="p3_v3_roller_stationary_service_module")


def make_role_service_module(role_index, spec=P3_V3_ROLLER_TOWER):
    z_lift = 15.0 + 13.0 * role_index
    radial = 8.0 * role_index
    children = [
        quadrant.moved(Location((radial, 0.0, z_lift)))
        for quadrant in make_ring_quadrants(role_index, spec)
    ]
    children.extend(
        hardware.moved(Location((radial, 0.0, z_lift)))
        for hardware in make_seam_hardware(role_index, spec)
    )
    children.extend(
        part.moved(Location((0.0, 0.0, -12.0 - 8.0 * role_index)))
        for part in make_motor_station_parts(role_index, spec)
    )
    children.append(make_station_support(role_index, spec))
    return Compound(children=children, label=f"p3_v3_roller_{spec.roles[role_index]}_service_module")


def make_service_exploded(spec=P3_V3_ROLLER_TOWER):
    children = list(make_stationary_service_module(spec).children)
    for role in range(3):
        children.extend(make_role_service_module(role, spec).children)
    return Compound(children=children, label="p3_v3_roller_COMPLETE_service_exploded")


PRIMARY_FACTORIES = (("assembled", make_assembled), ("service_exploded", make_service_exploded))
