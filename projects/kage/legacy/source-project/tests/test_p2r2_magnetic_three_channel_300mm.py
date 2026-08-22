from __future__ import annotations

from hashlib import sha256
from itertools import product
from math import cos, radians, sin
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh
from build123d import Axis, Location

from p2r2_magnetic_three_channel_300mm_export import mesh_data
from p2r2_magnetic_three_channel_300mm_geometry import (
    make_assembled,
    make_follower,
    make_front_cap_ring,
    make_hidden_driver,
    make_rear_base,
    make_separator,
    pairwise_intersection_volume,
)
from p2r2_magnetic_three_channel_300mm_spec import P2R1_ISOLATION_SHA256, P2R2


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_300mm_layout_and_functional_cross_sections():
    assert P2R2.fixture_od == 300.0
    assert P2R2.plate_outer_radius == 150.0
    assert P2R2.center_open_diameter == 52.0
    assert P2R2.track_radii == (95.0, 115.0, 135.0)
    assert P2R2.slot_spans == ((92.6, 97.4), (112.6, 117.4), (132.6, 137.4))
    assert P2R2.cap_spans == ((26.0, 92.6), (97.4, 112.6), (117.4, 132.6), (137.4, 147.0))
    assert (P2R2.magnet_pocket_diameter, P2R2.magnet_pocket_depth) == (6.15, 3.10)
    assert (P2R2.shoe_radial, P2R2.shoe_thickness, P2R2.slot_radial) == (9.0, 3.4, 4.8)
    assert P2R2.shoe_overlap_per_side == pytest.approx(2.10)
    assert [len(sites) for sites in P2R2.cap_fastener_sites] == [6, 3, 3, 6]


def test_outer_clearances_and_fastener_border_are_exact():
    assert P2R2.track_radii[-1] + P2R2.shoe_radial / 2 == pytest.approx(139.5)
    assert P2R2.track_radii[-1] + P2R2.magnet_boss_diameter / 2 == pytest.approx(139.5)
    assert P2R2.track_radii[-1] + P2R2.channels[-1].fin_radial / 2 == pytest.approx(138.0)
    spacer_inner = P2R2.stationary_hole_radius - P2R2.stationary_spacer_diameter / 2
    spacer_outer = P2R2.stationary_hole_radius + P2R2.stationary_spacer_diameter / 2
    assert (spacer_inner, spacer_outer) == pytest.approx((140.5, 146.5))
    assert spacer_inner - P2R2.driver_max_radial_envelope == pytest.approx(1.0)
    assert P2R2.stationary_hole_radius + P2R2.m3_washer_diameter / 2 == pytest.approx(147.0)
    assert P2R2.plate_outer_radius - 147.0 == pytest.approx(3.0)


def test_373248_five_degree_states_preserve_continuous_radial_independence():
    spans = {
        channel.name: (channel.radius - P2R2.shoe_radial / 2, channel.radius + P2R2.shoe_radial / 2)
        for channel in P2R2.channels
    }
    count = 0
    for _angles in product(range(0, 360, 5), repeat=3):
        assert spans["hour"][1] < spans["minute"][0]
        assert spans["minute"][1] < spans["second"][0]
        count += 1
    assert count == 373_248


def test_primary_parts_are_valid_positive_single_solids_and_expected_bounds():
    parts = [make_rear_base()]
    parts.extend(make_hidden_driver(name) for name in ("hour", "minute", "second"))
    parts.extend(make_separator(t) for t in P2R2.separator_options)
    parts.extend(make_front_cap_ring(index) for index in range(4))
    parts.extend(make_follower(name, 1.5) for name in ("hour", "minute", "second"))
    for part in parts:
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0
    assert make_rear_base().bounding_box().size.X == pytest.approx(300.0)
    assert make_separator(1.5).bounding_box().size.X == pytest.approx(300.0)
    assembly = make_assembled(1.5)
    bbox = assembly.bounding_box()
    assert assembly.is_valid and len(assembly.solids()) == 12
    assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx((300.0, 300.0, 63.6))


def test_base_is_one_manifold_shell_with_integral_backbones_pads_and_spacers():
    base = make_rear_base()
    mesh = mesh_data(base)
    assert mesh.body_count == 1 and mesh.is_watertight and mesh.is_volume
    # Backbones occupy the exact radial span r26..144 at the three phases.
    for angle in P2R2.backbone_angles:
        c, s = cos(radians(angle)), sin(radians(angle))
        # r143.5 is intentionally interrupted by the M3 through path; sample
        # the conformal backbone/ring overlap away from that fastener bore.
        for radius in (26.1, 95.0, 137.9, 139.5):
            assert base.is_inside((radius * c, radius * s, 0.6))
    # Six spacer paths remain open through the integrated base columns.
    for radius, angle in P2R2.cap_fastener_sites[3]:
        c, s = cos(radians(angle)), sin(radians(angle))
        for z in (0.1, 2.2, 4.3, 6.2):
            assert not base.is_inside((radius * c, radius * s, z))


