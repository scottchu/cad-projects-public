"""STEP-first geometry for the KAGE V3 MR84/profiled-spool tower successor.

The accepted keeper-fix ring quadrants, fins, seam hardware, gears and motor
stations are reused directly. Only the stationary chassis mounting holes and
three shared roller towers are new.
"""

from __future__ import annotations

from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location
from cadgen import srgb

from p3_v3_full_ring_r2_geometry import (
    _annulus,
    _full_role_ring as accepted_full_role_ring,
    _polar,
    _quarter_annulus,
    make_fin,
    make_frame_segments,
    make_motor_station_parts as accepted_motor_station_parts,
    make_outer_front_ring_posts,
    make_outer_front_ring_segments,
    make_ring_quadrants as accepted_ring_quadrants,
    make_seam_hardware,
    make_station_support as accepted_station_support,
)
from p3_v3_mr84_spool_tower_spec import (
    P3V3MR84SpoolTowerSpec,
    P3_V3_MR84_SPOOL_TOWER,
)


def _intersection_volume(left, right) -> float:
    common = left.intersect(right)
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _radial_slot_tool(center_radius, tangent, travel, diameter, z0, height):
    radius = diameter / 2.0
    a = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius - travel / 2.0, tangent, z0))
    )
    b = Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius + travel / 2.0, tangent, z0))
    )
    bridge = Box(travel, diameter, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((center_radius, tangent, z0))
    )
    return a.fuse(bridge).fuse(b)


def make_roller_bearing(role_index, tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    z0, z1 = spec.bearing_range(role_index)
    bearing = Cylinder(
        spec.bearing_outer_diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z0))).cut(
        Cylinder(
            spec.bearing_bore_diameter / 2.0,
            z1 - z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, z0 - 0.2)))
    ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
    bearing.label = (
        f"p3_v3_mr84_tower_{tower_index + 1}_{spec.roles[role_index]}_"
        f"independent_{spec.bearing_code}_REFERENCE"
    )
    bearing.color = srgb("#B9C0C5")
    return bearing


def make_roller_spool(role_index, tower_index, axis_radius=None, z_shift=0.0, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    hub_z0, hub_z1 = spec.hub_range(role_index)
    hub_z0 += z_shift
    hub_z1 += z_shift
    spool = Cylinder(
        spec.spool_hub_outer_diameter / 2.0,
        hub_z1 - hub_z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, hub_z0)))
    belt_z0, belt_z1 = spec.belt_range(role_index)
    belt_z0 += z_shift
    belt_z1 += z_shift
    spool = spool.fuse(
        Cylinder(
            spec.spool_belt_outer_diameter / 2.0,
            belt_z1 - belt_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, belt_z0)))
    )
    for lip_z0, lip_z1 in spec.lip_ranges(role_index):
        spool = spool.fuse(
            Cylinder(
                spec.spool_lip_outer_diameter / 2.0,
                lip_z1 - lip_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((axis, 0.0, lip_z0 + z_shift)))
        )
    spool = spool.cut(
        Cylinder(
            spec.spool_hub_bore_diameter / 2.0,
            hub_z1 - hub_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, hub_z0 - 0.2)))
    ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
    spool.label = (
        f"p3_v3_mr84_tower_{tower_index + 1}_{spec.roles[role_index]}_"
        f"profiled_spool_{spec.spool_material}"
    )
    spool.color = srgb(spec.role_colors[role_index])
    return spool


