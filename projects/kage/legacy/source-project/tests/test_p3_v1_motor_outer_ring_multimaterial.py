"""Frozen geometry, isolation, placement, and artifact tests for KAGE P3 V1."""

from __future__ import annotations

from hashlib import sha256
import json
from math import atan2, cos, degrees, pi, sin
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Box, Location, Vector, import_step

from p3_v0_motor_outer_ring_spec import P3_V0
from p3_v1_motor_outer_ring_multimaterial_geometry import (
    lobe_interface_radius,
    make_assembled,
    make_drive_material_pair,
    make_drive_pinch_tool,
    make_drive_split_tool,
    make_drive_wheel_compound,
    make_idler_material_pair,
    make_idler_wheel_compound,
    positive_intersection_volume,
)
from p3_v1_motor_outer_ring_multimaterial_spec import P3_V0_SOURCE_SHA256, P3_V1 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v1_motor_outer_ring_multimaterial"
CORE_NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}

P3_V0_PRIMARY_ARTIFACT_SHA256 = {
    "models/p3_v0_motor_outer_ring/p3_v0_assembled.step": "4e44e72d318346ba0f2997698fef0a6668e313c831dda360d8f38fb21e80e284",
    "models/p3_v0_motor_outer_ring/p3_v0_service_exploded.step": "e9cd7fe526e445599be0ea8c266ce43d8c8299a27880d6418a2f05100af369a7",
    "models/p3_v0_motor_outer_ring/p3_v0_axial_section.step": "ba35ab9c64300a436af5c7496e264e926ea2e1a2a958be9931bac713c028febc",
    "models/p3_v0_motor_outer_ring/p3_v0_drive_wheel.step": "47c54f3947a5d353b4bac5d13fefc2ed92035c121afdc2b1852fd850bbab1d46",
    "models/p3_v0_motor_outer_ring/p3_v0_drive_tire.step": "d028f9617326f19e7a392ecdfa607dcb52773cde91d9b469db209afdc6ff5314",
    "models/p3_v0_motor_outer_ring/p3_v0_idler_wheel.step": "46291e12730d11b1683b6a40f052d30532030e09e7a5a69099d55693fb82d3e6",
    "models/p3_v0_motor_outer_ring/p3_v0_idler_tire.step": "5d91b328ddc9eda6ccd44f8b7016947f8d06005dcffcb93ed5ab17442a6274ac",
    "models/p3_v0_motor_outer_ring/print/p3_v0_print_manifest.json": "aed1aaf887813e24dcdf4e1d99b9321e3ba44efa1c3ff358d1392227c087154b",
}


