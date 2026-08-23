from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build123d import Location, import_step
import pytest

from p3_v3_motor_station_assembly_sim_geometry import (
    MODEL_ROOT,
    make_bearing,
    make_bearing_cap_screws,
    make_bearing_radial_cap,
    make_chassis_patch,
    make_chassis_screws,
    make_clamp_collar,
    make_gearbox_frame,
    make_final_station_parts,
    make_grub_screw_references,
    make_gate_install_stage_parts,
    make_miter_pair,
    make_motor_body,
    make_motor_screws,
    make_motor_service_stage_parts,
    make_output_shaft,
    make_ring_mesh_coupon,
    make_role_pinion,
    make_role_spacer,
    make_stage_1_motor_mount,
    make_stage_2_gearbox_mount,
    make_stage_3_shaft_stack,
    make_stage_4_height_lock,
    make_stage_5_reverse_service,
    make_shaft_insertion_swept_volume,
    make_tool_access_references,
)
from p3_v3_motor_station_assembly_sim_spec import (
    P3_V3_MOTOR_STATION_ASSEMBLY_SIM as p,
)


def _intersection_volume(a, b) -> float:
    result = a.intersect(b)
    if result is None:
        return 0.0
    if hasattr(result, "volume"):
        return result.volume
    return sum(shape.volume for shape in result)


def test_fastener_lengths_match_real_interfaces():
    assert p.motor_screw == "ISO 4762 M2x4"
    assert p.motor_thread_engagement == pytest.approx(2.50)
    assert p.motor_thread_engagement >= p.motor_thread_depth_min
    assert p.chassis_screw == "ISO 4762 M3x8"
    assert p.chassis_insert_engagement == pytest.approx(5.00)
    assert p.chassis_insert_engagement >= p.chassis_insert_engagement_min
    assert p.chassis_insert_bottom_margin == pytest.approx(0.50)


def test_role_specific_axial_stack_math():
    assert tuple(p.spacer_length(role) for role in range(3)) == pytest.approx(
        (3.55, 6.95, 10.35)
    )
    expected = ((1.50, 3.90), (7.05, 9.45), (12.60, 15.00))
    for role in range(3):
        assert p.top_collar_z(role) == pytest.approx(expected[role])
    for role in range(3):
        shaft_z0, shaft_z1 = p.shaft_z(role)
        lower_z0, _ = p.lower_collar_z(role)
        _, top_z1 = p.top_collar_z(role)
        assert lower_z0 >= shaft_z0
        assert top_z1 <= shaft_z1 + 1e-9
        assert p.ring_mesh_overlap(role) == pytest.approx(2.10)


def test_output_stack_bores_and_endplay_are_explicit():
    assert "D-shaft" in p.shaft
    assert p.shaft_bore_clearance_diameter - p.parent.output_shaft_diameter == pytest.approx(0.10)
    assert p.spacer_bore_diameter - p.parent.output_shaft_diameter == pytest.approx(0.20)
    assert p.target_axial_endplay == pytest.approx(0.10)
    for role in range(3):
        assert p.lower_bearing_z(role)[0] - p.lower_collar_z(role)[1] == pytest.approx(0.10)
        assert p.top_collar_z(role)[0] - p.parent.pinion_face_ranges[role][1] == pytest.approx(0.10)


def test_all_role_open_yokes_are_one_solid_and_clear_real_rotating_breps_and_motor():
    for role in range(3):
        frame = make_gearbox_frame(role)
        horizontal, vertical = make_miter_pair(role)
        assert len(frame.solids()) == 1
        for moving in (
            make_motor_body(role),
            horizontal,
            vertical,
            make_output_shaft(role),
            make_bearing(role, "lower"),
            make_bearing(role, "upper"),
            make_role_spacer(role),
            make_role_pinion(role),
            make_clamp_collar(role, "lower"),
            make_clamp_collar(role, "top"),
        ):
            assert _intersection_volume(frame, moving) < 1e-5, (role, moving.label)


def test_all_role_exact_r2_pinion_and_ring_coupon_mesh_without_positive_collision():
    for role in range(3):
        pinion = make_role_pinion(role)
        ring = make_ring_mesh_coupon(role)
        assert _intersection_volume(pinion, ring) < 1e-5
        assert pinion.distance_to(ring) < 0.30


