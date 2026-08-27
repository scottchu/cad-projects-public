# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, the corrected P20 R2 contract under
`docs/iterations/p20-r2-fixed-rod-arc-rail/`, and every path declared by its
`DESIGN_INPUT_MANIFEST.sha256` before changing this project.

## Resume point

- Active forward iteration: `p20-r2-fixed-rod-arc-rail`.
- The user approved the complete P19-based P20 R2 assembly's fixed purple rod
  and both curved fixed-rod rails. Freeze source SHA-256
  `1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73`,
  focused STEP SHA-256
  `07c398b9b01233150dc4ca0805e2a7e2980f60fff302e1442654e0c3fb3f8f2c`,
  and full assembly STEP SHA-256
  `715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca`.
- Never touch `C=(0,0)`, world-fixed `A=(-15,-11)`, physical left/right
  `+45/-45 deg`, `qL(1)=(-18.384776310850235,+2.828427124746188)`,
  `qR(1)=(-2.828427124746192,-18.384776310850235)`, either `7.90 mm`
  curved rail, or the zero white-rod outer-rail count in the next task.
- The inherited P19 END-derived diagonal wire is **USER-REJECTED**. Correct
  only the wire to the established exact vertical leg + tangent R6 quarter arc
  + exact horizontal leg, with regressions against `REQ-002` and `REQ-017`.
- This escaped because P19 `build_workpiece_reference()` and its tests encoded
  the same contradictory diagonal assumption.
- Contract-opening clean HEAD: `a48c5697f9126dbb6934d764e48f2a01f6a01475`.
- Product baseline: exact P19 R1 `b69b6ad12af611644987f026eef4940db9c7bb34`.
- P20 R1 was rejected by the user because its round fixed-axle journal omitted
  the requested curved rotation rail and changed the effective outer rotation
  center from `C` to `A`. Preserve all P20 R1 files as rejected history.
- Corrected P20 R2 keeps `C=(0,0)`, fixed world axle candidate
  `A=(-15,-11)`, fixed inner plates, and physical left/right `+45/-45 deg`. Each outer
  plate needs a true curved inverse-frame fixed-axle rail.
- All white-rod outer rails and substitute apertures remain absent; all inner
  rails remain. Six white-rod/outer-solid collisions are deliberate,
  non-product evidence and must remain explicit.
- Future white-rod outer rails are one-at-a-time work because each interacts
  with its corresponding inner rail and neighboring outer rails.
- Next task is only `P20R2-DESIGN-01` and its phone-readable 2D intent gate.

## Rejected P20 R1 record

- Prior iteration: `p20-r1-fixed-rod-reset`.
- P20-DESIGN-01 and independent P20-CRITIC-01 remain immutable blocked
  product-gate evidence. The user has since authorized the same no-aperture,
  six-collision state as a deliberate evidence-only sequential scaffold.
- P20 scaffold implementation, focused repair, independent critic recheck,
  independent validator recheck, and formal scaffold review are complete.
  The exact scaffold fingerprint is `59ad1459...95c9`, verified `20/20`, and
  is accepted for scaffold conformance only.
- Contract-opening HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- Product input baseline: merged P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- P19 is retained as prior accepted digital evidence but superseded for
  forward product design by the user's rail-overlap/rotation failure report.

## Prior P19 fingerprint

- Active iteration: `p19-r1-front-edge-short-tail`.
- P19 R1 is digitally accepted for CAD, six written STEP artifacts, and exact
  Viewer handoff only.
- Exact candidate-manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- Independent validation: `PASS`, report SHA-256
  `304239aecb3b939a6ef1412d1b31979b4bafda2b2e997ca7e7311b36adfb88ef`.
- Formal review: `ACCEPT`, report SHA-256
  `7b5436c57070547b14241bc3de6cbc7047c07cbd1e4070b036f0d8d51040aba3`.
- Active handoff:
  `docs/iterations/p19-r1-front-edge-short-tail/HANDOFF.md`.

## Frozen current mechanism

- FRONT: `+Z` XT60 mating-head/up; `+Y` short-tail/tool right/outward.
- Three `OD4 x 50 mm` stainless rods, six permanent caps, four plates, one
  real fixed stepped axle at `A=(-13,-9)`; virtual rotation datum `C=(0,0)`.
- Shared motion only: `alpha_left=-5u`, `alpha_right=+5u`.
- Plate ODs `54.40/54.70/55.00 mm`; cutters `OD4.15 mm`.
- OPEN exact right angle; END exact ordered diagonal; identities unchanged.
- Six inverse-derived rail center travels are all at least `4.00 mm`.
- Minimum actual web `2.405845 mm`; rank `3`; worst condition `13.007687`.
- Completed-pigtail rigid removal is digitally clear by exactly the active
  `0.75 mm` nominal threshold, with zero actual-solid intersection.

## Next smallest action

Open only the wire correction and refactor the inherited diagonal reference to
the exact 90-degree vertical + R6 quarter arc + horizontal topology. Add a
requirement-level regression. Treat any requested fixed-rod/rail/source hash
change as a hard stop. Do not choose or add a white-rod outer rail.
