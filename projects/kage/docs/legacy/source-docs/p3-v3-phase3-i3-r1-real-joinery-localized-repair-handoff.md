# KAGE P3 V3 Phase-3 I3-R1 — real joinery localized repair handoff

Status: **IMPLEMENTATION HANDOFF — no CAD implementation; print release remains RED**  
Date: **2026-08-19**  
Successor namespace: `p3_v3_phase3_i3_r1_real_joinery`

This handoff repairs the rejected I3 implementation locally. It does not reopen
the clock architecture and does not authorize changes to the frozen baseline,
transmission, towers, motors, rollers, fins, optical envelope, or any protected
occurrence. Existing immutable I3 and I3.1-I3.12 documents remain authoritative.

## 1. Frozen inputs and permitted scope

- Preserve the frozen Phase-2A STEP SHA-256
  `8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724`.
- Preserve the I3.12 document SHA-256
  `e482b6f14e03d23080d5011b424efcaf0be280ea39ee9df5a93559ca0659a713`.
- Preserve exactly `131 protected_exact` occurrences and the frozen global
  assembled bounds `[-150,-150,-32.5]` to `[150,150,24.2514]` mm.
- The only authorized changes are real segmentation/joinery solids, associated
  hardware reference solids, actual print transforms, source-owned artifacts,
  and validation that measures those outputs.
- No Hall, balance, cosmetic, optical, transmission, or unrelated mechanical
  feature may enter this successor namespace.

## 2. Consolidated reviewer rejection evidence

Both final reviews reject the current implementation at CAD level despite the
reported `37/37` test pass and topologically valid STEP exports.

1. Moving geometry only intersects frozen rings with half-space masks. It does
   not add the required laps or subtract real screw bores, nut pockets, dowel
   bores, receiving clearance, or seam relief.
2. A direct BREP audit found positive intersection in all `30/30` moving
   screw/nut/dowel placements; maximum unintended IV was
   `25.165796 mm3`.
3. Stationary bridges are uncut boxes with hardware overlaid. A direct BREP
   audit found `48` positive stationary screw/dowel intersections; maximum
   unintended IV was `31.415927 mm3`.
4. The implemented front-ring bridge is `2.00 mm` thick with a D3 dowel; the
   frozen contract requires `3.00 mm` and D2.
5. Collision, loading, tooth, runout, motion, protected-parity, and raster-XOR
   results are returned as literal dictionaries or empty lists rather than
   calculated from actual solids. Segment reconstruction clamps the reported
   error instead of measuring Boolean XOR outside the seam ROI.
6. The unrotated moving-half AABB is approximately
   `272.921214 x175.390055 mm`, but the plate manifest substitutes a hardcoded
   square and reports containment without applying the required print transform.
7. The current `print_components.3mf` has only six mesh/build objects and omits
   the twelve stationary quadrants and sixteen printable bridges while another
   manifest claims `34` printable bodies.
8. The current parity projection uses obsolete I3.10 schema/fields and hashes
   raw member bytes while labelling them RFC8785 JCS or C14N1.1 results.
   Relationship and content-type projections do not satisfy I3.11/I3.12.
9. STEP export is skipped when a destination already exists, permitting stale
   exports to pass. Protected source/import parity is not recomputed.
10. Geometry-driving numbers remain embedded literals; the existing parameter
    test proves field presence, not that each parameter owns and changes the
    intended solid.
11. The current archive is one ordinary 3MF build containing six objects, not
    six real Orca plates. Custom KAGE JSON/XML does not establish Orca plate
    semantics. Its filament identifier is `kage-i3-petg-t0` instead of frozen
    `GFG00`, and the required machine/process/filament paths and hashes,
    four-nozzle mapping, bed, exact brim, zero-skirt, and disabled-prime-tower
    settings are absent. Its custom model-settings XML plus generic
    `application/octet-stream` `.config` declaration violate the grammar and
    resolved content-type contract.
