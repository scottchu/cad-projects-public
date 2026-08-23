"""Executable acceptance contracts for the isolated V3 drive-service station."""

from __future__ import annotations

from pathlib import Path

import pytest
from OCP.BRepCheck import BRepCheck_Analyzer

import p3_v3_drive_service_geometry as g
from p3_v3_drive_service_spec import P3_V3_DRIVE_SERVICE as p
from p3_v3_full_ring_r2_spec import P3_V3_FULL_RING_R2 as parent


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_drive_service"
VOLUME_TOL = 1e-7


def _intersection_volume(left, right) -> float:
    common = left.intersect(right)
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _valid_single_solid(shape) -> None:
    assert shape.is_valid
    assert BRepCheck_Analyzer(shape.wrapped).IsValid()
    assert len(shape.solids()) == 1
    assert shape.volume > 0.0


@pytest.fixture(scope="module")
def station():
    names = ("motor", "motor_shaft", "horizontal_miter", "vertical_miter", "output_shaft", "lower_bearing", "upper_bearing")
    return dict(zip(names, g.make_existing_drive_references()))


def test_service_contract_does_not_move_existing_transmission_datums():
    assert p.role == "minute" and p.role_index == 1
    assert p.output_axis_x == pytest.approx(parent.output_axis_radius)
    assert p.output_pinion_face == pytest.approx(parent.pinion_face_ranges[1])
    assert (p.ring_teeth, p.pinion_teeth, p.gear_module) == (260, 16, 1.0)
    assert p.gear_ratio == pytest.approx(16.25)


def test_real_nema8_face_pattern_uses_m2_not_m3(station):
    assert p.motor_face_size == pytest.approx(20.3)
    assert p.motor_mount_pitch == pytest.approx(15.4)
    assert p.motor_mount_thread == "M2"
    assert p.motor_mount_screw_length == pytest.approx(4.0)
    screws = g.make_motor_mount_screw_references()
    assert len(screws) == 4
    bracket = g.make_motor_cartridge_bracket()
    _valid_single_solid(bracket)
    assert _intersection_volume(bracket, station["motor"]) <= VOLUME_TOL
    assert bracket.distance_to(station["motor"]) == pytest.approx(0.0, abs=VOLUME_TOL)
    for screw in screws:
        assert screw.distance_to(bracket) == pytest.approx(0.0, abs=VOLUME_TOL)
        assert screw.distance_to(station["motor"]) == pytest.approx(0.0, abs=VOLUME_TOL)


def test_motor_cartridge_and_gearbox_use_separate_m3_chassis_interfaces():
    assert p.chassis_fastener == "M3x8"
    assert p.chassis_clearance_hole == pytest.approx(3.40)
    screws = g.make_chassis_screw_references()
    assert len(screws) == 4
    assert {round(s.bounding_box().center().X, 6) for s in screws} == {105.0, 131.0}
    assert {round(s.bounding_box().center().Y, 6) for s in screws} == {-13.0, 13.0}


def test_two_sided_gearbox_frame_is_one_valid_solid_and_clears_moving_parts(station):
    frame = g.make_gearbox_frame()
    _valid_single_solid(frame)
    for name in ("motor", "motor_shaft", "horizontal_miter", "vertical_miter", "output_shaft", "lower_bearing"):
        moving = station[name]
        assert _intersection_volume(frame, moving) <= VOLUME_TOL, name
    assert frame.distance_to(station["horizontal_miter"]) >= p.moving_to_frame_clearance_min


def test_removable_upper_bridge_holds_second_mr84_with_radial_clearance(station):
    bridge = g.make_upper_bearing_bridge()
    _valid_single_solid(bridge)
    assert p.bridge_fastener == "M3x8"
    assert len(g.make_bridge_screw_references()) == 2
    assert _intersection_volume(bridge, station["upper_bearing"]) <= VOLUME_TOL
    assert bridge.distance_to(station["upper_bearing"]) == pytest.approx(p.bearing_radial_clearance, abs=2e-7)


