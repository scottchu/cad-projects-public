"""Generate the closed-assembly CAD Viewer parameter readout sidecar.

This module deliberately produces a snapshot, not a customizer: CAD Viewer
cannot pass a changed control value back through the build123d generator.
"""
from dataclasses import fields
import json
from math import isfinite
from pathlib import Path

from .derive import derive as resolve_parameters
from .parameters import PARAMETER_SPECS, Parameters, preset


NOTICE_ID = "read_only_notice"
NOTICE_VALUE = "Current values - edit Python and regenerate STEP to change"
VISUAL_NOTICE_ID = "visual_preview_only"
VISUAL_NOTICE_VALUE = "Deforms or styles the displayed mesh. CAD and STEP stay unchanged."
ROW_DESCRIPTION = (
    "Read-only snapshot. Edit parameters.py and regenerate STEP to change CAD."
)
VISUAL_DESCRIPTION = (
    "Render only. Changes the displayed mesh, not CAD, STEP, fit, wall thickness, "
    "thread clearance, or printability."
)
BODY_OCCURRENCE_NAME = (
    "R7 body: 39mm diamond skin; new B right-hand thread; smooth chamfer with seven drains"
)
CAP_OCCURRENCE_NAME = (
    "R7 cap C25: new B thread; 39mm diamond skin; smooth end chamfer; seven drains"
)
BODY_COLOR = "#7097b3"
CAP_COLOR = "#77b09a"

VISUAL_CONTROLS = (
    ("visual_radial_scale_pct", "01 Visual - Common radial scale", "number", 100, 60, 160, 1, "%"),
    ("visual_axial_scale_pct", "01 Visual - Common axial scale", "number", 100, 60, 160, 1, "%"),
    ("visual_body_axial_scale_pct", "01 Visual - Body axial scale", "number", 100, 60, 160, 1, "%"),
    ("visual_cap_axial_scale_pct", "01 Visual - Cap axial scale", "number", 100, 60, 160, 1, "%"),
    ("visual_cap_unscrew_turns", "02 Visual - Cap unscrew", "number", 0, 0, 3, 0.25, "rev"),
    ("visual_cap_extra_lift_mm", "02 Visual - Cap extra lift", "number", 0, 0, 60, 1, "mm"),
    ("visual_body_color", "03 Visual - Body color", "color", BODY_COLOR, None, None, None, ""),
    ("visual_cap_color", "03 Visual - Cap color", "color", CAP_COLOR, None, None, None, ""),
    ("visual_body_opacity", "03 Visual - Body opacity", "number", 1, 0.10, 1, 0.05, ""),
    ("visual_cap_opacity", "03 Visual - Cap opacity", "number", 1, 0.10, 1, 0.05, ""),
)
GROUPS = (
    ("Axial", "axial"),
    ("Device reference", "reference"),
    ("Radial", "radial"),
    ("Exterior", "exterior"),
    ("Thread", "thread"),
    ("Skin", "skin"),
    ("Ends", "ends"),
    ("Drains", "drains"),
)
CLASSIFICATIONS = {
    "adjustable_geometry": "adjustable in Python",
    "reference_readout_only": "reference only; does not resize CAD",
    "locked": "locked P1 R7 value",
}


def _humanize(identifier):
    return identifier.replace("_", " ").title()


def _unit_label(unit):
    return {"mm_radial": "mm radial"}.get(unit, unit)


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError("preview readout values must be finite numbers")
    return str(int(value)) if float(value).is_integer() else format(value, ".12g")


def _source_value(value, unit):
    if isinstance(value, str):
        return value
    return f"{_number(value)} {_unit_label(unit)}"


def _row(label, value):
    return {
        "type": "enum",
        "label": label,
        "description": ROW_DESCRIPTION,
        "options": [{"value": value, "label": value}],
        "default": value,
    }


def _visual_row(identifier, label, row_type, default, minimum, maximum, step, unit):
    row = {
        "type": row_type,
        "label": label,
        "description": VISUAL_DESCRIPTION,
        "default": default,
        "renderOnly": True,
        "geometryRegeneration": False,
    }
    if row_type == "number":
        row.update({"min": minimum, "max": maximum, "step": step, "unit": unit})
    return row


