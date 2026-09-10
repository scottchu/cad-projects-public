"""Focused executable contract for the three-part integrated P1 dispenser."""

from dataclasses import replace

from build123d import Location, Vector
import pytest

from pill_click.p0_mechanical_fit_v23_keyboard_durable_latch.geometry import make_rear_rail_stop_bosses
from pill_click.p1_hollow_magnetic_dispenser import (
    P1_HOLLOW_MAGNETIC_DISPENSER as p,
    make_cover_m1_bore_tools, make_cover_m1_pick_bore_tools,
    make_cover_m2_bore_tools, make_cover_m2_pick_bore_tools, make_cover_magnet_bosses,
    make_hollow_keyboard_container, make_hopper_void, make_inner_magnet_pick_bore_tools,
    make_inner_magnet_pocket_tools, make_inner_port_tool,
    make_magnetic_rear_cover, make_outer_port_tool, make_ported_outer_housing,
    make_pressed_assembly, make_print_bundle, make_released_assembly,
    placed_hollow_keyboard_container,
)


def _intersection_volume(first, second):
    intersection = first & second
    return 0.0 if intersection is None else intersection.volume


def test_three_connected_manufactured_parts_with_integrated_inner_magnets():
    parts = (make_ported_outer_housing(), make_hollow_keyboard_container(), make_magnetic_rear_cover())
    assert len(make_print_bundle().children) == 3
    for part in parts:
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0
    assert p.standard_shell_thickness == pytest.approx(1.2)
    assert p.key_face_membrane_y == pytest.approx(0.8)
    assert p.inner_magnet_medicine_barrier_y == pytest.approx(2.7)
    assert p.minimum_internal_radius >= 1.2


def test_inner_is_one_piece_with_integrated_rear_wall_and_magnet_insets():
    body = make_hollow_keyboard_container()
    assert "one_piece" in body.label and "integrated_magnet_insets" in body.label
    assert body.bounding_box().min.Y == pytest.approx(p.inner_body_local_y[0])
    assert len(body.solids()) == 1
    for assembly in (make_pressed_assembly(), make_released_assembly()):
        assert len(assembly.children) == 3 and len(assembly.solids()) == 3


def test_literal_double_area_port_and_opaque_released_geometry_without_fin():
    assert (p.pill_port_width_x, p.pill_port_length_y, p.pill_port_corner_radius_xy) == pytest.approx((31.8, 9.3, 2.5))
    assert p.port_area_gain_ratio >= 1.70 and p.working_travel_y == pytest.approx(10.8)
    assert p.port_side_wall_thickness_x == pytest.approx(p.standard_shell_thickness)
    assert p.outer_port_rearward_bias_y == pytest.approx(2.5)
    assert p.pressed_port_overlap_y == pytest.approx(6.8)
    assert p.pressed_port_overlap_y >= p.minimum_pressed_port_overlap_y
    assert p.outer_port_length_y == pytest.approx(6.8)
    assert p.released_port_separation_y == pytest.approx(4.0)
    assert p.released_port_separation_y >= p.released_seal_safety_inset
    assert make_outer_port_tool().bounding_box().size.X == pytest.approx(31.8)
    # The seal contract is checked at the actual mechanical pull stop, not
    # merely at a named preview pose.
    assert p.maximum_pull_state == pytest.approx(p.released_state)
    assert p.released_endplay == pytest.approx(0.0)
    # Use the worst-case vertical-sag pose, not only the perfect rail stop.
    released_body = placed_hollow_keyboard_container(p.sagged_released_state)
    outer_port = make_outer_port_tool()
    housing = make_ported_outer_housing()
    # The openings are disjoint at release.
    assert p.inner_port_world_y(p.released_state)[0] - p.outer_port_world_y[1] == pytest.approx(4.0)
    # More importantly, the complete moving opening remains behind the outer
    # housing rather than travelling beyond its front edge.
    assert p.released_inner_port_front_cover_y == pytest.approx(1.5)
    assert p.released_outer_port_rear_cover_y == pytest.approx(0.5)

    # Looking through the complete fixed aperture must hit the normal flat
    # rear surface of the inner body, including the rounded edge bands.
    for x_index in range(71):
        sample_x = -p.pill_port_width_x / 2 + 0.01 + x_index * ((p.pill_port_width_x - 0.02) / 70)
        for y_index in range(41):
            sample_y = p.outer_port_world_y[0] + 0.01 + y_index * ((p.outer_port_length_y - 0.02) / 40)
            if outer_port.is_inside(Vector(sample_x, sample_y, -18.55)):
                assert released_body.is_inside(Vector(sample_x, sample_y, -16.25))

    # Looking through the complete moving opening must hit solid outer floor.
    released_inner_y = p.inner_port_world_y(p.sagged_released_state)
    released_inner_port = make_inner_port_tool().moved(Location((0, p.inner_center_y(p.sagged_released_state), 0)))
    for x_index in range(71):
        sample_x = -p.pill_port_width_x / 2 + 0.01 + x_index * ((p.pill_port_width_x - 0.02) / 70)
        for y_index in range(41):
            sample_y = released_inner_y[0] + 0.01 + y_index * ((p.pill_port_length_y - 0.02) / 40)
            if released_inner_port.is_inside(Vector(sample_x, sample_y, -18.55)):
                assert housing.is_inside(Vector(sample_x, sample_y, -18.55))


