# P17 R2 review record

Status: `P17-R04` formally accepts final focused `P17-I04` candidate
`24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`
for CAD/source and written STEP/export evidence only. Mesh/DfAM/slicer/3MF and
physical proof remain pending.

Version correction note: formal review must not treat the rejected P17 R1
simulator artifact as a P-version reset. It may reject that simulator evidence
while preserving P17 R2 as the direct-CAD revision of the same counter-twist
design.

## Critic gate `P17-C02`

Status: **block for critic gate**. Candidate source, focused tests, and primary
STEP files are present and hash-verified, but the candidate should not advance
to formal review until the lock/back-drive evidence is corrected or explicitly
downgraded to an unproven concept. Keeper retention and service/DfAM evidence
remain high-risk physical unknowns.

Reviewed candidate:

- Candidate fingerprint from `P17-I02` handoff:
  `cbec2062217dcdbbc8e5e0cc6f278bebc5ecaede8a517f0945c8030299e168de`.
- Frozen P17-D03 design-doc manifest from `P17-I02` handoff:
  `18e5b14b5fa01e2b03dcd4aa2a1e8347b5046070049e087508a1959dd46389b1`.
- Verified component hashes matched handoff/provenance for `BRIEF.md`,
  `DESIGN.md`, `docs/REQUIREMENTS.md`, source, tests, provenance JSON, eight
  STEP artifacts, and eight PNG snapshots. No fingerprint mismatch was found.

### Blocker findings

1. `P17-C02-BLOCK-001`: The endpoint lock/back-drive evidence is not a
   mechanically sufficient torque/back-drive argument for `REQ-016`.

   Evidence:

   - `docs/REQUIREMENTS.md:113`-`116` requires a real grounded reaction path and
     explicit endpoint lock architecture with a torque/back-drive geometry
     argument, while force/self-lock proof remains physical.
   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:943`-`974` computes
     `lock_backdrive_evidence()` from a fixed nominal reaction vector
     `(0.0, -1.0)`, slot tangent normalization, and a summed sign value. It does
     not compute the actual stop contact normal, the tab/stop contact face, a
     perturbation direction, frictionless constraint feasibility, or whether the
     hard stop rather than the rod slots is reacting a back-drive load.
   - `tests/test_p17_r2_direct_counter_twist.py:256`-`260` only asserts the
     claim-boundary string, endpoint gap, and tangent unit length. It does not
     assert a non-opening torque sign, contact normal direction, or no-back-drive
     invariant.
   - Static probe of the implemented functions returned
     `lock_contact_gap_y(32 deg) = 0.0063 mm` but
     `lock_contact_gap_y(35 deg) = 1.9150 mm`; the tests nevertheless accept
     over-closed right-inner/right-outer intersection at `theta_lock + 3 deg`
     (`tests/test_p17_r2_direct_counter_twist.py:245` and `:250`-`:254`). That
     means the over-closed intersection is not shown to be the same intended
     endpoint face contact; it may be bulk overlap elsewhere in the stop/tab
     geometry.

   Disposition: block. The geometry may still be a useful lock concept, and the
   source correctly bounds the claim as "CAD contact/sign check only", but the
   current evidence should not be treated as satisfying the back-drive argument
   part of `REQ-016`. Required correction is either a real geometry argument
   against actual stop/tab contact faces and perturbation direction, or a
   requirement/status downgrade that leaves lock/back-drive fully unresolved.

### High-risk non-blocking findings and physical unknowns

2. `P17-C02-HIGH-001`: Keeper retention is modeled as press-fit interference on
   a smooth round end section, but no groove, bead, shoulder, insertion feature,
   or coupon for keeper retention is present.

   Evidence:

   - `docs/REQUIREMENTS.md:130`-`134` requires the slide-over sequence and
     physically retained keeper geometry, not a floating ring.
   - `docs/REQUIREMENTS.md:183`-`186` allows a permanent press-fit ring on a real
     seat/groove or split/groove keeper with insertion and retention geometry.
   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:604`-`635` builds the
     stepped axle as one central hex, two hex keys, and two smooth round
     journals.
   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:639`-`652` builds each
     keeper as a simple ring with `keeper_bore_diameter =
     outer_journal_diameter - 0.10`, then labels it as a permanent press-fit
     keeper on a real seat.
   - `tests/test_p17_r2_direct_counter_twist.py:165`-`170` accepts retention by
     intentional CAD interference volume only. This proves the keeper is not
     floating in space; it does not prove axial retention, installability, or
     that a smooth `1.20 mm` PETG press-fit ring will stay permanent outside a
     rotating plate.

   Disposition: high risk, not a separate digital blocker if formal review
   accepts "smooth press-fit end seat" as the intended provisional equivalent.
   Physical acceptance must stay blocked until a keeper-specific coupon or
   retention feature is tested. Consider adding a keeper retention coupon or a
   modeled shallow bead/groove before printing the full assembly.

3. `P17-C02-HIGH-002`: Actual service-envelope clearance is under-modeled for
   `REQ-017`, `CON-016`, and the user's physical observations.

   Evidence:

   - `docs/REQUIREMENTS.md:117`-`119` requires loading, motion, soldering,
     cooling, and completed-pigtail removal without loading XT60 plastic.
   - `docs/REQUIREMENTS.md:158`-`160` requires the center axle as an actual solid
     to be checked against XT60 body, wire, soldering, release, and completed
     pigtail removal envelopes.
   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:699`-`716` models only a
     static XT60 body box and two straight wire cylinders.
   - `tests/test_p17_r2_direct_counter_twist.py:173`-`178` checks only center
     axle intersection against those static references. It does not check the
     rods, caps, rotating plates, soldering-iron keepout, cooling state, release
     sweep, or completed-pigtail removal path.

   Disposition: high physical/service risk. The reduced `18.40 mm` inner span is
   a plausible CAD response to the photo-observed P13 span failure, but it is
   not a finished printed dimension or a service-clearance proof.

