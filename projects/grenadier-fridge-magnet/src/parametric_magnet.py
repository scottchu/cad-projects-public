"""Exact pixel-grid mesh study. No smoothing, STEP, slicer or physical claims."""
from __future__ import annotations
import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import shapely
from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize
import trimesh
from scipy import ndimage
from face_vector import classify, contours, svg_path, CLASSES, PALETTE

PROJECT = Path(__file__).resolve().parents[1]
LAMPS = [(137,720,60,65),(288,732,59,60),(602,736,60,62),(802,727,65,69)]
REGIONS = {
 'windshield': [(299,464),(334,292),(365,267),(904,250),(927,279),(931,453),(904,476)],
 'side-front': [(971,285),(1029,307),(1050,497),(978,508)],
 'side-middle': [(1044,313),(1100,326),(1120,490),(1065,500)],
 'side-rear': [(1115,322),(1160,337),(1176,491),(1139,500)],
 'grille': [(236,628),(677,626),(681,818),(236,810)],
 'bumper': [(36,804),(225,811),(263,831),(619,829),(673,809),(938,814),(944,938),(878,961),(690,971),(626,951),(279,951),(234,965),(79,919),(36,889)],
 'plate': [(329,838),(583,838),(584,949),(326,949)],
}
FEATURES = {
 'plate': {'bounds':[326,838,584,949], 'anchor':[455,893.5], 'xy_scale':1.0,'stroke_offset_source_units':0},
 'grenadier_wordmark': {'bounds':[716,537,902,613], 'anchor':[809,575], 'xy_scale':1.0,'stroke_offset_source_units':0},
 'lamps': {'bounds':[[x-rx,y-ry,x+rx,y+ry] for x,y,rx,ry in LAMPS], 'anchor':[457,730], 'xy_scale':1.0,'stroke_offset_source_units':0},
}
@dataclass(frozen=True)
class Parameters:
    working_mm_per_source_unit: float = 0.1
    xy_scale: float = 1.0
    back_thickness_mm: float = 1.2
    flat_face_depth_mm: float = 0.8
    low_depth_mm: float = 0.4
    middle_depth_mm: float = 0.8
    high_depth_mm: float = 1.2
    def validate(self):
        if not all(np.isfinite(v) and v > 0 for v in asdict(self).values()):
            raise ValueError('All dimensions and scale must be finite and positive')
        if not self.low_depth_mm < self.middle_depth_mm < self.high_depth_mm:
            raise ValueError('Relief depths require low < middle < high')

def transform_xy(uv, p: Parameters):
    p.validate()
    return (np.asarray(uv,dtype=float)-627)*np.array([1,-1])*p.working_mm_per_source_unit*p.xy_scale

def inverse_xy(xy, p: Parameters):
    p.validate()
    return np.asarray(xy)/(p.working_mm_per_source_unit*p.xy_scale)*np.array([1,-1])+627

def validate_features(features):
    if features != FEATURES:
        raise ValueError('Nonidentity feature edits are deferred: scale/stroke/art bounds require a new reviewed delta')

def semantic_masks(foreground, regions=REGIONS, lamps=LAMPS):
    yy,xx = np.indices(foreground.shape,dtype=float); xx+=0.5; yy+=0.5
    inside = {name: shapely.intersects_xy(Polygon(points),xx,yy) for name,points in regions.items()}
    low=np.logical_or.reduce([inside[k] for k in ('windshield','side-front','side-middle','side-rear','grille')])
    high=inside['bumper']|inside['plate']
    for x,y,rx,ry in lamps:
        high |= ((xx-x)/rx)**2+((yy-y)/ry)**2<=1
    return {'low':foreground & low & ~high, 'middle':foreground & ~(low|high), 'high':foreground & high}

def mask_polygons(mask):
    loops=contours(mask)
    faces=list(polygonize([LineString(loop) for loop in loops]))
    selected=[]
    for polygon in faces:
        point=polygon.representative_point()
        if mask[int(point.y),int(point.x)]:
            if not polygon.is_valid: raise ValueError('Invalid exact polygon')
            selected.append(polygon)
    if sum(poly.area for poly in selected) != int(mask.sum()):
        raise ValueError('Polygon mask area mismatch')
    return selected

