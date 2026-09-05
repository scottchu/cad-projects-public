"""One pure validation and derivation boundary for the P1 R7 source laws."""

from dataclasses import asdict, dataclass, fields
from math import cos, floor, hypot, isfinite, pi, sin

from .parameters import Parameters


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Resolved:
    # Selected inputs. Geometry code receives this record, never Parameters.
    device_length: float
    device_diameter: float
    axial_allowance: float
    cap_cavity_length: float
    body_bore: float
    cap_bore: float
    floor: float
    thread_pitch: float
    engagement: float
    thread_clearance: float
    clearance_budget: float
    thread_height: float
    root_wall: float
    cap_taper_length: float
    outer_diameter: float
    skin_axial_pitch: float
    skin_arc_pitch_target: float
    skin_height: float
    plateau_half_fraction: float
    skin_phase_theta: float
    skin_phase_z: float
    end_chamfer_size: float
    drain_diameter: float
    drain_ring_radius: float
    drain_ring_count: int
    skin_style: str
    # Complete derived record.
    cavity_length: float
    cap_height: float
    body_inner_radius: float
    cap_inner_radius: float
    body_radius: float
    cap_radius: float
    thread_root: float
    thread_crest: float
    shoulder_radius: float
    neck_height: float
    full_thread_start: float
    full_thread_end: float
    collar_end: float
    taper_length: float
    cap_straight_start: float
    body_depth: float
    outer_crest_radius: float
    outer_valley_radius: float
    body_band: tuple[float, float]
    cap_band: tuple[float, float]
    lattice_count: int
    arc_pitch: float
    plateau_width: float
    skin_slope_bound: float
    end_chamfer_radius: float
    end_chamfer_axial_height: float
    end_chamfer_slope: float
    end_chamfer_smooth_band: float
    cap_end_radial_material: float
    thread_flank_slope: float
    thread_lead_slope: float
    outer_length: float
    female_minimum_wall: float
    minimum_wall: float
    body_straight_wall: float
    cap_straight_wall: float
    body_radial_gap: float
    cap_radial_gap: float
    drain_centers: tuple[tuple[float, float], ...]
    body_print_translation: tuple[float, float, float]
    cap_print_translation: tuple[float, float, float]
    cap_print_rotation: tuple[float, float, float]
    print_bounds_separation: float
    body_datums: tuple[tuple[str, float], ...]
    cap_datums: tuple[tuple[str, float], ...]


