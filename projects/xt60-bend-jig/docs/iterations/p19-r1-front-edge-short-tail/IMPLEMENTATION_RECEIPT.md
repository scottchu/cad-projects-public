# P19-IMPL-05 repaired implementation receipt

## Status and provenance

- Role owner: `P19-IMPL-05`, implementation only.
- Status: repaired candidate implemented and locally verified; independent validation and formal review remain required.
- Baseline commit: `bcc16305ff112ba814bdf19ad544a5819127e902`.
- Frozen repair input: `REPAIR2_IMPLEMENTATION_INPUT.sha256`, SHA-256 `2493c6f2591b52b615b4e4f18be2021e7c991dbcf3f300eb944a6638f8f8bef3`, verified 7/7 before implementation.
- Repaired design contract: `REOPTIMIZED_4MM_OPEN_UPRIGHT_DESIGN.md`, SHA-256 `36e346c45f6b241e834da8d2dcc9009823bbf85809044021b42e8a33e1f393d4`.
- Repaired critique: `REOPTIMIZED_4MM_OPEN_UPRIGHT_CRITIQUE.md`, SHA-256 `2ee1782bc64805522263bcb09e017ccce1e296a2ef507266ed0592be860b2248`.
- Candidate manifest: `IMPLEMENTATION_CANDIDATE.sha256`, SHA-256 `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`, verified 20/20.

## Exact repaired candidate fingerprint

- `theta_end = 5 deg`; shared normalized motion `u`; `alpha_left = -5u deg`; `alpha_right = +5u deg`.
- Rotation center `C = (Y=0, Z=0)`; fixed stepped axle `A = (Y=-13, Z=-9)`.
- OPEN: bottom `(5,10)`, diagonal `(20.4,10)`, upright `(20.4,-9.172814225900)`.
- END common delta: `(+1.552212035894,-0.977677650052)`.
- END: bottom `(9.552212035894,8.022322349948)`, diagonal `(15.802212035894,2.272322349948)`, upright `(22.052212035894,-3.477677650052)`.
- Plate ODs: inner `54.4`, left outer `54.7`, right outer `55.0` mm.
- Three `OD4 x 50 mm` stainless rods, six permanent caps, `OD4.15` moving tracks.
- OPEN wire line point `(12.192732506095444,10.892453295819136)` and unchanged unit direction `(0.7359310117618296,-0.6770565308208832)`.
- One pure `motion_state(u)` drives every rod, plate occurrence, export and Viewer sidecar. Both outer rails use the shared inverse-frame derivation; no manual rail extension exists.

## Focused repair

- Product geometry, identities and motion remain exactly the accepted repaired design.
- Completed-pigtail service evidence now transforms the XT60 body, two finite solder joints and two finite bent-wire solids separately.
- Evidence aggregates every pigtail-feature/production-solid pair and reports its limiting pose, distance and intersection instead of using a compound distance that could hide an individual collision.
- Deterministic bounded search produced the four-pose practical upward withdrawal path `(dy,dz,phiDeg)`:
  - `(0,0,0)`
  - `(-8,10,-5)`
  - `(-16,26,-10)`
  - `(-16,50,-10)`
- The old blocked validator case is a permanent regression: at rejected pose `(-4,26.84,-15)`, the two bent-wire/diagonal-rod intersections are `47.25940252956725` and `47.25940236750162 mm3` and may not be hidden by compound aggregation again.

## Changed implementation namespace

- `src/xt60_bend_jig/p19_r1_front_edge_short_tail.py`
- `tests/test_p19_r1_front_edge_short_tail.py`
- `cad/p19_r1_front_edge_short_tail/` written STEP artifacts and full-motion sidecar
- `docs/review/p19-r1-front-edge-short-tail/p19-r1-impl05-*.png`
- This receipt and `IMPLEMENTATION_CANDIDATE.sha256`

P17/P18 source, tests, CAD artifacts and continuity files were not edited. No Viewer, 3MF, slicing, printing or Git operation was performed.

## Commands and results

All commands ran from the repository root using the root `.venv` interpreter.

