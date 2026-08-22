"""Focused contracts for the KAGE low-Z drive comparison.

This is an experimental communication-model gate, not a print-readiness or
motion-validation suite.  It freezes the accepted direct-gear-race STEP as
the source of truth, checks the three agreed Z-envelope concepts, and proves
that the moving ring teeth and their output pinions were reused unchanged.
"""

from __future__ import annotations

from hashlib import sha256
import importlib
import json
from itertools import combinations
from pathlib import Path

from build123d import Align, Compound, Cylinder, Location, import_step
import pytest


ROOT = Path(__file__).resolve().parents[1]
LOCKED_ROOT = (
    ROOT
    / "models"
    / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
)
LOCKED_STEP = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step"
LOCKED_STEP_SHA256 = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"

MODEL_ROOT = ROOT / "models" / "p3_v3_exp_low_z_drive_comparison_r0"
GEOMETRY_MODULE = "p3_v3_exp_low_z_drive_comparison_r0_geometry"
EXPORT_MODULE = "p3_v3_exp_low_z_drive_comparison_r0_export"

ARTIFACTS = {
    "A": MODEL_ROOT / "A_locked_z_budget_section.step",
    "B": MODEL_ROOT / "B_flush_hardware_captive_axle.step",
    "C": MODEL_ROOT / "C_role_local_short_bevel_station.step",
    "comparison": MODEL_ROOT / "p3_v3_exp_low_z_drive_comparison_r0_side_by_side.step",
}


def _load_module(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(
                f"RED: experimental low-Z module {name!r} has not been implemented yet",
                pytrace=False,
            )
        raise


def _geometry():
    module = _load_module(GEOMETRY_MODULE)
    required = {
        "make_locked_reference_A",
        "make_flush_hardware_B",
        "make_side_by_side_comparison",
    }
    missing = sorted(required - set(dir(module)))
    assert not missing, f"missing low-Z geometry factories: {missing}"
    assert any(
        hasattr(module, name)
        for name in ("make_role_local_coupon_C", "make_short_bevel_C")
    ), "missing role-local Concept C geometry factory"
    return module


def _bounds(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return tuple(
        round(value, 6)
        for value in (box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z)
    )


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids())


def _z_facts(shape) -> tuple[float, float, float]:
    box = shape.bounding_box()
    return (box.min.Z, box.max.Z, box.size.Z)


def _is_frozen_drive_occurrence(label: str) -> bool:
    return label.startswith("p3_v3_direct_race_") and (
        "_M1_260T_quadrant_" in label or "_16T_output_pinion_" in label
    )


def _occurrence_signature(shape, *, frozen_drive_only: bool = False) -> dict[str, tuple]:
    result = {}
    for child in shape.children:
        label = child.label or ""
        if frozen_drive_only and not _is_frozen_drive_occurrence(label):
            continue
        assert label, "all compared STEP occurrences require stable labels"
        assert label not in result, f"duplicate occurrence label {label!r}"
        result[label] = (
            round(_volume(child), 5),
            _bounds(child),
            len(child.solids()),
        )
    return result


def _assert_positive_valid_solids(shape) -> None:
    solids = list(shape.solids())
    assert solids, "concept must contain closed solids"
    assert shape.is_valid
    assert all(solid.is_valid and solid.volume > 1e-6 for solid in solids)


@pytest.fixture(scope="module")
def locked_reference():
    assert LOCKED_STEP.exists()
    return import_step(str(LOCKED_STEP))


def _make_concept(key: str):
    geometry = _geometry()
    concept_c = getattr(
        geometry,
        "make_role_local_coupon_C",
        getattr(geometry, "make_short_bevel_C", None),
    )
    factories = {
        "A": geometry.make_locked_reference_A,
        "B": geometry.make_flush_hardware_B,
        "C": concept_c,
        "comparison": geometry.make_side_by_side_comparison,
    }
    assert factories[key] is not None
    return factories[key]()


def _walk(shape):
    for child in shape.children:
        yield child
        yield from _walk(child)


def _by_label(shape, token: str):
    return [child for child in _walk(shape) if token in (child.label or "")]


def _xy(child) -> tuple[float, float]:
    center = child.bounding_box().center()
    return (center.X, center.Y)


def _diameter_xy(child) -> float:
    box = child.bounding_box()
    return max(box.size.X, box.size.Y)


def _z_interval(child) -> tuple[float, float]:
    box = child.bounding_box()
    return (box.min.Z, box.max.Z)


def _cylinder_tool(
    x: float, y: float, z0: float, z1: float, diameter: float
):
    return Cylinder(
        diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))


