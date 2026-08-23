"""Actual BREP geometry for the isolated KAGE B0 four-to-one base MVP."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin
from typing import Iterable

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cylinder,
    Location,
    Polygon,
    ShapeList,
    Vector,
    extrude,
)

from p3_v3_mvp_base_q4_r1_spec import NAMESPACE, SPEC, BaseMvpSpec


def _solids(shape) -> list:
    if shape is None:
        return []
    roots: Iterable = shape if isinstance(shape, (list, tuple, ShapeList)) else (shape,)
    return [solid for root in roots for solid in root.solids()]


def single_solid(shape, label: str):
    solids = _solids(shape)
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    result.label = label
    return result


def volume_mm3(shape) -> float:
    return float(sum(solid.volume for solid in _solids(shape)))


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


@lru_cache(maxsize=1)
def full_annulus(spec: BaseMvpSpec = SPEC):
    """One source-owned R150/R66 annulus before any segmentation or joinery."""

    outer = Cylinder(
        spec.base_outer_radius_mm,
        spec.base_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    inner_tool = Cylinder(
        spec.base_inner_radius_mm,
        spec.base_thickness_mm + 2.0 * spec.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, -spec.boolean_overshoot_mm)))
    return single_solid(outer.cut(inner_tool), f"{NAMESPACE}_source_full_annulus_R150_R66")


def relieved_quadrant_mask(index: int, spec: BaseMvpSpec = SPEC):
    """Quarter-plane mask with both seam faces shifted inward by 0.05 mm.

    Before rotation the sector occupies local +X/+Y.  Moving the box minimum
    to (+relief,+relief) offsets each opposed radial seam face by the exact
    normal relief, producing a 0.10 mm gap against its neighbour.
    """

    if index not in range(1, spec.quadrant_count + 1):
        raise ValueError(f"quadrant index outside 1..{spec.quadrant_count}: {index}")
    angle = spec.seam_angles_deg[index - 1]
    height = spec.base_thickness_mm + 2.0 * spec.boolean_overshoot_mm
    mask = Box(
        spec.sector_mask_radius_mm,
        spec.sector_mask_radius_mm,
        height,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(
        Location(
            (
                spec.seam_relief_per_face_mm,
                spec.seam_relief_per_face_mm,
                -spec.boolean_overshoot_mm,
            )
        )
    )
    return mask.rotate(Axis.Z, angle)


def round_split_slip_tool(angle_deg: float, spec: BaseMvpSpec = SPEC):
    return vertical_cylinder(
        angle_deg,
        spec.round_dowel_axis_radius_mm,
        0.0,
        spec.base_split_slip_bore_diameter_mm,
        -spec.boolean_overshoot_mm,
        spec.base_thickness_mm + 2.0 * spec.boolean_overshoot_mm,
    )


def relieved_split_slip_tool(angle_deg: float, spec: BaseMvpSpec = SPEC):
    endpoint_cylinders = [
        vertical_cylinder(
            angle_deg,
            spec.relief_dowel_axis_radius_mm + radial_offset,
            0.0,
            spec.relief_split_slot_tangential_mm,
            -spec.boolean_overshoot_mm,
            spec.base_thickness_mm + 2.0 * spec.boolean_overshoot_mm,
        )
        for radial_offset in spec.relief_slot_center_offsets_mm
    ]
    center_x, center_y = local_point(angle_deg, spec.relief_dowel_axis_radius_mm, 0.0)
    center_bar = Box(
        spec.relief_slot_center_spacing_mm,
        spec.relief_split_slot_tangential_mm,
        spec.base_thickness_mm + 2.0 * spec.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.Z, angle_deg).moved(
        Location((center_x, center_y, -spec.boolean_overshoot_mm))
    )
    return single_solid(
        endpoint_cylinders[0].fuse(center_bar, endpoint_cylinders[1]),
        f"{NAMESPACE}_radial_relief_D4p15_L5p15_true_capsule_tool",
    )


def base_joinery_tools(spec: BaseMvpSpec = SPEC) -> tuple:
    tools = []
    for angle in spec.seam_angles_deg:
        tools.extend(
            vertical_cylinder(
                angle,
                spec.screw_axis_radius_mm,
                tangent,
                spec.base_screw_clearance_diameter_mm,
                -spec.boolean_overshoot_mm,
                spec.base_thickness_mm + 2.0 * spec.boolean_overshoot_mm,
            )
            for tangent in spec.screw_tangent_offsets_mm
        )
        tools.append(round_split_slip_tool(angle, spec))
        tools.append(relieved_split_slip_tool(angle, spec))
    return tuple(tools)


@lru_cache(maxsize=1)
def plain_quadrant_shapes() -> tuple:
    annulus = full_annulus()
    return tuple(
        single_solid(
            deepcopy(annulus).intersect(relieved_quadrant_mask(index)),
            f"{NAMESPACE}_quadrant_Q{index}_plain",
        )
        for index in range(1, SPEC.quadrant_count + 1)
    )


@lru_cache(maxsize=1)
def quadrant_shapes() -> tuple:
    tools = base_joinery_tools()
    result = []
    for index, plain in enumerate(plain_quadrant_shapes(), start=1):
        cut = deepcopy(plain)
        for tool in tools:
            candidate = cut.cut(deepcopy(tool))
            if candidate is not None:
                cut = single_solid(candidate, f"{NAMESPACE}_quadrant_Q{index}")
        cut.label = f"{NAMESPACE}_quadrant_Q{index}"
        result.append(cut)
    return tuple(result)


def _hex_prism(af_mm: float, z0_mm: float, height_mm: float, center_y_mm: float):
    radius = af_mm / (2.0 * cos(radians(30.0)))
    points = tuple(
        (
            radius * cos(radians(60.0 * vertex)),
            center_y_mm + radius * sin(radians(60.0 * vertex)),
        )
        for vertex in range(6)
    )
    return extrude(Polygon(*points), amount=height_mm).moved(Location((0.0, 0.0, z0_mm)))


def _local_cylinder(x_mm: float, y_mm: float, diameter_mm: float, z0_mm: float, height_mm: float):
    return Cylinder(
        diameter_mm / 2.0,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x_mm, y_mm, z0_mm)))


@lru_cache(maxsize=1)
def bridge_print_shape(spec: BaseMvpSpec = SPEC):
    """One printable bridge, bottom at Z=0 and all service openings at +Z."""

    bridge = Box(
        spec.bridge_radial_mm,
        spec.bridge_tangential_mm,
        spec.bridge_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    pocket_height = spec.nut_pocket_depth_mm + spec.boolean_overshoot_mm
    tip_height = spec.screw_tip_relief_depth_mm + spec.boolean_overshoot_mm
    for tangent in spec.screw_tangent_offsets_mm:
        pocket = _hex_prism(
            spec.nut_pocket_af_mm,
            spec.nut_pocket_floor_from_bridge_bottom_mm,
            pocket_height,
            tangent,
        )
        tip = _local_cylinder(
            0.0,
            tangent,
            spec.screw_tip_relief_diameter_mm,
            spec.tip_relief_floor_from_bridge_bottom_mm,
            tip_height,
        )
        bridge = single_solid(
            bridge.cut(pocket, tip),
            f"{NAMESPACE}_bridge_print",
        )
    press_height = spec.joiner_press_engagement_mm + spec.boolean_overshoot_mm
    press_z0 = spec.bridge_thickness_mm - spec.joiner_press_engagement_mm
    for radial_offset in spec.dowel_local_radial_offsets_mm:
        bridge = single_solid(
            bridge.cut(
                _local_cylinder(
                    radial_offset,
                    0.0,
                    spec.joiner_press_bore_diameter_mm,
                    press_z0,
                    press_height,
                )
            ),
            f"{NAMESPACE}_bridge_print",
        )
    bridge.label = f"{NAMESPACE}_bridge_print"
    return bridge


def bridge_assembly_shape(seam_index: int, spec: BaseMvpSpec = SPEC):
    if seam_index not in range(1, spec.bridge_count_total + 1):
        raise ValueError(f"bridge index outside 1..{spec.bridge_count_total}: {seam_index}")
    angle = spec.seam_angles_deg[seam_index - 1]
    x, y = local_point(angle, spec.bridge_center_radius_mm, 0.0)
    shape = deepcopy(bridge_print_shape()).rotate(Axis.Z, angle).moved(
        Location((x, y, -spec.bridge_thickness_mm))
    )
    shape.label = f"{NAMESPACE}_bridge_S{seam_index}"
    return shape


@lru_cache(maxsize=1)
def bridge_assembly_shapes() -> tuple:
    return tuple(bridge_assembly_shape(index) for index in range(1, SPEC.bridge_count_total + 1))


def assembled_base_shape():
    children = [deepcopy(shape) for shape in quadrant_shapes()]
    return Compound(children=children, label=f"{NAMESPACE}_base_plate_assembled")


def assembled_shape():
    children = [deepcopy(shape) for shape in quadrant_shapes() + bridge_assembly_shapes()]
    return Compound(children=children, label=f"{NAMESPACE}_assembled")


def service_exploded_shape():
    children = []
    for index, quadrant in enumerate(quadrant_shapes()):
        center_angle = SPEC.seam_angles_deg[index] + SPEC.quadrant_angle_deg / 2.0
        dx, dy = local_point(center_angle, SPEC.exploded_quadrant_radial_mm, 0.0)
        moved = deepcopy(quadrant).moved(Location((dx, dy, 0.0)))
        moved.label = quadrant.label
        children.append(moved)
    for bridge in bridge_assembly_shapes():
        moved = deepcopy(bridge).moved(Location((0.0, 0.0, -SPEC.exploded_bridge_drop_mm)))
        moved.label = bridge.label
        children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded")


def printable_quadrant_shape(index: int):
    source = deepcopy(quadrant_shapes()[index - 1])
    shape = source.rotate(Axis.X, SPEC.quadrant_print_flip_deg).moved(
        Location((0.0, 0.0, SPEC.base_thickness_mm))
    )
    shape.label = f"{NAMESPACE}_quadrant_Q{index}_front_down"
    return shape


def printable_bridge_shape(index: int):
    shape = deepcopy(bridge_print_shape())
    shape.label = f"{NAMESPACE}_bridge_S{index}_bottom_down"
    return shape


def printable_occurrences() -> tuple[dict[str, object], ...]:
    rows = [
        {
            "name": f"quadrant_Q{index}",
            "label": f"{NAMESPACE}_quadrant_Q{index}_front_down",
            "kind": "quadrant",
            "shape": printable_quadrant_shape(index),
        }
        for index in range(1, SPEC.quadrant_count + 1)
    ]
    rows.extend(
        {
            "name": f"bridge_S{index}",
            "label": f"{NAMESPACE}_bridge_S{index}_bottom_down",
            "kind": "bridge",
            "shape": printable_bridge_shape(index),
        }
        for index in range(1, SPEC.bridge_count_total + 1)
    )
    return tuple(rows)


def nominal_dowel_shape(seam_index: int, radius_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    return vertical_cylinder(
        angle,
        radius_mm,
        0.0,
        SPEC.dowel_nominal_diameter_mm,
        -SPEC.joiner_press_engagement_mm,
        SPEC.dowel_length_mm,
    )


def nominal_screw_shaft_shape(seam_index: int, tangent_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    return vertical_cylinder(
        angle,
        SPEC.screw_axis_radius_mm,
        tangent_mm,
        SPEC.m3_screw_nominal_diameter_mm,
        SPEC.base_thickness_mm - SPEC.m3_screw_length_mm,
        SPEC.m3_screw_length_mm,
    )


def nominal_nut_shape(seam_index: int, tangent_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    local = _hex_prism(
        SPEC.m3_hex_nut_nominal_af_mm,
        0.0,
        SPEC.m3_hex_nut_max_thickness_mm,
        tangent_mm,
    )
    x, y = local_point(angle, SPEC.screw_axis_radius_mm, 0.0)
    return local.rotate(Axis.Z, angle).moved(
        Location((x, y, -SPEC.m3_hex_nut_max_thickness_mm))
    )


def driver_access_shape(seam_index: int, tangent_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    return vertical_cylinder(
        angle,
        SPEC.screw_axis_radius_mm,
        tangent_mm,
        SPEC.driver_access_diameter_mm,
        SPEC.base_thickness_mm,
        SPEC.driver_access_height_mm,
    )
