"""Meaningful stack, fastener, and assembly-path gates for the r2 U clamp."""

from __future__ import annotations

from itertools import combinations
import json

import pytest
from build123d import import_step

from p3_v3_mvp_ring_seam_clamp_m2_r2_export import (
    COUPON_STEP,
    MANIFEST,
    PRINT_3MF,
    STACK_STEP,
    read_3mf_names,
)
from p3_v3_mvp_ring_seam_clamp_m2_r2_geometry import (
    _volume,
    authority,
    clamp_slide_rows,
    make_channel_clamp,
    make_hardware_references,
    make_hour_coupon,
    make_production_quadrant,
    make_three_ring_stack,
    print_layout_rows,
)
from p3_v3_mvp_ring_seam_clamp_m2_r2_spec import SPEC


def _all_stack_parts():
    parts = []
    for role in range(3):
        parts.extend(make_production_quadrant(role, quadrant) for quadrant in range(4))
        parts.append(make_channel_clamp(role))
        parts.extend(make_hardware_references(role))
    return parts


def test_locked_authority_and_stack_math_are_frozen_before_export():
    authority()
    SPEC.validate()
    assert SPEC.carrier_layer_pitch_mm == pytest.approx(5.55)
    assert SPEC.clamp_total_height_mm == pytest.approx(5.30)
    assert SPEC.adjacent_clamp_clearance_mm == pytest.approx(0.25)
    assert SPEC.worst_case_adjacent_clamp_clearance_mm == pytest.approx(0.05)


def test_flat_head_length_semantics_select_shortest_credible_screw():
    assert SPEC.nut_thread_engagement_mm(3.0) == pytest.approx(1.0)
    assert SPEC.nut_thread_engagement_mm(3.0) < SPEC.minimum_nut_thread_engagement_mm
    assert SPEC.nut_thread_engagement_mm(4.0) == pytest.approx(SPEC.nut_thickness_mm)
    assert SPEC.selected_standard_screw_length_mm == SPEC.screw_length_mm == 4.0
    assert SPEC.screw_tip_above_ring_bottom_mm == pytest.approx(0.30)


def test_one_piece_u_clamp_is_stack_safe_and_has_continuous_flat_bottom():
    clamps = [make_channel_clamp(role) for role in range(3)]
    for clamp in clamps:
        assert clamp.is_valid and len(clamp.solids()) == 1 and clamp.volume > 0
    assert clamps[0].distance_to(clamps[1]) == pytest.approx(0.25, abs=1e-5)
    assert clamps[1].distance_to(clamps[2]) == pytest.approx(0.25, abs=1e-5)
    for role, clamp in enumerate(clamps):
        z0 = SPEC.carrier_layers[role][0]
        assert clamp.bounding_box().min.Z == pytest.approx(z0 - 1.0, abs=1e-6)


def test_side_loaded_nut_pockets_preserve_top_and_bottom_ring_ligaments():
    assert SPEC.nut_trap_z_ligament_each_face_mm == pytest.approx(0.625)
    for role in range(3):
        for quadrant in (0, 1):
            part = make_production_quadrant(role, quadrant)
            assert part.is_valid and len(part.solids()) == 1 and part.volume > 0


def test_complete_three_ring_stack_has_zero_positive_volume_collisions():
    parts = _all_stack_parts()
    assert len(parts) == 27
    for index, (first, second) in enumerate(combinations(parts, 2)):
        assert _volume(first.intersect(second)) == pytest.approx(0.0, abs=1e-5), (
            index, first.label, second.label
        )


def test_u_clamps_have_collision_free_radial_slide_on_path_with_complete_ring_stack():
    rings = [make_production_quadrant(role, quadrant) for role in range(3) for quadrant in range(4)]
    for role in range(3):
        rows = clamp_slide_rows(role)
        assert len(rows) == SPEC.slide_sample_count
        assert rows[0][0] == pytest.approx(SPEC.slide_start_offset_mm)
        assert rows[-1][0] == pytest.approx(0.0)
        for offset, moving_clamp in rows:
            assert sum(_volume(moving_clamp.intersect(ring)) for ring in rings) == pytest.approx(0.0, abs=1e-5), offset


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
    exported_coupon = import_step(COUPON_STEP)
    source_stack = make_three_ring_stack(include_hardware=True)
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
    assert manifest["stack_math_mm"]["worst_case_adjacent_clamp_clearance"] > 0.0
