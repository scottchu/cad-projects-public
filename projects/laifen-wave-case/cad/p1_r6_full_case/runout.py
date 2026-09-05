"""Local trim/vertex consistency at the female upper helical runout.

The Boolean can leave a tolerance-covered edge endpoint near z=neck_height.
Normalize only its parameter trim against its existing vertex before export.
No underlying curve/surface, vertex coordinate or tolerance is changed.
"""
from math import hypot
import json
import sys
from build123d import GeomType
from OCP.BRep import BRep_Builder,BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from .params import derive,require

ENDPOINT_LIMIT=1e-7
DEFECT_THRESHOLD=1e-4
MAX_CORRECTION=.01


def runout_endpoint_mismatches(shape,p,threshold=DEFECT_THRESHOLD):
    """Find the named helical/conical upper-runout role without face indices."""
    d=derive(p);radius=d.thread_crest+p.thread_clearance
    faces=shape.faces()
    cones=[f for f in faces if f.geom_type==GeomType.CONE]
    helices=[f for f in faces if f.geom_type==GeomType.BSPLINE]
    matches=[];seen=[]
    for cone in cones:
        for edge in cone.edges():
            if any(edge.wrapped.IsSame(e.wrapped) for e in seen):continue
            if not any(any(edge.wrapped.IsSame(other.wrapped) for other in f.edges()) for f in helices):continue
            seen.append(edge)
            curve=BRepAdaptor_Curve(edge.wrapped)
            ends=(curve.FirstParameter(),curve.LastParameter())
            for vertex in edge.vertices():
                point=BRep_Tool.Pnt_s(vertex.wrapped)
                if abs(point.Z()-d.neck_height)>1e-6 or abs(hypot(point.X(),point.Y())-radius)>1e-4:continue
                parameter=min(ends,key=lambda t:curve.Value(t).Distance(point))
                residual=curve.Value(parameter).Distance(point)
                if residual>threshold:
                    matches.append(dict(edge=edge,vertex=vertex,parameter=parameter,
                                        interval=ends,residual=residual))
    return matches


def normalize_female_runout(shape,p):
    """Return an isolated topology copy with the single bounded trim corrected."""
    before=runout_endpoint_mismatches(shape,p)
    require(len(before)<=1,'multiple upper-runout defects need separate diagnosis')
    if not before:return shape
    # Clone topology, retaining exact underlying geometry; do not mutate cached
    # female-void tools, source shapes or other occurrences sharing a TShape.
    copied=BRepBuilderAPI_Copy(shape.wrapped,False,False).Shape()
    fixed=type(shape)(copied)
    matches=runout_endpoint_mismatches(fixed,p)
    require(len(matches)==1,'upper-runout witness changed during topology copy')
    match=matches[0];edge=match['edge'];vertex=match['vertex']
    point=BRep_Tool.Pnt_s(vertex.wrapped)
    curve=BRep_Tool.Curve_s(edge.wrapped,0.,0.)
    first,last=match['interval'];parameter=match['parameter']
    require(match['residual']<=MAX_CORRECTION,'upper-runout mismatch exceeds bounded correction')
    projection=GeomAPI_ProjectPointOnCurve(point,curve,first,last)
    require(projection.NbPoints()>0,'cannot project upper-runout vertex')
    new_parameter=projection.LowerDistanceParameter()
    require(projection.LowerDistance()<=ENDPOINT_LIMIT,'upper-runout vertex is not on existing curve')
    require(first<=new_parameter<=last,'runout correction would extend the curve')
    interval=(new_parameter,last) if parameter==first else (first,new_parameter)
    require(interval[0]<interval[1],'runout correction collapses edge')
    require(abs(new_parameter-parameter)<=.01*(last-first),'runout correction exceeds trim fraction bound')
    tolerance=BRep_Tool.Tolerance_s(vertex.wrapped)
    builder=BRep_Builder()
    builder.Range(edge.wrapped,*interval,False)
    builder.UpdateVertex(vertex.wrapped,new_parameter,edge.wrapped,tolerance)
    residual=curve.Value(new_parameter).Distance(point)
    require(residual<=ENDPOINT_LIMIT,'corrected runout endpoint remains inconsistent')
    require(BRep_Tool.Tolerance_s(vertex.wrapped)==tolerance,'vertex tolerance changed during trim correction')
    require(fixed.is_valid and len(fixed.solids())==1,'runout correction broke closed solid')
    print(json.dumps({'stage':'female_runout_trim','corrections':1,'before_residual':match['residual'],
                      'after_residual':residual,'before_range':[first,last],'after_range':interval,
                      'vertex_tolerance_unchanged':tolerance}),file=sys.stderr,flush=True)
    return fixed
