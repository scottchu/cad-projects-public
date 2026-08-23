"""Frozen, replaceable numeric contract for B4-R0 moving rings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_rings_b4_r0_segmented_fins_magnets"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class RingParameters:
    roles: tuple[str, ...] = ("hour", "minute", "second")
    teeth: int = 260
    module_mm: float = 1.0
    pitch_radius_mm: float = 130.0
    tip_radius_mm: float = 129.0
    root_radius_mm: float = 132.5
    race_radius_mm: float = 131.6
    body_outer_radius_mm: float = 138.9
    outer_diameter_mm: float = 277.8
    tooth_phase_deg: float = 0.6923077
    carrier_z_mm: tuple[tuple[float, float], ...] = ((-2.2,2.2),(4.5,8.9),(11.2,15.6))
    smooth_z_mm: tuple[tuple[float, float], ...] = ((-2.1,-0.1),(4.6,6.6),(11.3,13.3))
    tooth_z_mm: tuple[tuple[float, float], ...] = ((0.0,2.1),(6.7,8.8),(13.4,15.5))
    segment_names: tuple[str, ...] = ("A", "B", "C")
    segment_teeth: tuple[int, ...] = (87,87,86)
    segment_spans_deg: tuple[float, ...] = (120.461538,120.461538,119.076923)
    seam_angles_deg: tuple[float, ...] = (30.0,150.461538,270.923077)
    print_bbox_limit_mm: float = 255.0


@dataclass(frozen=True)
class FinParameters:
    datum_angle_deg: float = 0.0
    shelf_radii_mm: tuple[float,float] = (136.0,139.2)
    shelf_thickness_mm: float = 0.8
    blade_radii_mm: tuple[float,float] = (139.2,143.7)
    maximum_outer_diameter_mm: float = 287.4
    tangential_widths_mm: tuple[float,...] = (5.0,3.2,1.6)
    shelf_z_mm: tuple[tuple[float,float],...] = ((2.2,3.0),(8.9,9.7),(15.6,16.4))
    blade_z_mm: tuple[tuple[float,float],...] = ((3.0,7.2),(9.7,12.9),(16.4,18.6))
    root_fillet_mm: tuple[float,...] = (0.8,0.6,0.4)
    higher_ring_clearance_mm: float = 0.3
    roller_pinion_clearance_min_mm: float = 1.0


@dataclass(frozen=True)
class OpticalParameters:
    led_z_mm: float = 40.0
    wall_z_mm: float = -31.5
    expected_extensions_mm: tuple[float,...] = (35.1,39.4,44.1)

    def projection_extension(self, role_index: int) -> float:
        return self.expected_extensions_mm[role_index]


@dataclass(frozen=True)
class MagnetParameters:
    angle_deg: float = 180.0
    center_radius_mm: float = 136.2
    cavity_height_mm: float = 2.2
    skin_mm: float = 1.1
    cavity_diameters_mm: tuple[float,...] = (4.2,3.2,3.2)
    purchased_diameters_mm: tuple[float,...] = (4.0,3.0,3.0)
    purchased_thickness_mm: float = 2.0
    outer_wall_min_mm: float = 0.6
    polymer_density_g_cm3: float = 1.27
    magnet_density_g_cm3: float = 7.5
    com_eccentricity_max_mm: float = 0.5


@dataclass(frozen=True)
class FastenerParameters:
    lap_length_mm: float = 23.0
    lap_radial_width_mm: float = 6.4
    lap_split_mm: tuple[float,float] = (2.2,2.2)
    contact_area_min_mm2: float = 76.8
    nominal_contact_area_mm2: float = 78.38
    boss_radii_mm: tuple[float,float] = (134.0,138.7)
    boss_axial_mm: float = 5.8
    boss_tangential_length_mm: float = 12.0
    seam_relief_mm: float = 0.20
    seam_relief_radii_mm: tuple[float,float] = (133.35,138.90)
    role_clearance_mm: float = 0.9
    screw_name: str = "M3x12"
    screw_diameter_mm: float = 3.0
    screw_clearance_diameter_mm: float = 3.4
    screw_length_mm: float = 12.0
    screw_axis_radius_mm: float = 136.4
    nut_af_mm: float = 5.5
    nut_pocket_af_mm: float = 5.7
    nut_pocket_depth_mm: float = 2.6


@dataclass(frozen=True)
class B4Spec:
    ring: RingParameters = RingParameters()
    fin: FinParameters = FinParameters()
    optics: OpticalParameters = OpticalParameters()
    magnets: MagnetParameters = MagnetParameters()
    fasteners: FastenerParameters = FastenerParameters()
    q_mm: tuple[float,...] = (-0.35,0.0,0.10)
    independent_sweep_step_deg: float = 1.0
    coupled_state_count: int = 72
    brep_tolerance_mm3: float = 1e-6
    mesh_linear_deflection_mm: float = 0.08
    mesh_angular_deflection_rad: float = 0.15


SPEC = B4Spec()
