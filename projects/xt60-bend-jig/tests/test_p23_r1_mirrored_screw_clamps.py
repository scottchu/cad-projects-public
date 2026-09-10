from __future__ import annotations

from itertools import combinations
from pathlib import Path

import pytest
from build123d import import_step

import xt60_bend_jig.p20_r4_custom_profile_full_cad as p20
import xt60_bend_jig.p23_r1_mirrored_screw_clamps as p23


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad/p23_r1_mirrored_screw_clamps"


def _leaf_labels(shape) -> tuple[str, ...]:
    return tuple(child.label for child in p23.iter_leaf_shapes(shape))


def test_purchased_rods_and_inherited_yz_paths_are_exact() -> None:
    params = p23.P23_R1_DEFAULTS
    assert params.rod_diameter == 4.00
    assert params.rod_length == 50.00
    assert p20.P20_R4_DEFAULTS.rod_diameter == params.rod_diameter
    assert p20.P20_R4_DEFAULTS.rod_length_target == params.rod_length

    for role, p20_name in p23.ROD_ROLE_TO_P20_NAME.items():
        for progress in (0.0, 0.25, 0.5, 0.75, 1.0):
            assert p23.inherited_rod_center(role, progress).as_tuple() == pytest.approx(
                p20.world_rod_center(p20_name, progress).as_tuple(), abs=1.0e-12
            )


def test_orange_shoe_pure_math_has_exact_travel_and_equal_pitch_turns() -> None:
    assert p23.orange_shoe_center(0.0).as_tuple() == pytest.approx(
        (11.313708499, 11.313708499), abs=1.0e-9
    )
    assert p23.orange_shoe_center(1.0).as_tuple() == pytest.approx(
        (8.478077655, -0.501698056), abs=1.0e-9
    )
    assert p23.orange_travel_distance() == pytest.approx(12.150911, abs=5.0e-7)
    expected_turns = p23.orange_travel_distance() / 2.0
    assert p23.screw_turns(1.0) == pytest.approx(expected_turns, abs=1.0e-12)
    for side in ("left", "right"):
        assert p23.capture_manifest(side) == (
            f"{side}_green_fixed_capture",
            f"{side}_blue_follower_capture",
            f"{side}_orange_shoe_capture",
        )


def test_modules_are_x_mirrored_with_blind_outer_walls() -> None:
    params = p23.P23_R1_DEFAULTS
    assert p23.side_yoke_center_x("left") == pytest.approx(-p23.side_yoke_center_x("right"))
    assert p23.side_inner_face_x("left") == pytest.approx(-p23.side_inner_face_x("right"))
    assert p23.blind_socket_center_x("left") == pytest.approx(-p23.blind_socket_center_x("right"))
    assert p23.screw_axis_x("left") == pytest.approx(-p23.screw_axis_x("right"))
    assert params.yoke_inner_face_abs_x - 21.0 == pytest.approx(params.outer_plate_running_gap)
    assert params.yoke_thickness_x - params.socket_depth == pytest.approx(params.socket_outer_wall)
    assert abs(p23.blind_socket_end_x("left")) - 25.0 == pytest.approx(params.socket_end_clearance)


def test_open_and_clamped_have_no_caps_two_modules_and_six_captures() -> None:
    for state in ("open", "clamped"):
        assembly = p23.build_preview(state)
        evidence = p23.occurrence_census(assembly)
        labels = evidence["labels"]
        assert evidence["rodCount"] == 3
        assert evidence["capCount"] == 0
        assert evidence["moduleCount"] == 2
        assert evidence["captureCount"] == 6
        assert sum("left_printed_screw_with_knob" in label for label in labels) == 1
        assert sum("right_printed_screw_with_knob" in label for label in labels) == 1
        assert all(leaf.is_valid and leaf.volume > 0.0 for leaf in p23.iter_leaf_shapes(assembly))


