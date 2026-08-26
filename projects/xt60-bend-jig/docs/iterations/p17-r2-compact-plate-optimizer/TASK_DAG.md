# P17 R2 compact-plate optimizer task DAG

## O15-DESIGN — owner `/root/three_rod_design`

- Role: mechanism design and numeric search contract.
- Objective: define the optimizer variables, constraints, objective ordering,
  candidate selection rules, and 2D evidence contract.
- Done gate: one numerically explicit feasible candidate in the `50..55 mm`
  target band, or a bounded infeasibility result identifying the smallest scope
  conflict; no 3D source changes.
- Dependencies: frozen `DESIGN_INPUT_MANIFEST.sha256`.
- Exclusive writes: this iteration's `BRIEF.md`, `DESIGN.md`, design receipt,
  and design-only analysis outputs under
  `docs/review/p17-r2-compact-plate-optimizer/`.
- Forbidden: authoritative CAD source/tests/STEP/3MF, requirements, prior
  iteration history, project continuity indexes, slicing or printing.
- Retry ceiling: initial search plus two focused numeric repairs.

## O15-AUDIT — owner `/root/three_rod_contract_finalizer`

- Role: independent read-only invariant and baseline auditor.
- Objective: verify that the optimizer contract preserves the exact user-facing
  topology, orientation, contact, rod identities, and no-extra-part boundary.
- Done gate: concise receipt listing frozen numeric inputs and any contradiction.
- Dependencies: frozen `DESIGN_INPUT_MANIFEST.sha256`.
- Writes: optional receipt only under this iteration.
- Forbidden: design selection, source/tests/CAD/artifact mutation.

## O15-IMPLEMENT — owner `/root/three_rod_impl`

- Role: prescribed optimizer and 2D renderer implementation.
- Objective: implement the frozen design search and generate the exact SVG/HTML
  2D gate through the root `uv` environment.
- Dependency: O15-DESIGN accepted by orchestration.
- Exclusive writes: optimizer source/tests and exact 2D review artifacts named
  by the frozen design receipt.
- Forbidden: 3D CAD/STEP/3MF, changing the contract, self-approval.

## O15-VALIDATE — owner `/root/p17_lock_validator`

- Role: independent numeric and rendered-artifact validator.
- Objective: recompute the selected candidate independently and verify every
  plotted point, label, diameter, constraint and invariant.
- Dependency: immutable O15 implementation candidate fingerprint.
- Writes: `VALIDATION.md` only.

## O15-REVIEW — owner `/root/p17_formal_review`

- Role: formal independent 2D gate join.
- Objective: join design, audit and validation receipts and decide whether the
  diagram is safe to show as a 2D proposal; this does not authorize 3D.
- Dependency: O15-DESIGN, O15-AUDIT, O15-IMPLEMENT and O15-VALIDATE.
- Writes: `REVIEW.md` only.
