"""Executable design contract for isolated P2 refill / 8 mm experiment."""

from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from dataclasses import replace
from math import pi

from build123d import Axis, Location, Vector, import_step
import pytest

from pill_click.p1_hollow_magnetic_dispenser import (
    P1_HOLLOW_MAGNETIC_DISPENSER as p1,
    make_ported_outer_housing as make_p1_housing,
)
from pill_click.p2_bayonet_refill_8mm_rebound import (
    P2_BAYONET_REFILL_8MM_REBOUND as p,
    make_bayonet_cap,
    make_cover_m1_bore_tools,
    make_cover_m1_pick_bore_tools,
    make_cover_m2_bore_tools,
    make_cover_m2_pick_bore_tools,
    make_hollow_keyboard_container,
    make_inner_magnet_pick_bore_tools,
    make_inner_magnet_pocket_tools,
    make_inner_magnet_protection_bosses,
    make_magnetic_rear_cover,
    make_ported_outer_housing,
    make_pressed_assembly,
    make_print_bundle,
    make_refill_bore_tool,
    make_refill_neck_lugs,
    make_released_assembly,
    placed_hollow_keyboard_container,
    placed_bayonet_cap,
)


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models" / "p2_bayonet_refill_8mm_rebound"


def _intersection_volume(first, second):
    result = first & second
    return 0.0 if result is None else result.volume


def test_p1_geometry_and_motion_contract_remain_unchanged():
    p1_housing = make_p1_housing(p1)
    p2_housing = make_ported_outer_housing(p)
    assert p1_housing.volume == pytest.approx(p2_housing.volume, abs=1e-5)
    assert p1_housing.bounding_box().size == p2_housing.bounding_box().size
    assert (p.pressed_state, p.released_state, p.working_travel_y) == pytest.approx((3.4, 14.2, 10.8))
    assert (p.pill_port_width_x, p.pill_port_length_y, p.outer_port_length_y) == pytest.approx((31.8, 9.3, 6.8))
    assert p.pressed_port_overlap_y == pytest.approx(6.8)
    assert p.released_port_separation_y == pytest.approx(4.0)
    assert p.sagged_port_separation_y == pytest.approx(1.0)


def test_four_manifold_manufactured_parts_and_assemblies():
    parts = (make_ported_outer_housing(), make_hollow_keyboard_container(), make_magnetic_rear_cover(), make_bayonet_cap())
    assert len(make_print_bundle().children) == 4
    for part in parts:
        assert part.is_valid and len(part.solids()) == 1 and part.volume > 0
    for assembly in (make_pressed_assembly(), make_released_assembly()):
        assert len(assembly.children) == 4 and len(assembly.solids()) == 4


def test_exact_m1_m2_and_inner_seats_pick_bores_and_barriers():
    assert (p.fridge_magnet_pocket_diameter, p.rebound_magnet_pocket_diameter, p.inner_magnet_pocket_diameter) == pytest.approx((6.1, 8.1, 8.1))
    assert p.magnet_nominal_depth_y == pytest.approx(2.0)
    assert (p.cover_m1_seat_y[1] - p.cover_m1_seat_y[0], p.cover_m2_seat_y[1] - p.cover_m2_seat_y[0], p.inner_magnet_pocket_y[1] - p.inner_magnet_pocket_y[0]) == pytest.approx((2.1, 2.1, 2.1))
    assert p.cover_magnet_web_y == pytest.approx((-19.0, -16.4))
    assert p.cover_magnet_web_y[1] - p.cover_magnet_web_y[0] == pytest.approx(2.6)
    assert p.magnet_pick_bore_diameter == pytest.approx(1.4)
    assert p.fridge_pick_bore_centres_x == pytest.approx((-12.05, 12.05))
    assert p.rebound_pick_bore_centres_x == pytest.approx((-13.05, 13.05))
    assert p.inner_pick_bore_centres_x == pytest.approx((-13.05, 13.05))
    assert (p.cover_magnet_boss_diameter - p.rebound_magnet_pocket_diameter) / 2 >= 1.2
    for tool, diameter in (
        (make_cover_m1_bore_tools(), 6.1), (make_cover_m2_bore_tools(), 8.1),
        (make_inner_magnet_pocket_tools(), 8.1),
    ):
        assert tool.bounding_box().size.X == pytest.approx(17.0 + diameter)
    for tool in (make_cover_m1_pick_bore_tools(), make_cover_m2_pick_bore_tools(), make_inner_magnet_pick_bore_tools()):
        assert tool.bounding_box().size.Z == pytest.approx(1.4)
    assert p.inner_pick_medicine_barrier_y >= 2.0


