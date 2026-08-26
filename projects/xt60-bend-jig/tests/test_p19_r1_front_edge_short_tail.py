from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

import xt60_bend_jig.p19_r1_front_edge_short_tail as p19


ROOT = Path(__file__).parents[1]


def _labels(shape):
    if not shape.children:
        return [shape.label]
    return [label for child in shape.children for label in _labels(child)]


def test_frozen_cycle4_contract_and_exact_candidate() -> None:
    contract = ROOT / p19.P19_R1_DESIGN_CONTRACT_PATH
    assert sha256(contract.read_bytes()).hexdigest() == p19.P19_R1_DESIGN_CONTRACT_SHA256
    p = p19.P19_R1_DEFAULTS
    assert p.theta_end_deg == pytest.approx(5.0)
    assert (
        p.inner_plate_diameter,
        p.left_outer_secondary_grip_diameter,
        p.right_outer_primary_grip_diameter,
    ) == pytest.approx((54.4, 54.7, 55.0))
    assert p19.outer_rotation_center_yz(p).as_tuple() == pytest.approx((0.0, 0.0))
    assert p19.fixed_axle_center_yz(p).as_tuple() == pytest.approx((-13.0, -9.0))
    assert p.rod_diameter == pytest.approx(4.0)
    assert p.rod_length_target == pytest.approx(50.0)
    assert p.slot_endpoint_margin == pytest.approx(0.0)
    expected = {
        "bottom": ((5.0, 10.0), (9.552212035894, 8.022322349948)),
        "diagonal": ((20.4, 10.0), (15.802212035894, 2.272322349948)),
        "upright": ((20.4, -9.172814225900), (22.052212035894, -3.477677650052)),
    }
    for name, (open_point, end_point) in expected.items():
        assert p19.GUIDES[name].open.as_tuple() == pytest.approx(open_point)
        assert p19.GUIDES[name].end.as_tuple() == pytest.approx(end_point)


def test_motion_state_is_pure_deterministic_and_shared_by_both_sides() -> None:
    for u in (0.0, 0.05847953216371727, 0.5, 1.0):
        first = p19.motion_state(u)
        second = p19.motion_state(u)
        assert first == second
        assert first.theta_deg == pytest.approx(5.0 * u)
        assert first.alpha_left_deg == pytest.approx(-first.theta_deg)
        assert first.alpha_right_deg == pytest.approx(first.theta_deg)
        for name in p19.ROD_NAMES:
            assert first.rod(name).as_tuple() == pytest.approx(
                p19.rod_center(name, first.theta_deg).as_tuple(), abs=1.0e-12
            )
    with pytest.raises(ValueError):
        p19.motion_state(-1.0e-6)
    with pytest.raises(ValueError):
        p19.motion_state(1.000001)


def test_inverse_rails_reconstruct_exact_shared_world_motion() -> None:
    p = p19.P19_R1_DEFAULTS
    for side in ("left", "right"):
        for name in p19.ROD_NAMES:
            for index in range(65):
                theta = p.theta_end_deg * index / 64.0
                expected = p19.motion_state(index / 64.0, p).rod(name)
                reconstructed = p19.reconstruct_world_from_outer(side, name, theta, p)
                assert reconstructed.as_tuple() == pytest.approx(
                    expected.as_tuple(), abs=1.0e-11
                )
        for index in range(65):
            theta = p.theta_end_deg * index / 64.0
            assert p19.reconstruct_fixed_axle_from_outer(side, theta, p).as_tuple() == pytest.approx(
                (-13.0, -9.0), abs=1.0e-11
            )


def test_exact_outer_rail_lengths_and_four_mm_active_constraints() -> None:
    expected = {
        ("left", "upright"): 7.8641588369338695,
        ("left", "bottom"): 3.9999999999996283,
        ("left", "diagonal"): 8.012433561030779,
        ("right", "upright"): 4.000000000000192,
        ("right", "bottom"): 5.944910143797074,
        ("right", "diagonal"): 10.157688045825534,
    }
    actual = {
        key: p19.outer_rail_center_travel(*key)
        for key in expected
    }
    assert actual == pytest.approx(expected, abs=1.0e-10)
    assert min(actual.values()) + 1.0e-9 >= p19.P19_RAIL_CENTER_TRAVEL_MIN_MM
    assert actual[("left", "bottom")] == pytest.approx(4.0, abs=1.0e-9)
    assert actual[("right", "upright")] == pytest.approx(4.0, abs=1.0e-9)


def test_open_end_topology_interface_and_conditioning() -> None:
    triangle = p19.triangle_motion_evidence()
    assert triangle["triangles"]["open"]["areaMm2"] > 100.0
    assert triangle["openRightVerticalLegDeltaY"] == pytest.approx(0.0)
    assert triangle["triangles"]["end"]["areaMm2"] == pytest.approx(0.0, abs=1.0e-10)
    assert triangle["maximumAcceptedEndDisplacementMm"] == pytest.approx(0.0)
    assert p19.interface_alignment_evidence()["passes"]
    condition = p19.conditioning_evidence()
    assert condition["minimumRank"] == 3
    assert condition["maximumConditionNumber"] == pytest.approx(13.007686517253434)
    assert condition["maximumConditionNumber"] <= p19.P19_CONDITION_MAX


