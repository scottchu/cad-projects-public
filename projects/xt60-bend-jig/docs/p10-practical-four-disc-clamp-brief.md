# P10 — practical four-disc / three-rod clamp

P10 preserves P9's four-disc cam mechanism and turns it into a practical
soldering fixture. It clamps a **manually pre-bent 90 degree XT60 pigtail**; it
does not claim to bend a straight wire automatically. P9 remains unchanged as
the motion proof.

## Workflow

1. Clamp the shared base beside the bottom ESC with all three rods open.
2. Slide the one-piece locator into the base from +X. Its base key, ESC-edge
   tab, wire shelves, and one lateral fence place the insulation ends at the
   pad leading edge and the stripped conductors across the pad centers. Seat
   the connected pigtail toward +X against the right fence.
3. Turn the removable thumbwheel. Both cams move all three rods together.
4. At the exact 80 degree hard stop, translate the lock pin `20 mm` toward -X
   from its axial parking pose into the aligned bores. Slide the locator first
   `46 mm` toward +X to disengage it, then continue to its named `+80 mm`
   parking pose. The rods nominally locate the 90 degree path.
5. Solder and cool the horizontal wire ends with the locator absent.
6. Translate the lock pin `20 mm` toward +X back to its axial parking pose,
   then reopen the rods.
7. Remove the three right keepers `6 mm` toward -Y, then withdraw all three rods
   `55 mm` toward -X with their left caps attached.
8. Release the bench clamp, translate the remaining plate/base assembly
   `80 mm` toward -Y, and lift it away.

Actual unsupported wire retention after step 4 is a physical acceptance test,
not a CAD claim.

## Frozen mechanism

- Exactly three purchased `4.0 x 50.0 mm` 304 stainless rods.
- Exactly four principal circular plates: one fixed guide and one rotating cam
  per side.
- Preserve P9's `64.0 mm` disc diameter, shaft datum, closed rod endpoints,
  common `11.0 mm` travel, `0..70 degree` closing law, `70..80 degree` dwell,
  and exact 90 degree forming endpoint. Any endpoint change requires a revised
  brief and renewed geometry audit.
- Cam thickness is `3.0 mm`; fixed-disc thickness is `3.0 mm`; axial running
  gap is `0.30 mm`; guide/cam slots remain `4.4 mm`.
- Retain one `3.0 mm` closed-position lock pin. Do not add gears, linkages, a
  cage, towers, large walls, or an enclosure.

## Exact endpoint and hard stop

- At the hard stop, horizontal and vertical forming datums are
  `90.0 degrees +/-0.1 degree`; shaft/cam angle is
  `80.0 degrees +/-0.1 degree`; every rod center is within `0.02 mm` of its
  frozen P9 closed endpoint; upright/bottom contact tangents are orthogonal;
  and the lock pin aligns without moving the cams.
- The hard stop is integral and adds no printed parts. Each cam has a radial
  tab spanning radius `31..36 mm`, tangent width `3.0 mm`, and full cam
  thickness. Each fixed disc has an integral support arm at world polar angle
  `85.042451 degrees`, spanning radius `30.5..34.2 mm`, tangent width `3.0 mm`,
  plus an integral `3.0 mm` diameter stop pin centered at
  `(Y,Z)=(-4.5503852184,66.5044081354) mm`. Pin X spans are
  `18.0..22.8 mm` right and `-22.8..-18.0 mm` left. The exact tab dimensions
  and pin-center coordinates come from authoritative cam-local
  `(radial,tangent)=(34.0,3.0) mm` rotated by 80 degrees about the shaft. The
  arm angle is `80 + atan2(3,34) = 85.0424510692 degrees`; pin radius is
  `34.1320963 mm`. Source computes these values rather than copying rounded
  decimals. Cam-tab and arm root sections are each `>=9.0 mm2`.
- Stop faces touch without BREP overlap at 80 degrees. The stop prevents any
  allowed state above 80 degrees. Rods, wire, and lock pin are not hard stops.
