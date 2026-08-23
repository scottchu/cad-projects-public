"""Numeric interface contract for the isolated KAGE P3 V3 R1 transmission.

This subrevision replaces only one provisional motor-to-ring drive station.
The accepted P3 V3 rings, axial carrier layers, fins, simulator, and optical
math remain byte-for-byte frozen.  Units are millimetres and degrees.  XY is
the clock plane, +Z faces the viewer, and the reference station lies on +X.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import radians, sin


@dataclass(frozen=True)
class P3V3TransmissionR1Spec:
    """Manufacturable one-station transmission interface."""

    # Frozen parent coordinate system and role interfaces.
    clock_plane: str = "XY"
    viewer_axis: str = "+Z"
    motor_axis: str = "+X"
    output_axis: str = "+Z"
    axes_angle_degrees: float = 90.0
    roles: tuple[str, str, str] = ("hour", "minute", "second")
    selected_role: int = 1
    carrier_layers: tuple[tuple[float, float], ...] = (
        (2.8, 5.8),
        (6.2, 9.2),
        (9.6, 12.6),
    )
    pinion_face_margin: float = 0.10
    role_face_ranges: tuple[tuple[float, float], ...] = (
        (2.9, 5.7),
        (6.3, 9.1),
        (9.7, 12.5),
    )

    # Frozen 259T internal ring, revised true 16T output pinion.
    ring_module: float = 1.0
    ring_teeth: int = 259
    ring_pitch_radius: float = 129.5
    ring_tip_radius: float = 128.5
    output_pinion_teeth: int = 16
    output_pinion_pitch_radius: float = 8.0
    output_pinion_outer_radius: float = 9.0
    output_pinion_root_radius: float = 6.75
    output_pinion_bore_diameter: float = 4.10
    output_pinion_bore_across_flat: float = 3.60
    output_axis_radius: float = 121.5
    output_mesh_backlash: float = 0.20
    output_face_width: float = 2.8
    output_pinion_hub_diameter: float = 7.0
    output_pinion_hub_height: float = 1.8
    output_pinion_set_screw_thread: str = "M2"

    # Equal 16T straight bevel/miter pair.  Face width is limited to one third
    # of pitch-cone distance, a conservative printable bevel-gear rule.
    miter_module: float = 1.0
    miter_teeth: int = 16
    miter_ratio: float = 1.0
    miter_pitch_angle_degrees: float = 45.0
    miter_pitch_radius: float = 8.0
    miter_outer_radius: float = 9.0
    miter_face_width: float = 3.2
    miter_pressure_angle_degrees: float = 20.0
    miter_mesh_backlash: float = 0.20
    miter_axis_intersection_z: float = -12.0
    miter_outer_back_face_offset: float = 8.0
    miter_vertical_back_face_z: float = -4.0
    miter_vertical_hub_top_z: float = -3.10
    miter_vertical_hub_height: float = 2.0
    miter_vertical_hub_diameter: float = 7.5
    miter_output_bore_diameter: float = 4.10
    miter_output_bore_across_flat: float = 3.60
    miter_output_set_screw_thread: str = "M2"

    # The motor shaft is the real 4 x 7 mm D shaft from the supplied drawing.
    # Radial slot adjustment is symmetric about the nominal motor-face datum.
    motor_face_size: float = 20.3
    motor_body_length: float = 39.3
    motor_mount_pitch: float = 15.4
    motor_mount_thread: str = "M2"
    motor_shaft_diameter: float = 4.0
    motor_shaft_across_flat: float = 3.5
    motor_shaft_length: float = 7.0
    motor_shaft_length_tolerance: float = 0.25
    motor_face_radius: float = 111.25
    motor_adjustment: float = 0.50
    motor_miter_bore_diameter: float = 4.10
    motor_miter_bore_across_flat: float = 3.60

    # A 4 x 40 mm D-shaft runs in two catalogue MR84 bearings.  The
    # upper bearing top face at Z=0 is the common datum for every role spacer.
    output_shaft_diameter: float = 4.0
    output_shaft_across_flat: float = 3.5
    output_shaft_length: float = 40.0
    output_shaft_z: tuple[float, float] = (-25.0, 15.0)
    output_shaft_bore_across_flat: float = 3.60
    bearing_code: str = "MR84"
    bearing_id: float = 4.0
    bearing_od: float = 8.0
    bearing_width: float = 3.0
    bearing_pocket_diameter: float = 8.10
    bearing_lip_opening: float = 7.40
    bearing_outer_race_inner_radius: float = 3.10
    bearing_retainer_fastener_y: tuple[float, float] = (-7.0, 7.0)
    bearing_retainer_clearance_hole: float = 2.20
    bearing_retainer_post_diameter: float = 5.0
    bearing_retainer_ring_height: float = 0.70
    bearing_retainer_ear_thickness: float = 0.70
    bearing_retainer_ear_half_width_x: float = 2.0
    lower_bearing_retainer_pilot_engagement: float = 1.50
    upper_bearing_retainer_pilot_engagement: float = 1.60
    lower_bearing_range: tuple[float, float] = (-21.0, -18.0)
    upper_bearing_range: tuple[float, float] = (-3.0, 0.0)
    upper_common_datum_z: float = 0.0
    bearing_center_span: float = 18.0
    endplay_range: tuple[float, float] = (0.05, 0.15)
    target_endplay: float = 0.10

    # Printed hubs receive a true M2 tap pilot, not an M2 clearance tunnel.
    # The reference screw core is represented at the tap-pilot diameter and
    # ends exactly on the shaft's +Y D-flat.
    m2_tap_pilot_diameter: float = 1.60
    m2_service_clearance_diameter: float = 2.40
    output_shaft_flat_y: float = 1.50
    lower_collar_z: tuple[float, float] = (-24.0, -21.15)
    lower_collar_screw_z: float = -22.50

    # The curved 259T tooth form cannot translate tangentially by a full tooth
    # without geometric interference.  This retained coupon therefore permits
    # only +/-0.08 mm: enough to feel backlash/contact, not simulate rotation.
    slider_half_stroke: float = 0.08
    slider_running_clearance: float = 0.30
    slider_carriage_x: tuple[float, float] = (131.60, 140.00)
    slider_carriage_half_length_y: float = 18.0
    slider_rail_x: tuple[float, float] = (137.50, 141.00)
    slider_rail_y_half_length: float = 18.08
    slider_rail_thickness_z: float = 0.70
    slider_retainer_outer_x: float = 145.0
    slider_retainer_fastener_x: float = 143.0
    slider_retainer_fastener_y: tuple[float, float] = (-12.0, 12.0)
    slider_retainer_clearance_hole: float = 2.20
    slider_retainer_post_diameter: float = 5.0

    # The saddle slots are clearance features.  Four external M3 clamp stacks
    # provide the actual normal force; no printed thread is assumed here.
    saddle_clamp_count: int = 4
    saddle_clamp_clearance_diameter: float = 3.40
    saddle_clamp_bolt_diameter: float = 3.00
    saddle_clamp_washer_od: float = 7.00
    saddle_clamp_nut_af: float = 5.50
    saddle_clamp_y: float = 14.50
    saddle_clamp_lower_washer_z: tuple[float, float] = (-27.45, -27.00)
    saddle_clamp_upper_washer_z: tuple[float, float] = (-22.15, -21.65)
    saddle_clamp_nut_z: tuple[float, float] = (-21.65, -19.25)
    saddle_clamp_shank_z: tuple[float, float] = (-27.50, -19.25)
    saddle_clamp_thread_minor_diameter: float = 2.50

    # Role spacers are non-driving sleeves.  The 0.05 mm axial relief avoids
    # using a printed spacer as a friction thrust face; pinions are set-screwed.
    spacer_outer_diameter: float = 5.8
    spacer_bore_diameter: float = 4.20
    spacer_axial_relief: float = 0.05

    # Geometry tests use this threshold to reject the former smooth cone
    # envelopes.  A real 16T pair must expose at least two tooth-side edges and
    # one periodic tooth face per tooth on each gear.
    minimum_miter_tip_vertices: int = 32
    minimum_miter_tooth_side_faces: int = 32
    minimum_miter_periodic_faces: int = 16

    coupon_size: tuple[float, float, float] = (95.0, 55.0, 42.0)
    motor_adjustment_slot_travel: float = 1.0

    @property
    def gear_ratio(self) -> float:
        return self.ring_teeth / self.output_pinion_teeth

    @property
    def carrier_full_step_degrees(self) -> float:
        return 1.8 / self.gear_ratio

    @property
    def carrier_microstep_degrees(self) -> float:
        return self.carrier_full_step_degrees / 16.0

    @property
    def seconds_motor_rpm(self) -> float:
        return self.gear_ratio

    @property
    def seconds_microsteps_per_second(self) -> float:
        return (360.0 / 1.8 * 16.0) * self.seconds_motor_rpm / 60.0

    @property
    def miter_cone_distance(self) -> float:
        return self.miter_pitch_radius / sin(radians(self.miter_pitch_angle_degrees))

    @property
    def miter_face_width_limit(self) -> float:
        return min(self.miter_cone_distance / 3.0, 10.0 * self.miter_module)

    @property
    def nominal_motor_shaft_range(self) -> tuple[float, float]:
        return self.motor_face_radius, self.motor_face_radius + self.motor_shaft_length

    @property
    def worst_case_motor_shaft_tip_radius(self) -> float:
        return (
            self.motor_face_radius
            + self.motor_shaft_length
            + self.motor_shaft_length_tolerance
            + self.motor_adjustment
        )

    @property
    def worst_case_motor_to_output_shaft_clearance(self) -> float:
        output_inner_surface = self.output_axis_radius - self.output_shaft_diameter / 2.0
        return output_inner_surface - self.worst_case_motor_shaft_tip_radius

    @property
    def shaft_to_non_driven_tooth_clearance(self) -> float:
        return self.ring_tip_radius - (
            self.output_axis_radius + self.output_shaft_diameter / 2.0
        )

    @property
    def spacer_to_non_driven_tooth_clearance(self) -> float:
        return self.ring_tip_radius - (
            self.output_axis_radius + self.spacer_outer_diameter / 2.0
        )

    @property
    def bearing_to_non_driven_tooth_clearance(self) -> float:
        return self.ring_tip_radius - (
            self.output_axis_radius + self.bearing_od / 2.0
        )

    @property
    def miter_to_upper_bearing_clearance(self) -> float:
        return self.upper_bearing_range[0] - self.miter_vertical_hub_top_z

    @property
    def lower_collar_engagement(self) -> float:
        return self.lower_collar_z[1] - self.lower_collar_z[0]

    @property
    def shaft_above_second_pinion(self) -> float:
        return self.output_shaft_z[1] - self.role_face_ranges[2][1]

    @property
    def slider_total_stroke(self) -> float:
        return 2.0 * self.slider_half_stroke

    @property
    def upper_retainer_to_miter_clearance(self) -> float:
        return self.bearing_outer_race_inner_radius - self.output_shaft_diameter / 2.0

    def pinion_face_range(self, role_index: int) -> tuple[float, float]:
        return self.role_face_ranges[role_index]

    def spacer_length(self, role_index: int) -> float:
        face_start, _ = self.pinion_face_range(role_index)
        return face_start - self.upper_common_datum_z - self.spacer_axial_relief

    @property
    def role_spacer_lengths(self) -> tuple[float, float, float]:
        return tuple(self.spacer_length(role) for role in range(len(self.roles)))

    def miter_topology_has_teeth(
        self,
        *,
        tip_vertices: int,
        tooth_side_faces: int,
        periodic_faces: int,
    ) -> bool:
        """Return true only for topology rich enough to represent real teeth."""

        return (
            tip_vertices >= self.minimum_miter_tip_vertices
            and tooth_side_faces >= self.minimum_miter_tooth_side_faces
            and periodic_faces >= self.minimum_miter_periodic_faces
        )


P3_V3_TRANSMISSION_R1 = P3V3TransmissionR1Spec()


ACCEPTED_P3_V3_SHA256 = {
    "p3_v3_stacked_three_motor_90deg_spec.py": "1d0b44bab02c7bd3de5c00e76fde14828c9f154bef448ba4fca8c6be8d46080e",
    "p3_v3_stacked_three_motor_90deg_geometry.py": "c9ac46db39ad84e89a43b0fbeba6444e135792f2debaf6b79870eb5e4b8c11be",
    "p3_v3_stacked_three_motor_90deg_export.py": "096b0c7b088323e84068536a2abed18d5d7deb7a552de7d58d8b56a4e84fcfac",
    "tests/test_p3_v3_stacked_three_motor_90deg.py": "30429ef50969c3a377154c8233e87a84938293f2766ef198c5f0d0228ae51a39",
}
