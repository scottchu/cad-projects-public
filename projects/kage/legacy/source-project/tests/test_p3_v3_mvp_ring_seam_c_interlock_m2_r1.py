import json
from math import cos, radians, sin

import pytest
from build123d import Align, Axis, Cylinder, Location, import_step

from p3_v3_mvp_ring_seam_c_interlock_m2_r1_export import (
    COUPON_STEP, MANIFEST, PRINT_3MF, read_3mf_names,
)
from p3_v3_mvp_ring_seam_c_interlock_m2_r1_geometry import (
    _annular_sector, _volume, authority, make_capture_projection,
    make_clean_locked_full_ring, make_hardware_references, make_interlock_male,
    make_interlock_pocket_tool, make_production_quadrant, make_retention_bridge,
    make_shifted_base_quadrant, print_layout_rows,
)
from p3_v3_mvp_ring_seam_c_interlock_m2_r1_spec import SPEC


def _point(radius, angle_deg, z=0.5):
    return (radius * cos(radians(angle_deg)), radius * sin(radians(angle_deg)), z)


def _local_translation(radial_mm=0.0, tangent_mm=0.0, z_mm=0.0):
    a = radians(SPEC.coupon_seam_angle_deg)
    return Location((
        radial_mm * cos(a) - tangent_mm * sin(a),
        radial_mm * sin(a) + tangent_mm * cos(a),
        z_mm,
    ))


def test_shifted_boundaries_sample_valleys_and_each_production_quadrant_has_65_teeth():
    q1 = make_production_quadrant(0, 0)
    q2 = make_production_quadrant(0, 1)
    center_angles = [index * SPEC.tooth_pitch_deg for index in range(SPEC.ring_teeth)]
    assert sum(q1.is_inside(_point(130.0, angle), 1e-6) for angle in center_angles) == 65
    assert sum(q2.is_inside(_point(130.0, angle), 1e-6) for angle in center_angles) == 65
    assert not q1.is_inside(_point(130.0, SPEC.coupon_seam_angle_deg), 1e-6)
    assert not q2.is_inside(_point(130.0, SPEC.coupon_seam_angle_deg), 1e-6)
    assert q1.is_inside(_point(130.0, SPEC.coupon_seam_angle_deg - SPEC.tooth_pitch_deg / 2.0), 1e-6)
    assert q2.is_inside(_point(130.0, SPEC.coupon_seam_angle_deg + SPEC.tooth_pitch_deg / 2.0), 1e-6)


def test_global_260t_phase_race_fin_and_pinion_metadata_remain_locked():
    ring = make_clean_locked_full_ring(0)
    for index in range(SPEC.ring_teeth):
        center = index * SPEC.tooth_pitch_deg
        valley = center + SPEC.tooth_pitch_deg / 2.0
        assert ring.is_inside(_point(130.0, center), 1e-6)
        assert not ring.is_inside(_point(130.0, valley), 1e-6)
    assert SPEC.crop_boundary_shift_deg == pytest.approx(SPEC.locked_global_tooth_phase_deg)
    assert SPEC.carrier_race_radius_mm == 131.60
    assert SPEC.display_fin_angles_deg == (305.0, 45.0, 145.0)
    assert SPEC.global_pinion_phase_delta_deg == 0.0
    assert SPEC.locked_hour_global_pinion_spin_deg == pytest.approx(11.25)
    assert SPEC.shifted_quadrant_local_pinion_phase_deg == pytest.approx(0.0)


def test_production_quadrants_are_actual_solid_zero_delta_outside_local_seam():
    z0, z1 = SPEC.carrier_layers[0]
    envelope = _annular_sector(
        SPEC.protected_radius_mm, SPEC.bridge_outer_radius_mm,
        SPEC.non_seam_exclusion_tangential_width_mm, z0 - 0.2, z1 + 0.2,
    ).rotate(Axis.Z, SPEC.coupon_seam_angle_deg)
    protected = Cylinder(
        SPEC.protected_radius_mm, z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, z0 - 0.2)))
    for quadrant in (0, 1):
        source = make_shifted_base_quadrant(0, quadrant)
        production = make_production_quadrant(0, quadrant)
        source_non_seam = source.cut(envelope)
        production_non_seam = production.cut(envelope)
        assert _volume(source_non_seam.cut(production_non_seam)) == pytest.approx(0.0, abs=1e-6)
        assert _volume(production_non_seam.cut(source_non_seam)) == pytest.approx(0.0, abs=1e-6)
        source_protected = max(source.intersect(protected), key=lambda shape: shape.volume)
        production_protected = max(production.intersect(protected), key=lambda shape: shape.volume)
        assert _volume(source_protected.cut(production_protected)) == pytest.approx(0.0, abs=1e-6)
        assert _volume(production_protected.cut(source_protected)) == pytest.approx(0.0, abs=1e-6)


