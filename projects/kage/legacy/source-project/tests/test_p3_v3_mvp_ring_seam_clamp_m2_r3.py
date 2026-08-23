"""Meaningful full-coverage, stack, and station-motion gates for KAGE r3."""

from __future__ import annotations

from itertools import combinations
import json
from math import cos, radians, sin

import pytest
from build123d import Align, Axis, Cylinder, Location, import_step

from p3_v3_mvp_ring_seam_clamp_m2_r3_export import (
    COUPON_STEP,
    MANIFEST,
    PRINT_3MF,
    STACK_STEP,
    read_3mf_names,
)
from p3_v3_mvp_ring_seam_clamp_m2_r3_geometry import (
    _volume,
    authority,
    clamp_slide_rows,
    clamp_station_sweep_rows,
    make_channel_clamp,
    make_hardware_references,
    make_hour_coupon,
    make_production_quadrant,
    make_three_ring_stack,
    print_layout_rows,
    stationary_pinion_and_roller_references,
)
from p3_v3_mvp_ring_seam_clamp_m2_r3_spec import SPEC


def _all_stack_parts():
    parts = []
    for role in range(3):
        parts.extend(make_production_quadrant(role, quadrant) for quadrant in range(4))
        parts.append(make_channel_clamp(role))
        parts.extend(make_hardware_references(role))
    return parts


def test_locked_authority_and_r2_remain_immutable():
    authority()
    SPEC.validate()
    assert SPEC.carrier_layer_pitch_mm == pytest.approx(5.55)
    assert SPEC.clamp_total_height_mm == pytest.approx(5.30)
    assert SPEC.worst_case_adjacent_clamp_clearance_mm == pytest.approx(0.05)


def test_full_radial_coverage_replaces_r2_partial_coverage():
    assert SPEC.r2_ring_body_coverage_mm == pytest.approx(4.30)
    assert SPEC.r2_ring_body_coverage_fraction == pytest.approx(0.671875)
    assert SPEC.full_ring_body_coverage_mm == pytest.approx(6.40)
    assert SPEC.full_ring_body_coverage_fraction == pytest.approx(1.0)
    assert SPEC.clamp_inner_radius_mm == SPEC.tooth_root_radius_mm == pytest.approx(132.50)
    assert SPEC.carrier_outer_radius_mm == pytest.approx(138.90)

    clamp = make_channel_clamp(0)
    angle = radians(SPEC.seam_angle_deg)
    top_z = SPEC.carrier_layers[0][1] + SPEC.clamp_fit_clearance_per_face_mm + 0.5
    for radius in (SPEC.tooth_root_radius_mm + 0.05, SPEC.carrier_outer_radius_mm - 0.05):
        point = (radius * cos(angle), radius * sin(angle), top_z)
        assert clamp.is_inside(point), (radius, point)


def test_tooth_profile_is_radially_exposed_and_screws_are_surrounded():
    assert SPEC.tooth_profile_exposed_radial_width_mm == pytest.approx(3.50)
    assert SPEC.clamp_inner_radial_screw_edge_distance_mm == pytest.approx(2.80)
    assert SPEC.clamp_outer_radial_screw_edge_distance_mm == pytest.approx(2.50)
    clamp = make_channel_clamp(0)
    tooth_keepout = Cylinder(
        SPEC.tooth_root_radius_mm - 0.01,
        SPEC.clamp_total_height_mm + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0, 0, SPEC.carrier_layers[0][0] - 2.0)))
    assert _volume(clamp.intersect(tooth_keepout)) == pytest.approx(0.0, abs=1e-6)


def test_complete_three_ring_stack_has_zero_positive_volume_collisions():
    parts = _all_stack_parts()
    assert len(parts) == 27
    for first, second in combinations(parts, 2):
        assert _volume(first.intersect(second)) == pytest.approx(0.0, abs=1e-5), (first.label, second.label)


def test_full_width_u_clamps_slide_radially_onto_complete_ring_stack():
    rings = [make_production_quadrant(role, quadrant) for role in range(3) for quadrant in range(4)]
    for role in range(3):
        rows = clamp_slide_rows(role)
        assert len(rows) == 11 and rows[0][0] == pytest.approx(10.0) and rows[-1][0] == pytest.approx(0.0)
        for offset, moving_clamp in rows:
            collision = sum(_volume(moving_clamp.intersect(ring)) for ring in rings)
            assert collision == pytest.approx(0.0, abs=1e-5), (role, offset, collision)


def test_rotating_clamps_clear_actual_locked_pinions_and_rollers():
    references = {shape.label: shape for shape in stationary_pinion_and_roller_references()}
    assert len(references) == 12
    for role in range(3):
        rows = clamp_station_sweep_rows(role)
        assert len(rows) == 36
        for label, delta, moving_clamp in rows:
            collision = _volume(moving_clamp.intersect(references[label]))
            assert collision == pytest.approx(0.0, abs=1e-5), (role, label, delta, collision)


def test_print_objects_fit_u1_bed_with_clearance():
    rows = print_layout_rows()
    assert len(rows) == 3
    for row in rows:
        box = row["shape"].bounding_box()
        assert box.min.X >= SPEC.bed_margin_mm - 1e-7
        assert box.min.Y >= SPEC.bed_margin_mm - 1e-7
        assert box.min.Z >= -1e-7
        assert box.max.X <= SPEC.printer_bed_mm[0] - SPEC.bed_margin_mm + 1e-7
        assert box.max.Y <= SPEC.printer_bed_mm[1] - SPEC.bed_margin_mm + 1e-7
    for first, second in combinations(rows, 2):
        assert first["shape"].distance_to(second["shape"]) >= SPEC.minimum_layout_gap_mm


def test_export_source_parity_and_review_gate():
    source_coupon = make_hour_coupon()
    source_stack = make_three_ring_stack(include_hardware=True)
    exported_coupon = import_step(COUPON_STEP)
    exported_stack = import_step(STACK_STEP)
    assert len(exported_coupon.children) == len(source_coupon.children) == 7
    assert len(exported_stack.children) == len(source_stack.children) == 27
    for exported, source in ((exported_coupon, source_coupon), (exported_stack, source_stack)):
        assert [child.label for child in exported.children] == [child.label for child in source.children]
        for actual, expected in zip(exported.children, source.children, strict=True):
            assert actual.volume == pytest.approx(expected.volume, rel=1e-7, abs=1e-5)
    assert read_3mf_names(PRINT_3MF) == [row["shape"].label for row in print_layout_rows()]
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["status"] == "REVIEW_PENDING_NOT_PRINT_READY"
    assert manifest["radial_coverage_mm"]["r3_coverage_percent"] == pytest.approx(100.0)
