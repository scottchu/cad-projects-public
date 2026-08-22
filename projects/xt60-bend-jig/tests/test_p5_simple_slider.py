"""Acceptance tests for the deliberately minimal three-solid P5 slider."""

from __future__ import annotations

from math import pi, sqrt
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Cylinder, GeomType, Pos, import_step

from xt60_bend_jig.p2_corner_clamp import (
    PointYZ,
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
from xt60_bend_jig.p5_simple_slider import (
    BORE_CHAMFER,
    BORE_MOUTH_DIAMETER,
    GUIDE_CLEARANCE,
    LEFT_ARM_X,
    LEFT_PLATE_X,
    MOVING_SLOT_WIDTH,
    OPEN_COMPONENT,
    OPEN_STROKE,
    P5_DEFAULTS,
    RIGHT_ARM_X,
    RIGHT_PLATE_X,
    SLOT_RADIAL_CLEARANCE,
    build_fixed_plate,
    build_loaded_closed,
    build_loaded_mid,
    build_loaded_open,
    build_moving_rod,
    build_print_kit,
    build_pusher,
    build_release_open,
    build_rods,
    moving_center,
    slot_endpoints,
)


PROJECT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT / "cad" / "p5_simple_slider"


def _x_probe(diameter: float, length: float, x: float, point: PointYZ):
    return Pos(x, point.y, point.z) * Cylinder(
        diameter / 2.0, length, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )


def test_simple_contract_is_exactly_three_rods_three_prints_no_antirack_features():
    rods = build_rods()
    assert len(rods.children) == 3
    for rod in rods.children:
        assert (*rod.bounding_box().size,) == pytest.approx((50.0, 4.0, 4.0))
    kit = build_print_kit()
    assert len(kit.children) == 3 and all(len(child.solids()) == 1 for child in kit.children)
    labels = " ".join(child.label.lower() for child in kit.children)
    assert all(forbidden not in labels for forbidden in ("m3", "antirack", "guide_cheek", "lug"))


def test_plain_L_plates_have_only_two_fixed_bores_and_one_45deg_slot_each():
    fixed = rod_centers()
    for side, x in (("left", -21.0), ("right", 21.0)):
        plate = build_fixed_plate(side)
        assert plate.is_valid and len(plate.solids()) == 1
        for name in ("left", "bottom"):
            assert (plate & _x_probe(4.3, 6.0, x, fixed[name])).volume == pytest.approx(0.0, abs=1e-7)
        # Exactly two Ø4.3 fixed-bore cylindrical lands. The only other large
        # feature is the required obround moving slot.
        lands = [face for face in plate.faces().filter_by(GeomType.CYLINDER) if face.radius == pytest.approx(2.15)]
        assert len(lands) == 2


def test_slot_math_gives_physical_center_stops_exactly_11mm():
    assert MOVING_SLOT_WIDTH == pytest.approx(4.5)
    assert SLOT_RADIAL_CLEARANCE == pytest.approx(0.25)
    low, high = slot_endpoints()
    closed, opened = moving_center(0.0), moving_center(OPEN_STROKE)
    unit = 1.0 / sqrt(2.0)
    assert low == pytest.approx(PointYZ(closed.y + 0.25 * unit, closed.z + 0.25 * unit))
    assert high == pytest.approx(PointYZ(opened.y - 0.25 * unit, opened.z - 0.25 * unit))
    assert sqrt((high.y - low.y) ** 2 + (high.z - low.z) ** 2) == pytest.approx(10.5)
    plates = build_fixed_plate("left") + build_fixed_plate("right")
    base = rod_centers()["moving"]
    def free_rod(travel: float):
        d = travel / sqrt(2.0)
        return build_reference_rod("probe", PointYZ(base.y + d, base.z + d))
    assert (free_rod(-0.1) & plates).volume > 0.1
    assert (free_rod(0.0) & plates).volume == pytest.approx(0.0, abs=1e-7)
    assert (free_rod(OPEN_STROKE) & plates).volume == pytest.approx(0.0, abs=1e-7)
    assert (free_rod(11.1) & plates).volume > 0.1


def test_yellow_U_is_inside_plate_faces_with_0p3_axial_gap_and_has_no_pin_hole():
    assert RIGHT_PLATE_X[0] - RIGHT_ARM_X[1] == pytest.approx(GUIDE_CLEARANCE)
    assert LEFT_ARM_X[0] - LEFT_PLATE_X[1] == pytest.approx(GUIDE_CLEARANCE)
    pusher = build_pusher()
    assert pusher.is_valid and len(pusher.solids()) == 1
    assert pusher.bounding_box().min.X == pytest.approx(-18.7)
    assert pusher.bounding_box().max.X == pytest.approx(18.7)
    # Only the two moving-rod bores are cylindrical through-holes in yellow.
    lands = [face for face in pusher.faces().filter_by(GeomType.CYLINDER) if face.radius == pytest.approx(2.15)]
    assert len(lands) == 2


@pytest.mark.parametrize("wire_x", (-4.0, 4.0))
def test_frozen_R6_wire_contacts_and_90deg_force_normal_are_unchanged(wire_x):
    assert build_wire_centerline().length == pytest.approx(44.0)
    wire = build_wire(wire_x, "#FFFFFF")
    for name, point in rod_centers().items():
        rod = build_reference_rod(name, point)
        assert rod.distance_to(wire) == pytest.approx(0.0, abs=1.1e-7)
        assert (rod & wire).volume == pytest.approx(0.0, abs=1e-7)
    q, m = contact_points()["moving"], rod_centers()["moving"]
    assert (q.y - m.y) == pytest.approx(q.z - m.z)


def test_101_pose_sweep_is_clear_except_for_intended_rod_end_contacts():
    pusher = build_pusher()
    plates = build_fixed_plate("left") + build_fixed_plate("right")
    fixed = build_reference_rod("left", rod_centers()["left"]) + build_reference_rod("bottom", rod_centers()["bottom"])
    references = build_wires() + build_esc() + build_fc() + build_xt60()
    for index in range(101):
        travel = OPEN_STROKE * index / 100.0
        d = travel / sqrt(2.0)
        moved_pusher = Pos(0.0, d, d) * pusher
        moved_rod = build_moving_rod(travel)
        for moving, stationary in ((moved_pusher, plates), (moved_pusher, fixed), (moved_pusher, references), (moved_rod, fixed), (moved_rod, references)):
            assert (moving & stationary).volume == pytest.approx(0.0, abs=1e-7)
        assert (moved_rod & plates).volume == pytest.approx(0.0, abs=1e-7)


def test_cosmetic_production_details_and_all_build_states_hold():
    assert BORE_CHAMFER == pytest.approx(0.4) and BORE_MOUTH_DIAMETER == pytest.approx(5.1)
    for shape in (build_fixed_plate("left"), build_fixed_plate("right"), build_pusher()):
        cones = list(shape.faces().filter_by(GeomType.CONE))
        assert cones and all(face.bounding_box().size.X == pytest.approx(0.4, abs=1e-7) for face in cones)
    cap_r1 = [face for face in build_pusher().faces().filter_by(GeomType.CYLINDER) if face.radius == pytest.approx(1.0)]
    assert len(cap_r1) >= 2
    for assembly in (build_loaded_closed(), build_loaded_mid(), build_loaded_open(), build_release_open()):
        assert assembly.is_valid


def test_exported_steps_and_three_mesh_print_kit_match_source():
    cases = (
        ("p5_loaded_closed.step", build_loaded_closed()),
        ("p5_loaded_mid.step", build_loaded_mid()),
        ("p5_loaded_open.step", build_loaded_open()),
        ("p5_release_open.step", build_release_open()),
        ("p5_print_kit.step", build_print_kit()),
    )
    for filename, source in cases:
        imported = import_step(EXPORT_DIR / filename)
        assert len(imported.solids()) == len(source.solids())
        assert (*imported.bounding_box().min, *imported.bounding_box().max) == pytest.approx(
            (*source.bounding_box().min, *source.bounding_box().max), abs=1e-7
        )
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(EXPORT_DIR / "p5_print_kit.3mf") as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    meshes = [obj for obj in root.findall(".//m:object", ns) if obj.find("m:mesh", ns) is not None]
    assert {obj.attrib["name"] for obj in meshes} == {
        "print_left_plain_green_right_angle_slot_plate",
        "print_right_plain_green_right_angle_slot_plate",
        "print_yellow_simple_U_pusher",
    }
