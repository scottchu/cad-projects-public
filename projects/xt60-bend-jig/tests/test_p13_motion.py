from __future__ import annotations

import importlib.util
import json
import math
import shutil
import subprocess
from pathlib import Path

import pytest
from build123d import Pos, Rot

from xt60_bend_jig.p13_four_plate_three_rod import (
    GUIDE_DIRECTIONS,
    P13_DEFAULTS,
    ROD_NAMES,
    build_actuator_shaft,
    build_fixed_plate,
    build_left_cam,
    build_left_cap,
    build_right_actuator,
    build_right_cap,
    build_rod,
    build_shaft_keeper,
    build_workpiece,
    common_travel,
    rod_center,
)


ROOT = Path(__file__).resolve().parents[1]
MOTION_ENTRY = ROOT / "cad/p13_four_plate_three_rod/p13_motion.step.py"
MOTION_SIDECAR = ROOT / "cad/p13_four_plate_three_rod/p13_motion.params.js"
MOTION_STEP = ROOT / "cad/p13_four_plate_three_rod/p13_motion.step"
MOTION_PACKAGE = (
    ROOT
    / "cad/p13_four_plate_three_rod/__cadgen__/models/p13_motion.step.py/assembly.json"
)
EXPECTED_NAMES = (
    "motion_fixed_left_plate",
    "motion_fixed_right_plate",
    "motion_fixed_shaft_keeper",
    "motion_fixed_workpiece",
    "motion_rotating_left_cam",
    "motion_rotating_right_actuator",
    "motion_rotating_shaft",
    "motion_upright_rod",
    "motion_upright_left_cap",
    "motion_upright_right_cap",
    "motion_bottom_rod",
    "motion_bottom_left_cap",
    "motion_bottom_right_cap",
    "motion_diagonal_rod",
    "motion_diagonal_left_cap",
    "motion_diagonal_right_cap",
)


