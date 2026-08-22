# Repository instructions

## Scope

This is a multi-project repository for personal design work. Keep every design under `projects/<project-slug>/`; do not mix one project's source, tests, exports, or decisions into another project.

## Environment

- Use Python 3.12 and the root `uv` workspace.
- Run Python tooling through `uv run` from the repository root.
- Use `uv sync --all-packages --all-groups` to update the shared root `.venv`.
- Do not create, commit, copy, or rely on a project-local `.venv` or nested `uv.lock`.
- Keep project-specific dependencies in that project's `pyproject.toml`; keep only repository-wide tooling in the root `pyproject.toml`.
- Use the root npm workspace for JavaScript projects and run npm commands from the repository root.
- Keep project-specific JavaScript dependencies and scripts in that project's `package.json`; keep the root `package.json` limited to workspace configuration and repository-wide tooling.
- Use the root `package-lock.json` and root npm install. Do not create, commit, copy, or rely on a project-local `package-lock.json` or independently managed project-local `node_modules`.
- Let npm resolve unavoidable version conflicts inside the workspace rather than splitting projects into separate installs.

## Project boundaries

- Every project must have its own `README.md`, `pyproject.toml`, tests, and documented generation commands.
- Every project must satisfy `docs/PROJECT_CONTINUITY.md`. Agent sessions are disposable; repository files are the durable source of project state, rationale, evidence, experience, and handoff instructions.
- Before changing a project, read its `PROJECT_STATE.md`, `NEXT_AGENT.md`, requirements, experience log, decision index, and active iteration record. Do not rely on prior chat context as authority.
- Open or identify an iteration before material work. Record the exact baseline, intent, alternatives, decisions, validation, findings, unresolved risks, and next action while work is happening, not only at the end.
- Before stopping or handing work to another agent, update `PROJECT_STATE.md`, the active iteration `HANDOFF.md`, and `NEXT_AGENT.md`. A new agent must be able to resume from repository files alone.
- Keep durable reasoning and observed experience, but do not copy raw chat transcripts into the repository. Summarize decisions, rejected approaches, measurements, failures, and lessons that can affect later work.
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
- Use stable requirement and decision identifiers. Preserve superseded decisions and closed iterations as history; point to their replacements instead of rewriting history.
- Record physical observations separately from CAD inference. An observation log is append-only except for explicit factual corrections that retain the original entry and explain the correction.
- Every release artifact must identify its source revision or manifest, generating command, parameters when relevant, checksum, and separate CAD, artifact/slicer, and physical acceptance states.
- Keep root documentation about repository-wide policy only; project design decisions belong inside the relevant project.
- Update `docs/ARCHITECTURE.md` only when the repository contract changes.
