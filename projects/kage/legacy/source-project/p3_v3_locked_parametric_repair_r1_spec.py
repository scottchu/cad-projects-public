"""Phase-1 zero-delta parameter schema for the immutable KAGE assembly."""

from __future__ import annotations

from dataclasses import dataclass, fields
from math import isclose
from typing import Any, Mapping


class LockedParameterError(ValueError):
    """A protected parameter differs from the immutable locked default."""


class ValidationContractError(ValueError):
    """A parameter combination violates a measured design constraint."""


@dataclass(frozen=True)
class GlobalEnvelope:
    clock_outer_diameter_mm: float = 300.0
    stationary_outer_radius_mm: float = 150.0


@dataclass(frozen=True)
class RoleRings:
    carrier_layers_mm: tuple[tuple[float, float], ...] = ((-1.5, 1.5), (4.05, 7.05), (9.6, 12.6))
    pinion_face_ranges_mm: tuple[tuple[float, float], ...] = ((-0.7, 1.4), (4.85, 6.95), (10.4, 12.5))
    fin_angles_deg: tuple[float, float, float] = (305.0, 45.0, 145.0)
    fin_radial_ranges_mm: tuple[tuple[float, float], ...] = ((142.7, 143.9), (140.75, 141.95), (137.2, 138.4))
    fin_tangential_widths_mm: tuple[float, float, float] = (3.0, 2.0, 1.2)
    fin_start_z_mm: tuple[float, float, float] = (0.2, 5.3, 12.4)
    fin_tip_z_mm: tuple[float, float, float] = (17.152, 21.1867, 24.2514)


@dataclass(frozen=True)
class GearTrain:
    ring_teeth: int = 260
    pinion_teeth: int = 16
    module_mm: float = 1.0
    carrier_race_radius_mm: float = 131.6
    tooth_tip_radius_mm: float = 129.0
    tooth_root_radius_mm: float = 132.5
    ring_body_outer_radius_mm: float = 138.9
    output_axis_radius_mm: float = 122.0
    tooth_phase_offset_deg: float = 0.6923076923076923


@dataclass(frozen=True)
class MotorStations:
    station_angles_deg: tuple[float, float, float] = (0.0, 120.0, 240.0)
    service_adjustment_mm: float = 2.5
    powered_range_mm: tuple[float, float] = (-0.35, 0.10)
    mount_slot_width_mm: float = 3.6
    mount_slot_overall_length_mm: float = 8.6


@dataclass(frozen=True)
class FixedTowers:
    seat_bore_diameter_mm: float = 4.20
    axle_nominal_diameter_mm: float = 4.00


@dataclass(frozen=True)
class Spine:
    stationary_radius_limit_mm: float = 136.4
    minimum_wall_mm: float = 1.2


@dataclass(frozen=True)
class Cassettes:
    pin_bore_diameter_mm: float = 4.20
    pin_nominal_diameter_mm: float = 4.00


@dataclass(frozen=True)
class StopPlate:
    window_width_mm: float = 3.40
    required_clearance_mm: float = 0.20


@dataclass(frozen=True)
class Seams:
    recess_depth_mm: float = 1.00
    carrier_thickness_mm: float = 3.00


@dataclass(frozen=True)
class StationaryJoints:
    dowel_diameter_mm: float = 3.0
    joint_hole_diameter_mm: float = 2.2


@dataclass(frozen=True)
class HallBalance:
    hall_pocket_radius_mm: float = 137.0
    carrier_race_radius_mm: float = 131.6


@dataclass(frozen=True)
class Hardware:
    motor_mount_screw_nominal_mm: float = 3.0
    roller_axle_nominal_mm: float = 4.0


@dataclass(frozen=True)
class ServiceStates:
    # Existing locked mechanism supports this transform without changing any
    # source BREP.  It is the sole Phase-1 mutable parameter.
    motor_adjustments_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass(frozen=True)
