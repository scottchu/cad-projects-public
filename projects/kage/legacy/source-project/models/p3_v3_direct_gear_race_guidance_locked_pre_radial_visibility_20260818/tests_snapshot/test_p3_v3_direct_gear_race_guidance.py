"""Math and actual-solid contracts for the isolated direct gear-race trial."""

from __future__ import annotations

from hashlib import sha256
from math import cos, radians, sin
from pathlib import Path

import py_gearworks as pgw
import pytest
from build123d import Align, Axis, Box, Location

from p3_v3_direct_gear_race_guidance_geometry import (
    _bare_full_role_ring,
    make_carrier_race_band,
    make_fin_360_sweep,
    make_full_role_ring_reference,
    make_motor_station_parts,
    make_ring_quadrants,
    make_roller,
    make_roller_tower_yoke,
    make_seam_hardware,
    make_tooth_envelope,
    make_unibody_drive_yoke,
)
from p3_v3_direct_gear_race_guidance_spec import P3_V3_DIRECT_GEAR_RACE as p
from p3_v3_simplified_drive_guidance_spec import P3_V3_SIMPLIFIED as rollback


ROOT = Path(__file__).resolve().parents[1]
ROLLBACK_SHA256 = {
    "adr-free-spinner-ring-guidance-ui.js": "24c16ccc076d49375fdf1420f7fcb2fcbda4a9642b597f223a01b4e0c53545ef",
    "adr-free-spinner-ring-guidance.css": "24f5adb3d6bac81fc3cbb4457983b609c0a4f355c2048645b9c1c218c110a9f9",
    "adr-free-spinner-ring-guidance.html": "303391afda9afd08deb9d8a38f8310480f3ec8dbb685133073a888dc0f1c6cb9",
    "src/adr-free-spinner-ring-guidance.js": "89e916f6b59dd2b77e0143cde19eba3096c109260f39537bc6259e435f6bab57",
    "vendor/kage-free-spinner-adr.bundle.js": "e211e6ad71970fdac82b6ab5fdcbe7beffc96454f114bef7c2717329562da827",
    "tests/test_adr_free_spinner_ring_guidance.py": "962ead5d447e282c7892ccfc39bb64619134fed909caf79b486698fe58acbeb5",
    "p3_v3_simplified_drive_guidance_spec.py": "1e6b3fa62101ac5516a836f59dbdcd4174608eaffd00b01378bd0dc469054a7e",
    "p3_v3_simplified_drive_guidance_geometry.py": "ec9ee5dae0ece14cd1295db6fc75517d756660d449b3d48e0152262b1692c2cd",
    "p3_v3_simplified_drive_guidance_export.py": "c27b863d1bde5f4165e9c1b13b17ae0ee21ab009cfc9fdb54e932e5c0412ee11",
    "tests/test_p3_v3_simplified_drive_guidance.py": "293dec53a6a1e83bfa703d76d938ff604ae1efc1fb554cfc6c09b9bc5f1c12ff",
    "tests/test_p3_v3_simplified_drive_guidance_artifacts.py": "2b913e40a732e21db68bcb7371fdb2a5a349849817f5a088420510aa34fb97ab",
    "models/p3_v3_simplified_drive_guidance/p3_v3_simplified_assembled.step.py": "f34914fb2caa5d27d066f61e4a9a7aab46824906034aeab0a9d8bc622b9e874a",
    "models/p3_v3_simplified_drive_guidance/p3_v3_simplified_service_exploded.step.py": "ebc87c1fbfdf40ee5be91a82de558ec3ba1e376a83567c4ce49524818b7c5215",
    "models/p3_v3_simplified_drive_guidance/p3_v3_simplified_assembled.step": "e8f42c74add8aa5e30d896abc9dd8e4e710b8a2f5ae09cb04549c0e4676fd87f",
    "models/p3_v3_simplified_drive_guidance/p3_v3_simplified_service_exploded.step": "069c83b9fe89ddd729f0e3160e718044b72879007c8886a00c37885cf9f7ef9c",
}


def _volume(shape) -> float:
    return sum(s.volume for s in shape.solids()) if shape else 0.0


