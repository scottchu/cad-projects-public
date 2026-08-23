"""STEP-first geometry for the isolated KAGE direct gear-race V3 trial."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

import py_gearworks as pgw
from build123d import Align, Axis, Box, Compound, Cylinder, Location, RegularPolygon, extrude
from p3_v3_locked_parametric_repair_r1_color import srgb

from p3_v3_full_ring_r2_geometry import (
    _annulus,
    _polar,
    make_fin,
    make_frame_segments,
    make_outer_front_ring_posts,
    make_outer_front_ring_segments,
    make_output_pinion,
    make_seam_hardware,
)
from p3_v3_simplified_drive_guidance_geometry import (
    _radial_slot_tool,
    make_chassis_segments as _make_chassis_segments,
    make_motor_station_parts as _make_motor_station_parts,
    make_unibody_drive_yoke as _make_unibody_drive_yoke,
    make_roller_tower_yoke as _make_roller_tower_yoke,
)
from p3_v3_roller_tower_geometry import (
    make_tower_hardware_references as _make_tower_hardware_references,
    make_tower_spacers as _make_tower_spacers,
    make_tower_thrust_washers as _make_tower_thrust_washers,
)
from p3_v3_direct_gear_race_guidance_spec import (
    P3V3DirectGearRaceGuidanceSpec,
    P3_V3_DIRECT_GEAR_RACE,
)


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids()) if shape else 0.0


def _station_shift(role_index: int, adjustment: float, spec=P3_V3_DIRECT_GEAR_RACE):
    """Rigid local-radial translation expressed in the world XY frame."""

    angle = radians(spec.motor_station_angles[role_index])
    return adjustment * cos(angle), adjustment * sin(angle)


def _move_station_part(part, role_index: int, adjustment: float, spec=P3_V3_DIRECT_GEAR_RACE):
    dx, dy = _station_shift(role_index, adjustment, spec)
    return part.moved(Location((dx, dy, 0.0)))


@lru_cache(maxsize=3)
def _bare_full_role_ring(role_index: int):
    """The accepted teeth and carrier body, with every rear guide removed."""

    spec = P3_V3_DIRECT_GEAR_RACE
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
    ring = teeth.fuse(body)
    for angle in (
        spec.joint_hole_edge_angle_degrees,
        spec.quadrant_angle_degrees - spec.joint_hole_edge_angle_degrees,
    ):
        x, y = _polar(spec.joint_hole_radius, angle)
        ring = ring.cut(Cylinder(
            spec.joint_hole_diameter / 2.0,
            layer_z1 - layer_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, layer_z0 - 0.2))))
    for angle in (0.0, 90.0, 180.0, 270.0):
        x, y = _polar(spec.registration_dowel_radius, angle)
        ring = ring.cut(Cylinder(
            spec.registration_dowel_diameter / 2.0,
            layer_z1 - layer_z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, layer_z0 - 0.2))))
    return ring


@lru_cache(maxsize=3)
def _bare_canonical_quadrant(role_index: int):
    spec = P3_V3_DIRECT_GEAR_RACE
    z0, z1 = spec.carrier_layers[role_index]
    size = spec.ring_outer_radius + 1.0
    crop = Box(
        size,
        size,
        z1 - z0 + 0.8,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((0.0, 0.0, z0 - 0.4)))
    pieces = _bare_full_role_ring(role_index).intersect(crop)
    if not pieces:
        raise ValueError("bare 260T ring quadrant crop produced no solid")
    return max(pieces, key=lambda shape: shape.volume)


def make_ring_quadrant(role_index: int, quadrant_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    """Bare accepted carrier quadrant: no added bead or guide solid."""

    if not 0 <= role_index < 3 or not 0 <= quadrant_index < 4:
        raise ValueError("role/quadrant outside accepted V3 ranges")
    quadrant = deepcopy(_bare_canonical_quadrant(role_index)).rotate(
        Axis.Z, quadrant_index * spec.quadrant_angle_degrees
    )
    fin_quadrant = int(spec.display_fin_angles[role_index] // spec.quadrant_angle_degrees)
    if quadrant_index == fin_quadrant:
        quadrant = quadrant.fuse(make_fin(role_index, spec))
    quadrant.label = (
        f"p3_v3_direct_race_{spec.roles[role_index]}_M1_260T_"
        f"quadrant_Q{quadrant_index + 1}_65T_BARE_carrier_race"
    )
    quadrant.color = srgb(spec.role_colors[role_index])
    return quadrant


def make_ring_quadrants(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    return tuple(make_ring_quadrant(role_index, q, spec) for q in range(4))


def make_full_role_ring_reference(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    ring = deepcopy(_bare_full_role_ring(role_index))
    ring.label = f"p3_v3_direct_race_{spec.roles[role_index]}_bare_full_260T_validation_ring"
    ring.color = srgb(spec.role_colors[role_index])
    return ring


def make_fin_360_sweep(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    r0, r1 = spec.fin_blade_radial_ranges[role_index]
    z0, z1 = spec.fin_blade_start_zs[role_index], spec.fin_tip_zs[role_index]
    sweep = _annulus(r0, r1, z1 - z0, z0)
    root_r = spec.fin_root_radial_ranges[role_index]
    root_z = spec.fin_root_z_ranges[role_index]
    if root_r is not None and root_z is not None:
        sweep = sweep.fuse(_annulus(root_r[0], root_r[1], root_z[1] - root_z[0], root_z[0]))
    sweep.label = f"p3_v3_direct_race_{spec.roles[role_index]}_fin_360_sweep"
    return sweep


def make_tooth_envelope(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    z0, z1 = spec.pinion_face_ranges[role_index]
    envelope = _annulus(spec.tooth_tip_radius, spec.tooth_root_radius, z1 - z0, z0)
    envelope.label = f"p3_v3_direct_race_{spec.roles[role_index]}_exact_tooth_radial_Z_envelope"
    return envelope


def make_carrier_race_band(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    z0, z1 = spec.race_range(role_index)
    # A thin validation-only shell occupying the actual smooth carrier wall.
    race = _annulus(spec.carrier_race_radius, spec.carrier_race_radius + 0.05, z1 - z0, z0)
    race.label = f"p3_v3_direct_race_{spec.roles[role_index]}_R131p60_lower_root_land_REFERENCE"
    return race


def make_roller(
    role_index: int,
    tower_index: int,
    axis_radius=None,
    spec=P3_V3_DIRECT_GEAR_RACE,
):
    """Relieved spool whose broad land touches only the carrier lower race."""

    axis = spec.roller_axis_radius if axis_radius is None else axis_radius
    carrier_z0, carrier_z1 = spec.carrier_layers[role_index]
    z0, z1 = spec.roller_range(role_index)
    running_z0, running_z1 = spec.roller_running_range(role_index)
    roller = Cylinder(
        spec.roller_hub_outer_diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z0)))
    roller = roller.fuse(Cylinder(
        spec.roller_running_outer_diameter / 2.0,
        running_z1 - running_z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, running_z0))))
    for flange_z0, flange_z1 in spec.roller_flange_ranges(role_index):
        roller = roller.fuse(Cylinder(
            spec.roller_flange_outer_diameter / 2.0,
            flange_z1 - flange_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((axis, 0.0, flange_z0))))
    roller = roller.cut(Cylinder(
        spec.roller_bore_diameter / 2.0,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((axis, 0.0, z0 - 0.2))))
    roller = roller.rotate(Axis.Z, spec.roller_tower_angles[tower_index])
    roller.label = (
        f"p3_v3_direct_race_tower_{tower_index + 1}_{spec.roles[role_index]}_"
        "RELIEVED_spool_carrier_root_land_only"
    )
    roller.color = srgb(spec.role_colors[role_index])
    return roller


def make_tower_spacers(tower_index: int, axis_radius=None, spec=P3_V3_DIRECT_GEAR_RACE):
    parts = list(_make_tower_spacers(tower_index, axis_radius, spec))
    for index, part in enumerate(parts):
        part.label = f"p3_v3_direct_race_tower_{tower_index + 1}_D6x1p25_spacer_{index + 1}"
    return tuple(parts)


def make_tower_thrust_washers(tower_index: int, axis_radius=None, spec=P3_V3_DIRECT_GEAR_RACE):
    parts = list(_make_tower_thrust_washers(tower_index, axis_radius, spec))
    for index, part in enumerate(parts):
        part.label = f"p3_v3_direct_race_tower_{tower_index + 1}_{('lower','upper')[index]}_0p20_thrust_washer"
    return tuple(parts)


def make_tower_hardware_references(tower_index: int, axis_radius=None, spec=P3_V3_DIRECT_GEAR_RACE):
    parts = list(_make_tower_hardware_references(tower_index, axis_radius, spec))
    for part in parts:
        part.label = part.label.replace("p3_v3_roller", "p3_v3_direct_race")
        part.label = part.label.replace("4x20_smooth_pin", "D4x25_polished_axle")
    return tuple(parts)


def make_roller_tower_yoke(tower_index: int, axis_radius=None, spec=P3_V3_DIRECT_GEAR_RACE):
    yoke = _make_roller_tower_yoke(tower_index, axis_radius, spec)
    yoke.label = yoke.label.replace("p3_v3_simplified", "p3_v3_direct_race")
    return yoke


def make_roller_tower_module(tower_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    children = [make_roller_tower_yoke(tower_index, spec=spec)]
    children.extend(make_tower_spacers(tower_index, spec=spec))
    children.extend(make_tower_thrust_washers(tower_index, spec=spec))
    children.extend(make_roller(role, tower_index, spec=spec) for role in range(3))
    children.extend(make_tower_hardware_references(tower_index, spec=spec))
    return Compound(children=children, label=f"p3_v3_direct_race_inner_tower_{tower_index + 1}_module")


def make_unibody_drive_yoke(
    role_index: int,
    spec=P3_V3_DIRECT_GEAR_RACE,
    radial_adjustment: float = 0.0,
):
    # The inherited yoke is returned in its final station rotation.  Bring it
    # back to the local radial frame, trim only the upper-bearing-bridge band,
    # then restore the final rotation.  The cylindrical trim is rotation
    # invariant, but keeping the source order explicit protects the frozen
    # station datums and makes the service intent auditable.
    spec.validate_motor_radial_adjustment(radial_adjustment)
    station_angle = spec.motor_station_angles[role_index]
    yoke = _make_unibody_drive_yoke(role_index, spec).rotate(Axis.Z, -station_angle)
    z0, z1 = spec.upper_bearing_z(role_index)
    extent = spec.ring_outer_radius + 20.0
    band = Box(
        2.0 * extent,
        2.0 * extent,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z0)))
    protected = Cylinder(
        spec.yoke_upper_bridge_radial_limit,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z0)))
    yoke = yoke.cut(band.cut(protected))

    # Four M3 clamp slots exist in the moving yoke only.  The inherited round
    # openings are contained inside these wider radial capsules; the chassis
    # retains fixed D3.40 round holes at the same nominal axes.
    foot_z0 = spec.chassis_z[1]
    foot_z1 = foot_z0 + spec.unibody_foot_thickness
    for x in spec.unibody_chassis_mount_x:
        for y in spec.unibody_chassis_mount_y:
            yoke = yoke.cut(_radial_slot_tool(
                x,
                y,
                spec.motor_mount_slot_center_travel,
                spec.motor_mount_slot_width,
                foot_z0 - 0.20,
                spec.unibody_foot_thickness + 0.40,
            ))

            # The outboard clamp axes otherwise pass through the side columns.
            # These D10 vertical access chimneys begin at the yoke top, leaving
            # the full D7 washer land intact while providing a 12 mm handoff
            # path for the driver/hex key once the moving rings are removed.
            yoke = yoke.cut(Cylinder(
                spec.motor_mount_top_tool_diameter / 2.0,
                spec.motor_mount_top_tool_height,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, foot_z1))))

    # A printable powered-window band and two explicit SERVICE endpoint ticks
    # live outside the D7 washer sweep on the outer +Y rail.  These are shallow
    # recessed witness marks only: no detent or kinematic function is added.
    # The outer rail is y=[7.50,16.50].  Keep the witness strip wholly inside
    # it at y=[15.70,16.30], outside the D7 washer sweep ending at y=15.50.
    mark_y = spec.unibody_chassis_mount_y[1] + 4.00
    mark_z0 = foot_z1 - spec.motor_witness_mark_depth
    band = Box(
        spec.motor_witness_powered_band_radial_width,
        spec.motor_witness_mark_tangential_width,
        spec.motor_witness_mark_depth + 0.05,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((
        spec.unibody_chassis_mount_x[1] + spec.motor_witness_powered_band_center_offset,
        mark_y,
        mark_z0,
    )))
    yoke = yoke.cut(band)
    for service_x in (
        spec.unibody_chassis_mount_x[1] - spec.motor_mount_service_adjustment,
        spec.unibody_chassis_mount_x[1] + spec.motor_mount_service_adjustment,
    ):
        tick = Box(
            spec.motor_witness_service_tick_radial_width,
            spec.motor_witness_mark_tangential_width,
            spec.motor_witness_mark_depth + 0.05,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((service_x, mark_y, mark_z0)))
        yoke = yoke.cut(tick)

    yoke = yoke.rotate(Axis.Z, station_angle)
    yoke = _move_station_part(yoke, role_index, radial_adjustment, spec)
    yoke.label = yoke.label.replace("p3_v3_simplified", "p3_v3_direct_race")
    yoke.label += f"_RADIAL_SLOT_q{radial_adjustment:+0.2f}_SERVICE_plus_minus_2p50"
    return yoke


def make_motor_station_parts(
    role_index: int,
    spec=P3_V3_DIRECT_GEAR_RACE,
    radial_adjustment: float = 0.0,
):
    spec.validate_motor_radial_adjustment(radial_adjustment)
    parts = list(_make_motor_station_parts(role_index, spec))
    for index, part in enumerate(parts[:-1]):
        part.label = part.label.replace("p3_v3_simplified", "p3_v3_direct_race")
        part = _move_station_part(part, role_index, radial_adjustment, spec)
        part.label += f"_RIGID_q{radial_adjustment:+0.2f}"
        parts[index] = part
    parts[-1] = make_unibody_drive_yoke(role_index, spec, radial_adjustment)
    return tuple(parts)


def make_motor_clamp_hardware(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    """Four fixed-axis M3 clamp stacks for one adjustable station."""

    foot_top = spec.chassis_z[1] + spec.unibody_foot_thickness
    washer_z0 = foot_top
    head_z0 = washer_z0 + spec.motor_mount_washer_thickness
    nut_z0 = spec.chassis_z[0] - spec.motor_mount_nut_thickness
    shaft_z0 = head_z0 - spec.motor_mount_screw_length
    children = []
    angle = spec.motor_station_angles[role_index]
    for radial_name, x in zip(("inner", "outer"), spec.unibody_chassis_mount_x):
        for tangent_name, y in zip(("negative_tangent", "positive_tangent"), spec.unibody_chassis_mount_y):
            washer = Cylinder(
                spec.motor_mount_washer_outer_diameter / 2.0,
                spec.motor_mount_washer_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, washer_z0))).cut(Cylinder(
                spec.motor_mount_washer_inner_diameter / 2.0,
                spec.motor_mount_washer_thickness + 0.20,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, washer_z0 - 0.10))))
            screw = Cylinder(
                spec.motor_mount_screw_nominal_diameter / 2.0,
                head_z0 - shaft_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, shaft_z0))).fuse(Cylinder(
                spec.motor_mount_screw_head_diameter / 2.0,
                spec.motor_mount_screw_head_height,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, head_z0))))
            nut = extrude(
                RegularPolygon(
                    spec.motor_mount_nut_across_flats / 2.0,
                    6,
                    major_radius=False,
                ),
                amount=spec.motor_mount_nut_thickness,
            ).moved(Location((x, y, nut_z0)))
            items = (("M3x10_screw", screw), ("D7x0p50_washer", washer), ("M3_AF5p50_nut", nut))
            for item_name, item in items:
                item = item.rotate(Axis.Z, angle)
                item.label = (
                    f"p3_v3_direct_race_{spec.roles[role_index]}_clamp_"
                    f"{radial_name}_{tangent_name}_{item_name}_REFERENCE"
                )
                item.color = srgb("#B8B8B2")
                children.append(item)
    return tuple(children)


def make_motor_clamp_tool_paths(role_index: int, spec=P3_V3_DIRECT_GEAR_RACE):
    """Validation-only top and underside access cylinders at fixed axes."""

    foot_top = spec.chassis_z[1] + spec.unibody_foot_thickness
    angle = spec.motor_station_angles[role_index]
    paths = []
    for radial_name, x in zip(("inner", "outer"), spec.unibody_chassis_mount_x):
        for tangent_name, y in zip(("negative_tangent", "positive_tangent"), spec.unibody_chassis_mount_y):
            top = Cylinder(
                spec.motor_mount_top_tool_diameter / 2.0,
                spec.motor_mount_top_tool_height,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, foot_top + spec.motor_mount_washer_thickness + spec.motor_mount_screw_head_height)))
            bottom = Cylinder(
                spec.motor_mount_bottom_tool_diameter / 2.0,
                spec.motor_mount_bottom_tool_height,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, spec.chassis_z[0] - spec.motor_mount_bottom_tool_height)))
            for side, path in (("top_D10", top), ("underside_D8", bottom)):
                path = path.rotate(Axis.Z, angle)
                path.label = (
                    f"p3_v3_direct_race_{spec.roles[role_index]}_clamp_"
                    f"{radial_name}_{tangent_name}_{side}_TOOL_PATH"
                )
                paths.append(path)
    return tuple(paths)


def make_chassis_segments(spec=P3_V3_DIRECT_GEAR_RACE):
    parts = list(_make_chassis_segments(spec))
    for part in parts:
        part.label = part.label.replace("p3_v3_simplified", "p3_v3_direct_race")
    return tuple(parts)


def make_stationary_module(
    spec=P3_V3_DIRECT_GEAR_RACE,
    radial_adjustments: tuple[float, float, float] = (0.0, 0.0, 0.0),
):
    children = [*make_chassis_segments(spec), *make_frame_segments(spec)]
    children.extend(make_outer_front_ring_posts(spec))
    children.extend(make_outer_front_ring_segments(spec))
    for tower in range(3):
        children.extend(make_roller_tower_module(tower, spec).children)
    children.extend(make_unibody_drive_yoke(role, spec, radial_adjustments[role]) for role in range(3))
    for role in range(3):
        children.extend(make_motor_clamp_hardware(role, spec))
    return Compound(children=children, label="p3_v3_direct_race_stationary_structure")


def make_role_module(
    role_index: int,
    spec=P3_V3_DIRECT_GEAR_RACE,
    radial_adjustment: float = 0.0,
):
    children = [*make_ring_quadrants(role_index, spec)]
    children.extend(make_seam_hardware(role_index, spec))
    children.extend(make_motor_station_parts(role_index, spec, radial_adjustment)[:-1])
    return Compound(children=children, label=f"p3_v3_direct_race_{spec.roles[role_index]}_moving_drive_module")


def make_assembled(
    spec=P3_V3_DIRECT_GEAR_RACE,
    radial_adjustments: tuple[float, float, float] = (0.0, 0.0, 0.0),
    *,
    include_rings: bool = True,
):
    if len(radial_adjustments) != 3:
        raise ValueError("three motor radial adjustments are required")
    for value in radial_adjustments:
        spec.validate_motor_radial_adjustment(value)
    children = list(make_stationary_module(spec, radial_adjustments).children)
    for role in range(3):
        if include_rings:
            children.extend(make_ring_quadrants(role, spec))
            children.extend(make_seam_hardware(role, spec))
        children.extend(make_motor_station_parts(role, spec, radial_adjustments[role])[:-1])
    mode = "rings_installed" if include_rings else "ALL_RINGS_REMOVED_SERVICE_ONLY"
    return Compound(children=children, label=f"p3_v3_direct_race_COMPLETE_{mode}_radially_adjustable")


def make_powered_min(spec=P3_V3_DIRECT_GEAR_RACE):
    q = spec.motor_mount_powered_min_adjustment
    spec.validate_motor_radial_adjustment(q, powered=True)
    return make_assembled(spec, (q, q, q))


def make_powered_max(spec=P3_V3_DIRECT_GEAR_RACE):
    q = spec.motor_mount_powered_max_adjustment
    spec.validate_motor_radial_adjustment(q, powered=True)
    return make_assembled(spec, (q, q, q))


def make_service_disengaged(spec=P3_V3_DIRECT_GEAR_RACE):
    q = -spec.motor_mount_service_adjustment
    return make_assembled(spec, (q, q, q))


def make_service_outward_rings_removed(spec=P3_V3_DIRECT_GEAR_RACE):
    q = spec.motor_mount_service_adjustment
    return make_assembled(spec, (q, q, q), include_rings=False)


def make_service_exploded(spec=P3_V3_DIRECT_GEAR_RACE):
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
        for index, part in enumerate(make_motor_clamp_hardware(role, spec)):
            children.append(part.moved(Location((dx, dy, 18.0 + 2.0 * (index % 3)))))
    return Compound(children=children, label="p3_v3_direct_race_COMPLETE_service_exploded")


PRIMARY_FACTORIES = (
    ("assembled", make_assembled),
    ("service_exploded", make_service_exploded),
    ("powered_min", make_powered_min),
    ("powered_max", make_powered_max),
    ("service_disengaged", make_service_disengaged),
    ("service_outward_rings_removed", make_service_outward_rings_removed),
)
