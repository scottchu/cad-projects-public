"""Acceptance tests for the preserved-mechanics P3 rounded push cap."""

from __future__ import annotations

from math import pi
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Cylinder, GeomType, Pos, import_step

from xt60_bend_jig.p2_corner_clamp import (
    P2_DEFAULTS,
    build_esc,
    build_fc,
    build_reference_rod,
    build_rods,
    build_wire,
    build_wire_centerline,
    build_wires,
    build_xt60,
    contact_points,
    rod_centers,
)
from xt60_bend_jig.p3_rounded_cap import (
    BORE_CHAMFER,
    BORE_MOUTH_DIAMETER,
    P3_DEFAULTS,
    build_fixed_plate,
    build_loaded_closed,
    build_loaded_open,
    build_print_kit,
    build_push_cap,
    build_pusher,
)


PROJECT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT / "cad" / "p3_rounded_cap"


def _x_probe(diameter: float, length: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0, 90, 0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _bore_lands(shape):
    return [
        face
        for face in shape.faces().filter_by(GeomType.CYLINDER)
        if face.radius == pytest.approx(P3_DEFAULTS.rod_bore_diameter / 2.0)
    ]


def test_p3_reuses_all_frozen_p2_mechanics_without_penetration():
    p = P3_DEFAULTS
    assert p is P2_DEFAULTS
    assert p.rod_diameter == 4.0
    assert p.rod_length == 50.0
    assert p.rod_bore_diameter == 4.3
    assert p.clear_span == 38.0
    assert p.plate_thickness == 4.0
    assert p.bend_radius == 6.0
    assert p.available_lead == 44.0
    assert p.stop_y == 0.0 and p.stop_z == 30.0
    assert p.diagonal_stroke == 11.0
    assert rod_centers()["moving"].y == pytest.approx(4.691852455)
    assert rod_centers()["moving"].z == pytest.approx(34.691852455)
    assert p.moving_open.y == pytest.approx(12.470027048)
    assert p.moving_open.z == pytest.approx(42.470027048)
    assert build_wire_centerline().length == pytest.approx(44.0)


def test_three_rods_remain_exactly_4x50():
    rods = build_rods()
    assert len(rods.children) == 3
    for rod in rods.children:
        bounds = rod.bounding_box()
        assert (bounds.size.X, bounds.size.Y, bounds.size.Z) == pytest.approx((50.0, 4.0, 4.0))
        assert rod.volume == pytest.approx(pi * 2.0**2 * 50.0)


@pytest.mark.parametrize("wire_x", (-4.0, 4.0))
def test_all_six_rod_wire_tangencies_are_unchanged_actual_brep(wire_x):
    wire = build_wire(wire_x, "#FFFFFF")
    for name, center in rod_centers().items():
        rod = build_reference_rod(name, center)
        assert rod.distance_to(wire) == pytest.approx(0.0, abs=1.1e-7)
        assert (rod & wire).volume == pytest.approx(0.0, abs=1e-7)


def test_moving_contact_normal_and_45deg_close_vector_are_unchanged():
    q = contact_points()["moving"]
    m = rod_centers()["moving"]
    normal = (q.y - m.y, q.z - m.z)
    close = (-P3_DEFAULTS.withdrawal_component, -P3_DEFAULTS.withdrawal_component)
    assert normal[0] * close[1] - normal[1] * close[0] == pytest.approx(0.0, abs=1e-9)
    assert normal[0] * close[0] + normal[1] * close[1] > 0.0


@pytest.mark.parametrize("side", ("left", "right"))
def test_each_green_plate_is_one_solid_one_shell_with_exact_span_and_bores(side):
    p = P3_DEFAULTS
    plate = build_fixed_plate(side)
    assert plate.is_valid and len(plate.solids()) == 1 and len(plate.shells()) == 1
    bounds = plate.bounding_box()
    if side == "left":
        assert bounds.max.X == pytest.approx(-19.0)
    else:
        assert bounds.min.X == pytest.approx(19.0)
    x = (-1.0 if side == "left" else 1.0) * p.plate_center_x
    for name in ("left", "bottom"):
        center = rod_centers()[name]
        assert (plate & _x_probe(4.3, 6.0, x, center.y, center.z)).volume == pytest.approx(0.0, abs=1e-7)
        assert (plate & _x_probe(4.32, 3.0, x, center.y, center.z)).volume > 0.0
    lands = _bore_lands(plate)
    assert len(lands) == 2
    assert all(face.bounding_box().size.X == pytest.approx(3.2) for face in lands)


def test_yellow_pusher_is_one_solid_with_exact_bore_axes_and_r3_reliefs():
    pusher = build_pusher()
    assert pusher.is_valid and len(pusher.solids()) == 1 and len(pusher.shells()) == 1
    moving = rod_centers()["moving"]
    for sign in (-1.0, 1.0):
        x = sign * P3_DEFAULTS.plate_center_x
        assert (pusher & _x_probe(4.3, 6.0, x, moving.y, moving.z)).volume == pytest.approx(0.0, abs=1e-7)
        assert (pusher & _x_probe(4.32, 3.0, x, moving.y, moving.z)).volume > 0.0
    assert len(_bore_lands(pusher)) == 2
    reliefs = [
        face
        for face in pusher.faces().filter_by(GeomType.CYLINDER)
        if face.radius == pytest.approx(3.0)
    ]
    assert len(reliefs) == 2
    for relief in reliefs:
        bounds = relief.bounding_box()
        assert bounds.min.Y == pytest.approx(0.0)
        assert bounds.max.Y == pytest.approx(3.0)
        assert bounds.min.Z == pytest.approx(30.0)
        assert bounds.max.Z == pytest.approx(33.0)


@pytest.mark.parametrize("shape", (build_fixed_plate("left"), build_fixed_plate("right"), build_pusher()))
def test_constructive_bore_mouths_are_exact_0p4_by_45deg(shape):
    assert BORE_CHAMFER == pytest.approx(0.4)
    assert BORE_MOUTH_DIAMETER == pytest.approx(5.1)
    lands = _bore_lands(shape)
    cones = list(shape.faces().filter_by(GeomType.CONE))
    assert len(cones) == 2 * len(lands)
    assert all(face.bounding_box().size.X == pytest.approx(0.4, abs=1e-7) for face in cones)
    assert all(face.bounding_box().size.Y == pytest.approx(5.1, abs=1e-7) for face in cones)
    assert all(face.bounding_box().size.Z == pytest.approx(5.1, abs=1e-7) for face in cones)


def test_closed_stop_has_two_exact_planar_lands_per_side_and_no_overlap():
    pusher = build_pusher()
    vertical_lands = []
    horizontal_lands = []
    for face in pusher.faces().filter_by(GeomType.PLANE):
        bounds = face.bounding_box()
        if bounds.size.Y <= 1e-8 and bounds.min.Y == pytest.approx(0.0):
            vertical_lands.append(face)
        if bounds.size.Z <= 1e-8 and bounds.min.Z == pytest.approx(30.0):
            horizontal_lands.append(face)
    assert sorted(face.area for face in vertical_lands) == pytest.approx([28.0, 28.0])
    assert sorted(face.area for face in horizontal_lands) == pytest.approx([44.0, 44.0])
    for side in ("left", "right"):
        plate = build_fixed_plate(side)
        assert plate.distance_to(pusher) == pytest.approx(0.0, abs=1e-7)
        assert (plate & pusher).volume == pytest.approx(0.0, abs=1e-7)
        assert (plate & (Pos(0.0, -0.01, 0.0) * pusher)).volume > 0.0
        assert (plate & (Pos(0.0, 0.0, -0.01) * pusher)).volume > 0.0


def test_push_cap_envelope_bed_face_and_sweep_clearances():
    cap = build_push_cap()
    bounds = cap.bounding_box()
    assert (*bounds.min, *bounds.max) == pytest.approx((-23.0, 10.0, 44.0, 23.0, 18.0, 50.0))
    bed_faces = [
        face
        for face in cap.faces().filter_by(GeomType.PLANE)
        if face.bounding_box().min.Z == pytest.approx(50.0)
        and face.bounding_box().max.Z == pytest.approx(50.0)
    ]
    assert sum(face.area for face in bed_faces) >= 368.0
    references = {
        "wires": (build_wires(), 7.85),
        "xt60": (build_xt60(), 6.94),
        "fc": (build_fc(), 9.72),
        "esc": (build_esc(), 19.29),
    }
    minima = {name: float("inf") for name in references}
    for index in range(101):
        d = P3_DEFAULTS.withdrawal_component * index / 100.0
        moved = Pos(0.0, d, d) * cap
        for name, (reference, _) in references.items():
            minima[name] = min(minima[name], moved.distance_to(reference))
    for name, (_, required) in references.items():
        assert minima[name] >= required


def test_full_101_point_pusher_and_moving_rod_sweep_is_collision_free():
    p = P3_DEFAULTS
    pusher = build_pusher()
    fixed_plates = build_fixed_plate("left") + build_fixed_plate("right")
    centers = rod_centers()
    fixed_rods = build_reference_rod("left", centers["left"]) + build_reference_rod("bottom", centers["bottom"])
    references = build_wires() + build_esc() + build_fc() + build_xt60()
    for index in range(101):
        d = p.withdrawal_component * index / 100.0
        moved_pusher = Pos(0.0, d, d) * pusher
        moved_center = type(centers["moving"])(centers["moving"].y + d, centers["moving"].z + d)
        moved_rod = build_reference_rod("moving", moved_center)
        for moving, fixed in (
            (moved_pusher, fixed_plates),
            (moved_pusher, fixed_rods),
            (moved_pusher, references),
            (moved_rod, fixed_plates),
            (moved_rod, fixed_rods),
            (moved_rod, references),
        ):
            assert (moving & fixed).volume == pytest.approx(0.0, abs=1e-7)


def test_no_source_slivers_and_loaded_labels_explain_structural_intent():
    for shape in (build_fixed_plate("left"), build_fixed_plate("right"), build_pusher()):
        assert min(face.area for face in shape.faces()) >= 0.1
        assert min(edge.length for edge in shape.edges()) >= 0.1
    for assembly in (build_loaded_closed(), build_loaded_open()):
        assert assembly.is_valid and len(assembly.solids()) == 11
        labels = " ".join(child.label for child in assembly.children).lower()
        assert "push_cap" in labels
        assert "no_actuation" in assembly.label.lower()
        assert all(term not in labels for term in ("screw", "guide", "dial"))


def test_print_kit_is_exactly_three_stable_separated_solids():
    kit = build_print_kit()
    assert len(kit.children) == 3
    assert all(child.is_valid and len(child.solids()) == 1 and len(child.shells()) == 1 for child in kit.children)
    bounds = kit.bounding_box()
    assert bounds.min.Z == pytest.approx(0.0, abs=1e-7)
    assert bounds.size.X <= 256.0 and bounds.size.Y <= 256.0
    ordered = sorted(kit.children, key=lambda child: child.bounding_box().min.X)
    assert ordered[1].bounding_box().min.X - ordered[0].bounding_box().max.X == pytest.approx(15.0, abs=1e-6)
    assert ordered[2].bounding_box().min.X - ordered[1].bounding_box().max.X == pytest.approx(15.0, abs=1e-6)
    for child in ordered:
        assert child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    pusher = next(child for child in ordered if "push_cap" in child.label)
    bed_faces = [face for face in pusher.faces() if face.bounding_box().max.Z <= 1e-7]
    assert sum(face.area for face in bed_faces) >= 368.0
    for index, first in enumerate(ordered):
        for second in ordered[index + 1 :]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)