def _teeth(role: int):
    z0, z1 = p.pinion_face_ranges[role]
    return pgw.SpurRingGear(
        number_of_teeth=p.ring_teeth,
        module=p.module,
        height=z1 - z0,
        center=[0.0, 0.0, z0],
        backlash=0.10,
    ).build_part().solid().rotate(Axis.Z, p.tooth_phase_offset_degrees)


def test_rollback_cad_and_adr_are_byte_for_byte_unchanged():
    for relative, expected in ROLLBACK_SHA256.items():
        path = ROOT / relative
        assert path.is_file()
        assert sha256(path.read_bytes()).hexdigest() == expected, relative


def test_direct_race_contract_has_no_separate_guide_feature():
    assert p.separate_guide_feature is False
    assert p.tooth_tip_rolling_allowed is False
    assert p.roller_contact_surface == "carrier_inner_root_land_below_tooth_face"
    assert p.carrier_race_radius == pytest.approx(p.ring_body_inner_radius)
    labels = " ".join(q.label.lower() for role in range(3) for q in make_ring_quadrants(role))
    for forbidden in ("guide_bead", "guide_head", "guide_neck", "t_rail"):
        assert forbidden not in labels


def test_frozen_radii_gap_overlap_and_tooth_tip_clearance_math():
    assert (p.carrier_race_radius, p.tooth_tip_radius, p.tooth_root_radius) == pytest.approx((131.6, 129.0, 132.5))
    assert (p.roller_axis_radius, p.roller_hub_outer_diameter) == pytest.approx((125.5, 6.0))
    assert (p.roller_running_outer_diameter, p.roller_flange_outer_diameter) == pytest.approx((12.1, 13.8))
    assert p.roller_running_outer_radius == pytest.approx(131.55)
    assert p.roller_running_gap == pytest.approx(0.05)
    assert p.roller_stationary_outer_radius == pytest.approx(132.40)
    assert p.roller_capture_radial_overlap == pytest.approx(0.80)
    assert p.adjusted_tooth_tip_clearance == pytest.approx(0.25)


def test_compact_upper_safety_collars_preserve_bore_height_relief_and_endplay():
    """Only the unsafe upper OD changes; the shaft stack stays frozen."""

    assert p.upper_split_collar_outer_diameter == pytest.approx(8.00)
    assert p.split_collar_bore_diameter == pytest.approx(4.10)
    assert p.upper_split_collar_height == pytest.approx(2.60)
    assert p.upper_split_collar_relief == pytest.approx(0.05)
    for role in range(3):
        pinion_z1 = p.pinion_face_ranges[role][1]
        collar_z0, collar_z1 = p.upper_collar_z(role)
        assert collar_z0 - pinion_z1 == pytest.approx(0.05)
        assert collar_z1 - collar_z0 == pytest.approx(2.60)
        assert p.output_endplay_bounds[0] <= p.computed_output_endplay(role) <= p.output_endplay_bounds[1] + 1e-9
        collar = make_motor_station_parts(role)[10]
        bounds = collar.bounding_box()
        assert bounds.max.Z - bounds.min.Z == pytest.approx(2.60, abs=1e-6)
        assert max(bounds.size.X, bounds.size.Y) == pytest.approx(8.00, abs=1e-6)


def test_yoke_keepout_preserves_frozen_datums_bearing_ligament_and_service_slot():
    assert p.yoke_upper_bridge_radial_limit == pytest.approx(128.50)
    assert p.yoke_moving_ring_clearance == pytest.approx(0.50)
    assert p.yoke_upper_bearing_outer_ligament == pytest.approx(2.45)
    assert p.yoke_upper_bearing_outer_ligament >= 2.45 - 1e-9

    # No timing or purchased-part datum is allowed to move in this repair.
    frozen_names = (
        "output_axis_radius", "output_shaft_z", "output_shaft_diameter",
        "lower_bearing_range", "upper_bearing_range", "pinion_face_ranges",
        "station_role_z_translations", "motor_station_angles", "motor_face_radius",
        "unibody_bearing_pocket_diameter", "unibody_bearing_install_slot_width",
        "unibody_bearing_install_mouth_x",
    )
    for name in frozen_names:
        assert getattr(p, name) == getattr(rollback, name), name

    # The inherited +X bearing-install slot must remain genuinely open after
    # the radial trim, not merely described by a parameter.
    for role in range(3):
        z0, z1 = p.upper_bearing_z(role)
        local_slot = Box(
            p.yoke_upper_bridge_radial_limit - (p.output_axis_radius - 0.05) + 0.30,
            p.unibody_bearing_install_slot_width - 0.10,
            z1 - z0 - 0.20,
            align=(Align.MIN, Align.CENTER, Align.MIN),
        ).moved(Location((p.output_axis_radius - 0.05, 0.0, z0 + 0.10)))
        slot = local_slot.rotate(Axis.Z, p.motor_station_angles[role])
        assert _volume(make_unibody_drive_yoke(role).intersect(slot)) <= 1e-7


