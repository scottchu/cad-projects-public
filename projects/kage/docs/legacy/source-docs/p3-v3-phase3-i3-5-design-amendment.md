# KAGE P3 V3 Phase-3 I3.5 — profile-bound implementation closure

Status: **ACCEPTED DESIGN AMENDMENT — no CAD implementation**

Date: **2026-08-19**

Supersedes: `p3-v3-phase3-i3-4-design-amendment.md` wherever this document is
more specific or conflicting.

Immutable predecessors:

```text
I3.1  abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77
I3.2  9998612e8b9d5f6865b714dcd47199cf33afde787840350f261256c404d3bdc3
I3.3  4d29f72ba299ffe35ebbfa92349323681f4a3f6c76ac3a11a74a41462bc62691
I3.4  c6fb12ceab347b258b4f3be65b61d32f178bbf3075cf68869d5d87e9d47636e1
STEP  8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724
```

I3.5 resolves the remaining I3.4 review blockers using the installed
Snapmaker Orca profile evidence. It does not implement CAD or authorize any
change to the functional 300 mm clock, active teeth, R131.60 races, protected
geometry, accepted Z datums, registry classes, or hardware quantities. Earlier
requirements remain active unless explicitly superseded here.

## 1. Open frame/front receiver service contract

Only these two receiver families supersede the I3.1 and I3.4 after-closure
capture rule:

```text
stationary_frame_open_jig_captured_M2
outer_front_ring_open_jig_captured_M2
```

Their I3.3 slot geometry is unchanged: R=`[145.70,150.20]`, D4.20-equivalent
square-nut tangent width 4.20 at t=`+/-5.00`, depth 1.70, inner ligament 1.20,
end ligament 0.90, and hour-fin clearance 0.60.

For these families, product-side nut capture is required **while the screw
remains engaged**. The engaged screw shank through the DIN 562 nut is the
positive radial stop. The quadrant need not close the radial mouth. Controlled
nut removal without quadrant removal is authorized only on the assembly jig:

1. Seat the assembled quadrant/bridge on the jig with both mouth gates closed.
2. Remove one screw while its indexed jig gate remains closed.
3. Open only that indexed gate.
4. Translate the released nut along local +R from centre R=147.80 to R=152.30,
   at fixed tangent and seated Z, until its inner face is 0.10 beyond the
   R=150.20 Boolean mouth.
5. Close the gate before servicing the other receiver or removing the product
   from the jig.

The exact acceptance behaviors are:

- jig absent, screw engaged at its required engagement: the nut's complete
  +R escape sweep is blocked by the stationary screw and no detached state is
  reachable;
- jig present, screw absent, indexed gate closed: the nut escape sweep is
  blocked by the fixture;
- jig present, screw absent, indexed gate open: the R147.80-to-R152.30 nut
  service sweep has IV<=`1e-7 mm3` against all product solids and the nut is
  removable without quadrant removal;
- jig absent and screw absent is an unauthorized/RED assembly state.

`assembly_state_manifest.json` must enumerate all four states and transitions.
Rear-chassis and moving-lap captive receivers are not superseded. A test that
expects the quadrant alone to retain a frame/front nut after screw removal is
stale and must be replaced by this behavior contract.

## 2. Exact moving-half brim override

For the six moving-half plates only, I3.5 explicitly supersedes
`moving_brim_nominal_mm=5.00` with:

```text
moving_brim_nominal_mm = 3.50 per side
moving_plate_count     = 6
moving_bodies_per_plate= 1
skirt_loops            = 0
prime_tower_enabled    = false
```

The value is a per-object override on each moving-half plate. It does not
alter the installed process profile file. Stationary-body brim settings remain
unchanged and must be resolved from their own plate/profile evidence.

The 3.50 value was already accepted as the I3.1 moving fallback maximum; this
amendment promotes it to the six moving plates because the actual U1 profile
must be proved by slicing. CAD acceptance does not prove U1 adhesion. A six-
part physical adhesion/warp trial remains mandatory before production.

The parameter table, effective slicer configuration, 3MF object metadata,
plate manifest, slicing report, and RED suite must all assert exactly 3.50.
Inheriting the profile's base 5.00, applying 3.50 to stationary parts, using a
prime tower, or producing a skirt is RED.

## 3. Reference and candidate render-package identities

I3.4's use of `contentHash` as if it were a GLB byte digest is superseded.
`contentHash` is semantic identity metadata; it is retained but is never used
as proof of GLB file bytes.

### 3.1 Frozen 203-occurrence reference package

The reference render uses only the existing frozen package:

`models/p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention/__cadgen__/models/p3_v3_r1_i1_fixed_tower_retention_assembled.step/assembly.json`

