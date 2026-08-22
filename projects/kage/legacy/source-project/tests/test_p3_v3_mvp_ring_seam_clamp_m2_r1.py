"""Meaningful geometry gates for the isolated C-channel seam clamp coupon."""

from __future__ import annotations

import json
from math import cos, radians, sin

import pytest
from build123d import import_step

from p3_v3_mvp_ring_seam_clamp_m2_r1_export import COUPON_STEP, MANIFEST, read_3mf_names
from p3_v3_mvp_ring_seam_clamp_m2_r1_geometry import (
    _volume, authority, clamp_z, make_channel_clamp, make_clean_locked_full_ring,
    make_hardware_references, make_interlock_male, make_interlock_pocket_tool,
    make_production_quadrant, make_role_seam_module, print_layout_rows,
)
from p3_v3_mvp_ring_seam_clamp_m2_r1_spec import SPEC


def _point(radius: float, angle_deg: float, z: float = 0.5):
    return (radius * cos(radians(angle_deg)), radius * sin(radians(angle_deg)), z)


def test_authority_is_locked_and_seam_is_between_complete_teeth():
    authority()
    q1 = make_production_quadrant(0, 0)
    q2 = make_production_quadrant(0, 1)
    centers = [index * SPEC.tooth_pitch_deg for index in range(SPEC.ring_teeth)]
    assert sum(q1.is_inside(_point(130.0, angle), 1e-6) for angle in centers) == 65
    assert sum(q2.is_inside(_point(130.0, angle), 1e-6) for angle in centers) == 65
    assert not q1.is_inside(_point(130.0, SPEC.seam_angle_deg), 1e-6)
    assert not q2.is_inside(_point(130.0, SPEC.seam_angle_deg), 1e-6)
    assert q1.is_inside(_point(130.0, SPEC.seam_angle_deg - SPEC.tooth_pitch_deg / 2.0), 1e-6)
    assert q2.is_inside(_point(130.0, SPEC.seam_angle_deg + SPEC.tooth_pitch_deg / 2.0), 1e-6)


def test_locked_260_tooth_profile_is_unchanged_away_from_local_seam():
    ring = make_clean_locked_full_ring(0)
    for index in range(SPEC.ring_teeth):
        center = index * SPEC.tooth_pitch_deg
        valley = center + SPEC.tooth_pitch_deg / 2.0
        assert ring.is_inside(_point(130.0, center), 1e-6)
        assert not ring.is_inside(_point(130.0, valley), 1e-6)
    assert SPEC.display_fin_angles_deg == (305.0, 45.0, 145.0)
    assert SPEC.carrier_race_radius_mm == pytest.approx(131.6)


def test_existing_alignment_key_retained_with_print_clearance():
    male = make_interlock_male(0)
    pocket = make_interlock_pocket_tool(0)
    female = make_production_quadrant(0, 1)
    assert _volume(male.cut(pocket)) == pytest.approx(0.0, abs=1e-6)
    assert _volume(male.intersect(female)) == pytest.approx(0.0, abs=1e-6)
    assert SPEC.interlock_xy_clearance_per_side_mm == pytest.approx(0.22)


def test_one_piece_channel_has_top_bottom_and_outboard_wall_with_open_inner_side():
    clamp = make_channel_clamp(0)
    bottom_bottom, bottom_top, top_bottom, top_top = clamp_z(0)
    assert clamp.is_valid and len(clamp.solids()) == 1
    assert bottom_top < SPEC.carrier_layers[0][0]
    assert top_bottom > SPEC.carrier_layers[0][1]
    assert top_bottom - bottom_top == pytest.approx(SPEC.clamp_internal_gap_mm)
    assert top_top - bottom_bottom == pytest.approx(SPEC.clamp_total_height_mm)
    assert SPEC.clamp_side_wall_inner_radius_mm >= SPEC.carrier_outer_radius_mm
    assert SPEC.clamp_inner_radius_mm < SPEC.carrier_outer_radius_mm
    assert SPEC.clamp_half_span_mm >= SPEC.clamp_required_overlap_per_half_mm


def test_two_m2_fasteners_each_land_in_solid_and_m2x6_is_proven_too_short():
    assert SPEC.screw_count_per_seam == 2
    assert SPEC.screw_tangential_offsets_mm[0] < 0 < SPEC.screw_tangential_offsets_mm[1]
    assert min(SPEC.screw_inner_ring_ligament_mm, SPEC.screw_outer_ring_ligament_mm) >= SPEC.minimum_hole_edge_ligament_mm
    assert SPEC.minimum_full_nut_engagement_screw_length_mm == pytest.approx(6.65)
    assert 6.0 < SPEC.minimum_full_nut_engagement_screw_length_mm
    assert SPEC.selected_standard_screw_length_mm == SPEC.screw_length_mm == 8.0
    hardware = make_hardware_references(0)
    assert sum("M2x8" in part.label for part in hardware) == 2
    assert sum("captive_AF4_M2_nut" in part.label for part in hardware) == 2
    assert not any("M3" in part.label or "dowel" in part.label.lower() for part in hardware)


def test_assembled_printed_parts_and_hardware_have_only_clearance_or_face_contact():
    printed = [make_production_quadrant(0, 0), make_production_quadrant(0, 1), make_channel_clamp(0)]
    hardware = list(make_hardware_references(0))
    for index, part in enumerate((*printed, *hardware)):
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0
        for other in (*printed, *hardware)[index + 1:]:
            assert _volume(part.intersect(other)) == pytest.approx(0.0, abs=1e-5)
    assert make_channel_clamp(0).distance_to(make_production_quadrant(0, 0)) >= 0.099
    assert make_channel_clamp(0).distance_to(make_production_quadrant(0, 1)) >= 0.099


def test_three_print_objects_fit_u1_bed_with_clearance():
    rows = print_layout_rows()
    assert len(rows) == 3
    for row in rows:
        box = row["shape"].bounding_box()
        assert box.min.X >= SPEC.bed_margin_mm - 1e-7
        assert box.min.Y >= SPEC.bed_margin_mm - 1e-7
        assert box.min.Z >= -1e-7
        assert box.max.X <= SPEC.printer_bed_mm[0] - SPEC.bed_margin_mm + 1e-7
        assert box.max.Y <= SPEC.printer_bed_mm[1] - SPEC.bed_margin_mm + 1e-7
    for index, row in enumerate(rows):
        for other in rows[index + 1:]:
            assert row["shape"].distance_to(other["shape"]) >= SPEC.minimum_layout_gap_mm


def test_export_source_parity_and_review_gate():
    source = make_role_seam_module(0, include_hardware=True)
    exported = import_step(COUPON_STEP)
    assert len(exported.children) == len(source.children) == 7
    assert [child.label for child in exported.children] == [child.label for child in source.children]
    for actual, expected in zip(exported.children, source.children, strict=True):
        assert actual.volume == pytest.approx(expected.volume, rel=1e-7, abs=1e-5)
    assert read_3mf_names() == [row["shape"].label for row in print_layout_rows()]
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["status"] == "REVIEW_PENDING_NOT_PRINT_READY"
    assert manifest["design"]["retention"]["type"] == "one removable three-sided C-channel clamp"
