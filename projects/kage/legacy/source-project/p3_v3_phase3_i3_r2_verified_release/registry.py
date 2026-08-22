"""R2 successor registry and exact predecessor comparison."""

from __future__ import annotations

from typing import Any

from .geometry import moving_half_shapes, protected_occurrence_rows, semantic_shape_facts, volume
from .predecessor import r1_reference_protected_registry, r1_reference_registry
from .spec import DEFAULT_OWNERS, OwnerBundle


MOVING_NAMES = tuple(
    f"i3_r1_{role}_half_{half}"
    for role in ("hour", "minute", "second")
    for half in ("A", "B")
)


def _light_shape_fact(shape) -> dict[str, Any]:
    bounds = shape.bounding_box()
    position, orientation = shape.location.to_tuple()
    return {
        "transform": tuple(float(value) for value in (*position, *orientation)),
        "topology": tuple(
            (name, len(getattr(shape, name)()))
            for name in ("vertices", "edges", "wires", "faces", "shells", "solids", "compounds")
        ),
        "aabb_mm": (
            float(bounds.min.X), float(bounds.min.Y), float(bounds.min.Z),
            float(bounds.max.X), float(bounds.max.Y), float(bounds.max.Z),
        ),
        "area_mm2": float(shape.area),
        "volume_mm3": volume(shape),
    }


def _row_fact(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": row["name"],
        "classification": row["classification"],
        "printable": bool(row.get("printable")),
        "kind": row.get("kind"),
        "shape": semantic_shape_facts(row["shape"]),
    }


def successor_registry(owners: OwnerBundle = DEFAULT_OWNERS) -> tuple[dict[str, Any], ...]:
    replacements = {
        f"i3_r1_{role}_half_{half}": shape
        for (role, half), shape in moving_half_shapes(owners).items()
    }
    rows = []
    for source in r1_reference_registry():
        row = dict(source)
        if row["name"] in replacements:
            shape = replacements[str(row["name"])]
            row["shape"] = shape
            row["label"] = shape.label
        rows.append(row)
    return tuple(rows)


def protected_registry_comparison(owners: OwnerBundle = DEFAULT_OWNERS) -> dict[str, Any]:
    """Compare true R1 protected rows with the perturbed R2 successor partition."""

    predecessor = {str(row["name"]): row for row in r1_reference_protected_registry()}
    successor = {
        name: {
            "name": name,
            "label": str(shape.label),
            "shape": shape,
            "classification": "protected_exact",
            "printable": False,
        }
        for name, shape in protected_occurrence_rows()
    }
    rows = []
    drift = []
    for name in sorted(set(predecessor) | set(successor)):
        before = predecessor.get(name)
        after = successor.get(name)
        equal = bool(
            before is not None
            and after is not None
            and {key: value for key, value in before.items() if key != "shape"}
            == {key: value for key, value in after.items() if key != "shape"}
            and _light_shape_fact(before["shape"]) == _light_shape_fact(after["shape"])
        )
        rows.append({"name": name, "equal": equal, "mode": "r1_vs_r2_exact_metadata_plus_actual_solid_facts"})
        if not equal:
            drift.append(name)
    return {
        "predecessor_source": "R1 baseline_rows protected partition",
        "successor_source": "R2 protected_occurrence_rows under supplied owner bundle",
        "predecessor_count": len(predecessor),
        "successor_count": len(successor),
        "protected_ids": sorted(predecessor),
        "comparison_rows": rows,
        "protected_drift": drift,
        "passed": len(predecessor) == len(successor) == 131 and not drift,
    }


def registry_comparison(owners: OwnerBundle = DEFAULT_OWNERS) -> dict[str, Any]:
    predecessor = r1_reference_registry()
    successor = successor_registry(owners)
    predecessor_by_name = {str(row["name"]): row for row in predecessor}
    successor_by_name = {str(row["name"]): row for row in successor}
    predecessor_names = set(predecessor_by_name)
    successor_names = set(successor_by_name)
    counts = {
        classification: sum(
            row["classification"] == classification for row in predecessor
        )
        for classification in ("protected_exact", "authorized_replacement", "new_authorized")
    }
    changed = []
    protected_drift = []
    unauthorized_drift = []
    comparison_rows = []
    for name in sorted(predecessor_names & successor_names):
        source_row = predecessor_by_name[name]
        successor_row = successor_by_name[name]
        metadata_before = {key: value for key, value in source_row.items() if key != "shape"}
        metadata_after = {key: value for key, value in successor_row.items() if key != "shape"}
        if name in MOVING_NAMES:
            before = _row_fact(source_row)
            after = _row_fact(successor_row)
            comparison_mode = "independent_semantic_brep"
            equal = before == after
        elif source_row["classification"] == "protected_exact":
            comparison_mode = "exact_shared_brep_identity_plus_actual_solid_facts"
            equal = (
                metadata_before == metadata_after
                and source_row["shape"] is successor_row["shape"]
                and _light_shape_fact(source_row["shape"])
                == _light_shape_fact(successor_row["shape"])
            )
        else:
            comparison_mode = "exact_reused_shape_identity_and_metadata"
            equal = (
                metadata_before == metadata_after
                and source_row["shape"] is successor_row["shape"]
            )
        comparison_rows.append({"name": name, "mode": comparison_mode, "equal": equal})
        if not equal:
            changed.append(name)
            if source_row["classification"] == "protected_exact":
                protected_drift.append(name)
            if name not in MOVING_NAMES:
                unauthorized_drift.append(name)
    protected_ids = sorted(
        str(row["name"])
        for row in predecessor
        if row["classification"] == "protected_exact"
    )
    return {
        "predecessor_source": "p3_v3_phase3_i3_r1_real_joinery_geometry.candidate_occurrences",
        "successor_source": "p3_v3_phase3_i3_r2_verified_release.registry.successor_registry",
        "predecessor_count": len(predecessor),
        "successor_count": len(successor),
        "predecessor_partition_counts": counts,
        "missing_ids": sorted(predecessor_names - successor_names),
        "extra_ids": sorted(successor_names - predecessor_names),
        "protected_ids": protected_ids,
        "protected_count": len(protected_ids),
        "protected_drift": protected_drift,
        "changed_ids": changed,
        "authorized_changed_ids": sorted(MOVING_NAMES),
        "unauthorized_drift": unauthorized_drift,
        "comparison_rows": comparison_rows,
        "passed": (
            len(predecessor) == len(successor) == 275
            and counts
            == {"protected_exact": 131, "authorized_replacement": 18, "new_authorized": 126}
            and not (predecessor_names ^ successor_names)
            and len(protected_ids) == 131
            and not protected_drift
            and changed == sorted(MOVING_NAMES)
            and not unauthorized_drift
        ),
    }
