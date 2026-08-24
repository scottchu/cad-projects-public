# P17 R2 handoff

Status: `P17-I04` fingerprint
`24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`
is formally accepted by `P17-C04`, `P17-V04`, and `P17-R04` for CAD/source
and written STEP/export evidence only. Mesh/DfAM/slicer/3MF and every physical
claim remain pending.

## Root continuity closeout

- Current controlling contract: `P17-D05`.
- Accepted digital candidate: `P17-I04`.
- Candidate manifest SHA-256:
  `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`.
- `P17-C04`: pass/no blocker for the exact fingerprint.
- `P17-V04`: pass for CAD/source and all eight written STEP exports.
- `P17-R04`: formal pass with the same bounded acceptance.
- Tailscale CAD Viewer on `2026-08-24`: exact page HTTP `200`; final locked
  STEP artifact state `ready`.
- Regression result: `29 passed`; all eight STEP topology checks returned
  `ok:true`, `failureCount:0`.
- Physical PETG flexure, fit, wobble, retention, heat, wear, vibration,
  self-lock, solder ergonomics, removal ergonomics, and springback remain
  unproven.
- The next physical gate is the straight/curved slot, cap, and keeper coupon
  set before any full assembly print.

The detailed D05/I04/C04/V04/R04 receipts below remain the evidence authority.

## P17-D05 final focused repair design receipt

Status: complete as documentation-only repair design. No CAD/source/tests,
artifacts, requirements, continuity, review, validation, git, slicer, or
physical-acceptance changes were made by this role.

Inputs:

- P17-I03 candidate fingerprint:
  `2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`;
- P17-D04 frozen design-doc manifest:
  `72b9319c25fc17c57a27af2102288072fdcf3a6f8adc4cb3d7375fc146eca3aa`;
- P17-C03/P17-V03 blockers: lock shoulder collision during normal closing,
  completed-pigtail removal collisions, ambiguous full-X body-shadow wording,
  thin keeper wall, and non-reproducible prose-only candidate fingerprint;
- user P17-D05 directions preserving P17 R2 identity and requiring no extra
  structure.

Selected P17-D05 repairs:

- Retain the P17 R2 architecture: four plates, fixed inner plates, independently
  counter-rotating outer plates, single stepped offset hex/round axle, narrow
  `4.20 mm` continuous cam slots, no yoke/stability bars, larger right outer,
  and six permanent caps.
- Replace the blunt right-inner retaining shoulder with a same-solid one-way
  receiver: closing lead-in ramp, zero-penetration throat, hard-stop face,
  opening-side undercut/catch, and a modeled user-operable release deflection.
  The seated and released checks must use the same actual receiver occurrence;
  no imaginary shifted receiver is allowed.
- Add required lock states: closing sweep through `20,24,28,30,31 deg` with
  zero shoulder collision, locked `32 deg` hard-stop/capture, over-close
  `33 deg` allow-listed hard-stop only, unreleased-opening catch, and released
  opening clearance.
- Define completed-pigtail removal as release, full return to open service
  state, then a real modeled dogleg/window extraction path. Both fixed inner
  plates require production `completed_pigtail_window` cuts, initially centered
  near world `Z=22.50 mm` with `8.00 mm` `Z` width and front-side `+Y`
  extraction, tuned only by actual-solid clearance.
- Clarify the "behind XT60" rule: pivot centerline stays behind the body on
  `-Y` and pivot `Z` stays inside the body-height projection; the full
  X-spanning axle/keepers are not required to fit inside XT60 body `X` width,
  but actual axle/keeper solids still require zero collision and `>=0.75 mm`
  clearance to solder/wire/heat-shrink/tool/removal envelopes.
- Repair keeper print-readiness by replacing the P17-I03 `0.55 mm` annular
  wall with `outer_keeper_outer_diameter = 10.00 mm`,
  `keeper_bore_diameter = 7.55 mm`, `keeper_radial_wall >= 1.20 mm` at retained
  lobes, and a keeper-retention coupon ladder before any physical claim.
- Require persisted
  `p17-r2-candidate-manifest.json` and
  `p17-r2-candidate-fingerprint.json`; the fingerprint is the SHA-256 of the
  canonical fingerprint JSON file bytes and must be reproducible with
  `LC_ALL=C shasum -a 256`.

Changed paths:

- `projects/xt60-bend-jig/docs/iterations/p17-r2-direct-cad-counter-twist/BRIEF.md`
- `projects/xt60-bend-jig/docs/iterations/p17-r2-direct-cad-counter-twist/DESIGN.md`
- `projects/xt60-bend-jig/docs/iterations/p17-r2-direct-cad-counter-twist/HANDOFF.md`

P17-D05 frozen BRIEF/DESIGN hashes:

- `BRIEF.md`:
  `d79381a27ad3030e7d07e2c7a496cd9b71ce37b532f1162d787ee90f430dfa13`;
- `DESIGN.md`:
  `d46b5f906fc377a3fa7370b4338aa3728e442f2cd10ca2b5a79c32b1b1d3cf48`.

Validation/risk boundary:

- P17-D05 is a design contract only. It does not claim CAD implementation,
  artifact validity, slicer readiness, printed fit, lock force, thermal
  behavior, retention force, vibration resistance, or physical acceptance.
