"""Frozen V0R2 compact fixture with shadow-readable hand identities."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, degrees, hypot


@dataclass(frozen=True)
class FinIdentitySpec:
    stem_width: float
    crown_height: float
    crown_width: float


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
    def ring_bottom_z(self):
        return self.base_z - V0R2.ring_axial_thickness

    @property
    def local_height(self):
        return self.tip_z - self.ring_bottom_z


@dataclass(frozen=True)
class IdentifiableFinFixtureSpec:
    source_z: float = 40.0
    wall_z: float = 0.0
    body_x: float = 56.0
    body_y: float = 56.7
    body_depth: float = 16.0
    body_corner_radius: float = 3.0
    ring_radial_width: float = 1.6
    ring_axial_thickness: float = 1.2
    spoke_tangential_width: float = 2.0
    fin_radial_thickness: float = 1.6
    fin_root_overlap: float = 0.2
    lower_tower_height: float = 3.958333333
    lower_fit_diametral_clearance: float = 0.30
    hour_bore_diameter: float = 4.20
    hour_pad_tangential_width: float = 1.20
    hour_pad_radial_protrusion: float = 0.15
    hour_pad_interference: float = 0.05
    hour_slit_width: float = 1.0
    arbor_global_top: float = 17.2
    arbor_chamfer_height: float = 0.4
    nozzle_diameter: float = 0.4
    layer_height: float = 0.2

    @property
    def body_corner_envelope_radius(self):
        return hypot(self.body_x / 2, self.body_y / 2)

    @property
    def body_local_height(self):
        return self.body_depth + self.arbor_global_top

    @property
    def carriers(self):
        return (
            CarrierSpec("hour", 30.0, 15.0, 25.882352941, 85.0, 8.0, 4.20, 3.0),
            CarrierSpec(
                "minute", 34.75, 11.041666667, 27.363636364, 110.0,
                10.0, 6.30, 1.2, 8.40, self.lower_tower_height,
            ),
            CarrierSpec(
                "second", 39.5, 7.083333333, 27.846153846, 130.0,
                12.0, 8.30, 1.2, 10.40, self.lower_tower_height,
            ),
        )

    @property
    def by_name(self):
        return {carrier.name: carrier for carrier in self.carriers}

    @property
    def fin_identities(self):
        return {
            "hour": FinIdentitySpec(4.8, 0.8, 3.2),
            "minute": FinIdentitySpec(3.2, 0.8, 1.6),
            "second": FinIdentitySpec(1.6, 0.6, 0.4),
        }

    @property
    def arbor_segments_global(self):
        return (
            (0.0, 5.883333333, 12.0),
            (5.883333333, 7.083333333, 8.0),
            (7.083333333, 11.041666667, 6.0),
            (11.041666667, 16.8, 4.0),
        )


V0R2 = IdentifiableFinFixtureSpec()


def projected_radius(source_z: float, radius: float, blocker_z: float) -> float:
    if not (source_z > blocker_z >= 0 and radius > 0):
        raise ValueError("invalid projection ordering")
    return radius * source_z / (source_z - blocker_z)


def projected_tangential_width(source_z: float, width: float, blocker_z: float) -> float:
    """Project a tangential blocker width from axial z onto the wall."""
    if not (source_z > blocker_z >= 0 and width > 0):
        raise ValueError("invalid projection ordering")
    return width * source_z / (source_z - blocker_z)


def blocker_z_at_projected_radius(source_z: float, carrier_radius: float, wall_radius: float) -> float:
    """Return blocker z whose point-source projection reaches ``wall_radius``."""
    if not (source_z > 0 and 0 < carrier_radius <= wall_radius):
        raise ValueError("invalid projected radius")
    return source_z * (1.0 - carrier_radius / wall_radius)


def fin_physical_width_at_local_z(
    carrier: CarrierSpec,
    local_z: float,
    spec: IdentifiableFinFixtureSpec = V0R2,
) -> float:
    """Exact stem/crown width of one upright fin at part-local z."""
    identity = spec.fin_identities[carrier.name]
    root_z = spec.ring_axial_thickness - spec.fin_root_overlap
    if local_z < root_z - 1e-9 or local_z > carrier.local_height + 1e-9:
        raise ValueError("local z outside fin")
    crown_base = carrier.local_height - identity.crown_height
    if local_z <= crown_base:
        return identity.stem_width
    fraction = (local_z - crown_base) / identity.crown_height
    return identity.stem_width + fraction * (identity.crown_width - identity.stem_width)


def fin_projected_width_at_local_z(
    carrier: CarrierSpec,
    local_z: float,
    spec: IdentifiableFinFixtureSpec = V0R2,
) -> float:
    global_z = carrier.ring_bottom_z + local_z
    return projected_tangential_width(
        spec.source_z,
        fin_physical_width_at_local_z(carrier, local_z, spec),
        global_z,
    )


def fin_projected_width_at_wall_radius(
    carrier: CarrierSpec,
    wall_radius: float,
    spec: IdentifiableFinFixtureSpec = V0R2,
) -> float:
    """Projected fin width where its radial shadow reaches a shared wall radius."""
    global_z = blocker_z_at_projected_radius(spec.source_z, carrier.radius, wall_radius)
    local_z = global_z - carrier.ring_bottom_z
    return fin_projected_width_at_local_z(carrier, local_z, spec)


def required_half_angle(source_z: float, radius: float) -> float:
    return degrees(atan2(radius, source_z))


def validate_spec(spec: IdentifiableFinFixtureSpec = V0R2) -> None:
    assert spec.body_corner_envelope_radius < 48
    assert spec.body_local_height == 33.2
    assert [spec.fin_identities[name].stem_width for name in ("hour", "minute", "second")] == [4.8, 3.2, 1.6]
    assert [spec.fin_identities[name].crown_width for name in ("hour", "minute", "second")] == [3.2, 1.6, 0.4]
    for identity in spec.fin_identities.values():
        assert identity.stem_width >= 4 * spec.nozzle_diameter
        assert identity.crown_width >= spec.nozzle_diameter
        assert identity.crown_height >= 3 * spec.layer_height - 1e-9
        assert (identity.stem_width - identity.crown_width) / 2 <= identity.crown_height + 1e-9
    for carrier in spec.carriers:
        if abs(projected_radius(spec.source_z, carrier.radius, carrier.base_z) - 48) > 1e-6:
            raise ValueError("shadow start drift")
        if abs(projected_radius(spec.source_z, carrier.radius, carrier.tip_z) - carrier.target_tip_radius) > 1e-6:
            raise ValueError("shadow tip drift")
    if any(
        b.radius - a.radius - spec.ring_radial_width < 3.15 - 1e-9
        for a, b in zip(spec.carriers, spec.carriers[1:])
    ):
        raise ValueError("radial clearance drift")


validate_spec()
