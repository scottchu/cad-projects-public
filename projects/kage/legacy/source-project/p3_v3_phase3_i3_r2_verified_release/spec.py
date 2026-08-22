"""Immutable owner groups for KAGE I3-R2 Checkpoint A.

Only the two localized R2 repair dimensions are adjustable in this checkpoint:
Half-B XY receiving clearance and opposed exterior butt-face relief.  Every
other accepted architecture value is frozen and the dataclasses reject
in-place mutation.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, replace
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = "p3_v3_phase3_i3_r2_verified_release"

R2_HANDOFF_PATH = ROOT / "docs" / "p3-v3-phase3-i3-r2-verified-release-localized-handoff.md"
I3_SPEC_PATH = ROOT / "docs" / "p3-v3-phase3-i3-u1-segmentation-joinery-accepted-spec.md"
I3_12_PATH = ROOT / "docs" / "p3-v3-phase3-i3-12-design-amendment.md"
R1_HANDOFF_PATH = ROOT / "docs" / "p3-v3-phase3-i3-r1-real-joinery-localized-repair-handoff.md"
FROZEN_STEP_PATH = (
    ROOT
    / "models"
    / "p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention"
    / "p3_v3_r1_i1_fixed_tower_retention_assembled.step"
)
R1_ARTIFACT_ROOT = ROOT / "models" / "p3_v3_phase3_i3_r1_real_joinery"
R2_ARTIFACT_ROOT = ROOT / "models" / NAMESPACE

FROZEN_HASHES = {
    "r2_handoff": "b39376240fa9c3a88440592070d55d7caca7f9bb59b1032e7d8608c8dbf74ec8",
    "i3_spec": "abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77",
    "i3_12": "e482b6f14e03d23080d5011b424efcaf0be280ea39ee9df5a93559ca0659a713",
    "r1_handoff": "7b20b2fff600623a1fceab4ec66717d6b5bcc3257d4d32653b26a72d35b704f4",
    "frozen_step": "8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724",
}


def adjustable(default: float, *, delta: float = 0.10):
    return field(default=default, metadata={"adjustable": True, "probe_delta": delta})


@dataclass(frozen=True)
class Segmentation:
    ring_teeth: int = 260
    half_teeth: int = 130
    moving_seam_base_deg: float = 15.230769230769
    stationary_seam_base_deg: float = 37.5
    sector_mask_radius_mm: float = 420.0
    sector_mask_height_mm: float = 100.0
    boolean_overtravel_mm: float = 0.20

    @property
    def moving_seams_deg(self) -> tuple[float, float]:
        return self.moving_seam_base_deg, self.moving_seam_base_deg + 180.0


@dataclass(frozen=True)
class MovingJoinery:
    radial_min_mm: float = 133.50
    radial_max_mm: float = 140.00
    tangent_half_mm: float = 8.00
    half_a_lap_mm: float = 2.00
    half_b_lap_mm: float = 1.00
    receive_xy_clearance_mm: float = adjustable(0.10)
    axial_gap_mm: float = 0.08
    butt_face_relief_mm: float = adjustable(0.025)
    screw_axis_radius_mm: float = 136.75
    screw_tangent_mm: float = 5.00
    screw_clearance_diameter_mm: float = 2.20
    nut_pocket_radial_mm: float = 4.20
    nut_pocket_tangent_mm: float = 4.20
    nut_pocket_height_mm: float = 1.70
    nut_body_side_mm: float = 4.00
    nut_body_height_mm: float = 1.60
    rear_skin_mm: float = 0.30
    pin_diameter_mm: float = 3.00
    pin_length_mm: float = 3.00
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
    bridge_count: int


@dataclass(frozen=True)
class MotionValidation:
    state_count: int = 189_540
    audit_state_count: int = 2_187


@dataclass(frozen=True)
class PrintTransform:
    rotation_deg: float = 30.0
    brim_mm: float = 3.50
    raw_span_max_mm: float = 244.864483


@dataclass(frozen=True)
class MeshContract:
    weld_mm: float = 1e-6


@dataclass(frozen=True)
class OrcaContract:
    plate_count: int = 6
    filament_identifier: str = "GFG00"


@dataclass(frozen=True)
class FreshnessContract:
    fail_closed: bool = True


@dataclass(frozen=True)
class ReleaseContract:
    complete_build_count: int = 2


@dataclass(frozen=True)
class ArtifactContract:
    registry_count: int = 275
    protected_count: int = 131
    replacement_count: int = 18
    new_count: int = 126
    printable_count: int = 34


@dataclass(frozen=True)
class OwnerBundle:
    segmentation: Segmentation = field(default_factory=Segmentation)
    moving_joinery: MovingJoinery = field(default_factory=MovingJoinery)
    chassis_joinery: StationaryJoinery = field(
        default_factory=lambda: StationaryJoinery("rear_chassis", 8)
    )
    frame_joinery: StationaryJoinery = field(
        default_factory=lambda: StationaryJoinery("stationary_frame", 4)
    )
    front_ring_joinery: StationaryJoinery = field(
        default_factory=lambda: StationaryJoinery("outer_front_ring", 4)
    )
    motion_validation: MotionValidation = field(default_factory=MotionValidation)
    print_transform: PrintTransform = field(default_factory=PrintTransform)
    mesh_contract: MeshContract = field(default_factory=MeshContract)
    orca_contract: OrcaContract = field(default_factory=OrcaContract)
    freshness_contract: FreshnessContract = field(default_factory=FreshnessContract)
    release_contract: ReleaseContract = field(default_factory=ReleaseContract)
    artifact_contract: ArtifactContract = field(default_factory=ArtifactContract)


DEFAULT_OWNERS = OwnerBundle()


def adjustable_field_specs(owners: OwnerBundle = DEFAULT_OWNERS) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for owner_field in fields(owners):
        owner = getattr(owners, owner_field.name)
        if not hasattr(owner, "__dataclass_fields__"):
            continue
        for value_field in fields(owner):
            if value_field.metadata.get("adjustable"):
                rows.append(
                    {
                        "owner": owner_field.name,
                        "field": value_field.name,
                        "value": getattr(owner, value_field.name),
                        "probe_delta": value_field.metadata["probe_delta"],
                    }
                )
    return tuple(rows)


def adjusted_owner_bundle(
    owners: OwnerBundle,
    owner_name: str,
    field_name: str,
    value: Any,
) -> OwnerBundle:
    owner = getattr(owners, owner_name)
    changed_owner = replace(owner, **{field_name: value})
    return replace(owners, **{owner_name: changed_owner})

