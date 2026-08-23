# KAGE P3 V3 Phase-3 I3 U1 segmentation and joinery — accepted specification

Status: **ACCEPT — frozen design input for implementation**  
Revision: **I3.1 manufacturing freeze**  
Acceptance date: **2026-08-19**  
Scope: printable segmentation, joinery, assembly, artifacts, and validation only  
Units: millimetres, degrees, newtons, and cubic millimetres unless stated otherwise  
Coordinates: XY is the clock plane; +Z faces the viewer

This document records the independently accepted Phase-3 segmentation and
joinery design for the frozen KAGE Phase-1 plus Phase-2A I1 assembly. It does
not authorize changes to the transmission, optical geometry, motors, roller
towers, Phase-2A retention, or any other protected source geometry.

The original independent I3 handoff is retained in Appendix A for audit. The
I3.1 manufacturing amendments in the normative body supersede every conflicting
insert, bridge, moving-lap, receiver, and hardware value from that original
handoff. Implementations must not mix superseded and current dimensions.

## Frozen input

The sole mechanical baseline is:

`models/p3_v3_locked_parametric_repair_r1_i1_fixed_tower_retention/p3_v3_r1_i1_fixed_tower_retention_assembled.step`

Frozen Phase-2A STEP SHA-256:

`8bc30cab75f83380b6b53fb967b935a9198b36f814368ce53826e574f9649724`

Measured baseline facts:

- 203 accepted assembled occurrences;
- assembled bounds `[-150,-150,-32.5]` to `[150,150,24.2514]`;
- moving H/M/S carriers are four 65-tooth quadrants per role;
- rear chassis, stationary frame, and outer front optical ring are already four
  quadrants each;
- every accepted occurrence individually fits within a conservative 250 x 250
  XY envelope;
- there is no accepted Hall pocket, balance pocket, magnet, cap, wire, or Hall
  routing solid. Phase-1 contains only unused Hall/balance metadata.

## 1. Ownership and named parameters

All I3 parameters are owned by the `phase3_i3_u1_segmentation_joinery` design
group. An implementation must expose these names rather than burying numerical
literals in geometry code.

| Parameter | Frozen value |
|---|---:|
| `u1_nominal_xy_mm` | 270.00 |
| `u1_edge_keepout_mm` | 5.00 per edge |
| `u1_usable_xy_mm` | 260.00 |
| `fallback_raw_bed_xy_mm` | 260.00 |
| `fallback_usable_xy_mm` | 250.00 |
| `moving_half_raw_xy_max_mm` | 238.99 |
| `moving_brim_nominal_mm` | 5.00 per side on 270 bed |
| `moving_brim_fallback_max_mm` | 3.50 per side on 260 bed |
| `ring_teeth` | 260 |
| `moving_segment_count_per_role` | 2 |
| `moving_segment_teeth` | 130 |
| `stationary_segment_count_per_family` | 4 |
| `moving_seam_base_deg` | 15.230769230769 |
| `stationary_seam_base_deg` | 37.50 |
| `moving_join_radii_mm` | 133.50 to 140.00 |
| `moving_join_tangent_length_mm` | 16.00 |
| `moving_lower_lap_mm` | 2.00 |
| `moving_upper_lap_mm` | 1.00 |
| `lap_xy_clearance_mm` | 0.10 per side |
| `lap_z_clearance_mm` | 0.08 |
| `seam_face_relief_mm` | 0.025 per mating face |
| `seam_gap_target_mm` | 0.05 |
| `seam_gap_range_mm` | 0.03 to 0.10 |
| `seam_step_target_mm` | at most 0.10 |
| `seam_step_hard_max_mm` | 0.15 |
| `tooth_phase_tangent_max_mm` | 0.10 |
| `race_tir_target_mm` | at most 0.15 |
| `race_tir_hard_max_mm` | 0.20 |
| `race_pitch_concentricity_max_mm` | 0.10 |

## 2. Segmentation architecture

### 2.1 Moving carriers

Each hour, minute, and second carrier is split into two 180-degree, 130-tooth
halves. This produces six moving printed parts and two seams per role.

The tooth pitch and moving seams are:

```text
p_theta = 360 / 260 = 1.384615384615 degrees
p_arc   = 2*pi*130 / 260 = 3.141592653590 mm at pitch radius R130
beta_m  = 11*p_theta = 15.230769230769 degrees
seams   = beta_m and beta_m + 180 = 195.230769230769 degrees
teeth_per_half = 180 / p_theta = 130
```

