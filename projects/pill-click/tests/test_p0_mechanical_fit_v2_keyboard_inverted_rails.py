"""Deterministic contract tests for the isolated V2 mechanical prototype."""

from itertools import combinations
from pathlib import Path

import numpy as np
import pytest
import trimesh
from build123d import Location, Vector, export_stl

from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails import (
    P0_MECHANICAL_FIT_V2,
    make_blind_two_side_latch_rear_cover,
    make_c5_arm_cover_specimen,
    make_c5_coupon_assembly,
    make_c5_housing_receiver_specimen,
    make_deflected_side_latch_arm,
    make_outer_housing,
    make_pressed_assembly,
    make_print_bundle,
    make_rear_cover_core,
    make_released_assembly,
    make_side_latch_arm,
    make_side_latch_connector_pad,
    make_side_latch_hook,
    make_solid_keyboard_button,
    print_blind_two_side_latch_rear_cover,
    print_c5_arm_cover_specimen,
    print_c5_housing_receiver_specimen,
    print_outer_housing,
    print_solid_keyboard_button,
)
from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails.geometry import (
    _box_bounds,
    _male_rail,
    _rail_spine,
    _side_latch_root_local,
)


p = P0_MECHANICAL_FIT_V2
TOL = 1e-6


def _bbox(shape):
    box = shape.bounding_box()
    return (box.min.X, box.max.X, box.min.Y, box.max.Y, box.min.Z, box.max.Z)


def _intersection(first, second) -> float:
    return (first & second).volume


@pytest.fixture(scope="module")
def parts():
    return (
        make_outer_housing(),
        make_solid_keyboard_button(),
        make_blind_two_side_latch_rear_cover(),
    )


def test_frozen_math_contract() -> None:
    assert p.main_guide_size_xz - p.inner_body_size_xz == pytest.approx(0.4)
    assert p.male_rail_source_x == pytest.approx((16.9, 18.3))
    assert p.female_channel_x == pytest.approx((17.3, 18.5))
    assert p.female_mouth_x == pytest.approx((17.3, 18.9))
    assert p.rail_radial_engagement == pytest.approx(1.0)
    assert p.minimum_opposite_rail_engagement == pytest.approx(0.8)
    assert p.rail_stop_contact_area_total == pytest.approx(8.8)
    assert p.released_endplay == pytest.approx(0.15)
    assert p.rear_feed_first_entry_center_y == pytest.approx(-15.5)
    assert p.latch_strain(0.55) == pytest.approx(0.014666666666666666)
    assert p.side_latch_hook_pad_amplification == pytest.approx(1.375)
    assert p.predicted_hook_release_travel == pytest.approx(0.55)
    assert p.predicted_hook_stop_travel == pytest.approx(0.6875)
    assert p.pad_load_strain(0.4) == pytest.approx(1 / 60)
    assert p.pad_load_strain(0.5) == pytest.approx(1 / 48)


def test_exactly_three_valid_positive_single_solid_parts(parts) -> None:
    assert len(parts) == 3
    for part in parts:
        assert part.is_valid and part.volume > 0
        assert len(part.solids()) == 1
    labels = {part.label for part in parts}
    assert labels == {
        "p0_mechanical_fit_v2_outer_female_channels_two_side_latch_receivers",
        "p0_mechanical_fit_v2_solid_keyboard_button_four_continuous_male_rails",
        "p0_mechanical_fit_v2_blind_rear_cover_exactly_two_side_squeeze_latches",
    }


def test_part_and_assembly_bounding_boxes(parts) -> None:
    outer, inner, cover = parts
    assert _bbox(outer) == pytest.approx((-20, 20, -18.7, 20, -20, 20))
    assert _bbox(inner) == pytest.approx((-18.3, 18.3, -17.2, 15.5, -17.1, 17.1))
    assert _bbox(cover) == pytest.approx((-20, 20, -20, -9.85, -20, 20))
    pressed = make_pressed_assembly()
    released = make_released_assembly()
    assert len(pressed.children) == len(pressed.solids()) == 3
    assert _bbox(pressed) == pytest.approx((-20, 20, -20, 20, -20, 20))
    assert _bbox(released) == pytest.approx((-20, 20, -20, 33.4, -20, 20))


