"""Acceptance contracts for the MR84/profiled-spool tower successor."""

from __future__ import annotations

from math import cos, radians, sin

import pytest
from build123d import Align, Cylinder, Location

import p3_v3_mr84_spool_tower_geometry as g
from p3_v3_full_ring_r2_geometry import _full_role_ring as accepted_full_role_ring
from p3_v3_mr84_spool_tower_spec import P3_V3_MR84_SPOOL_TOWER as p


def _volume(common) -> float:
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _base_probe(tower: int, tangent: float, radial_shift: float):
    angle = radians(p.roller_tower_angles[tower])
    radius = p.base_mount_axis_radius + radial_shift
    x = radius * cos(angle) - tangent * sin(angle)
    y = radius * sin(angle) + tangent * cos(angle)
    z0, z1 = p.base_z_range
    return Cylinder(
        p.base_mount_bolt_diameter / 2.0,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0 - 0.2)))


def test_successor_reuses_accepted_keeper_fix_ring_geometry_exactly():
    assert p.rail_flange_radii == pytest.approx((132.8, 135.6))
    assert p.rail_neck_radii == pytest.approx((133.6, 134.8))
    assert p.rail_flange_depth == pytest.approx(0.8)
    assert p.rail_neck_depth == pytest.approx(1.0)
    for role in range(3):
        successor = g.accepted_full_role_ring(role)
        accepted = accepted_full_role_ring(role)
        assert successor is accepted
        assert successor.volume == pytest.approx(accepted.volume, abs=1e-9)
        assert successor.bounding_box().size == accepted.bounding_box().size


def test_exact_nine_mr84_and_profiled_spool_contract():
    assert p.roller_tower_angles == (60.0, 180.0, 300.0)
    assert p.motor_station_angles == (0.0, 120.0, 240.0)
    assert p.roller_center_zs == pytest.approx((-2.9, 2.65, 8.2))
    assert (p.bearing_bore_diameter, p.bearing_outer_diameter, p.bearing_width) == (4.0, 8.0, 3.0)
    assert (p.spool_hub_outer_diameter, p.spool_hub_width) == (10.0, 3.2)
    assert (p.spool_belt_outer_diameter, p.spool_belt_width) == (12.6, 0.6)
    assert p.spool_lip_outer_diameter == pytest.approx(14.4)
    bearings = [g.make_roller_bearing(role, tower) for tower in range(3) for role in range(3)]
    spools = [g.make_roller_spool(role, tower) for tower in range(3) for role in range(3)]
    assert len({part.label for part in bearings}) == len({part.label for part in spools}) == 9
    assert all(part.is_valid and len(part.solids()) == 1 for part in (*bearings, *spools))
    assert all(_volume(bearing.intersect(spool)) <= 1e-7 for bearing, spool in zip(bearings, spools))


def test_spool_groove_has_exact_axial_float_and_positive_capture_at_all_extremes():
    assert p.spool_groove_width == pytest.approx(1.10)
    assert p.spool_axial_float == pytest.approx(0.15)
    assert p.nominal_running_gap == pytest.approx(0.10)
    assert p.adjustable_running_gap_range == pytest.approx((0.05, 0.15))
    for role in range(3):
        flange_z0, flange_z1 = p.flange_range(role)
        lower, upper = p.lip_ranges(role)
        assert flange_z0 - lower[1] == pytest.approx(0.15)
        assert upper[0] - flange_z1 == pytest.approx(0.15)
        for axis in p.adjustable_axis_radius_range:
            overlap = axis + p.spool_lip_outer_diameter / 2.0 - p.rail_flange_radii[0]
            assert overlap >= 0.75 - 1e-9


def test_actual_solids_at_both_adjustment_and_axial_float_extremes():
    # The critic's exact R126.45/OD14.4 combination creates a measured 0.05 mm
    # upper-lip/neck setup contact. It is bounded here explicitly rather than
    # being mislabeled as free clearance; the R126.35 state is fully clear.
    outward_contacts = []
    for axis in p.adjustable_axis_radius_range:
        lower = g.make_tower_lower(2, axis)
        yoke = g.make_tower_upper_yoke(2, axis)
        assert lower.is_valid and len(lower.solids()) == 1
        assert yoke.is_valid and len(yoke.solids()) == 1
        for role in range(3):
            ring = g.accepted_full_role_ring(role)
            assert _volume(ring.intersect(lower)) <= 1e-7
            assert _volume(ring.intersect(yoke)) <= 1e-7
            for z_shift in (-p.spool_axial_float, 0.0, p.spool_axial_float):
                spool = g.make_roller_spool(role, 2, axis, z_shift)
                common = _volume(ring.intersect(spool))
                if axis == p.adjustable_axis_radius_range[0]:
                    assert common <= 1e-7
                else:
                    outward_contacts.append(common)
                    assert 0.03 < common < 0.04
    assert len(outward_contacts) == 9


