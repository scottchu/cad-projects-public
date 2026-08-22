"""P13 exploratory nominal four-plate / three-rod XT60 forming jig.

This module is deliberately limited to the nominal, centred geometry from the
P13 architecture brief.  It is useful for mechanism and assembly review, but
it is not a tolerance, strength, heat, fit, or physical-retention certificate.

Coordinates: rod/shaft axes are X; mechanism motion is in YZ.  The shaft datum
is derived from the requested wire/shaft clearance and is not an independent
input.  OPEN is 0 degrees and LOCKED is 27 degrees.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from copy import copy
from dataclasses import asdict, dataclass, fields, replace
from functools import lru_cache
from hashlib import sha256
from datetime import datetime
from math import asin, atan2, ceil, cos, degrees, floor, hypot, isfinite, pi, radians, sin, sqrt
from pathlib import Path
from typing import Literal

from build123d import (
    Align,
    Box,
    BuildLine,
    BuildSketch,
    CenterArc,
    Circle,
    Compound,
    Cone,
    Cylinder,
    Face,
    Line,
    Plane,
    Pos,
    Rot,
    Shape,
    Side as OffsetSide,
    Sphere,
    Wire,
    extrude,
    export_step,
    sweep,
)
from cadgen import srgb

from xt60_bend_jig.p16_cap_throat_test import (
    DEFAULTS as P16_CAP_DEFAULTS,
    build_functional_cap_core as build_p16_functional_cap_core,
)


RodName = Literal["upright", "bottom", "diagonal"]
ROD_NAMES: tuple[RodName, ...] = ("upright", "bottom", "diagonal")
P13_FIXED_JOURNAL_OPENING: Literal["upward"] = "upward"
P13_CAM_PHASE_FEATURE: Literal["separate_D_keyed_shaft"] = "separate_D_keyed_shaft"
P13_RIGHT_CAP_SLIT_COUNT: Literal[1] = 1
P13_FROZEN_TOPOLOGY = {
    "fixed_journal_opening": P13_FIXED_JOURNAL_OPENING,
    "cam_phase_feature": P13_CAM_PHASE_FEATURE,
    "right_cap_slit_count": P13_RIGHT_CAP_SLIT_COUNT,
}
P13_GATE0_BRIEF_PATH = "docs/p13-four-plate-three-rod-brief.md"
P13_GATE0_BRIEF_SHA256 = "9c2102114cbf87ccabaa4388ed3814b91cdf3f8f654c775f5ddd8a5d05272322"
P13_DOMAIN_AMENDMENT_PATH = "docs/p13-cad-source-domain-amendment.md"
P13_DOMAIN_AMENDMENT_SHA256 = "b50e850ac5425fe7bad0e49555de10b0e30f63e04934bdbf66d4220f44e1f590"
P13_EPS_GLOBAL_MM = 0.005
P13_CAP_ENGAGEMENT_DOMAIN_MM = (2.50, 3.00)
P13_FULL_ROLL_DOMAIN_DEG = (0.0, 360.0)
P13_RIGHT_FIXED_ALPHA0_DEG = 0.0
P13_ENGAGED_ROLL_CLASSIFICATION_TOLERANCE_DEG = 0.001
P13_RIGHT_FIXED_ROLL_DIAGNOSTIC_STEP_DEG = 15.0
P13_INSTALLED_ROLL_COUNTEREXAMPLE_DEG = 5.0
P13_CAM_D_ENGAGEMENT_MIN_MM = 4.50


@dataclass(frozen=True, slots=True)
class PointYZ:
    y: float
    z: float

    def distance_to(self, other: "PointYZ") -> float:
        return hypot(self.y - other.y, self.z - other.z)


@dataclass(frozen=True, slots=True)
class P13Parameters:
    # Modeling allowances used only to make boolean cutters robust.  They are
    # named here so a scale/tolerance study does not depend on source literals.
    boolean_axial_overcut: float = 0.20
    boolean_plate_overcut: float = 2.00
    boolean_radial_margin: float = 1.00

    # Purchased stock and workpiece envelope.
    rod_diameter: float = 4.00
    rod_length: float = 50.00
    wire_diameter_design: float = 4.30
    # Geometric wire squeeze after first tangency. This is a displacement
    # proxy for physical preload; actual force remains a print/wire test.
    wire_preload: float = 0.25
    c_sw: float = 0.50
    wire_x: float = 4.00
    bend_radius: float = 6.00
    xt60_x: float = 15.90
    xt60_y: float = 8.10
    xt60_z: float = 20.50
    cup_diameter: float = 3.00
    cup_z0: float = 43.00
    cup_z1: float = 48.00
    horizontal_z: float = 30.00
    bend_center_y: float = 6.00
    bend_center_z: float = 36.00
    horizontal_start_y: float = 19.00
    vertical_lead_z1: float = 43.00
    xt60_body_z0: float = 48.00

    # Four circular principal plates.
    plate_diameter: float = 40.50
    fixed_thickness: float = 2.80
    cam_thickness: float = 2.50
    main_face_gap: float = 0.30
    fixed_center_spacing: float = 29.00
    thrust_land_od: float = 10.00
    fixed_thrust_land_height: float = 0.20
    cam_thrust_land_height: float = 0.00

    # Nominal kinematics.
    open_angle_deg: float = 0.00
    rise_end_deg: float = 22.00
    locked_angle_deg: float = 27.00
    lane_width: float = 4.75
    passage_half_width_y: float = 4.25
    passage_z_min: float = 34.00
    clearance_margin: float = 0.75
    follower_uncertainty_y: float = 0.25
    follower_uncertainty_z: float = 0.25
    cam_path_step_deg: float = 0.25
    cam_band_segment_count: int = 20

    # Separate printed D-keyed actuator shaft and its two cam hubs.  The D
    # profile exists only at the cam stations; the fixed guides ride on round
    # reduced journal lands and the left keeper rides in its own round groove.
    shaft_od: float = 5.60
    shaft_d_across_flat: float = 5.15
    cam_d_bore_od: float = 5.70
    cam_d_bore_across_flat: float = 5.25
    cam_hub_od: float = 10.00
    cam_hub_extension: float = 2.00
    shaft_head_od: float = 9.60
    shaft_head_thickness: float = 2.00
    shaft_left_end_margin: float = 0.50
    axial_endplay: float = 0.275
    journal_land_od: float = 4.60
    fixed_groove_od: float = 4.80
    fixed_groove_width: float = 3.00
    keeper_groove_od: float = 4.60
    keeper_groove_width: float = 1.20

    # Integral fixed C-journal and round shaft keeper.
    journal_throat: float = 4.20
    journal_relief_diameter: float = 2.00
    journal_tip_width: float = 2.20
    keeper_tip_width: float = 1.20
    keeper_relief_diameter: float = 1.20
    keeper_od: float = 9.60
    keeper_id: float = 4.80
    keeper_throat: float = 4.00
    keeper_thickness: float = 1.00

    # Round rod-end retainers.
    cap_od: float = 7.00
    cap_length: float = 3.80
    left_cap_socket: float = 3.90
    left_cap_socket_depth: float = 3.00
    right_cap_cavity: float = 4.20
    right_cap_throat: float = 4.10
    right_cap_throat_depth: float = 0.60
    right_cap_cavity_end: float = 3.00
    right_cap_functional_overcut: float = 0.03
    right_cap_slit_width: float = 0.60
    right_cap_slit_z0: float = 1.995
    right_cap_slit_z1: float = 3.50
    nominal_cap_engagement: float = 2.75

    # Exact rigid review payload.
    pad_y0: float = 24.00
    pad_y1: float = 25.50
    pad_thickness_z: float = 0.50
    pad_width_x: float = 5.00
    stripped_y0: float = 19.00
    stripped_y1: float = 24.00
    stripped_diameter: float = 2.30
    solder_radius: float = 1.50
    iron_angle_deg: float = 35.00
    iron_tip_r0: float = 0.60
    iron_tip_r1: float = 1.75
    iron_tip_length: float = 12.00
    iron_barrel_radius: float = 4.00
    iron_barrel_length: float = 35.00

    # Diagnostic-only coupon and presentation layout parameters.
    diagnostic_lane_widths: tuple[float, float, float] = (4.55, 4.65, 4.75)
    diagnostic_cam_bores: tuple[float, float] = (5.65, 5.70)
    diagnostic_cam_across_flats: tuple[float, float] = (5.20, 5.25)
    diagnostic_journal_ods: tuple[float, float, float] = (4.55, 4.60, 4.65)
    diagnostic_coupon_thickness: float = 6.00
    diagnostic_lane_coupon_x: float = 20.00
    diagnostic_lane_coupon_y: float = 20.00
    diagnostic_lane_pitch: float = 5.50
    diagnostic_bore_coupon_x: float = 16.00
    diagnostic_bore_coupon_y: float = 16.00
    diagnostic_bore_pitch: float = 5.00
    exploded_plate_offset_x: float = 50.00
    exploded_fixed_offset_x: float = 8.00
    exploded_keeper_offset_z: float = -12.00
    exploded_rod_offset_y: float = -52.00
    exploded_rod_pitch_z: float = 8.00
    exploded_cap_lane_x: float = 12.00
    exploded_left_cap_lane_y: float = -68.00
    exploded_right_cap_lane_y: float = -82.00
    exploded_cap_pitch_z: float = 10.00
    print_plate_pitch_x: float = 48.00
    print_upper_y: float = 28.00
    print_actuator_y: float = -26.00
    print_keeper_x: float = -48.00
    print_keeper_y: float = -18.00
    print_cap_left_x0: float = -52.00
    print_cap_right_x0: float = 32.00
    print_cap_pitch_x: float = 10.00
    print_cap_y: float = -36.00
    print_coupon_y: float = -76.00
    print_coupon_x_offset: float = 25.00
    print_plate_rotation_deg: float = 90.00
    print_actuator_rotation_deg: float = 90.00
    print_cap_rotation_deg: float = 90.00
    print_shaft_x: float = 0.00
    print_shaft_y: float = -52.00
    print_shaft_rotation_deg: float = 0.00
    cap_reverse_rotation_deg: float = 180.00
    bend_arc_start_deg: float = -90.00
    bend_arc_sweep_deg: float = -90.00
    removal_review_sample_count: int = 5
    continuous_overlap_volume_tolerance: float = 1.0e-7
    rod_exit_clearance: float = 0.50
    removal_end_clearance: float = 0.50
    cap_removed_offset_x: float = 12.00
    service_keeper_offset_z: float = 12.00
    service_fixed_offset_z: float = -26.00
    service_shaft_end_clearance: float = 0.50

    def __post_init__(self) -> None:
        if self.rod_diameter <= 0.0 or self.rod_length <= 0.0:
            raise ValueError("rod dimensions must be positive")
        if self.plate_diameter <= 0.0:
            raise ValueError("plate diameter must be positive")
        if min(self.fixed_thickness, self.cam_thickness, self.lane_width) <= 0.0:
            raise ValueError("plate thicknesses and lane width must be positive")
        if self.fixed_thrust_land_height <= 0.0 or self.cam_thrust_land_height < 0.0:
            raise ValueError("fixed thrust land must be positive and cam thrust land nonnegative")
        if self.nominal_thrust_land_gap < 0.0:
            raise ValueError("facing thrust lands must fit inside the main-face gap")
        if self.locked_angle_deg <= self.rise_end_deg:
            raise ValueError("LOCKED must include a nonzero endpoint preload interval")
        if min(
            self.cam_band_segment_count,
            self.removal_review_sample_count,
        ) < 2:
            raise ValueError("path segmentation and removal sampling must contain at least two intervals")
        if self.principal_stack_width >= self.rod_length:
            raise ValueError("four-plate stack must fit between uncut rod ends")
        if not 0.50 <= self.c_sw <= 0.75:
            raise ValueError("P21 safe c_sw range is 0.50..0.75 mm")
        if not 4.20 <= self.wire_diameter_design <= 4.30:
            raise ValueError("P21 safe wire_diameter_design range is 4.20..4.30 mm")
        if not 0.0 <= self.wire_preload <= 0.40:
            raise ValueError("wire_preload must be within 0.00..0.40 mm")
        if self.shaft_d_across_flat >= self.shaft_od:
            raise ValueError("shaft D across-flat must be smaller than its round OD")
        if self.cam_d_bore_od <= self.shaft_od or self.cam_d_bore_across_flat <= self.shaft_d_across_flat:
            raise ValueError("cam D bore must clear the printed D shaft")
        if self.cam_hub_od / 2.0 - self.cam_d_bore_od / 2.0 < 2.075 - 1.0e-9:
            raise ValueError("cam hub radial wall must be at least 2.075 mm")
        if self.cam_d_engagement < P13_CAM_D_ENGAGEMENT_MIN_MM:
            raise ValueError("each cam D engagement must be at least 4.5 mm")
        if not 0.20 <= self.axial_endplay <= 0.35:
            raise ValueError("assembled shaft axial endplay must be 0.20..0.35 mm")
        if not self.keeper_groove_od <= self.journal_land_od < self.fixed_groove_od:
            raise ValueError("round keeper groove, journal land and fixed journal IDs are not nested")

    @property
    def principal_stack_width(self) -> float:
        return self.cam_right_outer_x - self.cam_left_outer_x

    @property
    def nominal_thrust_land_gap(self) -> float:
        """Nominal axial clearance between each cam/fixed bearing pair."""

        return (
            self.main_face_gap
            - self.fixed_thrust_land_height
            - self.cam_thrust_land_height
        )

    @property
    def fixed_left_x(self) -> float:
        return -self.fixed_center_spacing / 2.0

    @property
    def fixed_right_x(self) -> float:
        return self.fixed_center_spacing / 2.0

    @property
    def cam_left_x(self) -> float:
        return self.fixed_left_x - self.fixed_thickness / 2.0 - self.main_face_gap - self.cam_thickness / 2.0

    @property
    def cam_right_x(self) -> float:
        return -self.cam_left_x

    @property
    def cam_left_outer_x(self) -> float:
        return self.cam_left_x - self.cam_thickness / 2.0

    @property
    def cam_right_outer_x(self) -> float:
        return self.cam_right_x + self.cam_thickness / 2.0

    @property
    def cam_d_engagement(self) -> float:
        return self.cam_thickness + self.cam_hub_extension

    @property
    def left_cam_hub_outer_x(self) -> float:
        return self.cam_left_outer_x - self.cam_hub_extension

    @property
    def right_cam_hub_outer_x(self) -> float:
        return self.cam_right_outer_x + self.cam_hub_extension

    @property
    def keeper_groove_x(self) -> float:
        # The keeper's right face sits one endplay gap left of the left hub.
        return self.left_cam_hub_outer_x - self.axial_endplay - self.keeper_thickness / 2.0

    @property
    def shaft_x0(self) -> float:
        return self.keeper_groove_x - self.keeper_groove_width / 2.0 - self.shaft_left_end_margin

    @property
    def shaft_head_inner_x(self) -> float:
        return self.right_cam_hub_outer_x

    @property
    def shaft_head_outer_x(self) -> float:
        return self.shaft_head_inner_x + self.shaft_head_thickness

    @property
    def shaft_extraction_distance(self) -> float:
        return self.right_cam_hub_outer_x + self.service_shaft_end_clearance - self.shaft_x0

    @property
    def xt60_body_z1(self) -> float:
        return self.xt60_body_z0 + self.xt60_z

    @property
    def contact_offset(self) -> float:
        return self.tangent_contact_offset - self.wire_preload

    @property
    def tangent_contact_offset(self) -> float:
        """Rod-centre to wire-centre distance at first tangency."""

        return self.rod_diameter / 2.0 + self.wire_radius

    @property
    def locked_contact_offset(self) -> float:
        """Compatibility name for the derived, preloaded LOCK offset."""

        return self.contact_offset

    @property
    def wire_diameter(self) -> float:
        """Compatibility alias for the frozen design envelope diameter."""
        return self.wire_diameter_design

    @property
    def shaft_radius(self) -> float:
        return self.shaft_od / 2.0

    @property
    def wire_radius(self) -> float:
        return self.wire_diameter_design / 2.0

    @property
    def right_cap_min_radial_wall(self) -> float:
        """Minimum nominal radial wall at the largest right-cap bore."""
        return (self.cap_od - max(self.right_cap_cavity, self.right_cap_throat)) / 2.0

    @property
    def right_cap_nominal_radial_clearance(self) -> float:
        """Nominal one-sided clearance between the right cap and purchased rod."""
        return (min(self.right_cap_cavity, self.right_cap_throat) - self.rod_diameter) / 2.0

    @property
    def initial_arc_distance(self) -> float:
        return self.bend_radius * (sqrt(2.0) - 1.0)

    @property
    def pivot_delta(self) -> float:
        return (
            self.shaft_radius + self.wire_radius + self.c_sw - self.initial_arc_distance
        ) / sqrt(2.0)

    @property
    def shaft_y(self) -> float:
        return (self.bend_center_y - self.bend_radius) - self.pivot_delta

    @property
    def shaft_z(self) -> float:
        return self.horizontal_z - self.pivot_delta

    @property
    def left_cam_slab_min_x(self) -> float:
        return self.cam_left_x - self.cam_thickness / 2.0

    @property
    def rod_withdrawal_distance(self) -> float:
        nominal_right_tip = self.rod_length / 2.0
        target_right_tip = self.left_cam_slab_min_x - self.rod_exit_clearance
        return max(0.0, nominal_right_tip - target_right_tip)

    @property
    def right_fixed_rod_clearance_withdrawal(self) -> float:
        """Minus-X travel at which the rod tip reaches the fixed-plate inner face."""

        right_fixed_inner_x = self.fixed_right_x - self.fixed_thickness / 2.0
        return self.rod_length / 2.0 - right_fixed_inner_x

    @property
    def right_fixed_full_withdrawal_gap(self) -> float:
        return self.rod_withdrawal_distance - self.right_fixed_rod_clearance_withdrawal

    @property
    def mechanism_top_z(self) -> float:
        return self.shaft_z + self.plate_diameter / 2.0

    @property
    def completed_workpiece_min_z(self) -> float:
        return self.horizontal_z - self.wire_radius

    @property
    def removal_lift(self) -> float:
        return max(
            0.0,
            self.mechanism_top_z
            + self.removal_end_clearance
            - self.completed_workpiece_min_z,
        )

    @property
    def follower_error(self) -> float:
        return hypot(self.follower_uncertainty_y, self.follower_uncertainty_z)

    @property
    def clearance_rho(self) -> float:
        return self.rod_diameter / 2.0 + self.clearance_margin + self.follower_error

    @property
    def stroke_requirements(self) -> dict[RodName, float]:
        # OPEN clearance is measured from the first-tangent centres.  The
        # additional wire_preload is a distinct final closing stage.
        locked = self.contact_centres
        upright = max(
            0.0,
            locked["upright"].y - (-self.passage_half_width_y - self.clearance_rho),
        )
        bottom_outside = (
            locked["bottom"].y >= self.passage_half_width_y + self.clearance_rho
            or locked["bottom"].z <= self.passage_z_min - self.clearance_rho
        )
        bottom = 0.0 if bottom_outside else self.clearance_rho
        diagonal_delta_y = (
            self.passage_half_width_y + self.clearance_rho - locked["diagonal"].y
        )
        diagonal = max(0.0, sqrt(2.0) * diagonal_delta_y)
        return {"upright": upright, "bottom": bottom, "diagonal": diagonal}

    @property
    def common_stroke(self) -> float:
        return self.contact_stroke + self.wire_preload

    @property
    def contact_stroke(self) -> float:
        """Uniform OPEN-to-first-tangency travel shared by all three rods."""

        return max(self.stroke_requirements.values())

    def _centres_at_offset(self, offset: float) -> dict[RodName, PointYZ]:
        arc_y = self.bend_center_y - self.bend_radius / sqrt(2.0)
        arc_z = self.bend_center_z - self.bend_radius / sqrt(2.0)
        return {
            "upright": PointYZ(-offset, self.bend_center_z + self.bend_radius),
            "bottom": PointYZ(2.0 * self.bend_radius, self.horizontal_z - offset),
            "diagonal": PointYZ(
                arc_y + offset / sqrt(2.0),
                arc_z + offset / sqrt(2.0),
            ),
        }

    @property
    def contact_centres(self) -> dict[RodName, PointYZ]:
        """Three rod centres at first wire tangency (zero geometric preload)."""

        return self._centres_at_offset(self.tangent_contact_offset)

    @property
    def locked_centres(self) -> dict[RodName, PointYZ]:
        return self._centres_at_offset(self.contact_offset)

    @property
    def journal_z_tip_local(self) -> float:
        return sqrt((self.plate_diameter / 2.0) ** 2 - (self.journal_throat / 2.0 + self.journal_tip_width) ** 2)

    @property
    def journal_intersection_z_local(self) -> float:
        return sqrt((self.fixed_groove_od / 2.0) ** 2 - (self.journal_throat / 2.0) ** 2)

    @property
    def keeper_z_tip_local(self) -> float:
        return -sqrt((self.keeper_od / 2.0) ** 2 - (self.keeper_throat / 2.0 + self.keeper_tip_width) ** 2)

    @property
    def cam_path_max_step_rad(self) -> float:
        return radians(self.cam_path_step_deg)

P13_DEFAULTS = P13Parameters()

P13_SAFE_RETUNE_FIELDS = frozenset(
    {
        "c_sw",
        "wire_diameter_design",
        "wire_preload",
        "diagnostic_lane_widths",
        "diagnostic_cam_bores",
        "diagnostic_cam_across_flats",
        "diagnostic_journal_ods",
        "diagnostic_lane_coupon_x",
        "diagnostic_lane_coupon_y",
        "diagnostic_lane_pitch",
        "diagnostic_bore_coupon_x",
        "diagnostic_bore_coupon_y",
        "diagnostic_bore_pitch",
        "diagnostic_coupon_thickness",
        "follower_uncertainty_y",
        "follower_uncertainty_z",
        "clearance_margin",
    }
)
P13_REGATE_FIELDS = frozenset(field.name for field in fields(P13Parameters)) - P13_SAFE_RETUNE_FIELDS


def cad_source_removal_domain(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Formal Domain-A schema for the source geometry, never a measured p_c claim."""

    left_cam_transverse = max(0.0, (p.cam_d_bore_od - p.shaft_od) / 2.0)
    fixed_guide_transverse = max(0.0, (p.fixed_groove_od - p.journal_land_od) / 2.0)
    keeper_transverse = max(0.0, (p.keeper_id - p.keeper_groove_od) / 2.0)
    variables = {
        "c_sw": {"unit": "millimetre", "bounds": [0.50, 0.75], "kind": "closed-interval"},
        "wire_diameter_design": {"unit": "millimetre", "bounds": [4.20, 4.30], "kind": "closed-interval"},
        "theta_R_OPEN": {"unit": "degree", "bounds": [0.0, 0.0], "kind": "fixed-command"},
        "X_fixed_left": {"unit": "millimetre", "bounds": [-14.60, -14.40], "kind": "closed-interval"},
        "X_fixed_right": {"unit": "millimetre", "bounds": [14.40, 14.60], "kind": "closed-interval"},
        "X_keeper": {"unit": "millimetre", "bounds": [p.keeper_groove_x - 0.10, p.keeper_groove_x + 0.10], "kind": "derived-closed-interval"},
        "X_cam_projection": {"unit": "millimetre", "bounds": [-17.75, -17.25], "kind": "coupled-projection"},
        "left_cam_transverse_radius": {"unit": "millimetre", "bounds": [0.0, left_cam_transverse], "kind": "connected-component-enclosure"},
        "left_fixed_transverse_radius": {"unit": "millimetre", "bounds": [0.0, fixed_guide_transverse], "kind": "connected-component-enclosure"},
        "right_fixed_transverse_radius": {"unit": "millimetre", "bounds": [0.0, fixed_guide_transverse], "kind": "connected-component-enclosure"},
        "keeper_transverse_radius": {"unit": "millimetre", "bounds": [0.0, keeper_transverse], "kind": "connected-component-enclosure"},
        "right_fixed_roll": {
            "unit": "degree",
            "bounds": list(P13_FULL_ROLL_DOMAIN_DEG),
            "kind": "periodic-S1-projection-with-stage-correlated-admissibility",
        },
        "keeper_roll": {"unit": "degree", "bounds": [0.0, 360.0], "kind": "periodic-S1"},
        "rod_roll_each": {"unit": "degree", "bounds": [0.0, 360.0], "kind": "periodic-S1-x3"},
        "right_cap_roll_each": {"unit": "degree", "bounds": list(P13_FULL_ROLL_DOMAIN_DEG), "kind": "periodic-S1-x3-non-invariant"},
        "left_cap_engagement_each": {"unit": "millimetre", "bounds": list(P13_CAP_ENGAGEMENT_DOMAIN_MM), "kind": "frozen-per-specimen-x3"},
        "right_cap_engagement_each": {"unit": "millimetre", "bounds": list(P13_CAP_ENGAGEMENT_DOMAIN_MM), "kind": "movable-before-removal-x3"},
        "source_profile_deviation": {"unit": "millimetre", "bounds": [0.0, 0.0], "kind": "exact-source-only"},
    }
    return {
        "schema": "P13CADSourceRemovalDomain/v1",
        "status": "CAD_SOURCE_DOMAIN_CERTIFIED",
        "parentBrief": {"path": P13_GATE0_BRIEF_PATH, "sha256": P13_GATE0_BRIEF_SHA256},
        "amendment": {"path": P13_DOMAIN_AMENDMENT_PATH, "sha256": P13_DOMAIN_AMENDMENT_SHA256},
        "variables": variables,
        "correlations": {
            "X_cam_lower": "left cam hub outer face >= keeper right face + axial_endplay",
            "X_cam_upper": "X_cam <= X_fixed_left - 2.85 mm",
            "openState": "theta_R_OPEN = open_angle_deg = 0 degree",
            "rightCaps": "complete S1 is non-roll-invariant and is certified in Stage 1 before removal",
            "rightFixedRoll": "projection is complete S1; admissibility is the staged correlated union D0..D6",
        },
        "topology": {
            "remainingDuringLift": ["left_cam", "left_fixed", "right_fixed", "right_actuator", "separate_D_shaft", "shaft_keeper"],
            "removedBeforeLift": ["three_right_caps", "three_complete_rod_permanent_left_cap_units"],
            "workpiece": "one complete connected XT60 plus two full 90-degree leads",
        },
        "rightFixedRollAdmissibleUnion": right_fixed_roll_stage_union(p),
        "coverage": {
            "allVariablesBounded": True,
            "allPeriodicDomainProjectionsComplete": True,
            "coupledAxialConstraintsRetained": True,
            "rightFixedRollNeverIndependentWhileRodsJournaled": True,
        },
        "physicalRecordStatus": "PHYSICAL_RECORD_NOT_INSTANTIATED",
    }


