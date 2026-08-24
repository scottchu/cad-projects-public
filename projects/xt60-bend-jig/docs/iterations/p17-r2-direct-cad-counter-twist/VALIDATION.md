# P17-V04 final focused validation record

Status: passed for CAD/source and written STEP/export validation of candidate
`24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.

This is not mesh, slicer, 3MF, print, or physical acceptance. No PETG print,
keeper/cap retention, lock force, release effort, heat, wear, vibration, wire
holding, solder ergonomics, springback, or self-lock acceptance is claimed.

## Validator and environment

- Owner: `P17-V04` / `/root/p17_validator`.
- Role: independent validation gate, distinct from implementation, critic, and
  formal review.
- Date/time: `2026-08-24 14:08:57 EDT`.
- Worktree:
  `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`.
- Branch: `codex/xt60-p18-direct-cad`; HEAD
  `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Python: `3.12.13` through root `uv`; `uv 0.12.2`.
- Platform: macOS Darwin `25.5.0` arm64.
- CAD instructions read before CAD validation: `cad:cad`, plus
  `inspection-and-validation.md`, `snapshot-review.md`, and `positioning.md`.
- DfAM skill boundary read. It measures mesh files only; no P17 R2 `.stl`,
  `.obj`, `.ply`, or `.3mf` files exist in
  `cad/p17_r2_direct_counter_twist/`, and this gate was not authorized to
  create mesh sidecars.

Pre-existing candidate/worktree state: the P17-I04 candidate paths are
untracked in this worktree and project continuity files are modified as part
of the broader candidate branch. This validation edited only this
`VALIDATION.md`.

## Fingerprint and hash verification

Declared candidate fingerprint:
`24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.

Declared P17-D05 frozen manifest:
`64c6db4496520007f4b31c0050809fad29ce949e34e7c806a387107c099946cd`.

Independent reproduction passed:

- `LC_ALL=C shasum -a 256 projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`
  -> `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.
- `p17-r2-candidate-fingerprint.txt` contains the same fingerprint.
- `p17-r2-candidate-manifest.json` SHA-256:
  `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`.
- All 30 declared manifest path hashes matched: 11 inputs and 19 outputs.
- All 18 provenance cross-hashes matched: source, focused test, eight STEP
  files, and eight selected snapshots.
- The provenance JSON records the same D05 manifest and no component drift was
  found.

Key verified hashes:

| Item | SHA-256 |
|---|---|
| `BRIEF.md` | `d79381a27ad3030e7d07e2c7a496cd9b71ce37b532f1162d787ee90f430dfa13` |
| `DESIGN.md` | `d46b5f906fc377a3fa7370b4338aa3728e442f2cd10ca2b5a79c32b1b1d3cf48` |
| `docs/REQUIREMENTS.md` | `567e315522a0d5269daef52f95ff91cb67da3c1dd8b41ec5be5aa99ea646a2f5` |
| `src/xt60_bend_jig/p17_r2_direct_counter_twist.py` | `7d6250693bacbcfe962649406b65c6917ac3a187b3f3537f215d5150fbfb43a3` |
| `tests/test_p17_r2_direct_counter_twist.py` | `e7fd569f83cecc5f43225327dbcc7943cb6a37f7d485e675052ba67b12a75455` |
| `p17-r2-artifact-provenance.json` | `95b60da6cb9b11ff28d758e5b944322b8094bda86f2b102630895644af48ab43` |

Written STEP hashes matched manifest/provenance:

- `p17_r2_center_axle_coupon.step`:
  `61e6b5579fbfec6519e90a08fd4fb83f285498c403ee4667ddc83ba3de8e0241`
- `p17_r2_exploded.step`:
  `49028de1ecbca59a25178dc538adc32b318defd57298bd3e5cb1bb68f61dfed2`
- `p17_r2_lock_closeup.step`:
  `dd555503e49d1d83c0a84ba1e2b0e503083166a9674ab232084646ca5c9a82f7`
- `p17_r2_locked.step`:
  `c8a9407946f951d41de6dd94a4c06488ec2f1ce82541fc6bd1626518c8d520e2`
- `p17_r2_mid.step`:
  `fe92076f5896f4891d6382ae1a604f5541e0f2cf251cd23fb622842267af27ea`
- `p17_r2_open.step`:
  `4aff043f91143f677eed19021e1403083642834c0172b4aebd130b46c9c5316c`
- `p17_r2_permanent_cap_coupon.step`:
  `8f374e00b72cdd968ff51fbcb6c9f5ad9dc16059f2dddc20614e3ccb916575f5`
- `p17_r2_print_kit.step`:
  `f164094c6daf897fc11e39c863aa3b41d34c74c5e372de79c23cc6b4ade14113`

Selected snapshot hashes matched manifest/provenance:

- `p17_r2_center_axle_coupon_20260824T175525Z.png`:
  `0295c7a310c7c27180026fe0e4b32b2c3b1e39da576593e3fb642201554d4931`