- The wheel index is local `+10 degrees` from +Y toward +Z, making it exactly
  vertical/straight (world +90 degrees) at the 80 degree stop.
- The wheel has one integral open rim notch: a `6.30 mm` diameter through-cut
  centered at radius `15.50 mm` in the P9 local lock direction
  (`200.0 degrees`). It clears the `5.50 mm` lock-pin head with `0.40 mm`
  radial clearance and opens through the `16.0 mm` wheel radius.

## Workpiece contact

- Open, intermediate, and closed checks use the same fixed, pre-bent L-shaped
  pigtail; never substitute a straight open wire or fake elastic interpolation.
- Define `c_i(theta)` as rod-to-wire surface clearance. Require
  `c_i > 0.30 mm` before `theta=63.09485 degrees`; from there to dwell allow
  declared contact-band proximity but still require zero solid overlap.
- At `70..80 degrees`, tangency residual is `<=0.02 mm`. Contact bands are:
  upright `Y=0, Z=42 +/-0.5 mm`; bottom `Y=12 +/-0.5, Z=30 mm`; diagonal
  arc-length `+/-0.5 mm` around `(Y,Z)=(1.75736,31.75736) mm` on the R6 bend.
- The locator supports the pigtail before first rod contact. Horizontal wire
  endpoints stay aligned to the bottom ESC pads; XT60 remains vertical.

## Shared base and fixed-disc datums

- Base is one `44 x 22 x 8 mm` solid centered at
  `(X,Y,Z)=(0,-7.5,-4.5)`, top `Z=-0.5`, with a centered
  `24 x 18 mm` clamp land.
- Each fixed disc has an integral `3.0 x 14.0 x 4.0 mm` engaged downward tongue
  spanning `Z=-4.5..-0.5 mm`, plus an integral root extension to `Z=-0.25 mm`
  for `0.25 mm` volumetric fusion above the base top. It is centered at
  `X=+/-17.5, Y=-7.5 mm`. Left mortise spans
  `X=-19.25..-16.00`; right spans `X=16.00..19.25`; both span
  `Y=-14.80..-0.50, Z=-4.70..-0.50 mm`.
- Inboard X walls set separation and +Y walls set racking. Two fixed-disc
  shoulders spanning `Z=-0.5..2.2 mm` set Z/clocking. The negative-Y shoulder
  is `3.0 mm` X by `2.55 mm` Y by `2.70 mm` Z and spans
  `Y=-16.8..-14.25 mm`; the positive-Y shoulder is `3.0 mm` X by `2.25 mm` Y
  by `2.70 mm` Z and spans `Y=-0.75..1.5 mm`.
  Each overlaps the tongue root by `0.25 mm` in Y and Z, overlaps the circular
  disc volumetrically, and leaves exactly `2.00 mm` exposed base land
  (`6.00 mm2`). Loaded center separation is exactly `35.0 mm`.
- Each tongue has four integral sacrificial triangular crush ribs with
  30-degree insertion leads. Two on the outboard X face are `0.35 mm` proud,
  `0.80 mm` wide in Y, `2.50 mm` high, centered at `Y=-11,-4 mm`; they create
  `0.10 mm` nominal interference and bias toward the inboard datum. Two on the
  rear -Y face are `0.40 mm` proud, `0.60 mm` wide in X, `2.50 mm` high,
  centered at local `X=+/-0.75 mm`; they create `0.10 mm` nominal interference
  and bias toward +Y. The crushed/seated CAD envelope has zero overlap.
- Both rib types span `Z=-3.75..-1.25 mm`. The `0.35 mm` outboard ribs have
  `0.606218 mm` 30-degree lead length and a full-proud plateau over
  `Z=-3.143782..-1.856218 mm`. The `0.40 mm` rear ribs have `0.692820 mm` lead
  length and a plateau over `Z=-3.057180..-1.942820 mm`.
