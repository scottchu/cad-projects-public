from __future__ import annotations

import ast
import gc
import json
import subprocess
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import fields, replace
from hashlib import sha256
from itertools import combinations
from math import hypot, radians, sqrt
from pathlib import Path

import pytest
import lib3mf
from build123d import Pos, export_step, import_step

import xt60_bend_jig.p13_four_plate_three_rod as p13
import xt60_bend_jig.p16_cap_throat_test as p16


ROOT = Path(__file__).parents[1]
CAD = ROOT / "cad" / "p13_four_plate_three_rod"
GEOMETRY_CASE = ROOT / "tests" / "p13_geometry_case.py"


@pytest.fixture(autouse=True)
def _release_occ_memory_after_test():
    yield
    p13.clear_geometry_caches()
    gc.collect()


def intersection_volume(first, second) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return float(common.volume)
    return sum(float(item.volume) for item in common)


def bounds(shape) -> tuple[float, ...]:
    box = shape.bounding_box()
    return (*box.min, *box.max)


def leaves(shape):
    if not shape.children:
        return [shape]
    result = []
    for child in shape.children:
        result.extend(leaves(child))
    return result


def canonical_occurrences(shape) -> dict[str, list[tuple[int, float]]]:
    result: dict[str, list[tuple[int, float]]] = defaultdict(list)
    for leaf in leaves(shape):
        result[leaf.label].append((len(leaf.solids()), round(float(leaf.volume), 7)))
    return {key: sorted(values) for key, values in sorted(result.items())}