def test_generated_step_exports_preserve_source_counts_bounds_and_volume():
    cases = (
        ("p3_loaded_closed.step", build_loaded_closed()),
        ("p3_loaded_open.step", build_loaded_open()),
        ("p3_print_kit.step", build_print_kit()),
    )
    for filename, source in cases:
        imported = import_step(EXPORT_DIR / filename)
        assert len(imported.solids()) == len(source.solids())
        assert len(imported.children) == len(source.children)
        source_bounds = source.bounding_box()
        imported_bounds = imported.bounding_box()
        assert (*imported_bounds.min, *imported_bounds.max) == pytest.approx(
            (*source_bounds.min, *source_bounds.max), abs=1e-7
        )
        assert sorted(solid.volume for solid in imported.solids()) == pytest.approx(
            sorted(solid.volume for solid in source.solids()), rel=1e-8
        )
        assert all(min(face.area for face in solid.faces()) >= 0.1 for solid in imported.solids())
        assert all(min(edge.length for edge in solid.edges()) >= 0.1 for solid in imported.solids())


def test_generated_3mf_has_exactly_three_named_nonempty_meshes():
    export = EXPORT_DIR / "p3_print_kit.3mf"
    namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(export) as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    meshes = [
        obj
        for obj in root.findall(".//m:object", namespace)
        if obj.find("m:mesh", namespace) is not None
    ]
    assert {obj.attrib["name"] for obj in meshes} == {
        "print_left_rounded_fixed_L",
        "print_right_rounded_fixed_L",
        "print_synchronized_push_cap_not_handle",
    }
    assert all(obj.findall(".//m:vertex", namespace) for obj in meshes)
    assert all(obj.findall(".//m:triangle", namespace) for obj in meshes)
