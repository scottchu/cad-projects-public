# KAGE P3 V3 Phase-3 I3-R2 — verified-release localized handoff

Status: **IMPLEMENTATION HANDOFF — no CAD implementation; print release remains RED**  
Date: **2026-08-19**  
Successor namespace: `p3_v3_phase3_i3_r2_verified_release`

This handoff is the only authorized successor to the rejected
`p3_v3_phase3_i3_r1_real_joinery` checkpoint. It repairs the remaining joinery,
proof, mesh, freshness, validator, and publication defects without reopening the
locked KAGE architecture. No Hall, balance, optical, transmission, motor,
tower, roller, fin, cosmetic, or unrelated mechanical redesign is authorized.

## 1. Frozen inputs and accepted R1 facts

The implementation must hash and preserve these inputs before constructing any
successor geometry:

- frozen Phase-2A STEP SHA-256
  `8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724`;
- accepted I3 specification SHA-256
  `abbe7129ffe9383950c08a705245c96aa756930b19d5dc0af8eb6fa4401cdf77`;
- I3.12 amendment SHA-256
  `e482b6f14e03d23080d5011b424efcaf0be280ea39ee9df5a93559ca0659a713`;
- R1 repair handoff SHA-256
  `7b20b2fff600623a1fceab4ec66717d6b5bcc3257d4d32653b26a72d35b704f4`.

The following R1 facts were independently remeasured and remain frozen:

| Fact | Frozen value |
|---|---:|
| logical occurrence registry | `275` |
| `protected_exact` occurrences | `131` |
| authorized replacements | `18` |
| new authorized occurrences | `126` |
| nominal imported STEP occurrences | `275` |
| exploded imported STEP occurrences | `275` |
| imported STEP topology failures | `0` in each STEP |
| nominal bounds | `[-150,-150,-32.5]..[150,150,24.2514] mm` |
| exploded bounds | `[-150,-150,-32.5]..[150,150,78.8] mm` |
| disassembled printable objects | `34` |
| moving Orca source objects / plates | `6 / 6` |
| protected import drift | none |

The exact six-plate Orca object names, UUIDs, plate mapping, extruder `1`,
filament slot `1`, filament identifier `GFG00`, physical tool `T0`, U1
four-nozzle mapping, bed definition, profile chains, `3.50 mm` moving brim,
zero skirt, and disabled prime tower are frozen. Their current accepted mapping
may be copied but not silently regenerated with new identities.

These accepted facts do not approve the R1 implementation or its artifacts.
R1 remains rejected and may only be read as an input/reference.

## 2. Remaining R1 rejection and localized repair scope

R2 must repair all of the following:

1. `receive_xy_clearance_mm=0.10` and `butt_face_relief_mm=0.025` exist in the
   R1 owner object but do not drive its geometry.
2. The R1 parameter test mutates no parameter, measures no changed BREP, and
   returns prefilled empty issue arrays.
3. The R1 motion proof models only twelve moving lap-addition BREPs against six
   station solids rather than all moving participants. Its
   `audit_missing_candidate_pairs += 0` and global-set equality are not
   completeness proofs.
4. Teeth/phase, race sampling/TIR, loading and nut capture, slip clearance,
   hour-fin clearance, and protected raster/contour gates are absent from the
   sixteen R1 tests.
5. R1 mesh export is not proven manifold/oriented by either fresh lib3mf import
   or an independent indexed-edge audit.
6. R1 freshness omits transitive geometry-driving dependencies and its negative
   archive fixtures do not mutate archive bytes before invoking the production
   validator.
7. R1 performs only one complete STEP run and publishes mutable root-level
   files; it does not provide an old-or-new atomic release set.

The only authorized geometry change is the real Half-B receiving clearance and
the real exterior butt-face relief described below. All other repair work is
validation, deterministic meshing, artifact construction, freshness closure,
or release publication.

## 3. Real moving seam geometry

Retain the R1 numeric joinery contract:

| Variable | Value |
|---|---:|
| radial join band | `R133.50..140.00 mm` |
| tangential overlap | `-8.00..+8.00 mm` |
| Half-A lower male lap | `2.00 mm` |
| Half-B upper lap | `1.00 mm` |
| Half-B-only XY receiving clearance | `0.10 mm/side` |
| open axial fit interval | `0.08 mm` |
| butt relief outside overlap | `0.025 mm/face` |
| screw axes | `R136.75`, tangent `+/-5.00 mm` |
| M2 clearance bore | `D2.20 mm` |
| nut pocket | `4.20 x4.20 x1.70 mm` |
| rear/bed pocket skin | `0.30 mm` |
| registration pin | `D3.00 x3.00 mm` |
| Half-A press bore | `D2.95 mm` |
| Half-B slip bore | `D3.10 mm` |

| Role | carrier Z | Half-A lap Z | Half-B lap Z |
|---|---:|---:|---:|
| hour | `-1.50..1.50` | `-1.50..0.50` | `0.58..1.58` |
| minute | `4.05..7.05` | `4.05..6.05` | `6.13..7.13` |
| second | `9.60..12.60` | `9.60..11.60` | `11.68..12.68` |

Construction requirements:

- Half A owns the unshrunk lower male envelope.
- Construct a separate receiving-cavity tool from that male envelope, expanded
  in local radial and tangential XY by exactly `0.10 mm` on each side. Subtract
  it from Half B only. The seam ROI is a scope mask, not a replacement solid.
- Outside the overlap band, offset each opposed butt face by exactly
  `0.025 mm`, producing `0.050 mm` total open butt gap. Do not apply either
  relief to a lap boundary and do not apply it twice.
- Retain the `0.08 mm` open axial lap interval after all Booleans.
- Actual-BREP witnesses must measure both XY clearances on all six seams,
  exterior butt gap on both sides of all six seams, and axial interval. A label,
  owner value, tool AABB, or nominal equation is not evidence.
- Preserve all R1 screw, nut, press/slip bore, bridge, and hardware dimensions
  that already satisfy the accepted contract.

## 4. Stationary joinery retained

| Family | bridge | hardware / dowel |
|---|---|---|
| rear chassis | two per seam at `R85/R120`; `12R x18T x4Z mm` | M3x5, D3.40 clearance, `5.70 x5.70 x2.00` nut, D4x6, D3.95 press / D4.10 slip |
| stationary frame | one per seam at `R144.50..150.00`; `16T x3Z mm` | M2x4, D2.20 clearance, `4.20 x4.20 x1.70` nut, D3x5, D2.95 press / D3.10 slip |
| outer front ring | one per seam at `R144.50..150.00`; `16T x3Z mm` | M2x3, D2.20 clearance, `4.20 x4.20 x1.70` nut, D2x4, D1.95 press / D2.10 slip |

Totals remain exactly `16` printed bridges, `44` screws, `44` DIN 562 nuts,
and `22` pins/dowels. The hour-fin clearance to every frame/front bridge remains
at least `0.60 mm`.

## 5. Parameter ownership and perturbation probes

Use immutable owner groups passed explicitly through geometry, validation,
meshing, export, and release code. No geometry or artifact function may read a
parallel module literal after receiving an owner object.

At minimum retain these owners:

- `segmentation`;
- `moving_joinery`;
- `chassis_joinery`;
- `frame_joinery`;
- `front_ring_joinery`;
- `motion_validation`;
- `print_transform`;
- `mesh_contract`;
- `orca_contract`;
- `freshness_contract`;
- `release_contract`;
- `artifact_contract`.

For every adjustable field, construct a fresh owner with one changed field and
rebuild in a fresh process. Use these probe deltas unless the field has a more
restrictive domain:

| Field type | Probe delta |
|---|---:|
| linear dimension / diameter / clearance | `+0.10 mm` |
| angle | `+0.25 deg` |
| integer sample/count field | `+1` |
| Boolean | logical inverse |

Every probe must satisfy all of the following:

1. the intended named actual-BREP or transform witness changes;
2. its BREP/semantic digest changes;
3. a linear witness changes by at least `1e-4 mm` or a volume witness by at
   least `1e-5 mm3`;
4. every `protected_exact` occurrence retains transform, topology, AABB, area,
   volume, and BREP digest;
5. no non-owned witness changes.

