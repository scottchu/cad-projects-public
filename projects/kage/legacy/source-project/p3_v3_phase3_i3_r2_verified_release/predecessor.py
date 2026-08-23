"""Single audited read-only boundary to the rejected R1 reference registry."""

from __future__ import annotations

from p3_v3_phase3_i3_r1_real_joinery_geometry import (
    _REPLACED_INDICES,
    baseline_rows,
    candidate_occurrences,
)


def r1_reference_registry() -> tuple[dict[str, object], ...]:
    """Return fresh row dictionaries from the rejected predecessor reference."""

    return tuple(dict(row) for row in candidate_occurrences())


def r1_reference_protected_registry() -> tuple[dict[str, object], ...]:
    rows = []
    for name, shape in baseline_rows():
        if name.startswith("occurrence_") and int(name.rsplit("_", 1)[1]) in _REPLACED_INDICES:
            continue
        rows.append(
            {
                "name": name,
                "label": str(shape.label),
                "shape": shape,
                "classification": "protected_exact",
                "printable": False,
            }
        )
    if len(rows) != 131:
        raise RuntimeError(f"R1 protected registry count drifted to {len(rows)}")
    return tuple(rows)
