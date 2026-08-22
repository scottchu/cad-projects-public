"""Frozen math, geometry, isolation, and artifact tests for KAGE P3 V3."""

from __future__ import annotations

from hashlib import sha256
import json
from math import cos, radians, sin
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import pytest
from OCP.BRepCheck import BRepCheck_Analyzer
from build123d import Axis, import_step

import p3_v3_stacked_three_motor_90deg_geometry as g
from p3_v3_stacked_three_motor_90deg_spec import P3_V2_ISOLATION_SHA256, P3_V3 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_stacked_three_motor_90deg"


def _assert_valid_solid(shape):
    assert shape.is_valid
    assert BRepCheck_Analyzer(shape.wrapped).IsValid()
    assert len(shape.solids()) == 1
    assert shape.volume > 0.0


def test_p3_v2_checkpoint_is_byte_for_byte_untouched():
    for relative, expected in P3_V2_ISOLATION_SHA256.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative


def test_exact_stack_layers_gaps_and_static_fallback_gates():
    assert p.frame_radii == (141.0, 150.0) and p.frame_z == (0.0, 2.4)
    assert p.carrier_radii == (130.5, 135.5)
    assert p.carrier_layers == ((2.8, 5.8), (6.2, 9.2), (9.6, 12.6))
    assert p.carrier_stack_height == pytest.approx(9.8)
    assert p.fin_lane_centers == pytest.approx((138.1, 136.5, 134.9))
    assert p.fin_lane_centers[0] > p.fin_lane_centers[1] > p.fin_lane_centers[2]
    assert p.fin_lane_gaps == pytest.approx((0.0, 0.4, 0.4, 2.3))
    assert p.total_rear_depth == pytest.approx(25.5)
    assert p.total_rear_depth <= 28.0 and p.carrier_stack_height <= 10.0
    assert p.fin_lane_gaps[0] == pytest.approx(0.0)
    assert min(p.fin_lane_gaps[1:]) >= 0.4 - 1e-9


def test_exact_259_to_12_ratio_step_and_seconds_speed_equations():
    assert (p.internal_gear_module, p.internal_gear_teeth) == (1.0, 259)
    assert (p.internal_pitch_radius, p.internal_tip_radius, p.internal_root_radius) == (129.5, 128.5, 130.75)
    assert (p.pinion_teeth, p.pinion_pitch_radius, p.pinion_outer_radius, p.pinion_root_radius) == (12, 6.0, 7.0, 4.75)
    assert p.gear_ratio == pytest.approx(21.583333333333332)
    assert p.carrier_full_step_degrees == pytest.approx(0.0833976833976834)
    assert p.carrier_microstep_degrees == pytest.approx(0.005212355212355213)
    assert p.seconds_motor_rpm == pytest.approx(21.583333333333332)
    assert p.seconds_microsteps_per_second == pytest.approx(1151.111111111111)


@pytest.mark.parametrize("role_index", range(3))
def test_each_259t_carrier_and_12t_pinion_is_one_valid_brep(role_index):
    carrier = g.make_internal_gear_carrier(role_index)
    pinion = g.make_pinion(role_index)
    _assert_valid_solid(carrier)
    _assert_valid_solid(pinion)
    assert carrier.bounding_box().min.Z == pytest.approx(p.carrier_layers[role_index][0])
    assert carrier.bounding_box().max.Z == pytest.approx(p.carrier_layers[role_index][1])
    assert pinion.bounding_box().size.Z == pytest.approx(2.8)
    carrier_vertices, _ = carrier.tessellate(0.02, 0.04)
    pinion_vertices, _ = pinion.moved(
        g.Location((*g._polar(-p.output_axis_radius, p.motor_station_angles[role_index]), 0.0))
    ).tessellate(0.02, 0.04)
    carrier_radii = [(v.X * v.X + v.Y * v.Y) ** 0.5 for v in carrier_vertices]
    pinion_radii = [(v.X * v.X + v.Y * v.Y) ** 0.5 for v in pinion_vertices]
    assert min(carrier_radii) == pytest.approx(p.internal_tip_radius, abs=0.002)
    assert max(carrier_radii) == pytest.approx(p.carrier_radii[1], abs=0.002)
    assert min(pinion_radii) == pytest.approx(p.pinion_bore_radius, abs=0.002)
    assert min(abs(radius - p.pinion_root_radius) for radius in pinion_radii) < 0.002
    assert max(pinion_radii) == pytest.approx(p.pinion_outer_radius, abs=0.002)


