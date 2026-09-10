# P21 R1 axial-width and cap-fit physical correction

Date: `2026-08-28`

Status: **CORRECTED CONTRACT; PRIOR 60 MM ARTIFACTS REJECTED**

## Physical observations and user-required deltas

- User photos and caliper readings show the assembled inner-plate spacing is
  too narrow for the intended use.
- Increase only the fixed span between the two inner plates by exactly
  `10.00 mm`: `18.40 -> 28.40 mm`.
- The printed permanent caps are physically much too tight. Change the distal
  socket from `ID4.04 -> ID4.10 mm`, using prior P16/P13 hand-fit evidence as
  the bounded looser starting point.
- These are not asserted to be the only physical problems.
- User correction: all three purchased stainless rods are immutable
  `OD4.00 x 50.00 mm` stock. They cannot be lengthened.

## Coupled axial consequence

Preserve the `0.30 mm` cap-to-outer gap, plate thicknesses and inner/outer
running gaps while keeping all three rods at `50.00 mm`. The printed stepped
center axle changes `34.90 -> 44.90 mm`. The wider stack leaves `3.70 mm`
available cap engagement per side instead of `8.70 mm`; retention at this
shorter engagement is an explicit physical unknown and must not be claimed
from CAD.

This changes the axial stack and center-axle interface while preserving the
purchased-rod interface, so it remains the P21 R1 correction rather than
rewriting accepted P20 history.

## Frozen delta mask

Allowed: inner clear span, dependent X placements/printed axle length, actual
cap engagement, and cap distal socket ID. Forbidden: purchased rod length
(`50.00 mm`), YZ rod paths, rail topology, plate radii or
thickness, motion angles, axle YZ datum, XT60/workpiece geometry, keeper fit,
and unrelated blocker repairs.

## Newly opened architecture question

Physical handling indicates that direct Orange-rod depression while Blue and
Green are held produces the preferred motion, but release causes immediate
back-drive to OPEN. A retained bridge/latch is therefore a separate mechanism
architecture decision and is not authorized inside this axial-width/cap-fit
delta mask.
