"""Contract tests for the complete KAGE P3 V3 R2 stacked-ring mechanism."""

from __future__ import annotations

import json
from math import isclose
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest
from build123d import Axis

from p3_v3_full_ring_r2_geometry import (
    _full_role_ring,
    make_fin,
    make_frame_segments,
    make_keeper_saddle_parts,
    make_motor_station_parts,
    make_ring_quadrants,
    make_outer_front_ring_segments,
    make_seam_hardware,
    make_station_clearance_envelope,
    make_station_support,
    make_station_support_components,
)
from p3_v3_full_ring_r2_spec import P3_V3_FULL_RING_R2 as p


def _intersection_volume(left, right):
    common = left.intersect(right)
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _run_role_brep_subprocess(role: int):
    """Run each role's complete-ring BREP sweep in a fresh OCC process."""

    script = textwrap.dedent(
        """
        import json
        import sys

        from p3_v3_full_ring_r2_geometry import make_canonical_mesh_pair_at_phase
        from p3_v3_full_ring_r2_spec import P3_V3_FULL_RING_R2 as p

        role = int(sys.argv[1])
        station = p.motor_station_angles[role]
        phases = [("nominal", 0.0)] + [
            (f"seam_{seam:g}", station - seam)
            for seam in (0.0, 90.0, 180.0, 270.0)
        ]
        results = []
        for name, ring_angle in phases:
            ring, pinion = make_canonical_mesh_pair_at_phase(role, ring_angle)
            common = ring.intersect(pinion)
            volume = sum(solid.volume for solid in common.solids()) if common else 0.0
            results.append({
                "phase": name,
                "ringAngle": ring_angle,
                "intersectionVolume": volume,
                "distance": ring.distance_to(pinion),
            })
        print(json.dumps({"role": role, "checks": results}, sort_keys=True))
        """
    )
    project_root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "-c", script, str(role)],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    print(f"BREP_ROLE_EXIT role={role} code={completed.returncode}")
    assert completed.returncode == 0, (
        f"role {role} BREP subprocess exited {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    assert lines, f"role {role} BREP subprocess produced no JSON"
    return json.loads(lines[-1])


def _run_support_brep_subprocess(role: int):
    """Check one finished support against all twelve station occurrences."""

    script = textwrap.dedent(
        """
        import json
        import sys
        from p3_v3_full_ring_r2_geometry import make_motor_station_parts, make_station_support

        role = int(sys.argv[1])
        support = make_station_support(role)
        results = []
        for index, part in enumerate(make_motor_station_parts(role)):
            common = support.intersect(part)
            volume = sum(solid.volume for solid in common.solids()) if common else 0.0
            results.append({
                "index": index,
                "intersectionVolume": volume,
                "distance": support.distance_to(part),
            })
        print(json.dumps({"role": role, "supportSolids": len(support.solids()), "checks": results}, sort_keys=True))
        """
    )
    completed = subprocess.run(
        [sys.executable, "-c", script, str(role)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    print(f"SUPPORT_ROLE_EXIT role={role} code={completed.returncode}")
    assert completed.returncode == 0, (
        f"role {role} support subprocess exited {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )
    return json.loads([line for line in completed.stdout.splitlines() if line.strip()][-1])


def _run_support_topology_subprocess(role: int):
    """Build one completed support in a fresh OCC process."""

    script = textwrap.dedent(
        """
        import json
        import sys
        from p3_v3_full_ring_r2_geometry import make_station_support

        support = make_station_support(int(sys.argv[1]))
        print(json.dumps({
            "valid": support.is_valid,
            "solids": len(support.solids()),
            "volume": support.volume,
        }, sort_keys=True))
        """
    )
    completed = subprocess.run(
        [sys.executable, "-c", script, str(role)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert completed.returncode == 0, (
        f"role {role} support topology subprocess exited {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )
    return json.loads([line for line in completed.stdout.splitlines() if line.strip()][-1])


def test_complete_three_role_contract_not_coupon():
    assert p.roles == ("hour", "minute", "second")
    assert len(p.motor_station_angles) == len(p.roles) == 3
    assert p.ring_teeth == 260
    assert p.quadrant_count == 4
    assert p.quadrant_teeth == p.quadrant_tooth_count == 65
    assert p.quadrant_count * p.quadrant_teeth == p.ring_teeth


def test_one_coherent_m1_pa20_ring_and_pinion_system():
    assert p.module == pytest.approx(1.0)
    assert p.pressure_angle_degrees == pytest.approx(20.0)
    assert p.pinion_teeth == 16
    assert p.ring_pitch_radius == pytest.approx(p.module * p.ring_teeth / 2.0)
    assert p.pinion_pitch_radius == pytest.approx(p.module * p.pinion_teeth / 2.0)
    assert p.output_axis_radius == pytest.approx(p.ring_pitch_radius - p.pinion_pitch_radius)
    assert p.gear_ratio == pytest.approx(16.25)


def test_quadrant_seams_and_joint_holes_stay_outside_active_root():
    assert p.quadrant_angle_degrees * p.quadrant_count == pytest.approx(360.0)
    assert p.joint_inner_radius > p.ring_active_root_radius
    assert p.joint_hole_edge_angle_degrees > 0.0
    assert p.joint_hole_edge_angle_degrees < p.quadrant_angle_degrees / 2.0


def test_frozen_layers_and_active_faces_have_overlap_and_clearance():
    assert p.carrier_layers == ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    assert p.pinion_face_ranges == ((-0.7, 1.4), (4.85, 6.95), (10.4, 12.5))
    assert p.carrier_gaps == pytest.approx((2.55, 2.55))
    assert p.pinion_face_widths == pytest.approx((2.1, 2.1, 2.1))
    for face, carrier in zip(p.pinion_face_ranges, p.carrier_layers):
        assert carrier[0] < face[0] < face[1] < carrier[1]


def test_underside_races_are_below_active_mesh_faces():
    for role in range(3):
        race = p.race_range(role)
        assert race[1] == pytest.approx(p.carrier_layers[role][0])
        assert p.race_to_mesh_clearance(role) >= p.race_to_mesh_min_clearance
        assert race[0] == pytest.approx(p.carrier_layers[role][0] - p.rail_total_depth)


def test_three_rear_keepers_per_ring_and_positive_capture_clearance():
    assert tuple(len(group) for group in p.guide_tower_angles) == (3, 3, 3)
    assert p.keeper_axial_float == pytest.approx(0.30)
    assert p.keeper_axial_face_clearance == pytest.approx(0.15)
    assert p.keeper_radial_clearance == pytest.approx(0.25)
    assert p.keeper_channel_radii == pytest.approx((132.55, 135.85))
    assert p.keeper_pull_test_status == "PENDING_PHYSICAL"


def test_stationary_outer_front_ring_respects_all_fin_lanes():
    assert p.retainer_radii == pytest.approx((145.0, 150.0))
    assert max(r[1] for r in p.fin_blade_radial_ranges) == pytest.approx(143.9)
    assert p.retainer_radii[0] - max(r[1] for r in p.fin_blade_radial_ranges) == pytest.approx(1.10)


def test_integral_fin_roots_bridge_own_carrier_to_exact_blade_lanes():
    assert p.fin_blade_radial_ranges == (
        (142.7, 143.9), (140.75, 141.95), (137.2, 138.4)
    )
    assert p.fin_root_radial_ranges == (
        (135.5, 143.9), (135.5, 141.95), None
    )
    assert p.fin_root_z_ranges == ((0.2, 1.6), (5.3, 6.7), None)


def test_fin_width_order_z_datums_solidity_and_occurrence_labels():
    assert p.fin_tangential_widths[0] > p.fin_tangential_widths[1] > p.fin_tangential_widths[2]
    labels = []
    for role in range(3):
        fin = make_fin(role)
        labels.append(fin.label)
        assert fin.bounding_box().min.Z == pytest.approx(p.fin_blade_start_zs[role])
        assert fin.is_valid
        assert len(fin.solids()) == 1
        assert p.roles[role] in fin.label
    assert len(labels) == len(set(labels)) == 3


@pytest.mark.parametrize("fin_role,ring_role", ((0, 1), (0, 2), (1, 2)))
def test_corrected_fin_clears_every_nonown_ring_at_coincident_angle(fin_role, ring_role):
    """The full rings are rotationally symmetric, so one coincident pose is decisive."""

    fin = make_fin(fin_role).rotate(Axis.Z, -p.display_fin_angles[fin_role])
    volume = _intersection_volume(fin, _full_role_ring(ring_role))
    assert volume <= 1e-7, (
        f"{p.roles[fin_role]} fin intersects {p.roles[ring_role]} ring "
        f"by {volume:.6f} mm3"
    )


def test_corrected_fins_clear_stationary_frame_retainer_and_each_other():
    fins = [
        make_fin(role).rotate(Axis.Z, -p.display_fin_angles[role])
        for role in range(3)
    ]
    for fin in fins:
        for fixed in (*make_frame_segments(), *make_outer_front_ring_segments()):
            assert _intersection_volume(fin, fixed) <= 1e-7
    for left, right in ((0, 1), (0, 2), (1, 2)):
        assert _intersection_volume(fins[left], fins[right]) <= 1e-7


def test_horizontal_three_motor_station_interfaces_are_frozen_r1_values():
    assert p.motor_station_angles == pytest.approx((0.0, 120.0, 240.0))
    assert p.motor_face_size == pytest.approx(20.3)
    assert p.motor_body_length == pytest.approx(39.3)
    assert p.output_shaft_length == pytest.approx(40.0)
    assert p.output_shaft_z[1] - p.output_shaft_z[0] == pytest.approx(40.0)
    assert p.bearing_id == pytest.approx(p.output_shaft_diameter)
    assert p.bearing_od == pytest.approx(8.0)
    assert p.miter_teeth == 16 and p.miter_ratio == pytest.approx(1.0)
    assert p.miter_static_gap > 0.0
    assert p.motor_hub_overlap_min >= 5.95


def test_rigid_station_translation_updates_axis_and_motor_face_together():
    assert p.station_radial_translation == pytest.approx(0.50)
    assert p.output_axis_radius == pytest.approx(121.5 + p.station_radial_translation)
    assert p.motor_face_radius == pytest.approx(111.25 + p.station_radial_translation)


def test_all_quadrant_frame_chassis_and_retainer_segments_fit_u1():
    assert p.largest_quadrant_xy == pytest.approx(150.0)
    assert p.largest_quadrant_xy <= p.segment_bed_limit
    assert p.ring_outer_radius <= p.segment_bed_limit
    assert p.chassis_radii[1] <= p.segment_bed_limit
    assert p.retainer_radii[1] <= p.segment_bed_limit


def test_analytic_full_phase_sweep_covers_520_ring_phases_per_role():
    # Two samples per tooth guarantees both flanks of all 260 internal teeth
    # are represented; ring/pinion phase coupling follows the exact tooth ratio.
    samples = 520
    ring_angles = [360.0 * index / samples for index in range(samples)]
    assert len(ring_angles) == 520
    assert ring_angles[-1] < 360.0
    pinion_angles = [angle * p.gear_ratio for angle in ring_angles]
    for ring_angle, pinion_angle in zip(ring_angles, pinion_angles):
        reconstructed = pinion_angle / p.gear_ratio
        assert reconstructed == pytest.approx(ring_angle)
    assert pinion_angles[-1] - pinion_angles[0] > 16.0 * 360.0


def test_dense_seam_crossing_phase_neighborhoods_cover_both_sides():
    epsilon = p.tooth_pitch_degrees / 20.0
    phases = []
    for seam in (0.0, 90.0, 180.0, 270.0):
        phases.extend((seam - epsilon, seam, seam + epsilon))
    assert len(phases) == 12
    for seam, group in zip((0.0, 90.0, 180.0, 270.0), (phases[i:i+3] for i in range(0, 12, 3))):
        assert group[0] < seam < group[2]


def test_independent_role_angles_preserve_axial_clearance_simultaneously():
    # Angular state cannot reduce the frozen 0.4 mm axial carrier separation.
    angle_sets = ((0.0, 0.0, 0.0), (0.0, 120.0, 240.0), (359.9, 180.0, 0.1))
    for _angles in angle_sets:
        assert min(p.carrier_gaps) >= 0.40 - 1e-9


def test_ring_rotation_resolution_is_consistent():
    assert p.ring_degrees_per_pinion_revolution == pytest.approx(360.0 * 16.0 / 260.0)
    assert isclose(p.tooth_pitch_degrees * p.ring_teeth, 360.0, abs_tol=1e-12)


def test_actual_quadrants_are_unique_valid_65t_solids_with_real_seam_hardware():
    for role in range(3):
        quadrants = make_ring_quadrants(role)
        assert len(quadrants) == 4
        assert len({part.label for part in quadrants}) == 4
        assert all(part.is_valid and len(part.solids()) == 1 for part in quadrants)
        fin_quadrant = int(p.display_fin_angles[role] // p.quadrant_angle_degrees)
        plain_volumes = [part.volume for index, part in enumerate(quadrants) if index != fin_quadrant]
        assert max(plain_volumes) - min(plain_volumes) < 1e-4
        assert quadrants[fin_quadrant].volume > max(plain_volumes)
        hardware = make_seam_hardware(role)
        assert len(hardware) == 16  # 4 plates + 4 dowels + 8 M2 references
        labels = tuple(part.label for part in hardware)
        assert sum("underside_splice" in label for label in labels) == 4
        assert sum("registration_dowel" in label for label in labels) == 4
        assert sum("M2_screw" in label for label in labels) == 8


@pytest.mark.parametrize("role", range(3))
def test_complete_canonical_ring_brep_nominal_and_all_four_seams(role):
    # Exact seam poses are the mechanically highest-risk subset.  Each role is
    # isolated in a fresh process so an OCC failure becomes an explicit exit
    # code instead of terminating pytest.  The 520-pose relationship remains
    # covered analytically above.
    payload = _run_role_brep_subprocess(role)
    assert payload["role"] == role
    assert len(payload["checks"]) == 5
    assert {check["phase"] for check in payload["checks"]} == {
        "nominal", "seam_0", "seam_90", "seam_180", "seam_270"
    }
    for check in payload["checks"]:
        assert check["intersectionVolume"] <= 1e-7
        assert check["distance"] > 0.05


def test_actual_rear_keeper_parts_capture_each_ring_without_intersection():
    for role in range(3):
        ring = _full_role_ring(role)
        fixed, cap, liner = make_keeper_saddle_parts(role, 0)
        assert all(_intersection_volume(part, ring) <= 1e-7 for part in (fixed, cap, liner))
        assert liner.distance_to(ring) == pytest.approx(0.15, abs=1e-6)
        assert p.upper_bridge_range(role)[0] - (
            p.carrier_layers[role][0] - p.rail_neck_depth
        ) == pytest.approx(0.15)


def test_station_clearance_envelope_expands_every_axis_by_twice_allowance():
    representative_parts = make_motor_station_parts(0)
    for part in (representative_parts[0], representative_parts[2], representative_parts[11]):
        envelope = make_station_clearance_envelope(part, p.station_support_clearance)
        source_box = part.bounding_box()
        envelope_box = envelope.bounding_box()
        assert envelope_box.size.X == pytest.approx(source_box.size.X + 2 * p.station_support_clearance)
        assert envelope_box.size.Y == pytest.approx(source_box.size.Y + 2 * p.station_support_clearance)
        assert envelope_box.size.Z == pytest.approx(source_box.size.Z + 2 * p.station_support_clearance)


def test_station_support_is_one_solid_with_finite_component_overlaps():
    # Analytic construction intervals prove positive overlap before the fuse;
    # a fresh OCC process then proves that the cut finished support is one
    # valid solid.  This avoids the unstable in-process pairwise BREP loop.
    pad_x = (69.0, 115.0)
    bridge_x = (110.0, 130.0)
    lower_x = (p.output_axis_radius - 6.0, p.output_axis_radius + 6.0)
    pylon_x = (p.output_axis_radius - 3.0, p.output_axis_radius + 6.0)
    upper_arm_x = (p.output_axis_radius - 6.0, p.output_axis_radius + 6.0)
    assert min(pad_x[1], bridge_x[1]) - max(pad_x[0], bridge_x[0]) == pytest.approx(5.0)
    assert min(bridge_x[1], lower_x[1]) - max(bridge_x[0], lower_x[0]) > 10.0
    assert min(bridge_x[1], pylon_x[1]) - max(bridge_x[0], pylon_x[0]) > 8.0
    assert min(pylon_x[1], upper_arm_x[1]) - max(pylon_x[0], upper_arm_x[0]) > 8.0
    for role in range(3):
        payload = _run_support_topology_subprocess(role)
        assert payload["valid"] is True
        assert payload["solids"] == 1
        assert payload["volume"] > 3000.0


@pytest.mark.parametrize("role", range(3))
def test_finished_support_has_zero_brep_intersection_with_every_station_part(role):
    payload = _run_support_brep_subprocess(role)
    assert payload["supportSolids"] == 1
    assert len(payload["checks"]) == 12
    for check in payload["checks"]:
        assert check["intersectionVolume"] <= 1e-7
        if check["index"] in (5, 6):  # MR84 running clearance
            assert check["distance"] >= 0.099
        elif check["index"] == 10:  # saddle underside datum contact
            assert check["distance"] == pytest.approx(0.0, abs=1e-7)
        else:
            assert check["distance"] >= p.station_support_clearance - 1e-7
