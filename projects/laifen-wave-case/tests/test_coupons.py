"""Focused CDE-01 regression gates: profile fidelity, solids, stop and motion.

These gates test actual solids: a numerically correct parameter table cannot
pass a changed sweep profile, detached grip, blocked bore or misplaced cap.
"""
import json
import math
from pathlib import Path
import sys

import pytest
from build123d import Align, Axis, Box, Edge, Location, Vector
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN
from OCP.gp import gp_Pnt

SOURCE = Path(__file__).parents[1] / "cad" / "p1_r2_coupons"
sys.path.insert(0, str(SOURCE))
import coupon as c
CLASSIFIERS={}


@pytest.fixture(scope="module")
def parts():
    return {"M":c.male(), **{str(g):c.cap(g) for g in c.CLEARANCES}}


def radial_surface(shape, theta, z, female=False):
    """Binary solid classification measures the real material boundary."""
    low,high = (16.0,18.0)
    if id(shape) not in CLASSIFIERS:
        CLASSIFIERS[id(shape)] = BRepClass3d_SolidClassifier(shape.solids()[0].wrapped)
    classifier=CLASSIFIERS[id(shape)]
    for _ in range(15):
        radius=(low+high)/2
        classifier.Perform(gp_Pnt(radius*math.cos(theta),radius*math.sin(theta),z),1e-8)
        inside=classifier.State()==TopAbs_IN
        if inside == female:
            high=radius
        else:
            low=radius
    return (low+high)/2


def volume_of(result):
    if result is None:
        return 0.0
    if isinstance(result,list):
        return sum(item.volume for item in result)
    return result.volume


def test_math_and_allowed_domain():
    """Catch consumed wall budget, steep starts, and contract parameter drift."""
    with pytest.raises(ValueError): c.cap(.225)
    assert c.ROOT-c.BORE == pytest.approx(1.8)
    assert c.FULL_END-c.FULL_START == 3*c.PITCH
    assert .85+c.EMBED/(6/7) == pytest.approx(.908333333333)
    assert math.atan(6/7) < math.pi/4
    assert 2*c.K*c.A*c.B/math.hypot(c.A,c.B) == pytest.approx(1)
    assert math.hypot(c.XT,c.K*c.A) == pytest.approx(18.5)
    assert (c.XT-c.XB)/(c.B*(1-c.K)) < 1
    for gap in c.CLEARANCES:
        assert c.COLLAR_R-(c.CREST+gap) >= 1.8-1e-12
        assert (c.CREST+gap-15.5)/2.2 <= 1+1e-12


def test_actual_topology_dimensions_datums(parts):
    """Catch disconnected cells, capped male, wrong bounds/floor or datums."""
    for role,part in parts.items():
        assert part.is_valid
        assert len(part.solids()) == 1
        assert part.volume > 0
        bb=part.bounding_box()
        assert bb.size.X <= 39.00001 and bb.size.Y <= 39.00001
        # OCC bounds for the trimmed swept surface overestimate mouth Z by
        # 0.008716; material, exact vertices and the planar stop define height.
        zmin=min(v.Z for v in part.vertices())
        zmax=max(v.Z for v in part.vertices())
        assert zmax-zmin == pytest.approx(17 if role=="M" else 25,abs=1e-5)
        forbidden=Box(50,50,.1,align=(Align.CENTER,Align.CENTER,Align.MAX)).moved(Location((0,0,zmin-1e-6)))
        assert volume_of(part.intersect(forbidden)) <= 1e-6
        assert {"screw_axis","shoulder","tip","bed","full_thread_start","full_thread_end","grip_phase"} <= set(part.joints)
    male=parts["M"].solids()[0]
    for z in (-7.9,-4,0,4,8.9):
        assert not male.is_inside((0,0,z))
        assert not male.is_inside((14.99,0,z))
    for gap in c.CLEARANCES:
        solid=parts[str(gap)].solids()[0]
        assert not solid.is_inside((10,0,21.99))
        assert solid.is_inside((10,0,22.01))
        assert solid.is_inside((10,0,24.99))


