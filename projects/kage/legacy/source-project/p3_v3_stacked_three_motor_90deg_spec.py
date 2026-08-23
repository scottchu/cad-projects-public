"""Frozen P3 V3 stacked three-motor 90-degree-drive visualization contract.

XY is the clock plane, +Z faces the viewer, and -Z faces the wall.  Purchased
parts and miter geometry are provisional envelopes until physical measurement
and coupon testing; the equations and interface datums are frozen here.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class P3V3StackedThreeMotor90DegSpec:
    roles: tuple[str, str, str] = ("hour", "minute", "second")
    role_colors: tuple[str, str, str] = ("#3F8F87", "#E38B48", "#D95D78")
    motor_station_angles: tuple[float, float, float] = (0.0, 120.0, 240.0)
    display_fin_angles: tuple[float, float, float] = (305.0, 45.0, 145.0)

    frame_radii: tuple[float, float] = (141.0, 150.0)
    frame_z: tuple[float, float] = (0.0, 2.4)
    carrier_nominal_radius: float = 133.0
    carrier_radii: tuple[float, float] = (130.5, 135.5)
    carrier_layers: tuple[tuple[float, float], ...] = (
        (2.8, 5.8),
        (6.2, 9.2),
        (9.6, 12.6),
    )
    carrier_axial_gap: float = 0.40

    internal_gear_module: float = 1.0
    internal_gear_teeth: int = 259
    internal_pitch_radius: float = 129.5
    internal_tip_radius: float = 128.5
    internal_root_radius: float = 130.75
    internal_join_overlap: float = 0.25
    tooth_thickness_backlash: float = 0.15

    pinion_teeth: int = 12
    pinion_pitch_radius: float = 6.0
    pinion_outer_radius: float = 7.0
    pinion_root_radius: float = 4.75
    pinion_face_width: float = 2.8
    # Phase angles minimize the simplified involute-envelope subtraction at
    # each 0/120/240 degree drive station.  The final pinion is trimmed against
    # its own 259T carrier, leaving a zero-volume pitch-contact boundary.
    pinion_phase_angles: tuple[float, float, float] = (15.0, 5.0, 25.0)
    pinion_bore_radius: float = 2.2
    output_axis_radius: float = 123.5
    output_shaft_diameter: float = 4.2
    output_shaft_z: tuple[float, float] = (-13.5, 13.0)

    motor_step_degrees: float = 1.8
    microsteps: int = 16
    motor_keepout: tuple[float, float, float] = (20.6, 20.6, 39.3)
    motor_shaft_diameter: float = 4.0
    motor_shaft_length: float = 10.0
    motor_shaft_center_z: float = -12.8
    motor_body_z: tuple[float, float] = (-23.1, -2.5)
    motor_face_radius: float = 113.5
    motor_inward_radius: float = 74.2

    miter_module: float = 0.8
    miter_teeth: int = 10
    miter_pitch_diameter: float = 8.0
    miter_outer_diameter: float = 9.6
    miter_envelope_radius: float = 4.8
    miter_face_width: float = 2.4
    miter_ratio: float = 1.0

    rear_plane_z: float = -25.5
    upper_bearing_support_z: tuple[float, float] = (-2.3, -0.3)
    # Both supports sit above the bevel junction.  The previous -10..-8 plate
    # clipped the horizontal miter envelope and has been rejected.
    lower_bearing_support_z: tuple[float, float] = (-7.5, -5.5)
    bearing_outer_radius: float = 4.0
    bearing_bore_radius: float = 2.2
    bearing_plate_radii: tuple[float, float] = (118.0, 128.0)
    shaft_envelope_clearance: float = 0.10

    # Radial order is intentionally independent from axial stack order:
    #   hour/green/bottom  = outermost lane,
    #   minute/orange/mid = middle lane,
    #   second/red/top    = directly on the carrier outer band.
    # This keeps both lower stalks outside every carrier above them.  At a
    # coincident clock angle the 1.20 mm lanes retain 0.40 mm clear gaps.
    fin_lane_centers: tuple[float, float, float] = (138.1, 136.5, 134.9)
    fin_radial_width: float = 1.2
    fin_tangential_widths: tuple[float, float, float] = (3.0, 2.0, 1.2)
    fin_bases: tuple[float, float, float] = (2.8, 6.2, 12.4)
    direct_top_fin_role: int = 2
    direct_top_fin_penetration: float = 0.20
    root_arm_thickness: float = 0.8
    root_arm_inner_radius: float = 135.1
    root_carrier_overlap: float = 0.4
    common_visible_fin_base_z: float = 12.6

    source_z: float = 40.0
    target_tip_radii: tuple[float, float, float] = (250.0, 300.0, 350.0)
    legacy_v2_fin_heights: tuple[float, float, float] = (48.0, 55.0, 62.0)

    @property
    def carrier_layer_thickness(self) -> float:
        return self.carrier_layers[0][1] - self.carrier_layers[0][0]

    @property
    def carrier_stack_height(self) -> float:
        return self.carrier_layers[-1][1] - self.carrier_layers[0][0]

    @property
    def gear_ratio(self) -> float:
        return self.internal_gear_teeth / self.pinion_teeth

    @property
    def carrier_full_step_degrees(self) -> float:
        return self.motor_step_degrees / self.gear_ratio

    @property
    def carrier_microstep_degrees(self) -> float:
        return self.carrier_full_step_degrees / self.microsteps

    @property
    def seconds_motor_rpm(self) -> float:
        return self.gear_ratio

    @property
    def seconds_microsteps_per_second(self) -> float:
        return (360.0 / self.motor_step_degrees * self.microsteps) * self.seconds_motor_rpm / 60.0

    @property
    def shaft_to_non_driven_tooth_clearance(self) -> float:
        return self.internal_tip_radius - (self.output_axis_radius + self.output_shaft_diameter / 2.0)

    @property
    def miter_outer_radius(self) -> float:
        return self.output_axis_radius + self.miter_envelope_radius

    @property
    def motor_far_outer_corner_radius(self) -> float:
        radial_half = (self.motor_face_radius - self.motor_inward_radius) / 2.0
        center_radius = (self.motor_face_radius + self.motor_inward_radius) / 2.0
        tangential_half = self.motor_keepout[0] / 2.0
        return ((center_radius + radial_half) ** 2 + tangential_half**2) ** 0.5

    @property
    def total_rear_depth(self) -> float:
        return -self.rear_plane_z

    @property
    def rear_to_top_carrier(self) -> float:
        return -self.rear_plane_z + self.carrier_layers[-1][1]

    @property
    def fin_lane_gaps(self) -> tuple[float, float, float, float]:
        half = self.fin_radial_width / 2.0
        return (
            self.carrier_radii[1] - self.direct_top_fin_footprint_radii[1],
            self.fin_lane_centers[1] - half - self.direct_top_fin_footprint_radii[1],
            self.fin_lane_centers[0] - half - (self.fin_lane_centers[1] + half),
            self.frame_radii[0] - (self.fin_lane_centers[0] + half),
        )

    @property
    def direct_top_fin_footprint_radii(self) -> tuple[float, float]:
        center = self.fin_lane_centers[self.direct_top_fin_role]
        half = self.fin_radial_width / 2.0
        return center - half, center + half

    @property
    def direct_top_carrier_top_z(self) -> float:
        return self.carrier_layers[self.direct_top_fin_role][1]

    @property
    def direct_top_fin_base_z(self) -> float:
        return self.direct_top_carrier_top_z - self.direct_top_fin_penetration

    def projected_radius(self, radius: float, z: float) -> float:
        return radius * self.source_z / (self.source_z - z)

    def tip_z(self, role_index: int) -> float:
        return self.source_z * (1.0 - self.fin_lane_centers[role_index] / self.target_tip_radii[role_index])

    @property
    def fin_tip_zs(self) -> tuple[float, float, float]:
        return tuple(self.tip_z(i) for i in range(3))

    @property
    def fin_heights(self) -> tuple[float, float, float]:
        return tuple(tip - base for tip, base in zip(self.fin_tip_zs, self.fin_bases))

    @property
    def visible_fin_heights(self) -> tuple[float, float, float]:
        """Blade exposed beyond the complete three-ring stack."""

        return tuple(tip - self.common_visible_fin_base_z for tip in self.fin_tip_zs)

    @property
    def stalk_heights_to_common_datum(self) -> tuple[float, float, float]:
        """Outboard support below the common visible-blade datum."""

        return tuple(self.common_visible_fin_base_z - base for base in self.fin_bases)

    @property
    def fin_above_own_carrier_top_heights(self) -> tuple[float, float, float]:
        """Exposed height measured from each moving ring's own top face."""

        return tuple(tip - layer[1] for tip, layer in zip(self.fin_tip_zs, self.carrier_layers))

    @property
    def projected_base_radii(self) -> tuple[float, float, float]:
        """First visible wall radius after each opaque carrier occludes its fin root."""

        return tuple(
            self.projected_radius(radius, layer[1])
            for radius, layer in zip(self.fin_lane_centers, self.carrier_layers)
        )

    @property
    def shadow_occlusion_top_zs(self) -> tuple[float, float, float]:
        """Opaque carrier top planes that hide each fin's embedded root."""

        return tuple(layer[1] for layer in self.carrier_layers)

    @property
    def projected_shadow_lengths(self) -> tuple[float, float, float]:
        return tuple(target - base for target, base in zip(self.target_tip_radii, self.projected_base_radii))

    @property
    def led_nearest_tip_gap(self) -> float:
        return self.source_z - max(self.fin_tip_zs)

    @property
    def fin_reduction_percentages(self) -> tuple[float, float, float]:
        return tuple((1.0 - new / old) * 100.0 for new, old in zip(self.fin_heights, self.legacy_v2_fin_heights))

    @property
    def internal_material_tooth_thickness(self) -> float:
        return pi * self.internal_gear_module / 2.0 - self.tooth_thickness_backlash


