# P17 R1 validation record

Status: deterministic simulator checks passed; Browser-plugin visual/interactive
validation blocked because no browser surface was available. P17-V01 does not
accept the simulator candidate until the browser gate is rerun successfully.

## Validator

- Owner: `P17-V01` / `/root/p17_validator`.
- Role: independent validation/test owner, distinct from design and
  implementation.
- Date/time: `2026-08-23 22:48:37 EDT`.
- Project: `projects/xt60-bend-jig`.
- Branch: `codex/xt60-p17-counter-twist`.
- Baseline commit: `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`.
- Candidate fingerprint under validation:
  `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.
- Environment: macOS Darwin `25.5.0` arm64; Node `v24.19.0`; npm `11.17.0`.
- Browser skill: `browser:control-in-app-browser` skill was read completely
  before browser work. Browser setup guidance was followed after selection
  failure.

## Frozen candidate hash verification

All requested candidate hashes matched before validation continued.

| Path | SHA-256 |
|---|---|
| `docs/iterations/p17-r1-counter-twist-permanent-caps/BRIEF.md` | `32ffa429ccf4e382dacb0bfaac897b31eec3db3d387525a8a4b719b314800d05` |
| `docs/iterations/p17-r1-counter-twist-permanent-caps/DESIGN.md` | `b421db860cebe581f24c28361796e908048126e7cc515e60f42ddd5ffbdf8989` |
| `docs/REQUIREMENTS.md` | `99746664776c4709c16d6c5acc5cfba08f5168dafa8e4b175a4d760330360591` |
| `src/cam-contract.js` | `94d76a35e3503fc26f577e12063535843e3db20cc77f667c817f0d4ecd352ee0` |
| `src/scene.js` | `3665be98ba930ec3c67c3a4618c4b7c7172e714b65755ed29e389fa5e2fd0756` |
| `src/app.js` | `5404a345b357f8cfa176e15339c03451f5c201240fbb22ede4d1c6c781f984f5` |
| `src/screenshot-contract.js` | `4060f122fa1227ecbc0b57caf2cb84463d51c3e101b1b763f69ef326cc262390` |
| `index.html` | `04497a5facaef1ae681e57888d114633fd119904a147e80f2cc965928aadb0bf` |
| `tests/cam-contract.test.mjs` | `e2b5b97550cad16f8d49b8763de9fb59ae0fa42421204d1031a42ac93233ac9f` |
| `tests/screenshot-contract.test.mjs` | `d981af0a2a66c738d6cee65c3cd72b2070630b0eb5c0d9cdac24fdaa348734e1` |
| `tests/simulation-contract.test.mjs` | `1f73e1f38286a2aeb8bd0e12f308a98182ef739f25676f979a4575152c38c902` |

## Commands and results

| Command | Result |
|---|---|
| `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm test --workspace projects/xt60-bend-jig` | Passed: `18` tests, `0` failed. |
| `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm run build --workspace projects/xt60-bend-jig` | Passed; wrote reproducible ignored bundle `dist/xt60-bend-jig.bundle.js`, `527.8kb`. |
| `git diff --check` | Passed with no whitespace errors. |
| `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm run dev --workspace projects/xt60-bend-jig` | Started local dev server at `http://127.0.0.1:4173/`. |
| Browser skill setup: `agent.browsers.get("iab")` | Failed: `Browser is not available: iab`. |
| Browser troubleshooting: `agent.documentation.get("bootstrap-troubleshooting")` | Read; guidance says inspect available browser types once and do not silently substitute an explicit unavailable backend. |
| Browser discovery: `agent.browsers.list()` | Returned `[]`. |
| URL selection: `agent.browsers.getForUrl("http://127.0.0.1:4173/projects/xt60-bend-jig/")` | Failed: `No browser is available`. |

No browser screenshots were captured because the Browser plugin exposed no
available browser surface. No files were written under `docs/review/...`.

## Deterministic simulator checks

The focused npm tests and an additional read-only module probe validated the
numeric simulator contract:

- Same-direction failure guard: sampled `theta_rel` values `0, 13.5, 27, 44,
  54` give `left + right = 0` and `right - left = theta_rel`.
- Inner rotation: both inner plate rotations remained `0` for every sampled
  state.
- Complementary reconstruction: left and right side-local slot reconstruction
  matched common rod poses with maximum floating-point delta
  `3.552713678800501e-15`.
- Rod skew: maximum sampled skew was `1.9860273225978185e-15`; modeled skew is
  effectively zero.
- Collision math: `sampledCollisionReport(121)` returned no collisions and
  minimum rod gap `11.46555297129437 mm`.
