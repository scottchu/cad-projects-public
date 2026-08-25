# P17 R2 current-lock removal handoff

Status: `P17-D08` design complete; implementation and candidate gates pending.

## Design receipt

- Owner/role: `/root/p17_lock_design`, independent design-contract owner.
- Verified baseline commit:
  `ea416dc2c120f362cdf079b4b82bb8722c58682a`.
- Verified baseline fingerprint:
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
- Verified design-input manifest:
  `/tmp/p17-r2-lock-removal-design-input-manifest.txt`, SHA-256
  `ac8f8dae624cb3291a615a4907ed5a899a35d45819f4aea02d7c93dfa4ada35d`.
- Screenshot 1 identifies the current right-outer lock nose. Screenshot 2
  identifies the green left-secondary finger/force grip tab, not a lock part;
  that grip remains frozen. Source inspection identifies the complete
  right-inner receiver as the nose's actual lock counterpart.
- Selected action: remove both halves and retire the lock-only production
  source/evidence surface; add no replacement lock.
- Endpoint: retain `0..32 deg` motion as travel only, with no hard-stop,
  detent, over-center, or self-lock claim.
- Version: remains P17 R2.

## Exact implementation task `P17-I06`

Use `BRIEF.md` and `DESIGN.md` in this directory as authority. The sorted
implementation-input manifest is
`/tmp/p17-r2-lock-removal-implementation-input-manifest.txt`, SHA-256
`68f02a05b96d4f5d043a948b39a5017869d52cbc218fc6c351d902e066cc7937`.
It freezes the design contract, current requirements/experience, source/tests,
artifact generators, accepted candidate records, and the two user screenshots.
Mutable handoff/review/validation status files are intentionally excluded.

Allowed implementation writes are limited to:

- `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`;
- `tests/test_p17_r2_direct_counter_twist.py`;
- `cad/p17_r2_direct_counter_twist/` generators, generated STEP, motion
  sidecars, provenance, manifest, fingerprint, and review evidence.

Required implementation outcome:

1. Remove the nose from the right outer plate and the complete receiver from
   the right inner plate.
2. Delete dead lock parameters, helpers, builders, evidence, manifest data,
   public exports, tests, and the tracked lock-closeup generator/export.
3. Preserve all frozen geometry and motion semantics; use `open_to_end` as the
   singular visible Viewer control while retaining only narrowly documented
   internal compatibility names.
4. Regenerate source-derived artifacts and provenance. Do not hand-edit STEP.
5. Produce deterministic and visual evidence specified in `DESIGN.md`.

The implementation owner must not approve its own candidate. Return a receipt
with verified input fingerprint, changed/retired paths, exact commands and
results, new candidate fingerprint and provenance hashes, requirement
coverage, visual evidence paths, unresolved risks, and next action.

## Required downstream gates

- `P17-C06`: distinct critic challenges whether the screenshot-1 lock nose and
  its source-identified right-inner receiver are truly gone, whether the
  screenshot-2 green grip remains unchanged, whether hidden lock remnants or
  accidental geometry changes remain, and whether endpoint wording
  overclaims.
- `P17-V06`: distinct validator independently checks the exact candidate,
  actual solids, equations, frozen semantic tuples, STEP/source parity,
  snapshots/GIFs, artifact retirement, and visible `open_to_end` control.
- `P17-R06`: distinct formal reviewer joins C06 and V06 for the exact unchanged
  candidate fingerprint.
- Continuity/delivery updates occur only after R06.

## Unresolved risks

- Physical `50.00 mm` stainless stock does not match the current P17 modeled
  `40.60 mm` rod target. This iteration records the distinction but cannot
  decide it.
- The purple `34.90 mm` axle is mathematically long enough for the current
  stack and keeper seats, but print fit, stiffness, keeper retention, and real
  assembly remain untested.
- After removing the lock, P17 R2 has no accepted endpoint retention feature.
  Wire-holding force, back-drive, vibration resistance, and self-lock remain
  explicitly unclaimed.

## P17-I06 implementation receipt

- Status: implementation candidate complete; independent critique, validation,
  and formal review pending.
- Owner/role: `/root/p17_lock_impl`, distinct implementation owner.
- Verified baseline commit:
  `ea416dc2c120f362cdf079b4b82bb8722c58682a`.
