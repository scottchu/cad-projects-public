"""Deterministic CAD acceptance for P9's minimal four-disc motion proof."""

from __future__ import annotations

import json
from functools import lru_cache
from math import hypot
from pathlib import Path
import subprocess
import sys

import pytest
from build123d import Align, Box, Pos, import_step

import xt60_bend_jig.p9_four_disc_three_rod as p9
from xt60_bend_jig.p2_corner_clamp import build_wire_centerline


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "cad" / "p9_four_disc_three_rod"
ROD_NAMES = p9.ROD_NAMES


def _point_segment_distance(point, first, second):
    dy, dz = second.y - first.y, second.z - first.z
    denom = dy * dy + dz * dz
    t = max(0.0, min(1.0, ((point.y - first.y) * dy + (point.z - first.z) * dz) / denom))
    return hypot(point.y - (first.y + t * dy), point.z - (first.z + t * dz))


def _printed_parts(angle):
    fixed_left, cam_left, fixed_right, cam_right = _plate_bases()
    parts = [
        fixed_left,
        p9._rotate_about_shaft(cam_left, angle, p9.P9_DEFAULTS),
        fixed_right,
        p9._rotate_about_shaft(cam_right, angle, p9.P9_DEFAULTS),
    ]
    parts.extend(p9.build_caps(angle).children)
    parts.append(p9.build_keyed_shaft(angle))
    if angle == 80.0:
        parts.append(p9.build_lock_pin())
    return parts


@lru_cache(maxsize=1)
def _plate_bases():
    return (
        p9.build_fixed_disc("left"), p9.build_cam_disc("left"),
        p9.build_fixed_disc("right"), p9.build_cam_disc("right"),
    )


def test_measured_diameter_exception_and_axial_stack_are_frozen():
    p = p9.P9_DEFAULTS
    assert (p.rod_diameter, p.rod_length) == pytest.approx((4.0, 50.0))
    assert (p.shaft_y, p.shaft_z, p.scroll_diameter) == pytest.approx((-7.5, 32.5, 64.0))
    assert (p.fixed_plate_thickness, p.scroll_plate_thickness, p.scroll_axial_clearance) == pytest.approx((3.0, 2.5, 0.30))
    assert p.clear_span == pytest.approx(32.0)
    assert p.scroll_plate_center_x - p.scroll_plate_thickness / 2.0 - p.fixed_plate_outer_x == pytest.approx(0.30)
    assert p.rod_projection == pytest.approx(3.2)


def test_401_pose_common_travel_and_exact_70_to_80_dwell():
    p = p9.P9_DEFAULTS
    travels = [p9.travel_at_angle(p.end_angle * i / 400.0, p) for i in range(401)]
    assert travels[0] == pytest.approx(0.0)
    assert travels[-1] == pytest.approx(11.0)
    assert all(a <= b + 1e-12 for a, b in zip(travels, travels[1:]))
    for name in ROD_NAMES:
        closed = p9.rod_center(name, 70.0, p)
        assert all(p9.rod_center(name, 70.0 + i / 20.0, p) == closed for i in range(201))


def test_inverse_slots_reconstruct_801_followers_within_0p02mm():
    p = p9.P9_DEFAULTS
    for name in ROD_NAMES:
        polyline = p9.slot_path(name, p)
        worst = 0.0
        for i in range(801):
            q = p9.inverse_slot_point(name, p.end_angle * i / 800.0, p)
            worst = max(worst, min(_point_segment_distance(q, a, b) for a, b in zip(polyline, polyline[1:])))
        assert worst <= 0.02


def test_dense_cam_slot_edge_web_and_hub_web_measurements_pass():
    p = p9.P9_DEFAULTS
    paths = {
        name: [p9.inverse_slot_point(name, p.end_angle * i / 1600.0, p) for i in range(1601)]
        for name in ROD_NAMES
    }
    max_radius = max(hypot(q.y - p.shaft_y, q.z - p.shaft_z) for points in paths.values() for q in points)
    min_edge = p.scroll_diameter / 2.0 - max_radius - p.scroll_slot_width / 2.0
    assert max_radius == pytest.approx(26.3015683943, abs=2e-6)
    assert min_edge >= 3.498
    minimum_separation = float("inf")
    for i, first_name in enumerate(ROD_NAMES):
        for second_name in ROD_NAMES[i + 1:]:
            for first in paths[first_name]:
                minimum_separation = min(
                    minimum_separation,
                    min(hypot(first.y - second.y, first.z - second.z) for second in paths[second_name]),
                )
    assert minimum_separation - p.scroll_slot_width >= 2.014
    min_radius = min(hypot(q.y - p.shaft_y, q.z - p.shaft_z) for points in paths.values() for q in points)
    hub_web = min_radius - p.scroll_slot_width / 2.0 - p.scroll_hex_socket_across_corners / 2.0
    assert hub_web >= 4.225


