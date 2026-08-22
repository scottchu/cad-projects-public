"""CAD and math acceptance for P10's practical four-disc clamp."""

from __future__ import annotations

from itertools import combinations
from math import asin, atan2, cos, degrees, hypot, radians, sin, sqrt
from pathlib import Path
import subprocess
import sys

import pytest
from build123d import Pos, import_step

import xt60_bend_jig.p10_practical_four_disc_clamp as p10
from xt60_bend_jig.p2_corner_clamp import build_wire_centerline, build_wires


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "cad" / "p10_practical_four_disc_clamp"
P = p10.P10_DEFAULTS


def _all_clear(sweep, members, tolerance=1e-7):
    return all((sweep & member).volume <= tolerance for member in members)


def _bounds(shape):
    return (*shape.bounding_box().min, *shape.bounding_box().max)


def _solid_volume(shape):
    return sum(solid.volume for solid in shape.solids())


def _common_volume(first, second):
    common = first & second
    return 0.0 if common is None else common.volume


def _brep_symmetric_difference_volume(first, second):
    def key(solid):
        return tuple(round(value, 7) for value in _bounds(solid))

    first_solids = sorted(first.solids(), key=key)
    second_solids = sorted(second.solids(), key=key)
    assert len(first_solids) == len(second_solids)
    return sum(
        a.volume + b.volume - 2.0 * _common_volume(a, b)
        for a, b in zip(first_solids, second_solids)
    )


def _planar_face_area(shape, axis, coordinate, tolerance=1e-7):
    index = {"X": 0, "Y": 1, "Z": 2}[axis]
    return sum(
        face.area for face in shape.faces()
        if abs(tuple(face.bounding_box().min)[index] - coordinate) <= tolerance
        and abs(tuple(face.bounding_box().max)[index] - coordinate) <= tolerance
    )


def test_frozen_endpoint_is_exact_90_and_final_wheel_index_is_straight():
    assert P.end_angle == pytest.approx(80.0)
    assert P.stop_arm_angle == pytest.approx(85.0424510692, abs=1e-10)
    assert P.stop_pin_radius == pytest.approx(hypot(34.0, 3.0), abs=1e-12)
    assert (P.stop_pin_y, P.stop_pin_z) == pytest.approx(
        (-4.5503852184, 66.5044081354), abs=1e-10)
    dy, dz = P.stop_pin_y - P.shaft_y, P.stop_pin_z - P.shaft_z
    a = radians(P.end_angle)
    assert (cos(a) * dy + sin(a) * dz, -sin(a) * dy + cos(a) * dz) == pytest.approx((34.0, 3.0), abs=1e-10)
    assert P.end_angle + 10.0 == pytest.approx(90.0)
    centerline = build_wire_centerline()
    edges = list(centerline.edges())
    assert centerline.length == pytest.approx(44.0)
    assert tuple(edges[0].tangent_at(0.5)) == pytest.approx((0.0, -1.0, 0.0))
    assert tuple(edges[-1].tangent_at(0.5)) == pytest.approx((0.0, 0.0, 1.0))
    assert edges[0].tangent_at(0.5).dot(edges[-1].tangent_at(0.5)) == pytest.approx(0.0, abs=1e-12)


def test_motion_law_same_fixed_L_workpiece_clearance_and_tangency():
    wires = build_wires()
    travels = [p10.travel_at_angle(P.end_angle * i / 400.0, P) for i in range(401)]
    assert travels[0] == pytest.approx(0.0)
    assert travels[-1] == pytest.approx(11.0)
    assert all(first <= second + 1e-12 for first, second in zip(travels, travels[1:]))
    assert all(p10.rod_center(name, 70.0, P) == p10.rod_center(name, 80.0, P) for name in p10.ROD_NAMES)
    for angle in (0.0, 13.7, 41.3, 60.0, 63.09484):
        for rod in p10.build_rods(angle, 0.0, P).children:
            assert rod.distance_to(wires) > 0.30
            assert (rod & wires).volume == pytest.approx(0.0, abs=1e-7)
    for angle in (70.0, 73.3, 80.0):
        for rod in p10.build_rods(angle, 0.0, P).children:
            assert rod.distance_to(wires) <= 0.02
            assert (rod & wires).volume == pytest.approx(0.0, abs=1e-7)
    labels = [child.label for child in p10.build_fixed_L_workpiece().children]
    assert labels == [child.label for child in p10.build_fixed_L_workpiece().children]
    assert any("same_fixed_prebent_L" in label for label in labels)