- `p17_r2_exploded_20260824T175526Z.png`:
  `acad3375801b79c6e82f1ff2737a9238ab6c12e7c36c3acecae505916e616a6e`
- `p17_r2_lock_closeup_20260824T175512Z.png`:
  `5d94374ded8b84263b5e85ee3e71be42ec40959d82e3584ea9d6c9fca85fdcaa`
- `p17_r2_locked_20260824T175527Z.png`:
  `9a8923f0ead6f2752cb8467d22085ecbbc7e9991b4d6645c554634a922cdc17e`
- `p17_r2_mid_20260824T175529Z.png`:
  `fed355d8e9708c56e8a30088379fd4a13f4edf45e021d7c2e4ef3ae406876180`
- `p17_r2_open_20260824T175531Z.png`:
  `6733b20e66e8534e6dd1083d9b11e431a0973dbed2716018ec34e662f1097103`
- `p17_r2_permanent_cap_coupon_20260824T175534Z.png`:
  `4e3fe79fc75d858833430dfe243fe580f93ca9e43b97d09b5e5545523550ed5c`
- `p17_r2_print_kit_20260824T175535Z.png`:
  `a7653b599b9b51af0507787e3a6c3fed6f767a6d017cd3b905062047d17c0468`

## Commands and results

| Command | Result |
|---|---|
| Read `AGENTS.md`, `docs/CAD_WORKFLOW.md`, project continuity, active P17 docs, CAD skill, CAD references, and DfAM skill | Completed before CAD validation. |
| `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py projects/xt60-bend-jig/tests/test_parameters.py -q -x` | Exit `0`; `29 passed`. |
| Hash verifier over `p17-r2-candidate-manifest.json`, `p17-r2-candidate-fingerprint.json`, `.txt`, provenance, and all declared paths | Exit `0`; fingerprint reproduced, 30 manifest hashes and 18 provenance hashes matched. |
| CAD `scripts.inspect validate` on all eight written STEP files | Exit `0`; every file reported `ok=True`, `failures=0`. |
| CAD `scripts.inspect refs ... --facts --planes --positioning` on all eight written STEP files | Exit `0`; every file reported `ok=True`. |
| Independent source BREP dense probe over 65 motion samples plus lock, removal, body-shadow, keeper/cap, collision, cam, and source/export parity checks | Passed after correcting the validator's rod-center interpolation to the source smoothstep law; no production collision/contact blocker found. |
| `find projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist -type f \\( -name '*.stl' -o -name '*.3mf' -o -name '*.obj' -o -name '*.ply' \\)` | No output; no mesh file exists for read-only DfAM measurement. |
| `git diff --check` | Exit `0`. |

## Independent source BREP results

Lock and receiver:

- Normal closing sweep sampled 64 states from `0..31.8 deg`.
- Maximum normal-closing receiver/nose intersection:
  `0.0 mm^3`.
- Minimum normal-closing catch clearance:
  `0.5913644618595516 mm`.
- Explicit contract samples `0,4,8,12,16,20,24,28,30,31,31.5,31.8 deg`
  all had `0.0 mm^3` receiver intersection.
- Locked hard-stop intersection:
  `0.0 mm^3`.
- Locked shoulder intersection:
  `0.0 mm^3`.
- Overclose total intersection:
  `1.320771667443748 mm^3`, all attributed to the hard-stop; non-hard-stop
  overclose intersection was `0.0 mm^3`.
- Unreleased opening is blocked by the same seated shoulder:
  `31 deg = 0.1377097379440117 mm^3`,
  `30 deg = 1.5819943041307774 mm^3`.
- Released opening clears the shoulder:
  `31 deg = 0.0 mm^3`, `30 deg = 0.0 mm^3`.
- Same receiver connected solid counts:
  seated `1`, closing `1`, released `1`.
- Lock contact gap at `32 deg`: `0.020000000000000462 mm`.
- Capture: `0.40 mm`.

Service/removal:

- `service_clearance_evidence()` passed.
- Minimum actual service/removal clearance:
  `0.7764973081037425 mm`, above the `0.75 mm` target.
- Completed-pigtail removal sequence:
  `release -> full open -> lift to window centerline -> +Y extraction`.
- Removal waypoints:
  `(0.0,21.0) -> (0.0,22.5) -> (8.0,22.5) -> (20.0,22.5) -> (34.0,22.5)`.
- Removal zero-intersection: `true`.

Dense production collision sweep:

- Samples: 65 states from `0..32 deg`.
- Rods, caps, axle, keepers, XT60 body, fixed plates, and outer plates were
  checked for unintended intersections using source-built BREP solids.
- Maximum keeper/cap intersection: `0.0 mm^3`.
- Minimum keeper/cap gap: `0.10343750385644679 mm`.
- Maximum other checked unintended intersection: `0.0 mm^3`.
- Expected keeper/axle press-fit was the only allowed interference and was not
  counted as a failure.

Cam/slot reconstruction:

