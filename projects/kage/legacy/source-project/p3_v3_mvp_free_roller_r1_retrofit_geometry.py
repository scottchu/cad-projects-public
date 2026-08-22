"""STEP-first R1 retrofit of the accepted passive KAGE roller system."""

from __future__ import annotations

from copy import deepcopy
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Location, RegularPolygon, extrude
from cadgen import srgb

from p3_v3_direct_gear_race_guidance_geometry import make_full_role_ring_reference
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import local_point, named_sector
from p3_v3_mvp_free_roller_r0_three_station_geometry import (
    intersection_volume_mm3,
    make_fin_sweeps_reference,
    make_spacer_print as _make_spacer_r0,
    make_spool_print as _make_spool_r0,
    make_upper_bridge_print as _make_bridge_r0,
    volume_mm3,
)
from p3_v3_mvp_free_roller_r1_retrofit_spec import NAMESPACE, SPEC


def _single(shape, label: str):
    solids = list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    result.label = label
    return result


def _radial_slot(radius_mm: float, tangent_mm: float, z0_mm: float, height_mm: float):
    travel = SPEC.mount_slot_center_travel_mm
    diameter = SPEC.mount_slot_width_mm
    left = Cylinder(diameter / 2, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius_mm - travel / 2, tangent_mm, z0_mm))
    )
    right = Cylinder(diameter / 2, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius_mm + travel / 2, tangent_mm, z0_mm))
    )
    middle = Box(travel, diameter, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radius_mm, tangent_mm, z0_mm))
    )
    return left.fuse(middle).fuse(right)


def _elongated_hex_pocket(radius_mm: float, tangent_mm: float, z0_mm: float, height_mm: float):
    half = SPEC.nut_pocket_radial_elongation_mm / 2.0
    tools = []
    for offset in (-half, half):
        tools.append(
            extrude(
                RegularPolygon(SPEC.nut_across_flats_mm / 2.0, 6, major_radius=False),
                amount=height_mm,
            ).moved(Location((radius_mm + offset, tangent_mm, z0_mm)))
        )
    return tools[0].fuse(tools[1])


def make_spool_print():
    result = deepcopy(_make_spool_r0())
    result.label = f"{NAMESPACE}_canonical_flanged_spool_PRINT_QTY9"
    return result


def make_spacer_print():
    result = deepcopy(_make_spacer_r0())
    result.label = f"{NAMESPACE}_canonical_D6_D4p2_x0p8_spacer_PRINT_QTY6"
    return result


def make_upper_bridge_print():
    result = deepcopy(_make_bridge_r0())
    result.label = f"{NAMESPACE}_canonical_removable_upper_bridge_PRINT_QTY3"
    return result


def make_station_frame_print():
    """R0 frame with only the two base-fastening pockets changed for retrofit."""

    fz0, fz1 = SPEC.station_foot_z_mm
    fr0, fr1 = SPEC.station_foot_r_mm
    ft0, ft1 = SPEC.station_foot_t_mm
    local_height = fz1 - fz0
    foot = Box(fr1 - fr0, ft1 - ft0, local_height, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((fr0, ft0, 0.0))
    )
    slots = tuple(
        _radial_slot(SPEC.outer_mount_radius_mm, tangent, -0.2, local_height + 0.4)
        for tangent in SPEC.outer_mount_tangent_mm
    )

    # Open-top captures: 0.50 mm floor, 2.50 mm deep, AF5.8, with 0.60 mm
    # radial elongation to follow the existing D3.6 x 4.1 adjustment slots.
    pocket_z0 = SPEC.nut_front_skin_mm
    pockets = tuple(
        _elongated_hex_pocket(
            SPEC.outer_mount_radius_mm,
            tangent,
            pocket_z0,
            SPEC.nut_pocket_depth_mm + 0.2,
        )
        for tangent in SPEC.outer_mount_tangent_mm
    )
    foot = foot.cut(*slots, *pockets)

    post = Cylinder(
        SPEC.lower_post_od_mm / 2,
        SPEC.lower_post_top_z_mm - fz1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.roller_axis_radius_mm, 0, local_height)))
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
            bridge_z0_local - local_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.backbone_radius_mm, tangent, local_height)))
        neck = Box(
            fr0 + 0.2 - (SPEC.backbone_radius_mm - SPEC.backbone_section_mm / 2),
            SPEC.backbone_section_mm,
            SPEC.backbone_section_mm,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.backbone_radius_mm - SPEC.backbone_section_mm / 2, tangent, local_height)))
        backbones.extend((backbone, neck))

    boss_parts = tuple(
        Box(7.0, 7.0, SPEC.bridge_nut_thickness_mm + 0.6, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(
            Location((SPEC.bridge_screw_radius_mm, tangent, bridge_z0_local))
        )
        for tangent in SPEC.bridge_screw_tangent_mm
    )
    frame = foot.fuse(post, *backbones, *boss_parts).cut(socket)

    bridge_nut_z0 = bridge_z0_local - SPEC.bridge_nut_thickness_mm
    bridge_nut_tools = tuple(
        extrude(
            RegularPolygon(SPEC.bridge_nut_af_mm / 2, 6, major_radius=False),
            amount=SPEC.bridge_nut_thickness_mm,
        ).moved(Location((SPEC.bridge_screw_radius_mm, tangent, bridge_nut_z0)))
        for tangent in SPEC.bridge_screw_tangent_mm
    )
    bridge_pilots = tuple(
        Cylinder(
            SPEC.bridge_screw_diameter_mm / 2,
            SPEC.bridge_screw_length_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.bridge_screw_radius_mm, tangent, bridge_nut_z0 - 0.2)))
        for tangent in SPEC.bridge_screw_tangent_mm
    )
    frame = _single(
        frame.cut(*bridge_nut_tools, *bridge_pilots),
        f"{NAMESPACE}_open_station_frame_M3_nut_captures_PRINT_QTY3",
    )
    frame.color = srgb("#34495E")
    return frame