def test_dense_full_motion_brep_slots_and_named_contact_bands():
    expected_bands = {
        "upright": ((0.0, 42.0), (0.0, 1.0)),
        "bottom": ((12.0, 30.0), (-1.0, 0.0)),
        "diagonal": ((1.7573593129, 31.7573593129),
                     (-1.0 / sqrt(2.0), 1.0 / sqrt(2.0))),
    }
    for name, (center, tangent) in expected_bands.items():
        actual_center, actual_tangent = p10.contact_band(name, P)
        assert (actual_center.y, actual_center.z) == pytest.approx(center, abs=1e-9)
        assert (actual_tangent.y, actual_tangent.z) == pytest.approx(tangent, abs=1e-12)
        assert hypot(actual_tangent.y, actual_tangent.z) == pytest.approx(1.0, abs=1e-12)
        rod = p10.rod_center(name, P.end_angle, P)
        normal = (rod.y - actual_center.y, rod.z - actual_center.z)
        assert hypot(*normal) == pytest.approx(P.wire_diameter / 2.0 + P.rod_diameter / 2.0)
        assert normal[0] * actual_tangent.y + normal[1] * actual_tangent.z == pytest.approx(
            0.0, abs=1e-10)

    # 0.25-degree math grid, including the full dwell, proves every named
    # follower center transforms back onto its matching inverse-slot center.
    for index in range(321):
        angle = P.end_angle * index / 320.0
        a = radians(angle)
        for name in p10.ROD_NAMES:
            world = p10.rod_center(name, angle, P)
            local = p10.inverse_slot_point(name, angle, P)
            dy, dz = local.y - P.shaft_y, local.z - P.shaft_z
            reconstructed = (
                P.shaft_y + cos(a) * dy - sin(a) * dz,
                P.shaft_z + sin(a) * dy + cos(a) * dz,
            )
            assert reconstructed == pytest.approx((world.y, world.z), abs=1e-10)

    # A dense 1-degree BREP grid checks every purchased rod against the same
    # fixed workpiece used by all phases. A smaller 10-degree grid checks the
    # real through-slots without turning the regression into a many-minute
    # boolean of the complete cam at every fractional pose.
    wires = build_wires()
    for index in range(81):
        angle = float(index)
        for rod in p10.build_rods(angle, 0.0, P).children:
            assert _common_volume(rod, wires) == pytest.approx(0.0, abs=1e-7)
            clearance = rod.distance_to(wires)
            if angle <= 63.0:
                assert clearance > 0.30
            if angle >= 70.0:
                assert clearance <= 0.02

    fixed = {side: p10.build_fixed_disc(side, "seated_envelope", P)
             for side in ("left", "right")}
    cam_zero = {side: p10.build_cam_disc(side, P) for side in ("left", "right")}
    for index in range(9):
        angle = P.end_angle * index / 8.0
        for name in p10.ROD_NAMES:
            point = p10.rod_center(name, angle, P)
            for side in ("left", "right"):
                sign = -1.0 if side == "left" else 1.0
                fixed_probe = p10._x_cylinder(
                    4.0, P.fixed_plate_thickness + 0.2,
                    sign * P.fixed_plate_center_x, point.y, point.z,
                )
                cam_probe = p10._x_cylinder(
                    4.0, P.scroll_plate_thickness + 0.2,
                    sign * P.scroll_plate_center_x, point.y, point.z,
                )
                cam = p10._rotate_about_shaft(cam_zero[side], angle, P)
                assert _common_volume(fixed_probe, fixed[side]) == pytest.approx(0.0, abs=1e-7)
                assert _common_volume(cam_probe, cam) == pytest.approx(0.0, abs=1e-7)


def test_fixed_disc_core_lands_ribs_and_rotation_bounds_are_exact():
    base = p10.build_base(P)
    for side in ("left", "right"):
        core, tongue, shoulders = p10._fixed_disc_core(side, P)
        x = (-1.0 if side == "left" else 1.0) * P.fixed_plate_center_x
        disc = p10._x_cylinder(P.scroll_diameter, P.fixed_plate_thickness, x, P.shaft_y, P.shaft_z)
        assert core.is_valid and len(core.solids()) == 1
        assert [(tongue & shoulder).volume for shoulder in shoulders] == pytest.approx((0.1875, 0.1875), abs=1e-9)
        assert all((disc & shoulder).volume >= 4.78 for shoulder in shoulders)
        assert shoulders[0].bounding_box().min.Y == pytest.approx(-16.8)
        assert shoulders[1].bounding_box().max.Y == pytest.approx(1.5)
        assert (-14.8 - shoulders[0].bounding_box().min.Y) == pytest.approx(2.0)
        raw = p10.build_fixed_disc(side, "as_printed", P)
        seated = p10.build_fixed_disc(side, "seated_envelope", P)
        raw_overlap = (raw & base).volume
        assert raw_overlap > 0.0
        assert raw.volume - seated.volume == pytest.approx(raw_overlap, abs=1e-7)
        declared_ribs = p10._fuse([
            p10._outboard_rib(side, -11.0, P), p10._outboard_rib(side, -4.0, P),
            p10._rear_rib(side, -0.75, P), p10._rear_rib(side, 0.75, P),
        ])
        declared_mask = declared_ribs & base
        actual_mask = raw - seated
        assert (actual_mask - declared_mask).volume == pytest.approx(0.0, abs=1e-8)
        assert (declared_mask - actual_mask).volume == pytest.approx(0.0, abs=1e-8)
        assert (seated & base).volume == pytest.approx(0.0, abs=1e-7)
        assert seated.distance_to(base) == pytest.approx(0.0, abs=1e-7)
        for rib in (p10._outboard_rib(side, -11.0, P), p10._rear_rib(side, -0.75, P)):
            assert (rib.bounding_box().min.Z, rib.bounding_box().max.Z) == pytest.approx((-3.75, -1.25))
    yaw = degrees(asin(3.25 / sqrt(3.0**2 + 14.0**2)) - atan2(3.0, 14.0))
    roll = degrees(asin(4.20 / sqrt(4.0**2 + 14.0**2)) - atan2(4.0, 14.0))
    pitch = degrees(asin(3.25 / sqrt(3.0**2 + 4.0**2)) - atan2(3.0, 4.0))
    assert (yaw, roll, pitch) == pytest.approx((1.02515884, 0.82021652, 3.67170423), abs=1e-8)


def test_integral_stop_is_clear_to_79p99_touches_80_and_blocks_overtravel():
    fixed = p10.build_fixed_disc("right", "seated_envelope", P)
    cam_zero = p10.build_cam_disc("right", P)
    expectations = ((79.99, 0.0), (80.0, 0.0), (80.01, 0.0031652074), (80.1, 0.0995658976))
    for angle, expected in expectations:
        cam = p10._rotate_about_shaft(cam_zero, angle, P)
        assert (cam & fixed).volume == pytest.approx(expected, abs=2e-7)
    assert p10._rotate_about_shaft(cam_zero, 79.99, P).distance_to(fixed) > 0.0
    assert p10._rotate_about_shaft(cam_zero, 80.0, P).distance_to(fixed) == pytest.approx(0.0, abs=1e-7)
    assert (p10._rotate_about_shaft(cam_zero, 80.1, P) & fixed).volume >= 0.09
    pin_center_radius = hypot(P.stop_pin_y - P.shaft_y, P.stop_pin_z - P.shaft_z)
    assert pin_center_radius - P.scroll_diameter / 2.0 - 1.5 >= 0.60