The seam angles remain on the accepted tooth lattice and are approximately
14.77 degrees or farther from the accepted motor stations at 0/120/240
degrees, roller towers at 60/180/300 degrees, and fins at 305/45/145 degrees.

A three-way moving split is forbidden because `260/3` is not an integer. Four
moving quadrants are retained only as a documented fallback if a real U1 plate
or physical runout test rejects the semicircles.

### 2.2 Stationary structure

The rear chassis, stationary frame, and outer front optical ring remain four
quadrants each. Their seam angles are:

`beta_s + 90*k`, where `beta_s=37.5 degrees` and `k=0,1,2,3`.

This leaves at least 7.5 degrees from accepted motor, tower, and front-post
axes. Stationary semicircles are forbidden: an OD300 semicircle is about
256.07 mm before brim and violates the conservative packing rule.

Actual-solid bounds measured for the selected cuts are:

- moving half, including its role fin: at most 238.99 XY;
- rear chassis quadrant: at most 203.307 XY;
- stationary frame quadrant: at most 210.317 XY;
- outer front optical ring quadrant: at most 210.317 XY.

### 2.3 Geometry restoration rule

Segments must be produced by intersecting the frozen world-coordinate full
solid with source-owned sector masks. Teeth, fins, and functional surfaces
must not be rotated or reconstructed from approximations. Print-plate
transforms are packaging metadata only and never alter assembled transforms.

At nominal assembly, complementary segment unions reconstruct the frozen solid
outside the explicit seam envelopes. The Boolean XOR between reconstructed and
frozen solids outside those envelopes must be no more than `1e-7 mm3`.

## 3. Moving half-lap joint — normative I3.1

There is no separate underside splice plate and no threaded insert.

Each of the six moving seams uses an integral, flush outer-band half-lap:

- radial band `R=133.50..140.00`, width 6.50;
- tangential overlap length 16.00, or +/-8.00 about the seam;
- lower/rear lap thickness 2.00;
- upper/front lap thickness 1.00;
- XY clearance 0.10 per side;
- Z clearance 0.08;
- seam face relief 0.025 per face.

One half owns both lower laps and the mating half owns both upper laps, allowing
the upper half to be lowered in +Z onto the lower half on a flat circular jig.
The join band begins 1.00 outside the active tooth-root radius R132.50. No join
feature may enter the locked R131.60 race or an active tooth flank.

### 3.1 Moving screws and captive nuts

Two screw/nut axes per seam are located at local:

`R=136.75, tangent=-5.00` and `R=136.75, tangent=+5.00`.

Hardware per seam:

- 2 x ISO 7380-1 M2x3 button-head screws;
- 2 x DIN 562 M2 nominal 4x4 square nuts, accepted only when measured height
  is at most 1.60;
- button head diameter at most 3.50 and height at most 1.20;
- D2.20 clearance through the upper lap;
- 4.20 x 4.20 x 1.70 nut pockets in the 2.00 lower lap.

The nut pockets open in +Z at the lap interface. Nuts are loaded into the lower
half before the upper half is placed; the upper lap closes and captures the
pockets. A 0.30 rear/bed skin remains below each pocket.

Screw stack proof:

`3.00 = 1.00 upper lap + 1.60 nut engagement + 0.40 internal tip space`.

There is no rear screw protrusion. The maximum front button-head projection is
1.20, leaving at least `2.55-1.20=1.35` to the adjacent accepted carrier layer.

The join ligament equations are:

```text
nut radial wall        = (6.50-4.20)/2 = 1.15
nut-to-dowel ligament  = 5.00-2.10-1.55 = 1.35
tangential end wall    = 8.00-(5.00+2.10) = 0.90
tooth-root setback     = 133.50-132.50 = 1.00
```

Any actual-solid result below one of these values is RED.

### 3.2 Moving dowel

One steel D3.00 x3.00 registration pin is centred per seam at
`R=136.75, tangent=0`.

- lower lap finished bore D2.95: qualified press side;
- upper lap finished bore D3.10: slip side;
- pin insertion is +Z after the halves mate.

The press and slip interfaces must be gauged independently. CAD nominal values
do not prove the printed or reamed fit.

### 3.3 Moving hardware quantities

Per moving seam: 2 screws, 2 nuts, 1 pin.  
Per role: 4 screws, 4 nuts, 2 pins.  
All three roles: **12 M2x3 screws, 12 DIN 562 M2 nuts, and 6 D3 pins**.