def test_released_seal_regression_catches_old_print_and_covers_oblique_view():
    # The photo came from this earlier 10.30 mm port.  Its nominal 0.50 mm
    # edge-only separation disappears entirely when the printed shuttle stops
    # just 0.50 mm before the ideal rail coordinate, so it must fail the new
    # operating-state contract.
    old_print = replace(
        p,
        hopper_front_throat_y=0.80,
        pill_port_length_y=10.30,
        inner_port_local_y=(-9.50, 0.80),
        outer_port_rearward_bias_y=0.0,
        released_vertical_sag_envelope_y=0.50,
    )
    assert old_print.released_port_separation_y == pytest.approx(0.50)
    assert old_print.released_operating_port_separation_y == pytest.approx(0.0)
    assert old_print.released_no_peek_margin_y < 0.0

    # The corrected geometry is fully separated before the released rail stop and
    # retains positive coverage for an 8-degree look through the complete
    # 5.90 mm stacked port depth.
    assert p.sagged_released_state == pytest.approx(11.20)
    assert p.sagged_port_separation_y == pytest.approx(1.0)
    assert p.sagged_port_separation_y >= p.minimum_sagged_seal_separation_y
    assert p.released_view_depth_z == pytest.approx(5.90)
    assert p.sagged_no_peek_offset_y == pytest.approx(0.829, abs=0.001)
    assert p.sagged_no_peek_margin_y >= p.minimum_sagged_no_peek_margin_y


def test_dense_full_motion_without_rear_cover_hard_stops():
    body, housing, cover = make_hollow_keyboard_container(), make_ported_outer_housing(), make_magnetic_rear_cover()
    assert p.motion_sweep_step_y <= p.motion_sweep_max_step_y
    for index in range(p.motion_sweep_sample_count):
        state = p.pressed_state + index * p.motion_sweep_step_y
        assert _intersection_volume(Location((0, p.inner_center_y(state), 0)) * body, housing) < 1e-7
        assert _intersection_volume(Location((0, p.inner_center_y(state), 0)) * body, cover) < 1e-7
    assert p.magnet_face_separation_y(p.pressed_state) == pytest.approx(1.4)
    assert p.magnet_face_separation_y(p.released_state) == pytest.approx(12.2)


def test_existing_rear_cover_latch_is_tighter_but_still_two_finger_releasable():
    assert p.rear_pilot_clearance_per_side_xz == pytest.approx(0.15)
    assert p.rear_pilot_entry_chamfer_radial_xz == pytest.approx(0.40)
    assert p.planar_latch_beam_thickness_x == pytest.approx(2.0)
    assert p.planar_latch_hook_engagement_x == pytest.approx(0.90)
    assert p.planar_latch_release_travel_x >= p.planar_latch_hook_engagement_x
    assert p.planar_latch_hard_stop_travel_x > p.planar_latch_release_travel_x


