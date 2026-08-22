"""Frozen implementation contract for KAGE P2R3 Module A.

Coordinate convention:
- XY is parallel to the wall / clock face.
- +Z points from the wall toward the room viewer.
- The quartz case reference is behind the printed mount.

The MH011 / HR1688 envelope and shaft dimensions in this file are provisional
placeholders, not a universal compatibility claim.  The fit coupons are the
physical authority until a purchased movement is measured.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class ProvisionalQuartzReference:
    source_names: tuple[str, ...] = ("MH011", "HR1688")
    provenance: str = "user-nominated quartz families; step.parts exact/alias search returned no model"
    verification_state: str = "UNVERIFIED_PROVISIONAL_NONPRINTABLE_REFERENCE"
    case_width_x: float = 56.0
    case_height_y: float = 56.0
    case_depth_z: float = 16.2
    case_front_z: float = -15.4
    threaded_mount_diameter: float = 8.2
    shaft_nominal_od: tuple[float, float, float] = (5.0, 3.25, 0.75)
    shaft_attach_height_from_case_front: tuple[float, float, float] = (10.1, 13.5, 15.0)

    @property
    def case_rear_z(self) -> float:
        return self.case_front_z - self.case_depth_z

    @property
    def shaft_attach_z(self) -> tuple[float, float, float]:
        return tuple(
            self.case_front_z + height for height in self.shaft_attach_height_from_case_front
        )


@dataclass(frozen=True)
class DriverChannel:
    name: str
    shaft_nominal_od: float
    shaft_attach_z: float
    arm_z: tuple[float, float]
    magnet_face_z: float
    validation_radius: float
    production_radius: float
    hub_bore_candidates: tuple[float, float, float, float]
    counterweight_validation_radius: float
    counterweight_production_radius: float
    counterweight_cup_z: tuple[float, float]
    counterweight_tail_z_offset: float
    residual_target_gf_cm: float

    @property
    def arm_thickness(self) -> float:
        return self.arm_z[1] - self.arm_z[0]


@dataclass(frozen=True)
class QuartzDriverModuleSpec:
    quartz: ProvisionalQuartzReference = ProvisionalQuartzReference()

    mount_outer_diameter: float = 70.0
    mount_thickness: float = 2.4
    mount_rear_z: float = -15.4
    mount_bore_candidates: tuple[float, float, float, float] = (7.8, 8.0, 8.2, 8.4)
    mount_nominal_bore: float = 8.2

    arm_width: float = 3.2
    arm_thickness: float = 0.8
    hub_outer_diameter: float = 9.0
    magnet_nominal_diameter: float = 6.0
    magnet_nominal_thickness: float = 3.0
    magnet_pocket_diameter: float = 6.15
    magnet_pocket_depth: float = 3.10
    magnet_boss_outer_diameter: float = 9.0
    magnet_pocket_floor: float = 0.8
    magnet_face_recess: float = 0.1
    magnet_mass_g: float = 0.636

    counterweight_cup_length_x: float = 12.0
    counterweight_cup_width_y: float = 28.0
    counterweight_cup_height_z: float = 2.0
    counterweight_ballast_well_length_x: float = 10.0
    counterweight_ballast_well_width_y: float = 9.5
    counterweight_ballast_well_depth_z: float = 1.2
    counterweight_ballast_well_center_y: float = 7.75
    # The C-channel snaps over the 0.8 mm arm from one Z side.  Clearance is
    # specified per side; the rejected predecessor had only 0.30 mm total.
    counterweight_tail_clearance_y_per_side: float = 0.40
    counterweight_tail_clearance_z_per_side: float = 0.20
    # Worst-case installed cup float about its nominal axial plane.  Adjacent
    # corridors must remain separated when both cups float toward one another.
    counterweight_axial_float_z: float = 0.20
    counterweight_snap_opening_y: float = 3.00
    counterweight_adjustment_travel_x: float = 6.00
    counterweight_stop_length_x: float = 1.50
    counterweight_stop_width_y: float = 6.00
    counterweight_stop_gap_x: float = 0.30
    petg_density_g_per_cm3: float = 1.27
    # TP7 vendor reports a measured 7.2-7.4 g/cm3.  The CAD uses the lower
    # bound and requires a physical no-attraction check before installation.
    tungsten_putty_min_density_g_per_cm3: float = 7.20
    ballast_capacity_safety_factor: float = 1.20
    ballast_material_candidate: str = "TP7 tungsten-polymer putty"
    ballast_density_provenance: str = (
        "https://derbydust.com/products/tp7-tungsten-putty ; vendor measured 7.2-7.4 g/cm3"
    )
    ballast_magnetic_acceptance: str = (
        "PHYSICAL_GATE: no visible attraction to the installed 6x3 driver magnet at 5 mm"
    )

    coupon_boss_bore_candidates: tuple[float, float, float, float] = (7.8, 8.0, 8.2, 8.4)
    coupon_thickness_steps: tuple[float, float, float, float] = (1.5, 2.0, 2.5, 3.0)
    coupon_pad_length: float = 14.0
    coupon_pad_width: float = 14.0
    coupon_pitch: float = 16.0
    coupon_web_width: float = 3.0
    coupon_web_thickness: float = 1.5

    compact_dynamic_max_diameter: float = 150.0
    compact_angles_deg: tuple[float, float, float] = (0.0, 0.0, 0.0)

    p2r2_stable_file_count: int = 99
    p2r2_stable_manifest_sha256: str = (
        "0123bafc7142feac2dbf85c5144facbe2df466ecdd8d28b520bebcc9215b2c27"
    )

    @property
    def mount_front_z(self) -> float:
        return self.mount_rear_z + self.mount_thickness

    @property
    def magnet_boss_height(self) -> float:
        return self.magnet_pocket_depth + self.magnet_pocket_floor

    @property
    def channels(self) -> tuple[DriverChannel, DriverChannel, DriverChannel]:
        attach = self.quartz.shaft_attach_z
        return (
            DriverChannel(
                "hour", 5.0, attach[0], (-6.1, -5.3), -5.4, 32.0, 95.0,
                (4.8, 4.9, 5.0, 5.1), 22.0, 55.0, (-6.3, -4.3), 0.0, 1.0,
            ),
            DriverChannel(
                "minute", 3.25, attach[1], (-2.7, -1.9), -2.0, 51.0, 115.0,
                (3.05, 3.15, 3.25, 3.35), 44.0, 95.0, (-3.5, -1.5), 0.0, 1.0,
            ),
            DriverChannel(
                "second", 0.75, attach[2], (-1.2, -0.4), -0.5, 70.0, 135.0,
                (0.55, 0.65, 0.75, 0.85), 44.0, 75.0, (-0.9, 1.1), 0.5, 0.1,
            ),
        )

    def channel(self, name: str) -> DriverChannel:
        for channel in self.channels:
            if channel.name == name:
                return channel
        raise KeyError(name)

    def magnet_only_counterweight_mass_g(self, name: str, *, production: bool) -> float:
        channel = self.channel(name)
        driver_radius = channel.production_radius if production else channel.validation_radius
        counter_radius = (
            channel.counterweight_production_radius
            if production
            else channel.counterweight_validation_radius
        )
        return self.magnet_mass_g * driver_radius / counter_radius

    def magnet_torque_gf_cm(self, name: str, *, production: bool) -> float:
        channel = self.channel(name)
        radius = channel.production_radius if production else channel.validation_radius
        return self.magnet_mass_g * radius / 10.0

    @property
    def counterweight_tail_clearance_y(self) -> float:
        return 2.0 * self.counterweight_tail_clearance_y_per_side

    @property
    def counterweight_tail_clearance_z(self) -> float:
        return 2.0 * self.counterweight_tail_clearance_z_per_side

    @property
    def ballast_well_volume_cm3(self) -> float:
        return (
            2.0
            * self.counterweight_ballast_well_length_x
            * self.counterweight_ballast_well_width_y
            * self.counterweight_ballast_well_depth_z
            / 1000.0
        )

    @property
    def minimum_tungsten_putty_capacity_g(self) -> float:
        return self.ballast_well_volume_cm3 * self.tungsten_putty_min_density_g_per_cm3


P2R3A = QuartzDriverModuleSpec()


def validate_spec(spec: QuartzDriverModuleSpec = P2R3A) -> None:
    assert spec.quartz.verification_state.startswith("UNVERIFIED")
    assert spec.quartz.case_rear_z == -31.6
    assert spec.quartz.shaft_attach_z == (-5.300000000000001, -1.9000000000000004, -0.40000000000000036)
    assert tuple(round(channel.arm_thickness, 6) for channel in spec.channels) == (0.8, 0.8, 0.8)
    assert tuple(round(channel.shaft_attach_z, 6) for channel in spec.channels) == (-5.3, -1.9, -0.4)
    assert tuple(channel.validation_radius for channel in spec.channels) == (32.0, 51.0, 70.0)
    assert tuple(channel.production_radius for channel in spec.channels) == (95.0, 115.0, 135.0)
    assert isclose(spec.channels[1].arm_z[0] - spec.channels[0].arm_z[1], 2.6)
    assert isclose(spec.channels[2].arm_z[0] - spec.channels[1].arm_z[1], 0.7)
    assert min(2.6, 0.7) >= 0.4
    assert isclose(spec.magnet_boss_height, 3.9)
    assert spec.magnet_pocket_diameter == 6.15
    assert spec.magnet_pocket_depth == 3.10
    assert spec.magnet_pocket_floor == 0.8
    assert spec.magnet_face_recess == 0.1
    assert spec.coupon_thickness_steps == (1.5, 2.0, 2.5, 3.0)
    assert spec.counterweight_tail_clearance_y == 0.8
    assert spec.counterweight_tail_clearance_z == 0.4
    cup_gaps = tuple(
        spec.channels[index + 1].counterweight_cup_z[0]
        - spec.channels[index].counterweight_cup_z[1]
        for index in range(2)
    )
    assert all(isclose(observed, expected) for observed, expected in zip(cup_gaps, (0.8, 0.6)))
    assert min(cup_gaps) - 2.0 * spec.counterweight_axial_float_z >= 0.2 - 1e-9
    assert isclose(spec.ballast_well_volume_cm3, 0.228)
    assert isclose(spec.minimum_tungsten_putty_capacity_g, 1.6416)


validate_spec()
