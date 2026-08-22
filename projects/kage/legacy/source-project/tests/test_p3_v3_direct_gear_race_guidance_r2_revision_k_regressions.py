"""Second independent RED gate for the frozen Revision-K handoff.

These checks deliberately inspect production solids and written deliverables.
They do not accept report booleans, decorative witness geometry, or ZIP metadata
that merely says a slicer/clearance operation happened.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json
from math import hypot
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from build123d import (
    Align,
    Axis,
    Box,
    Compound,
    Cylinder,
    Location,
    export_brep,
    import_step,
)
import pytest

import p3_v3_direct_gear_race_guidance_r2_geometry as g
from p3_v3_direct_gear_race_guidance_r2_spec import P3_V3_DIRECT_GEAR_RACE_R2 as p


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_r2"
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
ROLES = ("hour", "minute", "second")
STATES = (
    "assembled_nominal",
    "service_exploded",
    "powered_min",
    "powered_max",
    "service_min_UNSAFE_TO_POWER",
    "service_max_UNSAFE_TO_POWER",
)


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


def _real_brep_digest(shape) -> str:
    with NamedTemporaryFile(suffix=".brep") as tmp:
        export_brep(shape, tmp.name)
        return sha256(Path(tmp.name).read_bytes()).hexdigest()


def _summary_facts_digest(shape) -> str:
    box = shape.bounding_box()
    facts = {
        "valid": bool(shape.is_valid),
        "bounds": tuple(round(value, 6) for value in (
            box.min.X, box.min.Y, box.min.Z,
            box.max.X, box.max.Y, box.max.Z,
        )),
        "volume": round(_volume(shape), 6),
        "faces": len(shape.faces()),
        "edges": len(shape.edges()),
        "solids": len(shape.solids()),
    }
    payload = json.dumps(facts, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode()).hexdigest()


def _source_registry(state="assembled_nominal"):
    return g.production_occurrence_registry(state)


def _records(category: str, state="assembled_nominal"):
    return [r for r in _source_registry(state) if r["category"] == category]


def _step_paths():
    return {
        "assembled_nominal": MODEL_ROOT / "p3_v3_r2_assembled.step",
        "service_exploded": MODEL_ROOT / "p3_v3_r2_service_exploded.step",
        "powered_min": MODEL_ROOT / "p3_v3_r2_powered_min.step",
        "powered_max": MODEL_ROOT / "p3_v3_r2_powered_max.step",
        "service_min_UNSAFE_TO_POWER": MODEL_ROOT / "p3_v3_r2_service_min_UNSAFE_TO_POWER.step",
        "service_max_UNSAFE_TO_POWER": MODEL_ROOT / "p3_v3_r2_service_max_UNSAFE_TO_POWER.step",
    }


def _read_3mf(path: Path):
    with ZipFile(path) as package:
        names = set(package.namelist())
        root = ET.fromstring(package.read("3D/3dmodel.model"))
    objects = {}
    for obj in root.findall(".//m:resources/m:object", NS):
        meta = {m.attrib.get("name"): (m.text or "") for m in obj.findall("m:metadata", NS)}
        verts = [
            (float(v.attrib["x"]), float(v.attrib["y"]), float(v.attrib["z"]))
            for v in obj.findall(".//m:vertices/m:vertex", NS)
        ]
        objects[obj.attrib["id"]] = {"name": obj.attrib.get("name", ""), "meta": meta, "vertices": verts}
    items = [dict(node.attrib) for node in root.findall(".//m:build/m:item", NS)]
    return names, objects, items


def test_revision_k_authoritative_station_and_fin_contract_was_not_rewritten():
    """K1/K2 preserve Revision-H fins and the accepted alternating stations."""

    assert p.motor_station_angles_deg == pytest.approx((0.0, 120.0, 240.0))
    assert p.fixed_tower_angles_deg == pytest.approx((60.0, 180.0))
    assert p.local_cassette_angle_deg == pytest.approx(300.0)
    authoritative_fin_ranges = (
        (142.50, 143.70),
        (139.30, 140.50),
        (136.10, 137.30),
    )
    assert len(p.fin_blade_radial_ranges) == len(authoritative_fin_ranges)
    for actual, expected in zip(p.fin_blade_radial_ranges, authoritative_fin_ranges):
        assert actual == pytest.approx(expected)
    assert p.fin_blade_start_zs == pytest.approx((2.00, 8.70, 15.40))


def test_every_lower_fin_clears_the_real_rear_ring_for_three_by_1040_positions():
    rear = Compound(children=[r["shape"] for r in _records("rear_stationary_quadrant")])
    moving = _records("moving_carrier_quadrant")
    violations = []
    sampled = 0
    for role in range(3):
        z0 = p.carrier_layers[role][0]
        r0, r1 = p.fin_blade_radial_ranges[role]
        crop = Cylinder(r1 + 0.15, 40, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
            Cylinder(r0 - 0.15, 40.4, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, -0.2)))
        ).moved(Location((0, 0, z0 + 1e-4)))
        pieces = []
        for row in moving[role * 4:(role + 1) * 4]:
            result = row["shape"].intersect(crop)
            if result is not None:
                pieces.extend(result.solids())
        assert pieces, f"role {role} has no source-derived lower-fin solid"
        fin = max(pieces, key=_volume)
        for index in range(1040):
            sampled += 1
            overlap = _iv(fin.rotate(Axis.Z, index * 360.0 / 1040.0), rear)
            if overlap > 1e-7:
                violations.append((role, index, overlap))
    assert sampled == 3120
    assert not violations, f"lower fin/rear ring collisions: {violations[:12]}"


def test_all_written_states_have_zero_unapproved_positive_volume_collision_pairs():
    """Run a complete broad-phase/exact BREP collision scan in isolated OCC."""

    paths = _step_paths()
    assert all(path.is_file() for path in paths.values())
    program = r'''
import json, sys
from build123d import import_step

def vol(s): return sum(x.volume for x in s.solids()) if s else 0.0
answer = {}
for raw in sys.argv[1:]:
    root = import_step(raw)
    children = list(root.children)
    failures = []
    checked = 0
    for i, a in enumerate(children):
        aa = a.bounding_box()
        for b in children[i+1:]:
            bb = b.bounding_box()
            if aa.max.X < bb.min.X or bb.max.X < aa.min.X or aa.max.Y < bb.min.Y or bb.max.Y < aa.min.Y or aa.max.Z < bb.min.Z or bb.max.Z < aa.min.Z:
                continue
            checked += 1
            v = vol(a.intersect(b))
            if v > 1e-7:
                failures.append([a.label, b.label, round(v, 7)])
    answer[raw] = {"checked": checked, "failures": failures}
print("REV_K_COLLISIONS=" + json.dumps(answer, separators=(",", ":")))
'''
    result = subprocess.run(
        [sys.executable, "-c", program, *(str(paths[s]) for s in STATES)],
        cwd=ROOT, capture_output=True, text=True, check=True, timeout=600,
    )
    line = next(x for x in result.stdout.splitlines() if x.startswith("REV_K_COLLISIONS="))
    facts = json.loads(line.split("=", 1)[1])
    assert all(v["checked"] > 0 for v in facts.values())
    failures = {Path(k).name: v["failures"] for k, v in facts.items() if v["failures"]}
    assert not failures, failures


def test_motor_station_has_true_90_degree_retained_transmission_and_clear_keepouts():
    registry = _source_registry()
    by_category = defaultdict(list)
    for row in registry:
        by_category[row["category"]].append(row["shape"])
    for role in range(3):
        station = g.make_motor_station_at_pose(role=role, motor_q_mm=0.0, ring_angle_deg=0.0)
        required = {"motor_shaft", "miter_input", "miter_output", "output_shaft", "pinion"}
        assert required <= set(station)
        motor_box, output_box = station["motor_shaft"].bounding_box(), station["output_shaft"].bounding_box()
        motor_axis = max(range(3), key=lambda i: (motor_box.size.X, motor_box.size.Y, motor_box.size.Z)[i])
        output_axis = max(range(3), key=lambda i: (output_box.size.X, output_box.size.Y, output_box.size.Z)[i])
        assert motor_axis != output_axis, "motor and output shafts must be orthogonal"
        # Real bevel/miter gears taper along their axes; rotated spur witnesses do not.
        for name in ("miter_input", "miter_output"):
            gear = station[name]
            box = gear.bounding_box()
            spans = sorted((box.size.X, box.size.Y, box.size.Z))
            assert spans[1] - spans[0] > 0.35, f"{name} is cylindrical spur witness, not bevel geometry"
        assert _iv(station["miter_input"], station["miter_output"]) <= 1e-7
        assert station["miter_input"].distance_to(station["miter_output"]) <= 0.20
        assert _iv(station["pinion"], by_category["motor_yoke"][role]) <= 1e-7
        assert _iv(station["miter_output"], by_category["tower_300_three_window_stop_plate"][0]) <= 1e-7
        assert _iv(station["pinion"], by_category["tower_300_role_slider_cassette"][role]) <= 1e-7


def test_tolerance_shell_poses_use_production_ring_quadrants_not_witness_annuli():
    shells = list(g.iter_revision_k_tolerance_shells())
    assert len(shells) == 4096
    production_labels = {
        row["occurrence_name"] for row in _source_registry()
        if row["category"] == "moving_carrier_quadrant"
    }
    for shell in (shells[0], shells[2047], shells[2048], shells[-1]):
        pose = g.make_tolerance_shell_pose("assembled_nominal", shell)
        labels = {child.label for child in pose.children}
        assert production_labels <= labels
        assert not any("shell_pose" in label for label in labels)
    # The production carrier itself must contain the frozen r=131.60 race.
    probe = Cylinder(131.65, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
        Cylinder(131.55, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0, 0, -0.2)))
    ).moved(Location((0, 0, p.carrier_layers[0][0] + 0.5)))
    host = Compound(children=[r["shape"] for r in _records("moving_carrier_quadrant")[:4]])
    assert _iv(probe, host) > 1e-7


def test_service_tools_hit_only_their_target_and_no_other_stack_material():
    fixed = g.make_fixed_axle_stack_solids(station_angle_deg=60, shim_index=0)
    assert _iv(fixed["service_tool"], fixed["collar"]) > 0
    assert all(_iv(fixed["service_tool"], fixed[name]) <= 1e-7 for name in ("axle", "washer"))
    for role in ROLES:
        pin = g.make_cassette_pin_stack_solids(role)
        assert _iv(pin["service_tool"], pin["m2_screw"]) > 0
        assert all(
            _iv(pin["service_tool"], pin[name]) <= 1e-7
            for name in ("pin", "roller", "lower_washer", "upper_washer", "retainer_washer")
        )
        adjuster = g.make_adjuster_stack_and_tool_solids(role=role, position_mm=1.0)
        assert _iv(adjuster["adjustment_tool"], adjuster["screw"]) > 0
        assert _iv(adjuster["heat_tool"], adjuster["insert"]) > 0
        assert all(
            _iv(adjuster["adjustment_tool"], adjuster[name]) <= 1e-7
            for name in ("insert", "washer", "spring", "guide", "boss")
        )
        assert all(
            _iv(adjuster["heat_tool"], adjuster[name]) <= 1e-7
            for name in ("screw", "washer", "spring", "guide", "boss")
        )


def test_revision_k_keys_caps_seats_and_seams_exist_in_production_solids():
    keys = _records("stationary_joint_registration_key")
    assert len(keys) == 16
    for row in keys:
        box = row["shape"].bounding_box()
        assert sorted((box.size.X, box.size.Y)) == pytest.approx((4.0, 6.0), abs=0.05)
        assert box.size.Z == pytest.approx(2.5, abs=0.05)
    hall = _records("hall_pocket_cap")
    balance = _records("balance_pocket_cap")
    assert len(hall) == 3 and len(balance) == 9
    for row in hall + balance:
        box = row["shape"].bounding_box()
        assert max(box.size.X, box.size.Y) == pytest.approx(4.08, abs=0.08)
        assert box.size.Z == pytest.approx(0.40, abs=0.05)
        centre = box.center()
        assert hypot(centre.X, centre.Y) == pytest.approx(136.0, abs=0.1)
    # Lower fixed leaves have real blind axle seats rather than solid slabs.
    for row, angle in zip(_records("fixed_tower_leaf"), (60.0, 180.0)):
        # A D4.05 gauge inside the expected local seat must see empty material.
        from math import cos, radians, sin
        gauge = Cylinder(2.0, 2.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((118.0 * cos(radians(angle)), 118.0 * sin(radians(angle)), -5.1))
        )
        assert _iv(gauge, row["shape"]) <= 1e-7
    # A canonical seam contains service holes and therefore is not a solid plate.
    for row in _records("moving_recessed_seam_plate"):
        assert len(row["shape"].solids()) >= 1
        assert len(row["shape"].faces()) >= 10


def test_state_semantics_keep_powered_keys_stationary_and_remove_them_for_service():
    def centers(state, category):
        return {
            r["occurrence_name"]: tuple(round(v, 5) for v in (
                r["shape"].bounding_box().center().X,
                r["shape"].bounding_box().center().Y,
                r["shape"].bounding_box().center().Z,
            ))
            for r in _source_registry(state) if r["category"] == category
        }
    assert centers("powered_min", "motor_powered_window_key") == centers("powered_max", "motor_powered_window_key")
    assert centers("powered_min", "motor_yoke") != centers("powered_max", "motor_yoke")
    assert not centers("service_min_UNSAFE_TO_POWER", "motor_powered_window_key")
    assert not centers("service_max_UNSAFE_TO_POWER", "motor_powered_window_key")
    paths = _step_paths()
    expected_tokens = {
        "assembled_nominal": "assembled",
        "service_exploded": "service_exploded",
        "powered_min": "powered_min",
        "powered_max": "powered_max",
        "service_min_UNSAFE_TO_POWER": "service_min_UNSAFE_TO_POWER",
        "service_max_UNSAFE_TO_POWER": "service_max_UNSAFE_TO_POWER",
    }
    assert all(token.lower() in paths[state].stem.lower() for state, token in expected_tokens.items())


def test_production_3mf_is_a_real_multiplate_slicer_project_with_orientations():
    path = MODEL_ROOT / "print" / "p3_v3_r2_production_94.3mf"
    names, objects, items = _read_3mf(path)
    assert any(name.startswith("Metadata/") and "model_settings" in name for name in names)
    assert any(name.startswith("Metadata/") and "plate" in name.lower() for name in names)
    assert len(items) == 94
    plates = defaultdict(list)
    for item in items:
        obj = objects[item["objectid"]]
        plates[int(obj["meta"]["kage:plate-index"])].append(obj)
        orientation = obj["meta"].get("kage:print-orientation", "")
        assert orientation not in ("", "source-z-up", "generic")
    assert len(plates) >= 2
    assert all(group for group in plates.values())


def test_coupon_and_ladders_encode_exact_source_flags_and_interface_families():
    coupon = MODEL_ROOT / "coupons" / "p3_v3_r2_complete_station_coupon.3mf"
    ladder = MODEL_ROOT / "coupons" / "p3_v3_r2_complete_station_fit_ladder.3mf"
    fixed = MODEL_ROOT / "coupons" / "p3_v3_r2_fixed_tower_fit_ladder.3mf"
    for path in (coupon, ladder, fixed):
        assert path.is_file()
    _, coupon_objects, coupon_items = _read_3mf(coupon)
    assert len(coupon_items) == 5
    references = [obj for obj in coupon_objects.values() if obj["meta"].get("kage:reference-only") == "true"]
    assert references
    assert not ({item["objectid"] for item in coupon_items} & {
        key for key, obj in coupon_objects.items() if obj in references
    })
    _, ladder_objects, ladder_items = _read_3mf(ladder)
    assert len(ladder_items) == 18
    assert len({obj["meta"].get("kage:interface-family") for obj in ladder_objects.values()}) == 6
    assert all(obj["meta"].get("kage:nominal-value-mm") for obj in ladder_objects.values())
    _, fixed_objects, fixed_items = _read_3mf(fixed)
    families = [obj["meta"].get("kage:interface-family") for obj in fixed_objects.values()]
    assert families.count("keyed-shim-pair") == 9
    assert families.count("paired-bore-cell") == 3
    assert len(fixed_items) >= 12


def test_manifest_uses_raw_canonical_brep_and_records_real_parity_and_slicer_facts():
    manifest = json.loads((MODEL_ROOT / "manifest.json").read_text())
    assert manifest["canonicalBrepDigestAlgorithm"] == "build123d-export-brep-sha256-v1"
    source = {r["occurrence_name"]: r["shape"] for r in _source_registry()}
    rows = manifest["productionOccurrences"]
    assert len(rows) == 94
    for row in rows:
        assert row["brepDigest"] == _real_brep_digest(source[row["name"]])
        assert row["factsDigest"] == _summary_facts_digest(source[row["name"]])
        assert {"plateIndex", "printOrientation", "slicerReload"} <= set(row)
    parity = manifest["stateParity"]
    expected_printed_counts = {
        "assembled_nominal": 94,
        "powered_min": 94,
        "powered_max": 94,
        "service_exploded": 91,
        "service_min_UNSAFE_TO_POWER": 91,
        "service_max_UNSAFE_TO_POWER": 91,
    }
    assert set(parity) == set(expected_printed_counts)
    step_paths = _step_paths()
    for state, expected_count in expected_printed_counts.items():
        value = parity[state]
        assert value["positiveVolumeCollisionCount"] == 0
        # ``occurrenceCount`` is the printable-state contract.  Purchased
        # shafts, bearings, retainers and fasteners may also be present in a
        # powered/assembled review STEP, but they must not inflate the frozen
        # 94-part production BOM.  Service states omit the three powered-only
        # keys and therefore contain 91 printable occurrences.
        assert value["occurrenceCount"] == expected_count

        source_printed = {
            row["occurrence_name"]
            for row in g.production_occurrence_registry(state)
            if row["printable"] is True
        }
        assert len(source_printed) == expected_count
        written_labels = {child.label for child in import_step(str(step_paths[state])).children}
        assert source_printed <= written_labels
        manifest_labels = {row["name"] for row in value["occurrences"]}
        assert source_printed <= manifest_labels
        assert not any("locator" in name.lower() for name in written_labels | manifest_labels)
        if state.startswith("service_"):
            # Service export is the physically extracted printable mechanism;
            # hardware references and substitute locator solids are absent.
            assert written_labels == source_printed == manifest_labels
    slicer = manifest["slicerValidation"]
    assert slicer["tool"] and slicer["version"] and slicer["reloadStatus"] == "passed"
