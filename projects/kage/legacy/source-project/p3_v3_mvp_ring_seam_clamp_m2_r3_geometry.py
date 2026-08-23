"""KAGE r3 seam clamp with full solid-ring-body radial flange coverage."""

from __future__ import annotations

from copy import deepcopy
from math import cos, radians, sin

from build123d import Align, Axis, Compound, Cone, Cylinder, Location
from cadgen import srgb

from p3_v3_mvp_ring_seam_clamp_m2_r1_geometry import _annular_sector, _volume
from p3_v3_mvp_ring_seam_clamp_m2_r2_geometry import (
    authority,
    make_hardware_references as _make_hardware_references_r2,
    make_production_quadrant as _make_production_quadrant_r2,
)
from p3_v3_mvp_ring_seam_clamp_m2_r3_spec import SPEC


def make_production_quadrant(role_index: int, quadrant_index: int):
    part = deepcopy(_make_production_quadrant_r2(role_index, quadrant_index))
    part.label = part.label.replace("valley_side_loaded_M2_nut", "r3_full_radial_valley_side_loaded_M2_nut")
    return part


def make_hardware_references(role_index: int):
    return tuple(deepcopy(part) for part in _make_hardware_references_r2(role_index))


def clamp_z(role_index: int) -> tuple[float, float, float, float]:
    z0, z1 = SPEC.carrier_layers[role_index]
    bottom_top = z0 - SPEC.clamp_fit_clearance_per_face_mm
    bottom_bottom = bottom_top - SPEC.clamp_bottom_flange_thickness_mm
    top_bottom = z1 + SPEC.clamp_fit_clearance_per_face_mm
    top_top = top_bottom + SPEC.clamp_top_flange_thickness_mm
    return bottom_bottom, bottom_top, top_bottom, top_top


def _local(shape, radial: float, tangent: float, z: float = 0.0):
    return shape.moved(Location((radial, tangent, z))).rotate(Axis.Z, SPEC.seam_angle_deg)


def _axis_from_tangent(tangent: float) -> tuple[float, float]:
    from math import sqrt
    return sqrt(SPEC.screw_axis_radius_mm**2 - tangent**2), tangent


def make_channel_clamp(role_index: int):
    """One U/ㄈ clamp whose flanges cover R132.50..R138.90 ring body.

    The clamp still ends at the tooth root, so the entire R129.00..R132.50
    involute-like tooth profile remains exposed to pinions and guide rollers.
    """
    bottom_bottom, bottom_top, top_bottom, top_top = clamp_z(role_index)
    bottom = _annular_sector(
        SPEC.clamp_inner_radius_mm, SPEC.clamp_outer_radius_mm,
        SPEC.clamp_tangential_width_mm, bottom_bottom, bottom_top,
    )
    top = _annular_sector(
        SPEC.clamp_inner_radius_mm, SPEC.clamp_outer_radius_mm,
        SPEC.clamp_tangential_width_mm, top_bottom, top_top,
    )
    wall = _annular_sector(
        SPEC.clamp_side_wall_inner_radius_mm, SPEC.clamp_outer_radius_mm,
        SPEC.clamp_tangential_width_mm, bottom_bottom, top_top,
    )
    clamp = bottom.fuse(top).fuse(wall).rotate(Axis.Z, SPEC.seam_angle_deg)
    for tangent in SPEC.screw_tangential_offsets_mm:
        radial, tangent = _axis_from_tangent(tangent)
        clamp = clamp.cut(_local(Cylinder(
            SPEC.screw_clearance_diameter_mm / 2.0,
            SPEC.clamp_top_flange_thickness_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_bottom - 0.1))
        clamp = clamp.cut(_local(Cone(
            SPEC.screw_clearance_diameter_mm / 2.0,
            SPEC.screw_head_diameter_mm / 2.0,
            SPEC.screw_head_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_bottom))
    clamp.label = f"{SPEC.roles[role_index]}_R3_FULL_RADIAL_ONE_PIECE_U_CLAMP_M2"
    clamp.color = srgb("#AEB5B9")
    return clamp


def make_role_seam_module(role_index: int, full_ring: bool = False, include_hardware: bool = True):
    quadrants = range(4) if full_ring else range(2)
    parts = [make_production_quadrant(role_index, q) for q in quadrants]
    parts.append(make_channel_clamp(role_index))
    if include_hardware:
        parts.extend(make_hardware_references(role_index))
    return Compound(children=parts, label=f"{SPEC.roles[role_index]}_r3_full_radial_U_clamp_M2")


def make_hour_coupon():
    return make_role_seam_module(0, full_ring=False, include_hardware=True)


def make_three_ring_stack(include_hardware: bool = True):
    parts = []
    for role in range(3):
        parts.extend(make_role_seam_module(role, full_ring=True, include_hardware=include_hardware).children)
    return Compound(children=parts, label="three_ring_stack_with_r3_full_radial_U_clamps")


def clamp_slide_rows(role_index: int):
    angle = radians(SPEC.seam_angle_deg)
    ux, uy = cos(angle), sin(angle)
    clamp = make_channel_clamp(role_index)
    rows = []
    for index in range(SPEC.slide_sample_count):
        offset = SPEC.slide_start_offset_mm * (SPEC.slide_sample_count - 1 - index) / (SPEC.slide_sample_count - 1)
        rows.append((offset, deepcopy(clamp).moved(Location((ux * offset, uy * offset, 0.0)))))
    return tuple(rows)


def stationary_pinion_and_roller_references():
    """Actual locked STEP solids that the rotating clamp must pass."""
    _, children = authority()
    indices = (23, 24, 25, 40, 41, 42, 57, 58, 59, 136, 167, 198)
    return tuple(deepcopy(children[index]) for index in indices)


def clamp_station_sweep_rows(role_index: int):
    """Align a role clamp to every real pinion/roller station, plus edge offsets."""
    rows = []
    clamp = make_channel_clamp(role_index)
    for reference in stationary_pinion_and_roller_references():
        box = reference.bounding_box()
        cx = (box.min.X + box.max.X) / 2.0
        cy = (box.min.Y + box.max.Y) / 2.0
        from math import atan2, degrees
        station_angle = degrees(atan2(cy, cx))
        for delta in (-5.0, 0.0, 5.0):
            rotation = station_angle + delta - SPEC.seam_angle_deg
            rows.append((reference.label, delta, deepcopy(clamp).rotate(Axis.Z, rotation)))
    return tuple(rows)


def print_layout_rows():
    shapes = [make_production_quadrant(0, 0), make_production_quadrant(0, 1), make_channel_clamp(0)]
    targets = ((5.0, 5.0), (110.0, 110.0), (230.0, 10.0))
    rows = []
    for shape, (x, y) in zip(shapes, targets, strict=True):
        box = shape.bounding_box()
        translation = (x - box.min.X, y - box.min.Y, -box.min.Z)
        placed = deepcopy(shape).moved(Location(translation))
        placed.label = shape.label
        rows.append({"source": shape, "shape": placed, "translation_mm": translation})
    return tuple(rows)


def make_print_layout():
    return Compound(children=[row["shape"] for row in print_layout_rows()], label="hour_r3_full_radial_U_clamp_M2_print_layout")


def make_cross_section_review():
    """Three clamps plus tooth-root/tip datum cylinders for visual review."""
    stack = make_three_ring_stack(include_hardware=True)
    return stack
