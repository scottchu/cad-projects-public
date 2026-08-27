# XT60 bend jig project state

Last updated: `2026-08-26`

## Active forward design gate

- Active iteration: `p20-r2-fixed-rod-arc-rail`.
- The user has approved the complete P19-based P20 R2 assembly's fixed purple
  rod and both curved fixed-rod rails. Their exact source/STEP fingerprints,
  `C=(0,0)`, `A=(-15,-11)`, physical left/right `+45/-45 deg`, local rail
  endpoints, `7.90 mm` cutters, and zero white-rod outer rails are frozen and
  may not change in the next task.
- Acceptance is split: fixed-rod/rail/complete-assembly presence is
  **USER-APPROVED**, while the inherited P19 END-derived diagonal wire is
  **USER-REJECTED**. The next bounded task corrects only the wire to an exact
  vertical leg + tangent R6 quarter arc + exact horizontal leg.
- The diagonal escaped because P19 `build_workpiece_reference()` and its tests
  encoded the same contradictory diagonal assumption instead of testing core
  `REQ-002`/`REQ-017` 90-degree topology.
- The user rejected the P20 R1 scaffold because it replaced the required
  curved fixed-rod rotation rails with round journals and effectively rotated
  the outer plates about the fixed axle. P20 R1 remains immutable rejected
  history; its source, artifacts, and scaffold-conformance evidence are not
  rewritten.
- P20 R2 restarts from exact P19 product baseline `b69b6ad...`, preserves P19
  outer virtual center `C=(0,0)`, keeps the axle/inner plates world-fixed,
  moves the axle to candidate `A=(-15,-11)`, and derives one true curved
  inverse-frame fixed-axle rail in each outer plate through physical
  left/right `+45/-45 deg`.
- All six white-rod outer rails remain absent and all six inner-plate rail cuts
  remain. The six resulting white-rod/solid-outer-plate collisions are a known,
  visible non-product boundary, not a reason to add substitute holes.
- Future white-rod outer rails will be added one at a time in separate
  contracts because each couples to its inner path and neighboring outer rails.
- Authority: `docs/iterations/p20-r2-fixed-rod-arc-rail/`.

## Rejected P20 R1 history

- Prior iteration: `p20-r1-fixed-rod-reset`.
- The user rejected P19 as the forward product direction because the outer
  rod rails overlap too much with the fixed-inner rails and the fixed-rod
  arrangement lacks effective rotation.
- P20 R1 starts from the exact merged P19 fingerprint, removes all six outer
  rod rails, moves the fixed stepped axle farther lower-left, changes the two
  outer plates to `-45/+45 deg`, and rederives their two fixed-axle guides.
- The numeric FRONT-YZ design gate and independent critique remain immutable
  blocked product-candidate evidence. They prove centered-equivalent
  `-45/+45 deg` motion about `A=(-15,-11)` and six unavoidable rod/solid-
  outer-plate collisions when all outer apertures are absent.
- The user has now authorized that exact collision state as a deliberate
  sequential **evidence-only scaffold**. No clearance holes are allowed now;
  the three outer rails may be added back only one at a time in future,
  separately authorized iterations.
- The exact sequential scaffold is implemented and formally accepted for
  **scaffold conformance only**. It remains explicitly non-candidate and
  cannot be called a complete movable assembly, manufacturable part, or
  physically accepted mechanism.
- P19 remains the prior accepted digital evidence baseline and is superseded
  only for forward design; its history and acceptance record are not erased.
- Authority: `docs/iterations/p20-r1-fixed-rod-reset/`.

## P20 scaffold conformance evidence

- Frozen candidate manifest SHA-256:
  `59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`,
  verified `20/20`.
- Fixed axle datum `A=(-15,-11)`; outer travel is `-45/+45 deg`, exactly
  `90 deg` relative, with one centered constant axle journal per outer plate.
- Outer rod rails and substitute rod apertures are exactly zero. All six
  expected OPEN rod/solid-outer-plate collisions remain present and total
  `241.2743157956962 mm3`; the unexpected collision map is empty.
- Focused P20 tests pass `8/8`; combined P19+P20 regression passes `16/16`.
  Four written STEP artifacts validate and match their generators.
- Independent critic recheck SHA-256:
  `6531dea20ed5d4d744259f5c6a4c8896d2c0ec929ff47395a5757f0282d10819`.
- Independent validator recheck SHA-256:
  `73312ac348745ce6a1a513283e752094bc826f1effcda028961f43d3b23a10b0`.
- Formal scaffold review SHA-256:
  `3f57e45432591b13ed7fcc71011185534c18107f099ac251b93c5dc6ee131130`;
  verdict `ACCEPT` for scaffold conformance only.

## Current accepted digital candidate

- Project: `projects/xt60-bend-jig`.
- Prior accepted iteration: `p19-r1-front-edge-short-tail`.
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

Open a wire-only correction from P20 R2 source SHA-256
`1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73`
and complete-assembly STEP SHA-256
`715851b434ab2e17a7f6c29be0b21924fb99ed6e28c20be8b276399a5d1d6bca`.
Replace only the diagonal wire reference with the exact vertical + R6 quarter
arc + horizontal topology and add requirement-level regression. Never alter
the fixed purple rod, either curved rail, their paths/cutters, `C`, `A`, motion
signs, or zero white-rod outer-rail count.