def validate_cad_source_removal_domain(
    candidate: dict[str, object], p: P13Parameters = P13_DEFAULTS
) -> None:
    """Fail closed on a missing Domain-A variable, correlation, topology or provenance item."""

    expected = cad_source_removal_domain(p)
    if candidate != expected:
        missing_variables = sorted(
            set(expected["variables"]) - set(candidate.get("variables", {}))
        )
        missing_correlations = sorted(
            set(expected["correlations"]) - set(candidate.get("correlations", {}))
        )
        raise ValueError(
            "CAD source removal domain gap: "
            f"missingVariables={missing_variables}, missingCorrelations={missing_correlations}"
        )


def _engagement_interval(
    domain: dict[str, object], variable: str
) -> tuple[float, float]:
    """Return one finite ordered Domain-A cap-engagement interval."""

    try:
        bounds = domain["variables"][variable]["bounds"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Domain-A engagement interval missing: {variable}") from exc
    if (
        not isinstance(bounds, list)
        or len(bounds) != 2
        or any(not isinstance(value, (int, float)) or not isfinite(float(value)) for value in bounds)
        or float(bounds[0]) < 0.0
        or float(bounds[0]) > float(bounds[1])
    ):
        raise ValueError(f"Domain-A engagement interval invalid: {variable}")
    return float(bounds[0]), float(bounds[1])


def _roll_interval(
    domain: dict[str, object], variable: str
) -> tuple[float, float]:
    """Return one finite ordered Domain-A periodic-roll interval."""

    try:
        bounds = domain["variables"][variable]["bounds"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Domain-A roll interval missing: {variable}") from exc
    if (
        not isinstance(bounds, list)
        or len(bounds) != 2
        or any(not isinstance(value, (int, float)) or not isfinite(float(value)) for value in bounds)
        or float(bounds[0]) > float(bounds[1])
    ):
        raise ValueError(f"Domain-A roll interval invalid: {variable}")
    return float(bounds[0]), float(bounds[1])


def physical_record_schema() -> dict[str, object]:
    required_breps = [
        "left_cam", "left_fixed", "right_fixed", "right_actuator", "separate_D_shaft", "shaft_keeper",
        "rod_upright", "rod_bottom", "rod_diagonal", "left_cap_upright", "left_cap_bottom",
        "left_cap_diagonal", "right_cap_upright", "right_cap_bottom", "right_cap_diagonal",
        "complete_workpiece", "frame_esc_reference", "iron_left", "iron_right",
    ]
    required_records = [
        "specimen_id", "measurement_provenance", "registration_frames", "lane_profiles",
        "bore_key_journal_keeper_geometry", "rod_end_frames_and_straightness",
        "left_cap_seated_engagements", "movable_component_domains", "breps",
    ]
    role_policies = {
        "left_cam": {"labelTokens": ["left_cam"], "minSolids": 1},
        "left_fixed": {"labelTokens": ["fixed_guide"], "minSolids": 1},
        "right_fixed": {"labelTokens": ["fixed_guide"], "minSolids": 1},
        "right_actuator": {"labelTokens": ["right", "actuator"], "minSolids": 1},
        "separate_D_shaft": {"labelTokens": ["shaft"], "minSolids": 1, "minSpanX": 40.0},
        "shaft_keeper": {"labelTokens": ["shaft_keeper"], "minSolids": 1},
        "rod_upright": {"labelTokens": ["rod", "upright"], "minSolids": 1, "minSpanX": 49.0},
        "rod_bottom": {"labelTokens": ["rod", "bottom"], "minSolids": 1, "minSpanX": 49.0},
        "rod_diagonal": {"labelTokens": ["rod", "diagonal"], "minSolids": 1, "minSpanX": 49.0},
        "left_cap_upright": {"labelTokens": ["left_cap"], "minSolids": 1, "maxSpan": 8.1},
        "left_cap_bottom": {"labelTokens": ["left_cap"], "minSolids": 1, "maxSpan": 8.1},
        "left_cap_diagonal": {"labelTokens": ["left_cap"], "minSolids": 1, "maxSpan": 8.1},
        "right_cap_upright": {"labelTokens": ["right_cap"], "minSolids": 1, "maxSpan": 8.1},
        "right_cap_bottom": {"labelTokens": ["right_cap"], "minSolids": 1, "maxSpan": 8.1},
        "right_cap_diagonal": {"labelTokens": ["right_cap"], "minSolids": 1, "maxSpan": 8.1},
        "complete_workpiece": {"labelTokens": ["workpiece"], "minSolids": 1, "minSpanZ": 35.0},
        "frame_esc_reference": {"labelTokens": ["esc"], "minSolids": 2},
        "iron_left": {"labelTokens": ["iron"], "minSolids": 2},
        "iron_right": {"labelTokens": ["iron"], "minSolids": 2},
    }
    return {
        "schema": "P13PhysicalMeasuredRecord/v1",
        "statusWhenAbsent": "PHYSICAL_RECORD_NOT_INSTANTIATED",
        "statusWhenCertified": "MEASURED_SPECIMEN_GEOMETRY_CERTIFIED",
        "requiredRecords": required_records,
        "requiredBREPs": required_breps,
        "brepEntrySchema": {
            "required": ["role", "path", "sha256", "registrationFrame", "provenance"],
            "allowedExtensions": [".step", ".stp"],
            "pathMustExist": True,
            "freshProcessParse": True,
        },
        "registrationFrameSchema": {
            "units": "millimetre",
            "convention": "right-handed",
            "transform": "finite-row-major-4x4-rigid-transform-det-plus-one",
        },
        "measurementSchema": {
            "required": ["value", "uncertainty", "unit", "range", "method", "measured_at_utc"],
            "finite": True,
            "rangeOrderedAndContainsValue": True,
        },
        "rolePolicies": role_policies,
        "allowedHashAliasGroups": [
            ["left_fixed", "right_fixed"],
            ["rod_upright", "rod_bottom", "rod_diagonal"],
            ["left_cap_upright", "left_cap_bottom", "left_cap_diagonal"],
            ["right_cap_upright", "right_cap_bottom", "right_cap_diagonal"],
        ],
        "missingDataPolicy": "FAIL_CLOSED",
    }


def _parse_utc_timestamp(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{field} must be an ISO-8601 UTC timestamp ending Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid UTC timestamp") from exc
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0.0:
        raise ValueError(f"{field} must be UTC")
    return value


def _validate_registration_frame(frame: object, field: str) -> None:
    if not isinstance(frame, dict):
        raise ValueError(f"{field} must be a typed registration frame")
    if frame.get("units") != "millimetre" or frame.get("convention") != "right-handed":
        raise ValueError(f"{field} must be right-handed millimetre coordinates")
    transform = frame.get("transform")
    if (
        not isinstance(transform, list)
        or len(transform) != 16
        or any(not isinstance(value, (int, float)) or not isfinite(float(value)) for value in transform)
    ):
        raise ValueError(f"{field}.transform must contain 16 finite numbers")
    matrix = [list(map(float, transform[index : index + 4])) for index in range(0, 16, 4)]
    if any(abs(matrix[3][index] - target) > 1.0e-8 for index, target in enumerate((0, 0, 0, 1))):
        raise ValueError(f"{field}.transform must be an affine rigid transform")
    rotation = [row[:3] for row in matrix[:3]]
    for row_index, row in enumerate(rotation):
        for other_index, other in enumerate(rotation):
            dot = sum(left * right for left, right in zip(row, other))
            target = 1.0 if row_index == other_index else 0.0
            if abs(dot - target) > 1.0e-6:
                raise ValueError(f"{field}.transform rotation is not orthonormal")
    determinant = (
        rotation[0][0] * (rotation[1][1] * rotation[2][2] - rotation[1][2] * rotation[2][1])
        - rotation[0][1] * (rotation[1][0] * rotation[2][2] - rotation[1][2] * rotation[2][0])
        + rotation[0][2] * (rotation[1][0] * rotation[2][1] - rotation[1][1] * rotation[2][0])
    )
    if abs(determinant - 1.0) > 1.0e-6:
        raise ValueError(f"{field}.transform determinant must be +1")


def _validate_measurement(value: object, field: str, timestamp: str, unit: str = "millimetre") -> None:
    required = set(physical_record_schema()["measurementSchema"]["required"])
    if not isinstance(value, dict) or not required <= set(value):
        raise ValueError(f"{field} must be a typed measurement")
    scalar = value["value"]
    uncertainty = value["uncertainty"]
    bounds = value["range"]
    if (
        not isinstance(scalar, (int, float))
        or not isinstance(uncertainty, (int, float))
        or not isfinite(float(scalar))
        or not isfinite(float(uncertainty))
        or float(uncertainty) < 0.0
        or not isinstance(bounds, list)
        or len(bounds) != 2
        or any(not isinstance(item, (int, float)) or not isfinite(float(item)) for item in bounds)
        or float(bounds[0]) > float(bounds[1])
        or not float(bounds[0]) <= float(scalar) <= float(bounds[1])
        or value.get("unit") != unit
        or not isinstance(value.get("method"), str)
        or not value["method"].strip()
        or value.get("measured_at_utc") != timestamp
    ):
        raise ValueError(f"{field} contains invalid value, uncertainty, range, unit, method, or timestamp")


def _fresh_process_step_facts(path: Path) -> dict[str, object]:
    probe = """
import json, sys
from build123d import import_step
shape = import_step(sys.argv[1])
solids = list(shape.solids())
box = shape.bounding_box()
print(json.dumps({
    'label': shape.label,
    'solidCount': len(solids),
    'valid': bool(shape.is_valid) and all(bool(solid.is_valid) for solid in solids),
    'volume': float(sum(solid.volume for solid in solids)),
    'span': [float(box.size.X), float(box.size.Y), float(box.size.Z)],
}))
"""
    result = subprocess.run(
        [sys.executable, "-c", probe, str(path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise ValueError(f"fresh-process STEP parse failed for {path.name}: {result.stderr.strip()}")
    try:
        facts = json.loads(result.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError) as exc:
        raise ValueError(f"fresh-process STEP facts missing for {path.name}") from exc
    if not facts["valid"] or facts["solidCount"] < 1 or facts["volume"] <= 0.0:
        raise ValueError(f"STEP has no valid positive-volume solid: {path.name}")
    return facts


def validate_physical_record(record: dict[str, object] | None) -> None:
    schema = physical_record_schema()
    if record is None:
        raise ValueError("PHYSICAL_RECORD_NOT_INSTANTIATED")
    if not isinstance(record, dict):
        raise ValueError("measured specimen record must be an object")
    missing_records = sorted(set(schema["requiredRecords"]) - set(record))
    if missing_records:
        raise ValueError(f"incomplete measured specimen record: missingRecords={missing_records}")
    specimen_id = record["specimen_id"]
    if not isinstance(specimen_id, str) or not re.fullmatch(r"P13-[A-Za-z0-9][A-Za-z0-9._-]{2,63}", specimen_id):
        raise ValueError("specimen_id must match P13-<unique-id>")
    provenance = record["measurement_provenance"]
    if (
        not isinstance(provenance, dict)
        or not isinstance(provenance.get("operator"), str)
        or not provenance["operator"].strip()
        or not isinstance(provenance.get("instrument_ids"), list)
        or not provenance["instrument_ids"]
        or any(not isinstance(item, str) or not item.strip() for item in provenance["instrument_ids"])
        or not isinstance(provenance.get("method"), str)
        or not provenance["method"].strip()
    ):
        raise ValueError("measurement_provenance is empty or untyped")
    timestamp = _parse_utc_timestamp(provenance.get("measured_at_utc"), "measurement_provenance.measured_at_utc")

    frames = record["registration_frames"]
    if not isinstance(frames, dict) or set(frames) != set(schema["requiredBREPs"]):
        raise ValueError("registration_frames must contain exactly one typed frame per role")
    for role, frame in frames.items():
        _validate_registration_frame(frame, f"registration_frames.{role}")

    lanes = record["lane_profiles"]
    if not isinstance(lanes, dict) or set(lanes) != set(ROD_NAMES):
        raise ValueError("lane_profiles must contain exactly upright, bottom, and diagonal")
    for name, lane in lanes.items():
        if not isinstance(lane, dict) or not isinstance(lane.get("sampleCount"), int) or lane["sampleCount"] < 2:
            raise ValueError(f"lane_profiles.{name} requires at least two measured samples")
        _validate_measurement(lane.get("width"), f"lane_profiles.{name}.width", timestamp)
        _validate_measurement(lane.get("depth"), f"lane_profiles.{name}.depth", timestamp)

    bore_geometry = record["bore_key_journal_keeper_geometry"]
    bore_fields = ("cam_d_bore_od", "cam_d_bore_across_flat", "fixed_journal_id", "keeper_id")
    if not isinstance(bore_geometry, dict) or set(bore_geometry) != set(bore_fields):
        raise ValueError("bore_key_journal_keeper_geometry fields are incomplete")
    for name in bore_fields:
        _validate_measurement(bore_geometry[name], f"bore_key_journal_keeper_geometry.{name}", timestamp)

    rods = record["rod_end_frames_and_straightness"]
    if not isinstance(rods, dict) or set(rods) != set(ROD_NAMES):
        raise ValueError("rod_end_frames_and_straightness must contain all three rods")
    for name, row in rods.items():
        if not isinstance(row, dict) or set(row) != {"leftEndX", "rightEndX", "straightness"}:
            raise ValueError(f"rod_end_frames_and_straightness.{name} is incomplete")
        for key in row:
            _validate_measurement(row[key], f"rod_end_frames_and_straightness.{name}.{key}", timestamp)

    engagements = record["left_cap_seated_engagements"]
    if not isinstance(engagements, dict) or set(engagements) != set(ROD_NAMES):
        raise ValueError("left_cap_seated_engagements must contain all three rods")
    for name, measurement in engagements.items():
        _validate_measurement(measurement, f"left_cap_seated_engagements.{name}", timestamp)

    movable = record["movable_component_domains"]
    movable_fields = {"right_fixed_roll", "keeper_roll", "rod_roll_each", "right_cap_roll_each"}
    if not isinstance(movable, dict) or set(movable) != movable_fields:
        raise ValueError("movable_component_domains is incomplete")
    for name, row in movable.items():
        if (
            not isinstance(row, dict)
            or set(row) != {"lower", "upper", "uncertainty", "unit", "periodic", "method", "measured_at_utc"}
            or any(not isinstance(row[key], (int, float)) or not isfinite(float(row[key])) for key in ("lower", "upper", "uncertainty"))
            or float(row["lower"]) > float(row["upper"])
            or float(row["uncertainty"]) < 0.0
            or row["unit"] != "degree"
            or not isinstance(row["periodic"], bool)
            or not isinstance(row["method"], str)
            or not row["method"].strip()
            or row["measured_at_utc"] != timestamp
        ):
            raise ValueError(f"movable_component_domains.{name} is invalid")

    breps = record["breps"]
    if not isinstance(breps, dict):
        raise ValueError("breps must be an object")
    missing_breps = sorted(set(schema["requiredBREPs"]) - set(breps))
    extra_breps = sorted(set(breps) - set(schema["requiredBREPs"]))
    if missing_breps or extra_breps:
        raise ValueError(f"BREP role mismatch: missing={missing_breps}, extra={extra_breps}")

    hashes_to_roles: dict[str, list[str]] = {}
    facts_by_hash: dict[str, dict[str, object]] = {}
    for role in schema["requiredBREPs"]:
        entry = breps[role]
        required = set(schema["brepEntrySchema"]["required"])
        if not isinstance(entry, dict) or not required <= set(entry) or entry.get("role") != role:
            raise ValueError(f"malformed BREP entry for {role}")
        path = Path(entry["path"])
        digest = entry["sha256"]
        if path.suffix.lower() not in schema["brepEntrySchema"]["allowedExtensions"] or not path.is_file():
            raise ValueError(f"BREP {role} must be an existing STEP/STP file")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"BREP hash mismatch for {role}")
        if entry["registrationFrame"] != frames[role]:
            raise ValueError(f"BREP registration frame mismatch for {role}")
        role_provenance = entry["provenance"]
        if (
            not isinstance(role_provenance, dict)
            or role_provenance.get("specimen_id") != specimen_id
            or role_provenance.get("role") != role
            or role_provenance.get("measured_at_utc") != timestamp
            or not isinstance(role_provenance.get("method"), str)
            or not role_provenance["method"].strip()
            or not isinstance(role_provenance.get("source"), str)
            or not role_provenance["source"].strip()
        ):
            raise ValueError(f"BREP provenance mismatch for {role}")
        hashes_to_roles.setdefault(digest, []).append(role)
        if digest not in facts_by_hash:
            facts_by_hash[digest] = _fresh_process_step_facts(path)
        facts = facts_by_hash[digest]
        policy = schema["rolePolicies"][role]
        label = str(facts["label"]).lower()
        if not all(token in label for token in policy["labelTokens"]):
            raise ValueError(f"STEP label does not match role {role}: {facts['label']!r}")
        if facts["solidCount"] < policy["minSolids"]:
            raise ValueError(f"STEP occurrence count is too low for {role}")
        span = facts["span"]
        if "minSpanX" in policy and span[0] < policy["minSpanX"]:
            raise ValueError(f"STEP X span is too small for {role}")
        if "minSpanZ" in policy and span[2] < policy["minSpanZ"]:
            raise ValueError(f"STEP Z span is too small for {role}")
        if "maxSpan" in policy and max(span) > policy["maxSpan"]:
            raise ValueError(f"STEP span is too large for {role}")

    allowed_aliases = [set(group) for group in schema["allowedHashAliasGroups"]]
    for digest, roles in hashes_to_roles.items():
        role_set = set(roles)
        if len(role_set) > 1 and not any(role_set <= group for group in allowed_aliases):
            raise ValueError(f"incompatible BREP roles share one hash {digest}: {sorted(role_set)}")


def cad_source_global_removal_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Directed closed-form global bound for Domain-A complete-workpiece lift."""

    domain = cad_source_removal_domain(p)
    validate_cad_source_removal_domain(domain, p)
    c_corner = domain["variables"]["c_sw"]["bounds"][0]
    wire_corner = domain["variables"]["wire_diameter_design"]["bounds"][1]
    pivot_delta = (
        p.shaft_radius + wire_corner / 2.0 + c_corner - p.initial_arc_distance
    ) / sqrt(2.0)
    shaft_z_corner = p.horizontal_z - pivot_delta
    left_cam_shift = domain["variables"]["left_cam_transverse_radius"]["bounds"][1]
    mechanism_candidates = {
        "leftCam": shaft_z_corner + p.plate_diameter / 2.0 + left_cam_shift,
        "rightActuatorCam": shaft_z_corner + p.plate_diameter / 2.0,
        "leftFixed": shaft_z_corner + p.plate_diameter / 2.0,
        "rightFixedAllS1": shaft_z_corner + p.plate_diameter / 2.0,
        "shaft": shaft_z_corner + p.shaft_radius,
        "keeperAllS1": shaft_z_corner
        + domain["variables"]["keeper_transverse_radius"]["bounds"][1]
        + p.keeper_od / 2.0,
    }
    mechanism_top_upper = max(mechanism_candidates.values())
    payload_candidates = {
        "insulatedLead": p.horizontal_z - wire_corner / 2.0,
        "strippedConductor": p.horizontal_z - p.stripped_diameter / 2.0,
        "solderEnvelope": p.horizontal_z - p.solder_radius,
        "solderCup": p.cup_z0 - p.cup_diameter / 2.0,
        "xt60Body": p.xt60_body_z0,
    }
    payload_min_lower = min(payload_candidates.values())
    exact_required = max(
        0.0, mechanism_top_upper + p.removal_end_clearance - payload_min_lower
    )
    lower = floor(exact_required / P13_EPS_GLOBAL_MM) * P13_EPS_GLOBAL_MM
    command = ceil(exact_required / P13_EPS_GLOBAL_MM) * P13_EPS_GLOBAL_MM
    if command - exact_required <= 1.0e-12:
        command += P13_EPS_GLOBAL_MM
    width = command - lower
    margin = command - exact_required
    if width > P13_EPS_GLOBAL_MM + 1.0e-12 or margin <= 0.0:
        raise ValueError("global removal command failed directed outward rounding")
    return {
        "schema": "P13CADSourceRemovalCertificate/v1",
        "status": "CAD_SOURCE_DOMAIN_CERTIFIED",
        "physicalRecordStatus": "PHYSICAL_RECORD_NOT_INSTANTIATED",
        "proofMethod": "closed-form monotone interval bound with directed outward 0.005-mm rounding",
        "domain": domain,
        "objective": "max(0,Z_mech_top+c_remove_end-Z_payload_min)",
        "worstCaseCorner": {"c_sw": c_corner, "wire_diameter_design": wire_corner, "leftCamTransverse": left_cam_shift},
        "mechanismTopCandidates": {"unit": "millimetre", "value": mechanism_candidates},
        "payloadMinCandidates": {"unit": "millimetre", "value": payload_candidates},
        "requiredLiftExactBound": {"unit": "millimetre", "value": exact_required},
        "certifiedBracket": {"unit": "millimetre", "lower": lower, "upper": command, "width": width},
        "globalRemovalCommand": {"unit": "millimetre", "value": command},
        "endpointMargin": {"unit": "millimetre", "value": margin},
        "epsGlobal": {"unit": "millimetre", "value": P13_EPS_GLOBAL_MM},
        "coverageComplete": True,
        "converged": True,
        "rightCapStage1Coverage": {
            "status": "CERTIFIED_BY_CONTINUOUS_REMOVAL_CERTIFICATE",
            "certificatePath": "removal.rightCapStage1Removal",
            "engagementDomainSource": "domain.variables.right_cap_engagement_each.bounds",
            "rollDomainSource": "domain.variables.right_cap_roll_each.bounds",
        },
        "nominalSeedOnly": {"unit": "millimetre", "value": p.removal_lift},
    }


def parameter_unit(name: str) -> str:
    if name.endswith("_count"):
        return "count"
    if name.endswith("_deg"):
        return "degree"
    if name in {
        "diagnostic_lane_widths",
        "diagnostic_cam_bores",
        "diagnostic_cam_across_flats",
        "diagnostic_journal_ods",
    }:
        return "millimetre[]"
    if name == "continuous_overlap_volume_tolerance":
        return "cubic_millimetre"
    return "millimetre"


def parameter_manifest(p: P13Parameters = P13_DEFAULTS) -> dict[str, object]:
    values = asdict(p)
    source_certificate = cad_source_global_removal_certificate(p)
    return {
        "schema": "P13Parameters/v1",
        "briefPath": P13_GATE0_BRIEF_PATH,
        "briefSha256": P13_GATE0_BRIEF_SHA256,
        "frozenTopology": P13_FROZEN_TOPOLOGY,
        "domainAmendmentPath": P13_DOMAIN_AMENDMENT_PATH,
        "domainAmendmentSha256": P13_DOMAIN_AMENDMENT_SHA256,
        "cadSourceStatus": "CAD_SOURCE_DOMAIN_CERTIFIED",
        "physicalRecordStatus": "PHYSICAL_RECORD_NOT_INSTANTIATED",
        "parameters": {
            field.name: {
                "type": str(field.type),
                "unit": parameter_unit(field.name),
                "class": "safe-retune" if field.name in P13_SAFE_RETUNE_FIELDS else "requires-regate",
                # Keep the in-memory manifest identical to its JSON evidence
                # representation; JSON serializes tuples as arrays.
                "value": list(values[field.name])
                if isinstance(values[field.name], tuple)
                else values[field.name],
            }
            for field in fields(P13Parameters)
        },
        "derived": {
            "initial_arc_distance": {"unit": "millimetre", "value": p.initial_arc_distance},
            "pivot_delta": {"unit": "millimetre", "value": p.pivot_delta},
            "shaft_y": {"unit": "millimetre", "value": p.shaft_y},
            "shaft_z": {"unit": "millimetre", "value": p.shaft_z},
            "stroke_requirements": {"unit": "millimetre", "value": p.stroke_requirements},
            "contact_stroke": {"unit": "millimetre", "value": p.contact_stroke},
            "common_stroke": {"unit": "millimetre", "value": p.common_stroke},
            "tangent_contact_offset": {
                "unit": "millimetre",
                "value": p.tangent_contact_offset,
            },
            "locked_contact_offset": {
                "unit": "millimetre",
                "value": p.locked_contact_offset,
            },
            "nominal_thrust_land_gap": {
                "unit": "millimetre",
                "value": p.nominal_thrust_land_gap,
            },
            "rod_withdrawal_distance": {
                "unit": "millimetre",
                "value": p.rod_withdrawal_distance,
            },
            "right_fixed_rod_clearance_withdrawal": {
                "unit": "millimetre",
                "value": p.right_fixed_rod_clearance_withdrawal,
            },
            "right_fixed_full_withdrawal_gap": {
                "unit": "millimetre",
                "value": p.right_fixed_full_withdrawal_gap,
            },
            "right_cap_min_radial_wall": {
                "unit": "millimetre",
                "value": p.right_cap_min_radial_wall,
            },
            "right_cap_nominal_radial_clearance": {
                "unit": "millimetre",
                "value": p.right_cap_nominal_radial_clearance,
            },
            "mechanism_top_z": {"unit": "millimetre", "value": p.mechanism_top_z},
            "completed_workpiece_min_z": {
                "unit": "millimetre",
                "value": p.completed_workpiece_min_z,
            },
            "removal_lift_nominal_seed_only": {"unit": "millimetre", "value": p.removal_lift},
            "removal_lift": {
                "unit": "millimetre",
                "value": p.removal_lift,
                "acceptanceRole": "nominal-seed-only-not-a-removal-command",
            },
            "global_removal_command": source_certificate["globalRemovalCommand"],
            "continuous_global_certificates": {
                "motion": continuous_motion_certificate(p),
                "rodLeftCapWithdrawal": rod_left_cap_withdrawal_certificate(p),
                "workpiecePlusZ": workpiece_plus_z_certificate(p),
            },
        },
    }


def parameter_manifest_sha256(p: P13Parameters = P13_DEFAULTS) -> str:
    payload = json.dumps(parameter_manifest(p), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def source_revision_sha256() -> str:
    return sha256(Path(__file__).read_bytes()).hexdigest()


def continuous_overlap_tolerance(p: P13Parameters = P13_DEFAULTS) -> float:
    """Single production read for the solid-overlap acceptance tolerance."""

    return p.continuous_overlap_volume_tolerance


P13_EFFECT_DOMAIN_CONSEQUENCES: dict[str, frozenset[str]] = {
    "boolean-geometry": frozenset(
        {
            "datum:boolean-allowances",
            "cutter:all-robust-boolean-cutters",
            "solid:all-boolean-generated-parts",
            "state:all-geometry-bearing-states",
            "test:solid-validity-and-source-export-parity",
            "export:all-geometry-step",
        }
    ),
    "rod-stock": frozenset(
        {
            "datum:rod-radius-and-physical-endpoints",
            "datum:rod-withdrawal-distance",
            "cutter:rod-fit-and-cap-socket-diagnostics",
            "solid:three-purchased-rods-and-six-cap-engagements",
            "solid:rod-left-cap-withdrawal-envelopes",
            "state:all-installed-and-normal-removal-states",
            "test:continuous-lane-and-complete-unit-withdrawal-certificates",
            "export:all-workflow-exploded-and-cap-step",
        }
    ),
    "workpiece": frozenset(
        {
            "datum:complete-workpiece-centreline-and-extrema",
            "cutter:none-workpiece-is-positive-geometry",
            "solid:connected-workpiece-and-exact-solder-constituents",
            "solid:workpiece-plus-z-global-bound",
            "state:loaded-locked-solder-cool-release-and-remove",
            "test:workpiece-connectivity-90-degree-and-plus-z-certificate",
            "export:all-loaded-solder-release-removal-step",
        }
    ),
    "pivot": frozenset(
        {
            "datum:initial-arc-distance-pivot-delta-shaft-y-shaft-z",
            "cutter:all-shaft-concentric-bore-groove-key-and-journal-cutters",
            "solid:all-four-plates-separate-D-shaft-and-keeper",
            "state:all-mechanism-and-tool-reference-poses",
            "test:pivot-metamorphic-and-global-clearance-certificates",
            "export:all-mechanism-workflow-and-service-step",
        }
    ),
    "motion": frozenset(
        {
            "datum:locked-centres-stroke-requirements-common-stroke-and-rod-centres",
            "datum:inverse-cam-paths-and-lane-centrelines",
            "cutter:fixed-lane-and-cam-lane-cutters",
            "solid:four-plate-lane-solids-and-three-rod-poses",
            "state:open-loaded-set-close-locked-cool-and-release",
            "test:continuous-full-domain-lane-certificate",
            "export:all-motion-bearing-workflow-step",
        }
    ),
    "plate-stack": frozenset(
        {
            "datum:four-plate-x-stack-and-principal-stack-width",
            "cutter:plate-lanes-centre-bores-keyway-and-journals",
            "solid:left-cam-two-fixed-guides-and-right-actuator",
            "state:all-assembled-service-exploded-and-print-states",
            "test:occurrence-census-solid-validity-and-clearance-certificates",
            "export:all-mechanism-service-exploded-and-print-step",
        }
    ),
    "actuator-shaft": frozenset(
        {
            "datum:D-shaft-head-hubs-x-extents-and-round-groove-frames",
            "cutter:two-cam-D-bores-and-shaft-round-land-annuli",
            "solid:two-D-bored-cams-and-separate-headed-D-shaft",
            "state:all-coupled-rotation-and-service-disassembly-states",
            "test:D-dimensions-phase-lash-endplay-extraction-and-source-export-parity",
            "export:left-cam-right-actuator-shaft-all-core-workflow-and-service-step",
        }
    ),
    "cam-D-bore": frozenset(
        {
            "datum:paired-cam-D-bore-OD-AF-and-shaft-transverse-source-domain",
            "cutter:left-and-right-cam-D-through-bores",
            "solid:both-D-bored-cams",
            "state:all-states-containing-cams-and-shaft",
            "test:cam-D-bore-perturbation-lash-and-source-domain-bound",
            "export:both-cams-core-workflow-exploded-and-print-step",
        }
    ),
    "fixed-journal": frozenset(
        {
            "datum:fixed-groove-and-upward-c-journal-profile",
            "cutter:fixed-centre-upward-c-journal-and-reliefs",
            "solid:two-integral-fixed-guide-plates",
            "state:all-core-and-fixed-guide-service-states",
            "test:upward-journal-topology-and-forbidden-shaft-motion",
            "export:fixed-guide-all-core-workflow-and-service-step",
        }
    ),
    "keeper": frozenset(
        {
            "datum:keeper-groove-and-downward-c-profile",
            "cutter:keeper-centre-mouth-reliefs-and-shaft-groove",
            "solid:round-c-shaft-keeper-and-grooved-separate-D-shaft",
            "state:all-retained-removal-and-service-states",
            "test:keeper-census-removal-clearance-and-service-order",
            "export:shaft-keeper-separate-shaft-core-removal-and-service-step",
        }
    ),
    "rod-caps": frozenset(
        {
            "datum:left-and-right-cap-local-engagement-frames",
            "cutter:left-socket-right-throat-cavity-and-slit",
            "solid:three-permanent-left-and-three-removable-right-caps",
            "solid:rod-left-cap-withdrawal-envelopes",
            "state:all-retained-caps-off-rods-withdrawn-remove-and-exploded-states",
            "test:cap-census-and-complete-unit-withdrawal-certificate",
            "export:left-cap-right-cap-core-removal-exploded-and-print-step",
        }
    ),
    "solder-tool": frozenset(
        {
            "datum:pad-conductor-solder-and-iron-target-frames",
            "cutter:none-review-reference-solids-only",
            "solid:exact-conductors-solder-pads-and-iron-envelopes",
            "state:solder-left-and-solder-right",
            "test:solder-constituent-source-export-parity",
            "export:solder-left-and-solder-right-step",
        }
    ),
    "diagnostic": frozenset(
        {
            "datum:diagnostic-coupon-layout",
            "cutter:diagnostic-lane-and-bore-coupon-cutters",
            "solid:two-diagnostic-coupon-solids",
            "state:fit-coupon-and-print-kit-layout",
            "test:coupon-solidity-and-source-export-parity",
            "export:fit-coupons-and-print-kit-step",
        }
    ),
    "exploded-layout": frozenset(
        {
            "datum:exploded-part-lanes-and-offsets",
            "cutter:none-presentation-transform-only",
            "solid:unchanged-fourteen-exploded-leaves",
            "state:exploded-review-layout",
            "test:exploded-census-and-zero-pairwise-overlap",
            "export:exploded-step-and-snapshots",
        }
    ),
    "print-layout": frozenset(
        {
            "datum:print-bed-layout-and-orientations",
            "cutter:none-presentation-transform-only",
            "solid:fourteen-step-print-kit-leaves-twelve-production-plus-two-coupons",
            "state:print-kit-layout",
            "test:print-kit-census-bed-contact-and-zero-overlap",
            "export:print-kit-step-and-snapshots",
        }
    ),
    "removal": frozenset(
        {
            "datum:rod-withdrawal-distance-removal-lift-and-review-samples",
            "cutter:none-removal-is-rigid-motion",
            "solid:complete-unit-withdrawal-and-workpiece-plus-z-bounds",
            "state:caps-off-rods-withdrawn-removal-sweep-and-remove",
            "test:continuous-complete-unit-withdrawal-and-plus-z-certificates",
            "export:caps-off-rods-withdrawn-removal-sweep-remove-step-and-snapshots",
        }
    ),
    "service-layout": frozenset(
        {
            "datum:service-keeper-fixed-guide-and-actuator-offsets",
            "cutter:none-service-rigid-transform-only",
            "solid:unchanged-five-service-disassembly-leaves",
            "state:service-disassembly-only",
            "test:service-order-and-source-export-parity",
            "export:service-disassembly-step-and-snapshots",
        }
    ),
}


def parameter_effect_domains() -> dict[str, tuple[str, ...]]:
    """Return an exhaustive, explicit primary-parameter effect registry.

    Prefix inference is intentionally forbidden here: every field is assigned
    by name, and the final completeness check fails source import if a new
    mutable field is added without a reviewed consequence domain.
    """

    assignments: dict[str, set[str]] = {
        field.name: set() for field in fields(P13Parameters)
    }

    def bind(domain: str, names: tuple[str, ...]) -> None:
        unknown = set(names) - set(assignments)
        if unknown:
            raise RuntimeError(f"unknown P13 dependency fields in {domain}: {sorted(unknown)}")
        for name in names:
            assignments[name].add(domain)

    bind("boolean-geometry", ("boolean_axial_overcut", "boolean_plate_overcut", "boolean_radial_margin"))
    bind("rod-stock", ("rod_diameter", "rod_length"))
    bind(
        "workpiece",
        (
            "wire_diameter_design", "wire_x", "bend_radius", "xt60_x", "xt60_y", "xt60_z",
            "cup_diameter", "cup_z0", "cup_z1", "horizontal_z", "bend_center_y",
            "bend_center_z", "horizontal_start_y", "vertical_lead_z1", "xt60_body_z0",
            "bend_arc_start_deg", "bend_arc_sweep_deg",
        ),
    )
    bind("pivot", ("shaft_od", "wire_diameter_design", "c_sw", "bend_radius", "bend_center_y", "bend_center_z", "horizontal_z"))
    bind(
        "motion",
        (
            "rod_diameter", "wire_preload", "open_angle_deg", "rise_end_deg",
            "locked_angle_deg", "lane_width", "passage_half_width_y", "passage_z_min",
            "clearance_margin", "follower_uncertainty_y", "follower_uncertainty_z",
            "cam_path_step_deg", "cam_band_segment_count", "bend_radius", "bend_center_y",
            "bend_center_z", "horizontal_z",
        ),
    )
    bind(
        "plate-stack",
        (
            "plate_diameter", "fixed_thickness", "cam_thickness", "main_face_gap",
            "fixed_center_spacing", "thrust_land_od", "fixed_thrust_land_height",
            "cam_thrust_land_height",
        ),
    )
    bind(
        "actuator-shaft",
        (
            "shaft_od", "shaft_d_across_flat", "cam_hub_od", "cam_hub_extension",
            "shaft_head_od", "shaft_head_thickness",
            "shaft_left_end_margin", "axial_endplay", "journal_land_od",
            "fixed_groove_od", "fixed_groove_width", "keeper_groove_od",
            "keeper_groove_width",
        ),
    )
    bind("cam-D-bore", ("cam_d_bore_od", "cam_d_bore_across_flat"))
    bind(
        "fixed-journal",
        ("fixed_groove_od", "journal_throat", "journal_relief_diameter", "journal_tip_width"),
    )
    bind(
        "keeper",
        (
            "keeper_groove_od", "keeper_groove_width", "keeper_tip_width",
            "keeper_relief_diameter", "keeper_od", "keeper_id", "keeper_throat", "keeper_thickness",
        ),
    )
    bind(
        "rod-caps",
        (
            "rod_diameter", "rod_length", "cap_od", "cap_length", "left_cap_socket",
            "left_cap_socket_depth", "right_cap_cavity", "right_cap_throat",
            "right_cap_throat_depth", "right_cap_cavity_end", "right_cap_functional_overcut",
            "right_cap_slit_width",
            "right_cap_slit_z0", "right_cap_slit_z1", "nominal_cap_engagement",
            "cap_reverse_rotation_deg",
        ),
    )
    bind(
        "solder-tool",
        (
            "wire_x", "horizontal_z", "pad_y0", "pad_y1", "pad_thickness_z", "pad_width_x",
            "stripped_y0", "stripped_y1", "stripped_diameter", "solder_radius", "iron_angle_deg",
            "iron_tip_r0", "iron_tip_r1", "iron_tip_length", "iron_barrel_radius", "iron_barrel_length",
        ),
    )
    bind(
        "diagnostic",
        (
            "diagnostic_lane_widths", "diagnostic_cam_bores", "diagnostic_cam_across_flats",
            "diagnostic_journal_ods",
            "diagnostic_coupon_thickness",
            "diagnostic_lane_coupon_x", "diagnostic_lane_coupon_y", "diagnostic_lane_pitch",
            "diagnostic_bore_coupon_x", "diagnostic_bore_coupon_y", "diagnostic_bore_pitch",
            "print_coupon_x_offset", "print_coupon_y",
        ),
    )
    bind(
        "exploded-layout",
        (
            "exploded_plate_offset_x", "exploded_fixed_offset_x", "exploded_keeper_offset_z",
            "exploded_rod_offset_y", "exploded_rod_pitch_z", "exploded_cap_lane_x",
            "exploded_left_cap_lane_y", "exploded_right_cap_lane_y", "exploded_cap_pitch_z",
        ),
    )
    bind(
        "print-layout",
        (
            "print_plate_pitch_x", "print_upper_y", "print_actuator_y", "print_keeper_x",
            "print_keeper_y", "print_cap_left_x0", "print_cap_right_x0", "print_cap_pitch_x",
            "print_cap_y", "print_coupon_y", "print_coupon_x_offset", "print_plate_rotation_deg",
            "print_actuator_rotation_deg", "print_cap_rotation_deg", "print_shaft_x", "print_shaft_y",
            "print_shaft_rotation_deg",
        ),
    )
    bind(
        "removal",
        (
            "rod_length", "rod_diameter", "cap_od", "cap_length", "nominal_cap_engagement",
            "plate_diameter", "fixed_thickness", "cam_thickness", "main_face_gap",
            "fixed_center_spacing", "shaft_od", "wire_diameter_design", "wire_x", "bend_radius",
            "xt60_x", "xt60_y", "xt60_z", "cup_diameter", "cup_z0", "cup_z1",
            "horizontal_z", "bend_center_y", "bend_center_z", "horizontal_start_y",
            "vertical_lead_z1", "xt60_body_z0", "pad_y0", "stripped_y0", "stripped_y1",
            "stripped_diameter", "solder_radius", "removal_review_sample_count",
            "continuous_overlap_volume_tolerance",
            "rod_exit_clearance", "removal_end_clearance", "cap_removed_offset_x",
            "open_angle_deg",
        ),
    )
    bind(
        "service-layout",
        ("service_keeper_offset_z", "service_fixed_offset_z", "service_shaft_end_clearance"),
    )
    missing = sorted(name for name, domains in assignments.items() if not domains)
    if missing:
        raise RuntimeError(f"P13 dependency effect domains missing fields: {missing}")
    return {name: tuple(sorted(domains)) for name, domains in assignments.items()}


P13_NON_RUNTIME_PARAMETER_FUNCTIONS = frozenset(
    {
        "__post_init__",
        "parameter_unit",
        "parameter_manifest",
        "parameter_manifest_sha256",
        "parameter_effect_domains",
        "parameter_runtime_consumers",
        "parameter_dependency_graph",
        "validate_parameter_dependency_graph",
        "parameters_from_overrides",
        "provenance_token",
        "evidence_package",
        "continuous_certificate_package",
        "write_evidence_files",
    }
)


@lru_cache(maxsize=1)
def parameter_runtime_consumers() -> dict[str, list[str]]:
    """Map every mutable field to real source functions that read it.

    Manifest, override, validation, and dependency-registry reads are excluded:
    they cannot justify a parameter that has no effect on a design, diagnostic,
    test, or export consumer.  A newly declared dead field therefore fails
    before evidence can be written.
    """

    field_names = {field.name for field in fields(P13Parameters)}
    readers: dict[str, set[str]] = {name: set() for name in field_names}
    tree = ast.parse(Path(__file__).read_text())

    class RuntimeReadVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.function_stack: list[str] = []

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.function_stack.append(node.name)
            self.generic_visit(node)
            self.function_stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.function_stack.append(node.name)
            self.generic_visit(node)
            self.function_stack.pop()

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if (
                self.function_stack
                and isinstance(node.value, ast.Name)
                and node.value.id in {"p", "self"}
                and node.attr in field_names
                and self.function_stack[-1] not in P13_NON_RUNTIME_PARAMETER_FUNCTIONS
            ):
                readers[node.attr].add(self.function_stack[-1])
            self.generic_visit(node)

    RuntimeReadVisitor().visit(tree)
    missing = sorted(name for name, names in readers.items() if not names)
    if missing:
        raise RuntimeError(f"P13 mutable parameters have no runtime consumer: {missing}")
    return {name: sorted(names) for name, names in sorted(readers.items())}


P13_DEPENDENCY_TERMINALS = (
    "continuous_motion_certificate", "continuous_lane_solid_certificate",
    "continuous_removal_certificate", "cad_source_global_removal_certificate",
    "build_open", "build_loaded", "build_set_close", "build_locked",
    "build_solder_left", "build_solder_right", "build_cool", "build_release",
    "build_caps_off", "build_rods_withdrawn", "build_remove",
    "build_removal_sweep_review", "build_exploded", "build_service_disassembly",
    "build_print_kit", "build_fixed_plate", "build_left_cam",
    "build_right_actuator", "build_shaft_keeper", "build_left_cap",
    "build_right_cap", "build_fit_coupons",
)


P13_TERMINAL_DESCRIPTORS = {
    terminal: frozenset(
        f"{kind}:terminal-{terminal}"
        for kind in ("datum", "cutter", "solid", "state", "test", "export")
    )
    for terminal in P13_DEPENDENCY_TERMINALS
}


@lru_cache(maxsize=1)
def parameter_source_use_map() -> dict[str, object]:
    """AST-derived direct reads, call/property edges, and terminal consumers."""

    tree = ast.parse(Path(__file__).read_text())
    field_names = {field.name for field in fields(P13Parameters)}
    parameter_class = next(
        node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "P13Parameters"
    )
    property_names = {
        node.name
        for node in parameter_class.body
        if isinstance(node, ast.FunctionDef)
        and any(isinstance(item, ast.Name) and item.id == "property" for item in node.decorator_list)
    }
    functions: dict[str, ast.FunctionDef] = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    functions.update(
        {
            f"P13Parameters.{node.name}": node
            for node in parameter_class.body
            if isinstance(node, ast.FunctionDef)
        }
    )
    direct = {name: set() for name in functions}
    calls = {name: set() for name in functions}
    forbidden: list[str] = []
    for owner, function in functions.items():
        for node in ast.walk(function):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id in {"p", "self"}:
                    if node.attr in field_names:
                        direct[owner].add(node.attr)
                    elif node.attr in property_names:
                        calls[owner].add(f"P13Parameters.{node.attr}")
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in functions:
                    calls[owner].add(node.func.id)
                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id == "getattr"
                    and node.args
                    and isinstance(node.args[0], ast.Name)
                    and node.args[0].id in {"p", "self"}
                ):
                    forbidden.append(f"{owner}:{node.lineno}")
    if forbidden:
        raise RuntimeError(f"dynamic P13 parameter getattr is forbidden: {forbidden}")

    def transitive(start: str) -> set[str]:
        found: set[str] = set()
        pending = [start]
        visited: set[str] = set()
        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            found.update(direct.get(current, set()))
            pending.extend(calls.get(current, set()) - visited)
        return found

    terminal_fields = {terminal: sorted(transitive(terminal)) for terminal in P13_DEPENDENCY_TERMINALS}
    return {
        "schema": "P13ASTParameterSourceUses/v1",
        "dynamicGetattr": forbidden,
        "directConsumers": {
            field: sorted(owner for owner, reads in direct.items() if field in reads)
            for field in sorted(field_names)
        },
        "terminalConsumers": {
            field: sorted(terminal for terminal, reads in terminal_fields.items() if field in reads)
            for field in sorted(field_names)
        },
        "terminalFields": terminal_fields,
        "callEdges": {owner: sorted(targets) for owner, targets in calls.items() if targets},
    }


@lru_cache(maxsize=1)
def parameter_dependency_graph() -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}
    runtime_consumers = parameter_runtime_consumers()
    actual = parameter_source_use_map()
    for name, domains in parameter_effect_domains().items():
        consequences = {
            "datum:default-parameter-manifest",
            "cutter:none-unless-listed-by-effect-domain",
            "solid:none-unless-listed-by-effect-domain",
            "state:parameter-manifest-and-provenance",
            "test:dependency-completeness-and-evidence-hash",
            "export:parameter-manifest-dependency-graph-and-artifact-provenance",
        }
        for domain in domains:
            consequences.update(P13_EFFECT_DOMAIN_CONSEQUENCES[domain])
        consequences.update(f"actual-read:{reader}" for reader in actual["directConsumers"][name])
        for terminal in actual["terminalConsumers"][name]:
            consequences.add(f"actual-terminal:{terminal}")
            consequences.update(P13_TERMINAL_DESCRIPTORS[terminal])
        graph[name] = [
            *(f"effect-domain:{domain}" for domain in domains),
            *(f"reader:{reader}" for reader in runtime_consumers[name]),
            *sorted(consequences),
        ]
    return graph


def validate_parameter_dependency_graph(
    candidate: dict[str, list[str]],
) -> None:
    """Reject any missing field or individual downstream consumer.

    The check is deliberately exact rather than checking only that six prefix
    categories exist.  Removing one datum, cutter, solid, state, test or export
    consumer from any registered effect domain is therefore a hard failure.
    """

    expected = parameter_dependency_graph()
    expected_fields = set(expected)
    candidate_fields = set(candidate)
    if candidate_fields != expected_fields:
        raise ValueError(
            "dependency registry field mismatch: "
            f"missing={sorted(expected_fields - candidate_fields)}, "
            f"extra={sorted(candidate_fields - expected_fields)}"
        )
    for name in sorted(expected):
        actual_tokens = set(candidate[name])
        expected_tokens = set(expected[name])
        missing = sorted(expected_tokens - actual_tokens)
        extra = sorted(actual_tokens - expected_tokens)
        if missing or extra:
            raise ValueError(
                f"dependency registry mismatch for {name}: "
                f"missing={missing}, extra={extra}"
            )


def provenance_token(p: P13Parameters = P13_DEFAULTS) -> str:
    return (
        f"brief_{P13_GATE0_BRIEF_SHA256}__"
        f"amendment_{P13_DOMAIN_AMENDMENT_SHA256}__"
        f"manifest_{parameter_manifest_sha256(p)[:12]}__"
        f"source_{source_revision_sha256()[:12]}"
    )


def parameters_from_overrides(
    overrides: dict[str, object] | None = None,
    *,
    allow_regate: bool = False,
) -> P13Parameters:
    overrides = overrides or {}
    frozen = set(overrides) & set(P13_FROZEN_TOPOLOGY)
    if frozen:
        raise ValueError(
            "frozen P13 topology is source-level and cannot be overridden: "
            f"{sorted(frozen)}"
        )
    unknown = set(overrides) - {field.name for field in fields(P13Parameters)}
    if unknown:
        raise ValueError(f"unknown P13 parameter(s): {sorted(unknown)}")
    blocked = set(overrides) & P13_REGATE_FIELDS
    if blocked and not allow_regate:
        raise ValueError(f"requires renewed Gate-0 review: {sorted(blocked)}")
    return replace(P13_DEFAULTS, **overrides)


def parameters_from_env() -> P13Parameters:
    raw = os.environ.get("P13_PARAMS_JSON", "").strip()
    overrides = json.loads(raw) if raw else {}
    allow_regate = os.environ.get("P13_ALLOW_REGATE", "0") == "1"
    return parameters_from_overrides(overrides, allow_regate=allow_regate)


def clear_geometry_caches() -> None:
    """Release cached OCC prototypes between independent validation cases."""
    for builder in (
        _fixed_plate_prototype,
        _left_cam_prototype,
        _right_actuator_prototype,
        _shaft_keeper_prototype,
    ):
        builder.cache_clear()


GUIDE_DIRECTIONS: dict[RodName, PointYZ] = {
    "upright": PointYZ(1.0, 0.0),
    "bottom": PointYZ(0.0, 1.0),
    "diagonal": PointYZ(-1.0 / sqrt(2.0), -1.0 / sqrt(2.0)),
}


def _label(shape: Shape, name: str, color: str | None = None) -> Shape:
    shape.label = name
    if color:
        shape.color = srgb(color)
    return shape


def _tag(value: float) -> str:
    """Stable filename-safe numeric label fragment for source/export parity."""
    return f"{value:.2f}".replace("-", "m").replace(".", "p")


def _x_cylinder(diameter: float, length: float, x: float, y: float, z: float) -> Shape:
    return Pos(x, y, z) * Cylinder(
        diameter / 2.0,
        length,
        rotation=(0.0, 90.0, 0.0),
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def _intersection_volume(first: Shape, second: Shape) -> float:
    common = first.intersect(second)
    if common is None:
        return 0.0
    if hasattr(common, "volume"):
        return float(common.volume)
    return sum(float(item.volume) for item in common)


def _box(center: tuple[float, float, float], size: tuple[float, float, float]) -> Shape:
    return Pos(*center) * Box(*size, align=(Align.CENTER, Align.CENTER, Align.CENTER))


def _fuse(shapes: list[Shape]) -> Shape:
    if not shapes:
        raise ValueError("cannot fuse an empty shape list")
    result = shapes[0]
    for item in shapes[1:]:
        result = result + item
    return result


def _rotate_about_shaft(shape: Shape, angle_deg: float, p: P13Parameters) -> Shape:
    return Pos(0.0, p.shaft_y, p.shaft_z) * Rot(angle_deg, 0.0, 0.0) * Pos(
        0.0, -p.shaft_y, -p.shaft_z
    ) * shape


def ease(value: float) -> float:
    a = max(0.0, min(1.0, value))
    return 3.0 * a * a - 2.0 * a * a * a


def common_travel(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> float:
    if not 0.0 <= angle_deg <= p.locked_angle_deg:
        raise ValueError("angle must be within OPEN..LOCKED")
    if angle_deg <= p.rise_end_deg:
        return p.contact_stroke * ease(angle_deg / p.rise_end_deg)
    preload_phase = (angle_deg - p.rise_end_deg) / (
        p.locked_angle_deg - p.rise_end_deg
    )
    return p.contact_stroke + p.wire_preload * ease(preload_phase)


def rod_center(name: RodName, angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> PointYZ:
    locked = p.locked_centres[name]
    guide = GUIDE_DIRECTIONS[name]
    remaining = p.common_stroke - common_travel(angle_deg, p)
    return PointYZ(locked.y - guide.y * remaining, locked.z - guide.z * remaining)


def _point_segment_distance(point: PointYZ, first: PointYZ, second: PointYZ) -> float:
    """Exact Euclidean distance from one YZ point to a closed segment."""

    dy = second.y - first.y
    dz = second.z - first.z
    denominator = dy * dy + dz * dz
    if denominator <= 0.0:
        return point.distance_to(first)
    parameter = max(
        0.0,
        min(
            1.0,
            ((point.y - first.y) * dy + (point.z - first.z) * dz)
            / denominator,
        ),
    )
    projection = PointYZ(first.y + parameter * dy, first.z + parameter * dz)
    return point.distance_to(projection)


def _inverse_right_fixed_roll_point(
    point: PointYZ, alpha_deg: float, p: P13Parameters
) -> PointYZ:
    """Express a world-fixed point in a right-fixed plate rolled by alpha."""

    dy = point.y - p.shaft_y
    dz = point.z - p.shaft_z
    angle = radians(-alpha_deg)
    return PointYZ(
        p.shaft_y + cos(angle) * dy - sin(angle) * dz,
        p.shaft_z + sin(angle) * dy + cos(angle) * dz,
    )


def _engaged_roll_endpoint_constraints(
    p: P13Parameters,
) -> tuple[tuple[str, str, PointYZ, PointYZ, PointYZ, float], ...]:
    """Finite exact reduction of the continuous-theta intended-lane predicate.

    Rod centre motion is an affine traversal of the fixed straight lane because
    smoothstep is continuous, monotone, and surjective on [0,1].  Distance to a
    convex segment after a rigid rotation is convex in that affine parameter;
    therefore its maximum over every theta in OPEN..LOCKED occurs at an endpoint.
    """

    rows: list[tuple[str, str, PointYZ, PointYZ, PointYZ, float]] = []
    for name in ROD_NAMES:
        opened = rod_center(name, p.open_angle_deg, p)
        locked = rod_center(name, p.locked_angle_deg, p)
        for endpoint_name, endpoint in (("OPEN", opened), ("LOCKED", locked)):
            radius = hypot(endpoint.y - p.shaft_y, endpoint.z - p.shaft_z)
            rows.append((name, endpoint_name, endpoint, opened, locked, radius))
    return tuple(rows)


def _engaged_roll_residuals(
    alpha_deg: float, p: P13Parameters
) -> dict[str, float]:
    allowance = (p.lane_width - p.rod_diameter) / 2.0
    return {
        f"{name}:{endpoint_name}": _point_segment_distance(
            _inverse_right_fixed_roll_point(endpoint, alpha_deg, p),
            opened,
            locked,
        )
        - allowance
        for name, endpoint_name, endpoint, opened, locked, _radius
        in _engaged_roll_endpoint_constraints(p)
    }


def right_fixed_engaged_roll_is_exact_lane_valid(
    alpha_deg: float, p: P13Parameters = P13_DEFAULTS
) -> bool:
    normalized = alpha_deg % 360.0
    return max(_engaged_roll_residuals(normalized, p).values()) <= 0.0


def _merge_classified_intervals(
    intervals: list[tuple[float, float]], tolerance: float = 1.0e-12
) -> list[list[float]]:
    merged: list[list[float]] = []
    for lower, upper in sorted(intervals):
        if merged and lower <= merged[-1][1] + tolerance:
            merged[-1][1] = max(merged[-1][1], upper)
        else:
            merged.append([lower, upper])
    return merged


def right_fixed_engaged_roll_classification(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Certified global classification of intended-lane validity over S1.

    Samples are not used.  For an angular interval of half-width h radians,
    rigid rotation moves each endpoint by at most radius*h.  This Lipschitz
    enclosure certifies a whole interval valid or invalid; only two boundary
    brackets are left at the named angular resolution.
    """

    allowance = (p.lane_width - p.rod_diameter) / 2.0
    constraints = _engaged_roll_endpoint_constraints(p)
    pending: list[tuple[float, float]] = [P13_FULL_ROLL_DOMAIN_DEG]
    classified: dict[str, list[tuple[float, float]]] = {
        "valid": [],
        "invalid": [],
        "boundary": [],
    }
    while pending:
        lower, upper = pending.pop()
        centre = (lower + upper) / 2.0
        half_width_rad = radians((upper - lower) / 2.0)
        residual_bounds: list[tuple[float, float]] = []
        for _name, _endpoint_name, endpoint, opened, locked, radius in constraints:
            distance = _point_segment_distance(
                _inverse_right_fixed_roll_point(endpoint, centre, p),
                opened,
                locked,
            )
            residual_bounds.append(
                (distance - radius * half_width_rad - allowance,
                 distance + radius * half_width_rad - allowance)
            )
        if all(upper_bound <= 0.0 for _lower_bound, upper_bound in residual_bounds):
            classified["valid"].append((lower, upper))
        elif any(lower_bound > 0.0 for lower_bound, _upper_bound in residual_bounds):
            classified["invalid"].append((lower, upper))
        elif upper - lower <= P13_ENGAGED_ROLL_CLASSIFICATION_TOLERANCE_DEG:
            classified["boundary"].append((lower, upper))
        else:
            midpoint = (lower + upper) / 2.0
            pending.extend(((lower, midpoint), (midpoint, upper)))

    valid = _merge_classified_intervals(classified["valid"])
    invalid = _merge_classified_intervals(classified["invalid"])
    boundary = _merge_classified_intervals(classified["boundary"])
    if len(boundary) != 2 or not valid or not invalid:
        raise ValueError("right-fixed engaged-roll S1 classification is not one seam component")
    if valid[0][0] != 0.0 or valid[-1][1] != 360.0:
        raise ValueError("right-fixed alpha0 component does not close through the S1 seam")
    if not right_fixed_engaged_roll_is_exact_lane_valid(P13_RIGHT_FIXED_ALPHA0_DEG, p):
        raise ValueError("right-fixed alpha0 is not exact-lane-valid")

    max_residual_alpha0 = max(_engaged_roll_residuals(0.0, p).values())
    boundary_residual_enclosures = []
    for lower, upper in boundary:
        centre = (lower + upper) / 2.0
        half_width_rad = radians((upper - lower) / 2.0)
        constraint_bounds = {}
        for name, endpoint_name, endpoint, opened, locked, radius in constraints:
            distance = _point_segment_distance(
                _inverse_right_fixed_roll_point(endpoint, centre, p),
                opened,
                locked,
            )
            constraint_bounds[f"{name}:{endpoint_name}"] = {
                "lower": distance - radius * half_width_rad - allowance,
                "upper": distance + radius * half_width_rad - allowance,
            }
        boundary_residual_enclosures.append(
            {
                "interval": {"unit": "degree", "value": [lower, upper]},
                "maximumResidualEnclosure": {
                    "unit": "millimetre",
                    "lower": max(row["lower"] for row in constraint_bounds.values()),
                    "upper": max(row["upper"] for row in constraint_bounds.values()),
                },
                "constraintResidualEnclosures": {
                    "unit": "millimetre",
                    "value": constraint_bounds,
                },
            }
        )
    return {
        "proofMethod": "endpoint-convex reduction plus Lipschitz interval branch-and-bound",
        "thetaDomain": {"unit": "degree", "value": [p.open_angle_deg, p.locked_angle_deg]},
        "rollDomain": {"unit": "degree", "value": list(P13_FULL_ROLL_DOMAIN_DEG)},
        "seamIdentification": "0 degree == 360 degree",
        "laneRadialAllowance": {"unit": "millimetre", "value": allowance},
        "classificationTolerance": {
            "unit": "degree",
            "value": P13_ENGAGED_ROLL_CLASSIFICATION_TOLERANCE_DEG,
        },
        "certifiedValidInnerIntervals": {"unit": "degree", "value": valid},
        "certifiedInvalidIntervals": {"unit": "degree", "value": invalid},
        "boundaryBrackets": {"unit": "degree", "value": boundary},
        "boundaryResidualEnclosures": boundary_residual_enclosures,
        "components": [
            {
                "id": "alpha0-seam",
                "reachableFromAlpha0": True,
                "innerIntervals": [valid[0], valid[-1]],
                "boundaryBrackets": boundary,
            }
        ],
        "nonAlpha0Components": [],
        "alpha0MaximumResidual": {"unit": "millimetre", "value": max_residual_alpha0},
        "continuousAlpha0PathForAllTheta": max_residual_alpha0 <= 0.0,
        "samplesUsedForProof": False,
    }


def right_fixed_roll_stage_union(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Stage-correlated Domain-A union for right-fixed roll admissibility."""

    u_clear = p.right_fixed_rod_clearance_withdrawal
    u_full = p.rod_withdrawal_distance
    component = right_fixed_engaged_roll_classification(p)
    full_roll = {"unit": "degree", "value": list(P13_FULL_ROLL_DOMAIN_DEG)}
    alpha0_component = {
        "componentId": "alpha0-seam",
        "certificatePath": "rightFixedRollCertificate.engagedComponent",
        "exactPredicateRequired": True,
    }
    return {
        "schema": "P13RightFixedRollStageUnion/v1",
        "projection": {
            "variable": "right_fixed_roll",
            "unit": "degree",
            "value": list(P13_FULL_ROLL_DOMAIN_DEG),
            "completeS1": True,
        },
        "admissibility": "stage-correlated union; never a Cartesian-independent S1 while any rod journal relation J_i is true",
        "supportGuard": {
            "variable": "u_clear",
            "unit": "millimetre",
            "value": u_clear,
            "relation": "all J_i are false iff rod_right_tip_X <= right_fixed_BREP_min_X",
        },
        "stages": {
            "D0-operate": {
                "theta": {"unit": "degree", "value": [p.open_angle_deg, p.locked_angle_deg]},
                "withdrawalU": {"unit": "millimetre", "value": [0.0, 0.0]},
                "caps": "installed",
                "rodJournalRelations": "J_upright=J_bottom=J_diagonal=true",
                "rightFixedRoll": alpha0_component,
            },
            "D1-caps-off": {
                "theta": {"unit": "degree", "value": [p.open_angle_deg, p.locked_angle_deg]},
                "withdrawalU": {"unit": "millimetre", "value": [0.0, 0.0]},
                "caps": "right-caps-removed",
                "rodJournalRelations": "J_upright=J_bottom=J_diagonal=true",
                "rightFixedRoll": alpha0_component,
            },
            "D2-engaged-withdrawal": {
                "theta": {"unit": "degree", "value": [p.open_angle_deg, p.locked_angle_deg]},
                "withdrawalU": {"unit": "millimetre", "lowerOpen": 0.0, "upperOpen": u_clear},
                "rodJournalRelations": "J_upright=J_bottom=J_diagonal=true",
                "rightFixedRoll": alpha0_component,
            },
            "D3-rods-clear": {
                "withdrawalU": {"unit": "millimetre", "value": [u_clear, u_full]},
                "rodJournalRelations": "J_upright=J_bottom=J_diagonal=false",
                "rightFixedRoll": full_roll,
            },
            "D4-workpiece-lift": {
                "rodJournalRelations": "all J_i=false",
                "rightFixedRoll": full_roll,
                "requires": "full-S1 right-fixed rotational envelope plus complete-workpiece +Z certificate",
            },
            "D5-empty-service-prealign": {
                "workpiece": "removed-or-clear",
                "rodJournalRelations": "all J_i=false",
                "rightFixedRoll": full_roll,
            },
            "D6-keeper-off-release": {
                "keeper": "removed",
                "motion": "right-fixed minus-Z service release",
                "rightFixedRoll": {"unit": "degree", "value": [P13_RIGHT_FIXED_ALPHA0_DEG, P13_RIGHT_FIXED_ALPHA0_DEG]},
                "mouth": "up",
            },
        },
        "engagedComponentSummary": {
            "componentIds": [row["id"] for row in component["components"]],
            "nonAlpha0Components": component["nonAlpha0Components"],
            "seamIdentification": component["seamIdentification"],
        },
    }


def validate_right_fixed_roll_stage_union(
    candidate: dict[str, object], p: P13Parameters = P13_DEFAULTS
) -> None:
    expected = right_fixed_roll_stage_union(p)
    if candidate != expected:
        raise ValueError(
            "right-fixed-roll Domain-A must be the complete staged correlated union; independent-S1 or omitted stages are forbidden"
        )


def validate_right_fixed_roll_state(
    stage: str,
    *,
    theta_deg: float,
    withdrawal_u: float,
    alpha_deg: float,
    rod_journal_relations: tuple[bool, bool, bool],
    keeper_installed: bool = True,
    component_id: str = "alpha0-seam",
    all_roll_lift_certificate_present: bool = True,
    p: P13Parameters = P13_DEFAULTS,
) -> None:
    """Executable fail-closed predicate for one staged right-fixed-roll state."""

    if stage not in right_fixed_roll_stage_union(p)["stages"]:
        raise ValueError(f"unknown right-fixed-roll stage: {stage}")
    if not p.open_angle_deg <= theta_deg <= p.locked_angle_deg:
        raise ValueError("theta outside OPEN..LOCKED")
    if not 0.0 <= withdrawal_u <= p.rod_withdrawal_distance:
        raise ValueError("withdrawal u outside source domain")
    normalized_alpha = alpha_deg % 360.0
    guard = p.right_fixed_rod_clearance_withdrawal
    expected_journaled = withdrawal_u < guard
    if any(value != expected_journaled for value in rod_journal_relations):
        raise ValueError("rod journal relation disagrees with exact support guard")

    if stage in {"D0-operate", "D1-caps-off", "D2-engaged-withdrawal"}:
        if component_id != "alpha0-seam":
            raise ValueError("engaged right-fixed roll cannot jump components")
        if not expected_journaled:
            raise ValueError("engaged stage selected after exact rod-clear guard")
        if not right_fixed_engaged_roll_is_exact_lane_valid(normalized_alpha, p):
            raise ValueError("engaged right-fixed roll is outside exact alpha0 lane component")
        if stage in {"D0-operate", "D1-caps-off"} and withdrawal_u != 0.0:
            raise ValueError("D0/D1 require u=0")
        if stage == "D2-engaged-withdrawal" and not 0.0 < withdrawal_u < guard:
            raise ValueError("D2 requires 0<u<u_clear")
    elif stage == "D3-rods-clear":
        if withdrawal_u < guard:
            raise ValueError("arbitrary right-fixed roll forbidden below rod-clear guard")
    elif stage == "D4-workpiece-lift":
        if withdrawal_u < guard:
            raise ValueError("workpiece lift requires all rods clear")
        if not all_roll_lift_certificate_present:
            raise ValueError("D4 omits mandatory all-roll lift certificate")
    elif stage == "D5-empty-service-prealign":
        if withdrawal_u < guard:
            raise ValueError("service prealign requires all rods clear")
    elif stage == "D6-keeper-off-release":
        if keeper_installed:
            raise ValueError("D6 requires keeper removed")
        if abs(normalized_alpha - P13_RIGHT_FIXED_ALPHA0_DEG) > 1.0e-12:
            raise ValueError("D6 requires alpha=0 mouth-up")


def inverse_cam_point(name: RodName, angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> PointYZ:
    point = rod_center(name, angle_deg, p)
    dy, dz = point.y - p.shaft_y, point.z - p.shaft_z
    a = radians(angle_deg)
    return PointYZ(
        p.shaft_y + cos(a) * dy + sin(a) * dz,
        p.shaft_z - sin(a) * dy + cos(a) * dz,
    )


def inverse_cam_path(
    name: RodName,
    p: P13Parameters = P13_DEFAULTS,
) -> tuple[PointYZ, ...]:
    return tuple(inverse_cam_point(name, angle, p) for angle in cam_path_angles_deg(p))


def cam_path_angles_deg(p: P13Parameters = P13_DEFAULTS) -> tuple[float, ...]:
    """Polygon knots with the C1 contact/preload junction as an exact endpoint.

    The inverse cam curve is C2 on each side of ``rise_end_deg``.  Including
    that junction explicitly is what makes the per-chord curvature bound below
    a continuous-domain certificate rather than an assumption about samples.
    """

    angles: list[float] = []
    domains = (
        (p.open_angle_deg, p.rise_end_deg),
        (p.rise_end_deg, p.locked_angle_deg),
    )
    for domain_index, (start, end) in enumerate(domains):
        interval_count = max(1, ceil((end - start) / p.cam_path_step_deg))
        domain_angles = [
            start + (end - start) * index / interval_count
            for index in range(interval_count + 1)
        ]
        angles.extend(domain_angles if domain_index == 0 else domain_angles[1:])
    return tuple(angles)


def continuous_motion_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Certified global rod-in-lane bound over the complete rotary domain.

    Fixed-guide centres lie exactly on their straight capsule centrelines
    because smoothstep travel is monotone.  In each rotating cam frame, the
    exact inverse centre curve ``q(theta)`` is approximated by the polygon used
    by the cutter.  For every cutter interval the classical linear-chord bound
    is ``max(||q''||) * h^2 / 8``.  The reported second-derivative bound follows
    from ``q=R(-theta)d`` and the triangle inequality:

    ``||q''|| <= ||d|| + 2||d'|| + ||d''||``.

    The first smoothstep closes OPEN to first tangency and the second supplies
    the explicit wire-preload stroke.  Each piece supplies bounds
    ``|s'|<=1.5A/theta`` and ``|s''|<=6A/theta^2`` for its own amplitude and
    angular interval. Thus this is a continuous full-domain certificate, not
    an angle sample.
    """

    theta_contact = radians(p.rise_end_deg - p.open_angle_deg)
    theta_preload = radians(p.locked_angle_deg - p.rise_end_deg)
    if min(theta_contact, theta_preload) <= 0.0:
        raise ValueError("continuous motion certificate requires positive contact and preload intervals")
    knot_angles = cam_path_angles_deg(p)
    h = max(
        radians(second - first)
        for first, second in zip(knot_angles, knot_angles[1:])
    )
    max_s_prime = max(
        1.5 * p.contact_stroke / theta_contact,
        1.5 * p.wire_preload / theta_preload,
    )
    max_s_second = max(
        6.0 * p.contact_stroke / (theta_contact * theta_contact),
        6.0 * p.wire_preload / (theta_preload * theta_preload),
    )
    radial_allowance = (p.lane_width - p.rod_diameter) / 2.0
    rods: dict[str, object] = {}
    for name in ROD_NAMES:
        locked = p.locked_centres[name]
        opened = rod_center(name, p.open_angle_deg, p)
        max_d = max(
            hypot(opened.y - p.shaft_y, opened.z - p.shaft_z),
            hypot(locked.y - p.shaft_y, locked.z - p.shaft_z),
        )
        rise_second_derivative_bound = max_d + 2.0 * max_s_prime + max_s_second
        rigid_rotation_second_derivative_bound = hypot(
            locked.y - p.shaft_y, locked.z - p.shaft_z
        )
        global_second_derivative_bound = max(
            rise_second_derivative_bound, rigid_rotation_second_derivative_bound
        )
        chord_error_bound = global_second_derivative_bound * h * h / 8.0
        cam_margin = radial_allowance - chord_error_bound
        path_radius = max(
            hypot(opened.y - p.shaft_y, opened.z - p.shaft_z),
            hypot(locked.y - p.shaft_y, locked.z - p.shaft_z),
        )
        nominal_rim_margin = p.plate_diameter / 2.0 - path_radius - p.lane_width / 2.0
        tolerance_rim_margin = nominal_rim_margin - p.follower_error
        if min(radial_allowance, cam_margin, tolerance_rim_margin) <= 0.0:
            raise ValueError(f"nonpositive continuous lane margin for {name}")
        rods[name] = {
            "fixedCentreResidualBound": {"unit": "millimetre", "value": 0.0},
            "camInverseSecondDerivativeBound": {
                "unit": "millimetre_per_radian_squared",
                "value": global_second_derivative_bound,
            },
            "camChordErrorBound": {"unit": "millimetre", "value": chord_error_bound},
            "fixedRadialMargin": {"unit": "millimetre", "value": radial_allowance},
            "camRadialMargin": {
                "unit": "millimetre",
                "value": cam_margin,
            },
            "nominalRimMargin": {
                "unit": "millimetre",
                "value": nominal_rim_margin,
            },
            "profileAllowanceRimMargin": {
                "unit": "millimetre",
                "value": tolerance_rim_margin,
            },
        }
    axial_reach_margin = p.rod_length / 2.0 - max(
        abs(p.cam_left_outer_x), abs(p.cam_right_outer_x)
    )
    return {
        "proof": "global-analytic-piecewise-C2-chord-bound",
        "domainThetaDegrees": {
            "unit": "degree",
            "value": [p.open_angle_deg, p.locked_angle_deg],
        },
        "contactThetaDegrees": {
            "unit": "degree",
            "value": [p.open_angle_deg, p.rise_end_deg],
        },
        "preloadThetaDegrees": {
            "unit": "degree",
            "value": [p.rise_end_deg, p.locked_angle_deg],
        },
        "maximumCutterInterval": {"unit": "radian", "value": h},
        "polygonKnotAnglesDegrees": {
            "unit": "degree",
            "value": list(knot_angles),
        },
        "smoothstepMonotone": True,
        "rodAxialReachMargin": {"unit": "millimetre", "value": axial_reach_margin},
        "rods": rods,
    }


def rod_left_cap_withdrawal_certificate(
    p: P13Parameters = P13_DEFAULTS,
    domain: dict[str, object] | None = None,
) -> dict[str, object]:
    """Analytic dimensions for the full Domain-A left-cap engagement union."""

    source_domain = cad_source_removal_domain(p) if domain is None else domain
    engagement_lower, engagement_upper = _engagement_interval(
        source_domain, "left_cap_engagement_each"
    )
    start_cap_min_x = -p.rod_length / 2.0 + engagement_lower - p.cap_length
    start_cap_max_x = -p.rod_length / 2.0 + engagement_upper
    endpoint_rightmost_x = p.rod_length / 2.0 - p.rod_withdrawal_distance
    target_rightmost_x = p.left_cam_slab_min_x - p.rod_exit_clearance
    return {
        "proof": "continuous-range-expanded-conservative-swept-BREP-complete-rod-left-cap-units",
        "engagementDomain": {
            "unit": "millimetre",
            "value": [engagement_lower, engagement_upper],
            "source": "Domain-A.variables.left_cap_engagement_each.bounds",
        },
        "domainLambda": {"unit": "dimensionless", "value": [0.0, 1.0]},
        "translationX": {
            "unit": "millimetre",
            "value": [-p.rod_withdrawal_distance, 0.0],
        },
        "rodSweepEnvelopeLength": {
            "unit": "millimetre",
            "value": p.rod_length + p.rod_withdrawal_distance,
        },
        "leftCapSweepEnvelopeLength": {
            "unit": "millimetre",
            "value": (
                p.cap_length
                + p.rod_withdrawal_distance
                + engagement_upper
                - engagement_lower
            ),
        },
        "leftCapStartExtentX": {
            "unit": "millimetre",
            "value": [start_cap_min_x, start_cap_max_x],
        },
        "endpointRightmostX": {"unit": "millimetre", "value": endpoint_rightmost_x},
        "targetRightmostX": {"unit": "millimetre", "value": target_rightmost_x},
        "endpointExitMargin": {
            "unit": "millimetre",
            "value": target_rightmost_x - endpoint_rightmost_x + p.rod_exit_clearance,
        },
    }


def _distance_to_interval(value: float, lower: float, upper: float) -> float:
    if value < lower:
        return lower - value
    if value > upper:
        return value - upper
    return 0.0


def workpiece_plus_z_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Certified global bound for the complete rigid +Z removal sweep.

    Every principal plate slab, cam hub, shaft head and keeper is excluded by axial
    separation from the complete workpiece X envelope.  The only structure in
    that X envelope is the separate D shaft.  Exact centreline/primitive
    distance bounds are evaluated at lift zero; all relevant primitive centres
    begin above the shaft centre, so every bound is nondecreasing for the full
    commanded +Z interval.
    """

    source_certificate = cad_source_global_removal_certificate(p)
    removal_command = source_certificate["globalRemovalCommand"]["value"]
    workpiece_half_x = max(
        p.xt60_x / 2.0,
        p.wire_x + p.wire_radius,
        p.wire_x + p.stripped_diameter / 2.0,
        p.wire_x + p.solder_radius,
        p.wire_x + p.cup_diameter / 2.0,
    )
    fixed_inner_x = p.fixed_right_x - p.fixed_thickness / 2.0
    plate_axial_margin = fixed_inner_x - workpiece_half_x
    keeper_max_x = p.keeper_groove_x + p.keeper_thickness / 2.0
    keeper_axial_margin = -workpiece_half_x - keeper_max_x

    shaft_r = p.shaft_radius
    wire_r = p.wire_radius
    bend_centre_distance = hypot(
        p.bend_center_y - p.shaft_y, p.bend_center_z - p.shaft_z
    )
    shaft_to_bend_angle = degrees(
        atan2(p.shaft_z - p.bend_center_z, p.shaft_y - p.bend_center_y)
    )
    arc_lower = min(
        p.bend_arc_start_deg, p.bend_arc_start_deg + p.bend_arc_sweep_deg
    )
    arc_upper = max(
        p.bend_arc_start_deg, p.bend_arc_start_deg + p.bend_arc_sweep_deg
    )
    arc_alignment_inside = arc_lower <= shaft_to_bend_angle <= arc_upper
    if not arc_alignment_inside:
        raise ValueError("shaft-to-bend radial alignment must remain inside the exact bend arc")

    margins = {
        "plateAxial": plate_axial_margin,
        "keeperAxial": keeper_axial_margin,
        "wireHorizontalToShaft": hypot(
            p.bend_center_y - p.shaft_y, p.horizontal_z - p.shaft_z
        )
        - shaft_r
        - wire_r,
        "wireArcToShaft": bend_centre_distance - p.bend_radius - shaft_r - wire_r,
        "wireVerticalToShaft": hypot(
            -p.shaft_y, p.bend_center_z - p.shaft_z
        )
        - shaft_r
        - wire_r,
        "strippedConductorToShaft": hypot(
            p.stripped_y0 - p.shaft_y, p.horizontal_z - p.shaft_z
        )
        - shaft_r
        - p.stripped_diameter / 2.0,
        "solderSphereToShaft": hypot(
            p.pad_y0 - p.shaft_y, p.horizontal_z - p.shaft_z
        )
        - shaft_r
        - p.solder_radius,
        "cupToShaft": hypot(-p.shaft_y, p.cup_z0 - p.shaft_z)
        - shaft_r
        - p.cup_diameter / 2.0,
        "xt60BodyToShaft": hypot(
            _distance_to_interval(p.shaft_y, -p.xt60_y / 2.0, p.xt60_y / 2.0),
            _distance_to_interval(p.shaft_z, p.xt60_body_z0, p.xt60_body_z1),
        )
        - shaft_r,
    }
    return {
        "proof": "certified-global-analytic-primitive-decomposition",
        "domainLift": {"unit": "millimetre", "value": [0.0, removal_command]},
        "commandSource": "P13CADSourceRemovalCertificate/v1.globalRemovalCommand",
        "workpieceHalfX": {"unit": "millimetre", "value": workpiece_half_x},
        "shaftToBendAngle": {"unit": "degree", "value": shaft_to_bend_angle},
        "bendArcAngleDomain": {"unit": "degree", "value": [arc_lower, arc_upper]},
        "arcRadialAlignmentInsideDomain": arc_alignment_inside,
        "plusZClearanceMonotone": min(
            p.horizontal_z,
            p.bend_center_z,
            p.cup_z0,
            p.xt60_body_z0,
        )
        > p.shaft_z,
        "margins": {
            name: {"unit": "millimetre", "value": value}
            for name, value in margins.items()
        },
        "globalMargin": {"unit": "millimetre", "value": min(margins.values())},
    }


def _straight_slot_x(first: PointYZ, second: PointYZ, width: float, x: float, depth: float) -> Shape:
    dy, dz = second.y - first.y, second.z - first.z
    length = hypot(dy, dz)
    angle = degrees(atan2(dz, dy))
    bar = Pos(x, (first.y + second.y) / 2.0, (first.z + second.z) / 2.0) * Rot(
        angle, 0.0, 0.0
    ) * Box(depth, length, width, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    return _fuse(
        [
            bar,
            _x_cylinder(width, depth, x, first.y, first.z),
            _x_cylinder(width, depth, x, second.y, second.z),
        ]
    )


def _slot_solid_x(points: tuple[PointYZ, ...], width: float, x: float, depth: float) -> Shape:
    path = Wire.make_polygon([(0.0, point.y, point.z) for point in points])
    try:
        outline = path.offset_2d(width / 2.0, side=OffsetSide.BOTH, closed=True)
        return Pos(x, 0.0, 0.0) * extrude(Face(outline), depth / 2.0, both=True)
    except ValueError:
        return _fuse(
            [
                _straight_slot_x(first, second, width, x, depth)
                for first, second in zip(points, points[1:])
            ]
        )


def _plate_blank(x: float, thickness: float, p: P13Parameters) -> Shape:
    return _x_cylinder(p.plate_diameter, thickness, x, p.shaft_y, p.shaft_z)


def _d_prism_x(
    od: float,
    across_flat: float,
    depth: float,
    x: float,
    p: P13Parameters,
) -> Shape:
    """Return a single-D prism on the shaft axis with its flat facing -Z.

    ``across_flat`` is the total distance from the lower flat to the opposite
    circular extreme.  This definition gives the printed shaft and both cam
    bores one unambiguous legal phase and a common coplanar print datum.
    """

    radius = od / 2.0
    flat_offset = across_flat - radius
    if not 0.0 < flat_offset < radius:
        raise ValueError("D across-flat must place one flat inside the round OD")
    cylinder = _x_cylinder(od, depth, x, p.shaft_y, p.shaft_z)
    keeper = _box(
        (x, p.shaft_y, p.shaft_z + (radius - flat_offset) / 2.0),
        (
            depth + p.boolean_axial_overcut,
            od + p.boolean_radial_margin,
            radius + flat_offset,
        ),
    )
    clipped = cylinder.intersect(keeper)
    return clipped if hasattr(clipped, "volume") else clipped.solids()[0]


def _cam_d_bore_cutter(x: float, depth: float, p: P13Parameters) -> Shape:
    return _d_prism_x(
        p.cam_d_bore_od,
        p.cam_d_bore_across_flat,
        depth,
        x,
        p,
    )


def d_shaft_one_sided_lash_deg(
    p: P13Parameters = P13_DEFAULTS,
) -> float:
    """Exact one-sided angular travel until a male D endpoint meets the bore flat.

    In the shaft cross-section, let ``a`` be the positive distance from the
    centre to the male flat, ``h`` its half-chord, and ``b`` the distance to
    the female flat.  After relative rotation ``phi`` the lower male endpoint
    has support ``a*cos(phi) + h*sin(phi)`` toward the female flat.  First
    contact therefore satisfies that expression equal to ``b``.  Expressing
    both angles with ``atan2`` avoids the earlier small-angle/radius shortcut,
    which understated the actual D-profile lash.
    """

    radius = p.shaft_od / 2.0
    male_flat_offset = p.shaft_d_across_flat - radius
    female_flat_offset = p.cam_d_bore_across_flat - p.cam_d_bore_od / 2.0
    male_half_chord = sqrt(radius * radius - male_flat_offset * male_flat_offset)
    if not male_flat_offset < female_flat_offset < radius:
        raise ValueError("D bore flat must be outside the shaft flat and inside its OD")
    male_endpoint_angle = atan2(male_half_chord, male_flat_offset)
    female_contact_angle = atan2(
        sqrt(radius * radius - female_flat_offset * female_flat_offset),
        female_flat_offset,
    )
    return degrees(male_endpoint_angle - female_contact_angle)


def _fixed_cutter(x: float, depth: float, p: P13Parameters) -> Shape:
    local_zt = p.journal_intersection_z_local
    circle = _x_cylinder(p.fixed_groove_od, depth, x, p.shaft_y, p.shaft_z)
    mouth = _box(
        (x, p.shaft_y, p.shaft_z + p.plate_diameter / 4.0),
        (depth, p.journal_throat, p.plate_diameter / 2.0),
    )
    reliefs = [
        _x_cylinder(
            p.journal_relief_diameter,
            depth,
            x,
            p.shaft_y + sign * p.journal_throat / 2.0,
            p.shaft_z + local_zt,
        )
        for sign in (-1.0, 1.0)
    ]
    full_disc = _x_cylinder(p.plate_diameter, depth, x, p.shaft_y, p.shaft_z)
    upper_box = _box(
        (x, p.shaft_y, p.shaft_z + p.plate_diameter / 2.0),
        (
            depth,
            p.plate_diameter + p.boolean_plate_overcut,
            2.0 * (p.plate_diameter / 2.0 - p.journal_z_tip_local),
        ),
    )
    top_cap = full_disc.intersect(upper_box)
    return _fuse([circle, mouth, *reliefs, top_cap])


def _fixed_lane_cutters(x: float, depth: float, p: P13Parameters) -> list[Shape]:
    return [
        _straight_slot_x(
            rod_center(name, 0.0, p),
            rod_center(name, p.locked_angle_deg, p),
            p.lane_width,
            x,
            depth,
        )
        for name in ROD_NAMES
    ]


@lru_cache(maxsize=8)
def _fixed_plate_prototype(side: Literal["left", "right"], p: P13Parameters) -> Shape:
    x = p.fixed_left_x if side == "left" else p.fixed_right_x
    depth = p.fixed_thickness
    blank = _plate_blank(x, depth, p)
    cutter = _fixed_cutter(x, depth + p.boolean_plate_overcut, p)
    plate = blank - [*_fixed_lane_cutters(x, depth + p.boolean_plate_overcut, p), cutter]

    land_x = (
        x - depth / 2.0 - p.fixed_thrust_land_height / 2.0
        if side == "left"
        else x + depth / 2.0 + p.fixed_thrust_land_height / 2.0
    )
    land = _x_cylinder(
        p.thrust_land_od,
        p.fixed_thrust_land_height,
        land_x,
        p.shaft_y,
        p.shaft_z,
    )
    land = land - [
        _fixed_cutter(land_x, p.fixed_thrust_land_height, p),
        # The extra 0.10 mm now projects beyond the fixed-journal groove and
        # therefore sees the rotating OD5.60 D shaft, not the OD4.60 journal
        # land.  Reuse the reviewed 5.70-mm running OD so the fixed thrust land
        # cannot intersect the shaft while the main C-journal stays ID4.80.
        _x_cylinder(
            p.cam_d_bore_od,
            p.fixed_thrust_land_height,
            land_x,
            p.shaft_y,
            p.shaft_z,
        ),
        *_fixed_lane_cutters(land_x, p.fixed_thrust_land_height, p),
    ]
    return plate + land


def build_fixed_plate(side: Literal["left", "right"], p: P13Parameters = P13_DEFAULTS) -> Shape:
    return _label(
        copy(_fixed_plate_prototype(side, p)),
        f"{side}_fixed_OD{_tag(p.plate_diameter)}_integral_upward_C_journal_ID{_tag(p.fixed_groove_od)}",
        "#1F6E49",
    )


def _cam_lane_cutters_at_width(
    x: float,
    depth: float,
    lane_width: float,
    p: P13Parameters,
) -> list[Shape]:
    """Return the per-rod banded cam cutters for an explicit diameter.

    Keeping the certified witness on the same band partition as the production
    cutter is essential: one offset of the complete upright path can
    self-overlap and select a different planar face even though every local
    production band is valid.
    """
    cutters: list[Shape] = []
    for name in ROD_NAMES:
        points = inverse_cam_path(name, p)
        # Short overlapping offset bands avoid the self-overlap failure of one
        # large inverse-path offset while preserving a single connected lane.
        band_point_count = p.cam_band_segment_count + 1
        bands = [
            _slot_solid_x(
                points[index : min(len(points), index + band_point_count)],
                lane_width,
                x,
                depth,
            )
            for index in range(0, len(points) - 1, p.cam_band_segment_count)
        ]
        cutters.append(_fuse(bands))
    return cutters


def _cam_lane_cutters(x: float, depth: float, p: P13Parameters) -> list[Shape]:
    return _cam_lane_cutters_at_width(x, depth, p.lane_width, p)


@lru_cache(maxsize=8)
def _left_cam_prototype(p: P13Parameters) -> Shape:
    x = p.cam_left_x
    depth = p.cam_thickness
    blank = _plate_blank(x, depth, p)
    hub_x = (
        p.cam_left_outer_x
        - p.cam_hub_extension / 2.0
        + p.boolean_axial_overcut / 2.0
    )
    hub = _x_cylinder(
        p.cam_hub_od,
        p.cam_hub_extension + p.boolean_axial_overcut,
        hub_x,
        p.shaft_y,
        p.shaft_z,
    )
    # Cam cutters use the exact slab depth.  In this OCC build, oversized
    # curved through-cutters can leave tool-side bounding faces on an otherwise
    # valid result; exact-depth cutters keep the exported stock envelope exact.
    bore_x = (p.left_cam_hub_outer_x + p.cam_left_x + depth / 2.0) / 2.0
    bore = _cam_d_bore_cutter(bore_x, p.cam_d_engagement, p)
    cam = _fuse([blank, hub]) - [*_cam_lane_cutters(x, depth, p), bore]

    if p.cam_thrust_land_height == 0.0:
        return cam
    land_x = x + depth / 2.0 + p.cam_thrust_land_height / 2.0
    land = _x_cylinder(
        p.thrust_land_od,
        p.cam_thrust_land_height,
        land_x,
        p.shaft_y,
        p.shaft_z,
    )
    land = land - [
        _cam_d_bore_cutter(land_x, p.cam_thrust_land_height, p),
        *_cam_lane_cutters(land_x, p.cam_thrust_land_height, p),
    ]
    return cam + land


def build_left_cam(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Shape:
    shape = _rotate_about_shaft(copy(_left_cam_prototype(p)), angle_deg, p)
    return _label(shape, f"left_D_bore_cam_OD{_tag(p.plate_diameter)}_theta_{_tag(angle_deg)}", "#D4A514")


def _groove_annulus(x: float, width: float, root_od: float, p: P13Parameters) -> Shape:
    outer = _x_cylinder(p.shaft_od + p.boolean_radial_margin, width, x, p.shaft_y, p.shaft_z)
    root = _x_cylinder(root_od, width + p.boolean_axial_overcut, x, p.shaft_y, p.shaft_z)
    return outer - root


@lru_cache(maxsize=8)
def _right_actuator_prototype(p: P13Parameters) -> Shape:
    x = p.cam_right_x
    blank = _plate_blank(x, p.cam_thickness, p)
    hub_x = (
        p.cam_right_outer_x
        + p.cam_hub_extension / 2.0
        - p.boolean_axial_overcut / 2.0
    )
    hub = _x_cylinder(
        p.cam_hub_od,
        p.cam_hub_extension + p.boolean_axial_overcut,
        hub_x,
        p.shaft_y,
        p.shaft_z,
    )
    bore_x = (p.cam_right_x - p.cam_thickness / 2.0 + p.right_cam_hub_outer_x) / 2.0
    bore = _cam_d_bore_cutter(bore_x, p.cam_d_engagement, p)
    cam = _fuse([blank, hub]) - [*_cam_lane_cutters(x, p.cam_thickness, p), bore]

    if p.cam_thrust_land_height == 0.0:
        return cam
    land_x = x - p.cam_thickness / 2.0 - p.cam_thrust_land_height / 2.0
    land = _x_cylinder(
        p.thrust_land_od,
        p.cam_thrust_land_height,
        land_x,
        p.shaft_y,
        p.shaft_z,
    )
    land = land - [
        _cam_d_bore_cutter(land_x, p.cam_thrust_land_height, p),
        *_cam_lane_cutters(land_x, p.cam_thrust_land_height, p),
    ]
    return cam + land


def build_right_actuator(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Shape:
    shape = _rotate_about_shaft(copy(_right_actuator_prototype(p)), angle_deg, p)
    return _label(
        shape,
        f"right_D_bore_cam_actuator_OD{_tag(p.plate_diameter)}_theta_{_tag(angle_deg)}",
        "#D4A514",
    )


@lru_cache(maxsize=8)
def _separate_shaft_prototype(p: P13Parameters) -> Shape:
    shaft_length = p.shaft_head_inner_x - p.shaft_x0
    shaft = _d_prism_x(
        p.shaft_od,
        p.shaft_d_across_flat,
        shaft_length,
        (p.shaft_x0 + p.shaft_head_inner_x) / 2.0,
        p,
    )
    # Restore truly round material at the two fixed-journal lands and at the
    # keeper groove before reducing each station to its declared diameter.
    shaft = _fuse(
        [
            shaft,
            _x_cylinder(
                p.journal_land_od,
                p.fixed_groove_width,
                p.fixed_left_x,
                p.shaft_y,
                p.shaft_z,
            ),
            _x_cylinder(
                p.journal_land_od,
                p.fixed_groove_width,
                p.fixed_right_x,
                p.shaft_y,
                p.shaft_z,
            ),
            _x_cylinder(
                p.keeper_groove_od,
                p.keeper_groove_width,
                p.keeper_groove_x,
                p.shaft_y,
                p.shaft_z,
            ),
        ]
    )
    shaft = shaft - [
        _groove_annulus(p.fixed_left_x, p.fixed_groove_width, p.journal_land_od, p),
        _groove_annulus(p.fixed_right_x, p.fixed_groove_width, p.journal_land_od, p),
        _groove_annulus(p.keeper_groove_x, p.keeper_groove_width, p.keeper_groove_od, p),
    ]
    shaft_flat_offset = p.shaft_d_across_flat - p.shaft_od / 2.0
    head_across_flat = p.shaft_head_od / 2.0 + shaft_flat_offset
    head = _d_prism_x(
        p.shaft_head_od,
        head_across_flat,
        p.shaft_head_thickness,
        (p.shaft_head_inner_x + p.shaft_head_outer_x) / 2.0,
        p,
    )
    return _fuse([shaft, head])


def build_actuator_shaft(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Shape:
    shape = _rotate_about_shaft(copy(_separate_shaft_prototype(p)), angle_deg, p)
    return _label(
        shape,
        f"separate_printed_D_shaft_OD{_tag(p.shaft_od)}_AF{_tag(p.shaft_d_across_flat)}_theta_{_tag(angle_deg)}",
        "#C48720",
    )


def build_principal_plates(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_left_cam(angle_deg, p),
            build_fixed_plate("left", p),
            build_fixed_plate("right", p),
            build_right_actuator(angle_deg, p),
        ],
        label=f"exactly_four_visible_OD{_tag(p.plate_diameter)}_principal_plate_occurrences",
    )


def build_rod(name: RodName, angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, p)
    return _label(
        _x_cylinder(p.rod_diameter, p.rod_length, 0.0, point.y, point.z),
        f"purchased_uncut_304_{name}_rod_D{_tag(p.rod_diameter)}x{_tag(p.rod_length)}",
        "#BFC7CC",
    )


def build_rods(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[build_rod(name, angle_deg, p) for name in ROD_NAMES],
        label=f"exactly_three_purchased_uncut_D{_tag(p.rod_diameter)}x{_tag(p.rod_length)}_rods",
    )


def _keeper_cutter(x: float, depth: float, p: P13Parameters) -> Shape:
    inner = _x_cylinder(p.keeper_id, depth, x, p.shaft_y, p.shaft_z)
    mouth = _box(
        (x, p.shaft_y, p.shaft_z - p.keeper_od / 4.0),
        (depth, p.keeper_throat, p.keeper_od / 2.0),
    )
    local_zt = -sqrt((p.keeper_id / 2.0) ** 2 - (p.keeper_throat / 2.0) ** 2)
    reliefs = [
        _x_cylinder(
            p.keeper_relief_diameter,
            depth,
            x,
            p.shaft_y + sign * p.keeper_throat / 2.0,
            p.shaft_z + local_zt,
        )
        for sign in (-1.0, 1.0)
    ]
    outer = _x_cylinder(p.keeper_od, depth, x, p.shaft_y, p.shaft_z)
    lower = _box(
        (x, p.shaft_y, p.shaft_z - p.keeper_od / 2.0),
        (
            depth,
            p.keeper_od + p.boolean_radial_margin,
            2.0 * (p.keeper_z_tip_local + p.keeper_od / 2.0),
        ),
    )
    return _fuse([inner, mouth, *reliefs, outer.intersect(lower)])


@lru_cache(maxsize=8)
def _shaft_keeper_prototype(p: P13Parameters) -> Shape:
    outer = _x_cylinder(p.keeper_od, p.keeper_thickness, p.keeper_groove_x, p.shaft_y, p.shaft_z)
    return outer - _keeper_cutter(
        p.keeper_groove_x,
        p.keeper_thickness + 2.0 * p.boolean_axial_overcut,
        p,
    )


def build_shaft_keeper(p: P13Parameters = P13_DEFAULTS) -> Shape:
    return _label(
        copy(_shaft_keeper_prototype(p)),
        f"round_C_shaft_keeper_OD{_tag(p.keeper_od)}_ID{_tag(p.keeper_id)}",
        "#59626A",
    )


def _left_cap_local(p: P13Parameters) -> Shape:
    body = _x_cylinder(p.cap_od, p.cap_length, p.cap_length / 2.0, 0.0, 0.0)
    socket = _x_cylinder(
        p.left_cap_socket,
        p.left_cap_socket_depth + p.boolean_axial_overcut,
        p.left_cap_socket_depth / 2.0 - p.boolean_axial_overcut / 2.0,
        0.0,
        0.0,
    )
    return body - socket


def _right_cap_local(p: P13Parameters) -> Shape:
    expected_slit_z0 = (
        min(P16_CAP_DEFAULTS.throat_diameters) / 2.0
        - p.right_cap_functional_overcut
    )
    if abs(p.right_cap_slit_z0 - expected_slit_z0) > 1.0e-12:
        raise ValueError("right-cap slit root must match the accepted P16 functional core")
    if abs(p.right_cap_slit_z1 - p.cap_od / 2.0) > 1.0e-12:
        raise ValueError("right-cap slit outer radius must reach the OD7 body")

    p16_contract = replace(
        P16_CAP_DEFAULTS,
        cavity_diameter=p.right_cap_cavity,
        cap_outer_diameter=p.cap_od,
        cap_height=p.cap_length,
        closed_base_thickness=p.cap_length - p.right_cap_cavity_end,
        throat_depth=p.right_cap_throat_depth,
        slit_width=p.right_cap_slit_width,
        boolean_overshoot=p.right_cap_functional_overcut,
        minimum_radial_wall=p.right_cap_min_radial_wall,
    )
    p16_core = build_p16_functional_cap_core(p.right_cap_throat, p16_contract)
    # P16 prints on its closed Z face.  P13 uses +X from the open face toward
    # the floor, so rotate +90 degrees about Y and translate the closed face.
    return Rot(0.0, -90.0, 0.0) * Pos(0.0, 0.0, -p.cap_length) * p16_core


def build_left_cap(name: RodName, angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, p)
    open_x = -p.rod_length / 2.0 + p.nominal_cap_engagement
    shape = Pos(open_x, point.y, point.z) * Rot(0.0, 0.0, p.cap_reverse_rotation_deg) * copy(_left_cap_local(p))
    return _label(
        shape,
        f"permanent_round_left_blind_cap_{name}_socket_D{_tag(p.left_cap_socket)}",
        "#525A60",
    )


def build_right_cap(name: RodName, angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Shape:
    point = rod_center(name, angle_deg, p)
    open_x = p.rod_length / 2.0 - p.nominal_cap_engagement
    shape = Pos(open_x, point.y, point.z) * copy(_right_cap_local(p))
    return _label(
        shape,
        (
            f"removable_round_right_slit_print_fit_cap_{name}_"
            f"cavity_D{_tag(p.right_cap_cavity)}_throat_D{_tag(p.right_cap_throat)}"
        ),
        "#737C82",
    )


def build_retainers(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[
            build_shaft_keeper(p),
            *[build_left_cap(name, angle_deg, p) for name in ROD_NAMES],
            *[build_right_cap(name, angle_deg, p) for name in ROD_NAMES],
        ],
        label="one_round_shaft_keeper_and_six_round_rod_caps",
    )


def build_wire_centerline(x: float, p: P13Parameters = P13_DEFAULTS) -> Wire:
    with BuildLine(Plane.YZ) as path:
        Line((p.horizontal_start_y, p.horizontal_z), (p.bend_center_y, p.horizontal_z))
        CenterArc(
            (p.bend_center_y, p.bend_center_z),
            p.bend_radius,
            p.bend_arc_start_deg,
            p.bend_arc_sweep_deg,
        )
        Line((0.0, p.bend_center_z), (0.0, p.vertical_lead_z1))
    return Pos(x, 0.0, 0.0) * Wire(path.line.edges())


def build_wire(x: float, p: P13Parameters = P13_DEFAULTS, lift: float = 0.0) -> Shape:
    centerline = build_wire_centerline(x, p)
    start_plane = Plane(
        origin=(x, p.horizontal_start_y, p.horizontal_z),
        x_dir=(1, 0, 0),
        z_dir=(0, -1, 0),
    )
    with BuildSketch(start_plane) as profile:
        Circle(p.wire_diameter / 2.0)
    color = "#D64536" if x < 0 else "#17191C"
    wire = Pos(0.0, 0.0, lift) * sweep(profile.sketch, centerline)
    return _label(wire, f"nominal_12AWG_exact_90deg_lead_x{x:+g}_lift_{lift:g}", color)


def build_workpiece_constituents(
    p: P13Parameters = P13_DEFAULTS, lift: float = 0.0
) -> Compound:
    """Exact labeled primitives used to build the connected workpiece.

    SOLDER review artifacts use this diagnostic decomposition so the conductor,
    solder and cup remain visible.  Production workflow artifacts fuse these
    same primitives into one connected solid via :func:`build_workpiece`.
    """
    insulated = [build_wire(-p.wire_x, p, lift), build_wire(p.wire_x, p, lift)]
    conductors = [
        _label(
            Pos(x, p.stripped_y0, p.horizontal_z + lift)
            * Cylinder(
                p.stripped_diameter / 2.0,
                p.stripped_y1 - p.stripped_y0,
                rotation=(-90.0, 0.0, 0.0),
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ),
            f"exact_stripped_copper_x{x:+g}_lift_{_tag(lift)}",
            "#B87333",
        )
        for x in (-p.wire_x, p.wire_x)
    ]
    solder = [
        _label(
            Pos(x, p.pad_y0, p.horizontal_z + lift) * Sphere(p.solder_radius),
            f"exact_solder_sphere_x{x:+g}_lift_{_tag(lift)}",
            "#C0C7CE",
        )
        for x in (-p.wire_x, p.wire_x)
    ]
    cups = [
        _label(
            Pos(x, 0.0, p.cup_z0 + lift)
            * Cylinder(
                p.cup_diameter / 2.0,
                p.cup_z1 - p.cup_z0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ),
            f"exact_XT60_solder_cup_x{x:+g}_lift_{_tag(lift)}",
            "#D9A91A",
        )
        for x in (-p.wire_x, p.wire_x)
    ]
    body = _label(
        _box(
            (0.0, 0.0, (p.xt60_body_z0 + p.xt60_body_z1) / 2.0 + lift),
            (p.xt60_x, p.xt60_y, p.xt60_z),
        ),
        f"exact_XT60_body_lift_{_tag(lift)}",
        "#D9A91A",
    )
    return Compound(
        children=[*insulated, *conductors, *solder, *cups, body],
        label=f"diagnostic_exact_workpiece_constituents_lift_{_tag(lift)}",
    )


def build_workpiece(p: P13Parameters = P13_DEFAULTS, lift: float = 0.0) -> Compound:
    constituents = build_workpiece_constituents(p, lift)
    complete = _label(
        _fuse(list(constituents.children)),
        f"complete_connected_XT60_two_exact_90deg_leads_lift_{_tag(lift)}",
        "#D9A91A",
    )
    return Compound(
        children=[complete],
        label=f"nominal_complete_connected_XT60_90deg_workpiece_lift_{lift:g}",
    )


def build_electronics_reference(p: P13Parameters = P13_DEFAULTS) -> Compound:
    pads = [
        _label(
            _box(
                (x, (p.pad_y0 + p.pad_y1) / 2.0, p.horizontal_z),
                (p.pad_width_x, p.pad_y1 - p.pad_y0, p.pad_thickness_z),
            ),
            f"provisional_ESC_pad_x{x:+g}",
            "#C6A147",
        )
        for x in (-p.wire_x, p.wire_x)
    ]
    return Compound(children=pads, label="translucent_nonstructural_ESC_pad_references")


def build_solder_tool(x: float, p: P13Parameters = P13_DEFAULTS) -> Compound:
    joint = (x, p.pad_y0, p.horizontal_z)
    tip_local = Cone(
        p.iron_tip_r0,
        p.iron_tip_r1,
        p.iron_tip_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    barrel_local = Pos(0.0, 0.0, p.iron_tip_length) * Cylinder(
        p.iron_barrel_radius,
        p.iron_barrel_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    tip = Pos(*joint) * Rot(-p.iron_angle_deg, 0.0, 0.0) * tip_local
    barrel = Pos(*joint) * Rot(-p.iron_angle_deg, 0.0, 0.0) * barrel_local
    return Compound(
        children=[
            _label(tip, f"iron_frustum_target_x{x:+g}", "#8B9399"),
            _label(barrel, f"iron_barrel_target_x{x:+g}", "#596168"),
        ],
        label=f"provisional_outward_solder_iron_x{x:+g}",
    )


def build_core(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[
            *build_principal_plates(angle_deg, p).children,
            build_actuator_shaft(angle_deg, p),
            *build_rods(angle_deg, p).children,
            *build_retainers(angle_deg, p).children,
        ],
        label=f"P13_exploratory_nominal_core_theta_{angle_deg:g}",
    )


def build_four_plate_structure(
    angle_deg: float, p: P13Parameters = P13_DEFAULTS
) -> Compound:
    """The invariant assembled structure retained throughout normal removal."""
    return Compound(
        children=[
            *build_principal_plates(angle_deg, p).children,
            build_actuator_shaft(angle_deg, p),
            build_shaft_keeper(p),
        ],
        label=f"assembled_four_plates_separate_D_shaft_keeper_theta_{angle_deg:g}",
    )


def build_rod_left_cap_unit(
    name: RodName,
    angle_deg: float,
    p: P13Parameters = P13_DEFAULTS,
    shift_x: float = 0.0,
) -> Compound:
    return Compound(
        children=[
            Pos(shift_x, 0.0, 0.0) * build_rod(name, angle_deg, p),
            Pos(shift_x, 0.0, 0.0) * build_left_cap(name, angle_deg, p),
        ],
        label=f"permanent_{name}_rod_left_cap_subassembly_shiftX_{_tag(shift_x)}",
    )


def build_three_rod_left_cap_units(
    angle_deg: float,
    p: P13Parameters = P13_DEFAULTS,
    shift_x: float = 0.0,
) -> Compound:
    return Compound(
        children=[
            *[
                build_rod_left_cap_unit(name, angle_deg, p, shift_x)
                for name in ROD_NAMES
            ]
        ],
        label=f"synchronous_three_rod_left_cap_units_shiftX_{_tag(shift_x)}",
    )


def build_rod_left_cap_withdrawal_envelope(
    name: RodName,
    p: P13Parameters = P13_DEFAULTS,
    domain: dict[str, object] | None = None,
) -> Compound:
    """Conservative exact BREP cover of one complete continuous withdrawal.

    A coaxial cylinder extended by the full -X travel is the exact translative
    sweep of the purchased rod.  A second Ø``cap_od`` cylinder extended by the
    same travel contains the exact blind-cap sweep, including its socket void.
    Their union therefore contains every rigid rod/permanent-left-cap pose for
    all lambda in [0,1]; it deliberately does not reduce the proof to a bare
    rod.
    """

    source_domain = cad_source_removal_domain(p) if domain is None else domain
    engagement_lower, engagement_upper = _engagement_interval(
        source_domain, "left_cap_engagement_each"
    )
    point = rod_center(name, p.open_angle_deg, p)
    distance = p.rod_withdrawal_distance
    rod_envelope = _label(
        _x_cylinder(
            p.rod_diameter,
            p.rod_length + distance,
            -distance / 2.0,
            point.y,
            point.z,
        ),
        f"continuous_withdrawal_{name}_full_rod_envelope",
        "#BFC7CC",
    )
    cap_start_min_x = -p.rod_length / 2.0 + engagement_lower - p.cap_length
    cap_start_max_x = -p.rod_length / 2.0 + engagement_upper
    cap_sweep_min_x = cap_start_min_x - distance
    cap_envelope = _label(
        _x_cylinder(
            p.cap_od,
            cap_start_max_x - cap_sweep_min_x,
            (cap_start_max_x + cap_sweep_min_x) / 2.0,
            point.y,
            point.z,
        ),
        (
            f"continuous_withdrawal_{name}_permanent_left_cap_outer_envelope_"
            f"engagement_{_tag(engagement_lower)}_to_{_tag(engagement_upper)}"
        ),
        "#525A60",
    )
    return Compound(
        children=[rod_envelope, cap_envelope],
        label=f"certified_continuous_{name}_complete_rod_left_cap_withdrawal_envelope",
    )


def build_three_rod_left_cap_withdrawal_envelopes(
    p: P13Parameters = P13_DEFAULTS,
    domain: dict[str, object] | None = None,
) -> Compound:
    return Compound(
        children=[
            build_rod_left_cap_withdrawal_envelope(name, p, domain)
            for name in ROD_NAMES
        ],
        label="certified_continuous_three_complete_rod_left_cap_withdrawal_envelopes",
    )


def build_right_cap_stage1_envelope(
    name: RodName,
    p: P13Parameters = P13_DEFAULTS,
    domain: dict[str, object] | None = None,
) -> Shape:
    """Conservative right-cap removal cover over engagement, translation and S1.

    Every revolved outer point of the slit cap lies inside its ``cap_od`` body
    cylinder for every roll.  The X interval starts at the deepest permitted
    seated engagement and ends at the fully disengaged cap outer face.  This
    single cylinder therefore contains every Stage-1 pose for every engagement
    in Domain A, including arbitrary synchronous cap roll.
    """

    source_domain = cad_source_removal_domain(p) if domain is None else domain
    engagement_lower, engagement_upper = _engagement_interval(
        source_domain, "right_cap_engagement_each"
    )
    roll_lower, roll_upper = _roll_interval(source_domain, "right_cap_roll_each")
    point = rod_center(name, p.open_angle_deg, p)
    min_x = p.rod_length / 2.0 - engagement_upper
    max_x = p.rod_length / 2.0 + p.cap_length
    return _label(
        _x_cylinder(
            p.cap_od,
            max_x - min_x,
            (min_x + max_x) / 2.0,
            point.y,
            point.z,
        ),
        (
            f"continuous_stage1_{name}_right_cap_outer_envelope_"
            f"engagement_{_tag(engagement_lower)}_to_{_tag(engagement_upper)}_"
            f"roll_{_tag(roll_lower)}_to_{_tag(roll_upper)}"
        ),
        "#737C82",
    )


def build_three_right_cap_stage1_envelopes(
    p: P13Parameters = P13_DEFAULTS,
    domain: dict[str, object] | None = None,
) -> Compound:
    return Compound(
        children=[
            build_right_cap_stage1_envelope(name, p, domain) for name in ROD_NAMES
        ],
        label="certified_continuous_three_right_cap_stage1_envelopes",
    )


def build_rigid_frame(angle_deg: float, p: P13Parameters = P13_DEFAULTS) -> Compound:
    """Compatibility name for the invariant four-plate removal remainder."""
    return build_four_plate_structure(angle_deg, p)


def build_open(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[*build_core(p.open_angle_deg, p).children],
        label="P13_OPEN_empty_corridor_exploratory_nominal",
    )


def build_loaded(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[*build_core(p.open_angle_deg, p).children, *build_workpiece(p).children],
        label="P13_LOADED_full_connected_90deg_workpiece_exploratory_nominal",
    )


def build_set_close(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[*build_core(p.rise_end_deg, p).children, *build_workpiece(p).children],
        label="P13_SET_CLOSE_end_of_rise_full_workpiece_exploratory_nominal",
    )


def build_locked(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[*build_core(p.locked_angle_deg, p).children, *build_workpiece(p).children],
        label="P13_LOCKED_loaded_exact_90deg_exploratory_nominal",
    )


def build_release(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[*build_core(p.open_angle_deg, p).children, *build_workpiece(p).children],
        label="P13_RELEASE_OPEN_full_connected_90deg_workpiece_exploratory_nominal",
    )


def build_caps_off(p: P13Parameters = P13_DEFAULTS) -> Compound:
    removed_caps = [
        Pos(p.cap_removed_offset_x, 0.0, 0.0)
        * build_right_cap(name, p.open_angle_deg, p)
        for name in ROD_NAMES
    ]
    return Compound(
        children=[
            *build_four_plate_structure(p.open_angle_deg, p).children,
            *build_three_rod_left_cap_units(p.open_angle_deg, p).children,
            *removed_caps,
            *build_workpiece(p).children,
        ],
        label="P13_OPEN_three_right_caps_removed_structure_unchanged",
    )


def build_rods_withdrawn(p: P13Parameters = P13_DEFAULTS) -> Compound:
    removed_caps = [
        Pos(p.cap_removed_offset_x, 0.0, 0.0)
        * build_right_cap(name, p.open_angle_deg, p)
        for name in ROD_NAMES
    ]
    return Compound(
        children=[
            *build_four_plate_structure(p.open_angle_deg, p).children,
            *build_three_rod_left_cap_units(
                p.open_angle_deg, p, -p.rod_withdrawal_distance
            ).children,
            *removed_caps,
            *build_workpiece(p).children,
        ],
        label="P13_OPEN_caps_off_three_rod_left_cap_units_synchronously_withdrawn_minusX",
    )


def build_cool(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[*build_locked(p).children],
        label="P13_COOL_LOCKED_full_connected_90deg_workpiece_exploratory_nominal",
    )


def build_solder_left(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[
            *build_core(p.locked_angle_deg, p).children,
            *build_workpiece_constituents(p).children,
            *build_electronics_reference(p).children,
            *build_solder_tool(-p.wire_x, p).children,
        ],
        label="P13_SOLDER_left_exact_decomposed_joint_exploratory_nominal_tool_envelope",
    )


def build_solder_right(p: P13Parameters = P13_DEFAULTS) -> Compound:
    return Compound(
        children=[
            *build_core(p.locked_angle_deg, p).children,
            *build_workpiece_constituents(p).children,
            *build_electronics_reference(p).children,
            *build_solder_tool(p.wire_x, p).children,
        ],
        label="P13_SOLDER_right_exact_decomposed_joint_exploratory_nominal_tool_envelope",
    )


def continuous_lane_solid_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Check the analytic continuous lane witnesses against final plate solids.

    The cam witness is the actual cutter polygon expanded by the purchased-rod
    radius plus the certified curve-to-chord error.  The fixed witness is the
    exact straight centre segment expanded by the rod radius.  Zero witness /
    final-material overlap verifies that the Boolean result contains the
    analytic continuous tubes; the separate rim margin prevents an escaped
    outside-the-disc path from passing this check.
    """

    tolerance = continuous_overlap_tolerance(p)
    motion = continuous_motion_certificate(p)
    fixed_solids = {
        "left": build_fixed_plate("left", p),
        "right": build_fixed_plate("right", p),
    }
    cam_solids = {
        "left": build_left_cam(p.open_angle_deg, p),
        "right": build_right_actuator(p.open_angle_deg, p),
    }
    fixed_slabs = {
        "left": (
            (p.fixed_left_x, p.fixed_thickness),
            (
                p.fixed_left_x
                - p.fixed_thickness / 2.0
                - p.fixed_thrust_land_height / 2.0,
                p.fixed_thrust_land_height,
            ),
        ),
        "right": (
            (p.fixed_right_x, p.fixed_thickness),
            (
                p.fixed_right_x
                + p.fixed_thickness / 2.0
                + p.fixed_thrust_land_height / 2.0,
                p.fixed_thrust_land_height,
            ),
        ),
    }
    cam_slabs = {
        "left": ((p.cam_left_x, p.cam_thickness),)
        + (
            (
                p.cam_left_x
                + p.cam_thickness / 2.0
                + p.cam_thrust_land_height / 2.0,
                p.cam_thrust_land_height,
            ),
        )
        if p.cam_thrust_land_height > 0.0
        else ((p.cam_left_x, p.cam_thickness),),
        "right": ((p.cam_right_x, p.cam_thickness),)
        + (
            (
                p.cam_right_x
                - p.cam_thickness / 2.0
                - p.cam_thrust_land_height / 2.0,
                p.cam_thrust_land_height,
            ),
        )
        if p.cam_thrust_land_height > 0.0
        else ((p.cam_right_x, p.cam_thickness),),
    }
    rows: dict[str, object] = {}
    for name in ROD_NAMES:
        row = motion["rods"][name]
        fixed_width = p.rod_diameter
        cam_width = p.rod_diameter + 2.0 * row["camChordErrorBound"]["value"]
        fixed_overlaps = {
            side: [
                _intersection_volume(
                    _straight_slot_x(
                        rod_center(name, p.open_angle_deg, p),
                        rod_center(name, p.locked_angle_deg, p),
                        fixed_width,
                        slab_x,
                        slab_depth,
                    ),
                    fixed_solids[side],
                )
                for slab_x, slab_depth in fixed_slabs[side]
            ]
            for side in ("left", "right")
        }
        cam_index = ROD_NAMES.index(name)
        cam_overlaps = {
            side: [
                _intersection_volume(
                    _cam_lane_cutters_at_width(
                        slab_x,
                        slab_depth,
                        cam_width,
                        p,
                    )[cam_index],
                    cam_solids[side],
                )
                for slab_x, slab_depth in cam_slabs[side]
            ]
            for side in ("left", "right")
        }
        all_overlaps = [
            volume
            for overlap_group in (*fixed_overlaps.values(), *cam_overlaps.values())
            for volume in overlap_group
        ]
        maximum = max(all_overlaps)
        if maximum > tolerance:
            raise ValueError(f"continuous lane witness intersects final material for {name}: {maximum}")
        rows[name] = {
            "fixedWitnessDiameter": {"unit": "millimetre", "value": fixed_width},
            "camWitnessDiameter": {"unit": "millimetre", "value": cam_width},
            "fixedPlateIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": fixed_overlaps,
            },
            "camPlateIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": cam_overlaps,
            },
            "maximumIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": maximum,
            },
            "minimumProfileAllowanceRimMargin": row[
                "profileAllowanceRimMargin"
            ],
        }
    return {
        "proof": "continuous analytic tubes checked against actual final fixed/cam material",
        "overlapVolumeTolerance": {
            "unit": "cubic_millimetre",
            "value": tolerance,
        },
        "rows": rows,
    }


def build_right_fixed_full_roll_envelope(
    p: P13Parameters = P13_DEFAULTS,
) -> Shape:
    """Conservative exact-BREP cover of the right fixed plate over full S1.

    The OD blanks and the central circular journal are coaxial with the roll
    axis.  Removing only that persistent circular void from each OD blank and
    retaining every other possible angular material location covers the union
    of all rotations without relying on samples.
    """

    x = p.fixed_right_x
    main = _plate_blank(x, p.fixed_thickness, p) - _x_cylinder(
        p.fixed_groove_od,
        p.fixed_thickness + 2.0 * p.boolean_axial_overcut,
        x,
        p.shaft_y,
        p.shaft_z,
    )
    land_x = (
        x
        + p.fixed_thickness / 2.0
        + p.fixed_thrust_land_height / 2.0
    )
    land = _x_cylinder(
        p.thrust_land_od,
        p.fixed_thrust_land_height,
        land_x,
        p.shaft_y,
        p.shaft_z,
    ) - _x_cylinder(
        p.cam_d_bore_od,
        p.fixed_thrust_land_height + 2.0 * p.boolean_axial_overcut,
        land_x,
        p.shaft_y,
        p.shaft_z,
    )
    return _label(
        main + land,
        "proof_only_right_fixed_full_S1_coaxial_annular_swept_envelope",
        "#8553A6",
    )


@lru_cache(maxsize=8)
def _right_fixed_roll_certificate_cached(p: P13Parameters) -> str:
    tolerance = continuous_overlap_tolerance(p)
    right_fixed = build_fixed_plate("right", p)
    right_fixed_bbox = right_fixed.bounding_box()
    derived_inner_x = p.fixed_right_x - p.fixed_thickness / 2.0
    if abs(right_fixed_bbox.min.X - derived_inner_x) > 1.0e-9:
        raise ValueError("right-fixed source BREP inner face disagrees with parametric datum")
    u_clear = p.rod_length / 2.0 - right_fixed_bbox.min.X
    if abs(u_clear - p.right_fixed_rod_clearance_withdrawal) > 1.0e-9:
        raise ValueError("right-fixed rod-clear guard disagrees with source BREP")
    u_full = p.rod_withdrawal_distance
    if u_full < u_clear:
        raise ValueError("full rod withdrawal does not reach right-fixed clear state")

    envelope = build_right_fixed_full_roll_envelope(p)
    structure = list(build_four_plate_structure(p.open_angle_deg, p).children)
    remaining = [item for item in structure if item.label != right_fixed.label]
    workpiece_start = build_workpiece(p).children[0]
    workpiece_end = build_workpiece(
        p, cad_source_global_removal_certificate(p)["globalRemovalCommand"]["value"]
    ).children[0]
    structure_overlaps = {
        item.label: _intersection_volume(envelope, item) for item in remaining
    }
    workpiece_overlaps = {
        "liftStart": _intersection_volume(envelope, workpiece_start),
        "liftEnd": _intersection_volume(envelope, workpiece_end),
    }
    maximum_envelope_overlap = max(
        [*structure_overlaps.values(), *workpiece_overlaps.values()], default=0.0
    )
    if maximum_envelope_overlap > tolerance:
        raise ValueError(
            f"right-fixed full-S1 envelope intersects remaining state: {maximum_envelope_overlap}"
        )

    diagnostic_angles = [
        index * P13_RIGHT_FIXED_ROLL_DIAGNOSTIC_STEP_DEG
        for index in range(
            int(360.0 / P13_RIGHT_FIXED_ROLL_DIAGNOSTIC_STEP_DEG) + 1
        )
    ]
    diagnostic_rows: list[dict[str, object]] = []
    for alpha in diagnostic_angles:
        rotated = _rotate_about_shaft(build_fixed_plate("right", p), alpha, p)
        outside = rotated - envelope
        outside_volume = 0.0 if outside is None else float(outside.volume)
        maximum_actual_overlap = max(
            [
                *[_intersection_volume(rotated, item) for item in remaining],
                _intersection_volume(rotated, workpiece_start),
                _intersection_volume(rotated, workpiece_end),
            ],
            default=0.0,
        )
        if outside_volume > tolerance or maximum_actual_overlap > tolerance:
            raise ValueError(f"right-fixed actual-solid roll diagnostic failed at {alpha} degrees")
        diagnostic_rows.append(
            {
                "alpha": {"unit": "degree", "value": alpha},
                "actualSolidOutsideAnalyticEnvelopeVolume": {
                    "unit": "cubic_millimetre",
                    "value": outside_volume,
                },
                "maximumActualSolidIntersectionVolume": {
                    "unit": "cubic_millimetre",
                    "value": maximum_actual_overlap,
                },
            }
        )

    counterexample_plate = _rotate_about_shaft(
        build_fixed_plate("right", p), P13_INSTALLED_ROLL_COUNTEREXAMPLE_DEG, p
    )
    counterexample_overlaps = {
        name: _intersection_volume(
            counterexample_plate,
            build_rod(name, p.open_angle_deg, p),
        )
        for name in ROD_NAMES
    }
    if max(counterexample_overlaps.values()) <= tolerance:
        raise ValueError("installed +5-degree counterexample did not intersect a rod")

    guard_delta = P13_EPS_GLOBAL_MM
    guard_rows = {}
    for label, withdrawal in (
        ("below", u_clear - guard_delta),
        ("at", u_clear),
        ("above", u_clear + guard_delta),
    ):
        right_tip = p.rod_length / 2.0 - withdrawal
        guard_rows[label] = {
            "withdrawalU": {"unit": "millimetre", "value": withdrawal},
            "rodRightTipX": {"unit": "millimetre", "value": right_tip},
            "rightFixedBREPMinX": {
                "unit": "millimetre",
                "value": right_fixed_bbox.min.X,
            },
            "journalRelationJi": right_tip > right_fixed_bbox.min.X,
            "axialClearance": {
                "unit": "millimetre",
                "value": right_fixed_bbox.min.X - right_tip,
            },
        }

    component = right_fixed_engaged_roll_classification(p)
    result = {
        "schema": "P13RightFixedRollCertificate/v1",
        "proof": "stage-correlated engaged exact-lane component plus analytic full-S1 annular swept-BREP after exact rod-clear guard",
        "stageUnion": right_fixed_roll_stage_union(p),
        "supportGuard": {
            "source": "final right-fixed BREP bounding_box.min.X",
            "rightFixedBREPMinX": {
                "unit": "millimetre",
                "value": right_fixed_bbox.min.X,
            },
            "uClear": {"unit": "millimetre", "value": u_clear},
            "uFull": {"unit": "millimetre", "value": u_full},
            "fullWithdrawalGap": {
                "unit": "millimetre",
                "value": u_full - u_clear,
            },
            "boundaryRows": guard_rows,
        },
        "engagedComponent": component,
        "installedFiveDegreeCounterexample": {
            "alpha": {
                "unit": "degree",
                "value": P13_INSTALLED_ROLL_COUNTEREXAMPLE_DEG,
            },
            "actualRodIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": counterexample_overlaps,
            },
            "maximumIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": max(counterexample_overlaps.values()),
            },
        },
        "fullS1AfterClear": {
            "proofMethod": "coaxial outer blanks minus persistent circular journal; lanes and C-mouth omitted only conservatively",
            "rollDomain": {"unit": "degree", "value": list(P13_FULL_ROLL_DOMAIN_DEG)},
            "envelopeLabel": envelope.label,
            "proofConstituents": {
                "actualRightFixedOccurrence": right_fixed.label,
                "persistentCutter": f"coaxial_circular_journal_D{_tag(p.fixed_groove_od)}",
                "mainOuterBlank": f"coaxial_disc_D{_tag(p.plate_diameter)}_T{_tag(p.fixed_thickness)}",
                "thrustLandOuterBlank": (
                    f"coaxial_land_D{_tag(p.thrust_land_od)}_"
                    f"T{_tag(p.fixed_thrust_land_height)}"
                ),
                "remainingStructureOccurrences": [item.label for item in remaining],
                "remainingIntegralFeatures": [
                    f"right_actuator_{P13_CAM_PHASE_FEATURE}",
                    f"shaft_keeper_C_journal_ID{_tag(p.keeper_id)}",
                ],
                "completeWorkpieceOccurrences": [workpiece_start.label, workpiece_end.label],
            },
            "remainingStructureIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": structure_overlaps,
            },
            "completeWorkpieceIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": workpiece_overlaps,
            },
            "maximumIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": maximum_envelope_overlap,
            },
            "diagnosticOnlyActualSolidSamples": diagnostic_rows,
            "samplesUsedForProof": False,
            "seamIdentification": "0 degree == 360 degree",
        },
        "allRollWorkpieceLift": {
            "certificatePath": "removal.completeWorkpieceLift",
            "rightFixedEnvelopePath": "rightFixedRollCertificate.fullS1AfterClear",
            "certifiedForEveryAlphaInS1": maximum_envelope_overlap <= tolerance,
        },
        "overlapVolumeTolerance": {
            "unit": "cubic_millimetre",
            "value": tolerance,
        },
    }
    return json.dumps(result, sort_keys=True, separators=(",", ":"))


