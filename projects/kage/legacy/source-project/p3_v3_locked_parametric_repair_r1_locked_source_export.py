"""Export entry points for the isolated P3 V3 direct gear-race artifacts."""

from __future__ import annotations

from pathlib import Path

from build123d import export_step

from p3_v3_direct_gear_race_guidance_geometry import (
    make_assembled,
    make_powered_max,
    make_powered_min,
    make_service_disengaged,
    make_service_exploded,
    make_service_outward_rings_removed,
)


MODEL_DIR = Path(__file__).resolve().parent / "models" / "p3_v3_direct_gear_race_guidance"


def export_all(model_dir: Path = MODEL_DIR) -> tuple[Path, ...]:
    model_dir.mkdir(parents=True, exist_ok=True)
    assembled = model_dir / "p3_v3_direct_gear_race_assembled.step"
    exploded = model_dir / "p3_v3_direct_gear_race_service_exploded.step"
    powered_min = model_dir / "p3_v3_direct_gear_race_powered_min_q-0p35.step"
    powered_max = model_dir / "p3_v3_direct_gear_race_powered_max_q+0p10.step"
    disengaged = model_dir / "p3_v3_direct_gear_race_SERVICE_disengaged_q-2p50.step"
    outward = model_dir / "p3_v3_direct_gear_race_SERVICE_outward_q+2p50_RINGS_REMOVED.step"
    export_step(make_assembled(), assembled)
    export_step(make_service_exploded(), exploded)
    export_step(make_powered_min(), powered_min)
    export_step(make_powered_max(), powered_max)
    export_step(make_service_disengaged(), disengaged)
    export_step(make_service_outward_rings_removed(), outward)
    return assembled, exploded, powered_min, powered_max, disengaged, outward


if __name__ == "__main__":
    for path in export_all():
        print(path)
