# P20 Blue-Orange web coupon

Date: `2026-08-27`

Status: **FROZEN TEST-ONLY DESIGN CONTRACT; IMPLEMENTATION PENDING**

This iteration does not change the product `P` or `R` version and does not
replace `docs/iterations/CURRENT`. It defines one flat FDM coupon for the
temporarily user-approved `1.72 mm` minimum plastic web between the Blue and
Orange rail cutouts in the simulator's **LEFT OUTER local** view. Approval is
for this physical test only: it is not approval of the full 2D profile,
assembly, motion, rail set, CAD candidate, slicer project, or production part.

## Outcome and pass/fail question

Print the smallest axis-aligned rectangular PETG patch that preserves both
complete local Blue and Orange LEFT-outer `4.15 mm` curved cutters, the exact
simulator sampling/transform contract, and the P20 outer-plate thickness.

The physical question is:

> After a support-free flat print in PETG with a `0.4 mm` nozzle, are both
> curved through-slots open and is the Blue-Orange ligament visibly continuous
> through the full `3.20 mm` thickness and intact after ordinary bed removal
> and finger handling, without a crack, split, missing extrusion, or fused
> bridge at the marked minimum-web witness?

`PASS` requires every condition above. Any severed, cracked, delaminated,
missing, or fused witness region is `FAIL`. Record the actual printer, nozzle,
material, slicer/profile, layer heights, wall strategy, measured/observed
result, and photos. Passing accepts only the coupon's print/handling result;
it does not waive the product `>=2.20 mm` web rule or prove strength, heat,
wear, fatigue, force, fit, motion, or assembly behavior.

## Coordinate frame and fixed inputs

- Units are millimeters.
- Geometry is authored in the simulator's FRONT/local `YZ` plane about
  `C=(0,0)`: `+Z` is XT60 mating-head/up and `+Y` is solder-tail/wires/right.
- `X` is plate thickness; the source coupon occupies
  `X=[-1.60,+1.60]`.
- LEFT outer rotation is `alpha_left(u)=-45u deg`, `u in [0,1]`.
- The fabrication mesh is source-oriented with one broad `YZ` face on the
  build plate, thickness along build `+Z`, and no support.
- PETG and a `0.4 mm` nozzle are the only frozen process assumptions. No
  temperature, layer height, wall count, infill, speed, or cooling setting is
  invented here; print preparation must record the actual values.

## Authorized delta mask

May change in later implementation: only new coupon source, focused tests,
explicit STEP/mesh artifacts, provenance, and this iteration's downstream
evidence records.

Must remain exact: the immutable simulator; Blue/Orange identities; all listed
angles, radii, endpoints, offset, sample count, transform, cutter width,
coupon thickness, and minimum-web witness. The implementation may translate
or rigidly rotate the complete finished coupon only for print orientation; it
may not scale, mirror, smooth, refit, resample, extend, shorten, or independently
move either cutter.

Forbidden: simulator edits; product source or test edits outside the new
coupon namespace; `CURRENT`, `PROJECT_STATE.md`, or `NEXT_AGENT.md` changes in
this design task; any fixed-axle cutter; Green or other rail; plate hub/rim,
rod, cap, keeper, wire, XT60, assembly, motion, grip, or lock geometry; and any
claim that the full profile is accepted.

## Planned outputs

- Parametric source:
  `src/xt60_bend_jig/p20_blue_orange_web_coupon.py`
- Focused tests:
  `tests/test_p20_blue_orange_web_coupon.py`
- STEP generator and primary artifact:
  `cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step.py` and
  `cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.step`
- Secondary print mesh/project and provenance:
  `cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.3mf` and
  `cad/p20_blue_orange_web_coupon/p20_blue_orange_web_coupon.provenance.json`
- Downstream evidence, created only by their role owners:
  `IMPLEMENTATION.md`, `CRITIQUE.md`, `VALIDATION.md`, `REVIEW.md`, and
  `PHYSICAL.md` in this iteration directory.

## Immutable design input manifest

Baseline Git HEAD: `9698cf30e9ddb3e576c08179bfdd067446514c67`.

