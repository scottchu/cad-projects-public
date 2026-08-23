"""Preview-only numeric contract for a three-sector KAGE MVP base.

This branch does not replace the validated Q4 base.  It exists to answer one
question: can the 300 mm base be split into three mechanically useful sectors,
with every seam beneath a free-roller tower, and still fit a Snapmaker U1 when
rotated diagonally?
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class Q3RollerSeamPreviewSpec:
    # Locked envelope copied from the current Q4 MVP base.
    base_outer_radius_mm: float = 150.0
    base_inner_radius_mm: float = 66.0
    plate_bottom_z_mm: float = -31.5
    plate_top_z_mm: float = -25.5
    plate_thickness_mm: float = 6.0

    # The three seams sit under the three free-roller towers.  Motors remain
    # centered in uninterrupted sectors halfway between adjacent seams.
    seam_angles_deg: tuple[float, float, float] = (60.0, 180.0, 300.0)
    sector_center_angles_deg: tuple[float, float, float] = (0.0, 120.0, 240.0)
    motor_station_angles_deg: tuple[float, float, float] = (0.0, 120.0, 240.0)
    sector_sweep_deg: float = 120.0

    # Complementary 3 + 3 mm step lap.  The outer radius reaches beyond the
    # roller C-bar and M3 axes so the roller station really bridges the seam.
    lap_r_min_mm: float = 70.0
    lap_r_max_mm: float = 124.0
    donor_t_half_mm: float = 13.0
    receiver_t_half_mm: float = 13.2
    receiver_plan_clearance_mm: float = 0.2
    lap_split_z_mm: float = -28.5
    lower_lap_thickness_mm: float = 3.0
    upper_lap_thickness_mm: float = 3.0

    # Four-hole seam interface.  The outer row is the B3 free-roller tower
    # interface.  The inner row mirrors it across the broad lap envelope so
    # every one of the three identical sectors has the same clamped baseline.
    roller_axle_radius_mm: float = 118.0
    inner_seam_clamp_radius_mm: float = 76.0
    roller_mount_tangent_offsets_mm: tuple[float, float] = (-7.0, 7.0)
    roller_mount_hole_diameter_mm: float = 3.3
    roller_bridge_radial_mm: tuple[float, float] = (114.0, 120.0)
    roller_bridge_tangent_mm: tuple[float, float] = (-11.2, 17.2)
    roller_bridge_preview_thickness_mm: float = 1.2
    roller_bridge_preview_z_mm: float = -24.8

    # U1 preview.  Each sector is placed on its own virtual build plate.
    u1_bed_xy_mm: float = 270.0
    u1_edge_keepout_mm: float = 5.0
    print_brim_mm: float = 5.0
    diagonal_rotation_deg: float = 45.0
    preview_bed_spacing_mm: float = 300.0
    preview_bed_thickness_mm: float = 0.8

    # Diagnostic model-only 3MF tessellation.  The file contains one sector;
    # the required print quantity is three.
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15

    boolean_overshoot_mm: float = 0.5
    brep_tolerance_mm3: float = 1.0e-6

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm

    @property
    def seam_hole_row_radii_mm(self) -> tuple[float, float]:
        return (self.inner_seam_clamp_radius_mm, self.roller_axle_radius_mm)

    @property
    def seam_holes_per_seam(self) -> int:
        return len(self.seam_hole_row_radii_mm) * len(self.roller_mount_tangent_offsets_mm)

    @property
    def seam_hole_total_count(self) -> int:
        return len(self.seam_angles_deg) * self.seam_holes_per_seam

    @property
    def seam_hole_radial_baseline_mm(self) -> float:
        return self.roller_axle_radius_mm - self.inner_seam_clamp_radius_mm

    @property
    def inner_seam_edge_inset_mm(self) -> float:
        return self.inner_seam_clamp_radius_mm - self.lap_r_min_mm

    @property
    def outer_seam_edge_inset_mm(self) -> float:
        return self.lap_r_max_mm - self.roller_axle_radius_mm

    @property
    def seam_bore_edge_margin_mm(self) -> float:
        radial_margin = min(self.inner_seam_edge_inset_mm, self.outer_seam_edge_inset_mm)
        tangent_margin = self.donor_t_half_mm - max(abs(v) for v in self.roller_mount_tangent_offsets_mm)
        return min(radial_margin, tangent_margin) - self.roller_mount_hole_diameter_mm / 2.0


SPEC = Q3RollerSeamPreviewSpec()
