"""Third-review direct evidence gates for KAGE Revision K.

Every assertion consumes production solids or re-imported deliverables.  A
report dictionary, witness cone/ring, or replacement locator is not accepted
as evidence for the physical mechanism it describes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json
from math import cos, hypot, pi, radians, sin, sqrt
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from build123d import Axis, Compound, export_brep, import_step
import pytest

import p3_v3_direct_gear_race_guidance_r2_geometry as g
from p3_v3_direct_gear_race_guidance_r2_spec import P3_V3_DIRECT_GEAR_RACE_R2 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_r2"
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
STATE_PATHS = {
    "assembled_nominal": MODEL_ROOT / "p3_v3_r2_assembled.step",
    "service_exploded": MODEL_ROOT / "p3_v3_r2_service_exploded.step",
    "powered_min": MODEL_ROOT / "p3_v3_r2_powered_min.step",
    "powered_max": MODEL_ROOT / "p3_v3_r2_powered_max.step",
    "service_min_UNSAFE_TO_POWER": MODEL_ROOT / "p3_v3_r2_service_min_UNSAFE_TO_POWER.step",
    "service_max_UNSAFE_TO_POWER": MODEL_ROOT / "p3_v3_r2_service_max_UNSAFE_TO_POWER.step",
}


def _volume(shape) -> float:
    return sum(s.volume for s in shape.solids()) if shape else 0.0


def _iv(a, b) -> float:
    aa, bb = a.bounding_box(), b.bounding_box()
    if (
        aa.max.X < bb.min.X or bb.max.X < aa.min.X
        or aa.max.Y < bb.min.Y or bb.max.Y < aa.min.Y
        or aa.max.Z < bb.min.Z or bb.max.Z < aa.min.Z
    ):
        return 0.0
    return _volume(a.intersect(b))


def _raw_brep_digest(shape) -> str:
    with NamedTemporaryFile(suffix=".brep") as tmp:
        export_brep(shape, tmp.name)
        return sha256(Path(tmp.name).read_bytes()).hexdigest()


def _facts_digest(shape) -> str:
    box = shape.bounding_box()
    facts = {
        "valid": bool(shape.is_valid),
        "bounds": tuple(round(x, 6) for x in (
            box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z,
        )),
        "volume": round(_volume(shape), 6),
        "faces": len(shape.faces()),
        "edges": len(shape.edges()),
        "solids": len(shape.solids()),
    }
    return sha256(json.dumps(facts, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _full_registry(state="assembled_nominal"):
    """The authoritative registry includes printed and non-printing references."""

    assert hasattr(g, "complete_occurrence_registry"), (
        "Revision K needs one complete occurrence registry; the 94-print-only "
        "registry cannot prove shafts, bearings, fasteners, magnets or keepouts"
    )
    return list(g.complete_occurrence_registry(state))


def _registry_categories(records):
    result = defaultdict(list)
    for row in records:
        result[row["category"]].append(row)
    return result


def test_complete_registry_and_step_retain_real_motor_output_shafts_and_fasteners():
    records = _full_registry()
    cats = _registry_categories(records)
    printed = [row for row in records if row["printable"] is True]
    references = [row for row in records if row["printable"] is False]
    assert len(records) == 127
    assert len(printed) == 94
    assert len(references) == 33
    assert len(cats["motor_shaft_reference"]) == 3
    assert len(cats["output_shaft_reference"]) == 3
    assert len(cats["shaft_bearing_reference"]) == 6
    assert len(cats["shaft_retainer_reference"]) == 6
    assert len(cats["miter_axial_retainer_reference"]) == 3
    assert len(cats["motor_mount_fastener_reference"]) == 12
    required = sum((cats[name] for name in (
        "motor_shaft_reference", "output_shaft_reference",
        "shaft_bearing_reference", "shaft_retainer_reference",
        "miter_axial_retainer_reference", "motor_mount_fastener_reference",
    )), [])
    assert len({row["occurrence_name"] for row in required}) == len(required)
    assert all(row.get("printable") is False for row in required)
    assert all(len(row["transform"]) == 12 and _volume(row["shape"]) > 0 for row in required)

    step = import_step(str(STATE_PATHS["assembled_nominal"]))
    labels = {child.label for child in step.children}
    assert {row["occurrence_name"] for row in required} <= labels


def test_miter_pair_has_positive_drive_teeth_phase_backlash_and_axial_retention():
    for role in range(3):
        station = g.make_motor_station_at_pose(role=role, motor_q_mm=0.0, ring_angle_deg=0.0)
        input_gear, output_gear = station["miter_input"], station["miter_output"]
        # A smooth Cone has only three faces/edges.  Positive drive requires a
        # repeated tooth topology on both members.
        assert len(input_gear.faces()) >= 18 and len(input_gear.edges()) >= 36
        assert len(output_gear.faces()) >= 18 and len(output_gear.edges()) >= 36
        assert _iv(input_gear, output_gear) <= 1e-7

        shaft_box = station["motor_shaft"].bounding_box()
        axis_index = max(range(3), key=lambda i: (shaft_box.size.X, shaft_box.size.Y, shaft_box.size.Z)[i])
        direction = ((1, 0, 0), (0, 1, 0), (0, 0, 1))[axis_index]
        axis = Axis(station["motor_shaft"].bounding_box().center(), direction)
        phase_distances = [
            input_gear.rotate(axis, phase).distance_to(output_gear)
            for phase in (0.0, 3.0, 6.0, 9.0, 12.0, 15.0)
        ]
        assert max(phase_distances) - min(phase_distances) >= 0.02
        assert 0.10 <= min(phase_distances) <= 0.25

    cats = _registry_categories(_full_registry())
    assert len(cats["miter_axial_retainer_reference"]) == 3


def test_all_4096_shells_are_actual_production_guidance_contact_assemblies():
    shells = list(g.iter_revision_k_tolerance_shells())
    assert len(shells) == 4096
    residual_vectors = set()
    flange_vectors = set()
    for shell in shells:
        facts = g.evaluate_tolerance_shell_contact_facts("assembled_nominal", shell)
        assert facts["production_derived"] is True
        assert len(facts["role_facts"]) == 3
        assert all(
            role["production_quadrant_count"] == 4
            and role["production_roller_count"] == 3
            and role["fixed_retaining_lip_count"] == 2
            for role in facts["role_facts"]
        )
        # Each role-local fact is measured from the accepted carrier's cropped
        # guidance race, the actual D9 roller BREP and fixed retaining lips.
        # Only the 48 physically distinct role/sign states are cached; this
        # loop still composes and validates all 4096 exact system shells.
        residuals = tuple(round(value, 5) for value in facts["contact_residuals_mm"])
        overlaps = tuple(round(value, 5) for value in facts["flange_overlap_volumes_mm3"])
        assert max(map(abs, residuals)) <= 0.05
        assert min(overlaps) > 0.0
        residual_vectors.add(residuals)
        flange_vectors.add(overlaps)
    assert g._role_local_tolerance_contact_facts.cache_info().currsize == 48
    assert len(residual_vectors) > 8
    assert len(flange_vectors) > 1


def test_ring_pinion_mesh_metrics_are_derived_by_direct_geometry_phase_sweep():
    rings = [
        row["shape"] for row in g.production_occurrence_registry("assembled_nominal")
        if row["category"] == "moving_carrier_quadrant"
    ]
    pinions = [
        row["shape"] for row in g.production_occurrence_registry("assembled_nominal")
        if row["category"] == "output_pinion"
    ]
    assert len(rings) == 12 and len(pinions) == 3
    for role, pinion in enumerate(pinions):
        ring = Compound(children=rings[role * 4:(role + 1) * 4])
        centre = pinion.bounding_box().center()
        axis = Axis((centre.X, centre.Y, centre.Z), (0, 0, 1))
        samples = []
        for index in range(129):
            phase = (360.0 / p.pinion_teeth) * index / 128.0
            moved = pinion.rotate(axis, phase)
            samples.append((_iv(moved, ring), moved.distance_to(ring)))
        collision_free = [i for i, (overlap, _) in enumerate(samples) if overlap <= 1e-7]
        assert collision_free
        backlash_deg = len(collision_free) / 128.0 * (360.0 / p.pinion_teeth)
        # Backlash is tangential clearance at the mesh, so convert the
        # geometry-derived free phase using the *pinion pitch radius*.  The
        # previous 122 mm motor-centre orbit radius measured unrelated global
        # travel and made even one 1/128-tooth sample equal 0.374 mm.  For the
        # frozen module-1, 16T pinion the pitch radius is 8 mm and the result
        # below is millimetres of tangential pinion-pitch-line clearance.
        pinion_pitch_radius_mm = p.gear_module * p.pinion_teeth / 2.0
        assert pinion_pitch_radius_mm == pytest.approx(8.0)
        backlash_mm_at_pinion_pitch_line = (
            pinion_pitch_radius_mm
            * backlash_deg
            * 3.141592653589793
            / 180.0
        )
        minimum_free_distance_mm = min(
            distance for overlap, distance in samples if overlap <= 1e-7
        )
        # One complete 16T pinion-tooth pitch is periodic.  A conventional
        # clearance window has one entry and one exit, hence exactly two
        # Boolean transitions.  Treat sample 127 -> sample 0 as adjacent so a
        # free window crossing the phase origin is still counted correctly.
        periodic_free = [overlap <= 1e-7 for overlap, _ in samples[:-1]]
        transitions = sum(
            periodic_free[index] != periodic_free[(index + 1) % len(periodic_free)]
            for index in range(len(periodic_free))
        )
        assert (
            0.10 <= backlash_mm_at_pinion_pitch_line <= 0.25
            and minimum_free_distance_mm <= 0.05
            and transitions == 2
        ), (
            f"role {role}: backlash={backlash_mm_at_pinion_pitch_line:.6f} mm "
            f"at pinion pitch line, minimum_free_distance={minimum_free_distance_mm:.6f} mm, "
            f"periodic_transitions={transitions}; expected 0.10-0.25 mm, <=0.05 mm, "
            "and exactly 2 transitions"
        )


def test_internal_involute_contact_ratio_uses_brep_addendum_and_root_geometry():
    """Contact ratio is independent of free-window transition count.

    For an external pinion meshing with an internal ring, the transverse path
    of contact is::

        sqrt(ra_p^2-rb_p^2) + a*sin(alpha)
        - sqrt(ra_r^2-rb_r^2)

    Dividing by the base pitch ``pi*m*cos(alpha)`` gives dimensionless contact
    ratio.  Pitch/base radii come from the frozen module/tooth counts; pinion
    addendum and root radii are measured from the production BREP; ring
    addendum/root radii are frozen production geometry.  This is not inferred
    from transition count and cannot be satisfied by a smooth witness disc.
    """

    pressure_angle = radians(20.0)
    pinion_pitch_radius = p.gear_module * p.pinion_teeth / 2.0
    ring_pitch_radius = p.gear_module * p.ring_teeth / 2.0
    centre_distance = ring_pitch_radius - pinion_pitch_radius
    pinion_base_radius = pinion_pitch_radius * cos(pressure_angle)
    ring_base_radius = ring_pitch_radius * cos(pressure_angle)
    ring_addendum_radius = p.tooth_tip_radius
    ring_root_radius = p.tooth_root_radius
    base_pitch = pi * p.gear_module * cos(pressure_angle)

    assert centre_distance == pytest.approx(122.0)
    assert ring_base_radius < ring_addendum_radius < ring_pitch_radius < ring_root_radius

    pinions = [
        row["shape"] for row in g.production_occurrence_registry("assembled_nominal")
        if row["category"] == "output_pinion"
    ]
    assert len(pinions) == 3
    for pinion in pinions:
        centre = pinion.bounding_box().center()
        pinion_addendum_radius = max(
            hypot(vertex.X - centre.X, vertex.Y - centre.Y)
            for vertex in pinion.vertices()
        )
        external_circle_radii = [
            edge.radius
            for edge in pinion.edges()
            if edge.geom_type.name == "CIRCLE"
            and edge.radius > 0.5 * pinion_pitch_radius
        ]
        assert external_circle_radii
        pinion_root_radius = min(external_circle_radii)

        assert pinion_root_radius < pinion_base_radius < pinion_pitch_radius
        assert pinion_addendum_radius > pinion_pitch_radius, (
            "positive involute addendum must extend beyond the 8 mm pitch "
            f"radius; production BREP reaches only {pinion_addendum_radius:.3f} mm"
        )
        path_of_contact_mm = (
            sqrt(pinion_addendum_radius**2 - pinion_base_radius**2)
            + centre_distance * sin(pressure_angle)
            - sqrt(ring_addendum_radius**2 - ring_base_radius**2)
        )
        contact_ratio = path_of_contact_mm / base_pitch
        assert contact_ratio >= 1.20


def test_written_step_state_occurrences_match_manifest_raw_brep_and_facts_digests():
    manifest = json.loads((MODEL_ROOT / "manifest.json").read_text())
    assert manifest["canonicalBrepDigestAlgorithm"] == "build123d-export-brep-sha256-v1"
    parity = manifest["stateParity"]
    assert set(parity) == set(STATE_PATHS)
    for state, path in STATE_PATHS.items():
        root = import_step(str(path))
        written = {child.label: child for child in root.children}
        rows = parity[state]["occurrences"]
        assert set(written) == {row["name"] for row in rows}
        for row in rows:
            shape = written[row["name"]]
            assert row["brepDigest"] == _raw_brep_digest(shape)
            assert row["factsDigest"] == _facts_digest(shape)
        state_payload = "".join(
            f"{name}:{_raw_brep_digest(written[name])}" for name in sorted(written)
        )
        assert parity[state]["stateDigest"] == sha256(state_payload.encode()).hexdigest()


def test_service_steps_remove_powered_keys_without_substitute_locator_geometry():
    for state in ("service_min_UNSAFE_TO_POWER", "service_max_UNSAFE_TO_POWER"):
        source_labels = {
            row["occurrence_name"] for row in g.production_occurrence_registry(state)
        }
        written = import_step(str(STATE_PATHS[state]))
        written_labels = {child.label for child in written.children}
        assert source_labels == written_labels
        assert not any("powered_window_key" in label or "locator" in label for label in written_labels)
        assert len(written_labels) == p.production_printed_occurrence_count - 3


def test_all_frozen_spine_cassette_stop_fixed_seam_cap_and_key_interfaces_are_material():
    records = list(g.production_occurrence_registry("assembled_nominal"))
    cats = _registry_categories(records)
    assert len(cats["tower_300_structural_spine"]) == 1
    assert len(cats["tower_300_role_slider_cassette"]) == 3
    assert len(cats["tower_300_three_window_stop_plate"]) == 1
    assert len(cats["fixed_tower_leaf"]) == 2
    assert len(cats["selected_fixed_tower_shim"]) == 4
    assert len(cats["moving_recessed_seam_plate"]) == 12
    assert len(cats["hall_pocket_cap"]) == 3
    assert len(cats["balance_pocket_cap"]) == 9
    assert len(cats["stationary_joint_registration_key"]) == 16

    spine = cats["tower_300_structural_spine"][0]["shape"]
    assert len(spine.faces()) >= 18, "spine needs real mount/guide/insert receiver topology"
    for cassette in cats["tower_300_role_slider_cassette"]:
        box = cassette["shape"].bounding_box()
        assert max(box.size.X, box.size.Y) >= 18.0, "integral D3 stop pin must project 4 mm from 14 mm cassette"
        assert len(cassette["shape"].faces()) >= 20
    stop_plate = cats["tower_300_three_window_stop_plate"][0]["shape"]
    assert len(stop_plate.faces()) >= 30, "three windows, fasteners and reversal key must be actual cuts/features"

    for seam in cats["moving_recessed_seam_plate"]:
        box = seam["shape"].bounding_box()
        assert box.size.Z == pytest.approx(2.00, abs=0.03)
        assert sorted((box.size.X, box.size.Y)) == pytest.approx((6.80, 18.00), abs=0.08)
        assert len(seam["shape"].faces()) >= 14, "two M2 holes and dowel interface must exist"
    for cap in cats["hall_pocket_cap"] + cats["balance_pocket_cap"]:
        box = cap["shape"].bounding_box()
        assert max(box.size.X, box.size.Y) == pytest.approx(4.08, abs=0.08)
        assert box.size.Z == pytest.approx(0.40, abs=0.03)
    for key in cats["stationary_joint_registration_key"]:
        box = key["shape"].bounding_box()
        assert sorted((box.size.X, box.size.Y)) == pytest.approx((4.0, 6.0), abs=0.05)
        assert box.size.Z == pytest.approx(2.5, abs=0.05)


def test_orca_project_and_coupon_evidence_are_native_source_derived_structures():
    production = MODEL_ROOT / "print" / "p3_v3_r2_production_94.3mf"
    with ZipFile(production) as package:
        names = set(package.namelist())
        assert "Metadata/model_settings.config" in names
        assert "Metadata/project_settings.config" in names
        settings = package.read("Metadata/model_settings.config")
        assert settings.count(b"<plate") >= 2
        assert b"slice_error" not in settings.lower()

    coupon_manifest = json.loads((MODEL_ROOT / "coupons" / "manifest.json").read_text())
    assert coupon_manifest["canonicalBrepDigestAlgorithm"] == "build123d-export-brep-sha256-v1"
    assert coupon_manifest["orcaReload"]["status"] == "passed"
    assert coupon_manifest["completeStation"]["printingOccurrenceCount"] == 5
    assert coupon_manifest["completeStation"]["referenceOccurrenceCount"] > 20
    assert coupon_manifest["stationLadder"]["cellCount"] == 18
    assert coupon_manifest["fixedLadder"]["keyedShimPairCount"] == 9
    assert coupon_manifest["fixedLadder"]["pairedBoreCellCount"] == 3
    assert all(
        row["sourceBrepDigest"] and row["sourceOccurrence"] and row["interfaceFamily"]
        for row in coupon_manifest["allObjects"]
    )
