import json

import pytest
from build123d import Axis, import_step

from p3_v3_mvp_ring_seam_screw_only_r1_export import (
    COUPON_STEP, MANIFEST, PRINT_3MF, read_3mf_names,
)
from p3_v3_mvp_ring_seam_screw_only_r1_geometry import (
    _annular_sector, authority, make_capture_projection, make_hardware_references,
    make_modified_quadrant, make_outboard_pad, print_layout_rows, source_quadrant,
)
from p3_v3_mvp_ring_seam_screw_only_r1_spec import SPEC


def _volume(shape):
    return sum(s.volume for s in shape.solids()) if shape else 0.0


def test_stationary_capture_has_required_actual_solid_clearance_at_representative_rotations():
    _, children = authority()
    capture_parts = children[14:18]
    for angle in (0.0, 17.0, 43.0, 90.0):
        envelope = make_capture_projection().rotate(Axis.Z, angle)
        assert min(envelope.distance_to(part) for part in capture_parts) >= (
            SPEC.required_capture_clearance_mm - 1e-7
        )
        assert sum(_volume(envelope.intersect(part)) for part in capture_parts) == pytest.approx(0.0, abs=1e-7)


def test_role_staggering_has_zero_adjacent_ring_actual_solid_interference():
    for lower, upper in ((0, 1), (1, 2)):
        upper_pad = make_outboard_pad(upper)
        for lower_hardware in make_hardware_references(lower):
            assert _volume(lower_hardware.intersect(upper_pad)) == pytest.approx(0.0, abs=1e-6), (
                lower_hardware.label, upper_pad.label
            )


def test_locked_quadrants_are_zero_delta_outside_declared_seam_envelope():
    envelope = _annular_sector(
        SPEC.seam_local_envelope_inner_radius_mm,
        SPEC.seam_local_envelope_outer_radius_mm,
        SPEC.seam_local_envelope_tangential_width_mm,
        SPEC.carrier_layers[0][0] - 0.2,
        SPEC.carrier_layers[0][1] + 0.2,
    ).rotate(Axis.Z, SPEC.seam_angle_deg)
    for quadrant in (0, 1):
        locked = source_quadrant(0, quadrant).cut(envelope)
        modified = make_modified_quadrant(0, quadrant).cut(envelope)
        assert _volume(locked.cut(modified)) == pytest.approx(0.0, abs=1e-6)
        assert _volume(modified.cut(locked)) == pytest.approx(0.0, abs=1e-6)


def test_printable_and_reference_shapes_are_valid_positive_solids():
    printable = (make_modified_quadrant(0, 0), make_modified_quadrant(0, 1), make_outboard_pad(0))
    for shape in (*printable, *make_hardware_references(0)):
        assert shape.is_valid
        assert len(shape.solids()) == 1
        assert shape.volume > 0.0


def test_print_layout_fits_270_mm_bed_with_actual_solid_gap():
    rows = print_layout_rows()
    for row in rows:
        box = row["shape"].bounding_box()
        assert box.min.X >= SPEC.bed_margin_mm - 1e-7
        assert box.min.Y >= SPEC.bed_margin_mm - 1e-7
        assert box.min.Z >= -1e-7
        assert box.max.X <= SPEC.printer_bed_mm[0] - SPEC.bed_margin_mm + 1e-7
        assert box.max.Y <= SPEC.printer_bed_mm[1] - SPEC.bed_margin_mm + 1e-7
        assert box.max.Z <= SPEC.printer_bed_mm[2] + 1e-7
    for index, row in enumerate(rows):
        for other in rows[index + 1:]:
            assert row["shape"].distance_to(other["shape"]) >= SPEC.minimum_layout_gap_mm


def test_exported_coupon_structure_and_review_gate():
    assert COUPON_STEP.is_file() and COUPON_STEP.stat().st_size > 0
    assert PRINT_3MF.is_file() and PRINT_3MF.stat().st_size > 0
    coupon = import_step(COUPON_STEP)
    assert len(coupon.children) == 7
    assert len(coupon.solids()) == 7
    assert read_3mf_names() == [row["shape"].label for row in print_layout_rows()]
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["status"] == "REVIEW_PENDING_NOT_PRINT_READY"
    assert len(manifest["artifacts"]["three_mf"]["objects"]) == 3