def test_exactly_four_plain_plate_solids_and_three_4x50_rods():
    plates = _plate_bases()
    rods = p9.build_rods(0.0)
    assert len(plates) == 4
    assert len(rods.children) == 3
    assert all(part.is_valid and len(part.solids()) == 1 and part.volume > 0 for part in plates)
    assert all((*rod.bounding_box().size,) == pytest.approx((50.0, 4.0, 4.0), abs=1e-7) for rod in rods.children)
    assert sum("fixed_plain_circular_guide_disc" in part.label for part in plates) == 2
    assert sum("rotating_plain_circular_cam_disc" in part.label for part in plates) == 2
    assert all("spider" not in part.label and "frame" not in part.label for part in plates)


def test_actual_cam_slot_tools_have_separate_web_and_clear_keyed_socket():
    p = p9.P9_DEFAULTS
    tools = [p9.build_cam_slot_tool(name, "right", p) for name in ROD_NAMES]
    for i, first in enumerate(tools):
        for second in tools[i + 1:]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)
            assert first.distance_to(second) >= 2.0
    socket = p9._x_hex_prism(
        p.scroll_hex_socket_across_corners, p.scroll_plate_thickness + 2.0,
        p.scroll_plate_center_x, p.shaft_y, p.shaft_z,
    )
    for tool in tools:
        assert (tool & socket).volume == pytest.approx(0.0, abs=1e-7)
        assert tool.distance_to(socket) >= 2.0


def test_42_off_grid_actual_brep_poses_clear_all_slotted_plates_and_each_other():
    fixed_left, cam_left, fixed_right, cam_right = _plate_bases()
    # 1,3,...79 degrees fall between the 2-degree slot-construction nodes.
    # Endpoints are added explicitly, so this is not a self-confirming sweep.
    for angle in (0.0, *(float(i) for i in range(1, 80, 2)), 80.0):
        plates = [
            fixed_left, p9._rotate_about_shaft(cam_left, angle, p9.P9_DEFAULTS),
            fixed_right, p9._rotate_about_shaft(cam_right, angle, p9.P9_DEFAULTS),
        ]
        rods = list(p9.build_rods(angle).children)
        for rod in rods:
            assert all((rod & plate).volume == pytest.approx(0.0, abs=1e-7) for plate in plates)
        for j, first in enumerate(rods):
            assert all((first & second).volume == pytest.approx(0.0, abs=1e-7) for second in rods[j + 1:])


def test_both_cam_discs_are_identical_and_share_exact_keyed_pose():
    p = p9.P9_DEFAULTS
    _, left, _, right = _plate_bases()
    assert left.volume == pytest.approx(right.volume, abs=1e-7)
    assert (*left.bounding_box().size,) == pytest.approx((*right.bounding_box().size,), abs=1e-7)
    for angle in (0.0, 23.0, 70.0, 80.0):
        shaft = p9.build_keyed_shaft(angle, p)
        for base in (left, right):
            cam = p9._rotate_about_shaft(base, angle, p)
            assert (shaft & cam).volume == pytest.approx(0.0, abs=1e-7)
            wrong = p9.build_keyed_shaft(angle + 30.0, p)
            assert (wrong & cam).volume > 1.0