Its assembly JSON SHA-256 remains
`2c25e2ae0db56cd24837c62f01764756752d421f79b2dafe4d36d67d8c907762`.
Its separate byte map is the required artifact
`reference_glb_file_sha256_map.json`.

### 3.2 Generated 275-occurrence candidate package

The candidate render uses only the generated I3 package at:

`__cadgen__/models/assembled_nominal.step/assembly.json`

under the I3 evidence root. It must contain exactly 275 occurrences with
classes `131+18+126`. Its generated assembly JSON SHA-256 is recorded as
`candidate_assembly_json_sha256`; its separate byte map is
`candidate_glb_file_sha256_map.json`. The value is generated evidence, never
copied from the 203 package.

Each GLB map has exact top-level keys `schema_version`, `package_role`,
`assembly_json_relative_path`, `assembly_json_sha256`, and `files`. `files` is
an object sorted by UTF-8 relative path; every key is a package-relative
`components/<name>.glb` path and every value is the SHA-256 of that GLB's
actual bytes. The file set must equal the assembly component-path set exactly:
no missing, extra, absolute, or symlink-resolved paths. Serialization is UTF-8
JSON with sorted keys, two-space indentation, and one terminal LF.

The reference map is recomputed from the frozen package before and after
implementation and must be byte-identical. The candidate map is recomputed
after every package generation and must match candidate bytes. The accepted
203 package is never used as the candidate render package.

### 3.3 Hybrid authorization pass

The reference geometry/color render uses all 203 frozen reference
occurrences. The candidate geometry/color render uses all 275 candidate
occurrences. The authorization-ID pass is deliberately hybrid:

- the 131 protected/reference triangle sets and transforms come from the
  frozen 203 package and write depth plus ID 0;
- the 18 replacement and 126 new triangle sets and transforms come from the
  generated 275 package and write IDs 1..144;
- candidate protected triangles are parity evidence but are not an alternate
  ID-pass source.

This prevents serializer drift in protected candidate meshes from changing
the authorization mask while still rendering every authorized I3 solid from
the real candidate package.

## 4. Deterministic AA-disabled geometry masks

The antialiased color PNGs are visual-review artifacts only. No silhouette,
geometry XOR, exterior flood-fill, or ROI pass/fail value may be derived from
them. All such gates use an AA-disabled software mask pass.

The mask rasterizer is platform-independent and has this exact contract:

1. Decode GLB position accessors as their exact binary32 values and widen to
   IEEE-754 binary64. Apply occurrence, view, and orthographic matrices in
   listed row order with round-to-nearest-ties-to-even and no fused contraction.
2. Clip in homogeneous coordinates in fixed order left, right, bottom, top,
   near, far using Sutherland-Hodgman. Triangulate each clipped polygon as a fan
   from vertex 0 in preserved winding order.
3. Cull clockwise/back-facing triangles in NDC where +y is up; CCW is front.
   Edge lines never participate.
4. Map to the 1800 x1200 viewport, then quantize x/y to signed 24.8 fixed point
   with ties-to-even. Pixel samples are at `(x+0.5,y+0.5)`. Use the top-left
   edge inclusion rule.
5. Quantize depth to unsigned 32-bit over `[0,1]` with ties-to-even. Interpolate
   orthographic depth from fixed vertex depths and use `LEQUAL`. Clear depth is
   `0xffffffff`.
6. Draw in exact registry order. For the hybrid candidate pass, draw the 131
   protected triangles first, then IDs 1..144. Background and protected visible
   surfaces are ID 0. Coverage is a separate one-bit buffer, so protected
   foreground is never confused with background.
7. Store arrays directly in top-left row order: pixel `(0,0)` is top-left, +x
   right, +y down. There is no WebGL `readPixels` flip in this software pass.

`reference_coverage_mask` is the coverage render of all frozen 203 triangles.
`candidate_coverage_mask` is the coverage render of the frozen 131 protected
plus candidate 144 authorized triangles. Geometry XOR, four/eight-connected
exterior XOR, and outer-contour XOR compare those coverage masks. The
authorization mask decodes nonzero IDs from the hybrid candidate ID buffer,
then applies the accepted two-pixel Chebyshev dilation and inherited fixed-
tower ROI union. The color-pass foreground predicate remains documented for
visual diagnostics but has no acceptance authority.

The exact raster contract and implementation SHA-256, both package/map hashes,
coverage/ID PNG hashes, pixel counts, and all XOR counts are recorded in
`i3_mask_raster_report.json`. Browser, GPU, driver, DPR, WebGL AA, and color
tone-mapping differences cannot affect these masks.

