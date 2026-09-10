from __future__ import annotations

from math import pi
from pathlib import Path

import pytest
from build123d import import_step

import xt60_bend_jig.p19_r1_front_edge_short_tail as p19
import xt60_bend_jig.p20_r1_fixed_rod_reset_scaffold as p20


ROOT = Path(__file__).parents[1]


def _labels(shape):
    if not shape.children:
        return [shape.label]
    return [label for child in shape.children for label in _labels(child)]


def test_scaffold_contract_parameters_and_p19_world_paths_are_frozen() -> None:
    p = p20.P20_R1_SCAFFOLD_DEFAULTS
    assert p20.SCAFFOLD_STATUS == "evidence-only intentionally-colliding non-candidate scaffold"
    assert p20.fixed_axle_center_yz(p).as_tuple() == pytest.approx((-15.0, -11.0))
    assert p.theta_end_deg == pytest.approx(45.0)
    assert p.rod_diameter == pytest.approx(4.0)
    assert p.rod_length_target == pytest.approx(50.0)
    for u in (0.0, 0.5, 1.0):
        state = p20.motion_state(u, p)
        baseline = p19.motion_state(u)
        assert state.alpha_left_deg == pytest.approx(-45.0 * u)
        assert state.alpha_right_deg == pytest.approx(+45.0 * u)
        for name in p20.ROD_NAMES:
            assert state.rod(name).as_tuple() == pytest.approx(
                baseline.rod(name).as_tuple(), abs=1.0e-12
            )
    with pytest.raises(ValueError):
        p20.motion_state(-1.0e-6, p)
    with pytest.raises(ValueError):
        p20.motion_state(1.000001, p)


def test_centered_outer_transform_is_pure_invertible_and_keeps_axle_constant() -> None:
    p = p20.P20_R1_SCAFFOLD_DEFAULTS
    axle = p20.fixed_axle_center_yz(p)
    for side in ("left", "right"):
        for u in (0.0, 0.25, 0.5, 1.0):
            assert p20.fixed_axle_guide_local_center(side, u, p).as_tuple() == pytest.approx((0.0, 0.0))
            assert p20.centered_outer_local_to_world(
                p20.PointYZ(0.0, 0.0), side, u, p
            ).as_tuple() == pytest.approx(axle.as_tuple(), abs=1.0e-12)
            for point in (p20.PointYZ(0.0, 0.0), p20.PointYZ(15.0, 11.0), p20.PointYZ(-4.0, 7.0)):
                world = p20.centered_outer_local_to_world(point, side, u, p)
                rebuilt = p20.world_to_centered_outer_local(world, side, u, p)
                assert rebuilt.as_tuple() == pytest.approx(point.as_tuple(), abs=1.0e-12)


def test_outer_plate_is_disk_minus_one_centered_round_journal_only() -> None:
    p = p20.P20_R1_SCAFFOLD_DEFAULTS
    for side, diameter in (
        ("left", p.left_outer_secondary_grip_diameter),
        ("right", p.right_outer_primary_grip_diameter),
    ):
        plate = p20.build_outer_plate(side, 0.0, p)
        expected = pi * (
            (diameter / 2.0) ** 2 - (p.outer_bearing_bore_diameter / 2.0) ** 2
        ) * p.outer_plate_thickness
        assert plate.is_valid
        assert plate.volume == pytest.approx(expected, abs=1.0e-5)
        assert "zero_outer_rod_rails" in plate.label
        assert "centered_round_axle_journal" in plate.label


def test_inner_rails_and_fixed_hardware_are_preserved_at_new_axle_datum() -> None:
    p = p20.P20_R1_SCAFFOLD_DEFAULTS
    for side in ("left", "right"):
        inner = p20.build_inner_plate(side, p)
        assert inner.is_valid
        assert "three_straight_closed_tracks" in inner.label
        for u in (0.0, 0.5, 1.0):
            for name in p20.ROD_NAMES:
                assert p20.intersection_volume(
                    p20.build_rod(name, 45.0 * u, p), inner
                ) <= 1.0e-7
    axle = p20.build_center_axle(p)
    for side in ("left", "right"):
        assert p20.intersection_volume(axle, p20.build_outer_plate(side, 45.0, p)) <= 1.0e-7


