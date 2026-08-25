# P17-C08 independent critic review

Status: P17-C08 critic gate passes with no blocker or major finding for the
I08-R2 digital candidate. This is not physical acceptance.

Reviewed candidate:

- Gate manifest: `/tmp/p17-i08-independent-gate-manifest.txt`
- Candidate fingerprint / manifest SHA-256:
  `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`
- Frozen entry audit: 30/30 path hashes matched before review.
- Source hash:
  `6b9004c7fb7d102c320c1c4184a78bbfc717540a91e5ea4f03b5a1fe1637e49b`
- Tests hash:
  `b713552b6b5fdefe7259d67b3dde1d464e46be85702a85f926cfd055bdb88c99`
- Candidate records inspected:
  `projects/xt60-bend-jig/docs/iterations/p17-r2-head-up-tail-right-orientation-repair/HANDOFF.md`,
  `projects/xt60-bend-jig/docs/provenance/p17-r2-candidate-fingerprint.json`,
  `projects/xt60-bend-jig/docs/provenance/p17-r2-candidate-manifest.json`,
  `projects/xt60-bend-jig/docs/provenance/p17-r2-artifact-provenance.json`.

## Findings

### Blocker

None found.

### Major

None found.

### Minor / nonblocking

1. Endpoint naming remains visually/API ambiguous because the production state
   and STEP stem still use `locked`, while the contract correctly defines this
   as an end-of-travel/preload proxy only. Evidence: BRIEF says “locked” is
   only colloquial and not retention/self-lock at
   `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/BRIEF.md:61`;
   DESIGN repeats the endpoint-only constraint at
   `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:67`;
   tests explicitly assert `endpoint["selfLockClaimed"] is False` at
   `tests/test_p17_r2_direct_counter_twist.py:351`. This is not a gate blocker
   because the public manifest/test evidence prevents a self-lock claim, but it
   remains a UX naming risk for downstream review.

2. Front snapshots communicate the corrected workpiece orientation and rod
   topology, but contact and END are visually close because END is only the
   named `0.25 mm` geometric preload proxy after first contact. The numeric
   evidence is stronger than the visual delta here. Evidence: contact offsets
   are `4.15 mm` and END offsets are `3.90 mm` in
   `tests/test_p17_r2_direct_counter_twist.py:109`, and DESIGN defines this as
   non-force preload proxy at
   `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:24`.

## Requirement coverage

- `REQ-027` head-up / tail-right front frame is covered. The contract defines
  world `YZ`, `+Y` right, `+Z` up, mating head up and tails right at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:7`;
  source evidence returns `frontViewForm="└"`, `headDirection="+Z"`,
  `tailDirection="+Y"` through the test at
  `tests/test_p17_r2_direct_counter_twist.py:118`.
- `REQ-028` OPEN topology is covered. The exact OPEN table has upper-left plus
  upper-right/lower-right on common `Y=22.235` at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:39`
  and is asserted with `openRightVerticalLegDeltaY == 0.0` at
  `tests/test_p17_r2_direct_counter_twist.py:95`.
- `REQ-029` END topology/contact intent is covered. The END table retains
  upper-left, middle, lower-right diagonal coordinates at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:41`;
  tests assert exact contact/end positions, triangle side lengths, and feature
  offsets at `tests/test_p17_r2_direct_counter_twist.py:59` and
  `tests/test_p17_r2_direct_counter_twist.py:109`.
- `REQ-030` endpoint-only semantics are covered. The design says “Locked”
  remains colloquial endpoint wording only at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:67`,
  and tests assert no self-lock claim at
  `tests/test_p17_r2_direct_counter_twist.py:351`.

## Mechanism critique

- Fixed members: The purple axle and inner guide system remain stationary in the
  evidence. The source sets the D10-R2 rotation datum and fixed axle at
  `src/xt60_bend_jig/p17_r2_direct_counter_twist.py:179`, while sidecar tests
  assert the fixed axle, both inner guides, and keepers are not animated at
  `tests/test_p17_r2_direct_counter_twist.py:300`; occurrence evidence checks
  `allFixedWorldInvariant` at
  `tests/test_p17_r2_direct_counter_twist.py:389`.