def test_inner_rebound_seats_have_explicit_d11_protected_solids():
    bosses = make_inner_magnet_protection_bosses()
    pockets = make_inner_magnet_pocket_tools()
    assert bosses.is_valid and len(bosses.solids()) == 2
    assert bosses.bounding_box().size.X == pytest.approx(17.0 + 11.0)
    assert (p.inner_magnet_protection_diameter - p.inner_magnet_pocket_diameter) / 2 == pytest.approx(1.45)
    assert (p.inner_magnet_protection_diameter - p.inner_magnet_pocket_diameter) / 2 >= 1.2
    nominal_seat_volume = 2 * pi * (p.inner_magnet_pocket_diameter / 2) ** 2 * 2.1
    assert _intersection_volume(bosses, pockets) == pytest.approx(nominal_seat_volume, rel=1e-5)


def test_dense_motion_sweep_has_no_housing_or_rear_collision():
    body, housing, rear = make_hollow_keyboard_container(), make_ported_outer_housing(), make_magnetic_rear_cover()
    for index in range(p.motion_sweep_sample_count):
        state = p.pressed_state + index * p.motion_sweep_step_y
        moved = Location((0, p.inner_center_y(state), 0)) * body
        assert _intersection_volume(moved, housing) < 1e-7
        assert _intersection_volume(moved, rear) < 1e-7
    assert p.magnet_face_separation_y(p.pressed_state) == pytest.approx(1.4)
    assert p.magnet_face_separation_y(p.released_state) == pytest.approx(12.2)


def test_fail_closed_release_sag_and_no_peek_sampling():
    assert p.released_vertical_sag_envelope_y == pytest.approx(3.0)
    assert p.sagged_released_state == pytest.approx(11.2)
    assert p.sagged_port_separation_y >= p.minimum_sagged_seal_separation_y
    assert p.sagged_no_peek_margin_y >= p.minimum_sagged_no_peek_margin_y
    released = placed_hollow_keyboard_container(p.sagged_released_state)
    housing = make_ported_outer_housing()
    for x in [(-p.pill_port_width_x / 2 + 0.1) + i * (p.pill_port_width_x - 0.2) / 20 for i in range(21)]:
        for y in [p.outer_port_world_y[0] + 0.1 + i * (p.outer_port_length_y - 0.2) / 12 for i in range(13)]:
            assert released.is_inside(Vector(x, y, -16.25))
    inner_world = p.inner_port_world_y(p.sagged_released_state)
    for x in (-12.0, 0.0, 12.0):
        for y in (inner_world[0] + 0.2, sum(inner_world) / 2, inner_world[1] - 0.2):
            assert housing.is_inside(Vector(x, y, -18.55))


def test_refill_bore_connects_hopper_and_preserves_printable_shell():
    bore = make_refill_bore_tool()
    assert bore.bounding_box().size.X == pytest.approx(16.0)
    assert bore.bounding_box().size.Z == pytest.approx(16.0)
    body = make_hollow_keyboard_container()
    for y in (p.cavity_front_y, p.key_local_y[1], p.refill_neck_front_y - 0.1):
        assert not body.is_inside(Vector(0, y, 0))
    assert p.standard_shell_thickness == pytest.approx(3 * p.nozzle_diameter)


