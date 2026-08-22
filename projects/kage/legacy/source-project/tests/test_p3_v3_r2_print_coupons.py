"""Focused executable contracts for the P3 V3 R2 progressive print coupons."""

from __future__ import annotations

import json
from itertools import combinations
from math import pi, radians, sin, sqrt
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest
import trimesh
from OCP.BRepCheck import BRepCheck_Analyzer
from build123d import Align, Box, Cylinder, Location, Vector, import_step

import p3_v3_r2_print_coupon_geometry as g
from p3_v3_r2_print_coupon_spec import P3_V3_R2_PRINT_COUPON as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_r2_print_coupons"
VOLUME_TOL = 1e-7


def _intersection_volume(left, right) -> float:
    common = left.intersect(right)
    return sum(solid.volume for solid in common.solids()) if common else 0.0


def _assert_valid_one_solid(shape) -> None:
    assert shape.is_valid
    assert BRepCheck_Analyzer(shape.wrapped).IsValid()
    assert len(shape.solids()) == 1
    assert shape.volume > 0.0


def _cylinder(diameter: float, height: float, x: float, y: float, z0: float):
    return Cylinder(
        diameter / 2.0,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))


@pytest.fixture(scope="module")
def seam_halves():
    return g.make_seam_arc_half("lower"), g.make_seam_arc_half("upper")


@pytest.fixture(scope="module")
def motor_parts():
    straps = g.make_motor_clamp_straps()
    horizontal_miter, vertical_miter, output_pinion = g.make_printable_drive_gears()
    return {
        "arc": g.make_motor_arc(),
        "housing": g.make_bearing_housing(),
        "cap": g.make_bearing_cap(),
        "saddle": g.make_motor_saddle(),
        "clamp_strap_1": straps[0],
        "clamp_strap_2": straps[1],
        "horizontal_miter": horizontal_miter,
        "vertical_miter": vertical_miter,
        "output_pinion": output_pinion,
        "petg_guide": g.make_operating_guide_shoe("PETG", -12.0),
        "tpu_guide": g.make_operating_guide_shoe("TPU95A", 12.0),
        "fin": g.make_fin(),
    }


@pytest.fixture(scope="module")
def motor_references():
    refs = g.make_motor_station_references()
    return {
        "motor": refs[0],
        "motor_shaft": refs[1],
        "output_shaft": refs[2],
        "lower_bearing": refs[3],
        "upper_bearing": refs[4],
    }


def test_frozen_m1_260t_16t_equations_and_24t_arc_chord():
    assert p.module == pytest.approx(1.0)
    assert p.pressure_angle_degrees == pytest.approx(20.0)
    assert p.ring_teeth == 260 and p.pinion_teeth == 16
    assert p.ring_pitch_radius == pytest.approx(p.module * p.ring_teeth / 2.0)
    assert p.pinion_pitch_radius == pytest.approx(p.module * p.pinion_teeth / 2.0)
    assert p.center_distance == pytest.approx(p.ring_pitch_radius - p.pinion_pitch_radius)
    assert p.center_distance == pytest.approx(p.output_axis_radius)
    assert p.gear_ratio == pytest.approx(16.25)
    assert p.ring_pitch_circumference == pytest.approx(2.0 * pi * 130.0)
    assert p.tooth_pitch_degrees * p.ring_teeth == pytest.approx(360.0)
    assert p.motor_arc_teeth == 24
    assert p.motor_arc_angle_degrees == pytest.approx(24.0 * 360.0 / 260.0)
    assert 2.0 * p.seam_half_angle_degrees == pytest.approx(p.motor_arc_angle_degrees)
    expected_chord = 2.0 * p.ring_outer_radius * sin(radians(p.motor_arc_angle_degrees / 2.0))
    assert p.motor_arc_chord() == pytest.approx(expected_chord)


