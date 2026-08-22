"""Zero-delta assembly adapter around the byte-copied locked source."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any

from p3_v3_locked_parametric_repair_r1_locked_source_geometry import make_assembled
from p3_v3_locked_parametric_repair_r1_spec import P3V3LockedParametricRepairR1


ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / "models" / "p3_v3_locked_parametric_repair_r1"
LOCKED_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
LOCKED_INPUTS = (
    LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step.py",
    LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step",
    LOCKED_ROOT / "source_snapshot" / "p3_v3_direct_gear_race_guidance_geometry.py",
    LOCKED_ROOT / "source_snapshot" / "p3_v3_direct_gear_race_guidance_spec.py",
    LOCKED_ROOT / "source_snapshot" / "p3_v3_direct_gear_race_guidance_export.py",
)


def _hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_candidate(params: P3V3LockedParametricRepairR1) -> dict[str, Any]:
    """Build only the new namespace while preserving the locked default BREP."""

    params.validate()
    shape = make_assembled(radial_adjustments=params.service_states.motor_adjustments_mm)
    return {
        "shape": shape,
        "model_root": MODEL_ROOT,
        "source_locked_hashes": {
            str(path.relative_to(ROOT)): _hash(path)
            for path in LOCKED_INPUTS
        },
    }


def flatten_occurrences(shape_or_registry) -> tuple[Any, ...]:
    """Return the 201 locked top-level leaf occurrences in stable order."""

    if isinstance(shape_or_registry, dict):
        shape_or_registry = shape_or_registry["shape"]
    children = tuple(getattr(shape_or_registry, "children", ()) or ())
    return children if children else (shape_or_registry,)
