# P17 R2 three-rod triangle motion handoff

Status: design complete; implementation pending.

## Frozen implementation contract

Implement the exact selected contract in `BRIEF.md` and `DESIGN.md` as the
smallest source-first change to P17 R2. Do not create a new P/R version.

Required implementation deltas:

1. Replace the invalid predecessor `GUIDES` with the selected OPEN/contact/END
   centers and fixed straight directions.
2. Replace geometric smoothstep with `u=theta/theta_end`; animation time may
   ease separately.
3. Set `theta_end=24 deg`, `C=(-1.74,13.22)`, fixed-inner/outer diameters
   `70/72/75`, and moving slot width `4.15`.
4. Keep purple axle geometry and `A=(-29,17)` unchanged; regenerate both
   side-specific axle rails and all six side/rod outer rails by inverse
   transform.
5. Use all three `OD4 x 50` rods. Keep the `32.00 mm` stack and implement
   `8.70 mm` cap engagement with stepped permanent blind caps at least
   `9.05 mm` long.
6. Remove the redundant green left grip block. Preserve the larger right
   force-side outer plate without adding another tab.
7. Remove the obsolete fixed-inner completed-pigtail window that intersects
   the selected bottom/diagonal tracks; prove central-span service instead.
8. Add focused regressions for the independently observed current failures:
   floating bottom rod, negative/insufficient webs, zero wire contact, and
   endpoint ill-conditioning.

## Required evidence

- Fast math, requirement, parameter-domain, and occurrence checks.
- Actual-solid collision and positive two-sided support checks at at least 65
  states including exact OPEN, first contact, and END.
- Rail reconstruction residual `<=0.05 mm`, crossing sine `>=0.25`, normalized
  constraint Jacobian condition `<=1000`, and no endpoint rank loss.
- Written STEP validation and source/export parity for explicit affected
  targets only.
- Assembled, side, OPEN/contact/END, and rail close-up snapshots.
- Live CAD Viewer page HTTP `200`, exact artifact HTTP `200` with
  `state=ready`, followed by visual inspection.
- Independent critic and validator on one frozen candidate fingerprint, then a
  distinct formal-review join.

## Acceptance boundary

Digital acceptance may establish geometry, constraints, collision freedom,
source/export parity, and prescribed motion. It cannot establish printed fit,
cap retention, preload force, insulation safety, heat behavior, springback, or
self-lock. The smallest next physical test after digital acceptance is a
three-rod/cap/slot motion assembly with both nominal `OD4.30` insulated wires,
recording first contact, END effort, rod wobble, wire marks, XT60 body reaction,
cap installation/retention, and cooled angle.

## Implementation input manifest

The immutable implementation manifest is
`/tmp/p17-r2-three-rod-implementation-input-manifest.txt`. Its SHA-256 is
recorded by the design receipt returned to the orchestrator. The implementer
must verify the manifest file and every entry before editing source.

## P17-D09-R1 superseding implementation handoff

Do not implement the earlier `S=4.0142135624`, `C=(-1.74,13.22)`, or
`70/72/75` envelope. They failed completed-pigtail service. Implement the
smallest bounded repair frozen in the R1 amendment to `DESIGN.md`:

1. Keep first-contact and END centers unchanged, but set common OPEN stroke to
   `12.80 mm` and OPEN centers to upright `(35.5,9)`, bottom `(6.8,37.7)`, and
   diagonal `(5.2339574413,7.4339574413)`.
2. Set `C=(1.75,6.25)`, retain `theta_end=24 deg`, linear geometric travel,
   and counter-rotation `left=-theta`, `right=+theta`. Regenerate all six rod
   rails and both fixed-axle rails from the inverse transform; do not redraw
   or approximate them.
3. Set inner/left-outer/right-force-outer diameters to `80/82/85 mm`. Retain
   slot width `4.15`, minimum web `2.20`, the larger right force side, and the
   unchanged purple axle. Add no structural part.
4. Prove the exact service path `P0=(0,0,0 deg)`, `P1=(0,0,-35 deg)`,
   `P2=(8,0,-35 deg)`, `P3=(20,20,-35 deg)`,
   `P4=(20,45,-30 deg)` by continuous linear interpolation after reverse
   opening. Use final actual body, solder joint, two wires, rods, caps, plates,
   axle, and keepers; require zero intersection and `>=0.75 mm` clearance at
   at least 1001 samples per segment.
5. Preserve the original 50 mm axial stack and six permanent stepped caps.
   Preserve all first-contact/END preload gates and physical-unknown language.
6. Replace the obsolete crossing-sine threshold with `>=0.10`; retain the
   normalized full-Jacobian condition `<=1000`, positive two-sided support,
   web, actual-solid collision, endpoint, reconstruction, and no-floating
   regressions.

This is P17 R2, not a new version. Failure of the exact R1 service path or any
retained gate returns to design; the implementer must not invent another
travel law, enlarge slots, move the fixed axle, add hardware, or weaken the
clearance threshold.