def test_locator_is_one_solid_single_Z_datum_and_has_full_clear_sweep():
    base = p10.build_base(P)
    raw = p10.build_locator("as_printed", 0.0, P)
    seated = p10.build_locator("seated_envelope", 0.0, P)
    assert raw.is_valid and seated.is_valid and len(raw.solids()) == len(seated.solids()) == 1
    assert (raw & base).volume == pytest.approx(0.0914285714, abs=1e-8)
    assert (seated & base).volume == pytest.approx(0.0, abs=1e-7)
    assert seated.distance_to(base) == pytest.approx(0.0, abs=1e-7)
    specs = dict((name, (center, size)) for name, center, size in p10._locator_box_specs())
    assert specs["main_T_rail"] == ((-0.25, 1.75, -4.65), (44.9, 2.0, 3.0))
    assert specs["T_neck_open_clearance"] == ((-0.25, 3.0, -3.4), (44.9, 1.2, 1.5))
    assert specs["runner_+8.5"] == ((8.5, 14.1, -2.3), (2.5, 21.2, 3.0))
    rail_center, rail_size = specs["main_T_rail"]
    assert (rail_center[0] - rail_size[0] / 2.0,
            rail_center[0] + rail_size[0] / 2.0) == pytest.approx((-22.70, 22.20))
    fence_center, fence_size = specs["right_wire_fence"]
    assert (fence_center[0] - fence_size[0] / 2.0,
            fence_center[0] + fence_size[0] / 2.0,
            fence_center[2] - fence_size[2] / 2.0,
            fence_center[2] + fence_size[2] / 2.0) == pytest.approx((6.15, 7.15, 27.65, 30.40))
    assert -4.15 - (-4.30) == pytest.approx(0.15)
    assert (-2.50) - (-2.65) == pytest.approx(0.15)
    assert 27.85 - (-6.15) == pytest.approx(34.0)
    sweep = p10.build_locator_swept_volume(80.0, P)
    plates = list(p10.build_principal_plates(80.0, "seated_envelope", 0.0, P).children)
    assert all((sweep & plate).volume == pytest.approx(0.0, abs=1e-7) for plate in plates)
    assert min(sweep.distance_to(plate) for plate in plates) >= 0.75
    raw_mask = raw - seated
    expected_raw_mask = p10._locator_wedge(True) - p10._locator_wedge(False)
    assert (raw_mask - expected_raw_mask).volume == pytest.approx(0.0, abs=1e-9)
    assert (expected_raw_mask - raw_mask).volume == pytest.approx(0.0, abs=1e-9)
    assert ((raw & base) - raw_mask).volume == pytest.approx(0.0, abs=1e-9)
    # +X is the only declared extraction direction. Pure +Y necessarily runs
    # the under-wire support into the ESC; -X also jams in the base key.
    esc = p10.build_electronics_reference().children[0]
    assert _common_volume(seated, esc) == pytest.approx(0.0, abs=1e-8)
    assert _common_volume(Pos(0.0, 0.50, 0.0) * seated, esc) >= 3.74
    assert ((Pos(-0.10, 0.0, 0.0) * seated) & base).volume >= 0.30
    stationary = [
        base, *plates, *p10.build_rods(80.0, 0.0, P).children,
        *p10.build_retainers(80.0, 0.0, 0.0, P).children,
        p10.build_shaft(80.0, P), p10.build_shaft_keeper(P),
        p10.build_wheel(80.0, "seated_envelope", P), p10.build_lock_pin(False, P),
        *p10.build_electronics_reference().children, *p10.build_fixed_L_workpiece().children,
    ]
    assert _all_clear(sweep, stationary)
    # 181 off-grid poses supplement the continuous swept-BREP proof.
    for index in range(181):
        shifted = Pos(80.0 * (index + 0.37) / 181.0, 0.0, 0.0) * seated
        assert all((shifted & plate).volume == pytest.approx(0.0, abs=1e-7) for plate in plates)


def test_locked_locator_removed_solder_tip_and_hand_corridor_is_clear():
    corridor = p10.build_solder_access_corridor(P)
    assert corridor.is_valid and len(corridor.solids()) == 1
    assert _bounds(corridor) == pytest.approx((-15.0, 28.0, 25.0, 15.0, 86.0, 43.0))
    targets = p10.build_solder_target_envelope(P)
    assert len(targets.children) == 2
    assert all((target - corridor).volume == pytest.approx(0.0, abs=1e-8)
               for target in targets.children)
    assembly = p10.build_locator_removed_closed(P)
    structural = [
        child for child in assembly.children
        if "ESC_FC" not in child.label and "pigtail" not in child.label
    ]
    assert _all_clear(corridor, structural)
    assert any("locator_seated_envelope_xshift_80" in child.label for child in structural)


def test_datum_chain_stripped_conductors_and_bottom_ESC_are_frozen():
    electronics = p10.build_electronics_reference()
    assert "bottom_ESC" in electronics.children[0].label
    assert "FC_above_ESC" in electronics.children[1].label
    workpiece = p10.build_fixed_L_workpiece()
    wire_pair = workpiece.children[0]
    left_wire, right_wire = wire_pair.children
    specs = dict((name, (center, size)) for name, center, size in p10._locator_box_specs())
    left_shelf = p10._box(*specs["left_wire_shelf"])
    right_shelf = p10._box(*specs["right_wire_shelf"])
    right_fence = p10._box(*specs["right_wire_fence"])
    esc_tab = p10._box(*specs["right_ESC_edge_tab"])
    assert left_shelf.distance_to(left_wire) == pytest.approx(0.0, abs=2e-7)
    assert right_shelf.distance_to(right_wire) == pytest.approx(0.0, abs=2e-7)
    assert _common_volume(left_shelf, left_wire) == pytest.approx(0.0, abs=1e-7)
    assert _common_volume(right_shelf, right_wire) == pytest.approx(0.0, abs=1e-7)
    assert right_fence.distance_to(right_wire) == pytest.approx(0.0, abs=2e-7)
    assert _common_volume(right_fence, right_wire) == pytest.approx(0.0, abs=1e-7)
    assert (right_fence.bounding_box().min.X,
            right_wire.bounding_box().max.X) == pytest.approx((6.15, 6.15), abs=2e-7)
    assert (left_shelf.bounding_box().max.Z,
            right_shelf.bounding_box().max.Z,
            left_wire.bounding_box().min.Z,
            right_wire.bounding_box().min.Z) == pytest.approx((27.85, 27.85, 27.85, 27.85), abs=2e-7)
    assert esc_tab.distance_to(electronics.children[0]) == pytest.approx(0.0, abs=1e-7)
    assert (esc_tab.bounding_box().max.Y,
            electronics.children[0].bounding_box().min.Y) == pytest.approx((28.0, 28.0))
    conductors = [child for child in workpiece.children if "tinned_conductor" in child.label]
    assert len(conductors) == 2
    for conductor, x in zip(conductors, (-4.0, 4.0)):
        box = conductor.bounding_box()
        assert (box.min.X + box.max.X) / 2.0 == pytest.approx(x)
        assert (box.min.Y, box.max.Y) == pytest.approx((28.0, 33.0))
        assert (box.size.X, box.size.Z) == pytest.approx((2.3, 2.3), abs=1e-7)
        pad = next(child for child in electronics.children
                   if f"reference_{'negative' if x < 0 else 'positive'}_copper_pad" in child.label)
        pad_box = pad.bounding_box()
        assert ((box.min.X + box.max.X) / 2.0,
                (box.min.Y + box.max.Y) / 2.0) == pytest.approx(
                    ((pad_box.min.X + pad_box.max.X) / 2.0,
                     (pad_box.min.Y + pad_box.max.Y) / 2.0))
        assert box.min.Y == pytest.approx(28.0)
        assert pad_box.max.Z == pytest.approx(27.85)


