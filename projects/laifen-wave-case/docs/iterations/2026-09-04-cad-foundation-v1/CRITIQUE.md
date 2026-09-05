# CAD and visual critique — P1 R7 parametric-core refactor

**Task:** `CRIT-CAD-CV1-01`  
**Owner/role:** independent CAD and visual critic  
**Status:** **PASS** — no CAD/visual refactor-drift blocker found. This is not
formal review, slicer/process acceptance, or physical acceptance.

## Frozen inputs and candidate identity

- Design fingerprint verified: `1c233c8c64f0e7cb87919b601435318f6402a96cd3ad19af0fdb7251e908ed83`
  (`inputs/frozen-inputs.sha256`, 57/57 entries passed `shasum -a 256 -c`).
- Candidate fingerprint verified: `6d58e564885c317c62f9b2e89652a9d7f9be04b82df797f9ccc70fc33e99a304`
  (`candidate-files.sha256`, 27/27 entries passed `shasum -a 256 -c`).
- The four candidate STEP SHA-256 values are `02bfc1ca52ef97dcba3451c930408f64d0f383293933f6183029e36409e1c05a`
  (body), `b9561b34b96667d1af6e84d145c03d9aa319694fbf11f2cc3c0b60d6b6f18cf0`
  (cap), `cca2ea627369c3e2b3ee5c962238e134ecb56eeb878f9ebaf270d3a8751e76a2`
  (closed), and `cfd674cbbc2b1827d06c17a1daa0e61ed130074b0de205d49d6880939d86f90b`
  (print layout).
- Candidate and immutable P1 R7 files are byte-identical after excluding only
  the permitted STEP `FILE_NAME` time record and `cadgen:sourcePath` /
  `cadgen:sourceHash` provenance records. This direct serialization comparison
  passed for all four artifact pairs.

## Written-STEP visual review

I reviewed the actual written-STEP packet, rather than source previews. The
packet's input STEP copies carry the candidate hashes above. I inspected the
body/cap drain and isometric views, closed exterior and cross-section, the
longitudinal section, the thread/shoulder close-up, and the isometric/top
print-layout views. The packet is recorded in
`scratch/container-generator-v1-implementation/snapshot-results.json`,
`longitudinal-snapshot-result.json`, and `thread-closeup-snapshot-result.json`.
The reviewed image hashes include:

- `contact-sheet.png`: `3642e03abe56c355b166bd9c05556bde78f16de2404ffe92c544e695774dfec8`
- `closed-longitudinal-section_20260904T061343Z.png`:
  `5b37346936581f0d4b08668e72ee9273f38bf972dfe7e49c4a9ec11c6d63e2ab`
- `closed-thread-shoulder-closeup_20260904T061419Z.png`:
  `1a5e8ca5ba570c7af9b634e519894622dd12a2eec93f44e4c4f92c709114b90a`

The visual result preserves the expected long two-piece identity: a common
39 mm textured exterior, a single centered seam, and the same diamond field
on both body and cap. The exterior view shows no added collar, alternate end,
label, attachment, or geometry family. The longitudinal and shoulder close-up
show the same open-ended cavities, full thread/runout region, and positive
external shoulder. Both floor-end views visibly show a center drain plus six
ring drains. The narrow circular end-chamfer bands are retained at both closed
ends. The print layout has two separated vertical parts, each with its opening
upward and its closed drained end on the bed; the longitudinal section shows
floors and no newly introduced internal ceiling.

## Geometry and scope cross-check

Existing imported-STEP inspection evidence identifies the candidate as:

| Check | Observed candidate result | Critic assessment |
| --- | --- | --- |
| Body / cap identity | 1 solid each; 10,255 / 6,396 faces; Z `[-135,9]` / `[0,84]` | Matches P1 R7 identity. |
| Common exterior / bores | 39.0 mm X extent; body floor plane at `-132`, cap floor plane at `81` | Consistent with 39 mm OD and retained 30/31 mm cavity architecture. |
| Closed case | 2 leaf occurrences, 16,651 faces, 219 mm outside length | Matches locked two-piece closed case. |
| Cavity and thread region | 213 mm floor-to-floor separation; 9 mm thread-zone span, including 6 mm full-form engagement | Matches the frozen axial and thread law. |
| Seam / stop | Both parts meet at Z=0; close-up and written test evidence show material immediately below/above the seam, with cropped thread-zone intersection `<=1e-7 mm3` | No visible or evidenced loss of the positive shoulder stop. |
| Drains / closed ends | Each end view shows seven open 3 mm drains and retained 1.2 mm circular chamfer | No lost, blocked, or redesigned drain/end feature seen. |
| Skin registration | Body/cap/closed views show the N33 diamond field continuing through the seam; STEP diff reports no geometry/topology/bounds change | No phase break or smooth-zone redesign seen. |
| Print poses | 2 solids, bed Z=0, 84/144 mm heights, 7 mm separation; top view shows both openings up | Retains support-free vertical pose intent. |

The candidate's stored actual-STEP `inspect diff --planes` reports no geometry,
topology, bounds, face-count, or major-plane change for body, cap, closed, or
print layout against immutable P1 R7. I also read the bounded requirement scan:
it excludes alternate wide/polygon/bayonet/label/drain-selection controls and
any STL/3MF/GLB output. No added redesign feature was found.

## Findings

No critical, major, or minor CAD/visual finding. **PASS.**

Remaining risks are unchanged acceptance boundaries, not refactor defects:
the support-free conclusion is a CAD/DfAM pose and slope assessment only;
slicer settings, tall-part adhesion, print quality, thread durability/fit,
drain behavior, and the unidentified printed-artifact/device fit remain
unverified physical or process questions.

## Receipt

- **Allowed changed path:** this file only.
- **Commands run:** frozen/candidate SHA-256 manifest checks; SHA-256 checks of
  the four new and four immutable STEP artifacts; a direct metadata-filtered
  STEP serialization comparison for all four artifact pairs; snapshot/result
  and imported-STEP evidence inspection; bounded forbidden-feature scan using
  `/opt/homebrew/bin/rg`.
- **Inspected authorities:** `PROJECT_STATE.md`, `NEXT_AGENT.md`, requirements,
  experience and decision records; frozen `BRIEF.md`, `DESIGN.md`,
  `IMPLEMENTATION.md`, `HANDOFF.md`, input and candidate manifests; immutable
  P1 R7 iteration records; the four immutable and four candidate written STEP
  artifacts; and the saved actual-STEP review packet named above.
- **Next action:** `REV-CAD-CV1-01` may use this PASS only with the distinct
  validator receipt for the same candidate fingerprint. Physical and
  slicer/process state remain HOLD.