def _at_station(shape, angle_deg: float, z_shift: float = 0.0):
    return deepcopy(shape).moved(Location((0, 0, z_shift))).rotate(Axis.Z, angle_deg)


def make_assembled_spool(role_index: int, station_angle_deg: float):
    z0, _ = SPEC.spool_ranges_z_mm[role_index]
    spool = make_spool_print().moved(Location((SPEC.roller_axis_radius_mm, 0, z0))).rotate(Axis.Z, station_angle_deg)
    spool.label = f"{NAMESPACE}_{('hour', 'minute', 'second')[role_index]}_spool_station_{station_angle_deg:g}deg"
    return spool


def _ring_reference(role_index: int):
    ring = make_full_role_ring_reference(role_index)
    ring.label = f"{NAMESPACE}_LOCKED_{('hour', 'minute', 'second')[role_index]}_ring_REFERENCE_UNCHANGED"
    return ring


def _ordinary_m3_nut_reference(angle_deg: float, radius_mm: float, tangent_mm: float, z0_mm: float, label: str):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    nut = extrude(
        RegularPolygon(SPEC.nut_nominal_across_flats_mm / 2, 6, major_radius=False),
        amount=SPEC.nut_nominal_thickness_mm,
    ).cut(
        Cylinder(1.6, SPEC.nut_nominal_thickness_mm + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((0, 0, -0.2))
        )
    ).moved(Location((x, y, z0_mm)))
    nut.label = label
    nut.color = srgb("#B7B9B5")
    return nut