def test_actual_brep_motion_web_service_support_and_cap_gates() -> None:
    rail = p19.inverse_rail_reconstruction_evidence()
    assert rail["passes"]
    assert rail["maximumRailReconstructionResidualMm"] < 1.0e-10
    assert rail["minimumWebMm"] == pytest.approx(2.405845086139318)
    assert all(rail["platesAreSingleValidSolids"].values())

    motion = p19.actual_solid_motion_evidence()
    assert motion["passes"]
    assert motion["sampleCount"] == 65
    assert motion["maximumUnintendedIntersectionMm3"] <= 1.0e-7
    assert motion["maximumPrecontactWireIntersectionMm3"] <= 1.0e-7
    assert motion["minimumXt60ClearanceMm"] >= 3.0

    service = p19.short_tail_service_evidence()
    assert service["passes"]
    assert service["toolOccurrenceCount"] == 2
    assert service["toolKeepoutOutsideLargestRimMm"] == pytest.approx(0.75)
    assert service["maximumProductionToolIntersectionMm3"] <= 1.0e-7

    support = p19.two_sided_support_evidence()
    assert support["passes"]
    assert support["allNormalSidesSupported"]
    assert support["allSlotEndsClosed"]
    assert support["allOuterSupportStripsContinuous"]

    fixed = p19.fixed_axle_actual_solid_evidence()
    assert fixed["minimumAnalyticWebMm"] >= 2.20
    assert fixed["allFrozenFeatureCuttersClear"]
    for key in (
        "allAxleOuterPlateIntersectionsZero",
        "allKeeperOuterPlateIntersectionsZero",
        "allAxleWhiteRodIntersectionsZero",
        "allKeeperCapIntersectionsZero",
        "allXt60AndServiceIntersectionsZero",
        "centerAtCHasNoDecorativeHole",
    ):
        assert fixed[key]
    assert p19.cap_stack_closure_evidence()["passes"]


def test_pairwise_completed_pigtail_removal_and_blocked_validator_regression() -> None:
    service = p19.central_span_service_evidence()
    assert service["waypoints"] == (
        (0.0, 0.0, 0.0),
        (-8.0, 10.0, -5.0),
        (-16.0, 26.0, -10.0),
        (-16.0, 50.0, -10.0),
    )
    assert service["brepSampleCount"] == 123
    assert service["analyticSampleCount"] == 3003
    assert service["minimumClearanceMm"] == pytest.approx(0.75, abs=1.0e-9)
    assert service["brepMaximumIntersectionMm3"] == pytest.approx(0.0)
    assert service["analyticLimitingPair"]["pigtailFeature"] == "bentWire0"
    assert service["analyticLimitingPair"]["productionSolid"] == "diagonalRod"
    assert service["zeroIntersection"]
    assert service["passes"]

    regression = p19.legacy_validator_collision_regression_evidence()
    assert regression["regressionDetected"]
    assert regression["maximumIntersectionMm3"] == pytest.approx(
        47.2594024, abs=2.0e-7
    )
    for row in regression["rows"].values():
        assert row["distanceMm"] == pytest.approx(0.0)
        assert row["intersectionMm3"] == pytest.approx(47.2594024, abs=2.0e-7)


def test_production_roles_sidecar_and_entrypoints() -> None:
    labels = _labels(p19.build_motion_state("open"))
    assert len([label for label in labels if "OD4_rod_L50.00" in label]) == 3
    assert len([label for label in labels if "permanent_follower_cap" in label]) == 6
    production = " ".join(
        label.lower() for label in labels if not label.startswith("reference_")
    )
    for forbidden in (
        "grip_block", "stability_bar", "yoke", "linkage", "gear", "lock_nose", "receiver"
    ):
        assert forbidden not in production

    cad = ROOT / "cad/p19_r1_front_edge_short_tail"
    for stem in ("open", "contact", "end", "exploded", "print_kit", "full_motion"):
        assert (cad / f"p19_r1_{stem}.step.py").exists()
    sidecar = (cad / "p19_r1_full_motion.params.js").read_text()
    assert "function motionState(value)" in sidecar
    assert "const THETA_END_DEG = 5.0" in sidecar
    assert "smoothstep" not in sidecar.lower()
    for fixed in (
        "fixed_stepped_center_axle", "fixed_left_keeper", "fixed_right_keeper",
        "fixed_left_inner", "fixed_right_inner", "fixed_xt60_reference",
        "fixed_workpiece_reference",
    ):
        assert f'effects.transform("{fixed}"' not in sidecar
