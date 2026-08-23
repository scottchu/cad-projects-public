from __future__ import annotations

from hashlib import sha256
from itertools import product
from math import cos, radians, sin
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
from build123d import Location

from p2_magnetic_three_channel_mvp_geometry import (
    make_assembled,
    make_front_cap_ring,
    make_hidden_driver,
    make_rear_base,
    make_separator,
    make_follower,
    pairwise_intersection_volume,
    placed_follower,
    placed_hidden_driver,
)
from p2_magnetic_three_channel_mvp_spec import P2, V0R2_ISOLATION_SHA256


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_primary_dimensions_and_magnet_fit():
    assert P2.fixture_od == 220.0
    assert P2.center_open_diameter == 52.0
    assert P2.track_radii == (45.0, 65.0, 85.0)
    assert P2.separator_options == (1.0, 1.5, 2.0)
    assert (P2.magnet_diameter, P2.magnet_thickness) == (6.0, 3.0)
    assert (P2.magnet_pocket_diameter, P2.magnet_pocket_depth) == (6.15, 3.10)
    assert P2.shoe_overlap_per_side == pytest.approx(2.10)
    assert P2.slot_radial - P2.neck_radial == pytest.approx(0.60)
    assert P2.driver_race_radial_width - P2.driver_ring_radial_width == pytest.approx(0.60)


def test_track_envelopes_are_continuously_disjoint_analytically():
    shoe_spans = [(radius - 4.5, radius + 4.5) for radius in P2.track_radii]
    fin_spans = [
        (channel.radius - channel.fin_radial / 2, channel.radius + channel.fin_radial / 2)
        for channel in P2.channels
    ]
    boss_spans = [(radius - 4.5, radius + 4.5) for radius in P2.track_radii]
    for spans, minimum_gap in ((shoe_spans, 11.0), (boss_spans, 11.0)):
        assert spans[1][0] - spans[0][1] >= minimum_gap
        assert spans[2][0] - spans[1][1] >= minimum_gap
    assert fin_spans[1][0] - fin_spans[0][1] >= 12.5
    assert fin_spans[2][0] - fin_spans[1][1] >= 13.5


def test_all_373248_five_degree_angle_states_preserve_radial_independence():
    spans = {
        channel.name: (
            channel.radius - P2.shoe_radial / 2,
            channel.radius + P2.shoe_radial / 2,
        )
        for channel in P2.channels
    }
    angles = range(0, 360, 5)
    count = 0
    for hour_angle, minute_angle, second_angle in product(angles, repeat=3):
        # Angular coordinates affect tangential position only. Independent
        # closed radial intervals are therefore a continuous all-angle proof.
        assert spans["hour"][1] < spans["minute"][0]
        assert spans["minute"][1] < spans["second"][0]
        count += 1
    assert count == 373_248


def test_magnet_pair_gaps_and_wrong_pair_clearances():
    assert [P2.matching_face_gap(t) for t in P2.separator_options] == pytest.approx(
        [1.50, 2.00, 2.50]
    )
    assert P2.adjacent_magnet_edge_gaps == (14.0, 14.0, 34.0)
    for thickness in P2.separator_options:
        assert P2.wrong_pair_center_distance(20.0, thickness) > 20.4
        assert P2.wrong_pair_surface_metric(14.0, thickness) > 14.0


def test_separator_variants_are_one_valid_solid_with_exact_bounds_and_holes():
    for thickness in P2.separator_options:
        separator = make_separator(thickness)
        bbox = separator.bounding_box()
        assert separator.is_valid and len(separator.solids()) == 1
        assert (bbox.size.X, bbox.size.Y) == pytest.approx((220.0, 220.0))
        assert bbox.min.Z == pytest.approx(P2.separator_rear_z)
        assert bbox.max.Z == pytest.approx(P2.separator_rear_z + thickness + P2.separator_boss_height)


def test_four_cap_rings_are_independent_valid_solids_with_exact_spans():
    for index, (inner, outer) in enumerate(P2.cap_spans):
        cap = make_front_cap_ring(index)
        bbox = cap.bounding_box()
        assert cap.is_valid and len(cap.solids()) == 1
        assert bbox.size.X == pytest.approx(2 * outer)
        assert bbox.size.Y == pytest.approx(2 * outer)
        assert bbox.size.Z == pytest.approx(P2.cap_thickness)
        assert inner >= P2.center_open_radius
    assert [len(angles) for angles in P2.cap_fastener_angles] == [3, 3, 3, 6]


