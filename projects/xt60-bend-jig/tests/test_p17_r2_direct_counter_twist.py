from __future__ import annotations

import ast
import gc
from hashlib import sha256
from math import isclose, radians, sqrt
from pathlib import Path

import pytest

import xt60_bend_jig.p17_r2_direct_counter_twist as p17


ROOT = Path(__file__).parents[1]


@pytest.fixture(autouse=True)
def _clear_occ_memory_after_test():
    yield
    p17.clear_geometry_caches()
    gc.collect()


def _labels(shape):
    if not shape.children:
        return [shape.label]
    return [label for child in shape.children for label in _labels(child)]


def _finite_difference_jacobian(side: str, travel: float, pose, step=1.0e-6):
    base = p17.outer_pose_constraint_residuals(side, travel, pose)
    columns = []
    for column in range(3):
        perturbed = list(pose)
        perturbed[column] += step
        values = p17.outer_pose_constraint_residuals(side, travel, tuple(perturbed))
        columns.append(tuple((values[row] - base[row]) / step for row in range(4)))
    return tuple(tuple(columns[column][row] for column in range(3)) for row in range(4))


def test_frozen_contract_hash_and_selected_named_parameters() -> None:
    contract = ROOT / p17.P17_R2_DESIGN_CONTRACT_PATH
    assert sha256(contract.read_bytes()).hexdigest() == p17.P17_R2_DESIGN_CONTRACT_SHA256
    p = p17.P17_R2_DEFAULTS
    assert p.inner_clear_span == pytest.approx(18.40)
    assert p.principal_stack_width == pytest.approx(32.00)
    assert p.rod_length_target == pytest.approx(50.00)
    assert p.cap_rod_engagement == pytest.approx(8.70)
    assert p.follower_head_length == pytest.approx(9.05)
    assert p.fixed_slot_width == p.outer_slot_width == pytest.approx(4.15)
    assert p.inner_plate_diameter == pytest.approx(80.0)
    assert p.left_outer_secondary_grip_diameter == pytest.approx(82.0)
    assert p.right_outer_primary_grip_diameter == pytest.approx(85.0)
    assert p.theta_lock_deg == pytest.approx(24.0)
    assert p17.outer_rotation_center_yz(p).as_tuple() == pytest.approx((3.00, 12.00))
    assert p17.fixed_axle_center_yz(p).as_tuple() == pytest.approx((-29.0, 17.0))


def test_all_three_exact_open_contact_end_triangles_and_linear_law() -> None:
    evidence = p17.triangle_motion_math_evidence()
    expected = {
        "open": {
            "bottom": (-4.2502813742, 24.435),
            "diagonal": (22.235, 24.435),
            "upright": (22.235, -2.0502813742),
            "area": 350.7350647343,
            "sides": (26.4852813742, 26.4852813742, 37.4558441227),
        },
        "contact": {
            "bottom": (6.085, 24.435),
            "diagonal": (14.9268524548, 17.1268524548),
            "upright": (22.235, 8.285),
            "area": 12.3846671450,
            "sides": (11.4711540559, 11.4711540559, 22.8395490323),
        },
        "end": {
            "bottom": (6.335, 24.435),
            "diagonal": (14.7500757595, 16.9500757595),
            "upright": (22.235, 8.535),
            "area": 7.39470457605,
            "sides": (11.2622196269, 11.2622196269, 22.4859956417),
        },
    }
    for state, values in expected.items():
        row = evidence["triangles"][state]
        for name in p17.ROD_NAMES:
            assert row["centersYZ"][name] == pytest.approx(values[name], abs=2.0e-10)
        assert row["areaMm2"] == pytest.approx(values["area"], abs=1.0e-8)
        assert row["sideLengthsMm"] == pytest.approx(values["sides"], abs=1.0e-8)
    assert evidence["thetaContactDeg"] == pytest.approx(23.4331751998)
    assert evidence["thetaEndDeg"] == pytest.approx(24.0)
    assert evidence["linearTravelLaw"] == "u=theta/theta_end"
    assert evidence["endpointDerivativeMmPerDeg"] > 0.0
    assert evidence["vertexOrder"] == ("bottom", "diagonal", "upright")
    assert evidence["openRightVerticalLegDeltaY"] == pytest.approx(0.0)
    assert evidence["maximumAcceptedEndDisplacementMm"] == pytest.approx(
        0.657823586728, abs=1.0e-12
    )
    assert evidence["maximumAcceptedEndDisplacementMm"] <= 0.657824
    assert evidence["requirementIds"] == ("REQ-028", "REQ-029", "REQ-030")
    for name in p17.ROD_NAMES:
        midpoint = p17.rod_center(name, 12.0)
        guide = p17.GUIDES[name]
        assert midpoint.as_tuple() == pytest.approx(
            ((guide.open.y + guide.locked.y) / 2.0, (guide.open.z + guide.locked.z) / 2.0)
        )


