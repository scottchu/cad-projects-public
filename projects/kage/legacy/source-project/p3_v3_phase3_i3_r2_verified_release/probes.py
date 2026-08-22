"""Fresh-process, actual-BREP parameter-consumption probes for R2."""

from __future__ import annotations

import argparse
import ast
from dataclasses import FrozenInstanceError
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from .geometry import actual_geometry_evidence, moving_half_shapes, parameter_change_locality, volume
from .registry import protected_registry_comparison
from .spec import DEFAULT_OWNERS, adjusted_owner_bundle, adjustable_field_specs


PACKAGE_ROOT = Path(__file__).resolve().parent
GEOMETRY_PATH = PACKAGE_ROOT / "geometry.py"


def _canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=list).encode()
    return sha256(payload).hexdigest()


def _shape_summaries(owners, geometry_evidence) -> dict[str, dict[str, object]]:
    rows = {}
    for (role, half), shape in moving_half_shapes(owners).items():
        rows[f"{role}_{half}"] = {
            "brep_sha256": next(
                row[f"half_{half.lower()}_brep_sha256"]
                for row in geometry_evidence["seams"]
                if row["role"] == role
            ),
            "volume_mm3": volume(shape),
        }
    return rows


def _ranges(evidence: dict[str, Any]) -> dict[str, list[float]]:
    return {
        "radial_receive_clearance_mm": evidence["radial_clearance_range_mm"],
        "tangential_receive_clearance_mm": evidence["tangential_clearance_range_mm"],
        "butt_gap_mm": evidence["butt_gap_range_mm"],
        "axial_gap_mm": evidence["axial_gap_range_mm"],
    }


def _worker(field_name: str) -> dict[str, object]:
    spec = next(row for row in adjustable_field_specs() if row["field"] == field_name)
    changed_value = float(spec["value"]) + float(spec["probe_delta"])
    changed_owners = adjusted_owner_bundle(
        DEFAULT_OWNERS,
        str(spec["owner"]),
        field_name,
        changed_value,
    )
    baseline_geometry = actual_geometry_evidence(DEFAULT_OWNERS)
    changed_geometry = actual_geometry_evidence(changed_owners)
    baseline_shapes = _shape_summaries(DEFAULT_OWNERS, baseline_geometry)
    changed_shapes = _shape_summaries(changed_owners, changed_geometry)
    locality = parameter_change_locality(DEFAULT_OWNERS, changed_owners, field_name)
    baseline_registry = protected_registry_comparison(DEFAULT_OWNERS)
    changed_registry = protected_registry_comparison(changed_owners)
    protected_drift = sorted(
        set(baseline_registry["protected_drift"]) | set(changed_registry["protected_drift"])
    )

    baseline_ranges = _ranges(baseline_geometry)
    changed_ranges = _ranges(changed_geometry)
    if field_name == "receive_xy_clearance_mm":
        intended = ("radial_receive_clearance_mm", "tangential_receive_clearance_mm")
        unchanged = ("butt_gap_mm", "axial_gap_mm")
        expected_changed_halves = {name for name in baseline_shapes if name.endswith("_B")}
    elif field_name == "butt_face_relief_mm":
        intended = ("butt_gap_mm",)
        unchanged = (
            "radial_receive_clearance_mm",
            "tangential_receive_clearance_mm",
            "axial_gap_mm",
        )
        expected_changed_halves = set(baseline_shapes)
    else:
        raise ValueError(f"unsupported Checkpoint A adjustable field {field_name!r}")

    changed_halves = {
        str(row["half_id"])
        for row in locality
        if float(row["delta_volume_mm3"]) > 1e-9 and int(row["delta_face_count"]) > 0
    }
    minimum_linear_change = min(
        abs(changed_ranges[name][0] - baseline_ranges[name][0]) for name in intended
    )
    unchanged_witness_drift = {
        name: max(
            abs(changed_ranges[name][index] - baseline_ranges[name][index])
            for index in (0, 1)
        )
        for name in unchanged
    }
    return {
        "field": field_name,
        "owner": spec["owner"],
        "baseline_value": spec["value"],
        "probe_delta": spec["probe_delta"],
        "changed_value": changed_value,
        "baseline_ranges": baseline_ranges,
        "changed_ranges": changed_ranges,
        "baseline_semantic_digest": _canonical_digest(
            {"ranges": baseline_ranges, "shapes": baseline_shapes}
        ),
        "changed_semantic_digest": _canonical_digest(
            {"ranges": changed_ranges, "shapes": changed_shapes}
        ),
        "minimum_intended_linear_change_mm": minimum_linear_change,
        "changed_halves": sorted(changed_halves),
        "expected_changed_halves": sorted(expected_changed_halves),
        "unchanged_witness_drift_mm": unchanged_witness_drift,
        "locality": locality,
        "locality_acceptance_basis": "actual_brep_symmetric_difference_faces_bounded_by_owned_tools",
        "protected_count": baseline_registry["predecessor_count"],
        "baseline_registry": baseline_registry,
        "changed_registry": changed_registry,
        "protected_before_digest": _canonical_digest(baseline_registry["protected_ids"]),
        "protected_after_digest": _canonical_digest(changed_registry["protected_ids"]),
        "protected_drift": protected_drift,
        "passed": (
            minimum_linear_change >= 1e-4
            and changed_halves == expected_changed_halves
            and all(value <= 1e-7 for value in unchanged_witness_drift.values())
            and not protected_drift
            and baseline_registry["passed"]
            and changed_registry["passed"]
            and all(float(row["outside_owned_region_mm3"]) <= 1e-7 for row in locality)
            and all(
                float(row["owned_region_intersection_mm3"]) > 1e-9
                for row in locality
                if row["half_id"] in expected_changed_halves
            )
        ),
    }