def test_cap_slots_are_continuous_360_degree_open_annuli():
    caps = tuple(make_front_cap_ring(index) for index in range(4))
    for angle in range(360):
        c = cos(radians(angle))
        s = sin(radians(angle))
        for inner, outer in P2.slot_spans:
            radius = (inner + outer) / 2
            point = (radius * c, radius * s, P2.cap_thickness / 2)
            assert not any(cap.is_inside(point) for cap in caps)


def test_v0r2_fake_fixture_is_byte_identical_to_pre_p2_baseline():
    for relative, expected in V0R2_ISOLATION_SHA256.items():
        path = ROOT / relative
        assert path.exists()
        assert sha256(path.read_bytes()).hexdigest() == expected


def test_p2_namespace_is_absent_from_v0r2_sources_and_print_bundle():
    root_sources = (
        ROOT / "v0r2_identifiable_fin_fixture_spec.py",
        ROOT / "v0r2_identifiable_fin_fixture_geometry.py",
        ROOT / "v0r2_identifiable_fin_fixture_export.py",
    )
    for path in root_sources:
        assert "p2_magnetic_three_channel_mvp" not in path.read_text()
    old_bundle = ROOT / "models/v0r2_identifiable_fin_fixture/print/v0r2_four_part_identifiable_fin_test.3mf"
    assert b"p2_magnetic_three_channel_mvp" not in old_bundle.read_bytes()


def test_all_primary_part_factories_are_valid_positive_one_solid():
    shapes = [make_rear_base()]
    shapes.extend(make_hidden_driver(name) for name in ("hour", "minute", "second"))
    shapes.extend(make_separator(t) for t in P2.separator_options)
    shapes.extend(make_front_cap_ring(i) for i in range(4))
    shapes.extend(make_follower(name, 1.5) for name in ("hour", "minute", "second"))
    for shape in shapes:
        assert shape.is_valid
        assert len(shape.solids()) == 1
        assert shape.volume > 0


def test_open_back_cassette_and_coplanar_driver_contract():
    base = make_rear_base()
    assert len(base.solids()) == 1
    assert base.bounding_box().min.Z == pytest.approx(0.0)
    assert base.bounding_box().max.Z == pytest.approx(P2.separator_rear_z)
    assert not base.is_inside((0, 0, 1.0))
    assert P2.driver_z[0] - P2.pad_z[1] == pytest.approx(0.30)
    assert P2.driver_z[0] - P2.backbone_z[1] == pytest.approx(1.40)
    assert P2.driver_boss_top_z - P2.driver_z[1] == pytest.approx(0.30)
    assert P2.driver_boss_top_z - P2.magnet_pocket_depth - P2.driver_z[0] == pytest.approx(0.60)
    for name in ("hour", "minute", "second"):
        driver = make_hidden_driver(name)
        assert driver.bounding_box().min.Z == pytest.approx(2.6)
        assert driver.bounding_box().max.Z == pytest.approx(6.3)


def test_six_integral_m3_spacers_form_the_stationary_hard_datum_and_true_through_paths():
    base = make_rear_base()
    spacer_inner_radius = P2.stationary_hole_radius - P2.stationary_spacer_diameter / 2
    spacer_outer_radius = P2.stationary_hole_radius + P2.stationary_spacer_diameter / 2
    assert len(P2.cap_fastener_angles[3]) == 6
    assert P2.stationary_spacer_z == pytest.approx((2.3, 6.3))
    assert P2.stationary_spacer_z[1] - P2.stationary_spacer_z[0] == pytest.approx(4.0)
    assert spacer_inner_radius == pytest.approx(100.0)
    assert spacer_inner_radius > P2.driver_max_radial_envelope
    assert len(base.solids()) == 1 and base.is_valid
    assert base.bounding_box().max.Z == pytest.approx(P2.separator_rear_z)

    for angle in P2.cap_fastener_angles[3]:
        c, s = cos(radians(angle)), sin(radians(angle))
        # Annular column material exists on both radial sides at mid-height.
        assert base.is_inside(((spacer_inner_radius + 0.15) * c, (spacer_inner_radius + 0.15) * s, 4.3))
        assert base.is_inside(((spacer_outer_radius - 0.15) * c, (spacer_outer_radius - 0.15) * s, 4.3))
        # The M3 clearance remains open continuously through column and base.
        for z in (0.1, 1.15, 2.25, 2.4, 4.3, 6.2):
            assert not base.is_inside((P2.stationary_hole_radius * c, P2.stationary_hole_radius * s, z))

    separator = make_separator(1.5)
    assert separator.bounding_box().min.Z == pytest.approx(base.bounding_box().max.Z)
    assert pairwise_intersection_volume(base, separator) <= 1e-6


