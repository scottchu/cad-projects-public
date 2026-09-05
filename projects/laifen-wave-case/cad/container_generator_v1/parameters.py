"""Truthful input registry for the standalone P1 R7 container generator.

The registry is the public parameter contract. ``Parameters`` is the immutable
transport used to pass one selected registry value set into :func:`derive`.
"""

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from types import MappingProxyType


def _spec(id, group, unit, default, domain, classification, geometry_targets,
          validation_oracle, *, affects_geometry):
    return MappingProxyType(dict(
        id=id,
        group=group,
        unit=unit,
        default=default,
        domain=domain,
        classification=classification,
        affects_geometry=affects_geometry,
        geometry_targets=tuple(geometry_targets),
        validation_oracle=validation_oracle,
    ))


PARAMETER_SPECS = (
    _spec('device_length', 'axial', 'mm', 208.0, {'exclusive_min': 0.0, 'coupled_max_cavity': 300.0}, 'adjustable_geometry', ('body',), 'body depth and outside length', affects_geometry=True),
    _spec('device_diameter', 'reference', 'mm', 29.0, {'exclusive_min': 0.0}, 'reference_readout_only', (), 'nominal body and cap radial gap readouts', affects_geometry=False),
    _spec('axial_allowance', 'axial', 'mm', 5.0, {'min': 3.0, 'coupled_max_cavity': 300.0}, 'adjustable_geometry', ('body',), 'cavity and body depth', affects_geometry=True),
    _spec('cap_cavity_length', 'axial', 'mm', 81.0, {'exclusive_min': 0.0, 'coupled': 'useful cap and body shells'}, 'adjustable_geometry', ('body', 'cap'), 'complementary body depth and cap height', affects_geometry=True),
    _spec('body_bore', 'radial', 'mm', 30.0, {'locked': 30.0}, 'locked', ('body',), 'locked body bore', affects_geometry=True),
    _spec('cap_bore', 'radial', 'mm', 31.0, {'locked': 31.0}, 'locked', ('cap',), 'locked cap bore', affects_geometry=True),
    _spec('floor', 'ends', 'mm', 3.0, {'locked': 3.0}, 'locked', ('body', 'cap'), 'locked closed floors', affects_geometry=True),
    _spec('thread_pitch', 'thread', 'mm/rev', 2.0, {'locked': 2.0}, 'locked', ('body', 'cap', 'closed'), 'locked screw pitch and motion law', affects_geometry=True),
    _spec('engagement', 'thread', 'mm', 6.0, {'locked': 6.0}, 'locked', ('body', 'cap', 'closed'), 'locked full-form engagement', affects_geometry=True),
    _spec('thread_clearance', 'thread', 'mm_radial', 0.25, {'min': 0.20, 'max': 0.30}, 'adjustable_geometry', ('cap',), 'female thread void only', affects_geometry=True),
    _spec('clearance_budget', 'thread', 'mm_radial', 0.30, {'locked': 0.30}, 'locked', ('cap',), 'locked ligament feasibility budget', affects_geometry=True),
    _spec('thread_height', 'thread', 'mm_radial', 0.5, {'locked': 0.5}, 'locked', ('body', 'cap'), 'locked thread radial height', affects_geometry=True),
    _spec('root_wall', 'thread', 'mm_radial', 1.4, {'locked': 1.4}, 'locked', ('body', 'cap'), 'locked male-root wall', affects_geometry=True),
    _spec('cap_taper_length', 'thread', 'mm', 2.2, {'locked': 2.2}, 'locked', ('cap',), 'locked cap transition', affects_geometry=True),
    _spec('outer_diameter', 'exterior', 'mm', 39.0, {'exclusive_min': 0.0, 'max': 80.0, 'coupled': 'wall and skin feasibility'}, 'adjustable_geometry', ('body', 'cap'), 'common exterior crest diameter', affects_geometry=True),
    _spec('skin_axial_pitch', 'skin', 'mm', 4.8, {'min': 3.0, 'max': 8.0}, 'adjustable_geometry', ('body', 'cap'), 'diamond axial period', affects_geometry=True),
    _spec('skin_arc_pitch_target', 'skin', 'mm', 3.63, {'exclusive_min': 0.0, 'derived_count_min': 8, 'derived_count_max': 128}, 'adjustable_geometry', ('body', 'cap'), 'nearest integral circumferential count', affects_geometry=True),
    _spec('skin_height', 'skin', 'mm_radial', 0.45, {'exclusive_min': 0.0, 'max': 0.6}, 'adjustable_geometry', ('body', 'cap'), 'crest-to-valley relief', affects_geometry=True),
    _spec('plateau_half_fraction', 'skin', 'ratio', 0.18, {'exclusive_min': 0.0, 'exclusive_max': 0.5, 'coupled_min_plateau_mm': 1.0}, 'adjustable_geometry', ('body', 'cap'), 'blunt diamond plateau', affects_geometry=True),
    _spec('skin_phase_theta', 'skin', 'rad', 0.0, {'finite': True, 'resolvable': True}, 'adjustable_geometry', ('body', 'cap'), 'circumferential skin phase', affects_geometry=True),
    _spec('skin_phase_z', 'skin', 'mm', 0.0, {'finite': True, 'resolvable': True}, 'adjustable_geometry', ('body', 'cap'), 'axial skin phase', affects_geometry=True),
    _spec('end_chamfer_size', 'ends', 'mm', 1.20, {'min': 0.80, 'max': 1.50, 'exclusive_max_field': 'floor'}, 'adjustable_geometry', ('body', 'cap'), '45-degree closed-end chamfer', affects_geometry=True),
    _spec('drain_diameter', 'drains', 'mm', 3.0, {'locked': 3.0}, 'locked', ('body', 'cap'), 'locked seven-hole floor pattern', affects_geometry=True),
    _spec('drain_ring_radius', 'drains', 'mm', 9.0, {'locked': 9.0}, 'locked', ('body', 'cap'), 'locked drain ring radius', affects_geometry=True),
    _spec('drain_ring_count', 'drains', 'count', 6, {'locked': 6}, 'locked', ('body', 'cap'), 'locked ring count plus one center', affects_geometry=True),
    _spec('skin_style', 'skin', 'enum', 'diamond', {'locked': 'diamond'}, 'locked', ('body', 'cap'), 'locked P1 R7 procedural skin family', affects_geometry=True),
)


