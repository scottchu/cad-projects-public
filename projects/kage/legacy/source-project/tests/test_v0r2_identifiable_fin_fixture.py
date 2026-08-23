from __future__ import annotations

from pathlib import Path

import pytest
from build123d import Align, Axis, Box, Compound, Location, import_step

from v0r2_identifiable_fin_fixture_geometry import (
    _fin,
    fin_profile_yz,
    make_assembly,
    make_fake_standard_quartz_body,
    part_factories,
    placed_body,
    placed_carrier,
)
from v0r2_identifiable_fin_fixture_spec import (
    V0R2,
    blocker_z_at_projected_radius,
    fin_physical_width_at_local_z,
    fin_projected_width_at_local_z,
    fin_projected_width_at_wall_radius,
    projected_radius,
    projected_tangential_width,
)


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "v0r2_identifiable_fin_fixture"


def volume(shape) -> float:
    if shape is None:
        return 0.0
    if hasattr(shape, "volume"):
        return float(shape.volume)
    return sum(float(child.volume) for child in shape)


def intersection_volume(a, b) -> float:
    return volume(a.intersect(b))


def test_v0r1_projection_stack_body_and_radii_are_preserved():
    assert V0R2.source_z == pytest.approx(40.0)
    assert (V0R2.body_x, V0R2.body_y, V0R2.body_depth, V0R2.arbor_global_top) == pytest.approx(
        (56.0, 56.7, 16.0, 17.2)
    )
    assert [carrier.radius for carrier in V0R2.carriers] == pytest.approx([30.0, 34.75, 39.5])
    assert [carrier.ring_bottom_z for carrier in V0R2.carriers] == pytest.approx(
        [13.8, 9.841666667, 5.883333333]
    )
    assert [(carrier.base_z, carrier.tip_z) for carrier in V0R2.carriers] == pytest.approx(
        [(15.0, 25.882352941), (11.041666667, 27.363636364), (7.083333333, 27.846153846)]
    )
    for carrier in V0R2.carriers:
        assert projected_radius(V0R2.source_z, carrier.radius, carrier.base_z) == pytest.approx(48.0, abs=1e-6)
        assert projected_radius(V0R2.source_z, carrier.radius, carrier.tip_z) == pytest.approx(
            carrier.target_tip_radius, abs=1e-6
        )


def test_exact_distinct_profiles_and_real_crown_sections():
    expected = {
        "hour": (4.8, 0.8, 3.2),
        "minute": (3.2, 0.8, 1.6),
        "second": (1.6, 0.6, 0.4),
    }
    root = V0R2.ring_axial_thickness - V0R2.fin_root_overlap
    for carrier in V0R2.carriers:
        identity = V0R2.fin_identities[carrier.name]
        assert (identity.stem_width, identity.crown_height, identity.crown_width) == pytest.approx(
            expected[carrier.name]
        )
        crown_base = carrier.local_height - identity.crown_height
        expected_profile = (
            (-identity.stem_width / 2, root),
            (identity.stem_width / 2, root),
            (identity.stem_width / 2, crown_base),
            (identity.crown_width / 2, carrier.local_height),
            (-identity.crown_width / 2, carrier.local_height),
            (-identity.stem_width / 2, crown_base),
        )
        for actual_point, expected_point in zip(fin_profile_yz(carrier), expected_profile):
            assert actual_point == pytest.approx(expected_point)
        fin = _fin(carrier, V0R2)
        assert fin.is_valid and len(fin.solids()) == 1
        assert fin.bounding_box().size.X == pytest.approx(V0R2.fin_radial_thickness)
        assert fin.bounding_box().size.Y == pytest.approx(identity.stem_width)
        # Thin physical section proves the BREP follows the same taper function.
        probe_z = carrier.local_height - 0.01
        probe = Box(
            3.0, 10.0, 0.01,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((carrier.radius, 0, probe_z)))
        section = Compound(children=list(fin.intersect(probe)))
        assert section.bounding_box().size.Y == pytest.approx(
            fin_physical_width_at_local_z(carrier, probe_z), abs=1e-6
        )


