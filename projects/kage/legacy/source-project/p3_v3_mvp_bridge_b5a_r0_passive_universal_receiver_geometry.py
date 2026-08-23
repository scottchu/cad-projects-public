"""Actual BREP geometry for the B5A passive bridge/receiver MVP."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import atan2, cos, degrees, radians, sin, sqrt

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude

import p3_v3_mvp_rings_b4_r1_exact_involute_mesh_geometry as b4
import p3_v3_mvp_roller_b3_r1_blind_axle_towers_geometry as b3
from p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver_spec import NAMESPACE, SPEC, RoleDatum


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(solid.volume for solid in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    if left is None or right is None:
        return 0.0
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def _one(shape, label: str):
    solids = tuple(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be exactly one solid, got {len(solids)}")
    result = solids[0]
    if not result.is_valid or result.volume <= 0.0:
        raise RuntimeError(f"{label} must be a valid positive-volume solid")
    result.label = label
    return result


def polar(radius_mm: float, angle_deg: float, tangent_mm: float = 0.0) -> tuple[float, float]:
    angle = radians(angle_deg)
    return (
        radius_mm * cos(angle) - tangent_mm * sin(angle),
        radius_mm * sin(angle) + tangent_mm * cos(angle),
    )


def vertical_cylinder(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    diameter_mm: float,
    z0_mm: float,
    height_mm: float,
):
    x, y = polar(radius_mm, angle_deg, tangent_mm)
    return Cylinder(
        diameter_mm / 2.0,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0_mm)))


def local_box(
    angle_deg: float,
    radial_min_mm: float,
    radial_max_mm: float,
    tangent_min_mm: float,
    tangent_max_mm: float,
    z_min_mm: float,
    z_max_mm: float,
):
    return Box(
        radial_max_mm - radial_min_mm,
        tangent_max_mm - tangent_min_mm,
        z_max_mm - z_min_mm,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((radial_min_mm, tangent_min_mm, z_min_mm))).rotate(Axis.Z, angle_deg)


def annulus_sector(
    radial_min_mm: float,
    radial_max_mm: float,
    angle_min_deg: float,
    angle_max_deg: float,
    z_min_mm: float,
    z_max_mm: float,
):
    annulus = Cylinder(
        radial_max_mm,
        z_max_mm - z_min_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z_min_mm))).cut(
        Cylinder(
            radial_min_mm,
            z_max_mm - z_min_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((0.0, 0.0, z_min_mm - 0.1)))
    )
    points = [(0.0, 0.0)]
    for index in range(33):
        points.append(polar(radial_max_mm + 5.0, angle_min_deg + (angle_max_deg - angle_min_deg) * index / 32.0))
    points.append((0.0, 0.0))
    mask = extrude(Polygon(*points), amount=z_max_mm - z_min_mm + 0.4).moved(
        Location((0.0, 0.0, z_min_mm - 0.2))
    )
    clipped = annulus.intersect(mask)
    solids = tuple(clipped.solids())
    if not solids:
        raise RuntimeError("annulus sector produced no solid")
    return max(solids, key=lambda solid: solid.volume)


def capsule_between(
    start_xy: tuple[float, float],
    end_xy: tuple[float, float],
    width_mm: float,
    z_min_mm: float,
    z_max_mm: float,
):
    dx, dy = end_xy[0] - start_xy[0], end_xy[1] - start_xy[1]
    length = sqrt(dx * dx + dy * dy)
    angle = degrees(atan2(dy, dx))
    height = z_max_mm - z_min_mm
    body = Box(
        length,
        width_mm,
        height,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).rotate(Axis.Z, angle).moved(Location((start_xy[0], start_xy[1], z_min_mm)))
    ends = tuple(
        Cylinder(width_mm / 2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((point[0], point[1], z_min_mm))
        )
        for point in (start_xy, end_xy)
    )
    return body.fuse(*ends)


def _hex_prism(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    across_flats_mm: float,
    z_min_mm: float,
    height_mm: float,
):
    circumradius = across_flats_mm / sqrt(3.0)
    points = tuple(
        (
            circumradius * cos(radians(30.0 + index * 60.0)),
            circumradius * sin(radians(30.0 + index * 60.0)),
        )
        for index in range(6)
    )
    shape = extrude(Polygon(*points), amount=height_mm).moved(Location((radius_mm, tangent_mm, z_min_mm)))
    return shape.rotate(Axis.Z, angle_deg)


def _entry_chamfers(role: RoleDatum, floor_bottom_z: float):
    r0 = SPEC.receiver_floor_radii_mm[0]
    c = SPEC.channel_width_mm / 2.0
    d = SPEC.insertion_chamfer_mm
    height = role.receiver_top_z_mm - floor_bottom_z + 0.2
    upper = extrude(
        Polygon((r0 - 0.1, c - 0.1), (r0 + d, c - 0.1), (r0 - 0.1, c + d)),
        amount=height,
    ).moved(Location((0.0, 0.0, floor_bottom_z - 0.1)))
    lower = extrude(
        Polygon((r0 - 0.1, -c + 0.1), (r0 + d, -c + 0.1), (r0 - 0.1, -c - d)),
        amount=height,
    ).moved(Location((0.0, 0.0, floor_bottom_z - 0.1)))
    return upper.rotate(Axis.Z, role.receiver_angle_deg), lower.rotate(Axis.Z, role.receiver_angle_deg)


def _receiver_body(role: RoleDatum):
    floor_r0, floor_r1 = SPEC.receiver_floor_radii_mm
    half_overall = SPEC.overall_tangential_width_mm / 2.0
    half_channel = SPEC.channel_width_mm / 2.0
    tongue_bottom = role.receiver_top_z_mm - SPEC.future_tongue_max_thickness_mm
    floor_bottom = tongue_bottom - SPEC.floor_thickness_mm

    floor = local_box(
        role.receiver_angle_deg, floor_r0, floor_r1, -half_overall, half_overall,
        floor_bottom, tongue_bottom,
    )
    walls = tuple(
        local_box(
            role.receiver_angle_deg, floor_r0, floor_r1, t0, t1,
            floor_bottom, role.receiver_top_z_mm,
        )
        for t0, t1 in ((-half_overall, -half_channel), (half_channel, half_overall))
    )
    lip_r0 = floor_r1 - SPEC.capture_lip_radial_length_mm
    lip_inner = half_channel - SPEC.capture_lip_total_mm / 2.0
    lips = tuple(
        local_box(
            role.receiver_angle_deg, lip_r0, floor_r1, t0, t1,
            role.receiver_top_z_mm - SPEC.capture_lip_thickness_mm,
            role.receiver_top_z_mm,
        )
        for t0, t1 in ((-half_overall, -lip_inner), (lip_inner, half_overall))
    )

    # The under-floor boss contains the captured nut and a closed blind tip
    # well.  A radial center-side service slot admits the nut before the tongue.
    boss_bottom = (
        floor_bottom
        - SPEC.captured_nut_thickness_mm
        - SPEC.blind_tip_well_depth_mm
        - SPEC.blind_floor_clearance_min_mm
    )
    boss = vertical_cylinder(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.captured_nut_af_mm + 2.4,
        boss_bottom,
        tongue_bottom - boss_bottom,
    )
    clamp_bore = vertical_cylinder(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.receiver_clearance_diameter_mm,
        floor_bottom - 0.1,
        role.receiver_top_z_mm - floor_bottom + 0.2,
    )
    nut_top = floor_bottom
    nut_bottom = nut_top - SPEC.captured_nut_thickness_mm
    nut_pocket = _hex_prism(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.captured_nut_af_mm,
        nut_bottom,
        SPEC.captured_nut_thickness_mm + 0.05,
    )
    nut_service = local_box(
        role.receiver_angle_deg,
        floor_r0 - 0.2,
        SPEC.clamp_axis_radius_mm,
        -SPEC.captured_nut_af_mm / 2.0,
        SPEC.captured_nut_af_mm / 2.0,
        nut_bottom,
        nut_top + 0.05,
    )
    tip_well = vertical_cylinder(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.receiver_clearance_diameter_mm,
        nut_bottom - SPEC.blind_tip_well_depth_mm,
        SPEC.blind_tip_well_depth_mm + 0.05,
    )
    chamfers = _entry_chamfers(role, floor_bottom)
    return floor.fuse(*walls, *lips, boss).cut(
        clamp_bore, nut_pocket, nut_service, tip_well, *chamfers
    )


def _bridge_structure(role: RoleDatum):
    band_z0, band_z1 = SPEC.structural_band_z_mm
    band = annulus_sector(
        role.band_radii_mm[0], role.band_radii_mm[1],
        role.band_angles_deg[0], role.band_angles_deg[1],
        band_z0, band_z1,
    )
    mount_points = tuple(
        polar(role.mount_radius_mm, role.anchor_angle_deg, tangent)
        for tangent in SPEC.mount_axis_tangent_mm
    )
    target_angles = (role.band_angles_deg[0] + 1.5, role.band_angles_deg[0] + 5.5)
    target_radius = sum(role.band_radii_mm) / 2.0
    targets = tuple(polar(target_radius, angle) for angle in target_angles)
    ear_z0, ear_z1 = SPEC.capture_ear_z_mm
    # The escape struts remain in the 0.40 mm capture-ear layer until they are
    # radially inboard of the tower/roller envelope, then overlap the arc band.
    # This is the center-service, no-tower-edit route.
    inner_waypoints = tuple(
        polar(role.band_radii_mm[1] + 0.8, role.anchor_angle_deg, tangent)
        for tangent in SPEC.mount_axis_tangent_mm
    )
    locator_escapes = tuple(
        segment
        for start, waypoint, end in zip(mount_points, inner_waypoints, targets)
        for segment in (
            capsule_between(start, waypoint, SPEC.escape_strut_width_mm, ear_z0, ear_z1),
            capsule_between(waypoint, end, SPEC.escape_strut_width_mm, ear_z0, ear_z1),
        )
    )
    web_z0, web_z1 = SPEC.post_roller_web_z_mm
    thick_escapes = tuple(
        segment
        for start, waypoint, end in zip(mount_points, inner_waypoints, targets)
        for segment in (
            capsule_between(start, waypoint, SPEC.escape_strut_width_mm, web_z0, web_z1),
            capsule_between(waypoint, end, SPEC.escape_strut_width_mm, web_z0, web_z1),
        )
    )

    ears = tuple(
        vertical_cylinder(
            role.anchor_angle_deg,
            role.mount_radius_mm,
            tangent,
            SPEC.capture_ear_outer_diameter_mm,
            ear_z0,
            ear_z1 - ear_z0,
        )
        for tangent in SPEC.mount_axis_tangent_mm
    )

    # Two structural side ribs rise from the arc band to the complete R128.4
    # outboard channel datum.  Circular R2 roots are constructive gussets.
    half_rib_spacing = (SPEC.overall_tangential_width_mm - SPEC.side_rib_width_mm) / 2.0
    mast_start_r = role.band_radii_mm[1] - SPEC.root_fillet_radius_mm
    mast_end_r = SPEC.receiver_bulk_max_radius_mm - SPEC.side_rib_width_mm / 2.0
    tongue_bottom = role.receiver_top_z_mm - SPEC.future_tongue_max_thickness_mm
    floor_bottom = tongue_bottom - SPEC.floor_thickness_mm
    mast_z0 = min(band_z0, floor_bottom)
    mast_z1 = max(band_z1, tongue_bottom)
    masts = tuple(
        capsule_between(
            polar(mast_start_r, role.receiver_angle_deg, tangent),
            polar(mast_end_r, role.receiver_angle_deg, tangent),
            SPEC.side_rib_width_mm,
            mast_z0,
            mast_z1,
        )
        for tangent in (-half_rib_spacing, half_rib_spacing)
    )
    roots = tuple(
        vertical_cylinder(
            role.receiver_angle_deg,
            mast_start_r,
            tangent,
            2.0 * SPEC.root_fillet_radius_mm,
            mast_z0,
            mast_z1 - mast_z0,
        )
        for tangent in (-half_rib_spacing, half_rib_spacing)
    )
    relief_z0 = mast_z0 - SPEC.boolean_overshoot_mm
    roller_footprint = vertical_cylinder(
        role.anchor_angle_deg,
        SPEC.inherited_roller_axle_radius_mm,
        0.0,
        SPEC.inherited_hour_roller_outer_diameter_mm
        + 2.0 * SPEC.stationary_roller_clearance_mm,
        relief_z0,
        mast_z1 - relief_z0 + SPEC.boolean_overshoot_mm,
    )
    structural = band.fuse(*thick_escapes, *masts, *roots).cut(
        roller_footprint,
        deepcopy(b3.tower_shape(role.anchor_angle_deg)),
    )
    locator = ears[0].fuse(*ears[1:], *locator_escapes)
    return structural.fuse(locator)


@lru_cache(maxsize=3)
def bridge_receiver_shape(role_index: int):
    role = SPEC.roles[role_index]
    raw = _bridge_structure(role).fuse(_receiver_body(role))
    mount_bores = tuple(
        vertical_cylinder(
            role.anchor_angle_deg,
            role.mount_radius_mm,
            tangent,
            SPEC.capture_ear_bore_diameter_mm,
            SPEC.structural_band_z_mm[0] - 0.2,
            SPEC.capture_ear_z_mm[1] - SPEC.structural_band_z_mm[0] + 0.4,
        )
        for tangent in SPEC.mount_axis_tangent_mm
    )
    return _one(
        raw.cut(*mount_bores),
        f"{NAMESPACE}_{role.name}_printed_passive_bridge_receiver",
    )


def slot_tool(z_min_mm: float, height_mm: float):
    straight = SPEC.tongue_slot_radial_length_mm - SPEC.tongue_slot_width_mm
    half_straight = straight / 2.0
    radius = SPEC.tongue_slot_width_mm / 2.0
    body = Box(
        straight,
        SPEC.tongue_slot_width_mm,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z_min_mm)))
    ends = tuple(
        Cylinder(radius, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, 0.0, z_min_mm))
        )
        for x in (-half_straight, half_straight)
    )
    return body.fuse(*ends)


@lru_cache(maxsize=1)
def alignment_gauge_shape():
    # Local gauge datum: slot center at X=0; active datum is +14.65 mm.
    inboard_x = -(SPEC.gauge_radial_length_mm - SPEC.active_offset_from_slot_center_mm - SPEC.gauge_outboard_nose_mm)
    plate = Box(
        SPEC.gauge_radial_length_mm,
        SPEC.gauge_tangential_width_mm,
        SPEC.gauge_thickness_mm,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((inboard_x, 0.0, 0.0)))
    slot = slot_tool(-0.1, SPEC.gauge_thickness_mm + 0.2)
    half_width = SPEC.gauge_tangential_width_mm / 2.0
    lead = SPEC.gauge_lead_in_mm
    lead_upper = extrude(
        Polygon((inboard_x - 0.1, half_width + 0.1), (inboard_x + lead, half_width + 0.1), (inboard_x - 0.1, half_width - lead)),
        amount=SPEC.gauge_thickness_mm + 0.2,
    ).moved(Location((0.0, 0.0, -0.1)))
    lead_lower = extrude(
        Polygon((inboard_x - 0.1, -half_width - 0.1), (inboard_x + lead, -half_width - 0.1), (inboard_x - 0.1, -half_width + lead)),
        amount=SPEC.gauge_thickness_mm + 0.2,
    ).moved(Location((0.0, 0.0, -0.1)))
    x = SPEC.active_offset_from_slot_center_mm
    d = SPEC.gauge_v_notch_depth_mm
    z0 = SPEC.gauge_thickness_mm - SPEC.gauge_v_notch_below_top_mm
    notch_height = SPEC.gauge_v_notch_below_top_mm + 0.1
    upper = extrude(
        Polygon((x - d, half_width + 0.1), (x, half_width - d), (x + d, half_width + 0.1)),
        amount=notch_height,
    ).moved(Location((0.0, 0.0, z0)))
    lower = extrude(
        Polygon((x - d, -half_width - 0.1), (x, -half_width + d), (x + d, -half_width - 0.1)),
        amount=notch_height,
    ).moved(Location((0.0, 0.0, z0)))
    return _one(plate.cut(slot, lead_upper, lead_lower, upper, lower), f"{NAMESPACE}_{SPEC.gauge_label}")


def gauge_at_role(role_index: int, active_radius_mm: float):
    role = SPEC.roles[role_index]
    slot_center_radius = active_radius_mm - SPEC.active_offset_from_slot_center_mm
    z0 = role.receiver_top_z_mm - SPEC.gauge_thickness_mm
    shape = deepcopy(alignment_gauge_shape()).moved(Location((slot_center_radius, 0.0, z0))).rotate(
        Axis.Z, role.receiver_angle_deg
    )
    shape.label = f"{NAMESPACE}_{role.name}_{SPEC.gauge_label}_R{active_radius_mm:.2f}"
    return shape


def receiver_hardware_witnesses(role_index: int) -> tuple:
    role = SPEC.roles[role_index]
    tongue_top = role.receiver_top_z_mm
    washer = vertical_cylinder(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.washer_od_mm,
        tongue_top,
        SPEC.washer_thickness_mm,
    ).cut(
        vertical_cylinder(
            role.receiver_angle_deg,
            SPEC.clamp_axis_radius_mm,
            0.0,
            SPEC.washer_id_mm,
            tongue_top - 0.05,
            SPEC.washer_thickness_mm + 0.1,
        )
    )
    washer = _one(washer, f"{NAMESPACE}_{role.name}_purchased_M3_washer")
    under_head = tongue_top + SPEC.washer_thickness_mm
    shaft = vertical_cylinder(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.receiver_screw_diameter_mm,
        under_head - SPEC.receiver_screw_length_mm,
        SPEC.receiver_screw_length_mm,
    )
    head = vertical_cylinder(
        role.receiver_angle_deg,
        SPEC.clamp_axis_radius_mm,
        0.0,
        SPEC.receiver_screw_head_diameter_mm,
        under_head,
        SPEC.receiver_screw_head_height_mm,
    )
    screw = _one(shaft.fuse(head), f"{NAMESPACE}_{role.name}_purchased_M3x10")
    floor_bottom = role.receiver_top_z_mm - SPEC.future_tongue_max_thickness_mm - SPEC.floor_thickness_mm
    nut = _one(
        _hex_prism(
            role.receiver_angle_deg,
            SPEC.clamp_axis_radius_mm,
            0.0,
            SPEC.purchased_nut_af_mm,
            floor_bottom - SPEC.captured_nut_thickness_mm,
            SPEC.captured_nut_thickness_mm,
        ),
        f"{NAMESPACE}_{role.name}_purchased_AF5p5_nut",
    )
    return screw, washer, nut


def b5a_assembled_occurrences() -> tuple:
    children = []
    for role_index in range(3):
        children.append(deepcopy(bridge_receiver_shape(role_index)))
        children.extend(receiver_hardware_witnesses(role_index))
    return tuple(children)


def b5a_exploded_occurrences() -> tuple:
    children = []
    for role_index, role in enumerate(SPEC.roles):
        offset = polar(30.0 + 12.0 * role_index, role.receiver_angle_deg)
        receiver = deepcopy(bridge_receiver_shape(role_index)).moved(
            Location((offset[0], offset[1], 30.0 + 16.0 * role_index))
        )
        receiver.label = f"{NAMESPACE}_step_01_mount_{role.name}_bridge_on_shared_B3_M3x8"
        children.append(receiver)
        for hardware_index, hardware in enumerate(receiver_hardware_witnesses(role_index), start=1):
            moved = hardware.moved(Location((offset[0], offset[1], 42.0 + 16.0 * role_index + hardware_index * 4.0)))
            moved.label = f"{NAMESPACE}_step_02_{role.name}_receiver_hardware_{hardware_index}"
            children.append(moved)
    gauge = deepcopy(alignment_gauge_shape()).moved(Location((-11.0, 0.0, 85.0)))
    gauge.label = f"{NAMESPACE}_step_03_{SPEC.gauge_label}_center_service_tool"
    children.append(gauge)
    return tuple(children)


def assembled_shape():
    children = [deepcopy(child) for child in b4.assembled_shape().children]
    children.extend(b5a_assembled_occurrences())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_no_sensor")


def exploded_shape():
    children = [deepcopy(child).moved(Location((0.0, 0.0, -30.0))) for child in b4.assembled_shape().children]
    children.extend(b5a_exploded_occurrences())
    return Compound(children=children, label=f"{NAMESPACE}_exploded_center_service_no_sensor")


def printable_occurrences() -> tuple[dict[str, object], ...]:
    rows = []
    for role_index, role in enumerate(SPEC.roles):
        source = bridge_receiver_shape(role_index)
        shape = deepcopy(source).moved(Location((0.0, 0.0, -source.bounding_box().min.Z)))
        label = f"{NAMESPACE}_{role.name}_bridge_receiver_print_orientation"
        shape.label = label
        rows.append({"name": f"{role.name}_bridge_receiver", "label": label, "shape": shape})
    gauge = deepcopy(alignment_gauge_shape())
    label = f"{NAMESPACE}_{SPEC.gauge_label}_print_orientation"
    gauge.label = label
    rows.append({"name": "alignment_gauge", "label": label, "shape": gauge})
    return tuple(rows)


def printed_additions_shape():
    return Compound(
        children=[*(bridge_receiver_shape(index) for index in range(3)), alignment_gauge_shape()],
        label=f"{NAMESPACE}_exactly_four_printed_solids",
    )
