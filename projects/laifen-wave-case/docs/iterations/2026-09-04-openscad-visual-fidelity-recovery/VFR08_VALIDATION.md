# VFR-08 independent validation

Status: **SCOPED GEOMETRY PASS; FORMAL JOIN BLOCKED BY FINAL INPUT DRIFT AND INVENTORY CORRECTION.** This receipt does not accept browser performance, CAD/STEP, slicer/process or physical printing.

Owner: `/root/openscad_vfr07_validator`, continuing the independent validation workstream on changed VFR-08 C1. Worktree: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`; project: `projects/laifen-wave-case`; iteration: `2026-09-04-openscad-visual-fidelity-recovery`. Sole changed path: this document. Candidate source/tests/artifacts, browser, services and continuity remain read-only.

## Provenance and scope

Validation manifest `inputs/VFR08_VALIDATION_INPUTS.sha256` verified at **`d65eb827738d942f49498e4eb03c1c0044053d4eaa027b50547adcf4614d03b7`**, all **9/9** entries OK. Candidate manifest `candidate/VFR08_C1_CANDIDATE.sha256` verified at **`6ec55511f9ee5b78b08d3e9572ab6cd49b6844f37306bbd5a368bc76c4f51817`**, all **17/17** entries OK.

SCAD: **`ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`**. New test: **`a7297933430d0e2f2135ff8c5a3ecde2fd573cff1ae90ef042d140bb66f96fa6`**. The retained VFR-07 source at `scratch/vfr07-implementation/candidate.scad` was independently verified as `48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`.

The frozen functional design explicitly permits only both drain-cylinder centering arguments, the cap print-layout transform and explanatory comments. An exact source reconstruction proves precisely those three executable fragment changes and the two comments; everything else is byte-preserved, including all four drain callers, parameters, B lattice, profiles, threads, shoulder, standalone/assembly transforms and assertions.

The additional root-relative `scratch/vfr08-implementation/hashes.sha256` inventory was checked. **33/34 entries OK; its own entry fails**, as detailed below. All 15 STL identities and their retained compiler receipts nevertheless verify against that inventory; its actual bytes are bound correctly by the candidate manifest.

## Results

Focused command: **17 passed in 0.10 s**. These source/math tests were supplemented by independent checks of the written meshes; the source-string tests alone are not functional proof.

### Through drains and closed unselected ends

Independently inspected all **15** written meshes: 12 standalone style/mode/role combinations, two layouts, and one corrected depth-zero witness. Exact XYZ indexing was used for inspection only, with no tolerance weld, repair or output rewrite.

Every standalone piece is one positive-volume, watertight, consistently wound component; all edges have incidence two, with no zero-area or duplicate triangles. Selected drained pieces have Euler **-12**, correctly representing seven through apertures. All unselected pieces have Euler **2**. Both layouts have exactly two separated components and total Euler **-10**.

| Written target | Faces | Euler |
|---|---:|---:|
| diamond-bottom-body | 55,772 | -12 |
| diamond-bottom-cap / diamond-none-cap | 40,510 | 2 |
| diamond-none-body / diamond-top-body | 53,056 | 2 |
| diamond-top-cap | 43,226 | -12 |
| smooth-bottom-body / diamond-depth0-bottom-body | 21,302 | -12 |
| smooth-bottom-cap / smooth-none-cap | 18,778 | 2 |
| smooth-none-body / smooth-top-body | 18,586 | 2 |
| smooth-top-cap | 21,494 | -12 |
| diamond-bottom-print_layout | 96,282 | -10 |
| smooth-top-print_layout | 40,080 | -10 |

For each standalone mesh, cast **35 full-axis rays**: all seven intended centers, each with offsets (0,0), (±0.75,0) and (0,±0.75) mm. Every selected-hole ray has **zero triangle intersection**, including beyond both floor faces. Every unselected ray returns its original closed-floor interval. Additional off-hole rays at (3,0) and (12,0) retain material:

- Body floor: **0..3 mm**.
- Cap floor: **81.01..84 mm**, retaining the intended **2.99 mm** thickness.

For each selected piece, sections 0.001 mm inside both floor faces contain one outer contour and **seven distinct closed hole contours**. All centers match (0,0) and the six radius-9 positions within 1e-7 mm; each aperture has 3×3 mm XY extent. Every section point lies on the prescribed radius-1.5, 96-sided polygon within **2.22e-15 mm**. This checks full apertures, not only a central hole or one mouth image.

Measured none-minus-selected volume agrees with the seven polygonal columns:

| Style | Body removed / expected mm3 | Cap removed / expected mm3 |
|---|---|---|
| Diamond | 148.334297093970 / 148.334297093965 | 147.839849436983 / 147.839849436985 |
| Smooth | 148.334297093985 / 148.334297093965 | 147.839849436976 / 147.839849436985 |

Maximum discrepancy is **2.03e-11 mm3**. Expected values use actual 96-gon area `96/2 × 1.5² × sin(2π/96)` times seven and floor thickness 3 or 2.99.

The exact source delta only changes a subtractive cutter within the existing XY footprints. Its shortened negative-Z extent previously occupied exterior air for the body, and pre-floor cavity for the cap; it cannot add material at the defaults. Its new extent removes the former roofs. Source mask proof, retained exterior/profile data, full aperture sections and volume accounting support containment in those floor columns; no new generic mesh-Boolean package was installed.

The VFR-07 **1.5 mm blind-roof defect is resolved** in selected bottom body and selected top cap, for both surface styles.

### Actual production cutter boundary witnesses

Executed the real production caller lines and shared cutter in pinned SCAD, using source-derived globals. Checked exact default and thickness boundaries with a nondefault split:

| Floor / cap height | Body cutter Z interval | Cap cutter Z interval |
|---|---|---|
| 2 / 97 | -0.1..2.1 | 94.9..97.1 |
| 3 / 84 | -0.1..3.1 | 80.9..84.1 |
| 8 / 97 | -0.1..8.1 | 88.9..97.1 |

All six executable witnesses returned zero without assertion/error/warning diagnostics, and STL vertex bounds match the expected intervals within 1e-8 mm. The cutter strictly spans the selected floor for these prescribed fixtures. This is not an exhaustive parameter-domain proof.

### Written print-layout orientation and separation

Both exact written layouts were split into their actual two components. Every component matches its corresponding standalone mesh after the prescribed transform: **maximum bidirectional vertex discrepancy 0 mm**, and all triangles match after canonical ordering at 1e-8 mm.

| Component | Bounds X mm | Bounds Z mm | Off-hole closed floor | Upper-mouth radial intersections |
|---|---|---|---|---|
| Body in both layouts | 3.5..42.5 | 0..144 | 0..3 | 15..16.4 |
| Cap in both layouts | -42.5..-3.5 | 0..84 | 0..2.99 | 17.04..19.488681653 diamond; 17.04..19.5 smooth |

The floor probes use local off-hole x=3; upper-mouth rays are 0.01 mm below the rim. Sections 0.5 mm below each rim contain two contours, showing the open cavity and exterior. These witnesses establish **closed-end-down/open-end-up** rather than merely matching overall bounds. Cap local z=84 is now bed z=0, and local z=0 is print z=84.

The measured X-envelope gap is **7 mm** for each layout. The strictly disjoint X intervals prove zero part-to-part intersection volume without a mesh Boolean. No scaling or mirroring occurs: cap uses the proper 180-degree X rotation and translation, and body pose is unchanged.

This is the required source-defined print orientation. **Support-free slicing, adhesion and real print behavior remain untested.**

### Preservation and source/artifact identity

All **34,716 body** and **22,110 cap** lateral diamond exterior triangles match the VFR-07 artifacts after canonical ordering at 1e-8 mm. The actual repaired body's seam at global z=135 and repaired cap's local z=0 have **99 exactly equal XY vertices**. OD39, heights144/84, unchanged end chamfers, bores and internal profiles are preserved by exact source scope and actual exterior/transform comparisons.

The frozen VFR-07 exterior sampled-error and analytic-bound results remain applicable to these same measured exterior triangles: maximum sample approximately **0.012886375 mm**, body/cap analytic maxima **0.013694029 / 0.017661157 mm**, below 0.025 mm, with exterior counts below250,000. These numerical error values were established earlier in this same validation workstream; VFR-08 rechecked triangle identity rather than redundantly resampling unchanged triangles.

Fresh pinned-source WASM execution independently reproduced the exact hashes of all six candidate-listed meshes:

- diamond-bottom-body: `6789c6b1ade20b205646bcc2e5eb17d22b515e47c6e3fd1fd5688390376f60c8`.
- diamond-bottom-cap: `e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514`.
- diamond-top-body: `ee4257d6bbb25796acab882fc52c9648face2607311f85092c4c16914dc0b317`.
- diamond-top-cap: `c26c7f2c17abcd5bd0328e223554e267153aa2150efcc6ae445bc71e55d46ecc`.
- diamond-bottom-print_layout: `73dc750bd9bea35d1e65e4cd05ec7a56b1cc5cdd42faf8a1649455694d83062e`.
- smooth-top-print_layout: `62857ff511b4a5eb3531a3a48f993b8b12bc2c3ffdc25b1ae3f0ed1da20632e3`.

Separately reran frozen VFR-07 source for all four smooth/diamond `none` body/cap outputs: each is byte-identical to its VFR-08 counterpart. All unselected body/top and cap/bottom outputs equal their same-style none outputs. Corrected depth-zero diamond body is byte-identical to corrected smooth bottom body, hash `db78a5eb2a24a16d47ae0e8837003115ee573812016ef443715997aea07474a2`.

Comparison builds remained entirely inside WASM memory; no generated workspace artifact was created or overwritten.

## Findings, disposition and limits

**H0 — a frozen test input changed during the task.** Initial validation manifests passed before testing. At the final recheck, both manifests failed only `tests/test_openscad_wasm_simulator.py`: frozen SHA `363bcfdb85ab3ef27951c2d6e45c1a7c769e532c5489215c39d4071cb429ac37` had become `caab4001caf57e36ad3d54e0de366ecb02306cb462c3ea5e0b965568e3fae4eb`. SCAD, all other declared inputs and every candidate mesh still passed. The validator did not edit this test. Stop on the design's drift rule: the 17-test result applies only to the initially frozen test fingerprint; do not claim current full-manifest verification. Root must establish the changed test's intended ownership and refreeze the affected inputs before rerunning that affected gate. Unchanged source/artifact geometry evidence remains identified separately above.

**M1 — checksum inventory self-entry is invalid.** `scratch/vfr08-implementation/hashes.sha256` records itself as `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty file), but its actual hash is `06acda97e079e405e62010bbf26d68fe8884b96327d4f2d3ab869e76f9748140`. Its full verification returns exit1, with only that entry failing. Remove the self-entry and bind the corrected inventory from the outer candidate manifest; do not attempt a self-referential digest. This is a record-only correction, not a geometry failure or a reason to regenerate CAD. The sole-write validator did not modify it.

