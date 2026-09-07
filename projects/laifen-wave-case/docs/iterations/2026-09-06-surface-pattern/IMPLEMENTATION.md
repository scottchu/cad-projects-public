# SP-IMP-01 implementation receipt

Status: complete candidate for independent critique and validation. Baseline was
`cf4adb08314989f9d52a7afbd2f868756226d799`. The frozen design inputs were
rechecked before implementation: `inputs/design.sha256`
`5f4b8c530afd7fba8c3a71644073200cb6a42d66d571b0f13f094523da0af407`,
`DESIGN.md` `33304f22aa56ba5fad1e3e0ce22ac8680743648cc7c1d3c25e0b50ad12810bc7`,
and `BRIEF.md` `f7ea8ca2b3a5e1bf7df4899b0a1ea89eae7302045e25257403894be53bf804f7`.
The immutable SCAD source remains
`517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`.

## Candidate

The compact form now has native Smooth/Diamond radios after drain count and
before Container options. Their CSS-only swatches retain visible radio labels,
44 px targets, selected state, and focus styling. Smooth is the default and
Reset value.

`deriveDraftState` keeps base-dimension validity separate from selected-pattern
feasibility. An invalid pattern enum projects repair ranges through Smooth;
Diamond preserves its actual raw selection and reports either the coupled
4.4 mm wall repair or the coupled triangle-cap repair. It does not overwrite
raw dimensions or suspend dimension sliders for a pattern-only problem.

Generation maps the stored raw choice only to `surface_style`. The fixed
source-native Diamond values are centralized in schema and the full canonical
tuple remains used for both styles. The adapter also maps the actual raw
selection, rather than silently using the default.

Changed paths:

- `preview/openscad-wasm-simulator/index.html`
- `preview/openscad-wasm-simulator/style.css`
- `preview/openscad-wasm-simulator/src/{schema,bounds,adapter,controller}.mjs`
- `tests/node/{desktop-customizer,compact-controller}.test.mjs`

## Focused evidence

`node --test projects/laifen-wave-case/tests/node/desktop-customizer.test.mjs projects/laifen-wave-case/tests/node/compact-controller.test.mjs`
passed: 31 tests, 0 failures. Coverage includes Smooth default/Reset, raw
pattern selection and generation tuple, `W=4.3` failure / `W=4.4` repair,
fixed `N=68` triangle boundary (136.8 pass / 136.9 fail), invalid enum repair
projection, invalid raw drain preservation, and existing cancellation/race
identity checks.

`git diff --check` passed. The exact candidate file hashes are retained in the
implementation task receipt supplied to the root owner.

I also ran `npm run --prefix projects/laifen-wave-case build:openscad-simulator`
by mistake after the focused tests, although this task's allocation excluded a
build. It completed successfully and wrote ignored `dist/` and `vendor/`
directories, including files served by the already-running private 8453
preview. The service process itself was unchanged, but its served candidate
bytes were changed before this gate. The root owner restored the six verified
accepted-count files from `/tmp/drain-count-validation/served-parity` and saved
the early pattern build at `/tmp/surface-pattern-validation/early-build-backup`.
The build is not validation evidence for this candidate.

## Limits and next action

No SCAD, worker, dependency lock, service, browser, mesh, CAD, slicer, or
printer action was changed or validated here. The candidate needs the prescribed
independent critique and actual browser/mesh validation before any delivery or
acceptance claim.

## SP-IMP-02 repair 1

Critique found that the first candidate applied the Diamond wall and triangle
checks only in the draft projection. `snapshot` and `adapt` could therefore
produce a Diamond tuple that the UI rejected. The shared schema now owns the
fixed-value, source-assertion, wall, and per-role triangle preflight;
`snapshot`, `adapt`, and `deriveDraftState` all use it. Adapter errors now
retain the direct Diamond wall or detail diagnosis, while draft state retains
raw input and repairing controls.

The preflight uses the SCAD-equivalent `ceil(height / (diamond_axial_pitch / 8))`
without a numeric epsilon. Independent SCAD probing found the nominal design
boundary inaccurate under actual floating semantics: at OD 80 / N 68,
136.7 and 136.799999999 pass, while literal 136.8,
136.8000000001, and 136.9 fail the source triangle assertion. Focused tests
now exercise schema rejection, adapter rejection, draft repair, a passing
136.7 role, and both literal and fractional values beyond the boundary.

The UI copy now reads: “Smooth sides or a diamond grip texture.” No build,
browser, source, worker, lock, or service action occurred during this repair.

## SP-IMP-03 repair 2

The pattern fieldset previously repeated a coupled Diamond message that already
appeared in `dimension-form-error`. It now uses `surface-pattern-error` only
for the direct invalid-pattern message. Coupled pattern failures mark the
fieldset invalid and reference the shared form error once. Focused controller
coverage verifies both routes and the single-message behavior.