def _derived_value(resolved, identifier):
    values = {
        "derived__cavity_length": (resolved.cavity_length, "mm", "", ""),
        "derived__outer_length": (resolved.outer_length, "mm", "", ""),
        "derived__body_cavity_depth": (resolved.body_depth, "mm", "", ""),
        "derived__body_height": (resolved.body_depth + resolved.floor + resolved.neck_height, "mm", "", ""),
        "derived__cap_height": (resolved.cap_height, "mm", "", ""),
        "derived__thread_turns": (resolved.engagement / resolved.thread_pitch, "rev", "", ""),
        "derived__body_radial_gap": (resolved.body_radial_gap, "mm radial", "", ", reference only"),
        "derived__cap_radial_gap": (resolved.cap_radial_gap, "mm radial", "", ", reference only"),
        "derived__lattice_count": (resolved.lattice_count, "repeats", "", ""),
        "derived__exact_arc_pitch": (resolved.arc_pitch, "mm", "approximately ", ""),
        "derived__female_minimum_wall": (resolved.female_minimum_wall, "mm", "", ""),
        "derived__overall_minimum_wall": (resolved.minimum_wall, "mm", "", ""),
        "derived__drain_hole_count_each_end": (len(resolved.drain_centers), "holes", "", ""),
        "derived__print_bounds_separation": (resolved.print_bounds_separation, "mm", "", ""),
    }
    value, unit, prefix, suffix = values[identifier]
    return f"{prefix}{_number(value)} {unit}{suffix} - derived readout"


DERIVED_IDS = (
    "derived__cavity_length", "derived__outer_length", "derived__body_cavity_depth",
    "derived__body_height", "derived__cap_height", "derived__thread_turns",
    "derived__body_radial_gap", "derived__cap_radial_gap", "derived__lattice_count",
    "derived__exact_arc_pitch", "derived__female_minimum_wall",
    "derived__overall_minimum_wall", "derived__drain_hole_count_each_end",
    "derived__print_bounds_separation",
)


def readout_rows():
    """Return ordered readout rows generated from the one source registry."""
    parameters = preset()
    resolved = resolve_parameters(parameters)
    specs = tuple(PARAMETER_SPECS)
    expected_ids = {field.name for field in fields(Parameters)}
    if len(specs) != len(expected_ids) or {spec["id"] for spec in specs} != expected_ids:
        raise ValueError("PARAMETER_SPECS must contain every parameter exactly once")
    if len({spec["id"] for spec in specs}) != len(specs):
        raise ValueError("PARAMETER_SPECS contains duplicate ids")
    rows = [(NOTICE_ID, _row("00 READ ONLY", NOTICE_VALUE))]
    for order, (visible_group, registry_group) in enumerate(GROUPS, start=1):
        for spec in (row for row in specs if row["group"] == registry_group):
            if spec["classification"] not in CLASSIFICATIONS:
                raise ValueError(f"unsupported classification: {spec['classification']}")
            value = getattr(parameters, spec["id"])
            if value != spec["default"]:
                raise ValueError(f"registry default drift: {spec['id']}")
            shown = f"{_source_value(value, spec['unit'])} - {CLASSIFICATIONS[spec['classification']]}"
            rows.append((spec["id"], _row(
                f"{order:02d} {visible_group} - {_humanize(spec['id'])}", shown)))
    if len(rows) != 27:
        raise ValueError("expected 26 registry rows plus read-only notice")
    for identifier in DERIVED_IDS:
        rows.append((identifier, _row(
            f"09 Derived - {_humanize(identifier.removeprefix('derived__'))}",
            _derived_value(resolved, identifier))))
    if len(rows) != 41 or len({identifier for identifier, _ in rows}) != len(rows):
        raise ValueError("preview row count or ids are invalid")
    return tuple(rows)


def visual_rows():
    """Return the bounded Viewer-time controls in their frozen display order."""
    rows = [(VISUAL_NOTICE_ID, {
        "type": "enum",
        "label": "00 VISUAL PREVIEW ONLY",
        "description": VISUAL_NOTICE_VALUE,
        "options": [{"value": VISUAL_NOTICE_VALUE, "label": VISUAL_NOTICE_VALUE}],
        "default": VISUAL_NOTICE_VALUE,
        "renderOnly": True,
        "geometryRegeneration": False,
    })]
    rows.extend((identifier, _visual_row(
        identifier, label, row_type, default, minimum, maximum, step, unit))
        for identifier, label, row_type, default, minimum, maximum, step, unit in VISUAL_CONTROLS)
    return tuple(rows)


def manifest():
    return {
        "schemaVersion": 1,
        "step": {"path": "cad/container_generator_v1/closed.step"},
        "features": {
            "body": {"label": "Body display mesh", "names": [BODY_OCCURRENCE_NAME], "axis": [0, 0, 1], "origin": [0, 0, 0]},
            "cap": {"label": "Cap display mesh", "names": [CAP_OCCURRENCE_NAME], "axis": [0, 0, 1], "origin": [0, 0, 0]},
        },
        "parameters": dict((*visual_rows(), *readout_rows())),
    }