## 4. Stationary joinery — normative I3.1

All stationary receivers use DIN 562 captive nuts. There are no heat-set or
press-in threaded inserts.

### 4.1 Rear chassis

Each of four chassis seams uses two rear bridge blocks centred at R85 and
R120. Each bridge is 12 radial x18 tangential x4 thick.

Per bridge:

- two 5.70 x5.70 x2.00 pockets at tangent +/-5.50;
- two DIN 562 M3 nuts, accepted only if measured height is at most 1.90;
- pockets open in +Z at the assembly face;
- nuts load before the chassis quadrants are placed, and the chassis closes
  the loading openings;
- two D3.40 chassis clearance holes;
- two ISO 7380-1 M3x5 screws;
- one D4.00 x6 alignment dowel with D3.95 bridge press bore and D4.10 chassis
  split slip bore.

M3 stack proof:

`5.00 = 2.50 chassis + 1.90 nut engagement + 0.60 D3.40 captured tip relief`.

Per chassis seam: 2 bridges, 4 screws, 4 nuts, 2 dowels.  
Four chassis seams: **8 bridges, 16 M3x5 screws, 16 DIN 562 M3 nuts, 8 D4
dowels**.

### 4.2 Stationary frame

Each of four frame seams uses one rear bridge:

- radial range R144.50..150.00;
- tangential length 16.00;
- thickness 3.00;
- two 4.20 x4.20 x1.70 DIN 562 M2 pockets at
  `R=147.80, tangent=+/-5.00`;
- pockets open +Z and are closed by the frame quadrant;
- DIN 562 M2 nut measured height at most 1.60;
- two D2.20 frame clearance holes;
- two ISO 7380-1 M2x4 screws;
- one D3.00 x5 dowel with at least 2.60 press engagement in a D2.95 bridge
  bore and 2.40 slip engagement in a D3.10 frame split bore.

The inner radial nut ligament is:

`147.80-2.10-144.50 = 1.20`.

The screw stack is exactly:

`4.00 = 2.40 frame + 1.60 nut engagement`.

Four frame seams: **4 bridges, 8 M2x4 screws, 8 DIN 562 M2 nuts, 4 D3
dowels**.

### 4.3 Outer front optical ring

Each of four front-ring seams uses one rear bridge:

- radial range R144.50..150.00;
- tangential length 16.00;
- thickness 3.00;
- two 4.20 x4.20 x1.70 DIN 562 M2 pockets at
  `R=147.80, tangent=+/-5.00`;
- pockets open +Z and are closed by the optical-ring quadrant;
- two D2.20 ring clearance holes;
- two ISO 7380-1 M2x3 screws;
- one D2.00 x4 dowel with 3.00 press engagement in a D1.95 bridge bore and
  1.00 slip engagement in a D2.10 ring split bore.

Front-ring screw stack:

`3.00 = 1.00 ring + 1.60 nut engagement + 0.40 D2.20 tip relief`.

Four front-ring seams: **4 bridges, 8 M2x3 screws, 8 DIN 562 M2 nuts, 4 D2
dowels**.

Every frame/front bridge remains at R144.50 or greater. The hour fin ends at
R143.90, leaving a hard radial optical clearance of 0.60. Minute and second
clearances remain larger.

### 4.4 Frozen joinery totals

| Family | Bridges | Screws | DIN 562 nuts | Dowels/pins |
|---|---:|---:|---:|---:|
| moving carriers | 0 | 12 | 12 | 6 |
| rear chassis | 8 | 16 | 16 | 8 |
| stationary frame | 4 | 8 | 8 | 4 |
| outer front ring | 4 | 8 | 8 | 4 |
| **I3 total** | **16** | **44** | **44** | **22** |

No hardware quantity may be inferred from duplicated viewer references. The
source registry and BOM must each equal this table.

## 5. U1 print contract

The normal profile uses the nominal 270 x270 bed with a 5.00 keepout on every
edge, giving 260 x260 usable XY.

For a moving half:

`238.99 + 2*5.00 = 248.99 < 260.00`.

If a slicer exposes only a raw 260 x260 bed, its 5.00 edge keepout gives 250
x250 usable. In that profile the moving brim must be no more than 3.50 per
side:

`238.99 + 2*3.50 = 245.99 < 250.00`.