def right_fixed_roll_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    return json.loads(_right_fixed_roll_certificate_cached(p))


def validate_right_fixed_roll_certificate(candidate: dict[str, object]) -> None:
    """Reject omitted stage, guard, cutter, occurrence, and all-roll evidence."""

    required = {
        "schema",
        "proof",
        "stageUnion",
        "supportGuard",
        "engagedComponent",
        "installedFiveDegreeCounterexample",
        "fullS1AfterClear",
        "allRollWorkpieceLift",
        "overlapVolumeTolerance",
    }
    if set(candidate) != required:
        raise ValueError("right-fixed-roll certificate has omitted or hidden top-level evidence")
    validate_right_fixed_roll_stage_union(candidate["stageUnion"])
    full_roll = candidate["fullS1AfterClear"]
    constituents = full_roll.get("proofConstituents", {})
    required_constituents = {
        "actualRightFixedOccurrence",
        "persistentCutter",
        "mainOuterBlank",
        "thrustLandOuterBlank",
        "remainingStructureOccurrences",
        "remainingIntegralFeatures",
        "completeWorkpieceOccurrences",
    }
    if set(constituents) != required_constituents:
        raise ValueError("right-fixed-roll certificate hides a cutter or occurrence")
    if not candidate["allRollWorkpieceLift"].get("certifiedForEveryAlphaInS1"):
        raise ValueError("right-fixed-roll certificate omits all-roll workpiece lift")
    component = candidate["engagedComponent"]
    if component.get("seamIdentification") != "0 degree == 360 degree":
        raise ValueError("right-fixed-roll certificate omits S1 seam equivalence")
    if component.get("nonAlpha0Components") != []:
        raise ValueError("right-fixed-roll certificate permits a component jump")


