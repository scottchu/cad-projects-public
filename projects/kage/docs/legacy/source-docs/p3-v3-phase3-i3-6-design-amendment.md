# KAGE P3 V3 Phase-3 I3.6 — bit-exact mask and complete profile closure

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation**

Date: **2026-08-19**

Supersedes: `p3-v3-phase3-i3-5-design-amendment.md` wherever this document is
more specific or conflicting.

Immutable predecessors:

```text
I3.1  abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77
I3.2  9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3
I3.3  4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691
I3.4  c6fb12ceab347b258b4f3be65b61d32f178bbf3075cf68869d5d87e9d47636e1
I3.5  08ab0d28e84036a3bcf17e74e9d3ab18d22c376f8a9f71f4cd1fd6494ede35d6
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

This amendment freezes a bit-exact CPU raster contract and closes the complete
active Snapmaker Orca application, configuration, machine, process, and
filament inheritance chains. It does not modify CAD, source, tests, meshes,
profiles, or the functional 300 mm clock.

## 1. Numeric representation and source coordinates

The normative algorithm is the **Pineda half-space triangle rasterizer** with
the constants and tie rules below. It uses no browser, WebGL, GPU, shader,
device pixel ratio, or implementation-defined math.

All floating operations are IEEE-754 binary64, round-to-nearest ties-to-even.
Subnormals are preserved. Fused multiply-add, extended-precision temporaries,
fast-math reassociation, and epsilon comparisons are forbidden. Every
multiply/add expression is evaluated left-to-right with a binary64 rounding
after every elementary operation. JSON decimals must be correctly rounded to
binary64; the fixed camera constants below are supplied as hexadecimal binary64
literals and those bit patterns are authoritative.

GLB positions are decoded as exact accessor binary32 values, widened exactly
to binary64, transformed by glTF 2.0 node transforms using column vectors and
the glTF column-major matrix convention, then multiplied by exactly 1000.0 to
convert package metres to CAD millimetres. For TRS nodes use
`G=T*R*S`, quaternion order `(x,y,z,w)`, and parent-to-child composition
`G_world=G_parent*G_local`. A node may define matrix or TRS, never both.

The assembly JSON occurrence list is ordered. Its 16-number `transform` is
interpreted as four row-major rows acting on a column vector. For component
point `p_mm=[x,y,z,1]^T`, world point is `p_world=M_occurrence*p_mm`.
Triangle order is occurrence order, glTF mesh primitive array order, and index
triplet order. Non-indexed primitives use consecutive vertex triplets. Only
mode 4 TRIANGLES is accepted; another primitive mode is RED.

## 2. Frozen view and projection matrices

Vectors are column vectors. Composition is exactly:

`c = P * V * M_occurrence * p_mm`.

Evaluation is sequential, never by precomposing matrices: first
`p0=M_occurrence*p_mm`, then `p1=V*p0`, then `c=P*p1`. Each output component
uses exactly `(((m0*x + m1*y) + m2*z) + m3*w)` with binary64 rounding after
each multiply and add. When a glTF node hierarchy requires a matrix product,
each result element is evaluated in k order 0,1,2,3 as
`(((a[i,0]*b[0,j] + a[i,1]*b[1,j]) + a[i,2]*b[2,j]) + a[i,3]*b[3,j])`.

The camera uses local +X right, +Y up, +Z backward, and -Z forward. The view
matrix rows are frozen hexadecimal binary64 values:

```text
V = [
 [ 0x1.6a09e667f3bcdp-1,  0x1.6a09e667f3bcdp-1,  0x0.0p+0,              -0x0.0p+0             ],
 [-0x1.6482d37a5a3d2p-2,  0x1.6482d37a5a3d2p-2,  0x1.bda38858f0cc7p-1, 0x1.df79f308a6f80p+1 ],
 [ 0x1.3b1d3d51b89c1p-1, -0x1.3b1d3d51b89c1p-1,  0x1.f82ec882c0f9cp-2,-0x1.556b429bde164p+9 ],
 [ 0x0.0p+0,              0x0.0p+0,              0x0.0p+0,              0x1.0000000000000p+0]
]
```

This is the standard look-at construction with rows `right`, `true_up`, and
`backward`, and translations `-dot(axis,position)`. It encodes camera forward
`[-0.6154574548966637,+0.6154574548966637,-0.4923659639173310]`.

The OpenGL orthographic projection maps camera near/far to NDC -1/+1. Its
frozen matrix is:

```text
P = [
 [0x1.91faecea6cb4ap-8, 0,                       0,                        -0x0.0p+0            ],
 [0,                      0x1.2d7c31afd1877p-7, 0,                        -0x0.0p+0            ],
 [0,                      0,                      -0x1.9848df3ea2d7fp-11, -0x1.000082a6add6ap+0],
 [0,                      0,                       0,                        0x1.0000000000000p+0]
]
```

It derives from left/right `-163.03291470718082/+163.03291470718082`,
bottom/top `-108.68860980478722/+108.68860980478722`, near 0.01, and far
2568.257381947491. Matrix-vector row evaluation is exactly
`(((m0*x + m1*y) + m2*z) + m3*w)`.

## 3. Homogeneous clipping

For clip vertex `c=(x,y,z,w)`, the six signed plane functions and inside
conditions are:

```text
left    d=x+w >=0
right   d=w-x >=0
bottom  d=y+w >=0
top     d=w-y >=0
near    d=z+w >=0
far     d=w-z >=0
```

Clip every triangle with Sutherland-Hodgman in exactly the listed plane order.
Negative zero compares inside. Process each directed polygon edge `S->E` in
stored vertex order:

```text
S in,  E in  -> append E
S in,  E out -> append I
S out, E in  -> append I, then E
S out, E out -> append nothing
```

For a crossing, calculate `den=dS-dE`, `t=dS/den`, then each component as
`I_k = S_k + t*(E_k-S_k)` with the stated rounding/order. A crossing with
`den==0` is RED because opposite inside states cannot then be valid. Snap the
new vertex to the active plane after interpolation: left `x=-w`, right `x=w`,
bottom `y=-w`, top `y=w`, near `z=-w`, far `z=w`, using the just-computed w.
Attributes needed for ID are flat per occurrence and are not interpolated.

After all planes, fewer than three vertices produces no triangles. Otherwise
emit the fan `(v0,vi,vi+1)` for `i=1..n-2` in that order. Divide each emitted
vertex by w in component order x, y, z. `w<=0`, NaN, or infinity is RED.

## 4. Culling, viewport, and quantization

For NDC vertices, compute the y-up signed area:

`a=((x1-x0)*(y2-y0))-((y1-y0)*(x2-x0))`.

Only `a>0` is a CCW front face. `a<=0` is culled; no epsilon is used. The
viewport is W=1800, H=1200. Map NDC to top-left edge coordinates:

```text
sx=(ndc_x+1)*900
sy=(1-ndc_y)*600
```

Quantize each coordinate to signed 24.8 fixed point:

```text
X=round_even(sx*256)
Y=round_even(sy*256)
```

`round_even` means nearest integer, with an exact half choosing the even
integer; there is no epsilon. Compute fixed signed area with unbounded signed
integer arithmetic:

`A=orient(v0,v1,v2)=(X1-X0)*(Y2-Y0)-(Y1-Y0)*(X2-X0)`.

The y flip makes an accepted front face have `A<0`. If `A>=0` after
quantization, discard it. Otherwise swap complete vertices v1/v2, recompute A,
and require `A>0`; this normalization does not change the triangle.

Depth is first mapped as `q=(ndc_z+1)/2`, clamped to `[0,1]`, then each vertex
gets `Z=round_even(q*4294967295)` in unsigned 32-bit range.

## 5. Pineda coverage and top-left rule

All edge and interpolation arithmetic uses unbounded signed integers (a
correct at-least-128-bit implementation is sufficient for this viewport).
For directed edge `a->b` and pixel sample p:

`E(a,b,p)=(Xb-Xa)*(Yp-Ya)-(Yb-Ya)*(Xp-Xa)`.

Pixel `(x,y)` samples exactly at fixed coordinates
`Xp=256*x+128`, `Yp=256*y+128`. Iterate the inclusive pixel box:

```text
xmin=max(0,ceil_div(min(Xi)-128,256))
xmax=min(1799,floor_div(max(Xi)-128,256))
ymin=max(0,ceil_div(min(Yi)-128,256))
ymax=min(1199,floor_div(max(Yi)-128,256))
```

`floor_div` and `ceil_div` are mathematical floor/ceiling for signed integers,
not truncation toward zero.

An edge with `dx=Xb-Xa`, `dy=Yb-Ya` is top-left iff
`dy<0 || (dy==0 && dx>0)`. A pixel passes an edge iff `E>0`, or `E==0` and the
edge is top-left. It is covered iff it passes all three directed edges. This is
the Direct3D-style top-left ownership rule expressed explicitly for the
top-left/y-down viewport and normalized positive A.

For a covered sample compute unbiased integer barycentric numerators:

```text
w0=E(v1,v2,p)
w1=E(v2,v0,p)
w2=E(v0,v1,p)
w0+w1+w2=A
D=w0*Z0+w1*Z1+w2*Z2
Zp=round_div_even(D,A)
```

`round_div_even(n,d)` for nonnegative n and positive d computes quotient q and
remainder r; returns q if `2r<d`, q+1 if `2r>d`, and the even member of
`{q,q+1}` if `2r==d`. The result is clamped to uint32 only as a defensive check;
clamping after valid interpolation is not expected.

## 6. Depth equality, draw order, IDs, and outputs

Each pixel stores uint32 depth, signed triangle serial, uint16 ID, and uint8
coverage. Initial values are depth `0xffffffff`, serial `-1`, ID0, coverage0.
Triangle serial starts at0 and increments for every post-clip fan triangle,
including culled/degenerate triangles, in source order.

A covered fragment wins iff:

`Zp < stored_depth || (Zp == stored_depth && triangle_serial > stored_serial)`.

Thus equal depth is deterministic later-draw-wins, exactly specifying LEQUAL.
On a win set depth, serial, flat occurrence ID, and coverage1. Reference draw
order is all 203 frozen occurrences. Hybrid candidate order is the 131 frozen
protected occurrences followed by candidate IDs1..144 in candidate registry
order. Protected triangles write ID0 and depth/coverage; authorized triangles
write their ID plus depth/coverage.

Acceptance hashes operate on canonical raw arrays, not PNG encoders:

```text
mask/reference_coverage.u8    2160000 bytes, one 0/1 byte per top-left row-major pixel
mask/candidate_coverage.u8    2160000 bytes, one 0/1 byte per top-left row-major pixel
mask/candidate_ids.u16le      4320000 bytes, uint16 little-endian per top-left row-major pixel
mask/authorized_roi.u8        2160000 bytes, one 0/1 byte per top-left row-major pixel
```

No header, row padding, or terminal newline is present. PNGs are derived visual
copies and their hashes are recorded but are not cross-implementation mask
authority. Geometry/exterior/contour XOR uses the coverage arrays. The
authorization ROI starts with exactly those pixels whose final candidate ID is
1..144. Its two-pixel Chebyshev dilation sets output `(x,y)` iff an input pixel
`(u,v)` with value1 exists such that `|u-x|<=2` and `|v-y|<=2`; input and output
coordinates are clipped to `0<=x,u<1800`, `0<=y,v<1200`. Then union the two
fixed-tower rectangles `(370,205,438,380)` and `(1495,390,1522,414)`. For I3.6
these integer `(xmin,ymin,xmax,ymax)` rectangles are explicitly inclusive at
both minima and maxima. Output origin is always top-left; no vertical flip
occurs anywhere in this CPU pipeline.

## 7. Bit-for-bit conformance fixtures

`i3_mask_raster_report.json` must record the implementation source SHA-256,
compiler/interpreter identity, all four canonical-array SHA-256 values,
package/map hashes, triangle counts before/after clipping/culling, equal-depth
win count, and XOR counts. Before model acceptance, two independent
implementations must reproduce byte-identical arrays for these fixtures:

- one CCW triangle with one horizontal top edge;
- two triangles sharing every edge orientation of a rectangle with zero
  double-owned or uncovered interior samples;
- triangles crossing each of the six clip planes;
- a triangle whose vertex lands on a half-fixed-point tie;
- two coincident triangles with IDs 0 and 1 proving later-draw-wins;
- the complete frozen 203 reference package.

Fixture coordinates, expected raw arrays, and their SHA-256 values are stored
in `mask_raster_conformance_fixtures.json`; generation code may not generate
its own expected results during the acceptance run.

## 8. Complete machine/process/filament audit

The acceptance slicer authority is the installed Snapmaker Orca 2.3.5 and the
active configuration snapshot below. Every path is absolute and every digest
is the SHA-256 of the exact file at that path:

```text
application executable
  /Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca
  4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe

application Info.plist
  /Applications/Snapmaker Orca.app/Contents/Info.plist
  5470e7545a9b983901c31fb50dd767333469343a57016b4bff398bc79acfe3fd

active application configuration
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/Snapmaker_Orca.conf
  aca607784e075d4c99e98fdf458acbaa78655ad09f8811328e0d9b5c407aecfe
```

`Info.plist` has bundle identifier `com.snapmaker.snapmaker-orca`, short version
`2.3.5`, and empty bundle-build version. The configuration header is
`Snapmaker Orca 2.3.5`.

### 8.1 Active machine chain

Resolve child over parent in exactly this order; the final file has no parent:

```text
Snapmaker U1 (0.4 nozzle), version 2.2.0.4, inherits fdm_U1
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json
  545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d

fdm_U1, version 2.1.1.1, inherits fdm_toolchanger
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/fdm_U1.json
  ff0724000b1436fcc3d77ffa74bb623a9b322474fc20c8a8d5a26ee164077046

fdm_toolchanger, no version field, inherits fdm_klipper
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/fdm_toolchanger.json
  b2ee2d2c31a26ddee7b0c8bd84c58934d9c01e84e1b8f7ae45e14acfd1f7b52a

fdm_klipper, no version field, no parent
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/machine/fdm_klipper.json
  78dd750211347543368a8a0f136441ef7e23b3a4a09a9e33a370c91dbda273b9
