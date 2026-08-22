"""Frozen, named dimensions for the isolated KAGE B0 base MVP.

This successor intentionally owns only the four-to-one stationary base test.
It contains no ring, motor, electronics, light source, or future support holes.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import cos, radians
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q4_r1"
MODEL_ROOT = ROOT / "models" / NAMESPACE

DESIGN_HANDOFF = ROOT / "docs" / "p3-v3-mvp-base-q4-r0-design-handoff.md"
RECONCILIATION_HANDOFF = ROOT / "docs" / "kage-mvp-base-handoffs-independent-reconciliation.md"
DESIGN_HANDOFF_SHA256 = "3ff2073e1eb5247ee1cc1ab7c0001ad1cc885b6d350d1c78ba097406de10b67a"
RECONCILIATION_HANDOFF_SHA256 = "de1b5907f62a4da4e36b94a410e2975a715bfea18cffc9cfa13bb0c1576fb309"


@dataclass(frozen=True)
class BaseMvpSpec:
    # Base datum and segmentation.
    base_outer_radius_mm: float = 150.0
    base_inner_radius_mm: float = 66.0
    base_thickness_mm: float = 2.5
    quadrant_count: int = 4
    quadrant_angle_deg: float = 90.0
    seam_base_angle_deg: float = 45.0
    seam_relief_per_face_mm: float = 0.05

    # Printer envelope. ``brim`` is reserved on every side of the part AABB.
    u1_bed_xy_mm: float = 270.0
    u1_edge_keepout_mm: float = 5.0
    quadrant_brim_mm: float = 5.0
    quadrant_print_flip_deg: float = 180.0

    # One bridge per seam, entirely inside the later B1 support reservation.
    bridge_count_per_seam: int = 1
    bridge_radial_min_mm: float = 69.0
    bridge_radial_max_mm: float = 117.0
    bridge_tangential_mm: float = 26.0
    bridge_thickness_mm: float = 5.0
    future_support_clear_radius_min_mm: float = 118.0
    future_support_clear_radius_max_mm: float = 150.0

    # M3x6 clamp interface: one screw on each side of every seam.
    screw_axis_radius_mm: float = 93.0
    screw_tangent_offset_mm: float = 7.0
    base_screw_clearance_diameter_mm: float = 3.40
    m3_screw_nominal_diameter_mm: float = 3.0
    m3_screw_length_mm: float = 6.0
    m3_button_head_max_diameter_mm: float = 5.50
    m3_hex_nut_nominal_af_mm: float = 5.50
    m3_hex_nut_max_thickness_mm: float = 2.40
    nut_pocket_af_mm: float = 5.80
    nut_pocket_depth_mm: float = 2.70
    screw_tip_relief_diameter_mm: float = 3.40
    screw_tip_relief_depth_mm: float = 1.30
    bridge_bottom_skin_mm: float = 1.00

    # Round-plus-relieved seam registration.
    round_dowel_axis_radius_mm: float = 78.0
    relief_dowel_axis_radius_mm: float = 108.0
    dowel_nominal_diameter_mm: float = 4.0
    dowel_length_mm: float = 6.0
    joiner_press_bore_diameter_mm: float = 3.95
    joiner_press_engagement_mm: float = 3.50
    base_split_slip_bore_diameter_mm: float = 4.15
    base_split_slip_engagement_mm: float = 2.50
    relief_split_slot_radial_mm: float = 5.15
    relief_split_slot_tangential_mm: float = 4.15

    # Bare-base assembly/service checks.
    driver_access_diameter_mm: float = 8.0
    driver_access_height_mm: float = 25.0
    exploded_quadrant_radial_mm: float = 28.0
    exploded_bridge_drop_mm: float = 18.0
    bad_fixture_shim_mm: float = 0.50
    bad_fixture_radial_offset_mm: float = 0.50
    final_bridge_seam_index: int = 4
    final_bridge_below_start_z_offset_mm: float = -3.0
    rejected_last_quadrant_above_start_z_offset_mm: float = 8.0
    assembly_path_sample_step_mm: float = 0.25

    # Source construction and verification tolerances.
    boolean_overshoot_mm: float = 0.50
    sector_mask_radius_mm: float = 400.0
    seam_face_sample_radii_mm: tuple[float, ...] = (70.0, 75.0, 93.0, 100.0, 114.0, 138.0)
    seam_nonface_dowel_radii_mm: tuple[float, ...] = (78.0, 108.0)
    seam_gap_probe_radial_mm: float = 0.40
    seam_gap_probe_tangential_mm: float = 1.00
    brep_slot_probe_radial_thickness_mm: float = 0.00001
    brep_intersection_tolerance_mm3: float = 1.0e-7
    cad_linear_tolerance_mm: float = 0.02
    coplanarity_tolerance_mm: float = 0.02
    fixture_failure_threshold_mm: float = 0.25
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    legacy_mount_voids_enabled: bool = False

    @property
    def base_outer_diameter_mm(self) -> float:
        return self.base_outer_radius_mm * 2.0

    @property
    def base_inner_diameter_mm(self) -> float:
        return self.base_inner_radius_mm * 2.0

    @property
    def seam_gap_nominal_mm(self) -> float:
        return self.seam_relief_per_face_mm * 2.0

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm

    @property
    def bridge_radial_mm(self) -> float:
        return self.bridge_radial_max_mm - self.bridge_radial_min_mm

    @property
    def bridge_center_radius_mm(self) -> float:
        return (self.bridge_radial_min_mm + self.bridge_radial_max_mm) / 2.0

    @property
    def bridge_count_total(self) -> int:
        return self.quadrant_count * self.bridge_count_per_seam

    @property
    def screw_count_total(self) -> int:
        return self.bridge_count_total * 2

    @property
    def nut_count_total(self) -> int:
        return self.screw_count_total

    @property
    def dowel_count_total(self) -> int:
        return self.bridge_count_total * 2

    @property
    def printable_body_count(self) -> int:
        return self.quadrant_count + self.bridge_count_total

    @property
    def seam_angles_deg(self) -> tuple[float, ...]:
        return tuple(self.seam_base_angle_deg + self.quadrant_angle_deg * index for index in range(self.quadrant_count))

    @property
    def screw_tangent_offsets_mm(self) -> tuple[float, float]:
        return (-self.screw_tangent_offset_mm, self.screw_tangent_offset_mm)

    @property
    def dowel_axis_radii_mm(self) -> tuple[float, float]:
        return (self.round_dowel_axis_radius_mm, self.relief_dowel_axis_radius_mm)

    @property
    def dowel_local_radial_offsets_mm(self) -> tuple[float, float]:
        return tuple(radius - self.bridge_center_radius_mm for radius in self.dowel_axis_radii_mm)

    @property
    def nut_pocket_circumradius_mm(self) -> float:
        return self.nut_pocket_af_mm / (2.0 * cos(radians(30.0)))

    @property
    def nut_nominal_circumradius_mm(self) -> float:
        return self.m3_hex_nut_nominal_af_mm / (2.0 * cos(radians(30.0)))

    @property
    def nut_pocket_floor_from_bridge_bottom_mm(self) -> float:
        return self.bridge_thickness_mm - self.nut_pocket_depth_mm

    @property
    def tip_relief_floor_from_bridge_bottom_mm(self) -> float:
        return self.nut_pocket_floor_from_bridge_bottom_mm - self.screw_tip_relief_depth_mm

    @property
    def relief_slot_center_spacing_mm(self) -> float:
        return self.relief_split_slot_radial_mm - self.relief_split_slot_tangential_mm

    @property
    def relief_slot_center_offsets_mm(self) -> tuple[float, float]:
        half = self.relief_slot_center_spacing_mm / 2.0
        return (-half, half)

    @property
    def dowel_diametral_slip_mm(self) -> float:
        return self.base_split_slip_bore_diameter_mm - self.dowel_nominal_diameter_mm

    @property
    def nut_axial_slack_mm(self) -> float:
        return self.nut_pocket_depth_mm - self.m3_hex_nut_max_thickness_mm

    @property
    def screw_tip_beyond_base_and_nut_mm(self) -> float:
        return self.m3_screw_length_mm - self.base_thickness_mm - self.m3_hex_nut_max_thickness_mm

    @property
    def nut_pocket_across_corners_mm(self) -> float:
        return self.nut_pocket_circumradius_mm * 2.0

    @property
    def nut_radial_wall_mm(self) -> float:
        return (self.bridge_radial_mm - self.nut_pocket_across_corners_mm) / 2.0

    @property
    def nut_to_nearest_dowel_ligament_mm(self) -> float:
        nearest_axis_distance = min(abs(self.screw_axis_radius_mm - radius) for radius in self.dowel_axis_radii_mm)
        return nearest_axis_distance - self.nut_pocket_circumradius_mm - self.joiner_press_bore_diameter_mm / 2.0

    @property
    def tangential_end_wall_mm(self) -> float:
        return self.bridge_tangential_mm / 2.0 - self.screw_tangent_offset_mm - self.nut_pocket_circumradius_mm


SPEC = BaseMvpSpec()


def frozen_input_evidence() -> dict[str, object]:
    actual = {
        "design_handoff": sha256(DESIGN_HANDOFF.read_bytes()).hexdigest(),
        "reconciliation_handoff": sha256(RECONCILIATION_HANDOFF.read_bytes()).hexdigest(),
    }
    expected = {
        "design_handoff": DESIGN_HANDOFF_SHA256,
        "reconciliation_handoff": RECONCILIATION_HANDOFF_SHA256,
    }
    return {
        "actual": actual,
        "expected": expected,
        "all_frozen_hashes_match": actual == expected,
    }