def right_cap_stage1_certificate(
    p: P13Parameters = P13_DEFAULTS,
    domain: dict[str, object] | None = None,
) -> dict[str, object]:
    """Certify all three right-cap removals before rod withdrawal.

    The cap's full-S1 outer-cylinder cover is checked against the complete
    invariant structure, the connected workpiece, both non-mating rods, and
    the other two cap envelopes.  Intersection with its own rod is recorded as
    the intended seated engagement and is never counted as clearance.
    """

    source_domain = cad_source_removal_domain(p) if domain is None else domain
    engagement_lower, engagement_upper = _engagement_interval(
        source_domain, "right_cap_engagement_each"
    )
    roll_lower, roll_upper = _roll_interval(source_domain, "right_cap_roll_each")
    structure = list(build_four_plate_structure(p.open_angle_deg, p).children)
    workpiece = build_workpiece(p).children[0]
    rods = {name: build_rod(name, p.open_angle_deg, p) for name in ROD_NAMES}
    envelopes = {
        name: build_right_cap_stage1_envelope(name, p, source_domain)
        for name in ROD_NAMES
    }
    tolerance = continuous_overlap_tolerance(p)
    rows: dict[str, object] = {}
    for name in ROD_NAMES:
        envelope = envelopes[name]
        structure_overlaps = {
            rigid.label: _intersection_volume(envelope, rigid) for rigid in structure
        }
        workpiece_overlap = _intersection_volume(envelope, workpiece)
        non_mating_rod_overlaps = {
            other_name: _intersection_volume(envelope, rods[other_name])
            for other_name in ROD_NAMES
            if other_name != name
        }
        mutual_overlaps = {
            other_name: _intersection_volume(envelope, envelopes[other_name])
            for other_name in ROD_NAMES
            if other_name != name
        }
        intended_own_rod_overlap = _intersection_volume(envelope, rods[name])
        maximum = max(
            [
                *structure_overlaps.values(),
                workpiece_overlap,
                *non_mating_rod_overlaps.values(),
                *mutual_overlaps.values(),
            ],
            default=0.0,
        )
        if maximum > tolerance:
            raise ValueError(f"right-cap Stage-1 envelope collides for {name}: {maximum}")
        rows[name] = {
            "engagementDomain": {
                "unit": "millimetre",
                "value": [engagement_lower, engagement_upper],
            },
            "rollDomain": {
                "unit": "degree",
                "value": [roll_lower, roll_upper],
            },
            "outwardTranslationDomainX": {
                "unit": "millimetre",
                "value": [0.0, engagement_upper],
            },
            "seatedCapExtentXAtEngagementEndpoints": {
                "unit": "millimetre",
                "value": {
                    "lower": [
                        p.rod_length / 2.0 - engagement_lower,
                        p.rod_length / 2.0 - engagement_lower + p.cap_length,
                    ],
                    "upper": [
                        p.rod_length / 2.0 - engagement_upper,
                        p.rod_length / 2.0 - engagement_upper + p.cap_length,
                    ],
                },
            },
            "sweptEnvelopeExtentX": {
                "unit": "millimetre",
                "value": [
                    p.rod_length / 2.0 - engagement_upper,
                    p.rod_length / 2.0 + p.cap_length,
                ],
            },
            "envelopeLabel": envelope.label,
            "structureIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": structure_overlaps,
            },
            "completeWorkpieceIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": workpiece_overlap,
            },
            "nonMatingRodIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": non_mating_rod_overlaps,
            },
            "otherStage1EnvelopeIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": mutual_overlaps,
            },
            "intendedOwnRodEngagementEnvelopeIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": intended_own_rod_overlap,
            },
            "maximumUnintendedIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": maximum,
            },
            "certificateMargin": {
                "unit": "cubic_millimetre",
                "value": tolerance - maximum,
            },
        }
    global_maximum = max(
        row["maximumUnintendedIntersectionVolume"]["value"] for row in rows.values()
    )
    return {
        "proof": "range-expanded outer-cylinder swept-BREP over engagement, outward translation, and full S1 roll",
        "stageOrdering": {
            "stage": 1,
            "mustCompleteBefore": "rodLeftCapWithdrawal",
            "rightCapsRemovedBeforeLift": True,
        },
        "domainSources": {
            "engagement": "Domain-A.variables.right_cap_engagement_each.bounds",
            "roll": "Domain-A.variables.right_cap_roll_each.bounds",
        },
        "overlapVolumeTolerance": {
            "unit": "cubic_millimetre",
            "value": tolerance,
        },
        "rows": rows,
        "maximumUnintendedIntersectionVolume": {
            "unit": "cubic_millimetre",
            "value": global_maximum,
        },
    }


