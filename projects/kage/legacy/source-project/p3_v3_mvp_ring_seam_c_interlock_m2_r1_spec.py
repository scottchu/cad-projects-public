"""Numeric contract for the isolated valley-seam C/jigsaw interlock coupon."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_ring_seam_c_interlock_m2_r1"
MODEL_ROOT = ROOT / "models" / NAMESPACE
LOCKED_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
LOCKED_STEP = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step"
PARITY_JSON = ROOT / "models" / "p3_v3_locked_parametric_repair_r1" / "p3_v3_locked_parametric_repair_r1_zero_delta_parity.json"
LOCKED_STEP_SHA256 = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"


@dataclass(frozen=True)
class CInterlockM2R1Spec:
    roles: tuple[str, str, str] = ("hour", "minute", "second")
    role_colors: tuple[str, str, str] = ("#3F8F87", "#E38B48", "#D95D78")
    display_fin_angles_deg: tuple[float, float, float] = (305.0, 45.0, 145.0)
    carrier_layers: tuple[tuple[float, float], ...] = ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    quadrant_occurrence_indices: tuple[tuple[int, int, int, int], ...] = (
        (108, 109, 110, 111), (139, 140, 141, 142), (170, 171, 172, 173),
    )

    ring_teeth: int = 260
    quadrant_count: int = 4
    quadrant_teeth: int = 65
    tooth_pitch_deg: float = 360.0 / 260.0
    locked_global_tooth_phase_deg: float = 360.0 / 520.0
    crop_boundary_shift_deg: float = 0.692307692308
    coupon_seam_angle_deg: float = 90.0 + 0.692307692308
    gear_ratio: float = 260.0 / 16.0
    locked_hour_global_pinion_spin_deg: float = (360.0 / 520.0) * (260.0 / 16.0)
    shifted_quadrant_local_pinion_phase_deg: float = 0.0
    global_pinion_phase_delta_deg: float = 0.0

    carrier_race_radius_mm: float = 131.60
    tooth_root_radius_mm: float = 132.50
    protected_radius_mm: float = 133.20
    carrier_outer_radius_mm: float = 138.90

    interlock_center_radius_mm: float = 136.00
    interlock_engagement_mm: float = 4.00
    interlock_neck_width_mm: float = 1.40
    interlock_neck_root_mm: float = 0.80
    interlock_lobe_radius_mm: float = 1.50
    interlock_lobe_center_tangent_mm: float = 2.50
    interlock_xy_clearance_per_side_mm: float = 0.22
    interlock_axial_allowance_mm: float = 0.10
    interlock_root_fillet_mm: float = 0.35

    bridge_inner_radius_mm: float = 138.60
    bridge_outer_radius_mm: float = 144.70
    bridge_tangential_width_mm: float = 28.0
    bridge_thickness_mm: float = 1.10
    capture_inner_radius_mm: float = 145.00
    required_capture_clearance_mm: float = 0.25

    screw_count_per_seam: int = 2
    screw_nominal_diameter_mm: float = 2.00
    screw_clearance_diameter_mm: float = 2.40
    screw_length_mm: float = 6.00
    socket_head_diameter_mm: float = 3.80
    socket_head_height_mm: float = 2.00
    hardware_axis_global_radius_mm: float = 141.90
    role_tangential_offsets_mm: tuple[tuple[float, float], ...] = (
        (-11.0, 5.0), (-5.0, 11.0), (-11.0, 5.0),
    )
    nut_across_flats_mm: float = 4.00
    nut_thickness_mm: float = 1.60
    nut_trap_across_flats_mm: float = 4.15
    nut_trap_depth_mm: float = 1.70
    nut_axial_play_mm: float = 0.10
    receiver_boss_radius_mm: float = 2.55
    receiver_connector_inner_radius_mm: float = 138.20
    receiver_connector_tangential_width_mm: float = 5.20

    non_seam_exclusion_tangential_width_mm: float = 32.0
    printer_bed_mm: tuple[float, float, float] = (270.0, 270.0, 270.0)
    bed_margin_mm: float = 5.0
    minimum_layout_gap_mm: float = 3.0

    @property
    def bridge_capture_clearance_mm(self) -> float:
        return self.capture_inner_radius_mm - self.bridge_outer_radius_mm

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

    def boundary_angle(self, quadrant_index: int) -> float:
        return self.crop_boundary_shift_deg + 90.0 * quadrant_index

    def validate(self) -> None:
        assert self.ring_teeth == self.quadrant_count * self.quadrant_teeth
        assert isclose(self.crop_boundary_shift_deg, self.locked_global_tooth_phase_deg, abs_tol=1e-12)
        assert isclose(self.coupon_seam_angle_deg, self.boundary_angle(1), abs_tol=1e-12)
        assert self.interlock_engagement_mm == 4.0
        assert self.interlock_neck_width_mm >= 1.20
        assert 0.20 <= self.interlock_xy_clearance_per_side_mm <= 0.25
        assert self.interlock_axial_allowance_mm == 0.10
        assert self.screw_count_per_seam == 2 and self.screw_length_mm == 6.0
        assert self.screw_clearance_diameter_mm == 2.40
        assert self.nut_across_flats_mm == 4.0
        assert min(self.bridge_capture_clearance_mm, self.head_capture_clearance_mm, self.trap_capture_clearance_mm) >= self.required_capture_clearance_mm
        assert isclose(
            self.locked_hour_global_pinion_spin_deg - self.crop_boundary_shift_deg * self.gear_ratio,
            self.shifted_quadrant_local_pinion_phase_deg,
            abs_tol=1e-10,
        )


SPEC = CInterlockM2R1Spec()
