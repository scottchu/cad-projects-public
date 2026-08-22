"""Export the isolated KAGE P3 V3 motor-station assembly sequence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build123d import export_step

from p3_v3_motor_station_assembly_sim_geometry import (
    MODEL_ROOT,
    make_chassis_patch,
    make_final_station,
    make_gearbox_frame,
    make_stage_1_motor_mount,
    make_stage_2_gearbox_mount,
    make_stage_3_shaft_stack,
    make_stage_4_height_lock,
    make_stage_5_reverse_service,
)


def export_all(output_dir: Path = MODEL_ROOT) -> tuple[Path, ...]:
    output_dir.mkdir(parents=True, exist_ok=True)
    role = 2
    factories = {
        "p3_v3_motor_station_stage1_motor_mount.step": lambda: make_stage_1_motor_mount(role),
        "p3_v3_motor_station_stage2_gearbox_mount.step": lambda: make_stage_2_gearbox_mount(role),
        "p3_v3_motor_station_stage3_shaft_stack.step": lambda: make_stage_3_shaft_stack(role),
        "p3_v3_motor_station_stage4_final_height_lock.step": lambda: make_stage_4_height_lock(role),
        "p3_v3_motor_station_stage5_reverse_service.step": lambda: make_stage_5_reverse_service(role),
        "p3_v3_motor_station_open_yoke.step": lambda: make_gearbox_frame(role),
        "p3_v3_motor_station_chassis_patch.step": make_chassis_patch,
    }
    paths = []
    for name, factory in factories.items():
        path = output_dir / name
        export_step(factory(), path)
        paths.append(path)
    source_paths = (
        Path(__file__).resolve(),
        Path(__file__).with_name("p3_v3_motor_station_assembly_sim_spec.py"),
        Path(__file__).with_name("p3_v3_motor_station_assembly_sim_geometry.py"),
    )
    manifest = {
        "revision": "D-shaft-retained-static-stages-r2",
        "stage_labels": {name: factory().label for name, factory in factories.items()},
        "source_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths
        },
        "artifact_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths
        },
    }
    (output_dir / "p3_v3_motor_station_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return tuple(paths)


if __name__ == "__main__":
    for exported in export_all():
        print(exported)