def test_spacer_columns_are_support_free_and_rear_open_area_is_preserved():
    base = make_rear_base()
    # Every vertical column footprint is backed by the outer base ring at z2.0.
    for angle in P2.cap_fastener_angles[3]:
        c, s = cos(radians(angle)), sin(radians(angle))
        for radius in (100.2, 105.8):
            assert base.is_inside((radius * c, radius * s, 2.0))
            assert base.is_inside((radius * c, radius * s, 4.0))
    # Representative rear access points between the narrow structural ribs
    # remain completely open beneath the driver channels.
    for radius in (35.0, 55.0, 75.0, 95.0):
        for angle in (10.0, 70.0, 190.0, 310.0):
            c, s = cos(radians(angle)), sin(radians(angle))
            assert not base.is_inside((radius * c, radius * s, 0.6))


def test_coplanar_driver_sweeps_clear_base_and_each_other():
    base = make_rear_base()
    names = ("hour", "minute", "second")
    for name in names:
        for angle in range(360):
            assert pairwise_intersection_volume(placed_hidden_driver(name, angle), base) <= 1e-6
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            fixed = placed_hidden_driver(left, 0)
            for angle in range(360):
                assert pairwise_intersection_volume(fixed, placed_hidden_driver(right, angle)) <= 1e-6


def test_all_relative_angles_have_zero_cross_channel_solid_intersection_volume():
    pairs = (("hour", "minute"), ("minute", "second"), ("hour", "second"))
    for left_name, right_name in pairs:
        fixed_driver = placed_hidden_driver(left_name, 0)
        fixed_follower = placed_follower(left_name, 1.5, 0)
        for relative_angle in range(360):
            assert pairwise_intersection_volume(
                fixed_driver, placed_hidden_driver(right_name, relative_angle)
            ) <= 1e-6
            assert pairwise_intersection_volume(
                fixed_follower, placed_follower(right_name, 1.5, relative_angle)
            ) <= 1e-6


def test_individual_360_sweeps_clear_stationary_parts_except_running_contact_faces():
    base = make_rear_base()
    separator = make_separator(1.5)
    caps = tuple(
        make_front_cap_ring(index).moved(Location((0, 0, P2.separator_rear_z + 1.5 + 4.0)))
        for index in range(4)
    )
    for channel_name in ("hour", "minute", "second"):
        for angle in range(360):
            driver = placed_hidden_driver(channel_name, angle)
            follower = placed_follower(channel_name, 1.5, angle)
            # Driver support pads are declared running/contact faces; only the
            # separator and cap solids must be strictly nonintersecting.
            assert pairwise_intersection_volume(driver, separator) <= 1e-6
            for cap in caps:
                assert pairwise_intersection_volume(follower, cap) <= 1e-6


def test_default_assembly_is_valid_and_contains_twelve_labeled_occurrences():
    assembly = make_assembled(1.5)
    assert assembly.is_valid
    assert len(assembly.solids()) == 12


def test_three_variant_3mf_bundles_have_exact_twelve_named_objects():
    print_root = ROOT / "models/p2_magnetic_three_channel_mvp/print"
    expected_common = [
        "rear_base",
        "hidden_driver_hour",
        "hidden_driver_minute",
        "hidden_driver_second",
    ]
    expected_tail = [
        "front_cap_ring_r0",
        "front_cap_ring_r1",
        "front_cap_ring_r2",
        "front_cap_ring_r3",
        "follower_hour_fin",
        "follower_minute_fin",
        "follower_second_fin",
    ]
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    for thickness in P2.separator_options:
        tag = str(thickness).replace(".", "p")
        path = print_root / f"p2_magnetic_three_channel_mvp_t{tag}.3mf"
        assert path.exists() and path.stat().st_size > 0
        with ZipFile(path) as package:
            assert package.testzip() is None
            root = ET.fromstring(package.read("3D/3dmodel.model"))
        names = [obj.attrib["name"] for obj in root.findall("m:resources/m:object", ns)]
        assert names == [*expected_common, f"separator_t{tag}", *expected_tail]
        assert len(root.findall("m:build/m:item", ns)) == 12
