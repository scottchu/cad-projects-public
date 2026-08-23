"""Frozen Q3 r2 contract: r0 sector plus a two-hole free-roller mount base.

The accepted r0 sector remains the only printable base sector.  R2 adds one
canonical mount base, repeated at the three seams, while the inner hole pair is
retained for plain M3 screw-and-nut hardware only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC as BASE_SPEC


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q3_r2_roller_mount_inner_screws"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class Q3RollerMountInnerScrewsSpec:
    # Canonical mount is authored at the 0 degree seam in radial/tangential
    # coordinates and rotated to the r0 seam stations.
    mount_hole_radius_mm: float = BASE_SPEC.roller_axle_radius_mm
    mount_hole_tangent_offsets_mm: tuple[float, float] = BASE_SPEC.roller_mount_tangent_offsets_mm
    mount_hole_diameter_mm: float = BASE_SPEC.roller_mount_hole_diameter_mm
    minimum_mount_ligament_mm: float = 3.0

    # Start from the r0 roller-bridge witness footprint, enlarging only the
    # three deficient edges needed to leave a full 3 mm bore-edge ligament.
    # The +tangent edge remains at r0's 17.2 mm so it reaches beyond the
    # receiver lap and positively seats on the lower sector owner.
    mount_radial_min_mm: float = 113.35
    mount_radial_max_mm: float = 122.65
    mount_tangent_min_mm: float = -11.65
    mount_tangent_max_mm: float = BASE_SPEC.roller_bridge_tangent_mm[1]
    mount_contact_z_mm: float = BASE_SPEC.plate_top_z_mm
    mount_thickness_mm: float = 3.0
    mount_instance_angles_deg: tuple[float, float, float] = BASE_SPEC.seam_angles_deg
    mount_print_quantity: int = 3
    sector_print_quantity: int = 3

    # Simplified, non-print hardware envelopes used only in assembled/service
    # STEP views.  They are not threaded manufacturing models.
    m3_shank_diameter_mm: float = 3.0
    m3_head_diameter_mm: float = 5.5
    m3_head_height_mm: float = 2.0
    m3_nut_across_flats_mm: float = 5.5
    m3_nut_height_mm: float = 2.4
    m3_nut_bore_diameter_mm: float = 3.2

    # Exploded presentation offsets only.
    exploded_sector_radial_offset_mm: float = 22.0
    exploded_mount_z_offset_mm: float = 18.0
    exploded_screw_z_offset_mm: float = 34.0
    exploded_nut_z_offset_mm: float = -12.0

    # Three-mount print-fit diagnostic layout.
    mount_print_spacing_x_mm: float = 36.0
    u1_bed_xy_mm: float = BASE_SPEC.u1_bed_xy_mm
    u1_edge_keepout_mm: float = BASE_SPEC.u1_edge_keepout_mm

    # Modeled collision envelopes inherited from the neighboring MVP stations.
    ring_keepout_inner_radius_mm: float = 129.0
    ring_keepout_outer_radius_mm: float = 143.7
    ring_keepout_bottom_z_mm: float = BASE_SPEC.plate_top_z_mm
    ring_keepout_height_mm: float = 35.0
    motor_keepout_radial_min_mm: float = 78.0
    motor_keepout_radial_max_mm: float = 132.0
    motor_keepout_tangent_half_mm: float = 18.0
    motor_keepout_bottom_z_mm: float = BASE_SPEC.plate_top_z_mm
    motor_keepout_height_mm: float = 25.0
    free_roller_keepout_axis_radius_mm: float = 125.5
    free_roller_keepout_diameter_mm: float = 13.8
    free_roller_keepout_bottom_z_mm: float = -20.0
    free_roller_keepout_height_mm: float = 30.0

    contact_probe_epsilon_mm: float = 0.01
    boolean_overshoot_mm: float = BASE_SPEC.boolean_overshoot_mm
    brep_tolerance_mm3: float = BASE_SPEC.brep_tolerance_mm3
    mesh_linear_deflection_mm: float = BASE_SPEC.mesh_linear_deflection_mm
    mesh_angular_deflection_rad: float = BASE_SPEC.mesh_angular_deflection_rad

    @property
    def mount_hole_radius_clearance_mm(self) -> float:
        return self.mount_hole_diameter_mm / 2.0

    @property
    def mount_hole_axes_local_rt_mm(self) -> tuple[tuple[float, float], ...]:
        return tuple(
            (self.mount_hole_radius_mm, tangent)
            for tangent in self.mount_hole_tangent_offsets_mm
        )

    @property
    def minimum_actual_mount_ligament_mm(self) -> float:
        radial = min(
            self.mount_hole_radius_mm - self.mount_radial_min_mm,
            self.mount_radial_max_mm - self.mount_hole_radius_mm,
        ) - self.mount_hole_radius_clearance_mm
        tangent = min(
            min(self.mount_hole_tangent_offsets_mm) - self.mount_tangent_min_mm,
            self.mount_tangent_max_mm - max(self.mount_hole_tangent_offsets_mm),
        ) - self.mount_hole_radius_clearance_mm
        return min(radial, tangent)

    @property
    def lower_owner_contact_band_mm(self) -> float:
        return self.mount_tangent_max_mm - BASE_SPEC.receiver_t_half_mm

    @property
    def mount_top_z_mm(self) -> float:
        return self.mount_contact_z_mm + self.mount_thickness_mm

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm


SPEC = Q3RollerMountInnerScrewsSpec()
