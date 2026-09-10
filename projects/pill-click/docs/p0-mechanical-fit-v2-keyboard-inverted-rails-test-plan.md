# P0 mechanical-fit V2 print and physical test plan

Status: `accepted_for_C5_first_physical_print`. Independent CAD/package review
passed with no blockers. This does not approve physical fit, force, fatigue,
food-contact suitability, or child resistance, and the complete three-part
dispenser remains gated on a successful C5 physical test.

## What this gate proves

V2 is the next mechanical-fit print after V1. It has exactly three dispenser
parts: a rounded housing with four inverted female channels, a solid tapered
keyboard button with four continuous male rails, and a blind rear cover with
two side squeeze latches. It deliberately has no pill openings, spring,
magnet, push-push mechanism, or text.

The 13.40 mm manual stroke is represented by pressed, released, and maximum
pull STEP assemblies. The 13.60 mm rejection state is intentionally outside
the allowed travel and intersects only the four blind rail stops.

## Print order

1. Print the two C5 specimen STLs separately. Do not merge them or add a shared
   base. Both files are already oriented with their native +Y direction up.
2. Assemble the C5 arm/cover specimen into the C5 housing/receiver specimen.
3. Only after C5 passes, print the three dispenser STLs or the three-component
   3MF bundle.

Use the same material, 0.40 mm nozzle, layer height, cooling, perimeter count,
and slicer settings planned for later prototypes. Disable scaling. Add text in
Orca Slicer only after this gate passes.

## C5 latch coupon acceptance

- Direct insertion visibly deflects the hook inward by 0.55 +/- 0.05 mm.
- The hook seats behind the receiver shoulder without cracking or permanent
  whitening.
- A 0.40 mm inward pad squeeze releases the hook.
- The 0.50 mm pad stop prevents further travel; do not force beyond the stop.
- Complete 30 insert/release cycles. The hook must still seat and resist a
  10 N axial pull for 10 seconds.
- Reject on a fused coupon, inability to move the specimens independently,
  cracked root, hook bypass, pad over-travel, or permanent set above 0.20 mm.

## Three-part dimensional checks

Measure before assembly:

- outer envelope: 40.00 x 40.00 mm in X/Z;
- inner body and key skirt: 34.20 mm across straight sides;
- key face: 32.80 mm;
- each male rail: 2.20 mm tangential width and 1.20 mm external height;
- each normal female channel: 2.60 mm wide and 1.20 mm deep;
- each rear mouth: 3.00 mm wide and 1.60 mm deep;
- each blind stop wall: 1.20 mm axial thickness;
- nominal straight-side body clearance: 0.20 mm per side.

Functional faces must remain unsanded: rails, channels, stop faces, latch
beams/roots/hooks, pad stops, ledges, and pockets.

## Assembly and motion checks

1. Remove the rear cover, rear-feed the button into all four flared channel
   mouths, then install the cover. No key relief is required.
2. Confirm all four rails remain engaged. The button must not pull out from the
   front at any allowed state.
3. Cycle manually from pressed to released through 13.40 mm. The final 0.15 mm
   is endplay before the four flat stop contacts at 13.55 mm.
4. Complete 100 full cycles. Record sliding force at cycles 1, 25, 50, 75, and
   100. Acceptance is <=8 N nominal with no spike above 12 N.
5. With one cover latch squeezed and the other seated, the cover must remain
   retained. With both pads squeezed 0.40 mm, it must release without damage.
6. Complete 30 rear-cover cycles after C5 passes. Both hooks must still seat
   and withstand a 10 N axial pull for 10 seconds.

## Blind-face and visual checks

- The rear face has no through opening in pressed, released, or maximum-pull
  states. Side squeeze notches may expose only guide-clearance space behind the
  solid button.
- Confirm the top and bottom are plain: exactly two latch mechanisms exist,
  one on each side.
- Compare the physical parts with the reviewed snapshots listed in
  `models/p0_mechanical_fit_v2_keyboard_inverted_rails/p0_mechanical_fit_v2_manifest.json`.

Record printer, material, nozzle, layer height, measured dimensions, force
results, cycle results, fracture/whitening observations, and pass/fail. A CAD
pass is not a physical pass.
