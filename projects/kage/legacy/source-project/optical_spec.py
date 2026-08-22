"""Pure optical, clock, packaging, warning, and scenario calculations.

The browser remains dependency-free. This Python contract exists for CLI use,
repeatable design studies, and regression tests.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from math import atan, degrees, isfinite, pi, radians, tan
from typing import Any, Mapping


def _positive(name: str, value: float) -> float:
    value = float(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if value < 0:
        raise ValueError(f"{name} cannot be negative")
    return value


def _source_and_plane(source_z: float, point_z: float, *, point_name: str = "point z") -> tuple[float, float]:
    source = _positive("source z", source_z)
    point = float(point_z)
    if not 0 < point < source:
        raise ValueError(f"{point_name} must obey 0 < z < source z")
    return source, point


def projected_radius(source_z: float, fin_radius: float, point_z: float) -> float:
    """Project one constant-radius upright-fin point onto the z=0 wall."""
    source, point = _source_and_plane(source_z, point_z)
    radius = _nonnegative("fin radius", fin_radius)
    return radius * source / (source - point)


def fin_z_for_projected_radius(source_z: float, fin_radius: float, projected_radius_value: float) -> float:
    """Return the upright-fin z coordinate that projects to a wall radius."""
    source = _positive("source z", source_z)
    radius = _positive("fin radius", fin_radius)
    projected = _positive("projected radius", projected_radius_value)
    if projected <= radius:
        raise ValueError("projected radius must exceed fin radius")
    point = source * (1 - radius / projected)
    _source_and_plane(source, point)
    return point


def fin_shadow_interval(source_z: float, fin_radius: float, base_z: float, tip_z: float) -> dict[str, float]:
    """Project a constant-radius axial fin into its radial wall-shadow interval."""
    if float(tip_z) <= float(base_z):
        raise ValueError("fin tip z must be greater than base z")
    start = projected_radius(source_z, fin_radius, base_z)
    tip = projected_radius(source_z, fin_radius, tip_z)
    return {"start_radius": start, "tip_radius": tip, "shadow_length": tip - start}


def projected_tangential_width(source_z: float, physical_width: float, point_z: float) -> float:
    source, point = _source_and_plane(source_z, point_z)
    width = _nonnegative("physical width", physical_width)
    return width * source / (source - point)


def projected_mask_radius(source_z: float, mask_radius: float, mask_z: float) -> float:
    return projected_radius(source_z, mask_radius, mask_z)


def required_mask_radius(source_z: float, projected_radius_value: float, mask_z: float) -> float:
    source, point = _source_and_plane(source_z, mask_z, point_name="mask z")
    projected = _nonnegative("projected radius", projected_radius_value)
    return projected * (source - point) / source


def cone_radius(source_z: float, projected_wall_radius: float, plane_z: float) -> float:
    source = _positive("source z", source_z)
    wall_radius = _nonnegative("projected wall radius", projected_wall_radius)
    plane = float(plane_z)
    if not 0 <= plane < source:
        raise ValueError("cone plane z must obey 0 <= z < source z")
    return wall_radius * (source - plane) / source


LED_CLEAR_FULL_ANGLE_MIN_DEGREES = 110.0
LED_CLEAR_FULL_ANGLE_MAX_DEGREES = 180.0
LED_CLEAR_FULL_ANGLE_DEFAULT_DEGREES = 150.0


def normalize_led_full_angle_degrees(full_angle_degrees: float) -> float:
    """Clamp the user-facing full cone angle to the simulator's LED contract."""
    value = float(full_angle_degrees)
    if not isfinite(value):
        return LED_CLEAR_FULL_ANGLE_DEFAULT_DEGREES
    return max(LED_CLEAR_FULL_ANGLE_MIN_DEGREES, min(LED_CLEAR_FULL_ANGLE_MAX_DEGREES, value))


def full_angle_to_half_angle_degrees(full_angle_degrees: float) -> float:
    """Convert the normalized user-facing full cone to the optical half-angle."""
    return normalize_led_full_angle_degrees(full_angle_degrees) / 2.0


def baffle_clear_radius_for_full_angle(
    distance_from_source: float,
    full_angle_degrees: float,
    margin: float,
) -> float | None:
    """Return baffle clearance, or ``None`` for the unbounded 180-degree field."""
    half_angle = full_angle_to_half_angle_degrees(full_angle_degrees)
    if half_angle == 90.0:
        _nonnegative("distance from source", distance_from_source)
        _nonnegative("baffle margin", margin)
        return None
    return baffle_clear_radius(distance_from_source, half_angle, margin)


def baffle_clear_radius(distance_from_source: float, half_angle_degrees: float, margin: float) -> float:
    distance = _nonnegative("distance from source", distance_from_source)
    angle = float(half_angle_degrees)
    if not 0 < angle < 90:
        raise ValueError("baffle half angle must be between 0 and 90 degrees")
    clearance = _nonnegative("baffle margin", margin)
    return distance * tan(radians(angle)) + clearance


def radial_envelope_clearance(inner_envelope: tuple[float, float], outer_envelope: tuple[float, float]) -> float:
    inner_lo, inner_hi = map(float, inner_envelope)
    outer_lo, outer_hi = map(float, outer_envelope)
    if min(inner_lo, outer_lo) < 0 or inner_lo > inner_hi or outer_lo > outer_hi:
        raise ValueError("radial envelopes must be ordered nonnegative intervals")
    return outer_lo - inner_hi


def project_point_to_wall(
    source: tuple[float, float, float], point: tuple[float, float, float]
) -> dict[str, Any]:
    """Project an arbitrary 3D point to z=0, reporting off-axis source use."""
    sx, sy, sz = map(float, source)
    px, py, pz = map(float, point)
    sz, pz = _source_and_plane(sz, pz)
    scale = sz / (sz - pz)
    return {
        "x": sx + scale * (px - sx),
        "y": sy + scale * (py - sy),
        "scale": scale,
        "source_axis_offset_warning": abs(sx) > 1e-12 or abs(sy) > 1e-12,
    }


def carrier_radii(carrier_pitch: float, hour_radius: float = 30.0) -> dict[str, float]:
    """Derive the three constant-radius carrier lanes from one pitch."""
    pitch = _positive("carrier pitch", carrier_pitch)
    hour = _positive("hour carrier radius", hour_radius)
    return {"hour": hour, "minute": hour + pitch, "second": hour + 2 * pitch}


def led_nearest_fin_gap(source_z: float, fins: Mapping[str, Mapping[str, float]]) -> float:
    """Return the axial gap from the LED plane to the nearest fin tip."""
    source = _positive("source z", source_z)
    tips = [float(fin["tip_z"]) for fin in fins.values()]
    if not tips:
        raise ValueError("at least one fin tip is required")
    return source - max(tips)


def optical_depth(source_z: float, glare_cap_offset: float = 6.0) -> float:
    """Return the optical extent from the wall through the room-side glare cap."""
    return _positive("source z", source_z) + _positive("glare cap offset", glare_cap_offset)


