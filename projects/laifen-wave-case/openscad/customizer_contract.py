"""Independent analytic oracle for the OpenSCAD Customizer VFR-04 contract."""
from dataclasses import dataclass
from math import ceil, floor, isfinite, pi, sqrt


@dataclass(frozen=True)
class DiamondConstraints:
    count: int
    actual_arc_pitch: float
    plateau_width: float
    axial_slope: float
    body_valley_wall: float
    cap_valley_wall: float
    female_thread_valley_wall: float
    female_entry_relief_wall: float
    estimated_exterior_triangles: int


@dataclass(frozen=True)
class Derived:
    cavity: float
    engagement: float
    overlap: float
    body_height: float
    cap_height: float
    split_from_top: float
    split_percent: float
    lattice_count: int
    arc_pitch: float
    diamond: DiamondConstraints


def clamp(value, lower, upper):
    return min(max(float(value), lower), upper)


def split_from_mode(total_height, mode, distance_from_top, percent_from_top):
    if not isfinite(total_height) or total_height <= 0:
        raise ValueError("total height must be finite and positive")
    if mode == "percentage":
        return total_height * clamp(percent_from_top, 1e-6, 100 - 1e-6) / 100
    if mode != "distance":
        raise ValueError("split mode must be distance or percentage")
    return float(distance_from_top)


def diamond_count(valley_radius: float, target_arc: float) -> int:
    """Positive half-up repeat count; Python's bankers round is forbidden here."""
    if not all(isfinite(float(v)) for v in (valley_radius, target_arc)):
        raise ValueError("diamond count inputs must be finite")
    if valley_radius <= 0 or target_arc <= 0:
        raise ValueError("diamond count inputs must be positive")
    count = floor(2 * pi * valley_radius / target_arc + 0.5)
    if not 8 <= count <= 128:
        raise ValueError("diamond count must be in [8, 128]")
    return count


def diamond_wrap(t: float) -> float:
    if not isfinite(float(t)):
        raise ValueError("diamond coordinate must be finite")
    return t - floor(t + 0.5)


def diamond_coordinates(theta_deg, z_global, phase_deg, seam_z, count, axial_pitch):
    values = (theta_deg, z_global, phase_deg, seam_z, count, axial_pitch)
    if not all(isfinite(float(v)) for v in values) or axial_pitch <= 0:
        raise ValueError("diamond coordinates require finite values and positive pitch")
    return count * (theta_deg - phase_deg) / 360, (z_global - seam_z) / axial_pitch


def diamond_field(u: float, v: float, plateau_half_fraction: float) -> float:
    if not all(isfinite(float(x)) for x in (u, v, plateau_half_fraction)):
        raise ValueError("diamond field inputs must be finite")
    if not 0 < plateau_half_fraction < 0.5:
        raise ValueError("plateau half fraction must be in (0, 0.5)")
    m = max(abs(diamond_wrap(u + v)), abs(diamond_wrap(u - v)))
    return min(1.0, max(0.0, (0.5 - m) / (0.5 - plateau_half_fraction)))


def diamond_radius(valley_radius, depth, u, v, plateau_half_fraction):
    if not all(isfinite(float(x)) for x in (valley_radius, depth)):
        raise ValueError("diamond radius inputs must be finite")
    if valley_radius <= 0 or depth < 0:
        raise ValueError("diamond radius requires positive valley radius and nonnegative depth")
    return valley_radius + depth * diamond_field(u, v, plateau_half_fraction)


def diamond_global_z(role: str, local_z: float, seam_z: float) -> float:
    if role == "body":
        return local_z
    if role == "cap":
        return seam_z + local_z
    raise ValueError("diamond role must be body or cap")


def diamond_patch_coordinates(s: float, t: float):
    return (s + t) / 2, (s - t) / 2


def diamond_patch_inverse(u: float, v: float):
    return u + v, u - v


