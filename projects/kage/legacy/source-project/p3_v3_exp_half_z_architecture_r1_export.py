"""Export the complete KAGE half-Z communication assemblies."""

from __future__ import annotations

import json
from pathlib import Path

from build123d import Compound, Solid, export_step

from p3_v3_exp_half_z_architecture_r1_geometry import (
    _bounds,
    envelope_z,
    locked_step_sha256,
    make_D_complete,
    make_D_exploded,
    make_D_led_keepout_reference,
    make_D_true_side_section,
    make_E_complete,
    make_E_true_side_section,
    make_side_by_side,
)
from p3_v3_exp_half_z_architecture_r1_spec import P3_V3_EXP_HALF_Z_ARCHITECTURE_R1 as P


ARTIFACT_BUILDERS = {
    "D_compact_split_plane_complete.step": make_D_complete,
    "D_true_side_section.step": make_D_true_side_section,
    "D_true_exploded_installation_order.step": make_D_exploded,
    "D_LED_keepout_reference_not_hardware.step": make_D_led_keepout_reference,
    "E_REJECTED_coplanar_radial_lanes_comparison.step": make_E_complete,
    "E_REJECTED_true_side_section_comparison.step": make_E_true_side_section,
    "p3_v3_exp_half_z_architecture_r1_side_by_side.step": make_side_by_side,
}


def _flatten(shape, label: str) -> Compound:
    rows = []
    for index, source_solid in enumerate(shape.solids(), start=1):
        child = Solid(source_solid.wrapped)
        child.label = f"{label}_presentation_solid_{index:03d}"
        child.color = source_solid.color
        rows.append(child)
    return Compound(children=rows, label=f"{label}_flat_written_STEP")


def export_all(output_dir: Path | None = None) -> dict[str, Path]:
    root = output_dir or P.model_root
    root.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    manifest = {
        "status": "communication_geometry_not_print_ready",
        "namespace": P.artifact_slug,
        "locked_source": str(P.locked_step),
        "locked_sha256": locked_step_sha256(),
        "locked_files_modified": False,
        "led_module_included": False,
        "architectures": {
            "D": {
                "claim": "repaired_complete_clock_compact_split_plane_locked_transmission",
                "status": "CAD_COMMUNICATION_CANDIDATE_NOT_PRINT_READY",
                "miter_geometry": "real_16T_straight_miter_teeth_reused_from_locked_transmission_source",
                "motor_shaft_plane_source": "derived_from_actual_motor_envelope_center",
                "guide_contact": "D4p2_bored_relief_spools_on_D4_posts_and_tooth_free_lower_carrier_race",
                "guide_retention": "D6_rear_collar_seated_in_D6p2_chassis_counterbore_plus_removable_keeper_cap",
                "motor_retention": "serviceable_U_cradle_4xM2_face_2xM3_chassis_per_station",
                "ring_teeth": list(P.d_ring_teeth_by_role),
                "pinion_teeth": P.pinion_teeth,
                "pitch_radii": list(P.d_pitch_radii),
                "pinion_axes": list(P.d_pinion_axes),
                "carrier_layers": [list(v) for v in P.d_carrier_layers],
                "fin_tip_zs": list(P.d_fin_tip_zs),
                "expected_z_envelope": P.d_expected_z_envelope,
                "led_source_to_mask": P.d_led_source_to_mask,
                "optical_led_clearance_risk_mm": P.d_optical_clearance_risk,
                "optical_status": "RISK_REQUIRES_PHYSICAL_LIGHT_CONE_TEST",
            },
            "E": {
                "claim": "rejected_comparison_only_not_a_complete_drive",
                "status": "REJECTED_COMPARISON_LAYOUT_ONLY",
                "miter_geometry": "smooth_reference_cones_not_functional_teeth",
                "ring_teeth": list(P.e_ring_teeth),
                "pinion_teeth": P.pinion_teeth,
                "pitch_radii": list(P.e_pitch_radii),
                "pinion_axes": list(P.e_pinion_axis_radii),
                "radial_envelopes": [list(v) for v in P.e_radial_envelopes],
                "fin_tip_zs": list(P.e_fin_tip_zs),
                "expected_z_envelope": P.e_expected_z_envelope,
                "led_source_to_mask": P.e_led_source_to_mask,
                "optical_led_clearance_risk_mm": P.e_optical_clearance_risk,
                "optical_status": "HIGHER_RISK_REQUIRES_PHYSICAL_LIGHT_CONE_TEST",
            },
        },
        "artifacts": {},
    }
    for filename, builder in ARTIFACT_BUILDERS.items():
        shape = builder()
        path = root / filename
        export_step(_flatten(shape, Path(filename).stem), str(path))
        written[filename] = path
        manifest["artifacts"][filename] = {
            "scope": (
                "primary_complete_candidate"
                if filename == "D_compact_split_plane_complete.step"
                else "true_exploded_installation_order"
                if "exploded" in filename
                else "optical_keepout_reference_not_hardware"
                if "keepout" in filename
                else "rejected_comparison"
                if filename.startswith("E_REJECTED")
                else "side_by_side_comparison"
                if "side_by_side" in filename
                else "true_side_section"
            ),
            "solids": len(shape.solids()),
            "bounds": [round(v, 6) for v in _bounds(shape)],
            "z_envelope": [round(v, 6) for v in envelope_z(shape)],
        }
    side = make_side_by_side()
    d_box = _bounds(side.children[0])
    e_box = _bounds(side.children[1])
    manifest["comparison_layout"] = {
        "D_to_E_gap_x": round(e_box[0] - d_box[3], 6),
        "non_overlapping": e_box[0] > d_box[3],
    }
    manifest["LED_keepout"] = {
        "included_in_primary_physical_envelope": False,
        "LED_module_included": False,
        "reference_artifact": "D_LED_keepout_reference_not_hardware.step",
        "center_remains_open": True,
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    written[manifest_path.name] = manifest_path
    return written


if __name__ == "__main__":
    for name, path in export_all().items():
        print(f"{name}: {path}")
