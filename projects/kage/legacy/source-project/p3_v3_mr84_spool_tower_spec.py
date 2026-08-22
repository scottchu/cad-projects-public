"""Frozen contract for the KAGE V3 MR84/profiled-spool tower successor."""

from __future__ import annotations

from dataclasses import dataclass

from p3_v3_full_ring_r2_spec import P3V3FullRingR2Spec


@dataclass(frozen=True)
class P3V3MR84SpoolTowerSpec(P3V3FullRingR2Spec):
    roller_tower_angles: tuple[float, float, float] = (60.0, 180.0, 300.0)
    fixed_tower_indices: tuple[int, int] = (0, 1)
    adjustable_tower_index: int = 2

    bearing_code: str = "MR84ZZ"
    bearing_bore_diameter: float = 4.00
    bearing_outer_diameter: float = 8.00
    bearing_width: float = 3.00
    roller_center_zs: tuple[float, float, float] = (-2.90, 2.65, 8.20)
    axle_axis_radius: float = 126.40
    adjustable_axis_radius_range: tuple[float, float] = (126.35, 126.45)
    fixed_axis_radial_tolerance: float = 0.05

    spool_hub_outer_diameter: float = 10.00
    spool_hub_bore_diameter: float = 8.10
    spool_hub_width: float = 3.20
    spool_belt_outer_diameter: float = 12.60
    spool_belt_width: float = 0.60
    spool_lip_outer_diameter: float = 14.40
    spool_lower_lip_offsets: tuple[float, float] = (-0.95, -0.55)
    spool_upper_lip_offsets: tuple[float, float] = (0.55, 1.15)
    spool_groove_width: float = 1.10
    spool_capture_overlap: float = 0.80
    spool_axial_float: float = 0.15
    spool_material: str = "POM_or_low_friction_print"

    spacer_lengths: tuple[float, float] = (2.55, 2.55)
    spacer_outer_diameter: float = 6.00
    spacer_bore_diameter: float = 4.10
    shim_thickness: float = 0.20
    shim_outer_diameter: float = 6.00
    shim_bore_diameter: float = 4.10

    axle_shoulder_diameter: float = 3.985
    axle_z_range: tuple[float, float] = (-5.60, 15.80)
    axle_internal_thread_diameter: float = 3.00
    axle_thread_z_range: tuple[float, float] = (14.50, 15.80)
    lower_socket_bore_diameter: float = 4.10
    lower_socket_z_range: tuple[float, float] = (-5.70, -4.60)
    upper_bushing_outer_diameter: float = 5.20
    upper_bushing_bore_diameter: float = 4.10
    upper_bushing_z_range: tuple[float, float] = (12.80, 15.80)
    upper_stack_shoulder_outer_diameter: float = 6.00
    upper_stack_shoulder_z_range: tuple[float, float] = (9.90, 10.30)
    retainer_outer_diameter: float = 6.40
    retainer_thread_diameter: float = 3.00
    retainer_head_z_range: tuple[float, float] = (16.00, 17.60)

    base_radial_range: tuple[float, float] = (108.80, 133.40)
    base_tangential_width: float = 14.00
    base_z_range: tuple[float, float] = (-25.50, -23.50)
    base_mount_axis_radius: float = 119.50
    base_mount_tangent_offsets: tuple[float, float] = (-4.50, 4.50)
    base_mount_clearance_diameter: float = 3.40
    base_mount_bolt_diameter: float = 3.00
    base_mount_bolt_length: float = 10.00
    adjustable_slot_travel: float = 0.10
    post_outer_diameter: float = 7.00
    backbone_radius: float = 110.20
    backbone_tangent_offsets: tuple[float, float] = (-5.50, 5.50)
    backbone_section: float = 2.50
    column_top_z: float = 12.80
    yoke_radial_range: tuple[float, float] = (109.00, 128.90)
    yoke_tangential_width: float = 17.00
    yoke_z_range: tuple[float, float] = (12.80, 15.80)
    yoke_fastener_axis_radius: float = 110.20
    yoke_fastener_tangent_offsets: tuple[float, float] = (-5.50, 5.50)
    yoke_clearance_diameter: float = 3.40
    yoke_bolt_diameter: float = 3.00
    yoke_bolt_length: float = 8.00
    stationary_radius_limit: float = 136.40
    minimum_fin_clearance: float = 0.80

    output_shaft_across_flat: float = 3.50
    output_pinion_bore_diameter: float = 4.10
    output_pinion_bore_across_flat: float = 3.60

    @property
    def spool_outer_radius(self) -> float:
        return self.axle_axis_radius + self.spool_lip_outer_diameter / 2.0

    @property
    def nominal_running_gap(self) -> float:
        return self.rail_flange_radii[0] - (
            self.axle_axis_radius + self.spool_belt_outer_diameter / 2.0
        )

    @property
    def adjustable_running_gap_range(self) -> tuple[float, float]:
        belt_radius = self.spool_belt_outer_diameter / 2.0
        return tuple(
            self.rail_flange_radii[0] - (axis + belt_radius)
            for axis in reversed(self.adjustable_axis_radius_range)
        )

    @property
    def fin_clearance(self) -> float:
        return min(r0 for r0, _ in self.fin_blade_radial_ranges) - self.spool_outer_radius

    def flange_range(self, role_index: int) -> tuple[float, float]:
        z0, _ = self.race_range(role_index)
        return z0, z0 + self.rail_flange_depth

    def bearing_range(self, role_index: int) -> tuple[float, float]:
        center = self.roller_center_zs[role_index]
        return center - self.bearing_width / 2.0, center + self.bearing_width / 2.0

    def hub_range(self, role_index: int) -> tuple[float, float]:
        center = self.roller_center_zs[role_index]
        return center - self.spool_hub_width / 2.0, center + self.spool_hub_width / 2.0

    def belt_range(self, role_index: int) -> tuple[float, float]:
        center = self.roller_center_zs[role_index]
        return center - self.spool_belt_width / 2.0, center + self.spool_belt_width / 2.0

    def lip_ranges(self, role_index: int) -> tuple[tuple[float, float], tuple[float, float]]:
        center = self.roller_center_zs[role_index]
        return (
            tuple(center + value for value in self.spool_lower_lip_offsets),
            tuple(center + value for value in self.spool_upper_lip_offsets),
        )

    def spacer_range(self, spacer_index: int) -> tuple[float, float]:
        z0 = self.bearing_range(spacer_index)[1]
        return z0, z0 + self.spacer_lengths[spacer_index]

    @property
    def lower_shim_range(self) -> tuple[float, float]:
        z1 = self.bearing_range(0)[0]
        return z1 - self.shim_thickness, z1

    @property
    def upper_shim_range(self) -> tuple[float, float]:
        z0 = self.bearing_range(2)[1]
        return z0, z0 + self.shim_thickness


P3_V3_MR84_SPOOL_TOWER = P3V3MR84SpoolTowerSpec()
