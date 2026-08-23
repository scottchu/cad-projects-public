"""Assembly contract for the isolated KAGE P3 V3 motor station.

This package does not change the accepted rings, fins, keepers, or roller work.
It documents one serviceable 90-degree motor station and the three axial output
variants needed to mesh the H/M/S carrier layers.  Units are millimetres.
"""

from __future__ import annotations

from dataclasses import dataclass

from p3_v3_full_ring_r2_spec import P3V3FullRingR2Spec, P3_V3_FULL_RING_R2


@dataclass(frozen=True)
class P3V3MotorStationAssemblySimSpec:
    parent: P3V3FullRingR2Spec = P3_V3_FULL_RING_R2

    selected_role: int = 2
    local_station_angle_degrees: float = 0.0

    # Supplied StepperOnline NEMA8 drawing.  The motor's four holes are
    # threaded M2, not through holes in the motor.
    motor_mount_pitch: float = 15.40
    motor_thread: str = "M2"
    motor_thread_depth_min: float = 2.50
    motor_flange_thickness: float = 1.50
    motor_clearance_hole_diameter: float = 2.20
    motor_screw: str = "ISO 4762 M2x4"
    motor_screw_length: float = 4.00
    motor_screw_head_diameter: float = 3.80
    motor_screw_head_height: float = 2.00
    motor_center_passage_diameter: float = 18.80

    # The complete gearbox yoke bolts to four heat-set inserts in the fixed
    # chassis patch.  The screws enter from the viewer side (+Z).
    chassis_screw: str = "ISO 4762 M3x8"
    chassis_screw_length: float = 8.00
    chassis_screw_clearance_diameter: float = 3.40
    chassis_screw_head_diameter: float = 5.50
    gearbox_foot_thickness: float = 3.00
    chassis_insert_outer_diameter: float = 4.60
    chassis_insert_pilot_diameter: float = 4.40
    chassis_insert_length: float = 5.50
    chassis_insert_engagement_min: float = 5.00
    chassis_mount_x: tuple[float, float] = (84.0, 104.0)
    chassis_mount_y: tuple[float, float] = (-14.50, 14.50)
    gearbox_foot_z: tuple[float, float] = (-27.50, -24.50)
    chassis_patch_z: tuple[float, float] = (-30.00, -27.50)

    # Open yoke structure: no closed gearbox and clear side access to all set
    # screws.  Bearing pockets retain only the cooler outer race.
    frame_side_y: float = 11.50
    frame_wall: float = 2.50
    bearing_pocket_diameter: float = 8.10
    bearing_lip_opening: float = 7.40
    bearing_housing_outer_diameter: float = 12.00
    bearing_press_allowance_diameter: float = 0.10
    motor_driver_clearance_diameter: float = 6.00
    # A 3 mm service envelope is ample for the 1.5 mm hex key used by M2 grub
    # screws while staying below the adjacent MR84 outer race.
    set_screw_tool_clearance_diameter: float = 3.00
    driver_window_clearance: float = 0.20
    shaft_set_screw_tap_pilot_diameter: float = 1.60
    motor_shaft_across_flat: float = 3.50
    output_shaft_flat_y: float = 1.50
    miter_hub_diameter: float = 7.50
    miter_outer_radius: float = 9.00
    horizontal_bevel_grub_screw: str = "M2x3 cup-point grub screw"
    output_grub_screw: str = "M2x3 cup-point grub screw"

    # Removable radial bearing gates close the otherwise open +X insertion
    # mouth.  Two M2x4 screws per gate pass a 1.5 mm cap and engage 2.5 mm in
    # the printed side posts.
    bearing_cap_thickness_x: float = 1.50
    bearing_cap_radial_clearance_x: float = 0.05
    bearing_cap_screw_y: tuple[float, float] = (-11.50, 11.50)
    bearing_cap_screw: str = "ISO 4762 M2x4"
    bearing_cap_screw_engagement: float = 2.50

    # Purchased stack.  A steel 4x40 D-shaft and two MR84ZZ bearings are
    # retained by two purchased split clamp collars.  This deliberately avoids
    # a fragile printed M4 nut/thread at the top of the shaft.
    bearing_code: str = "MR84ZZ"
    # Every driven part is phased first, then recut with the same +Y-facing
    # D-flat.  Tooth phase and shaft-flat phase are independent contracts.
    shaft: str = "4x40 mm steel D-shaft, 3.5 mm across-flat"
    collar: str = "4 mm split clamp shaft collar with M2 clamp screw"
    shaft_bore_clearance_diameter: float = 4.10
    shaft_bore_across_flat: float = 3.60
    shaft_across_flat: float = 3.50
    collar_outer_diameter: float = 7.00
    collar_height: float = 2.40
    # Bias the upper collar's M2 clamp axis 0.20 mm above its axial centre.
    # This leaves a full 3.0 mm hex-key service cylinder tangent to, rather
    # than passing through, the output pinion below it.
    top_collar_screw_offset_z: float = 1.40
    collar_axial_relief: float = 0.10
    target_axial_endplay: float = 0.10
    spacer_outer_diameter: float = 5.80
    spacer_bore_diameter: float = 4.20
    spacer_axial_relief: float = 0.05

    # The frame is built around the exact R2 station translation.  All local
    # staged models use the +X station so dimensions remain directly readable.
    station_translation_x: float = 0.50
    output_axis_x: float = 122.00
    motor_face_x: float = 111.75
    motor_face_plate_x: tuple[float, float] = (111.75, 113.25)
    motor_body_x: tuple[float, float] = (72.45, 111.75)
    motor_face_size: float = 20.30
    motor_body_length: float = 39.30
    motor_shaft_length: float = 7.00

    # Exploded stage distances are visualization-only and never enter the
    # assembled mechanical tests.
    motor_explode_x: float = -18.0
    frame_explode_z: float = 18.0
    stack_explode_z: float = 8.0
    service_explode_x: float = 18.0

    def role_shift_z(self, role: int) -> float:
        return self.parent.station_role_z_translations[role]

    def shaft_z(self, role: int) -> tuple[float, float]:
        shift = self.role_shift_z(role)
        return tuple(v + shift for v in self.parent.output_shaft_z)

    def lower_bearing_z(self, role: int) -> tuple[float, float]:
        shift = self.role_shift_z(role)
        return tuple(v + shift for v in self.parent.lower_bearing_range)

    def upper_bearing_z(self, role: int) -> tuple[float, float]:
        shift = self.role_shift_z(role)
        return tuple(v + shift for v in self.parent.upper_bearing_range)

    def miter_intersection_z(self, role: int) -> float:
        return self.parent.miter_axis_intersection_z + self.role_shift_z(role)

    def lower_collar_z(self, role: int) -> tuple[float, float]:
        lower = self.lower_bearing_z(role)
        z1 = lower[0] - self.collar_axial_relief
        return z1 - self.collar_height, z1

    def spacer_z(self, role: int) -> tuple[float, float]:
        upper_top = self.upper_bearing_z(role)[1]
        pinion_bottom = self.parent.pinion_face_ranges[role][0]
        return upper_top + self.spacer_axial_relief, pinion_bottom

    def spacer_length(self, role: int) -> float:
        z0, z1 = self.spacer_z(role)
        return z1 - z0

    def top_collar_z(self, role: int) -> tuple[float, float]:
        pinion_top = self.parent.pinion_face_ranges[role][1]
        z0 = pinion_top + self.collar_axial_relief
        return z0, z0 + self.collar_height

    def top_collar_screw_z(self, role: int) -> float:
        return self.top_collar_z(role)[0] + self.top_collar_screw_offset_z

    @property
    def motor_thread_engagement(self) -> float:
        return self.motor_screw_length - self.motor_flange_thickness

    @property
    def chassis_insert_engagement(self) -> float:
        return self.chassis_screw_length - self.gearbox_foot_thickness

    @property
    def chassis_insert_bottom_margin(self) -> float:
        return self.chassis_insert_length - self.chassis_insert_engagement

    def ring_mesh_overlap(self, role: int) -> float:
        a0, a1 = self.parent.pinion_face_ranges[role]
        b0, b1 = self.parent.pinion_face_ranges[role]
        return max(0.0, min(a1, b1) - max(a0, b0))


P3_V3_MOTOR_STATION_ASSEMBLY_SIM = P3V3MotorStationAssemblySimSpec()
