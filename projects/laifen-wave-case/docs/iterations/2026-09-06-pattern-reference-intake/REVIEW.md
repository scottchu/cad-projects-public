# REF-REV independent review

Status: **PASS for original-image archival and proposed design notes only.**
Owner: `/root/reference_review`, distinct from archive and proposal authors.
Baseline: `2989aa412911df1fd947df81d056ea3ebfe7c66d`.

## Frozen inputs verified

| Input | SHA-256 |
| --- | --- |
| `inputs/sources-v2.json` | `3d81399f55b1bd1d34fe6693fc22b51484c433b95009e98407c08b3a79d62f83` |
| `inputs/source-images-v2.sha256` | `7102384c86cfa60ba4136c6551c829045aa73a778e976ec297cd174e047128f7` |
| Reference archive `SHA256SUMS` | `7cdda37eb2ca54c0a2461214b24482b42089df68534c95886c9fd4320c8bcbd5` |
| `ARCHIVE.md` | `71aa77f3dfecf546ce3034814cfe50b8acbb56347fe7ae8168f138148f4b1fd5` |
| Reference `PATTERN_PARAMETERS.md` | `d4e5f6a9ad0b315b4dbb57187ffa2eee9864fd1c646a01bbdacfd0b17f88f16f` |
| `DESIGN.md` | `492d0f0ac77e965a3d6afaefacebd4839642431e3995565b92f5e3a70ae1bbfe` |

## Evidence and coverage

- Root `uv run python` with standard-library `json`, `hashlib`, `struct`, and `re`: 33/33 archived files equal their original source bytes; IDs, batch order, byte counts, SHA-256 and PNG-header dimensions equal catalog values. All 36 archive manifest entries match.
- The first 30 entries of `sources-v2.json` equal `sources.json`; the first 30 source-image manifest lines equal the preserved original manifest. REF-031–033 append without renumbering.
- The same command checked 33 gallery figures, all README image rows and relative image links. Final focused `uv run python` verified all local README/gallery/proposal/DESIGN links resolve, all 33 per-reference proposal rows occur exactly once in order, and no trailing whitespace exists in those files, including untracked files.
- `view_image` independently inspected every original REF-001–033, including dark crosshatch/openwork ambiguities and the latest square flowing ribs and round threaded slots. Photo descriptions and explicitly uncertain alternatives are consistent with those images.
- `shasum -a 256` verified final proposal/receipt hashes and unchanged authoritative SCAD `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`. `git status --short` showed intake/reference documents and coordination pointers, without source/app edits.

## Findings and decision

No unresolved blocking findings. One minor wording typo was corrected before the final proposal freeze; no material repair cycle was required.

The 10-family grouping sensibly reuses patterns across sizes and separates body shape, lid grip, closure architecture, attachments, fade and actual openwork. Basic controls have everyday names and conditional advanced options; dimensions such as repeat count, groove size and outside envelope are derived rather than exposed as competing independent controls. Proposed common dimensions and variants are explicitly future design choices, preserving the current source gate.

Practicality judgments are appropriately conditional: openwork needs a liner or blind relief for ordinary sealed storage; deep/thin ribs and sharp facets need adaptation and later evidence. REF-031/032 flowing ribs can decorate a round shell, while a square cavity and closure require separate architecture. REF-033 finite rounded slots are distinguished from continuous spiral grooves. No reference is declared inherently impossible, waterproof, strong, or physically validated from appearance or embedded marketing text.

Remaining uncertainties: exact cell geometry in low-detail images, hidden liners, wall thickness, closure fit, usable safe parameter domains and physical durability. These do not block archival/design-note delivery. CAD, written exports, slicer and physical acceptance are untested in this documentation-only scope.

Next action: root updates continuity and delivers these records through the existing draft PR. User chooses one small appearance/section gate before any implementation; this review does not approve the existing recessed-diamond study or authorize new geometry.
