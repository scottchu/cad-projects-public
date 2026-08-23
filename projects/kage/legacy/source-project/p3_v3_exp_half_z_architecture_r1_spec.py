"""Numeric contract for the isolated KAGE half-Z architecture experiment.

This is communication geometry only.  It deliberately leaves the accepted
locked direct-gear-race model immutable.  Architecture D is the repair target;
architecture E is retained only as a rejected comparison:

* D -- the locked M1 260T/16T radial transmission in three compressed planes;
* E -- rejected three-independent-lane comparison, not a release candidate.

Units are millimetres.  XY is the clock plane and +Z faces the viewer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class P3V3HalfZArchitectureR1Spec:
    artifact_slug: str = "p3_v3_exp_half_z_architecture_r1"
    locked_step_sha256: str = "dea274f64bdc841e77d75fda9d4e0638a9627a599d13295cb78b0ec1bd6997a7"
    locked_step_relative: str = (
        "models/p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818/"
        "p3_v3_direct_gear_race_assembled.step"
    )

    roles: tuple[str, str, str] = ("hour", "minute", "second")
    role_colors: tuple[str, str, str] = ("#148F88", "#F09A35", "#E84A8A")
    motor_station_angles: tuple[float, float, float] = (0.0, 120.0, 240.0)
    display_fin_angles: tuple[float, float, float] = (305.0, 45.0, 145.0)

    module: float = 1.0
    pinion_teeth: int = 16
    ring_thickness: float = 2.65
    axial_gap: float = 0.35
    backlash: float = 0.20
    pressure_angle_degrees: float = 20.0
    pinion_pitch_radius: float = 8.0
    pinion_tip_radius: float = 9.0

    plate_outer_radius: float = 150.0
    plate_z: tuple[float, float] = (-6.0, 0.0)
    plate_color: str = "#B9B5A8"
    motor_body_length: float = 39.3
    motor_face_size: float = 20.3
    motor_shaft_diameter: float = 4.0
    motor_shaft_across_flat: float = 3.5
    motor_shaft_gap_to_output_axis: float = 10.0
    motor_mount_pitch: float = 15.4
    motor_face_thread: str = "M2"
    motor_face_clearance_diameter: float = 2.20
    motor_face_thread_depth: float = 2.50
    motor_yoke_radial_thickness: float = 1.80
    motor_yoke_center_clearance_radius: float = 9.10
    motor_cradle_side_thickness: float = 2.0
    motor_cradle_running_clearance: float = 0.30
    motor_chassis_screw_diameter: float = 3.20
    motor_chassis_screw_pitch_y: float = 30.0
    motor_chassis_screw_radius: float = 117.0
    output_shaft_diameter: float = 4.0
    representative_fastener_diameter: float = 2.4
    representative_fastener_head_diameter: float = 5.0

    # D -- compressed version of the locked architecture.
    d_carrier_layers: tuple[tuple[float, float], ...] = (
        (0.80, 3.45),
        (3.80, 6.45),
        (6.80, 9.45),
    )
    d_ring_teeth: int = 260
    d_ring_pitch_radius: float = 130.0
    d_ring_body_inner_radius: float = 131.6
    d_ring_body_outer_radius: float = 138.9
    d_output_axis_radius: float = 122.0
    d_fin_radii: tuple[float, float, float] = (143.1, 139.9, 136.7)
    d_fin_tip_zs: tuple[float, float, float] = (8.873, 11.074, 12.646)
    d_motor_z: tuple[float, float] = (-18.5, 1.8)
    d_rear_limit_z: float = -19.2
    d_plate_inner_radius: float = 66.0
    d_guide_angles: tuple[float, float, float] = (60.0, 180.0, 300.0)
    d_guide_axis_radius: float = 125.5
    d_guide_shaft_z: tuple[float, float] = (-5.20, 10.40)
    d_guide_shaft_diameter: float = 4.0
    d_guide_spool_bore_diameter: float = 4.2
    d_guide_rear_collar_diameter: float = 6.0
    d_guide_rear_collar_z: tuple[float, float] = (-5.20, -4.40)
    d_guide_rear_counterbore_diameter: float = 6.2
    d_guide_rear_counterbore_z: tuple[float, float] = (-6.20, -4.40)
    d_guide_chassis_boss_diameter: float = 9.0
    d_guide_chassis_boss_z: tuple[float, float] = (-1.20, 0.65)
    d_guide_anchor_screw_diameter: float = 2.00
    d_guide_keeper_cap_diameter: float = 8.0
    d_guide_keeper_cap_z: tuple[float, float] = (10.40, 11.20)
    d_guide_running_diameter: float = 12.1
    d_guide_hub_diameter: float = 6.0
    d_guide_flange_diameter: float = 13.8
    d_guide_flange_thickness: float = 0.50
    d_guide_flange_axial_clearance: float = 0.15
    d_guide_running_z_offset: tuple[float, float] = (0.10, 0.70)
    d_tooth_free_race_depth: float = 0.80
    d_tooth_tip_radius: float = 129.0
    d_carrier_race_radius: float = 131.60
    d_led_source_to_mask: float = 20.75
    d_optical_clearance_risk: float = 8.10
    d_expected_z_envelope: float = 31.846
    d_miter_teeth: int = 16
    d_miter_module: float = 1.0
    d_miter_face_width: float = 3.2
    d_miter_reference_axis_radius: float = 121.5
    d_miter_reference_intersection_z: float = -12.0
    d_led_keepout_bottom_z: float = 0.0
    d_led_keepout_top_z: float = 20.75
    d_led_keepout_bottom_radius: float = 61.0
    d_led_keepout_top_radius: float = 10.0

    # E -- mechanically valid coplanar radial lanes.
    e_carrier_layer: tuple[float, float] = (0.80, 3.45)
    e_ring_teeth: tuple[int, int, int] = (270, 216, 162)
    e_pitch_radii: tuple[float, float, float] = (135.0, 108.0, 81.0)
    e_radial_envelopes: tuple[tuple[float, float], ...] = (
        (134.0, 143.9),
        (107.0, 116.9),
        (80.0, 89.9),
    )
    e_pinion_axis_radii: tuple[float, float, float] = (127.0, 100.0, 73.0)
    e_pinion_tip_envelopes: tuple[tuple[float, float], ...] = (
        (118.0, 136.0),
        (91.0, 109.0),
        (64.0, 82.0),
    )
    e_fin_radii: tuple[float, float, float] = (142.5, 115.5, 88.5)
    e_fin_tip_zs: tuple[float, float, float] = (6.880, 9.840, 11.954)
    e_motor_z: tuple[float, float] = (-20.0, 0.3)
    e_rear_limit_z: float = -20.0
    e_plate_inner_radius: float = 10.0
    e_guide_angles: tuple[float, float, float] = (60.0, 180.0, 300.0)
    e_spool_center_radii: tuple[float, float, float] = (146.55, 119.55, 92.55)
    e_spool_running_diameter: float = 5.0
    e_spool_flange_diameter: float = 6.0
    e_spool_groove_width: float = 2.95
    e_spool_flange_thickness: float = 0.15
    e_spool_outer_radius: float = 149.55
    e_guide_bar_z: tuple[float, float] = (-0.40, 0.50)
    e_led_source_to_mask: float = 16.0
    e_optical_clearance_risk: float = 4.046
    e_expected_z_envelope: float = 31.954

    fin_radial_thickness: float = 1.20
    fin_tangential_widths: tuple[float, float, float] = (3.0, 2.0, 1.2)
    fin_root_tangential_width: float = 4.0

    @property
    def root(self) -> Path:
        return ROOT

    @property
    def model_root(self) -> Path:
        return ROOT / "models" / self.artifact_slug

    @property
    def snapshot_root(self) -> Path:
        return self.model_root / "snapshots"

    @property
    def locked_step(self) -> Path:
        return ROOT / self.locked_step_relative

    @property
    def d_pinion_axes(self) -> tuple[float, float, float]:
        return (self.d_output_axis_radius,) * 3

    @property
    def d_pitch_radii(self) -> tuple[float, float, float]:
        return (self.d_ring_pitch_radius,) * 3

    @property
    def d_ring_teeth_by_role(self) -> tuple[int, int, int]:
        return (self.d_ring_teeth,) * 3

    @property
    def d_actual_z_envelope(self) -> float:
        return max(self.d_fin_tip_zs) - self.d_rear_limit_z

    @property
    def d_motor_center_z(self) -> float:
        return sum(self.d_motor_z) / 2.0

    @property
    def d_miter_translation_x(self) -> float:
        return self.d_output_axis_radius - self.d_miter_reference_axis_radius

    @property
    def d_miter_translation_z(self) -> float:
        return self.d_motor_center_z - self.d_miter_reference_intersection_z

    def d_pinion_face_range(self, role_index: int) -> tuple[float, float]:
        """Active mesh starts above the locked 0.80 mm smooth race land."""

        z0, z1 = self.d_carrier_layers[role_index]
        return z0 + self.d_tooth_free_race_depth, z1

    @property
    def e_actual_z_envelope(self) -> float:
        return max(self.e_fin_tip_zs) - self.e_rear_limit_z

    def validate(self) -> None:
        assert self.ring_thickness == 2.65
        assert all(abs((b - a) - self.ring_thickness) < 1e-9 for a, b in self.d_carrier_layers)
        assert all(
            abs(self.d_carrier_layers[i + 1][0] - self.d_carrier_layers[i][1] - self.axial_gap) < 1e-9
            for i in range(2)
        )
        assert all(
            abs(pitch - axis - self.pinion_pitch_radius) < 1e-9
            for pitch, axis in zip(self.e_pitch_radii, self.e_pinion_axis_radii)
        )
        assert abs(
            max(self.e_spool_center_radii) + self.e_spool_flange_diameter / 2.0
            - self.e_spool_outer_radius
        ) < 1e-9
        assert abs(self.d_actual_z_envelope - self.d_expected_z_envelope) < 1e-9
        assert abs(self.e_actual_z_envelope - self.e_expected_z_envelope) < 1e-9
        assert abs(self.d_motor_center_z + 8.35) < 1e-9
        assert abs(self.d_miter_translation_x - 0.5) < 1e-9
        assert abs(self.d_miter_translation_z - 3.65) < 1e-9
        assert self.d_guide_shaft_z[0] < self.plate_z[0] + 1.0
        assert self.d_guide_keeper_cap_z[0] == self.d_guide_shaft_z[1]
        assert abs(
            self.d_carrier_race_radius
            - (self.d_guide_axis_radius + self.d_guide_running_diameter / 2.0)
            - 0.05
        ) < 1e-9
        assert (
            self.d_guide_axis_radius
            + self.d_guide_hub_diameter / 2.0
            <= self.d_tooth_tip_radius - 0.50
        )


P3_V3_EXP_HALF_Z_ARCHITECTURE_R1 = P3V3HalfZArchitectureR1Spec()
P3_V3_EXP_HALF_Z_ARCHITECTURE_R1.validate()