- Counter-rotating outers: The design requires `alpha_left=-theta` and
  `alpha_right=+theta` about `C=(3.00,12.00)` at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:94`.
  The tests verify sidecar `open_to_end`, linear `24.0 * travel`, C in sidecar,
  and opposite outer angles at `tests/test_p17_r2_direct_counter_twist.py:300`
  and `tests/test_p17_r2_direct_counter_twist.py:389`.
- Rod/contact motion: Source guide states are exact D10 rods, not a floating
  displacement proxy, and tests assert exact open/contact/end coordinates,
  contact theta `23.4331751998 deg`, endpoint `24 deg`, and linear law at
  `tests/test_p17_r2_direct_counter_twist.py:59`. Contact at `4.15 mm` and END
  at `3.90 mm` are digital geometry/preload proxies only.
- C=(3,12) repair: The design records why the old datum lost local reaction
  material and why the selected rounded datum restores a continuous `+0.30 mm`
  two-sided strip without changing rods, workpiece, angle, envelopes, axle, or
  part count at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:110`.
  Tests independently require 65 samples, exact contact, all normal sides
  supported, all slot ends closed, continuous strip rows, and no partial support
  recession at `tests/test_p17_r2_direct_counter_twist.py:170`.
- Rail coherence: The replacement for the old crossing-sine threshold is
  mechanically defensible for the exact coupled topology. The diagnostic
  crossing sine is still reported, while the pass gate now checks rail
  reconstruction, nonzero derivatives, monotonic fixed-track progress,
  one-to-one/no-self-intersection branches, continuation, rank 3, and bounded
  conditioning. Evidence is in DESIGN at
  `docs/iterations/p17-r2-head-up-tail-right-orientation-repair/DESIGN.md:167`
  and tests at `tests/test_p17_r2_direct_counter_twist.py:145` and
  `tests/test_p17_r2_direct_counter_twist.py:209`.
- No added mechanism: Production label tests reject `grip_block`,
  `stability_bar`, `yoke`, `linkage`, `gear`, `lock_nose`, and `receiver`, while
  requiring three rods, six permanent caps, two fixed inner guides, two outer
  guides, and two keepers at `tests/test_p17_r2_direct_counter_twist.py:272`.
- Service path and central clearance: The service test includes XT60 body, two
  solder joints, two bent wires, 16 production solids, at least 1001 samples per
  segment, zero intersection, and `>=0.75 mm` BREP clearance at
  `tests/test_p17_r2_direct_counter_twist.py:362`.
- Rods/caps/stack: Tests require physical/model target `50.0 mm` rods, six caps,
  `32.0 mm` principal stack, `8.70 mm` engagement per side, blind cap length at
  least `9.05 mm`, and cap/plate/keeper intersection under tolerance at
  `tests/test_p17_r2_direct_counter_twist.py:241`. This supports the digital
  assembly intent but not actual press-fit retention.
- Right larger force plate: Constants/tests retain `80/82/85 mm` hierarchy and
  `right_primary_extra_lever_radius == 1.50` at
  `tests/test_p17_r2_direct_counter_twist.py:41` and
  `tests/test_p17_r2_direct_counter_twist.py:264`.

## Commands and results

- `shasum -a 256 /tmp/p17-i08-independent-gate-manifest.txt`:
  `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`
