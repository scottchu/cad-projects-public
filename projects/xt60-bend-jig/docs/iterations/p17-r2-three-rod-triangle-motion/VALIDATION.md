# P17-V07 independent validation

## Receipt

- Validator role: `P17-V07`, independent of design, implementation, critique, and formal review.
- Candidate: `P17-I07-R1`.
- Verdict: **PASS for CAD source, written STEP exports, frozen visual evidence, and singleton Viewer HTTP readiness.** Physical manufacture, PETG fit, stainless-stock selection, and printed operation remain unproven.
- Frozen independent gate manifest: `/tmp/p17-i07-independent-gate-manifest.txt`, SHA-256 `5965f4e88bc807a1e13ac38c7bc3b342cc285f24a9082c9975dd44000540cb87`; all 30 entries passed `shasum -a 256 -c` before and after the long-running gates.
- Authoritative source SHA-256: `11b5336d7c4523c4ce685b8d784406934a08098179160b306cd595c2fcf589c2`.
- Focused test SHA-256: `752fb84281113a5025aefd37db17340f5d00388c43743884af2c3388a628b779`.
- Artifact provenance SHA-256: `19e9927cb9d17ef307e96b70eb06600ac5d691d0aa164568d7bddf46b741190c`.
- Candidate manifest SHA-256: `733f11d57aec71f9be8875a8d6ea3196fcc7c4076a673fc5de267c1253686c91`.
- Candidate-fingerprint record SHA-256: `8d399246cb21b295de169b62863243da5ed6e75a7bf3f079e0ab97767a7dc0bd`; its recorded immutable-input fingerprint is the exact independent manifest SHA above.

## Independent gates

All Python work ran from the repository root through the shared root environment with `uv run`; no environment or dependency changes were made.

### Kinematic math, inverse rails, and conditioning

- Independently recomputed `S = 12.80 mm`, `OPEN U=(35.5,9.0)`, `B=(6.8,37.7)`, `D=(5.2339574413,7.4339574413)`, fixed center `C=(1.75,6.25)`, contact stroke `12.55 mm`, contact angle `23.53125 deg`, endpoint angle `24 deg`, and `open_to_end = 0.98046875` at first contact.
- Triangle doubled areas were `456.7904214346901` at OPEN, `12.384667144969583` at CONTACT, and `7.394704576049996` at END; corresponding side lengths remained finite and positive.
- Inverse rail-to-axle reconstruction over 65 states had maximum error `1.0048591735576161e-14 mm` and minimum determinant `3.3007142674880665`.
- Minimum crossing sine was `0.10202218156989079`, above the `0.10` gate.
- Actual extended-cutter gaps were `6.52182604717553 mm` left, `6.418265282176154 mm` right, and `6.103048327205 mm` for the fixed extended cutter. Minimum actual web was `2.6675894314400947 mm`, above the `2.20 mm` gate.
- Centered finite differences against the public residual/Jacobian API gave maximum residual norm `8.181e-15`, rank 3 at every sampled state, minimum normalized singular-value ratio `0.10373000727499965`, and maximum normalized condition number `9.64041193353906` (`9.640422856842672` in candidate evidence). The maximum absolute forward-versus-centered finite-difference entry difference was `1.63308e-5`, attributable to the distinct finite-difference schemes and not a rank/conditioning failure.

### Actual solids, support, caps, and service motion

- Checked 65 states plus exact contact using actual solids. Minimum XT60 clearance was `0.75 mm`; maximum unintended pair intersection and maximum pre-contact wire intersection were both `0`; contact clearance was numerical zero (`4.44e-16 mm`). At END, intended rod/wire intersections were positive: upright `0.7896612 mm^3`, bottom `0.7896666 mm^3`, diagonal `1.089034 mm^3`.
- Production inventory was exactly 3 rods, 6 permanent caps, 2 inner plates, 2 outer plates, and 2 axle keepers. No forbidden/replaced geometry labels were present.
- Actual support probes passed across all 65 states on both sides; minimum probe/material intersection was `0.10053096491487308 mm^3`, with rail ends closed.
- Axial closure used `50.00 mm` physical rod stock, `32.00 mm` stack, `8.70 mm` engagement, and `9.05 mm` cap length, leaving `0.35 mm` wall. Six caps were present; cap-to-plate/keeper and nominal rod-to-cap-material unintended intersections were `0`.
- Full service path used the required linear waypoints `P0(0,0,0) -> P1(0,0,-35) -> P2(8,0,-35) -> P3(20,20,-35) -> P4(20,45,-30)` at 1001 samples per segment (4004 evaluated samples). The actual pigtail body, two solder joints, and two wires were checked against all 16 production obstacles. Minimum BREP clearance was `0.846751751172426 mm`, analytic clearance `0.8467517511724272 mm`, and maximum intersection was `0`.

