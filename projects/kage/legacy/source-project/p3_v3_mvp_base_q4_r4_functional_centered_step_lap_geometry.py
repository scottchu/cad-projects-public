"""Source-owned actual BREP geometry for the Q4-R4 functional MVP chassis."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude, loft

from p3_v3_mvp_base_q4_r4_functional_centered_step_lap_spec import NAMESPACE, SPEC


# seam name, angle, upper owner, lower owner
LAPS = (
    ("S12", 135.0, 1, 2),
    ("S23", 225.0, 2, 3),
    ("S34", 315.0, 3, 4),
    ("S41", 45.0, 1, 4),
)


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
    angle = radians(angle_deg)
    return (
        radius_mm * cos(angle) - tangent_mm * sin(angle),
        radius_mm * sin(angle) + tangent_mm * cos(angle),
    )


def _local_box(
    angle_deg: float,
    radial_min_mm: float,
    radial_max_mm: float,
    tangent_min_mm: float,
    tangent_max_mm: float,
    z0_mm: float,
    height_mm: float,
):
    return Box(
        radial_max_mm - radial_min_mm,
        tangent_max_mm - tangent_min_mm,
        height_mm,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((radial_min_mm, tangent_min_mm, z0_mm))).rotate(Axis.Z, angle_deg)


def vertical_cylinder(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    diameter_mm: float,
    z0_mm: float,
    height_mm: float,
):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    return Cylinder(
        diameter_mm / 2.0,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0_mm)))


def _hex_wire(
    radius_mm: float,
    tangent_mm: float,
    across_flats_mm: float,
    z_mm: float = 0.0,
):
    circumradius = across_flats_mm / (2.0 * cos(radians(30.0)))
    points = tuple(
        (
            radius_mm + circumradius * cos(radians(30.0 + 60.0 * vertex)),
            tangent_mm + circumradius * sin(radians(30.0 + 60.0 * vertex)),
        )
        for vertex in range(6)
    )
    return Polygon(*points).moved(Location((0.0, 0.0, z_mm)))


def _hex_prism(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    across_flats_mm: float,
    z0_mm: float,
    height_mm: float,
):
    return extrude(
        _hex_wire(radius_mm, tangent_mm, across_flats_mm), amount=height_mm
    ).moved(Location((0.0, 0.0, z0_mm))).rotate(Axis.Z, angle_deg)


def full_annulus_shape():
    outer = Cylinder(
        SPEC.base_outer_radius_mm,
        SPEC.plate_nominal_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm)))
    inner = Cylinder(
        SPEC.base_inner_radius_mm,
        SPEC.plate_nominal_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm)))
    return _single_solid(outer.cut(inner), f"{NAMESPACE}_source_annulus")


def _quadrant_mask(index: int):
    if index not in range(1, 5):
        raise ValueError("quadrant index must be 1..4")
    angle = SPEC.seam_angles_deg[index - 1]
    span = SPEC.base_outer_radius_mm + SPEC.boolean_overshoot_mm
    height = SPEC.plate_nominal_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm
    return Box(span, span, height, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((
            SPEC.seam_relief_per_face_mm,
            SPEC.seam_relief_per_face_mm,
            SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm,
        ))
    ).rotate(Axis.Z, angle)


def plain_quadrant_shapes() -> tuple:
    annulus = full_annulus_shape()
    return tuple(
        _single_solid(
            deepcopy(annulus).intersect(_quadrant_mask(index)),
            f"{NAMESPACE}_quadrant_Q{index}_plain",
        )
        for index in range(1, 5)
    )


def donor_plan_tool(angle_deg: float, z0_mm: float, height_mm: float):
    return _local_box(
        angle_deg,
        SPEC.lap_r_min_mm,
        SPEC.lap_r_max_mm,
        SPEC.donor_t_min_mm,
        SPEC.donor_t_max_mm,
        z0_mm,
        height_mm,
    )


def receiver_plan_tool(angle_deg: float, z0_mm: float, height_mm: float):
    return _local_box(
        angle_deg,
        SPEC.receiver_r_min_mm,
        SPEC.receiver_r_max_mm,
        SPEC.receiver_t_min_mm,
        SPEC.receiver_t_max_mm,
        z0_mm,
        height_mm,
    )


def upper_donor_shape(angle_deg: float):
    return donor_plan_tool(angle_deg, SPEC.lap_split_z_mm, SPEC.upper_lap_thickness_mm)


def lower_receiver_shape(angle_deg: float):
    return receiver_plan_tool(angle_deg, SPEC.plate_bottom_z_mm, SPEC.lower_land_thickness_mm)


def receiver_lower_layer_cut_tool(angle_deg: float):
    return receiver_plan_tool(
        angle_deg,
        SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm,
        SPEC.lower_land_thickness_mm + SPEC.boolean_overshoot_mm,
    )


def receiver_upper_layer_cut_tool(angle_deg: float):
    return receiver_plan_tool(
        angle_deg,
        SPEC.lap_split_z_mm,
        SPEC.upper_lap_thickness_mm + SPEC.boolean_overshoot_mm,
    )


def radial_capsule_tool(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    width_mm: float,
    overall_length_mm: float,
    z0_mm: float,
    height_mm: float,
):
    center_spacing = overall_length_mm - width_mm
    bar = _local_box(
        angle_deg,
        radius_mm - center_spacing / 2.0,
        radius_mm + center_spacing / 2.0,
        tangent_mm - width_mm / 2.0,
        tangent_mm + width_mm / 2.0,
        z0_mm,
        height_mm,
    )
    ends = tuple(
        vertical_cylinder(
            angle_deg,
            radius_mm + radial_offset,
            tangent_mm,
            width_mm,
            z0_mm,
            height_mm,
        )
        for radial_offset in (-center_spacing / 2.0, center_spacing / 2.0)
    )
    return _single_solid(bar.fuse(*ends), f"{NAMESPACE}_radial_capsule_tool")


def motor_slot_tools() -> tuple:
    z0 = SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm
    height = SPEC.plate_nominal_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm
    return tuple(
        radial_capsule_tool(
            angle,
            radius,
            tangent,
            SPEC.motor_slot_width_mm,
            SPEC.motor_slot_overall_length_mm,
            z0,
            height,
        )
        for angle in SPEC.motor_station_angles_deg
        for radius in SPEC.motor_slot_axis_radii_mm
        for tangent in SPEC.motor_slot_tangent_offsets_mm
    )


def spine_mount_tools() -> tuple:
    return tuple(
        vertical_cylinder(
            SPEC.spine_angle_deg,
            SPEC.spine_center_radius_mm,
            tangent,
            SPEC.spine_mount_path_diameter_mm,
            SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm,
            SPEC.plate_nominal_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        )
        for tangent in SPEC.spine_mount_tangent_offsets_mm
    )


def bearing_boss_shape(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    return vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.bearing_boss_diameter_mm,
        SPEC.plate_top_z_mm,
        SPEC.bearing_boss_height_mm,
    )


def upper_clearance_tool(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    return vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.upper_clearance_hole_diameter_mm,
        SPEC.lap_split_z_mm - SPEC.boolean_overshoot_mm,
        SPEC.upper_lap_thickness_mm + SPEC.bearing_boss_height_mm + 2.0 * SPEC.boolean_overshoot_mm,
    )


def nut_trap_tool(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    # The AF5.8 cavity receives a true 0.30 x 45 degree hexagonal entry lead:
    # every side grows 0.30 mm from the lower section to the split-plane mouth.
    nominal = _hex_prism(
        angle,
        radius_mm,
        0.0,
        SPEC.nut_trap_af_mm,
        SPEC.nut_trap_bottom_z_mm,
        SPEC.nut_trap_depth_mm - SPEC.nut_trap_entry_chamfer_mm,
    )
    entry_chamfer = loft((
        _hex_wire(
            radius_mm,
            0.0,
            SPEC.nut_trap_af_mm,
            SPEC.lap_split_z_mm - SPEC.nut_trap_entry_chamfer_mm,
        ),
        _hex_wire(
            radius_mm,
            0.0,
            SPEC.nut_trap_af_mm + 2.0 * SPEC.nut_trap_entry_chamfer_mm,
            SPEC.lap_split_z_mm,
        ),
    )).rotate(Axis.Z, angle)
    entry_cap = _hex_prism(
        angle,
        radius_mm,
        0.0,
        SPEC.nut_trap_af_mm + 2.0 * SPEC.nut_trap_entry_chamfer_mm,
        SPEC.lap_split_z_mm,
        0.01,
    )
    return nominal.fuse(entry_chamfer, entry_cap)


def tip_relief_tool(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    return vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.tip_relief_diameter_mm,
        SPEC.tip_relief_bottom_z_mm,
        SPEC.tip_relief_depth_mm + SPEC.boolean_overshoot_mm,
    )


@lru_cache(maxsize=1)
def quadrant_shapes() -> tuple:
    quadrants = [deepcopy(shape) for shape in plain_quadrant_shapes()]

    # Remove only the opposing half-layer from each owner, then span the seam
    # with the complementary donor/receiver.  Keeping the owner's own half-
    # layer provides a continuous structural root while the 0.20 mm expanded
    # receiver plan clears the cross-seam donor on the mating side.
    for seam_name, angle, upper_index, lower_index in LAPS:
        quadrants[upper_index - 1] = _single_solid(
            quadrants[upper_index - 1]
            .cut(receiver_lower_layer_cut_tool(angle))
            .fuse(upper_donor_shape(angle)),
            f"{NAMESPACE}_quadrant_Q{upper_index}_{seam_name}_upper",
        )
        quadrants[lower_index - 1] = _single_solid(
            quadrants[lower_index - 1]
            .cut(receiver_upper_layer_cut_tool(angle))
            .fuse(lower_receiver_shape(angle)),
            f"{NAMESPACE}_quadrant_Q{lower_index}_{seam_name}_lower",
        )

    functional_cuts = (*motor_slot_tools(), *spine_mount_tools())
    for index in range(4):
        quadrants[index] = _single_solid(
            quadrants[index].cut(*(deepcopy(tool) for tool in functional_cuts)),
            f"{NAMESPACE}_quadrant_Q{index + 1}_functional",
        )

    for lap_index, (_, _, upper_index, lower_index) in enumerate(LAPS):
        for radius in SPEC.seam_screw_axis_radii_mm:
            quadrants[upper_index - 1] = _single_solid(
                quadrants[upper_index - 1]
                .fuse(bearing_boss_shape(lap_index, radius))
                .cut(upper_clearance_tool(lap_index, radius)),
                f"{NAMESPACE}_quadrant_Q{upper_index}_bossed",
            )
            quadrants[lower_index - 1] = _single_solid(
                quadrants[lower_index - 1].cut(
                    nut_trap_tool(lap_index, radius),
                    tip_relief_tool(lap_index, radius),
                ),
                f"{NAMESPACE}_quadrant_Q{lower_index}_trapped",
            )

    roles = {
        1: "two_upper",
        2: "upper_lower",
        3: "upper_lower",
        4: "two_lower",
    }
    for index, shape in enumerate(quadrants, 1):
        shape.label = f"{NAMESPACE}_quadrant_Q{index}_{roles[index]}"
    return tuple(quadrants)


def named_quadrant(index: int):
    if index not in range(1, 5):
        raise ValueError("quadrant index must be 1..4")
    return deepcopy(quadrant_shapes()[index - 1])


def assembled_printed_shape():
    return Compound(
        children=[named_quadrant(index) for index in range(1, 5)],
        label=f"{NAMESPACE}_four_part_functional_base",
    )


def nominal_screw_shaft_shape(lap_index: int, radius_mm: float, length_mm: float | None = None):
    length = SPEC.m3_screw_length_mm if length_mm is None else length_mm
    _, angle, _, _ = LAPS[lap_index]
    return vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.m3_screw_nominal_diameter_mm,
        SPEC.screw_under_head_z_mm - length,
        length,
    )


def nominal_screw_shape(lap_index: int, radius_mm: float):
    shaft = nominal_screw_shaft_shape(lap_index, radius_mm)
    _, angle, _, _ = LAPS[lap_index]
    head = vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.m3_socket_head_max_diameter_mm,
        SPEC.screw_under_head_z_mm,
        SPEC.m3_socket_head_height_mm,
    )
    return _single_solid(shaft.fuse(head), f"{NAMESPACE}_ISO4762_M3x6")


def nominal_nut_shape(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    return _single_solid(
        _hex_prism(
            angle,
            radius_mm,
            0.0,
            SPEC.m3_nut_max_af_mm,
            SPEC.nut_trap_bottom_z_mm,
            SPEC.m3_nut_max_thickness_mm,
        ),
        f"{NAMESPACE}_ISO4032_M3_nut",
    )


def driver_path_shape(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    return vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.driver_path_diameter_mm,
        SPEC.screw_under_head_z_mm,
        SPEC.driver_path_length_mm,
    )


def nut_insertion_path_shape(lap_index: int, radius_mm: float):
    _, angle, _, _ = LAPS[lap_index]
    return _hex_prism(
        angle,
        radius_mm,
        0.0,
        SPEC.nut_trap_af_mm,
        SPEC.lap_split_z_mm,
        SPEC.driver_path_length_mm,
    )


def hardware_occurrences() -> tuple[dict[str, object], ...]:
    rows = []
    for lap_index, (seam_name, _, _, _) in enumerate(LAPS):
        for position, radius in zip(("inner", "outer"), SPEC.seam_screw_axis_radii_mm):
            screw = nominal_screw_shape(lap_index, radius)
            screw.label = f"{NAMESPACE}_M3x6_{seam_name}_{position}"
            nut = nominal_nut_shape(lap_index, radius)
            nut.label = f"{NAMESPACE}_M3_nut_{seam_name}_{position}"
            rows.extend((
                {"kind": "screw", "lap_index": lap_index, "seam": seam_name, "position": position, "radius_mm": radius, "shape": screw},
                {"kind": "nut", "lap_index": lap_index, "seam": seam_name, "position": position, "radius_mm": radius, "shape": nut},
            ))
    return tuple(rows)


def assembled_shape():
    children = [named_quadrant(index) for index in range(1, 5)]
    children.extend(deepcopy(row["shape"]) for row in hardware_occurrences())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_with_hardware")


def service_exploded_shape():
    children = []
    for index in range(1, 5):
        center_angle = SPEC.seam_angles_deg[index - 1] + 45.0
        dx, dy = local_point(center_angle, SPEC.exploded_quadrant_radial_mm, 0.0)
        moved = named_quadrant(index).moved(Location((dx, dy, 0.0)))
        moved.label = named_quadrant(index).label
        children.append(moved)
    for row in hardware_occurrences():
        dz = SPEC.exploded_hardware_z_mm if row["kind"] == "screw" else SPEC.exploded_hardware_z_mm / 2.0
        moved = deepcopy(row["shape"]).moved(Location((0.0, 0.0, dz)))
        moved.label = row["shape"].label
        children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded")


def printable_quadrant_shape(index: int):
    shape = named_quadrant(index).moved(Location((0.0, 0.0, -SPEC.plate_bottom_z_mm)))
    shape.label = f"{NAMESPACE}_quadrant_Q{index}_underside_down"
    return shape


def printable_occurrences() -> tuple[dict[str, object], ...]:
    roles = ("two_upper", "upper_lower", "upper_lower", "two_lower")
    return tuple(
        {
            "name": f"quadrant_Q{index}",
            "kind": roles[index - 1],
            "orientation": "underside_down",
            "label": f"{NAMESPACE}_quadrant_Q{index}_underside_down",
            "shape": printable_quadrant_shape(index),
        }
        for index in range(1, 5)
    )


def fixed_tower_landing_volume(angle_deg: float):
    return _local_box(
        angle_deg,
        SPEC.fixed_tower_center_radius_mm - SPEC.fixed_tower_landing_radial_mm / 2.0,
        SPEC.fixed_tower_center_radius_mm + SPEC.fixed_tower_landing_radial_mm / 2.0,
        -SPEC.fixed_tower_landing_tangential_mm / 2.0,
        SPEC.fixed_tower_landing_tangential_mm / 2.0,
        SPEC.plate_bottom_z_mm,
        SPEC.plate_nominal_thickness_mm,
    )


def spine_landing_volume():
    return _local_box(
        SPEC.spine_angle_deg,
        SPEC.spine_center_radius_mm - SPEC.spine_foot_radial_mm / 2.0,
        SPEC.spine_center_radius_mm + SPEC.spine_foot_radial_mm / 2.0,
        -SPEC.spine_foot_tangential_mm / 2.0,
        SPEC.spine_foot_tangential_mm / 2.0,
        SPEC.plate_bottom_z_mm,
        SPEC.plate_nominal_thickness_mm,
    )


def seam_feature_envelope():
    children = []
    for lap_index, (_, angle, _, _) in enumerate(LAPS):
        children.extend((upper_donor_shape(angle), lower_receiver_shape(angle)))
        for radius in SPEC.seam_screw_axis_radii_mm:
            children.extend((
                bearing_boss_shape(lap_index, radius),
                nominal_screw_shape(lap_index, radius),
                nominal_nut_shape(lap_index, radius),
                driver_path_shape(lap_index, radius),
            ))
    return Compound(children=children, label=f"{NAMESPACE}_seam_feature_envelope")


def ring_motion_plan_keepout():
    outer = Cylinder(
        SPEC.fin_outer_radius_mm,
        SPEC.driver_path_length_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm)))
    inner = Cylinder(
        SPEC.tooth_tip_radius_mm,
        SPEC.driver_path_length_mm + 2.0 * SPEC.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm)))
    return outer.cut(inner)


def hall_keepout_shapes() -> tuple:
    magnet_rows = tuple(
        vertical_cylinder(
            SPEC.hall_module_angle_deg,
            SPEC.hall_magnet_radius_mm,
            0.0,
            SPEC.hall_magnet_pocket_diameter_mm + 2.0 * SPEC.hall_mechanical_clearance_mm,
            SPEC.plate_top_z_mm,
            SPEC.hall_magnet_pocket_depth_mm,
        ).moved(Location((0.0, 0.0, role * 6.7)))
        for role in range(SPEC.hall_magnet_count)
    )
    radial, tangent, height = SPEC.hall_module_envelope_mm
    shell = SPEC.hall_connector_service_shell_mm + SPEC.hall_mechanical_clearance_mm
    sensor = _local_box(
        SPEC.hall_module_angle_deg,
        SPEC.hall_magnet_radius_mm - radial / 2.0 - shell,
        SPEC.hall_magnet_radius_mm + radial / 2.0 + shell,
        -tangent / 2.0 - shell,
        tangent / 2.0 + SPEC.hall_wire_bend_zone_mm + shell,
        SPEC.plate_top_z_mm,
        height + 2.0 * shell,
    )
    return (*magnet_rows, sensor)


def locked_motor_service_shapes(q_mm: float) -> tuple:
    """Return actual Revision-K yoke/gear station solids at one service q."""

    import p3_v3_direct_gear_race_guidance_r2_geometry as locked

    children = []
    for role in range(3):
        station = locked.make_motor_station_at_pose(role=role, motor_q_mm=q_mm, ring_angle_deg=0.0)
        children.append(locked._make_motor_yoke(role, q_mm))
        children.extend(station.values())
    return tuple(children)


def locked_tower_service_shapes() -> tuple:
    """Return the actual Revision-K fixed leaves and distinct 300 degree spine."""

    import p3_v3_direct_gear_race_guidance_r2_geometry as locked

    leaves = tuple(
        locked._local_box(12.0, 18.0, 3.0, 118.0, angle, -5.20)
        for angle in SPEC.fixed_tower_angles_deg
    )
    return (*leaves, locked._spine_shape())
