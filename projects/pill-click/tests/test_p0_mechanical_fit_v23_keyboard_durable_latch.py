"""Contract tests for the V2.3 keyboard silhouette and durable latch."""

from dataclasses import replace

import pytest
from build123d import Location, Vector

from pill_click.p0_mechanical_fit_v2_keyboard_inverted_rails import P0_MECHANICAL_FIT_V2
from pill_click.p0_mechanical_fit_v23_keyboard_durable_latch import (
    P0_MECHANICAL_FIT_V23,
    make_deflected_planar_latch_lock,
    make_keyboard_button,
    make_keyboard_keycap,
    make_outer_housing,
    make_planar_latch_hook,
    make_planar_latch_lock,
    make_planar_latch_rear_cover,
    make_planar_latch_stop,
    make_pressed_assembly,
    make_rear_rail_stop_bosses,
    make_released_assembly,
    placed_keyboard_button,
)


p = P0_MECHANICAL_FIT_V23


def _intersection_volume(first, second) -> float:
    intersection = first & second
    return 0.0 if intersection is None else intersection.volume


def test_accepted_rail_cross_sections_and_front_stops_are_frozen() -> None:
    old = P0_MECHANICAL_FIT_V2
    assert p.male_rail_centres_z == old.male_rail_centres_z
    assert p.male_rail_width_z == old.male_rail_width_z
    assert p.male_rail_external_height_x == old.male_rail_external_height_x
    assert p.male_rail_local_y[0] == pytest.approx(-21.6)
    assert p.male_rail_local_y[1] == old.male_rail_local_y[1]
    assert p.male_rail_source_embed_x == old.male_rail_source_embed_x
    assert p.spine_inner_x == old.spine_inner_x
    assert p.spine_local_y[0] == pytest.approx(-21.6)
    assert p.spine_local_y[1] == old.spine_local_y[1]
    assert p.female_channel_blind_front_y == old.female_channel_blind_front_y
    assert p.blind_stop_wall_axial_thickness == old.blind_stop_wall_axial_thickness


def test_true_keyboard_contract_and_exact_travel() -> None:
    assert p.inner_body_local_y == (-20.8, 1.5)
    assert p.inner_body_length_y == pytest.approx(22.3)
    assert p.inner_body_rear_to_rail_rear_gap_y == pytest.approx(0.8)
    assert p.inner_body_rear_to_rail_rear_gap_y / p.nozzle_diameter == pytest.approx(2.0)
    assert p.key_local_y == (1.5, 20.5)
    assert p.key_skirt_size_xz == pytest.approx(34.2)
    assert p.key_face_size_xz == pytest.approx(27.5)
    assert p.front_guide_size_xz == pytest.approx(35.2)
    assert p.front_bezel_chamfer == pytest.approx(1.0)
    assert p.key_face_edge_fillet_y == pytest.approx(0.9)
    assert p.key_face_dish_depth_y == pytest.approx(0.0)
    assert p.key_face_dish_radius_xz == pytest.approx(12.25)
    assert p.working_travel_y == pytest.approx(10.0)
    assert p.pressed_state == pytest.approx(3.4)
    assert p.inward_state == pytest.approx(3.4)
    assert p.pressed_face_world_y == pytest.approx(28.4)
    assert p.released_face_world_y == pytest.approx(38.4)
    assert p.pressed_key_proud_y == pytest.approx(8.4)
    assert p.released_key_proud_y == pytest.approx(18.4)
    assert p.key_seam_hidden_at_max_pull_y >= 0.45 - 1e-9


def test_boolean_kernel_allowances_are_named_contract_values() -> None:
    assert p.housing_guide_boolean_overshoot_y == pytest.approx(0.20)
    assert p.female_channel_boolean_overshoot_y == pytest.approx(0.01)
    assert p.rear_cover_boolean_overshoot_y == pytest.approx(0.10)


def test_keycap_silhouette_is_one_monotonic_continuous_loft() -> None:
    samples = [p.key_local_y[0] + index * 0.5 for index in range(39)]
    assert samples[-1] == pytest.approx(p.key_local_y[1])
    sizes = [p.key_section_size_xz(y) for y in samples]
    assert sizes[0] == pytest.approx(34.2)
    assert sizes[-1] == pytest.approx(27.5)
    assert all(later < earlier for earlier, later in zip(sizes, sizes[1:]))
    keycap = make_keyboard_keycap()
    assert keycap.is_valid and len(keycap.solids()) == 1
    assert keycap.bounding_box().size.Y == pytest.approx(19.0, abs=1e-5)


