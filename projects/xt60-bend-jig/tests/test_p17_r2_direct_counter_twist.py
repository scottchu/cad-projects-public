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
    assert (p.working_set_translation_y, p.working_set_translation_z) == pytest.approx(
        (-12.350, -10.550)
    )
    assert p17.outer_rotation_center_yz(p).as_tuple() == pytest.approx((3.00, 12.00))
    assert p17.fixed_axle_center_yz(p).as_tuple() == pytest.approx((30.0, 12.0))


def test_all_three_exact_open_contact_end_triangles_and_linear_law() -> None:
    evidence = p17.triangle_motion_math_evidence()
    expected = {
        "open": {
            "bottom": (-16.6002813742, 13.885),
            "diagonal": (9.885, 13.885),
            "upright": (9.885, -12.6002813742),
            "area": 350.7350647343,
            "sides": (26.4852813742, 26.4852813742, 37.4558441227),
        },
        "contact": {
            "bottom": (-6.265, 13.885),
            "diagonal": (2.5768524548, 6.5768524548),
            "upright": (9.885, -2.265),
            "area": 12.3846671450,
            "sides": (11.4711540559, 11.4711540559, 22.8395490323),
        },
        "end": {
            "bottom": (-6.015, 13.885),
            "diagonal": (2.4000757595, 6.4000757595),
            "upright": (9.885, -2.015),
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
    assert evidence["xt60BodyCenterYZ"] == pytest.approx((-2.115, 26.885))
    assert evidence["bendCenterYZ"] == pytest.approx((3.885, 7.885))
    assert evidence["verticalLeg"] == {
        "yMm": pytest.approx(-2.115),
        "fromZMm": pytest.approx(7.885),
        "toZMm": pytest.approx(26.885),
        "headDirection": "+Z",
    }
    assert evidence["horizontalTail"] == {
        "zMm": pytest.approx(1.885),
        "fromYMm": pytest.approx(3.885),
        "toYMm": pytest.approx(15.885),
        "tailDirection": "+Y",
    }
    assert evidence["rodFeatureByIdentity"] == {
        "bottom": "upper-left vertical-leg former",
        "diagonal": "upper-right/middle bend-arc former",
        "upright": "lower-right horizontal-tail former",
    }
    assert evidence["requirementIds"] == ("REQ-027",)


def test_d12_translation_is_rigid_once_and_fixed_datums_do_not_move() -> None:
    evidence = p17.d12_working_set_translation_evidence()
    assert evidence["workingSetTranslationYZ"] == pytest.approx((-12.350, -10.550))
    assert evidence["rejectedI10WorkingSetTranslationYZ"] == pytest.approx((-16.735, -14.935))
    assert evidence["deltaFromRejectedI10YZ"] == pytest.approx((4.385, 4.385))
    assert evidence["openWorkingSetBoxMidpointRelativeToCYZ"] == pytest.approx(
        (-6.3576406871, -11.3576406871)
    )
    assert evidence["rejectedI10OpenWorkingSetBoxMidpointRelativeToCYZ"] == pytest.approx(
        (-10.7426406871, -15.7426406871)
    )
    assert evidence["screenRightAndUpPlacementRegressionPasses"] is True
    assert evidence["physicalOuterRotationCenterYZ"] == pytest.approx((3.0, 12.0))
    assert evidence["railShapingRelativeDatumYZ"] == pytest.approx((15.350, 22.550))
    assert evidence["fixedAxleCenterYZ"] == pytest.approx((30.0, 12.0))
    assert evidence["translationAppliedExactlyOnce"] is True
    assert evidence["maximumRigidTranslationResidualMm"] <= 1.0e-12
    assert evidence["workpiece"] == {
        "bendCenterYZ": pytest.approx((3.885, 7.885)),
        "xt60BodyCenterYZ": pytest.approx((-2.115, 26.885)),
        "verticalLegYMm": pytest.approx(-2.115),
        "horizontalLegZMm": pytest.approx(1.885),
        "completedPigtailExtractEndYMm": pytest.approx(21.650),
    }
    assert evidence["outerRailsRecomputedFromTranslatedRods"] is True
    assert evidence["oldRailSolidsReusedOrTranslated"] is False
    assert evidence["minimumContactOrEndResidualFromNaivelyTranslatedOldRailMm"] > 6.5
    assert evidence["fixedAxleRailsUnchanged"] is True
    assert evidence["fixedAxleRailEndpoints"] == {
        "left": {
            "open": pytest.approx((27.0, 0.0)),
            "end": pytest.approx((24.665727356, 10.981889363)),
        },
        "right": {
            "open": pytest.approx((27.0, 0.0)),
            "end": pytest.approx((24.665727356, -10.981889363)),
        },
    }
    for name in p17.ROD_NAMES:
        row = evidence["guides"][name]
        assert row["functionalLengthMm"] == pytest.approx(10.5852813742)
        pre = row["preD12"]
        translated = row["translated"]
        for state in ("open", "contact", "end"):
            assert translated[state][0] - pre[state][0] == pytest.approx(-12.350)
            assert translated[state][1] - pre[state][1] == pytest.approx(-10.550)


def test_d12_r4b_quick_preview_axle_and_guides_preserve_working_set_digest() -> None:
    evidence = p17.d12_r4b_fixed_axle_preview_evidence()
    assert evidence["fixedAxleCenterYZ"] == pytest.approx((30.0, 12.0))
    assert evidence["outerRotationCenterYZ"] == pytest.approx((3.0, 12.0))
    assert evidence["fixedAxleRelativeToCYZ"] == pytest.approx((27.0, 0.0))
    assert evidence["priorI11FixedAxleCenterYZ"] == pytest.approx((-29.0, 17.0))
    assert evidence["deltaFromI11YZ"] == pytest.approx((59.0, -5.0))
    assert evidence["markedBandTargetA0YZ"] == pytest.approx((17.0, 12.0))
    assert evidence["distanceFromMarkedBandTargetMm"] == pytest.approx(13.0)
    assert evidence["recommendedR4bTrueCenterRightDatumYZ"] == pytest.approx(
        (30.0, 12.0)
    )
    assert evidence["isRecommendedR4bTrueCenterRightDatum"] is True
    assert evidence["insideMarkedCenterRightBand"] is False
    assert evidence["heightAboveHorizontalWireReferenceMm"] == pytest.approx(10.115)
    assert evidence["fixedAxleGuideSlotWidthMm"] == pytest.approx(7.90)
    expected = {
        "left": {
            "open": (27.0, 0.0),
            "contact": (24.773161951, 10.737338915),
            "end": (24.665727356, 10.981889363),
        },
        "right": {
            "open": (27.0, 0.0),
            "contact": (24.773161951, -10.737338915),
            "end": (24.665727356, -10.981889363),
        },
    }
    for side, points in expected.items():
        row = evidence["guideRails"][side]
        for state, point in points.items():
            assert row[state] == pytest.approx(point, abs=1.0e-9)
        assert row["analyticArcLengthMm"] == pytest.approx(11.309733553, abs=1.0e-9)
        assert row["sampledPolylineLengthMm"] == pytest.approx(11.309652808, abs=1.0e-9)
    assert evidence["fixedWorldFrame"] is True
    assert evidence["stainlessRodRailsAndWorkingSetUnchanged"] is True
    assert evidence["rodWorkpieceSixRailDigestSha256"] == (
        "a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58"
    )


def test_d12_r4b_quick_preview_actual_solids_clear_rods_and_caps() -> None:
    evidence = p17.fixed_axle_actual_solid_evidence()
    assert evidence["minimumAnalyticWebMm"] == pytest.approx(8.294595306, abs=2.0e-9)
    assert evidence["minimumActualInnerHexWebMm"] == pytest.approx(8.294595306, abs=2.0e-9)
    assert evidence["leftOuterBoundaryWebMm"] == pytest.approx(10.05)
    assert evidence["rightOuterBoundaryWebMm"] == pytest.approx(11.55)
    assert evidence["minimumActualOuterGuideWebMmBySide"] == {
        "left": pytest.approx(12.012572604, abs=2.0e-9),
        "right": pytest.approx(14.178129708, abs=2.0e-9),
    }
    assert evidence["minimumExactFrozenFeatureGapMm"] == pytest.approx(12.012572604, abs=2.0e-9)
    assert evidence["minimumAxleGuideRadialClearanceMm"] == pytest.approx(0.15)
    assert evidence["minimumKeeperRadialCaptureMm"] == pytest.approx(1.05)
    assert evidence["fixedGuideSupportProbeCount"] == 132
    assert evidence["minimumFixedGuideSupportMaterialRatio"] >= 0.999
    assert evidence["allFixedGuideSupportProbesFull"] is True
    assert evidence["fixedGuideSupportStripDepthMm"] == pytest.approx(0.30)
    assert evidence["fixedGuideSupportStripSampleCountPerSide"] == 61
    assert evidence["allFixedGuideSupportStripsContinuous"] is True
    assert evidence["minimumXt60AndServiceClearanceMm"] == pytest.approx(2.965, abs=2.0e-9)
    assert evidence["sampleCount"] == 65
    assert evidence["minimumAxleToWhiteRodClearanceMm"] == pytest.approx(
        12.464846008, abs=2.0e-9
    )
    assert evidence["minimumKeeperToCapClearanceMm"] == pytest.approx(
        11.903129708, abs=2.0e-9
    )
    assert evidence["minimumFixedHardwareToRodOrCapClearanceMm"] >= 11.903
    for key in (
        "allFrozenFeatureCuttersClear",
        "allAxleOuterPlateIntersectionsZero",
        "allKeeperOuterPlateIntersectionsZero",
        "allAxleWhiteRodIntersectionsZero",
        "allKeeperCapIntersectionsZero",
        "allXt60AndServiceIntersectionsZero",
        "centerAtCHasNoDecorativeHole",
    ):
        assert evidence[key] is True


def test_d12_six_outer_rails_are_rederived_with_exact_endpoints_and_lengths() -> None:
    evidence = p17.outer_rail_length_and_force_evidence()
    expected = {
        "bottom": {
            "left": ((-19.600281374, 1.885), (-9.250489975, -1.954964251), (-9.002310873, -1.944697650), 11.535632996, 0.248395166),
            "right": ((-19.600281374, 1.885), (-7.751239319, 5.414031679), (-7.468913728, 5.388764025), 12.907013192, 0.283457937),
            "ratio": 1.118882093,
            "contactRatio": 1.141157219,
        },
        "diagonal": {
            "left": ((6.885, 1.885), (1.768424834, -5.144147816), (1.729636322, -5.359796525), 9.201239566, 0.219113381),
            "right": ((6.885, 1.885), (-2.544921328, -4.807593845), (-2.825752452, -4.871774181), 12.139694820, 0.288075639),
            "ratio": 1.319354282,
            "contactRatio": 1.314733212,
        },
        "upright": {
            "left": ((6.885, -24.600281374), (11.990050357, -10.350465807), (11.990174529, -10.002957801), 15.749176568, 0.347511926),
            "right": ((6.885, -24.600281374), (0.644262237, -15.826508654), (0.589346423, -15.603721376), 11.202968733, 0.229458948),
            "ratio": 1.405803849,
            "contactRatio": 1.514484088,
        },
    }
    for name, expected_row in expected.items():
        row = evidence["rows"][name]
        for side in ("left", "right"):
            side_row = row["sides"][side]
            values = expected_row[side]
            assert side_row["openLocalYZ"] == pytest.approx(values[0], abs=5.0e-10)
            assert side_row["contactLocalYZ"] == pytest.approx(values[1], abs=5.0e-10)
            assert side_row["endLocalYZ"] == pytest.approx(values[2], abs=5.0e-10)
            assert side_row["openToEndFunctionalLengthMm"] == pytest.approx(values[3], abs=5.0e-9)
            assert side_row["contactToEndFunctionalLengthMm"] == pytest.approx(values[4], abs=5.0e-9)
            assert side_row["minimumContactToEndCrossingSine"] > 0.0
        assert row["openToEndSideRatio"] == pytest.approx(expected_row["ratio"], abs=5.0e-9)
        assert row["contactToEndSideRatio"] == pytest.approx(expected_row["contactRatio"], abs=5.0e-9)
        assert row["openToEndRatioImprovedFromRejectedD12"] is True
        assert row["openToEndSideRatio"] <= 1.50
    assert evidence["baselineWorstOpenToEndSideRatio"] == pytest.approx(4.212853)
    assert evidence["rejectedD12WorstOpenToEndSideRatio"] == pytest.approx(2.012551004)
    assert evidence["d12WorstOpenToEndSideRatio"] == pytest.approx(1.405803849, abs=5.0e-9)
    assert evidence["d12WorstOpenToEndSideRatio"] <= evidence["maximumAcceptedOpenToEndSideRatio"]
    expected_force = {
        "bottom": {"left": (21.081418, 2.780139), "right": (18.364978, 3.173908), "ratio": 1.141636388},
        "diagonal": {"left": (10.768937, 5.351923), "right": (8.166759, 7.039543), "ratio": 1.315329662},
        "upright": {"left": (23.550019, 2.502819), "right": (37.317751, 1.649526), "ratio": 1.517295884},
    }
    for name, expected_row in expected_force.items():
        row = evidence["rows"][name]
        for side in ("left", "right"):
            angle, multiplier = expected_row[side]
            side_row = row["sides"][side]
            assert side_row["minimumContactToEndAcuteAngleDeg"] == pytest.approx(angle, abs=2.0e-6)
            assert side_row["maximumFrictionlessGeometricMultiplier"] == pytest.approx(multiplier, abs=2.0e-6)
            assert side_row["minimumContactToEndAcuteAngleDeg"] >= 8.0
        assert row["worstGeometricMultiplierSideRatio"] == pytest.approx(expected_row["ratio"], abs=2.0e-6)
    assert min(
        side["minimumContactToEndAcuteAngleDeg"]
        for row in evidence["rows"].values()
        for side in row["sides"].values()
    ) == pytest.approx(8.166759353, abs=2.0e-6)
    assert evidence["forceProven"] is False
    assert evidence["selfLockClaimed"] is False
    assert "physical unknowns" in evidence["physicalBoundary"]


def test_six_inverse_outer_rails_reconstruct_and_retain_web() -> None:
    evidence = p17.inverse_rail_reconstruction_evidence()
    assert evidence["sampleCount"] == 65
    assert evidence["rodRailCount"] == 6
    assert evidence["fixedAxleRailCount"] == 2
    assert evidence["includesExactContact"] is True
    assert evidence["maximumRailReconstructionResidualMm"] <= 0.05
    assert evidence["maximumAxleReconstructionResidualMm"] <= 0.05
    assert evidence["minimumCrossingSine"] == pytest.approx(0.002836570780, abs=1.0e-10)
    assert evidence["minimumOuterRodCutterGapMm"]["left"] == pytest.approx(7.059616, abs=2.0e-3)
    assert evidence["minimumOuterRodCutterGapMm"]["right"] == pytest.approx(7.085232, abs=2.0e-3)
    assert evidence["minimumFixedExtendedRodCutterGapMm"] == pytest.approx(6.103048, abs=2.0e-3)
    assert evidence["minimumWebMm"] == pytest.approx(6.103048, abs=2.0e-3)
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


def test_pure_frame_transform_round_trips_and_pairs_left_right_rails() -> None:
    p = p17.P17_R2_DEFAULTS
    world_frame = p17.PointYZ(0.0, 0.0)
    outer_frame = p17.outer_rotation_center_yz(p)
    progress = tuple(
        index / (p.validation_sample_count - 1)
        for index in range(p.validation_sample_count)
    ) + (p17.theta_contact_deg(p) / p.theta_lock_deg,)
    for name in p17.ROD_NAMES:
        fixed_inner_path = tuple(
            p17.rod_center(name, value * p.theta_lock_deg, p) for value in progress
        )
        left_path = p17.derive_mating_rail(
            fixed_inner_path,
            progress,
            source_origin=world_frame,
            source_total_rotation_deg=0.0,
            target_origin=outer_frame,
            target_total_rotation_deg=-p.theta_lock_deg,
        )
        right_path = p17.derive_mating_rail(
            fixed_inner_path,
            progress,
            source_origin=world_frame,
            source_total_rotation_deg=0.0,
            target_origin=outer_frame,
            target_total_rotation_deg=p.theta_lock_deg,
        )
        paired_right_path = p17.derive_mating_rail(
            left_path,
            progress,
            source_origin=outer_frame,
            source_total_rotation_deg=-p.theta_lock_deg,
            target_origin=outer_frame,
            target_total_rotation_deg=p.theta_lock_deg,
        )
        round_trip_inner_path = p17.derive_mating_rail(
            right_path,
            progress,
            source_origin=outer_frame,
            source_total_rotation_deg=p.theta_lock_deg,
            target_origin=world_frame,
            target_total_rotation_deg=0.0,
        )
        for index, value in enumerate(progress):
            theta = value * p.theta_lock_deg
            fixed_inner = fixed_inner_path[index]
            side_locals = {}
            for side in ("left", "right"):
                angle = p17.rotation_for_side(side, theta)
                outer = p17.transform_point_between_frames_yz(
                    fixed_inner,
                    world_frame,
                    0.0,
                    outer_frame,
                    angle,
                )
                assert outer.as_tuple() == pytest.approx(
                    p17.outer_slot_local_center(side, name, theta, p).as_tuple(),
                    abs=1.0e-12,
                )
                reconstructed_inner = p17.transform_point_between_frames_yz(
                    outer,
                    outer_frame,
                    angle,
                    world_frame,
                    0.0,
                )
                assert reconstructed_inner.as_tuple() == pytest.approx(
                    fixed_inner.as_tuple(), abs=1.0e-12
                )
                side_locals[side] = outer
            assert left_path[index].as_tuple() == pytest.approx(
                side_locals["left"].as_tuple(), abs=1.0e-12
            )
            assert right_path[index].as_tuple() == pytest.approx(
                side_locals["right"].as_tuple(), abs=1.0e-12
            )
            assert paired_right_path[index].as_tuple() == pytest.approx(
                right_path[index].as_tuple(), abs=1.0e-12
            )
            assert round_trip_inner_path[index].as_tuple() == pytest.approx(
                fixed_inner.as_tuple(), abs=1.0e-12
            )
            paired_right = p17.transform_point_between_frames_yz(
                side_locals["left"],
                outer_frame,
                p17.alpha_left(theta),
                outer_frame,
                p17.alpha_right(theta),
            )
            assert paired_right.as_tuple() == pytest.approx(
                side_locals["right"].as_tuple(), abs=1.0e-12
            )


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
    assert evidence["minimumSigmaMinOverSigmaMax"] == pytest.approx(0.101441491, abs=2.0e-9)
    assert evidence["maximumConditionNumber"] == pytest.approx(9.857899236, abs=2.0e-9)
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
        assert "open: [9.885, -12.6002813742], end: [9.885, -2.015]" in js
        assert "open: [-16.6002813742, 13.885], end: [-6.015, 13.885]" in js
        assert "open: [9.885, 13.885], end: [2.4000757595, 6.4000757595]" in js
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
    translation = manifest["d12WorkingSetTranslation"]
    assert translation["workingSetTranslationYZ"] == pytest.approx((-12.350, -10.550))
    assert translation["deltaFromRejectedI10YZ"] == pytest.approx((4.385, 4.385))
    assert translation["screenRightAndUpPlacementRegressionPasses"] is True
    assert translation["oldRailSolidsReusedOrTranslated"] is False
    axle = manifest["d12R4bFixedAxlePreview"]
    assert axle["fixedAxleCenterYZ"] == pytest.approx((30.0, 12.0))
    assert axle["fixedAxleRelativeToCYZ"] == pytest.approx((27.0, 0.0))
    assert axle["rodWorkpieceSixRailDigestSha256"] == (
        "a13a2cb0deef4c08b20bbd690b8cc74e377cd0f750810c0f86781ed1d09a1e58"
    )
    diagnostic = manifest["outerRailLengthAndForceDiagnostic"]
    assert diagnostic["forceProven"] is False
    assert diagnostic["selfLockClaimed"] is False
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
    assert evidence["sampleCount"] == 65
    assert evidence["includesExactContact"] is True
    assert len(evidence["states"]) == 66
    assert evidence["allFixedWorldInvariant"] is True
    for row in evidence["states"].values():
        assert row["leftOuterAngleDeg"] == pytest.approx(-row["rightOuterAngleDeg"])
        frames = row["fixedFramesXYZAngleDeg"]
        assert frames["stepped_center_axle"][1:3] == pytest.approx((30.0, 12.0))
        assert frames["left_keeper"][1:3] == pytest.approx((30.0, 12.0))
        assert frames["right_keeper"][1:3] == pytest.approx((30.0, 12.0))


def test_state_contact_value_is_derived_consistently() -> None:
    assert p17.STATE_THETA["contact"] == pytest.approx(p17.theta_contact_deg(), abs=3.0e-11)
    assert isclose(p17.STATE_THETA["locked"], 24.0)
