"""R1 retrofit parameters for the accepted KAGE three-station free roller.

R1 preserves the R0 roller, spool, ring, fin, bridge and axial-stack geometry.
Only the station-to-existing-base fastening interface changes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from p3_v3_mvp_free_roller_r0_three_station_spec import FreeRollerR0Spec


ROOT = Path(__file__).resolve().parent
NAMESPACE = "p3_v3_mvp_free_roller_r1_retrofit"
MODEL_ROOT = ROOT / "models" / NAMESPACE


@dataclass(frozen=True)
class FreeRollerR1Spec(FreeRollerR0Spec):
    # Existing base: canonical Q3 r0 sectors, already printed, unchanged CAD.
    countersink_major_diameter_mm: float = 6.0
    countersink_included_angle_deg: float = 90.0
    countersink_target_depth_mm: float = 1.45
    countersink_depth_tolerance_mm: float = 0.10
    countersink_rear_flush_allowance_mm: float = 0.10

    # R1 station fastening: rear-inserted M3 flat heads and top-loaded nuts.
    station_screw_length_mm: float = 10.0
    nut_across_flats_mm: float = 5.8
    nut_nominal_across_flats_mm: float = 5.5
    nut_pocket_depth_mm: float = 2.5
    nut_front_skin_mm: float = 0.5
    nut_pocket_radial_elongation_mm: float = 0.6
    nut_nominal_thickness_mm: float = 2.4

    # R1 lower axle socket correction.  The D4.20 socket starts at the
    # unchanged axle datum Z=-5.00 and continues 0.10 mm beyond the unchanged
    # D6 lower-post top Z=-2.45, preventing a coincident socket/post end face.
    lower_socket_top_clearance_mm: float = 0.10
    lower_socket_depth_mm: float = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "lower_socket_depth_mm",
            self.lower_post_top_z_mm
            + self.lower_socket_top_clearance_mm
            - self.axle_z_mm[0],
        )

    @property
    def rear_datum_z_mm(self) -> float:
        return self.base_plate_z_mm[0]

    @property
    def countersink_apex_z_mm(self) -> float:
        return self.rear_datum_z_mm + self.countersink_target_depth_mm

    @property
    def station_nut_pocket_z_mm(self) -> tuple[float, float]:
        return (
            self.station_foot_z_mm[0] + self.nut_front_skin_mm,
            self.station_foot_z_mm[1],
        )

    @property
    def station_screw_tip_z_mm(self) -> float:
        # ISO countersunk screw length is measured from the flush head datum.
        return self.rear_datum_z_mm + self.station_screw_length_mm

    @property
    def station_nut_engagement_mm(self) -> float:
        pocket_bottom, pocket_top = self.station_nut_pocket_z_mm
        available_thread = max(0.0, min(self.station_screw_tip_z_mm, pocket_top) - pocket_bottom)
        # The pocket is 2.50 mm deep, but an ordinary ISO M3 nut is only
        # 2.40 mm thick.  Report actual metal thread engagement, not empty
        # pocket depth above the nut.
        return min(self.nut_nominal_thickness_mm, available_thread)

    @property
    def lower_socket_top_z_mm(self) -> float:
        return self.axle_z_mm[0] + self.lower_socket_depth_mm


SPEC = FreeRollerR1Spec()