def test_keyboard_key_is_rounded_tapered_and_solid() -> None:
    inner = make_solid_keyboard_button()
    assert p.key_skirt_size_xz == pytest.approx(34.2)
    assert p.key_face_size_xz == pytest.approx(32.8)
    assert np.degrees(np.arctan(((34.2 - 32.8) / 2) / 3.0)) == pytest.approx(13.1340223)
    assert inner.is_inside(Vector(0, p.key_local_y[1] - 0.01, 0), tolerance=1e-7)
    assert inner.is_inside(Vector(16.35, p.key_local_y[1] - 0.01, 0), tolerance=1e-7)
    assert not inner.is_inside(Vector(16.55, p.key_local_y[1] - 0.01, 0), tolerance=1e-7)
    assert not inner.is_inside(Vector(17.0, p.key_local_y[1] - 0.01, 17.0), tolerance=1e-7)


def test_four_continuous_male_rails_and_spines_have_exact_brep_bounds() -> None:
    inner = make_solid_keyboard_button()
    assert len(p.male_rail_centres_z) * 2 == 4
    for side in (-1.0, 1.0):
        for z_center in p.male_rail_centres_z:
            rail = _male_rail(side, z_center, p)
            spine = _rail_spine(side, z_center, p)
            assert rail.volume == pytest.approx(1.4 * 14.0 * 2.2)
            assert _intersection(inner, rail) == pytest.approx(rail.volume, abs=1e-6)
            assert _intersection(rail, spine) == pytest.approx(1.936, abs=1e-6)
            assert _intersection(spine, _box_bounds(
                (-p.inner_body_half, p.inner_body_half),
                p.inner_body_local_y,
                (-p.inner_body_half, p.inner_body_half),
            )) == pytest.approx(0.352, abs=1e-6)


def test_four_female_channels_mouths_and_blind_stop_walls_are_real_brep(parts) -> None:
    outer = parts[0]
    for side in (-1.0, 1.0):
        normal_x = p.female_channel_x if side > 0 else (-18.5, -17.3)
        mouth_x = p.female_mouth_x if side > 0 else (-18.9, -17.3)
        for z_center in p.male_rail_centres_z:
            normal_void = _box_bounds(
                normal_x,
                (-17.8, p.female_channel_blind_front_y - 0.01),
                (z_center - 1.29, z_center + 1.29),
            )
            mouth_void = _box_bounds(
                mouth_x,
                (-18.69, -17.91),
                (z_center - 1.49, z_center + 1.49),
            )
            stop_wall = _box_bounds(
                normal_x,
                (
                    p.female_channel_blind_front_y,
                    p.female_channel_blind_front_y + p.blind_stop_wall_axial_thickness,
                ),
                (z_center - 1.3, z_center + 1.3),
            )
            assert _intersection(outer, normal_void) < TOL
            assert _intersection(outer, mouth_void) < TOL
            assert _intersection(outer, stop_wall) == pytest.approx(3.744, abs=1e-6)


def test_292_allowed_motion_states_are_collision_free_and_rejection_is_only_stops(parts) -> None:
    outer, inner, cover = parts
    states = [-1.0 + 0.05 * index for index in range(292)]
    assert states[-1] == pytest.approx(13.55)
    for state in states:
        moving = Location((0, p.inner_center_y(state), 0)) * inner
        assert _intersection(outer, moving) < TOL
        assert _intersection(cover, moving) < TOL
    rejected = Location((0, p.inner_center_y(p.rejection_state), 0)) * inner
    assert _intersection(outer, rejected) == pytest.approx(0.44, abs=1e-6)
    assert _intersection(cover, rejected) < TOL


def test_transverse_shift_margin_and_cocking_samples(parts) -> None:
    outer, inner, _ = parts
    diagonal = 0.2 / np.sqrt(2)
    shifts = (
        (-0.2, 0.0),
        (0.2, 0.0),
        (0.0, -0.2),
        (0.0, 0.2),
        (-diagonal, -diagonal),
        (-diagonal, diagonal),
        (diagonal, -diagonal),
        (diagonal, diagonal),
        (0.0, 0.0),
    )
    for state in (p.inward_state, p.pressed_state, 6.0, p.released_state, p.maximum_pull_state):
        for dx, dz in shifts:
            moving = Location((dx, p.inner_center_y(state), dz)) * inner
            assert _intersection(outer, moving) < TOL
    assert np.degrees(np.arctan(0.4 / 14.0)) == pytest.approx(1.636577, abs=1e-6)


def test_390_state_rear_feed_is_collision_free(parts) -> None:
    outer, inner, _ = parts
    centres = [p.feed_start_center_y + p.feed_step * index for index in range(390)]
    assert centres[-1] == pytest.approx(p.feed_end_center_y)
    for center in centres:
        assert _intersection(outer, Location((0, center, 0)) * inner) < TOL
    assert p.rear_feed_first_entry_center_y == pytest.approx(-15.5)


