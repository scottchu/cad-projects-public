"""Stack-safe KAGE seam clamp: one U-channel, two flush M2 paths."""

from __future__ import annotations

from copy import deepcopy
from math import atan2, cos, degrees, radians, sin, sqrt

from build123d import Align, Axis, Box, Compound, Cone, Cylinder, Location, RegularPolygon, extrude
from cadgen import srgb

from p3_v3_mvp_ring_seam_clamp_m2_r1_geometry import (
    _annular_sector,
    _volume,
    authority,
    capture_clearance_report as _obsolete_capture_clearance_report,
    make_clean_locked_full_ring,
    make_interlock_male,
    make_interlock_pocket_tool,
    make_shifted_base_quadrant,
)
from p3_v3_mvp_ring_seam_clamp_m2_r2_spec import SPEC


def _local(shape, radial: float, tangent: float, z: float = 0.0):
    return shape.moved(Location((radial, tangent, z))).rotate(Axis.Z, SPEC.seam_angle_deg)


def _axis_from_tangent(tangent: float) -> tuple[float, float]:
    return sqrt(SPEC.screw_axis_radius_mm**2 - tangent**2), tangent


def _hex_prism(across_flats: float, height: float, radial: float, tangent: float, z0: float):
    local_radial_angle = degrees(atan2(tangent, radial))
    shape = extrude(RegularPolygon(across_flats / 2.0, 6, major_radius=False), amount=height)
    return shape.rotate(Axis.Z, local_radial_angle - 90.0).moved(
        Location((radial, tangent, z0))
    ).rotate(Axis.Z, SPEC.seam_angle_deg)


def _receiver_ear(role_index: int, tangent: float):
    z0, z1 = SPEC.carrier_layers[role_index]
    radial, tangent = _axis_from_tangent(tangent)
    connector = Box(
        radial - SPEC.receiver_connector_inner_radius_mm + SPEC.receiver_boss_radius_mm,
        SPEC.receiver_connector_tangential_width_mm,
        z1 - z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.receiver_connector_inner_radius_mm, tangent, z0)))
    boss = Cylinder(SPEC.receiver_boss_radius_mm, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((radial, tangent, z0))
    )
    return connector.fuse(boss).rotate(Axis.Z, SPEC.seam_angle_deg)


def _nut_pocket_and_outboard_loading_slot(role_index: int, tangent: float):
    z0, z1 = SPEC.carrier_layers[role_index]
    z_mid = (z0 + z1) / 2.0
    pocket_z0 = z_mid - SPEC.nut_trap_depth_mm / 2.0
    radial, tangent = _axis_from_tangent(tangent)
    pocket = _hex_prism(
        SPEC.nut_trap_across_flats_mm,
        SPEC.nut_trap_depth_mm,
        radial,
        tangent,
        pocket_z0,
    )
    slot = Box(
        SPEC.clamp_outer_radius_mm - radial + 0.6,
        SPEC.nut_insertion_channel_width_mm,
        SPEC.nut_trap_depth_mm,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((radial, tangent, pocket_z0))).rotate(Axis.Z, SPEC.seam_angle_deg)
    return pocket.fuse(slot)


def make_production_quadrant(role_index: int, quadrant_index: int):
    part = deepcopy(make_shifted_base_quadrant(role_index, quadrant_index))
    if quadrant_index == 0:
        part = part.fuse(make_interlock_male(role_index))
        tangent = SPEC.screw_tangential_offsets_mm[0]
    elif quadrant_index == 1:
        part = part.cut(make_interlock_pocket_tool(role_index))
        tangent = SPEC.screw_tangential_offsets_mm[1]
    else:
        part.label = f"{SPEC.roles[role_index]}_Q{quadrant_index + 1}_65T_locked"
        part.color = srgb(SPEC.role_colors[role_index])
        return part
    z0, z1 = SPEC.carrier_layers[role_index]
    part = part.fuse(_receiver_ear(role_index, tangent))
    radial, tangent = _axis_from_tangent(tangent)
    part = part.cut(_local(Cylinder(
        SPEC.screw_clearance_diameter_mm / 2.0,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ), radial, tangent, z0 - 0.2))
    part = part.cut(_nut_pocket_and_outboard_loading_slot(role_index, tangent))
    part.label = f"{SPEC.roles[role_index]}_Q{quadrant_index + 1}_65T_valley_side_loaded_M2_nut"
    part.color = srgb(SPEC.role_colors[role_index])
    return part


def clamp_z(role_index: int) -> tuple[float, float, float, float]:
    z0, z1 = SPEC.carrier_layers[role_index]
    bottom_top = z0 - SPEC.clamp_fit_clearance_per_face_mm
    bottom_bottom = bottom_top - SPEC.clamp_bottom_flange_thickness_mm
    top_bottom = z1 + SPEC.clamp_fit_clearance_per_face_mm
    top_top = top_bottom + SPEC.clamp_top_flange_thickness_mm
    return bottom_bottom, bottom_top, top_bottom, top_top


