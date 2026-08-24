# XT60 bend jig project state

Last updated: `2026-08-24`

## Baseline

- Canonical project: `projects/xt60-bend-jig`.
- Repository baseline commit: `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`.
- Historical fabrication candidate: P13 four-plate, three-rod mechanism. P13
  remains evidence, but the latest physical assembly observations reject its
  architecture for the next design.
- Current architecture decision: `ADR-0003`, P17 simulator-first counter-twist
  with permanent caps.

## Active iteration

- Active iteration: `p17-r1-counter-twist-permanent-caps`.
- Deterministic simulator candidate fingerprint:
  `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.
- Canonical handoff:
  `docs/iterations/p17-r1-counter-twist-permanent-caps/HANDOFF.md`.
- Development branch: `codex/xt60-p17-counter-twist`.

## Current result — rejected simulator

P17 replaces the P13 same-direction shared-D-shaft motion with one relative
twist input. The two smaller inner plates remain fixed and grounded. The left
secondary outer plate rotates `-theta_rel / 2`; the larger right primary outer
plate rotates `+theta_rel / 2`. Complementary side-local tracks reconstruct the
same world position at both ends of each straight rod.

The simulator shows:

- fixed `50 mm` inner plates tied by a grounded yoke;
- a `60 mm` left secondary outer grip and `64 mm` right primary outer grip;
- six permanent rod-end caps, with no removable-cap service role;
- a provisional `18.5 mm` inner clear span around the `15.9 mm` XT60 envelope;
- a fixed-carrier opposed-bevel relation as a kinematic concept; and
- a grounded endpoint detent/hard stop at `theta_rel = 54 deg`.

The user reviewed the live simulator on `2026-08-24` and rejected it because
the holes or slots appeared to move with the animation. The user explicitly
directed the project to skip simulation rather than repair it. The
`18.5 mm` span, opposed-bevel relation, detent, cap geometry, and all other P17
simulator-specific visual choices are rejected as product-direction evidence.

## Acceptance state

- Deterministic simulator: historical evidence only; tests passed but the user
  rejected the rendered behavior and skipped the phase.
- Independent critic/formal review: superseded by the user's rejection. Their
  conditional simulator-review dispositions are not product acceptance.
- Visual/runtime: rejected by user observation.
- CAD/STEP/3MF/slicer: not started for the replacement mechanism.
- Physical: not accepted. Cap fit, grip effort, fixture stiffness, bevel
  hardware, lock force/self-lock, heat, wear, cycling, assembly, and springback
  remain unknown.

## Retired simulator service

The dedicated LaunchAgent `com.scottchu.xt60-p17-simulator` is disabled and
stopped. The Tailscale `:8443` simulator handler was removed; the unrelated
`:443` CAD Viewer handler remains unchanged.

## Next action

Do not repair or rerun the simulator. Open a new mechanism/CAD iteration from
the user's fixed-inner/opposite-outer/permanent-cap requirements and the actual
P13 physical observations. Re-derive the counter-rotation hardware, ground and
reaction path, lock mechanics, plate spacing, rod length/stack, and cap fit
without inheriting rejected simulator dimensions or animation geometry.
