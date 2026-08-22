# Adding or migrating a project

## 1. Inventory the source project

Before copying, identify:

- authoritative parametric and simulator source;
- project dependencies and Python version;
- tests and exact validation commands;
- intentional release artifacts;
- local environments, caches, logs, and disposable generated data to exclude;
- current CAD, slicer, and physical-validation status.

Do not modify the original project during this inventory.

## 2. Copy into the workspace

Create `projects/<project-slug>/` and preserve the project's meaningful internal layout. Do not copy `.venv`, `uv.lock`, Python caches, Node dependencies, slicer scratch data, or unrelated review output.

Keep the project `pyproject.toml`, but remove any project-local workspace declaration. The root workspace will own the shared lockfile and environment.

## 3. Register dependencies

From the repository root:

```bash
uv lock
uv sync --all-packages --all-groups
```

If requirements conflict with another member, resolve and test the conflict explicitly. Do not create a nested environment as a shortcut.

## 4. Verify the migration

At minimum:

```bash
uv lock --check
uv run --project projects/<project-slug> pytest
```

Then run the project's documented export and artifact checks. Compare source and destination manifests or hashes for files that were intended to move.

## 5. Document the handoff

Update the project README or handoff docs with:

- new canonical paths;
- exact setup, test, and export commands;
- accepted artifacts and checksums where appropriate;
- known failures or rejected experiments;
- remaining physical-print and assembly checks.

Commit and push one migrated project before beginning the next migration.