def _probe(x: float, y: float, z: float, size: float = 0.04):
    return Box(size, size, size, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(
        Location((x, y, z))
    )


def _inside(shape, radius: float, theta: float, z: float) -> bool:
    return shape.is_inside(Vector(radius * cos(theta), radius * sin(theta), z))


def test_frozen_multimaterial_dimensions_and_unchanged_interfaces():
    assert p.wheel_width == 2.60
    assert p.end_band_width == 0.60
    assert p.center_z_local == (0.60, 2.00)
    assert p.center_width == 1.40
    assert p.lobe_count == 6 and p.lobe_samples_per_lobe == 24
    assert (p.drive_contact_radius, p.drive_crest_radius, p.drive_valley_radius) == (6.0, 5.0, 4.2)
    assert (p.idler_contact_radius, p.idler_crest_radius, p.idler_valley_radius) == (4.0, 3.0, 2.4)
    assert (p.drive_bore_diameter, p.idler_bore_diameter) == (4.10, 3.20)
    assert p.drive_z == p.idler_z == (2.9, 5.5)
    assert p.drive_axis_radius == P3_V0.motor_axis_radius_start == 145.8
    assert p.idler_axis_radius == P3_V0.idler_axis_radius_start == 143.8
    assert p.drive_nominal_compression == pytest.approx(0.20)
    assert p.idler_nominal_compression == pytest.approx(0.20)


def test_p3_v0_sources_and_primary_artifacts_are_byte_identical():
    for relative, expected in {**P3_V0_SOURCE_SHA256, **P3_V0_PRIMARY_ARTIFACT_SHA256}.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative


@pytest.mark.parametrize(
    "role,factory,contact,crest,valley,bore,z0",
    [
        ("drive", make_drive_material_pair, 6.0, 5.0, 4.2, 4.10, 2.9),
        ("idler", make_idler_material_pair, 4.0, 3.0, 2.4, 3.20, 2.9),
    ],
)
def test_each_material_is_one_valid_closed_body_with_exact_bounds_and_no_overlap(
    role, factory, contact, crest, valley, bore, z0
):
    petg, tpu = factory()
    assert len(petg.solids()) == len(tpu.solids()) == 1
    assert petg.is_valid and tpu.is_valid
    assert petg.volume > 1.0 and tpu.volume > 1.0
    assert positive_intersection_volume(petg, tpu) == pytest.approx(0.0, abs=1e-8)
    fused = petg.fuse(tpu)
    assert len(fused.solids()) == 1 and fused.is_valid
    assert fused.volume == pytest.approx(petg.volume + tpu.volume, abs=1e-7)
    bounds = tpu.bounding_box()
    assert (bounds.min.X, bounds.min.Y, bounds.min.Z) == pytest.approx((-contact, -contact, z0), abs=1e-6)
    assert (bounds.max.X, bounds.max.Y, bounds.max.Z) == pytest.approx((contact, contact, z0 + p.wheel_width), abs=1e-6)
    assert petg.bounding_box().min.Z == pytest.approx(z0)
    assert petg.bounding_box().max.Z == pytest.approx(z0 + p.wheel_width)
    # The rigid core exists through the full width, and the bore is open
    # through every PETG layer.
    for z in (z0 + 0.30, z0 + 1.30, z0 + 2.30):
        assert _inside(petg, valley - 0.1, pi / 2, z)
        assert not _inside(petg, bore / 2.0 - 0.04, pi / 2, z)


@pytest.mark.parametrize(
    "factory,contact,crest,valley,z0",
    [
        (make_drive_material_pair, 6.0, 5.0, 4.2, 2.9),
        (make_idler_material_pair, 4.0, 3.0, 2.4, 2.9),
    ],
)
def test_tpu_is_one_full_width_tread_with_both_end_lock_lips_and_axial_shoulders(
    factory, contact, crest, valley, z0
):
    petg, tpu = factory()
    lip_radius = (valley + crest) / 2.0
    # TPU occupies the annular locking lips at both wheel ends.  At the same
    # radius in the lobed center it is displaced by the PETG crest, proving a
    # positive axial shoulder instead of a center-only TPU sleeve.
    # Probe a crest away from the drive wheel's intentional split-clamp slot.
    crest_theta = pi / 3.0
    for z in (z0 + 0.30, z0 + 2.30):
        assert _inside(tpu, lip_radius, crest_theta, z)
        assert not _inside(petg, lip_radius, crest_theta, z)
    assert _inside(petg, lip_radius, crest_theta, z0 + 1.30)
    assert not _inside(tpu, lip_radius, crest_theta, z0 + 1.30)
    # The outer tread stays continuous in Z and at its exact contact radius.
    for z in (z0 + 0.30, z0 + 1.30, z0 + 2.30):
        assert _inside(tpu, contact - 0.05, pi / 7, z)


def test_exact_six_lobe_interface_and_petg_only_drive_cuts():
    assert lobe_interface_radius(0.0, 5.0, 4.2) == pytest.approx(5.0)
    assert lobe_interface_radius(pi / 6.0, 5.0, 4.2) == pytest.approx(4.2)
    for k in range(6):
        assert lobe_interface_radius(k * pi / 3.0, 5.0, 4.2) == pytest.approx(5.0)
    petg, tpu = make_drive_material_pair()
    split = make_drive_split_tool()
    pinch = make_drive_pinch_tool()
    assert positive_intersection_volume(petg, split) == pytest.approx(0.0, abs=1e-8)
    assert positive_intersection_volume(petg, pinch) == pytest.approx(0.0, abs=1e-8)
    assert positive_intersection_volume(tpu, split) > 1.0
    assert positive_intersection_volume(tpu, pinch) > 1e-4


def test_compounds_are_two_aligned_material_bodies():
    for wheel in (make_drive_wheel_compound(), make_idler_wheel_compound()):
        assert len(wheel.solids()) == 2
        labels = {child.label for child in wheel.children}
        assert any("PETG" in label for label in labels)
        assert any("TPU" in label for label in labels)


def test_assembly_keeps_one_drive_and_two_idler_axes_at_v0_datums():
    assembly = make_assembled()
    material_children = [child for child in assembly.children if "p3_v1_" in (child.label or "")]
    assert len(material_children) == 6
    centers = []
    for child in material_children:
        center = child.bounding_box().center()
        centers.append((child.label, (center.X**2 + center.Y**2) ** 0.5, degrees(atan2(center.Y, center.X)) % 360.0))
    drive = [entry for entry in centers if "drive" in entry[0]]
    idlers = [entry for entry in centers if "idler" in entry[0]]
    assert len(drive) == 2 and len(idlers) == 4
    for _, radius, angle in drive:
        assert radius == pytest.approx(145.8, abs=0.01)
        assert angle == pytest.approx(270.0, abs=0.01)
    for _, radius, angle in idlers:
        assert radius == pytest.approx(143.8, abs=0.01)
        assert angle == pytest.approx(30.0 if angle < 90.0 else 150.0, abs=0.01)


def test_generated_step_artifacts_import_as_expected_multibody_geometry():
    expected = {
        "p3_v1_assembled.step": 27,
        "p3_v1_drive_wheel_multimaterial.step": 2,
        "p3_v1_idler_wheel_multimaterial.step": 2,
        "p3_v1_material_exploded.step": 4,
    }
    for filename, solids in expected.items():
        path = MODEL_ROOT / filename
        assert path.exists() and path.stat().st_size > 10_000
        imported = import_step(path)
        assert imported.is_valid and len(imported.solids()) == solids


def _parse_3mf(path: Path):
    with ZipFile(path) as package:
        assert package.testzip() is None
        root = ElementTree.fromstring(package.read("3D/3dmodel.model"))
    return root


@pytest.mark.parametrize("role,diameter", [("drive", 12.0), ("idler", 8.0)])
def test_aligned_3mf_has_two_explicit_material_objects_and_fits_bed(role, diameter):
    path = MODEL_ROOT / "print" / f"p3_v1_{role}_wheel_PETG_TPU.3mf"
    root = _parse_3mf(path)
    assert root.attrib["unit"] == "millimeter"
    bases = root.findall(".//m:basematerials/m:base", CORE_NS)
    assert [(base.attrib["name"], base.attrib["displaycolor"]) for base in bases] == [
        ("PETG", f"{p.petg_display_color}FF"),
        ("TPU", f"{p.tpu_display_color}FF"),
    ]
    objects = root.findall(".//m:object", CORE_NS)
    items = root.findall(".//m:item", CORE_NS)
    assert len(objects) == len(items) == 2
    assert [obj.attrib["pindex"] for obj in objects] == ["0", "1"]
    assert all(obj.attrib["pid"] == "1" for obj in objects)
    assert "PETG" in objects[0].attrib["name"] and "TPU" in objects[1].attrib["name"]
    transforms = [item.attrib["transform"] for item in items]
    assert transforms[0] == transforms[1]
    tx, ty, tz = map(float, transforms[0].split()[9:12])
    all_points = []
    for obj in objects:
        points = [
            (float(v.attrib["x"]) + tx, float(v.attrib["y"]) + ty, float(v.attrib["z"]) + tz)
            for v in obj.findall(".//m:vertex", CORE_NS)
        ]
        assert points
        all_points.extend(points)
    assert min(x for x, _, _ in all_points) == pytest.approx(5.0, abs=1e-5)
    assert min(y for _, y, _ in all_points) == pytest.approx(5.0, abs=1e-5)
    assert min(z for _, _, z in all_points) == pytest.approx(0.0, abs=1e-5)
    assert max(x for x, _, _ in all_points) <= 251.0
    assert max(y for _, y, _ in all_points) <= 251.0
    assert max(x for x, _, _ in all_points) - min(x for x, _, _ in all_points) == pytest.approx(diameter, abs=0.03)


def test_multimaterial_manifest_is_explicit_but_requires_slicer_tool_confirmation():
    manifest = json.loads((MODEL_ROOT / "print" / "p3_v1_multimaterial_manifest.json").read_text())
    assert len(manifest["packages"]) == 2
    assert all(package["material_assignments_embedded"] for package in manifest["packages"])
    assert all(package["materials"] == ["PETG", "TPU"] for package in manifest["packages"])
    assert "Confirm filament/tool mapping" in manifest["note"]