def test_bayonet_cap_fit_locked_unlocked_and_print_minima():
    assert p.refill_clear_bore_diameter == pytest.approx(16.0)
    assert (p.refill_neck_outer_diameter, p.cap_outer_diameter, p.cap_internal_running_diameter) == pytest.approx((20.0, 26.0, 20.6))
    assert p.cap_radial_clearance_per_side == pytest.approx(0.3)
    assert p.cap_axial_clearance_y == pytest.approx(0.25)
    assert p.cap_rotation_degrees == pytest.approx(90.0)
    assert p.cap_locked_axial_overlap_y == pytest.approx(1.35)
    assert p.cap_locked_axial_overlap_y > 0
    assert p.cap_ramp_angle_degrees <= 45.0
    assert p.cap_shell_radial_thickness - p.cap_radial_clearance_per_side >= p.cap_minimum_wall_after_slots
    assert p.cap_top_thickness_y >= 5 * p.nozzle_diameter
    assert p.refill_neck_lug_axial_thickness_y >= 4 * p.nozzle_diameter
    assert p.cap_rotation_stop_thickness == pytest.approx(3 * p.nozzle_diameter)
    assert p.cap_lead_in_chamfer >= p.nozzle_diameter


def test_neck_lugs_are_real_opposed_30_degree_annular_sectors():
    lugs = make_refill_neck_lugs()
    assert lugs.is_valid and len(lugs.solids()) == 2
    outer = p.neck_lug_outer_radius
    inner = p.refill_neck_outer_diameter / 2 - p.refill_neck_lug_body_overlap
    expected = 2 * pi * (outer ** 2 - inner ** 2) * (p.refill_neck_lug_arc_degrees / 360) * p.refill_neck_lug_axial_thickness_y
    assert lugs.volume == pytest.approx(expected, rel=1e-6)


def test_cap_lead_in_is_cut_into_real_geometry():
    shallow = make_bayonet_cap(replace(p, cap_lead_in_chamfer=0.10))
    nominal = make_bayonet_cap()
    assert nominal.volume < shallow.volume
    assert shallow.volume - nominal.volume > 1.0


def test_actual_cap_solids_clear_rotation_and_removal_but_block_pull_and_overrotation():
    inner = placed_hollow_keyboard_container(p.released_state)
    cap_y = p.inner_center_y(p.released_state) + p.key_local_y[1]
    for angle_index in range(13):
        angle = -angle_index * p.cap_slot_sampling_degrees
        cap = Location((0, cap_y, 0)) * make_bayonet_cap().rotate(Axis.Y, angle)
        assert _intersection_volume(cap, inner) < 1e-7

    unlocked = placed_bayonet_cap(p.released_state, locked=False)
    for pull_y in (0.0, 1.0, 2.0, 4.0, 8.0, 12.0):
        assert _intersection_volume(Location((0, pull_y, 0)) * unlocked, inner) < 1e-7

    locked = placed_bayonet_cap(p.released_state, locked=True)
    assert _intersection_volume(locked, inner) < 1e-7
    assert p.cap_locked_axial_overlap_y > 0
    assert _intersection_volume(Location((0, 0.5, 0)) * locked, inner) > 0.05

    overrotated = Location((0, cap_y, 0)) * make_bayonet_cap().rotate(Axis.Y, -95.0)
    assert _intersection_volume(overrotated, inner) > 1.0


def test_generated_steps_reopen_and_3mf_has_four_named_meshes():
    step_names = ("p2_released.step", "p2_pressed.step", "p2_hopper_cutaway.step", "p2_cap_locked.step", "p2_cap_exploded.step")
    for name in step_names:
        path = MODEL_DIR / name
        assert path.exists()
        reopened = import_step(path)
        assert reopened.is_valid and len(reopened.solids()) >= 1
    bundle = MODEL_DIR / "print" / "p2_four_part_test_bundle.3mf"
    assert bundle.exists()
    with ZipFile(bundle) as archive:
        model_name = next(name for name in archive.namelist() if name.endswith("3dmodel.model"))
        root = ET.fromstring(archive.read(model_name))
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    # 3MF assemblies carry one component-only build object in addition to the
    # actual mesh resources.  The print contract is exactly four independently
    # selectable meshes.
    objects = root.findall(".//m:resources/m:object", ns)
    mesh_objects = [obj for obj in objects if obj.find("m:mesh", ns) is not None]
    assert len(mesh_objects) == 4
    assert {obj.attrib.get("name") for obj in mesh_objects} == {
        "outer_housing",
        "integrated_inner",
        "rear_cover",
        "bayonet_cap",
    }
