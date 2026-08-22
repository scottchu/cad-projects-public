"""P4 acceptance: a captured, non-racking 45-degree slider, not a loose cap."""

from __future__ import annotations

from math import pi, sqrt
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Cylinder, GeomType, Pos, import_step

from xt60_bend_jig.p2_corner_clamp import (
    build_esc,
    build_fc,
    build_reference_rod,
    build_wire,
    build_wire_centerline,
    build_wires,
    build_xt60,
    contact_points,
    rod_centers,
)
from xt60_bend_jig.p4_sliding_carriage import (
    BORE_CHAMFER,
    BORE_MOUTH_DIAMETER,
    GUIDE_CLEARANCE,
    LEFT_CHEEK_X,
    LEFT_SHOE_X,
    M3_PIN_CLOSED,
    M3_PIN_DIAMETER,
    M3_SLOT_CLOSED,
    M3_SLOT_OPEN,
    M3_SLOT_WIDTH,
    OPEN_COMPONENT,
    OPEN_STOP_STROKE,
    P4_DEFAULTS,
    RIGHT_CHEEK_X,
    RIGHT_SHOE_X,
    ROD_SLOT_CLOSED,
    ROD_SLOT_OPEN,
    ROD_SLOT_WIDTH_FOLLOWER,
    ROD_SLOT_WIDTH_MASTER,
    build_fixed_plate,
    build_loaded_closed,
    build_loaded_mid,
    build_loaded_open,
    build_m3_guide_pin,
    build_moving_rod,
    build_print_kit,
    build_pusher,
    build_release_open,
    build_rods,
    moving_center,
    pin_center,
)


PROJECT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT / "cad" / "p4_sliding_carriage"


