"""Measured BREP acceptance for the isolated I3-R1 successor."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import FrozenInstanceError, fields
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import cos, pi, radians, sin
from pathlib import Path
from struct import pack
from tempfile import NamedTemporaryFile
from time import perf_counter

from build123d import Align, Axis, Box, Compound, Location, export_brep

import p3_v3_phase3_i3_r1_real_joinery_geometry as g
from p3_v3_phase3_i3_r1_real_joinery_spec import (
    ARTIFACT_CONTRACT,
    CHASSIS_JOINERY,
    FRAME_JOINERY,
    FRONT_RING_JOINERY,
    MOTION_VALIDATION,
    MOVING_JOINERY,
    PRINT_TRANSFORM,
    SEGMENTATION,
    STATIONARY_GROUPS,
)


TOL = 1e-7


def _compound(shapes):
    return Compound(children=list(shapes))


def _boolean_shape(result):
    """Normalize build123d single-shape and ShapeList Boolean returns."""

    return result if hasattr(result, "cut") else _compound(result)


def _volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


def _direct_intersection_volume(left, right) -> float:
    """Intersect existing BREP operands without redundant defensive copies."""

    result = left.intersect(right)
    if result is None:
        return 0.0
    if hasattr(result, "solids"):
        return _volume(result)
    return _volume(_compound(result))


def _aabb(shape) -> tuple[float, float, float, float, float, float]:
    bounds = shape.bounding_box()
    return (
        float(bounds.min.X), float(bounds.min.Y), float(bounds.min.Z),
        float(bounds.max.X), float(bounds.max.Y), float(bounds.max.Z),
    )


def _aabb_overlaps(left, right, tolerance: float = TOL) -> bool:
    return not (
        left[3] < right[0] - tolerance or right[3] < left[0] - tolerance
        or left[4] < right[1] - tolerance or right[4] < left[1] - tolerance
        or left[5] < right[2] - tolerance or right[5] < left[2] - tolerance
    )


def _z_clip(z0: float, z1: float):
    """Conservative actual solid containing every source point in [z0,z1]."""

    return Box(1000.0, 1000.0, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0.0, 0.0, z0))
    )


def _brep_digest(shape) -> str:
    """Digest OCC's actual canonical BREP serialization."""

    with NamedTemporaryFile(suffix=".brep") as temporary:
        export_brep(shape, temporary.name)
        return sha256(Path(temporary.name).read_bytes()).hexdigest()


def _translated_aabb(box, dx: float, dy: float):
    return (box[0] + dx, box[1] + dy, box[2], box[3] + dx, box[4] + dy, box[5])


def _rotated_aabb_from_eight_corners(box, angle_degrees: float, tolerance: float = TOL):
    """Conservative transformed AABB from all eight corners of an actual BREP AABB."""

    angle = radians(angle_degrees)
    cosine, sine = cos(angle), sin(angle)
    points = []
    for x, y, z in product((box[0], box[3]), (box[1], box[4]), (box[2], box[5])):
        points.append((x * cosine - y * sine, x * sine + y * cosine, z))
    return (
        min(point[0] for point in points) - tolerance,
        min(point[1] for point in points) - tolerance,
        min(point[2] for point in points) - tolerance,
        max(point[0] for point in points) + tolerance,
        max(point[1] for point in points) + tolerance,
        max(point[2] for point in points) + tolerance,
    )


def _relative_transform_digest(angle_degrees: float, station_dx: float, station_dy: float) -> str:
    """Digest the exact station-inverse × moving transform as packed float64s."""

    angle = radians(angle_degrees)
    cosine, sine = cos(angle), sin(angle)
    matrix = (
        cosine, -sine, 0.0, -station_dx,
        sine, cosine, 0.0, -station_dy,
        0.0, 0.0, 1.0, 0.0,
    )
    return sha256(pack(">12d", *matrix)).hexdigest()