def test_shaft_wheel_lock_and_retainers_have_named_positive_retention():
    shaft = p10.build_shaft(80.0, P)
    assert (*shaft.bounding_box().min, *shaft.bounding_box().max) == pytest.approx(
        (-27.2, -12.0, 28.0, 31.6, -3.0, 37.0), abs=1e-7)
    wheel_raw = p10.build_wheel(0.0, "as_printed", P)
    wheel_seated = p10.build_wheel(0.0, "seated_envelope", P)
    assert (wheel_raw & p10.build_shaft(0.0, P)).volume > 0.0
    assert (wheel_seated & p10.build_shaft(0.0, P)).volume == pytest.approx(0.0, abs=1e-7)
    assert 31.6 - 26.0 == pytest.approx(5.6)
    assert 31.8 - 31.6 == pytest.approx(0.2)
    pin = p10.build_lock_pin(False, P)
    parked = p10.build_lock_pin(True, P)
    assert (pin.bounding_box().min.X, pin.bounding_box().max.X) == pytest.approx((15.0, 35.0))
    assert (parked.bounding_box().min.X, parked.bounding_box().max.X) == pytest.approx((35.0, 55.0))
    assert (pin & p10.build_wheel(80.0, "seated_envelope", P)).volume == pytest.approx(0.0, abs=1e-7)
    for name in p10.ROD_NAMES:
        point = p10.rod_center(name, 0.0, P)
        rod = p10.build_rod(name, 0.0, 0.0, P)
        left = p10.build_left_cap(point, 0.0, P)
        right = p10.build_right_keeper(point, 0.0, P)
        assert (rod & left).volume > 0.0
        assert (rod & right).volume == pytest.approx(0.0, abs=1e-7)
        assert right.bounding_box().min.X == pytest.approx(22.5)
        assert left.bounding_box().max.X == pytest.approx(-22.5)


def test_left_cam_thrust_boss_is_rooted_strong_and_clear():
    left_cam = p10.build_cam_disc("left", P)
    boss = (
        p10._x_cylinder(10.0, 0.25, -22.375, P.shaft_y, P.shaft_z)
        - p10._x_hex_prism(6.25, 0.35, -22.375, P.shaft_y, P.shaft_z)
    )
    cam_disc = p10._x_cylinder(
        P.scroll_diameter, P.scroll_plate_thickness,
        -P.scroll_plate_center_x, P.shaft_y, P.shaft_z,
    )
    assert left_cam.is_valid and len(left_cam.solids()) == 1
    assert _bounds(boss) == pytest.approx(
        (-22.50, -12.50, 27.50, -22.25, -2.50, 37.50), abs=1e-8)
    assert (boss - left_cam).volume == pytest.approx(0.0, abs=1e-8)
    assert _common_volume(boss, cam_disc) > 0.0
    assert 10.0 / 2.0 - 6.25 / 2.0 == pytest.approx(1.875)
    obstacles = [
        p10.build_fixed_disc("left", "seated_envelope", P),
        *p10.build_rods(P.end_angle, 0.0, P).children,
        p10.build_locator("seated_envelope", 0.0, P),
        *p10.build_fixed_L_workpiece().children,
    ]
    assert _all_clear(boss, obstacles)


