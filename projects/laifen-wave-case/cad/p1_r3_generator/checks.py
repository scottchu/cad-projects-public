"""Focused geometric diagnostics; no source or tolerance healing."""
import math
from OCP.BRepAdaptor import BRepAdaptor_Surface,BRepAdaptor_Curve,BRepAdaptor_Curve2d
from OCP.BRep import BRep_Tool
from OCP.GeomAbs import GeomAbs_Cylinder,GeomAbs_BSplineCurve,GeomAbs_BezierCurve,GeomAbs_Line,GeomAbs_Circle
from .params import derive,require


def mouth_face(part,p):
    d=derive(p)
    faces=[]
    for face in part.faces():
        ad=BRepAdaptor_Surface(face.wrapped)
        if ad.GetType()==GeomAbs_Cylinder and abs(ad.Cylinder().Radius()-(d.thread_crest+p.thread_clearance))<1e-7:
            if max(v.Z for v in face.vertices())<=.5*p.thread_pitch+.01:faces.append(face)
    require(len(faces)==1,f'expected one mouth cylinder; found{len(faces)}')
    return faces[0]


def mouth_report(part,p):
    face=mouth_face(part,p);surface=BRepAdaptor_Surface(face.wrapped);records=[]
    for index,edge in enumerate(face.edges()):
        c=BRepAdaptor_Curve(edge.wrapped);first,last=c.FirstParameter(),c.LastParameter()
        pts=[c.Value(first),c.Value(last)]
        vertices=[(BRep_Tool.Pnt_s(v.wrapped),BRep_Tool.Tolerance_s(v.wrapped)) for v in edge.vertices()]
        error=max(min(point.Distance(v) for v,t in vertices) for point in pts)
        controls=None
        if c.GetType() in (GeomAbs_BSplineCurve,GeomAbs_BezierCurve):
            curve=(c.BSpline() if c.GetType()==GeomAbs_BSplineCurve else c.Bezier()).Copy()
            curve.Segment(first,last)
            controls=[[curve.Pole(i).X(),curve.Pole(i).Y(),curve.Pole(i).Z()] for i in range(1,curve.NbPoles()+1)]
            low,high=min(x[2] for x in controls),max(x[2] for x in controls)
        elif c.GetType()==GeomAbs_Line:low,high=min(x.Z() for x in pts),max(x.Z() for x in pts)
        elif c.GetType()==GeomAbs_Circle:
            circle=c.Circle();dz=circle.Radius()*math.hypot(circle.XAxis().Direction().Z(),circle.YAxis().Direction().Z())
            low,high=circle.Location().Z()-dz,circle.Location().Z()+dz
        else:raise ValueError(f'unhandled mouth curve{c.GetType()}')
        pc=BRepAdaptor_Curve2d(edge.wrapped,face.wrapped)
        lifted=[]
        for t in (pc.FirstParameter(),pc.LastParameter()):
            uv=pc.Value(t);lifted.append(surface.Value(uv.X(),uv.Y()))
        lift_error=max(a.Distance(b) for a,b in zip(pts,lifted))
        record=dict(edge=index,type=str(c.GetType()),range=[first,last],
                    endpoints=[[a.X(),a.Y(),a.Z()] for a in pts],
                    vertices=[dict(point=[a.X(),a.Y(),a.Z()],tolerance=t) for a,t in vertices],
                    endpoint_error=error,lifted_endpoint_error=lift_error,z_bounds=[low,high],trimmed_controls=controls)
        records.append(record)
        require(error<=1e-4,f'mouth endpoint mismatch: {record}')
        require(lift_error<=1e-4,f'mouth pcurve endpoint mismatch: {record}')
        require(low>=-1e-4,f'mouth curve extends below plane: {record}')
        if all(abs(v.Z())<1e-4 for v,t in vertices) and c.GetType() in (GeomAbs_Line,GeomAbs_Circle):
            require(max(abs(low),abs(high))<=1e-4,f'mouth-plane curve not in plane: {record}')
    require(part.is_valid,'source invalid after read-only inspection')
    return dict(edges=records,maximum_endpoint_error=max(r['endpoint_error'] for r in records),
                maximum_lifted_endpoint_error=max(r['lifted_endpoint_error'] for r in records),
                minimum_z_bound=min(r['z_bounds'][0] for r in records),
                maximum_native_tolerance=max(v['tolerance'] for r in records for v in r['vertices']))


def normalized_speed(c):
    width=c.LastParameter()-c.FirstParameter()
    if c.GetType()==GeomAbs_Circle:return width*c.Circle().Radius()
    if c.GetType()==GeomAbs_Line:return width
    require(c.GetType()==GeomAbs_BSplineCurve,'unsupported correspondence curve')
    bs=c.BSpline();require(not bs.IsRational() and not bs.IsPeriodic(),'unsupported rational/periodic mouth curve')
    degree=bs.Degree();knots=[]
    for i in range(1,bs.NbKnots()+1):knots.extend([bs.Knot(i)]*bs.Multiplicity(i))
    return width*max(degree*bs.Pole(i+1).Distance(bs.Pole(i+2))/(knots[i+degree+1]-knots[i+1]) for i in range(bs.NbPoles()-1))


def at(c,t):return c.Value(c.FirstParameter()+(c.LastParameter()-c.FirstParameter())*t)


def mouth_correspondence(source,written,p):
    """Bijective full-edge matching plus derivative-bounded continuous error."""
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    a=[BRepAdaptor_Curve(e.wrapped) for e in mouth_face(source,p).edges()]
    b=[BRepAdaptor_Curve(e.wrapped) for e in mouth_face(written,p).edges()]
    require(len(a)==len(b),'mouth edge counts differ')
    cost=np.zeros((len(a),len(b)));reverse={}
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            forward=max(at(x,t).Distance(at(y,t)) for t in (0,.25,.5,.75,1))
            backward=max(at(x,t).Distance(at(y,1-t)) for t in (0,.25,.5,.75,1))
            cost[i,j]=min(forward,backward);reverse[i,j]=backward<forward
    rows=[]
    for i,j in zip(*linear_sum_assignment(cost)):
        x,y=a[i],b[j];L=normalized_speed(x)+normalized_speed(y)
        n=max(64,math.ceil(L/(2*.0002)))
        maximum=max(at(x,k/n).Distance(at(y,1-k/n if reverse[i,j] else k/n)) for k in range(n+1))
        bound=maximum+L/(2*n)
        rows.append(dict(source=int(i),written=int(j),reversed=reverse[i,j],samples=n+1,
                         derivative_bound=L,sampled_error=maximum,continuous_bound=bound))
        require(bound<=.001,f'mouth source/STEP bound exceeds.001: {rows[-1]}')
    return dict(edges=rows,maximum_continuous_bound=max(r['continuous_bound'] for r in rows))
