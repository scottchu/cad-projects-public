# P0 mechanical-fit v1 physical test plan

This plan validates only the three-part manual slider interfaces. It does not
approve medicine use, a return-force system, or push-push behavior. Record the
printer, material, nozzle, layer height, wall count, infill pattern/percentage,
cooling, and any dimensional compensation. Scaling is disabled.

## Print

Print exactly these three files:

1. `p0_mechanical_fit_v1_outer_housing.stl` on its X-negative exterior side;
2. `p0_mechanical_fit_v1_solid_inner_button.stl` on the plain key face, with Y
   vertical; and
3. `p0_mechanical_fit_v1_snap_rear_cover.stl` on the blind exterior rear face,
   with all four snap arms upward.

Use slicer infill to control the solid inner button's internal material. Do not
add a CAD drain or opening. Keep supports and sanding away from rails, grooves,
lips, backing ribs, tabs, stop pads, snap roots, beams, hooks, and pockets.

## Before assembly

- Confirm the rear faceplate is blind.
- Measure all eight normal lips; each must be at least 0.70 mm.
- Measure all eight positive-Y mouth lips; each must be at least 0.50 mm.
- Reject cracks, whitening, missing layers, curled rail ramps, or damaged snap
  roots.

## Assembly and cycling

1. Leave the rear cover off and rear-feed the solid inner button to pressed
   position.
2. Install the rear cover and confirm all four hooks seat and the cover is
   flush.
3. Manually cycle pressed to released 100 times. This prototype has no spring,
   magnet, or latch.
4. Record breakaway and steady sliding force at cycles 1, 25, 50, 75, and 100.
   Acceptance is at most 8 N steady/breakaway and no local spike above 12 N.
5. At cycles 0 and 100, apply a measured 10 N front pull for 10 seconds at
   pressed, mid-travel, and released positions. The button must remain captive.
6. Separately complete 30 rear-cover insertion/removal cycles and record snap
   extraction force rather than inferring it.

## Final inspection

Pass only if every rail, lip, backing rib, tab, stop, snap, and cover remains
free of cracking, whitening, delamination, derailment, and permanent set. At
mid-travel, measure total lateral and vertical key play; each must be at most
0.50 mm. Preserve the explicit artifact names and manifest hashes with the
results.