1. `python -m pytest -q projects/xt60-bend-jig/tests/test_p19_r1_front_edge_short_tail.py`
   - PASS, 8/8 focused tests.
   - Includes exact contract/candidate, pure shared motion, 65-state inverse equivalence, exact six rail travels, OPEN/END topology, conditioning, actual BREP collision/web/service/support/cap gates, pairwise completed-pigtail removal, the exact `47.2594024 mm3` defect regression, sidecar scope and entrypoints.
2. Direct pairwise removal evidence.
   - PASS, 123 actual-BREP service states and 3003 dense analytic states.
   - Minimum clearance `0.7499999999996647 mm`; BREP minimum `0.7499999999996648 mm`; maximum intersection `0 mm3`.
   - Limiting pair is `bentWire0::diagonalRod` at seated OPEN, as intended by the exact 0.75 mm interface constraint.
3. `scripts/gen` with all six explicit P19 generators and `--write`.
   - PASS; regenerated OPEN, CONTACT, END, EXPLODED, PRINT_KIT and FULL_MOTION STEP artifacts.
4. `scripts/inspect refs ... --facts --planes --positioning` on all six generator entries.
   - PASS for all six.
   - OPEN/CONTACT/END: `1515 faces / 4359 edges`; EXPLODED `1485/4311`; PRINT_KIT `1476/4302`; FULL_MOTION `1497/4329`.
5. `scripts/inspect validate` on all six written STEP files.
   - PASS; all solids are valid, closed and positive volume.
   - Occurrences: OPEN `22`, CONTACT `22`, END `22`, EXPLODED `16`, PRINT_KIT `13`, FULL_MOTION `18`.
6. `scripts/inspect diff <generator> <written STEP> --planes` on all six pairs.
   - PASS for every pair: `topologyChanged=False`, `geometryChanged=False`, `bboxChanged=False`, `kindChanged=False`.
7. `scripts/snapshot` on written OPEN, END and EXPLODED STEP.
   - PASS without warnings; right/+X OPEN, right/+X END and exploded ISO PNGs were visually inspected by implementer and root.

## Deterministic and BREP evidence

- Inverse-derived outer rail centerline travels, mm:
  - left upright `7.864158836934`
  - left bottom `4.000000000000`
  - left diagonal `8.012433561031`
  - right upright `4.000000000000`
  - right bottom `5.944910143797`
  - right diagonal `10.157688045826`
- Both active minimum rails satisfy the exact 4 mm requirement within numeric tolerance.
- Minimum actual rail/web: `2.405845086139 mm` against `2.20 mm` requirement.
- Constraint system rank `3`; worst condition number `13.007686517253` against limit `15`.
- OPEN wire surface clearances, mm: upright `5.059868571589`, bottom `1.376670574642`, diagonal `0.749999999999666`.
- END wire surface gap for all three rods: `-0.25 mm` geometric preload proxy.
- 65-state actual-solid sweep, two-sided support, cap closure and fixed-occurrence gates pass.
- Full `8 x 8 mm` solder-tool keepout begins exactly `0.75 mm` outside the OD55 rim; production/tool BREP intersection is zero.

## Visual inspection

- OPEN right/+X: OPEN triangle remains at the +Y/right service edge; purple fixed axle remains left/behind; short-tail XT60 wire/tool references exit +Y/right.
- END right/+X: the three rods reach the accepted shared collinear clamp endpoint without an identity swap.
- Exploded ISO: four plates, stepped axle, keepers, three rods and six caps are separate and present; no extra yoke, linkage, gear or floating rod appears.

## Unresolved physical risks

- The two 4 mm rail travels and the 0.75 mm OPEN diagonal-wire clearance are active constraints, not generous margins.
- CAD does not establish hand force, self-lock, friction, backlash, heat response, PETG wear, cap retention, printed clearances, stainless-stock tolerance, ESC-tail ergonomics or physical clamp force.
- No 3MF, slicing, printing or physical acceptance was performed.

## Next action

Freeze `IMPLEMENTATION_CANDIDATE.sha256` as the sole repaired candidate input for independent critique, validation and formal review. Implementation self-check is not independent acceptance.
