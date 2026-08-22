"""Named dimensions for the KAGE B0 Q4-R2 screw-only base MVP."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import cos, radians
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q4_r2_screw_only"
MODEL_ROOT = ROOT / "models" / NAMESPACE
HANDOFF = ROOT / "docs" / "p3-v3-mvp-base-q4-r2-screw-only-design-handoff.md"

LOCKED_INPUT_HASHES = {
    "p3_v3_mvp_base_q4_r1_spec.py": "9235d8f10d9802382d63981dd1cb95307013f49b03fbe723ae34891d7a35f35e",
    "p3_v3_mvp_base_q4_r1_geometry.py": "2c989ed42de710f3a133bd7c854e36b58bc508fcfc91559f35037621838228e9",
    "p3_v3_mvp_base_q4_r1_validation.py": "32a9674490b22e1de25e90b198859de409dc8b1e4f9f3da4584167590f2ba12b",
    "models/p3_v3_mvp_base_q4_r1/p3_v3_mvp_base_q4_r1_assembled.step": "e93ad8295c427210586c3cf72d7e7157b26d01f467f848f75186548ea1f2db33",
}
HANDOFF_SHA256 = "b86557bcc9e16339c90a269ca8a85811f1988196cb3bbab7b6fb88b2b2947729"


@dataclass(frozen=True)
class ScrewOnlyBaseSpec:
    # Locked base datum and segmentation.
    base_outer_radius_mm: float = 150.0
    base_inner_radius_mm: float = 66.0
    base_thickness_mm: float = 2.5
    quadrant_count: int = 4
    quadrant_angle_deg: float = 90.0
    seam_base_angle_deg: float = 45.0
    seam_relief_per_face_mm: float = 0.05

    # U1 print envelope.
    u1_bed_xy_mm: float = 270.0
    u1_edge_keepout_mm: float = 5.0
    quadrant_brim_mm: float = 5.0
    quadrant_print_flip_deg: float = 180.0

    # One identical screw-only clamp at every seam.
    clamp_count_total: int = 4
    clamp_radial_min_mm: float = 69.0
    clamp_radial_max_mm: float = 117.0
    clamp_tangential_mm: float = 26.0
    clamp_body_thickness_mm: float = 5.0
    integral_boss_count_per_clamp: int = 2
    integral_boss_axis_radii_mm: tuple[float, float] = (78.0, 108.0)
    integral_boss_diameter_mm: float = 4.0
    integral_boss_height_mm: float = 2.4
    integral_boss_tip_chamfer_mm: float = 0.2

    # Locked quadrant receiver geometry.
    round_split_feature_diameter_mm: float = 4.15
    relieved_split_feature_radial_mm: float = 5.15
    relieved_split_feature_tangential_mm: float = 4.15

    # M3x6 ISO 4762 / ISO 4032 interface.
    screw_count_per_clamp: int = 2
    screw_axis_radius_mm: float = 93.0
    screw_tangent_offset_mm: float = 7.0
    base_screw_clearance_diameter_mm: float = 3.40
    m3_screw_nominal_diameter_mm: float = 3.0
    m3_screw_length_mm: float = 6.0
    m3_socket_head_max_diameter_mm: float = 5.50
    m3_socket_head_nominal_height_mm: float = 3.0
    m3_hex_nut_nominal_af_mm: float = 5.50
    m3_hex_nut_max_thickness_mm: float = 2.40
    nut_pocket_af_mm: float = 5.80
    nut_pocket_depth_mm: float = 2.70
    screw_tip_relief_diameter_mm: float = 3.40
    screw_tip_relief_depth_mm: float = 1.30
    clamp_bottom_skin_mm: float = 1.00
    driver_access_diameter_mm: float = 8.00
    driver_access_height_mm: float = 25.00

    # Reserved future support annulus.
    future_support_clear_radius_min_mm: float = 118.0
    future_support_clear_radius_max_mm: float = 150.0

    # Service/exploded presentation and assembly paths.
    exploded_quadrant_radial_mm: float = 28.0
    exploded_clamp_drop_mm: float = 18.0
    exploded_hardware_lift_mm: float = 18.0
    final_clamp_seam_index: int = 4
    final_clamp_below_start_z_offset_mm: float = -3.0
    rejected_last_quadrant_above_start_z_offset_mm: float = 8.0
    assembly_path_sample_step_mm: float = 0.25

    # Deliberate seam-registration negatives.
    sensitivity_tangential_translation_mm: float = 0.20
    sensitivity_rotation_deg: float = 0.20

    # Geometry construction and verification tolerances.
    boolean_overshoot_mm: float = 0.50
    seam_gap_probe_radial_mm: float = 0.40
    seam_gap_probe_tangential_mm: float = 1.00
    seam_face_sample_radii_mm: tuple[float, ...] = (70.0, 75.0, 93.0, 100.0, 114.0, 138.0)
    cad_linear_tolerance_mm: float = 0.02
    coplanarity_tolerance_mm: float = 0.02
    brep_intersection_tolerance_mm3: float = 1.0e-7
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15

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
    def clamp_radial_mm(self) -> float:
        return self.clamp_radial_max_mm - self.clamp_radial_min_mm

    @property
    def clamp_center_radius_mm(self) -> float:
        return (self.clamp_radial_min_mm + self.clamp_radial_max_mm) / 2.0

    @property
    def seam_angles_deg(self) -> tuple[float, ...]:
        return tuple(self.seam_base_angle_deg + self.quadrant_angle_deg * index for index in range(self.quadrant_count))

    @property
    def screw_tangent_offsets_mm(self) -> tuple[float, float]:
        return (-self.screw_tangent_offset_mm, self.screw_tangent_offset_mm)

    @property
    def boss_local_radial_offsets_mm(self) -> tuple[float, float]:
        return tuple(radius - self.clamp_center_radius_mm for radius in self.integral_boss_axis_radii_mm)

    @property
    def integral_boss_count_total(self) -> int:
        return self.clamp_count_total * self.integral_boss_count_per_clamp

    @property
    def screw_count_total(self) -> int:
        return self.clamp_count_total * self.screw_count_per_clamp

    @property
    def nut_count_total(self) -> int:
        return self.screw_count_total

    @property
    def printable_body_count(self) -> int:
        return self.quadrant_count + self.clamp_count_total

    @property
    def nut_pocket_circumradius_mm(self) -> float:
        return self.nut_pocket_af_mm / (2.0 * cos(radians(30.0)))

    @property
    def nut_pocket_floor_from_clamp_bottom_mm(self) -> float:
        return self.clamp_body_thickness_mm - self.nut_pocket_depth_mm

    @property
    def tip_relief_floor_from_clamp_bottom_mm(self) -> float:
        return self.nut_pocket_floor_from_clamp_bottom_mm - self.screw_tip_relief_depth_mm

    @property
    def nut_axial_slack_mm(self) -> float:
        return self.nut_pocket_depth_mm - self.m3_hex_nut_max_thickness_mm

    @property
    def screw_tip_beyond_base_and_nut_mm(self) -> float:
        return self.m3_screw_length_mm - self.base_thickness_mm - self.m3_hex_nut_max_thickness_mm

    @property
    def round_boss_diametral_clearance_mm(self) -> float:
        return self.round_split_feature_diameter_mm - self.integral_boss_diameter_mm

    @property
    def relieved_boss_radial_clearance_mm(self) -> float:
        return self.relieved_split_feature_radial_mm - self.integral_boss_diameter_mm

    @property
    def relieved_boss_tangential_clearance_mm(self) -> float:
        return self.relieved_split_feature_tangential_mm - self.integral_boss_diameter_mm

    @property
    def boss_front_recess_mm(self) -> float:
        return self.base_thickness_mm - self.integral_boss_height_mm


SPEC = ScrewOnlyBaseSpec()


def frozen_input_evidence() -> dict[str, object]:
    actual = {relative: sha256((ROOT / relative).read_bytes()).hexdigest() for relative in LOCKED_INPUT_HASHES}
    actual["handoff"] = sha256(HANDOFF.read_bytes()).hexdigest()
    expected = dict(LOCKED_INPUT_HASHES)
    expected["handoff"] = HANDOFF_SHA256
    return {"actual": actual, "expected": expected, "all_frozen_hashes_match": actual == expected}