Fields declared frozen must reject in-place mutation. AST analysis must map each
adjustable field to at least one real consumer and reject geometry-driving
numeric literals that duplicate an owner field. Empty issue arrays and
field-presence checks are explicitly RED.

Mandatory focused probes include the Half-B `0.10 mm/side` receiving clearance
and `0.025 mm/face` relief. Each must independently move only its intended
actual-BREP witness.

## 6. Complete motion ownership model

The motion proof uses all `275` logical occurrences, partitioned exactly once:

| Owner | Per owner | Owners | Total |
|---|---:|---:|---:|
| rotating ring: two halves + ten moving seam hardware bodies | `12` | `3` | `36` |
| motor station: yoke + twelve clamp hardware + eleven rigid-station bodies | `24` | `3` | `72` |
| tower T1 / T2 | `18` | `2` | `36` |
| tower T3 | `17` | `1` | `17` |
| fixed pool: six front posts + twelve quadrants + sixteen bridges + eighty stationary hardware | `114` | `1` | `114` |
| total |  |  | `275` |

The eleven rigid station bodies are motor, motor shaft, two miter gears, output
shaft, two MR84 bearings, spacer, pinion, and two collars. T1/T2 each contain
their seventeen original occurrences plus the I1 washer.

No occurrence may be omitted, duplicated, or placed in two owners. Internal
pairs inside one rigid owner are not unintended-collision pairs; their assembly
contacts are validated separately. Every cross-owner occurrence pair whose
relative transform changes is in the collision universe, including the target
rotating group against the fixed pool and both non-target ring groups.

## 7. State grid and exact transforms

For target role `R in {hour,minute,second}`:

```text
phi_R = j * (360/260) + delta
j     = 0..259
delta = {-0.05, 0.00, +0.05} degrees
q_H, q_M, q_S = {-0.35, 0.00, +0.10} mm
q_T3          = {-0.25, 0.00, +0.25} mm
```

- The target rotating owner receives `Rz(phi_R)` about the frozen clock origin.
- The two non-target rotating owners remain at their nominal zero transform.
- Motor owners translate radially by their own `q` at station angles
  `0/120/240 deg` for hour/minute/second.
- T3 translates radially by `q_T3` at `300 deg`.
- T1, T2, and the fixed pool remain stationary.

The exact state count remains:

```text
3 target roles * 260 teeth * 3 delta values * 3^4 q combinations
= 189,540 states
```

This count is compatible with, and does not excuse, the expanded participant
set. A state containing only lap additions and six stations is incomplete.

## 8. Broadphase, narrowphase, and per-state evidence

For every occurrence store canonical source BREP digest and local actual-solid
AABB. Apply the exact owner transform to all eight AABB corners. Use an
inclusive-tolerance hierarchical owner AABB followed by an occurrence BVH.

Every overlapping occurrence pair receives this canonical signature:

```text
ordered occurrence IDs
+ both source BREP SHA-256 digests
+ exact relative 4x4 float64 transform SHA-256 digest
+ relationship class
```

Every unique signature reaches actual-BREP intersection. Cache only by that
complete identity. Gear mesh and race contact are not positive-volume
whitelists; they remain `IV <=1e-7 mm3` and also receive dedicated
distance/contact checks. Thread and slip pairs require zero material IV. The
only permitted positive-volume intersections are the exactly `22` named press
pairs, measured by their dedicated press-fit gate.

Each of the `189,540` state records must include:

- stable state ID and all owner transform digests;
- sorted candidate signature IDs;
- sorted evaluated-result IDs;
- maximum non-whitelisted actual IV;
- an explicit empty list when the state has no candidates.

For every state assert `candidate IDs subset-of evaluated-result IDs`; global
set equality is insufficient. Deleting any state candidate or bypassing one BREP
evaluation must fail the affected state.

Measure and publish candidate references, unique signatures, BREP calls, cache
hits, and peak memory. Configure an explicit implementation cap for unique OCC
calls based on the first bounded run; exceeding it fails with counts and may not
silently prune. The cap is a runtime guard, never acceptance evidence.

## 9. Mandatory full-scan broadphase audit

Audit exactly `2,187` complete states:

```text
3 target roles
* tooth indices {0,130,259}
* 3 delta values
* 81 q combinations
= 2,187
```

At each audit state enumerate every cross-owner pair without owner/BVH pruning.
An AABB-disjoint pair needs an explicit separating-axis certificate. Every
AABB-overlap pair receives actual-BREP intersection. Compare the full-scan
candidate set with production broadphase and require exactly zero missed pairs.

A separate seam-focused audit may add the tooth nearest each seam angle and its
`+/-1` neighbors. It does not replace or alter the mandated `2,187` count.
Initializing a missing-pair counter to zero or executing `+=0` is RED.

## 10. Dedicated mechanical gates

All measurements use actual source or imported solids:

| Gate | Acceptance |
|---|---:|
| moving reconstruction XOR outside seam ROI | `<=1e-7 mm3` |
| stationary reconstruction XOR outside seam ROI | `<=1e-7 mm3` |
| moving teeth | `130/half`, `260/ring` |
| seam-adjacent flank tangential phase error | `<=0.10 mm` |
| race radial probes | `4/tooth =1040/ring` minimum |
| CAD race TIR, `max(radius)-min(radius)` | `<=0.02 mm` |
| non-whitelisted actual intersection | `<=1e-7 mm3` |
| motion states | exactly `189,540` complete states |
| broadphase full-scan audit | `2,187` states, `0` misses |
| driver/loading swept obstruction | `<=1e-7 mm3` |
| slip-side positive material IV | `0 mm3` |
| slip diametral clearance | `<=0.12 mm` |
| hour-fin to every frame/front bridge | `>=0.60 mm` |
| transformed moving-half raw X/Y span | each `<=244.864483 mm` |
| moving brim | exactly `3.50 mm/side` |
| packed moving envelope | inside `[5,265]^2` |
| plate-occurrence positive overlap | `<=1e-7 mm3` |
| protected exterior-mask XOR, 4-connectivity | `0` |
| protected exterior-mask XOR, 8-connectivity | `0` |
| foreground XOR outside authorized ROI | `0` |
| global outer-contour XOR | `0` |
| source/import protected drift | none |

Gear/race ownership is exact: each role may contact only its own pinion and its
own three lands. A foreign pinion or roller is never accepted. Measure seam
phase from actual seam-adjacent flank datums. Sample gear mesh at every role,
tooth, delta, and own-motor-q combination using actual IV plus tooth distance
and backlash witnesses.

Driver/loading checks sweep actual tool and fastener solids through the complete
specified insertion path. Nut capture requires throat-versus-nut measurement
and swept escape tests in every open direction after closure; a statement that
the nut is captured is not evidence.

Exactly `22` named press pairs must match:

| Pair | Expected press IV |
|---|---:|
| moving D3 / D2.95 | `0.4673119072 mm3` each |
| chassis D4 / D3.95 | `1.2487830798 mm3` each |
| frame D3 / D2.95 | `0.6075054794 mm3` each |
| front D2 / D1.95 | `0.4653484118 mm3` each |

## 11. Required mechanical mutation negatives

Each fixture changes actual temporary source geometry/evidence and invokes the
same production validator. Require stable named rejection codes for:

- omitted participant;
- pinion, race, or fin shifted beyond its accepted tolerance;
- one bypassed BREP evaluation;
- one deleted candidate signature;
- seam phase error `0.11 mm`;
- race TIR `0.021 mm`;
- slip clearance `0.13 mm`;
- hour-fin clearance `0.59 mm`.

No fixture may mutate only a returned dictionary.

## 12. Print transforms and package obligations

Retain exact moving-half transform precedence:

```text
rotate source +30.000 degrees about global +Z
measure rotated actual-solid AABB including fin and real joinery
translate Z by -bbox_min_Z
translate rotated AABB center to (135.00,135.00)
raw X and Y span each <=244.864483 mm
moving brim exactly 3.50 mm/side
reserved packed square 251.864483 x251.864483 mm
usable bed [5.00,265.00]^2
moving bodies / plates = 1 / 6
```

Store exact float64 `T_print_from_source` and its inverse for each object.

Two separate packages remain mandatory:

1. `print_components.3mf`: exactly `34` printable objects and build items =
   twelve stationary quadrants + six moving halves + sixteen bridges; no
   purchased hardware.
2. `i3_8_six_moving_halves_source.3mf`: exactly six real Orca plate records and
   six named build objects with the frozen identities and U1 settings.

## 13. Deterministic manifold mesh contract

For each source object:

1. tessellate every source solid;
2. spatially weld vertices at exactly `1e-6 mm` using deterministic
   representative selection and index ordering;
3. reject, rather than silently heal, nontrivial duplicate or degenerate
   triangles;
4. preserve source solid/component count, name, UUID, and build registry.

Fresh lib3mf import must report `IsManifoldAndOriented=true` for every one of the
`34 + 6` objects. An independent indexed-edge audit must also prove:

- every index is in range;
- every triangle has positive nonzero area;
- every undirected edge has incidence exactly `2`;
- the two incidents traverse the edge in opposite orientations exactly once;
- connected component count equals source solid count;
- imported AABB and volume match the recorded source tolerances;
- source name, UUID, object ID, and build mapping are exact.

Record per-object vertex, triangle, component, edge, AABB, volume, source-solid,
name, UUID, and registry facts. Passing only one of lib3mf or the independent
edge audit is RED.

## 14. Production Orca archive validator

Implement one production `validate_orca_archive` path and use it for normal
builds and every negative fixture. Cross-validate:

- lib3mf model resources and build resources;
- `Metadata/model_settings.config` objects and plates;
- `Metadata/model_settings.json`;
- `Metadata/plate_data.json`;
- `Metadata/project_settings.config` and all profile paths/hashes;
- UUID, name, object, instance, identify, and plate IDs;
- extruder, filament slot/identifier, and physical tool;
- canonical relationships and content types;
- accepted member grammar with no unknown or missing member.

Temporary archive negatives must modify real ZIP member bytes, rebuild the
temporary archive, and call the production validator. Require stable rejection
codes for at least:

- `plate_data` plate index `999`;
- XML `plater_id=999`;
- object name mismatch;
- object UUID mismatch;
- extruder mismatch;
- profile path mismatch;
- profile hash mismatch;
- duplicate object/instance/identify/plate ID;
- model-resource/build-resource mismatch;
- unknown member;
- missing member.

In-memory dictionary mutations that bypass the validator are RED.

## 15. Complete freshness closure

Build the freshness graph by AST-resolving direct and transitive local imports
from every R2 entry module. Fail closed on unresolved local imports, dynamic
imports, or generated local dependencies unless they are explicitly resolved
and hashed.

The signed input closure includes:

- every R2 source and test entry plus all direct/transitive local modules,
  including the five previously omitted locked R1/I1 geometry, parity, and spec
  dependencies;
- accepted specification, I3.2-I3.12 amendments, R1 handoff, and this handoff;
- frozen STEP;
- all thirteen resolved profile-chain files: four filament system files plus
  user PETG, four machine files, and four process files;
- `pyproject.toml` and `uv.lock`;
- pinned RFC8785 JCS implementation;
- `node`, `xmllint`, lib3mf, Python, build123d/OCC, and runtime dependency
  identity/version evidence.

An omitted-leaf fixture must mutate a temporary copy of a transitive dependency
and change the freshness signature. Deletion, hash mismatch, or unresolved
dependency must fail before reading any existing artifact.

## 16. Two complete isolated builds and semantic parity

Perform exactly two complete builds in separate fresh directories. Each run
must independently regenerate and fresh-process import:

- nominal STEP;
- service-exploded STEP;
- 34-object disassembled 3MF;
- six-plate Orca source 3MF;
- I3.12 v3 canonical projection;
- STEP parity report;
- mesh/manifold report;
- motion and mechanical evidence;
- freshness manifest;
- release semantic manifest.

For each STEP run require `275` unique labels, valid positive topology, exact
bounds, `131` protected occurrences with no drift, and complete replacement/new
registry facts. Compare run 1 and run 2 using the complete RFC8785-JCS semantic
release manifests and require equality. Compare source/import occurrence facts
and STEP semantic projections per run. Raw STEP hashes remain detached
provenance; raw-byte equality is not canonical STEP equality.

