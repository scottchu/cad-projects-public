"""Accepted P0 v3 named variables and derived dimensional equations."""

from dataclasses import dataclass


Interval = tuple[float, float]


def interval(center: float, length: float) -> Interval:
    return (center - length / 2, center + length / 2)


@dataclass(frozen=True)
class P0V3Spec:
    """Frozen P0 v3 contract, in millimetres."""

    # Housing and motion.
    housing_size: float = 40.0
    housing_fixed_rear_y: float = -18.7
    latched_center_y: float = 4.5
    shuttle_inward_state: float = -1.0
    pressed_state: float = 0.0
    released_state: float = 13.4
    maximum_pull_state: float = 13.55
    normal_coupling_backlash: float = 0.10

    # Main guide, key, and captivity.
    rear_channel_width: float = 37.3
    rear_channel_height: float = 35.8
    front_key_guide_width: float = 35.6
    captive_stop_throat_width: float = 34.9
    key_face_size: float = 35.2
    key_face_thickness: float = 3.0
    shuttle_width: float = 34.2
    shuttle_height: float = 34.2
    shuttle_rear_local_y: float = -13.0
    shuttle_front_local_y: float = 12.5
    key_front_local_y: float = 15.5
    medicine_wall: float = 2.0
    captive_tab_span: float = 36.9
    captive_tab_depth: float = 3.0
    captive_tab_height: float = 5.0
    captive_stop_pad_height: float = 5.4
    front_shoulder_y: float = 15.35
    tab_local_front_y: float = -2.70
    tab_local_rear_y: float = -5.70

    # Rail/land interface.
    rail_count: int = 4
    rail_z_offset: float = 9.5
    rail_radial_height: float = 1.2
    rail_tangential_width: float = 2.2
    rail_inner_tip_x: float = 17.45
    rail_root_x: float = 18.65
    rail_start_y: float = -18.70
    rail_end_y: float = 15.35
    rail_rear_lead_in: float = 0.70
    key_rail_relief_width: float = 2.8
    key_rail_relief_depth: float = 0.35
    key_relief_rear_local_y: float = 12.30
    key_relief_front_local_y: float = 15.70
    key_stop_relief_min_z: float = -2.70
    key_stop_relief_max_z: float = 2.70
    land_length: float = 6.8
    bearing_boss_width: float = 4.3
    groove_width_nominal: float = 2.7
    groove_width_loose: float = 2.8
    groove_radial_depth: float = 0.65
    groove_bottom_x: float = 17.25
    groove_mouth_length: float = 0.6
    groove_mouth_extra_width: float = 0.4
    groove_mouth_extra_depth: float = 0.3
    rear_land_local_y: float = -13.8
    front_land_local_y: float = -6.6
    rear_land_backing_radial_thickness: float = 0.8
    rear_land_backing_body_overlap_y: float = 0.2

    # Printable shutter/track section.
    shutter_web_width: float = 25.0
    shutter_web_thickness: float = 0.8
    shutter_flange_width: float = 27.4
    shutter_flange_thickness: float = 0.8
    track_web_width: float = 25.4
    track_flange_width: float = 27.8
    track_lateral_clearance_per_side: float = 0.2
    track_vertical_clearance: float = 0.2
    track_floor_clearance: float = 0.2
    track_capture_overlap_per_side: float = 1.0
    shutter_exterior_recess: float = 0.2
    opaque_shroud_thickness: float = 0.8
    opaque_shroud_width_x: float = 25.4
    shutter_lead_in_length: float = 0.8
    track_mouth_extra_width: float = 0.4
    track_mouth_extra_height: float = 0.2
    top_shutter_exterior_z: float = 19.8
    bottom_shutter_exterior_z: float = -19.8
    top_track_floor_z: float = 18.0
    top_lip_underside_z: float = 19.2
    bottom_track_floor_z: float = -18.0
    bottom_lip_inner_z: float = -19.2

    # Apertures, shrouds, and solid shutter edge plates.
    fixed_fill_center_y: float = 0.5
    fixed_fill_width: float = 23.0
    fixed_fill_length: float = 10.0
    moving_fill_local_center_y: float = -4.0
    moving_fill_width: float = 23.0
    moving_fill_length: float = 10.0
    top_shutter_local_rear_y: float = -22.9
    top_shutter_local_front_y: float = -9.6
    top_opaque_shroud_rear_y: float = 8.7
    top_opaque_shroud_front_y: float = 20.0
    fixed_outlet_center_y: float = 3.2
    fixed_outlet_width: float = 22.0
    fixed_outlet_length: float = 4.8
    moving_outlet_local_center_y: float = -1.3
    moving_outlet_width: float = 22.0
    moving_outlet_length: float = 4.8
    bottom_shutter_local_rear_y: float = -22.9
    bottom_shutter_local_front_y: float = -4.3
    bottom_opaque_shroud_rear_y: float = 14.0
    bottom_opaque_shroud_front_y: float = 20.0

    # Lost-motion dog/socket and preload fingers.
    coupling_lug_length_y: float = 1.2
    coupling_socket_length_y: float = 2.4
    coupling_lost_motion: float = 1.0
    coupling_end_clearance: float = 0.1
    coupling_transverse_clearance: float = 0.2
    coupling_lug_width_x: float = 3.0
    coupling_lug_height_z: float = 0.8
    coupling_socket_width_x: float = 3.4
    coupling_socket_height_z: float = 1.2
    coupling_boss_width_x: float = 5.0
    coupling_channel_width: float = 5.4
    coupling_channel_height: float = 3.2
    coupling_channel_rear_lead_in: float = 0.4
    coupling_rearward_shift_y: float = -9.0
    top_coupling_channel_front_y: float = 7.65
    bottom_coupling_channel_front_y: float = 13.65
    top_lug_local_y: Interval = (-20.6, -19.4)
    top_socket_local_y: Interval = (-20.7, -18.3)
    bottom_lug_local_y: Interval = (-14.6, -13.4)
    bottom_socket_local_y: Interval = (-14.7, -12.3)
    top_complete_coupling_local_y: Interval = (-21.3, -10.6)
    bottom_complete_coupling_local_y: Interval = (-15.3, -4.6)
    detent_finger_free_length: float = 8.0
    detent_finger_width: float = 3.0
    detent_finger_thickness: float = 0.8
    detent_root_fillet: float = 0.8
    detent_entry_chamfer: float = 0.6
    detent_relief: float = 1.2
    detent_maximum_deflection: float = 0.5

    # Full blind rear faceplate and shutter stops.
    rear_faceplate_width: float = 40.0
    rear_faceplate_height: float = 40.0
    rear_faceplate_thickness: float = 1.3
    rear_faceplate_exterior_y: float = -20.0
    rear_faceplate_interior_y: float = -18.7
    rear_cover_pilot_width: float = 36.9
    rear_cover_pilot_height: float = 35.3
    rear_cover_pilot_depth: float = 1.6
    rear_cover_pilot_front_y: float = -17.1
    rear_cover_edge_chamfer: float = 0.3
    shutter_stop_nibs_per_shutter: int = 2
    shutter_stop_nib_center_x: float = 11.0
    shutter_stop_nib_width_x: float = 2.0
    shutter_stop_nib_thickness_z: float = 0.8
    shutter_stop_nib_rear_y: float = -18.7
    shutter_stop_nib_front_y: float = -18.4

    # Four exact C4-mapped cover snaps.
    rear_snap_count: int = 4
    rear_snap_center_x: float = 16.2
    rear_snap_effective_length: float = 7.5
    rear_snap_width: float = 3.6
    rear_snap_bending_thickness: float = 1.2
    rear_snap_root_fillet: float = 0.8
    rear_snap_root_overlap: float = 0.2
    rear_snap_root_tangent_y: float = 0.8
    rear_snap_local_front_y: float = 8.85
    rear_snap_hook_base_rear_y: float = 7.75
    rear_snap_hook_base_front_y: float = 8.85
    rear_snap_hook_apex_y: float = 8.30
    rear_snap_top_beam_outer_z: float = 18.15
    rear_snap_top_hook_apex_z: float = 18.70
    rear_snap_bottom_beam_outer_z: float = -18.15
    rear_snap_bottom_hook_apex_z: float = -18.70
    rear_snap_pocket_outer_z: float = 18.80
    rear_snap_pocket_width_x: float = 4.0
    rear_snap_pocket_rear_y: float = -10.95
    rear_snap_pocket_front_y: float = -9.85
    rear_snap_pocket_radial_depth: float = 0.65
    rear_snap_nominal_deflection: float = 0.55
    rear_snap_worst_deflection: float = 0.65

    # Feed sweep.
    feed_start_center_y: float = -34.4
    feed_end_center_y: float = 4.5
    feed_step: float = 0.1

    @property
    def housing_half(self) -> float:
        return self.housing_size / 2

    @property
    def rear_channel_half_width(self) -> float:
        return self.rear_channel_width / 2

    @property
    def rear_channel_half_height(self) -> float:
        return self.rear_channel_height / 2

    @property
    def shuttle_inner_half_x(self) -> float:
        return self.shuttle_width / 2 - self.medicine_wall

    @property
    def shuttle_inner_half_z(self) -> float:
        return self.shuttle_height / 2 - self.medicine_wall

    @property
    def shuttle_inner_rear_y(self) -> float:
        return self.shuttle_rear_local_y + self.medicine_wall

    @property
    def shuttle_inner_front_y(self) -> float:
        return self.shuttle_front_local_y - self.medicine_wall

    @property
    def rear_channel_wall(self) -> float:
        return (self.housing_size - self.rear_channel_width) / 2

    @property
    def key_main_clearance(self) -> float:
        return (self.front_key_guide_width - self.key_face_size) / 2

    @property
    def tab_rear_channel_clearance(self) -> float:
        return (self.rear_channel_width - self.captive_tab_span) / 2

    @property
    def tab_stop_pad_overlap(self) -> float:
        return (self.captive_tab_span - self.captive_stop_throat_width) / 2

    @property
    def rear_cover_pilot_x_clearance(self) -> float:
        return (self.rear_channel_width - self.rear_cover_pilot_width) / 2

    @property
    def rear_cover_pilot_z_clearance(self) -> float:
        return (self.rear_channel_height - self.rear_cover_pilot_height) / 2

    @property
    def released_endplay(self) -> float:
        tab_front = self.shuttle_center_y(self.released_state) + self.tab_local_front_y
        return self.front_shoulder_y - tab_front

    @property
    def track_lateral_clearance(self) -> float:
        return (self.track_flange_width - self.shutter_flange_width) / 2

    @property
    def track_capture_overlap(self) -> float:
        return (self.shutter_flange_width - self.track_web_width) / 2

    @property
    def normal_lip_per_side(self) -> float:
        return (self.bearing_boss_width - self.groove_width_nominal) / 2

    @property
    def mouth_lip_per_side(self) -> float:
        return (
            self.bearing_boss_width
            - self.groove_width_nominal
            - self.groove_mouth_extra_width
        ) / 2

    @property
    def longitudinal_land_gap(self) -> float:
        return self.front_land_local_y - self.rear_land_local_y - self.land_length

    @property
    def rear_land_backing_local_y(self) -> Interval:
        return (
            self.rear_land_local_y - self.land_length / 2,
            self.shuttle_rear_local_y + self.rear_land_backing_body_overlap_y,
        )

    @property
    def estimated_detent_strain(self) -> float:
        return (
            3
            * self.detent_finger_thickness
            * self.detent_maximum_deflection
            / (2 * self.detent_finger_free_length**2)
        )

    @property
    def top_coupling_aperture_y_clearance(self) -> float:
        moving_fill_rear = self.moving_fill_local_center_y - self.moving_fill_length / 2
        return moving_fill_rear - self.top_complete_coupling_local_y[1]

    @property
    def bottom_coupling_aperture_y_clearance(self) -> float:
        moving_outlet_rear = (
            self.moving_outlet_local_center_y - self.moving_outlet_length / 2
        )
        return moving_outlet_rear - self.bottom_complete_coupling_local_y[1]

    @property
    def nominal_snap_strain(self) -> float:
        return (
            1.5
            * self.rear_snap_bending_thickness
            * self.rear_snap_nominal_deflection
            / self.rear_snap_effective_length**2
        )

    @property
    def worst_snap_strain(self) -> float:
        return (
            1.5
            * self.rear_snap_bending_thickness
            * self.rear_snap_worst_deflection
            / self.rear_snap_effective_length**2
        )

    @property
    def feed_sample_count(self) -> int:
        return int(round((self.feed_end_center_y - self.feed_start_center_y) / self.feed_step)) + 1

    def shuttle_center_y(self, state: float) -> float:
        if not self.shuttle_inward_state <= state <= self.maximum_pull_state:
            raise ValueError("state outside P0 v3 hard range")
        return self.latched_center_y + state

    def shutter_q(self, state: float) -> float:
        if not self.shuttle_inward_state <= state <= self.maximum_pull_state:
            raise ValueError("state outside P0 v3 hard range")
        return max(0.0, state)

    def relative_lost_motion(self, state: float) -> float:
        return state - self.shutter_q(state)

    def fixed_fill_interval(self) -> Interval:
        return interval(self.fixed_fill_center_y, self.fixed_fill_length)

    def fixed_outlet_interval(self) -> Interval:
        return interval(self.fixed_outlet_center_y, self.fixed_outlet_length)

    def moving_fill_interval(self, state: float) -> Interval:
        return interval(
            self.shuttle_center_y(state) + self.moving_fill_local_center_y,
            self.moving_fill_length,
        )

    def moving_outlet_interval(self, state: float) -> Interval:
        return interval(
            self.shuttle_center_y(state) + self.moving_outlet_local_center_y,
            self.moving_outlet_length,
        )

    def top_shutter_interval_q(self, q: float) -> Interval:
        return (
            self.latched_center_y + q + self.top_shutter_local_rear_y,
            self.latched_center_y + q + self.top_shutter_local_front_y,
        )

    def bottom_shutter_interval_q(self, q: float) -> Interval:
        return (
            self.latched_center_y + q + self.bottom_shutter_local_rear_y,
            self.latched_center_y + q + self.bottom_shutter_local_front_y,
        )

    def land_interval(self, state: float, local_y: float) -> Interval:
        return interval(self.shuttle_center_y(state) + local_y, self.land_length)

    def feed_states(self) -> list[float]:
        return [
            round(self.feed_start_center_y + i * self.feed_step, 10)
            for i in range(self.feed_sample_count)
        ]


P0V3 = P0V3Spec()

__all__ = ["Interval", "P0V3", "P0V3Spec", "interval"]
