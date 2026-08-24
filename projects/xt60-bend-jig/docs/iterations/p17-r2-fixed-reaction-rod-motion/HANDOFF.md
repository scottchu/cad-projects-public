# P17 R2 fixed stepped-axle guide handoff

Status: `P17-D07` focused datum repair complete; implementation and all
candidate acceptance gates pending. Same P17 R2 identity.

## P17-D07 receipt

- Owner/role: `/root/p17_fixed_rod_design`, independent datum-repair designer.
- D06 STOP evidence: provisional `A=(-18.00,17.00)` caused actual cutter
  intersections `68.3212367/34.0035540/128.9744351 mm^3` and signed webs
  `-3.915/-2.195/-5.042 mm` against `+2.20 mm` required.
- Corrected datums: `C=(-10.60,17.00)`, `A=(-29.00,17.00)`, `e=18.40 mm`.
  White rods, their loci, lock, caps, stack, and plate dimensions stay frozen.
- Search evidence: same-Z feasible sampled region was approximately
  `A_y=-27.5..-30.5 mm`; selected `A_y=-29.0` gave analytic minimum web
  `3.849 mm`.
- Actual-solid evidence at selected `A`: zero cutter intersections; minimum
  frozen-feature gap `3.650 mm`; inner/left/right boundary webs
  `3.8946/7.650/9.150 mm`; all four local plates valid one-solid results.
- Motion probe: over 33 states, unintended axle/outer, keeper/outer,
  axle/white-rod, and keeper/cap intersection volumes were zero. Minimum
  radial axle/guide clearance was `0.150 mm`, keeper radial capture
  `1.050 mm`, and XT60/service clearance `19.1764973 mm`.
- Kinematic math: reconstruction error `<=7.11e-15 mm`, mirror error zero.
- Physics boundary: one fixed axle in one arc slot is not a revolute joint.
  Acceptance still requires the unchanged white-rod contact network plus the
  axle guide to reconstruct one pose at every sampled `theta`.
- Design evidence is not candidate validation and is not physical proof.

## Frozen implementation input

Sorted path/content manifest:
`/tmp/p17-d07-implementation-input-manifest.txt`; SHA-256
`c9085b63a5512ef61f8c01f6191d6445765cd7cc1a2107575e3c0badbfc357c3`.
It freezes the corrected requirements, experience entry, brief, design,
current WIP source/test failure baseline, and four supplied images. Relevant
contract hashes are:

- `REQUIREMENTS.md`: `9a2742a31513526f382bc84a7ed1f7624819430bad0591d4505dac7914ced84c`
- `EXPERIENCE.md`: `cf61fae5f12ceca01d96cffd91181ff2a75d8a2303d8b3a21238147526679799`
- `BRIEF.md`: `b50b03d2c4277a71caff98b4fff50d78cad2a93df6784fb0747ad62022668598`
- `DESIGN.md`: `f7462b5916a5fb7972df8b9fa47d03eea56a5bb1b4725f9ded452bfdbb2b21e1`
- source failure baseline: `7f52f3c0f73be24bd86be8d829e6c03b03ceb0dbec02579f8d8c7b9851d745d4`
- focused-test failure baseline: `ecc52b38612bef34c9f714d3194c15d935642a313ead0a2e2384d3d5deede747`

Any input-path hash change invalidates only the dependent P17-I05 gates and
requires a refreshed receipt; it does not automatically change version.

## Exact next task: P17-I05

Distinct implementation owner may edit only the authorized P17 source,
focused tests, generated STEP/motion entries, and candidate review artifacts.
Implement `A=(-29.00,17.00)`, preserve `C`, frozen white-rod/lock/cap tuples,
generate the two mirrored `7.90 mm` axle guides, and keep axle/inners/keepers
world-invariant while only outers rotate `-theta/+theta` about `C`.

Done gate: focused regressions pass; exact-solid web/collision results meet the
D07 numbers/tolerances; the unchanged contact network plus axle guide closes
to one pose at every sample; focused Viewer motion and full-assembly sampled
motion are both visible; candidate fingerprint and reproducible artifacts are
returned without self-approval.

Stop if closure requires changing any white-rod path, adding structure, or
moving another frozen datum. Route the exact candidate independently to
`P17-C05`, `P17-V05`, then `P17-R05` as defined in `BRIEF.md`.

## P17-I05 implementation receipt

- Status: implementation candidate complete; not self-approved. Candidate
  fingerprint is
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
  Verified D07 input manifest is
  `c9085b63a5512ef61f8c01f6191d6445765cd7cc1a2107575e3c0badbfc357c3`.
- Owner/role: `/root/p17_fixed_rod_impl`, distinct implementation owner.
- Source/test hashes:
  `3df2574dc571ba37f24125d6cc1028d67273841d7c4951359f676fd07de46000` /
  `20145cfea70b483cb0b1e7efc7f418d6bea744fbc713a18e6500612702e0aeb7`.
