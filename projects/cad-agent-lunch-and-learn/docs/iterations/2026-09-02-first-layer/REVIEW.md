# F-R formal review — PASS

2026-09-02. Owner `/root/deck_review`, distinct from `/root/first_layer_writer`, `/root/first_layer_validator` and `/root/first_layer_reader`.

Accept the first-layer repair1 candidate for presentation delivery. No P1/P2 finding remains in this focused scope. This verdict addresses slide 5 and its 4→5→6 transition, not a repeated whole-deck approval.

## Exact provenance

- HTML: `c8766aeb3d0c03f0332e226b55a896bc33d52c21da0969f5a9263626cfb9dfa7`.
- `CANDIDATE.sha256`: `71673185ca5f4f88e512ae74ff7356b2247641e0290ef34443c097861d03a709`; 14/14 entries independently verified.
- `INPUTS.sha256`: `55234a74dfdb328ac82865dadacc59b3cb0021d1c7c775a9fe7029ece0ed2806`; 8/8 frozen entries independently verified.

Commands from the repository root: `shasum -a 256` on these three files, and `shasum -a 256 -c` on both manifests. All returned exit 0, matching identities and all members OK. Read BRIEF/DESIGN/IMPLEMENTATION and the written final repair1 F-C/F-V PASS sections. Both final receipts identify this exact candidate; the initial factual FAIL remains historical.

## Direct review and finding disposition

Inspected full-size desktop slides 4 and 6 from `/tmp/cad-first-layer-validation/1280x800-slide-{4,6}.png`; repaired desktop slide 5, mobile slide 5 top/bottom and actual PDF page 5 from `/tmp/cad-first-layer-validation/repair1/`. These show a complete visible progression: one tested rod fit, preparation of the plates for the bed-up printing process, then the separate unmet wire-bend requirement. No notes, imagined dialogue, audience answer or model manipulation is needed. The paired scenes and adjacent text distinguish the recorded preview problem from the source response; the print equivalent is labelled and complete.

Directly checked XT60 `docs/EXPERIENCE.md:24–29` and `docs/p13-cad-source-domain-amendment.md:74–81`. The former records faces above the bed, incomplete/floating early layers and source changes. The latter specifies plain/flat face down, raised hub/land up, with authored footprints at Z=0. The revised observed caption no longer asserts a measured clearance above the whole first-layer band or an exact missing toolpath. Both orange-band labels say “Schematic”; the visible footnote states exaggerated geometry, non-toolpath status and unestablished successful physical print. The initial P2 overstatement is closed. The earlier P3 contact-surface jargon is resolved by the ordinary-language raised-area explanation.

Joined F-V's independent evidence for unchanged other 17 sections, navigation and fit geometry; byte-identical repair CSS/scripts/simulator; preserved 5/5 checks; refreshed offline bed rendering, no-WebGL fallback, compact/mobile views and exactly 18 PDF pages. This formal review does not duplicate those runtime tests. Coverage: REQ-005/006/007 source boundaries, REQ-009/014 offline/fallback/print, REQ-020 sequence and limited scope, REQ-021 read-only show-and-tell.

## Limits and next action

Mobile uses vertical scrolling; inherited fixed navigation crosses content during scrolling and truncates its Fullscreen label at narrow width, but all teaching content is reachable. That is a nonblocking inherited presentation-shell limitation. Global presentation navigation remains within the authorized scope; there are no audience questions or model controls. No live demo, new CAD, slicing, printer action or physical acceptance is established.

Only this `REVIEW.md` was written. No source, tests, dependencies, locks, hosting or Git changes and no optional test expansion. Root owns continuity and served-hash verification. Deliver the exact reviewed candidate with the fresh link.