def test_contact_and_end_offsets_are_tangency_then_named_preload_proxy() -> None:
    evidence = p17.triangle_motion_math_evidence()
    for value in evidence["triangles"]["contact"]["wireFeatureOffsetsMm"].values():
        assert value == pytest.approx(4.15, abs=2.0e-9)
    for value in evidence["triangles"]["end"]["wireFeatureOffsetsMm"].values():
        assert value == pytest.approx(3.90, abs=2.0e-9)
    assert "physical" in evidence["physicalBoundary"]


def test_d10_front_view_workpiece_is_head_up_tail_right_corner() -> None:
    evidence = p17.workpiece_orientation_evidence()
    assert evidence["frontPlane"] == "world YZ"
    assert evidence["screenRightAxis"] == "+Y"
    assert evidence["screenUpAxis"] == "+Z"
    assert evidence["frontViewForm"] == "└"
    assert evidence["bendCenterYZ"] == pytest.approx((16.235, 18.435))
    assert evidence["verticalLeg"] == {
        "yMm": pytest.approx(10.235),
        "fromZMm": pytest.approx(18.435),
        "toZMm": pytest.approx(37.435),
        "headDirection": "+Z",
    }
    assert evidence["horizontalTail"] == {
        "zMm": pytest.approx(12.435),
        "fromYMm": pytest.approx(16.235),
        "toYMm": pytest.approx(28.235),
        "tailDirection": "+Y",
    }
    assert evidence["rodFeatureByIdentity"] == {
        "bottom": "upper-left vertical-leg former",
        "diagonal": "upper-right/middle bend-arc former",
        "upright": "lower-right horizontal-tail former",
    }
    assert evidence["requirementIds"] == ("REQ-027",)


def test_six_inverse_outer_rails_reconstruct_and_retain_web() -> None:
    evidence = p17.inverse_rail_reconstruction_evidence()
    assert evidence["sampleCount"] == 65
    assert evidence["rodRailCount"] == 6
    assert evidence["fixedAxleRailCount"] == 2
    assert evidence["includesExactContact"] is True
    assert evidence["maximumRailReconstructionResidualMm"] <= 0.05
    assert evidence["maximumAxleReconstructionResidualMm"] <= 0.05
    assert evidence["minimumCrossingSine"] == pytest.approx(0.000718717, abs=1.0e-8)
    assert evidence["minimumOuterRodCutterGapMm"]["left"] == pytest.approx(3.630990, abs=2.0e-3)
    assert evidence["minimumOuterRodCutterGapMm"]["right"] == pytest.approx(5.884374, abs=2.0e-3)
    assert evidence["minimumFixedExtendedRodCutterGapMm"] == pytest.approx(6.103048, abs=2.0e-3)
    assert evidence["minimumWebMm"] >= evidence["minimumRequiredWebMm"]
    assert all(evidence["platesAreSingleValidSolids"].values())
    regularity = evidence["regularity"]
    assert regularity["minimumAnalyticRailDerivativeMmPerDeg"] > 0.0
    assert regularity["fixedTrackProgressMmPerDeg"] == pytest.approx(0.441053390592)
    assert regularity["fixedTrackProgressStrictlyMonotonic"] is True
    assert regularity["allRailsOneToOneNoSelfIntersection"] is True
    assert regularity["continuationHasNoBranchJump"] is True
    assert regularity["maximumContinuationResidualMm"] <= 0.05
    assert regularity["passes"] is True
    assert evidence["passes"] is True