- Without ribs, translation bounds are `0.25 mm` X and `0.30 mm` Y. Exact
  unloaded rotation bounds are: Z yaw `1.02515884 degrees`, X clock/roll
  `0.82021652 degrees`, and Y pitch `3.67170423 degrees`, from the corresponding
  rotated-rectangle extent equations. Printed crush, seating force, and
  repeatability remain physical tests. The joint is dry-removable with no glue
  or hardware.

## Locator and complete datum chain

- The one-piece open-sided locator establishes
  `base -> fixed discs -> rods -> locator -> pigtail -> ESC` and installs from
  +X by sliding -X.
- Base transverse T-cavity runs through X. Main cavity is
  `46 x 2.30 x 3.30 mm` centered at `(0,1.60,-4.50)`; neck/opening is
  `46 x 1.50 x 1.80 mm` centered at `(0,3.00,-3.40)`. Cavity minimum Y is
  `0.45 mm`, leaving `0.95 mm` to the mortises ending at `Y=-0.50 mm`.
- In its gravity/+Y seated state, the locator rail is
  `44.90 x 2.00 x 3.00 mm` centered at `(-0.25,1.75,-4.65)`, spanning
  `X=-22.7..22.2`; its `44.90 x 1.20 x 1.50 mm` neck is centered at
  `(-0.25,3.00,-3.40)`, spanning `Y=2.4..3.6, Z=-4.15..-2.65 mm`.
  Rail bottom seats at `Z=-6.15 mm`; the main rail +Y face seats at
  `Y=2.75 mm`. The nominal neck cutter is clipped by the base outer face at
  `Y=3.5 mm`, so it is an open slot with no +Y neck wall. The neck has
  `0.15 mm` clearance to both Z faces and creates no second gravity datum.
- A `2 x 3 x 4 mm` insertion shoulder centered at `(23,2,-4.5)` contacts the
  base right face at `X=22`. A rear rail wedge over `X=16..22 mm` ramps for
  `4 mm`, plateaus for `2 mm`, is `0.35 mm` proud toward -Y and `0.80 mm` high
  in Z. Against `0.30 mm` rear clearance it gives `0.05 mm` nominal crush,
  biases +Y, and friction-preloads the X shoulder. Loaded CAD X play is zero;
  physical movement under `+/-1 N` must be `<=0.10 mm`.
- The wedge spans `Z=-5.05..-4.25 mm`; its X ramp is `16..20 mm` and plateau
  is `20..22 mm`. Raw rear Y is `0.40 mm` for `0.05 mm` interference; the
  compressed seated-envelope rear Y is `0.45 mm`.
- Rail and insertion shoulder overlap `0.20 mm` in X. The connected load path
  comprises two `2.5 x 21.2 x 3.0 mm` runners centered at
  `X=+/-8.5, Y=14.1, Z=-2.3`, starting at `Y=3.5 mm` and overlapping the neck
  by `0.10 mm`; two `2.5 x 2.65 x 28.6 mm` lower posts at
  `X=+/-8.5, Y=25.675, Z=10.5`; two `2.5 x 1.0 x 3.15 mm` upper necks at
  `X=+/-8.5, Y=25.45, Z=26.275`; and one `19.5 x 1.0 x 2.2 mm` bridge centered
  at `(0,25.45,26.65) mm`.
- Two `4.6 x 1.0 x 1.2 mm` shelves centered at
  `X=+/-4, Y=25.45, Z=27.25 mm` have exact top `Z=27.85 mm` and tangentially
  support the `4.3 mm` wire envelopes centered at `X=+/-4, Z=30 mm`.