def test_old_tabs_guards_block_bosses_and_key_reliefs_are_absent(parts) -> None:
    _, inner, _ = parts
    old_tab_probe = _box_bounds((18.31, 18.46), (-5.7, -2.7), (-2.5, 2.5))
    # Probe the old boss's extra Z wing, outside the new 2.20-wide rail.
    old_boss_probe = _box_bounds((17.11, 17.89), (-9.9, -3.3), (10.61, 11.64))
    assert _intersection(inner, old_tab_probe) < TOL
    assert _intersection(inner, old_boss_probe) < TOL
    assert "tab" not in inner.label.lower()
    assert "groove" not in inner.label.lower()


def test_exactly_two_side_latches_and_top_bottom_are_clean(parts) -> None:
    outer, _, cover = parts
    assert p.side_latch_count == 2
    for side in (-1.0, 1.0):
        arm = make_side_latch_arm(side)
        assert arm.is_valid and len(arm.solids()) == 1
        assert _intersection(cover, arm) == pytest.approx(arm.volume, abs=1e-6)
    top_band = _box_bounds((-19, 19), (-18.69, -9.86), (6.0, 19.0))
    bottom_band = _box_bounds((-19, 19), (-18.69, -9.86), (-19.0, -6.0))
    core = make_rear_cover_core()
    assert _intersection(cover - core, top_band) < TOL
    assert _intersection(cover - core, bottom_band) < TOL
    # Side access never reaches the top/bottom walls.
    assert outer.is_inside(Vector(19.5, -14.0, 10.0), tolerance=1e-7)
    assert outer.is_inside(Vector(19.5, -14.0, -10.0), tolerance=1e-7)


def test_side_latch_root_hook_pocket_pad_and_stop_math(parts) -> None:
    outer = parts[0]
    root = _side_latch_root_local(p)
    assert root.is_valid and len(root.solids()) == 1
    faceplate_grip = _box_bounds((0, 1), (-0.2, 0), (-3, 3))
    beam_overlap = _box_bounds((0, 1), (0, 0.8), (-3, 3))
    assert _intersection(root, faceplate_grip) == pytest.approx(1.2, abs=1e-6)
    assert _intersection(root, beam_overlap) == pytest.approx(4.8, abs=1e-6)
    assert p.side_latch_hook_apex_x - (p.side_latch_beam_inner_x + p.side_latch_beam_thickness_x) == pytest.approx(0.65)
    assert p.side_latch_pocket_x[1] - p.side_latch_hook_apex_x == pytest.approx(0.10)
    assert p.half_housing - p.side_latch_pocket_x[1] == pytest.approx(1.30)
    untouched_pocket = _box_bounds(
        p.side_latch_pocket_x,
        p.side_latch_pocket_y,
        (-p.side_latch_pocket_width_z / 2, p.side_latch_pocket_width_z / 2),
    )
    assert untouched_pocket.volume == pytest.approx(2.112)
    assert _intersection(outer, untouched_pocket) < TOL
    assert 0.45 * p.side_latch_width_z == pytest.approx(2.70)
    assert 1.7 * (p.side_latch_pad_width_z - p.side_latch_pocket_width_z) == pytest.approx(6.12)


def test_latch_release_stop_and_one_side_retention_envelopes(parts) -> None:
    outer = parts[0]
    for side in (-1.0, 1.0):
        hook = make_side_latch_hook(side)
        released_hook = Location((-side * 0.55, 0, 0)) * hook
        released_pad = Location((-side * 0.40, 0, 0)) * make_side_latch_connector_pad(side)
        assert _intersection(outer, hook) < TOL
        assert _intersection(outer, released_hook) < TOL
        assert _intersection(outer, released_pad) < TOL
        engaged_pull = Location((0, -0.05, 0)) * hook
        released_pull = Location((0, -0.05, 0)) * released_hook
        assert _intersection(outer, engaged_pull) == pytest.approx(0.135, abs=1e-6)
        assert _intersection(outer, released_pull) < TOL
        pad = _box_bounds(
            (18.6, 19.6) if side > 0 else (-19.6, -18.6),
            p.side_latch_pad_y,
            (-5.0, 5.0),
        )
        pad_at_stop = Location((-side * 0.50, 0, 0)) * pad
        pad_beyond_stop = Location((-side * 0.51, 0, 0)) * pad
        assert _intersection(outer, pad_at_stop) < TOL
        assert _intersection(outer, pad_beyond_stop) > 0
    # One released side leaves one positive retention shoulder.
    assert _intersection(
        outer,
        Location((0, -0.05, 0)) * make_side_latch_hook(-1),
    ) > 0