def run_fresh_process_probe(field_name: str) -> dict[str, object]:
    command = [sys.executable, "-m", __name__, "--worker", field_name]
    completed = subprocess.run(command, cwd=PACKAGE_ROOT.parent, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(
            f"fresh R2 probe {field_name} failed with {completed.returncode}: {completed.stderr}"
        )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError(f"fresh R2 probe {field_name} emitted no evidence")
    return json.loads(lines[-1])


def analyze_parameter_consumption(module_sources: dict[str, str]) -> dict[str, object]:
    adjustable = adjustable_field_specs()
    production_consumers: dict[str, list[dict[str, object]]] = {
        str(row["field"]): [] for row in adjustable
    }
    validation_consumers: dict[str, list[dict[str, object]]] = {
        str(row["field"]): [] for row in adjustable
    }
    duplicated_literals: dict[str, list[int]] = {str(row["field"]): [] for row in adjustable}

    def names_in(node: ast.AST) -> set[str]:
        return {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}

    def called_names(node: ast.AST) -> set[str]:
        names = set()
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            cursor = child.func
            while isinstance(cursor, ast.Attribute):
                cursor = cursor.value
            if isinstance(cursor, ast.Name):
                names.add(cursor.id)
        return names

    def assigned_name(node: ast.Assign | ast.AnnAssign) -> str | None:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if len(targets) == 1 and isinstance(targets[0], ast.Name):
            return targets[0].id
        return None

    for module_name, source in module_sources.items():
        tree = ast.parse(source)
        parents: dict[ast.AST, ast.AST] = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent
        functions = {
            node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
        }
        imported_solids = set()
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "build123d":
                imported_solids.update(
                    alias.asname or alias.name
                    for alias in node.names
                    if alias.name in {"Box", "Cylinder", "Compound", "Sphere", "Cone", "Torus"}
                )

        # A local function is a solid constructor only when a returned value
        # actually calls a build123d constructor (directly or transitively).
        solid_builders = set(imported_solids)
        changed = True
        while changed:
            changed = False
            for function_name, function in functions.items():
                if function_name in solid_builders:
                    continue
                returns = [node.value for node in ast.walk(function) if isinstance(node, ast.Return) and node.value]
                if any(called_names(value) & solid_builders for value in returns):
                    solid_builders.add(function_name)
                    changed = True

        # Boolean functions are discovered from actual .cut/.fuse/.intersect
        # calls, not from their Python names.
        boolean_functions = {
            function_name
            for function_name, function in functions.items()
            if any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"cut", "fuse", "intersect"}
                for node in ast.walk(function)
            )
        }

        producer_keys: dict[tuple[str, str], list[dict[str, object]]] = {}
        raw_reads: dict[str, list[dict[str, object]]] = {
            str(row["field"]): [] for row in adjustable
        }
        for function_name, function in functions.items():
            assignments = [
                node
                for node in ast.walk(function)
                if isinstance(node, (ast.Assign, ast.AnnAssign))
                and assigned_name(node) is not None
            ]
            returned_dicts = [
                node.value
                for node in ast.walk(function)
                if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict)
            ]
            for field_name in raw_reads:
                field_nodes = [
                    node
                    for node in ast.walk(function)
                    if isinstance(node, ast.Attribute) and node.attr == field_name
                ]
                raw_reads[field_name].extend(
                    {"module": module_name, "function": function_name, "line": node.lineno}
                    for node in field_nodes
                )
                if not field_nodes:
                    continue
                tainted = set()
                solid_seed_lines = []
                for assignment in assignments:
                    value = assignment.value
                    if any(field_node in set(ast.walk(value)) for field_node in field_nodes):
                        target = assigned_name(assignment)
                        if target and called_names(value) & solid_builders:
                            tainted.add(target)
                            solid_seed_lines.append(assignment.lineno)
                propagated = True
                while propagated:
                    propagated = False
                    for assignment in assignments:
                        target = assigned_name(assignment)
                        if target and target not in tainted and names_in(assignment.value) & tainted:
                            tainted.add(target)
                            propagated = True
                for returned in returned_dicts:
                    for key, value in zip(returned.keys, returned.values, strict=True):
                        if (
                            isinstance(key, ast.Constant)
                            and isinstance(key.value, str)
                            and names_in(value) & tainted
                        ):
                            producer_keys.setdefault((function_name, key.value), []).append(
                                {
                                    "module": module_name,
                                    "producer_function": function_name,
                                    "tool_key": key.value,
                                    "field": field_name,
                                    "solid_seed_lines": sorted(set(solid_seed_lines)),
                                    "return_line": returned.lineno,
                                }
                            )

        # Follow each returned tool into a real Boolean call whose result is a
        # solid variable placed in the enclosing function's returned mapping.
        for function_name, function in functions.items():
            return_names = set()
            for node in ast.walk(function):
                if isinstance(node, ast.Return) and node.value:
                    return_names.update(names_in(node.value))
            output_solids = set(return_names)
            for node in ast.walk(function):
                if not isinstance(node, ast.Assign):
                    continue
                for target in node.targets:
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.value, ast.Name)
                        and target.value.id in return_names
                        and isinstance(node.value, ast.Name)
                    ):
                        output_solids.add(node.value.id)

            producer_bindings: dict[str, str] = {}
            for node in ast.walk(function):
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                target = assigned_name(node)
                if target and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    producer_bindings[target] = node.value.func.id

            for node in ast.walk(function):
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                target = assigned_name(node)
                call = node.value if isinstance(node.value, ast.Call) else None
                if not target or target not in output_solids or call is None:
                    continue
                if isinstance(call.func, ast.Name):
                    is_boolean = call.func.id in boolean_functions
                    boolean_name = call.func.id
                elif isinstance(call.func, ast.Attribute):
                    is_boolean = call.func.attr in {"cut", "fuse", "intersect"}
                    boolean_name = call.func.attr
                else:
                    is_boolean = False
                    boolean_name = ""
                if not is_boolean:
                    continue
                for subscript in (child for child in ast.walk(call) if isinstance(child, ast.Subscript)):
                    if not isinstance(subscript.value, ast.Name):
                        continue
                    tool_variable = subscript.value.id
                    producer = producer_bindings.get(tool_variable)
                    slice_node = subscript.slice
                    if not producer or not isinstance(slice_node, ast.Constant) or not isinstance(slice_node.value, str):
                        continue
                    key = slice_node.value
                    for seed in producer_keys.get((producer, key), []):
                        field_name = str(seed["field"])
                        production_consumers[field_name].append(
                            {
                                **seed,
                                "consumer_function": function_name,
                                "boolean_operation": boolean_name,
                                "boolean_line": node.lineno,
                                "returned_solid_variable": target,
                            }
                        )

        for field_name, reads in raw_reads.items():
            proven_locations = {
                (str(row["module"]), str(row["producer_function"]))
                for row in production_consumers[field_name]
            }
            validation_consumers[field_name].extend(
                row
                for row in reads
                if (str(row["module"]), str(row["function"])) not in proven_locations
            )

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                for row in adjustable:
                    if float(node.value) == float(row["value"]):
                        duplicated_literals[str(row["field"])].append(node.lineno)

    return {
        "adjustable_fields": adjustable,
        "production_consumers": production_consumers,
        "validation_consumers": validation_consumers,
        "duplicated_geometry_literals": {
            name: sorted(set(lines)) for name, lines in duplicated_literals.items() if lines
        },
        "proof_contract": (
            "owner attribute -> build123d-backed solid seed -> returned tool key -> "
            "actual cut/fuse/intersect -> returned solid"
        ),
        "solid_builder_functions": sorted(solid_builders),
        "boolean_functions": sorted(boolean_functions),
        "all_adjustable_fields_consumed": all(production_consumers.values()),
        "no_duplicated_geometry_literals": not any(duplicated_literals.values()),
    }