- One right fence has bounding box `X=6.15..7.15, Y=25.2..26.2,
  Z=27.65..30.40 mm`. Its inner face at `X=6.15 mm` is the one-sided +X wire
  datum and contacts the right wire's nominal `X=6.15 mm` outer surface over
  `Y=25.2..26.2 mm`. It overlaps the right shelf by `0.15 mm` in X and `0.20 mm`
  in Z so the locator remains one solid. The user seats the connected pigtail
  toward +X against this fence. No left fence is allowed because it would cross
  a wire during withdrawal. With the assumed XT60 cup spacing, nominal wire
  center X positions are exact; physical repeated-loading endpoint error must
  remain `<=0.25 mm`.
- One right-only `2.5 x 2.2 x 3.0 mm` ESC tab centered at
  `(8.5,26.9,25.8) mm` contacts the leading PCB edge at `Y=28.0 mm`.
  Reference pad centers are `X=+/-4, Y=30.5 mm`, pad top is `Z=27.85 mm`.
  `X=+/-4, Y=28.0, Z=30.0 mm` is the insulation-end/solder-entry datum, not the
  pad center. Each modeled stripped/tinned conductor is `2.30 mm` diameter and
  `5.0 mm` long, spans `Y=28.0..33.0 mm`, and is centered over its pad at
  `Y=30.5 mm`, providing `5.0 mm` solderable pad overlap. Solder-entry planar
  error and conductor-to-pad-center planar error are each `<=0.25 mm`; insulated
  wire underside-to-pad-top error is `<=0.10 mm`.
- A connected `12.5 x 2.65 x 6.0 mm` grip centered at
  `(15.75,25.675,16.0) mm` is included in every sweep.
- Shelf top is dimensioned `34.00 mm` from the seated rail bottom, so key
  clearance cannot change loaded height. Physical shelf top is
  `27.85 +/-0.10 mm`.
- Accepted disengagement is pure +X by `46 mm`, leaving locator minimum X
  `23.3 mm`, at least `1.3 mm` beyond the base. It then continues on the same
  axis to a named `+80 mm` parking pose, where locator minimum X is
  `57.3 mm`. The parked locator remains present in all later collision sets.
  Pure +Y is an expected-failure regression because the under-wire support
  necessarily intersects the ESC.

## Shaft, wheel, and retainers

- Shaft is `6.00 mm` across corners; fixed-disc running bore is `6.50 mm`.
  Cam/wheel socket is provisionally `6.25 mm` and must be chosen using the fit
  coupon.
- Integral right shaft collar is `9.0 mm` diameter and spans
  `X=22.45..24.50 mm`. It is the unique right-side stop that limits shaft
  travel toward -X, with `0.15 mm` right-cam clearance.
- The functional left reduced neck is circular `5.20 mm` diameter over
  `X=-25.70..-22.30 mm`; its solid core continues to `X=-22.20 mm` for
  `0.10 mm` volumetric overlap with the full AC6 main shaft beginning at
  `X=-22.30 mm`. A removable `3.0 mm` C-keeper spans
  `X=-25.50..-22.50 mm`, with `5.4 mm` pocket and `4.7 mm` throat. The terminal
  `6.00 mm` across-corner shoulder spans `X=-27.20..-25.60 mm`, overlapping the
  neck by `0.10 mm`.
- The left cam has an integral `10.0 mm` OD annular thrust boss with the
  `6.25 mm` across-corner socket cut through. Its functional projection spans
  `X=-22.50..-22.30 mm`; its solid root continues to `X=-22.25 mm` for
  `0.05 mm` volumetric overlap with the cam. Minimum boss radial wall is
  `1.875 mm`. The 3.0 mm keeper floats axially between this stationary thrust
  face and the moving terminal shoulder; it is not assumed fixed to the shaft.
- Exact axial sequence: -X travel is clear until the collar contacts the right
  cam at `-0.15 mm`; the main-hex/keeper gap is still `0.05 mm`. +X travel is
  clear until the terminal shoulder, floating keeper, and boss close their
  total `0.10 mm` free stack gap at `+0.10 mm`, independent of the keeper's
  initial axial position.
  Positive overlap appears `0.001 mm` beyond either stop. Total peak-to-peak
  shaft float is `0.25 mm`.
