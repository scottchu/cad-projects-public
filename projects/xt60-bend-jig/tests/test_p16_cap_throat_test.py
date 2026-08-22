from __future__ import annotations

from pathlib import Path

import lib3mf
import pytest
from build123d import GeomType, import_step

import xt60_bend_jig.p16_cap_throat_test as caps


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad" / "p16_cap_throat_test"
STEP = CAD / "p16_cap_throat_test.step"
THREEMF = CAD / "p16_cap_throat_test.3mf"


def test_parameter_contract_isolates_throat_and_records_nozzle() -> None:
    p = caps.DEFAULTS
    assert p.throat_diameters == (4.05, 4.10, 4.15)
    assert p.cavity_diameter == 4.20
    assert p.digit_stroke == 0.80
    assert p.engraving_depth == 0.40
    assert caps.cavity_depth(p) == pytest.approx(2.40)
    assert caps.minimum_radial_wall(p) == pytest.approx(1.40)
    manifest = caps.parameter_manifest(p)
    assert manifest["labels"] == ["405", "410", "415"]
    assert manifest["nozzleContract"]["diameterMm"] == 0.40
    assert "3.60 mm throat dominated" in manifest["p15PhysicalFinding"]


def test_three_labeled_caps_are_valid_separate_upright_solids() -> None:
    p = caps.DEFAULTS
    specimens = caps.build_caps(p)
    assert len(specimens) == 3
    for specimen in specimens:
        assert specimen.is_valid
        assert len(specimen.solids()) == 1
        assert float(specimen.volume) > 0.0
        box = specimen.bounding_box()
        assert box.size.Z == pytest.approx(3.80, abs=1e-6)
        assert box.min.Z == pytest.approx(0.0, abs=1e-7)
        assert box.max.Z == pytest.approx(3.80, abs=1e-7)
    assembly = caps.build_cap_throat_test(p)
    assert assembly.is_valid
    assert len(assembly.solids()) == 3


def test_source_brep_contains_common_cavity_and_three_exact_throats() -> None:
    p = caps.DEFAULTS
    for diameter in p.throat_diameters:
        shape = caps.build_cap(diameter, p)
        radii = [float(edge.radius) for edge in shape.edges() if edge.geom_type == GeomType.CIRCLE]
        assert sum(radius == pytest.approx(p.cavity_diameter / 2.0, abs=1e-8) for radius in radii) == 2
        assert sum(radius == pytest.approx(diameter / 2.0, abs=1e-8) for radius in radii) == 2


def test_written_step_and_3mf_are_valid() -> None:
    assert STEP.is_file() and STEP.stat().st_size > 0
    assert THREEMF.is_file() and THREEMF.stat().st_size > 0
    source = caps.build_cap_throat_test()
    exported = import_step(STEP)
    assert exported.is_valid
    assert len(exported.solids()) == 3
    assert float(exported.volume) == pytest.approx(float(source.volume), abs=1e-4)

    wrapper = lib3mf.Wrapper()
    model = wrapper.CreateModel()
    model.QueryReader("3mf").ReadFromFile(str(THREEMF))
    assert model.GetUnit() == lib3mf.ModelUnit.MilliMeter
    meshes = model.GetMeshObjects()
    count = 0
    while meshes.MoveNext():
        mesh = meshes.GetCurrentMeshObject()
        assert mesh.IsValid()
        assert mesh.IsManifoldAndOriented()
        count += 1
    assert count >= 1
    assert model.GetBuildItems().Count() >= 1
