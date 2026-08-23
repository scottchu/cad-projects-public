# Kage

Kage is a roughly 300 mm wall-mounted kinetic shadow-clock concept. This migrated project provides a clean-restart authority, an installed historical simulator/optics compatibility runtime, frozen historical evidence, and focused migration-integrity checks. It does not provide a physically accepted restart mechanism.

Start with `PROJECT_STATE.md` and `NEXT_AGENT.md`; do not select a version by filename or timestamp. `kage_cli.py` and `optical_spec.py` are installed historical compatibility runtime, not normative restart architecture. In particular, their commodity-quartz/no-gearing/non-hollow-center reference scenario is not current. Historical CAD source/tests are recoverable under `legacy/source-project/` but are not normal acceptance.

## Root-workspace setup

Run commands from the repository root:

```sh
uv sync --all-packages --all-groups
npm install
```

No project-local `.venv`, `uv.lock`, `node_modules`, or `package-lock.json` is used.

## Normal migration acceptance

```sh
uv run --package kage pytest projects/kage/tests
```

This normal suite contains migration integrity only. It does not silently execute compatibility, historical, rejected, or frozen-reference test suites.

## Optional compatibility commands

```sh
uv run --package kage pytest projects/kage/compatibility-tests
uv run kage-clock upright-optics --json
npm run --workspace kage build:three
npm run --workspace kage build:adr
```

These commands preserve the installed legacy runtime. Passing them does not validate restart requirements. The retained `kage-clock b0-evaluate` command evaluates historical Q4 result documents; its presence does not make Q4 current or physically accepted.

Serve the static page with any local HTTP server rooted at `projects/kage/`; `serve.ts` retains the legacy Bun convenience command.

## CAD and artifacts

- `references/locked-direct-gear/`: frozen parent/reference, not a finished product.
- `references/q3-r0/`: candidate/reference only.
- `manifests/`: exact provenance, inclusion/exclusion, workspace adaptation, and candidate hashes.

Future CAD must begin in a new restart namespace, keep named parametric parameters and source authority, generate explicit targets from source, and record commands/hashes in a release manifest. Do not regenerate historical artifacts merely to match their hashes.