def _load_motion_entry():
    spec = importlib.util.spec_from_file_location("p13_motion_step", MOTION_ENTRY)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _node_binary() -> str:
    candidates = [
        shutil.which("node"),
        "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    pytest.skip("Node runtime is unavailable")


def _node_solutions(values: list[float]) -> dict:
    script = """
import { solveMotion, loopMotion } from %s;
const values = JSON.parse(process.argv[1]);
console.log(JSON.stringify({
  solutions: values.map((value) => solveMotion(value)),
  loop: [0, 1.5, 3, 4.5, 6, 12].map((time) => loopMotion(time, 6)),
}));
""" % json.dumps(MOTION_SIDECAR.as_uri())
    completed = subprocess.run(
        [_node_binary(), "--input-type=module", "-e", script, json.dumps(values)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _node_effect_records(values: list[float]) -> dict:
    script = """
import definition, { FEATURE_NAMES, solveMotion } from %s;
const values = JSON.parse(process.argv[1]);
const records = values.map((motion) => {
  const calls = [];
  definition.update({
    params: { motion },
    effects: { transform(target, spec) { calls.push({ target, spec }); } },
  });
  return { motion, solved: solveMotion(motion), calls };
});
console.log(JSON.stringify({ featureNames: FEATURE_NAMES, records }));
""" % json.dumps(MOTION_SIDECAR.as_uri())
    completed = subprocess.run(
        [_node_binary(), "--input-type=module", "-e", script, json.dumps(values)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _symmetric_difference_volume(first, second) -> float:
    return float((first - second).volume) + float((second - first).volume)


def test_motion_entry_has_exact_sixteen_stable_open_occurrences_and_envelope() -> None:
    envelope = _load_motion_entry().gen_step()
    assert set(envelope) == {"shape", "params"}
    assert envelope["params"] == "p13_motion.params.js"
    shape = envelope["shape"]
    assert len(shape.children) == 16
    assert tuple(child.label for child in shape.children) == EXPECTED_NAMES
    assert len(shape.solids()) == 16
    assert all(child.is_valid and child.volume > 0 for child in shape.children)


def test_motion_open_occurrences_reuse_exact_current_p13_solids() -> None:
    p = P13_DEFAULTS
    theta = p.open_angle_deg
    expected = [
        build_fixed_plate("left", p),
        build_fixed_plate("right", p),
        build_shaft_keeper(p),
        list(build_workpiece(p).children)[0],
        build_left_cam(theta, p),
        build_right_actuator(theta, p),
        build_actuator_shaft(theta, p),
    ]
    for name in ROD_NAMES:
        expected.extend(
            [
                build_rod(name, theta, p),
                build_left_cap(name, theta, p),
                build_right_cap(name, theta, p),
            ]
        )
    actual = list(_load_motion_entry().build_motion_open().children)
    assert len(actual) == len(expected) == 16
    for actual_shape, expected_shape in zip(actual, expected, strict=True):
        assert _symmetric_difference_volume(actual_shape, expected_shape) <= 1.0e-7


def test_javascript_solver_matches_python_kinematics_on_dense_grid() -> None:
    p = P13_DEFAULTS
    values = [index / 400.0 for index in range(401)]
    payload = _node_solutions(values)
    assert len(payload["solutions"]) == len(values)
    for motion, solved in zip(values, payload["solutions"], strict=True):
        theta = p.locked_angle_deg * motion
        assert solved["motion"] == pytest.approx(motion, abs=1.0e-14)
        assert solved["thetaDeg"] == pytest.approx(theta, abs=1.0e-12)
        assert solved["travel"] == pytest.approx(common_travel(theta, p), abs=1.0e-12)
        for name in ROD_NAMES:
            expected = rod_center(name, theta, p)
            opened = rod_center(name, p.open_angle_deg, p)
            assert solved["centers"][name] == pytest.approx([expected.y, expected.z], abs=1.0e-12)
            assert solved["translations"][name] == pytest.approx(
                [0.0, expected.y - opened.y, expected.z - opened.z], abs=1.0e-12
            )
        assert solved["shaftOrigin"] == pytest.approx(
            [0.0, p.shaft_y, p.shaft_z], abs=5.0e-13
        )
        assert solved["shaftAxis"] == [1.0, 0.0, 0.0]


def test_motion_contact_preload_directions_and_loop_are_exact() -> None:
    p = P13_DEFAULTS
    rise_motion = p.rise_end_deg / p.locked_angle_deg
    payload = _node_solutions([0.0, rise_motion, 0.9, 1.0])
    solutions = payload["solutions"]
    assert solutions[0]["travel"] == pytest.approx(0.0, abs=1.0e-14)
    assert solutions[1]["travel"] == pytest.approx(p.contact_stroke, abs=1.0e-12)
    assert p.contact_stroke < solutions[2]["travel"] < p.common_stroke
    assert solutions[3]["travel"] == pytest.approx(p.common_stroke, abs=1.0e-12)
    assert payload["loop"] == pytest.approx([0.0, 0.5, 1.0, 0.5, 0.0, 0.0], abs=1.0e-14)

    for name in ROD_NAMES:
        locked = p.locked_centres[name]
        assert solutions[1]["centers"][name] == pytest.approx(
            [p.contact_centres[name].y, p.contact_centres[name].z], abs=1.0e-12
        )
        opened = rod_center(name, p.open_angle_deg, p)
        guide = GUIDE_DIRECTIONS[name]
        delta = (locked.y - opened.y, locked.z - opened.z)
        assert delta == pytest.approx(
            (guide.y * p.common_stroke, guide.z * p.common_stroke), abs=1.0e-12
        )
        assert math.hypot(*delta) == pytest.approx(p.common_stroke, abs=1.0e-12)


def test_sidecar_is_self_contained_name_based_and_declares_exact_loop_contract() -> None:
    source = MOTION_SIDECAR.read_text()
    assert not any(line.lstrip().startswith("import ") for line in source.splitlines())
    assert "durationSeconds: 6.0" in source
    assert "open_lock_open" in source
    assert "thetaDeg = MOTION_CONSTANTS.lockedAngleDeg * normalizedMotion" in source
    assert "names: [name]" in source
    for name in EXPECTED_NAMES:
        assert name in source
    assert "#o" not in source
    assert MOTION_STEP.parent == MOTION_SIDECAR.parent


def test_default_update_emits_only_exact_rotating_and_translating_effects() -> None:
    p = P13_DEFAULTS
    values = [0.0, 0.5, p.rise_end_deg / p.locked_angle_deg, 1.0]
    payload = _node_effect_records(values)
    rotation_targets = {
        "rotating_left_cam",
        "rotating_right_actuator",
        "rotating_shaft",
    }
    translation_targets = {
        f"{name}_{role}"
        for name in ROD_NAMES
        for role in ("rod", "left_cap", "right_cap")
    }
    fixed_targets = {
        "fixed_left_plate",
        "fixed_right_plate",
        "fixed_shaft_keeper",
        "fixed_workpiece",
    }

    for motion, record in zip(values, payload["records"], strict=True):
        calls = record["calls"]
        assert len(calls) == 12
        assert {call["target"] for call in calls[:3]} == rotation_targets
        assert {call["target"] for call in calls[3:]} == translation_targets
        assert not ({call["target"] for call in calls} & fixed_targets)

        theta = p.locked_angle_deg * motion
        for call in calls[:3]:
            rotate = call["spec"]["rotate"]
            assert rotate["origin"] == pytest.approx(
                [0.0, p.shaft_y, p.shaft_z], abs=5.0e-13
            )
            assert rotate["axis"] == [1.0, 0.0, 0.0]
            assert rotate["angleDeg"] == pytest.approx(theta, abs=1.0e-12)

        for call in calls[3:]:
            name = call["target"].split("_", 1)[0]
            opened = rod_center(name, p.open_angle_deg, p)
            posed = rod_center(name, theta, p)
            assert call["spec"]["translate"] == pytest.approx(
                [0.0, posed.y - opened.y, posed.z - opened.z], abs=1.0e-12
            )


def test_generated_package_registers_sidecar_and_resolves_each_feature_once() -> None:
    package = json.loads(MOTION_PACKAGE.read_text())
    assert package["paramsPath"] == "p13_motion.params.js"
    occurrences = package["occurrences"]
    occurrence_names = [occurrence["name"] for occurrence in occurrences]
    assert len(occurrences) == len(set(occurrence_names)) == 16
    assert set(occurrence_names) == set(EXPECTED_NAMES)
    assert package["stats"]["occurrenceCount"] == 16
    assert package["stats"]["shapeCount"] == 16

    feature_names = _node_effect_records([0.0])["featureNames"]
    assert len(feature_names) == 16
    assert set(feature_names.values()) == set(EXPECTED_NAMES)
    for target_name in feature_names.values():
        assert occurrence_names.count(target_name) == 1


@pytest.mark.parametrize("motion", [0.0, 0.5, 22.0 / 27.0, 1.0])
def test_every_viewer_moved_open_solid_equals_source_built_pose(motion: float) -> None:
    p = P13_DEFAULTS
    theta = p.locked_angle_deg * motion
    open_theta = p.open_angle_deg
    pivot_rotation = (
        Pos(0.0, p.shaft_y, p.shaft_z)
        * Rot(theta, 0.0, 0.0)
        * Pos(0.0, -p.shaft_y, -p.shaft_z)
    )

    rotating_pairs = (
        (build_left_cam(open_theta, p), build_left_cam(theta, p)),
        (build_right_actuator(open_theta, p), build_right_actuator(theta, p)),
        (build_actuator_shaft(open_theta, p), build_actuator_shaft(theta, p)),
    )
    for opened, source_pose in rotating_pairs:
        assert _symmetric_difference_volume(pivot_rotation * opened, source_pose) <= 1.0e-7

    for name in ROD_NAMES:
        opened_center = rod_center(name, open_theta, p)
        posed_center = rod_center(name, theta, p)
        translation = Pos(
            0.0,
            posed_center.y - opened_center.y,
            posed_center.z - opened_center.z,
        )
        translating_pairs = (
            (build_rod(name, open_theta, p), build_rod(name, theta, p)),
            (build_left_cap(name, open_theta, p), build_left_cap(name, theta, p)),
            (build_right_cap(name, open_theta, p), build_right_cap(name, theta, p)),
        )
        for opened, source_pose in translating_pairs:
            assert _symmetric_difference_volume(translation * opened, source_pose) <= 1.0e-7