## 5. Installed Snapmaker Orca evidence

The moving-plate slicing authority is the installed application and profile
chain below. Paths are evidence-source paths, not files to modify.

```text
application version       Snapmaker Orca 2.3.5
application executable    /Applications/Snapmaker Orca.app/Contents/MacOS/Snapmaker_Orca
executable SHA-256         4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe

machine                    Snapmaker U1 (0.4 nozzle)
machine version            2.2.0.4
machine JSON SHA-256       545e4456b78cc58e701ed257e4024b0ed9e2461cccc1046e6f901ce3c020ee0d
printable polygon          [(0.5,1),(270.5,1),(270.5,271),(0.5,271)]

active process             0.20 Standard @Snapmaker U1 (0.4 nozzle)
active process SHA-256     3342dbe3e995b66ab5700245c676f446a88d35f56498b074ab6fe14039d67763
inherits fdm_process_U1_0.20
  SHA-256                  2df28dc2474b6aeb77d5416043b3a67e54ff7ea1cdf5a5daa9e97db7e5b034a6
inherits fdm_process_U1_common
  SHA-256                  43fba9fe359864b265ffa8682cf404c2b935d12164ffe3d0048e5dcb0691db74
inherits fdm_process_U1
  SHA-256                  66e9e51c4bd04cbbec49fa1a3a043bc3c6e329396c2b38a18db5a66b6e72b4e2
```

The effective moving-plate overrides are brim width3.50, skirt loops0, prime
tower disabled, one material, and one object. Do not edit any system JSON to
obtain them. Export the resolved effective configuration for each plate,
record its SHA-256, and prove the values after inheritance and override.

The machine start G-code and firmware macro sequence remain enabled and
unmodified. Its explicit slicer-visible extrusion line is:

```text
G0 X85 Y1 Z2
G1 Z0.2
M83
G1 X185 E15 F360
```

Thus the explicit startup extrusion centreline is X=`[85,185]` at Y=`1`.
I3.4's invented purge rectangle is deleted. Firmware cleaning, discard,
auto-feed, flow-calibration, and purge macros are not disabled. Their internal
motion is firmware-dependent and is recorded as a machine assumption, not CAD
or host-G-code collision proof.

## 6. Actual slicing and first-layer G-code gate

Slice each of the six actual moving-half 3MF occurrences independently with
the exact application, machine, process chain, and overrides in Section 5.
Synthetic rectangles and nominal AABBs do not satisfy this gate.

For each plate record the source BREP SHA-256, 3MF occurrence/mesh SHA-256,
effective configuration SHA-256, complete generated G-code SHA-256, application
executable SHA-256, all profile-chain hashes, and slicer stdout/stderr log
SHA-256 values.

Parse the complete G-code modal state for G90/G91, M82/M83, active tool,
X/Y/Z/E, and G0/G1/G2/G3. A first-layer extrusion segment is every continuous
XY line or arc with positive deposited extrusion from the explicit startup
line through completion of the first object layer. Arcs are checked as their
continuous circular paths, not endpoints only. Retractions, travels, and
firmware macro internals with no explicit XY path are reported separately.

The exact gates are:

- every parsed extrusion centreline point lies in or on the closed machine
  printable polygon; this polygon is the nozzle-centre domain;
- object/support/brim extrusion paths do not intersect the explicit startup
  line or any other non-object first-layer extrusion path;
- no prime-tower extrusion segment or prime-tower G-code marker exists;
- no skirt extrusion segment exists;
- the measured object brim reaches 3.50 within slicer discretization tolerance
  0.05 and never exceeds 3.55 from the actual first-layer object silhouette;
- every support extrusion remains inside the sliced moving-half/brim envelope;
- all six reports have identical application/profile hashes and zero failed
  predicates.

The reviewed raw worst-axis footprint remains 244.864483. With the 3.50 brim,
the exact reserved width remains:

`244.864483 + 2*3.50 = 251.864483 mm`.

Centre the reserved envelope on the actual printable-polygon centre
`(135.5,136.0)`. Exact bounds and arithmetic are:

```text
raw X                 [13.0677585,257.9322415]
raw Y                 [13.5677585,258.4322415]
brim-reserved X       [ 9.5677585,261.4322415]
brim-reserved Y       [10.0677585,261.9322415]
printable X           [ 0.5000000,270.5000000]
printable Y           [ 1.0000000,271.0000000]
total slack per axis  270-251.864483 = 18.1355170
edge slack            18.135517/2 = 9.0677585
startup-line-to-reserved-Y clearance = 10.0677585-1 = 9.0677585
```