def make_tower_lower(tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    z0, z1 = spec.base_z_range
    base = Box(
        spec.base_radial_range[1] - spec.base_radial_range[0],
        spec.base_tangential_width,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((sum(spec.base_radial_range) / 2.0, 0.0, z0)))
    sleeve = Cylinder(
        spec.post_outer_diameter / 2.0,
        spec.lower_shim_range[0] - z1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z1)))
    tower = base.fuse(sleeve)
    for tangent in spec.backbone_tangent_offsets:
        column = Box(
            spec.backbone_section,
            spec.backbone_section,
            spec.column_top_z - z1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.backbone_radius, tangent, z1)))
        pilot = Cylinder(
            (spec.yoke_bolt_diameter - 0.4) / 2.0,
            spec.yoke_bolt_length + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((spec.yoke_fastener_axis_radius, tangent, spec.column_top_z + 0.2)))
        tower = tower.fuse(column.cut(pilot))
    socket_z0, socket_z1 = spec.lower_socket_z_range
    tower = tower.cut(
        Cylinder(
            spec.lower_socket_bore_diameter / 2.0,
            socket_z1 - socket_z0 + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, socket_z0 - 0.1)))
    )
    for tangent in spec.base_mount_tangent_offsets:
        if tower_index == spec.adjustable_tower_index:
            hole = _radial_slot_tool(
                spec.base_mount_axis_radius,
                tangent,
                spec.adjustable_slot_travel,
                spec.base_mount_clearance_diameter,
                z0 - 0.2,
                z1 - z0 + 0.4,
            )
        else:
            hole = Cylinder(
                spec.base_mount_clearance_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.base_mount_axis_radius, tangent, z0 - 0.2)))
        tower = tower.cut(hole)
    tower = tower.rotate(Axis.Z, spec.roller_tower_angles[tower_index])
    datum = "adjustable_R126p35_to_R126p45" if tower_index == 2 else "fixed_round_datum"
    tower.label = f"p3_v3_mr84_tower_{tower_index + 1}_{datum}_lower_socket_columns"
    tower.color = srgb("#69737A")
    return tower


def make_tower_upper_yoke(tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    z0, z1 = spec.yoke_z_range
    r0, r1 = spec.yoke_radial_range
    yoke = Box(
        r1 - r0,
        spec.yoke_tangential_width,
        z1 - z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((r0, 0.0, z0)))
    bz0, bz1 = spec.upper_bushing_z_range
    bushing = Cylinder(
        spec.upper_bushing_outer_diameter / 2.0,
        bz1 - bz0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, bz0))).cut(
        Cylinder(
            spec.upper_bushing_bore_diameter / 2.0,
            bz1 - bz0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, bz0 - 0.2)))
    )
    yoke = yoke.fuse(bushing)
    for tangent in spec.yoke_fastener_tangent_offsets:
        yoke = yoke.cut(
            Cylinder(
                spec.yoke_clearance_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((spec.yoke_fastener_axis_radius, tangent, z0 - 0.2)))
        )
    yoke = yoke.rotate(Axis.Z, spec.roller_tower_angles[tower_index])
    yoke.label = f"p3_v3_mr84_tower_{tower_index + 1}_removable_upper_yoke_2xM3x8"
    yoke.color = srgb("#8A949A")
    return yoke


def make_spacers(tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    parts = []
    for index in range(2):
        z0, z1 = spec.spacer_range(index)
        part = Cylinder(
            spec.spacer_outer_diameter / 2.0,
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, z0))).cut(
            Cylinder(
                spec.spacer_bore_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((axis, 0.0, z0 - 0.2)))
        ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
        part.label = f"p3_v3_mr84_tower_{tower_index + 1}_D6_D4p1_L2p55_spacer_{index + 1}"
        part.color = srgb("#D8D0C2")
        parts.append(part)
    return tuple(parts)


def make_shims(tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    parts = []
    for name, (z0, z1) in (("lower", spec.lower_shim_range), ("upper", spec.upper_shim_range)):
        part = Cylinder(
            spec.shim_outer_diameter / 2.0,
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, z0))).cut(
            Cylinder(
                spec.shim_bore_diameter / 2.0,
                z1 - z0 + 0.4,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((axis, 0.0, z0 - 0.2)))
        ).rotate(Axis.Z, spec.roller_tower_angles[tower_index])
        part.label = f"p3_v3_mr84_tower_{tower_index + 1}_{name}_0p20_inner_race_shim"
        part.color = srgb("#D8D0C2")
        parts.append(part)
    return tuple(parts)