def test_fixed_inner_tracks_are_direct_closed_capsules_with_endpoint_margin() -> None:
    p = p17.P17_R2_DEFAULTS
    for name in p17.ROD_NAMES:
        first, second = p17.fixed_guide_locus(name, p)
        guide = p17.GUIDES[name]
        assert first.distance_to(guide.open) == pytest.approx(p.slot_endpoint_margin)
        assert second.distance_to(guide.locked) == pytest.approx(p.slot_endpoint_margin)
    evidence = p17.two_sided_support_evidence()
    assert evidence["sampleCount"] == 65
    assert evidence["plateCount"] == 4
    assert evidence["rodCount"] == 3
    assert evidence["allNormalSidesSupported"] is True
    assert evidence["allSlotEndsClosed"] is True
    assert evidence["includesExactContact"] is True
    assert evidence["outerSupportStripDepthMm"] == pytest.approx(0.30)
    assert evidence["outerSupportStripSampleCountPerSide"] == 61
    assert evidence["allOuterEndpointProbesFull"] is True
    assert evidence["allOuterSupportStripsContinuous"] is True
    assert evidence["maximumEstimatedSweptBoundaryRecessionMm"] < 0.30
    for pair in evidence["outerSupportStripRows"].values():
        for row in pair:
            assert row["continuousFromSweptBoundaryThroughPlus0p30"] is True
    assert evidence["passes"] is True


def test_public_constraint_residuals_and_jacobian_are_finite_difference_reproducible() -> None:
    p = p17.P17_R2_DEFAULTS
    for side, sign in (("left", -1.0), ("right", 1.0)):
        for travel in (0.0, p17.theta_contact_deg(p) / p.theta_lock_deg, 1.0):
            pose = (0.0, 0.0, sign * radians(p.theta_lock_deg * travel))
            residuals = p17.outer_pose_constraint_residuals(side, travel, pose)
            assert len(residuals) == 4
            assert sqrt(sum(value * value for value in residuals)) <= 1.0e-6
            published = p17.outer_pose_constraint_jacobian(side, travel, pose)
            independently_fd = _finite_difference_jacobian(side, travel, pose)
            for first, second in zip(published, independently_fd):
                assert first == pytest.approx(second, abs=1.0e-8)


def test_normalized_conditioning_has_no_rank_loss_or_endpoint_dwell() -> None:
    evidence = p17.conditioning_evidence()
    assert evidence["sampleCountPerSide"] == 65
    assert evidence["includesExactContactPerSide"] is True
    assert evidence["residualRowOrder"] == ("fixed_axle", "upright", "bottom", "diagonal")
    assert evidence["poseCoordinateOrder"] == ("delta_y_mm", "delta_z_mm", "alpha_rad")
    assert evidence["minimumRank"] == 3
    assert evidence["minimumSigmaMinOverSigmaMax"] >= 1.0e-3
    assert evidence["maximumConditionNumber"] <= 1000.0
    assert evidence["passes"] is True
    for row in evidence["rows"].values():
        assert len(row["residualVectorMm"]) == 4
        assert len(row["rawJacobian"]) == 4
        assert len(row["rawSingularValues"]) == 3
        assert len(row["normalizedSingularValues"]) == 3
        assert row["rank"] == 3


def test_actual_solids_pass_65_state_motion_collision_and_wire_allowlist() -> None:
    evidence = p17.actual_solid_motion_evidence()
    assert evidence["sampleCount"] == 65
    assert evidence["includesExactContact"] is True
    assert evidence["minimumXt60ClearanceMm"] == pytest.approx(0.75, abs=1.0e-9)
    assert evidence["maximumUnintendedIntersectionMm3"] <= 1.0e-7
    assert evidence["maximumPrecontactWireIntersectionMm3"] <= 1.0e-7
    assert evidence["minimumExactContactWireClearanceMm"] <= 1.0e-6
    assert all(value > 0.0 for value in evidence["endWireIntersectionMm3ByRod"].values())
    assert evidence["allPlateGuidesClear"] is True
    assert evidence["allFixedHardwareClear"] is True
    assert evidence["passes"] is True