- If the next implementation cannot satisfy pass-in/retained/released lock
  states or released-open completed-pigtail removal using only the existing
  right inner/outer parts and within the P17 R2 architecture, return to design
  with `REQ-016` or removal unresolved instead of adding structure silently.

Next action:

- Route the next implementation repair candidate against `P17-D05`; assign the
  exact implementation task id in the persisted candidate manifest.

Supersession note: the older D04/D03/I03 receipts below are preserved as
history. Where they conflict with the P17-D05 receipt or DESIGN contract above,
P17-D05 controls the next implementation.

## P17-D04 repair design receipt

Status: complete. This was a bounded mechanism repair-design pass only. It did
not edit CAD source, tests, generated artifacts, requirements, project
continuity, review, validation, git/PR state, or physical acceptance records.

Inputs:

- P17-I02 candidate fingerprint:
  `cbec2062217dcdbbc8e5e0cc6f278bebc5ecaede8a517f0945c8030299e168de`.
- P17-D03 docs manifest:
  `18e5b14b5fa01e2b03dcd4aa2a1e8347b5046070049e087508a1959dd46389b1`.
- P17-V02 failure: center axle and keepers collide with diagonal rod/caps in
  written STEP/source BREP.
- User P17-D04 directions: prefer offset shared pivot; axle/keeper sits behind
  XT60 body away from wire-exit/solder side; recalculate every guide and cam
  slot around the offset pivot; reject `4.90 mm` and `7.55 mm` slot widths.

Selected smallest repair contract:

- Preserve P17 R2 identity: four plates, fixed inner plates, independently
  counter-rotating outer plates, one stepped hex/round center axle, six
  permanent caps, no yoke/stability bars, no simulator.
- Offset the shared pivot/center axle behind the XT60 body:
  `pivot_y = -10.60 mm`, `pivot_z = 17.00 mm`.
- Interpret `+Y` as outgoing-wire/solder side and `-Y` as behind-connector
  side. The axle/keeper centerline must sit inside the XT60 body `XZ` shadow in
  locked state and away from the solder-joint/outgoing-wire side.
- Require zero actual-solid axle/keeper intersection with XT60 body, solder
  joints, wires, heat-shrink, soldering-tool, release, and completed-pigtail
  envelopes across open/mid/locked, with `0.75 mm` minimum positive CAD
  clearance target.
- Recalculate every fixed inner guide and rotating outer cam slot around the
  offset pivot; do not translate axle alone.
- Use provisional repaired guide centers:
  - `upright`: open `(1.00, 12.00)`, locked `(1.00, 24.00)`;
  - `bottom`: open `(-2.00, 9.00)`, locked `(8.00, 9.00)`;
  - `diagonal`: open `(8.00, 8.00)`, locked `(2.00, 14.00)`.
- Resize only as needed for the offset guide/web envelope:
  `inner_plate_diameter = 54.00 mm`,
  `left_outer_secondary_grip_diameter = 60.00 mm`,
  `right_outer_primary_grip_diameter = 63.00 mm`.
- Replace rejected slot widths with low-wobble defaults:
  `fixed_slot_width = 4.20 mm`, `outer_cam_slot_width = 4.20 mm`,
  nominal CAD center slop `±0.10 mm`.
- Add PETG slot-fit coupon ladder for actual `OD4.00 mm` rods:
  `4.10, 4.15, 4.20, 4.25, 4.30 mm`, in both straight fixed-guide and
  representative curved cam-slot forms. This is a physical gate, not
  acceptance.
- Cut each outer cam slot from the continuous part-local centerline
  `R_x(-alpha_s(theta)) * (rod_center_i(theta) - pivot_yz)` with reconstruction
  error below `0.05 mm`. Do not use an oversized straight endpoint capsule.
- Reduce nonfunctional slot/rail bulk: no raised rails without named function,
  slot webs minimum `2.20 mm`, preferred `2.40..3.20 mm`, and any local wall
  above `4.00 mm` needs a named load-path/strength justification.
- Strengthen `REQ-016` with actual receiver-pocket/lock-nose geometry:
  hard-stop contact at lock, opening-side retaining shoulder, default
  `0.40 mm` over-center capture, blocked unreleased opening sweeps at `1 deg`
  and `2 deg`, and released-opening clearance proof.

Read-only evidence run by P17-D04:

- Source constants confirmed current candidate used `rod_diameter = 4.00`,
  `fixed_slot_width = 4.90`, and `outer_slot_width = 7.55`.
- Read-only BREP probe with `pivot_yz = (-10.60, 17.00)` and repaired guide
  centers above reported no axle/keeper/rod/cap/XT60/wire intersections in
  open, mid, or locked states.
- Approximate scalar behind-body clearances before actual-solid verification:
  central hex corner to XT60 back face `≈0.78 mm`; keeper to XT60 back face
  `≈1.25 mm`.

Required P17-I02 repair tests:

- actual-solid collision matrix for axle, keepers, rods, caps, XT60 body,
  solder joints, wires, heat-shrink/service envelopes, soldering tool,
  release, and completed-pigtail removal across open/mid/locked;
- positive clearance report with `0.75 mm` target for axle/keeper service
  envelopes;
- one-pivot-datum test proving axle, inner bores, outer bores, guide slots,
  cam slots, and lock geometry all use the offset pivot;
- cam centerline reconstruction/slop tests across open/mid/locked and
  intermediate samples, with rod-center reconstruction error below `0.05 mm`;
