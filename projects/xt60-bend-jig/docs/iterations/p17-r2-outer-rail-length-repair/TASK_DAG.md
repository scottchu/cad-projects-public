# P17 R2 outer-rail length/working-area placement repair task DAG

Baseline commit: `8adfb20f352e36cede54a3414307ced3de81c2b8`.
Branch: `codex/xt60-p17-r2-outer-force-balance`.
Frozen inputs: `INPUT_MANIFEST.sha256` plus `AUTHORIZATION.md`.

## P17-D12 — outer-rail length and working-area placement design

- Owner: `/root/three_rod_contract_finalizer`; role: mechanism designer.
- Objective: select the smallest outer-rail length/placement correction for
  Rod 1 and Rod 2. If boundary clearance requires it, rigidly translate the
  complete rod/XT60 working area inward/back without distorting its geometry.
- Dependencies: frozen inputs and explicit user correction.
- Exclusive writes: this iteration's `BRIEF.md`, `DESIGN.md`, design section
  of `HANDOFF.md`, and its immutable implementation manifest.
- Forbidden: source/tests/CAD artifacts, git, Viewer, unrelated projects,
  altered rail topology/section, new parts/mechanisms, slot widening, triangle
  distortion, track-direction changes, or gate weakening.
- Done gate: exact rail endpoint/length and optional rigid translation
  parameters; unchanged relative OPEN/contact/END/workpiece geometry; force-
  angle and side/path balance; plate boundary/web and 0.30 mm continuous
  reaction material; actual-solid collision/service/conditioning; assembly
  counts; implementation manifest.
- Ceiling: one design plus at most two focused repairs. Test the direct rail-
  length correction first, then introduce only the minimum rigid translation
  required by boundary evidence.

## P17-I10 — source-first implementation

- Owner: `/root/three_rod_impl`; role: CAD implementer.
- Dependency: accepted P17-D12 manifest.
- Exclusive writes: P17 source/tests, explicit affected STEP generators/
  exports/sidecars/snapshots/GIFs/provenance, implementation HANDOFF section.
- Done gate: root-uv regressions, actual-solid gates, STEP validation/parity,
  mandatory PNG/GIF packet, and one immutable candidate fingerprint.

## P17-C10 and P17-V10 — independent gates

- Owners: `/root/p17_critic` and `/root/p17_lock_validator`.
- Dependency: identical frozen I10 fingerprint; may run in parallel.
- Exclusive writes: this iteration's `REVIEW.md` critic section and
  `VALIDATION.md`, respectively.
- Done gate: independent force/rail/boundary/support/collision/service/
  conditioning, STEP, motion-visual, and exact Viewer page/artifact review.

## P17-R10 — formal join and delivery

- Owner: `/root/p17_formal_review`; role: formal reviewer.
- Dependencies: C10/V10 receipts for one unchanged fingerprint.
- Exclusive write: formal section of `REVIEW.md`.
- Done gate: exact candidate accept/reject with digital/physical boundaries.

Root then updates continuity, commits, opens/updates the PR, merges only after
acceptance, synchronizes main/branch, and returns the verified persistent
Viewer URL.
