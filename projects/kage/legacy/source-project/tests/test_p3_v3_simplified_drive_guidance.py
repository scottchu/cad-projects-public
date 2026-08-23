"""Focused design and actual-solid contracts for the simplified V3 mechanism."""

from __future__ import annotations

from math import cos, radians, sin
from pathlib import Path

import pytest
import py_gearworks as pgw
from build123d import Axis, Compound, Location

from p3_v3_simplified_drive_guidance_geometry import (
    make_chassis_segments,
    make_fin_360_sweep,
    make_full_role_ring_reference,
    make_motor_station_parts,
    make_ring_quadrants,
    make_roller,
    make_roller_tower_yoke,
    make_stationary_module,
    make_unibody_drive_yoke,
)
from p3_v3_simplified_drive_guidance_spec import P3_V3_SIMPLIFIED as p


def _volume(shape) -> float:
    return sum(s.volume for s in shape.solids()) if shape else 0.0


def _radial_vector(angle_degrees: float) -> tuple[float, float]:
    angle = radians(angle_degrees)
    return cos(angle), sin(angle)


def _ring_teeth(role: int):
    z0, z1 = p.pinion_face_ranges[role]
    return pgw.SpurRingGear(
        number_of_teeth=p.ring_teeth,
        module=p.module,
        height=z1 - z0,
        center=[0.0, 0.0, z0],
        backlash=0.10,
    ).build_part().solid().rotate(Axis.Z, p.tooth_phase_offset_degrees)


def test_frozen_three_ring_transmission_and_envelope():
    assert p.roles == ("hour", "minute", "second")
    assert p.ring_teeth == 260 and p.pinion_teeth == 16
    assert p.carrier_layers == ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    assert p.retainer_radii[1] * 2.0 == pytest.approx(300.0)


def test_compact_smooth_bead_contract_replaces_t_rail():
    assert p.guide_head_radii == pytest.approx((132.8, 134.8))
    assert p.guide_neck_radii == pytest.approx((133.6, 134.8))
    assert (p.guide_head_depth, p.guide_neck_depth, p.guide_total_depth) == pytest.approx((0.8, 0.8, 1.6))
    labels = [part.label.lower() for part in make_stationary_module().children]
    assert not any(
        rejected in label
        for label in labels
        for rejected in ("keeper", "saddle", "t_rail", "removable_bar", "side_gate")
    )


def test_exactly_three_inner_towers_nine_direct_spools_and_one_adjuster():
    assert p.roller_tower_angles == (60.0, 180.0, 300.0)
    assert p.fixed_tower_indices == (0, 1)
    assert p.adjustable_tower_indices == (2,)
    assert p.tower_preload_slot_travel == pytest.approx(0.50)
    rollers = [make_roller(role, tower) for tower in range(3) for role in range(3)]
    assert len(rollers) == 9
    assert all(part.is_valid and len(part.solids()) == 1 for part in rollers)


def test_direct_spool_dimensions_and_nominal_bead_gap():
    assert p.roller_bore_diameter == pytest.approx(4.06)
    assert p.roller_hub_outer_diameter == pytest.approx(6.4)
    assert p.roller_running_outer_diameter == pytest.approx(7.9)
    assert p.roller_flange_outer_diameter == pytest.approx(9.6)
    assert p.roller_flange_thickness == pytest.approx(0.50)
    assert p.roller_axis_radius == pytest.approx(128.8)
    assert p.roller_running_gap == pytest.approx(0.05)
    assert p.roller_capture_radial_overlap == pytest.approx(0.8)


@pytest.mark.parametrize("tower", range(3))
def test_each_tower_is_one_connected_two_sided_yoke(tower):
    yoke = make_roller_tower_yoke(tower)
    assert yoke.is_valid and len(yoke.solids()) == 1
    if tower == 2:
        assert "adjustable_plus_minus_0p25" in yoke.label
    else:
        assert "fixed_round_mounts" in yoke.label


@pytest.mark.parametrize("role", range(3))
def test_each_drive_is_one_open_unibody_with_minimal_retained_stack(role):
    yoke = make_unibody_drive_yoke(role)
    parts = make_motor_station_parts(role)
    assert yoke.is_valid and len(yoke.solids()) == 1
    assert len(parts) == 12
    labels = " ".join(part.label.lower() for part in parts)
    assert "one_connected" in labels
    assert "only_role_height_spacer" in labels
    assert not any(word in labels for word in ("side_gate", "upper_bridge_plate", "decorative_grip"))
    lower, upper = p.output_endplay_bounds
    assert p.nominal_output_endplay == pytest.approx(0.10)
    assert p.output_endplay_tolerance == pytest.approx(0.05)
    assert lower - 1e-9 <= p.computed_output_endplay(role) <= upper + 1e-9


@pytest.mark.parametrize("role", range(3))
def test_nominal_ring_clears_its_three_direct_spools(role):
    ring = make_full_role_ring_reference(role)
    for tower in range(3):
        assert _volume(ring.intersect(make_roller(role, tower))) <= 1e-7


