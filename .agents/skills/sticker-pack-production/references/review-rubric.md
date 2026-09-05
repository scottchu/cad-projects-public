# Sticker review rubric

Review the exact candidate hash, one slot at a time. The reviewer must be
distinct from the art implementer and must inspect source/candidate plus native
and small-size evidence. A pack-wide glance cannot replace these rows.

## Disposition columns

Use `PASS`, `FAIL`, or `NA` for every category. Use only `PASS` or `FAIL` for
the row result.

| Column | Review question |
|---|---|
| `source_semantics` | Is the declared action, expression, camera, pose, and source-required layout preserved without an invented substitute? |
| `identity_style` | Is the person/character recognizable with the approved face proportions, outfit, palette, contour, and rendering style? |
| `anatomy_occlusion` | Are there exactly the intended limbs, attached coherently, with every hidden limb explained by its named owner and no tail/wedge/ghost form? |
| `props_effects` | Is the correct prop present, held or contacted as declared, and are required effects complete and owned by the scene? |
| `text` | Is text absent when `null`; otherwise is the exact approved string reserved for deterministic composition with no pseudo-text in the art? |
| `crop_border` | Are the figure, helmet, limbs, prop, effects, and continuous white die-cut border fully visible with safe margins and genuine alpha? |
| `small_size` | At 512, 370, and 190 pixels on light and dark backgrounds, is the intended action readable without details merging or disappearing? |

Record a concrete note for every `FAIL`: name the object, side or attachment,
expected contract, and observed defect. Examples of actionable evidence are
"right heart intersects canvas edge" and "extra peach-colored endpoint below
left sleeve". Avoid generic notes such as "looks wrong".

## Result consistency

- `result=PASS` only when every applicable category is `PASS` and the remainder
  are `NA`.
- Any category `FAIL` requires `result=FAIL`.
- Blank reviewer, category, result, slot, or candidate hash means pending, not
  acceptance.
- A reviewer identity equal to the implementer identity bound in `audit.json`
  remains pending. `review-lint` must receive that same implementer identity so
  it can verify provenance and independence.
- The machine audit may warn about dHash similarity, isolated alpha components,
  or semantic duplicates. A human must inspect the evidence; warnings do not
  authorize a redesign and do not automatically fail a source-faithful slot.

## Decision routing

Return source/scene ambiguity to G1, method-wide identity/style or topology
failure to G2, and isolated candidate defects to the current G3 wave. Ask the
user only about an unresolved design choice. The coordinator, implementer, and
reviewer remain responsible for completeness and defect discovery.