- Identity and scope: the purple printed stepped axle, both keepers and both
  inner plates are world-fixed at `A=(-29,17)`; outer outlines still rotate
  about `C=(-10.6,17)` in opposite senses. All three white OD4 rods remain
  moving forming/locking rods. Frozen white-rod loci, lock, caps, stack and
  plate dimensions retain semantic hash
  `a6c25c8977c2c9debe9838c0c60ee74bb9f28dbe0e1c1a9167c29d9ce594dec5`.
  No bar, boss, linkage or decorative center hole was added.
- Math/constraint gate: both 33-sample `7.90 mm` mirrored axle guides preserve
  radius `18.40 mm`; reconstruction error is at most `7.11e-15 mm` and mirror
  error is zero. Existing three-white-rod contacts plus the axle guide pass
  local rank-3 closure at all 66 side/state rows; two perturbed solves per row
  return to the prescribed pose with maximum error `7.31e-12` and minimum
  rank-3 minor `3.60e-4`.
- Actual-solid gate: exact frozen-feature gap `3.6500 mm`; analytic minimum web
  `3.84868 mm`; inner/left/right boundary webs
  `3.8946/7.650/9.150 mm`; axle-guide radial clearance `0.150 mm`; keeper
  radial capture `1.050 mm`; XT60/service clearance `19.1764973 mm`. Across
  33 states, axle/outer, keeper/outer, axle/white-rod, keeper/cap and
  fixed-member/service unintended intersections are all zero; the probe at C
  confirms solid material rather than an empty decorative bore.
- Test commands: `uv run pytest -q .../test_p17_r2_direct_counter_twist.py
  -k 'd06_'` -> `8 passed`; full focused file -> `31 passed`.
- Artifact commands: CAD `scripts/gen` wrote all ten affected STEP/render
  packages; `scripts/inspect validate` returned `ok:true failureCount:0` for
  all ten. Generator/export refs show exactly matching occurrence/topology
  summaries and bounds; maximum bound delta is `0.0 mm`.
- Motion/review artifacts: source-declared focused
  `p17_r2_fixed_axle_motion.step.py` + self-contained JS sidecar transforms
  only left/right outer occurrences. Full-assembly
  `p17_r2_full_motion.step.py` + sidecar also shows the unchanged white rods
  and caps moving. Eleven PNG and two 72-frame GIF artifacts rendered
  `ok:true warnings:[]` and were visually inspected. Purple axle/keepers and
  inners remain fixed, green/blue outers counter-rotate, C remains filled, all
  three white rods remain present in the full packet, and exploded separation
  is confined to the explicitly exploded artifact.
- Environment receipt: root `uv sync --all-packages --all-groups` did not add
  Python Playwright. With root authorization, CAD skill requirements were
  installed into the existing sole root `.venv` using `uv pip install
  --python .venv/bin/python -r .../skills/cad/requirements.txt`; no alternate
  environment or dependency/lock-file edit was created.
- Provenance package:
  `cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json` SHA-256
  `4de4d236f67729b142b0ae0752ef41fe3087a9c191890947695f7ff72dc4be37`;
  candidate manifest/fingerprint and `.txt` are adjacent. STEP and review
  artifact hashes are recorded in provenance.
- Remaining risks: this is nominal CAD/contact closure, not force, friction,
  self-lock, tolerance, PETG fit, wire holding or physical proof. The focused
  motion intentionally omits white rods for axle clarity; the full-motion GIF
  is the non-hidden assembly evidence. Singleton CAD Viewer serving and exact
  page/artifact readiness remain the root handoff owner's task.
- Next action: route this exact fingerprint independently to `P17-C05`, then
  `P17-V05`, then `P17-R05`; any source, test, generator, sidecar, STEP or
  selected review-artifact change requires a new fingerprint and re-run of
  dependent gates.

## P17-V05 independent validation receipt

- Status: PASS for digital CAD/export validation of candidate fingerprint
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
  This is not physical force, fit, tolerance, PETG, heat, wear, lock-force,
  self-lock, wire-holding, solder-ergonomics, slicer, 3MF, or printer
  acceptance.
- Owner/role: `/root/p17_validator`, independent validator. Scope was
  read-only except this appended P17-V05 HANDOFF section.
