from __future__ import annotations

import ast
import gc
import json
from hashlib import sha256
from math import hypot
from pathlib import Path

import pytest
from build123d import Align, Cylinder, Pos

import xt60_bend_jig.p17_r2_direct_counter_twist as p17


ROOT = Path(__file__).parents[1]


@pytest.fixture(autouse=True)
def _release_occ_memory_after_test():
    yield
    p17.clear_geometry_caches()
    gc.collect()


def _labels(shape):
    if not shape.children:
        return [shape.label]
    labels = []
    for child in shape.children:
        labels.extend(_labels(child))
    return labels


def _intersection_volume(first, second) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return float(common.volume)
    return sum(float(item.volume) for item in common)


def _bounds_size(shape) -> tuple[float, float, float]:
    box = shape.bounding_box()
    return (
        float(box.max.X - box.min.X),
        float(box.max.Y - box.min.Y),
        float(box.max.Z - box.min.Z),
    )


def _x_cylinder(diameter: float, length: float, x: float = 0.0):
    return Pos(x, 0.0, 0.0) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def test_contract_hash_and_core_dimensions_do_not_regress() -> None:
    contract = ROOT / p17.P17_R2_DESIGN_CONTRACT_PATH
    assert sha256(contract.read_bytes()).hexdigest() == p17.P17_R2_DESIGN_CONTRACT_SHA256

    p = p17.P17_R2_DEFAULTS
    assert p.inner_clear_span == pytest.approx(18.40)
    assert p.inner_clear_span < 26.2
    assert p.principal_stack_width == pytest.approx(32.00)
    assert p.rod_length_raw == pytest.approx(40.60)
    assert p.rod_length_target == pytest.approx(40.60)
    assert p.rod_length_target != pytest.approx(50.00)
    assert p.center_axle_total_length == pytest.approx(34.90)
    assert p.cap_socket_id == pytest.approx(4.04)
    assert p.cap_socket_id >= p.rod_diameter
    assert p.right_primary_extra_lever_radius == pytest.approx(1.50)
    assert p.inner_plate_diameter == pytest.approx(54.00)
    assert p.left_outer_secondary_grip_diameter == pytest.approx(60.00)
    assert p.right_outer_primary_grip_diameter == pytest.approx(63.00)


def test_outer_plates_counter_rotate_and_inner_plate_positions_are_fixed() -> None:
    assert p17.alpha_left(12.5) == pytest.approx(-12.5)
    assert p17.alpha_right(12.5) == pytest.approx(12.5)
    assert p17.rotation_for_side("left", 20.0) + p17.rotation_for_side("right", 20.0) == pytest.approx(0.0)

    p = p17.P17_R2_DEFAULTS
    assert p.left_inner_x == pytest.approx(-10.80)
    assert p.right_inner_x == pytest.approx(10.80)
    assert p.left_outer_x == pytest.approx(-14.40)
    assert p.right_outer_x == pytest.approx(14.40)


def test_fixed_guide_loci_are_state_independent_and_outer_slots_are_part_local() -> None:
    fixed_before = {name: p17.fixed_guide_locus(name) for name in p17.ROD_NAMES}
    for theta in (0.0, 8.0, 16.0, 24.0, p17.P17_R2_DEFAULTS.theta_lock_deg):
        assert {name: p17.fixed_guide_locus(name) for name in p17.ROD_NAMES} == fixed_before
        for name in p17.ROD_NAMES:
            left_local = p17.outer_slot_local_center("left", name, theta)
            right_local = p17.outer_slot_local_center("right", name, theta)
            world = p17.rod_center(name, theta)
            assert p17.reconstruct_world_from_outer("left", name, theta).as_tuple() == pytest.approx(world.as_tuple())
            assert p17.reconstruct_world_from_outer("right", name, theta).as_tuple() == pytest.approx(world.as_tuple())
            if theta:
                assert left_local.as_tuple() != pytest.approx(world.as_tuple())
                assert right_local.as_tuple() != pytest.approx(world.as_tuple())


