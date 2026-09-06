# Next agent — drain count

Current work: `docs/iterations/2026-09-06-drain-count`, baseline `2819a8e`.
User accepted the checkboxes and requested drain-hole count, then pattern.
Count candidate C3 is implemented and passes focused deterministic, compiled
mesh and desktop/mobile browser checks. Formal review passes for draft PR
delivery; obtain the incremental user review before implementing pattern.
Read the active iteration HANDOFF and final receipts. Candidate manifest SHA:
`6fa4bb84a83bc859b95b0568d43e34227a5bc2be7f82fe8fb6a2f11796953f57`.

## Accepted drain checkbox baseline

Active iteration: `docs/iterations/2026-09-06-drain-checkboxes` on
`codex/container-desktop-customizer`, draft PR19. Read BRIEF, IMPLEMENTATION,
VALIDATION, CRITIQUE, REVIEW and HANDOFF. The user wants additions one at a time;
only Top/Bottom drain checkboxes and actual both-end support were added here.

Current preview <https://mac-mini.duckbill-ionian.ts.net:8453/> was checked in
Safari on desktop/mobile; both-end generation/download passed. Baseline Bottom
STL is byte-identical. CUA access recovered for these scoped checks, but prior
compact-controls full QA gaps were not all retested. Do not claim full UI or
print acceptance or merge automatically. The user marked the drain checkbox
item passed after `2819a8e` and authorized drain-hole count next, then pattern.

The accepted checkbox baseline SCAD SHA was
`cf0983e84e738be87e31462c903afcf02646915cc1e4a9e8641b8edce05b5393`;
only existing drain predicates/enum comment changed. Preserve all other geometry,
engine/worker lock, existing8448 route, and historical STEP releases.

## Preserved predecessor delivery

The predecessor iteration is `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery`.
Preserve the historical predecessor OpenSCAD revision
`ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`,
the R7 print-layout STEP
`80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`,
and the live VFR-12 simulator at
<https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>. Do not reset
Tailscale or runtime services.

LC-IMP-02 repairs LC-CRIT-01 C1-C3. It removes current claims for the dead 8449
CAD Viewer, aligns both CURRENT files, documents the implemented OpenSCAD
workflow, and excludes only the redundant R7 body/cap/closed STEP views from
Git. The files remain local and reproducible. Git must retain R7
`print_layout.step` plus all four `container_generator_v1` STEP releases.

The merged candidate `ac45ff09118ee46883d852eccc594ac221e569f0b780dcc6591986909e404be8`
passed independent formal review `ecdb122bbcbed1bdf8dee2ea9053ea9681473e6eca6dddf7568db073b362a69c`
with review evidence `333280b91159058d18af3d82bcccf3449a63dbe4544e1b7b60f0f8d99811c23f`.
Documentation critique `7ab756208e210aa75c32972bb21534f7b80a6723cc2438c48cf02fc23752a626`
and validation `53913a5f040f7f9535456abfff1a72558b8594acedbd256b5c3e3791cc5cca8d`
also PASS. The 55 + 2 test classification and current artifact/runtime checks are
final. PR #16 is merged at `8faeddaa0ea4a4de8c1c6d97199a68d7b4efe7d4`
(source commit `5829211964ebecbff8fb505941475648436b1f9c`), with final formal
receipt `ecdb122bbcbed1bdf8dee2ea9053ea9681473e6eca6dddf7568db073b362a69c` and
evidence `333280b91159058d18af3d82bcccf3449a63dbe4544e1b7b60f0f8d99811c23f`.

Cleanup recovery is
`/Users/scottchu/.Trash/laifen-wave-case-premerge-cleanup-2026-09-05.46d83abc57`
(617 files, 210 directories, 1,303,210,296 bytes). Frozen predecessor hashes:
LC-DES-02 `ece9e37ba3b10aa787f4e4a40691d6ce68ad28facd23b0ee1d01d0c240dc8ee8`;
LC-IMP-01 `fb390af434987010e0644a57a75196e8f018197cd0b1a02fab8e6b3c5216fe0e`;
LC-VAL-02 `b3acb4889c877fe18526ee80d5ecfecbafd460b7bf87111fe5eade748d77817c`;
LC-CRIT-01 `9363b472e33e8308c01a78d508476340f768fdc643d54197d6db0724eac79caf`.

The 27-root quarantine remains recoverable at
`/Users/scottchu/.Trash/laifen-wave-case-premerge-cleanup-2026-09-05.46d83abc57`
(617 files/symlinks, 210 directories, 1,303,210,296 bytes). Do not claim a
fresh clone, Safari, Diamond, new CAD, CAD regeneration, slicing or physical
acceptance. The next work is user-device review, then separate print/slicer,
fit, thread wear/strength, drainage-flow and physical acceptance checks. Do not
upload or start a printer job without a new explicit authorization.
