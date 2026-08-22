# Design Projects

Private monorepo for personal parametric design, simulation, CAD, fabrication, and physical-validation projects.

The repository is intentionally a container for multiple independent projects. Each project keeps its own source, dependencies, tests, generated-artifact rules, and handoff notes, while the repository uses one `uv` workspace, one root `.venv`, and one `uv.lock`.

## Repository layout

```text
design-projects/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
├── docs/
│   ├── ARCHITECTURE.md
│   └── ADDING_A_PROJECT.md
└── projects/
    └── <project-slug>/
        ├── README.md
        ├── pyproject.toml
        ├── src or CAD source
        ├── tests/
        └── docs/
```

The first planned migrations are:

- `japandi-shadow-clock-simulator`
- `xt60-bend-jig`

They will be transferred one at a time. This initialization does not copy or modify either existing project.

## One-time setup

Install `uv`, clone the repository, then run from the repository root:

```bash
uv sync --all-packages --all-groups
```

`uv` creates and maintains the shared environment at `.venv/`. Do not create another `.venv` inside an individual project.

After pulling dependency changes, run the same command again. It updates the existing environment instead of requiring a manual recreation.

## Daily commands

Run a command for one workspace project from the repository root:

```bash
uv run --project projects/<project-slug> pytest
uv run --project projects/<project-slug> python path/to/export.py
```

Validate all currently registered workspace projects:

```bash
uv lock --check
uv sync --all-packages --all-groups
uv run pytest
```

Project-specific commands belong in that project's README.

## Project standards

- Parametric source is authoritative; STEP, 3MF, STL, GLB, renders, and previews must be regenerated from source.
- CAD acceptance, slicer acceptance, and physical print/assembly acceptance are separate states.
- Each project documents inputs, purchased-part assumptions, tolerances, export commands, tests, and open physical-validation work.
- Generated files are committed only when they are intentional release or review artifacts.
- Migrations preserve history and working artifacts without importing local environments, caches, or disposable output.

See [Architecture](docs/ARCHITECTURE.md) and [Adding a project](docs/ADDING_A_PROJECT.md) for the workspace contract.
