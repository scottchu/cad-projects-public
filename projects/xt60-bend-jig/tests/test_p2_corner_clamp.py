"""Analytic and BREP acceptance tests for the mirrored P2 corner clamp."""

from __future__ import annotations

from math import pi, sqrt
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Cylinder, Pos, import_step

from xt60_bend_jig.p2_corner_clamp import (
    P2_DEFAULTS,
    P2Parameters,
    PointYZ,
    build_esc,
    build_fc,
    build_fixed_plate,
    build_loaded_closed,
    build_loaded_open,
    build_print_kit,
    build_pusher,
    build_reference_rod,
    build_rods,
    build_wire,
    build_wire_centerline,
    build_wires,
    build_xt60,
    contact_points,
    rod_centers,
)


def _x_probe(diameter: float, length: float, x: float, point: PointYZ):
    return Pos(x, point.y, point.z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def test_p2_is_explicitly_12awg_only():
    with pytest.raises(ValueError, match="12 AWG only"):
        P2Parameters(wire_gauge=14)


def test_mirrored_wire_math_is_exact_44mm_R6_quarter_circle():
    p = P2_DEFAULTS
    assert p.wire_radius == pytest.approx(2.15)
    assert p.rod_radius == pytest.approx(2.0)
    assert p.rho == pytest.approx(4.15)
    assert p.horizontal_length == pytest.approx(22.0)
    assert p.arc_length == pytest.approx(pi * 6.0 / 2.0)
    assert p.vertical_length == pytest.approx(44.0 - 22.0 - pi * 6.0 / 2.0)
    assert p.vertical_endpoint_z == pytest.approx(48.575222039)
    assert build_wire_centerline().length == pytest.approx(44.0)


def test_frozen_rod_and_contact_coordinates_match_contract():
    rods = rod_centers()
    contacts = contact_points()
    assert rods["bottom"] == PointYZ(12.0, 25.85)
    assert rods["left"] == PointYZ(-4.15, 42.0)
    assert rods["moving"].y == pytest.approx(4.691852455)
    assert rods["moving"].z == pytest.approx(34.691852455)
    assert contacts["moving"].y == pytest.approx(1.757359313)
    assert contacts["moving"].z == pytest.approx(31.757359313)
    assert P2_DEFAULTS.moving_open.y == pytest.approx(12.470027048)
    assert P2_DEFAULTS.moving_open.z == pytest.approx(42.470027048)


def test_all_three_side_profile_contacts_are_exact_zero_gap():
    p = P2_DEFAULTS
    rods = rod_centers()
    contacts = contact_points()
    for name in ("bottom", "left", "moving"):
        assert rods[name].distance_to(contacts[name]) == pytest.approx(p.rho)


@pytest.mark.parametrize("wire_x", (-4.0, 4.0))
def test_actual_brep_has_six_tangent_rod_wire_contacts_without_overlap(wire_x):
    wire = build_wire(wire_x, "#FFFFFF")
    for name, center in rod_centers().items():
        rod = build_reference_rod(name, center)
        assert rod.distance_to(wire) == pytest.approx(0.0, abs=1.1e-7)
        assert (rod & wire).volume == pytest.approx(0.0, abs=1e-7)


def test_moving_contact_normal_is_parallel_to_down_left_close_vector():
    q = contact_points()["moving"]
    m = rod_centers()["moving"]
    normal = (q.y - m.y, q.z - m.z)
    close = (-P2_DEFAULTS.withdrawal_component, -P2_DEFAULTS.withdrawal_component)
    cross = normal[0] * close[1] - normal[1] * close[0]
    dot = normal[0] * close[0] + normal[1] * close[1]
    assert cross == pytest.approx(0.0, abs=1e-9)
    assert dot > 0.0


@pytest.mark.parametrize("side", ("left", "right"))
def test_each_large_L_has_exactly_two_4p3_coaxial_bores(side):
    p = P2_DEFAULTS
    plate = build_fixed_plate(side)
    x = (-1.0 if side == "left" else 1.0) * p.plate_center_x
    for name in ("left", "bottom"):
        center = rod_centers()[name]
        assert (plate & _x_probe(4.3, 6.0, x, center)).volume == pytest.approx(0.0, abs=1e-7)
        assert (plate & _x_probe(4.32, 3.0, x, center)).volume > 0.0
    cylindrical = [face for face in plate.faces() if face.geom_type.name == "CYLINDER"]
    assert len(cylindrical) == 2


def test_each_small_L_has_exactly_one_4p3_bore_on_shared_axis():
    p = P2_DEFAULTS
    pusher = build_pusher()
    moving = rod_centers()["moving"]
    for sign in (-1.0, 1.0):
        x = sign * p.plate_center_x
        assert (pusher & _x_probe(4.3, 6.0, x, moving)).volume == pytest.approx(0.0, abs=1e-7)
        assert (pusher & _x_probe(4.32, 3.0, x, moving)).volume > 0.0
    cylindrical = [face for face in pusher.faces() if face.geom_type.name == "CYLINDER"]
    assert len(cylindrical) == 2
    assert pusher.is_valid and len(pusher.solids()) == 1


def test_exactly_three_reference_rods_are_4x50():
    rods = build_rods()
    assert len(rods.children) == 3
    for rod in rods.children:
        bounds = rod.bounding_box()
        assert bounds.size.X == pytest.approx(50.0)
        assert bounds.size.Y == pytest.approx(4.0)
        assert bounds.size.Z == pytest.approx(4.0)


def test_both_closed_hard_stops_touch_and_overtravel_interferes_each_axis():
    plate = build_fixed_plate("left")
    pusher = build_pusher()
    assert plate.distance_to(pusher) == pytest.approx(0.0, abs=1e-7)
    assert (plate & pusher).volume == pytest.approx(0.0, abs=1e-7)
    assert (plate & (Pos(0.0, -0.01, 0.0) * pusher)).volume > 0.0
    assert (plate & (Pos(0.0, 0.0, -0.01) * pusher)).volume > 0.0


def test_open_stop_gaps_are_exactly_7p778_in_Y_and_Z():
    p = P2_DEFAULTS
    d = p.withdrawal_component
    opened = Pos(0.0, d, d) * build_pusher()
    bounds = opened.bounding_box()
    assert bounds.min.Y - p.stop_y == pytest.approx(d)
    assert bounds.min.Z - p.stop_z == pytest.approx(d)


def test_full_101_point_pusher_and_rod_sweep_is_collision_free():
    p = P2_DEFAULTS
    pusher = build_pusher()
    fixed_plates = build_fixed_plate("left") + build_fixed_plate("right")
    centers = rod_centers()
    fixed_rods = build_reference_rod("left", centers["left"]) + build_reference_rod("bottom", centers["bottom"])
    references = build_wires() + build_esc() + build_fc() + build_xt60()
    for index in range(101):
        d = p.withdrawal_component * index / 100.0
        moved_pusher = Pos(0.0, d, d) * pusher
        moved_center = PointYZ(centers["moving"].y + d, centers["moving"].z + d)
        moved_rod = build_reference_rod("moving", moved_center)
        for moving, fixed in (
            (moved_pusher, fixed_plates),
            (moved_pusher, fixed_rods),
            (moved_pusher, references),
            (moved_rod, fixed_plates),
            (moved_rod, fixed_rods),
            (moved_rod, references),
        ):
            assert (moving & fixed).volume == pytest.approx(0.0, abs=1e-6)


def test_reference_layout_has_right_side_ESC_FC_and_visible_workpiece():
    for assembly in (build_loaded_closed(), build_loaded_open()):
        assert assembly.is_valid
        labels = {child.label for child in assembly.children}
        assert "reference_bottom_ESC_right_side" in labels
        assert "reference_FC_above_ESC_right_side" in labels
        assert "reference_two_mirrored_12awg_R6_leads" in labels
        assert "reference_vertical_XT60_above_bend" in labels
        text = " ".join(labels).lower()
        assert all(term not in text for term in ("screw", "dial", "adjustable"))


def test_print_kit_is_exactly_three_stable_nonoverlapping_solids():
    kit = build_print_kit()
    assert len(kit.children) == 3
    assert all(child.is_valid and len(child.solids()) == 1 for child in kit.children)
    bounds = kit.bounding_box()
    assert bounds.min.Z == pytest.approx(0.0, abs=1e-7)
    assert bounds.size.X <= 256.0 and bounds.size.Y <= 256.0
    for child in kit.children:
        assert child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    for index, first in enumerate(kit.children):
        for second in kit.children[index + 1 :]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)