def test_pinion_contact_envelopes_and_output_shaft_interfaces_are_disjoint():
    for role in range(3):
        shaft = g.make_output_shaft(role)
        pinion = g.make_pinion(role)
        ring = g.make_internal_gear_carrier(role)
        # Contact-envelope teeth are phased and trimmed at the carrier surface;
        # separate STEP occurrences never claim the same material volume.
        assert g.positive_intersection_volume(pinion, ring) == pytest.approx(0.0, abs=1e-6)
        assert g.positive_intersection_volume(shaft, pinion) == pytest.approx(0.0, abs=1e-6)
        assert g.positive_intersection_volume(shaft, ring) == pytest.approx(0.0, abs=1e-8)
        for other in range(3):
            if other == role:
                continue
            assert g.positive_intersection_volume(shaft, g.make_pinion(other)) == pytest.approx(0.0, abs=1e-8)
            assert g.positive_intersection_volume(shaft, g.make_internal_gear_carrier(other)) == pytest.approx(0.0, abs=1e-8)
    assert p.shaft_to_non_driven_tooth_clearance == pytest.approx(2.9)


def test_motors_and_provisional_miter_envelopes_have_frozen_clearances():
    assert p.motor_station_angles == (0.0, 120.0, 240.0)
    assert p.motor_keepout == (20.6, 20.6, 39.3)
    assert p.motor_body_z == (-23.1, -2.5)
    assert p.miter_outer_radius == pytest.approx(128.3)
    assert p.internal_tip_radius - p.miter_outer_radius == pytest.approx(0.2)
    for first in range(3):
        body = g.make_motor_body(first)
        assert body.bounding_box().min.Z == pytest.approx(-23.1)
        assert body.bounding_box().max.Z == pytest.approx(-2.5)
        horizontal, vertical = g.make_miter_pair(first)
        assert g.positive_intersection_volume(horizontal, vertical) == pytest.approx(0.0, abs=1e-6)
        assert g.positive_intersection_volume(g.make_motor_shaft(first), g.make_output_shaft(first)) == pytest.approx(0.0, abs=1e-6)
        assert g.positive_intersection_volume(g.make_motor_shaft(first), vertical) == pytest.approx(0.0, abs=1e-6)
        assert g.positive_intersection_volume(horizontal, g.make_output_shaft(first)) == pytest.approx(0.0, abs=1e-6)
        lower_bearing = g.make_bearing(first, p.lower_bearing_support_z)
        lower_plate = g.make_bearing_plate(p.lower_bearing_support_z)
        assert g.positive_intersection_volume(horizontal, lower_bearing) == pytest.approx(0.0, abs=1e-6)
        assert g.positive_intersection_volume(horizontal, lower_plate) == pytest.approx(0.0, abs=1e-6)
        for second in range(first + 1, 3):
            assert g.positive_intersection_volume(body, g.make_motor_body(second)) == pytest.approx(0.0, abs=1e-8)
    center_separation = 2.0 * ((p.motor_face_radius + p.motor_inward_radius) / 2.0) * sin(radians(60.0))
    assert center_separation - p.motor_keepout[0] > 3.0
    assert p.motor_far_outer_corner_radius < p.internal_tip_radius


