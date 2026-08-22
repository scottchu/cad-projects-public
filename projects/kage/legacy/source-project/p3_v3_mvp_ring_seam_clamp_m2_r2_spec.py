"""Stack-safe numeric contract for KAGE's removable M2 U-channel seam clamp."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from p3_v3_mvp_ring_seam_clamp_m2_r1_spec import (
    LOCKED_ROOT,
    LOCKED_STEP,
    LOCKED_STEP_SHA256,
    PARITY_JSON,
    ROOT,
    RingSeamClampM2R1Spec,
)


NAMESPACE = "p3_v3_mvp_ring_seam_clamp_m2_r2"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class RingSeamClampM2R2Spec(RingSeamClampM2R1Spec):
    """Only the clamp/fastener envelope changes from r1; locked ring geometry does not."""

    # 3.00 mm ring plus 0.10 mm running clearance on each face.
    clamp_internal_axial_clearance_mm: float = 0.20
    clamp_fit_clearance_per_face_mm: float = 0.10
    clamp_top_flange_thickness_mm: float = 1.20
    clamp_bottom_flange_thickness_mm: float = 0.90

    # Flush M2 flat-head screw; nut is captured inside the 3 mm ring/end land.
    screw_length_mm: float = 4.00
    available_standard_screw_lengths_mm: tuple[float, ...] = (3.0, 4.0, 5.0, 6.0)
    screw_head_diameter_mm: float = 4.00
    screw_head_height_mm: float = 1.20
    screw_head_style: str = "M2_90deg_flat_head_flush"
    minimum_nut_thread_engagement_mm: float = 1.20
    capture_method: str = "side_loaded_M2_hex_nut_in_3mm_ring_land"
    nut_trap_depth_mm: float = 1.75
    nut_insertion_channel_width_mm: float = 4.90
    nut_minimum_top_bottom_ligament_mm: float = 0.60
    blind_bottom_floor_mm: float = 0.10
    required_adjacent_clamp_clearance_mm: float = 0.20
    modeled_axial_growth_per_clamp_face_mm: float = 0.10
    slide_start_offset_mm: float = 10.0
    slide_sample_count: int = 11

    @property
    def carrier_layer_pitch_mm(self) -> float:
        return self.carrier_layers[1][0] - self.carrier_layers[0][0]

    @property
    def adjacent_clamp_clearance_mm(self) -> float:
        return self.carrier_layer_pitch_mm - self.clamp_total_height_mm

    @property
    def nut_trap_z_ligament_each_face_mm(self) -> float:
        return (self.ring_thickness_mm - self.nut_trap_depth_mm) / 2.0

    @property
    def worst_case_adjacent_clamp_clearance_mm(self) -> float:
        return self.adjacent_clamp_clearance_mm - 2.0 * self.modeled_axial_growth_per_clamp_face_mm

    @property
    def screw_shank_below_head_mm(self) -> float:
        # ISO-style flat-head nominal length is measured over the complete screw.
        return self.screw_length_mm - self.screw_head_height_mm

    def nut_thread_engagement_mm(self, nominal_screw_length_mm: float) -> float:
        z0, z1 = self.carrier_layers[0]
        ring_mid = (z0 + z1) / 2.0
        nut_bottom = ring_mid - self.nut_thickness_mm / 2.0
        nut_top = ring_mid + self.nut_thickness_mm / 2.0
        top_top = z1 + self.clamp_fit_clearance_per_face_mm + self.clamp_top_flange_thickness_mm
        screw_tip = top_top - nominal_screw_length_mm
        return max(0.0, min(nut_top, top_top - self.screw_head_height_mm) - max(nut_bottom, screw_tip))

    @property
    def selected_standard_screw_length_mm(self) -> float:
        return min(
            length for length in self.available_standard_screw_lengths_mm
            if self.nut_thread_engagement_mm(length) >= self.minimum_nut_thread_engagement_mm
        )

    @property
    def screw_tip_above_ring_bottom_mm(self) -> float:
        z0, z1 = self.carrier_layers[0]
        top_top = z1 + self.clamp_fit_clearance_per_face_mm + self.clamp_top_flange_thickness_mm
        return (top_top - self.screw_length_mm) - z0

    def validate(self) -> None:
        assert self.ring_teeth == self.quadrant_count * self.quadrant_teeth
        assert isclose(self.seam_angle_deg, self.boundary_angle(1), abs_tol=1e-12)
        assert self.interlock_engagement_mm == 4.0
        assert 0.20 <= self.interlock_xy_clearance_per_side_mm <= 0.25
        assert self.screw_count_per_seam == 2
        assert self.capture_method == "side_loaded_M2_hex_nut_in_3mm_ring_land"
        assert self.screw_head_style == "M2_90deg_flat_head_flush"
        assert self.clamp_internal_gap_mm == self.ring_thickness_mm + 2.0 * self.clamp_fit_clearance_per_face_mm
        assert isclose(self.clamp_total_height_mm, 5.30, abs_tol=1e-12)
        assert isclose(self.carrier_layer_pitch_mm, 5.55, abs_tol=1e-12)
        assert isclose(self.adjacent_clamp_clearance_mm, 0.25, abs_tol=1e-12)
        assert self.adjacent_clamp_clearance_mm >= self.required_adjacent_clamp_clearance_mm
        assert self.worst_case_adjacent_clamp_clearance_mm > 0.0
        assert self.nut_trap_z_ligament_each_face_mm >= self.nut_minimum_top_bottom_ligament_mm
        assert self.screw_length_mm == 4.0
        assert self.nut_thread_engagement_mm(3.0) < self.minimum_nut_thread_engagement_mm
        assert self.nut_thread_engagement_mm(4.0) == self.nut_thickness_mm
        assert self.selected_standard_screw_length_mm == self.screw_length_mm
        assert self.screw_head_height_mm == self.clamp_top_flange_thickness_mm
        assert isclose(self.screw_shank_below_head_mm, 2.8, abs_tol=1e-12)
        assert self.screw_tip_above_ring_bottom_mm > 0.0
        assert self.clamp_side_wall_inner_radius_mm >= self.carrier_outer_radius_mm
        assert self.clamp_half_span_mm >= self.clamp_required_overlap_per_half_mm
        assert self.screw_edge_margin_tangent_mm >= self.minimum_hole_edge_ligament_mm
        assert min(self.screw_inner_ring_ligament_mm, self.screw_outer_ring_ligament_mm) >= self.minimum_hole_edge_ligament_mm


SPEC = RingSeamClampM2R2Spec()