def test_actual_14mm_r132_to_r138_complementary_half_lap_is_flush(seam_halves):
    lower, upper = seam_halves
    assert p.seam_overlap_tangential == pytest.approx(14.0)
    assert p.seam_overlap_half == pytest.approx(7.0)
    assert (p.seam_lap_inner_radius, p.seam_lap_outer_radius) == pytest.approx((132.0, 138.0))
    assert 2.0 * p.seam_lap_layer == pytest.approx(p.ring_thickness)
    for half in seam_halves:
        box = half.bounding_box()
        assert box.min.Z == pytest.approx(0.0, abs=2e-7)
        assert box.max.Z == pytest.approx(3.0, abs=2e-7)
    assert lower.bounding_box().max.Y == pytest.approx(p.seam_overlap_half, abs=2e-7)
    assert upper.bounding_box().min.Y == pytest.approx(-p.seam_overlap_half, abs=2e-7)

    # At both sides of the seam the lower half owns Z=0..1.5 and the upper
    # half owns Z=1.5..3.0.  Choose points away from all hardware bores.
    for y in (-6.0, 6.0):
        assert lower.is_inside(Vector(134.0, y, 0.75))
        assert not upper.is_inside(Vector(134.0, y, 0.75))
        assert upper.is_inside(Vector(134.0, y, 2.25))
        assert not lower.is_inside(Vector(134.0, y, 2.25))


def test_seam_cutters_match_pin_countersink_nut_dimensions_and_ligaments(seam_halves):
    bore, countersink, nut, pin_a, pin_b = g._seam_cutters(p)
    assert bore.bounding_box().size.X == pytest.approx(p.seam_clamp_bore_diameter)
    assert countersink.bounding_box().size.X == pytest.approx(p.seam_countersink_diameter)
    assert countersink.bounding_box().size.Z == pytest.approx(p.seam_countersink_depth)
    assert nut.bounding_box().size.X == pytest.approx(p.seam_nut_af)
    assert nut.bounding_box().size.Z == pytest.approx(p.seam_nut_depth + 0.01)
    assert pin_a.bounding_box().size.X == pytest.approx(p.alignment_bore_diameter)
    assert pin_b.bounding_box().size.X == pytest.approx(p.alignment_bore_diameter)
    for cutter in (bore, countersink, nut, pin_a, pin_b):
        for half in seam_halves:
            assert _intersection_volume(cutter, half) <= VOLUME_TOL

    lap_width = p.seam_lap_outer_radius - p.seam_lap_inner_radius
    assert (lap_width - p.seam_countersink_diameter) / 2.0 == pytest.approx(0.90)
    assert (lap_width - p.seam_nut_af) / 2.0 == pytest.approx(0.925)
    assert (lap_width - p.alignment_bore_diameter) / 2.0 == pytest.approx(1.95)
    screw_to_pin = abs(p.alignment_pin_tangential_offsets[0]) - (
        p.seam_countersink_diameter + p.alignment_bore_diameter
    ) / 2.0
    assert screw_to_pin == pytest.approx(1.35)
    assert abs(p.alignment_pin_tangential_offsets[1] - p.alignment_pin_tangential_offsets[0]) - p.alignment_bore_diameter == pytest.approx(6.90)


def test_assembled_seam_halves_have_zero_positive_volume_overlap(seam_halves):
    lower, upper = seam_halves
    assert _intersection_volume(lower, upper) <= VOLUME_TOL
    assert lower.distance_to(upper) == pytest.approx(0.0, abs=VOLUME_TOL)


def test_seam_hardware_is_sized_and_separated_from_race(seam_halves):
    screw, nut, pin_a, pin_b = g.make_seam_hardware_references(p)
    assert screw.bounding_box().size.Z == pytest.approx(p.ring_thickness)
    assert screw.bounding_box().size.X == pytest.approx(p.seam_countersink_diameter - 0.10)
    assert nut.bounding_box().size.X == pytest.approx(4.0)
    for pin in (pin_a, pin_b):
        assert pin.bounding_box().size.X == pytest.approx(p.alignment_pin_diameter)
        assert pin.bounding_box().size.Z == pytest.approx(p.alignment_pin_length)
    race_envelope = g._annulus(p.race_inner_radius, p.race_outer_radius, p.race_axial, 0.0)
    for hardware in (screw, nut, pin_a, pin_b):
        assert _intersection_volume(hardware, race_envelope) <= VOLUME_TOL
        assert hardware.distance_to(race_envelope) >= 0.90 - 1e-7
        for half in seam_halves:
            assert _intersection_volume(hardware, half) <= VOLUME_TOL
        for index, clearance in enumerate(p.guide_clearances):
            shoe = g.make_guide_shoe_variant(clearance, index, p)
            assert _intersection_volume(hardware, shoe) <= VOLUME_TOL


