"""Actual BREP geometry for the isolated three-sector diagonal-fit preview."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, Solid, extrude
from cadgen import srgb
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.TopLoc import TopLoc_Location

from p3_v3_mvp_base_q4_r4_functional_centered_step_lap_geometry import (
    motor_slot_tools,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import NAMESPACE, SPEC


# seam name, angle, upper owner, lower owner (zero-based sector indexes)
LAPS = (
    ("S_AB", 60.0, 0, 1),
    ("S_BC", 180.0, 1, 2),
    ("S_CA", 300.0, 2, 0),
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


def _bake_location(shape):
    """Bake a build123d Location into BREP geometry for export parity."""

    location = shape.wrapped.Location()
    unlocated = shape.wrapped.Located(TopLoc_Location())
    transformed = BRepBuilderAPI_Transform(
        unlocated,
        location.Transformation(),
        True,
        True,
    ).Shape()
    return Solid(transformed)


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


def _vertical_cylinder(
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


def full_annulus_shape():
    outer = Cylinder(
        SPEC.base_outer_radius_mm,
        SPEC.plate_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm)))
    inner = Cylinder(
        SPEC.base_inner_radius_mm,
        SPEC.plate_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm)))
    return _single_solid(outer.cut(inner), f"{NAMESPACE}_source_annulus")


def _sector_mask(center_angle_deg: float):
    start = center_angle_deg - SPEC.sector_sweep_deg / 2.0
    end = center_angle_deg + SPEC.sector_sweep_deg / 2.0
    radius = SPEC.base_outer_radius_mm + 2.0 * SPEC.boolean_overshoot_mm
    samples = 32
    points = [(0.0, 0.0)]
    for index in range(samples + 1):
        angle = radians(start + (end - start) * index / samples)
        points.append((radius * cos(angle), radius * sin(angle)))
    face = Polygon(*points)
    return extrude(face, amount=SPEC.plate_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm).moved(
        Location((0.0, 0.0, SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm))
    )


def plain_sector_shapes() -> tuple:
    annulus = full_annulus_shape()
    return tuple(
        _single_solid(
            deepcopy(annulus).intersect(_sector_mask(center)),
            f"{NAMESPACE}_sector_{index}_plain",
        )
        for index, center in enumerate(SPEC.sector_center_angles_deg, 1)
    )


def _donor_tool(angle_deg: float, z0_mm: float, height_mm: float):
    return _local_box(
        angle_deg,
        SPEC.lap_r_min_mm,
        SPEC.lap_r_max_mm,
        -SPEC.donor_t_half_mm,
        SPEC.donor_t_half_mm,
        z0_mm,
        height_mm,
    )


def _receiver_tool(angle_deg: float, z0_mm: float, height_mm: float):
    return _local_box(
        angle_deg,
        SPEC.lap_r_min_mm - SPEC.receiver_plan_clearance_mm,
        SPEC.lap_r_max_mm + SPEC.receiver_plan_clearance_mm,
        -SPEC.receiver_t_half_mm,
        SPEC.receiver_t_half_mm,
        z0_mm,
        height_mm,
    )


def seam_mount_hole_tools() -> tuple:
    """Return the 12 through-bore tools: four at each identical seam."""

    return tuple(
        _vertical_cylinder(
            angle,
            radius,
            tangent,
            SPEC.roller_mount_hole_diameter_mm,
            SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm,
            SPEC.plate_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        )
        for angle in SPEC.seam_angles_deg
        for radius in SPEC.seam_hole_row_radii_mm
        for tangent in SPEC.roller_mount_tangent_offsets_mm
    )


@lru_cache(maxsize=1)
def lapped_sector_shapes() -> tuple:
    """Return the three complementary lap owners before functional bores."""

    sectors = [deepcopy(shape) for shape in plain_sector_shapes()]
    for seam_name, angle, upper_index, lower_index in LAPS:
        sectors[upper_index] = _single_solid(
            sectors[upper_index]
            .cut(_receiver_tool(
                angle,
                SPEC.plate_bottom_z_mm - SPEC.boolean_overshoot_mm,
                SPEC.lower_lap_thickness_mm + SPEC.boolean_overshoot_mm,
            ))
            .fuse(_donor_tool(angle, SPEC.lap_split_z_mm, SPEC.upper_lap_thickness_mm)),
            f"{NAMESPACE}_{seam_name}_upper",
        )
        sectors[lower_index] = _single_solid(
            sectors[lower_index]
            .cut(_receiver_tool(
                angle,
                SPEC.lap_split_z_mm,
                SPEC.upper_lap_thickness_mm + SPEC.boolean_overshoot_mm,
            ))
            .fuse(_receiver_tool(
                angle,
                SPEC.plate_bottom_z_mm,
                SPEC.lower_lap_thickness_mm,
            )),
            f"{NAMESPACE}_{seam_name}_lower",
        )

    return tuple(sectors)


@lru_cache(maxsize=1)
def sector_shapes() -> tuple:
    sectors = [deepcopy(shape) for shape in lapped_sector_shapes()]
    # The inherited Q4 spine holes are intentionally absent in Q3.  Q3 uses
    # only its three repeated motor stations and four repeated holes per seam.
    functional_tools = (*motor_slot_tools(), *seam_mount_hole_tools())
    colors = ("#EC6A2C", "#00A6A6", "#E71D73")
    for index in range(3):
        sectors[index] = _single_solid(
            sectors[index].cut(*(deepcopy(tool) for tool in functional_tools)),
            f"{NAMESPACE}_sector_{index + 1}",
        )
        sectors[index].color = srgb(colors[index])
    return tuple(sectors)


def named_sector(index: int):
    if index not in range(1, 4):
        raise ValueError("sector index must be 1..3")
    return deepcopy(sector_shapes()[index - 1])


def roller_bridge_witness_shape(angle_deg: float):
    bridge = _local_box(
        angle_deg,
        SPEC.roller_bridge_radial_mm[0],
        SPEC.roller_bridge_radial_mm[1],
        SPEC.roller_bridge_tangent_mm[0],
        SPEC.roller_bridge_tangent_mm[1],
        SPEC.roller_bridge_preview_z_mm,
        SPEC.roller_bridge_preview_thickness_mm,
    )
    holes = tuple(
        _vertical_cylinder(
            angle_deg,
            SPEC.roller_axle_radius_mm,
            tangent,
            SPEC.roller_mount_hole_diameter_mm,
            SPEC.roller_bridge_preview_z_mm - SPEC.boolean_overshoot_mm,
            SPEC.roller_bridge_preview_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        )
        for tangent in SPEC.roller_mount_tangent_offsets_mm
    )
    bridge = _single_solid(bridge.cut(*holes), f"{NAMESPACE}_roller_bridge_{angle_deg:g}deg")
    bridge.color = srgb("#2D3748")
    return bridge


def assembled_preview_shape():
    children = [named_sector(index) for index in range(1, 4)]
    children.extend(roller_bridge_witness_shape(angle) for angle in SPEC.seam_angles_deg)
    return Compound(children=children, label=f"{NAMESPACE}_assembled_with_roller_seam_witnesses")


def printable_sector_shape(index: int):
    center = SPEC.sector_center_angles_deg[index - 1]
    rotation = SPEC.diagonal_rotation_deg - center
    shape = named_sector(index).rotate(Axis.Z, rotation).moved(
        Location((0.0, 0.0, -SPEC.plate_bottom_z_mm))
    )
    shape = _bake_location(shape)
    shape.label = f"{NAMESPACE}_sector_{index}_diagonal_u1_orientation"
    return shape


def _bed_shape(center_x_mm: float):
    bed = Box(
        SPEC.u1_bed_xy_mm,
        SPEC.u1_bed_xy_mm,
        SPEC.preview_bed_thickness_mm,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    ).moved(Location((center_x_mm, 0.0, -0.5)))
    bed.label = f"{NAMESPACE}_u1_bed_{center_x_mm:g}"
    bed.color = srgb("#ECE7DD", 0.55)
    return bed


def diagonal_bed_preview_shape():
    children = []
    for index in range(1, 4):
        center_x = (index - 2) * SPEC.preview_bed_spacing_mm
        children.append(_bed_shape(center_x))
        part = printable_sector_shape(index).moved(Location((center_x, 0.0, 0.0)))
        part.label = f"{NAMESPACE}_sector_{index}_on_u1_bed"
        children.append(part)
    return Compound(children=children, label=f"{NAMESPACE}_three_diagonal_u1_beds")


def printable_bounds_with_brim(index: int) -> tuple[float, float]:
    box = printable_sector_shape(index).bounding_box()
    return (
        float(box.size.X + 2.0 * SPEC.print_brim_mm),
        float(box.size.Y + 2.0 * SPEC.print_brim_mm),
    )