These bounds are planning reservations. The parsed actual G-code paths, not
the reservation alone, are the final containment/no-intersection authority.
Any failed slice, changed profile/app hash, prime tower, skirt, 5.00 moving
brim, omitted startup line, path outside the polygon, or first-layer path
intersection is RED.

## 7. Report and manifest schema closure

I3.4's acyclic detached main-manifest rule remains active. The complete
subsidiary report set is now exactly:

```text
i3_serializer_calibration.json
i3_authorized_roi_report.json
i3_mask_raster_report.json
i3_nut_loading_report.json
i3_q_motion_report.json
i3_contact_whitelist_report.json
i3_fastener_access_report.json
i3_printable_body_manifest.json
i3_render_package_report.json
i3_slicing_report.json
i3_locked_copy_preservation_report.json
```

The primary artifact set adds:

```text
reference_glb_file_sha256_map.json
candidate_glb_file_sha256_map.json
```

and retains `assembled_nominal.step`, `service_exploded.step`,
`print_components.3mf`, `source_import_parity_manifest.json`,
`purchased_hardware_bom.json`, `assembly_state_manifest.json`,
`plate_manifest.json`, the three required PNGs, `i3_validation_manifest.json`,
and its detached `.sha256` file. The main manifest never hashes itself or its
detached checksum internally. `reports` hashes exactly the eleven subsidiary
reports; `artifacts` hashes every primary artifact except the main manifest
and detached checksum.

`i3_render_package_report.json` requires `reference_package`,
`reference_assembly_json_sha256`, `reference_glb_map_sha256`,
`candidate_package`, `candidate_assembly_json_sha256`,
`candidate_glb_map_sha256`, `reference_occurrence_count`,
`candidate_occurrence_count`, `candidate_classification_counts`,
`hybrid_id_sources`, and `violations`.

`i3_slicing_report.json` requires `application`, `machine_profile`,
`process_chain`, `effective_overrides`, `printable_polygon`,
`startup_explicit_extrusions`, `firmware_macro_assumptions`, `plates`,
`first_layer_parser`, `containment_failures`, `intersection_failures`,
`prime_tower_segment_count`, `skirt_segment_count`, and `violations`.

`i3_contact_whitelist_report.json` retains the exact ordered 22-key
`expected_press_iv_by_label_mm3` and `observed_press_iv_by_label_mm3` maps from
I3.4, `1e-7 mm3` comparison tolerance, no wildcard, and no nonwhitelist
positive pair. `i3_locked_copy_preservation_report.json` adds I3.5, both
profile source JSONs plus all inherited profile JSONs, the reference assembly
JSON, every reference GLB from its map, and the I3.5-published hash to its
pre/post byte-identity set.

The main manifest includes the published I3.1 through I3.5 hashes. As before,
the I3.5 hash is the externally published SHA-256 of this immutable file and
is not embedded in itself. Copy preservation takes the I3.5 pre-hash before
implementation source work.

## 8. Preserved numeric gates and RED-suite updates

The RED suite must retain and assert:

```text
registry                         131 protected +18 replacement +126 new =275
printable bodies                 exactly 34
q state transforms              exactly 189540
press maps                       exactly 22 expected +22 observed labels
moving pin                       final3.00/press2.00/gap0.08/slip0.92/recess0.08
moving tool directions           +Z approach, -Z insertion/engagement sweep
adjacent-role head clearance     expected1.27, gate >=1.25
M3 actual minimum wall           >=0.60
frame M2 actual under-head       >=3.80
frame M2 actual engagement       >=1.40
moving brim                      exactly3.50 on exactly6 one-body plates
moving prime towers/skirts       0/0
```

It must also assert the two screw-retained open receiver families and service
states, separate 203-reference/275-candidate packages, assembly/map byte
hashes, frozen-reference/candidate-authorized hybrid sources, software mask
contract, coverage-versus-ID0 distinction, actual app/profile/G-code hashes,
parsed first-layer polygon containment/no intersection, exact report/artifact
sets, acyclic manifest hashing, all five published spec hashes, and locked-copy
preservation. Stale quadrant-only capture, 5.00 moving brim, semantic
`contentHash` used as a byte digest, 203 package used for candidate rendering,
AA color-mask pass/fail, browser-dependent mask output, invented purge
rectangle, disabled firmware cleaning/purge, 136 protected occurrences, 1.35
clearance, or fewer than 189540 states is RED.

Physical adhesion, warp, half flatness, installed TIR, tooth noise/backlash,
receiver wear, joint strength, optical continuity, firmware macro motion, and
full 360-degree running behavior remain physical acceptance gates and are not
proved by CAD, package parity, or G-code parsing.
