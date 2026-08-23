"""Frozen numeric contract for the complete KAGE P3 V3 R2 mechanism.

This remains a P3 V3 subrevision.  It replaces the rejected one-station R1
coupon with three complete, independently driven stacked rings.  Units are
millimetres and degrees; XY is the clock plane and +Z faces the viewer.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class P3V3FullRingR2Spec:
    roles: tuple[str, str, str] = ("hour", "minute", "second")
    role_colors: tuple[str, str, str] = ("#3F8F87", "#E38B48", "#D95D78")
    motor_station_angles: tuple[float, float, float] = (0.0, 120.0, 240.0)
    display_fin_angles: tuple[float, float, float] = (305.0, 45.0, 145.0)

    # One coherent involute tooth system for every ring and output pinion.
    module: float = 1.0
    pressure_angle_degrees: float = 20.0
    ring_teeth: int = 260
    quadrant_teeth: int = 65
    quadrant_angle_degrees: float = 90.0
    quadrant_count: int = 4
    pinion_teeth: int = 16
    ring_pitch_radius: float = 130.0
    ring_tooth_outer_radius: float = 132.5
    ring_active_root_radius: float = 132.5
    pinion_pitch_radius: float = 8.0
    pinion_outer_radius: float = 9.0
    output_axis_radius: float = 122.0
    output_mesh_backlash: float = 0.20
    tooth_phase_offset_degrees: float = 360.0 / (2.0 * 260.0)

    # Frozen H/M/S carrier and active mesh planes.
    carrier_layers: tuple[tuple[float, float], ...] = (
        (-1.5, 1.5),
        (4.05, 7.05),
        (9.6, 12.6),
    )
    pinion_face_ranges: tuple[tuple[float, float], ...] = (
        (-0.7, 1.4),
        (4.85, 6.95),
        (10.4, 12.5),
    )
    ring_body_inner_radius: float = 131.6
    ring_body_outer_radius: float = 138.9
    ring_outer_radius: float = 140.0
    rail_neck_radii: tuple[float, float] = (133.6, 134.8)
    rail_neck_depth: float = 1.0
    rail_flange_radii: tuple[float, float] = (132.8, 135.6)
    rail_flange_depth: float = 0.8
    rail_total_depth: float = 1.8
    rail_seam_step_max: float = 0.15
    rail_seam_step: float = 0.0
    race_to_mesh_min_clearance: float = 0.20

    # Segment joints lie wholly outside the active tooth-root cylinder.
    joint_hole_radius: float = 137.4
    joint_hole_diameter: float = 2.20
    joint_hole_edge_angle_degrees: float = 1.8
    quadrant_overlap_epsilon: float = 0.02
    registration_dowel_radius: float = 137.0
    registration_dowel_diameter: float = 3.0
    splice_plate_radii: tuple[float, float] = (135.8, 138.8)
    splice_plate_radial_width: float = 3.0
    splice_plate_tangential_length: float = 12.0
    splice_plate_thickness: float = 1.0
    splice_plate_contact_width: float = 5.0
    splice_fastener_core_diameter: float = 1.6
    splice_fastener_head_diameter: float = 3.8

    # Integral roots/blades: H/M move outside the carrier stack while S grows
    # directly from its own top carrier.  There are no separate M2 fin feet.
    fin_blade_radial_ranges: tuple[tuple[float, float], ...] = (
        (142.7, 143.9),
        (140.75, 141.95),
        (137.2, 138.4),
    )
    fin_tangential_widths: tuple[float, float, float] = (3.0, 2.0, 1.2)
    fin_blade_start_zs: tuple[float, float, float] = (0.2, 5.3, 12.4)
    fin_tip_zs: tuple[float, float, float] = (17.152, 21.1867, 24.2514)
    fin_root_radial_ranges: tuple[tuple[float, float] | None, ...] = (
        (135.5, 143.9),
        (135.5, 141.95),
        None,
    )
    fin_root_z_ranges: tuple[tuple[float, float] | None, ...] = (
        (0.2, 1.6),
        (5.3, 6.7),
        None,
    )
    fin_root_tangential_width: float = 4.0
    fin_root_fillet_radius: float = 0.8

    # Segmented stationary structure; every segment fits a 270 x 270 U1 bed.
    frame_radii: tuple[float, float] = (145.0, 150.0)
    frame_z: tuple[float, float] = (-6.45, -4.05)
    chassis_radii: tuple[float, float] = (66.0, 145.0)
    chassis_z: tuple[float, float] = (-28.0, -25.5)
    printer_bed_xy: tuple[float, float] = (270.0, 270.0)
    segment_bed_margin: float = 5.0

    # Three corrected rear keeper saddles per role.  The fixed lower shoe and
    # removable upper bridge leave 0.15 mm on each face of the T flange.  This
    # is a V3 keeper correction, not a new mechanism version.
    guide_tower_angles: tuple[tuple[float, float, float], ...] = (
        (42.0, 162.0, 282.0),
        (54.0, 174.0, 294.0),
        (66.0, 186.0, 306.0),
    )
    keeper_channel_radii: tuple[float, float] = (132.55, 135.85)
    keeper_radial_clearance: float = 0.25
    keeper_lower_shoe_offsets: tuple[float, float] = (-2.75, -1.95)
    keeper_upper_bridge_offsets: tuple[float, float] = (-0.85, -0.05)
    keeper_axial_face_clearance: float = 0.15
    keeper_axial_float: float = 0.30
    keeper_capture_radial: float = 0.80
    keeper_capture_axial: float = 1.60
    keeper_structural_wall_min: float = 1.20
    keeper_tangential_width: float = 16.0
    keeper_service_radial_travel: float = 12.0
    keeper_cap_outer_radius: float = 143.0
    keeper_fastener_axis_radius: float = 139.50
    keeper_fastener_tangent_offsets: tuple[float, float] = (-4.50, 4.50)
    keeper_cap_fastener_nominal_diameter: float = 2.5
    keeper_cap_fastener_clearance_diameter: float = 2.8
    keeper_cap_screw_length: float = 10.0
    keeper_cap_button_head_diameter: float = 4.6
    keeper_cap_button_head_height: float = 1.2
    keeper_boss_outer_diameter: float = 7.0
    keeper_insert_outer_diameter: float = 3.8
    keeper_insert_length: float = 4.0
    keeper_insert_pilot_diameter: float = 3.6
    keeper_insert_pilot_depth: float = 4.2
    keeper_boss_depth: float = 4.8
    keeper_insert_engagement_min: float = 3.5
    keeper_liner_material: str = "POM/UHMW"
    keeper_pull_test_newtons: float = 5.0
    keeper_pull_test_status: str = "PENDING_PHYSICAL"
    station_support_clearance: float = 0.15

    # One removable retainer captures the outer shoulder without crossing the
    # outward fin lanes or active internal teeth.
    # Visible stationary front ring.  It is decorative/structural only; rear
    # T-rail keepers provide moving-ring retention.
    retainer_radii: tuple[float, float] = (145.0, 150.0)
    retainer_z: tuple[float, float] = (12.80, 13.80)
    retainer_overlap: float = 0.0
    retainer_endplay: float = 0.20
    retainer_fastener_angles: tuple[float, ...] = (15.0, 75.0, 135.0, 195.0, 255.0, 315.0)
    retainer_fastener_radius: float = 147.5
    retainer_clearance_hole: float = 2.2

    # Proven R1 16T:16T miter / two-MR84 / 4x40 D shaft station, translated
    # +0.50 mm radially as one rigid station.
    station_radial_translation: float = 0.50
    station_role_z_translations: tuple[float, float, float] = (-4.3, -2.15, 0.0)
    motor_face_radius: float = 111.75
    motor_face_size: float = 20.3
    motor_body_length: float = 39.3
    motor_shaft_diameter: float = 4.0
    motor_shaft_length: float = 7.0
    motor_shaft_across_flat: float = 3.5
    output_shaft_diameter: float = 4.0
    output_shaft_length: float = 40.0
    output_shaft_z: tuple[float, float] = (-25.0, 15.0)
    bearing_id: float = 4.0
    bearing_od: float = 8.0
    bearing_width: float = 3.0
    lower_bearing_range: tuple[float, float] = (-21.0, -18.0)
    upper_bearing_range: tuple[float, float] = (-3.0, 0.0)
    miter_teeth: int = 16
    miter_module: float = 1.0
    miter_face_width: float = 3.2
    miter_axis_intersection_z: float = -12.0
    miter_ratio: float = 1.0
    miter_static_gap: float = 0.071588
    motor_hub_overlap_min: float = 5.95

    @property
    def gear_ratio(self) -> float:
        return self.ring_teeth / self.pinion_teeth

    @property
    def ring_degrees_per_pinion_revolution(self) -> float:
        return 360.0 * self.pinion_teeth / self.ring_teeth

    @property
    def tooth_pitch_degrees(self) -> float:
        return 360.0 / self.ring_teeth

    @property
    def quadrant_tooth_count(self) -> int:
        return self.ring_teeth // self.quadrant_count

    @property
    def joint_inner_radius(self) -> float:
        return self.joint_hole_radius - self.joint_hole_diameter / 2.0

    def fin_local_mount_angle(self, role_index: int) -> float:
        return self.display_fin_angles[role_index] % self.quadrant_angle_degrees

    def race_range(self, role_index: int) -> tuple[float, float]:
        z0, _ = self.carrier_layers[role_index]
        return z0 - self.rail_total_depth, z0

    def race_to_mesh_clearance(self, role_index: int) -> float:
        return self.pinion_face_ranges[role_index][0] - self.race_range(role_index)[1]

    def guide_dot_top(self, role_index: int) -> float:
        return self.carrier_layers[role_index][0] + self.keeper_lower_shoe_offsets[1]

    def upper_capture_bottom(self, role_index: int) -> float:
        return self.carrier_layers[role_index][0] + self.keeper_upper_bridge_offsets[0]

    def lower_shoe_range(self, role_index: int) -> tuple[float, float]:
        z0 = self.carrier_layers[role_index][0]
        return tuple(z0 + value for value in self.keeper_lower_shoe_offsets)

    def upper_bridge_range(self, role_index: int) -> tuple[float, float]:
        z0 = self.carrier_layers[role_index][0]
        return tuple(z0 + value for value in self.keeper_upper_bridge_offsets)

    def keeper_boss_range(self, role_index: int) -> tuple[float, float]:
        top = self.upper_bridge_range(role_index)[1]
        return top - self.keeper_boss_depth, top

    @property
    def largest_quadrant_xy(self) -> float:
        return self.frame_radii[1]

    @property
    def segment_bed_limit(self) -> float:
        return min(self.printer_bed_xy) - self.segment_bed_margin

    @property
    def carrier_gaps(self) -> tuple[float, float]:
        return tuple(
            self.carrier_layers[i + 1][0] - self.carrier_layers[i][1]
            for i in range(2)
        )

    @property
    def pinion_face_widths(self) -> tuple[float, float, float]:
        return tuple(b - a for a, b in self.pinion_face_ranges)

    @property
    def full_ring_pitch_circumference(self) -> float:
        return 2.0 * pi * self.ring_pitch_radius


P3_V3_FULL_RING_R2 = P3V3FullRingR2Spec()