def make_hardware(tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    axis = spec.axle_axis_radius if axis_radius is None else axis_radius
    angle = spec.roller_tower_angles[tower_index]
    az0, az1 = spec.axle_z_range
    axle = Cylinder(
        spec.axle_shoulder_diameter / 2.0,
        az1 - az0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, az0)))
    sz0, sz1 = spec.upper_stack_shoulder_z_range
    axle = axle.fuse(
        Cylinder(
            spec.upper_stack_shoulder_outer_diameter / 2.0,
            sz1 - sz0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, sz0)))
    )
    tz0, _ = spec.axle_thread_z_range
    axle = axle.cut(
        Cylinder(
            spec.axle_internal_thread_diameter / 2.0,
            az1 - tz0 + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, tz0)))
    ).rotate(Axis.Z, angle)
    axle.label = f"p3_v3_mr84_tower_{tower_index + 1}_D3p985_two_end_supported_axle_M3_tapped"
    axle.color = srgb("#59636A")

    hz0, hz1 = spec.retainer_head_z_range
    core = Cylinder(
        spec.retainer_thread_diameter / 2.0,
        hz1 - tz0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, tz0)))
    head = Cylinder(
        spec.retainer_outer_diameter / 2.0,
        hz1 - hz0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, hz0)))
    retainer = core.fuse(head).rotate(Axis.Z, angle)
    retainer.label = f"p3_v3_mr84_tower_{tower_index + 1}_removable_M3_threaded_retainer_REFERENCE"
    retainer.color = srgb("#59636A")
    parts = [axle, retainer]

    for index, tangent in enumerate(spec.base_mount_tangent_offsets):
        screw = Cylinder(
            spec.base_mount_bolt_diameter / 2.0,
            spec.base_mount_bolt_length,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((spec.base_mount_axis_radius, tangent, spec.chassis_z[0] - 1.5)))
        screw = screw.rotate(Axis.Z, angle)
        screw.label = f"p3_v3_mr84_tower_{tower_index + 1}_M3x10_base_screw_{index + 1}_REFERENCE"
        screw.color = srgb("#59636A")
        parts.append(screw)
    for index, tangent in enumerate(spec.yoke_fastener_tangent_offsets):
        screw = Cylinder(
            spec.yoke_bolt_diameter / 2.0,
            spec.yoke_bolt_length,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((spec.yoke_fastener_axis_radius, tangent, spec.yoke_z_range[1])))
        screw = screw.rotate(Axis.Z, angle)
        screw.label = f"p3_v3_mr84_tower_{tower_index + 1}_M3x8_yoke_screw_{index + 1}_REFERENCE"
        screw.color = srgb("#59636A")
        parts.append(screw)
    return tuple(parts)


def make_tower_module(tower_index, axis_radius=None, spec=P3_V3_MR84_SPOOL_TOWER):
    children = [
        make_tower_lower(tower_index, axis_radius, spec),
        make_tower_upper_yoke(tower_index, axis_radius, spec),
        *make_spacers(tower_index, axis_radius, spec),
        *make_shims(tower_index, axis_radius, spec),
    ]
    for role in range(3):
        children.append(make_roller_bearing(role, tower_index, axis_radius, spec))
        children.append(make_roller_spool(role, tower_index, axis_radius, 0.0, spec))
    children.extend(make_hardware(tower_index, axis_radius, spec))
    return Compound(children=children, label=f"p3_v3_mr84_tower_{tower_index + 1}_complete")


def make_fin_360_sweep(role_index, spec=P3_V3_MR84_SPOOL_TOWER):
    r0, r1 = spec.fin_blade_radial_ranges[role_index]
    sweep = _annulus(r0, r1, spec.fin_tip_zs[role_index] - spec.fin_blade_start_zs[role_index], spec.fin_blade_start_zs[role_index])
    rr = spec.fin_root_radial_ranges[role_index]
    rz = spec.fin_root_z_ranges[role_index]
    if rr is not None and rz is not None:
        sweep = sweep.fuse(_annulus(rr[0], rr[1], rz[1] - rz[0], rz[0]))
    sweep.label = f"p3_v3_{spec.roles[role_index]}_fin_exact_360_sweep"
    return sweep


def make_chassis_segments(spec=P3_V3_MR84_SPOOL_TOWER):
    parts = []
    for q in range(4):
        part = _quarter_annulus(*spec.chassis_radii, *spec.chassis_z, q)
        for angle in spec.roller_tower_angles:
            rad = radians(angle)
            for tangent in spec.base_mount_tangent_offsets:
                x = spec.base_mount_axis_radius * cos(rad) - tangent * sin(rad)
                y = spec.base_mount_axis_radius * sin(rad) + tangent * cos(rad)
                part = part.cut(
                    Cylinder(
                        spec.base_mount_clearance_diameter / 2.0,
                        spec.chassis_z[1] - spec.chassis_z[0] + 0.4,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    ).moved(Location((x, y, spec.chassis_z[0] - 0.2)))
                )
        part.label = f"p3_v3_mr84_rear_chassis_Q{q + 1}_tower_mount_paths"
        part.color = srgb("#59636A")
        parts.append(part)
    return tuple(parts)


