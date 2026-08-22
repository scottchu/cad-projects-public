from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import lib3mf
import pytest
from build123d import Align, Box, GeomType, import_step

import xt60_bend_jig.p15_cap_fit_test as caps


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad" / "p15_cap_fit_test"
STEP = CAD / "p15_cap_fit_test.step"
THREEMF = CAD / "p15_cap_fit_test.3mf"
PROVENANCE = CAD / "p15_cap_fit_test.provenance.json"
GENERATOR = CAD / "p15_cap_fit_test.step.py"


def test_parameter_contract_records_physical_coupon_observations() -> None:
    p = caps.DEFAULTS
    assert p.socket_diameters == (4.05, 4.10, 4.15)
    assert p.cap_outer_diameter == 7.0
    assert p.cap_height == 3.8
    assert p.closed_base_thickness == 0.8
    assert p.throat_diameter == 3.6
    assert p.slit_width == 0.6
    assert caps.station_x_positions(p) == (-12.0, 0.0, 12.0)
    assert caps.cavity_depth(p) == pytest.approx(2.4)
    assert caps.minimum_radial_wall(p) == pytest.approx(1.425)
    assert caps.throat_radial_interference_for_nominal_rod(p) == pytest.approx(0.2)
    manifest = caps.parameter_manifest(p)
    assert manifest["priorRigidCouponObservation"]["4.10"].startswith("tight")
    assert manifest["identification"]["4.10"] == "two exterior notches"
    assert len(caps.parameter_manifest_sha256(p)) == 64


def test_each_actual_cap_is_one_valid_positive_upright_solid() -> None:
    p = caps.DEFAULTS
    specimens = caps.build_caps(p)
    assert len(specimens) == 3
    for specimen, expected_x in zip(specimens, caps.station_x_positions(p), strict=True):
        assert specimen.is_valid
        assert len(specimen.solids()) == 1
        assert float(specimen.volume) > 0.0
        box = specimen.bounding_box()
        assert box.size.X == pytest.approx(7.0, abs=1e-6)
        assert box.size.Y == pytest.approx(7.0, abs=1e-6)
        assert box.size.Z == pytest.approx(3.8, abs=1e-6)
        assert (box.min.X + box.max.X) / 2.0 == pytest.approx(expected_x, abs=1e-6)
        assert box.min.Z == pytest.approx(0.0, abs=1e-7)
        assert box.max.Z == pytest.approx(3.8, abs=1e-7)


def test_actual_caps_preserve_closed_base_and_open_flex_slit() -> None:
    p = caps.DEFAULTS
    for index, diameter in enumerate(p.socket_diameters):
        local = caps.build_cap(diameter, index + 1, p)
        # The bottom 0.80 mm is continuous; every cutting feature starts above it.
        bottom_slice = local.intersect(
            Box(
                8.0,
                8.0,
                p.closed_base_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        )
        assert len(bottom_slice.solids()) == 1
        assert float(bottom_slice.solids()[0].volume) == pytest.approx(
            3.141592653589793 * (p.cap_outer_diameter / 2.0) ** 2 * p.closed_base_thickness,
            rel=2e-6,
        )
        # A point in the radial slit above the base must be outside the cap.
        assert not local.is_inside((p.cap_outer_diameter / 2.0 - 0.1, 0.0, 2.0))


def test_three_specimen_layout_is_compact_and_non_overlapping() -> None:
    p = caps.DEFAULTS
    shape = caps.build_cap_fit_test(p)
    assert shape.is_valid
    assert len(shape.solids()) == 3
    box = shape.bounding_box()
    assert (box.size.X, box.size.Y, box.size.Z) == pytest.approx((31.0, 7.0, 3.8), abs=1e-6)
    assert p.station_pitch - p.cap_outer_diameter == pytest.approx(5.0)


def test_written_step_and_three_object_3mf_roundtrip() -> None:
    assert STEP.is_file() and STEP.stat().st_size > 0
    assert THREEMF.is_file() and THREEMF.stat().st_size > 0
    assert PROVENANCE.is_file() and PROVENANCE.stat().st_size > 0
    exported = import_step(STEP)
    source = caps.build_cap_fit_test()
    assert exported.is_valid
    assert len(exported.solids()) == 3
    assert float(exported.volume) == pytest.approx(float(source.volume), abs=1e-4)
    assert exported.bounding_box().size == pytest.approx(source.bounding_box().size, abs=1e-6)
    circular_radii = [
        float(edge.radius)
        for edge in exported.edges()
        if edge.geom_type == GeomType.CIRCLE
    ]
    for diameter in caps.DEFAULTS.socket_diameters:
        assert sum(
            radius == pytest.approx(diameter / 2.0, abs=1e-7)
            for radius in circular_radii
        ) == 2
    assert sum(
        radius == pytest.approx(caps.DEFAULTS.throat_diameter / 2.0, abs=1e-7)
        for radius in circular_radii
    ) == 6

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
    assert names == [specimen.label for specimen in caps.build_caps()]
    assert model.GetBuildItems().Count() == 3

    provenance = json.loads(PROVENANCE.read_text())
    assert provenance["objectCount"] == 3
    assert provenance["unit"] == "millimeter"
    assert provenance["minimumZMm"] == pytest.approx(0.0, abs=1e-7)
    assert provenance["sourceRevisionSha256"] == caps.source_revision_sha256()
    assert provenance["parameterManifestSha256"] == caps.parameter_manifest_sha256()
    assert provenance["stepSha256"] == sha256(STEP.read_bytes()).hexdigest()
    assert provenance["threeMfSha256"] == sha256(THREEMF.read_bytes()).hexdigest()
    assert provenance["generatorSha256"] == sha256(GENERATOR.read_bytes()).hexdigest()