def extrude_indexed(vertices, faces, depth):
    """Split disconnected triangle fans at exact grid pinches; never weld positions.

    Coincident vertical contact edges remain distinct shell topology, preserving
    exact artwork. STL position welding can destroy this topology; use GLB.
    """
    vertices=vertices.tolist(); faces=faces.copy()
    edges=np.sort(faces[:,[0,1,1,2,2,0]].reshape(-1,2),axis=1)
    unique,counts=np.unique(edges,axis=0,return_counts=True)
    boundary=unique[counts==1]
    ids,degrees=np.unique(boundary,return_counts=True)
    for vertex in ids[degrees>2]:
        incident=np.flatnonzero(np.any(faces==vertex,axis=1)).tolist()
        fans=[]
        while incident:
            fan=[incident.pop()]; neighbors=set(faces[fan[0]])-{vertex}
            changed=True
            while changed:
                changed=False
                for tri in incident[:]:
                    if neighbors.intersection(set(faces[tri])-{vertex}):
                        fan.append(tri);incident.remove(tri);neighbors.update(set(faces[tri])-{vertex});changed=True
            fans.append(fan)
        for fan in fans[1:]:
            new=len(vertices);vertices.append(vertices[vertex])
            for tri in fan: faces[tri,faces[tri]==vertex]=new
    vertices=np.asarray(vertices)
    a,b,c=vertices[faces].transpose(1,0,2)
    cross=(b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0])
    faces[cross<0]=faces[cross<0,::-1]
    edges=faces[:,[0,1,1,2,2,0]].reshape(-1,2)
    _,idx,counts=np.unique(np.sort(edges,axis=1),axis=0,return_index=True,return_counts=True)
    boundary=edges[idx[counts==1]]; n=len(vertices)
    side=np.array([[a,b,b+n,a,b+n,a+n] for a,b in boundary]).reshape(-1,3)
    xyz=np.column_stack([vertices,np.zeros(n)])
    return trimesh.Trimesh(vertices=np.vstack([xyz,xyz+[0,0,depth]]),faces=np.vstack([faces[:,::-1],faces+n,side]),process=False)

def extrude_mask(mask, z0, depth, p):
    meshes=[]
    for polygon in mask_polygons(mask):
        triangles=shapely.constrained_delaunay_triangles(polygon)
        raw=np.array([np.asarray(t.exterior.coords)[:3] for t in triangles.geoms])
        if abs(sum(t.area for t in triangles.geoms)-polygon.area)>1e-8:
            raise ValueError('Triangulation area mismatch')
        vertices,index=np.unique(raw.reshape(-1,2),axis=0,return_inverse=True)
        mesh=extrude_indexed(transform_xy(vertices,p),index.reshape(-1,3),depth)
        mesh.apply_translation([0,0,z0])
        if not mesh.is_watertight or not mesh.is_winding_consistent or mesh.volume<=0:
            raise ValueError(f'Nonclosed or inverted extrusion: bounds={polygon.bounds}, area={polygon.area}, holes={len(polygon.interiors)}, watertight={mesh.is_watertight}, winding={mesh.is_winding_consistent}, volume={mesh.volume}')
        meshes.append(mesh)
    combined=trimesh.util.concatenate(meshes)
    expected=int(mask.sum())*(p.working_mm_per_source_unit*p.xy_scale)**2*depth
    if not np.isclose(combined.volume,expected,rtol=1e-9,atol=1e-8):
        raise ValueError('Extrusion volume mismatch')
    return combined,len(meshes)

def accepted_masks():
    masks,bg=classify(PROJECT/'references/d4-approved.png')
    svg=ET.parse(PROJECT/'SVG/p1-r1/face.svg').getroot()
    for group in svg.findall('{http://www.w3.org/2000/svg}g'):
        name=group.attrib['id']
        actual=svg_path(contours(masks[name]))
        if actual != group[0].attrib['d']: raise ValueError('Accepted SVG path mismatch: '+name)
    if not np.all(sum(m.astype(int) for m in masks.values()) == (~bg).astype(int)):
        raise ValueError('Color overlap or gap')
    return masks,~bg