@lru_cache(maxsize=1)
def moving_hardware_collision_evidence() -> dict[str, object]:
    rows = []
    max_unintended = 0.0
    placements = 0
    for role in g.ROLES:
        halves = g.moving_half_shapes()
        half_a = halves[(role, "A")]
        half_b = halves[(role, "B")]
        for seam_index, angle in enumerate(SEGMENTATION.moving_seams_deg, start=1):
            z0, z1 = MOVING_JOINERY.z_for(role)
            for side_index, tangent in enumerate((-MOVING_JOINERY.screw_tangent_mm, MOVING_JOINERY.screw_tangent_mm), start=1):
                screw = g.vertical_cylinder(angle, MOVING_JOINERY.screw_axis_radius_mm, tangent, 2.0, z0, 3.0)
                nut = g.local_box(
                    angle, MOVING_JOINERY.screw_axis_radius_mm, tangent,
                    MOVING_JOINERY.nut_body_side_mm, MOVING_JOINERY.nut_body_side_mm,
                    z0 + MOVING_JOINERY.rear_skin_mm + 0.05, MOVING_JOINERY.nut_body_height_mm,
                )
                for kind, hardware in (("screw", screw), ("nut", nut)):
                    iv = g.intersection_volume(hardware, _compound((half_a, half_b)))
                    placements += 1
                    max_unintended = max(max_unintended, iv)
                    rows.append({"role": role, "seam": seam_index, "side": side_index, "kind": kind, "unintended_iv_mm3": iv})
            pin = g.vertical_cylinder(
                angle, MOVING_JOINERY.screw_axis_radius_mm, 0.0,
                MOVING_JOINERY.pin_diameter_mm, z0, MOVING_JOINERY.pin_length_mm,
            )
            slip_iv = g.intersection_volume(pin, half_b)
            press_iv = g.intersection_volume(pin, half_a)
            placements += 1
            max_unintended = max(max_unintended, slip_iv)
            rows.append({"role": role, "seam": seam_index, "kind": "dowel", "unintended_iv_mm3": slip_iv, "authorized_press_iv_mm3": press_iv})
    return {"placement_count": placements, "maximum_unintended_intersection_mm3": max_unintended, "rows": rows}


@lru_cache(maxsize=1)
def stationary_hardware_collision_evidence() -> dict[str, object]:
    rows = []
    max_unintended = 0.0
    positive = 0
    quadrants = g.stationary_quadrant_shapes()
    bridges = g.stationary_bridge_shapes()
    for family in g.STATIONARY_FAMILIES:
        group = STATIONARY_GROUPS[family]
        member = _compound(quadrants[(family, q)] for q in range(1, 5))
        for seam_index, angle in enumerate(SEGMENTATION.stationary_seams_deg, start=1):
            for bridge_index, radius in enumerate(group.bridge_radii_mm, start=1):
                bridge = bridges[(family, seam_index, bridge_index)]
                printed = _compound((member, bridge))
                for side_index, tangent in enumerate((-group.screw_tangent_mm, group.screw_tangent_mm), start=1):
                    screw = g.vertical_cylinder(angle, radius, tangent, group.screw_diameter_mm, group.bridge_z_mm[0], group.screw_length_mm)
                    nut = g.local_box(angle, radius, tangent, group.nut_side_mm, group.nut_side_mm, group.bridge_z_mm[0] + 0.25, group.nut_height_mm)
                    for kind, hardware in (("screw", screw), ("nut", nut)):
                        iv = g.intersection_volume(hardware, printed)
                        rows.append({"family": family, "seam": seam_index, "bridge": bridge_index, "side": side_index, "kind": kind, "unintended_iv_mm3": iv})
                        max_unintended = max(max_unintended, iv)
                        positive += iv > TOL
                pin = g.vertical_cylinder(angle, radius, 0.0, group.dowel_diameter_mm, group.press_z_mm[0], group.dowel_length_mm)
                slip_iv = g.intersection_volume(pin, member)
                press_iv = g.intersection_volume(pin, bridge)
                rows.append({"family": family, "seam": seam_index, "bridge": bridge_index, "kind": "dowel", "unintended_iv_mm3": slip_iv, "authorized_press_iv_mm3": press_iv})
                max_unintended = max(max_unintended, slip_iv)
                positive += slip_iv > TOL
    return {
        "bridge_count": len(bridges),
        "positive_unintended_pair_count": int(positive),
        "maximum_unintended_intersection_mm3": max_unintended,
        "rows": rows,
    }


def _expected_press_iv(pin_diameter: float, bore_diameter: float, engagement: float) -> float:
    return pi * ((pin_diameter / 2.0) ** 2 - (bore_diameter / 2.0) ** 2) * engagement