@pytest.mark.parametrize("station_role", range(3))
def test_actual_source_motor_station_to_complete_ring_pair_matrix(station_role):
    """Fresh OCC process: every non-meshing station/ring pair is disjoint.

    This is intentionally an actual-solid matrix rather than a radial-only
    assertion.  The only exclusions are the four quadrants of the station's
    own 16T/260T working mesh.
    """

    program = f'''
import json
from p3_v3_direct_gear_race_guidance_geometry import make_motor_station_parts, make_ring_quadrants
from p3_v3_direct_gear_race_guidance_spec import P3_V3_DIRECT_GEAR_RACE as p

station_role = {station_role}
parts = list(make_motor_station_parts(station_role))
rings = [list(make_ring_quadrants(role)) for role in range(3)]

def separated(a, b, eps=1e-8):
    aa, bb = a.bounding_box(), b.bounding_box()
    return (aa.max.X < bb.min.X - eps or bb.max.X < aa.min.X - eps or
            aa.max.Y < bb.min.Y - eps or bb.max.Y < aa.min.Y - eps or
            aa.max.Z < bb.min.Z - eps or bb.max.Z < aa.min.Z - eps)

checked = 0
candidate_pairs = 0
worst_volume = 0.0
worst_pair = None
for part in parts:
    for ring_role, quadrants in enumerate(rings):
        for ring in quadrants:
            if "16T_output_pinion" in part.label and ring_role == station_role:
                continue
            checked += 1
            volume = 0.0
            if not separated(part, ring):
                candidate_pairs += 1
                hit = part.intersect(ring)
                volume = sum(s.volume for s in hit.solids()) if hit else 0.0
            if volume > worst_volume:
                worst_volume = volume
                worst_pair = [part.label, ring.label]

yoke = parts[11]
yoke_clearances = []
for ring_role, quadrants in enumerate(rings):
    for ring in quadrants:
        aa, bb = yoke.bounding_box(), ring.bounding_box()
        z_overlap = min(aa.max.Z, bb.max.Z) - max(aa.min.Z, bb.min.Z)
        yoke_clearances.append({{
            "ring_role": ring_role,
            "label": ring.label,
            "z_overlap": z_overlap,
            "distance": yoke.distance_to(ring),
        }})

from p3_v3_full_ring_r2_geometry import _annulus
sweep_clearances = []
for ring_role in range(3):
    face0, face1 = p.pinion_face_ranges[ring_role]
    layer0, layer1 = p.carrier_layers[ring_role]
    tooth_sweep = _annulus(p.tooth_tip_radius, p.tooth_root_radius, face1 - face0, face0)
    body_sweep = _annulus(p.ring_body_inner_radius, p.ring_body_outer_radius, layer1 - layer0, layer0)
    sweep = tooth_sweep.fuse(body_sweep)
    aa, bb = yoke.bounding_box(), sweep.bounding_box()
    z_overlap = min(aa.max.Z, bb.max.Z) - max(aa.min.Z, bb.min.Z)
    sweep_clearances.append({{"ring_role": ring_role, "z_overlap": z_overlap, "distance": yoke.distance_to(sweep)}})

upper = parts[10]
collar_clearances = [min(upper.distance_to(q) for q in quadrants) for quadrants in rings]
print("P3_SOURCE_PAIR_MATRIX=" + json.dumps({{
    "checked": checked,
    "candidate_pairs": candidate_pairs,
    "worst_volume": worst_volume,
    "worst_pair": worst_pair,
    "collar_clearances": collar_clearances,
    "yoke_clearances": yoke_clearances,
    "sweep_clearances": sweep_clearances,
}}, separators=(",", ":")))
'''
    completed = __import__("subprocess").run(
        [__import__("sys").executable, "-c", program],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=240,
    )
    line = next(
        line for line in completed.stdout.splitlines()
        if line.startswith("P3_SOURCE_PAIR_MATRIX=")
    )
    result = __import__("json").loads(line.split("=", 1)[1])
    assert result["checked"] == 140
    assert result["candidate_pairs"] > 0
    assert result["worst_volume"] <= 1e-7, result["worst_pair"]
    assert result["collar_clearances"] == pytest.approx(
        {
            0: (3.0004166377, 3.1048349393, 7.0229979354),
            1: (6.3731748301, 3.0430013827, 3.1460065822),
            2: (11.5576752600, 6.3731748301, 3.0430013827),
        }[station_role],
        abs=1e-5,
    )
    assert min(result["collar_clearances"]) >= 3.0
    assert len(result["yoke_clearances"]) == 12
    assert all(item["distance"] >= -1e-9 for item in result["yoke_clearances"])
    assert all(
        item["distance"] >= 0.50 - 1e-6
        for item in result["yoke_clearances"]
        if item["z_overlap"] >= -1e-8
    )
    assert all(
        item["distance"] >= 0.50 - 1e-6
        for item in result["sweep_clearances"]
        if item["z_overlap"] >= -1e-8
    )


