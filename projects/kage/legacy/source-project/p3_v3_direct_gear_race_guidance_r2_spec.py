"""Revision-K frozen numeric contract for KAGE P3 V3 R2.

The module is intentionally isolated from the locked rollback variant.  It
contains only dimensions accepted by the Revision-K handoff; geometry and
exports live in the sibling ``_geometry`` and ``_export`` modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class P3V3DirectGearRaceGuidanceR2Spec:
    revision: str = "K"
    namespace: str = "p3_v3_direct_gear_race_guidance_r2"
    clock_outer_diameter: float = 300.00
    stationary_outer_radius: float = 150.00
    ring_teeth: int = 260
    pinion_teeth: int = 16
    gear_module: float = 1.00
    gear_ratio: float = 16.25
    carrier_race_radius: float = 131.60
    tooth_tip_radius: float = 129.00
    tooth_root_radius: float = 132.50
    ring_body_outer_radius: float = 138.90
    ring_body_inner_radius: float = 132.50
    shells_per_critical_pose: int = 4096
    motion_samples_per_revolution: int = 1040
    role_local_q_acceptance_abs_max_mm: float = 0.76
    role_local_powered_stop_abs_mm: float = 1.00
    role_local_service_stop_abs_mm: float = 1.25
    role_local_powered_margin_min_mm: float = 0.24
    fixed_axle_diameter_mm: float = 3.99
    fixed_axle_length_mm: float = 30.00
    cassette_pin_diameter_mm: float = 3.99
    cassette_pin_length_mm: float = 7.70
    production_printed_occurrence_count: int = 94
    fixed_setup_values_mm: tuple[float, ...] = (
        -1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00
    )
    roles: tuple[str, ...] = ("hour", "minute", "second")
    role_keys: tuple[str, ...] = ("H", "M", "S")
    role_colors: tuple[str, ...] = ("#df1455", "#e87500", "#087f79")
    carrier_layers: tuple[tuple[float, float], ...] = (
        (-2.75, -0.10), (3.95, 6.60), (10.65, 13.30)
    )
    pinion_face_ranges: tuple[tuple[float, float], ...] = (
        (-0.70, 1.40), (4.85, 6.95), (10.40, 12.50)
    )
    tooth_phase_offset_degrees: float = 0.6923076923076923
    # Pinion-only assembly clocking.  The production internal ring keeps the
    # locked tooth phase above; the 16T pinion is rotated half a tooth pitch
    # so its nominal state sits at the centre of the measured free mesh
    # window rather than in positive-volume tooth overlap.
    pinion_mesh_phase_trim_degrees: float = 11.25
    # Compact printable 1:1 miter pair.  The 5.11 mm orthogonal-axis offset
    # leaves a measured 0.100-0.133 mm free tooth clearance over the review
    # phase samples while retaining 16 explicit positive teeth per member.
    miter_pair_axis_offset_mm: float = 5.11
    miter_tooth_radial_length_mm: float = 0.60
    miter_tooth_tangential_width_mm: float = 0.10
    miter_tooth_height_mm: float = 1.50
    miter_tooth_z_start_mm: float = 0.30
    miter_tooth_center_radius_mm: float = 3.00
    # NEMA-8 drawing: D4 shaft, 7 +/-0.25 exposed length.  The review solid is
    # placed from the motor side and terminates just past the input-gear centre;
    # it must never be a symmetric witness that penetrates the output bevel.
    motor_shaft_reference_diameter_mm: float = 3.99
    motor_shaft_reference_length_mm: float = 7.00
    motor_shaft_input_center_overrun_mm: float = 0.40
    display_fin_angles: tuple[float, ...] = (305.0, 45.0, 145.0)
    fin_blade_radial_ranges: tuple[tuple[float, float], ...] = (
        (142.50, 143.70), (139.30, 140.50), (136.10, 137.30)
    )
    fin_blade_start_zs: tuple[float, ...] = (2.00, 8.70, 15.40)
    fin_tip_zs: tuple[float, ...] = (17.152, 21.1867, 24.2514)
    motor_station_angles_deg: tuple[float, ...] = (0.0, 120.0, 240.0)
    fixed_tower_angles_deg: tuple[float, ...] = (60.0, 180.0)
    local_cassette_angle_deg: float = 300.0
    rollback_model_root: Path = ROOT / "models" / "p3_v3_direct_gear_race_guidance_locked_pre_radial_visibility_20260818"
    model_root: Path = ROOT / "models" / "p3_v3_direct_gear_race_guidance_r2"


P3_V3_DIRECT_GEAR_RACE_R2 = P3V3DirectGearRaceGuidanceR2Spec()