- Samples: 65 states from `0..32 deg`.
- Maximum rod-center reconstruction error:
  `7.32410687763558e-15 mm` against the source `rod_center()` motion law.
- Maximum left/right rod-end YZ skew:
  `7.944109290391274e-15 mm`.
- Slot width: `4.20 mm`; nominal center slop:
  `0.10000000000000009 mm`.

Source/export parity:

- All eight artifacts matched source-built occurrence counts and
  dot-normalized labels.
- Maximum source-vs-written STEP bounds delta:
  `6.256328788367682e-12 mm`.
- Leaf counts:
  open `63/63`, mid `26/26`, locked `26/26`, exploded `16/16`,
  print kit `13/13`, permanent cap coupon `26/26`, center axle coupon `9/9`,
  lock closeup `2/2`.

Dimensions and naming:

- `inner_clear_span = 18.40 mm`.
- `rod_length_target = 40.60 mm`.
- `center_axle_total_length = 34.90 mm`.
- `outer_journal_diameter < fixed_inner_hex_bore_af` is true.
- `keeper_radial_wall_min = 1.225 mm`.
- Fixed and outer slot widths are both `4.20 mm`.
- Right primary lever radius is `1.50 mm` larger than the left.
- Locked assembly labels contain six permanent follower caps and two
  press-fit outer keepers, with no removable/service cap, yoke/stability,
  Three.js, or simulator production wording.

## Explicit axle/keeper behind-XT60 body-shadow validation

The corrected P17-D05 rule is proven as written:

- XT60 body bbox:
  `X[-7.95, 7.95]`, `Y[-4.05, 4.05]`, `Z[10.75, 31.25]`.
- Pivot/axis datum: `Y=-10.60`, `Z=17.00`.
- Proven: pivot/axis is behind the body on `-Y`.
- Proven: pivot/axis `X=0, Z=17.00` is inside the XT60 body `XZ` projection.
- Proven: actual axle/keeper/service clearance is positive, with minimum
  actual service clearance `0.7764973081037425 mm`.
- Not true, and not required by D05: the full X-spanning axle/keepers are
  inside the XT60 body `X` width. The center axle bbox is
  `X[-17.45,17.45]`, `Y[-16.373502691896256,-4.826497308103742]`,
  `Z[12.0,22.0]`; keeper bboxes are at approximately
  `X[-17.45,-16.25]` and `X[16.25,17.45]`.
- The candidate manifest explicitly records
  `fullAxleXShadowRequired = false`, because requiring full axle/keeper X
  containment would contradict the four-plate stack.

Therefore actual body-shadow placement is proven under the corrected D05
coordinate contract. It would fail only a superseded literal requirement that
the entire axle/keeper geometry fit inside the connector body's narrow X
shadow.

## Orange upper-right receiver structure

The orange upper-right structure is part of
`right_inner_fixed_guide_hex_keyed_with_completed_pigtail_window_and_receiver`.
It is the grounded right-inner receiver/catch/stop/flexure/thumb-tab structure
for the blue right outer primary actuator's integrated lock nose.

Confirmed contacts:

- Normal closing: no receiver/nose intersection through `31.8 deg`.
- Locked: no hard-stop or shoulder penetration; hard-stop gap is about
  `0.02 mm`.
- Overclose: only the hard-stop contact/interference is present.
- Unreleased opening: the same seated receiver shoulder intentionally blocks
  the nose.
- Released opening: shoulder clears with zero intersection.

No non-lock contact was found in the dense production collision sweep.

## Snapshot review

All eight selected PNG hashes matched provenance and were visually inspected.

- Open/mid/locked snapshots show the four-plate stack, fixed inner pair,
  opposite outer rotation, narrow curved slots, rods, six permanent caps,
  offset stepped axle, OD10 keepers, and orange right-inner receiver.
- The lock closeup is distinct from the root oblique/locked snapshot and tightly
  frames the blue right-outer nose against the orange same-receiver catch/stop.
- Exploded view shows separate plates, rods, permanent caps, keepers, and the
  stepped axle without yoke/stability bars.
- Print kit snapshot shows bed-flat print orientations and expected part
  census.
- Permanent cap/slot coupon snapshot shows the cap ladder and five straight /
  curved slot coupon widths.
- Center axle coupon snapshot shows hex/bearing/keeper-retention coupon
  features.

Visual review did not reveal missing parts or obvious production overlaps, but
the acceptance above relies on the BREP and STEP checks, not the screenshots.

## Requirement coverage disposition

- `REQ-009`, `REQ-010`, `REQ-011`, `REQ-018`, `REQ-019`, `REQ-020`: passed
  digitally. Inner plates and axle are fixed across states; outer plates rotate
  opposite directions; no simulator, yoke/stability bars, or same-direction
  shared shaft is present.
- `REQ-012`: passed digitally. Both outer plates are larger than the inner
  plates, and the right primary lever radius is `1.50 mm` larger than the left.