class U1Layout:
    build_volume_mm: tuple[float, float, float] = (260.0, 260.0, 260.0)
    minimum_bed_margin_mm: float = 5.0


@dataclass(frozen=True)
class Validation:
    absolute_tolerance_mm: float = 1e-6
    require_exact_default_parity: bool = True


@dataclass(frozen=True)
class ParameterContract:
    path: str
    units: str
    minimum: float | int | None
    maximum: float | int | None
    locked: bool
    owner_labels: tuple[str, ...]
    effect: str
    probe_value: Any = None


@dataclass(frozen=True)
class P3V3LockedParametricRepairR1:
    global_envelope: GlobalEnvelope = GlobalEnvelope()
    role_rings: RoleRings = RoleRings()
    gear_train: GearTrain = GearTrain()
    motor_stations: MotorStations = MotorStations()
    fixed_towers: FixedTowers = FixedTowers()
    spine: Spine = Spine()
    cassettes: Cassettes = Cassettes()
    stop_plate: StopPlate = StopPlate()
    seams: Seams = Seams()
    stationary_joints: StationaryJoints = StationaryJoints()
    hall_balance: HallBalance = HallBalance()
    hardware: Hardware = Hardware()
    service_states: ServiceStates = ServiceStates()
    u1_layout: U1Layout = U1Layout()
    validation: Validation = Validation()

    @property
    def parameter_groups(self) -> Mapping[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}

    @property
    def field_ownership(self) -> Mapping[str, tuple[str, ...]]:
        return {
            path: tuple(contract.owner_labels)
            for group in parameter_schema(self).values()
            for path, contract in ((c.path, c) for c in group.values())
        }

    @property
    def outer_radius_mm(self) -> float:
        return self.global_envelope.clock_outer_diameter_mm / 2.0

    @property
    def gear_ratio(self) -> float:
        return self.gear_train.ring_teeth / self.gear_train.pinion_teeth

    @property
    def ring_pitch_radius_mm(self) -> float:
        return self.gear_train.module_mm * self.gear_train.ring_teeth / 2.0

    @property
    def pinion_pitch_radius_mm(self) -> float:
        return self.gear_train.module_mm * self.gear_train.pinion_teeth / 2.0

    @property
    def quadrant_teeth(self) -> int:
        return self.gear_train.ring_teeth // 4

    @property
    def motor_slot_center_travel_mm(self) -> float:
        return self.motor_stations.mount_slot_overall_length_mm - self.motor_stations.mount_slot_width_mm

    @property
    def u1_usable_xy_mm(self) -> float:
        return self.u1_layout.build_volume_mm[0] - 2.0 * self.u1_layout.minimum_bed_margin_mm

    @property
    def fin_heights_mm(self) -> tuple[float, float, float]:
        return tuple(tip - start for start, tip in zip(self.role_rings.fin_start_z_mm, self.role_rings.fin_tip_z_mm, strict=True))

    @property
    def fin_radial_lengths_mm(self) -> tuple[float, float, float]:
        return tuple(r1 - r0 for r0, r1 in self.role_rings.fin_radial_ranges_mm)

    def validate(self) -> None:
        baseline = P3_V3_LOCKED_PARAMETRIC_REPAIR_R1
        schema = parameter_schema(baseline)

        # Combination checks run before the generic lock gate so an invalid
        # replacement reports the measured requirement that it violates.
        if self.motor_stations.service_adjustment_mm < 0:
            raise ValidationContractError("motor_stations.service_adjustment_mm service_adjustment must be nonnegative as required")
        if self.fixed_towers.seat_bore_diameter_mm < self.fixed_towers.axle_nominal_diameter_mm + 0.10:
            raise ValidationContractError("fixed_towers.seat_bore_diameter_mm seat_bore clearance must be at least 0.10 mm required")
        if self.cassettes.pin_bore_diameter_mm < self.cassettes.pin_nominal_diameter_mm + 0.10:
            raise ValidationContractError("cassettes.pin_bore_diameter_mm pin_bore clearance must be at least 0.10 mm required")
        if self.stop_plate.window_width_mm < 3.0 + self.stop_plate.required_clearance_mm:
            raise ValidationContractError("stop_plate.window_width_mm window_width clearance must be at least 3.20 mm required")
        if self.seams.recess_depth_mm >= self.seams.carrier_thickness_mm / 2.0:
            raise ValidationContractError("seams.recess_depth_mm recess_depth must retain required half-thickness material")
        if self.hall_balance.hall_pocket_radius_mm <= self.hall_balance.carrier_race_radius_mm:
            raise ValidationContractError("hall_balance.hall_pocket_radius_mm hall_pocket clearance must remain outside required race radius")
        if self.u1_layout.minimum_bed_margin_mm * 2.0 >= min(self.u1_layout.build_volume_mm[:2]):
            raise ValidationContractError("u1_layout.minimum_bed_margin_mm minimum_bed_margin must leave required positive build area")
        for group_name, group in self.parameter_groups.items():
            baseline_group = getattr(baseline, group_name)
            for data_field in fields(group):
                path = f"{group_name}.{data_field.name}"
                value = getattr(group, data_field.name)
                contract = schema[group_name][data_field.name]
                if contract.locked and value != getattr(baseline_group, data_field.name):
                    raise LockedParameterError(f"{path} is locked to the immutable baseline")
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    if contract.minimum is not None and value < contract.minimum:
                        raise ValidationContractError(f"{path} outside required minimum {contract.minimum}")
                    if contract.maximum is not None and value > contract.maximum:
                        raise ValidationContractError(f"{path} outside required maximum {contract.maximum}")

        service = self.motor_stations.service_adjustment_mm
        for value in self.service_states.motor_adjustments_mm:
            if value < -service or value > service:
                raise ValidationContractError("service_states.motor_adjustments_mm outside required physical service range")
        if not isclose(self.outer_radius_mm, self.global_envelope.stationary_outer_radius_mm, abs_tol=1e-12):
            raise ValidationContractError("global_envelope radii must satisfy required diameter equation")
        if self.gear_train.ring_teeth % 4:
            raise ValidationContractError("gear_train.ring_teeth must be divisible by four for required quadrants")


