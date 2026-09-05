# VAL-GCS-R19-01 independent validation

**Verdict: FAIL.** The exact candidate and evidence fingerprints verify, and the supplied whole-target tests report 84/84. Independent class-specific and browser checks expose generic witness rendering, 36 failed field rows, ten failed R19 local oracles, four family aliases, polygon symmetry failure, malformed SVG, and empty teaching panels.

## Provenance and scope

- Candidate: `566aa6bc8c0aa57f1aeea341805a48db7d54c2078a48cebc4f9204a685e2fc74`; all `candidate-files.sha256` entries verified.
- Implementation evidence: `01dca854cd3048c0d5adece7e2325a2fb9e5abde3c512d75f5169f555c282966`; all `evidence-files.sha256` entries verified.
- Frozen input/design fingerprint: `cc4d1cd276a1394d000745e1177ae9eb3a3b114ed9bf7994c4622ee7c5432eef`; all 23 entries verified.
- Candidate source, tests, prior iterations, core, live routes, CAD, OpenSCAD, export, slicer, printer, physical, and continuity files remained read-only. New evidence is limited to this receipt, its manifest, and `scratch/r19-validation/**`.

## Gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Supplied target/source gate | PASS as written | Reports 84 map rows, 84 unique paths, exact-one official targets, and no literal strings covered by its narrow regex. |
| Supplied whole-target observability/collecting audit | PASS as written | 84/84 strings differ, but it does not strip or separately validate class-specific geometry/dimensions/metadata. |
| Full map/path/class shape | PASS | 84/84 rows and paths; 43 geometry, 40 dimension-annotation, one truthful-metadata; no missing/extra paths. All declared group sources resolve. |
| Exact-one/inactive handling | PASS | 84/84 official pairs have exactly one active primary target; zero unexpected inactive targets. |
| Independent class-specific audit | **FAIL, 48/84** | 35/40 dimension rows fail; the metadata row also fails. Only five dimension rows have a unique, changing named dimension subgroup with dimension geometry. |
| Eleven R19 local oracles | **FAIL, 1/11** | Only `label.weight` satisfies its exact local mapping. The other ten are listed below. |
| Transitive source/import boundary | Partial | Standalone renderer and local map only; no prior renderer or explicit hash/crypto/random mechanism. Generic witness mechanisms remain. |
| Ten explicit surface patterns | PASS | 10/10 explicit keys with no fallback for unknown patterns. |
| Stripped families | **FAIL** | Ends 3/4 (`flat == chamfer`), envelope 3/4 (`full == fade_from_top`), attachment 5/6 (`captured_loop == bridge_handle`), drain 3/4 (`bottom == top`). Closure 2/2, patterns 10/10, relief 3/3, and label modes 3/3 pass. |
| Polygon behavior | **FAIL** | Side-count output is 30/30 unique, but only 14/21 sampled rotation/roundness cases pass; all seven roundness-1 cases incorrectly change with rotation. |
| Six browser contexts with control activation | **FAIL** | Firefox desktop/mobile functionally pass. Chromium and WebKit desktop/mobile emit SVG parse errors and give `surface.spiral.softness` a zero-area target after selecting `shallow_helix`. No context has horizontal overflow. |
| Teaching panels | **FAIL, 0/6 contexts** | All six label mini-panel SVGs and all four attachment mini-panel SVGs are empty in every engine/viewport. |
| Normal/caption-hidden category sheets | Captured | Fourteen validation-local sheets were captured after mode activation. Every normal/hidden pair is byte-identical because the captured cards contain no caption content; hiding affects elements outside the card. |
| Evidence size | PASS | Independent JSON evidence totals about 163 KiB, below 1 MiB. |

## Blocking findings

### R19-VAL-01 — generic witness rendering

The renderer selects surface samples with field-path length, converts string length to geometry width, converts unrelated values through one scalar-width rule, and routes most dimensions through one generic curve/bracket fallback. These mechanisms make official target strings differ without representing the named relationship. They violate R19-03/R19-05 and the R18 standalone design's ban on common scalar witnesses.

