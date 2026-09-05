"""DES-SKIN-02 rational Bezier skin, exact shared 3D edges and UV p-curves."""
from dataclasses import dataclass
from math import ceil, comb, cos, factorial, floor, pi, sin, tan
from time import monotonic
import numpy as np
from OCP.BRep import BRep_Builder
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeSolid, BRepBuilderAPI_MakeVertex, BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_Sewing)
from OCP.Geom import Geom_BezierCurve, Geom_BezierSurface
from OCP.Geom2d import Geom2d_BezierCurve
from OCP.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array2OfPnt
from OCP.TColStd import TColStd_Array1OfReal, TColStd_Array2OfReal
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt, gp_Pnt2d
from build123d import Face, Shell, Solid
try:
    from .params import derive, require
    from .skin import facet_polygons, radius
except ImportError:
    from params import derive, require
    from skin import facet_polygons, radius

TOLERANCE=1e-7


def add(a,b):
    c=np.zeros((max(a.shape[0],b.shape[0]),max(a.shape[1],b.shape[1])))
    c[:a.shape[0],:a.shape[1]]+=a;c[:b.shape[0],:b.shape[1]]+=b
    return c


def mul(a,b):
    c=np.zeros((a.shape[0]+b.shape[0]-1,a.shape[1]+b.shape[1]-1))
    for i,j in np.ndindex(a.shape):
        c[i:i+b.shape[0],j:j+b.shape[1]]+=a[i,j]*b
    return c


def bernstein_to_power(b):
    n=len(b)-1;c=np.zeros(n+1)
    for k,v in enumerate(b):
        for j in range(n-k+1):c[k+j]+=v*comb(n,k)*comb(n-k,j)*(-1)**j
    return c


def power_to_bernstein(a,degree):
    out=np.zeros((degree[0]+1,degree[1]+1))
    for k,l in np.ndindex(out.shape):
        out[k,l]=sum(a[i,j]*comb(k,i)/comb(degree[0],i)*comb(l,j)/comb(degree[1],j)
                     for i in range(min(k+1,a.shape[0])) for j in range(min(l+1,a.shape[1])))
    return out


def compose_line(a,start,end):
    """Exact polynomial substitution t=t0+q*dt, s=s0+q*ds."""
    out=np.zeros(sum(a.shape)-1)
    for i,j in np.ndindex(a.shape):
        if a[i,j]==0:continue
        t=np.array([comb(i,k)*start[0]**(i-k)*(end[0]-start[0])**k for k in range(i+1)])
        s=np.array([comb(j,k)*start[1]**(j-k)*(end[1]-start[1])**k for k in range(j+1)])
        v=np.convolve(t,s)*a[i,j];out[:len(v)]+=v
    while len(out)>1 and abs(out[-1])<1e-14:out=out[:-1]
    return out


def clip(poly,axis,bound,sign):
    out=[]
    if not poly:return out
    prev=poly[-1];ap=sign*(prev[axis]-bound)
    for curr in poly:
        ac=sign*(curr[axis]-bound)
        if (ac>=0)!=(ap>=0):
            t=ap/(ap-ac);out.append(tuple(prev[k]+t*(curr[k]-prev[k]) for k in range(2)))
        if ac>=0:out.append(curr)
        prev,ap=curr,ac
    clean=[]
    for v in out:
        if not clean or np.linalg.norm(np.subtract(v,clean[-1]))>1e-11:clean.append(v)
    if len(clean)>1 and np.linalg.norm(np.subtract(clean[0],clean[-1]))<1e-11:clean.pop()
    return clean


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0


def route_bounds(p):
    d=derive(p);require(p.skin_style=='diamond','STEP currently supports diamond only')
    m=1
    while True:
        delta=2*pi/(m*d.lattice_count);a=delta/2
        warp=.5*max(delta-2*sin(a),4*tan(a/2)-delta)
        angular=p.skin_height*d.lattice_count/(2*pi*(.5-p.plateau_half_fraction))*warp
        if angular<=.0025:break
        m+=1
        require(m<=8,'angular patch multiplication exceeds bounded route')
    fade=p.skin_height*pi**8/(2*factorial(8)*256)
    slope=p.skin_height*(1/(p.skin_axial_pitch*(.5-p.plateau_half_fraction))+(7-pi*pi/2)/p.fade_length)
    require(angular+fade<=.004,'rational route radial bound > .004')
    require(slope<=1,'rational fade slope bound > 1')
    plateau=min(d.body_plateau_width,d.cap_plateau_width)*sin(a)/a
    require(plateau>=1,'warped plateau width bound < 1')
    return dict(m=m,radial_bound=angular+fade,angular_bound=angular,fade_bound=fade,slope_bound=slope,plateau_bound=plateau)


