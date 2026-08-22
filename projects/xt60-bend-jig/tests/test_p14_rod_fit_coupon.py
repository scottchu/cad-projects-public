from __future__ import annotations

from hashlib import sha256
import json
from math import pi
from pathlib import Path

import lib3mf
import pytest
from build123d import GeomType, import_step

import xt60_bend_jig.p14_rod_fit_coupon as coupon


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad" / "p14_rod_fit_coupon"
STEP = CAD / "p14_rod_fit_coupon.step"
THREEMF = CAD / "p14_rod_fit_coupon.3mf"
PROVENANCE = CAD / "p14_rod_fit_coupon.provenance.json"
GENERATOR = CAD / "p14_rod_fit_coupon.step.py"


def _circular_edge_records(shape) -> list[tuple[float, float]]:
    return [
        (float(edge.radius), float(edge.center().Z))
        for edge in shape.edges()
        if edge.geom_type == GeomType.CIRCLE
    ]


def test_exact_3x3_station_contract_is_unique_and_monotonic() -> None:
    p = coupon.DEFAULTS
    assert p.hole_diameters == (
        4.00,
        4.05,
        4.10,
        4.15,
        4.20,
        4.25,
        4.30,
        4.35,
        4.40,
    )
    assert coupon.hole_centres(p) == (
        (-14.0, 14.0),
        (0.0, 14.0),
        (14.0, 14.0),
        (-14.0, 0.0),
        (0.0, 0.0),
        (14.0, 0.0),
        (-14.0, -14.0),
        (0.0, -14.0),
        (14.0, -14.0),
    )
    labels = coupon.label_centres(p)
    assert len(labels) == len(set(labels)) == 9
    manifest = coupon.parameter_manifest(p)
    assert manifest["stationOrder"] == [
        "4.00", "4.05", "4.10", "4.15", "4.20", "4.25", "4.30", "4.35", "4.40"
    ]
    assert manifest["interpretation"]["4.00"] == "physical too-tight press control"
    assert len(coupon.parameter_manifest_sha256(p)) == 64


def test_coupon_is_one_closed_positive_flat_xy_solid() -> None:
    p = coupon.DEFAULTS
    shape = coupon.build_coupon(p)
    assert shape.is_valid
    assert len(shape.solids()) == 1
    assert float(shape.volume) > 0.0
    box = shape.bounding_box()
    assert (box.size.X, box.size.Y, box.size.Z) == pytest.approx((40.0, 42.0, 3.0), abs=1e-6)
    assert box.min.Z == pytest.approx(0.0, abs=1e-7)
    assert box.max.Z == pytest.approx(3.0, abs=1e-7)


def test_actual_brep_has_both_45_degree_chamfers_and_2p44_land() -> None:
    p = coupon.DEFAULTS
    assert 0.25 <= p.entrance_chamfer <= 0.30
    assert coupon.cylindrical_land(p) == pytest.approx(2.44, abs=1e-9)
    assert coupon.cylindrical_land(p) >= 2.4
    records = _circular_edge_records(coupon.build_coupon(p))
    for diameter in p.hole_diameters:
        nominal_radius = diameter / 2.0
        entrance_radius = nominal_radius + p.entrance_chamfer
        assert sum(
            radius == pytest.approx(nominal_radius, abs=1e-8)
            and z == pytest.approx(expected_z, abs=1e-8)
            for radius, z in records
            for expected_z in (p.entrance_chamfer, p.plate_thickness - p.entrance_chamfer)
        ) == 2
        assert sum(
            radius == pytest.approx(entrance_radius, abs=1e-8)
            and z == pytest.approx(expected_z, abs=1e-8)
            for radius, z in records
            for expected_z in (0.0, p.plate_thickness)
        ) == 2
        assert entrance_radius - nominal_radius == pytest.approx(p.entrance_chamfer)


