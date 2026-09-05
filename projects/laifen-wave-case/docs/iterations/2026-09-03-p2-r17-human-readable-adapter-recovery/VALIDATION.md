# VAL-GCS-R17-01 independent validation

**Verdict: FAIL.** The exact frozen candidate and implementation evidence were verified, all prescribed tests pass, and the strict six-context browser gate passes. Independent source and target-class inspection found three acceptance blockers: two of the four repaired dimension annotations do not respond to their fields, the R17 target map contains only the nine repaired rows instead of preserving the full 84-row classified map, and the R17 wrapper retains generic witness geometry through its imported R16 renderer.

## Provenance and scope

- Candidate manifest SHA-256: `5fe1228ca56d11f6e0d6d30c2c7e832118dcb3b67293cd79fbc475dc2da9a9c6` — exact requested fingerprint; every entry verified.
- Implementation evidence manifest SHA-256: `b0e1fe67b45bc387ff2bf44840d9851e1558be9005110afed2865e391c3b2667` — exact requested fingerprint; every entry verified.
- Frozen design/input fingerprint: `d791f7d51606e0e448ddc7b5443bb66f885700eb7f333bd651a7d1c2d0424d63`.
- Validation was read-only over candidate source, tests, prior iterations, frozen core, live routes, CAD, OpenSCAD, export, slicer, printer, physical, and continuity files. New files are limited to this receipt, its evidence manifest, and `scratch/r17-validation/**`.
- No screenshots were needed for the deterministic semantic and browser checks. This receipt makes no CAD, export, printability, fit, drainage-performance, or physical claim.

## Results

| Gate | Result | Independent evidence |
| --- | --- | --- |
| Manifest identity and contents | PASS | Both requested SHA-256 fingerprints match; all listed files verify. |
| Prescribed source/target contract | PASS as written | `test_p2_r17_target_contract.mjs` passes, but it scans only the R17 wrapper and checks only that the nine `descriptorPath()` results begin with `descriptor.`. |
| Prescribed 84-field observability | PASS as written | 84/84 target groups change for the official pairs after labels and data attributes are stripped. |
| Independent 84-field collection | PASS | 84/84 stripped target deltas, 84/84 exact-one ownership, 84/84 descriptor/effect deltas, and zero inactive target leaks. |
| Four repaired dimensions | **FAIL, 2/4** | `container.rotationDeg` and `attachment.mountAngleDeg` pass. `surface.flute.waveWavelength` and `surface.spiral.pitch` contain dimension paths, but those paths are byte-identical across their official field pairs. |
| Nine corrected descriptor paths | PASS individually | All nine exact paths match the R17 design table and resolve in the descriptor. |
| Full classified target map | **FAIL, 9/84** | R17 exports nine `{path, source}` rows and drops the other 75 rows plus the R16 `targetClass`, `surface`, and `oracle` declarations. |
| Explicit source ban | PASS | No field-witness, crypto/hash output, JSON stringify, HSL, randomness, timestamp, or renderer-side schema/derive import appears in the transitive renderer source. |
| Generic witness ban | **FAIL** | The imported R16 renderer still drives `surface.pattern` geometry with `s.pattern.length` and drives many surface targets with the same `raw.reduce((a,x)=>a+x,0)` aggregate motif. The R17 wrapper adds geometry without removing these inherited witnesses. |
| Pattern and drain families | PASS by stripped target output | Pattern 10/10 and drain 4/4 are unique; the named pattern and bottom/top drain aliases are removed. Closure 2/2, ends 4/4, envelope 4/4, relief 3/3, label 3/3, and attachment 6/6 are also unique. |
| Explicit per-enum pattern builders | **FAIL, 4/10** | R17 directly defines only `blunt_diamond`, `knit_stitch`, `shallow_helix`, and `wave_flutes`; six values use one fallback while inherited enum-length geometry supplies their distinction. |
| Polygon behavior | PASS | Side counts 3 through 32 produce 30 unique paths; all 21 sampled side/rotation/roundness cases pass, including expected rotation symmetry at roundness 1. |
| Metadata | PASS | The only metadata-bearing field target is `label.openScadFontFamily`, and its visible text changes truthfully with the descriptor value. |
| UI contract | PASS | Seven categories, Basic 14 / hidden Advanced 13 / expanded 27, no hidden focus, invalid-state clearing, and persistent conceptual/scale disclosure. |
| Chromium/Firefox/WebKit desktop/mobile | PASS, 6/6 | Chromium 151.0.7922.34, Firefox 153.0, and WebKit 26.5 at 1280x900 and 390x844: all active targets and the three repaired defaults have nonzero boxes; no duplicates, overflow, page errors, console errors, or request failures. |
| Independent evidence size | PASS | `independent-audit.json` is below the 1 MB limit. |

