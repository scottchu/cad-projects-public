"""Fresh-process destructive BREP gates for all six tooth/roller poses.

OpenCascade in this environment accumulates enough state from repeated 260T
ring-gear subtraction booleans to crash a long-lived process.  Every case is
therefore built and intersected in its own Python process.  This is deliberate:
all H/M/S roles and nominal/+0.25 mm tower positions still exercise the actual
involute tooth solid, without allowing one pose to contaminate the next.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _actual_motor_mesh_case(q: float, phase: float) -> dict:
    """Build one unchanged 260T/16T mesh pose in its own OCC process."""

    program = r'''
import json
from math import cos, radians, sin
import sys

import py_gearworks as pgw
from build123d import Axis, Location

from p3_v3_direct_gear_race_guidance_geometry import make_output_pinion
from p3_v3_direct_gear_race_guidance_spec import P3_V3_DIRECT_GEAR_RACE as p

q = float(sys.argv[1])
phase = float(sys.argv[2])
role = 0
z0, z1 = p.pinion_face_ranges[role]
ring = pgw.SpurRingGear(
    number_of_teeth=p.ring_teeth,
    module=p.module,
    height=z1-z0,
    center=[0, 0, z0],
    backlash=0.10,
).build_part().solid().rotate(Axis.Z, p.tooth_phase_offset_degrees + phase)

station_angle = radians(p.motor_station_angles[role])
dx, dy = q*cos(station_angle), q*sin(station_angle)
pinion = make_output_pinion(role, p).moved(Location((dx, dy, 0)))
axis_radius = p.output_axis_radius + q
pinion_axis = Axis(
    (axis_radius*cos(station_angle), axis_radius*sin(station_angle), 0),
    (0, 0, 1),
)
pinion = pinion.rotate(pinion_axis, phase*p.gear_ratio)
hit = ring.intersect(pinion)
volume = sum(s.volume for s in hit.solids()) if hit else 0.0
print(json.dumps({"q": q, "phase": phase, "volume": volume, "distance": ring.distance_to(pinion)}))
'''
    completed = subprocess.run(
        [sys.executable, "-c", program, str(q), str(phase)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=90,
        check=True,
    )
    return json.loads(completed.stdout.splitlines()[-1])


@pytest.mark.parametrize("q", (-0.35, 0.10))
@pytest.mark.parametrize("phase", (-0.6923, -0.3462, 0.0, 0.3462, 0.6923))
def test_actual_unchanged_260t_16t_mesh_is_collision_free_in_powered_window(q, phase):
    result = _actual_motor_mesh_case(q, phase)
    assert result["volume"] <= 1e-7
    if q == pytest.approx(0.10):
        assert result["distance"] >= 0.06


@pytest.mark.parametrize(
    "q,expected_mode",
    ((0.0, "nominal_reserve"), (0.20, "contact_no_reserve"), (0.25, "collision")),
)
def test_actual_tooth_mesh_rejects_adjustments_beyond_powered_window(q, expected_mode):
    result = _actual_motor_mesh_case(q, 0.0)
    if expected_mode == "nominal_reserve":
        assert result["volume"] <= 1e-7
        assert result["distance"] == pytest.approx(0.099866, abs=0.001)
    elif expected_mode == "contact_no_reserve":
        assert result["volume"] <= 1e-7
        assert result["distance"] <= 1e-7
    else:
        assert result["volume"] > 0.06
        assert result["distance"] <= 1e-7


@pytest.mark.parametrize("role", range(3))
@pytest.mark.parametrize("delta", (0.0, 0.25))
def test_actual_260t_brep_has_zero_intersection_with_relived_roller(role, delta):
    program = f"""
import json
import py_gearworks as pgw
from build123d import Axis
from p3_v3_direct_gear_race_guidance_geometry import make_roller
from p3_v3_direct_gear_race_guidance_spec import P3_V3_DIRECT_GEAR_RACE as p
role={role}; delta={delta!r}
z0,z1=p.pinion_face_ranges[role]
teeth=pgw.SpurRingGear(number_of_teeth=p.ring_teeth,module=p.module,height=z1-z0,center=[0,0,z0],backlash=0.10).build_part().solid().rotate(Axis.Z,p.tooth_phase_offset_degrees)
roller=make_roller(role,2,p.roller_axis_radius+delta)
hit=teeth.intersect(roller)
volume=sum(s.volume for s in hit.solids()) if hit else 0.0
print(json.dumps({{"role":role,"delta":delta,"volume":volume,"distance":teeth.distance_to(roller)}}))
"""
    result = subprocess.run([sys.executable, "-c", program], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    actual = json.loads(result.stdout)
    assert actual["role"] == role and actual["delta"] == pytest.approx(delta)
    assert actual["volume"] <= 1e-7
    assert actual["distance"] >= 0.099
