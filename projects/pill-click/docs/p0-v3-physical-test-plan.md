# P0 v3 progressive physical-validation plan

This plan converts the accepted P0 v3 geometry into print gates. The sequence
is mandatory: C1R1/C1R1B rails (with legacy C2 diagnostic), C3 shutter track,
C4 rear snap, then the complete
manual P0. A failed gate stops the sequence; do not compensate by sanding,
scaling, lubricating, or forcing a part and then call it a pass.

P0 contains no return spring, return magnet, or push-push latch. Use only
inert plastic or glass test beads, never medication.

## Shared controls and tools

Print all compared specimens with the same:

- printer, build plate, nozzle, material spool, drying state, layer height,
  line width, wall count, temperatures, cooling, speed, and orientation;
- slicer scaling disabled; and
- no support touching a functional interface.

Required tools:

- digital callipers with 0.01 mm display resolution;
- 0-20 N push/pull gauge or equivalent gauge that records peak force;
- rigid straightedge and 0.10/0.20/0.30 mm feeler strips;
- 0.8 mm smooth probe wire with a rounded end;
- ten inert `3.0 +/- 0.1 mm` spherical test beads;
- magnifier, phone camera, backlight, timer, cycle counter, and permanent
  marker for specimen IDs.

Before testing, define these user-calibrated force gates and record how each
was obtained:

| Variable | Definition |
|---|---|
| `F_slide_limit` | Maximum sliding force the user accepts for repeated thumb operation, measured from ten trials on a comfortable reference control or deliberately selected on the gauge |
| `F_handling_pull` | Deliberate handling/tug load the assembled key and shutter capture must survive for ten seconds |
| `F_cover_required` | Minimum rear-cover extraction load required to exceed all measured normal operating and handling loads |

These variables must have measured values before they are used. This plan
does not invent universal force guarantees for an unprinted mechanism.

For every print, record:

```text
specimen ID, date/time, printer, nozzle, material/spool, drying history,
layer height, line width, walls, top/bottom layers, temperatures, cooling,
speed, orientation, slicer version/profile, print duration, visible defects,
all allowed cleanup, operator, ambient notes
```

## Gate C1R1/C1R1B: strengthened nominal rails, with preserved C2 diagnostic

The original C1 failed by derailment and retaining-lip fracture. Print C1R1
and C1R1B in the same batch without changing process. C2 is preserved in its
original short, loose form only to diagnose printer clearance; it cannot
approve capture durability. `C1R1` and `C1R1B` are coupon revision IDs, not
product design-version numbers.

| Variable | C1R1 primary | C1R1B durability | C2 legacy loose |
|---|---:|---:|---:|
| Groove width | 2.70 | 2.70 | 2.80 |
| Radial clearance | 0.20 | 0.20 | 0.30 |
| Tangential clearance/side | 0.25 | 0.25 | 0.30 |
| Land length | 6.80 | 6.80 | 3.40 |
| Normal lip/side | 0.80 | 1.20 | 0.35 |
| Mouth lip/side | 0.60 | 1.00 | 0.15 |
| Rail section | 2.20 x 1.20 | 2.20 x 1.20 | 2.20 x 1.20 |
| Rail length | 22.40 | 22.40 | 19.00 |
| Rail lead-in | 0.70 | 0.70 | 0.70 |
| Tested travel | 14.55 | 14.55 | 14.55 |

### Measurements and procedure

1. Confirm specimen IDs from the filenames. Measure the rail width/height at
   three Y stations; measure both normal lips, both mouth lips, groove
   width/depth, and land length. Reject C1R1 if either normal lip is below
   0.70 or either mouth lip below 0.50. C1R1B limits are 1.10 and 0.90.
2. Insert each receiver by hand from the specified leading edge. No tool or
   impact is allowed.
3. Complete 100 full `14.55 mm` cycles. Mark cycles `1, 10, 25, 50, 75, 100`.
4. At those six cycles, record breakaway peak, forward steady force, reverse
   steady force, and largest local spike. Use the same gauge direction and
   travel speed each time.
5. At cycles 0 and 100, apply a measured 10 N pull normal to the rail for ten
   seconds at inward, mid-travel, and released positions.
6. After cycle 100, remeasure the same sections and inspect for dust, gouging,
   whitening, cracks, delamination, mouth damage, and permanent looseness.

Observation row:

```text
coupon; section dimensions; cycle; breakaway peak; forward steady;
reverse steady; local peak; completed travel; binding location;
visible wear; dimensional change; pass/fail; notes/photo ID
```

### Exact pass/fail and selection rules

A coupon passes only if:

- it inserts by hand without functional-surface sanding;
- all 100 cycles complete the full `14.55 mm` travel without stall, seizure,
  derailment, or tool assistance;
- every recorded breakaway, steady, and local peak is `<= F_slide_limit`;
- there is no crack, delamination, gouge that catches the receiver, stress
  whitening, or rail/groove material loss that changes guidance; and
- the receiver remains guided at both endpoints and cannot disengage laterally
  during the normal sweep.

Select C1R1 when it passes all dimensional, force, 100-cycle, and 10 N pull
checks. Select C1R1B only when C1R1 shows lip damage or insufficient printed
wall count and C1R1B passes every gate. If neither strengthened nominal coupon
passes, stop. C2 may identify a clearance/process problem, but its thin short
lands cannot overrule a C1R1/C1R1B durability failure. A loose long-land
revision requires a separately specified coupon.

## Gate C3: captured shutter-track strip

Frozen coupon interface:

```text
track length=32.00; slider length=12.00; stroke=13.40
web=25.00 x 0.80; flange=27.40 x 0.80
lateral/floor/lip clearances=0.20; capture overlap=1.00/side
pressed/released slider centers=9.30/22.70
```

### Measurements and procedure

1. Measure web and flange thickness at both ends and center; measure track web
   and flange widths, mouth flare, floor clearance, lip clearance, and lip
   thickness on both sides.
2. Insert the slider by hand through the negative-Y track mouth.
3. Measure total lateral and vertical play at mid-stroke using the callipers or
   feelers while alternately loading both directions.
4. Record force traces at cycles `1, 10, 25, 50, 75, 100`, then complete 100
   full `13.40 mm` cycles.
5. At mid-stroke, apply `F_handling_pull` normal to the track for ten seconds,
   three times, allowing one minute between trials.
6. Inspect and remeasure after cycle 100.

Observation row:

```text
section dimensions; cycle; breakaway; forward/reverse steady; peak;
lateral play; vertical play; normal-pull load/time; capture result;
lip/flange wear; permanent set; pass/fail; notes/photo ID
```

C3 passes only if:

- insertion is tool-free and all 100 cycles complete `13.40 mm`;
- all measured sliding forces are `<= F_slide_limit`;
- total lateral play is `<=0.50 mm` and total vertical play is `<=0.50 mm`;
- the slider remains captured during all three `F_handling_pull` holds;
- neither lip nor flange cracks, whitens, delaminates, or takes a measurable
  permanent bend; and
- no wear ridge causes a stall or increasing local force spike.

Any capture failure, layer separation, or force above the calibrated gate
stops the full P0 print.

## Gate C4: reversible rear-cover snap

Frozen coupon interface:

```text
beam width=3.60; bending thickness=1.20; effective length=7.50
root fillet=0.80; hook protrusion=0.55; pocket clearance=0.20/side
receiver outer skin=1.20; nominal/worst geometric strain=1.76/2.08 percent
```

### Measurements and procedure

1. Measure beam thickness/width, effective length, hook protrusion, pocket
   width/depth, remaining outer skin, and undeflected hook datum.
2. Insert and remove the arm by hand for 30 full cycles.
3. Record insertion peak and extraction peak at cycles
   `1, 5, 10, 20, 30`.
4. After cycle 30, leave the arm unloaded for one minute; measure permanent
   hook set from the original datum.
5. Inspect the root fillet, beam layers, hook ramps, and receiver pocket under
   magnification.

Observation row:

```text
dimensions; cycle; insertion peak; extraction peak; permanent set;
root/beam/hook/pocket condition; whitening; pass/fail; notes/photo ID
```

C4 passes only if:

- all 30 cycles are tool-free and the hook positively seats every time;
- there is no crack, delamination, root tear, hook damage, pocket breakout, or
  visible stress whitening;
- permanent hook set after relaxation is `<=0.20 mm`;
- cycle-30 extraction force is at least `80%` of cycle-1 extraction force; and
- the measured one-arm force is retained as calibration data for the complete
  four-arm cover, not multiplied into an assumed guarantee.

If C4 fails, stop. Do not print the full cover with the same unchanged snap
geometry/process.

## Full manual P0 gate

Use the rail variant selected by C1R1/C1R1B and the same qualified process as C3
and C4.

### Preassembly checks

1. Inspect both `0.80 mm` opaque shrouds against a backlight. Any pinhole,
   unbonded strand, missing line, or open split is an immediate failure.
2. Measure each shroud thickness at five evenly distributed points. Every
   reading must be `0.80 +/-0.20 mm`.
3. Place a straightedge across each 25.40 mm shroud span. Maximum gap/sag at
   any of five points must be `<=0.20 mm`.
