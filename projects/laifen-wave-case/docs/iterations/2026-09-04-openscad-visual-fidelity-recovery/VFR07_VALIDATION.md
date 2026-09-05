# VFR-07 independent C1 validation

Status: **PARTIAL — independent bounded source/mesh checks pass; full V06 acceptance is not established. Browser diamond remains pending.**

Owner: `/root/openscad_vfr07_validator`, independent validator, distinct from implementation and critique. Sole changed path: this document. No source, tests, frozen artifacts, browser, runtime, service, slicer, printer, or continuity index changed. All generated comparison meshes existed only in the WASM virtual filesystem; no candidate artifact was overwritten.

## Provenance

- Worktree: `/Users/scottchu/.codex/worktrees/4f8c/design-projects`.
- Project: `projects/laifen-wave-case`; iteration: `2026-09-04-openscad-visual-fidelity-recovery`.
- Validation input fingerprint: `25ff3222014368aa0137cdd00d7043fa0ce13ebd36d225f20a3419b88a7b4c3a`, **10/10 entries OK**.
- C1 candidate manifest: `c95ca570ada87f7fad216c1beba08c0933764bddeb9fb1be7903075c39526101`, **13/13 entries OK**.
- Authoritative SCAD: `48b4ac84dc0cf4b8274200e9e2e13f145cfc01a5f721f975c37d1166c91ebd31`.
- Focused customizer test: `be973544f458701851aa1b01d3aa638121b50733663245fb84983124331ae6b4`.
- Supplementary preserved baseline used for source/geometry parity: `scratch/vfr06-implementation/frozen.scad`, independently hashed `4e6ccd68f95d583d0c3b93bc33442d01107af90b5e66267bfe20034732e0d672`, matching the baseline named by the frozen VFR-06 architecture.
- Pinned JS/WASM identities were verified by the existing preflight verifier: `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` / `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26`.
- Read root AGENTS/CAD workflow, project state/handoff, requirements, experience, decisions, active brief, B decision and frozen VFR-06/VFR-07 contracts. Applied CAD skill's source/geometry/acceptance separation. No relevant memory entry was found.

## Independent results

The focused two-file pytest run passed all **14** tests. The syntax-delta verifier confirmed the single missing outer-list terminator repair, unchanged attempted test, and exact scratch-to-authoritative source equality. The preflight verifier validated the existing five receipts and declared coverage of 50 helpers; that command validates retained receipts, not a new execution of their original timing probes.

A separate fresh source execution emitted actual production G2, trimmed G2 and coincident-endpoint arrays. Evaluation took **847.665 ms** in pinned WASM. Each had no unused vertices, duplicate XYZ records, duplicate faces, repeated-index/zero-area triangles or invalid vertex links; all edges had two opposite directed uses, one component and Euler 2:

| Source-emitted data case | Vertices | Triangles |
|---|---:|---:|
| G2 global 131.93..139.06 | 1,586 | 3,168 |
| Same band with 1.2 mm lower trim | 2,048 | 4,092 |
| Coincident v=-0.5..0.5 | 695 | 1,386 |

These checks consumed source-emitted indices directly. Echo coordinates have OpenSCAD's display precision; exact numerical artifact checks below use the full written STL coordinates. Host code neither created nor repaired geometry.

Fresh source Manifold runs independently reproduced **the exact bytes of all three frozen C1 STL files**:

| Artifact under scratch/vfr07-implementation/ | SHA-256 | Fresh Node wall / compile-export ms |
|---|---|---:|
| g2-short-band.stl | `1923d030999cacbd256d4c551b539c29d5a08ec1ed84d35edc9f2c79be7fe00f` | 287.887 / 258.318 |
| body-final.stl | `0cb0fcd9f420e68b548302bd0018d6f7a848f55caaf1653e3eeb13208605c4a3` | 3,094.720 / 3,079.676 |
| cap-final.stl | `e9629eb47fc215a914d6579c77af945d96d935789a44a5cacb7557bd0dbcd514` | 2,025.863 / 2,012.370 |