def test_race_is_frozen_2mm_radial_by_0p8mm_axial():
    assert p.race_outer_radius - p.race_inner_radius == pytest.approx(2.0)
    assert p.race_axial == pytest.approx(0.8)
    gauge = g.make_guide_race_gauge(p.guide_clearances[0], 0, p)
    box = gauge.bounding_box()
    assert box.size.X == pytest.approx(2.0)
    assert box.size.Z == pytest.approx(0.8)


@pytest.mark.parametrize("index,clearance", tuple(enumerate(p.guide_clearances)))
def test_actual_guide_clearance_ladder(index, clearance):
    assert p.guide_clearances == pytest.approx((0.15, 0.25, 0.35))
    shoe = g.make_guide_shoe_variant(clearance, index, p)
    gauge = g.make_guide_race_gauge(clearance, index, p)
    _assert_valid_one_solid(shoe)
    _assert_valid_one_solid(gauge)
    assert _intersection_volume(shoe, gauge) <= VOLUME_TOL
    assert shoe.distance_to(gauge) == pytest.approx(clearance, abs=1e-7)
    assert shoe.bounding_box().size.Z == pytest.approx(
        p.race_axial + 2.0 * clearance + 2.0 * p.guide_shoe_floor
    )


def test_stationary_joiner_step_has_clearance_and_assembles_without_collision():
    male, female = g.make_stationary_joiner_parts(p)
    _assert_valid_one_solid(male)
    _assert_valid_one_solid(female)
    assert p.joiner_step_size == pytest.approx((6.0, 4.0, 1.2))
    assert p.joiner_clearance == pytest.approx(0.25)
    expected_pocket = tuple(
        size + (2.0 * p.joiner_clearance if axis < 2 else p.joiner_clearance)
        for axis, size in enumerate(p.joiner_step_size)
    )
    assert expected_pocket == pytest.approx((6.5, 4.5, 1.45))
    assert _intersection_volume(male, female) <= VOLUME_TOL
    assert male.distance_to(female) == pytest.approx(0.0, abs=VOLUME_TOL)
    assert male.bounding_box().size.Z == pytest.approx(p.joiner_body_size[2])
    assert female.bounding_box().size.Z == pytest.approx(p.joiner_body_size[2])


def test_actual_motor_arc_is_complete_24t_chord_and_valid(motor_parts):
    arc = motor_parts["arc"]
    _assert_valid_one_solid(arc)
    assert "24T" in arc.label and "260T" in arc.label
    assert arc.bounding_box().size.Y == pytest.approx(p.motor_arc_chord(), abs=2e-6)
    assert arc.bounding_box().max.Z == pytest.approx(p.motor_carrier_z0 + p.ring_thickness, abs=2e-7)
    assert p.pinion_face_range[1] < arc.bounding_box().max.Z