- Removable wheel spans `X=26..32 mm`; its blind `6.25 mm` across-corner socket
  is `5.8 mm` deep. Shaft engagement is `>=5.6 mm` with `0.20 mm` blind-end
  clearance. Two opposite integral socket ribs are `0.15 mm` high,
  `0.80 mm` wide, and `4.0 mm` long. Target wheel pull-off `3..10 N` is a
  physical coupon test.
- The press-fit wheel and shaft are one coupled moving body for axial checks;
  the wheel translates with the shaft and retains `>=5.6 mm` relative keyed
  engagement throughout the permitted float.
- The lengthened lock pin has a `3.0 mm` diameter shaft spanning
  `X=15..33 mm` when engaged and a `5.50 mm` diameter head spanning
  `X=33..35 mm`, leaving its head fully beyond the wheel with `1.0 mm` axial
  clearance. Engaged insertion is a pure `-X 20 mm` translation through the
  aligned fixed/cam bores and wheel notch. Removal is `+X 20 mm`; the parked
  pin spans `X=35..55 mm` and remains present in every later collision set.
- P10 retainers use `0.20 mm` axial float and do not reuse P9's `0.30 mm` axial
  placement. Right keeper spans `X=22.5..25.4 mm`, with `4.10 mm` pocket and
  `3.60 mm` +Y-facing throat. It must clear the rod after `6 mm` travel toward
  -Y; exploded view shows `8 mm`. Left cap keeps the `3.90 mm` trial bore.
  Rod engagement is `>=2.50 mm` at both ends.

## Named minimum geometry

- Cam inter-slot web `>=2.00 mm`; cam outer rim `>=3.40 mm`; left-cam keyed
  engagement is `3.00 mm` nominal and `>=2.90 mm` throughout permitted axial
  float; right-cam engagement is `>=3.00 mm`.
- Wheel keyed engagement `>=5.60 mm`; wheel hub radial wall `>=2.875 mm`.
- Shaft collar radial section `>=1.50 mm`; C-keeper radial web `>=2.30 mm`.
- Base floor below mortises `>=3.80 mm`; outer X wall `>=2.75 mm`; rear Y wall
  `>=3.70 mm`; gross front wall away from T-key `>=4.00 mm`; local
  mortise-to-T-cavity ligament `>=0.95 mm`; T-main top/bottom ligaments
  `>=2.35 mm`; T-neck top ligament `>=2.00 mm`; shoulder land `>=2.0 mm` Y and
  `>=6.0 mm2` each. These are geometry limits, not stiffness claims.

## Soldering and removal

- Keep P9 orientation: power ESC below FC. Locked-state solder corridor must
  have zero intersection with printed parts after locator removal.
- Locator withdrawal collision set is: base; four complete plates including
  stop features; three rods; six rod retainers; shaft; shaft keeper; wheel;
  lock pin; ESC/FC/pads/solder; pigtail; and XT60. An exact rigid-translation
  swept-volume BREP must have intersection `<=1e-6 mm3` with every stationary
  member. At least 181 off-grid positions remain as regression visualization.
  Minimum clearance to every principal disc is `>=0.75 mm`.
- The exact locator swept-volume proof continues through the full `+80 mm`
  parking translation. Later phases include the locator at that named pose.
- Lock-pin insertion/removal swept volumes include the wheel/notch, complete
  plates and bores, base, shaft/keeper, rods/retainers, locator, electronics,
  pigtail, and XT60. Exempt only intended passage through aligned bores/notch.
  Engaged wheel/pin overlap is zero and plate engagement is positive.
- Intact-jig -Y removal is an expected-failure regression. Accepted post-solder
  removal is: reopen; sweep each right keeper separately `6 mm` toward -Y;
  pull all rods/caps `55 mm` toward -X; translate the remaining
  base/plates/shaft `80 mm` toward -Y.
