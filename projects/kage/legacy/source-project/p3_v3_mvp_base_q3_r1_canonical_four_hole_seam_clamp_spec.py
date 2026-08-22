"""Frozen contract for the Q3 canonical four-hole seam clamp branch.

The Q3 sector geometry remains owned by the accepted r0 preview source.  This
branch adds only one separately printable, repeated flat clamp.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p3_v3_mvp_base_q3_r0_roller_seam_diagonal_preview_spec import SPEC as BASE_SPEC


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_base_q3_r1_canonical_four_hole_seam_clamp"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class CanonicalFourHoleSeamClampSpec:
    # The canonical part is authored at the zero-degree seam in local
    # radial/tangential coordinates, then rotated to the three Q3 seams.
    clamp_radial_min_mm: float = 71.35
    clamp_radial_max_mm: float = 122.65
    clamp_tangent_min_mm: float = -11.65
    clamp_tangent_max_mm: float = 17.20
    clamp_thickness_mm: float = 3.00

    # Flush contact is on the existing Q3 plate top plane.  The clamp remains
    # a separate printable part and shares only this face with the base.
    clamp_contact_z_mm: float = BASE_SPEC.plate_top_z_mm

    # Frozen M3 clearance pattern: two radial rows x two tangential columns.
    clamp_hole_radii_mm: tuple[float, float] = (76.0, 118.0)
    clamp_hole_tangent_offsets_mm: tuple[float, float] = (-7.0, 7.0)
    clamp_hole_diameter_mm: float = 3.30
    clamp_hole_count: int = 4
    clamp_instance_angles_deg: tuple[float, float, float] = BASE_SPEC.seam_angles_deg
    clamp_print_quantity: int = 3
    sector_print_quantity: int = 3

    # Exploded/service presentation only; assembled placements remain flush.
    exploded_sector_radial_offset_mm: float = 22.0
    exploded_clamp_z_offset_mm: float = 18.0

    # Clamp-only print layout.  Three identical clamps fit comfortably on U1.
    clamp_print_spacing_x_mm: float = 62.0
    u1_bed_xy_mm: float = BASE_SPEC.u1_bed_xy_mm
    u1_edge_keepout_mm: float = BASE_SPEC.u1_edge_keepout_mm

    # Existing optical/mechanical keep-out envelopes.  These are validation
    # volumes only and do not add geometry to the base or clamp.
    ring_keepout_inner_radius_mm: float = 129.0
    ring_keepout_outer_radius_mm: float = 143.7
    ring_keepout_bottom_z_mm: float = BASE_SPEC.plate_top_z_mm
    ring_keepout_height_mm: float = 35.0
    motor_keepout_radial_min_mm: float = 78.0
    motor_keepout_radial_max_mm: float = 132.0
    motor_keepout_tangent_half_mm: float = 18.0
    motor_keepout_bottom_z_mm: float = BASE_SPEC.plate_top_z_mm
    motor_keepout_height_mm: float = 25.0
    roller_keepout_axis_radius_mm: float = 125.5
    roller_keepout_diameter_mm: float = 13.8
    roller_keepout_bottom_z_mm: float = -20.0
    roller_keepout_height_mm: float = 30.0

    minimum_edge_ligament_mm: float = 3.0
    boolean_overshoot_mm: float = BASE_SPEC.boolean_overshoot_mm
    brep_tolerance_mm3: float = BASE_SPEC.brep_tolerance_mm3
    mesh_linear_deflection_mm: float = BASE_SPEC.mesh_linear_deflection_mm
    mesh_angular_deflection_rad: float = BASE_SPEC.mesh_angular_deflection_rad

    @property
    def clamp_radial_span_mm(self) -> float:
        return self.clamp_radial_max_mm - self.clamp_radial_min_mm

    @property
    def clamp_tangent_span_mm(self) -> float:
        return self.clamp_tangent_max_mm - self.clamp_tangent_min_mm

    @property
    def clamp_top_z_mm(self) -> float:
        return self.clamp_contact_z_mm + self.clamp_thickness_mm

    @property
    def clamp_hole_radius_mm(self) -> float:
        return self.clamp_hole_diameter_mm / 2.0

    @property
    def clamp_hole_axes_local_rt_mm(self) -> tuple[tuple[float, float], ...]:
        return tuple(
            (radius, tangent)
            for radius in self.clamp_hole_radii_mm
            for tangent in self.clamp_hole_tangent_offsets_mm
        )

    @property
    def minimum_actual_edge_ligament_mm(self) -> float:
        radial = min(
            min(self.clamp_hole_radii_mm) - self.clamp_radial_min_mm,
            self.clamp_radial_max_mm - max(self.clamp_hole_radii_mm),
        ) - self.clamp_hole_radius_mm
        tangent = min(
            min(self.clamp_hole_tangent_offsets_mm) - self.clamp_tangent_min_mm,
            self.clamp_tangent_max_mm - max(self.clamp_hole_tangent_offsets_mm),
        ) - self.clamp_hole_radius_mm
        return min(radial, tangent)

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_bed_xy_mm - 2.0 * self.u1_edge_keepout_mm


SPEC = CanonicalFourHoleSeamClampSpec()