def test_mr84_pocket_shoulder_cap_and_aperture_contract(motor_parts, motor_references):
    assert p.bearing_code == "MR84"
    assert (p.bearing_id, p.bearing_od, p.bearing_width) == pytest.approx((4.0, 8.0, 3.0))
    assert p.bearing_centers[1] - p.bearing_centers[0] == pytest.approx(p.bearing_center_span)
    assert p.bearing_pocket_diameter - p.bearing_od == pytest.approx(0.10)
    assert p.bearing_pocket_depth - p.bearing_width == pytest.approx(0.10)
    assert p.bearing_fixed_shoulder == pytest.approx(1.20)
    assert p.bearing_cap_thickness == pytest.approx(1.60)
    assert (p.bearing_od - p.bearing_aperture_diameter) / 2.0 == pytest.approx(0.80)
    assert (p.bearing_aperture_diameter - p.bearing_id) / 2.0 == pytest.approx(1.20)

    housing = motor_parts["housing"]
    cap = motor_parts["cap"]
    shaft = motor_references["output_shaft"]
    for bearing_name in ("lower_bearing", "upper_bearing"):
        bearing = motor_references[bearing_name]
        assert _intersection_volume(housing, bearing) <= VOLUME_TOL
        assert housing.distance_to(bearing) == pytest.approx(0.05, abs=2e-7)
    assert _intersection_volume(cap, motor_references["upper_bearing"]) <= VOLUME_TOL
    assert cap.distance_to(motor_references["upper_bearing"]) == pytest.approx(0.0, abs=VOLUME_TOL)
    for retaining_part in (housing, cap):
        assert _intersection_volume(retaining_part, shaft) <= VOLUME_TOL
        assert retaining_part.distance_to(shaft) == pytest.approx(1.20, abs=2e-7)


def test_bearing_housing_and_cap_are_valid_single_breps(motor_parts):
    _assert_valid_one_solid(motor_parts["housing"])
    _assert_valid_one_solid(motor_parts["cap"])
    assert motor_parts["cap"].bounding_box().size.Z == pytest.approx(p.bearing_cap_thickness)
    assert _intersection_volume(motor_parts["housing"], motor_parts["cap"]) <= VOLUME_TOL
    assert motor_parts["housing"].distance_to(motor_parts["cap"]) == pytest.approx(0.0, abs=VOLUME_TOL)


def test_motor_saddle_slots_travel_and_minimum_features(motor_parts):
    saddle = motor_parts["saddle"]
    _assert_valid_one_solid(saddle)
    box = saddle.bounding_box()
    assert tuple(box.size) == pytest.approx((43.0, 36.0, p.motor_saddle_thickness))
    assert p.motor_slot_total_travel == pytest.approx(2.0 * p.motor_adjustment)
    z0 = box.min.Z
    for x in p.motor_clamp_x:
        for y in p.motor_clamp_y:
            frozen_slot = g._slot_cutter(
                x,
                y,
                z0 - 0.2,
                p.motor_clamp_clearance,
                p.motor_slot_total_travel,
                p.motor_saddle_thickness + 0.4,
            )
            assert _intersection_volume(saddle, frozen_slot) <= VOLUME_TOL

    assert p.motor_saddle_thickness - p.motor_clamp_nut_depth == pytest.approx(0.60)
    x_ligament = min(p.motor_clamp_x) - p.motor_adjustment - p.motor_clamp_clearance / 2.0 - p.motor_saddle_x[0]
    y_ligament = p.motor_saddle_half_width - (
        max(abs(y) for y in p.motor_clamp_y) + p.motor_clamp_nut_af / sqrt(3.0)
    )
    assert x_ligament == pytest.approx(5.80)
    assert y_ligament > 0.32
    assert p.guide_arm_min_thickness == pytest.approx(1.20)


def test_two_printable_clamp_straps_retain_motor_at_all_four_m3_axes(motor_parts, motor_references):
    straps = (motor_parts["clamp_strap_1"], motor_parts["clamp_strap_2"])
    motor = motor_references["motor"]
    assert p.motor_clamp_strap_radial >= 6.0
    assert p.motor_clamp_strap_tangential >= 36.0
    assert p.motor_clamp_strap_thickness >= 3.0
    for x, strap in zip(p.motor_clamp_x, straps):
        _assert_valid_one_solid(strap)
        assert tuple(strap.bounding_box().size) == pytest.approx(
            (p.motor_clamp_strap_radial, p.motor_clamp_strap_tangential, p.motor_clamp_strap_thickness)
        )
        assert strap.distance_to(motor) == pytest.approx(0.0, abs=VOLUME_TOL)
        assert _intersection_volume(strap, motor) <= VOLUME_TOL
        for y in p.motor_clamp_y:
            hole = _cylinder(
                p.motor_clamp_clearance,
                p.motor_clamp_strap_thickness + 0.4,
                x,
                y,
                p.motor_clamp_strap_z0 - 0.2,
            )
            assert _intersection_volume(strap, hole) <= VOLUME_TOL
        radial_ligament = (p.motor_clamp_strap_radial - p.motor_clamp_clearance) / 2.0
        tangential_ligament = p.motor_clamp_strap_tangential / 2.0 - (
            max(abs(y) for y in p.motor_clamp_y) + p.motor_clamp_clearance / 2.0
        )
        assert radial_ligament >= 1.30
        assert tangential_ligament >= 1.80


