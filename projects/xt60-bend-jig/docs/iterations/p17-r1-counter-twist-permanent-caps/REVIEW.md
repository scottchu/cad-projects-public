# P17 R1 review record

Status: superseded by user rejection on `2026-08-24`; simulator phase skipped.

## Critic record: `P17-C01`

Status: pass/no-blocker for critic gate. The candidate is acceptable for simulator review only. It must not be promoted to CAD, print, lock-force, cap-fit, or bevel/differential acceptance without later design, CAD, validation, and physical evidence.

Candidate fingerprint verified on entry: `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.

Verified path hashes:

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

Findings by severity:

- Medium, mechanical schematic risk, non-blocking for simulator: the opposed-bevel/differential display is a concept marker, not buildable mechanism evidence. `scene.js` names a `fixed-carrier-opposed-bevel-differential-idler-one-to-one-relation` and places side bevels plus an idler (`src/scene.js:31`-`src/scene.js:32`), while the actual 1:1 opposite relationship is enforced numerically in `plateRotations()` (`src/cam-contract.js:21`-`src/cam-contract.js:22`) rather than by simulated gear contact. For coaxial, separated outer plates, a fixed-carrier bevel differential may be a plausible future architecture only after gear axes, tooth geometry, bearings, carrier grounding, clearances, and torque path are designed. Disposition: acceptable because visible UI calls it a depiction/concept with proof pending (`index.html:72`, `src/app.js:7`), but later CAD must reopen this as a real mechanism design problem.

- Medium, ground/reaction-path incompleteness, non-blocking for simulator: fixed inner plates are correctly held at zero rotation and tied visually by a yoke (`src/scene.js:29`-`src/scene.js:30`, `src/scene.js:39`), and the UI states the intended rod-load path (`index.html:70`). However, the yoke is still a floating simulator frame, not a bench clamp, handle, fixture interface, or hand reaction design. Disposition: passes the simulator requirement to show a grounded reaction concept; remains a CAD/physical risk for stiffness, anchoring, grip load, and actual load transfer.

- Medium, dimensional-wording risk, non-blocking: the candidate reduces the simulator span to `18.5 mm` against the `15.9 mm` XT60 envelope (`src/cam-contract.js:2`-`src/cam-contract.js:5`, `tests/cam-contract.test.mjs:4`) and this directly addresses the photo-3 middle-spacing observation. The visible chip says `18.5 mm INNER SPAN` (`index.html:25`) without repeating that it is provisional simulator geometry, while the durable requirement correctly says it is not yet a CAD dimension (`docs/REQUIREMENTS.md:39`). Disposition: acceptable under the surrounding `P17 / SIMULATOR-FIRST` and `KINEMATIC CONCEPT` copy (`index.html:37`, `index.html:76`), but any user-facing handoff should call it a provisional simulator target, not a finished CAD dimension.

- Low, primary-grip affordance ambiguity, non-blocking: hierarchy is numerically correct (`64 > 60 > 50` in `src/cam-contract.js:1`-`src/cam-contract.js:4`) and rendered as right-primary versus left-secondary grip plates (`src/scene.js:16`-`src/scene.js:20`). The 64/60 diameter delta is only 4 mm, both outer plates share similar material/color, and separated left/right placement may make "primary force side" subtle in some camera views. Disposition: passes the requirement but should be visually checked in browser screenshots before user review.

- Low, cap/service risk, non-blocking: six permanent caps are represented by constants and rod-end meshes (`src/scene.js:10`, `src/scene.js:34`), and P17 UI/source avoids removable/service-cap wording except historical P13 notes (`index.html:25`, `index.html:76`, `tests/simulation-contract.test.mjs:5`). The cap meshes are simple cylinders outside the outer plates, not physical blind sockets, retention features, or an assembly sequence. Disposition: acceptable simulator abstraction; cap fit/retention remains `PHYS-007` and needs coupons/CAD later.

- Low, lock depiction risk, non-blocking: the lock is endpoint-only in the reducer (`src/cam-contract.js:23`-`src/cam-contract.js:30`), grounded in scene naming/placement (`src/scene.js:33`, `src/scene.js:39`), and explicitly bounded as a kinematic concept without force or self-lock proof (`index.html:51`-`index.html:52`, `src/app.js:7`). Disposition: passes simulator intent; no physical lock, detent force, contact-normal, wear, creep, or release-effort claim exists.

Requirement coverage and critic disposition:

| Requirement / risk | Critic disposition |
|---|---|
| `REQ-009` six permanent caps | Pass for simulator; physical cap fit and retention pending. |
| `REQ-010` fixed inner plates | Pass for simulator; actual fixture/bench reaction pending. |
| `REQ-011` counter-rotating outer plates under one relative twist | Pass; math uses equal/opposite rotations and side-local reconstruction, not same-direction P13 shaft motion. |
| `REQ-012` outer/primary diameter hierarchy | Pass with visual ambiguity risk. |
| `REQ-013` ground/reaction path and lock concept | Pass as concept; bevel/differential, fixture, and lock force remain unresolved. |
| `REQ-014` simulator-first, no CAD/print claim | Pass; no P17 STEP/3MF/CAD validation is claimed. |
| `CON-009` rod-end coincidence | Pass by source math and local spot checks; validator still needs browser/screenshot evidence. |
| `CON-010` reduced `18.5 mm` inner span | Pass as provisional simulator target; not a finished CAD dimension. |

Read-only commands and evidence:

- `git status --short --branch && git rev-parse HEAD && git branch --show-current` -> branch `codex/xt60-p17-counter-twist`, baseline `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`; scoped working tree changes only.
- `shasum -a 256 ...` over frozen P17 contract/source/test paths -> matched the candidate hashes listed above.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm test --workspace projects/xt60-bend-jig` -> `18` passed, `0` failed.
- Static source inspection of `src/cam-contract.js`, `src/scene.js`, `src/app.js`, `index.html`, and focused tests.
- Direct inspection of the three supplied photos from `/tmp/codex-remote-attachments/.../B931B501-4470-4E89-82E8-BD46F0E51353/`: photos 1/2 show the superseded P13 same-shaft/keeper visual architecture; photo 3 shows permanent caps, rod protrusion, and excessive middle spacing.
- Spot-check script over sampled `theta_rel` values `0, 13.5, 27, 44, 54` -> equal/opposite rotations, zero side reconstruction delta to numeric precision, distinct left/right side-local slot samples, and no sampled rod collisions; minimum sampled rod gap `11.46555297129437 mm`.

