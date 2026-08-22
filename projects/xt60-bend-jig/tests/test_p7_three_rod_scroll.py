"""Math and actual-BREP acceptance for the P7 synchronized scroll prototype."""

from __future__ import annotations

from math import hypot, isclose, sqrt
from pathlib import Path

import pytest
from build123d import import_step

import xt60_bend_jig.p7_three_rod_scroll as p7
from xt60_bend_jig.p2_corner_clamp import build_wire_centerline, build_wires


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "cad" / "p7_three_rod_scroll"
ROD_NAMES = ("upright", "bottom", "diagonal")


def _distance_point_to_segment(point, first, second):
    dy, dz = second.y - first.y, second.z - first.z
    denom = dy * dy + dz * dz
    if denom == 0.0:
        return hypot(point.y - first.y, point.z - first.z)
    u = max(0.0, min(1.0, ((point.y - first.y) * dy + (point.z - first.z) * dz) / denom))
    return hypot(point.y - (first.y + u * dy), point.z - (first.z + u * dz))


def test_frozen_stack_hardware_and_math_audit_values():
    p = p7.P7_DEFAULTS
    assert (p.rod_diameter, p.rod_length) == pytest.approx((4.0, 50.0))
    assert (p.clear_span, p.fixed_plate_thickness, p.scroll_plate_thickness) == pytest.approx((32.0, 3.0, 2.5))
    assert p.scroll_axial_clearance == pytest.approx(0.3)
    assert (p.shaft_y, p.shaft_z) == pytest.approx((-7.5, 32.5))
    assert (p.shaft_diameter, p.shaft_bore_diameter, p.scroll_hex_socket_across_corners) == pytest.approx((6.0, 6.2, 6.15))
    assert p.scroll_diameter == pytest.approx(64.0)
    assert p.rod_projection == pytest.approx(3.2)
    assert p.cap_socket_depth == pytest.approx(2.9)
    assert (p.shaft_keeper_neck_width, p.shaft_keeper_neck_across_corners) == pytest.approx((3.2, 5.2))
    assert (p.shaft_keeper_pocket, p.shaft_keeper_throat) == pytest.approx((5.4, 4.7))


def test_401_pose_contract_is_common_monotonic_and_has_true_70_to_80_dwell():
    p = p7.P7_DEFAULTS
    travels = [p7.travel_at_angle(p.end_angle * i / 400.0) for i in range(401)]
    assert travels[0] == pytest.approx(0.0) and travels[-1] == pytest.approx(11.0)
    assert all(a <= b + 1e-12 for a, b in zip(travels, travels[1:]))
    dwell = [p7.travel_at_angle(70.0 + 10.0 * i / 200.0) for i in range(201)]
    assert max(dwell) - min(dwell) == pytest.approx(0.0, abs=1e-12)
    for name in ROD_NAMES:
        frozen = p7.rod_center(name, 70.0)
        assert all(p7.rod_center(name, 70.0 + i / 20.0) == frozen for i in range(201))


def test_inverse_kinematic_slot_polyline_reconstructs_every_follower_within_0p02mm():
    p = p7.P7_DEFAULTS
    for name in ROD_NAMES:
        polyline = p7.slot_path(name)
        worst = 0.0
        for index in range(801):
            q = p7.inverse_slot_point(name, p.end_angle * index / 800.0)
            residual = min(_distance_point_to_segment(q, a, b) for a, b in zip(polyline, polyline[1:]))
            worst = max(worst, residual)
        assert worst <= 0.02
        # The local dwell is a constant-radius arc about the shared shaft.
        radii = []
        for index in range(101):
            q = p7.inverse_slot_point(name, 70.0 + 10.0 * index / 100.0)
            radii.append(hypot(q.y - p.shaft_y, q.z - p.shaft_z))
        assert max(radii) - min(radii) <= 1e-9