def make_station_assembly(angle_deg: float, include_hardware: bool = True):
    fz0, _ = SPEC.station_foot_z_mm
    children = [
        _at_station(make_station_frame_print(), angle_deg, fz0),
        _at_station(make_upper_bridge_print(), angle_deg, SPEC.bridge_z_mm[0]),
    ]
    children.extend(make_assembled_spool(role, angle_deg) for role in range(3))
    for z0, _ in SPEC.spacer_ranges_z_mm:
        spacer = make_spacer_print().moved(Location((SPEC.roller_axis_radius_mm, 0, z0))).rotate(Axis.Z, angle_deg)
        spacer.label = f"{NAMESPACE}_spacer_station_{angle_deg:g}_{z0:g}"
        children.append(spacer)

    if include_hardware:
        axle = Cylinder(
            SPEC.axle_finished_diameter_mm / 2,
            SPEC.axle_z_mm[1] - SPEC.axle_z_mm[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.roller_axis_radius_mm, 0, SPEC.axle_z_mm[0]))).rotate(Axis.Z, angle_deg)
        axle.label = f"{NAMESPACE}_D4x25_polished_axle_REFERENCE_station_{angle_deg:g}"
        axle.color = srgb("#B7B9B5")
        children.append(axle)

        for index, (z0, z1) in enumerate(SPEC.washer_ranges_z_mm, 1):
            washer = Cylinder(SPEC.washer_od_mm / 2, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
                Cylinder(SPEC.washer_bore_mm / 2, z1 - z0 + 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                    Location((0, 0, -0.1))
                )
            ).moved(Location((SPEC.roller_axis_radius_mm, 0, z0))).rotate(Axis.Z, angle_deg)
            washer.label = f"{NAMESPACE}_thrust_washer_{index}_station_{angle_deg:g}_REFERENCE"
            children.append(washer)

        collar = Cylinder(
            SPEC.collar_od_mm / 2,
            SPEC.collar_z_mm[1] - SPEC.collar_z_mm[0],
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).cut(
            Cylinder(
                SPEC.collar_bore_mm / 2,
                SPEC.collar_z_mm[1] - SPEC.collar_z_mm[0] + 0.2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((0, 0, -0.1)))
        ).moved(Location((SPEC.roller_axis_radius_mm, 0, SPEC.collar_z_mm[0]))).rotate(Axis.Z, angle_deg)
        collar.label = f"{NAMESPACE}_D4_split_collar_REFERENCE_station_{angle_deg:g}"
        collar.color = srgb("#B7B9B5")
        children.append(collar)

        for tangent in SPEC.outer_mount_tangent_mm:
            x, y = local_point(angle_deg, SPEC.outer_mount_radius_mm, tangent)
            shaft = Cylinder(
                SPEC.station_screw_diameter_mm / 2,
                SPEC.station_screw_length_mm - SPEC.countersink_target_depth_mm,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, SPEC.countersink_apex_z_mm)))
            head = Cone(
                SPEC.countersink_major_diameter_mm / 2,
                SPEC.station_screw_diameter_mm / 2,
                SPEC.countersink_target_depth_mm,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, SPEC.rear_datum_z_mm)))
            screw = Compound(children=[head, shaft], label=f"{NAMESPACE}_M3x10_flat_head_REFERENCE_{angle_deg:g}_{tangent:g}")
            children.append(screw)
            nut_bottom, _ = SPEC.station_nut_pocket_z_mm
            children.append(
                _ordinary_m3_nut_reference(
                    angle_deg,
                    SPEC.outer_mount_radius_mm,
                    tangent,
                    nut_bottom,
                    f"{NAMESPACE}_ordinary_M3_station_nut_REFERENCE_{angle_deg:g}_{tangent:g}",
                )
            )

        for tangent in SPEC.bridge_screw_tangent_mm:
            x, y = local_point(angle_deg, SPEC.bridge_screw_radius_mm, tangent)
            bridge_screw = Cylinder(
                SPEC.bridge_screw_diameter_mm / 2,
                SPEC.bridge_screw_length_mm,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            ).moved(Location((x, y, SPEC.bridge_z_mm[1])))
            bridge_screw.label = f"{NAMESPACE}_M3x6_bridge_screw_REFERENCE_{angle_deg:g}_{tangent:g}"
            children.append(bridge_screw)
            children.append(
                _ordinary_m3_nut_reference(
                    angle_deg,
                    SPEC.bridge_screw_radius_mm,
                    tangent,
                    SPEC.bridge_z_mm[0] - SPEC.bridge_nut_thickness_mm,
                    f"{NAMESPACE}_ordinary_M3_bridge_nut_REFERENCE_{angle_deg:g}_{tangent:g}",
                )
            )

    return Compound(children=children, label=f"{NAMESPACE}_station_{angle_deg:g}deg")


def make_three_station_context():
    # Existing canonical base sectors are references only; R1 produces no
    # derivative sector, replacement base STEP, or base 3MF.
    children = [named_sector(1).rotate(Axis.Z, angle) for angle in (0.0, 120.0, 240.0)]
    for index, sector in enumerate(children, 1):
        sector.label = f"{NAMESPACE}_EXISTING_CANONICAL_Q3_R0_sector_{index}_REFERENCE_UNCHANGED"
    children.extend(_ring_reference(index) for index in range(3))
    for angle in SPEC.station_angles_deg:
        children.extend(make_station_assembly(angle).children)
    return Compound(children=children, label=f"{NAMESPACE}_THREE_STATIONS_RETROFIT_EXISTING_BASE_CONTEXT")


def make_service_exploded():
    children = [_ring_reference(index) for index in range(3)]
    for station_index, angle in enumerate(SPEC.station_angles_deg):
        radial_lift = 18.0 + station_index * 4.0
        dx = -radial_lift * cos(radians(angle))
        dy = -radial_lift * sin(radians(angle))
        module = make_station_assembly(angle)
        for index, part in enumerate(module.children):
            children.append(part.moved(Location((dx, dy, 8.0 + index * 1.5))))
    return Compound(children=children, label=f"{NAMESPACE}_SERVICE_EXPLODED")


def make_print_station_kit():
    children = [
        make_station_frame_print(),
        make_upper_bridge_print().moved(Location((35, 0, 0))),
    ]
    for index in range(3):
        children.append(make_spool_print().moved(Location((45 + 15 * index, 0, 0))))
    for index in range(2):
        children.append(make_spacer_print().moved(Location((45 + 15 * index, 15, 0))))
    return Compound(children=children, label=f"{NAMESPACE}_ONE_STATION_PRINT_KIT_PRINT_QTY3")