def test_cycle15_shaft_stop_chain_and_neck_escape_are_exact():
    keeper = p10.build_shaft_keeper(P)
    shaft = p10.build_shaft(0.0, P)
    right_cam = p10.build_cam_disc("right", P)
    left_cam = p10.build_cam_disc("left", P)
    main = p10._x_hex_prism(6.0, 53.9, 4.65, P.shaft_y, P.shaft_z)
    neck_core = p10._x_cylinder(5.2, 3.5, -23.95, P.shaft_y, P.shaft_z)
    shoulder = p10._x_hex_prism(6.0, 1.6, -26.4, P.shaft_y, P.shaft_z)
    collar = p10._x_cylinder(9.0, 2.05, 23.475, P.shaft_y, P.shaft_z)
    assert (main.bounding_box().min.X, main.bounding_box().max.X) == pytest.approx((-22.30, 31.60))
    assert (neck_core.bounding_box().min.X, neck_core.bounding_box().max.X) == pytest.approx((-25.70, -22.20))
    assert (shoulder.bounding_box().min.X, shoulder.bounding_box().max.X) == pytest.approx((-27.20, -25.60))
    assert (collar.bounding_box().min.X, collar.bounding_box().max.X) == pytest.approx((22.45, 24.50))
    assert _common_volume(main, neck_core) > 0.0
    assert _common_volume(neck_core, shoulder) > 0.0

    # -X: the right collar is the unique stop at 0.15 mm. The main shaft is
    # still 0.05 mm clear of the C-keeper at that limit.
    assert _common_volume(Pos(-0.149999, 0.0, 0.0) * shaft, right_cam) == pytest.approx(0.0)
    assert (Pos(-0.149999, 0.0, 0.0) * shaft).distance_to(right_cam) > 0.0
    assert (Pos(-0.150000, 0.0, 0.0) * shaft).distance_to(right_cam) == pytest.approx(0.0, abs=1e-8)
    assert _common_volume(Pos(-0.150001, 0.0, 0.0) * shaft, right_cam) > 0.0
    assert (Pos(-0.15, 0.0, 0.0) * main).distance_to(keeper) == pytest.approx(0.05, abs=1e-8)

    # At zero the keeper may float anywhere over the 0.10-mm interval between
    # shoulder and boss without overlap.
    for keeper_x in (-0.10, -0.05, 0.0):
        floating = Pos(keeper_x, 0.0, 0.0) * keeper
        assert _common_volume(floating, shaft) == pytest.approx(0.0, abs=1e-8)
        assert _common_volume(floating, left_cam) == pytest.approx(0.0, abs=1e-8)

    # +X: shoulder -> keeper -> left-cam boss becomes a deterministic
    # three-face stack at +0.10 mm and overlaps immediately beyond it.
    assert (Pos(0.099999, 0.0, 0.0) * shoulder).distance_to(keeper) > 0.0
    assert (Pos(0.100000, 0.0, 0.0) * shoulder).distance_to(keeper) == pytest.approx(0.0, abs=1e-8)
    assert keeper.distance_to(left_cam) == pytest.approx(0.0, abs=1e-8)
    assert _common_volume(Pos(0.100001, 0.0, 0.0) * shoulder, keeper) > 0.0
    assert 0.15 + 0.10 == pytest.approx(0.25)
    assert min(3.0, 3.0 - 0.10) == pytest.approx(2.90)
    for dx in (-0.15, 0.0, 0.10):
        moved_shaft = Pos(dx, 0.0, 0.0) * shaft
        moved_wheel = Pos(dx, 0.0, 0.0) * p10.build_wheel(0.0, "as_printed", P)
        assert moved_shaft.bounding_box().max.X - moved_wheel.bounding_box().min.X == pytest.approx(5.6)

    assert 5.20 - 4.70 == pytest.approx(0.50)
    neck = p10._x_cylinder(5.20, 3.50, -23.95, P.shaft_y, P.shaft_z)
    escape_sweep = p10._straight_slot_solid_x(
        p10.PointYZ(P.shaft_y, P.shaft_z),
        p10.PointYZ(P.shaft_y + 5.50, P.shaft_z),
        5.20, -23.95, 3.50,
    )
    assert (escape_sweep & keeper).volume > 0.0
    for angle_index in range(17):
        angle = P.end_angle * angle_index / 16.0
        rotated_neck = p10._rotate_about_shaft(neck, angle, P)
        assert (rotated_neck - escape_sweep).volume == pytest.approx(0.0, abs=1e-8)
        for dy_index in range(1, 23):
            displaced = Pos(0.0, 5.50 * dy_index / 22.0, 0.0) * rotated_neck
            assert (displaced - escape_sweep).volume == pytest.approx(0.0, abs=1e-8)
            assert (displaced & keeper).volume > 0.0


def test_closed_wheel_contains_real_vertical_index_groove():
    groove = p10._rotate_about_shaft(p10._wheel_index_groove(P), P.end_angle, P)
    body = p10._rotate_about_shaft(
        p10._x_cylinder(32.0, 6.0, 29.0, P.shaft_y, P.shaft_z), P.end_angle, P)
    actual_cut = groove & body
    wheel = p10.build_wheel(P.end_angle, "as_printed", P)
    assert _bounds(groove) == pytest.approx((31.5, -7.9, 43.0, 32.1, -7.1, 48.0), abs=1e-8)
    assert tuple(actual_cut.bounding_box().size) == pytest.approx((0.5, 0.8, 5.0), abs=1e-8)
    assert (actual_cut.bounding_box().size.Z / actual_cut.bounding_box().size.Y) == pytest.approx(6.25)
    assert actual_cut.volume == pytest.approx(2.0, abs=1e-9)
    assert (groove & wheel).volume == pytest.approx(0.0, abs=1e-9)