- Verified implementation-input manifest:
  `/tmp/p17-r2-lock-removal-implementation-input-manifest.txt`, SHA-256
  `68f02a05b96d4f5d043a948b39a5017869d52cbc218fc6c351d902e066cc7937`;
  all `23` listed paths matched before implementation.
- Candidate fingerprint:
  `c831a81999919746c4fb73e85b5ddac6201eb9d2535ca7b44143a0642ede3780`.
- Source/test hashes:
  `374236fa8dc3e0e5458a0e656a929e827cdbf01d81123e11fcb9d2c1780ef1cf` /
  `ad4a5281ed88b8f70a74c54f272f5355a107c16a77a7da490dead6de22b4ef12`.
- Provenance/candidate-manifest hashes:
  `ba713bf717b78c924ba73e952f2a1689a3237cc3da085ba57b9c77727d6eaae1` /
  `15a5da33662bf51c52515088f70ee091903c92f1ecd833f1eb75f1b2af49f87f`.

### Implemented scope

- Removed the complete orange right-outer nose and the complete right-inner
  receiver, including ground arm, axial bridge, hard stop/rib, flexure, ramp,
  retaining shoulder, and thumb-release tab. No replacement lock, stop,
  bridge, bar, yoke, boss, linkage, or stability structure was added.
- Removed every lock-only parameter, validation branch, geometry helper,
  builder, evidence function, public export, manifest field, and positive
  lock test. Added negative-presence and exact plate-volume regression tests.
- Deleted tracked `p17_r2_lock_closeup.step.py` and
  `p17_r2_lock_closeup.step`; removed lock-closeup review images and all
  lock-closeup entries from current provenance/fingerprint/manifest records.
- Preserved compatibility identifiers `locked`, `theta_lock_deg`, and
  `GuidePath.locked` only as internal endpoint names. Both Viewer sidecars now
  expose one visible normalized control, `open_to_end`, labelled
  `OPEN to END OF TRAVEL`; no `open_to_lock` control remains.

### Frozen geometry and delta evidence

- Purple stepped axle remains `34.90 mm`; principal stack remains `32.00 mm`;
  per-side axle construction remains `8.25 mm`; modeled white-rod target
  remains `40.60 mm`. Physical `50.00 mm` stainless stock is recorded but not
  substituted or resolved in this task.
- Left-inner volume remained `6401.617269691559 mm3`; left-outer volume
  remained `8306.767693237123 mm3`.
- Right-inner volume changed from `6643.953172798893` to
  `6401.617269691560 mm3`, an exact removal of `242.335903107333 mm3`.
- Right-outer volume changed from `8870.838945923684` to
  `8853.059620356184 mm3`, an exact removal of `17.779325567500 mm3`.
- Both surviving right plate bodies are valid positive-volume single solids.
  Guide slots, axle-guide slots, hex bores, completed-pigtail windows, plate
  diameters/thicknesses, left grip, rod/cap geometry, XT60/service envelopes,
  `A`, `C`, and `0..32 deg` counter-motion were unchanged.

### Commands and results

- `uv run --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -q`
  followed by the conditional sentinel ->
  `P17_I06_PYTEST_PASS_33` (`33` tests).
- CAD `scripts/gen` on the nine explicit retained generator paths with
  `--write` -> all nine STEP/render packages built.
- CAD `scripts/inspect refs <each retained STEP> --facts --planes
  --positioning` -> all nine resolved with occurrence, topology, bounds,
  plane, and placement facts.
- CAD `scripts/inspect validate <each retained STEP>` -> all nine PASS; every
  solid valid, closed, and positive-volume. Retained STEP occurrence counts
  were `9/16/8/18/26/26/63/26/13` for center-axle coupon, exploded, focused
  motion, full motion, endpoint, mid, open, cap coupon, and print kit.
- Direct source-built versus imported written-STEP parity across all nine
  retained outputs -> equal solid counts, maximum bounds delta
  `6.253e-12 mm`, maximum summed-solid-volume delta `2.212e-9 mm3`.
- `fixed_axle_actual_solid_evidence()` -> `33` samples with zero axle/outer,
  keeper/outer, axle/white-rod, keeper/cap, axle-guide-probe, and
  XT60/service unintended intersections; minimum exact feature gap
  `3.6500 mm`, axle-guide radial clearance `0.150 mm`, and keeper radial
  capture `1.050 mm`.
