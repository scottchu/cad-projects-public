"""STEP-first geometry for the passive three-station KAGE roller MVP."""

from __future__ import annotations

from copy import deepcopy
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, RegularPolygon, Solid, extrude
from cadgen import srgb

from p3_v3_direct_gear_race_guidance_geometry import (
    make_fin_360_sweep,
    make_full_role_ring_reference,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import (
    local_point,
    named_sector,
)
from p3_v3_mvp_free_roller_r0_three_station_spec import NAMESPACE, SPEC


def _single(shape, label: str):
    solids = list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    result.label = label
    return result


def volume_mm3(shape) -> float:
    return float(sum(s.volume for s in shape.solids())) if shape is not None else 0.0


def intersection_volume_mm3(left, right) -> float:
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def _radial_slot(radius_mm: float, tangent_mm: float, z0_mm: float, height_mm: float):
    center_travel = SPEC.mount_slot_center_travel_mm
    diameter = SPEC.mount_slot_width_mm
    left = Cylinder(diameter / 2, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius_mm - center_travel / 2, tangent_mm, z0_mm))
    )
    right = Cylinder(diameter / 2, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius_mm + center_travel / 2, tangent_mm, z0_mm))
    )
    middle = Box(center_travel, diameter, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius_mm, tangent_mm, z0_mm))
    )
    return left.fuse(middle).fuse(right)


def _hex_prism_at(angle_deg: float, radius_mm: float, tangent_mm: float, z0_mm: float, height_mm: float):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    return extrude(
        RegularPolygon(SPEC.nut_across_flats_mm / 2, 6, major_radius=False),
        amount=height_mm,
    ).moved(Location((x, y, z0_mm)))


def make_derivative_sector_print():
    """One canonical accepted Q3 sector plus only two blind outer nut pockets."""

    sector = named_sector(1)
    # Sector 1 owns the upper leaf at the +60 degree seam.  Its identical
    # 120-degree copies therefore provide the pocket pair at all three seams.
    pocket_z0 = SPEC.base_plate_z_mm[1] - SPEC.nut_front_skin_mm - SPEC.nut_pocket_depth_mm
    pockets = tuple(
        _hex_prism_at(60.0, SPEC.outer_mount_radius_mm, tangent, pocket_z0, SPEC.nut_pocket_depth_mm)
        for tangent in SPEC.outer_mount_tangent_mm
    )
    sector = _single(sector.cut(*pockets), f"{NAMESPACE}_identical_Q3_sector_outer_nut_pockets_only")
    sector.color = srgb("#E97A35")
    return sector


def make_spool_print():
    hub = Cylinder(
        SPEC.spool_hub_od_mm / 2,
        SPEC.spool_complete_height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    running = Cylinder(
        SPEC.spool_running_od_mm / 2,
        SPEC.spool_running_z_mm[1] - SPEC.spool_running_z_mm[0],
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, SPEC.spool_running_z_mm[0])))
    lower = Cylinder(
        SPEC.spool_flange_od_mm / 2,
        SPEC.spool_flange_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    upper = Cylinder(
        SPEC.spool_flange_od_mm / 2,
        SPEC.spool_flange_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, SPEC.spool_upper_flange_z_mm[0])))
    bore = Cylinder(
        SPEC.spool_bore_diameter_mm / 2,
        SPEC.spool_complete_height_mm + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, -0.2)))
    spool = _single(hub.fuse(running, lower, upper).cut(bore), f"{NAMESPACE}_canonical_flanged_spool_PRINT_QTY9")
    spool.color = srgb("#F08A24")
    return spool


def make_spacer_print():
    spacer = Cylinder(
        SPEC.spacer_od_mm / 2,
        SPEC.spacer_length_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).cut(
        Cylinder(
            SPEC.spacer_bore_mm / 2,
            SPEC.spacer_length_mm + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((0, 0, -0.2)))
    )
    spacer = _single(spacer, f"{NAMESPACE}_canonical_D6_D4p2_x0p8_spacer_PRINT_QTY6")
    spacer.color = srgb("#E3C567")
    return spacer