All returns were zero. Body/cap reported Manifold `NoError`. Only the known localization diagnostic appeared. These are **Node evidence-only reproductions of existing artifacts**, not the required actual browser-worker runs or permission to advance sequential browser gates.

### Actual written-mesh topology and identity

Exact XYZ indexing was used only to inspect STL incidence; no tolerance welding, cleanup or serialization was performed.

| Artifact | Vertices / faces | Bounds X; Y; Z mm | Volume mm3 |
|---|---:|---|---:|
| G2 | 1,586 / 3,168 | ±19.5; ±19.49826809; 0..7.13 | 8,316.935598 |
| Body | 27,874 / 55,744 | ±19.5; ±19.49826809; 0..144 | 65,337.408528 |
| Cap | 20,257 / 40,510 | ±19.5; ±19.49826809; 0..84 | 35,766.812584 |

All three: watertight, consistent winding, one connected component, Euler 2, positive volume, every edge used twice, no duplicate triangles and no degenerate faces. The two roles retain separate local identities. The body's external seam is z=135; the cap's is local z=0.

The actual outer seam XYZ projections are **99 vertices each, exactly equal**, with nearest discrepancy **0 mm**. A separate production-data assertion also passed the same equality. The physical-angle annulus at phase 0 and phase 17 degrees has 99 outer / 96 internal vertices and exactly 195 consistently oriented, nondegenerate triangles. Its area equals outer polygon minus inner polygon within 4.55e-13 mm2. The internal ring's first point remains **[16.4, 0, 135]** in both cases. This covers unequal rings, default equal-angle events, wrap and a nonzero external phase without rotating the internal datum.

### B math and radial error

The focused tests execute the actual SCAD math witnesses and independent Python oracle. Defaults retain valley-derived **N33**, half-up rounding, plateau half-fraction **0.18**, global seam **135**, pitch **4.8**, crest/valley **19.5/19.05**, body/cap shared phase, 1.041776914 mm developed plateau width and 0.29296875 axial slope. No external collar was introduced.

On every selected lateral exterior triangle, independent code sampled **three interior points using seed 404**, its centroid and all three edge midpoints. Selection requires all radii >18 mm and nonzero axial extent; this excludes disks, internal surfaces and the shoulder. It covers exterior wrap, endpoints and chamfers. Targets are the independent B field at physical atan2/global Z, clipped by the appropriate end cone.

| Artifact | Side triangles | Samples | Maximum / p99 / mean error mm | Actual-triangle analytic maximum mm |
|---|---:|---:|---|---:|
| G2 | 2,706 | 18,942 | 0.012886374592 / 0.012886372409 / 0.004168568445 | 0.013388067285 |
| Body | 34,716 | 243,012 | 0.012886374592 / 0.012886373114 / 0.005279648962 | 0.013694028294 |
| Cap | 22,110 | 154,770 | 0.012886374592 / 0.012886373114 / 0.005172259056 | 0.017661156965 |

All are below **0.025 mm**. All exterior triangle counts are below **250,000**. The analytic calculation applies the frozen VFR-06 angular-shift formula to actual triangle radii/angular spans; maximum span is approximately 0.3600000021 u. Its correctness still relies on the architecture's affine-patch containment premise; this run did not independently exhaust every clipping-coincidence/self-intersection fixture.

Worst sample provenance uses original STL triangle indices and local XYZ: G2 triangle 220 at [13.510322325,-13.733454175,7.054]; body triangle 5389 at [13.510322325,13.733454175,131.016]; cap triangle 7963 at [-13.510322325,-13.733454175,78.384].

### Protected profiles, floors, threads and drains

Source-emitted profiles exactly match the frozen contract:

- Body: (16.4,135) → (16.4,144) → (15,144) → (15,3).
- Cap: (17.05,0) → (16.65,0.4) → (16.65,9) → (15.5,9) → (15.5,81.01).

