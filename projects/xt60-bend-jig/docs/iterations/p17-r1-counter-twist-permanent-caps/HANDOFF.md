# P17 R1 handoff

Status: deterministic simulator candidate complete and conditionally approved
for user review; independent browser visual/runtime validation remains blocked.

## Completed by `P17-D01`

- Opened iteration `p17-r1-counter-twist-permanent-caps`.
- Recorded frozen input manifest `b71a2bf9aafe949618ef9a1356bce54eae1241b19c24e4e539849d99209f1293`.
- Selected the counter-twist simulator architecture in `DESIGN.md`.
- Added P17 requirement IDs and supersession notes in `docs/REQUIREMENTS.md`.
- Appended exact physical observations and photo references in `docs/EXPERIENCE.md`.
- Added `ADR-0003` and updated the decision index.
- Initialized pending validation and review records.

## Changed paths

- `docs/iterations/CURRENT`
- `docs/iterations/p17-r1-counter-twist-permanent-caps/BRIEF.md`
- `docs/iterations/p17-r1-counter-twist-permanent-caps/DESIGN.md`
- `docs/iterations/p17-r1-counter-twist-permanent-caps/VALIDATION.md`
- `docs/iterations/p17-r1-counter-twist-permanent-caps/REVIEW.md`
- `docs/iterations/p17-r1-counter-twist-permanent-caps/HANDOFF.md`
- `docs/REQUIREMENTS.md`
- `docs/EXPERIENCE.md`
- `docs/decisions/ADR-0003-p17-counter-twist-permanent-caps.md`
- `docs/decisions/README.md`

## Not changed

No CAD/Python source, generated CAD artifacts, simulator JS source, tests, package files, root config, git state, or PR was intentionally changed by this design task.

## Original design-to-implementation action

Assign `P17-I01` to implement the simulator only. The implementer should read `BRIEF.md`, `DESIGN.md`, `docs/REQUIREMENTS.md`, `docs/EXPERIENCE.md`, `docs/decisions/ADR-0003-p17-counter-twist-permanent-caps.md`, and the current simulator files before editing.

The first implementation candidate must make these defects fail if present:

- same-direction outer rotation;
- inner plate rotation;
- left/right rod-end mismatch or skew;
- copied slot geometry with only animation sign flip;
- missing ground/reaction path;
- missing or overclaimed lock concept;
- wrong plate diameter hierarchy;
- removable-cap wording;
- cap count other than six permanent caps;
- P13-sized inner-span surplus retained.

No P17 CAD, STEP, or 3MF should be generated until the user reviews the simulator motion.

## IMPLEMENTATION — `P17-I01` / `/root/p17_implementation`

Status: implementation candidate complete; not self-approved. Independent critic, validation, and formal review remain required.

### Verified frozen input fingerprint

- Baseline commit: `7ca4d99ded0c0ccb0f67c0ee56494aa932596da1` plus the completed P17 design-document working tree.
- Frozen contract hashes verified before editing: `BRIEF.md` `32ffa429ccf4e382dacb0bfaac897b31eec3db3d387525a8a4b719b314800d05`; `DESIGN.md` `b421db860cebe581f24c28361796e908048126e7cc515e60f42ddd5ffbdf8989`; `REQUIREMENTS.md` `99746664776c4709c16d6c5acc5cfba08f5168dafa8e4b175a4d760330360591`; baseline `cam-contract.js` `a58f5057116027bab0f1678f525d61f457c1d5a85774ba0727f666979d55eca3`; baseline `app.js` `f9961b6b9d0a2dc27cfadb32371fb004ff499864ed4c32a216e1dfe8dce584a4`; baseline `scene.js` `3edc5d5166de72cf3901dd7202c6e9d590bcc6a8e6c1624bfad91fe4563388b2`; baseline `screenshot-contract.js` `56e57b3b7a8e718fec634ed9d4db84ee7b30e5d87474866bf83b680c654f3d70`; baseline cam tests `cff9ef1dc329f42a4439c92911cc35536c187a8e2c9fb6de9cbaf1d8705941a4`; `index.html` `a7aa9770d4ea5b3473f1ab43bd1007751fc2736bb5a35084f78d87b6866e1c35`; `styles.css` `1f7641da61b01c0ae00b9311cc8ee802d00007cbefdf34c63472c5ba689fb97f`; project `package.json` `f2cc0542c9056bf85119c3d4394d3e7e74a44676bb972d315a9c3c21e92b250e`; root `package-lock.json` `a5bfa9bb8ed1028deb0086c001c9c5eca714de9dc115b5da5426f97a8e4fa9a5`.
- Sorted frozen-input manifest hash: `0cd6f127b431ee0038cfe37b276b416e57f843b7a7c611e4491cbb23d3fa5ab0`.

### Candidate and coverage

