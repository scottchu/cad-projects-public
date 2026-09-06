# Project state

## Surface pattern in progress — 2026-09-06

Current iteration: `docs/iterations/2026-09-06-surface-pattern`, baseline
`cf4adb08314989f9d52a7afbd2f868756226d799`. The user requested the next item
after delivery of the count control. Implement the next surface-pattern gate
using the existing Smooth/Diamond source, with no extra CAD parameters.
Candidate C3 is implemented: native Smooth/Diamond swatches, immutable existing
Diamond geometry, shared schema/adapter/UI guards, and exact compiler-compatible
size limits. Candidate manifest SHA
`412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`.
32 Node and 12 Python checks, source critique and scoped mesh checks pass.
Whole-solid nonadjacent intersections and geometric T-junction checks remain
open; closed topology alone does not satisfy them. Full browser acceptance is pending:
Safari returned `cgWindowNotFound`, then the Chrome connection dropped with
`Transport closed` after partial C2 checks. Root requested restoration from the
user. Private 8453 continues to serve the accepted count build; do not enable
Diamond there before the combined C3 gates pass. Isolated candidate is on local
5181 and the held-real-worker harness on local 8461; see active HANDOFF.
Formal review approves a WIP commit to draft PR19 only; UI/mesh acceptance and
live enablement remain pending. The final review and replay inputs are retained
in the active iteration and project browser tests.

## Drain count — 2026-09-06

Current iteration: `docs/iterations/2026-09-06-drain-count`, baseline
`2819a8e5d2dd9c4c4f0b53958c4cce6c6ceec36f`. User passed the drain checkboxes
and specified the next order: drain-hole count, then pattern. Implement and
review count first; pattern is queued for the following user gate.
Candidate C3 manifest `inputs/candidate-03.sha256` SHA
`6fa4bb84a83bc859b95b0568d43e34227a5bc2be7f82fe8fb6a2f11796953f57`
adds a shared integer count per selected end, default 7, with size-dependent
limits (D10:1, D11:7, D30:17). The 0.4 mm ligament is a design assumption.
29 Node and 12 Python checks, build, independent actual-opening/mesh/boundary
checks and exact default STL parity pass. Root Safari desktop/mobile count,
invalid-entry recovery, checkbox memory, slider and Reset checks pass. Current
SCAD SHA `517f8546612ffecbc50a732362c9e3a326db03fa2c94e94a68daad472a0b42e2`.
Private 8453 serves C3 with six-file served-byte parity. Formal review passes
for this scoped item and draft PR delivery; REVIEW.md SHA
`c863bc1334595a6bcad5a543b52bd67397dc5992792082f00d07313d609ccad7`.
The user authorized advancing to pattern after count delivery. Keep PR19 draft.

## Accepted drain checkbox baseline — 2026-09-06

Current iteration: `docs/iterations/2026-09-06-drain-checkboxes`.
User acceptance: the user marked the drain checkbox item passed after delivery
of `2819a8e`, then authorized continuing one item at a time. The next item is
drain-hole count, followed by pattern.
The user requests one item at a time; this iteration only replaces the drain
selector with independent Top and Bottom checkboxes, including both/neither.
Bottom-only is the preserved default and Reset state. Candidate manifest
`inputs/candidate-01.sha256` SHA
`4a716d71c154bcba1264d556946613ec615c50217bba6331e36da8e9f1c67389`.

Editable SCAD source `openscad/laifen_case_customizer_v1.scad` is now SHA
`cf0983e84e738be87e31462c903afcf02646915cc1e4a9e8641b8edce05b5393`.
This intentionally extends only the existing drain selection predicates to
both; cutter shape, hole locations, dimensions and threads remain unchanged.
The prior immutable-source UI boundary is superseded only for this user request.
27 Node and16 Python tests, pinned WASM end-opening checks across all4 modes,
exact Bottom-only smooth-default STL parity, and build pass. Root Safari
verified desktop/mobile checkbox states, manual generation, Reset and a both-end
STL download. See VALIDATION and CRITIQUE; formal review passes for this scoped item and draft PR delivery. REVIEW.md SHA
`19ef28f4d3032b1d1a56dbb790e7885725433e33575240f4afea1aee58ef0646`.

Private preview: <https://mac-mini.duckbill-ionian.ts.net:8453/>; all6 built
files match the served bytes. Keep existing draft PR19 unmerged. Earlier compact
controls evidence lives in `2026-09-06-compact-controls`; current drain checks
do not retroactively close every broader UI acceptance gap. Existing4mm wall
floor and edited closed-assembly seam issue remain; no print-ready or physical
acceptance claim. No change to8448 or printer/public hosting.

## Preserved deployed baseline and CAD authority