def test_projection_width_functions_at_base_mid_tip_and_common_wall_radii():
    expected = {
        "hour": {
            "samples": (7.619048, 9.766607, 9.066667),
            "common": (9.6, 12.8),
        },
        "minute": {
            "samples": (4.389826, 6.125179, 5.064748),
            "common": (5.52518, 7.366906),
        },
        "second": {
            "samples": (1.932562, 2.827448, 1.316456),
            "common": (2.43038, 3.240506),
        },
    }
    root = V0R2.ring_axial_thickness - V0R2.fin_root_overlap
    for carrier in V0R2.carriers:
        midpoint = (root + carrier.local_height) / 2
        samples = tuple(
            fin_projected_width_at_local_z(carrier, z)
            for z in (root, midpoint, carrier.local_height)
        )
        common = tuple(fin_projected_width_at_wall_radius(carrier, radius) for radius in (60.0, 80.0))
        assert samples == pytest.approx(expected[carrier.name]["samples"], abs=1e-6)
        assert common == pytest.approx(expected[carrier.name]["common"], abs=1e-6)
        for radius in (60.0, 80.0):
            z = blocker_z_at_projected_radius(V0R2.source_z, carrier.radius, radius)
            assert projected_radius(V0R2.source_z, carrier.radius, z) == pytest.approx(radius)
    assert projected_tangential_width(40, 4.8, 15) == pytest.approx(7.68)


def test_support_free_print_section_and_minimum_feature_contract():
    for identity in V0R2.fin_identities.values():
        run_per_side = (identity.stem_width - identity.crown_width) / 2
        assert run_per_side == pytest.approx(identity.crown_height)
        assert identity.stem_width >= 4 * V0R2.nozzle_diameter
        assert identity.crown_width >= V0R2.nozzle_diameter
        assert identity.crown_height >= 3 * V0R2.layer_height - 1e-9
    assert V0R2.fin_radial_thickness == pytest.approx(4 * V0R2.nozzle_diameter)


def test_four_connected_parts_bounds_and_compact_assembly_envelope():
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
    body = make_fake_standard_quartz_body()
    assert body.bounding_box().size.Z == pytest.approx(33.2)
    assembly = make_assembly()
    bbox = assembly.bounding_box()
    assert len(assembly.solids()) == 4
    assert (bbox.min.X, bbox.min.Y, bbox.min.Z) == pytest.approx((-40.3, -40.3, -16.0), abs=1e-6)
    assert (bbox.max.X, bbox.max.Y, bbox.max.Z) == pytest.approx((40.3, 40.3, 27.846153846), abs=1e-6)


def test_every_five_degree_pose_is_collision_free_except_intended_hour_pad_contact():
    body = placed_body()
    carriers = {
        name: placed_carrier(name, 0)
        for name in ("second", "minute", "hour")
    }
    for angle in range(0, 360, 5):
        assert intersection_volume(body, carriers["second"].rotate(Axis.Z, angle)) < 1e-7
        assert intersection_volume(body, carriers["minute"].rotate(Axis.Z, angle)) < 1e-7
        assert intersection_volume(body, carriers["hour"].rotate(Axis.Z, angle)) == pytest.approx(0.26731967, abs=1e-6)
    for fixed_name, moving_name in (("second", "minute"), ("second", "hour"), ("minute", "hour")):
        fixed = carriers[fixed_name]
        for angle in range(0, 360, 5):
            assert intersection_volume(fixed, carriers[moving_name].rotate(Axis.Z, angle)) < 1e-7


def test_generated_part_and_assembly_steps_match_live_source_geometry_bidirectionally():
    for name, factory in part_factories():
        path = MODEL / f"{name}.step"
        assert path.exists()
        exported = import_step(path)
        source = factory()
        assert exported.is_valid and len(exported.solids()) == 1
        assert volume(source.cut(exported)) < 1e-5
        assert volume(exported.cut(source)) < 1e-5
    assembly = import_step(MODEL / "v0r2_assembled.step")
    assert assembly.is_valid and len(assembly.solids()) == 4
    bbox = assembly.bounding_box()
    assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx((80.6, 80.6, 43.846153846), abs=1e-5)
