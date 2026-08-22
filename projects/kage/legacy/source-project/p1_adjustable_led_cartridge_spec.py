"""Frozen dimensional contract for the P1 adjustable LED cartridge.

Coordinate convention: the wall is z=0 and +Z points into the room.  Every
moving-part placement is driven by the LED die/source plane on x=y=0.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class AdjustableLedCartridgeSpec:
    wall_z: float = 0.0
    mask_z: float = 6.0
    source_z_min: float = 36.0
    source_z_default: float = 40.0
    source_z_max: float = 86.0

    rail_x: float = 29.0
    rail_x_size: float = 4.0
    rail_y_size: float = 5.0
    bearing_outer_x: float = 6.0
    rail_clearance_per_side: float = 0.30
    rail_z_min: float = 30.0
    rail_z_max: float = 96.0
    frame_max_x: float = 72.0
    frame_max_y: float = 62.0
    bearing_land: float = 12.0

    carriage_stop_tab_half_height: float = 2.0
    front_stop_top_z: float = 34.0
    rear_stop_bottom_z: float = 88.0

    mcpcb_diameter: float = 20.0
    mcpcb_thickness: float = 1.6
    emitter_size: float = 3.45
    emitter_thickness: float = 0.6
    heatsink_x: float = 40.0
    heatsink_y: float = 40.0
    heatsink_depth: float = 30.0
    heatsink_base: float = 3.0
    hot_base_footprint: float = 24.0
    free_air_lateral: float = 5.0
    free_air_rear: float = 5.0
    decorative_pla_keepout: float = 10.0
    driver_clearance: float = 30.0

    m4_clearance_diameter: float = 4.5
    m4_nut_af: float = 7.2
    m4_nut_thickness: float = 3.4

    moving_wire_anchor_offset: float = 12.0
    wire_nominal_u_loop: float = 80.0
    wire_min_bend_radius: float = 15.0
    wire_lead_count: int = 2
    edge_clip_width: float = 6.0
    edge_clip_depth: float = 3.0
    edge_clip_height: float = 4.0
    clip_mount_size: float = 4.4
    clip_mount_clearance: float = 0.30

    v0r2_keepout_radius: float = 40.3
    v0r2_keepout_z_min: float = -16.0
    v0r2_keepout_z_max: float = 27.846

    @property
    def travel(self) -> float:
        return self.source_z_max - self.source_z_min

    @property
    def rail_clearance_size(self) -> float:
        return self.rail_y_size + 2 * self.rail_clearance_per_side

    @property
    def rail_x_clearance_size(self) -> float:
        return self.rail_x_size + 2 * self.rail_clearance_per_side

    @property
    def mask_distances(self) -> tuple[float, float, float]:
        return tuple(z - self.mask_z for z in self.source_positions)

    @property
    def source_positions(self) -> tuple[float, float, float]:
        return self.source_z_min, self.source_z_default, self.source_z_max

    @property
    def heatsink_front_offset(self) -> float:
        return self.mcpcb_thickness

    @property
    def heatsink_rear_offset(self) -> float:
        return self.mcpcb_thickness + self.heatsink_depth

    @property
    def free_air_half_x(self) -> float:
        return self.heatsink_x / 2 + self.free_air_lateral

    @property
    def decorative_keepout_half_x(self) -> float:
        return self.heatsink_x / 2 + self.decorative_pla_keepout

    @property
    def v0r2_keepout_volume(self) -> float:
        return pi * self.v0r2_keepout_radius**2 * (
            self.v0r2_keepout_z_max - self.v0r2_keepout_z_min
        )


P1 = AdjustableLedCartridgeSpec()


def validate_spec(spec: AdjustableLedCartridgeSpec = P1) -> None:
    assert spec.wall_z == 0.0 and spec.mask_z == 6.0
    assert spec.source_positions == (36.0, 40.0, 86.0)
    assert spec.mask_distances == (30.0, 34.0, 80.0)
    assert spec.travel == 50.0
    assert spec.rail_z_min == spec.source_z_min - spec.bearing_land / 2
    assert spec.rear_stop_bottom_z == spec.source_z_max + spec.carriage_stop_tab_half_height
    assert spec.front_stop_top_z == spec.source_z_min - spec.carriage_stop_tab_half_height
    assert spec.rail_z_max - spec.rail_z_min >= spec.travel
    assert spec.rail_clearance_size == 5.6
    assert 2 * (spec.rail_x + spec.rail_x_size / 2) <= spec.frame_max_x
    assert spec.rail_x - spec.bearing_outer_x / 2 > spec.free_air_half_x
    assert spec.heatsink_x + 2 * spec.free_air_lateral == 50.0
    assert spec.heatsink_x + 2 * spec.decorative_pla_keepout == 60.0
    assert spec.wire_nominal_u_loop >= 2 * spec.wire_min_bend_radius + spec.travel
    assert spec.v0r2_keepout_z_max < spec.rail_z_min
    assert spec.clip_mount_size + 2 * spec.clip_mount_clearance == 5.0


validate_spec()