## Blocking findings

### R17-VAL-01 — P1: two dimension repairs are decorative rather than field-driven

`surface.flute.waveWavelength` renders its bracket width from `d.surface.field[1].z`, and `surface.spiral.pitch` renders its bracket width from `d.surface.field[5].z - d.surface.field[1].z`. Those sample Z positions do not change when the respective wavelength or pitch field changes. The surrounding target still changes because generic motif geometry changes, so the prescribed whole-target hash test masks the defect. R17-05 requires the dimension geometry itself to be feature-anchored and responsive. Smallest repair: derive each bracket span/endpoints from its named wavelength or pitch descriptor effect, then require the dimension-only geometry to differ across the official pair.

### R17-VAL-02 — P1: the full target-map contract was replaced by a nine-row delta

The nine corrected sources are accurate and resolve, but `target-map.mjs` exports only those nine rows using a new `{path, source}` shape. The R16 map had 84 rows with `targetClass`, `surface`, `descriptorSource`, and `oracle`. Dropping 75 declarations prevents the R17 candidate from independently expressing and auditing the required geometry/dimension/metadata classification and does not preserve the R16 map contract. Smallest repair: retain the 84-row map/API and override only the nine `descriptorSource` values listed by R17-06.

### R17-VAL-03 — P1: generic witness rendering remains hidden in the imported renderer

The R17 source-ban test reads only the wrapper file. The wrapper imports and returns R16 markup, then injects additional paths. The imported renderer still uses enum-name length for `surface.pattern` and a shared aggregate of sampled raw values for many surface-field motifs. R17 explicitly supplies only four of ten pattern builders and falls back for the rest, so successful family uniqueness still depends on the inherited generic witness. This violates R17-04 and the selected per-enum builder design. Smallest bounded repair: remove the inherited generic surface witnesses from the R17 rendering path and give every enum/field a direct, human-readable semantic builder; scan the full renderer dependency closure in the source-ban gate.

## Commands

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r17-human-readable-adapter-recovery/CANDIDATE_MANIFEST.sha256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r17-human-readable-adapter-recovery/IMPLEMENTATION_EVIDENCE_MANIFEST.sha256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r17-human-readable-adapter-recovery/inputs/frozen-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r17-human-readable-adapter-recovery/CANDIDATE_MANIFEST.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r17-human-readable-adapter-recovery/IMPLEMENTATION_EVIDENCE_MANIFEST.sha256
node projects/laifen-wave-case/tests/test_p2_r17_target_contract.mjs
node projects/laifen-wave-case/tests/test_p2_r17_render_observability.mjs
node projects/laifen-wave-case/tests/test_p2_r17_visual_families.mjs
node projects/laifen-wave-case/tests/test_p2_r17_ui_contract.mjs
node projects/laifen-wave-case/scratch/r17-independent-audit/audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r17_browser.py
node projects/laifen-wave-case/scratch/r17-validation/independent-audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r17-validation/independent-browser.py
```

## Acceptance gap

The same R17 fingerprint cannot proceed to formal acceptance while R17-VAL-01 through R17-VAL-03 remain open. The browser, alias-removal, polygon, metadata, UI, and basic 84-field delta results can be preserved during the bounded repair. Independent critique and formal review remain separate required gates.
