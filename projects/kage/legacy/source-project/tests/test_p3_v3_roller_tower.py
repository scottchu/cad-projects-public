"""Actual-solid contracts for the KAGE V3 shared roller towers."""

from __future__ import annotations

from math import cos, hypot, radians, sin

import pytest
from build123d import Align, Axis, Compound, Cylinder, Location

from p3_v3_roller_tower_geometry import (
    _full_role_ring,
    make_capture_cheeks,
    make_chassis_segments,
    make_fin_360_sweep,
    make_frame_segments,
    make_motor_station_parts,
    make_outer_front_ring_segments,
    make_ring_quadrants,
    make_roller,
    make_station_support,
    make_stationary_module,
    make_tower_base,
    make_tower_hardware_references,
    make_tower_spacers,
    make_tower_thrust_washers,
)
from p3_v3_roller_tower_spec import P3_V3_ROLLER_TOWER as p


def _volume(common) -> float:
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _radial_probe(tower: int, tangent: float, radial_shift: float):
    angle = radians(p.roller_tower_angles[tower])
    local_x = p.tower_mount_axis_radius + radial_shift
    x = local_x * cos(angle) - tangent * sin(angle)
    y = local_x * sin(angle) + tangent * cos(angle)
    z0, z1 = p.tower_base_z_range
    return Cylinder(
        p.tower_mount_bolt_diameter / 2.0,
        z1 - z0 + 0.4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0 - 0.2)))


def test_architecture_is_three_identical_towers_and_nine_direct_spools():
    assert p.roller_tower_angles == (60.0, 180.0, 300.0)
    assert p.motor_station_angles == (0.0, 120.0, 240.0)
    assert p.adjustable_tower_indices == (0, 1, 2)
    assert p.roller_type == "independent_direct_running_flanged_spool"
    assert "MR84" not in p.roller_type
    rollers = [make_roller(role, tower) for tower in range(3) for role in range(3)]
    assert len(rollers) == 9
    assert len({roller.label for roller in rollers}) == 9
    assert all(roller.is_valid and len(roller.solids()) == 1 for roller in rollers)


def test_rejected_t_rail_and_keeper_saddles_are_absent():
    assert p.guide_total_depth == pytest.approx(1.6)
    assert p.guide_head_depth == pytest.approx(0.8)
    assert p.guide_neck_depth == pytest.approx(0.8)
    assert p.guide_head_radii == pytest.approx((132.8, 134.8))
    assert all(make_capture_cheeks(role, tower) == () for role in range(3) for tower in range(3))
    labels = [child.label.lower() for child in make_stationary_module().children]
    assert not any("keeper" in label or "saddle" in label or "t_rail" in label for label in labels)


def test_spool_stack_and_carrier_gaps_are_mathematically_consistent():
    assert p.carrier_layers == ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    assert p.roller_center_zs == pytest.approx((-2.70, 2.85, 8.40))
    ranges = [p.roller_range(role) for role in range(3)]
    assert tuple(ranges[index + 1][0] - ranges[index][1] for index in range(2)) == pytest.approx(
        p.roller_spacer_lengths
    )
    assert p.lower_thrust_washer_range[1] == pytest.approx(ranges[0][0])
    assert p.upper_thrust_washer_range[0] == pytest.approx(ranges[2][1])


@pytest.mark.parametrize("tower", range(3))
def test_every_tower_has_symmetric_plus_minus_0p6_mount_adjustment(tower):
    base = make_tower_base(tower)
    assert base.is_valid and len(base.solids()) == 1
    assert "symmetric_radial_slots" in base.label
    assert p.adjusted_roller_axis_radius_range == pytest.approx((128.2, 129.4))
    for tangent in p.tower_mount_tangent_offsets:
        for shift in (-0.55, 0.0, 0.55):
            assert _volume(base.intersect(_radial_probe(tower, tangent, shift))) <= 1e-7


@pytest.mark.parametrize("tower", range(3))
def test_one_connected_two_sided_tower_and_independent_axial_bands(tower):
    tower_body = make_tower_base(tower)
    assert tower_body.is_valid and len(tower_body.solids()) == 1
    assert "single_connected_two_sided_yoke" in tower_body.label
    rollers = [make_roller(role, tower) for role in range(3)]
    for left, right in zip(rollers, rollers[1:]):
        assert _volume(left.intersect(right)) <= 1e-7
    assert [part.bounding_box().size.Z for part in make_tower_spacers(tower)] == pytest.approx((3.15, 3.15))
    assert [part.bounding_box().size.Z for part in make_tower_thrust_washers(tower)] == pytest.approx((0.2, 0.2))


