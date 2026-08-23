"""Numeric contract for KAGE's removable C-channel ring-seam clamp coupon."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_ring_seam_clamp_m2_r1"
MODEL_ROOT = ROOT / "models" / NAMESPACE
LOCKED_ROOT = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
LOCKED_STEP = LOCKED_ROOT / "p3_v3_direct_gear_race_assembled.step"
PARITY_JSON = ROOT / "models" / "p3_v3_locked_parametric_repair_r1" / "p3_v3_locked_parametric_repair_r1_zero_delta_parity.json"
LOCKED_STEP_SHA256 = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"


@dataclass(frozen=True)
class RingSeamClampM2R1Spec:
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
    seam_angle_deg: float = 90.0 + 360.0 / 520.0
    carrier_race_radius_mm: float = 131.60
    protected_radius_mm: float = 133.20
    carrier_outer_radius_mm: float = 138.90

    # Existing small keyhole/C alignment feature retained from the accepted coupon.
    interlock_center_radius_mm: float = 136.00
    interlock_engagement_mm: float = 4.00
    interlock_neck_width_mm: float = 1.40
    interlock_neck_root_mm: float = 0.80
    interlock_lobe_radius_mm: float = 1.50
    interlock_lobe_center_tangent_mm: float = 2.50
    interlock_xy_clearance_per_side_mm: float = 0.22
    interlock_axial_allowance_mm: float = 0.10
    interlock_root_fillet_mm: float = 0.35

    # One removable three-sided channel: open radially inward, closed outboard.
    clamp_inner_radius_mm: float = 134.60
    clamp_outer_radius_mm: float = 140.20
    clamp_side_wall_inner_radius_mm: float = 139.40
    clamp_tangential_width_mm: float = 24.00
    clamp_top_flange_thickness_mm: float = 1.60
    clamp_bottom_flange_thickness_mm: float = 3.50
    clamp_internal_axial_clearance_mm: float = 0.30
    clamp_fit_clearance_per_face_mm: float = 0.15
    clamp_required_overlap_per_half_mm: float = 8.0

    screw_count_per_seam: int = 2
    screw_nominal_diameter_mm: float = 2.00
    screw_clearance_diameter_mm: float = 2.40
    screw_length_mm: float = 8.00
    available_standard_screw_lengths_mm: tuple[float, ...] = (6.0, 8.0, 10.0)
    screw_head_diameter_mm: float = 3.80
    screw_head_height_mm: float = 2.00
    screw_axis_radius_mm: float = 136.50
    screw_tangential_offsets_mm: tuple[float, float] = (-7.00, 7.00)
    minimum_hole_edge_ligament_mm: float = 1.20

    capture_method: str = "captive_M2_hex_nut_blind_bottom"
    nut_across_flats_mm: float = 4.00
    nut_thickness_mm: float = 1.60
    nut_trap_across_flats_mm: float = 4.20
    nut_trap_depth_mm: float = 1.75
    nut_floor_thickness_mm: float = 0.40

    receiver_boss_radius_mm: float = 2.55
    receiver_connector_inner_radius_mm: float = 134.60
    receiver_connector_tangential_width_mm: float = 5.20
    capture_inner_radius_mm: float = 145.00
    required_capture_clearance_mm: float = 0.25

    non_seam_exclusion_tangential_width_mm: float = 30.0
    printer_bed_mm: tuple[float, float, float] = (270.0, 270.0, 270.0)
    bed_margin_mm: float = 5.0
    minimum_layout_gap_mm: float = 3.0

    @property
    def ring_thickness_mm(self) -> float:
        return self.carrier_layers[0][1] - self.carrier_layers[0][0]

    @property
    def clamp_internal_gap_mm(self) -> float:
        return self.ring_thickness_mm + self.clamp_internal_axial_clearance_mm

    @property
    def clamp_total_height_mm(self) -> float:
        return self.clamp_top_flange_thickness_mm + self.clamp_internal_gap_mm + self.clamp_bottom_flange_thickness_mm

    @property
    def clamp_half_span_mm(self) -> float:
        return self.clamp_tangential_width_mm / 2.0

    @property
    def screw_edge_margin_tangent_mm(self) -> float:
        return self.clamp_half_span_mm - abs(self.screw_tangential_offsets_mm[0]) - self.screw_clearance_diameter_mm / 2.0

    @property
    def screw_outer_ring_ligament_mm(self) -> float:
        return self.carrier_outer_radius_mm - self.screw_axis_radius_mm - self.screw_clearance_diameter_mm / 2.0

    @property
    def screw_inner_ring_ligament_mm(self) -> float:
        return self.screw_axis_radius_mm - self.carrier_race_radius_mm - self.screw_clearance_diameter_mm / 2.0

    @property
    def minimum_full_nut_engagement_screw_length_mm(self) -> float:
        return self.clamp_top_flange_thickness_mm + self.clamp_internal_gap_mm + self.nut_trap_depth_mm

    @property
    def selected_standard_screw_length_mm(self) -> float:
        return min(length for length in self.available_standard_screw_lengths_mm if length >= self.minimum_full_nut_engagement_screw_length_mm)

    def boundary_angle(self, quadrant_index: int) -> float:
        return self.locked_global_tooth_phase_deg + 90.0 * quadrant_index

    def validate(self) -> None:
        assert self.ring_teeth == self.quadrant_count * self.quadrant_teeth
        assert isclose(self.seam_angle_deg, self.boundary_angle(1), abs_tol=1e-12)
        assert self.capture_method == "captive_M2_hex_nut_blind_bottom"
        assert self.interlock_engagement_mm == 4.0
        assert 0.20 <= self.interlock_xy_clearance_per_side_mm <= 0.25
        assert self.screw_count_per_seam == 2
        assert self.screw_tangential_offsets_mm[0] < 0 < self.screw_tangential_offsets_mm[1]
        assert self.clamp_internal_gap_mm == self.ring_thickness_mm + 2.0 * self.clamp_fit_clearance_per_face_mm
        assert self.clamp_side_wall_inner_radius_mm >= self.carrier_outer_radius_mm
        assert self.clamp_half_span_mm >= self.clamp_required_overlap_per_half_mm
        assert self.screw_edge_margin_tangent_mm >= self.minimum_hole_edge_ligament_mm
        assert min(self.screw_inner_ring_ligament_mm, self.screw_outer_ring_ligament_mm) >= self.minimum_hole_edge_ligament_mm
        assert self.clamp_bottom_flange_thickness_mm >= self.nut_trap_depth_mm + self.nut_floor_thickness_mm
        assert 6.0 < self.minimum_full_nut_engagement_screw_length_mm <= 8.0
        assert self.screw_length_mm == self.selected_standard_screw_length_mm == 8.0


SPEC = RingSeamClampM2R1Spec()
