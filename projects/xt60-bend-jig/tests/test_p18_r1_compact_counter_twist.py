from __future__ import annotations

import gc
from hashlib import sha256
from math import sqrt
from pathlib import Path

import pytest

import xt60_bend_jig.p18_r1_compact_counter_twist as p18


ROOT = Path(__file__).parents[1]


@pytest.fixture(autouse=True)
def _clear_geometry_caches():
    yield
    p18.clear_geometry_caches()
    gc.collect()


def _labels(shape):
    if not shape.children:
        return [shape.label]
    return [label for child in shape.children for label in _labels(child)]


def test_frozen_contract_and_compact_parameter_set() -> None:
    contract = ROOT / p18.P18_R1_DESIGN_CONTRACT_PATH
    assert sha256(contract.read_bytes()).hexdigest() == p18.P18_R1_DESIGN_CONTRACT_SHA256
    p = p18.P18_R1_DEFAULTS
    assert (p.inner_plate_diameter, p.left_outer_secondary_grip_diameter, p.right_outer_primary_grip_diameter) == pytest.approx((52.933, 53.933, 54.933))
    assert p.theta_end_deg == pytest.approx(45.0)
    assert p18.outer_rotation_center_yz(p).as_tuple() == pytest.approx((0.0, 0.0))
    assert p18.fixed_axle_center_yz(p).as_tuple() == pytest.approx((-9.5, -9.5))
    assert p.rod_length_target == pytest.approx(50.0)
    assert p.center_axle_total_length == pytest.approx(34.9)


def test_exact_accepted_workpiece_alignment_and_triangles() -> None:
    assert p18.P18_ACCEPTED_RIGID_SHIFT.as_tuple() == pytest.approx((-14.6869657526, -12.2949747468))
    assert p18.P18_WORKPIECE_ALIGNMENT_DELTA.as_tuple() == pytest.approx((1.5, -2.0))
    expected = {
        "bottom": ((-19.4852813742, 7.5), (-8.9, 7.5)),
        "diagonal": ((7.0, 7.5), (-0.4849242405, 0.0150757595)),
        "upright": ((7.0, -18.9852813742), (7.0, -8.4)),
    }
    for name, (open_point, end_point) in expected.items():
        assert p18.GUIDES[name].open.as_tuple() == pytest.approx(open_point)
        assert p18.GUIDES[name].end.as_tuple() == pytest.approx(end_point)
    orientation = p18.workpiece_orientation_evidence()
    assert orientation["xt60BodyCenterYZ"] == pytest.approx((-5.0, 20.5))
    assert orientation["bendCenterYZ"] == pytest.approx((1.0, 1.5))
    assert orientation["screenRightAxis"] == "+Y"
    assert orientation["screenUpAxis"] == "+Z"


def test_contact_state_is_derived_from_preload_and_common_travel() -> None:
    assert p18.GUIDES["upright"].travel == pytest.approx(10.5852813742)
    assert p18.theta_contact_deg() == pytest.approx(43.9372034996235)
    assert p18.STATE_THETA == pytest.approx({"open": 0.0, "mid": 22.5, "contact": 43.9372034996235, "end": 45.0})


def test_all_inverse_rails_reconstruct_the_same_world_points() -> None:
    p = p18.P18_R1_DEFAULTS
    for side in ("left", "right"):
        for name in p18.ROD_NAMES:
            for index in range(65):
                theta = p.theta_end_deg * index / 64.0
                actual = p18.reconstruct_world_from_outer(side, name, theta, p)
                expected = p18.rod_center(name, theta, p)
                assert actual.as_tuple() == pytest.approx(expected.as_tuple(), abs=1.0e-11)
        for index in range(65):
            theta = p.theta_end_deg * index / 64.0
            actual = p18.reconstruct_fixed_axle_from_outer(side, theta, p)
            assert actual.as_tuple() == pytest.approx((-9.5, -9.5), abs=1.0e-11)


def test_exact_regular_hex_and_axial_stack_are_modeled() -> None:
    p = p18.P18_R1_DEFAULTS
    assert p.inner_hex_bore_circumradius == pytest.approx(8.15 / sqrt(3.0))
    assert p.inner_hex_bore_circumradius > p.inner_hex_bore_af / 2.0
    axle = p18.build_center_axle(p)
    assert axle.is_valid
    bounds = axle.bounding_box()
    assert bounds.max.X - bounds.min.X == pytest.approx(34.9)
    assert p.outer_journal_diameter < p.inner_hex_bore_af


def test_compact_plates_are_valid_and_actual_rail_web_gate_passes() -> None:
    for side in ("left", "right"):
        assert p18.build_inner_plate(side).is_valid
        assert p18.build_outer_plate(side, 0.0).is_valid
        assert p18.build_outer_plate(side, 45.0).is_valid
    evidence = p18.inverse_rail_reconstruction_evidence()
    assert evidence["maximumRailReconstructionResidualMm"] < 1.0e-10
    assert evidence["maximumAxleReconstructionResidualMm"] < 1.0e-10
    assert evidence["minimumWebMm"] >= 2.20
    assert all(evidence["platesAreSingleValidSolids"].values())


def test_four_contact_constraint_has_rank_three_with_recorded_risk() -> None:
    evidence = p18.conditioning_evidence()
    assert evidence["minimumRank"] == 3
    assert evidence["maximumConditionNumber"] == pytest.approx(3.7502959057792857)
    rail = p18.inverse_rail_reconstruction_evidence()
    assert rail["minimumCrossingSine"] < 0.001


def test_exact_production_roles_and_absent_extra_structure() -> None:
    labels = _labels(p18.build_motion_state("end"))
    assert len([label for label in labels if "OD4_rod_L50.00" in label]) == 3
    assert len([label for label in labels if "permanent_follower_cap" in label]) == 6
    assert len([label for label in labels if "inner_fixed_guide" in label]) == 2
    assert len([label for label in labels if "outer_" in label and "guide" in label]) == 2
    production = " ".join(label.lower() for label in labels if not label.startswith("reference_"))
    for forbidden in ("grip_block", "stability_bar", "yoke", "linkage", "gear", "lock_nose", "receiver"):
        assert forbidden not in production


def test_motion_sidecar_moves_only_outer_plates_rods_and_caps() -> None:
    sidecar = ROOT / "cad/p18_r1_compact_counter_twist/p18_r1_full_motion.params.js"
    text = sidecar.read_text()
    assert "45.0 * travel" in text
    assert "[0.0, 0.0, 0.0]" in text
    assert "smoothstep" not in text.lower()
    for fixed in ("stepped_center_axle", "left_inner", "right_inner", "left_keeper", "right_keeper", "xt60", "workpiece"):
        assert f'effects.transform("{fixed}"' not in text


def test_required_p18_entrypoints_exist() -> None:
    cad = ROOT / "cad/p18_r1_compact_counter_twist"
    for stem in ("open", "contact", "end", "exploded", "print_kit", "full_motion"):
        assert (cad / f"p18_r1_{stem}.step.py").exists()
    assert (cad / "p18_r1_full_motion.params.js").exists()