P3_V3 = P3V3StackedThreeMotor90DegSpec()


P3_V2_ISOLATION_SHA256 = {
    "p3_v2_three_ring_comparison_spec.py": "6b37c1c26f9322213e1e7c6725d9268020c9a52d260902efb147d77b79ea7457",
    "p3_v2_three_ring_comparison_geometry.py": "59fc56068735384961ba4a74564e10faf84fc465b7869de749619b40fd07504a",
    "p3_v2_three_ring_comparison_export.py": "bce5a6ba6d6e5a16a1e6f4011c0c59d163f56fc4b9a806515a9adbca9ee565f7",
    "tests/test_p3_v2_three_ring_comparison.py": "62f9d15ea984dbd49b2af4f4a1dc4b05102c4274394522bee5db0f2b3aa84c28",
    "models/p3_v2_three_ring_comparison/p3_v2_concentric_three_ring.step": "a8a735c9e2a42a88c8a99deac4fc4ced0ec29c29938d86838dac42e1a4151b48",
    "models/p3_v2_three_ring_comparison/p3_v2_side_by_side_comparison.step": "7bd40a5907ba5b9c7c5393acbf750a858d1ef2ee835baa43cf51da00d4ae06d1",
    "models/p3_v2_three_ring_comparison/p3_v2_stacked_three_ring.step": "28bd4b05b7206079f4ce9d3cff9840dd5d01660926534d7069a0af969151b324",
    "models/p3_v2_three_ring_comparison/p3_v2_concentric_three_ring.step.py": "a14cdb5d6169c317d0226ae9b5e57ecc953588b7122dd860db5a5662596c9336",
    "models/p3_v2_three_ring_comparison/p3_v2_side_by_side_comparison.step.py": "de07700efdef4bfea296f2955f2ed87ab68952433cd50f1486651774c3ecdfa8",
    "models/p3_v2_three_ring_comparison/p3_v2_stacked_three_ring.step.py": "006725648b798c234daf89347cf272ba4d38915636ab7424f1e5d7356c888d6e",
    "models/p3_v2_three_ring_comparison/snapshots/p3_v2_comparison_iso_20260815T015141Z.png": "701864a33636bf1a47db1e79faa6cfbe6031956ebb1bc9d842423e3695ce11b5",
    "models/p3_v2_three_ring_comparison/snapshots/p3_v2_comparison_top_20260815T015142Z.png": "9e19fa70993fcdf4c5c7b3e8cdffc3c9cae169c3bd92a950a9dbcb0f6b415946",
    "models/p3_v2_three_ring_comparison/snapshots/p3_v2_concentric_iso_20260815T015139Z.png": "687a147ec17b7ae191d4724efc92fbb8ef39971b79b2831cdffd44288e55f3e7",
    "models/p3_v2_three_ring_comparison/snapshots/p3_v2_concentric_top_20260815T015140Z.png": "0d18ef9fb85cd71df6ba0c01b4f77e5e4514b99fd2f928489153a58ce53b2d23",
    "models/p3_v2_three_ring_comparison/snapshots/p3_v2_stacked_front_20260815T015137Z.png": "d2df73f89024e994659177d578ace6114121e0b9e7101f3c57871e616038821c",
    "models/p3_v2_three_ring_comparison/snapshots/p3_v2_stacked_iso_20260815T015119Z.png": "1cacb73af9548f86d96ae6d02de63bc88ccceddac3658867779a339b1f7ab04a",
}


