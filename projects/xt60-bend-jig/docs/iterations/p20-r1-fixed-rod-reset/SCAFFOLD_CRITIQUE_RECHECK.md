# P20-SCAFFOLD-CRIT-01 focused-repair-1 independent recheck

Date: `2026-08-26`

Owner/role: `/root/p20_scaffold_critic`, independent scaffold scope/mechanism
critic, distinct from the designer, implementer, validator, and formal reviewer.

## Verdict and boundary

**PASS for exact scaffold conformance.** This verdict applies only to the
replacement evidence-only scaffold fingerprint
`59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`.
It resolves prior findings `SC-01`, `SC-02`, and `SC-03` without adding an
outer rail, choosing a future rail order, or changing the intentionally
colliding non-candidate delivery class.

This is not mechanism, product, print, manufacturing, or physical acceptance.
Independent validation and formal scaffold review remain separate gates.

## Verified provenance

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening/current HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- Product baseline: P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Replacement candidate manifest:
  `SCAFFOLD_CANDIDATE.sha256`.
- Candidate-manifest file SHA-256:
  `59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`,
  exactly matching the assigned recheck fingerprint.
- Candidate entries: `20/20` verified.
- Nested input-manifest file SHA-256:
  `74fe83b49142ff43ce9a356825d8078c27e065bd5123f6cc446f5be00bcbadd6`;
  nested entries: `18/18` verified.
- Prior blocking critique SHA-256:
  `994f38fbfa5c6fc5b27029055c175ce95e56f098e5dec2c4cd08d3c88d40d203`,
  unchanged and explicitly pinned by the replacement candidate manifest.
- No fingerprint mismatch or input drift was found.

## Prior-finding dispositions

### SC-01 — RESOLVED — static service occurrence is preserved

P20 OPEN, mid and END now each delegate to the unchanged P19
`build_service_envelopes(theta, p)` and include it as one top-level compound.
Independent source and written-STEP inspection found:

| State | Source top-level | Source leaves | STEP top-level | STEP leaves | Service top-level label |
|---|---:|---:|---:|---:|---|
| OPEN | 19 | 22 | 19 | 22 | `reference_service_envelopes_theta_0.0` / STEP-safe `0_0` |
| mid | 19 | 22 | 19 | 22 | `reference_service_envelopes_theta_22.5` / STEP-safe `22_5` |
| END | 19 | 22 | 19 | 22 | `reference_service_envelopes_theta_45.0` / STEP-safe `45_0` |
| full motion | 18 | 18 | 18 | 18 | not present, matching the P19 full-motion presentation baseline |

Every source and STEP root/leaf inspected as valid. The focused test now
enforces the exact static/full-motion census, service name, top-level source to
written-STEP volume census, bounds and labels. The former test gap is closed.

### SC-02 — RESOLVED — collision media is explicit and non-misleading

All four replacement transparent PNGs and the rendered collision contact sheet
were inspected directly. The outer plates are transparent, so the rods can be
seen passing through solid outer-plate volume instead of resembling circular
holes. The contact sheet states, in-frame:

- `NON-CANDIDATE SCAFFOLD — EXPECTED ROD/OUTER COLLISIONS`;
- `the circles are not holes`;
- `STATIC COLLISION EVIDENCE ONLY · THIS IS NOT VALID MOTION`.

OPEN, mid and END are presented as three labeled static states rather than a
motion-validity animation. The raw transparent PNGs are component evidence;
the annotated contact sheet provides their explicit delivery context. No
visual evidence claims a working mechanism.

### SC-03 — RESOLVED — collision evaluation now fails closed

`intersection_volume()` now raises the named `CollisionEvaluationError` when
the BREP common operation fails and chains the original exception. An
independent forced-failure call returned:

- exception type: `CollisionEvaluationError`;
- message: `BREP common failed; collision state is unknown`;
- chained cause: `RuntimeError`.

The focused regression exercises the same forced-failure path. Unknown
collision state can no longer be converted into `0.0`.

## Original scaffold-contract regression