def test_axial_stack_uses_50mm_rods_and_six_stepped_permanent_caps() -> None:
    evidence = p17.cap_stack_closure_evidence()
    assert evidence["rodLengthMm"] == pytest.approx(50.0)
    assert evidence["principalStackWidthMm"] == pytest.approx(32.0)
    assert evidence["derivedEngagementMmPerSide"] == pytest.approx(8.70)
    assert evidence["capLengthMm"] >= 9.05
    assert evidence["closedEndWallMm"] >= 0.35
    assert evidence["proximalGuide"] == {"idMm": 4.15, "depthMm": 4.70}
    assert evidence["distalRetention"]["idMm"] == pytest.approx(4.04)
    assert evidence["distalRetention"]["depthMm"] == pytest.approx(4.00)
    assert evidence["distalRetention"]["physicalCouponRequired"] is True
    assert evidence["capCount"] == 6
    assert evidence["maximumCapPlateOrKeeperIntersectionMm3"] <= 1.0e-7
    assert evidence["passes"] is True
    coupon_caps = [
        child
        for child in p17.build_permanent_cap_coupon().children
        if child.label.startswith("coupon_permanent_cap_ID")
    ]
    assert len(coupon_caps) == 15
    assert len({round(float(child.volume), 6) for child in coupon_caps}) == 15


def test_wobble_budget_and_right_force_plate_are_quantified() -> None:
    p = p17.P17_R2_DEFAULTS
    evidence = p17.triangle_motion_math_evidence(p)
    assert evidence["nominalDiametralGuidePlayMm"] == pytest.approx(0.15)
    assert evidence["nominalAngularWobbleDeg"] <= 0.40
    assert p.right_primary_extra_lever_radius == pytest.approx(1.50)


def test_exact_production_counts_and_no_added_structure_or_green_grip() -> None:
    assembly = p17.build_motion_state("locked")
    labels = _labels(assembly)
    assert len([label for label in labels if "OD4_rod_L50.00" in label]) == 3
    assert len([label for label in labels if "permanent_follower_cap" in label]) == 6
    assert len([label for label in labels if "inner_fixed_guide" in label]) == 2
    assert len([label for label in labels if "outer_" in label and "guide" in label]) == 2
    assert len([label for label in labels if "press_fit_outer_keeper" in label]) == 2
    production = " ".join(label.lower() for label in labels if not label.startswith("reference_"))
    for forbidden in ("grip_block", "stability_bar", "yoke", "linkage", "gear", "lock_nose", "receiver"):
        assert forbidden not in production
    assert "completed_pigtail_window" not in production


def test_source_has_no_obsolete_window_grip_or_geometric_smoothstep() -> None:
    source = Path(p17.__file__).read_text()
    tree = ast.parse(source)
    function_names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert "_completed_pigtail_window_cutter_local" not in function_names
    assert "smoothstep" not in source.lower()
    assert "left_outer_secondary_grip_block" not in source
    assert "Pos(0.0, -28.0, 0.0)" not in source


def test_motion_sidecars_use_correct_linear_all_rod_motion_and_stationary_inner_geometry() -> None:
    cad = ROOT / "cad" / "p17_r2_direct_counter_twist"
    for stem in ("p17_r2_fixed_axle_motion", "p17_r2_full_motion"):
        entry = cad / f"{stem}.step.py"
        sidecar = cad / f"{stem}.params.js"
        assert f'"params": "{stem}.params.js"' in entry.read_text()
        js = sidecar.read_text()
        assert "open_to_end" in js
        assert "24.0 * travel" in js
        assert "smoothstep" not in js.lower()
        assert "[0.0, 3.0, 12.0]" in js
        for name in p17.ROD_NAMES:
            assert f"`${{name}}_rod`" in js
            assert f"left_${{name}}_cap" in js
            assert f"right_${{name}}_cap" in js
        for fixed in (
            "stepped_center_axle",
            "left_inner_fixed_guide",
            "right_inner_fixed_guide",
            "left_keeper",
            "right_keeper",
        ):
            assert f'effects.transform("{fixed}"' not in js