### Focused tests and written exports

- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py` -> **18 passed**.
- All 10 written STEP exports passed independent `refs --facts --planes --positioning` and `validate` inspection with zero failures: center-axle coupon, contact, exploded, fixed-axle motion, full motion, locked/end, mid, open/service, permanent-cap coupon, and print kit.
- Inspector safety note: a same-stem `.step.py` can be selected when the requested `.step` remains beside it. Validation therefore copied each manifest-verified STEP byte stream to an isolated temporary directory under a distinct `export_*.step` name before invoking the inspector.
- Direct `build123d.import_step` source/export parity passed for all 10 exports. Maximum bounds delta was `6.252776074688882e-12 mm`, maximum summed-volume delta `4.889443516731262e-09 mm^3`, and maximum per-solid signature delta `1.0000880834581949e-7`, below the `1e-6` gate.

### Visual evidence and singleton Viewer

- Manifest-verified OPEN, CONTACT, END isometric, and END opposite PNGs were visually inspected. The 72-frame, 1800x1200, looping full-motion GIF was inspected at frames 0, 17, 35, 53, and 71; successive frames had non-empty image differences and showed the three rod/cap groups following their rails while the two outer plates counter-rotate around the fixed eccentric axle.
- The frozen visual packet retained hashes: OPEN `b03f5737a91655af1d4db05fde241839472fad088312153987766311e54c5faa`, CONTACT `036f562de8f8debc2e985422d124e7e8d2f4845b7716ba620ded4fa86738ae45`, END iso `0bb984c99d155559eec56eea10270618de99fd8dc6c2e7c9b6a54766df56a336`, END opposite `05163104d7c355f1ac7bf6379031b1b1aba74f60f08afeff61b71c1001d7bab4`, GIF `7a0dada9bdcf0c800569dd4499d229051a9aeb3ff8e202be81305e15122a63fc`.
- Exact singleton Viewer page for `projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py` returned HTTP 200 locally and through Tailscale. `GET /__cad/artifact` returned HTTP 200 and `state: ready` on both routes.
- The assembly descriptor returned HTTP 200 on both routes, SHA-256 `c873d5f25b8cbc5fcdecb7a7094d3bf2aa34f838a1890ac9e7ba3cf5f59511aa`, with 10 component prototypes and 18 occurrences. The motion module returned HTTP 200, SHA-256 `fcd64a66ab930b47a16f1d3261281c60dbb40f2c283d2dc982a33881299fe177`, and exposes the singular `open_to_end` control. Every one of the 10 referenced GLB components and all six page JavaScript/CSS assets returned HTTP 200 with identical local/Tailscale hashes.
- Local page: `http://127.0.0.1:3245/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_full_motion.step.py`.
- Tailscale page: `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_full_motion.step.py`.
- Limitation: no controllable browser surface was available to this validator, so live slider interaction was not independently exercised. This does not weaken the verified page/artifact/descriptor/module/component HTTP readiness or the separately inspected frozen motion GIF, but it remains distinct from an interactive human review.

## Acceptance boundary and next action

- **CAD source:** PASS for the exact immutable candidate.
- **Written STEP exports:** PASS for all 10 exports and source/export parity.
- **Frozen visual evidence:** PASS for the inspected OPEN/CONTACT/END views and full-motion GIF.
- **Live preview transport/readiness:** PASS locally and through Tailscale; interactive browser manipulation was unavailable to this validator and is recorded above.
- **Physical acceptance:** NOT TESTED. The candidate has no PETG print/assembly/fit proof, no stainless-stock procurement/cut acceptance, and no physical locking/force/wobble result.
- Next action: independent formal review may consume this exact fingerprint. After that gate, generate/slice only the approved print package and run the documented physical fit and operation checks; any candidate-input change invalidates this receipt.
