# P20-SCAFFOLD-CRIT-01 independent scaffold critique

Date: `2026-08-26`

## Verdict and boundary

**BLOCKED for scaffold conformance.** This verdict applies only to the frozen
evidence-only scaffold candidate. It is not a product-candidate, print,
mechanism-performance, or physical-acceptance judgment, and this review does
not select or design any future outer rail.

The candidate correctly implements most of the axle-only sequential step, but
it does not preserve the P19 static service-envelope occurrence required by
the frozen scaffold contract. Its visual packet can also make the deliberate
rod/solid-plate intersections look like valid apertures or valid motion.

## Verified provenance

- Branch: `codex/xt60-p20-r1-fixed-rod-reset`.
- Contract-opening/current HEAD:
  `5e58e37ad22ed9d2121417c245410c3dbda45a7b`.
- Product baseline: P19 R1
  `b69b6ad12af611644987f026eef4940db9c7bb34`.
- Candidate manifest:
  `SCAFFOLD_CANDIDATE.sha256`.
- Candidate-manifest file SHA-256:
  `2f5c68e65a96ee3ef1d32150e283a23b06a3854905883180935f3540af60f903`,
  exactly matching the assigned fingerprint.
- Candidate entries: `18/18` verified.
- Nested input-manifest file SHA-256:
  `74fe83b49142ff43ce9a356825d8078c27e065bd5123f6cc446f5be00bcbadd6`,
  exactly matching the candidate header; nested entries: `18/18` verified.
- No fingerprint mismatch was found. This review inspected the exact frozen
  candidate.

## Findings

### SC-01 — BLOCKER — P19 static service geometry is omitted

The frozen `SCAFFOLD_BRIEF.md` requires the P19 service geometry to remain
unchanged and forbids deleting tool/removal evidence. P19
`build_motion_state()` has `19` top-level children and includes
`build_service_envelopes(theta, p)` as the `reference_service_envelopes_*`
child. P20 `build_motion_state()` builds only `18` children and does not add
that child.

Independent source and STEP census found:

- P19 OPEN source: `19` children, including
  `reference_service_envelopes_theta_0.0`;
- P20 OPEN source: `18` children, no service-envelope occurrence;
- P20 OPEN written STEP: `18` children, no service-envelope occurrence;
- P20 full-motion STEP: `18` children. This matches the P19 full-motion
  presentation baseline, which also omits the static service-envelope child,
  but it does not repair the OPEN/mid/END omission.

The P20 test currently asserts `18` source/export occurrences, so the test
locks in rather than detects the static omission. The collision routine does
instantiate P19 service envelopes temporarily to test production clearance,
but analytical use is not the same as preserving the service occurrence in
the static scaffold artifacts. The implementation receipt's statement that
service envelopes remain is therefore not supported by the written static
STEP census.

Smallest next action: restore the unchanged P19 service-envelope compound to
the P20 OPEN/mid/END assembly entries, add an explicit preservation/census
regression, regenerate only the affected STEP and review evidence, and issue a
new candidate fingerprint. This correction must not add a rod aperture or
outer rail.

### SC-02 — MAJOR — visual evidence can imply valid holes and valid motion

The four PNGs and sampled frames `0,18,36,54,71` of the 72-frame GIF were
visually inspected. In the opaque FRONT-YZ views, the black rods/caps render
on or through the blue solid outer plate as circular black marks. A reader can
reasonably interpret those marks as holes even though the source proves there
are zero rod apertures. The GIF then moves the intersecting solids without an
in-frame `NON-CANDIDATE / INTENTIONAL COLLISION` warning, which can look like
a functioning motion demonstration.

The source labels, root labels, manifest, sidecar and prose consistently say
`scaffold` and `non-candidate`; the defect is the delivery media itself. A
transparent/section collision view or explicit in-frame collision annotation
is needed before the snapshot packet can serve as truthful visual evidence.
It must continue to show, not hide, the intersections.

### SC-03 — MAJOR — collision measurement fails open on BREP exceptions

`intersection_volume()` catches every exception from the BREP common operation
and returns `0.0`. That can silently convert an unevaluated collision into a
false no-collision result, contrary to the contract's requirement that the
expected collisions are never suppressed and that any additional collision
blocks the scaffold.

For this exact frozen candidate, an independent strict recomputation performed
the same common operations without a catch and raised no exception. The six
OPEN values and the absence of production/service-envelope intersections are
therefore supported for these artifacts. The source still needs fail-closed
behavior before it can be accepted as the scaffold's collision authority.