- Replaced the P13 shared-shaft contract with one relative twist (`0..54 deg`), `alpha_left = -theta_rel/2`, `alpha_right = +theta_rel/2`, two fixed zero-rotation inner guides, signed side-local complementary slots, world reconstruction, and sampled skew.
- Rendered 50 mm fixed inner plates joined by a grounded yoke; 60 mm secondary left and 64 mm primary right outer grip plates; straight fixed guide tracks; a grounded-carrier opposed-bevel/idler 1:1 relation concept; and a grounded detent/hard stop on the primary right plate.
- Rendered and asserted six permanent end caps, reduced the simulator clear span to `18.5 mm` (`2.6 mm` surplus around the `15.9 mm` XT60 envelope), retained the `3 x OD4 x 50 mm` purchased rods, and kept the 90-degree bend as a target.
- Lock reducer reaches and freezes only the `54 deg` hard-stop pose. UI explicitly calls this a kinematic lock concept and leaves lock force/self-lock, cap fit, heat, and other physical behavior pending.
- Updated P17 screenshot presets: `open`, `mid`, `closed`, and `locked`.

### Candidate hashes

Candidate fingerprint (sorted P17 contract plus candidate source/test/browser paths): `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.

- `src/cam-contract.js` `94d76a35e3503fc26f577e12063535843e3db20cc77f667c817f0d4ecd352ee0`
- `src/scene.js` `3665be98ba930ec3c67c3a4618c4b7c7172e714b65755ed29e389fa5e2fd0756`
- `src/app.js` `5404a345b357f8cfa176e15339c03451f5c201240fbb22ede4d1c6c781f984f5`
- `src/screenshot-contract.js` `4060f122fa1227ecbc0b57caf2cb84463d51c3e101b1b763f69ef326cc262390`
- `index.html` `04497a5facaef1ae681e57888d114633fd119904a147e80f2cc965928aadb0bf`
- Focused tests: `tests/cam-contract.test.mjs` `e2b5b97550cad16f8d49b8763de9fb59ae0fa42421204d1031a42ac93233ac9f`; `tests/screenshot-contract.test.mjs` `d981af0a2a66c738d6cee65c3cd72b2070630b0eb5c0d9cdac24fdaa348734e1`; `tests/simulation-contract.test.mjs` `1f73e1f38286a2aeb8bd0e12f308a98182ef739f25676f979a4575152c38c902`.

### Commands and results

- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm ci --ignore-scripts` — installed the lockfile dependencies because Node/npm were absent from `PATH`; no lockfile mutation.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm test --workspace projects/xt60-bend-jig` — `18` passed, `0` failed.
- `PATH=/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH npm run build --workspace projects/xt60-bend-jig` — built `dist/xt60-bend-jig.bundle.js` successfully.
- `git diff --check` — passed.

### Remaining risks and next action

This is simulator-only kinematic evidence. It does not prove bevel/differential geometry, lock force, self-lock, cap retention/fit, stiffness, heat, wear, or printed assembly. Assign `P17-C01` and `P17-V01` against this candidate fingerprint, then require `P17-R01` to join their independent receipts before user motion review. Do not generate CAD or print artifacts yet.

## Independent gates and closeout

- Critic `P17-C01`: pass/no-blocker for simulator review only. It confirmed
  fixed-inner/opposite-outer intent, complementary tracks, six permanent caps,
  the diameter hierarchy, provisional reduced span, and bounded lock wording.
  It explicitly did not accept real bevel hardware, fixture stiffness, cap fit,
  or physical locking.
- Validator `P17-V01`: deterministic checks passed (`18` tests, build,
  zero practical reconstruction skew, no sampled rod collisions). Browser
  visual/interactive validation is blocked because no Browser-plugin surface
  was available; no screenshots or live interaction evidence were captured.
- Formal reviewer `P17-R01`: conditional pass for PR delivery as a
  simulator-review candidate. It accepted deterministic simulator evidence,
  kept visual/runtime acceptance blocked, and did not authorize CAD or print
  work.
- Root closeout `P17-H01`: updated `PROJECT_STATE.md`, `NEXT_AGENT.md`, and this
  handoff. The development server command and user review gate are durable.

### Current candidate

- Fingerprint:
  `8c57e19ac3ef1f46a4bcab299a679935c638daea0dfe5e0a6fde106f243cb537`.
- Branch: `codex/xt60-p17-counter-twist`.
- Tests: `18 passed`, `0 failed`.
- Build: passed; `dist/` remains ignored reproducible output.
- Whitespace: `git diff --check` passed.

### Acceptance boundaries

- Deterministic simulator: accepted.
- Independent visual/runtime: blocked and not accepted.
- CAD/STEP/3MF/slicer: not started and not authorized.
- Physical: not accepted.

### Next action

Have the user review
`http://127.0.0.1:4173/projects/xt60-bend-jig/` while the local dev server is
running. Rerun the browser portion of `P17-V01` when a browser surface is
available. Begin a new CAD/mechanism iteration only after user acceptance of
the counter-twist motion.
