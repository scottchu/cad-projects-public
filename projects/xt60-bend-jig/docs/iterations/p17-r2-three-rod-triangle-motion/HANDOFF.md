# P17 R2 three-rod triangle motion handoff

Status: P17-I07-R1 digitally accepted by P17-R07; physical validation pending.

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

## P17-I07-R1 implementation receipt

Status: implementation candidate complete; independent critic, validator, and
formal reviewer remain mandatory. The implementer does not approve this
candidate.

Verified frozen input:

- `/tmp/p17-r2-three-rod-service-r1-implementation-input-manifest.txt`;
- SHA-256
  `a309e0d836454ac4b9e2f48b8ab3de3cf450b41e96909e6ef96aa47dc277930a`;
- all four manifest entries matched before R1 source work.

Implemented source-first changes:

- all three moving rods are `OD4 x 50.00 mm`, use the exact R1
  OPEN/contact/END triangles, and translate with linear
  `u=theta/24`;
- fixed-inner guides are direct extended closed capsules; all six outer rod
  rails and both fixed-axle rails are inverse transforms about
  `C=(1.75,6.25)` with left/right counter-rotation;
- `80/82/85 mm` inner/left-outer/right-force-outer plates, `4.15 mm` slots,
  unchanged purple axle `A=(-29,17)`, six permanent stepped caps with
  `8.70 mm` engagement and `9.05 mm` length;
- redundant green grip and obsolete inner service-window cutter absent; no
  bar, yoke, linkage, gear, tab, or lock added;
- fixed and full Viewer sidecars move all three rods/caps linearly, rotate
  only outer plates in opposite senses, and keep fixed-inner holes stationary;
- explicit contact generator and written contact STEP added.

Deterministic evidence:

- focused test file: `18 passed`;
- 65-state actual-solid motion, wire contact/preload, rail reconstruction,
  support, conditioning, cap closure, collision, and occurrence gates pass;
- maximum rail reconstruction residual
  `7.160723346098895e-15 mm`; minimum crossing sine
  `0.1020238653409378`; normalized maximum condition number
  `9.640422856842672`, rank `3` throughout;
- minimum web `2.6675894314400947 mm`; actual extended fixed-inner cutter gap
  `6.103048327204936 mm`; outer rod-cutter gaps left/right
  `6.522658438854226/6.41897887963513 mm`;
- exact D09-R1 full-component service sweep: `1001` actual BREP samples per
  segment (`4004` evaluated poses) and `1001` dense reconstruction samples per
  segment; BREP minimum `0.846751751172426 mm`, dense minimum
  `0.8467517511724272 mm`, maximum intersection `0.0 mm3`;
- CAD `scripts/gen --write --force --json` built all ten explicit targets;
  `scripts/inspect validate` passed all ten written STEP files with zero
  geometry failures;
- direct-source versus imported-STEP parity passed all ten targets: maximum
  bounds delta `6.253e-12 mm`, maximum summed-solid volume delta
  `4.890e-9 mm3`;
- four fresh open/contact/END/opposite-view PNGs and one fresh 72-frame
  opposed-twist GIF rendered with empty warnings and were visually inspected.

Candidate identity and evidence:

- source SHA-256:
  `11b5336d7c4523c4ce685b8d784406934a08098179160b306cd595c2fcf589c2`;
- focused test SHA-256:
  `752fb84281113a5025aefd37db17340f5d00388c43743884af2c3388a628b779`;
- independent gate manifest:
  `/tmp/p17-i07-independent-gate-manifest.txt`, 30 verified entries;
- candidate fingerprint SHA-256:
  `5965f4e88bc807a1e13ac38c7bc3b342cc285f24a9082c9975dd44000540cb87`;
- repository records:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-manifest.json`,
  `p17-r2-candidate-fingerprint.json`, and
  `p17-r2-artifact-provenance.json`;
- review packet:
  `cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i07r1_*`.

Physical boundary: CAD/source and written-STEP evidence do not prove PETG fit,
cap or keeper retention, required hand force, heat, wear, vibration, wire
holding, insulation safety, springback, endpoint retention, self-lock, slicer,
3MF, or physical acceptance.

## P17-C07 / P17-V07 / P17-R07 closure

The exact independent-gate fingerprint
`5965f4e88bc807a1e13ac38c7bc3b342cc285f24a9082c9975dd44000540cb87`
was unchanged through all three independent gates.

- `P17-C07`: PASS with no blocker or major finding.
- `P17-V07`: PASS; `18` focused tests, all `10` written STEP exports and
  source/export parity, frozen visual packet, and singleton Viewer HTTP
  readiness passed.
- `P17-R07`: ACCEPT for delivery of CAD source, written STEP/export evidence,
  frozen visual evidence, and Viewer transport/readiness.
- Full actual-solid service sweep: `4004` poses, zero intersection, minimum
  clearance `0.846751751172426 mm`.
- Physical manufacture and operation remain explicitly untested.

The next responsible action is an explicitly authorized print/slice package
and physical three-rod/cap/slot trial. Any authoritative source or frozen
candidate-input change invalidates C07, V07, and R07.
