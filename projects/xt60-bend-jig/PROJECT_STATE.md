# XT60 bend jig project state

Last updated: `2026-08-23`

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

## Current result

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

The `18.5 mm` span, opposed-bevel relation, detent, and cap geometry are
simulator concepts, not accepted CAD dimensions or physical mechanisms.

## Acceptance state

- Deterministic simulator: accepted for the candidate fingerprint above.
  Independent tests report `18 passed`, build succeeds, signed left/right track
  reconstruction has effectively zero skew, and sampled rod states have no
  collisions.
- Independent critic: pass/no-blocker for simulator review only.
- Formal review: conditional pass for PR delivery to user simulator review.
- Visual/runtime: blocked, not accepted. The validation environment exposed no
  Browser-plugin surface, so canvas screenshots, console checks, and live UI
  interaction could not be independently recorded.
- CAD/STEP/3MF/slicer: not started and not authorized before user simulator
  motion review.
- Physical: not accepted. Cap fit, grip effort, fixture stiffness, bevel
  hardware, lock force/self-lock, heat, wear, cycling, assembly, and springback
  remain unknown.

## Live simulator

From the repository root:

```sh
PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH \
  npm run dev --workspace projects/xt60-bend-jig
```

Then open `http://127.0.0.1:4173/projects/xt60-bend-jig/`.

## Next action

The user must review the live P17 outer-plate counter-twist motion, fixed inner
plates, primary/secondary size hierarchy, six permanent caps, and endpoint lock
concept. When a Browser-plugin surface is available, rerun only the visual and
interactive portion of `P17-V01`. If user review and browser validation pass,
open the next design iteration for real counter-rotation hardware, grounded
fixture geometry, lock mechanics, cap-fit experiments, and CAD. Do not generate
P17 STEP/3MF or print parts before that gate.