| Contract item | Result | Independent evidence |
|---|---|---|
| Exact P19 baseline and frozen inputs | PASS | Replacement candidate `20/20`; nested input `18/18`; prior critique preserved and pinned. |
| Sequential zero-outer-rail STOP state | PASS | Candidate contains no added rail, rail-order decision, 3MF, STL, slicing, print work, or later-rail artifact. |
| Zero outer rod rails and substitute apertures | PASS | Each outer plate remains exactly one disk minus one centered round journal. Left/right volume deltas from the analytic form are `1.82e-12/0.0 mm3`. |
| Three fixed inner tracks per side | PASS | P19 inner constructor remains the authority; the P19+P20 regression suite passes. |
| Axle datum `A=(-15,-11)` | PASS | Parameter guard and independent transform output agree. |
| Centered-equivalent fixed journal | PASS | Local axle point is `(0,0)` for both sides and maps to world `(-15,-11)` at END. |
| `-45/+45 deg`, `90 deg` relative END travel | PASS | Independent source call returned `-45`, `+45`, and `90` relative. The sidecar remains the previously frozen scoped transform. |
| Six expected OPEN rod/outer collisions | PASS | Six exact named BREP intersections remain approximately `40.212385966 mm3` each, total `241.274315796 mm3`. |
| No unexpected sampled-state collision | PASS | Repaired fail-closed evidence returned an empty unexpected map and `passesExceptExpectedSixOpenRodOuterCollisions=True`. |
| P19 static service occurrence | PASS | Exact `19` top-level / `22` leaves at OPEN, mid and END; full motion remains `18`. |
| Truthful non-candidate review media | PASS | Transparent states plus explicit annotated contact sheet; no valid-motion implication. |
| STOP before future rail work | PASS | No outer rail was added and no future order was selected. |

## Commands and results

All Python commands ran from the repository root through the root `uv`
workspace.

1. `shasum -a 256 SCAFFOLD_CANDIDATE.sha256`
   - PASS; exact assigned SHA-256
     `59ad1459f3abcdbb3a8771f3fa10ad461471594d47dbb723781ea3597f9395c9`.
2. `shasum -a 256 -c SCAFFOLD_CANDIDATE.sha256`
   - PASS, `20/20`.
3. `shasum -a 256 SCAFFOLD_INPUT_MANIFEST.sha256` and
   `shasum -a 256 -c SCAFFOLD_INPUT_MANIFEST.sha256`
   - PASS; exact nested SHA-256 and `18/18` entries.
4. `uv run pytest -q projects/xt60-bend-jig/tests/test_p19_r1_front_edge_short_tail.py projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py`
   - PASS, `16/16`.
5. Read-only `uv run python` source/STEP recursive census, geometry validity,
   analytic outer-volume check, centered-frame evaluation, fail-closed forced
   failure, and collision-evidence query
   - PASS; exact census and labels above;
   - every inspected root and leaf valid;
   - exact disk-minus-journal topology supported;
   - forced failure raised the named error with chained cause;
   - six OPEN collisions and empty unexpected map reproduced.
6. Direct visual inspection of four transparent PNGs and the annotated contact
   sheet PNG
   - PASS; intersections are visible and the media explicitly denies holes,
     valid motion and product-candidate status.
7. Candidate-directory inventory and scoped source/test/sidecar text check
   - PASS; four STEP/generator entries, one unchanged sidecar and only the six
     replacement evidence files are present; no future rail order or added
     rail appears.

## Remaining risks and next action

The exact replacement candidate passes independent scaffold critique. The six
rod/solid-outer-plate collisions remain deliberate evidence, so the assembly
is still not movable or manufacturable. Torque, force, fit, friction, heat,
strength, wear, service ergonomics and all physical outcomes remain untested.

Proceed only to independent validation and formal scaffold conformance review
against this exact `59ad1459...95c9` fingerprint. Any later addition of one
outer rail requires a new user-confirmed one-factor-at-a-time contract and its
own immutable fingerprint; this review does not choose that rail or its order.