@pytest.mark.parametrize("role", range(3))
def test_nominal_ring_has_running_gap_and_zero_stationary_collision(role):
    ring = _full_role_ring(role)
    assert p.roller_running_gap == pytest.approx(p.roller_nominal_contact_gap)
    assert p.roller_stationary_outer_radius - p.guide_head_radii[0] == pytest.approx(
        p.roller_capture_radial_overlap
    )
    for tower in range(3):
        roller = make_roller(role, tower)
        assert _volume(ring.intersect(roller)) <= 1e-7
        running_z0, running_z1 = p.roller_running_range(role)
        running_core = Cylinder(
            p.roller_running_outer_diameter / 2.0,
            running_z1 - running_z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((p.roller_axis_radius, 0.0, running_z0))).rotate(
            Axis.Z, p.roller_tower_angles[tower]
        )
        assert ring.distance_to(running_core) == pytest.approx(
            p.roller_nominal_contact_gap, abs=1e-6
        )
        assert _volume(ring.intersect(make_tower_base(tower))) <= 1e-7


@pytest.mark.parametrize("role", range(3))
def test_actual_brep_plus_minus_0p30_axial_translation_hits_capture_stop(role):
    """Tolerance motion must meet a flange before the guide land can escape."""

    nominal = _full_role_ring(role)
    for dz in (-p.roller_axial_tolerance, p.roller_axial_tolerance):
        moved_ring = nominal.moved(Location((0.0, 0.0, dz)))
        stop_volumes = [
            _volume(moved_ring.intersect(make_roller(role, tower)))
            for tower in range(3)
        ]
        assert min(stop_volumes) > 1e-4


def test_exact_360_fin_sweeps_clear_all_stationary_tower_parts():
    stationary = list(make_stationary_module().children)
    stationary.extend(make_station_support(role) for role in range(3))
    for role in range(3):
        sweep = make_fin_360_sweep(role)
        for fixed in stationary:
            assert _volume(sweep.intersect(fixed)) <= 1e-7, (
                f"{p.roles[role]} fin sweep intersects {fixed.label}"
            )


def test_complete_stationary_envelope_is_inside_fin_corridor():
    assert p.guide_head_radii[1] <= p.tower_stationary_radius_limit
    assert p.roller_stationary_outer_radius == pytest.approx(133.6)
    assert p.tower_base_radial_range[1] <= p.tower_stationary_radius_limit
    assert p.fin_corridor_clearance >= p.minimum_fin_corridor_clearance
    assert min(r0 for r0, _ in p.fin_blade_radial_ranges) == pytest.approx(137.2)


