from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh
from build123d import Axis, Location

from p2r3_quartz_driver_module_geometry import (
    compact_dynamic_envelope_diameter,
    clock_angles_deg,
    make_all_fit_coupons,
    make_compact_reference_assembly,
    make_counterweight_cup,
    make_driver_arm,
    make_fit_coupon_ladder,
    make_full_radius_second_torque_wand,
    make_quartz_mount,
    pairwise_intersection_volume,
    placed_counterweight_cup,
    placed_driver_arm,
    production_balance_solution,
)
from p2r3_quartz_driver_module_spec import P2R3A


ROOT = Path(__file__).resolve().parents[1]


def _p2r2_stable_manifest():
    paths = [
        ROOT / "p2r2_magnetic_three_channel_300mm_spec.py",
        ROOT / "p2r2_magnetic_three_channel_300mm_geometry.py",
        ROOT / "p2r2_magnetic_three_channel_300mm_export.py",
        ROOT / "tests/test_p2r2_magnetic_three_channel_300mm.py",
        ROOT / "docs/p2r2-magnetic-three-channel-300mm-physical-test-plan.md",
    ]
    model_root = ROOT / "models/p2r2_magnetic_three_channel_300mm"
    for path in model_root.rglob("*"):
        if (
            path.is_file()
            and not any(part in path.parts for part in ("__cadgen__", "__pycache__", "snapshots"))
            and path.name != ".DS_Store"
        ):
            paths.append(path)
    paths = sorted(set(paths))
    digest = sha256()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + sha256(path.read_bytes()).digest())
    return paths, digest.hexdigest()


def test_provisional_quartz_envelope_is_explicit_and_parameterized():
    q = P2R3A.quartz
    assert q.source_names == ("MH011", "HR1688")
    assert q.verification_state == "UNVERIFIED_PROVISIONAL_NONPRINTABLE_REFERENCE"
    assert "step.parts" in q.provenance
    assert (q.case_width_x, q.case_height_y, q.case_depth_z) == (56.0, 56.0, 16.2)
    assert (q.case_rear_z, q.case_front_z) == pytest.approx((-31.6, -15.4))
    assert q.threaded_mount_diameter == 8.2
    assert q.shaft_nominal_od == (5.0, 3.25, 0.75)
    assert q.shaft_attach_height_from_case_front == (10.1, 13.5, 15.0)
    assert q.shaft_attach_z == pytest.approx((-5.3, -1.9, -0.4))


def test_frozen_arm_planes_clear_and_match_shaft_attach_datums():
    channels = P2R3A.channels
    assert tuple(channel.validation_radius for channel in channels) == (32.0, 51.0, 70.0)
    assert tuple(channel.production_radius for channel in channels) == (95.0, 115.0, 135.0)
    assert tuple(channel.arm_z for channel in channels) == ((-6.1, -5.3), (-2.7, -1.9), (-1.2, -0.4))
    assert tuple(channel.magnet_face_z for channel in channels) == (-5.4, -2.0, -0.5)
    assert tuple(channel.shaft_attach_z for channel in channels) == pytest.approx((-5.3, -1.9, -0.4))
    gaps = (
        channels[1].arm_z[0] - channels[0].arm_z[1],
        channels[2].arm_z[0] - channels[1].arm_z[1],
    )
    assert gaps == pytest.approx((2.6, 0.7))
    assert min(gaps) >= 0.4
    cup_corridors = tuple(channel.counterweight_cup_z for channel in channels)
    assert cup_corridors == ((-6.3, -4.3), (-3.5, -1.5), (-0.9, 1.1))
    assert tuple(channel.counterweight_tail_z_offset for channel in channels) == (0.0, 0.0, 0.5)
    cup_gaps = (
        cup_corridors[1][0] - cup_corridors[0][1],
        cup_corridors[2][0] - cup_corridors[1][1],
    )
    assert cup_gaps == pytest.approx((0.8, 0.6))
    assert min(cup_gaps) - 2 * P2R3A.counterweight_axial_float_z >= 0.2 - 1e-7