| Decision-bearing input | SHA-256 |
|---|---|
| `/Users/scottchu/.codex/visualizations/2026/08/26/01a03fb3-e479-7562-b8ff-8baec6a79b6b/inner-outer-rails-3d.html` | `1f7cae7260871f2ba54e663ebf24aaa01a5bdef69e5c0a40e6524736846558cc` |
| `projects/xt60-bend-jig/docs/iterations/p20-r3-wire-90deg/BRIEF.md` | `d07b20ce105c0d1b7fe3a5568ef2ed3b8ebb4524f72181f7e381f3d48600296a` |
| `projects/xt60-bend-jig/docs/REQUIREMENTS.md` | `07e86ede330777bca4f1d9975604024aada7fdf7e3d7b261bc524135cfc3cc82` |
| `projects/xt60-bend-jig/docs/EXPERIENCE.md` | `4b23ae3a0c65fb861e1215e95ba435b5747d2d3c4f085a6e07a925af37263f5c` |
| `projects/xt60-bend-jig/src/xt60_bend_jig/p20_r2_fixed_rod_arc_rail.py` | `1b004ac07fbd3f8ff2f776b3219c5b98e50825b123e1ec3410683d61134baa73` |
| `projects/xt60-bend-jig/src/xt60_bend_jig/p19_r1_front_edge_short_tail.py` | `41c06b8536fbf4e1bb2e9979d74de299232379b4b0ebf87ee81e93c63f581017` |

The simulator is read-only intent geometry, not CAD or product authority.
P20 R2's exact inheritance of P19 resolves the coupon's `3.20 mm` outer-plate
thickness; project requirements/experience resolve PETG, the `0.4 mm` nozzle,
the `4.15 mm` sliding cutter, and the ordinary `2.20 mm` web gate.

## Task DAG and status contract

Stable owner identity is the task ID. Future runtime agents must remain
distinct for implementation, critique, validation, and formal review.

| Task | Role / status | Dependencies and immutable input | Exclusive writes and deliverable | Done gate |
|---|---|---|---|---|
| `P20-WEB-DESIGN-01` | design / **COMPLETE** | manifest above | only this `BRIEF.md` and `DESIGN.md` | numeric geometry, crop, tests, physical gate, scope, and DAG frozen; hashes returned |
| `P20-WEB-IMPLEMENT-01` | implementation / **PENDING** | design manifest plus final hashes of this `BRIEF.md` and `DESIGN.md` | new coupon source/test/artifact namespace and `IMPLEMENTATION.md` only | focused tests pass; one valid STEP solid and source-oriented 3MF generated; no authority file changed |
| `P20-WEB-CRITIC-01` | independent mechanical/DfAM critic / **PENDING** | exact implementation candidate fingerprint | read-only candidate; `CRITIQUE.md` only | challenges representativeness, print orientation, witness accessibility, and unsupported claims; severities recorded |
| `P20-WEB-VALIDATE-01` | independent validator / **PENDING** | same exact candidate fingerprint as critic | read-only candidate; `VALIDATION.md` only | verifies manifest, equations, actual-solid gap/edge webs, topology, STEP/3MF parity, orientation, and snapshot |
| `P20-WEB-REVIEW-01` | formal independent reviewer / **PENDING** | joined critic and validator receipts plus dispositions | `REVIEW.md` only | accepts or rejects digital coupon release; scope and unresolved physical gate explicit |
| `P20-WEB-PHYSICAL-01` | user physical observer / **PENDING** | formally accepted exact print artifact and recorded slicer/profile | `PHYSICAL.md` only | records photos/process and the exact pass/fail answer above; does not edit CAD acceptance |

Dependency edges are `DESIGN -> IMPLEMENT -> (CRITIC || VALIDATE) -> REVIEW
-> PHYSICAL`. At most three workers may be active; there is one writer per
namespace. Each agent is limited to one focused task, one concise canonical
deliverable and receipt, bounded task-only context/tokens, and an initial
attempt plus at most two focused repair cycles. A candidate change invalidates
only downstream gates whose fingerprint includes the changed path. Stop on a
manifest mismatch, geometry ambiguity, thickness/process-authority conflict,
scope expansion, inability to reproduce the `1.72 mm` witness, or a third
material failure; reopen design or ask the user instead of guessing.

