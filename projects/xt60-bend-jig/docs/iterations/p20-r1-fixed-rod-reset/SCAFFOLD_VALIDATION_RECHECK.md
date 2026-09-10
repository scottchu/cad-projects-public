# P20-SCAFFOLD-VAL-01 independent scaffold validation recheck

Date: `2026-08-26`

## Verdict and scope

**PASS — the focused-repair-1 candidate conforms to the frozen P20
evidence-only, intentionally colliding scaffold contract.** This is scaffold
conformance only. It is not mechanism, product, print, manufacturability,
force, fit, or physical acceptance, and it neither authorizes nor selects a
future outer-rail order.

The prior `SCAFFOLD_VALIDATION.md` remains a historical receipt for superseded
candidate-manifest SHA-256
`2f5c68e65a96ee3ef1d32150e283a23b06a3854905883180935f3540af60f903`.
It is not evidence for this recheck.

- Validator: `/root/p20_scaffold_validator`, independent of the designer,
  implementer, critic, and formal reviewer.
- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- P19 product baseline:
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Rechecked candidate-manifest SHA-256:
  `59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`.
- Nested input-manifest SHA-256:
  `74fe83b49142ff43ce9a356825d8078c27e065bd5123f6cc446f5be00bcbadd6`.
- Candidate verification: PASS, `20/20` entries.
- Nested input verification: PASS, `18/18` entries.

No source, test, STEP, generator, sidecar, snapshot, contract, continuity, or
candidate-manifest file was edited or regenerated. The only validator-owned
write is this recheck report.

## Focused repair gates

### Fail-closed collision evaluation

The focused P20 test suite passed `8/8`, including the new forced BREP-failure
regression. An independent direct call using a shape whose boolean-common
operation raises `RuntimeError` produced:

```text
CollisionEvaluationError: BREP common failed; collision state is unknown
cause: RuntimeError
```

The collision authority therefore fails closed rather than converting an
unevaluated intersection into `0 mm3`.

### Static service-envelope preservation and occurrence census

Independent source and written-STEP inspection produced:

| State | Source top-level | Source leaves | Written STEP top-level | Written STEP leaves | Preserved source service label |
|---|---:|---:|---:|---:|---|
| OPEN | `19` | `22` | `19` | `22` | `reference_service_envelopes_theta_0.0` |
| mid | `19` | `22` | `19` | `22` | `reference_service_envelopes_theta_22.5` |
| END | `19` | `22` | `19` | `22` | `reference_service_envelopes_theta_45.0` |
| full-motion | `18` | `18` | `18` | `18` | intentionally not present, matching the presentation entry contract |

Each static service occurrence contains exactly four leaves. For each state,
its leaf count, summed leaf volume, bounding-box size, and source label match a
fresh call to the unchanged P19 `build_service_envelopes()` authority. STEP
name sanitation changes only dots to underscores:
`reference_service_envelopes_theta_0_0`,
`reference_service_envelopes_theta_22_5`, and
`reference_service_envelopes_theta_45_0`.

The combined P19 and P20 regression suite passed with exit code `0` and
`16/16` tests. The successful command ran once in one session; no duplicate
pytest process was created.

## Geometry and motion gates

Independent source execution confirmed:

- fixed axle `A=(Y=-15.0,Z=-11.0) mm`;
- OPEN/mid/END angles respectively `(0,0)`, `(-22.5,+22.5)`, and
  `(-45,+45) deg`, with exactly `90 deg` relative END travel;
- fixed axle local point exactly `(0,0)` for left and right at
  `u=0,0.25,0.5,1`;
- each outer solid equals its complete P19-diameter disk minus one centered
  `OD7.90 mm` round journal;
- left analytic disk-minus-journal volume delta
  `1.8189894035458565e-12 mm3`, right delta `0 mm3`;
- exact outer labels state `zero_outer_rod_rails` and
  `centered_round_axle_journal`, with no rod cutter or substitute aperture;
- both inner plates retain the three P19 straight closed paths per side.

## Actual-solid collision census

The frozen BREP census independently recomputed the six expected OPEN
rod/solid-outer-plate intersections:

| Pair | OPEN intersection (`mm3`) |
|---|---:|
| `upright_rod::left_outer_plate` | `40.212385965949366` |
| `upright_rod::right_outer_plate` | `40.212385965949380` |
| `bottom_rod::left_outer_plate` | `40.212385965949350` |
| `bottom_rod::right_outer_plate` | `40.212385965949366` |
| `diagonal_rod::left_outer_plate` | `40.212385965949360` |
| `diagonal_rod::right_outer_plate` | `40.212385965949370` |
| **Total** | **`241.2743157956962`** |

`unexpectedCollisionMm3ByPair` is empty. The OPEN, mid, and END per-state
unexpected maps and unexpected service-envelope maps are also empty. Existing
P19 reference contacts remain separately classified and were not presented as
new P20 collisions.