def test_generated_step_exports_preserve_source_solid_count_and_bounds():
    project = Path(__file__).resolve().parents[1]
    export_dir = project / "cad" / "p2_corner_clamp_three_rod"
    cases = (
        ("p2_loaded_closed.step", build_loaded_closed()),
        ("p2_loaded_open.step", build_loaded_open()),
        ("p2_print_kit.step", build_print_kit()),
    )
    for filename, source in cases:
        imported = import_step(export_dir / filename)
        assert len(imported.solids()) == len(source.solids())
        source_bounds = source.bounding_box()
        imported_bounds = imported.bounding_box()
        for source_value, imported_value in zip(
            (*source_bounds.min, *source_bounds.max),
            (*imported_bounds.min, *imported_bounds.max),
            strict=True,
        ):
            assert imported_value == pytest.approx(source_value, abs=1e-7)


def test_generated_3mf_preserves_exact_three_named_print_meshes():
    project = Path(__file__).resolve().parents[1]
    export = project / "cad" / "p2_corner_clamp_three_rod" / "p2_print_kit.3mf"
    namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(export) as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    meshes = [
        obj for obj in root.findall(".//m:object", namespace)
        if obj.find("m:mesh", namespace) is not None
    ]
    assert {obj.attrib["name"] for obj in meshes} == {
        "print_left_large_fixed_L",
        "print_right_large_fixed_L",
        "print_one_piece_upper_right_corner_pusher",
    }
    assert all(obj.findall(".//m:vertex", namespace) for obj in meshes)
    assert all(obj.findall(".//m:triangle", namespace) for obj in meshes)
