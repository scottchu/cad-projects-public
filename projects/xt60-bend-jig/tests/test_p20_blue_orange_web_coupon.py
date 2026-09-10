from __future__ import annotations

from hashlib import sha256
import json
from math import hypot
from pathlib import Path

from build123d import import_step, import_stl
import lib3mf
import pytest

import xt60_bend_jig.p20_blue_orange_web_coupon as coupon


ROOT = Path(__file__).parents[1]
ITERATION = ROOT / "docs/iterations/p20-blue-orange-web-coupon"
CAD = ROOT / "cad/p20_blue_orange_web_coupon"
STEP = CAD / "p20_blue_orange_web_coupon.step"
THREEMF = CAD / "p20_blue_orange_web_coupon.3mf"
STL = CAD / "p20_blue_orange_web_coupon.stl"
PROVENANCE = CAD / "p20_blue_orange_web_coupon.provenance.json"


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_frozen_contract_hashes_parameters_and_scope() -> None:
    assert _sha(ITERATION / "BRIEF.md") == coupon.BRIEF_SHA256
    assert _sha(ITERATION / "DESIGN.md") == coupon.DESIGN_SHA256
    p = coupon.DEFAULTS
    assert p.path_steps == 360
    assert p.rail_cutter_width_mm == 4.15
    assert p.outer_plate_thickness_mm == 3.20
    assert p.cutter_length_x_mm == 5.20
    assert set(coupon.RAIL_SPECS) == {"blue", "orange"}
    manifest = coupon.parameter_manifest()
    assert manifest["contents"] == ["blue_cutout", "orange_cutout"]
    assert manifest["physicalAcceptanceClaimed"] is False
    assert manifest["productAcceptanceClaimed"] is False
    with pytest.raises(ValueError):
        coupon.trajectory_point("green", 0.5)  # type: ignore[arg-type]


def test_exact_361_point_trajectories_endpoints_extrema_and_determinism() -> None:
    expected = {
        "blue": {
            "start": (-7.5115450045742485, 14.127161485742834),
            "end": (5.286598713468044, 2.135621075408544),
            "bounds": (-7.5115450045742485, 5.286598713468044, 2.135621075408544, 14.127161485742834),
        },
        "orange": {
            "start": (11.313708498984761, 11.313708498984760),
            "end": (5.640152104061318, -6.349660298830027),
            "bounds": (5.640152104061318, 12.033446371474318, -6.349660298830027, 11.313708498984760),
        },
    }
    for rail in ("blue", "orange"):
        first = coupon.sampled_trajectory(rail)
        second = coupon.sampled_trajectory(rail)
        assert len(first) == 361
        assert first == second
        assert first[0].as_tuple() == pytest.approx(expected[rail]["start"], abs=1.0e-12)
        assert first[-1].as_tuple() == pytest.approx(expected[rail]["end"], abs=1.0e-12)
        bounds = (
            min(point.y for point in first),
            max(point.y for point in first),
            min(point.z for point in first),
            max(point.z for point in first),
        )
        assert bounds == pytest.approx(expected[rail]["bounds"], abs=1.0e-12)
        for index, point in enumerate(first):
            assert point == coupon.trajectory_point(rail, index / 360)
    with pytest.raises(ValueError):
        coupon.trajectory_point("blue", -1.0e-12)
    with pytest.raises(ValueError):
        coupon.trajectory_point("orange", 1.0 + 1.0e-12)


def test_named_blue_orange_witness_reproduces_1p72_display_gap() -> None:
    blue = coupon.sampled_trajectory("blue")[coupon.BLUE_WITNESS_INDEX]
    orange = coupon.sampled_trajectory("orange")[coupon.ORANGE_WITNESS_INDEX]
    assert blue.as_tuple() == pytest.approx((5.286598713468044, 2.135621075408544), abs=1.0e-12)
    assert orange.as_tuple() == pytest.approx((10.641121565936023, -0.2577384749490106), abs=1.0e-12)
    center_distance = hypot(orange.y - blue.y, orange.z - blue.z)
    assert center_distance == pytest.approx(coupon.WITNESS_CENTER_DISTANCE_MM, abs=1.0e-12)
    assert coupon.sampled_witness_gap_mm() == pytest.approx(1.7150733085690888, abs=1.0e-12)
    assert round(coupon.sampled_witness_gap_mm(), 2) == 1.72


