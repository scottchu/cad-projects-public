# P13 R1 monorepo migration brief

- Iteration ID: `p13-r1-monorepo-migration`
- Date opened: `2026-08-22`
- Legacy parent revision: `96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84`
- Imported P13 source SHA-256: `e424fac8064d35713ed15748bb8a0e1f966ef429b507ba4be5a5dc31cfc7c72b`
- Status: active

## User outcome and use sequence

Move the legacy XT60 project into the design-projects monorepo without losing design reasoning, measured experience, handoff state, parametric source, tests, or intentional release evidence. A fresh agent must be able to continue using repository files alone.

## Scope

- Add and enforce the repository project-continuity contract.
- Import the XT60 project under `projects/xt60-bend-jig`.
- Adapt Python and npm configuration to the root-owned workspaces.
- Preserve the P13 baseline without redesign.
- Reproduce tests and explicit P13 source/artifact checks in the new workspace.
- Record migration evidence and remaining physical gates.
- Preserve the newly reported center-hole physical defect for the next iteration and worktree task.

## Requirements and invariants

- Preserve the exact imported P13 source and controlling brief/amendment hashes.
- Preserve legacy source directories unchanged.
- Do not create nested `.venv`, `uv.lock`, `node_modules`, or `package-lock.json`.
- Preserve historical files under `docs/legacy/` and normalize current facts into the continuity records.
- Keep CAD/source, written artifact/slicer, and physical acceptance separate.

## Explicit non-goals

- No mechanism redesign or parameter retune.
- No center-hole repair inside the migration iteration; it receives its own post-migration iteration and regression.
- No `cadgen` upgrade during baseline reproduction.
- No claim of physical acceptance.
- No migration of caches, broad logs, complete render history, or every generated binary.

## Risks and physical unknowns

- Shared dependency resolution may expose reliance on the old environment.
- Generated serialization may differ even when geometry matches.
- Simulator source may pass contracts but still need visual runtime review.
- The failed printed center interface is not yet mapped unambiguously to a CAD feature.
- All remaining complete-assembly physical unknowns in `docs/REQUIREMENTS.md` remain open.

## Planned evidence and acceptance targets

- Source/destination checksum dry runs and key artifact hashes.
- Root workspace structure tests and absence of nested environments or locks.
- Full Python suite plus npm test/build.
- Explicit P13 STEP regeneration, geometry inspection, snapshot review, and 3MF regeneration.
- Updated release and handoff records with exact commands and results.