**L1 — implementation prose transcribes the new test hash incorrectly.** Its inline digest starts `a7297933430d2e2f`; actual/test manifests use `a7297933430d0e2f`. The test bytes themselves verify. Correct the receipt prose when the record-only correction is routed.

No scoped drain, topology, pattern, dimension or print-pose defect was found. DRAIN-08 and POSE-08 pass the independent evidence above. REQ-05 selected through-drain geometry and REQ-10 orientation are covered; broader support-free/slicer/physical claims are not.

Retain prior open VFR-06/07 browser, comprehensive clipping/ownership/self-intersection, assembled thread/service path and physical acceptance gaps. This task does not re-open those unrelated gates or turn corrected orientation into print acceptance. No browser or delivery-surface observation occurred. No new snapshot was written under this sole-document scope; selected-end and layout visual review remain the critic/formal-review join's evidence responsibility.

Next action: root resolves the changed test ownership, routes the smallest record-only corrections, refreezes affected inputs and reruns only the affected test/provenance gates before formal review. Unchanged source and mesh hashes allow geometry evidence to be carried with an explicit provenance addendum rather than rerunning the successful geometry matrix.

## Exact commands and verification notes

Root working directory for the following commands is the worktree above. Project-relative manifest checks ran with cwd `projects/laifen-wave-case`:

```sh
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR08_VALIDATION_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR08_VALIDATION_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR08_C1_CANDIDATE.sha256
```

Root commands:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run pytest projects/laifen-wave-case/tests/test_vfr08_functional_repair.py projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -p no:cacheprovider
shasum -a 256 -c projects/laifen-wave-case/scratch/vfr08-implementation/hashes.sha256
diff -u projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
```

Pytest exited0. The inventory check exited1 solely for M1. Diff exited1 as expected for the prescribed changes. An initial source reconstruction omitted the permitted comments/line break and failed; the exact reconstruction below includes them and passes. An initial high-level section traversal required unavailable `networkx`; the final command reads existing section entities directly and installs nothing. The body rim section at only0.01 mm below the mouth produced extra tiny traversal entities; direct rays and triangle parity passed, and the stable plane0.5 mm below the mouth returns the expected two loops in both unchanged body styles. This was an inspection-plane issue, not repaired geometry.

All remaining independent checks are reproduced by the exact stdin commands below. They print results and write no workspace artifacts.

### Mesh matrix, full-axis probes, aperture sections and volume

```sh
uv run python -B - <<'PY'
import json
from pathlib import Path
import numpy as np,trimesh
p=Path('projects/laifen-wave-case/scratch/vfr08-implementation')
def rays(m,origin,direction):
 t=m.triangles; o=np.asarray(origin); d=np.asarray(direction); e1=t[:,1]-t[:,0];e2=t[:,2]-t[:,0]
 h=np.cross(d,e2);det=np.einsum('ij,ij->i',e1,h); valid=np.abs(det)>1e-12
 inv=np.divide(1,det,out=np.zeros_like(det),where=valid);s=o-t[:,0];u=inv*np.einsum('ij,ij->i',s,h);q=np.cross(s,e1);v=inv*(q@d);dist=inv*np.einsum('ij,ij->i',e2,q)
 keep=valid&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(dist>=0)
 return np.unique(np.round(dist[keep],9))