def test_all_role_documented_service_stage_tool_axes_are_reachable():
    chassis = make_chassis_patch()
    for role in range(3):
        frame = make_gearbox_frame(role)
        tools = make_tool_access_references(role)
        assert len(make_motor_screws(role)) == 4
        assert len(make_chassis_screws()) == 4
        assert len(tools) == 17
        for tool in tools:
            assert _intersection_volume(tool, frame) < 1e-5, (role, tool.label, "frame")
            assert _intersection_volume(tool, chassis) < 1e-5, (role, tool.label, "chassis")
        # The lower collar is serviced beside, not through, the installed MR84.
        assert _intersection_volume(tools[8], make_bearing(role, "lower")) < 1e-5
        # The motor bevel driver begins outside the actual gear surface.
        horizontal, _ = make_miter_pair(role)
        assert _intersection_volume(tools[12], horizontal) < 1e-5
        # Bearing gates install last and must be removed first.  Once translated
        # to the explicit reverse-service pose, all four motor axes are open.
        removed_caps = [
            make_bearing_radial_cap(role, which).moved(Location((p.service_explode_x, 0.0, 0.0)))
            for which in ("lower", "upper")
        ]
        for motor_tool in tools[:4]:
            for removed_cap in removed_caps:
                assert _intersection_volume(motor_tool, removed_cap) < 1e-5


def test_all_role_staged_tool_access_matches_real_assembly_and_reverse_order():
    for role in range(3):
        tools = make_tool_access_references(role)

        # Gates are fitted before the role ring.  Each driver must therefore
        # clear every non-fastener solid present at that documented stage.
        gate_stage = [
            part
            for part in make_gate_install_stage_parts(role)
            if "screw" not in part.label.lower() and "insert" not in part.label.lower()
        ]
        for gate_tool in tools[13:17]:
            for present in gate_stage:
                assert _intersection_volume(gate_tool, present) < 1e-5, (
                    role,
                    gate_tool.label,
                    present.label,
                )

        # Motor service is intentionally last: role ring, gates, bearings,
        # vertical bevel, D-shaft, spacer, pinion, and collars are all absent.
        # Motor screws are targets, so they are excluded from obstruction.
        motor_stage = [
            part
            for part in make_motor_service_stage_parts(role)
            if "screw" not in part.label.lower() and "insert" not in part.label.lower()
        ]
        for motor_tool in tools[:4]:
            for present in motor_stage:
                assert _intersection_volume(motor_tool, present) < 1e-5, (
                    role,
                    motor_tool.label,
                    present.label,
                )

        # The upward-biased top-collar lock has a real 3 mm service envelope
        # that clears both the output pinion and its installed grub reference.
        top_tool = tools[11]
        pinion = make_role_pinion(role)
        pinion_grub = make_grub_screw_references(role)[2]
        assert _intersection_volume(top_tool, pinion) < 1e-5
        assert _intersection_volume(top_tool, pinion_grub) < 1e-5


def test_representative_stage_component_continuity_until_documented_removal():
    """An installed item may move for an exploded view, but never vanish."""

    stages = (
        make_stage_1_motor_mount(),
        make_stage_2_gearbox_mount(),
        make_stage_3_shaft_stack(),
        make_stage_4_height_lock(),
        make_stage_5_reverse_service(),
    )
    label_sets = tuple(
        {child.label for child in stage.children if "keep_clear" not in child.label.lower()}
        for stage in stages
    )
    for earlier, later in zip(label_sets, label_sets[1:]):
        assert earlier <= later, sorted(earlier - later)

    required_persistent = {
        "stage_second_horizontal_miter_D_bore_M2_axial_lock",
        "purchased_M2x3_horizontal_bevel_grub_screw_REFERENCE",
    }
    for labels in label_sets:
        assert required_persistent <= labels


def test_common_D_shaft_insertion_sweep_clears_every_role_stack():
    for role in range(3):
        frame = make_gearbox_frame(role)
        _, vertical = make_miter_pair(role)
        shaft = make_output_shaft(role)
        pinion = make_role_pinion(role)
        swept = make_shaft_insertion_swept_volume(role)
        # Tooth phase is applied first; one common +Y-facing D-bore is cut
        # afterward, so the same physical D-shaft must insert in all roles.
        assert _intersection_volume(shaft, pinion) < 1e-5
        assert "common_D_bore" in pinion.label
        for fixed_or_bored in (
            frame,
            make_bearing(role, "lower"),
            make_bearing(role, "upper"),
            vertical,
            make_clamp_collar(role, "lower"),
            make_role_spacer(role),
            pinion,
            make_clamp_collar(role, "top"),
        ):
            assert _intersection_volume(swept, fixed_or_bored) < 1e-5


