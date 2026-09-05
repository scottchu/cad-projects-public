# Laifen Wave case
Original parametric two-piece toothbrush case; downloaded case meshes were inspected for fit diagnosis only and were never copied into new geometry.
Current deliverable: one teaching-oriented axial/diameter section under the P1 R2 width-preserving measurement gate; no case CAD, print artifact, or physical acceptance exists. Thread-budget and texture previews are deferred; the full case requirements remain pending.
Read PROJECT_STATE.md, NEXT_AGENT.md, docs/REQUIREMENTS.md and docs/iterations/CURRENT before work.
Authoritative preview contract: docs/iterations/2026-09-01-p1-r2-fit-feedback/DESIGN.md.
Setup: repository-root `uv sync --all-packages --all-groups`; Python 3.12/root .venv only.
Preview source: `preview/measurement-gate.html` (an HTML fragment for the interactive 2D gate).

Run its focused interaction test from the repository root:

```sh
node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs
```

For a wrapped local review page:

```sh
mkdir -p scratch/validation/laifen-wave-case
uv run python /Users/scottchu/.codex/plugins/cache/openai-bundled/visualize/1.0.23/skills/visualize/scripts/render.py "$(pwd)/projects/laifen-wave-case/preview/measurement-gate.html" "$(pwd)/scratch/validation/laifen-wave-case/measurement-gate-review.html"
```

The preview is a teaching illustration only: it creates no CAD, thread solids, print exports, or acceptance claim.
Later delivery: original build123d source and datums/joints; STEP body, cap, coupons and assembly; section and validated secondary STL/3MF. These remain deferred until the measurement/design gate is resolved.