def test_cap_fastener_sites_have_material_ligament_and_tracks_stay_open():
    caps = [make_front_cap_ring(i) for i in range(4)]
    for index, cap in enumerate(caps):
        assert len(cap.solids()) == 1
        for radius, angle in P2R2.cap_fastener_sites[index]:
            c, s = cos(radians(angle)), sin(radians(angle))
            sample_offset = 2.3 if index < 3 else 2.1
            assert cap.is_inside(((radius + sample_offset) * c, (radius + sample_offset) * s, 0.2))
    for angle in range(360):
        c, s = cos(radians(angle)), sin(radians(angle))
        for inner, outer in P2R2.slot_spans:
            radius = (inner + outer) / 2
            assert not any(cap.is_inside((radius * c, radius * s, 0.9)) for cap in caps)


def test_pairwise_solid_brep_bounded_relative_angle_sweeps():
    base = make_rear_base()
    separator = make_separator(1.5)
    drivers = {name: make_hidden_driver(name) for name in ("hour", "minute", "second")}
    followers = {name: make_follower(name, 1.5) for name in ("hour", "minute", "second")}
    critical_angles = sorted(set(range(0, 360, 15)) | {0, 1, 29, 30, 59, 60, 89, 90, 119, 120, 179, 180, 239, 240, 299, 300, 359})
    # Bounded grid plus exact transition-neighbor angles against stationary structure; uses solid intersections,
    # never Compound.intersect (which previously yielded false zeroes).
    for name in drivers:
        for angle in critical_angles:
            driver = drivers[name].rotate(Axis.Z, angle)
            assert pairwise_intersection_volume(driver, base) <= 1e-6
            assert pairwise_intersection_volume(driver, separator) <= 1e-6
    # Bounded 15-degree relative BREP samples complement the continuous radial
    # interval proof above without creating an unbounded CAD-kernel test.
    pairs = (("hour", "minute"), ("minute", "second"), ("hour", "second"))
    for left, right in pairs:
        for angle in critical_angles:
            assert pairwise_intersection_volume(drivers[left], drivers[right].rotate(Axis.Z, angle)) <= 1e-6
            assert pairwise_intersection_volume(followers[left], followers[right].rotate(Axis.Z, angle)) <= 1e-6


def test_followers_clear_all_placed_cap_rings_at_critical_angles():
    caps = [
        make_front_cap_ring(index).moved(Location((0, 0, P2R2.separator_rear_z + 1.5 + 4.0)))
        for index in range(4)
    ]
    critical_angles = sorted(set(range(0, 360, 15)) | {0, 1, 29, 30, 59, 60, 89, 90, 119, 120, 179, 180, 239, 240, 299, 300, 359})
    for name in ("hour", "minute", "second"):
        follower = make_follower(name, 1.5)
        for angle in critical_angles:
            moved = follower.rotate(Axis.Z, angle)
            for cap in caps:
                assert pairwise_intersection_volume(moved, cap) <= 1e-6


def test_p2r1_source_and_accepted_artifacts_remain_byte_identical():
    for relative, expected in P2R1_ISOLATION_SHA256.items():
        path = ROOT / relative
        assert path.exists()
        assert sha256(path.read_bytes()).hexdigest() == expected


def test_three_transfer_bundles_and_individual_plates_are_current_and_named():
    print_root = ROOT / "models/p2r2_magnetic_three_channel_300mm/print"
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    for thickness in P2R2.separator_options:
        tag = str(thickness).replace(".", "p")
        bundle = print_root / f"p2r2_magnetic_three_channel_300mm_t{tag}.3mf"
        assert bundle.exists() and bundle.stat().st_size > 0
        with ZipFile(bundle) as package:
            assert package.testzip() is None
            root = ET.fromstring(package.read("3D/3dmodel.model"))
        objects = root.findall("m:resources/m:object", ns)
        items = root.findall("m:build/m:item", ns)
        assert len(objects) == len(items) == 12
        assert [obj.attrib["name"] for obj in objects][4] == f"separator_t{tag}"
        part_root = print_root / f"t{tag}_individual_plates"
        parts = sorted(part_root.glob("*.3mf"))
        assert len(parts) == 12
        for path in parts:
            with ZipFile(path) as package:
                assert package.testzip() is None
                part = ET.fromstring(package.read("3D/3dmodel.model"))
            assert len(part.findall("m:resources/m:object", ns)) == 1
            vertices = part.findall("m:resources/m:object/m:mesh/m:vertices/m:vertex", ns)
            assert min(float(v.attrib["z"]) for v in vertices) == pytest.approx(0.0, abs=1e-7)


def test_canonical_stls_are_single_watertight_positive_shells():
    print_root = ROOT / "models/p2r2_magnetic_three_channel_300mm/print"
    stls = sorted(print_root.glob("*.stl"))
    assert len(stls) >= 12
    for path in stls:
        mesh = trimesh.load_mesh(path, process=True, validate=True)
        assert mesh.body_count == 1 and mesh.is_watertight and mesh.is_volume
