# KAGE hard-mechanics MVP — independent test architecture

Status: independent design critique and physical-validation handoff  
Date: 2026-08-19  
Scope: minimum mechanics before motors, electronics, optics, and release packaging  
CAD changes: none

## Decision

Yes: validate that the four rear-chassis/base quadrants become one flat, rigid,
repeatably assembled base before doing more transmission work.

The current release work is much broader than the MVP question. Its frozen
contract describes 275 assembled occurrences, 34 printable bodies, six moving
print plates, and a 189,540-state motion matrix. Those can be useful later, but
they do not answer the first physical dependency: whether four printed base
quadrants close as one usable datum.

Do not count a quadrant coupon, a CAD union, or four parts clamped flat as a
pass. The first prototype is the complete rear base with all four seams and the
intended joinery. A closed four-seam loop exposes cumulative pitch error,
warpage, overconstraint, and the difficult final-seam closure that a coupon
cannot.

## Minimum ordered prototypes

Each prototype reuses the preceding one. Stop at the first RED result, repair
only the responsible layer, and repeat that gate.

### MVP-1 — four-quadrant rear base

Build only:

- four `rear_chassis` quadrants;
- eight rear bridge blocks;
- the intended 16 M3x5 screws, 16 DIN 562 M3 nuts, and eight D4 dowels;
- a simple flat assembly surface and measuring references.

One failure question:

> Can the four independently printed quadrants close into one flat, rigid,
> serviceable base without forced alignment or stored distortion?

Physical acceptance:

- all four seams close in the documented order, including the last seam;
- no filing, heat-forming, clamping left in place, or enlarging of an
  undesignated feature is needed to obtain closure;
- no visible rocking on the reference surface; provisional total datum
  flatness is at most 0.50 mm across the 300 mm assembly;
- seam step is at most 0.25 mm and no seam opens more than 0.25 mm after the
  assembly is removed from the flat fixture for one hour;
- opposed tower/mounting datums agree within 0.50 mm in-plane;
- the vertically hung base carries its own weight for one hour without seam
  growth above 0.25 mm, cracking, dowel migration, or permanent set;
- three assemble/disassemble cycles do not strip a nut capture, loosen a press
  seat, crack a bridge, or materially worsen the measurements.

The numerical limits above are MVP control limits, not production
specifications. Record the raw measurements so they can be tightened only when
the ring-support stack shows what it actually needs.

Do not substitute printed screws, printed nuts, or improvised pins if the
claim is that the frozen joinery works. If the small hardware is unavailable,
the result may establish print warp and gross closure only; it cannot pass the
joinery gate.

### MVP-2 — one full ring on one role's three supports, rim-pushed

After MVP-1 passes, add:

- one complete two-half, 260-tooth moving ring, preferably the hour role
  because its larger fin envelope is the more demanding mechanical article;
- the three support locations and the rollers/axles needed for that role;
- no pinion, motor, miter gears, Hall parts, or other rings.

One failure question:

> Does one real segmented ring remain captured and turn through 360 degrees in
> both directions under gravity, including both seams, without a drive mesh
> hiding a guidance problem?

Physical acceptance:

- ten slow rim-pushed revolutions in each direction with no bind, derailment,
  tooth/race damage, roller lift, or manual reseating;
- both seams pass all three support stations in both directions;
- installed radial TIR is at most 0.20 mm, matching the existing hard maximum;
- axial lift and sag are measured at the three stations and at the midpoint
  between stations; neither causes contact with a foreign surface;
- the ring remains captured when the base is vertical and after direction
  reversal at each seam;
- removal and reinstall produces comparable runout rather than a one-time
  lucky adjustment.

Use the intended bearings and axles before making friction or torque claims. A
printed sacrificial roller is acceptable only for checking gross geometry and
retention, and the report must say so.

### MVP-3 — the same ring with a base-mounted manual pinion

Reuse MVP-2 and add one 16T, module-1 pinion on a rigid base-mounted hand knob
or shaft. Bypass the motor and miter stage.

One failure question:

> Does the real tooth train drive through every tooth and both ring seams,
> forward and reverse, without climb, skip, jam, or a seam torque spike?

Physical acceptance:

- ten pinion-driven ring revolutions in each direction;
- reversal at each ring seam and at least four away-from-seam positions causes
  no skipped tooth or roller escape;
- both seams pass the pinion in both directions without tooth climb or visible
  separation;
- peak seam-zone hand force is no more than 1.5 times the median force measured
  over an equal away-from-seam arc; record force versus angle rather than using
  feel alone;
- backlash is measured at the pinion and at the ring, and is repeatable after
  removal/reinstall;
- teeth show no whitening, chipping, burr growth, or layer separation.

This proves geometric mesh and seam passage only. A hand drive can slow down,
change angle, and add force unconsciously; it cannot prove motor torque,
speed, endplay, noise, wear, or control behavior.

