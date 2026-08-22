# P3 V3 MVP free roller R1 retrofit contract

## Scope

R1 changes only how the accepted three-spool roller station fastens to the
already-printed canonical Q3 r0 base sectors. R0 remains untouched. Ring,
tooth, fin, spool, axle, spacer, bridge and three-station positions remain the
accepted R0 geometry.

## Lower axle socket correction

The lower axle socket remains `D4.20 mm` around the unchanged `D3.99 mm`
finished axle, and the lower post remains `D6.00 mm`. The socket now spans
`Z=-5.00 .. -2.35 mm`, a derived depth of `2.65 mm`. Its top is `0.10 mm`
above the unchanged lower-post top at `Z=-2.45 mm`, preventing a coincident
socket/post end face. No other roller-stack datum or envelope changes.

## Existing-base post-print operation

At the six existing outer mount holes (`R118 mm`, local tangent `-7/+7 mm` at
the three seams):

1. Keep the existing `D3.3 mm` through bore as the pilot.
2. Work from the flat rear face only.
3. Cut an ISO M3 `90 degree` countersink to `D6.0 mm` and `1.45 mm` target
   axial depth (`+/-0.10 mm`).
4. Deburr by hand. The M3 flat-head screw must be flush or no more than
   `0.10 mm` below the rear datum; it must never protrude behind the plate.

This is a post-print operation. R1 intentionally exports no replacement base
STEP or 3MF.

## Station fastening

- Existing base holes: `D3.3 mm`, `R118 mm`, local tangent `-7/+7 mm`.
- Station foot adjustment slots: `D3.6 x 4.1 mm`, radial direction.
- Station screw: ISO M3 x 10, 90-degree flat head, inserted from the rear.
- Station nut: ordinary metal M3, top-loaded into an open capture.
- Nut capture: `AF5.8 mm`, `2.5 mm` deep, `0.6 mm` radial elongation.
- Printed floor below each nut: `0.5 mm`.
- Nominal thread engagement through the captured nut: `2.4 mm`, minimum
  acceptance `1.0 mm`.

## Upper bridge

The accepted removable bridge is unchanged. Use ordinary metal M3 nuts and
M3 x 6 screws. No printed thread is permitted.

## Assembly sequence

1. Rear-countersink the six existing outer base holes and deburr.
2. Insert six M3 x 10 flat-head screws from the rear; verify the rear remains
   flat on a table.
3. Place each station frame over its two radial slots.
4. Drop ordinary M3 nuts into the open-top captures, adjust the station
   radially for roller contact, and tighten.
5. Assemble the accepted axle, washers, three spools and two spacers.
6. Load ordinary M3 bridge nuts, install the bridge and tighten M3 x 6 screws.

## Physical gate

CAD proves axes, envelopes and nominal clearances only. Countersink quality,
nut fit, friction, wear, free rotation and load retention require the printed
prototype.
