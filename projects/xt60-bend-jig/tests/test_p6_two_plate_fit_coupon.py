"""BREP acceptance for the P6 Ø4 hardware fit coupon."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Cylinder, GeomType, Pos, import_step

from xt60_bend_jig.p6_two_plate_fit_coupon import (
    P6_DEFAULTS,
    build_cap,
    build_cap_ladder,
    build_exploded_assembly,
    build_nominal_assembly,
    build_plate,
    build_plate_ladder,
    build_print_kit,
    build_reference_rod,
    build_setup_gauge,
)


PROJECT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT / "cad" / "p6_two_plate_fit_coupon"


def _x_probe(diameter: float, length: float, x: float):
    return Pos(x, 0.0, 0.0) * Cylinder(
        diameter / 2.0, length, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )


def test_frozen_coupon_dimensions_and_ladder_values():
    p = P6_DEFAULTS
    assert p.rod_diameter == pytest.approx(4.0) and p.rod_length == pytest.approx(50.0)
    assert p.plate_size == pytest.approx(24.0) and p.plate_corner_radius == pytest.approx(2.0)
    assert p.plate_thicknesses == (2.0, 2.5, 3.0, 3.5)
    assert p.press_hole_diameter == pytest.approx(3.90)
    assert p.slip_hole_diameter == pytest.approx(4.20)
    assert p.cap_bores == (3.90, 4.00, 4.10, 4.20)
    assert p.inner_gap == pytest.approx(38.0)


@pytest.mark.parametrize("side,hole", (("left", 3.90), ("right", 4.20)))
@pytest.mark.parametrize("thickness", P6_DEFAULTS.plate_thicknesses)
def test_every_plate_variant_is_one_solid_with_centered_chamfered_hole(side, hole, thickness):
    plate = build_plate(side, thickness)
    assert plate.is_valid and len(plate.solids()) == 1 and len(plate.shells()) == 1
    bounds = plate.bounding_box()
    assert bounds.size.Y == pytest.approx(24.0) and bounds.size.Z == pytest.approx(24.0)
    assert bounds.size.X == pytest.approx(thickness)
    center_x = (bounds.min.X + bounds.max.X) / 2.0
    assert (plate & _x_probe(hole, thickness + 1.0, center_x)).volume == pytest.approx(0.0, abs=1e-7)
    assert (plate & _x_probe(hole + 0.02, thickness / 2.0, center_x)).volume > 0.0
    cones = list(plate.faces().filter_by(GeomType.CONE))
    assert len(cones) == 2
    assert all(face.bounding_box().size.X == pytest.approx(0.4, abs=1e-7) for face in cones)
    id_notch = Pos(0.0, 9.0, 12.0) * _x_probe(2.0, thickness + 1.0, center_x)
    if side == "right":
        assert (plate & id_notch).volume == pytest.approx(0.0, abs=1e-7)
        assert "service_notch" in plate.label
    else:
        assert (plate & id_notch).volume > 0.1


def test_nominal_outer_seating_datum_creates_real_40_39_38_37_gap_ladder():
    p = P6_DEFAULTS
    expected = {2.0: 40.0, 2.5: 39.0, 3.0: 38.0, 3.5: 37.0}
    for thickness, gap in expected.items():
        left, right = build_plate("left", thickness), build_plate("right", thickness)
        assert right.bounding_box().min.X - left.bounding_box().max.X == pytest.approx(gap)
    nominal = build_nominal_assembly()
    plates = [child for child in nominal.children if "plate_t3.0" in child.label]
    assert len(plates) == 2
    ordered = sorted(plates, key=lambda part: part.bounding_box().min.X)
    assert ordered[1].bounding_box().min.X - ordered[0].bounding_box().max.X == pytest.approx(38.0)


@pytest.mark.parametrize("side", ("left", "right"))
@pytest.mark.parametrize("bore", P6_DEFAULTS.cap_bores)
def test_every_hex_cap_is_one_solid_8AF_with_3mm_blind_socket_and_closed_end(side, bore):
    cap = build_cap(side, bore)
    assert cap.is_valid and len(cap.solids()) == 1 and len(cap.shells()) == 1
    bounds = cap.bounding_box()
    assert bounds.size.X == pytest.approx(5.0)
    assert bounds.size.Y == pytest.approx(8.0)
    entry_x = -22.0 if side == "left" else 22.0
    socket_x = entry_x + (-1.0 if side == "left" else 1.0) * 1.5
    assert (cap & _x_probe(bore, 3.0, socket_x)).volume == pytest.approx(0.0, abs=1e-7)
    assert (cap & _x_probe(bore + 0.02, 1.0, socket_x)).volume > 0.01
    # The 2 mm outer end remains solid: a socket-depth over-probe meets it.
    beyond_x = entry_x + (-1.0 if side == "left" else 1.0) * 3.5
    assert (cap & _x_probe(bore, 1.0, beyond_x)).volume > 0.0
    cones = list(cap.faces().filter_by(GeomType.CONE))
    assert len(cones) == 1
    assert cones[0].bounding_box().size.X == pytest.approx(0.4, abs=1e-7)
    count = P6_DEFAULTS.cap_bores.index(bore) + 1
    cap_center = (bounds.min.X + bounds.max.X) / 2.0
    sign = -1.0 if side == "left" else 1.0
    dimple_x = cap_center + sign * (P6_DEFAULTS.cap_length / 2.0 - 0.4)
    for index in range(count):
        dimple = Pos(0.0, -2.7 + index * 1.25, 0.0) * _x_probe(0.9, 0.9, dimple_x)
        assert (cap & dimple).volume == pytest.approx(0.0, abs=1e-7)


def test_real_4mm_rod_has_only_documented_press_interference_in_nominal_assembly():
    assembly = build_nominal_assembly()
    rod = next(child for child in assembly.children if "purchased_stainless" in child.label)
    left_plate = next(child for child in assembly.children if child.label.startswith("left_press"))
    right_plate = next(child for child in assembly.children if child.label.startswith("right_slip"))
    fixed_cap = next(child for child in assembly.children if child.label.startswith("left_hex"))
    service_cap = next(child for child in assembly.children if child.label.startswith("right_hex"))
    gauge = next(child for child in assembly.children if "setup_gauge" in child.label)
    assert (rod & left_plate).volume > 0.01  # intended Ø3.90 press
    assert (rod & fixed_cap).volume > 0.01  # intended Ø3.90 fixed cap
    assert (rod & right_plate).volume == pytest.approx(0.0, abs=1e-7)
    assert (rod & service_cap).volume == pytest.approx(0.0, abs=1e-7)
    assert (rod & gauge).volume == pytest.approx(0.0, abs=1e-7)
    assert (left_plate & fixed_cap).volume == pytest.approx(0.0, abs=1e-7)
    assert (right_plate & service_cap).volume == pytest.approx(0.0, abs=1e-7)


def test_setup_gauge_is_removable_38x8x3_and_touches_only_nominal_inner_faces():
    gauge = build_setup_gauge()
    assert gauge.is_valid and len(gauge.solids()) == 1
    assert (*gauge.bounding_box().size,) == pytest.approx((38.0, 8.0, 3.0))
    left, right = build_plate("left", 3.0), build_plate("right", 3.0)
    assert gauge.distance_to(left) == pytest.approx(0.0, abs=1e-7)
    assert gauge.distance_to(right) == pytest.approx(0.0, abs=1e-7)
    assert (gauge & (left + right)).volume == pytest.approx(0.0, abs=1e-7)


def test_ladder_assemblies_and_full_13_solid_print_kit_are_printable_and_named():
    assert build_plate_ladder().is_valid and len(build_plate_ladder().solids()) == 8
    assert build_cap_ladder().is_valid and len(build_cap_ladder().solids()) == 4
    kit = build_print_kit()
    assert kit.is_valid and len(kit.children) == 13
    assert all(child.is_valid and len(child.solids()) == 1 for child in kit.children)
    assert kit.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)
    assert all(child.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7) for child in kit.children)
    for index, first in enumerate(kit.children):
        for second in kit.children[index + 1 :]:
            assert (first & second).volume == pytest.approx(0.0, abs=1e-7)
    labels = [child.label for child in kit.children]
    assert len(set(labels)) == 13


def test_required_assemblies_have_explicit_access_and_coupon_labels():
    nominal = build_nominal_assembly()
    exploded = build_exploded_assembly()
    assert nominal.is_valid and exploded.is_valid
    assert len(nominal.solids()) == 6 and len(exploded.solids()) == 6
    assert "press_left_slip_right" in nominal.label
    assert "access" in exploded.label


def test_exported_steps_and_3mf_preserve_source_solids_bounds_and_print_names():
    cases = (
        ("p6_nominal_assembly.step", build_nominal_assembly()),
        ("p6_exploded_assembly.step", build_exploded_assembly()),
        ("p6_plate_thickness_ladder.step", build_plate_ladder()),
        ("p6_cap_fit_ladder.step", build_cap_ladder()),
        ("p6_full_print_kit.step", build_print_kit()),
    )
    for filename, source in cases:
        imported = import_step(EXPORT_DIR / filename)
        assert len(imported.solids()) == len(source.solids())
        assert (*imported.bounding_box().min, *imported.bounding_box().max) == pytest.approx(
            (*source.bounding_box().min, *source.bounding_box().max), abs=1e-7
        )
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(EXPORT_DIR / "p6_full_print_kit.3mf") as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    meshes = [obj for obj in root.findall(".//m:object", ns) if obj.find("m:mesh", ns) is not None]
    assert len(meshes) == 13
    assert {mesh.attrib["name"] for mesh in meshes} == {child.label for child in build_print_kit().children}
