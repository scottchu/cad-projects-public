# P20-SCAFFOLD-IMPL-01 implementation receipt

Date: `2026-08-26`

## Status and provenance

- Role owner: `/root/p20_scaffold_implementer`, CAD implementation only.
- Status: **FOCUSED REPAIR 1 IMPLEMENTED AND LOCALLY VERIFIED AS AN
  EVIDENCE-ONLY, INTENTIONALLY COLLIDING, NON-CANDIDATE SCAFFOLD.** This is
  not self-approval. Independent critique, validation and formal conformance
  review must be rerun against the replacement candidate.
- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- Product baseline: P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Frozen input manifest file SHA-256:
  `74fe83b49142ff43ce9a356825d8078c27e065bd5123f6cc446f5be00bcbadd6`;
  verified `18/18` before initial implementation and repair.
- Repair input critique file SHA-256:
  `994f38fbfa5c6fc5b27029055c175ce95e56f098e5dec2c4cd08d3c88d40d203`.
- Superseded candidate manifest file SHA-256:
  `2f5c68e65a96ee3ef1d32150e283a23b06a3854905883180935f3540af60f903`;
  verified `18/18` before repair.
- Replacement candidate manifest file SHA-256:
  `59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`;
  verified `20/20` after repair.
- P20 source manifest SHA-256:
  `e51c996b5880cb1ec9b88af88bb53c1be717ee692792634974c3a60905ddbe4a`.
- Source revision SHA-256:
  `81dc74444bd7dc5c2e4e29f5ce4c8bbc9012d5a3baa6d4a29931ea369b44262a`.

## Exact implemented scaffold

- Fixed stepped-axle datum `A=(Y=-15.00,Z=-11.00) mm`.
- One normalized state `u in [0,1]` drives
  `alpha_left=-45u deg` and `alpha_right=+45u deg`; END relative travel is
  exactly `90 deg`.
- The reusable pure transform is
  `T_s(q,u)=A+R(alpha_s(u))q`, with an explicit inverse and boundary tests.
  The fixed axle is exactly `q_A=(0,0)` in both outer frames at every sampled
  state.
- Each outer plate is its frozen P19-diameter disk minus exactly one centered
  `OD7.90 mm` round journal. There are zero outer rod rails and zero substitute
  rod holes, windows, slots, pockets or bores.
- Both fixed inner plates retain all three P19 straight closed tracks. Only
  their keyed axle bore moves to `A`.
- All three `OD4 x 50 mm` rods retain their exact P19 identities and OPEN-to-END
  world paths. Six caps, plate X stack, axle/keepers, XT60/wire references,
  workpiece and the unchanged P19 static service-envelope occurrence remain.
- OPEN, mid and END each contain `19` top-level source occurrences, exactly
  matching the preserved P19 static assembly contract. The static service
  compound expands to four children in imported STEP, giving `22` leaf
  occurrences there. Full motion preserves its P19-matching `18` top-level
  occurrences.
- Every generated root/occurrence, sidecar and review medium labels the result
  as scaffold evidence or non-candidate evidence. No mechanism, product,
  print or physical acceptance is claimed.

## Focused repair 1 findings and dispositions

- `SC-01` — PASS: restored `reference_service_envelopes` by delegating to the
  unchanged P19 generator in every static state. Tests now enforce its exact
  top-level occurrence/name preservation and source/written-STEP parity.
- `SC-03` — PASS: `intersection_volume()` now fails closed. A BREP common
  failure raises named `CollisionEvaluationError` with the original exception
  chained; it can no longer turn unknown collision state into `0.0`. A fake
  failing BREP regression exercises this path.
- `SC-02` — PASS at implementation evidence level: opaque review frames and
  the moving GIF were superseded. Replacement static media use transparent
  outer plates and an in-frame label:
  `NON-CANDIDATE SCAFFOLD — EXPECTED ROD/OUTER COLLISIONS`. The contact sheet
  explicitly says the rods pass through solid plate volume, the circles are
  not holes, and the sequence is static collision evidence rather than valid
  motion.

## Expected collision truth

Actual source BREP at OPEN measures exactly the six authorized rod/solid-outer
plate intersections; none is suppressed:

