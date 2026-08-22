"""Generate isolated P3 V3 transmission R1 STEP artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import trimesh
from build123d import export_step, export_stl

from p3_v3_transmission_r1_geometry import (
    INDIVIDUAL_PRINT_FACTORIES,
    PRIMARY_FACTORIES,
)


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_transmission_r1"
PRINT_ROOT = MODEL_ROOT / "print"
PART_ROOT = PRINT_ROOT / "parts"


def export_clean_stl(part, destination: Path) -> None:
    """Tessellate one CAD solid and discard numerical zero-volume slivers."""

    raw = destination.with_name(f".{destination.stem}.raw.stl")
    export_stl(part, raw)
    loaded = trimesh.load_mesh(raw, process=True, force="mesh")
    components = [
        component
        for component in loaded.split(only_watertight=False)
        if component.area > 1e-8 and len(component.faces) >= 4
    ]
    if not components:
        raise ValueError(f"STL tessellation produced no physical mesh: {destination.name}")
    mesh = max(components, key=lambda component: (abs(component.volume), component.area))
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.remove_unreferenced_vertices()
    mesh.process(validate=True)
    if mesh.volume < 0.0:
        mesh.invert()
    if not mesh.is_watertight or mesh.volume <= 0.0:
        raise ValueError(f"clean STL is not one watertight positive solid: {destination.name}")
    mesh.export(destination)
    raw.unlink(missing_ok=True)


def generate_artifacts() -> None:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    PRINT_ROOT.mkdir(parents=True, exist_ok=True)
    PART_ROOT.mkdir(parents=True, exist_ok=True)
    for name, factory in PRIMARY_FACTORIES:
        export_step(factory(), MODEL_ROOT / f"p3_v3_r1_{name}.step")
    individual_paths = []
    for name, factory in INDIVIDUAL_PRINT_FACTORIES:
        part = factory()
        step_path = PART_ROOT / f"p3_v3_r1_{name}.step"
        stl_path = PART_ROOT / f"p3_v3_r1_{name}.stl"
        export_step(part, step_path)
        export_clean_stl(part, stl_path)
        individual_paths.extend(
            (str(step_path.relative_to(MODEL_ROOT)), str(stl_path.relative_to(MODEL_ROOT)))
        )
    manifest = {
        "title": "KAGE P3 V3 transmission R1 one-station coupon",
        "status": "CAD validated; physical gear, noise, runout, and endurance gates pending",
        "selected_role": "minute",
        "purchased_references": {
            "motor": "NEMA8 20.3 mm face, 4 x 7 mm D shaft, 3.5 mm across-flat",
            "bearings": "2 x MR84ZZ 4 x 8 x 3 mm",
            "shaft": "4 x 40 mm D steel shaft, 3.5 mm across-flat",
            "grub_screws": "3 x M2",
            "bearing_retainer_screws": "4 x M2",
            "slider_retainer_screws": "2 x M2",
            "saddle_clamps": "4 x M3 bolts + 8 washers + 4 external 5.5 mm AF nuts",
        },
        "transmission": {
            "miter": "M1 16T:16T straight bevel pair",
            "output": "M1 16T pinion to M1 259T internal ring arc",
            "output_axis_radius_mm": 121.5,
            "motor_radial_adjustment_mm": 0.5,
            "motor_bore": "4.10 mm D bore, 3.60 mm across-flat",
            "output_bores": "4.10 mm D bore, 3.60 mm across-flat",
            "m2_tap_pilot_mm": 1.6,
            "axial_retention": "lower clamp collar + thrust sleeve + upper miter hub",
            "ring_arc_fixture": "captured tangential backlash/contact slider; +/-0.08 mm only",
            "bearing_retention": "two removable outer-race-only retainers; 3.10 mm clear opening",
            "guide_load_path": "lower guide fused to chassis by two full-height pylons",
            "saddle_clamp_stack": "lower washer contacts chassis; upper washer contacts saddle; 2.40 mm nut engagement",
        },
        "print_artifact_kind": "functional-position catalog; not a slicer plate",
        "individual_print_files": individual_paths,
        "assembly_order": [
            "press lower MR84ZZ into lower chassis pocket; fit its outer-race retainer with two M2 screws",
            "slide the lower D clamp collar onto the 4 x 40 mm output D-shaft",
            "insert the output shaft upward through the lower bearing",
            "install the printed lower thrust sleeve above the lower bearing",
            "slide vertical 16T miter gear onto shaft and tighten its M2 grub screw",
            "insert upper MR84ZZ into upper pocket, pass shaft through it, and fit its outer-race retainer with two M2 screws",
            "draw the shaft upward and tighten the lower collar M2 screw to retain the lower stack",
            "fit role spacer and 16T output pinion; tighten its M2 screw at 0.05-0.15 mm axial endplay",
            "seat the horizontal miter gear on the motor D shaft; its D bore is the positive drive",
            "bolt horizontal NEMA8 to saddle and slide saddle until the miter pair meshes",
            "install four M3 bolts from below with washers and external nuts outside the motor footprint",
            "install the captured arc carriage on the chassis-fused lower guide/stops",
            "fit the removable upper arc retainer with its two M2 screws",
            "tighten the four M3 saddle clamps, then verify ring-arc backlash by hand",
        ],
        "physical_gates": {
            "manual_free_rotation": "PENDING",
            "100_forward_reverse_cycles": "PENDING",
            "24_hour_seconds_speed_run": "PENDING",
            "noise_at_one_meter": "PENDING",
            "printed_axial_runout_le_0p2_mm": "PENDING",
        },
    }
    (MODEL_ROOT / "p3_v3_r1_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )


if __name__ == "__main__":
    generate_artifacts()
