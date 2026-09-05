"""Normalize only tolerance-covered endpoint trims on the new closed-end cone."""
from math import pi
import json
import sys
from build123d import GeomType
from OCP.BRep import BRep_Builder,BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve,BRepAdaptor_Surface
from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy
from OCP.GeomAPI import GeomAPI_ProjectPointOnCurve
from .params import derive,require


def end_cone(shape,p,role):
    d=derive(p);end=d.body_band[0] if role=='body' else d.cap_band[1]
    require(role in ('body','cap'),'unknown closed-end role')
    def local(face):
        box=face.bounding_box()
        lo,hi=(box.min.Z-end,box.max.Z-end) if role=='body' else (end-box.max.Z,end-box.min.Z)
        return lo>=-.02 and hi<=p.end_chamfer_size+.02
    cones=[f for f in shape.faces() if f.geom_type==GeomType.CONE and local(f)
           and abs(abs(BRepAdaptor_Surface(f.wrapped).Cone().SemiAngle())-pi/4)<1e-8]
    require(len(cones)==1,'expected one end-local45degree conical face')
    return cones[0]


def end_endpoint_defects(shape,p,role):
    defects=[]
    for edge in end_cone(shape,p,role).edges():
        curve=BRepAdaptor_Curve(edge.wrapped);ends=(curve.FirstParameter(),curve.LastParameter())
        for vertex in edge.vertices():
            pt=BRep_Tool.Pnt_s(vertex.wrapped)
            parameter=min(ends,key=lambda t:curve.Value(t).Distance(pt))
            residual=curve.Value(parameter).Distance(pt)
            if residual>1e-6: defects.append(dict(edge=edge,vertex=vertex,parameter=parameter,residual=residual,interval=ends))
    return defects


def normalize_end_trim(shape,p,role):
    """Keep curves, surfaces, coordinates and tolerances; shorten existing trims."""
    before=end_endpoint_defects(shape,p,role)
    require(len(before)<=4*derive(p).lattice_count,'unexpected end-edge defect count')
    if not before:return shape
    fixed=type(shape)(BRepBuilderAPI_Copy(shape.wrapped,False,False).Shape())
    defects=end_endpoint_defects(fixed,p,role);builder=BRep_Builder();after=[]
    for defect in defects:
        edge,vertex=defect['edge'],defect['vertex'];pt=BRep_Tool.Pnt_s(vertex.wrapped)
        curve=BRep_Tool.Curve_s(edge.wrapped,0.,0.)
        current=BRepAdaptor_Curve(edge.wrapped);first,last=current.FirstParameter(),current.LastParameter()
        require(defect['residual']<=1e-4,'end-edge mismatch exceeds local normalization bound')
        projection=GeomAPI_ProjectPointOnCurve(pt,curve,first,last)
        require(projection.NbPoints()>0 and projection.LowerDistance()<=1e-7,'end vertex is not on existing curve')
        new=projection.LowerDistanceParameter()
        require(first<=new<=last,'end trim would extend existing curve')
        require(abs(new-defect['parameter'])<=.01*(last-first),'end trim exceeds one-percent bound')
        interval=(new,last) if defect['parameter']==defect['interval'][0] else (first,new)
        require(interval[0]<interval[1],'end trim collapses edge')
        tolerance=BRep_Tool.Tolerance_s(vertex.wrapped)
        builder.Range(edge.wrapped,*interval,False)
        builder.UpdateVertex(vertex.wrapped,new,edge.wrapped,tolerance)
        require(BRep_Tool.Tolerance_s(vertex.wrapped)==tolerance,'end vertex tolerance changed')
        after.append(curve.Value(new).Distance(pt))
    require(fixed.is_valid and len(fixed.solids())==1,'end trim damaged closed solid')
    require(not end_endpoint_defects(fixed,p,role),'end trim left a detectable mismatch')
    print(json.dumps({'stage':role+'_native_end_trim','count':len(defects),
                      'max_before':max(d['residual'] for d in before),'max_after':max(after)}),file=sys.stderr,flush=True)
    return fixed
