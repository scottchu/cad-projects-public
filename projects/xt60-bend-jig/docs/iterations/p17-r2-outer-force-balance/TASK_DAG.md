# P17 R2 outer-rail force-balance task DAG

Baseline: `8adfb20f352e36cede54a3414307ced3de81c2b8` on
`codex/xt60-p17-r2-outer-force-balance`.

Frozen inputs: `INPUT_MANIFEST.sha256` plus `DEFECT_INPUT.md`. Any changed
listed input invalidates downstream gates that depend on it.

## P17-D11 — force-transmission design

- Owner: `/root/three_rod_design`; role: mechanism designer.
- Objective: derive the smallest rail/outer-motion correction that improves
  Rod 1 and Rod 2 force angle and two-side balance to a quantified standard
  comparable to the middle rod, while preserving the frozen product geometry.
- Dependencies: frozen input manifest.
- Allowed reads: frozen inputs, current source/tests, repository workflow.
- Exclusive writes: this iteration's `BRIEF.md`, `DESIGN.md`, and design section
  of `HANDOFF.md`; if necessary, append-only new active requirement/constraint
  IDs to `docs/REQUIREMENTS.md` and a separate observation to `EXPERIENCE.md`.
- Forbidden: source/tests/CAD artifacts, git, Viewer runtime, unrelated
  projects, architecture/version change, slot widening, or force claims.
- Done gate: exact parameter/equation contract; baseline/new force-angle and
  rail-balance table; preserved-state proof; analytic feasibility; explicit
  actual-solid and physical-boundary gates; immutable implementation manifest.
- Ceiling: strong mechanism reasoning; one design plus at most two focused
  repairs; stop if invariants make the force target infeasible.

### P17-D11-R1 — bounded outer-envelope reopening

The first D11 search proved the frozen `80/82/85 mm` plate envelope cannot
simultaneously pass force balance, guide collision, web, and continuous
two-sided support. Under the user's existing requirement that the outer plates
be larger and the force side slightly larger, one focused repair reopens only
the outer plate envelopes/profile and the virtual common rotation datum needed
to place their rails. Inner geometry, world rod states, fixed axle, slot width,
hardware, architecture, opposite rotation, and all prior D11 gates remain
frozen. The designer must select the smallest passing envelope growth or return
the exact infeasible frontier; a rejected D11 candidate may not reach I09.

### P17-D11-R2 — final bounded monotone motion-family repair

R1 proved plate growth cannot repair the remaining two-sided-support failure:
the failing probes enter another portion of the same swept rail, and the
required radial envelope already fits inside the existing outer diameters.
The final focused design repair may replace the single power-law angle curve
with a low-degree, strictly monotone, equal-magnitude/opposite motion curve.
It must retain `beta(0)=0`, `beta(1)=24 deg`, exact rod world paths/states,
fixed inner tracks, one-to-one rails, the complete force/web/support/collision/
conditioning gates, and all product invariants. It may not weaken the
`0.30 mm` two-sided-support rule, introduce a branch/cusp/dwell, change slot
width, or add geometry. If no passing low-complexity law exists after this
bounded repair, the design remains blocked for user-level reopening.

## P17-I09 — parametric implementation

- Owner: `/root/three_rod_impl`; role: CAD implementer.
- Dependency: frozen accepted P17-D11 contract.
- Objective: implement only D11, add defect regressions, regenerate affected
  STEP/motion outputs and visual evidence, and freeze one candidate fingerprint.
- Exclusive writes: P17 authoritative source/tests, explicit P17 CAD derived
  artifacts/provenance, and implementation section of this iteration's
  `HANDOFF.md`.
- Forbidden: design/review/validation files, unrelated projects, 3MF/slicer,
  version bump, or gate weakening.
- Done gate: root-uv tests; force-angle/balance regression; actual-solid math,
  support, collision, service, STEP parity; mandatory PNG/GIF review packet;
  immutable candidate manifest.

## P17-C09 — independent critique

- Owner: `/root/p17_critic`; role: independent mechanism critic.
- Dependency: exact frozen I09 candidate.
- Exclusive write: critic section of this iteration's `REVIEW.md`.
- Done gate: severity-classified findings on force logic, rail balance,
  preserved invariants, actual geometry, and physical claim boundary.

## P17-V09 — independent validation

- Owner: `/root/p17_lock_validator`; role: independent validator.
- Dependency: exact frozen I09 candidate; may run in parallel with C09.
- Exclusive write: this iteration's `VALIDATION.md`.
- Done gate: independently reproduce force-angle/balance math, kinematics,
  actual-solid, STEP/export parity, frozen visuals, and exact Viewer page plus
  artifact readiness using the root uv environment.

## P17-R09 — formal join

- Owner: `/root/p17_formal_review`; role: formal reviewer.
- Dependencies: C09 and V09 receipts on one unchanged candidate fingerprint.
- Exclusive write: formal section of this iteration's `REVIEW.md`.
- Done gate: accept/reject exact CAD/export/visual/Viewer candidate and state
  physical gaps explicitly.

## Coordination and delivery

Root schedules dependency-ready roles, verifies manifests/receipts, updates
project continuity, commits on the non-main branch, opens a concise GitHub PR,
merges only after R09 acceptance, and synchronizes local main and the delivery
branch. Maximum three worker agents active; one writer per namespace.
