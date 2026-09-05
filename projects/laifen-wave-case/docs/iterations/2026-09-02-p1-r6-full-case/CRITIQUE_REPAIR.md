# CRIT-R6-02 independent export-repair critique

Status: complete as a narrow, read-only critique of the repaired R6 export
candidate. This is not geometry validation, slicer validation, physical
acceptance, or formal release approval.

Owner: `/root/case39_critique` (Terra/high), distinct from implementation,
validation, and formal review. The final repaired candidate is frozen by
`inputs/implementation-repaired.sha256`
(`a3873490fc7d7742698d9d73aceb6a8a29131fd8b846c76973d7133afb438bdc`).
The repair-specific source/artifact input set in
`inputs/critique-repair-inputs.sha256` was verified before this receipt and is
verified again with the evidence packet. The critic read every primary source
and STEP input only.

## Repair assessment

The repair is appropriately narrow. `normalize_female_runout()` selects a
single cone/B-spline shared edge through its neck-height and crest-radius
role, rather than a face index; requires at most one pre-existing mismatch;
copies topology before change; projects only onto the existing curve; bounds
that trim; preserves vertex tolerance; and fails closed unless the final
residual meets its tight guard. The production cap applies it only after the
existing cap operations. This supports isolation from the body, diamond
field, end floors, and the 39 mm exterior intent.

The selector remains deliberately specific to this topology, so an unrelated
future generator change must fail its exact-one guard and receive a new review.
That is an appropriate contained maintenance boundary, not a current blocker.
No source redesign is requested. The independent validator separately reported
cap parity and runout checks passing for this same frozen candidate; this
critic does not reclassify that result as physical or slicer acceptance.

## Visually inspected written-artifact evidence

| Evidence | Observation |
| --- | --- |
| `scratch/fullcase-critique/repair/cap-ready-shaded_20260903T032726Z.png` (`b571e438…fff43b31b`) | Repaired standalone cap retains the full diamond field to its narrow end treatment; no smooth collar is visible. |
| `scratch/fullcase-critique/repair/cap-ready-drain-face_20260903T032739Z.png` (`3c38c388…367ab862`) | The cap closed face visibly retains seven axial drains. |
| `scratch/fullcase-critique/repair/thread-section-cap-ready_20260903T033141Z.png` (`5472eb97…b5fc44b5`) | SHA-pinned standalone body and repaired-cap import shows the visible thread flanks and stop/shoulder relationship. It is not a fit or strength test. |
| `scratch/fullcase-critique/repair/closed-long-shaded_20260903T033014Z.png` (`93cd9513…671c345a`) | Exact repaired closed STEP reads as a continuous full-length 39 mm textured two-part case. |
| `scratch/fullcase-critique/repair/closed-longitudinal-reference_20260903T033236Z.png` (`d2da78d4…e7c4b64c8`) | SHA-pinned imported repaired closed STEP yields two actual Y>=0 halves. The gold L208/D29 item is visibly separate and labeled only as the centered, unretained nominal reference. |
| `scratch/fullcase-critique/repair/section-dimensions.png` (`5e57252e…caa1b4cd`) from `section-dimensions.svg` (`380b3091…db941554`) | Actual repaired section and compact panel clearly retain C213, outside219, overlap9/E6, L208/D29, and 2.5 + 2.5 nominal gaps, with the unretained limit visible. |
| `scratch/fullcase-critique/repair/print-layout-open-up_20260903T033441Z.png` (`7d0d28e2…051f5e3d`) | Exact repaired layout visibly contains two separated vertically oriented textured parts with their openings upward. |

The current full closed and longitudinal PNG hashes match the pre-repair
visual evidence. That is useful visual regression evidence, not a substitute
for the validator's exact written-artifact measurements.

## Findings and acceptance boundary

No new visual, source-isolation, or mechanical-intent blocker is found for the
minimal runout trim. The prior critique's unresolved boundaries remain:

- **Medium — adhesion and early layers:** the tall patterned, perforated end
  remains a slicer/first-layer risk; no slice or print was performed here.
- **Medium — threaded joint:** root strength, clearance, wobble, wear, and
  loaded closure are physical unknowns.
- **High physical-acceptance gap — device reference:** L208/D29 and both 2.5
  mm nominal gaps are a centered unretained envelope only. They do not prove
  actual fit, retention, or literal two-end non-contact.

## Commands and checks

Run from repository root with root `uv` Python 3.12 and CAD runtime 0.4.28:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-02-p1-r6-full-case/inputs/implementation-repaired.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-02-p1-r6-full-case/inputs/critique-repair-inputs.sha256
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/cad/p1_r6_full_case/closed_c25.step --output projects/laifen-wave-case/scratch/fullcase-critique/repair/closed-long-shaded.png --camera front --display rendered --size-profile presentation --view-labels --json
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/scratch/fullcase-critique/repair/longitudinal-r6-repaired.step.py --output projects/laifen-wave-case/scratch/fullcase-critique/repair/closed-longitudinal-reference.png --camera front --size-profile presentation --view-labels --json
uv run python /Users/scottchu/.codex/plugins/cache/text-to-cad/cad/0.4.28/skills/cad/scripts/snapshot --input projects/laifen-wave-case/cad/p1_r6_full_case/print_layout.step --output projects/laifen-wave-case/scratch/fullcase-critique/repair/print-layout-open-up.png --camera iso --size-profile presentation --view-labels --json
```

The section PNG was rendered from the exact SVG with root-UV Playwright
Chromium using a 1600 x 1067 viewport, then visually inspected. Every PNG in
the table was visually inspected; a successful renderer command alone was not
treated as a visual pass.

## Handoff

Route no CAD change from this critique. A distinct formal reviewer may join
this receipt to independent validation. Preserve the three physical/slicer
boundaries above; they prohibit claims beyond provisional CAD readiness.