def validate_continuous_removal_certificate(candidate: dict[str, object]) -> None:
    """Fail closed if a serialized removal proof omits a stage or rod row."""

    required_stages = {
        "rightCapStage1Removal",
        "rodLeftCapWithdrawal",
        "completeWorkpieceLift",
        "rightFixedRollStageCorrelation",
    }
    missing_stages = sorted(required_stages - set(candidate))
    if missing_stages:
        raise ValueError(f"continuous removal certificate missing stages: {missing_stages}")
    for stage_name, maximum_name in (
        ("rightCapStage1Removal", "maximumUnintendedIntersectionVolume"),
        ("rodLeftCapWithdrawal", "maximumIntersectionVolume"),
    ):
        stage = candidate[stage_name]
        if not isinstance(stage, dict):
            raise ValueError(f"continuous removal stage is not an object: {stage_name}")
        rows = stage.get("rows", stage if stage_name == "rodLeftCapWithdrawal" else None)
        if not isinstance(rows, dict) or set(rows) != set(ROD_NAMES):
            raise ValueError(f"continuous removal stage has incomplete rod rows: {stage_name}")
        for name, row in rows.items():
            if not isinstance(row, dict) or maximum_name not in row:
                raise ValueError(
                    f"continuous removal stage row omits maximum: {stage_name}.{name}"
                )
    validate_right_fixed_roll_certificate(candidate["rightFixedRollStageCorrelation"])


