# Pattern backlog and first missing-pattern gate — PB-DES

Baseline `191cb37119f9a4e4d23112ecd5bc0d18f0daec86`; the19-file
`inputs/baseline.sha256` verified, SHA
`9d08cea42a798c548d54528cb28f715db5335b51d1f06e5cc37b534aeef832bb`.
Current SCAD SHA `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
The user requests continuation of the original roadmap one item at a time,
starting with remaining patterns, and offers a photo if needed.

## Selected gate

Current Diamond has broad flat crowns and low crossing grooves: it covers the
blunt-diamond family. The first missing distinct item in the original V2 order
is Recessed diamond: inward pockets with high crossing ridges. This distinction
is explicit in the historical R4 contract; no photo is needed to propose it.
The next deliverable is an isolated analytic comparison, not new container CAD.

| ID | Contract / acceptance |
| --- | --- |
| PB-01 | Restore the full roadmap in FEATURE_BACKLOG; separate delivered geometry, partial overlap, missing work and rejected prototype evidence. |
| PB-02 | Compare actual current Diamond mathematics with the documented recessed-pocket proposal at identical pitch, depth, phase, lighting and scale. |
| PB-03 | Show only Size/Depth controls, exact inputs and sliders; true-proportion section plus clearly labelled depth-enlarged section. No invented third motif. |
| PB-04 | The user can identify high centers/low crossings versus low centers/high crossings from shape, then pass/reject the proposed pocket appearance. |
| PB-05 | Label the page as an analytic appearance study; no compiled/STL/download/print-ready claim. Main app, source, internals, worker and dependencies stay unchanged. |
| PB-06 | Browser-local computation remains; user accepts waiting for real compilation later. No server compilation, Figma, printer, public release or main merge. |

Historical pattern names and pixel hashes do not prove distinct geometry.
R16/R17/R21 failures are counterexamples; their renderer code is not a reusable
validated implementation. Fixed source/model geometry remains separately accepted.

## Bounded task DAG

`PB-DES -> PB-IMP -> (PB-VAL || PB-CRIT) -> PB-REV -> user appearance gate`.
PB-DES owner `/root/pattern_family_design`: exclusive BRIEF/DESIGN,
`docs/FEATURE_BACKLOG.md`, and `inputs/design-extra.sha256`; baseline19 plus
declared decisive history. Done: frozen comparison contract and complete mapping.
PB-IMP workstream `/root/pattern_direct_implementation`: exclusive
`preview/recessed-diamond-study/`; no production app/source writes. Done: runnable
study and implementation receipt against frozen design/source hashes.
PB-VAL: distinct validator, exclusive `tests/node/recessed-diamond-study-independent.test.mjs`
and validation receipt/scratch; independent math/state checks and actual browser.
PB-CRIT: distinct critic, read-only source/screenshots, exclusive critique receipt;
test no-caption relief recognition, truthful scale and mobile usability.
PB-REV: distinct formal reviewer, review receipt only; join exact candidate and
evidence fingerprints. Root binds remaining identities/manifests before dispatch.
Pending CAD/additional-family tasks are unscheduled until the user gate passes.

Root owns mutable scheduling/continuity and may copy reviewed study files to
isolated `/pattern-study/` on existing8453; preserve the main app's six files.
Design ceiling12min, workers15min/checkpoint5min, strong/high design/acceptance,
balanced/medium prescribed implementation, max3 workers and2 focused repairs.
Stop on ambiguous appearance, baseline drift, duplicated visual motifs or scope
expansion. Every return binds paths/hashes, commands, findings and next action.