UPRIGHT_FIN_REFERENCE = {
    "source_z": 40.0,
    "wall_z": 0.0,
    "mask_z": 6.0,
    "projected_mask_radius": 50.0,
    "fin_profile_scale": 1.0,
    "fin_radial_thickness": 1.6,
    "carrier_pitch": 4.75,
    "fin_profiles": {
        "hour": {"stem_width": 4.8, "crown_width": 3.2, "crown_height": 0.8, "crown_style": "round"},
        "minute": {"stem_width": 3.2, "crown_width": 1.6, "crown_height": 0.8, "crown_style": "chamfer"},
        "second": {"stem_width": 1.6, "crown_width": 0.4, "crown_height": 0.6, "crown_style": "spear"},
    },
    "fins": {
        "hour": {"radius": 30.0, "base_z": 15.0, "tip_z": 25.882352941, "target_tip_radius": 85.0},
        "minute": {"radius": 34.75, "base_z": 11.041666667, "tip_z": 27.363636364, "target_tip_radius": 110.0},
        "second": {"radius": 39.5, "base_z": 7.083333333, "tip_z": 27.846153846, "target_tip_radius": 130.0},
    },
}


def upright_fin_reference(source_z: float = 40.0, carrier_pitch: float = 4.75) -> dict[str, Any]:
    """Return the frozen upright-fin optical model, re-derived for source z."""
    source = _positive("source z", source_z)
    pitch = max(4.0, min(5.75, float(carrier_pitch)))
    radii = carrier_radii(pitch)
    start_target = 48.0
    fins: dict[str, Any] = {}
    for name, values in UPRIGHT_FIN_REFERENCE["fins"].items():
        radius = radii[name]
        base_z = fin_z_for_projected_radius(source, radius, start_target)
        tip_z = fin_z_for_projected_radius(source, radius, values["target_tip_radius"])
        interval = fin_shadow_interval(source, radius, base_z, tip_z)
        profile = UPRIGHT_FIN_REFERENCE["fin_profiles"][name]
        crown_base_z = max(base_z, tip_z - profile["crown_height"])
        fins[name] = {
            "orientation": "constant-radius-tangential-axial-upright-fin",
            "radius": radius,
            "base_z": base_z,
            "tip_z": tip_z,
            "height": tip_z - base_z,
            "radial_thickness": UPRIGHT_FIN_REFERENCE["fin_radial_thickness"],
            **profile,
            "projected_base_width": projected_tangential_width(source, profile["stem_width"], base_z),
            "projected_crown_base_width": projected_tangential_width(source, profile["stem_width"], crown_base_z),
            "projected_tip_width": projected_tangential_width(source, profile["crown_width"], tip_z),
            **interval,
        }
    mask_z = UPRIGHT_FIN_REFERENCE["mask_z"]
    projected_mask = UPRIGHT_FIN_REFERENCE["projected_mask_radius"]
    return {
        "architecture": "v0r2-identifiable-upright-rim-fin",
        "wall_z": 0.0,
        "source_z": source,
        "optical_depth": optical_depth(source),
        "glare_cap_offset": 6.0,
        "mask_z": mask_z,
        "projected_mask_radius": projected_mask,
        "mask_physical_radius": required_mask_radius(source, projected_mask, mask_z),
        "carrier_pitch": pitch,
        "carrier_radii": radii,
        "fin_profile_scale": UPRIGHT_FIN_REFERENCE["fin_profile_scale"],
        "fins": fins,
        "radial_clearances": {
            "hour_to_minute": pitch - UPRIGHT_FIN_REFERENCE["fin_radial_thickness"],
            "minute_to_second": pitch - UPRIGHT_FIN_REFERENCE["fin_radial_thickness"],
        },
        "led_nearest_fin_gap": led_nearest_fin_gap(source, fins),
        "flat_xy_blades_allowed": False,
    }


def projection_distances(source_hand_mm: float, hand_wall_mm: float) -> dict[str, float]:
    """Return L, W, D=L+W, and pinhole magnification M=D/L."""
    source_hand = _positive("source-to-hand distance L", source_hand_mm)
    hand_wall = _nonnegative("hand-to-wall distance W", hand_wall_mm)
    source_wall = source_hand + hand_wall
    return {
        "source_hand_mm": source_hand,
        "hand_wall_mm": hand_wall,
        "source_wall_mm": source_wall,
        "magnification": source_wall / source_hand,
    }


def projected_hand(
    length_mm: float,
    width_mm: float,
    source_hand_mm: float,
    hand_wall_mm: float,
) -> dict[str, float]:
    distances = projection_distances(source_hand_mm, hand_wall_mm)
    length = _nonnegative("hand length", length_mm)
    width = _nonnegative("hand width", width_mm)
    return {
        "physical_length_mm": length,
        "physical_width_mm": width,
        "projected_length_mm": length * distances["magnification"],
        "projected_width_mm": width * distances["magnification"],
    }


def projected_blocker(
    *,
    name: str,
    shape: str,
    radial_length_mm: float,
    width_mm: float,
    source_hand_mm: float,
    hand_wall_mm: float,
    occluder_radius_mm: float = 0.0,
    shape_parameters: Mapping[str, float] | None = None,
    physical_length_range_mm: tuple[float, float] | None = None,
) -> dict[str, Any]:
    if not name.strip() or not shape.strip():
        raise ValueError("blocker name and shape are required")
    projection = projected_hand(radial_length_mm, width_mm, source_hand_mm, hand_wall_mm)
    occluder_radius = _nonnegative("occluder radius", occluder_radius_mm)
    if physical_length_range_mm is not None:
        low, high = physical_length_range_mm
        if low <= 0 or high < low or not low <= radial_length_mm <= high:
            raise ValueError("blocker radial length must lie inside its declared range")
    return {
        "name": name,
        "shape": shape,
        "physical_radial_length_mm": projection["physical_length_mm"],
        "physical_width_mm": projection["physical_width_mm"],
        "projected_length_mm": projection["projected_length_mm"],
        "projected_width_mm": projection["projected_width_mm"],
        "occluder_radius_mm": occluder_radius,
        "visible_length_mm": max(0.0, projection["projected_length_mm"] - occluder_radius),
        "shape_parameters": dict(shape_parameters or {}),
        "physical_length_range_mm": list(physical_length_range_mm) if physical_length_range_mm else None,
    }


