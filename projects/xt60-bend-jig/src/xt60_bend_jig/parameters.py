"""Named design parameters for the XT60 pigtail bend-jig prototype.

All dimensions are millimetres.  X is the rod axis, Y runs from the solder
pad toward the bend, and Z is height above the base.
"""

from __future__ import annotations

from dataclasses import dataclass


WIRE_DIAMETERS: dict[int, float] = {12: 4.3, 14: 3.5}
"""Conservative insulated-wire outside diameters indexed by AWG."""

FIT_COUPON_SIZES: tuple[float, ...] = (4.2, 4.3, 4.4, 4.5)


@dataclass(frozen=True, slots=True)
class PrototypeParameters:
    """Single source of truth for the printable prototype and its mechanism."""

    rod_diameter: float = 4.0
    rod_length: float = 50.0
    clear_span: float = 38.0
    side_plate_thickness: float = 4.0

    wire_center_z: float = 10.0
    bend_start_y: float = 16.0
    bend_radius: float = 6.0
    pad_exit_y: float = -6.0
    available_lead_length: float = 44.0

    reaction_position_count: int = 3
    reaction_position_pitch: float = 6.5
    minimum_pad_to_contact: float = 6.0

    moving_angle_degrees: float = 45.0
    moving_stroke: float = 11.0
    slot_width: float = 4.6

    m4_screw_diameter: float = 4.0
    m4_clearance_diameter: float = 4.5
    m4_nut_across_flats: float = 7.0
    m4_nut_thickness: float = 3.2
    nut_trap_clearance_per_side: float = 0.1
    running_clearance_per_side: float = 0.25

    xt60_width: float = 15.9
    xt60_depth: float = 8.1
    xt60_length: float = 20.5
    cradle_clearance_per_side: float = 0.4

    reference_board_width: float = 36.0
    minimum_frame_clearance: float = 0.5
    minimum_iron_to_petg_clearance: float = 12.0
    designed_iron_to_petg_clearance: float = 12.0

    fit_coupon_sizes: tuple[float, ...] = FIT_COUPON_SIZES

    def __post_init__(self) -> None:
        positive = (
            self.rod_diameter,
            self.rod_length,
            self.clear_span,
            self.side_plate_thickness,
            self.bend_radius,
            self.available_lead_length,
            self.reaction_position_pitch,
            self.moving_stroke,
            self.slot_width,
            self.m4_screw_diameter,
            self.m4_clearance_diameter,
        )
        if any(value <= 0.0 for value in positive):
            raise ValueError("mechanism dimensions must be positive")
        if self.reaction_position_count != 3:
            raise ValueError("the prototype requires exactly three reaction positions")
        if self.reaction_position_pitch < 6.5:
            raise ValueError("reaction-position pitch must be at least 6.5 mm")
        if self.slot_width <= self.rod_diameter:
            raise ValueError("the moving slot must clear the 4 mm rod")
        if self.rod_length < self.outer_span:
            raise ValueError("rod length must span the outside faces of both plates")
        if not 0.0 < self.moving_angle_degrees < 90.0:
            raise ValueError("moving angle must be strictly between 0 and 90 degrees")
        if self.nominal_frame_clearance < self.minimum_frame_clearance:
            raise ValueError("designed frame clearance is below the acceptance limit")
        if self.designed_iron_to_petg_clearance < self.minimum_iron_to_petg_clearance:
            raise ValueError("PETG is too close to the soldering-iron keep-out")

    @property
    def rod_radius(self) -> float:
        return self.rod_diameter / 2.0

    @property
    def outer_span(self) -> float:
        return self.clear_span + 2.0 * self.side_plate_thickness

    @property
    def rod_end_protrusion(self) -> float:
        return (self.rod_length - self.outer_span) / 2.0

    @property
    def bend_center_z(self) -> float:
        return self.wire_center_z + self.bend_radius

    @property
    def vertical_leg_y(self) -> float:
        return self.bend_start_y + self.bend_radius

    @property
    def lower_reaction_y_positions(self) -> tuple[float, ...]:
        first = self.pad_exit_y + self.minimum_pad_to_contact
        return tuple(first + index * self.reaction_position_pitch for index in range(3))

    @property
    def upper_reaction_z_positions(self) -> tuple[float, ...]:
        first = self.bend_center_z + self.minimum_pad_to_contact
        return tuple(first + index * self.reaction_position_pitch for index in range(3))

    @property
    def cradle_opening(self) -> tuple[float, float, float]:
        allowance = 2.0 * self.cradle_clearance_per_side
        return (
            self.xt60_width + allowance,
            self.xt60_depth + allowance,
            self.xt60_length + allowance,
        )

    @property
    def m4_nut_trap_across_flats(self) -> float:
        return self.m4_nut_across_flats + 2.0 * self.nut_trap_clearance_per_side

    @property
    def nominal_frame_clearance(self) -> float:
        return (self.clear_span - self.reference_board_width) / 2.0


DEFAULT_PARAMETERS = PrototypeParameters()
