"""Written STEP validity and source/export parity for the direct race trial."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance"
SOURCE_FILES = (
    ROOT / "p3_v3_direct_gear_race_guidance_spec.py",
    ROOT / "p3_v3_direct_gear_race_guidance_geometry.py",
    ROOT / "p3_v3_direct_gear_race_guidance_export.py",
)
EXPECTED_OCCURRENCES = 201


def _facts_in_fresh_process(value: str) -> dict:
    """Import one 41 MB STEP in an isolated OCC process."""

    script = r'''
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
value = sys.argv[2]
sys.path.insert(0, str(root))

from build123d import import_step
shape = import_step(root / "models" / "p3_v3_direct_gear_race_guidance" / value)

def bounds(item):
    box = item.bounding_box()
    return [box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z]

labels = [child.label for child in shape.children]
facts = {
    "valid": bool(shape.is_valid),
    "labels": labels,
    "label_hash": __import__("hashlib").sha256(json.dumps(labels, separators=(",", ":")).encode()).hexdigest(),
    "child_count": len(shape.children),
    "solid_count": len(shape.solids()),
    "bounds": bounds(shape),
    "children": [
        {"valid": bool(child.is_valid), "volume": float(child.volume), "bounds": bounds(child)}
        for child in shape.children
    ],
}
print("P3_DIRECT_RACE_FACTS=" + json.dumps(facts, separators=(",", ":")))
'''
    completed = subprocess.run(
        [sys.executable, "-c", script, str(ROOT), value],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    line = next(
        line for line in completed.stdout.splitlines()
        if line.startswith("P3_DIRECT_RACE_FACTS=")
    )
    return json.loads(line.split("=", 1)[1])


def _source_facts_in_fresh_process(factory_name: str) -> dict:
    """Build one source state in isolation for label/placement parity."""

    script = r'''
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
factory_name = sys.argv[2]
sys.path.insert(0, str(root))

from p3_v3_direct_gear_race_guidance_geometry import (
    make_assembled,
    make_powered_min,
    make_powered_max,
    make_service_exploded,
)
factory = {
    "nominal": make_assembled,
    "powered_min": make_powered_min,
    "powered_max": make_powered_max,
    "exploded": make_service_exploded,
}[factory_name]
shape = factory()

def bounds(item):
    box = item.bounding_box()
    return [box.min.X, box.min.Y, box.min.Z, box.max.X, box.max.Y, box.max.Z]

# STEP occurrence names sanitize decimal dots to underscores.  Normalize only
# that serialization detail on the source side; every other character and the
# exact ordering stay under parity control.
labels = [child.label.replace(".", "_") for child in shape.children]
facts = {
    "valid": bool(shape.is_valid),
    "labels": labels,
    "label_hash": __import__("hashlib").sha256(json.dumps(labels, separators=(",", ":")).encode()).hexdigest(),
    "child_count": len(shape.children),
    "solid_count": len(shape.solids()),
    "bounds": bounds(shape),
    "children": [
        {"valid": bool(child.is_valid), "volume": float(child.volume), "bounds": bounds(child)}
        for child in shape.children
    ],
}
print("P3_DIRECT_RACE_SOURCE_FACTS=" + json.dumps(facts, separators=(",", ":")))
'''
    completed = subprocess.run(
        [sys.executable, "-c", script, str(ROOT), factory_name],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    line = next(
        line for line in completed.stdout.splitlines()
        if line.startswith("P3_DIRECT_RACE_SOURCE_FACTS=")
    )
    return json.loads(line.split("=", 1)[1])


def _expected_source_labels(exploded: bool) -> list[str]:
    """Legacy label-order helper retained for readable manifest construction.

    The authoritative 201-occurrence gate below compares a fresh source build
    with the written STEP, including the 36 new clamp-hardware occurrences.
    """

    labels = [
        *(f"p3_v3_direct_race_rear_chassis_Q{q}_two_fixed_one_adjustable_tower" for q in range(1, 5)),
        *(f"p3_v3_r2_stationary_frame_quadrant_Q{q}" for q in range(1, 5)),
        *(f"p3_v3_r2_stationary_outer_front_ring_post_{n}" for n in range(1, 7)),
        *(f"p3_v3_r2_stationary_outer_front_ring_quadrant_Q{q}" for q in range(1, 5)),
    ]
    roles = ("hour", "minute", "second")
    for tower in range(1, 4):
        mount = "fixed_round_mounts" if tower < 3 else "adjustable_plus_minus_0p25"
        labels.append(f"p3_v3_direct_race_inner_tower_{tower}_{mount}_connected_two_sided_yoke")
        labels.extend(f"p3_v3_direct_race_tower_{tower}_D6x1p25_spacer_{n}" for n in (1, 2))
        labels.extend((
            f"p3_v3_direct_race_tower_{tower}_lower_0p20_thrust_washer",
            f"p3_v3_direct_race_tower_{tower}_upper_0p20_thrust_washer",
        ))
        labels.extend(
            f"p3_v3_direct_race_tower_{tower}_{role}_RELIEVED_spool_carrier_root_land_only"
            for role in roles
        )
        labels.extend((
            f"p3_v3_direct_race_tower_{tower}_D4x25_polished_axle_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_purchased_D4x10x4_metal_M2_set_screw_collar_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M2_collar_set_screw_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M3_mount_screw_1_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M3_washer_1_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M3_hex_nut_1_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M3_mount_screw_2_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M3_washer_2_REFERENCE",
            f"p3_v3_direct_race_tower_{tower}_M3_hex_nut_2_REFERENCE",
        ))

    yoke_suffix = "ONE_CONNECTED_open_yoke_integral_motor_face_chassis_foot_two_MR84_seats"
    motor_suffixes = (
        "NEMA8_REFERENCE",
        "NEMA8_D4x7_shaft_REFERENCE",
        "horizontal_16T_miter",
        "vertical_16T_miter",
        "D4x40_output_shaft_REFERENCE",
        "lower_MR84ZZ_REFERENCE",
        "upper_MR84ZZ_REFERENCE",
        "ONLY_role_height_spacer",
        "16T_output_pinion",
        "lower_datum_split_collar_REFERENCE",
        "upper_safety_split_collar_REFERENCE",
        yoke_suffix,
    )
    if not exploded:
        labels.extend(f"p3_v3_direct_race_{role}_{yoke_suffix}" for role in roles)
    for role in roles:
        labels.extend(
            f"p3_v3_direct_race_{role}_M1_260T_quadrant_Q{q}_65T_BARE_carrier_race"
            for q in range(1, 5)
        )
        for seam in range(1, 5):
            labels.extend((
                f"p3_v3_r2_{role}_seam_{seam}_underside_splice",
                f"p3_v3_r2_{role}_seam_{seam}_3mm_registration_dowel",
                f"p3_v3_r2_{role}_seam_{seam}_M2_screw_1_REFERENCE",
                f"p3_v3_r2_{role}_seam_{seam}_M2_screw_2_REFERENCE",
            ))
        suffixes = motor_suffixes if exploded else motor_suffixes[:-1]
        labels.extend(f"p3_v3_direct_race_{role}_{suffix}" for suffix in suffixes)
    return labels


def _assembled_step_pair_matrix_in_fresh_process(filename: str) -> dict:
    """Re-import the written STEP and collision-check labeled occurrences."""

    script = r'''
import json
import sys
from pathlib import Path
from build123d import import_step

root = Path(sys.argv[1])
filename = sys.argv[2]
shape = import_step(root / "models" / "p3_v3_direct_gear_race_guidance" / filename)
children = list(shape.children)
roles = ("hour", "minute", "second")
ring_parts = [child for child in children if "_M1_260T_quadrant_" in child.label]
motor_suffixes = (
    "NEMA8_REFERENCE", "NEMA8_D4x7_shaft_REFERENCE", "horizontal_16T_miter",
    "vertical_16T_miter", "D4x40_output_shaft_REFERENCE", "lower_MR84ZZ_REFERENCE",
    "upper_MR84ZZ_REFERENCE", "ONLY_role_height_spacer", "16T_output_pinion",
    "lower_datum_split_collar_REFERENCE", "upper_safety_split_collar_REFERENCE",
    "ONE_CONNECTED_open_yoke_integral_motor_face_chassis_foot_two_MR84_seats",
)

def role_of(label):
    for role in roles:
        if f"_{role}_" in label:
            return role
    raise AssertionError(label)

def separated(a, b, eps=1e-8):
    aa, bb = a.bounding_box(), b.bounding_box()
    return (aa.max.X < bb.min.X - eps or bb.max.X < aa.min.X - eps or
            aa.max.Y < bb.min.Y - eps or bb.max.Y < aa.min.Y - eps or
            aa.max.Z < bb.min.Z - eps or bb.max.Z < aa.min.Z - eps)

motor_parts = [
    child for child in children
    if any(suffix in child.label for suffix in motor_suffixes)
]
assert len(ring_parts) == 12, [c.label for c in ring_parts]
assert len(motor_parts) == 36, [c.label for c in motor_parts]

checked = 0
candidate_pairs = 0
worst_volume = 0.0
worst_pair = None
for part in motor_parts:
    part_role = role_of(part.label)
    for ring in ring_parts:
        ring_role = role_of(ring.label)
        if "16T_output_pinion" in part.label and part_role == ring_role:
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

collars = [
    child for child in motor_parts
    if "upper_safety_split_collar_REFERENCE" in child.label
]
collar_clearances = {}
for collar in collars:
    station_role = role_of(collar.label)
    collar_clearances[station_role] = {
        ring_role: min(collar.distance_to(ring) for ring in ring_parts if role_of(ring.label) == ring_role)
        for ring_role in roles
    }

print("P3_IMPORTED_PAIR_MATRIX=" + json.dumps({
    "checked": checked,
    "candidate_pairs": candidate_pairs,
    "worst_volume": worst_volume,
    "worst_pair": worst_pair,
    "collar_clearances": collar_clearances,
}, separators=(",", ":")))
'''
    completed = subprocess.run(
        [sys.executable, "-c", script, str(ROOT), filename],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    line = next(
        line for line in completed.stdout.splitlines()
        if line.startswith("P3_IMPORTED_PAIR_MATRIX=")
    )
    return json.loads(line.split("=", 1)[1])


@pytest.mark.parametrize(
    "filename",
    (
        "p3_v3_direct_gear_race_powered_min_q-0p35.step",
        "p3_v3_direct_gear_race_assembled.step",
        "p3_v3_direct_gear_race_powered_max_q+0p10.step",
    ),
)
def test_imported_assembled_step_label_keyed_motor_ring_pair_matrix(filename):
    result = _assembled_step_pair_matrix_in_fresh_process(filename)
    assert result["checked"] == 420
    assert result["candidate_pairs"] > 0
    assert result["worst_volume"] <= 1e-7, result["worst_pair"]
    assert set(result["collar_clearances"]) == {"hour", "minute", "second"}
    for station_clearances in result["collar_clearances"].values():
        assert set(station_clearances) == {"hour", "minute", "second"}
        assert min(station_clearances.values()) >= 2.89


@pytest.mark.parametrize(
    "filename,factory_name",
    (
        ("p3_v3_direct_gear_race_assembled.step", "nominal"),
        ("p3_v3_direct_gear_race_powered_min_q-0p35.step", "powered_min"),
        ("p3_v3_direct_gear_race_powered_max_q+0p10.step", "powered_max"),
        ("p3_v3_direct_gear_race_service_exploded.step", "exploded"),
    ),
)
def test_written_step_is_fresh_valid_and_has_exact_source_occurrence_parity(filename, factory_name):
    path = MODEL_ROOT / filename
    newest_source = max(source.stat().st_mtime for source in SOURCE_FILES)
    assert path.is_file() and path.stat().st_mtime >= newest_source
    source = _source_facts_in_fresh_process(factory_name)
    written = _facts_in_fresh_process(filename)
    assert source["valid"] and written["valid"]
    assert source["child_count"] == source["solid_count"] == EXPECTED_OCCURRENCES
    assert written["child_count"] == written["solid_count"] == EXPECTED_OCCURRENCES
    assert written["labels"] == source["labels"]
    assert written["label_hash"] == source["label_hash"]
    assert written["bounds"] == pytest.approx(source["bounds"], abs=0.002)
    assert len(source["children"]) == len(written["children"]) == EXPECTED_OCCURRENCES
    for source_child, written_child in zip(source["children"], written["children"]):
        assert source_child["valid"] and source_child["volume"] > 0.0
        assert written_child["valid"] and written_child["volume"] > 0.0
        # Bounds encode occurrence placement as well as extents.  This catches
        # stale q states even when their label manifest is otherwise identical.
        assert written_child["bounds"] == pytest.approx(source_child["bounds"], abs=0.002)
        assert written_child["volume"] == pytest.approx(source_child["volume"], rel=2e-5, abs=2e-5)
