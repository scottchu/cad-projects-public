from __future__ import annotations

from pathlib import Path

import pytest
from build123d import import_step

from v0r1_compact_quartz_fixture_geometry import (
    make_assembly,
    make_fake_standard_quartz_body,
    part_factories,
    placed_body,
    placed_carrier,
)
from v0r1_compact_quartz_fixture_spec import V0R1, projected_radius


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "v0r1_compact_quartz_fixture"


def volume(shape) -> float:
    if shape is None:
        return 0.0
    if hasattr(shape, "volume"):
        return float(shape.volume)
    return sum(float(child.volume) for child in shape)


def intersection_volume(a, b) -> float:
    return volume(a.intersect(b))


def test_frozen_compact_projection_equations_radii_and_clearances():
    assert V0R1.source_z == pytest.approx(40.0)
    assert [carrier.radius for carrier in V0R1.carriers] == pytest.approx([30.0, 34.75, 39.5])
    assert [
        b.radius - a.radius - V0R1.ring_radial_width
        for a, b in zip(V0R1.carriers, V0R1.carriers[1:])
    ] == pytest.approx([3.15, 3.15])
    for carrier in V0R1.carriers:
        assert projected_radius(V0R1.source_z, carrier.radius, carrier.base_z) == pytest.approx(48.0, abs=1e-6)
        assert projected_radius(V0R1.source_z, carrier.radius, carrier.tip_z) == pytest.approx(
            carrier.target_tip_radius, abs=1e-6
        )


def test_representative_quartz_body_and_global_arbor_contract():
    assert (V0R1.body_x, V0R1.body_y, V0R1.body_depth, V0R1.body_corner_radius) == pytest.approx(
        (56.0, 56.7, 16.0, 3.0)
    )
    assert V0R1.body_corner_envelope_radius < 48.0
    assert V0R1.arbor_segments_global == (
        (0.0, 5.883333333, 12.0),
        (5.883333333, 7.083333333, 8.0),
        (7.083333333, 11.041666667, 6.0),
        (11.041666667, 16.8, 4.0),
    )
    assert V0R1.arbor_global_top == pytest.approx(17.2)
    assert V0R1.body_local_height == pytest.approx(33.2)
    body = make_fake_standard_quartz_body()
    bbox = body.bounding_box()
    assert body.is_valid and len(body.solids()) == 1 and body.volume > 0
    assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx((56.0, 56.7, 33.2), abs=1e-6)
    assert (bbox.min.Z, bbox.max.Z) == pytest.approx((0.0, 33.2), abs=1e-6)
    placed = placed_body().bounding_box()
    assert (placed.min.Z, placed.max.Z) == pytest.approx((-16.0, 17.2), abs=1e-6)


def test_exact_carrier_z_stack_bores_and_towers():
    assert [carrier.ring_bottom_z for carrier in V0R1.carriers] == pytest.approx(
        [13.8, 9.841666667, 5.883333333]
    )
    assert [(c.base_z, c.tip_z) for c in V0R1.carriers] == pytest.approx(
        [(15.0, 25.882352941), (11.041666667, 27.363636364), (7.083333333, 27.846153846)]
    )
    assert V0R1.by_name["second"].bore_diameter - 8.0 == pytest.approx(0.30)
    assert V0R1.by_name["minute"].bore_diameter - 6.0 == pytest.approx(0.30)
    assert V0R1.by_name["hour"].bore_diameter == pytest.approx(4.20)
    assert 2.0 - (V0R1.hour_bore_diameter / 2 - V0R1.hour_pad_radial_protrusion) == pytest.approx(0.05)
    assert (V0R1.by_name["second"].tower_od, V0R1.by_name["second"].tower_height) == pytest.approx(
        (10.4, 3.958333333)
    )
    assert (V0R1.by_name["minute"].tower_od, V0R1.by_name["minute"].tower_height) == pytest.approx(
        (8.4, 3.958333333)
    )


def test_exact_four_connected_part_bounds_and_compact_assembly_envelope():
    expected = {
        "fake_standard_quartz_body": (56.0, 56.7, 33.2),
        "hour_carrier_hand": (61.6, 61.6, 12.082352941),
        "minute_carrier_hand": (71.1, 71.1, 17.521969697),
        "second_carrier_hand": (80.6, 80.6, 21.962820513),
    }
    assert [name for name, _ in part_factories()] == list(expected)
    for name, factory in part_factories():
        shape = factory()
        bbox = shape.bounding_box()
        assert shape.is_valid and shape.volume > 0 and len(shape.solids()) == 1
        assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx(expected[name], abs=0.05)
        assert bbox.min.Z == pytest.approx(0.0)
    assembly = make_assembly()
    bbox = assembly.bounding_box()
    assert len(assembly.solids()) == 4
    assert (bbox.min.X, bbox.min.Y, bbox.min.Z) == pytest.approx((-40.3, -40.3, -16.0), abs=1e-6)
    assert (bbox.max.X, bbox.max.Y, bbox.max.Z) == pytest.approx((40.3, 40.3, 27.846153846), abs=1e-6)


def test_every_five_degree_pose_is_collision_free_except_intended_hour_pad_contact():
    body = placed_body()
    for angle in range(0, 360, 5):
        assert intersection_volume(body, placed_carrier("second", angle)) < 1e-7
        assert intersection_volume(body, placed_carrier("minute", angle)) < 1e-7
        assert intersection_volume(body, placed_carrier("hour", angle)) == pytest.approx(0.26731967, abs=1e-6)
    for fixed_name, moving_name in (("second", "minute"), ("second", "hour"), ("minute", "hour")):
        fixed = placed_carrier(fixed_name, 0)
        for angle in range(0, 360, 5):
            assert intersection_volume(fixed, placed_carrier(moving_name, angle)) < 1e-7


def test_generated_part_and_assembly_steps_match_live_source_geometry_bidirectionally():
    for name, factory in part_factories():
        path = MODEL / f"{name}.step"
        assert path.exists()
        exported = import_step(path)
        source = factory()
        assert exported.is_valid and len(exported.solids()) == 1
        assert volume(source.cut(exported)) < 1e-5
        assert volume(exported.cut(source)) < 1e-5
    assembly = import_step(MODEL / "v0r1_assembled.step")
    assert assembly.is_valid and len(assembly.solids()) == 4
    bbox = assembly.bounding_box()
    assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx((80.6, 80.6, 43.846153846), abs=1e-5)

