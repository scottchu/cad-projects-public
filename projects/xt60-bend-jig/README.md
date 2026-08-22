# XT60 bend jig

Parametric PETG jig and Three.js mechanism study for holding and forming two insulated XT60 pigtail wires through a fixed 90-degree bend while they are soldered and cooled. The XT60 plastic body is not the clamped load.

## Current baseline

The supported prototype is P13: four principal circular plates, one rotary input, and three purchased uncut 304 stainless rods of `OD4.00 x 50.00 mm`. The rods have equal scalar travel along different guide directions. `0 deg` is open, first nominal wire contact is near `22 deg`, and `27 deg` is locked with a geometric preload proxy of `0.25 mm`.

Start with [PROJECT_STATE.md](PROJECT_STATE.md), [NEXT_AGENT.md](NEXT_AGENT.md), and the iteration named by [docs/iterations/CURRENT](docs/iterations/CURRENT). Earlier prototypes remain as design history and parametric source; they are not the current release.

## Acceptance boundary

- CAD/source: historical P13 evidence was imported and is being reproduced in the monorepo.
- Written artifact/slicer: the corrected historical P13 print kit is retained as comparison evidence until regenerated and revalidated here.
- Physical: the latest printed version exposed a center-hole fit defect: the user's "middle stick" is too thick for the center hole. The exact printed interface must be identified before changing source. Complete P13 physical acceptance remains pending.

## Authoritative P13 source

- `src/xt60_bend_jig/p13_four_plate_three_rod.py`
- `docs/p13-four-plate-three-rod-brief.md`
- `docs/p13-cad-source-domain-amendment.md`
- `docs/p13-parameter-table.md`
- `docs/p13-default-parameter-manifest.json`
- `tests/test_p13_four_plate_three_rod.py`
- `tests/test_p13_motion.py`
- `scripts/export_p13_3mf.py`
- `cad/p13_four_plate_three_rod/*.step.py`

Parametric source is authoritative. Never hand-edit generated STEP or 3MF files.

## Shared workspace setup

Run all setup and commands from the repository root:

```bash
uv lock
uv sync --all-packages --all-groups
npm install
```

This project owns its dependency declarations in `pyproject.toml` and `package.json`. The repository root owns `.venv`, `uv.lock`, `node_modules`, and `package-lock.json`.

## Tests

```bash
uv run --project projects/xt60-bend-jig pytest projects/xt60-bend-jig/tests
npm run test --workspace projects/xt60-bend-jig
npm run build --workspace projects/xt60-bend-jig
```

The Python suite includes historical prototypes and the focused P13 math, requirements, actual-solid, motion, provenance, STEP, and 3MF checks. Passing tests are CAD or artifact evidence only unless a test explicitly records a physical observation.

## Generate current P13 STEP and 3MF

Use the installed CAD skill runtime rather than copying its environment into the project. The current installation is shown below; update `CAD_SKILL` if the plugin version changes.

```bash
CAD_SKILL=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.21/skills/cad

uv run --project projects/xt60-bend-jig python "$CAD_SKILL/scripts/gen" \
  projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_print_kit.step.py \
  projects/xt60-bend-jig/cad/p13_four_plate_three_rod/p13_motion.step.py \
  --write

uv run --project projects/xt60-bend-jig python \
  projects/xt60-bend-jig/scripts/export_p13_3mf.py
```

Regeneration must be followed by focused tests, STEP inspection, source/export parity, snapshot review, 3MF validation, and the intended printer/slicer check before replacing an accepted artifact manifest.

## Three.js simulator

```bash
npm run test --workspace projects/xt60-bend-jig
npm run build --workspace projects/xt60-bend-jig
npm run dev --workspace projects/xt60-bend-jig
```

Open <http://127.0.0.1:4173>. The simulator is a design aid and requires runtime and visual verification; it does not prove CAD geometry or physical behavior.

## Historical evidence

Legacy handoff and continuation files are preserved unchanged under `docs/legacy/`. Curated historical P13 review media is under `docs/review/p13-historical/`. The current project state and active iteration take precedence when those historical files name old paths or old runtime versions.
