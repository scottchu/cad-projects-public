"""Geometry contract for the no-purchase phone-flash halo experiment.

This model predicts projected diameters and first-order edge transition only.
It intentionally does not predict perceived brightness or uniformity: a phone
flash is a near-field, finite, model-specific source with its own optics.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PhoneHaloExperiment:
    body_mask_diameter_mm: float = 65.0
    outer_aperture_diameter_mm: float = 105.0
    source_to_mask_mm: float = 35.0
    mask_to_wall_mm: float = 12.0
    effective_source_diameter_mm: float = 5.0
    final_body_diameter_mm: float = 260.0

    def validate(self) -> None:
        if self.body_mask_diameter_mm <= 0:
            raise ValueError("body mask diameter must be positive")
        if self.outer_aperture_diameter_mm <= self.body_mask_diameter_mm:
            raise ValueError("outer aperture must be larger than the body mask")
        if min(self.source_to_mask_mm, self.mask_to_wall_mm) <= 0:
            raise ValueError("both optical distances must be positive")
        if self.effective_source_diameter_mm <= 0:
            raise ValueError("effective source diameter must be positive")

    @property
    def magnification(self) -> float:
        return 1.0 + self.mask_to_wall_mm / self.source_to_mask_mm

    @property
    def projected_inner_diameter_mm(self) -> float:
        return self.body_mask_diameter_mm * self.magnification

    @property
    def projected_outer_diameter_mm(self) -> float:
        return self.outer_aperture_diameter_mm * self.magnification

    @property
    def projected_ring_width_mm(self) -> float:
        return (self.projected_outer_diameter_mm - self.projected_inner_diameter_mm) / 2.0

    @property
    def first_order_edge_transition_mm(self) -> float:
        return self.effective_source_diameter_mm * self.mask_to_wall_mm / self.source_to_mask_mm

    @property
    def final_scale(self) -> float:
        return self.final_body_diameter_mm / self.body_mask_diameter_mm

    @property
    def scaled_wall_gap_mm(self) -> float:
        return self.mask_to_wall_mm * self.final_scale

    @property
    def scaled_halo_outer_diameter_mm(self) -> float:
        return self.projected_outer_diameter_mm * self.final_scale


DEFAULT_PHONE_HALO = PhoneHaloExperiment()