- `combined_contact_closure_evidence()` -> PASS for `66` side/state rows;
  maximum residual `3.429e-15 mm`, minimum rank-3 minor `3.600686e-4`, and
  maximum perturbed-pose error `7.306e-12`.
- Provenance audit -> all `20` recorded STEP, motion-source/sidecar, and
  selected PNG/GIF hashes match; fingerprint JSON hash matches both candidate
  manifest and adjacent text value; no lock-closeup artifact remains.

### Visual evidence and findings

- Focused open/mid/end/opposed end PNGs:
  `cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i06_fixed_*_20260824T222951Z.png`.
- Full end PNG:
  `cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i06_full_end_20260824T223057Z.png`.
- Focused/full motion GIFs:
  `cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i06_fixed_motion_20260824T223033Z.gif`
  and
  `cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i06_full_motion_20260824T223033Z.gif`.
- All five PNGs and both 72-frame GIFs rendered `ok:true`, `warnings:[]` and
  were visually inspected. The orange fork/nose and right-inner receiver/
  bridge/catch are absent at open, mid, end, and through focused/full motion.
  The purple axle, two keepers, fixed inner plates, opposite outer rotations,
  XT60 reference, three white rods, and six caps remain visible in the
  appropriate evidence.

### Claim boundary and next action

- `32 deg` is only the prescribed travel endpoint; no hard-stop, detent,
  over-center capture, retention, or self-lock is claimed.
- CAD/source and written STEP generation are complete for this implementation
  candidate. Mesh, DfAM, slicer, 3MF, PETG, force, fit, keeper/cap retention,
  heat, wear, vibration, wire holding, and physical acceptance are not proven.
- Route exact fingerprint `c831a819...3780` to `P17-C06`, `P17-V06`, then
  `P17-R06`. Any source, test, generator, sidecar, STEP, selected review
  artifact, provenance, or fingerprint change invalidates those gates.

## Post-implementation factual visual correction

- Full-resolution review corrects the earlier screenshot mapping: screenshot
  2 circles the retained green `left_outer_secondary_grip_block`, an integral
  finger/force tab, not the right-inner receiver.
- The implemented source outcome remains correct: screenshot 1's orange nose
  and the source-identified right-inner receiver are the two current-lock
  halves and are removed; the green left grip is retained and its baseline
  volume is unchanged.
- C06/V06 must use the corrected mapping and the post-correction candidate-gate
  manifest recorded below, not the superseded statement that both circles
  showed lock parts.
- Corrected candidate-gate input manifest:
  `/tmp/p17-r2-lock-removal-candidate-gate-input-manifest.txt`, SHA-256
  `e427c660362949763a1d79811abcc2b416a8214d3f83f955a2cbb08e08d9615c`.
  All listed hashes were verified after the factual correction. It freezes
  corrected immutable design/current-state docs, exact candidate source/tests,
  all nine retained generators and STEP exports, both motion sidecars, selected
  PNG/GIF evidence, provenance/fingerprint records, and both supplied
  screenshots. Mutable handoff/review/validation status is excluded.

## P17-I06-R1 semantic repair receipt

### Input and scope

- Verified `/tmp/p17-r2-lock-semantic-repair-input-manifest.txt` at SHA-256
  `60873c78ff74f5bb40010826c9ba9af690ca15d650043d258b66ba8fc4702f7a`;
  all `13/13` listed path hashes matched before repair.
- Repair baseline fingerprint was
  `c831a81999919746c4fb73e85b5ddac6201eb9d2535ca7b44143a0642ede3780`.
- This cycle changed semantics, guards, tests, and candidate records only. It
  did not change CAD geometry, STEP geometry, motion transforms, screenshot
  mapping, any path, or any plate/axle/rod/cap/guide/XT60 dimension.

### Semantic repair

- Active service wording is now `move to full open -> lift to window
  centerline -> +Y extraction`; production evidence no longer implies a
  release mechanism or released state.
- The candidate's modeled white-rod target remains exactly `40.60 mm`.
  Physical stainless stock is explicitly `50.00 mm`; whether or how that stock
  is used remains a separate unresolved physical decision. No text or guard
  calls the physical stock rejected.
