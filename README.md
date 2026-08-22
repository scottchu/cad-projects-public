# Design Projects

Private monorepo for personal parametric design, simulation, CAD, fabrication, and physical-validation projects.

The repository is intentionally a container for multiple independent projects. Each project keeps its own source, dependency declarations, tests, generated-artifact rules, and handoff notes. Python projects share one root `uv` workspace, `.venv`, and `uv.lock`; JavaScript projects share one root npm workspace, install, and `package-lock.json`.

## Repository layout

```text
design-projects/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
├── package.json
├── package-lock.json
├── docs/
│   ├── ARCHITECTURE.md
│   └── ADDING_A_PROJECT.md
└── projects/
    └── <project-slug>/
        ├── README.md
        ├── pyproject.toml
        ├── package.json (when JavaScript is used)
        ├── src or CAD source
        ├── tests/
        └── docs/
```

The first planned migrations are:

- `japandi-shadow-clock-simulator`
- `xt60-bend-jig`

They will be transferred one at a time. This initialization does not copy or modify either existing project.

## One-time setup

Install `uv` and Node.js/npm, clone the repository, then run from the repository root:

```bash
uv sync --all-packages --all-groups
npm install
```

`uv` creates and maintains the shared environment at `.venv/`. Do not create another `.venv` inside an individual project.

npm installs all JavaScript workspace projects from their project-owned `package.json` files using the root `package-lock.json`. Do not run separate project-local installs or retain nested lockfiles.

After pulling dependency changes, run both commands again. They update the existing environment and install instead of requiring manual recreation.

## Daily commands

Run a command for one workspace project from the repository root:

```bash
uv run --project projects/<project-slug> pytest
uv run --project projects/<project-slug> python path/to/export.py
npm run test --workspace projects/<project-slug>
npm run build --workspace projects/<project-slug>
```

Validate all currently registered workspace projects:

```bash
uv lock --check
uv sync --all-packages --all-groups
uv run pytest
npm install --package-lock-only --ignore-scripts
```

Run project JavaScript checks with the workspace-specific commands above. Repository-wide npm aggregation becomes available after JavaScript workspace projects are registered.

Project-specific commands belong in that project's README.

## Project standards

- Parametric source is authoritative; STEP, 3MF, STL, GLB, renders, and previews must be regenerated from source.
- CAD acceptance, slicer acceptance, and physical print/assembly acceptance are separate states.
- Each project documents inputs, purchased-part assumptions, tolerances, export commands, tests, and open physical-validation work.
- Each project owns its Python and JavaScript dependency declarations, while the repository owns the shared environments, resolved lockfiles, and installs.
- Generated files are committed only when they are intentional release or review artifacts.
- Migrations preserve history and working artifacts without importing local environments, caches, or disposable output.

See [Architecture](docs/ARCHITECTURE.md), [CAD workflow](docs/CAD_WORKFLOW.md), and [Adding a project](docs/ADDING_A_PROJECT.md) for the repository contract.
