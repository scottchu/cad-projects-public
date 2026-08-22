from __future__ import annotations

from hashlib import sha256
import json
from math import pi
from pathlib import Path

import lib3mf
import pytest
from build123d import GeomType, import_step

import xt60_bend_jig.p13_rod_fit_coupon_3p8 as coupon


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad" / "p13_rod_fit_coupon_3p8"
STEP = CAD / "p13_rod_fit_coupon_3p8.step"
THREEMF = CAD / "p13_rod_fit_coupon_3p8.3mf"
PROVENANCE = CAD / "p13_rod_fit_coupon_3p8.provenance.json"


def _circular_edge_radii(shape) -> list[float]:
    return [float(edge.radius) for edge in shape.edges() if edge.geom_type == GeomType.CIRCLE]


def test_parameter_contract_is_exactly_seven_ordered_labeled_stations() -> None:
    p = coupon.DEFAULTS
    assert p.measured_rod_diameter == pytest.approx(3.80)
    assert p.hole_diameters == (3.70, 3.75, 3.80, 3.85, 3.90, 3.95, 4.00)
    assert p.plate_thickness == pytest.approx(3.0)
    assert coupon.hole_centres(p) == (
        (-14.25, 5.5),
        (-4.75, 5.5),
        (4.75, 5.5),
        (14.25, 5.5),
        (-9.5, -5.5),
        (0.0, -5.5),
        (9.5, -5.5),
    )
    assert coupon.label_centres(p) == (
        (-14.25, 11.05),
        (-4.75, 11.05),
        (4.75, 11.05),
        (14.25, 11.05),
        (-9.5, -11.05),
        (0.0, -11.05),
        (9.5, -11.05),
    )
    manifest = coupon.parameter_manifest(p)
    assert manifest["stationOrder"] == [
        "3.70", "3.75", "3.80", "3.85", "3.90", "3.95", "4.00"
    ]
    assert set(manifest["interpretation"]) == {"3.70", "3.80", "3.90", "4.00"}
    assert len(coupon.parameter_manifest_sha256(p)) == 64


def test_coupon_is_one_closed_positive_flat_print_solid_with_clipped_datum() -> None:
    p = coupon.DEFAULTS
    shape = coupon.build_coupon(p)
    assert shape.is_valid
    assert len(shape.solids()) == 1
    assert float(shape.volume) > 0.0
    box = shape.bounding_box()
    assert (box.size.X, box.size.Y, box.size.Z) == pytest.approx(
        (p.plate_width, p.plate_depth, p.plate_thickness), abs=1e-6
    )
    assert box.min.Z == pytest.approx(0.0, abs=1e-6)
    assert box.max.Z == pytest.approx(3.0, abs=1e-6)

    vertices = {(round(v.X, 6), round(v.Y, 6)) for v in shape.vertices()}
    assert (-20.0, 14.0) not in vertices
    assert (-16.0, 14.0) in vertices
    assert (-20.0, 10.0) in vertices


def test_actual_brep_contains_exact_seven_specified_through_hole_diameters() -> None:
    shape = coupon.build_coupon()
    radii = _circular_edge_radii(shape)
    expected = [diameter / 2.0 for diameter in coupon.DEFAULTS.hole_diameters]
    for radius in expected:
        # A through bore contributes a top and bottom circular edge.
        assert sum(value == pytest.approx(radius, abs=1e-8) for value in radii) == 2
    assert not any(value == pytest.approx(2.025, abs=1e-8) for value in radii)


def test_compact_layout_keeps_petg_ligament_and_edge_material() -> None:
    p = coupon.DEFAULTS
    centres = coupon.hole_centres(p)
    assert (p.plate_width, p.plate_depth) == pytest.approx((40.0, 28.0))
    assert p.plate_width * p.plate_depth < 0.38 * (84.0 * 36.0)

    for index, ((x0, y0), diameter0) in enumerate(zip(centres, p.hole_diameters)):
        radius0 = diameter0 / 2.0
        assert p.plate_width / 2.0 - abs(x0) - radius0 >= p.minimum_edge_wall
        assert p.plate_depth / 2.0 - abs(y0) - radius0 >= p.minimum_edge_wall
        for (x1, y1), diameter1 in zip(
            centres[index + 1 :], p.hole_diameters[index + 1 :]
        ):
            centre_distance = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
            ligament = centre_distance - radius0 - diameter1 / 2.0
            assert ligament >= p.minimum_ligament


def test_engraved_labels_exist_as_real_top_surface_volume_removal() -> None:
    p = coupon.DEFAULTS
    shape = coupon.build_coupon(p)
    outline_area = p.plate_width * p.plate_depth - p.clipped_corner_size**2 / 2.0
    base_minus_holes = (
        outline_area * p.plate_thickness
        - sum(pi * (diameter / 2.0) ** 2 * p.plate_thickness for diameter in p.hole_diameters)
    )
    # All seven diameter strings are engraved and therefore remove positive volume.
    assert float(shape.volume) < base_minus_holes - 1.0
    # Engraving is shallow; it must not create a second solid or pierce the floor.
    assert len(shape.solids()) == 1
    assert shape.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)


def test_written_step_and_model_only_3mf_roundtrip_are_valid() -> None:
    assert STEP.is_file() and STEP.stat().st_size > 0
    assert THREEMF.is_file() and THREEMF.stat().st_size > 0
    assert PROVENANCE.is_file() and PROVENANCE.stat().st_size > 0

    source_shape = coupon.build_coupon()
    exported_step = import_step(STEP)
    assert len(exported_step.solids()) == 1
    assert exported_step.is_valid
    assert float(exported_step.volume) == pytest.approx(float(source_shape.volume), abs=1e-4)
    assert exported_step.bounding_box().size == pytest.approx(
        source_shape.bounding_box().size, abs=1e-6
    )
    exported_radii = _circular_edge_radii(exported_step)
    for diameter in coupon.DEFAULTS.hole_diameters:
        assert sum(
            radius == pytest.approx(diameter / 2.0, abs=1e-8)
            for radius in exported_radii
        ) == 2

    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.QueryReader("3mf").ReadFromFile(str(THREEMF))
    assert model.GetUnit() == lib3mf.ModelUnit.MilliMeter
    iterator = model.GetMeshObjects()
    names: list[str] = []
    while iterator.MoveNext():
        mesh = iterator.GetCurrentMeshObject()
        names.append(mesh.GetName())
        assert mesh.IsValid()
        assert mesh.IsManifoldAndOriented()
        assert mesh.GetVertexCount() > 0
        assert mesh.GetTriangleCount() > 0
    assert names == [coupon.PART_LABEL]
    assert model.GetBuildItems().Count() == 1
    assert len(sha256(STEP.read_bytes()).hexdigest()) == 64
    assert len(sha256(THREEMF.read_bytes()).hexdigest()) == 64
    provenance = json.loads(PROVENANCE.read_text())
    assert provenance["objectCount"] == 1
    assert provenance["unit"] == "millimeter"
    assert provenance["minimumZMm"] == pytest.approx(0.0, abs=1e-7)
    assert provenance["sourceRevisionSha256"] == coupon.source_revision_sha256()
    assert provenance["parameterManifestSha256"] == coupon.parameter_manifest_sha256()
    assert provenance["threeMfSha256"] == sha256(THREEMF.read_bytes()).hexdigest()
    assert provenance["parameterManifest"]["stationOrder"] == [
        "3.70", "3.75", "3.80", "3.85", "3.90", "3.95", "4.00"
    ]