12. Freshness signatures omit export/parity sources, frozen documents, and the
    frozen STEP. Deleting a signature allows the implementation to re-sign the
    existing stale archive; it does not force source regeneration.
13. The direct moving intersections include screw `9.4248 mm3`, nut up to
    `25.1658 mm3`, and dowel `21.2058 mm3`; stationary unintended IV reaches
    `31.4159 mm3`.
14. Imported nominal STEP bounds reach `maxY=150.253499 mm`, contradicting the
    hardcoded `150.000000 mm` protected-envelope claim. Imported bounds, not a
    returned constant, govern parity.

Topology validation alone remains useful but non-dispositive: both nominal and
service STEP files imported as closed/positive-volume topology with `299`
viewer occurrences and zero topology failures. That result does not prove the
required logical `275`-occurrence registry, joinery, collision freedom, or
source/export parity.

## 3. Real moving joinery

There are six moving seams, two for each of hour, minute, and second.

| Variable | Required value |
|---|---:|
| join radial band | `R133.50..140.00 mm` |
| tangential overlap | `-8.00..+8.00 mm` |
| Half A lower male lap | `2.00 mm` |
| Half B upper receiving lap | `1.00 mm` |
| Half-B-only XY receiving clearance | `0.10 mm/side` |
| open axial fit interval | `0.08 mm` |
| butt-face relief outside overlap | `0.025 mm/face` |
| screw axes | `R136.75, tangent +/-5.00 mm` |
| upper-lap clearance bore | `D2.20 mm` |
| lower-lap nut pocket | `4.20 x4.20 x1.70 mm` |
| rear/bed pocket skin | `0.30 mm` |
| centered registration pin | `D3.00 x3.00 mm` |
| Half A press bore | `D2.95 mm` |
| Half B slip bore | `D3.10 mm` |

Half A owns the unshrunk male envelope and both lower laps. Half B alone owns
receiving relief and both upper laps. Do not double-apply the `0.025 mm`
butt-face relief to a lap boundary.

| Role | Carrier Z | Half A lap Z | Half B lap Z |
|---|---:|---:|---:|
| hour | `-1.50..1.50` | `-1.50..0.50` | `0.58..1.58` |
| minute | `4.05..7.05` | `4.05..6.05` | `6.13..7.13` |
| second | `9.60..12.60` | `9.60..11.60` | `11.68..12.68` |

Each seam owns two ISO 7380-1 M2x3 screws, two DIN 562 M2 nuts with measured
height at most `1.60 mm`, and one D3x3 pin. Hardware solids are purchased
reference/validation bodies. They never substitute for Boolean cuts.

## 4. Real stationary joinery

| Family | Printed bridge | Screw and clearance | Nut pocket | Dowel pair |
|---|---|---|---|---|
| rear chassis | two per seam at R85/R120; `12R x18T x4Z mm` | M3x5; `D3.40` chassis clearance | `5.70 x5.70 x2.00 mm` | D4x6; `D3.95` press / `D4.10` slip |
| stationary frame | one per seam; `R144.50..150.00`, `16T x3Z mm` | M2x4; `D2.20` clearance | `4.20 x4.20 x1.70 mm` | D3x5; `D2.95` press / `D3.10` slip |
| outer front ring | one per seam; `R144.50..150.00`, `16T x3Z mm` | M2x3; `D2.20` clearance | `4.20 x4.20 x1.70 mm` | D2x4; `D1.95` press / `D2.10` slip |

Frozen totals are exactly `16` printed bridges, `44` screws, `44` DIN 562
nuts, and `22` pins/dowels. The hour-fin radial clearance to every frame/front
bridge must remain at least `0.60 mm`.

## 5. Assembly and service order

1. Qualify pocket, seam-gap, and each press/slip dowel coupon.
2. Load bridge or Half-A nuts through their open +Z loading mouths.
3. Press each pin into its designated press member.
4. Lower the closing quadrant or Half B in +Z; it closes the nut mouth.
5. Seat remaining dowels and tighten screws crosswise.
6. Validate every complete moving ring for tooth phase, seam step/gap, and TIR
   before it enters the stack.