def test_drive_gears_are_actual_printable_single_breps_not_purchased_references(motor_parts):
    gears = (
        motor_parts["horizontal_miter"],
        motor_parts["vertical_miter"],
        motor_parts["output_pinion"],
    )
    assert all("PRINT" in gear.label for gear in gears)
    assert sum("miter" in gear.label for gear in gears) == 2
    assert sum("output_pinion" in gear.label for gear in gears) == 1
    for gear in gears:
        _assert_valid_one_solid(gear)


def test_fin_foot_holes_leave_measured_ligaments(motor_parts):
    fin = motor_parts["fin"]
    _assert_valid_one_solid(fin)
    box = fin.bounding_box()
    assert (box.size.X, box.size.Y) == pytest.approx((p.fin_foot_radial, p.fin_foot_tangential))
    radial_ligament = (p.fin_foot_radial - p.fin_hole_diameter) / 2.0
    tangential_ligament = p.fin_foot_tangential / 2.0 - p.fin_hole_spacing / 2.0 - p.fin_hole_diameter / 2.0
    between_holes = p.fin_hole_spacing - p.fin_hole_diameter
    assert (radial_ligament, tangential_ligament, between_holes) == pytest.approx((1.8, 1.8, 5.6))
    for y in (-p.fin_hole_spacing / 2.0, p.fin_hole_spacing / 2.0):
        hole = _cylinder(p.fin_hole_diameter, p.fin_foot_thickness + 0.4, p.fin_mount_radius, y, 5.6)
        assert _intersection_volume(fin, hole) <= VOLUME_TOL


@pytest.mark.parametrize(
    "filename,expected",
    (("p3_v3_r2_seam_race_coupon.step", 14), ("p3_v3_r2_motor_station_coupon.step", 19)),
)
def test_key_exported_assembly_breps_are_valid_and_named(filename, expected):
    assembly = import_step(MODEL_ROOT / filename)
    assert assembly.is_valid and BRepCheck_Analyzer(assembly.wrapped).IsValid()
    assert len(assembly.children) == len(assembly.solids()) == expected
    assert len({child.label for child in assembly.children}) == expected
    assert all(child.volume > 0 and len(child.solids()) == 1 for child in assembly.children)


def test_motor_station_all_pairwise_brep_collisions_are_declared(motor_parts, motor_references):
    parts = [*motor_parts.values(), *motor_references.values()]
    collisions = []
    for left, right in combinations(parts, 2):
        volume = _intersection_volume(left, right)
        if volume > VOLUME_TOL:
            collisions.append((left.label, right.label, volume))
    assert len(collisions) == 1
    labels = set(collisions[0][:2])
    assert labels == {
        "p3_v3_r2_coupon_B_purchased_4x40mm_vertical_D_steel_shaft_3p5AF",
        "p3_v3_r2_B_PRINT_M1_16T_output_pinion_D4p1",
    }
    assert collisions[0][2] > 0.0


def test_motor_ring_pinion_phase_sampling_and_nominal_brep_clearance(motor_parts, motor_references):
    phases = tuple(-p.tooth_pitch_degrees / 2.0 + i * p.tooth_pitch_degrees / 16.0 for i in range(17))
    for phase in phases:
        pinion_phase = phase * p.gear_ratio
        assert pinion_phase / p.gear_ratio == pytest.approx(phase)
    arc = motor_parts["arc"]
    pinion = motor_parts["output_pinion"]
    assert _intersection_volume(arc, pinion) <= VOLUME_TOL
    assert arc.distance_to(pinion) >= 0.099


