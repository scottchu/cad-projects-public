"""Locked KAGE ring seam with a real removable three-sided M2 channel clamp."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from math import atan2, cos, degrees, radians, sin, sqrt

from build123d import (
    Align, Axis, Box, Circle, Compound, Cylinder, Face, Kind, Location, Polygon,
    Rectangle, RegularPolygon, extrude, import_step,
)
from cadgen import srgb

from p3_v3_mvp_ring_seam_clamp_m2_r1_spec import (
    LOCKED_STEP, LOCKED_STEP_SHA256, PARITY_JSON, SPEC,
)


def _sha(path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _volume(shape) -> float:
    return sum(s.volume for s in shape.solids()) if shape else 0.0


@lru_cache(maxsize=1)
def authority():
    SPEC.validate()
    if _sha(LOCKED_STEP) != LOCKED_STEP_SHA256:
        raise RuntimeError("locked STEP hash drift")
    parity = json.loads(PARITY_JSON.read_text())
    if parity["locked_step_sha256"] != LOCKED_STEP_SHA256:
        raise RuntimeError("parity manifest authority mismatch")
    assembly = import_step(LOCKED_STEP)
    if len(assembly.children) != 201:
        raise RuntimeError("locked occurrence count drift")
    return parity, tuple(assembly.children)


def _annulus(inner: float, outer: float, height: float, z0: float):
    return Cylinder(outer, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    ).cut(Cylinder(inner, height + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0 - 0.2))
    ))


def _sector_mask(start_deg: float, end_deg: float, z0: float, z1: float, radius: float = 146.0):
    points = [(0.0, 0.0)]
    for index in range(33):
        angle = start_deg + (end_deg - start_deg) * index / 32.0
        points.append((radius * cos(radians(angle)), radius * sin(radians(angle))))
    points.append((0.0, 0.0))
    return extrude(Polygon(*points), amount=z1 - z0).moved(Location((0.0, 0.0, z0)))


def _annular_sector(inner: float, outer: float, tangential_width: float, z0: float, z1: float):
    center = (inner + outer) / 2.0
    half_angle = degrees(tangential_width / (2.0 * center))
    pieces = _annulus(inner, outer, z1 - z0, z0).intersect(
        _sector_mask(-half_angle, half_angle, z0, z1, outer + 0.5)
    )
    return max(pieces, key=lambda shape: shape.volume)


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


@lru_cache(maxsize=3)
def make_clean_locked_full_ring(role_index: int):
    """Rejoin immutable locked occurrences and fill only superseded seam bores."""
    _, children = authority()
    z0, z1 = SPEC.carrier_layers[role_index]
    indices = SPEC.quadrant_occurrence_indices[role_index]
    ring = deepcopy(children[indices[0]])
    for index in indices[1:]:
        ring = ring.fuse(deepcopy(children[index]))
    carrier = _annulus(SPEC.carrier_race_radius_mm, SPEC.carrier_outer_radius_mm, z1 - z0, z0)
    joint_angles = sorted({(90.0 * q + edge) % 360.0 for q in range(4) for edge in (1.8, 88.2)})
    for angle, diameter, radius in (
        *((a, 2.24, 137.4) for a in joint_angles),
        *((a, 3.04, 137.0) for a in (0.0, 90.0, 180.0, 270.0)),
    ):
        fill = Cylinder(diameter / 2.0, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((radius * cos(radians(angle)), radius * sin(radians(angle)), z0))
        ).intersect(carrier)
        if fill:
            ring = ring.fuse(max(fill, key=lambda shape: shape.volume))
    ring.label = f"{SPEC.roles[role_index]}_clean_locked_global_260T_ring_reference"
    return ring


@lru_cache(maxsize=12)
def make_shifted_base_quadrant(role_index: int, quadrant_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    start = SPEC.boundary_angle(quadrant_index)
    pieces = make_clean_locked_full_ring(role_index).intersect(
        _sector_mask(start, start + 90.0, z0 - 0.4, z1 + 25.0)
    )
    part = max(pieces, key=lambda shape: shape.volume)
    part.label = f"{SPEC.roles[role_index]}_valley_Q{quadrant_index + 1}_65T_locked"
    part.color = srgb(SPEC.role_colors[role_index])
    return part


def _male_profile_face():
    neck_length = SPEC.interlock_lobe_center_tangent_mm - SPEC.interlock_neck_root_mm / 2.0
    neck_center_y = (SPEC.interlock_lobe_center_tangent_mm - neck_length) / 2.0
    sketch = Rectangle(SPEC.interlock_neck_width_mm, neck_length).moved(Location((0.0, neck_center_y, 0.0)))
    sketch += Circle(SPEC.interlock_lobe_radius_mm).moved(Location((0.0, SPEC.interlock_lobe_center_tangent_mm, 0.0)))
    face = sketch.faces()[0]
    return face.fillet_2d(SPEC.interlock_root_fillet_mm, face.vertices())


def make_interlock_male(role_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    return extrude(_male_profile_face(), amount=z1 - z0).moved(
        Location((SPEC.interlock_center_radius_mm, 0.0, z0))
    ).rotate(Axis.Z, SPEC.seam_angle_deg)


def make_interlock_pocket_tool(role_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    face = Face(_male_profile_face().outer_wire().offset_2d(SPEC.interlock_xy_clearance_per_side_mm, kind=Kind.ARC))
    return extrude(face, amount=(z1 - z0) + SPEC.interlock_axial_allowance_mm).moved(
        Location((SPEC.interlock_center_radius_mm, 0.0, z0 - SPEC.interlock_axial_allowance_mm / 2.0))
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


def make_production_quadrant(role_index: int, quadrant_index: int):
    part = deepcopy(make_shifted_base_quadrant(role_index, quadrant_index))
    if quadrant_index == 0:
        part = part.fuse(make_interlock_male(role_index))
        tangent = SPEC.screw_tangential_offsets_mm[0]
    elif quadrant_index == 1:
        part = part.cut(make_interlock_pocket_tool(role_index))
        tangent = SPEC.screw_tangential_offsets_mm[1]
    else:
        return part
    z0, z1 = SPEC.carrier_layers[role_index]
    part = part.fuse(_receiver_ear(role_index, tangent))
    radial, tangent = _axis_from_tangent(tangent)
    part = part.cut(_local(Cylinder(
        SPEC.screw_clearance_diameter_mm / 2.0,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ), radial, tangent, z0 - 0.2))
    part.label = f"{SPEC.roles[role_index]}_Q{quadrant_index + 1}_65T_valley_alignment_M2"
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
        # Blind clearance ends above the flat bench datum.
        clamp = clamp.cut(_local(Cylinder(
            SPEC.screw_clearance_diameter_mm / 2.0,
            top_top - bottom_bottom - SPEC.nut_floor_thickness_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, bottom_bottom + SPEC.nut_floor_thickness_mm))
        clamp = clamp.cut(_hex_prism(
            SPEC.nut_trap_across_flats_mm, SPEC.nut_trap_depth_mm,
            radial, tangent, bottom_top - SPEC.nut_trap_depth_mm,
        ))
    clamp.label = f"{SPEC.roles[role_index]}_ONE_PIECE_C_CHANNEL_CLAMP_M2"
    clamp.color = srgb("#AEB5B9")
    return clamp


def make_hardware_references(role_index: int):
    bottom_bottom, bottom_top, _, top_top = clamp_z(role_index)
    parts = []
    for index, tangent in enumerate(SPEC.screw_tangential_offsets_mm, start=1):
        radial, tangent = _axis_from_tangent(tangent)
        shaft = _local(Cylinder(
            SPEC.screw_nominal_diameter_mm / 2.0, SPEC.screw_length_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_top - SPEC.screw_length_mm)
        head = _local(Cylinder(
            SPEC.screw_head_diameter_mm / 2.0, SPEC.screw_head_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, top_top)
        screw = shaft.fuse(head)
        screw.label = f"{SPEC.roles[role_index]}_seam_M2x8_socket_cap_{index}_REFERENCE"
        screw.color = srgb("#6B7074")
        nut = _hex_prism(
            SPEC.nut_across_flats_mm, SPEC.nut_thickness_mm,
            radial, tangent, bottom_top - SPEC.nut_trap_depth_mm,
        ).cut(_local(Cylinder(
            SPEC.screw_nominal_diameter_mm / 2.0, SPEC.nut_thickness_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, bottom_top - SPEC.nut_trap_depth_mm - 0.1))
        nut.label = f"{SPEC.roles[role_index]}_captive_AF4_M2_nut_{index}_REFERENCE"
        nut.color = srgb("#848A8E")
        parts.extend((screw, nut))
    return tuple(parts)


def make_role_seam_module(role_index: int, include_hardware: bool = True):
    parts = [make_production_quadrant(role_index, 0), make_production_quadrant(role_index, 1), make_channel_clamp(role_index)]
    if include_hardware:
        parts.extend(make_hardware_references(role_index))
    return Compound(children=parts, label=f"{SPEC.roles[role_index]}_Q1_Q2_C_channel_clamp_M2")


def make_hour_coupon():
    return make_role_seam_module(0, include_hardware=True)


def capture_clearance_report():
    _, children = authority()
    capture = children[14:18]
    clamp = make_channel_clamp(0)
    return {
        "clamp_outer_radius_mm": SPEC.clamp_outer_radius_mm,
        "minimum_actual_capture_clearance_mm": min(clamp.distance_to(part) for part in capture),
        "intersection_volume_mm3": sum(_volume(clamp.intersect(part)) for part in capture),
    }


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
    return Compound(children=[row["shape"] for row in print_layout_rows()], label="hour_Q1_Q2_C_channel_clamp_M2_print_layout")