@dataclass
class Patch:
    polynomials: tuple
    polygon: list
    keys: list
    kind: str
    surface: object=None
    face: object=None


class Builder:
    """Single canonical edge/vertex namespace; positions never rounded for CAD."""
    def __init__(self):
        self.vertices={};self.edges={};self.uses={};self.faces=[];self.patches=[]
        self.max_join_error=0.

    def edge(self,patch,a,b,ka,kb):
        reverse=ka>kb
        if reverse:a,b,ka,kb=b,a,kb,ka
        key=(ka,kb)
        coeffs=[compose_line(c,a,b) for c in patch.polynomials]
        degree=max(map(len,coeffs))-1
        bs=[power_to_bernstein(c[:,None],(degree,0))[:,0] for c in coeffs]
        poles=TColgp_Array1OfPnt(1,degree+1);weights=TColStd_Array1OfReal(1,degree+1)
        for i in range(degree+1):
            require(bs[3][i]>0,'nonpositive edge weight')
            poles.SetValue(i+1,gp_Pnt(*(bs[j][i]/bs[3][i] for j in range(3))))
            weights.SetValue(i+1,float(bs[3][i]))
        curve=Geom_BezierCurve(poles,weights)
        for k,q in ((ka,0.),(kb,1.)):
            pt=curve.Value(q)
            if k not in self.vertices:self.vertices[k]=(BRepBuilderAPI_MakeVertex(pt).Vertex(),pt)
            else:
                error=pt.Distance(self.vertices[k][1]);self.max_join_error=max(self.max_join_error,error)
                require(error<1e-8,f'canonical vertex mismatch {error}')
        if key not in self.edges:
            self.edges[key]=BRepBuilderAPI_MakeEdge(curve,self.vertices[ka][0],self.vertices[kb][0],0.,1.).Edge()
        else:
            # Comparison at interior points catches equal-endpoint but different curves.
            from OCP.BRep import BRep_Tool
            existing=BRep_Tool.Curve_s(self.edges[key],0.,1.)
            for q in (.25,.5,.75):
                error=curve.Value(q).Distance(existing.Value(q));self.max_join_error=max(self.max_join_error,error)
                require(error<1e-8,f'canonical edge mismatch {error}')
        points=TColgp_Array1OfPnt2d(1,2)
        points.SetValue(1,gp_Pnt2d(*a));points.SetValue(2,gp_Pnt2d(*b))
        pcurve=Geom2d_BezierCurve(points)
        BRep_Builder().UpdateEdge(self.edges[key],pcurve,patch.surface,TopLoc_Location(),TOLERANCE)
        self.uses[key]=self.uses.get(key,0)+1
        return self.edges[key].Reversed() if reverse else self.edges[key]

    def add(self,patch,reverse=False):
        degree=tuple(max(c.shape[k] for c in patch.polynomials)-1 for k in (0,1))
        bs=[power_to_bernstein(c,degree) for c in patch.polynomials]
        poles=TColgp_Array2OfPnt(1,degree[0]+1,1,degree[1]+1)
        weights=TColStd_Array2OfReal(1,degree[0]+1,1,degree[1]+1)
        for i,j in np.ndindex(bs[3].shape):
            w=bs[3][i,j];require(w>0,'nonpositive surface weight')
            poles.SetValue(i+1,j+1,gp_Pnt(*(bs[k][i,j]/w for k in range(3))))
            weights.SetValue(i+1,j+1,float(w))
        patch.surface=Geom_BezierSurface(poles,weights)
        wire=BRepBuilderAPI_MakeWire()
        for n,a in enumerate(patch.polygon):
            m=(n+1)%len(patch.polygon)
            edge=self.edge(patch,a,patch.polygon[m],patch.keys[n],patch.keys[m])
            wire.Add(TopoDS.Edge_s(edge))
        face=BRepBuilderAPI_MakeFace(patch.surface,wire.Wire(),True).Face()
        if reverse:face=TopoDS.Face_s(face.Reversed())
        patch.face=face;self.faces.append(face);self.patches.append(patch)
        return patch

    def solid(self):
        require(all(v==2 for v in self.uses.values()),f'edge incidence: {list(self.uses.values()).count(1)} free edges')
        sewing=BRepBuilderAPI_Sewing(TOLERANCE)
        for face in self.faces:sewing.Add(face)
        sewing.Perform()
        require(sewing.NbFreeEdges()==0,f'sewing free edges {sewing.NbFreeEdges()}')
        require(sewing.NbMultipleEdges()==0,'non-manifold sewn edges')
        shell=TopoDS.Shell_s(sewing.SewedShape())
        solid=Solid(BRepBuilderAPI_MakeSolid(shell).Solid())
        if solid.volume<0:solid=Solid(TopoDS.Solid_s(solid.wrapped.Reversed()))
        require(solid.is_valid,'closed patch BREP invalid')
        require(solid.volume>0,'closed patch volume not positive')
        return solid


