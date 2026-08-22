"""Immutable owner groups for the localized I3-R1 real-joinery repair."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HANDOFF_PATH = ROOT / "docs" / "p3-v3-phase3-i3-r1-real-joinery-localized-repair-handoff.md"
FROZEN_STEP_PATH = ROOT / "models" / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention" / "p3_v3_r1_i1_fixed_tower_retention_assembled.step"
HANDOFF_SHA256 = "7b20b2fff600623a1fceab4ec66717d6b5bcc3257d4d32653b26a72d35b704f4"
I3_12_SHA256 = "e482b6f14e03d23080d5011b424efcaf0be280ea39ee9df5a93559ca0659a713"
FROZEN_STEP_SHA256 = "8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724"
NAMESPACE = "p3_v3_phase3_i3_r1_real_joinery"


@dataclass(frozen=True)
class Segmentation:
    ring_teeth: int = 260
    half_teeth: int = 130
    moving_seam_base_deg: float = 15.230769230769
    stationary_seam_base_deg: float = 37.5
    half_count_per_role: int = 2
    quadrant_count_per_family: int = 4
    sector_mask_radius_mm: float = 420.0
    sector_mask_height_mm: float = 100.0

    @property
    def moving_seams_deg(self) -> tuple[float, float]:
        return self.moving_seam_base_deg, self.moving_seam_base_deg + 180.0

    @property
    def stationary_seams_deg(self) -> tuple[float, ...]:
        return tuple(self.stationary_seam_base_deg + 90.0 * i for i in range(4))


@dataclass(frozen=True)
class MovingJoinery:
    radial_min_mm: float = 133.5
    radial_max_mm: float = 140.0
    tangent_half_mm: float = 8.0
    half_a_lap_mm: float = 2.0
    half_b_lap_mm: float = 1.0
    receive_xy_clearance_mm: float = 0.10
    axial_gap_mm: float = 0.08
    butt_face_relief_mm: float = 0.025
    screw_axis_radius_mm: float = 136.75
    screw_tangent_mm: float = 5.0
    screw_clearance_diameter_mm: float = 2.20
    nut_pocket_radial_mm: float = 4.20
    nut_pocket_tangent_mm: float = 4.20
    nut_pocket_height_mm: float = 1.70
    nut_body_side_mm: float = 4.0
    nut_body_height_mm: float = 1.60
    rear_skin_mm: float = 0.30
    pin_diameter_mm: float = 3.0
    pin_length_mm: float = 3.0
    press_bore_diameter_mm: float = 2.95
    slip_bore_diameter_mm: float = 3.10
    role_z_mm: tuple[tuple[str, float, float], ...] = (
        ("hour", -1.50, 1.50),
        ("minute", 4.05, 7.05),
        ("second", 9.60, 12.60),
    )

    @property
    def radial_mid_mm(self) -> float:
        return (self.radial_min_mm + self.radial_max_mm) / 2.0

    @property
    def radial_span_mm(self) -> float:
        return self.radial_max_mm - self.radial_min_mm

    def z_for(self, role: str) -> tuple[float, float]:
        return next((z0, z1) for name, z0, z1 in self.role_z_mm if name == role)


@dataclass(frozen=True)
class StationaryJoinery:
    family: str
    bridge_radii_mm: tuple[float, ...]
    bridge_radial_mm: float
    bridge_tangent_mm: float
    bridge_height_mm: float
    member_z_mm: tuple[float, float]
    bridge_z_mm: tuple[float, float]
    screw_diameter_mm: float
    screw_clearance_diameter_mm: float
    screw_length_mm: float
    screw_tangent_mm: float
    nut_side_mm: float
    nut_pocket_side_mm: float
    nut_height_mm: float
    nut_pocket_height_mm: float
    dowel_diameter_mm: float
    dowel_length_mm: float
    press_bore_diameter_mm: float
    slip_bore_diameter_mm: float
    press_z_mm: tuple[float, float]
    slip_z_mm: tuple[float, float]


CHASSIS_JOINERY = StationaryJoinery(
    "rear_chassis", (85.0, 120.0), 12.0, 18.0, 4.0,
    (-28.0, -25.5), (-32.0, -28.0), 3.0, 3.4, 5.0, 5.5,
    5.5, 5.7, 1.9, 2.0, 4.0, 6.0, 3.95, 4.10,
    (-32.0, -28.0), (-28.0, -26.0),
)
FRAME_JOINERY = StationaryJoinery(
    "stationary_frame", (147.25,), 5.5, 16.0, 3.0,
    (-6.45, -4.05), (-9.45, -6.45), 2.0, 2.2, 4.0, 5.5,
    4.0, 4.2, 1.6, 1.7, 3.0, 5.0, 2.95, 3.10,
    (-9.05, -6.45), (-6.45, -4.05),
)
FRONT_RING_JOINERY = StationaryJoinery(
    "outer_front_ring", (147.25,), 5.5, 16.0, 3.0,
    (12.8, 13.8), (9.8, 12.8), 2.0, 2.2, 3.0, 5.5,
    4.0, 4.2, 1.6, 1.7, 2.0, 4.0, 1.95, 2.10,
    (9.8, 12.8), (12.8, 13.8),
)


@dataclass(frozen=True)
class PrintTransform:
    rotation_deg: float = 30.0
    bed_center_xy_mm: tuple[float, float] = (135.0, 135.0)
    usable_bed_min_xy_mm: tuple[float, float] = (5.0, 5.0)
    usable_bed_max_xy_mm: tuple[float, float] = (265.0, 265.0)
    moving_raw_span_max_mm: float = 244.864483
    moving_brim_mm: float = 3.5
    moving_reserved_square_mm: float = 251.864483
    moving_plate_count: int = 6
    skirt_loops: int = 0
    prime_tower_enabled: bool = False


@dataclass(frozen=True)
class ArtifactContract:
    registry_count: int = 275
    protected_count: int = 131
    replacement_count: int = 18
    new_count: int = 126
    printable_count: int = 34
    moving_plate_count: int = 6
    projection_schema: str = "kage.i3.12.3mf-parity-projection.v3"
    filament_identifier: str = "GFG00"
    physical_tool: str = "T0"
    # lib3mf otherwise creates random UUIDs for the build container and each
    # build item on every write.  Pin them as source-owned artifact parameters
    # so two fresh packages have byte-identical canonical XML semantics.
    orca_build_uuid: str = "89dfc049-1b5b-5c68-8c18-e80bb6d54280"
    orca_build_item_uuids: tuple[str, ...] = (
        "fbd143f6-eb17-551d-9945-3f46d1ff6313",
        "07717b23-238f-544d-bbd0-cf0122ea5bff",
        "7f2af355-4a98-51a1-8691-550e82513cf7",
        "ae6f7396-51db-5e04-b069-6b8730a11742",
        "82a47418-2c57-5b0a-95dd-ef83feb106f6",
        "3b8e092c-b009-55ea-be10-a4de362a0d49",
    )


@dataclass(frozen=True)
class MotionValidation:
    """Exact I3.3 powered-motion matrix and rigid station ownership."""

    target_roles: tuple[str, ...] = ("hour", "minute", "second")
    tooth_positions: int = 260
    tooth_pitch_degrees: float = 360.0 / 260.0
    phase_offsets_degrees: tuple[float, ...] = (-0.05, 0.0, 0.05)
    motor_q_mm: tuple[float, ...] = (-0.35, 0.0, 0.10)
    tower_q_mm: tuple[float, ...] = (-0.25, 0.0, 0.25)
    motor_station_angles_degrees: tuple[tuple[str, float], ...] = (
        ("hour", 0.0),
        ("minute", 120.0),
        ("second", 240.0),
    )
    fixed_tower_angles_degrees: tuple[float, ...] = (60.0, 180.0)
    adjustable_tower_angle_degrees: float = 300.0

    @property
    def q_state_count(self) -> int:
        return len(self.motor_q_mm) ** 3 * len(self.tower_q_mm)

    @property
    def target_angle_count(self) -> int:
        return self.tooth_positions * len(self.phase_offsets_degrees)

    @property
    def state_count(self) -> int:
        return len(self.target_roles) * self.target_angle_count * self.q_state_count


SEGMENTATION = Segmentation()
MOVING_JOINERY = MovingJoinery()
PRINT_TRANSFORM = PrintTransform()
ARTIFACT_CONTRACT = ArtifactContract()
MOTION_VALIDATION = MotionValidation()
STATIONARY_GROUPS = {
    group.family: group for group in (CHASSIS_JOINERY, FRAME_JOINERY, FRONT_RING_JOINERY)
}


def frozen_input_evidence() -> dict[str, object]:
    actual = {
        "handoff": sha256(HANDOFF_PATH.read_bytes()).hexdigest(),
        "frozen_step": sha256(FROZEN_STEP_PATH.read_bytes()).hexdigest(),
    }
    expected = {"handoff": HANDOFF_SHA256, "frozen_step": FROZEN_STEP_SHA256}
    return {"actual": actual, "expected": expected, "all_frozen_hashes_match": actual == expected}
