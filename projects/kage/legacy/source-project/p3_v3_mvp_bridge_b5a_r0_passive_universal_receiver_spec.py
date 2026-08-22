"""Frozen numeric contract for the B5A passive universal bridge/receiver MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_bridge_b5a_r0_passive_universal_receiver"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class RoleDatum:
    name: str
    anchor_angle_deg: float
    receiver_angle_deg: float
    mount_radius_mm: float
    band_radii_mm: tuple[float, float]
    band_angles_deg: tuple[float, float]
    receiver_top_z_mm: float

    @property
    def tongue_bottom_max_z_mm(self) -> float:
        return self.receiver_top_z_mm - 1.8


@dataclass(frozen=True)
class B5ASpec:
    roles: tuple[RoleDatum, ...] = (
        RoleDatum("hour", 60.0, 90.0, 118.0, (105.0, 110.0), (64.0, 88.0), -2.4),
        RoleDatum("minute", 180.0, 210.0, 118.0, (105.0, 110.0), (184.0, 208.0), 4.3),
        RoleDatum("second", 300.0, 330.0, 100.0, (92.0, 98.0), (304.0, 328.0), 11.0),
    )

    # Shared, unchanged B3 mounting interface.
    mount_axis_tangent_mm: tuple[float, float] = (-7.0, 7.0)
    inherited_mount_screw: str = "M3x8"
    capture_ear_outer_diameter_mm: float = 7.0
    capture_ear_bore_diameter_mm: float = 3.4
    capture_ear_z_mm: tuple[float, float] = (-3.60, -3.40)
    post_roller_web_z_mm: tuple[float, float] = (-3.60, -3.20)
    tower_geometry_z_change_mm: float = 0.0

    # Below-ring bridge and mast.
    structural_band_z_mm: tuple[float, float] = (-5.0, -3.0)
    overall_tangential_width_mm: float = 9.4
    escape_strut_width_mm: float = 4.0
    side_rib_width_mm: float = 1.5
    root_fillet_radius_mm: float = 2.0
    receiver_bulk_max_radius_mm: float = 128.4
    inherited_hour_roller_outer_diameter_mm: float = 30.0
    inherited_roller_axle_radius_mm: float = 118.0
    inherited_hour_roller_bottom_z_mm: float = -3.1
    stationary_roller_clearance_mm: float = 0.30

    # Universal receiver.  The channel is open at the center-side R114 entry
    # and continues through the R128.4 outboard mouth.
    receiver_floor_radii_mm: tuple[float, float] = (114.0, 128.4)
    clamp_axis_radius_mm: float = 119.0
    channel_width_mm: float = 6.40
    future_tongue_width_mm: float = 5.80
    sidewall_width_mm: float = 1.5
    floor_thickness_mm: float = 2.0
    future_tongue_max_thickness_mm: float = 1.8
    capture_lip_radial_length_mm: float = 2.2
    capture_lip_total_mm: float = 0.4
    capture_lip_thickness_mm: float = 0.4
    insertion_chamfer_mm: float = 0.5

    # Future-tongue slot and active radial datum.  Only the passive receiver
    # and datum gauge are modeled in B5A; no sensor/electronics body exists.
    tongue_slot_width_mm: float = 3.4
    tongue_slot_radial_length_mm: float = 5.1
    active_offset_from_slot_center_mm: float = 14.65
    active_radius_range_mm: tuple[float, float] = (132.8, 134.5)
    active_radius_nominal_mm: float = 134.0

    # Receiver-only purchased hardware witnesses.
    receiver_screw_name: str = "M3x10"
    receiver_screw_diameter_mm: float = 3.0
    receiver_screw_length_mm: float = 10.0
    receiver_screw_head_diameter_mm: float = 5.5
    receiver_screw_head_height_mm: float = 3.0
    receiver_clearance_diameter_mm: float = 3.4
    washer_id_mm: float = 3.2
    washer_od_mm: float = 7.0
    washer_thickness_mm: float = 0.5
    captured_nut_af_mm: float = 5.8
    purchased_nut_af_mm: float = 5.5
    captured_nut_thickness_mm: float = 2.5
    blind_tip_well_depth_mm: float = 3.5
    blind_floor_clearance_min_mm: float = 0.2
    inherited_driver_diameter_mm: float = 6.5
    driver_access_height_mm: float = 8.0

    # Datum-only alignment gauge.
    gauge_radial_length_mm: float = 22.0
    gauge_tangential_width_mm: float = 5.8
    gauge_thickness_mm: float = 1.8
    gauge_outboard_nose_mm: float = 6.5
    gauge_lead_in_mm: float = 0.30
    gauge_v_notch_depth_mm: float = 0.30
    gauge_v_notch_below_top_mm: float = 0.65
    gauge_label: str = "DATUM_ONLY_NO_SENSOR"

    q_mm: tuple[float, ...] = (-0.35, 0.0, 0.10)
    target_ring_clearance_min_mm: float = 0.20
    lower_ring_clearance_min_mm: float = 0.30
    fin_clearance_min_mm: float = 0.30
    brep_tolerance_mm3: float = 1e-6
    axis_tolerance_mm: float = 0.05
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15
    boolean_overshoot_mm: float = 1.0
    u1_usable_xy_mm: float = 260.0
    print_brim_mm: float = 5.0


SPEC = B5ASpec()