def test_key_face_is_flat_by_default_and_dish_remains_parametric() -> None:
    flat = make_keyboard_keycap()
    dished = make_keyboard_keycap(replace(p, key_face_dish_depth_y=0.55))
    face_center = Vector(0.0, p.key_local_y[1] - 0.05, 0.0)
    assert flat.is_valid and flat.is_inside(face_center)
    assert dished.is_valid and not dished.is_inside(face_center)
    assert dished.volume < flat.volume


def test_latch_dimensions_are_nozzle_and_layer_robust() -> None:
    assert p.planar_latch_stop_rail_x == (13.8, 15.0)
    assert p.planar_latch_inner_slot_x == (15.0, 16.2)
    assert p.planar_latch_inner_slot_width_x == pytest.approx(1.2)
    assert p.planar_latch_beam_x == (18.0, 20.0)
    assert p.planar_latch_beam_thickness_x == pytest.approx(2.0)
    assert p.planar_latch_beam_thickness_x / p.nozzle_diameter == pytest.approx(5.0)
    assert p.planar_latch_beam_x[1] == pytest.approx(p.half_housing)
    assert p.planar_latch_outer_slot_x == (16.0, 18.0)
    assert p.planar_latch_outer_slot_x[1] == pytest.approx(p.planar_latch_beam_x[0])
    assert p.planar_latch_slot_overlap_x >= p.planar_latch_slot_corner_radius
    assert p.planar_latch_upper_outer_slot_z == (5.0, 18.0)
    assert p.planar_latch_lower_outer_slot_z == (-18.0, -5.0)
    assert p.planar_latch_inner_slot_z == (-18.0, 18.0)
    assert p.planar_latch_pilot_relief_x[0] == pytest.approx(
        p.planar_latch_stop_rail_x[0]
    )
    assert p.planar_latch_pilot_relief_z == (-18.1, 18.1)
    assert p.planar_latch_beam_effective_length_z == pytest.approx(13.0)
    assert p.planar_latch_rounded_anchor_bridge_z == pytest.approx(1.464101615)
    assert p.planar_latch_rounded_anchor_bridge_z / p.nozzle_diameter > 3.5
    assert p.planar_latch_strain(p.planar_latch_release_travel_x) == pytest.approx(
        0.0319526627
    )
    assert p.planar_latch_tower_thickness_x == pytest.approx(2.0)
    assert p.planar_latch_tower_thickness_x / p.nozzle_diameter == pytest.approx(5.0)
    assert p.planar_latch_tower_passage_clearance_x == pytest.approx(0.2)
    assert p.planar_latch_tower_width_z == pytest.approx(10.0)
    assert p.planar_latch_hook_axial_plateau_y == pytest.approx(1.2)
    assert p.planar_latch_hook_axial_plateau_y / p.nominal_layer_height == pytest.approx(6.0)
    assert p.planar_latch_hook_axial_length_y == pytest.approx(3.6)
    assert p.planar_latch_hook_engagement_x == pytest.approx(0.8)
    assert p.planar_latch_paddle_projection_x == pytest.approx(0.0)
    assert p.planar_latch_paddle_z[1] - p.planar_latch_paddle_z[0] >= 10.0
    assert p.planar_latch_outer_skin_x == pytest.approx(1.2)
    assert p.planar_latch_axial_seating_clearance_y == pytest.approx(0.1)
    assert p.planar_latch_axial_front_clearance_y == pytest.approx(0.2)
    assert p.planar_latch_retention_wall_y == pytest.approx(1.5)


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_thick_hook_is_a_valid_full_height_solid(side: float) -> None:
    hook = make_planar_latch_hook(side)
    box = hook.bounding_box()
    assert hook.is_valid and len(hook.solids()) == 1 and hook.volume > 0
    assert box.size.X == pytest.approx(1.6)
    assert box.size.Y == pytest.approx(3.6)
    assert box.size.Z == pytest.approx(10.0)


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_real_hard_stop_geometry_matches_1_2_mm_limit(side: float) -> None:
    stop = make_planar_latch_stop(side)
    box = stop.bounding_box()
    stop_surface = box.min.X if side < 0 else box.max.X
    paddle_inner = -p.planar_latch_paddle_x[0] if side < 0 else p.planar_latch_paddle_x[0]
    assert abs(paddle_inner - stop_surface) == pytest.approx(1.2)
    assert p.planar_latch_actual_stop_travel_x == pytest.approx(1.2)
    assert p.planar_latch_release_travel_x == pytest.approx(0.9)
    assert p.planar_latch_released_hook_clearance_x == pytest.approx(0.1)
    assert box.size.Z == pytest.approx(36.0)

    released_lock = make_deflected_planar_latch_lock(
        side, p.planar_latch_release_travel_x
    )
    stopped_lock = make_deflected_planar_latch_lock(
        side, p.planar_latch_hard_stop_travel_x
    )
    assert _intersection_volume(stop, released_lock) < 1e-9
    assert _intersection_volume(stop, stopped_lock) < 1e-9
    released_box = released_lock.bounding_box()
    stopped_box = stopped_lock.bounding_box()
    if side > 0:
        assert released_box.min.X - box.max.X == pytest.approx(0.3)
        assert stopped_box.min.X - box.max.X == pytest.approx(0.0, abs=2e-7)
    else:
        assert box.min.X - released_box.max.X == pytest.approx(0.3)
        assert box.min.X - stopped_box.max.X == pytest.approx(0.0, abs=2e-7)

    # A further 0.01 mm would penetrate the rail, proving this actual solid is
    # the limiting contact rather than a documentation-only dimension.
    beyond_stop = Location((-side * 1.21, 0.0, 0.0)) * make_planar_latch_lock(side)
    assert _intersection_volume(stop, beyond_stop) > 0.0