@pytest.mark.parametrize("role", range(2))
def test_each_root_connects_only_its_own_carrier_to_its_fin(role):
    carrier = g.make_internal_gear_carrier(role)
    root = g._root_arm(role, p)
    fin = g._upright_fin(role, p)
    assembly = g.make_carrier_with_fin(role)
    assert g.positive_intersection_volume(carrier, root) > 0.05
    assert g.positive_intersection_volume(root, fin) > 0.05
    _assert_valid_solid(assembly)
    assert assembly.bounding_box().max.Z == pytest.approx(p.fin_tip_zs[role])


def test_top_red_fin_is_directly_fused_to_carrier_outer_top_band():
    role = p.direct_top_fin_role
    carrier = g.make_internal_gear_carrier(role)
    fin = g._upright_fin(role, p)
    assembly = g.make_carrier_with_fin(role)
    assert p.direct_top_fin_footprint_radii == pytest.approx((134.3, 135.5))
    assert p.direct_top_fin_base_z == pytest.approx(p.carrier_layers[role][1] - 0.20)
    assert g.positive_intersection_volume(carrier, fin) > 0.01
    with pytest.raises(ValueError):
        g._root_arm(role, p)
    _assert_valid_solid(assembly)
    assert "DIRECT_TOP_OUTER_BAND" in assembly.label


def test_dense_independent_and_coincident_fin_motion_preserves_lane_clearance():
    half = p.fin_radial_width / 2.0
    intervals = sorted((radius - half, radius + half) for radius in p.fin_lane_centers)
    for hour_angle in range(0, 361, 2):
        hx, hy = cos(radians(hour_angle)), sin(radians(hour_angle))
        assert hx * hx + hy * hy == pytest.approx(1.0)
        for minute_angle in range(0, 361, 2):
            mx, my = cos(radians(minute_angle)), sin(radians(minute_angle))
            assert mx * mx + my * my == pytest.approx(1.0)
            assert intervals[1][0] - intervals[0][1] >= 0.4 - 1e-9
    for second_angle in range(0, 361, 2):
        sx, sy = cos(radians(second_angle)), sin(radians(second_angle))
        assert sx * sx + sy * sy == pytest.approx(1.0)
        assert intervals[2][0] - intervals[1][1] >= 0.4 - 1e-9
    coincident = g.make_coincident_fins_closeup()
    assert coincident.is_valid and len(coincident.children) == 4
    coincident_bodies = [
        g.make_carrier_with_fin(role, p).rotate(Axis.Z, -p.display_fin_angles[role])
        for role in range(3)
    ]
    for first in range(3):
        for second in range(first + 1, 3):
            assert g.positive_intersection_volume(
                coincident_bodies[first], coincident_bodies[second]
            ) == pytest.approx(0.0, abs=1e-8)


def test_all_fins_clear_common_stack_top_and_preserve_frozen_cross_sections():
    assert p.common_visible_fin_base_z == pytest.approx(12.6)
    assert p.fin_tangential_widths == pytest.approx((3.0, 2.0, 1.2))
    assert p.fin_radial_width == pytest.approx(1.2)
    assert p.fin_tip_zs == pytest.approx((17.904, 21.8, 24.5828571429))
    assert p.visible_fin_heights == pytest.approx((5.304, 9.2, 11.9828571429))
    assert p.fin_above_own_carrier_top_heights == pytest.approx((12.104, 12.6, 11.9828571429))
    assert max(p.fin_above_own_carrier_top_heights) - min(p.fin_above_own_carrier_top_heights) < 0.7
    assert all(tip > p.common_visible_fin_base_z for tip in p.fin_tip_zs)
    for role in range(3):
        fin = g._upright_fin(role, p)
        assert fin.bounding_box().size.X > 0.0
        assert fin.bounding_box().size.Y > 0.0
        assert fin.bounding_box().size.Z == pytest.approx(p.fin_tip_zs[role] - (p.direct_top_fin_base_z if role == p.direct_top_fin_role else p.fin_bases[role]))


