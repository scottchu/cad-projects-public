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

## Durable project memory

Agent sessions are temporary execution contexts, not authoritative project records. Every project externalizes current state and cumulative learning according to `docs/PROJECT_CONTINUITY.md`.

`PROJECT_STATE.md` is the current-state index. `NEXT_AGENT.md` is a concise restart route, not a duplicate specification. Stable requirements, experience, and architectural decisions live in project-local documents. Each active iteration has a frozen brief plus design, validation, review, and handoff records. Generated releases carry manifests that link artifacts to source and evidence.

Closed iterations and superseded decisions remain readable history. Current documents point to replacements rather than silently rewriting past reasoning.

## Agent orchestration contract

Material repository work is run as a bounded task DAG: the root agent may schedule, collect provenance/receipts, and maintain concise continuity indexes, while distinct role owners create substantive design, implementation, critique, formal review, or validation deliverables. Tasks record owner identity and task-specific SHA-256 immutable input manifests for declared frozen requirements and brief/design contracts plus applicable authoritative source/test/artifact paths; only mutable orchestration/status and evidence records are excluded. Only gates whose declared inputs changed are invalidated. Only frozen, dependency-ready tasks with disjoint writes (or read-only scopes) may run in parallel; one writer owns a project/source/artifact namespace. Implementation cannot self-approve, formal review joins independent critic and validation results, and those acceptance identities are distinct for one candidate. Continuity records retain concise receipts and durable evidence, never raw transcripts or per-agent diaries.

## Repository-local skills

Project-owned Codex skills live under `.agents/skills/<skill-name>/`. The `design-reflection` skill provides read-only, evidence-grounded daily or on-demand reflection for CAD/3D-print projects and reads repository-wide equipment availability from `docs/WORKSHOP.md`. Skills may route work, but workshop inventory and skills do not supersede project evidence, `AGENTS.md`, project continuity, mutation authority, or acceptance gates.

## Trunk delivery

`main` is the trunk branch. Changes intended for trunk are made on a non-`main` branch and enter through a GitHub pull request. Only an explicit user override for the specific change may bypass that route. Pull requests capture a concise critical delivery summary, provenance, acceptance gaps, unresolved risks, next action, and what happened; repository continuity files remain authoritative. GitHub Projects are intentionally outside the repository architecture and are not used for planning, knowledge, or delivery tracking. `.github/repository-policy.toml` is the machine-readable statement of this repository contract; it does not claim that GitHub branch protection or another server-side rule currently enforces it.

## Artifact policy

Generated CAD and fabrication files are allowed when they are useful handoff or release artifacts. They must remain traceable to authoritative source and preferably carry manifest or checksum evidence.

Temporary renders, slicer workspaces, caches, and bulk diagnostics are not release artifacts and should remain untracked.

## Validation states

Use distinct language for:

1. source and CAD geometry validated;
2. written STEP/mesh and slicer behavior validated;
3. physical print, fit, motion, heat, strength, or durability validated.

Passing an earlier state does not imply a later one.