def _bbox_may_overlap(a, b, tolerance: float = 1e-6) -> bool:
    aa = a.bounding_box()
    bb = b.bounding_box()
    return not (
        aa.max.X < bb.min.X - tolerance
        or bb.max.X < aa.min.X - tolerance
        or aa.max.Y < bb.min.Y - tolerance
        or bb.max.Y < aa.min.Y - tolerance
        or aa.max.Z < bb.min.Z - tolerance
        or bb.max.Z < aa.min.Z - tolerance
    )


def _intersection_volume(a, b) -> float:
    if not _bbox_may_overlap(a, b):
        return 0.0
    common = a.intersect(b)
    if common is None:
        return 0.0
    return sum(solid.volume for solid in common.solids())


def _frozen_m3_axes(locked_reference) -> dict[str, tuple[float, float]]:
    axes = {}
    for child in locked_reference.children:
        label = child.label or ""
        if "M3x10_screw_REFERENCE" not in label and "M3_mount_screw_" not in label:
            continue
        axes[label] = _xy(child)
    assert len(axes) == 18, "locked clock must expose 12 clamp and 6 tower M3 axes"
    return axes


def test_locked_source_step_is_immutable_and_A_is_an_exact_reference(locked_reference):
    assert sha256(LOCKED_STEP.read_bytes()).hexdigest() == LOCKED_STEP_SHA256

    reference_bounds = _bounds(locked_reference)
    assert reference_bounds == pytest.approx((-150.0, -150.0, -32.5, 150.0, 150.0, 24.2514))
    assert reference_bounds[5] - reference_bounds[2] == pytest.approx(56.7514)

    concept_a = _make_concept("A")
    assert _bounds(concept_a) == pytest.approx(reference_bounds)
    assert _volume(concept_a) == pytest.approx(_volume(locked_reference), abs=1e-4)
    assert _occurrence_signature(concept_a) == _occurrence_signature(locked_reference)


def test_B_meets_its_complete_clock_Z_budget_without_moving_the_tallest_fin():
    z_min, z_max, height = _z_facts(_make_concept("B"))
    assert z_min >= -28.0 - 1e-6
    assert z_max == pytest.approx(24.2514, abs=1e-4), "existing tallest fin must remain unchanged"
    assert height <= 52.3 + 1e-6


@pytest.mark.parametrize("key", ("A", "B", "C", "comparison"))
def test_every_concept_contains_only_positive_valid_solids(key: str):
    _assert_positive_valid_solids(_make_concept(key))


def test_B_preserves_all_15_locked_ring_and_output_pinion_occurrences(locked_reference):
    expected = _occurrence_signature(locked_reference, frozen_drive_only=True)
    actual = _occurrence_signature(_make_concept("B"), frozen_drive_only=True)
    assert len(expected) == 15, "locked reference must contain 12 ring quadrants and 3 pinions"
    assert actual == expected


def test_B_has_real_D6_counterbores_and_D3p4_shank_continuity_at_all_frozen_axes(
    locked_reference,
):
    concept_b = _make_concept("B")
    counterbored_members = _by_label(concept_b, "B_REAL_COUNTERBORED_")
    assert counterbored_members, "B requires cut structural members, not positive void-tool props"

    for source_label, (x, y) in _frozen_m3_axes(locked_reference).items():
        candidates = []
        for member in counterbored_members:
            box = member.bounding_box()
            if (
                box.min.X - 3.0 <= x <= box.max.X + 3.0
                and box.min.Y - 3.0 <= y <= box.max.Y + 3.0
            ):
                candidates.append(member)
        assert candidates, f"no real counterbored B member owns frozen axis {source_label}"

        z0 = min(member.bounding_box().min.Z for member in candidates)
        assert z0 >= -28.0 - 1e-6
        counterbore = _cylinder_tool(x, y, z0 - 0.01, z0 + 2.0, 6.0)
        # The screw crosses the 6.70 mm mounting stack at the member's lower
        # face.  The member bounding box also contains the upright yoke, which
        # is not part of the fastener span and must not be treated as a bore.
        shank = _cylinder_tool(x, y, z0 - 0.01, z0 + 6.71, 3.4)
        assert sum(_intersection_volume(member, counterbore) for member in candidates) < 1e-4
        assert sum(_intersection_volume(member, shank) for member in candidates) < 1e-4