- absence tests for rejected `4.90 mm`/`7.55 mm` slot defaults and oversized
  straight endpoint-capsule cam slots;
- no-binding/no-wobble-envelope tests using nominal `4.20 mm` slots and
  reporting CAD slop;
- slot coupon artifact/test for the `4.10..4.30 mm` ladder;
- rail/bulk tests for named minimum and maximum slot webs;
- falsifiable lock tests for hard-stop contact, over-center capture,
  unreleased opening block, released opening clearance, and no collision
  regression.

Unresolved risks:

- Physical slot fit, rod wobble, PETG slot wear, keeper retention, lock force,
  heat, vibration, soldering ergonomics, and springback remain physical gates.
- If actual lock contact plus over-center capture cannot be achieved on the
  existing right inner/outer plates without adding structure, `REQ-016` remains
  unresolved and must return to design.

## What changed

`P17-D02` refined the P17 R2 direct-CAD contract after the user corrected the
architecture: do not add yoke/stability bars. P17 R2 remains the same
counter-twist design revision, not a new `P` version. The design contract now
selects a two-hand direct counter-twist architecture:

- two fixed inner plates grounded by one stepped center axle;
- larger central hex spacer section setting the fixed-inner clear span and
  providing axial shoulders;
- smaller hex key sections fixing the inner plates rotationally;
- outer round journal sections supporting independent left/right outer plate
  rotation;
- thin axial keepers retaining the stack with named running clearance;
- two independently supported outer hand plates rotating in opposite
  directions;
- no shared same-direction shaft and no animation sidecar;
- three rigid rods constrained by fixed inner guide slots and complementary
  physical outer slots;
- six permanent rod-end follower caps;
- a right primary actuator side with larger grip/lever affordance and an
  endpoint hard-stop/detent/over-center lock concept.

`P17-D03` corrects the D02 numeric/assembly defaults after a read-only audit
found an impossible slide-over path: an `AF6` fixed-inner hex bore/key cannot
slide over an `OD8` round journal. P17-D03 supersedes that numeric table inside
P17 R2 and requires:

- `outer_journal_diameter < fixed_inner_hex_bore_af`;
- coherent provisional defaults: central spacer hex `AF10`, inner key `AF8`,
  fixed-inner hex bore about `AF8.15`, round journal `OD7.60`, and outer
  bearing bore about `7.90`;
- per-side axle sequence from central shoulder through full inner hex key,
  running gap, full outer plate thickness, keeper clearance, and actual keeper
  seat;
- axle solid extending under a retained keeper;
- a modeled retained keeper, provisionally a permanent press-fit end ring on a
  real seat/groove, not a floating ring.

## Changed paths

- `docs/iterations/CURRENT`
- `docs/iterations/p17-r2-direct-cad-counter-twist/BRIEF.md`
- `docs/iterations/p17-r2-direct-cad-counter-twist/DESIGN.md`
- `docs/iterations/p17-r2-direct-cad-counter-twist/VALIDATION.md`
- `docs/iterations/p17-r2-direct-cad-counter-twist/REVIEW.md`
- `docs/iterations/p17-r2-direct-cad-counter-twist/HANDOFF.md`
- `docs/REQUIREMENTS.md`
- `docs/EXPERIENCE.md`
- `docs/decisions/ADR-0003-p17-r2-direct-cad-counter-twist.md`
- `docs/decisions/README.md`

## Not changed

No Python source, JavaScript source, tests, generated CAD artifacts, slicer
artifacts, root config, git/PR state, or physical acceptance was changed by
`P17-D03`.

The implementation receipt below is now superseded. It still lists
pre-correction `p18_*` source, test, and CAD artifact paths because this
bounded design correction did not mutate source/tests/artifacts. Those files
were generated against the previous yoke/annular-journal contract and are
historical evidence only. Any first center-axle implementation produced from
the P17-D02 numeric table is also superseded if it preserves the impossible
`AF6` / `OD8` slide-over path. A separate implementation owner must perform a
P17-I02 source/artifact update from this corrected contract.

## Next action

Assign `P17-I02` to implement the corrected stepped-center-axle contract in source and
regenerate artifacts. The implementer must read `BRIEF.md`, `DESIGN.md`,
`docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`, and
`docs/decisions/ADR-0003-p17-r2-direct-cad-counter-twist.md` before editing.

The first implementation candidate must make these defects fail if present:

- fixed inner plates rotate;
- outer plates rotate same direction or share a same-direction shaft;
- center axle couples either outer plate's rotation;
- yoke/stability bars, yoke sockets, or yoke tenons appear;
- central axle is not one piece, lacks larger central hex spacer shoulders,
  lacks smaller fixed-inner hex key sections, lacks outer round journals, or
  lacks thin axial keepers;
- fixed-inner hex bore cannot slide over the outer round journal and keeper
  seat before seating on the inner hex key;
- round journal OD is not smaller than the fixed-inner hex bore inscribed
  diameter;
- the per-side center axle does not extend under the retained keeper;
- keeper is a floating ring instead of a modeled retained press-fit/groove or
  equivalent keeper;
- outer bearing bore is not derived from the round journal plus named running
  clearance;
- any fixed guide slot moves between STEP states;
- any outer slot is world-space/scene-only rather than part-local geometry
  transformed by the outer plate occurrence;