- Python manifest verifier over all 30 rows: `failures 0`.
- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`:
  `19 passed`.
- Targeted source/provenance probe:
  source hash `6b9004c7fb7d102c320c1c4184a78bbfc717540a91e5ea4f03b5a1fe1637e49b`;
  tests hash `b713552b6b5fdefe7259d67b3dde1d464e46be85702a85f926cfd055bdb88c99`;
  `C=(3.0,12.0)`, `A=(-29.0,17.0)`, `theta=24.0`,
  `rod_len=50.0`, contact offsets all `4.15`, END offsets all `3.90`,
  max rail residual `5.687116766346677e-15`, max axle residual
  `7.105427357601002e-15`, minimum outer cutter gaps
  `3.630989824536459 / 5.884373740993324`, minimum fixed gap
  `6.103048327204938`, maximum condition number `12.82163283054513`.
- A follow-up ad hoc support/motion probe was interrupted after exceeding the
  bounded review window inside repeated build123d boolean intersections. This is
  not counted as a failure because the focused pytest run completed the same
  actual-solid support/motion/service/cap gates successfully.
- Visual inspection: accepted OPEN/contact/END/opposite PNGs and GIF were
  inspected. The OPEN image shows the requested head-up/tail-right `└` and
  upper-left plus upper-right/lower-right vertical rod layout; contact/END retain
  the intended straight/arc/straight and diagonal topology; opposite view shows
  four principal plates, fixed axle/keepers, larger right plate, three rods, six
  caps, and no visible yoke/bar/link/lock receiver.

## Unresolved physical risks

- PETG print tolerance, guide wear, rod wobble under hand load, cap retention,
  keeper press fit, insulation damage, bend springback, heated-wire behavior,
  and actual 90-degree cooled bend are not proven by this gate.
- The digital `0.25 mm` END overtravel is a geometric preload proxy, not proof of
  force or holding torque.
- The cap coupon is required before treating permanent caps as physically
  accepted.

## Disposition

P17-C08 critic gate: pass / no blocker for I08-R2 digital candidate. Proceed to
the next independent validation/review step. Do not route as physical acceptance.

## P17-R08 final formal review

Status: ACCEPT for the exact P17-I08-R2 immutable candidate fingerprint
`f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5` for CAD
source, written STEP/export evidence, and the frozen static visual/motion
packet. Physical manufacture and printed operation are not accepted.

Owner/role: `P17-R08`, distinct formal reviewer and acceptance-boundary
arbiter. This role did not design, implement, critique, validate, repair,
regenerate artifacts, mutate Viewer state, or change git/continuity records.

### Provenance and candidate identity

- Branch/commit verified before formal join:
  `codex/xt60-p17-r2-orientation-repair` at
  `d7fefd8323b2a41394001cf69da774842d239197`.
- Formal review input file:
  `projects/xt60-bend-jig/docs/iterations/p17-r2-head-up-tail-right-orientation-repair/FORMAL_REVIEW_INPUT.sha256`,
  SHA-256
  `3ed77df36dfb274cf32b6077592312526e2346482afe437962e5f371c43e515c`;
  all `3` listed entries matched.
- Nested independent gate manifest:
  `/tmp/p17-i08-independent-gate-manifest.txt`, SHA-256
  `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`;
  all `30` entries matched.
- Joined C08 receipt: this `REVIEW.md` pre-formal SHA-256
  `46d8979a4617e87281521813973777ccdec0d2c6f9a0ab92064ee55a2b7a5e8f`,
  `P17-C08` PASS/no blocker on the same exact fingerprint.
- Joined V08 receipt: `VALIDATION.md` SHA-256
  `00ecd2fe6d65aae19397497b057adbd5f37f9d300b39a6469ae97f270c530985`,
  `P17-V08` PASS on the same exact fingerprint.
- Source SHA-256:
  `6b9004c7fb7d102c320c1c4184a78bbfc717540a91e5ea4f03b5a1fe1637e49b`.
- Test SHA-256:
  `b713552b6b5fdefe7259d67b3dde1d464e46be85702a85f926cfd055bdb88c99`.
- Candidate records matched V08: artifact provenance
  `97dccfad274fd82724f06c8e1ec15cd4ccc25659b6aa652dca7b8b9ecefb6b4b`,
  candidate manifest
  `0eaa98ffdc26baea5f409867929ffb9df317030bfa902cf20cd2b770919deb25`,
  candidate-fingerprint JSON
  `2b84cf88b9079edd8766a03d3fa9fe9fb251b6b1afeed7647124061f157a2fe5`,
  and fingerprint text
  `74a8c72100949170e05f3eba71d63d3a92049892a995b044ef9d4ae952b7d255`.

### Requirement coverage joined

- `REQ-027`: ACCEPT digitally. The workpiece-relative front frame is preserved:
  `+Z` is XT60 mating head/up and `+Y` is solder-tail/both-wires/right; this is
  not a camera-pose reinterpretation.
- `REQ-028`: ACCEPT digitally. OPEN topology is upper-left, upper-right, and
  lower-right, with the upper-right/lower-right rods on the exact right
  vertical leg and fixed-inner guides stationary.
- `REQ-029`: ACCEPT digitally. CLAMPED/END topology converges
  upper-left -> middle -> lower-right on one diagonal three-point wire wrap,
  with contact and END offset evidence accepted by V08.
- `REQ-030`: ACCEPT digitally as endpoint-only semantics. `locked` remains
  compatibility/colloquial wording only; no hard-stop, retention, detent,
  over-center, physical holding, or self-lock claim is accepted.

### Evidence boundaries

- CAD/source and prescribed motion: ACCEPT for exact fingerprint only. V08
  independently recomputed D10-R2 math, actual-solid support/motion/contact,
  service path, cap/stock closure, and endpoint-conditioning gates; focused
  tests passed `19/19`.
- Written STEP/export: ACCEPT for the `10` manifest-frozen written STEP exports
  and source/import parity recorded by V08. V08 isolated each STEP byte stream
  before inspection to avoid same-stem `.step.py` resolution.
- Static visual/motion packet: ACCEPT. R08 inspected the critical OPEN,
  contact, END front, and END opposite PNGs named in V08; they show the true
  `└` workpiece, head-up/tail-right orientation, OPEN right vertical rod pair,
  contact/END diagonal wrap, four plates, fixed eccentric purple axle/keepers,
  larger right force plate, three rods/six caps, and no added yoke/bar/link/
  lock receiver. R08 also inspected the GIF metadata and sampled frame
  differences: SHA-256
  `461aeb86ae7aa1212e8cccee129e70f4f2fcb0f8cfd3ccf7e24a9d35bc4dd11c`,
  `72` frames, `900 x 650`, and non-empty differences across V08's sampled
  frame indices.
- Viewer/live/browser interaction: NOT part of this R08 acceptance. This review
  did not mutate Viewer state and does not claim a live slider/browser gate.
- Physical acceptance: NOT TESTED and NOT ACCEPTED. PETG print tolerance, guide
  wear, rod wobble under hand load, cap/coupon retention, keeper press fit,
  insulation marking/damage, hand torque, holding force, soldering heat,
  PETG stiffness/creep/wear, vibration, bend springback, cooled 90-degree bend,
  endpoint holding, self-lock, slicer/3MF, and assembled operation remain
  physical/manufacturing gates.

### Finding severities

- Blockers: none.
- Majors: none.
- Minors/nonblocking:
  1. C08 endpoint terminology ambiguity remains nonblocking because tests and
     manifest keep `locked` bounded to endpoint/preload proxy semantics with
     `selfLockClaimed: False`.
  2. Contact and END front snapshots are visually close because END is only
     `0.25 mm` of additional geometric overtravel after contact; numeric
     evidence is the acceptance authority for that distinction.
  3. C08 text cites candidate records under `docs/provenance/...`, but the
     frozen manifest and actual files are under
     `cad/p17_r2_direct_counter_twist/`. This is a citation/path slip, not a
     candidate mismatch, because the manifest and V08 hashes bind the
     authoritative files used for this formal join.

### Commands and read-only results

```text
git rev-parse --abbrev-ref HEAD
  -> codex/xt60-p17-r2-orientation-repair