## Independent positive checks

| Contract item | Result | Evidence |
|---|---|---|
| Exact candidate and nested inputs | PASS | Both manifest files and every declared entry verified. |
| Sequential zero-outer-rail STOP state | PASS | Source contains no outer rod cutter; no rail order, future rail, 3MF, slicing, or print work appears in the candidate. |
| Zero outer rod rails and substitute apertures | PASS | Each outer plate is exactly one disk minus one centered round journal. Left/right measured volumes differ from the analytic disk-minus-journal values by `1.82e-12/0.0 mm3`. |
| Preserve three inner tracks per side | PASS | P20 delegates to the frozen P19 inner-plate constructor with only the axle datum changed; focused tests verify all three retained rod paths clear both inner solids. |
| Fixed axle at `A=(-15,-11)` | PASS | Parameter guard, source placement, transform origin and sidecar all agree. |
| Physical outer rotation about `A` | PASS | `T_s(q,u)=A+R(alpha_s(u))q`; the local axle point is `(0,0)` and maps to `A` for both sides and all checked states. |
| `-45/+45 deg`, `90 deg` relative END travel | PASS | Pure-math tests and an independent Node sidecar call returned `-45/+45` at `u=1`, with 11 transforms limited to two outer plates plus three rods and six caps. |
| Centered fixed journal | PASS | Outer topology/volume is disk minus one round journal; transform and inverse tests pass, and no rod aperture is present. |
| Six expected OPEN collisions disclosed | PASS for exact current geometry | Strict BREP recomputation measured six pairs at approximately `40.212385966 mm3` each, total `241.274315796 mm3`, with no boolean exception. |
| No additional production/service collision at OPEN/mid/END | PASS for sampled exact states | Strict recomputation found only the named rod/outer pairs plus preserved P19 axle/keeper, XT60/wire and rod/wire reference contacts; no production part intersected a solder/tool service-envelope child. |
| Preserve P19 static service occurrence | **BLOCK** | P19 static source has 19 children including service envelopes; P20 static source and written STEP have 18 and omit it. |
| Truthful non-candidate visual delivery | **BLOCK** | Text/labels are explicit, but opaque PNG/GIF media hide intersections and can resemble holes or valid travel. |

## Commands and results

All repository Python commands ran from the repository root through the root
`uv` workspace.

1. `shasum -a 256 SCAFFOLD_CANDIDATE.sha256`
   - PASS; exact assigned SHA-256.
2. `shasum -a 256 -c SCAFFOLD_CANDIDATE.sha256`
   - PASS, `18/18`.
3. `shasum -a 256 SCAFFOLD_INPUT_MANIFEST.sha256` and
   `shasum -a 256 -c SCAFFOLD_INPUT_MANIFEST.sha256`
   - PASS; exact nested SHA-256 and `18/18` entries.
4. `uv run pytest -q projects/xt60-bend-jig/tests/test_p20_r1_fixed_rod_reset_scaffold.py`
   - PASS, `7/7`; the critic separately identified the missing service-census
     assertion described in SC-01.
5. Read-only `uv run python` source/STEP census, analytic outer-volume check,
   and strict all-pairs BREP common at OPEN/mid/END
   - all source/written STEP children valid;
   - exact outer disk-minus-journal volumes confirmed;
   - strict collision operations completed without exceptions;
   - P19/P20 static occurrence mismatch confirmed as `19/18`.
6. Read-only Node import of the frozen parameter sidecar at `u=1`
   - PASS; `theta=45`, left/right `-45/+45`, pivot
     `[0,-15,-11]`, and exactly 11 moving occurrence transforms.
7. Direct inspection of all four frozen PNGs and a five-frame contact sheet
   sampled from the 72-frame frozen GIF
   - geometry motion is visible, but the collision/non-candidate state is not
     self-evident in-frame; SC-02 remains.

## Requirement coverage and next action

The axle relocation, centered journal, `90 deg` relative travel, exact
zero-outer-rail topology, retained inner paths, deliberate collision numbers,
one-factor-at-a-time rationale, and STOP boundary conform. Scaffold acceptance
is blocked only by the bounded evidence defects above: restore the unchanged
static service occurrence, make collision computation fail closed, and replace
or augment the misleading review media. Then regenerate a new immutable
candidate and rerun independent scaffold critique/validation.

No rail may be added and no future rail order may be chosen during that repair.
The scaffold remains intentionally colliding and cannot be described as a
movable, manufacturable, product-accepted, or physically accepted assembly.