def test_B_exports_a_complete_low_profile_M3_reference_stack_at_every_frozen_axis(
    locked_reference,
):
    concept_b = _make_concept("B")
    for source_label, axis in _frozen_m3_axes(locked_reference).items():
        parts = {
            token: [
                child
                for child in _walk(concept_b)
                if source_label in (child.label or "") and token in (child.label or "")
            ]
            for token in ("head", "shank", "opposite_washer", "captive_nut")
        }
        assert all(len(found) == 1 for found in parts.values()), (
            f"{source_label} requires one head, shank, washer and nut reference; "
            f"got { {token: len(found) for token, found in parts.items()} }"
        )
        head = parts["head"][0]
        shank = parts["shank"][0]
        washer = parts["opposite_washer"][0]
        nut = parts["captive_nut"][0]
        assert _xy(head) == pytest.approx(axis, abs=1e-4)
        assert all(_xy(part) == pytest.approx(axis, abs=1e-4) for part in (shank, washer, nut))
        assert _diameter_xy(head) == pytest.approx(5.5, abs=0.05)
        assert head.bounding_box().size.Z <= 1.8 + 1e-4
        assert _diameter_xy(shank) == pytest.approx(3.0, abs=0.05)
        assert _diameter_xy(washer) == pytest.approx(7.0, abs=0.05)
        assert washer.bounding_box().size.Z == pytest.approx(0.5, abs=0.05)
        assert nut.bounding_box().size.Z == pytest.approx(2.4, abs=0.05)
        stack_parts = [item for found in parts.values() for item in found]
        assert min(part.bounding_box().min.Z for part in stack_parts) >= -28.0 - 1e-6
        assert max(part.bounding_box().max.Z for part in stack_parts) <= 24.2514 + 1e-6


@pytest.mark.parametrize(
    ("shaft_token", "lower_token", "upper_token", "count"),
    (
        (
            "short_captive_output_shaft",
            "output_lower_shoulder",
            "output_low_snap_retainer",
            3,
        ),
        (
            "blind_captive_roller_axle",
            "roller_lower_shoulder",
            "roller_low_snap_retainer",
            3,
        ),
    ),
)
def test_B_shafts_and_roller_axles_have_positive_two_direction_axial_retention(
    shaft_token: str, lower_token: str, upper_token: str, count: int
):
    concept_b = _make_concept("B")
    shafts = _by_label(concept_b, shaft_token)
    lowers = _by_label(concept_b, lower_token)
    uppers = _by_label(concept_b, upper_token)
    assert len(shafts) == len(lowers) == len(uppers) == count

    unmatched_lowers = list(lowers)
    unmatched_uppers = list(uppers)
    for shaft in shafts:
        lower = min(unmatched_lowers, key=lambda candidate: sum((a - b) ** 2 for a, b in zip(_xy(candidate), _xy(shaft))))
        upper = min(unmatched_uppers, key=lambda candidate: sum((a - b) ** 2 for a, b in zip(_xy(candidate), _xy(shaft))))
        unmatched_lowers.remove(lower)
        unmatched_uppers.remove(upper)
        assert _xy(lower) == pytest.approx(_xy(shaft), abs=1e-4)
        assert _xy(upper) == pytest.approx(_xy(shaft), abs=1e-4)
        assert _diameter_xy(lower) >= _diameter_xy(shaft) + 2.0
        assert _diameter_xy(upper) >= _diameter_xy(shaft) + 2.0
        assert lower.bounding_box().center().Z < shaft.bounding_box().center().Z
        assert upper.bounding_box().center().Z > shaft.bounding_box().center().Z
        assert lower.bounding_box().min.Z >= -28.0 - 1e-6
        assert upper.bounding_box().max.Z <= 24.2514 + 1e-6


def test_B_new_hardware_does_not_occupy_counterbored_structural_material():
    concept_b = _make_concept("B")
    hardware_tokens = (
        "B_low_profile_head_",
        "B_low_profile_shank_",
        "B_opposite_washer_",
        "B_captive_nut_",
        "B_output_lower_shoulder_",
        "B_output_low_snap_retainer_",
        "B_roller_lower_shoulder_",
        "B_roller_low_snap_retainer_",
    )
    hardware = [
        child for child in _walk(concept_b) if any(token in (child.label or "") for token in hardware_tokens)
    ]
    material = _by_label(concept_b, "B_REAL_COUNTERBORED_")
    assert hardware and material
    collisions = []
    for hardware_part in hardware:
        for member in material:
            volume = _intersection_volume(hardware_part, member)
            if volume > 1e-3:
                collisions.append((hardware_part.label, member.label, volume))
    assert not collisions, f"new B hardware overlaps structural material: {collisions[:8]}"


