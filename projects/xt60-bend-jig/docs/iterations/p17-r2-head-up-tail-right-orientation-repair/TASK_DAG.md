# P17 R2 head-up / tail-right orientation repair task DAG

Baseline commit: `2b82131973d395e917e4471914584bcef1734fc3`.
Version disposition: focused P17 R2 correction; no P/R increment.
Frozen design input: `/tmp/p17-r2-orientation-design-input-manifest.txt`.

## User-fixed contract

- Front-view world convention: `+Z` is screen up and `+Y` is screen right.
- Completed workpiece is `└`: XT60 mating head points up; soldered tail and
  both wires leave outward to screen right.
- Preserve the current CLAMPED/END upper-left to lower-right diagonal topology
  and rod ordering. Preserve the exact numeric centers only if they remain
  compatible with three-point tangency to the corrected `└` workpiece; if the
  wrong workpiece orientation made them contradictory, allow only the smallest
  re-derived diagonal translation/rotation and record the proof.
- Replace only the wrong UNLOCKED/OPEN topology: one rod at upper-left and two
  rods on the right vertical leg (upper-right and lower-right).
- Fixed-inner guides are the direct straight OPEN-to-END rod paths. Recompute
  both side-local outer rod rails from those paths and the existing opposite
  outer rotations; do not draw rails by eye.
- Preserve the fixed purple axle at `A=(-29,17)`, four-plate architecture,
  three `OD4 x 50 mm` rods, six permanent caps, larger right force-side plate,
  and no-added-bar/link/gear/lock boundary unless a geometry gate proves a
  directly dependent parameter must reopen.
- Do not preserve the old completed-pigtail service path blindly: revalidate
  loading, reverse opening, and removal against the corrected workpiece and
  OPEN geometry.

## Material tasks

### P17-D10 — mechanism design

- Owner: `/root/three_rod_design`; role: mechanism designer.
- Objective: create `BRIEF.md`, `DESIGN.md`, and implementation handoff for an
  exact numeric corrected OPEN triangle and `└` workpiece while preserving the
  accepted END diagonal topology and retaining exact centers when feasible.
- Dependencies: frozen design manifest only.
- Allowed reads: frozen manifest entries and repository-wide policy docs.
- Exclusive writes: this iteration's `BRIEF.md`, `DESIGN.md`, `HANDOFF.md`.
- Forbidden: authoritative source, tests, CAD artifacts, review/validation,
  git, Viewer runtime, and unrelated projects.
- Done gate: exact OPEN/contact/END table; explicit rod vertex mapping;
  positive OPEN area with right vertical leg; correct workpiece axes; derived
  straight paths and inverse outer rails; actual-solid feasibility plan;
  retained/reopened parameters identified; immutable implementation manifest.
- Model class: strong/high mechanism reasoning. One attempt plus at most two
  focused repairs; stop if no collision-free numeric contract exists.

### P17-I08 — source-first implementation

- Owner: `/root/three_rod_impl`; role: CAD implementer.
- Dependency: accepted P17-D10 implementation manifest.
- Objective: implement only D10, regenerate explicit STEP targets and motion
  sidecars, add defect regressions, and produce the required snapshot/GIF
  packet and candidate fingerprint.
- Exclusive writes: XT60 P17 source, focused tests, explicit derived P17
  artifacts/sidecars/provenance, and this iteration's `HANDOFF.md` receipt.
- Forbidden: critic/reviewer/validator files, version bump, unrelated projects,
  3MF/slicer output, git delivery, or weakening gates without design reopen.
- Done gate: source-derived corrected orientation and OPEN topology; END
  unchanged; actual-solid motion/contact/service gates; written STEP validation
  and parity; mandatory visual packet; frozen candidate manifest.

### P17-C08 — independent critique

- Owner: `/root/p17_critic`; role: independent mechanism critic.
- Dependency: exact frozen P17-I08 candidate.
- Exclusive write: this iteration's `REVIEW.md` critic section.
- Done gate: classify blocker/major/minor findings against the user-fixed
  orientation, OPEN topology, preserved END, motion, support, force-path
  language, and physical boundary.

### P17-V08 — independent validation

- Owner: `/root/p17_lock_validator`; role: independent validator.
- Dependency: exact frozen P17-I08 candidate; runs parallel with P17-C08.
- Exclusive write: this iteration's `VALIDATION.md`.
- Done gate: independently reproduce math, actual-solid collision/contact,
  support, service, STEP/export parity, snapshots/GIF, and exact Viewer
  page/artifact readiness using the root uv environment.

### P17-R08 — formal join

- Owner: `/root/p17_formal_review`; role: formal reviewer.
- Dependencies: P17-C08 and P17-V08 receipts for the same fingerprint.
- Exclusive write: this iteration's `REVIEW.md` formal section.
- Done gate: accept or reject the exact candidate with explicit CAD/export,
  visual/Viewer, interactive, and physical boundaries.

## Delivery

The coordinating root verifies receipts and provenance, updates continuity,
commits on `codex/xt60-p17-r2-orientation-repair`, delivers through a new PR,
merges only after P17-R08 acceptance, and synchronizes main/branch without
touching the user's unrelated modified P13 3MF.
