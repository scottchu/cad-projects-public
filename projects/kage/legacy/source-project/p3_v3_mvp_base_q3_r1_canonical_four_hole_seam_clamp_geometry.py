"""BREP geometry for the Q3 canonical four-hole flat seam clamp branch."""

from __future__ import annotations

from copy import deepcopy
from math import cos, radians, sin

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Solid
from cadgen import srgb
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.TopLoc import TopLoc_Location

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import (
    LAPS,
    intersection_volume_mm3,
    local_point,
    motor_slot_tools,
    named_sector,
    printable_sector_shape,
    sector_shapes,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC as BASE_SPEC
from p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp_spec import NAMESPACE, SPEC


def _single_solid(shape, label: str):
    solids = [] if shape is None else list(shape.solids())
    if len(solids) != 1:
        raise RuntimeError(f"{label} must be one solid, got {len(solids)}")
    result = solids[0]
    result.label = label
    return result


def _bake_location(shape):
    location = shape.wrapped.Location()
    unlocated = shape.wrapped.Located(TopLoc_Location())
    transformed = BRepBuilderAPI_Transform(
        unlocated,
        location.Transformation(),
        True,
        True,
    ).Shape()
    baked = Solid(transformed)
    baked.label = f"{NAMESPACE}_baked_shape"
    return baked


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


def clamp_hole_axes_world_xy(angle_deg: float) -> tuple[tuple[float, float], ...]:
    return tuple(
        local_point(angle_deg, radius, tangent)
        for radius, tangent in SPEC.clamp_hole_axes_local_rt_mm
    )


def clamp_hole_tools(angle_deg: float, overshoot_mm: float | None = None) -> tuple:
    overshoot = SPEC.boolean_overshoot_mm if overshoot_mm is None else overshoot_mm
    return tuple(
        _vertical_cylinder(
            angle_deg,
            radius,
            tangent,
            SPEC.clamp_hole_diameter_mm,
            SPEC.clamp_contact_z_mm - overshoot,
            SPEC.clamp_thickness_mm + 2.0 * overshoot,
        )
        for radius, tangent in SPEC.clamp_hole_axes_local_rt_mm
    )


def canonical_clamp_uncut_shape():
    body = _local_box(
        0.0,
        SPEC.clamp_radial_min_mm,
        SPEC.clamp_radial_max_mm,
        SPEC.clamp_tangent_min_mm,
        SPEC.clamp_tangent_max_mm,
        SPEC.clamp_contact_z_mm,
        SPEC.clamp_thickness_mm,
    )
    return _single_solid(body, f"{NAMESPACE}_canonical_clamp_uncut")


def canonical_clamp_shape():
    clamp = canonical_clamp_uncut_shape().cut(*clamp_hole_tools(0.0))
    clamp = _single_solid(clamp, f"{NAMESPACE}_canonical_four_hole_flat_clamp")
    clamp.color = srgb("#253446")
    return clamp


def clamp_instance_shape(angle_deg: float):
    clamp = canonical_clamp_shape().rotate(Axis.Z, angle_deg)
    clamp.label = f"{NAMESPACE}_clamp_{angle_deg:g}deg"
    return clamp


def assembled_shape():
    children = [deepcopy(shape) for shape in sector_shapes()]
    children.extend(clamp_instance_shape(angle) for angle in SPEC.clamp_instance_angles_deg)
    return Compound(children=children, label=f"{NAMESPACE}_assembled")


def service_exploded_shape():
    children = []
    for index, center_angle in enumerate(BASE_SPEC.sector_center_angles_deg, 1):
        angle = radians(center_angle)
        dx = SPEC.exploded_sector_radial_offset_mm * cos(angle)
        dy = SPEC.exploded_sector_radial_offset_mm * sin(angle)
        sector = named_sector(index).moved(Location((dx, dy, 0.0)))
        sector.label = f"{NAMESPACE}_service_sector_{index}"
        children.append(sector)
    for angle in SPEC.clamp_instance_angles_deg:
        clamp = clamp_instance_shape(angle).moved(Location((0.0, 0.0, SPEC.exploded_clamp_z_offset_mm)))
        clamp.label = f"{NAMESPACE}_service_clamp_{angle:g}deg"
        children.append(clamp)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded")


def printable_clamp_shape():
    clamp = canonical_clamp_shape().moved(Location((0.0, 0.0, -SPEC.clamp_contact_z_mm)))
    clamp = _bake_location(clamp)
    clamp.label = f"{NAMESPACE}_canonical_clamp_print_orientation"
    clamp.color = srgb("#253446")
    return clamp


def printable_clamp_qty3_shape():
    children = []
    for index, x_offset in enumerate((-SPEC.clamp_print_spacing_x_mm, 0.0, SPEC.clamp_print_spacing_x_mm), 1):
        clamp = printable_clamp_shape().moved(Location((x_offset, 0.0, 0.0)))
        clamp.label = f"{NAMESPACE}_canonical_clamp_print_{index}_of_3"
        children.append(clamp)
    return Compound(children=children, label=f"{NAMESPACE}_canonical_clamp_print_qty3")


def canonical_printable_sector_shape():
    """Return the accepted Q3 sector without modifying its source geometry."""

    sector = printable_sector_shape(1)
    sector.label = f"{NAMESPACE}_canonical_sector_print_orientation"
    return sector


def ring_motion_keepout_shape():
    outer = Cylinder(
        SPEC.ring_keepout_outer_radius_mm,
        SPEC.ring_keepout_height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.ring_keepout_bottom_z_mm)))
    inner = Cylinder(
        SPEC.ring_keepout_inner_radius_mm,
        SPEC.ring_keepout_height_mm + 2.0 * SPEC.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, SPEC.ring_keepout_bottom_z_mm - SPEC.boolean_overshoot_mm)))
    return outer.cut(inner)


def motor_keepout_shapes() -> tuple:
    return tuple(
        _local_box(
            angle,
            SPEC.motor_keepout_radial_min_mm,
            SPEC.motor_keepout_radial_max_mm,
            -SPEC.motor_keepout_tangent_half_mm,
            SPEC.motor_keepout_tangent_half_mm,
            SPEC.motor_keepout_bottom_z_mm,
            SPEC.motor_keepout_height_mm,
        )
        for angle in BASE_SPEC.motor_station_angles_deg
    )


def roller_keepout_shapes() -> tuple:
    return tuple(
        _vertical_cylinder(
            angle,
            SPEC.roller_keepout_axis_radius_mm,
            0.0,
            SPEC.roller_keepout_diameter_mm,
            SPEC.roller_keepout_bottom_z_mm,
            SPEC.roller_keepout_height_mm,
        )
        for angle in SPEC.clamp_instance_angles_deg
    )


def clamp_base_intersection_volumes_mm3() -> tuple[float, ...]:
    sectors = sector_shapes()
    return tuple(
        intersection_volume_mm3(clamp_instance_shape(angle), sector)
        for angle in SPEC.clamp_instance_angles_deg
        for sector in sectors
    )


def clamp_print_bounds_mm() -> tuple[float, float, float]:
    box = printable_clamp_qty3_shape().bounding_box()
    return float(box.size.X), float(box.size.Y), float(box.size.Z)