def test_real_one_piece_purchased_collar_and_complete_m3_retention_hardware():
    chassis = Compound(children=make_chassis_segments())
    for tower in range(3):
        hardware = make_tower_hardware_references(tower)
        assert sum("M3_mount_screw" in part.label for part in hardware) == 2
        assert sum("metal_M2_set_screw_collar" in part.label for part in hardware) == 1
        assert sum("M2_collar_set_screw" in part.label for part in hardware) == 1
        assert sum("M3_washer" in part.label for part in hardware) == 2
        assert sum("M3_hex_nut" in part.label for part in hardware) == 2
        collar = next(part for part in hardware if "metal_M2_set_screw_collar" in part.label)
        pin = next(part for part in hardware if "smooth_pin" in part.label)
        set_screw = next(part for part in hardware if "M2_collar_set_screw" in part.label)
        assert collar.is_valid and len(collar.solids()) == 1
        assert collar.bounding_box().size.Z == pytest.approx(4.0)
        assert _volume(collar.intersect(pin)) <= 1e-7
        assert _volume(set_screw.intersect(pin)) > 0.0
        assert _volume(set_screw.intersect(collar)) > 0.0
        tower_body = make_tower_base(tower)
        for rise in (0.0, 2.0, 5.0, 10.0):
            lifted = collar.moved(Location((0.0, 0.0, rise)))
            assert _volume(lifted.intersect(tower_body)) <= 1e-7
            for role in range(3):
                assert _volume(lifted.intersect(make_roller(role, tower))) <= 1e-7
        screws = [part for part in hardware if "M3_mount_screw" in part.label]
        washers = [part for part in hardware if "M3_washer" in part.label]
        nuts = [part for part in hardware if "M3_hex_nut" in part.label]
        assert all(part.is_valid and len(part.solids()) == 1 for part in screws)
        assert all(part.is_valid and len(part.solids()) == 1 for part in washers)
        assert all(part.is_valid and len(part.solids()) == 1 for part in nuts)
        assert all(_volume(screw.intersect(chassis)) <= 1e-7 for screw in screws)
        assert all(_volume(screw.intersect(tower_body)) <= 1e-7 for screw in screws)
        assert all(
            screw.bounding_box().min.Z + p.tower_mount_socket_head_height
            == pytest.approx(p.chassis_z[0])
            for screw in screws
        )
        assert all(
            screw.bounding_box().max.Z
            >= p.tower_base_z_range[1]
            + p.tower_mount_washer_thickness
            + p.tower_mount_hex_nut_thickness
            for screw in screws
        )
        # Nut-driver access is open toward the viewer before the ring stack is
        # installed; this is an assembly operation, not an inaccessible insert.
        for tangent in p.tower_mount_tangent_offsets:
            angle = radians(p.roller_tower_angles[tower])
            x = p.tower_mount_axis_radius * cos(angle) - tangent * sin(angle)
            y = p.tower_mount_axis_radius * sin(angle) + tangent * cos(angle)
            access_z0 = (
                p.tower_base_z_range[1]
                + p.tower_mount_washer_thickness
                + p.tower_mount_hex_nut_thickness
            )
            access = Cylinder(
                p.tower_mount_tool_access_diameter / 2.0,
                -5.0 - access_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, access_z0)))
            assert _volume(access.intersect(tower_body)) <= 1e-7
        for tangent in p.tower_mount_tangent_offsets:
            assert p.chassis_radii[0] < hypot(p.tower_mount_axis_radius, tangent) < p.chassis_radii[1]
    assert p.tower_mount_clearance_diameter == pytest.approx(3.4)
    axial_edge_material = (
        p.tower_retainer_collar_z_range[1]
        - p.tower_retainer_collar_z_range[0]
        - p.tower_collar_set_screw_pilot_diameter
    ) / 2.0
    assert axial_edge_material >= p.tower_collar_min_pilot_edge_material
    assert p.tower_axle_z0 + p.tower_axle_length >= p.tower_retainer_collar_z_range[1]
    assert p.tower_retainer_collar_z_range[0] > p.tower_upper_bushing_z_range[1]
    assert (
        min(p.tower_axle_z0 + p.tower_axle_length, p.tower_retainer_collar_z_range[1])
        - max(p.tower_axle_z0, p.tower_retainer_collar_z_range[0])
    ) == pytest.approx(4.0)
    # The collar can be lifted straight off the pin after its purchased M2
    # set screw is loosened; nothing in the stationary tower bridges above it.
    assert p.tower_retainer_collar_z_range[1] > p.tower_top_bridge_z_range[1]


def test_inherited_drive_datum_uses_true_axis_not_asymmetric_d_flat_bbox():
    """A D-flat solid's bounding-box centre is not its shaft axis."""

    for role in range(3):
        shaft, pinion = make_motor_station_parts(role)[4], make_motor_station_parts(role)[11]
        angle = radians(p.motor_station_angles[role])
        expected_x = p.output_axis_radius * cos(angle)
        expected_y = p.output_axis_radius * sin(angle)
        pinion_center = pinion.bounding_box().center()
        assert pinion_center.X == pytest.approx(expected_x, abs=0.03)
        assert pinion_center.Y == pytest.approx(expected_y, abs=0.03)
        # Detailed shaft/bore clearance belongs to the separate motor-station
        # work package.  This correction freezes only its true integration
        # axis; a D-flat solid's asymmetric bounding box is not that axis.
        assert shaft.bounding_box().min.Z < pinion.bounding_box().min.Z
        assert shaft.bounding_box().max.Z > pinion.bounding_box().max.Z


def test_each_printed_primary_part_fits_snapmaker_u1_xy():
    bed = p.segment_bed_limit
    parts = [*make_chassis_segments(), *make_frame_segments(), *make_outer_front_ring_segments()]
    for role in range(3):
        parts.extend(make_ring_quadrants(role))
        parts.append(make_station_support(role))
    for tower in range(3):
        parts.append(make_tower_base(tower))
        parts.extend(make_roller(role, tower) for role in range(3))
        parts.extend(make_tower_spacers(tower))
        parts.extend(make_tower_thrust_washers(tower))
    for part in parts:
        size = part.bounding_box().size
        assert size.X <= bed and size.Y <= bed, f"{part.label}: {size.X:.2f} x {size.Y:.2f}"