def make_upper_bridge_print():
    r0, r1 = SPEC.bridge_r_mm
    t0, t1 = SPEC.bridge_t_mm
    z0, z1 = SPEC.bridge_z_mm
    bridge = Box(r1 - r0, t1 - t0, z1 - z0, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((r0, t0, 0.0))
    )
    axle = Cylinder(
        SPEC.axle_clearance_diameter_mm / 2,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.roller_axis_radius_mm, 0, -0.2)))
    screw_tools = tuple(
        Cylinder(
            SPEC.bridge_clearance_diameter_mm / 2,
            z1 - z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.bridge_screw_radius_mm, t, -0.2)))
        for t in SPEC.bridge_screw_tangent_mm
    )
    bridge = _single(bridge.cut(axle, *screw_tools), f"{NAMESPACE}_canonical_removable_upper_bridge_PRINT_QTY3")
    bridge.color = srgb("#4F6D7A")
    return bridge


def make_station_frame_print():
    fz0, fz1 = SPEC.station_foot_z_mm
    fr0, fr1 = SPEC.station_foot_r_mm
    ft0, ft1 = SPEC.station_foot_t_mm
    foot = Box(fr1 - fr0, ft1 - ft0, fz1 - fz0, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((fr0, ft0, 0.0))
    )
    slots = tuple(_radial_slot(SPEC.outer_mount_radius_mm, t, -0.2, fz1 - fz0 + 0.4) for t in SPEC.outer_mount_tangent_mm)
    foot = foot.cut(*slots)

    # Lower axle locator/post.  D6 leaves 0.50 mm to the locked R129 tooth tip
    # during complete-ring axial insertion.
    post = Cylinder(
        SPEC.lower_post_od_mm / 2,
        SPEC.lower_post_top_z_mm - fz1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.roller_axis_radius_mm, 0, fz1 - fz0)))
    socket = Cylinder(
        SPEC.axle_clearance_diameter_mm / 2,
        SPEC.lower_socket_depth_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.roller_axis_radius_mm, 0, SPEC.axle_z_mm[0] - fz0)))

    bridge_z0_local = SPEC.bridge_z_mm[0] - fz0
    backbones = []
    for tangent in SPEC.backbone_tangent_mm:
        backbone = Box(
            SPEC.backbone_section_mm,
            SPEC.backbone_section_mm,
            bridge_z0_local - (fz1 - fz0),
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.backbone_radius_mm, tangent, fz1 - fz0)))
        # A short inboard neck connects the legacy backbone datum to the
        # contract foot without enlarging the foot itself.
        neck = Box(
            fr0 + 0.2 - (SPEC.backbone_radius_mm - SPEC.backbone_section_mm / 2),
            SPEC.backbone_section_mm,
            SPEC.backbone_section_mm,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.backbone_radius_mm - SPEC.backbone_section_mm / 2, tangent, fz1 - fz0)))
        backbones.extend((backbone, neck))

    # Local top bosses carry the replaceable prototype nuts.  They overlap
    # the inboard backbones but keep the screw axes safely inside the bridge
    # outline, avoiding edge-open bores in the thin removable bridge.
    boss_parts = tuple(
        Box(7.0, 7.0, SPEC.bridge_nut_thickness_mm + 0.6, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(
            Location((SPEC.bridge_screw_radius_mm, t, bridge_z0_local))
        )
        for t in SPEC.bridge_screw_tangent_mm
    )

    frame = foot.fuse(post, *backbones, *boss_parts).cut(socket)
    # Blind hex pockets immediately below the removable bridge; a loose,
    # replaceable prototype nut is loaded from the open top before the bridge.
    nut_z0 = bridge_z0_local - SPEC.bridge_nut_thickness_mm
    nut_tools = tuple(
        extrude(
            RegularPolygon(SPEC.bridge_nut_af_mm / 2, 6, major_radius=False),
            amount=SPEC.bridge_nut_thickness_mm,
        ).moved(Location((SPEC.bridge_screw_radius_mm, t, nut_z0)))
        for t in SPEC.bridge_screw_tangent_mm
    )
    pilot_tools = tuple(
        Cylinder(
            SPEC.bridge_screw_diameter_mm / 2,
            SPEC.bridge_screw_length_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.bridge_screw_radius_mm, t, nut_z0 - 0.2)))
        for t in SPEC.bridge_screw_tangent_mm
    )
    frame = _single(frame.cut(*nut_tools, *pilot_tools), f"{NAMESPACE}_canonical_open_station_frame_PRINT_QTY3")
    frame.color = srgb("#34495E")
    return frame