def test_audited_scroll_envelope_rim_and_inter_slot_webs_are_preserved():
    p = p7.P7_DEFAULTS
    sampled = {
        name: [p7.inverse_slot_point(name, p.end_angle * i / 800.0) for i in range(801)]
        for name in ROD_NAMES
    }
    max_radius = max(
        hypot(q.y - p.shaft_y, q.z - p.shaft_z)
        for points in sampled.values() for q in points
    )
    assert max_radius == pytest.approx(26.301568, abs=2e-5)
    assert p.scroll_diameter / 2.0 - max_radius - p.scroll_slot_width / 2.0 >= 3.49
    minimum_center_separation = float("inf")
    for first_index, first_name in enumerate(ROD_NAMES):
        for second_name in ROD_NAMES[first_index + 1:]:
            for first in sampled[first_name]:
                minimum_center_separation = min(
                    minimum_center_separation,
                    min(hypot(first.y - second.y, first.z - second.z) for second in sampled[second_name]),
                )
    assert minimum_center_separation - p.scroll_slot_width >= 2.0


def test_201_actual_brep_pose_sweep_has_clear_guides_scrolls_rods_and_zero_skew():
    p = p7.P7_DEFAULTS
    frame = p7.build_fixed_frame()
    scroll_zero = p7.build_scroll_plate("left")
    stop_pin = p7.build_stop_pins().children[0]
    assert frame.is_valid and len(frame.solids()) == 1
    assert scroll_zero.is_valid and len(scroll_zero.solids()) == 1
    for index in range(201):
        angle = p.end_angle * index / 200.0
        scroll = p7._rotate_about_shaft(scroll_zero, angle, p)
        rods = list(p7.build_rods(angle).children)
        assert len(rods) == 3
        for rod in rods:
            assert (*rod.bounding_box().size,) == pytest.approx((50.0, 4.0, 4.0), abs=1e-7)
            assert (rod & frame).volume == pytest.approx(0.0, abs=1e-7)
            assert (rod & scroll).volume == pytest.approx(0.0, abs=1e-7)
        for first_index, first in enumerate(rods):
            for second in rods[first_index + 1:]:
                assert (first & second).volume == pytest.approx(0.0, abs=1e-7)
        assert (scroll & stop_pin).volume == pytest.approx(0.0, abs=1e-7)


def test_closed_actual_brep_rods_are_tangent_to_actual_brep_90deg_wire_reference():
    rods = p7.build_rods(80.0)
    wires = build_wires()
    for rod in rods.children:
        assert rod.distance_to(wires) == pytest.approx(0.0, abs=1.1e-7)
        assert (rod & wires).volume == pytest.approx(0.0, abs=1e-7)
    centerline = build_wire_centerline()
    edges = list(centerline.edges())
    assert centerline.length == pytest.approx(44.0)
    horizontal = edges[0].tangent_at(0.5)
    vertical = edges[-1].tangent_at(0.5)
    assert horizontal.dot(vertical) == pytest.approx(0.0, abs=1e-12)
    assert tuple(horizontal) == pytest.approx((0.0, -1.0, 0.0))
    assert tuple(vertical) == pytest.approx((0.0, 0.0, 1.0))


def test_hex_shaft_clears_round_fixed_bearings_keys_scrolls_and_rejects_phase_error():
    p = p7.P7_DEFAULTS
    frame = p7.build_fixed_frame()
    scroll_zero = p7.build_scroll_plate("right")
    for angle in (0.0, 13.0, 37.0, 70.0, 80.0):
        shaft = p7.build_shaft_and_dial(angle)
        scroll = p7._rotate_about_shaft(scroll_zero, angle, p)
        assert (shaft & frame).volume == pytest.approx(0.0, abs=1e-7)
        assert (shaft & scroll).volume == pytest.approx(0.0, abs=1e-7)
        wrong_phase = p7.build_shaft_and_dial(angle + 30.0)
        assert (wrong_phase & scroll).volume > 1.0


def test_positive_80deg_stop_is_zero_gap_and_overtravel_interferes_without_wire_overtravel():
    p = p7.P7_DEFAULTS
    base = p7.build_scroll_plate("right")
    pin = p7.build_stop_pins().children[1]
    at_stop = p7._rotate_about_shaft(base, 80.0, p)
    over = p7._rotate_about_shaft(base, 80.2, p)
    assert at_stop.distance_to(pin) == pytest.approx(0.0, abs=1e-7)
    assert (at_stop & pin).volume == pytest.approx(0.0, abs=1e-7)
    assert (over & pin).volume > 0.1
    frame = p7.build_fixed_frame()
    assert (at_stop & frame).volume == pytest.approx(0.0, abs=1e-7)
    assert at_stop.distance_to(frame) == pytest.approx(0.0, abs=1e-7)
    assert (over & frame).volume > 0.1
    assert p7.rod_center("upright", 70.0) == p7.rod_center("upright", 80.0)


