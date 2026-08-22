# Adding or migrating a project

## 1. Inventory the source project

Before copying, identify:

- authoritative parametric and simulator source;
- project dependencies and Python version;
- tests and exact validation commands;
- intentional release artifacts;
- local environments, caches, logs, and disposable generated data to exclude;
- current CAD, slicer, and physical-validation status.
- existing decisions, failed approaches, measured observations, and handoff material that must become durable project history.

Do not modify the original project during this inventory.

## 2. Copy into the workspace

Create `projects/<project-slug>/` and preserve the project's meaningful internal layout. Do not copy `.venv`, `uv.lock`, Python caches, `node_modules`, a project-local `package-lock.json`, slicer scratch data, or unrelated review output.

Keep the project `pyproject.toml`, but remove any project-local workspace declaration. The root workspace will own the shared lockfile and environment.

Keep the project `package.json` when JavaScript is used, but remove any project-local npm workspace declaration. The root npm workspace will own dependency resolution, the lockfile, and the install.

Create the continuity structure from `docs/templates/project-continuity/`. Preserve legacy handoff files under project-local `docs/legacy/`, then normalize their current facts into `PROJECT_STATE.md`, `NEXT_AGENT.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`, the decision index, and the migration iteration. Do not leave a legacy summary as the only source of current truth.

## 3. Register dependencies

From the repository root:

```bash
uv lock
uv sync --all-packages --all-groups
npm install
```

If requirements conflict with another member, resolve and test the conflict explicitly. Do not create a nested environment as a shortcut.

Run both Python and npm commands from the repository root. Keep dependency declarations with the project that uses them; add only repository-wide tooling to the root manifests.

## 4. Verify the migration

At minimum:

```bash
uv lock --check
uv run --project projects/<project-slug> pytest projects/<project-slug>/tests
npm run test --workspace projects/<project-slug> --if-present
npm run build --workspace projects/<project-slug> --if-present
```

Then run the project's documented export and artifact checks. Compare source and destination manifests or hashes for files that were intended to move.

## 5. Document the handoff

Update the project README or handoff docs with:

- new canonical paths;
- exact setup, test, and export commands;
- accepted artifacts and checksums where appropriate;
- known failures or rejected experiments;
- remaining physical-print and assembly checks.

Complete the active iteration's validation, review, and handoff records; update `PROJECT_STATE.md` and `NEXT_AGENT.md`; and verify that a new agent can identify the baseline, accepted evidence, unresolved risks, and next action without session history.

Commit and push one migrated project before beginning the next migration.