- The broad `>=45 mm` rejection guard was replaced by the exact current-model
  invariant `rod_length_target == 40.60 mm`. Regression tests assert that the
  modeled target and physical stock are distinct.
- Only the design-approved internal endpoint compatibility identifiers remain:
  `locked`, `theta_lock_deg`, `GuidePath.locked`, and the retained
  `p17_r2_locked.step` artifact name. Viewer-facing control remains singular
  `open_to_end`.

### Verification and immutable artifacts

- Focused semantic/contract selection -> `5 passed`.
- Full P17 focused file -> `33` tests reached `[100%]` with sentinel
  `P17_I06_R1_FULL_PASS_33`.
- Provenance hash audit -> `22/22`: source, tests, nine STEP files, two motion
  generators, two motion sidecars, five PNGs, and two GIFs all match their
  recorded hashes.
- All `9/9` retained STEP hashes and all `7/7` selected PNG/GIF hashes are
  byte-identical to blocked candidate P17-I06. No STEP, snapshot, or GIF was
  regenerated because geometry, transforms, and visual evidence were frozen.
  The existing focused open/mid/end/opposed-end and full end/motion evidence
  therefore continues to show both removed circled lock features absent.

### Candidate records

- Source SHA-256:
  `371c9beff6909517b71d33ef5882df54997145e9373a1357d6d19bb34e29133b`.
- Test SHA-256:
  `b626047b6c2f6c764cb6a4107e5b64b1155054559c06f6dc6ac0ffc3d1e2429d`.
- Provenance SHA-256:
  `d51bc72aafffead0360f3e037ac932b8d64dface19a2b00a803093ccaab4b047`.
- Candidate fingerprint SHA-256:
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
- Candidate manifest SHA-256:
  `be993fa2a713abc86895aad95eb670eeb342237ff1e2d8e4799289cf07ef2590`.
- Selected evidence remains under
  `cad/p17_r2_direct_counter_twist/snapshots/p17_r2_i06_*` and exact artifact
  hashes remain recorded in `p17-r2-artifact-provenance.json`.

### Boundary and routing

- Purple axle remains `34.90 mm`; white modeled rods remain `40.60 mm`;
  physical stainless stock remains `50.00 mm` and unresolved. No replacement
  stop, lock, detent, catch, bridge, bar, or linkage was added.
- Route exact P17-I06-R1 fingerprint `20fc5068...0cba1` through fresh independent
  `P17-C06`, `P17-V06`, and `P17-R06` gates. Physical stock/use, print fit,
  retention, force, heat, wear, wire holding, and physical acceptance remain
  outside this semantic repair.

## P17-R06 formal review and critic-join receipt

