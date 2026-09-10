"""Frozen millimetre contract for the V2 keyboard/inverted-rail prototype."""

from dataclasses import dataclass


Interval = tuple[float, float]


@dataclass(frozen=True)
class P0MechanicalFitV2Spec:
    housing_size: float = 40.0
    housing_outer_corner_radius_xz: float = 4.0
    housing_rear_y: float = -18.7
    housing_front_y: float = 20.0
    main_guide_size_xz: float = 34.6
    main_guide_corner_radius_xz: float = 3.2
    front_guide_size_xz: float = 35.6
    front_guide_corner_radius_xz: float = 4.2
    front_guide_rear_y: float = 16.05
    front_bezel_chamfer: float = 1.0

    pressed_center_y: float = 4.5
    inward_state: float = -1.0
    pressed_state: float = 0.0
    released_state: float = 13.4
    maximum_pull_state: float = 13.55
    rejection_state: float = 13.6
    feed_start_center_y: float = -34.4
    feed_end_center_y: float = 4.5
    feed_step: float = 0.1

    inner_body_size_xz: float = 34.2
    inner_body_corner_radius_xz: float = 3.0
    inner_body_local_y: Interval = (-13.0, 12.5)
    key_skirt_size_xz: float = 34.2
    key_skirt_corner_radius_xz: float = 4.0
    key_face_size_xz: float = 32.8
    key_face_corner_radius_xz: float = 5.0
    key_local_y: Interval = (12.5, 15.5)

    male_rail_centres_z: tuple[float, float] = (-9.5, 9.5)
    male_rail_width_z: float = 2.2
    male_rail_external_height_x: float = 1.2
    male_rail_local_y: Interval = (-17.2, -3.2)
    male_rail_source_embed_x: float = 0.2
    female_channel_width_z: float = 2.6
    female_channel_depth_x: float = 1.2
    female_channel_rear_y: float = -18.7
    female_channel_blind_front_y: float = 14.85
    female_mouth_length_y: float = 0.8
    female_mouth_extra_width_z: float = 0.4
    female_mouth_extra_depth_x: float = 0.4
    blind_stop_wall_axial_thickness: float = 1.2
    spine_inner_x: float = 16.3
    spine_local_y: Interval = (-17.2, -12.8)

    rear_faceplate_exterior_y: float = -20.0
    rear_faceplate_interior_y: float = -18.7
    rear_pilot_size_xz: float = 34.2
    rear_pilot_corner_radius_xz: float = 3.0
    rear_pilot_front_y: float = -17.1

    side_latch_count: int = 2
    side_latch_width_z: float = 6.0
    side_latch_beam_thickness_x: float = 1.0
    side_latch_beam_inner_x: float = 16.95
    side_latch_beam_y: Interval = (-18.7, -9.85)
    side_latch_root_radius: float = 0.8
    side_latch_root_overlap: float = 0.2
    side_latch_root_faceplate_overlap_y: float = 0.2
    side_latch_root_tangent_local_y: float = 0.8
    side_latch_effective_length_y: float = 7.5
    side_latch_hook_base_local_y: Interval = (7.85, 8.75)
    side_latch_hook_apex_local_y: float = 8.3
    side_latch_hook_shoulder_local_y: float = 8.25
    side_latch_hook_shoulder_inner_x: float = 18.15
    side_latch_hook_apex_x: float = 18.6
    side_latch_hook_protrusion_x: float = 0.65
    side_latch_direct_insertion_travel_x: float = 0.55
    side_latch_required_hook_release_x: float = 0.55
    side_latch_pad_release_travel_x: float = 0.4
    side_latch_pad_squeeze_stop_x: float = 0.5
    side_latch_pad_load_distance_a: float = 6.0
    side_latch_pocket_width_z: float = 6.4
    side_latch_pocket_depth_x: float = 0.55
    side_latch_outer_skin_x: float = 1.3
    side_latch_pad_y: Interval = (-12.75, -11.05)
    side_latch_pad_width_z: float = 10.0
    side_latch_pad_thickness_x: float = 1.0
    side_latch_pad_inner_x: float = 18.6
    side_latch_connector_x: Interval = (17.75, 18.8)
    side_latch_connector_width_z: float = 6.0
    side_latch_broad_notch_x: Interval = (18.1, 20.2)
    side_latch_broad_notch_y: Interval = (-18.7, -10.85)
    side_latch_broad_notch_width_z: float = 10.4
    side_latch_rear_connector_slot_x: Interval = (16.9, 19.0)
    side_latch_forward_beam_passage_x: Interval = (16.75, 18.15)
    side_latch_forward_beam_passage_y: Interval = (-11.6, -9.65)
    side_latch_flex_slot_width_z: float = 6.4
    side_latch_pocket_x: Interval = (18.15, 18.7)
    side_latch_pocket_y: Interval = (-10.45, -9.85)

    @property
    def half_housing(self) -> float:
        return self.housing_size / 2

    @property
    def main_guide_half(self) -> float:
        return self.main_guide_size_xz / 2

    @property
    def inner_body_half(self) -> float:
        return self.inner_body_size_xz / 2

    @property
    def male_rail_source_x(self) -> Interval:
        return (
            self.inner_body_half - self.male_rail_source_embed_x,
            self.inner_body_half + self.male_rail_external_height_x,
        )

    @property
    def female_channel_x(self) -> Interval:
        return (
            self.main_guide_half,
            self.main_guide_half + self.female_channel_depth_x,
        )

    @property
    def female_mouth_x(self) -> Interval:
        return (
            self.main_guide_half,
            self.female_channel_x[1] + self.female_mouth_extra_depth_x,
        )

    @property
    def male_tip_x(self) -> float:
        return self.inner_body_half + self.male_rail_external_height_x

    @property
    def rail_radial_engagement(self) -> float:
        return self.male_tip_x - self.main_guide_half

    @property
    def minimum_opposite_rail_engagement(self) -> float:
        return self.rail_radial_engagement - (
            self.main_guide_size_xz - self.inner_body_size_xz
        ) / 2

    @property
    def rail_stop_contact_area_total(self) -> float:
        return 4 * self.rail_radial_engagement * self.male_rail_width_z

    @property
    def rail_front_local_y(self) -> float:
        return self.male_rail_local_y[1]

    def inner_center_y(self, state: float) -> float:
        return self.pressed_center_y + state

    def rail_world_y(self, state: float) -> Interval:
        center = self.inner_center_y(state)
        return tuple(center + value for value in self.male_rail_local_y)  # type: ignore[return-value]

    @property
    def released_endplay(self) -> float:
        return self.female_channel_blind_front_y - self.rail_world_y(self.released_state)[1]

    @property
    def rear_feed_first_entry_center_y(self) -> float:
        return self.female_channel_rear_y - self.rail_front_local_y

    def latch_strain(self, deflection: float) -> float:
        return (
            1.5
            * self.side_latch_beam_thickness_x
            * deflection
            / self.side_latch_effective_length_y**2
        )

    @property
    def side_latch_hook_pad_amplification(self) -> float:
        length = self.side_latch_effective_length_y
        a = self.side_latch_pad_load_distance_a
        return (3 * length - a) / (2 * a)

    @property
    def predicted_hook_release_travel(self) -> float:
        return self.side_latch_hook_pad_amplification * self.side_latch_pad_release_travel_x

    @property
    def predicted_hook_stop_travel(self) -> float:
        return self.side_latch_hook_pad_amplification * self.side_latch_pad_squeeze_stop_x

    def pad_load_strain(self, pad_travel: float) -> float:
        return (
            1.5
            * self.side_latch_beam_thickness_x
            * pad_travel
            / self.side_latch_pad_load_distance_a**2
        )


P0_MECHANICAL_FIT_V2 = P0MechanicalFitV2Spec()

__all__ = ["P0_MECHANICAL_FIT_V2", "P0MechanicalFitV2Spec"]