def test_flush_rails_and_rear_cover_have_no_hard_stop_geometry():
    assert p.male_rail_local_y[0] == pytest.approx(p.inner_body_local_y[0])
    assert p.spine_local_y[0] == pytest.approx(p.inner_body_local_y[0])
    # The female groove stays one constant section at its rear entrance;
    # there is no redundant larger assembly-mouth inset around it.
    assert p.female_mouth_extra_width_z == pytest.approx(0.0)
    assert p.female_mouth_extra_depth_x == pytest.approx(0.0)
    assert p.female_mouth_x == pytest.approx(p.female_channel_x)
    assert p.released_endplay == pytest.approx(0.0)
    cover = make_magnetic_rear_cover()
    assert _intersection_volume(cover, make_rear_rail_stop_bosses(p)) < 1e-7
    bosses = make_cover_magnet_bosses()
    assert len(bosses.solids()) == 2
    assert bosses.bounding_box().max.Y == pytest.approx(-14.3)
    assert p.inner_center_y(p.pressed_state) + p.inner_body_local_y[0] == pytest.approx(-12.9)
    assert p.magnet_face_separation_y(p.pressed_state) == pytest.approx(1.4)
    # Regression samples through the exact two former long stop bars.  These
    # points must stay empty: only the two circular rebound bosses may project
    # toward the inner container.
    for z in (-12.0, 12.0):
        assert not cover.is_inside(Vector(0.0, -13.0, z))


def test_exact_coaxial_one_magnet_seats_web_and_polarity():
    assert p.return_magnet_centres_x == (-8.5, 8.5) and p.return_magnet_center_z == pytest.approx(0.0)
    assert p.inner_magnet_pocket_y == pytest.approx((-20.8, -18.7))
    assert p.cover_m1_seat_y == pytest.approx((-21.1, -19.0))
    assert p.cover_m2_seat_y == pytest.approx((-16.4, -14.3))
    assert p.cover_magnet_web_thickness_y == pytest.approx(2.6)
    assert p.cavity_rear_y - p.inner_magnet_pocket_y[1] == pytest.approx(2.7)
    assert _intersection_volume(make_inner_magnet_pocket_tools(), make_hopper_void()) < 1e-7
    assert p.magnet_pocket_diameter == pytest.approx(6.1)
    assert p.inner_magnet_seat_depth_y == pytest.approx(2.1)
    assert p.cover_m1_depth_y == pytest.approx(2.1) and p.cover_m2_depth_y == pytest.approx(2.1)
    assert p.inner_magnet_count == 2 and p.rear_cover_magnet_count == 4
    assert len(make_inner_magnet_pocket_tools().solids()) == 2
    assert len(make_cover_m1_bore_tools().solids()) == 2 and len(make_cover_m2_bore_tools().solids()) == 2
    assert p.m1_m2_attract and p.m2_inner_repel

    # The full visible return recess is exactly the 2.10 mm M2 seat.  There is
    # no continuation toward the rear plate that can accept a second magnet.
    cover = make_magnetic_rear_cover()
    for x in p.return_magnet_centres_x:
        assert not cover.is_inside(Vector(x, -14.31, p.return_magnet_center_z))
        assert not cover.is_inside(Vector(x, -16.39, p.return_magnet_center_z))
        assert cover.is_inside(Vector(x, -16.41, p.return_magnet_center_z))
        assert cover.is_inside(Vector(x, -14.29, p.return_magnet_center_z)) is False

    # The fridge-facing M1 recess is likewise exactly one 2.10 mm seat.  Its
    # front wall is solid, so a second magnet cannot stack inside the plate.
    for x in p.return_magnet_centres_x:
        assert not cover.is_inside(Vector(x, -21.09, p.return_magnet_center_z))
        assert not cover.is_inside(Vector(x, -19.01, p.return_magnet_center_z))
        assert cover.is_inside(Vector(x, -18.99, p.return_magnet_center_z))