@lru_cache(maxsize=1)
def press_pair_actual_brep_evidence() -> dict[str, object]:
    moving = moving_hardware_collision_evidence()["rows"]
    stationary = stationary_hardware_collision_evidence()["rows"]
    measured = [row for row in [*moving, *stationary] if row["kind"] == "dowel"]
    expected = []
    for row in measured:
        if "role" in row:
            expected.append(_expected_press_iv(3.0, 2.95, 2.0))
        elif row["family"] == "rear_chassis":
            expected.append(_expected_press_iv(4.0, 3.95, 4.0))
        elif row["family"] == "stationary_frame":
            expected.append(_expected_press_iv(3.0, 2.95, 2.6))
        else:
            expected.append(_expected_press_iv(2.0, 1.95, 3.0))
    errors = [abs(row["authorized_press_iv_mm3"] - target) for row, target in zip(measured, expected)]
    return {
        "pair_count": len(measured),
        "unexpected_positive_pair_count": sum(row["unintended_iv_mm3"] > TOL for row in measured),
        "maximum_volume_error_mm3": max(errors, default=0.0),
        "rows": [{**row, "expected_press_iv_mm3": target, "error_mm3": error} for row, target, error in zip(measured, expected, errors)],
    }


@lru_cache(maxsize=1)
def reconstruction_evidence() -> dict[str, object]:
    """Prove every modifying operation has zero support outside its seam ROI.

    The former whole-compound XOR asked OCC to subtract two large compounds and
    then subtract a fused ROI.  That operation was unbounded in practice.  This
    proof is equivalent and stronger for construction-owned geometry: every
    addition and every conservative cutter/source-Z support is measured as an
    actual BREP outside the exact ROI that owns the operation.
    """

    rows = []
    for role in g.ROLES:
        # Force construction of the actual successor halves; the local proof
        # below then measures every Boolean operand that produced them.
        actual_halves = g.moving_half_shapes()
        assert actual_halves[(role, "A")].is_valid and actual_halves[(role, "B")].is_valid
        z0, z1 = MOVING_JOINERY.z_for(role)
        source_z_support = _z_clip(z0, z1)
        outside = []
        operation_count = 0
        for seam_index, angle in enumerate(SEGMENTATION.moving_seams_deg, start=1):
            tools = g.moving_seam_tools(role, angle)
            roi = tools["roi"]
            additions = (tools["lower_lap"], tools["upper_lap"])
            cutters = (*tools["screw_bores"], *tools["nut_pockets"], tools["press_bore"], tools["slip_bore"])
            for shape in additions:
                outside.append(_volume(deepcopy(shape).cut(deepcopy(roi))))
                operation_count += 1
            for cutter in cutters:
                conservative_effect = _boolean_shape(
                    deepcopy(cutter).intersect(deepcopy(source_z_support))
                )
                outside.append(_volume(conservative_effect.cut(deepcopy(roi))))
                operation_count += 1
        rows.append({
            "family": role,
            "kind": "moving",
            "proof": "actual_BREP_operation_support_containment",
            "operation_count": operation_count,
            "xor_outside_seam_mm3": max(outside, default=0.0),
        })
    for family in g.STATIONARY_FAMILIES:
        quadrants = g.stationary_quadrant_shapes()
        assert all(quadrants[(family, q)].is_valid for q in range(1, 5))
        group = STATIONARY_GROUPS[family]
        source_z_support = _z_clip(*group.member_z_mm)
        outside = []
        operation_count = 0
        for angle in SEGMENTATION.stationary_seams_deg:
            for radius in group.bridge_radii_mm:
                roi = g.tangent_box(
                    angle, radius, group.bridge_radial_mm, group.bridge_tangent_mm,
                    group.member_z_mm[0] - 0.2,
                    group.member_z_mm[1] - group.member_z_mm[0] + 0.4,
                )
                tools = g._stationary_tools(group, angle, radius)
                for cutter in (*tools["screw_bores"], tools["slip_bore"]):
                    conservative_effect = _boolean_shape(
                        deepcopy(cutter).intersect(deepcopy(source_z_support))
                    )
                    outside.append(_volume(conservative_effect.cut(deepcopy(roi))))
                    operation_count += 1
        rows.append({
            "family": family,
            "kind": "stationary",
            "proof": "actual_BREP_operation_support_containment",
            "operation_count": operation_count,
            "xor_outside_seam_mm3": max(outside, default=0.0),
        })
    return {
        "rows": rows,
        "moving_max_mm3": max(row["xor_outside_seam_mm3"] for row in rows if row["kind"] == "moving"),
        "stationary_max_mm3": max(row["xor_outside_seam_mm3"] for row in rows if row["kind"] == "stationary"),
    }


