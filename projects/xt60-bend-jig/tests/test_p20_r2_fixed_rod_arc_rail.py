from __future__ import annotations

from dataclasses import asdict
from math import hypot
from pathlib import Path

import pytest

import xt60_bend_jig.p19_r1_front_edge_short_tail as p19
import xt60_bend_jig.p20_r2_fixed_rod_arc_rail as p20


ROOT = Path(__file__).parents[1]


def _labels(shape):
    if not shape.children:
        return [shape.label]
    return [label for child in shape.children for label in _labels(child)]


def test_frozen_p19_delta_mask_and_exact_motion_contract() -> None:
    p = p20.P20_R2_DEFAULTS
    baseline = asdict(p19.P19_R1_DEFAULTS)
    candidate = asdict(p)
    changed = {
        name: (baseline[name], value)
        for name, value in candidate.items()
        if value != baseline[name]
    }
    assert changed == {
        "fixed_axle_center_y": (-13.0, -15.0),
        "fixed_axle_center_z": (-9.0, -11.0),
        "theta_end_deg": (5.0, 45.0),
    }
    assert p20.outer_rotation_center_yz(p).as_tuple() == (0.0, 0.0)
    assert p20.fixed_axle_center_yz(p).as_tuple() == (-15.0, -11.0)
    assert p.fixed_axle_guide_slot_width == pytest.approx(7.90)
    assert p.fixed_axle_guide_sample_count == 33
    assert p20.P20_R2_STATE_THETA == {
        "open": 0.0,
        "mid": 22.5,
        "end": 45.0,
    }


def test_fixed_axle_inverse_frame_loci_are_true_arcs_and_reconstruct() -> None:
    p = p20.P20_R2_DEFAULTS
    radius = hypot(15.0, 11.0)
    expected = {
        ("left", 0.0): (-15.0, -11.0),
        ("left", 0.5): (-18.067710743685, -4.422423372148),
        ("left", 1.0): (-18.384776310850, 2.828427124746),
        ("right", 0.0): (-15.0, -11.0),
        ("right", 0.5): (-9.648675231653, -15.902926343101),
        ("right", 1.0): (-2.828427124746, -18.384776310850),
    }
    for side in ("left", "right"):
        locus = p20.fixed_axle_rail_locus(side, p)
        assert len(locus) == 33
        assert locus[0] != locus[-1]
        for point in locus:
            assert hypot(point.y, point.z) == pytest.approx(radius, abs=1.0e-12)
        for u in (0.0, 0.25, 0.5, 0.75, 1.0):
            local = p20.fixed_axle_local_center(side, u, p)
            world = p20.reconstruct_fixed_axle_world(side, u, p)
            assert world.as_tuple() == pytest.approx((-15.0, -11.0), abs=1.0e-10)
            assert p20.inverse_outer_local_to_world(side, local, u, p).as_tuple() == pytest.approx(
                (-15.0, -11.0), abs=1.0e-10
            )
        for u in (0.0, 0.5, 1.0):
            assert p20.fixed_axle_local_center(side, u, p).as_tuple() == pytest.approx(
                expected[(side, u)], abs=1.0e-11
            )
    with pytest.raises(ValueError):
        p20.fixed_axle_local_center("left", -1.0e-9, p)
    with pytest.raises(ValueError):
        p20.fixed_axle_local_center("right", 1.000000001, p)


def test_approved_physical_twist_signs_rotate_only_about_c() -> None:
    p = p20.P20_R2_DEFAULTS
    assert p20.rotation_for_side("left", 45.0) == 45.0
    assert p20.rotation_for_side("right", 45.0) == -45.0
    assert p20.outer_rotation_center_yz(p).as_tuple() == (0.0, 0.0)
    assert p20.fixed_axle_center_yz(p).as_tuple() == (-15.0, -11.0)
    assert p20.fixed_axle_local_center("left", 1.0, p).as_tuple() == pytest.approx(
        (-18.384776310850235, 2.828427124746188), abs=1.0e-12
    )
    assert p20.fixed_axle_local_center("right", 1.0, p).as_tuple() == pytest.approx(
        (-2.828427124746192, -18.384776310850235), abs=1.0e-12
    )
    for side in ("left", "right"):
        for u in (0.0, 0.5, 1.0):
            assert p20.reconstruct_fixed_axle_world(side, u, p).as_tuple() == pytest.approx(
                (-15.0, -11.0), abs=1.0e-10
            )