def test_compact_reference_pose_and_full_dynamic_envelope_are_under_150mm():
    assembly = make_compact_reference_assembly()
    bbox = assembly.bounding_box()
    assert len(assembly.solids()) == 11
    assert (bbox.size.X, bbox.size.Y, bbox.size.Z) == pytest.approx((129.3, 70.0, 32.7))
    assert compact_dynamic_envelope_diameter() == pytest.approx(149.0)
    assert compact_dynamic_envelope_diameter() <= P2R3A.compact_dynamic_max_diameter
    printed = [make_quartz_mount()]
    for name in ("hour", "minute", "second"):
        printed.extend((make_driver_arm(name), make_counterweight_cup(name, arm_z0=0.0)))
    for part in printed:
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0


@pytest.mark.parametrize("name", ("hour", "minute", "second"))
def test_driver_arm_has_real_hub_bore_magnet_floor_and_6p15x3p10_seat(name):
    channel = P2R3A.channel(name)
    arm = make_driver_arm(name)
    radius = channel.validation_radius
    assert arm.is_valid and len(arm.solids()) == 1 and arm.volume > 0
    assert arm.bounding_box().size.Y == pytest.approx(P2R3A.magnet_boss_outer_diameter)
    expected_z = P2R3A.magnet_boss_height + channel.counterweight_tail_z_offset
    assert arm.bounding_box().size.Z == pytest.approx(expected_z)
    # Hub bore is open through the arm plane.
    assert not arm.is_inside((0.0, 0.0, sum(channel.arm_z) / 2))
    # Pocket center is open for exactly the 3.10 mm seat depth.
    pocket_bottom = channel.arm_z[1] - P2R3A.magnet_pocket_depth
    assert not arm.is_inside((radius, 0.0, pocket_bottom + 0.05))
    # The printed 0.80 mm floor immediately behind the pocket remains solid.
    floor_bottom = channel.arm_z[1] - P2R3A.magnet_boss_height
    assert arm.is_inside((radius, 0.0, floor_bottom + P2R3A.magnet_pocket_floor / 2))
    # Radial sampling distinguishes the Ø6.15 pocket from the Ø9.0 boss.
    assert not arm.is_inside((radius, P2R3A.magnet_pocket_diameter / 2 - 0.02, pocket_bottom + 0.2))
    assert arm.is_inside((radius, P2R3A.magnet_pocket_diameter / 2 + 0.20, pocket_bottom + 0.2))


@pytest.mark.parametrize("name", ("hour", "minute", "second"))
def test_counterweight_cup_tunnel_is_clear_and_reference_pose_does_not_collide(name):
    cup = make_counterweight_cup(name, arm_z0=0.0)
    assert cup.is_valid and len(cup.solids()) == 1 and cup.volume > 0
    assert not cup.is_inside((0.0, 0.0, P2R3A.arm_thickness / 2))
    assert P2R3A.counterweight_tail_clearance_y == pytest.approx(0.8)
    assert P2R3A.counterweight_tail_clearance_z == pytest.approx(0.4)
    assert P2R3A.counterweight_snap_opening_y < P2R3A.arm_width
    angle = dict(zip(("hour", "minute", "second"), P2R3A.compact_angles_deg))[name]
    arm = placed_driver_arm(name, angle)
    placed = placed_counterweight_cup(name, angle)
    assert pairwise_intersection_volume(arm, placed) <= 1e-6

    # The integral widened stops allow 6 mm travel, then positively block the
    # cup in both radial directions.  The C-mouth is the only assembly path.
    beyond = P2R3A.counterweight_adjustment_travel_x / 2 + 0.75
    assert pairwise_intersection_volume(arm, placed.moved(Location((-beyond, 0, 0)))) > 0.1
    assert pairwise_intersection_volume(arm, placed.moved(Location((beyond, 0, 0)))) > 0.1


