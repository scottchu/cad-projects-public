"""Source-authored P1 R7 assembly and print placements."""

from build123d import Compound, Location

from .parts import build_body, build_cap


def build_assembly(resolved, beta_degrees=0., gap=None):
    body = build_body(resolved).moved(Location())
    cap = build_cap(resolved).moved(Location())
    axial_position = resolved.thread_pitch * beta_degrees / 360 if gap is None else gap
    body.joints['screw_axis'].connect_to(
        cap.joints['shoulder'], position=axial_position, angle=beta_degrees)
    return Compound(
        label=(f'R7 new B threaded cylinder C{round(resolved.thread_clearance*100):02}; '
               f'angle{beta_degrees:g}; gap{axial_position:g}'),
        children=[body, cap],
    )


def print_layout(resolved):
    body = build_body(resolved).moved(Location(resolved.body_print_translation))
    cap = build_cap(resolved).moved(Location(
        resolved.cap_print_translation, resolved.cap_print_rotation))
    return Compound(
        label=(f'R7 body and C{round(resolved.thread_clearance*100)} cap; '
               'both openings up; two print objects'),
        children=[body, cap],
    )


__all__ = ['build_assembly', 'print_layout']