```

The active machine leaf owns the four 0.4 mm nozzle diameters, printable
polygon `[(0.5,1),(270.5,1),(270.5,271),(0.5,271)]`, printable height270.05,
machine start G-code, machine end G-code, pause G-code, and
`change_filament_gcode`. Parent values for those keys are shadowed wherever the
leaf defines them.

The similarly named application-bundle profile is inspected but explicitly
nonactive and may not be substituted:

```text
/Applications/Snapmaker Orca.app/Contents/Resources/profiles/Snapmaker/machine/Snapmaker U1 (0.4 nozzle).json
67047c9fd6d2e935c1e0b84afaf6a674698e326a7785d7c6febd47f3d7d3e765
```

The OTA copies happen to match the active system-copy machine hashes, but only
the exact `system/Snapmaker/machine` paths above are acceptance inputs. Mixing
bundle, OTA, and system copies is RED.

### 8.2 Active process chain

Resolve child over parent in exactly this order; none of these files has a
version field and the final file has no parent:

```text
0.20 Standard @Snapmaker U1 (0.4 nozzle), inherits fdm_process_U1_0.20
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/0.20 Standard @Snapmaker U1 (0.4 nozzle).json
  3342dbe3e995b66ab5700245c676f446a88d35f56498b074ab6fe14039d67763

