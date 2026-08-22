# Repository instructions

## Scope

This is a multi-project repository for personal design work. Keep every design under `projects/<project-slug>/`; do not mix one project's source, tests, exports, or decisions into another project.

## Environment

- Use Python 3.12 and the root `uv` workspace.
- Run Python tooling through `uv run` from the repository root.
- Use `uv sync --all-packages --all-groups` to update the shared root `.venv`.
- Do not create, commit, copy, or rely on a project-local `.venv` or nested `uv.lock`.
- Keep project-specific dependencies in that project's `pyproject.toml`; keep only repository-wide tooling in the root `pyproject.toml`.

## Project boundaries

- Every project must have its own `README.md`, `pyproject.toml`, tests, and documented generation commands.
- Preserve unrelated projects and user changes.
- Transfer existing projects one at a time and verify each migration before starting the next.
- Treat parametric source as authoritative. Regenerate derived STEP, 3MF, STL, GLB, DXF, renders, manifests, and checksums from source; never hand-edit generated CAD artifacts.
- Commit only intentional source, documentation, tests, and release/review artifacts. Exclude environments, caches, logs, screenshots, slicer scratch data, and other reproducible temporary files.

## CAD workflow

- Follow `docs/CAD_WORKFLOW.md` for CAD design, testing, review, and handoff.
- Before modeling, identify the exact current baseline by path/version and record the user's requirements, invariants, intended use sequence, and explicit non-goals. A locked baseline may change only intentionally, in a new version, with regression evidence.
- For substantial CAD changes, use separate agents for design, implementation, critique, review, and validation/tests. An implementation agent must not approve its own work. Keep one bounded agent per role, hand off exact immutable paths, and stop unused agents.
- Inspect supplied references and existing physical-test observations before broad design changes. Observed failures outrank nominal CAD assumptions.
- Treat every design as parametric: expose meaningful named parameters, derive dependent dimensions mathematically, and identify invariant, derived constraint, design choice, and physical unknown separately.
- Use a small risk-driven test plan. Every test must name a credible failure it can catch; test count is not a quality metric.
- Every non-trivial CAD change requires the four core evidence categories: object-collision, math, constraint, and user-requirement checks. Cosmetic-only changes still require geometry validation and a snapshot, but should not invent irrelevant tests. Add motion/service-path, source/export parity, manufacturing, or defect-regression checks only when that risk exists.
- Validate actual solids, hardware-inclusive assemblies, critical motion/service states, and written exports—not only nominal source parameters or screenshots.
- Snapshot and visually review the primary artifact after deterministic checks. Visual approval does not replace geometric evidence.
- State CAD validation, written STEP/mesh/slicer validation, and physical print/assembly validation separately. Never present an unprinted design as physically proven.
- When a physical defect is reported, first add or identify a regression that represents the concrete failure, then make the smallest responsible source change and rerun only the affected focused gates before broader regression.

## Documentation and handoff

- Record major decisions, assumptions, exact commands, artifact paths, test evidence, and remaining physical-validation gaps in project-local docs.
- Keep root documentation about repository-wide policy only; project design decisions belong inside the relevant project.
- Update `docs/ARCHITECTURE.md` only when the repository contract changes.
