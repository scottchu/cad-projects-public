# Pill Click

Parametric pill-dispenser experiments preserved from `3d-print/design/pill-click`.
This is the canonical development location; migration does not approve a design
or authorize printing. Start with [PROJECT_STATE.md](PROJECT_STATE.md).

## Authority and history

Authoritative Python lives in `src/pill_click/`. P0 through V2.3 histories remain
separate. The available later experiments are P1 hollow magnetic dispenser
(three parts) and P2 bayonet refill / 8 mm rebound (four parts); P2 has source,
tests, STEP and 3MF but no standalone design brief. Do not treat a greater P
number or the old README's "current candidate" as acceptance.

`models/` preserves only the P1 and P2 files present at migration. Historical
P0 model entrypoints, manifests and two artifact-test modules referenced by the
old README were absent. [Original README](docs/legacy/README.source.md) is
historical evidence, including obsolete plugin paths and missing file links.
The distinct root-level legacy P1 spec is isolated under
`docs/legacy/root-pill-click/`; it is not importable production source.

## Root-workspace commands

Run from `/Users/scottchu/Projects/personal/design-projects`:

```sh
uv sync --all-packages --all-groups
uv lock --check
uv run --project projects/pill-click pytest projects/pill-click/tests --collect-only
uv run --project projects/pill-click pytest projects/pill-click/tests
```

The full suite is a diagnostic command, not a claim that it passes. Migration
ran only the bounded checks recorded in the iteration's `VALIDATION.md`.
No nested environment or lockfile is used; dependencies remain in this
project's `pyproject.toml`. There is no JavaScript package.

## Generation, only after a new design-validation gate

Preserved entrypoints expose `gen_step()`, for example
`models/p2_bayonet_refill_8mm_rebound/p2_released.py`. A source-defined STEP can
be generated using the shared root environment:

```sh
uv run --project projects/pill-click python -c 'import runpy; from build123d import export_step; p="projects/pill-click/models/p2_bayonet_refill_8mm_rebound/p2_released"; export_step(runpy.run_path(p+".py")["gen_step"](), p+".step")'
```

This overwrites a derived artifact and was NOT run during migration. Confirm
the selected baseline and pass cheap intent/math gates first. Use the installed
CAD skill for mesh exports and review rather than old hard-coded plugin paths.
Preserve source-authored print poses; do not infer slicer or physical acceptance.

## Restart

See [NEXT_AGENT.md](NEXT_AGENT.md), [requirements](docs/REQUIREMENTS.md),
[printing profile](PRINTING_PROFILE.md), and
[migration handoff](docs/iterations/2026-09-01-workspace-migration/HANDOFF.md).