def serialize():
    """Return deterministic, standalone ES module bytes as text."""
    schema = json.dumps({
        "mode": "read_only_parameter_snapshot",
        "source": "PARAMETER_SPECS + derive(preset())",
        "geometryRegeneration": False,
    }, indent=2, sort_keys=True)
    rendered_manifest = json.dumps(manifest(), indent=2, ensure_ascii=False)
    return (
        "// Generated by preview_parameters.py; do not edit by hand.\n"
        f"export const READOUT_SCHEMA = Object.freeze({schema});\n\n"
        "export function solveVisualPreview(rawParams = {}) {\n"
        "  const finite = (value, fallback) => Number.isFinite(Number(value)) ? Number(value) : fallback;\n"
        "  const clamp = (value, low, high, fallback) => Math.min(Math.max(finite(value, fallback), low), high);\n"
        "  const r = clamp(rawParams.visual_radial_scale_pct, 60, 160, 100) / 100;\n"
        "  const az = clamp(rawParams.visual_axial_scale_pct, 60, 160, 100) / 100;\n"
        "  const bz = az * clamp(rawParams.visual_body_axial_scale_pct, 60, 160, 100) / 100;\n"
        "  const cz = az * clamp(rawParams.visual_cap_axial_scale_pct, 60, 160, 100) / 100;\n"
        "  const turns = clamp(rawParams.visual_cap_unscrew_turns, 0, 3, 0);\n"
        "  const extraLift = clamp(rawParams.visual_cap_extra_lift_mm, 0, 60, 0);\n"
        "  const bodyColor = /^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i.test(String(rawParams.visual_body_color || '')) ? String(rawParams.visual_body_color) : '" + BODY_COLOR + "';\n"
        "  const capColor = /^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i.test(String(rawParams.visual_cap_color || '')) ? String(rawParams.visual_cap_color) : '" + CAP_COLOR + "';\n"
        "  const bodyOpacity = clamp(rawParams.visual_body_opacity, 0.10, 1, 1);\n"
        "  const capOpacity = clamp(rawParams.visual_cap_opacity, 0.10, 1, 1);\n"
        "  return { r, az, bz, cz, turns, extraLift, theta_deg: 360 * turns, cap_z_mm: 2 * turns + extraLift, bodyColor, capColor, bodyOpacity, capOpacity };\n"
        "}\n\n"
        "const identityScale = (scale) => scale.every((value) => Math.abs(value - 1) <= 1e-9);\n"
        "const scaleSpec = (scale) => ({ transforms: [{ scale, origin: [0, 0, 0] }] });\n"
        "const capSpec = (solved) => ({ transforms: [\n"
        "  { scale: [solved.r, solved.r, solved.cz], origin: [0, 0, 0] },\n"
        "  { rotate: { axis: [0, 0, 1], angleDeg: solved.theta_deg, origin: [0, 0, 0] } },\n"
        "  { translate: [0, 0, solved.cap_z_mm] }\n"
        "] });\n\n"
        "const definition = {\n"
        f"  manifest: {rendered_manifest},\n"
        "  update({ params = {}, effects = {} } = {}) {\n"
        "    const solved = solveVisualPreview(params);\n"
        "    if (!identityScale([solved.r, solved.r, solved.bz])) effects.transform('body', scaleSpec([solved.r, solved.r, solved.bz]));\n"
        "    if (!identityScale([solved.r, solved.r, solved.cz]) || solved.theta_deg !== 0 || solved.cap_z_mm !== 0) effects.transform('cap', capSpec(solved));\n"
        "    if (solved.bodyColor.toLowerCase() !== '" + BODY_COLOR + "' || solved.bodyOpacity !== 1) effects.style('body', { color: solved.bodyColor, opacity: solved.bodyOpacity, edgeOpacity: solved.bodyOpacity });\n"
        "    if (solved.capColor.toLowerCase() !== '" + CAP_COLOR + "' || solved.capOpacity !== 1) effects.style('cap', { color: solved.capColor, opacity: solved.capOpacity, edgeOpacity: solved.capOpacity });\n"
        "  }\n"
        "};\n\n"
        "export default definition;\n"
    )


def write_sidecar(path=None):
    target = Path(path) if path else Path(__file__).with_name("closed.params.js")
    target.write_text(serialize(), encoding="utf-8")
    return target


if __name__ == "__main__":
    write_sidecar()
