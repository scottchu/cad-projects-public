# P2R3 Module A physical test plan

## P0 — purchased movement identification

Record manufacturer/model, case dimensions, threaded boss diameter/length,
hour pipe OD/shape, minute pipe OD/shape, second pin OD, exposed shaft heights,
hand press direction and rated hand mass/length if supplied.  The CAD values are
provisional until this table is complete.

Pass: every fit-critical spec parameter is replaced by a measurement or a
selected coupon result.  Fail: any production arm is printed from an unmeasured
hub assumption.

## P1 — coupon ladders

Print at the intended arm process, orientation and material.  The four bore
values are:

- Movement mount: 7.8 / 8.0 / 8.2 / 8.4 mm
- Hour: 4.8 / 4.9 / 5.0 / 5.1 mm
- Minute: 3.05 / 3.15 / 3.25 / 3.35 mm
- Second: 0.55 / 0.65 / 0.75 / 0.85 mm

Each ladder also exposes 1.5 / 2.0 / 2.5 / 3.0 mm plate steps.  Mark the smallest
bore that installs without cracking and the thinnest section that does not curl
or split during removal.

Pass: one coupon per interface fits securely, is removable without shaft damage,
and repeats for three install/remove cycles.  Fail: no candidate fits, the shaft
shape is noncircular, or the 0.8 mm production arm section is not printable.

## P2 — compact three-arm movement test

Use the 32 / 51 / 70 mm arms without the magnetic follower cassette.  Run the
movement horizontal and vertical for 24 hours each.  Verify the arms never touch
at the frozen -6.1..-5.3, -2.7..-1.9 and -1.2..-0.4 mm planes.

Pass: all three shafts start reliably, complete their expected motion, and keep
time within the purchased movement's specification.  Fail: missed steps,
stalling, hub slip, visible shaft bending, or arm-to-arm contact.

## P3 — counterbalance

Install one Ø6 × 3 mm magnet at each arm tip.  Use nonmagnetic filler in the
printed cups; do not use another magnet as ballast.  Initial fill mass comes
from the live arm/cup BREP volume and centroid plus the magnet moment; the
magnet-only radius ratio is insufficient.  At PETG density 1.27 g/cm³ the
current starting fills are 1.0562 / 0.5557 / 1.2123 g for hour/minute/second.

Use TP7 tungsten-polymer putty or an equivalently documented nonmagnetic
tungsten-polymer fill.  TP7's vendor reports measured density 7.2–7.4 g/cm³;
the two wells provide 0.228 cm³ and therefore at least 1.6416 g capacity at the
lower bound.  Before filling, hold a sample 5 mm from the installed Ø6 × 3 mm
magnet.  Any visible attraction fails the batch.  Weigh the installed material;
do not infer mass from nominal pocket volume.

Use a 0.1 g scale for hour/minute and a 0.01 g scale for second.  Tune cup mass
and position until gravity does not prefer one angle.  Record cup radius, filler
mass and residual moment.

Pass: calculated residual is ≤1.0 gf·cm for hour/minute and ≤0.1 gf·cm for
second, followed by a 24-hour powered run without stall.  CAD proves only the
equation; the movement run is the authority.

## P4 — full-radius second torque wand

Install the 135 mm second wand and its captured counterweight cup at the 75 mm
radius.  The live-BREP starting filler estimate is 1.2120 g for the printed
PETG arm/cup plus a 0.636 g magnet.  Test without a
follower first, then add a stationary opposing test magnet at the planned Module
B axial gap.

The installed cup axial-float allowance is +/-0.20 mm.  The nominal hour to
minute and minute to second cup gaps are 0.80 and 0.60 mm, leaving 0.40 and
0.20 mm respectively at the opposite worst-case tolerance corners.  Reject a
printed cup/arm fit that visibly exceeds this float allowance.

Pass before Module B integration:

- starts from twelve clock angles without assistance;
- completes 24 hours without a missed tick or hub slip;
- does not permanently bend the second shaft;
- does not attract the hour/minute test arms enough to move them;
- counterweight stays captured and does not migrate.

Fail: any missed tick, lag accumulation, coupling into another shaft, shaft
deflection, or cup migration.  A failure returns to arm mass, magnet strength,
air gap or movement selection—not to rail-cassette CAD.

## Boundary

BREP and math tests verify dimensions, positive-volume solids, clearances,
counterweight equations and artifact integrity.  They cannot establish quartz
torque margin, magnetic force, long-term hub retention or print-process fit.
