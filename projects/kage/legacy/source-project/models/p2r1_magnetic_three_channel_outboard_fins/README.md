# KAGE P2R1 magnetic three-channel MVP

This is a standalone manual mechanism experiment. It does not replace or
modify the V0R2 fake quartz/hand optics fixture, the LED cartridge, or the web
simulator.

## What it tests

- Three hidden manual driver rings at radii 55 / 75 / 95 mm.
- One removable, mechanically captured front follower per radius.
- One Ø6 x 3 mm magnet in each driver and follower (six total).
- Three separator variants: 1.0 / 1.5 / 2.0 mm.
- Distinct H/M/S fins and arbitrary-angle mechanical coexistence.

The printed tracks determine position. Magnets only transfer torque. CAD does
not prove magnetic force, lag, cross-coupling, friction, or durability.

## Assembly (+Z / rear to viewer)

1. Lay `rear_base` flat.
2. Install the coplanar S, M, and H hidden rings on the open-back wear pads.
   Insert the driver magnets from +Z; mark polarity first.
3. Install one selected separator. It closes the rear races and traps the rear
   magnets.
4. Insert the three follower magnets from -Z into the H/M/S followers. Use the
   opposite attracting polarity relative to the corresponding driver magnet.
5. Place each follower in its own annular track.
6. Install cap rings R0/R1/R2 with nine M2x4 self-tapping screws into the
   separator bosses. Install R3 with six M3 through screws passing through R3,
   the separator, the six base-integral spacer columns, and the rear base ring.
   Secure them with external rear washers/nuts; do not use the spacers as
   self-tapping bosses. The columns set the separator datum without compressing
   the cap stack.
7. Reverse the order for service. Magnets remain removable only when the front
   caps and separator are disassembled.

## Printing

Use the variant matching the separator you want to test. Each main 3MF is a
collision-free transfer bundle with exactly 12 named objects, all bed-contact
and separated by at least 5 mm along X. Because several parts are Ø220 mm, the
complete bundle intentionally spans multiple normal printer-bed widths and is
not a one-plate print.

For actual slicing, use the matching `t1p0_individual_plates`,
`t1p5_individual_plates`, or `t2p0_individual_plates` directory. It contains
one normalized, bed-contact 3MF per part. Arrange only the smaller parts
together when your slicer confirms clearance; print `rear_base`, the selected
`separator`, and the large cap rings separately. The canonical individual
follower STLs are the 1.5 mm variant; t1p0 and t2p0 follower STLs are separately
named.

- 0.4 mm nozzle; 0.20 mm layer; PLA or PETG.
- Parts are modeled support-free in their export orientation.
- Start with t1p5, then compare t1p0 and t2p0.

This P2R1 layout moves every fin 10 mm farther from the center than P2 while
retaining the same 20 mm channel pitch. The second follower shoe and rear
magnet boss reach r99.5, leaving 1.0 mm to the stationary spacer envelope.

See `docs/p2r1-magnetic-three-channel-outboard-fins-physical-test-plan.md` before judging
the mechanism.
