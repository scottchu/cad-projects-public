"""Actual Boolean geometry for the isolated I3-R1 localized repair."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from math import cos, radians, sin
from typing import Any, Iterable

from build123d import Align, Axis, Box, Compound, Cylinder, Location

from p3_v3_locked_parametric_repair_r1_i1_geometry import candidate_occurrence_shapes
from p3_v3_locked_parametric_repair_r1_i1_spec import P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
from p3_v3_phase3_i3_r1_real_joinery_spec import (
    ARTIFACT_CONTRACT,
    MOVING_JOINERY,
    SEGMENTATION,
    STATIONARY_GROUPS,
    MovingJoinery,
    Segmentation,
    StationaryJoinery,
)


ROLES = ("hour", "minute", "second")
STATIONARY_FAMILIES = ("rear_chassis", "stationary_frame", "outer_front_ring")
ROLE_SOURCE_INDICES = {"hour": range(108, 112), "minute": range(139, 143), "second": range(170, 174)}
STATIONARY_SOURCE_INDICES = {"rear_chassis": range(0, 4), "stationary_frame": range(4, 8), "outer_front_ring": range(14, 18)}
_REPLACED_INDICES = set(range(0, 8)) | set(range(14, 18))
for _start in (108, 139, 170):
    _REPLACED_INDICES.update(range(_start, _start + 20))


def volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids())) if shape is not None else 0.0


def intersection_volume(a, b) -> float:
    return volume(deepcopy(a).intersect(deepcopy(b)))


@lru_cache(maxsize=1)
def baseline_rows() -> tuple[tuple[str, Any], ...]:
    return tuple(candidate_occurrence_shapes(P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1))


def _source(indices: Iterable[int]) -> Compound:
    rows = dict(baseline_rows())
    return Compound(children=[deepcopy(rows[f"occurrence_{index:03d}"]) for index in indices])


def _half_space(angle_start_deg: float, segmentation: Segmentation = SEGMENTATION):
    return Box(
        segmentation.sector_mask_radius_mm,
        segmentation.sector_mask_radius_mm * 2.0,
        segmentation.sector_mask_height_mm,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, -segmentation.sector_mask_height_mm / 2.0))).rotate(
        Axis.Z, angle_start_deg + 90.0
    )


def _quadrant_space(angle_start_deg: float, segmentation: Segmentation = SEGMENTATION):
    return Box(
        segmentation.sector_mask_radius_mm,
        segmentation.sector_mask_radius_mm,
        segmentation.sector_mask_height_mm,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((0.0, 0.0, -segmentation.sector_mask_height_mm / 2.0))).rotate(Axis.Z, angle_start_deg)


def _clip_children(source: Compound, mask) -> Compound:
    children = []
    for child in source.children:
        result = deepcopy(child).intersect(mask)
        for candidate in result if isinstance(result, list) else [result]:
            if volume(candidate) > 1e-8:
                children.append(candidate)
    return Compound(children=children)


def local_point(angle_deg: float, radius_mm: float, tangent_mm: float) -> tuple[float, float]:
    angle = radians(angle_deg)
    return (
        radius_mm * cos(angle) - tangent_mm * sin(angle),
        radius_mm * sin(angle) + tangent_mm * cos(angle),
    )


def tangent_box(angle_deg: float, radius_mm: float, radial_mm: float, tangent_mm: float, z0: float, height: float):
    x, y = local_point(angle_deg, radius_mm, 0.0)
    return Box(radial_mm, tangent_mm, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Z, angle_deg
    ).moved(Location((x, y, z0)))


def local_box(angle_deg: float, radius_mm: float, tangent_mm: float, radial_size: float, tangent_size: float, z0: float, height: float):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    return Box(radial_size, tangent_size, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).rotate(
        Axis.Z, angle_deg
    ).moved(Location((x, y, z0)))


def vertical_cylinder(angle_deg: float, radius_mm: float, tangent_mm: float, diameter_mm: float, z0: float, height: float):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    return Cylinder(diameter_mm / 2.0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))


def _cut(shape, tools: Iterable[Any]):
    result = deepcopy(shape)
    for tool in tools:
        result = result.cut(deepcopy(tool))
    return result


def _fuse(shape, additions: Iterable[Any]):
    result = deepcopy(shape)
    for addition in additions:
        result = result.fuse(deepcopy(addition))
    return result


def moving_seam_tools(role: str, angle_deg: float, moving: MovingJoinery = MOVING_JOINERY) -> dict[str, Any]:
    z0, z1 = moving.z_for(role)
    roi = tangent_box(
        angle_deg,
        moving.radial_mid_mm,
        moving.radial_span_mm,
        moving.tangent_half_mm * 2.0,
        z0 - 0.25,
        (z1 - z0) + 0.58,
    )
    lower_lap = tangent_box(
        angle_deg, moving.radial_mid_mm, moving.radial_span_mm,
        moving.tangent_half_mm * 2.0, z0, moving.half_a_lap_mm,
    )
    upper_lap = tangent_box(
        angle_deg, moving.radial_mid_mm, moving.radial_span_mm,
        moving.tangent_half_mm * 2.0, z0 + moving.half_a_lap_mm + moving.axial_gap_mm,
        moving.half_b_lap_mm,
    )
    screw_bores = [
        vertical_cylinder(
            angle_deg, moving.screw_axis_radius_mm, tangent,
            moving.screw_clearance_diameter_mm, z0 - 0.25, (z1 - z0) + 0.66,
        )
        for tangent in (-moving.screw_tangent_mm, moving.screw_tangent_mm)
    ]
    nut_pockets = [
        local_box(
            angle_deg, moving.screw_axis_radius_mm, tangent,
            moving.nut_pocket_radial_mm, moving.nut_pocket_tangent_mm,
            z0 + moving.rear_skin_mm, moving.nut_pocket_height_mm,
        )
        for tangent in (-moving.screw_tangent_mm, moving.screw_tangent_mm)
    ]
    press_bore = vertical_cylinder(
        angle_deg, moving.screw_axis_radius_mm, 0.0, moving.press_bore_diameter_mm,
        z0, moving.half_a_lap_mm,
    )
    slip_bore = vertical_cylinder(
        angle_deg, moving.screw_axis_radius_mm, 0.0, moving.slip_bore_diameter_mm,
        z0 + moving.half_a_lap_mm + moving.axial_gap_mm, moving.half_b_lap_mm,
    )
    return {
        "roi": roi,
        "lower_lap": lower_lap,
        "upper_lap": upper_lap,
        "screw_bores": screw_bores,
        "nut_pockets": nut_pockets,
        "press_bore": press_bore,
        "slip_bore": slip_bore,
    }


@lru_cache(maxsize=1)
def plain_moving_half_shapes() -> dict[tuple[str, str], Any]:
    result = {}
    for role in ROLES:
        source = _source(ROLE_SOURCE_INDICES[role])
        result[(role, "A")] = _clip_children(source, _half_space(SEGMENTATION.moving_seams_deg[0]))
        result[(role, "B")] = _clip_children(source, _half_space(SEGMENTATION.moving_seams_deg[1]))
    return result


@lru_cache(maxsize=1)
def moving_half_shapes() -> dict[tuple[str, str], Any]:
    result: dict[tuple[str, str], Any] = {}
    for role in ROLES:
        half_a = deepcopy(plain_moving_half_shapes()[(role, "A")])
        half_b = deepcopy(plain_moving_half_shapes()[(role, "B")])
        for angle in SEGMENTATION.moving_seams_deg:
            tools = moving_seam_tools(role, angle)
            half_a = _fuse(_cut(half_a, [tools["roi"]]), [tools["lower_lap"]])
            half_a = _cut(half_a, [*tools["screw_bores"], *tools["nut_pockets"], tools["press_bore"]])
            half_b = _fuse(_cut(half_b, [tools["roi"]]), [tools["upper_lap"]])
            half_b = _cut(half_b, [*tools["screw_bores"], tools["slip_bore"]])
        half_a.label = f"p3_v3_direct_race_{role}_M1_260T_I3_R1_half_A_130T_beta15p230769"
        half_b.label = f"p3_v3_direct_race_{role}_M1_260T_I3_R1_half_B_130T_beta195p230769"
        result[(role, "A")] = half_a
        result[(role, "B")] = half_b
    return result


def _stationary_tools(group: StationaryJoinery, angle_deg: float, radius_mm: float) -> dict[str, Any]:
    bridge = tangent_box(
        angle_deg, radius_mm, group.bridge_radial_mm, group.bridge_tangent_mm,
        group.bridge_z_mm[0], group.bridge_height_mm,
    )
    screw_bores = [
        vertical_cylinder(
            angle_deg, radius_mm, tangent, group.screw_clearance_diameter_mm,
            group.bridge_z_mm[0] - 0.2,
            group.member_z_mm[1] - group.bridge_z_mm[0] + 0.4,
        )
        for tangent in (-group.screw_tangent_mm, group.screw_tangent_mm)
    ]
    nut_pockets = [
        local_box(
            angle_deg, radius_mm, tangent,
            group.nut_pocket_side_mm, group.nut_pocket_side_mm,
            group.bridge_z_mm[0] + 0.2, group.nut_pocket_height_mm,
        )
        for tangent in (-group.screw_tangent_mm, group.screw_tangent_mm)
    ]
    press_bore = vertical_cylinder(
        angle_deg, radius_mm, 0.0, group.press_bore_diameter_mm,
        group.press_z_mm[0], group.press_z_mm[1] - group.press_z_mm[0],
    )
    slip_bore = vertical_cylinder(
        angle_deg, radius_mm, 0.0, group.slip_bore_diameter_mm,
        group.slip_z_mm[0], group.slip_z_mm[1] - group.slip_z_mm[0],
    )
    return {"bridge": bridge, "screw_bores": screw_bores, "nut_pockets": nut_pockets, "press_bore": press_bore, "slip_bore": slip_bore}


@lru_cache(maxsize=1)
def stationary_quadrant_shapes() -> dict[tuple[str, int], Any]:
    result: dict[tuple[str, int], Any] = {}
    for family in STATIONARY_FAMILIES:
        group = STATIONARY_GROUPS[family]
        source = _source(STATIONARY_SOURCE_INDICES[family])
        for quadrant in range(1, 5):
            angle = SEGMENTATION.stationary_seams_deg[quadrant - 1]
            shape = _clip_children(source, _quadrant_space(angle))
            # Every seam tool is subtracted from every quadrant; only the two
            # adjacent real solids are affected by each Boolean operation.
            for seam_angle in SEGMENTATION.stationary_seams_deg:
                for radius in group.bridge_radii_mm:
                    tools = _stationary_tools(group, seam_angle, radius)
                    shape = _cut(shape, [*tools["screw_bores"], tools["slip_bore"]])
            shape.label = f"{family}_I3_R1_beta37p5_quadrant_Q{quadrant}"
            result[(family, quadrant)] = shape
    return result


@lru_cache(maxsize=1)
def stationary_bridge_shapes() -> dict[tuple[str, int, int], Any]:
    result = {}
    for family in STATIONARY_FAMILIES:
        group = STATIONARY_GROUPS[family]
        for seam_index, angle in enumerate(SEGMENTATION.stationary_seams_deg, start=1):
            for bridge_index, radius in enumerate(group.bridge_radii_mm, start=1):
                tools = _stationary_tools(group, angle, radius)
                bridge = _cut(tools["bridge"], [*tools["screw_bores"], *tools["nut_pockets"], tools["press_bore"]])
                bridge.label = f"i3_r1_{family}_seam_{seam_index:02d}_bridge_{bridge_index:02d}"
                result[(family, seam_index, bridge_index)] = bridge
    return result


def _purchased(shape, label: str, kind: str) -> dict[str, Any]:
    shape.label = label
    return {"label": label, "shape": shape, "kind": kind, "classification": "purchased", "printable": False}


@lru_cache(maxsize=1)
def purchased_hardware_rows() -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    moving = MOVING_JOINERY
    for role in ROLES:
        z0, z1 = moving.z_for(role)
        for seam_index, angle in enumerate(SEGMENTATION.moving_seams_deg, start=1):
            for side_index, tangent in enumerate((-moving.screw_tangent_mm, moving.screw_tangent_mm), start=1):
                thread = vertical_cylinder(angle, moving.screw_axis_radius_mm, tangent, 2.0, z0, 3.0)
                head = vertical_cylinder(angle, moving.screw_axis_radius_mm, tangent, 4.4, z1, 1.0)
                rows.append(_purchased(thread.fuse(head), f"i3_r1_{role}_seam_{seam_index}_M2x3_screw_{side_index}", "screw"))
                nut = local_box(
                    angle, moving.screw_axis_radius_mm, tangent,
                    moving.nut_body_side_mm, moving.nut_body_side_mm,
                    z0 + moving.rear_skin_mm + 0.05, moving.nut_body_height_mm,
                )
                rows.append(_purchased(nut, f"i3_r1_{role}_seam_{seam_index}_DIN562_M2_nut_{side_index}", "nut"))
            pin = vertical_cylinder(angle, moving.screw_axis_radius_mm, 0.0, moving.pin_diameter_mm, z0, moving.pin_length_mm)
            rows.append(_purchased(pin, f"i3_r1_{role}_seam_{seam_index}_D3x3_pin", "dowel"))
    for family in STATIONARY_FAMILIES:
        group = STATIONARY_GROUPS[family]
        for seam_index, angle in enumerate(SEGMENTATION.stationary_seams_deg, start=1):
            for bridge_index, radius in enumerate(group.bridge_radii_mm, start=1):
                for side_index, tangent in enumerate((-group.screw_tangent_mm, group.screw_tangent_mm), start=1):
                    screw_z0 = group.bridge_z_mm[0]
                    screw = vertical_cylinder(angle, radius, tangent, group.screw_diameter_mm, screw_z0, group.screw_length_mm)
                    rows.append(_purchased(screw, f"i3_r1_{family}_seam_{seam_index}_bridge_{bridge_index}_screw_{side_index}", "screw"))
                    nut = local_box(
                        angle, radius, tangent, group.nut_side_mm, group.nut_side_mm,
                        group.bridge_z_mm[0] + 0.25, group.nut_height_mm,
                    )
                    rows.append(_purchased(nut, f"i3_r1_{family}_seam_{seam_index}_bridge_{bridge_index}_nut_{side_index}", "nut"))
                pin_z0 = group.press_z_mm[0]
                pin = vertical_cylinder(angle, radius, 0.0, group.dowel_diameter_mm, pin_z0, group.dowel_length_mm)
                rows.append(_purchased(pin, f"i3_r1_{family}_seam_{seam_index}_bridge_{bridge_index}_dowel", "dowel"))
    return tuple(rows)


def moving_joinery_actual_brep_evidence() -> list[dict[str, Any]]:
    rows = []
    shapes = moving_half_shapes()
    for role in ROLES:
        for half in ("A", "B"):
            plain = plain_moving_half_shapes()[(role, half)]
            actual = shapes[(role, half)]
            added = volume(actual.cut(plain))
            removed = volume(plain.cut(actual))
            rows.append({"role": role, "half": half, "lap_added_volume_mm3": added, "cut_volume_mm3": removed, "actual_volume_mm3": volume(actual)})
    return rows


def front_ring_joinery_measurements() -> dict[str, float]:
    group = STATIONARY_GROUPS["outer_front_ring"]
    bridge = stationary_bridge_shapes()[("outer_front_ring", 1, 1)]
    return {
        "bridge_thickness_mm": bridge.bounding_box().size.Z,
        "dowel_nominal_diameter_mm": group.dowel_diameter_mm,
    }


@lru_cache(maxsize=1)
def candidate_occurrences_cached() -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for name, shape in baseline_rows():
        if name.startswith("occurrence_") and int(name.rsplit("_", 1)[1]) in _REPLACED_INDICES:
            continue
        rows.append({"name": name, "label": str(shape.label), "shape": shape, "classification": "protected_exact", "printable": False})
    for role in ROLES:
        for half in ("A", "B"):
            shape = moving_half_shapes()[(role, half)]
            rows.append({"name": f"i3_r1_{role}_half_{half}", "label": shape.label, "shape": shape, "classification": "authorized_replacement", "printable": True})
    for family in STATIONARY_FAMILIES:
        for quadrant in range(1, 5):
            shape = stationary_quadrant_shapes()[(family, quadrant)]
            rows.append({"name": f"i3_r1_{family}_Q{quadrant}", "label": shape.label, "shape": shape, "classification": "authorized_replacement", "printable": True})
    for shape in stationary_bridge_shapes().values():
        rows.append({"name": shape.label, "label": shape.label, "shape": shape, "kind": "bridge", "classification": "new_authorized", "printable": True})
    for row in purchased_hardware_rows():
        rows.append({"name": row["label"], **row, "classification": "new_authorized"})
    counts = {key: sum(row["classification"] == key for row in rows) for key in ("protected_exact", "authorized_replacement", "new_authorized")}
    expected = {"protected_exact": 131, "authorized_replacement": 18, "new_authorized": 126}
    if counts != expected or len(rows) != ARTIFACT_CONTRACT.registry_count:
        raise RuntimeError(f"I3-R1 registry mismatch {counts}, total={len(rows)}")
    return tuple(rows)


def candidate_occurrences() -> list[dict[str, Any]]:
    return [dict(row) for row in candidate_occurrences_cached()]


def printable_occurrences() -> list[dict[str, Any]]:
    return [row for row in candidate_occurrences() if row.get("printable")]


def assembled_shape() -> Compound:
    return Compound(children=[row["shape"] for row in candidate_occurrences()], label="KAGE_P3_V3_I3_R1_REAL_JOINERY")


def service_exploded_shape() -> Compound:
    children = []
    for index, row in enumerate(candidate_occurrences()):
        shape = deepcopy(row["shape"])
        if row["classification"] == "authorized_replacement":
            shape = shape.moved(Location((0.0, 0.0, 25.0 + 2.0 * (index % 6))))
        elif row["classification"] == "new_authorized":
            shape = shape.moved(Location((0.0, 0.0, 65.0)))
        children.append(shape)
    return Compound(children=children, label="KAGE_P3_V3_I3_R1_SERVICE_EXPLODED")