| Pair | Intersection volume (`mm3`) |
|---|---:|
| `upright_rod::left_outer_plate` | `40.212385965949366` |
| `upright_rod::right_outer_plate` | `40.212385965949380` |
| `bottom_rod::left_outer_plate` | `40.212385965949350` |
| `bottom_rod::right_outer_plate` | `40.212385965949366` |
| `diagonal_rod::left_outer_plate` | `40.212385965949360` |
| `diagonal_rod::right_outer_plate` | `40.212385965949370` |
| **OPEN total** | **`241.2743157956962`** |

The same six authorized pair names are evaluated at OPEN, mid and END. Some
pairs become partial or clear as the intentionally solid eccentric disks move;
the evidence function reports those actual values rather than suppressing
them. The exhaustive scoped census found no new unexpected collision. Existing
P19 retention/reference contacts are reported separately as preserved baseline
contacts. Production solids have zero intersection with all four preserved
P19 solder-joint/tool service-envelope children at OPEN, mid and END.

## Changed implementation namespace

- `src/xt60_bend_jig/p20_r1_fixed_rod_reset_scaffold.py`
- `tests/test_p20_r1_fixed_rod_reset_scaffold.py`
- `cad/p20_r1_fixed_rod_reset_scaffold/`
  - explicit OPEN, mid, END and full-motion generators;
  - matching written STEP artifacts;
  - one full-motion parameter sidecar.
- `docs/review/p20-r1-fixed-rod-reset/scaffold/`
  - transparent OPEN/mid/END world-YZ snapshots;
  - transparent OPEN axial-stack snapshot;
  - deterministic SVG and rendered PNG collision contact sheets.
- This receipt and `SCAFFOLD_CANDIDATE.sha256`.

No P19 file, contract, critique, validation, continuity index or design record
was edited by this repair. No outer rod rail, clearance aperture, 3MF, STL,
slicing, printing, future rail order, Git commit or product/physical acceptance
was created. The old opaque PNGs and moving GIF were removed as superseded,
reproducible derived review media; they are not recoverable in-place but can be
regenerated from the frozen old candidate if ever needed.

## Exact commands and results

All Python commands ran from the repository root through the root `uv`
workspace.

1. `shasum -a 256` plus `shasum -a 256 -c` verified the critique SHA and the
   superseded candidate `18/18` before mutation.
2. `uv run pytest projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py -q`
   - PASS, `8/8`, including the restored static occurrence, exact naming,
     source/export parity and fail-closed BREP regression.
3. `uv run pytest projects/xt60-bend-jig/tests/test_p19_r1_front_edge_short_tail.py projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py -q`
   - PASS, `16/16`; no P19 regression.
4. CAD `scripts/gen --write --force` on each of the four explicit P20
   generators.
   - PASS; all four STEP artifacts and render packages were regenerated from
     the final repaired source.
5. CAD `scripts/inspect validate` on all four written STEP artifacts.
   - PASS, `0` failures. OPEN/mid/END each expose `22` imported leaf
     occurrences; full motion exposes `18`.
6. CAD `scripts/inspect refs --facts --planes --positioning` on all four.
   - PASS. OPEN/full-motion package facts are
     `50.7 x 65.1247 x 58.25 mm`; mid is
     `50.7 x 79.9423 x 83.0868 mm`; END is
     `50.7 x 93.0175 x 98.6744 mm`.
7. CAD `scripts/inspect diff <generator> <written STEP> --planes --format text`
   on all four pairs.
   - PASS for every pair: `topologyChanged=False`,
     `geometryChanged=False`, `bboxChanged=False`, `kindChanged=False`.
8. CAD `scripts/snapshot ... --display transparent` generated four replacement
   PNGs. A deterministic SVG assembled the three static YZ states with the
   required in-frame warning; macOS `qlmanage -t -s 3000` rendered the PNG
   contact sheet.
   - PASS. The final contact sheet was inspected directly at full-frame scale:
     the solid outer plates are transparent, rods visibly cross their solid
     volume, and no motion-validity implication remains.
9. Direct source evidence rerun:
   - PASS; six expected OPEN intersections total
     `241.2743157956962 mm3`, unexpected collision map `{}`, static top-level
     counts `19/19/19`, full-motion top-level count `18`.