- `REQ-013`, `REQ-014`: passed for CAD presence/coupon contract only. Six
  permanent caps and coupon ladders exist; physical retention is pending.
- `REQ-015`: passed digitally. Span, rod length, center-axle length, cap
  engagement, slots, and stack are source-derived and match written STEP.
- `REQ-016`: passed as a bounded CAD contact/release geometry proof. Physical
  lock force, self-lock, vibration, creep, wear, heat, and release effort
  remain pending.
- `REQ-017`: passed digitally for represented service/removal solids in the
  released-open sequence with minimum clearance above `0.75 mm`. Real
  soldering ergonomics, heat, wire holding, springback, and physical removal
  remain pending.
- `REQ-021`: passed digitally for slide-over math, axle extension, keeper
  presence, and explicit keeper/axle press-fit allowlist. Keeper installation
  and retention remain physical gates.
- `CON-008`–`CON-023`: passed for checked digital constraints, including
  `18.40 mm` span, `34.90 mm` axle, `40.60 mm` rods, `OD7.60 < AF8.15`,
  `4.20 mm` slots, `1.225 mm` keeper radial wall, and zero skew.

## Acceptance boundary and next action

CAD/source validation: passed for P17-I04.

Written STEP/export validation: passed for all eight STEP artifacts.

Mesh/DfAM/slicer/3MF validation: not accepted; no mesh exists and no slicer or
3MF gate ran.

Physical validation: pending.

Next action: route the verified candidate to the distinct formal review gate.
If formal review accepts the CAD/export evidence, the next smallest physical
work is PETG coupons for slot fit, permanent caps, keeper retention, and then a
full assembly/use trial for lock effort, heat, wire holding, removal,
springback, and wear.

# P17 R2 validation record

Status: failed. `P17-V03` rejects candidate
`2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`.

The source, tests, written STEP files, and fresh snapshot hashes match the
declared `P17-I03` candidate set, but independent actual-solid validation found
blocking defects:

1. the right outer lock nose collides with the fixed retaining shoulder during
   the normal closing sweep at intermediate angles before lock; and
2. the literal completed-pigtail removal sweep intersects production geometry;
   and
3. the literal axle/keeper "inside XT60 body XZ shadow" placement is not proven
   for the full axle/keeper geometry.

CAD/source and written STEP acceptance are therefore not granted. Mesh, slicer,
and physical acceptance are not claimed.

## Validator and environment

- Owner: `P17-V03` / `/root/p17_validator`.
- Role: independent validation gate, distinct from design, implementation,
  critic, and formal review.
