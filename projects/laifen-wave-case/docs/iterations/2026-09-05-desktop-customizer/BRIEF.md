# Cylindrical Container Customizer — desktop iteration

Opened 2026-09-05 by CC-DES-01 (`/root/desktop_design`). Baseline commit
`fef4f264d6af6904e8debd99d522ce186bcec49d`. Design contract only; implementation,
independent critique, validation and formal review remain pending.

The user selects visual option 2, a section-oriented container workspace, and
requires real Generate and Reset actions. Everyday users describe the space
they need without calculating CAD relationships. Sequence: inspect existing
container → edit four dimensions → Generate → inspect actual compiled result
in 3D or Cutaway → download the current STL. The page is canvas left, settings
right on desktop, with no introductory title/subtitle consuming workspace.

## Requirements

| ID | Contract and evidence gate |
|---|---|
| CC-01 | Desktop two-pane layout; visible dimensions and action footer without page scrolling at 1280×800 and 1440×900. Screenshot and bounding-box inspection. |
| CC-02 | Four plain inputs: Inside diameter, Inside height, Wall thickness, Top & bottom thickness. Exact adapter and friendly constraint tests. |
| CC-03 | Preserve the current tall, two-piece screw-container topology and preset geometry. No short-lid reinterpretation. Exact default snapshot comparison. |
| CC-04 | Generate, active-job Cancel, Reset dimensions, Reset view, and current exact-byte Download have distinct truthful behavior. Adversarial async lifecycle tests and real browser generation. |
| CC-05 | 3D/Cutaway uses actual compiled STL; clipping is display-only. On-canvas measurements describe generated values. Visual inspection plus unchanged download-byte hash. |
| CC-06 | Existing useful choices remain: automatic/explicit lid height; drains Off/Top/Bottom; assembled/body/lid/print-layout outputs. Smooth only; Diamond stays unavailable. |
| CC-07 | Keyboard-operable labeled controls, visible focus, inline associated errors, readable busy/stale states, responsive mobile fallback. Browser inspection. |

Millimetres; source Z is container axis. No new material/printer assumptions.
Existing source and downloaded geometry remain authoritative; physical fit,
thread strength, slicing and print acceptance remain unproven. The example of
3 mm walls is unsupported by the unchanged screw geometry and must fail
truthfully, never silently become thicker. Historical Laifen requirements are
preserved; this is a new generic UI adapter, not a new printable CAD release.

## Bounded DAG

`CC-DES-01 → CC-IMP-01 → (CC-CRIT-01 || CC-VAL-01) → CC-REV-01`.
Root owns orchestration and continuity indexes. Every subsequent task must
receive a frozen candidate manifest and distinct owner before execution.

CC-DES-01: design role; done gate is the numeric/lifecycle contract in DESIGN.
Reads this project's source, tests, requirements, experience, decision index,
active handoff and option 2 reference. Exclusive writes BRIEF and DESIGN in
this iteration. Forbidden code, CAD, other projects, services and deployment.
Strong/high bounded design reasoning; approximately five-minute checkpoint,
1,500-word narrative target, one worker, initial plus two focused repairs.
Stop for baseline drift, missing mandatory reference, or required mechanics
change. Source/schema/worker must not change in the implementation scope.

The root will assign implementation (UI, adapter, lifecycle, focused tests),
independent read-only critique, independent validation, and formal review with
disjoint writes and explicit ceilings. No live-route deployment follows from
this design receipt.

## Frozen inputs

SHA-256 path-and-content manifest follows in DESIGN; mutable PROJECT_STATE,
NEXT_AGENT, CURRENT, handoff and evidence records are context, excluded from
gate fingerprint. The selected option-2 image is a visual reference, not
authority for container dimensions or generation semantics.