def backing_connectivity(foreground):
    """Shortest <=2-background-cell paths; global (length, XY path) tie-break.

    Recompute connected components after every chosen link so connectors are
    reused. Four-neighbour adjacency gives positive-area extrusion contacts.
    """
    original=foreground.copy(); repaired=original.copy()
    labels,count=ndimage.label(original)
    sizes=np.bincount(labels.ravel()); sizes[0]=0
    main=int(sizes.argmax()); anchor=tuple(np.argwhere(labels==main)[0])
    yy,xx=np.nonzero(original); bounds=(int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max()))
    allowed=ndimage.binary_dilation(original,structure=np.ones((5,5),bool))
    additions=[];links=[]
    def neighbors(x,y):
        return ((x-1,y),(x,y-1),(x,y+1),(x+1,y))
    def valid(x,y):
        return bounds[0]<=x<=bounds[2] and bounds[1]<=y<=bounds[3] and allowed[y,x]
    while count>1:
        connected=labels==labels[anchor]
        detached=repaired & ~connected
        candidates=[]
        for y,x in np.argwhere(detached):
            for bx,by in neighbors(int(x),int(y)):
                if not valid(bx,by) or repaired[by,bx]: continue
                path=((bx,by),)
                if any(valid(nx,ny) and connected[ny,nx] for nx,ny in neighbors(bx,by)):
                    candidates.append(path);continue
                for cx,cy in neighbors(bx,by):
                    if not valid(cx,cy) or repaired[cy,cx] or (cx,cy)==(bx,by):continue
                    if any(valid(nx,ny) and connected[ny,nx] for nx,ny in neighbors(cx,cy)):
                        candidates.append(path+((cx,cy),))
        if not candidates:raise ValueError('No permitted <=2-cell backing link remains')
        path=min(candidates,key=lambda path:(len(path),path))
        for x,y in path: repaired[y,x]=True
        additions.extend(path);links.append(path)
        labels,count=ndimage.label(repaired)
        if len(additions)>356:raise ValueError('Backing addition ceiling exceeded')
    if not np.all(repaired[original]):raise ValueError('Backing deleted original pixels')
    return repaired,{'original_components':int(ndimage.label(original)[1]),'connected_components':count,'added_count':len(additions),'added_cells_xy':additions,'links_xy':links,'original_bounds_inclusive_xy':bounds,'max_cells_per_link':max(map(len,links),default=0)}

def srgb_to_linear(rgb):
    rgb=np.asarray(rgb,dtype=float)
    return np.where(rgb<=0.04045,rgb/12.92,((rgb+0.055)/1.055)**2.4)

def linear_to_srgb(rgb):
    rgb=np.asarray(rgb,dtype=float)
    return np.where(rgb<=0.0031308,12.92*rgb,1.055*rgb**(1/2.4)-0.055)

def encode_glb_materials(tree):
    """glTF PBR factors are linear; source palette is sRGB, convert once.

    Constant per-part material avoids quantizing dark linear RGB to UINT8.
    COLOR_0 is removed to prevent a second color multiplier; unused buffer
    entries are legal glTF and geometry buffers stay unchanged.
    """
    materials=[]
    for mesh in tree['meshes']:
        name=mesh['name']
        color='black' if name=='backing-black' else next(c for c in CLASSES if name.startswith(c+'-'))
        rgba=[int(PALETTE[color][i:i+2],16)/255 for i in (1,3,5)]
        factor=srgb_to_linear(rgba).tolist()+[1.0]
        index=len(materials)
        materials.append({'name':color+'-linear','pbrMetallicRoughness':{'baseColorFactor':factor,'metallicFactor':1.0,'roughnessFactor':1.0},'alphaMode':'OPAQUE','doubleSided':False})
        for primitive in mesh['primitives']:
            primitive['attributes'].pop('COLOR_0',None)
            primitive['material']=index
    tree['materials']=materials