### MVP-4 — three-ring passive stack

Only after MVP-1 through MVP-3 pass, add the other two rings and all nine roller
contacts. Still omit motors and miter gears. Rim-push each ring independently;
the proven manual pinion may be moved between roles if its mount preserves the
intended center distance.

One failure question:

> Do all three printed tolerance stacks coexist and allow independent 360
> degree motion without cross-role contact, accumulated sag, or capture loss?

Physical acceptance:

- each ring completes five turns in both directions while the other two are
  parked at deliberately worst seam/fin orientations;
- every seam passes every relevant support and the role's pinion station;
- no ring, fin, join, fastener, roller, or fixed structure contacts a foreign
  role;
- each role remains within 0.20 mm radial TIR after the full stack is installed;
- vertical dwell for 24 hours creates no permanent sag, seam opening, roller
  migration, or loss of independent motion;
- removing and reinstalling one role does not require disturbing the base
  joints or reworking another ring.

MVP-4 is the last hard-mechanics gate before procuring or designing the drive
system.

## Assumptions that need challenging

### Four base quadrants

The base architecture is not merely “four parts fit.” It is an overconstrained
closed loop: eight bridge locations and eight press/slip dowel pairs must all
agree after four large FDM parts warp independently. Tightening screws on a
flat jig can conceal stored stress and can make the assembly look flat only
while constrained. The last seam, free-state flatness, vertical dwell, and
repeat assembly are therefore the decisive observations.

The present base joint also requires 52 items when quadrants, bridges, screws,
nuts, and dowels are counted. That may still be acceptable, but it is a warning
that joinery complexity—not motors—is currently the MVP risk. If MVP-1 fails,
first reconsider constraint count and adjustability rather than tuning every
nominal clearance independently.

### Ring segmentation

The moving-ring design is currently two 130-tooth halves, while the stationary
base is four quadrants. Do not let “four base plates” silently become “four
moving ring quadrants.” A full ring is the minimum useful ring specimen. An
arc coupon cannot reveal closure error, installed runout, gravity sag, or seam
passage at all support locations.

### Roller guidance

Three support locations can define a circle, but three rigidly fixed contact
conditions can also overconstrain a warped ring. The design needs an explicit
answer to which support establishes radius, which establishes axial position,
and where manufacturing error is absorbed. If all three are intended to
preload the ring, define and measure that preload. If one tower is adjustable,
MVP-2 must establish a repeatable setup procedure rather than accepting a
single tuned success.

CAD contact and a printed substitute roller do not prove MR84 fit, friction,
axle retention, roller concentricity, or vertical capture. Those are physical
claims.

### Manual pinion

A hand pinion is valuable only after rim-pushed guidance passes. Otherwise a
bind cannot be attributed to guidance or gear mesh. It must be mounted at the
intended center distance; holding a loose pinion by hand is not evidence. It
does not validate the motor, miter pair, shaft stack, bearing endplay, or
continuous-speed dynamics.

## Compact evidence matrix

| Risk / gate | CAD-verifiable evidence | Slicer-verifiable evidence | Print-only evidence |
|---|---|---|---|
| MVP-1 base closure | Four valid quadrants; actual bridge/nut/dowel solids; accessible assembly paths; no unintended assembled interference; tower datums restored | Every part plus real brim/support/skirt fits; correct orientation; critical walls and holes produce toolpaths | Last-seam closure, insertion force, free-state flatness, loop error, rigidity, creep, wear, repeat assembly |
| MVP-2 ring join | Two 130T halves reconstruct one 260T ring; tooth phase and seam envelopes; valid solids | Each half fits with adhesion features; seam, race, teeth, and fin are actually sliced | Joint strength, seam step, TIR, sag, balance, dimensional drift |
| MVP-2 roller guidance | Own-role clearances/contact intent over a targeted 360-degree sweep; capture geometry | Tower/roller features, bores, seats, and retaining lips survive slicing | Bearing/axle fit, friction, preload, roller runout, derailment, vertical behavior |
| MVP-3 manual pinion | 16T/module-1 geometry, center distance, own-role Z, tooth/seam sweep | Tooth tips, root gaps, shaft bore, and mount produce toolpaths | Hand force, backlash, tooth climb, skip, seam impulse, wear |
| MVP-4 three-ring stack | Axial ordering and foreign-role clearance at targeted event states | All required parts have viable plates and orientations | Cumulative tolerance, cross-role rubbing, service access, long-dwell sag, independent motion |

No row can be promoted from CAD or slicer PASS to physical PASS. Slicer preview
can show that geometry will be attempted; it cannot show the resulting fit.

## Lean automated test contract

Keep each prototype at fewer than 15 high-value automated tests. A test may
iterate a deliberately selected event matrix, but it must answer one named
failure question. Every positive check must include a controlled negative
mutation that the check rejects; otherwise it has not demonstrated sensitivity.