- Frozen hash gate, all matched before tests:
  - candidate fingerprint JSON:
    `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`
    for `cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`;
  - artifact provenance:
    `4de4d236f67729b142b0ae0752ef41fe3087a9c191890947695f7ff72dc4be37`;
  - candidate manifest:
    `df92325baba8d39f8f511819c93467ac3cf8c5c4535bbde762755889acccddc8`;
  - source:
    `3df2574dc571ba37f24125d6cc1028d67273841d7c4951359f676fd07de46000`;
  - tests:
    `20145cfea70b483cb0b1e7efc7f418d6bea744fbc713a18e6500612702e0aeb7`;
  - pre-validation active HANDOFF:
    `ce9e5ef8ae0b061fcaeff8a70d4a63650bb364745220b7ca9162031609c86338`.
  Recomputed `p17-r2-candidate-fingerprint.json` SHA-256 and adjacent
  `p17-r2-candidate-fingerprint.txt` both equal the candidate fingerprint; the
  candidate manifest also records the same fingerprint.
- Test commands and results:
  - `uv run pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -k 'd06_'`
    -> `8 passed`;
  - `uv run pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`
    -> `31 passed`.
- Provenance hash audit: recomputed every provenance-recorded STEP, motion
  source/sidecar, and selected review artifact hash. All ten STEP hashes, four
  motion source/sidecar hashes, eleven PNG hashes, and two GIF hashes matched
  `p17-r2-artifact-provenance.json`.
- Written STEP validation: CAD `scripts/inspect validate` returned
  `ok:true` and `failureCount:0` for all ten written STEP exports:
  `center_axle_coupon`, `exploded`, `fixed_axle_motion`, `full_motion`,
  `lock_closeup`, `locked`, `mid`, `open`, `permanent_cap_coupon`, and
  `print_kit`. Occurrence counts were respectively
  `9/16/8/18/2/26/26/63/26/13` from validate output.
- Written STEP refs/facts audit: CAD `scripts/inspect refs --facts` was run
  for all ten STEP exports. STEP hashes matched the provenance set, no refs
  command returned errors, and leaf occurrence counts matched source-built leaf
  label counts for all ten artifacts. Raw in-memory source bounding boxes were
  not used as final parity evidence because direct build123d/OCCT bounds and
  CAD imported-STEP refs use different bound modes; candidate provenance still
  records `sourceExportMaxBoundDeltaMm: 0.0`, and the full P17 test/provenance
  gates passed.
- Independent source evidence:
  - `p17_r2_manifest()` reports fixed member
    `purple printed stepped center axle`, three moving white stainless rods,
    `centerAxle.worldInvariant: true`, fixed axle center `A=(-29.0,17.0)`,
    outer rotation center `C=(-10.6,17.0)`, one-piece axle, two keepers, no
    outer coupling, and non-goals `simulator`, `animation_sidecar`,
    `shared_D_shaft`, `removable_caps`, `yoke_bars`;
  - `fixed_occurrence_transform_evidence()` reports fixed occurrences
    `stepped_center_axle`, `left_inner_fixed_guide`, `right_inner_fixed_guide`,
    `left_keeper`, `right_keeper`, with `allFixedWorldInvariant: true` over
    open/mid/locked and outer angles `0`, `-/+16`, `-/+32` degrees;
  - `fixed_axle_actual_solid_evidence()` reports minimum exact frozen-feature
    gap `3.6500 mm`, analytic web `3.84868 mm`, inner/left/right webs
    `3.8946/7.650/9.150 mm`, axle-guide radial clearance `0.150 mm`, keeper
    radial capture `1.050 mm`, sample count `33`, zero axle/outer,
    keeper/outer, axle/white-rod, keeper/cap, and XT60/service intersections,
    and `centerAtCHasNoDecorativeHole: true`;
  - `combined_contact_closure_evidence()` reports `passes: true`, `66` rows
    (`33` samples per side), rank values `{3}`, maximum residual
    `3.43e-15 mm`, maximum perturbed pose error `7.31e-12`, and a claim
    boundary limited to nominal centerline local-mobility closure, explicitly
    excluding slot clearance, force, friction, self-lock, and physical fit.
- Sidecar audit:
  - focused `p17_r2_fixed_axle_motion.params.js` is self-contained, has no
    imports, and calls `effects.transform` only for `left_outer` and
    `right_outer`; it does not transform the stepped axle, keepers, fixed
    inner guides, or any rods;
  - full `p17_r2_full_motion.params.js` is self-contained, has no imports, and
    transforms `left_outer`, `right_outer`, plus all three rod and cap feature
    groups on frozen paths; it still does not transform the fixed axle,
    keepers, or fixed inner guides.
- Snapshot/GIF audit:
  - inventory matched exactly eleven `p17_r2_d07_*.png` and two
    `p17_r2_d07_*.gif` files, all `1800 x 1200`;
  - both GIFs contained 72 frames; frames `0`, `36`, and `71` were extracted
    to `/tmp/p17-v05-gif-frames/` for midframe inspection;
  - visual review of the PNG contact sheet and extracted GIF frames confirmed
    fixed purple axle/black keepers/inner plates, only outer plates
    counter-rotating in the focused sidecar, three rods/caps moving in the full
    sidecar, no visible decorative C hole, no new yoke/bar/boss/linkage, and
    the expected print kit/coupon contents. Visual review was used only as
    corroboration; deterministic tests and STEP/source evidence above are the
    validation basis.
