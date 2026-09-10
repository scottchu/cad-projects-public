from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest
from build123d import import_step

import xt60_bend_jig.p20_r4_custom_profile_full_cad as r4


def test_exact_profile_and_361_point_inverse_authority() -> None:
    evidence = r4.profile_evidence()
    assert sha256(r4.PROFILE_JSON.encode()).hexdigest() == r4.PROFILE_SHA256
    assert evidence["profileSha256"] == r4.PROFILE_SHA256
    assert evidence["pointCountPerPath"] == 361
    assert evidence["greenInnerTravelMm"] <= 1.0e-9
    assert evidence["maxRodInverseRoundTripResidualMm"] <= 1.0e-10
    assert evidence["maxFixedAxleRoundTripResidualMm"] <= 1.0e-10
    assert evidence["brepRailPointCount"] == 33
    assert evidence["brepInterpolationMaxDeviationMm"] <= 0.01
    assert evidence["knownInnerRimWebMm"] == pytest.approx(1.152)
    assert evidence["knownLeftBlueOrangeWebMm"] == pytest.approx(1.715)
    assert not evidence["manufacturingAccepted"]


def test_exact_open_mid_end_coordinates_and_motion_signs() -> None:
    expected = {
        "bottom": ((-7.511545005, 14.127161486), (-2.641733675, 9.687731715), (2.228077655, 5.248301944)),
        "diagonal": ((11.313708499, 11.313708499), (9.895893077, 5.406005222), (8.478077655, -0.501698056)),
        "upright": ((14.728077655, -6.251698056),) * 3,
    }
    for name, rows in expected.items():
        for u, wanted in zip((0.0, 0.5, 1.0), rows):
            assert r4.world_rod_center(name, u).as_tuple() == pytest.approx(wanted, abs=1.0e-9)
    assert r4.outer_rotation_deg("left", 1.0) == 45.0
    assert r4.outer_rotation_deg("right", 1.0) == -45.0


def test_full_preview_census_constraints_and_valid_solids() -> None:
    for state in ("open", "mid", "end"):
        assembly = r4.build_motion_state(state)
        census = r4.occurrence_census(assembly)
        assert census["occurrenceCount"] == 18
        assert census["plateCount"] == 4
        assert census["rodCount"] == 3
        assert census["capCount"] == 6
        assert census["keeperCount"] == 2
        assert census["hasXt60"] and census["has90DegWorkpiece"]
        assert all(child.is_valid and child.volume > 0 for child in assembly.children)
    p = r4.P20_R4_DEFAULTS
    assert (p.inner_plate_radius, p.outer_plate_radius) == (20.0, 22.5)
    assert p.inner_clear_span == pytest.approx(28.4)
    assert (p.left_inner_x, p.right_inner_x) == pytest.approx((-15.8, 15.8))
    assert (p.left_outer_x, p.right_outer_x) == pytest.approx((-19.4, 19.4))
    assert p.center_axle_total_length == pytest.approx(44.9)
    assert p.rod_length_target == 50.0
    assert p.available_cap_rod_engagement == pytest.approx(3.70)
    assert p.cap_socket_id == pytest.approx(4.10)
    assert p.cap_socket_id - p.rod_diameter == pytest.approx(0.10)
    assert p.follower_head_length == 9.05


def test_open_mid_end_actual_solids_keep_rods_axle_and_caps_clear_of_plates() -> None:
    evidence = r4.actual_solid_evidence()
    assert evidence["states"] == ("open", "mid", "end")
    assert evidence["maximumRodPlateIntersectionMm3"] <= 1.0e-7
    assert evidence["maximumAxleOuterIntersectionMm3"] <= 1.0e-7
    assert evidence["maximumCapPlateIntersectionMm3"] <= 1.0e-7
    assert evidence["minimumCapOuterAxialClearanceMm"] == pytest.approx(0.30, abs=1.0e-9)
    assert evidence["rodSupportedByInnerAndOuterFeatures"]
    assert evidence["fixedAxleWorldInvariant"]
    assert evidence["passesPreviewCollisionGate"]


def test_viewer_entry_and_all_static_entries_exist() -> None:
    root = Path(__file__).parents[1]
    cad = root / "cad/p20_r4_custom_profile_full_cad"
    for stem in ("open", "mid", "end", "exploded", "full_motion"):
        assert (cad / f"p20_r4_{stem}.step.py").exists()
    sidecar = (cad / "p20_r4_full_motion.params.js").read_text()
    assert 'step: { path: "cad/p20_r4_custom_profile_full_cad/p20_r4_full_motion.step" }' in sidecar
    assert "leftDeg: 45.0 * u" in sidecar
    assert "rightDeg: -45.0 * u" in sidecar


def test_written_steps_export_distinct_left_and_right_inner_occurrences() -> None:
    root = Path(__file__).parents[1]
    cad = root / "cad/p20_r4_custom_profile_full_cad"
    for stem in ("open", "mid", "end", "exploded"):
        labels = [child.label for child in import_step(cad / f"p20_r4_{stem}.step").children]
        assert labels.count("fixed_left_inner_R20_blue_orange_rails_green_round_bore") == 1
        assert labels.count("fixed_right_inner_R20_blue_orange_rails_green_round_bore") == 1
    labels = [child.label for child in import_step(cad / "p20_r4_full_motion.step").children]
    assert labels.count("motion_full_fixed_left_inner") == 1
    assert labels.count("motion_full_fixed_right_inner") == 1
