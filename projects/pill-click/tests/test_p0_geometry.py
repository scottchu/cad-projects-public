"""BREP validity, clearance, and sampled sweep tests for P0."""

import pytest
from build123d import Location

from pill_click.p0 import (
    P0,
    make_back_insert,
    make_housing,
    make_p0_assembly,
    make_shuttle,
)


def _intersection_volume(first, second) -> float:
    return (first & second).volume


def test_p0_parts_are_valid_single_solids() -> None:
    parts = [make_housing(), make_back_insert(), make_shuttle()]
    assert all(part.is_valid and part.volume > 0 for part in parts)
    assert all(len(part.solids()) == 1 for part in parts)


def test_housing_bbox_is_exactly_40_mm() -> None:
    bbox = make_housing().bounding_box()
    assert bbox.size.X == pytest.approx(40.0)
    assert bbox.size.Y == pytest.approx(40.0)
    assert bbox.size.Z == pytest.approx(40.0)


def test_assembly_contains_only_three_p0_parts() -> None:
    assembly = make_p0_assembly(P0.released_state)
    labels = {child.label for child in assembly.children}
    assert assembly.is_valid
    assert labels == {
        "p0_fixed_housing_with_four_rails",
        "p0_rear_insert",
        "p0_medicine_shuttle:s_13.40",
    }
    forbidden = ("spring", "magnet", "cam", "follower", "gate")
    assert not any(token in label for token in forbidden for label in labels)


@pytest.mark.parametrize(
    "state",
    [-1.0, 0.0, 2.4, 4.8, 6.7, 9.0, 11.2, 13.4],
)
def test_sampled_stroke_has_no_positive_volume_collision(state: float) -> None:
    p = P0
    housing = make_housing(p)
    insert = make_back_insert(p).moved(
        Location((0.0, p.rear_insert_center_y, 0.0))
    )
    shuttle = make_shuttle(p).moved(
        Location((0.0, p.shuttle_center_y(state), 0.0))
    )

    assert _intersection_volume(housing, shuttle) == pytest.approx(
        0.0, abs=1e-6
    )
    assert _intersection_volume(insert, shuttle) == pytest.approx(
        0.0, abs=1e-6
    )
    assert _intersection_volume(housing, insert) == pytest.approx(
        0.0, abs=1e-6
    )


def test_ready_closure_skin_physically_backs_fixed_aperture_footprints() -> None:
    p = P0
    shuttle = make_shuttle(p).moved(
        Location((0.0, p.shuttle_center_y(p.released_state), 0.0))
    )

    # Thin probes lie wholly inside the named moving roof/floor skins.
    from build123d import Align, Box

    roof_probe = Box(
        p.fill_width,
        p.fill_length,
        0.20,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((0.0, p.fill_fixed_center_y, p.shuttle_height / 2 - 0.10)))
    floor_probe = Box(
        p.outlet_width,
        p.outlet_length,
        0.20,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(
        Location((0.0, p.outlet_fixed_center_y, -p.shuttle_height / 2 + 0.10))
    )
    assert _intersection_volume(shuttle, roof_probe) == pytest.approx(
        roof_probe.volume, rel=1e-6
    )
    assert _intersection_volume(shuttle, floor_probe) == pytest.approx(
        floor_probe.volume, rel=1e-6
    )