- Date/time: `2026-08-24 13:03:03 EDT`.
- Project: `projects/xt60-bend-jig`.
- Branch: `codex/xt60-p18-direct-cad` (branch name predates the P17 R2 relabel).
- Baseline commit: `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Python: `3.12.13` through root `uv`; `uv 0.12.2`.
- Platform: macOS Darwin `25.5.0` arm64.
- CAD instructions read before CAD validation: `cad:cad`; references read:
  `inspection-and-validation.md`, `snapshot-review.md`, and `positioning.md`.
- DfAM skill boundary read. It measures mesh files only; no P17 R2 `.stl`,
  `.obj`, `.ply`, or `.3mf` file exists, and this gate was not authorized to
  create one.

## Candidate and hash verification

Declared candidate fingerprint:
`2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`.

Declared D04 frozen design-doc manifest:
`72b9319c25fc17c57a27af2102288072fdcf3a6f8adc4cb3d7375fc146eca3aa`.

The component hashes below match
`cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json` and the
`P17-I03` handoff receipt:

| Item | SHA-256 |
|---|---|
| `BRIEF.md` | `f3e3fbae98597d3cd8cf4ed9ae13dd305b8edb53d794d9dfe0331a794d53e8ad` |
| `DESIGN.md` | `17b5bfe10ea13e3a4fe34ebdd0a0485f6814195018d5c9e7e2033fbf8523e3da` |
| `docs/REQUIREMENTS.md` | `567e315522a0d5269daef52f95ff91cb67da3c1dd8b41ec5be5aa99ea646a2f5` |
| `src/xt60_bend_jig/p17_r2_direct_counter_twist.py` | `2de1784d71300cd85c8753f10e2868cdd7b4cbb9a6331808d4ee7f56c072817d` |
| `tests/test_p17_r2_direct_counter_twist.py` | `b44d34a7dec06db3ba379e8eaca10ad1f905cc24f8d05e433c4f9cf4d2a10237` |
| `p17-r2-artifact-provenance.json` | `7a826f100f3ae48c6ecf43f0b44ad77a557a321ac3769eb0361d6a84d923da4b` |

All eight written STEP hashes matched provenance:

- `p17_r2_open.step`: `a79d653a762fbaa803049b90e9179d8ef6ec25e1ff0fba818669005a7fd481a1`
- `p17_r2_mid.step`: `724c6cf7a955b224190803f3065525d37a146111092d7b81f76ebb0e507c2df3`
- `p17_r2_locked.step`: `d28e27637818c2e743d8b7c6beb0f9f8da8e056c21c24724aa895f35e892e27f`
- `p17_r2_exploded.step`: `182cbe5dfb203405a43220213f6e1a4d60f12433ba94ca6ca67b76ecf3d5f785`
- `p17_r2_print_kit.step`: `3525b3497549b944551a8e6800cc432200ff453caee9e34ddcb3092c855bf853`
- `p17_r2_permanent_cap_coupon.step`: `2931ac19246e9e2bfbbc00d3a79ae23924eef68891710e6729ab322a8759fdba`
- `p17_r2_center_axle_coupon.step`: `4ded1f49c3f3e489ce458ce720b93310bf09bf3aea65f536e2d5e54849b20445`
- `p17_r2_lock_closeup.step`: `399948c522d2e96b61588483e2c64730fe35fbe6480d5b3c1a3d15c7a8624c53`

All eight fresh snapshot hashes matched provenance:

- `p17_r2_open_20260824T165606Z.png`: `c31800844bba216ebe6b07fb3a07f1dc4b0643361b2920311a2ca624ba69dc73`
- `p17_r2_mid_20260824T165623Z.png`: `e311c11af7386eaa56cae165952fa3ae70a1ec42d55d41903dbb2504ef169eda`
- `p17_r2_locked_20260824T165625Z.png`: `b675fc3df228bb8a4544a544deda8324fc322f2db77d6c0789c9c17c25510810`
- `p17_r2_exploded_20260824T165627Z.png`: `d2caf005417e05b75233aad5507823d429fd76bf1b487b95b4c778b6a36e1238`
- `p17_r2_lock_closeup_20260824T170019Z.png`: `f3c0fc46345d5db3ab4c23dbcc297e25204f8c5565f0ff193788c53755231ed4`
- `p17_r2_print_kit_20260824T165630Z.png`: `3c5e6a3ea9c92466c13c95a717c0e2578ee1b081f284d7f11ba3bb7333a52be4`
- `p17_r2_permanent_cap_coupon_20260824T165631Z.png`: `e7df4f32f988da9bfff343059ac41587000590acdff36a9c446879358783535f`
- `p17_r2_center_axle_coupon_20260824T165632Z.png`: `601ac41922d2fff0f33557750653ce7f8c4602194b5911a208a57e7e0e077f63`

Fingerprint reproduction limitation: the provenance says the fingerprint is
the SHA-256 of canonical JSON containing `frozenDocManifestSha256` and
path/SHA-256 rows for source, focused test, and eight STEP files. Several
reasonable canonical JSON and line-manifest variants did not reproduce
`2761adf...`; for example `pathAndSha256Rows` with sorted compact JSON produced
`d6a9bd3960247fc0598777456fa25bc6f6b77515018f373494b2dc0fedfcfbac`.
Because all declared component hashes matched, this is recorded as a provenance
finding rather than as evidence of file drift.

## Commands and results

| Command | Result |
|---|---|
| `rg -n "P17\|p17\|xt60\|direct-cad\|counter\|2761adf\|72b9319" /Users/scottchu/.codex/memories/MEMORY.md` | No P17 R2 current-candidate memory record found; repo evidence used as authority. |
| `sed -n ... AGENTS.md`, `docs/CAD_WORKFLOW.md`, CAD skill `SKILL.md`, and CAD references | Read before validation. |
| `jq . projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json` | Parsed; declared fingerprint, D04 manifest, hashes, evidence, and boundaries extracted. |
| `shasum -a 256 ...` over docs/source/tests/provenance/eight STEP/eight fresh snapshots | All component hashes matched provenance. |
| `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py projects/xt60-bend-jig/tests/test_parameters.py -q -x` | Exit `0`; focused tests completed successfully (`27` dots / no failure). |
| `git diff --check` | Passed. |
| CAD `scripts/inspect validate` on all eight written STEP files through root `uv` Python | Passed: every file reported `ok:true`, `failureCount:0`. First bare `python` attempt failed because `python` is not on `PATH`; the same check was rerun correctly with `uv run ... python`. |
| CAD `scripts/inspect refs ... --facts --planes --positioning` on all eight STEP files | Passed command-level refs/facts/positioning extraction. |
| CAD `scripts/inspect frame` on `p17_r2_locked.step '#'` and `p17_r2_print_kit.step '#'` | Passed root-frame checks; both root transforms are identity and local axes align to world XYZ. |
| CAD `scripts/inspect measure p17_r2_print_kit.step --from '#o1.1.1.f2' --to '#o1.1.1.f3' --axis z` | Passed; representative plate thickness measured `3.2 mm`. |
| CAD `scripts/inspect interfere` on open/mid/locked/lock-closeup STEP files | Raw command reports many overlaps, dominated by reference-vs-reference envelopes and intentional keeper/axle press fits. No P17-V02 rod/cap/axle/keeper production collision recurred in the three written motion states. |
| Independent source BREP sweep at 9 samples from `0..32 deg` | Failed: right inner fixed receiver/shoulder intersects right outer lock nose at intermediate angles. |
| Independent source BREP sweep of completed-pigtail removal envelope at 9 samples from `0..32 deg` | Failed: removal sweep intersects both fixed inner plates in all samples and intersects the diagonal rod in early samples. |
| DfAM mesh search: `find ... -name '*.stl' -o -name '*.3mf' -o -name '*.obj' -o -name '*.ply'` | No mesh files found; DfAM not applicable without creating a mesh, which this gate was not authorized to do. |

## STEP topology and refs summary

All eight final STEP files are topologically valid:

| STEP | Occurrences validated | Failure count |
|---|---:|---:|
| `p17_r2_open.step` | 27 | 0 |
| `p17_r2_mid.step` | 27 | 0 |
| `p17_r2_locked.step` | 27 | 0 |
| `p17_r2_exploded.step` | 16 | 0 |
| `p17_r2_print_kit.step` | 13 | 0 |
| `p17_r2_permanent_cap_coupon.step` | 26 | 0 |
| `p17_r2_center_axle_coupon.step` | 3 | 0 |
| `p17_r2_lock_closeup.step` | 27 | 0 |

Representative written-STEP frame facts:

- `p17_r2_locked.step` root frame: identity transform; bounding size
  `[41.4, 88.032272, 87.006785]`; center
  `[0.0, -9.966136, 17.1297005]`.
- `p17_r2_print_kit.step` root frame: identity transform; bounding size
  `[244.461978, 155.339934, 10.0]`; center
  `[17.230989, -3.919967, 5.0]`.
- `p17_r2_print_kit.step` representative plate thickness:
  `3.2 mm`.

## Source BREP validation facts

Independent source BREP probes confirmed these passing facts:

- Pivot datum: `pivot_y = -10.60 mm`, `pivot_z = 17.00 mm`.
- XT60 body reference bbox: `X[-7.95, 7.95]`,
  `Y[-4.05, 4.05]`, `Z[10.75, 31.25]`.
- Pivot point at `X=0, Z=17.00` is inside the XT60 body `XZ` projection, and
  `pivot_y=-10.60` is behind the body on `-Y`.
- Minimum actual-solid axle/keeper clearance to XT60 body and modeled +Y
  service envelopes over 9 samples is `0.7764973081037425 mm`, above the
  `0.75 mm` target.
- Open/mid/locked rotations remain `left=-theta`, `right=+theta`; inner plate
  X positions are fixed at `-10.80` and `+10.80 mm`.
- Continuous cam reconstruction over 33 samples has maximum reconstruction
  error `7.32410687763558e-15 mm`; maximum left/right rod skew is
  `7.944109290391274e-15 mm`.
- Source labels show six permanent follower caps and two permanent
  press-fit keepers. No yoke/stability bar, simulator, animation sidecar,
  shared D shaft, same-direction shaft, removable cap, or Three.js production
  label was found.
- Source print kit contains 13 leaf parts and is bed-aligned in the written
  STEP; the cap coupon contains cap ID/depth ladders plus straight and curved
  slot-fit coupon ladders at `4.10, 4.15, 4.20, 4.25, 4.30 mm`.

## Added body-shadow coordinate validation

Root specifically requested axle/keeper "behind XT60 body shadow" validation
instead of relying on the oblique screenshot or min-clearance alone.

Result: not fully proven under the literal full-geometry `XZ` interpretation.

Source facts:

- XT60 body `XZ` shadow is `X[-7.95, 7.95]`, `Z[10.75, 31.25]`.
- Pivot point at `X=0`, `Z=17.00` is inside that shadow.
- The full center axle bbox is `X[-17.45, 17.45]`,
  `Y[-16.373502691896256, -4.826497308103742]`,
  `Z[12.0, 22.0]`.
- The left keeper bbox is `X[-17.45, -16.25]`,
  `Y[-14.90, -6.30]`, `Z[12.7, 21.3]`.
- The right keeper bbox is `X[16.25, 17.45]`,
  `Y[-14.90, -6.30]`, `Z[12.7, 21.3]`.

Therefore:

- Proven: pivot/axis datum is behind the XT60 body on `-Y`.
- Proven: pivot/axis datum at `X=0, Z=17.00` is vertically and centrally within
  the XT60 body `XZ` projection.
- Not proven: full axle bbox is inside XT60 body `XZ` shadow; it extends beyond
  body X width by `9.50 mm` per side.
- Not proven: keeper centers or keeper bboxes are inside XT60 body `XZ` shadow;
  keeper centers sit at `X=±16.85 mm`, outside the body X range.

If the design intent is only "the shared pivot YZ coordinate is behind the
body and vertically inside the connector silhouette," the source satisfies it.
If the requirement means actual axle/keeper geometry must sit inside the XT60
body's full XZ projection, this candidate fails that requirement. P17-V03 does
not accept the body-shadow requirement as fully proven.

## Orange twin-arm upper-right structure identification

The orange twin-arm upper-right structure in the snapshots is not a rod or cap.
It is part of the right fixed inner guide:

- source label: `right_inner_fixed_guide_hex_keyed_with_grounded_receiver_pocket`;
- internal receiver pieces from `_lock_receiver_components_local()`:
  `ground_arm`, `axial_bridge`, `outboard_spine`, `hard_stop`, and
  `retaining_shoulder`;
- source color: `#D89A19`, the orange used for inner fixed guide geometry.

