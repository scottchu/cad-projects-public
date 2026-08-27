# P20-SCAFFOLD-VAL-01 independent scaffold validation

Date: `2026-08-26`

## Verdict and scope

**PASS — the frozen artifact conforms to the evidence-only, intentionally
colliding P20 scaffold contract.** This verdict is limited to scaffold
conformance. It is not mechanism, product, print, manufacturability, force,
fit, or physical acceptance, and it does not authorize or select a future
outer-rail order.

- Validator: `/root/p20_scaffold_validator`, independent of the designer,
  implementer, critic, and formal reviewer.
- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- P19 product baseline:
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Frozen candidate manifest file SHA-256:
  `2f5c68e65a96ee3ef1d32150e283a23b06a3854905883180935f3540af60f903`.
- Frozen nested input-manifest file SHA-256:
  `74fe83b49142ff43ce9a356825d8078c27e065bd5123f6cc446f5be00bcbadd6`.
- Candidate manifest verification: PASS, `18/18` entries, before validation.

No source, test, STEP, sidecar, snapshot, contract, continuity, or candidate
manifest was edited or regenerated. The only validator-owned write is this
report.

## Pure math, state, and topology gates

Independent execution against the frozen source produced:

- fixed axle `A=(Y=-15.0,Z=-11.0) mm`;
- OPEN/mid/END outer angles respectively
  `(0,0)`, `(-22.5,+22.5)`, and `(-45,+45) deg`, giving exactly `90 deg`
  relative END travel;
- centered axle guide local coordinate exactly `(0,0)` for left and right at
  `u=0,0.25,0.5,1`;
- local-to-world-to-local round trips within the focused test tolerance
  `1e-12 mm`;
- each outer solid equals its complete P19-diameter disk minus one centered
  `OD7.90 mm` journal: left volume delta from the analytic expression
  `1.82e-12 mm3`, right delta `0 mm3`;
- exact outer labels identify `zero_outer_rod_rails` and
  `centered_round_axle_journal`; no second cutter is present in the frozen
  outer-plate construction;
- both inner plates retain the delegated P19 geometry and labels identifying
  `three_straight_closed_tracks`; actual rod/inner-solid checks at OPEN, mid,
  and END remain at or below `1e-7 mm3`;
- all OPEN, mid, END, and full-motion source and written STEP assemblies have
  exactly `18` occurrences.

Focused source tests passed `7/7`. The combined P19 regression plus P20
scaffold suite completed with exit code `0` and `15/15` tests represented by
the quiet-mode progress output. The successful combined run was the sole run
used as validation evidence; an older duplicate left alive by an initial tool
wait timeout was terminated without touching candidate files.

## Actual-solid collision census

The frozen BREP census independently recomputed every named expected pair and
the exhaustive occurrence-pair checks at OPEN, mid, and END. The six OPEN
rod/solid-outer-plate collisions are present individually:

| Pair | OPEN intersection (`mm3`) |
|---|---:|
| `upright_rod::left_outer_plate` | `40.212385965949366` |
| `upright_rod::right_outer_plate` | `40.212385965949380` |
| `bottom_rod::left_outer_plate` | `40.212385965949350` |
| `bottom_rod::right_outer_plate` | `40.212385965949366` |
| `diagonal_rod::left_outer_plate` | `40.212385965949360` |
| `diagonal_rod::right_outer_plate` | `40.212385965949370` |
| **Total** | **`241.2743157956962`** |

No new unexpected collision was found at OPEN, mid, or END, and no production
part intersected any preserved service-envelope child above `1e-7 mm3`.
Expected-pair evolution was retained rather than suppressed: at mid the right
upright pair is `4.109437240100468 mm3`; at END the right upright pair is
`0 mm3` and the right diagonal pair is `8.357046092861985 mm3`. Existing P19
reference contacts between axle/keepers, XT60/wire, and post-contact rods/wire
are separately enumerated by the evidence function and were not misreported
as new P20 collisions.

## Written STEP validation and source/export parity

`scripts/inspect validate` passed all four written STEP files. Every file has
`18` occurrences, all solids valid, closed, and positive-volume, with zero
reported geometry errors.