def ast_parameter_consumption_evidence() -> dict[str, object]:
    return analyze_parameter_consumption(
        {"geometry.py": GEOMETRY_PATH.read_text(encoding="utf-8")}
    )


def immutability_evidence() -> dict[str, object]:
    rejected = []
    try:
        DEFAULT_OWNERS.moving_joinery.axial_gap_mm = 99.0  # type: ignore[misc]
    except FrozenInstanceError as exc:
        rejected.append(type(exc).__name__)
    return {
        "required_owner_names": [
            "segmentation",
            "moving_joinery",
            "chassis_joinery",
            "frame_joinery",
            "front_ring_joinery",
            "motion_validation",
            "print_transform",
            "mesh_contract",
            "orca_contract",
            "freshness_contract",
            "release_contract",
            "artifact_contract",
        ],
        "actual_owner_names": list(DEFAULT_OWNERS.__dataclass_fields__),
        "mutation_rejections": rejected,
        "passed": bool(rejected),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=[row["field"] for row in adjustable_field_specs()])
    args = parser.parse_args(argv)
    if args.worker:
        print(json.dumps(_worker(args.worker), sort_keys=True, separators=(",", ":")))
        return 0
    parser.error("--worker is required")


if __name__ == "__main__":
    raise SystemExit(main())
