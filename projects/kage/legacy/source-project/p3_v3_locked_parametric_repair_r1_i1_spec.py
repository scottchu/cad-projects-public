"""Frozen I1 contract for the two fixed KAGE roller-tower axles.

Only the 60 and 180 degree fixed towers are owned here.  Every other clock
feature remains owned by the independently accepted R1 zero-delta baseline.
All dimensions are millimetres unless explicitly marked otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class ParameterContract:
    path: str
    units: str
    owner_group: str
    minimum: float
    maximum: float
    probe_value: Any


@dataclass(frozen=True)
class M3FlatPointSetScrewHardware:
    catalog_designation: str = "M3x2 ISO 4026 flat-point set screw; collar tapped M3x0.5"
    nominal_screw_diameter_mm: float = 3.00
    tap_pilot_diameter_mm: float = 2.50
    nominal_screw_length_mm: float = 2.00
    hex_socket_across_flats_mm: float = 1.50
    hex_socket_depth_mm: float = 1.00
    minimum_thread_engagement_mm: float = 1.50
    nominal_outer_face_recess_mm: float = 0.005
    adjustment_allowance_mm: float = 0.20
    rigid_overtravel_probe_mm: float = 0.05
    required_post_print_operation: str = "Tap D2.50 pilot M3x0.5 after printing"
    assembly_risk: str = "D2.50 pilot is not a finished M3 thread; tap before screw installation"

    def validate(self) -> None:
        if self.catalog_designation != "M3x2 ISO 4026 flat-point set screw; collar tapped M3x0.5":
            raise ValueError("catalog_designation: frozen ISO 4026 set-screw hardware required")
        if self.nominal_screw_diameter_mm != 3.0:
            raise ValueError("nominal_screw_diameter_mm: M3 required")
        if self.tap_pilot_diameter_mm >= self.nominal_screw_diameter_mm:
            raise ValueError("tap_pilot_diameter_mm: pilot must retain thread material")
        if self.nominal_screw_length_mm != 2.0:
            raise ValueError("nominal_screw_length_mm: ISO 4026 M3x2 required")
        if self.minimum_thread_engagement_mm < 1.5:
            raise ValueError("minimum_thread_engagement_mm: at least 1.5 mm required")
        if (self.hex_socket_across_flats_mm, self.hex_socket_depth_mm) != (1.5, 1.0):
            raise ValueError("hex socket: ISO 4026 M3 internal-hex envelope required")
        if self.nominal_outer_face_recess_mm != 0.005:
            raise ValueError("nominal_outer_face_recess_mm: 0.005 mm tangent datum required")
        if self.adjustment_allowance_mm != 0.20:
            raise ValueError("adjustment_allowance_mm: +/-0.20 mm required")
        if self.rigid_overtravel_probe_mm != 0.05:
            raise ValueError("rigid_overtravel_probe_mm: 0.05 mm fail-closed probe required")
        if self.required_post_print_operation != "Tap D2.50 pilot M3x0.5 after printing":
            raise ValueError("required_post_print_operation: M3 tapping step must be explicit")
        if "not a finished M3 thread" not in self.assembly_risk:
            raise ValueError("assembly_risk: unfinished pilot risk must be explicit")


@dataclass(frozen=True)
class FixedTowerParams:
    fixed_station_angles_deg: tuple[float, float] = (60.0, 180.0)
    tower_axis_radius_mm: float = 125.5
    leaf_seat_diameter_mm: float = 4.05
    leaf_seat_z_range_mm: tuple[float, float] = (-5.20, -2.20)
    minimum_leaf_bottom_wall_mm: float = 1.50
    upper_bridge_bore_diameter_mm: float = 4.06
    upper_bridge_z_range_mm: tuple[float, float] = (16.70, 19.70)
    axle_diameter_mm: float = 3.99
    axle_length_mm: float = 30.0
    axle_bottom_z_mm: float = -5.20
    washer_outer_diameter_mm: float = 8.0
    washer_bore_diameter_mm: float = 4.0
    washer_thickness_mm: float = 0.15
    collar_bore_diameter_mm: float = 4.0
    collar_outer_diameter_mm: float = 8.0
    collar_height_mm: float = 4.0
    collar_bottom_z_mm: float = 19.95
    collar_fastener_nominal_mm: float = 3.0
    nominal_endplay_mm: float = 0.10
    minimum_endplay_mm: float = 0.05
    maximum_endplay_mm: float = 0.15
    tool_withdrawal_diameter_mm: float = 6.50

    @property
    def leaf_seat_depth_mm(self) -> float:
        return self.leaf_seat_z_range_mm[1] - self.leaf_seat_z_range_mm[0]

    @property
    def leaf_seat_radial_clearance_mm(self) -> float:
        return (self.leaf_seat_diameter_mm - self.axle_diameter_mm) / 2.0

    @property
    def upper_bridge_radial_clearance_mm(self) -> float:
        return (self.upper_bridge_bore_diameter_mm - self.axle_diameter_mm) / 2.0

    @property
    def axle_top_z_mm(self) -> float:
        return self.axle_bottom_z_mm + self.axle_length_mm

    @property
    def stock_axle_length_mm(self) -> float:
        """Purchased pin length before the exterior-envelope service cut."""

        return self.axle_length_mm

    @property
    def installed_axle_span_mm(self) -> float:
        """True modeled pin span after trimming to accepted R1 Z=24.2514."""

        return 24.2514 - self.axle_bottom_z_mm

    @property
    def axle_trim_allowance_mm(self) -> float:
        return self.stock_axle_length_mm - self.installed_axle_span_mm

    @property
    def collar_top_z_mm(self) -> float:
        return self.collar_bottom_z_mm + self.collar_height_mm

    @property
    def support_plane_z_mm(self) -> tuple[float, float]:
        return (self.leaf_seat_z_range_mm[1], self.upper_bridge_z_range_mm[0])

    @property
    def support_span_mm(self) -> float:
        return self.support_plane_z_mm[1] - self.support_plane_z_mm[0]

    @property
    def retained_stack_top_z_mm(self) -> float:
        return self.upper_bridge_z_range_mm[1] + self.washer_thickness_mm

    @property
    def leaf_bottom_wall_mm(self) -> float:
        # I1 creates a local leaf floor down to Z=-6.70.
        return self.leaf_seat_z_range_mm[0] - (-6.70)

    def validate(self) -> None:
        if self.fixed_station_angles_deg != (60.0, 180.0):
            raise ValueError("fixed_station_angles_deg: fixed stations must remain 60 and 180 degrees")
        if self.tower_axis_radius_mm != 125.5:
            raise ValueError("tower_axis_radius_mm: fixed stations must remain at R125.5")
        if self.leaf_seat_diameter_mm <= self.axle_diameter_mm:
            raise ValueError("leaf_seat_diameter_mm: leaf seat and axle clearance required")
        if abs(self.leaf_seat_depth_mm - 3.0) > 1e-9:
            raise ValueError("leaf_seat_z_range_mm: seat depth must remain 3.0 mm")
        if self.minimum_leaf_bottom_wall_mm < 1.50 or self.leaf_bottom_wall_mm < self.minimum_leaf_bottom_wall_mm:
            raise ValueError("minimum_leaf_bottom_wall_mm: bottom wall must be at least 1.50 mm")
        if self.upper_bridge_bore_diameter_mm <= self.axle_diameter_mm:
            raise ValueError("upper_bridge_bore_diameter_mm: bridge clearance required around axle")
        if abs((self.upper_bridge_z_range_mm[1] - self.upper_bridge_z_range_mm[0]) - 3.0) > 1e-9:
            raise ValueError("upper_bridge_z_range_mm: bridge span must remain 3.0 mm")
        if self.axle_diameter_mm >= min(self.leaf_seat_diameter_mm, self.upper_bridge_bore_diameter_mm):
            raise ValueError("axle_diameter_mm: axle must clear both support bores")
        if abs(self.axle_length_mm - 30.0) > 1e-9:
            raise ValueError("axle_length_mm: axle length must remain 30.0 mm")
        if self.washer_thickness_mm <= 0.0:
            raise ValueError("washer_thickness_mm: washer thickness must be positive")
        if self.collar_bore_diameter_mm <= self.axle_diameter_mm:
            raise ValueError("collar_bore_diameter_mm: collar bore clearance required around axle")
        if self.collar_outer_diameter_mm < self.tool_withdrawal_diameter_mm:
            raise ValueError("collar_outer_diameter_mm: tool envelope requires collar OD at least tool diameter")
        if abs(self.collar_height_mm - 4.0) > 1e-9:
            raise ValueError("collar_height_mm: collar height must remain 4.0 mm")
        if abs(self.collar_fastener_nominal_mm - 3.0) > 1e-9:
            raise ValueError("collar_fastener_nominal_mm: M3 fastener is required")
        calculated_endplay = self.collar_bottom_z_mm - self.retained_stack_top_z_mm
        if not self.minimum_endplay_mm <= calculated_endplay <= self.maximum_endplay_mm:
            raise ValueError("collar_bottom_z_mm: calculated endplay must remain inside the required range")
        if not self.minimum_endplay_mm <= self.nominal_endplay_mm <= self.maximum_endplay_mm:
            raise ValueError("nominal_endplay_mm: endplay must remain inside the required range")
        if self.tool_withdrawal_diameter_mm < 6.50:
            raise ValueError("tool_withdrawal_diameter_mm: tool clearance must be at least 6.50 mm")


P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1 = FixedTowerParams()
P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1_SET_SCREW_HARDWARE = M3FlatPointSetScrewHardware()


_OWNER = {
    "leaf_seat_diameter_mm": "fixed_tower_leaves",
    "leaf_seat_z_range_mm": "fixed_tower_leaves",
    "minimum_leaf_bottom_wall_mm": "fixed_tower_leaves",
    "upper_bridge_bore_diameter_mm": "fixed_tower_bridges",
    "upper_bridge_z_range_mm": "fixed_tower_bridges",
    "washer_outer_diameter_mm": "fixed_tower_shims",
    "washer_bore_diameter_mm": "fixed_tower_shims",
    "washer_thickness_mm": "fixed_tower_shims",
}


_PROBES: dict[str, Any] = {
    "fixed_station_angles_deg": (60.0, 180.0),
    "tower_axis_radius_mm": 125.5,
    "leaf_seat_diameter_mm": 4.07,
    "leaf_seat_z_range_mm": (-5.20, -2.20),
    "minimum_leaf_bottom_wall_mm": 1.60,
    "upper_bridge_bore_diameter_mm": 4.08,
    "upper_bridge_z_range_mm": (16.70, 19.70),
    "axle_diameter_mm": 3.98,
    "axle_length_mm": 30.0,
    "axle_bottom_z_mm": -5.20,
    "washer_outer_diameter_mm": 8.1,
    "washer_bore_diameter_mm": 4.02,
    "washer_thickness_mm": 0.12,
    "collar_bore_diameter_mm": 4.02,
    "collar_outer_diameter_mm": 8.1,
    "collar_height_mm": 4.0,
    "collar_bottom_z_mm": 19.90,
    "collar_fastener_nominal_mm": 3.0,
    "nominal_endplay_mm": 0.10,
    "minimum_endplay_mm": 0.04,
    "maximum_endplay_mm": 0.16,
    "tool_withdrawal_diameter_mm": 6.70,
}


def parameter_schema(params: FixedTowerParams | None = None) -> dict[str, ParameterContract]:
    params = params or P3_V3_LOCKED_PARAMETRIC_REPAIR_R1_I1
    result = {}
    tuple_fields = {"fixed_station_angles_deg", "leaf_seat_z_range_mm", "upper_bridge_z_range_mm"}
    for field in fields(params):
        name = field.name
        result[name] = ParameterContract(
            path=name,
            units="deg" if name == "fixed_station_angles_deg" else "mm",
            owner_group=_OWNER.get(name, "fixed_tower_hardware"),
            minimum=0.0 if name in tuple_fields else -10.0,
            maximum=360.0 if name == "fixed_station_angles_deg" else 200.0,
            probe_value=_PROBES[name],
        )
    return result
