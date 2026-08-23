# KAGE P2R3 Module A — quartz driver validation

This isolated revision replaces P2R2's three manual driver rings with a stock
quartz movement and three direct shaft-driven magnet arms.  It implements only
the clock/driver half of the mechanism.  The inset-rail magnetic follower plate
is a separate Module B and is intentionally absent.

## Important movement limitation

`MH011` and `HR1688` are purchasing candidates, not verified CAD inputs.
step.parts was searched for the exact names, aliases, `clock movement`, and
`quartz motor`; no matching model was available.  The grey 56 × 56 × 16.2 mm
case and its 5.0 / 3.25 / 0.75 mm concentric shafts are labeled
`PROVISIONAL_NONPRINTABLE` in STEP.  Do not print them and do not infer universal
quartz compatibility from this model.

Measure the purchased movement, print the coupon ladders, then set the named
parameters in `p2r3_quartz_driver_module_spec.py` before producing final hubs.

## Architecture

1. A 70 mm printed panel is captured by the movement's threaded shaft and nut.
2. Three 0.8 mm arms attach directly to the hour, minute and second shafts.
3. A Ø6.15 × 3.10 mm pocket retains one Ø6 × 3 mm driver magnet behind a
   0.10 mm recessed face; a 0.80 mm printed floor prevents push-through.
4. Each opposite tail accepts a removable 12 × 28 × 2 mm C-channel cup.  It
   snaps over the 0.8 mm arm, has 0.40 mm Y and 0.20 mm Z clearance per side,
   and is captured between integral widened stops over 6 mm of adjustment.
5. Compact arms use 32 / 51 / 70 mm magnet radii.  The full second torque wand
   uses the final 135 mm magnet radius and a 75 mm counterweight radius.

The compact aligned reference pose is 129.3 × 70.0 × 32.7 mm.  The complete
rotating envelope from live BREP vertices is 149.0 mm, including magnet boss,
counterweight stops and cup.  The cup Z corridors are hour -6.3..-4.3, minute
-3.5..-1.5 and second -0.9..1.1 mm.  The second arm's counterweight tail uses
a localized +0.5 mm axial jog while its hub and magnet arm remain on the frozen
shaft plane.  The nominal 0.8/0.6 mm cup gaps retain at
least 0.4/0.2 mm when adjacent cups take opposite worst-case +/-0.20 mm axial
float.  Exhaustive one-degree checks cover all 360 relative angles for every
cross-channel arm/cup and cup/cup pair in both validation and production
geometry, including every axial-float corner.

The production counterweight starting fills are computed from live PETG arm and
cup volumes and mass centroids at 1.27 g/cm³, plus the 0.636 g tip magnet.  They
are 1.0562 g hour, 0.5557 g minute and 1.2120 g second before physical tuning.

Each cup has two 10 × 9.5 × 1.2 mm ballast wells, 0.228 cm³ total.  The declared
prototype fill is TP7 tungsten-polymer putty; its vendor reports measured
7.2–7.4 g/cm³, so the conservative capacity is 1.6416 g.  That exceeds every
ideal fill by at least 20%.  Product reference:
https://derbydust.com/products/tp7-tungsten-putty.  Density is documented;
nonmagnetic behavior is still a physical gate—reject any batch showing visible
attraction to a Ø6 × 3 mm driver magnet at 5 mm.

## Files

- `p2r3_compact_reference_assembly.step`: printed mount/arms/cups plus the
  clearly labeled nonprintable movement envelope.
- `p2r3_fit_coupon_ladders.step`: movement, hour, minute and second fit ladders.
- `p2r3_second_r135_torque_wand.step`: full-radius second arm and adjustable cup.
- `p2r3_quartz_mount.step`: printed movement panel only.
- `p2r3_state_060000.step` and `p2r3_state_120030.step`: former dynamic-failure
  clock states, retained as review/snapshot regressions.
- `print/p2r3_module_a_compact_validation.3mf`: eleven printable objects; no
  provisional movement geometry.
- `print/p2r3_second_r135_torque_wand.3mf`: wand, second cup and second hub coupon.
- `print/*.stl`: each printable object as a separate, bed-normalized mesh.

## Assembly order

1. Print the four coupon ladders first.  Test each bore against the exact
   purchased shaft without forcing it.
2. Update the selected hub bores in the named spec.  Regenerate the arms.
3. Mount the quartz movement behind the 70 mm panel with its stock washer/nut.
4. Press one magnet into each arm pocket with identical wall-facing polarity.
5. Snap an empty printed counterweight cup over the opposite tail between the
   two widened stops; verify it cannot pass either stop but slides through the
   full 6 mm adjustment range.
6. Install hour, then minute, then second arm at their stock shaft heights.
7. Add nonmagnetic mass to each cup and move the cup until the arm does not
   self-rotate under gravity.

The compact arms are fit/drive tests.  The r135 second wand is the torque gate;
do not build Module B until it passes the physical plan.
