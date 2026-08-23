"""Frozen visualization contract for two KAGE three-ring architectures.

XY is the clock plane, +Z faces the viewer, and -Z faces the wall.  This is a
comparison model only: it intentionally omits motors, Hall sensors, and final
guides while preserving the 300 mm outer frame envelope.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class P3V2ThreeRingComparisonSpec:
    frame_inner_radius: float = 141.0
    frame_outer_radius: float = 150.0
    frame_z: tuple[float, float] = (0.0, 2.4)

    roles: tuple[str, str, str] = ("hour", "minute", "second")
    role_colors: tuple[str, str, str] = ("#3F8F87", "#E38B48", "#D95D78")
    display_angles: tuple[float, float, float] = (305.0, 45.0, 145.0)

    carrier_radial_width: float = 5.0
    carrier_thickness: float = 1.8
    stacked_carrier_radius: float = 135.0
    stacked_first_z: float = 2.7
    stacked_axial_gap: float = 0.30
    # All three vertical blades sit just inside the common carrier band.  Thin
    # root arms connect them to their own Z layer; no blade crosses another
    # moving carrier when the hands rotate through the same angle.
    stacked_fin_radii: tuple[float, float, float] = (125.0, 128.0, 131.0)

    concentric_carrier_radii: tuple[float, float, float] = (117.0, 126.0, 135.0)
    concentric_z: float = 2.7

    fin_radial_width: float = 2.4
    fin_tangential_widths: tuple[float, float, float] = (3.0, 2.0, 1.2)
    fin_heights: tuple[float, float, float] = (48.0, 55.0, 62.0)
    fin_root_sink: float = 0.20
    root_arm_thickness: float = 0.40
    root_arm_carrier_overlap: float = 0.40

    @property
    def stacked_pitch(self) -> float:
        return self.carrier_thickness + self.stacked_axial_gap

    @property
    def stacked_z_starts(self) -> tuple[float, float, float]:
        return tuple(self.stacked_first_z + index * self.stacked_pitch for index in range(3))

    @property
    def stacked_total_height(self) -> float:
        return self.stacked_z_starts[-1] + self.carrier_thickness - self.stacked_first_z

    @property
    def stacked_fin_lane_gap(self) -> float:
        return self.stacked_fin_radii[1] - self.stacked_fin_radii[0] - self.fin_radial_width

    @property
    def concentric_radial_gap(self) -> float:
        return self.concentric_carrier_radii[1] - self.concentric_carrier_radii[0] - self.carrier_radial_width

    @property
    def concentric_center_clear_diameter(self) -> float:
        return 2.0 * (self.concentric_carrier_radii[0] - self.carrier_radial_width / 2.0)


P3_V2 = P3V2ThreeRingComparisonSpec()


P3_V1_ISOLATION_SHA256 = {
    "p3_v1_motor_outer_ring_multimaterial_spec.py": "495af64724288b9b96c62e0a6d79dbd63ef236001d2eeb38bab65f84eda9bcdb",
    "p3_v1_motor_outer_ring_multimaterial_geometry.py": "8757899169addb04b3642dfa51a2b04ae6c172a1c9983115af5edf1dd0a4f70d",
    "p3_v1_motor_outer_ring_multimaterial_export.py": "5c083d84864d570128263eb53b976b04d63b4fb8ed2addbcc370a20d5a3e8606",
    "tests/test_p3_v1_motor_outer_ring_multimaterial.py": "a3e5986b2eb123aab66acb381163262dd2675557c765f626497a446cd8731b03",
    "models/p3_v1_motor_outer_ring_multimaterial/p3_v1_assembled.step": "5c63193ce72c7d13b62b6909024ae113dfef30355af22042c373693c64a3f490",
}


def validate_spec(p: P3V2ThreeRingComparisonSpec = P3_V2) -> None:
    assert p.frame_outer_radius * 2.0 == 300.0
    assert all(abs(actual - expected) < 1e-9 for actual, expected in zip(p.stacked_z_starts, (2.7, 4.8, 6.9)))
    assert abs(p.stacked_total_height - 6.0) < 1e-9
    assert abs(p.stacked_fin_lane_gap - 0.6) < 1e-9
    assert p.concentric_carrier_radii == (117.0, 126.0, 135.0)
    assert abs(p.concentric_radial_gap - 4.0) < 1e-9
    assert abs(p.concentric_center_clear_diameter - 229.0) < 1e-9
    assert min(p.fin_tangential_widths) >= 1.2
    assert len(set(p.display_angles)) == 3


validate_spec()
