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

- For substantial CAD changes, use separate agents for design, implementation, critique, review, and validation/tests. An implementation agent must not approve its own work.
- Inspect supplied references and existing physical-test observations before broad design changes.
- Validate actual solids and written exports, not only nominal source parameters.
- State CAD validation, mesh/slicer validation, and physical print/assembly validation separately. Never present an unprinted design as physically proven.
- When a physical defect is reported, diagnose and repair the concrete failure before proposing a broad redesign.

## Documentation and handoff

- Record major decisions, assumptions, exact commands, artifact paths, test evidence, and remaining physical-validation gaps in project-local docs.
- Keep root documentation about repository-wide policy only; project design decisions belong inside the relevant project.
- Update `docs/ARCHITECTURE.md` only when the repository contract changes.
