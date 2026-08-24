# P17 R2 current-lock removal validation

Status: fresh `P17-V06-R1` validation **PASS** for repaired fingerprint
`20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
The earlier blocked `P17-V06` receipt remains below as superseded history.

## P17-V06 independent validation receipt

- Owner/role: `/root/p17_lock_validator`, independent of design,
  implementation, critique, and formal review.
- Candidate-gate manifest:
  `/tmp/p17-r2-lock-removal-candidate-gate-input-manifest.txt`, SHA-256
  `e427c660362949763a1d79811abcc2b416a8214d3f83f955a2cbb08e08d9615c`.
  The manifest itself and all `39` listed inputs matched before validation and
  remained exact after deterministic, parity, and visual inspection.
- Verified candidate/source/test/provenance/manifest hashes:
  `c831a81999919746c4fb73e85b5ddac6201eb9d2535ca7b44143a0642ede3780` /
  `374236fa8dc3e0e5458a0e656a929e827cdbf01d81123e11fcb9d2c1780ef1cf` /
  `ad4a5281ed88b8f70a74c54f272f5355a107c16a77a7da490dead6de22b4ef12` /
  `ba713bf717b78c924ba73e952f2a1689a3237cc3da085ba57b9c77727d6eaae1` /
  `15a5da33662bf51c52515088f70ee091903c92f1ecd833f1eb75f1b2af49f87f`.

### Passing geometry and artifact evidence

- `uv run --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -q` ->
  all `33` focused tests reached `100%` with exit `0`.
- CAD `scripts/inspect validate` on all nine retained written STEP exports ->
  PASS with zero invalid-solid failures. Written occurrence counts were
  `9/16/8/18/26/26/63/26/13` for axle coupon, exploded, focused motion, full
  motion, endpoint, mid, open, cap coupon, and print kit.
- CAD `scripts/inspect refs --facts --planes --positioning` on all nine -> each
  returned `ok:true`, resolved topology/bounds/planes/placement facts, and no
  errors.
- Direct source-built versus imported written-STEP parity -> equal solid counts
  for every retained output; maximum bounds delta
  `6.25277607468888e-12 mm`, maximum summed-solid volume delta
  `2.21189111471176e-9 mm3`.
- Independent provenance audit -> all `22` recorded source, test, STEP,
  motion-source/sidecar, PNG, and GIF hashes matched. Fingerprint JSON hash,
  candidate-manifest binding, and adjacent fingerprint text all matched
  `c831a819...3780`. Neither retired lock-closeup file exists.
- Baseline-versus-candidate BREP subtraction proved no added replacement
  geometry: candidate-minus-baseline volume was zero for all four plates.
  Left-inner and left-outer symmetric differences were both zero, preserving
  the green `left_outer_secondary_grip_block` exactly. Right-inner removal was
  `242.335903107333 mm3`; right-outer removal was
  `17.7793255675006 mm3`; both surviving right plates remain positive-volume
  single solids.
- Baseline/current dataclass comparison found no changed common parameter.
  Exactly the `15` specified lock-only fields were removed, with no new field.
  Lock builders, lock evidence API, lock manifest object, lock labels, and
  lock-closeup output are absent; only the design-authorized internal
  compatibility endpoint names remain.
- `fixed_axle_actual_solid_evidence()` -> `33` samples and all aggregate
  collision/clearance booleans true: axle/outer, keeper/outer,
  axle/white-rod, keeper/cap, axle-guide probe, and XT60/service intersections
  remained zero. Minimum exact frozen-feature gap was `3.6500 mm`, minimum
  axle-guide radial clearance `0.150 mm`, and minimum keeper radial capture
  `1.050 mm`.
- `combined_contact_closure_evidence()` -> PASS for `66` side/sample rows;
  maximum prescribed residual `3.42888e-15 mm`, minimum rank-3 minor
  `3.600686e-4`, and maximum perturbed-pose error `7.30649e-12`.
- Purple axle math is internally sufficient for the current CAD stack:
  principal stack outer faces are at `-16.00/+16.00 mm`, axle ends are at
  `-17.45/+17.45 mm`, leaving `1.45 mm` per side for `0.25 mm` running
  clearance plus the `1.20 mm` keeper seat. This is not physical fit,
  stiffness, or retention proof.
- The user's physical stainless stock is `50.00 mm`; the current modeled white
  rod remains the separately derived `40.60 mm`. This mismatch is unresolved
  and no rod-length decision is accepted by this validation.
- Both motion sidecars expose exactly one visible control, `open_to_end`, and
  apply `-theta/+theta` only to the left/right outer plates. Each GIF contains
  `72` frames. Five stills plus frames `0/18/36/54/71` from both GIFs were
  visually inspected: the orange right-outer lock nose and source-identified
  right-inner receiver remain absent at open, intermediate, and endpoint
  poses; no replacement endpoint geometry appears; the green left grip,
  purple axle, both keepers, inner plates, outer plates, XT60 reference, rods,
  and caps remain where appropriate.

### Blocking findings

- `V06-01` — **major, source requirement semantics**: `P17R2Parameters` still
  rejects every modeled rod target at or above `45.0 mm` with the message
  `must not inherit the rejected 50 mm rod`. The corrected contract and latest
  user clarification establish that `50.00 mm` is the real stainless stock;
  only whether P17 uses that uncut stock is unresolved and frozen out of this
  lock-removal task. The current guard therefore turns an unresolved future
  decision into a false source-level rejection. Its associated test also
  requires the physical `50.00` fact to be absent from source. Repair must
  preserve the current `40.60 mm` candidate geometry while removing the false
  rejection and explicitly recording the physical-versus-modeled distinction.
- `V06-02` — **moderate, stale removed-lock evidence semantics**: service
  evidence still uses `released-open`, labels the sweep
  `completed_pigtail_actual_released_open...`, and returns/manifests the
  sequence `release -> full open -> ...`. After removal of the only release
  feature, those terms imply an operation that the candidate no longer has.
  Rename that evidence to begin at the fully open travel state and update the
  focused test/manifest wording without changing service geometry.

### Verdict and acceptance boundary

- Deterministic CAD geometry, written STEP validity/parity, collision/math/
  constraint checks, lock removal, green-grip preservation, and visual motion
  evidence: **PASS for this exact fingerprint**.
- User-requirement and evidence-semantics acceptance: **FAIL / repair
  required** because of `V06-01` and `V06-02`.
- Current fingerprint `c831a819...3780` must not advance to formal acceptance.
  The implementation owner should make the two wording/guard corrections,
  update tests and regenerated manifests/provenance as required, and issue a
  new candidate fingerprint for fresh C06/V06/R06 gates.
- Mesh, DfAM, slicer, 3MF, PETG, physical `50 mm` rod disposition, axle fit or
  stiffness, keeper/cap retention, force, heat, wear, vibration, wire holding,
  and physical acceptance remain unproven.

Tooling note: the first inspection attempt used the plugin root rather than
the installed `skills/cad/scripts` path and exited `2` before reading a STEP;
the corrected installed path was then used for all reported CAD inspection
results. No candidate input was changed by validation.

## P17-V06-R1 repaired-candidate validation receipt

- Owner/role: `/root/p17_lock_validator`, the same independent validator that
  blocked P17-I06 and distinct from design, implementation, critique, and
  formal review.
- Exact candidate fingerprint:
  `20fc5068814e5c3f5d9c58fdaffbb98bb5dba0eb8b4dffabc7eea59ff3e0cba1`.
- Repaired candidate-gate manifest:
  `/tmp/p17-r2-lock-removal-r1-gate-manifest.txt`, SHA-256
  `4707d17353a6c72a6556646db42298c2247a7df983ee63a95f08437e25bd8d53`.
  The manifest itself and all `13` listed inputs matched before validation and
  again immediately before this receipt was appended. This receipt changes
  `VALIDATION.md`, which was intentionally one of the frozen pre-receipt
  inputs; candidate source, tests, artifacts, and records did not drift.
- Verified source/test/provenance/candidate-manifest hashes:
  `371c9beff6909517b71d33ef5882df54997145e9373a1357d6d19bb34e29133b` /
  `b626047b6c2f6c764cb6a4107e5b64b1155054559c06f6dc6ac0ffc3d1e2429d` /
  `d51bc72aafffead0360f3e037ac932b8d64dface19a2b00a803093ccaab4b047` /
  `be993fa2a713abc86895aad95eb670eeb342237ff1e2d8e4799289cf07ef2590`.

### Blocker repair findings

- `V06-01` is resolved. Source now records physical stainless stock as
  `PHYSICAL_STAINLESS_STOCK_LENGTH_MM = 50.00`, retains the independently
  derived modeled white-rod target at exactly `40.60 mm`, and identifies use
  of the physical stock as an unresolved separate decision. The previous
  broad `>=45 mm` rejection and its false `rejected 50 mm rod` message are
  gone. The current guard freezes this candidate's modeled `40.60 mm` result
  without rejecting physical `50.00 mm` stock.
- `V06-02` is resolved. Active source/service evidence now starts with
  `move to full open`, the sweep label uses `full_open`, and returned/manifest
  sequences contain no `release` or `released` state. The remaining source
  word `rejected` appears only in an unrelated historical comment about the
  provisional D04 guide table; it is not a rod, stock, lock, release, or
  current-candidate claim.
- Focused scans found no active nose, receiver, ground arm, axial bridge, hard
  stop, flexure, lead-in, retaining-shoulder, or thumb-release source/record
  token. Design-authorized legacy endpoint identifiers remain internal only.

### Fresh deterministic checks

- `uv run --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -q` -> all
  `33` focused tests reached `100%`, exit `0`.
- Independent provenance audit -> all `22` recorded source, test, nine STEP,
  four motion-source/sidecar, and seven PNG/GIF hashes match. Fingerprint JSON,
  candidate-manifest binding, and adjacent fingerprint text all equal
  `20fc5068...0cba1`. Both retired lock-closeup files remain absent.
- Byte comparison to the blocked P17-I06 evidence -> all `9/9` STEP files and
  all `7/7` reviewed PNG/GIF files are unchanged. Therefore the prior exact-
  byte `inspect validate`, refs/positioning, and full visual review evidence
  applies without regeneration.
- Fresh source-built versus imported written-STEP parity on all nine outputs ->
  equal solid counts; maximum bounds delta `6.25277607468888e-12 mm`, maximum
  summed-solid-volume delta `2.21189111471176e-9 mm3`. This independently
  confirms the semantic source repair did not change generated solids.
- Fresh baseline/current BREP subtraction -> the green left outer grip and
  full left outer plate remain exact, with zero symmetric-difference volume;
  left inner is also exact. Candidate-minus-baseline volume remains zero for
  both right plates, proving no replacement geometry was added. Right-inner
  removal remains `242.335903107333 mm3`; right-outer removal remains
  `17.779325567501 mm3`; all four current plates are single solids.
- The full focused test run re-executed the 33-state collision/clearance and
  66-row closure gates. Frozen dimensions remain: principal stack `32.00 mm`,
  modeled rods `40.60 mm`, physical stock `50.00 mm` unresolved, purple axle
  `34.90 mm`; axle ends `-17.45/+17.45 mm` remain `1.45 mm` beyond plate faces
  `-16.00/+16.00 mm` for running clearance and keeper seating.
- Both unchanged sidecars still expose one visible `open_to_end` control with
  `OPEN to END OF TRAVEL`, rotate only outer plates by `-theta/+theta`, and
  retain the `32 deg` endpoint as prescribed travel rather than a lock claim.

### Verdict and boundaries

- P17-I06-R1 exact fingerprint `20fc5068...0cba1`: **P17-V06-R1 PASS**.
- Lock removal, green-grip preservation, frozen geometry, source/STEP parity,
  motion semantics, corrected service wording, and the 40.60-versus-50.00 rod
  distinction satisfy the bounded P17 R2 contract.
- This pass may advance to fresh formal review only if the candidate source,
  tests, STEP/motion/visual artifacts, provenance, manifest, and fingerprint
  remain unchanged. Appending gate receipts to continuity records is not a CAD
  candidate change.
- Physical `50.00 mm` stock use remains undecided. Mesh, DfAM, slicer, 3MF,
  PETG, axle/keeper/cap fit or stiffness, endpoint retention, force, heat,
  wear, vibration, wire holding, solder ergonomics, and physical acceptance
  remain unproven.
