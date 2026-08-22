"""Frozen dimensions for the four-part KAGE B0 Q4-R3 integral-lap MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q4_r3_integral_lap"
MODEL_ROOT = ROOT / "models" / NAMESPACE
HANDOFF = ROOT / "docs" / "p3-v3-mvp-base-q4-r3-integral-lap-design-handoff.md"


@dataclass(frozen=True)
class IntegralLapSpec:
    base_outer_radius_mm: float = 150.0
    base_inner_radius_mm: float = 66.0
    base_thickness_mm: float = 2.5
    quadrant_count: int = 4
    seam_base_angle_deg: float = 45.0
    quadrant_angle_deg: float = 90.0
    seam_relief_per_face_mm: float = 0.05

    role_a_quadrants: tuple[int, int] = (1, 3)
    role_b_quadrants: tuple[int, int] = (2, 4)
    lap_radial_min_mm: float = 70.0
    lap_radial_max_mm: float = 116.0
    tongue_overlap_depth_mm: float = 10.0
    receiver_rebate_depth_mm: float = 10.3
    receiver_radial_clearance_per_side_mm: float = 0.2
    receiver_tip_clearance_mm: float = 0.3
    tongue_thickness_mm: float = 1.25
    receiver_roof_thickness_mm: float = 1.25
    lap_interface_z_mm: float = 1.25

    screws_per_seam: int = 2
    screw_axis_radii_mm: tuple[float, float] = (82.0, 104.0)
    screw_axis_tangent_into_b_mm: float = 5.0
    clearance_hole_diameter_mm: float = 3.4
    m3_screw_nominal_diameter_mm: float = 3.0
    m3_screw_length_mm: float = 6.0
    m3_socket_head_max_diameter_mm: float = 5.5
    m3_socket_head_height_mm: float = 3.0
    m3_nut_af_mm: float = 5.5
    m3_nut_max_thickness_mm: float = 2.4
    driver_hex_mm: float = 2.5
    wrench_access_af_mm: float = 5.5

    future_support_clear_radius_min_mm: float = 118.0
    future_support_clear_radius_max_mm: float = 150.0
    u1_bed_xy_mm: float = 270.0
    u1_edge_keepout_mm: float = 5.0
    quadrant_brim_mm: float = 5.0

    assembly_start_z_mm: float = 5.0
    assembly_path_step_mm: float = 0.25
    registration_negative_shift_mm: float = 0.5
    boolean_overshoot_mm: float = 0.5
    tool_fuse_overlap_mm: float = 0.5
    brep_intersection_tolerance_mm3: float = 1.0e-7
    cad_linear_tolerance_mm: float = 0.02
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    exploded_quadrant_radial_mm: float = 28.0
    exploded_hardware_z_mm: float = 18.0

    @property
    def seam_angles_deg(self) -> tuple[float, ...]:
        return tuple(self.seam_base_angle_deg + self.quadrant_angle_deg * i for i in range(4))

    @property
    def lap_radial_span_mm(self) -> float:
        return self.lap_radial_max_mm - self.lap_radial_min_mm

    @property
    def seam_gap_nominal_mm(self) -> float:
        return 2.0 * self.seam_relief_per_face_mm

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm

    @property
    def screw_count_total(self) -> int:
        return 4 * self.screws_per_seam

    @property
    def nut_count_total(self) -> int:
        return self.screw_count_total


SPEC = IntegralLapSpec()