@pytest.mark.parametrize("radius_kind", ("validation", "production"))
def test_true_aligned_pose_has_zero_pairwise_printed_solid_collisions(radius_kind):
    parts = []
    for name in ("hour", "minute", "second"):
        parts.extend(
            (
                (f"{name}_arm", placed_driver_arm(name, 0.0, radius_kind=radius_kind)),
                (f"{name}_cup", placed_counterweight_cup(name, 0.0, radius_kind=radius_kind)),
            )
        )
    observed = {}
    for index, (left_name, left) in enumerate(parts):
        for right_name, right in parts[index + 1 :]:
            observed[(left_name, right_name)] = pairwise_intersection_volume(left, right)
    assert observed
    assert all(volume <= 1e-7 for volume in observed.values()), observed


@pytest.mark.parametrize("radius_kind", ("validation", "production"))
def test_all_360_relative_angles_clear_for_cross_arm_cup_and_cup_cup(radius_kind):
    """Exhaustive one-degree BREP sweep; parts are built once then rotated."""
    names = ("hour", "minute", "second")
    arms = {
        name: placed_driver_arm(name, 0.0, radius_kind=radius_kind) for name in names
    }
    cups = {
        name: placed_counterweight_cup(name, 0.0, radius_kind=radius_kind)
        for name in names
    }
    worst = (None, 0.0)
    for arm_name, arm in arms.items():
        for cup_name, cup in cups.items():
            if arm_name == cup_name:
                continue
            for relative_angle in range(360):
                volume = pairwise_intersection_volume(
                    arm, cup.rotate(Axis.Z, relative_angle)
                )
                if volume > worst[1]:
                    worst = ((f"{arm_name}_arm", f"{cup_name}_cup", relative_angle), volume)
    for index, left_name in enumerate(names):
        for right_name in names[index + 1 :]:
            for relative_angle in range(360):
                volume = pairwise_intersection_volume(
                    cups[left_name], cups[right_name].rotate(Axis.Z, relative_angle)
                )
                if volume > worst[1]:
                    worst = ((f"{left_name}_cup", f"{right_name}_cup", relative_angle), volume)
    assert worst[1] <= 1e-7, worst


@pytest.mark.parametrize("radius_kind", ("validation", "production"))
def test_all_360_relative_angles_clear_at_every_axial_float_corner(radius_kind):
    """Exhaustive angle proof at every +/-0.20 mm cup-float corner.

    Rotation about Z cannot change a solid's Z interval.  Strictly disjoint Z
    bounds therefore exclude a collision for every relative angle exactly,
    without thousands of redundant Boolean operations.  The nominal BREP
    sweep above remains the independent solid-level check.
    """
    names = ("hour", "minute", "second")
    float_limit = P2R3A.counterweight_axial_float_z
    float_corners = (-float_limit, float_limit)
    arms = {
        name: placed_driver_arm(name, 0.0, radius_kind=radius_kind) for name in names
    }
    cups = {
        (name, axial_float): placed_counterweight_cup(
            name,
            0.0,
            radius_kind=radius_kind,
            axial_float_z=axial_float,
        )
        for name in names
        for axial_float in float_corners
    }

    def axial_gap(left, right):
        left_box, right_box = left.bounding_box(), right.bounding_box()
        return max(
            right_box.min.Z - left_box.max.Z,
            left_box.min.Z - right_box.max.Z,
        )

    observed_worst = (None, 0.0)
    for arm_name, arm in arms.items():
        for cup_name in names:
            if arm_name == cup_name:
                continue
            for cup_float in float_corners:
                cup = cups[(cup_name, cup_float)]
                gap = axial_gap(arm, cup)
                for relative_angle in range(360):
                    # Magnet bosses enlarge the arm Z bound, so use a real
                    # Boolean only for the few pairs whose axial bounds overlap.
                    volume = 0.0 if gap >= 0.0 else pairwise_intersection_volume(
                        arm, cup.rotate(Axis.Z, relative_angle)
                    )
                    if volume > observed_worst[1]:
                        observed_worst = (
                            (f"{arm_name}_arm", f"{cup_name}_cup", cup_float, relative_angle),
                            volume,
                        )

    minimum_cup_gap = (None, float("inf"))
    for left_index, left_name in enumerate(names):
        for right_name in names[left_index + 1 :]:
            for left_float in float_corners:
                for right_float in float_corners:
                    gap = axial_gap(
                        cups[(left_name, left_float)],
                        cups[(right_name, right_float)],
                    )
                    for relative_angle in range(360):
                        if gap < minimum_cup_gap[1]:
                            minimum_cup_gap = (
                                (
                                    f"{left_name}_cup",
                                    left_float,
                                    f"{right_name}_cup",
                                    right_float,
                                    relative_angle,
                                ),
                                gap,
                            )
    assert observed_worst[1] <= 1e-7, observed_worst
    assert minimum_cup_gap[1] >= 0.2 - 1e-7, minimum_cup_gap


