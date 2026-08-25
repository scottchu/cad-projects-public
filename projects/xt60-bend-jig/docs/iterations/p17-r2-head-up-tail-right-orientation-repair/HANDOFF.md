# P17-D10-R2 implementation handoff

Status: design frozen; implementation, independent critique/validation, and
formal review pending.

D10-R1 changes the corresponding-vertex END displacement acceptance from the
contradictory `<=0.65761 mm` to the exact-derived safe ceiling
`<=0.657824 mm`; the expected exact maximum is `0.657823586728 mm`. It also
replaces the inherited per-rail `crossing sine >=0.10` threshold with regular
rail derivative, monotonic progress, one-to-one branch continuity, exact
reconstruction, and full-rank combined-Jacobian gates. Crossing sine remains a
reported diagnostic. All exact rod coordinates and all actual-solid, web,
support, collision, service, and user-visible gates remain frozen.

D10-R2 changes only `C` from `(1.75,6.25)` to `(3.00,12.00)`. Regenerate all
six rod rails and both axle rails from the unchanged inverse equations. This
datum passed the frozen actual-solid support, web, reconstruction,
conditioning, collision, XT60-clearance, and service gates. Do not change the
exact rod states, `A`, workpiece, `24 deg`, plate envelopes, slot width, or
topology.

## Implement exactly

1. Correct the front convention to `+Z` up / `+Y` right and author the `└`
   wire centerline from `B=(16.235,18.435)`, `R=6`, vertical `Y=10.235`
   upward, and horizontal `Z=12.435` rightward.
2. Replace only the rod state contract with the exact table in `DESIGN.md`:
   OPEN upper-left/upper-right/lower-right, then END upper-left/middle/lower-
   right. Add explicit first-contact state/evidence.
3. Use common linear stroke `S=10.5852813742` and `theta_end=24 deg`; do not
   use smoothstep for geometry.
4. Build both fixed-inner guides as direct stationary straight capsules and
   rederive all six outer rod rails plus both fixed-axle rails by the exact
   side-local inverse transforms. Do not edit rails by eye.
5. Preserve `A=(-29,17)`, use `C=(3.00,12.00)`, four plates, `80/82/85 mm`
   envelopes, three `OD4 x 50` rods, six permanent stepped caps, `4.15 mm`
   slots, the larger right force side, and the accepted axial stack.
6. Add orientation, vertex-mapping, right-vertical OPEN leg, small END-delta,
   contact, straight-track, inverse-rail, endpoint-conditioning, no-floating,
   actual-solid collision, and service-path regressions.
   Endpoint conditioning must use the D10-R1 regularity/monotonicity/branch/
   combined-Jacobian gates, not reinstate an individual crossing-sine cutoff.
   Add a continuous two-sided support-strip regression from slot boundary
   through `+0.30 mm` at all 65 states; a point probe alone is insufficient.
7. Regenerate only explicit affected source-derived STEP states, motion
   sidecars, provenance/fingerprint, and the mandatory OPEN/contact/END plus
   opposite-side visual packet. Do not hand-edit outputs.
8. Trace `REQ-027` through `REQ-030`: workpiece-relative +Z head/up and +Y
   tail/right; OPEN UL-UR-LR right vertical leg without role swap/crossing;
   CLAMPED/END UL-middle-LR three-point wire wrap; and no retention/self-lock
   meaning. Viewer camera orientation cannot satisfy these requirements.

## Allowed implementation writes

- `projects/xt60-bend-jig/src/xt60_bend_jig/p17_r2_direct_counter_twist.py`
- `projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`
- explicit generators, STEP files, parameter sidecars, snapshots/GIFs,
  provenance, candidate manifest, and fingerprint under
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/`
- this iteration's `HANDOFF.md` implementation receipt only

Forbidden: unrelated projects or tools, version bump, 3MF/slicer release,
new hardware/structure/lock, or weakening a failed gate. Use Python only
through the repository root `uv` environment.

## Implementation done gate

- Focused tests derive and pass the full D10 numeric contract.
- Actual-solid motion/contact/support/collision and revalidated loading/reverse
  opening/removal path pass, including exact endpoints.
- Every affected written STEP is valid and matches source occurrences, bounds,
  and topology.
- Fresh visual evidence clearly shows the corrected `└` workpiece, correct
  OPEN vertical pair, preserved END diagonal, fixed inner plates/axle, and
  opposite outer rotation.
- One immutable candidate fingerprint is handed independently to P17-C08 and
  P17-V08; P17-R08 is their formal join. Physical validation remains pending.

## Immutable input

Implementation must verify
`/tmp/p17-d10-r2-implementation-input-manifest.txt` and every listed entry before
editing source. Any mismatch in the frozen D10 design files or authoritative
source/tests invalidates this handoff.

## P17-I08-R2 implementation receipt

- Status: implementation candidate complete; independent critique, validation,
  formal review, and physical proof remain pending.
- Frozen input verified: `/tmp/p17-d10-r2-implementation-input-manifest.txt`
  SHA-256 `2eb7184b774735f796169dc3efc039d68e7b60ef869fb105eba125467e1ebc2e`;
  every entry matched before D10-R2 writes.
- Implemented the true front-view `└` orientation, exact OPEN/contact/END rod
  states, stationary inner tracks, exact opposed inverse rails about
  `C=(3.00,12.00)`, 65-state continuous `+0.30 mm` support strips, actual-solid
  collision/contact, and the rederived P17-D10-R1 service path. No mechanism,
  hardware topology, product version, mesh, 3MF, or slicer change was added.
- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`:
  `19 passed`.
- Ten explicit generators rebuilt their STEP targets; ten of ten written STEP
  files passed CAD validation. Source/import parity passed ten of ten with
  maximum bounds delta `8.811e-12 mm` and maximum summed-volume delta
  `1.339e-8 mm3`.
- Digital gates: maximum rail residual `5.687e-15 mm`; minimum web
  `3.630990 mm`; combined rank `3`; maximum normalized condition `12.821633`;
  unintended intersection `0`; minimum XT60 clearance `0.750000 mm`; service
  BREP/analytic minima `1.250000/0.933816 mm` over `1001` samples per segment.
- Visual packet: three front orientation views with only the two front review
  plates hidden, one opposite-side END view, and a visually inspected 72-frame
  opposed-twist GIF. All render warnings were empty.
- Independent gate manifest:
  `/tmp/p17-i08-independent-gate-manifest.txt`, 30 entries, all verified,
  SHA-256 `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`.
- Candidate records are under
  `cad/p17_r2_direct_counter_twist/p17-r2-{artifact-provenance,candidate-manifest,candidate-fingerprint}.*`.
- Physical boundary: cap retention, force, endpoint holding/self-lock, heat,
  wear, vibration, soldered-wire behavior, print fit, and PETG acceptance are
  not proven digitally.