def test_C_is_explicitly_a_three_role_local_coupon_not_a_complete_clock():
    concept_c = _make_concept("C")
    groups = [
        child
        for child in concept_c.children
        if (child.label or "").startswith("C_role_coupon_")
    ]
    assert sorted((group.label or "").removeprefix("C_role_coupon_") for group in groups) == [
        "hour",
        "minute",
        "second",
    ]
    assert not _by_label(concept_c, "M1_260T_quadrant"), (
        "C must show local ring excerpts instead of importing a full 12-quadrant annulus"
    )
    assert len(_by_label(concept_c, "16T_output_pinion")) == 3
    assert len(_by_label(concept_c, "local_ring_segment")) == 3
    for group in groups:
        box = group.bounding_box()
        assert min(box.size.X, box.size.Y) < 180.0, (
            f"{group.label} must be a local station, not a 300 mm annulus"
        )


def test_each_C_role_coupon_has_one_connected_support_and_retention_structure():
    concept_c = _make_concept("C")
    for role in ("hour", "minute", "second"):
        group = next(child for child in concept_c.children if (child.label or "") == f"C_role_coupon_{role}")
        supports = [
            child
            for child in _walk(group)
            if "connected_mount_and_capture" in (child.label or "")
        ]
        assert len(supports) == 1, f"{role} coupon needs one unibody mount/capture support"
        support = supports[0]
        assert support.is_valid and len(support.solids()) == 1 and _volume(support) > 1e-3
        labels = [child.label or "" for child in _walk(group)]
        assert any("16T_output_pinion" in label for label in labels)
        assert any("local_ring_segment" in label for label in labels)
        assert any("output_shaft" in label for label in labels)
        assert any("lower_shoulder" in label for label in labels)
        assert any("low_snap_retainer" in label for label in labels)


def test_C_role_coupon_groups_have_no_obvious_unintended_overlap():
    concept_c = _make_concept("C")
    groups = [child for child in concept_c.children if (child.label or "").startswith("C_role_coupon_")]
    for left, right in combinations(groups, 2):
        assert _intersection_volume(left, right) < 1e-4

    collisions = []
    for group in groups:
        segment = next(
            child for child in group.children if "local_ring_segment" in (child.label or "")
        )
        support = next(
            child
            for child in group.children
            if "connected_mount_and_capture" in (child.label or "")
        )

        # The shaft/bearing/pinion and motor/yoke reference solids deliberately
        # share their fitted volume.  Treat only ring clearance and retainer
        # seat clearance as collision contracts for this communication coupon.
        for fixed_part in group.children:
            label = fixed_part.label or ""
            if fixed_part is segment or "16T_output_pinion" in label:
                continue
            volume = _intersection_volume(segment, fixed_part)
            if volume > 1e-3:
                collisions.append((group.label, segment.label, label, volume))

        for retainer in group.children:
            label = retainer.label or ""
            if not (
                "roller_lower_shoulder" in label
                or "roller_low_snap_retainer" in label
            ):
                continue
            volume = _intersection_volume(retainer, support)
            if volume > 1e-3:
                collisions.append((group.label, retainer.label, support.label, volume))
    assert not collisions, f"C coupon contains unintended component overlap: {collisions[:8]}"


def test_manifest_marks_C_incomplete_and_makes_no_complete_clock_Z_claim():
    manifest_path = MODEL_ROOT / "manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    row = manifest["concepts"][ARTIFACTS["C"].name]
    assert row["complete_clock"] is False
    assert row["scope"] == "three_role_local_coupon"
    assert "complete_clock_z_envelope" not in row


def test_written_STEP_artifacts_match_their_source_factories():
    _load_module(EXPORT_MODULE)
    for key in ("A", "B", "C"):
        path = ARTIFACTS[key]
        assert path.exists(), f"missing exported concept STEP: {path}"
        exported = import_step(str(path))
        source = _make_concept(key)
        assert _bounds(exported) == pytest.approx(_bounds(source), abs=1e-5)
        assert _volume(exported) == pytest.approx(_volume(source), abs=2e-3)
        assert len(exported.solids()) == len(source.solids())
        assert _occurrence_signature(exported, frozen_drive_only=True) == _occurrence_signature(
            source, frozen_drive_only=True
        )


def test_side_by_side_comparison_is_exported_as_a_separate_review_artifact():
    path = ARTIFACTS["comparison"]
    assert path.exists(), f"missing side-by-side review STEP: {path}"
    exported = import_step(str(path))
    source = _make_concept("comparison")
    assert len(exported.solids()) >= 3
    assert _bounds(exported) == pytest.approx(_bounds(source), abs=1e-5)
