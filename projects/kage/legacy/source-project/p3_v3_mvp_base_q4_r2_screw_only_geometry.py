"""Actual BREP geometry for the KAGE B0 Q4-R2 screw-only base."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin
from typing import Iterable

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Location, Polygon, ShapeList, extrude

import p3_v3_mvp_base_q4_r1_geometry as locked_geometry
from p3_v3_mvp_base_q4_r2_screw_only_spec import NAMESPACE, SPEC, ScrewOnlyBaseSpec


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
    return Cylinder(diameter_mm / 2.0, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, y, z0_mm))
    )


def _local_cylinder(x_mm: float, y_mm: float, diameter_mm: float, z0_mm: float, height_mm: float):
    return Cylinder(diameter_mm / 2.0, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x_mm, y_mm, z0_mm))
    )


def _hex_prism(af_mm: float, z0_mm: float, height_mm: float, center_y_mm: float):
    radius = af_mm / (2.0 * cos(radians(30.0)))
    points = tuple(
        (radius * cos(radians(60.0 * vertex)), center_y_mm + radius * sin(radians(60.0 * vertex)))
        for vertex in range(6)
    )
    return extrude(Polygon(*points), amount=height_mm).moved(Location((0.0, 0.0, z0_mm)))


@lru_cache(maxsize=1)
def locked_quadrant_shapes() -> tuple:
    """Return untouched Q4-R1 quadrant BREPs as the successor's locked input."""

    return locked_geometry.quadrant_shapes()


@lru_cache(maxsize=1)
def quadrant_shapes() -> tuple:
    return locked_quadrant_shapes()


def _named_quadrant_copy(index: int):
    shape = deepcopy(quadrant_shapes()[index - 1])
    shape.label = f"{NAMESPACE}_quadrant_Q{index}"
    return shape


def round_receiver_tool(angle_deg: float):
    return deepcopy(locked_geometry.round_split_slip_tool(angle_deg))


def relieved_receiver_tool(angle_deg: float):
    return deepcopy(locked_geometry.relieved_split_slip_tool(angle_deg))


def _local_integral_boss(radial_offset_mm: float, z0_mm: float, spec: ScrewOnlyBaseSpec = SPEC):
    cylindrical_height = spec.integral_boss_height_mm - spec.integral_boss_tip_chamfer_mm
    cylinder = _local_cylinder(
        radial_offset_mm,
        0.0,
        spec.integral_boss_diameter_mm,
        z0_mm,
        cylindrical_height,
    )
    tip = Cone(
        spec.integral_boss_diameter_mm / 2.0,
        spec.integral_boss_diameter_mm / 2.0 - spec.integral_boss_tip_chamfer_mm,
        spec.integral_boss_tip_chamfer_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((radial_offset_mm, 0.0, z0_mm + cylindrical_height)))
    return single_solid(cylinder.fuse(tip), f"{NAMESPACE}_integral_registration_boss")