- Status: split formal verdict. Exact repaired fingerprint
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`
  is accepted for CAD source and written STEP/export evidence only; live Viewer
  delivery is blocked pending ready-artifact verification; no physical
  acceptance is recorded.
- Owner/role: `P17-R06`, distinct formal reviewer and acceptance-boundary
  arbiter. This role did not perform implementation, C06 critique, V06
  validation, source repair, or Viewer/cache mutation.
- Formal input manifest:
  `/tmp/p17-r2-lock-r06-input-manifest.txt`, SHA-256
  `7d112debd0e740592a6936eaa777975812c8aa421f275029760b1e035f4e3e9b`;
  all listed path hashes matched.
- Joined critic provenance: parent-supplied independent `P17-C06-R1` PASS/no
  blocker message for this candidate, recorded here without claiming R06
  performed critique.
- Joined validator provenance: active `VALIDATION.md` `P17-V06-R1` PASS for
  the same candidate fingerprint, with the initial blocker and semantic repair
  audit preserved.
- Matched hashes: provenance
  `d51bc72aafffead0360f3e037ac932b8d64dface19a2b00a803093ccaab4b047`,
  candidate manifest
  `be993fa2a713abc86895aad95eb670eeb342237ff1e2d8e4799289cf07ef2590`,
  source
  `371c9beff6909517b71d33ef5882df54997145e9373a1357d6d19bb34e29133b`,
  tests `b626047b6c2f6c764cb6a4107e5b64b1155054559c06f6dc6ac0ffc3d1e2429d`.
- Formal checks: `33` focused tests passed; `open_to_end` is the only visible
  motion control; `open_to_lock` is absent; no replacement lock/stop/catch/
  bridge/bar/linkage is present; all `9` STEP and `7` selected visual artifact
  hashes are unchanged across the semantic repair.
- Corrected visual mapping enforced: screenshot 1's orange right-outer nose is
  removed; screenshot 2's green left-outer grip is retained; the
  source-identified right-inner receiver counterpart is removed.
- Viewer blocker: the supplied Tailscale page and active local Viewer page
  returned HTTP `200`, but the exact `/__cad/artifact` endpoint did not return
  `state: ready` under read-only review. Earlier probing returned
  `needs-build`/`stale_step_artifact`; subsequent local/Tailscale artifact
  probes timed out. Therefore `assembly.json`, params module, and component GLB
  readiness were not accepted.
- Boundary: physical `50.00 mm` stainless rod stock remains unresolved and
  distinct from modeled `40.60 mm` white rods; purple axle remains modeled
  `34.90 mm` with `1.45 mm` per side beyond the `32.00 mm` four-plate stack.
  No physical cap fit, keeper retention, lock force, self-lock, heat, wear,
  creep, springback, vibration, slicer, mesh/DfAM, 3MF, PETG, or assembly claim
  is made.
- Next action: for CAD/export delivery, preserve exact fingerprint
  `20fc5068...0cba1` and the physical boundary above. For live preview
  delivery, authorize a Viewer artifact refresh/rebuild and recheck page HTTP
  `200`, `/__cad/artifact` HTTP `200` with `state: ready`, actual
  `assembly.json`, params module, and one component GLB HTTP `200` before
  claiming Viewer acceptance.

## P17-R06 Viewer repair follow-up receipt

- Status: live Viewer/runtime preview accepted after root's authorized artifact
  rebuild and R06 read-only recheck. Final combined R06 verdict is ACCEPT for
  exact candidate
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1` for CAD
  source, written STEP/export evidence, and live Viewer preview. Physical
  acceptance remains explicitly unrecorded.
- Repair provenance joined without claiming R06 performed it: root reported the
  prior Viewer blocker was the singleton build importing the canonical-checkout
  editable package instead of this worktree's new P17 module, then rebuilt the
  focused package without changing source/service/geometry using
  `uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad/scripts/artifact projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py --force --verbose`.
- Root-reported rebuild result: `ok: true`, source hash
  `5df821aea698153885f7b379e79e482679b0e6fba64522f03730bc16dc453876`, STEP hash
  `b1d190430f86d1243842048a28d3357aa9ff4c0a8d99bd8a84a389f898e4aeab`, package
  under this worktree's `__cadgen__`.
- R06 read-only Viewer evidence: singleton `/__cad/server` returned HTTP `200`
  on localhost and Tailscale with `pid: 92779`, port `3245`, and
  `stepArtifactGenerationAvailable: true`; focused pages returned HTTP `200` on
  localhost and on the supplied Tailscale URL.
- Exact `/__cad/artifact?dir=<worktree>&file=<focused source>` returned HTTP
  `200` and `state: ready` on both localhost and Tailscale.
- Catalog/package evidence: source-kind `python`, kind `assembly`, source hash
  `5df821aea698153885f7b379e79e482679b0e6fba64522f03730bc16dc453876`, package
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/__cadgen__/models/p17_r2_fixed_axle_motion.step.py`.
- Payload evidence: `assembly.json` returned HTTP `200` on both routes with
  `schemaVersion: 2`, `packageSchemaVersion: 3`, `6` components, `8`
  occurrences, and STEP hash
  `b1d190430f86d1243842048a28d3357aa9ff4c0a8d99bd8a84a389f898e4aeab`.
- Params module returned HTTP `200` on both routes with SHA-256
  `7f5e6906bf73a019b2908430d0d58d348aeac0528a087d57ffede7fb62c346e7`;
  visible parameter surface remains singular `open_to_end`, and
  `open_to_lock` count is `0`.
- Component GLB `3bb3ae3413a94ba0` returned HTTP `200` on both routes with
  content type `model/gltf-binary`, `137340` bytes, and `glTF` magic.
- Boundary unchanged: no physical rod-stock decision, PETG, mesh/DfAM,
  3MF/slicer, cap/keeper fit, heat, wear, creep, springback, vibration, wire
  holding, retention force, self-lock, or assembly acceptance is claimed.