10. `shasum -a 256 -c .../SCAFFOLD_CANDIDATE.sha256`
    - PASS, `20/20`; manifest file SHA-256 is
      `59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`.
11. Optional `uv run ruff check` remains unavailable because `ruff` is not
    installed in the frozen root environment. No environment or dependency
    was changed. Python import/collection, all `16` tests, generator execution
    and STEP generation exercised source syntax and runtime behavior.

## Artifact SHA-256

| Artifact | SHA-256 |
|---|---|
| P20 source | `81dc74444bd7dc5c2e4e29f5ce4c8bbc9012d5a3baa6d4a29931ea369b44262a` |
| P20 focused tests | `e70fc6e3e51e6fef6db78900be63d184a7794893bd2c7577c1a95631faa0b67c` |
| OPEN STEP | `ab87e7845b1dc62096fdff60e5bdb80adaed731d14d7c6ee3f14925fd0b3df46` |
| mid STEP | `597cf193d9db4fb649176b60e20224907ac3941e2ca8cdeaa1c4f17d4d47801e` |
| END STEP | `f4cff03091838057ea9202e64e4851b0911f067815f8a3c7fd7cb601bc12c810` |
| full-motion STEP | `0807c2345544efe1b8dfc8b5704de07c31af7389bf6d7d9bc3940af66953eab6` |
| full-motion sidecar | `822d0b4219ebe73714f9cca201373dbfa7251d10b93408e9f422f686f26ea1a2` |
| OPEN transparent YZ PNG | `24ba7317b7d03c2638a93ee2a66f6cd80dd041cc61cf0034dabd4b077ea2a14c` |
| mid transparent YZ PNG | `6e47fb47f80f7883c828cedc02847996256780139567e09b5fe534d024e83f98` |
| END transparent YZ PNG | `c40c9cf622ee43df3cedd7841463df96e12d6577bf7a1a38a4134c9b30f40e7d` |
| OPEN transparent axial PNG | `105089d6b677610bff522d079f3e1732ff6266fabae199d8ac61b6e3930d4835` |
| collision contact sheet SVG | `dc6e7651918cf5e018c8ca403a20bc5313b3403fc93ea692b6f68ba8c10b0acf` |
| collision contact sheet PNG | `85bf6e110f7717adba83b6618c0fbc1186774793cbaae4d1334bff4fa24e874e` |

## Requirement coverage

| Contract or repair requirement | Implementation result |
|---|---|
| Exact P19 baseline and frozen inputs | PASS; baseline untouched, input `18/18`, old candidate `18/18`. |
| Zero outer rod rails/apertures | PASS source/topology/volume/label/STEP checks. |
| Preserve three inner tracks per side | PASS actual source BREP at OPEN/mid/END. |
| Move fixed axle/inner bores/keepers to `A=(-15,-11)` | PASS parameter, transform and solid checks. |
| `-45/+45 deg`, `90 deg` relative | PASS pure math, endpoints, static STEP and sidecar. |
| Centered-equivalent fixed journal | PASS constant local `(0,0)`, inverse and round-only solid. |
| Preserve rods/caps/stack/workpiece/service | PASS regression, exact static occurrence/name and STEP parity. |
| Expose six known collisions | PASS exact named actual-BREP values; no fail-open suppression. |
| No unexpected collision | PASS scoped exhaustive OPEN/mid/END census and service checks. |
| Unambiguous non-candidate media | PASS static transparent collision sheet with in-frame warnings. |
| Replacement immutable candidate | PASS, `20/20`, manifest SHA `59ad1459...95c9`. |
| Stop before future rail/print work | PASS. |

## Unresolved risks and next action

- This scaffold is intentionally not a movable or manufacturable assembly:
  all three rods intersect both solid outer plates at OPEN.
- Force, torque, friction, backlash, fit, heat, PETG strength/wear, cap
  retention, soldering ergonomics and every physical outcome remain untested.
- No future outer-rail order, path, neighboring-rail interaction or rollback
  result is represented here.
- The repaired candidate has not yet received independent critique, validation
  or formal conformance review under its new `59ad1459...95c9` fingerprint.

The next action is a distinct critic and validator rerun against the exact
replacement `SCAFFOLD_CANDIDATE.sha256`, followed by formal conformance review.
Adding even one outer rail requires a new user-confirmed contract and manifest.
