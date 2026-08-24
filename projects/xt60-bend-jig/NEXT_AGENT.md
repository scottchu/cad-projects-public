# Next agent

Read `PROJECT_STATE.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`,
`docs/decisions/README.md`, and every file under the iteration named by
`docs/iterations/CURRENT` before changing this project.

## Resume point

- Active iteration: `p17-r1-counter-twist-permanent-caps`.
- Branch: `codex/xt60-p17-counter-twist`.
- Baseline commit: `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`.
- Deterministic simulator candidate fingerprint:
  `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.
- Canonical evidence: current iteration `BRIEF.md`, `DESIGN.md`,
  `VALIDATION.md`, `REVIEW.md`, and `HANDOFF.md`.
- Architecture authority: `docs/decisions/ADR-0003-p17-counter-twist-permanent-caps.md`.

## Immediate task

Obtain user review of the live P17 simulator. Verify that only the two outer
plates rotate, they rotate in opposite global directions, both inner plates and
the yoke remain fixed, the right primary outer plate reads as slightly larger,
all six permanent caps remain visible, rods remain straight, and the endpoint
detent/hard-stop concept is understandable.

When a Browser-plugin surface is available, rerun only the blocked
visual/interactive portion of `P17-V01` against the same fingerprint. Record
open, mid, closed, and locked views; nonblank canvas and console state; slider,
open/close/cycle, lock/unlock, and camera interactions.

## Preserve and do not assume

- Preserve the user requirement: two inner plates fixed; two outer plates
  counter-rotate; right primary outer is slightly larger; all six caps are
  permanent.
- Preserve signed complementary track math and zero rod-end skew. A scene-only
  sign flip is not an accepted mechanism.
- Treat the `18.5 mm` clear span, `64/60/50 mm` diameters, opposed-bevel
  relation, and detent as provisional simulator design choices.
- Do not claim the schematic opposed-bevel display is buildable hardware.
- Do not claim cap fit, lock force, self-locking, fixture stiffness, heat,
  wear, springback, or physical assembly acceptance.
- Do not generate or modify P17 CAD, STEP, 3MF, slicer, or print artifacts
  before user simulator-motion approval.
- Use only the root `uv` and npm workspaces. Never edit generated artifacts by
  hand.

## Run the simulator

From the repository root:

```sh
PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH \
  npm test --workspace projects/xt60-bend-jig
PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH \
  npm run dev --workspace projects/xt60-bend-jig
```

Open `http://127.0.0.1:4173/projects/xt60-bend-jig/`.
