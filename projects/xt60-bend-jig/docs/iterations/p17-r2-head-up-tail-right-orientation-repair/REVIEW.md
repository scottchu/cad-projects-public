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