def projected_ring_carrier(
    *,
    name: str,
    carrier_inner_radius_mm: float,
    carrier_outer_radius_mm: float,
    blocker_radial_start_mm: float,
    blocker_radial_end_mm: float,
    blocker_width_mm: float,
    blocker_shape: str,
    axial_plane_offset_mm: float,
    source_hand_mm: float,
    hand_wall_mm: float,
    effective_occluder_radius_mm: float,
    optical_angle_degrees: float = 0.0,
    effective_aperture_mm: float = 0.8,
    carrier_thickness_mm: float = 1.2,
    axial_gap_mm: float = 0.4,
    exposed_drive_radius_mm: float = 49.5,
    clear_center_radius_mm: float = 18.0,
    pivot_offset_mm: float = 0.0,
) -> dict[str, Any]:
    """Project a blocker carried by a hollow concentric ring.

    Positive axial offset moves the blocker plane toward the wall, increasing
    source-to-blocker distance and reducing blocker-to-wall distance.  The
    optical angle describes the shadow state only; it is not a gear, bearing,
    motor, or drive-model input.
    """
    if not name.strip() or not blocker_shape.strip():
        raise ValueError("carrier name and blocker shape are required")
    inner = _nonnegative("carrier inner radius", carrier_inner_radius_mm)
    outer = _positive("carrier outer radius", carrier_outer_radius_mm)
    radial_start = _nonnegative("blocker radial start", blocker_radial_start_mm)
    radial_end = _positive("blocker radial end", blocker_radial_end_mm)
    width = _positive("blocker width", blocker_width_mm)
    occluder = _nonnegative("effective occluder radius", effective_occluder_radius_mm)
    aperture = _nonnegative("effective aperture", effective_aperture_mm)
    thickness = _positive("carrier thickness", carrier_thickness_mm)
    axial_gap = _nonnegative("axial gap", axial_gap_mm)
    exposed_radius = _positive("exposed drive radius", exposed_drive_radius_mm)
    clear_center = _positive("clear center radius", clear_center_radius_mm)
    pivot_offset = _nonnegative("pivot offset", pivot_offset_mm)
    offset = float(axial_plane_offset_mm)
    if inner >= outer:
        raise ValueError("carrier outer radius must exceed inner radius")
    if radial_start >= radial_end:
        raise ValueError("blocker radial end must exceed radial start")
    if radial_start > outer or radial_end < inner:
        raise ValueError("blocker must overlap its carrier radial envelope")
    if clear_center > inner:
        raise ValueError("clear center radius cannot exceed carrier inner radius")
    if exposed_radius < outer:
        raise ValueError("exposed drive radius cannot be smaller than carrier outer radius")
    if not -source_hand_mm < offset < hand_wall_mm:
        raise ValueError("axial plane offset must keep both optical distances positive")
    effective_source_hand = source_hand_mm + offset
    effective_hand_wall = hand_wall_mm - offset
    distances = projection_distances(effective_source_hand, effective_hand_wall)
    projected_start = radial_start * distances["magnification"]
    projected_end = radial_end * distances["magnification"]
    projected_drive_radius = exposed_radius * distances["magnification"]
    visible_start = max(projected_start, occluder)
    visible_end = max(projected_end, visible_start)
    hide_margin = occluder - projected_drive_radius
    failure_flags = {
        "donut_shadow": occluder > 0 and hide_margin < 0,
        "collision": axial_gap < 0.4,
        "vignetting": aperture / 2.0 >= clear_center,
        "glare": aperture > 1.0,
        "pivot_drift": pivot_offset > 0.5,
        "central_obstruction": clear_center > inner,
    }
    return {
        "name": name,
        "movement_type": "annular-ring-carrier",
        "carrier_inner_radius_mm": inner,
        "carrier_outer_radius_mm": outer,
        "carrier_thickness_mm": thickness,
        "axial_gap_mm": axial_gap,
        "exposed_drive_radius_mm": exposed_radius,
        "clear_center_radius_mm": clear_center,
        "blocker_radial_start_mm": radial_start,
        "blocker_radial_end_mm": radial_end,
        "blocker_width_mm": width,
        "blocker_shape": blocker_shape,
        "axial_plane_offset_mm": offset,
        "optical_angle_degrees": float(optical_angle_degrees) % 360.0,
        "angle_semantics": "optical-blocker-angle-only-not-drive-geometry",
        "effective_source_hand_mm": effective_source_hand,
        "effective_hand_wall_mm": effective_hand_wall,
        "magnification": distances["magnification"],
        "effective_aperture_mm": aperture,
        "penumbra_mm": penumbra_width(aperture, effective_source_hand, effective_hand_wall),
        "projected_radial_start_mm": projected_start,
        "projected_radial_end_mm": projected_end,
        "projected_tip_mm": projected_end,
        "projected_drive_radius_mm": projected_drive_radius,
        "effective_occluder_radius_mm": occluder,
        "visible_projected_start_mm": visible_start,
        "visible_projected_end_mm": visible_end,
        "visible_projected_span_mm": max(0.0, projected_end - max(projected_start, occluder)),
        "visible_length_mm": max(0.0, projected_end - max(projected_start, occluder)),
        "carrier_hide_margin_mm": hide_margin,
        "pivot_offset_mm": pivot_offset,
        "failure_flags": failure_flags,
        "all_clear": not any(failure_flags.values()),
    }


def projected_mask(
    *,
    physical_radius_mm: float,
    mask_z_mm: float,
    source_z_mm: float,
    wall_z_mm: float = 0.0,
) -> dict[str, float]:
    """Project a real fixed mask onto the wall using explicit axial planes.

    Coordinates are measured from the wall toward the room.  The source must
    be room-side of the mask.  A decorative shell on the viewer side is never
    accepted as the wall-facing occlusion mask.
    """
    radius = _positive("mask physical radius", physical_radius_mm)
    source_z = _positive("source z", source_z_mm)
    mask_z = _positive("mask z", mask_z_mm)
    wall_z = float(wall_z_mm)
    source_wall = source_z - wall_z
    source_mask = source_z - mask_z
    if not wall_z < mask_z < source_z:
        raise ValueError("planes must satisfy wall_z < mask_z < source_z")
    magnification = source_wall / source_mask
    return {
        "physical_radius_mm": radius,
        "physical_diameter_mm": radius * 2.0,
        "mask_z_mm": mask_z,
        "source_z_mm": source_z,
        "wall_z_mm": wall_z,
        "source_mask_mm": source_mask,
        "source_wall_mm": source_wall,
        "magnification": magnification,
        "projected_radius_mm": radius * magnification,
        "projected_diameter_mm": radius * magnification * 2.0,
    }


def required_ray_clear_radius_mm(
    *,
    blocker_tip_radius_mm: float,
    blocker_z_mm: float,
    source_z_mm: float,
    sample_z_mm: float,
) -> float:
    """Radius of the source-to-tip ray at an axial sample plane."""
    tip = _positive("blocker tip radius", blocker_tip_radius_mm)
    blocker_z = _positive("blocker z", blocker_z_mm)
    source_z = _positive("source z", source_z_mm)
    sample_z = float(sample_z_mm)
    if not sample_z < source_z or not blocker_z < source_z:
        raise ValueError("sample and blocker planes must lie wall-side of source")
    return tip * (source_z - sample_z) / (source_z - blocker_z)


def flared_pod_clearance(
    *,
    blocker_tip_radius_mm: float,
    blocker_z_mm: float,
    source_z_mm: float,
    pod_clear_radius_mm: float,
    pod_rear_z_mm: float,
) -> dict[str, float | bool]:
    """Prove where a room-side pod must end to avoid clipping the ray cone."""
    clear_radius = _positive("pod clear radius", pod_clear_radius_mm)
    rear_z = float(pod_rear_z_mm)
    required_at_rear = required_ray_clear_radius_mm(
        blocker_tip_radius_mm=blocker_tip_radius_mm,
        blocker_z_mm=blocker_z_mm,
        source_z_mm=source_z_mm,
        sample_z_mm=rear_z,
    )
    source_blocker = source_z_mm - blocker_z_mm
    minimum_end_z = source_z_mm - clear_radius * source_blocker / blocker_tip_radius_mm
    return {
        "pod_clear_radius_mm": clear_radius,
        "pod_rear_z_mm": rear_z,
        "required_clear_radius_at_pod_rear_mm": required_at_rear,
        "minimum_room_side_pod_end_z_mm": minimum_end_z,
        "continuous_pod_clears_cone": clear_radius >= required_at_rear,
        "pod_must_end_before_cone_expands": clear_radius < required_at_rear,
    }


def required_full_field_angle_degrees(
    *,
    blocker_tip_radius_mm: float,
    source_blocker_mm: float,
) -> float:
    """Full optical cone required to illuminate a radial blocker tip."""
    tip = _positive("blocker tip radius", blocker_tip_radius_mm)
    distance = _positive("source-to-blocker distance", source_blocker_mm)
    return 2.0 * degrees(atan(tip / distance))