def test_cover_clearance_and_rear_face_blind_grid(parts) -> None:
    _, inner, cover = parts
    pressed = Location((0, p.pressed_center_y, 0)) * inner
    assert _intersection(cover, pressed) < TOL
    assert p.pressed_center_y + p.inner_body_local_y[0] - p.side_latch_beam_y[1] == pytest.approx(1.35)
    rear_mid_y = (p.rear_faceplate_exterior_y + p.rear_faceplate_interior_y) / 2
    probes = []
    for x in np.arange(-19.75, 20.0, 0.5):
        for z in np.arange(-19.75, 20.0, 0.5):
            corner_dx = max(abs(x) - 16.0, 0.0)
            corner_dz = max(abs(z) - 16.0, 0.0)
            expected_inside_r4 = corner_dx**2 + corner_dz**2 <= 4.0**2
            actual_inside = cover.is_inside(Vector(x, rear_mid_y, z), tolerance=1e-7)
            probes.append((expected_inside_r4, actual_inside))
    assert len(probes) == 6400
    assert sum(expected for expected, _ in probes) == 6352
    assert sum(not expected for expected, _ in probes) == 48
    assert all(expected == actual for expected, actual in probes)


def test_c5_is_two_exact_separate_positive_single_solid_specimens() -> None:
    arm = make_c5_arm_cover_specimen()
    receiver = make_c5_housing_receiver_specimen()
    coupon = make_c5_coupon_assembly()
    assert len(coupon.children) == len(coupon.solids()) == 2
    assert {child.label for child in coupon.children} == {
        "C5_V2_side_latch_arm_cover_specimen",
        "C5_V2_side_latch_housing_receiver_specimen",
    }
    assert arm.is_valid and receiver.is_valid
    assert len(arm.solids()) == len(receiver.solids()) == 1
    assert _intersection(arm, receiver) < TOL


def test_print_exports_are_exact_three_part_layout_and_separate_c5() -> None:
    factories = (
        print_outer_housing,
        print_solid_keyboard_button,
        print_blind_two_side_latch_rear_cover,
        print_c5_arm_cover_specimen,
        print_c5_housing_receiver_specimen,
    )
    for factory in factories:
        printed = factory()
        assert printed.is_valid and len(printed.solids()) == 1
        assert printed.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    assert "cover_positive_Y_up" in print_c5_arm_cover_specimen().label
    assert "housing_positive_Y_up" in print_c5_housing_receiver_specimen().label
    bundle = make_print_bundle()
    assert len(bundle.children) == len(bundle.solids()) == 3
    assert {child.label for child in bundle.children} == {
        "outer_housing",
        "keyboard_button",
        "rear_cover",
    }
    for first, second in combinations(bundle.children, 2):
        assert _intersection(first, second) < TOL


@pytest.mark.parametrize(
    "name,factory",
    [
        ("outer", print_outer_housing),
        ("inner", print_solid_keyboard_button),
        ("cover", print_blind_two_side_latch_rear_cover),
        ("c5_arm", print_c5_arm_cover_specimen),
        ("c5_receiver", print_c5_housing_receiver_specimen),
    ],
)
def test_each_production_stl_is_one_watertight_manifold_shell(name, factory, tmp_path: Path) -> None:
    path = tmp_path / f"{name}.stl"
    export_stl(factory(), path, tolerance=0.02, angular_tolerance=0.05)
    mesh = trimesh.load_mesh(path, process=False)
    assert isinstance(mesh, trimesh.Trimesh)
    mesh.merge_vertices(digits_vertex=6, merge_tex=True, merge_norm=True)
    mesh.remove_unreferenced_vertices()
    faces = np.asarray(mesh.faces)
    canonical_faces = np.sort(faces, axis=1)
    _, face_counts = np.unique(canonical_faces, axis=0, return_counts=True)
    edges = np.sort(faces[:, [[0, 1], [1, 2], [2, 0]]].reshape((-1, 2)), axis=1)
    _, edge_counts = np.unique(edges, axis=0, return_counts=True)
    assert np.all(mesh.area_faces > 1e-18)
    assert np.all(face_counts == 1)
    assert np.all(edge_counts == 2)
    assert len(mesh.split(only_watertight=False)) == 1
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0
