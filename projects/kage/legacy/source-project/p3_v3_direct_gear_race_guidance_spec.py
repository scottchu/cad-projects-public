"""Frozen contract for the isolated KAGE V3 direct gear-race guidance trial.

This variant keeps the accepted 300 mm, 260T/16T three-ring transmission and
the connected motor yokes.  It removes the added guide bead entirely.  The
smooth inner cylinder of the existing carrier body, in the tooth-free 0.80 mm
land below each gear face, is the only roller contact surface.

Units are millimetres; XY is the clock plane and +Z faces the viewer.
"""

from __future__ import annotations

from dataclasses import dataclass

from p3_v3_simplified_drive_guidance_spec import P3V3SimplifiedDriveGuidanceSpec


@dataclass(frozen=True)
class P3V3DirectGearRaceGuidanceSpec(P3V3SimplifiedDriveGuidanceSpec):
    artifact_slug: str = "p3_v3_direct_gear_race_guidance"

    # The inherited D4 x 10 upper safety collar touched the adjacent carrier
    # in the complete three-ring stack.  Keep every axial datum and the D4
    # bore unchanged, but use the compact D4 x 8 collar only in this isolated
    # fork.  The rollback source intentionally retains its 10 mm collar.
    upper_split_collar_outer_diameter: float = 8.00

    # Only the upper-bearing-bridge Z band is allowed to approach the moving
    # rings.  Trim that band to a stationary R128.50 limit, leaving 0.50 mm to
    # the R129.00 tooth-tip sweep.  All inherited motor/shaft/gear datums stay
    # unchanged.
    yoke_moving_ring_clearance: float = 0.50

    # Phase-02 motor-mesh adjustment.  The complete connected station moves
    # rigidly along its local radial axis; the motor, miter pair, output shaft,
    # bearings, collars, pinion, and printed yoke never move relative to one
    # another.  The broad slot ends are service positions only.  Powered
    # operation is deliberately limited to the much smaller checked window.
    motor_mount_service_adjustment: float = 2.50
    # Actual unchanged 16T/260T tooth BREPs make the powered window
    # asymmetric: negative q opens the mesh, while positive q tightens it.
    # +0.15 mm already loses reserve in one sampled tooth phase, so +0.10 mm
    # is the frozen powered maximum.  The full slot remains service-only.
    motor_mount_powered_min_adjustment: float = -0.35
    motor_mount_powered_max_adjustment: float = 0.10
    motor_mount_slot_width: float = 3.60
    motor_mount_slot_overall_length: float = 8.60
    motor_mount_screw_nominal_diameter: float = 3.00
    motor_mount_chassis_hole_diameter: float = 3.40
    motor_mount_washer_outer_diameter: float = 7.00
    motor_mount_washer_inner_diameter: float = 3.20
    motor_mount_washer_thickness: float = 0.50
    motor_mount_screw_head_diameter: float = 5.50
    motor_mount_screw_head_height: float = 3.00
    motor_mount_screw_length: float = 10.00
    motor_mount_top_tool_diameter: float = 10.00
    motor_mount_top_tool_height: float = 12.00
    motor_mount_bottom_tool_diameter: float = 8.00
    motor_mount_bottom_tool_height: float = 5.00
    motor_mount_nut_across_flats: float = 5.50
    motor_mount_nut_thickness: float = 2.40

    # Four identical clamps per station.  These replace the inherited outboard
    # R130 clamp line with an R126 line so the complete slot and washer remain
    # inside the widened foot rails at both physical service endpoints.
    unibody_chassis_mount_x: tuple[float, float] = (88.00, 126.00)
    unibody_chassis_mount_y: tuple[float, float] = (-12.00, 12.00)
    unibody_chassis_mount_clearance: float = 3.40
    unibody_foot_rail_width: float = 9.00

    # Small non-functional setup marks on the moving foot show the nominal and
    # powered limits against a fixed chassis datum.  They are not detents and
    # do not constrain motion.
    motor_witness_powered_band_radial_width: float = 0.45
    motor_witness_mark_tangential_width: float = 0.60
    motor_witness_mark_depth: float = 0.25
    motor_witness_service_tick_radial_width: float = 0.40

    @property
    def yoke_upper_bridge_radial_limit(self) -> float:
        return self.tooth_tip_radius - self.yoke_moving_ring_clearance

    @property
    def yoke_upper_bearing_outer_ligament(self) -> float:
        return self.yoke_upper_bridge_radial_limit - (
            self.output_axis_radius + self.unibody_bearing_pocket_diameter / 2.0
        )

    @property
    def motor_mount_slot_center_travel(self) -> float:
        """Distance between the two capsule end centers."""

        return self.motor_mount_slot_overall_length - self.motor_mount_slot_width

    @property
    def motor_mount_physical_range(self) -> tuple[float, float]:
        return (-self.motor_mount_service_adjustment, self.motor_mount_service_adjustment)

    @property
    def motor_mount_powered_range(self) -> tuple[float, float]:
        return (
            self.motor_mount_powered_min_adjustment,
            self.motor_mount_powered_max_adjustment,
        )

    @property
    def motor_witness_powered_band_center_offset(self) -> float:
        lower, upper = self.motor_mount_powered_range
        return (lower + upper) / 2.0

    @property
    def motor_mount_slot_radial_clearance(self) -> float:
        return (self.motor_mount_slot_width - self.motor_mount_screw_nominal_diameter) / 2.0

    @property
    def motor_mount_washer_tangential_ligament(self) -> float:
        return (self.unibody_foot_rail_width - self.motor_mount_washer_outer_diameter) / 2.0

    @property
    def motor_mount_worst_radial_ligament(self) -> float:
        # Outboard washer at R126 and the inward service endpoint govern.
        return (
            self.unibody_foot_x[1]
            - self.motor_mount_service_adjustment
            - (self.unibody_chassis_mount_x[1] + self.motor_mount_washer_outer_diameter / 2.0)
        )

    def validate_motor_radial_adjustment(self, adjustment: float, *, powered: bool = False) -> None:
        lower, upper = self.motor_mount_powered_range if powered else self.motor_mount_physical_range
        if adjustment < lower - 1e-9 or adjustment > upper + 1e-9:
            mode = "powered" if powered else "physical service"
            raise ValueError(
                f"motor adjustment {adjustment:g} outside {mode} range "
                f"[{lower:g}, {upper:g}] mm"
            )

    # The existing carrier body itself is the race.  No added rail, bead,
    # head, neck, or tooth-flank rolling is permitted.
    separate_guide_feature: bool = False
    roller_contact_surface: str = "carrier_inner_root_land_below_tooth_face"
    carrier_race_radius: float = 131.60
    tooth_tip_radius: float = 129.00
    tooth_root_radius: float = 132.50
    tooth_tip_rolling_allowed: bool = False
    race_land_depth: float = 0.80
    contact_land_width: float = 0.60

    # Three towers: two fixed datums and one +/-0.25 mm radial setup tower.
    roller_axis_radius: float = 125.50
    roller_axis_adjustment: float = 0.25
    tower_preload_slot_travel: float = 0.50

    # Relieved asymmetric spool.  The small hub clears tooth tips; the broad
    # running land reaches only the smooth lower carrier land; the two deep
    # flanges capture the carrier axially without occupying its Z envelope.
    roller_bore_diameter: float = 4.06
    roller_axle_finished_diameter: float = 3.99
    roller_hub_outer_diameter: float = 6.00
    roller_running_outer_diameter: float = 12.10
    roller_flange_outer_diameter: float = 13.80
    roller_flange_thickness: float = 0.50
    roller_flange_axial_clearance: float = 0.15
    roller_nominal_contact_gap: float = 0.05
    roller_capture_radial_overlap: float = 0.80
    roller_spacer_lengths: tuple[float, float] = (1.25, 1.25)
    roller_spacer_outer_diameter: float = 6.00
    roller_spacer_bore_diameter: float = 4.20
    roller_thrust_washer_thickness: float = 0.20
    roller_thrust_washer_outer_diameter: float = 6.00
    roller_thrust_washer_bore_diameter: float = 4.20
    roller_step_fillet_radius: float = 0.30
    roller_edge_chamfer: float = 0.20

    # D4 x 25 axle and matching upper service hardware.
    tower_axle_nominal_diameter: float = 4.00
    tower_axle_clearance_diameter: float = 4.20
    tower_axle_z0: float = -5.00
    tower_axle_length: float = 25.00
    tower_upper_bushing_z_range: tuple[float, float] = (13.45, 14.75)
    tower_top_bridge_z_range: tuple[float, float] = (13.45, 14.75)
    tower_upper_bushing_outer_diameter: float = 5.20
    tower_upper_bushing_bore_diameter: float = 4.20
    tower_retainer_collar_z_range: tuple[float, float] = (15.00, 19.00)
    tower_retainer_collar_outer_diameter: float = 10.00

    @property
    def roller_stationary_outer_radius(self) -> float:
        return self.roller_axis_radius + self.roller_flange_outer_diameter / 2.0

    @property
    def roller_running_outer_radius(self) -> float:
        return self.roller_axis_radius + self.roller_running_outer_diameter / 2.0

    @property
    def roller_running_gap(self) -> float:
        return self.carrier_race_radius - self.roller_running_outer_radius

    @property
    def adjusted_roller_axis_radius_range(self) -> tuple[float, float]:
        return (
            self.roller_axis_radius - self.roller_axis_adjustment,
            self.roller_axis_radius + self.roller_axis_adjustment,
        )

    @property
    def adjusted_tooth_tip_clearance(self) -> float:
        return self.tooth_tip_radius - (
            self.roller_axis_radius
            + self.roller_axis_adjustment
            + self.roller_hub_outer_diameter / 2.0
        )

    def race_range(self, role: int) -> tuple[float, float]:
        z0, _ = self.carrier_layers[role]
        return z0, z0 + self.race_land_depth

    def contact_range(self, role: int) -> tuple[float, float]:
        z0, _ = self.carrier_layers[role]
        return z0 + 0.10, z0 + 0.70

    def roller_flange_ranges(self, role: int) -> tuple[tuple[float, float], tuple[float, float]]:
        z0, z1 = self.carrier_layers[role]
        return (
            (z0 - 0.65, z0 - self.roller_flange_axial_clearance),
            (z1 + self.roller_flange_axial_clearance, z1 + 0.65),
        )

    def roller_running_range(self, role: int) -> tuple[float, float]:
        return self.contact_range(role)

    def roller_range(self, role: int) -> tuple[float, float]:
        lower, upper = self.roller_flange_ranges(role)
        return lower[0], upper[1]

    @property
    def lower_thrust_washer_range(self) -> tuple[float, float]:
        z0 = self.roller_range(0)[0]
        return z0 - self.roller_thrust_washer_thickness, z0

    @property
    def upper_thrust_washer_range(self) -> tuple[float, float]:
        z1 = self.roller_range(2)[1]
        return z1, z1 + self.roller_thrust_washer_thickness


P3_V3_DIRECT_GEAR_RACE = P3V3DirectGearRaceGuidanceSpec()