def test_six_open_rod_outer_collisions_are_measured_not_suppressed() -> None:
    evidence = p20.scaffold_collision_evidence()
    assert evidence["expectedPairCount"] == 6
    assert tuple(evidence["expectedPairs"]) == tuple(
        f"{name}_rod::{side}_outer_plate"
        for name in p20.ROD_NAMES
        for side in ("left", "right")
    )
    assert all(volume > 0.0 for volume in evidence["openExpectedCollisionMm3ByPair"].values())
    assert evidence["openExpectedCollisionTotalMm3"] == pytest.approx(
        sum(evidence["openExpectedCollisionMm3ByPair"].values())
    )
    assert evidence["unexpectedCollisionPairs"] == ()
    assert evidence["passesExceptExpectedSixOpenRodOuterCollisions"]
    for row in evidence["states"].values():
        assert row["unexpectedCollisionMm3ByPair"] == {}
        assert row["unexpectedServiceEnvelopeCollisionMm3ByPair"] == {}
    preserved = evidence["preservedP19ReferenceContactMm3ByPair"]
    assert "open:center_axle::left_keeper" in preserved
    assert "open:center_axle::right_keeper" in preserved
    assert "open:xt60_reference::wire_reference" in preserved


def test_collision_boolean_failure_is_a_named_fail_closed_error() -> None:
    class BrokenShape:
        def __and__(self, other):
            del other
            raise RuntimeError("forced common failure")

    with pytest.raises(
        p20.CollisionEvaluationError,
        match="BREP common failed; collision state is unknown",
    ):
        p20.intersection_volume(BrokenShape(), BrokenShape())


def test_scaffold_occurrence_census_entrypoints_and_sidecar_are_explicit() -> None:
    open_state = p20.build_motion_state("open")
    labels = _labels(open_state)
    assert len([label for label in labels if "OD4_rod_L50.00" in label]) == 3
    assert len([label for label in labels if "permanent_follower_cap" in label]) == 6
    assert len([label for label in labels if "zero_outer_rod_rails" in label]) == 2
    service_labels = [
        child.label for child in open_state.children if "reference_service_envelopes" in child.label
    ]
    assert service_labels == ["reference_service_envelopes_theta_0.0"]
    assert len(p20.build_motion_state("open").children) == 19
    assert len(p20.build_motion_state("mid").children) == 19
    assert len(p20.build_motion_state("end").children) == 19
    assert len(p20.build_full_motion_open().children) == 18
    assert all("scaffold" in label.lower() or label.startswith("reference_") for label in labels)

    cad = ROOT / "cad/p20_r1_fixed_rod_reset_scaffold"
    for stem in ("open", "mid", "end", "full_motion"):
        assert (cad / f"p20_r1_scaffold_{stem}.step.py").exists()
    sidecar = (cad / "p20_r1_scaffold_full_motion.params.js").read_text()
    assert "const AXLE_ORIGIN = Object.freeze([0.0, -15.0, -11.0])" in sidecar
    assert "const THETA_END_DEG = 45.0" in sidecar
    assert "evidence-only intentionally-colliding non-candidate scaffold" in sidecar
    assert "outer_rod_rail" not in sidecar
    for fixed in (
        "fixed_stepped_center_axle", "fixed_left_keeper", "fixed_right_keeper",
        "fixed_left_inner", "fixed_right_inner", "fixed_xt60_reference",
        "fixed_workpiece_reference",
    ):
        assert f'effects.transform("{fixed}"' not in sidecar


def test_written_steps_match_source_occurrences_volume_bounds_and_labels() -> None:
    cad = ROOT / "cad/p20_r1_fixed_rod_reset_scaffold"
    sources = {
        "open": p20.build_motion_state("open"),
        "mid": p20.build_motion_state("mid"),
        "end": p20.build_motion_state("end"),
        "full_motion": p20.build_full_motion_open(),
    }
    for stem, source in sources.items():
        exported = import_step(cad / f"p20_r1_scaffold_{stem}.step")
        expected_count = 18 if stem == "full_motion" else 19
        assert len(source.children) == len(exported.children) == expected_count
        # build123d root Compound.volume omits nested compounds such as the
        # restored service occurrence, so compare the explicit top-level
        # occurrence volume census instead of the root convenience property.
        assert sum(child.volume for child in exported.children) == pytest.approx(
            sum(child.volume for child in source.children), abs=1.0e-6
        )
        assert tuple(exported.bounding_box().size) == pytest.approx(
            tuple(source.bounding_box().size), abs=1.0e-6
        )
        assert "scaffold" in exported.label.lower()
        exported_labels = tuple(child.label.lower() for child in exported.children)
        assert all(
            "p20_scaffold" in label or label.startswith("reference_service_envelopes")
            for label in exported_labels
        )
        if stem != "full_motion":
            outer_labels = tuple(label for label in exported_labels if "_outer_" in label)
            assert len(outer_labels) == 2
            assert all("zero_outer_rod_rails" in label for label in outer_labels)
            service_labels = tuple(
                label for label in exported_labels if "reference_service_envelopes" in label
            )
            expected_theta = {"open": "0_0", "mid": "22_5", "end": "45_0"}[stem]
            assert service_labels == (f"reference_service_envelopes_theta_{expected_theta}",)
