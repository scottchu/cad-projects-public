# XT60 bend jig project state

Last updated: `2026-08-25`

## Baseline and active iteration

- Canonical project: `projects/xt60-bend-jig`.
- Active iteration: `p17-r2-head-up-tail-right-orientation-repair`.
- Current design contract: `P17-D10-R2`.
- Accepted digital candidate: `P17-I08-R2`, formally accepted by `P17-R08`.
- Independent candidate fingerprint:
  `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`.
- Candidate manifest SHA-256:
  `0eaa98ffdc26baea5f409867929ffb9df317030bfa902cf20cd2b770919deb25`.
- Artifact provenance SHA-256:
  `97dccfad274fd82724f06c8e1ec15cd4ccc25659b6aa652dca7b8b9ecefb6b4b`.
- Canonical handoff:
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/HANDOFF.md`.

This remains P17 R2. The correction changes orientation and motion details
inside the accepted four-plate/three-rod architecture; evidence regeneration,
Viewer readiness, and focused numeric repair do not create a new P/R version.

## Accepted digital result

P17-I08-R2 is the source-derived four-plate, three-rod counter-twist candidate:

- the workpiece-relative front frame is fixed: `+Z` is XT60 mating-head/up and
  `+Y` is solder-tail/both-wires/right;
- OPEN uses the same three rod identities at upper-left, upper-right, and
  lower-right, with an exact upper-right/lower-right vertical leg;
- first contact and END converge upper-left -> middle -> lower-right on the
  accepted diagonal three-point wire wrap;
- all three moving rods are `OD4.00 x 50.00 mm` stainless stock with six
  permanent stepped blind caps;
- both inner plates, both keepers, and the purple stepped axle at
  `A=(-29.00,17.00) mm` remain world-fixed;
- the left/right outer plates counter-rotate by `-theta/+theta` about the
  virtual datum `C=(3.00,12.00) mm`, and the right force side is larger;
- fixed-inner rod guides are direct stationary straight tracks; all six outer
  rod rails and both axle rails are inverse-transform-derived;
- END is `24 deg`; the first-contact-to-END `0.25 mm` displacement is a
  geometric preload proxy only;
- no stability bar, yoke, linkage, gear, grip block, lock nose, receiver, or
  self-lock feature was added.

The production source retains legacy `locked` naming only for compatibility.
It means CLAMPED/END of prescribed travel and makes no retention claim.

## Independent evidence

- `P17-C08`: PASS with no blocker or major finding.
- `P17-V08`: PASS for CAD source, actual-solid motion/support/service gates,
  ten written STEP exports, source/export parity, and the frozen visual packet.
- `P17-R08`: ACCEPT for delivery of the unchanged exact fingerprint.
- Focused tests: `19 passed` through the repository root `uv` environment.
- Continuous two-sided rail support: `48,312` actual-solid probe points with
  zero failures and minimum full-probe material ratio
  `0.9999999999999983`.
- Motion/contact: zero unintended intersection, minimum XT60 clearance
  `0.750000 mm`, rank `3`, and maximum normalized condition `12.821633`.
- Service path: `2002` poses, zero intersection, BREP minimum clearance
  `1.250000 mm`, and analytic minimum `0.933816 mm`.
- Ten of ten STEP exports passed geometry validation and source/import parity;
  maximum bounds delta was `8.811e-12 mm`.
- OPEN/contact/END/opposite snapshots and the 72-frame motion GIF were visually
  inspected against `REQ-027` through `REQ-030`.

## Primary artifacts

- Parametric authority:
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Focused regression:
  `tests/test_p17_r2_direct_counter_twist.py`.
- Full motion:
  `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`.
- OPEN, contact, midpoint, END, exploded, print-kit, cap coupon, axle coupon,
  and both motion STEP exports are under
  `cad/p17_r2_direct_counter_twist/`.

## Viewer delivery

- Persistent singleton: `com.scottchu.cad-viewer` on `127.0.0.1:3245`, managed
  by `~/.local/bin/cad-viewer`; it survives agent/chat termination.
- Runtime: CAD Viewer `0.4.26`, using the canonical repository root uv Python
  `/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`.
- Exact local and Tailscale pages returned HTTP `200`; exact artifact endpoints
  returned HTTP `200` with `state: ready`.
- Assembly descriptor returned HTTP `200`, schema `2`, package schema `3`, ten
  components and eighteen occurrences; SHA-256
  `0b391d68f28c665594a2683219186fc45dfa51dedffbf95f8036b0d643f3125f`.
- The `open_to_end` params module and all ten GLBs returned HTTP `200` with
  identical local/Tailscale content hashes.
- Live browser slider manipulation was not independently exercised. Frozen GIF
  motion and Viewer transport/readiness are accepted separately.

## Acceptance boundary

- CAD/source and prescribed motion: digitally accepted for exact fingerprint
  `f5bc383f...` only.
- Ten written STEP exports and frozen visual/motion evidence: accepted.
- Viewer transport/readiness: accepted; interactive human review remains open.
- Mesh/DfAM/slicer/3MF: not generated or accepted for P17-I08-R2.
- Physical: not tested or accepted. PETG slot fit, permanent-cap and keeper
  retention, hand torque, holding force, wobble, insulation safety, heat,
  cooled bend angle, springback, creep, wear, vibration, endpoint retention,
  and self-lock remain physical gates.

## Repository delivery

- Branch: `codex/xt60-p17-r2-orientation-repair`.
- Pull request: pending creation/merge in the current delivery step.
- Preserve the unrelated user-modified P13 `p13_print_kit.3mf` in the canonical
  main checkout.

## Next action

Keep the accepted fingerprint unchanged while the user reviews the persistent
Viewer. After explicit print authorization, generate/slice only the accepted
P17-I08-R2 print package and perform the documented three-rod/cap/slot physical
test. Record first contact, END effort, rod wobble, wire marks, XT60 reaction,
cap/keeper retention, removal path, cooled bend angle, and springback. Do not
claim a physical lock: this candidate intentionally contains none.