@pytest.mark.parametrize("radius_kind", ("validation", "production"))
def test_minute_second_same_angle_opposite_float_corner_has_0p20_gap(radius_kind):
    minute = placed_counterweight_cup(
        "minute", 0.0, radius_kind=radius_kind, axial_float_z=0.20
    )
    second = placed_counterweight_cup(
        "second", 0.0, radius_kind=radius_kind, axial_float_z=-0.20
    )
    minute_box, second_box = minute.bounding_box(), second.bounding_box()
    assert second_box.min.Z - minute_box.max.Z == pytest.approx(0.20)
    assert pairwise_intersection_volume(minute, second) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        placed_counterweight_cup(
            "second", 0.0, radius_kind=radius_kind, axial_float_z=0.201
        )


def test_former_failure_states_and_representative_12_hour_clock_sweep_clear():
    names = ("hour", "minute", "second")
    base = {}
    for name in names:
        base[(name, "arm")] = placed_driver_arm(name, 0.0)
        base[(name, "cup")] = placed_counterweight_cup(name, 0.0)

    states = [(6, 0, 0), (12, 0, 30)]
    states.extend((hour, minute, 0) for hour in range(12) for minute in (0, 30))
    observed_worst = (None, 0.0)
    for state in states:
        angles = dict(zip(names, clock_angles_deg(*state)))
        parts = [
            (f"{name}_{kind}", base[(name, kind)].rotate(Axis.Z, angles[name]))
            for name in names
            for kind in ("arm", "cup")
        ]
        for index, (left_name, left) in enumerate(parts):
            for right_name, right in parts[index + 1 :]:
                volume = pairwise_intersection_volume(left, right)
                if volume > observed_worst[1]:
                    observed_worst = ((state, left_name, right_name), volume)
    assert observed_worst[1] <= 1e-7, observed_worst


def test_counterweight_mass_uses_live_petg_brep_centroids_and_meets_targets():
    observed_ideal = {}
    for name in ("hour", "minute", "second"):
        channel = P2R3A.channel(name)
        solution = production_balance_solution(name)
        observed_ideal[name] = solution.ideal_filler_mass_g
        assert solution.arm_mass_g > 0.0 and solution.cup_mass_g > 0.0
        assert solution.arm_centroid_x_mm != 0.0
        assert solution.cup_centroid_x_mm == pytest.approx(-channel.counterweight_production_radius)
        assert abs(solution.residual_gf_cm) <= channel.residual_target_gf_cm
    assert observed_ideal == pytest.approx(
        {"hour": 1.05615660, "minute": 0.55568563, "second": 1.21204693},
        abs=1e-6,
    )


def test_tungsten_putty_wells_have_verified_density_capacity_margin():
    assert P2R3A.ballast_material_candidate == "TP7 tungsten-polymer putty"
    assert "7.2-7.4" in P2R3A.ballast_density_provenance
    assert P2R3A.ballast_magnetic_acceptance.startswith("PHYSICAL_GATE")
    assert P2R3A.ballast_well_volume_cm3 == pytest.approx(0.228)
    assert P2R3A.minimum_tungsten_putty_capacity_g == pytest.approx(1.6416)
    for name in ("hour", "minute", "second"):
        required = production_balance_solution(name).ideal_filler_mass_g
        assert P2R3A.minimum_tungsten_putty_capacity_g >= (
            P2R3A.ballast_capacity_safety_factor * required
        )