def build(p=Parameters(), output_tag='p1-r2-color-corrected', preflight=False, features=FEATURES, backing_mode='connected', export_stl=True):
    p.validate();validate_features(features)
    masks,fg=accepted_masks()
    if preflight:
        mesh,components=extrude_mask(masks['deep-blue'],p.back_thickness_mm,p.flat_face_depth_mm,p)
        result={'preflight':'deep-blue','components':components,'faces':len(mesh.faces),'watertight':mesh.is_watertight,'volume_mm3':float(mesh.volume)}
        print(json.dumps(result),flush=True);return result
    levels=semantic_masks(fg)
    assert np.all(sum(m.astype(int) for m in levels.values())==fg.astype(int))
    report={'parameters':asdict(p),'features':features,'regions':REGIONS,'lamps':LAMPS,'representation':'closed multipart mesh; exact grid; no STEP','material_intents':{'black':'black','gray':'gray','white':'white','deep-blue':'deep-blue','glass-mix':'blue+white unresolved process placeholder; NOT fifth spool'},'variants':{}}
    back_mask,delta=backing_connectivity(fg) if backing_mode=='connected' else (fg,{'mode':'historical-exact'})
    report['backing_delta']=delta
    print('backing delta',json.dumps(delta),flush=True)
    backing,back_count=extrude_mask(back_mask,0,p.back_thickness_mm,p)
    if backing_mode=='connected' and (back_count!=1 or len(backing.split(only_watertight=False))!=1):raise ValueError('Backing is not one connected indexed shell')
    for variant in ('flat','relief'):
        scene=trimesh.Scene(); parts={'backing-black':(backing.copy(),back_count,int(back_mask.sum()),p.back_thickness_mm,'black',0)}
        for color in CLASSES:
            for level,region in ({'flat':fg} if variant=='flat' else levels).items():
                mask=masks[color]&region
                if not mask.any(): continue
                depth=p.flat_face_depth_mm if level=='flat' else getattr(p,level+'_depth_mm')
                mesh,count=extrude_mask(mask,p.back_thickness_mm,depth,p)
                parts[color+'-'+level]=(mesh,count,int(mask.sum()),depth,color,p.back_thickness_mm)
        stats={}
        stldir=PROJECT/'STL'/output_tag/variant
        if export_stl:stldir.mkdir(parents=True,exist_ok=True)
        for name,(mesh,count,pixels,depth,color,z0) in parts.items():
            rgb=[int(PALETTE[color][i:i+2],16) for i in (1,3,5)]+[255]
            mesh.visual=trimesh.visual.ColorVisuals(mesh,face_colors=rgb)
            mesh.metadata.update({'name':name,'units':'mm','material_intent':report['material_intents'][color]})
            scene.add_geometry(mesh,node_name=name,geom_name=name)
            if export_stl:mesh.export(stldir/(name+'.stl'))
            stats[name]={'components':count,'faces':len(mesh.faces),'pixel_area':pixels,'bounds':mesh.bounds.tolist(),'volume_mm3':float(mesh.volume),'expected_volume_mm3':pixels*(p.xy_scale*p.working_mm_per_source_unit)**2*depth,'z0':z0,'depth':depth,'watertight_indexed':bool(mesh.is_watertight),'winding_consistent':bool(mesh.is_winding_consistent)}
        glb=PROJECT/'GLB'/output_tag/(variant+'.glb');glb.parent.mkdir(parents=True,exist_ok=True)
        glb.write_bytes(trimesh.exchange.gltf.export_glb(scene,tree_postprocessor=encode_glb_materials))
        written=trimesh.load_scene(glb,process=False)
        for name,mesh in written.geometry.items():
            if not mesh.is_watertight or not mesh.is_winding_consistent: raise ValueError('GLB topology mismatch '+name)
            if not np.allclose(mesh.bounds,stats[name]['bounds'],atol=5e-6): raise ValueError('GLB placement mismatch')
            if not np.isclose(mesh.volume,stats[name]['volume_mm3'],rtol=3e-5):raise ValueError('GLB volume mismatch')
        report['variants'][variant]={'parts':stats,'bounds':scene.bounds.tolist(),'glb':str(glb.relative_to(PROJECT))}
        print(variant,'complete',len(parts),'parts',sum(v['faces'] for v in stats.values()),'faces',flush=True)
    dest=PROJECT/'GLB'/output_tag/'mesh-report.json'
    dest.write_text(json.dumps(report,indent=2)+'\n')
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,help='JSON with parameters and optional identity-only features')
    parser.add_argument('--output-tag',default='p1-r2-color-corrected')
    parser.add_argument('--glb-only',action='store_true',help='Skip unchanged STL exports for color-only revisions')
    parser.add_argument('--backing-mode',choices=('connected','historical-exact'),default='connected')
    parser.add_argument('--preflight',action='store_true')
    for name,value in asdict(Parameters()).items(): parser.add_argument('--'+name.replace('_','-'),type=float,default=None)
    args=parser.parse_args(); config=json.loads(args.config.read_text()) if args.config else {}
    params=config.get('parameters',{})|{k:getattr(args,k) for k in asdict(Parameters()) if getattr(args,k) is not None}
    build(Parameters(**params),args.output_tag,args.preflight,config.get('features',FEATURES),args.backing_mode,not args.glb_only)
if __name__=='__main__': main()
