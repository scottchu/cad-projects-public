# P18-REVIEW formal independent join

Reviewer: `/root/p17_optimizer_formal_review`  
Date: `2026-08-26`  
Decision: **ACCEPT — P18 R1 CAD, written STEP artifacts, and Viewer review handoff only**.

This decision accepts the immutable P18 R1 candidate as a digitally coherent
parametric CAD baseline. It does not accept a mesh, 3MF, slicer result, print,
fit, retention, force, heat, wear, locking behavior, or physical product.

## Frozen provenance

- Branch: `codex/xt60-p18-r1-compact-counter-twist`
- Reviewed repository HEAD: `466a65dd4a5550a5e104a74408e14e083d987982`
- Candidate-manifest SHA-256:
  `fb0755a0d448ee000dde4bd63eacca7fbaf6e55abeb16312a7f39c5ccfc5d1d5`
- Critique SHA-256:
  `5f75f9ec0c2267e54ba2f0eb2630c7382a842415b59a6ec4b6a35258b775905a`
- Validation SHA-256:
  `6d823b79e16d57c7cf38562166763669caaea1da685c105e5b419ba7274163b8`
- Dispositions SHA-256:
  `e94c84428a0eb8e152458bf90df347950a69d177e20282d76518e3bb4b258976`

The manifest itself and all `20/20` declared paths were independently
re-hashed successfully. `VALIDATION.md` says `21` declared paths; that is a
non-blocking receipt count typo, because the immutable manifest contains and
verifies exactly `20` entries.

## Join decision

- The P18 source, six STEP entrypoints, full-motion sidecar, focused tests and
  four review snapshots are all included in the same verified fingerprint.
- The focused P18 suite was independently rerun: `10 passed`.
- The OPEN written STEP was independently revalidated and source/import diffed:
  zero validity failures and no topology, geometry, bounds or count delta. The
  frozen validator separately passed the same validate/diff gates for all six
  written STEP artifacts.
- The four frozen snapshots were independently inspected at original
  resolution. They show the accepted P18 OPEN right-angle and END diagonal
  topology, correct head-up/tail-right workpiece orientation, unchanged rod
  identities, eccentric fixed purple axle, four plates, three rods, six caps,
  opposite outer-plate rail families, and a coherent exploded axial stack.
- Critique findings C1-C7 are dispositioned without altering the candidate.
  C3 is closed digitally: a functional rail may cross virtual datum `C`, but
  no centered pivot bore or physical member is authored there. C1, C2 and
  C4-C7 remain explicitly bounded as unresolved service or physical risks.

The P18 R1 CAD and written STEP artifacts therefore pass this formal join.
The exact `p18_r1_full_motion.step` candidate may be handed to CAD Viewer and
shown to the user for review. A claim that the live preview is ready still
requires the exact Viewer page to return HTTP `200`, its exact artifact endpoint
to return HTTP `200` with `state == "ready"`, and a visual check showing no
error state; the link alone is not preview evidence.

## Unaccepted gates

- Full-assembly soldering-iron/tool access is **not validated**. The pigtail
  extraction and partial keepout checks do not prove a real iron clears every
  plate, rod and cap.
- The near-tangent rail interval does **not** prove acceptable hand torque,
  friction, absence of wedging/backlash, or back-drive behavior.
- Permanent cap and keeper retention, axle/hex fit, PETG dimensional outcome,
  limiting-web tolerance robustness, right-side tactile advantage, heat,
  wear, assembled motion and self-lock behavior remain physical gates.
- Mesh/3MF generation, slicing, printer orientation/profile, printability and
  physical acceptance were not performed and are not accepted here.
