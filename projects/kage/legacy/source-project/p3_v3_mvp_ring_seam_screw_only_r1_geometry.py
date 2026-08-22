"""Localized screw-only seam geometry derived from the immutable locked STEP."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from math import atan2, cos, degrees, radians, sin, sqrt

from build123d import (
    Align, Axis, Box, Compound, Cylinder, Location, Polygon, RegularPolygon,
    extrude, import_step,
)
from cadgen import srgb

from p3_v3_mvp_ring_seam_screw_only_r1_spec import LOCKED_STEP, LOCKED_STEP_SHA256, PARITY_JSON, SPEC


def _sha(path) -> str:
    return sha256(path.read_bytes()).hexdigest()


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


def _annular_sector(inner: float, outer: float, tangential_width: float, z0: float, z1: float):
    center = (inner + outer) / 2.0
    half_angle = degrees(tangential_width / (2.0 * center))
    radius = outer + 0.5
    points = [(0.0, 0.0)]
    for index in range(13):
        angle = -half_angle + 2.0 * half_angle * index / 12.0
        points.append((radius * cos(radians(angle)), radius * sin(radians(angle))))
    points.append((0.0, 0.0))
    mask = extrude(Polygon(*points), amount=z1 - z0).moved(Location((0.0, 0.0, z0)))
    pieces = _annulus(inner, outer, z1 - z0, z0).intersect(mask)
    return max(pieces, key=lambda shape: shape.volume)


def _local(shape, x: float, tangent: float, z: float = 0.0):
    return shape.moved(Location((x, tangent, z))).rotate(Axis.Z, SPEC.seam_angle_deg)


def _axis_local(role_index: int, slot_index: int) -> tuple[float, float]:
    tangent = SPEC.role_tangential_offsets_mm[role_index][slot_index]
    radial = sqrt(SPEC.hardware_axis_global_radius_mm**2 - tangent**2)
    return radial, tangent


def _axis_from_tangent(tangent: float) -> tuple[float, float]:
    return sqrt(SPEC.hardware_axis_global_radius_mm**2 - tangent**2), tangent


def _hex_prism(across_flats: float, height: float, x: float, tangent: float, z0: float):
    # build123d's unrotated AF hex has flats normal to Y. Rotate its flat to
    # the exact global radial direction before placing it.
    local_radial_angle = degrees(atan2(tangent, x))
    shape = extrude(RegularPolygon(across_flats / 2.0, 6, major_radius=False), amount=height)
    return shape.rotate(Axis.Z, local_radial_angle - 90.0).moved(
        Location((x, tangent, z0))
    ).rotate(Axis.Z, SPEC.seam_angle_deg)


def source_quadrant(role_index: int, quadrant_index: int):
    _, children = authority()
    index = SPEC.quadrant_occurrence_indices[role_index][quadrant_index]
    return deepcopy(children[index])


def _quadrant_crop(quadrant_index: int, z0: float, z1: float):
    size = SPEC.pad_outer_radius_mm + 1.0
    return Box(size, size, z1 - z0 + 0.4, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((0.0, 0.0, z0 - 0.2))
    ).rotate(Axis.Z, 90.0 * quadrant_index)


def _legacy_fill(quadrant_index: int, z0: float, z1: float):
    carrier = _annulus(SPEC.tooth_root_radius_mm, SPEC.carrier_outer_radius_mm, z1 - z0, z0)
    crop = _quadrant_crop(quadrant_index, z0, z1)
    fills = []
    for radius, angle, diameter in (
        (137.4, 88.2, 2.20), (137.4, 91.8, 2.20), (137.0, 90.0, 3.00),
    ):
        x, y = radius * cos(radians(angle)), radius * sin(radians(angle))
        tool = Cylinder(diameter / 2.0 + 0.02, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, y, z0))
        )
        for piece in tool.intersect(carrier):
            clipped = piece.intersect(crop)
            if clipped:
                fills.extend(clipped)
    return fills


def _receiver_boss(role_index: int, slot_index: int, z0: float, z1: float):
    x, tangent = _axis_local(role_index, slot_index)
    raw = _local(
        Cylinder(SPEC.receiver_boss_radius_mm, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)),
        x, tangent, z0,
    )
    limiter = _annulus(SPEC.pad_inner_radius_mm, SPEC.pad_outer_radius_mm, z1 - z0, z0)
    pieces = raw.intersect(limiter)
    return max(pieces, key=lambda shape: shape.volume)


def _registration_pocket(quadrant_index: int, z0: float):
    tangent = SPEC.registration_tangential_offsets_mm[quadrant_index]
    return _local(
        Box(
            SPEC.pocket_radial_mm, SPEC.pocket_tangential_mm, SPEC.pocket_depth_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ),
        SPEC.registration_radius_mm, tangent, z0,
    )


def make_modified_quadrant(role_index: int, quadrant_index: int):
    if quadrant_index not in (0, 1):
        raise ValueError("coupon contains only adjacent Q1/Q2")
    z0, z1 = SPEC.carrier_layers[role_index]
    part = source_quadrant(role_index, quadrant_index)
    for fill in _legacy_fill(quadrant_index, z0, z1):
        part = part.fuse(fill)
    part = part.fuse(_receiver_boss(role_index, quadrant_index, z0, z1))
    x, tangent = _axis_local(role_index, quadrant_index)
    screw_hole = _local(
        Cylinder(SPEC.screw_clearance_diameter_mm / 2.0, z1 - z0 + 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)),
        x, tangent, z0 - 0.2,
    )
    trap = _hex_prism(SPEC.nut_trap_across_flats_mm, SPEC.nut_trap_depth_mm, x, tangent, z0)
    part = part.cut(screw_hole).cut(trap).cut(_registration_pocket(quadrant_index, z0))
    part.label = f"{SPEC.roles[role_index]}_locked_65T_Q{quadrant_index + 1}_screw_only_r1"
    part.color = srgb(("#3F8F87", "#E38B48", "#D95D78")[role_index])
    return part


def make_outboard_pad(role_index: int):
    z0, _ = SPEC.carrier_layers[role_index]
    pad = _annular_sector(
        SPEC.pad_inner_radius_mm, SPEC.pad_outer_radius_mm,
        SPEC.pad_tangential_width_mm, z0 - SPEC.pad_thickness_mm, z0,
    )
    for tangent in SPEC.registration_tangential_offsets_mm:
        tab = Box(5.50, 6.50, SPEC.pad_thickness_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((SPEC.registration_radius_mm, tangent, z0 - SPEC.pad_thickness_mm))
        )
        shoulder = Box(
            SPEC.shoulder_radial_mm, SPEC.shoulder_tangential_mm, SPEC.shoulder_height_mm,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((SPEC.registration_radius_mm, tangent, z0)))
        pad = pad.fuse(tab).fuse(shoulder)
    # The long screw of each lower role traverses the next outboard pad's Z
    # band. Role staggering keeps these apertures distinct from this pad's own
    # fasteners; repeated tangential positions are cut only once.
    pass_through_tangents = sorted({
        tangent
        for lower_or_self_role in range(role_index + 1)
        for tangent in SPEC.role_tangential_offsets_mm[lower_or_self_role]
    })
    for tangent in pass_through_tangents:
        x, tangent = _axis_from_tangent(tangent)
        hole = Cylinder(
            SPEC.screw_clearance_diameter_mm / 2.0,
            SPEC.pad_thickness_mm + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, tangent, z0 - SPEC.pad_thickness_mm - 0.2)))
        pad = pad.cut(hole)
    pad = pad.rotate(Axis.Z, SPEC.seam_angle_deg)
    pad.label = f"{SPEC.roles[role_index]}_screw_only_outboard_splice_pad_two_shoulders"
    pad.color = srgb("#AEB5B9")
    return pad


def make_hardware_references(role_index: int):
    z0, _ = SPEC.carrier_layers[role_index]
    parts = []
    for slot_index in range(2):
        x, tangent = _axis_local(role_index, slot_index)
        head_top = z0 - SPEC.pad_thickness_mm
        head_bottom = head_top - SPEC.socket_head_height_mm
        shaft = _local(
            Cylinder(SPEC.screw_nominal_diameter_mm / 2.0, SPEC.screw_length_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)),
            x, tangent, head_top,
        )
        head = _local(
            Cylinder(SPEC.socket_head_diameter_mm / 2.0, SPEC.socket_head_height_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)),
            x, tangent, head_bottom,
        )
        screw = shaft.fuse(head)
        screw.label = f"{SPEC.roles[role_index]}_seam_M3x8_socket_cap_{slot_index + 1}_REFERENCE"
        screw.color = srgb("#6B7074")
        nut = _hex_prism(
            SPEC.nut_across_flats_mm, SPEC.nut_thickness_mm,
            x, tangent, z0 + SPEC.nut_axial_play_mm / 2.0,
        )
        nut.label = f"{SPEC.roles[role_index]}_seam_AF5p5_M3_nut_{slot_index + 1}_REFERENCE"
        nut.color = srgb("#848A8E")
        parts.extend((screw, nut))
    return tuple(parts)


def make_role_seam_module(role_index: int, *, include_hardware: bool = True):
    children = [make_modified_quadrant(role_index, 0), make_modified_quadrant(role_index, 1), make_outboard_pad(role_index)]
    if include_hardware:
        children.extend(make_hardware_references(role_index))
    return Compound(children=children, label=f"{SPEC.roles[role_index]}_Q1_Q2_screw_only_seam_module")


def make_hour_coupon():
    return make_role_seam_module(0, include_hardware=True)


def make_capture_projection(role_index: int = 0):
    z0, z1 = (12.80, 13.80)
    envelope = _annular_sector(
        SPEC.pad_inner_radius_mm, SPEC.pad_outer_radius_mm,
        SPEC.pad_tangential_width_mm, z0, z1,
    ).rotate(Axis.Z, SPEC.seam_angle_deg)
    for slot_index in range(2):
        x, tangent = _axis_local(role_index, slot_index)
        envelope = envelope.fuse(_local(
            Cylinder(SPEC.socket_head_diameter_mm / 2.0, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)),
            x, tangent, z0,
        ))
    envelope.label = "conservative_complete_rotating_seam_radial_projection"
    return envelope


def capture_clearance_report() -> dict[str, float]:
    _, children = authority()
    capture = children[14:18]
    envelope = make_capture_projection(0)
    distances, intersection = [], 0.0
    for part in capture:
        distances.append(envelope.distance_to(part))
        hit = envelope.intersect(part)
        intersection += sum(s.volume for s in hit.solids()) if hit else 0.0
    return {
        "head_outer_radius_mm": SPEC.hardware_axis_global_radius_mm + SPEC.socket_head_diameter_mm / 2.0,
        "trap_outer_radius_mm": SPEC.hardware_axis_global_radius_mm + SPEC.nut_trap_across_flats_mm / 2.0,
        "pad_outer_radius_mm": SPEC.pad_outer_radius_mm,
        "minimum_actual_capture_clearance_mm": min(distances),
        "intersection_volume_mm3": intersection,
    }


def print_layout_rows():
    shapes = [make_modified_quadrant(0, 0), make_modified_quadrant(0, 1), make_outboard_pad(0)]
    targets = ((5.0, 5.0), (110.0, 110.0), (230.0, 10.0))
    rows = []
    for shape, (x, y) in zip(shapes, targets, strict=True):
        box = shape.bounding_box()
        moved = deepcopy(shape).moved(Location((x - box.min.X, y - box.min.Y, -box.min.Z)))
        moved.label = shape.label
        rows.append({"source": shape, "shape": moved, "translation_mm": (x - box.min.X, y - box.min.Y, -box.min.Z)})
    return tuple(rows)


def make_print_layout():
    return Compound(children=[row["shape"] for row in print_layout_rows()], label="hour_Q1_Q2_screw_only_r1_print_layout")