@lru_cache(maxsize=1)
def clamp_print_shape(spec: ScrewOnlyBaseSpec = SPEC):
    """One one-solid clamp, bottom at Z=0, with bosses/openings facing +Z."""

    clamp = Box(
        spec.clamp_radial_mm,
        spec.clamp_tangential_mm,
        spec.clamp_body_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    pocket_height = spec.nut_pocket_depth_mm + spec.boolean_overshoot_mm
    tip_height = spec.screw_tip_relief_depth_mm + spec.boolean_overshoot_mm
    cut_tools = []
    for tangent in spec.screw_tangent_offsets_mm:
        cut_tools.extend(
            (
                _hex_prism(
                    spec.nut_pocket_af_mm,
                    spec.nut_pocket_floor_from_clamp_bottom_mm,
                    pocket_height,
                    tangent,
                ),
                _local_cylinder(
                    0.0,
                    tangent,
                    spec.screw_tip_relief_diameter_mm,
                    spec.tip_relief_floor_from_clamp_bottom_mm,
                    tip_height,
                ),
            )
        )
    clamp = single_solid(clamp.cut(*cut_tools), f"{NAMESPACE}_clamp_cut")
    bosses = tuple(
        _local_integral_boss(offset, spec.clamp_body_thickness_mm, spec)
        for offset in spec.boss_local_radial_offsets_mm
    )
    clamp = single_solid(clamp.fuse(*bosses), f"{NAMESPACE}_clamp_print")
    clamp.label = f"{NAMESPACE}_clamp_print"
    return clamp


def clamp_assembly_shape(seam_index: int, spec: ScrewOnlyBaseSpec = SPEC):
    if seam_index not in range(1, spec.clamp_count_total + 1):
        raise ValueError(f"clamp index outside 1..{spec.clamp_count_total}: {seam_index}")
    angle = spec.seam_angles_deg[seam_index - 1]
    x, y = local_point(angle, spec.clamp_center_radius_mm, 0.0)
    shape = deepcopy(clamp_print_shape()).rotate(Axis.Z, angle).moved(
        Location((x, y, -spec.clamp_body_thickness_mm))
    )
    shape.label = f"{NAMESPACE}_clamp_C{seam_index}"
    return shape


@lru_cache(maxsize=1)
def clamp_assembly_shapes() -> tuple:
    return tuple(clamp_assembly_shape(index) for index in range(1, SPEC.clamp_count_total + 1))


def integral_boss_assembly_shape(seam_index: int, radius_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    local_offset = radius_mm - SPEC.clamp_center_radius_mm
    local = _local_integral_boss(local_offset, 0.0)
    x, y = local_point(angle, SPEC.clamp_center_radius_mm, 0.0)
    shape = local.rotate(Axis.Z, angle).moved(Location((x, y, 0.0)))
    shape.label = f"{NAMESPACE}_boss_C{seam_index}_R{int(radius_mm)}"
    return shape


def nominal_screw_shaft_shape(seam_index: int, tangent_mm: float, length_mm: float = 6.0):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    return vertical_cylinder(
        angle,
        SPEC.screw_axis_radius_mm,
        tangent_mm,
        SPEC.m3_screw_nominal_diameter_mm,
        SPEC.base_thickness_mm - length_mm,
        length_mm,
    )


def nominal_screw_shape(seam_index: int, tangent_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    shaft = nominal_screw_shaft_shape(seam_index, tangent_mm, SPEC.m3_screw_length_mm)
    head = vertical_cylinder(
        angle,
        SPEC.screw_axis_radius_mm,
        tangent_mm,
        SPEC.m3_socket_head_max_diameter_mm,
        SPEC.base_thickness_mm,
        SPEC.m3_socket_head_nominal_height_mm,
    )
    shape = single_solid(shaft.fuse(head), f"{NAMESPACE}_m3x6_socket_head")
    return shape


def nominal_nut_shape(seam_index: int, tangent_mm: float):
    angle = SPEC.seam_angles_deg[seam_index - 1]
    local = _hex_prism(
        SPEC.m3_hex_nut_nominal_af_mm,
        0.0,
        SPEC.m3_hex_nut_max_thickness_mm,
        tangent_mm,
    )
    x, y = local_point(angle, SPEC.screw_axis_radius_mm, 0.0)
    shape = local.rotate(Axis.Z, angle).moved(Location((x, y, -SPEC.nut_pocket_depth_mm)))
    return single_solid(shape, f"{NAMESPACE}_m3_hex_nut")


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


def hardware_occurrences() -> tuple[dict[str, object], ...]:
    rows = []
    for seam_index in range(1, SPEC.clamp_count_total + 1):
        for side, tangent in zip(("left", "right"), SPEC.screw_tangent_offsets_mm):
            screw = nominal_screw_shape(seam_index, tangent)
            screw.label = f"{NAMESPACE}_m3x6_C{seam_index}_{side}"
            nut = nominal_nut_shape(seam_index, tangent)
            nut.label = f"{NAMESPACE}_m3_nut_C{seam_index}_{side}"
            rows.extend(
                (
                    {"kind": "screw", "seam_index": seam_index, "side": side, "shape": screw},
                    {"kind": "nut", "seam_index": seam_index, "side": side, "shape": nut},
                )
            )
    return tuple(rows)


def assembled_base_shape():
    return Compound(
        children=[_named_quadrant_copy(index) for index in range(1, SPEC.quadrant_count + 1)],
        label=f"{NAMESPACE}_base_plate_assembled",
    )


def assembled_printed_shape():
    return Compound(
        children=[
            *(_named_quadrant_copy(index) for index in range(1, SPEC.quadrant_count + 1)),
            *(deepcopy(shape) for shape in clamp_assembly_shapes()),
        ],
        label=f"{NAMESPACE}_printed_assembly",
    )


def assembled_shape():
    children = [_named_quadrant_copy(index) for index in range(1, SPEC.quadrant_count + 1)]
    children.extend(deepcopy(shape) for shape in clamp_assembly_shapes())
    children.extend(deepcopy(row["shape"]) for row in hardware_occurrences())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_with_hardware")


def service_exploded_shape():
    children = []
    for index, quadrant in enumerate(quadrant_shapes()):
        center_angle = SPEC.seam_angles_deg[index] + SPEC.quadrant_angle_deg / 2.0
        dx, dy = local_point(center_angle, SPEC.exploded_quadrant_radial_mm, 0.0)
        moved = deepcopy(quadrant).moved(Location((dx, dy, 0.0)))
        moved.label = f"{NAMESPACE}_quadrant_Q{index + 1}"
        children.append(moved)
    for clamp in clamp_assembly_shapes():
        moved = deepcopy(clamp).moved(Location((0.0, 0.0, -SPEC.exploded_clamp_drop_mm)))
        moved.label = clamp.label
        children.append(moved)
    for row in hardware_occurrences():
        z_shift = SPEC.exploded_hardware_lift_mm if row["kind"] == "screw" else -SPEC.exploded_clamp_drop_mm
        moved = deepcopy(row["shape"]).moved(Location((0.0, 0.0, z_shift)))
        moved.label = row["shape"].label
        children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded")


def printable_quadrant_shape(index: int):
    source = deepcopy(quadrant_shapes()[index - 1])
    shape = source.rotate(Axis.X, SPEC.quadrant_print_flip_deg).moved(Location((0.0, 0.0, SPEC.base_thickness_mm)))
    shape.label = f"{NAMESPACE}_quadrant_Q{index}_front_down"
    return shape


def printable_clamp_shape(index: int):
    shape = deepcopy(clamp_print_shape())
    shape.label = f"{NAMESPACE}_clamp_C{index}_bottom_down"
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
            "name": f"clamp_C{index}",
            "label": f"{NAMESPACE}_clamp_C{index}_bottom_down",
            "kind": "clamp",
            "shape": printable_clamp_shape(index),
        }
        for index in range(1, SPEC.clamp_count_total + 1)
    )
    return tuple(rows)