def test_continuous_removal_envelopes_clear_every_stationary_member():
    plates = list(p10.build_principal_plates(0.0, "seated_envelope", 0.0, P).children)
    rods = list(p10.build_rods(0.0, 0.0, P).children)
    retainers = list(p10.build_retainers(0.0, 0.0, 0.0, P).children)
    common = [
        p10.build_base(P), *plates, p10.build_wheel(0.0, "seated_envelope", P),
        p10.build_shaft(0.0, P), p10.build_shaft_keeper(P), p10.build_lock_pin(True, P),
        p10.build_locator("seated_envelope", 80.0, P),
        *p10.build_electronics_reference().children, *p10.build_fixed_L_workpiece().children,
    ]
    for index, name in enumerate(p10.ROD_NAMES):
        sweep = p10.build_keeper_swept_volume(name, 0.0, P)
        others = [*common, *[rod for j, rod in enumerate(rods) if j != index],
                  *[retainer for j, retainer in enumerate(retainers) if j != 2 * index + 1]]
        assert _all_clear(sweep, others)
        assert (sweep & rods[index]).volume > 0.0  # declared elastic snap interval only
    removed = list(p10.build_retainers(0.0, -6.0, -55.0, P).children)
    for index, name in enumerate(p10.ROD_NAMES):
        sweep = p10.build_rod_cap_swept_volume(name, P)
        own_left = removed[2 * index]
        others = [*common, *[rod for j, rod in enumerate(rods) if j != index],
                  *[retainer for j, retainer in enumerate(removed) if j != 2 * index]]
        assert _all_clear(sweep, others)
        assert (sweep & own_left).volume > 0.0
    final_sweeps = p10.build_final_core_swept_volume(P)
    assert final_sweeps.is_valid and len(final_sweeps.children) == 16
    primitives = p10.build_final_core_moving_primitives(P)
    assert primitives.is_valid and len(primitives.children) == 16
    shoulder_primitives = [
        child for child in primitives.children if "tongue_shoulders" in child.label
    ]
    assert len(shoulder_primitives) == 2
    assert all((child.bounding_box().min.Y, child.bounding_box().max.Y)
               == pytest.approx((-16.8, 1.5)) for child in shoulder_primitives)
    base = p10.build_base(P)
    for side in ("left", "right"):
        fixed_insert = next(
            child for child in shoulder_primitives if side in child.label
        )
        seated_residuals = [
            rib - base
            for rib in (
                p10._outboard_rib(side, -11.0, P),
                p10._outboard_rib(side, -4.0, P),
                p10._rear_rib(side, -0.75, P),
                p10._rear_rib(side, 0.75, P),
            )
        ]
        assert len(seated_residuals) == 4
        assert all(residual.volume > 0.35 for residual in seated_residuals)
        assert all(_common_volume(residual, base) == pytest.approx(0.0, abs=1e-8)
                   for residual in seated_residuals)
        assert all((residual - fixed_insert).volume == pytest.approx(0.0, abs=1e-8)
                   for residual in seated_residuals)
        _, tongue, shoulders = p10._fixed_disc_core(side, P)
        exact_insert = p10._fuse([tongue, *shoulders, *seated_residuals])
        assert _brep_symmetric_difference_volume(
            fixed_insert, exact_insert) == pytest.approx(0.0, abs=1e-8)
    for primitive, envelope in zip(primitives.children, final_sweeps.children):
        parked = Pos(0.0, P.assembly_remove_y, 0.0) * primitive
        assert (primitive - envelope).volume == pytest.approx(0.0, abs=1e-7)
        assert (parked - envelope).volume == pytest.approx(0.0, abs=1e-7)

    # Prove that the declared primitives cover the complete production moving
    # subset, including all eight seated crush-rib remnants, both before and
    # after the final -Y translation.  This closes the gap that a primitive can
    # fit its own sweep while still omitting a feature from the real part.
    declared_union = p10._fuse(list(primitives.children))
    actual_start = [
        p10.build_base(P),
        *p10.build_principal_plates(0.0, "seated_envelope", 0.0, P).children,
        p10.build_shaft(0.0, P), p10.build_shaft_keeper(P),
        p10.build_wheel(0.0, "seated_envelope", P),
    ]
    assert all((part - declared_union).volume == pytest.approx(0.0, abs=1e-7)
               for part in actual_start)
    declared_parked = Pos(0.0, P.assembly_remove_y, 0.0) * declared_union
    actual_parked = [Pos(0.0, P.assembly_remove_y, 0.0) * part for part in actual_start]
    assert all((part - declared_parked).volume == pytest.approx(0.0, abs=1e-7)
               for part in actual_parked)

    primitive_by_name = {
        child.label.removeprefix("final_core_moving_primitive_"): child
        for child in primitives.children
    }
    envelope_by_name = {
        name: envelope
        for (name, _, _), envelope in zip(
            p10._final_core_proof_features(P), final_sweeps.children)
    }
    plate_start = actual_start[1:5]
    named_actual_parts = (
        ("base", actual_start[0], ("base_outer",)),
        ("left_fixed", plate_start[0], (
            "left_fixed_disc_outer", "left_fixed_stop_arm_outer",
            "left_fixed_tongue_shoulders_outer", "left_fixed_stop_pin_outer",
        )),
        ("left_cam", plate_start[1], (
            "left_cam_disc_outer", "left_cam_tab_outer",
        )),
        ("right_fixed", plate_start[2], (
            "right_fixed_disc_outer", "right_fixed_stop_arm_outer",
            "right_fixed_tongue_shoulders_outer", "right_fixed_stop_pin_outer",
        )),
        ("right_cam", plate_start[3], (
            "right_cam_disc_outer", "right_cam_tab_outer",
        )),
        ("shaft", actual_start[5], ("shaft_complete",)),
        ("keeper", actual_start[6], ("shaft_keeper_complete",)),
        ("wheel", actual_start[7], ("wheel_outer",)),
    )
    assert len(named_actual_parts) == 8
    for _, actual_part, feature_names in named_actual_parts:
        matching_primitives = p10._fuse([
            primitive_by_name[name] for name in feature_names
        ])
        matching_envelopes = p10._fuse([
            envelope_by_name[name] for name in feature_names
        ])
        parked_part = Pos(0.0, P.assembly_remove_y, 0.0) * actual_part
        assert (actual_part - matching_primitives).volume == pytest.approx(
            0.0, abs=1e-7)
        assert (actual_part - matching_envelopes).volume == pytest.approx(
            0.0, abs=1e-7)
        assert (parked_part - matching_envelopes).volume == pytest.approx(
            0.0, abs=1e-7)

    stationary = [
        p10.build_lock_pin(True, P), p10.build_locator("seated_envelope", 80.0, P),
        *p10.build_rods(0.0, -55.0, P).children, *removed,
        *p10.build_electronics_reference().children, *p10.build_fixed_L_workpiece().children,
    ]
    assert all(_all_clear(envelope, stationary) for envelope in final_sweeps.children)
    intact_locator = p10.build_locator("seated_envelope", 0.0, P)
    assert sum((envelope & intact_locator).volume for envelope in final_sweeps.children) > 300.0


def test_sequential_keeper_and_rod_removal_all_endpoint_orders_are_clear():
    rods_initial = list(p10.build_rods(0.0, 0.0, P).children)
    rods_parked = list(p10.build_rods(0.0, P.rod_withdraw_x, P).children)
    retainers_initial = list(p10.build_retainers(0.0, 0.0, 0.0, P).children)
    retainers_parked = list(p10.build_retainers(
        0.0, P.keeper_travel_y, P.rod_withdraw_x, P).children)
    structural = [
        p10.build_base(P),
        *p10.build_principal_plates(0.0, "seated_envelope", 0.0, P).children,
        p10.build_wheel(0.0, "seated_envelope", P), p10.build_shaft(0.0, P),
        p10.build_shaft_keeper(P), p10.build_lock_pin(True, P),
        p10.build_locator("seated_envelope", P.locator_park_x, P),
        *p10.build_electronics_reference().children, *p10.build_fixed_L_workpiece().children,
    ]
    # During each keeper removal, every other keeper may independently be at
    # its initial or parked endpoint; all rods and left caps remain initial.
    for moving_index, name in enumerate(p10.ROD_NAMES):
        sweep = p10.build_keeper_swept_volume(name, 0.0, P)
        obstacles = [*structural]
        for other_index in range(3):
            if other_index != moving_index:
                obstacles.append(rods_initial[other_index])
            obstacles.append(retainers_initial[2 * other_index])
            if other_index != moving_index:
                obstacles.extend((
                    retainers_initial[2 * other_index + 1],
                    retainers_parked[2 * other_index + 1],
                ))
        assert _all_clear(sweep, obstacles)
        assert (sweep & rods_initial[moving_index]).volume > 0.0

    # During each rod+cap withdrawal, every other pair may independently be at
    # either endpoint and every right keeper is already parked.
    parked_right_keepers = [retainers_parked[2 * index + 1] for index in range(3)]
    for moving_index, name in enumerate(p10.ROD_NAMES):
        sweep = p10.build_rod_cap_swept_volume(name, P)
        obstacles = [*structural, *parked_right_keepers]
        for other_index in range(3):
            if other_index == moving_index:
                continue
            obstacles.extend((
                rods_initial[other_index], rods_parked[other_index],
                retainers_initial[2 * other_index], retainers_parked[2 * other_index],
            ))
        assert _all_clear(sweep, obstacles)


