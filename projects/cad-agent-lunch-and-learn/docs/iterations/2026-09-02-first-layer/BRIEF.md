# Slide 5: explain the first-layer problem

User feedback: "i still don't understand 5/18". Current slide shows a floating plate and a translucent plate with an orange contact foot; prior visual/narrative passes do not resolve this feedback. Explain the visible physical relationship and why the preview observation leads to a source change. Use visible content alone, with slide 4 -> 5 -> 6 continuity. No imagined narration, audience questions or controls.

Baseline: branch codex/cad-agents-lunch-and-learn, parent d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c. HTML 6ce17971db1871cc4bc2c8958359cc6a28e52e16b875f5dae4e838a876a41445. Immutable copies and SHA256 list in INPUTS.sha256. Scope: slide 5, its two read-only Three.js scenes, scoped CSS, offline/print equivalents and necessary existing-check changes. Other 17 slide sections, fit scene, navigation and real source facts must remain unchanged.

Primary evidence: XT60 EXPERIENCE 2026-08-22 missing-half/floating early-layer observation. It records large plate faces above bed, incomplete/floating early layers, and contact-land/source-orientation repair. It does not supply an exact validated before/after toolpath or proof of successful physical print. Author must verify supporting sources if an exact geometry claim is needed. Do not imply that adding a central foot magically supports a floating plate. Read-only teaching diagrams must identify schematic status in ordinary language.

## Task DAG and ownership

F-I (writer, strong/high): design and implement the smallest clear slide 5 explanation. Dependencies: frozen baseline. Exclusive writes: build.mjs, simulator.mjs, generated index.html, test/deck.test.mjs only if needed; DESIGN.md, IMPLEMENTATION.md, CANDIDATE.sha256, approved append-only project experience/decision entry. Reads: project and XT60 primary source records. Forbidden: production CAD, slicer/printer, hosting configuration, dependencies/locks, Git operations. Done: source-grounded visible explanation, build/check pass, immutable candidate manifest and receipt.

F-C (critic, strong/high): independent visible-content comprehension review after F-I. Read rendered slides 4,5,6 before design/notes; review desktop/compact/mobile/print slide 5. Exclusive write CRITIQUE.md. Done: name what the slide actually communicates, identify unexplained jumps and mark pass/fail. No source edits.

F-V (validator, strong/high): independent targeted browser and factual validation after F-I. Exclusive write VALIDATION.md, captures in /tmp/cad-first-layer-validation. Check exact candidate, existing tests, real offline WebGL, fallback, desktop/compact/mobile/print, other 17 sections/navigation/fit unchanged. Verify primary-source claims and schematic boundaries. No source edits.

F-R (formal reviewer, strong/high, distinct identity): after written F-C/F-V verdicts join exact candidate receipts and directly sample relevant pixels; exclusive write REVIEW.md. Done: accept exact candidate or return concrete unresolved blocker.

Root coordinates manifests, status and final private delivery. Each receipt states status, verified hashes, paths, commands/results, severity, requirement coverage, remaining risks and next action. All task inputs use INPUTS.sha256 and later exact CANDIDATE.sha256; mutable status and receipts excluded. At most three workers active. Initial attempt plus two narrow repairs maximum. Qualitative ceilings: writer 8 minutes/8k tokens; critic and validator 5 minutes/5k each; reviewer 3 minutes/3k; receipt <=1000 words. Stop on source uncertainty or scope expansion; do not invent facts. Gates invalidate only when their declared candidate inputs change.

## Repair 1 — factual boundary and plain-language response

F-V found that the initial left caption incorrectly attached the schematic's completely empty first-layer band to the historical preview. EXPERIENCE establishes faces above the bed and incomplete/floating early layers, not a broad face above the entire first-layer thickness. F-C also found the secondary contact-surface wording opaque. Repair scope is copy only: caption uses the literal observation, orange-band labels explicitly identify the schematic, and the source geometry change is described as the small raised areas where plates touch. Geometry, cameras, layout, other slides and source facts stay unchanged. Prior source and manifest are preserved under /tmp/cad-first-layer-repair1-baseline; initial HTML 1a31ba1fc5b2f1b45773f69a902be2527aa75987f9ee41d46c059027bc0ec1e6, manifest 80d2e8905cd9fc3bc848a0eb4c427859d7e4ce86f9a43dce3295d63404d393c8.
