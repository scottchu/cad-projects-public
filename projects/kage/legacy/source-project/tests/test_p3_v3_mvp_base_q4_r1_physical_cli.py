"""Exactly seven grouped tests for the accepted KAGE B0 physical CLI v3."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import subprocess

import pytest

from p3_v3_mvp_base_q4_r1_physical_contract import (
    B0ContractError,
    B0_PHYSICAL_ACCEPTANCE,
    CHECK_IDS,
    INPUT_SCHEMA,
    json_report,
    load_and_evaluate,
    text_report,
)
from p3_v3_mvp_base_q4_r1_spec import NAMESPACE, SPEC


ROOT = Path(__file__).resolve().parents[1]


def _gaps(value: float = 0.15) -> dict:
    return {
        f"S{seam}": {position: value for position in ("inner", "middle", "outer")}
        for seam in range(1, 5)
    }


def _steps(value: float = 0.10) -> dict:
    return {
        f"S{seam}-{side}": value
        for seam in range(1, 5)
        for side in ("A", "B")
    }


def _checkpoint() -> dict:
    return {
        "s4_hand_pressure_only": True,
        "forced_actions": [],
        "seam_overlap": False,
        "visible_bow": False,
        "diameters_mm": {"d0": 300.0, "d45": 300.0, "d90": 300.0, "d135": 300.0},
        "seam_gaps_mm": _gaps(),
        "seam_steps_mm": _steps(),
        "rocking": False,
        "worst_flatness_gap_mm": 0.20,
        "worst_flatness_location": "d45 outer",
        "rechecks": {},
    }


def _pass_document() -> dict:
    pins = []
    for seam in range(1, 5):
        for radius in (78, 108):
            pins.append({
                "id": f"S{seam}-R{radius}",
                "before_mm": 2.50,
                "after_mm": 2.50,
                "steady_nonimpact_pressure": True,
                "free_dropped": False,
                "impact_used": False,
                "released": False,
                "visible_movement": False,
                "damage": False,
            })
    nuts = []
    screws = []
    for seam in range(1, 5):
        for side in ("A", "B"):
            identifier = f"S{seam}-{side}"
            nuts.append({"id": identifier, "flat": True, "below_seat": True, "spun": False, "forced": False})
            screws.append({
                "id": identifier,
                "hard_before_head_contact": False,
                "bridge_moved_when_tight": False,
                "paper_remained_at_contact": False,
                "cross_threaded": False,
            })
    return {
        "schema": INPUT_SCHEMA,
        "article": NAMESPACE,
        "card_version": B0_PHYSICAL_ACCEPTANCE.card_version,
        "card_sha256": B0_PHYSICAL_ACCEPTANCE.card_sha256,
        "print": {
            "material": "PLA",
            "printer": "Snapmaker U1",
            "profile": "0.20 structural",
            "date": "2026-08-20",
            "nozzle_mm": 0.4,
            "layer_height_mm": 0.2,
        },
        "measurement_systems": {
            "od": {"name": "long caliper", "resolution_mm": 0.10, "uncertainty_mm": 0.05, "verified": True},
            "gap": {"name": "feeler set", "resolution_mm": 0.05, "uncertainty_mm": 0.025, "calibrated": True},
            "step": {"name": "feeler/indicator", "resolution_mm": 0.05, "uncertainty_mm": 0.025, "calibrated": True},
            "flatness": {"name": "straightedge/feeler", "resolution_mm": 0.10, "uncertainty_mm": 0.05, "calibrated": True},
            "pin_exposure": {"name": "digital caliper", "resolution_mm": 0.01, "uncertainty_mm": 0.01, "calibrated": True},
        },
        "reference_plane": {"kind": "verified", "verification_feeler_mm": 0.25, "passed": True, "worst_location": "north edge"},
        "hardware_fit": {"pins": pins, "nuts": nuts, "screws": screws},
        "assembly_attestations": {
            "all_quadrants_supported_in_final_xy": True,
            "bridge_insertion_order": ["S1", "S2", "S3", "S4"],
            "s4_inserted_upward_from_below": True,
            "q4_with_s4_lowering_used": False,
            "all_eight_screws_loose_before_tightening": True,
            "tightening_order": ["S1", "S3", "S2", "S4"],
            "finger_snug_only": True,
            "forced_closure_used": False,
            "unconstrained_wait_minutes": 60,
            "direct_force_or_damage_observed": False,
        },
        "cycles": [
            {"cycle": 1, "initial_assembly": True, "s4_force": "light", "damage": []},
            {"cycle": 2, "initial_assembly": False, "s4_force": "light", "damage": []},
            {"cycle": 3, "initial_assembly": False, "s4_force": "light", "damage": []},
        ],
        "checkpoints": {
            "cycle1_free_state": _checkpoint(),
            "after_vertical": _checkpoint(),
            "after_lift_place": _checkpoint(),
        },
        "vertical": {
            "down_quadrant": "Q1",
            "started_at": "2026-08-20T10:00:00-04:00",
            "ended_at": "2026-08-20T11:00:00-04:00",
            "only_down_quadrant_rim_contact": True,
            "safety_tether_load_bearing": False,
            "movement_or_disengagement": False,
        },
        "lift_place": {
            "sequence": list(B0_PHYSICAL_ACCEPTANCE.lift_sequence),
            "height_mm": 50,
            "hold_seconds": 3,
            "seam_click_or_disengagement": False,
            "hardware_moved": False,
        },
        "photos": {
            key: {"kind": "stable_id", "value": f"lab-photo:2026-08-20:{index:02d}"}
            for index, key in enumerate((
                "parts_and_hardware", "hardware_fit", "reference_plane",
                "supported_quadrants_s1_s3", "s4_half_inserted", "s4_fully_seated",
                "cycle1_front", "cycle1_underside", "od_measurement_setup",
                "worst_seam_measurement", "worst_flatness_measurement",
                "vertical_start_q1_down", "vertical_end_q1_down", "final_front",
                "final_underside",
            ), start=1)
        },
    }


def _write(tmp_path: Path, doc: dict, name: str = "results.json") -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def _evaluate(tmp_path: Path, doc: dict, name: str = "results.json") -> dict:
    return load_and_evaluate(_write(tmp_path, doc, name))


def _check(payload: dict, check_id: str) -> dict:
    return next(row for row in payload["checks"] if row["id"] == check_id)


def test_group_1_installed_uv_cli_six_check_mapping_and_output_parity(tmp_path: Path):
    path = _write(tmp_path, _pass_document())
    text = subprocess.run(
        ["uv", "run", "kage-clock", "b0-evaluate", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    machine = subprocess.run(
        ["uv", "run", "kage-clock", "--json", "b0-evaluate", str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    after = subprocess.run(
        ["uv", "run", "kage-clock", "b0-evaluate", str(path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert text.returncode == machine.returncode == after.returncode == 0
    payload = json.loads(machine.stdout)
    assert payload == json.loads(after.stdout)
    assert payload["overall_status"] == "pass"
    assert tuple(row["id"] for row in payload["checks"]) == CHECK_IDS
    assert len(payload["checks"]) == 6
    assert all(row["status"] == "pass" for row in payload["checks"])
    assert "KAGE B0 Q4-R1: PASS" in text.stdout
    assert "independent acceptance still required" in text.stdout
    assert text.stderr == machine.stderr == after.stderr == ""


def test_group_2_od_uncertainty_complete_rechecks_and_negatives(tmp_path: Path):
    inside = _evaluate(tmp_path, _pass_document(), "inside.json")
    assert _check(inside, "01_loop_od")["status"] == "pass"

    touching_doc = _pass_document()
    touching_doc["checkpoints"]["cycle1_free_state"]["diameters_mm"]["d0"] = 299.55
    touching = _evaluate(tmp_path, touching_doc, "touching.json")
    assert _check(touching, "01_loop_od")["status"] == "borderline"

    exact_recheck = deepcopy(touching_doc)
    exact_recheck["checkpoints"]["cycle1_free_state"]["rechecks"]["od"] = {
        "d0": 299.50, "d45": 299.75, "d90": 299.75, "d135": 300.00
    }
    exact = _evaluate(tmp_path, exact_recheck, "exact.json")
    assert _check(exact, "01_loop_od")["status"] == "pass"
    assert exact["derived"]["cycle1_free_state"]["od_range_mm"] == 0.5

    outside = _pass_document()
    outside["checkpoints"]["cycle1_free_state"]["diameters_mm"]["d0"] = 299.40
    assert _check(_evaluate(tmp_path, outside, "outside.json"), "01_loop_od")["status"] == "fail"

    partial = deepcopy(touching_doc)
    partial["checkpoints"]["cycle1_free_state"]["rechecks"]["od"] = {"d0": 299.50}
    assert _check(_evaluate(tmp_path, partial, "partial.json"), "01_loop_od")["status"] == "incomplete"

    bad_recheck = deepcopy(touching_doc)
    bad_recheck["checkpoints"]["cycle1_free_state"]["rechecks"]["od"] = {
        "d0": 299.49, "d45": 300.0, "d90": 300.0, "d135": 300.0
    }
    assert _check(_evaluate(tmp_path, bad_recheck, "bad-recheck.json"), "01_loop_od")["status"] == "fail"

    forbidden = deepcopy(touching_doc)
    forbidden["checkpoints"]["cycle1_free_state"]["rechecks"]["od"] = {
        "d0": 299.50, "d45": 299.75, "d90": 299.75, "d135": 300.00,
        "range_mm": 0.50,
    }
    with pytest.raises(B0ContractError):
        _evaluate(tmp_path, forbidden, "forbidden.json")

    untriggered = _pass_document()
    untriggered["checkpoints"]["cycle1_free_state"]["rechecks"]["od"] = {
        "d0": 300.0, "d45": 300.0, "d90": 300.0, "d135": 300.0
    }
    with pytest.raises(B0ContractError, match="without a corresponding BORDERLINE trigger"):
        _evaluate(tmp_path, untriggered, "untriggered-od.json")
    untriggered_cli = subprocess.run(
        ["uv", "run", "kage-clock", "b0-evaluate", str(tmp_path / "untriggered-od.json"), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert untriggered_cli.returncode == 2
    assert untriggered_cli.stdout == ""
    assert "without a corresponding BORDERLINE trigger" in untriggered_cli.stderr


def test_group_3_gap_step_flatness_uncertainty_rechecks_and_boundaries(tmp_path: Path):
    gap_touch = _pass_document()
    gap_touch["checkpoints"]["after_lift_place"]["seam_gaps_mm"]["S1"]["inner"] = 0.075
    assert _check(_evaluate(tmp_path, gap_touch, "gap-touch.json"), "02_seam_gap_step")["status"] == "borderline"
    gap_exact = deepcopy(gap_touch)
    gap_exact["checkpoints"]["after_lift_place"]["rechecks"]["seam_gaps"] = _gaps(0.05)
    assert _check(_evaluate(tmp_path, gap_exact, "gap-exact.json"), "02_seam_gap_step")["status"] == "pass"
    gap_out = _pass_document()
    gap_out["checkpoints"]["after_lift_place"]["seam_gaps_mm"]["S1"]["inner"] = 0.01
    assert _check(_evaluate(tmp_path, gap_out, "gap-out.json"), "02_seam_gap_step")["status"] == "fail"

    step_touch = _pass_document()
    step_touch["checkpoints"]["cycle1_free_state"]["seam_steps_mm"]["S1-A"] = 0.225
    assert _check(_evaluate(tmp_path, step_touch, "step-touch.json"), "02_seam_gap_step")["status"] == "borderline"
    step_exact = deepcopy(step_touch)
    step_exact["checkpoints"]["cycle1_free_state"]["rechecks"]["seam_steps"] = _steps(0.25)
    assert _check(_evaluate(tmp_path, step_exact, "step-exact.json"), "02_seam_gap_step")["status"] == "pass"
    step_out = _pass_document()
    step_out["checkpoints"]["cycle1_free_state"]["seam_steps_mm"]["S1-A"] = 0.30
    assert _check(_evaluate(tmp_path, step_out, "step-out.json"), "02_seam_gap_step")["status"] == "fail"

    flat_touch = _pass_document()
    flat_touch["checkpoints"]["cycle1_free_state"]["worst_flatness_gap_mm"] = 0.45
    assert _check(_evaluate(tmp_path, flat_touch, "flat-touch.json"), "03_free_state_flatness")["status"] == "borderline"
    flat_exact = deepcopy(flat_touch)
    flat_exact["checkpoints"]["cycle1_free_state"]["rechecks"]["flatness"] = {
        "rocking": False, "worst_flatness_gap_mm": 0.50, "worst_flatness_location": "outer"
    }
    assert _check(_evaluate(tmp_path, flat_exact, "flat-exact.json"), "03_free_state_flatness")["status"] == "pass"
    flat_out = _pass_document()
    flat_out["checkpoints"]["cycle1_free_state"]["worst_flatness_gap_mm"] = 0.56
    assert _check(_evaluate(tmp_path, flat_out, "flat-out.json"), "03_free_state_flatness")["status"] == "fail"

    coarse = _pass_document()
    coarse["measurement_systems"]["gap"]["resolution_mm"] = 1.0
    coarse["measurement_systems"]["step"]["resolution_mm"] = 1.0
    coarse["measurement_systems"]["flatness"]["resolution_mm"] = 1.0
    assert _evaluate(tmp_path, coarse, "coarse.json")["overall_status"] == "pass"
    paper = _pass_document()
    del paper["checkpoints"]["cycle1_free_state"]["seam_gaps_mm"]
    paper["checkpoints"]["cycle1_free_state"]["paper_screen"] = True
    paper_result = _evaluate(tmp_path, paper, "paper.json")
    assert paper_result["overall_status"] == "incomplete"
    assert "checkpoints.cycle1_free_state.seam_gaps_mm" in paper_result["missing_fields"]

    exact_pin_fail = _pass_document()
    exact_pin_fail["hardware_fit"]["pins"][0]["before_mm"] = 2.49
    assert _check(_evaluate(tmp_path, exact_pin_fail, "pin.json"), "04_service_cycles")["status"] == "fail"
    short_wait = _pass_document()
    short_wait["assembly_attestations"]["unconstrained_wait_minutes"] = 59
    assert _check(_evaluate(tmp_path, short_wait, "wait.json"), "03_free_state_flatness")["status"] == "incomplete"

    for family, recheck in (
        ("seam_gaps", _gaps(0.15)),
        ("seam_steps", _steps(0.10)),
        ("flatness", {"rocking": False, "worst_flatness_gap_mm": 0.20, "worst_flatness_location": "outer"}),
    ):
        untriggered = _pass_document()
        untriggered["checkpoints"]["cycle1_free_state"]["rechecks"][family] = recheck
        with pytest.raises(B0ContractError, match="without a corresponding BORDERLINE trigger"):
            _evaluate(tmp_path, untriggered, f"untriggered-{family}.json")


def test_group_4_hardware_and_assembly_sensitivity(tmp_path: Path):
    cases = []
    pin_motion = _pass_document()
    pin_motion["hardware_fit"]["pins"][0]["after_mm"] = 2.51
    cases.append(pin_motion)
    for flag, rejected in (
        ("steady_nonimpact_pressure", False),
        ("free_dropped", True),
        ("impact_used", True),
        ("released", True),
        ("visible_movement", True),
        ("damage", True),
    ):
        pin_flag = _pass_document()
        pin_flag["hardware_fit"]["pins"][0][flag] = rejected
        cases.append(pin_flag)
    for flag, rejected in (("flat", False), ("below_seat", False), ("spun", True), ("forced", True)):
        nut = _pass_document()
        nut["hardware_fit"]["nuts"][0][flag] = rejected
        cases.append(nut)
    for flag in ("hard_before_head_contact", "bridge_moved_when_tight", "paper_remained_at_contact", "cross_threaded"):
        screw = _pass_document()
        screw["hardware_fit"]["screws"][0][flag] = True
        cases.append(screw)
    for index, doc in enumerate(cases):
        assert _check(_evaluate(tmp_path, doc, f"hardware-{index}.json"), "04_service_cycles")["status"] == "fail"

    for field in (
        "all_quadrants_supported_in_final_xy",
        "s4_inserted_upward_from_below",
        "all_eight_screws_loose_before_tightening",
        "finger_snug_only",
    ):
        doc = _pass_document()
        doc["assembly_attestations"][field] = False
        assert _check(_evaluate(tmp_path, doc, f"method-{field}.json"), "01_loop_od")["status"] == "incomplete"
    order = _pass_document()
    order["assembly_attestations"]["bridge_insertion_order"] = ["S1", "S2", "S4", "S3"]
    assert _check(_evaluate(tmp_path, order, "order.json"), "01_loop_od")["status"] == "incomplete"
    forced = _pass_document()
    forced["assembly_attestations"]["forced_closure_used"] = True
    assert _check(_evaluate(tmp_path, forced, "forced.json"), "01_loop_od")["status"] == "fail"
    damaged = _pass_document()
    damaged["assembly_attestations"]["direct_force_or_damage_observed"] = True
    assert _check(_evaluate(tmp_path, damaged, "damaged.json"), "01_loop_od")["status"] == "fail"


def test_group_5_cycles_handling_and_post_handling_growth(tmp_path: Path):
    c2 = _pass_document()
    c2["cycles"][0]["s4_force"] = "free"
    c2["cycles"][1]["s4_force"] = "light"
    assert _check(_evaluate(tmp_path, c2, "c2.json"), "04_service_cycles")["status"] == "fail"
    c3 = _pass_document()
    c3["cycles"][1]["s4_force"] = "free"
    c3["cycles"][2]["s4_force"] = "light"
    assert _check(_evaluate(tmp_path, c3, "c3.json"), "04_service_cycles")["status"] == "fail"

    short_vertical = _pass_document()
    short_vertical["vertical"]["ended_at"] = "2026-08-20T10:59:59-04:00"
    assert _check(_evaluate(tmp_path, short_vertical, "short-v.json"), "05_vertical_retention")["status"] == "incomplete"
    moved_vertical = _pass_document()
    moved_vertical["vertical"]["movement_or_disengagement"] = True
    assert _check(_evaluate(tmp_path, moved_vertical, "moved-v.json"), "05_vertical_retention")["status"] == "fail"
    short_lift = _pass_document()
    short_lift["lift_place"]["height_mm"] = 49.9
    assert _check(_evaluate(tmp_path, short_lift, "short-l.json"), "06_lift_place")["status"] == "incomplete"
    moved_lift = _pass_document()
    moved_lift["lift_place"]["hardware_moved"] = True
    assert _check(_evaluate(tmp_path, moved_lift, "moved-l.json"), "06_lift_place")["status"] == "fail"

    below = _pass_document()
    below["checkpoints"]["after_vertical"]["seam_gaps_mm"]["S1"]["inner"] = 0.199
    assert _check(_evaluate(tmp_path, below, "growth-below.json"), "02_seam_gap_step")["status"] == "pass"
    equal = _pass_document()
    equal["checkpoints"]["after_vertical"]["seam_gaps_mm"]["S1"]["inner"] = 0.20
    assert _check(_evaluate(tmp_path, equal, "growth-equal.json"), "02_seam_gap_step")["status"] == "borderline"
    above = _pass_document()
    above["checkpoints"]["after_vertical"]["seam_gaps_mm"]["S1"]["inner"] = 0.201
    assert _check(_evaluate(tmp_path, above, "growth-above.json"), "02_seam_gap_step")["status"] == "fail"

    one_recheck = deepcopy(equal)
    one_recheck["checkpoints"]["cycle1_free_state"]["rechecks"]["seam_gaps"] = _gaps(0.16)
    assert _check(_evaluate(tmp_path, one_recheck, "one-recheck.json"), "02_seam_gap_step")["status"] == "incomplete"
    paired = deepcopy(one_recheck)
    paired["checkpoints"]["after_vertical"]["rechecks"]["seam_gaps"] = _gaps(0.16)
    paired_result = _evaluate(tmp_path, paired, "paired.json")
    assert _check(paired_result, "02_seam_gap_step")["status"] == "pass"
    assert paired_result["derived"]["post_handling_growth"]["worst_sequential_gap_delta_mm"] == 0.0
    assert paired_result["derived"]["cycle1_free_state"]["worst_gap_mm"] == 0.16
    assert paired_result["derived"]["after_vertical"]["worst_gap_mm"] == 0.16
    positive = deepcopy(one_recheck)
    positive["checkpoints"]["after_vertical"]["rechecks"]["seam_gaps"] = _gaps(0.17)
    assert _check(_evaluate(tmp_path, positive, "positive.json"), "02_seam_gap_step")["status"] == "fail"

    newest_pair = _pass_document()
    newest_pair["checkpoints"]["after_vertical"]["seam_gaps_mm"]["S1"]["inner"] = 0.20
    newest_pair["checkpoints"]["after_lift_place"]["seam_gaps_mm"]["S1"]["inner"] = 0.20
    newest_pair["checkpoints"]["cycle1_free_state"]["rechecks"]["seam_gaps"] = _gaps(0.16)
    newest_pair["checkpoints"]["after_vertical"]["rechecks"]["seam_gaps"] = _gaps(0.16)
    newest_pair["checkpoints"]["after_lift_place"]["rechecks"]["seam_gaps"] = _gaps(0.17)
    newest = _evaluate(tmp_path, newest_pair, "newest.json")
    assert _check(newest, "02_seam_gap_step")["status"] == "fail"
    assert newest["derived"]["post_handling_growth"]["worst_cumulative_gap_delta_mm"] == 0.01

    step_equal = _pass_document()
    step_equal["checkpoints"]["after_vertical"]["seam_steps_mm"]["S1-A"] = 0.15
    assert _check(_evaluate(tmp_path, step_equal, "step-growth-equal.json"), "02_seam_gap_step")["status"] == "borderline"
    step_paired = deepcopy(step_equal)
    step_paired["checkpoints"]["cycle1_free_state"]["rechecks"]["seam_steps"] = _steps(0.12)
    step_paired["checkpoints"]["after_vertical"]["rechecks"]["seam_steps"] = _steps(0.12)
    step_paired_result = _evaluate(tmp_path, step_paired, "step-growth-paired.json")
    assert _check(step_paired_result, "02_seam_gap_step")["status"] == "pass"
    assert step_paired_result["derived"]["after_vertical"]["worst_step_mm"] == 0.12
    step_above = _pass_document()
    step_above["checkpoints"]["after_vertical"]["seam_steps_mm"]["S1-A"] = 0.151
    assert _check(_evaluate(tmp_path, step_above, "step-growth-above.json"), "02_seam_gap_step")["status"] == "fail"

    absurd_gap = deepcopy(equal)
    absurd_gap["checkpoints"]["cycle1_free_state"]["rechecks"]["seam_gaps"] = _gaps(0.16)
    absurd_gap["checkpoints"]["after_vertical"]["rechecks"]["seam_gaps"] = _gaps(0.16)
    absurd_gap["checkpoints"]["after_vertical"]["rechecks"]["seam_gaps"]["S1"]["inner"] = 9.0
    absurd_gap_path = _write(tmp_path, absurd_gap, "absurd-gap.json")
    absurd_gap_cli = subprocess.run(
        ["uv", "run", "kage-clock", "b0-evaluate", str(absurd_gap_path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert absurd_gap_cli.returncode == 1
    absurd_gap_payload = json.loads(absurd_gap_cli.stdout)
    assert _check(absurd_gap_payload, "02_seam_gap_step")["status"] == "fail"
    assert absurd_gap_payload["derived"]["after_vertical"]["worst_gap_mm"] == 9.0

    absurd_step = deepcopy(step_equal)
    absurd_step["checkpoints"]["cycle1_free_state"]["rechecks"]["seam_steps"] = _steps(0.12)
    absurd_step["checkpoints"]["after_vertical"]["rechecks"]["seam_steps"] = _steps(0.12)
    absurd_step["checkpoints"]["after_vertical"]["rechecks"]["seam_steps"]["S1-A"] = 9.0
    absurd_step_payload = _evaluate(tmp_path, absurd_step, "absurd-step.json")
    assert _check(absurd_step_payload, "02_seam_gap_step")["status"] == "fail"
    assert absurd_step_payload["derived"]["after_vertical"]["worst_step_mm"] == 9.0


def test_group_6_missing_malformed_and_photo_evidence(tmp_path: Path):
    for key in _pass_document()["photos"]:
        doc = _pass_document()
        del doc["photos"][key]
        payload = _evaluate(tmp_path, doc, f"missing-{key}.json")
        assert payload["exit_code"] == 4
        assert f"photos.{key}" in payload["missing_fields"]

    photo_file = tmp_path / "one.jpg"
    photo_file.write_bytes(b"not inspected by evaluator")
    local = _pass_document()
    local["photos"]["parts_and_hardware"] = {"kind": "local_path", "value": "one.jpg"}
    assert _evaluate(tmp_path, local, "local.json")["overall_status"] == "pass"
    missing_photo = _pass_document()
    missing_photo["photos"]["parts_and_hardware"] = {"kind": "local_path", "value": "missing.jpg"}
    assert _evaluate(tmp_path, missing_photo, "missing-photo.json")["overall_status"] == "incomplete"
    invalid_id = _pass_document()
    invalid_id["photos"]["parts_and_hardware"] = {"kind": "stable_id", "value": "bad id"}
    assert _evaluate(tmp_path, invalid_id, "bad-id.json")["overall_status"] == "incomplete"
    array_photo = _pass_document()
    array_photo["photos"]["parts_and_hardware"] = [{"kind": "stable_id", "value": "one"}]
    assert _evaluate(tmp_path, array_photo, "array.json")["overall_status"] == "incomplete"

    for key, value in (("schema", "wrong"), ("card_version", "v2"), ("card_sha256", "0" * 64)):
        doc = _pass_document()
        doc[key] = value
        with pytest.raises(B0ContractError):
            _evaluate(tmp_path, doc, f"bad-{key}.json")
    bad_schema_path = _write(tmp_path, {**_pass_document(), "schema": "wrong"}, "bad-schema-cli.json")
    schema_cli = subprocess.run(
        ["uv", "run", "kage-clock", "b0-evaluate", str(bad_schema_path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert schema_cli.returncode == 2 and schema_cli.stdout == ""
    assert "error:" in schema_cli.stderr
    boolean_number = _pass_document()
    boolean_number["print"]["nozzle_mm"] = True
    with pytest.raises(B0ContractError):
        _evaluate(tmp_path, boolean_number, "bool.json")
    duplicate = _pass_document()
    duplicate["hardware_fit"]["pins"][1]["id"] = duplicate["hardware_fit"]["pins"][0]["id"]
    with pytest.raises(B0ContractError):
        _evaluate(tmp_path, duplicate, "duplicate.json")
    nan_path = tmp_path / "nan.json"
    nan_path.write_text(json.dumps(_pass_document()).replace('"nozzle_mm": 0.4', '"nozzle_mm": NaN'), encoding="utf-8")
    with pytest.raises(B0ContractError):
        load_and_evaluate(nan_path)


def test_group_7_single_source_precedence_and_deterministic_reporting(tmp_path: Path):
    assert B0_PHYSICAL_ACCEPTANCE.od_min_mm == Decimal(str(SPEC.base_outer_diameter_mm)) - B0_PHYSICAL_ACCEPTANCE.od_tolerance_mm
    assert B0_PHYSICAL_ACCEPTANCE.od_max_mm == Decimal(str(SPEC.base_outer_diameter_mm)) + B0_PHYSICAL_ACCEPTANCE.od_tolerance_mm
    assert B0_PHYSICAL_ACCEPTANCE.pin_target_exposure_mm == Decimal(str(SPEC.base_split_slip_engagement_mm))
    assert len(_pass_document()["hardware_fit"]["pins"]) == SPEC.dowel_count_total

    fail_missing = _pass_document()
    fail_missing["hardware_fit"]["nuts"][0]["forced"] = True
    del fail_missing["photos"]["final_front"]
    failed = _evaluate(tmp_path, fail_missing, "fail-missing.json")
    assert failed["overall_status"] == "fail" and failed["exit_code"] == 1
    assert _check(failed, "06_lift_place")["status"] == "incomplete"

    incomplete_borderline = _pass_document()
    incomplete_borderline["checkpoints"]["cycle1_free_state"]["diameters_mm"]["d0"] = 299.55
    del incomplete_borderline["photos"]["final_front"]
    mixed = _evaluate(tmp_path, incomplete_borderline, "mixed.json")
    assert mixed["overall_status"] == "incomplete" and mixed["exit_code"] == 4
    assert _check(mixed, "01_loop_od")["status"] == "borderline"

    borderline_doc = _pass_document()
    borderline_doc["checkpoints"]["cycle1_free_state"]["diameters_mm"]["d0"] = 299.55
    borderline_path = _write(tmp_path, borderline_doc, "borderline-cli.json")
    for name, expected_code in (("fail-missing.json", 1), ("mixed.json", 4), (borderline_path.name, 3)):
        result = subprocess.run(
            ["uv", "run", "kage-clock", "b0-evaluate", str(tmp_path / name), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == expected_code
        assert json.loads(result.stdout)["exit_code"] == expected_code

    stable = _evaluate(tmp_path, _pass_document(), "stable.json")
    assert json_report(stable) == json_report(load_and_evaluate(tmp_path / "stable.json"))
    text = text_report(stable)
    positions = [text.index(label) for label in (
        "01 loop + OD", "02 seam gap + step", "03 free-state flatness",
        "04 three service cycles", "05 vertical retention", "06 ten lift/place cycles",
    )]
    assert positions == sorted(positions)
    assert stable["derived"]["cycle1_free_state"]["od_range_interval_mm"] == [0.0, 0.1]
    assert all(set(row) == {"id", "status", "reasons"} for row in stable["checks"])