Independent ray/triangle intersections on actual STL confirm body bore radius 15 at z=3.01,50,134.9; root radius 16.4 above the shoulder; cap entry radius 17.049 at z=.001, 16.85 at .2, 16.65 at .4..8.9, and bore 15.5 at z=9.1,50,81. The undrained body floor is z=0..3; cap floor is **81.01..84 = 2.99 mm**.

Actual body thread/root vertices span radius approximately 16.391232394..16.9; female groove vertices reach **17.15**. These agree with the retained helix/faceted-root placement; source engagement is 6 mm inside 9 mm overlap, with unchanged 0.05 mm constructive embed and 0.25 mm radial clearance. The default nominal patterned walls are body 4.05, cap 3.55 and female groove 1.9 mm before tessellation. Actual outer error measurements leave the patterned female wall above 1.8 mm on the validated exterior under the radial-profile assumptions. This is not a complete global minimum-distance wall or thread-contact proof.

Defaults/derivation and eight protected modules were compared byte-for-byte with the frozen baseline: drain pattern, male thread, female void/groove, both outer envelopes, closed assembly and print-layout transforms. All unchanged. Smooth body/cap and C1 zero-depth diamond independently emitted exactly the same STL bytes as frozen smooth baseline:

- Body: `28e1cf21cba70b2c31d1dcbf11842fde9cb7bad71556b8c7fcd58c39260989e3`.
- Cap: `646efb49c116b47b49521872c0e35af724053f9fbaa619c412aca40009e0b7d0`.

Actual SCAD at depth 0.60 still raises the female-thread-valley-wall assertion. Its `.echo` command returns zero despite containing `ERROR`; checking return code alone would be insufficient. The frozen preflight runner additionally inspects diagnostic/echo content.

## Findings and coverage limits

**H1 — inherited drainage functionality gap, confirmed in actual body STL.** The selected bottom cutter is centered with h=3.2 and translated to z=-0.1, so its upper extent is z=1.5. Actual vertical intersections at both the center drain (0,0) and a ring drain (9,0) are **z=1.5 and z=3**, leaving a **1.5 mm solid roof**. This is a blind pocket, not a through-drain. Off-drain probes at x=3 and x=12 show the full 3 mm floor. Source parity proves preservation of the baseline cutter rather than a newly introduced C1 error. Do not silently repair protected drainage under this recovery task; root should record or route a separate scope decision. REQ-05 drainage/function and later physical drainage acceptance cannot be marked passed.

**H2 — actual browser-worker acceptance remains unmeasured, known scope blocker.** Fresh Node timings and exact bytes cannot pass V06-3B/3C. The unchanged worker remains smooth-only. No enablement, deployment, UI change, worker change or user delivery-surface validation occurred.

**M1 — full V06-1/3P acceptance coverage remains partial.** This run checked source-emitted short-band topology/vertex links, actual STL topology, profiles, seam/annulus, error, protected source and smooth parity. It did not exhaust all h-equality/trim-coincidence ownership fixtures, independently prove every triangle's affine patch membership, perform a general geometric self-intersection/T-junction search, run the required direct-body-before-Boolean timing gate, or prove actual assembled thread collision/service paths. The original preflights chiefly establish syntax/type/shape and cannot substitute for those remaining gates.

No new C1 topology or scoped protected-geometry regression was observed. These findings do not constitute implementer approval, critic acceptance or formal independent review.

| Requirement/risk | Evidence disposition |
|---|---|
| B selection, N33, plateau, shared phase/to-seam | Independent math, source data and actual seam pass |
| Source owns geometry; output identity | Three byte-identical independent source reproductions pass |
| Mesh topology/bounds, local part identities | All three exact artifacts pass stated checks |
| Bore/floor/entry/root/groove contract | Source profiles and targeted actual-mesh evidence pass; global fit/contact not claimed |
| Through drainage | **Fails function; inherited/protected**, H1 |
| Smooth/depth-zero preservation; .60 rejection | Actual source execution and byte parity pass |
| Complete V06-1 / direct body / actual browser gates | **Pending/partial**, M1/H2 |
| CAD/STEP, slicer/process, physical fit/printing | **Not accepted by this task** |

