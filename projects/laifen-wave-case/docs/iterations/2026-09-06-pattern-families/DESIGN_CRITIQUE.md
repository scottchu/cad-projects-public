# PF-CRIT-DES — frozen design risk check

**Verdict: NEEDS CONTRACT CLARIFICATION before candidate acceptance.**

## Provenance

`inputs/design.sha256` verified at `9866b1c43c45ab0e5e7c29883985aa28fcab90bd67cb01228144435b86bc9679`.
The reviewed immutable inputs are `BRIEF.md`
`28483df404ab8b99528cdedb71ba98ef4f2f1146015a0b110904a7d4c78f71b6`
and `DESIGN.md`
`375bf58ffc3d60605c12da37c882778a0dbf93762031c3b2b39d1ee1b4edf8eb`.
Baseline UI conventions were read only through `git show c181dda`; no moving
candidate source, tests, build, service or browser state was read or changed.

## P1 — exact values and stepped sliders have no synchronization contract

The design accepts finite in-range exact values off the slider grid, while its
native ranges move in 0.1/0.05 mm steps. It does not define what the thumb shows
for Diamond size `4.83` or depth `0.43`, or what the first arrow/pointer move
does. A browser may visually snap the range while the exact input and job keep
the unsnapped value, recreating the misleading text/slider mismatch this UI was
built to remove. Freeze exact input as authoritative, prohibit render-time raw
mutation, and specify the thumb projection plus the first slider interaction.
Acceptance needs an off-grid value retained across family switches and a clear,
deterministic transition when its slider is used.

## P1 — selected invalid raw values have no range source

PF-03 requires invalid raw text to survive switching and requires current
allowed limits, but the selected-family predicate cannot derive a valid range
when one input is blank/non-numeric. The contract does not say whether that
slider, its coupled partner, or dimension sliders use nominal, default or
per-family last-valid values. This can silently replace memory or advertise a
range that is false for the preserved draft. Define the range source and enabled
repair controls for invalid size, spacing and depth separately; switching away
and back must leave the invalid text intact, and inactive invalid groups must
remain excluded from validity and identity.

## P1 — the five-choice compact selector has no responsive acceptance shape

The baseline has two visual cards. The new contract names five choices but does
not require distinct visual cues for the three additions or constrain wrapping,
overflow and target size. A five-column squeeze, horizontal scroller or tall
single-column list could all satisfy the text while failing the user's compact
mobile goal. Freeze acceptance at both viewports: all five labelled choices and
their distinguishable cues visible without horizontal page scrolling, each
target at least 44 px, no clipped focus ring, and the selected two-control group
immediately after the complete selector.

## P1 — canonical identity wording is internally ambiguous

“Only selected values enter identity” conflicts literally with putting every
new source field in the allowlist and assigning inactive fields fixed defaults;
the existing identity hashes the full canonical snapshot. Specify that the full
snapshot remains hashed, inactive source fields are normalized to fixed defaults,
and only unselected **raw memories** are excluded. Otherwise two implementations
can both claim compliance while producing incompatible cache/job identities.

These clarifications do not change the families, geometry, pilot or evidence
plan. The remaining design is sufficiently bounded for the Spiral pilot.

## PF-CRIT-DES-02 — repaired-contract recheck

**Superseding verdict: three findings closed; one narrowed P1 remains.**

Reviewed `DESIGN.md` SHA-256
`f748c76f1b413a88c8b90f9aa2af5b708363e25c6be439f9758c0c15dce5290c`
and `DESIGN_REPAIR.md` SHA-256
`d4ee50bae4ef78741af1a4af477d678bc2b3258ef99ae1bc8ad960e5ed0593af`.

- **Closed:** valid off-grid exact values now own state; their proportional
  thumb rendering, explicit-grid pointer/arrow commits and switch preservation
  are deterministic.
- **Retained, narrowed P1:** when exactly one selected-family value is invalid,
  its own slider remains enabled as a repair control, but the contract does not
  define that slider's thumb value or first keyboard Arrow action. “Strictly
  above/below the exact value” has no origin for blank/non-numeric raw text.
  Define a visible non-authoritative thumb origin and first Arrow behavior, or
  disable that slider until exact entry is numeric; never replace the raw text.
- **Closed:** the five-card desktop/mobile wrapping, distinct cues, 44 px target,
  overflow, focus and selected-group placement requirements are explicit.
- **Closed:** identity now hashes the full normalized allowlist snapshot with
  inactive source fields fixed and only inactive controller raw memory excluded.

This recheck read only the repaired design documents. Geometry and pilot
evidence remain outside this focused disposition.

## PF-CRIT-DES-03 — final design closure

**Superseding verdict: PASS; all four original design findings are closed.**

Reviewed `DESIGN.md` SHA-256
`426729855f05805f16661cc3728a6145b2eac291b56f60199fc6ca7528cc3e61`
and `DESIGN_REPAIR.md` SHA-256
`81b9c0026cf0bd890569e786466426f25c3e2ab8ad57663d84ffb49ee8b8456a`.
The narrowed blank/non-numeric case now disables its own slider, hides the
thumb, prompts exact entry, preserves raw text, and defines no pointer or
keyboard fallback before numeric recovery. This removes the undefined origin
without weakening finite numeric one-field slider repair. No design finding
remains open. Pilot geometry and its separately reopened topology work are
outside this focused closure.