4. Confirm the shutters, selected rails, lost-motion couplings, blind rear
   cover, four stops, and four snap arms have no cracks or unsupported debris.
5. Couple shutters and shuttle outside at `s=q=0`, rear-feed the stack, then
   install the blind cover exactly as specified. Verify the cover-supplied
   shutter stops only after cover installation.

### Stroke, guidance, and force

1. Complete ten slow settling cycles without recording force.
2. Complete 50 recorded manual cycles from pressed `s=0` to released
   `s=13.40` and back. Record force traces at cycles `1, 10, 25, 50`.
3. Measure released-minus-pressed travel ten times at the same key datum.
   Every reading must be `13.40 +/-0.30 mm`; record mean and range.
4. Every cycle must reach both stops without bind, derailment, scraping that
   sheds material, or force above `F_slide_limit`.

### Pressed aperture alignment and accessibility

At `s=q=0`:

1. Inspect the complete `23x10 mm` top and `22x4.8 mm` bottom openings with
   backlight.
2. Probe the top on the nine-point grid
   `X={-11,0,11}`, `Y={-4.0,0.5,5.0}` and the bottom on
   `X={-10.5,0,10.5}`, `Y={1.3,3.2,5.1}` using the rounded 0.8 mm probe.
3. Every probe position must reach the medicine cavity without contacting a
   shutter, coupling, rail, or cover feature.
4. Introduce all ten 3 mm test beads through the top opening. All ten must
   enter without removing a part. Confirm that all ten can be recovered or
   dispensed through the bottom opening while the key remains pressed.

Any blocked grid point or inaccessible bead is a failure.

### Released hidden/no-through condition

At `s=q=13.40`:

1. Inspect top, bottom, front, and rear under backlight. Functional fill,
   outlet, coupling, track-entry, and tool holes must not be visible. Permitted
   moving seams are limited to the specified running clearances.
2. Repeat the same top and bottom nine-point probe grids. The 0.8 mm probe and
   a 0.10 mm feeler must not pass into the medicine cavity at any point.
3. The first stopping surface over each fixed port must be no more than
   `0.50 mm` below the nominal exterior face.
4. None of the ten 3 mm beads may enter through the top or bottom exterior in
   the released state.
5. Rear backlight and probe checks must include both shutter-track entries,
   all four snap regions, and the coupling-channel projection; no through path
   is allowed.

Any light-visible pinhole confirmed by probe, any feeler through-path, or any
functional opening accessible while released is a failure.

### Captivity and cover retention

1. At released, pull the key forward at `F_handling_pull` for ten seconds,
   three times. The shuttle must not extract, pass its captive stop, crack, or
   permanently change endplay.
2. Apply the same three holds normal to each shutter. Neither shutter may
   escape its track or damage a capture lip.
3. Measure complete-cover insertion and extraction force before cycling. If
   removal is necessary for measurement, reinstall it and verify all four
   snaps seat before continuing.
4. After the 50 mechanism cycles, measure cover extraction again. It passes
   only if the cover never released during operation, final extraction is at
   least `80%` of its initial value, and the minimum measured extraction is
   `>=F_cover_required` and greater than the maximum recorded normal operating
   force.
5. Inspect the key tabs, front shoulder, rear cover, stops, snap roots, hooks,
   and pockets for damage or permanent displacement.

### Full-P0 observation record

```text
selected rail C1R1/C1R1B and reason; legacy C2 diagnostic result;
shroud thickness points and maximum sag;
cycle; pressed datum; released datum; stroke;
breakaway/steady/local peak force each direction;
pressed top/bottom nine-point results;
released top/bottom nine-point results;
beads loaded/recovered in each state;
key pull load/time/result;
shutter pull load/time/result;
cover initial/final insertion and extraction;
cover retention during cycling;
rail/shutter/coupling/snap wear;
photos before/after; overall pass/fail; corrective action
```

## Final decision rules

- Advance to return-force experiments only when C1R1 or C1R1B, C3, C4, and the
  complete manual P0 all pass.
- Select C1R1 whenever it passes. Select C1R1B only under the strengthened
  durability rule above. C2 remains diagnostic and is not a production rail.
- A geometry or closure failure requires redesign; a repeatable process defect
  may be reprinted only after recording the changed process variable.
- Never hide a failed fit with global scaling. Never sand a functional coupon
  and use it to approve nominal CAD clearance.
- Force readings establish calibration gates for the next spring and magnet
  prototypes. They are observations, not promises about unprinted variants.
- The `0.80 mm` shrouds are the highest print-risk feature. A shroud pinhole,
  split bridge, or sag over `0.20 mm` blocks further assembly even if every
  other coupon passed.
