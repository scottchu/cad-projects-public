# RES-01 official dimensional research

**Research date:** 2026-09-01. **Scope:** original Laifen Wave only; this is
web evidence for the measurement gate, not a measurement, CAD decision, or
acceptance record.  Frozen input manifest verified before research:
`8f3a859f5cf183d2abb489ac9d1112d8b50bbeb4965707088ac4e9ee9430da72`
(`inputs/contract.sha256`).  `docs/REQUIREMENTS.md` was also verified as
`71fa1a6ca7768219e5716e0efdbae538c80d30d06369542ec0803bf792126c8d`.

## Primary-source finding

Laifen's official [Wave specification page](https://www.laifentech.com/pages/toothbrush-specs)
states that its *handle dimensions* exclude the "Motor shaft/Brush head." It
lists the following dimensions by material: ABS 31.6 x 28.2 x 142.7 mm;
aluminum alloy 29.2 x 27.8 x 142.7 mm; stainless steel 28.8 x 27.4 x 142.7
mm. The manufacturer labels the first two fields Length and Width and the
third Height. In this project, only the 142.7-mm field can plausibly be read
as the axial handle dimension; the page does **not** state an installed-head
overall length. Thus its transverse field named "Length" must not be confused
with the case's axial `L`.

The official [Canadian Wave page](https://ca.laifentech.com/pages/wave-electric-toothbrushes)
repeats the same three material-specific handle tables and describes the heads,
but publishes no head length, head cross-section, installed overall length, or
maximum assembled envelope. Its confirmation that the heads carry a metal
counterweight is qualitative only and must not be turned into a dimension.

Focused official-site searches checked on 2026-09-01:

- `site:laifentech.com Wave toothbrush brush head dimensions overall length`
- `site:laifentech.com "Wave" "brush head" "mm"`
- `site:laifentech.com/products "toothbrush head" "Dimensions" Laifen`
- `site:laifentech.com "Gum care brush head" mm`

No source in those results gave an explicit installed original-Wave length or
variant/head-specific maximum cross-section.

## What this can inform

This evidence leaves **REQ-02** open: `L=208` is still an unverified
placeholder and the installed-head maximum envelope `D=29` is unverified.
It cannot establish end clearance, contact intent, or REQ-03's closed-cavity
length `C`.

It exposes a **high-severity necessary-condition conflict** for an
ABS-inclusive 32-mm circular ID. The published ABS transverse extent is 31.6
mm. Even if that extent is centered in a 32-mm bore, the best possible radial
clearance in that direction is `(32 - 31.6) / 2 = 0.2 mm` per side, below
REQ-03's at-least-1-mm radial-clearance target. This conclusion does not
depend on knowing the full outline; the missing outline can only reveal
additional conflicts. A circular bore nevertheless cannot be proven from
fitting a rectangle's two listed dimensions independently: actual outline,
orientation, motor shaft, installed head, counterweight, and their motion
envelope remain unknown. The aluminum and stainless transverse extents (29.2
and 28.8 mm) do not resolve their assembled-envelope fit. Conversely, a 29-mm
provisional circular device `D` conflicts with the published 31.6-mm ABS
handle extent and is unsuitable as a universal ABS-inclusive circular
envelope. It is not evidence that the other variants, nor the installed
assembly, fit a 29-mm cylinder.

## Remaining measurement gate

Ask the owner to identify the actual handle material and installed head, then
measure (1) assembled axial tip-to-base length and (2) the maximum installed
cross-section/envelope in the orientation intended for storage. Retain the
separate decision whether normal lower-floor resting contact is permitted;
internet evidence cannot decide that use-sequence intent.

**Disposition:** incomplete. The ABS/32-mm radial-clearance conflict is high
severity; installed length and the head envelope remain unresolved. Official
web evidence does not replace the required physical measurement and does not
authorize CAD, export, slicer, or physical acceptance.
