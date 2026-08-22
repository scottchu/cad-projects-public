"""Frozen contract for the KAGE V3 three-tower direct-spool correction.

The 2.55 mm carrier gaps cannot package 3.0 mm-wide MR84 bearings.  Each tower
therefore carries three independent POM/low-friction flanged spools directly
on one polished D4 pin.  This file intentionally defines only that architecture.
"""

from dataclasses import dataclass

from p3_v3_full_ring_r2_spec import P3V3FullRingR2Spec


@dataclass(frozen=True)
class P3V3RollerTowerSpec(P3V3FullRingR2Spec):
    roller_tower_angles: tuple[float, float, float] = (60.0, 180.0, 300.0)
    adjustable_tower_indices: tuple[int, int, int] = (0, 1, 2)

    guide_head_radii: tuple[float, float] = (132.80, 134.80)
    guide_head_depth: float = 0.80
    guide_neck_radii: tuple[float, float] = (133.60, 134.80)
    guide_neck_depth: float = 0.80
    guide_total_depth: float = 1.60

    roller_type: str = "independent_direct_running_flanged_spool"
    roller_material: str = "POM_preferred_or_low_friction_print"
    roller_bore_diameter: float = 4.20
    roller_hub_outer_diameter: float = 6.40
    roller_running_outer_diameter: float = 7.90
    roller_flange_outer_diameter: float = 9.60
    roller_flange_thickness: float = 0.60
    roller_flange_axial_clearance: float = 0.20
    roller_nominal_contact_gap: float = 0.05
    roller_axis_radius: float = 128.80
    roller_axis_adjustment: float = 0.60
    roller_center_zs: tuple[float, float, float] = (-2.70, 2.85, 8.40)
    roller_spacer_lengths: tuple[float, float] = (3.15, 3.15)
    roller_spacer_outer_diameter: float = 6.00
    roller_spacer_bore_diameter: float = 4.20
    roller_thrust_washer_thickness: float = 0.20
    roller_thrust_washer_outer_diameter: float = 6.00
    roller_thrust_washer_bore_diameter: float = 4.20
    roller_axial_tolerance: float = 0.30
    roller_capture_radial_overlap: float = 0.80

    tower_axle_nominal_diameter: float = 4.00
    tower_axle_clearance_diameter: float = 4.20
    tower_axle_z0: float = -5.00
    # D4 x 24 mm polished pin; the extra length carries a real purchased
    # 4 mm-wide shaft collar above the stationary upper bushing.
    tower_axle_length: float = 24.00
    tower_lower_socket_depth: float = 1.10
    tower_post_outer_diameter: float = 7.00
    tower_post_top_clearance: float = 0.20
    tower_upper_bushing_outer_diameter: float = 5.20
    tower_upper_bushing_bore_diameter: float = 4.20
    tower_upper_bushing_z_range: tuple[float, float] = (12.85, 14.15)
    tower_retainer_type: str = "purchased_D4_metal_set_screw_shaft_collar"
    tower_retainer_collar_outer_diameter: float = 10.00
    tower_retainer_collar_bore_diameter: float = 4.10
    tower_retainer_collar_z_range: tuple[float, float] = (14.25, 18.25)
    tower_collar_set_screw_nominal_diameter: float = 2.00
    tower_collar_set_screw_pilot_diameter: float = 1.70
    tower_collar_set_screw_length: float = 4.00
    tower_collar_min_pilot_edge_material: float = 1.00

    tower_base_radial_range: tuple[float, float] = (108.80, 133.40)
    tower_base_tangential_width: float = 14.00
    tower_base_z_range: tuple[float, float] = (-25.50, -23.50)
    tower_mount_axis_radius: float = 119.50
    tower_mount_tangent_offsets: tuple[float, float] = (-4.50, 4.50)
    tower_mount_clearance_diameter: float = 3.40
    tower_mount_bolt_diameter: float = 3.00
    tower_mount_bolt_length: float = 8.00
    tower_mount_socket_head_diameter: float = 5.50
    tower_mount_socket_head_height: float = 3.00
    tower_mount_washer_outer_diameter: float = 7.00
    tower_mount_washer_thickness: float = 0.50
    tower_mount_hex_nut_across_flats: float = 5.50
    tower_mount_hex_nut_thickness: float = 2.40
    tower_mount_tool_access_diameter: float = 8.00
    tower_preload_slot_travel: float = 1.20
    tower_backbone_radius: float = 110.20
    tower_backbone_tangent_offsets: tuple[float, float] = (-5.50, 5.50)
    tower_backbone_section: float = 2.50
    tower_top_bridge_radial_range: tuple[float, float] = (109.00, 131.10)
    tower_top_bridge_tangential_width: float = 14.00
    tower_top_bridge_z_range: tuple[float, float] = (12.85, 14.15)
    tower_stationary_radius_limit: float = 136.40
    minimum_fin_corridor_clearance: float = 0.80

    output_shaft_across_flat: float = 3.50
    output_pinion_bore_diameter: float = 4.10
    output_pinion_bore_across_flat: float = 3.60

    def guide_head_range(self, role: int) -> tuple[float, float]:
        z0 = self.carrier_layers[role][0]
        return z0 - self.guide_total_depth, z0 - self.guide_neck_depth

    def guide_neck_range(self, role: int) -> tuple[float, float]:
        z0 = self.carrier_layers[role][0]
        return z0 - self.guide_neck_depth, z0

    def roller_flange_ranges(self, role: int):
        head0, head1 = self.guide_head_range(role)
        lower_top = head0 - self.roller_flange_axial_clearance
        upper_bottom = head1 + self.roller_flange_axial_clearance
        return (
            (lower_top - self.roller_flange_thickness, lower_top),
            (upper_bottom, upper_bottom + self.roller_flange_thickness),
        )

    def roller_range(self, role: int):
        lower, upper = self.roller_flange_ranges(role)
        return lower[0], upper[1]

    def roller_running_range(self, role: int):
        return self.guide_head_range(role)

    @property
    def lower_thrust_washer_range(self):
        top = self.roller_range(0)[0]
        return top - self.roller_thrust_washer_thickness, top

    @property
    def upper_thrust_washer_range(self):
        bottom = self.roller_range(2)[1]
        return bottom, bottom + self.roller_thrust_washer_thickness

    @property
    def roller_stationary_outer_radius(self):
        return self.roller_axis_radius + self.roller_flange_outer_diameter / 2.0

    @property
    def roller_running_outer_radius(self):
        return self.roller_axis_radius + self.roller_running_outer_diameter / 2.0

    @property
    def roller_running_gap(self):
        return self.guide_head_radii[0] - self.roller_running_outer_radius

    @property
    def fin_corridor_clearance(self):
        return min(r0 for r0, _ in self.fin_blade_radial_ranges) - self.roller_stationary_outer_radius

    @property
    def adjusted_roller_axis_radius_range(self):
        return self.roller_axis_radius - self.roller_axis_adjustment, self.roller_axis_radius + self.roller_axis_adjustment


P3_V3_ROLLER_TOWER = P3V3RollerTowerSpec()
