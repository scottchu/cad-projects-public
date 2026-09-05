# Next agent — open and merge the reviewed pre-merge candidate

Use `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery` as the single
current iteration. Preserve the authoritative OpenSCAD source
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

The frozen candidate `ede603baef8ac0302a3ad044f4c32a8495b565dfd74e21293bcb660a1653761b`
passed independent formal review `1655b984a5cd71c8aaee7f55c46efa958bb0e1b8c2d38865e9585d0cc07c1d73`
with review evidence `1c690a08e6a0441766ed0bc79f3f671b0d1750943b8f16fd08a44034b57d126d`.
Documentation critique `7ab756208e210aa75c32972bb21534f7b80a6723cc2438c48cf02fc23752a626`
and validation `53913a5f040f7f9535456abfff1a72558b8594acedbd256b5c3e3791cc5cca8d`
also PASS. The 55 + 2 test classification and current artifact/runtime checks are
final for this candidate; create the PR and merge through the normal path.

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
acceptance. Do not publish, upload, slice or print.