- Each right-keeper removal checks its exact swept volume against base, complete
  plates, wheel, shaft/keeper, all rods, the other five retainers, electronics,
  pigtail, XT60, parked pin, and parked locator. Exempt only the declared
  elastic throat/rod snap interval.
- Each rod/left-cap withdrawal checks its exact swept volume against base,
  complete plates, shaft/keeper, wheel, parked pin, parked locator, electronics,
  pigtail, XT60, the other rods/caps, and all removed keepers still present in
  the modeled workspace. Exempt only the intended rod/left-cap press interface.
- Final -Y translation moves base, four complete plates, shaft, shaft keeper,
  and wheel. Its exact swept volume is checked against electronics, pigtail,
  XT60, parked pin, parked locator, withdrawn rods/caps, and removed keepers.
  A part may be omitted only if
  its modeled prior phase explicitly moves it to a named parking pose outside
  this workspace.

## Artifacts

- Source: `src/xt60_bend_jig/p10_practical_four_disc_clamp.py`
- Tests: `tests/test_p10_practical_four_disc_clamp.py`
- Generated STEP entrypoints under `cad/p10_practical_four_disc_clamp/`:
  `p10_loaded_open`, `p10_loaded_closed`, `p10_locator_removed_closed`,
  `p10_rods_withdrawn`, `p10_removal_clear`, `p10_exploded`, `p10_print_kit`,
  and `p10_fit_coupon`.
- The fit ladder has across-corner sockets `6.15`, `6.25`, and `6.35 mm`, each
  through a `6.0 mm` thick ladder in the same print orientation as the
  cam/wheel sockets. The separate male plug is `6.00 mm` across corners, uses
  the same print orientation, and has two readable depth marks at `3.0 mm` for
  cam-fit evaluation and `5.6 mm` for wheel-engagement evaluation.
- Print kit contains exactly 18 printed solids: two fixed discs with integral
  arms/pins/ribs; two cams with integral tabs; base; locator; shaft; wheel;
  shaft C-keeper; lock pin; three left caps; three right keepers; one
  three-socket fit ladder; and one separate `6.00 mm` male plug. Purchased rods
  and electronics are excluded.
- Principal plates use side-specific bed orientations so outboard features face
  upward: left fixed disc and left cam use `Rot(0,+90,0)`; right fixed disc and
  right cam use `Rot(0,-90,0)`. Thus each inboard full disc face—not the left
  cam's thrust boss or a fixed-disc stop pin—is the Z=0 bed-contact datum.

## CAD acceptance

- P9 source/artifacts remain unchanged; exactly three purchased rods and four
  principal plates remain.
- Same fixed L workpiece at every pose; dense motion checks prove the named
  pre-contact clearance, zero overlap, contact bands, and final tangencies.
- Stop tests prove each cam+tab and fixed-disc+arm+pin is one solid, zero overlap
  through `79.99 degrees`, contact at 80, positive overlap at 80.01, at least
  `0.09 mm3` overlap at 80.1, body clearance `>=0.60 mm`, and no extra part.
- Base tests prove raw rib interference `0.10 mm`, zero-overlap crushed envelope,
  datum-face contact, named unloaded play, exact loaded transforms, and
  `35.0 mm` disc-center separation.
- Fixed-disc core tests prove one solid before ribs/tools, tongue/shoulder
  common volume `>=0.187 mm3`, disc/shoulder common volume `>=4.78 mm3`, each
  exposed land `>=2.0 mm` Y and `>=6.0 mm2`, base overlap zero, and base
  distance zero. Exact extent equations reproduce all three named rotation
  bounds.
- Direct bounding-box tests freeze mortise-rib and locator-wedge extents. Raw
  intersections equal only their named masks; seated envelopes remove only
  those masks.
- The print kit and exploded view use named `as_printed` fixed discs, wheel,
  and locator with undeformed crush/socket/wedge ribs. Loaded and swept
  assemblies use a named `seated_envelope` in which only the declared
  interference volume is trimmed. The as-printed locator proves `0.05 mm` raw
  wedge interference; its seated envelope has zero base overlap. All non-rib
  geometry, transforms, and part labels must match. Generic overlap assertions
  exempt only the named raw rib/wedge interference regions.