| STEP state | Bounding size (`X x Y x Z mm`) | STEP SHA-256 |
|---|---|---|
| OPEN | `50.7 x 65.1247 x 58.25` | `fd0dd3081d300c961441f0016d5e6fff8b27c3ded25878ca39fe39351bbb674c` |
| mid | `50.7 x 79.9423 x 83.0868` | `770a27f1d51cff386b70b39dbde6e5b9e8d0e5cc16bd80a06a3b8ee4cd3b689f` |
| END | `50.7 x 93.0175 x 98.6744` | `61be69ca8cc1272213fe0c1030a27e7916f54113f74519d68da769327f9dcc64` |
| full-motion OPEN entry | `50.7 x 65.1247 x 58.25` | `d4755c4a50db132ad27663fa39b1a2b393e0865bd0ff8cfe79086a06b1a282c2` |

The table records the values reported by
`refs --facts --planes --positioning`. A separate direct build123d BREP import
comparison matched source and export occurrence counts `18/18`, total volume
within `7.28e-10 mm3`, and the source/export bounding-box dimensions within
the asserted `1e-6 mm` tolerance.

For all four generator/written-STEP pairs, `scripts/inspect diff --planes`
reported:

`topologyChanged=False, geometryChanged=False, bboxChanged=False, kindChanged=False`.

## Direct snapshot and motion review

All five frozen review files matched the candidate manifest and were directly
inspected. The four PNGs show:

- the blue outer plate face is solid except for the centered round axle
  journal; no elongated outer rod slot is visible;
- black circular rod/cap faces can occlude the outer plate because the rods
  deliberately intersect it; they are not substitute plate apertures, as
  confirmed by the outer-solid analytic volume gate;
- the gold/green fixed inner plates and their existing straight tracks remain
  behind the moving outer plate in the mid and END views;
- the OPEN axial view retains the four-plate stack, rods, axle, keepers,
  workpiece reference, and their relative X order.

The frozen GIF is `1200 x 800`, contains `72` frames, uses `60 ms` per frame,
and loops. Direct inspection of frames `0`, `35`, and `71` shows the outer disk
sweeping about the stationary lower-left journal while the inner plates stay
fixed; it also visibly preserves the intentionally colliding rod/outer state.
Visual review is diagnostic only; the math, BREP, collision, STEP, and parity
checks above determine the PASS verdict.

Snapshot hashes:

- OPEN world-YZ PNG:
  `739ba4ef58d9080a8f21eac319b88e0357f51d5b274ca825a79cbb1365385c87`
- mid world-YZ PNG:
  `38e814e15b995554fa90fcce8f31c77498ef785d22c01b97fabd9c302a1cfda8`
- END world-YZ PNG:
  `a2ed1ae597a5567de0ced28ed00d88dd37580e41e25d3bf6228c7881694c6184`
- OPEN axial-stack PNG:
  `1bd3fb8ac7e70435b718826489a6ea8fef22f3e0d1172eee828ff12df02b5f9b`
- full-motion GIF:
  `5a36b8851abcad415e16db3b80a9c874fbd95d4f48674761eafc874e1cb78839`

## Commands actually run

From repository root, using the root `uv` workspace:

```text
shasum -a 256 -c projects/xt60-bend-jig/docs/iterations/p20-r1-fixed-rod-reset/SCAFFOLD_CANDIDATE.sha256
uv run pytest projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py -q
uv run pytest projects/xt60-bend-jig/tests/test_p19_r1_front_edge_short_tail.py projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py -q
uv run python <cad-skill>/scripts/inspect validate <each-written-step> --format text
uv run python <cad-skill>/scripts/inspect refs <each-written-step> --facts --planes --positioning --format text
uv run python <cad-skill>/scripts/inspect diff <each-generator> <each-written-step> --planes --format text
uv run python <read-only-inline-check>  # transform, topology, occurrence, STEP parity, and collision census
```

The frozen PNGs and GIF were reviewed with the local image viewer. Three GIF
frames were extracted only into `/tmp/p20-gif-review.BtWwsW/` for inspection;
that temporary material is outside the repository and is not evidence or a
candidate input.

## Limits and next gate

This validation proves only that the exact frozen scaffold is internally
consistent with its explicit non-candidate contract and truthfully exposes
the temporary rod/outer collisions. It does not demonstrate movable geometry,
force/torque, wear, clearance, strength, printability, assembly, or physical
performance. A distinct formal scaffold reviewer must verify this receipt and
the critic result against the same candidate fingerprint. Any later addition
of one outer rail requires a new user-confirmed one-rail contract and a new
immutable candidate fingerprint.