def test_six_same_face_pick_bores_are_small_depth_limited_and_parametric():
    assert p.magnet_pick_bore_diameter == pytest.approx(1.4)
    assert p.magnet_pick_bore_overlap_x == pytest.approx(0.2)
    assert p.magnet_pick_bore_extra_depth_y == pytest.approx(0.5)
    assert p.magnet_pick_bore_offset_x == pytest.approx(3.55)
    assert p.magnet_pick_bore_centres_x == pytest.approx((-12.05, 12.05))
    assert p.inner_magnet_pick_bore_y == pytest.approx((-20.8, -18.2))
    assert p.cover_m1_pick_bore_y == pytest.approx((-21.1, -18.5))
    assert p.cover_m2_pick_bore_y == pytest.approx((-16.9, -14.3))
    assert p.magnet_pick_bore_depth_y == pytest.approx(2.6)

    # The 0.20 mm radial overlap opens each pick bore into the corresponding
    # seat, while the 1.40 mm diameter cannot accept another 6 mm magnet.
    seat_radius = p.magnet_pocket_diameter / 2
    pick_radius = p.magnet_pick_bore_diameter / 2
    assert seat_radius + pick_radius - p.magnet_pick_bore_offset_x == pytest.approx(0.2)
    assert p.magnet_pick_bore_diameter < p.magnet_nominal_diameter / 4

    inner_tools = make_inner_magnet_pick_bore_tools()
    m1_tools = make_cover_m1_pick_bore_tools()
    m2_tools = make_cover_m2_pick_bore_tools()
    assert sum(len(tools.solids()) for tools in (inner_tools, m1_tools, m2_tools)) == 6
    for tools in (inner_tools, m1_tools, m2_tools):
        assert tools.is_valid
        assert tools.bounding_box().size.X == pytest.approx(25.5)
        assert tools.bounding_box().size.Z == pytest.approx(1.4)

    # Every cutter remains safely buried after its 0.50 mm under-edge reach:
    # no medicine-cavity breakthrough and no M1-to-M2 through tunnel.
    assert p.inner_pick_medicine_barrier_y == pytest.approx(2.2)
    assert p.cover_pick_web_thickness_y == pytest.approx(1.6)
    assert p.inner_pick_medicine_barrier_y >= 5 * p.nozzle_diameter
    assert p.cover_pick_web_thickness_y >= 4 * p.nozzle_diameter
    assert p.magnet_pick_outer_boss_skin_x == pytest.approx(0.25)
    assert _intersection_volume(inner_tools, make_hopper_void()) < 1e-7

    body = make_hollow_keyboard_container()
    cover = make_magnetic_rear_cover()
    for x in p.magnet_pick_bore_centres_x:
        # Empty inside each pick channel, solid immediately beyond its floor.
        assert not body.is_inside(Vector(x, -18.21, p.return_magnet_center_z))
        assert body.is_inside(Vector(x, -18.19, p.return_magnet_center_z))
        assert not cover.is_inside(Vector(x, -18.51, p.return_magnet_center_z))
        assert cover.is_inside(Vector(x, -18.49, p.return_magnet_center_z))
        assert not cover.is_inside(Vector(x, -16.89, p.return_magnet_center_z))
        assert cover.is_inside(Vector(x, -16.91, p.return_magnet_center_z))


def test_integrated_rear_surface_has_magnet_clearance_without_hard_stop_contact():
    assert p.cover_magnet_boss_y == pytest.approx((-18.8, -14.3))
    pressed_body = placed_hollow_keyboard_container(p.pressed_state)
    assert p.inner_center_y(p.pressed_state) + p.inner_body_local_y[0] == pytest.approx(-12.9)
    assert p.magnet_face_separation_y(p.pressed_state) == pytest.approx(1.4)
    assert _intersection_volume(pressed_body, make_magnetic_rear_cover()) < 1e-7


def test_integrated_inner_has_no_exposed_shutter_fin_or_cover_relief():
    body = make_hollow_keyboard_container()
    assert body.is_valid and len(body.solids()) == 1
    assert body.bounding_box().min.Y == pytest.approx(p.inner_body_local_y[0])
    assert p.released_outer_port_rear_cover_y >= p.released_seal_safety_inset
    assert p.released_inner_port_front_cover_y >= p.released_seal_safety_inset
    assert _intersection_volume(placed_hollow_keyboard_container(p.pressed_state), make_magnetic_rear_cover()) < 1e-7
