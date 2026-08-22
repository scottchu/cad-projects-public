# KAGE M1 Mechanics Specification

## Status and scope

This is the frozen numeric handoff for the KAGE M1 mechanics-first prototype.

- `KAGE_M1_PASSIVE_R0` covers the passive 300 mm clock mechanics.
- `KAGE_M1B_MOTOR_MESH_R0` covers a separate provisional motor-mesh bench test.
- B5A, B6, and B7 remain reference-only; none of their geometry is inherited.
- Motorized, thermal, optical, Hall, noise, and long-duration behavior remain explicitly unproven.

## 1. Printed-part manifest

M1 passive contains exactly 25 printed parts:

- 4 base quadrants.
- 9 ring sectors: hour, minute, and second, each split into three 120-degree sectors.
- 3 identical guide towers.
- 9 printed rollers: hour, minute, and second roller at each tower.

M1B contains exactly 2 provisional printed parts:

- 1 adjustable motor station.
- 1 18-tooth pinion.

M1 excludes continuous rails, loose splice plates, dowels, bearings, electronics, Hall parts, cable parts, and LED components.

## 2. Coordinate system and base

Use the table plane as `Z = 0`. The assembled base underside is coincident with it, and the base top is `Z = 6 mm`.

- Overall base diameter: 300 mm.
- Base outer radius: 150 mm.
- Center opening diameter: 132 mm.
- Center opening radius: 66 mm.
- Base thickness: 6 mm.
- Base seams: 45, 135, 225, and 315 degrees.
- Existing centered step-lap radial span: `R70-R116`.
- Existing centered step-lap tangential span: `+/-13 mm`.
- Step-lap thickness split: `3 + 3 mm`.
- Step-lap plan clearance: `0.2 mm` at each edge.
- Two M3 fasteners per seam at radii 82 and 104 mm.

The `0.2 mm` step-lap edge clearance is a nominal CAD allowance and an explicit
physical fit gate. It must be verified on the printed base; it is not evidence
that the four quadrants will assemble flat without sanding or tolerance tuning.

Base fasteners:

- M3x6 socket-head screws.
- Clearance bore: 3.4 mm diameter.
- Head counterbore: 5.7 mm diameter.
- Captive, side-loaded nut pocket: 5.8 mm across flats by 2.6 mm deep.
- Nominal nut: 5.5 mm across flats by 2.4 mm thick.
- Solid bottom skin below the screw tip and nut pocket: 0.3-0.4 mm.
- No fastener may protrude through the `Z = 0` table plane.

## 3. Ring bodies, gears, and fins

### Ring stack

The thinnest ring is on top and the thickest ring is on the bottom.

| Stack position | Role | Body Z interval | Body thickness |
| --- | --- | ---: | ---: |
| Bottom | Hour | 27.5-30.5 mm | 3.0 mm |
| Middle | Minute | 32.2-34.9 mm | 2.7 mm |
| Top | Second | 36.6-39.0 mm | 2.4 mm |

The body gap between neighboring rings is 1.7 mm:

```text
0.5 flange + 0.5 washer + 0.5 flange + 0.1 + 0.1 running clearance = 1.7 mm
```

### Internal transmission

- Gear module: 1.0.
- Pressure angle: 20 degrees.
- Ring tooth count: 258.
- Teeth per 120-degree sector: 86.
- Ring pitch radius: 129 mm.
- Ring tooth-tip radius: 128 mm.
- Ring tooth-root radius: 131.5 mm.
- Smooth roller-race radius: 127.6 mm.
- Ordinary ring-body outer radius: 138.5 mm.
- Angular tooth pitch: `360 / 258 = 1.395348837 degrees`.
- Tooth phase: `0.697674419 degrees`, placing each sector seam between complete teeth.
- M1B pinion tooth count: 18.
- M1B pinion pitch radius: 9 mm.
- Nominal internal-gear center distance: `129 - 9 = 120 mm`.

### Axial race and gear faces

- Hour:
  - Race: `Z27.5-Z28.7`.
  - Relief: `Z28.7-Z28.9`.
  - Gear: `Z28.9-Z30.5`.
- Minute:
  - Race: `Z32.2-Z33.4`.
  - Relief: `Z33.4-Z33.6`.
  - Gear: `Z33.6-Z34.9`.
- Second:
  - Race: `Z36.6-Z37.6`.
  - Relief: `Z37.6-Z37.8`.
  - Gear: `Z37.8-Z39.0`.

### Shadow fins

All fin roots occupy `R134.5-R138.5`, on the outer top region of the corresponding ring.

| Role | Tangential width | Z interval | Height |
| --- | ---: | ---: | ---: |
| Hour | 5.0 mm | 27.5-32.0 mm | 4.5 mm |
| Minute | 3.2 mm | 32.2-36.4 mm | 4.2 mm |
| Second | 1.8 mm | 36.6-40.5 mm | 3.9 mm |