## Written STEP validation and source/export parity

`scripts/inspect validate` passed every written STEP. OPEN, mid, and END each
contain `22` valid, closed, positive-volume leaves; full-motion contains `18`.

| STEP state | `refs` bounding size (`X x Y x Z mm`) | STEP SHA-256 |
|---|---|---|
| OPEN | `50.7 x 65.1247 x 58.25` | `ab87e7845b1dc62096fdff60e5bdb80adaed731d14d7c6ee3f14925fd0b3df46` |
| mid | `50.7 x 79.9423 x 83.0868` | `597cf193d9db4fb649176b60e20224907ac3941e2ca8cdeaa1c4f17d4d47801e` |
| END | `50.7 x 93.0175 x 98.6744` | `f4cff03091838057ea9202e64e4851b0911f067815f8a3c7fd7cb601bc12c810` |
| full-motion OPEN entry | `50.7 x 65.1247 x 58.25` | `0807c2345544efe1b8dfc8b5704de07c31af7389bf6d7d9bc3940af66953eab6` |

For all four generator/written-STEP pairs,
`scripts/inspect diff --planes` reported:

```text
topologyChanged=False, geometryChanged=False, bboxChanged=False, kindChanged=False
```

The focused source/export regression also compared explicit top-level
occurrence-volume sums and exact BREP bounding boxes within `1e-6 mm`.

## Transparent annotated visual evidence

The four transparent state/axial PNGs and the annotated contact-sheet PNG were
directly inspected. The frozen SVG annotation source was also checked.

The transparent views visibly expose rods passing through the solid outer
plate volume rather than depicting circular clearance holes. The contact sheet
shows OPEN, mid, and END as static evidence and carries all of these prominent
in-frame statements:

- `NON-CANDIDATE SCAFFOLD — EXPECTED ROD/OUTER COLLISIONS`;
- `SOLID OUTER PLATES ARE DISPLAYED TRANSPARENT`;
- `Dark rods pass through solid plate volume — the circles are not holes.`;
- `STATIC COLLISION EVIDENCE ONLY · THIS IS NOT VALID MOTION`.

Therefore the repaired media does not imply that rod apertures exist or that
the scaffold is valid motion. Visual evidence is diagnostic; the BREP and
topology gates remain authoritative.

Review hashes:

- OPEN transparent YZ PNG:
  `24ba7317b7d03c2638a93ee2a66f6cd80dd041cc61cf0034dabd4b077ea2a14c`
- mid transparent YZ PNG:
  `6e47fb47f80f7883c828cedc02847996256780139567e09b5fe534d024e83f98`
- END transparent YZ PNG:
  `c40c9cf622ee43df3cedd7841463df96e12d6577bf7a1a38a4134c9b30f40e7d`
- OPEN transparent axial PNG:
  `105089d6b677610bff522d079f3e1732ff6266fabae199d8ac61b6e3930d4835`
- annotated contact-sheet SVG:
  `dc6e7651918cf5e018c8ca403a20bc5313b3403fc93ea692b6f68ba8c10b0acf`
- annotated contact-sheet PNG:
  `85bf6e110f7717adba83b6618c0fbc1186774793cbaae4d1334bff4fa24e874e`

## Commands actually run

All repository Python commands ran from the repository root through the root
`uv` workspace:

```text
sha256sum SCAFFOLD_CANDIDATE.sha256
shasum -a 256 -c SCAFFOLD_CANDIDATE.sha256
sha256sum SCAFFOLD_INPUT_MANIFEST.sha256
shasum -a 256 -c SCAFFOLD_INPUT_MANIFEST.sha256
uv run pytest projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py -q
uv run pytest projects/xt60-bend-jig/tests/test_p19_r1_front_edge_short_tail.py projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py -q
uv run python <read-only-inline-check>  # fail-closed, transforms, topology, source/STEP/service and collision census
uv run python <cad-skill>/scripts/inspect validate <each-written-step> --format text
uv run python <cad-skill>/scripts/inspect refs <each-written-step> --facts --planes --positioning --format text
uv run python <cad-skill>/scripts/inspect diff <each-generator> <each-written-step> --planes --format text
```

The transparent PNGs and contact sheet were reviewed with the local image
viewer. No artifact was regenerated, so CAD Viewer startup/handoff was not
required for this inspection-only recheck.

## Limits and next gate

This PASS proves only that the exact focused-repair-1 scaffold candidate
conforms to its deliberately colliding, evidence-only contract. It does not
prove movable geometry, force/torque, clearance, wear, strength, printability,
assembly, or physical performance. A distinct formal scaffold reviewer must
verify this receipt and the updated critic result against the same
`59ad1459...` fingerprint. Adding even one outer rail remains a separate,
user-confirmed iteration with a new immutable manifest.
