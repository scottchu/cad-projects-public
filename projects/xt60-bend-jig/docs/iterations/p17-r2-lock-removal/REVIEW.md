# P17 R2 current-lock removal review

Status: `P17-R06` final combined verdict recorded. Exact repaired candidate
`20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`
is ACCEPTED for CAD source, written STEP/export evidence, and the repaired live
Viewer preview route. No physical acceptance is recorded.

## P17-R06 formal review receipt

- Owner/role: `P17-R06`, distinct formal reviewer and acceptance-boundary
  arbiter. This role did not implement, critique, validate, repair source, or
  mutate Viewer state.
- Formal input manifest:
  `/tmp/p17-r2-lock-r06-input-manifest.txt`, SHA-256
  `7d112debd0e740592a6936eaa777975812c8aa421f275029760b1e035f4e3e9b`;
  all listed entries matched by path and content.
- Candidate fingerprint:
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
- Provenance, candidate-manifest, source, and test hashes matched:
  `d51bc72aafffead0360f3e037ac932b8d64dface19a2b00a803093ccaab4b047`,
  `be993fa2a713abc86895aad95eb670eeb342237ff1e2d8e4799289cf07ef2590`,
  `371c9beff6909517b71d33ef5882df54997145e9373a1357d6d19bb34e29133b`,
  and `b626047b6c2f6c764cb6a4107e5b64b1155054559c06f6dc6ac0ffc3d1e2429d`.
- Pre-write records matched the R06 input manifest: `VALIDATION.md`
  `7f1d989e87901a1b175c65adae96299a26616401b37b7b788215ef4da31e7afc`,
  `HANDOFF.md`
  `db6d184e7e457a85562215612c20396dbf77a3103d98a3f0089ffff6146c8f5b`,
  and `REVIEW.md`
  `6433fb2c3695cdce3af0cf34e39b48c6dd892ad9c6b072c49560b876a0f20eef`.

## Joined independent gates

- Critic gate: joined the parent-supplied independent `P17-C06-R1` PASS/no
  blocker message as critic provenance. This formal review records that
  provenance without claiming to have performed C06.
- Validator gate: joined active `VALIDATION.md` `P17-V06-R1` PASS for the same
  candidate fingerprint, including preserved initial blocker history and the
  subsequent semantic-repair audit.
- Correct visual mapping is enforced: screenshot 1's orange right-outer lock
  nose is removed; screenshot 2's green left-outer secondary grip is retained;
  the source-identified right-inner receiver counterpart is removed.

## Deterministic acceptance