### Medium and low findings

4. `P17-C02-MED-001`: Full-assembly collision coverage is narrower than the
   mechanical risk.

   Evidence:

   - Tests cover selected axle/outer intersections, right stop/right outer
     intersections, and parameter invariants, but do not demonstrate a complete
     hardware-inclusive actual-solid collision sweep for both left and right
     plates, rods, caps, keepers, fixed slots, and service references across
     open/mid/locked states.
   - STEP structural validation passed for `p17_r2_locked.step` and
     `p17_r2_print_kit.step`, but STEP validity only establishes importable
     solids/assemblies, not mechanical clearance under motion.

   Disposition: validator should run a broader actual-solid collision and
   clearance matrix before formal review treats this as digitally accepted.

5. `P17-C02-MED-002`: Snapshot evidence is insufficient for the lock close-up
   and some coupon interpretation.

   Evidence:

   - Snapshot hashes show `p17_r2_lock_closeup_20260824T125859Z.png` is byte-for
     byte identical to `p17_r2_locked_20260824T125859Z.png`
     (`9fe71e47a31d...` for both), so it is not an independent close-up view of
     the stop/tab contact.
   - The center axle is mostly obscured in the locked assembly snapshot.
   - The permanent-cap coupon snapshot shows the coupon bodies but does not make
     the socket ID/depth ladder visually auditable without relying on labels and
     tests.

   Disposition: non-blocking for source review, but this should be corrected
   before user-facing CAD review or formal review depends on visual evidence.

### Requirement coverage disposition

- `REQ-009`, `REQ-010`, `REQ-011`, `REQ-018`, `REQ-019`, `REQ-020`: no blocker
  found in source/math evidence. Inner plates are fixed occurrences keyed by hex
  bores, outer rotations are `-theta`/`+theta`, outer bores are round journals,
  yoke/stability bars are absent, and no simulator/Three.js sidecar is present.
- `REQ-012`: no blocker found. Implemented diameters are inner `48.00 mm`, left
  outer `56.00 mm`, right outer `60.00 mm`, giving a quantified `2.00 mm` larger
  right-side lever radius.
- `REQ-013`, `REQ-014`: CAD intent is present: six permanent caps and cap coupon
  ladder. Physical cap retention remains unresolved by requirement.
- `REQ-015`: no blocker found in derivation. Implemented probe returned
  `inner_clear_span = 18.40 mm`, `principal_stack_width = 32.00 mm`,
  `rod_length_target = 40.60 mm`, and `center_axle_total_length = 34.90 mm`.
- `REQ-016`: blocked by `P17-C02-BLOCK-001`.
- `REQ-017`: high-risk incomplete service evidence by `P17-C02-HIGH-002`.
- `REQ-021`: slide-over math is coherent (`OD7.60 < AF8.15`) and the axle
  extends under the keeper, but keeper retention remains a high-risk physical
  unknown by `P17-C02-HIGH-001`.

### Commands and results

- `sed -n '1,240p' AGENTS.md`; `sed -n '1,260p' docs/CAD_WORKFLOW.md`; read CAD
  skill instructions.
- `git status --short --branch`; baseline branch
  `codex/xt60-p18-direct-cad`, `HEAD`
  `05e0152b045bd82a41ea07a715f2361606c1ec99`; unrelated/pre-existing project
  changes and untracked P17 R2 candidate paths were present.
