# SP-CRIT-01 — independent surface-pattern critique

## Candidate 03 source gate

**Verdict: SOURCE PASS; browser/visual acceptance remains pending.**

Candidate manifest `inputs/candidate-03.sha256` has SHA-256
`412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`;
all 23 declared paths passed `sha256sum -c` from the repository root. The
revised `BRIEF.md` and `DESIGN.md` hashes are respectively
`5df06828d9794d6fd75e0cce4412858f4ded86ef6d3f6241f47090fd77f3d5bd`
and `176bb99dc05b08b52ae757682b8f70ae1ccdf8a3e470a89476dfad4701e3d924`.
The immutable SCAD remains
`517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`;
the pinned worker and dependency lock also retain their declared hashes.

No open source finding remains from this critique. `snapshot()` now invokes a
single schema-native Diamond preflight for the fixed pitch, arc, depth and
phase tuple and for the source count, plateau, slope, shell, thread-wall and
per-role triangle assertions. The adapter and draft projection both pass
through that authority. Its segment calculation is the unchanged source
expression `ceil(height / (4.8/8))`, with no epsilon or rounded direct-entry
exception. The revised evidence boundary is truthful: the N=68 browser slider
ends at role height 136.7 mm, while literal 136.8 mm and values immediately
above it are rejected by the same predicate before generation.

The Candidate 02 error duplication is also resolved. A direct missing/invalid
pattern uses only `surface-pattern-error`; a Diamond coupled failure uses the
single shared `dimension-form-error`. The fieldset remains invalid and its
runtime `aria-describedby` selects only the applicable error node, while the
wall or size participants reference the shared coupled error. Pattern help no
longer exposes implementation/debug wording.

Source inspection covers SP-01 through SP-06: the fieldset order, native
radios, visible 44 px cards, Smooth default/Reset, fixed source-native Diamond,
preserved raw state, explicit generation, repairable 4.4 mm wall constraint,
selected-pattern intervals, all four output values and unchanged generation
lifecycle remain wired as specified. The Smooth and Diamond swatches are only
choice cues; they are not geometry evidence.

### Browser gate still required

The live browser connection closed before Candidate 03 could be captured.
Candidate 02 supplied only a fresh Smooth render and the duplicated-error state
that Candidate 03 subsequently changed. It cannot establish the repaired
error presentation, selected/focus state, responsive reachability, all four
actual jobs, or cancellation/supersession behavior for this fingerprint.

Acceptance therefore still requires current Candidate 03 evidence at
1280x900 and 390x844: default Smooth; Diamond selection with preserved values
and stale/download invalidation; wall 4.3 error and 4.4 repair; strict
triangle-cap error and repair; focus-visible cards; Generate/Cancel/Reset and
all four output jobs; and the held-real-worker Cancel/late/superseded-result
sequence. Chromium evidence may close Chromium coverage only. Native Safari
remains explicitly unverified after `cgWindowNotFound`; screenshots cannot
establish full assistive-technology behavior or physical print acceptance.

## Candidate 01 source checkpoint

**Verdict: NEEDS REPAIR before browser enablement.**

Candidate manifest `inputs/candidate-01.sha256` has SHA-256
`3b1eb72f62c4b8b6031f25e1f861506498010bb6ee7dc7e284636914075a1b13`;
all 23 declared paths passed `shasum -a 256 -c` from the repository root.
Baseline is `cf4adb08314989f9d52a7afbd2f868756226d799`. Immutable SCAD remains
`517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`;
the worker and dependency lock also match their baseline hashes.

### P1 — the schema accepts Diamond jobs that the UI says are impossible

`deriveDraftState()` checks the 4.4 mm Diamond wall and 250,000-triangle
limits, but `snapshot()` does not check any Diamond-specific source assertion.
`adapter.mjs` calls that unguarded snapshot directly. A non-UI caller can
therefore obtain generation values for Diamond with wall 4.3, an oversized
patterned role, or even changed Diamond pitch/depth values allowed by the broad
numeric schema ranges. Those values are deferred to immutable SCAD assertions.

This violates SP-05's requirement to preflight every Diamond assertion and
DESIGN's requirement that the fixed relationship-B facts remain in the
schema/source contract. UI projection and job validation need one native
Diamond predicate. `snapshot()` should reject a non-fixed Diamond tuple and
the same source-equivalent wall/count/plateau/slope/shell/triangle failures;
`deriveDraftState()` should project that authority into repairable UI issues
without becoming the only guard.

### P1 — the triangle guard has a direct-entry gap above exact boundaries

The browser estimate uses `ceil(height / 0.6 - 1e-9)`, whereas immutable SCAD
uses `ceil(height / 0.6)`. The subtraction makes a small interval immediately
above every 0.6 mm boundary appear feasible. At N=68, for example, a direct
entry producing role height `136.8000000001` is treated like 136.8 by the UI,
but SCAD advances to the next axial segment and exceeds 250,000 triangles.
The focused tests cover only 136.8 and 136.9, so they do not catch this exact
input path.

Compute the maximum permitted role height algebraically from the integer
triangle budget and compare the unrounded input directly. This keeps 136.8
inclusive, rejects any larger exact value when N=68, and lets the 0.1 mm slider
project the same boundary without a tolerance that broadens the source set.

### P2 risk to inspect after repair — duplicated coupled error announcement

For a pattern-coupled issue, the controller copies `draft.formError` into
`surface-pattern-error`, while the fieldset's `aria-describedby` references
both that node and `dimension-form-error`. This can present and announce the
same error twice. The repaired browser state should show one clear message near
the affected choice, and accessibility inspection should confirm the fieldset
or radios receive it once.

## Source UX coverage

The placement and interaction model otherwise match the selected gate: one
visible Surface pattern fieldset after drain count, native labelled Smooth and
Diamond radios, 44 px cards, distinct swatches, Smooth default/Reset, no extra
pattern parameters, and a pattern change routed through the existing explicit
edit/invalidation path. Raw dimensions, drains/count, output and Auto are not
mutated by radio changes. The canonical generation tuple includes
`surface_style` plus the existing fixed Diamond pitch/arc/depth/phase values,
so job identity distinguishes Smooth from Diamond. Existing epoch, timeout,
fresh-worker and current-download wiring is unchanged in source.

This does not approve browser behavior, compiled meshes, service bytes, CAD,
slicing, printability, grip or physical acceptance. The accidental implementer
build is excluded from critique evidence; root restored the previously served
six assets and recorded their parity.

## Evidence and next action

The critic read current project continuity, requirements, experience/decision
records, active BRIEF/DESIGN/IMPLEMENTATION/HANDOFF, candidate HTML/CSS,
schema/state/controller/adapter/lifecycle paths, focused tests, and immutable
SCAD assertions. Commands were explicit Homebrew `rg`, `sed`/`nl`, Git
read-only diff/status inspection, and SHA-256 verification. No tests, build,
browser, service, source, CAD or artifact mutation was performed.

Changed path: this `CRITIQUE.md` only. Repair the two P1 guards, freeze a new
candidate, then run the prescribed current screenshots and eight-step browser
flow at 1280x900 and 390x844. The final audit must number each captured step and
tie UX/accessibility findings to those accepted screenshots.
