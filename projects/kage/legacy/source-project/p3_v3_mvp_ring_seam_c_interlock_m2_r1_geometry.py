"""Valley-shifted production ring quadrants with planar jigsaw and M2 bridge."""

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

from p3_v3_mvp_ring_seam_c_interlock_m2_r1_spec import (
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
    mask = _sector_mask(-half_angle, half_angle, z0, z1, outer + 0.5)
    pieces = _annulus(inner, outer, z1 - z0, z0).intersect(mask)
    return max(pieces, key=lambda shape: shape.volume)


def _local(shape, radial: float, tangent: float, z: float = 0.0, angle: float | None = None):
    return shape.moved(Location((radial, tangent, z))).rotate(
        Axis.Z, SPEC.coupon_seam_angle_deg if angle is None else angle
    )


def _axis_from_tangent(tangent: float) -> tuple[float, float]:
    return sqrt(SPEC.hardware_axis_global_radius_mm**2 - tangent**2), tangent


def _hex_prism(across_flats: float, height: float, radial: float, tangent: float, z0: float):
    local_radial_angle = degrees(atan2(tangent, radial))
    shape = extrude(RegularPolygon(across_flats / 2.0, 6, major_radius=False), amount=height)
    return shape.rotate(Axis.Z, local_radial_angle - 90.0).moved(
        Location((radial, tangent, z0))
    ).rotate(Axis.Z, SPEC.coupon_seam_angle_deg)


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
    joint_angles = sorted({
        (90.0 * quadrant + edge) % 360.0
        for quadrant in range(4)
        for edge in (1.8, 88.2)
    })
    for angle, diameter, radius in (
        *((a, 2.24, 137.4) for a in joint_angles),
        *((a, 3.04, 137.0) for a in (0.0, 90.0, 180.0, 270.0)),
    ):
        x, y = radius * cos(radians(angle)), radius * sin(radians(angle))
        fill_pieces = Cylinder(diameter / 2.0, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, y, z0))
        ).intersect(carrier)
        if fill_pieces:
            ring = ring.fuse(max(fill_pieces, key=lambda shape: shape.volume))
    ring.label = f"{SPEC.roles[role_index]}_clean_locked_global_260T_ring_reference"
    return ring


@lru_cache(maxsize=12)
def make_shifted_base_quadrant(role_index: int, quadrant_index: int):
    if role_index not in range(3) or quadrant_index not in range(4):
        raise ValueError("role/quadrant outside 3x4 production range")
    z0, z1 = SPEC.carrier_layers[role_index]
    start = SPEC.boundary_angle(quadrant_index)
    mask = _sector_mask(start, start + 90.0, z0 - 0.4, z1 + 25.0)
    pieces = make_clean_locked_full_ring(role_index).intersect(mask)
    if not pieces:
        raise ValueError("shifted 65-pitch quadrant crop produced no solid")
    part = max(pieces, key=lambda shape: shape.volume)
    part.label = f"{SPEC.roles[role_index]}_shifted_valley_Q{quadrant_index + 1}_65T_global_phase_locked"
    part.color = srgb(SPEC.role_colors[role_index])
    return part


def _male_profile_face():
    neck_length = SPEC.interlock_lobe_center_tangent_mm - SPEC.interlock_neck_root_mm / 2.0
    neck_center_y = (SPEC.interlock_lobe_center_tangent_mm - neck_length) / 2.0
    sketch = Rectangle(SPEC.interlock_neck_width_mm, neck_length).moved(
        Location((0.0, neck_center_y, 0.0))
    ) + Circle(SPEC.interlock_lobe_radius_mm).moved(
        Location((0.0, SPEC.interlock_lobe_center_tangent_mm, 0.0))
    )
    face = sketch.faces()[0]
    return face.fillet_2d(SPEC.interlock_root_fillet_mm, face.vertices())