- `shasum -a 256 ...` over frozen P17 R2 docs, source, tests, provenance, STEP,
  and snapshots -> matched handoff/provenance hashes; no mismatch.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH uv run
  --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py
  projects/xt60-bend-jig/tests/test_parameters.py -q` -> `20 passed`.
- Static source/dimension probe with `uv run --project projects/xt60-bend-jig
  python - <<'PY' ...` -> `inner_clear_span 18.4`,
  `rod_length_target 40.6`, `center_axle_total_length 34.9`,
  `outer_journal_diameter 7.6`, `fixed_inner_hex_bore_af 8.15`,
  `outer_bearing_bore 7.9`, `keeper_bore 7.5`,
  `lock gaps {0: 20.2196, 16: 10.2116, 32: 0.0063, 35: 1.9150}`,
  `summedTorqueAboutRightHub 1.0`.
- CAD inspect refs on `p17_r2_locked.step` -> `ok:true`, assembly size
  `[41.4, 88.148, 86.096]`, leaf occurrence count `18`.
- CAD inspect refs on `p17_r2_print_kit.step` -> `ok:true`, assembly size
  `[240.0, 160.081, 11.4]`, leaf occurrence count `13`.
- CAD inspect validate via
  `/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad/scripts/inspect/__main__.py`
  on `p17_r2_locked.step` -> `ok:true`, `failureCount:0`.
- CAD inspect validate via the same wrapper on `p17_r2_print_kit.step` ->
  `ok:true`, `failureCount:0`.

### Next action

Route to implementation/design for the smallest correction: strengthen or
downgrade the lock/back-drive evidence, then rerun the focused lock test and
snapshot close-up. In parallel for validation planning, add keeper-retention and
service-envelope gates before any physical acceptance language.

## Critic gate `P17-C03`

Status: **block for critic gate**. The P17-I03 replacement is a real mechanical
improvement over P17-I02: it preserves the four-plate/no-yoke architecture,
moves the shared pivot behind the XT60 body, replaces the fat slots with
`4.20 mm` curved cam slots, and provides a much clearer lock close-up. It still
must not advance to formal review because the aggregate candidate fingerprint is
not reproducible from the documented method and the literal service/removal
envelope still intersects production solids. Keeper manufacturability also
remains a high-risk physical gate.

Reviewed candidate:

- Candidate fingerprint assigned by `P17-I03`:
  `2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`.
- Frozen P17-D04 manifest assigned by `P17-I03`:
  `72b9319c25fc17c57a27af2102288072fdcf3a6f8adc4cb3d7375fc146eca3aa`.
- Component hashes matched `p17-r2-artifact-provenance.json`: D04 `BRIEF.md`,
  `DESIGN.md`, `docs/REQUIREMENTS.md`, source, focused tests, provenance JSON,
  all eight STEP files, and the fresh `20260824T1656/1700` snapshots.

### Blocker findings

1. `P17-C03-BLOCK-001`: The aggregate candidate fingerprint is not reproducible
   from the documented method.

   Evidence:

   - `HANDOFF.md:460`-`465` and
     `cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json` state the
     candidate fingerprint and describe the method as SHA-256 of canonical JSON
     containing the frozen-doc manifest plus path/SHA rows for source, focused
     test, and eight STEP files.
   - Recomputing that documented shape with sorted path/SHA rows over the
     matching source, test, and eight STEP hashes produced
     `5d2052addd19d8905a4ca9a60e328c73f437c5584a544a7709622e064b09bf5e`,
     not `2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`.
   - A bounded search over common canonical JSON variants, basename/project-path
     variants, `path`/`sha256` key variants, array-row variants, and line-based
     variants reported `NO_MATCH`.

   Disposition: block. Component hashes are consistent, so the mechanical review
   continued, but the critic gate cannot verify the frozen aggregate identity as
   requested. Required correction is to record the exact canonical manifest text
   or a manifest file whose SHA-256 is the candidate fingerprint.

2. `P17-C03-BLOCK-002`: The literal completed-pigtail removal/service envelope
   still intersects production solids, so `REQ-017` service/removal acceptance
   is not proven.

   Evidence:

   - `docs/REQUIREMENTS.md:117`-`119` requires loading, motion, soldering,
     cooling, and completed-pigtail removal.
   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:911`-`942` builds a
     `reference_completed_pigtail_release_removal_sweep` as part of the service
     envelope, and `build_motion_state()` includes it in every open/mid/locked
     state (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:945`-`963`).
   - Targeted source BREP probe found production/service intersections:
     - theta `0 deg`: `diagonal_rod` vs removal sweep
       `217.6119389372 mm^3`, `right_inner` vs removal sweep
       `198.6044575443 mm^3`, `left_inner` vs removal sweep
       `182.0067303277 mm^3`;
     - theta `16 deg` and `32 deg`: right/left inner fixed plates still intersect
       the removal sweep by `198.6044575443/182.0067303277 mm^3`.
   - CAD `scripts/inspect interfere` on `p17_r2_locked.step` also reported
     right and left inner fixed plates intersecting the same removal sweep. The
     all-STEP validity checks still pass because they check topology, not service
     feasibility.

   Disposition: block. Either the removal sweep is over-broad/incorrect and must
   be narrowed with a new explicit service-path contract, or the mechanism still
   obstructs completed-pigtail removal. The current tests only prove axle/keeper
   clearance to service envelopes (`tests/test_p17_r2_direct_counter_twist.py:363`-`368`),
   not full production/service clearance.

### High-risk non-blocking findings and physical unknowns

3. `P17-C03-HIGH-001`: Keeper retention remains mechanically and DfAM-risky; the
   new keeper ring has only about `0.55 mm` radial wall while also using a
   `0.10 mm` diametral press fit.

   Evidence:

   - `docs/REQUIREMENTS.md:130`-`134` and `:183`-`:186` require physically
     retained keeper geometry, not a floating ring.
   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:825`-`830` reduces the
     keeper OD to `outer_journal_diameter + 1.00`; with bore `7.50 mm`, the
     actual radial wall is `(8.60 - 7.50) / 2 = 0.55 mm`.
   - The source parameter checks enforce plate/hub web minimums but do not apply
     `min_web_mm = 2.20` to the keeper ring wall
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:310`-`317`).
   - `tests/test_p17_r2_direct_counter_twist.py:168`-`173` checks only that the
     keeper intersects the axle as a press fit; it does not test keeper wall,
     cracking risk, install path, or axial retention under plate rotation.

   Disposition: high physical/manufacturing risk. This blocks print/slicer or
   physical acceptance language, but is recorded below the digital blocker
   findings because it may be resolved by a keeper coupon or redesigned keeper
   without changing the core four-plate architecture.

4. `P17-C03-HIGH-002`: The modeled released-lock proof is an alternate shifted
   receiver shape, not an actual release/flexure mechanism.

   Evidence:

   - `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:560`-`649` builds named
     receiver components: `ground_arm`, `axial_bridge`, `outboard_spine`,
     `hard_stop`, and `retaining_shoulder`.
   - `build_lock_receiver(..., released=True)` shifts the shoulder by
     `lock_receiver_release_shift` (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:760`-`786`).
   - `lock_backdrive_evidence()` proves seated hard-stop/shoulder intersections
     and a released `-2 deg` clearance (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:1263`-`1306`),
     and tests assert those numbers
     (`tests/test_p17_r2_direct_counter_twist.py:236`-`268`).
   - No actual thumb tab, living hinge, flexure path, force limit, or user
     release sequence is modeled as a production motion state.

   Disposition: acceptable as a bounded CAD concept only. Do not claim physical
   lock force, self-lock, vibration resistance, or release usability without a
   physical coupon/assembly test.

### Medium findings and visual/UX risks

5. `P17-C03-MED-001`: The orange twin-arm receiver is functionally named and is
   not a rejected yoke/stability-bar architecture, but it is visually ambiguous
   enough to need simplification or explicit labeling before user-facing review.

   Evidence:

   - Root visual synthesis flagged the upper-right orange receiver as resembling
     previously rejected brown bars/two linked blocks.
   - Source shows the visible arms are part of the right-inner grounded receiver
     load path: a grounded arm, axial bridge, outboard spine, hard stop, and
     retaining shoulder (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:560`-`649`),
     not separate stabilizers, yoke bars, or left/right couplers.
   - `tests/test_p17_r2_direct_counter_twist.py:117`-`129` rejects yoke,
     stability-bar, tenon, shared-shaft, simulator, animation, and Three.js
     labels; source labels passed.
   - The fresh lock close-up snapshot
     `p17_r2_lock_closeup_20260824T170019Z.png` is distinct from the locked
     snapshot and clearly shows the receiver/nose, but it also makes the
     two-arm visual ambiguity obvious.

   Disposition: not a blocker. A simpler integrated pocket is not required by
   this critic if the current arms remain the named hard-stop/shoulder load path,
   but the next user-facing view should call out the two receiver functions or
   simplify the pocket if equivalent strength/clearance is preserved.

