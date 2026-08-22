"""Actual-solid keeper correction contract for KAGE P3 V3."""

from __future__ import annotations

from build123d import Location
import pytest

from p3_v3_full_ring_r2_geometry import (
    _full_role_ring,
    keeper_service_offset,
    make_chassis_segments,
    make_frame_segments,
    make_keeper_fastener_references,
    make_keeper_saddle_parts,
    make_outer_front_ring_segments,
    make_output_pinion,
    make_ring_quadrants,
    make_station_support,
)
from p3_v3_full_ring_r2_spec import P3_V3_FULL_RING_R2 as p


def _intersection_volume(left, right) -> float:
    common = left.intersect(right)
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def test_frozen_keeper_bands_channels_walls_and_pending_physical_gate():
    assert p.carrier_layers == ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    assert p.carrier_gaps == pytest.approx((2.55, 2.55))
    assert p.pinion_face_ranges == ((-0.7, 1.4), (4.85, 6.95), (10.4, 12.5))
    assert p.station_role_z_translations == pytest.approx((-4.3, -2.15, 0.0))
    assert p.frame_z == pytest.approx((-6.45, -4.05))
    assert p.rail_neck_depth == pytest.approx(1.0)
    assert p.rail_total_depth == pytest.approx(1.8)
    assert p.keeper_channel_radii == pytest.approx((132.55, 135.85))
    assert p.keeper_radial_clearance == pytest.approx(0.25)
    assert p.keeper_capture_radial >= 0.8
    assert p.keeper_capture_axial >= 1.6
    assert p.keeper_structural_wall_min >= 1.2
    assert p.keeper_pull_test_newtons == pytest.approx(5.0)
    assert p.keeper_pull_test_status == "PENDING_PHYSICAL"


@pytest.mark.parametrize("role", range(3))
def test_exact_axial_capture_bands_leave_0p30_total_float(role):
    z0 = p.carrier_layers[role][0]
    flange = (z0 - 1.8, z0 - 1.0)
    shoe = p.lower_shoe_range(role)
    bridge = p.upper_bridge_range(role)
    assert shoe == pytest.approx((z0 - 2.75, z0 - 1.95))
    assert bridge == pytest.approx((z0 - 0.85, z0 - 0.05))
    assert flange[0] - shoe[1] == pytest.approx(0.15)
    assert bridge[0] - flange[1] == pytest.approx(0.15)
    assert (flange[0] - shoe[1]) + (bridge[0] - flange[1]) == pytest.approx(0.30)
    assert p.race_range(role)[0] - p.frame_z[1] >= 0.75 - 1e-9


@pytest.mark.parametrize("role", range(3))
def test_actual_keeper_shoe_cap_fasteners_and_ring_have_zero_unwanted_brep(role):
    ring = _full_role_ring(role)
    fixed, cap, shoe = make_keeper_saddle_parts(role, 0)
    screws_and_inserts = make_keeper_fastener_references(role, 0)

    assert all(part.is_valid and len(part.solids()) == 1 for part in (fixed, cap, shoe))
    assert all(_intersection_volume(part, ring) <= 1e-7 for part in (fixed, cap, shoe))
    assert _intersection_volume(fixed, cap) <= 1e-7
    assert _intersection_volume(fixed, shoe) <= 1e-7
    assert _intersection_volume(cap, shoe) <= 1e-7
    assert shoe.distance_to(ring) == pytest.approx(0.15, abs=1e-7)
    for part in screws_and_inserts:
        assert part.is_valid and len(part.solids()) == 1
        assert _intersection_volume(part, ring) <= 1e-7


def test_m2p5_cap_hardware_dimensions_wall_and_engagement():
    assert p.keeper_cap_fastener_nominal_diameter == pytest.approx(2.5)
    assert p.keeper_cap_fastener_clearance_diameter == pytest.approx(2.8)
    assert p.keeper_cap_screw_length == pytest.approx(10.0)
    assert p.keeper_boss_outer_diameter == pytest.approx(7.0)
    assert p.keeper_insert_outer_diameter == pytest.approx(3.8)
    assert p.keeper_insert_length == pytest.approx(4.0)
    assert p.keeper_insert_pilot_diameter == pytest.approx(3.6)
    assert p.keeper_insert_pilot_depth == pytest.approx(4.2)
    assert p.keeper_boss_depth >= 4.8
    assert (p.keeper_boss_outer_diameter - p.keeper_insert_outer_diameter) / 2 == pytest.approx(1.6)
    assert p.keeper_insert_length >= p.keeper_insert_engagement_min
    assert p.keeper_fastener_axis_radius + p.keeper_boss_outer_diameter / 2 <= 143.0
    _fixed, cap, _shoe = make_keeper_saddle_parts(0, 0)
    assert max((vertex.X**2 + vertex.Y**2) ** 0.5 for vertex in cap.vertices()) <= 143.0 + 1e-7


@pytest.mark.parametrize("role", range(3))
def test_radially_removed_cap_has_clear_service_position(role):
    ring = _full_role_ring(role)
    _fixed, cap, _shoe = make_keeper_saddle_parts(role, 0)
    dx, dy, dz = keeper_service_offset(role, 0)
    assert (dx * dx + dy * dy) ** 0.5 == pytest.approx(p.keeper_service_radial_travel)
    for fraction in (0.0, 0.25, 0.50, 0.75, 1.0):
        moved = cap.moved(Location((dx * fraction, dy * fraction, dz)))
        assert _intersection_volume(moved, ring) <= 1e-7
    removed = cap.moved(Location((dx, dy, dz)))
    assert removed.distance_to(ring) > 7.0


@pytest.mark.parametrize("role", range(3))
def test_pinion_actual_solid_stays_on_R122_and_exact_face_band(role):
    pinion = make_output_pinion(role)
    bounds = pinion.bounding_box()
    assert bounds.min.Z == pytest.approx(p.pinion_face_ranges[role][0])
    assert bounds.max.Z == pytest.approx(p.pinion_face_ranges[role][1])
    station_angle = p.motor_station_angles[role]
    # Rotation preserves the pitch-axis radius; the OD bounds extend by the
    # pinion radius but the source axis remains exactly R122.
    assert p.output_axis_radius == pytest.approx(122.0)
    assert station_angle in p.motor_station_angles


def test_every_corrected_printed_part_bbox_fits_snapmaker_u1_270mm_bed():
    parts = [*make_frame_segments(), *make_chassis_segments(), *make_outer_front_ring_segments()]
    for role in range(3):
        parts.extend(make_ring_quadrants(role))
        parts.append(make_station_support(role))
        for guide in range(3):
            parts.extend(make_keeper_saddle_parts(role, guide))
    for part in parts:
        bounds = part.bounding_box()
        assert bounds.size.X <= p.printer_bed_xy[0] + 1e-7
        assert bounds.size.Y <= p.printer_bed_xy[1] + 1e-7