from hashlib import sha256
meshes={}
centers=np.array([[0.,0.]]+[[9*np.cos(a),9*np.sin(a)] for a in np.arange(6)*np.pi/3])
offsets=np.array([[0.,0.],[.75,0.],[-.75,0.],[0.,.75],[0.,-.75]])
for path in sorted(p.glob('*.stl')):
 raw=trimesh.load_mesh(path,process=False);v,inv=np.unique(raw.vertices,axis=0,return_inverse=True);f=inv[raw.faces];m=trimesh.Trimesh(v,f,process=False);meshes[path.stem]=m
 _,uses=np.unique(np.sort(m.edges,axis=1),axis=0,return_counts=True)
 ncomp=len(m.split(only_watertight=False));expected_comp=2 if 'print_layout' in path.stem else 1
 assert m.is_watertight and m.is_winding_consistent and ncomp==expected_comp and m.volume>0 and np.all(uses==2)
 assert not np.any(m.area_faces<1e-12) and len(f)==len(np.unique(np.sort(f,axis=1),axis=0))
 row=dict(name=path.stem,vertices=len(v),triangles=len(f),euler=m.euler_number,components=ncomp,bounds=m.bounds.tolist(),volume=m.volume,topology_pass=True)
 if expected_comp==1:
  body=path.stem.endswith('body');selected=('bottom' in path.stem and body) or ('top' in path.stem and not body)
  floor=[0,3] if body else [81.01,84]
  assert m.euler_number==(-12 if selected else 2)
  for c in centers:
   for off in offsets:
    xyz=c+off;hits=rays(m,[*xyz,-1],[0,0,1])-1
    if selected:assert len(hits)==0,(path,xyz,hits)
    else:assert np.allclose(hits,floor,atol=1e-8),(path,xyz,hits)
  for x in [3,12]:assert np.allclose(rays(m,[x,0,-1],[0,0,1])-1,floor,atol=1e-8)
  row['drain_axes_plus_offsets']=35;row['through' if selected else 'closed']=True
  if selected:
   contours=[]
   for z in [floor[0]+.001,floor[1]-.001]:
    sec=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1]);loops=[e.discrete(sec.vertices) for e in sec.entities]
    assert len(loops)==8 and all(np.linalg.norm(q[0]-q[-1])<1e-8 for q in loops)
    holes=[q[:-1,:2] for q in loops if np.max(np.linalg.norm(q[:,:2],axis=1))<12]
    assert len(holes)==7
    measured=[]
    for q in holes:
     cc=(q.max(axis=0)+q.min(axis=0))/2
     assert np.min(np.linalg.norm(centers-cc,axis=1))<1e-7
     assert np.allclose(q.max(axis=0)-q.min(axis=0),[3,3],atol=1e-7)
     measured.append(cc.tolist())
    contours.append(dict(z=z,hole_centers=measured))
   row['aperture_sections']=contours
 print(json.dumps(row))
