"""Evidence-only B4-R2 adversarial fin-clearance contract."""

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_rings_b4_r2_adversarial_fin_clearance"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class EvidenceParameters:
    accepted_b4_r1_tree_hash: str = (
        "fdc8f459730747bff59b036f1e8614afea717d720d07d0e5012f06c536cc5f03"
    )
    # Independent aligned-pose measurements.  Each moving fin passes one
    # assigned stationary roller and its own role pinion during a revolution.
    roller_fin_pose_deg: tuple[float, ...] = (60.0, 180.0, 300.0)
    pinion_fin_pose_deg: tuple[float, ...] = (0.0, 120.0, 240.0)
    roller_distance_mm: tuple[float, float] = (2.999999, 3.000001)
    exact_pinion_distance_min_mm: float = 5.0
    brep_tolerance_mm3: float = 1e-6


SPEC = EvidenceParameters()
