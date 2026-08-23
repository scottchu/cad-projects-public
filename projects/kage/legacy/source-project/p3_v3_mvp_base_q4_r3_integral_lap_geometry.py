"""Actual-solid alternating A/B half-lap geometry for Q4-R3."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, extrude

import p3_v3_mvp_base_q4_r1_geometry as locked_plain_geometry
from p3_v3_mvp_base_q4_r3_integral_lap_spec import NAMESPACE, SPEC


# (seam index, angle, A quadrant, B quadrant, sign of seam-local tangent into B)
SEAMS = (
    (1, 45.0, 1, 4, -1.0),
    (2, 135.0, 1, 2, +1.0),
    (3, 225.0, 3, 2, -1.0),
    (4, 315.0, 3, 4, +1.0),
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
    return volume_mm3(deepcopy(left).intersect(deepcopy(right)))


def local_point(angle_deg: float, radius_mm: float, tangent_mm: float) -> tuple[float, float]:
    a = radians(angle_deg)
    return (radius_mm * cos(a) - tangent_mm * sin(a), radius_mm * sin(a) + tangent_mm * cos(a))


def _seam_box(angle_deg: float, radial_min: float, radial_max: float, tangent_min: float,
              tangent_max: float, z0: float, height: float):
    return Box(
        radial_max - radial_min,
        tangent_max - tangent_min,
        height,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((radial_min, tangent_min, z0))).rotate(Axis.Z, angle_deg)


def tongue_tool(angle_deg: float, into_b_sign: float, include_fuse_overlap: bool = True):
    a_overlap = SPEC.tool_fuse_overlap_mm if include_fuse_overlap else 0.0
    endpoints = (into_b_sign * SPEC.tongue_overlap_depth_mm, -into_b_sign * a_overlap)
    return _seam_box(
        angle_deg, SPEC.lap_radial_min_mm, SPEC.lap_radial_max_mm,
        min(endpoints), max(endpoints), 0.0, SPEC.tongue_thickness_mm,
    )


def rebate_tool(angle_deg: float, into_b_sign: float):
    endpoints = (
        into_b_sign * SPEC.receiver_rebate_depth_mm,
        -into_b_sign * SPEC.tool_fuse_overlap_mm,
    )
    return _seam_box(
        angle_deg,
        SPEC.lap_radial_min_mm - SPEC.receiver_radial_clearance_per_side_mm,
        SPEC.lap_radial_max_mm + SPEC.receiver_radial_clearance_per_side_mm,
        min(endpoints), max(endpoints),
        -SPEC.boolean_overshoot_mm,
        SPEC.lap_interface_z_mm + SPEC.boolean_overshoot_mm,
    )


def vertical_cylinder(angle_deg: float, radius_mm: float, tangent_mm: float,
                      diameter_mm: float, z0_mm: float, height_mm: float):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    return Cylinder(diameter_mm / 2.0, height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x, y, z0_mm))
    )


@lru_cache(maxsize=1)
def quadrant_shapes() -> tuple:
    quadrants = [deepcopy(shape) for shape in locked_plain_geometry.plain_quadrant_shapes()]
    for _, angle, a_index, _, sign in SEAMS:
        quadrants[a_index - 1] = _single_solid(
            quadrants[a_index - 1].fuse(tongue_tool(angle, sign)),
            f"{NAMESPACE}_quadrant_Q{a_index}_A",
        )
    for _, angle, _, b_index, sign in SEAMS:
        quadrants[b_index - 1] = _single_solid(
            quadrants[b_index - 1].cut(rebate_tool(angle, sign)),
            f"{NAMESPACE}_quadrant_Q{b_index}_B",
        )
    for _, angle, a_index, b_index, sign in SEAMS:
        holes = tuple(
            vertical_cylinder(
                angle, radius, sign * SPEC.screw_axis_tangent_into_b_mm,
                SPEC.clearance_hole_diameter_mm, -SPEC.boolean_overshoot_mm,
                SPEC.base_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
            )
            for radius in SPEC.screw_axis_radii_mm
        )
        for index in (a_index, b_index):
            quadrants[index - 1] = _single_solid(
                quadrants[index - 1].cut(*(deepcopy(hole) for hole in holes)),
                f"{NAMESPACE}_quadrant_Q{index}_{'A' if index in SPEC.role_a_quadrants else 'B'}",
            )
    return tuple(quadrants)


def named_quadrant(index: int):
    role = "A" if index in SPEC.role_a_quadrants else "B"
    shape = deepcopy(quadrant_shapes()[index - 1])
    shape.label = f"{NAMESPACE}_quadrant_Q{index}_{role}"
    return shape


def assembled_printed_shape():
    return Compound(children=[named_quadrant(i) for i in range(1, 5)], label=f"{NAMESPACE}_four_part_base")


def _hex_prism(angle_deg: float, radius_mm: float, tangent_mm: float,
               across_flats_mm: float, z0_mm: float, height_mm: float):
    circumradius = across_flats_mm / (2.0 * cos(radians(30.0)))
    points = tuple(
        (
            radius_mm + circumradius * cos(radians(60.0 * vertex)),
            tangent_mm + circumradius * sin(radians(60.0 * vertex)),
        )
        for vertex in range(6)
    )
    return extrude(Polygon(*points), amount=height_mm).moved(Location((0.0, 0.0, z0_mm))).rotate(
        Axis.Z, angle_deg
    )


def screw_axis_tangent(seam_index: int) -> float:
    return SEAMS[seam_index - 1][4] * SPEC.screw_axis_tangent_into_b_mm


def nominal_screw_shaft_shape(seam_index: int, radius_mm: float, length_mm: float = 6.0):
    angle = SEAMS[seam_index - 1][1]
    return vertical_cylinder(
        angle,
        radius_mm,
        screw_axis_tangent(seam_index),
        SPEC.m3_screw_nominal_diameter_mm,
        SPEC.base_thickness_mm - length_mm,
        length_mm,
    )


def nominal_screw_shape(seam_index: int, radius_mm: float):
    angle = SEAMS[seam_index - 1][1]
    shaft = nominal_screw_shaft_shape(seam_index, radius_mm, SPEC.m3_screw_length_mm)
    head = vertical_cylinder(
        angle,
        radius_mm,
        screw_axis_tangent(seam_index),
        SPEC.m3_socket_head_max_diameter_mm,
        SPEC.base_thickness_mm,
        SPEC.m3_socket_head_height_mm,
    )
    return _single_solid(shaft.fuse(head), f"{NAMESPACE}_ISO4762_M3x6")


def nominal_nut_shape(seam_index: int, radius_mm: float):
    angle = SEAMS[seam_index - 1][1]
    return _single_solid(
        _hex_prism(
            angle,
            radius_mm,
            screw_axis_tangent(seam_index),
            SPEC.m3_nut_af_mm,
            -SPEC.m3_nut_max_thickness_mm,
            SPEC.m3_nut_max_thickness_mm,
        ),
        f"{NAMESPACE}_ISO4032_M3_nut",
    )


def driver_access_shape(seam_index: int, radius_mm: float):
    angle = SEAMS[seam_index - 1][1]
    return vertical_cylinder(
        angle,
        radius_mm,
        screw_axis_tangent(seam_index),
        SPEC.m3_socket_head_max_diameter_mm,
        SPEC.base_thickness_mm,
        20.0,
    )


def wrench_access_shape(seam_index: int, radius_mm: float):
    angle = SEAMS[seam_index - 1][1]
    return _hex_prism(
        angle,
        radius_mm,
        screw_axis_tangent(seam_index),
        SPEC.wrench_access_af_mm + 2.0,
        -6.0,
        6.0,
    )


def hardware_occurrences() -> tuple[dict[str, object], ...]:
    rows = []
    for seam_index in range(1, 5):
        for position, radius in zip(("inner", "outer"), SPEC.screw_axis_radii_mm):
            screw = nominal_screw_shape(seam_index, radius)
            screw.label = f"{NAMESPACE}_M3x6_S{seam_index}_{position}"
            nut = nominal_nut_shape(seam_index, radius)
            nut.label = f"{NAMESPACE}_M3_nut_S{seam_index}_{position}"
            rows.extend((
                {"kind": "screw", "seam_index": seam_index, "position": position, "radius_mm": radius, "shape": screw},
                {"kind": "nut", "seam_index": seam_index, "position": position, "radius_mm": radius, "shape": nut},
            ))
    return tuple(rows)


def assembled_shape():
    children = [named_quadrant(i) for i in range(1, 5)]
    children.extend(deepcopy(row["shape"]) for row in hardware_occurrences())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_with_hardware")


def service_exploded_shape():
    children = []
    for index in range(1, 5):
        center_angle = SPEC.seam_base_angle_deg + (index - 0.5) * SPEC.quadrant_angle_deg
        dx, dy = local_point(center_angle, SPEC.exploded_quadrant_radial_mm, 0.0)
        moved = named_quadrant(index).moved(Location((dx, dy, 0.0)))
        moved.label = f"{NAMESPACE}_quadrant_Q{index}_{'A' if index in SPEC.role_a_quadrants else 'B'}"
        children.append(moved)
    for row in hardware_occurrences():
        direction = SPEC.exploded_hardware_z_mm if row["kind"] == "screw" else -SPEC.exploded_hardware_z_mm
        moved = deepcopy(row["shape"]).moved(Location((0.0, 0.0, direction)))
        moved.label = row["shape"].label
        children.append(moved)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded")


def printable_quadrant_shape(index: int):
    shape = named_quadrant(index)
    if index in SPEC.role_b_quadrants:
        shape = shape.rotate(Axis.X, 180.0).moved(Location((0.0, 0.0, SPEC.base_thickness_mm)))
        orientation = "front_down"
    else:
        orientation = "underside_down"
    shape.label = f"{NAMESPACE}_quadrant_Q{index}_{orientation}"
    return shape


def printable_occurrences() -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "name": f"quadrant_Q{index}",
            "kind": "quadrant_A" if index in SPEC.role_a_quadrants else "quadrant_B",
            "orientation": "underside_down" if index in SPEC.role_a_quadrants else "front_down",
            "label": f"{NAMESPACE}_quadrant_Q{index}_{'underside_down' if index in SPEC.role_a_quadrants else 'front_down'}",
            "shape": printable_quadrant_shape(index),
        }
        for index in range(1, 5)
    )