def _at_station(shape, angle_deg: float, z_shift: float = 0.0):
    return deepcopy(shape).moved(Location((0, 0, z_shift))).rotate(Axis.Z, angle_deg)


def make_assembled_spool(role_index: int, station_angle_deg: float):
    z0, _ = SPEC.spool_ranges_z_mm[role_index]
    spool = make_spool_print().moved(Location((SPEC.roller_axis_radius_mm, 0, z0))).rotate(Axis.Z, station_angle_deg)
    spool.label = f"{NAMESPACE}_{('hour','minute','second')[role_index]}_spool_station_{station_angle_deg:g}deg"
    return spool


def _ring_reference(role_index: int):
    ring = make_full_role_ring_reference(role_index)
    ring.label = f"{NAMESPACE}_LOCKED_{('hour','minute','second')[role_index]}_ring_REFERENCE_UNCHANGED"
    return ring


def make_station_assembly(angle_deg: float, include_hardware: bool = True):
    fz0, _ = SPEC.station_foot_z_mm
    frame = _at_station(make_station_frame_print(), angle_deg, fz0)
    bridge = _at_station(make_upper_bridge_print(), angle_deg, SPEC.bridge_z_mm[0])
    children = [frame, bridge]
    children.extend(make_assembled_spool(role, angle_deg) for role in range(3))

    for z0, z1 in SPEC.spacer_ranges_z_mm:
        spacer = make_spacer_print().moved(Location((SPEC.roller_axis_radius_mm, 0, z0))).rotate(Axis.Z, angle_deg)
        spacer.label = f"{NAMESPACE}_spacer_station_{angle_deg:g}_{z0:g}"
        children.append(spacer)
    if include_hardware:
        # Reference-only axle, washers, collar, screws and nuts.
        axle = Cylinder(
            SPEC.axle_finished_diameter_mm / 2,
            SPEC.axle_z_mm[1] - SPEC.axle_z_mm[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.roller_axis_radius_mm, 0, SPEC.axle_z_mm[0]))).rotate(Axis.Z, angle_deg)
        axle.label = f"{NAMESPACE}_D4x25_polished_axle_REFERENCE_station_{angle_deg:g}"
        axle.color = srgb("#B7B9B5")
        children.append(axle)
        for i, (z0, z1) in enumerate(SPEC.washer_ranges_z_mm, 1):
            washer = Cylinder(SPEC.washer_od_mm / 2, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
                Cylinder(SPEC.washer_bore_mm / 2, z1 - z0 + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, -0.1)))
            ).moved(Location((SPEC.roller_axis_radius_mm, 0, z0))).rotate(Axis.Z, angle_deg)
            washer.label = f"{NAMESPACE}_thrust_washer_{i}_station_{angle_deg:g}_REFERENCE"
            children.append(washer)
        collar = Cylinder(
            SPEC.collar_od_mm / 2,
            SPEC.collar_z_mm[1] - SPEC.collar_z_mm[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).cut(Cylinder(
            SPEC.collar_bore_mm / 2,
            SPEC.collar_z_mm[1] - SPEC.collar_z_mm[0] + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((0, 0, -0.1)))).moved(
            Location((SPEC.roller_axis_radius_mm, 0, SPEC.collar_z_mm[0]))
        ).rotate(Axis.Z, angle_deg)
        collar.label = f"{NAMESPACE}_D4_split_collar_REFERENCE_station_{angle_deg:g}"
        collar.color = srgb("#B7B9B5")
        children.append(collar)

        # Purchased station and bridge hardware are reference solids only.
        # Their envelopes make top-side access and the no-fin corridor visible
        # without turning any of this hardware into a printable deliverable.
        for tangent in SPEC.outer_mount_tangent_mm:
            x, y = local_point(angle_deg, SPEC.outer_mount_radius_mm, tangent)
            screw = Cylinder(
                SPEC.station_screw_diameter_mm / 2,
                SPEC.station_screw_length_mm,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((x, y, SPEC.station_foot_z_mm[1])))
            screw.label = f"{NAMESPACE}_M3x8_station_screw_REFERENCE_{angle_deg:g}_{tangent:g}"
            children.append(screw)
            washer = Cylinder(
                SPEC.station_washer_od_mm / 2,
                SPEC.station_washer_thickness_mm,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).cut(Cylinder(
                1.7,
                SPEC.station_washer_thickness_mm + 0.2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((0, 0, -0.1)))).moved(Location((x, y, SPEC.station_foot_z_mm[1])))
            washer.label = f"{NAMESPACE}_D7_station_washer_REFERENCE_{angle_deg:g}_{tangent:g}"
            children.append(washer)
        for tangent in SPEC.bridge_screw_tangent_mm:
            x, y = local_point(angle_deg, SPEC.bridge_screw_radius_mm, tangent)
            bridge_screw = Cylinder(
                SPEC.bridge_screw_diameter_mm / 2,
                SPEC.bridge_screw_length_mm,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((x, y, SPEC.bridge_z_mm[1])))
            bridge_screw.label = f"{NAMESPACE}_M3x6_bridge_screw_REFERENCE_{angle_deg:g}_{tangent:g}"
            children.append(bridge_screw)
    return Compound(children=children, label=f"{NAMESPACE}_station_{angle_deg:g}deg")


def make_three_station_context():
    children = [make_derivative_sector_print().rotate(Axis.Z, angle) for angle in (0.0, 120.0, 240.0)]
    for index, sector in enumerate(children, 1):
        sector.label = f"{NAMESPACE}_derivative_Q3_sector_instance_{index}_REFERENCE"
    children.extend(_ring_reference(i) for i in range(3))
    for angle in SPEC.station_angles_deg:
        children.extend(make_station_assembly(angle).children)
    return Compound(children=children, label=f"{NAMESPACE}_THREE_STATIONS_NINE_SPOOLS_LOCKED_RING_CONTEXT")


def make_service_exploded():
    children = [_ring_reference(i) for i in range(3)]
    for station_index, angle in enumerate(SPEC.station_angles_deg):
        radial_lift = 18.0 + station_index * 4.0
        dx = -radial_lift * cos(radians(angle))
        dy = -radial_lift * sin(radians(angle))
        module = make_station_assembly(angle)
        for index, part in enumerate(module.children):
            children.append(part.moved(Location((dx, dy, 8.0 + index * 1.5))))
    return Compound(children=children, label=f"{NAMESPACE}_SERVICE_EXPLODED")


def make_print_station_kit():
    frame = make_station_frame_print()
    bridge = make_upper_bridge_print().moved(Location((35, 0, 0)))
    children = [frame, bridge]
    for i in range(3):
        children.append(make_spool_print().moved(Location((45 + 15 * i, 0, 0))))
    for i in range(2):
        children.append(make_spacer_print().moved(Location((45 + 15 * i, 15, 0))))
    return Compound(children=children, label=f"{NAMESPACE}_ONE_STATION_PRINT_KIT_PRINT_QTY3")


def make_derivative_sector_bed_print():
    """Accepted 45-degree bed orientation, baked with the rear face at Z=0."""

    shape = make_derivative_sector_print().rotate(Axis.Z, 45.0).moved(
        Location((0.0, 0.0, -SPEC.base_plate_z_mm[0]))
    )
    shape = _single(shape, f"{NAMESPACE}_identical_Q3_sector_DIAGONAL_PRINT_QTY3")
    shape.color = srgb("#E97A35")
    return shape


def make_fin_sweeps_reference():
    return Compound(children=[make_fin_360_sweep(i) for i in range(3)], label=f"{NAMESPACE}_LOCKED_FIN_SWEEPS_REFERENCE")