A96=96/2*1.5**2*np.sin(2*np.pi/96)
for style in ['diamond','smooth']:
 for role,mode,thickness in [('body','bottom',3),('cap','top',2.99)]:
  removed=meshes[f'{style}-none-{role}'].volume-meshes[f'{style}-{mode}-{role}'].volume
  expected=7*A96*thickness;assert abs(removed-expected)<1e-7
  print('REMOVED_VOLUME',style,role,removed,'EXPECTED',expected,'ERROR',removed-expected)
print('DEPTH_ZERO_EXACT_BYTES', (p/'diamond-depth0-bottom-body.stl').read_bytes()==(p/'smooth-bottom-body.stl').read_bytes())

PY
```

### Layout surface/pose and VFR-07 exterior/seam parity

```sh
uv run python -B - <<'PY'
import json
from pathlib import Path
import numpy as np,trimesh
p=Path('projects/laifen-wave-case/scratch/vfr08-implementation')
def rays(m,origin,direction):
 t=m.triangles; o=np.asarray(origin); d=np.asarray(direction); e1=t[:,1]-t[:,0];e2=t[:,2]-t[:,0]
 h=np.cross(d,e2);det=np.einsum('ij,ij->i',e1,h); valid=np.abs(det)>1e-12
 inv=np.divide(1,det,out=np.zeros_like(det),where=valid);s=o-t[:,0];u=inv*np.einsum('ij,ij->i',s,h);q=np.cross(s,e1);v=inv*(q@d);dist=inv*np.einsum('ij,ij->i',e2,q)
 keep=valid&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(dist>=0)
 return np.unique(np.round(dist[keep],9))


from scipy.spatial import cKDTree
def mesh(name):
 raw=trimesh.load_mesh(p/(name+'.stl'),process=False);v,inv=np.unique(raw.vertices,axis=0,return_inverse=True);return trimesh.Trimesh(v,inv[raw.faces],process=False)
def triangles_key(t):
 q=np.round(t,8);q=np.sort(q.view([('',q.dtype)]*3),axis=1).view(q.dtype).reshape(-1,9);return np.unique(q,axis=0)
for style,mode in [('diamond','bottom'),('smooth','top')]:
 layout=mesh(f'{style}-{mode}-print_layout');comps=sorted(layout.split(only_watertight=False),key=lambda x:x.bounds[0,0]);cap,body=comps
 gap=body.bounds[0,0]-cap.bounds[1,0];assert abs(gap-7)<1e-8
 for role,part in [('body',body),('cap',cap)]:
  ref=mesh(f'{style}-{mode}-{role}');v=ref.vertices.copy()
  if role=='body':v[:,0]+=23
  else:v[:,1]*=-1;v[:,2]=84-v[:,2];v[:,0]-=23
  err=max(cKDTree(v).query(part.vertices)[0].max(),cKDTree(part.vertices).query(v)[0].max());assert err<1e-6
  assert np.array_equal(triangles_key(v[ref.faces]),triangles_key(part.triangles))
  height=144 if role=='body' else 84;floor=3 if role=='body' else 2.99;cx=23 if role=='body' else -23
  hits=rays(part,[cx+3,0,-1],[0,0,1])-1;assert np.allclose(hits,[0,floor],atol=1e-8)
  mouth=rays(part,[cx,0,height-.01],[1,0,0]);assert len(mouth)==2 and mouth[0]>14
  sec=part.section(plane_origin=[0,0,height-.5],plane_normal=[0,0,1]);assert len(sec.entities)==2
  print(json.dumps(dict(layout=style,role=role,bounds=part.bounds.tolist(),surface_vertex_error=float(err),triangles_equal=True,offhole_floor_hits=hits.tolist(),mouth_radial_hits=mouth.tolist(),mouth_contours=len(sec.entities),gap=float(gap))))
