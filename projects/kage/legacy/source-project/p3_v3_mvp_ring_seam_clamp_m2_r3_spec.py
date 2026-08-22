"""Full-radial-coverage contract for KAGE's stack-safe M2 seam clamp."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from p3_v3_mvp_ring_seam_clamp_m2_r2_spec import (
    LOCKED_ROOT,
    LOCKED_STEP,
    LOCKED_STEP_SHA256,
    PARITY_JSON,
    ROOT,
    RingSeamClampM2R2Spec,
)


NAMESPACE = "p3_v3_mvp_ring_seam_clamp_m2_r3"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class RingSeamClampM2R3Spec(RingSeamClampM2R2Spec):
    """Extend only the removable flanges; preserve the accepted r2 stack and hardware."""

    tooth_tip_radius_mm: float = 129.00
    tooth_root_radius_mm: float = 132.50

    # r2 began at R134.60 and covered only 4.30 / 6.40 mm of solid ring body.
    r2_clamp_inner_radius_mm: float = 134.60
    clamp_inner_radius_mm: float = 132.50

    @property
    def solid_ring_body_radial_width_mm(self) -> float:
        return self.carrier_outer_radius_mm - self.tooth_root_radius_mm

    @property
    def r2_ring_body_coverage_mm(self) -> float:
        return self.carrier_outer_radius_mm - self.r2_clamp_inner_radius_mm

    @property
    def full_ring_body_coverage_mm(self) -> float:
        return self.carrier_outer_radius_mm - self.clamp_inner_radius_mm

    @property
    def r2_ring_body_coverage_fraction(self) -> float:
        return self.r2_ring_body_coverage_mm / self.solid_ring_body_radial_width_mm

    @property
    def full_ring_body_coverage_fraction(self) -> float:
        return self.full_ring_body_coverage_mm / self.solid_ring_body_radial_width_mm

    @property
    def clamp_inner_radial_screw_edge_distance_mm(self) -> float:
        return self.screw_axis_radius_mm - self.screw_clearance_diameter_mm / 2.0 - self.clamp_inner_radius_mm

    @property
    def clamp_outer_radial_screw_edge_distance_mm(self) -> float:
        return self.clamp_outer_radius_mm - self.screw_axis_radius_mm - self.screw_clearance_diameter_mm / 2.0

    @property
    def tooth_profile_exposed_radial_width_mm(self) -> float:
        return self.tooth_root_radius_mm - self.tooth_tip_radius_mm

    def validate(self) -> None:
        super().validate()
        assert isclose(self.r2_ring_body_coverage_mm, 4.30, abs_tol=1e-12)
        assert isclose(self.solid_ring_body_radial_width_mm, 6.40, abs_tol=1e-12)
        assert isclose(self.full_ring_body_coverage_mm, 6.40, abs_tol=1e-12)
        assert self.r2_ring_body_coverage_fraction < 0.68
        assert isclose(self.full_ring_body_coverage_fraction, 1.0, abs_tol=1e-12)
        assert self.clamp_inner_radius_mm == self.tooth_root_radius_mm
        assert self.tooth_profile_exposed_radial_width_mm == 3.50
        assert self.clamp_inner_radial_screw_edge_distance_mm >= self.minimum_hole_edge_ligament_mm
        assert self.clamp_outer_radial_screw_edge_distance_mm >= self.minimum_hole_edge_ligament_mm


SPEC = RingSeamClampM2R3Spec()