def test_lock_pin_continuous_sweep_clears_every_named_member():
    sweep = p10.build_lock_pin_swept_volume(P)
    members = [
        p10.build_base(P), *p10.build_principal_plates(80.0, "seated_envelope", 0.0, P).children,
        *p10.build_rods(80.0, 0.0, P).children, *p10.build_retainers(80.0, 0.0, 0.0, P).children,
        p10.build_shaft(80.0, P), p10.build_shaft_keeper(P),
        p10.build_wheel(80.0, "seated_envelope", P), p10.build_locator("seated_envelope", 0.0, P),
        *p10.build_electronics_reference().children, *p10.build_fixed_L_workpiece().children,
    ]
    assert _all_clear(sweep, members)


def test_safe_cached_prototypes_survive_100_mutated_public_copies():
    prototype = p10._cam_disc_prototype("right", P)
    original = (prototype.label, prototype.volume, (*prototype.bounding_box().min, *prototype.bounding_box().max), id(prototype.wrapped))
    for index in range(100):
        candidate = p10.build_cam_disc("right", P)
        candidate.label = f"mutated_{index}"
        candidate.color = None
        moved = Pos(float(index), 0.0, 0.0) * candidate
        assert moved is not prototype
    assert (prototype.label, prototype.volume, (*prototype.bounding_box().min, *prototype.bounding_box().max), id(prototype.wrapped)) == original


def test_fit_coupon_and_print_kit_have_exact_printed_part_contract():
    coupon = p10.build_fit_coupon(P)
    assert coupon.is_valid and len(coupon.children) == len(coupon.solids()) == 2
    ladder, plug = coupon.children
    assert "6p15_6p25_6p35" in ladder.label
    assert "marks_at_3p0_and_5p6" in plug.label
    kit = p10.build_print_kit(P)
    assert kit.is_valid and len(kit.children) == len(kit.solids()) == 18
    assert len({child.label for child in kit.children}) == 18
    assert all(child.is_valid and len(child.solids()) == 1 and child.volume > 0.0 for child in kit.children)
    assert all(child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7) for child in kit.children)
    principal_sources = (
        (p10.build_fixed_disc("left", "as_printed", P),
         -P.fixed_plate_center_x + P.fixed_plate_thickness / 2.0),
        (p10.build_fixed_disc("right", "as_printed", P),
         P.fixed_plate_center_x - P.fixed_plate_thickness / 2.0),
        (p10.build_cam_disc("left", P),
         -P.scroll_plate_center_x + P.scroll_plate_thickness / 2.0),
        (p10.build_cam_disc("right", P),
         P.scroll_plate_center_x - P.scroll_plate_thickness / 2.0),
    )
    for printed, (source, inboard_x) in zip(kit.children[:4], principal_sources):
        expected_face = _planar_face_area(source, "X", inboard_x)
        bed_footprint = _planar_face_area(printed, "Z", 0.0)
        assert expected_face > 2800.0
        assert bed_footprint == pytest.approx(expected_face, abs=1e-5)
    # The outboard stop pins and new left thrust boss project upward, never
    # become point/edge support beneath the full inboard disc face.
    assert kit.children[0].bounding_box().size.Z > P.fixed_plate_thickness
    assert kit.children[1].bounding_box().size.Z > P.fixed_plate_thickness
    assert kit.children[2].bounding_box().size.Z == pytest.approx(3.20, abs=1e-7)
    assert kit.children[3].bounding_box().size.Z == pytest.approx(3.00, abs=1e-7)
    assert all("purchased" not in child.label and "reference" not in child.label for child in kit.children)
    for index, first in enumerate(kit.children):
        assert all((first & second).volume == pytest.approx(0.0, abs=1e-7) for second in kit.children[index + 1:])


def test_all_named_phase_assemblies_are_valid_and_keep_same_workpiece():
    assemblies = (
        p10.build_loaded_open(P), p10.build_loaded_closed(P),
        p10.build_locator_removed_closed(P), p10.build_rods_withdrawn(P),
        p10.build_removal_clear(P), p10.build_exploded(P),
    )
    embedded_workpieces = []
    for assembly in assemblies:
        assert assembly.is_valid and len(assembly.solids()) == 30
        labels = [child.label for child in assembly.children]
        assert sum("fixed_90deg_pigtail" in label for label in labels) == 1
        assert sum("exactly_three_rods" in label for label in labels) == 0  # rods are flattened as three named children
        embedded_workpieces.append(next(
            child for child in assembly.children if "fixed_90deg_pigtail" in child.label
        ))

    # Compare the actual embedded child from every phase pair.  A rebuilt
    # standalone workpiece on both sides would be tautological and would not
    # detect a phase-specific transform or substitution.
    for first, second in combinations(embedded_workpieces, 2):
        assert first.label == second.label
        assert [child.label for child in first.children] == [
            child.label for child in second.children
        ]
        assert _bounds(first) == pytest.approx(_bounds(second), abs=1e-7)
        assert _solid_volume(first) == pytest.approx(_solid_volume(second), abs=1e-7)
        assert _brep_symmetric_difference_volume(first, second) == pytest.approx(
            0.0, abs=1e-7)
        for first_child, second_child in zip(first.children, second.children):
            assert _bounds(first_child) == pytest.approx(_bounds(second_child), abs=1e-7)
            assert _solid_volume(first_child) == pytest.approx(
                _solid_volume(second_child), abs=1e-7)
            assert _brep_symmetric_difference_volume(
                first_child, second_child) == pytest.approx(0.0, abs=1e-7)


