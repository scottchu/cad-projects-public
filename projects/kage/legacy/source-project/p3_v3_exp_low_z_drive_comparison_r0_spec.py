"""Frozen dimensions for the KAGE low-Z communication study.

This experiment is derived from the locked direct-gear-race STEP.  It is not a
print release: it compares packaging changes without changing the three ring
gears, their fins, or the 16-tooth output pinions.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class P3V3LowZComparisonSpec:
    artifact_slug: str = "p3_v3_exp_low_z_drive_comparison_r0"
    locked_relative_dir: str = (
        "models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
    )
    locked_step_name: str = "p3_v3_direct_gear_race_assembled.step"
    locked_sha256: str = (
        "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"
    )

    # Measured from the immutable STEP, including the tallest second fin.
    locked_z_min: float = -32.50
    locked_z_max: float = 24.2514
    locked_z_height: float = 56.7514

    # Concept B removes only protruding rear/upper fastener hardware and uses
    # blind/captive axles.  The accepted rear chassis itself stays at -28 mm.
    flush_hardware_z_min: float = -28.00
    flush_hardware_max_height: float = 52.30

    # Concept C is deliberately a role-local packaging coupon.  It is not a
    # complete clock and therefore has no honest complete-clock Z claim.
    local_station_complete_clock: bool = False
    local_station_chassis_thickness: float = 2.50

    ring_outer_radius: float = 150.00
    local_station_chassis_inner_radius: float = 62.00
    captive_axle_diameter: float = 4.00
    flush_fastener_head_diameter: float = 5.50
    flush_fastener_head_height: float = 1.80
    flush_fastener_clearance_diameter: float = 3.40
    flush_fastener_pocket_diameter: float = 6.00
    flush_fastener_pocket_depth: float = 2.00
    flush_fastener_washer_diameter: float = 7.00
    flush_fastener_washer_height: float = 0.50
    flush_fastener_nut_af: float = 5.50
    flush_fastener_nut_height: float = 2.40
    shaft_retainer_diameter: float = 7.00
    shaft_retainer_height: float = 0.60
    roller_retainer_diameter: float = 7.00
    roller_retainer_height: float = 0.40
    coupon_spacing_x: float = 320.00
    comparison_min_gap_x: float = 40.00

    @property
    def locked_step(self) -> Path:
        return ROOT / self.locked_relative_dir / self.locked_step_name

    @property
    def model_root(self) -> Path:
        return ROOT / "models" / self.artifact_slug


P3_V3_EXP_LOW_Z_DRIVE_COMPARISON_R0 = P3V3LowZComparisonSpec()