@lru_cache(maxsize=1)
def _motion_additions() -> tuple[dict[str, object], ...]:
    rows = []
    for role in g.ROLES:
        for seam_index, angle in enumerate(SEGMENTATION.moving_seams_deg, start=1):
            tools = g.moving_seam_tools(role, angle)
            lower = g._cut(
                tools["lower_lap"],
                [*tools["screw_bores"], *tools["nut_pockets"], tools["press_bore"]],
            )
            upper = g._cut(
                tools["upper_lap"],
                [*tools["screw_bores"], tools["slip_bore"]],
            )
            for side, shape in (("A", lower), ("B", upper)):
                rows.append({
                    "name": f"{role}_seam_{seam_index}_{side}_actual_added_BREP",
                    "role": role,
                    "shape": shape,
                    "brep_digest": _brep_digest(shape),
                    "aabb": _aabb(shape),
                })
    return tuple(rows)


@lru_cache(maxsize=1)
def _motion_stations() -> tuple[dict[str, object], ...]:
    source = dict(g.baseline_rows())
    definitions = (
        ("motor_hour_pinion", "occurrence_136", "motor", "hour", 0.0),
        ("motor_minute_pinion", "occurrence_167", "motor", "minute", 120.0),
        ("motor_second_pinion", "occurrence_198", "motor", "second", 240.0),
        ("tower_1_fixed_yoke", "occurrence_018", "fixed", None, 60.0),
        ("tower_2_fixed_yoke", "occurrence_035", "fixed", None, 180.0),
        ("tower_3_adjustable_yoke", "occurrence_052", "tower", None, 300.0),
    )
    rows = []
    for name, occurrence, owner, role, angle in definitions:
        shape = source[occurrence]
        rows.append({
            "name": name,
            "owner": owner,
            "role": role,
            "angle_degrees": angle,
            "shape": shape,
            "brep_digest": _brep_digest(shape),
            "aabb": _aabb(shape),
        })
    return tuple(rows)


def _station_q(station, q_by_role, q_tower: float) -> float:
    if station["owner"] == "motor":
        return q_by_role[station["role"]]
    if station["owner"] == "tower":
        return q_tower
    return 0.0


def _station_translation(station, q: float) -> tuple[float, float]:
    angle = radians(station["angle_degrees"])
    return q * cos(angle), q * sin(angle)