- left and right rod ends reconstruct different `YZ` centers or rod skew;
- P13's `26.2 mm` span, `50.00 mm` rod freeze, or `ID3.90` permanent cap
  interference is preserved as accepted;
- cap count is not six permanent caps;
- right primary side lacks a quantified larger grip/lever affordance;
- lock geometry lacks a grounded hard-stop/detent/over-center reaction path;
- XT60 plastic body appears in the load path;
- central axle collides with XT60 body, wires, soldering, cooling, release, or
  completed-pigtail removal envelopes;
- any simulator/Three.js/JS sidecar is introduced.

## Acceptance boundaries

- CAD/source: no current implementation candidate for the P17-D03 corrected
  stepped-center-axle contract. The pre-correction and D02-numeric candidates
  are superseded.
- STEP: no current STEP candidate for the P17-D03 corrected stepped-center-axle
  contract.
- Mesh/3MF/slicer: not generated or accepted.
- Physical: not accepted.

## P17-I02 implementation receipt

Status: implementation candidate complete; not self-approved. Requires
independent critic, validation, and formal review before digital acceptance.

Verified frozen inputs:

- P17-D03 manifest:
  `18e5b14b5fa01e2b03dcd4aa2a1e8347b5046070049e087508a1959dd46389b1`
- `BRIEF.md`:
  `43a3d57022435eb768cb449fa70074ab4811a598c98d99bbae94bbe16f8fc9f6`
- `DESIGN.md`:
  `3edca74e706fd43c6c5e32d74fbcb1a3ad0d9776bf3499b2cbb42bec26c5ccc1`
- `docs/REQUIREMENTS.md`:
  `567e315522a0d5269daef52f95ff91cb67da3c1dd8b41ec5be5aa99ea646a2f5`

Candidate fingerprint:
`cbec2062217dcdbbc8e5e0cc6f278bebc5ecaede8a517f0945c8030299e168de`.

Implemented paths:

- `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`
- `tests/test_p17_r2_direct_counter_twist.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_open.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_mid.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_locked.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_exploded.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_print_kit.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_permanent_cap_coupon.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_center_axle_coupon.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_lock_closeup.step.py`
- `cad/p17_r2_direct_counter_twist/*.step`
- `cad/p17_r2_direct_counter_twist/snapshots/*.png`
- `cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json`

Key implemented constraints:

- Authoritative P17 R2 namespace; no active `p18_*` implementation paths remain
  after replacement verification.
- No yoke/stability bars, yoke sockets, or yoke tenons.
- One stepped center axle with central spacer `AF10`, inner keys `AF8`,
  fixed-inner hex bores `AF8.15`, round journals `OD7.60`, and outer bearing
  bores `7.90`.
- Slide-over invariant enforced:
  `outer_journal_diameter < fixed_inner_hex_bore_af`.
- Center axle total length `34.90 mm`; per-side sequence is inner key,
  running gap, full outer-plate journal, keeper axial clearance, and keeper
  seat.
- Separate permanent press-fit keeper rings are modeled on real end seats, not
  floating rings. Keeper retention force remains a physical/coupon gate.
- Inner clear span remains `18.40 mm`; rod length target remains `40.60 mm`,
  not inherited `50.00 mm`.
- Left/right outer rotations are equal magnitude and opposite sign.
- Fixed inner guide loci are state-independent; outer slots are part-local and
  reconstruct zero-skew rod centers.
- Six permanent caps with one-sided blind sockets and a cap coupon ladder.
- Right primary outer side has larger grip diameter and integrated rounded tab.
- Right fixed inner carries grounded stop geometry; BREP tests verify zero
  right-stop/right-outer intersection at open/mid, small allow-listed locked
  contact, and over-closed contact/penetration.
- Reference XT60 and wire envelopes are not load paths and clear the center
  axle in tested states.

Commands/results:

- `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py projects/xt60-bend-jig/tests/test_parameters.py -q`
  -> `20 passed`.
- CAD `scripts/gen --write --force --json` for eight explicit P17 R2
  generators -> all `ok:true`, `outcome:"built"`.
- CAD `scripts/inspect validate` for all eight written STEP files -> all
  `ok:true`, `failureCount:0`.
- CAD `scripts/inspect refs ... p17_r2_print_kit.step --facts --planes --positioning`
  -> size `[240, 160.081, 11.4]`, occurrence count `13`.
- CAD `scripts/snapshot` for open, mid, locked, exploded, print kit, permanent
  cap coupon, center axle coupon, and lock closeup -> all rendered without
  warnings.
- CAD Viewer handoff attempted; startup failed because `npm` was not available
  in the execution environment.

Primary hashes:

- Source:
  `339440b6fe38aaf797916928a986d1a38758cdb939ef5f87f264488f02f6ffbe`
- Tests:
  `c5611aee9a47707ffd6078487445b6ac5a6768ab41475bb76ae1951e309420ba`
- Provenance JSON:
  `d162b6dbd4944e2f4fa82c30bb180a45dd97ab4aede1cc1856a5a33b6efbdc00`

STEP SHA-256:

- `p17_r2_open.step`:
  `a2340443daf21ff72783372fa065a0c6a996fe2f19255436c486d7b75d39a325`
- `p17_r2_mid.step`:
  `5f75c9aae71738c3fbc637102bb796b28814924f00170e9d7fdee67d8af0da88`