def test_removable_bearing_gates_are_clear_at_nominal_and_block_radial_escape():
    for role in range(3):
        frame = make_gearbox_frame(role)
        for which in ("lower", "upper"):
            bearing = make_bearing(role, which)
            cap = make_bearing_radial_cap(role, which)
            assert len(cap.solids()) == 1
            assert _intersection_volume(cap, frame) < 1e-5
            assert _intersection_volume(cap, bearing) < 1e-5
            escaped = bearing.moved(Location((2.50, 0.0, 0.0)))
            assert _intersection_volume(cap, escaped) > 0.1
            assert len(make_bearing_cap_screws(role, which)) == 2


def test_positive_axial_locks_and_exact_output_height_exist_for_all_roles():
    for role in range(3):
        horizontal, vertical = make_miter_pair(role)
        refs = make_grub_screw_references(role)
        assert len(refs) == 3
        assert "M2_axial_lock" in horizontal.label
        assert "M2_set_screw" in vertical.label
        pinion = make_role_pinion(role)
        bounds = pinion.bounding_box()
        expected = p.parent.pinion_face_ranges[role]
        assert bounds.min.Z == pytest.approx(expected[0], abs=1e-6)
        assert bounds.max.Z == pytest.approx(expected[1], abs=1e-6)


def test_all_role_final_stations_have_no_unintended_pairwise_solid_collision():
    # Threaded inserts and screws intentionally occupy their mating pilots.
    # Every other staged solid must remain positive-volume disjoint, including
    # both bevels, D-shaft stack, bearing gates, output pinion, and ring coupon.
    for role in range(3):
        parts = [
            part
            for part in make_final_station_parts(role)
            if "screw" not in part.label.lower() and "insert" not in part.label.lower()
        ]
        for index, first in enumerate(parts):
            for second in parts[index + 1 :]:
                assert _intersection_volume(first, second) < 1e-5, (
                    role,
                    first.label,
                    second.label,
                    _intersection_volume(first, second),
                )


def test_exported_stage_set_is_nonempty_and_source_parity_is_reasonable():
    names = (
        "p3_v3_motor_station_stage1_motor_mount.step",
        "p3_v3_motor_station_stage2_gearbox_mount.step",
        "p3_v3_motor_station_stage3_shaft_stack.step",
        "p3_v3_motor_station_stage4_final_height_lock.step",
        "p3_v3_motor_station_stage5_reverse_service.step",
    )
    for name in names:
        path = MODEL_ROOT / name
        assert path.exists() and path.stat().st_size > 20_000
        exported = import_step(path)
        assert exported.bounding_box().size.X > 45.0
        assert exported.bounding_box().size.Z > 25.0


def test_export_manifest_hashes_current_sources_and_artifacts_without_stale_round_labels():
    manifest_path = MODEL_ROOT / "p3_v3_motor_station_manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    assert manifest["revision"] == "D-shaft-retained-static-stages-r2"
    root = Path(__file__).resolve().parents[1]
    for name, expected in manifest["source_sha256"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected
    for name, expected in manifest["artifact_sha256"].items():
        path = MODEL_ROOT / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        assert "round_shaft" not in path.read_text(errors="ignore")
    assert all("round" not in label.lower() for label in manifest["stage_labels"].values())


def test_viewer_caches_match_exact_current_step_hashes_and_labels():
    """Reject stale CAD Viewer packets after a STEP is regenerated.

    These caches are generated from the exported BREP, so their stepHash must
    match the manifest and their occurrences must not retain superseded
    round-shaft terminology.
    """
    manifest = json.loads(
        (MODEL_ROOT / "p3_v3_motor_station_manifest.json").read_text()
    )
    for name, expected_hash in manifest["artifact_sha256"].items():
        if not name.startswith("p3_v3_motor_station_stage"):
            continue
        cache_path = MODEL_ROOT / "__cadgen__" / "models" / name / "assembly.json"
        assert cache_path.exists(), name
        cache = json.loads(cache_path.read_text())
        assert cache["stepPath"] == name
        assert cache["stepHash"] == expected_hash
        assert cache["rootName"] == Path(name).stem
        occurrence_names = [item["name"] for item in cache["occurrences"]]
        assert occurrence_names
        assert all("round_shaft" not in label.lower() for label in occurrence_names)