def test_outer_topology_has_only_fixed_axle_arc_and_preserves_inner_tracks() -> None:
    evidence = p20.topology_evidence()
    assert evidence["outerWhiteRodCutCount"] == 0
    assert evidence["innerWhiteRodCutCount"] == 6
    assert evidence["fixedAxleArcRailCount"] == 2
    assert evidence["allPlatesSingleValidSolids"]
    assert evidence["innerRailLociExactlyP19"]
    assert evidence["outerArcVsRoundEndpointChordMm"] == pytest.approx(
        14.236646635318, abs=1.0e-10
    )
    assert evidence["minimumOuterRimWebMm"] >= 4.79
    labels = _labels(p20.build_motion_state("open"))
    assert len([label for label in labels if "OD4_rod_L50.00" in label]) == 3
    assert len([label for label in labels if "fixed_axle_curved_rail" in label]) == 2


def test_actual_axle_passes_through_both_curved_slots_for_all_33_states() -> None:
    evidence = p20.fixed_axle_brep_evidence()
    assert evidence["sampleCountPerSide"] == 33
    assert evidence["maximumAxleOuterPlateIntersectionMm3"] <= 1.0e-7
    assert evidence["minimumAxleOuterPlateClearanceMm"] >= 0.148
    assert evidence["allOuterPlatesSingleValidSolids"]
    assert evidence["passes"]


def test_collision_census_fail_closed_allows_only_six_named_rod_outer_pairs() -> None:
    evidence = p20.collision_census_evidence()
    assert evidence["sampleCount"] == 33
    assert set(evidence["expectedCollisionPairs"]) == {
        f"{name}_rod:{side}_outer"
        for name in p19.ROD_NAMES
        for side in ("left", "right")
    }
    assert evidence["expectedPairCount"] == 6
    assert evidence["allExpectedPairsCollideAtEveryState"]
    assert evidence["minimumExpectedIntersectionMm3"] > 1.0
    assert evidence["maximumUnexpectedIntersectionMm3"] <= 1.0e-7
    assert evidence["unexpectedCollisionPairs"] == ()
    assert evidence["passes"]


def test_service_and_p19_regressions_remain_separate_from_non_product_collision() -> None:
    service = p20.service_evidence()
    assert service["passes"]
    assert service["toolOccurrenceCount"] == 2
    assert service["maximumProductionToolIntersectionMm3"] <= 1.0e-7
    assert service["minimumAxleServiceClearanceMm"] > 0.0
    assert p19.interface_alignment_evidence()["passes"]
    assert p19.triangle_motion_evidence()["triangles"]["end"]["areaMm2"] == pytest.approx(
        0.0, abs=1.0e-10
    )


def test_required_cad_entrypoints_sidecar_and_non_product_manifest() -> None:
    cad = ROOT / "cad/p20_r2_fixed_rod_arc_rail"
    for stem in ("open", "mid", "end", "full_motion", "fixed_rail_review"):
        assert (cad / f"p20_r2_{stem}.step.py").exists()
    sidecar = (cad / "p20_r2_full_motion.params.js").read_text()
    assert "const THETA_END_DEG = 45.0" in sidecar
    assert "origin: ORIGIN" in sidecar
    assert "fixed_stepped_center_axle" not in sidecar.split("effects.transform", 1)[-1]
    manifest = p20.p20_r2_manifest()
    assert manifest["candidateStatus"] == "intermediate_non_product_fixed_rod_arc_rail"
    assert manifest["whiteRodOuterRailCount"] == 0
    assert manifest["knownRodOuterCollisionPairCount"] == 6
    assert manifest["physicalAcceptanceClaimed"] is False
    assert manifest["manufacturingAcceptanceClaimed"] is False
