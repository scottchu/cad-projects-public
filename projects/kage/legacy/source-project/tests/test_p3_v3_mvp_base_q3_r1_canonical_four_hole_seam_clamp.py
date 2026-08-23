"""Focused mechanical contracts for the Q3 four-hole flat seam clamp."""

from __future__ import annotations

from copy import deepcopy
from math import pi

import pytest
from build123d import Align, Axis, Cylinder, Location

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import (
    LAPS,
    intersection_volume_mm3,
    lapped_sector_shapes,
    local_point,
    printable_bounds_with_brim,
    printable_sector_shape,
    sector_shapes,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC as BASE_SPEC
from p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp_geometry import (
    assembled_shape,
    canonical_clamp_shape,
    canonical_clamp_uncut_shape,
    canonical_printable_sector_shape,
    clamp_base_intersection_volumes_mm3,
    clamp_hole_axes_world_xy,
    clamp_instance_shape,
    clamp_print_bounds_mm,
    motor_keepout_shapes,
    printable_clamp_shape,
    printable_clamp_qty3_shape,
    ring_motion_keepout_shape,
    roller_keepout_shapes,
)
from p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp_spec import SPEC


def _volume(shape) -> float:
    return float(sum(solid.volume for solid in shape.solids()))


def _vertical_probe(x: float, y: float, z0: float, height: float, diameter: float = 2.8):
    return Cylinder(
        diameter / 2.0,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))


def test_frozen_four_hole_flat_clamp_contract_and_ligaments():
    assert (SPEC.clamp_radial_min_mm, SPEC.clamp_radial_max_mm) == pytest.approx((71.35, 122.65))
    assert (SPEC.clamp_tangent_min_mm, SPEC.clamp_tangent_max_mm) == pytest.approx((-11.65, 17.20))
    assert SPEC.clamp_thickness_mm == pytest.approx(3.0)
    assert SPEC.clamp_hole_axes_local_rt_mm == (
        (76.0, -7.0),
        (76.0, 7.0),
        (118.0, -7.0),
        (118.0, 7.0),
    )
    assert SPEC.clamp_hole_diameter_mm == pytest.approx(3.3)
    assert SPEC.minimum_actual_edge_ligament_mm == pytest.approx(3.0)
    assert SPEC.minimum_actual_edge_ligament_mm >= SPEC.minimum_edge_ligament_mm


def test_clamp_is_one_positive_valid_solid_with_four_actual_through_bores():
    uncut = canonical_clamp_uncut_shape()
    clamp = canonical_clamp_shape()
    solids = list(clamp.solids())
    assert len(solids) == 1
    assert clamp.is_valid and clamp.volume > 0.0
    expected_removed = 4.0 * pi * SPEC.clamp_hole_radius_mm**2 * SPEC.clamp_thickness_mm
    assert uncut.volume - clamp.volume == pytest.approx(expected_removed, rel=0.0, abs=0.02)
    box = clamp.bounding_box()
    assert (box.min.X, box.max.X) == pytest.approx((71.35, 122.65))
    assert (box.min.Y, box.max.Y) == pytest.approx((-11.65, 17.20))
    assert (box.min.Z, box.max.Z) == pytest.approx((BASE_SPEC.plate_top_z_mm, BASE_SPEC.plate_top_z_mm + 3.0))
    for x, y in clamp_hole_axes_world_xy(0.0):
        bore = _vertical_probe(x, y, SPEC.clamp_contact_z_mm - 0.5, SPEC.clamp_thickness_mm + 1.0)
        assert intersection_volume_mm3(clamp, bore) <= SPEC.brep_tolerance_mm3


def test_three_clamps_are_only_rotated_instances_of_one_canonical_part():
    reference = canonical_clamp_shape()
    assert SPEC.clamp_instance_angles_deg == (60.0, 180.0, 300.0)
    for angle in SPEC.clamp_instance_angles_deg:
        aligned = clamp_instance_shape(angle).rotate(Axis.Z, -angle)
        assert aligned.volume == pytest.approx(reference.volume, rel=0.0, abs=1.0e-4)
        assert intersection_volume_mm3(reference, aligned) == pytest.approx(reference.volume, rel=0.0, abs=1.0e-3)
    assert len(list(printable_clamp_qty3_shape().solids())) == 3


