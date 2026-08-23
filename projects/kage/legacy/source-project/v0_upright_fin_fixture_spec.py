"""Frozen V0 four-part manual upright-fin optics fixture contract.

Coordinates are millimetres.  The wall is z=0 and +z points toward the viewer.
This is a manual optics fixture, not a quartz-compatible clock mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, degrees


@dataclass(frozen=True)
class CarrierSpec:
    name: str
    radius: float
    base_z: float
    tip_z: float
    target_tip_radius: float
    hub_od: float
    bore_diameter: float
    hub_height: float
    tower_od: float | None = None
    tower_height: float = 0.0

    @property
    def ring_bottom_z(self) -> float:
        return self.base_z - V0.ring_axial_thickness

    @property
    def local_height(self) -> float:
        return self.tip_z - self.ring_bottom_z

    @property
    def expected_xy(self) -> float:
        return 2.0 * (self.radius + V0.ring_radial_width / 2.0)


@dataclass(frozen=True)
class FixtureSpec:
    source_z: float = 60.0
    wall_z: float = 0.0
    body_diameter: float = 90.0
    body_height: float = 6.0
    mask_radius: float = 45.0
    projected_mask_radius: float = 50.0
    ring_radial_width: float = 1.6
    ring_axial_thickness: float = 1.2
    spoke_tangential_width: float = 2.0
    spoke_count: int = 3
    fin_radial_thickness: float = 1.6
    fin_tangential_width: float = 2.4
    fin_root_overlap: float = 0.2
    fin_tip_radius: float = 0.6
    root_flare_height: float = 1.2
    root_flare_width: float = 4.8
    lower_fit_diametral_clearance: float = 0.30
    hour_bore_diameter: float = 4.20
    hour_pad_tangential_width: float = 1.20
    hour_pad_radial_protrusion: float = 0.15
    hour_pad_interference: float = 0.05
    hour_slit_width: float = 1.0
    arbor_height: float = 24.30
    arbor_tip_chamfer_height: float = 0.40
    arbor_tip_diameter: float = 3.40
    nozzle_diameter: float = 0.4
    layer_height: float = 0.2

    @property
    def carriers(self) -> tuple[CarrierSpec, ...]:
        return (
            CarrierSpec("hour", 30.0, 22.5, 38.823529412, 85.0, 8.0, 4.20, 3.0),
            CarrierSpec("minute", 34.75, 16.5625, 41.045454545, 110.0, 10.0, 6.30, 1.2, 8.40, 5.9375),
            CarrierSpec("second", 39.5, 10.625, 41.769230769, 130.0, 12.0, 8.30, 1.2, 10.40, 5.9375),
        )

    @property
    def by_name(self) -> dict[str, CarrierSpec]:
        return {carrier.name: carrier for carrier in self.carriers}

    @property
    def arbor_segments(self) -> tuple[tuple[float, float, float], ...]:
        """(z0, z1, diameter), excluding final taper endpoint."""
        return (
            (6.0, 9.425, 12.0),
            (9.425, 10.625, 8.0),
            (10.625, 16.5625, 6.0),
            (16.5625, 23.90, 4.0),
        )


V0 = FixtureSpec()


def projected_radius(source_z: float, physical_radius: float, blocker_z: float) -> float:
    if not (source_z > blocker_z >= 0 and physical_radius > 0):
        raise ValueError("require source_z > blocker_z >= 0 and positive radius")
    return physical_radius * source_z / (source_z - blocker_z)


def required_half_angle(source_z: float, projected_radius_mm: float) -> float:
    return degrees(atan2(projected_radius_mm, source_z))


def validate_spec(spec: FixtureSpec = V0) -> None:
    if len(spec.carriers) != 3:
        raise ValueError("exactly three carriers are required")
    if spec.mask_radius * spec.source_z / (spec.source_z - spec.body_height) != spec.projected_mask_radius:
        raise ValueError("mask projection contract drift")
    if spec.ring_axial_thickness + 1e-9 < 6 * spec.layer_height:
        raise ValueError("ring must remain at least six layers")
    if spec.fin_radial_thickness + 1e-9 < 4 * spec.nozzle_diameter:
        raise ValueError("fin radial section must remain at least four nozzle widths")
    radii = [carrier.radius for carrier in spec.carriers]
    if any((b - a - spec.ring_radial_width) < 3.0 for a, b in zip(radii, radii[1:])):
        raise ValueError("carrier radial clearance below 3.0 mm")
    for carrier in spec.carriers:
        if abs(projected_radius(spec.source_z, carrier.radius, carrier.base_z) - 48.0) > 1e-6:
            raise ValueError(f"{carrier.name} shadow start drift")
        if abs(projected_radius(spec.source_z, carrier.radius, carrier.tip_z) - carrier.target_tip_radius) > 1e-6:
            raise ValueError(f"{carrier.name} shadow tip drift")


validate_spec()