6. `P17-C03-MED-002`: Full-service validation is narrower than the model now
   implies.

   Evidence:

   - `service_clearance_evidence()` checks only the fixed center axle and two
     keepers against XT60/service-envelope targets
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:1133`-`1159`).
   - `tests/test_p17_r2_direct_counter_twist.py:323`-`360` check rods/caps
     against the XT60 body and non-owning mechanism solids, while
     `tests/test_p17_r2_direct_counter_twist.py:363`-`368` checks axle/keeper
     service-envelope clearance only.
   - The actual `scripts/inspect interfere` output contains many
     reference-vs-reference overlaps, so future automated interference gates need
     an explicit allowlist and separate production-vs-reference service checks.

   Disposition: medium. This is partly covered by blocker
   `P17-C03-BLOCK-002`; after fixing the removal sweep, validator should add an
   explicit collision matrix that separates expected reference overlaps from
   production/service violations.

### Passed or acceptable-by-critic items

- Four plates/no stability bars: pass. The source and snapshots preserve two
  fixed inner plates, two rotating outer plates, one center axle, two keepers,
  rods/caps, and no yoke/stability bars.
- Fixed inner plates and counter-rotating outers: pass. Source places inner
  plates at fixed occurrences about the shared pivot and rotates outers by
  `alpha_left = -theta`, `alpha_right = +theta`
  (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:359`-`367`,
  `:727`-`:745`).
- Offset axle behind XT60: pass for the D04 axle/keeper intent. Source sets the
  shared pivot at `YZ=(-10.60, 17.00)` (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:150`-`154`);
  source BREP probe found the XT60 body Y extent `[-4.05, 4.05]`, so the pivot is
  `6.55 mm` behind the back face, with pivot Z inside the body Z shadow and axle
  distance to XT60 body `0.7764973081 mm`.
- D04 guide-center deviation: acceptable within frozen intent. The D04
  provisional table in `HANDOFF.md:42`-`45` was lower priority than the explicit
  no-XT60-collision/service-clearance gates. A read-only probe of those
  provisional centers found repeated rod/body intersections up to
  `199.8052927683 mm^3`; the implemented recalculated centers recorded in
  `HANDOFF.md:506`-`514` had no rod/cap-to-XT60-body clashes in the nine sampled
  states. This does not require reopening design, but the accepted recalculated
  centers should become the durable design table if the candidate is repaired.
- Low-wobble curved cams: pass for CAD intent. Source uses
  `fixed_slot_width = 4.20`, `outer_slot_width = 4.20`, and `slot_sample_count =
  33` (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:142`-`145`), with
  part-local inverse transforms around the pivot (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:404`-`418`).
  Tests reject the old `4.90/7.55` values and require polyline length above
  endpoint chord (`tests/test_p17_r2_direct_counter_twist.py:380`-`391`).
- Larger force plate: pass. Current D04 diameters are inner `54.00`, left outer
  `60.00`, right primary `63.00`, giving `1.50 mm` larger right lever radius.
- Permanent cap/coupon logic: pass for CAD artifact only. Six permanent caps are
  present, and the coupon now includes cap ID/depth ladder plus straight/curved
  slot-fit coupons (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:1031`-`1072`).
  Physical cap fit remains `PHYS-007`.
- Lock close-up image: pass for critic visibility. The fresh
  `p17_r2_lock_closeup_20260824T170019Z.png` is not the old duplicate locked
  snapshot and exposes the nose/receiver relationship. Visual evidence remains
  secondary to BREP checks.

### Requirement coverage disposition

- `REQ-009`, `REQ-010`, `REQ-011`, `REQ-012`, `REQ-013`, `REQ-014`,
  `REQ-015`, `REQ-018`, `REQ-019`, `REQ-020`: no critic blocker found in the
  P17-I03 source/STEP evidence.
- `REQ-016`: no digital blocker found for bounded endpoint lock concept after
  P17-I03; hard-stop/shoulder/release BREP checks exist. Physical lock force,
  release effort, vibration resistance, and self-lock remain `NON-GOAL-007` /
  `PHYS-010`.
- `REQ-017`: blocked by `P17-C03-BLOCK-002` until service/removal-envelope
  intersections are resolved or the service envelope is re-specified.
- `REQ-021`: slide-over math and axle-under-keeper geometry pass, but keeper
  DfAM/retention remains high risk by `P17-C03-HIGH-001`.

### Commands and results

- Read `AGENTS.md`, `docs/CAD_WORKFLOW.md`, CAD skill instructions, P17 R2
  `BRIEF.md`, `DESIGN.md`, `HANDOFF.md`, prior `REVIEW.md`, prior
  `VALIDATION.md`, `docs/REQUIREMENTS.md`, source, tests, provenance JSON, STEP
  generators, and fresh snapshots.
- `git status --short --branch`; baseline branch
  `codex/xt60-p18-direct-cad`, `HEAD`
  `05e0152b045bd82a41ea07a715f2361606c1ec99`; existing modified/untracked P17
  R2 worktree state preserved.
