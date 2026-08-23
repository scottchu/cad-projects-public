from __future__ import annotations

from math import isclose
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh
from build123d import Cylinder, Location, Vector

from p0_optics_fixture_geometry import make_assembly, make_hand, make_pedestal_mask, part_factories, placed_hand
from p0_optics_fixture_spec import P0, local_pad_interference_mm, magnification, penumbra_mm, projected_contract


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p0_optics_fixture"
PRINT_ROOT = MODEL_ROOT / "print"


def _intersection_volume(a, b) -> float:
    result = a.intersect(b)
    if result is None:
        return 0.0
    if hasattr(result, "volume"):
        return float(result.volume)
    return sum(float(shape.volume) for shape in result)


def test_frozen_axial_stack_and_body_contract():
    assert (P0.wall_z_mm, P0.mask_z_mm, P0.source_z_mm) == (-60.0, 0.0, 44.8)
    assert [hand.plane_z_mm for hand in P0.hands] == [1.2, 3.2, 5.2]
    assert (P0.body_rear_diameter_mm, P0.body_mask_diameter_mm, P0.body_depth_mm) == pytest.approx((80.0, 111.1429, 60.0))
    assert P0.journal_land_mm == 1.7
    assert P0.journal_lead_mm == 0.3


def test_projection_math_is_callable_and_mask_projects_to_260_mm():
    result = projected_contract()
    assert result["source_wall_mm"] == pytest.approx(104.8)
    assert result["mask_magnification"] == pytest.approx(104.8 / 44.8)
    assert result["projected_mask_diameter_mm"] == pytest.approx(260.0, abs=0.01)
    assert result["hands"]["hour"]["projected_tip_radius_mm"] == pytest.approx(60 * 104.8 / 43.6)
    assert result["hands"]["minute"]["projected_tip_radius_mm"] == pytest.approx(70 * 104.8 / 41.6)
    assert result["hands"]["second"]["projected_tip_radius_mm"] == pytest.approx(85 * 104.8 / 39.6)
    assert penumbra_mm(0.8, 44.8, 1.2, -60) == pytest.approx(0.8 * 61.2 / 43.6)


def test_part_solid_counts_validity_and_named_dimensions():
    expected_lengths = {"hour_hand": 60.0, "minute_hand": 70.0, "second_hand": 85.0}
    for name, factory in part_factories():
        shape = factory()
        assert shape.is_valid
        assert shape.volume > 0
        assert len(shape.solids()) == 1
        if name in expected_lengths:
            assert shape.bounding_box().max.X == pytest.approx(expected_lengths[name], abs=0.01)
            assert shape.bounding_box().size.Z == pytest.approx(P0.hand_thickness_mm)
    pedestal = make_pedestal_mask()
    bbox = pedestal.bounding_box()
    assert bbox.size.X == pytest.approx(P0.body_mask_diameter_mm, abs=0.002)
    assert bbox.min.Z == pytest.approx(P0.wall_z_mm)
    assert bbox.max.Z == pytest.approx(6.37, abs=0.01)


def test_exact_four_part_assembly_and_plane_positions():
    assembly = make_assembly()
    assert assembly.is_valid
    assert len(assembly.solids()) == 4
    for hand in P0.hands:
        placed = placed_hand(hand)
        assert placed.bounding_box().center().Z == pytest.approx(hand.plane_z_mm)
    for a, b in zip(P0.hands, P0.hands[1:]):
        lower = placed_hand(a)
        upper = placed_hand(b)
        assert _intersection_volume(lower, upper) == pytest.approx(0.0, abs=1e-8)
        assert upper.bounding_box().min.Z - lower.bounding_box().max.Z == pytest.approx(0.8)


def test_slit_hubs_three_contact_pads_and_intended_local_interference():
    assert P0.hub_slit_mm == 1.0
    for hand in P0.hands:
        shape = make_hand(hand)
        assert local_pad_interference_mm(hand) == pytest.approx(0.05)
        assert not shape.is_inside(Vector(0, 0, 0))
        # The slit opposite the blade is open at the hub rim.
        assert not shape.is_inside(Vector(-(hand.hub_outer_diameter_mm / 2 - 0.2), 0, 0))
        # A pad on +X intentionally enters the nominal journal by 0.05 mm.
        probe_radius = hand.journal_diameter_mm / 2 - 0.025
        assert shape.is_inside(Vector(probe_radius, 0, 0))


def test_hand_profiles_are_single_tapered_rounded_blades_not_rings_or_spokes():
    source = (ROOT / "p0_optics_fixture_geometry.py").read_text(encoding="utf-8").lower()
    assert "ring" not in source
    assert "spoke" not in source
    assert "star" not in source
    for hand in P0.hands:
        assert hand.tip_width_mm == pytest.approx(2 * hand.tip_radius_mm)
        assert hand.root_width_mm > hand.tip_width_mm


def test_intended_press_contacts_are_small_and_no_unintended_body_collision():
    pedestal = make_pedestal_mask()
    for hand in P0.hands:
        overlap = _intersection_volume(pedestal, placed_hand(hand))
        assert 0.0 < overlap < 1.0


def test_checked_stls_are_watertight_single_shells_when_generated():
    for name, _ in part_factories():
        path = PRINT_ROOT / f"p0_{name}.stl"
        if not path.exists():
            pytest.skip("derived print artifacts not generated yet")
        # STL stores duplicated triangle vertices; merge coincident vertices
        # before topology checks, matching how slicers reconstruct the shell.
        mesh = trimesh.load_mesh(path, process=True)
        assert isinstance(mesh, trimesh.Trimesh)
        assert mesh.is_watertight
        assert mesh.is_volume
        assert len(mesh.split(only_watertight=False)) == 1


def test_four_object_3mf_contract_when_generated():
    path = PRINT_ROOT / "p0_four_part_test_bundle.3mf"
    if not path.exists():
        pytest.skip("derived 3MF not generated yet")
    with ZipFile(path) as package:
        assert package.testzip() is None
        assert {"[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model"} <= set(package.namelist())
        model = ET.fromstring(package.read("3D/3dmodel.model"))
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objects = model.findall("m:resources/m:object", ns)
    build = model.findall("m:build/m:item", ns)
    assert [obj.attrib["name"] for obj in objects] == ["pedestal_mask", "hour_hand", "minute_hand", "second_hand"]
    assert len(objects) == len(build) == 4
    for obj in objects:
        vertices = [
            (float(vertex.attrib["x"]), float(vertex.attrib["y"]), float(vertex.attrib["z"]))
            for vertex in obj.findall("m:mesh/m:vertices/m:vertex", ns)
        ]
        faces = [
            (int(face.attrib["v1"]), int(face.attrib["v2"]), int(face.attrib["v3"]))
            for face in obj.findall("m:mesh/m:triangles/m:triangle", ns)
        ]
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
        assert mesh.is_watertight
        assert mesh.is_volume
        assert len(mesh.split(only_watertight=False)) == 1