for role,oldfile,newfile in [('body','body-final','diamond-bottom-body'),('cap','cap-final','diamond-top-cap')]:
 old=trimesh.load_mesh(p.parent/'vfr07-implementation'/(oldfile+'.stl'),process=False);new=mesh(newfile)
 def exterior(m):
  t=m.triangles;r=np.linalg.norm(t[:,:,:2],axis=2);return t[(r.min(axis=1)>18)&(np.ptp(t[:,:,2],axis=1)>1e-9)]
 a,b=exterior(old),exterior(new);assert np.array_equal(triangles_key(a),triangles_key(b))
 print('VFR07_EXACT_EXTERIOR_TRIANGLES',role,len(a),len(b))
b=mesh('diamond-bottom-body').vertices;c=mesh('diamond-top-cap').vertices
b=np.unique(b[(abs(b[:,2]-135)<1e-8)&(np.linalg.norm(b[:,:2],axis=1)>18),:2],axis=0)
c=np.unique(c[(abs(c[:,2])<1e-8)&(np.linalg.norm(c[:,:2],axis=1)>18),:2],axis=0)
assert np.array_equal(b,c);print('EXACT_SEAM',len(b),len(c))

PY
```

### Exact permitted source delta

```sh
uv run python -B - <<'PY'
from pathlib import Path
from hashlib import sha256
p=Path('projects/laifen-wave-case')
old=(p/'scratch/vfr07-implementation/candidate.scad').read_bytes()
assert sha256(old).hexdigest()=='48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31'
new=(p/'openscad/laifen_case_customizer_v1.scad').read_bytes()
expected=old.replace(b'cylinder(d=drain_diameter, h=h, center=true);',b'cylinder(d=drain_diameter, h=h, center=false);')
before=b'translate([-outer_diameter/2-3.5,0,0]) color("#77b09a") cap_shell();'
after=b'translate([-outer_diameter/2-3.5,0,cap_height])\n    rotate([180,0,0]) color("#77b09a") cap_shell();'
assert old.count(b'cylinder(d=drain_diameter, h=h, center=true);')==2 and old.count(before)==1
normalized=new.replace(b'  // VFR-08: callers provide the complete bounded axial interval.\n',b'').replace(b'  // VFR-08: print closed-end-down/open-end-up while preserving cap geometry.\n',b'')
assert expected.replace(before,after)==normalized
print('EXACT_THREE_FRAGMENT_DELTA',sha256(new).hexdigest())

PY
```

### Fresh candidate and frozen-none byte identities

```sh
node --input-type=module <<'JS'
import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';
import factory from './projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js';
const p='projects/laifen-wave-case/';const wasm=readFileSync(p+'preview/openscad-wasm-simulator/vendor/openscad.wasm');
const cases=[['diamond','bottom','body'],['diamond','bottom','cap'],['diamond','top','body'],['diamond','top','cap'],['diamond','bottom','print_layout'],['smooth','top','print_layout']];
for(const [style,mode,role] of cases) {
 const mod=await factory({noInitialRun:true,wasmBinary:wasm,print:()=>{},printErr:()=>{}});
 mod.FS.writeFile('/case.scad',readFileSync(p+'openscad/laifen_case_customizer_v1.scad'));
 const ret=mod.callMain(['/case.scad','--backend=Manifold','-D','surface_style="'+style+'"','-D','drainage_mode="'+mode+'"','-D','output_mode="'+role+'"','-o','/out.stl']);
 const name=[style,mode,role].join('-');const digest=x=>createHash('sha256').update(x).digest('hex');
 const actual=digest(mod.FS.readFile('/out.stl'));const expected=digest(readFileSync(p+'scratch/vfr08-implementation/'+name+'.stl'));
 if(ret!==0||actual!==expected)throw Error('Mismatch '+name);
 console.log(JSON.stringify({name,ret,exactBytes:true,sha256:actual}));
}
for(const style of ['smooth','diamond']) for(const role of ['body','cap']) {
 const mod=await factory({noInitialRun:true,wasmBinary:wasm,print:()=>{},printErr:()=>{}});
 mod.FS.writeFile('/case.scad',readFileSync(p+'scratch/vfr07-implementation/candidate.scad'));
 const ret=mod.callMain(['/case.scad','--backend=Manifold','-D','surface_style="'+style+'"','-D','drainage_mode="none"','-D','output_mode="'+role+'"','-o','/out.stl']);
 const digest=x=>createHash('sha256').update(x).digest('hex');const actual=digest(mod.FS.readFile('/out.stl'));
 const expected=digest(readFileSync(p+'scratch/vfr08-implementation/'+style+'-none-'+role+'.stl'));
 if(ret!==0||actual!==expected)throw Error('Baseline mismatch');
 console.log(JSON.stringify({baseline:style+'-none-'+role,ret,exactBytes:true,sha256:actual}));
}

