# XT60 bend jig project state

Last updated: `2026-08-26`

## Current accepted digital candidate

- Project: `projects/xt60-bend-jig`.
- Active iteration: `p19-r1-front-edge-short-tail`.
- P19 R1 is formally accepted for parametric CAD, the six written STEP
  artifacts, and exact-artifact Viewer handoff only.
- Candidate manifest:
  `docs/iterations/p19-r1-front-edge-short-tail/IMPLEMENTATION_CANDIDATE.sha256`.
- Candidate-manifest SHA-256:
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- The manifest verifies `20/20` exact design, source, test, generator, STEP,
  sidecar, and snapshot files.
- P18 R1 remains the prior accepted baseline and P17 remains immutable
  history; neither was modified by P19.

## P19 R1 mechanism

- Physical FRONT is YZ: `+Z` is XT60 mating-head/up and `+Y` is the short
  ESC tail, solder-tool approach, right/outward direction.
- Three purchased rods remain uncut `OD4.00 x 50.00 mm` stainless stock with
  six permanent caps.
- OPEN ordered rods are bottom `(5,10)`, diagonal `(20.4,10)`, and upright
  `(20.4,-9.172814225900) mm`: an exact right angle.
- END ordered rods are `(9.552212035894,8.022322349948)`,
  `(15.802212035894,2.272322349948)`, and
  `(22.052212035894,-3.477677650052) mm`: one exact equal-pitch diagonal.
- One shared normalized state drives both sides:
  `alpha_left=-5u`, `alpha_right=+5u`. Both inner plates and the real purple
  stepped X-axis axle remain fixed; only the two outer plates counter-rotate.
- Virtual outer rotation datum is `C=(0,0)`. The one-piece fixed axle remains
  left/behind at `A=(-13,-9)` through all four plates.
- Plate ODs are inner `54.40`, left outer `54.70`, and right force outer
  `55.00 mm`; rod rail cutters are `OD4.15 mm`.
- All six outer rod rails are exact inverse transforms of the same world rod
  paths. Their center travels are left `4.000000/8.012434/7.864159 mm` and
  right `5.944910/10.157688/4.000000 mm`; no rail was hand-extended.
- No lock, stability bar, yoke, gear, linkage, grip block, or self-lock claim
  was added.

## Independent evidence

- 2D optimizer design SHA-256:
  `36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4`.
- Independent analytic critique SHA-256:
  `2ee1782bc64805522263bcb09e017ccce1e296a2ef507266ed0592be860b2248`.
- Implementation receipt SHA-256:
  `72bd3b928e8733af79457d92f9c4f738c0f3e62600d7e39324f0f6339371d73f`.
- Independent validation SHA-256:
  `304239aecb3b939a6ef1412d1b31979b4bafda2b2e997ca7e7311b36adfb88ef`.
- Formal review SHA-256:
  `7b5436c57070547b14241bc3de6cbc7047c07cbd1e4070b036f0d8d51040aba3`.
- Focused source regression: `8/8` passed.
- Shared-state reconstruction mismatch is below `8e-15 mm`; identities do
  not swap and left/right use the same complete motion state.
- OPEN wire surface clearances are
  `1.376671/0.750000/5.059869 mm`; END preload proxy is `0.25 mm`.
- Actual minimum plate web is `2.405845 mm`; contact closure retains rank `3`
  and maximum normalized condition `13.007687 <= 15`.
- The 65-state hardware-inclusive actual-solid sweep has zero unintended and
  pre-contact intersection.
- Completed-pigtail removal uses the verified rigid sequence
  `(0,0,0) -> (-8,10,-5 deg) -> (-16,26,-10 deg) -> (-16,50,-10 deg)`.
  Across `123` pairwise BREP and `3003` analytic states, minimum clearance is
  `0.749999999999665 mm` and maximum intersection is zero. The former
  `47.2594024 mm3` diagonal-rod collision is retained as a passing regression.
- All six written STEP artifacts pass independent validate, refs, and
  source/export diff with zero topology, geometry, bounds, size, or center
  delta: OPEN/contact/END `22/22`, exploded `16/16`, print kit `13/13`, and
  full motion `18/18` valid closed positive-volume occurrences.

## Viewer delivery

- Exact P19 page:
  `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp19_r1_front_edge_short_tail%2Fp19_r1_full_motion.step.py`.
- Local and Tailscale page probes return HTTP `200`; exact artifact status is
  `ready`; the assembly descriptor and a generated component GLB return HTTP
  `200`.
- The app browser-control connection was unavailable, so live slider/UI
  manipulation was not independently exercised. Exact snapshots were
  inspected at original resolution and Viewer transport/readiness is accepted
  separately from human interactive review.

## Acceptance boundary

- Accepted: parametric source, deterministic motion/rail math, production CAD
  solids, six STEP exports, frozen snapshots, and Viewer readiness for the
  exact candidate fingerprint.
- The `0.75 mm` removal clearance and two `4.00 mm` rail travels are active
  nominal equalities with effectively no extra manufacturing margin.
- Still physical only: upright tangent-state hand force, friction, wedging,
  backlash, real solder ergonomics, PETG fit/tolerance, cap and keeper
  retention, axle fit, wobble, heat, wear, back-drive, and self-lock behavior.
- No mesh, 3MF, DfAM, slicing, printing, or physical acceptance was performed
  or authorized in this implementation task.

## Authoritative paths

- Source: `src/xt60_bend_jig/p19_r1_front_edge_short_tail.py`.
- Focused tests: `tests/test_p19_r1_front_edge_short_tail.py`.
- CAD/STEP/sidecar: `cad/p19_r1_front_edge_short_tail/`.
- Evidence and handoff:
  `docs/iterations/p19-r1-front-edge-short-tail/`.
- Review media: `docs/review/p19-r1-front-edge-short-tail/`.

## Next action

The exact accepted fingerprint is delivered in GitHub PR
`https://github.com/scottchu/design-projects/pull/11`. After merge, the next
product action is human Viewer review and then a separately authorized
prototype/physical test plan. Do not silently add margin, change topology,
produce 3MF, slice, or print.

## Printing-profile addendum — 2026-08-31

[PRINTING_PROFILE.md](PRINTING_PROFILE.md) holds editable P19 process fields and
manufacturing concerns. Historical coupon evidence is not P19 print authority.
See the [repository-policy handoff](../../docs/iterations/2026-08-31-printing-profiles/HANDOFF.md) for independent status.
P19 CURRENT, frozen contract/fingerprint and CAD/STEP/physical acceptance remain
unchanged; this is not a new product baseline or permission to print.
