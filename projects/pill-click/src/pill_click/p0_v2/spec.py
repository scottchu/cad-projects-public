"""Named variables and exact derived equations for P0 v2."""

from dataclasses import dataclass


Interval = tuple[float, float]


def interval(center: float, length: float) -> Interval:
    return (center - length / 2, center + length / 2)


def overlap_length(first: Interval, second: Interval) -> float:
    return max(0.0, min(first[1], second[1]) - max(first[0], second[0]))


@dataclass(frozen=True)
class P0V2Spec:
    """Frozen P0 v2 dimensions in millimetres."""

    # Housing and motion states.
    housing_size: float = 40.0
    rear_channel_width: float = 37.3
    rear_channel_height: float = 35.8
    front_guide_width: float = 34.9
    front_shoulder_y: float = 15.35
    inward_stop_plane_y: float = 16.0
    key_recess_size: float = 35.6
    inward_state: float = -1.0
    pressed_state: float = 0.0
    released_state: float = 13.4
    maximum_pull_state: float = 13.55

    # Medicine shuttle and captivity.
    shuttle_width: float = 34.2
    shuttle_height: float = 34.2
    shuttle_rear_y: float = -13.0
    shuttle_front_y: float = 12.5
    medicine_wall: float = 2.0
    key_face_size: float = 35.2
    key_face_thickness: float = 3.0
    captive_tab_overall_width: float = 36.9
    captive_tab_depth: float = 3.0
    captive_tab_height: float = 5.0

    # Captured shutter section.
    shutter_web_width: float = 25.0
    shutter_flange_width: float = 27.0
    shutter_web_thickness: float = 0.8
    shutter_flange_thickness: float = 0.4
    shutter_lateral_clearance: float = 0.2
    shutter_vertical_clearance: float = 0.15
    shutter_track_floor_clearance: float = 0.2
    shutter_lip_capture_overlap: float = 0.8
    shutter_exterior_step: float = 0.1
    top_shutter_exterior_z: float = 19.9
    bottom_shutter_exterior_z: float = -19.9
    track_skin_thickness: float = 0.05

    # Top shutter and fill aperture.
    fixed_fill_center_y: float = 0.5
    fixed_fill_width: float = 23.0
    fixed_fill_length: float = 10.0
    moving_fill_local_center_y: float = -4.0
    moving_fill_width: float = 23.4
    moving_fill_length: float = 10.4
    top_shutter_local_rear_y: float = -22.9
    top_shutter_local_front_y: float = 2.1
    top_hidden_front_margin: float = 0.9
    top_fixed_backing_margin: float = 0.5

    # Bottom shutter and outlet aperture.
    fixed_outlet_center_y: float = 3.5
    fixed_outlet_width: float = 22.0
    fixed_outlet_length: float = 4.8
    moving_outlet_local_center_y: float = -1.0
    moving_outlet_width: float = 22.4
    moving_outlet_length: float = 5.2
    bottom_shutter_local_rear_y: float = -17.4
    bottom_shutter_local_front_y: float = 2.1
    bottom_opaque_front_boundary_y: float = 20.0
    bottom_hidden_front_margin: float = 0.5
    bottom_fixed_backing_margin: float = 0.6

    # Four rails and eight bearing lands.
    rail_count: int = 4
    rail_z_offset: float = 9.5
    rail_radial_height: float = 1.2
    rail_tangential_width: float = 2.2
    groove_radial_depth: float = 0.65
    groove_width_nominal: float = 2.7
    groove_width_loose: float = 2.8
    radial_running_clearance: float = 0.20
    tangential_clearance_per_side: float = 0.25
    groove_bottom_x: float = 17.25
    bearing_boss_tangential_width: float = 3.5
    land_length: float = 3.4
    rear_land_local_y: float = -12.1
    front_land_local_y: float = -4.9
    rail_start_y: float = -15.70
    rail_end_y: float = 15.35
    rail_rear_lead_in: float = 0.7
    groove_mouth_length: float = 0.6
    groove_mouth_extra_width: float = 0.4
    groove_mouth_extra_depth: float = 0.3

    # Blind retained rear cover.
    rear_cover_width: float = 37.0
    rear_cover_height: float = 35.4
    rear_cover_thickness: float = 2.4
    rear_cover_back_y: float = -20.0
    rear_hook_count: int = 4
    rear_hook_tip_span: float = 38.9
    rear_hook_extraction_overlap: float = 0.8
    rear_hook_chamfer: float = 0.7
    rear_hook_cantilever_thickness: float = 1.2
    rear_hook_z_offset: float = 14.0
    rear_hook_height: float = 3.4
    rear_hook_beam_length: float = 2.4

    # Shutter-to-shuttle coupling interfaces.
    coupling_lug_width: float = 3.0
    coupling_lug_length: float = 1.2
    coupling_lug_engagement: float = 0.5
    coupling_socket_clearance: float = 0.2
    top_coupling_local_y: float = -11.0
    bottom_coupling_local_y: float = -5.0

    @property
    def latched_center_y(self) -> float:
        key_front_local = self.shuttle_front_y + self.key_face_thickness
        return self.housing_size / 2 - key_front_local

    @property
    def housing_inner_half_x(self) -> float:
        return self.rear_channel_width / 2

    @property
    def housing_inner_half_z(self) -> float:
        return self.rear_channel_height / 2

    @property
    def shuttle_inner_half_x(self) -> float:
        return self.shuttle_width / 2 - self.medicine_wall

    @property
    def shuttle_inner_half_z(self) -> float:
        return self.shuttle_height / 2 - self.medicine_wall

    @property
    def shuttle_inner_rear_y(self) -> float:
        return self.shuttle_rear_y + self.medicine_wall

    @property
    def shuttle_inner_front_y(self) -> float:
        return self.shuttle_front_y - self.medicine_wall

    @property
    def shutter_track_flange_width(self) -> float:
        return self.shutter_flange_width + 2 * self.shutter_lateral_clearance

    @property
    def shutter_track_web_width(self) -> float:
        return self.shutter_web_width + 2 * self.shutter_lateral_clearance

    @property
    def derived_lip_overlap(self) -> float:
        return (self.shutter_flange_width - self.shutter_track_web_width) / 2

    @property
    def top_web_bottom_z(self) -> float:
        return self.top_shutter_exterior_z - self.shutter_web_thickness

    @property
    def top_flange_bottom_z(self) -> float:
        return self.top_web_bottom_z - self.shutter_flange_thickness

    @property
    def top_track_floor_z(self) -> float:
        return self.top_flange_bottom_z - self.shutter_track_floor_clearance

    @property
    def top_track_lip_underside_z(self) -> float:
        return self.top_web_bottom_z + self.shutter_vertical_clearance

    @property
    def bottom_web_top_z(self) -> float:
        return self.bottom_shutter_exterior_z + self.shutter_web_thickness

    @property
    def bottom_flange_top_z(self) -> float:
        return self.bottom_web_top_z + self.shutter_flange_thickness

    @property
    def bottom_track_floor_z(self) -> float:
        return self.bottom_flange_top_z + self.shutter_track_floor_clearance

    @property
    def bottom_track_lip_underside_z(self) -> float:
        return self.bottom_web_top_z - self.shutter_vertical_clearance

    @property
    def bearing_boss_outer_x(self) -> float:
        return self.groove_bottom_x + self.groove_radial_depth

    @property
    def rail_tip_x(self) -> float:
        return self.groove_bottom_x + self.radial_running_clearance

    @property
    def rail_root_x(self) -> float:
        return self.rail_tip_x + self.rail_radial_height

    @property
    def tab_local_front_y(self) -> float:
        return self.front_shoulder_y - (
            self.latched_center_y + self.maximum_pull_state
        )

    @property
    def tab_local_rear_y(self) -> float:
        return self.tab_local_front_y - self.captive_tab_depth

    @property
    def tab_side_clearance(self) -> float:
        return (self.rear_channel_width - self.captive_tab_overall_width) / 2

    @property
    def tab_shoulder_overlap(self) -> float:
        return (
            self.captive_tab_overall_width - self.front_guide_width
        ) / 2

    @property
    def ready_endplay(self) -> float:
        ready_front = (
            self.latched_center_y
            + self.released_state
            + self.tab_local_front_y
        )
        return self.front_shoulder_y - ready_front

    @property
    def rear_key_vertical_clearance(self) -> float:
        return (self.rear_channel_height - self.key_face_size) / 2

    @property
    def rear_cover_side_clearance(self) -> float:
        return (self.rear_channel_width - self.rear_cover_width) / 2

    @property
    def rear_cover_vertical_clearance(self) -> float:
        return (self.rear_channel_height - self.rear_cover_height) / 2

    @property
    def rear_hook_tip_x(self) -> float:
        return self.rear_hook_tip_span / 2

    @property
    def rear_channel_half_width(self) -> float:
        return self.rear_channel_width / 2

    @property
    def derived_hook_overlap(self) -> float:
        return self.rear_hook_tip_x - self.rear_channel_half_width

    @property
    def bearing_center_spacing(self) -> float:
        return self.front_land_local_y - self.rear_land_local_y

    @property
    def bearing_end_to_end_span(self) -> float:
        return self.bearing_center_spacing + self.land_length

    def shuttle_center_y(self, state: float) -> float:
        if not self.inward_state <= state <= self.maximum_pull_state:
            raise ValueError("state outside P0 v2 hard-stop range")
        return self.latched_center_y + state

    def world_interval(self, local: Interval, state: float) -> Interval:
        center = self.shuttle_center_y(state)
        return (local[0] + center, local[1] + center)

    def top_shutter_interval(self, state: float) -> Interval:
        return self.world_interval(
            (self.top_shutter_local_rear_y, self.top_shutter_local_front_y),
            state,
        )

    def bottom_shutter_interval(self, state: float) -> Interval:
        return self.world_interval(
            (
                self.bottom_shutter_local_rear_y,
                self.bottom_shutter_local_front_y,
            ),
            state,
        )

    def fixed_fill_interval(self) -> Interval:
        return interval(self.fixed_fill_center_y, self.fixed_fill_length)

    def moving_fill_interval(self, state: float) -> Interval:
        return interval(
            self.shuttle_center_y(state) + self.moving_fill_local_center_y,
            self.moving_fill_length,
        )

    def fixed_outlet_interval(self) -> Interval:
        return interval(self.fixed_outlet_center_y, self.fixed_outlet_length)

    def moving_outlet_interval(self, state: float) -> Interval:
        return interval(
            self.shuttle_center_y(state) + self.moving_outlet_local_center_y,
            self.moving_outlet_length,
        )

    def fill_overlap(self, state: float) -> float:
        return overlap_length(
            self.fixed_fill_interval(), self.moving_fill_interval(state)
        )

    def outlet_overlap(self, state: float) -> float:
        return overlap_length(
            self.fixed_outlet_interval(), self.moving_outlet_interval(state)
        )

    def land_interval(self, state: float, local_y: float) -> Interval:
        return interval(self.shuttle_center_y(state) + local_y, self.land_length)


P0V2 = P0V2Spec()


__all__ = ["Interval", "P0V2", "P0V2Spec", "interval", "overlap_length"]
