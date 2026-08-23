"""Frozen numeric contract for the P0 shadow-clock optics fixture.

Coordinates use millimetres.  The optical axis is Z: the wall is at -60,
the physical mask face is at 0, the blockers are room-side of the mask, and
the point source is at +44.8.  XY is the wall plane.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class HandSpec:
    name: str
    plane_z_mm: float
    journal_diameter_mm: float
    hub_outer_diameter_mm: float
    relief_bore_diameter_mm: float
    radial_length_mm: float
    root_width_mm: float
    tip_width_mm: float
    tip_radius_mm: float


@dataclass(frozen=True)
class FixtureSpec:
    wall_z_mm: float = -60.0
    mask_z_mm: float = 0.0
    source_z_mm: float = 44.8
    body_rear_diameter_mm: float = 80.0
    body_mask_diameter_mm: float = 111.1429
    body_depth_mm: float = 60.0
    hand_thickness_mm: float = 1.20
    journal_land_mm: float = 1.70
    journal_lead_mm: float = 0.30
    hub_slit_mm: float = 1.00
    contact_pad_tangential_mm: float = 1.20
    contact_pad_radial_protrusion_mm: float = 0.15
    aperture_diameter_mm: float = 0.80
    # Low infill is a slicer instruction.  The CAD body remains a closed solid.
    body_slicer_infill_percent: float = 8.0

    @property
    def hands(self) -> tuple[HandSpec, ...]:
        return (
            HandSpec("hour", 1.2, 8.0, 12.0, 8.20, 60.0, 7.2, 1.5, 0.75),
            HandSpec("minute", 3.2, 6.0, 10.0, 6.20, 70.0, 4.8, 2.4, 1.20),
            HandSpec("second", 5.2, 4.0, 8.0, 4.20, 85.0, 3.2, 1.2, 0.60),
        )


P0 = FixtureSpec()


def source_to_plane_mm(source_z_mm: float, plane_z_mm: float) -> float:
    distance = float(source_z_mm) - float(plane_z_mm)
    if distance <= 0:
        raise ValueError("source must be room-side of the projected plane")
    return distance


def plane_to_wall_mm(plane_z_mm: float, wall_z_mm: float) -> float:
    distance = float(plane_z_mm) - float(wall_z_mm)
    if distance < 0:
        raise ValueError("projected plane cannot be behind the wall")
    return distance


def magnification(source_z_mm: float, plane_z_mm: float, wall_z_mm: float) -> float:
    source_plane = source_to_plane_mm(source_z_mm, plane_z_mm)
    source_wall = source_to_plane_mm(source_z_mm, wall_z_mm)
    return source_wall / source_plane


def projected_length_mm(physical_length_mm: float, source_z_mm: float, plane_z_mm: float, wall_z_mm: float) -> float:
    if physical_length_mm < 0:
        raise ValueError("physical length cannot be negative")
    return float(physical_length_mm) * magnification(source_z_mm, plane_z_mm, wall_z_mm)


def penumbra_mm(aperture_diameter_mm: float, source_z_mm: float, plane_z_mm: float, wall_z_mm: float) -> float:
    if aperture_diameter_mm < 0:
        raise ValueError("aperture diameter cannot be negative")
    return float(aperture_diameter_mm) * plane_to_wall_mm(plane_z_mm, wall_z_mm) / source_to_plane_mm(source_z_mm, plane_z_mm)


def local_pad_interference_mm(hand: HandSpec, pad_protrusion_mm: float = P0.contact_pad_radial_protrusion_mm) -> float:
    """Return radial interference at each of the three compliant contact pads."""
    return hand.journal_diameter_mm / 2.0 - (hand.relief_bore_diameter_mm / 2.0 - pad_protrusion_mm)


def projected_contract(spec: FixtureSpec = P0) -> dict[str, object]:
    mask_m = magnification(spec.source_z_mm, spec.mask_z_mm, spec.wall_z_mm)
    hands = {}
    for hand in spec.hands:
        m = magnification(spec.source_z_mm, hand.plane_z_mm, spec.wall_z_mm)
        hands[hand.name] = {
            "plane_z_mm": hand.plane_z_mm,
            "magnification": m,
            "projected_tip_radius_mm": hand.radial_length_mm * m,
            "projected_tip_width_mm": hand.tip_width_mm * m,
            "penumbra_mm": penumbra_mm(spec.aperture_diameter_mm, spec.source_z_mm, hand.plane_z_mm, spec.wall_z_mm),
            "local_pad_radial_interference_mm": local_pad_interference_mm(hand),
        }
    return {
        "wall_z_mm": spec.wall_z_mm,
        "mask_z_mm": spec.mask_z_mm,
        "source_z_mm": spec.source_z_mm,
        "source_wall_mm": source_to_plane_mm(spec.source_z_mm, spec.wall_z_mm),
        "mask_magnification": mask_m,
        "projected_mask_diameter_mm": spec.body_mask_diameter_mm * mask_m,
        "hands": hands,
    }


def validate_spec(spec: FixtureSpec = P0) -> None:
    if not isclose(spec.mask_z_mm - spec.wall_z_mm, spec.body_depth_mm, abs_tol=1e-9):
        raise ValueError("body depth must span wall datum to mask datum")
    if spec.hand_thickness_mm > 1.60:
        raise ValueError("hand thickness exceeds frozen maximum")
    if spec.hub_slit_mm < 1.0 or spec.hub_slit_mm > 1.2:
        raise ValueError("hub slit must remain in the 1.0-1.2 mm test range")
    for previous, current in zip(spec.hands, spec.hands[1:]):
        free_gap = current.plane_z_mm - previous.plane_z_mm - spec.hand_thickness_mm
        if free_gap < 0.4:
            raise ValueError("blocker planes need at least 0.4 mm axial free gap")
    for hand in spec.hands:
        if hand.tip_radius_mm * 2.0 != hand.tip_width_mm:
            raise ValueError(f"{hand.name} rounded tip must be tangent to its width")
        if not isclose(local_pad_interference_mm(hand), 0.05, abs_tol=1e-9):
            raise ValueError(f"{hand.name} local pad interference must be 0.05 mm radial")


validate_spec()