def projected_direct_shaft_disc(
    *,
    name: str,
    plane_z_mm: float,
    source_z_mm: float,
    wall_z_mm: float,
    carrier_outer_radius_mm: float,
    blocker_radial_start_mm: float,
    blocker_radial_end_mm: float,
    blocker_width_mm: float,
    blocker_shape: str,
    projected_mask_radius_mm: float,
    effective_aperture_mm: float = 0.8,
    required_hide_margin_mm: float = 5.0,
    optical_angle_degrees: float = 0.0,
) -> dict[str, Any]:
    """Project one quartz-shaft single tapered orbital blocker blade.

    This is the selected architecture: stock concentric quartz shafts directly
    carry separate discs.  It intentionally contains no hollow optical tunnel,
    printed gears, or invented shaft-bore dimensions.
    """
    if not name.strip() or not blocker_shape.strip():
        raise ValueError("disc name and blocker shape are required")
    source_z = _positive("source z", source_z_mm)
    plane_z = _positive("blocker plane z", plane_z_mm)
    wall_z = float(wall_z_mm)
    carrier_radius = _positive("carrier outer radius", carrier_outer_radius_mm)
    radial_start = _nonnegative("blocker radial start", blocker_radial_start_mm)
    radial_end = _positive("blocker radial end", blocker_radial_end_mm)
    width = _positive("blocker width", blocker_width_mm)
    mask_radius = _positive("projected mask radius", projected_mask_radius_mm)
    aperture = _nonnegative("effective aperture", effective_aperture_mm)
    required_margin = _nonnegative("required hide margin", required_hide_margin_mm)
    if not wall_z < plane_z < source_z:
        raise ValueError("blocker plane must lie between wall and source")
    if radial_start >= radial_end:
        raise ValueError("blocker radial end must exceed radial start")
    if carrier_radius > radial_start:
        raise ValueError("blocker must start at or outside the carrier envelope")
    source_blocker = source_z - plane_z
    blocker_wall = plane_z - wall_z
    source_wall = source_z - wall_z
    magnification = source_wall / source_blocker
    projected_carrier = carrier_radius * magnification
    projected_start = radial_start * magnification
    projected_tip = radial_end * magnification
    hide_margin = mask_radius - projected_carrier
    return {
        "name": name,
        "movement_type": "quartz-direct-shaft-orbital-disc",
        "drive_mechanism": "stock-quartz-concentric-shaft-direct-drive",
        "drive_geometry_modeled": False,
        "plane_z_mm": plane_z,
        "source_z_mm": source_z,
        "wall_z_mm": wall_z,
        "source_blocker_mm": source_blocker,
        "blocker_wall_mm": blocker_wall,
        "source_wall_mm": source_wall,
        "magnification": magnification,
        "effective_aperture_mm": aperture,
        "penumbra_mm": aperture * blocker_wall / source_blocker,
        "carrier_outer_radius_mm": carrier_radius,
        "projected_carrier_radius_mm": projected_carrier,
        "blocker_radial_start_mm": radial_start,
        "blocker_radial_end_mm": radial_end,
        "blocker_width_mm": width,
        "blocker_shape": blocker_shape,
        "projected_radial_start_mm": projected_start,
        "projected_tip_mm": projected_tip,
        "projected_width_mm": width * magnification,
        "projected_mask_radius_mm": mask_radius,
        "visible_projected_start_mm": max(projected_start, mask_radius),
        "visible_projected_end_mm": max(projected_tip, mask_radius),
        "visible_length_mm": max(0.0, projected_tip - max(projected_start, mask_radius)),
        "carrier_hide_margin_mm": hide_margin,
        "required_hide_margin_mm": required_margin,
        "carrier_hidden": hide_margin >= required_margin,
        "required_full_field_angle_degrees": required_full_field_angle_degrees(
            blocker_tip_radius_mm=radial_end,
            source_blocker_mm=source_blocker,
        ),
        "optical_angle_degrees": float(optical_angle_degrees) % 360.0,
        "angle_semantics": "optical-blocker-angle-only-not-drive-geometry",
        "shaft_bore_status": "measure-selected-quartz-movement",
    }


def central_occlusion_check(
    *,
    occluder_radius_mm: float,
    occluder_source_distance_mm: float,
    hardware: Mapping[str, tuple[float, float]],
) -> dict[str, Any]:
    """Check that every hardware radial extent remains inside central shadow.

    Each hardware tuple is ``(radial_extent_mm, source_distance_mm)``.  The
    comparison uses angular extent r/z, so body corners, stand, washer, nut,
    hubs, and movement case can be checked independently once measured.
    """
    radius = _positive("occluder radius", occluder_radius_mm)
    distance = _positive("occluder source distance", occluder_source_distance_mm)
    if not hardware:
        raise ValueError("at least one hardware envelope is required")
    occluder_slope = radius / distance
    components: dict[str, dict[str, float | bool]] = {}
    for name, envelope in hardware.items():
        if not name.strip() or len(envelope) != 2:
            raise ValueError("hardware entries require a name, radius, and source distance")
        hardware_radius = _nonnegative(f"{name} radial extent", envelope[0])
        hardware_distance = _positive(f"{name} source distance", envelope[1])
        slope = hardware_radius / hardware_distance
        components[name] = {
            "radial_extent_mm": hardware_radius,
            "source_distance_mm": hardware_distance,
            "angular_extent": slope,
            "angular_hide_margin": occluder_slope - slope,
            "hidden": occluder_slope >= slope,
        }
    failures = [name for name, component in components.items() if not component["hidden"]]
    return {
        "occluder_radius_mm": radius,
        "occluder_source_distance_mm": distance,
        "occluder_angular_extent": occluder_slope,
        "components": components,
        "all_hardware_hidden": not failures,
        "central_obstruction_failures": failures,
    }
def projected_offset(
    offset_x_mm: float,
    offset_y_mm: float,
    source_hand_mm: float,
    hand_wall_mm: float,
) -> dict[str, float]:
    magnification = projection_distances(source_hand_mm, hand_wall_mm)["magnification"]
    factor = 1.0 - magnification
    return {
        "projected_x_mm": float(offset_x_mm) * factor,
        "projected_y_mm": float(offset_y_mm) * factor,
    }


def penumbra_width(aperture_mm: float, source_hand_mm: float, hand_wall_mm: float) -> float:
    """Finite-source approximation e*W/L; not a diffraction model."""
    aperture = _nonnegative("effective aperture", aperture_mm)
    distances = projection_distances(source_hand_mm, hand_wall_mm)
    return aperture * distances["hand_wall_mm"] / distances["source_hand_mm"]


def halo_response(
    base_radius_mm: float,
    wall_gap_mm: float,
    spread_percent: float,
    brightness_percent: float,
) -> dict[str, float]:
    base_radius = _positive("halo base radius", base_radius_mm)
    wall_gap = _nonnegative("wall gap", wall_gap_mm)
    spread = float(spread_percent)
    brightness = float(brightness_percent)
    if not 0 <= spread <= 100 or not 0 <= brightness <= 100:
        raise ValueError("halo spread and brightness must be between 0 and 100")
    diffusion = spread / 100.0
    radius = base_radius + wall_gap * (0.12 + diffusion * 0.22)
    distance_falloff = 1.0 / (1.0 + max(0.0, wall_gap - 10.0) / 130.0)
    return {
        "radius_mm": radius,
        "diameter_mm": radius * 2.0,
        "edge_softness": 0.12 + diffusion * 0.34 + wall_gap / 600.0,
        "effective_brightness_percent": brightness * distance_falloff,
    }