def make_channel_clamp(role_index: int):
    bottom_bottom, bottom_top, top_bottom, top_top = clamp_z(role_index)
    bottom = _annular_sector(
        SPEC.clamp_inner_radius_mm, SPEC.clamp_outer_radius_mm, SPEC.clamp_tangential_width_mm,
        bottom_bottom, bottom_top,
    )
    top = _annular_sector(
        SPEC.clamp_inner_radius_mm, SPEC.clamp_outer_radius_mm, SPEC.clamp_tangential_width_mm,
        top_bottom, top_top,
    )
    wall = _annular_sector(
        SPEC.clamp_side_wall_inner_radius_mm, SPEC.clamp_outer_radius_mm, SPEC.clamp_tangential_width_mm,
        bottom_bottom, top_top,
    )
    clamp = bottom.fuse(top).fuse(wall).rotate(Axis.Z, SPEC.seam_angle_deg)
    for tangent in SPEC.screw_tangential_offsets_mm:
        radial, tangent = _axis_from_tangent(tangent)
        # The screw ends inside the ring land, so only the top flange needs a bore;
        # the bottom flange stays continuous and flat.
        clamp = clamp.cut(_local(Cylinder(
            SPEC.screw_clearance_diameter_mm / 2.0,
            SPEC.clamp_top_flange_thickness_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_bottom - 0.1))
        # The 90-degree flat head is flush with the top of the 1.20 mm flange.
        countersink = Cone(
            SPEC.screw_clearance_diameter_mm / 2.0,
            SPEC.screw_head_diameter_mm / 2.0,
            SPEC.screw_head_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        clamp = clamp.cut(_local(countersink, radial, tangent, top_bottom))
    clamp.label = f"{SPEC.roles[role_index]}_ONE_PIECE_STACK_SAFE_U_CHANNEL_CLAMP_M2"
    clamp.color = srgb("#AEB5B9")
    return clamp


def make_hardware_references(role_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    z_mid = (z0 + z1) / 2.0
    nut_z0 = z_mid - SPEC.nut_thickness_mm / 2.0
    _, _, top_bottom, top_top = clamp_z(role_index)
    parts = []
    for index, tangent in enumerate(SPEC.screw_tangential_offsets_mm, start=1):
        radial, tangent = _axis_from_tangent(tangent)
        shaft = _local(Cylinder(
            SPEC.screw_nominal_diameter_mm / 2.0,
            SPEC.screw_shank_below_head_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_bottom - SPEC.screw_shank_below_head_mm)
        head = _local(Cone(
            SPEC.screw_nominal_diameter_mm / 2.0,
            SPEC.screw_head_diameter_mm / 2.0,
            SPEC.screw_head_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_bottom)
        screw = shaft.fuse(head)
        screw.label = f"{SPEC.roles[role_index]}_seam_M2x4_flat_head_{index}_REFERENCE"
        screw.color = srgb("#6B7074")
        nut = _hex_prism(
            SPEC.nut_across_flats_mm,
            SPEC.nut_thickness_mm,
            radial,
            tangent,
            nut_z0,
        ).cut(_local(Cylinder(
            SPEC.screw_nominal_diameter_mm / 2.0,
            SPEC.nut_thickness_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, nut_z0 - 0.1))
        nut.label = f"{SPEC.roles[role_index]}_side_loaded_AF4_M2_nut_{index}_REFERENCE"
        nut.color = srgb("#848A8E")
        parts.extend((screw, nut))
    return tuple(parts)


def make_role_seam_module(role_index: int, full_ring: bool = False, include_hardware: bool = True):
    quadrant_range = range(4) if full_ring else range(2)
    parts = [make_production_quadrant(role_index, q) for q in quadrant_range]
    parts.append(make_channel_clamp(role_index))
    if include_hardware:
        parts.extend(make_hardware_references(role_index))
    return Compound(children=parts, label=f"{SPEC.roles[role_index]}_stack_safe_U_channel_M2")


def make_hour_coupon():
    return make_role_seam_module(0, full_ring=False, include_hardware=True)


def make_three_ring_stack(include_hardware: bool = True):
    parts = []
    for role_index in range(3):
        module = make_role_seam_module(role_index, full_ring=True, include_hardware=include_hardware)
        parts.extend(module.children)
    return Compound(children=parts, label="three_ring_stack_with_stack_safe_U_clamps")


def clamp_slide_rows(role_index: int):
    angle = radians(SPEC.seam_angle_deg)
    ux, uy = cos(angle), sin(angle)
    clamp = make_channel_clamp(role_index)
    rows = []
    for index in range(SPEC.slide_sample_count):
        offset = SPEC.slide_start_offset_mm * (SPEC.slide_sample_count - 1 - index) / (SPEC.slide_sample_count - 1)
        rows.append((offset, deepcopy(clamp).moved(Location((ux * offset, uy * offset, 0.0)))))
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
    return Compound(children=[row["shape"] for row in print_layout_rows()], label="hour_stack_safe_U_clamp_M2_print_layout")