def make_interlock_male(role_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    male = extrude(_male_profile_face(), amount=z1 - z0).moved(
        Location((SPEC.interlock_center_radius_mm, 0.0, z0))
    ).rotate(Axis.Z, SPEC.coupon_seam_angle_deg)
    male.label = f"{SPEC.roles[role_index]}_full_thickness_jigsaw_male_4mm"
    return male


def make_interlock_pocket_tool(role_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    wire = _male_profile_face().outer_wire().offset_2d(
        SPEC.interlock_xy_clearance_per_side_mm, kind=Kind.ARC
    )
    face = Face(wire)
    tool = extrude(face, amount=(z1 - z0) + SPEC.interlock_axial_allowance_mm).moved(
        Location((SPEC.interlock_center_radius_mm, 0.0, z0 - SPEC.interlock_axial_allowance_mm / 2.0))
    ).rotate(Axis.Z, SPEC.coupon_seam_angle_deg)
    tool.label = f"{SPEC.roles[role_index]}_jigsaw_pocket_tool_0p22_per_side"
    return tool


def _receiver_ear(role_index: int, slot_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    tangent = SPEC.role_tangential_offsets_mm[role_index][slot_index]
    radial, tangent = _axis_from_tangent(tangent)
    connector_length = radial - SPEC.receiver_connector_inner_radius_mm + SPEC.receiver_boss_radius_mm
    connector = Box(
        connector_length, SPEC.receiver_connector_tangential_width_mm, z1 - z0,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((SPEC.receiver_connector_inner_radius_mm, tangent, z0)))
    boss = Cylinder(
        SPEC.receiver_boss_radius_mm, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)
    ).moved(Location((radial, tangent, z0)))
    return connector.fuse(boss).rotate(Axis.Z, SPEC.coupon_seam_angle_deg)


def make_production_quadrant(role_index: int, quadrant_index: int):
    if quadrant_index not in (0, 1):
        return deepcopy(make_shifted_base_quadrant(role_index, quadrant_index))
    z0, z1 = SPEC.carrier_layers[role_index]
    part = deepcopy(make_shifted_base_quadrant(role_index, quadrant_index))
    if quadrant_index == 0:
        part = part.fuse(make_interlock_male(role_index))
    else:
        part = part.cut(make_interlock_pocket_tool(role_index))
    part = part.fuse(_receiver_ear(role_index, quadrant_index))
    tangent = SPEC.role_tangential_offsets_mm[role_index][quadrant_index]
    radial, tangent = _axis_from_tangent(tangent)
    hole = _local(
        Cylinder(SPEC.screw_clearance_diameter_mm / 2.0, z1 - z0 + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)),
        radial, tangent, z0 - 0.2,
    )
    trap = _hex_prism(
        SPEC.nut_trap_across_flats_mm, SPEC.nut_trap_depth_mm,
        radial, tangent, z1 - SPEC.nut_trap_depth_mm,
    )
    part = part.cut(hole).cut(trap)
    part.label = f"{SPEC.roles[role_index]}_production_Q{quadrant_index + 1}_65T_valley_C_interlock_M2_r1"
    part.color = srgb(SPEC.role_colors[role_index])
    return part


def make_retention_bridge(role_index: int):
    z0, _ = SPEC.carrier_layers[role_index]
    bridge = _annular_sector(
        SPEC.bridge_inner_radius_mm, SPEC.bridge_outer_radius_mm,
        SPEC.bridge_tangential_width_mm, z0 - SPEC.bridge_thickness_mm, z0,
    )
    pass_tangents = sorted({
        tangent
        for lower_or_self in range(role_index + 1)
        for tangent in SPEC.role_tangential_offsets_mm[lower_or_self]
    })
    for tangent in pass_tangents:
        radial, tangent = _axis_from_tangent(tangent)
        bridge = bridge.cut(Cylinder(
            SPEC.screw_clearance_diameter_mm / 2.0, SPEC.bridge_thickness_mm + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((radial, tangent, z0 - SPEC.bridge_thickness_mm - 0.2))))
    bridge = bridge.rotate(Axis.Z, SPEC.coupon_seam_angle_deg)
    bridge.label = f"{SPEC.roles[role_index]}_localized_underside_retention_bridge_M2x6"
    bridge.color = srgb("#AEB5B9")
    return bridge


def make_hardware_references(role_index: int):
    z0, z1 = SPEC.carrier_layers[role_index]
    parts = []
    for slot_index, tangent in enumerate(SPEC.role_tangential_offsets_mm[role_index]):
        radial, tangent = _axis_from_tangent(tangent)
        head_top = z0 - SPEC.bridge_thickness_mm
        head_bottom = head_top - SPEC.socket_head_height_mm
        shaft = _local(Cylinder(
            SPEC.screw_nominal_diameter_mm / 2.0, SPEC.screw_length_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, head_top)
        head = _local(Cylinder(
            SPEC.socket_head_diameter_mm / 2.0, SPEC.socket_head_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, head_bottom)
        screw = shaft.fuse(head)
        screw.label = f"{SPEC.roles[role_index]}_seam_M2x6_socket_cap_{slot_index + 1}_REFERENCE"
        screw.color = srgb("#6B7074")
        nut = _hex_prism(
            SPEC.nut_across_flats_mm, SPEC.nut_thickness_mm, radial, tangent,
            z1 - SPEC.nut_trap_depth_mm + SPEC.nut_axial_play_mm / 2.0,
        )
        nut = nut.cut(_local(Cylinder(
            SPEC.screw_nominal_diameter_mm / 2.0, SPEC.nut_thickness_mm + 0.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ), radial, tangent, z1 - SPEC.nut_trap_depth_mm + SPEC.nut_axial_play_mm / 2.0 - 0.1))
        nut.label = f"{SPEC.roles[role_index]}_seam_AF4p0_M2_nut_{slot_index + 1}_REFERENCE"
        nut.color = srgb("#848A8E")
        parts.extend((screw, nut))
    return tuple(parts)


def make_role_seam_module(role_index: int, include_hardware: bool = True):
    children = [make_production_quadrant(role_index, 0), make_production_quadrant(role_index, 1), make_retention_bridge(role_index)]
    if include_hardware:
        children.extend(make_hardware_references(role_index))
    return Compound(children=children, label=f"{SPEC.roles[role_index]}_Q1_Q2_valley_C_interlock_M2_r1")


def make_hour_coupon():
    return make_role_seam_module(0, include_hardware=True)


def make_capture_projection(role_index: int = 0):
    z0, z1 = (12.80, 13.80)
    envelope = _annular_sector(
        SPEC.bridge_inner_radius_mm, SPEC.bridge_outer_radius_mm,
        SPEC.bridge_tangential_width_mm, z0, z1,
    ).rotate(Axis.Z, SPEC.coupon_seam_angle_deg)
    envelope.label = "complete_rotating_C_interlock_M2_seam_radial_projection"
    return envelope


def capture_clearance_report():
    _, children = authority()
    capture = children[14:18]
    envelope = make_capture_projection(0)
    distances, intersection = [], 0.0
    for part in capture:
        distances.append(envelope.distance_to(part))
        intersection += _volume(envelope.intersect(part))
    return {
        "bridge_outer_radius_mm": SPEC.bridge_outer_radius_mm,
        "head_outer_radius_mm": SPEC.hardware_axis_global_radius_mm + SPEC.socket_head_diameter_mm / 2.0,
        "trap_outer_radius_mm": SPEC.hardware_axis_global_radius_mm + SPEC.nut_trap_across_flats_mm / 2.0,
        "minimum_actual_capture_clearance_mm": min(distances),
        "intersection_volume_mm3": intersection,
    }


def print_layout_rows():
    shapes = [make_production_quadrant(0, 0), make_production_quadrant(0, 1), make_retention_bridge(0)]
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
    return Compound(children=[row["shape"] for row in print_layout_rows()], label="hour_Q1_Q2_C_interlock_M2_r1_print_layout")
