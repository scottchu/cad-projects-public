# REV-02 formal review join

Owner `/root/preview_formal_review`; 2026-09-01; independent formal reviewer. **PASS for publishing this width preview as a 2D diagnostic only** on exact candidate `inputs/des05-repair-candidate.sha256`, fingerprint `9f1fdb44f7b350f7ca903c37ca2383ba195dd2f7235bbe69d2b1596f86ae4f61`.

This join is limited to the DES-05 rendered-numeric recovery and its authorized label-only repair. It does **not** confer CAD, STEP/export, slicer, printer, fit, or physical acceptance.

## Provenance and manifest verification

- Frozen design inputs remain `inputs/des05-inputs.sha256`, fingerprint `8975b1e6fcb23c2b16d3eadb423a9ff05b6ac01a9a2fb4a7a6411940406d35b9`.
- Initial DES-05 implementation candidate remains preserved at `inputs/des05-candidate.sha256`, fingerprint `f0fe32796fcfae64591565b2f48983325b2c7d407e6152cf2272c3e9536eb788`.
- Final repair candidate verified here: `inputs/des05-repair-candidate.sha256`, fingerprint `9f1fdb44f7b350f7ca903c37ca2383ba195dd2f7235bbe69d2b1596f86ae4f61`.
- `shasum -a 256 -c` on the repair manifest returned 19/19 OK during this review.
- Diffing `preview/measurement-gate.html` against preserved `inputs/des05-pre-repair-source.html` shows the described one-line change only: `上段參考 ID 31` moved from centered `x="${cx}" y="64" text-anchor="middle"` to the external label column at `x="${label}" y="40"`.
- Diffing `inputs/des05-candidate.sha256` against `inputs/des05-repair-candidate.sha256` shows one manifest-entry change only: the hash for `projects/laifen-wave-case/preview/measurement-gate.html`. `tests/test_measurement_gate.mjs` and all frozen inputs stayed unchanged.

## Joined findings and disposition

- DES-05 contract scope is preserved: fixed bores 30/31, no D clamp, no geometry/UX redesign, and the existing invalid-input clearing path remain intact under `REQ-03`, `REQ-12`, `REQ-14`, `DEC-05`, `DES04_RECOVERY.md`, and `DES05_NUMERIC.md`.
- CRI-05 PASS on `f0fe3279...` resolved C04-01 within scope: extreme `D=1.7e308` now clears SVG/readouts and restores ordinary finite output when D returns to 29.
- VAL-05 PASS on `f0fe3279...` confirmed the same DOM sequence at true widths 360/736 and initially raised medium presentation finding V05-01 for the upper-ID label overlap.
- The authorized repair candidate `9f1fdb44...` preserves that numeric pass state and changes only the upper-ID label placement.
- CRI-05 label-delta continuation PASS verified byte-exact preservation apart from that label move.
- VAL-05 repair rerun PASS verified the same `9f1fdb44...` candidate, reported zero bounding-box intersections in `scratch/width-des05/repair-dom.json`, and recorded four repaired screenshots. This review also spot-checked `scratch/width-des05/repair-360-light.png`; the upper-ID label is visibly outside the cavity and clear of the upper-floor/device region.

## Formal decision

No blocking finding remains within the frozen DES-05 width-preview scope. Prior failures are preserved and explicitly dispositioned rather than overwritten:

- Historical IMP-03 candidate `57a181b7...` remains preserved and rejected.
- Historical DES-05 candidate `f0fe3279...` remains preserved as the numeric-fix pass state before the label-only repair.
- V05-01 is resolved on exact repair fingerprint `9f1fdb44...`; C04-01 remains resolved on the same downstream publication state because the repair leaves the numeric guard and tests unchanged.

Changed paths attributable to the accepted repair candidate are exactly:

- `projects/laifen-wave-case/preview/measurement-gate.html`

Changed path from this formal-review task:

- `projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/REVIEW_DES05.md`

Next action for root: publish or wrap this exact `9f1fdb44...` preview as the updated private 2D diagnostic if desired, while keeping all remaining full-case measurement, CAD, export, slicer, and physical gates explicitly pending.
