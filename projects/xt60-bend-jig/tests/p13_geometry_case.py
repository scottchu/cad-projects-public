"""Fresh-process OCC checks used by the P13 pytest contract.

Each invocation performs one bounded geometry case so OpenCascade allocations
are returned to the OS at process exit.  This is a validation harness, not a
second geometry implementation.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from build123d import Pos, export_step, import_step

import xt60_bend_jig.p13_four_plate_three_rod as p13


def volume(common) -> float:
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return float(common.volume)
    return sum(float(item.volume) for item in common)


def overlap(a, b) -> float:
    return volume(a.intersect(b))


def leaves(shape):
    if not shape.children:
        return [shape]
    result = []
    for child in shape.children:
        result.extend(leaves(child))
    return result


def canonical(shape):
    result = defaultdict(list)
    for leaf in leaves(shape):
        result[leaf.label].append((len(leaf.solids()), round(float(leaf.volume), 7)))
    return {key: sorted(values) for key, values in sorted(result.items())}


def case_workpiece(_: list[str]) -> None:
    p = p13.P13_DEFAULTS
    workpiece = p13.build_workpiece(p)
    assert workpiece.is_valid and len(workpiece.children) == 1 and len(workpiece.solids()) == 1
    box = workpiece.bounding_box()
    assert abs(box.min.Z - p.completed_workpiece_min_z) <= 2e-6
    assert abs(box.max.Y - (p.pad_y0 + p.solder_radius)) <= 2e-6
    assert abs(box.max.Z - p.xt60_body_z1) <= 2e-6


def case_occurrence(_: list[str]) -> None:
    labels = [leaf.label.lower() for leaf in leaves(p13.build_locked())]
    assert sum("fixed_od40p50" in label and "upward_c_journal" in label for label in labels) == 2
    assert sum("purchased_uncut_304" in label for label in labels) == 3
    assert not any(any(word in label for word in ("base", "spine", "bridge", "holder")) for label in labels)


def case_rods(args: list[str]) -> None:
    angle = float(args[0])
    plates = p13.build_principal_plates(angle).children
    rods = p13.build_rods(angle).children
    assert len(plates) == 4 and len(rods) == 3
    for plate in plates:
        assert plate.is_valid and len(plate.solids()) == 1
    for rod in rods:
        assert rod.is_valid and len(rod.solids()) == 1
        for plate in plates:
            assert overlap(rod, plate) <= 1e-7


def case_wire_preload(_: list[str]) -> None:
    """Actual-solid witness for tangent CONTACT and positive-overlap LOCK."""

    p = p13.P13_DEFAULTS
    wire = p13.build_wire(p.wire_x, p)
    for name in p13.ROD_NAMES:
        tangent = p13.build_rod(name, p.rise_end_deg, p)
        locked = p13.build_rod(name, p.locked_angle_deg, p)
        assert tangent.distance_to(wire) <= 2.0e-9
        assert overlap(tangent, wire) <= p.continuous_overlap_volume_tolerance
        assert overlap(locked, wire) > 0.30


def case_removal(_: list[str]) -> None:
    p = p13.P13_DEFAULTS
    structure = list(p13.build_four_plate_structure(p.open_angle_deg, p).children)
    workpiece = p13.build_workpiece(p).children[0]
    rods = list(p13.build_rods(p.open_angle_deg, p).children)
    cap_open_x = p.rod_length / 2.0 - p.nominal_cap_engagement
    cap_sweep = p13._x_cylinder(
        p.cap_od,
        p.cap_length + p.cap_removed_offset_x,
        cap_open_x + (p.cap_length + p.cap_removed_offset_x) / 2.0,
        0.0,
        0.0,
    )
    for index, name in enumerate(p13.ROD_NAMES):
        point = p13.rod_center(name, p.open_angle_deg, p)
        sweep_at_rod = Pos(0.0, point.y, point.z) * cap_sweep
        for rigid in [*structure, workpiece, *[rod for j, rod in enumerate(rods) if j != index]]:
            assert overlap(sweep_at_rod, rigid) <= 1e-7
        # Gate closure uses the continuous conservative swept-BREP cover of
        # the complete rod + permanent-left-cap unit, never a bare rod.
        complete_unit_envelope = p13.build_rod_left_cap_withdrawal_envelope(name, p)
        assert len(complete_unit_envelope.children) == 2
        assert any("full_rod_envelope" in child.label for child in complete_unit_envelope.children)
        assert any("permanent_left_cap_outer_envelope" in child.label for child in complete_unit_envelope.children)
        for swept_member in complete_unit_envelope.children:
            for rigid in [*structure, workpiece]:
                assert overlap(swept_member, rigid) <= 1e-7
        assert p13.build_left_cap(name, p.open_angle_deg, p).bounding_box().max.X < p.left_cam_slab_min_x
    endpoint = p13.build_three_rod_left_cap_units(
        p.open_angle_deg, p, -p.rod_withdrawal_distance
    )
    target = p.left_cam_slab_min_x - p.rod_exit_clearance
    for unit in endpoint.children:
        assert max(child.bounding_box().max.X for child in unit.children) <= target + 1e-7
    # Full +Z gate closure is the serialized global analytic certificate.
    # Discrete poses are retained only in the review artifact below.
    plus_z = p13.workpiece_plus_z_certificate(p)
    assert plus_z["plusZClearanceMonotone"]
    assert plus_z["globalMargin"]["value"] > 0.0
    continuous = p13.continuous_removal_certificate(p)
    assert continuous["completeWorkpieceLift"] == plus_z
    assert all(
        row["maximumIntersectionVolume"]["value"] == 0.0
        for row in continuous["rodLeftCapWithdrawal"].values()
    )
    review_labels = [leaf.label for leaf in leaves(p13.build_removal_sweep_review(p))]
    assert sum("removable_round_right" in label for label in review_labels) == 3
    assert sum("diagnostic_only_removal_plusZ_sample" in label for label in review_labels) == p.removal_review_sample_count


def case_forbidden(_: list[str]) -> None:
    p = p13.P13_DEFAULTS
    certificate = p13.shaft_service_extraction_certificate(p)
    assert not certificate["directPlusXWithFixedGuidesInstalled"]["admissible"]
    assert min(
        certificate["directPlusXWithFixedGuidesInstalled"]
        ["actualSolidIntersectionVolumes"]["value"].values()
    ) > 0.50
    assert certificate["stagedPlusXAfterFixedGuidesClear"]["maximumIntersectionVolume"]["value"] <= 1e-7
    assert "guides_minusZ_clear_then_separate_D_shaft_plusX" in p13.build_service_disassembly(p).label


def case_coupons(args: list[str]) -> None:
    coupons = p13.build_fit_coupons()
    assert len(coupons.children) == 2
    assert all(child.is_valid and len(child.solids()) == 1 for child in coupons.children)
    path = Path(args[0])
    assert export_step(p13.build_artifact("fit_coupons"), path)
    imported = import_step(path)
    coupon_leaves = [leaf for leaf in leaves(imported) if "coupon_role" in leaf.label]
    assert len(coupon_leaves) == 2 and all(len(child.solids()) == 1 for child in coupon_leaves)


def case_print(_: list[str]) -> None:
    kit = p13.build_print_kit()
    assert len(kit.children) == 14
    assert all(child.is_valid and abs(child.bounding_box().min.Z) <= 1e-7 for child in kit.children)
    for first, second in combinations(kit.children, 2):
        assert overlap(first, second) <= 1e-7
    exploded = leaves(p13.build_exploded())
    labels = [leaf.label for leaf in exploded]
    assert len(exploded) == 15
    for first, second in combinations(exploded, 2):
        assert overlap(first, second) <= 1e-7
    assert sum("purchased_uncut_304" in label for label in labels) == 3
    assert sum("permanent_round_left" in label for label in labels) == 3
    assert sum("removable_round_right" in label for label in labels) == 3
    assert sum("shaft_keeper" in label for label in labels) == 1
    assert sum("separate_printed_D_shaft" in label for label in labels) == 1


def case_parity(args: list[str]) -> None:
    name, path_raw = args[:2]
    overrides = json.loads(args[2]) if len(args) > 2 else {}
    p = p13.parameters_from_overrides(overrides)
    source = p13.build_artifact(name, p)
    imported = import_step(Path(path_raw))
    assert imported.is_valid and imported.label == source.label
    sb, ib = source.bounding_box(), imported.bounding_box()
    assert max(abs(a - b) for a, b in zip((*sb.min, *sb.max), (*ib.min, *ib.max))) <= 2e-6
    assert canonical(imported) == canonical(source)


CASES = {
    "workpiece": case_workpiece,
    "occurrence": case_occurrence,
    "rods": case_rods,
    "wire_preload": case_wire_preload,
    "removal": case_removal,
    "forbidden": case_forbidden,
    "coupons": case_coupons,
    "print": case_print,
    "parity": case_parity,
}


if __name__ == "__main__":
    CASES[sys.argv[1]](sys.argv[2:])
    print("PASS")
