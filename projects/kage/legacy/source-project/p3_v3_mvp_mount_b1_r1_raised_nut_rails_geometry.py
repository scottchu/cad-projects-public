"""Actual BREP geometry for the B1-R1 raised captive-nut rail MVP.

The four base quadrants are rebuilt from the immutable R4 source immediately
before its legacy mount cuts.  All B1 changes are then applied inside explicit
localized receiver masks.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude

import p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry as r4
from p3_v3_mvp_mount_b1_r1_raised_nut_rails_spec import NAMESPACE, SPEC


LAPS = r4.LAPS


def _single_solid(shape, label: str):
    solids = [] if shape is None else list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    result.label = label
    return result


def volume_mm3(shape) -> float:
    return 0.0 if shape is None else float(sum(s.volume for s in shape.solids()))


def intersection_volume_mm3(left, right) -> float:
    if left is None or right is None:
        return 0.0
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def local_point(angle_deg: float, radius_mm: float, tangent_mm: float) -> tuple[float, float]:
    a = radians(angle_deg)
    return (
        radius_mm * cos(a) - tangent_mm * sin(a),
        radius_mm * sin(a) + tangent_mm * cos(a),
    )


def _local_box(angle: float, r0: float, r1: float, t0: float, t1: float, z0: float, height: float):
    return Box(
        r1 - r0, t1 - t0, height, align=(Align.MIN, Align.MIN, Align.MIN)
    ).moved(Location((r0, t0, z0))).rotate(Axis.Z, angle)


def vertical_cylinder(angle: float, radius: float, tangent: float, diameter: float, z0: float, height: float):
    x, y = local_point(angle, radius, tangent)
    return Cylinder(
        diameter / 2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((x, y, z0)))


def _hex_prism(
    angle: float,
    radius: float,
    tangent: float,
    across_flats: float,
    z0: float,
    height: float,
    clock_deg: float = 0.0,
):
    cr = across_flats / (2.0 * cos(radians(30.0)))
    wire = Polygon(*tuple(
        (
            radius + cr * cos(radians(30.0 + clock_deg + 60.0 * i)),
            tangent + cr * sin(radians(30.0 + clock_deg + 60.0 * i)),
        )
        for i in range(6)
    ))
    return extrude(wire, amount=height).moved(Location((0.0, 0.0, z0))).rotate(Axis.Z, angle)


def radial_capsule(angle: float, radius: float, tangent: float, width: float, overall_length: float, z0: float, height: float):
    spacing = overall_length - width
    body = _local_box(
        angle,
        radius - spacing / 2.0,
        radius + spacing / 2.0,
        tangent - width / 2.0,
        tangent + width / 2.0,
        z0,
        height,
    )
    ends = tuple(
        vertical_cylinder(angle, radius + dr, tangent, width, z0, height)
        for dr in (-spacing / 2.0, spacing / 2.0)
    )
    return _single_solid(body.fuse(*ends), f"{NAMESPACE}_radial_capsule")


def _quadrant_owner(angle_deg: float) -> int:
    a = angle_deg % 360.0
    if 45.0 <= a < 135.0:
        return 1
    if 135.0 <= a < 225.0:
        return 2
    if 225.0 <= a < 315.0:
        return 3
    return 4


@lru_cache(maxsize=1)
def _r4_pre_mount_quadrants() -> tuple:
    """Exact R4 quadrants after laps/seam hardware but before mount voids."""

    quadrants = [deepcopy(shape) for shape in r4.plain_quadrant_shapes()]
    for seam_name, angle, upper_index, lower_index in LAPS:
        quadrants[upper_index - 1] = _single_solid(
            quadrants[upper_index - 1]
            .cut(r4.receiver_lower_layer_cut_tool(angle))
            .fuse(r4.upper_donor_shape(angle)),
            f"{NAMESPACE}_Q{upper_index}_{seam_name}_upper",
        )
        quadrants[lower_index - 1] = _single_solid(
            quadrants[lower_index - 1]
            .cut(r4.receiver_upper_layer_cut_tool(angle))
            .fuse(r4.lower_receiver_shape(angle)),
            f"{NAMESPACE}_Q{lower_index}_{seam_name}_lower",
        )
    for lap_index, (_, _, upper_index, lower_index) in enumerate(LAPS):
        for radius in r4.SPEC.seam_screw_axis_radii_mm:
            quadrants[upper_index - 1] = _single_solid(
                quadrants[upper_index - 1]
                .fuse(r4.bearing_boss_shape(lap_index, radius))
                .cut(r4.upper_clearance_tool(lap_index, radius)),
                f"{NAMESPACE}_Q{upper_index}_seam_boss",
            )
            quadrants[lower_index - 1] = _single_solid(
                quadrants[lower_index - 1].cut(
                    r4.nut_trap_tool(lap_index, radius),
                    r4.tip_relief_tool(lap_index, radius),
                ),
                f"{NAMESPACE}_Q{lower_index}_seam_trap",
            )
    return tuple(quadrants)


def _motor_rail_features(angle: float, radius: float, tangent: float):
    outward_open = radius == max(SPEC.motor_axis_radii_mm)
    c0 = radius - SPEC.motor_channel_working_length_mm / 2.0
    c1 = radius + SPEC.motor_channel_working_length_mm / 2.0
    if outward_open:
        e0, e1 = c0 - SPEC.receiver_sidewall_mm, c1
        nib_r0, nib_r1 = c1 - SPEC.receiver_nib_radial_length_mm, c1 + 0.05
    else:
        e0, e1 = c0, c1 + SPEC.receiver_sidewall_mm
        nib_r0, nib_r1 = c0 - 0.05, c0 + SPEC.receiver_nib_radial_length_mm
    body = _local_box(
        angle, e0, e1,
        tangent - SPEC.motor_rail_external_width_mm / 2.0,
        tangent + SPEC.motor_rail_external_width_mm / 2.0,
        SPEC.plate_top_z_mm - 0.20,
        SPEC.receiver_roof_top_z_mm - (SPEC.plate_top_z_mm - 0.20),
    )
    channel = _local_box(
        angle,
        c0 - (SPEC.nut_insertion_approach_length_mm if not outward_open else 0.0),
        c1 + (SPEC.nut_insertion_approach_length_mm if outward_open else 0.0),
        tangent - SPEC.nut_channel_width_mm / 2.0,
        tangent + SPEC.nut_channel_width_mm / 2.0,
        SPEC.receiver_channel_bottom_z_mm,
        SPEC.receiver_channel_height_mm,
    )
    top_slot = radial_capsule(
        angle, radius, tangent,
        SPEC.motor_top_slot_width_mm,
        SPEC.motor_top_slot_overall_length_mm,
        SPEC.receiver_channel_top_z_mm - 0.05,
        SPEC.receiver_roof_thickness_mm + 0.10,
    )
    tip_relief = radial_capsule(
        angle, radius, tangent,
        SPEC.m3_clearance_diameter_mm,
        SPEC.motor_top_slot_overall_length_mm,
        SPEC.receiver_channel_bottom_z_mm - SPEC.receiver_tip_relief_depth_mm,
        SPEC.receiver_tip_relief_depth_mm + 0.02,
    )
    nibs = ()
    mask = _local_box(
        angle,
        min(e0, c0 - (SPEC.nut_insertion_approach_length_mm if not outward_open else 0.0)) - 0.25,
        max(e1, c1 + (SPEC.nut_insertion_approach_length_mm if outward_open else 0.0)) + 0.25,
        tangent - SPEC.motor_rail_external_width_mm / 2.0 - 0.25,
        tangent + SPEC.motor_rail_external_width_mm / 2.0 + 0.25,
        SPEC.plate_bottom_z_mm - 0.1,
        SPEC.receiver_roof_top_z_mm - SPEC.plate_bottom_z_mm + 0.2,
    )
    return body, channel, top_slot, tip_relief, nibs, mask


def _static_rail_features(angle: float, radius: float, external_tangent_length: float):
    channel_half = SPEC.fixed_channel_tangential_length_mm / 2.0
    # Positive tangential end is the insertion mouth; negative end is closed.
    e1 = channel_half
    e0 = e1 - external_tangent_length
    if -channel_half - e0 < SPEC.receiver_sidewall_mm - 1e-9:
        raise ValueError("static rail closed end is below minimum sidewall")
    body = _local_box(
        angle,
        radius - SPEC.fixed_rail_radial_width_mm / 2.0,
        radius + SPEC.fixed_rail_radial_width_mm / 2.0,
        e0,
        e1,
        SPEC.plate_top_z_mm - 0.20,
        SPEC.receiver_roof_top_z_mm - (SPEC.plate_top_z_mm - 0.20),
    )
    channel = _local_box(
        angle,
        radius - SPEC.nut_channel_width_mm / 2.0,
        radius + SPEC.nut_channel_width_mm / 2.0,
        -channel_half,
        channel_half + SPEC.nut_insertion_approach_length_mm,
        SPEC.receiver_channel_bottom_z_mm,
        SPEC.receiver_channel_height_mm,
    )
    holes = tuple(
        vertical_cylinder(
            angle, radius, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_channel_top_z_mm - 0.05,
            SPEC.receiver_roof_thickness_mm + 0.10,
        )
        for tangent in SPEC.fixed_axis_tangent_offsets_mm
    )
    tips = tuple(
        vertical_cylinder(
            angle, radius, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_channel_bottom_z_mm - SPEC.receiver_tip_relief_depth_mm,
            SPEC.receiver_tip_relief_depth_mm + 0.02,
        )
        for tangent in SPEC.fixed_axis_tangent_offsets_mm
    )
    nibs = ()
    mask = _local_box(
        angle,
        radius - SPEC.fixed_rail_radial_width_mm / 2.0 - 0.25,
        radius + SPEC.fixed_rail_radial_width_mm / 2.0 + 0.25,
        e0 - 0.25,
        e1 + SPEC.nut_insertion_approach_length_mm + 0.25,
        SPEC.plate_bottom_z_mm - 0.1,
        SPEC.receiver_roof_top_z_mm - SPEC.plate_bottom_z_mm + 0.2,
    )
    return body, channel, holes, tips, nibs, mask


@lru_cache(maxsize=1)
def quadrant_shapes() -> tuple:
    quadrants = [deepcopy(shape) for shape in _r4_pre_mount_quadrants()]

    motor_features = []
    for angle in SPEC.motor_station_angles_deg:
        for radius in SPEC.motor_axis_radii_mm:
            for tangent in SPEC.motor_tangent_offsets_mm:
                motor_features.append((angle, _motor_rail_features(angle, radius, tangent)))

    static_features = []
    for angle in SPEC.fixed_angles_deg:
        static_features.append((angle, _static_rail_features(
            angle, SPEC.fixed_center_radius_mm, SPEC.fixed_rail_tangential_length_mm
        )))
    static_features.append((SPEC.spine_angle_deg, _static_rail_features(
        SPEC.spine_angle_deg, SPEC.spine_center_radius_mm, SPEC.spine_foot_tangential_length_mm
    )))

    for angle, (body, channel, slot, tip, nibs, _mask) in motor_features:
        owner = _quadrant_owner(angle) - 1
        quadrants[owner] = _single_solid(
            quadrants[owner].fuse(body),
            f"{NAMESPACE}_quadrant_Q{owner + 1}_motor_receiver",
        )
        # The localized receiver belongs to one quadrant, but its void tools
        # must clear any complementary lap tongue that reaches the channel.
        for index in range(4):
            quadrants[index] = _single_solid(
                quadrants[index].cut(deepcopy(channel), deepcopy(slot), deepcopy(tip)),
                f"{NAMESPACE}_quadrant_Q{index + 1}_motor_void",
            )
    for angle, (body, channel, holes, tips, nibs, _mask) in static_features:
        owner = _quadrant_owner(angle) - 1
        quadrants[owner] = _single_solid(
            quadrants[owner].fuse(body),
            f"{NAMESPACE}_quadrant_Q{owner + 1}_static_receiver",
        )
        for index in range(4):
            quadrants[index] = _single_solid(
                quadrants[index].cut(
                    deepcopy(channel),
                    *(deepcopy(tool) for tool in (*holes, *tips)),
                ),
                f"{NAMESPACE}_quadrant_Q{index + 1}_static_void",
            )

    for index, shape in enumerate(quadrants, 1):
        shape.label = f"{NAMESPACE}_quadrant_Q{index}_localized_R4p1"
    return tuple(quadrants)


def named_quadrant(index: int):
    if index not in range(1, 5):
        raise ValueError("quadrant index must be 1..4")
    return deepcopy(quadrant_shapes()[index - 1])


def motor_sled_shape(q_mm: float = 0.0, angle_deg: float = 0.0):
    if abs(q_mm) > SPEC.motor_service_travel_mm + 1e-9:
        raise ValueError("sled q outside +/-2.5 mm service travel")
    foot = _local_box(
        0.0,
        SPEC.sled_radial_min_mm,
        SPEC.sled_radial_max_mm,
        -SPEC.sled_tangent_half_width_mm,
        SPEC.sled_tangent_half_width_mm,
        SPEC.receiver_roof_top_z_mm,
        SPEC.mounting_foot_thickness_mm,
    )
    holes = tuple(
        vertical_cylinder(
            0.0, radius, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_roof_top_z_mm - 0.1,
            SPEC.mounting_foot_thickness_mm + 0.2,
        )
        for radius in SPEC.motor_axis_radii_mm
        for tangent in SPEC.motor_tangent_offsets_mm
    )
    sled = foot.cut(*holes)
    guide_inner_tangent = (
        abs(SPEC.motor_tangent_offsets_mm[1])
        - SPEC.motor_rail_external_width_mm / 2.0
        - SPEC.sled_guide_clearance_per_side_mm
    )
    shoulders = motor_sled_guide_shoulder_shapes()
    rib = _local_box(
        0.0,
        SPEC.sled_rib_radial_min_mm,
        SPEC.sled_rib_radial_max_mm,
        -SPEC.sled_rib_tangential_mm / 2.0,
        SPEC.sled_rib_tangential_mm / 2.0,
        SPEC.receiver_roof_top_z_mm + SPEC.mounting_foot_thickness_mm - 0.2,
        SPEC.sled_rib_height_mm + 0.2,
    )
    boss = vertical_cylinder(
        0.0,
        SPEC.motor_output_witness_radius_mm,
        0.0,
        SPEC.sled_load_boss_diameter_mm,
        SPEC.receiver_roof_top_z_mm + SPEC.mounting_foot_thickness_mm - 0.2,
        SPEC.sled_load_boss_height_mm + 0.2,
    )
    sled = _single_solid(sled.fuse(*shoulders, rib, boss), f"{NAMESPACE}_reusable_motor_sled")
    if q_mm:
        sled = sled.moved(Location((q_mm, 0.0, 0.0)))
    if angle_deg:
        sled = sled.rotate(Axis.Z, angle_deg)
    sled.label = f"{NAMESPACE}_reusable_motor_sled_q{q_mm:+.2f}_A{angle_deg:03.0f}"
    return sled


def motor_sled_guide_shoulder_shapes(q_mm: float = 0.0, angle_deg: float = 0.0) -> tuple:
    guide_inner_tangent = (
        abs(SPEC.motor_tangent_offsets_mm[1])
        - SPEC.motor_rail_external_width_mm / 2.0
        - SPEC.sled_guide_clearance_per_side_mm
    )
    shoulders = (
        _local_box(
            0.0, SPEC.sled_radial_min_mm, SPEC.sled_radial_max_mm,
            guide_inner_tangent - SPEC.sled_guide_shoulder_thickness_mm,
            guide_inner_tangent,
            SPEC.receiver_roof_top_z_mm - SPEC.sled_guide_shoulder_depth_mm,
            SPEC.sled_guide_shoulder_depth_mm + 0.05,
        ),
        _local_box(
            0.0, SPEC.sled_radial_min_mm, SPEC.sled_radial_max_mm,
            -guide_inner_tangent,
            -guide_inner_tangent + SPEC.sled_guide_shoulder_thickness_mm,
            SPEC.receiver_roof_top_z_mm - SPEC.sled_guide_shoulder_depth_mm,
            SPEC.sled_guide_shoulder_depth_mm + 0.05,
        ),
    )
    moved = tuple(
        shoulder.moved(Location((q_mm, 0.0, 0.0))) if q_mm else shoulder
        for shoulder in shoulders
    )
    if angle_deg:
        moved = tuple(shoulder.rotate(Axis.Z, angle_deg) for shoulder in moved)
    return moved


def fixed_riser_shape(angle_deg: float = 0.0):
    foot = _local_box(
        0.0,
        SPEC.fixed_center_radius_mm - SPEC.fixed_foot_radial_width_mm / 2.0,
        SPEC.fixed_center_radius_mm + SPEC.fixed_foot_radial_width_mm / 2.0,
        -SPEC.fixed_foot_tangential_length_mm / 2.0,
        SPEC.fixed_foot_tangential_length_mm / 2.0,
        SPEC.receiver_roof_top_z_mm,
        SPEC.mounting_foot_thickness_mm,
    )
    holes = tuple(
        vertical_cylinder(
            0.0, SPEC.fixed_center_radius_mm, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_roof_top_z_mm - 0.1,
            SPEC.mounting_foot_thickness_mm + 0.2,
        )
        for tangent in SPEC.fixed_axis_tangent_offsets_mm
    )
    top_pad = _local_box(
        0.0,
        SPEC.fixed_center_radius_mm - SPEC.fixed_foot_radial_width_mm / 2.0,
        SPEC.fixed_center_radius_mm + SPEC.fixed_foot_radial_width_mm / 2.0,
        -SPEC.fixed_foot_tangential_length_mm / 2.0,
        SPEC.fixed_foot_tangential_length_mm / 2.0,
        SPEC.mechanism_interface_z_mm - 3.0,
        3.0,
    )
    stem = _local_box(
        0.0,
        SPEC.fixed_center_radius_mm - SPEC.fixed_stem_radial_width_mm / 2.0,
        SPEC.fixed_center_radius_mm + SPEC.fixed_stem_radial_width_mm / 2.0,
        -SPEC.fixed_stem_tangential_width_mm / 2.0,
        SPEC.fixed_stem_tangential_width_mm / 2.0,
        SPEC.receiver_roof_top_z_mm + SPEC.mounting_foot_thickness_mm - 0.2,
        SPEC.mechanism_interface_z_mm - (
            SPEC.receiver_roof_top_z_mm + SPEC.mounting_foot_thickness_mm - 0.2
        ),
    )
    shaft_tools = tuple(
        vertical_cylinder(
            0.0, SPEC.fixed_center_radius_mm, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_roof_top_z_mm - 0.1,
            SPEC.mounting_foot_thickness_mm + 0.2,
        )
        for tangent in SPEC.fixed_axis_tangent_offsets_mm
    )
    driver_tools = tuple(
        vertical_cylinder(
            0.0, SPEC.fixed_center_radius_mm, tangent, SPEC.driver_path_diameter_mm,
            SPEC.screw_under_head_z_mm - 0.05,
            SPEC.mechanism_interface_z_mm - SPEC.screw_under_head_z_mm + 0.10,
        )
        for tangent in SPEC.fixed_axis_tangent_offsets_mm
    )
    riser = _single_solid(
        foot.fuse(stem, top_pad).cut(*shaft_tools, *driver_tools),
        f"{NAMESPACE}_reusable_fixed_riser",
    )
    if angle_deg:
        riser = riser.rotate(Axis.Z, angle_deg)
    riser.label = f"{NAMESPACE}_reusable_fixed_riser_A{angle_deg:03.0f}"
    return riser


def spine_riser_shape():
    a = SPEC.spine_angle_deg
    foot = _local_box(
        a,
        SPEC.spine_center_radius_mm - SPEC.spine_foot_radial_width_mm / 2.0,
        SPEC.spine_center_radius_mm + SPEC.spine_foot_radial_width_mm / 2.0,
        -SPEC.spine_foot_tangential_length_mm / 2.0,
        SPEC.spine_foot_tangential_length_mm / 2.0,
        SPEC.receiver_roof_top_z_mm,
        SPEC.mounting_foot_thickness_mm,
    )
    holes = tuple(
        vertical_cylinder(
            a, SPEC.spine_center_radius_mm, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_roof_top_z_mm - 0.1,
            SPEC.mounting_foot_thickness_mm + 0.2,
        )
        for tangent in SPEC.spine_axis_tangent_offsets_mm
    )
    stem = _local_box(
        a,
        SPEC.spine_center_radius_mm - SPEC.spine_stem_radial_width_mm / 2.0,
        SPEC.spine_center_radius_mm + SPEC.spine_stem_radial_width_mm / 2.0,
        -SPEC.spine_stem_tangential_width_mm / 2.0,
        SPEC.spine_stem_tangential_width_mm / 2.0,
        SPEC.receiver_roof_top_z_mm + SPEC.mounting_foot_thickness_mm - 0.2,
        SPEC.mechanism_interface_z_mm - (
            SPEC.receiver_roof_top_z_mm + SPEC.mounting_foot_thickness_mm - 0.2
        ),
    )
    top_pad = _local_box(
        a,
        SPEC.spine_center_radius_mm - SPEC.spine_foot_radial_width_mm / 2.0,
        SPEC.spine_center_radius_mm + SPEC.spine_foot_radial_width_mm / 2.0,
        -SPEC.spine_foot_tangential_length_mm / 2.0,
        SPEC.spine_foot_tangential_length_mm / 2.0,
        SPEC.mechanism_interface_z_mm - 3.0,
        3.0,
    )
    shaft_tools = tuple(
        vertical_cylinder(
            a, SPEC.spine_center_radius_mm, tangent, SPEC.m3_clearance_diameter_mm,
            SPEC.receiver_roof_top_z_mm - 0.1,
            SPEC.mounting_foot_thickness_mm + 0.2,
        )
        for tangent in SPEC.spine_axis_tangent_offsets_mm
    )
    driver_tools = tuple(
        vertical_cylinder(
            a, SPEC.spine_center_radius_mm, tangent, SPEC.driver_path_diameter_mm,
            SPEC.screw_under_head_z_mm - 0.05,
            SPEC.mechanism_interface_z_mm - SPEC.screw_under_head_z_mm + 0.10,
        )
        for tangent in SPEC.spine_axis_tangent_offsets_mm
    )
    spine = _single_solid(
        foot.fuse(stem, top_pad).cut(*shaft_tools, *driver_tools),
        f"{NAMESPACE}_spine_riser",
    )
    spine.label = f"{NAMESPACE}_spine_riser_A300"
    return spine


def m3_nut_shape(angle: float, radius: float, tangent: float, clock_deg: float = 0.0):
    nut = _single_solid(
        _hex_prism(
            angle, radius, tangent, SPEC.m3_nut_max_af_mm,
            SPEC.receiver_channel_top_z_mm - SPEC.m3_nut_max_thickness_mm,
            SPEC.m3_nut_max_thickness_mm,
            clock_deg,
        ),
        f"{NAMESPACE}_M3_metal_nut_reference",
    )
    return nut


def m3_screw_shape(angle: float, radius: float, tangent: float):
    shaft = vertical_cylinder(
        angle, radius, tangent, SPEC.m3_screw_diameter_mm,
        SPEC.screw_tip_z_mm, SPEC.m3_screw_length_mm,
    )
    head = vertical_cylinder(
        angle, radius, tangent, SPEC.m3_socket_head_diameter_mm,
        SPEC.screw_under_head_z_mm, SPEC.m3_socket_head_height_mm,
    )
    return _single_solid(shaft.fuse(head), f"{NAMESPACE}_ISO4762_M3x8_reference")


def installed_mount_hardware() -> tuple:
    axes = []
    for radius in SPEC.motor_axis_radii_mm:
        for tangent in SPEC.motor_tangent_offsets_mm:
            axes.append((0.0, radius, tangent, "motor"))
    for tangent in SPEC.fixed_axis_tangent_offsets_mm:
        axes.append((60.0, SPEC.fixed_center_radius_mm, tangent, "fixed"))
    for tangent in SPEC.spine_axis_tangent_offsets_mm:
        axes.append((SPEC.spine_angle_deg, SPEC.spine_center_radius_mm, tangent, "spine"))
    rows = []
    for angle, radius, tangent, role in axes:
        screw = m3_screw_shape(angle, radius, tangent)
        screw.label = f"{NAMESPACE}_{role}_M3x8_A{angle:03.0f}_R{radius:.0f}_T{tangent:+.0f}"
        nut = m3_nut_shape(angle, radius, tangent, -30.0 if role == "motor" else 0.0)
        nut.label = f"{NAMESPACE}_{role}_M3_nut_A{angle:03.0f}_R{radius:.0f}_T{tangent:+.0f}"
        rows.extend((screw, nut))
    return tuple(rows)


def assembled_printed_shape():
    children = [named_quadrant(i) for i in range(1, 5)]
    children.extend((motor_sled_shape(), fixed_riser_shape(60.0), spine_riser_shape()))
    return Compound(children=children, label=f"{NAMESPACE}_seven_printed_objects")


def assembled_test_rig_shape():
    children = [deepcopy(child) for child in assembled_printed_shape().children]
    children.extend(deepcopy(row["shape"]) for row in r4.hardware_occurrences())
    children.extend(installed_mount_hardware())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_MVP_test_rig")


def service_exploded_shape():
    children = []
    for i in range(1, 5):
        angle = r4.SPEC.seam_angles_deg[i - 1] + 45.0
        dx, dy = local_point(angle, SPEC.exploded_radial_mm, 0.0)
        q = named_quadrant(i).moved(Location((dx, dy, 0.0)))
        q.label = named_quadrant(i).label
        children.append(q)
    for index, part in enumerate((motor_sled_shape(), fixed_riser_shape(60.0), spine_riser_shape())):
        moved = part.moved(Location((0.0, 0.0, SPEC.exploded_component_z_mm + index * 18.0)))
        moved.label = part.label
        children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded")


def printable_occurrences() -> tuple[dict[str, object], ...]:
    source = [
        *(named_quadrant(i) for i in range(1, 5)),
        motor_sled_shape(),
        fixed_riser_shape(0.0),
        spine_riser_shape(),
    ]
    names = (
        "quadrant_Q1", "quadrant_Q2", "quadrant_Q3", "quadrant_Q4",
        "reusable_motor_sled", "reusable_fixed_riser", "spine_riser",
    )
    rows = []
    for name, shape in zip(names, source):
        min_z = float(shape.bounding_box().min.Z)
        printable = shape.moved(Location((0.0, 0.0, -min_z)))
        printable.label = f"{NAMESPACE}_{name}_print_orientation"
        rows.append({
            "name": name,
            "label": printable.label,
            "orientation": "minimum_z_on_bed",
            "shape": printable,
        })
    return tuple(rows)


def modification_mask_shape():
    children = [deepcopy(tool) for tool in (*r4.motor_slot_tools(), *r4.spine_mount_tools())]
    for angle in SPEC.motor_station_angles_deg:
        for radius in SPEC.motor_axis_radii_mm:
            for tangent in SPEC.motor_tangent_offsets_mm:
                children.append(_motor_rail_features(angle, radius, tangent)[5])
    for angle in SPEC.fixed_angles_deg:
        children.append(_static_rail_features(angle, SPEC.fixed_center_radius_mm, SPEC.fixed_rail_tangential_length_mm)[5])
    children.append(_static_rail_features(
        SPEC.spine_angle_deg, SPEC.spine_center_radius_mm, SPEC.spine_foot_tangential_length_mm
    )[5])
    return Compound(children=children, label=f"{NAMESPACE}_explicit_localized_change_masks")


def ring_keepout_witness():
    outer = Cylinder(
        SPEC.ring_tooth_tip_radius_mm + 0.02,
        SPEC.driver_path_height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.receiver_roof_top_z_mm)))
    inner = Cylinder(
        SPEC.ring_tooth_tip_radius_mm,
        SPEC.driver_path_height_mm + 0.04,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.receiver_roof_top_z_mm - 0.02)))
    return outer.cut(inner)


def driver_path(angle: float, radius: float, tangent: float):
    return vertical_cylinder(
        angle, radius, tangent, SPEC.driver_path_diameter_mm,
        SPEC.screw_under_head_z_mm,
        SPEC.driver_path_height_mm,
    )
