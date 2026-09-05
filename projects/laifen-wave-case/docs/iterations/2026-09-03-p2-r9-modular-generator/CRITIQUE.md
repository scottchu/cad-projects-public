# CRIT-GCS-R9-01 independent visual/product critique

**Verdict: BLOCK.** The exact R9 source candidate verifies as
`d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab`, and
the browser is accessible, responsive, and free of runtime failures in the
tested matrix. It still has three P1 visual-intent failures. This is browser
intent evidence only; it is not CAD, OpenSCAD, mating, export, slicing, print,
or physical acceptance.

## Provenance and method

- Owner and role: `CRIT-GCS-R9-01`, independent critic; candidate source and
  tests were read-only. Writes are limited to this receipt, its manifests, and
  `scratch/r9-critique/`.
- `shasum -a 256 -c CANDIDATE_MANIFEST.sha256` passed for all R9 source and
  test entries. Hashing the ordered manifest entries other than the test entry
  reconstructs the required source-tree fingerprint `d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab`.
  The protected five-entry R8 candidate also verifies.
- Ran the prescribed focused pure check:
  `node projects/laifen-wave-case/tests/test_modular_generator.mjs` →
  `R9 modular generator focused pure checks passed`.
- Opened the exact files through an ephemeral loopback server in Chrome for a
  desktop accessibility/screenshot inspection. Independently captured fresh
  Chromium `151.0.7922.34` at `1440x1000`, `390x844`, and `360x800`, covering
  Basic, Advanced, bayonet/dome/both drains, all requested pattern fixtures,
  all three relief modes, all five accessories, and invalid OD. The complete
  raw-state record, screenshot paths/hashes, and zero console/page/request
  failures are in `scratch/r9-critique/capture.json`.

## P1 blockers

### CR9-P1-01 — locked bayonet breaks the two-piece closed topology in the visible model

At a valid 73-degree, four-lug bayonet state, the `Assembled / locked` scene
rotates the entire upper side elevation around the seam. The upper core appears
as a diagonal, detached trapezoid instead of an upper cylinder that meets the
lower cylinder at the sole mid split. This gives the user a false operation:
an axial Z rotation should demonstrate lock phase/lugs without tilting the
piece in a side projection. It contradicts R9-07's continuous core OD and
one split, and makes the R9-24 lock-transform repair unreadable as a closed
container.

Evidence: `scratch/r9-critique/desktop-bayonet-dome.png`, SHA-256
`622d3395097691711bf0478671656e5f5db529784a0201c8508809eee235358c`.
The same capture confirms the visible BAYONET lugs/ramps/73-degree label and
three top/bottom holes; those elements address the former R8 absence but do
not make the tilted assembled state valid.

**Smallest action:** project the upper's axial lock rotation without rotating
the side silhouette; retain the two coaxial core outlines in `assembled`, and
show the phase/twist through the seam proxy, lugs, arrow, or an explicitly
labelled top/cross-section inset.

### CR9-P1-02 — the end comparison surface cannot distinguish flat, chamfer, and rounded fillet

The required compact comparison strip presents the same filled semicircle
glyph (`◒`) for Flat, Chamfer, and Rounded Fillet. Only Dome changes to a
separate U-shaped glyph. Since the main scene shows only the selected profile,
the user cannot compare all four requested end silhouettes before relying on
that integrated scene. The dome itself is now visibly curved in the selected
state, so this is not the old R8 planar-dome failure; it is a remaining R9-10
comparison/recognition failure.

Evidence: `desktop-basic-default.png`, SHA-256
`31dc9067e609a4486728012c7266ee0544e6e1653df01f07dd4d8a4a7a962d0a`,
and `desktop-bayonet-dome.png` above. The first shows the three identical
cards; the latter shows the curved dome selection.

**Smallest action:** render profile-specific side silhouettes in all four
cards at one scale: planar flat, beveled chamfer, tangent rounded fillet, and
curved dome.

### CR9-P1-03 — named surface choices and fade controls do not produce their claimed visual identities

The visual adapter collapses several required modes. `knit_stitch` renders the
same diamond lattice as the generic diamond path; `flowing_flutes` renders the
same straight vertical strokes as `straight_micro_flutes`; and the selected
`fade_from_top` remains full-height/unfaded. The shallow-helix fixture does
show broad spiral lines, but its pitch, band width, softness, and direction
are not consumed by the rendered lines. Thus a user cannot validate knit,
flowing, fade, or the wide-spiral tuning relationship through the claimed
visual gate.

Evidence: `desktop-pattern-knit_stitch.png`
(`43e5039d59ba9e5ae459173c0fee0d8b9c06039e3d09ce3f207ee36b315729ff`),
`desktop-pattern-straight_micro_flutes.png`
(`537486658a2cc274d5d57aaf5ca15fcf3c905bef777844108b6e3785318e7393`),
`desktop-pattern-flowing_flutes.png`
(`3f964a199d9fabda6121f009acbd32f96ba2f9b3f974e74b32ade46404181a58`),
and `desktop-pattern-shallow_helix.png` (recorded in `capture.json`). All use
the visible Advanced `fade from top` setting. Source inspection corroborates
the browser evidence: `render/svg.mjs`'s `texture()` branches only for quilt,
shallow helix, any `flute`, and a shared final diamond branch; it does not use
the fade or pattern tuning values.

**Smallest action:** have the visual adapter consume the existing derived
pattern/fade values. Draw a distinct stitch motif, a phase-modulated flowing
flute, and a fade-weighted field; map spiral pitch/band/softness/direction to
the visible path. Preserve the pure registry/derive contract.

## Confirmed behavior and R8 regression disposition

| Relationship | Critique outcome |
| --- | --- |
| Basic/Advanced and conditional relevance | PASS. Basic initially contains the 14 choice controls; Advanced exposes only active screw or bayonet, selected-pattern, label, drain, and attachment fields. No horizontal overflow was recorded at 390 or 360 CSS px. |
| Two pieces, middle split, core/base/crest/total readouts | PASS in screw states. The default is clearly two labelled core pieces and discloses distinct base, crest, accessory, and total envelopes. CR9-P1-01 blocks bayonet assembled state only. |
| Screw versus bayonet | R8's missing mode proxy is fixed: screw has a helix/travel label and bayonet has lugs/ramp/twist annotation. CR9-P1-01 independently blocks the bayonet locked projection. |
| Dome, label, relief, invalid state | PASS. The selected dome has a curved face; `WAVE` is readable and inset/outset have opposite visual treatment and explicit inward/outward signs; invalid OD retains the raw value, linked error, and clears model/detail/readout. |
| Accessories and drains | PASS for identity/comprehension. The five selected accessory fixtures have different named silhouettes and different total envelopes. `both` exposes labelled top/bottom through-floor circles and the readout distinguishes counts. |
| R8 P2 regressions | PASS for the user-facing effects: Basic/Advanced resolves irrelevant controls; R9 exercises lower/upper label target `both`, finite mount-angle invalidation, and profile invalidation without stale scene output. |
| Accessibility and honesty boundary | PASS in the observed matrix. Labels, field-linked invalid state, live/alert messages, focus treatment, 360/390 layout, and `1 scene unit = 1 mm · fit-to-view only` / visual-only limitations are present. |

## Next action

Repair only the three visual adapter paths above, freeze a new candidate
fingerprint, then rerun the affected browser critique and validation gates.
No delivery or fabrication claim may advance from this candidate.