def continuous_removal_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    """Continuous normal-removal certificate for the nominal CAD.

    Complete rod/permanent-cap units use conservative exact-X swept BREPs.
    The complete workpiece +Z motion uses the stronger global analytic
    primitive proof from :func:`workpiece_plus_z_certificate`: every non-shaft
    structure is X-separated, and every shaft-relevant point begins above the
    shaft so its radial distance is nondecreasing through the full lift.
    """

    source_certificate = cad_source_global_removal_certificate(p)
    source_domain = source_certificate["domain"]
    left_withdrawal_geometry = rod_left_cap_withdrawal_certificate(p, source_domain)
    right_cap_certificate = right_cap_stage1_certificate(p, source_domain)
    right_fixed_certificate = right_fixed_roll_certificate(p)
    structure = list(build_four_plate_structure(p.open_angle_deg, p).children)
    structure_labels = [item.label for item in structure]
    workpiece = build_workpiece(p).children[0]
    tolerance = continuous_overlap_tolerance(p)
    rod_rows: dict[str, object] = {}
    envelopes = {
        name: build_rod_left_cap_withdrawal_envelope(name, p, source_domain)
        for name in ROD_NAMES
    }
    for name in ROD_NAMES:
        envelope = envelopes[name]
        structure_overlaps = {
            rigid.label: max(
                _intersection_volume(piece, rigid) for piece in envelope.children
            )
            for rigid in structure
        }
        workpiece_overlap = max(
            _intersection_volume(piece, workpiece) for piece in envelope.children
        )
        other_unit_overlaps = {
            other_name: max(
                _intersection_volume(piece, other_piece)
                for piece in envelope.children
                for other_piece in envelopes[other_name].children
            )
            for other_name in ROD_NAMES
            if other_name != name
        }
        maximum = max(
            [*structure_overlaps.values(), workpiece_overlap, *other_unit_overlaps.values()],
            default=0.0,
        )
        if maximum > tolerance:
            raise ValueError(f"continuous withdrawal envelope collides for {name}: {maximum}")
        rod_rows[name] = {
            "engagementDomain": left_withdrawal_geometry["engagementDomain"],
            "translationDomainX": {
                "unit": "millimetre",
                "value": [-p.rod_withdrawal_distance, 0.0],
            },
            "envelopeLabels": [item.label for item in envelope.children],
            "structureIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": structure_overlaps,
            },
            "completeWorkpieceIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": workpiece_overlap,
            },
            "otherWithdrawalEnvelopeIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": other_unit_overlaps,
            },
            "synchronousWithdrawalEnvelopeIntersectionVolumes": {
                "unit": "cubic_millimetre",
                "value": other_unit_overlaps,
            },
            "maximumIntersectionVolume": {
                "unit": "cubic_millimetre",
                "value": maximum,
            },
            "certificateMargin": {
                "unit": "cubic_millimetre",
                "value": tolerance - maximum,
            },
        }

    lift_certificate = workpiece_plus_z_certificate(p)
    if lift_certificate["globalMargin"]["value"] <= 0.0:
        raise ValueError("nonpositive continuous complete-workpiece +Z margin")
    result = {
        "cadSourceStatus": "CAD_SOURCE_DOMAIN_CERTIFIED",
        "physicalRecordStatus": "PHYSICAL_RECORD_NOT_INSTANTIATED",
        "method": "range-expanded cap and complete-unit swept BREPs plus exact global analytic complete-workpiece +Z decomposition",
        "cadSourceDomainCertificate": source_certificate,
        "futureMeasuredSpecimenSchema": physical_record_schema(),
        "overlapVolumeTolerance": {
            "unit": "cubic_millimetre",
            "value": tolerance,
        },
        "invariantStructureLabels": structure_labels,
        "rightCapStage1Removal": right_cap_certificate,
        "rightFixedRollStageCorrelation": right_fixed_certificate,
        "rodLeftCapWithdrawalDomain": left_withdrawal_geometry,
        "rodLeftCapWithdrawal": rod_rows,
        "completeWorkpieceLift": lift_certificate,
    }
    validate_continuous_removal_certificate(result)
    return result


