"""Pure-Python kinematics for the three-rod 90 degree bend mechanism."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, radians, sin
from types import MappingProxyType
from typing import Mapping

from .parameters import DEFAULT_PARAMETERS, WIRE_DIAMETERS, PrototypeParameters


_EPSILON = 1e-12


@dataclass(frozen=True, slots=True)
class PointYZ:
    """A point or vector in the side-view mechanism plane."""

    y: float
    z: float

    def __add__(self, other: PointYZ) -> PointYZ:
        return PointYZ(self.y + other.y, self.z + other.z)

    def __sub__(self, other: PointYZ) -> PointYZ:
        return PointYZ(self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> PointYZ:
        return PointYZ(self.y * scalar, self.z * scalar)

    __rmul__ = __mul__

    def distance_to(self, other: PointYZ) -> float:
        return hypot(self.y - other.y, self.z - other.z)

    @property
    def magnitude(self) -> float:
        return hypot(self.y, self.z)


@dataclass(frozen=True, slots=True)
class _FiniteWire:
    start: PointYZ
    bend_start: PointYZ
    center: PointYZ
    arc_end: PointYZ
    end: PointYZ
    outgoing_unit: PointYZ
    angle_radians: float
    incoming_length: float
    arc_length: float
    outgoing_length: float
    points: tuple[PointYZ, ...]

    @property
    def exact_length(self) -> float:
        return self.incoming_length + self.arc_length + self.outgoing_length


@dataclass(frozen=True, slots=True)
class MechanismSolution:
    """Solved side-view geometry at one closure value."""

    parameters: PrototypeParameters
    wire_gauge: int
    wire_diameter: float
    wire_radius: float
    contact_radius: float
    available_lead_length: float
    incoming_length: float
    bend_arc_length: float
    outgoing_length: float
    path_length: float
    closure: float
    bend_angle_degrees: float
    upper_index: int
    lower_index: int

    bend_start: PointYZ
    bend_center: PointYZ
    vertical_leg_start: PointYZ
    wire_path: tuple[PointYZ, ...]
    wire_endpoint: PointYZ

    upper_rod_center: PointYZ
    lower_rod_center: PointYZ
    moving_rod_center: PointYZ
    moving_closed_center: PointYZ
    moving_outward_unit: PointYZ

    upper_contact: PointYZ
    lower_contact: PointYZ
    moving_contact: PointYZ
    contact_gaps: Mapping[str, float]
    minimum_required_lead_length: float
    upper_contact_reachable: bool
    usable: bool
    status: str

    left_moving_axis: PointYZ
    right_moving_axis: PointYZ
    screw_axis_direction: PointYZ
    ideal_skew: float
    frame_clearance: float
    pad_to_contact: float
    iron_to_petg_clearance: float

    @property
    def wire_angle_degrees(self) -> float:
        return self.bend_angle_degrees

    @property
    def rod_centers(self) -> Mapping[str, PointYZ]:
        return MappingProxyType(
            {
                "upper": self.upper_rod_center,
                "lower": self.lower_rod_center,
                "moving": self.moving_rod_center,
            }
        )

    @property
    def closed_rod_centers(self) -> Mapping[str, PointYZ]:
        return MappingProxyType(
            {
                "upper": self.upper_rod_center,
                "lower": self.lower_rod_center,
                "moving": self.moving_closed_center,
            }
        )

    @property
    def moving_retraction(self) -> float:
        return self.moving_rod_center.distance_to(self.moving_closed_center)

    @property
    def axis_collinearity_error(self) -> float:
        return abs(_cross(self.moving_outward_unit, self.screw_axis_direction))


def _cross(a: PointYZ, b: PointYZ) -> float:
    return a.y * b.z - a.z * b.y


def _finite_wire(
    params: PrototypeParameters,
    angle_degrees: float,
    lead_length: float,
    *,
    arc_samples: int = 48,
) -> _FiniteWire:
    """Construct a finite line-arc-line path without creating wire length."""

    angle = radians(angle_degrees)
    incoming = params.bend_start_y - params.pad_exit_y
    arc_length = params.bend_radius * angle
    outgoing = lead_length - incoming - arc_length
    if incoming <= 0.0:
        raise ValueError("bend start must be downstream of the pad exit")
    if outgoing < -_EPSILON:
        required = incoming + arc_length
        raise ValueError(
            f"available lead length {lead_length:g} is too short for the bend; "
            f"requires at least {required:.6g}"
        )
    outgoing = max(0.0, outgoing)

    start = PointYZ(params.pad_exit_y, params.wire_center_z)
    bend_start = PointYZ(params.bend_start_y, params.wire_center_z)
    center = PointYZ(params.bend_start_y, params.bend_center_z)
    arc_end = PointYZ(
        center.y + params.bend_radius * sin(angle),
        center.z - params.bend_radius * cos(angle),
    )
    tangent = PointYZ(cos(angle), sin(angle))
    end = arc_end + tangent * outgoing

    points = [start, bend_start]
    count = max(1, round(arc_samples * angle_degrees / 90.0))
    for index in range(1, count + 1):
        sample_angle = angle * index / count
        points.append(
            PointYZ(
                center.y + params.bend_radius * sin(sample_angle),
                center.z - params.bend_radius * cos(sample_angle),
            )
        )
    points.append(end)
    return _FiniteWire(
        start=start,
        bend_start=bend_start,
        center=center,
        arc_end=arc_end,
        end=end,
        outgoing_unit=tangent,
        angle_radians=angle,
        incoming_length=incoming,
        arc_length=arc_length,
        outgoing_length=outgoing,
        points=tuple(points),
    )


def _closest_on_segment(point: PointYZ, start: PointYZ, end: PointYZ) -> PointYZ:
    delta = end - start
    length_squared = delta.y * delta.y + delta.z * delta.z
    if length_squared <= _EPSILON:
        return start
    projection = ((point.y - start.y) * delta.y + (point.z - start.z) * delta.z) / length_squared
    projection = min(1.0, max(0.0, projection))
    return start + delta * projection


def _closest_on_arc(point: PointYZ, wire: _FiniteWire, radius: float) -> PointYZ:
    relative = point - wire.center
    if relative.magnitude <= _EPSILON:
        parameter = 0.0
    else:
        # Arc parameter q uses radial vector (sin(q), -cos(q)).
        parameter = atan2(relative.y, -relative.z)
    parameter = min(wire.angle_radians, max(0.0, parameter))
    return PointYZ(
        wire.center.y + radius * sin(parameter),
        wire.center.z - radius * cos(parameter),
    )


def _closest_on_wire(point: PointYZ, wire: _FiniteWire, radius: float) -> PointYZ:
    candidates = (
        _closest_on_segment(point, wire.start, wire.bend_start),
        _closest_on_arc(point, wire, radius),
        _closest_on_segment(point, wire.arc_end, wire.end),
    )
    return min(candidates, key=point.distance_to)


def solve_mechanism(
    params: PrototypeParameters = DEFAULT_PARAMETERS,
    wire_gauge: int = 12,
    closure: float = 1.0,
    upper_index: int = 1,
    lower_index: int = 1,
    available_lead_length: float | None = None,
) -> MechanismSolution:
    """Solve the finite-wire, ideal three-rod geometry.

    Reaction indices are zero-based (0..2).  The default middle position is
    index 1.  ``closure`` is zero with the forming rod fully retracted and one
    at the exact 90 degree closed state.
    """

    if wire_gauge not in WIRE_DIAMETERS:
        raise ValueError(f"unsupported wire gauge: {wire_gauge}")
    if not 0.0 <= closure <= 1.0:
        raise ValueError("closure must be between 0 and 1")
    if not 0 <= upper_index < params.reaction_position_count:
        raise IndexError("upper_index must be in range(3)")
    if not 0 <= lower_index < params.reaction_position_count:
        raise IndexError("lower_index must be in range(3)")

    lead_length = params.available_lead_length if available_lead_length is None else available_lead_length
    if lead_length <= 0.0:
        raise ValueError("available lead length must be positive")

    wire_diameter = WIRE_DIAMETERS[wire_gauge]
    wire_radius = wire_diameter / 2.0
    contact_radius = params.rod_radius + wire_radius
    slot_angle = radians(params.moving_angle_degrees)
    outward = PointYZ(cos(slot_angle), -sin(slot_angle))

    bend_angle = 90.0 * closure
    wire = _finite_wire(params, bend_angle, lead_length)
    bend_start = wire.bend_start
    bend_center = wire.center
    vertical_leg_start = PointYZ(params.vertical_leg_y, params.bend_center_z)

    lower_target = PointYZ(
        params.lower_reaction_y_positions[lower_index], params.wire_center_z
    )
    lower_center = PointYZ(lower_target.y, lower_target.z - contact_radius)

    upper_target = PointYZ(
        params.vertical_leg_y, params.upper_reaction_z_positions[upper_index]
    )
    upper_center = PointYZ(upper_target.y - contact_radius, upper_target.z)

    moving_target = bend_center + outward * params.bend_radius
    moving_closed = bend_center + outward * (params.bend_radius + contact_radius)
    retraction = params.moving_stroke * (1.0 - closure)
    moving_center = moving_closed + outward * retraction

    upper_contact = _closest_on_wire(upper_center, wire, params.bend_radius)
    lower_contact = _closest_on_wire(lower_center, wire, params.bend_radius)
    moving_contact = _closest_on_wire(moving_center, wire, params.bend_radius)
    centers_and_contacts = {
        "upper": (upper_center, upper_contact),
        "lower": (lower_center, lower_contact),
        "moving": (moving_center, moving_contact),
    }
    contact_gaps = MappingProxyType(
        {
            name: center.distance_to(contact) - contact_radius
            for name, (center, contact) in centers_and_contacts.items()
        }
    )

    required_length = (
        wire.incoming_length
        + params.bend_radius * pi / 2.0
        + (upper_target.z - params.bend_center_z)
    )
    reachable = lead_length + _EPSILON >= required_length
    usable = reachable and all(abs(gap) <= 1e-9 for gap in contact_gaps.values())
    status = "usable" if usable else "upper-contact-unreachable" if not reachable else "not-closed"

    return MechanismSolution(
        parameters=params,
        wire_gauge=wire_gauge,
        wire_diameter=wire_diameter,
        wire_radius=wire_radius,
        contact_radius=contact_radius,
        available_lead_length=lead_length,
        incoming_length=wire.incoming_length,
        bend_arc_length=wire.arc_length,
        outgoing_length=wire.outgoing_length,
        path_length=wire.exact_length,
        closure=closure,
        bend_angle_degrees=bend_angle,
        upper_index=upper_index,
        lower_index=lower_index,
        bend_start=bend_start,
        bend_center=bend_center,
        vertical_leg_start=vertical_leg_start,
        wire_path=wire.points,
        wire_endpoint=wire.end,
        upper_rod_center=upper_center,
        lower_rod_center=lower_center,
        moving_rod_center=moving_center,
        moving_closed_center=moving_closed,
        moving_outward_unit=outward,
        upper_contact=upper_contact,
        lower_contact=lower_contact,
        moving_contact=moving_contact,
        contact_gaps=contact_gaps,
        minimum_required_lead_length=required_length,
        upper_contact_reachable=reachable,
        usable=usable,
        status=status,
        left_moving_axis=moving_center,
        right_moving_axis=moving_center,
        screw_axis_direction=outward,
        ideal_skew=0.0,
        frame_clearance=params.nominal_frame_clearance,
        pad_to_contact=lower_target.y - params.pad_exit_y,
        iron_to_petg_clearance=params.designed_iron_to_petg_clearance,
    )