- `shasum -a 256 ...` over frozen docs, source, tests, provenance, eight STEP
  files, and fresh snapshots -> component hashes matched P17-I03 provenance.
- `uv run --project projects/xt60-bend-jig python - <<'PY' ...` candidate
  fingerprint reconstruction -> recomputed `5d2052addd...`, expected
  `2761adf615...`; bounded schema search -> `NO_MATCH`.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH uv run
  --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py
  projects/xt60-bend-jig/tests/test_parameters.py -q -x` -> 27 focused test dots
  completed successfully.
- Source BREP D04 deviation/service probe -> provisional guide centers hit XT60
  body up to `199.8052927683 mm^3`; implemented guide centers had no sampled
  rod/cap-to-body clashes; pivot/body and axle/service distances reported above;
  production/removal sweep intersections reported in `P17-C03-BLOCK-002`.
- CAD inspect validate via
  `/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad/scripts/inspect/__main__.py`
  on all eight final STEP files -> all `ok:true`, `failureCount:0`.
- CAD inspect refs on `p17_r2_locked.step` -> `ok:true`, leaf occurrences `27`,
  size `[41.4, 88.032, 87.007]`; on `p17_r2_print_kit.step` -> `ok:true`, leaf
  occurrences `13`, size `[244.462, 155.340, 10.0]`.
- CAD inspect interfere on `p17_r2_locked.step` -> command `ok:false` due
  reference/service overlaps, production/removal sweep overlaps, and expected
  keeper/axle press-fit intersections. No renewed diagonal rod/keeper/axle clash
  like P17-I02 was observed in the reported locked pairs.

### Acceptance boundaries and next action

- CAD/source and written STEP: **critic-blocked** for candidate `2761adf...`
  until fingerprint reproducibility and service/removal envelope intersections
  are fixed or re-specified.
- Mesh/3MF/slicer: not generated or validated.
- Physical: not accepted. No PETG slot fit, wobble, cap retention, keeper
  retention, lock force/self-lock, heat, wear, vibration, solder ergonomics,
  wire holding, cooled angle, or springback proof exists.

Next action: return to implementation/coordination for a minimal provenance and
service-path repair: record the exact candidate manifest text, resolve the
literal removal-sweep intersections or replace the sweep with the intended
release/removal path, add an explicit production-vs-reference allowlist, and
rerun critic/validation on the regenerated fingerprint. Keeper ring wall should
be repaired or coupon-gated before any print-ready handoff.

## Critic gate `P17-C04`

Status: **pass/no-blocker for critic gate only**. Candidate
`24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`
is hash-reproducible from the persisted fingerprint JSON, all 30 declared
path hashes match, and the actual-solid/source checks I ran did not reproduce
the C03 lock-pass-in, removal-sweep, keeper-wall, or body-shadow blockers.
This is not formal approval, not slicer/print approval, and not physical
acceptance.

Reviewed candidate:

- Candidate: `P17-I04`.
- Candidate fingerprint:
  `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.
- Frozen P17-D05 manifest:
  `64c6db4496520007f4b31c0050809fad29ce949e34e7c806a387107c099946cd`.
- Persisted fingerprint payload:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`.
- Persisted candidate manifest:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-manifest.json`,
  SHA-256 `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`.
- Verified 11 input and 19 output path hashes from the fingerprint payload;
  mismatch count `0`.

### Blocker findings

None found by this critic gate on the frozen `P17-I04` candidate.

### High-risk physical unknowns and non-blocking findings

1. `P17-C04-HIGH-001`: The lock is now a coherent CAD contact/flexure concept,
   but the closing and release proof depends on modeled compliant deflection,
   not on a physically proven PETG latch.

   Evidence:

   - Source models three conditions of the same receiver datum:
     `seated`, `closing_unreleased`, and `released`, and documents them as one
     grounded receiver solid with a connected compliant latch arm
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:581`-`592`).
   - The catch is displaced by `lock_receiver_closing_deflection = 4.50 mm`
     for closing and `lock_receiver_release_shift = 5.00 mm` for release
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:141`-`147`,
     `:649`-`:654`).
   - My actual-solid probe matched the intended D05-modeled states:
     normal closing under `closing_unreleased` had maximum receiver
     intersection `0.0 mm^3` and minimum catch clearance `0.5913644619 mm`;
     released opening had maximum receiver intersection `0.0 mm^3` and
     minimum catch clearance `1.3076630688 mm`; locked hard-stop and shoulder
     intersections were both `0.0 mm^3`; over-close intersection was isolated to
     the hard stop (`overclosedNonHardStopIntersectionMm3 = 0.0`).
   - The same probe also found that a rigid, seated receiver still intersects
     during normal approach at `20, 24, 28, 30, 31 deg`
     (`0.3810546203`, `8.3777834062`, `6.0631812625`,
     `1.5819943041`, and `0.1377097379 mm^3`). That is acceptable only if the
     modeled lead-in/flexure action is treated as the real closing mechanism,
     not if the latch is assumed rigid.
   - The source correctly bounds the claim as
     "CAD receiver-pocket/contact proof only; physical self-lock not claimed"
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:1581`-`1583`).

   Disposition: non-blocking for this critic gate because P17-D05 explicitly
   allowed a same-solid modeled release/deflection path. Physical lock force,
   flexure strain, creep, heat, wear, vibration resistance, release effort, and
   self-lock remain unproven.

2. `P17-C04-HIGH-002`: Keeper/cap retention and rubbing remain physical risks
   despite the D05 wall repair.

   Evidence:

   - D05 keeper dimensions are now enforced in source: OD `10.00 mm`,
     bore `7.55 mm`, radial wall `1.225 mm`
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:117`-`119`,
     `:291`-`:297`, `:332`-`:337`, `:911`-`:925`).
   - The axle extends under the keeper seat and the keeper intentionally
     intersects the journal as a press fit; tests verify the keeper is not
     floating (`tests/test_p17_r2_direct_counter_twist.py:161`-`184`).
   - My 65-sample keeper/cap sweep found zero keeper/cap intersections, but the
     minimum digital distance was only `0.1034375039 mm`.
   - The keeper is still a smooth press-fit ring on a modeled end seat; no PETG
     coupon has proven install force, crack resistance, axial retention, or
     running friction.

   Disposition: non-blocking digital repair; blocks any print/physical
   acceptance language. Run keeper and cap coupons before relying on permanence.