def test_single_index_pin_fits_only_exact_80_degree_pose_and_is_only_lock():
    p = p9.P9_DEFAULTS
    pin = p9.build_lock_pin(p)
    fixed = p9.build_fixed_disc("right", p)
    assert pin.distance_to(fixed) == pytest.approx(0.1, abs=1e-7)
    base = _plate_bases()[3]
    at_end = p9._rotate_about_shaft(base, 80.0, p)
    before = p9._rotate_about_shaft(base, 79.0, p)
    assert pin.distance_to(at_end) == pytest.approx(0.1, abs=1e-7)
    assert (pin & at_end).volume == pytest.approx(0.0, abs=1e-7)
    assert (pin & before).volume > 0.5
    kit = p9.build_print_kit(p)
    assert sum("lock_pin" in child.label for child in kit.children) == 1


def test_open_xt60_removal_corridor_is_clear_of_all_hardware():
    corridor = Pos(0.0, 0.0, 67.0) * Box(
        16.5, 8.5, 66.0, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    hardware = [*_printed_parts(0.0), *p9.build_rods(0.0).children]
    assert all((part & corridor).volume == pytest.approx(0.0, abs=1e-7) for part in hardware)
    assert p9.build_keyed_shaft(0.0).distance_to(corridor) >= 0.25
    xt60 = p9.build_open_xt60_removal_reference()
    assert (xt60 & corridor).volume == pytest.approx(xt60.volume, abs=1e-7)


def test_closed_wire_is_44mm_R6_and_exactly_90_degrees_with_clear_solder_approach():
    centerline = build_wire_centerline()
    edges = list(centerline.edges())
    assert centerline.length == pytest.approx(44.0)
    horizontal, vertical = edges[0].tangent_at(0.5), edges[-1].tangent_at(0.5)
    assert tuple(horizontal) == pytest.approx((0.0, -1.0, 0.0))
    assert tuple(vertical) == pytest.approx((0.0, 0.0, 1.0))
    assert horizontal.dot(vertical) == pytest.approx(0.0, abs=1e-12)
    assert p9.rod_center("upright", 70.0) == p9.rod_center("upright", 80.0)
    corridor = Pos(0.0, 47.0, 32.925) * Box(
        20.0, 46.0, 10.15, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    assert all((part & corridor).volume == pytest.approx(0.0, abs=1e-7) for part in _printed_parts(80.0))


def test_print_kit_has_only_twelve_named_printed_parts_on_bed_without_overlap():
    kit = p9.build_print_kit()
    assert kit.is_valid and len(kit.children) == 12 and len(kit.solids()) == 12
    assert len({child.label for child in kit.children}) == 12
    assert all(child.is_valid and len(child.solids()) == 1 and child.volume > 0 for child in kit.children)
    assert all(child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7) for child in kit.children)
    assert all("purchased" not in child.label and "reference" not in child.label for child in kit.children)
    for i, first in enumerate(kit.children):
        assert all((first & second).volume == pytest.approx(0.0, abs=1e-7) for second in kit.children[i + 1:])


def test_fresh_process_source_build_is_repeatable():
    code = """
import json
import xt60_bend_jig.p9_four_disc_three_rod as p9
s=p9.build_loaded_closed()
print(json.dumps({'solids':len(s.solids()),'bbox':[round(v,7) for v in (*s.bounding_box().min,*s.bounding_box().max)],'labels':[c.label for c in s.children]},sort_keys=True))
"""
    first = subprocess.check_output([sys.executable, "-c", code], cwd=PROJECT, text=True)
    second = subprocess.check_output([sys.executable, "-c", code], cwd=PROJECT, text=True)
    assert json.loads(first) == json.loads(second)


def test_generated_steps_match_source_labels_and_bounds_when_present():
    filenames = (
        "p9_loaded_open.step", "p9_loaded_closed.step",
        "p9_exploded.step", "p9_print_kit.step",
    )
    if not all((OUT / filename).exists() for filename in filenames):
        pytest.skip("P9 STEP artifacts not generated yet")
    cases = (
        ("p9_loaded_open.step", p9.build_loaded_open()),
        ("p9_loaded_closed.step", p9.build_loaded_closed()),
        ("p9_exploded.step", p9.build_exploded()),
        ("p9_print_kit.step", p9.build_print_kit()),
    )
    for filename, source in cases:
        imported = import_step(OUT / filename)
        assert len(imported.solids()) == len(source.solids())
        assert (*imported.bounding_box().min, *imported.bounding_box().max) == pytest.approx(
            (*source.bounding_box().min, *source.bounding_box().max), abs=1e-7)
        assert imported.label == source.label