Its purpose is the grounded receiver pocket/lock reaction path for the blue
right outer primary actuator's integral lock nose.

## Findings

### `BLOCKING` - Right outer lock nose collides with retaining shoulder during closing sweep

The contract requires sampled full motion beyond just open/mid/locked states
and only intentional lock contacts. The independent source BREP sweep found
right inner fixed receiver/shoulder intersection with the right outer lock
nose during the normal closing path:

| Theta | Colliding components | Intersection volume |
|---:|---|---:|
| `20 deg` | right inner retaining shoulder vs right outer/lock nose | `0.20732811499922943 mm^3` |
| `24 deg` | right inner retaining shoulder vs right outer/lock nose | `8.281342565082042 mm^3` |
| `28 deg` | right inner retaining shoulder vs right outer/lock nose | `6.070579515921791 mm^3` |
| `30 deg` | right inner retaining shoulder vs right outer/lock nose | `1.5819943041307944 mm^3` |
| `31 deg` | right inner retaining shoulder vs right outer/lock nose | `0.13770973794401176 mm^3` |

Component decomposition showed no contact against `ground_arm`, `axial_bridge`,
`outboard_spine`, or `hard_stop` at these approach angles. The overlap is the
retaining shoulder.

The following lock contacts are consistent with the intended falsifiable lock
concept:

- `theta = 32 deg`: locked hard-stop and shoulder intersection are both `0.0`.
- `theta = 33 deg`: hard-stop overclose intersection is
  `1.0993069026092468 mm^3`.
- `theta = 30/31 deg` can represent unreleased-opening shoulder engagement
  when modeled as an opening perturbation from locked.
- released `theta = 30 deg` shoulder intersection is `0.0`.

However, the same `30/31 deg` geometries occur on the normal closing path from
open to lock, and additional `20/24/28 deg` retaining-shoulder collisions were
found. The candidate does not prove that the lock nose can enter the receiver
without material collision. This blocks the user motion/use sequence.

Disposition: return to implementation. The smallest likely correction is to
reshape or gate the retaining shoulder so the nose has a collision-free closing
entry path, while preserving shoulder engagement for unreleased opening and
released-opening clearance.

### `BLOCKING` - Literal full axle/keeper body-shadow placement is not proven

The source proves pivot-point placement and min clearance, but not full
axle/keeper placement inside the XT60 body's `XZ` projection:

- body X range is `[-7.95, 7.95]`;
- center axle X range is `[-17.45, 17.45]`;
- keeper centers are at `X=±16.85`.

This may be a wording/design-contract ambiguity, but P17-V03 cannot mark the
body-shadow requirement proven when root asked for coordinate validation beyond
the oblique screenshot.

Disposition: clarify or restate the contract. If full XZ-shadow placement is
required, redesign the axle/keeper layout. If only pivot YZ placement was
intended, update the contract and acceptance checks to say that exactly.

### `BLOCKING` - Completed-pigtail removal sweep collides with production geometry

The task specifically required all unintended production/service-envelope
collisions to be validated. P17-V03 independently measured the literal
`reference_completed_pigtail_release_removal_sweep` solid against production
parts over 9 samples from `0..32 deg`.

The removal sweep intersects both fixed inner plates at every sampled state:

- left inner fixed guide: `182.00673032766952 mm^3`;
- right inner fixed guide: `198.60445754430197 mm^3`.

It also intersects the diagonal rod in early motion:

| Theta | Part | Intersection volume |
|---:|---|---:|
| `0 deg` | diagonal rod | `217.61193893720142 mm^3` |
| `4 deg` | diagonal rod | `194.62208030180818 mm^3` |
| `8 deg` | diagonal rod | `125.03538761287365 mm^3` |
| `12 deg` | diagonal rod | `30.532806940493643 mm^3` |

This may indicate that the completed-pigtail removal envelope is over-broad or
not actually the intended post-release removal path. It still blocks validation
because the candidate presents that actual solid as a service/removal envelope
and it overlaps production geometry.

Disposition: either redesign the service/removal path or restate the envelope
as an intentionally conservative visual reference that is not an acceptance
keep-out. If it remains an acceptance keep-out, the production geometry must
clear it in the required released/removal states.

### `MAJOR` - Candidate fingerprint formula is still not reproducible

All component hashes match, but the exact canonical JSON used for the candidate
fingerprint is not stored. Reconstructed variants did not produce `2761adf...`.

Disposition: future handoffs should record the exact manifest JSON or a
manifest file whose SHA-256 is the candidate fingerprint.

