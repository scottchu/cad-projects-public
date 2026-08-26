# P18 R1 independent validation

Validator: `/root/p18_validator` (independent of design, implementation,
critique and formal review)

Date: 2026-08-26

Status: **PASS — CAD candidate and written STEP artifacts**. Physical force,
fit, cap retention, heat, wear and self-lock remain unproven.

## Frozen candidate

- Branch: `codex/xt60-p18-r1-compact-counter-twist`
- Candidate manifest:
  `CANDIDATE_MANIFEST.sha256`
- Candidate-manifest SHA-256:
  `fb0755a0d448ee000dde4bd63eacca7fbaf6e55abeb16312a7f39c5ccfc5d1d5`
- `sha256sum -c .../CANDIDATE_MANIFEST.sha256`: all 21 declared paths
  returned `OK` before validation.
- No candidate source, tests, STEP, sidecar or snapshot was edited by this
  role. This file is the validator's only write.

## Commands actually run

All Python commands used the repository-root uv environment.

```text
uv run pytest -q projects/xt60-bend-jig/tests/test_p18_r1_compact_counter_twist.py

uv run python - <<'PY'
# called the P18 evidence APIs listed below and reported their numeric results
PY

uv run python <cad-skill>/scripts/inspect validate \
  projects/xt60-bend-jig/cad/p18_r1_compact_counter_twist/p18_r1_<artifact>.step

uv run python <cad-skill>/scripts/inspect diff \
  projects/xt60-bend-jig/cad/p18_r1_compact_counter_twist/p18_r1_<artifact>.step.py \
  projects/xt60-bend-jig/cad/p18_r1_compact_counter_twist/p18_r1_<artifact>.step
```

`<artifact>` covered `open`, `contact`, `end`, `exploded`, `print_kit` and
`full_motion`. The four frozen PNGs were opened at original resolution and
visually inspected.

## Results

### Focused regression

- `test_p18_r1_compact_counter_twist.py`: **10 passed**.
- It independently covered the frozen contract hash and dimensions, accepted
  workpiece/triangle mapping, derived contact state, inverse reconstruction,
  exact-hex law, single-solid plates/web, rank/conditioning risk, production
  roles/forbidden extras, sidecar fixed occurrences and required entrypoints.

### Math and constraint evidence

- OPEN rod centers are `bottom=(-19.4852813742,7.5)`,
  `diagonal=(7.0,7.5)`, `upright=(7.0,-18.9852813742)` in YZ: exact
  upper-left -> upper-right -> lower-right topology and exact right-side
  vertical leg (`delta Y = 0`).
- END rod centers are `bottom=(-8.9,7.5)`,
  `diagonal=(-0.4849242405,0.0150757595)`,
  `upright=(7.0,-8.4)`: identity-preserving accepted diagonal wrap.
- Common rod stroke: `10.5852813742 mm`; END displacement error against the
  accepted coordinates: `1.84e-15 mm` maximum.
- `theta_contact=43.9372034996235 deg`; END is exactly `45 deg`.
- Six rod rails and two fixed-axle rails reconstruct world points with
  `3.9721e-15 mm` maximum residual. Rail branches are one-to-one, have no
  self-intersection or continuation jump, and fixed-track progress is strictly
  monotonic.
- Minimum analytic rail derivative: `0.185135989996 mm/deg`; minimum
  non-adjacent branch gap: `0.132595657991 mm`.
- Minimum web: `2.200398673579 mm` against required `2.20 mm`.
  Outer minima are left `2.739501503378 mm`, right `2.597732481369 mm`.
- Four-contact closure passed at 65 samples per side. Minimum rank is `3`,
  maximum normalized condition number is `3.750295905779`, and minimum
  `sigma_min/sigma_max` is `0.266645626138`.
- The known near-tangent diagonal/contact crossing remains a physical
  force/friction risk. Digital closure does not prove acceptable hand force.

### Actual solids, support and service

- 65-state actual-BREP motion sweep plus exact contact: maximum unintended
  intersection `0.0 mm^3`; maximum pre-contact wire intersection `0.0 mm^3`;
  minimum XT60 clearance `0.75 mm` within numeric tolerance. The named END
  wire intersections are the explicit `0.25 mm` geometric-preload allow-list.
