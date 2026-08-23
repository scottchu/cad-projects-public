"""Frozen contract for KAGE P3 V1 six-lobe multi-material wheels.

XY is the clock plane, +Z faces the viewer, and -Z faces the wall.  P3 V1
changes only the drive/idler wheel material architecture.  Carrier, frame,
motor/Hall mounts, wheel axes, contact diameters, and preload remain P3 V0.
"""

from __future__ import annotations

from dataclasses import dataclass

from p3_v0_motor_outer_ring_spec import P3V0MotorOuterRingSpec, P3_V0


@dataclass(frozen=True)
class P3V1MotorOuterRingMultimaterialSpec:
    wheel_width: float = 2.60
    end_band_width: float = 0.60
    center_z_local: tuple[float, float] = (0.60, 2.00)
    lobe_count: int = 6
    lobe_samples_per_lobe: int = 24

    drive_contact_radius: float = 6.00
    drive_crest_radius: float = 5.00
    drive_valley_radius: float = 4.20
    drive_bore_diameter: float = 4.10

    idler_contact_radius: float = 4.00
    idler_crest_radius: float = 3.00
    idler_valley_radius: float = 2.40
    idler_bore_diameter: float = 3.20

    petg_material_name: str = "PETG"
    tpu_material_name: str = "TPU"
    petg_display_color: str = "#D8732A"
    tpu_display_color: str = "#25211F"
    three_mf_bed_size: float = 256.0
    three_mf_brim: float = 5.0

    @property
    def center_width(self) -> float:
        return self.center_z_local[1] - self.center_z_local[0]

    @property
    def drive_z(self) -> tuple[float, float]:
        return P3_V0.drive_z

    @property
    def idler_z(self) -> tuple[float, float]:
        return P3_V0.idler_z

    @property
    def drive_axis_radius(self) -> float:
        return P3_V0.motor_axis_radius_start

    @property
    def idler_axis_radius(self) -> float:
        return P3_V0.idler_axis_radius_start

    @property
    def drive_nominal_compression(self) -> float:
        return P3_V0.flange_radii[1] + self.drive_contact_radius - self.drive_axis_radius

    @property
    def idler_nominal_compression(self) -> float:
        return P3_V0.flange_radii[1] + self.idler_contact_radius - self.idler_axis_radius


P3_V1 = P3V1MotorOuterRingMultimaterialSpec()


P3_V0_SOURCE_SHA256 = {
    "p3_v0_motor_outer_ring_spec.py": "ab8279ef4812f1e28fb7e168bdae799bd889e71d185d38ad7a24e75dcc7bde41",
    "p3_v0_motor_outer_ring_geometry.py": "21e9612427a1f3ef18950f4c72ba985f9a51a064ce34321ecdc8304c1ed38861",
    "p3_v0_motor_outer_ring_export.py": "0a35ca9a290dbbcf501ac9a77b3f561e9d216a28a6019468912bbac65fae4035",
    "tests/test_p3_v0_motor_outer_ring.py": "096ffc8b5f7598ae9e430b53f63081b3b1f9ceb25d6db6fccac76fba6beb3dd2",
}


def validate_spec(
    p: P3V1MotorOuterRingMultimaterialSpec = P3_V1,
    v0: P3V0MotorOuterRingSpec = P3_V0,
) -> None:
    assert p.wheel_width == 2.60
    assert p.end_band_width == 0.60
    assert p.center_z_local == (0.60, 2.00)
    assert p.center_width == 1.40
    assert p.lobe_count == 6
    assert (p.drive_contact_radius, p.drive_crest_radius, p.drive_valley_radius) == (6.0, 5.0, 4.2)
    assert (p.idler_contact_radius, p.idler_crest_radius, p.idler_valley_radius) == (4.0, 3.0, 2.4)
    assert p.drive_bore_diameter == v0.drive_shaft_bore_diameter == 4.10
    assert p.idler_bore_diameter == v0.idler_bore_diameter == 3.20
    assert p.drive_z == v0.drive_z and p.idler_z == v0.idler_z
    assert p.drive_axis_radius == v0.motor_axis_radius_start
    assert p.idler_axis_radius == v0.idler_axis_radius_start
    assert abs(p.drive_nominal_compression - v0.nominal_compression) < 1e-9
    assert abs(p.drive_nominal_compression - 0.20) < 1e-9
    assert abs(p.idler_nominal_compression - v0.nominal_idler_compression) < 1e-9
    assert abs(p.idler_nominal_compression - 0.20) < 1e-9


validate_spec()