3. `P17-C04-MED-001`: The prominent orange upper-right receiver remains visually
   conspicuous, but I do not find it to be the previously rejected unnecessary
   twin-block/yoke structure.

   Evidence:

   - Source decomposes the orange receiver into named functions:
     `ground_arm`, `axial_bridge`, `hard_stop`, `flexure_beam`,
     `lead_in_ramp`, `retaining_shoulder`, and `thumb_release_tab`
     (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:607`-`710`).
   - The receiver is integrated into the right fixed inner plate, not a separate
     stability bar or yoke (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:764`-`782`).
   - The final lock closeup visually shows one compact receiver/catch around the
     blue nose rather than two freestanding linked blocks. It is still visually
     busy enough that the user may read it as an extra bracket unless the CAD
     view is labeled or shown in closeup.

   Disposition: no critic blocker. Consider simplifying after physical latch
   behavior is known, but do not remove named load/release geometry before lock
   testing.

4. `P17-C04-MED-002`: DfAM and slicer evidence are still absent for fabrication
   handoff.

   Evidence:

   - `find projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist \( -name
     '*.stl' -o -name '*.3mf' -o -name '*.obj' -o -name '*.ply' \) -type f
     -print` returned no mesh files.
   - STEP validation and snapshots prove source-derived CAD artifacts, not mesh,
     3MF, slicer, support, first-layer, or printer-profile readiness.

   Disposition: non-blocking for critic gate; required before print handoff.

### Requirement coverage disposition

- `REQ-009`, `REQ-019`, `REQ-020`, `REQ-021`: no blocker found. The candidate
  uses one stepped center axle, hex-keyed fixed inners, round independent outer
  journals, actual keeper seats, and no yoke/stability bars. Slide-over math is
  coherent: `OD7.60 < AF8.15`, and the axle span/keeper positions are explicit
  (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:97`-`120`,
  `:217`-`:305`, `:875`-`:925`).
- `REQ-010`, `CON-013`: no blocker found. Source rotations remain
  `left=-theta`, `right=+theta`; my reconstruction probe found maximum cam
  reconstruction error `7.3241068776e-15 mm`, maximum left/right rod skew
  `7.9441092904e-15 mm`, and curved slot polyline exceeds endpoint chord by at
  least `0.7453593293 mm`, so the outer slots are not oversized straight
  endpoint capsules.
- `REQ-011`, `REQ-018`: no blocker found. I found no simulator/Three.js sidecar
  source and all eight STEP files are generated from source entrypoints in the
  P17 R2 namespace.
- `REQ-012`: no blocker found. Actual defaults are inner `54.00 mm`, left outer
  `60.00 mm`, right outer `63.00 mm`, giving `1.50 mm` larger right-side lever
  radius (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:131`-`133`,
  `:251`-`:256`).
- `REQ-013`, `REQ-014`: no blocker found for CAD intent. Source and snapshots
  show six permanent caps and a cap/slot coupon ladder; physical cap retention
  remains pending (`src/xt60_bend_jig/p17_r2_direct_counter_twist.py:1192`-`1233`).
- `REQ-015`: no blocker found. The reduced span and rod derivation are coherent
  for the photo-observed P13 spacing failure: `inner_clear_span = 18.40 mm`,
  `principal_stack_width = 32.00 mm`, `rod_length_target = 40.60 mm`, and
  `center_axle_total_length = 34.90 mm`. These are CAD defaults, not a finished
  printed dimension.
- `REQ-016`: no critic blocker for the D05 CAD concept. Same-receiver contact
  checks now cover pass-in, locked capture, hard-stop overclose, unreleased
  opening block, and released opening. Physical lock/release proof remains
  pending by `P17-C04-HIGH-001`.
- `REQ-017`, `CON-016`: no blocker found for the repaired digital service path.
  Pivot centerline is behind the XT60 body on `-Y` at `pivot_y=-10.60` and
  `pivot_z=17.00`; actual axle bbox is
  `X[-17.45,17.45]`, `Y[-16.3735,-4.8265]`, `Z[12.0,22.0]`; XT60 bbox is
  `X[-7.95,7.95]`, `Y[-4.05,4.05]`, `Z[10.75,31.25]`; minimum axle/XT60
  distance is `0.7764973081 mm`. The full axle/keeper X span is not required to
  fit inside the XT60 body width under the D05 wording. Released-open removal
  waypoints are `(0,21) -> (0,22.5) -> (8,22.5) -> (20,22.5) -> (34,22.5)`,
  with zero production intersections and minimum clearance `0.7764973081 mm`.

### Commands and results

- Read `AGENTS.md`, `docs/CAD_WORKFLOW.md`, CAD skill instructions,
  `PROJECT_STATE.md`, `NEXT_AGENT.md`, `docs/REQUIREMENTS.md`,
  `docs/EXPERIENCE.md`, `docs/decisions/README.md`, `ADR-0003`, P17 R2
  `BRIEF.md`, `DESIGN.md`, `HANDOFF.md`, prior `REVIEW.md`, prior
  `VALIDATION.md`, source, tests, STEP generators, provenance, fingerprint
  JSON/TXT/manifest, and selected fresh snapshots.