def test_two_fixed_round_datums_and_only_third_has_functional_slots():
    assert p.fixed_tower_indices == (0, 1)
    assert p.adjustable_tower_index == 2
    for tower in p.fixed_tower_indices:
        base = g.make_tower_lower(tower)
        assert "fixed_round_datum" in base.label
        for tangent in p.base_mount_tangent_offsets:
            assert _volume(base.intersect(_base_probe(tower, tangent, 0.0))) <= 1e-7
            assert _volume(base.intersect(_base_probe(tower, tangent, 0.25))) > 1e-4
    base = g.make_tower_lower(2)
    assert "adjustable_R126p35_to_R126p45" in base.label
    for tangent in p.base_mount_tangent_offsets:
        for shift in (-0.05, 0.0, 0.05):
            assert _volume(base.intersect(_base_probe(2, tangent, shift))) <= 1e-7


def test_shoulder_axle_spacers_shims_yoke_and_retainer_are_explicit():
    assert 3.98 <= p.axle_shoulder_diameter <= 3.99
    assert p.spacer_lengths == pytest.approx((2.55, 2.55))
    assert p.shim_thickness == pytest.approx(0.20)
    for tower in range(3):
        spacers = g.make_spacers(tower)
        shims = g.make_shims(tower)
        yoke = g.make_tower_upper_yoke(tower)
        hardware = g.make_hardware(tower)
        assert [part.bounding_box().size.Z for part in spacers] == pytest.approx((2.55, 2.55))
        assert [part.bounding_box().size.Z for part in shims] == pytest.approx((0.20, 0.20))
        assert yoke.is_valid and len(yoke.solids()) == 1
        assert "M3_tapped" in hardware[0].label
        assert "removable_M3_threaded_retainer" in hardware[1].label
        assert sum("M3x10_base_screw" in part.label for part in hardware) == 2
        assert sum("M3x8_yoke_screw" in part.label for part in hardware) == 2


def test_exact_fin_360_sweep_clears_all_towers_and_motor_supports():
    stationary = list(g.make_stationary_module().children)
    stationary.extend(g.accepted_station_support(role, p) for role in range(3))
    for role in range(3):
        sweep = g.make_fin_360_sweep(role)
        assert sweep.is_valid
        for fixed in stationary:
            assert _volume(sweep.intersect(fixed)) <= 1e-7, fixed.label
    assert p.spool_outer_radius == pytest.approx(133.6)
    assert p.spool_outer_radius <= p.stationary_radius_limit
    assert p.fin_clearance >= p.minimum_fin_clearance


def test_actual_seam_crossing_neighborhoods_clear_spools():
    epsilon = p.tooth_pitch_degrees / 20.0
    phases = [seam + delta for seam in (0.0, 90.0, 180.0, 270.0) for delta in (-epsilon, 0.0, epsilon)]
    for role in range(3):
        quadrants = g.accepted_ring_quadrants(role, p)
        for phase in phases:
            moved = [part.rotate(g.Axis.Z, phase) for part in quadrants]
            for tower in range(3):
                spool = g.make_roller_spool(role, tower, p.adjustable_axis_radius_range[0])
                assert all(_volume(part.intersect(spool)) <= 1e-7 for part in moved)


def test_inherited_d_flat_motor_pinion_interfaces_remain_torque_only():
    assert p.output_shaft_across_flat == pytest.approx(3.5)
    assert p.output_pinion_bore_across_flat == pytest.approx(3.6)
    for role in range(3):
        parts = g.accepted_motor_station_parts(role, p)
        shaft, pinion = parts[4], parts[11]
        assert "vertical_D_steel_shaft" in shaft.label
        assert "real_M1_16T_output_pinion" in pinion.label
        # The inherited reference assembly represents the keyed torque fit as
        # a small positive D-flat engagement volume, not as a loose shaft.
        assert 0.20 < _volume(shaft.intersect(pinion)) < 2.0
        for tower in range(3):
            module = g.make_tower_module(tower)
            assert all(_volume(part.intersect(child)) <= 1e-7 for part in parts for child in module.children)


def test_primary_printed_parts_fit_snapmaker_u1():
    parts = [*g.make_chassis_segments(), *g.make_frame_segments(p), *g.make_outer_front_ring_segments(p)]
    for role in range(3):
        parts.extend(g.accepted_ring_quadrants(role, p))
        parts.append(g.accepted_station_support(role, p))
    for tower in range(3):
        parts.extend((g.make_tower_lower(tower), g.make_tower_upper_yoke(tower)))
        parts.extend(g.make_spacers(tower))
        parts.extend(g.make_shims(tower))
        parts.extend(g.make_roller_spool(role, tower) for role in range(3))
    for part in parts:
        size = part.bounding_box().size
        assert size.X <= p.segment_bed_limit and size.Y <= p.segment_bed_limit