Decision: ACCEPT for unchanged CAD source, written STEP/export evidence, and
static preview artifacts associated with exact fingerprint
`20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.

Evidence checked:

- Focused test command:
  `uv run --project projects/xt60-bend-jig pytest -q
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py` -> `33`
  tests passed.
- Source-side visible Viewer control is singular `open_to_end`; `open_to_lock`
  is absent from source, tests, and current motion sidecars.
- No replacement lock, stop, catch, bridge, bar, yoke, linkage, or stability
  structure is present in the candidate records.
- All `9/9` retained STEP hashes and `7/7` selected PNG/GIF visual evidence
  hashes are byte-identical across the semantic repair; the retired
  lock-closeup source and STEP are absent from the candidate artifact set.
- Visual spot checks match the corrected contract: orange right-outer nose
  absent, green left grip retained, right-inner receiver absent, and no new
  endpoint lock visible.
- The candidate preserves fixed inner guides, opposite independent outer
  rotations, larger force outer geometry, completed-pigtail service window,
  permanent cap/coupon strategy, four-plate layout, and version semantics for
  this R2 current-lock removal scope.

## Live Viewer delivery boundary

Decision: BLOCKED for live Viewer/runtime preview acceptance.

Read-only probes did not verify the required ready artifact state:

- Supplied Tailscale page URL returned HTTP `200`.
- Active local Viewer was found on port `3245`; the focused page returned HTTP
  `200`.
- The exact focused `/__cad/artifact` endpoint did not return `state: ready`.
  Earlier read-only probing returned HTTP `200` with `state: needs-build` and
  `reason: stale_step_artifact`; subsequent local artifact probes timed out on
  port `3245`, and the Tailscale artifact probe timed out.
- Because the artifact endpoint was not ready, `assembly.json`, the params
  module, and a component GLB were not formally verified in this review.

This is a delivery/runtime blocker only. It does not invalidate the deterministic
CAD/source/export acceptance above, but no PR or handoff should claim live
Viewer readiness until a separately authorized owner refreshes the exact Viewer
artifact and rechecks page HTTP `200`, `/__cad/artifact` HTTP `200` with
`state: ready`, actual `assembly.json`, params module, and at least one
component GLB HTTP `200` on the intended localhost/Tailscale route.

## Physical and manufacturing boundaries

- Physical `50.00 mm` stainless rod stock remains unresolved and is distinct
  from the modeled white rods at `40.60 mm`.
- The purple stepped axle remains modeled at `34.90 mm`, equal to the `32.00 mm`
  four-plate stack plus `1.45 mm` per side beyond the stack.
- No physical cap fit, keeper retention, lock force, self-lock, bevel hardware,
  heat, wear, creep, springback, vibration, slicer, 3MF, PETG, mesh/DfAM, or
  assembly acceptance is claimed.

## Next action

If the delivery target is CAD source and written STEP/export evidence, proceed
with the exact accepted fingerprint and preserve the physical boundary above.
If the delivery target includes live preview, first authorize a Viewer artifact
refresh/rebuild by the appropriate owner, then rerun the exact ready-state,
`assembly.json`, params, and component-GLB checks before claiming Viewer
acceptance.

## P17-R06 Viewer repair follow-up acceptance

Status: ACCEPTED for live Viewer/runtime preview after root's authorized
artifact rebuild and this read-only R06 recheck. This supersedes the earlier
R06 Viewer blocker above; the CAD/source/export acceptance and physical boundary
are unchanged.

Repair provenance joined without claiming R06 performed it: root reported the
singleton Viewer build issue was the canonical-checkout editable package import
path, then rebuilt the focused render package without source/service/geometry
changes using:

`uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad/scripts/artifact projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py --force --verbose`

Root-reported rebuild result: `ok: true`, source hash
`5df821aea698153885f7b379e79e482679b0e6fba64522f03730bc16dc453876`, STEP hash
`b1d190430f86d1243842048a28d3357aa9ff4c0a8d99bd8a84a389f898e4aeab`, package
under the current worktree `__cadgen__`.

Read-only R06 Viewer checks:

- Singleton Viewer/server is running on port `3245`; `/__cad/server` returned
  HTTP `200` on localhost and Tailscale with `pid: 92779` and
  `stepArtifactGenerationAvailable: true`.
- Exact focused page returned HTTP `200` on localhost and on the supplied
  Tailscale URL.
- Exact `/__cad/artifact?dir=<worktree>&file=<focused source>` returned HTTP
  `200` and `state: ready` on both localhost and Tailscale.
- Catalog entry resolved to source-kind `python`, kind `assembly`, package
  `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/__cadgen__/models/p17_r2_fixed_axle_motion.step.py`,
  and source hash
  `5df821aea698153885f7b379e79e482679b0e6fba64522f03730bc16dc453876`.
- `assembly.json` returned HTTP `200` on both routes with `schemaVersion: 2`,
  `packageSchemaVersion: 3`, `kind: assembly-package`, `6` components, `8`
  occurrences, and STEP hash
  `b1d190430f86d1243842048a28d3357aa9ff4c0a8d99bd8a84a389f898e4aeab`.
- Params module returned HTTP `200` on both routes; SHA-256
  `7f5e6906bf73a019b2908430d0d58d348aeac0528a087d57ffede7fb62c346e7`.
  The visible parameter surface remains singular `open_to_end`;
  `open_to_lock` count is `0`.
- Component GLB `3bb3ae3413a94ba0` returned HTTP `200` on both routes with
  content type `model/gltf-binary`, `137340` bytes, and `glTF` magic.

Final R06 boundary: exact candidate
`20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1` is accepted
for CAD source, written STEP/export evidence, and live Viewer preview. Physical
rod length, PETG, mesh/DfAM, 3MF/slicer, cap/keeper fit, heat, wear, creep,
springback, vibration, wire holding, retention force, self-lock, and assembly
acceptance remain unproven.