JS
```

### Actual source cutter boundary cases

```sh
node --input-type=module <<'JS'
import {readFileSync} from 'node:fs';
import factory from './projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js';
const p='projects/laifen-wave-case/';const source=readFileSync(p+'openscad/laifen_case_customizer_v1.scad','utf8');
const prefix=source.slice(0,source.indexOf('if (VFR04_PROBE_MODE == "short_band")'));
for(const [thickness,height] of [[2,97],[3,84],[8,97]]) for(const mode of ['bottom','top']) {
 const logs=[];const mod=await factory({noInitialRun:true,wasmBinary:readFileSync(p+'preview/openscad-wasm-simulator/vendor/openscad.wasm'),print:x=>logs.push(String(x)),printErr:x=>logs.push(String(x))});
 const call=source.split('\n').find(x=>x.includes('if (drainage_mode == "'+mode+'")'));
 mod.FS.writeFile('/probe.scad',prefix+'\n'+call);
 const ret=mod.callMain(['/probe.scad','--backend=Manifold','-D','floor_thickness='+thickness,'-D','split_distance_from_top='+height,'-D','drainage_mode="'+mode+'"','-o','/out.stl']);
 const stl=mod.FS.readFile('/out.stl',{encoding:'utf8'});const verts=[...stl.matchAll(/vertex\s+(\S+)\s+(\S+)\s+(\S+)/g)].map(x=>x.slice(1).map(Number));
 const z=verts.map(x=>x[2]);const actual=[Math.min(...z),Math.max(...z)];const expected=mode==='bottom'?[-.1,thickness+.1]:[height-thickness-.1,height+.1];
 if(ret!==0||actual.some((x,i)=>Math.abs(x-expected[i])>1e-8)||logs.some(x=>/ERROR|WARNING|Assertion/.test(x)))throw Error('Probe failed');
 console.log(JSON.stringify({thickness,height,mode,interval:actual,ret}));
}

JS
```

### Face-adjacent aperture sections against the 96-gon

```sh
uv run python -B - <<'PY'
import numpy as np,trimesh
from pathlib import Path
p=Path('projects/laifen-wave-case/scratch/vfr08-implementation')
for name,levels in [('diamond-bottom-body',[.001,2.999]),('diamond-top-cap',[81.011,83.999]),('smooth-bottom-body',[.001,2.999]),('smooth-top-cap',[81.011,83.999])]:
 m=trimesh.load_mesh(p/(name+'.stl'),process=False)
 maxerr=0
 for z in levels:
  sec=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
  for entity in sec.entities:
   q=entity.discrete(sec.vertices)[:-1,:2]
   if np.max(np.linalg.norm(q,axis=1))>=12:continue
   c=(q.max(axis=0)+q.min(axis=0))/2;q=q-c
   a=2*np.pi*np.arange(96)/96
   v=1.5*np.column_stack([np.cos(a),np.sin(a)])
   edges=np.roll(v,-1,axis=0)-v
   delta=q[:,None,:]-v[None,:,:]
   t=np.clip(np.einsum('qei,ei->qe',delta,edges)/np.sum(edges*edges,axis=1),0,1)
   d=np.linalg.norm(delta-t[:,:,None]*edges[None,:,:],axis=2).min(axis=1)
   maxerr=max(maxerr,float(d.max()));assert d.max()<1e-7
 print(name,'max_section_to_prescribed_96gon',maxerr)

PY
```
