# KAGE P3 V3 motor station assembly simulation

This isolated package documents one second-channel station. It does not change
the full rings, fins, keepers, roller towers, Hall homing, or optical model.

## Assembly order

1. Bolt the NEMA8 face to the open yoke with four ISO 4762 M2x4 screws. The
   1.5 mm printed flange leaves 2.5 mm engagement in the motor's threaded
   holes. Before any output-shaft parts are present, slide the horizontal
   D-bore bevel onto the motor shaft and tighten its M2x3 cup-point grub screw;
   this is its positive axial lock.
2. Heat-set four M3 inserts into the fixed chassis bosses. Bolt the complete
   yoke down with four ISO 4762 M3x8 screws; 5.0 mm enters each insert after the
   3.0 mm yoke foot, leaving 0.5 mm at the blind bottom.
3. With the role ring still absent, fit the lower split collar, lower MR84ZZ,
   real vertical 16T bevel, upper MR84ZZ, and 4x40 mm D-shaft. Tighten the
   bevel's M2x3 grub screw on the common +Y-facing shaft flat. Fit the role
   spacer, exact R2 16T output pinion, and upper collar; set the exact Z band
   and tighten both locks. The upper collar's clamp axis is biased 0.20 mm
   upward so a 3.0 mm hex-key envelope clears the pinion below it.
4. Still before installing the role ring, close each MR84 cradle with its
   removable radial gate and two M2x4 screws. Install the role ring last and
   verify the 16T/260T mesh. The collars leave 0.10 mm axial relief at both
   retention datums.

## Reverse service order

1. Remove the role ring first. Its teeth obstruct the hour-channel upper-gate
   screw axes, so the ring cannot remain installed during gate service.
2. Remove the four M2x4 radial-gate screws and pull both MR84 gates toward +X.
3. Use the separate +Y hex-key windows to loosen the top collar, output pinion,
   vertical bevel, and lower collar. Withdraw the D-shaft and remove the full
   output stack. The lower-collar screw sits 0.80 mm above the collar bottom so
   its 3.0 mm tool envelope passes below the MR84.
4. Only after the ring, gates, and vertical output stack are absent do the four
   M2 motor screw axes become open. Remove the motor screws, loosen the
   horizontal bevel lock from +Z, and withdraw the motor toward the clock
   centre (-X). These are static staged views, not CAD mates.

## BOM for one station

- 1x StepperOnline NEMA8, 20.3 mm face, 39.3 mm body, 4x7 mm D shaft
- 4x ISO 4762 M2x4 motor screws
- 4x ISO 4762 M3x8 chassis screws
- 4x M3 heat-set inserts, 4.6 mm OD x 5.5 mm
- 2x MR84ZZ bearings, 4x8x3 mm
- 1x steel output D-shaft, 4x40 mm, 3.5 mm across-flat
- 2x 4 mm split clamp shaft collars with M2 clamp screws
- 2x printed MR84 radial gates + 4x ISO 4762 M2x4 gate screws
- 3x M2x3 cup-point grub screws: horizontal bevel, vertical bevel, output pinion
- 1x printed open yoke, 1x printed role spacer, 1x printed 16T output pinion
- 1x printed horizontal and 1x printed vertical 16T bevel gear

The NEMA8 retains its supplied 4x7 mm D-shaped motor shaft. The separate
vertical output shaft is also D-shaped. Every role pinion receives its final
tooth/station phase first; its hub is then refilled and one common 4.10 mm,
3.60 mm-across-flat bore is cut. Tooth phase therefore cannot rotate the bore.

H/M/S spacer lengths are 3.55 / 6.95 / 10.35 mm. Corresponding output-pinion
face bands are -0.70..1.40 / 4.85..6.95 / 10.40..12.50 mm.

Physical validation remains required for bearing press fit, printed bevel wear,
split-collar availability, acoustic noise, heat-set insert pullout, and real
motor/ring runout.