@pytest.mark.parametrize("role", range(3))
def test_motor_shaft_miters_and_pinion_clear_connected_yoke(role):
    parts = make_motor_station_parts(role)
    yoke = parts[11]
    # Motor body/shaft, both miter gears, output shaft, and output pinion.
    for index in (0, 1, 2, 3, 4, 8):
        assert _volume(yoke.intersect(parts[index])) <= 1e-7, parts[index].label


def test_frozen_carrier_race_contact_and_roller_z_bands():
    assert tuple(value for i in range(3) for value in p.race_range(i)) == pytest.approx((-1.5, -0.7, 4.05, 4.85, 9.6, 10.4))
    assert tuple(value for i in range(3) for value in p.contact_range(i)) == pytest.approx((-1.4, -0.8, 4.15, 4.75, 9.7, 10.3))
    assert tuple(value for i in range(3) for value in p.roller_range(i)) == pytest.approx((-2.15, 2.15, 3.4, 7.7, 8.95, 13.25))
    for role, (z0, z1) in enumerate(p.carrier_layers):
        lower, upper = p.roller_flange_ranges(role)
        assert lower[1] == pytest.approx(z0 - 0.15)
        assert upper[0] == pytest.approx(z1 + 0.15)
    assert p.roller_spacer_lengths == pytest.approx((1.25, 1.25))
    assert p.roller_thrust_washer_thickness == pytest.approx(0.20)


@pytest.mark.parametrize("role", range(3))
def test_bare_full_ring_matches_accepted_no_guide_carrier(role):
    accepted = _bare_full_role_ring(role)
    direct = make_full_role_ring_reference(role)
    assert direct.is_valid and len(direct.solids()) == 1
    assert _volume(direct) == pytest.approx(_volume(accepted), rel=1e-9, abs=1e-6)
    assert direct.bounding_box().min.Z == pytest.approx(p.carrier_layers[role][0])
    assert direct.bounding_box().max.Z == pytest.approx(p.carrier_layers[role][1])


@pytest.mark.parametrize("role", range(3))
def test_nominal_roller_has_0p05_gap_to_only_the_smooth_carrier(role):
    ring = make_full_role_ring_reference(role)
    roller = make_roller(role, 0)
    assert roller.is_valid and len(roller.solids()) == 1
    assert _volume(ring.intersect(roller)) <= 1e-7
    assert ring.distance_to(roller) == pytest.approx(0.05, abs=1e-6)


@pytest.mark.parametrize("role", range(3))
def test_contact_pose_touches_carrier_race_and_not_teeth(role):
    roller = make_roller(role, 0, p.roller_axis_radius + p.roller_nominal_contact_gap)
    ring = make_full_role_ring_reference(role)
    race = make_carrier_race_band(role)
    assert ring.distance_to(roller) <= 1e-6
    assert race.distance_to(roller) <= 1e-6
    assert _volume(ring.intersect(roller)) <= 1e-7
    # The closest features are the running-land top and tooth-face bottom,
    # separated axially by 0.10 mm; the hub has the larger radial clearance.
    assert p.pinion_face_ranges[role][0] - p.contact_range(role)[1] >= 0.099