### `LIMITATION` - Broad STEP interference includes reference-envelope overlaps

CAD `scripts/inspect interfere` on full motion-state STEP files reports
reference-vs-reference overlaps among wire, solder, heat-shrink, tool, removal,
and XT60 reference envelopes. It also reports the intentional axle/keeper
press-fit (`1.423141472076... mm^3` per keeper).

Those raw clashes are not treated as production-mechanism failures. The
blocking failure above comes from independent source BREP decomposition of
production right-inner/right-outer lock geometry during the sampled closing
sweep.

## Requirement coverage

| Requirement / risk | Evidence | Status |
|---|---|---|
| `REQ-009`: fixed inner plates and center axle | Source/tests confirm fixed inner X positions and shared pivot; STEP root frames are stable. | Pass, subject to lock repair. |
| `REQ-010`: opposite outer rotation | Source/tests confirm left `-theta`, right `+theta`. | Pass. |
| `REQ-011`: no simulator/sidecar/shared shaft | Source labels and source text checks found no simulator/Three.js/shared same-direction shaft. | Pass. |
| `REQ-012`: outer plates larger/right larger | Source defaults: inner `54`, left outer `60`, right outer `63`; right extra lever radius `1.50 mm`. | Pass. |
| `REQ-013`/`REQ-014`: six permanent caps and coupon gate | Source and snapshots show six permanent caps; coupon ladders exist; physical cap proof pending. | Pass for CAD count/coupon presence only. |
| `REQ-015`: re-derived stack/rod length | Source defaults preserve `18.40 mm` span, `34.90 mm` axle, `40.60 mm` rods. | Pass. |
| `REQ-016`: grounded endpoint lock | Grounded receiver/nose exists, but intermediate closing-sweep shoulder collision blocks usable lock motion. | Fail. |
| `REQ-017`: wire forming/use sequence | Axle/keeper service clearance passes numerically, but closing to lock has solid collision and the completed-pigtail removal sweep intersects fixed inner plates and the diagonal rod. | Fail. |
| `REQ-018`: source-derived STEP-first workflow | Component hashes, STEP topology, and fresh snapshots are present; fingerprint formula is not reproducible. | Partial. |
| `REQ-019`/`REQ-020`: stepped axle, no outer coupling | Source labels and tests support one stepped axle and independent outer journals. | Pass, subject to shadow clarification. |
| `REQ-021`: slide-over/keeper strategy | Slide-over dimensions are coherent and keepers are modeled as intentional press-fit rings; physical retention remains pending. | Partial physical risk. |
| D04 body-shadow placement | Pivot YZ coordinate is proven behind the body and centrally/vertically inside body projection; full axle/keeper XZ shadow placement is not. | Not proven / fail closed. |

## Snapshot review

The eight fresh provenance snapshots were hash-verified and visually inspected:

- open/mid/locked: nonblank; fixed orange inner plates, larger green/blue
  outer plates, black permanent caps, gray rods, and transparent reference body
  are visible;
- `lock_closeup_20260824T170019Z`: nonblank, distinct from locked snapshot,
  and tightly frames the orange right-inner receiver/twin-arm structure and
  blue right-outer lock area;
- exploded: nonblank; shows four principal plates, stepped purple axle,
  keepers, rods, and caps;
- print kit: nonblank; shows flat-oriented four plates, stepped axle, keepers,
  and six caps;
- permanent-cap coupon: nonblank; shows cap ID/depth ladder and straight/curved
  slot-fit coupons;
- center-axle coupon: nonblank; shows axle and fit coupons.

Visual review does not override the source BREP lock collision failure or the
body-shadow coordinate finding.

## Acceptance boundaries

- CAD/source: failed for candidate `2761adf...`.
- Written STEP: topologically valid and hash-matched, but not accepted because
  source BREP sampled motion fails, the literal completed-pigtail removal
  sweep overlaps production geometry, and the written STEP set contains no
  intermediate `20/24/28/30/31 deg` states to prove the closing sweep.
- Mesh/3MF/slicer: not generated and not validated.
- DfAM: not run because no mesh upload artifact exists and P17-V03 was not
  authorized to create one.
- Physical: not performed. This validation does not prove cap retention,
  keeper retention, lock force, self-lock, heat, wear, vibration, wire holding,
  solder ergonomics, springback, printed fit, or assembly behavior.

## Next action

Return to implementation for the smallest source repair:

1. eliminate the right lock retaining-shoulder collision during normal closing
   while preserving hard-stop overclose, unreleased-opening shoulder capture,
   and released-opening clearance;
2. repair or explicitly reclassify the completed-pigtail removal envelope so it
   no longer fails the service-path keep-out check;
3. clarify and then satisfy the axle/keeper body-shadow coordinate contract;
4. record the exact candidate manifest JSON used for the fingerprint; and
5. regenerate the eight STEP files and fresh snapshots from source, then rerun
   independent validation with sampled motion evidence.
