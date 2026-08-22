"""Export KAGE P3 V2 three-ring comparison STEP assemblies."""

from __future__ import annotations

from pathlib import Path

from build123d import export_step

from p3_v2_three_ring_comparison_geometry import THREE_RING_FACTORIES


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v2_three_ring_comparison"


def generate_artifacts() -> None:
    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    for name, factory in THREE_RING_FACTORIES:
        export_step(factory(), MODEL_ROOT / f"p3_v2_{name}.step")


if __name__ == "__main__":
    generate_artifacts()