def test_clamp_axes_are_coaxial_with_existing_q3_base_bores_at_all_seams():
    for angle in SPEC.clamp_instance_angles_deg:
        expected = tuple(
            local_point(angle, radius, tangent)
            for radius in BASE_SPEC.seam_hole_row_radii_mm
            for tangent in BASE_SPEC.roller_mount_tangent_offsets_mm
        )
        for actual_axis, expected_axis in zip(clamp_hole_axes_world_xy(angle), expected, strict=True):
            assert actual_axis == pytest.approx(expected_axis)
        clamp = clamp_instance_shape(angle)
        for x, y in expected:
            probe = _vertical_probe(x, y, BASE_SPEC.plate_bottom_z_mm - 0.5, BASE_SPEC.plate_thickness_mm + SPEC.clamp_thickness_mm + 1.0)
            assert intersection_volume_mm3(clamp, probe) <= SPEC.brep_tolerance_mm3
            for sector in sector_shapes():
                assert intersection_volume_mm3(sector, probe) <= SPEC.brep_tolerance_mm3


def test_each_screw_axis_is_owned_by_both_adjacent_lap_sectors_across_z():
    lapped = lapped_sector_shapes()
    for _name, angle, upper_index, lower_index in LAPS:
        for radius, tangent in SPEC.clamp_hole_axes_local_rt_mm:
            x, y = local_point(angle, radius, tangent)
            upper_probe = _vertical_probe(x, y, BASE_SPEC.lap_split_z_mm + 0.05, BASE_SPEC.upper_lap_thickness_mm - 0.10)
            lower_probe = _vertical_probe(x, y, BASE_SPEC.plate_bottom_z_mm + 0.05, BASE_SPEC.lower_lap_thickness_mm - 0.10)
            upper_owners = [i for i, sector in enumerate(lapped) if intersection_volume_mm3(sector, upper_probe) > SPEC.brep_tolerance_mm3]
            lower_owners = [i for i, sector in enumerate(lapped) if intersection_volume_mm3(sector, lower_probe) > SPEC.brep_tolerance_mm3]
            assert upper_owners == [upper_index]
            assert lower_owners == [lower_index]


def test_clamps_touch_base_only_at_flush_face_and_clear_motion_keepouts():
    sectors = sector_shapes()
    assert max(clamp_base_intersection_volumes_mm3()) <= SPEC.brep_tolerance_mm3
    ring_keepout = ring_motion_keepout_shape()
    motor_keepouts = motor_keepout_shapes()
    roller_keepouts = roller_keepout_shapes()
    for angle in SPEC.clamp_instance_angles_deg:
        clamp = clamp_instance_shape(angle)
        assert min(clamp.distance_to(sector) for sector in sectors) == pytest.approx(0.0, abs=1.0e-7)
        pressed = deepcopy(clamp).moved(Location((0.0, 0.0, -0.01)))
        assert max(intersection_volume_mm3(pressed, sector) for sector in sectors) > 0.0
        assert intersection_volume_mm3(clamp, ring_keepout) <= SPEC.brep_tolerance_mm3
        assert max(intersection_volume_mm3(clamp, keepout) for keepout in motor_keepouts) <= SPEC.brep_tolerance_mm3
        assert max(intersection_volume_mm3(clamp, keepout) for keepout in roller_keepouts) <= SPEC.brep_tolerance_mm3


def test_accepted_q3_sector_is_geometry_identical_and_print_orientations_fit_u1():
    baseline = printable_sector_shape(1)
    inherited = canonical_printable_sector_shape()
    assert inherited.volume == pytest.approx(baseline.volume, rel=0.0, abs=1.0e-4)
    assert intersection_volume_mm3(inherited, baseline) == pytest.approx(baseline.volume, rel=0.0, abs=1.0e-3)
    assert inherited.bounding_box().min.Z == pytest.approx(0.0, abs=1.0e-7)
    assert printable_clamp_shape().bounding_box().min.Z == pytest.approx(0.0, abs=1.0e-7)
    assert max(printable_bounds_with_brim(1)) <= SPEC.u1_usable_xy_mm
    assert max(clamp_print_bounds_mm()[:2]) <= SPEC.u1_usable_xy_mm


def test_complete_assembled_shape_contains_three_sectors_and_three_clamps_without_overlap():
    assembled = assembled_shape()
    assert len(list(assembled.solids())) == 6
    sectors = sector_shapes()
    clamps = tuple(clamp_instance_shape(angle) for angle in SPEC.clamp_instance_angles_deg)
    assert max(
        intersection_volume_mm3(sectors[left], sectors[right])
        for left in range(3)
        for right in range(left + 1, 3)
    ) <= SPEC.brep_tolerance_mm3
    assert max(
        intersection_volume_mm3(clamps[left], clamps[right])
        for left in range(3)
        for right in range(left + 1, 3)
    ) <= SPEC.brep_tolerance_mm3