def test_left_and_right_rod_end_reconstruction_has_zero_yz_skew() -> None:
    for theta in (0.0, 4.0, 16.0, 28.0, p17.P17_R2_DEFAULTS.theta_lock_deg):
        for name in p17.ROD_NAMES:
            left = p17.reconstruct_world_from_outer("left", name, theta)
            right = p17.reconstruct_world_from_outer("right", name, theta)
            assert left.distance_to(right) <= 1.0e-9
            assert left.as_tuple() == pytest.approx(p17.rod_center(name, theta).as_tuple(), abs=1.0e-9)


def test_one_piece_stepped_center_axle_and_keepers_replace_yoke_bars() -> None:
    assembly = p17.build_motion_state("locked")
    labels = _labels(assembly)
    assert any("stepped_center_axle_one_piece_hex_spacer_hex_keys_round_journals" in label for label in labels)
    assert len([label for label in labels if "press_fit_outer_keeper" in label]) == 2
    forbidden = ("yoke", "stability_bar", "tenon", "shared_D_shaft", "same_direction", "simulator", "animation", "threejs")
    production_labels = [label for label in labels if not label.startswith("reference_")]
    assert not [
        label
        for label in production_labels
        for word in forbidden
        if word.lower() in label.lower()
    ]


def test_center_axle_parameters_ground_inner_only_and_outer_journals_are_round_clearance() -> None:
    p = p17.P17_R2_DEFAULTS
    assert p.center_axle_central_hex_af == pytest.approx(10.00)
    assert p.center_axle_inner_hex_af == pytest.approx(8.00)
    assert p.inner_hex_bore_af == pytest.approx(8.15)
    assert p.outer_journal_diameter == pytest.approx(7.60)
    assert p.outer_bearing_bore_diameter == pytest.approx(7.90)
    assert p.outer_bearing_bore_diameter > p.outer_journal_diameter
    assert p.outer_journal_diameter < p.inner_hex_bore_af
    assert p.inner_hex_bore_web >= p.min_web_mm
    assert p.outer_bearing_wall >= p.min_web_mm
    assert p.journal_outer_plate_overlap >= 2.40
    assert p.keeper_axial_running_clearance == pytest.approx(0.25)
    assert p.keeper_seat_length == pytest.approx(1.20)
    assert p.per_side_center_axle_length == pytest.approx(8.25)
    assert p.journal_with_keeper_seat_length == pytest.approx(5.05)
    assert p.keeper_bore_diameter < p.outer_journal_diameter
    assert p.keeper_outer_diameter == pytest.approx(10.00)
    assert p.keeper_bore_diameter == pytest.approx(7.55)
    assert p.keeper_radial_wall_min == pytest.approx(1.225)
    assert p.keeper_radial_wall_min >= 1.20

    axle = p17.build_center_axle(p)
    left_outer = p17.build_outer_plate("left", 0.0, p)
    right_outer = p17.build_outer_plate("right", 0.0, p)
    assert _intersection_volume(axle, left_outer) <= 1.0e-7
    assert _intersection_volume(axle, right_outer) <= 1.0e-7


def test_center_axle_full_journal_spans_and_keeper_retention_are_not_floating() -> None:
    p = p17.P17_R2_DEFAULTS
    assert -p.center_axle_total_length / 2.0 == pytest.approx(-17.45)
    assert p.center_axle_total_length / 2.0 == pytest.approx(17.45)
    assert p.keeper_left_x == pytest.approx(-16.85)
    assert p.keeper_right_x == pytest.approx(16.85)
    assert p.left_outer_x - p.outer_plate_thickness / 2.0 == pytest.approx(-16.00)
    assert p.right_outer_x + p.outer_plate_thickness / 2.0 == pytest.approx(16.00)
    assert abs(p.keeper_left_x + p.outer_keeper_thickness / 2.0) - 16.0 == pytest.approx(0.25)
    assert p.keeper_right_x - p.outer_keeper_thickness / 2.0 - 16.0 == pytest.approx(0.25)

    axle = p17.build_center_axle(p)
    for side in ("left", "right"):
        keeper = p17.build_keeper(side, p)
        # A permanent press-fit keeper intentionally intersects the modeled
        # journal end seat in CAD; physical install force is a coupon gate.
        assert _intersection_volume(axle, keeper) > 0.01

    coupon_labels = _labels(p17.build_center_axle_coupon(p))
    for bore in p.keeper_coupon_bore_diameters:
        assert any(
            f"coupon_keeper_OD10p00_bore_{bore:.2f}".replace(".", "p") == label
            for label in coupon_labels
        )


