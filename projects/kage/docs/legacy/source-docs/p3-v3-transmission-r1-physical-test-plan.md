# P3 V3 transmission R1 physical test plan

## Purpose

Validate one horizontal NEMA8 to one unchanged P3 V3 carrier plane before
duplicating the station three times. Do not print the complete 300 mm clock for
this gate.

## Assembly

1. Print the chassis, motor saddle, both real 16T miter gears, the selected role
   spacer and output pinion, the matching 259T arc, lower thrust sleeve, lower
   D-bored clamp collar, both bearing retainers, captured arc carriage, and
   removable upper retainer. The lower guide and hard stops are already fused
   into the printed chassis; they are not a separate part.
2. Press the lower MR84ZZ into its pocket and fasten the lower retainer with
   two M2 screws. Install the upper MR84ZZ and its two-screw retainer later in
   the shaft-stack sequence.
3. Put the lower clamp collar on the 4 x 40 mm D-shaft, insert the shaft through
   the lower bearing, then add the thrust sleeve, vertical miter gear, and upper
   MR84ZZ. Tighten the collar and vertical-gear M2 screws.
4. Add the role spacer and output pinion. Set axial endplay to 0.05-0.15 mm,
   then tighten the output-pinion M2 screw.
5. Seat the horizontal miter gear on the 4 x 7 mm D shaft; the matching D-bore
   is the positive drive. Bolt the motor to its saddle. Slide the saddle within
   the +/-0.5 mm slots until the miter pair turns freely without visible tooth
   separation, then tighten the four M3 stacks: lower washer against chassis,
   upper washer against saddle, and at least 2.4 mm nut engagement.
6. Capture the 259T arc carriage between the chassis-fused lower guide/stops
   and the two-screw removable upper retainer. This fixture moves only
   +/-0.08 mm to test backlash and tooth
   contact; do not treat it as a continuous-rotation ring.

## Pass/fail gates

- Hand rotation: 20 complete output-shaft revolutions with the arc carriage
  removed, without bind or bearing movement.
- Captured mesh: carriage reaches both +/-0.08 mm hard stops without tooth
  climb, rail escape, or retainer lift.
- Backlash: visible/tactile clearance at both meshes, but no skipped tooth when
  direction reverses.
- Axial endplay: 0.05-0.15 mm measured at the output pinion.
- Radial runout: <=0.20 mm at the output pinion pitch circle.
- Endurance: 100 forward/reverse cycles before any full-speed test.
- Seconds-speed test: 24 hours at 16.1875 motor rpm without losing mesh.
- Noise: record A-weighted dBA at 1 m and compare gear materials/driving modes.
- Temperature: no softened PETG, creeping saddle, or bearing-pocket movement.

If the coupon fails, change only the isolated R1 transmission. The accepted V3
ring/fin source remains frozen until a physical coupon passes.