git rev-parse HEAD
  -> d7fefd8323b2a41394001cf69da774842d239197
shasum -a 256 FORMAL_REVIEW_INPUT.sha256
  -> 3ed77df36dfb274cf32b6077592312526e2346482afe437962e5f371c43e515c
Python manifest verifier over FORMAL_REVIEW_INPUT.sha256
  -> 3/3 entries OK
shasum -a 256 /tmp/p17-i08-independent-gate-manifest.txt
  -> f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5
Python manifest verifier over /tmp/p17-i08-independent-gate-manifest.txt
  -> 30/30 entries OK
shasum -a 256 REVIEW.md before append
  -> 46d8979a4617e87281521813973777ccdec0d2c6f9a0ab92064ee55a2b7a5e8f
shasum -a 256 VALIDATION.md
  -> 00ecd2fe6d65aae19397497b057adbd5f37f9d300b39a6469ae97f270c530985
PIL GIF probe on p17_r2_i08_full_motion_20260825T123129Z.gif
  -> 72 frames, 900 x 650, non-empty sampled frame differences
```

### Final disposition and next action

Formal gate disposition: ACCEPT the unchanged P17-I08-R2 digital candidate for
delivery/continuity as CAD source, prescribed motion, written STEP/export
evidence, and frozen static visual/motion evidence. Any candidate-input change
invalidates C08, V08, and this R08 join. Next action is coordinating-owner
continuity/delivery update, followed by generating/slicing only the approved
print package and running the documented physical fit and operation checks.