def test_yokes_and_screw_with_knob_are_each_one_connected_solid() -> None:
    for side in ("left", "right"):
        assert len(p23.build_fixed_yoke(side).solids()) == 1
        for progress in (0.0, 0.5, 1.0):
            assert len(p23.build_screw_with_knob(side, progress).solids()) == 1


def test_module_parts_have_no_unintended_pairwise_overlap() -> None:
    intersection_volume = p20.p19._intersection_volume
    for progress in (0.0, 1.0):
        for side in ("left", "right"):
            for first, second in combinations(p23.module_parts(side, progress), 2):
                assert intersection_volume(first, second) <= 1.0e-7, (
                    progress,
                    first.label,
                    second.label,
                )


def test_keyed_orange_captive_pullback_and_x_retention_contract() -> None:
    params = p23.P23_R1_DEFAULTS
    assert params.orange_shoe_length != params.orange_shoe_width
    assert params.captive_head_cavity_diameter > params.captive_head_diameter
    assert params.captive_head_cavity_length > params.captive_head_thickness
    assert params.captive_neck_slot_diameter > params.captive_neck_diameter
    assert params.retention_lip_thickness_x > 0.0
    assert params.retention_flange_thickness_x < params.retention_cavity_thickness_x

    for side in ("left", "right"):
        assert "x_retention_face_lips" in p23.build_fixed_yoke(side).label
        for progress in (0.0, 1.0):
            blue = p23.build_blue_follower(side, progress)
            orange = p23.build_orange_shoe(side, progress)
            screw = p23.build_screw_with_knob(side, progress)
            assert "x_retention_flange" in blue.label
            assert "anti_rotation_keyed" in orange.label
            assert "x_retention_flange" in orange.label
            assert "captive_T_head_pocket" in orange.label
            assert "captive_T_head" in screw.label
            assert all(len(part.solids()) == 1 for part in (blue, orange, screw))


def test_knob_stays_outside_nut_with_declared_clearance_throughout_travel() -> None:
    params = p23.P23_R1_DEFAULTS
    for progress in (0.0, 0.25, 0.5, 0.75, 1.0):
        assert p23.knob_nut_clearance(progress) >= params.knob_nut_clearance - 1.0e-9


def test_side_modules_clear_outer_plates_and_all_three_purchased_rods() -> None:
    intersection_volume = p20.p19._intersection_volume
    for progress in (0.0, 1.0):
        rods = {name: p20.build_rod(name, progress) for name in p20.ROD_NAMES}
        for side in ("left", "right"):
            module = p23.build_side_module(side, progress)
            outer = p20.build_outer_plate(side, progress)
            for leaf in p23.iter_leaf_shapes(module):
                assert intersection_volume(leaf, outer) <= 1.0e-7, leaf.label
                for rod in rods.values():
                    assert intersection_volume(leaf, rod) <= 1.0e-7, leaf.label


def test_open_and_clamped_context_rods_remain_exactly_od4_x_50() -> None:
    for state in ("open", "clamped"):
        assembly = p23.build_preview(state)
        rods = [leaf for leaf in p23.iter_leaf_shapes(assembly) if "_OD4_rod_L50.00" in leaf.label]
        assert len(rods) == 3
        for rod in rods:
            bounds = rod.bounding_box().size
            assert bounds.X == pytest.approx(50.0, abs=1.0e-7)
            assert sorted((bounds.Y, bounds.Z)) == pytest.approx([4.0, 4.0], abs=1.0e-7)


def test_explicit_entrypoints_and_nonempty_written_steps() -> None:
    for state in ("open", "clamped"):
        source = CAD / f"p23_r1_{state}.step.py"
        artifact = CAD / f"p23_r1_{state}.step"
        assert source.exists()
        assert artifact.exists() and artifact.stat().st_size > 10_000
        imported = import_step(artifact)
        assert imported.is_valid and imported.volume > 0.0
        labels = _leaf_labels(imported)
        assert not any("permanent_cap" in label for label in labels)
        assert any("left_printed_screw_with_knob" in label for label in labels)
        assert any("right_printed_screw_with_knob" in label for label in labels)