def test_press_caps_and_radial_C_keepers_retain_without_clamping_scroll_faces():
    p = p7.P7_DEFAULTS
    point = p7.rod_center("bottom", 80.0)
    rod = p7.build_rod("bottom", 80.0)
    left = p7.build_cap("left", point)
    right = p7.build_cap("right", point)
    right_scroll = p7._rotate_about_shaft(p7.build_scroll_plate("right"), 80.0, p)
    assert left.is_valid and len(left.solids()) == 1
    assert right.is_valid and len(right.solids()) == 1
    assert (rod & left).volume > 0.01  # documented Ø3.90 press trial
    assert (rod & right).volume == pytest.approx(0.0, abs=1e-7)
    assert right.distance_to(right_scroll) == pytest.approx(p.axial_float, abs=1e-7)
    # A radial withdrawal must flex the 3.60 throat over the Ø4 rod.
    shifted_toward_throat = p7.Pos(0.0, -1.0, 0.0) * right
    assert (shifted_toward_throat & rod).volume > 0.0


def test_end_lock_and_shaft_keeper_are_removable_positive_retention_parts():
    p = p7.P7_DEFAULTS
    frame = p7.build_fixed_frame()
    lock_pin = p7.build_end_lock_pin()
    shaft_80 = p7.build_shaft_and_dial(80.0)
    shaft_79 = p7.build_shaft_and_dial(79.0)
    assert (lock_pin & frame).volume == pytest.approx(0.0, abs=1e-7)
    assert (lock_pin & shaft_80).volume == pytest.approx(0.0, abs=1e-7)
    assert (lock_pin & shaft_79).volume > 0.1
    keeper = p7.build_shaft_keeper()
    assert keeper.is_valid and len(keeper.solids()) == 1
    assert keeper.distance_to(p7.build_scroll_plate("left")) == pytest.approx(p.axial_float, abs=1e-7)
    shaft = p7.build_shaft_and_dial(0.0)
    assert (keeper & shaft).volume == pytest.approx(0.0, abs=1e-7)
    # The 3.0 mm keeper has 0.1 mm axial clearance per side in the 3.2 mm
    # reduced neck; +/-0.2 mm reaches an actual full Ø6 shoulder.
    assert (p7.Pos(0.2, 0.0, 0.0) * keeper & shaft).volume > 0.0
    assert (p7.Pos(-0.2, 0.0, 0.0) * keeper & shaft).volume > 0.0


def test_all_printed_parts_are_named_closed_positive_solids_and_kit_has_no_overlap():
    kit = p7.build_print_kit()
    assert kit.is_valid and len(kit.children) == 12
    assert len({child.label for child in kit.children}) == 12
    assert all(child.is_valid and len(child.solids()) == 1 and child.volume > 0.0 for child in kit.children)
    assert all(child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7) for child in kit.children)
    # The one-piece frame stands on the flat external clamp tab; the paired
    # guide plates are vertical, not suspended as a horizontal bridge.
    frame = kit.children[0]
    assert frame.bounding_box().size.Z > 60.0
    bed_faces = [face for face in frame.faces() if abs(face.bounding_box().min.Z) <= 1e-7 and abs(face.bounding_box().max.Z) <= 1e-7]
    assert max(face.area for face in bed_faces) >= 38.0 * 17.0
    for index, first in enumerate(kit.children):
        for second in kit.children[index + 1:]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)


def test_generated_step_targets_match_source_when_artifacts_exist():
    cases = (
        ("p7_loaded_open.step", p7.build_loaded_open()),
        ("p7_loaded_mid.step", p7.build_loaded_mid()),
        ("p7_loaded_closed.step", p7.build_loaded_closed()),
        ("p7_exploded.step", p7.build_exploded()),
        ("p7_print_kit.step", p7.build_print_kit()),
    )
    if not all((OUT / filename).exists() for filename, _ in cases):
        pytest.skip("P7 STEP artifacts not generated yet")
    for filename, source in cases:
        imported = import_step(OUT / filename)
        assert len(imported.solids()) == len(source.solids())
        assert (*imported.bounding_box().min, *imported.bounding_box().max) == pytest.approx(
            (*source.bounding_box().min, *source.bounding_box().max), abs=1e-7
        )