fdm_process_U1_0.20, inherits fdm_process_U1_common
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/fdm_process_U1_0.20.json
  2df28dc2474b6aeb77d5416043b3a67e54ff7ea1cdf5a5daa9e97db7e5b034a6

fdm_process_U1_common, inherits fdm_process_U1
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/fdm_process_U1_common.json
  43fba9fe359864b265ffa8682cf404c2b935d12164ffe3d0048e5dcb0691db74

fdm_process_U1, no parent
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/fdm_process_U1.json
  66e9e51c4bd04cbbec49fa1a3a043bc3c6e329396c2b38a18db5a66b6e72b4e2
```

The root process owns the inherited brim width5.00. `fdm_process_U1_common`
owns effective skirt loops0, effective prime tower enabled1, and effective
first-layer line width0.50; its value shadows root first-layer line width0.42.
I3.5/I3.6 then apply exact per-plate overrides to each of the six moving-half
plates: brim width3.50, skirt loops0, prime tower disabled, one material, and
one object. Therefore the effective accepted moving-plate values are
3.50/0/false, not the unoverridden 5.00/0/true chain result.

The stale sibling below is explicitly excluded and is neither an ancestor nor
an override:

```text
/Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/process/0.20 Standard @Snapmaker U1 (0.4 nozzle)_old.json
590e629321359cfc9f26eb07dcc632e2392cd6df6125ec3e43163e6d94760d91
```

### 8.3 Active filament chain

The acceptance filament is the existing user PETG profile, resolved child over
parent in exactly this order; the final file has no parent:

```text
PETG, version 2.2.46.2, inherits Generic PETG
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/user/default/filament/PETG.json
  d7a7c0e5911779e70836bf53c29fd736c8702ff45ad46880690c2f092c5433df

