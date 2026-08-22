from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Axis, Cylinder, Location, import_step

from p3_v3_direct_gear_race_guidance_geometry import (
    make_fin_360_sweep,
    make_full_role_ring_reference,
)
from p3_v3_mvp_free_roller_r0_three_station_geometry import (
    intersection_volume_mm3,
    make_assembled_spool,
    make_derivative_sector_bed_print,
    make_derivative_sector_print,
    make_print_station_kit,
    make_spacer_print,
    make_spool_print,
    make_station_assembly,
    make_station_frame_print,
    make_three_station_context,
    make_upper_bridge_print,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import local_point, named_sector
from p3_v3_mvp_free_roller_r0_three_station_spec import MODEL_ROOT, SPEC


ROOT = Path(__file__).resolve().parents[1]
LOCKED = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
LOCKED_DIGEST = MODEL_ROOT / "locked_baseline_sha256.json"


def _hash_locked():
    return {
        str(path.relative_to(LOCKED)): sha256(path.read_bytes()).hexdigest()
        for path in sorted(LOCKED.rglob("*"))
        if path.is_file() and path.name != ".DS_Store" and "__pycache__" not in path.parts
    }


def _stable_locked_records():
    return {
        str(path.relative_to(LOCKED)): {
            "bytes": path.stat().st_size,
            "sha256": sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(LOCKED.rglob("*"))
        if path.is_file()
        and path.name != ".DS_Store"
        and "__pycache__" not in path.parts
        and "__cadgen__" not in path.parts
    }


def _planar_face_area_at_z(shape, z_mm: float) -> float:
    return sum(
        face.area
        for face in shape.faces()
        if face.bounding_box().min.Z == pytest.approx(z_mm, abs=1e-7)
        and face.bounding_box().max.Z == pytest.approx(z_mm, abs=1e-7)
    )


def _bottom_mesh_area_from_3mf(path: Path):
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
    vertices = [
        tuple(float(vertex.attrib[axis]) for axis in "xyz")
        for vertex in root.findall(".//m:mesh/m:vertices/m:vertex", ns)
    ]
    triangles = [
        tuple(int(triangle.attrib[key]) for key in ("v1", "v2", "v3"))
        for triangle in root.findall(".//m:mesh/m:triangles/m:triangle", ns)
    ]
    z_min = min(vertex[2] for vertex in vertices)
    bottom_area = 0.0
    for triangle in triangles:
        a, b, c = (vertices[index] for index in triangle)
        if all(vertex[2] == pytest.approx(z_min, abs=1e-7) for vertex in (a, b, c)):
            bottom_area += abs(
                (b[0] - a[0]) * (c[1] - a[1])
                - (b[1] - a[1]) * (c[0] - a[0])
            ) / 2.0
    return z_min, max(vertex[2] for vertex in vertices), bottom_area


def _bottom_mesh_area_from_shape(shape):
    vertices, triangles = shape.tessellate(
        SPEC.mesh_linear_deflection_mm,
        SPEC.mesh_angular_deflection_rad,
    )
    z_min = min(vertex.Z for vertex in vertices)
    bottom_area = 0.0
    for triangle in triangles:
        a, b, c = (vertices[index] for index in triangle)
        if all(vertex.Z == pytest.approx(z_min, abs=1e-7) for vertex in (a, b, c)):
            bottom_area += abs(
                (b.X - a.X) * (c.Y - a.Y)
                - (b.Y - a.Y) * (c.X - a.X)
            ) / 2.0
    return z_min, max(vertex.Z for vertex in vertices), bottom_area


def _volume(shape):
    return sum(s.volume for s in shape.solids())


def test_locked_baseline_does_not_change_during_branch_generation():
    before = _hash_locked()
    make_derivative_sector_print()
    make_three_station_context()
    after = _hash_locked()
    assert before and after == before


def test_locked_baseline_matches_checked_in_digest_manifest_exactly():
    payload = json.loads(LOCKED_DIGEST.read_text())
    assert payload["algorithm"] == "sha256"
    assert payload["locked_root"] == LOCKED.name
    expected = {
        item["path"]: {"bytes": item["bytes"], "sha256": item["sha256"]}
        for item in payload["files"]
    }
    assert expected
    assert _stable_locked_records() == expected


def test_actual_derivative_sector_rear_plane_is_complete_and_unrecessed_in_step_and_3mf():
    accepted = named_sector(1)
    derivative = make_derivative_sector_print()
    accepted_rear_area = _planar_face_area_at_z(accepted, SPEC.base_plate_z_mm[0])
    derivative_rear_area = _planar_face_area_at_z(derivative, SPEC.base_plate_z_mm[0])
    assert derivative.bounding_box().min.Z == pytest.approx(-31.50)
    assert derivative_rear_area == pytest.approx(accepted_rear_area, abs=1e-6)

    written_step = import_step(str(MODEL_ROOT / "derivative_q3_sector_print_qty3.step"))
    step_rear_z = written_step.bounding_box().min.Z
    # The print transform maps the accepted design rear plane Z=-31.50 to the
    # bed plane Z=0 without changing its complete support area.
    assert step_rear_z == pytest.approx(0.0)
    assert _planar_face_area_at_z(written_step, step_rear_z) == pytest.approx(
        accepted_rear_area,
        abs=1e-6,
    )

    source_z_min, source_z_max, source_mesh_area = _bottom_mesh_area_from_shape(
        make_derivative_sector_bed_print()
    )
    mesh_z_min, mesh_z_max, written_mesh_area = _bottom_mesh_area_from_3mf(
        MODEL_ROOT / "derivative_q3_sector_print_qty3.3mf"
    )
    assert (source_z_min, source_z_max) == pytest.approx((0.0, 6.0))
    assert (mesh_z_min, mesh_z_max) == pytest.approx((0.0, 6.0))
    assert written_mesh_area == pytest.approx(source_mesh_area, abs=1e-3)


def test_three_identical_station_instances_and_nine_independent_spools():
    context = make_three_station_context()
    labels = [child.label for child in context.children]
    assert SPEC.station_angles_deg == (60.0, 180.0, 300.0)
    assert sum("_spool_station_" in label for label in labels) == 9
    canonical = make_station_assembly(60.0, include_hardware=False)
    for angle in SPEC.station_angles_deg:
        station = make_station_assembly(angle, include_hardware=False)
        assert _volume(station) == pytest.approx(_volume(canonical), abs=1e-6)


def test_nominal_running_capture_and_tooth_clearance_math():
    assert SPEC.nominal_running_gap_mm == pytest.approx(0.05)
    assert SPEC.nominal_flange_overlap_mm == pytest.approx(0.80)
    assert SPEC.hub_to_tooth_clearance_worst_mm == pytest.approx(0.45)
    assert SPEC.spool_fin_clearance_mm == pytest.approx(3.10)
    for delta in (-SPEC.roller_axis_operating_tolerance_mm, SPEC.roller_axis_operating_tolerance_mm):
        gap = SPEC.carrier_race_radius_mm - (
            SPEC.roller_axis_radius_mm + delta + SPEC.spool_running_od_mm / 2
        )
        overlap = (
            SPEC.roller_axis_radius_mm + delta + SPEC.spool_flange_od_mm / 2
            - SPEC.carrier_race_radius_mm
        )
        assert 0.0 <= gap <= 0.1
        assert 0.75 <= overlap <= 0.85


def test_removable_bridge_has_critic_required_solid_ligaments_and_fin_margin():
    assert SPEC.bridge_radial_ligament_mm == pytest.approx(1.50)
    assert SPEC.bridge_tangential_ligament_mm == pytest.approx(1.50)
    assert min(SPEC.bridge_radial_ligament_mm, SPEC.bridge_tangential_ligament_mm) >= 1.20
    assert SPEC.bridge_fin_clearance_lower_bound_mm >= SPEC.minimum_fin_clearance_mm
    bridge = make_upper_bridge_print()
    assert len(list(bridge.solids())) == 1


def test_printed_parts_are_single_positive_solids_and_fit_u1():
    parts = (
        make_derivative_sector_bed_print(),
        make_station_frame_print(),
        make_upper_bridge_print(),
        make_spool_print(),
        make_spacer_print(),
    )
    for part in parts:
        assert len(list(part.solids())) == 1
        assert _volume(part) > 0
    for part in (make_derivative_sector_bed_print(), make_print_station_kit()):
        box = part.bounding_box()
        assert box.size.X <= SPEC.u1_usable_xy_mm
        assert box.size.Y <= SPEC.u1_usable_xy_mm


def test_actual_spools_do_not_intersect_any_locked_ring():
    rings = [make_full_role_ring_reference(i) for i in range(3)]
    for role in range(3):
        spool = make_assembled_spool(role, 60.0)
        assert [intersection_volume_mm3(spool, ring) for ring in rings] == pytest.approx([0, 0, 0], abs=1e-7)


def test_actual_stationary_parts_clear_locked_rings_and_fin_sweeps():
    station = make_station_assembly(60.0, include_hardware=False)
    stationary = [part for part in station.children if "spool" not in part.label and "spacer" not in part.label]
    rings = [make_full_role_ring_reference(i) for i in range(3)]
    fins = [make_fin_360_sweep(i) for i in range(3)]
    for part in stationary:
        for obstacle in rings + fins:
            assert intersection_volume_mm3(part, obstacle) == pytest.approx(0.0, abs=1e-7)
            assert part.distance_to(obstacle) >= SPEC.minimum_fin_clearance_mm


def test_m3x8_station_screws_follow_existing_clearance_bores_without_touching_lower_leaf():
    sectors = [make_derivative_sector_print().rotate(Axis.Z, angle) for angle in (0.0, 120.0, 240.0)]
    for tangent in SPEC.outer_mount_tangent_mm:
        x, y = local_point(60.0, SPEC.outer_mount_radius_mm, tangent)
        screw = Cylinder(
            SPEC.station_screw_diameter_mm / 2,
            SPEC.station_screw_length_mm,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        ).moved(Location((x, y, SPEC.station_foot_z_mm[1])))
        assert [intersection_volume_mm3(screw, sector) for sector in sectors] == pytest.approx([0, 0, 0], abs=1e-7)
    assert SPEC.nut_pocket_depth_mm >= 2.0


def test_axial_stack_has_six_washers_two_spacers_and_residual_play():
    assert len(SPEC.washer_ranges_z_mm) == 6
    assert len(SPEC.spacer_ranges_z_mm) == 2
    assert all(z1 - z0 == pytest.approx(0.2) for z0, z1 in SPEC.washer_ranges_z_mm)
    assert all(z1 - z0 == pytest.approx(0.8) for z0, z1 in SPEC.spacer_ranges_z_mm)
    assert SPEC.spool_ranges_z_mm[1][0] - SPEC.spool_ranges_z_mm[0][1] - 0.4 - 0.8 == pytest.approx(0.05)
    assert SPEC.spool_ranges_z_mm[2][0] - SPEC.spool_ranges_z_mm[1][1] - 0.4 - 0.8 == pytest.approx(0.05)


def test_derivative_sector_preserves_locked_envelope_and_existing_axes():
    derivative = make_derivative_sector_print().bounding_box()
    assert derivative.min.Z == pytest.approx(SPEC.base_plate_z_mm[0])
    assert derivative.max.Z == pytest.approx(SPEC.base_plate_z_mm[1])
    assert derivative.size.X == pytest.approx(126.53153533, abs=1e-6)
    assert derivative.size.Y == pytest.approx(259.80762114, abs=1e-6)
    assert SPEC.outer_mount_radius_mm == 118.0
    assert SPEC.outer_mount_tangent_mm == (-7.0, 7.0)
    assert SPEC.inner_seam_radius_mm == 76.0


def test_written_step_files_are_fresh_importable_positive_geometry():
    paths = (
        MODEL_ROOT / "derivative_q3_sector_print_qty3.step",
        MODEL_ROOT / "station_frame_print_qty3.step",
        MODEL_ROOT / "upper_bridge_print_qty3.step",
        MODEL_ROOT / "flanged_spool_print_qty9.step",
        MODEL_ROOT / "spacer_print_qty6.step",
        MODEL_ROOT / "three_station_locked_context.step",
    )
    for path in paths:
        assert path.is_file() and path.stat().st_size > 1000
        imported = import_step(str(path))
        assert _volume(imported) > 0


def test_written_3mf_counts_and_manifest_quantities():
    expected = {
        "derivative_q3_sector_print_qty3.3mf": 1,
        "one_station_print_kit_print_qty3.3mf": 7,
    }
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    for filename, object_count in expected.items():
        path = MODEL_ROOT / filename
        assert path.is_file() and path.stat().st_size > 1000
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            root = ElementTree.fromstring(archive.read("3D/3dmodel.model"))
        assert len(root.findall(".//m:resources/m:object", ns)) == object_count
        assert len(root.findall(".//m:build/m:item", ns)) == object_count

    manifest = json.loads((MODEL_ROOT / "print_manifest.json").read_text())
    assert manifest["base"]["object_count"] == 1
    assert manifest["base"]["build_item_count"] == 1
    assert manifest["base"]["print_quantity"] == 3
    assert manifest["canonical_base_policy"] == {
        "artifact_object_count": 1,
        "artifact_build_item_count": 1,
        "copies_per_clock": 3,
        "copies_share_one_canonical_file": True,
        "three_copies_fit_one_u1_bed": False,
    }


def test_branch_contains_no_printed_rail_motor_or_drive_gear_deliverable():
    labels = [child.label.lower() for child in make_three_station_context().children]
    assert not any("motor" in label or "pinion" in label or "electronics" in label for label in labels)
    # Locked ring teeth remain reference geometry; no new drive gear is added.
    assert not any("drive_gear" in label or "guide_rail" in label for label in labels)