- Diameter hierarchy: primary outer `64 mm` > secondary outer `60 mm` > inner
  `50 mm`.
- Permanent cap count: scene export reports `permanentRodEndCaps: 6`.
- Inner span and XT60 relationship: inner clear span `18.5 mm`, XT60 envelope
  `15.9 mm`, surplus `2.6 mm`, within the `<= 4.0 mm` target.
- Lock endpoint/freeze: `LOCK` sets `thetaRel: 54, locked: true`; `SET_THETA`
  while locked returns the same state object; `UNLOCK` then `OPEN` returns to
  `0`.
- Screenshot presets: `open`, `mid`, `closed`, and `locked` are present with
  states `{0,false}`, `{27,false}`, `{54,false}`, and `{54,true}`.
- Static UI/source checks: tests passed for grounded naming, opposed-bevel
  relation naming, primary grip naming, permanent cap wording, one relative
  twist control, and pending-proof lock/physical language.

## Browser validation not completed

The required visual/interactive runtime checks were not completed:

- open, mid/counter-twist, closed, and locked browser screenshots;
- canvas nonblank pixel evidence;
- browser console/runtime-error inspection;
- live UI exercise of slider, open/close/cycle, lock/unlock, and camera
  buttons;
- visual confirmation that the right outer is visibly larger than the left,
  both outers are larger than the inner plates, only outers rotate in opposite
  global directions, inner/yoke stay fixed, all six permanent caps remain at
  rod ends, rod bodies remain straight, the grounded reaction yoke and
  opposed-bevel relation are visible, the detent moves/engages only when
  locked, physical proof remains pending in UI text, and the `18.5 mm` span is
  visible.

This is an environment/tooling blocker rather than an implementation finding:
the local dev server started, but the Browser plugin reported no available
browser surface.

## Requirement trace

| Requirement / risk | Evidence | Status |
|---|---|---|
| `REQ-009`: six permanent caps, no removable/service cap surface | Unit/static tests and scene count report six permanent rod-end caps; static browser-surface text test passed. | Deterministic pass; visual browser confirmation pending. |
| `REQ-010`: fixed grounded inner plates | Rotation tests and scene names for grounded inner plates/yoke passed. | Deterministic pass; visual browser confirmation pending. |
| `REQ-011`, `CON-009`: counter-rotating outer plates and complementary tracks | Rotation and reconstruction tests passed with zero practical skew. | Deterministic pass; visual browser confirmation pending. |
| `REQ-012`: outer diameter hierarchy | Numeric hierarchy `64 > 60 > 50` passed. | Deterministic pass; visual browser confirmation pending. |
| `REQ-013`: ground/reaction path and lock concept, no physical lock overclaim | Static source/UI tests passed; lock reducer freezes only at hard stop. | Deterministic pass; browser interaction pending. |
| `REQ-014`: simulator-first, no CAD/print artifact | No CAD/STEP/3MF/STL/GLB/DXF validation or generation was performed by P17-V01. | Pass for scope separation. |
| Physical unknowns `PHYS-007`-`PHYS-009` | UI/static text keeps cap fit, lock force, self-lock, heat, and physical behavior pending. | Pending physical validation; no acceptance claimed. |

## Findings

### `BLOCKING` - Browser-plugin runtime gate could not run

The required Browser-plugin visual/interactive validation did not run because
`agent.browsers.get("iab")` returned `Browser is not available: iab`,
`agent.browsers.list()` returned `[]`, and URL selection returned `No browser
is available`. This leaves the screenshot, canvas-pixel, console, and live UI
interaction requirements unverified.

Disposition: rerun P17-V01 in an environment where the Browser plugin exposes
an available browser surface. This does not require an implementation repair
unless that rerun reveals a visual or interaction defect.

## Acceptance boundaries

- Simulator deterministic validation: passed for the candidate fingerprint
  above.
- Browser/runtime visual validation: blocked and not accepted.
- CAD/source-export validation: not applicable to P17 R1; no STEP/3MF
  candidate exists.
- Artifact/slicer validation: not applicable to P17 R1.
- Physical validation: not performed. This validation does not prove cap fit,
  grip force, lock force, self-lock behavior, stiffness, heat response, wear,
  printed assembly, cycling, soldering behavior, springback, or actual XT60
  use.

## Next action

Rerun the browser portion of `P17-V01` once a Browser-plugin surface is
available. If it passes, append the screenshot paths, browser actions, console
state, and visual findings to this record and hand the same candidate
fingerprint to formal review. If it fails, return the smallest concrete visual
or interaction defect to implementation.