### MVP-1: seven tests

1. Exact article selection: four chassis quadrants and eight bridges only.
   Negative: remove or duplicate one occurrence.
2. Each printed article is one valid positive-volume solid.
   Negative: substitute a split/disconnected bridge.
3. The assembled quadrants reconstruct the protected base outside join ROIs.
   Negative: rotate one quadrant by 0.20 degrees.
4. All non-press interfaces have positive clearance and only named press pairs
   intersect. Negative: enlarge one dowel or shrink one slip bore.
5. Nut loading, screw access, and final closure paths remain unobstructed.
   Negative: cap one loading mouth or shift a screw axis.
6. The four-seam loop restores named tower/mount datums within the MVP CAD
   tolerance. Negative: translate the final quadrant by 0.50 mm.
7. Full slicer footprints, not nominal BREP bounds, stay inside the selected
   bed and do not overlap. Negative: add a brim/support envelope that crosses
   the keepout.

### MVP-2: seven tests

1. Exactly two 130T halves produce one 260T role ring. Negative: alter one
   half's tooth count.
2. Ring reconstruction and seam tooth phase meet the 0.10 mm tangential limit.
   Negative: phase one half beyond the equivalent 0.044073-degree limit.
3. Both seam joints are valid solids with only intended contact/clearance.
   Negative: remove a lap or close its axial clearance.
4. The ring has no unintended positive-volume collision through targeted
   tooth-index positions, with extra states at both seams and all three
   supports. Negative: move one support radially inward.
5. Axial capture retains the ring while preserving running clearance.
   Negative: lift or shift the ring beyond the capture envelope.
6. The three support axes attach to restored MVP-1 datums and own only the
   selected role. Negative: assign a foreign-role roller/land.
7. Both real half footprints, including process features, slice within the bed
   and retain teeth/race/fin toolpaths. Negative: suppress a thin critical
   feature or exceed the bed keepout.

### MVP-3: six tests

1. The article contains one 16T module-1 pinion at the selected role Z.
   Negative: use the wrong tooth count or role plane.
2. Mount and shaft establish the intended center distance without relying on
   hand placement. Negative: offset the axis beyond adjustment range.
3. A targeted 260-index sweep includes both ring seams at the pinion and has
   no non-owned collision. Negative: introduce a tooth-phase error at one seam.
4. Forward and reverse mesh envelopes preserve backlash without tooth escape.
   Negative: close center distance until backlash disappears.
5. The hand knob/shaft and fastener tool paths clear the base and ring.
   Negative: block one removal or driver path.
6. Slicer preview retains pinion teeth, root gaps, bore, and mount walls.
   Negative: use a profile that drops a named feature.

### MVP-4: six tests

1. Exact article selection: three rings, three role planes, and nine role
   roller contacts. Negative: omit or cross-assign one contact.
2. Axial order and minimum foreign-role clearances are measured from actual
   solids. Negative: shift one ring 0.50 mm in Z.
3. Each role sweeps targeted tooth-index and seam/support/pinion events while
   the other roles occupy named worst-case positions. Negative: inject a known
   foreign-role collision.
4. Every fin clears fixed structure and other roles at event-derived relative
   angles. Negative: extend or rotate one fin into a protected envelope.
5. All support loads resolve into MVP-1 datums without floating or disconnected
   solids. Negative: disconnect one tower support.
6. All printable articles retain critical slicer paths and fit the planned
   plates. Negative: enable a process envelope that causes collision or bed
   escape.

Do not reinstate exhaustive release parity, silhouette, serializer, manifest,
or hundreds-of-thousands-of-states checks as prerequisites to these MVP
prints. Retain a small source-to-output identity check and actual-solid checks,
then spend the validation budget on physical observations that software cannot
make.

## Explicitly deferred

Until MVP-4 passes, defer:

- motors, motor choice, drivers, wiring, control software, and synchronization;
- miter gears, powered shaft stacks, speed/endurance/noise/temperature testing;
- Hall sensors, magnets, homing, balance correction, and electronics pockets;
- optical validation, LEDs, shadow quality, front cosmetics, and enclosure work;
- production three-motor duplication and complete purchased-hardware BOM;
- release-grade 275-occurrence parity, canonical archive details, silhouette
  proofs, complete 3MF packaging, and 189,540-state motion certification;
- tuning all three ring roles before one worst-case role passes;
- printing the stationary frame and outer front optical-ring quadrants before
  the rear-base joinery has passed.

Preserve the existing design as a hypothesis, not as a production commitment.
The result of each print gate should decide the smallest next CAD change.

## Test record required at each gate

Record material, printer, nozzle, layer height, orientation, slicer profile,
part revision/hash, purchased hardware measurements, assembly order, raw
measurements, photos/video of the named failure event, and PASS/RED. A PASS
without the raw measurement or a RED without the failure location is not
actionable evidence.

