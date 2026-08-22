"""Frozen dimensional contract for the isolated 300 mm KAGE magnetic MVP.

XY is the plate plane, +Z faces the viewer, and -Z faces the wall/rear.
P2R2 enlarges the fixture without scaling any functional fit cross-section.
"""

from __future__ import annotations

from dataclasses import dataclass

from p2r1_magnetic_three_channel_outboard_fins_spec import (
    ChannelSpec,
    MagneticThreeChannelOutboardFinsSpec,
)


@dataclass(frozen=True)
class MagneticThreeChannel300Spec(MagneticThreeChannelOutboardFinsSpec):
    fixture_od: float = 300.0
    plate_outer_radius: float = 150.0
    track_radii: tuple[float, float, float] = (95.0, 115.0, 135.0)

    base_outer_ring_span: tuple[float, float] = (138.0, 150.0)
    stationary_hole_radius: float = 143.5
    driver_max_radial_envelope: float = 139.5

    cap_spans: tuple[tuple[float, float], ...] = (
        (26.0, 92.6),
        (97.4, 112.6),
        (117.4, 132.6),
        (137.4, 147.0),
    )
    slot_spans: tuple[tuple[float, float], ...] = (
        (92.6, 97.4),
        (112.6, 117.4),
        (132.6, 137.4),
    )
    # R0 uses two staggered circles so the broad inner cap is supported
    # without introducing a bridge through any 360-degree follower track.
    cap_fastener_radii: tuple[float, float, float, float] = (50.0, 105.0, 125.0, 143.5)
    cap_fastener_angles: tuple[tuple[float, ...], ...] = (
        (0.0, 120.0, 240.0, 60.0, 180.0, 300.0),
        (40.0, 160.0, 280.0),
        (80.0, 200.0, 320.0),
        (0.0, 60.0, 120.0, 180.0, 240.0, 300.0),
    )
    pad_radial_width: float = 6.4

    @property
    def cap_fastener_sites(self) -> tuple[tuple[tuple[float, float], ...], ...]:
        return (
            tuple((50.0, angle) for angle in (0.0, 120.0, 240.0))
            + tuple((78.0, angle) for angle in (60.0, 180.0, 300.0)),
            tuple((105.0, angle) for angle in (40.0, 160.0, 280.0)),
            tuple((125.0, angle) for angle in (80.0, 200.0, 320.0)),
            tuple((143.5, angle) for angle in (0.0, 60.0, 120.0, 180.0, 240.0, 300.0)),
        )

    @property
    def channels(self) -> tuple[ChannelSpec, ...]:
        return (
            ChannelSpec("hour", 95.0, self.driver_z, 30.0, 8.0, 2.0, "rounded"),
            ChannelSpec("minute", 115.0, self.driver_z, 40.0, 7.0, 1.6, "chamfered"),
            ChannelSpec("second", 135.0, self.driver_z, 50.0, 6.0, 1.2, "pointed"),
        )


P2R2 = MagneticThreeChannel300Spec()


P2R1_ISOLATION_SHA256 = {
    "p2r1_magnetic_three_channel_outboard_fins_spec.py": "018b4cab5cdce57cdf99c23029ec2b848375314a66b21a0e04bdef5850103659",
    "p2r1_magnetic_three_channel_outboard_fins_geometry.py": "21abd8b9048307558cd3564f10fb31ddf5673c73869305e6e433674bb6993a31",
    "p2r1_magnetic_three_channel_outboard_fins_export.py": "5ea46261a6b6435382d7eea0ac2a09079071e1f7b9f74a26728ee54a09d1e8a5",
    "tests/test_p2r1_magnetic_three_channel_outboard_fins.py": "e9c2d95195a550851a3712abb0d03044ca8a770499c23143d16812afa7c3b1ed",
    "models/p2r1_magnetic_three_channel_outboard_fins/p2r1_assembled_t1p5.step": "043f0af5cd3107a0e7395ba96865214166283bd0c0a92c9fa97d7e7e387a8025",
    "models/p2r1_magnetic_three_channel_outboard_fins/print/p2r1_magnetic_three_channel_outboard_fins_t1p5.3mf": "642643a952b2136ecab1ea2d5f62e20e41a9fcfa2c07748716aeb13dba06b58a",
}


def validate_spec(spec: MagneticThreeChannel300Spec = P2R2) -> None:
    assert spec.fixture_od == 300.0
    assert spec.plate_outer_radius == 150.0
    assert spec.center_open_diameter == 52.0
    assert spec.track_radii == (95.0, 115.0, 135.0)
    assert spec.slot_spans == ((92.6, 97.4), (112.6, 117.4), (132.6, 137.4))
    assert spec.cap_spans == ((26.0, 92.6), (97.4, 112.6), (117.4, 132.6), (137.4, 147.0))
    assert [len(sites) for sites in spec.cap_fastener_sites] == [6, 3, 3, 6]
    assert spec.track_radii[-1] + spec.shoe_radial / 2 == 139.5
    assert spec.track_radii[-1] + spec.channels[-1].fin_radial / 2 == 138.0
    assert spec.stationary_hole_radius - spec.stationary_spacer_diameter / 2 == 140.5
    assert spec.stationary_hole_radius + spec.stationary_spacer_diameter / 2 == 146.5
    assert spec.stationary_hole_radius - spec.stationary_spacer_diameter / 2 - spec.driver_max_radial_envelope == 1.0
    assert spec.stationary_hole_radius + spec.m3_washer_diameter / 2 == 147.0
    assert spec.plate_outer_radius - 147.0 == 3.0
    assert spec.shoe_overlap_per_side == 2.10
    assert abs((spec.slot_radial - spec.neck_radial) - 2 * spec.radial_clearance_per_side) < 1e-9
    assert spec.pad_radial_width == 6.4
    assert spec.separator_options == (1.0, 1.5, 2.0)


validate_spec()