def test_actual_chamfer_envelopes_keep_ligament_and_edge_wall_above_3mm() -> None:
    p = coupon.DEFAULTS
    assert coupon.minimum_actual_ligament(p) >= p.minimum_ligament
    assert coupon.minimum_actual_edge_wall(p) >= p.minimum_edge_wall
    manifest = coupon.parameter_manifest(p)
    assert manifest["derived"]["minimumActualLigamentMm"] == pytest.approx(
        coupon.minimum_actual_ligament(p)
    )
    assert manifest["derived"]["minimumActualEdgeWallMm"] == pytest.approx(
        coupon.minimum_actual_edge_wall(p)
    )


def test_actual_label_bounds_keep_at_least_1mm_outline_clearance() -> None:
    p = coupon.DEFAULTS
    clearance = coupon.minimum_label_to_outline_clearance(p)
    assert clearance == pytest.approx(1.54390859140625, abs=1e-9)
    assert clearance >= p.minimum_label_outline_clearance == 1.0
    assert coupon.parameter_manifest(p)["derived"][
        "minimumLabelToOutlineClearanceMm"
    ] == pytest.approx(clearance)


def test_all_nine_labels_remove_real_shallow_top_surface_volume() -> None:
    p = coupon.DEFAULTS
    shape = coupon.build_coupon(p)
    outline_area = p.plate_width * p.plate_depth - p.clipped_corner_size**2 / 2.0
    cylindrical_hole_volume = sum(
        pi * (diameter / 2.0) ** 2 * p.plate_thickness for diameter in p.hole_diameters
    )
    # Chamfers and nine engraved labels both remove volume beyond plain cylinders.
    assert float(shape.volume) < outline_area * p.plate_thickness - cylindrical_hole_volume - 1.0
    assert len(shape.solids()) == 1
    assert shape.bounding_box().min.Z == pytest.approx(0.0, abs=1e-7)


def test_written_step_and_one_object_model_only_3mf_roundtrip() -> None:
    assert STEP.is_file() and STEP.stat().st_size > 0
    assert THREEMF.is_file() and THREEMF.stat().st_size > 0
    assert PROVENANCE.is_file() and PROVENANCE.stat().st_size > 0
    source_shape = coupon.build_coupon()
    exported_step = import_step(STEP)
    assert exported_step.is_valid
    assert len(exported_step.solids()) == 1
    assert float(exported_step.volume) == pytest.approx(float(source_shape.volume), abs=1e-4)
    assert exported_step.bounding_box().size == pytest.approx(source_shape.bounding_box().size, abs=1e-6)
    exported_records = _circular_edge_records(exported_step)
    for diameter in coupon.DEFAULTS.hole_diameters:
        nominal_radius = diameter / 2.0
        entrance_radius = nominal_radius + coupon.DEFAULTS.entrance_chamfer
        assert sum(
            radius == pytest.approx(nominal_radius, abs=1e-7)
            and z == pytest.approx(expected_z, abs=1e-7)
            for radius, z in exported_records
            for expected_z in (
                coupon.DEFAULTS.entrance_chamfer,
                coupon.DEFAULTS.plate_thickness - coupon.DEFAULTS.entrance_chamfer,
            )
        ) == 2
        assert sum(
            radius == pytest.approx(entrance_radius, abs=1e-7)
            and z == pytest.approx(expected_z, abs=1e-7)
            for radius, z in exported_records
            for expected_z in (0.0, coupon.DEFAULTS.plate_thickness)
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

    provenance = json.loads(PROVENANCE.read_text())
    assert provenance["objectCount"] == 1
    assert provenance["unit"] == "millimeter"
    assert provenance["minimumZMm"] == pytest.approx(0.0, abs=1e-7)
    assert provenance["sourceRevisionSha256"] == coupon.source_revision_sha256()
    assert provenance["parameterManifestSha256"] == coupon.parameter_manifest_sha256()
    assert provenance["stepSha256"] == sha256(STEP.read_bytes()).hexdigest()
    assert provenance["threeMfSha256"] == sha256(THREEMF.read_bytes()).hexdigest()
    assert provenance["generatorSha256"] == sha256(GENERATOR.read_bytes()).hexdigest()
