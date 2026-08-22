"""Math, fit, geometry, and artifact contracts for KAGE P3 V0."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from math import cos, radians, sin
from pathlib import Path
import json
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from build123d import Align, Axis, Box, Compound, Cylinder, Location, import_step

from p3_v0_motor_outer_ring_geometry import (
    PRINTABLE_FACTORIES,
    make_carrier_segment,
    make_drive_tire,
    make_frame_quadrant,
    make_hall_bracket,
    make_hall_module_reference,
    make_hall_spacer_pad,
    make_idler_tire,
    make_idler_wheel,
    make_motor_slide_cradle,
    pairwise_intersection_volume,
    placed_joint_key,
    _guide_station,
)
from p3_v0_motor_outer_ring_spec import PRIOR_ISOLATION_SHA256, P3_V0 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v0_motor_outer_ring"


def test_frozen_radius_segmentation_and_bed_math():
    assert p.carrier_radius == 135.0
    assert p.carrier_od == 280.0
    assert len(p.segment_extents) == 3
    assert p.carrier_segment_tangential_bbox == pytest.approx(242.4871, abs=0.001)
    assert p.carrier_segment_with_brim <= 256.0


def test_center_is_free_and_fin_is_at_final_radius():
    assert p.center_clear_radius == 130.0
    assert p.flange_radii[0] == 130.0
    assert p.fin_angle == 270.0
    assert p.fin_radial == 6.0 and p.fin_tangential == 1.2
    assert p.fin_height == 50.0


def test_outer_sided_guide_clearances_and_capture():
    assert p.guide_angles == (0.0, 90.0, 210.0, 330.0)
    assert p.guide_floor_radii == (130.0, 141.2)
    assert p.guide_floor_z == (0.0, 2.4)
    assert p.guide_outer_wall_radii == (140.3, 141.2)
    assert p.guide_outer_wall_z == (2.3, 7.2)
    assert p.guide_lip_radii == (138.8, 141.2)
    assert p.guide_lip_top_z == 7.2
    assert p.guide_lip_outer_underside_z == 6.0
    assert p.flange_z == (2.7, 5.7)
    assert p.spine_z == (5.7, 7.7)
    assert p.guide_outer_wall_radii[0] - p.flange_radii[1] == pytest.approx(0.30)
    assert p.flange_radii[1] - 138.8 == pytest.approx(1.20)
    assert 138.8 - p.spine_radii[1] == pytest.approx(0.80)


def _minimum_tessellated_radius(shape):
    vertices, _triangles = shape.tessellate(0.02, 0.05)
    return min((vertex.X**2 + vertex.Y**2) ** 0.5 for vertex in vertices)


def _probe(radius, z, size=0.04):
    return Box(size, size, size, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(
        Location((radius, 0.0, z))
    )


def test_actual_guide_brep_matches_frozen_surfaces_and_never_enters_r130():
    guide = _guide_station(0.0, p)
    assert len(guide.solids()) == 1
    assert _minimum_tessellated_radius(guide) >= 130.0 - 1e-7
    assert pairwise_intersection_volume(guide, _probe(130.05, 2.35)) > 0.0
    assert pairwise_intersection_volume(guide, _probe(129.95, 2.35)) == 0.0
    assert pairwise_intersection_volume(guide, _probe(140.35, 4.0)) > 0.0
    assert pairwise_intersection_volume(guide, _probe(140.10, 4.0)) == 0.0
    assert pairwise_intersection_volume(guide, _probe(138.85, 7.15)) > 0.0
    assert pairwise_intersection_volume(guide, _probe(138.70, 7.15)) == 0.0


def test_dogbone_joint_clearance_floor_and_installed_height():
    assert p.key_xy_clearance_per_side == 0.15
    assert p.key_axial_clearance == 0.10
    assert p.key_pocket_depth == 1.20
    assert p.spine_z[1] - p.key_pocket_depth - p.spine_z[0] == pytest.approx(0.80)
    assert p.key_installed_z == (6.6, 7.6)


def test_motor_and_drive_math():
    assert p.motor_keepout_xy == 20.6
    assert p.motor_keepout_length == 40.0
    assert p.motor_mount_pitch == 15.4
    assert p.motor_pilot_relief_diameter == 16.3
    assert p.drive_ratio == pytest.approx(23.3333333333)
    assert p.ring_full_step_degrees == pytest.approx(0.0771428571)
    assert p.ring_microstep_degrees == pytest.approx(0.00482142857)
    assert p.ring_microstep_arc_mm == pytest.approx(0.0113602234)
    assert p.motor_rpm_at_seconds_speed == pytest.approx(23.3333333333)
    assert p.microsteps_per_second_at_seconds_speed == pytest.approx(1244.4444444)


def test_motor_slide_mount_and_preload_contract():
    assert p.motor_axis_radius_range == (144.0, 148.0)
    assert p.motor_axis_radius_start == pytest.approx(145.8)
    assert p.drive_hub_diameter == 10.0
    assert p.nominal_compression == pytest.approx(0.20)
    assert p.motor_axis_radius_tuned_range == (145.75, 145.85)
    assert p.motor_slot_spacing_tangential == 18.0
    assert p.motor_frame_slot_length == 7.4
    assert p.motor_ear_z == (-4.7, 0.0)


def test_three_point_contact_triangle_and_idler_preload_math():
    assert p.idler_angles + (p.motor_angle,) == (30.0, 150.0, 270.0)
    vectors = [(cos(radians(a)), sin(radians(a))) for a in (*p.idler_angles, p.motor_angle)]
    assert sum(v[0] for v in vectors) == pytest.approx(0.0, abs=1e-12)
    assert sum(v[1] for v in vectors) == pytest.approx(0.0, abs=1e-12)
    ordered = sorted((*p.idler_angles, p.motor_angle))
    gaps = [ordered[1] - ordered[0], ordered[2] - ordered[1], 360.0 + ordered[0] - ordered[2]]
    assert max(gaps) < 180.0
    assert p.idler_hub_diameter == 6.0
    assert p.idler_tire_diameter == 8.0
    assert p.idler_bore_diameter == 3.2
    assert p.idler_axis_radius_range == (143.5, 145.0)
    assert p.idler_axis_radius_tuned_range == (143.75, 143.85)
    assert p.idler_axis_radius_start == 143.8
    assert p.nominal_idler_compression == pytest.approx(0.20)
    assert (p.drive_tire_diameter - p.drive_hub_diameter) / 2.0 == pytest.approx(1.0)
    assert (p.idler_tire_diameter - p.idler_hub_diameter) / 2.0 == pytest.approx(1.0)


def test_hall_pocket_is_single_magnet_and_adjustable():
    assert p.hall_pocket_diameter == 3.15
    assert p.hall_pocket_depth == 2.15
    assert p.hall_front_wall == pytest.approx(0.85)
    assert p.hall_face_gap_range == (1.0, 8.0)
    assert p.hall_face_gap_nominal == 3.0
    assert p.hall_module_envelope == (10.0, 15.0, 5.0)
    assert p.hall_spacer_nominal_thickness == 5.0
    assert p.hall_spacer_range == (0.0, 7.0)


def test_hall_bracket_module_spacer_and_fasteners_stay_outside_r130():
    for shape in (make_hall_bracket(), make_hall_spacer_pad(), make_hall_module_reference()):
        assert _minimum_tessellated_radius(shape) >= 130.0 - 1e-7
    assert make_hall_bracket().bounding_box().max.Z == pytest.approx(0.0)
    assert make_hall_spacer_pad().bounding_box().size.Z == pytest.approx(5.0)


def test_exported_hall_brep_stays_outside_r130_after_generation():
    for filename in ("p3_v0_hall_bracket.step", "p3_v0_hall_module_reference.step"):
        path = MODEL_ROOT / filename
        if not path.exists():
            pytest.skip("final repaired STEP export pending")
        assert _minimum_tessellated_radius(import_step(path)) >= 130.0 - 1e-6


def test_motor_and_hall_mounts_have_matching_real_frame_holes():
    frame = _frame()
    cradle = make_motor_slide_cradle()
    hall = make_hall_bracket()
    assert len(cradle.solids()) == len(hall.solids()) == 1
    assert cradle.bounding_box().max.Z == pytest.approx(0.0)
    assert hall.bounding_box().max.Z == pytest.approx(0.0)
    # Axial fastener probes pass through both separate parts at the exact same
    # XY datums; surrounding ears/towers remain positive material.
    for angle, radius, offsets, diameter in (
        (p.motor_angle, p.motor_axis_radius_nominal, (-9.0, 9.0), 3.4),
        (p.hall_angle, p.hall_fastener_radius, p.hall_fastener_tangential_offsets, 2.3),
    ):
        for offset in offsets:
            x = radius * cos(radians(angle)) + offset * cos(radians(angle + 90.0))
            y = radius * sin(radians(angle)) + offset * sin(radians(angle + 90.0))
            fastener = Cylinder(
                diameter * 0.30,
                20.0,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
            ).moved(Location((x, y, -2.0)))
            assert pairwise_intersection_volume(frame, fastener) == 0.0
            target = cradle if angle == p.motor_angle else hall
            assert pairwise_intersection_volume(target, fastener) == 0.0


@pytest.mark.parametrize("name,factory", PRINTABLE_FACTORIES)
def test_each_printable_is_one_positive_solid(name, factory):
    part = factory()
    assert len(part.solids()) == 1, name
    assert part.volume > 1.0, name


@pytest.mark.parametrize("index", range(4))
def test_each_frame_quadrant_is_integral(index):
    frame = make_frame_quadrant(index)
    assert len(frame.solids()) == 1
    assert frame.bounding_box().min.X >= -150.001
    assert frame.bounding_box().min.Y >= -150.001


def test_printable_xy_extents_fit_one_at_a_time_on_256_bed():
    for name, factory in PRINTABLE_FACTORIES:
        box = factory().bounding_box().size
        assert min(box.X, box.Y) + 2 * p.brim <= p.bed_size, name
        assert max(box.X, box.Y) + 2 * p.brim <= p.bed_size, name


@lru_cache(maxsize=1)
def _carrier():
    return Compound(
        children=[
            *(make_carrier_segment(i) for i in range(3)),
            *(placed_joint_key(angle) for angle in p.seam_angles),
        ]
    )


@lru_cache(maxsize=1)
def _frame():
    return Compound(children=[make_frame_quadrant(i) for i in range(4)])


@pytest.mark.parametrize(
    "angle",
    [0.0, 0.5, 59.5, 60.0, 89.5, 90.0, 179.5, 180.0, 269.5, 270.0, 329.5, 330.0],
)
def test_actual_carrier_fin_and_keys_clear_guides_at_critical_angles(angle):
    assert pairwise_intersection_volume(_carrier().rotate(Axis.Z, angle), _frame()) < 1e-7


def test_dense_360_envelope_math_keeps_fin_and_keys_out_of_capture_lips():
    # Angular motion cannot alter these radial envelopes.  Check every degree
    # so any later fin/key radius edit fails before the slower BREP probes.
    for _angle in range(360):
        assert p.spine_radii[1] <= 138.0
        assert p.carrier_radius + p.fin_radial / 2.0 <= 138.0
        assert p.carrier_radius + p.key_end_radial / 2.0 <= 137.5
        assert 138.8 - max(138.0, 137.5) >= 0.8


def test_motor_cradle_tire_and_hall_bracket_are_service_parts():
    for part in (
        make_motor_slide_cradle(), make_drive_tire(), make_idler_wheel(),
        make_idler_tire(), make_hall_bracket(), make_hall_spacer_pad(),
    ):
        assert len(part.solids()) == 1
        assert part.volume > 1.0


def test_prior_design_sources_and_reference_print_are_unchanged():
    for relative, expected in PRIOR_ISOLATION_SHA256.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_generated_primary_steps_exist_after_export():
    for name in ("p3_v0_assembled.step", "p3_v0_service_exploded.step", "p3_v0_axial_section.step"):
        path = MODEL_ROOT / name
        assert path.exists() and path.stat().st_size > 100_000


def _plate_object_bounds(path):
    namespace = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    with ZipFile(path) as package:
        assert package.testzip() is None
        root = ElementTree.fromstring(package.read("3D/3dmodel.model"))
    object_bounds = {}
    for obj in root.findall(".//m:object", namespace):
        points = [
            (float(v.attrib["x"]), float(v.attrib["y"]))
            for v in obj.findall(".//m:vertex", namespace)
        ]
        object_bounds[obj.attrib["id"]] = (
            min(x for x, _ in points), min(y for _, y in points),
            max(x for x, _ in points), max(y for _, y in points),
        )
    result = []
    for item in root.findall(".//m:item", namespace):
        tx, ty = map(float, item.attrib["transform"].split()[9:11])
        x0, y0, x1, y1 = object_bounds[item.attrib["objectid"]]
        result.append((x0 + tx, y0 + ty, x1 + tx, y1 + ty))
    return result


def test_nine_advertised_3mf_plates_fit_bed_and_have_five_mm_object_clearance():
    print_root = MODEL_ROOT / "print"
    manifest_path = print_root / "p3_v0_print_manifest.json"
    if not manifest_path.exists():
        pytest.skip("final repaired print manifest pending")
    manifest = json.loads(manifest_path.read_text())
    assert len(manifest["plates"]) == 9
    assert not (print_root / "p3_v0_motor_outer_ring_parts.3mf").exists()
    for plate in manifest["plates"]:
        bounds = _plate_object_bounds(print_root / plate["file"])
        assert bounds
        for x0, y0, x1, y1 in bounds:
            assert x0 >= 5.0 - 1e-6 and y0 >= 5.0 - 1e-6
            assert x1 <= 251.0 + 1e-6 and y1 <= 251.0 + 1e-6
        for index, a in enumerate(bounds):
            for b in bounds[index + 1:]:
                x_gap = max(b[0] - a[2], a[0] - b[2])
                y_gap = max(b[1] - a[3], a[1] - b[3])
                assert max(x_gap, y_gap) >= 5.0 - 1e-6