- `p17_r2_locked.step`:
  `0ce95ddba90b22953ba1e15e7e521bd6debcc98963e52fac1ff7abbcf4bfbe8a`
- `p17_r2_exploded.step`:
  `48da6365f42a134b00390e3cbc64b8f9e14ead9a50fc8c4f6b1c98e9fc0631e8`
- `p17_r2_print_kit.step`:
  `c930572e7b3e7a2d43ba0b07d021a1d1480687b2c124c93b7684c4c1dfb1c5b6`
- `p17_r2_permanent_cap_coupon.step`:
  `da9c0e0dabee631b3e015c543e32a1d6635aa5740dee40f831ed7a868ecf6179`
- `p17_r2_center_axle_coupon.step`:
  `5dbf06fcbada10e21960f26f91d0d18da121a62915927cd2868f9fdf06ee4779`
- `p17_r2_lock_closeup.step`:
  `7a7e445345bc034f655760a1461f3b7d5fbb14a2028cd8a731ca6bf85c4ed97b`

Snapshot SHA-256:

- `p17_r2_open_20260824T125845Z.png`:
  `2100a4ae34cc275758c7110cf0e401bb0b5cceb0636a113d3a7fb084e693f081`
- `p17_r2_mid_20260824T125852Z.png`:
  `e793a23128530abeffae88e3164fc1632776127e39b95da1aea2d661dc03b0d7`
- `p17_r2_locked_20260824T125859Z.png`:
  `9fe71e47e68b036e1afe554e0b43518c605e1a457339aa441d839324e0a358c5`
- `p17_r2_exploded_20260824T125906Z.png`:
  `0706bbc1146a84daf0afeec69aac5581a7e37458ff987c4e7e4b2c6a6369b02c`
- `p17_r2_print_kit_20260824T125912Z.png`:
  `55fe6ac7507c0be0c44b1532334c3f8103c4d848151be519dcc09b1c070eab05`
- `p17_r2_permanent_cap_coupon_20260824T125913Z.png`:
  `72faa16485a7f5f9940bd3cd8e28e923ff38f7adf3c9a55d8b166ca7d2264ecc`
- `p17_r2_center_axle_coupon_20260824T125919Z.png`:
  `616a222ab7ccc00cf41a44d8a885e986a7dc281b9a3b5be71ca754934b3b8fd4`
- `p17_r2_lock_closeup_20260824T125922Z.png`:
  `9fe71e47e68b036e1afe554e0b43518c605e1a457339aa441d839324e0a358c5`

Unresolved risks:

- This is CAD/source and written STEP evidence only. No physical cap retention,
  keeper retention, lock force, self-lock, heat, wear, vibration, wire holding,
  springback, or PETG fit is accepted.
- STEP colors are clearer in snapshots after source color reapplication, but
  CAD Viewer live review could not be verified in this environment because
  `npm` was unavailable.

Smallest next action: run independent critic `P17-C02` against candidate
`cbec2062217dcdbbc8e5e0cc6f278bebc5ecaede8a517f0945c8030299e168de`.

## Superseded pre-correction implementation receipt

Correction note: this receipt was originally recorded under `P18-I01`, then
temporarily relabeled as P17 R2. It is now superseded by the P17-D02
center-axle correction and the P17-D03 numeric/assembly correction. The hashes
and exact implemented paths below are preserved as observed and were not
renamed or edited in this correction.

Candidate fingerprint:
`4b9c53e3c060d35a8b401db6389da9d3ff7005c93f871e5e6bb9b3bd53f52cd3`.
Source SHA-256:
`290d7b8861fa0ee7f820a021ff6dbdff0e3bb02fb91577a77df2a774000d1b7a`.
Test SHA-256:
`2ab3ce3201d954cf91da0cc07ada638d773b20ed074cedaef300ca4ee8aa5504`.

Implemented paths:

- `src/xt60_bend_jig/p18_direct_counter_twist.py`
- `tests/test_p18_direct_counter_twist.py`
- `cad/p18_direct_counter_twist/p18_open.step.py`
- `cad/p18_direct_counter_twist/p18_mid.step.py`
- `cad/p18_direct_counter_twist/p18_locked.step.py`
- `cad/p18_direct_counter_twist/p18_exploded.step.py`
- `cad/p18_direct_counter_twist/p18_print_kit.step.py`
- `cad/p18_direct_counter_twist/p18_permanent_cap_coupon.step.py`
- `cad/p18_direct_counter_twist/p18_lock_closeup.step.py`
- `cad/p18_direct_counter_twist/*.step`
- `cad/p18_direct_counter_twist/snapshots/*1157*.png`
- `cad/p18_direct_counter_twist/p18-artifact-provenance.json`

Key implemented constraints:

- inner clear span `18.40 mm`;
- rod length target `40.60 mm`, not the rejected `50.00 mm`;
- left outer angle `-theta`, right outer angle `+theta`;
- fixed inner guide loci are state-independent;
- outer slots are part-local and reconstruct the same world rod centers;
- six permanent caps with one-sided blind sockets, default socket `ID4.04`;
- cap coupon ladder: `ID3.96, 4.00, 4.04, 4.08, 4.12` by depths
  `3.50, 4.00, 4.50`;
