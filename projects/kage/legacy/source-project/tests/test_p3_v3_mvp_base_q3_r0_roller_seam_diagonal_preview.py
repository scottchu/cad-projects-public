"""Meaningful acceptance checks for the isolated Q3 preview branch."""

from __future__ import annotations

from copy import deepcopy

import pytest
from build123d import Axis

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import (
    intersection_volume_mm3,
    lapped_sector_shapes,
    named_sector,
    printable_bounds_with_brim,
    printable_sector_shape,
    seam_mount_hole_tools,
    sector_shapes,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC


def test_three_seams_are_the_three_roller_towers_and_motors_are_mid_sector():
    assert SPEC.seam_angles_deg == (60.0, 180.0, 300.0)
    assert SPEC.motor_station_angles_deg == SPEC.sector_center_angles_deg
    for motor_angle in SPEC.motor_station_angles_deg:
        nearest = min(abs(((motor_angle - seam + 180.0) % 360.0) - 180.0) for seam in SPEC.seam_angles_deg)
        assert nearest == pytest.approx(60.0)


def test_exactly_three_valid_positive_volume_sector_solids():
    sectors = sector_shapes()
    assert len(sectors) == 3
    assert all(len(list(shape.solids())) == 1 for shape in sectors)
    assert all(shape.is_valid and shape.volume > 0.0 for shape in sectors)


def test_assembled_sectors_do_not_overlap_and_keep_locked_envelope():
    sectors = tuple(named_sector(index) for index in range(1, 4))
    overlaps = [
        intersection_volume_mm3(sectors[left], sectors[right])
        for left in range(3)
        for right in range(left + 1, 3)
    ]
    assert max(overlaps) <= SPEC.brep_tolerance_mm3
    compound = deepcopy(sectors[0]).fuse(deepcopy(sectors[1]), deepcopy(sectors[2]))
    box = compound.bounding_box()
    assert box.size.X == pytest.approx(300.0, abs=0.05)
    assert box.size.Y == pytest.approx(300.0, abs=0.05)
    assert box.size.Z == pytest.approx(6.0, abs=0.01)


def test_every_seam_has_the_same_four_hole_mirrored_interface():
    assert SPEC.seam_hole_row_radii_mm == (76.0, 118.0)
    assert SPEC.roller_mount_tangent_offsets_mm == (-7.0, 7.0)
    assert SPEC.seam_holes_per_seam == 4
    assert SPEC.seam_hole_total_count == 12
    assert len(seam_mount_hole_tools()) == 12
    assert SPEC.inner_seam_edge_inset_mm == pytest.approx(6.0)
    assert SPEC.outer_seam_edge_inset_mm == pytest.approx(6.0)
    assert SPEC.seam_hole_radial_baseline_mm == pytest.approx(42.0)
    assert SPEC.seam_bore_edge_margin_mm >= 4.35 - 1.0e-9


def test_no_legacy_radius_100_spine_row_survives_in_q3_contract():
    assert 100.0 not in SPEC.seam_hole_row_radii_mm


def test_each_seam_bore_crosses_exactly_two_lap_owners_then_is_fully_removed():
    lapped = lapped_sector_shapes()
    finished = sector_shapes()
    for hole in seam_mount_hole_tools():
        pre_cut_owners = [
            index for index, sector in enumerate(lapped)
            if intersection_volume_mm3(sector, hole) > SPEC.brep_tolerance_mm3
        ]
        assert len(pre_cut_owners) == 2
        for owner in pre_cut_owners:
            assert intersection_volume_mm3(finished[owner], hole) <= SPEC.brep_tolerance_mm3


def test_roller_bridge_and_bore_rows_stay_inside_the_broad_lap_envelope():
    assert all(SPEC.lap_r_min_mm < radius < SPEC.lap_r_max_mm for radius in SPEC.seam_hole_row_radii_mm)
    assert max(abs(value) for value in SPEC.roller_mount_tangent_offsets_mm) < SPEC.donor_t_half_mm
    assert SPEC.roller_bridge_radial_mm[0] >= SPEC.lap_r_min_mm
    assert SPEC.roller_bridge_radial_mm[1] <= SPEC.lap_r_max_mm


def test_three_finished_sectors_are_rotationally_identical():
    reference = named_sector(1)
    for index, center_angle in ((2, 120.0), (3, 240.0)):
        aligned = named_sector(index).rotate(Axis.Z, -center_angle)
        assert reference.volume == pytest.approx(aligned.volume, rel=0.0, abs=1.0e-4)
        assert intersection_volume_mm3(reference, aligned) == pytest.approx(reference.volume, rel=0.0, abs=1.0e-3)


def test_each_diagonal_sector_fits_the_u1_with_keepout_and_brim():
    for index in range(1, 4):
        span_x, span_y = printable_bounds_with_brim(index)
        assert max(span_x, span_y) <= SPEC.u1_usable_xy_mm
        box = printable_sector_shape(index).bounding_box()
        assert box.min.Z == pytest.approx(0.0, abs=1.0e-7)
        assert tuple(printable_sector_shape(index).location.position) == pytest.approx((0.0, 0.0, 0.0))
