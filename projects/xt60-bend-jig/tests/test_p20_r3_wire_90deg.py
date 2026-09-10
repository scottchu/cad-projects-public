from __future__ import annotations

import inspect
from hashlib import sha256
from math import pi
from pathlib import Path

import pytest

import xt60_bend_jig.p18_r1_compact_counter_twist as p18
import xt60_bend_jig.p20_r2_fixed_rod_arc_rail as p20r2
import xt60_bend_jig.p20_r3_wire_90deg as p20r3


ROOT = Path(__file__).parents[1]


def test_p20_r2_hard_invariants_are_byte_frozen() -> None:
    expected = {
        "src/xt60_bend_jig/p20_r2_fixed_rod_arc_rail.py":
            "1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73",
        "cad/p20_r2_fixed_rod_arc_rail/p20_r2_fixed_rail_review.step":
            "07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c",
        "cad/p20_r2_fixed_rod_arc_rail/p20_r2_full_motion.step":
            "715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca",
    }
    for relative, digest in expected.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    assert p20r2.outer_rotation_center_yz().as_tuple() == (0.0, 0.0)
    assert p20r2.fixed_axle_center_yz().as_tuple() == (-15.0, -11.0)
    assert p20r2.rotation_for_side("left", 45.0) == 45.0
    assert p20r2.rotation_for_side("right", 45.0) == -45.0


def test_wire_topology_is_exact_p18_vertical_quarter_arc_horizontal() -> None:
    p18_params = p18.P18_R1_DEFAULTS
    p20_params = p20r2.P20_R2_DEFAULTS
    assert (
        p18_params.xt60_body_width_x,
        p18_params.xt60_body_y,
        p18_params.xt60_body_z,
        p18_params.xt60_body_center_y,
        p18_params.xt60_body_center_z,
    ) == (
        p20_params.xt60_body_width_x,
        p20_params.xt60_body_y,
        p20_params.xt60_body_z,
        p20_params.xt60_body_center_y,
        p20_params.xt60_body_center_z,
    )
    evidence = p20r3.wire_90deg_evidence()
    assert evidence["frontViewForm"] == "└"
    assert evidence["bendCenterYZ"] == (1.0, 1.5)
    assert evidence["bendRadiusMm"] == pytest.approx(6.0)
    assert evidence["turnAngleDeg"] == pytest.approx(90.0)
    assert evidence["turnAngleRad"] == pytest.approx(pi / 2.0)
    assert evidence["verticalLeg"] == {
        "yMm": -5.0,
        "fromZMm": 1.5,
        "toZMm": 20.5,
        "direction": "+Z toward XT60 / -Z away from XT60",
    }
    assert evidence["horizontalTail"] == {
        "zMm": -4.5,
        "fromYMm": 1.0,
        "toYMm": 13.0,
        "direction": "+Y",
    }
    assert evidence["verticalTangentYZ"] == (-5.0, 1.5)
    assert evidence["horizontalTangentYZ"] == (1.0, -4.5)
    assert evidence["tangentDot"] == pytest.approx(0.0)
    assert evidence["usesP18AcceptedBuilder"]
    assert not evidence["usesDiagonalLineParameters"]


def test_workpiece_delegates_to_p18_and_diagonal_line_parameters_are_unused() -> None:
    r3 = p20r3.build_workpiece_reference_90deg(0.0)
    accepted = p18.build_workpiece_reference(0.0, p18.P18_R1_DEFAULTS)
    assert p20r3.shape_signature(r3) == p20r3.shape_signature(accepted)
    source = inspect.getsource(p20r3)
    assert "wire_line_point" not in source
    assert "wire_line_direction" not in source
    assert "p19.build_workpiece_reference" not in source


def test_all_non_workpiece_occurrences_match_p20_r2_exactly() -> None:
    evidence = p20r3.non_workpiece_invariance_evidence()
    assert evidence["p20R2OccurrenceCount"] == evidence["p20R3OccurrenceCount"]
    assert evidence["replacedOccurrenceLabels"] == ("motion_full_fixed_workpiece_reference",)
    assert evidence["allNonWorkpieceLabelsAndGeometrySignaturesIdentical"]
    assert evidence["mismatches"] == {}
    assert evidence["workpieceChanged"]


def test_full_motion_entrypoint_and_sidecar_preserve_p20_r2_motion() -> None:
    cad = ROOT / "cad/p20_r3_wire_90deg"
    assert (cad / "p20_r3_full_motion.step.py").exists()
    sidecar = (cad / "p20_r3_full_motion.params.js").read_text()
    assert 'step: { path: "cad/p20_r3_wire_90deg/p20_r3_full_motion.step" }' in sidecar
    assert "const THETA_END_DEG = 45.0" in sidecar
    assert "alphaLeftDeg: thetaDeg" in sidecar
    assert "alphaRightDeg: -thetaDeg" in sidecar
    assert "fixed_workpiece" not in sidecar.split("effects.transform", 1)[-1]