def test_parts_and_assemblies_are_valid_solids() -> None:
    button = make_keyboard_button()
    housing = make_outer_housing()
    cover = make_planar_latch_rear_cover()
    for part in (button, housing, cover):
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0
    for assembly in (make_pressed_assembly(), make_released_assembly()):
        assert len(assembly.children) == len(assembly.solids()) == 3
        assert all(solid.is_valid for solid in assembly.solids())


def test_four_rear_rail_bosses_create_the_inward_stop_plane() -> None:
    bosses = make_rear_rail_stop_bosses()
    box = bosses.bounding_box()
    assert bosses.is_valid and len(bosses.solids()) == p.rear_stop_boss_count == 4
    assert p.rear_stop_boss_width_x == pytest.approx(1.0)
    assert p.rear_stop_boss_width_x / p.nozzle_diameter == pytest.approx(2.5)
    assert p.rear_stop_boss_length_y == pytest.approx(5.0)
    assert p.rear_stop_contact_area_total == pytest.approx(8.8)
    assert box.min.Y == pytest.approx(p.rear_faceplate_interior_y)
    assert box.max.Y == pytest.approx(p.rear_stop_boss_contact_plane_y)
    assert p.inward_stop_gap_y(3.40) == pytest.approx(0.0, abs=2e-9)
    assert p.inward_stop_gap_y(3.41) == pytest.approx(0.01)
    assert p.inward_stop_gap_y(3.39) == pytest.approx(-0.01)
    assert _intersection_volume(bosses, placed_keyboard_button(3.40)) < 1e-9
    assert _intersection_volume(bosses, placed_keyboard_button(3.41)) < 1e-9
    assert _intersection_volume(bosses, placed_keyboard_button(3.39)) > 0.0


def test_release_paddles_are_flush_with_the_40_mm_cover_envelope() -> None:
    cover = make_planar_latch_rear_cover()
    box = cover.bounding_box()
    assert box.min.X == pytest.approx(-p.half_housing, abs=1e-6)
    assert box.max.X == pytest.approx(p.half_housing, abs=1e-6)
    assert box.size.X == pytest.approx(p.housing_size, abs=1e-6)
    assert box.size.Z == pytest.approx(p.housing_size, abs=1e-6)
    assert p.planar_latch_paddle_z == (-5.0, 5.0)


