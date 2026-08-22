"""STEP-first BREP geometry for the Q3 r2 roller-mount release.

Coordinate convention: the clock remains in r0 world coordinates (XY plate,
+Z upward).  The canonical mount is authored at a zero-degree radial seam and
all assembly instances are exact rotations about world Z.
"""

from __future__ import annotations

from copy import deepcopy
from math import cos, pi, radians, sin, sqrt

from build123d import Align, Axis, Box, Compound, Cylinder, Location, Polygon, Solid, extrude
from cadgen import srgb
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.TopLoc import TopLoc_Location

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import (
    LAPS,
    intersection_volume_mm3,
    local_point,
    named_sector,
    printable_bounds_with_brim,
    printable_sector_shape,
    sector_shapes,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC as BASE_SPEC
from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_spec import NAMESPACE, SPEC


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
    return Solid(transformed)


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


def canonical_printable_sector_shape():
    """Return the accepted r0 printable BREP directly, without remodeling it."""

    return printable_sector_shape(1)


def roller_mount_hole_tools(angle_deg: float = 0.0) -> tuple:
    """Two and only two bores: the outer r=118 mm free-roller pair."""

    return tuple(
        _vertical_cylinder(
            angle_deg,
            radius,
            tangent,
            SPEC.mount_hole_diameter_mm,
            SPEC.mount_contact_z_mm - SPEC.boolean_overshoot_mm,
            SPEC.mount_thickness_mm + 2.0 * SPEC.boolean_overshoot_mm,
        )
        for radius, tangent in SPEC.mount_hole_axes_local_rt_mm
    )


def canonical_roller_mount_uncut_shape():
    body = _local_box(
        0.0,
        SPEC.mount_radial_min_mm,
        SPEC.mount_radial_max_mm,
        SPEC.mount_tangent_min_mm,
        SPEC.mount_tangent_max_mm,
        SPEC.mount_contact_z_mm,
        SPEC.mount_thickness_mm,
    )
    return _single_solid(body, f"{NAMESPACE}_canonical_roller_mount_base_uncut")


def canonical_roller_mount_shape():
    mount = canonical_roller_mount_uncut_shape().cut(*roller_mount_hole_tools())
    mount = _single_solid(mount, f"{NAMESPACE}_canonical_roller_mount_base")
    mount.color = srgb("#253446")
    return mount


def roller_mount_instance_shape(angle_deg: float):
    mount = canonical_roller_mount_shape().rotate(Axis.Z, angle_deg)
    mount.label = f"{NAMESPACE}_roller_mount_{angle_deg:g}deg"
    return mount


def printable_roller_mount_shape():
    radial_center = (SPEC.mount_radial_min_mm + SPEC.mount_radial_max_mm) / 2.0
    tangent_center = (SPEC.mount_tangent_min_mm + SPEC.mount_tangent_max_mm) / 2.0
    mount = canonical_roller_mount_shape().moved(
        Location((-radial_center, -tangent_center, -SPEC.mount_contact_z_mm))
    )
    mount = _bake_location(mount)
    mount.label = f"{NAMESPACE}_canonical_roller_mount_print_orientation"
    mount.color = srgb("#253446")
    return mount


def printable_roller_mount_qty3_layout_shape():
    children = []
    for index, x_offset in enumerate(
        (-SPEC.mount_print_spacing_x_mm, 0.0, SPEC.mount_print_spacing_x_mm), 1
    ):
        mount = printable_roller_mount_shape().moved(Location((x_offset, 0.0, 0.0)))
        mount.label = f"{NAMESPACE}_roller_mount_print_{index}_of_3"
        children.append(mount)
    return Compound(children=children, label=f"{NAMESPACE}_roller_mount_print_qty3_layout")


def _hex_face(center_x_mm: float, center_y_mm: float, across_flats_mm: float):
    circumradius = across_flats_mm / sqrt(3.0)
    points = tuple(
        (
            center_x_mm + circumradius * cos(radians(30.0 + index * 60.0)),
            center_y_mm + circumradius * sin(radians(30.0 + index * 60.0)),
        )
        for index in range(6)
    )
    return Polygon(*points)


def m3_screw_hardware_envelope(angle_deg: float, radius_mm: float, tangent_mm: float):
    """Simplified M3 shank/head envelope; not a threaded purchased-part model."""

    has_mount = radius_mm == SPEC.mount_hole_radius_mm
    seat_z = SPEC.mount_top_z_mm if has_mount else BASE_SPEC.plate_top_z_mm
    nut_bottom_z = BASE_SPEC.plate_bottom_z_mm - SPEC.m3_nut_height_mm
    shank = _vertical_cylinder(
        angle_deg,
        radius_mm,
        tangent_mm,
        SPEC.m3_shank_diameter_mm,
        nut_bottom_z,
        seat_z - nut_bottom_z,
    )
    head = _vertical_cylinder(
        angle_deg,
        radius_mm,
        tangent_mm,
        SPEC.m3_head_diameter_mm,
        seat_z,
        SPEC.m3_head_height_mm,
    )
    row = "outer_mount" if has_mount else "inner_plain"
    screw = _single_solid(
        shank.fuse(head),
        f"{NAMESPACE}_m3_screw_hardware_envelope_{row}_{angle_deg:g}_{tangent_mm:+g}",
    )
    screw.color = srgb("#A9B0B7")
    return screw


def m3_nut_hardware_envelope(angle_deg: float, radius_mm: float, tangent_mm: float):
    """Simplified M3 hex-nut envelope with a clearance bore."""

    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    face = _hex_face(x, y, SPEC.m3_nut_across_flats_mm)
    nut = extrude(face, amount=SPEC.m3_nut_height_mm).moved(
        Location((0.0, 0.0, BASE_SPEC.plate_bottom_z_mm - SPEC.m3_nut_height_mm))
    )
    bore = Cylinder(
        SPEC.m3_nut_bore_diameter_mm / 2.0,
        SPEC.m3_nut_height_mm + 2.0 * SPEC.boolean_overshoot_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(
        Location(
            (
                x,
                y,
                BASE_SPEC.plate_bottom_z_mm - SPEC.m3_nut_height_mm - SPEC.boolean_overshoot_mm,
            )
        )
    )
    row = "outer_mount" if radius_mm == SPEC.mount_hole_radius_mm else "inner_plain"
    nut = _single_solid(
        nut.cut(bore),
        f"{NAMESPACE}_m3_nut_hardware_envelope_{row}_{angle_deg:g}_{tangent_mm:+g}",
    )
    nut.color = srgb("#747D87")
    return nut


def assembled_hardware_shapes() -> tuple:
    children = []
    for angle in BASE_SPEC.seam_angles_deg:
        for radius in BASE_SPEC.seam_hole_row_radii_mm:
            for tangent in BASE_SPEC.roller_mount_tangent_offsets_mm:
                children.append(m3_screw_hardware_envelope(angle, radius, tangent))
                children.append(m3_nut_hardware_envelope(angle, radius, tangent))
    return tuple(children)


def assembled_shape():
    children = [deepcopy(shape) for shape in sector_shapes()]
    children.extend(roller_mount_instance_shape(angle) for angle in SPEC.mount_instance_angles_deg)
    children.extend(assembled_hardware_shapes())
    return Compound(children=children, label=f"{NAMESPACE}_assembled_hardware_envelopes")


def service_exploded_shape():
    children = []
    for index, center_angle in enumerate(BASE_SPEC.sector_center_angles_deg, 1):
        angle = radians(center_angle)
        sector = named_sector(index).moved(
            Location(
                (
                    SPEC.exploded_sector_radial_offset_mm * cos(angle),
                    SPEC.exploded_sector_radial_offset_mm * sin(angle),
                    0.0,
                )
            )
        )
        sector.label = f"{NAMESPACE}_service_sector_{index}"
        children.append(sector)
    children.extend(
        roller_mount_instance_shape(angle).moved(Location((0.0, 0.0, SPEC.exploded_mount_z_offset_mm)))
        for angle in SPEC.mount_instance_angles_deg
    )
    for index, hardware in enumerate(assembled_hardware_shapes()):
        is_screw = "_screw_" in hardware.label
        z_offset = SPEC.exploded_screw_z_offset_mm if is_screw else SPEC.exploded_nut_z_offset_mm
        item = hardware.moved(Location((0.0, 0.0, z_offset)))
        item.label = f"{hardware.label}_service_{index + 1}"
        children.append(item)
    return Compound(children=children, label=f"{NAMESPACE}_service_exploded_hardware_envelopes")


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
    return _single_solid(outer.cut(inner), f"{NAMESPACE}_modeled_ring_motion_keepout")


def motor_keepout_shapes() -> tuple:
    return tuple(
        _single_solid(
            _local_box(
                angle,
                SPEC.motor_keepout_radial_min_mm,
                SPEC.motor_keepout_radial_max_mm,
                -SPEC.motor_keepout_tangent_half_mm,
                SPEC.motor_keepout_tangent_half_mm,
                SPEC.motor_keepout_bottom_z_mm,
                SPEC.motor_keepout_height_mm,
            ),
            f"{NAMESPACE}_modeled_motor_keepout_{angle:g}deg",
        )
        for angle in BASE_SPEC.motor_station_angles_deg
    )


def free_roller_keepout_shapes() -> tuple:
    return tuple(
        _single_solid(
            _vertical_cylinder(
                angle,
                SPEC.free_roller_keepout_axis_radius_mm,
                0.0,
                SPEC.free_roller_keepout_diameter_mm,
                SPEC.free_roller_keepout_bottom_z_mm,
                SPEC.free_roller_keepout_height_mm,
            ),
            f"{NAMESPACE}_modeled_free_roller_keepout_{angle:g}deg",
        )
        for angle in SPEC.mount_instance_angles_deg
    )


def roller_mount_print_bounds_mm() -> tuple[float, float, float]:
    box = printable_roller_mount_qty3_layout_shape().bounding_box()
    return float(box.size.X), float(box.size.Y), float(box.size.Z)


def mount_base_intersection_volumes_mm3() -> tuple[float, ...]:
    sectors = sector_shapes()
    return tuple(
        intersection_volume_mm3(roller_mount_instance_shape(angle), sector)
        for angle in SPEC.mount_instance_angles_deg
        for sector in sectors
    )


__all__ = [
    "LAPS",
    "assembled_hardware_shapes",
    "assembled_shape",
    "canonical_printable_sector_shape",
    "canonical_roller_mount_shape",
    "canonical_roller_mount_uncut_shape",
    "free_roller_keepout_shapes",
    "intersection_volume_mm3",
    "motor_keepout_shapes",
    "mount_base_intersection_volumes_mm3",
    "printable_bounds_with_brim",
    "printable_roller_mount_qty3_layout_shape",
    "printable_roller_mount_shape",
    "ring_motion_keepout_shape",
    "roller_mount_hole_tools",
    "roller_mount_instance_shape",
    "roller_mount_print_bounds_mm",
    "service_exploded_shape",
]
