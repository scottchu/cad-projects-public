"""Frozen I3.1 parameter and refusal contract for KAGE U1 segmentation.

This module intentionally contains no geometry.  It records only dimensions
and equations explicitly frozen by the accepted I3.1 manufacturing spec.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from math import pi
from typing import Any, Mapping


OWNER_GROUP = "phase3_i3_u1_segmentation_joinery"

AMENDMENT_HASHES = {
    "i3_1": "abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77",
    "i3_2": "9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3",
    "i3_3": "4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691",
    "i3_4": "c6fb12ceab347b258b4f3be65b61d32f178bbf3075cf68869d5d87e9d47636e1",
    "i3_5": "08ab0d28e84036a3bcf17e74e9d3ab18d22c376f8a9f71f4cd1fd6494ede35d6",
    "i3_6": "326f9dbd21fa04885447c8080390a70187176f90020f0ebfee212255bc4154f9",
    "i3_7": "7dc3657a2cea56bf5061d7be06303f7b265df48b1c55098dfe9864d57248fe48",
    "i3_8": "3ca35b53d725c54b3e1299dd3a757a09baba7562dd7e984f1fbd7128be22cf4c",
    "i3_9": "88e3ca6ede27fd37d3fd22039362698994914ff1deceed82178fb170fe88408e",
    "i3_10": "e398947925734687a060324adcf91d2c12584739f70dfe48c76a9cd2834d9e0b",
    "i3_11": "da99646a7c7bf0f4f7487ee7898c504771dc62b467e66b934fc679a25a6598fd",
    "i3_12": "e482b6f14e03d23080d5011b424efcaf0be280ea39ee9df5a93559ca0659a713",
}
FROZEN_STEP_SHA256 = "8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724"

_SOURCE_3MF_ROWS = (
    (1, "hour", "A", "fa6a01e8-5e16-50e5-a679-572d6f97eebb"),
    (2, "hour", "B", "8647d48e-3be7-5bcc-96ce-f99edd27d2f1"),
    (3, "minute", "A", "cd27fc98-3338-5c4a-930a-a5f3641c1250"),
    (4, "minute", "B", "cf2d9c10-7eb8-51f4-9acb-70e15bda166e"),
    (5, "second", "A", "e2b2957a-7f3c-57ac-a071-f4ad0ed15dd5"),
    (6, "second", "B", "1d950c12-033f-5037-8c6d-7b006ed0746a"),
)


def accepted_contract_summary() -> dict[str, Any]:
    return {
        "amendment_hashes": dict(AMENDMENT_HASHES),
        "frozen_step_sha256": FROZEN_STEP_SHA256,
        "registry_classification_counts": {
            "protected_exact": 131,
            "authorized_replacement": 18,
            "new_authorized": 126,
        },
        "registry_count": 275,
        "printable_body_count": 34,
        "moving_half_count": 6,
        "moving_half_teeth": 130,
        "cartesian_motion_state_count": 189_540,
        "press_iv_pair_count": 22,
    }


def source_3mf_object_map() -> list[dict[str, Any]]:
    rows = []
    for plate, role, half, object_uuid in _SOURCE_3MF_ROWS:
        beta = "15p230769" if half == "A" else "195p230769"
        rows.append({
            "plate_index": plate,
            "object_name": f"{role}_I3_half_{half}_130T_beta{beta}",
            "object_uuid": object_uuid,
            "role": role,
            "half": half,
            "teeth": 130,
            "extruder": 1,
            "filament_slot": 1,
            "physical_tool": "T0",
        })
    return rows


@dataclass(frozen=True)
class ParameterContract:
    path: str
    units: str
    owner_group: str
    minimum: float
    maximum: float
    probe_value: Any


@dataclass(frozen=True)
class Phase3I3Params:
    u1_nominal_xy_mm: float = 270.00
    u1_edge_keepout_mm: float = 5.00
    u1_usable_xy_mm: float = 260.00
    fallback_raw_bed_xy_mm: float = 260.00
    fallback_usable_xy_mm: float = 250.00
    moving_half_raw_xy_max_mm: float = 244.864483
    moving_brim_nominal_mm: float = 3.50
    moving_brim_fallback_max_mm: float = 3.50
    ring_teeth: int = 260
    moving_segment_count_per_role: int = 2
    moving_segment_teeth: int = 130
    stationary_segment_count_per_family: int = 4
    moving_seam_base_deg: float = 15.230769230769
    stationary_seam_base_deg: float = 37.50
    moving_join_radii_mm: tuple[float, float] = (133.50, 140.00)
    moving_join_tangent_length_mm: float = 16.00
    moving_lower_lap_mm: float = 2.00
    moving_upper_lap_mm: float = 1.00
    lap_xy_clearance_mm: float = 0.10
    lap_z_clearance_mm: float = 0.08
    seam_face_relief_mm: float = 0.025
    seam_gap_target_mm: float = 0.05
    seam_gap_range_mm: tuple[float, float] = (0.03, 0.10)
    seam_step_target_mm: float = 0.10
    seam_step_hard_max_mm: float = 0.15
    tooth_phase_tangent_max_mm: float = 0.10
    race_tir_target_mm: float = 0.15
    race_tir_hard_max_mm: float = 0.20
    race_pitch_concentricity_max_mm: float = 0.10

    @property
    def tooth_pitch_deg(self) -> float:
        return 360.0 / self.ring_teeth

    @property
    def tooth_pitch_arc_mm(self) -> float:
        return 2.0 * pi * 130.0 / self.ring_teeth

    @property
    def moving_seam_angles_deg(self) -> tuple[float, float]:
        return (self.moving_seam_base_deg, self.moving_seam_base_deg + 180.0)

    @property
    def stationary_seam_angles_deg(self) -> tuple[float, float, float, float]:
        return tuple(self.stationary_seam_base_deg + 90.0 * k for k in range(4))

    @property
    def moving_nominal_packed_xy_mm(self) -> float:
        return self.moving_half_raw_xy_max_mm + 2.0 * self.moving_brim_nominal_mm

    @property
    def moving_fallback_packed_xy_mm(self) -> float:
        return self.moving_half_raw_xy_max_mm + 2.0 * self.moving_brim_fallback_max_mm

    @property
    def moving_nut_radial_wall_mm(self) -> float:
        return (self.moving_join_radii_mm[1] - self.moving_join_radii_mm[0] - 4.20) / 2.0

    @property
    def moving_nut_to_dowel_ligament_mm(self) -> float:
        return 5.00 - 2.10 - 1.55

    @property
    def moving_tangential_end_wall_mm(self) -> float:
        return self.moving_join_tangent_length_mm / 2.0 - (5.00 + 2.10)

    @property
    def moving_tooth_root_setback_mm(self) -> float:
        return self.moving_join_radii_mm[0] - 132.50

    @property
    def moving_m2_screw_stack_mm(self) -> float:
        return self.moving_upper_lap_mm + 1.60 + 0.40

    @property
    def moving_screw_head_adjacent_clearance_mm(self) -> float:
        # I3.3 accounts for the authorized 0.08 mm Half-B front protrusion.
        return round(2.55 - 0.08 - 1.20, 10)

    def validate(self) -> None:
        if self.moving_segment_count_per_role != 2 or self.ring_teeth % self.moving_segment_count_per_role:
            raise ValueError("integer tooth allocation: exactly two moving halves required")
        if self.stationary_segment_count_per_family != 4:
            raise ValueError("stationary semicircles: exactly four quadrants required")
        if self.moving_segment_teeth * self.moving_segment_count_per_role != self.ring_teeth:
            raise ValueError("integer tooth allocation: 130 teeth per half required")
        if abs(self.moving_seam_base_deg - 11.0 * self.tooth_pitch_deg) > 1e-12:
            raise ValueError("moving seam must remain on the tooth lattice")
        if self.moving_join_radii_mm[0] < 133.50:
            raise ValueError("R133.50: moving join may not enter functional geometry")
        if self.moving_join_radii_mm[1] > 140.00:
            raise ValueError("R140.00: moving join may not leave its named ROI")
        # I3.4 forbids the conservative 250 mm fallback domain for moving
        # halves. The accepted six plates use nominal U1 XY and the I3.5 brim.
        if self.moving_nominal_packed_xy_mm >= self.u1_usable_xy_mm:
            raise ValueError("nominal U1 bed: moving half plus brim exceeds usable XY")
        if self.seam_gap_range_mm != (0.03, 0.10):
            raise ValueError("seam gap: accepted range is exactly 0.03 to 0.10 mm")
        if self.seam_step_target_mm > 0.10 or self.seam_step_hard_max_mm > 0.15:
            raise ValueError("seam step: target and hard maximum exceeded")
        if self.race_tir_target_mm > 0.15 or self.race_tir_hard_max_mm > 0.20:
            raise ValueError("race TIR: target and hard maximum exceeded")
        if min(
            self.moving_nut_radial_wall_mm,
            self.moving_nut_to_dowel_ligament_mm,
            self.moving_tangential_end_wall_mm,
            self.moving_tooth_root_setback_mm,
        ) <= 0.0:
            raise ValueError("moving joint ligament: all named ligaments must remain positive")


@dataclass(frozen=True)
class Phase3I3Hardware:
    chassis_m3_stack_mm: float = 5.00
    frame_m2_stack_mm: float = 4.00
    front_ring_m2_stack_mm: float = 3.00
    frame_inner_radial_ligament_mm: float = 1.20
    frame_front_hour_fin_clearance_mm: float = 0.60


P3_V3_PHASE3_I3_U1_SEGMENTATION_JOINERY = Phase3I3Params()
P3_V3_PHASE3_I3_HARDWARE = Phase3I3Hardware()


_PROBES: dict[str, Any] = {
    field.name: getattr(P3_V3_PHASE3_I3_U1_SEGMENTATION_JOINERY, field.name)
    for field in fields(P3_V3_PHASE3_I3_U1_SEGMENTATION_JOINERY)
}
_PROBES.update({
    "moving_segment_count_per_role": 3,
    "stationary_segment_count_per_family": 2,
    "moving_join_radii_mm": (133.49, 140.0),
    "moving_brim_fallback_max_mm": 6.0,
})


def parameter_schema(params: Phase3I3Params | None = None) -> dict[str, ParameterContract]:
    params = params or P3_V3_PHASE3_I3_U1_SEGMENTATION_JOINERY
    result: dict[str, ParameterContract] = {}
    for field in fields(params):
        name = field.name
        units = "count" if "count" in name or "teeth" in name else "deg" if name.endswith("_deg") else "mm"
        result[name] = ParameterContract(
            path=name,
            units=units,
            owner_group=OWNER_GROUP,
            minimum=0.0,
            maximum=360.0 if units == "deg" else 1000.0,
            probe_value=_PROBES[name],
        )
    return result


def refusal_validator(overrides: Mapping[str, Any]) -> None:
    """Fail closed for every named I3 refusal category.

    This mapping API also covers refusal inputs that are not Phase3I3Params,
    such as purchased-hardware measurements and export provenance.
    """

    checks = (
        ("three_moving_segments", overrides.get("moving_segment_count_per_role") == 3),
        ("stationary_semicircles", overrides.get("stationary_segment_count_per_family") == 2),
        ("off_lattice_seam", "moving_seam_base_deg" in overrides and abs(float(overrides["moving_seam_base_deg"]) - 15.230769230769) > 1e-12),
        ("join_inside_r133p5", overrides.get("moving_join_radii_mm", (133.5, 140.0))[0] < 133.5),
        ("join_outside_r140", overrides.get("moving_join_radii_mm", (133.5, 140.0))[1] > 140.0),
        ("threaded_insert", overrides.get("receiver_type") == "heat_set_insert"),
        ("loose_1mm_splice", overrides.get("moving_join_style") == "loose_1mm_splice"),
        ("oversize_nut", float(overrides.get("din562_m2_height_mm", 1.6)) > 1.6),
        ("stationary_join_inside_r144p5", float(overrides.get("stationary_join_min_radius_mm", 144.5)) < 144.5),
        ("old_cardinal_seam", int(overrides.get("surviving_old_seam_count", 0)) > 0),
        ("in_stack_seam_assembly", bool(overrides.get("in_stack_ring_assembly", False))),
        ("hall_geometry", int(overrides.get("hall_geometry_count", 0)) > 0),
        ("hand_edited_export", overrides.get("source_owned_export", True) is False),
    )
    for name, rejected in checks:
        if rejected:
            raise ValueError(f"{name}: rejected by frozen I3.1 specification")


P3_V3_PHASE3_I3_U1_SEGMENTATION_JOINERY.validate()
