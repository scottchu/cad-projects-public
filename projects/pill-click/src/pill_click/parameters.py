"""Frozen v0 dimensions and state positions for Pill Click."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PillClickParameters:
    """Dimensions in millimetres; X width, Y rear-to-front, Z up.

    ``s`` is shuttle travel relative to the latched position.  Positive S is
    outward/ready and a press moves toward negative Y.
    """

    housing_size: float = 40.0
    housing_depth: float = 40.0
    wall: float = 2.4
    back_cover_thickness: float = 2.4
    trap_plate_thickness: float = 0.8
    corner_radius: float = 4.0

    latched_state: float = 0.0
    ready_state: float = 13.4
    inward_stop_state: float = -1.0

    sliding_clearance: float = 0.35
    front_guide_size: float = 34.9
    rear_tab_channel: float = 37.3
    shoulder_y: float = 15.8
    ready_tab_front_y: float = 15.4
    inward_stop_plane_y: float = 16.0

    key_face_size: float = 35.2
    key_face_thickness: float = 3.0
    key_face_radius: float = 3.6
    key_taper: float = 1.4

    shuttle_width: float = 34.2
    shuttle_height: float = 34.2
    shuttle_depth: float = 25.0
    shuttle_wall: float = 2.0
    loading_port_width: float = 23.0
    loading_port_depth: float = 10.0
    loading_port_center_y: float = 11.5
    outlet_width: float = 22.0
    outlet_depth: float = 4.8
    outlet_local_y: float = 7.0
    outlet_closed_state: float = 4.8
    gate_open_state: float = 5.8
    transfer_slope_drop: float = 3.0

    captive_tab_depth: float = 3.0
    captive_tab_height: float = 5.0
    captive_overlap: float = 1.55

    gate_blade_width: float = 22.0
    gate_blade_depth: float = 1.9
    gate_blade_height: float = 3.4
    gate_dam_width: float = 22.8
    gate_dam_depth: float = 2.0
    gate_vertical_overlap: float = 0.9
    gate_chamfer: float = 0.6

    follower_pin_diameter: float = 2.2
    cam_groove_width: float = 3.0
    cam_groove_depth: float = 1.7
    cam_plate_thickness: float = 3.2
    cam_branch_spacing: float = 4.2
    cam_overtravel: float = 1.0
    follower_beam_thickness: float = 1.2
    follower_beam_width: float = 4.0

    spring_thickness: float = 1.6
    spring_width: float = 5.0
    spring_depth: float = 18.0
    spring_turns: int = 3

    magnet_diameter: float = 6.0
    magnet_thickness: float = 2.0
    magnet_pocket_diameter: float = 6.1
    magnet_pocket_depth: float = 2.1
    magnet_min_gap: float = 1.2
    fridge_magnet_offset_x: float = 11.5

    @property
    def travel(self) -> float:
        """Stable latched-to-ready span retained for compatibility."""

        return self.ready_state - self.latched_state

    @property
    def total_press_span(self) -> float:
        return self.ready_state - self.inward_stop_state

    @property
    def latched_shuttle_center_y(self) -> float:
        return (
            self.housing_depth / 2
            - self.key_face_thickness
            - self.shuttle_depth / 2
        )

    @property
    def tab_local_front_y(self) -> float:
        ready_center = self.latched_shuttle_center_y + self.ready_state
        return self.ready_tab_front_y - ready_center


DEFAULTS = PillClickParameters()