def clock_angles(hour: int, minute: int, second: float) -> tuple[float, float, float]:
    """Return angles clockwise from 12 o'clock in radians."""
    if not 0 <= hour <= 23 or not 0 <= minute <= 59 or not 0 <= second < 60:
        raise ValueError("clock time must be within 00:00:00 through 23:59:59.999")
    minute_value = minute + second / 60.0
    hour_value = (hour % 12) + minute_value / 60.0
    return hour_value * pi / 6.0, minute_value * pi / 30.0, second * pi / 30.0


def resolve_time(
    *,
    use_real_time: bool,
    manual: tuple[int, int, int] = (10, 10, 35),
    now: datetime | None = None,
    sweep: bool = True,
) -> tuple[int, int, float]:
    if not use_real_time:
        clock_angles(*manual)
        return manual[0], manual[1], float(manual[2])
    value = now or datetime.now()
    second = value.second + (value.microsecond / 1_000_000 if sweep else 0.0)
    return value.hour, value.minute, second


def body_stack_packaging(
    *,
    front_occluder_diameter_mm: float,
    front_occluder_depth_mm: float,
    rear_pod_diameter_mm: float,
    rear_pod_depth_mm: float,
    pod_front_overlap_mm: float,
    wall_gap_mm: float,
    hand_plane_to_pod_rear_mm: float,
    source_hand_mm: float,
    source_recess_mm: float,
    movement_allowance_mm: float,
    rear_opening_diameter_mm: float,
    movement_envelope_width_mm: float,
    movement_envelope_height_mm: float,
) -> dict[str, float | bool]:
    """Derive a stepped-body axial/radial packaging contract.

    Coordinates start at the visible room-side face. The rear pod overlaps the
    decorative shell, so overall depth is shell + pod - overlap. The legacy
    ``front_occluder_*`` argument names are retained for CLI compatibility;
    this shell is not the optical mask.
    """
    front_diameter = _positive("decorative front shell diameter", front_occluder_diameter_mm)
    front_depth = _positive("decorative front shell depth", front_occluder_depth_mm)
    pod_diameter = _positive("rear pod diameter", rear_pod_diameter_mm)
    pod_depth = _positive("rear pod depth", rear_pod_depth_mm)
    overlap = _nonnegative("pod/front overlap", pod_front_overlap_mm)
    gap = _nonnegative("wall gap", wall_gap_mm)
    hand_to_rear = _positive("hand-plane to pod rear", hand_plane_to_pod_rear_mm)
    source_hand = _positive("source-to-hand distance", source_hand_mm)
    source_recess = _nonnegative("source recess", source_recess_mm)
    movement = _positive("movement allowance", movement_allowance_mm)
    rear_opening = _positive("rear opening diameter", rear_opening_diameter_mm)
    movement_width = _positive("movement envelope width", movement_envelope_width_mm)
    movement_height = _positive("movement envelope height", movement_envelope_height_mm)
    if overlap >= min(front_depth, pod_depth):
        raise ValueError("pod/front overlap must be smaller than both component depths")
    if pod_diameter > front_diameter:
        raise ValueError("rear pod cannot exceed the decorative front shell diameter")
    if rear_opening >= pod_diameter:
        raise ValueError("rear opening must leave a positive pod perimeter")
    overall_depth = front_depth + pod_depth - overlap
    hand_plane = overall_depth - hand_to_rear
    available_optical_run = hand_plane - source_recess
    optical_allowance = available_optical_run - source_hand
    movement_allowance_delta = hand_to_rear - movement
    return {
        "overall_depth_mm": overall_depth,
        "total_front_to_wall_mm": overall_depth + gap,
        "hand_plane_from_front_mm": hand_plane,
        "aperture_plane_from_front_mm": hand_plane - source_hand,
        "source_recess_mm": source_recess,
        "available_optical_run_mm": available_optical_run,
        "optical_packaging_allowance_mm": optical_allowance,
        "movement_packaging_allowance_mm": movement_allowance_delta,
        "hand_wall_mm": hand_to_rear + gap,
        "radial_shoulder_mm": (front_diameter - pod_diameter) / 2.0,
        "rear_opening_radial_wall_mm": (pod_diameter - rear_opening) / 2.0,
        "rear_opening_diameter_mm": rear_opening,
        "movement_envelope_width_mm": movement_width,
        "movement_envelope_height_mm": movement_height,
        "movement_lateral_clearance_mm": (rear_opening - max(movement_width, movement_height)) / 2.0,
        "source_plane_behind_front_occluder_mm": source_recess - front_depth,
        "source_plane_from_room_face_mm": source_recess,
        "decorative_shell_is_optical_mask": False,
        "fits_axially": optical_allowance >= 0 and movement_allowance_delta >= 0,
    }


@dataclass(frozen=True)
class WiredLedBreadboard:
    source_hand_mm: float = 40.0
    hand_wall_mm: float = 60.0
    hour_hand_mm: float = 45.0
    minute_hand_mm: float = 70.0
    second_hand_mm: float = 85.0
    effective_aperture_mm: float = 1.0
    led_current_ma: float = 350.0
    source_hand_range_mm: tuple[float, float] = (25.0, 80.0)
    hand_wall_range_mm: tuple[float, float] = (30.0, 120.0)
    printed_aperture_trials_mm: tuple[float, ...] = (1.0, 1.5, 2.0)
    optional_measured_aperture_mm: float = 0.6


@dataclass(frozen=True)
class OpticalConfig:
    source_hand_mm: float = 40.0
    hand_wall_mm: float = 60.0
    aperture_mm: float = 1.0
    hour_hand_mm: float = 45.0
    minute_hand_mm: float = 70.0
    second_hand_mm: float = 85.0
    hour_width_mm: float = 4.5
    minute_width_mm: float = 2.4
    second_width_mm: float = 0.8
    led_offset_x_mm: float = 0.0
    led_offset_y_mm: float = 0.0

    def __post_init__(self) -> None:
        projection_distances(self.source_hand_mm, self.hand_wall_mm)
        _nonnegative("effective aperture", self.aperture_mm)

    @property
    def source_wall_mm(self) -> float:
        return projection_distances(self.source_hand_mm, self.hand_wall_mm)["source_wall_mm"]

    @property
    def magnification(self) -> float:
        return projection_distances(self.source_hand_mm, self.hand_wall_mm)["magnification"]

    def project_length(self, physical_mm: float) -> float:
        return projected_hand(physical_mm, 0, self.source_hand_mm, self.hand_wall_mm)["projected_length_mm"]

    def project_width(self, physical_mm: float) -> float:
        return projected_hand(0, physical_mm, self.source_hand_mm, self.hand_wall_mm)["projected_width_mm"]

    @property
    def penumbra_mm(self) -> float:
        return penumbra_width(self.aperture_mm, self.source_hand_mm, self.hand_wall_mm)

    @property
    def projected_pivot_mm(self) -> tuple[float, float]:
        offset = projected_offset(
            self.led_offset_x_mm,
            self.led_offset_y_mm,
            self.source_hand_mm,
            self.hand_wall_mm,
        )
        return offset["projected_x_mm"], offset["projected_y_mm"]