def test_center_axle_clears_reference_xt60_and_wire_envelopes() -> None:
    p = p17.P17_R2_DEFAULTS
    axle = p17.build_center_axle(p)
    assert _intersection_volume(axle, p17.build_xt60_reference(p)) <= 1.0e-7
    for theta in (0.0, 16.0, p.theta_lock_deg):
        assert _intersection_volume(axle, p17.build_workpiece_reference(theta, p)) <= 1.0e-7


def test_six_caps_are_permanent_and_cap_coupon_contains_ladder() -> None:
    assembly = p17.build_motion_state("locked")
    labels = _labels(assembly)
    cap_labels = [label for label in labels if "permanent_follower_cap" in label]
    assert len(cap_labels) == 6
    assert all("permanent" in label for label in cap_labels)
    assert not any("removable" in label.lower() or "service_cap" in label.lower() for label in labels)

    coupon_labels = _labels(p17.build_permanent_cap_coupon())
    for diameter in p17.P17_R2_DEFAULTS.cap_socket_ladder_ids:
        assert any(f"ID{diameter:.2f}".replace(".", "p") in label for label in coupon_labels)
    for depth in p17.P17_R2_DEFAULTS.cap_socket_ladder_depths:
        assert any(f"depth{depth:.2f}".replace(".", "p") in label for label in coupon_labels)


def test_permanent_cap_socket_is_one_sided_blind_geometry() -> None:
    p = p17.P17_R2_DEFAULTS
    cap = p17._cap_local(p, socket_open_side=1)
    open_probe = _x_cylinder(p.cap_socket_id * 0.80, 0.20, p.follower_head_length / 2.0 - 0.05)
    closed_probe = _x_cylinder(p.cap_socket_id * 0.80, 0.20, -p.follower_head_length / 2.0 + p.cap_closed_end_wall / 2.0)
    assert _intersection_volume(cap, open_probe) <= 1.0e-7
    assert _intersection_volume(cap, closed_probe) > 0.1
    assert p.cap_rod_engagement + p.cap_closed_end_wall <= p.follower_head_length


def test_print_kit_uses_flat_local_plate_occurrences_and_includes_axle_parts() -> None:
    kit = p17.build_print_kit()
    labels = [child.label for child in kit.children]
    plate_z_sizes = {
        child.label: _bounds_size(child)[2]
        for child in kit.children
        if child.label.startswith("print_left_inner")
        or child.label.startswith("print_right_inner")
        or child.label.startswith("print_left_outer")
        or child.label.startswith("print_right_outer")
    }
    assert len(plate_z_sizes) == 4
    assert max(value for label, value in plate_z_sizes.items() if "right_inner" not in label) <= 5.01
    # The right-inner receiver's 8.6 mm axial bridge is the named grounded
    # lock load path, not nonfunctional rail bulk.
    assert next(value for label, value in plate_z_sizes.items() if "right_inner" in label) <= 8.61
    assert len([label for label in labels if label.endswith("_permanent_cap")]) == 6
    assert any("print_stepped_center_axle" in label for label in labels)
    assert len([label for label in labels if "press_fit_outer_keeper" in label]) == 2
    axle_z = [
        _bounds_size(child)[2]
        for child in kit.children
        if child.label.startswith("print_stepped_center_axle")
    ]
    assert axle_z and max(axle_z) <= 11.0


