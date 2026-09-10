"""Accepted dimensions for the isolated P0 mechanical-fit v1 prototype."""

from dataclasses import dataclass


Interval = tuple[float, float]


@dataclass(frozen=True)
class P0MechanicalFitV1Spec:
    """Frozen millimetre contract for exactly three printed parts."""

    housing_size: float = 40.0
    housing_fixed_rear_y: float = -18.7
    rear_channel_width: float = 37.3
    rear_channel_height: float = 35.8
    front_key_guide_width: float = 35.6
    front_shoulder_y: float = 15.35
    captive_stop_throat_width: float = 34.9
    captive_stop_pad_height: float = 5.4

    pressed_center_y: float = 4.5
    inward_state: float = -1.0
    pressed_state: float = 0.0
    released_state: float = 13.4
    maximum_pull_state: float = 13.55
    feed_start_center_y: float = -34.4
    feed_end_center_y: float = 4.5
    feed_step: float = 0.1

    key_face_size: float = 35.2
    key_face_thickness: float = 3.0
    inner_body_width_xz: float = 34.2
    inner_body_rear_local_y: float = -13.0
    inner_body_front_local_y: float = 12.5
    captive_tab_span: float = 36.9
    captive_tab_local_y: Interval = (-5.7, -2.7)
    captive_tab_height_z: float = 5.0
    # Localized underside/side reliefs are running interfaces, not cavity
    # openings. They are required for the key cap to pass the fixed rails and
    # front stop pads at pressed and future inward states.
    key_interface_relief_x: Interval = (17.25, 17.70)
    key_interface_relief_local_y: Interval = (12.30, 15.70)
    key_rail_relief_width_z: float = 2.80
    key_stop_relief_z: Interval = (-2.70, 2.70)

    rail_z_centres: tuple[float, float] = (-9.5, 9.5)
    rail_radial_height: float = 1.2
    rail_tangential_width: float = 2.2
    rail_root_x: float = 18.65
    rail_inner_tip_x: float = 17.45
    rail_global_y: Interval = (-18.7, 15.35)
    rail_rear_ramp: float = 0.7
    nominal_groove_width: float = 2.7
    nominal_radial_clearance: float = 0.2
    groove_bottom_x: float = 17.25
    groove_radial_depth: float = 0.65
    land_length: float = 6.8
    bearing_boss_width: float = 4.3
    normal_lip_per_side: float = 0.8
    mouth_length: float = 0.6
    mouth_width: float = 3.1
    mouth_lip_per_side: float = 0.6
    mouth_extra_radial_depth: float = 0.3
    rear_land_local_center_y: float = -13.8
    front_land_local_center_y: float = -6.6
    rear_backing_rib_radial_thickness: float = 0.8
    rear_backing_rib_body_overlap_y: float = 0.2

    rear_faceplate_exterior_y: float = -20.0
    rear_faceplate_interior_y: float = -18.7
    rear_cover_pilot_width: float = 36.9
    rear_cover_pilot_height: float = 35.3
    rear_cover_pilot_front_y: float = -17.1

    rear_snap_center_x: float = 16.2
    rear_snap_width: float = 3.6
    rear_snap_bending_thickness: float = 1.2
    rear_snap_root_fillet: float = 0.8
    rear_snap_root_overlap: float = 0.2
    rear_snap_root_tangent_y: float = 0.8
    rear_snap_effective_length: float = 7.5
    rear_snap_hook_base_rear_y: float = 7.75
    rear_snap_hook_apex_y: float = 8.3
    rear_snap_hook_base_front_y: float = 8.85
    rear_snap_top_beam_outer_z: float = 18.15
    rear_snap_top_hook_apex_z: float = 18.7
    rear_snap_bottom_beam_outer_z: float = -18.15
    rear_snap_bottom_hook_apex_z: float = -18.7
    rear_snap_pocket_width_x: float = 4.0
    rear_snap_pocket_rear_y: float = -10.95
    rear_snap_pocket_front_y: float = -9.85
    rear_snap_pocket_radial_depth: float = 0.65
    rear_snap_pocket_outer_z: float = 18.8
    rear_snap_nominal_deflection: float = 0.55
    rear_snap_worst_deflection: float = 0.65

    @property
    def half_housing(self) -> float:
        return self.housing_size / 2

    @property
    def inner_body_half(self) -> float:
        return self.inner_body_width_xz / 2

    @property
    def key_local_y(self) -> Interval:
        return (
            self.inner_body_front_local_y,
            self.inner_body_front_local_y + self.key_face_thickness,
        )

    @property
    def rear_land_local_y(self) -> Interval:
        return (
            self.rear_land_local_center_y - self.land_length / 2,
            self.rear_land_local_center_y + self.land_length / 2,
        )

    @property
    def front_land_local_y(self) -> Interval:
        return (
            self.front_land_local_center_y - self.land_length / 2,
            self.front_land_local_center_y + self.land_length / 2,
        )

    @property
    def rear_backing_rib_local_y(self) -> Interval:
        return (
            self.rear_land_local_y[0],
            self.inner_body_rear_local_y + self.rear_backing_rib_body_overlap_y,
        )

    @property
    def boss_outer_x(self) -> float:
        return self.groove_bottom_x + self.groove_radial_depth

    @property
    def stop_pad_width(self) -> float:
        return (self.rear_channel_width - self.captive_stop_throat_width) / 2

    @property
    def released_endplay(self) -> float:
        tab_front = (
            self.pressed_center_y
            + self.released_state
            + self.captive_tab_local_y[1]
        )
        return self.front_shoulder_y - tab_front

    @property
    def tab_stop_overlap_per_side(self) -> float:
        return (self.captive_tab_span - self.captive_stop_throat_width) / 2

    @property
    def full_depth_rail_y(self) -> Interval:
        return (self.rail_global_y[0] + self.rail_rear_ramp, self.rail_global_y[1])

    def inner_center_y(self, state: float) -> float:
        return self.pressed_center_y + state

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


P0_MECHANICAL_FIT_V1 = P0MechanicalFitV1Spec()

__all__ = ["P0_MECHANICAL_FIT_V1", "P0MechanicalFitV1Spec"]
