"""RED contract for the immutable-copy KAGE Phase-1 implementation.

This module is intentionally written before the production namespace exists.
It must collect cleanly and fail closed until
``p3_v3_locked_parametric_repair_r1`` implements the complete locked-copy,
parameter-ownership, and occurrence-parity APIs below.

The immutable 2026-08-18 generator and STEP are evidence inputs only.  The new
implementation may copy/modularize that accepted source, but may not modify the
locked folder or alias the rejected Revision-K R2 implementation.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from hashlib import sha256
import importlib
import inspect
from pathlib import Path
from typing import Any, Mapping

import pytest


ROOT = Path(__file__).resolve().parents[1]
LOCKED_ROOT = (
    ROOT
    / "models"
    / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
)
LOCKED_GENERATOR = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step.py"
LOCKED_STEP = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step"
MODEL_ROOT = ROOT / "models" / "p3_v3_locked_parametric_repair_r1"

SPEC_MODULE = "p3_v3_locked_parametric_repair_r1_spec"
GEOMETRY_MODULE = "p3_v3_locked_parametric_repair_r1_geometry"
PARITY_MODULE = "p3_v3_locked_parametric_repair_r1_parity"

LOCKED_HASHES = {
    LOCKED_GENERATOR: "a71d06ad5713e040295329dddb81fc8b8b2b72138d82a1b5a3798523bc7f4cac",
    LOCKED_STEP: "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7",
    LOCKED_ROOT
    / "source_snapshot"
    / "p3_v3_direct_gear_race_guidance_geometry.py": (
        "a435865878c59fbadd48ee14aa6bd3f3dd9b08aee032bb64537b9d948104ec52"
    ),
    LOCKED_ROOT / "source_snapshot" / "p3_v3_direct_gear_race_guidance_spec.py": (
        "76122f22de604ec50292bb3fceff6d5be545cdd52a4769a448bda995c8793773"
    ),
    LOCKED_ROOT / "source_snapshot" / "p3_v3_direct_gear_race_guidance_export.py": (
        "af3aea16d31a98fd0837f3302950451f0bb0069bb1147a944de181e99c820433"
    ),
}

EXPECTED_GROUPS = {
    "global_envelope",
    "role_rings",
    "gear_train",
    "motor_stations",
    "fixed_towers",
    "spine",
    "cassettes",
    "stop_plate",
    "seams",
    "stationary_joints",
    "hall_balance",
    "hardware",
    "service_states",
    "u1_layout",
    "validation",
}

EXPECTED_LOCKED_DEFAULTS = {
    "global_envelope.clock_outer_diameter_mm": 300.0,
    "global_envelope.stationary_outer_radius_mm": 150.0,
    "gear_train.ring_teeth": 260,
    "gear_train.pinion_teeth": 16,
    "gear_train.module_mm": 1.0,
    "gear_train.carrier_race_radius_mm": 131.6,
    "gear_train.tooth_tip_radius_mm": 129.0,
    "gear_train.tooth_root_radius_mm": 132.5,
    "gear_train.ring_body_outer_radius_mm": 138.9,
    "gear_train.output_axis_radius_mm": 122.0,
    "gear_train.tooth_phase_offset_deg": 0.6923076923076923,
    "role_rings.carrier_layers_mm": ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6)),
    "role_rings.pinion_face_ranges_mm": ((-0.7, 1.4), (4.85, 6.95), (10.4, 12.5)),
    "role_rings.fin_angles_deg": (305.0, 45.0, 145.0),
    "role_rings.fin_radial_ranges_mm": (
        (142.7, 143.9),
        (140.75, 141.95),
        (137.2, 138.4),
    ),
    "role_rings.fin_tangential_widths_mm": (3.0, 2.0, 1.2),
    "role_rings.fin_start_z_mm": (0.2, 5.3, 12.4),
    "role_rings.fin_tip_z_mm": (17.152, 21.1867, 24.2514),
    "motor_stations.station_angles_deg": (0.0, 120.0, 240.0),
    "motor_stations.service_adjustment_mm": 2.5,
    "motor_stations.powered_range_mm": (-0.35, 0.10),
    "motor_stations.mount_slot_width_mm": 3.6,
    "motor_stations.mount_slot_overall_length_mm": 8.6,
    "u1_layout.build_volume_mm": (260.0, 260.0, 260.0),
    "u1_layout.minimum_bed_margin_mm": 5.0,
}

REQUIRED_ROW_FIELDS = {
    "name",
    "label",
    "transform",
    "shape",
    "topology",
    "volume_mm3",
    "area_mm2",
    "aabb_mm",
    "classification",
    "owner_group",
}

ALLOWED_CLASSIFICATIONS = {
    "protected_exact",
    "allowed_local_delta",
    "new_authorized",
}


def _load(name: str):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            pytest.fail(
                f"RED: required isolated module {name!r} does not exist; "
                "do not alias a locked or rejected R2 module",
                pytrace=False,
            )
        raise


def _spec_module():
    module = _load(SPEC_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _geometry_module():
    module = _load(GEOMETRY_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _parity_module():
    module = _load(PARITY_MODULE)
    assert Path(module.__file__).resolve().parent == ROOT
    return module


def _params():
    module = _spec_module()
    assert hasattr(module, "P3_V3_LOCKED_PARAMETRIC_REPAIR_R1")
    return module.P3_V3_LOCKED_PARAMETRIC_REPAIR_R1


def _value_at(value: Any, path: str) -> Any:
    for name in path.split("."):
        value = value[name] if isinstance(value, Mapping) else getattr(value, name)
    return value


def _replace_at(value: Any, path: str, new_value: Any) -> Any:
    head, *tail = path.split(".")
    child = getattr(value, head)
    updated = _replace_at(child, ".".join(tail), new_value) if tail else new_value
    return replace(value, **{head: updated})


def _schema_rows(schema: Mapping[str, Mapping[str, Any]]):
    for group_name, group in schema.items():
        for field_name, contract in group.items():
            path = f"{group_name}.{field_name}"
            yield path, contract


def _meta(contract: Any, name: str) -> Any:
    if isinstance(contract, Mapping):
        assert name in contract, f"parameter contract missing {name!r}"
        return contract[name]
    assert hasattr(contract, name), f"parameter contract missing {name!r}"
    return getattr(contract, name)


def _assert_numeric_tree(actual: Any, expected: Any, *, path: str = "value") -> None:
    """Compare nested numeric tuples without relying on nested pytest.approx."""

    if isinstance(expected, (tuple, list)):
        assert len(actual) == len(expected), path
        for index, (actual_item, expected_item) in enumerate(zip(actual, expected)):
            _assert_numeric_tree(actual_item, expected_item, path=f"{path}[{index}]")
        return
    assert actual == pytest.approx(expected), path


def _row_map(rows):
    result = {}
    for row in rows:
        assert REQUIRED_ROW_FIELDS <= set(row), set(row)
        name = row["name"]
        assert name not in result, f"duplicate flattened occurrence {name!r}"
        result[name] = row
    return result


def _signature(row: Mapping[str, Any], parity) -> dict[str, Any]:
    fingerprint = parity.brep_fingerprint(row["shape"])
    return {
        "label": row["label"],
        "transform": tuple(row["transform"]),
        "brep_sha256": fingerprint["brep_sha256"],
        "topology": fingerprint["topology"],
        "volume_mm3": fingerprint["volume_mm3"],
        "area_mm2": fingerprint["area_mm2"],
        "aabb_mm": tuple(fingerprint["aabb_mm"]),
    }


def test_immutable_locked_inputs_have_exact_hashes_and_new_root_is_separate():
    for path, expected in LOCKED_HASHES.items():
        assert path.is_file(), path
        assert sha256(path.read_bytes()).hexdigest() == expected, path
    assert MODEL_ROOT != LOCKED_ROOT
    assert LOCKED_ROOT not in MODEL_ROOT.parents


def test_new_namespace_cannot_import_rejected_r2_or_runtime_alias_locked_geometry():
    modules = (_spec_module(), _geometry_module(), _parity_module())
    forbidden = (
        "p3_v3_direct_gear_race_guidance_r2",
        "/rollback/",
        "rollback.",
        "tests_snapshot",
    )
    for module in modules:
        path = Path(module.__file__).resolve()
        source = path.read_text()
        assert path.parent == ROOT
        assert not any(term in source for term in forbidden), path
        imports = inspect.getsource(module)
        assert "import *" not in imports


def test_locked_tree_and_default_candidate_flatten_to_exactly_201_unique_leaves():
    parity = _parity_module()
    baseline = _row_map(parity.baseline_occurrences())
    candidate = _row_map(parity.candidate_occurrences(_params()))
    assert len(baseline) == 201
    assert len(candidate) == 201
    assert set(candidate) == set(baseline)


def test_zero_delta_candidate_has_exact_label_transform_brep_and_mass_parity():
    parity = _parity_module()
    baseline = _row_map(parity.baseline_occurrences())
    candidate = _row_map(parity.candidate_occurrences(_params()))
    for name in sorted(baseline):
        assert _signature(candidate[name], parity) == _signature(baseline[name], parity), name


def test_protected_tooth_race_and_fin_masks_are_exact_locked_values():
    parity = _parity_module()
    masks = parity.protected_feature_masks()
    assert masks["ring_teeth"] == 260
    assert masks["pinion_teeth"] == 16
    assert masks["module_mm"] == pytest.approx(1.0)
    assert masks["carrier_race_radius_mm"] == pytest.approx(131.6)
    assert masks["tooth_tip_radius_mm"] == pytest.approx(129.0)
    assert masks["tooth_root_radius_mm"] == pytest.approx(132.5)
    assert masks["ring_body_outer_radius_mm"] == pytest.approx(138.9)
    _assert_numeric_tree(
        masks["carrier_layers_mm"],
        ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6)),
        path="carrier_layers_mm",
    )
    _assert_numeric_tree(
        masks["fin_radial_ranges_mm"],
        ((142.7, 143.9), (140.75, 141.95), (137.2, 138.4)),
        path="fin_radial_ranges_mm",
    )
    assert masks["fin_start_z_mm"] == pytest.approx((0.2, 5.3, 12.4))
    assert masks["fin_tip_z_mm"] == pytest.approx((17.152, 21.1867, 24.2514))
    assert masks["fin_angles_deg"] == pytest.approx((305.0, 45.0, 145.0))


def test_motor_axes_station_frames_and_complete_clock_silhouette_are_locked():
    parity = _parity_module()
    masks = parity.protected_feature_masks()
    assert masks["motor_station_angles_deg"] == pytest.approx((0.0, 120.0, 240.0))
    assert masks["output_axis_radius_mm"] == pytest.approx(122.0)
    assert masks["motor_yoke_occurrence_count"] == 3
    assert masks["nema8_occurrence_count"] == 3
    assert masks["rear_chassis_quadrant_count"] == 4
    assert masks["outer_frame_post_count"] == 6
    assert masks["overall_aabb_mm"] == pytest.approx(
        (-150.0, -150.0, -32.5, 150.0, 150.0, 24.2514), abs=1e-6
    )


def test_parameter_schema_has_all_groups_frozen_dataclasses_and_locked_defaults():
    module = _spec_module()
    params = _params()
    schema = module.parameter_schema(params)
    assert set(schema) == EXPECTED_GROUPS
    assert is_dataclass(params)
    for field in fields(params):
        group = getattr(params, field.name)
        assert is_dataclass(group), field.name
        assert getattr(group, "__dataclass_params__").frozen is True
    assert getattr(params, "__dataclass_params__").frozen is True
    with pytest.raises(FrozenInstanceError):
        params.global_envelope = params.global_envelope
    for path, expected in EXPECTED_LOCKED_DEFAULTS.items():
        _assert_numeric_tree(_value_at(params, path), expected, path=path)


def test_derived_equations_are_computed_once_from_primary_inputs():
    params = _params()
    assert params.outer_radius_mm == pytest.approx(150.0)
    assert params.gear_ratio == pytest.approx(260.0 / 16.0)
    assert params.ring_pitch_radius_mm == pytest.approx(1.0 * 260.0 / 2.0)
    assert params.pinion_pitch_radius_mm == pytest.approx(1.0 * 16.0 / 2.0)
    assert params.quadrant_teeth == 65
    assert params.motor_slot_center_travel_mm == pytest.approx(8.6 - 3.6)
    assert params.u1_usable_xy_mm == pytest.approx(260.0 - 2.0 * 5.0)
    assert params.fin_heights_mm == pytest.approx(
        (17.152 - 0.2, 21.1867 - 5.3, 24.2514 - 12.4)
    )
    assert params.fin_radial_lengths_mm == pytest.approx((1.2, 1.2, 1.2))
    params.validate()


def test_every_parameter_field_declares_units_range_lock_and_geometry_owners():
    module = _spec_module()
    schema = module.parameter_schema(_params())
    rows = list(_schema_rows(schema))
    assert rows
    for path, contract in rows:
        assert _meta(contract, "path") == path
        assert _meta(contract, "units") in {"mm", "deg", "count", "ratio", "bool", "enum"}
        assert isinstance(_meta(contract, "locked"), bool)
        owners = tuple(_meta(contract, "owner_labels"))
        assert owners, f"{path} has no geometry/placement owner"
        assert _meta(contract, "effect") in {"geometry", "transform", "placement", "metadata"}
        minimum = _meta(contract, "minimum")
        maximum = _meta(contract, "maximum")
        if minimum is not None and maximum is not None:
            assert minimum <= maximum, path
        if not _meta(contract, "locked"):
            assert _meta(contract, "probe_value") is not None, path


@pytest.mark.parametrize(
    "path,value",
    (
        ("global_envelope.clock_outer_diameter_mm", 301.0),
        ("gear_train.ring_teeth", 264),
        ("gear_train.module_mm", 1.05),
        ("gear_train.carrier_race_radius_mm", 131.7),
        ("role_rings.carrier_layers_mm", ((-1.4, 1.6), (4.05, 7.05), (9.6, 12.6))),
        ("role_rings.fin_start_z_mm", (0.3, 5.3, 12.4)),
        ("motor_stations.station_angles_deg", (1.0, 120.0, 240.0)),
    ),
)
def test_locked_fields_raise_locked_parameter_error(path, value):
    module = _spec_module()
    with pytest.raises(module.LockedParameterError, match=path):
        changed = _replace_at(_params(), path, value)
        changed.validate()


def test_every_mutable_geometry_or_transform_perturbation_changes_only_declared_owners():
    module = _spec_module()
    parity = _parity_module()
    params = _params()
    schema = module.parameter_schema(params)
    baseline = _row_map(parity.candidate_occurrences(params))
    exercised = []
    for path, contract in _schema_rows(schema):
        if _meta(contract, "locked") or _meta(contract, "effect") not in {
            "geometry",
            "transform",
        }:
            continue
        exercised.append(path)
        changed_params = _replace_at(params, path, _meta(contract, "probe_value"))
        changed_params.validate()
        changed = _row_map(parity.candidate_occurrences(changed_params))
        report = parity.diff_occurrence_sets(baseline, changed)
        changed_names = set(report["changed_occurrence_names"])
        owner_names = set(_meta(contract, "owner_labels"))
        assert changed_names, f"{path} is a dead parameter"
        assert changed_names <= owner_names, (path, changed_names - owner_names)
        assert not report["added_occurrence_names"], path
        assert not report["removed_occurrence_names"], path
        for name in set(baseline) - changed_names:
            assert _signature(changed[name], parity) == _signature(baseline[name], parity), (
                path,
                name,
            )
    assert exercised, "schema exposes no mutable geometry/transform parameters"


@pytest.mark.parametrize(
    "path,value,message",
    (
        ("motor_stations.service_adjustment_mm", -0.1, "service_adjustment"),
        ("fixed_towers.seat_bore_diameter_mm", 3.80, "seat_bore"),
        ("cassettes.pin_bore_diameter_mm", 3.80, "pin_bore"),
        ("stop_plate.window_width_mm", 2.90, "window_width"),
        ("seams.recess_depth_mm", 1.90, "recess_depth"),
        ("hall_balance.hall_pocket_radius_mm", 131.60, "hall_pocket"),
        ("u1_layout.minimum_bed_margin_mm", 131.0, "minimum_bed_margin"),
    ),
)
def test_invalid_parameter_combinations_fail_with_path_and_measured_requirement(path, value, message):
    module = _spec_module()
    with pytest.raises(ValueError, match=rf"{path}.*{message}.*(required|must|outside|clearance)"):
        changed = _replace_at(_params(), path, value)
        changed.validate()


def test_parity_manifest_classifies_every_occurrence_and_rejects_unknown_drift():
    parity = _parity_module()
    manifest = parity.parity_manifest(_params())
    rows = manifest["occurrences"]
    assert len(rows) == 201
    assert len({row["name"] for row in rows}) == 201
    assert {row["classification"] for row in rows} <= ALLOWED_CLASSIFICATIONS
    assert all(row["classification"] in ALLOWED_CLASSIFICATIONS for row in rows)
    assert manifest["unknown_occurrence_names"] == []
    assert manifest["unclassified_occurrence_names"] == []
    assert manifest["protected_drift_occurrence_names"] == []
    assert manifest["comparison_method"] == (
        "imported_locked_step_vs_imported_candidate_step"
    )
    symmetric = manifest["protected_symmetric_difference_evidence"]
    assert symmetric["method"] == (
        "OCC_boolean_cut_imported_locked_STEP_vs_imported_candidate_STEP"
    )
    assert symmetric["protected_occurrence_count"] == 201
    assert symmetric["violation_occurrence_names"] == []
    assert symmetric["tolerance_mm3"] <= 1e-7
    assert symmetric["maximum_symmetric_difference_mm3"] <= symmetric["tolerance_mm3"]
    assert len(symmetric["occurrences"]) == 201
    for occurrence in symmetric["occurrences"]:
        assert {
            "name",
            "a_minus_b_mm3",
            "b_minus_a_mm3",
            "maximum_mm3",
            "passes",
        } <= set(occurrence)
        assert occurrence["a_minus_b_mm3"] <= symmetric["tolerance_mm3"]
        assert occurrence["b_minus_a_mm3"] <= symmetric["tolerance_mm3"]
        assert occurrence["maximum_mm3"] <= symmetric["tolerance_mm3"]
        assert occurrence["passes"] is True
    rogue = dict(rows[0])
    rogue["name"] = "unauthorized_unknown_drift"
    with pytest.raises(ValueError, match="unauthorized_unknown_drift.*unknown|unknown.*unauthorized_unknown_drift"):
        parity.validate_parity_manifest([*rows, rogue])


def test_required_phase1_api_is_explicit_and_default_build_targets_only_new_root():
    geometry = _geometry_module()
    parity = _parity_module()
    assert set(inspect.signature(geometry.build_candidate).parameters) == {"params"}
    for name in (
        "baseline_occurrences",
        "candidate_occurrences",
        "protected_feature_masks",
        "parity_manifest",
        "validate_parity_manifest",
        "brep_fingerprint",
        "diff_occurrence_sets",
    ):
        assert callable(getattr(parity, name, None)), name
    built = geometry.build_candidate(_params())
    assert built["model_root"] == MODEL_ROOT
    assert LOCKED_ROOT not in Path(built["model_root"]).parents
    assert built["source_locked_hashes"] == {
        str(path.relative_to(ROOT)): digest for path, digest in LOCKED_HASHES.items()
    }