@dataclass(frozen=True)
class Parameters:
    device_length: float = 208.0
    device_diameter: float = 29.0
    axial_allowance: float = 5.0
    cap_cavity_length: float = 81.0
    body_bore: float = 30.0
    cap_bore: float = 31.0
    floor: float = 3.0
    thread_pitch: float = 2.0
    engagement: float = 6.0
    thread_clearance: float = 0.25
    clearance_budget: float = 0.30
    thread_height: float = 0.5
    root_wall: float = 1.4
    cap_taper_length: float = 2.2
    outer_diameter: float = 39.0
    skin_axial_pitch: float = 4.8
    skin_arc_pitch_target: float = 3.63
    skin_height: float = 0.45
    plateau_half_fraction: float = 0.18
    skin_phase_theta: float = 0.0
    skin_phase_z: float = 0.0
    end_chamfer_size: float = 1.20
    drain_diameter: float = 3.0
    drain_ring_radius: float = 9.0
    drain_ring_count: int = 6
    skin_style: str = 'diamond'


def preset(name='laifen_wave_r7', **overrides):
    if name not in ('laifen_wave_r7', 'laifen-wave'):
        raise ValueError('unknown container preset')
    return replace(Parameters(), **overrides)


def parameter_fingerprint(parameters):
    return sha256(json.dumps(asdict(parameters), sort_keys=True, separators=(',', ':'),
                             allow_nan=False).encode()).hexdigest()


__all__ = ['PARAMETER_SPECS', 'Parameters', 'preset', 'parameter_fingerprint']