def continuous_certificate_package(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    return {
        "schema": "P13ContinuousCertificates/v1",
        "briefSha256": P13_GATE0_BRIEF_SHA256,
        "domainAmendmentSha256": P13_DOMAIN_AMENDMENT_SHA256,
        "cadSourceStatus": "CAD_SOURCE_DOMAIN_CERTIFIED",
        "physicalRecordStatus": "PHYSICAL_RECORD_NOT_INSTANTIATED",
        "sourceRevisionSha256": source_revision_sha256(),
        "parameterManifestSha256": parameter_manifest_sha256(p),
        "motion": continuous_motion_certificate(p),
        "laneSolidWitness": continuous_lane_solid_certificate(p),
        "removal": continuous_removal_certificate(p),
        "shaftServiceExtraction": shaft_service_extraction_certificate(p),
    }


def build_removal_sweep_review(p: P13Parameters = P13_DEFAULTS) -> Compound:
    removal_command = cad_source_global_removal_certificate(p)["globalRemovalCommand"]["value"]
    removal_command_tag = f"{removal_command:.3f}".replace(".", "p")
    palette = ("#7C3AED", "#2563EB", "#06B6D4", "#22C55E", "#EAB308")
    sampled_workpieces = []
    for index in range(p.removal_review_sample_count):
        lift = removal_command * index / (p.removal_review_sample_count - 1)
        workpiece = build_workpiece(p, lift).children[0]
        sampled_workpieces.append(
            _label(
                workpiece,
                f"diagnostic_only_removal_plusZ_sample_{index + 1}_of_{p.removal_review_sample_count}_lift_{_tag(lift)}",
                palette[index % len(palette)],
            )
        )
    removed_caps = [
        Pos(p.cap_removed_offset_x, 0.0, 0.0)
        * build_right_cap(name, p.open_angle_deg, p)
        for name in ROD_NAMES
    ]
    return Compound(
        children=[
            *build_four_plate_structure(p.open_angle_deg, p).children,
            *build_three_rod_left_cap_units(
                p.open_angle_deg, p, -p.rod_withdrawal_distance
            ).children,
            *removed_caps,
            *sampled_workpieces,
        ],
        label=f"P13_REMOVE_diagnostic_only_samples_to_global_command_{removal_command_tag}mm",
    )


def build_remove(p: P13Parameters = P13_DEFAULTS) -> Compound:
    removal_command = cad_source_global_removal_certificate(p)["globalRemovalCommand"]["value"]
    removal_command_tag = f"{removal_command:.3f}".replace(".", "p")
    removed_caps = [
        Pos(p.cap_removed_offset_x, 0.0, 0.0)
        * build_right_cap(name, p.open_angle_deg, p)
        for name in ROD_NAMES
    ]
    return Compound(
        children=[
            *build_four_plate_structure(p.open_angle_deg, p).children,
            *build_three_rod_left_cap_units(
                p.open_angle_deg, p, -p.rod_withdrawal_distance
            ).children,
            *removed_caps,
            *build_workpiece(p, removal_command).children,
        ],
        label=f"P13_REMOVE_global_command_{removal_command_tag}mm_full_workpiece_caps_off_rods_left",
    )


def build_exploded(p: P13Parameters = P13_DEFAULTS) -> Compound:
    parts = [
        Pos(-p.exploded_plate_offset_x, 0.0, 0.0) * build_left_cam(p.open_angle_deg, p),
        Pos(-p.exploded_fixed_offset_x, 0.0, 0.0) * build_fixed_plate("left", p),
        Pos(p.exploded_fixed_offset_x, 0.0, 0.0) * build_fixed_plate("right", p),
        Pos(p.exploded_plate_offset_x, 0.0, 0.0) * build_right_actuator(p.open_angle_deg, p),
        Pos(0.0, p.exploded_rod_offset_y / 2.0, 0.0)
        * build_actuator_shaft(p.open_angle_deg, p),
        Pos(-p.exploded_plate_offset_x, 0.0, p.exploded_keeper_offset_z) * build_shaft_keeper(p),
    ]
    for index, name in enumerate(ROD_NAMES):
        offset = Pos(0.0, p.exploded_rod_offset_y, -p.exploded_rod_pitch_z * index)
        parts.append(offset * build_rod(name, p.open_angle_deg, p))
        stage_z = p.exploded_cap_pitch_z * (1 - index)
        left_cap = (
            Pos(-p.exploded_cap_lane_x, p.exploded_left_cap_lane_y, stage_z)
            * Rot(0.0, 0.0, p.cap_reverse_rotation_deg)
            * copy(_left_cap_local(p))
        )
        right_cap = Pos(
            p.exploded_cap_lane_x,
            p.exploded_right_cap_lane_y,
            stage_z,
        ) * copy(_right_cap_local(p))
        parts.extend(
            [
                _label(
                    left_cap,
                    f"exploded_stage_{index + 1}_permanent_round_left_cap_{name}",
                    "#525A60",
                ),
                _label(
                    right_cap,
                    f"exploded_stage_{index + 1}_removable_round_right_cap_{name}",
                    "#737C82",
                ),
            ]
        )
    return Compound(
        children=parts,
        label="P13_exploded_four_plates_separate_D_shaft_keeper_three_rod_left_cap_units_three_right_caps",
    )


def build_shaft_extraction_envelope(
    p: P13Parameters = P13_DEFAULTS,
) -> Compound:
    """Exact translational sweep cover for staged +X shaft extraction.

    Both round reduced lands are contained inside the shallow-D main profile.
    The stop head starts outside the right hub and moves farther right, so its
    own D-prism sweep is kept separate from the body sweep.
    """

    distance = p.shaft_extraction_distance
    body_length = p.shaft_head_inner_x - p.shaft_x0 + distance
    body = _label(
        _d_prism_x(
            p.shaft_od,
            p.shaft_d_across_flat,
            body_length,
            (p.shaft_x0 + p.shaft_head_inner_x + distance) / 2.0,
            p,
        ),
        "continuous_plusX_separate_D_shaft_body_sweep",
        "#C48720",
    )
    shaft_flat_offset = p.shaft_d_across_flat - p.shaft_od / 2.0
    head_across_flat = p.shaft_head_od / 2.0 + shaft_flat_offset
    head = _label(
        _d_prism_x(
            p.shaft_head_od,
            head_across_flat,
            p.shaft_head_thickness + distance,
            (p.shaft_head_inner_x + p.shaft_head_outer_x + distance) / 2.0,
            p,
        ),
        "continuous_plusX_stop_head_sweep_outside_right_hub",
        "#C48720",
    )
    return Compound(
        children=[body, head],
        label="certified_staged_keeper_off_guides_clear_then_shaft_plusX_sweep",
    )


def shaft_service_extraction_certificate(
    p: P13Parameters = P13_DEFAULTS,
) -> dict[str, object]:
    tolerance = continuous_overlap_tolerance(p)
    envelope = build_shaft_extraction_envelope(p)
    cams = [build_left_cam(p.open_angle_deg, p), build_right_actuator(p.open_angle_deg, p)]
    fixed = [build_fixed_plate("left", p), build_fixed_plate("right", p)]
    staged = {
        cam.label: max(_intersection_volume(piece, cam) for piece in envelope.children)
        for cam in cams
    }
    direct = {
        guide.label: max(_intersection_volume(piece, guide) for piece in envelope.children)
        for guide in fixed
    }
    max_staged = max(staged.values(), default=0.0)
    min_direct = min(direct.values(), default=0.0)
    d_bore_flat_offset = p.cam_d_bore_across_flat - p.cam_d_bore_od / 2.0
    journal_to_d_flat_clearance = d_bore_flat_offset - p.journal_land_od / 2.0
    one_sided_lash_deg = d_shaft_one_sided_lash_deg(p)
    if max_staged > tolerance:
        raise ValueError(f"staged shaft extraction intersects stationary cams: {max_staged}")
    if min_direct <= tolerance:
        raise ValueError("direct extraction through installed fixed guides was not rejected")
    if journal_to_d_flat_clearance < 0.10 - 1.0e-9:
        raise ValueError("round journal-to-D-bore flat clearance is below 0.10 mm")
    if one_sided_lash_deg > 3.0 + 1.0e-9:
        raise ValueError("exact one-sided D-interface angular lash exceeds 3 degrees")
    return {
        "schema": "P13StagedShaftServiceExtractionCertificate/v1",
        "serviceOrder": [
            "shaft_keeper_radially_off",
            "both_upward_C_fixed_guides_release_minusZ",
            "separate_D_shaft_extract_plusX_through_stationary_cams",
        ],
        "directPlusXWithFixedGuidesInstalled": {
            "admissible": False,
            "actualSolidIntersectionVolumes": {"unit": "cubic_millimetre", "value": direct},
        },
        "stagedPlusXAfterFixedGuidesClear": {
            "admissible": True,
            "actualSolidIntersectionVolumes": {"unit": "cubic_millimetre", "value": staged},
            "maximumIntersectionVolume": {"unit": "cubic_millimetre", "value": max_staged},
            "extractionDistance": {"unit": "millimetre", "value": p.shaft_extraction_distance},
        },
        "journalToDBoreFlatClearance": {
            "unit": "millimetre",
            "value": journal_to_d_flat_clearance,
        },
        "dInterfaceAngularLash": {
            "method": "exact_male_D_endpoint_support_to_female_flat_contact",
            "oneSided": {"unit": "degree", "value": one_sided_lash_deg},
            "totalSymmetric": {"unit": "degree", "value": 2.0 * one_sided_lash_deg},
            "acceptanceMaximumOneSided": {"unit": "degree", "value": 3.0},
        },
        "overlapVolumeTolerance": {"unit": "cubic_millimetre", "value": tolerance},
    }


def build_service_disassembly(p: P13Parameters = P13_DEFAULTS) -> Compound:
    """Service-only order after workpiece and all rods/caps are already off.

    Keeper is shown radially released first, both upward-C guides are released
    -Z, then the separate shaft is extracted +X/right through the two cams.
    from normal REMOVE, where the four-plate structure remains assembled.
    """
    return Compound(
        children=[
            build_left_cam(p.open_angle_deg, p),
            Pos(0.0, 0.0, p.service_fixed_offset_z) * build_fixed_plate("left", p),
            Pos(0.0, 0.0, p.service_fixed_offset_z) * build_fixed_plate("right", p),
            build_right_actuator(p.open_angle_deg, p),
            Pos(p.shaft_extraction_distance, 0.0, 0.0)
            * build_actuator_shaft(p.open_angle_deg, p),
            Pos(0.0, 0.0, p.service_keeper_offset_z) * build_shaft_keeper(p),
        ],
        label="P13_SERVICE_keeper_off_guides_minusZ_clear_then_separate_D_shaft_plusX_through_cams",
    )


def _on_bed(shape: Shape, x: float, y: float, rotate_y: float) -> Shape:
    oriented = Rot(0.0, rotate_y, 0.0) * shape
    bounds = oriented.bounding_box()
    return Pos(x - (bounds.min.X + bounds.max.X) / 2.0, y - (bounds.min.Y + bounds.max.Y) / 2.0, -bounds.min.Z) * oriented


def _d_prism_z(
    od: float,
    across_flat: float,
    height: float,
    x: float,
    y: float,
    p: P13Parameters,
) -> Shape:
    radius = od / 2.0
    flat_offset = across_flat - radius
    cylinder = Pos(x, y, 0.0) * Cylinder(
        radius,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    keeper = _box(
        (x, y + (radius - flat_offset) / 2.0, height / 2.0),
        (
            od + p.boolean_radial_margin,
            radius + flat_offset,
            height + p.boolean_axial_overcut,
        ),
    )
    clipped = cylinder.intersect(keeper)
    return clipped if hasattr(clipped, "volume") else clipped.solids()[0]


def build_fit_coupons(p: P13Parameters = P13_DEFAULTS) -> Compound:
    coupon_z = p.diagnostic_coupon_thickness / 2.0
    lane_start_y = -p.diagnostic_lane_pitch * (len(p.diagnostic_lane_widths) - 1) / 2.0
    lane = _box(
        (0.0, 0.0, coupon_z),
        (p.diagnostic_lane_coupon_x, p.diagnostic_lane_coupon_y, p.diagnostic_coupon_thickness),
    ) - [
        _x_cylinder(
            width,
            p.diagnostic_lane_coupon_x + p.boolean_plate_overcut,
            0.0,
            lane_start_y + index * p.diagnostic_lane_pitch,
            coupon_z,
        )
        for index, width in enumerate(p.diagnostic_lane_widths)
    ]
    lane = _label(lane, "diagnostic_lane_width_coupon_role", "#7A858B")
    if len(p.diagnostic_cam_bores) != len(p.diagnostic_cam_across_flats):
        raise ValueError("diagnostic D bore OD/AF variants must be paired")
    bore_start_x = -p.diagnostic_bore_pitch * (len(p.diagnostic_cam_bores) - 1) / 2.0
    d_cutters = [
        _d_prism_z(
            diameter,
            p.diagnostic_cam_across_flats[index],
            p.diagnostic_coupon_thickness + p.boolean_axial_overcut,
            bore_start_x + index * p.diagnostic_bore_pitch,
            -4.0,
            p,
        )
        for index, diameter in enumerate(p.diagnostic_cam_bores)
    ]
    journal_start_x = -5.0
    journal_cutters = [
        Pos(journal_start_x + index * 5.0, 4.0, 0.0)
        * Cylinder(
            diameter / 2.0,
            p.diagnostic_coupon_thickness + p.boolean_axial_overcut,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        for index, diameter in enumerate(p.diagnostic_journal_ods)
    ]
    bore = _box(
        (0.0, 0.0, coupon_z),
        (p.diagnostic_bore_coupon_x, p.diagnostic_bore_coupon_y, p.diagnostic_coupon_thickness),
    ) - [*d_cutters, *journal_cutters]
    bore = _label(bore, "diagnostic_D_bore_and_round_journal_coupon_role", "#7A858B")
    return Compound(
        children=[lane, Pos(p.print_coupon_x_offset, 0.0, 0.0) * bore],
        label="diagnostic_fit_coupons_not_production_selectors",
    )


def build_print_kit(p: P13Parameters = P13_DEFAULTS) -> Compound:
    # Purchased rods and every review-only workpiece/tool envelope are excluded.
    left_cam = _on_bed(
        build_left_cam(p.open_angle_deg, p),
        -p.print_plate_pitch_x,
        p.print_upper_y,
        p.print_actuator_rotation_deg,
    )
    left_fixed = _on_bed(
        build_fixed_plate("left", p), 0.0, p.print_upper_y, p.print_plate_rotation_deg
    )
    right_fixed = _on_bed(
        build_fixed_plate("right", p),
        p.print_plate_pitch_x,
        p.print_upper_y,
        -p.print_plate_rotation_deg,
    )
    right_actuator = _on_bed(
        build_right_actuator(p.open_angle_deg, p),
        0.0,
        p.print_actuator_y,
        -p.print_actuator_rotation_deg,
    )
    shaft = _on_bed(
        build_actuator_shaft(p.open_angle_deg, p),
        p.print_shaft_x,
        p.print_shaft_y,
        p.print_shaft_rotation_deg,
    )
    keeper = _on_bed(
        build_shaft_keeper(p), p.print_keeper_x, p.print_keeper_y, p.print_plate_rotation_deg
    )
    caps = [
        _on_bed(
            copy(_left_cap_local(p)),
            p.print_cap_left_x0 + index * p.print_cap_pitch_x,
            p.print_cap_y,
            p.print_cap_rotation_deg,
        )
        for index in range(3)
    ] + [
        _on_bed(
            copy(_right_cap_local(p)),
            p.print_cap_right_x0 + index * p.print_cap_pitch_x,
            p.print_cap_y,
            p.print_cap_rotation_deg,
        )
        for index in range(3)
    ]
    for index, cap in enumerate(caps[:3]):
        _label(cap, f"print_permanent_left_cap_{index + 1}", "#525A60")
    for index, cap in enumerate(caps[3:]):
        _label(cap, f"print_removable_right_cap_{index + 1}", "#737C82")
    coupons = [Pos(0.0, p.print_coupon_y, 0.0) * child for child in build_fit_coupons(p).children]
    return Compound(
        children=[left_cam, left_fixed, right_fixed, right_actuator, shaft, keeper, *caps, *coupons],
        label="P13_print_kit_four_principal_plates_separate_D_shaft_keeper_six_caps_diagnostic_coupons_no_forming_rods",
    )


def source_occurrence_census() -> dict[str, int]:
    return {
        "visible_principal_plate_occurrences": 4,
        "unique_principal_print_definitions": 3,
        "fixed_guide_print_quantity": 2,
        "purchased_uncut_rods": 3,
        "right_actuator_occurrences": 1,
        "separate_shaft_occurrences": 1,
        "shaft_keepers": 1,
        "rod_caps": 6,
        "user_actuator_inputs": 1,
        "bases_spines_bridges_holders": 0,
    }


def nominal_validation_boundary() -> str:
    return (
        "EXPLORATORY NOMINAL ONLY: physical fit, measured tolerance feasible-set, "
        "strength, heat, long-term friction retention, springback, and mechanism usability "
        "are unproven; the removable right-cap has only an initial accepted PETG hand-fit gate"
    )


P13_ARTIFACT_NAMES = (
    "open",
    "loaded",
    "set_close",
    "locked",
    "solder_left",
    "solder_right",
    "cool",
    "release",
    "caps_off",
    "rods_withdrawn",
    "remove",
    "removal_sweep",
    "exploded",
    "service_disassembly",
    "print_kit",
    "fixed_guide",
    "left_cam",
    "right_actuator",
    "actuator_shaft",
    "shaft_keeper",
    "left_cap",
    "right_cap",
    "fit_coupons",
)


def build_artifact(name: str, p: P13Parameters = P13_DEFAULTS) -> Compound:
    builders = {
        "open": lambda: build_open(p),
        "loaded": lambda: build_loaded(p),
        "set_close": lambda: build_set_close(p),
        "locked": lambda: build_locked(p),
        "solder_left": lambda: build_solder_left(p),
        "solder_right": lambda: build_solder_right(p),
        "cool": lambda: build_cool(p),
        "release": lambda: build_release(p),
        "caps_off": lambda: build_caps_off(p),
        "rods_withdrawn": lambda: build_rods_withdrawn(p),
        "remove": lambda: build_remove(p),
        "removal_sweep": lambda: build_removal_sweep_review(p),
        "exploded": lambda: build_exploded(p),
        "service_disassembly": lambda: build_service_disassembly(p),
        "print_kit": lambda: build_print_kit(p),
        "fixed_guide": lambda: build_fixed_plate("left", p),
        "left_cam": lambda: build_left_cam(p.open_angle_deg, p),
        "right_actuator": lambda: build_right_actuator(p.open_angle_deg, p),
        "actuator_shaft": lambda: build_actuator_shaft(p.open_angle_deg, p),
        "shaft_keeper": lambda: build_shaft_keeper(p),
        "left_cap": lambda: build_left_cap("upright", p.open_angle_deg, p),
        "right_cap": lambda: build_right_cap("upright", p.open_angle_deg, p),
        "fit_coupons": lambda: build_fit_coupons(p),
    }
    if name not in builders:
        raise ValueError(f"unknown artifact {name!r}; choose from {P13_ARTIFACT_NAMES}")
    shape = builders[name]()
    return Compound(
        children=[shape],
        label=f"P13_ARTIFACT_{name}__{provenance_token(p)}",
    )


def evidence_package(p: P13Parameters = P13_DEFAULTS) -> dict[str, object]:
    root = Path(__file__).parents[2]
    folder = root / "cad" / "p13_four_plate_three_rod"
    continuous_path = root / "docs" / "p13-continuous-certificates.json"
    domain_paths = {
        "cadSourceDomain": root / "docs" / "cad-source-domain.json",
        "cadSourceCertificate": root / "docs" / "cad-source-certificate.json",
        "physicalRecordSchema": root / "docs" / "physical-record-schema.json",
    }
    artifacts: dict[str, object] = {}
    for name in P13_ARTIFACT_NAMES:
        path = folder / f"p13_{name}.step"
        artifacts[name] = {
            "path": str(path.relative_to(Path(__file__).parents[2])),
            "exists": path.exists(),
            "stepSha256": sha256(path.read_bytes()).hexdigest() if path.exists() else None,
            "provenanceRoot": f"P13_ARTIFACT_{name}__{provenance_token(p)}",
            "briefSha256": P13_GATE0_BRIEF_SHA256,
            "domainAmendmentSha256": P13_DOMAIN_AMENDMENT_SHA256,
        }
    return {
        "boundary": nominal_validation_boundary(),
        "sourceRevisionSha256": source_revision_sha256(),
        "briefSha256": P13_GATE0_BRIEF_SHA256,
        "domainAmendmentSha256": P13_DOMAIN_AMENDMENT_SHA256,
        "cadSourceStatus": "CAD_SOURCE_DOMAIN_CERTIFIED",
        "physicalRecordStatus": "PHYSICAL_RECORD_NOT_INSTANTIATED",
        "parameterManifestSha256": parameter_manifest_sha256(p),
        "continuousCertificate": {
            "path": str(continuous_path.relative_to(root)),
            "exists": continuous_path.exists(),
            "sha256": sha256(continuous_path.read_bytes()).hexdigest()
            if continuous_path.exists()
            else None,
        },
        "domainEvidence": {
            name: {
                "path": str(path.relative_to(root)),
                "exists": path.exists(),
                "sha256": sha256(path.read_bytes()).hexdigest() if path.exists() else None,
            }
            for name, path in domain_paths.items()
        },
        "artifacts": artifacts,
    }


def write_evidence_files(p: P13Parameters = P13_DEFAULTS) -> None:
    root = Path(__file__).parents[2]
    initial_outputs = (
        (root / "docs" / "p13-default-parameter-manifest.json", parameter_manifest(p)),
        (root / "docs" / "p13-dependency-graph.json", parameter_dependency_graph()),
        (root / "docs" / "p13-continuous-certificates.json", continuous_certificate_package(p)),
        (root / "docs" / "cad-source-domain.json", cad_source_removal_domain(p)),
        (root / "docs" / "cad-source-certificate.json", cad_source_global_removal_certificate(p)),
        (root / "docs" / "physical-record-schema.json", physical_record_schema()),
    )
    for path, payload in initial_outputs:
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    provenance_path = (
        root / "cad" / "p13_four_plate_three_rod" / "p13-artifact-provenance.json"
    )
    provenance_path.write_text(
        json.dumps(evidence_package(p), indent=2, sort_keys=True) + "\n"
    )


def _parse_overrides(raw: str | None) -> dict[str, object]:
    if not raw:
        return {}
    if raw.startswith("@"):
        return json.loads(Path(raw[1:]).read_text())
    return json.loads(raw)


def normalize_step_header(path: Path) -> None:
    """Remove the exporter wall-clock field so one manifest is byte-stable."""
    text = path.read_text()
    normalized, replacements = re.subn(
        r"'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'",
        "'1970-01-01T00:00:00'",
        text,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError(f"expected one STEP FILE_NAME timestamp in {path}")
    path.write_text(normalized)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate parametric P13 STEP artifacts")
    parser.add_argument("--artifact", choices=P13_ARTIFACT_NAMES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--params-json", help="JSON object or @path; safe-retunes only by default")
    parser.add_argument("--allow-regate", action="store_true")
    parser.add_argument("--write-evidence", action="store_true")
    args = parser.parse_args(argv)
    p = parameters_from_overrides(
        _parse_overrides(args.params_json),
        allow_regate=args.allow_regate,
    )
    if args.write_evidence:
        write_evidence_files(p)
    if args.artifact:
        if args.output is None:
            parser.error("--output is required with --artifact")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if not export_step(build_artifact(args.artifact, p), args.output):
            raise RuntimeError(f"failed to export {args.output}")
        normalize_step_header(args.output)
    if not args.artifact and not args.write_evidence:
        parser.error("choose --artifact and/or --write-evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