No snapshot was created: sole-write read-only validation scope excludes new review artifacts, and this receipt makes no feature-specific visual or user-surface claim. Visual critique and browser delivery review remain separate owner gates. No source or output correction is recommended from the passing scoped topology/error checks alone.

Next action: root joins this exact-fingerprint receipt with the critic and formal reviewer, retains browser diamond disabled, and routes the outstanding browser/coverage and inherited drainage decisions without broadening the C1 syntax recovery.

## Commands and reproducibility

All commands below were run from the worktree root unless a project-directory working directory is explicitly shown. Python ran through root `uv run` and the root Python 3.12 environment. The first attempt to use trimesh's ray accelerator failed with `ModuleNotFoundError: No module named 'rtree'`; no dependency was installed. The successful read-only replacement below performs direct vectorized Möller–Trumbore ray/triangle intersections.

Project-directory provenance commands (all successful):

```sh
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR07_VALIDATION_INPUTS.sha256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR07_C1_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/inputs/VFR07_VALIDATION_INPUTS.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR07_C1_CANDIDATE.sha256
```

Root focused commands (all exit 0):

```sh
PYTHONDONTWRITEBYTECODE=1 uv run pytest projects/laifen-wave-case/tests/test_openscad_customizer.py projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q -p no:cacheprovider
uv run python -B projects/laifen-wave-case/scratch/vfr07-implementation/verify-delta.py
uv run python -B projects/laifen-wave-case/scratch/vfr07-implementation/verify-preflight.py
cmp projects/laifen-wave-case/scratch/vfr07-implementation/candidate.scad projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad
shasum -a 256 projects/laifen-wave-case/scratch/vfr06-implementation/frozen.scad
```

The following exact stdin commands are the independent checks actually run. They print compact results and write no workspace artifacts.

### Written mesh topology and direct rays

```sh
uv run python -B - <<'PY'
import json
from pathlib import Path
import numpy as np,trimesh
p=Path('projects/laifen-wave-case/scratch/vfr07-implementation')
def rays(m,origin,direction):
 t=m.triangles; o=np.asarray(origin); d=np.asarray(direction); e1=t[:,1]-t[:,0];e2=t[:,2]-t[:,0]
 h=np.cross(d,e2);det=np.einsum('ij,ij->i',e1,h); valid=np.abs(det)>1e-12
 inv=np.divide(1,det,out=np.zeros_like(det),where=valid);s=o-t[:,0];u=inv*np.einsum('ij,ij->i',s,h);q=np.cross(s,e1);v=inv*(q@d);dist=inv*np.einsum('ij,ij->i',e2,q)
 keep=valid&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(dist>=0)
 return np.unique(np.round(dist[keep],9))
for name in ['g2-short-band','body-final','cap-final']:
 raw=trimesh.load_mesh(p/(name+'.stl'),process=False); v,inv=np.unique(raw.vertices,axis=0,return_inverse=True);f=inv[raw.faces];m=trimesh.Trimesh(v,f,process=False)
 _,uses=np.unique(np.sort(m.edges,axis=1),axis=0,return_counts=True)
 print(json.dumps(dict(name=name,vertices=len(v),faces=len(f),bounds=m.bounds.tolist(),volume=m.volume,watertight=m.is_watertight,winding=m.is_winding_consistent,components=len(m.split(only_watertight=False)),euler=m.euler_number,edge_use=np.unique(uses).tolist(),degenerate=int((m.area_faces<1e-12).sum()),duplicate_faces=len(f)-len(np.unique(np.sort(f,axis=1),axis=0)))))
 if name=='g2-short-band': continue
 for x,y in [(0,0),(9,0),(3,0),(12,0)]:
  print(name,'vertical',x,y,(rays(m,[x,y,-1],[0,0,1])-1).tolist())
 for z in ([1,1.5,2,2.99,3.01,50,134.9,135.01,136,138,143.9] if name=='body-final' else [.001,.2,.4,1,3,8.9,9.1,50,81,81.02,83]):
  print(name,'radial',z,rays(m,[0,0,z],[1,0,0]).tolist())

PY
```

