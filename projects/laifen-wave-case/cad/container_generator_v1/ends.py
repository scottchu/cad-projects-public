"""Closed-end chamfer construction and bounded endpoint normalization."""
from .chamfer import CUTTER_EPSILON, apply_end_chamfer, end_chamfer_cutter, end_chamfer_radius
from .end_trim import end_cone, end_endpoint_defects, normalize_end_trim

__all__ = [
    'CUTTER_EPSILON', 'apply_end_chamfer', 'end_chamfer_cutter',
    'end_chamfer_radius', 'end_cone', 'end_endpoint_defects',
    'normalize_end_trim',
]
