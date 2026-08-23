"""Frozen service contract for one KAGE V3 drive station.

This is an isolated minute-channel installation model.  It does not modify the
accepted three-ring mechanism.  Units are millimetres; XY is the clock plane
and +Z faces the viewer.
"""

from __future__ import annotations

from dataclasses import dataclass

from p3_v3_full_ring_r2_spec import P3_V3_FULL_RING_R2


@dataclass(frozen=True)
class P3V3DriveServiceSpec:
    role_index: int = 1
    role: str = "minute"

    # Existing transmission datums, deliberately not re-tuned here.
    output_axis_x: float = 122.0
    motor_face_x: float = 111.75
    motor_axis_z: float = -14.40
    motor_face_size: float = 20.30
    motor_mount_pitch: float = 15.40
    motor_mount_thread: str = "M2"
    motor_mount_screw_length: float = 4.0
    motor_plate_thickness: float = 2.0
    motor_center_aperture: float = 19.0
    motor_shaft_diameter: float = 4.0
    motor_shaft_across_flat: float = 3.5
    motor_shaft_length: float = 7.0

    output_shaft_diameter: float = 4.0
    output_shaft_across_flat: float = 3.5
    output_shaft_z: tuple[float, float] = (-27.15, 12.85)
    lower_bearing_range: tuple[float, float] = (-23.15, -20.15)
    upper_bearing_range: tuple[float, float] = (-5.15, -2.15)
    bearing_id: float = 4.0
    bearing_od: float = 8.0
    bearing_width: float = 3.0
    bearing_pocket_diameter: float = 8.10
    bearing_aperture_diameter: float = 6.40
    bearing_shoulder: float = 1.20

    # The output pinion remains exactly in the existing minute-ring plane.
    output_pinion_face: tuple[float, float] = (4.85, 6.95)
    pinion_teeth: int = 16
    ring_teeth: int = 260
    gear_module: float = 1.0
    output_mesh_backlash: float = 0.20

    # The lower collar and pinion/spacer define the shaft's axial datum.
    lower_collar_z: tuple[float, float] = (-27.05, -24.45)
    lower_inner_race_spacer_z: tuple[float, float] = (-24.40, -23.20)
    spacer_z: tuple[float, float] = (-2.10, 4.85)
    safety_collar_z: tuple[float, float] = (7.05, 10.05)
    axial_endplay: float = 0.15
    collar_od: float = 10.0
    service_knob_od: float = 14.0

    # Separate motor cartridge and bearing gearbox attach to the clock chassis.
    chassis_z: tuple[float, float] = (-30.0, -28.0)
    motor_flange_x: tuple[float, float] = (102.0, 114.0)
    gearbox_flange_x: tuple[float, float] = (114.0, 134.0)
    flange_half_width: float = 16.0
    flange_z: tuple[float, float] = (-28.0, -25.5)
    chassis_fastener: str = "M3x8"
    chassis_clearance_hole: float = 3.40
    chassis_fastener_x: tuple[float, float] = (105.0, 131.0)
    chassis_fastener_y: tuple[float, float] = (-13.0, 13.0)

    tower_column_y: float = 10.5
    tower_column_width: float = 2.0
    tower_column_x: tuple[float, float] = (115.0, 129.0)
    bridge_fastener: str = "M3x8"
    bridge_clearance_hole: float = 3.40
    bridge_insert_pilot: float = 4.0
    bridge_insert_depth: float = 5.0
    bridge_z: tuple[float, float] = (-5.20, -0.95)

    # Fit allowances and assembly policy.
    d_bore_diameter: float = 4.10
    d_bore_across_flat: float = 3.60
    bearing_radial_clearance: float = 0.05
    moving_to_frame_clearance_min: float = 0.15
    tool_clearance_diameter_m2: float = 4.0
    tool_clearance_diameter_m3: float = 6.0

    @property
    def gear_ratio(self) -> float:
        return self.ring_teeth / self.pinion_teeth

    @property
    def lower_collar_gap(self) -> float:
        return (
            self.lower_inner_race_spacer_z[0] - self.lower_collar_z[1]
            + self.lower_bearing_range[0] - self.lower_inner_race_spacer_z[1]
        )

    @property
    def spacer_lower_gap(self) -> float:
        return self.spacer_z[0] - self.upper_bearing_range[1]

    @property
    def spacer_upper_gap(self) -> float:
        return self.output_pinion_face[0] - self.spacer_z[1]

    @property
    def computed_endplay(self) -> float:
        return self.lower_collar_gap + self.spacer_lower_gap + self.spacer_upper_gap


P3_V3_DRIVE_SERVICE = P3V3DriveServiceSpec()

# Guard against accidental drift from the full mechanism.
assert P3_V3_DRIVE_SERVICE.output_pinion_face == P3_V3_FULL_RING_R2.pinion_face_ranges[1]
assert P3_V3_DRIVE_SERVICE.output_axis_x == P3_V3_FULL_RING_R2.output_axis_radius