_LOCKED_OCCURRENCE_NAMES = tuple(f"occurrence_{index:03d}" for index in range(201))


def parameter_schema(params: P3V3LockedParametricRepairR1) -> Mapping[str, Mapping[str, ParameterContract]]:
    """Return a complete contract row for every public group field."""

    result: dict[str, dict[str, ParameterContract]] = {}
    for group_name, group in params.parameter_groups.items():
        result[group_name] = {}
        for data_field in fields(group):
            path = f"{group_name}.{data_field.name}"
            value = getattr(group, data_field.name)
            units = "bool" if isinstance(value, bool) else "enum" if isinstance(value, str) else "count" if isinstance(value, int) else "deg" if "deg" in data_field.name else "ratio" if "ratio" in data_field.name else "mm"
            locked = path != "service_states.motor_adjustments_mm"
            # Phase 1 keeps a deliberately broad fail-closed owner set.  It
            # authorizes no local BREP edits; the one mutable service-state
            # transform is checked by occurrence diff before acceptance.
            owners = _LOCKED_OCCURRENCE_NAMES
            minimum = maximum = value if isinstance(value, (int, float)) and not isinstance(value, bool) and locked else None
            probe = (0.05, 0.05, 0.05) if path == "service_states.motor_adjustments_mm" else None
            effect = "transform" if path == "service_states.motor_adjustments_mm" else "geometry" if group_name not in {"validation", "u1_layout"} else "metadata"
            result[group_name][data_field.name] = ParameterContract(path, units, minimum, maximum, locked, owners, effect, probe)
    return result


P3_V3_LOCKED_PARAMETRIC_REPAIR_R1 = P3V3LockedParametricRepairR1()