Any larger brim, skirt, support, purge feature, or slicer exclusion envelope
that exceeds the usable bed is RED. Nominal part bounds alone are insufficient.

Print orientation:

- moving halves: frozen rear planar face on bed, +Z and fin upward, one half
  per plate;
- chassis, frame, and optical ring quadrants: rear planar face on bed;
- stationary bridges: flat;
- two same-family stationary quadrants may share a plate only after actual
  brim/support envelopes prove containment and zero overlap.

The six moving halves require six dedicated primary plates. The expected
stationary minimum is two chassis, two frame, and two outer-ring plates, but
plate count is evidence-derived rather than assumed.

## 6. Assembly and service order

1. Print coupons for seam gaps, captive-nut pockets, and every press/slip
   dowel pair. Qualify the selected material/profile before production parts.
2. Print and inspect all segments. Finish only source-designated holes.
3. Assemble the chassis on a flat R150 datum jig. Load bridge nuts, place the
   quadrants, seat dowels, and tighten screws crosswise. Verify flatness.
4. Assemble the stationary frame in the same way, then install accepted posts.
5. Assemble the outer optical ring, but do not mount it on the clock yet.
6. For each role, place the lower-lap half on a circular jig, load four DIN 562
   nuts, lower the upper-lap half in +Z, insert both dowels, and tighten the
   four M2 screws crosswise.
7. Each complete ring must pass tooth phase, seam step/gap, and runout tests
   before it enters the stack. In-stack nut loading, dowel pressing, seam
   drilling, or seam tightening is forbidden.
8. Install the frozen transmission rear-to-front: hour, minute, second, while
   retaining the accepted roller, spacer, axle, motor, and I1 retention order.
9. Install the outer front optical ring last.
10. Service follows the exact reverse order.

## 7. Functional equations and acceptance

Tooth-phase tangential error at pitch radius R130 is:

`e_t = 130*abs(delta_theta_rad) <= 0.10`.

Equivalent angular error:

`abs(delta_theta) <= 0.044073 degrees`.

Acceptance limits:

- assembled seam gap: 0.03..0.10;
- radial and axial seam step: target at most 0.10, hard maximum 0.15;
- race radial TIR: target at most 0.15, hard maximum 0.20;
- race-to-pitch concentricity: at most 0.10;
- no proud tooth flank or race land;
- moving seam tangential proof load: at least 15 N without slip, crack,
  stripped nut, gap growth over 0.05, or permanent step over 0.05;
- moving seam axial peel proof: at least 10 N;
- chassis joint proof: at least 50 N per seam;
- frame and front-ring joint proof: at least 15 N per seam;
- frame/front joinery to hour-fin radial clearance: at least 0.60;
- moving screw-head to adjacent carrier axial clearance: at least 1.35.

These values are design acceptance requirements, not claims about untested
printed parts.

## 8. Exact change allowlist

Only the following exact accepted labels or exact label pairs are replaceable.

### 8.1 Stationary labels

For `k=1..4`:

- `p3_v3_direct_race_rear_chassis_Q{k}_two_fixed_one_adjustable_tower`
  -> `p3_v3_direct_race_rear_chassis_I3_beta37p5_quadrant_Q{k}`;
- `p3_v3_r2_stationary_frame_quadrant_Q{k}`
  -> `p3_v3_r2_stationary_frame_I3_beta37p5_quadrant_Q{k}`;
- `p3_v3_r2_stationary_outer_front_ring_quadrant_Q{k}`
  -> `p3_v3_r2_stationary_outer_front_ring_I3_beta37p5_quadrant_Q{k}`.

### 8.2 Moving label pairs

For each role `hour`, `minute`, and `second`:

- exact pair `quadrant_Q1_65T_BARE_carrier_race` plus
  `quadrant_Q2_65T_BARE_carrier_race`
  -> `I3_half_A_130T_beta15p230769`;
- exact pair `quadrant_Q3_65T_BARE_carrier_race` plus
  `quadrant_Q4_65T_BARE_carrier_race`
  -> `I3_half_B_130T_beta195p230769`.

The complete accepted prefix
`p3_v3_direct_race_{role}_M1_260T_` remains part of every source label.

These pairs define occurrence ownership only. New halves must come from the
frozen full-ring world BREP, not literal fusion or rotation of old quadrants.

### 8.3 Removed old seam labels

Every old label matching one of these exact enumerated families must be absent
for roles hour/minute/second and seam indices 1..4:

- `p3_v3_r2_{role}_seam_{n}_underside_splice`;
- `p3_v3_r2_{role}_seam_{n}_3mm_registration_dowel`;
- `p3_v3_r2_{role}_seam_{n}_M2_screw_1_REFERENCE`;
- `p3_v3_r2_{role}_seam_{n}_M2_screw_2_REFERENCE`.

New moving hardware labels are limited to:

- `i3_{role}_seam_{1|2}_dowel`;
- `i3_{role}_seam_{1|2}_M2_button_screw_{1|2}`;
- `i3_{role}_seam_{1|2}_DIN562_M2_nut_{1|2}`.

Stationary bridge, screw, nut, and dowel labels must explicitly enumerate
family, seam 1..4, bridge where applicable, and hardware index. Wildcard
ownership is forbidden.

### 8.4 Protected geometry

The following accepted occurrence ranges are protected exact by their original
labels and BREP facts:

- outer posts occurrences 008..013;
- all tower and I1 geometry occurrences 018..068 and 201..202;
- all motor yokes, clamp hardware, and station parts 069..107, 128..138,
  159..169, and 190..200;
- every tooth, race, fin, and carrier surface outside a named seam envelope;
- all accepted transforms and the global assembled envelope.

No Hall/balance geometry may be introduced under I3 ownership.

## 9. Actual-solid RED tests

### 9.1 U1 and plates

- Orient every printable actual BREP using its recorded print transform.
- Union its brim, skirt, support, purge, and exclusion envelopes.
- Require complete containment in the selected usable XY and Z<=270.
- Require zero positive-volume overlap between plate occurrences.
- Require exactly one moving half per plate.

### 9.2 Segment reconstruction and teeth

- Reconstruct each moving and stationary family from actual source segments.
- Outside seam envelopes, require XOR with frozen full source <=`1e-7 mm3`.
- Count exactly 130 teeth per moving half and 260 per assembled ring.
- Test both moving seams for adjacent-flank pitch and `e_t<=0.10`.
- Sample actual-solid ring radius at least 1040 angular positions.
- CAD race TIR must be at most 0.02 before print allowances; exported and
  physical assemblies must satisfy the target/hard limits above.

### 9.3 Hardware and loading paths

- Instantiate every screw, DIN 562 nut, bridge, and dowel as an actual solid.
- Prove all pocket sizes, nut heights, screw engagements, tip reliefs, and
  named ligaments from faces rather than labels.
- Sweep driver cylinders along every screw axis in preassembly order; require
  IV<=`1e-7 mm3` against non-target protected solids.
- Translate actual nuts through their named +Z loading openings before the
  closing half/quadrant is placed.
- After closure, nut removal in every direction must collide unless its screw
  and the closing part are removed.
- Gauge press and slip dowel halves separately. Slip sides must have zero
  positive-volume intersection and no more than 0.12 diametral clearance.

### 9.4 Full motion

Every moving seam must sweep past all three pinions and all nine roller solids
because the rings rotate through 360 degrees.

For each role, test:

```text
phi = j*360/260, j=0..259
additional seam offsets = -0.05, 0, +0.05 degrees
motor q = -0.35, 0, +0.10
adjustable tower q = -0.25, 0, +0.25
```

No unintended positive-volume intersection greater than `1e-7 mm3` is allowed.
Accepted tooth mesh and roller-contact semantics remain unchanged.

### 9.5 Source/export parity and silhouette

- Rebuild in fresh processes and compare the source assembly with imported
  STEP using measured serializer tolerances.
- Protected labels, topology, transforms, AABBs, areas, volumes, and BREP
  digests must remain exact under their existing calibrated floors.
- Global bounds must remain `[-150,-150,-32.5]` to
  `[150,150,24.2514]`.
- Locked-camera exterior masks using both four- and eight-connected background
  flood fill must remain unchanged outside explicit seam/hardware ROIs.
- Global outer-contour XOR must be zero. Foreground changes are allowed only
  within named I3 ROIs.

## 10. Required artifacts and manifests

Implementation must generate from source, never by hand-editing exports:

- `assembled_nominal.step`;
- `service_exploded.step`;
- disassembled `print_components.3mf`;
- source/import parity manifest;
- purchased-hardware BOM;
- assembly-state manifest;
- per-plate print manifest.

Each 3MF/plate occurrence row must include:

- exact source label and source BREP SHA-256;
- material, printer, slicer profile, nozzle, and layer height;
- bed profile 270 or fallback 260;
- edge keepout and brim width;
- support/skirt/purge envelope;
- raw and full packed bounding boxes;
- plate identifier and overlap result;
- source-to-print transform;
- inverse restore-to-assembly transform.

The 3MF must contain disassembled printable components only. An assembled
300 mm clock in a print 3MF is RED. Purchased hardware may be represented in
assembly STEP/manifest but must not be marked printable.

Assembly states must distinguish at least:

- source printed segments;
- purchased hardware;
- preassembled role rings;
- nominal installed assembly;
- service/exploded assembly.

## 11. Refusal rules and physical boundary

Reject implementation when any of the following occurs:

- three moving segments or any noninteger tooth allocation;
- stationary semicircles;
- seams off the tooth lattice;
- moving join material below R133.50 or outside the named R140.00 seam ROI;
- any modification of the R131.60 race or active teeth outside a seam ROI;
- any threaded insert;
- a loose one-millimetre splice plate or a screw without a real DIN 562
  receiver;
- DIN 562 hardware exceeding the measured height gate;
- a hidden or obstructed nut-loading, dowel, or driver path;
- stationary join material inward of R144.50;
- a brim/support envelope outside the selected usable bed;
- any old cardinal seam hole or old splice-plate occurrence surviving;
- in-stack ring seam assembly or adjustment;
- any protected occurrence drift or hidden positive-volume collision;
- any hand-edited STEP or 3MF.

CAD acceptance does not prove U1 adhesion, warp, half flatness, installed ring
TIR, tooth noise or backlash across seams, DIN 562 pocket wear, dowel fit,
joint load capacity, optical shadow continuity, 360-degree running behavior,
or repeatable service. Those remain physical acceptance gates and must be
reported separately.

---

## Appendix A — original independent I3 handoff retained for audit

This appendix is historical. Normative I3.1 values above supersede conflicts.

### A1. Original architecture and bed decision

The original handoff selected the same hybrid architecture: two 130-tooth
semicircles per moving role and four quadrants for each stationary family. It
rejected a three-way split because 260/3 is noninteger and rejected OD300
stationary semicircles because their pre-brim footprint was approximately
256.07. It established moving seam angles 15.230769 and 195.230769 degrees,
stationary seams at 37.5+90k degrees, a measured moving-part maximum of 238.99,
stationary maxima of 203.307/210.317, and the 270/260/250 bed semantics retained
above.

### A2. Original moving joint, superseded

The first handoff proposed an integrated outer-band half-lap at
R134.40..138.80 with 12.00 tangential length, a 2.00/1.00 lap split, M2 axes
at tangent +/-4.00, a central D3.10 bore, and DIN 562-like captive receivers.
Before manufacturing review it also described a separate 3 x12 x1 underside
plate and M2 receiver concepts inherited from the accepted geometry.

Manufacturing review rejected that narrow band and every insert/unspecified
receiver. The normative body expands the band to R133.50..140.00, overlap to
16.00, moves screws to R136.75/tangent +/-5.00, and freezes DIN 562 pockets,
loading openings, wall equations, and press/slip dowel ownership.

### A3. Original stationary joinery, superseded

The first handoff proposed rear bridge blocks but used unspecified M3 and M2
threaded inserts:

- chassis bridges 12 x18 x4 at R85/R120 with M3 insert receivers;
- frame bridge R145..150 x14 x3 with M2 inserts;
- front-ring bridge R145..150 x14 x3 with M2 inserts.

Manufacturing review rejected every insert and required DIN 562 nuts, explicit
loading/capture openings, screw stack proofs, and an inward extension of the
frame/front bridges to R144.50. Sections 4.1 through 4.4 are the complete
superseding values.

### A4. Original validation and artifact contract retained

The original handoff required:

- actual full-footprint bed tests including brim/support/skirt, not nominal
  BREP size alone;
- exact 130/260 tooth counts and tooth-phase continuity;
- actual-solid seam gap, step, runout, concentricity, joint, and tool tests;
- a 360-degree sweep across all pinions and all nine rollers;
- exact protected-occurrence source/export parity;
- locked-camera silhouette masks;
- source-owned STEP, service STEP, disassembled 3MF, plate manifest, BOM, and
  assembly-state evidence;
- an explicit physical-proof boundary.

Those requirements remain active and are expanded, not replaced, by the
normative I3.1 RED tests above.