def test_actual_cutters_coupon_and_boundary_constraints() -> None:
    p = coupon.DEFAULTS
    blue = coupon.build_rail_cutter("blue")
    orange = coupon.build_rail_cutter("orange")
    actual_gap = blue.distance_to(orange)
    assert 1.714 <= actual_gap <= 1.716
    assert round(actual_gap, 2) == 1.72
    assert float((blue & orange).volume) <= 1.0e-9
    assert len(blue.solids()) == len(orange.solids()) == 1
    assert blue.is_valid and orange.is_valid

    shape = coupon.build_coupon()
    bounds = shape.bounding_box()
    assert shape.is_valid
    assert len(shape.solids()) == 1
    assert bounds.min.X == pytest.approx(-1.6, abs=1.0e-9)
    assert bounds.max.X == pytest.approx(1.6, abs=1.0e-9)
    assert (bounds.min.Y, bounds.max.Y) == pytest.approx(coupon.BLANK_Y_BOUNDS, abs=1.0e-9)
    assert (bounds.min.Z, bounds.max.Z) == pytest.approx(coupon.BLANK_Z_BOUNDS, abs=1.0e-9)

    # Each complete cutter passes through the blank; their disjointness proves
    # two separate through-slots rather than one fused opening.
    for cutter in (blue, orange):
        assert cutter.bounding_box().min.X < bounds.min.X
        assert cutter.bounding_box().max.X > bounds.max.X
    assert blue.distance_to(orange) > 0.0

    y_min, y_max = coupon.BLANK_Y_BOUNDS
    z_min, z_max = coupon.BLANK_Z_BOUNDS
    outer_webs = []
    for cutter in (blue, orange):
        cb = cutter.bounding_box()
        outer_webs.extend((cb.min.Y - y_min, y_max - cb.max.Y, cb.min.Z - z_min, z_max - cb.max.Z))
    assert min(outer_webs) == pytest.approx(p.ordinary_min_web_mm, abs=1.0e-9)


def test_print_orientation_has_broad_face_at_build_z_zero() -> None:
    source = coupon.build_coupon()
    printed = coupon.build_print_coupon()
    source_bounds = source.bounding_box()
    print_bounds = printed.bounding_box()
    assert print_bounds.min.Z == pytest.approx(0.0, abs=1.0e-9)
    assert print_bounds.max.Z == pytest.approx(coupon.DEFAULTS.outer_plate_thickness_mm, abs=1.0e-9)
    assert sorted((print_bounds.size.X, print_bounds.size.Y)) == pytest.approx(
        sorted((source_bounds.size.Y, source_bounds.size.Z)), abs=1.0e-9
    )
    assert float(printed.volume) == pytest.approx(float(source.volume), abs=1.0e-8)
    assert printed.is_valid and len(printed.solids()) == 1


def test_written_step_meshes_and_provenance_match_source() -> None:
    for path in (STEP, THREEMF, STL, PROVENANCE):
        assert path.is_file() and path.stat().st_size > 0

    source = coupon.build_coupon()
    exported = import_step(STEP)
    assert exported.is_valid and len(exported.solids()) == 1
    assert float(exported.volume) == pytest.approx(float(source.volume), abs=1.0e-4)
    assert exported.bounding_box().size == pytest.approx(source.bounding_box().size, abs=1.0e-6)

    stl = import_stl(STL)
    oriented = coupon.build_print_coupon()
    assert stl.bounding_box().min.Z == pytest.approx(0.0, abs=1.0e-6)
    assert stl.bounding_box().size == pytest.approx(oriented.bounding_box().size, abs=0.002)

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
    assert provenance["schema"] == "P20BlueOrangeWebCouponProvenance/v1"
    assert provenance["candidateStatus"] == "test_only_non_product_coupon"
    assert provenance["parameterManifestSha256"] == coupon.parameter_manifest_sha256()
    assert provenance["stepSha256"] == _sha(STEP)
    assert provenance["threeMfSha256"] == _sha(THREEMF)
    assert provenance["stlSha256"] == _sha(STL)
    assert provenance["physicalAcceptanceClaimed"] is False
    assert provenance["productAcceptanceClaimed"] is False
