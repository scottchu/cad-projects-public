"""Focused topology checks for the independent push-push latch parts."""

from math import isclose

from build123d import Align, Box

from pill_click.latch import make_cam_carrier, make_compliant_follower
from pill_click.parameters import DEFAULTS, PillClickParameters


def test_cam_carrier_is_a_valid_recessed_positive_solid() -> None:
    carrier = make_cam_carrier()
    bbox = carrier.bounding_box()
    blank_volume = bbox.size.X * bbox.size.Y * DEFAULTS.cam_plate_thickness

    assert carrier.is_valid
    assert carrier.volume > 0
    assert carrier.volume < blank_volume
    assert carrier.label == "push_push_cam_carrier"
    assert bbox.min.Z == 0
    assert isclose(bbox.max.Z, DEFAULTS.cam_plate_thickness, abs_tol=1e-7)


def test_cam_groove_is_blind_and_retains_a_floor() -> None:
    carrier = make_cam_carrier()
    floor = DEFAULTS.cam_plate_thickness - DEFAULTS.cam_groove_depth

    # A thin box below the nominal groove floor must remain fully occupied.
    probe_height = 0.25
    probe = Box(
        DEFAULTS.follower_pin_diameter,
        DEFAULTS.follower_pin_diameter,
        probe_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    probe = probe.translate((0, -0.5 * DEFAULTS.travel, floor - probe_height))
    intersection = carrier & probe

    assert intersection.volume > 0.95 * probe.volume


def test_compliant_follower_is_one_valid_connected_solid() -> None:
    follower = make_compliant_follower()
    bbox = follower.bounding_box()

    assert follower.is_valid
    assert follower.volume > 0
    assert len(follower.solids()) == 1
    assert follower.label == "compliant_cam_follower"
    assert bbox.min.Y < 0
    assert bbox.max.Z > DEFAULTS.follower_beam_width


def test_latch_geometry_tracks_parameter_changes() -> None:
    tuned = PillClickParameters(
        ready_state=12.8,
        cam_groove_width=3.1,
        follower_pin_diameter=2.3,
        follower_beam_thickness=1.35,
    )
    carrier = make_cam_carrier(tuned)
    follower = make_compliant_follower(tuned)

    assert carrier.is_valid and carrier.volume > 0
    assert follower.is_valid and follower.volume > 0
    assert carrier.bounding_box().size.Y > tuned.total_press_span
    assert follower.bounding_box().size.Y > tuned.total_press_span
