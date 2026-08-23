"""Frozen dimensional contract for the standalone KAGE P2 magnetic MVP.

The fixture is intentionally independent of every earlier KAGE prototype.
XY is the plate plane, +Z faces the viewer, and -Z faces the wall/rear.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot


@dataclass(frozen=True)
class ChannelSpec:
    name: str
    radius: float
    driver_z: tuple[float, float]
    fin_height: float
    fin_radial: float
    fin_tangential: float
    fin_top: str


@dataclass(frozen=True)
class MagneticThreeChannelMvpSpec:
    fixture_od: float = 220.0
    center_open_diameter: float = 52.0
    plate_outer_radius: float = 110.0
    center_open_radius: float = 26.0
    track_radii: tuple[float, float, float] = (45.0, 65.0, 85.0)
    separator_options: tuple[float, float, float] = (1.0, 1.5, 2.0)

    magnet_diameter: float = 6.0
    magnet_thickness: float = 3.0
    magnet_pocket_diameter: float = 6.15
    magnet_pocket_depth: float = 3.10
    magnet_recess: float = 0.10
    magnet_boss_diameter: float = 9.0

    shoe_radial: float = 9.0
    shoe_arc_length: float = 18.0
    shoe_thickness: float = 3.4
    neck_radial: float = 4.2
    slot_radial: float = 4.8
    radial_clearance_per_side: float = 0.30
    axial_clearance: float = 0.30
    cap_thickness: float = 1.8

    driver_thickness: float = 3.4
    driver_ring_radial_width: float = 4.0
    driver_race_radial_width: float = 4.6
    driver_gap_z: float = 0.60
    rear_base_z: tuple[float, float] = (0.0, 2.3)
    driver_z: tuple[float, float] = (2.6, 6.0)
    driver_boss_top_z: float = 6.3
    separator_rear_z: float = 6.3
    base_outer_ring_span: tuple[float, float] = (98.0, 110.0)
    backbone_z: tuple[float, float] = (0.0, 1.2)
    backbone_width: float = 6.0
    backbone_angles: tuple[float, float, float] = (0.0, 120.0, 240.0)
    pad_z: tuple[float, float] = (1.2, 2.3)
    pad_radial_width: float = 6.0
    pad_arc_degrees: float = 18.0
    pad_connector_width: float = 1.6
    paddle_radial: float = 12.0
    paddle_tangential: float = 10.0

    stationary_hole_radius: float = 103.0
    m3_clearance_diameter: float = 3.4
    m3_external_head_washer: bool = True
    stationary_spacer_diameter: float = 6.0
    stationary_spacer_z: tuple[float, float] = (2.3, 6.3)
    driver_max_radial_envelope: float = 98.95
    m2_clearance_diameter: float = 2.2
    m2_counterbore_diameter: float = 4.2
    m2_counterbore_depth: float = 1.35
    separator_boss_diameter: float = 5.5
    separator_boss_height: float = 4.0
    separator_pilot_diameter: float = 1.6
    separator_pilot_depth: float = 2.4

    cap_spans: tuple[tuple[float, float], ...] = (
        (26.0, 42.6),
        (47.4, 62.6),
        (67.4, 82.6),
        (87.4, 107.0),
    )
    slot_spans: tuple[tuple[float, float], ...] = (
        (42.6, 47.4),
        (62.6, 67.4),
        (82.6, 87.4),
    )
    cap_fastener_radii: tuple[float, float, float, float] = (33.5, 55.0, 75.0, 103.0)
    cap_fastener_angles: tuple[tuple[float, ...], ...] = (
        (0.0, 120.0, 240.0),
        (40.0, 160.0, 280.0),
        (80.0, 200.0, 320.0),
        (0.0, 60.0, 120.0, 180.0, 240.0, 300.0),
    )

    @property
    def channels(self) -> tuple[ChannelSpec, ...]:
        return (
            ChannelSpec("hour", 45.0, self.driver_z, 30.0, 8.0, 2.0, "rounded"),
            ChannelSpec("minute", 65.0, self.driver_z, 40.0, 7.0, 1.6, "chamfered"),
            ChannelSpec("second", 85.0, self.driver_z, 50.0, 6.0, 1.2, "pointed"),
        )

    @property
    def by_name(self) -> dict[str, ChannelSpec]:
        return {channel.name: channel for channel in self.channels}

    @property
    def shoe_overlap_per_side(self) -> float:
        return (self.shoe_radial - self.slot_radial) / 2

    def matching_face_gap(self, separator_thickness: float) -> float:
        return separator_thickness + 0.50

    def wrong_pair_center_distance(self, radial_delta: float, separator_thickness: float) -> float:
        return hypot(radial_delta, separator_thickness + 3.50)

    def wrong_pair_surface_metric(self, radial_edge_gap: float, separator_thickness: float) -> float:
        return hypot(radial_edge_gap, separator_thickness + 0.50)

    @property
    def adjacent_magnet_edge_gaps(self) -> tuple[float, float, float]:
        return (14.0, 14.0, 34.0)

    @property
    def adjacent_shoe_edge_gaps(self) -> tuple[float, float]:
        return (11.0, 11.0)

    @property
    def rear_boss_edge_gaps(self) -> tuple[float, float]:
        return (11.0, 11.0)


P2 = MagneticThreeChannelMvpSpec()


# Captured before the first P2 edit on branch kage/magnetic-three-channel-mvp.
# This keeps the user's still-needed fake V0R2 optics fixture byte-identical.
V0R2_ISOLATION_SHA256 = {
    "v0r2_identifiable_fin_fixture_spec.py": "68d2de8211cd43db6697850a9499b7f296becf3398f354d14e59efe0cb6cf558",
    "v0r2_identifiable_fin_fixture_geometry.py": "5645ec1793d910ea67cb439a8c67db6131b47ff56643694603c0f5271a704f99",
    "v0r2_identifiable_fin_fixture_export.py": "e54e28da21ce2e772e100338b9e844b9aa536f8c95369479d526474b03051203",
    "models/v0r2_identifiable_fin_fixture/v0r2_assembled.step": "6424353da6468e784b07f7f00ff29505677077297146533fc6f8fa2886f673db",
    "models/v0r2_identifiable_fin_fixture/print/v0r2_four_part_identifiable_fin_test.3mf": "4279e5e5fcc0494ba18890764a1de973224daaad9196bda1d69893ffbd79379a",
    "models/v0r2_identifiable_fin_fixture/print/v0r2_manifest.json": "68a3b941bfbe06c0f04875f471b7e51c7ff2bf8c62b4e54fbe5292c750b6ea7b",
}


def validate_spec(spec: MagneticThreeChannelMvpSpec = P2) -> None:
    assert spec.fixture_od == 220.0
    assert spec.center_open_diameter == 52.0
    assert spec.track_radii == (45.0, 65.0, 85.0)
    assert spec.separator_options == (1.0, 1.5, 2.0)
    assert abs(spec.magnet_pocket_diameter - spec.magnet_diameter - 0.15) < 1e-9
    assert abs(spec.magnet_pocket_depth - spec.magnet_thickness - 0.10) < 1e-9
    assert abs(spec.shoe_overlap_per_side - 2.10) < 1e-9
    assert abs(spec.slot_radial - spec.neck_radial - 2 * spec.radial_clearance_per_side) < 1e-9
    assert abs(spec.driver_race_radial_width - spec.driver_ring_radial_width - 0.60) < 1e-9
    assert spec.adjacent_magnet_edge_gaps == (14.0, 14.0, 34.0)
    assert spec.adjacent_shoe_edge_gaps == (11.0, 11.0)
    assert spec.rear_boss_edge_gaps == (11.0, 11.0)
    assert [c.driver_z for c in spec.channels] == [spec.driver_z] * 3
    assert abs(spec.driver_z[0] - spec.pad_z[1] - 0.30) < 1e-9
    assert abs(spec.driver_z[0] - spec.backbone_z[1] - 1.40) < 1e-9
    assert spec.stationary_spacer_z == (spec.rear_base_z[1], spec.separator_rear_z)
    assert spec.stationary_spacer_z[1] - spec.stationary_spacer_z[0] == 4.0
    assert spec.stationary_hole_radius - spec.stationary_spacer_diameter / 2 == 100.0
    assert spec.stationary_hole_radius - spec.stationary_spacer_diameter / 2 > spec.driver_max_radial_envelope
    assert len(spec.cap_fastener_angles[3]) == 6
    assert [c.fin_height for c in spec.channels] == [30.0, 40.0, 50.0]
    assert [c.fin_radial for c in spec.channels] == [8.0, 7.0, 6.0]
    assert [c.fin_tangential for c in spec.channels] == [2.0, 1.6, 1.2]
    assert spec.cap_spans == ((26.0, 42.6), (47.4, 62.6), (67.4, 82.6), (87.4, 107.0))
    assert spec.slot_spans == ((42.6, 47.4), (62.6, 67.4), (82.6, 87.4))
    assert [len(a) for a in spec.cap_fastener_angles] == [3, 3, 3, 6]
    for thickness, expected_gap in zip(spec.separator_options, (1.50, 2.00, 2.50)):
        assert abs(spec.matching_face_gap(thickness) - expected_gap) < 1e-9
    for thickness, expected in zip(spec.separator_options, (20.500, 20.616, 20.742)):
        assert abs(spec.wrong_pair_center_distance(20.0, thickness) - expected) < 0.001
    for thickness, expected in zip(spec.separator_options, (14.080, 14.142, 14.221)):
        assert abs(spec.wrong_pair_surface_metric(14.0, thickness) - expected) < 0.001


validate_spec()