def patch_polynomials(p,R,k,m,low,high,zone,affine):
    """Algebraic exact rational numerator/denominator, no sample fitting."""
    d=derive(p);delta=2*pi/(m*d.lattice_count);a=delta/2
    center=p.skin_phase_theta+(k+.5)*delta
    # Cache-equivalent endpoint trig: modulo K enforces exact revolution seam.
    K=m*d.lattice_count
    t0=p.skin_phase_theta+(k%K)*delta;t1=p.skin_phase_theta+((k+1)%K)*delta
    W=bernstein_to_power([1,cos(a),1])[:,None]
    X=bernstein_to_power([cos(t0),cos(center),cos(t1)])[:,None]
    Y=bernstein_to_power([sin(t0),sin(center),sin(t1)])[:,None]
    z0=p.skin_phase_z+p.skin_axial_pitch*low
    dz=p.skin_axial_pitch*(high-low)
    Z=np.array([[z0,dz]])
    if zone=='core':E=np.array([[1.]])
    elif zone=='smooth':E=np.array([[0.]])
    else:
        b=[0,0,pi*pi/84,pi*pi/28,1-pi*pi/28,1-pi*pi/84,1,1]
        if zone=='upper':b=b[::-1]
        E=bernstein_to_power(b)[None,:]
    c,fu,fv=affine
    F=np.array([[c+fu*k/m+fv*low,fv*(high-low)],[fu/m,0.]])
    rad=add(np.array([[R]]),p.skin_height*mul(E,F))
    return (mul(rad,X),mul(rad,Y),mul(Z,W),W)


def vertex_key(layer,u,v,N):
    # Keys only unify analytically identical clipping intersections; cached points
    # remain unrounded and are checked to 1e-8 mm before an edge is shared.
    return (layer,round(u%N,11),round(v,11))


def skin_patches(p,role,umin=None,umax=None,zmin=None,zmax=None):
    d=derive(p);bounds=route_bounds(p);m=bounds['m'];N=d.lattice_count
    R=getattr(d,role+'_radius');blo,bhi=getattr(d,role+'_band')
    lo=(blo-p.skin_phase_z)/p.skin_axial_pitch;hi=(bhi-p.skin_phase_z)/p.skin_axial_pitch
    f=p.fade_length/p.skin_axial_pitch
    umin=0 if umin is None else umin;umax=N if umax is None else umax
    vmin=lo if zmin is None else (zmin-p.skin_phase_z)/p.skin_axial_pitch
    vmax=hi if zmax is None else (zmax-p.skin_phase_z)/p.skin_axial_pitch
    b=.5-p.plateau_half_fraction
    zones=[(lo,lo+f,'lower'),(lo+f,hi-f,'core'),(hi-f,hi,'upper')]
    for i in range(floor(umin+lo)-2,ceil(umax+hi)+3):
        for j in range(floor(umin-hi)-2,ceil(umax-lo)+3):
            affine=[(1,0,0),((.5-j)/b,1/b,-1/b),((.5+i)/b,-1/b,-1/b),
                    ((.5+j)/b,-1/b,1/b),((.5-i)/b,1/b,1/b)]
            for fidx,poly in enumerate(facet_polygons(p,i,j)):
                for low,high,zone in zones:
                    q=clip(clip(list(poly),1,max(low,vmin),1),1,min(high,vmax),-1)
                    if area(q)<1e-12:continue
                    first=max(floor(umin*m),floor(min(v[0] for v in q)*m))
                    last=min(ceil(umax*m),ceil(max(v[0] for v in q)*m))
                    for k in range(first,last):
                        r=clip(clip(q,0,max(k/m,umin),1),0,min((k+1)/m,umax),-1)
                        if area(r)<1e-12:continue
                        uv=[(m*u-k,(v-low)/(high-low)) for u,v in r]
                        keys=[vertex_key('outer',u,v,N) for u,v in r]
                        yield Patch(patch_polynomials(p,R,k,m,low,high,zone,affine[fidx]),uv,keys,
                                    'plateau' if fidx==0 and zone=='core' else zone)
    # Smooth band-edge extension for the bounded coupon, one strip per sector.
    if vmin<lo:
        for k in range(floor(umin*m),ceil(umax*m)):
            r=[(k/m,vmin),((k+1)/m,vmin),((k+1)/m,lo),(k/m,lo)]
            yield Patch(patch_polynomials(p,R,k,m,vmin,lo,'smooth',(0,0,0)),
                        [(0,0),(1,0),(1,1),(0,1)],[vertex_key('outer',u,v,N) for u,v in r],'smooth')