def make_stationary_module(spec=P3_V3_MR84_SPOOL_TOWER):
    children = [*make_chassis_segments(spec), *make_frame_segments(spec)]
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(make_outer_front_ring_segments(spec))
    for tower in range(3):
        children.extend(make_tower_module(tower, spec=spec).children)
    return Compound(children=children, label="p3_v3_mr84_stationary_frame_three_supported_towers")


def make_role_module(role_index, spec=P3_V3_MR84_SPOOL_TOWER):
    children = [*accepted_ring_quadrants(role_index, spec)]
    children.extend(make_seam_hardware(role_index, spec))
    children.extend(accepted_motor_station_parts(role_index, spec))
    children.append(accepted_station_support(role_index, spec))
    return Compound(children=children, label=f"p3_v3_mr84_{spec.roles[role_index]}_accepted_role_module")


def make_assembled(spec=P3_V3_MR84_SPOOL_TOWER):
    children = list(make_stationary_module(spec).children)
    for role in range(3):
        children.extend(make_role_module(role, spec).children)
    return Compound(children=children, label="p3_v3_mr84_COMPLETE_three_ring_three_motor_roller_assembly")


def make_stationary_service_module(spec=P3_V3_MR84_SPOOL_TOWER):
    children = [*make_chassis_segments(spec)]
    children.extend(part.moved(Location((0.0, 0.0, 4.0))) for part in make_frame_segments(spec))
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(part.moved(Location((0.0, 0.0, 62.0))) for part in make_outer_front_ring_segments(spec))
    for tower in range(3):
        angle = spec.roller_tower_angles[tower]
        dx, dy = _polar(14.0, angle)
        children.append(make_tower_lower(tower, spec=spec))
        children.append(make_tower_upper_yoke(tower, spec=spec).moved(Location((dx, dy, 30.0))))
        for index, part in enumerate(make_spacers(tower, spec=spec)):
            children.append(part.moved(Location((dx, dy, 12.0 + 5.0 * index))))
        for index, part in enumerate(make_shims(tower, spec=spec)):
            children.append(part.moved(Location((dx, dy, 22.0 + 5.0 * index))))
        for role in range(3):
            lift = Location((dx, dy, 36.0 + 7.0 * role))
            children.append(make_roller_bearing(role, tower, spec=spec).moved(lift))
            children.append(make_roller_spool(role, tower, spec=spec).moved(lift))
        children.extend(part.moved(Location((dx, dy, 58.0))) for part in make_hardware(tower, spec=spec))
    return Compound(children=children, label="p3_v3_mr84_stationary_service_module")


def make_role_service_module(role_index, spec=P3_V3_MR84_SPOOL_TOWER):
    z_lift = 15.0 + 13.0 * role_index
    radial = 8.0 * role_index
    children = [part.moved(Location((radial, 0.0, z_lift))) for part in accepted_ring_quadrants(role_index, spec)]
    children.extend(part.moved(Location((radial, 0.0, z_lift))) for part in make_seam_hardware(role_index, spec))
    children.extend(part.moved(Location((0.0, 0.0, -12.0 - 8.0 * role_index))) for part in accepted_motor_station_parts(role_index, spec))
    children.append(accepted_station_support(role_index, spec))
    return Compound(children=children, label=f"p3_v3_mr84_{spec.roles[role_index]}_service_module")


def make_service_exploded(spec=P3_V3_MR84_SPOOL_TOWER):
    children = list(make_stationary_service_module(spec).children)
    for role in range(3):
        children.extend(make_role_service_module(role, spec).children)
    return Compound(children=children, label="p3_v3_mr84_COMPLETE_service_exploded")


PRIMARY_FACTORIES = (("assembled", make_assembled), ("service", make_service_exploded))