def test_lock_has_same_solid_one_way_flexure_capture_release_and_no_self_lock_claim() -> None:
    labels = _labels(p17.build_motion_state("locked"))
    assert any("completed_pigtail_window_and_receiver" in label for label in labels)
    assert any("right_outer_primary_actuator_larger_integrated_lock_nose" in label for label in labels)

    p = p17.P17_R2_DEFAULTS
    assert p.lock_nose_orbit_radius + p.lock_nose_radius <= p.right_outer_primary_grip_diameter / 2.0 + p.min_web_mm
    assert p.lock_nose_axial_thickness >= 1.00
    assert p.lock_over_center_capture == pytest.approx(0.40)
    assert p17.lock_contact_gap_y(0.0, p) > 10.0
    assert p17.lock_contact_gap_y(16.0, p) > 7.0
    assert p17.lock_contact_gap_y(p.theta_lock_deg, p) == pytest.approx(0.02)
    assert p17.lock_contact_gap_y(p.theta_lock_deg + 1.0, p) < 0.0

    receiver = p17.build_lock_receiver(p, condition="seated")
    assert _intersection_volume(receiver, p17.build_outer_plate("right", 0.0, p)) <= 1.0e-7
    assert _intersection_volume(receiver, p17.build_outer_plate("right", 16.0, p)) <= 1.0e-7
    assert _intersection_volume(receiver, p17.build_outer_plate("right", p.theta_lock_deg, p)) <= 1.0e-7

    evidence = p17.lock_backdrive_evidence()
    assert evidence["claimBoundary"].startswith("CAD receiver-pocket/contact proof only")
    assert evidence["rightLockContactGapY"] == pytest.approx(0.02)
    solids = evidence["solidLockChecks"]
    assert solids["lockedHardStopIntersectionMm3"] <= 1.0e-7
    assert solids["overclosedHardStopIntersectionMm3"] > 0.01
    assert solids["lockedShoulderIntersectionMm3"] <= 1.0e-7
    assert solids["opening1degShoulderIntersectionMm3"] > 0.01
    assert solids["opening2degShoulderIntersectionMm3"] > solids["opening1degShoulderIntersectionMm3"]
    assert solids["releasedOpening2degShoulderIntersectionMm3"] <= 1.0e-7
    assert solids["overclosedNonHardStopIntersectionMm3"] <= 1.0e-7
    assert solids["overCenterCaptureMm"] == pytest.approx(0.40)
    assert max(row["receiverIntersectionMm3"] for row in evidence["normalClosingSweep"].values()) <= 1.0e-7
    assert min(row["catchClearanceMm"] for row in evidence["normalClosingSweep"].values()) >= 0.20
    assert max(row["receiverIntersectionMm3"] for row in evidence["releasedOpeningSweep"].values()) <= 1.0e-7
    assert min(row["catchClearanceMm"] for row in evidence["releasedOpeningSweep"].values()) >= 0.20
    assert evidence["sameReceiverOccurrence"]["connectedSolidCountSeated"] == 1
    assert evidence["sameReceiverOccurrence"]["connectedSolidCountClosing"] == 1
    assert evidence["sameReceiverOccurrence"]["connectedSolidCountReleased"] == 1
    for row in evidence["rodChecks"].values():
        assert hypot(*row["slotTangent"]) == pytest.approx(1.0)