- `python3 - <<'PY' ...` over `p17-r2-candidate-fingerprint.json` ->
  SHA-256 `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`,
  candidate `P17-I04`, D05 manifest
  `64c6db4496520007f4b31c0050809fad29ce949e34e7c806a387107c099946cd`,
  `path_count 30`, `bad_count 0`.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH uv run
  --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py
  projects/xt60-bend-jig/tests/test_parameters.py -q -x` -> `29 passed`.
- Source/BREP critic probe with `uv run --project projects/xt60-bend-jig
  python - <<'PY' ...` -> lock, service/removal, slot reconstruction,
  keeper/cap clearance, axle/XT60 bbox, and label facts listed above.
- CAD inspect validate on all eight `cad/p17_r2_direct_counter_twist/*.step` ->
  every file reported `ok:true`, `failureCount:0`.
- CAD inspect refs/facts/positioning:
  `p17_r2_locked.step` -> hash `c8a9407946f951d...`, leaf occurrences `26`,
  size `[41.4, 88.032272, 87.006785]`; `p17_r2_print_kit.step` -> hash
  `f164094c6daf...`, leaf occurrences `13`, size
  `[244.458775,155.040773,10.0]`.
- Visual inspection via final selected snapshots:
  lock closeup, open, locked, print kit, center-axle coupon, and
  permanent-cap/slot coupon. Findings are reflected above.
- Mesh/DfAM search for `.stl`, `.3mf`, `.obj`, `.ply` under the P17 R2 CAD
  directory -> no files found.

### Acceptance boundaries and next action

- Critic gate: **pass/no-blocker** for candidate `24f5d752...`.
- CAD/source and written STEP: not approved overall here; route to independent
  validation and formal review with this critic receipt.
- Mesh/3MF/slicer: not generated or accepted.
- Physical: not accepted. PETG slot fit, keeper/cap retention, lock force,
  release effort, self-lock, heat/creep, wear, vibration, wire holding,
  soldering ergonomics, completed-pigtail hand clearance, cooled angle, and
  springback remain unresolved.

Next action: independent validator should rerun the D05 actual-solid gates on
the same fingerprint, especially the modeled compliant-lock states, released-open
dogleg removal, and the tight keeper/cap clearance. If validation agrees, formal
review can join the C04 and validator receipts; fabrication should still wait
for mesh/slicer checks and keeper/cap/slot coupons.

## Formal review gate `P17-R04`

Status: **pass with bounded acceptance**. Candidate
`24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb` is
formally accepted for CAD/source and written STEP/export evidence only.

Formal owner: `P17-R04` / `/root/p17_formal_review`, distinct from design,
implementation, critic, and validation. This role did not edit source, tests,
CAD artifacts, generated snapshots, validation, continuity, git, or PR state.

### Provenance join

- Branch and baseline verified from repository state: `codex/xt60-p18-direct-cad`
  at `05e0152b045bd82a41ea07a715f2361606c1ec99`.
- Candidate identity verified by persisted fingerprint file:
  `LC_ALL=C shasum -a 256 cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`
  reproduced `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.
- Frozen P17-D05 manifest verified from the same fingerprint payload:
  `64c6db4496520007f4b31c0050809fad29ce949e34e7c806a387107c099946cd`.
- Persisted candidate manifest hash verified:
  `p17-r2-candidate-manifest.json`
  `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`.
- All 30 declared fingerprint paths matched: 11 inputs and 19 outputs, with
  mismatch count `0`.
- Pre-formal-review record hashes:
  `REVIEW.md` `d0d78000a9c70897e547b025f5c3d378910c5fe5c06c85e187589c4789f93cb0`;
  `VALIDATION.md` `577a8a4b8e7f386f5192889eb6fd0a653e0e24c396e709b2c0643d778566d6e6`.
- Critic join: `P17-C04` passed/no-blocker for this exact candidate and did not
  reproduce the C03 lock-pass-in, removal-sweep, keeper-wall, or body-shadow
  blockers.
- Validator join: `P17-V04` passed CAD/source and written STEP/export
  validation for this exact candidate, with `29 passed`, all eight STEP files
  valid, all selected snapshot hashes matched, source/export parity matched,
  and no production collision/contact blocker found.

### Requirement audit

| Requirement / user contract | Formal disposition |
|---|---|
| Four principal plates | Accepted digitally. The print-kit and motion-state evidence show two fixed inner plates plus left/right outer plates; no extra yoke/stability-bar architecture is accepted. |
| Fixed inner guides | Accepted digitally. Tests and source keep inner positions fixed; fixed guide loci are state-independent. |
| Opposite independent outer rotations | Accepted digitally. Source rotations remain `left=-theta`, `right=+theta`; outer journals are round and not coupled by the center axle. |
| Larger force-side outer plate | Accepted digitally. Implemented diameters are inner `54.00 mm`, left outer `60.00 mm`, right primary `63.00 mm`, giving the right primary a `1.50 mm` larger lever radius. |
| Offset stepped hex/round center axle behind XT60 | Accepted digitally under D05 wording. Pivot is behind the body on `-Y` at `pivot_y=-10.60`, `pivot_z=17.00`, with minimum actual service clearance `0.7764973081037425 mm`; full axle X-span containment inside the XT60 body width is explicitly not required. |
| Away from solder/wire/service envelopes | Accepted digitally for modeled envelopes. V04 reports zero production intersections and minimum service/removal clearance above the `0.75 mm` target. Real soldering ergonomics and heat behavior remain physical gates. |
| No unnecessary stability bars | Accepted digitally. C04/V04 source and label checks found no yoke/stability bars, yoke tenons, simulator sidecar, shared D shaft, or same-direction coupling. |
| Narrow low-wobble true curved tracks | Accepted digitally. Fixed and outer slot widths are `4.20 mm`; cam loci are sampled curved part-local paths, not oversized straight endpoint capsules; maximum reconstruction error was `7.32410687763558e-15 mm` and maximum rod skew was `7.944109290391274e-15 mm`. |
| Permanent cap strategy and coupons | Accepted as CAD/source and STEP/coupon artifacts only. Six permanent caps and cap/slot coupon ladders are present. Cap fit, retention, cracking, wear, and installation force remain physical gates. |
| Operable close-lock-backdrive-release | Accepted as bounded CAD contact/release geometry. Normal closing and released opening have zero receiver/nose intersection in the modeled compliant states; unreleased opening is blocked; overclose contact is isolated to the hard stop. Physical PETG lock force, flexure strain, creep, heat, vibration, release effort, and self-lock are unproven. |
| Completed-pigtail removal | Accepted digitally for the modeled released-open dogleg removal path. Waypoints are `(0,21) -> (0,22.5) -> (8,22.5) -> (20,22.5) -> (34,22.5)` with zero production intersections in V04. Physical hand clearance, wire stiffness, soldered-joint bulk, and springback remain unproven. |
| Version semantics | Accepted. This remains P17 R2 direct CAD; the rejected P17 R1 simulator is an excluded evidence layer and does not reset the product-design `P` number. |
| Simulator excluded as evidence | Accepted. No simulator/Three.js/JS sidecar evidence is used for this formal acceptance. |

### STEP and snapshot evidence accepted

The accepted written STEP/export set is exactly the fingerprinted P17-I04 output
set:

- `p17_r2_open.step`
  `4aff043f91143f677eed19021e1403083642834c0172b4aebd130b46c9c5316c`
- `p17_r2_mid.step`
  `fe92076f5896f4891d6382ae1a604f5541e0f2cf251cd23fb622842267af27ea`
- `p17_r2_locked.step`
  `c8a9407946f951d41de6dd94a4c06488ec2f1ce82541fc6bd1626518c8d520e2`
- `p17_r2_exploded.step`
  `49028de1ecbca59a25178dc538adc32b318defd57298bd3e5cb1bb68f61dfed2`
- `p17_r2_print_kit.step`
  `f164094c6daf897fc11e39c863aa3b41d34c74c5e372de79c23cc6b4ade14113`
- `p17_r2_permanent_cap_coupon.step`
  `8f374e00b72cdd968ff51fbcb6c9f5ad9dc16059f2dddc20614e3ccb916575f5`
- `p17_r2_center_axle_coupon.step`
  `61e6b5579fbfec6519e90a08fd4fb83f285498c403ee4667ddc83ba3de8e0241`
- `p17_r2_lock_closeup.step`
  `dd555503e49d1d83c0a84ba1e2b0e503083166a9674ab232084646ca5c9a82f7`

Final selected snapshots were hash-verified by V04 and spot-reviewed during
formal review. The locked and lock-closeup snapshots show the right-primary
outer plate and same-receiver lock geometry; the print-kit snapshot shows the
four plates, stepped axle, keepers, and six caps; the permanent-cap coupon
snapshot shows cap and slot coupon ladders. These snapshots support visual
review only; deterministic BREP/source/STEP checks carry the acceptance.

### Residual risks and boundaries

- Accepted: CAD/source and written STEP/export evidence for the exact P17-I04
  fingerprint above.
- Not accepted: mesh, DfAM, slicer, 3MF, print readiness, printer-profile
  behavior, and physical assembly/use.
- High physical risks remain open: compliant PETG lock force, latch strain,
  creep, heat, vibration, release effort, self-lock behavior, keeper/cap
  retention, smooth press-fit keeper installation, cap cracking/wear, slot fit,
  rod wobble, soldering ergonomics, wire holding, completed-pigtail hand
  clearance, cooled angle, and springback.
- Tight digital margin: C04 reports zero keeper/cap intersections but only
  `0.1034375039 mm` minimum digital keeper/cap gap. Treat that as a physical
  coupon/assembly risk, not a proven working clearance.
- No mesh files were present under `cad/p17_r2_direct_counter_twist`; therefore
  no DfAM mesh measurement or slicer gate exists.
- `PROJECT_STATE.md` and `NEXT_AGENT.md` still contain older pre-R04 continuity
  language at the time of this review. That does not invalidate the exact
  fingerprinted candidate, but the handoff/continuity owner must update them
  before trunk delivery.

### Commands and spot checks

- Read project continuity, requirements, experience log, decision index,
  `ADR-0003`, P17 R2 `BRIEF.md`, `DESIGN.md`, `HANDOFF.md`, `REVIEW.md`,
  `VALIDATION.md`, candidate source/tests, fingerprint/manifest/provenance
  JSON, STEP/snapshot evidence, CAD workflow, CAD skill instructions, and CAD
  inspection/snapshot references.
- `LC_ALL=C shasum -a 256 .../p17-r2-candidate-fingerprint.json
  .../p17-r2-candidate-manifest.json REVIEW.md VALIDATION.md` -> hashes listed
  above.
- Python fingerprint verifier over `p17-r2-candidate-fingerprint.json` -> candidate
  `P17-I04`, expected fingerprint matched, D05 manifest matched, `path_count
  30`, `bad_count 0`.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH uv run
  --project projects/xt60-bend-jig pytest
  projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py
  projects/xt60-bend-jig/tests/test_parameters.py -q -x` -> `29 passed`.
- `find projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist -type f \( -name
  '*.stl' -o -name '*.3mf' -o -name '*.obj' -o -name '*.ply' \) -print` -> no
  mesh files.
- `git diff --check` -> clean before formal write.

### Next action

Route to continuity/handoff closeout. Update `PROJECT_STATE.md`, `NEXT_AGENT.md`,
and final handoff language to name this exact accepted CAD/source and STEP
fingerprint while keeping mesh/slicer/3MF/physical acceptance pending. The next
smallest physical path is PETG coupons for slot fit, permanent caps, and keeper
retention before any full assembly/use trial.

## Design-owner self-scope note

`P17-D03` corrected and documented the center-axle numeric/assembly contract
only. It did not
edit CAD/source/tests/artifacts and does not approve future implementation.
