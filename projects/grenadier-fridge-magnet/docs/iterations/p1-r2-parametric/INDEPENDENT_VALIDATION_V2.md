# P2-V2 independent validation — development mesh gates pass

Owner `/root/parametric_mesh_validation`, 2026-09-06. Independent of implementation. Historical failure remains in INDEPENDENT_VALIDATION.md; this report applies only to the connected replacement.

Verified all37 manifest entries before and after testing, with fingerprint `2541d21cfbb28d29eede289a3ae978c9d516a91b1e5f07e045f8d6c8286993ce`. Flat GLB SHA-256 `3d7f7e8f9e2bcc4ffbb2355abd9f1aba848cb3a18cff64059d2cd6011309008b`; relief `86d99b9b6ca36f31969e71db48a61dbb1c4f84024e32a46a1a2a521202eb2a75`.

## Results and requirement coverage

- GM-R2-01 / backing repair: each written GLB has one connected watertight backing shell and one four-neighbour connected footprint. Actual backing area1,011,658 source units²; exactly176 cells added, zero removed, same bounds[1,126,1251,1144], all additions within the permitted distance2. Independently replayed175 reported links: each reduces component count; maximum2 added cells per link; final count1.
- GM-R2-01/07: every nonbacking vertex and face array is exactly equal to its historical candidate. Reconstructed actual top-cap boundaries for each of the five colors exactly match accepted SVG path boundaries after float32 coordinates recover to the native grid (maximum recovery residual below0.00003 source unit). Projected areas also match accepted masks. Accepted-art hashes remain unchanged.
- GM-R2-02/03: flat face Z=2.0; relief low/middle/high Z=1.6/2.0/2.4 within float32 tolerance; all face bottoms Z=1.2 touch backing. Every foreground pixel center inside the plate semantic polygon occurs at high level. Main lamp/body/glass region recognition remains the critic's visual gate.
- Actual GLB mesh geometry: all6 flat and14 relief parts are indexed-watertight, consistently wound, positive-volume extrusions with identity graph transforms, matching top/bottom footprints and vertical side triangles. Measured volume equals projected area×height within relative2e-6; maximum absolute deviation0.00007903 mm³. Pairwise footprint intersections combined with actual Z intervals find no positive-volume overlap. Every face footprint is covered by backing.
- GM-R2-04/05: correct part names, actual vertex colors and material-intent metadata; glass-mix explicitly blue+white placeholder, not fifth spool. No retention holes or motion introduced; scale remains development choice.
- GM-R2-06:6 existing focused tests pass. Independent scratch extrusion with3×XY has9×volume and identical Z; changed depth preserves XY. Nonidentity plate scale and stroke edits raise ValueError.

Commands: `uv run pytest -q projects/grenadier-fridge-magnet/tests/test_parametric_magnet.py` (6 passed); `uv run python /tmp/grenadier-v2-independent.py` (all assertions passed). All tooling used root uv; scratch only outside the repository. Full independent script and results follow for reproducibility. The link replay used reported `backing_delta.links_xy`, added each previously empty cell to the original mask, and checked `scipy.ndimage.label` decreases after each link to1.

## Acceptance limits

PASS for these deterministic development-mesh gates, subject to separate critic and formal review. Added backing176 cells (1.76 mm² at working scale) changes the combined silhouette locally; it is explicitly permitted by BACKING_REPAIR.md and must remain disclosed. Thin connectors and coincident/pinched color contacts are not proven manufacturable. STL welding, STEP/BREP, slicing, glass-mix process, magnet retention/strength, physical detail survival and physical assembly remain unaccepted. This validator makes no user-surface visual claim. No source or candidate artifact was mutated.

Next: formal reviewer joins this receipt with independent front/oblique critique for the same fingerprint, then presents the development study.

## Independent written-artifact script

