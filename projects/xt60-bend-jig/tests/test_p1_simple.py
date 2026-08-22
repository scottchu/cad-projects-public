"""Geometry and mechanism contract for the manual P1 proof."""

from __future__ import annotations

from math import pi

import pytest
from build123d import Align, Cylinder, Pos

from xt60_bend_jig.mechanism import solve_mechanism
from xt60_bend_jig.p1_simple import (
    P1_SIMPLE_DEFAULTS,
    SimpleP1Parameters,
    build_center_pusher,
    build_large_side_plate,
    build_loaded_closed,
    build_loaded_open,
    build_print_kit,
    build_three_rods,
    closed_contact_centers,
)


def _x_probe(diameter: float, length: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def test_p1_rejects_14_awg_instead_of_claiming_shared_fixed_datums():
    with pytest.raises(ValueError, match="12 AWG only"):
        SimpleP1Parameters(wire_gauge=14)


def test_exactly_two_fixed_plates_and_one_rigid_pusher_are_printed():
    kit = build_print_kit()
    assert len(kit.children) == 3
    assert [len(child.solids()) for child in kit.children] == [1, 1, 1]
    assert all(child.is_valid and child.volume > 0 for child in kit.children)
    assert len(build_center_pusher().solids()) == 1


def test_large_plates_are_mirrored_and_preserve_38mm_clear_span():
    p = P1_SIMPLE_DEFAULTS
    left = build_large_side_plate("left").bounding_box()
    right = build_large_side_plate("right").bounding_box()
    assert left.size.X == pytest.approx(4.0)
    assert right.size.X == pytest.approx(4.0)
    assert right.min.X - left.max.X == pytest.approx(38.0)
    assert right.max.X - left.min.X == pytest.approx(46.0)


@pytest.mark.parametrize("side", ("left", "right"))
def test_each_large_plate_has_exactly_two_4p3_reaction_bores(side):
    p = P1_SIMPLE_DEFAULTS
    plate = build_large_side_plate(side)
    x = (-1 if side == "left" else 1) * p.plate_center_x
    centers = closed_contact_centers()
    for name in ("upper", "lower"):
        point = centers[name]
        exact = _x_probe(4.3, 6.0, x, point.y, point.z)
        oversize = _x_probe(4.32, 3.0, x, point.y, point.z)
        assert (plate & exact).volume == pytest.approx(0.0, abs=1e-7)
        assert (plate & oversize).volume > 0.0
    cylindrical_faces = [face for face in plate.faces() if face.geom_type.name == "CYLINDER"]
    assert len(cylindrical_faces) == 2


def test_each_small_end_tab_has_one_shared_4p3_moving_axis():
    p = P1_SIMPLE_DEFAULTS
    pusher = build_center_pusher()
    moving = closed_contact_centers()["moving"]
    for sign in (-1.0, 1.0):
        x = sign * p.plate_center_x
        exact = _x_probe(4.3, 6.0, x, moving.y, moving.z)
        oversize = _x_probe(4.32, 3.0, x, moving.y, moving.z)
        assert (pusher & exact).volume == pytest.approx(0.0, abs=1e-7)
        assert (pusher & oversize).volume > 0.0
    cylindrical_faces = [face for face in pusher.faces() if face.geom_type.name == "CYLINDER"]
    assert len(cylindrical_faces) == 2


def test_all_three_reference_rods_are_exactly_4x50_and_coaxial_with_bores():
    rods = build_three_rods()
    assert len(rods.children) == 3
    for rod in rods.children:
        bb = rod.bounding_box()
        assert bb.size.X == pytest.approx(50.0)
        assert bb.size.Y == pytest.approx(4.0)
        assert bb.size.Z == pytest.approx(4.0)
    centers = closed_contact_centers()
    p = P1_SIMPLE_DEFAULTS
    for side in (-1.0, 1.0):
        x = side * p.plate_center_x
        for name in ("upper", "lower"):
            point = centers[name]
            assert (build_large_side_plate("left" if side < 0 else "right") & _x_probe(4.0, 6.0, x, point.y, point.z)).volume == pytest.approx(0.0, abs=1e-7)


def test_closed_moving_axis_matches_12awg_solver_exactly():
    raw = solve_mechanism(wire_gauge=12, closure=1.0).moving_rod_center
    actual = closed_contact_centers()["moving"]
    assert actual.y == pytest.approx(raw.y)
    assert actual.z == pytest.approx(raw.z + P1_SIMPLE_DEFAULTS.assembly_z_lift)


def test_matching_hard_stops_touch_without_positive_volume_interference():
    pusher = build_center_pusher()
    for side in ("left", "right"):
        plate = build_large_side_plate(side)
        assert (plate & pusher).volume == pytest.approx(0.0, abs=1e-7)
        assert plate.distance_to(pusher) == pytest.approx(0.0, abs=1e-7)


def test_manual_45deg_open_path_is_collision_free_and_not_powered():
    p = P1_SIMPLE_DEFAULTS
    closed = build_center_pusher()
    plates = build_large_side_plate("left") + build_large_side_plate("right")
    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        d = p.withdrawal_component * fraction
        moved = Pos(0, d, -d) * closed
        assert (plates & moved).volume == pytest.approx(0.0, abs=1e-7)
    labels = " ".join(child.label for child in build_loaded_open().children).lower()
    assert "manual" in labels
    assert all(term not in labels for term in ("screw", "dial", "nut", "powered"))


def test_90_degree_r6_wire_solver_tangencies_and_length_are_preserved():
    solution = solve_mechanism(wire_gauge=12, closure=1.0)
    assert solution.bend_angle_degrees == pytest.approx(90.0)
    assert solution.parameters.bend_radius == pytest.approx(6.0)
    assert solution.bend_arc_length == pytest.approx(6.0 * pi / 2.0)
    assert solution.path_length == pytest.approx(solution.available_lead_length)
    assert all(abs(gap) <= 1e-9 for gap in solution.contact_gaps.values())


def test_loaded_states_are_valid_and_keep_workpiece_references_visible():
    for assembly in (build_loaded_closed(), build_loaded_open()):
        assert assembly.is_valid
        labels = {child.label for child in assembly.children}
        assert "reference_bottom_ESC" in labels
        assert "reference_vertical_XT60" in labels
        assert "reference_two_horizontal_R6_90deg_vertical_12awg_leads" in labels


def test_print_layout_is_on_bed_nonoverlapping_and_within_256_square():
    kit = build_print_kit()
    bounds = kit.bounding_box()
    assert bounds.min.Z == pytest.approx(0.0, abs=1e-7)
    assert bounds.size.X <= 256.0
    assert bounds.size.Y <= 256.0
    for child in kit.children:
        assert child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    for index, first in enumerate(kit.children):
        for second in kit.children[index + 1 :]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)

