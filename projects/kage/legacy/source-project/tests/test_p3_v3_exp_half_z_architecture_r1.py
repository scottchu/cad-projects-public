"""Meaningful repair gates for the isolated KAGE half-Z D candidate."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from build123d import import_step

from p3_v3_exp_half_z_architecture_r1_export import export_all
from p3_v3_exp_half_z_architecture_r1_geometry import (
    _bounds,
    locked_step_sha256,
    make_D_complete,
    make_D_exploded,
    make_D_led_keepout_reference,
)
from p3_v3_exp_half_z_architecture_r1_spec import P3_V3_EXP_HALF_Z_ARCHITECTURE_R1 as P


def _children_with(shape, text: str):
    return [child for child in shape.children if text in (child.label or "")]


def _one(shape, text: str):
    rows = _children_with(shape, text)
    assert len(rows) == 1, (text, [row.label for row in rows])
    return rows[0]


def _intersection_volume(a, b) -> float:
    common = a.intersect(b)
    return 0.0 if not common else sum(solid.volume for solid in common.solids())


@pytest.fixture(scope="module")
def d_complete():
    return make_D_complete()


@pytest.fixture(scope="module")
def written():
    return export_all()


def test_locked_authority_hash_and_namespace_are_unchanged():
    assert locked_step_sha256() == P.locked_step_sha256
    assert P.model_root != P.locked_step.parent
    assert P.model_root.name == "p3_v3_exp_half_z_architecture_r1"
    assert P.model_root.name != "p3_v3_exp_low_z_drive_comparison_r0"


def test_D_numeric_stack_and_honest_depth_contract():
    assert P.d_carrier_layers == ((0.80, 3.45), (3.80, 6.45), (6.80, 9.45))
    assert [P.d_carrier_layers[i + 1][0] - P.d_carrier_layers[i][1] for i in range(2)] == pytest.approx([0.35, 0.35])
    assert P.d_motor_center_z == pytest.approx(-8.35)
    assert P.d_miter_translation_z == pytest.approx(3.65)
    assert P.d_actual_z_envelope == pytest.approx(31.846)
    assert P.d_actual_z_envelope <= 32.0


def test_D_complete_inventory_and_actual_bbox(d_complete):
    assert d_complete.label.startswith("D_REPAIRED_COMPLETE")
    assert len(_children_with(d_complete, "carrier_with_integral_fin")) == 3
    assert len(_children_with(d_complete, "positive_drive_pinion")) == 3
    assert len(_children_with(d_complete, "NEMA8_20p3x39p3_PURCHASED_ENVELOPE")) == 3
    assert len(_children_with(d_complete, "REAL_16T_straight_miter")) == 6
    assert len(_children_with(d_complete, "positive_serviceable_U_cradle")) == 3
    assert len(_children_with(d_complete, "NEMA8_face_M2_fastener")) == 12
    assert len(_children_with(d_complete, "cradle_chassis_M3_fastener")) == 6
    assert len(_children_with(d_complete, "post_with_rear_stop_collar")) == 3
    assert len(_children_with(d_complete, "independent_flanged_spool")) == 9
    assert len(_children_with(d_complete, "removable_keeper_cap")) == 3
    assert _bounds(d_complete) == pytest.approx((-150, -150, -19.2, 150, 150, 12.646), abs=1e-6)


def test_three_ring_pinion_meshes_share_pitch_and_active_face_planes(d_complete):
    for role_index, role in enumerate(P.roles):
        carrier = _one(d_complete, f"D_{role}_complete_M1_260T_carrier")
        pinion = _one(d_complete, f"D_{role}_real_M1_16T_positive_drive_pinion")
        assert P.d_ring_pitch_radius - P.d_pinion_axes[role_index] == pytest.approx(P.pinion_pitch_radius)
        face_z0, face_z1 = P.d_pinion_face_range(role_index)
        assert carrier.bounding_box().min.Z == pytest.approx(P.d_carrier_layers[role_index][0])
        assert pinion.bounding_box().min.Z == pytest.approx(P.d_carrier_layers[role_index][0])
        assert pinion.bounding_box().max.Z == pytest.approx(P.d_carrier_layers[role_index][1])
        assert face_z0 - P.d_carrier_layers[role_index][0] == pytest.approx(P.d_tooth_free_race_depth)
        assert face_z1 == pytest.approx(P.d_carrier_layers[role_index][1])
        assert _intersection_volume(carrier, pinion) <= 1e-6


def test_real_miter_teeth_mesh_at_actual_motor_center(d_complete):
    assert not _children_with(d_complete, "LAYOUT_REFERENCE_NOT_TEETH")
    for role in P.roles:
        horizontal = _one(d_complete, f"D_{role}_REAL_16T_straight_miter_horizontal")
        vertical = _one(d_complete, f"D_{role}_REAL_16T_straight_miter_vertical")
        assert len(horizontal.faces()) > 80
        assert len(vertical.faces()) > 80
        assert horizontal.bounding_box().min.Z < P.d_motor_center_z < horizontal.bounding_box().max.Z
        assert vertical.bounding_box().max.Z > P.d_motor_center_z
        assert _intersection_volume(horizontal, vertical) <= 1e-6


def test_critical_pairwise_clearances_are_positive(d_complete):
    carriers = [_one(d_complete, f"D_{role}_complete") for role in P.roles]
    assert _intersection_volume(carriers[0], carriers[1]) <= 1e-6
    assert _intersection_volume(carriers[1], carriers[2]) <= 1e-6
    for role_index, role in enumerate(P.roles):
        motor = _one(d_complete, f"D_{role}_NEMA8_20p3x39p3_PURCHASED_ENVELOPE")
        cradle = _one(d_complete, f"D_{role}_positive_serviceable_U_cradle")
        assert _intersection_volume(motor, cradle) <= 1e-6
        assert _intersection_volume(carriers[role_index], cradle) <= 1e-6
        for spool in _children_with(d_complete, f"_{role}_independent_flanged_spool"):
            assert _intersection_volume(carriers[role_index], spool) <= 1e-6


def test_guides_are_chassis_anchored_relieved_and_axially_captured(d_complete):
    chassis = _one(d_complete, "D_300mm_OD_6mm_chassis")
    assert P.d_guide_spool_bore_diameter - P.d_guide_shaft_diameter == pytest.approx(0.20)
    assert P.d_guide_rear_counterbore_diameter - P.d_guide_rear_collar_diameter == pytest.approx(0.20)
    assert P.d_guide_rear_counterbore_z[1] == pytest.approx(P.d_guide_rear_collar_z[1])
    assert P.d_guide_axis_radius + P.d_guide_running_diameter / 2.0 == pytest.approx(131.55)
    assert P.d_carrier_race_radius - 131.55 == pytest.approx(0.05)
    assert P.d_guide_axis_radius + P.d_guide_hub_diameter / 2.0 == pytest.approx(128.50)
    assert P.d_tooth_tip_radius - 128.50 == pytest.approx(0.50)
    for tower in range(1, 4):
        post = _one(d_complete, f"guide_tower_{tower}_D4_post_with_rear_stop_collar")
        cap = _one(d_complete, f"guide_tower_{tower}_removable_keeper_cap")
        grub = _one(d_complete, f"guide_tower_{tower}_M2_boss_grub_screw")
        spools = [
            part for part in _children_with(d_complete, f"guide_tower_{tower}_")
            if "independent_flanged_spool" in (part.label or "")
        ]
        assert post.bounding_box().min.Z <= P.plate_z[0] + 0.8
        assert post.bounding_box().max.Z == pytest.approx(P.d_guide_shaft_z[1])
        assert cap.bounding_box().min.Z == pytest.approx(post.bounding_box().max.Z)
        assert grub.bounding_box().min.Z < P.d_guide_chassis_boss_z[1]
        assert len(spools) == 3
        assert _intersection_volume(post, chassis) <= 1e-6
        for role_index, spool in enumerate(spools):
            z0, z1 = P.d_carrier_layers[role_index]
            assert spool.bounding_box().min.Z < z0
            assert spool.bounding_box().max.Z > z1
            assert _intersection_volume(post, spool) <= 1e-6


def test_motor_shafts_are_coaxial_and_fastened_to_serviceable_cradles(d_complete):
    for role in P.roles:
        motor = _one(d_complete, f"D_{role}_NEMA8_20p3x39p3_PURCHASED_ENVELOPE")
        horizontal = _one(d_complete, f"D_{role}_horizontal_motor_shaft")
        output = _one(d_complete, f"D_{role}_vertical_output_shaft")
        face_fasteners = _children_with(d_complete, f"D_{role}_NEMA8_face_M2_fastener")
        chassis_fasteners = _children_with(d_complete, f"D_{role}_cradle_chassis_M3_fastener")
        assert (horizontal.bounding_box().min.Z + horizontal.bounding_box().max.Z) / 2.0 == pytest.approx(P.d_motor_center_z)
        assert motor.bounding_box().min.Z == pytest.approx(P.d_motor_z[0])
        assert motor.bounding_box().max.Z == pytest.approx(P.d_motor_z[1])
        assert output.bounding_box().min.Z == pytest.approx(P.d_motor_z[0])
        assert len(face_fasteners) == 4
        assert len(chassis_fasteners) == 2
        assert all(max(f.bounding_box().size.X, f.bounding_box().size.Y) > P.motor_face_thread_depth for f in face_fasteners)
        assert all(f.bounding_box().min.Z <= P.plate_z[0] for f in chassis_fasteners)


def test_exploded_state_is_true_installation_order_and_service_separated(d_complete):
    exploded = make_D_exploded()
    assert exploded.label == "D_TRUE_EXPLODED_INSTALLATION_ORDER"
    assert len(exploded.children) == len(d_complete.children)
    labels = [child.label or "" for child in exploded.children]
    assert any("INSTALL_ORDER_dz_-28.0_D_hour_NEMA8" in label for label in labels)
    assert any("INSTALL_ORDER_dz_+28.0_D_hour_complete" in label for label in labels)
    assert any("INSTALL_ORDER_dz_+66.0_D_shared_guide_tower_1_removable_keeper" in label for label in labels)
    assert exploded.bounding_box().size.Z > d_complete.bounding_box().size.Z + 50.0


def test_led_keepout_is_separate_clear_and_center_remains_open(d_complete):
    keepout = make_D_led_keepout_reference().children[0]
    assert "REFERENCE_ONLY" in (keepout.label or "")
    assert not _children_with(d_complete, "LED_OPTICAL_KEEP_OUT")
    assert P.d_plate_inner_radius - P.d_led_keepout_bottom_radius == pytest.approx(5.0)
    for physical in d_complete.children:
        assert _intersection_volume(keepout, physical) <= 1e-6, physical.label
    assert P.d_optical_clearance_risk == pytest.approx(8.10)


def test_written_steps_and_manifest_match_repaired_claims(written):
    primary = import_step(str(written["D_compact_split_plane_complete.step"]))
    assert primary.bounding_box().size.Z == pytest.approx(31.846, abs=1e-6)
    assert primary.bounding_box().size.Z <= 32.0
    assert len(primary.solids()) >= 65

    exploded = import_step(str(written["D_true_exploded_installation_order.step"]))
    section = import_step(str(written["D_true_side_section.step"]))
    keepout = import_step(str(written["D_LED_keepout_reference_not_hardware.step"]))
    assert exploded.bounding_box().size.Z > primary.bounding_box().size.Z + 50.0
    assert section.bounding_box().size.Y <= 18.000001
    assert section.volume < primary.volume
    assert keepout.bounding_box().min.Z == pytest.approx(0.0)
    assert keepout.bounding_box().max.Z == pytest.approx(P.d_led_keepout_top_z)

    manifest = json.loads(Path(written["manifest.json"]).read_text())
    assert manifest["locked_sha256"] == P.locked_step_sha256
    assert manifest["architectures"]["D"]["claim"].startswith("repaired_complete")
    assert manifest["architectures"]["D"]["miter_geometry"].startswith("real_16T")
    assert manifest["architectures"]["E"]["status"] == "REJECTED_COMPARISON_LAYOUT_ONLY"
    assert manifest["LED_keepout"]["included_in_primary_physical_envelope"] is False
    assert manifest["artifacts"]["D_compact_split_plane_complete.step"]["scope"] == "primary_complete_candidate"
    assert manifest["artifacts"]["E_REJECTED_coplanar_radial_lanes_comparison.step"]["scope"] == "rejected_comparison"