The preserved predecessor source revision of `openscad/laifen_case_customizer_v1.scad` is
SHA-256 `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.
It implements relationship B, the VFR-08 drain and print-layout repairs, and the
39 mm crest OD with 30/31 mm body/cap bores. The preserved deployed review
surface is the VFR-12 C3 OpenSCAD WASM simulator:
<https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>.

The deployed predecessor UI candidate is
`2a58f483d2ba653c7e3c7de747bec8466837dd7f46ee4cd493ef9e8b61199433`.
Deployed predecessor runtime source hashes are schema
`894062333ba7370c4b17efc93b788623eb9db86d0117ffc45275886d0f754ae0`,
main `98af41e1377afb873208977eedc679ea9e887b04b96253bc2025b3896fbeb353`,
worker `fabd153527ec6c1aa0d5be9008679c7e2147d4559049149d8084b60795ec3845`,
and CSS `b530ae8870b5b2c0eb9548192edeb96fb122860ead203eb1295bd9ebb3893114`.
The live route and six built assets passed exact-byte HTTP checks in LC-VAL-02.
Older P2 R3 and CAD Viewer records are historical evidence; no 8449 CAD Viewer
URL is claimed current or ready.

## CAD and Git artifact policy

The immutable printable STEP authority is
`cad/p1_r7_end_chamfer/print_layout.step`, SHA-256
`80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`.
Git includes this R7 two-part print layout and all four distinct
`cad/container_generator_v1` STEP releases. The R7 `body.step`, `cap_c25.step`
and `closed_c25.step` are redundant views, remain in the local worktree, and
are reproducible from retained source; exact project-local ignore rules keep
them out of the first Git import. Historical P1 R2-R6 STEP fixtures remain
local and excluded while their source and durable evidence remain retained.

## Reversible pre-merge cleanup

LC-IMP-01 moved exactly 27 declared roots into
`/Users/scottchu/.Trash/laifen-wave-case-premerge-cleanup-2026-09-05.46d83abc57`:
617 files, 210 directories and 1,303,210,296 bytes. PREMOVE and POSTMOVE hashes
match; Trash was not emptied. The current source, R7 print layout, VFR-12
runtime and current evidence were preserved.

Frozen predecessor receipts are LC-DES-02 `DESIGN.md`
`ece9e37ba3b10aa787f4e4a40691d6ce68ad28facd23b0ee1d01d0c240dc8ee8`,
LC-IMP-01 `IMPLEMENTATION.md`
`fb390af434987010e0644a57a75196e8f018197cd0b1a02fab8e6b3c5216fe0e`,
LC-VAL-02 `VALIDATION.md`
`b3acb4889c877fe18526ee80d5ecfecbafd460b7bf87111fe5eade748d77817c`,
and LC-CRIT-01 `CRITIQUE.md`
`9363b472e33e8308c01a78d508476340f768fdc643d54197d6db0724eac79caf`.
LC-VAL-02 passed 57 focused tests. LC-CRIT-01's findings are resolved by
LC-IMP-02 and the independent final review. The frozen pre-merge candidate was
`ac45ff09118ee46883d852eccc594ac221e569f0b780dcc6591986909e404be8` (1,012 entries).
Formal review is PASS (`ecdb122bbcbed1bdf8dee2ea9053ea9681473e6eca6dddf7568db073b362a69c`)
with review evidence `333280b91159058d18af3d82bcccf3449a63dbe4544e1b7b60f0f8d99811c23f`.
Documentation recovery also passed critique `7ab756208e210aa75c32972bb21534f7b80a6723cc2438c48cf02fc23752a626`
and validation `53913a5f040f7f9535456abfff1a72558b8594acedbd256b5c3e3791cc5cca8d`.
The README classification is 55 fresh-clone-relevant selections plus 2 local-fixture-only checks.

## Final pre-merge evidence

The exact 27-root quarantine remains recoverable at
`/Users/scottchu/.Trash/laifen-wave-case-premerge-cleanup-2026-09-05.46d83abc57`:
27 roots, 617 files/symlinks, 210 directories and 1,303,210,296 bytes; its
recovery receipt records matching PREMOVE/POSTMOVE hashes and no permanent deletion.
Git inclusion is the R7 `print_layout.step` above plus the four
`cad/container_generator_v1` releases. Redundant R7 component STEP views remain
local/ignored and reproducible. The live 8448 index is HTTP 200 with SHA-256
`53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb`; the
OpenSCAD source remains `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.
The focused evidence is 55 + 2 tests; no fresh clone, Safari, Diamond, CAD
regeneration, slicing or physical acceptance is claimed. PR #16 was merged on
2026-09-05T16:18:45Z at `8faeddaa0ea4a4de8c1c6d97199a68d7b4efe7d4`, from source
commit `5829211964ebecbff8fb505941475648436b1f9c`. Final formal receipt is
`ecdb122bbcbed1bdf8dee2ea9053ea9681473e6eca6dddf7568db073b362a69c` with
evidence `333280b91159058d18af3d82bcccf3449a63dbe4544e1b7b60f0f8d99811c23f`.

## Open acceptance gaps

Actual-user Safari and icon comprehension remain open. Diamond controls remain
disabled because the cancellation/late-result race, smooth P3 sequencing,
detailed mesh gates and assembled/print-layout browser runs remain unresolved.
Native CAD reconstruction, slicing, support-free printing, loaded fit, thread
wear/strength, drainage flow and physical acceptance are also open. No printer,
MakerWorld or public-hosting action is authorized by this state.