- right primary plate has `2.00 mm` larger lever radius than left;
- fixed-inner journal `OD13 / ID8`, radial wall `2.50 mm`;
- outer bearing bore `13.40 mm`;
- journal overlap into outer bore `2.40 mm`, outer-face clearance `0.80 mm`;
- no shared D shaft, no simulator, no JS/animation sidecar.

Commands/results:

- `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p18_direct_counter_twist.py projects/xt60-bend-jig/tests/test_parameters.py -q`
  -> `19 passed`.
- `git diff --check` -> clean.
- `scripts/gen ... --write --force --json` for all seven P17 R2 generators ->
  built.
- `scripts/artifact --force --kind assembly` and `scripts/inspect validate`
  for all seven P17 R2 STEP files -> all `ok: true`, `failureCount: 0`.
- `scripts/snapshot` for open, mid, locked, exploded, print kit, permanent cap
  coupon, and lock closeup -> all rendered without warnings.

Final STEP SHA-256 values:

- `p18_open.step`:
  `dd2e861383769c25ef29f91c953bdb754efe7f4269e69371c2ab0259e41779d7`
- `p18_mid.step`:
  `f53f49a859b8174805ffddf0e86396be283f824459cc29de3d1f8b8ce25d218a`
- `p18_locked.step`:
  `e58a2e0117f884d0fd233de330f45c9bd2bc394ddc98f9634d6be7501f141d7a`
- `p18_exploded.step`:
  `0a818bad5c38cf5a6c96dc8d4a7edca6d27a9ac1826b7e9ab677fa191923f9a9`
- `p18_print_kit.step`:
  `129c04287f5e6f1a1a4ca5fd1da2efdc0e93b0ad076270038d165a7d188feac6`
- `p18_permanent_cap_coupon.step`:
  `72584968756f6be27c5100573a57a1f61b5c9fdc97e9fa7eff6da334108afa8e`
- `p18_lock_closeup.step`:
  `5a45f48f90d31402aee9bdea15eda9b32b040ad60c565eb81fb50d034c8492ef`

Important boundary:

The earlier full project pytest run was interrupted after a long mixed-state
run and is not recorded as passing evidence. It started before later P17 R2
source/artifact repairs and should not be used for acceptance.

## P17-I03 replacement implementation receipt

Status: implementation complete against frozen P17-D04 inputs; not
self-approved. Independent critique, validation, formal review, CAD Viewer
handoff, slicer proof, and physical proof remain separate gates.

Verified input provenance:

- frozen design-doc manifest:
  `72b9319c25fc17c57a27af2102288072fdcf3a6f8adc4cb3d7375fc146eca3aa`;
- `DESIGN.md`:
  `17b5bfe10ea13e3a4fe34ebdd0a0485f6814195018d5c9e7e2033fbf8523e3da`;
- `BRIEF.md`:
  `f3e3fbae98597d3cd8cf4ed9ae13dd305b8edb53d794d9dfe0331a794d53e8ad`;
- `docs/REQUIREMENTS.md`:
  `567e315522a0d5269daef52f95ff91cb67da3c1dd8b41ec5be5aa99ea646a2f5`.

Candidate fingerprint:

- `2761adf6154054185bb2cff21e3ef7b923e06682ab760b1acd1e99a22aa370f8`;
- method: SHA-256 of canonical JSON containing the frozen-doc manifest plus
  path-and-SHA-256 rows for the authoritative source, focused test, and eight
  written STEP files.

Changed paths owned by this implementation task:

- `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`;
- `tests/test_p17_r2_direct_counter_twist.py`;
- `cad/p17_r2_direct_counter_twist/` source entrypoints, eight STEP files,
  render packages, fresh snapshots, and provenance JSON;
- this appended receipt in `HANDOFF.md`.

Implemented result:

- preserves four plates, fixed hex-keyed inner plates, independently
  counter-rotating round-journal outer plates, one stepped offset axle, two
  permanent keepers, six permanent caps, and the larger right actuator;
- shared pivot is `YZ=(-10.60, 17.00) mm`, behind the XT60 body; axle, inner
  plates/bores, outer plates/bores, guide/cam construction, and lock geometry
  all derive from that datum;
- both production guide/cam widths are `4.20 mm` for `OD4.00 mm` rods;
  rejected `4.90/7.55 mm` defaults are absent;
- each outer cam is the continuous 33-sample part-local inverse-transform
  locus; reconstruction error is gated below `0.05 mm` and no straight
  endpoint-only cam shortcut remains;
- permanent-cap coupon now also contains five straight and five representative
  curved slot coupons at `4.10, 4.15, 4.20, 4.25, 4.30 mm`;
- right outer carries an integral round lock nose; right inner carries a
  grounded receiver pocket with hard stop and retaining shoulder;
- locked hard-stop and shoulder overlap are zero, `+1 deg` overclose engages
  the hard stop by `1.0993069026 mm^3`, unreleased `-1/-2 deg` opening engages
  the shoulder by `0.1377097379/1.5819943041 mm^3`, and the modeled released
  `-2 deg` sweep clears; over-center capture is `0.40 mm`;
- nine sampled motion states have zero unintended rod/cap intersection with
  axle, keepers, inner plates, outer plates, or XT60 body;
- actual-solid axle/keeper clearance to XT60 and +Y solder, wire, heat-shrink,
  tool, release, and removal envelopes is at least `0.7764973081 mm`, above
  the `0.75 mm` target;