def _x_probe(diameter: float, length: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _along(start, end, point) -> float:
    dy, dz = end.y - start.y, end.z - start.z
    length = sqrt(dy * dy + dz * dz)
    return ((point.y - start.y) * dy + (point.z - start.z) * dz) / length


def test_frozen_12awg_R6_wire_and_three_4x50_rods_are_unchanged():
    p = P4_DEFAULTS
    assert p.wire_gauge == 12 and p.wire_diameter == pytest.approx(4.3)
    assert p.bend_radius == pytest.approx(6.0)
    assert build_wire_centerline().length == pytest.approx(44.0)
    assert p.arc_length == pytest.approx(pi * 6.0 / 2.0)
    rods = build_rods()
    assert len(rods.children) == 3
    for rod in rods.children:
        bounds = rod.bounding_box()
        assert (*bounds.size,) == pytest.approx((50.0, 4.0, 4.0))


def test_carriage_is_captured_between_exact_x_cheeks_with_0p3_gap():
    assert RIGHT_CHEEK_X == pytest.approx((19.0, 23.0))
    assert LEFT_CHEEK_X == pytest.approx((-23.0, -19.0))
    assert RIGHT_SHOE_X == pytest.approx((14.7, 18.7))
    assert LEFT_SHOE_X == pytest.approx((-18.7, -14.7))
    assert RIGHT_CHEEK_X[0] - RIGHT_SHOE_X[1] == pytest.approx(GUIDE_CLEARANCE)
    assert LEFT_SHOE_X[0] - LEFT_CHEEK_X[1] == pytest.approx(GUIDE_CLEARANCE)
    pusher = build_pusher()
    for side in ("left", "right"):
        fixed = build_fixed_plate(side)
        assert len(fixed.solids()) == 1 and fixed.is_valid
        assert (pusher & fixed).volume == pytest.approx(0.0, abs=1e-7)


def test_slots_and_pin_have_exact_contract_widths_and_0p5_endpoint_margin():
    assert ROD_SLOT_WIDTH_MASTER == pytest.approx(4.5)
    assert ROD_SLOT_WIDTH_FOLLOWER == pytest.approx(4.8)
    assert M3_PIN_DIAMETER == pytest.approx(3.0)
    assert M3_SLOT_WIDTH == pytest.approx(3.5)
    assert _along(ROD_SLOT_CLOSED, ROD_SLOT_OPEN, moving_center()) == pytest.approx(0.5)
    assert _along(ROD_SLOT_CLOSED, ROD_SLOT_OPEN, moving_center(OPEN_STOP_STROKE)) == pytest.approx(
        sqrt((ROD_SLOT_OPEN.y - ROD_SLOT_CLOSED.y) ** 2 + (ROD_SLOT_OPEN.z - ROD_SLOT_CLOSED.z) ** 2) - 0.5
    )
    assert _along(M3_SLOT_CLOSED, M3_SLOT_OPEN, pin_center()) == pytest.approx(0.5)
    assert _along(M3_SLOT_CLOSED, M3_SLOT_OPEN, pin_center(OPEN_STOP_STROKE)) == pytest.approx(
        sqrt((M3_SLOT_OPEN.y - M3_SLOT_CLOSED.y) ** 2 + (M3_SLOT_OPEN.z - M3_SLOT_CLOSED.z) ** 2) - 0.5
    )
    # The master pin physically lives on the left shoe/left cheek, not the
    # follower.  It is a separate guide constraint, not a fourth forming rod.
    pin = build_m3_guide_pin()
    assert pin.bounding_box().max.X <= -14.5 + 1e-7
    assert (pin & build_fixed_plate("left")).volume == pytest.approx(0.0, abs=1e-7)


def test_closed_stop_lugs_are_exact_and_open_stop_is_exact_11mm():
    pusher = build_pusher()
    for side in ("left", "right"):
        fixed = build_fixed_plate(side)
        assert fixed.distance_to(pusher) == pytest.approx(0.0, abs=1e-7)
        assert (fixed & pusher).volume == pytest.approx(0.0, abs=1e-7)
        # Both stop planes retain finite lands beyond the R3 relief: each
        # separate 10 µm overtravel direction penetrates a real solid.
        assert (fixed & (Pos(0.0, -0.01, 0.0) * pusher)).volume > 0.0
        assert (fixed & (Pos(0.0, 0.0, -0.01) * pusher)).volume > 0.0
    assert OPEN_STOP_STROKE == pytest.approx(11.0)
    fixed = build_fixed_plate("left") + build_fixed_plate("right")
    at_10p9 = Pos(0.0, 10.9 / sqrt(2.0), 10.9 / sqrt(2.0)) * pusher
    at_11 = Pos(0.0, OPEN_COMPONENT, OPEN_COMPONENT) * pusher
    at_11p1 = Pos(0.0, 11.1 / sqrt(2.0), 11.1 / sqrt(2.0)) * pusher
    assert at_10p9.distance_to(fixed) > 0.069
    assert at_11.distance_to(fixed) == pytest.approx(0.0, abs=1e-7)
    assert (at_11 & fixed).volume == pytest.approx(0.0, abs=1e-7)
    assert (at_11p1 & fixed).volume > 0.1


def test_rod_bores_keep_p3_0p4_by_45deg_chamfers_and_cap_has_r1_lower_edges():
    assert BORE_CHAMFER == pytest.approx(0.4)
    assert BORE_MOUTH_DIAMETER == pytest.approx(5.1)
    for shape in (build_fixed_plate("left"), build_fixed_plate("right"), build_pusher()):
        cones = list(shape.faces().filter_by(GeomType.CONE))
        assert cones
        assert all(face.bounding_box().size.X == pytest.approx(0.4, abs=1e-7) for face in cones)
    r1 = [face for face in build_pusher().faces().filter_by(GeomType.CYLINDER) if face.radius == pytest.approx(1.0)]
    assert len(r1) >= 2


@pytest.mark.parametrize("wire_x", (-4.0, 4.0))
def test_three_rod_contact_geometry_and_down_left_normal_stay_true(wire_x):
    wire = build_wire(wire_x, "#FFFFFF")
    for name, center in rod_centers().items():
        rod = build_reference_rod(name, center)
        assert rod.distance_to(wire) == pytest.approx(0.0, abs=1.1e-7)
        assert (rod & wire).volume == pytest.approx(0.0, abs=1e-7)
    q, m = contact_points()["moving"], rod_centers()["moving"]
    normal = (q.y - m.y, q.z - m.z)
    assert normal[0] * -1.0 - normal[1] * -1.0 == pytest.approx(0.0, abs=1e-9)
    assert normal[0] * -1.0 + normal[1] * -1.0 > 0.0


def test_101_pose_slider_sweep_is_contained_and_collision_free():
    pusher = build_pusher()
    fixed = build_fixed_plate("left") + build_fixed_plate("right")
    centers = rod_centers()
    fixed_rods = build_reference_rod("left", centers["left"]) + build_reference_rod("bottom", centers["bottom"])
    references = build_wires() + build_esc() + build_fc() + build_xt60()
    for index in range(101):
        travel = OPEN_STOP_STROKE * index / 100.0
        delta = travel / sqrt(2.0)
        carriage = Pos(0.0, delta, delta) * pusher
        moving_rod = build_moving_rod(travel)
        pin = build_m3_guide_pin(travel)
        # pusher may touch the two closed lugs at index 0 only; it never
        # penetrates a cheek, fixed rod, loaded wire, ESC, FC or XT60.
        for moving, stationary in (
            (carriage, fixed),
            (moving_rod, fixed),
            (pin, build_fixed_plate("left")),
            (carriage, fixed_rods),
            (moving_rod, fixed_rods),
            (carriage, references),
            (moving_rod, references),
        ):
            assert (moving & stationary).volume == pytest.approx(0.0, abs=1e-7)
        assert carriage.distance_to(fixed) >= -1e-8
        assert moving_rod.distance_to(fixed) >= -1e-8


def test_all_required_loaded_builds_and_exact_three_solid_print_kit_smoke():
    for assembly in (build_loaded_closed(), build_loaded_mid(), build_loaded_open(), build_release_open()):
        assert assembly.is_valid
    kit = build_print_kit()
    assert kit.is_valid and len(kit.children) == 3
    assert all(len(child.solids()) == 1 for child in kit.children)
    assert kit.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)


def test_generated_steps_and_3mf_match_source_after_export():
    cases = (
        ("p4_loaded_closed.step", build_loaded_closed()),
        ("p4_loaded_mid.step", build_loaded_mid()),
        ("p4_loaded_open.step", build_loaded_open()),
        ("p4_release_open.step", build_release_open()),
        ("p4_print_kit.step", build_print_kit()),
    )
    for filename, source in cases:
        imported = import_step(EXPORT_DIR / filename)
        assert len(imported.solids()) == len(source.solids())
        assert (*imported.bounding_box().min, *imported.bounding_box().max) == pytest.approx(
            (*source.bounding_box().min, *source.bounding_box().max), abs=1e-7
        )
    namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(EXPORT_DIR / "p4_print_kit.3mf") as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    meshes = [obj for obj in root.findall(".//m:object", namespace) if obj.find("m:mesh", namespace) is not None]
    assert {mesh.attrib["name"] for mesh in meshes} == {
        "print_left_green_master_slider_guide_cheek",
        "print_right_green_follower_slider_guide_cheek",
        "print_yellow_one_piece_captured_sliding_carriage",
    }