def test_actual_phase_sections(parts):
    """Catch sweep-frame distortion and min/max envelope implementation errors."""
    errors=[]
    zs=(.001,.5,1,1.15,1.5,1.85,2,2.15,2.5,2.85,3,4,4.15,6.5,7,7.85,8,8.15,8.5,8.85,8.999)
    for theta in (0,math.pi/2,math.pi,3*math.pi/2):
        for z in zs:
            actual=radial_surface(parts["M"],theta,z)
            errors.append((abs(actual-c.male_radius(theta,z)),"M",theta,z))
            for gap in c.CLEARANCES:
                actual=radial_surface(parts[str(gap)],theta,z,True)
                errors.append((abs(actual-c.female_radius(theta,z,gap)),str(gap),theta,z))
    assert max(errors)[0] <= c.PROFILE_TOLERANCE, max(errors)
    for z in (3,7):
        assert not parts["M"].solids()[0].is_inside((17.2,0,z)), ("filled male valley",z)
    print("maximum_radial_section_error_mm",max(errors))


def test_actual_grip_cells():
    """Catch curved/undersized tips, detached corners or incomplete rows."""
    cells=c.grip_cells()
    assert len(cells)==62
    for cell in cells:
        assert cell.is_valid and len(cell.solids())==1
        assert cell.bounding_box().min.Z >= 14.4-1e-7
        assert cell.bounding_box().max.Z <= 20.0+1e-7
        for vertex in cell.vertices():
            assert math.hypot(vertex.X,vertex.Y) <= 18.5+1e-7
    canonical=c.grip_cell()
    assert len(canonical.faces())==6
    for face in canonical.faces():
        assert str(face.geom_type).endswith("PLANE")
        n=face.normal_at()
        assert abs(n.Z)/math.hypot(n.X,n.Y) <= 1+1e-9
    tip=max(canonical.faces(),key=lambda f:f.center().X)
    center=tip.center()
    assert 2*min(edge.distance_to(center) for edge in tip.edges()) >= 1-1e-7
    shell=c.turned([(15.5,-2),(17.9,-2),(17.9,2),(15.5,2)])
    assert volume_of(canonical.intersect(shell)) > 0


def test_actual_screw_path_and_positive_stop(parts):
    """Catch interference during entry/removal and failure of external stop."""
    male=parts["M"]
    results=[]
    for gap in c.CLEARANCES:
        cap=parts[str(gap)]
        for beta in (0,15,45,90,180,360,720,1080,1440,1620):
            dz=c.PITCH*beta/360
            moved=c.screw_pose(gap,beta).children[1]
            assert moved.location.position.Z == pytest.approx(dz,abs=1e-8)
            actual_angle=math.radians(moved.location.orientation.Z)
            assert math.sin(actual_angle)==pytest.approx(math.sin(math.radians(beta)),abs=1e-8)
            assert math.cos(actual_angle)==pytest.approx(math.cos(math.radians(beta)),abs=1e-8)
            volume=volume_of(male.intersect(moved))
            results.append((gap,beta,dz,volume))
            print("screw_pose",gap,beta,dz,volume,flush=True)
            assert volume <= 1e-6,(gap,beta,volume)
        for dz in (9,10,11):
            moved=cap.moved(Location((0,0,dz),(0,0,1620)))
            volume=volume_of(male.intersect(moved))
            print("straight_extraction",gap,dz,volume,flush=True)
            assert volume <= 1e-6
        blocked=cap.moved(Location((0,0,-.02),(0,0,-3.6)))
        stop_volume=volume_of(male.intersect(blocked))
        print("negative_stop",gap,stop_volume,flush=True)
        assert stop_volume > .1
        assembled=c.screw_pose(gap,15)
        assert min(v.Z for v in assembled.children[1].vertices()) == pytest.approx(1/12,abs=1e-6)
    print("screw_path_actual_intersections",json.dumps(results))
