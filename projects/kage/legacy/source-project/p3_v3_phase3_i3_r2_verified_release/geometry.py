"""Localized actual-BREP geometry for KAGE I3-R2 Checkpoint A.

The locked I1 source ring BREPs are intersected with the accepted half-space
masks.  R2 then applies two real, owner-driven repairs: Half-B-only expanded
receiving cavities and symmetric exterior butt-face relief outside the lap
band.  No rejected R1 geometry function is imported.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from math import cos, radians, sin
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Iterable

from build123d import Align, Axis, Box, Compound, Cylinder, Location, export_brep

from p3_v3_locked_parametric_repair_r1_i1_geometry import candidate_occurrence_shapes
from p3_v3_locked_parametric_repair_r1_i1_spec import P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1

from .spec import OwnerBundle


ROLES = ("hour", "minute", "second")
ROLE_SOURCE_INDICES = {
    "hour": range(108, 112),
    "minute": range(139, 143),
    "second": range(170, 174),
}
REPLACED_BASELINE_INDICES = frozenset(
    tuple(range(0, 8))
    + tuple(range(14, 18))
    + tuple(range(108, 128))
    + tuple(range(139, 159))
    + tuple(range(170, 190))
)


def volume(shape) -> float:
    if shape is None:
        return 0.0
    if not hasattr(shape, "solids"):
        shape = Compound(children=list(shape))
    return float(sum(solid.volume for solid in shape.solids()))


def _as_shape(result):
    if result is None:
        return Compound(children=[])
    if hasattr(result, "wrapped"):
        return result
    return Compound(children=list(result))


def intersection(left, right):
    return _as_shape(deepcopy(left).intersect(deepcopy(right)))


def intersection_volume(left, right) -> float:
    return volume(intersection(left, right))


def brep_digest(shape) -> str:
    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return sha256(Path(temporary.name).read_bytes()).hexdigest()


def semantic_shape_facts(shape) -> dict[str, Any]:
    bounds = shape.bounding_box()
    topology = {
        name: len(getattr(shape, name)())
        for name in ("vertices", "edges", "wires", "faces", "shells", "solids", "compounds")
    }
    position, orientation = shape.location.to_tuple()
    return {
        "transform": [float(value) for value in (*position, *orientation)],
        "topology": topology,
        "aabb_mm": [
            float(bounds.min.X), float(bounds.min.Y), float(bounds.min.Z),
            float(bounds.max.X), float(bounds.max.Y), float(bounds.max.Z),
        ],
        "area_mm2": float(shape.area),
        "volume_mm3": volume(shape),
        "brep_sha256": brep_digest(shape),
    }


@lru_cache(maxsize=1)
def baseline_rows() -> tuple[tuple[str, Any], ...]:
    return tuple(candidate_occurrence_shapes(P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1))


def protected_occurrence_rows() -> tuple[tuple[str, Any], ...]:
    rows = []
    for name, shape in baseline_rows():
        if name.startswith("i1_new_tower_"):
            rows.append((name, shape))
            continue
        if not name.startswith("occurrence_"):
            continue
        index = int(name.rsplit("_", 1)[1])
        if index not in REPLACED_BASELINE_INDICES:
            rows.append((name, shape))
    if len(rows) != 131:
        raise RuntimeError(f"R2 protected partition is {len(rows)}, expected 131")
    return tuple(rows)


def protected_occurrence_facts() -> tuple[dict[str, Any], ...]:
    return tuple(
        {"name": name, **semantic_shape_facts(shape)}
        for name, shape in protected_occurrence_rows()
    )


def _source(indices: Iterable[int]) -> Compound:
    rows = dict(baseline_rows())
    return Compound(children=[deepcopy(rows[f"occurrence_{index:03d}"]) for index in indices])


def _half_space(angle_start_deg: float, owners: OwnerBundle):
    segmentation = owners.segmentation
    return Box(
        segmentation.sector_mask_radius_mm,
        segmentation.sector_mask_radius_mm * 2.0,
        segmentation.sector_mask_height_mm,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(
        Location((0.0, 0.0, -segmentation.sector_mask_height_mm / 2.0))
    ).rotate(Axis.Z, angle_start_deg + 90.0)


def _clip_children(source: Compound, mask) -> Compound:
    children = []
    for child in source.children:
        result = intersection(child, mask)
        for candidate in result.solids():
            if volume(candidate) > 1e-8:
                children.append(candidate)
    return Compound(children=children)


def local_point(angle_deg: float, radius_mm: float, tangent_mm: float) -> tuple[float, float]:
    angle = radians(angle_deg)
    return (
        radius_mm * cos(angle) - tangent_mm * sin(angle),
        radius_mm * sin(angle) + tangent_mm * cos(angle),
    )


def local_box(
    angle_deg: float,
    radius_mm: float,
    tangent_mm: float,
    radial_size_mm: float,
    tangent_size_mm: float,
    z0_mm: float,
    height_mm: float,
):
    x, y = local_point(angle_deg, radius_mm, tangent_mm)
    return Box(
        radial_size_mm,
        tangent_size_mm,
        height_mm,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).rotate(Axis.Z, angle_deg).moved(Location((x, y, z0_mm)))


def vertical_cylinder(
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


def _cut(shape, tools: Iterable[Any]):
    result = deepcopy(shape)
    for tool in tools:
        result = _as_shape(result.cut(deepcopy(tool)))
    return result


def _fuse(shape, additions: Iterable[Any]):
    result = deepcopy(shape)
    for addition in additions:
        result = _as_shape(result.fuse(deepcopy(addition)))
    return result


def moving_seam_tools(role: str, angle_deg: float, owners: OwnerBundle) -> dict[str, Any]:
    moving = owners.moving_joinery
    overtravel = owners.segmentation.boolean_overtravel_mm
    z0, z1 = moving.z_for(role)
    full_height = (z1 - z0) + moving.axial_gap_mm + overtravel * 2.0
    nominal_roi = local_box(
        angle_deg,
        moving.radial_mid_mm,
        0.0,
        moving.radial_span_mm,
        moving.tangent_half_mm * 2.0,
        z0 - overtravel,
        full_height,
    )
    lower_male = local_box(
        angle_deg,
        moving.radial_mid_mm,
        0.0,
        moving.radial_span_mm,
        moving.tangent_half_mm * 2.0,
        z0,
        moving.half_a_lap_mm,
    )
    upper_tongue = local_box(
        angle_deg,
        moving.radial_mid_mm,
        0.0,
        moving.radial_span_mm,
        moving.tangent_half_mm * 2.0,
        z0 + moving.half_a_lap_mm + moving.axial_gap_mm,
        moving.half_b_lap_mm,
    )
    receiving_cavity = local_box(
        angle_deg,
        moving.radial_mid_mm,
        0.0,
        moving.radial_span_mm + moving.receive_xy_clearance_mm * 2.0,
        (moving.tangent_half_mm + moving.receive_xy_clearance_mm) * 2.0,
        z0 - overtravel,
        moving.half_a_lap_mm + moving.axial_gap_mm + overtravel,
    )
    relief_strip = local_box(
        angle_deg,
        owners.segmentation.sector_mask_radius_mm / 2.0,
        0.0,
        owners.segmentation.sector_mask_radius_mm,
        moving.butt_face_relief_mm * 2.0,
        z0 - overtravel,
        full_height,
    )
    relief_exclusion = local_box(
        angle_deg,
        moving.radial_mid_mm,
        0.0,
        moving.radial_span_mm,
        moving.butt_face_relief_mm * 4.0,
        z0 - overtravel * 2.0,
        full_height + overtravel * 2.0,
    )
    exterior_relief = _as_shape(relief_strip.cut(relief_exclusion))
    screw_bores = [
        vertical_cylinder(
            angle_deg,
            moving.screw_axis_radius_mm,
            tangent,
            moving.screw_clearance_diameter_mm,
            z0 - overtravel,
            full_height,
        )
        for tangent in (-moving.screw_tangent_mm, moving.screw_tangent_mm)
    ]
    nut_pockets = [
        local_box(
            angle_deg,
            moving.screw_axis_radius_mm,
            tangent,
            moving.nut_pocket_radial_mm,
            moving.nut_pocket_tangent_mm,
            z0 + moving.rear_skin_mm,
            moving.nut_pocket_height_mm,
        )
        for tangent in (-moving.screw_tangent_mm, moving.screw_tangent_mm)
    ]
    press_bore = vertical_cylinder(
        angle_deg,
        moving.screw_axis_radius_mm,
        0.0,
        moving.press_bore_diameter_mm,
        z0,
        moving.half_a_lap_mm,
    )
    slip_bore = vertical_cylinder(
        angle_deg,
        moving.screw_axis_radius_mm,
        0.0,
        moving.slip_bore_diameter_mm,
        z0 + moving.half_a_lap_mm + moving.axial_gap_mm,
        moving.half_b_lap_mm,
    )
    return {
        "nominal_roi": nominal_roi,
        "lower_male": lower_male,
        "upper_tongue": upper_tongue,
        "receiving_cavity": receiving_cavity,
        "exterior_relief": exterior_relief,
        "screw_bores": screw_bores,
        "nut_pockets": nut_pockets,
        "press_bore": press_bore,
        "slip_bore": slip_bore,
    }


@lru_cache(maxsize=8)
def plain_moving_half_shapes(owners: OwnerBundle) -> dict[tuple[str, str], Any]:
    result: dict[tuple[str, str], Any] = {}
    seams = owners.segmentation.moving_seams_deg
    for role in ROLES:
        source = _source(ROLE_SOURCE_INDICES[role])
        result[(role, "A")] = _clip_children(source, _half_space(seams[0], owners))
        result[(role, "B")] = _clip_children(source, _half_space(seams[1], owners))
    return result


@lru_cache(maxsize=8)
def moving_half_shapes(owners: OwnerBundle) -> dict[tuple[str, str], Any]:
    result: dict[tuple[str, str], Any] = {}
    for role in ROLES:
        half_a = deepcopy(plain_moving_half_shapes(owners)[(role, "A")])
        half_b = deepcopy(plain_moving_half_shapes(owners)[(role, "B")])
        for angle in owners.segmentation.moving_seams_deg:
            tools = moving_seam_tools(role, angle, owners)
            half_a = _cut(half_a, [tools["exterior_relief"], tools["nominal_roi"]])
            half_a = _fuse(half_a, [tools["lower_male"]])
            half_a = _cut(
                half_a,
                [*tools["screw_bores"], *tools["nut_pockets"], tools["press_bore"]],
            )
            half_b = _cut(
                half_b,
                [tools["exterior_relief"], tools["nominal_roi"], tools["receiving_cavity"]],
            )
            half_b = _fuse(half_b, [tools["upper_tongue"]])
            half_b = _cut(half_b, [*tools["screw_bores"], tools["slip_bore"]])
        half_a.label = f"p3_v3_direct_race_{role}_M1_260T_I3_R2_half_A_130T_beta15p230769"
        half_b.label = f"p3_v3_direct_race_{role}_M1_260T_I3_R2_half_B_130T_beta195p230769"
        result[(role, "A")] = half_a
        result[(role, "B")] = half_b
    return result


def _patch(shape, zone, label: str):
    result = intersection(shape, zone)
    if volume(result) <= 1e-8:
        raise RuntimeError(f"R2 actual-BREP witness patch is empty: {label}")
    return result


def _distance(left, right) -> float:
    return float(left.distance_to(right))


@dataclass(frozen=True)
class WitnessDatums:
    """Frozen validation coordinates, intentionally independent of owners."""

    seam_angles_deg: tuple[float, float] = (15.230769230769, 195.230769230769)
    radial_min_mm: float = 133.50
    radial_span_mm: float = 6.50
    tangent_half_mm: float = 8.00
    screw_axis_radius_mm: float = 136.75
    screw_tangent_mm: float = 5.00
    half_a_lap_mm: float = 2.00
    witness_size_mm: float = 0.30
    role_z_mm: tuple[tuple[str, float], ...] = (
        ("hour", -1.50),
        ("minute", 4.05),
        ("second", 9.60),
    )

    def z0_for(self, role: str) -> float:
        return next(z0 for name, z0 in self.role_z_mm if name == role)


DEFAULT_WITNESS_DATUMS = WitnessDatums()


def _distance_to_seam_datum(patch, angle_deg: float, side: float) -> float:
    """Actual cropped-face distance to the frozen tangential datum t=0."""

    local_bounds = deepcopy(patch).rotate(Axis.Z, -angle_deg).bounding_box()
    return float(local_bounds.min.Y if side > 0.0 else -local_bounds.max.Y)


def seam_witnesses_from_shapes(
    shapes: dict[tuple[str, str], Any],
    datums: WitnessDatums = DEFAULT_WITNESS_DATUMS,
) -> tuple[dict[str, Any], ...]:
    """Measure frozen BREPs with fixed, owner-independent crop datums."""

    rows: list[dict[str, Any]] = []
    present_roles = tuple(role for role in ROLES if (role, "A") in shapes and (role, "B") in shapes)
    for role in present_roles:
        z0 = datums.z0_for(role)
        role_digests = {
            "A": brep_digest(shapes[(role, "A")]),
            "B": brep_digest(shapes[(role, "B")]),
        }
        for seam_index, angle in enumerate(datums.seam_angles_deg, start=1):
            half_a = shapes[(role, "A")]
            half_b = shapes[(role, "B")]
            b_side = -1.0 if seam_index == 1 else 1.0
            a_side = -b_side
            witness_height = datums.witness_size_mm
            witness_z = z0 + datums.half_a_lap_mm / 2.0 - witness_height / 2.0

            tangent_male = _patch(
                half_a,
                local_box(
                    angle,
                    datums.screw_axis_radius_mm,
                    b_side * (datums.tangent_half_mm - witness_height / 2.0),
                    witness_height,
                    witness_height,
                    witness_z,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/tangent_male",
            )
            tangent_wall = _patch(
                half_b,
                local_box(
                    angle,
                    datums.screw_axis_radius_mm,
                    b_side * (datums.tangent_half_mm + 0.30),
                    witness_height,
                    0.60,
                    witness_z,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/tangent_wall",
            )
            radial_male = _patch(
                half_a,
                local_box(
                    angle,
                    datums.radial_min_mm + witness_height / 2.0,
                    b_side * datums.screw_tangent_mm,
                    witness_height,
                    witness_height,
                    witness_z,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/radial_male",
            )
            radial_wall = _patch(
                half_b,
                local_box(
                    angle,
                    datums.radial_min_mm - 0.35,
                    b_side * datums.screw_tangent_mm,
                    0.70,
                    witness_height,
                    witness_z,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/radial_wall",
            )
            butt_radius = datums.radial_min_mm - witness_height * 2.0
            butt_a = _patch(
                half_a,
                local_box(
                    angle,
                    butt_radius,
                    a_side * 0.20,
                    witness_height,
                    0.40,
                    witness_z,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/butt_a",
            )
            butt_b = _patch(
                half_b,
                local_box(
                    angle,
                    butt_radius,
                    b_side * 0.20,
                    witness_height,
                    0.40,
                    witness_z,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/butt_b",
            )
            axial_radius = datums.radial_min_mm + datums.radial_span_mm / 3.0
            axial_tangent = a_side * datums.tangent_half_mm / 3.0
            axial_a = _patch(
                half_a,
                local_box(
                    angle,
                    axial_radius,
                    axial_tangent,
                    witness_height,
                    witness_height,
                    z0 + datums.half_a_lap_mm - witness_height,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/axial_a",
            )
            axial_b = _patch(
                half_b,
                local_box(
                    angle,
                    axial_radius,
                    axial_tangent,
                    witness_height,
                    witness_height,
                    z0 + datums.half_a_lap_mm,
                    witness_height,
                ),
                f"{role}/seam{seam_index}/axial_b",
            )
            rows.append(
                {
                    "role": role,
                    "seam": seam_index,
                    "radial_receive_clearance_mm": _distance(radial_male, radial_wall),
                    "tangential_receive_clearance_mm": _distance(tangent_male, tangent_wall),
                    "half_a_butt_relief_mm": _distance_to_seam_datum(butt_a, angle, a_side),
                    "half_b_butt_relief_mm": _distance_to_seam_datum(butt_b, angle, b_side),
                    "butt_gap_mm": _distance(butt_a, butt_b),
                    "axial_gap_mm": _distance(axial_a, axial_b),
                    "half_a_brep_sha256": role_digests["A"],
                    "half_b_brep_sha256": role_digests["B"],
                }
            )
    return tuple(rows)


def seam_witnesses(owners: OwnerBundle) -> tuple[dict[str, Any], ...]:
    """Build owner-driven shapes, then hand only frozen BREPs to validation."""

    return seam_witnesses_from_shapes(moving_half_shapes(owners))


def actual_geometry_evidence(owners: OwnerBundle) -> dict[str, Any]:
    rows = seam_witnesses(owners)
    return {
        "seams": rows,
        "seam_count": len(rows),
        "radial_clearance_range_mm": [
            min(row["radial_receive_clearance_mm"] for row in rows),
            max(row["radial_receive_clearance_mm"] for row in rows),
        ],
        "tangential_clearance_range_mm": [
            min(row["tangential_receive_clearance_mm"] for row in rows),
            max(row["tangential_receive_clearance_mm"] for row in rows),
        ],
        "butt_gap_range_mm": [
            min(row["butt_gap_mm"] for row in rows),
            max(row["butt_gap_mm"] for row in rows),
        ],
        "half_a_butt_relief_range_mm": [
            min(row["half_a_butt_relief_mm"] for row in rows),
            max(row["half_a_butt_relief_mm"] for row in rows),
        ],
        "half_b_butt_relief_range_mm": [
            min(row["half_b_butt_relief_mm"] for row in rows),
            max(row["half_b_butt_relief_mm"] for row in rows),
        ],
        "axial_gap_range_mm": [
            min(row["axial_gap_mm"] for row in rows),
            max(row["axial_gap_mm"] for row in rows),
        ],
    }


def _symmetric_difference(left, right):
    removed = _as_shape(deepcopy(left).cut(deepcopy(right)))
    added = _as_shape(deepcopy(right).cut(deepcopy(left)))
    return _as_shape(removed.fuse(added))


def _region_union(regions: Iterable[Any]):
    rows = list(regions)
    if not rows:
        return Compound(children=[])
    return _fuse(rows[0], rows[1:])


def parameter_change_locality(
    baseline_owners: OwnerBundle,
    changed_owners: OwnerBundle,
    field_name: str,
) -> tuple[dict[str, Any], ...]:
    """Bound actual changed BREP faces to the field's construction tools."""

    baseline = moving_half_shapes(baseline_owners)
    changed = moving_half_shapes(changed_owners)
    rows = []
    for role in ROLES:
        for half in ("A", "B"):
            delta = _symmetric_difference(baseline[(role, half)], changed[(role, half)])
            delta_volume = volume(delta)
            owned_tools = []
            for angle in baseline_owners.segmentation.moving_seams_deg:
                before_tools = moving_seam_tools(role, angle, baseline_owners)
                after_tools = moving_seam_tools(role, angle, changed_owners)
                if field_name == "receive_xy_clearance_mm":
                    owned_tools.extend(
                        [before_tools["receiving_cavity"], after_tools["receiving_cavity"]]
                    )
                elif field_name == "butt_face_relief_mm":
                    owned_tools.extend(
                        [before_tools["exterior_relief"], after_tools["exterior_relief"]]
                    )
                else:
                    raise ValueError(f"unsupported locality field {field_name!r}")
            owned_region = _region_union(owned_tools)
            outside = _as_shape(deepcopy(delta).cut(deepcopy(owned_region)))
            if delta_volume > 1e-9:
                bounds = delta.bounding_box()
                aabb = [
                    float(bounds.min.X), float(bounds.min.Y), float(bounds.min.Z),
                    float(bounds.max.X), float(bounds.max.Y), float(bounds.max.Z),
                ]
            else:
                aabb = None
            rows.append(
                {
                    "half_id": f"{role}_{half}",
                    "delta_volume_mm3": delta_volume,
                    "delta_face_count": len(delta.faces()),
                    "delta_aabb_mm": aabb,
                    "owned_region_intersection_mm3": intersection_volume(delta, owned_region),
                    "outside_owned_region_mm3": volume(outside),
                }
            )
    return tuple(rows)
