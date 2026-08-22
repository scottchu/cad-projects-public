"""Frozen implementation parameters for the passive KAGE three-station roller MVP.

This namespace implements only the design contract in
``docs/p3_v3_mvp_free_roller_r0_contract.md``.  It deliberately has no motor,
drive-pinion, electronics, or stationary guide-rail parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_free_roller_r0_three_station"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class FreeRollerR0Spec:
    station_angles_deg: tuple[float, float, float] = (60.0, 180.0, 300.0)

    base_outer_radius_mm: float = 150.0
    base_plate_z_mm: tuple[float, float] = (-31.5, -25.5)
    station_seat_z_mm: float = -25.5
    outer_mount_radius_mm: float = 118.0
    outer_mount_tangent_mm: tuple[float, float] = (-7.0, 7.0)
    inner_seam_radius_mm: float = 76.0
    base_hole_diameter_mm: float = 3.3
    mount_slot_width_mm: float = 3.6
    mount_slot_length_mm: float = 4.1
    mount_slot_center_travel_mm: float = 0.5
    station_foot_z_mm: tuple[float, float] = (-25.5, -22.5)
    station_foot_r_mm: tuple[float, float] = (112.5, 130.0)
    station_foot_t_mm: tuple[float, float] = (-12.5, 17.2)

    nut_across_flats_mm: float = 5.7
    nut_pocket_depth_mm: float = 2.5
    nut_front_skin_mm: float = 0.5
    station_screw_length_mm: float = 8.0
    station_screw_diameter_mm: float = 3.0
    station_washer_od_mm: float = 7.0
    station_washer_thickness_mm: float = 0.5
    nut_thickness_mm: float = 2.4

    carrier_layers_z_mm: tuple[tuple[float, float], ...] = (
        (-1.5, 1.5),
        (4.05, 7.05),
        (9.6, 12.6),
    )
    carrier_race_radius_mm: float = 131.6
    tooth_tip_radius_mm: float = 129.0
    contact_land_width_mm: float = 0.6
    roller_axis_radius_mm: float = 125.5
    roller_axis_operating_tolerance_mm: float = 0.05
    spool_bore_diameter_mm: float = 4.06
    axle_finished_diameter_mm: float = 3.99
    spool_hub_od_mm: float = 6.0
    spool_running_od_mm: float = 12.1
    spool_flange_od_mm: float = 13.8
    spool_flange_thickness_mm: float = 0.5
    spool_face_clearance_mm: float = 0.15
    spool_complete_height_mm: float = 4.3
    spool_running_z_mm: tuple[float, float] = (0.75, 1.35)
    spool_upper_flange_z_mm: tuple[float, float] = (3.8, 4.3)
    spool_ranges_z_mm: tuple[tuple[float, float], ...] = (
        (-2.15, 2.15),
        (3.4, 7.7),
        (8.95, 13.25),
    )

    axle_z_mm: tuple[float, float] = (-5.0, 20.0)
    axle_nominal_diameter_mm: float = 4.0
    axle_clearance_diameter_mm: float = 4.2
    lower_socket_depth_mm: float = 1.1
    lower_post_od_mm: float = 6.0
    lower_post_top_z_mm: float = -2.45
    spacer_length_mm: float = 0.8
    spacer_od_mm: float = 6.0
    spacer_bore_mm: float = 4.2
    washer_thickness_mm: float = 0.2
    washer_od_mm: float = 6.0
    washer_bore_mm: float = 4.2
    washer_ranges_z_mm: tuple[tuple[float, float], ...] = (
        (-2.35, -2.15), (2.15, 2.35),
        (3.15, 3.35), (7.7, 7.9),
        (8.7, 8.9), (13.25, 13.45),
    )
    spacer_ranges_z_mm: tuple[tuple[float, float], ...] = ((2.35, 3.15), (7.9, 8.7))

    backbone_radius_mm: float = 110.2
    backbone_tangent_mm: tuple[float, float] = (-5.5, 5.5)
    backbone_section_mm: float = 2.5
    # Critic repair: widen the removable bridge only, preserving its outer
    # radius and every locked ring/base interface.  With the unchanged
    # R111/T+/-4.5 screw axes and D3.4 bores these limits provide 1.50 mm
    # actual ligament at both the inboard and tangential bridge edges.
    bridge_r_mm: tuple[float, float] = (107.8, 131.1)
    bridge_t_mm: tuple[float, float] = (-7.7, 7.7)
    bridge_z_mm: tuple[float, float] = (13.55, 14.85)
    bridge_screw_diameter_mm: float = 3.0
    bridge_clearance_diameter_mm: float = 3.4
    bridge_screw_length_mm: float = 6.0
    bridge_screw_radius_mm: float = 111.0
    bridge_screw_tangent_mm: tuple[float, float] = (-4.5, 4.5)
    bridge_nut_af_mm: float = 5.5
    bridge_nut_thickness_mm: float = 2.4
    collar_od_mm: float = 10.0
    collar_bore_mm: float = 4.1
    collar_z_mm: tuple[float, float] = (15.0, 19.0)

    fin_root_inner_radius_mm: float = 135.5
    minimum_fin_clearance_mm: float = 0.8
    stationary_radius_limit_mm: float = 134.7
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    u1_usable_xy_mm: float = 260.0

    @property
    def nominal_running_gap_mm(self) -> float:
        return self.carrier_race_radius_mm - (
            self.roller_axis_radius_mm + self.spool_running_od_mm / 2.0
        )

    @property
    def nominal_flange_overlap_mm(self) -> float:
        return self.roller_axis_radius_mm + self.spool_flange_od_mm / 2.0 - self.carrier_race_radius_mm

    @property
    def hub_to_tooth_clearance_worst_mm(self) -> float:
        return self.tooth_tip_radius_mm - (
            self.roller_axis_radius_mm
            + self.roller_axis_operating_tolerance_mm
            + self.spool_hub_od_mm / 2.0
        )

    @property
    def spool_fin_clearance_mm(self) -> float:
        return self.fin_root_inner_radius_mm - (
            self.roller_axis_radius_mm + self.spool_flange_od_mm / 2.0
        )

    @property
    def bridge_radial_ligament_mm(self) -> float:
        return self.bridge_screw_radius_mm - self.bridge_clearance_diameter_mm / 2.0 - self.bridge_r_mm[0]

    @property
    def bridge_tangential_ligament_mm(self) -> float:
        return self.bridge_t_mm[1] - abs(self.bridge_screw_tangent_mm[1]) - self.bridge_clearance_diameter_mm / 2.0

    @property
    def bridge_outer_corner_radius_mm(self) -> float:
        return (self.bridge_r_mm[1] ** 2 + self.bridge_t_mm[1] ** 2) ** 0.5

    @property
    def bridge_fin_clearance_lower_bound_mm(self) -> float:
        return self.fin_root_inner_radius_mm - self.bridge_outer_corner_radius_mm


SPEC = FreeRollerR0Spec()
