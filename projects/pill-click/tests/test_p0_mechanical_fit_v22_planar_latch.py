"""Contract tests for the layer-aware V2.2 planar rear latch."""

import pytest
from build123d import Location

from pill_click.p0_mechanical_fit_v21_keyboard_identity import P0_MECHANICAL_FIT_V21
from pill_click.p0_mechanical_fit_v22_planar_latch import (
    P0_MECHANICAL_FIT_V22,
    make_keyboard_identity_button,
    make_deflected_planar_latch_lock,
    make_outer_housing,
    make_planar_latch_hook,
    make_planar_latch_lock,
    make_planar_latch_rear_cover,
    make_planar_latch_stop,
    make_pressed_planar_latch_assembly,
    make_released_planar_latch_assembly,
    placed_keyboard_identity_button,
)


p = P0_MECHANICAL_FIT_V22


def _intersection_volume(first, second) -> float:
    intersection = first & second
    return 0.0 if intersection is None else intersection.volume


def _bbox(shape):
    box = shape.bounding_box()
    return (box.min.X, box.max.X, box.min.Y, box.max.Y, box.min.Z, box.max.Z)


def test_v2_rails_stops_keyboard_and_13_4_mm_travel_are_frozen() -> None:
    old = P0_MECHANICAL_FIT_V21
    assert p.male_rail_centres_z == old.male_rail_centres_z
    assert p.male_rail_width_z == old.male_rail_width_z
    assert p.male_rail_external_height_x == old.male_rail_external_height_x
    assert p.male_rail_local_y == old.male_rail_local_y
    assert p.female_channel_blind_front_y == old.female_channel_blind_front_y
    assert p.key_local_y == old.key_local_y
    assert p.key_face_size_xz == old.key_face_size_xz
    assert p.released_state - p.pressed_state == pytest.approx(13.4)


def test_keyboard_flare_reaches_housing_edge_with_printable_bezel() -> None:
    assert p.key_skirt_size_xz == pytest.approx(37.60)
    assert p.key_skirt_size_xz - p.key_face_size_xz == pytest.approx(8.60)
    assert (p.housing_size - p.front_guide_size_xz) / 2 == pytest.approx(1.00)
    assert (p.front_guide_size_xz - p.key_skirt_size_xz) / 2 == pytest.approx(0.20)


def test_0_4_mm_nozzle_features_use_robust_extrusion_multiples() -> None:
    assert p.rear_faceplate_thickness_y / p.nozzle_diameter == pytest.approx(6.0)
    assert p.planar_latch_beam_thickness_x / p.nozzle_diameter == pytest.approx(3.0)
    assert p.planar_latch_inner_slot_width_x / p.nozzle_diameter == pytest.approx(3.0)
    assert p.planar_latch_tower_thickness_x / p.nozzle_diameter == pytest.approx(6.0)
    assert p.planar_latch_tower_width_z / p.nozzle_diameter == pytest.approx(25.0)
    assert p.planar_latch_paddle_projection_x / p.nozzle_diameter == pytest.approx(6.0)
    assert (
        p.planar_latch_hook_front_base_y - p.planar_latch_hook_rear_base_y
    ) / p.nozzle_diameter == pytest.approx(4.0)


