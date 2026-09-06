# CC-REV-01 — formal review of C2

Status: **PASS for local UI/runtime development delivery**. This does not
approve a printable CAD release or the edited assembled STL. Owner:
`/root/desktop_formal_review`, distinct from designer, implementer, critic and
validator. Review date: 2026-09-05 (America/Toronto).

## Verified candidate and provenance

Baseline `fef4f264d6af6904e8debd99d522ce186bcec49d`; project
`projects/laifen-wave-case`; iteration `2026-09-05-desktop-customizer`.

From the repository root, ran `shasum -a 256` on both assigned manifests,
then these exact commands:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-05-desktop-customizer/inputs/candidate-02.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-05-desktop-customizer/inputs/review-join.sha256
```

All 16 candidate entries and all 7 review-join entries passed. Verified
manifest hashes respectively:

- `b57642a532d834fddeb56c938496af44a03d3635e4a748ad46ada0cf86df609c`
- `1e5fd43a409db541e8d5831a94c3b9174f882bafb87281eff400872f3b0567ed`

Read BRIEF, DESIGN, IMPLEMENTATION, VALIDATION, CRITIQUE, project design-qa,
STATE/NEXT/HANDOFF, all new runtime modules, HTML/CSS, and focused Node tests.
Used `cat`, `tail -65` and `git diff --stat` for read-only inspection. No
browser, build, test suite, CAD generation, deployment or printer operation
was performed by this reviewer. Test results below are attributed to VAL;
visual comparison results are attributed to CRIT.

The frozen join links the candidate manifest to implementation, independent
validation, independent critique, design QA and explanatory project records.
C1's stale test hash is closed by the complete C2 manifest verification.
C1's browser timer binding failure is closed by source wrappers, the branded
timer regression and VAL's actual successful clean-reload evidence. C1's
wrong-section/drain-intersecting annotations are closed by the source anchor
repair and independent 1,881-case probe plus visual interpretation.

Browser evidence was operated by root under VAL's checklist because VAL's
session had no available browser. VAL independently interpreted captures and
parsed downloads; CRIT independently opened the selected reference and actual
render together. This is sufficient for this scoped gate, and is explicitly
not independent browser operation or user-device Safari acceptance.

## Requirement disposition

| Requirement | Review conclusion |
|---|---|
| CC-01 | Pass: canvas-left/settings-right desktop workspace, no title block, persistent actions; VAL/CRIT evidence covers 1280×800 and 1440×900. |
| CC-02 | Pass within disclosed mechanics: four plain dimensions, derived outside dimensions, explicit body/lid differences; 3 mm rejects instead of silently thickening. |
| CC-03 | Pass for preservation: exact preset comparison and unchanged frozen SCAD/schema/worker/lock; tall cap retained. |
| CC-04 | Pass: Generate reserves ownership before asynchronous identity work; cancellation/edit/reset/timeout invalidate it; verified exact byte slices enter download. Real browser interactions complement deterministic tests. |
| CC-05 | Pass for display/integrity: actual STL clipping, generated-value annotations, stale preview labeling, and unchanged default download hash across view changes. Artifact acceptance remains partial. |
| CC-06 | Pass: drains remain visible, optional Auto/manual lid and all four export shapes retained; Diamond explicitly unavailable. |
| CC-07 | Focused pass: associated errors, keyboard focus, busy/stale states and mobile reachability have evidence; no exhaustive accessibility claim. |

VAL reports 13 Node tests, 4 Python tests and the C2 production build passed.
Source inspection found no additional material UI/runtime defect requiring
another repair cycle. CRIT's final visual pass is scoped consistently with
the actual implementation, including its real tall geometry and uncapped
display clipping rather than promising exact illustrative geometry.

## Findings, boundaries and delivery

- **P2, carried artifact limitation:** edited D39/H60/W4/T4 assembled STL has
  four degenerate seam faces and fails strict manifold validation. Default,
  body, lid and print-layout samples passed VAL's measured mesh checks. This
  blocks approval of that assembled artifact as print-ready, not the scoped
  UI development delivery. Preserve exact output bytes; source diagnosis and
  repair require a separate mechanics/artifact iteration.
- **Disclosed unmet example:** the original 3 mm wall request is unsupported;
  the UI advertises a stable 4 mm minimum. Do not describe the user's entire
  container-design need as fulfilled or claim geometry redesign occurred.
- **P3:** central-axis height annotation and seam lighting remain optional
  teaching/visual polish. Neither invalidates the reviewed dimensions.
- Actual-user Safari, slicing, fit, thread strength and physical acceptance
  remain open. The inherited dependency advisory and bundle-size warning are
  recorded in setup/validation receipts; this review did not reassess them.

Only this REVIEW.md was written by CC-REV-01. Next: root may update continuity,
commit intentional changes and create the scoped draft PR. Deliver a verified
local development preview with the wall and artifact limits explicit; no
live-route replacement or print-ready claim follows from this review. Changes
to frozen inputs require rerunning affected gates.
