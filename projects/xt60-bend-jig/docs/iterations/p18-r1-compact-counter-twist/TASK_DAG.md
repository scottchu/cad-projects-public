# P18 R1 compact counter-twist task DAG

## P18-DESIGN — owner `/root/three_rod_design`

- Role: parametric 3D mechanism designer.
- Objective: map the approved 2D candidate into the existing four-plate P17
  axial architecture, define named derived parameters and exact 3D gates.
- Done: frozen `DESIGN.md` with no source mutation.
- Writes: this iteration's `DESIGN.md` only.

## P18-IMPLEMENT — owner assigned after P18-DESIGN

- Role: prescribed build123d implementation.
- Objective: create separate P18 R1 source, focused tests, CAD entrypoints,
  STEP artifacts and snapshots from the frozen design.
- Done: deterministic focused suite and source-generated artifacts complete.
- Forbidden: contract changes, self-approval, P17 source mutation, slicing.

## P18-CRITIQUE — owner distinct from implementation and review

- Role: independent mechanical/fit/service critic.
- Objective: challenge the immutable P18 candidate and record actionable
  findings without editing candidate source.

## P18-VALIDATE — owner distinct from implementation, critique and review

- Role: independent CAD/artifact validator.
- Objective: rerun math, constraint, actual-solid collision, service,
  requirement, STEP parity and snapshot gates.

## P18-REVIEW — owner `/root/p17_optimizer_formal_review`

- Role: formal independent join gate.
- Objective: accept or reject the exact P18 fingerprint after critique and
  validation dispositions. Physical acceptance remains separate.