def test_jigsaw_has_full_thickness_clearance_engagement_neck_and_vertical_drop_fit():
    male = make_interlock_male(0)
    pocket = make_interlock_pocket_tool(0)
    female = make_production_quadrant(0, 1)
    assert SPEC.interlock_engagement_mm == 4.0
    assert SPEC.interlock_neck_width_mm >= 1.20
    assert 0.20 <= SPEC.interlock_xy_clearance_per_side_mm <= 0.25
    assert SPEC.interlock_axial_allowance_mm == 0.10
    assert _volume(male.cut(pocket)) == pytest.approx(0.0, abs=1e-6)
    assert _volume(male.intersect(female)) == pytest.approx(0.0, abs=1e-6)
    probe = SPEC.interlock_xy_clearance_per_side_mm - 0.001
    for move in (
        _local_translation(radial_mm=probe), _local_translation(radial_mm=-probe),
        _local_translation(tangent_mm=probe), _local_translation(tangent_mm=-probe),
        _local_translation(z_mm=SPEC.interlock_axial_allowance_mm / 2.0 - 0.001),
        _local_translation(z_mm=-SPEC.interlock_axial_allowance_mm / 2.0 + 0.001),
    ):
        assert _volume(male.moved(move).cut(pocket)) == pytest.approx(0.0, abs=1e-5)


def test_m2x6_bridge_hardware_has_containment_and_required_engagement():
    quadrants = (make_production_quadrant(0, 0), make_production_quadrant(0, 1))
    bridge = make_retention_bridge(0)
    hardware = make_hardware_references(0)
    assert sum("M2x6" in part.label for part in hardware) == 2
    assert sum("AF4p0_M2_nut" in part.label for part in hardware) == 2
    assert not any("M3" in part.label or "dowel" in part.label.lower() for part in hardware)
    assert SPEC.screw_length_mm - SPEC.bridge_thickness_mm - (SPEC.carrier_layers[0][1] - SPEC.carrier_layers[0][0]) >= SPEC.nut_thickness_mm
    for part in hardware:
        assert _volume(part.intersect(bridge)) == pytest.approx(0.0, abs=1e-6)
        for quadrant in quadrants:
            assert _volume(part.intersect(quadrant)) == pytest.approx(0.0, abs=1e-6)


def test_role_staggering_and_frozen_capture_have_zero_actual_solid_collision():
    for lower, upper in ((0, 1), (1, 2)):
        upper_printed = (
            make_production_quadrant(upper, 0), make_production_quadrant(upper, 1),
            make_retention_bridge(upper),
        )
        for hardware in make_hardware_references(lower):
            for printed in upper_printed:
                assert _volume(hardware.intersect(printed)) == pytest.approx(0.0, abs=1e-6)
    _, children = authority()
    capture = children[14:18]
    for angle in (0.0, 17.0, 43.0, 90.0):
        envelope = make_capture_projection().rotate(Axis.Z, angle)
        assert min(envelope.distance_to(part) for part in capture) >= SPEC.required_capture_clearance_mm - 1e-7
        assert sum(_volume(envelope.intersect(part)) for part in capture) == pytest.approx(0.0, abs=1e-7)


def test_all_coupon_shapes_are_valid_positive_solids_and_layout_fits_270mm():
    printable = (make_production_quadrant(0, 0), make_production_quadrant(0, 1), make_retention_bridge(0))
    for shape in (*printable, *make_hardware_references(0)):
        assert shape.is_valid
        assert len(shape.solids()) == 1
        assert shape.volume > 0.0
    rows = print_layout_rows()
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


def test_exported_artifacts_are_named_and_review_gated():
    coupon = import_step(COUPON_STEP)
    assert len(coupon.children) == 7 and len(coupon.solids()) == 7
    assert read_3mf_names() == [row["shape"].label for row in print_layout_rows()]
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["status"] == "REVIEW_PENDING_NOT_PRINT_READY"
    assert len(manifest["artifacts"]["three_mf"]["objects"]) == 3
    assert manifest["phase_contract"]["pinion_geometry_in_coupon"] is False