def test_source_does_not_define_world_space_only_outer_slots_or_p17_sidecar() -> None:
    source = Path(p17.__file__).read_text()
    tree = ast.parse(source)
    function_names = [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert "outer_slot_local_center" in function_names
    assert "reconstruct_world_from_outer" in function_names
    assert "build_simulator" not in function_names
    assert "build_animation" not in function_names
    assert "Three" not in source
    assert "50.00" not in source
    assert "ID3.90" not in source


def test_source_export_entrypoints_exist_for_primary_p17_r2_artifacts() -> None:
    cad = ROOT / "cad" / "p17_r2_direct_counter_twist"
    for name in (
        "p17_r2_open",
        "p17_r2_mid",
        "p17_r2_locked",
        "p17_r2_exploded",
        "p17_r2_print_kit",
        "p17_r2_permanent_cap_coupon",
        "p17_r2_center_axle_coupon",
        "p17_r2_lock_closeup",
    ):
        assert (cad / f"{name}.step.py").exists()
        assert f'build_artifact("{name.removeprefix("p17_r2_")}"' in (cad / f"{name}.step.py").read_text()


def test_d04_offset_shared_pivot_drives_axle_plates_and_complementary_slot_reconstruction() -> None:
    p = p17.P17_R2_DEFAULTS
    pivot = p17.pivot_yz(p)
    assert pivot.as_tuple() == pytest.approx((-10.60, 17.00))
    assert pivot.y < -p.xt60_body_y / 2.0
    assert p.fixed_slot_width == pytest.approx(4.20)
    assert p.outer_slot_width == pytest.approx(4.20)
    assert p.slot_center_slop_nominal == pytest.approx(0.10)
    assert p17.GUIDES["upright"].open.as_tuple() == pytest.approx((-12.0, 3.0))
    assert p17.GUIDES["upright"].locked.as_tuple() == pytest.approx((-18.0, 13.0))
    assert p17.GUIDES["bottom"].open.as_tuple() == pytest.approx((-5.0, -12.0))
    assert p17.GUIDES["bottom"].locked.as_tuple() == pytest.approx((8.0, -12.0))
    assert p17.GUIDES["diagonal"].open.as_tuple() == pytest.approx((11.5, 9.0))
    assert p17.GUIDES["diagonal"].locked.as_tuple() == pytest.approx((3.0, 1.0))
    for theta in (0.0, 8.0, 16.0, 24.0, p.theta_lock_deg):
        for name in p17.ROD_NAMES:
            reconstructed = p17.reconstruct_world_from_outer("left", name, theta, p)
            assert reconstructed.distance_to(p17.rod_center(name, theta, p)) < 0.05


def test_d04_actual_sweep_has_no_axle_or_keeper_contact_with_rods_or_caps() -> None:
    p = p17.P17_R2_DEFAULTS
    for theta in tuple(index * p.theta_lock_deg / 8.0 for index in range(9)):
        axle = p17.build_center_axle(p)
        for name in p17.ROD_NAMES:
            assert _intersection_volume(axle, p17.build_rod(name, theta, p)) <= 1.0e-7
            for side in ("left", "right"):
                assert _intersection_volume(p17.build_keeper(side, p), p17.build_cap(side, name, theta, p)) <= 1.0e-7


def test_d04_actual_sweep_rods_and_caps_do_not_cross_xt60_body() -> None:
    p = p17.P17_R2_DEFAULTS
    body = p17.build_xt60_reference(p)
    for theta in tuple(index * p.theta_lock_deg / 8.0 for index in range(9)):
        for name in p17.ROD_NAMES:
            assert _intersection_volume(p17.build_rod(name, theta, p), body) <= 1.0e-7
            for side in ("left", "right"):
                assert _intersection_volume(p17.build_cap(side, name, theta, p), body) <= 1.0e-7


def test_d04_actual_sweep_rods_and_caps_clear_all_nonowning_mechanism_solids() -> None:
    p = p17.P17_R2_DEFAULTS
    for theta in tuple(index * p.theta_lock_deg / 8.0 for index in range(9)):
        solids = {
            "axle": p17.build_center_axle(p),
            "left_keeper": p17.build_keeper("left", p),
            "right_keeper": p17.build_keeper("right", p),
            "left_inner": p17.build_inner_plate("left", p),
            "right_inner": p17.build_inner_plate("right", p),
            "left_outer": p17.build_outer_plate("left", theta, p),
            "right_outer": p17.build_outer_plate("right", theta, p),
        }
        for name in p17.ROD_NAMES:
            rod = p17.build_rod(name, theta, p)
            assert all(_intersection_volume(rod, solid) <= 1.0e-7 for solid in solids.values())
            for side in ("left", "right"):
                cap = p17.build_cap(side, name, theta, p)
                assert all(_intersection_volume(cap, solid) <= 1.0e-7 for solid in solids.values())


def test_d04_service_envelopes_have_actual_solid_clearance_above_target() -> None:
    evidence = p17.service_clearance_evidence()
    assert evidence["minimumRequiredMm"] == pytest.approx(0.75)
    assert evidence["minimumActualMm"] >= evidence["minimumRequiredMm"]
    assert evidence["passes"] is True
    assert all(row["zeroIntersection"] is True for row in evidence["rows"].values())
    assert evidence["removalSequence"] == "release -> full open -> lift to window centerline -> +Y extraction"
    assert evidence["removalZeroIntersection"] is True
    assert evidence["removalMinimumActualMm"] >= evidence["minimumRequiredMm"]
    assert evidence["removalWaypointsYZ"] == pytest.approx(
        [(0.0, 21.0), (0.0, 22.5), (8.0, 22.5), (20.0, 22.5), (34.0, 22.5)]
    )


def test_d05_fixed_inner_service_windows_are_real_through_cuts() -> None:
    p = p17.P17_R2_DEFAULTS
    assert p.completed_pigtail_window_start_y == pytest.approx(4.50)
    assert p.completed_pigtail_window_center_z == pytest.approx(22.50)
    assert p.completed_pigtail_window_width_z == pytest.approx(8.00)
    for side in ("left", "right"):
        plate = p17.build_inner_plate(side, p)
        x = p.left_inner_x if side == "left" else p.right_inner_x
        probe = Pos(x, 9.0, p.completed_pigtail_window_center_z) * Cylinder(
            1.0,
            p.inner_plate_thickness + 1.0,
            rotation=(0.0, 90.0, 0.0),
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        assert _intersection_volume(plate, probe) <= 1.0e-7


def test_d05_pivot_intent_is_yz_behind_body_not_impossible_full_axle_x_shadow() -> None:
    p = p17.P17_R2_DEFAULTS
    manifest = p17.p17_r2_manifest(p)
    assert p.pivot_y < p.xt60_body_center_y - p.xt60_body_y / 2.0
    assert abs(p.pivot_z - p.xt60_body_center_z) <= p.xt60_body_z / 2.0
    assert manifest["pivotIntent"]["behindXt60OnMinusY"] is True
    assert manifest["pivotIntent"]["fullAxleXShadowRequired"] is False


def test_d04_slot_fit_coupon_contains_straight_and_curved_ladders() -> None:
    p = p17.P17_R2_DEFAULTS
    labels = _labels(p17.build_slot_fit_coupon(p))
    for width in p.slot_fit_coupon_widths:
        token = f"{width:.2f}".replace(".", "p")
        assert any(f"slot_fit_straight_OD4_width_{token}" == label for label in labels)
        assert any(f"slot_fit_curved_OD4_width_{token}" == label for label in labels)


def test_d04_rejected_slot_widths_and_straight_cam_shortcut_are_absent() -> None:
    source = Path(p17.__file__).read_text()
    assert "fixed_slot_width: float = 4.90" not in source
    assert "outer_slot_width: float = 7.55" not in source
    assert p17.P17_R2_DEFAULTS.slot_sample_count >= 33
    for side in ("left", "right"):
        for name in p17.ROD_NAMES:
            locus = p17.outer_slot_locus(side, name)
            assert len(locus) == p17.P17_R2_DEFAULTS.slot_sample_count
            chord = locus[0].distance_to(locus[-1])
            polyline = sum(first.distance_to(second) for first, second in zip(locus, locus[1:]))
            assert polyline > chord + 0.01


def _d06_frozen_scope_semantics() -> dict[str, object]:
    """The exact P17-I04 semantics D06 is forbidden to redesign."""
    p = p17.P17_R2_DEFAULTS
    return {
        "guides": {
            name: [p17.GUIDES[name].open.as_tuple(), p17.GUIDES[name].locked.as_tuple()]
            for name in p17.ROD_NAMES
        },
        "white_cam_loci": {
            f"{side}:{name}": [
                [round(point.y, 9), round(point.z, 9)]
                for point in p17.outer_slot_locus(side, name, p)
            ]
            for side in ("left", "right")
            for name in p17.ROD_NAMES
        },
        "rod_cap": {
            name: getattr(p, name)
            for name in (
                "rod_diameter",
                "follower_head_diameter",
                "follower_head_length",
                "cap_closed_end_wall",
                "cap_socket_id",
                "cap_socket_ladder_ids",
                "cap_socket_ladder_depths",
            )
        },
        "lock": {
            name: getattr(p, name)
            for name in (
                "lock_nose_orbit_radius",
                "lock_nose_radius",
                "lock_nose_axial_thickness",
                "lock_contact_clearance",
                "lock_over_center_capture",
                "lock_receiver_stop_depth",
                "lock_receiver_normal_width",
                "lock_receiver_release_shift",
                "lock_receiver_closing_deflection",
                "lock_receiver_bridge_radius",
                "lock_receiver_bridge_diameter",
                "lock_flexure_width",
                "lock_lead_in_length",
                "lock_thumb_tab_length",
                "hard_stop_dwell_deg",
            )
        },
        "axial_stack": {
            name: getattr(p, name)
            for name in (
                "xt60_body_width_x",
                "xt60_side_clearance_each",
                "inner_plate_thickness",
                "outer_plate_thickness",
                "inner_outer_running_gap",
                "cap_to_outer_running_gap",
                "cap_rod_engagement",
                "keeper_seat_length",
                "outer_keeper_thickness",
                "keeper_axial_running_clearance",
            )
        },
        "plates_and_white_slots": {
            name: getattr(p, name)
            for name in (
                "inner_plate_diameter",
                "left_outer_secondary_grip_diameter",
                "right_outer_primary_grip_diameter",
                "fixed_slot_width",
                "outer_slot_width",
                "slot_endpoint_margin",
                "slot_sample_count",
                "theta_lock_deg",
            )
        },
    }


def test_d06_frozen_white_rod_lock_stack_and_plate_semantics_do_not_change() -> None:
    encoded = json.dumps(
        _d06_frozen_scope_semantics(), sort_keys=True, separators=(",", ":")
    ).encode()
    assert sha256(encoded).hexdigest() == (
        "a6c25c8977c2c9debe9838c0c60ee74bb9f28dbe0e1c1a9167c29d9ce594dec5"
    )


def test_d06_fixed_identity_is_purple_axle_and_all_white_rods_remain_moving() -> None:
    manifest = p17.p17_r2_manifest()
    assert manifest["fixedMember"] == "purple printed stepped center axle"
    assert manifest["centerAxle"]["worldInvariant"] is True
    assert manifest["whiteRods"] == {
        "count": 3,
        "color": "white stainless",
        "roles": ("upright", "bottom", "diagonal"),
        "moving": True,
        "fixedReactionMember": False,
    }


def test_d06_split_rotation_and_fixed_axle_datums_are_exact() -> None:
    p = p17.P17_R2_DEFAULTS
    assert p17.outer_rotation_center_yz(p).as_tuple() == pytest.approx((-10.60, 17.00))
    assert p17.fixed_axle_center_yz(p).as_tuple() == pytest.approx((-29.00, 17.00))
    assert p.fixed_axle_eccentricity == pytest.approx(18.40)
    assert p.fixed_axle_guide_slot_width == pytest.approx(7.90)
    assert p.fixed_axle_guide_sample_count >= 33


def test_d06_axle_guides_are_mirrored_constant_radius_and_reconstruct_fixed_world_axle() -> None:
    p = p17.P17_R2_DEFAULTS
    left = p17.fixed_axle_guide_locus("left", p)
    right = p17.fixed_axle_guide_locus("right", p)
    assert len(left) == len(right) == p.fixed_axle_guide_sample_count
    for index, (left_point, right_point) in enumerate(zip(left, right)):
        theta = p.theta_lock_deg * index / (len(left) - 1)
        assert left_point.y == pytest.approx(right_point.y, abs=1.0e-9)
        assert left_point.z == pytest.approx(-right_point.z, abs=1.0e-9)
        assert hypot(left_point.y, left_point.z) == pytest.approx(
            p.fixed_axle_eccentricity, abs=0.05
        )
        for side in ("left", "right"):
            reconstructed = p17.reconstruct_fixed_axle_from_outer(side, theta, p)
            assert reconstructed.as_tuple() == pytest.approx(
                p17.fixed_axle_center_yz(p).as_tuple(), abs=0.05
            )


def test_d06_axle_inner_and_keeper_frames_are_world_invariant_while_outers_counter_rotate() -> None:
    p = p17.P17_R2_DEFAULTS
    evidence = p17.fixed_occurrence_transform_evidence(p)
    assert evidence["fixedOccurrenceNames"] == (
        "stepped_center_axle",
        "left_inner_fixed_guide",
        "right_inner_fixed_guide",
        "left_keeper",
        "right_keeper",
    )
    assert evidence["allFixedWorldInvariant"] is True
    for row in evidence["states"].values():
        assert row["leftOuterAngleDeg"] == pytest.approx(-row["rightOuterAngleDeg"])


def test_d06_actual_solids_keep_axle_in_guides_with_required_web_and_keeper_capture() -> None:
    p = p17.P17_R2_DEFAULTS
    evidence = p17.fixed_axle_actual_solid_evidence(p)
    assert evidence["minimumRequiredWebMm"] == pytest.approx(2.20)
    assert evidence["minimumExactFrozenFeatureGapMm"] == pytest.approx(3.6500, abs=0.001)
    assert evidence["minimumAnalyticWebMm"] == pytest.approx(3.849, abs=0.01)
    assert evidence["minimumActualInnerHexWebMm"] == pytest.approx(3.8946, abs=0.001)
    assert evidence["leftOuterBoundaryWebMm"] == pytest.approx(7.650, abs=0.001)
    assert evidence["rightOuterBoundaryWebMm"] == pytest.approx(9.150, abs=0.001)
    assert evidence["minimumAxleGuideRadialClearanceMm"] == pytest.approx(0.150)
    assert evidence["minimumKeeperRadialCaptureMm"] == pytest.approx(1.050)
    assert evidence["sampleCount"] == 33
    assert evidence["allAxleOuterPlateIntersectionsZero"] is True
    assert evidence["allKeeperOuterPlateIntersectionsZero"] is True
    assert evidence["allAxleGuideProbeIntersectionsZero"] is True
    assert evidence["allAxleWhiteRodIntersectionsZero"] is True
    assert evidence["allKeeperCapIntersectionsZero"] is True
    assert evidence["allXt60AndServiceIntersectionsZero"] is True
    assert evidence["centerAtCHasNoDecorativeHole"] is True


def test_d06_combined_existing_white_rod_contacts_and_axle_guide_close_uniquely() -> None:
    evidence = p17.combined_contact_closure_evidence()
    assert evidence["claimBoundary"].startswith("nominal centerline local-mobility")
    assert evidence["passes"] is True
    assert evidence["sampleCountPerSide"] == 33
    for row in evidence["rows"].values():
        assert row["contactResidualNormMm"] <= 1.0e-6
        assert row["mobilityJacobianRank"] == 3
        assert row["allPerturbedSolvesConvergedToPrescribedPose"] is True
        assert row["maximumPerturbedPoseError"] <= 1.0e-6


def test_d06_motion_entry_is_source_declared_self_contained_and_targets_only_outers() -> None:
    cad = ROOT / "cad" / "p17_r2_direct_counter_twist"
    entry = cad / "p17_r2_fixed_axle_motion.step.py"
    sidecar = cad / "p17_r2_fixed_axle_motion.params.js"
    assert entry.exists()
    assert sidecar.exists()
    assert '"params": "p17_r2_fixed_axle_motion.params.js"' in entry.read_text()
    js = sidecar.read_text()
    assert "open_to_lock" in js
    assert "import " not in js
    assert "effects.transform(\"left_outer\"" in js
    assert "effects.transform(\"right_outer\"" in js
    for forbidden in (
        "stepped_center_axle",
        "left_inner_fixed_guide",
        "right_inner_fixed_guide",
        "left_keeper",
        "right_keeper",
        "upright_rod",
        "bottom_rod",
        "diagonal_rod",
    ):
        assert f'effects.transform("{forbidden}"' not in js
