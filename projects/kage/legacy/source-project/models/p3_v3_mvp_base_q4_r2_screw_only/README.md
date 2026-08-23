# KAGE B0 Q4-R2 screw-only four-to-one base MVP

This isolated successor validates only the hard stationary mechanic: four
locked Q4-R1 annular quadrants closing into one 300 mm base with four new
screw-only clamps. It has no ring, roller support, pinion, motor, electronics,
LED, or future support holes.

## Printed and purchased items

Print exactly eight one-solid bodies:

- four `quadrant_Q*_front_down.step` parts, one each; these are the exact
  locked Q4-R1 quadrant BREPs;
- four `clamp_C*_bottom_down.step` parts, one each, with two fused registration
  bosses per clamp.

Purchase 8 x M3x6 ISO 4762 socket-head cap screws and 8 x ISO 4032 M3 hex
nuts. There are no dowels or pins of any kind and no loose printed locators.

The model-only 3MF contains only the eight printed bodies and no slicer
profile. It is not a production plate layout. Import one quadrant per U1 plate;
the four clamps may share a plate.

## Print orientation

- Quadrants are already front-face down at Z=0. Print with a 5 mm brim and no
  support.
- Clamps are bottom-down. Their integral bosses and open nut pockets face up.
  Print without support in the pockets or blind screw-tip reliefs.
- Use the same material, layer height, wall count, cooling, and bed preparation
  for all four quadrants.

Before the complete set, use one clamp or a small coupon to qualify the AF5.8
nut pockets and both D4.00 boss fits. A coupon does not pass B0.

## Assembly

1. Load two M3 nuts into each clamp from its open top.
2. Support all four quadrants front-face up in their final XY positions with
   every seam accessible from below.
3. Insert C1, C2, and C3 upward from below. Add one M3x6 screw through each
   adjacent quadrant and leave both screws loose.
4. Insert C4 upward from below while all four quadrants remain in final XY.
   Do not attach C4 to Q4 and lower Q4.
5. Confirm all eight screws are present and loose. Put all clamp bottoms on a
   verified plane and tighten finger-snug in C1, C3, C2, C4 order, twice.
6. Remove the base from the plane, wait one hour, and measure the free state.

## B0 physical acceptance

- OD at 0/45/90/135 degrees: 300.00 +/-0.50 mm; max minus min <=0.50 mm.
- Every seam gap: 0.05..0.30 mm, with no forced bow or overlap.
- Front-face seam step <=0.25 mm.
- Free-standing front deviation under a straightedge <=0.50 mm after one hour.
- Assemble/disassemble three complete cycles without damaged bosses, spinning
  nuts, or last-seam force escalation.
- Hold the free-standing assembly vertically under self weight and repeat the
  seam/flatness checks.
- Ten lift/place cycles, changing the held quadrant each time, must not
  disengage a seam.

## What CAD does not prove

Passing CAD proves nominal solids, registration geometry, access, and
envelopes only. It does not prove printed boss fit, screw preload, seam slip,
first-layer flatness, shrinkage, creep, free-state flatness, or handling
durability. Do not begin B1 support work until the complete printed B0 passes
the physical gates. R118..150 remains reserved and must stay clear.
