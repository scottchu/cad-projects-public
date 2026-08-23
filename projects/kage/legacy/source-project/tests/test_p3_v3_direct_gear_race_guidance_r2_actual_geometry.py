"""Non-reportable Revision-K geometry, motion, and manufacturing gates.

The companion contract module freezes numbers and public APIs.  This module
deliberately ignores self-reported ``used_actual_brep`` booleans: it consumes
Build123d solids, written STEP occurrences, and raw 3MF triangles itself.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import json
from math import cos, hypot, isclose, radians, sin
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from build123d import Align, Axis, Compound, Cylinder, Location
import pytest

import p3_v3_direct_gear_race_guidance_r2_geometry as g
from p3_v3_direct_gear_race_guidance_r2_spec import P3_V3_DIRECT_GEAR_RACE_R2 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_r2"
PRODUCTION_3MF = MODEL_ROOT / "print" / "p3_v3_r2_production_94.3mf"
MANIFEST = MODEL_ROOT / "manifest.json"
ROLE_KEYS = ("H", "M", "S")
ROLES = ("hour", "minute", "second")
RADIAL_KEYS = tuple(f"{role}{angle}" for role in ROLE_KEYS for angle in (60, 180, 300))
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}


def _volume(shape) -> float:
    return sum(solid.volume for solid in shape.solids()) if shape else 0.0


def _intersection_volume(left, right) -> float:
    a, b = left.bounding_box(), right.bounding_box()
    if (
        a.max.X < b.min.X or b.max.X < a.min.X
        or a.max.Y < b.min.Y or b.max.Y < a.min.Y
        or a.max.Z < b.min.Z or b.max.Z < a.min.Z
    ):
        return 0.0
    return _volume(left.intersect(right))


def _shape_facts(shape) -> dict:
    box = shape.bounding_box()
    return {
        "valid": bool(shape.is_valid),
        "bounds": tuple(round(value, 6) for value in (
            box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z,
        )),
        "volume": round(_volume(shape), 6),
        "faces": len(shape.faces()),
        "edges": len(shape.edges()),
        "solids": len(shape.solids()),
    }


def _facts_digest(shape) -> str:
    payload = json.dumps(_shape_facts(shape), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode()).hexdigest()


def _children_by_prefix(assembly, prefix: str):
    return [child for child in assembly.children if child.label.startswith(prefix)]


def _require_shape_api(name: str):
    assert hasattr(g, name), (
        f"RED: {name} must return real Build123d solids; a numeric/report "
        "dictionary is not acceptable evidence"
    )
    return getattr(g, name)


def _read_3mf(path: Path):
    with ZipFile(path) as package:
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    objects = {}
    for obj in root.findall(".//m:resources/m:object", NS):
        vertices = [
            (float(v.attrib["x"]), float(v.attrib["y"]), float(v.attrib["z"]))
            for v in obj.findall(".//m:vertices/m:vertex", NS)
        ]
        triangles = [
            (int(t.attrib["v1"]), int(t.attrib["v2"]), int(t.attrib["v3"]))
            for t in obj.findall(".//m:triangles/m:triangle", NS)
        ]
        metadata = {
            node.attrib.get("name"): (node.text or "")
            for node in obj.findall("m:metadata", NS)
        }
        objects[obj.attrib["id"]] = {
            "name": obj.attrib.get("name", ""),
            "vertices": vertices,
            "triangles": triangles,
            "metadata": metadata,
        }
    items = [dict(item.attrib) for item in root.findall(".//m:build/m:item", NS)]
    return objects, items


def _transform_point(point, transform: str | None):
    if not transform:
        return point
    values = tuple(float(value) for value in transform.split())
    assert len(values) == 12, "3MF transform must be a 3x4 affine matrix"
    x, y, z = point
    return (
        values[0] * x + values[3] * y + values[6] * z + values[9],
        values[1] * x + values[4] * y + values[7] * z + values[10],
        values[2] * x + values[5] * y + values[8] * z + values[11],
    )


def _step_occurrence_facts(paths: tuple[Path, ...]) -> dict[str, dict]:
    """Inspect large STEP states in one isolated OCC process."""

    program = r'''
import hashlib
import json
import sys
from build123d import import_step

def facts(shape):
    box = shape.bounding_box()
    return {
        "label": shape.label,
        "bounds": [round(value, 5) for value in (
            box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z
        )],
        "volume": round(sum(s.volume for s in shape.solids()), 5),
        "faces": len(shape.faces()),
        "solids": len(shape.solids()),
        "valid": bool(shape.is_valid),
    }

answer = {}
for raw in sys.argv[1:]:
    shape = import_step(raw)
    children = [facts(child) for child in shape.children]
    payload = json.dumps(children, sort_keys=True, separators=(",", ":"))
    answer[raw] = {
        "children": children,
        "digest": hashlib.sha256(payload.encode()).hexdigest(),
    }
print("R2_STEP_FACTS=" + json.dumps(answer, separators=(",", ":")))
'''
    result = subprocess.run(
        [sys.executable, "-c", program, *(str(path) for path in paths)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=360,
    )
    line = next(line for line in result.stdout.splitlines() if line.startswith("R2_STEP_FACTS="))
    return json.loads(line.split("=", 1)[1])


def test_real_1040_sample_fin_sweeps_never_intersect_front_stationary_ring():
    assembly = g.make_r2_assembly()
    front = _children_by_prefix(assembly, "r2_front_stationary_quadrant_")
    rings = _children_by_prefix(assembly, "r2_moving_carrier_quadrant_")
    assert (len(front), len(rings)) == (4, 12)
    front_ring = front[0].fuse(*front[1:])

    sampled = 0
    violations = []
    for role in range(3):
        # Crop the source body above this carrier's top face and inside the
        # role-specific fin radius.  The resulting solid is the actual fused
        # fin, not a test-local redraw; the annular carrier itself is excluded
        # by the axial crop even for the innermost second-hand fin.
        carrier_top = p.carrier_layers[role][1]
        r0, r1 = p.fin_blade_radial_ranges[role]
        fin_shell = Cylinder(r1 + 0.10, 40.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
            Cylinder(r0 - 0.10, 40.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((0, 0, -0.2))
            )
        ).moved(Location((0, 0, carrier_top + 1e-4)))
        candidates = []
        for ring in rings[role * 4:(role + 1) * 4]:
            intersection = ring.intersect(fin_shell)
            if intersection is not None:
                candidates.extend(intersection.solids())
        fin = max(candidates, key=_volume)
        assert _volume(fin) > 0.0, f"role {role} has no source-derived fin"
        for sample in range(1040):
            sampled += 1
            moved = fin.rotate(Axis.Z, sample * 360.0 / 1040.0)
            volume = _intersection_volume(moved, front_ring)
            if volume > 1e-7:
                violations.append((role, sample, volume))
    assert sampled == 3 * 1040
    assert not violations, f"fin/front-ring BREP collisions: {violations[:8]}"


def test_actual_ring_and_pinion_are_tooth_geometry_and_share_the_frozen_mesh_axis():
    assembly = g.make_r2_assembly()
    rings = _children_by_prefix(assembly, "r2_moving_carrier_quadrant_")
    pinions = _children_by_prefix(assembly, "r2_output_pinion_")
    assert (len(rings), len(pinions)) == (12, 3)
    assert all(len(ring.faces()) > 100 for ring in rings), "ring quadrants must retain real 260T geometry"

    for role, pinion in enumerate(pinions):
        # A three-face cylinder can claim the right OD, but is not a 16T gear.
        assert len(pinion.faces()) > 34, f"role {role} output pinion is not toothed"
        assert len(pinion.edges()) > 50
        centre = pinion.bounding_box().center()
        assert hypot(centre.X, centre.Y) == pytest.approx(122.00, abs=0.02)
        host_ring = Compound(children=rings[role * 4:(role + 1) * 4])
        assert _intersection_volume(pinion, host_ring) <= 1e-7


def test_motor_to_pinion_alignment_and_ring_to_spine_clearance_use_actual_solids():
    make_station = _require_shape_api("make_motor_station_at_pose")
    assembly = g.make_r2_assembly()
    rings = _children_by_prefix(assembly, "r2_moving_carrier_quadrant_")
    spine = _children_by_prefix(assembly, "r2_tower_300_structural_spine_")
    assert len(spine) == 1
    assert sum(_intersection_volume(spine[0], ring) for ring in rings) <= 1e-7

    for role in range(3):
        station = make_station(role=role, motor_q_mm=0.0, ring_angle_deg=0.0)
        assert set(station) >= {"motor_shaft", "miter_input", "miter_output", "output_shaft", "pinion"}
        for name, shape in station.items():
            assert hasattr(shape, "solids") and _volume(shape) > 0.0, name
        motor_axis = station["motor_shaft"].bounding_box().center()
        input_axis = station["miter_input"].bounding_box().center()
        output_axis = station["output_shaft"].bounding_box().center()
        pinion_axis = station["pinion"].bounding_box().center()
        # The real 7 mm motor shaft approaches from the motor side; its centre
        # is not the input-gear centre.  Require the gear centre to lie on the
        # shaft axis instead of requiring two physically wrong coincident
        # bounding-box centres.
        angle = radians(p.motor_station_angles_deg[role])
        tangent = (-sin(angle), cos(angle))
        tangential_offset = abs(
            (input_axis.X - motor_axis.X) * tangent[0]
            + (input_axis.Y - motor_axis.Y) * tangent[1]
        )
        assert tangential_offset <= 0.02
        assert abs(input_axis.Z - motor_axis.Z) <= 0.02
        assert hypot(output_axis.X - pinion_axis.X, output_axis.Y - pinion_axis.Y) <= 0.02


def test_all_seam_plates_have_unique_source_occurrences_and_transforms():
    registry_fn = _require_shape_api("production_occurrence_registry")
    registry = registry_fn("assembled_nominal")
    seams = [record for record in registry if record["category"] == "moving_recessed_seam_plate"]
    assert len(seams) == 12
    assert len({record["occurrence_name"] for record in seams}) == 12
    assert len({tuple(record["transform"]) for record in seams}) == 12
    assert all(hasattr(record["shape"], "solids") and _volume(record["shape"]) > 0 for record in seams)
    assert len({
        sha256(json.dumps({
            "shape": _shape_facts(record["shape"]),
            "transform": tuple(record["transform"]),
        }, sort_keys=True).encode()).hexdigest()
        for record in seams
    }) == 12


def test_4096_shells_materially_change_solutions_and_obey_each_shell_equation():
    solve_one = _require_shape_api("solve_role_local_shell")
    make_shell_pose = _require_shape_api("make_tolerance_shell_pose")
    shells = list(g.iter_revision_k_tolerance_shells())
    assert len(shells) == 4096

    q_vectors = set()
    centre_vectors = set()
    axial_vectors = set()
    for shell in shells:
        result = solve_one("assembled_nominal", shell)
        q = result["role_local_q_mm"]
        centres = result["solved_ring_centres_xy_mm"]
        axial = result["ring_axial_positions_mm"]
        q_vectors.add(tuple(round(q[key], 8) for key in ROLE_KEYS))
        centre_vectors.add(tuple(round(value, 8) for key in ROLE_KEYS for value in centres[key]))
        axial_vectors.add(tuple(round(axial[key], 8) for key in ROLE_KEYS))
        for role in ROLE_KEYS:
            assert abs(q[role]) <= 0.76
            assert 1.00 - abs(q[role]) >= 0.24
            assert axial[role] == pytest.approx(result["nominal_axial_positions_mm"][role] + 0.75 * shell.axial_signs[role])
            expected_force = result["spring_rates_n_per_mm"][role] * (1.50 + q[role])
            assert result["role_force_n"][role] == pytest.approx(expected_force)
            for tower in (60, 180, 300):
                key = f"{role}{tower}"
                expected_residual = (
                    result["contact_distance_mm"][key]
                    + result["roller_running_radius_mm"]
                    - result["race_radius_mm"][key]
                )
                assert result["contact_residuals_mm"][key] == pytest.approx(expected_residual)
                assert abs(expected_residual) <= 0.05
        assert 0.555 <= sum(result["role_force_n"].values()) <= 2.034
        assert min(result["flange_overlaps_mm"].values()) >= 1.05

    assert len(q_vectors) > 1
    assert len(centre_vectors) > 1
    assert len(axial_vectors) == 8

    for shell in (shells[0], shells[-1], shells[2047], shells[2048]):
        pose = make_shell_pose("assembled_nominal", shell)
        assert hasattr(pose, "children") and all(child.is_valid for child in pose.children)
    first = make_shell_pose("assembled_nominal", shells[0])
    last = make_shell_pose("assembled_nominal", shells[-1])
    assert _facts_digest(first) != _facts_digest(last)


def test_axle_pin_insert_spring_stop_and_tool_paths_are_real_solids():
    fixed_fn = _require_shape_api("make_fixed_axle_stack_solids")
    pin_fn = _require_shape_api("make_cassette_pin_stack_solids")
    adjuster_fn = _require_shape_api("make_adjuster_stack_and_tool_solids")
    stop_fn = _require_shape_api("make_stop_window_solids")

    fixed = fixed_fn(station_angle_deg=60, shim_index=0)
    assert set(fixed) >= {"axle", "blind_seat_void", "upper_bore_void", "washer", "collar", "service_tool"}
    assert all(hasattr(shape, "solids") and _volume(shape) > 0.0 for shape in fixed.values())
    axle_box = fixed["axle"].bounding_box()
    assert axle_box.size.Z == pytest.approx(30.00, abs=0.02)
    assert max(axle_box.size.X, axle_box.size.Y) == pytest.approx(3.99, abs=0.02)
    assert _intersection_volume(fixed["service_tool"], fixed["collar"]) > 0.0

    for role in ROLES:
        pin = pin_fn(role)
        assert set(pin) >= {"pin", "blind_bore_void", "roller", "lower_washer", "upper_washer", "retainer_washer", "m2_screw", "pin_flat", "service_tool"}
        assert all(hasattr(shape, "solids") and _volume(shape) > 0.0 for shape in pin.values())
        assert pin["pin"].bounding_box().size.Z == pytest.approx(7.70, abs=0.02)
        assert _intersection_volume(pin["service_tool"], pin["m2_screw"]) > 0.0

        adjuster = adjuster_fn(role=role, position_mm=1.0)
        assert set(adjuster) >= {"insert", "screw", "washer", "spring", "guide", "boss", "adjustment_tool", "heat_tool"}
        assert all(hasattr(shape, "solids") and _volume(shape) > 0.0 for shape in adjuster.values())
        assert _intersection_volume(adjuster["spring"], adjuster["washer"]) > 0.0
        assert _intersection_volume(adjuster["adjustment_tool"], adjuster["screw"]) > 0.0
        assert _intersection_volume(adjuster["heat_tool"], adjuster["insert"]) > 0.0

        stop = stop_fn(role=role, cassette_q_mm=1.0, operating_mode="powered")
        assert set(stop) >= {"plate", "window_void", "stop_pin", "guide_capsules", "driver_tools"}
        assert all(hasattr(shape, "solids") and _volume(shape) > 0.0 for shape in stop.values())
        assert _intersection_volume(stop["stop_pin"], stop["window_void"]) > 0.0


def test_written_powered_and_service_state_brep_digests_move_the_correct_occurrences():
    state_paths = {
        "assembled_nominal": MODEL_ROOT / "p3_v3_r2_assembled.step",
        "powered_min": MODEL_ROOT / "p3_v3_r2_powered_min.step",
        "powered_max": MODEL_ROOT / "p3_v3_r2_powered_max.step",
        "service_exploded": MODEL_ROOT / "p3_v3_r2_service_exploded.step",
        "service_min_UNSAFE_TO_POWER": MODEL_ROOT / "p3_v3_r2_service_min_UNSAFE_TO_POWER.step",
        "service_max_UNSAFE_TO_POWER": MODEL_ROOT / "p3_v3_r2_service_max_UNSAFE_TO_POWER.step",
    }
    paths = tuple(state_paths.values())
    assert all(path.is_file() for path in paths)
    facts = _step_occurrence_facts(paths)
    by_name = {Path(path).name: value for path, value in facts.items()}
    digests = {name: value["digest"] for name, value in by_name.items()}
    assert len(set(digests.values())) == len(digests), digests

    assert all(child["valid"] for value in by_name.values() for child in value["children"])

    for state, path in state_paths.items():
        written_labels = {child["label"] for child in by_name[path.name]["children"]}
        printable_labels = {
            record["occurrence_name"]
            for record in g.production_occurrence_registry(state)
        }
        if state.startswith("service_"):
            assert written_labels == printable_labels
            assert len(written_labels) == 91
            assert not any("powered_window_key" in label or "locator" in label for label in written_labels)
        else:
            complete_labels = {
                record["occurrence_name"]
                for record in g.complete_occurrence_registry(state)
            }
            assert written_labels == complete_labels
            assert printable_labels <= written_labels
            assert len(written_labels) == 127
            assert len([label for label in written_labels if "powered_window_key" in label]) == 3

    powered_min = {child["label"]: child for child in by_name["p3_v3_r2_powered_min.step"]["children"]}
    powered_max = {child["label"]: child for child in by_name["p3_v3_r2_powered_max.step"]["children"]}
    changed = {label for label in powered_min if powered_min[label] != powered_max[label]}
    assert changed
    assert all(any(token in label for token in (
        "motor_yoke", "output_pinion", "miter_gear", "motor_shaft",
        "output_shaft", "bearing", "retainer", "motor_mount_fastener",
    )) for label in changed)
    powered_keys = {label for label in powered_min if "powered_window_key" in label}
    assert len(powered_keys) == 3
    assert all(powered_min[label] == powered_max[label] for label in powered_keys)


def test_production_3mf_objects_are_closed_manifolds_with_required_metadata():
    objects, items = _read_3mf(PRODUCTION_3MF)
    assert len(objects) == len(items) == 94
    assert len({obj["name"] for obj in objects.values()}) == 94
    for obj in objects.values():
        assert obj["vertices"] and obj["triangles"], obj["name"]
        edges = Counter()
        for a, b, c in obj["triangles"]:
            assert len({a, b, c}) == 3, f"degenerate triangle in {obj['name']}"
            edges[tuple(sorted((a, b)))] += 1
            edges[tuple(sorted((b, c)))] += 1
            edges[tuple(sorted((c, a)))] += 1
        assert set(edges.values()) == {2}, f"open/nonmanifold mesh {obj['name']}"
        assert {
            "kage:category", "kage:material", "kage:print-orientation",
            "kage:plate-index", "kage:source-brep-digest",
        } <= set(obj["metadata"]), obj["name"]


def test_production_3mf_is_disassembled_and_packed_within_u1_plate_limits():
    objects, items = _read_3mf(PRODUCTION_3MF)
    plate_points = defaultdict(list)
    for item in items:
        obj = objects[item["objectid"]]
        plate = int(obj["metadata"]["kage:plate-index"])
        transformed = [_transform_point(point, item.get("transform")) for point in obj["vertices"]]
        plate_points[plate].extend(transformed)
    assert plate_points
    assert len(plate_points) >= 2, "a 300 mm assembled clock cannot be one U1 print plate"
    for plate, points in plate_points.items():
        xs, ys, zs = zip(*points)
        assert max(xs) - min(xs) <= 260.00, plate
        assert max(ys) - min(ys) <= 260.00, plate
        assert min(xs) >= 5.00 and min(ys) >= 5.00, plate
        assert max(xs) <= 255.00 and max(ys) <= 255.00, plate
        assert min(zs) >= -1e-6


def test_manifest_has_transitive_hashes_and_direct_source_occurrence_facts():
    manifest = json.loads(MANIFEST.read_text())
    hashes = manifest["transitiveSourceHashes"]
    required_sources = {
        "p3_v3_direct_gear_race_guidance_r2_spec.py",
        "p3_v3_direct_gear_race_guidance_r2_geometry.py",
        "p3_v3_direct_gear_race_guidance_r2_export.py",
    }
    assert required_sources <= set(hashes)
    records = manifest["productionOccurrences"]
    assert len(records) == 94
    required = {
        "name", "category", "transform", "valid", "bounds", "volume",
        "faceCount", "brepDigest", "factsDigest", "sourcePath",
    }
    assert all(required <= set(record) for record in records)
    assert len({record["name"] for record in records}) == 94
    assert len({(record["name"], tuple(record["transform"])) for record in records}) == 94

    complete_registry = list(g.complete_occurrence_registry("assembled_nominal"))
    printable_registry = [record for record in complete_registry if record["printable"] is True]
    reference_registry = [record for record in complete_registry if record["printable"] is False]
    assert len(complete_registry) == 127
    assert len(printable_registry) == 94
    assert len(reference_registry) == 33
    assert all(record["printable"] is True for record in printable_registry)
    assert all(record["printable"] is False for record in reference_registry)

    reference_inventory = Counter(record["category"] for record in reference_registry)
    assert reference_inventory == {
        "motor_shaft_reference": 3,
        "output_shaft_reference": 3,
        "shaft_bearing_reference": 6,
        "shaft_retainer_reference": 6,
        "miter_axial_retainer_reference": 3,
        "motor_mount_fastener_reference": 12,
    }
    assert len({record["occurrence_name"] for record in complete_registry}) == 127
    assert all(
        len(record["transform"]) == 12
        and hasattr(record["shape"], "solids")
        and _volume(record["shape"]) > 0.0
        for record in complete_registry
    )

    source = {record["occurrence_name"]: record["shape"] for record in printable_registry}
    assert set(source) == {record["name"] for record in records}
    for record in records:
        facts = _shape_facts(source[record["name"]])
        assert record["valid"] == facts["valid"]
        assert tuple(record["bounds"]) == pytest.approx(facts["bounds"], abs=0.02)
        assert record["volume"] == pytest.approx(facts["volume"], rel=1e-5)
        assert record["faceCount"] == facts["faces"]
        # ``brepDigest`` is reserved for the raw canonical export_brep hash.
        # The compact bounds/volume/topology fingerprint remains independently
        # useful, but must live under a field whose name does not misrepresent
        # it as canonical BREP evidence.
        assert record["factsDigest"] == _facts_digest(source[record["name"]])

    # Source freshness is checked after schema/digest semantics so a stale
    # export cannot conceal a missing canonical-evidence field.
    for relative, expected in hashes.items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_coupon_solids_are_canonical_crops_of_production_occurrences():
    registry_fn = _require_shape_api("production_occurrence_registry")
    crop_fn = _require_shape_api("canonical_crop")
    tool_fn = _require_shape_api("complete_station_coupon_crop_tool")
    source_records = registry_fn("assembled_nominal")
    source = {record["occurrence_name"]: record["shape"] for record in source_records}
    crop_tool = tool_fn()
    expected = {
        name: crop_fn(shape, crop_tool)
        for name, shape in source.items()
        if _intersection_volume(shape, crop_tool) > 1e-7
    }
    actual = {
        child.label: child
        for child in g.make_complete_station_coupon().children
        if not child.label.startswith("coupon_only_stop_")
    }
    assert set(actual) == set(expected)
    for name in expected:
        assert _shape_facts(actual[name]) == _shape_facts(expected[name])

    coupon_manifest = json.loads((MODEL_ROOT / "coupons" / "manifest.json").read_text())
    assert coupon_manifest["canonicalCropToolDigest"] == _facts_digest(crop_tool)
    assert coupon_manifest["sourceOccurrenceDigests"] == {
        name: _facts_digest(shape) for name, shape in expected.items()
    }
