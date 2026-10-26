# XT60 bend jig

Parametric PETG jig and Three.js mechanism study for holding and forming two insulated XT60 pigtail wires through a fixed 90-degree bend while they are soldered and cooled. The XT60 plastic body is not the clamped load.

## Current baseline

The digitally accepted review baseline is P19 R1: four principal plates, a
fixed purple printed stepped axle and fixed inner pair, two counter-rotating
outer plates, and three moving `OD4.00 x 50.00 mm` stainless forming rods.
One shared normalized state drives the complete left/right motion through
`-5/+5 deg`. The short-tail work area is at the `+Y`/right/front edge so the
XT60 solder cups and solder-tool keepout remain outside the largest plate.
There is no lock, yoke, linkage, gear, grip block, or self-lock claim.

Start with [PROJECT_STATE.md](PROJECT_STATE.md),
[NEXT_AGENT.md](NEXT_AGENT.md), and the iteration named by
[docs/iterations/CURRENT](docs/iterations/CURRENT). Earlier P13 and P17
candidates remain design history; they are not the current review candidate.

## Acceptance boundary

- CAD/source and six STEP exports: accepted for exact P19 R1 candidate
  fingerprint
  `e2492339de9037b6e2a84351699b693202e4585a32623305c616d97712b91677`.
- Viewer transport/readiness: accepted for exact-artifact human review; live
  slider interaction remains a user review action.
- Mesh/DfAM/slicer/3MF and all physical claims: pending. The `0.75 mm`
  completed-pigtail clearance and two `4.00 mm` rails are nominal active
  limits, not manufacturing margin. CAD does not prove force, fit, friction,
  wobble, retention, solder ergonomics, heat, wear, or self-lock behavior.

## Authoritative P19 R1 source

- `src/xt60_bend_jig/p19_r1_front_edge_short_tail.py`
- `tests/test_p19_r1_front_edge_short_tail.py`
- `docs/iterations/p19-r1-front-edge-short-tail/`
- `cad/p19_r1_front_edge_short_tail/p19_r1_full_motion.step.py`
- `cad/p19_r1_front_edge_short_tail/p19_r1_print_kit.step.py`

## Authoritative P17 R2 source

- `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`
- `tests/test_p17_r2_direct_counter_twist.py`
- `docs/iterations/p17-r2-lock-removal/`
- `cad/p17_r2_direct_counter_twist/p17_r2_fixed_axle_motion.step.py`
- `cad/p17_r2_direct_counter_twist/p17_r2_full_motion.step.py`
- `cad/p17_r2_direct_counter_twist/p17-r2-artifact-provenance.json`

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

## Generate current P19 R1 STEP review artifacts

Use the installed CAD skill runtime rather than copying its environment into the project. The current installation is shown below; update `CAD_SKILL` if the plugin version changes.

```bash
CAD_SKILL=/Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad

uv run python "$CAD_SKILL/scripts/gen" \
  projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_open.step.py \
  projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_contact.step.py \
  projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_end.step.py \
  projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_exploded.step.py \
  projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_print_kit.step.py \
  projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_full_motion.step.py \
  --write
```

Regeneration must be followed by focused tests, STEP inspection,
source/export parity, snapshot/motion review, and a new provenance fingerprint.
Do not infer mesh, slicer, 3MF, or physical acceptance from STEP generation.

## Singleton CAD Viewer

The per-user Viewer is managed by `~/.local/bin/cad-viewer`; do not start a
competing ad-hoc server on port `3245`.

```bash
cad-viewer status
cad-viewer restart
cad-viewer url --workspace "$PWD" \
  --file projects/xt60-bend-jig/cad/p19_r1_front_edge_short_tail/p19_r1_full_motion.step.py \
  --tailscale
```

The service always uses the canonical repository uv interpreter at
`/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3`.

## Three.js simulator

### Offline rail customizer

Open [`preview/xt60-rail-customizer.html`](preview/xt60-rail-customizer.html)
directly in a browser. This self-contained offline page recreates the missing
P20 rail customizer: drag the three OPEN and END hole positions, scrub motion,
inspect fixed-inner and both outer-local rail paths, save/load JSON and export
SVG drawings in mm. It does not change accepted CAD or establish fabrication
or physical acceptance. The archived P20 default's thin-web warnings remain.

Editable source is in `preview/rail-customizer/`. Rebuild the standalone HTML
from the repository root with `npm run build:rails --workspace projects/xt60-bend-jig`.
Recovery evidence is in `docs/iterations/2026-10-26-rail-customizer-recovery/`.

### Historical cam mechanism study

```bash
npm run test --workspace projects/xt60-bend-jig
npm run build --workspace projects/xt60-bend-jig
npm run dev --workspace projects/xt60-bend-jig
```

Open <http://127.0.0.1:4173>. The simulator is a design aid and requires runtime and visual verification; it does not prove CAD geometry or physical behavior.

## Historical evidence

Legacy handoff and continuation files are preserved unchanged under `docs/legacy/`. Curated historical P13 review media is under `docs/review/p13-historical/`. The current project state and active iteration take precedence when those historical files name old paths or old runtime versions.
