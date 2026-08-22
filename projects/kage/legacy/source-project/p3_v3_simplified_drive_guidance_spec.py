"""Frozen implementation contract for the simplified KAGE P3 V3 mechanism.

This is a V3 correction, not a V4 redesign.  It preserves the accepted
300 mm, three-ring, 260T/16T transmission and replaces only two printed
subsystems: the rear T-rail keepers and the multi-part motor/gearbox support.
Units are millimetres; XY is the clock plane and +Z faces the viewer.
"""

from __future__ import annotations

from dataclasses import dataclass

from p3_v3_roller_tower_spec import P3V3RollerTowerSpec


@dataclass(frozen=True)
class P3V3SimplifiedDriveGuidanceSpec(P3V3RollerTowerSpec):
    artifact_slug: str = "p3_v3_simplified_drive_guidance"

    # Exactly three inner towers.  Towers 1 and 2 are fixed; only tower 3 is
    # adjusted radially during setup, over a total 0.50 mm slot travel.
    roller_tower_angles: tuple[float, float, float] = (60.0, 180.0, 300.0)
    fixed_tower_indices: tuple[int, int] = (0, 1)
    adjustable_tower_indices: tuple[int] = (2,)
    roller_axis_adjustment: float = 0.25
    tower_preload_slot_travel: float = 0.50

    # Direct-running spool: a finished 4.05--4.08 bore on a polished D4 axle.
    roller_bore_diameter: float = 4.06
    roller_flange_thickness: float = 0.50
    roller_spacer_lengths: tuple[float, float] = (3.35, 3.35)
    roller_axle_finished_diameter: float = 3.99

    # One open, connected printed yoke replaces the motor bracket, gearbox
    # foot, removable bearing gates, upper bridge, and decorative grip.
    unibody_motor_face_thickness: float = 2.00
    unibody_motor_face_aperture: float = 18.80
    unibody_motor_mount_pitch: float = 15.40
    unibody_motor_mount_clearance: float = 2.20
    unibody_chassis_mount_x: tuple[float, float] = (88.0, 130.0)
    unibody_chassis_mount_y: tuple[float, float] = (-12.0, 12.0)
    unibody_chassis_mount_clearance: float = 3.40
    unibody_foot_x: tuple[float, float] = (78.0, 134.0)
    unibody_foot_y: tuple[float, float] = (-14.0, 14.0)
    unibody_foot_rail_width: float = 3.50
    unibody_foot_thickness: float = 2.50
    unibody_column_x: tuple[float, float] = (115.0, 130.0)
    unibody_column_y: tuple[float, float] = (-11.5, 11.5)
    unibody_column_width: float = 2.50
    unibody_bearing_bridge_x: tuple[float, float] = (114.0, 132.0)
    unibody_bearing_bridge_y: tuple[float, float] = (-12.75, 12.75)
    unibody_bearing_bridge_lip: float = 1.00
    unibody_bearing_pocket_diameter: float = 8.10
    unibody_bearing_install_slot_width: float = 8.20
    unibody_bearing_install_mouth_x: float = 133.0
    unibody_moving_clearance: float = 0.20
    unibody_min_wall: float = 1.20

    # Minimal retained shaft stack.  There is exactly one role spacer, then an
    # output pinion bracketed by commercial lower/upper split collars.
    lower_split_collar_outer_diameter: float = 10.0
    lower_split_collar_height: float = 2.60
    lower_split_collar_relief: float = 0.05
    upper_split_collar_outer_diameter: float = 10.0
    upper_split_collar_height: float = 2.60
    upper_split_collar_relief: float = 0.05
    split_collar_bore_diameter: float = 4.10
    split_collar_set_screw_pilot: float = 1.70
    split_collar_set_screw_length: float = 4.0
    role_spacer_outer_diameter: float = 5.80
    role_spacer_bore_diameter: float = 4.20
    role_spacer_axial_relief: float = 0.05
    nominal_output_endplay: float = 0.10
    output_endplay_tolerance: float = 0.05

    exploded_role_radial_offsets: tuple[float, float, float] = (0.0, 9.0, 18.0)
    exploded_role_z_offsets: tuple[float, float, float] = (18.0, 31.0, 44.0)
    exploded_station_inward_offsets: tuple[float, float, float] = (12.0, 20.0, 28.0)

    def tower_is_adjustable(self, tower_index: int) -> bool:
        return tower_index in self.adjustable_tower_indices

    def role_shift_z(self, role_index: int) -> float:
        return self.station_role_z_translations[role_index]

    def shifted_range(self, values: tuple[float, float], role_index: int) -> tuple[float, float]:
        shift = self.role_shift_z(role_index)
        return values[0] + shift, values[1] + shift

    def output_shaft_range(self, role_index: int) -> tuple[float, float]:
        return self.shifted_range(self.output_shaft_z, role_index)

    def lower_bearing_z(self, role_index: int) -> tuple[float, float]:
        return self.shifted_range(self.lower_bearing_range, role_index)

    def upper_bearing_z(self, role_index: int) -> tuple[float, float]:
        return self.shifted_range(self.upper_bearing_range, role_index)

    def miter_center_z(self, role_index: int) -> float:
        return self.miter_axis_intersection_z + self.role_shift_z(role_index)

    def lower_collar_z(self, role_index: int) -> tuple[float, float]:
        lower0, _ = self.lower_bearing_z(role_index)
        z1 = lower0 - self.lower_split_collar_relief
        return z1 - self.lower_split_collar_height, z1

    def role_spacer_z(self, role_index: int) -> tuple[float, float]:
        _, upper1 = self.upper_bearing_z(role_index)
        pinion0, _ = self.pinion_face_ranges[role_index]
        return upper1 + self.role_spacer_axial_relief, pinion0

    def upper_collar_z(self, role_index: int) -> tuple[float, float]:
        _, pinion1 = self.pinion_face_ranges[role_index]
        z0 = pinion1 + self.upper_split_collar_relief
        return z0, z0 + self.upper_split_collar_height

    def computed_output_endplay(self, role_index: int) -> float:
        lower0, _ = self.lower_bearing_z(role_index)
        _, lower_collar1 = self.lower_collar_z(role_index)
        _, upper_bearing1 = self.upper_bearing_z(role_index)
        spacer0, spacer1 = self.role_spacer_z(role_index)
        pinion0, pinion1 = self.pinion_face_ranges[role_index]
        upper_collar0, _ = self.upper_collar_z(role_index)
        return (
            (lower0 - lower_collar1)
            + (spacer0 - upper_bearing1)
            + (pinion0 - spacer1)
            + (upper_collar0 - pinion1)
        )

    @property
    def output_endplay_bounds(self) -> tuple[float, float]:
        return (
            self.nominal_output_endplay - self.output_endplay_tolerance,
            self.nominal_output_endplay + self.output_endplay_tolerance,
        )


P3_V3_SIMPLIFIED = P3V3SimplifiedDriveGuidanceSpec()