def run_geometry_case(case: str, *args: object) -> None:
    subprocess.run(
        [sys.executable, str(GEOMETRY_CASE), case, *[str(arg) for arg in args]],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def test_gate0_hash_p21_pivot_and_independent_stroke_derivations() -> None:
    p = p13.P13_DEFAULTS
    brief = ROOT / p13.P13_GATE0_BRIEF_PATH
    assert sha256(brief.read_bytes()).hexdigest() == p13.P13_GATE0_BRIEF_SHA256
    assert p13.P13_GATE0_BRIEF_SHA256 == "9c2102114cbf87ccabaa4388ed3814b91cdf3f8f654c775f5ddd8a5d05272322"
    amendment = ROOT / p13.P13_DOMAIN_AMENDMENT_PATH
    assert sha256(amendment.read_bytes()).hexdigest() == p13.P13_DOMAIN_AMENDMENT_SHA256
    assert p13.P13_DOMAIN_AMENDMENT_SHA256 == "b50e850ac5425fe7bad0e49555de10b0e30f63e04934bdbf66d4220f44e1f590"
    expected_delta = (
        p.shaft_od / 2.0
        + p.wire_diameter_design / 2.0
        + p.c_sw
        - p.bend_radius * (sqrt(2.0) - 1.0)
    ) / sqrt(2.0)
    assert p.pivot_delta == pytest.approx(expected_delta, abs=1e-12)
    assert (p.shaft_y, p.shaft_z) == pytest.approx(
        (-2.0963726445859683, 27.90362735541403), abs=1e-12
    )
    assert p.stroke_requirements == pytest.approx(
        {"upright": 3.2035533905932736, "bottom": 0.0, "diagonal": 3.7642135623730946}
    )
    assert p.contact_stroke == pytest.approx(max(p.stroke_requirements.values()))
    assert p.common_stroke == pytest.approx(p.contact_stroke + p.wire_preload)
    assert "shaft_y" not in {field.name for field in fields(p13.P13Parameters)}
    assert "common_stroke" not in {field.name for field in fields(p13.P13Parameters)}


def test_manifest_units_classes_dependency_graph_and_provenance_are_complete() -> None:
    p = p13.P13_DEFAULTS
    manifest = p13.parameter_manifest(p)
    graph = p13.parameter_dependency_graph()
    field_names = {field.name for field in fields(p13.P13Parameters)}
    assert set(manifest["parameters"]) == field_names
    assert manifest["frozenTopology"] == p13.P13_FROZEN_TOPOLOGY
    assert set(graph) == field_names
    assert all(row["unit"] for row in manifest["parameters"].values())
    assert all(row["class"] in {"safe-retune", "requires-regate"} for row in manifest["parameters"].values())
    assert set(p13.P13_SAFE_RETUNE_FIELDS) | set(p13.P13_REGATE_FIELDS) == field_names
    assert not set(p13.P13_SAFE_RETUNE_FIELDS) & set(p13.P13_REGATE_FIELDS)
    assert {"c_sw", "wire_diameter_design", "wire_preload"} <= p13.P13_SAFE_RETUNE_FIELDS
    assert {
        "pivot_delta", "shaft_y", "shaft_z", "contact_stroke", "common_stroke",
        "tangent_contact_offset", "locked_contact_offset",
        "nominal_thrust_land_gap",
        "rod_withdrawal_distance", "removal_lift",
    } <= set(manifest["derived"])
    effect_domains = p13.parameter_effect_domains()
    assert set(effect_domains) == field_names
    assert all(effect_domains[name] for name in field_names)
    required_prefixes = ("datum:", "cutter:", "solid:", "state:", "test:", "export:")
    for primary, consequences in graph.items():
        assert all(
            any(token.startswith(prefix) for token in consequences)
            for prefix in required_prefixes
        ), primary
        for domain in effect_domains[primary]:
            expected = p13.P13_EFFECT_DOMAIN_CONSEQUENCES[domain]
            assert expected <= set(consequences), (primary, domain, expected - set(consequences))
    p13.validate_parameter_dependency_graph(graph)
    runtime_consumers = p13.parameter_runtime_consumers()
    assert set(runtime_consumers) == field_names
    assert all(runtime_consumers.values())
    for field_name, readers in runtime_consumers.items():
        assert {f"reader:{reader}" for reader in readers} <= set(graph[field_name])

    # Omission-sensitive critical chains: these assert the requested semantic
    # consequences, not merely graph key presence.
    assert {
        "effect-domain:motion",
        "datum:locked-centres-stroke-requirements-common-stroke-and-rod-centres",
        "datum:inverse-cam-paths-and-lane-centrelines",
        "cutter:fixed-lane-and-cam-lane-cutters",
        "solid:four-plate-lane-solids-and-three-rod-poses",
        "state:open-loaded-set-close-locked-cool-and-release",
        "test:continuous-full-domain-lane-certificate",
        "export:all-motion-bearing-workflow-step",
    } <= set(graph["wire_preload"])
    assert {
        "effect-domain:actuator-shaft",
        "datum:D-shaft-head-hubs-x-extents-and-round-groove-frames",
        "cutter:two-cam-D-bores-and-shaft-round-land-annuli",
        "solid:two-D-bored-cams-and-separate-headed-D-shaft",
        "state:all-coupled-rotation-and-service-disassembly-states",
        "test:D-dimensions-phase-lash-endplay-extraction-and-source-export-parity",
        "export:left-cam-right-actuator-shaft-all-core-workflow-and-service-step",
    } <= set(graph["axial_endplay"])

    # Mutation checks are omission-sensitive at the individual-consumer level,
    # rather than merely confirming six category prefixes are still present.
    missing_field = deepcopy(graph)
    del missing_field["wire_preload"]
    with pytest.raises(ValueError, match="field mismatch"):
        p13.validate_parameter_dependency_graph(missing_field)
    for field_name, consumer in (
        (
            "wire_preload",
            "cutter:fixed-lane-and-cam-lane-cutters",
        ),
        (
            "axial_endplay",
            "datum:D-shaft-head-hubs-x-extents-and-round-groove-frames",
        ),
    ):
        missing_consumer = deepcopy(graph)
        missing_consumer[field_name].remove(consumer)
        with pytest.raises(ValueError, match=field_name):
            p13.validate_parameter_dependency_graph(missing_consumer)

    # Every serialized field -> consequence edge is omission-sensitive.  This
    # catches a registry that retains six broad category prefixes while losing
    # one actual datum, cutter, solid, state, test, or export consumer.
    for field_name, consumers in graph.items():
        for consumer in consumers:
            missing_edge = deepcopy(graph)
            missing_edge[field_name].remove(consumer)
            with pytest.raises(ValueError, match=field_name):
                p13.validate_parameter_dependency_graph(missing_edge)

    # A stale proof body hidden by a later same-name definition invalidates
    # source review even when Python happens to execute the final definition.
    source_tree = ast.parse(Path(p13.__file__).read_text())
    function_names = [
        node.name
        for node in source_tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert not [name for name, count in Counter(function_names).items() if count > 1]
    token = p13.provenance_token(p)
    assert p13.P13_GATE0_BRIEF_SHA256 in token
    assert p13.P13_DOMAIN_AMENDMENT_SHA256 in token
    assert p13.parameter_manifest_sha256(p)[:12] in token
    assert p13.source_revision_sha256()[:12] in token


def test_serialized_dependencies_match_actual_critical_geometry_consequences() -> None:
    base = p13.P13_DEFAULTS
    contact = replace(base, wire_preload=base.wire_preload + 0.10)
    assert contact.locked_centres != base.locked_centres
    assert contact.contact_centres == base.contact_centres
    assert contact.stroke_requirements == base.stroke_requirements
    assert contact.common_stroke != pytest.approx(base.common_stroke)
    changed_open = p13.rod_center("upright", 0.0, contact)
    base_open = p13.rod_center("upright", 0.0, base)
    assert (changed_open.y, changed_open.z) == pytest.approx(
        (base_open.y, base_open.z), abs=1.0e-12
    )
    assert p13.inverse_cam_path("upright", contact) != p13.inverse_cam_path("upright", base)

    shaft = replace(base, shaft_head_thickness=base.shaft_head_thickness + 0.20)
    base_shaft = p13.build_actuator_shaft(base.open_angle_deg, base)
    changed_shaft = p13.build_actuator_shaft(shaft.open_angle_deg, shaft)
    assert changed_shaft.bounding_box().max.X == pytest.approx(
        base_shaft.bounding_box().max.X + 0.20, abs=1e-7
    )
    assert changed_shaft.volume != pytest.approx(base_shaft.volume)


def test_every_mutable_field_has_a_runtime_consumer_and_frozen_choices_reject_overrides() -> None:
    field_names = {field.name for field in fields(p13.P13Parameters)}
    removed_or_frozen = {
        "removal_sample_count",
        "fixed_journal_opening",
        "cam_phase_feature",
        "right_cap_slit_count",
    }
    assert not field_names & removed_or_frozen
    assert set(p13.parameter_runtime_consumers()) == field_names

    manifest = p13.parameter_manifest()
    assert manifest["frozenTopology"] == {
        "fixed_journal_opening": "upward",
        "cam_phase_feature": "separate_D_keyed_shaft",
        "right_cap_slit_count": 1,
    }
    noncanonical = {
        "fixed_journal_opening": "downward",
        "cam_phase_feature": "round_pin",
        "right_cap_slit_count": 2,
    }
    for name, value in noncanonical.items():
        for allow_regate in (False, True):
            with pytest.raises(ValueError, match="frozen P13 topology"):
                p13.parameters_from_overrides(
                    {name: value},
                    allow_regate=allow_regate,
                )
    for allow_regate in (False, True):
        with pytest.raises(ValueError, match="unknown P13 parameter"):
            p13.parameters_from_overrides(
                {"removal_sample_count": 129},
                allow_regate=allow_regate,
            )

    # The retained sampling control is explicitly diagnostic: perturbing it
    # changes only the number of review poses, never a proof certificate.
    base = p13.P13_DEFAULTS
    changed = replace(
        base,
        removal_review_sample_count=base.removal_review_sample_count + 1,
    )
    base_labels = [leaf.label for leaf in leaves(p13.build_removal_sweep_review(base))]
    changed_labels = [leaf.label for leaf in leaves(p13.build_removal_sweep_review(changed))]
    assert sum("diagnostic_only_removal_plusZ_sample" in label for label in base_labels) == 5
    assert sum("diagnostic_only_removal_plusZ_sample" in label for label in changed_labels) == 6
    assert p13.continuous_removal_certificate(base) == p13.continuous_removal_certificate(changed)


@pytest.mark.parametrize(
    "overrides",
    ({"c_sw": 0.60}, {"wire_diameter_design": 4.25}, {"c_sw": 0.65, "wire_diameter_design": 4.20}),
)
def test_safe_pivot_retunes_move_every_concentric_datum_but_not_task_contacts(overrides) -> None:
    base = p13.P13_DEFAULTS
    changed = p13.parameters_from_overrides(overrides)
    assert (changed.shaft_y, changed.shaft_z) != (base.shaft_y, base.shaft_z)
    if "wire_diameter_design" in overrides:
        assert changed.contact_centres != base.contact_centres
        assert changed.locked_centres != base.locked_centres
        assert changed.common_stroke != pytest.approx(base.common_stroke)
        assert changed.wire_preload == pytest.approx(base.wire_preload)
    else:
        assert changed.contact_centres == base.contact_centres
        assert changed.locked_centres == base.locked_centres
        assert changed.common_stroke == pytest.approx(base.common_stroke)
    assert changed.initial_arc_distance == pytest.approx(base.initial_arc_distance)
    assert changed.pivot_delta != base.pivot_delta


def test_one_connected_complete_workpiece_has_required_extrema_and_90_degree_path() -> None:
    run_geometry_case("workpiece")


def test_three_rods_are_tangent_at_contact_then_apply_locked_wire_preload() -> None:
    p = p13.P13_DEFAULTS
    assert p.tangent_contact_offset == pytest.approx(
        p.rod_diameter / 2.0 + p.wire_diameter_design / 2.0
    )
    assert p.locked_contact_offset == pytest.approx(
        p.tangent_contact_offset - p.wire_preload
    )
    for name in p13.ROD_NAMES:
        contact = p.contact_centres[name]
        locked = p.locked_centres[name]
        assert contact.distance_to(locked) == pytest.approx(p.wire_preload)
    run_geometry_case("wire_preload")


def test_exact_occurrence_census_and_upward_journal_topology() -> None:
    assert p13.source_occurrence_census() == {
        "visible_principal_plate_occurrences": 4,
        "unique_principal_print_definitions": 3,
        "fixed_guide_print_quantity": 2,
        "purchased_uncut_rods": 3,
        "right_actuator_occurrences": 1,
        "separate_shaft_occurrences": 1,
        "shaft_keepers": 1,
        "rod_caps": 6,
        "user_actuator_inputs": 1,
        "bases_spines_bridges_holders": 0,
    }
    assert p13.P13_FIXED_JOURNAL_OPENING == "upward"
    run_geometry_case("occurrence")


def test_right_cap_physical_fit_contract_is_rigid_clear_and_floor_blocked() -> None:
    p = p13.P13_DEFAULTS
    assert p.right_cap_cavity == pytest.approx(4.20)
    assert p.right_cap_throat == pytest.approx(4.10)
    assert p.right_cap_min_radial_wall == pytest.approx(1.40)
    assert p.right_cap_nominal_radial_clearance == pytest.approx(0.05)
    assert p.right_cap_functional_overcut == pytest.approx(0.03)
    assert p.right_cap_slit_z0 == pytest.approx(1.995)

    cap = p13._right_cap_local(p)
    assert cap.is_valid
    assert len(cap.solids()) == 1
    assert float(cap.volume) > 0.0
    assert bounds(cap) == pytest.approx(
        (0.0, -p.cap_od / 2.0, -p.cap_od / 2.0,
         p.cap_length, p.cap_od / 2.0, p.cap_od / 2.0),
        abs=1.0e-7,
    )

    # The complete annular floor must remain present: the slit and all bore
    # cutters stop exactly at X=3.00 and may overcut only past the open face.
    expected_floor = p13._x_cylinder(
        p.cap_od,
        p.cap_length - p.right_cap_cavity_end,
        (p.cap_length + p.right_cap_cavity_end) / 2.0,
        0.0,
        0.0,
    )
    assert float((expected_floor - cap).volume) == pytest.approx(0.0, abs=1.0e-7)
    assert intersection_volume(cap, expected_floor) == pytest.approx(
        float(expected_floor.volume), abs=1.0e-7
    )

    # Production P13 is exactly the accepted P16 4.10 functional core, with
    # P16's tag/label excluded and its print-Z axis rigidly mapped to P13 +X.
    p16_core = p16.build_functional_cap_core(4.10)
    transformed_p16 = (
        p13.Rot(0.0, -90.0, 0.0)
        * p13.Pos(0.0, 0.0, -p.cap_length)
        * p16_core
    )
    symmetric_difference_volume = float((cap - transformed_p16).volume) + float(
        (transformed_p16 - cap).volume
    )
    assert symmetric_difference_volume == pytest.approx(0.0, abs=1.0e-7)

    # A 10-mm-long coaxial rod ending at q covers every installation pose
    # while keeping the far end out of the finite cap body.
    for cap_roll_deg in (0.0, 90.0, 180.0, 270.0):
        rolled_cap = p13.Rot(cap_roll_deg, 0.0, 0.0) * cap
        for q in (-3.0, 0.0, 2.5, 3.0):
            rod = p13._x_cylinder(p.rod_diameter, 10.0, q - 5.0, 0.0, 0.0)
            assert intersection_volume(rolled_cap, rod) == pytest.approx(0.0, abs=1.0e-7)

    # The accepted endpoint is tangent to the retained floor; advancing past
    # it produces positive overlap and therefore proves geometric blocking.
    rod_past_floor = p13._x_cylinder(p.rod_diameter, 10.0, 3.10 - 5.0, 0.0, 0.0)
    assert intersection_volume(cap, rod_past_floor) > 1.0e-5

    installed_cap = p13.build_right_cap("upright", p.open_angle_deg, p)
    installed_rod = p13.build_rod("upright", p.open_angle_deg, p)
    assert intersection_volume(installed_cap, installed_rod) == pytest.approx(0.0, abs=1.0e-7)
    assert "print_fit" in installed_cap.label
    assert "cavity_D4p20_throat_D4p10" in installed_cap.label


def test_separate_D_shaft_actual_solids_capture_phase_and_print_orientation() -> None:
    p = p13.P13_DEFAULTS
    assert p.cam_d_engagement == pytest.approx(4.50)
    assert (p.cam_hub_od - p.cam_d_bore_od) / 2.0 >= 2.075

    shaft = p13.build_actuator_shaft(p.open_angle_deg, p)
    shaft_section = shaft.intersect(
        p13._box((0.0, p.shaft_y, p.shaft_z), (0.10, 12.0, 12.0))
    )
    if not hasattr(shaft_section, "bounding_box"):
        shaft_section = shaft_section.solids()[0]
    section_box = shaft_section.bounding_box()
    assert section_box.size.Y == pytest.approx(p.shaft_od, abs=1e-7)
    assert section_box.size.Z == pytest.approx(p.shaft_d_across_flat, abs=1e-7)

    bore = p13._cam_d_bore_cutter(p.cam_left_x, p.cam_d_engagement, p)
    bore_box = bore.bounding_box()
    assert bore_box.size.Y == pytest.approx(p.cam_d_bore_od, abs=1e-7)
    assert bore_box.size.Z == pytest.approx(p.cam_d_bore_across_flat, abs=1e-7)
    assert intersection_volume(p13.build_left_cam(0.0, p), bore) == pytest.approx(0.0, abs=1e-7)
    right_bore = p13._cam_d_bore_cutter(p.cam_right_x, p.cam_d_engagement, p)
    assert intersection_volume(p13.build_right_actuator(0.0, p), right_bore) == pytest.approx(0.0, abs=1e-7)

    one_sided_lash = p13.d_shaft_one_sided_lash_deg(p)
    assert one_sided_lash == pytest.approx(1.9325113632826, abs=1e-10)
    assert one_sided_lash <= 3.0
    male_d = p13._d_prism_x(
        p.shaft_od,
        p.shaft_d_across_flat,
        1.0,
        0.0,
        p,
    )
    female_d = p13._cam_d_bore_cutter(0.0, 1.0, p)
    contained = p13._rotate_about_shaft(male_d, one_sided_lash - 0.02, p)
    escaped = p13._rotate_about_shaft(male_d, one_sided_lash + 0.02, p)
    assert float((contained - female_d).volume) == pytest.approx(0.0, abs=1e-9)
    assert float((escaped - female_d).volume) > 1.0e-7

    endplay = p.left_cam_hub_outer_x - (
        p.keeper_groove_x + p.keeper_thickness / 2.0
    )
    assert endplay == pytest.approx(p.axial_endplay, abs=1e-9)
    assert 0.20 <= endplay <= 0.35
    assert p.shaft_head_inner_x == pytest.approx(p.right_cam_hub_outer_x)
    assert p.fixed_groove_od - p.journal_land_od == pytest.approx(0.20)
    assert p.main_face_gap == pytest.approx(0.30)
    assert p.fixed_thrust_land_height == pytest.approx(0.20)
    assert p.cam_thrust_land_height == pytest.approx(0.0)
    assert p.nominal_thrust_land_gap == pytest.approx(0.10)

    # Zero-height cam lands are absent, not modeled as degenerate solids.  Each
    # fixed plate carries the whole 0.20-mm projection, preserving the exact
    # 0.10-mm nominal clearance without changing either cam/fixed main face.
    left_cam_box = p13.build_left_cam(p.open_angle_deg, p).bounding_box()
    left_fixed_box = p13.build_fixed_plate("left", p).bounding_box()
    right_fixed_box = p13.build_fixed_plate("right", p).bounding_box()
    right_actuator_box = p13.build_right_actuator(p.open_angle_deg, p).bounding_box()
    assert left_cam_box.max.X == pytest.approx(
        p.cam_left_x + p.cam_thickness / 2.0, abs=1e-7
    )
    assert left_fixed_box.min.X == pytest.approx(
        p.fixed_left_x - p.fixed_thickness / 2.0 - p.fixed_thrust_land_height,
        abs=1e-7,
    )
    assert left_fixed_box.min.X - left_cam_box.max.X == pytest.approx(0.10, abs=1e-7)
    assert right_fixed_box.max.X == pytest.approx(
        p.fixed_right_x + p.fixed_thickness / 2.0 + p.fixed_thrust_land_height,
        abs=1e-7,
    )
    assert right_actuator_box.min.X == pytest.approx(
        p.cam_right_x - p.cam_thickness / 2.0, abs=1e-7
    )
    assert right_actuator_box.min.X - right_fixed_box.max.X == pytest.approx(
        0.10, abs=1e-7
    )
    service = p13.shaft_service_extraction_certificate(p)
    assert service["dInterfaceAngularLash"]["oneSided"]["value"] == pytest.approx(
        one_sided_lash,
        abs=1e-12,
    )
    assert service["serviceOrder"] == [
        "shaft_keeper_radially_off",
        "both_upward_C_fixed_guides_release_minusZ",
        "separate_D_shaft_extract_plusX_through_stationary_cams",
    ]
    assert not service["directPlusXWithFixedGuidesInstalled"]["admissible"]
    assert min(
        service["directPlusXWithFixedGuidesInstalled"]["actualSolidIntersectionVolumes"]["value"].values()
    ) > p.continuous_overlap_volume_tolerance
    assert service["stagedPlusXAfterFixedGuidesClear"]["maximumIntersectionVolume"]["value"] == pytest.approx(0.0, abs=1e-7)
    assert service["journalToDBoreFlatClearance"]["value"] >= 0.10 - 1e-9

    for angle in (p.open_angle_deg, p.rise_end_deg, p.locked_angle_deg):
        structure = list(p13.build_four_plate_structure(angle, p).children)
        assert len(structure) == 6
        assert max(
            intersection_volume(first, second)
            for first, second in combinations(structure, 2)
        ) <= p.continuous_overlap_volume_tolerance

    print_parts = list(p13.build_print_kit(p).children)
    assert len(print_parts) == 14  # 12 production objects + two diagnostic coupons
    assert all(-1e-7 <= part.bounding_box().min.Z <= 1e-7 for part in print_parts)
    principal = print_parts[:4]
    bed_face_areas = []
    for part in principal:
        planar_bed_faces = [
            face
            for face in part.faces()
            if abs(face.bounding_box().min.Z) <= 1e-7
            and abs(face.bounding_box().max.Z) <= 1e-7
        ]
        assert len(planar_bed_faces) == 1
        bed_face_areas.append(float(planar_bed_faces[0].area))
    assert min(bed_face_areas) > 1000.0
    assert p.print_plate_rotation_deg == pytest.approx(90.0)
    assert p.print_actuator_rotation_deg == pytest.approx(90.0)
    assert p.print_cap_rotation_deg == pytest.approx(90.0)
    printed_caps = print_parts[6:12]
    assert len(printed_caps) == 6
    closed_base_height = p.cap_length - p.left_cap_socket_depth
    for index, cap in enumerate(printed_caps):
        cap_box = cap.bounding_box()
        assert cap_box.min.Z == pytest.approx(0.0, abs=1e-7)
        assert cap_box.size.Z == pytest.approx(p.cap_length, abs=1e-7)
        assert cap_box.size.X == pytest.approx(p.cap_od, abs=1e-7)
        assert cap_box.size.Y == pytest.approx(p.cap_od, abs=1e-7)
        bed_faces = [
            face
            for face in cap.faces()
            if abs(face.bounding_box().min.Z) <= 1e-7
            and abs(face.bounding_box().max.Z) <= 1e-7
        ]
        assert len(bed_faces) == 1
        assert float(bed_faces[0].area) == pytest.approx(
            3.141592653589793 * (p.cap_od / 2.0) ** 2,
            abs=1e-6,
        )
        socket_diameter = p.left_cap_socket if index < 3 else p.right_cap_throat
        vertical_open_cavity = (
            Pos(
                (cap_box.min.X + cap_box.max.X) / 2.0,
                (cap_box.min.Y + cap_box.max.Y) / 2.0,
                closed_base_height,
            )
            * p13.Cylinder(
                socket_diameter / 2.0,
                p.cap_length - closed_base_height + p.boolean_axial_overcut,
                align=(p13.Align.CENTER, p13.Align.CENTER, p13.Align.MIN),
            )
        )
        assert intersection_volume(cap, vertical_open_cavity) == pytest.approx(
            0.0, abs=1e-7
        )
    printed_shaft = next(part for part in print_parts if "separate_printed_D_shaft" in part.label)
    shaft_box = printed_shaft.bounding_box()
    assert shaft_box.size.X > shaft_box.size.Y
    assert shaft_box.size.X > shaft_box.size.Z
    assert p.print_shaft_rotation_deg == pytest.approx(0.0)
    coupons = p13.build_fit_coupons(p)
    assert len(coupons.children) == 2
    assert "round_journal" in coupons.children[1].label


@pytest.mark.parametrize("angle", (0.0, 5.0, 11.0, 22.0, 27.0))
def test_representative_rod_plate_poses_are_diagnostics_not_gate_closure(angle: float) -> None:
    run_geometry_case("rods", angle)


def test_continuous_full_domain_motion_and_removal_certificates() -> None:
    p = p13.P13_DEFAULTS
    motion = p13.continuous_motion_certificate(p)
    assert motion["proof"] == "global-analytic-piecewise-C2-chord-bound"
    assert motion["domainThetaDegrees"]["value"] == [p.open_angle_deg, p.locked_angle_deg]
    assert motion["smoothstepMonotone"]
    assert motion["rodAxialReachMargin"]["value"] > 0.0

    theta_contact = radians(p.rise_end_deg - p.open_angle_deg)
    theta_preload = radians(p.locked_angle_deg - p.rise_end_deg)
    knot_angles = p13.cam_path_angles_deg(p)
    h = max(
        radians(second - first)
        for first, second in zip(knot_angles, knot_angles[1:])
    )
    assert motion["polygonKnotAnglesDegrees"]["value"] == list(knot_angles)
    assert motion["maximumCutterInterval"] == {"unit": "radian", "value": h}
    max_s_prime = max(
        1.5 * p.contact_stroke / theta_contact,
        1.5 * p.wire_preload / theta_preload,
    )
    max_s_second = max(
        6.0 * p.contact_stroke / theta_contact**2,
        6.0 * p.wire_preload / theta_preload**2,
    )
    for name in p13.ROD_NAMES:
        opened = p13.rod_center(name, p.open_angle_deg, p)
        locked = p.locked_centres[name]
        max_d = max(
            hypot(opened.y - p.shaft_y, opened.z - p.shaft_z),
            hypot(locked.y - p.shaft_y, locked.z - p.shaft_z),
        )
        expected_m = max(
            max_d + 2.0 * max_s_prime + max_s_second,
            hypot(locked.y - p.shaft_y, locked.z - p.shaft_z),
        )
        expected_error = expected_m * h**2 / 8.0
        row = motion["rods"][name]
        assert row["camInverseSecondDerivativeBound"]["value"] == pytest.approx(expected_m)
        assert row["camChordErrorBound"]["value"] == pytest.approx(expected_error)
        assert row["fixedRadialMargin"]["value"] == pytest.approx(
            (p.lane_width - p.rod_diameter) / 2.0
        )
        assert row["camRadialMargin"]["value"] > 0.0

    withdrawal = p13.rod_left_cap_withdrawal_certificate(p)
    assert withdrawal["domainLambda"]["value"] == [0.0, 1.0]
    assert withdrawal["endpointExitMargin"]["value"] > 0.0
    assert withdrawal["rodSweepEnvelopeLength"]["value"] == pytest.approx(
        p.rod_length + p.rod_withdrawal_distance
    )
    assert withdrawal["leftCapSweepEnvelopeLength"]["value"] == pytest.approx(
        p.cap_length
        + p.rod_withdrawal_distance
        + p13.P13_CAP_ENGAGEMENT_DOMAIN_MM[1]
        - p13.P13_CAP_ENGAGEMENT_DOMAIN_MM[0]
    )
    assert withdrawal["engagementDomain"]["value"] == list(
        p13.P13_CAP_ENGAGEMENT_DOMAIN_MM
    )

    plus_z = p13.workpiece_plus_z_certificate(p)
    global_command = p13.cad_source_global_removal_certificate(p)["globalRemovalCommand"]["value"]
    assert plus_z["domainLift"]["value"] == [0.0, global_command]
    assert plus_z["arcRadialAlignmentInsideDomain"]
    assert plus_z["plusZClearanceMonotone"]
    assert plus_z["globalMargin"]["value"] > 0.0
    assert plus_z["globalMargin"]["value"] == pytest.approx(
        min(row["value"] for row in plus_z["margins"].values())
    )

    lane_witness = p13.continuous_lane_solid_certificate(p)
    assert lane_witness["proof"] == (
        "continuous analytic tubes checked against actual final fixed/cam material"
    )
    for row in lane_witness["rows"].values():
        assert row["maximumIntersectionVolume"]["value"] == 0.0
        assert row["minimumProfileAllowanceRimMargin"]["value"] > 0.0

    exact_removal = p13.continuous_removal_certificate(p)
    assert exact_removal["completeWorkpieceLift"] == plus_z
    stage1 = exact_removal["rightCapStage1Removal"]
    assert stage1["maximumUnintendedIntersectionVolume"]["value"] == 0.0
    assert stage1["stageOrdering"]["mustCompleteBefore"] == "rodLeftCapWithdrawal"
    for row in stage1["rows"].values():
        assert row["engagementDomain"]["value"] == list(
            p13.P13_CAP_ENGAGEMENT_DOMAIN_MM
        )
        assert row["rollDomain"]["value"] == list(p13.P13_FULL_ROLL_DOMAIN_DEG)
        assert row["maximumUnintendedIntersectionVolume"]["value"] == 0.0
        assert row["completeWorkpieceIntersectionVolume"]["value"] == 0.0
        assert set(row["otherStage1EnvelopeIntersectionVolumes"]["value"].values()) == {0.0}
        assert set(row["nonMatingRodIntersectionVolumes"]["value"].values()) == {0.0}
        assert row["intendedOwnRodEngagementEnvelopeIntersectionVolume"]["value"] > 0.0
    for row in exact_removal["rodLeftCapWithdrawal"].values():
        assert row["maximumIntersectionVolume"]["value"] == 0.0
        assert row["completeWorkpieceIntersectionVolume"]["value"] == 0.0
        assert set(row["otherWithdrawalEnvelopeIntersectionVolumes"]["value"].values()) == {0.0}
        assert set(row["synchronousWithdrawalEnvelopeIntersectionVolumes"]["value"].values()) == {0.0}


def test_domain_a_cap_engagement_endpoints_drive_envelopes_and_omission_fails() -> None:
    p = p13.P13_DEFAULTS
    canonical = p13.cad_source_removal_domain(p)
    left_canonical = p13.build_rod_left_cap_withdrawal_envelope(
        "upright", p, canonical
    ).children[1]
    right_canonical = p13.build_right_cap_stage1_envelope("upright", p, canonical)

    lower_changed = deepcopy(canonical)
    lower_changed["variables"]["left_cap_engagement_each"]["bounds"][0] -= 0.10
    lower_changed["variables"]["right_cap_engagement_each"]["bounds"][0] -= 0.10
    left_lower = p13.build_rod_left_cap_withdrawal_envelope(
        "upright", p, lower_changed
    ).children[1]
    right_lower_certificate = p13.right_cap_stage1_certificate(p, lower_changed)
    assert left_lower.bounding_box().min.X == pytest.approx(
        left_canonical.bounding_box().min.X - 0.10
    )
    assert right_lower_certificate["rows"]["upright"][
        "seatedCapExtentXAtEngagementEndpoints"
    ]["value"]["lower"] != p13.right_cap_stage1_certificate(p, canonical)["rows"][
        "upright"
    ]["seatedCapExtentXAtEngagementEndpoints"]["value"]["lower"]

    upper_changed = deepcopy(canonical)
    upper_changed["variables"]["left_cap_engagement_each"]["bounds"][1] += 0.10
    upper_changed["variables"]["right_cap_engagement_each"]["bounds"][1] += 0.10
    left_upper = p13.build_rod_left_cap_withdrawal_envelope(
        "upright", p, upper_changed
    ).children[1]
    right_upper = p13.build_right_cap_stage1_envelope("upright", p, upper_changed)
    assert left_upper.bounding_box().max.X == pytest.approx(
        left_canonical.bounding_box().max.X + 0.10
    )
    assert right_upper.bounding_box().min.X == pytest.approx(
        right_canonical.bounding_box().min.X - 0.10
    )

    removal = p13.continuous_removal_certificate(p)
    omitted_stage = deepcopy(removal)
    del omitted_stage["rightCapStage1Removal"]
    with pytest.raises(ValueError, match="missing stages"):
        p13.validate_continuous_removal_certificate(omitted_stage)
    omitted_row = deepcopy(removal)
    del omitted_row["rodLeftCapWithdrawal"]["diagonal"]
    with pytest.raises(ValueError, match="incomplete rod rows"):
        p13.validate_continuous_removal_certificate(omitted_row)


def test_full_normal_removal_sequence_is_collision_free_and_structure_invariant() -> None:
    assert p13.P13_DEFAULTS.removal_lift == pytest.approx(20.80362735541403, abs=1e-12)
    run_geometry_case("removal")


def test_domain_a_global_command_is_closed_form_outward_and_not_the_nominal_seed() -> None:
    p = p13.P13_DEFAULTS
    domain = p13.cad_source_removal_domain(p)
    p13.validate_cad_source_removal_domain(domain, p)
    certificate = p13.cad_source_global_removal_certificate(p)
    assert certificate["status"] == "CAD_SOURCE_DOMAIN_CERTIFIED"
    assert certificate["physicalRecordStatus"] == "PHYSICAL_RECORD_NOT_INSTANTIATED"
    assert certificate["coverageComplete"] and certificate["converged"]
    assert certificate["certifiedBracket"]["width"] <= p13.P13_EPS_GLOBAL_MM + 1e-12
    assert certificate["endpointMargin"]["value"] > 0.0
    assert "rightCapS1HandledBeforeLift" not in certificate
    assert certificate["rightCapStage1Coverage"] == {
        "status": "CERTIFIED_BY_CONTINUOUS_REMOVAL_CERTIFICATE",
        "certificatePath": "removal.rightCapStage1Removal",
        "engagementDomainSource": "domain.variables.right_cap_engagement_each.bounds",
        "rollDomainSource": "domain.variables.right_cap_roll_each.bounds",
    }
    command = certificate["globalRemovalCommand"]["value"]
    assert command == pytest.approx(20.855, abs=1e-12)
    assert command != pytest.approx(p.removal_lift, abs=1e-6)
    assert f"global_command_{str(command).replace('.', 'p')}mm" in p13.build_remove(p).label

    incomplete = deepcopy(domain)
    del incomplete["variables"]["right_cap_roll_each"]
    with pytest.raises(ValueError, match="domain gap"):
        p13.validate_cad_source_removal_domain(incomplete, p)


def test_right_fixed_roll_is_a_complete_s1_projection_with_staged_admissibility() -> None:
    p = p13.P13_DEFAULTS
    domain = p13.cad_source_removal_domain(p)
    roll = domain["variables"]["right_fixed_roll"]
    assert roll == {
        "unit": "degree",
        "bounds": [0.0, 360.0],
        "kind": "periodic-S1-projection-with-stage-correlated-admissibility",
    }
    union = domain["rightFixedRollAdmissibleUnion"]
    p13.validate_right_fixed_roll_stage_union(union, p)
    assert union["projection"]["completeS1"]
    assert set(union["stages"]) == {
        "D0-operate",
        "D1-caps-off",
        "D2-engaged-withdrawal",
        "D3-rods-clear",
        "D4-workpiece-lift",
        "D5-empty-service-prealign",
        "D6-keeper-off-release",
    }

    independent = deepcopy(domain)
    independent["variables"]["right_fixed_roll"]["kind"] = "periodic-S1-independent"
    with pytest.raises(ValueError, match="domain gap"):
        p13.validate_cad_source_removal_domain(independent, p)
    omitted = deepcopy(union)
    del omitted["stages"]["D4-workpiece-lift"]
    with pytest.raises(ValueError, match="staged correlated union"):
        p13.validate_right_fixed_roll_stage_union(omitted, p)


def test_right_fixed_engaged_component_is_globally_classified_and_seam_connected() -> None:
    p = p13.P13_DEFAULTS
    classification = p13.right_fixed_engaged_roll_classification(p)
    assert classification["proofMethod"] == (
        "endpoint-convex reduction plus Lipschitz interval branch-and-bound"
    )
    assert classification["seamIdentification"] == "0 degree == 360 degree"
    assert classification["samplesUsedForProof"] is False
    assert classification["continuousAlpha0PathForAllTheta"]
    assert classification["nonAlpha0Components"] == []
    assert [row["id"] for row in classification["components"]] == ["alpha0-seam"]
    assert len(classification["boundaryBrackets"]["value"]) == 2
    assert p13.right_fixed_engaged_roll_is_exact_lane_valid(0.0, p)
    assert p13.right_fixed_engaged_roll_is_exact_lane_valid(360.0, p)
    assert not p13.right_fixed_engaged_roll_is_exact_lane_valid(5.0, p)


def test_right_fixed_exact_support_guard_and_staged_state_predicate_fail_closed() -> None:
    p = p13.P13_DEFAULTS
    certificate = p13.right_fixed_roll_certificate(p)
    guard = certificate["supportGuard"]
    assert guard["uClear"]["value"] == pytest.approx(11.90)
    assert guard["uFull"]["value"] == pytest.approx(44.20)
    assert guard["fullWithdrawalGap"]["value"] == pytest.approx(32.30)
    assert guard["boundaryRows"]["below"]["journalRelationJi"] is True
    assert guard["boundaryRows"]["at"]["journalRelationJi"] is False
    assert guard["boundaryRows"]["above"]["journalRelationJi"] is False
    assert certificate["installedFiveDegreeCounterexample"][
        "maximumIntersectionVolume"
    ]["value"] > 0.0
    assert certificate["fullS1AfterClear"]["maximumIntersectionVolume"]["value"] == 0.0
    assert certificate["fullS1AfterClear"]["samplesUsedForProof"] is False
    assert certificate["allRollWorkpieceLift"]["certifiedForEveryAlphaInS1"]
    p13.validate_right_fixed_roll_certificate(certificate)

    journaled = (True, True, True)
    clear = (False, False, False)
    p13.validate_right_fixed_roll_state(
        "D0-operate",
        theta_deg=27.0,
        withdrawal_u=0.0,
        alpha_deg=0.0,
        rod_journal_relations=journaled,
        p=p,
    )
    p13.validate_right_fixed_roll_state(
        "D2-engaged-withdrawal",
        theta_deg=0.0,
        withdrawal_u=guard["uClear"]["value"] - 0.005,
        alpha_deg=1.0,
        rod_journal_relations=journaled,
        p=p,
    )
    p13.validate_right_fixed_roll_state(
        "D3-rods-clear",
        theta_deg=0.0,
        withdrawal_u=guard["uClear"]["value"],
        alpha_deg=197.0,
        rod_journal_relations=clear,
        p=p,
    )

    with pytest.raises(ValueError, match="outside exact alpha0 lane component"):
        p13.validate_right_fixed_roll_state(
            "D0-operate",
            theta_deg=0.0,
            withdrawal_u=0.0,
            alpha_deg=5.0,
            rod_journal_relations=journaled,
            p=p,
        )
    with pytest.raises(ValueError, match="arbitrary right-fixed roll forbidden"):
        p13.validate_right_fixed_roll_state(
            "D3-rods-clear",
            theta_deg=0.0,
            withdrawal_u=guard["uClear"]["value"] - 0.005,
            alpha_deg=90.0,
            rod_journal_relations=journaled,
            p=p,
        )
    with pytest.raises(ValueError, match="jump components"):
        p13.validate_right_fixed_roll_state(
            "D1-caps-off",
            theta_deg=0.0,
            withdrawal_u=0.0,
            alpha_deg=0.0,
            rod_journal_relations=journaled,
            component_id="invented-component",
            p=p,
        )
    with pytest.raises(ValueError, match="all-roll lift certificate"):
        p13.validate_right_fixed_roll_state(
            "D4-workpiece-lift",
            theta_deg=0.0,
            withdrawal_u=guard["uClear"]["value"],
            alpha_deg=180.0,
            rod_journal_relations=clear,
            all_roll_lift_certificate_present=False,
            p=p,
        )
    with pytest.raises(ValueError, match="alpha=0 mouth-up"):
        p13.validate_right_fixed_roll_state(
            "D6-keeper-off-release",
            theta_deg=0.0,
            withdrawal_u=p.rod_withdrawal_distance,
            alpha_deg=1.0,
            rod_journal_relations=clear,
            keeper_installed=False,
            p=p,
        )


def test_right_fixed_roll_certificate_rejects_hidden_cutter_occurrence_and_all_roll_lift() -> None:
    certificate = p13.right_fixed_roll_certificate()
    hidden = deepcopy(certificate)
    del hidden["fullS1AfterClear"]["proofConstituents"]["persistentCutter"]
    with pytest.raises(ValueError, match="hides a cutter or occurrence"):
        p13.validate_right_fixed_roll_certificate(hidden)
    omitted_occurrence = deepcopy(certificate)
    del omitted_occurrence["fullS1AfterClear"]["proofConstituents"][
        "remainingStructureOccurrences"
    ]
    with pytest.raises(ValueError, match="hides a cutter or occurrence"):
        p13.validate_right_fixed_roll_certificate(omitted_occurrence)
    hidden_key = deepcopy(certificate)
    del hidden_key["fullS1AfterClear"]["proofConstituents"][
        "remainingIntegralFeatures"
    ]
    with pytest.raises(ValueError, match="hides a cutter or occurrence"):
        p13.validate_right_fixed_roll_certificate(hidden_key)
    omitted_lift = deepcopy(certificate)
    omitted_lift["allRollWorkpieceLift"]["certifiedForEveryAlphaInS1"] = False
    with pytest.raises(ValueError, match="omits all-roll workpiece lift"):
        p13.validate_right_fixed_roll_certificate(omitted_lift)


def _valid_physical_record(tmp_path: Path) -> dict[str, object]:
    p = p13.P13_DEFAULTS
    custom = {
        "rod_upright": p13.build_rod("upright", p.open_angle_deg, p),
        "rod_bottom": p13.build_rod("bottom", p.open_angle_deg, p),
        "rod_diagonal": p13.build_rod("diagonal", p.open_angle_deg, p),
        "complete_workpiece": p13.build_workpiece(p),
        "frame_esc_reference": p13.build_electronics_reference(p),
        "iron_left": p13.build_solder_tool(-p.wire_x, p),
        "iron_right": p13.build_solder_tool(p.wire_x, p),
    }
    paths: dict[str, Path] = {
        "left_cam": CAD / "p13_left_cam.step",
        "left_fixed": CAD / "p13_fixed_guide.step",
        "right_fixed": CAD / "p13_fixed_guide.step",
        "right_actuator": CAD / "p13_right_actuator.step",
        "separate_D_shaft": CAD / "p13_actuator_shaft.step",
        "shaft_keeper": CAD / "p13_shaft_keeper.step",
        "left_cap_upright": CAD / "p13_left_cap.step",
        "left_cap_bottom": CAD / "p13_left_cap.step",
        "left_cap_diagonal": CAD / "p13_left_cap.step",
        "right_cap_upright": CAD / "p13_right_cap.step",
        "right_cap_bottom": CAD / "p13_right_cap.step",
        "right_cap_diagonal": CAD / "p13_right_cap.step",
    }
    for role, shape in custom.items():
        path = tmp_path / f"{role}.step"
        assert export_step(shape, path)
        paths[role] = path

    timestamp = "2026-08-20T23:30:00Z"
    specimen_id = "P13-specimen-001"
    frame = {
        "units": "millimetre",
        "convention": "right-handed",
        "transform": [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    }

    def measurement(value: float, lower: float, upper: float) -> dict[str, object]:
        return {
            "value": value,
            "uncertainty": 0.01,
            "unit": "millimetre",
            "range": [lower, upper],
            "method": "registered CMM measurement",
            "measured_at_utc": timestamp,
        }

    schema = p13.physical_record_schema()
    frames = {role: deepcopy(frame) for role in schema["requiredBREPs"]}
    breps = {
        role: {
            "role": role,
            "path": str(path),
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "registrationFrame": frames[role],
            "provenance": {
                "specimen_id": specimen_id,
                "role": role,
                "measured_at_utc": timestamp,
                "method": "registered STEP reconstruction",
                "source": f"fixture scan for {role}",
            },
        }
        for role, path in paths.items()
    }
    return {
        "specimen_id": specimen_id,
        "measurement_provenance": {
            "operator": "test-metrologist",
            "instrument_ids": ["CMM-001", "CALIPER-001"],
            "method": "registered metrology fixture",
            "measured_at_utc": timestamp,
        },
        "registration_frames": frames,
        "lane_profiles": {
            name: {"width": measurement(4.75, 4.70, 4.80), "depth": measurement(2.8, 2.7, 2.9), "sampleCount": 5}
            for name in p13.ROD_NAMES
        },
        "bore_key_journal_keeper_geometry": {
            "cam_d_bore_od": measurement(5.70, 5.65, 5.75),
            "cam_d_bore_across_flat": measurement(5.25, 5.20, 5.30),
            "fixed_journal_id": measurement(4.80, 4.75, 4.85),
            "keeper_id": measurement(4.80, 4.75, 4.85),
        },
        "rod_end_frames_and_straightness": {
            name: {
                "leftEndX": measurement(-25.0, -25.1, -24.9),
                "rightEndX": measurement(25.0, 24.9, 25.1),
                "straightness": measurement(0.03, 0.0, 0.08),
            }
            for name in p13.ROD_NAMES
        },
        "left_cap_seated_engagements": {
            name: measurement(2.75, 2.50, 3.00) for name in p13.ROD_NAMES
        },
        "movable_component_domains": {
            name: {
                "lower": 0.0, "upper": 360.0, "uncertainty": 0.1,
                "unit": "degree", "periodic": True,
                "method": "rotary stage sweep", "measured_at_utc": timestamp,
            }
            for name in ("right_fixed_roll", "keeper_roll", "rod_roll_each", "right_cap_roll_each")
        },
        "breps": breps,
    }


def test_domain_b_measured_record_is_strict_and_cannot_pass_when_absent_or_stale(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="PHYSICAL_RECORD_NOT_INSTANTIATED"):
        p13.validate_physical_record(None)
    with pytest.raises(ValueError, match="incomplete measured specimen record"):
        p13.validate_physical_record({})
    record = _valid_physical_record(tmp_path)
    fake = tmp_path / "not-a-brep.txt"
    fake.write_text("not a BREP")
    fake_hash = sha256(fake.read_bytes()).hexdigest()
    for entry in record["breps"].values():
        entry["path"] = str(fake)
        entry["sha256"] = fake_hash
    with pytest.raises(ValueError, match="existing STEP/STP"):
        p13.validate_physical_record(record)

    fake_step = tmp_path / "not-a-brep.step"
    fake_step.write_text("not a BREP")
    fake_step_hash = sha256(fake_step.read_bytes()).hexdigest()
    for entry in record["breps"].values():
        entry["path"] = str(fake_step)
        entry["sha256"] = fake_step_hash
    with pytest.raises(ValueError, match="fresh-process STEP parse failed|no valid positive-volume solid"):
        p13.validate_physical_record(record)


def test_domain_b_valid_typed_record_with_real_step_leaves_passes(tmp_path: Path) -> None:
    p13.validate_physical_record(_valid_physical_record(tmp_path))


def test_domain_b_rejects_bad_frame_nan_measurement_timestamp_and_incompatible_alias(tmp_path: Path) -> None:
    record = _valid_physical_record(tmp_path)
    reflected = deepcopy(record)
    reflected["registration_frames"]["left_cam"]["transform"][0] = -1.0
    reflected["breps"]["left_cam"]["registrationFrame"] = reflected["registration_frames"]["left_cam"]
    with pytest.raises(ValueError, match=r"determinant must be \+1"):
        p13.validate_physical_record(reflected)

    nan_record = deepcopy(record)
    nan_record["lane_profiles"]["upright"]["width"]["uncertainty"] = float("nan")
    with pytest.raises(ValueError, match="contains invalid"):
        p13.validate_physical_record(nan_record)

    stale = deepcopy(record)
    stale["left_cap_seated_engagements"]["upright"]["measured_at_utc"] = "2026-08-20T23:31:00Z"
    with pytest.raises(ValueError, match="contains invalid"):
        p13.validate_physical_record(stale)

    incompatible = deepcopy(record)
    incompatible["breps"]["complete_workpiece"]["path"] = incompatible["breps"]["left_cam"]["path"]
    incompatible["breps"]["complete_workpiece"]["sha256"] = incompatible["breps"]["left_cam"]["sha256"]
    with pytest.raises(ValueError, match="STEP label does not match role|incompatible BREP roles"):
        p13.validate_physical_record(incompatible)


def test_ast_dependency_graph_closes_known_semantic_misses_and_rejects_dynamic_getattr() -> None:
    uses = p13.parameter_source_use_map()
    assert uses["dynamicGetattr"] == []
    assert "continuous_removal_certificate" in uses["terminalConsumers"]["open_angle_deg"]
    assert "continuous_lane_solid_certificate" in uses["terminalConsumers"]["continuous_overlap_volume_tolerance"]
    assert "build_left_cam" in uses["terminalConsumers"]["cam_d_bore_od"]
    assert "build_right_actuator" in uses["terminalConsumers"]["cam_d_bore_od"]
    graph = p13.parameter_dependency_graph()
    assert "effect-domain:cam-D-bore" in graph["cam_d_bore_od"]
    assert "actual-terminal:build_left_cam" in graph["cam_d_bore_od"]
    assert "actual-terminal:build_right_actuator" in graph["cam_d_bore_od"]

    base = p13.P13_DEFAULTS
    opened = replace(base, open_angle_deg=1.0)
    assert p13.build_rod_left_cap_withdrawal_envelope("upright", opened).bounding_box().center() != \
        p13.build_rod_left_cap_withdrawal_envelope("upright", base).bounding_box().center()
    tolerance = replace(base, continuous_overlap_volume_tolerance=2.0e-7)
    assert p13.continuous_overlap_tolerance(tolerance) == 2.0e-7
    bore = replace(base, cam_d_bore_od=5.80)
    assert p13._cam_d_bore_cutter(0.0, 2.0, bore).volume != pytest.approx(
        p13._cam_d_bore_cutter(0.0, 2.0, base).volume
    )


def test_forbidden_axial_shaft_through_installed_id4p80_journals_is_rejected() -> None:
    run_geometry_case("forbidden")


def test_coupons_are_each_one_solid_in_source_and_fresh_step(tmp_path: Path) -> None:
    path = tmp_path / "fit_coupons.step"
    run_geometry_case("coupons", path)


def test_print_kit_and_exploded_have_complete_allowed_census() -> None:
    run_geometry_case("print")


def test_declared_wrappers_and_every_step_have_no_skip_source_parity() -> None:
    wrappers = {path.stem.removesuffix(".step") for path in CAD.glob("p13_*.step.py")}
    # The motion entry is review-only: it re-groups exact production solids for
    # viewer transforms and is intentionally outside production artifact parity.
    assert wrappers - {"p13_motion"} == {
        f"p13_{name}" for name in p13.P13_ARTIFACT_NAMES
    }
    missing = [name for name in p13.P13_ARTIFACT_NAMES if not (CAD / f"p13_{name}.step").exists()]
    assert not missing, f"missing generated P13 STEP artifacts: {missing}"
    for name in p13.P13_ARTIFACT_NAMES:
        run_geometry_case("parity", name, CAD / f"p13_{name}.step")


@pytest.mark.parametrize(
    "overrides,artifact",
    (
        ({"c_sw": 0.60}, "fixed_guide"),
        ({"wire_diameter_design": 4.25}, "fixed_guide"),
        ({"diagnostic_lane_pitch": 5.60}, "fit_coupons"),
        ({"c_sw": 0.65, "wire_diameter_design": 4.20}, "fixed_guide"),
    ),
)
def test_fresh_process_safe_metamorphic_step_generation(overrides, artifact, tmp_path: Path) -> None:
    output = tmp_path / f"{artifact}.step"
    command = [
        sys.executable,
        "-m",
        "xt60_bend_jig.p13_four_plate_three_rod",
        "--artifact",
        artifact,
        "--output",
        str(output),
        "--params-json",
        json.dumps(overrides),
    ]
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    run_geometry_case("parity", artifact, output, json.dumps(overrides))


def test_repeat_generation_for_identical_manifest_is_byte_deterministic(tmp_path: Path) -> None:
    paths = [tmp_path / "repeat_a.step", tmp_path / "repeat_b.step"]
    for path in paths:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "xt60_bend_jig.p13_four_plate_three_rod",
                "--artifact",
                "fixed_guide",
                "--output",
                str(path),
                "--params-json",
                '{"c_sw":0.6}',
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    assert sha256(paths[0].read_bytes()).hexdigest() == sha256(paths[1].read_bytes()).hexdigest()


def test_written_production_3mf_principal_bed_contact_matches_provenance() -> None:
    three_mf = CAD / "p13_print_kit.3mf"
    provenance = json.loads((CAD / "p13-3mf-provenance.json").read_text())
    production = provenance["production"]
    for artifact_role in ("production", "coupons"):
        sidecar = provenance[artifact_role]
        assert sidecar["parentBriefSha256"] == p13.P13_GATE0_BRIEF_SHA256
        assert (
            sidecar["controllingAmendmentSha256"]
            == p13.P13_DOMAIN_AMENDMENT_SHA256
        )
        assert sidecar["embeddedMetadata"]["parentBriefSha256"] == p13.P13_GATE0_BRIEF_SHA256
        assert (
            sidecar["embeddedMetadata"]["controllingAmendmentSha256"]
            == p13.P13_DOMAIN_AMENDMENT_SHA256
        )
    principal_labels = set(production["principalBedContact"]["labels"])
    assert len(principal_labels) == 4
    assert production["principalBedContact"]["writtenRoundTripValidated"]
    assert production["principalBedContact"][
        "minimumRequiredCoplanarZ0TriangleAreaMm2"
    ] == pytest.approx(1000.0)
    rows = {row["label"]: row for row in production["objects"]}

    wrapper = lib3mf.Wrapper()
    namespace = "https://openai.com/codex/xt60-bend-jig/p13"
    for artifact_role in ("production", "coupons"):
        written_model = wrapper.CreateModel()
        written_model.QueryReader("3mf").ReadFromFile(
            str(ROOT / provenance[artifact_role]["path"])
        )
        written_metadata = written_model.GetMetaDataGroup()
        assert written_metadata.GetMetaDataByKey(
            namespace, "parentBriefSha256"
        ).GetValue() == p13.P13_GATE0_BRIEF_SHA256
        assert written_metadata.GetMetaDataByKey(
            namespace, "controllingAmendmentSha256"
        ).GetValue() == p13.P13_DOMAIN_AMENDMENT_SHA256

    model = wrapper.CreateModel()
    model.QueryReader("3mf").ReadFromFile(str(three_mf))
    metadata = model.GetMetaDataGroup()
    assert metadata.GetMetaDataByKey(
        namespace, "parentBriefSha256"
    ).GetValue() == p13.P13_GATE0_BRIEF_SHA256
    assert metadata.GetMetaDataByKey(
        namespace, "controllingAmendmentSha256"
    ).GetValue() == p13.P13_DOMAIN_AMENDMENT_SHA256
    iterator = model.GetMeshObjects()
    observed = set()
    while iterator.MoveNext():
        mesh = iterator.GetCurrentMeshObject()
        label = mesh.GetName()
        if label not in principal_labels:
            continue
        observed.add(label)
        vertices = [
            tuple(float(value) for value in vertex.Coordinates)
            for vertex in mesh.GetVertices()
        ]
        triangles = [
            tuple(int(value) for value in triangle.Indices)
            for triangle in mesh.GetTriangleIndices()
        ]
        minimum_z = min(vertex[2] for vertex in vertices)
        assert minimum_z >= -1.0e-6
        assert minimum_z == pytest.approx(0.0, abs=1.0e-6)
        bed_area = 0.0
        for first, second, third in triangles:
            a, b, c = vertices[first], vertices[second], vertices[third]
            if all(abs(point[2]) <= 1.0e-6 for point in (a, b, c)):
                bed_area += abs(
                    (b[0] - a[0]) * (c[1] - a[1])
                    - (b[1] - a[1]) * (c[0] - a[0])
                ) / 2.0
        assert bed_area > 1000.0
        written = rows[label]["writtenRoundTripBedContact"]
        assert written["minimumZMm"] == pytest.approx(minimum_z, abs=1.0e-9)
        assert written["boundsZMm"][0] == pytest.approx(minimum_z, abs=1.0e-9)
        assert written["coplanarZ0TriangleAreaMm2"] == pytest.approx(
            bed_area, abs=1.0e-6
        )
    assert observed == principal_labels


def test_regate_fields_are_blocked_without_explicit_gate_override() -> None:
    with pytest.raises(ValueError, match="renewed Gate-0"):
        p13.parameters_from_overrides({"shaft_od": 5.65})
    changed = p13.parameters_from_overrides({"shaft_od": 5.65}, allow_regate=True)
    assert changed.shaft_od == 5.65
    assert changed.pivot_delta != p13.P13_DEFAULTS.pivot_delta


def test_evidence_files_match_current_source_manifest_and_all_step_hashes() -> None:
    manifest_path = ROOT / "docs" / "p13-default-parameter-manifest.json"
    graph_path = ROOT / "docs" / "p13-dependency-graph.json"
    provenance_path = CAD / "p13-artifact-provenance.json"
    continuous_path = ROOT / "docs" / "p13-continuous-certificates.json"
    assert json.loads(manifest_path.read_text()) == p13.parameter_manifest()
    assert json.loads(graph_path.read_text()) == p13.parameter_dependency_graph()
    continuous = json.loads(continuous_path.read_text())
    assert continuous == p13.continuous_certificate_package()
    assert continuous["removal"]["completeWorkpieceLift"]["globalMargin"]["value"] > 0.0
    assert all(
        row["maximumIntersectionVolume"]["value"] == 0.0
        for row in continuous["removal"]["rodLeftCapWithdrawal"].values()
    )
    provenance = json.loads(provenance_path.read_text())
    assert provenance == p13.evidence_package()
    assert all(row["exists"] and row["stepSha256"] for row in provenance["artifacts"].values())
    for name, row in provenance["artifacts"].items():
        assert row["briefSha256"] == p13.P13_GATE0_BRIEF_SHA256
        assert row["domainAmendmentSha256"] == p13.P13_DOMAIN_AMENDMENT_SHA256
        assert p13.P13_GATE0_BRIEF_SHA256 in row["provenanceRoot"]
        assert p13.P13_DOMAIN_AMENDMENT_SHA256 in row["provenanceRoot"]
        step_text_without_line_wraps = (ROOT / row["path"]).read_text().replace("\n", "")
        assert row["provenanceRoot"] in step_text_without_line_wraps, name
    written_step_paths = sorted(CAD.glob("p13_*.step"))
    assert len(written_step_paths) == 24
    for path in written_step_paths:
        step_text_without_line_wraps = path.read_text().replace("\n", "")
        assert p13.P13_GATE0_BRIEF_SHA256 in step_text_without_line_wraps, path.name
        assert p13.P13_DOMAIN_AMENDMENT_SHA256 in step_text_without_line_wraps, path.name


def test_validation_boundary_does_not_overclaim_physical_acceptance() -> None:
    boundary = p13.nominal_validation_boundary()
    assert "EXPLORATORY NOMINAL ONLY" in boundary
    for unproven in ("strength", "heat", "friction", "springback", "usability"):
        assert unproven in boundary