def test_keyed_steel_shaft_two_mr84_and_miter_are_coaxial(station):
    shaft = station["output_shaft"]
    assert shaft.bounding_box().size.Z == pytest.approx(40.0)
    assert shaft.bounding_box().center().X == pytest.approx(p.output_axis_x)
    for bearing in (station["lower_bearing"], station["upper_bearing"]):
        assert bearing.bounding_box().center().X == pytest.approx(p.output_axis_x)
        assert _intersection_volume(shaft, bearing) <= VOLUME_TOL
        assert shaft.distance_to(bearing) == pytest.approx(0.0, abs=VOLUME_TOL)
    assert _intersection_volume(shaft, station["vertical_miter"]) <= VOLUME_TOL


def test_shoulder_spacer_pinion_stack_sets_exact_height_and_endplay():
    assert p.lower_collar_gap == pytest.approx(0.10)
    assert p.spacer_lower_gap == pytest.approx(0.05)
    assert p.spacer_upper_gap == pytest.approx(0.0)
    assert p.computed_endplay == pytest.approx(p.axial_endplay)
    assert p.axial_endplay == pytest.approx(0.15)
    assert g.make_lower_datum_collar().bounding_box().max.Z == pytest.approx(p.lower_collar_z[1])
    assert g.make_lower_inner_race_spacer().bounding_box().min.Z == pytest.approx(p.lower_inner_race_spacer_z[0])
    assert g.make_role_spacer().bounding_box().max.Z == pytest.approx(p.output_pinion_face[0])
    pinion = g.make_minute_output_pinion()
    assert (pinion.bounding_box().min.Z, pinion.bounding_box().max.Z) == pytest.approx(p.output_pinion_face)


def test_existing_minute_ring_and_canonical_pinion_are_real_noninterfering_breps():
    ring = g.make_minute_ring_arc_reference()
    pinion = g.make_minute_output_pinion()
    _valid_single_solid(ring)
    _valid_single_solid(pinion)
    assert _intersection_volume(ring, pinion) <= VOLUME_TOL
    assert ring.distance_to(pinion) > 0.05
    assert ring.distance_to(pinion) < p.output_mesh_backlash


def test_external_retainer_is_commercial_collar_with_removable_printed_grip():
    collar = g.make_safety_collar()
    knob = g.make_service_knob_shell()
    _valid_single_solid(collar)
    _valid_single_solid(knob)
    assert "purchased_4mm_split" in collar.label
    assert "hand_grip" in knob.label
    assert _intersection_volume(collar, knob) <= VOLUME_TOL
    assert collar.distance_to(knob) == pytest.approx(0.15, abs=2e-7)


def test_service_sequence_has_explicit_installation_stages():
    stages = (
        g.make_stage_1_motor(),
        g.make_stage_2_gearbox(),
        g.make_stage_3_shaft(),
        g.make_stage_4_pinion(),
    )
    # A build123d stage may group already-installed parts into a nested
    # compound, so its top-level child count is not a meaningful proxy for
    # assembly order.  The explicit stage identity is the stable contract.
    assert [stage.label for stage in stages] == [
        "p3_v3_drive_service_STAGE_1_mount_NEMA8_with_four_M2x4",
        "p3_v3_drive_service_STAGE_2_mount_frame_and_horizontal_miter",
        "p3_v3_drive_service_STAGE_3_insert_keyed_shaft_miter_two_MR84_and_bridge",
        "p3_v3_drive_service_STAGE_4_set_minute_pinion_height_and_external_retainer",
    ]


def test_expected_step_artifacts_exist_after_generation():
    expected = (
        "p3_v3_drive_service_stage_1_motor.step",
        "p3_v3_drive_service_stage_2_gearbox.step",
        "p3_v3_drive_service_stage_3_shaft.step",
        "p3_v3_drive_service_assembled.step",
        "p3_v3_drive_service_exploded.step",
    )
    for name in expected:
        assert (MODEL_ROOT / name).is_file(), name