@dataclass(frozen=True)
class HaloConfig:
    base_radius_mm: float = 195.0
    wall_gap_mm: float = 45.0
    spread_percent: float = 52.0
    brightness_percent: float = 74.0

    @property
    def radius_mm(self) -> float:
        return halo_response(
            self.base_radius_mm,
            self.wall_gap_mm,
            self.spread_percent,
            self.brightness_percent,
        )["radius_mm"]


REFERENCE_FINAL_INPUTS: dict[str, Any] = {
    "body": {
        "front_occluder_diameter_mm": 260.0,
        "front_occluder_depth_mm": 12.0,
        "rear_pod_diameter_mm": 150.0,
        "rear_pod_depth_mm": 60.0,
        "pod_front_overlap_mm": 2.0,
        "wall_gap_mm": 45.0,
        # Nominal minute plane: z=62.8, rear pod plane z=45, room face z=115.
        "hand_plane_to_pod_rear_mm": 17.8,
        # LED/aperture z=104.8 is 10.2 mm behind the room-side face at z=115.
        "source_recess_mm": 10.2,
        "movement_allowance_mm": 15.0,
        "rear_opening_diameter_mm": 120.0,
        "movement_envelope_width_mm": 99.0,
        "movement_envelope_height_mm": 99.0,
    },
    "optics": {
        "source_hand_mm": 42.0,
        "source_z_mm": 104.8,
        "wall_z_mm": 0.0,
        "aperture_mm": 0.8,
        "hand_lengths_mm": {"hour": 60.0, "minute": 70.0, "second": 85.0},
        "hand_widths_mm": {"hour": 9.0, "minute": 2.4, "second": 0.8},
        "hand_shapes": {"hour": "leaf-kite", "minute": "blade", "second": "needle"},
        "hand_length_ranges_mm": {"hour": (58.0, 64.0)},
        "hand_shape_parameters": {
            "hour": {
                "root_width_mm": 4.0,
                "max_width_mm": 9.0,
                "max_width_position_percent": 86.0,
                "tip_width_mm": 1.5,
            }
        },
        "offset_x_mm": 0.0,
        "offset_y_mm": 0.0,
    },
    "mask": {
        "physical_radius_mm": 55.57142857142857,
        "mask_z_mm": 60.0,
        "required_projected_radius_mm": 130.0,
        "minimum_hardware_hide_margin_mm": 5.0,
    },
    "halo": {
        "base_radius_mm": 195.0,
        "spread_percent": 52.0,
        "brightness_percent": 74.0,
    },
}


DIRECT_SHAFT_DISC_INPUTS: dict[str, dict[str, Any]] = {
    "hour": {
        "plane_z_mm": 61.2,
        "carrier_outer_radius_mm": 47.0,
        "blocker_radial_start_mm": 47.0,
        "blocker_radial_end_mm": 60.0,
        "blocker_width_mm": 9.0,
        "blocker_shape": "leaf-kite",
        "optical_angle_degrees": 305.2916667,
        "shaft_interface": "hour-tube-adjustable",
    },
    "minute": {
        "plane_z_mm": 62.8,
        "carrier_outer_radius_mm": 47.0,
        "blocker_radial_start_mm": 47.0,
        "blocker_radial_end_mm": 70.0,
        "blocker_width_mm": 2.4,
        "blocker_shape": "blade",
        "optical_angle_degrees": 63.5,
        "shaft_interface": "minute-shaft-adjustable",
    },
    "second": {
        "plane_z_mm": 64.4,
        "carrier_outer_radius_mm": 47.0,
        "blocker_radial_start_mm": 47.0,
        "blocker_radial_end_mm": 85.0,
        "blocker_width_mm": 0.8,
        "blocker_shape": "needle",
        "optical_angle_degrees": 210.0,
        "shaft_interface": "second-pin-adjustable",
    },
}


RING_CARRIER_INPUTS: dict[str, dict[str, Any]] = {
    "hour": {
        "carrier_inner_radius_mm": 38.0,
        "carrier_outer_radius_mm": 48.0,
        "blocker_radial_start_mm": 48.0,
        "blocker_radial_end_mm": 60.0,
        "blocker_width_mm": 9.0,
        "blocker_shape": "leaf-kite",
        "axial_plane_offset_mm": 1.6,
        "optical_angle_degrees": 305.2916667,
    },
    "minute": {
        "carrier_inner_radius_mm": 38.0,
        "carrier_outer_radius_mm": 48.0,
        "blocker_radial_start_mm": 48.0,
        "blocker_radial_end_mm": 70.0,
        "blocker_width_mm": 2.4,
        "blocker_shape": "blade",
        "axial_plane_offset_mm": 0.0,
        "optical_angle_degrees": 63.5,
    },
    "second": {
        "carrier_inner_radius_mm": 38.0,
        "carrier_outer_radius_mm": 48.0,
        "blocker_radial_start_mm": 48.0,
        "blocker_radial_end_mm": 85.0,
        "blocker_width_mm": 0.8,
        "blocker_shape": "needle",
        "axial_plane_offset_mm": -1.6,
        "optical_angle_degrees": 210.0,
    },
}


def movement_architecture(kind: str) -> dict[str, Any]:
    """Return movement metadata without inventing drive or gear geometry."""
    architectures = {
        "manual-concentric-ring-jig": {
            "movement_type": "manual-concentric-ring-jig",
            "scenario_role": "P0 optical breadboard",
            "drive_mechanism": "manual rotation only",
            "drive_geometry_modeled": False,
            "hollow_center": True,
            "carrier_inputs": {
                "hour": RING_CARRIER_INPUTS["hour"],
                "minute": RING_CARRIER_INPUTS["minute"],
            },
            "optional_carrier_names": ["second"],
        },
        "annular-orbital-hollow-center": {
            "movement_type": "annular-orbital-hollow-center",
            "scenario_role": "comparison-only optical hypothesis",
            "drive_mechanism": "future mechanism intentionally not modeled",
            "drive_geometry_modeled": False,
            "hollow_center": True,
            "carrier_inputs": RING_CARRIER_INPUTS,
            "optional_carrier_names": [],
        },
        "quartz-driven-orbital-hands": {
            "movement_type": "quartz-driven-orbital-hands",
            "scenario_role": "reference-final primary architecture",
            "drive_mechanism": "stock quartz hour/minute/seconds shafts directly drive independent single tapered orbital blocker blades; no printed gearing",
            "drive_geometry_modeled": False,
            "hollow_center": False,
            "carrier_inputs": DIRECT_SHAFT_DISC_INPUTS,
            "optional_carrier_names": [],
            "room_to_wall_stack": [
                "viewer-cosmetic-shell-and-metal-heatsink",
                "point-led-and-thin-flared-aperture",
                "second-minute-hour-direct-shaft-blocker-discs",
                "fixed-physical-mask-and-quartz-face",
                "stock-quartz-case",
                "wall-standoff",
                "wall",
            ],
            "hardware_occlusion_status": "carrier-envelope-passes-mask; exact-bores-and-case-require-measurement",
            "fixed_mask_is_separate_from_cosmetic_shell": True,
            "minimum_source_to_front_hardware_clearance_mm": 30.0,
            "maximum_axis_offset_mm": 0.5,
            "minimum_full_optical_field_degrees": 130.0,
            "aperture_construction": "thin-or-flared; deep-printed-bore-rejected",
            "movement_hardware_reference": {
                "shipped_variant_overall_mm": 34.0,
                "shipped_threaded_bushing_mm": 7.7,
                "published_cad_overall_mm": 29.7,
                "provisional_variant_dependent": True,
                "movement_envelope_adjustable": True,
                "mounting_thickness_adjustable": True,
            },
        },
        "architecture-under-review": {
            "movement_type": "architecture-under-review",
            "scenario_role": "reference-final movement decision",
            "drive_mechanism": "not selected",
            "drive_geometry_modeled": False,
            "hollow_center": None,
            "candidate_movement_types": [
                "rear-side-conventional-arbor",
                "annular-orbital-hollow-center",
            ],
            "carrier_inputs": {},
            "optional_carrier_names": [],
        },
        "standard-center-shaft-quartz": {
            "movement_type": "standard-center-shaft-quartz",
            "scenario_role": "generic timing experiment only",
            "drive_mechanism": "off-the-shelf quartz movement",
            "drive_geometry_modeled": False,
            "hollow_center": False,
            "carrier_inputs": {},
            "optional_carrier_names": [],
        },
    }
    if kind not in architectures:
        raise KeyError(f"unknown movement architecture: {kind}")
    architecture = architectures[kind]
    return {
        **architecture,
        "carrier_inputs": {
            name: dict(values) for name, values in architecture["carrier_inputs"].items()
        },
    }


