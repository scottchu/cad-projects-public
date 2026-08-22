# Repository architecture

## Goals

This repository provides one stable home for multiple independent design projects while avoiding repeated Python-environment setup.

The central rule is:

> Shared environments, installs, and lockfiles; project-owned dependency declarations, source, tests, artifacts, and decisions.

## uv workspace model

The root `pyproject.toml` declares `projects/*` as workspace members. A project becomes a member when `projects/<slug>/pyproject.toml` exists.

The workspace owns:

- `.python-version`
- `.venv/`
- `uv.lock`
- repository-wide development tools

Each project owns:

- its package metadata and runtime dependencies
- source and generators
- tests and test configuration
- export and validation commands
- design notes and physical-validation status

The root project is non-package tooling only (`tool.uv.package = false`). It should not become a shared application module or a dumping ground for project runtime dependencies.

## Dependency workflow

After adding or changing a member project:

```bash
uv lock
uv sync --all-packages --all-groups
```

To run one project without changing directories:

```bash
uv run --project projects/<project-slug> <command>
```

All workspace members resolve into one `uv.lock` and use the root `.venv`. Conflicting requirements must be resolved explicitly; do not work around them with nested environments.

## npm workspace model

The root `package.json` declares `projects/*` as npm workspace members. A JavaScript project keeps its dependencies and scripts in `projects/<slug>/package.json`, while the repository owns the root `package-lock.json` and npm install.

The repository owns:

- the root npm workspace configuration;
- `package-lock.json`;
- the root `node_modules` install;
- repository-wide JavaScript tooling, when needed.

Each JavaScript project owns:

- its runtime and development dependency declarations;
- its build, test, and development scripts;
- its simulator or application source.

Run npm commands from the repository root. Do not maintain a project-local lockfile or independent project-local install. npm may place a conflicting package version in a nested location as part of normal workspace resolution; that is still one root-managed install and is not a separate project environment.

## Project layout

A project may adapt its internal structure to the work, but should expose these stable entry points:

```text
projects/<project-slug>/
├── README.md
├── pyproject.toml
├── package.json (when JavaScript is used)
├── docs/
├── tests/
└── source and generated-release directories
```

The project README must identify authoritative source, regeneration commands, expected outputs, focused tests, and what remains physically unverified.

## Artifact policy

Generated CAD and fabrication files are allowed when they are useful handoff or release artifacts. They must remain traceable to authoritative source and preferably carry manifest or checksum evidence.

Temporary renders, slicer workspaces, caches, and bulk diagnostics are not release artifacts and should remain untracked.

## Validation states

Use distinct language for:

1. source and CAD geometry validated;
2. written STEP/mesh and slicer behavior validated;
3. physical print, fit, motion, heat, strength, or durability validated.

Passing an earlier state does not imply a later one.