def inner_patch(patch,R):
    """Same exact rational circle and UV trimming at a constant inner radius."""
    # X/Y = radius polynomial * circle; derive the circle from endpoint sector
    # coefficients by taking z at a fixed parameter, then normalizing its poles.
    # Instead recover homogeneous unit circle from the degree-2 denominator and
    # endpoint/midpoint angle values; algebra is exact for the rational mapping.
    surf=patch.surface
    xyz=[]
    for t in (0.,.5,1.):
        point=surf.Value(t,0.);r=(point.X()**2+point.Y()**2)**.5
        xyz.append((point.X()/r,point.Y()/r))
    w=patch.polynomials[3]
    wm=float(np.polynomial.polynomial.polyval(.5,w[:,0]))
    X=np.array([xyz[0][0],4*xyz[1][0]*wm-3*xyz[0][0]-xyz[2][0],
                2*(xyz[0][0]+xyz[2][0]-2*xyz[1][0]*wm)])[:,None]*R
    Y=np.array([xyz[0][1],4*xyz[1][1]*wm-3*xyz[0][1]-xyz[2][1],
                2*(xyz[0][1]+xyz[2][1]-2*xyz[1][1]*wm)])[:,None]*R
    return Patch((X,Y,patch.polynomials[2],w),patch.polygon,
                 [('inner',*k[1:]) for k in patch.keys],'inner')


def ruled_closure(outer,inner,a,b,ka,kb):
    polys=[]
    for co,ci in zip(outer.polynomials,inner.polynomials):
        o=compose_line(co,a,b);i=compose_line(ci,a,b)
        n=max(len(o),len(i));o=np.pad(o,(0,n-len(o)));i=np.pad(i,(0,n-len(i)))
        polys.append(np.column_stack((o,i-o)))
    return Patch(tuple(polys),[(0,0),(0,1),(1,1),(1,0)],
                 [ka,('inner',*ka[1:]),('inner',*kb[1:]),kb],'closure')


def build_patch(p,role='cap'):
    start=monotonic();d=derive(p);lo=getattr(d,role+'_band')[0]
    outer=list(skin_patches(p,role,-1,1,lo-.3,lo+p.skin_axial_pitch))
    builder=Builder();pairs=[]
    for patch in outer:
        builder.add(patch)
        inside=inner_patch(patch,getattr(d,role+'_radius')-1)
        builder.add(inside,reverse=True);pairs.append((patch,inside))
    for patch,inside in pairs:
        for n,a in enumerate(patch.polygon):
            m=(n+1)%len(patch.polygon);ka,kb=patch.keys[n],patch.keys[m]
            key=tuple(sorted((ka,kb)))
            if builder.uses[key]==1:
                builder.add(ruled_closure(patch,inside,a,patch.polygon[m],ka,kb))
    require(len(builder.faces)<=100,f'patch face ceiling: {len(builder.faces)}')
    solid=builder.solid()
    require(monotonic()-start<60,'patch exceeded 60 seconds')
    errors=[];normals=[]
    for patch in outer:
        u=sum(a[0] for a in patch.polygon)/len(patch.polygon)
        v=sum(a[1] for a in patch.polygon)/len(patch.polygon)
        for a,b in [(u,v),*patch.polygon]:
            point=patch.surface.Value(a,b)
            from math import atan2,hypot
            r=hypot(point.X(),point.Y())
            errors.append(abs(r-radius(p,role,atan2(point.Y(),point.X()),point.Z(),d)))
        face=Face(patch.face);normal=face.normal_at(u,v)
        point=patch.surface.Value(u,v)
        dot=normal.X*point.X()+normal.Y*point.Y()
        require(dot>0,'inward skin face normal')
        normals.append(abs(normal.Z)/(normal.X**2+normal.Y**2)**.5)
    require(max(errors)<=.01,f'actual skin deviation {max(errors)}')
    require(max(normals)<=1,'actual patch overhang >45 degrees')
    report=dict(faces=len(builder.faces),volume=solid.volume,valid=solid.is_valid,
                seconds=monotonic()-start,maximum_radial_error=max(errors),
                maximum_join_error=builder.max_join_error,maximum_normal_slope=max(normals),
                plateau_faces=sum(x.kind=='plateau' for x in outer),route_bounds=route_bounds(p))
    return solid,builder,report