def stage_presets() -> dict[str, dict[str, Any]]:
    p0 = WiredLedBreadboard()
    return {
        "wired-led-breadboard": {
            "description": "Wired current-limited point-LED breadboard with fake interchangeable blockers",
            "source_hand_mm": p0.source_hand_mm,
            "hand_wall_mm": p0.hand_wall_mm,
            "aperture_mm": p0.effective_aperture_mm,
            "hand_lengths_mm": {
                "hour": p0.hour_hand_mm,
                "minute": p0.minute_hand_mm,
            },
            "movement": movement_architecture("manual-concentric-ring-jig"),
            "provenance": "accepted first-stage wired LED optical bench",
        },
        "generic-quartz": {
            "description": "Generic center-shaft quartz timing experiment",
            "provenance": "separate generic experiment; not the reference-final architecture",
            **REFERENCE_FINAL_INPUTS,
            "movement": movement_architecture("standard-center-shaft-quartz"),
        },
        "reference-final": {
            "description": "Quartz-direct orbital blockers with explicit fixed mask and stepped body",
            "provenance": "image-derived design inference; not a measurement of the reference product",
            **REFERENCE_FINAL_INPUTS,
            "movement": movement_architecture("quartz-driven-orbital-hands"),
        },
        "reference-orbital-study": {
            "description": "Annular orbital carrier optical hypothesis",
            "provenance": "comparison study only; not the selected reference-final drive architecture",
            **REFERENCE_FINAL_INPUTS,
            "movement": movement_architecture("annular-orbital-hollow-center"),
        },
    }


def design_warnings(
    *,
    optics: Mapping[str, Any],
    halo: Mapping[str, Any],
    packaging: Mapping[str, float | bool] | None = None,
    stage: str = "p1",
) -> list[str]:
    warnings: list[str] = []
    maximum_shadow = max(v["projected_length_mm"] for v in optics["hands"].values())
    if halo.get("enabled", True) and maximum_shadow > halo["radius_mm"]:
        warnings.append("shadow_exceeds_halo")
    if optics["penumbra_mm"] > 3.2:
        warnings.append("shadow_likely_soft")
    if packaging is not None:
        if not packaging["fits_axially"]:
            warnings.append("body_stack_does_not_fit")
        elif packaging["optical_packaging_allowance_mm"] < 2:
            warnings.append("optical_stack_has_little_tuning_allowance")
        if not 120 <= REFERENCE_FINAL_INPUTS["body"]["rear_pod_diameter_mm"] <= 180:
            warnings.append("rear_pod_outside_reference_silhouette_range")
        if packaging["rear_opening_radial_wall_mm"] < 3:
            warnings.append("rear_opening_leaves_thin_pod_wall")
        if packaging["movement_lateral_clearance_mm"] < 2:
            warnings.append("movement_envelope_tight_in_rear_opening")
    warnings.append("verify_led_thermal_clearance_from_pla")
    return warnings


def warning_codes(
    optical: OpticalConfig,
    halo: HaloConfig,
    *,
    body_depth_mm: float = 35.0,
    movement_depth_mm: float = 15.0,
    shell_mm: float = 2.0,
    second_hand_heavy: bool = False,
    stage: str = "p1",
) -> set[str]:
    warnings: set[str] = set()
    if optical.project_length(optical.second_hand_mm) > halo.radius_mm:
        warnings.add("shadow_exceeds_halo")
    if stage != "p0" and optical.source_hand_mm > body_depth_mm - movement_depth_mm - shell_mm:
        warnings.add("source_path_exceeds_shell")
    if optical.source_hand_mm < 10:
        warnings.add("led_too_close")
    warnings.add("verify_led_thermal_clearance_from_pla")
    if optical.aperture_mm < 0.5:
        warnings.add("aperture_reduces_brightness")
    if second_hand_heavy:
        warnings.add("second_hand_load")
    return warnings