def test_explicit_open_contact_end_and_review_artifact_entrypoints_exist() -> None:
    cad = ROOT / "cad" / "p17_r2_direct_counter_twist"
    expected = (
        "p17_r2_open",
        "p17_r2_mid",
        "p17_r2_contact",
        "p17_r2_locked",
        "p17_r2_exploded",
        "p17_r2_print_kit",
        "p17_r2_permanent_cap_coupon",
        "p17_r2_center_axle_coupon",
        "p17_r2_fixed_axle_motion",
        "p17_r2_full_motion",
    )
    for stem in expected:
        assert (cad / f"{stem}.step.py").exists()


def test_manifest_states_physical_boundary_and_same_version_scope() -> None:
    manifest = p17.p17_r2_manifest()
    assert manifest["contractPath"] == p17.P17_R2_DESIGN_CONTRACT_PATH
    assert manifest["whiteRods"]["count"] == 3
    assert manifest["whiteRods"]["modeledTargetLengthMm"] == pytest.approx(50.0)
    assert manifest["whiteRods"]["physicalStockLengthMm"] == pytest.approx(50.0)
    assert manifest["whiteRods"]["stockUseDecision"].endswith("used uncut")
    assert manifest["caps"]["count"] == 6
    assert manifest["endpoint"]["meaning"] == "end-of-travel only"
    assert manifest["endpoint"]["selfLockClaimed"] is False
    assert manifest["service"]["obsoleteInnerWindowRemoved"] is True
    assert set(manifest["requirementTraceability"]) == {
        "REQ-027",
        "REQ-028",
        "REQ-029",
        "REQ-030",
    }


def test_d10_r1_full_component_rigid_body_service_path_is_clear() -> None:
    evidence = p17.central_span_service_evidence()
    assert evidence["innerClearSpanMm"] == pytest.approx(18.40)
    assert evidence["xt60BodyWidthMm"] == pytest.approx(15.90)
    assert evidence["sideClearanceMmEach"] == pytest.approx(1.25)
    assert evidence["pathId"] == "P17-D10-R1"
    assert evidence["waypoints"] == (
        (0.0, 0.0, 0.0),
        (-4.0, 10.0, -15.0),
        (-4.0, 50.0, -15.0),
    )
    assert evidence["brepSamplesPerSegment"] == 1001
    assert evidence["analyticSamplesPerSegment"] == 1001
    assert evidence["brepSampleCount"] >= 2 * 1001
    assert evidence["analyticSampleCount"] >= 2 * 1001
    assert set(evidence["includedPigtailFeatures"]) == {
        "XT60 body",
        "two solder joints",
        "two bent wires",
    }
    assert len(evidence["includedProductionSolids"]) == 16
    assert evidence["minimumClearanceMm"] == pytest.approx(0.933815921231)
    assert evidence["brepMinimumClearanceMm"] >= 0.75
    assert evidence["zeroIntersection"] is True
    assert evidence["passes"] is True


def test_fixed_occurrences_remain_world_invariant_and_outers_counter_rotate() -> None:
    evidence = p17.fixed_occurrence_transform_evidence()
    assert evidence["allFixedWorldInvariant"] is True
    for row in evidence["states"].values():
        assert row["leftOuterAngleDeg"] == pytest.approx(-row["rightOuterAngleDeg"])


def test_state_contact_value_is_derived_consistently() -> None:
    assert p17.STATE_THETA["contact"] == pytest.approx(p17.theta_contact_deg(), abs=3.0e-11)
    assert isclose(p17.STATE_THETA["locked"], 24.0)
