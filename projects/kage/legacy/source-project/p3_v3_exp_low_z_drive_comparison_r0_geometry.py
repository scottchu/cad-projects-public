"""Geometry for three KAGE low-Z packaging concepts.

The immutable locked STEP is imported as the geometric source of truth.  The
experiment deliberately reuses its exact ring/fins and output pinions rather
than rebuilding teeth from nominal dimensions.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from pathlib import Path

from build123d import Align, Box, Color, Compound, Cylinder, Location, Solid, import_step

from p3_v3_exp_low_z_drive_comparison_r0_spec import (
    P3_V3_EXP_LOW_Z_DRIVE_COMPARISON_R0 as P,
)


RING_TOKEN = "M1_260T_quadrant"
PINION_TOKEN = "16T_output_pinion"
ROLES = ("hour", "minute", "second")


def locked_step_sha256() -> str:
    return sha256(P.locked_step.read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def _locked_import() -> Compound:
    if locked_step_sha256() != P.locked_sha256:
        raise ValueError("locked direct-gear-race STEP hash changed")
    result = import_step(str(P.locked_step))
    result.label = "A_locked_direct_gear_race_reference"
    return result


def _children() -> list:
    # A Compound reparents Python child wrappers, so each factory needs fresh
    # wrappers.  Re-wrap the same immutable TopoDS solids (no costly geometric
    # copy) and retain the embedded STEP labels/colors.
    rows = []
    for child in _locked_import().children:
        clone = type(child)(child.wrapped)
        clone.label = child.label
        clone.color = child.color
        rows.append(clone)
    return rows


def _tag(shape, label: str, color: str):
    shape.label = label
    shape.color = Color(color)
    return shape


def _cylinder_at(x: float, y: float, z0: float, z1: float, diameter: float, label: str):
    part = Cylinder(
        diameter / 2.0,
        z1 - z0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z0)))
    return _tag(part, label, "#68737d")


def _disc_at(x: float, y: float, z0: float, height: float, diameter: float, label: str):
    return _cylinder_at(x, y, z0, z0 + height, diameter, label)


def _clone(child, *, label: str | None = None, move: Location | None = None):
    # build123d primitives such as Cylinder inherit Compound but expose their
    # geometry as one wrapped solid with no Python children.  Recursing solely
    # on isinstance() therefore creates an empty Compound.  Only recurse for a
    # genuine multi-child assembly.
    if child.children:
        result = Compound(children=[_clone(part) for part in child.children])
    else:
        result = Solid(child.wrapped)
    result.label = label or child.label
    result.color = child.color
    if move is not None:
        result = result.moved(move)
        result.label = label or child.label
        result.color = child.color
    return result


def _bounds(shape) -> tuple[float, float, float, float, float, float]:
    b = shape.bounding_box()
    return (b.min.X, b.min.Y, b.min.Z, b.max.X, b.max.Y, b.max.Z)


def component_signature(shape, *, tokens: tuple[str, ...] = (RING_TOKEN, PINION_TOKEN)) -> dict:
    """Geometry signature for the exact parts that may never be redesigned."""

    rows = {}
    for child in shape.children:
        label = child.label or ""
        if not any(token in label for token in tokens):
            continue
        rows[label] = {
            "bounds": tuple(round(v, 6) for v in _bounds(child)),
            "volume": round(sum(s.volume for s in child.solids()), 6),
            "solids": len(child.solids()),
        }
    return rows


def make_locked_reference_A() -> Compound:
    """Concept A: exact locked baseline used as the Z-budget reference."""

    result = Compound(children=_children(), label="A_locked_z_budget_section")
    return result


def _is_removed_for_flush_hardware(label: str) -> bool:
    return any(
        token in label
        for token in (
            "M3x10_screw_REFERENCE",
            "M3_AF5p50_nut_REFERENCE",
            "M3_mount_screw_",
            "M3_washer_",
            "M3_hex_nut_",
            "D7x0p50_washer_REFERENCE",
            "D4x25_polished_axle_REFERENCE",
            "purchased_D4x10x4_metal_M2_set_screw_collar_REFERENCE",
            "M2_collar_set_screw_REFERENCE",
            "D4x40_output_shaft_REFERENCE",
            "lower_datum_split_collar_REFERENCE",
        )
    )


def _original_fastener_axes(source: list, member_token: str) -> list[tuple[float, float, str]]:
    rows = []
    for child in source:
        label = child.label or ""
        is_axis = (
            ("M3x10_screw_REFERENCE" in label or "M3_mount_screw_" in label)
            and member_token in label
        )
        if not is_axis:
            continue
        box = child.bounding_box()
        rows.append((box.center().X, box.center().Y, label))
    return rows


def _pocketed_member(child, axes: list[tuple[float, float, str]]):
    """Cut explicit shank/head/nut clearance into one frozen stationary member."""

    box = child.bounding_box()
    z0 = box.min.Z
    z1 = z0 + 6.70
    result = child
    for x, y, _ in axes:
        bore = Cylinder(
            P.flush_fastener_clearance_diameter / 2.0,
            z1 - z0 + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, z0 - 0.2)))
        head = Cylinder(
            P.flush_fastener_pocket_diameter / 2.0,
            P.flush_fastener_pocket_depth + 0.1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, z0 - 0.05)))
        nut = Cylinder(
            (P.flush_fastener_nut_af + 0.35) / 2.0,
            P.flush_fastener_washer_height + P.flush_fastener_nut_height + 0.15,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, z0 + 3.75)))
        result = result - bore - head - nut
    result.label = f"B_REAL_COUNTERBORED_{child.label}"
    result.color = child.color
    return result


def _roller_retainer_seat_relief(member, x: float, y: float):
    """Relieve only the two low-profile retainer seats in a tower yoke."""

    result = member
    seat_diameter = P.roller_retainer_diameter + 0.20
    for z0, z1 in ((-5.05, -4.55), (14.30, 14.80)):
        tool = Cylinder(
            seat_diameter / 2.0,
            z1 - z0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, z0)))
        result = result - tool
    result.label = member.label
    result.color = member.color
    return result


def _flush_fastener_stack(x: float, y: float, z0: float, source_label: str) -> list:
    """Low-profile communication hardware with face-to-face, not overlapping, pieces."""

    head = _disc_at(
        x,
        y,
        z0,
        P.flush_fastener_head_height,
        P.flush_fastener_head_diameter,
        f"B_low_profile_head_{source_label}",
    )
    shank = _cylinder_at(
        x,
        y,
        z0 + P.flush_fastener_head_height,
        z0 + 3.75,
        3.0,
        f"B_low_profile_shank_{source_label}",
    )
    washer = _disc_at(
        x,
        y,
        z0 + 3.75,
        P.flush_fastener_washer_height,
        P.flush_fastener_washer_diameter,
        f"B_opposite_washer_{source_label}",
    )
    nut = _disc_at(
        x,
        y,
        z0 + 3.75 + P.flush_fastener_washer_height,
        P.flush_fastener_nut_height,
        P.flush_fastener_nut_af,
        f"B_captive_nut_reference_{source_label}",
    )
    return [head, shank, washer, nut]


def _retained_output_shaft(
    x: float, y: float, role: str, z0: float, z1: float
) -> list:
    shaft = _cylinder_at(
        x, y, z0 + P.shaft_retainer_height, z1 - P.shaft_retainer_height,
        P.captive_axle_diameter, f"B_{role}_short_captive_output_shaft",
    )
    lower = _disc_at(
        x, y, z0, P.shaft_retainer_height, P.shaft_retainer_diameter,
        f"B_{role}_output_lower_shoulder",
    )
    upper = _disc_at(
        x, y, z1 - P.shaft_retainer_height, P.shaft_retainer_height,
        P.shaft_retainer_diameter, f"B_{role}_output_low_snap_retainer",
    )
    return [shaft, lower, upper]


def _retained_roller_axle(x: float, y: float, source_label: str) -> list:
    z0, z1 = -5.00, 14.75
    axle = _cylinder_at(
        x, y, z0 + P.roller_retainer_height, z1 - P.roller_retainer_height,
        P.captive_axle_diameter, f"B_blind_captive_roller_axle_{source_label}",
    )
    lower = _disc_at(
        x, y, z0, P.roller_retainer_height, P.roller_retainer_diameter,
        f"B_roller_lower_shoulder_{source_label}",
    )
    upper = _disc_at(
        x, y, z1 - P.roller_retainer_height, P.roller_retainer_height,
        P.roller_retainer_diameter, f"B_roller_low_snap_retainer_{source_label}",
    )
    return [axle, lower, upper]


def make_flush_hardware_B() -> Compound:
    """Concept B: locked drive with real counterbores and positive axial capture."""

    source = _children()
    kept = []

    # Replace the actual imported yokes with pocketed derivatives at every
    # frozen M3 axis.  All moving datums and the radial slots remain untouched.
    member_axes: dict[str, list[tuple[float, float, str]]] = {}
    for role in ROLES:
        token = f"direct_race_{role}_"
        member_axes[token] = _original_fastener_axes(source, token)
    for tower in ("tower_1_", "tower_2_", "tower_3_"):
        member_axes[tower] = _original_fastener_axes(source, tower)

    for child in source:
        label = child.label or ""
        if _is_removed_for_flush_hardware(label):
            continue
        token = next((token for token in member_axes if token in label and "yoke" in label), None)
        if token:
            replacement = _pocketed_member(child, member_axes[token])
            if token.startswith("tower_"):
                axle = next(
                    part for part in source
                    if token in (part.label or "")
                    and "D4x25_polished_axle_REFERENCE" in (part.label or "")
                )
                center = axle.bounding_box().center()
                replacement = _roller_retainer_seat_relief(replacement, center.X, center.Y)
            kept.append(replacement)
        else:
            kept.append(child)

    for token, axes in member_axes.items():
        member = next(
            child for child in source if token in (child.label or "") and "yoke" in (child.label or "")
        )
        z0 = member.bounding_box().min.Z
        for x, y, source_label in axes:
            kept.extend(_flush_fastener_stack(x, y, z0, source_label))

    for child in source:
        label = child.label or ""
        if "D4x25_polished_axle_REFERENCE" in label:
            b = child.bounding_box()
            kept.extend(_retained_roller_axle(b.center().X, b.center().Y, label))

    role_z = {
        "hour": (-25.30, 4.05),
        "minute": (-23.15, 9.60),
        "second": (-21.00, 15.15),
    }
    for child in source:
        label = child.label or ""
        if "D4x40_output_shaft_REFERENCE" not in label:
            continue
        role = next(role for role in ROLES if f"_{role}_" in label)
        b = child.bounding_box()
        kept.extend(_retained_output_shaft(b.center().X, b.center().Y, role, *role_z[role]))

    return Compound(children=kept, label="B_flush_hardware_captive_axle")


def _role(label: str) -> str | None:
    return next((role for role in ROLES if f"_{role}_" in label), None)


def _role_ring_labels(role: str) -> tuple[str, ...]:
    quadrants = {"hour": ("Q1", "Q4"), "minute": ("Q2",), "second": ("Q3",)}[role]
    return tuple(f"direct_race_{role}_M1_260T_quadrant_{quadrant}_" for quadrant in quadrants)


def _coupon_members_for_role(source: list, role: str) -> list:
    tokens = (
        f"direct_race_{role}_ONE_CONNECTED",
        f"direct_race_{role}_NEMA8_",
        f"direct_race_{role}_horizontal_16T_miter_",
        f"direct_race_{role}_vertical_16T_miter_",
        f"direct_race_{role}_lower_MR84ZZ_",
        f"direct_race_{role}_upper_MR84ZZ_",
        f"direct_race_{role}_ONLY_role_height_spacer_",
        f"direct_race_{role}_16T_output_pinion_",
    )
    return [child for child in source if any(token in (child.label or "") for token in tokens)]


def _local_ring_segment(source: list, role: str):
    """Crop the locked carrier around its frozen output-pinion mesh station."""

    ring_parts = [
        child for child in source
        if f"direct_race_{role}_M1_260T_quadrant_" in (child.label or "")
    ]
    pinion = next(
        child for child in source
        if f"direct_race_{role}_16T_output_pinion_" in (child.label or "")
    )
    pb = pinion.bounding_box()
    tool = Box(54.0, 54.0, 40.0, align=(Align.CENTER, Align.CENTER, Align.CENTER)).moved(
        Location((pb.center().X, pb.center().Y, pb.center().Z))
    )
    cut = Compound(children=[_clone(part) for part in ring_parts]).intersect(tool)
    cut_solids = [] if cut is None else list(cut.solids())
    if not cut_solids:
        raise ValueError(f"failed to crop {role} locked ring plane")
    segment = Compound(children=cut_solids)
    segment.label = f"C_{role}_local_ring_segment_from_locked_teeth_and_carrier"
    segment.color = ring_parts[0].color
    return segment


def make_role_local_coupon_C() -> Compound:
    """Concept C: three honest station coupons; explicitly not a complete clock.

    Each coupon keeps one frozen motor/yoke/miter/output-pinion datum and the
    relevant exact ring quadrant plane.  A local mounting island and a retained
    shaft make the packaging legible, but no annular chassis or full-depth claim
    is implied.
    """

    source = _children()
    members = []
    shifts = {"hour": -P.coupon_spacing_x, "minute": 0.0, "second": P.coupon_spacing_x}
    tower_for_role = {"hour": "tower_1_", "minute": "tower_2_", "second": "tower_3_"}
    shaft_z = {"hour": (-25.30, 4.05), "minute": (-23.15, 9.60), "second": (-21.00, 15.15)}

    for role in ROLES:
        role_members = []
        dx = shifts[role]
        move = Location((dx, 0, 0))
        role_parts = _coupon_members_for_role(source, role)
        role_members.extend(
            _clone(part, label=f"C_{role}_FROZEN_DATUM_{part.label}", move=move)
            for part in role_parts
            if "ONE_CONNECTED" not in (part.label or "")
        )
        role_members.append(_clone(_local_ring_segment(source, role), move=move))

        # One existing roller station demonstrates the corresponding captured
        # ring plane.  The axle/collar references are replaced by low retainers.
        tower_token = tower_for_role[role]
        tower_parts = [
            child for child in source
            if tower_token in (child.label or "")
            and not any(token in (child.label or "") for token in (
                "D4x25_polished_axle_REFERENCE", "purchased_D4x10x4", "M2_collar",
                "M3_mount_screw_", "M3_washer_", "M3_hex_nut_",
            ))
        ]
        role_members.extend(
            _clone(part, label=f"C_{role}_ROLLER_SUPPORT_{part.label}", move=move)
            for part in tower_parts
            if "yoke" not in (part.label or "")
        )

        shaft = next(
            child for child in source
            if f"direct_race_{role}_D4x40_output_shaft_REFERENCE" in (child.label or "")
        )
        sb = shaft.bounding_box()
        for part in _retained_output_shaft(sb.center().X, sb.center().Y, role, *shaft_z[role]):
            role_members.append(_clone(part, label=(part.label or "").replace("B_", "C_"), move=move))

        axle = next(
            child for child in source
            if tower_token in (child.label or "") and "D4x25_polished_axle_REFERENCE" in (child.label or "")
        )
        ab = axle.bounding_box()
        for part in _retained_roller_axle(ab.center().X, ab.center().Y, axle.label or ""):
            role_members.append(_clone(part, label=(part.label or "").replace("B_", f"C_{role}_"), move=move))

        yoke_boxes = [part.bounding_box() for part in role_parts if "ONE_CONNECTED" in (part.label or "")]
        tower_boxes = [part.bounding_box() for part in tower_parts if "yoke" in (part.label or "")]
        boxes = yoke_boxes + tower_boxes
        xmin = min(b.min.X for b in boxes) - 5.0
        xmax = max(b.max.X for b in boxes) + 5.0
        ymin = min(b.min.Y for b in boxes) - 5.0
        ymax = max(b.max.Y for b in boxes) + 5.0
        # Seat the local island against the higher of the two frozen feet; the
        # lower foot already extends through this plane.  A 0.10 mm union lap
        # makes the communication support one actual connected solid.
        z_top = max(b.min.Z for b in boxes)
        pad = Box(
            xmax - xmin,
            ymax - ymin,
            P.local_station_chassis_thickness + 0.10,
            align=(Align.MIN, Align.MIN, Align.MAX),
        ).moved(Location((xmin + dx, ymin, z_top + 0.10)))
        support = pad
        for support_part in [
            *(part for part in role_parts if "ONE_CONNECTED" in (part.label or "")),
            *(part for part in tower_parts if "yoke" in (part.label or "")),
        ]:
            support = support + _clone(support_part, move=move)

        # Communication-solid clearance, not decorative positive props: the
        # referenced motor must sit inside the yoke without occupying its
        # material, and the retained roller axle/shoulders need a continuous
        # bore plus two shallow seats.
        motor = next(part for part in role_parts if "NEMA8_REFERENCE" in (part.label or ""))
        mb = motor.bounding_box()
        motor_clearance = Box(
            mb.size.X + 0.40,
            mb.size.Y + 0.40,
            mb.size.Z + 0.40,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((mb.center().X + dx, mb.center().Y, mb.center().Z)))
        support = support - motor_clearance

        roller_x = ab.center().X + dx
        roller_y = ab.center().Y
        roller_bore = Cylinder(
            (P.captive_axle_diameter + 0.20) / 2.0,
            20.10,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((roller_x, roller_y, -5.15)))
        support = support - roller_bore
        support = _roller_retainer_seat_relief(support, roller_x, roller_y)
        # The clearance subtraction can detach a tiny non-load-bearing chip at
        # one inherited corner of the locked yoke.  It is not a mount and must
        # not survive as a floating communication solid.
        support_solids = sorted(support.solids(), key=lambda solid: solid.volume, reverse=True)
        support = Solid(support_solids[0].wrapped)
        support.label = f"C_{role}_connected_mount_and_capture_complete_clock_false"
        support.color = Color("#86939d")
        role_members.append(support)
        members.append(Compound(children=role_members, label=f"C_role_coupon_{role}"))

    result = Compound(children=members, label="C_role_local_station_coupons_complete_clock_FALSE")
    return result


# Compatibility alias for the existing STEP generator filename.  The geometry
# is now the truthful coupon comparison above, not the rejected shallow annulus.
def make_short_bevel_C() -> Compound:
    return make_role_local_coupon_C()


def make_side_by_side_comparison() -> Compound:
    # Place the concepts from their *actual* source bounding boxes.  Concept C
    # is a three-coupon communication model and is wider than a complete clock,
    # so a fixed nominal spacing can silently overlap it with B.
    source_a = make_locked_reference_A()
    source_b = make_flush_hardware_B()
    source_c = make_short_bevel_C()
    box_a = source_a.bounding_box()
    box_b = source_b.bounding_box()
    box_c = source_c.bounding_box()
    move_a_x = box_b.min.X - P.comparison_min_gap_x - box_a.max.X
    move_c_x = box_b.max.X + P.comparison_min_gap_x - box_c.min.X
    concepts = [
        source_a.moved(Location((move_a_x, 0, 0))),
        source_b,
        source_c.moved(Location((move_c_x, 0, 0))),
    ]
    concepts[0].label = "A_locked_z_budget_section_at_left"
    concepts[1].label = "B_flush_hardware_captive_axle_at_center"
    concepts[2].label = "C_role_local_short_bevel_station_at_right"
    return Compound(children=concepts, label="KAGE_low_Z_A_B_C_side_by_side")


def envelope_z(shape) -> tuple[float, float, float]:
    box = shape.bounding_box()
    return (box.min.Z, box.max.Z, box.size.Z)