def derive(parameters: Parameters) -> Resolved:
    """Validate all inputs and compute every downstream scalar/placement once."""
    require(isinstance(parameters, Parameters), 'derive requires Parameters')
    for field in fields(parameters):
        value = getattr(parameters, field.name)
        if field.name != 'skin_style':
            require(isinstance(value, (float, int)) and not isinstance(value, bool)
                    and isfinite(value), f'{field.name} must be finite')
    p = parameters
    require(p.skin_style == 'diamond', 'P1 R7 supports diamond skin only')
    for name, value in dict(body_bore=30., cap_bore=31., floor=3.,
                            thread_pitch=2., engagement=6., thread_height=.5,
                            root_wall=1.4, clearance_budget=.30, cap_taper_length=2.2,
                            drain_diameter=3., drain_ring_radius=9., drain_ring_count=6).items():
        require(getattr(p, name) == value, f'P1 R7 parameter {name} is locked at {value}')
    require(.20 <= p.thread_clearance <= .30, 'thread_clearance must be in [.20,.30]')
    require(p.device_length > 0 and p.device_diameter > 0, 'device dimensions must be positive')
    require(p.axial_allowance >= 3, 'axial allowance must be at least 3mm')
    require(p.cap_cavity_length > 0, 'cap_cavity_length must be positive')
    require(p.outer_diameter > 0, 'outer_diameter must be positive')
    require(0 < p.skin_height <= .6, 'skin_height must be in (0,.6]')
    require(3 <= p.skin_axial_pitch <= 8, 'skin_axial_pitch must be in [3,8]')
    require(0 < p.plateau_half_fraction < .5, 'invalid plateau fraction')
    require(p.skin_arc_pitch_target > 0, 'arc pitch target must be positive')
    require(.80 <= p.end_chamfer_size <= 1.50, 'end_chamfer_size must be in [.80,1.50]')
    cavity_length = p.device_length + p.axial_allowance
    cap_height = p.cap_cavity_length + p.floor
    rb, rc = p.body_bore / 2, p.cap_bore / 2
    root = rb + p.root_wall
    crest = root + p.thread_height
    thread_tool_length = 1.5 * p.thread_pitch + p.engagement
    collar_end = thread_tool_length + .6 * p.thread_pitch
    taper_length = p.cap_taper_length
    cap_straight_start = collar_end + taper_length
    body_depth = cavity_length - p.cap_cavity_length
    require(body_depth > p.floor and cap_height > cap_straight_start + p.floor,
            'cavity/cap length leaves no useful shell')
    require(cavity_length <= 300 and cap_height <= 300, 'length exceeds bounded domain')
    outer_crest_radius = p.outer_diameter / 2
    outer_valley_radius = outer_crest_radius - p.skin_height
    body_radius = cap_radius = shoulder_radius = outer_valley_radius
    female_wall = outer_valley_radius - crest - p.clearance_budget
    require(female_wall >= 1.8 - 1e-10, 'outer diameter leaves female ligament below 1.8mm')
    require(p.thread_height - p.clearance_budget >= .2 - 1e-10, 'radial interlock below .20mm')
    require((crest + p.clearance_budget - rc) / taper_length <= 1, 'cap taper exceeds 45 degrees')
    require(p.drain_ring_radius + p.drain_diameter / 2 < min(rb, rc), 'drains reach cylindrical sidewall')
    require(p.outer_diameter <= 80, 'outer diameter exceeds bounded domain')
    lattice_count = floor(2 * pi * outer_valley_radius / p.skin_arc_pitch_target + .5)
    require(8 <= lattice_count <= 128, 'lattice count must be in [8,128]')
    arc_pitch = 2 * pi * outer_valley_radius / lattice_count
    plateau_width = (2 * p.plateau_half_fraction * arc_pitch * p.skin_axial_pitch
                     / hypot(arc_pitch, p.skin_axial_pitch))
    require(plateau_width >= 1, 'developed plateau width below 1mm')
    skin_slope = p.skin_height / (p.skin_axial_pitch * (.5 - p.plateau_half_fraction))
    require(skin_slope <= 1, 'diamond slope exceeds 45 degrees')
    require(p.end_chamfer_size < p.floor, 'chamfer reaches the inner floor')
    require(abs(p.skin_phase_theta * lattice_count / (2 * pi)) < 2**40
            and abs(p.skin_phase_z / p.skin_axial_pitch) < 2**40, 'unresolvable phase')
    drain_centers = ((0., 0.),) + tuple(
        (p.drain_ring_radius * cos(2*pi*k/p.drain_ring_count),
         p.drain_ring_radius * sin(2*pi*k/p.drain_ring_count))
        for k in range(p.drain_ring_count)
    )
    spacing = p.outer_diameter + 7.0
    body_datums = (
        ('shoulder', 0.), ('tip', thread_tool_length),
        ('full_thread_start', p.thread_pitch),
        ('full_thread_end', p.thread_pitch+p.engagement),
        ('skin_phase', p.skin_phase_z), ('bed', -body_depth-p.floor),
        ('inner_floor', -body_depth),
    )
    cap_datums = (
        ('shoulder', 0.), ('tip', thread_tool_length),
        ('full_thread_start', p.thread_pitch),
        ('full_thread_end', p.thread_pitch+p.engagement),
        ('skin_phase', p.skin_phase_z), ('bed', cap_height),
        ('inner_floor', p.cap_cavity_length),
    )
    derived = dict(
        cavity_length=cavity_length, cap_height=cap_height,
        body_inner_radius=rb, cap_inner_radius=rc,
        body_radius=body_radius, cap_radius=cap_radius,
        thread_root=root, thread_crest=crest, shoulder_radius=shoulder_radius,
        neck_height=thread_tool_length, full_thread_start=p.thread_pitch,
        full_thread_end=p.thread_pitch+p.engagement, collar_end=collar_end,
        taper_length=taper_length, cap_straight_start=cap_straight_start,
        body_depth=body_depth, outer_crest_radius=outer_crest_radius,
        outer_valley_radius=outer_valley_radius,
        body_band=(-body_depth-p.floor, 0.), cap_band=(0., cap_height),
        lattice_count=lattice_count, arc_pitch=arc_pitch, plateau_width=plateau_width,
        skin_slope_bound=skin_slope,
        end_chamfer_radius=outer_crest_radius-p.end_chamfer_size,
        end_chamfer_axial_height=p.end_chamfer_size, end_chamfer_slope=1.,
        end_chamfer_smooth_band=p.end_chamfer_size-p.skin_height,
        cap_end_radial_material=outer_crest_radius-p.end_chamfer_size-rc,
        thread_flank_slope=p.thread_height/(.35*p.thread_pitch),
        thread_lead_slope=p.thread_height/(.5*p.thread_pitch),
        outer_length=cavity_length+2*p.floor,
        female_minimum_wall=female_wall, minimum_wall=min(p.root_wall, female_wall),
        body_straight_wall=outer_valley_radius-rb,
        cap_straight_wall=outer_valley_radius-rc,
        body_radial_gap=(p.body_bore-p.device_diameter)/2,
        cap_radial_gap=(p.cap_bore-p.device_diameter)/2,
        drain_centers=drain_centers,
        body_print_translation=(spacing/2, 0., body_depth+p.floor),
        cap_print_translation=(-spacing/2, 0., cap_height),
        cap_print_rotation=(180., 0., 0.), print_bounds_separation=7.0,
        body_datums=body_datums, cap_datums=cap_datums,
    )
    return Resolved(**asdict(p), **derived)


__all__ = ['Resolved', 'derive', 'require']