- Each fin stops 0.2 mm below the following ring body.
- Fin-root fillet target: 0.6 mm.
- Place each complete fin root and its fillet outside every `+/-6 mm` seam
  half-lap window. A fin belongs to the uninterrupted middle of one sector; it
  may not bridge a sector seam or enter a joint-pad window.
- The `0.2 mm` fin-to-following-body axial clearance is a nominal CAD allowance
  and an explicit physical no-contact gate for the printed three-ring stack.
- Optical shadow length is a later LED/wall-datum gate. M1 proves only mechanical clearance.

## 4. Integral ring joints

Each ring has three integral half-lap joints and uses one M3x6 screw at each seam.

- Tangential lap window: 12 mm.
- Each mating sector extends 6 mm across the seam.
- Tangential seam clearance: 0.15 mm per mating edge, 0.30 mm total.
- The gear/tooth band must terminate at the seam without cutting a tooth.
- The lap and fastener boss exist only in the structural outer band.

A fully recessed M3x6 fastening stack requires a localized 9.4 mm joint pad:

- Head recess depth: 3.0 mm.
- Under-head screw length: 6.0 mm.
- Solid floor below the screw tip: 0.4 mm.
- Captive, side-loaded nut pocket: 5.8 mm across flats by 2.6 mm deep.
- Nominal nut: 5.5 mm across flats by 2.4 mm thick.
- A 7.0 mm radial pad around a 5.7 mm head recess leaves a 0.65 mm wall per side.
- A 12 mm tangential pad around a 5.7 mm head recess leaves a 3.15 mm end wall per side.
- The screw enters axially from the visible/top face.
- The nut enters tangentially from the sector seam.
- No screw, head, or nut protrudes below the localized pad.

### Frozen sector-to-pad topology

Build every ring sector as one connected solid in this order:

1. Create the ordinary 120-degree sector body, including its uninterrupted
   race and complete-tooth band.
2. Add any role-specific neck and the localized joint pad.
3. Union `sector + neck + pad` into one solid.
4. Only after that union, cut the mating half-lap, screw bore, head recess, and
   side-loaded nut pocket.

Hour and second pads are already integral to their sectors inside the common
inner pad lane. They require no separate neck.

The minute role uses this exact connector:

- Minute pad: `R139.0-R146.0`, `Z25.5-Z34.9`.
- Minute neck: `R138.1-R139.3`, `Z32.2-Z34.9`.
- Clip the minute neck to that sector's existing `+/-6 mm` seam half-lap
  ownership. The neck may not continue around the ring or cross into the
  neighboring sector's lap ownership.
- Union the minute sector, clipped neck, and pad before making any joint or
  fastener cut.

### Rotation-safe pad zones

- Hour pad lane: `R131.7-R138.7`, `Z21.1-Z30.5`.
- Second pad lane: `R131.7-R138.7`, `Z36.6-Z46.0`.
- Minute pad lane: `R139.0-R146.0`, `Z25.5-Z34.9`.
- Minute neck lane: `R138.1-R139.3`, `Z32.2-Z34.9`, clipped tangentially to
  the owning sector's `+/-6 mm` seam half-lap window.
- Hour and second share a radial lane but are axially disjoint by 6.1 mm.
- The minute pad is radially separated from the hour/second pad lane by
  `139.0 - 138.7 = 0.3 mm` wherever their Z intervals overlap.
- The minute neck overlaps the common radial lane, but it is axially separated
  from the hour pad by `32.2 - 30.5 = 1.7 mm` and from the second pad by
  `36.6 - 34.9 = 1.7 mm`.
- Therefore the independently rotated swept connector volumes have a minimum
  nominal separation of 0.3 mm in the pad-overlap region and 1.7 mm in the
  neck/common-lane region.

Required proof: rotate all three complete connector sets independently through
360 degrees and prove that their swept volumes are disjoint. The actual solids
must also prove that every sector remains one connected solid after all lap and
fastener cuts.

The 0.30 mm total seam clearance and the 0.3 mm radial pad separation are
nominal CAD allowances and explicit physical fit gates. They must be checked on
the printed ring seams and freely rotating stack; equation or BREP clearance
alone does not prove reliable printed motion.

## 5. Sector print bounds

The Snapmaker U1 test bed is `270 x 270 mm`. Orient each 120-degree sector on
positive X with a `+/-60-degree` angular span and allow a 5 mm brim on every
side. Fins stay outside seam windows and must be oriented inward in the print
layout so they do not enlarge the stated tangential envelope.

- Hour/second maximum raw tangential span: approximately 246.25 mm.
- Hour/second span including brim: approximately 256.25 mm.
- Hour/second remaining U1 margin: approximately 13.75 mm total, or 6.875 mm
  per centered side.
