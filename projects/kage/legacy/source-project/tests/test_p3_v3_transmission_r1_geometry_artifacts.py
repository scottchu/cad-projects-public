"""Geometry and generated-artifact gates for P3 V3 transmission R1."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import trimesh
from OCP.BRepCheck import BRepCheck_Analyzer
from build123d import Align, Axis, Cylinder, Location, import_step

import p3_v3_transmission_r1_geometry as g
from p3_v3_transmission_r1_spec import P3_V3_TRANSMISSION_R1 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_transmission_r1"


def _valid_single_solid(shape):
    assert shape.is_valid
    assert BRepCheck_Analyzer(shape.wrapped).IsValid()
    assert len(shape.solids()) == 1
    assert shape.volume > 0.0


def _boxes_overlap(a, b, tolerance=1e-7):
    aa, bb = a.bounding_box(), b.bounding_box()
    return all(
        getattr(aa.min, axis) < getattr(bb.max, axis) - tolerance
        and getattr(bb.min, axis) < getattr(aa.max, axis) - tolerance
        for axis in "XYZ"
    )


def test_real_16t_miter_pair_has_periodic_tooth_topology_and_clean_mesh():
    horizontal, vertical = g.make_miter_pair()
    for gear in (horizontal, vertical):
        _valid_single_solid(gear)
        assert "ENVELOPE" not in gear.label
        assert p.miter_topology_has_teeth(
            tip_vertices=len(gear.edges()),
            tooth_side_faces=len(gear.faces()),
            periodic_faces=min(len(gear.faces()), p.miter_teeth),
        )
        assert len(gear.faces()) >= 100
        assert len(gear.edges()) >= 290
    assert g.positive_intersection_volume(horizontal, vertical) == pytest.approx(0.0)
    assert 0.02 <= horizontal.distance_to(vertical) <= p.miter_mesh_backlash


def test_real_motor_shaft_is_full_4x7_and_engages_bored_horizontal_gear_at_adjustment_extremes():
    horizontal, _ = g.make_miter_pair()
    shaft = g.make_motor_shaft()
    assert shaft.bounding_box().min.X == pytest.approx(111.25)
    assert shaft.bounding_box().max.X == pytest.approx(118.25)
    assert shaft.bounding_box().size.X == pytest.approx(7.0)
    assert shaft.bounding_box().size.Y == pytest.approx(4.0)
    assert shaft.bounding_box().size.Z == pytest.approx(p.motor_shaft_across_flat)
    assert "D_shaft" in shaft.label
    for adjustment in (-p.motor_adjustment, 0.0, p.motor_adjustment):
        shifted = shaft.moved(Location((adjustment, 0.0, 0.0)))
        assert g.positive_intersection_volume(shifted, horizontal) == pytest.approx(0.0)
        assert shifted.distance_to(horizontal) == pytest.approx(0.05, abs=0.002)
        assert shifted.bounding_box().max.X > horizontal.bounding_box().min.X + 1.0


def test_vertical_shaft_two_mr84_stack_and_role_interfaces_are_coaxial_and_retained():
    shaft = g.make_output_shaft()
    _, vertical = g.make_miter_pair()
    assert shaft.bounding_box().size.Z == pytest.approx(40.0)
    assert shaft.bounding_box().size.X == pytest.approx(4.0)
    assert shaft.bounding_box().size.Y == pytest.approx(3.5)
    assert "D_steel_shaft" in shaft.label
    assert shaft.distance_to(vertical) == pytest.approx(0.05, abs=0.002)
    assert g.positive_intersection_volume(shaft, vertical) == pytest.approx(0.0)
    for which, expected in (("lower", p.lower_bearing_range), ("upper", p.upper_bearing_range)):
        bearing = g.make_bearing(which)
        _valid_single_solid(bearing)
        assert (bearing.bounding_box().min.Z, bearing.bounding_box().max.Z) == pytest.approx(expected)
        assert shaft.distance_to(bearing) == pytest.approx(0.0, abs=1e-7)
        assert g.positive_intersection_volume(shaft, bearing) == pytest.approx(0.0)
    # The clamped bevel hub is 0.10 mm below the upper bearing; the role
    # spacer begins 0.05 mm above it.  The retained stack remains in the
    # reviewed 0.05-0.15 mm endplay window.
    assert p.upper_bearing_range[0] - p.miter_vertical_hub_top_z == pytest.approx(0.10)
    assert p.spacer_axial_relief == pytest.approx(0.05)
    assert sum((0.10, p.spacer_axial_relief)) == pytest.approx(p.endplay_range[1])


def test_vertical_miter_output_pinion_and_lower_collar_have_matching_d_bores():
    _, vertical = g.make_miter_pair()
    pinion = g.make_output_pinion(p.selected_role)
    collar = g.make_lower_clamp_collar()
    probes = (
        (vertical, -20.0, p.miter_vertical_hub_top_z + 0.2),
        (pinion, p.pinion_face_range(p.selected_role)[0] - 0.2, p.pinion_face_range(p.selected_role)[1] + 0.2),
        (collar, p.lower_collar_z[0] - 0.2, p.lower_collar_z[1] + 0.2),
    )
    for body, z0, z1 in probes:
        d_probe = g._d_prism_z(
            p.output_axis_radius,
            z0,
            z1,
            p.output_pinion_bore_diameter,
            p.output_pinion_bore_across_flat,
        )
        round_probe = Cylinder(
            p.output_pinion_bore_diameter / 2.0,
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((p.output_axis_radius, 0.0, z0)))
        assert g.positive_intersection_volume(d_probe, body) == pytest.approx(0.0)
        assert g.positive_intersection_volume(round_probe, body) > 0.0


def test_lower_thrust_sleeve_and_clamp_collar_close_the_axial_retention_stack():
    shim = g.make_lower_miter_shim()
    collar = g.make_lower_clamp_collar()
    _valid_single_solid(shim)
    _valid_single_solid(collar)
    assert shim.bounding_box().min.Z == pytest.approx(p.lower_bearing_range[1] + 0.05)
    assert shim.bounding_box().max.Z <= p.miter_vertical_hub_top_z - 2.0
    assert (collar.bounding_box().min.Z, collar.bounding_box().max.Z) == pytest.approx(
        p.lower_collar_z
    )
    assert p.lower_collar_engagement >= 2.0
    assert g.positive_intersection_volume(shim, g.make_miter_pair()[0]) == pytest.approx(0.0)
    assert g.positive_intersection_volume(collar, g.make_bearing("lower")) == pytest.approx(0.0)


def test_three_explicit_m2_grub_screws_seat_on_output_d_flat_through_tap_pilots():
    screws = g.make_set_screw_references(p.selected_role)
    assert len(screws) == 3
    screw_labels = [s.label for s in screws]
    assert not any("horizontal_D_hub" in label for label in screw_labels)
    assert any("vertical_miter_hub" in label for label in screw_labels)
    assert any("minute_output_pinion" in label for label in screw_labels)
    assert any("lower_clamp_collar" in label for label in screw_labels)
    assert all(s.is_valid and len(s.solids()) == 1 for s in screws)
    shaft = g.make_output_shaft()
    _, vertical = g.make_miter_pair()
    pinion = g.make_output_pinion(p.selected_role)
    collar = g.make_lower_clamp_collar()
    for screw, hub in zip(screws, (vertical, pinion, collar)):
        assert screw.bounding_box().size.X == pytest.approx(p.m2_tap_pilot_diameter)
        assert screw.bounding_box().size.Z == pytest.approx(p.m2_tap_pilot_diameter)
        assert screw.distance_to(shaft) == pytest.approx(0.0, abs=1e-7)
        assert g.positive_intersection_volume(screw, shaft) == pytest.approx(0.0)
        assert g.positive_intersection_volume(screw, hub) == pytest.approx(0.0)
        # A 0.02 mm larger core must bite the printed wall, proving this is a
        # 1.60 mm tap pilot rather than the rejected 2.20 mm clearance tunnel.
        box = screw.bounding_box()
        larger_core = Cylinder(
            p.m2_tap_pilot_diameter / 2.0 + 0.01,
            box.max.Y - box.min.Y,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).rotate(Axis.X, 90.0).moved(
            Location(((box.min.X + box.max.X) / 2.0, (box.min.Y + box.max.Y) / 2.0, (box.min.Z + box.max.Z) / 2.0))
        )
        assert g.positive_intersection_volume(larger_core, hub) > 0.0
    assembly = g.make_assembled()
    labels = [child.label for child in assembly.children]
    assert sum("purchased_M2_grub_screw" in label for label in labels) == 3
    assert any("lower_D_collar" in label for label in labels)
    assert any("lower_bearing_to_miter_drive_spacer" in label for label in labels)


@pytest.mark.parametrize("role", range(3))
def test_true_259t_arc_16t_output_pinion_and_role_spacer_match_each_carrier_plane(role):
    arc = g.make_ring_arc(role)
    pinion = g.make_output_pinion(role)
    spacer = g.make_role_spacer(role)
    _valid_single_solid(arc)
    _valid_single_solid(pinion)
    _valid_single_solid(spacer)
    assert len(arc.faces()) >= 80
    assert len(pinion.faces()) >= 100
    assert g.positive_intersection_volume(arc, pinion) == pytest.approx(0.0)
    assert 0.05 <= arc.distance_to(pinion) <= 0.25
    assert (pinion.bounding_box().min.Z, pinion.bounding_box().max.Z) == pytest.approx(
        p.pinion_face_range(role)
    )
    assert spacer.bounding_box().min.Z == pytest.approx(p.spacer_axial_relief)
    assert spacer.bounding_box().max.Z == pytest.approx(p.pinion_face_range(role)[0])


@pytest.mark.parametrize("role", range(3))
@pytest.mark.parametrize("offset", (-p.slider_half_stroke, 0.0, p.slider_half_stroke))
def test_true_ring_arc_is_captured_for_backlash_stroke_without_tooth_or_rail_collision(role, offset):
    carriage = g.make_ring_arc_carriage(role, offset)
    lower, upper = g.make_arc_slider_rails(role)
    pinion = g.make_output_pinion(role)
    _valid_single_solid(carriage)
    _valid_single_solid(lower)
    _valid_single_solid(upper)
    assert g.positive_intersection_volume(carriage, pinion) == pytest.approx(0.0)
    assert g.positive_intersection_volume(carriage, lower) == pytest.approx(0.0)
    assert g.positive_intersection_volume(carriage, upper) == pytest.approx(0.0)
    if offset:
        assert carriage.distance_to(lower) == pytest.approx(0.0, abs=1e-7)
    else:
        assert carriage.distance_to(lower) == pytest.approx(p.slider_half_stroke)


def test_nominal_assembled_occurrences_have_no_positive_volume_collisions():
    assembly = g.make_assembled()
    assert assembly.is_valid
    assert len(assembly.children) == 42
    checked = 0
    for index, first in enumerate(assembly.children):
        for second in assembly.children[index + 1 :]:
            if not _boxes_overlap(first, second):
                continue
            checked += 1
            volume = g.positive_intersection_volume(first, second)
            intentional_threads = (
                "M3_saddle_clamp_bolt" in first.label
                and "M3_external_nut" in second.label
            ) or (
                "M3_saddle_clamp_bolt" in second.label
                and "M3_external_nut" in first.label
            )
            if intentional_threads:
                assert volume > 0.0
            else:
                assert volume <= 1e-6, (first.label, second.label)
    assert checked >= 70


def test_both_outer_race_bearing_retainers_are_fastened_and_clear_rotating_parts():
    assembly = g.make_assembled()
    labels = [child.label for child in assembly.children]
    assert sum("bearing_service_retainer" in label for label in labels) == 2
    assert sum("bearing_retainer_screw" in label for label in labels) == 4
    shaft = g.make_output_shaft()
    _, vertical = g.make_miter_pair()
    for which in ("lower", "upper"):
        retainer = g.make_bearing_retainer(which)
        _valid_single_solid(retainer)
        assert g.positive_intersection_volume(retainer, shaft) == pytest.approx(0.0)
        assert g.positive_intersection_volume(retainer, vertical) == pytest.approx(0.0)
        assert retainer.distance_to(shaft) >= 1.0
        screws = g.make_bearing_retainer_screw_references(which)
        assert len(screws) == 2
        assert all(g.positive_intersection_volume(screw, retainer) == pytest.approx(0.0) for screw in screws)
    assert p.lower_bearing_retainer_pilot_engagement >= 1.50
    assert p.upper_bearing_retainer_pilot_engagement >= 1.50


def test_arc_lower_guide_has_positive_chassis_load_path_and_upper_retainer_has_two_screws():
    lower, upper = g.make_arc_slider_rails(p.selected_role)
    chassis = g.make_fixed_chassis(role_index=p.selected_role)
    _valid_single_solid(chassis)
    assert g.positive_intersection_volume(chassis, lower) > 10.0
    assert len(g.make_arc_retainer_screw_references(p.selected_role)) == 2
    assembly_labels = [child.label for child in g.make_assembled().children]
    assert not any(label == lower.label for label in assembly_labels)
    assert upper.label in assembly_labels
    assert sum("upper_slider_retainer_screw" in label for label in assembly_labels) == 2


def test_four_external_m3_saddle_clamp_stacks_are_explicit_and_clear_motor():
    hardware = g.make_motor_saddle_clamp_hardware()
    assert len(hardware) == 16
    labels = [item.label for item in hardware]
    assert sum("clamp_bolt" in label for label in labels) == 4
    assert sum("lower_washer" in label for label in labels) == 4
    assert sum("upper_washer" in label for label in labels) == 4
    assert sum("external_nut" in label for label in labels) == 4
    motor = g.make_motor_body()
    assert all(g.positive_intersection_volume(item, motor) == pytest.approx(0.0) for item in hardware)
    chassis = g.make_fixed_chassis()
    saddle = g.make_motor_saddle()
    for stack in range(4):
        bolt, lower_washer, upper_washer, nut = hardware[4 * stack : 4 * stack + 4]
        assert bolt.bounding_box().min.Z == pytest.approx(-29.50)
        assert bolt.bounding_box().max.Z == pytest.approx(p.saddle_clamp_shank_z[1])
        assert lower_washer.bounding_box().max.Z == pytest.approx(chassis.bounding_box().min.Z)
        assert lower_washer.distance_to(chassis) == pytest.approx(0.0, abs=1e-7)
        assert bolt.distance_to(lower_washer) == pytest.approx(0.0, abs=1e-7)
        assert upper_washer.bounding_box().min.Z == pytest.approx(-22.15)
        assert upper_washer.distance_to(saddle) == pytest.approx(0.0, abs=1e-7)
        assert nut.bounding_box().min.Z == pytest.approx(upper_washer.bounding_box().max.Z)
        assert nut.distance_to(upper_washer) == pytest.approx(0.0, abs=1e-7)
        threaded_engagement = min(bolt.bounding_box().max.Z, nut.bounding_box().max.Z) - max(
            p.saddle_clamp_shank_z[0], nut.bounding_box().min.Z
        )
        assert threaded_engagement == pytest.approx(2.40)
        assert g.positive_intersection_volume(bolt, nut) > 0.0
        assert bolt.bounding_box().min.Z < chassis.bounding_box().min.Z
        assert bolt.bounding_box().max.Z > -22.15


@pytest.mark.parametrize("name", ("assembled", "service_exploded", "print_components"))
def test_exact_wrappers_and_generated_step_are_valid(name):
    wrapper = MODEL_ROOT / f"p3_v3_r1_{name}.step.py"
    spec = importlib.util.spec_from_file_location(f"p3_v3_r1_{name}_wrapper", wrapper)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    generated = module.gen_step()
    assert generated.is_valid and generated.volume > 0.0
    artifact = import_step(MODEL_ROOT / f"p3_v3_r1_{name}.step")
    assert artifact.is_valid
    assert BRepCheck_Analyzer(artifact.wrapped).IsValid()
    assert artifact.volume > 0.0


def test_manifest_keeps_all_physical_gates_pending_and_documents_assembly_order():
    manifest = json.loads((MODEL_ROOT / "p3_v3_r1_manifest.json").read_text())
    assert len(manifest["assembly_order"]) >= 10
    assert manifest["transmission"]["output_axis_radius_mm"] == pytest.approx(121.5)
    assert manifest["purchased_references"]["grub_screws"] == "3 x M2"
    assert manifest["purchased_references"]["bearing_retainer_screws"] == "4 x M2"
    assert manifest["purchased_references"]["slider_retainer_screws"] == "2 x M2"
    assert "4 x M3" in manifest["purchased_references"]["saddle_clamps"]
    assert manifest["purchased_references"]["shaft"] == "4 x 40 mm D steel shaft, 3.5 mm across-flat"
    assert manifest["transmission"]["motor_bore"] == "4.10 mm D bore, 3.60 mm across-flat"
    assert manifest["transmission"]["m2_tap_pilot_mm"] == pytest.approx(1.6)
    assert "+/-0.08 mm" in manifest["transmission"]["ring_arc_fixture"]
    assert manifest["print_artifact_kind"] == "functional-position catalog; not a slicer plate"
    assert len(manifest["individual_print_files"]) >= 20
    for relative in manifest["individual_print_files"]:
        artifact = MODEL_ROOT / relative
        assert artifact.exists() and artifact.stat().st_size > 0
    assert set(manifest["physical_gates"].values()) == {"PENDING"}


def test_exported_step_contains_both_bearing_retainer_names():
    step_text = (MODEL_ROOT / "p3_v3_r1_assembled.step").read_text(errors="ignore")
    assert "p3_v3_r1_lower_bearing_service_retainer" in step_text
    assert "p3_v3_r1_upper_bearing_service_retainer" in step_text


def test_every_individual_stl_is_one_watertight_positive_nondegenerate_component():
    manifest = json.loads((MODEL_ROOT / "p3_v3_r1_manifest.json").read_text())
    stl_paths = [MODEL_ROOT / relative for relative in manifest["individual_print_files"] if relative.endswith(".stl")]
    assert len(stl_paths) == 12
    for path in stl_paths:
        mesh = trimesh.load_mesh(path, process=True, force="mesh")
        components = mesh.split(only_watertight=False)
        assert len(components) == 1, path.name
        assert mesh.is_watertight, path.name
        assert mesh.volume > 0.0, path.name
        assert mesh.nondegenerate_faces().all(), path.name
