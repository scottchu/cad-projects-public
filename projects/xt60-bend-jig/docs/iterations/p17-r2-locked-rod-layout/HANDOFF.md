# P17-D13 locked rod-layout handoff

Status: **STOP — EXACT REVIEW CANDIDATE MATERIALIZED; PRODUCT/MERGE BLOCKED**.

## Verified baseline identity

- Repository/branch/HEAD:
  `/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects`,
  `codex/xt60-p17-r2-locked-rod-layout`,
  `8adfb20f352e36cede54a3414307ced3de81c2b8`.
- I10-R1 manifest file SHA/fingerprint:
  `5443e39e3b82bbbc2f6e3ed8dd6c2487a69035c263d44128a47f31ddab509d93`.
- Baseline-owner I10 source/test receipt:
  `0d66dd9b0668c976750036c03bb8b8886a04df2d557ddee4330e933072161060`
  / `e1806f15ffb5b92afcd92f665e501ed58632bddfc991733d0224c431f2286895`.

## Frozen result

The exact user-locked delta is `(+16.1869657526,+10.2949747468)` on all rod
states, three inner tracks and six derived outer rails. `A=(-29,12)` and
`C=(3,12)`. I10 XT60/body/wire/service coordinates remain fixed.

END rod centers are `(5.7869657526,19.7949747468)`,
`(14.2020415121,12.3100505063)`, and
`(21.6869657526,3.8949747468)`; centroid Z is `11.99999999997`.

All six inverse rails are mathematically constructible. Minimum analytic web
is `3.632336547 mm` and minimum boundary web is `3.294595306 mm`, both above
`2.20 mm`.

## Blocking findings

- Bottom OPEN rod center is inside the frozen XT60 body rectangle; OD4 signed
  clearance is `-2.000 mm`. This loads/intersects the plastic body.
- Bottom OPEN is only `1.7016843784 mm` from the vertical-wire centerline,
  giving `2.4483156216 mm` nominal rod/wire radial overlap.
- END bottom and upright wire surface gaps are `8.136965753 mm` and
  `2.244974747 mm`; the forming/contact endpoint no longer exists.
- Full rail ratios are bottom `1.859285`, diagonal `1.605235`, upright
  `3.071372`; contact ratios are `1.876587`, `1.750768`, `4.243331`; minimum
  contact crossing angle is `4.387453 deg`.

The body/wire collisions and lost END contact are hard analytic failures, not
missing polish or Viewer evidence. Rail ratios/angles are a separate
force/path-balance diagnostic rather than physical-force proof. D13 was
materialized exactly as a bounded review artifact after this design stop; do
not treat that evidence materialization as product acceptance, and do not
change any locked coordinate on behalf of the user.

## I13/C13/V13/R13 evidence

- Exact immutable candidate fingerprint:
  `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`
  (`21/21` payload entries pre/post independent review).
- Implementation: 22/22 focused tests; ten STEP writes/current checks,
  validate, refs and source/export parity; four PNGs and a 72-frame moving GIF.
- C13: faithful implementation, product BLOCK.
- V13: fidelity PASS; 14 focused tests, independent math/conditioning, ten
  STEP validate/refs/parity and RGB motion checks PASS; product BLOCK.
- R13: formal ACCEPT only for bounded fidelity/export/static-motion/Viewer
  transport evidence; formal REJECT for product, mechanical, physical, PR
  merge, release, slicing and printing.
- Persistent review URL:
  `https://mac-mini.duckbill-ionian.ts.net/Users/scottchu/.codex/worktrees/a373f6e6-90f4-4c0e-857b-643add242937/design-projects?file=projects%2Fxt60-bend-jig%2Fcad%2Fp17_r2_direct_counter_twist%2Fp17_r2_full_motion.step.py`.
- Local and Tailscale page/artifact/assets returned HTTP `200`; artifact state
  was `ready`. In-app browser/live slider manipulation was unavailable and is
  not accepted.

## Next action

Ask for one explicit scope choice: preserve the locked END centroid/triangle
while reopening the common XY placement, or preserve the frozen workpiece
interface and abandon this rod-only delta. A superseding design amendment must
restore zero XT60 collision, meaningful wire contact and acceptable rail
balance before a new implementation candidate can start. Do not merge I13.

Physical fit, retention, wear, wobble, hand force, wire damage, heat,
springback, endpoint retention and self-lock remain untested.
