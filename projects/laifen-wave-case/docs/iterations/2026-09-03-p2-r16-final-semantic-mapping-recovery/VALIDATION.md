# VAL-GCS-R16-01 independent validation

**Verdict: FAIL.** Candidate `14b625606e1abd2a705d1874b557d9a9ba9ad6cc368d306de5d42417c8362a5e` and implementation evidence `e90328d9318420814168c21cc209c6094ed5e3c6e04c5bd1920575cbc64f7184` verify exactly. The prescribed gates all pass as written, but independent semantic checks find four incorrectly classified dimension targets, two categorical family aliases, an invalid nine-row target-map source declaration, and zero-height default targets in four of six browser contexts.

R16 remains conceptual preview evidence only. This receipt grants no live route, delivery, CAD, OpenSCAD, STEP/export, slicer, printability, fit, physical, MakerWorld, or publication acceptance.

## Provenance and passing gates

- Every entry in the candidate and implementation-evidence manifests verified before and after validation.
- The frozen design fingerprint is `8604d5a9fb6275a949f385153fcf4f8c3c54551d87058b68b607ebac33766dfc`; the frozen R15 predecessor fingerprint is `550dfb50af2b9ea950471d114ac9485a9ec507742225e6dcb80c219f88b15301`.
- Renderer source-ban PASS: no field-witness, crypto/hash geometry, `JSON.stringify` encoding, HSL encoding, randomness, timestamps, or schema/derive/preset/utils import.
- Exact-one target PASS: 84/84 official A/B pairs are valid and active, every render contains one primary target, there are zero duplicates and zero unexpected inactive targets, and all 84 descriptor/effect sources change.
- Only `label.openScadFontFamily` is declared metadata. Its visible badge truthfully changes with the descriptor.
- The frozen collecting audit reran in an isolated mirror, remained byte-identical, reported 84/84, and is 61 bytes. The independent 84-row audit is 48,898 bytes, below 1 MB.
- Polygon checks PASS: 30/30 side-count silhouettes are unique; all 21 sampled rotation/roundness cases behave as required, including rotational symmetry at roundness 1.
- Prescribed target, collecting-audit, stripped-observability, polygon, UI, and browser tests all pass as written.

## Blocking findings

### R16-V01 — P1 — Four dimension targets are geometry-only

The independent field audit is **80/84 PASS** when target classes are enforced. These four fields change stripped geometry, but their target lacks the required dimension annotation paired with the measured feature:

- `container.rotationDeg`: polygon path only; no angle arc or datum dimension.
- `surface.flute.waveWavelength`: motif path only; the case-sensitive dimension selector does not match `waveWavelength`.
- `surface.spiral.pitch`: motif path only; the case-sensitive selector checks `Pitch`, not lowercase `pitch`.
- `attachment.mountAngleDeg`: rotated attachment path only; no local angular datum or arc.

The prescribed audit hashes any target-byte delta and never verifies the target-map class, so all four incorrectly pass there.

### R16-V02 — P1 — Pattern and drain families still alias

After captions, metadata, and `data-*` attributes are removed:

- Surface patterns are **8/10 unique**. `blunt_diamond` aliases `shallow_helix`, and `knit_stitch` aliases `wave_flutes`. The renderer derives `surface.pattern` geometry from `s.pattern.length`, so equal-length names generate identical generic motifs instead of family geometry.
- Drain modes are **3/4 unique**. `bottom` and `top` serialize identically because the mode target places holes by array index and ignores each mask's `end` identity.

Closure 2/2, end profiles 4/4, envelopes 4/4, relief modes 3/3, label modes 3/3, and attachment modes 6/6 remain distinct. The prescribed visual-family test checks only polygon side counts, so it misses both aliases.

### R16-V03 — P1 — Nine target-map descriptor sources do not exist

The 84 target-map rows and classifications are unique and complete, but only 75 declared descriptor paths resolve. These nine container rows declare `descriptor.body`, which is not a descriptor root:

`container.height`, `container.outerDiameter`, `container.splitFromTop`, `container.wall`, `container.floor`, `container.crossSection`, `container.sideCount`, `container.cornerRoundness`, and `container.rotationDeg`.

The renderer obtains their data from real `constraints`, `envelopes`, `section`, and `projection` leaves, so this is a target-map declaration defect rather than a descriptor payload gap. **No descriptor gap exists.**

### R16-V04 — P1 — Four browser contexts contain zero-height default targets

The prescribed browser suite passes all six engine/viewport contexts. Independent browser checks also find 14 Basic fields, 13 hidden Advanced fields, 27 fields after expansion, seven category sheets, zero duplicates, no hidden-field focus, no page/console/request errors, no horizontal overflow, persistent disclosure, and transactional invalid clearing in all six contexts.

Chromium and WebKit at both `1280×900` and `390×844` nevertheless report zero-height primary target boxes for `ends.bottom.profile`, `label.mode`, and `attachment.mode` in their default flat/none states. Firefox reports nonzero boxes. The default representations are one-dimensional datum/path marks, so the strict nonzero target-visibility gate passes only **2/6** contexts. The prescribed browser test checks target existence for only `container.outerDiameter` and does not measure every active target.

## Commands

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r16-final-semantic-mapping-recovery/CANDIDATE_MANIFEST.sha256 projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r16-final-semantic-mapping-recovery/IMPLEMENTATION_EVIDENCE_MANIFEST.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r16-final-semantic-mapping-recovery/CANDIDATE_MANIFEST.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r16-final-semantic-mapping-recovery/IMPLEMENTATION_EVIDENCE_MANIFEST.sha256
node projects/laifen-wave-case/tests/test_p2_r16_target_contract.mjs
(cd projects/laifen-wave-case/scratch/r16-validation/mirror && node projects/laifen-wave-case/scratch/r16-exhaustive-audit/audit.mjs)
wc -c projects/laifen-wave-case/scratch/r16-validation/mirror/projects/laifen-wave-case/scratch/r16-exhaustive-audit/audit.json
cmp projects/laifen-wave-case/scratch/r16-validation/mirror/projects/laifen-wave-case/scratch/r16-exhaustive-audit/audit.json projects/laifen-wave-case/scratch/r16-exhaustive-audit/audit.json
node projects/laifen-wave-case/tests/test_p2_r16_render_observability.mjs
node projects/laifen-wave-case/tests/test_p2_r16_visual_families.mjs
node projects/laifen-wave-case/tests/test_p2_r16_ui_contract.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/tests/test_p2_r16_browser.py
node projects/laifen-wave-case/scratch/r16-validation/independent-audit.mjs
uv run --package laifen-wave-case python projects/laifen-wave-case/scratch/r16-validation/independent-browser.py
```

The smallest repair is bounded to four dimension mappings, the `surface.pattern` family dispatcher, drain-mode end placement, the nine container target-map source strings, and nonzero default geometry for the three affected targets. A new fingerprint requires fresh independent semantic, family, and six-context validation.
