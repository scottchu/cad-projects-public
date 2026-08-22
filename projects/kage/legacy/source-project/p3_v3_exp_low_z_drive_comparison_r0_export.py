"""Export entrypoint for the KAGE low-Z communication study."""

from __future__ import annotations

import json
from pathlib import Path

from build123d import Compound, Solid, export_step

from p3_v3_exp_low_z_drive_comparison_r0_geometry import (
    _bounds,
    envelope_z,
    locked_step_sha256,
    make_flush_hardware_B,
    make_locked_reference_A,
    make_short_bevel_C,
    make_side_by_side_comparison,
)
from p3_v3_exp_low_z_drive_comparison_r0_spec import (
    P3_V3_EXP_LOW_Z_DRIVE_COMPARISON_R0 as P,
)


ARTIFACT_BUILDERS = {
    "A_locked_z_budget_section.step": make_locked_reference_A,
    "B_flush_hardware_captive_axle.step": make_flush_hardware_B,
    "C_role_local_short_bevel_station.step": make_short_bevel_C,
    "p3_v3_exp_low_z_drive_comparison_r0_side_by_side.step": make_side_by_side_comparison,
}


def _flatten_for_written_step(shape, label_prefix: str) -> Compound:
    """Bake nested placements into leaf solids for deterministic STEP review.

    The CAD viewer's imported-assembly renderer can ignore a transform on a
    nested compound.  C and the ABC sheet intentionally use nested placement,
    so write a geometrically identical flat presentation compound instead.
    """

    children = []
    for index, source_solid in enumerate(shape.solids(), start=1):
        child = Solid(source_solid.wrapped)
        child.label = f"{label_prefix}_presentation_solid_{index:03d}"
        child.color = source_solid.color
        children.append(child)
    return Compound(children=children, label=f"{label_prefix}_flattened_written_STEP")


def export_all(output_dir: Path | None = None) -> dict[str, Path]:
    root = output_dir or P.model_root
    root.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    manifest = {
        "status": "communication_geometry_not_print_ready",
        "locked_step": str(P.locked_step),
        "locked_sha256": locked_step_sha256(),
        "preserved": ["three exact 260T ring/fins", "three exact 16T output pinions"],
        "concepts": {},
    }
    for filename, builder in ARTIFACT_BUILDERS.items():
        shape = builder()
        path = root / filename
        # A is the accepted communication baseline.  Keep the existing bytes
        # immutable in the canonical model directory; temporary/export-test
        # destinations may still materialize their own copy.
        preserve_existing_a = (
            filename.startswith("A_")
            and root.resolve() == P.model_root.resolve()
            and path.exists()
        )
        if not preserve_existing_a:
            export_shape = shape
            if filename.startswith("C_") or filename.endswith("side_by_side.step"):
                export_shape = _flatten_for_written_step(shape, Path(filename).stem)
            export_step(export_shape, str(path))
        written[filename] = path
        manifest["concepts"][filename] = {
            "z_envelope": [round(v, 6) for v in envelope_z(shape)],
            "solids": len(shape.solids()),
        }
        if filename.startswith("A_"):
            manifest["concepts"][filename]["immutable_existing_artifact"] = preserve_existing_a
        if filename.startswith("C_"):
            manifest["concepts"][filename].update(
                {
                    "complete_clock": False,
                    "scope": "three_role_local_coupon",
                    "claim": "packaging_potential_only_full_clock_integration_unproven",
                }
            )
        if filename.endswith("side_by_side.step"):
            children = shape.children
            a_bounds = _bounds(children[0])
            b_bounds = _bounds(children[1])
            c_bounds = _bounds(children[2])
            manifest["comparison_layout"] = {
                "minimum_requested_gap_x": P.comparison_min_gap_x,
                "measured_A_to_B_gap_x": round(b_bounds[0] - a_bounds[3], 6),
                "measured_B_to_C_gap_x": round(c_bounds[0] - b_bounds[3], 6),
            }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    written[manifest_path.name] = manifest_path
    return written


if __name__ == "__main__":
    for name, path in export_all().items():
        print(f"{name}: {path}")
