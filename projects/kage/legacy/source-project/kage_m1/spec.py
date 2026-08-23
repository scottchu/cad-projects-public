"""Frozen named parameters for the KAGE M1 mechanics-only prototype."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, tan, radians
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PASSIVE_NAMESPACE = "KAGE_M1_PASSIVE_R0"
MOTOR_NAMESPACE = "KAGE_M1B_MOTOR_MESH_R0"
PASSIVE_ROOT = PROJECT_ROOT / "models" / PASSIVE_NAMESPACE
MOTOR_ROOT = PROJECT_ROOT / "models" / MOTOR_NAMESPACE


@dataclass(frozen=True)
class RoleSpec:
    name: str
    body_z0: float
    body_z1: float
    race_z1: float
    relief_z1: float
    fin_width: float
    fin_z1: float
    pad_r0: float
    pad_r1: float
    pad_z0: float
    pad_z1: float
    color: str

    @property
    def body_height(self) -> float:
        return self.body_z1 - self.body_z0


@dataclass(frozen=True)
class KageM1Spec:
    namespace: str = PASSIVE_NAMESPACE
    base_outer_radius: float = 150.0
    base_inner_radius: float = 66.0
    base_thickness: float = 6.0
    base_seams: tuple[float, ...] = (45.0, 135.0, 225.0, 315.0)
    base_lap_r0: float = 70.0
    base_lap_r1: float = 116.0
    base_lap_half_t: float = 13.0
    base_lap_split_z: float = 3.0
    base_lap_edge_clearance: float = 0.2
    base_screw_radii: tuple[float, ...] = (82.0, 104.0)
    m3_clearance_diameter: float = 3.4
    m3_head_diameter: float = 5.7
    m3_head_depth: float = 3.0
    m3_nut_af: float = 5.8
    m3_nut_depth: float = 2.6
    bottom_skin: float = 0.4
    gear_module: float = 1.0
    pressure_angle_deg: float = 20.0
    ring_teeth: int = 258
    sector_teeth: int = 86
    ring_pitch_radius: float = 129.0
    ring_tip_radius: float = 128.0
    ring_root_radius: float = 131.5
    race_radius: float = 127.6
    ring_outer_radius: float = 138.5
    tooth_phase_deg: float = 360.0 / (2.0 * 258.0)
    sector_span_deg: float = 120.0
    sector_start_deg: float = -60.0
    fin_r0: float = 134.5
    fin_r1: float = 138.5
    fin_angle_deg: float = 0.0
    fin_root_fillet: float = 0.6
    lap_window: float = 12.0
    lap_half: float = 6.0
    seam_clearance_total: float = 0.30
    pad_radial_width: float = 7.0
    pad_tangential_length: float = 12.0
    minute_neck_r0: float = 138.1
    minute_neck_r1: float = 139.3
    minute_neck_z0: float = 32.2
    minute_neck_z1: float = 34.9
    joint_screw_radius: float = 135.2
    tower_angles: tuple[float, ...] = (0.0, 120.0, 240.0)
    tower_axle_radius: float = 115.9
    roller_tread_radius: float = 11.6
    roller_flange_radius: float = 13.0
    radial_gap: float = 0.10
    flange_overlap: float = 1.30
    trim_total: float = 0.8
    tower_foot_z0: float = 6.0
    tower_foot_z1: float = 18.0
    tower_foot_r0: float = 108.0
    tower_foot_r1: float = 124.0
    tower_foot_half_t: float = 10.0
    tower_mount_t: tuple[float, ...] = (-6.0, 6.0)
    tower_axle_under_head_z: float = 18.0
    roller_bore_diameter: float = 3.4
    washer_z: tuple[tuple[float, float], ...] = (
        (26.4, 26.9), (31.1, 31.6), (35.5, 36.0), (39.6, 40.1)
    )
    roller_z: tuple[tuple[float, float], ...] = (
        (26.9, 31.1), (31.6, 35.5), (36.0, 39.6)
    )
    roller_groove_z: tuple[tuple[float, float], ...] = (
        (27.4, 30.6), (32.1, 35.0), (36.5, 39.1)
    )
    u1_xy: float = 270.0
    brim: float = 5.0
    boolean_overshoot: float = 0.2
    mesh_linear_deflection: float = 0.10
    mesh_angular_deflection: float = 0.15

    roles: tuple[RoleSpec, ...] = (
        RoleSpec("hour", 27.5, 30.5, 28.7, 28.9, 5.0, 32.0,
                 131.7, 138.7, 21.1, 30.5, "#D84C3E"),
        RoleSpec("minute", 32.2, 34.9, 33.4, 33.6, 3.2, 36.4,
                 139.0, 146.0, 25.5, 34.9, "#E3A02B"),
        RoleSpec("second", 36.6, 39.0, 37.6, 37.8, 1.8, 40.5,
                 131.7, 138.7, 36.6, 46.0, "#178D88"),
    )

    @property
    def tooth_pitch_deg(self) -> float:
        return 360.0 / self.ring_teeth

    @property
    def tooth_pitch_arc(self) -> float:
        return 2.0 * pi * self.ring_pitch_radius / self.ring_teeth

    @property
    def passive_part_count(self) -> int:
        return 4 + 9 + 3 + 9


@dataclass(frozen=True)
class KageM1BSpec:
    namespace: str = MOTOR_NAMESPACE
    pinion_teeth: int = 18
    pinion_pitch_radius: float = 9.0
    nominal_center_distance: float = 120.0
    motor_envelope: tuple[float, float, float] = (20.3, 20.3, 39.3)
    provisional_shaft_diameter: float = 4.0
    provisional_shaft_length: float = 7.0
    measurement_gated_hole_pitch: float = 15.4
    slot_width: float = 3.4
    slot_overall_length: float = 9.4
    adjustment: float = 3.0
    provisional_backlash: float = 0.20
    target_backlash: float = 0.10
    pressure_angle_deg: float = 20.0
    station_plate_z0: float = 6.0
    station_plate_z1: float = 10.0
    station_r0: float = 102.0
    station_r1: float = 126.0
    station_half_t: float = 15.0

    def center_distance(self, q: float) -> float:
        return self.nominal_center_distance + q

    def backlash(self, q: float) -> float:
        return self.provisional_backlash - 2.0 * q * tan(radians(self.pressure_angle_deg))

    @property
    def target_q(self) -> float:
        return (self.provisional_backlash - self.target_backlash) / (
            2.0 * tan(radians(self.pressure_angle_deg))
        )


M1 = KageM1Spec()
M1B = KageM1BSpec()
