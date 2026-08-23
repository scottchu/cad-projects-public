"""Focused acceptance tests for Q3 r2 roller mounts and inner screws."""

from __future__ import annotations

from copy import deepcopy
from math import pi
from pathlib import Path

import pytest
from build123d import Axis, Location, export_brep

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_geometry import (
    LAPS,
    lapped_sector_shapes,
    local_point,
    printable_sector_shape,
    seam_mount_hole_tools,
    sector_shapes,
)
from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC as BASE_SPEC
from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_geometry import (
    assembled_hardware_shapes,
    assembled_shape,
    canonical_printable_sector_shape,
    canonical_roller_mount_shape,
    canonical_roller_mount_uncut_shape,
    free_roller_keepout_shapes,
    intersection_volume_mm3,
    motor_keepout_shapes,
    mount_base_intersection_volumes_mm3,
    printable_bounds_with_brim,
    printable_roller_mount_shape,
    ring_motion_keepout_shape,
    roller_mount_hole_tools,
    roller_mount_instance_shape,
    roller_mount_print_bounds_mm,
    service_exploded_shape,
)
from p3_v3_mvp_base_q3_r2_roller_mount_inner_screws_spec import MODEL_ROOT, NAMESPACE, SPEC


def test_r2_canonical_sector_is_byte_identical_r0_brep(tmp_path: Path):
    baseline_path = tmp_path / "r0_sector.brep"
    r2_path = tmp_path / "r2_sector.brep"
    export_brep(printable_sector_shape(1), str(baseline_path))
    export_brep(canonical_printable_sector_shape(), str(r2_path))
    assert r2_path.read_bytes() == baseline_path.read_bytes()


def test_base_keeps_exactly_four_holes_per_seam_and_two_lap_owners():
    assert BASE_SPEC.seam_angles_deg == (60.0, 180.0, 300.0)
    assert BASE_SPEC.seam_hole_row_radii_mm == (76.0, 118.0)
    assert BASE_SPEC.roller_mount_tangent_offsets_mm == (-7.0, 7.0)
    assert BASE_SPEC.roller_mount_hole_diameter_mm == pytest.approx(3.3)
    assert BASE_SPEC.seam_holes_per_seam == 4
    assert len(seam_mount_hole_tools()) == 12
    lapped = lapped_sector_shapes()
    finished = sector_shapes()
    for hole in seam_mount_hole_tools():
        owners = [
            index
            for index, sector in enumerate(lapped)
            if intersection_volume_mm3(sector, hole) > BASE_SPEC.brep_tolerance_mm3
        ]
        assert len(owners) == 2
        assert all(
            intersection_volume_mm3(finished[index], hole) <= BASE_SPEC.brep_tolerance_mm3
            for index in owners
        )


def test_mount_has_only_outer_pair_and_full_three_mm_bore_ligament():
    assert SPEC.mount_hole_axes_local_rt_mm == ((118.0, -7.0), (118.0, 7.0))
    assert len(roller_mount_hole_tools()) == 2
    assert SPEC.minimum_actual_mount_ligament_mm == pytest.approx(3.0)
    assert SPEC.minimum_actual_mount_ligament_mm >= SPEC.minimum_mount_ligament_mm
    assert SPEC.lower_owner_contact_band_mm == pytest.approx(4.0)

    uncut = canonical_roller_mount_uncut_shape()
    mount = canonical_roller_mount_shape()
    expected_removed = 2.0 * pi * (SPEC.mount_hole_diameter_mm / 2.0) ** 2 * SPEC.mount_thickness_mm
    assert uncut.volume - mount.volume == pytest.approx(expected_removed, abs=0.02)
    assert len(list(mount.solids())) == 1
    assert mount.is_valid and mount.volume > 0.0


def test_three_mounts_are_rotationally_identical_and_at_only_seam_stations():
    reference = canonical_roller_mount_shape()
    assert SPEC.mount_instance_angles_deg == (60.0, 180.0, 300.0)
    for angle in SPEC.mount_instance_angles_deg:
        aligned = roller_mount_instance_shape(angle).rotate(Axis.Z, -angle)
        assert aligned.volume == pytest.approx(reference.volume, abs=1.0e-5)
        assert intersection_volume_mm3(reference, aligned) == pytest.approx(reference.volume, abs=1.0e-3)