- print-kit occurrences are recentered and bed-aligned; no yoke/stability bars,
  simulator, animation, shared outer coupling, or removable caps were added.

Implementation correction to a provisional design input:

- the provisional P17-D04 guide-center table was probed as actual rods and
  found to intersect the XT60 body substantially; it therefore failed the
  higher-priority actual-solid collision gate;
- the implementation preserves the partial repair's recalculated
  collision-free world guide centers (`upright -12,3 -> -18,13`,
  `bottom -5,-12 -> 8,-12`, `diagonal 11.5,9 -> 3,1`) and regenerates both
  counter-rotating outer cams from them; independent critique must review this
  evidence-backed deviation rather than treating the provisional table as
  accepted geometry.

Exact commands and results:

- `uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py projects/xt60-bend-jig/tests/test_parameters.py -q -x`
  -> `27 passed`;
- CAD `scripts/gen --write --force --json` on all eight explicit
  `p17_r2_*.step.py` entrypoints -> eight `outcome: built`;
- CAD `scripts/artifact --force` followed by `scripts/inspect validate` on all
  eight final STEP files -> all `ok: true`, `failureCount: 0`;
- source/export parity script -> all eight occurrence counts, dot-normalized
  labels, transforms, and bounds match; maximum bound delta
  `0.0000005 mm`;
- CAD `scripts/snapshot` using the pinned skill requirements -> eight fresh
  PNGs, all `ok: true`, `warnings: []`; all were visually inspected, and the
  initially redundant lock framing was replaced by a tight lock close-up;
- `jq empty cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json`
  and path-limited `git diff --check` -> clean.

Authoritative hashes:

- source:
  `2de1784d71300cd85c8753f10e2868cdd7b4cbb9a6331808d4ee7f56c072817d`;
- focused test:
  `b44d34a7dec06db3ba379e8eaca10ad1f905cc24f8d05e433c4f9cf4d2a10237`;
- parameter manifest:
  `183800722143c2c8894f9c7817a56b6fa99894e42886db5587cf797c55f82515`;
- artifact provenance JSON:
  `7a826f100f3ae48c6ecf43f0b44ad77a557a321ac3769eb0361d6a84d923da4b`;
- every STEP and selected fresh snapshot SHA-256 is recorded in
  `cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json`.

Visual review findings:

- open/mid/locked states visibly preserve fixed inner plates and opposite
  outer rotation; rods sit in narrow curved outer slots;
- stepped hex/round axle, keepers, permanent caps, larger right outer, and
  grounded receiver/nose are visible; no unintended extra stability members
  appear;
- bed-aligned print kit and the five-width straight/curved slot ladder are
  visible; no missing or obviously overlapping production part was observed;
- the transparent XT60/service reference envelope is presentation-only and is
  not part of the print kit or load path.

Unresolved physical risks:

- `4.20 mm` slot fit and real rod wobble/wear require the PETG straight/curved
  coupon on the actual `OD4.00 mm` rods;
- cap and keeper installation/retention, PETG creep, lock release force,
  vibration resistance, heat response, wire holding, solder ergonomics,
  springback, and self-lock remain unproven physically;
- this receipt makes no 3MF, slicer, print, or physical-acceptance claim.

## P17-I04 final focused implementation receipt

Status: implementation complete against frozen P17-D05 inputs; not
self-approved. Independent critique, validation, formal review, CAD Viewer,
slicer/3MF, print, and physical acceptance remain separate gates.

Verified immutable inputs:

- P17-D05 frozen manifest:
  `64c6db4496520007f4b31c0050809fad29ce949e34e7c806a387107c099946cd`;
- `BRIEF.md`:
  `d79381a27ad3030e7d07e2c7a496cd9b71ce37b532f1162d787ee90f430dfa13`;
- `DESIGN.md`:
  `d46b5f906fc377a3fa7370b4338aa3728e442f2cd10ca2b5a79c32b1b1d3cf48`;
- pre-I04 `HANDOFF.md`:
  `45127fd5f372246aa2b847aecbe95bb8937d4b0959bde37c51677ec9f118a4f6`;
- baseline commit: `05e0152b045bd82a41ea07a715f2361606c1ec99`.

Candidate identity and reproducibility:

- candidate fingerprint:
  `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`;
- persisted canonical payload:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`;
- persisted companion hash:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.txt`;
- persisted candidate manifest:
  `cad/p17_r2_direct_counter_twist/p17-r2-candidate-manifest.json`, SHA-256
  `c5fbeaaee626ad3adafb4f2cb5ca195c27e84683c4c4db9b2b27e25fa5241ae2`;
- independent command
  `LC_ALL=C shasum -a 256 projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/p17-r2-candidate-fingerprint.json`
  returned the candidate fingerprint above;
- canonical JSON, sorted `path`/`kind` arrays, one trailing newline, manifest
  payload parity, and all 11 input/19 output path hashes passed independent
  reconstruction.

Changed implementation-owned paths:

- `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`;
- `tests/test_p17_r2_direct_counter_twist.py`;
- `cad/p17_r2_direct_counter_twist/` eight regenerated STEP files, render
  packages, eight selected fresh snapshots, provenance, manifest, fingerprint
  payload, and fingerprint text;
- this appended `HANDOFF.md` receipt only.

Implemented D05 result:

- preserved the accepted four-plate, one offset stepped axle, fixed-inner hex
  keying, independent opposite-rotation round-journal outers, larger right
  actuator, three existing guide paths, six permanent caps, narrow `4.20 mm`
  slots, and no stability bars;
- right inner now contains a single connected receiver solid with grounded
  rib, closing lead-in ramp, zero-penetration throat, hard-stop/load rib,
  undercut catch, connected flexure, and thumb tab. Seated, nose-driven closing
  deflection, and user-release deflection keep the same world receiver datum
  and each remain one connected solid;
- normal close `0..31.8 deg` has zero receiver intersection and minimum
  `0.5913644619 mm` catch clearance. Locked hard-stop/catch intersections are
  both zero with `0.40 mm` capture. Unreleased opening is blocked by the same
  catch at `31/30 deg` by `0.1377097379/1.5819943041 mm^3`. Released
  `32 -> 30 deg` has zero receiver intersection and minimum
  `1.3076630688 mm` catch clearance. Overclose has zero non-hard-stop
  interference;
- both fixed inner plates have actual rounded through-windows starting at
  world `Y=4.50 mm`, centered `Z=22.50 mm`, width `8.00 mm`;
- completed-pigtail removal is an actual-solid released-open dogleg at YZ
  waypoints `(0,21) -> (0,22.5) -> (8,22.5) -> (20,22.5) -> (34,22.5)`.
  It has zero production-solid intersections and minimum actual clearance
  `0.7764973081 mm`, above the required `0.75 mm`, without a reference
  allowlist;
- pivot metadata now explicitly requires the pivot behind the XT60 on `-Y`
  and `Z` inside the body projection, while rejecting the impossible demand
  that the full four-plate axle remain inside the body `X` width;
- each keeper is full `OD10.00 / bore7.55`, radial wall `1.225 mm`, with a
  three-bore physical retention coupon ladder. The mandatory keeper increase
  exposed a cap contact; the focused repair reduced follower-head OD from
  `7.20` to `6.60 mm`, retains `1.28 mm` socket wall, and gives zero keeper/cap
  intersection over 65 half-degree samples with minimum gap
  `0.1034375039 mm`. No guide, slot, axle, or axial-stack value changed.

Exact commands and results:

- `uv run pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py -q -x`
  -> `23 passed`;
- `uv run pytest projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py projects/xt60-bend-jig/tests/test_parameters.py -q -x`
  -> `29 passed`;
- `for f in projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/*.step.py; do PYTHONPATH=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad uv run python -m scripts.gen "$f" --write --force --json || exit 1; done`
  -> eight `outcome: built`;
- `for f in projects/xt60-bend-jig/cad/p17_r2_direct_counter_twist/*.step; do PYTHONPATH=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad uv run python -m scripts.artifact "$f" --force --kind assembly >/tmp/p17-artifact-last.json || exit 1; PYTHONPATH=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.25/skills/cad uv run python -m scripts.inspect validate "$f" || exit 1; done`
  -> all eight `ok:true`, `failureCount:0`;
- exact source/export parity command is persisted in
  `p17-r2-candidate-manifest.json`; it returned all eight occurrence counts and
  dot-normalized labels matching with maximum bounds delta
  `0.000000000 mm`;
- exact seven-state plus custom lock-closeup snapshot commands are persisted in
  the candidate manifest; eight final PNGs returned `ok:true`, `warnings:[]`.

Authoritative hashes:

- source:
  `7d6250693bacbcfe962649406b65c6917ac3a187b3f3537f215d5150fbfb43a3`;
- focused test:
  `e7fd569f83cecc5f43225327dbcc7943cb6a37f7d485e675052ba67b12a75455`;
- provenance JSON:
  `95b60da6cb9b11ff28d758e5b944322b8094bda86f2b102630895644af48ab43`;
- STEP hashes: center-axle coupon `61e6b5579fbf...`, exploded
  `49028de1ecbc...`, lock closeup `dd555503e49d...`, locked
  `c8a9407946f9...`, mid `fe92076f5896...`, open `4aff043f9114...`, permanent
  cap coupon `8f374e00b72c...`, print kit `f164094c6daf...`; exact full hashes and
  selected snapshot hashes are persisted in provenance and the candidate
  fingerprint payload.

Visual inspection findings:

- open/mid/locked snapshots show the four-plate stack, fixed inner pair,
  opposite outer rotation, offset stepped axle, OD10 keepers, permanent caps,
  and narrow curved slots; no extra bar/frame appears;
- fixed-inner front service windows and the actual blue released-open pigtail
  sweep are visible; the sweep is reference/service evidence, not a printable
  production part;
- the dedicated closeup clearly shows the blue right-outer nose captured by
  the orange connected receiver/catch and its thumb/flexure path;
- exploded, print-kit, cap/slot ladder, and axle/keeper coupon snapshots show
  the expected part census with no missing or visibly overlapping printed
  part.

Unresolved risks and next action:

- CAD proves the bounded deformation states and contact geometry, not actual
  PETG flexure strain, release effort, lock force, vibration resistance,
  thermal creep, or self-lock;
- keeper/cap installation force and retention, `4.20 mm` printed-slot fit and
  wobble, heat response, wire holding, solder ergonomics, springback, and the
  completed-pigtail hand path remain physical coupon/print gates;
- no 3MF, slicer, print, or physical-acceptance claim is made. Route exact
  fingerprint `24f5d752...` to distinct critic and validator owners.