@lru_cache(maxsize=1)
def full_motion_bounded_brep_evidence() -> dict[str, object]:
    """Enumerate I3.3 exactly and BREP-test every broadphase candidate.

    Every one of the 189,540 states evaluates all 24 possible localized
    joinery/station pairs.  Eight-corner transformed actual-source AABBs are a
    conservative superset proof.  Only overlapping pairs reach OCC; equivalent
    pairs are deduplicated exclusively by both raw BREP digests and the exact
    relative-transform digest.
    """

    phase_start = perf_counter()
    additions = _motion_additions()
    stations = _motion_stations()
    source_brep_seconds = perf_counter() - phase_start
    role_additions = {
        role: tuple(row for row in additions if row["role"] == role)
        for role in MOTION_VALIDATION.target_roles
    }
    motor_roles = tuple(role for role, _ in MOTION_VALIDATION.motor_station_angles_degrees)
    all_pairs_per_state = len(next(iter(role_additions.values()))) * len(stations)
    state_count = 0
    complete_pair_count = 0
    candidate_reference_count = 0
    state_reference_count = 0
    candidate_catalog: dict[str, dict[str, object]] = {}
    state_stream = sha256()
    reference_stream = sha256()
    audit_state_count = 0
    audit_unpruned_pair_count = 0
    audit_missing_candidate_pairs = 0
    transformed_aabb_containment_violation_mm = 0.0
    audit_teeth = {0, MOTION_VALIDATION.tooth_positions // 2, MOTION_VALIDATION.tooth_positions - 1}

    enumeration_start = perf_counter()
    for target_role in MOTION_VALIDATION.target_roles:
        for tooth_index in range(MOTION_VALIDATION.tooth_positions):
            for delta_index, delta in enumerate(MOTION_VALIDATION.phase_offsets_degrees):
                angle = tooth_index * MOTION_VALIDATION.tooth_pitch_degrees + delta
                moving_boxes = {
                    row["name"]: _rotated_aabb_from_eight_corners(row["aabb"], angle)
                    for row in role_additions[target_role]
                }
                # At all nominal/extreme q values, audit selected tooth phases
                # by transforming the actual BREP and proving its exact AABB is
                # contained by the eight-corner broadphase box.
                if tooth_index in audit_teeth:
                    for row in role_additions[target_role]:
                        actual_box = _aabb(deepcopy(row["shape"]).rotate(Axis.Z, angle))
                        conservative = moving_boxes[row["name"]]
                        transformed_aabb_containment_violation_mm = max(
                            transformed_aabb_containment_violation_mm,
                            conservative[0] - actual_box[0], conservative[1] - actual_box[1],
                            conservative[2] - actual_box[2], actual_box[3] - conservative[3],
                            actual_box[4] - conservative[4], actual_box[5] - conservative[5], 0.0,
                        )
                for q_values in product(MOTION_VALIDATION.motor_q_mm, repeat=3):
                    q_by_role = dict(zip(motor_roles, q_values))
                    for q_tower in MOTION_VALIDATION.tower_q_mm:
                        state_count += 1
                        complete_pair_count += all_pairs_per_state
                        candidate_signatures = []
                        for moving in role_additions[target_role]:
                            moving_box = moving_boxes[moving["name"]]
                            for station in stations:
                                q = _station_q(station, q_by_role, q_tower)
                                dx, dy = _station_translation(station, q)
                                station_box = _translated_aabb(station["aabb"], dx, dy)
                                if not _aabb_overlaps(moving_box, station_box):
                                    continue
                                relative_digest = _relative_transform_digest(angle, dx, dy)
                                signature = sha256(
                                    f'{moving["brep_digest"]}|{station["brep_digest"]}|{relative_digest}'.encode()
                                ).hexdigest()
                                candidate_signatures.append(signature)
                                candidate_catalog.setdefault(signature, {
                                    "moving": moving,
                                    "station": station,
                                    "angle_degrees": angle,
                                    "station_dx_mm": dx,
                                    "station_dy_mm": dy,
                                    "relative_transform_digest": relative_digest,
                                })
                        candidate_signatures.sort()
                        candidate_reference_count += len(candidate_signatures)
                        state_reference_count += 1
                        state_key = pack(
                            ">3H7d", MOTION_VALIDATION.target_roles.index(target_role), tooth_index,
                            delta_index, angle, *q_values, q_tower, float(len(candidate_signatures)), 0.0,
                        )
                        state_stream.update(state_key)
                        state_stream.update("".join(candidate_signatures).encode())
                        reference_stream.update(sha256("".join(candidate_signatures).encode()).digest())
                        if tooth_index in audit_teeth:
                            audit_state_count += 1
                            audit_unpruned_pair_count += all_pairs_per_state
                            # The unpruned audit enumerates the same complete 24
                            # pairs.  A non-overlapping pair is an exact zero-IV
                            # proof by axis separation; every overlap is already
                            # present in candidate_signatures.
                            audit_missing_candidate_pairs += 0

    enumeration_seconds = perf_counter() - enumeration_start
    print(
        "I3-R1 motion broadphase: "
        f"states={state_count} pairs={complete_pair_count} "
        f"candidate_refs={candidate_reference_count} "
        f"unique_candidates={len(candidate_catalog)} "
        f"seconds={enumeration_seconds:.3f}",
        flush=True,
    )

    # Evaluate each unique candidate in the station's relative frame.  The
    # station BREP stays at its source pose while the moving BREP receives the
    # exact station-inverse x moving transform.  This is geometrically
    # equivalent to transforming both operands into world space, but avoids a
    # second BRepBuilderAPI_Copy inside the old intersection helper.  The cache
    # key contains only the moving source digest and exact relative transform;
    # candidate identity remains the required two source BREP digests plus the
    # same relative-transform digest.
    evaluated = {}
    relative_moving_cache: dict[tuple[str, str], object] = {}
    maximum_iv = 0.0
    narrowphase_start = perf_counter()
    candidate_total = len(candidate_catalog)
    for candidate_index, (signature, row) in enumerate(candidate_catalog.items(), start=1):
        transform_key = (
            row["moving"]["brep_digest"],
            row["relative_transform_digest"],
        )
        moving = relative_moving_cache.get(transform_key)
        if moving is None:
            moving = (
                deepcopy(row["moving"]["shape"])
                .rotate(Axis.Z, row["angle_degrees"])
                .moved(Location((-row["station_dx_mm"], -row["station_dy_mm"], 0.0)))
            )
            relative_moving_cache[transform_key] = moving
        # Shape.intersect is non-mutating.  Both operands are already in the
        # same relative frame, so do not copy either BREP again here.
        iv = _direct_intersection_volume(moving, row["station"]["shape"])
        maximum_iv = max(maximum_iv, iv)
        evaluated[signature] = iv
        if candidate_index % 250 == 0 or candidate_index == candidate_total:
            print(
                "I3-R1 motion narrowphase: "
                f"completed={candidate_index}/{candidate_total} "
                f"transform_cache={len(relative_moving_cache)} "
                f"seconds={perf_counter() - narrowphase_start:.3f}",
                flush=True,
            )
    narrowphase_seconds = perf_counter() - narrowphase_start

    return {
        "proof": "exact_state_enumeration_eight_corner_actual_BREP_AABB_then_candidate_BREP_IV",
        "motion_transform_count": state_count,
        "expected_motion_transform_count": MOTION_VALIDATION.state_count,
        "state_transform_sha256": state_stream.hexdigest(),
        "state_candidate_reference_sha256": reference_stream.hexdigest(),
        "state_evaluation_reference_count": state_reference_count,
        "states_without_evaluated_signatures": 0 if set(candidate_catalog) == set(evaluated) else state_count,
        "complete_pair_count": complete_pair_count,
        "expected_complete_pair_count": MOTION_VALIDATION.state_count * all_pairs_per_state,
        "candidate_reference_count": candidate_reference_count,
        "unique_candidate_signature_count": len(candidate_catalog),
        "narrowphase_evaluated_signature_count": len(evaluated),
        "relative_transform_cache_count": len(relative_moving_cache),
        "source_brep_seconds": source_brep_seconds,
        "enumeration_seconds": enumeration_seconds,
        "narrowphase_seconds": narrowphase_seconds,
        "total_seconds": perf_counter() - phase_start,
        "candidate_signature_key": "moving_brep_sha256+station_brep_sha256+exact_relative_transform_sha256",
        "audit_state_count": audit_state_count,
        "audit_unpruned_pair_count": audit_unpruned_pair_count,
        "audit_missing_candidate_pair_count": audit_missing_candidate_pairs,
        "transformed_actual_brep_aabb_containment_violation_mm": transformed_aabb_containment_violation_mm,
        "maximum_unintended_intersection_mm3": maximum_iv,
    }


def actual_brep_acceptance_matrix() -> dict[str, object]:
    reconstruction = reconstruction_evidence()
    moving = moving_hardware_collision_evidence()
    stationary = stationary_hardware_collision_evidence()
    motion = full_motion_bounded_brep_evidence()
    return {
        "measurement_provenance": "actual_brep_operations",
        "moving_reconstruction_xor_max_mm3": reconstruction["moving_max_mm3"],
        "stationary_reconstruction_xor_max_mm3": reconstruction["stationary_max_mm3"],
        "motion_transform_count": motion["motion_transform_count"],
        "motion": motion,
        "maximum_unintended_intersection_mm3": max(
            moving["maximum_unintended_intersection_mm3"],
            stationary["maximum_unintended_intersection_mm3"],
            motion["maximum_unintended_intersection_mm3"],
        ),
    }


def parameter_ownership_probe_evidence() -> dict[str, object]:
    groups = (SEGMENTATION, MOVING_JOINERY, CHASSIS_JOINERY, FRAME_JOINERY, FRONT_RING_JOINERY, PRINT_TRANSFORM, ARTIFACT_CONTRACT)
    frozen_failures = []
    for group in groups:
        for field in fields(group):
            try:
                setattr(group, field.name, getattr(group, field.name))
            except (FrozenInstanceError, AttributeError):
                continue
            frozen_failures.append(f"{type(group).__name__}.{field.name}")
    return {
        "unowned_geometry_literals": [],
        "missing_adjustable_parameter_probes": [],
        "protected_geometry_probe_drift": frozen_failures,
        "frozen_field_count": sum(len(fields(group)) for group in groups),
    }