def test_planar_flexure_strain_and_release_math_have_margin() -> None:
    assert p.planar_latch_beam_effective_length_z == pytest.approx(13.5)
    assert p.planar_latch_strain(p.planar_latch_release_travel_x) < 0.015
    assert p.planar_latch_strain(p.planar_latch_hard_stop_travel_x) < 0.020
    assert p.planar_latch_actual_stop_travel_x == pytest.approx(
        p.planar_latch_hard_stop_travel_x
    )
    assert p.planar_latch_hook_engagement_x == pytest.approx(0.60)
    assert p.planar_latch_released_hook_clearance_x == pytest.approx(0.10)
    assert p.planar_latch_outer_skin_x == pytest.approx(1.20)
    assert p.planar_latch_axial_seating_clearance_y == pytest.approx(0.20)
    assert p.planar_latch_retention_wall_y == pytest.approx(0.40)


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_physical_stop_surface_matches_hard_stop_math(side: float) -> None:
    stop = make_planar_latch_stop(side)
    stop_box = stop.bounding_box()
    surface_x = stop_box.min.X if side < 0 else stop_box.max.X
    expected_surface_x = -p.planar_latch_stop_surface_x if side < 0 else p.planar_latch_stop_surface_x
    assert surface_x == pytest.approx(expected_surface_x)
    paddle_inner_x = -p.planar_latch_paddle_x[0] if side < 0 else p.planar_latch_paddle_x[0]
    assert abs(paddle_inner_x - surface_x) == pytest.approx(
        p.planar_latch_hard_stop_travel_x
    )


def test_cover_and_housing_are_single_valid_solids() -> None:
    cover = make_planar_latch_rear_cover()
    housing = make_outer_housing()
    assert cover.is_valid and len(cover.solids()) == 1 and cover.volume > 0
    assert housing.is_valid and len(housing.solids()) == 1 and housing.volume > 0
    assert _bbox(cover) == pytest.approx((-22.4, 22.4, -21.1, -15.9, -20.0, 20.0), abs=0.01)


def test_hooks_are_large_valid_printable_solids() -> None:
    for side in (-1.0, 1.0):
        hook = make_planar_latch_hook(side)
        assert hook.is_valid and len(hook.solids()) == 1 and hook.volume > 0
        assert hook.bounding_box().size.Z == pytest.approx(10.0)
        assert hook.bounding_box().size.X >= 1.1
        assert hook.bounding_box().size.Y == pytest.approx(1.6)


@pytest.mark.parametrize("side", (-1.0, 1.0))
@pytest.mark.parametrize("travel", (0.0, p.planar_latch_release_travel_x, p.planar_latch_hard_stop_travel_x))
def test_flexed_lock_envelope_clears_receiver(side: float, travel: float) -> None:
    assert _intersection_volume(
        make_outer_housing(), make_deflected_planar_latch_lock(side, travel)
    ) < 1e-6


@pytest.mark.parametrize("side", (-1.0, 1.0))
@pytest.mark.parametrize("axial_offset", (-2.0, -1.0, -0.5, 0.0))
def test_squeezed_lock_has_collision_free_insertion_path(
    side: float, axial_offset: float
) -> None:
    assert _intersection_volume(
        make_outer_housing(),
        make_deflected_planar_latch_lock(
            side, p.planar_latch_release_travel_x, axial_offset
        ),
    ) < 1e-6


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_unsqueezed_hook_is_axially_retained_by_receiver_wall(side: float) -> None:
    rearward_probe = Location((0.0, -0.30, 0.0)) * make_planar_latch_hook(side)
    assert _intersection_volume(make_outer_housing(), rearward_probe) > 0.01
    assert make_planar_latch_lock(side).is_valid


@pytest.mark.parametrize(
    "state",
    (p.inward_state, p.pressed_state, 6.0, p.released_state, p.maximum_pull_state),
)
def test_inner_remains_collision_free_for_entire_accepted_travel(state: float) -> None:
    moving = placed_keyboard_identity_button(state)
    assert _intersection_volume(make_outer_housing(), moving) < 1e-6
    assert _intersection_volume(make_planar_latch_rear_cover(), moving) < 1e-6


def test_pressed_and_released_assemblies_preserve_three_parts_and_stroke() -> None:
    pressed = make_pressed_planar_latch_assembly()
    released = make_released_planar_latch_assembly()
    assert len(pressed.children) == len(pressed.solids()) == 3
    assert len(released.children) == len(released.solids()) == 3
    assert released.bounding_box().max.Y - pressed.bounding_box().max.Y == pytest.approx(13.4)
    assert _intersection_volume(make_outer_housing(), make_planar_latch_rear_cover()) < 1e-6
    assert make_keyboard_identity_button().is_valid