def validate_spec(p: P3V3StackedThreeMotor90DegSpec = P3_V3) -> None:
    assert p.frame_radii == (141.0, 150.0) and p.frame_z == (0.0, 2.4)
    assert p.carrier_layers == ((2.8, 5.8), (6.2, 9.2), (9.6, 12.6))
    assert p.carrier_layer_thickness == 3.0 and abs(p.carrier_stack_height - 9.8) < 1e-9
    assert all(abs(actual - expected) < 1e-9 for actual, expected in zip(p.fin_lane_gaps, (0.0, 0.4, 0.4, 2.3)))
    assert p.direct_top_fin_footprint_radii == (134.3, 135.5)
    assert abs(p.direct_top_fin_base_z - 12.4) < 1e-9
    assert abs(p.gear_ratio - 21.583333333333332) < 1e-12
    assert abs(p.carrier_full_step_degrees - 0.0833976833976834) < 1e-12
    assert abs(p.carrier_microstep_degrees - 0.005212355212355213) < 1e-12
    assert abs(p.seconds_microsteps_per_second - 1151.111111111111) < 1e-9
    assert abs(p.shaft_to_non_driven_tooth_clearance - 2.9) < 1e-9
    assert abs(p.miter_outer_radius - 128.3) < 1e-9
    assert p.total_rear_depth == 25.5 and abs(p.rear_to_top_carrier - 38.1) < 1e-9
    assert p.fin_lane_centers == (138.1, 136.5, 134.9)
    assert p.common_visible_fin_base_z == p.carrier_layers[-1][1]
    for actual, expected in zip(p.fin_tip_zs, (17.904, 21.8, 24.582857142857144)):
        assert abs(actual - expected) < 1e-9
    for actual, expected in zip(p.fin_heights, (15.104, 15.600000000000001, 12.182857142857145)):
        assert abs(actual - expected) < 1e-9
    assert max(p.fin_above_own_carrier_top_heights) - min(p.fin_above_own_carrier_top_heights) < 0.7
    assert p.led_nearest_tip_gap > 15.4171


validate_spec()