The published report must state `complete_build_count=2`. Comparing only a
package subset or rerunning only 3MF generation is RED.

## 17. Content-addressed atomic release set

Do not publish mutable root-level artifact copies. Publish this complete set:

```text
models/p3_v3_phase3_i3_r2_verified_release/
  releases/<content-id>/
    assembled_nominal.step
    service_exploded.step
    print_components.3mf
    i3_8_six_moving_halves_source.3mf
    i3_12_parity_projection.jcs.json
    step_parity_report.json
    manifold_report.json
    motion_validation_report.json
    freshness_manifest.jcs.json
    release_manifest.jcs.json
  current -> releases/<content-id>
```

Define `<content-id>` as SHA-256 of the RFC8785-JCS release semantic manifest
payload before inserting the detached content ID. A release directory is
immutable after publication.

Publication order on one filesystem:

1. build under `.staging-<uuid>`;
2. validate every payload and cross-hash;
3. `fsync` every payload, manifest, and staging directory;
4. rename staging to a previously absent `releases/<content-id>`;
5. `fsync` the releases directory;
6. create a replacement symlink and use `os.replace` to atomically replace
   `current`;
7. `fsync` the parent directory.

Use `F_FULLFSYNC` where available, while reporting durability as best-effort.
macOS same-filesystem rename and pointer replacement provide atomic visibility
for each operation; they do not provide a multi-file atomic replace or certified
power-loss durability.

Consumers must call `readlink(current)` once, validate/pin that content ID, and
read every file through the pinned directory. They may not resolve `current`
separately for each file.

SIGKILL and exception failpoints before/after staging fsync, release rename, and
pointer replacement must prove that `current` resolves to either the complete
old release or the complete new release, never a mixture. An orphan complete
release before pointer switch is allowed and must not become current implicitly.

## 18. Required R2 test coverage

The R2 suite must contain direct tests for every numbered section above and every
acceptance row. At minimum it must separately cover:

1. frozen hashes and accepted R1 facts;
2. actual Half-B XY receiving clearance;
3. actual butt relief and lap axial interval;
4. moving/stationary joinery and exact press/slip intersections;
5. one real perturbation probe for every adjustable owner field;
6. exact 275-occurrence owner partition;
7. all 189,540 complete states with per-state evidence;
8. 2,187-state unpruned audit with zero misses;
9. teeth, seam phase, race samples/TIR, own/foreign drive checks;
10. loading, nut capture, slip clearance, and hour-fin clearance;
11. all mechanical mutation negatives;
12. exact +30-degree bed transforms and six plates;
13. 34-object and six-plate package contents;
14. lib3mf and independent manifold/orientation audits;
15. production Orca validator and all archive byte-mutation negatives;
16. complete transitive freshness closure and omitted-leaf negative;
17. two complete isolated builds and semantic equality;
18. protected/import parity and protected raster/contour XOR;
19. content-addressed atomic publication and all failpoints;
20. isolated successor namespace with no stale R1 artifact fallback.

No test may satisfy these gates with a prefilled count, zero, Boolean, empty
array, label, tool envelope, clamped result, or mutated report dictionary.

## 19. Contradiction audit and boundary

No true specification contradiction was found:

- the exact `189,540` state grid is unchanged; R2 expands participants and
  evidence within each state;
- the accepted R1 six-plate mapping is compatible with deterministic manifold
  remeshing because identities and semantic mappings remain fixed;
- preserving accepted R1 geometry is compatible with adding the two explicitly
  missing, previously required Half-B clearance and butt-relief Booleans;
- the specialist's suggested artifact sub-namespace is resolved by the parent
  requirement: all modules and artifacts live under the exact successor
  namespace `p3_v3_phase3_i3_r2_verified_release`.

Passing R2 proves source-level CAD, imported STEP, source-3MF, motion-proof, and
atomic artifact-publication acceptance only. Sliced G-code, first-layer/profile
execution, printed coupons, fit, warp, TIR, wear, strength, motion, noise,
thermal, electrical, optical, and long-duration performance remain
RED/PENDING physical work.