def calculate_scenario(name: str) -> dict[str, Any]:
    presets = stage_presets()
    if name not in presets:
        raise KeyError(f"unknown scenario: {name}")
    preset = presets[name]
    if name == "wired-led-breadboard":
        source_hand = preset["source_hand_mm"]
        hand_wall = preset["hand_wall_mm"]
        aperture = preset["aperture_mm"]
        body = None
        packaging = None
        hand_lengths = preset["hand_lengths_mm"]
        hand_widths = {"hour": 4.5, "minute": 2.4, "second": 0.8}
        hand_shapes = {"hour": "blade", "minute": "blade", "second": "needle"}
        hand_ranges: dict[str, tuple[float, float]] = {}
        hand_shape_parameters: dict[str, Mapping[str, float]] = {}
        occluder_radius = 0.0
        halo_inputs = asdict(HaloConfig(wall_gap_mm=0))
        stage = "p0"
    else:
        body_inputs = dict(preset["body"])
        source_hand = preset["optics"]["source_hand_mm"]
        packaging = body_stack_packaging(source_hand_mm=source_hand, **body_inputs)
        hand_wall = packaging["hand_wall_mm"]
        aperture = preset["optics"]["aperture_mm"]
        hand_lengths = preset["optics"]["hand_lengths_mm"]
        hand_widths = preset["optics"]["hand_widths_mm"]
        hand_shapes = preset["optics"]["hand_shapes"]
        hand_ranges = preset["optics"]["hand_length_ranges_mm"]
        hand_shape_parameters = preset["optics"]["hand_shape_parameters"]
        mask = (
            projected_mask(
                physical_radius_mm=preset["mask"]["physical_radius_mm"],
                mask_z_mm=preset["mask"]["mask_z_mm"],
                source_z_mm=preset["optics"]["source_z_mm"],
                wall_z_mm=preset["optics"]["wall_z_mm"],
            )
            if name in {"reference-final", "reference-orbital-study"}
            else None
        )
        occluder_radius = mask["projected_radius_mm"] if mask else 0.0
        body = {"inputs": body_inputs, "derived": packaging}
        halo_inputs = {
            **preset["halo"],
            "wall_gap_mm": body_inputs["wall_gap_mm"],
        }
        stage = "p2" if name in {"generic-quartz", "reference-orbital-study"} else "p3"
    distances = projection_distances(source_hand, hand_wall)
    hands = {
        hand: projected_blocker(
            name=hand,
            shape=hand_shapes[hand],
            radial_length_mm=length,
            width_mm=hand_widths[hand],
            source_hand_mm=source_hand,
            hand_wall_mm=hand_wall,
            occluder_radius_mm=occluder_radius,
            shape_parameters=hand_shape_parameters.get(hand),
            physical_length_range_mm=hand_ranges.get(hand),
        )
        for hand, length in hand_lengths.items()
    }
    optics = {
        **distances,
        "aperture_mm": aperture,
        "penumbra_mm": penumbra_width(aperture, source_hand, hand_wall),
        "offset": projected_offset(0, 0, source_hand, hand_wall),
        "hands": hands,
        "projected_sweep_diameter_mm": max(v["projected_length_mm"] for v in hands.values()) * 2,
        "projected_hour_length_mm": hands.get("hour", {}).get("projected_length_mm"),
        "visible_hour_length_mm": hands.get("hour", {}).get("visible_length_mm"),
    }
    halo = halo_response(**halo_inputs)
    halo["enabled"] = stage == "p3"
    movement_input = preset["movement"]
    if movement_input["movement_type"] == "quartz-driven-orbital-hands":
        carriers = {}
        for carrier_name, carrier_input in movement_input["carrier_inputs"].items():
            values = dict(carrier_input)
            shaft_interface = values.pop("shaft_interface")
            carrier = projected_direct_shaft_disc(
                name=carrier_name,
                source_z_mm=preset["optics"]["source_z_mm"],
                wall_z_mm=preset["optics"]["wall_z_mm"],
                projected_mask_radius_mm=occluder_radius,
                effective_aperture_mm=aperture,
                required_hide_margin_mm=preset["mask"]["minimum_hardware_hide_margin_mm"],
                **values,
            )
            carrier["shaft_interface"] = shaft_interface
            carriers[carrier_name] = carrier
        optics["hands"] = {
            name: {
                "name": name,
                "shape": carrier["blocker_shape"],
                "physical_radial_length_mm": carrier["blocker_radial_end_mm"],
                "physical_width_mm": carrier["blocker_width_mm"],
                "projected_length_mm": carrier["projected_tip_mm"],
                "projected_width_mm": carrier["projected_width_mm"],
                "occluder_radius_mm": occluder_radius,
                "visible_length_mm": carrier["visible_length_mm"],
                "shape_parameters": hand_shape_parameters.get(name, {}),
                "physical_length_range_mm": list(hand_ranges[name]) if name in hand_ranges else None,
            }
            for name, carrier in carriers.items()
        }
        optics["per_plane"] = {
            name: {
                key: carrier[key]
                for key in (
                    "plane_z_mm", "source_blocker_mm", "blocker_wall_mm",
                    "source_wall_mm", "magnification", "penumbra_mm",
                    "projected_tip_mm", "visible_length_mm",
                    "carrier_hide_margin_mm", "required_full_field_angle_degrees",
                )
            }
            for name, carrier in carriers.items()
        }
        optics["penumbra_mm"] = carriers["minute"]["penumbra_mm"]
        optics["projected_sweep_diameter_mm"] = max(
            carrier["projected_tip_mm"] for carrier in carriers.values()
        ) * 2.0
        optics["projected_hour_length_mm"] = carriers["hour"]["projected_tip_mm"]
        optics["visible_hour_length_mm"] = carriers["hour"]["visible_length_mm"]
        optics["fixed_mask"] = mask
        optics["required_full_field_angle_degrees"] = max(
            carrier["required_full_field_angle_degrees"] for carrier in carriers.values()
        )
        optics["flared_pod_clearance"] = flared_pod_clearance(
            blocker_tip_radius_mm=carriers["second"]["blocker_radial_end_mm"],
            blocker_z_mm=carriers["second"]["plane_z_mm"],
            source_z_mm=preset["optics"]["source_z_mm"],
            pod_clear_radius_mm=body_inputs["rear_opening_diameter_mm"] / 2.0,
            pod_rear_z_mm=45.0,
        )
    else:
        carriers = {
            carrier_name: projected_ring_carrier(
                name=carrier_name,
                source_hand_mm=source_hand,
                hand_wall_mm=hand_wall,
                effective_occluder_radius_mm=occluder_radius,
                **carrier,
            )
            for carrier_name, carrier in movement_input["carrier_inputs"].items()
        }
    movement = {
        key: value for key, value in movement_input.items() if key != "carrier_inputs"
    }
    movement["carriers"] = carriers
    movement["angle_semantics"] = "optical blocker angles are independent of future drive geometry"
    if carriers and movement["movement_type"] == "quartz-driven-orbital-hands":
        movement["direct_shaft_stack"] = {
            "wall_z_mm": preset["optics"]["wall_z_mm"],
            "quartz_case_z_mm": [45.0, 60.0],
            "fixed_mask_z_mm": 60.0,
            "blocker_plane_z_mm": {
                name: carrier["plane_z_mm"] for name, carrier in carriers.items()
            },
            "source_z_mm": preset["optics"]["source_z_mm"],
            "room_shell_z_mm": 115.0,
            "fixed_mask": mask,
            "carrier_outer_radius_mm": 47.0,
            "minimum_carrier_hide_margin_mm": min(
                carrier["carrier_hide_margin_mm"] for carrier in carriers.values()
            ),
            "minimum_source_to_front_hardware_clearance_mm": 30.0,
            "minimum_full_optical_field_degrees": 130.0,
            "flared_pod_clearance": optics["flared_pod_clearance"],
        }
        movement["ring_stack"] = None
        movement["failure_flags"] = {
            "carrier_or_hardware_shadow": any(not carrier["carrier_hidden"] for carrier in carriers.values()),
            "insufficient_optical_field": optics["required_full_field_angle_degrees"] > 130.0,
            "hollow_tunnel_in_primary": False,
            "printed_gearing_in_primary": False,
        }
    elif carriers:
        movement["ring_stack"] = {
            "clear_center_diameter_mm": 36.0,
            "carrier_inner_radius_mm": 38.0,
            "carrier_outer_radius_mm": 48.0,
            "maximum_exposed_drive_radius_mm": 49.5,
            "carrier_thickness_mm": 1.2,
            "axial_gap_mm": 0.4,
            "axial_pitch_mm": 1.6,
            "three_ring_stack_depth_mm": 4.4,
            "worst_carrier_hide_margin_mm": min(
                carrier["carrier_hide_margin_mm"] for carrier in carriers.values()
            ),
        }
        movement["failure_flags"] = {
            flag: any(carrier["failure_flags"][flag] for carrier in carriers.values())
            for flag in next(iter(carriers.values()))["failure_flags"]
        }
    else:
        movement["ring_stack"] = None
        movement["failure_flags"] = {}
    warnings = design_warnings(optics=optics, halo=halo, packaging=packaging, stage=stage)
    if movement["movement_type"] == "quartz-driven-orbital-hands":
        warnings.extend([
            "continuous_rear_pod_rejected_open_flare_required",
            "measure_selected_quartz_shaft_bores_and_axial_heights",
            "verify_24_hour_disc_clearance_and_timekeeping",
            "verify_30_minute_led_thermal_run",
        ])
    return {
        "schema_version": 1,
        "scenario": name,
        "description": preset["description"],
        "provenance": preset["provenance"],
        "movement_type": movement["movement_type"],
        "movement": movement,
        "body": body,
        "optics": optics,
        "halo": halo,
        "warnings": warnings,
    }