Smallest repair group: remove `signal()` and the generic fallback from accepted field paths; dispatch each map row to a descriptor-specific builder and make the source-ban reject field-name/string-length selectors and universal scalar templates.

### R19-VAL-02 — class-specific audit failure

The target map declares 40 dimension fields. Thirty-four have no `[data-dimension-for="path"]` subgroup. `label.angleDeg` has a named subgroup but it contains a `motif` ray, no dimension geometry. Thus 35/40 dimension rows fail the required dimension-only gate. `label.openScadFontFamily` renders `Future OpenSCAD font <value>` instead of text exactly equal to the descriptor value, so the sole metadata row fails too.

Smallest repair group: add one feature-anchored, changing named dimension subgroup to every dimension field; implement the label angle arc/datum; render the metadata value exactly while keeping any explanatory label outside its primary metadata target.

### R19-VAL-03 — ten of eleven residual mappings remain incomplete

- `closure.matchPatternClosed`: phase rays change, but there is no fixed seam datum and assembled rotations are not used.
- `closure.screw.leadRunoutTurns`: lead and pitch change a bracket, but protected length is unused and the path is not the specified tapered helix/runout.
- `closure.screw.radialClearance`: profiles separate vertically while the bracket extends horizontally, so its endpoints do not measure the gap.
- `surface.reliefMode`: inset/outset values are used; base OD, crest OD, and minimum residual wall are omitted.
- `surface.envelope`: weight/placed values are used, but samples are laid out by array index rather than their theta/Z coordinates.
- `surface.coverage`: sampled thresholds replace the required interpolated transition bounds.
- `surface.flute.duty`: the first 12 samples replace the specified mid-height theta-sorted cross-section and crossing interpolation.
- `surface.spiral.softness`: the first 10 samples replace the required cross-band slice and 25/75-percent crossing width.
- `label.openScadFontFamily`: the target text is prefixed and therefore not the exact descriptor value.
- `label.angleDeg`: the glyph rotates, but its named subgroup has no angle arc, dimension class, or seam datum.

`label.weight` passes: numeric weight changes a closed glyph outline.

### R19-VAL-04 — family and polygon regressions

Stripped primary-target hashes alias the four family pairs in the table above. Rotation also changes the generic `container.rotationDeg` witness at roundness 1, although the section is rotationally symmetric. These violate R19-06 preserved behavior.

### R19-VAL-05 — browser/rendering failure

Chromium and WebKit report many malformed SVG `d` values such as concatenated numeric tokens in generic quadratic paths. After actual control selection of `surface.pattern=shallow_helix`, `surface.spiral.softness` has a zero-height primary target in both viewports for those engines. The supplied browser test misses this because it checks page errors rather than console errors and measures only three selected targets. The declared label and attachment mini-panel containers are empty in all six contexts.

Smallest repair group: emit unambiguous SVG numeric separators, validate every active target after each required mode activation, listen for console and request errors, and populate the required six label/four attachment panels before recapturing normal and caption-hidden sheets.

## Commands

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/candidate-files.sha256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/evidence-files.sha256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/inputs/frozen-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/candidate-files.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/evidence-files.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r19-eleven-field-semantic-recovery/inputs/frozen-inputs.sha256
node projects/laifen-wave-case/tests/test_p2_r19_target_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r19_render_observability.mjs
node projects/laifen-wave-case/tests/test_p2_r19_visual_families.mjs
node projects/laifen-wave-case/tests/test_p2_r19_ui_contract.mjs
node projects/laifen-wave-case/scratch/r19-collecting-audit/audit.mjs
node projects/laifen-wave-case/scratch/r19-validation/independent-audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r19-validation/independent-browser.py
```

## Remaining boundary

R19 remains conceptual preview evidence. This candidate cannot enter the VAL/CRIT/REV acceptance join. Caption-hidden human clarity still requires independent critique after the deterministic and browser blockers are repaired.