- Minute maximum raw tangential span: approximately 258.88 mm.
- Minute span including brim: approximately 268.88 mm.
- Minute remaining U1 margin: approximately 1.12 mm total, or 0.56 mm per
  centered side.
- The minute sector is the limiting part. Its small stated margin is a physical
  slicer-placement gate, not a guarantee of printable brim clearance.

Actual exported BREP bounds, not only these equations, are a mandatory acceptance test.

## 6. Guide towers and roller stack

### Tower placement and radial guidance

- Three identical printed tower bodies at 0, 120, and 240 degrees.
- The 0- and 120-degree stations are fixed.
- Only the 240-degree station has small radial tolerance trim.
- This is a true three-point support arrangement.
- Roller axle radius: 115.9 mm.
- Roller tread radius: 11.6 mm.
- Ring race radius: 127.6 mm.
- Nominal radial running gap:

```text
127.6 - (115.9 + 11.6) = 0.10 mm
```

- Roller flange radius: 13.0 mm.
- Radial flange capture overlap:

```text
115.9 + 13.0 - 127.6 = 1.30 mm
```

Let `q` be outward-positive tower trim:

```text
gap(q) = 0.10 - q
```

- Physical target after trim: 0.05-0.15 mm running gap.
- Do not use forced roller preload.
- Trim slot: 3.4 mm wide by 4.2 mm overall radial length.
- Slot travel: 0.8 mm total, or `+/-0.4 mm`.

### Printed rollers

| Roller | Groove height | Total height |
| --- | ---: | ---: |
| Hour | 3.2 mm | 4.2 mm |
| Minute | 2.9 mm | 3.9 mm |
| Second | 2.6 mm | 3.6 mm |

Exact axial stack:

- Bottom washer: `Z26.4-Z26.9`.
- Hour roller: `Z26.9-Z31.1`; groove `Z27.4-Z30.6`.
- Washer: `Z31.1-Z31.6`.
- Minute roller: `Z31.6-Z35.5`; groove `Z32.1-Z35.0`.
- Washer: `Z35.5-Z36.0`.
- Second roller: `Z36.0-Z39.6`; groove `Z36.5-Z39.1`.
- Top washer: `Z39.6-Z40.1`.

Each ring body has 0.1 mm axial running clearance at each groove face.

### Tower axle and mounting

- One M3x25 axle screw per tower.
- Install the axle screw upward through the tower before mounting the tower to the base.
- Capture its head in a 5.7 mm diameter by 3.1 mm deep counterbore.
- Axle screw under-head datum: `Z18.0`.
- Axle screw end: `Z43.0`.
- Bottom-up axle assembly:

```text
M3x25 screw
-> bottom washer
-> hour roller and ring
-> washer
-> minute roller and ring
-> washer
-> second roller and ring
-> top washer
-> M3 nyloc nut
```

- Each tower uses two M3x8 screws and two captive ordinary M3 nuts to mount to the base.
- Tower-foot target thickness: 3 mm.
- All tower mounting hardware remains above the `Z = 0` table plane.

## 7. M1B provisional motor-mesh test

M1B is a vertical-shaft bench mesh test only. It is not the final low-profile motor packaging.

- Provisional motor envelope: `20.3 x 20.3 x 39.3 mm`.
- Provisional shaft: 4 mm diameter by 7 mm protrusion.
- Supplied 15.4 mm M2 mounting-hole pitch remains measurement-gated.
- Two radial motor-station slots: 3.4 mm wide by 9.4 mm overall length.
- Available station travel: `+/-3 mm`.

Let `q` be outward-positive motor adjustment:

```text
C(q) = 120 + q
b(q) = b0 - 2q * tan(20 degrees)
```

At provisional `b0 = 0.20 mm`, a 0.10 mm backlash target corresponds to approximately `q = +0.137 mm`.

- The `+/-3 mm` range is setup travel only, never a powered operating range.
- Pinion bore must be `measured_shaft_diameter + measured_fit_clearance`; do not freeze it from a listing.
- Pinion face height must be parameterized by the role-specific ring gear face under test.
- A horizontal motor requires direction-changing hardware and violates the two-part M1B limit. It is explicitly deferred.

M1B cannot pass until the actual motor shaft, face, mounting-hole pitch, and pinion fit are measured.

## 8. Hardware and assembly sequence

Hardware quantities:

- 17 M3x6 screws: 8 base seams and 9 ring seams.
- 6 M3x8 screws: tower feet.
- 3 M3x25 screws: roller axles.
- 23 ordinary M3 nuts: 8 base, 9 ring, and 6 tower.
- 3 M3 nyloc nuts.
- 12 M3 washers.

Bottom-up passive assembly sequence:

1. Place all four base quadrants flat on the table plane.
2. Assemble the four centered base step-laps with eight M3x6 screws and captive nuts.
3. Pre-install one upward M3x25 axle screw in each guide tower.
4. Mount the three towers to the functional base holes with six M3x8 screws and captive nuts; leave the 240-degree trim tower adjustable.
5. Assemble the three hour sectors using their integral half-laps and three M3x6 screws.
6. Place the bottom washers, hour rollers, and hour ring on the three tower axles.
7. Add the first inter-roller washers.
8. Assemble and install the minute ring and rollers.
9. Add the second inter-roller washers.
10. Assemble and install the second ring and rollers.
11. Add the top washers and M3 nyloc nuts.
12. Adjust only the 240-degree tower until the measured running gap is 0.05-0.15 mm, then tighten it.
13. Rotate every ring manually through 360 degrees before any motor test.
14. Build and fit the separate M1B motor station only after the real motor is measured.

## 9. Meaningful acceptance tests

### Math and source tests

1. The manifest contains exactly 25 passive printed parts plus 2 M1B parts.
2. Four base quadrants lie flat at `Z = 0` and assemble without fastener protrusion.
3. Ring role order, thicknesses, Z positions, 1.7 mm gaps, and race/gear subfaces match this specification.
4. Each ring has exactly 258 teeth, each sector has 86 complete teeth, and no seam cuts a tooth.
5. Every exported sector plus a 5 mm brim fits a 270 x 270 mm bed.
6. Every M3 head, nut, tip, floor, and minimum wall fits inside its localized joint pad.
7. Every role-specific sector remains one connected solid after the prescribed
   union-before-cut sequence; the minute neck is clipped to the owning
   `+/-6 mm` seam half-lap window.
8. Independently rotated 360-degree swept connector volumes are disjoint, with
   the modeled 0.3 mm pad separation and 1.7 mm neck-to-common-lane axial
   separations preserved.
9. Roller groove containment, 0.1 mm face clearances, 1.3 mm flange capture, and the trim equation pass.
10. M1B center-distance and backlash equations pass, and no measurement-gated motor dimension is accidentally frozen as accepted fact.

### Actual-solid tests after implementation

- All 25 passive printed components are valid, connected solids.
- Actual BREP intersections are checked at these meaningful states only:
  - All fins and seams aligned as the worst overlap state.
  - Hour moved independently by one tooth.
  - Minute moved independently by one tooth.
  - Second moved independently by one tooth.
  - Six representative coupled clock positions.
- Prove no pad-to-ring, fin-to-ring, fin-to-tower, fin-to-pinion, roller-to-wrong-ring, or stationary-to-swept-body collision.
- Prove source/export dimensional parity for the base, every ring role, tower, roller, and M1B part.

### Physical gates

- Base lies on a flat table without rocking.
- Hand-tightened M3 base joints do not crack, lift, or distort their seams.
- One complete three-sector ring has radial seam runout no greater than 0.5 mm and no tooth snag.
- Printed base step-laps fit at their nominal 0.2 mm edge allowance without
  forcing, lift, or seam distortion.
- Printed ring half-laps fit at their nominal 0.30 mm total seam allowance, and
  the 0.3 mm radial minute-pad separation does not rub in any independent ring
  position.
- Every fin clears the next ring at the nominal 0.2 mm axial allowance and
  remains outside the assembled seam/joint windows.
- All three assembled rings rotate manually through 360 degrees without binding, cross-driving, tower contact, or fin collision.
- Assembled ring axial lift is no greater than 0.5 mm.
- Assembled ring radial rattle is no greater than 0.6 mm.
- Required third-tower trim remains within `+/-0.4 mm`.
- Motorized, thermal, optical, Hall, noise, and long-duration behavior remain unproven until their own physical stages.

## 10. Versioning, exports, and review packet

Implementation namespaces:

- `KAGE_M1_PASSIVE_R0`
- `KAGE_M1B_MOTOR_MESH_R0`

Required implementation exports:

- Assembled STEP.
- Exploded STEP.
- Table-assembly STEP showing the flat underside.
- Named-object 3MF containing exactly 25 passive objects.
- Sector print-layout STEP and 3MF.
- Separate M1B bench-test STEP and 3MF.

Required review views:

- Flat base underside and top view.
- Assembled front oblique view.
- Bottom-up exploded assembly.
- Seam macro for hour, minute, and second pad lanes.
- Roller-tower section showing the exact washer and groove stack.
- 120-degree sector print layout with measured brim bounds.
- Worst-case all-pad and all-fin alignment.
- M1B motor station at -3, 0, and +3 mm adjustment.

CAD acceptance is not physical proof. Print fit, friction, ring runout, fastener durability, motor mesh, noise, thermal behavior, optical performance, and serviceability must pass their stated physical gates before the next subsystem is accepted.