def test_rear_pilot_matches_the_outer_housing_cavity_profile() -> None:
    assert p.rear_pilot_size_xz == pytest.approx(34.2)
    assert p.main_guide_size_xz == pytest.approx(34.6)
    assert (p.main_guide_size_xz - p.rear_pilot_size_xz) / 2 == pytest.approx(0.2)
    assert p.rear_pilot_corner_radius_xz == pytest.approx(3.0)
    assert p.main_guide_corner_radius_xz == pytest.approx(3.2)
    assert (
        p.main_guide_corner_radius_xz - p.rear_pilot_corner_radius_xz
    ) == pytest.approx(0.2)
    assert p.rear_pilot_depth_y == pytest.approx(3.2)
    assert p.rear_pilot_depth_y / p.nozzle_diameter == pytest.approx(8.0)
    assert p.rear_pilot_straight_depth_y == pytest.approx(2.8)
    assert p.rear_pilot_entry_chamfer_length_y == pytest.approx(0.4)
    assert p.rear_pilot_entry_chamfer_length_y / p.nozzle_diameter == pytest.approx(1.0)
    assert p.rear_pilot_entry_chamfer_radial_xz == pytest.approx(0.4)
    assert p.rear_pilot_entry_chamfer_angle_degrees == pytest.approx(45.0)
    assert p.rear_pilot_tip_size_xz == pytest.approx(33.4)
    assert p.rear_pilot_tip_corner_radius_xz == pytest.approx(2.6)
    assert p.rear_faceplate_interior_y == pytest.approx(p.housing_rear_y)


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_flexure_slot_has_rounded_caps_and_no_isolated_ledge(side: float) -> None:
    cover = make_planar_latch_rear_cover()
    y = (p.rear_faceplate_exterior_y + p.rear_faceplate_interior_y) / 2
    # The union stays open from the central slot through both branches.
    for magnitude_x in (15.2, 16.1, 17.0, 17.7):
        assert not cover.is_inside(Vector(side * magnitude_x, y, 17.6))
        assert not cover.is_inside(Vector(side * magnitude_x, y, -17.6))
    # R0.50 terminal caps: centre points are open, extreme corners remain
    # solid, and material resumes immediately beyond Z=+/-18.00.
    assert not cover.is_inside(Vector(side * 16.5, y, 17.9))
    assert not cover.is_inside(Vector(side * 16.5, y, -17.9))
    assert cover.is_inside(Vector(side * 17.9, y, 17.9))
    assert cover.is_inside(Vector(side * 17.9, y, -17.9))
    assert cover.is_inside(Vector(side * 16.5, y, 18.1))
    assert cover.is_inside(Vector(side * 16.5, y, -18.1))


def test_button_collision_sweep_is_clear_every_0_1_mm() -> None:
    housing = make_outer_housing()
    cover = make_planar_latch_rear_cover()
    for step in range(34, 136):
        state = step / 10
        button = placed_keyboard_button(state)
        assert _intersection_volume(housing, button) < 1e-6
        assert _intersection_volume(cover, button) < 1e-6
    button = placed_keyboard_button(p.maximum_pull_state)
    assert _intersection_volume(housing, button) < 1e-6
    assert _intersection_volume(cover, button) < 1e-6


def test_rear_feed_sweep_is_clear_at_named_half_mm_steps() -> None:
    housing = make_outer_housing()
    button = make_keyboard_button()
    center_y = p.feed_start_center_y
    while center_y <= p.feed_end_center_y + 1e-9:
        placed = Location((0.0, center_y, 0.0)) * button
        assert _intersection_volume(housing, placed) < 1e-6
        center_y += p.feed_step
    placed = Location((0.0, p.feed_end_center_y, 0.0)) * button
    assert _intersection_volume(housing, placed) < 1e-6


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_latch_deflection_sweep_is_clear_every_0_1_mm(side: float) -> None:
    housing = make_outer_housing()
    for step in range(0, 13):
        travel = step / 10
        lock = make_deflected_planar_latch_lock(side, travel)
        assert _intersection_volume(housing, lock) < 1e-6


@pytest.mark.parametrize("side", (-1.0, 1.0))
def test_release_insertion_and_retention_envelopes(side: float) -> None:
    housing = make_outer_housing()
    for step in range(-40, 1):
        offset = step / 10
        squeezed = make_deflected_planar_latch_lock(
            side, p.planar_latch_release_travel_x, offset
        )
        assert _intersection_volume(housing, squeezed) < 1e-6
    retained = Location((0.0, -0.11, 0.0)) * make_planar_latch_hook(side)
    assert _intersection_volume(housing, retained) > 0.01


def test_tightened_retention_begins_after_0_1_mm_axial_clearance() -> None:
    housing = make_outer_housing()
    cover = make_planar_latch_rear_cover()
    assert _intersection_volume(housing, cover) < 1e-6
    assert _intersection_volume(housing, Location((0.0, -0.10, 0.0)) * cover) < 1e-6
    assert _intersection_volume(housing, Location((0.0, -0.11, 0.0)) * cover) > 0.01


def test_assembly_stroke_and_static_interfaces() -> None:
    pressed = make_pressed_assembly()
    released = make_released_assembly()
    assert released.bounding_box().max.Y - pressed.bounding_box().max.Y == pytest.approx(10.0)
    assert pressed.bounding_box().max.Y == pytest.approx(p.pressed_face_world_y)
    assert released.bounding_box().max.Y == pytest.approx(p.released_face_world_y)
    assert _intersection_volume(make_outer_housing(), make_planar_latch_rear_cover()) < 1e-6
