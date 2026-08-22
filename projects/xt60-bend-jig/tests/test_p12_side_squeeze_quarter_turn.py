from __future__ import annotations

from itertools import combinations
from math import cos, radians, sin
from pathlib import Path

import pytest
from build123d import import_step

import xt60_bend_jig.p11_asymmetric_three_rod_solder_jig as p11
import xt60_bend_jig.p12_side_squeeze_quarter_turn as p12


def intersection_volume(first, second) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return common.volume
    return sum(item.volume for item in common)


def shape_bounds(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return (*box.min, *box.max)


def leaf_shapes(shape):
    if not shape.children:
        return [shape]
    leaves = []
    for child in shape.children:
        leaves.extend(leaf_shapes(child))
    return leaves


def test_p12_preserves_p11_workpiece_and_three_role_specific_rods() -> None:
    p = p12.P12_DEFAULTS
    assert p.motion is p11.P11_DEFAULTS
    assert (p.motion.rod_diameter, p.motion.rod_length) == (4.0, 50.0)
    assert p.principal_width_x < p.motion.rod_length
    assert len(p11.build_rods(p.motion.end_angle, p.motion).children) == 3
    for name in p12.ROD_NAMES:
        for angle in (0.0, 5.0, 10.0, 20.0, 27.0, 32.0, 35.0):
            assert p11.rod_center(name, angle, p.motion) == p11.rod_center(
                name, angle, p11.P11_DEFAULTS
            )
    assert p11.travel_fraction("upright", 20.0) == 1.0
    assert p11.travel_fraction("bottom", 27.0) == 1.0
    assert p11.travel_fraction("diagonal", 32.0) == 1.0


def test_compact_core_has_no_bottom_plate_or_full_disc() -> None:
    p = p12.P12_DEFAULTS
    core = p12.printed_core_parts(0.0, p)
    assert len(core) == 4
    assert all(not part.label.startswith("bottom_plate") for part in core)
    assert all("full_disc" not in part.label for part in core)
    assert "no_bottom_plate" in p12.build_spine(p).label
    p11_volume = p11.build_base(p.motion).volume + sum(
        part.volume for part in p11.build_principal_plates(0.0, p.motion).children
    )
    p12_volume = sum(part.volume for part in core)
    assert p12_volume / p11_volume < 0.45


def test_two_cheeks_one_cam_and_spine_are_valid_and_non_overlapping() -> None:
    p = p12.P12_DEFAULTS
    for angle in (0.0, p.motion.end_angle):
        core = p12.printed_core_parts(angle, p)
        assert all(part.is_valid and part.volume > 0.0 for part in core)
        for first, second in combinations(core, 2):
            assert intersection_volume(first, second) <= 1e-7
    assert p12.build_cheek("left", p).distance_to(p12.build_spine(p)) == pytest.approx(0.0)
    assert p12.build_cheek("right", p).distance_to(p12.build_spine(p)) == pytest.approx(0.0)


def test_spine_is_xt60_backstop_with_clearance_and_no_workpiece_overlap() -> None:
    p = p12.P12_DEFAULTS
    spine = p12.build_spine(p)
    xt60 = p11.build_xt60(p.motion)
    spine_front = p.spine_y + p.spine_depth_y / 2.0
    xt60_rear = -p.motion.xt60_y / 2.0
    assert xt60_rear - spine_front == pytest.approx(0.10, abs=1e-9)
    for child in p11.build_workpiece(p.motion).children:
        assert intersection_volume(spine, child) <= 1e-7
    assert "clamp_tongue" in spine.label
    assert intersection_volume(spine, xt60) <= 1e-7


@pytest.mark.parametrize("angle", (0.0, 5.0, 10.0, 20.0, 27.0, 32.0, 35.0))
def test_rods_clear_both_cheeks_and_rotating_cam_through_stroke(angle: float) -> None:
    p = p12.P12_DEFAULTS
    for rod in p11.build_rods(angle, p.motion).children:
        for printed in p12.printed_core_parts(angle, p):
            assert intersection_volume(rod, printed) <= 1e-7


def test_cam_inverse_slots_reconstruct_all_three_independent_rod_laws() -> None:
    p = p12.P12_DEFAULTS
    for name in p12.ROD_NAMES:
        for index in range(141):
            angle = p.motion.end_angle * index / 140.0
            local = p11.inverse_slot_point(name, angle, p.motion)
            a = radians(angle)
            dy = local.y - p.motion.shaft_y
            dz = local.z - p.motion.shaft_z
            world = p12.PointYZ(
                p.motion.shaft_y + cos(a) * dy - sin(a) * dz,
                p.motion.shaft_z + sin(a) * dy + cos(a) * dz,
            )
            assert world.distance_to(p11.rod_center(name, angle, p.motion)) <= 1e-9


def test_open_and_lock_detent_pockets_index_to_same_fixed_nose() -> None:
    p = p12.P12_DEFAULTS
    nose = p12._detent_nose_world(p)
    for angle in (0.0, p.motion.end_angle):
        local = p12._detent_pocket_local(angle, p)
        a = radians(angle)
        dy = local.y - p.motion.shaft_y
        dz = local.z - p.motion.shaft_z
        world = p12.PointYZ(
            p.motion.shaft_y + cos(a) * dy - sin(a) * dz,
            p.motion.shaft_z + sin(a) * dy + cos(a) * dz,
        )
        assert world.distance_to(nose) <= 1e-9


def test_hard_stop_allows_35_degrees_and_blocks_further_rotation() -> None:
    p = p12.P12_DEFAULTS
    sampled = [p12.stop_signed_clearance(index / 4.0, p) for index in range(141)]
    assert min(sampled) >= -1e-9
    assert p12.stop_signed_clearance(35.0, p) == pytest.approx(0.0, abs=1e-9)
    assert p12.stop_signed_clearance(35.25, p) < 0.0
    assert p12.stop_signed_clearance(36.0, p) < 0.0


def test_round_retainers_define_one_locked_and_one_releasable_rod_end() -> None:
    p = p12.P12_DEFAULTS
    point = p11.rod_center("upright", p.motion.end_angle, p.motion)
    rod = p11.build_rod("upright", p.motion.end_angle, p.motion)
    cap = p12.build_left_rod_cap(point, p)
    keeper = p12.build_right_rod_keeper(point, p)
    assert "round_rod_cap_3p90" in cap.label
    assert "round_rod_C_keeper_4p10" in keeper.label
    assert intersection_volume(cap, rod) > 1.0
    assert intersection_volume(keeper, rod) <= 1e-7
    assert intersection_volume(p12.build_shaft(p), p12.build_shaft_keeper(p)) <= 1e-7


def test_solder_tool_paths_clear_all_printed_parts_at_lock() -> None:
    p = p12.P12_DEFAULTS
    printed = [
        *p12.build_frame(p.motion.end_angle, p).children,
        *p12.build_retainers(p.motion.end_angle, p).children,
    ]
    for tool in p11.build_solder_tool_sweeps(p.motion).children:
        for part in printed:
            assert intersection_volume(tool, part) <= 1e-7


def test_print_kit_has_twelve_non_overlapping_parts_on_180mm_bed() -> None:
    kit = p12.build_print_kit()
    assert len(kit.children) == 12
    box = kit.bounding_box()
    assert box.size.X <= 180.0
    assert box.size.Y <= 180.0
    for child in kit.children:
        assert child.is_valid and child.volume > 0.0
        assert child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    for first, second in combinations(kit.children, 2):
        assert intersection_volume(first, second) <= 1e-7


def test_required_generators_are_exactly_the_five_p12_views() -> None:
    root = Path(__file__).parents[1]
    folder = root / "cad" / "p12_side_squeeze_quarter_turn"
    expected = {
        "p12_loaded_open.step.py",
        "p12_loaded_closed.step.py",
        "p12_solder_access.step.py",
        "p12_exploded.step.py",
        "p12_print_kit.step.py",
    }
    assert {path.name for path in folder.glob("*.step.py")} == expected


def test_all_generated_steps_match_source_leaf_geometry_when_present() -> None:
    root = Path(__file__).parents[1]
    folder = root / "cad" / "p12_side_squeeze_quarter_turn"
    cases = (
        ("p12_loaded_open.step", p12.build_loaded_open()),
        ("p12_loaded_closed.step", p12.build_loaded_closed()),
        ("p12_solder_access.step", p12.build_solder_access()),
        ("p12_exploded.step", p12.build_exploded()),
        ("p12_print_kit.step", p12.build_print_kit()),
    )
    if not all((folder / filename).exists() for filename, _ in cases):
        pytest.skip("P12 STEP artifacts not generated yet")

    for filename, source in cases:
        imported = import_step(folder / filename)
        assert imported.is_valid
        assert imported.label == source.label
        assert shape_bounds(imported) == pytest.approx(shape_bounds(source), abs=2e-6)
        imported_leaves = leaf_shapes(imported)
        source_leaves = leaf_shapes(source)
        assert [leaf.label for leaf in imported_leaves] == [leaf.label for leaf in source_leaves]
        assert len(imported_leaves) == len(source_leaves)
        for imported_leaf, source_leaf in zip(imported_leaves, source_leaves):
            assert shape_bounds(imported_leaf) == pytest.approx(
                shape_bounds(source_leaf), abs=2e-6
            )
            assert len(imported_leaf.solids()) == len(source_leaf.solids())
            assert len(imported_leaf.faces()) == len(source_leaf.faces())
            assert imported_leaf.volume == pytest.approx(
                source_leaf.volume, rel=1e-8, abs=1e-6
            )
