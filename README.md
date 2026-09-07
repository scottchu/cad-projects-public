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
        ├── PROJECT_STATE.md
        ├── NEXT_AGENT.md
        ├── pyproject.toml
        ├── package.json (when JavaScript is used)
        ├── src or CAD source
        ├── tests/
        └── docs/
            ├── REQUIREMENTS.md
            ├── EXPERIENCE.md
            ├── decisions/
            └── iterations/
```

Reusable workflow source, policies, templates and skills belong to [CAD Workbench](https://github.com/scottchu/CAD-workbench). This repository selects them through [the versioned binding](docs/workflows-binding.json). Actual design source and evidence stay project-owned. The sticker project now lives in [sticker-projects](https://github.com/scottchu/sticker-projects) at the preserved `projects/example-sticker-pack` path; its historical V2 release remains in this repository's GitHub releases.

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
uv run --project projects/<project-slug> pytest projects/<project-slug>/tests
uv run --project projects/<project-slug> python path/to/export.py
npm run test --workspace projects/<project-slug>
npm run build --workspace projects/<project-slug>
```

Validate all currently registered workspace projects with Node.js 22 or newer:

```bash
uv lock --check
uv sync --all-packages --all-groups
uv run pytest tests/test_repository_structure.py

uv run --project projects/xt60-bend-jig pytest \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_gate0_hash_p21_pivot_and_independent_stroke_derivations \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_one_connected_complete_workpiece_has_required_extrema_and_90_degree_path \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_three_rods_are_tangent_at_contact_then_apply_locked_wire_preload \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_exact_occurrence_census_and_upward_journal_topology \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_right_cap_physical_fit_contract_is_rigid_clear_and_floor_blocked \
  projects/xt60-bend-jig/tests/test_p13_four_plate_three_rod.py::test_continuous_full_domain_motion_and_removal_certificates \
  projects/xt60-bend-jig/tests/test_p13_motion.py::test_motion_entry_has_exact_sixteen_stable_open_occurrences_and_envelope \
  projects/xt60-bend-jig/tests/test_p13_motion.py::test_javascript_solver_matches_python_kinematics_on_dense_grid \
  projects/xt60-bend-jig/tests/test_p13_motion.py::test_motion_contact_preload_directions_and_loop_are_exact \
  projects/xt60-bend-jig/tests/test_p13_rod_fit_coupon_3p8.py::test_written_step_and_model_only_3mf_roundtrip_are_valid

npm ci --ignore-scripts
git diff --exit-code -- package-lock.json
npm test --workspaces --if-present
npm run build --workspaces --if-present
```

These are the required local or delegated validation gates: repository structure, the current supported P13 architecture/regression subset, and declared JavaScript workspace tests/builds. This repository does not use hosted CI workflows; their absence does not waive testing. The complete XT60 Python suite contains historical P1–P16 export diagnostics and is intentionally manual because unsupported historical outputs make it slow and non-green; run it only when investigating migration history. Workspace-wide npm commands run scripts only where a project declares them.

Project-specific commands belong in that project's README.

## Workflows and project records

Resolve [the external workflow binding](docs/workflows-binding.json) before selecting a workflow or skill. The compatibility pointers for [CAD](docs/CAD_WORKFLOW.md), [continuity](docs/PROJECT_CONTINUITY.md), [FDM rules](docs/FDM_DESIGN_RULES.md) and [adding projects](docs/ADDING_A_PROJECT.md) preserve existing links. Workbench provides shared guidance; project records retain current source, requirements, commands, artifacts and acceptance evidence.

[Workshop inventory](docs/WORKSHOP.md) is local availability context. [Architecture](docs/ARCHITECTURE.md) explains repository ownership and [the separation handoff](docs/iterations/2026-09-07-workflow-ownership/HANDOFF.md) records migration and recovery.

## Contributing changes

Start trunk-bound work from a non-`main` branch and use the [pull request template](.github/pull_request_template.md) for the critical delivery summary and evidence pointers. Repository continuity files remain authoritative. The machine-readable delivery contract is in [`.github/repository-policy.toml`](.github/repository-policy.toml); only an explicit user override for a specific change bypasses the pull-request route. Required validation runs locally or through delegated validation, not hosted CI workflows.
