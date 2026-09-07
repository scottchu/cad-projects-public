# Repository instructions

This repository owns personal design projects under `projects/<project-slug>/`: authoritative source, project-specific generation logic, dependencies, tests, decisions, assets and evidence. Preserve unrelated projects, historical records and user changes.

## Bound reusable workflows

Read `docs/workflows-binding.json` and resolve its pinned CAD Workbench revision and policy manifest before material workflow work. Workbench owns the reusable CAD workflow, continuity policy, templates, skills and viewer-service source. Follow the bound CAD workflow's delegation and independent acceptance rules; use project-local records to select the exact baseline and current iteration. Root compatibility documents are navigation pointers, not policy copies. Missing external workflow material is a concrete dependency to report, not permission to invent another implementation.

Before changing a project, read its README, PROJECT_STATE.md, NEXT_AGENT.md, requirements, experience, decisions and current iteration. Update its durable records when its state changes. Keep project-local geometry and generation logic with that project. Workshop availability is recorded in `docs/WORKSHOP.md`.

## Local environment and checks

Use Python 3.12 and the root uv workspace. Run Python through `uv run` from the repository root; repair the sole root `.venv` with `uv sync --all-packages --all-groups`. A subprocess needing an interpreter must use the absolute root `.venv/bin/python`; do not select system or another checkout's Python. No project-local environments or locks.

Use the root npm workspace, root install and `package-lock.json`. Dependencies belong in their project manifests. Run npm commands from the root. Keep caches and diagnostic scratch ignored. For shell search use `/opt/homebrew/bin/rg`; report unavailability before choosing an alternative.

Run the relevant project checks and root repository checks documented in README. Repository-hosted CI workflows are not used; their absence does not waive testing.

## Delivery

Develop trunk-bound changes on a non-main branch and deliver through a GitHub pull request unless the user explicitly overrides that route for the specific change. Preserve concise review and validation provenance in project records. The local delivery declaration is `.github/repository-policy.toml`; it does not claim server enforcement. Do not operate services or printers as incidental setup.
