# V0R1 compact representative-quartz fixture — physical test plan

## Purpose and boundary

This four-part prototype tests compact manual rotation and upright-fin shadow
geometry at a 40 mm LED-to-wall reference distance. Its body is a
representative quartz-movement envelope, not a dimensionally certified clock
movement replacement.

CAD and automated mesh checks cannot prove printed fit, torque, friction,
fatigue, runout, LED temperature, electrical safety, or visible shadow quality.
Those remain physical gates.

## Print setup

- Print the supplied four-object 3MF without scaling.
- Start with a 0.4 mm nozzle and 0.20 mm layers.
- Keep the supplied flat print orientations.
- Use ordinary PLA for the first cold optics trial; keep the powered LED and
  heatsink physically separate from printed plastic.
- Do not install the parts on a purchased quartz movement during this test.

## Gate 1 — artifact and part identity

Confirm the plate contains exactly these four separate objects:

1. `fake_standard_quartz_body`
2. `hour_carrier_hand`
3. `minute_carrier_hand`
4. `second_carrier_hand`

Fail if a part is missing, fused to another object, open, visibly split, or
scaled by the slicer.

## Gate 2 — dry assembly and retention

1. Inspect the stepped arbor and remove only loose stringing or elephant-foot
   material. Do not sand the nominal running journals before the first fit.
2. Install second, minute, then hour.
3. Verify the second and minute carriers rotate through 360 degrees without
   binding, lifting, or contacting one another.
4. Verify the hour split collet installs without cracking and is the only axial
   retainer.
5. Invert the cold assembly over a padded surface. Fail if any carrier escapes.

Record carrier rotational force, axial play, visible wobble, and whitening or
cracks around the split collet.

## Gate 3 — manual motion endurance

Rotate every carrier through 100 complete manual cycles. Fail for:

- ring, spoke, fin, or hub contact;
- increasing friction or intermittent sticking;
- a carrier climbing the arbor;
- a fin bending or separating at its root;
- split-collet cracking, permanent opening, or loss of retention.

## Gate 4 — cold optical alignment

Use an unpowered point-source marker first. Place its emitting point on the
fixture axis, 40 mm from the wall reference plane. Confirm the three upright
fins—not the carrier rings or spokes—are the intended blockers.

The target radial shadow intervals are:

| Carrier | Wall radius, root to tip |
| --- | ---: |
| Hour | 48 to 85 mm |
| Minute | 48 to 110 mm |
| Second | 48 to 130 mm |

Fail if the body, ring, spoke, or hub remains visibly exposed outside the
central mask region in the intended viewing direction.

## Gate 5 — current-limited LED trial

Only after the cold alignment passes:

1. Use a current-limited wired point LED on its specified heatsink and driver.
2. Keep the LED assembly independently supported; printed plastic is not a
   heatsink or electrical enclosure.
3. Begin at the lowest useful current and observe for one minute.
4. Check three different carrier angles, then the full 360-degree range.
5. Record shadow length, edge sharpness, spill/glare, visibility of carrier
   supports, LED/heatsink temperature, and any softening or odor from plastic.
6. Stop immediately for uncontrolled heating, flicker, exposed wiring, plastic
   deformation, or unstable support.

## Gate 6 — decision before a real clock

Pass V0R1 only if all four parts survive assembly and 100 cycles, the lower
carriers rotate freely, the hour collet retains the stack, and the three fins
produce distinct readable shadows without exposed support geometry.

Before adapting this fixture to a purchased quartz movement, independently
measure its case envelope, shaft stack, hand-interface sizes, allowable hand
mass, available torque, mounting thread, and electrical clearances. This test
does not authorize claiming compatibility with a generic or named movement.
