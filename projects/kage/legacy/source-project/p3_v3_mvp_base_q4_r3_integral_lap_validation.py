"""Focused actual-solid evidence for the accepted Q4-R3 CAD gates."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from math import hypot
from pathlib import Path

from build123d import Align, Axis, Compound, Cylinder, Location

import p3_v3_mvp_base_q4_r1_geometry as locked_plain_geometry
import p3_v3_mvp_base_q4_r3_integral_lap_geometry as geometry
from p3_v3_mvp_base_q4_r3_integral_lap_spec import HANDOFF, NAMESPACE, ROOT, SPEC


FROZEN_TREE_HASHES = {
    "p3_v3_mvp_base_q4_r1": "477f855bfda1f12533e080feee45028f1cc8e94d501ce6e270d4e097920f6e93",
    "p3_v3_mvp_base_q4_r2_screw_only": "b26a17f40e6767b878c44558bf7e7b41b3da9aa11f62b5b4d8b5315f70a802c2",
}
HANDOFF_SHA256 = "1221b572f01877225b6cba7335d2b0b4baf267757a63da2cbe133d99c5570220"


def _tree_files(namespace: str) -> tuple[Path, ...]:
    files = [path for path in ROOT.glob(f"{namespace}*") if path.is_file()]
    files.extend(path for path in (ROOT / "tests").glob(f"test_{namespace}*") if path.is_file())
    model_root = ROOT / "models" / namespace
    if model_root.exists():
        files.extend(
            path for path in model_root.rglob("*")
            if path.is_file() and "__cadgen__" not in path.parts and "__pycache__" not in path.parts
        )
    return tuple(sorted(set(files), key=lambda path: path.as_posix()))


def namespace_tree_hash(namespace: str) -> str:
    digest = sha256()
    for path in _tree_files(namespace):
        relative = path.relative_to(ROOT).as_posix().encode()
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def part_registry_evidence() -> dict[str, object]:
    rows = geometry.printable_occurrences()
    forbidden = ("clamp", "bridge", "dowel", "pin", "insert", "carrier", "ring", "motor")
    labels = tuple(row["label"] for row in rows)
    return {
        "printable_count": len(rows),
        "labels": labels,
        "roles": tuple(row["kind"] for row in rows),
        "all_one_solid_valid": all(
            len(row["shape"].solids()) == 1 and row["shape"].is_valid and row["shape"].volume > 0.0 for row in rows
        ),
        "forbidden_occurrence_count": sum(any(word in label.lower() for word in forbidden) for label in labels),
    }


def all_seam_engagement_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    rows = []
    for seam_index, angle, a_index, b_index, sign in geometry.SEAMS:
        tongue_envelope = geometry.tongue_tool(angle, sign, include_fuse_overlap=False)
        roof_probe = geometry._seam_box(
            angle,
            SPEC.lap_radial_min_mm,
            SPEC.lap_radial_max_mm,
            min(0.0, sign * SPEC.tongue_overlap_depth_mm),
            max(0.0, sign * SPEC.tongue_overlap_depth_mm),
            SPEC.lap_interface_z_mm,
            SPEC.receiver_roof_thickness_mm,
        )
        a_shape = quadrants[a_index - 1]
        b_shape = quadrants[b_index - 1]
        rows.append({
            "seam_index": seam_index,
            "a_index": a_index,
            "b_index": b_index,
            "actual_a_tongue_material_mm3": geometry.intersection_volume_mm3(a_shape, tongue_envelope),
            "actual_b_roof_material_mm3": geometry.intersection_volume_mm3(b_shape, roof_probe),
            "seating_distance_mm": a_shape.distance_to(b_shape),
            "gross_radial_span_mm": SPEC.lap_radial_span_mm,
            "gross_overlap_depth_mm": SPEC.tongue_overlap_depth_mm,
        })
    return {
        "rows": tuple(rows),
        "seam_count": len(rows),
        "all_expected_ownership": tuple((row["a_index"], row["b_index"]) for row in rows) == ((1, 4), (1, 2), (3, 2), (3, 4)),
        "minimum_tongue_material_mm3": min(row["actual_a_tongue_material_mm3"] for row in rows),
        "minimum_roof_material_mm3": min(row["actual_b_roof_material_mm3"] for row in rows),
        "maximum_seating_distance_mm": max(row["seating_distance_mm"] for row in rows),
    }


def no_collision_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    rows = tuple(
        {"pair": (i + 1, j + 1), "intersection_mm3": geometry.intersection_volume_mm3(quadrants[i], quadrants[j])}
        for i in range(4) for j in range(i + 1, 4)
    )
    return {"rows": rows, "maximum_intersection_mm3": max(row["intersection_mm3"] for row in rows)}


def straight_z_path_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    offsets = tuple(SPEC.assembly_start_z_mm - SPEC.assembly_path_step_mm * i for i in range(21))
    rows = []
    seated_q2 = deepcopy(quadrants[1])
    for moving_index, fixed_indices in ((2, (1, 3)), (4, (1, 2, 3))):
        fixed_children = [deepcopy(quadrants[index - 1]) for index in fixed_indices]
        if moving_index == 4:
            fixed_children[1] = seated_q2
        fixed = Compound(children=fixed_children, label=f"fixed_before_Q{moving_index}")
        samples = tuple(
            geometry.intersection_volume_mm3(
                deepcopy(quadrants[moving_index - 1]).moved(Location((0.0, 0.0, z))), fixed
            )
            for z in offsets
        )
        rows.append({"moving_quadrant": moving_index, "offsets_mm": offsets, "intersections_mm3": samples, "maximum_intersection_mm3": max(samples)})
    return {
        "rows": tuple(rows),
        "sample_step_mm": SPEC.assembly_path_step_mm,
        "start_z_mm": offsets[0],
        "end_z_mm": offsets[-1],
        "maximum_intersection_mm3": max(row["maximum_intersection_mm3"] for row in rows),
    }


def hardware_evidence() -> dict[str, object]:
    printed = geometry.assembled_printed_shape()
    rows = []
    for seam_index in range(1, 5):
        for radius in SPEC.screw_axis_radii_mm:
            shaft = geometry.nominal_screw_shaft_shape(seam_index, radius)
            nut = geometry.nominal_nut_shape(seam_index, radius)
            rows.append({
                "seam_index": seam_index,
                "radius_mm": radius,
                "shaft_printed_intersection_mm3": geometry.intersection_volume_mm3(shaft, printed),
                "nut_printed_intersection_mm3": geometry.intersection_volume_mm3(nut, printed),
                "driver_obstruction_mm3": geometry.intersection_volume_mm3(geometry.driver_access_shape(seam_index, radius), printed),
                "wrench_obstruction_mm3": geometry.intersection_volume_mm3(geometry.wrench_access_shape(seam_index, radius), printed),
                "shaft_nut_intersection_mm3": geometry.intersection_volume_mm3(shaft, nut),
            })
    def protrusion(length: float) -> float:
        return length - SPEC.base_thickness_mm - SPEC.m3_nut_max_thickness_mm
    return {
        "rows": tuple(rows),
        "interface_count": len(rows),
        "maximum_unintended_intersection_mm3": max(
            value for row in rows for value in (
                row["shaft_printed_intersection_mm3"], row["nut_printed_intersection_mm3"],
                row["driver_obstruction_mm3"], row["wrench_obstruction_mm3"],
            )
        ),
        "minimum_shaft_nut_intersection_mm3": min(row["shaft_nut_intersection_mm3"] for row in rows),
        "m3x5_protrusion_mm": protrusion(5.0),
        "m3x6_protrusion_mm": protrusion(6.0),
        "m3x8_protrusion_mm": protrusion(8.0),
        "m3x5_accepted": 0.8 <= protrusion(5.0) <= 1.4,
        "m3x6_accepted": 0.8 <= protrusion(6.0) <= 1.4,
        "m3x8_accepted": 0.8 <= protrusion(8.0) <= 1.4,
    }


def _registration_case(translation: tuple[float, float, float]) -> dict[str, object]:
    seam_index, angle, a_index, b_index, _ = geometry.SEAMS[0]
    a_shape = deepcopy(geometry.quadrant_shapes()[a_index - 1])
    b_shape = deepcopy(geometry.quadrant_shapes()[b_index - 1]).moved(Location(translation))
    shaft_intersections = tuple(
        geometry.intersection_volume_mm3(geometry.nominal_screw_shaft_shape(seam_index, radius), b_shape)
        for radius in SPEC.screw_axis_radii_mm
    )
    pair_intersection = geometry.intersection_volume_mm3(a_shape, b_shape)
    passed = max((*shaft_intersections, pair_intersection)) <= SPEC.brep_intersection_tolerance_mm3 and a_shape.distance_to(b_shape) <= SPEC.cad_linear_tolerance_mm
    return {
        "translation_mm": translation,
        "shaft_intersections_mm3": shaft_intersections,
        "pair_intersection_mm3": pair_intersection,
        "registration_pass": passed,
    }


def registration_negative_evidence() -> dict[str, object]:
    _, angle, _, _, sign = geometry.SEAMS[0]
    radial = geometry.local_point(angle, SPEC.registration_negative_shift_mm, 0.0)
    cross = geometry.local_point(angle, 0.0, sign * SPEC.registration_negative_shift_mm)
    cases = {
        "nominal": _registration_case((0.0, 0.0, 0.0)),
        "radial_shift": _registration_case((radial[0], radial[1], 0.0)),
        "cross_seam_shift": _registration_case((cross[0], cross[1], 0.0)),
    }
    return {
        "cases": cases,
        "nominal_pass": cases["nominal"]["registration_pass"],
        "all_negatives_rejected": not cases["radial_shift"]["registration_pass"] and not cases["cross_seam_shift"]["registration_pass"],
    }


def flatness_evidence() -> dict[str, object]:
    tops = tuple(float(shape.bounding_box().max.Z) for shape in geometry.quadrant_shapes())
    return {
        "polymer_top_z_mm": tops,
        "maximum_top_deviation_mm": max(abs(value - SPEC.base_thickness_mm) for value in tops),
        "nominal_polymer_step_mm": max(tops) - min(tops),
        "socket_head_projection_mm": SPEC.m3_socket_head_height_mm,
    }


def _max_vertex_radius(shape) -> float:
    return max(hypot(vertex.X, vertex.Y) for vertex in shape.vertices())


def keepout_and_outline_evidence() -> dict[str, object]:
    quadrants = geometry.quadrant_shapes()
    plain = locked_plain_geometry.plain_quadrant_shapes()
    keepout = Cylinder(SPEC.base_outer_radius_mm, SPEC.base_thickness_mm, align=(Align.CENTER, Align.CENTER, Align.MIN)).cut(
        Cylinder(SPEC.future_support_clear_radius_min_mm, SPEC.base_thickness_mm + 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((0.0, 0.0, -0.5)))
    )
    removed_in_keepout = tuple(
        max(0.0, geometry.intersection_volume_mm3(plain[i], keepout) - geometry.intersection_volume_mm3(quadrants[i], keepout))
        for i in range(4)
    )
    tools = []
    for seam_index, angle, _, _, sign in geometry.SEAMS:
        tools.extend((geometry.tongue_tool(angle, sign), geometry.rebate_tool(angle, sign)))
        tools.extend(
            geometry.vertical_cylinder(angle, radius, sign * SPEC.screw_axis_tangent_into_b_mm,
                                       SPEC.clearance_hole_diameter_mm, 0.0, SPEC.base_thickness_mm)
            for radius in SPEC.screw_axis_radii_mm
        )
    assembly_box = geometry.assembled_printed_shape().bounding_box()
    return {
        "outer_diameter_mm": max(assembly_box.size.X, assembly_box.size.Y),
        "inner_diameter_mm": 2.0 * SPEC.base_inner_radius_mm,
        "maximum_functional_vertex_radius_mm": max(_max_vertex_radius(tool) for tool in tools),
        "removed_in_keepout_mm3": removed_in_keepout,
        "maximum_keepout_void_mm3": max(removed_in_keepout),
    }


def bed_fit_evidence() -> dict[str, object]:
    rows = []
    for row in geometry.printable_occurrences():
        box = row["shape"].bounding_box()
        span = (float(box.size.X), float(box.size.Y), float(box.size.Z))
        rows.append({
            "name": row["name"],
            "orientation": row["orientation"],
            "span_mm": span,
            "span_with_brim_xy_mm": (span[0] + 2.0 * SPEC.quadrant_brim_mm, span[1] + 2.0 * SPEC.quadrant_brim_mm),
            "z_floor_error_mm": abs(float(box.min.Z)),
            "one_solid": len(row["shape"].solids()) == 1,
        })
    return {
        "rows": tuple(rows),
        "all_fit": all(max(row["span_with_brim_xy_mm"]) <= SPEC.u1_usable_xy_mm for row in rows),
        "all_on_bed": all(row["z_floor_error_mm"] <= 1.0e-7 for row in rows),
        "all_one_solid": all(row["one_solid"] for row in rows),
        "orientations": tuple(row["orientation"] for row in rows),
    }


def version_isolation_evidence() -> dict[str, object]:
    actual = {namespace: namespace_tree_hash(namespace) for namespace in FROZEN_TREE_HASHES}
    return {
        "expected": FROZEN_TREE_HASHES,
        "actual": actual,
        "all_frozen_tree_hashes_match": actual == FROZEN_TREE_HASHES,
        "handoff_sha256": sha256(HANDOFF.read_bytes()).hexdigest(),
        "handoff_hash_matches": sha256(HANDOFF.read_bytes()).hexdigest() == HANDOFF_SHA256,
    }