def diamond_constraints(*, outer_diameter=39, body_bore=30, cap_bore=31,
                        minimum_wall=2.4, thread_root_wall=1.4,
                        thread_clearance=0.25, thread_depth=0.5,
                        axial_pitch=4.8, target_arc=3.63, depth=0.45,
                        plateau_half_fraction=0.18, band_height=135,
                        angular_subdivisions=8, maximum_triangles=250_000):
    values = (outer_diameter, body_bore, cap_bore, minimum_wall,
              thread_root_wall, thread_clearance, thread_depth, axial_pitch,
              target_arc, depth, plateau_half_fraction, band_height)
    if not all(isfinite(float(v)) for v in values):
        raise ValueError("all diamond constraint inputs must be finite")
    if depth < 0 or outer_diameter <= 0 or band_height <= 0:
        raise ValueError("diamond dimensions must be positive (depth may be zero)")
    valley = outer_diameter / 2 - depth
    count = diamond_count(valley, target_arc)
    actual_arc = 2 * pi * valley / count
    if depth == 0:
        plateau_width = 0.0
        slope = 0.0
    else:
        if not 0 < plateau_half_fraction < 0.5:
            raise ValueError("plateau half fraction must be in (0, 0.5)")
        plateau_width = 2 * plateau_half_fraction * actual_arc * axial_pitch / sqrt(actual_arc * actual_arc + axial_pitch * axial_pitch)
        slope = depth / (axial_pitch * (0.5 - plateau_half_fraction))
    thread_root_radius = body_bore / 2 + thread_root_wall
    female_crest = thread_root_radius + thread_clearance + thread_depth
    entry_relief_radius = thread_root_radius + thread_clearance + 0.4
    body_wall = valley - body_bore / 2
    cap_wall = valley - cap_bore / 2
    female_wall = valley - female_crest
    relief_wall = valley - entry_relief_radius
    angular_segments = count * angular_subdivisions
    axial_segments = ceil(band_height / (axial_pitch / angular_subdivisions))
    estimate = 2 * angular_segments * axial_segments + 2 * angular_segments
    if depth > 0:
        if plateau_width < 1.0:
            raise ValueError("diamond plateau developed width below 1.0mm")
        if slope > 1.0:
            raise ValueError("diamond axial slope exceeds 1")
        if body_wall < minimum_wall or cap_wall < minimum_wall:
            raise ValueError("diamond valley shell wall below minimum_wall")
        if female_wall < 1.8:
            raise ValueError("diamond female thread valley wall below 1.8mm")
        if relief_wall < 1.8:
            raise ValueError("diamond female entry relief wall below 1.8mm")
        if estimate > maximum_triangles:
            raise ValueError("diamond exterior triangle estimate exceeds cap")
    return DiamondConstraints(count, actual_arc, plateau_width, slope,
                              body_wall, cap_wall, female_wall, relief_wall,
                              estimate)


def derive(*, device_length=208, axial_allowance=5, outer_diameter=39,
           body_bore=30, cap_bore=31, minimum_wall=2.4, floor=3, thread_pitch=2,
           thread_turns=3, thread_clearance=0.25, thread_depth=0.5,
           thread_root_wall=1.4, split_mode="distance", split_distance_from_top=84,
           split_percent_from_top=84 / 219 * 100, skin_arc_pitch=3.63,
           diamond_axial_pitch=4.8, diamond_depth=0.45,
           diamond_plateau_half_fraction=0.18):
    values = (device_length, axial_allowance, outer_diameter, body_bore, cap_bore,
              minimum_wall, floor, thread_pitch, thread_turns, thread_clearance,
              thread_depth, thread_root_wall, split_distance_from_top,
              split_percent_from_top, skin_arc_pitch, diamond_axial_pitch,
              diamond_depth, diamond_plateau_half_fraction)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all numeric values must be finite")
    cavity = device_length + axial_allowance
    engagement = thread_pitch * thread_turns
    overlap = engagement + 3
    total = cavity + 2 * floor
    cap_height = split_from_mode(total, split_mode, split_distance_from_top, split_percent_from_top)
    body_height = total - cap_height + overlap
    if cavity < 2 * floor + engagement + 3:
        raise ValueError("cavity leaves no closure/end-clearance budget")
    if outer_diameter <= max(body_bore, cap_bore) + 2 * minimum_wall:
        raise ValueError("outer diameter does not retain wall")
    if not 0.20 <= thread_clearance <= 0.30:
        raise ValueError("thread clearance must be in [0.20, 0.30]")
    if thread_pitch <= 0 or thread_turns <= 0 or thread_depth <= 0:
        raise ValueError("thread dimensions must be positive")
    transition = overlap + 2
    if cap_height <= floor + transition or body_height <= floor + transition:
        raise ValueError("split is outside feasible body/cap transition interval")
    thread_root_radius = body_bore / 2 + thread_root_wall
    if outer_diameter / 2 - (thread_root_radius + thread_depth + thread_clearance) < 1.8:
        raise ValueError("threaded cap wall below 1.8mm")
    diamond = diamond_constraints(outer_diameter=outer_diameter, body_bore=body_bore,
        cap_bore=cap_bore, minimum_wall=minimum_wall, thread_root_wall=thread_root_wall,
        thread_clearance=thread_clearance, thread_depth=thread_depth,
        axial_pitch=diamond_axial_pitch, target_arc=skin_arc_pitch,
        depth=diamond_depth, plateau_half_fraction=diamond_plateau_half_fraction,
        band_height=max(total - cap_height, cap_height))
    return Derived(cavity, engagement, overlap, body_height, cap_height,
                   cap_height, 100 * cap_height / total, diamond.count,
                   diamond.actual_arc_pitch, diamond)
