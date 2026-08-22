"""Focused contracts for the P3 V3 direct-drive motor mesh adjustment."""

from __future__ import annotations

from math import cos, radians, sin

import pytest
from build123d import Align, Box, Cylinder, Location

from p3_v3_direct_gear_race_guidance_geometry import (
    make_chassis_segments,
    make_motor_clamp_hardware,
    _move_station_part,
    make_unibody_drive_yoke,
)
from p3_v3_direct_gear_race_guidance_spec import P3_V3_DIRECT_GEAR_RACE as p


def _volume(shape) -> float:
    return sum(s.volume for s in shape.solids()) if shape else 0.0


def _center(shape):
    box = shape.bounding_box()
    return ((box.min.X + box.max.X) / 2.0, (box.min.Y + box.max.Y) / 2.0)


def _fixed_axis(role: int, x: float, y: float) -> tuple[float, float]:
    angle = radians(p.motor_station_angles[role])
    return (x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle))


def test_named_slot_powered_window_and_clamp_ligament_math():
    assert p.motor_mount_physical_range == pytest.approx((-2.50, 2.50))
    assert p.motor_mount_powered_range == pytest.approx((-0.35, 0.10))
    assert p.motor_mount_slot_center_travel == pytest.approx(5.00)
    assert p.motor_mount_slot_overall_length == pytest.approx(8.60)
    assert p.motor_mount_slot_width == pytest.approx(3.60)
    assert p.motor_mount_slot_radial_clearance == pytest.approx(0.30)
    assert p.motor_mount_washer_tangential_ligament == pytest.approx(1.00)
    assert p.motor_mount_worst_radial_ligament == pytest.approx(2.00)
    assert p.motor_witness_powered_band_radial_width == pytest.approx(0.45)
    assert p.motor_witness_powered_band_center_offset == pytest.approx(-0.125)

    for q in (-2.50, -0.35, 0.0, 0.10, 2.50):
        p.validate_motor_radial_adjustment(q)
    for q in (-0.35, 0.0, 0.10):
        p.validate_motor_radial_adjustment(q, powered=True)
    for q in (-0.351, 0.101):
        with pytest.raises(ValueError):
            p.validate_motor_radial_adjustment(q, powered=True)


@pytest.mark.parametrize("role", range(3))
@pytest.mark.parametrize("q", (-2.50, -0.35, 0.0, 0.10, 2.50))
def test_whole_station_moves_as_one_rigid_radial_cartridge(role: int, q: float):
    # Every purchased/reference part and the connected yoke passes through this
    # single translation helper.  Exercise it on distinct dummy occurrences so
    # this kinematic contract stays lightweight and does not regenerate bevel
    # gears 30 times inside one OCC process.
    angle = radians(p.motor_station_angles[role])
    expected = (q * cos(angle), q * sin(angle))
    nominal = tuple(Box(1 + i / 20, 1, 1).moved(Location((i * 2, i / 3, i / 5))) for i in range(12))
    moved = tuple(_move_station_part(part, role, q, p) for part in nominal)
    for before, after in zip(nominal, moved):
        b = _center(before)
        a = _center(after)
        assert (a[0] - b[0], a[1] - b[1]) == pytest.approx(expected, abs=2e-6)


@pytest.mark.parametrize("q", (-2.50, 0.0, 2.50))
def test_fixed_m3_axes_clear_actual_yoke_slots_at_service_limits(q: float):
    role = 0  # The other two stations are exact 120/240 degree rotations.
    yoke = make_unibody_drive_yoke(role, p, q)
    for x in p.unibody_chassis_mount_x:
        for y in p.unibody_chassis_mount_y:
            gx, gy = _fixed_axis(role, x, y)
            screw_probe = Cylinder(
                p.motor_mount_screw_nominal_diameter / 2.0,
                p.unibody_foot_thickness + 0.8,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((gx, gy, p.chassis_z[1] - 0.4)))
            assert _volume(yoke.intersect(screw_probe)) <= 1e-7


def test_each_station_has_four_fixed_m3_washer_and_nut_clamp_stacks():
    for role in range(3):
        hardware = make_motor_clamp_hardware(role, p)
        assert len(hardware) == 12
        labels = [part.label for part in hardware]
        assert sum("M3x10_screw" in label for label in labels) == 4
        assert sum("D7x0p50_washer" in label for label in labels) == 4
        assert sum("M3_AF5p50_nut" in label for label in labels) == 4


def test_chassis_holes_remain_round_and_fixed_while_only_yoke_is_slotted():
    chassis = make_chassis_segments(p)
    for role in range(3):
        for x in p.unibody_chassis_mount_x:
            for y in p.unibody_chassis_mount_y:
                gx, gy = _fixed_axis(role, x, y)
                probe = Cylinder(
                    (p.motor_mount_chassis_hole_diameter - 0.05) / 2.0,
                    p.chassis_z[1] - p.chassis_z[0] + 0.4,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ).moved(Location((gx, gy, p.chassis_z[0] - 0.2)))
                assert all(_volume(segment.intersect(probe)) <= 1e-7 for segment in chassis)