- Locator tests prove one connected solid, shoulder/base contact at `X=22`,
  gravity contact at `Z=-6.15`, main-rail +Y contact, exact `34.00 mm` seated shelf
  height, datum-chain endpoint errors, `>=0.75 mm` disc clearance, and the
  collision-free +X sweep. +Y withdrawal must fail for the expected ESC hit.
- Datum tests separately prove insulation entry at the pad leading edge and the
  `5.0 mm` stripped conductor centered across each pad. Worst-case one-sided
  fence play remains inside the `0.25 mm` endpoint bound.
- Separate shaft pull checks prove the right collar contacts the right cam and
  stops -X travel, while the left terminal shoulder/keeper/left-cam stack stops
  +X travel. Cam/wheel
  engagement, wheel index, shaft float, retainer float, cap engagement, and
  keeper-removal sweeps meet named limits.
- The left thrust boss is one solid with the cam, has its named bbox and radial
  wall, and remains clear of rods/fixed disc/locator/workpiece. Tests evaluate
  the full floating-keeper interval at shaft displacements `-0.15, 0, +0.10`:
  collar touch/overlap at `-0.15/-0.150001`, worst main/keeper clearance
  `>=0.05 mm`, deterministic three-face stack touch/overlap at
  `+0.10/+0.100001`, total float `0.25 mm`, and left key engagement
  `>=2.90 mm`.
- At multiple shaft angles across `0..80 degrees`, a radial escape sweep proves
  the circular `5.20 mm` neck cannot pass through the `4.70 mm` keeper throat
  without entering the declared elastic snap interval.
- Source and exported STEP both prove endpoint angle, 80 degree shaft pose, rod
  endpoints, stop contact, lock-pin alignment, tangency, all part labels/counts,
  access/removal sweeps, and source/export parity. Tests pass fresh under
  `uv run`; mandatory snapshots are visually reviewed.
- Print-kit tests prove every principal plate has a full inboard disc-face
  footprint at Z=0 and every boss/stop-pin projection faces upward. Merely
  checking `bbox.min.Z == 0` is insufficient.
- Exact swept-volume BREP tests, not discrete samples alone, prove every rigid
  linear withdrawal/removal phase. Sampled poses remain additional regression
  and visualization evidence.
- If performance caching is used, only private immutable part prototypes may be
  cached. Every public builder returns a shallow topological copy before label,
  color, transform, boolean, or Compound use. A regression mutates 100 copies
  and proves prototype bbox, volume, label, and wrapped topology are unchanged;
  cached complete assemblies and direct mutable-shape reuse are prohibited.

## Physical acceptance boundary

CAD does not prove printed socket/keeper fit, crush-rib seating, real XT60
dimensions, wire springback, clamp load/deflection, friction, heat response, or
soldering ergonomics. Physical prototype tests must include:

- 10 fixed-disc seating cycles with repeatable datum position;
- locator movement `<=0.10 mm` under `+/-1 N` and shelf height
  `27.85 +/-0.10 mm`;
- 10 repeated pigtail loadings against the one-sided +X fence with both
  insulation-entry and conductor pad-center errors `<=0.25 mm`;
- each left cap holds `10 N` axial for 10 seconds with `<=0.20 mm` slip;
- each right keeper holds `10 N` axially and removes radially at `3..15 N`;
- rod endplay `<=0.40 mm`, 25 assembly cycles without cracks/keeper loss, and
  measured locked rod centers within `+/-0.20 mm`;
- with locator removed at soldering orientation, the pigtail remains seated
  under gravity and light soldering-iron contact;
- after solder/heat/cool, verify 90 degree retention and wire tangency.

The XT60 remains an assumed clearance envelope until measured or replaced by
an exact sourced model.