```python
import json,hashlib,re,sys,copy,itertools
from pathlib import Path
import numpy as np,trimesh,shapely
from shapely.geometry import LineString,Polygon
from scipy import ndimage
import xml.etree.ElementTree as ET
P=Path('projects/grenadier-fridge-magnet');sys.path.insert(0,str(P/'src'))
from parametric_magnet import accepted_masks,Parameters,extrude_mask,FEATURES,validate_features,REGIONS
masks,fg=accepted_masks(); yy,xx=np.indices(fg.shape); pixpoints=(xx+.5,yy+.5)
svg={}
for g in ET.parse(P/'SVG/p1-r1/face.svg').getroot().findall('{http://www.w3.org/2000/svg}g'):
 loops=[]
 for piece in g[0].attrib['d'].split('Z'):
  nums=re.findall(r'-?\d+(?:\.\d+)?',piece)
  if nums:
   xy=np.array(nums,dtype=float).reshape(-1,2);loops.append(LineString(np.vstack([xy,xy[0]])))
 svg[g.attrib['id']]=shapely.union_all(loops)
report={}; allfoot={}
for variant in ('flat','relief'):
 scene=trimesh.load_scene(P/'GLB/p1-r2-connected'/f'{variant}.glb',process=False)
 old=trimesh.load_scene(P/'GLB/p1-r2'/f'{variant}.glb',process=False)
 footprints={}; intervals={}; colors={}; volerr=[]
 assert len(scene.geometry)==(6 if variant=='flat' else 14)
 for name,mesh in scene.geometry.items():
  assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
  assert np.allclose(scene.graph[name][0],np.eye(4))
  zlo,zhi=mesh.bounds[:,2];t=mesh.triangles
  top=np.all(t[:,:,2]==zhi,axis=1);bottom=np.all(t[:,:,2]==zlo,axis=1)
  assert np.all(np.isin(t[:,:,2],[zlo,zhi]))
  uv=t[:,:,:2]*[10,-10]+627; assert np.max(abs(uv-np.rint(uv)))<3e-5
  uv=np.rint(uv)
  footprint=shapely.union_all(shapely.polygons(uv[top]));lower=shapely.union_all(shapely.polygons(uv[bottom]))
  assert footprint.equals(lower)
  sides=uv[~(top|bottom)]
  assert all(len(np.unique(tri,axis=0))==2 for tri in sides)
  expected=footprint.area*.01*(zhi-zlo);assert np.isclose(mesh.volume,expected,rtol=2e-6)
  volerr.append(abs(mesh.volume-expected));footprints[name]=footprint;intervals[name]=(zlo,zhi)
  if name!='backing-black':
   assert np.array_equal(mesh.vertices,old.geometry[name].vertices)
   assert np.array_equal(mesh.faces,old.geometry[name].faces)
   color=name.rsplit('-',1)[0];colors.setdefault(color,[]).append(footprint)
  else:assert len(mesh.split(only_watertight=False))==1 and footprint.geom_type=='Polygon'
  color='black' if name=='backing-black' else name.rsplit('-',1)[0]
  from face_vector import PALETTE
  rgb=np.array([int(PALETTE[color][i:i+2],16) for i in (1,3,5)]+[255])
  assert np.all(mesh.visual.vertex_colors==rgb),(name,'color')
  assert mesh.metadata['material_intent']==('blue+white unresolved process placeholder; NOT fifth spool' if color=='glass-mix' else color)
 for color,polys in colors.items():
  union=shapely.union_all(polys);assert union.boundary.symmetric_difference(svg[color]).length==0,(variant,color,'SVG boundary')
  assert union.area==int(masks[color].sum())
 for a,b in itertools.combinations(footprints,2):
  overlap=min(intervals[a][1],intervals[b][1])-max(intervals[a][0],intervals[b][0])
  if overlap>1e-6:assert footprints[a].intersection(footprints[b]).area==0,(a,b,'collision')
 back=footprints['backing-black']; backmask=shapely.contains_xy(back,*pixpoints)
 assert np.all(backmask[fg]);assert ndimage.label(backmask)[1]==1
 addition=backmask&~fg;assert addition.sum()==176
 assert np.all(ndimage.binary_dilation(fg,structure=np.ones((5,5)))[addition])
 assert back.bounds==(1.,126.,1251.,1144.)
 for n in footprints:
  if n!='backing-black':
   assert back.covers(footprints[n]); assert np.isclose(intervals[n][0],1.2)
   level=n.rsplit('-',1)[1];assert np.isclose(intervals[n][1],{'flat':2,'low':1.6,'middle':2,'high':2.4}[level])
 if variant=='relief':
  plate=shapely.intersects_xy(Polygon(REGIONS['plate']),*pixpoints)&fg
  for n in footprints:
   if n!='backing-black' and not n.endswith('-high'):
    assert not np.any(shapely.contains_xy(footprints[n],xx[plate]+.5,yy[plate]+.5))
 report[variant]={'parts':len(scene.geometry),'backing_components':1,'backing_area_source':back.area,'added_cells':int(addition.sum()),'max_volume_error_mm3':max(volerr),'bounds':scene.bounds.tolist(),'svg_boundary_parity':'exact after checked float32 grid recovery','positive_volume_collisions':0,'all_colors_and_material_intents':'match'}
 allfoot[variant]=footprints
# Independent source parameter perturbation reaches actual generated scratch meshes, no candidate exports.
small=np.ones((3,4),bool);a,_=extrude_mask(small,1.2,.8,Parameters());b,_=extrude_mask(small,1.2,.8,Parameters(xy_scale=3));c,_=extrude_mask(small,1.2,1.1,Parameters())
assert np.allclose(a.vertices[:,:2]*3,b.vertices[:,:2]);assert np.array_equal(a.vertices[:,2],b.vertices[:,2]);assert np.array_equal(a.vertices[:,:2],c.vertices[:,:2]);assert np.isclose(b.volume/a.volume,9)
for field,value in [('xy_scale',1.01),('stroke_offset_source_units',1)]:
 f=copy.deepcopy(FEATURES);f['plate'][field]=value
 try:validate_features(f)
 except ValueError:pass
 else:raise AssertionError('Unsupported feature accepted')
print(json.dumps(report,indent=2));Path('/tmp/grenadier-v2-independent-results.json').write_text(json.dumps(report,indent=2))
```

## Actual results

```json
{
  "flat": {
    "parts": 6,
    "backing_components": 1,
    "backing_area_source": 1011658.0,
    "added_cells": 176,
    "max_volume_error_mm3": 4.370518990981509e-05,
    "bounds": [
      [
        -62.599998474121094,
        -51.70000076293945,
        0.0
      ],
      [
        62.400001525878906,
        50.099998474121094,
        2.0
      ]
    ],
    "svg_boundary_parity": "exact after checked float32 grid recovery",
    "positive_volume_collisions": 0,
    "all_colors_and_material_intents": "match"
  },
  "relief": {
    "parts": 14,
    "backing_components": 1,
    "backing_area_source": 1011658.0,
    "added_cells": 176,
    "max_volume_error_mm3": 7.902877155174792e-05,
    "bounds": [
      [
        -62.599998474121094,
        -51.70000076293945,
        0.0
      ],
      [
        62.400001525878906,
        50.099998474121094,
        2.4000000953674316
      ]
    ],
    "svg_boundary_parity": "exact after checked float32 grid recovery",
    "positive_volume_collisions": 0,
    "all_colors_and_material_intents": "match"
  }
}
```
