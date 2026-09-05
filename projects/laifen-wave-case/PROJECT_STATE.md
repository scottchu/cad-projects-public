# Project state

## Current authority and review surface

The authoritative editable source is `openscad/laifen_case_customizer_v1.scad`,
SHA-256 `ade77d3fcff4d5ba1c659838b4f9d24245584f0570834453b6e8c2b778047841`.
It implements relationship B, the VFR-08 drain and print-layout repairs, and the
39 mm crest OD with 30/31 mm body/cap bores. The only current live review
surface is the VFR-12 C3 OpenSCAD WASM simulator:
<https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/>.

The reviewed UI candidate is
`2a58f483d2ba653c7e3c7de747bec8466837dd7f46ee4cd493ef9e8b61199433`.
Current runtime source hashes are schema
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
LC-IMP-02 and the independent final review. The frozen pre-merge candidate is
`ede603baef8ac0302a3ad044f4c32a8495b565dfd74e21293bcb660a1653761b`.
Formal review is PASS (`1655b984a5cd71c8aaee7f55c46efa958bb0e1b8c2d38865e9585d0cc07c1d73`)
with review evidence `1c690a08e6a0441766ed0bc79f3f671b0d1750943b8f16fd08a44034b57d126d`.
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
regeneration, slicing or physical acceptance is claimed. PR creation and merge are next.

## Open acceptance gaps

Actual-user Safari and icon comprehension remain open. Diamond controls remain
disabled because the cancellation/late-result race, smooth P3 sequencing,
detailed mesh gates and assembled/print-layout browser runs remain unresolved.
Native CAD reconstruction, slicing, support-free printing, loaded fit, thread
wear/strength, drainage flow and physical acceptance are also open. No printer,
MakerWorld or public-hosting action is authorized by this state.
