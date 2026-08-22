# KAGE B0 four-to-one base MVP

This isolated successor validates only the hard stationary mechanic: four
printed annular quadrants closing into one 300 mm base. It intentionally has no
ring, roller support, pinion, motor, electronics, LED, or legacy mounting holes.

## Printed and purchased items

Print exactly eight bodies:

- four `quadrant_Q*_front_down.step` parts, one each;
- four `bridge_S*_bottom_down.step` parts, one each.

Purchase:

- 8 × M3x6 ISO 7380-1 button-head screws;
- 8 × ISO 4032 M3 hex nuts;
- 8 × D4x6 steel dowel pins.

The model-only 3MF contains the eight printed bodies and no slicer profile or
purchased hardware. Import or auto-arrange one quadrant per U1 plate; bridges
may share a plate. Do not interpret the 3MF as a production plate layout.

## Print orientation

- Quadrant STEP files are already flipped with the visible/front face at Z=0.
  Print that face on the bed with a 5 mm brim and no support.
- Bridge STEP files are bottom-down. Their nut pockets and blind dowel bores
  must remain open upward; print without support in those openings.
- Use the same material, layer height, wall count, cooling, and bed preparation
  for all four quadrants. Do not tune one quadrant independently.

Before the complete set, print a small fit coupon or one bridge to qualify the
AF5.8 nut pocket, D3.95 press bore, round D4.15 slip half-feature, and 5.15 ×
4.15 radial-relief half-feature. A coupon does not pass B0.

## Assembly

1. Press one D4x6 pin into each R78 and R108 bridge bore to 3.50 mm engagement.
2. Load both M3 nuts from each bridge top; the pockets are 2.70 mm deep and
   open at the assembly face.
3. Support all four quadrants front-face up in their final XY arrangement on
   equal-height blocks or an open fixture that leaves every seam accessible
   from below. Keep the four front faces coplanar; do not lower a last quadrant
   vertically with a bridge hanging beneath it.
4. From below, loosely preattach only bridges S1, S2, and S3, one at a time.
   Guide both exposed 2.50 mm pin lengths into the adjacent quadrant before
   adding the two M3x6 screws from above. The R78 feature is round; the R108
   feature is radially relieved. Do not force the relieved pair radially.
5. With all four quadrants still supported in final position, insert bridge S4
   upward from below. Its pins travel straight into the open R78 and R108
   features without moving Q4 through another quadrant or bridge. Seat S4
   against both quadrant undersides, then add its two screws from above.
6. Confirm all eight screws are present and still loose. Put all four bridge
   bottoms on a verified flat plane. Tighten in a cross-seam
   sequence, alternating across the base.
7. Remove the base from the fixture, wait one hour, then measure the free state.

## B0 physical acceptance

- OD at 0/45/90/135 degrees: 300.00 ±0.50 mm; max minus min ≤0.50 mm.
- Every seam gap: 0.05..0.30 mm, with no forced bow or overlap.
- Front-face seam step ≤0.25 mm.
- Free-standing front deviation under a straightedge ≤0.50 mm after one hour.
- Assemble/disassemble three complete cycles without damaged holes, spinning
  nuts, pin pull-out, or last-seam force escalation.
- Hold the free-standing assembly vertically under self weight and repeat the
  seam/flatness checks.
- Ten lift/place cycles, changing the held quadrant each time, must not
  disengage a seam.

## What CAD does not prove

Passing CAD proves nominal solids, gaps, access, and envelopes only. It does not
prove first-layer flatness, shrinkage, press fit, clamp preload, creep, free-state
flatness, or handling durability. Do not start B1 ring/support CAD release from
this article until the complete printed B0 passes the physical gates above.

R118..150 is reserved for later B1 through-bolted support cartridges. Do not
drill or add guessed support holes to this B0 model.