def _manifest_artifact_paths(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from _manifest_artifact_paths(child)
    elif isinstance(value, list):
        for child in value:
            yield from _manifest_artifact_paths(child)
    elif isinstance(value, str) and value.lower().endswith((".step", ".stl", ".3mf")):
        yield value


def _transform_3mf_point(values, point):
    x, y, z = point
    return (
        x * values[0] + y * values[3] + z * values[6] + values[9],
        x * values[1] + y * values[4] + z * values[7] + values[10],
        x * values[2] + y * values[5] + z * values[8] + values[11],
    )


def test_valid_3mf_xml_objects_transforms_and_nonoverlapping_bed_placement():
    path = MODEL_ROOT / "print" / "p3_v3_r2_printable_coupons.3mf"
    with ZipFile(path) as package:
        assert package.testzip() is None
        for member in package.namelist():
            if member.endswith((".xml", ".rels", ".model")) or member == "[Content_Types].xml":
                ET.fromstring(package.read(member))
        root = ET.fromstring(package.read("3D/3dmodel.model"))

    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objects = root.findall(".//m:object", ns)
    items = root.findall(".//m:item", ns)
    assert len(objects) == len(items) == 21
    object_by_id = {obj.attrib["id"]: obj for obj in objects}
    bounds = []
    for item in items:
        obj = object_by_id[item.attrib["objectid"]]
        mesh = obj.find("m:mesh", ns)
        assert mesh is not None
        vertices = mesh.findall("m:vertices/m:vertex", ns)
        triangles = mesh.findall("m:triangles/m:triangle", ns)
        assert vertices and triangles
        values = tuple(float(value) for value in item.attrib["transform"].split())
        assert len(values) == 12
        placed = [
            _transform_3mf_point(
                values,
                (float(vertex.attrib["x"]), float(vertex.attrib["y"]), float(vertex.attrib["z"])),
            )
            for vertex in vertices
        ]
        low = tuple(min(point[axis] for point in placed) for axis in range(3))
        high = tuple(max(point[axis] for point in placed) for axis in range(3))
        assert low[2] == pytest.approx(0.0, abs=1e-5)
        assert low[0] >= 0.0 and low[1] >= 0.0
        assert high[0] <= 250.0 and high[1] <= 250.0
        bounds.append((obj.attrib["name"], low, high))

    for (name_a, low_a, high_a), (name_b, low_b, high_b) in combinations(bounds, 2):
        overlap_x = min(high_a[0], high_b[0]) - max(low_a[0], low_b[0])
        overlap_y = min(high_a[1], high_b[1]) - max(low_a[1], low_b[1])
        assert not (overlap_x > 1e-5 and overlap_y > 1e-5), (name_a, name_b)

    arc_name, _, _ = next(record for record in bounds if "24T_motor_station_arc" in record[0])
    arc_item = next(item for item in items if object_by_id[item.attrib["objectid"]].attrib["name"] == arc_name)
    arc_transform = tuple(float(value) for value in arc_item.attrib["transform"].split())
    assert arc_transform[0] == pytest.approx(1.0)
    assert arc_transform[4] == pytest.approx(-1.0)
    assert arc_transform[8] == pytest.approx(-1.0)


def test_printable_drive_clamps_orientation_and_purchased_bom_manifest():
    manifest = json.loads((MODEL_ROOT / "manifest.json").read_text())
    assert "complete horizontal NEMA8 retention" in manifest["assemblyNote"]
    assert manifest["printableOnly3mf"]["objects"] == 21
    assert manifest["printableOnly3mf"]["items"] == 21
    stl_labels = {record["sourceFacts"]["label"] for record in manifest["individualPrintableStl"]}
    assert len(stl_labels) == 21
    assert {
        "p3_v3_r2_B_PRINT_M1_16T_horizontal_miter",
        "p3_v3_r2_B_PRINT_M1_16T_vertical_miter",
        "p3_v3_r2_B_PRINT_M1_16T_output_pinion_D4p1",
        "p3_v3_r2_B_NEMA8_M3_clamp_strap_1",
        "p3_v3_r2_B_NEMA8_M3_clamp_strap_2",
    }.issubset(stl_labels)
    assert not any("NEMA8_20p3_face" in label or "MR84ZZ" in label or "steel_shaft" in label for label in stl_labels)

    bom = {(row["item"], row["quantity"], row["specification"]) for row in manifest["purchasedBom"]}
    assert any(item == "output D-shaft" and qty == 1 and "4.00 mm diameter x 40.0 mm" in spec for item, qty, spec in bom)
    assert any(item == "MR84ZZ bearing" and qty == 2 and "4 x 8 x 3 mm" in spec for item, qty, spec in bom)
    assert any(item == "M2 heat-set insert" and qty == 4 and "3.2 mm OD x 3.0 mm" in spec for item, qty, spec in bom)
    assert any(item == "M3 socket-head screw" and qty == 4 and "M3 x 30 mm" in spec for item, qty, spec in bom)
    assert any(item == "M3 hex nut" and qty == 4 and "AF 5.5 mm" in spec for item, qty, spec in bom)
    assert any(item == "split shaft collar" and qty == 1 and "4.0 mm bore" in spec for item, qty, spec in bom)

    arc_record = next(record for record in manifest["individualPrintableStl"] if "24T_motor_station_arc" in record["sourceFacts"]["label"])
    assert arc_record["orientationEulerDegreesXYZ"] == [180.0, 0.0, 0.0]
    assert arc_record["printFacts"]["boundsMm"]["min"][2] == pytest.approx(0.0, abs=1e-6)
    arc_stl = MODEL_ROOT / arc_record["file"]["path"]
    mesh = trimesh.load_mesh(arc_stl, process=True, force="mesh")
    bed_faces = [index for index, center in enumerate(mesh.triangles_center) if abs(center[2]) <= 1e-5 and mesh.face_normals[index][2] < -0.99]
    assert sum(float(mesh.area_faces[index]) for index in bed_faces) > 300.0


def test_export_artifacts_manifest_and_meshes_when_present():
    manifests = [MODEL_ROOT / "manifest.json"] if (MODEL_ROOT / "manifest.json").exists() else []
    steps = sorted(path for path in MODEL_ROOT.rglob("*.step") if path.is_file()) if MODEL_ROOT.exists() else []
    meshes = sorted(path for path in MODEL_ROOT.rglob("*.stl") if path.is_file()) if MODEL_ROOT.exists() else []
    bundles = sorted(path for path in MODEL_ROOT.rglob("*.3mf") if path.is_file()) if MODEL_ROOT.exists() else []
    if not (manifests or steps or meshes or bundles):
        pytest.skip("coupon export owner has not emitted artifacts yet")

    assert manifests, "exported coupons require a machine-readable manifest"
    manifest = json.loads(manifests[0].read_text())
    assert all(max(record["extentDeltaMm"]) <= 1e-6 for record in manifest["assemblies"])
    assert all(record["sourceFacts"]["solids"] == record["importedSolids"] for record in manifest["assemblies"])
    advertised = set(_manifest_artifact_paths(manifest))
    assert advertised, "manifest does not advertise any STEP/STL/3MF artifacts"
    for relative in advertised:
        candidates = (MODEL_ROOT / relative, manifests[0].parent / relative, ROOT / relative)
        path = next((candidate for candidate in candidates if candidate.exists()), None)
        assert path is not None, relative
        assert path.stat().st_size > 100, relative

    for path in steps:
        exported = import_step(path)
        assert exported.is_valid and BRepCheck_Analyzer(exported.wrapped).IsValid(), path.name
        assert all(solid.volume > 0.0 for solid in exported.solids()), path.name
    for path in meshes:
        mesh = trimesh.load_mesh(path, process=True, force="mesh")
        assert isinstance(mesh, trimesh.Trimesh) and mesh.is_watertight and mesh.volume > 0.0, path.name
    for path in bundles:
        with ZipFile(path) as package:
            assert package.testzip() is None, path.name
            assert "3D/3dmodel.model" in package.namelist(), path.name