def test_four_fit_ladders_are_single_solids_with_exact_bores_and_step_heights():
    ladders = (
        ("movement_mount", P2R3A.mount_bore_candidates),
        ("hour_hub", P2R3A.channel("hour").hub_bore_candidates),
        ("minute_hub", P2R3A.channel("minute").hub_bore_candidates),
        ("second_hub", P2R3A.channel("second").hub_bore_candidates),
    )
    total_length = P2R3A.coupon_pad_length + 3 * P2R3A.coupon_pitch
    x0 = -total_length / 2 + P2R3A.coupon_pad_length / 2
    for name, bores in ladders:
        ladder = make_fit_coupon_ladder(name, bores)
        assert ladder.is_valid and len(ladder.solids()) == 1 and ladder.volume > 0
        assert tuple(ladder.bounding_box().size) == pytest.approx((62.0, 14.0, 3.0))
        for index, (bore, thickness) in enumerate(zip(bores, P2R3A.coupon_thickness_steps)):
            x = x0 + index * P2R3A.coupon_pitch
            assert not ladder.is_inside((x, 0.0, thickness / 2))
            assert ladder.is_inside((x, bore / 2 + 0.35, min(thickness - 0.05, 1.0)))
            assert not ladder.is_inside((x, 5.0, thickness + 0.05))
    coupons = make_all_fit_coupons()
    assert len(coupons.solids()) == 4


def test_full_radius_second_torque_wand_has_r135_tip_and_captured_r75_counter_tail():
    wand = make_full_radius_second_torque_wand()
    bbox = wand.bounding_box()
    assert wand.is_valid and len(wand.solids()) == 1 and wand.volume > 0
    assert bbox.min.X == pytest.approx(-85.8)
    assert bbox.max.X == pytest.approx(139.5)
    assert bbox.size.X == pytest.approx(225.3)
    assert not wand.is_inside((135.0, 0.0, P2R3A.channel("second").arm_z[1] - 0.2))


def test_p2r2_stable_sources_and_artifacts_remain_byte_identical():
    paths, digest = _p2r2_stable_manifest()
    assert len(paths) == P2R3A.p2r2_stable_file_count
    assert digest == P2R3A.p2r2_stable_manifest_sha256


def test_generated_step_and_print_artifacts_are_named_and_loadable():
    model_root = ROOT / "models/p2r3_quartz_driver_module"
    for filename in (
        "p2r3_compact_reference_assembly.step",
        "p2r3_fit_coupon_ladders.step",
        "p2r3_second_r135_torque_wand.step",
        "p2r3_quartz_mount.step",
        "p2r3_state_060000.step",
        "p2r3_state_120030.step",
    ):
        path = model_root / filename
        assert path.exists() and path.stat().st_size > 0

    print_root = model_root / "print"
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    expected = {
        "p2r3_module_a_compact_validation.3mf": 11,
        "p2r3_second_r135_torque_wand.3mf": 3,
    }
    for filename, count in expected.items():
        path = print_root / filename
        assert path.exists() and path.stat().st_size > 0
        with ZipFile(path) as package:
            assert package.testzip() is None
            root = ET.fromstring(package.read("3D/3dmodel.model"))
        objects = root.findall("m:resources/m:object", ns)
        items = root.findall("m:build/m:item", ns)
        assert len(objects) == len(items) == count
        assert all("PROVISIONAL" not in obj.attrib["name"] for obj in objects)

    stls = sorted(print_root.glob("*.stl"))
    assert len(stls) == 12
    for path in stls:
        mesh = trimesh.load_mesh(path, process=True, validate=True)
        assert mesh.body_count == 1 and mesh.is_watertight and mesh.is_volume
        assert mesh.bounds[0][2] == pytest.approx(0.0, abs=1e-7)