def test_adjustable_tower_extremes_keep_every_roller_isolated_from_ring_teeth():
    for role in range(3):
        teeth = _ring_teeth(role)
        for delta in (-p.roller_axis_adjustment, p.roller_axis_adjustment):
            roller = make_roller(role, 2, p.roller_axis_radius + delta)
            assert _volume(teeth.intersect(roller)) <= 1e-7
            assert teeth.distance_to(roller) >= 0.899


def test_complete_fin_sweeps_clear_full_105_part_stationary_matrix():
    fixed = list(make_stationary_module().children)
    # All non-ring drive occurrences remain in fixed spatial envelopes even
    # when their shafts turn; include the eleven retained parts per role.
    for role in range(3):
        fixed.extend(make_motor_station_parts(role)[:-1])
    assert len(fixed) == 105
    for role in range(3):
        sweep = make_fin_360_sweep(role)
        for part in fixed:
            assert _volume(sweep.intersect(part)) <= 1e-7, f"{p.roles[role]} fin hits {part.label}"


@pytest.mark.parametrize("role", range(3))
def test_both_mr84_bearings_have_sampled_collision_free_plus_x_install_paths(role):
    parts = make_motor_station_parts(role)
    ux, uy = _radial_vector(p.motor_station_angles[role])
    yoke, bearings = parts[11], (parts[5], parts[6])
    for moving_index in (0, 1):
        for radial_offset in (15.0, 12.0, 9.0, 6.0, 3.0, 0.0):
            moving = bearings[moving_index].moved(
                Location((radial_offset * ux, radial_offset * uy, 0.0))
            )
            assert _volume(moving.intersect(yoke)) <= 1e-7
            assert _volume(moving.intersect(bearings[1 - moving_index])) <= 1e-7


@pytest.mark.parametrize("role", range(3))
def test_vertical_miter_and_d4_shaft_have_sampled_service_paths(role):
    parts = make_motor_station_parts(role)
    ux, uy = _radial_vector(p.motor_station_angles[role])
    yoke, vertical, shaft = parts[11], parts[3], parts[4]
    bearings = (parts[5], parts[6])
    for radial_offset in (15.0, 12.0, 9.0, 6.0, 3.0, 0.0):
        moving = vertical.moved(Location((radial_offset * ux, radial_offset * uy, 0.0)))
        for obstacle in (yoke, *bearings):
            assert _volume(moving.intersect(obstacle)) <= 1e-7
    for z_offset in (45.0, 36.0, 27.0, 18.0, 9.0, 0.0):
        moving = shaft.moved(Location((0.0, 0.0, z_offset)))
        for bored_or_open in (yoke, *bearings, vertical):
            assert _volume(moving.intersect(bored_or_open)) <= 1e-7


@pytest.mark.parametrize("role", range(3))
def test_motor_and_horizontal_miter_install_together_from_inner_side(role):
    parts = make_motor_station_parts(role)
    ux, uy = _radial_vector(p.motor_station_angles[role])
    moving_set = Compound(children=parts[:3])
    installed = (parts[11], parts[5], parts[6], parts[3], parts[4])
    for inward_offset in (35.0, 28.0, 21.0, 14.0, 7.0, 0.0):
        moving = moving_set.moved(Location((-inward_offset * ux, -inward_offset * uy, 0.0)))
        for obstacle in installed:
            assert _volume(moving.intersect(obstacle)) <= 1e-7


@pytest.mark.parametrize("role", range(3))
@pytest.mark.parametrize("quadrant", range(4))
def test_each_ring_quadrant_installs_radially_around_all_nine_roller_grooves(role, quadrant):
    midpoint = (quadrant + 0.5) * p.quadrant_angle_degrees
    ux, uy = _radial_vector(midpoint)
    quadrant_part = make_ring_quadrants(role)[quadrant]
    rollers = [make_roller(r, tower) for r in range(3) for tower in range(3)]
    for outward_offset in (15.0, 12.0, 9.0, 6.0, 3.0, 0.0):
        moving = quadrant_part.moved(Location((outward_offset * ux, outward_offset * uy, 0.0)))
        for roller in rollers:
            assert _volume(moving.intersect(roller)) <= 1e-7


def test_primary_printed_parts_fit_snapmaker_u1_bed():
    parts = [*make_chassis_segments()]
    parts.extend(make_roller_tower_yoke(t) for t in range(3))
    parts.extend(make_unibody_drive_yoke(r) for r in range(3))
    for role in range(3):
        parts.extend(make_ring_quadrants(role))
    for part in parts:
        size = part.bounding_box().size
        assert size.X <= p.segment_bed_limit and size.Y <= p.segment_bed_limit


def test_generated_step_entry_sources_exist():
    root = Path(__file__).resolve().parents[1] / "models" / p.artifact_slug
    assert (root / "p3_v3_simplified_assembled.step.py").is_file()
    assert (root / "p3_v3_simplified_service_exploded.step.py").is_file()