Unresolved risks:

- Browser validator still needs screenshot/pixel evidence that the primary plate, fixed yoke, caps, detent, and timing relation are actually visible and not visually occluded.
- The actual `dist/xt60-bend-jig.bundle.js` contains P17 code in this checkout, but it is generated runtime output outside the declared source/test candidate hash list; formal review should decide whether this is acceptable for delivery or whether the served bundle needs its own recorded hash.
- Bevel/differential, cap retention, physical lock, print clearances, heat, stiffness, wear, wire holding, springback, and completed assembly remain physical/CAD unknowns.

## Formal review record: `P17-R01`

Status: conditional pass for PR delivery as a simulator-review candidate; visual/browser acceptance remains blocked. Do not begin P17 CAD, STEP/3MF, print, cap-fit, bevel-hardware, or physical-lock work from this gate.

### Provenance join

- Owner: `P17-R01` / `/root/p17_formal_review`, distinct from design, implementation, critic, and validation.
- Branch and baseline verified: `codex/xt60-p17-counter-twist` at `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`.
- Candidate fingerprint joined: `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.
- Critic provenance accepted: `P17-C01` reviewed the exact same candidate fingerprint and its pre-formal-review record hash was verified as `020f0835b45966b2303d4cadaba89dab5bf502171a34ec163180c8e214d0cc00`.
- Validator provenance accepted: `P17-V01` validated the exact same candidate fingerprint and its record hash was verified as `bd74680cb03d624f20e69eaa8fe0eb6681091b38fa072a732891effe18843328`.
- Candidate path hashes for `BRIEF.md`, `DESIGN.md`, `docs/REQUIREMENTS.md`, `src/cam-contract.js`, `src/scene.js`, `src/app.js`, `src/screenshot-contract.js`, `index.html`, and the three focused P17 test files matched both independent receipts.
- Supplied photo hashes matched the design record: `1-Photo-1.jpg` `8604131d1b6ba3e636492a964d0c3d92811041bbf93696afefe0a8a20a976f93`; `2-Photo-2.jpg` `d740f4e252e0bd1636dd674480c865949c3dbde21c6c6e2522d3a4e602c362ec`; `3-Photo-3.jpg` `8d12c39427823ff36c4205e70716db6df1f166aab87d113b7a0a767bb7f079fe`.

### Requirement traceability

| Requirement / invariant | Formal review disposition |
|---|---|
| `REQ-009` six permanent caps | Deterministic pass: scene/test surface reports exactly six permanent rod-end caps and no removable-cap/service-cap wording. Visual confirmation remains blocked. Cap socket fit, retention, insertion force, wear, and variability remain `PHYS-007`. |
| `REQ-010` fixed inner plates | Deterministic pass: contract and scene keep both inner rotations at zero and name fixed grounded inner plates/yoke. Visual confirmation remains blocked; actual fixture stiffness and bench/hand reaction remain future CAD/physical work. |
| `REQ-011`, `CON-009` opposite outer rotation / one relative twist | Deterministic pass: `alpha_left = -theta_rel/2`, `alpha_right = +theta_rel/2`; sampled reconstruction shows both rod ends coincident with maximum delta `4.440892098500626e-15` and maximum skew `3.552713678800501e-15`. This is not bevel/differential hardware proof. |
| `REQ-012` size hierarchy | Deterministic pass: `64 mm > 60 mm > 50 mm`. The critic's visual-affordance concern remains pending browser/user review, not a source blocker. |
| `REQ-013` ground/reaction path and lock concept | Deterministic pass for concept only: grounded yoke/detent naming and lock reducer freeze at `54 deg`; UI text keeps physical lock force and self-lock pending. Bevel axes, teeth, bearings, torque path, contact normals, release effort, creep, and wear are unresolved future work. |
| `REQ-014` simulator-first | Pass for scope: no P17 CAD, STEP, 3MF, slicer, or print artifact is accepted or authorized by this iteration. |
| Simulator reduced inner span / photo-driven spacing issue | Deterministic pass as provisional simulator geometry: `18.5 mm - 15.9 mm = 2.6 mm` surplus, within the `<= 4.0 mm` target. This is not a CAD dimension. |

### Critic-risk disposition

- Opposed-bevel/differential display: non-blocking for simulator delivery because the UI and critic record label it as a concept and tests enforce the numeric 1:1 opposite relationship. Blocking for later CAD/mechanism acceptance until real hardware geometry and torque path are designed.
- Ground/reaction path: non-blocking for simulator delivery because fixed inner guide/yoke representation exists. Blocking for later physical force claims until fixture, anchoring, stiffness, and load transfer are designed and tested.
- `18.5 mm` wording: non-blocking for PR delivery if the handoff/PR text calls it a provisional simulator target. It must not be presented as a finished CAD dimension.
- Primary grip hierarchy: deterministic pass, but browser/user visual review must confirm the right primary plate is actually obvious in rendered views.
- Cap service/fit: simulator pass only. No physical cap fit, retention, or assembly claim is accepted.
- Lock depiction: simulator pass only. No force, self-lock, creep, vibration, wear, or release-effort claim is accepted.

### Acceptance decisions

- Deterministic simulator acceptance: accepted for the joined candidate fingerprint. `npm test --workspace projects/xt60-bend-jig` passed `18` tests, `npm run build --workspace projects/xt60-bend-jig` passed, `git diff --check` passed, and an independent module probe found zero sampled rod collisions with minimum rod gap `11.46555297129437 mm`.
- Visual/runtime acceptance: blocked, not accepted. `P17-V01` could not run browser screenshots, canvas-pixel checks, console inspection, or interactive UI exercises because the Browser plugin reported no available browser surface.
- PR delivery for user review: authorized as a conditional simulator-review PR only, with the browser-validation blocker and physical/CAD gaps stated explicitly. This does not lower the simulator-first design requirement; the user still must review live motion before CAD/print work.
- CAD/print start: not authorized. No P17 CAD, STEP/3MF, slicer, print, cap-fit, lock-force, self-lock, heat, wear, springback, bevel hardware, or assembly work may begin from this gate.

### Dist bundle disposition

`dist/xt60-bend-jig.bundle.js` exists and rebuilds successfully, but it is ignored by `projects/xt60-bend-jig/.gitignore` as reproducible runtime output. Source, tests, `index.html`, and lockfile/workspace scripts are authoritative for review. No repository policy found in this gate requires committing or hashing the generated bundle as a tracked artifact.

### Commands and evidence

- `git rev-parse HEAD` and `git branch --show-current` -> `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1`, `codex/xt60-p17-counter-twist`.
- `shasum -a 256` over critic/validator candidate paths, `REVIEW.md`, `VALIDATION.md`, and supplied photos -> matched hashes listed above and in the independent receipts.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm test --workspace projects/xt60-bend-jig` -> `18` passed, `0` failed.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm run build --workspace projects/xt60-bend-jig` -> built `dist/xt60-bend-jig.bundle.js`, `527.8kb`.
- `git diff --check` -> passed.
- `git check-ignore -v projects/xt60-bend-jig/dist/xt60-bend-jig.bundle.js` -> ignored by `projects/xt60-bend-jig/.gitignore:12:dist/`.
- Static review of `src/cam-contract.js`, `src/scene.js`, `src/app.js`, `index.html`, and focused tests.
- Read-only module probe over sampled `theta_rel` values `0, 13.5, 27, 44, 54` -> max reconstruction delta `4.440892098500626e-15`, max skew `3.552713678800501e-15`, zero sampled collisions, six permanent caps, valid diameter hierarchy, `2.6 mm` provisional inner-span surplus, and locked state frozen at `{ thetaRel: 54, locked: true }`.

### Next action

Deliver the branch in a concise PR for user simulator review, clearly marking browser visual/runtime acceptance as blocked and CAD/physical acceptance as not started. When a browser surface is available, rerun only the visual/runtime portion of `P17-V01` against the same candidate fingerprint or a newly fingerprinted repair candidate. Begin P17 CAD only after the user reviews and accepts simulator motion.

## Design-owner self-scope note

`P17-D01` produced the architecture contract and initialized this review file. It did not implement, validate, critique, or approve the future candidate.

## User review disposition — `2026-08-24`

The user rejected the live simulator because its holes or slots appeared to
move with the animation and directed the project to skip simulation. This
observation supersedes the conditional simulator-review delivery gate. The
candidate is not accepted as product direction or CAD input; no repair or
browser rerun is requested.
