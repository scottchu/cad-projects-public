# XT60 bend jig project state

Last updated: `2026-08-26`

## Baseline and active iteration

- Canonical project: `projects/xt60-bend-jig`.
- Active iteration: `p18-r1-compact-counter-twist`.
- Active product baseline: **P18 R1**, explicitly opened by the user after
  approval of the compact P17 2D gate.
- CAD/source and six written STEP artifacts are formally accepted for exact
  candidate-manifest SHA-256
  `fb0755a0d448ee000dde4bd63eacca7fbaf6e55abeb16312a7f39c5ccfc5d1d5`.
- P18 plate diameters are `52.933/53.933/54.933 mm`; outer plates twist
  `-45/+45 deg`; fixed axle is `A=(-9.5,-9.5)` around virtual datum `C=(0,0)`.
- Three rods remain `OD4 x 50 mm`; six caps remain permanent; inner plates and
  axle are fixed; outer rails are inverse-transform-derived.
- Independent validation passed `10/10` tests, 65-state BREP and full
  two-sided support, with minimum web `2.200398673579 mm`, rank `3`, maximum
  normalized condition `3.750295905779`, and six exact STEP parity passes.
- Active handoff:
  `docs/iterations/p18-r1-compact-counter-twist/HANDOFF.md`.

Acceptance is digital only. Full solder-tool access, near-tangent hand force,
friction/wedging/backlash, cap/keeper retention, axle/hex fit, PETG tolerance,
heat, wear, mesh/3MF, slicing, printing and physical acceptance remain open.
P17 source/artifacts remain immutable history and were not modified by P18.

## Current D14 option-3 design result

The user authorized a deterministic joint search over outer rotation datum
`C=(Cy,Cz)` and one common rod translation `D=(Dy,Dz)`, while keeping the I10
workpiece/contact interface, `A=(-29,12)`, topology, identities, straight
strokes, `24 deg` counter-twist, plates and architecture fixed.

The feasible set is empty. Exact END three-point contact forces `D=(0,0)`.
At that locus the fixed axle/hex envelope to the bottom inner straight slot
has only `1.615172394712 mm` web, below the `2.20 mm` gate. This relation is
independent of `C`, so expanding or refining only the rotation-center search
cannot repair it. Independent P17-V14 reproduced the contact reduction and
web result.

A rail-only comparison near `C=(4.000,9.550)` gives worst full-path ratio
`1.086832`, worst contact-to-END ratio `1.088179`, and minimum crossing
diagnostic `19.448050 deg`, but is explicitly rejected because the fixed-inner
web still fails. It must not be implemented or presented as a CAD candidate.

The corrected cheap 2D evidence is
`docs/review/p17-r2-balanced-rail-search/p17-d14-bounded-infeasibility.svg`.
P17-V14 verified its red web geometry and all six 33-point rail polylines;
maximum plotted point error was `6.65e-10 mm`.

## Current blocked D13 review candidate

The feature branch materializes the user's exact locked placement as evidence,
not as an accepted product revision:

- every I10 rod state is translated by
  `D=(+16.1869657526,+10.2949747468) mm`;
- the purple fixed axle changes only from `A=(-29,17)` to `A=(-29,12)`;
- `C=(3,12)`, XT60, finite wire model, service geometry, plates, X frames,
  rod stock, caps, topology, and `24 deg` counter-twist remain frozen;
- one pure frame transform and one parametric mating-rail function derive all
  six outer rails; the common delta derives all three rod paths and inner
  tracks from the frozen I10 table;
- 22 implementation tests passed; V13 independently passed 14 focused tests,
  exact math/conditioning, all ten STEP validate/refs/parity gates, occurrence
  invariants, and RGB motion evidence.

D13 is nevertheless invalid as a product. At OPEN the bottom rod intersects
the XT60 body (`-2.000 mm` signed clearance, `199.805293 mm3` BREP overlap) and
the vertical wire (`2.448316 mm` radial overlap, `53.787371 mm3` BREP overlap).
At END the finite wire surface gaps are `8.136966`, `16.718340`, and
`7.877883 mm`, so the three-point forming contact is gone. R13 therefore
rejects PR merge/release. The branch must not replace accepted I08 on `main`
without an explicit design-scope reopening and a new independently accepted
candidate.

## Historical P17 accepted digital result

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
- Runtime: CAD Viewer `0.4.27`, using the canonical repository root uv Python
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
- D13 review page (transport/readiness only):
  `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_full_motion.step.py`.
- For exact D13, local and Tailscale page/artifact/assembly/params/one-GLB
  probes returned HTTP `200`; artifact state was `ready`, with ten components,
  eighteen occurrences, and one `open_to_end` parameter. No browser surface
  was available for live slider manipulation.

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

- Accepted baseline delivery: PR <https://github.com/scottchu/design-projects/pull/9>.
- Current blocked evidence branch: `codex/xt60-p17-r2-locked-rod-layout`.
- Blocked evidence commit: `8e7aba7`; branch pushed to `origin` for durable
  review, without a pull request.
- No D13 PR was opened or merged because C13/V13/R13 formally reject it for
  product advancement.
- Current D14 design branch: `codex/xt60-p17-r2-balanced-rail-search`; no PR or
  merge is eligible because D14 has no feasible implementation candidate.
- Preserve the unrelated user-modified P13 `p13_print_kit.3mf` in the canonical
  main checkout.

## Next action

Preserve D13 and D14 as review/design evidence. Before further source work,
obtain one explicit scope decision to reopen the fixed axle `A`, the fixed
axle/hex guide envelope, or the exact workpiece/contact placement. Merely
expanding the `C` search cannot work. Any superseding candidate must restore
zero OPEN body/wire collision, meaningful END contact, `>=2.20 mm` web and
acceptable rail/path balance, then repeat independent implementation,
critique, validation, formal review, and merge gating. Do not slice or print
D13 or the rejected D14 rail-only comparison.