def test_optical_functions_derive_short_fins_and_target_shadow_radii():
    assert p.source_z == pytest.approx(40.0)
    assert p.target_tip_radii == pytest.approx((250.0, 300.0, 350.0))
    assert p.fin_tip_zs == pytest.approx((17.904, 21.8, 24.582857142857144))
    assert p.fin_heights == pytest.approx((15.104, 15.600000000000001, 12.182857142857145))
    assert p.projected_base_radii == pytest.approx((161.5204678363, 177.2727272727, 196.9343065693), abs=1e-8)
    assert p.projected_shadow_lengths == pytest.approx((88.4795321637, 122.7272727273, 153.0656934307), abs=1e-8)
    assert p.shadow_occlusion_top_zs == pytest.approx((5.8, 9.2, 12.6))
    for role, target in enumerate(p.target_tip_radii):
        assert p.projected_radius(p.fin_lane_centers[role], p.fin_tip_zs[role]) == pytest.approx(target)
        assert p.fin_tip_zs[role] < p.source_z
    assert p.led_nearest_tip_gap == pytest.approx(15.4171428571)


def test_primary_visualization_compounds_are_valid_and_center_remains_free():
    assembly = g.make_assembled()
    assert assembly.is_valid and len(assembly.children) == 31 and len(assembly.solids()) == 31
    assert assembly.bounding_box().min.Z == pytest.approx(-25.5)
    assert assembly.bounding_box().max.Z == pytest.approx(24.5828571429)
    assert g.make_axial_side_section().is_valid
    assert g.make_transmission_exploded().is_valid
    assert g.make_fins_rings_closeup().is_valid


def _bounding_boxes_have_positive_overlap(a, b, tolerance=1e-8):
    first, second = a.bounding_box(), b.bounding_box()
    return all(
        getattr(first.min, axis) < getattr(second.max, axis) - tolerance
        and getattr(second.min, axis) < getattr(first.max, axis) - tolerance
        for axis in "XYZ"
    )


def test_exhaustive_assembled_occurrence_pairs_have_zero_positive_volume_overlap():
    children = list(g.make_assembled().children)
    assert len(children) == 31
    # Empty allowlist by design: fused roots/fins are contained within their
    # carrier occurrence, while every distinct assembly occurrence is disjoint.
    positive_collision_allowlist = set()
    checked = 0
    for first_index, first in enumerate(children):
        for second_index in range(first_index + 1, len(children)):
            second = children[second_index]
            if not _bounding_boxes_have_positive_overlap(first, second):
                continue
            checked += 1
            pair = frozenset((first.label, second.label))
            volume = g.positive_intersection_volume(first, second)
            if pair not in positive_collision_allowlist:
                assert volume <= 1e-6, (first.label, second.label, volume)
    assert checked >= 70


@pytest.mark.parametrize("name,_factory", g.PRIMARY_FACTORIES)
def test_generated_step_wrappers_are_valid(name, _factory):
    path = MODEL_ROOT / f"p3_v3_{name}.step"
    shape = import_step(path)
    assert shape.is_valid
    assert BRepCheck_Analyzer(shape.wrapped).IsValid()
    assert shape.volume > 0.0


def test_gear_coupon_3mf_is_two_named_bed_fitting_objects_and_gates_are_pending():
    path = MODEL_ROOT / "print" / "p3_v3_m1_259T_12T_mesh_coupon.3mf"
    with ZipFile(path) as package:
        assert package.testzip() is None
        xml = package.read("3D/3dmodel.model")
    root = ElementTree.fromstring(xml)
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objects = root.findall(".//m:object", ns)
    items = root.findall(".//m:build/m:item", ns)
    assert len(objects) == len(items) == 2
    assert {obj.attrib["name"] for obj in objects} == {
        "p3_v3_coupon_259T_internal_gear_segment",
        "p3_v3_coupon_12T_pinion",
    }
    manifest = json.loads((MODEL_ROOT / "print" / "p3_v3_manifest.json").read_text())
    assert set(manifest["physical_gates"].values()) == {"PENDING"}
    assert "not printable tooth geometry" in manifest["warning"]
