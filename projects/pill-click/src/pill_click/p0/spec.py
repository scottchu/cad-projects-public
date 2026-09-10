"""Frozen named dimensions and derived equations for the P0 manual slider.

Coordinate convention:

* X is left/right.
* Y is rear (-) to front/key (+).
* Z is bottom (-) to top/fill (+).
* ``s`` is shuttle travel from the pressed aperture-aligned pose.
"""

from dataclasses import dataclass


Interval = tuple[float, float]


def interval(center: float, length: float) -> Interval:
    """Return a closed one-dimensional interval."""

    return (center - length / 2, center + length / 2)


def overlap_length(first: Interval, second: Interval) -> float:
    """Return the non-negative overlap of two closed intervals."""

    return max(0.0, min(first[1], second[1]) - max(first[0], second[0]))


@dataclass(frozen=True)
class P0Spec:
    """P0-only dimensions in millimetres.

    This contract intentionally has no return spring, return magnet, cam,
    follower, or pill-transfer gate parameters.
    """

    # Fixed housing and rear insert.
    housing_size: float = 40.0
    housing_top_bottom_wall: float = 2.4
    rear_channel_width: float = 37.3
    front_guide_width: float = 34.9
    interior_height: float = 35.2
    front_shoulder_y: float = 15.35
    inward_stop_plane_y: float = 16.0
    key_recess_size: float = 35.6
    rear_insert_width: float = 37.0
    rear_insert_height: float = 34.9
    rear_insert_thickness: float = 2.0
    rear_insert_center_y: float = -19.0
    manual_access_width: float = 14.0
    manual_access_height: float = 12.0

    # Slider states.
    inward_state: float = -1.0
    pressed_state: float = 0.0
    released_state: float = 13.4
    maximum_pull_state: float = 13.55

    # Medicine shuttle and key.
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

    # Fill and outlet aperture timing.
    fill_width: float = 23.0
    fill_length: float = 10.0
    fill_fixed_center_y: float = -1.5
    fill_moving_local_center_y: float = -6.0
    outlet_width: float = 22.0
    outlet_length: float = 4.8
    outlet_fixed_center_y: float = 11.5
    outlet_moving_local_center_y: float = 7.0
    roof_closure_local_start_y: float = -25.4
    roof_closure_local_end_y: float = -13.4
    floor_closure_local_start_y: float = -9.8
    floor_closure_local_end_y: float = -3.0
    roof_tongue_width: float = 27.0

    # Four fixed rails and eight short moving bearing lands.
    rail_count: int = 4
    rail_z_offset: float = 9.5
    rail_radial_height: float = 1.2
    rail_tangential_width: float = 2.2
    groove_radial_depth: float = 0.65
    groove_width: float = 2.7
    groove_width_coupon_loose: float = 2.8
    radial_running_clearance: float = 0.20
    tangential_clearance_per_side: float = 0.25
    groove_bottom_x: float = 17.25
    bearing_boss_tangential_width: float = 3.5
    land_length: float = 3.4
    rear_land_local_y: float = -12.1
    front_land_local_y: float = -4.9
    rail_start_y: float = -15.70
    rail_end_y: float = 15.35

    @property
    def latched_center_y(self) -> float:
        """Center that places the key front flush at Y=+20 when s=0."""

        key_front_local = self.shuttle_front_y + self.key_face_thickness
        return self.housing_size / 2 - key_front_local

    @property
    def housing_inner_half_x(self) -> float:
        return self.rear_channel_width / 2

    @property
    def housing_side_wall(self) -> float:
        return self.housing_size / 2 - self.housing_inner_half_x

    @property
    def housing_inner_half_z(self) -> float:
        return self.interior_height / 2

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
        """Front face that contacts the shoulder only at maximum pull."""

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
        ready_tab_front = (
            self.latched_center_y
            + self.released_state
            + self.tab_local_front_y
        )
        return self.front_shoulder_y - ready_tab_front

    @property
    def bearing_center_spacing(self) -> float:
        return self.front_land_local_y - self.rear_land_local_y

    @property
    def bearing_end_to_end_span(self) -> float:
        return self.bearing_center_spacing + self.land_length

    def shuttle_center_y(self, state: float) -> float:
        if not self.inward_state <= state <= self.maximum_pull_state:
            raise ValueError(
                f"state must be between {self.inward_state} and "
                f"{self.maximum_pull_state} mm"
            )
        return self.latched_center_y + state

    def fixed_fill_interval(self) -> Interval:
        return interval(self.fill_fixed_center_y, self.fill_length)

    def moving_fill_interval(self, state: float) -> Interval:
        center = (
            self.shuttle_center_y(state) + self.fill_moving_local_center_y
        )
        return interval(center, self.fill_length)

    def fixed_outlet_interval(self) -> Interval:
        return interval(self.outlet_fixed_center_y, self.outlet_length)

    def moving_outlet_interval(self, state: float) -> Interval:
        center = (
            self.shuttle_center_y(state) + self.outlet_moving_local_center_y
        )
        return interval(center, self.outlet_length)

    def fill_overlap(self, state: float) -> float:
        return overlap_length(
            self.fixed_fill_interval(), self.moving_fill_interval(state)
        )

    def outlet_overlap(self, state: float) -> float:
        return overlap_length(
            self.fixed_outlet_interval(), self.moving_outlet_interval(state)
        )

    def fixed_interval_in_shuttle_frame(
        self, fixed_interval: Interval, state: float
    ) -> Interval:
        center = self.shuttle_center_y(state)
        return (fixed_interval[0] - center, fixed_interval[1] - center)

    def land_interval(self, state: float, local_center_y: float) -> Interval:
        center = self.shuttle_center_y(state) + local_center_y
        return interval(center, self.land_length)


P0 = P0Spec()


__all__ = ["Interval", "P0", "P0Spec", "interval", "overlap_length"]
