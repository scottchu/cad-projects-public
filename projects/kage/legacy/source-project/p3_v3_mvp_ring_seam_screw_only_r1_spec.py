"""Numeric contract for the isolated locked-ring screw-only seam coupon."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_ring_seam_screw_only_r1"
MODEL_ROOT = ROOT / "models" / NAMESPACE
LOCKED_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
LOCKED_STEP = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step"
PARITY_JSON = ROOT / "models" / "p3_v3_locked_parametric_repair_r1" / "p3_v3_locked_parametric_repair_r1_zero_delta_parity.json"
LOCKED_STEP_SHA256 = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"


@dataclass(frozen=True)
class RingSeamScrewOnlyR1Spec:
    roles: tuple[str, str, str] = ("hour", "minute", "second")
    carrier_layers: tuple[tuple[float, float], ...] = ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    quadrant_occurrence_indices: tuple[tuple[int, int], ...] = ((108, 109), (139, 140), (170, 171))
    seam_angle_deg: float = 90.0
    ring_teeth: int = 260
    tooth_phase_deg: float = 360.0 / 520.0
    tooth_root_radius_mm: float = 132.50
    carrier_race_radius_mm: float = 131.60
    carrier_outer_radius_mm: float = 138.90

    capture_inner_radius_mm: float = 145.00
    required_capture_clearance_mm: float = 0.20
    pad_inner_radius_mm: float = 138.70
    pad_outer_radius_mm: float = 144.75
    pad_tangential_width_mm: float = 30.0
    pad_thickness_mm: float = 1.20

    screw_count_per_seam: int = 2
    screw_nominal_diameter_mm: float = 3.00
    screw_clearance_diameter_mm: float = 3.40
    screw_length_mm: float = 8.00
    socket_head_diameter_mm: float = 5.50
    socket_head_height_mm: float = 3.00
    hardware_axis_global_radius_mm: float = 141.85
    role_tangential_offsets_mm: tuple[tuple[float, float], ...] = ((-12.0, 4.0), (-4.0, 12.0), (-12.0, 4.0))

    nut_across_flats_mm: float = 5.50
    nut_thickness_mm: float = 2.40
    nut_trap_across_flats_mm: float = 5.60
    nut_trap_depth_mm: float = 2.50
    nut_trap_roof_mm: float = 0.50
    nut_axial_play_mm: float = 0.10
    receiver_boss_radius_mm: float = 3.20

    shoulder_radial_mm: float = 5.00
    shoulder_tangential_mm: float = 6.00
    shoulder_height_mm: float = 0.80
    pocket_radial_mm: float = 5.25
    pocket_tangential_mm: float = 6.25
    pocket_depth_mm: float = 0.90
    registration_radius_mm: float = 136.00
    registration_tangential_offsets_mm: tuple[float, float] = (-8.0, 8.0)

    seam_local_envelope_inner_radius_mm: float = 133.20
    seam_local_envelope_outer_radius_mm: float = 144.90
    seam_local_envelope_tangential_width_mm: float = 32.0
    printer_bed_mm: tuple[float, float, float] = (270.0, 270.0, 270.0)
    bed_margin_mm: float = 5.0
    minimum_layout_gap_mm: float = 3.0

    @property
    def pad_capture_clearance_mm(self) -> float:
        return self.capture_inner_radius_mm - self.pad_outer_radius_mm

    @property
    def head_capture_clearance_mm(self) -> float:
        return self.capture_inner_radius_mm - (
            self.hardware_axis_global_radius_mm + self.socket_head_diameter_mm / 2.0
        )

    @property
    def trap_capture_clearance_mm(self) -> float:
        return self.capture_inner_radius_mm - (
            self.hardware_axis_global_radius_mm + self.nut_trap_across_flats_mm / 2.0
        )

    def validate(self) -> None:
        assert self.screw_count_per_seam == 2
        assert self.screw_clearance_diameter_mm == 3.40
        assert self.nut_trap_across_flats_mm == 5.60
        assert self.nut_trap_depth_mm + self.nut_trap_roof_mm == 3.0
        assert self.shoulder_radial_mm == 5.0 and self.shoulder_tangential_mm == 6.0
        assert self.pocket_radial_mm == 5.25 and self.pocket_tangential_mm == 6.25
        assert isclose(self.pocket_depth_mm - self.shoulder_height_mm, 0.10, abs_tol=1e-12)
        assert min(self.pad_capture_clearance_mm, self.head_capture_clearance_mm, self.trap_capture_clearance_mm) >= self.required_capture_clearance_mm


SPEC = RingSeamScrewOnlyR1Spec()
