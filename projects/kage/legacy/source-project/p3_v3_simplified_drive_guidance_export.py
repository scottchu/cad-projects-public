"""Export entry points for the simplified P3 V3 assembly artifacts."""

from __future__ import annotations

from pathlib import Path

from build123d import export_step

from p3_v3_simplified_drive_guidance_geometry import make_assembled, make_service_exploded


MODEL_DIR = Path(__file__).resolve().parent / "models" / "p3_v3_simplified_drive_guidance"


def export_all(model_dir: Path = MODEL_DIR) -> tuple[Path, Path]:
    model_dir.mkdir(parents=True, exist_ok=True)
    assembled = model_dir / "p3_v3_simplified_assembled.step"
    exploded = model_dir / "p3_v3_simplified_service_exploded.step"
    export_step(make_assembled(), assembled)
    export_step(make_service_exploded(), exploded)
    return assembled, exploded


if __name__ == "__main__":
    for path in export_all():
        print(path)
