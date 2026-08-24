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

## CAD preview

Use the installed `cad-viewer` workflow directly with the explicit file to review. The
workflow starts one Viewer and constructs a link from an absolute workspace path plus
the artifact path relative to that workspace. Do not add a repository launcher or pin
an installed plugin-cache version here; the installed workflow is the runtime authority.

A started server or printed URL is not proof that a preview works. Before reporting a
preview as ready, require both the exact review page to return HTTP `200` and the exact
artifact endpoint to return HTTP `200` with JSON `state == "ready"`. After inspecting
the loaded page or snapshot, the general visual claim is limited to “the requested
artifact rendered with no visible error state.” Any feature-specific visual claim must
name the inspected features and views. Keep preview readiness separate from CAD,
slicer, and physical acceptance.

## Project standards

- Parametric source is authoritative; STEP, 3MF, STL, GLB, renders, and previews must be regenerated from source.
- CAD acceptance, slicer acceptance, and physical print/assembly acceptance are separate states.
- Each project documents inputs, purchased-part assumptions, tolerances, export commands, tests, and open physical-validation work.
- Each project owns its Python and JavaScript dependency declarations, while the repository owns the shared environments, resolved lockfiles, and installs.
- Project state, design reasoning, observed experience, validation, and next-agent instructions must live in the repository. Agent sessions are not project memory.
- Every active project points to one current iteration whose brief, design record, validation, review, and handoff are sufficient for a fresh agent to continue.
- Generated files are committed only when they are intentional release or review artifacts.
- Migrations preserve history and working artifacts without importing local environments, caches, or disposable output.

See [Architecture](docs/ARCHITECTURE.md), [Project continuity](docs/PROJECT_CONTINUITY.md), [CAD workflow](docs/CAD_WORKFLOW.md), [Workshop inventory](docs/WORKSHOP.md), and [Adding a project](docs/ADDING_A_PROJECT.md) for the repository contract and fabrication context.

## Contributing changes

Start trunk-bound work from a non-`main` branch and use the [pull request template](.github/pull_request_template.md) for the critical delivery summary and evidence pointers. Repository continuity files remain authoritative. The machine-readable delivery contract is in [`.github/repository-policy.toml`](.github/repository-policy.toml); only an explicit user override for a specific change bypasses the pull-request route. Required validation runs locally or through delegated validation, not hosted CI workflows.