7. Install rear-to-front: hour, minute, second, then the outer optical ring.
8. Service in exact reverse order. In-stack nut loading, dowel pressing,
   drilling, or seam tightening is forbidden.

## 6. Parameter ownership

Create immutable, named owner groups and pass them explicitly to every geometry,
export, and validation function:

- `segmentation`: source indices, `260` teeth, seam angles, sector ownership;
- `moving_joinery`: all values in Section 3 and role Z intervals;
- `chassis_joinery`, `frame_joinery`, `front_ring_joinery`: all dimensions,
  axes, hardware, and engagement values in Section 4;
- `print_transform`: rotation, bed center, raw envelope, brim, and all slicer
  envelopes;
- `artifact_contract`: registry/class counts, labels, UUIDs, schemas,
  canonicalizers, and accepted member grammar.

Remove geometry-driving literals including radii, tangential offsets, bridge
sizes, nut dimensions, bores, Z spans, and hardware lengths from modeling code.
Every adjustable parameter needs a probe test proving the intended measured
BREP or transform changes while protected geometry does not. Every frozen field
must reject mutation. Field-presence tests alone are RED.

## 7. Authoritative U1 placement and precedence

There is no packing infeasibility and no reason to segment further.

I3.5 explicitly supersedes the earlier I3.1 `5.00 mm` moving-half brim. The
authoritative moving-half rule is:

```text
rotation                         +30.000 degrees about source global +Z
raw actual-solid X span          <=244.864483 mm
raw actual-solid Y span          <=244.864483 mm
moving brim                      exactly 3.50 mm per side
reserved packed square           251.864483 x251.864483 mm
usable U1 square                 [5.00,265.00]^2 =260 x260 mm
packed total-axis slack          8.135517 mm
moving plate count               exactly 6
moving bodies per moving plate   exactly 1
skirt loops                      0
prime tower                      disabled
```

Transform order is exact:

1. rotate `+30.000 degrees` through the source clock origin;
2. measure the rotated actual-solid AABB including fin and real joinery;
3. translate Z by `-bbox_min_Z`;
4. translate the rotated AABB center to `(135.00,135.00)`.

The rejected incomplete geometry measured approximately
`236.721 x237.512 mm` after the required rotation, confirming feasibility.
Acceptance uses the frozen `244.864483 mm` maximum and full
`251.864483 mm` reserved packed square. Store the exact 4x4
`T_print_from_source` and inverse `T_source_from_print`; never substitute a
constant for a measured transformed AABB.

The old `5.00 mm` value remains applicable only where a later amendment did not
override it. It is not valid for the six moving-half plates. Stationary-part
brims remain resolved from their own plate/profile evidence.

## 8. Two distinct 3MF obligations

Do not conflate these artifacts.

### 8.1 Disassembled printable package

`print_components.3mf` contains exactly `34` printable bodies:

```text
12 stationary quadrants
 6 moving halves
16 stationary bridges
34 total
```

All `44` screws, `44` nuts, and `22` pins/dowels are absent from its printable
body set. Every body has a unique source label, BREP digest, material/profile,
plate assignment, actual raw/packed envelope, source-to-print transform, and
inverse restore transform.

### 8.2 I3.8 Orca source project

The separate Orca source project retains exactly six plates and six build
objects, one named moving half per plate, with the frozen I3.8 UUID, name,
extruder `1`, filament slot `1`, physical tool `T0`, and filament identifier
`GFG00` mapping. It is not a replacement for the 34-body disassembled package.
Six actual Orca plate records are required; one standard 3MF build plus custom
metadata claiming six plates is RED. Embed and verify the frozen
machine/process/filament source paths and hashes, four-nozzle configuration,
actual bed definition, exact `3.50 mm` moving brim, zero skirt loops, and
disabled prime tower.