### Actual exterior samples and exact seam equality

```sh
uv run python -B - <<'PY'
import json
from pathlib import Path
import numpy as np,trimesh
p=Path('projects/laifen-wave-case/scratch/vfr07-implementation')
def field(q,offset,role):
 z=q[:,2]+offset;u=33*np.arctan2(q[:,1],q[:,0])/(2*np.pi);v=(z-135)/4.8
 s=u+v;t=u-v;s-=np.floor(s+.5);t-=np.floor(t+.5)
 radius=19.05+.45*np.clip((.5-np.maximum(abs(s),abs(t)))/.32,0,1)
 if role=='body-final': radius=np.minimum(radius,18.3+z)
 if role=='cap-final': radius=np.minimum(radius,18.3+219-z)
 return radius
meshes={}
for name,offset in [('g2-short-band',131.93),('body-final',0),('cap-final',135)]:
 m=trimesh.load_mesh(p/(name+'.stl'),process=False);meshes[name]=m
 tri=m.triangles;r=np.linalg.norm(tri[:,:,:2],axis=2);sel=(r.min(axis=1)>18)&(np.ptp(tri[:,:,2],axis=1)>1e-9);ids=np.where(sel)[0];tri=tri[sel]
 rng=np.random.default_rng(404);uv=rng.random((len(tri),3,2));sqrt=np.sqrt(uv[:,:,0]);w=np.stack([1-sqrt,sqrt*(1-uv[:,:,1]),sqrt*uv[:,:,1]],axis=2)
 w=np.concatenate([w,np.broadcast_to(np.array([[1/3]*3,[.5,.5,0],[.5,0,.5],[0,.5,.5]]),(len(tri),4,3))],axis=1)
 q=np.einsum('tki,tij->tkj',w,tri).reshape(-1,3);errors=abs(np.linalg.norm(q[:,:2],axis=1)-field(q,offset,name));idx=np.argmax(errors)
 print(json.dumps(dict(name=name,side_triangles=len(tri),samples=len(q),max=float(errors.max()),p99=float(np.percentile(errors,99)),mean=float(errors.mean()),worst_triangle=int(ids[idx//7]),worst_point=q[idx].tolist(),pass025=bool(errors.max()<.025))))
b=meshes['body-final'].vertices;c=meshes['cap-final'].vertices
b=b[(abs(b[:,2]-135)<1e-8)&(np.linalg.norm(b[:,:2],axis=1)>18),:2]
c=c[(abs(c[:,2])<1e-8)&(np.linalg.norm(c[:,:2],axis=1)>18),:2]
b=np.unique(b,axis=0);c=np.unique(c,axis=0)
print(json.dumps(dict(seam_body_vertices=len(b),seam_cap_vertices=len(c),exact_equal=np.array_equal(b,c),max_nearest=max(np.min(np.linalg.norm(b[:,None]-c[None,:],axis=2),axis=1)))))

PY
```

### Production source-emitted array topology and seam