def test_each_mount_is_flush_nonpenetrating_and_positive_epsilon_contacts_both_owners():
    sectors = sector_shapes()
    assert max(mount_base_intersection_volumes_mm3()) <= SPEC.brep_tolerance_mm3
    for _name, angle, upper_index, lower_index in LAPS:
        mount = roller_mount_instance_shape(angle)
        assert mount.distance_to(sectors[upper_index]) == pytest.approx(0.0, abs=1.0e-7)
        assert mount.distance_to(sectors[lower_index]) == pytest.approx(0.0, abs=1.0e-7)
        pressed = deepcopy(mount).moved(Location((0.0, 0.0, -SPEC.contact_probe_epsilon_mm)))
        assert intersection_volume_mm3(pressed, sectors[upper_index]) > 0.0
        assert intersection_volume_mm3(pressed, sectors[lower_index]) > 0.0


def test_modeled_ring_motor_and_free_roller_keepouts_are_clear():
    ring_keepout = ring_motion_keepout_shape()
    motor_keepouts = motor_keepout_shapes()
    roller_keepouts = free_roller_keepout_shapes()
    assert len(list(ring_keepout.solids())) == 1
    assert len(motor_keepouts) == 3
    assert len(roller_keepouts) == 3
    for index, angle in enumerate(SPEC.mount_instance_angles_deg):
        mount = roller_mount_instance_shape(angle)
        assert intersection_volume_mm3(mount, ring_keepout) <= SPEC.brep_tolerance_mm3
        assert max(intersection_volume_mm3(mount, keepout) for keepout in motor_keepouts) <= SPEC.brep_tolerance_mm3
        assert intersection_volume_mm3(mount, roller_keepouts[index]) <= SPEC.brep_tolerance_mm3
        assert mount.distance_to(roller_keepouts[index]) > 0.0


def test_hardware_envelopes_cover_both_pairs_but_are_not_print_parts():
    hardware = assembled_hardware_shapes()
    screws = [shape for shape in hardware if "_screw_" in shape.label]
    nuts = [shape for shape in hardware if "_nut_" in shape.label]
    assert len(screws) == 12
    assert len(nuts) == 12
    assert sum("inner_plain" in shape.label for shape in hardware) == 12
    assert sum("outer_mount" in shape.label for shape in hardware) == 12
    assert all("hardware_envelope" in shape.label for shape in hardware)

    assembled = assembled_shape()
    exploded = service_exploded_shape()
    assert len(list(assembled.solids())) == 30
    assert len(list(exploded.solids())) == 30


def test_no_standalone_clamp_solids_or_r2_clamp_exports():
    labels = [shape.label.lower() for shape in assembled_shape().solids()]
    assert all("clamp" not in label for label in labels)
    if MODEL_ROOT.exists():
        assert not any("clamp" in path.name.lower() for path in MODEL_ROOT.iterdir())


def test_sector_and_three_mount_layout_fit_snapmaker_u1_usable_area():
    assert max(printable_bounds_with_brim(1)) <= SPEC.u1_usable_xy_mm
    mount = printable_roller_mount_shape()
    assert mount.bounding_box().min.Z == pytest.approx(0.0, abs=1.0e-7)
    span_x, span_y, span_z = roller_mount_print_bounds_mm()
    assert max(span_x, span_y) <= SPEC.u1_usable_xy_mm
    assert span_z == pytest.approx(SPEC.mount_thickness_mm)


def test_r2_source_contract_has_no_inner_mount_axis():
    assert all(radius == BASE_SPEC.roller_axle_radius_mm for radius, _ in SPEC.mount_hole_axes_local_rt_mm)
    assert all(radius != BASE_SPEC.inner_seam_clamp_radius_mm for radius, _ in SPEC.mount_hole_axes_local_rt_mm)
    for angle in SPEC.mount_instance_angles_deg:
        expected = tuple(
            local_point(angle, BASE_SPEC.roller_axle_radius_mm, tangent)
            for tangent in BASE_SPEC.roller_mount_tangent_offsets_mm
        )
        actual = tuple(
            local_point(angle, radius, tangent)
            for radius, tangent in SPEC.mount_hole_axes_local_rt_mm
        )
        for actual_axis, expected_axis in zip(actual, expected, strict=True):
            assert actual_axis == pytest.approx(expected_axis)