- Full two-sided support sweep passed at 65 states, four plates and all three
  rods. Every normal-side probe and slot-end closure passed; all outer endpoint
  probe ratios were effectively `1.0`; the swept-boundary recession bound was
  `0.005098333333 mm`.
- Pigtail service path passed 2,002 BREP and 2,002 analytic samples. Maximum
  BREP intersection was `0.0 mm^3`; BREP minimum clearance was `1.25 mm`;
  controlling analytic clearance was `0.933815921231 mm` against required
  `0.75 mm`.
- Fixed-axle actual-solid sweep passed 33 states: no axle/outer-plate,
  axle/rod, keeper/outer-plate, keeper/cap, XT60 or service intersection.
  Exact frozen-feature gap and minimum outer-guide web were both
  `2.597732481369 mm`; axle-guide radial clearance was `0.15 mm`.
- Cap/stack closure passed: three rods are exactly `OD4 x 50.00 mm`, principal
  stack is `32.00 mm`, six caps engage `8.70 mm` per side, cap/plate gap is
  `0.30 mm`, and all tested cap/plate/keeper/material intersections are zero.
- Exact AF8.15 fixed-inner geometry is present in the actual source solid:
  the bore cutter is a regular six-sided polygon specified by its apothem
  `AF/2`, giving exact circumradius `8.15/sqrt(3) = 4.705404693895 mm`.
  The matching one-piece axle uses AF8.00 keys, AF10 central spacer and OD7.60
  round journals; total length is `34.90 mm`. The measured actual inner-hex
  boundary web is `8.326066463560 mm`.
- The diagnostic `centerAtCHasNoDecorativeHole` is false because a required
  derived rod/axle rail crosses the virtual datum in part of the motion; source
  inspection confirms there is no separately authored centered pivot bore or
  physical member at C. This is not a contract failure.

### Orientation and occurrence invariants

- FRONT is world YZ, screen right is `+Y`, screen up is `+Z`.
- XT60 body center is `(-5.0,20.5)` in YZ; its mating head points `+Z` and the
  horizontal tail/wires run toward `+Y`.
- The stepped axle remains fixed at `A=(-9.5,-9.5)` and both inner plates,
  both keepers and the XT60/workpiece references receive no motion-sidecar
  transform.
- Left/right outer plates rotate `-45/+45 deg` about world X through
  `C=(0,0)` while the three rods and all six caps translate by the same linear
  state law. Plate-owned rails therefore remain rigid with their plate; no
  hole is animated independently.

### Written STEP/source parity

All six written STEP files passed `inspect validate` with zero failures.
Occurrence counts were OPEN `670` leaves (service-sweep reference included),
contact `26`, END `26`, exploded `16`, print-kit `13`, and full-motion `18`.

For every generator/written-STEP pair, `inspect diff` returned:

- `topologyChanged=false`
- `geometryChanged=false`
- `bboxChanged=false`
- zero face/edge/shape-count delta
- `[0,0,0]` size and center delta

Thus source and imported STEP bounds/occurrences are identical for all six
artifacts, with no duplicate export transform.

### Snapshot review

Reviewed at original resolution:

- `p18-r1-open-front_20260826T050914Z.png`
- `p18-r1-end-front_20260826T050919Z.png`
- `p18-r1-end-opposite_20260826T050921Z.png`
- `p18-r1-exploded-iso_20260826T050923Z.png`

The views show the intended OPEN right-angle arrangement, END diagonal wrap,
opposite outer-plate rail families, head-up/tail-right workpiece orientation,
eccentric purple axle behind/left of the XT60, four plates, one stepped axle,
three rods, and six separated caps. No floating axle/keeper segment, swapped
rod identity, mirrored workpiece, extra stability bar, yoke, gear, linkage or
grip block is visible.

## Requirement disposition

- **CAD accepted for the frozen P18 R1 candidate:** math, constraints,
  actual-solid collision, support, service path, user topology/orientation,
  source/export parity and visual evidence pass.
- **Artifact/slicer acceptance:** not claimed; no mesh, 3MF or slicing was
  requested or performed.
- **Physical acceptance:** pending. Print/coupon evidence is still required
  for PETG rail friction and hand force (especially the near-tangent contact
  region), permanent cap and keeper retention, axle/bore fit, heat exposure,
  wear, assembled motion and any retention/self-lock behavior.
