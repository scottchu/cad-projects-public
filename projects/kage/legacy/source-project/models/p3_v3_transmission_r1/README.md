# KAGE P3 V3 transmission R1

This is an isolated one-station transmission coupon. It does not alter or
replace the accepted P3 V3 300 mm rings, fins, simulator, or optical math.

## What each part does

- `p3_v3_r1_assembled.step`: nominal minute-height station with purchased-part
  references in place.
- `p3_v3_r1_service_exploded.step`: assembly-order view.
- `p3_v3_r1_print_components.step`: selected-minute functional-position
  catalog only, not a slicer plate. Use the individual STEP/STL files under
  `print/parts/` for printing; motor, steel shaft, bearings, and screws are omitted.
- Chassis: holds two MR84ZZ bearings on one 121.5 mm output-axis datum.
- Motor saddle: mounts one horizontal NEMA8 and provides +/-0.5 mm radial mesh
  adjustment through four slots.
- 16T miter pair: turns the horizontal 4 x 7 mm D motor shaft through 90 degrees
  to the vertical 4 x 40 mm D output shaft.
- Lower thrust sleeve and split clamp collar: keep the vertical shaft stack at
  the assigned ring height instead of relying on bearing friction or a loose
  printed post.
- Role spacer: places the selected minute output pinion at its unchanged
  carrier height. Hour and second variants remain parametric source options;
  they are not duplicated in the selected-minute catalog.
- 16T output pinion and 259T ring arc: a true involute M1 mesh coupon for the
  unchanged full-carrier interface.
- Captured arc carriage: fuses the real 259T tooth arc to a backing tongue held
  by a lower guide/hard-stop feature fused into the chassis and a removable
  upper retainer. Curvature
  limits translation to +/-0.08 mm, so this is explicitly a backlash and tooth-
  contact coupon, not a continuous-rotation substitute for the full ring.

## Prototype hardware

- 1 x NEMA8 motor, 20.3 mm face, 39.3 mm body, 4 x 7 mm shaft
- 2 x MR84ZZ bearings, 4 x 8 x 3 mm
- 1 x 4 x 40 mm D steel shaft, 3.5 mm across-flat
- M2 motor screws, 3 x M2 grub screws, 4 x bearing-retainer M2 screws, and
  2 x upper-slider-retainer M2 screws
- 4 x M3 saddle bolts, 8 x washers, and 4 x external M3 nuts
- PETG chassis, saddle, retainers, and spacers
- Tough PLA/PETG/nylon test gears; material choice remains a physical test

The assembly uses the upper bearing as the common role datum. The clamped
vertical miter hub is 0.10 mm below the upper bearing and the role spacer begins
0.05 mm above it, keeping total nominal shaft endplay at the reviewed 0.15 mm
upper limit. Below the drive, the shaft-guided thrust sleeve spans from the
lower bearing to the vertical miter hub; a 2.85 mm-long D-bored M2 clamp collar
retains the shaft beneath the lower bearing. The vertical miter, output pinion,
and collar all use matching 3.60 mm across-flat D-bores, while their 1.60 mm M2
tap pilots accept secondary retainers whose tips seat on the shaft flat. The
Both bearing outer races are positively captured by removable retainers. The
lower retainer uses 1.50 mm of PETG pilot engagement and the upper uses 1.60 mm.

## Not yet proven

CAD proves alignment, topology, nominal clearance, and assembly order. It does
not prove printed tooth strength, sound level, long-run heat, runout, wear, or
the real motor/shaft tolerances. Those gates remain `PENDING` in the manifest.