The semantic projection schema is exactly
`kage.i3.12.3mf-parity-projection.v3`. Relationship entries contain exactly
`source_part`, `id`, `type`, `target_mode`,
`normalized_target_reference`, and `resolved_part_name`. Content types contain
exactly `defaults`, `overrides`, and `resolved`. JSON members use the pinned
RFC8785 JCS implementation; XML members use actual C14N1.1 without comments.
Raw hashes remain detached provenance and may not be relabelled as canonical
hashes.

## 9. Fresh atomic regeneration and parity

Each run must generate nominal STEP, exploded STEP, both 3MF obligations, and
all manifests into a new temporary directory. Validate there, import in a fresh
process, compare with source, then atomically replace published artifacts. File
existence and timestamps are never freshness evidence.

Source/import gates:

- logical registry exactly `275 =131 protected +18 replacement +126 new`;
- printable bodies exactly `34`;
- all protected labels, transforms, topology, AABBs, areas, volumes, and BREP
  digests unchanged;
- exact global bounds preserved;
- imported actual bounds are measured; any `maxY=150.253499 mm` result is RED
  against the frozen `150.000000 mm` maximum;
- two fresh builds produce equal semantic manifests;
- all referenced hashes recompute exactly;
- freshness input digests cover geometry, spec, export, parity, every frozen
  predecessor, frozen STEP, and profile source; deleting a signature may not
  bless or reuse an existing archive;
- no stale, hand-edited, or partially replaced STEP/3MF survives.

## 10. Actual-solid acceptance matrix

| Gate | Authoritative acceptance |
|---|---:|
| moving reconstruction XOR outside seam ROI | `<=1e-7 mm3` |
| stationary reconstruction XOR outside seam ROI | `<=1e-7 mm3` |
| moving teeth | `130/half`, `260/ring` |
| adjacent-flank tangential phase error | `<=0.10 mm` |
| actual-solid race samples | `>=1040/ring` |
| CAD race TIR | `<=0.02 mm` |
| non-whitelisted positive intersection | `<=1e-7 mm3` |
| authorized press pairs | exactly `22` named pairs |
| each moving D3/D2.95 press IV | `0.4673119072 mm3` |
| each chassis D4/D3.95 press IV | `1.2487830798 mm3` |
| each frame D3/D2.95 press IV | `0.6075054794 mm3` |
| each front-ring D2/D1.95 press IV | `0.4653484118 mm3` |
| driver/loading obstruction before closure | `<=1e-7 mm3` |
| nut capture after closure | no removal path without opening the joint |
| slip-side positive intersection | `0 mm3` |
| slip diametral clearance | `<=0.12 mm` |
| hour-fin to bridge clearance | `>=0.60 mm` |
| motion transforms | exactly `189540` |
| motion unintended IV | `<=1e-7 mm3` |
| transformed moving-half raw span | each axis `<=244.864483 mm` |
| moving brim | exactly `3.50 mm/side` |
| full moving packed envelope | inside `[5,265]^2` |
| plate-occurrence positive overlap | `<=1e-7 mm3` |
| printable body set | exactly `34`, no purchased hardware |
| protected exterior-mask XOR | `0` for 4- and 8-connectivity |
| foreground XOR outside authorized ROI | `0` |
| global outer-contour XOR | `0` |
| source/import protected drift | none |

Actual-solid evidence means the test constructs, transforms, imports, measures,
intersects, or sweeps the real BREP/mesh involved. Prefilled counts, zeros,
booleans, labels, empty drift arrays, clamped values, or manifest self-claims do
not satisfy any row in this matrix.

## 11. Boundary

Passing this handoff proves only source-level CAD, STEP, and source-3MF
acceptance. Six real G-codes, first-layer/profile/T0 checks, printed seam and
dowel coupons, assembly fit, warp, TIR, wear, strength, motion, noise, thermal,
and optical performance remain RED/PENDING or physical-validation work.

No new design amendment is required. Apply the existing amendment precedence,
repair the implementation locally under
`p3_v3_phase3_i3_r1_real_joinery`, and prohibit unrelated redesign.