@pytest.mark.parametrize("role", range(3))
@pytest.mark.parametrize("delta", (0.0, 0.25))
def test_roller_core_clears_exact_swept_tooth_envelope(role, delta):
    # The hub overlaps the tooth Z range, so radial separation is the exact
    # swept-envelope criterion.  The broad running land is entirely below the
    # tooth face and is covered independently by the 0.10 mm axial assertion.
    hub_outer_radius = p.roller_axis_radius + delta + p.roller_hub_outer_diameter / 2.0
    assert p.tooth_tip_radius - hub_outer_radius >= 0.25 - 1e-9
    assert p.contact_range(role)[1] <= p.pinion_face_ranges[role][0] - 0.10 + 1e-9


@pytest.mark.parametrize("role", range(3))
def test_flange_capture_has_0p15_axial_relief_and_zero_carrier_intersection(role):
    roller = make_roller(role, 1)
    ring = make_full_role_ring_reference(role)
    assert _volume(ring.intersect(roller)) <= 1e-7
    z0, z1 = p.carrier_layers[role]
    lower, upper = p.roller_flange_ranges(role)
    assert z0 - lower[1] == pytest.approx(0.15)
    assert upper[0] - z1 == pytest.approx(0.15)


def test_all_nine_rollers_clear_all_three_fin_sweeps_and_seam_hardware():
    rollers = [make_roller(role, tower) for role in range(3) for tower in range(3)]
    obstacles = [make_fin_360_sweep(role) for role in range(3)]
    obstacles.extend(part for role in range(3) for part in make_seam_hardware(role, p))
    for roller in rollers:
        for obstacle in obstacles:
            assert _volume(roller.intersect(obstacle)) <= 1e-7


def test_rollers_clear_motor_pinions_shafts_and_unibody_yokes():
    rollers = [make_roller(role, tower) for role in range(3) for tower in range(3)]
    drive_parts = [part for role in range(3) for part in make_motor_station_parts(role)]
    for roller in rollers:
        for part in drive_parts:
            assert _volume(roller.intersect(part)) <= 1e-7, part.label


def test_stationary_roller_envelope_clears_all_fin_roots():
    assert p.roller_stationary_outer_radius <= 132.40 + 1e-9
    assert p.fin_root_radial_ranges[0][0] - p.roller_stationary_outer_radius >= 3.10 - 1e-9
    assert p.fin_root_radial_ranges[1][0] - p.roller_stationary_outer_radius >= 3.10 - 1e-9
    assert p.fin_blade_radial_ranges[2][0] - p.roller_stationary_outer_radius >= 4.80 - 1e-9


def test_four_quadrants_are_valid_65t_service_parts_with_continuous_race_reference():
    for role in range(3):
        quadrants = make_ring_quadrants(role)
        assert len(quadrants) == 4 and p.quadrant_teeth == 65
        assert all(q.is_valid and len(q.solids()) == 1 for q in quadrants)
        assert p.quadrant_count * p.quadrant_teeth == p.ring_teeth == 260
        assert p.rail_seam_step == pytest.approx(0.0)
        assert p.rail_seam_step <= 0.10
        assert p.joint_inner_radius > p.tooth_root_radius
        assert p.registration_dowel_radius > p.tooth_root_radius
        race = make_carrier_race_band(role)
        for angle in range(0, 360, 10):
            rad = radians(angle)
            x, y = (p.carrier_race_radius + 0.025) * cos(rad), (p.carrier_race_radius + 0.025) * sin(rad)
            probe = Location((x, y, sum(p.race_range(role)) / 2.0))
            assert race.distance_to(probe.position) <= 0.026


@pytest.mark.parametrize("tower", range(3))
def test_three_connected_towers_preserve_two_fixed_one_adjustable_mount(tower):
    yoke = make_roller_tower_yoke(tower)
    assert yoke.is_valid and len(yoke.solids()) == 1
    assert p.roller_tower_angles == (60.0, 180.0, 300.0)
    if tower == 2:
        assert "adjustable" in yoke.label
    else:
        assert "fixed" in yoke.label