- Additional textual audit: STEP labels contain the expected
  `manifest_e76b1cd77eb0__source_3df2574dc571` provenance token family. Source
  and sidecar search found only declared non-goals/animation metadata for
  simulator/yoke/shared-shaft terms, not production structure.
- Limitations and boundary:
  - no source, tests, STEP, sidecar, snapshot, CAD artifact, requirements,
    design, review, git, or PR files were edited;
  - no regeneration or repair was performed;
  - digital CAD/export pass does not prove keeper press-fit force, release
    effort, lock force, self-lock behavior, PETG tolerances, slicer/3MF, wire
    retention, solder ergonomics, durability, or physical acceptance.
- Next action: route this exact fingerprint to `P17-R05` formal review. Any
  source/test/generator/sidecar/STEP/snapshot/provenance/fingerprint change
  invalidates this P17-V05 receipt and requires revalidation.

## P17-C05 independent critic receipt

- Owner/role: `/root/p17_critic`, distinct critic; read-only.
- Status: PASS/no blocker for exact candidate fingerprint
  `b4ad7e49b198c189c5a32fdeecef7cf231b0306ef26d2404ae662711b22ff5b5`.
- Reconstructed candidate, provenance, manifest, source, test, and frozen path
  hashes all matched. Focused `8 passed`, full-file `31 passed`, numeric
  closure, representative STEP validation, and PNG/GIF motion review passed.
- Requirements satisfied digitally: fixed purple stepped axle; fixed inner
  plates/keepers; all three white rods remain moving; opposite outer twist on
  mirrored guides; `C` filled; no added bar/yoke/boss/linkage; frozen legacy
  paths and one-at-a-time scope preserved.
- Nonblocking physical risks: `0.150 mm` nominal radial guide clearance,
  `1.050 mm` keeper capture, PETG tolerance/wear, and nominal local closure do
  not prove force, friction, backlash, wobble, retention, or self-lock.
- The focused motion omits white rods for clarity and must not be used alone as
  full-assembly evidence; the full-motion artifact contains all three moving
  rods and caps.

## P17-R05 formal review receipt

- Owner/role: `/root/p17_formal_review`, distinct formal reviewer; read-only.
- Verdict: ACCEPT the unchanged fingerprint for digital CAD/source, all ten
  written STEP/export artifacts, and live preview delivery.
- C05 and V05 evidence, actual snapshots, requirements, scope, version
  semantics, candidate/provenance hashes, and physical boundaries were joined
  and accepted. P17 remains R2; the corrected datum, motion review, and Viewer
  evidence do not themselves create a new product version.
- Acceptance excludes mesh, DfAM, slicer, 3MF, PETG print, cap/keeper fit,
  force, strain, creep, heat, vibration, self-lock, wear, springback, solder
  ergonomics, and completed physical assembly.

## Singleton Viewer and exact preview receipt

- Service: per-user LaunchAgent `com.scottchu.cad-viewer`, stable command
  `~/.local/bin/cad-viewer`, one listener on `127.0.0.1:3245`.
- Payload digest:
  `9ae1b0eb9651d7fbd589c50108cb8be08efbed31ed3d0ac55af25c9dcc61ab0e`.
- Python is fixed to the canonical root uv interpreter
  `/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`.
- Independent Viewer V02 preserved a stable-shim symlink failure. Focused I03
  repaired realpath entry detection; V03 then passed 17/17 tests, install
  manifest, fresh-shell stable command, idempotent start, restart, crash
  recovery, durable stop/start, foreign-port safety, source independence,
  lifecycle logs/URL, one-listener state, and unchanged Tailscale Serve JSON.
- Exact focused Tailscale page returned HTTP `200`. Exact artifact status
  returned HTTP `200` with `state:"ready"`. The real `assembly.json`, motion
  params module, and one component GLB each returned HTTP `200` from both
  localhost and Tailscale. The package base ref is a directory and is not an
  asset file; its direct `404` is not used as readiness evidence.
- Review URL:
  `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_fixed_axle_motion.step.py`.

## P17-H05 continuity closeout

- `PROJECT_STATE.md`, `NEXT_AGENT.md`, this iteration's `BRIEF.md`,
  `REVIEW.md`, `VALIDATION.md`, and the project README now point to P17-I05,
  P17-D07, C05/V05/R05 evidence, and the current acceptance boundary.
- User visual review is the next gate. Keep this exact fingerprint unchanged
  while collecting feedback. A later authorized visible-issue repair opens a
  new bounded iteration; it does not rewrite this evidence.
