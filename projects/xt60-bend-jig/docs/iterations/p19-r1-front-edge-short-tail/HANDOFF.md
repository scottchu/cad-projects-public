# P19 R1 front-edge short-tail handoff

Date: `2026-08-26`

## Status

P19 R1 is complete and independently accepted for parametric CAD, the six
written STEP artifacts, and exact-artifact Viewer handoff only. It is not a
physical acceptance and does not authorize 3MF, slicing, or printing.

## Frozen authority chain

- Baseline commit: `bcc16305ff112ba814bdf19ad544a5819127e902`.
- Candidate manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`
  (`20/20` entries verified).
- Repaired 2D design SHA-256:
  `36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4`.
- Independent 2D critique SHA-256:
  `2ee1782bc64805522263bcb09e017ccce1e296a2ef507266ed0592be860b2248`.
- Implementation receipt SHA-256:
  `72bd3b928e8733af79457d92f9c4f738c0f3e62600d7e39324f0f6339371d73f`.
- Independent validation SHA-256:
  `304239aecb3b939a6ef1412d1b31979b4bafda2b2e997ca7e7311b36adfb88ef`.
- Formal review SHA-256:
  `7b5436c57070547b14241bc3de6cbc7047c07cbd1e4070b036f0d8d51040aba3`.

## Verified result

- Focused tests: `8/8` passed.
- One shared `u` drives equal-magnitude opposite outer rotation; rods retain
  identity and both sides reconstruct the same physical state.
- Six exact inverse rails are at least `4.00 mm`; no manual extension.
- Minimum actual web is `2.405845 mm`; closure rank is `3`; maximum normalized
  condition is `13.007687`.
- The 65-state hardware-inclusive sweep has zero unintended collision.
- The repaired four-waypoint completed-pigtail path has minimum nominal
  clearance `0.749999999999665 mm` and zero intersection across `123` pairwise
  BREP plus `3003` analytic states.
- All six STEP artifacts independently pass validate/refs/source-export diff.
- Three exact snapshots were inspected; no extra linkage, lock, yoke, gear, or
  reassigned/floating rod exists.

## Viewer

Exact review page:

`https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp19_r1_front_edge_short_tail%2Fp19_r1_full_motion.step.py`

Page HTTP, artifact `ready`, assembly descriptor, and component GLB transport
were verified locally and through the Tailscale hostname. Browser automation
was unavailable, so live slider interaction remains for human review.

## Remaining boundary

The `0.75 mm` service clearance and two `4.00 mm` rails are exact active
limits, not manufacturing margin. Physical hand force/tangency, friction,
backlash, PETG fit, caps/keepers, axle fit, solder ergonomics, heat, wear,
wobble, back-drive, and self-lock remain unverified. No 3MF, slicing, printing,
or physical acceptance is included.

## Resume action

Merge the exact candidate fingerprint through GitHub PR
`https://github.com/scottchu/design-projects/pull/11`. Any source, parameter,
STEP, sidecar, or review-artifact change reopens validation and formal review.
Do not produce print artifacts without separate authorization.

## Later printing-profile pointer — 2026-08-31

See [PRINTING_PROFILE.md](../../../PRINTING_PROFILE.md) and the separate
[repository-policy handoff](../../../../../docs/iterations/2026-08-31-printing-profiles/HANDOFF.md).
Only documentation/profile concerns were added. The P19 frozen candidate,
source/tests/artifacts and CAD/STEP verdict remain unchanged; no printing or
physical acceptance is granted.

## Later documentation-refresh addendum — 2026-09-05

PR #11 is now merged. Current-facing documentation foregrounds the focused P19
test and the installed CAD/CAD Viewer workflows, while preserving the exact P19
candidate and all digital-versus-physical acceptance boundaries. No source,
test, STEP, sidecar, review artifact, candidate hash, or CURRENT pointer changed.