def test_fresh_process_source_build_is_repeatable():
    code = """
import json
import xt60_bend_jig.p10_practical_four_disc_clamp as p
s=p.build_loaded_closed()
print(json.dumps({'solids':len(s.solids()),'bbox':[round(v,7) for v in (*s.bounding_box().min,*s.bounding_box().max)],'labels':[c.label for c in s.children]},sort_keys=True))
"""
    first = subprocess.check_output([sys.executable, "-c", code], cwd=PROJECT, text=True)
    second = subprocess.check_output([sys.executable, "-c", code], cwd=PROJECT, text=True)
    assert first == second


def test_generated_steps_match_source_labels_counts_and_bounds_when_present():
    cases = (
        ("p10_loaded_open.step", p10.build_loaded_open()),
        ("p10_loaded_closed.step", p10.build_loaded_closed()),
        ("p10_locator_removed_closed.step", p10.build_locator_removed_closed()),
        ("p10_rods_withdrawn.step", p10.build_rods_withdrawn()),
        ("p10_removal_clear.step", p10.build_removal_clear()),
        ("p10_exploded.step", p10.build_exploded()),
        ("p10_print_kit.step", p10.build_print_kit()),
        ("p10_fit_coupon.step", p10.build_fit_coupon()),
    )
    if not all((OUT / filename).exists() for filename, _ in cases):
        pytest.skip("P10 STEP artifacts not generated yet")
    for filename, source in cases:
        imported = import_step(OUT / filename)
        assert imported.is_valid
        assert len(imported.solids()) == len(source.solids())
        assert _bounds(imported) == pytest.approx(_bounds(source), abs=1e-6)
        assert imported.label == source.label
        assert [child.label for child in imported.children] == [child.label for child in source.children]
        assert len(imported.children) == len(source.children)
        for imported_child, source_child in zip(imported.children, source.children):
            assert _bounds(imported_child) == pytest.approx(_bounds(source_child), abs=1e-6)
            assert _solid_volume(imported_child) == pytest.approx(
                _solid_volume(source_child), rel=1e-9, abs=1e-6)
            assert _brep_symmetric_difference_volume(
                imported_child, source_child) == pytest.approx(0.0, abs=2e-5)
        if filename not in ("p10_print_kit.step", "p10_fit_coupon.step"):
            imported_workpiece = next(
                child for child in imported.children
                if "fixed_90deg_pigtail" in child.label
            )
            source_workpiece = next(
                child for child in source.children
                if "fixed_90deg_pigtail" in child.label
            )
            assert imported_workpiece.label == source_workpiece.label
            assert [child.label for child in imported_workpiece.children] == [
                child.label for child in source_workpiece.children
            ]
            for imported_child, source_child in zip(
                imported_workpiece.children, source_workpiece.children
            ):
                assert _bounds(imported_child) == pytest.approx(
                    _bounds(source_child), abs=1e-6)
                assert _solid_volume(imported_child) == pytest.approx(
                    _solid_volume(source_child), abs=1e-6)
                assert _brep_symmetric_difference_volume(
                    imported_child, source_child) == pytest.approx(0.0, abs=2e-5)

    imported_closed = import_step(OUT / "p10_loaded_closed.step")
    closed_by_label = {child.label: child for child in imported_closed.children}
    imported_rods = [closed_by_label[f"purchased_304_stainless_{name}_rod_4x50"]
                     for name in p10.ROD_NAMES]
    for name, rod in zip(p10.ROD_NAMES, imported_rods):
        center = p10.rod_center(name, P.end_angle, P)
        bbox = rod.bounding_box()
        assert ((bbox.min.Y + bbox.max.Y) / 2.0,
                (bbox.min.Z + bbox.max.Z) / 2.0) == pytest.approx((center.y, center.z), abs=1e-6)
    left_fixed = closed_by_label["left_fixed_disc_integral_stop_tongue_crush_ribs_seated_envelope"]
    left_cam = closed_by_label[
        "left_cam_disc_three_inverse_slots_integral_80deg_stop_tab_thrust_boss_10OD_Xm22p50_to_m22p25"
    ]
    assert left_fixed.distance_to(left_cam) == pytest.approx(0.0, abs=1e-7)
    overlap = left_fixed & left_cam
    assert overlap is None or overlap.volume == pytest.approx(0.0, abs=1e-7)
    overtravel = p10._rotate_about_shaft(left_cam, 0.10, P)
    assert _common_volume(left_fixed, overtravel) >= 0.09
    imported_shaft = closed_by_label[
        "shared_keyed_shaft_right_collar_left_round_neck_terminal_shoulder_80deg"
    ]
    assert _bounds(imported_shaft) == pytest.approx(
        (-27.2, -12.0, 28.0, 31.6, -3.0, 37.0), abs=1e-6)
    imported_pin = closed_by_label["lengthened_lock_pin_engaged_xshift_0"]
    lock = p10.lock_world_point(P)
    pin_box = imported_pin.bounding_box()
    assert ((pin_box.min.Y + pin_box.max.Y) / 2.0,
            (pin_box.min.Z + pin_box.max.Z) / 2.0) == pytest.approx(
                (lock.y, lock.z), abs=1e-6)
    assert _common_volume(imported_pin, left_fixed) == pytest.approx(0.0, abs=1e-7)
    assert _common_volume(imported_pin, left_cam) == pytest.approx(0.0, abs=1e-7)
    imported_wheel = closed_by_label[
        "removable_thumbwheel_notched_indexed_socket_ribs_seated_envelope_80deg"
    ]
    closed_groove = p10._rotate_about_shaft(
        p10._wheel_index_groove(P), P.end_angle, P)
    groove_overlap = imported_wheel & closed_groove
    assert groove_overlap is None or groove_overlap.volume == pytest.approx(0.0, abs=1e-7)
    workpiece = closed_by_label["fixed_90deg_pigtail_two_5mm_stripped_conductors_XT60"]
    for rod in imported_rods:
        assert rod.distance_to(workpiece) <= 0.02
        overlap = rod & workpiece
        assert overlap is None or overlap.volume == pytest.approx(0.0, abs=1e-7)

    imported_access = import_step(OUT / "p10_locator_removed_closed.step")
    access_structural = [
        child for child in imported_access.children
        if "ESC_FC" not in child.label and "pigtail" not in child.label
    ]
    assert _all_clear(p10.build_solder_access_corridor(P), access_structural)