```sh
uv run python -B - <<'PY'
import subprocess,json
import numpy as np,trimesh
script="import {readFileSync} from 'node:fs';\nimport factory from './projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js';\nconst root='projects/laifen-wave-case/';\nconst source=readFileSync(root+'openscad/laifen_case_customizer_v1.scad','utf8');\nconst prefix=source.slice(0,source.indexOf('if (VFR04_PROBE_MODE == \"short_band\")'));\nconst diagnostics=[];\nconst mod=await factory({noInitialRun:true,wasmBinary:readFileSync(root+'preview/openscad-wasm-simulator/vendor/openscad.wasm'),print:x=>diagnostics.push(String(x)),printErr:x=>diagnostics.push(String(x))});\nconst probe=String.raw`\nfor(c=[[131.93,139.06,\"none\"],[131.93,139.06,\"trim_band\"],[132.6,137.4,\"none\"]]) {\n data=v06_data((c[0]-body_thread_z)/diamond_axial_pitch,(c[1]-body_thread_z)/diamond_axial_pitch,c[0],c[2],c[1]-c[0]);\n mesh=v06_closed_band(data);\n echo(\"MESH\",c,mesh[0],mesh[1]);\n}\nb=v06_data(-1,0,0,\"body\",cap_height);\nc=v06_data(0,1,cap_close_z,\"cap\",cap_height);\nbr=[for(i=v06_ring_indices(b,1))[b[0][i][0],b[0][i][1]]];\ncr=[for(i=v06_ring_indices(c,0))[c[0][i][0],c[0][i][1]]];\nassert(br==cr,\"Independent seam ring mismatch\");\necho(\"SEAM\",len(br),br==cr);\ncube(.01);\n`;\nmod.FS.writeFile('/validate.scad',prefix+probe);\nconst started=performance.now();const ret=mod.callMain(['/validate.scad','-o','/validate.echo']);const ms=performance.now()-started;\nconst echo=mod.FS.readFile('/validate.echo',{encoding:'utf8'});\nconsole.log(JSON.stringify({ret,ms,diagnostics,echo}));\n"
r=subprocess.run(['node','--input-type=module'],input=script,text=True,capture_output=True,timeout=20,check=True)
data=json.loads(r.stdout);assert data['ret']==0;assert not any(x in data['echo'] for x in ['ERROR','WARNING','undef'])
print('SOURCE_ARRAY_EVALUATION_MS',data['ms'],'DIAGNOSTICS',data['diagnostics'])
for line in data['echo'].splitlines():
 row=json.loads('['+line.removeprefix('ECHO: ')+']')
 if row[0]!='MESH':print(row);continue
 _,case,v,f=row;v=np.asarray(v);f=np.asarray(f);m=trimesh.Trimesh(v,f,process=False)
 _,uses=np.unique(np.sort(m.edges,axis=1),axis=0,return_counts=True)
 badlinks=0
 links=[[] for _ in v]
 for a,b,c in f:links[a].append((b,c));links[b].append((c,a));links[c].append((a,b))
 for edges in links:
  adj={}
  for a,b in edges:adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
  if not adj or any(len(n)!=2 for n in adj.values()):badlinks+=1;continue
  seen=set();todo=[next(iter(adj))]
  while todo:
   a=todo.pop()
   if a in seen:continue
   seen.add(a);todo.extend(adj[a]-seen)
  badlinks+=len(seen)!=len(adj)
 print(json.dumps(dict(case=case,vertices=len(v),faces=len(f),unused=len(v)-len(np.unique(f)),duplicate_xyz=len(v)-len(np.unique(v,axis=0)),duplicate_faces=len(f)-len(np.unique(np.sort(f,axis=1),axis=0)),edge_use=np.unique(uses).tolist(),winding=m.is_winding_consistent,euler=m.euler_number,components=len(m.split(only_watertight=False)),degenerate=int((m.area_faces<1e-12).sum()),bad_vertex_links=badlinks)))

PY
```

### Fresh source-to-artifact byte identity

```sh
node --input-type=module <<'JS'
import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';
import factory from './projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js';
const p='projects/laifen-wave-case/'; const source=readFileSync(p+'openscad/laifen_case_customizer_v1.scad');
for(const [name,defs] of [['g2-short-band',['VFR04_PROBE_MODE="short_band"']],['body-final',['output_mode="body"']],['cap-final',['output_mode="cap"']]]) {
 const diagnostics=[];const start=performance.now();
 const mod=await factory({noInitialRun:true,wasmBinary:readFileSync(p+'preview/openscad-wasm-simulator/vendor/openscad.wasm'),print:x=>diagnostics.push(String(x)),printErr:x=>diagnostics.push(String(x))});
 mod.FS.writeFile('/case.scad',source);const before=performance.now();
 const ret=mod.callMain(['/case.scad','--backend=Manifold',...defs.flatMap(x=>['-D',x]),'-o','/out.stl']);
 const bytes=mod.FS.readFile('/out.stl');const actual=createHash('sha256').update(bytes).digest('hex'); const expected=createHash('sha256').update(readFileSync(p+'scratch/vfr07-implementation/'+name+'.stl')).digest('hex');
 console.log(JSON.stringify({name,ret,wallMs:performance.now()-start,compileExportMs:performance.now()-before,sha256:actual,exactArtifactIdentity:actual===expected,diagnostics}));
}

JS
```

### Actual-triangle analytic bounds and protected radial witnesses

```sh
uv run python -B - <<'PY'
import json
from pathlib import Path
import numpy as np,trimesh
p=Path('projects/laifen-wave-case/scratch/vfr07-implementation')
for name in ['g2-short-band','body-final','cap-final']:
 m=trimesh.load_mesh(p/(name+'.stl'),process=False);tri=m.triangles;r=np.linalg.norm(tri[:,:,:2],axis=2)
 mask=(r.min(axis=1)>18)&(np.ptp(tri[:,:,2],axis=1)>1e-9);t=tri[mask];r=r[mask]
 theta=np.unwrap(np.arctan2(t[:,:,1],t[:,:,0]),axis=1);delta=np.ptp(theta,axis=1)
 rmin=r.min(axis=1);rmax=r.max(axis=1);dr=rmax-rmin;L=.45*33/(2*np.pi*.32)
 E=rmax*(1-np.cos(delta/2))+L*np.arctan((dr*delta/4+rmax*delta**3/6)/(rmin*np.cos(delta)))+.000002
 print(json.dumps(dict(name=name,analytic_bound_max=float(E.max()),max_span_u=float(delta.max()*33/(2*np.pi)),pass025=bool(E.max()<=.025))))
 if name!='g2-short-band':
  v=m.vertices;rad=np.linalg.norm(v[:,:2],axis=1)
  for lo,hi in ([(3.01,134.99),(135.01,143.99)] if name=='body-final' else [(.001,.4),(.4,8.99),(9.01,81)]):
   s=(v[:,2]>=lo)&(v[:,2]<=hi);outer=rad[s&(rad>18)];inside=rad[s&(rad<18)]
   print(name,'vertex radial interval',lo,hi,'outer',None if not len(outer) else [float(outer.min()),float(outer.max())],'inner/root',None if not len(inside) else [float(inside.min()),float(inside.max())])

PY
```

### Smooth/depth-zero baseline parity and depth rejection

```sh
node --input-type=module <<'JS'
import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';
import factory from './projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js';
const p='projects/laifen-wave-case/';const wasm=readFileSync(p+'preview/openscad-wasm-simulator/vendor/openscad.wasm');
for (const role of ['body','cap']) {
 const rows=[];
 for(const [src,style,depth] of [['scratch/vfr06-implementation/frozen.scad','smooth',.45],['openscad/laifen_case_customizer_v1.scad','smooth',.45],['openscad/laifen_case_customizer_v1.scad','diamond',0]]) {
  const logs=[];const mod=await factory({noInitialRun:true,wasmBinary:wasm,print:x=>logs.push(String(x)),printErr:x=>logs.push(String(x))});
  mod.FS.writeFile('/case.scad',readFileSync(p+src));const ret=mod.callMain(['/case.scad','--backend=Manifold','-D','output_mode="'+role+'"','-D','surface_style="'+style+'"','-D','diamond_depth='+depth,'-o','/out.stl']);
  rows.push({src,style,depth,ret,sha256:createHash('sha256').update(mod.FS.readFile('/out.stl')).digest('hex'),errors:logs.filter(x=>/ERROR|WARNING|Assertion/.test(x))});
 }
 console.log(JSON.stringify({role,rows,exactEqual:rows.every(x=>x.sha256===rows[0].sha256)}));
}
const logs=[];const mod=await factory({noInitialRun:true,wasmBinary:wasm,print:x=>logs.push(String(x)),printErr:x=>logs.push(String(x))});
mod.FS.writeFile('/case.scad',readFileSync(p+'openscad/laifen_case_customizer_v1.scad'));
const ret=mod.callMain(['/case.scad','-D','diamond_depth=.6','-o','/out.echo']);
console.log(JSON.stringify({depth06Ret:ret,diagnostics:logs,echo:mod.FS.readFile('/out.echo',{encoding:'utf8'})}));

JS
```

### Nonzero-phase annulus and profile proof

```sh
uv run python -B - <<'PY'
import subprocess,json
import numpy as np
script="import {readFileSync} from 'node:fs';\nimport factory from './projects/laifen-wave-case/preview/openscad-wasm-simulator/vendor/openscad.js';\nconst p='projects/laifen-wave-case/';let s=readFileSync(p+'openscad/laifen_case_customizer_v1.scad','utf8');s=s.slice(0,s.indexOf('if (VFR04_PROBE_MODE == \"short_band\")'));\nconst probe=`d=v06_data(-1,0,0,\"body\",cap_height);n=len(d[0]);o=v06_outer_angles(d,1);ip=v06_internal_points([[thread_root_radius,body_thread_z]]);f=v06_zip(o,n,true);echo(\"ANNULUS\",concat(d[0],ip),f,[for(x=o)x[1]],n);echo(\"PROFILE\",v06_profile(\"body\"),v06_profile(\"cap\"));cube(.01);`;\nfor(const phase of [0,17]) {\n const mod=await factory({noInitialRun:true,wasmBinary:readFileSync(p+'preview/openscad-wasm-simulator/vendor/openscad.wasm'),print:()=>{},printErr:()=>{}});\n mod.FS.writeFile('/v.scad',s+probe);const ret=mod.callMain(['/v.scad','-D','diamond_phase_deg='+phase,'-o','/out.echo']);\n console.log(JSON.stringify({phase,ret,echo:mod.FS.readFile('/out.echo',{encoding:'utf8'})}));\n}"
r=subprocess.run(['node','--input-type=module'],input=script,text=True,capture_output=True,check=True,timeout=10)
for line in r.stdout.splitlines():
 data=json.loads(line);assert data['ret']==0
 for echo in data['echo'].splitlines():
  row=json.loads('['+echo.removeprefix('ECHO: ')+']')
  if row[0]!='ANNULUS':print(data['phase'],row);continue
  _,points,faces,outer,n=row;p=np.asarray(points);f=np.asarray(faces);t=p[f];z=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])[:,2]
  def area(q):return abs(np.sum(q[:,0]*np.roll(q[:,1],-1)-q[:,1]*np.roll(q[:,0],-1)))/2
  expected=area(p[outer])-area(p[n:n+96]);actual=np.abs(z).sum()/2
  print(json.dumps(dict(phase=data['phase'],outer_count=len(outer),inner_count=96,triangles=len(f),all_negative=bool((z<0).all()),minimum_area=float(abs(z).min()/2),area_discrepancy=float(abs(actual-expected)),inner_datum=p[n].tolist())))

PY
```

### Protected source-region parity

```sh
uv run python -B - <<'PY'
from pathlib import Path
from hashlib import sha256
p=Path('projects/laifen-wave-case')
old=(p/'scratch/vfr06-implementation/frozen.scad').read_text()
new=(p/'openscad/laifen_case_customizer_v1.scad').read_text()
def module(s,name):
 start=s.index('module '+name+'(');a=s.index('{',start);depth=1;i=a+1
 while depth:
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[start:i]
for name in ['drain_pattern','body_thread','female_thread_void','female_thread_groove','body_outer_envelope','cap_outer_envelope','closed_assembly','print_layout']:
 a,b=module(old,name),module(new,name);assert a==b
 print(name,sha256(a.encode()).hexdigest(),'unchanged')
assert old[:old.index('// VFR-04 pure field contract.')]==new[:new.index('// VFR-04 pure field contract.')]
print('DEFAULT_PARAMETERS_AND_DERIVATION_UNCHANGED')

PY
```

