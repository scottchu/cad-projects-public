# P17 R2 locked rod-layout task DAG

Baseline HEAD: `8adfb20f352e36cede54a3414307ced3de81c2b8`.
Branch: `codex/xt60-p17-r2-locked-rod-layout`.
I10-R1 manifest/fingerprint:
`5443e39e3b82bbbc2f6e3ed8dd6c2487a69035c263d44128a47f31ddab509d93`.

## P17-D13 — exact locked-coordinate design

- Owner: `/root/three_rod_design`; role: mechanism designer.
- Objective: apply the exact user-locked rod/track delta and axle-Z change,
  derive all coordinates and rails, and classify feasibility without changing
  any locked number.
- Inputs: I10 coordinate receipt, active requirements/experience/ADR, current
  parametric dimensional baseline and the exact task contract.
- Exclusive writes: this iteration's `BRIEF.md`, `DESIGN.md`, `TASK_DAG.md`,
  `HANDOFF.md`, `IMPLEMENTATION_INPUT_MANIFEST.sha256`, and iteration `CURRENT`.
- Forbidden: source, tests, generated CAD, Viewer, Git, workpiece movement,
  coordinate repair, new mechanism/part/lock, rail drawing by eye, or physical
  claims.
- Done gate: exact rod states, END centroid, six inverse rails, ratios/angles,
  plate/web feasibility, product/service blockers, durable overlay and frozen
  manifest.
- Result: complete; coordinate contract frozen and product blockers recorded.

## P17-I13 — source-first implementation

Status: **COMPLETE AS REVIEW-ONLY MATERIALIZATION; PRODUCT BLOCKED**.

- Owner: `/root/three_rod_impl`; implementation role distinct from design and
  review.
- Result: exact D13 source, tests, ten STEP review exports, params, provenance,
  snapshots/GIF and immutable fingerprint `590e05f9...` generated.
- Gate: 22/22 implementation tests; no product acceptance claim.

## P17-C13 / P17-V13 / P17-R13 — independent gates

- C13 owner: `/root/p17_critic`; result fidelity PASS, product BLOCK.
- V13 owner: `/root/p17_lock_validator`; result fidelity PASS, product BLOCK;
  independent math, actual-solid checks, ten STEP parity and RGB motion passed.
- R13 owner: `/root/p17_formal_review`; formal reject for product, mechanical,
  physical, PR merge, release, slicing and printing.
- Next dependency: explicit user scope reopening and a superseding design; no
  delivery task is dependency-ready.
