"""BREP acceptance for the deliberately minimal P6A rod test."""

from math import pi
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Cylinder, Pos, import_step

from xt60_bend_jig.p6a_two_plate_rod_test import (
    CAP_FIT_DIAMETERS, HOLE_FIT_DIAMETERS, P6_DEFAULTS, THICKNESS_VARIANTS,
    build_cap, build_default_assembly, build_exploded, build_fit_ladder,
    build_fixed_cap, build_fixed_plate, build_gap_gauge, build_hole_fit_ladder,
    build_plate, build_print_kit, build_reference_rod, build_service_cap,
    build_service_plate, plate_centers,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cad" / "p6a_two_plate_rod_test"


def _probe(diameter: float, depth: float, z: float = -0.5):
    return Pos(0, 0, z) * Cylinder(
        diameter / 2, depth, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def _mesh_names(path: Path) -> set[str]:
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    return {
        node.attrib["name"] for node in root.findall(".//m:object", ns)
        if node.find("m:mesh", ns) is not None
    }


def test_frozen_dimensions_and_exact_gap_math():
    p = P6_DEFAULTS
    assert (p.rod_diameter, p.rod_length) == (4.0, 50.0)
    assert (p.plate_size, p.plate_thickness) == (24.0, 3.0)
    assert (p.fixed_plate_bore, p.service_plate_bore) == (3.90, 4.05)
    assert (p.cap_outer_diameter, p.cap_length) == (8.0, 5.0)
    assert (p.cap_insertion_depth, p.cap_closed_end) == (3.0, 2.0)
    assert p.rod_length - 2 * (p.cap_insertion_depth + p.plate_thickness) == p.gap == 38.0
    assert plate_centers() == (-20.5, 20.5)


def test_plate_breps_are_square_flat_and_have_real_through_bores():
    for part, bore in ((build_fixed_plate(), 3.90), (build_service_plate(), 4.05)):
        assert part.is_valid and len(part.solids()) == 1
        assert (*part.bounding_box().size,) == pytest.approx((24, 24, 3))
        assert (part & _probe(bore - 0.02, 4)).volume == pytest.approx(0, abs=1e-8)
        assert part.volume == pytest.approx(24 * 24 * 3 - pi * (bore / 2) ** 2 * 3)
        flats = [f for f in part.faces() if abs(abs(f.normal_at().Z) - 1) < 1e-8]
        assert len(flats) >= 2 and max(f.area for f in flats) > 500


def test_rod_clearance_and_intentional_interference_are_distinguished():
    rod_local = Cylinder(2, 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    assert (*build_reference_rod().bounding_box().size,) == pytest.approx((50, 4, 4))
    assert (build_service_plate() & rod_local).volume == pytest.approx(0, abs=1e-8)
    expected = pi * (2 ** 2 - (3.90 / 2) ** 2) * 3
    assert (build_fixed_plate() & rod_local).volume == pytest.approx(expected)


def test_round_blind_caps_have_exact_outer_envelope_and_two_mm_end():
    for cap, bore in ((build_fixed_cap(), 3.90), (build_service_cap(), 3.95)):
        assert cap.is_valid and len(cap.solids()) == 1
        assert (*cap.bounding_box().size,) == pytest.approx((8, 8, 5))
        assert (cap & _probe(bore - 0.05, 2.9, 0.05)).volume == pytest.approx(0, abs=1e-8)
        assert (cap & _probe(bore - 0.05, 0.2, 3.05)).volume > 0.1


def test_assembled_cap_sockets_face_inward_and_end_at_rod_ends():
    assembly = build_default_assembly()
    left_cap, right_cap = assembly.children[3], assembly.children[4]
    socket_probe = Cylinder(
        1.85, 2.8, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    assert (left_cap & Pos(-23.5, 0, 0) * socket_probe).volume == pytest.approx(0, abs=1e-8)
    assert (right_cap & Pos(23.5, 0, 0) * socket_probe).volume == pytest.approx(0, abs=1e-8)
    assert (left_cap & Pos(-26, 0, 0) * socket_probe).volume > 0.1
    assert (right_cap & Pos(26, 0, 0) * socket_probe).volume > 0.1


def test_assembly_is_exactly_five_parts_at_correct_faces():
    assembly = build_default_assembly()
    assert assembly.is_valid and len(assembly.children) == 5
    bounds = [value for child in assembly.children for value in (child.bounding_box().min.X, child.bounding_box().max.X)]
    assert bounds == pytest.approx([-22, -19, 19, 22, -25, 25, -27, -22, 22, 27])
    assert "not_self_fixturing" in assembly.label
    assert len(build_exploded().children) == 5


def test_gauge_is_broad_and_sets_spacing_only():
    gauge = build_gap_gauge()
    assert (*gauge.bounding_box().size,) == pytest.approx((38, 18, 5))
    xfaces = [f for f in gauge.faces() if abs(abs(f.normal_at().X) - 1) < 1e-8]
    assert len(xfaces) == 2 and all(f.area == pytest.approx(90) for f in xfaces)
    assert "spacing_only" in gauge.label and "two_clamps" in gauge.label


def test_fit_parts_cover_all_declared_variants_on_the_bed():
    assert THICKNESS_VARIANTS == (2.0, 2.5, 3.0, 3.5)
    assert HOLE_FIT_DIAMETERS == (3.85, 3.90, 3.95, 4.00, 4.05, 4.10)
    assert CAP_FIT_DIAMETERS == (3.85, 3.90, 3.95, 4.00)
    for thickness in THICKNESS_VARIANTS:
        assert build_plate(4.05, thickness).bounding_box().size.Z == pytest.approx(thickness)
    ladder = build_hole_fit_ladder()
    for i, diameter in enumerate(HOLE_FIT_DIAMETERS):
        probe = Pos(11 + i * 12, 0, 0) * _probe(diameter - 0.02, 4)
        assert (ladder & probe).volume == pytest.approx(0, abs=1e-8)
    fit = build_fit_ladder()
    assert len(fit.children) == 9
    assert all(child.bounding_box().min.Z == pytest.approx(0) for child in fit.children)


def test_print_kit_has_only_two_plates_two_caps_and_gauge_on_bed():
    kit = build_print_kit()
    assert len(kit.children) == 5 and all(child.is_valid for child in kit.children)
    assert all(len(child.solids()) == 1 for child in kit.children)
    assert all(child.bounding_box().min.Z == pytest.approx(0) for child in kit.children)


def test_exported_steps_and_mesh_names_match_source():
    cases = (
        ("p6a_default_assembly.step", build_default_assembly()),
        ("p6a_exploded.step", build_exploded()),
        ("p6a_print_kit.step", build_print_kit()),
        ("p6a_fit_ladder.step", build_fit_ladder()),
    )
    if not (OUT / cases[0][0]).exists():
        pytest.skip("P6A artifacts not generated yet")
    for filename, source in cases:
        imported = import_step(OUT / filename)
        assert len(imported.solids()) == len(source.solids())
        assert (*imported.bounding_box().min, *imported.bounding_box().max) == pytest.approx(
            (*source.bounding_box().min, *source.bounding_box().max), abs=1e-7
        )
    assert _mesh_names(OUT / "p6a_print_kit.3mf") == {c.label for c in build_print_kit().children}
    assert _mesh_names(OUT / "p6a_fit_ladder.3mf") == {c.label for c in build_fit_ladder().children}


@pytest.mark.parametrize("diameter", CAP_FIT_DIAMETERS)
def test_cap_fit_variants_are_closed_solids(diameter):
    cap = build_cap(diameter)
    assert cap.is_valid and len(cap.solids()) == 1 and cap.volume > 0
