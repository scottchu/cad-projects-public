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

## Immediate task — skip simulation

The user rejected the P17 simulator because the holes or slots appeared to move
with the animation and explicitly instructed the project to skip simulation.
Do not repair, rerun, validate, or present the simulator again.

Open a new mechanism/CAD iteration. Start from the physical observations and
hard user requirements, then design real counter-rotation hardware, a grounded
reaction path, endpoint locking, plate spacing, rod/stack lengths, and permanent
cap retention. Use separate design, implementation, critic, validator, and
formal-review owners as required by repository policy.

## Preserve and do not assume

- Preserve the user requirement: two inner plates fixed; two outer plates
  counter-rotate; right primary outer is slightly larger; all six caps are
  permanent.
- Do not inherit simulator slot paths, animation transforms, the `18.5 mm`
  span, `64/60/50 mm` diameters, opposed-bevel depiction, or detent geometry as
  accepted CAD input.
- A scene-only sign flip or prescribed motion is not an accepted mechanism.
- Do not claim cap fit, lock force, self-locking, fixture stiffness, heat,
  wear, springback, or physical assembly acceptance.
- Regenerate any future CAD/export artifacts only from the new authoritative
  parametric source after its independent gates.
- Use only the root `uv` and npm workspaces. Never edit generated artifacts by
  hand.

## Retired service

The P17 simulator LaunchAgent is disabled/stopped, and its Tailscale `:8443`
handler is removed. Do not re-enable it unless the user explicitly reverses the
decision.