Generic PETG, no version field, inherits Generic PETG @base
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/Generic PETG.json
  9887427bf889b4364b49b401aa69a1f874ff484e530a09a54be5e77a0bd5ad9b

Generic PETG @base, no version field, inherits fdm_filament_pet_generic
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/Generic PETG @base.json
  e46b5aac9d983eff69a18f6f2453fc2e5a28f1d581370195ef01c9d0d7032e57

fdm_filament_pet_generic, no version field, inherits fdm_filament_common_generic
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/fdm_filament_pet_generic.json
  33f78fc9a87c83976a635d23c0303797bc9468c8a1c27ab2d1ef769ea66ac2d1

fdm_filament_common_generic, no version field, no parent
  /Users/scottchu/Library/Application Support/Snapmaker_Orca/system/Snapmaker/filament/fdm_filament_common_generic.json
  24e4920907489bfdeb250ba749b005c97571d7a547416989af10df502896e99d
```

The effective filament type is PETG. `Generic PETG` explicitly owns empty
filament start/end G-code strings, so the nonempty ancestor filament scripts
are shadowed and do not execute. The `Snapmaker_Orca.conf` machine entry retains
a saved `Generic TPU` four-tool combination; that saved selection is not the
I3 acceptance filament and is explicitly excluded. No saved Generic TPU
profile, project-embedded filament, backup-user copy, or OTA filament copy may
replace the five exact paths above.

### 8.4 Plate selection, G-code ownership, and resolved-input gate

The acceptance selection is machine `Snapmaker U1 (0.4 nozzle)`, process
`0.20 Standard @Snapmaker U1 (0.4 nozzle)`, four 0.4 mm nozzle positions,
configuration `curr_bed_type` raw value3, and user filament `PETG`. The
six-plate 3MFs must contain only the I3.5 moving-plate overrides above; any
other project/user override is RED. Each slicing report must export and hash
the fully resolved effective configuration so the raw bed-type value and all
override sources are independently checkable.

The effective machine start, end, pause, and change-filament scripts all come
from the active machine leaf file identified by its full path and digest in
Section 8.1. The explicit host-visible startup extrusion remains exactly:

```text
G0 X85 Y1 Z2 F18000
M109 S{nozzle_temperature_initial_layer[initial_extruder]}
G1 Z0.2
M83
G1 X185 E15 F360
G1 Z1.5
```

The effective end script is the leaf `PRINT_END`/`TIMELAPSE_STOP` sequence;
the effective pause command is leaf `M600`; and the effective tool-change
script is the leaf `change_filament_gcode` block dated 20251213. The active
machine start script calls firmware macros including `PRINT_START`,
`DEFECT_DETECTION_START`, `TIMELAPSE_START`, `SM_PRINT_AUTO_FEED`,
`SM_PRINT_FLOW_CALIBRATE`, nozzle-cleaning/discard macros, `DETECT_BED_PLATE`,
and `BED_MESH_CALIBRATE`. Their bodies are device-firmware state, not inherited
host-profile JSON, and remain the explicit I3.5 machine assumption; they are
not CAD clearance or collision proof.

Every acceptance slice must record the exact application/configuration hashes,
all 13 active profile-file hashes, selected plate/nozzle/material, resolved
configuration hash, and generated G-code hash. A missing parent, unresolved
firmware macro reported as host geometry, name-only preset resolution, partial
hash, stale `_old` process, saved TPU substitution, application-bundle machine
substitution, or mixed OTA/system chain is RED.

## 9. Preserved I3.5 contracts

Unless the final audit explicitly supersedes a profile value, I3.5 remains
active for open-slot service behavior, six moving plates with 3.50 brim and
zero skirt/prime tower, separate 203 reference and 275 candidate package/maps,
actual six-part slicing and full first-layer G-code parsing, the exact 22-key
expected/observed press maps, acyclic detached manifest hashing, locked-copy
preservation, 189540 q states, 34 printable bodies, registry
`131+18+126=275`, head clearance >=1.25, M3 wall >=0.60, and frame M2 actual
length/engagement >=3.80/>=1.40.
