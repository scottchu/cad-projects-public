# P18 R1 independent mechanical critique

Status: **ACCEPT for independent validation; BLOCK formal review pending the
explicit dispositions below.** This is a critique of the immutable digital
candidate, not approval for slicing, printing, force, retention, heat, wear or
physical use.

## Candidate provenance

- Candidate manifest SHA-256:
  `fb0755a0d448ee000dde4bd63eacca7fbaf6e55abeb16312a7f39c5ccfc5d1d5`.
- All 20 manifest entries verified by `sha256sum -c` from the repository root.
- Focused source suite: `10 passed`.
- The four frozen snapshots were inspected at original resolution; the END and
  exploded STEP artifacts were also inspected for bounds/assembly structure.

## What the candidate preserves

- PASS — FRONT remains `+Z` head/up and `+Y` solder-tail/wires/right. OPEN is
  upper-left -> upper-right -> lower-right with the exact right vertical leg;
  END is upper-left -> middle -> lower-right. Bottom, diagonal and upright rod
  identities remain continuous and do not mirror, cross or swap.
- PASS — the production topology remains four plates, one stepped purple axle,
  three moving `OD4 x 50 mm` stainless rods, six permanent-cap occurrences and
  two keepers. No stability bar, yoke, linkage, gear, centered pivot member or
  replacement lock is present.
- PASS — both inner plates and the stepped axle are world-fixed; outer plates
  rotate oppositely by `-45/+45 deg`. The right force outer is larger
  (`OD54.933`) than the left outer (`OD53.933`) and both exceed the inner
  (`OD52.933`).
- PASS — the axle assembly order is geometrically coherent: `OD7.60` journals
  pass through exact `AF8.15` inner bores before the `AF8.00` keys seat against
  the `AF10.00` central spacer. The derived axle length is `34.90 mm`; the rod
  stack closes at `50.00 mm` with `8.70 mm` cap engagement per side.
- PASS — independently rerun nominal evidence reports rank 3, normalized worst
  condition `3.7502959057792857`, rail/axle reconstruction residual
  `3.97e-15 mm`, minimum web `2.200398673579 mm`, zero unintended sampled
  motion intersection and completed-pigtail removal clearance
  `0.933815921231 mm` against the `0.75 mm` digital gate.

## Findings requiring validation disposition

### C1 — High: near-tangent 45-degree rail segment is not a force proof

The minimum crossing sine is `0.000104329999`; the design contract already
places the diagonal near tangency around `u≈0.969`. Rank 3 proves nominal
centerline local closure only. It does not prove acceptable hand torque,
friction, absence of wedging, or absence of longitudinal backlash when the
real clearances are included (`0.075 mm` radial at rod slots and `0.150 mm`
radial at the axle guide). The longer 45-degree twist lowers nominal rod travel
per degree, but that alone does not establish a smooth or low-force mechanism.

Disposition required before formal review: validation must retain the exact
rank/conditioning and branch-continuation checks, quantify continuous cutter
coverage and clearance-amplified freedom around the near-tangent interval, and
leave final hand force/jamming/back-drive as an explicit physical test gate.

### C2 — High: solder-tool access is not yet a full-assembly actual-solid gate

The completed-pigtail removal sweep includes the XT60 body, both solder joints,
both bent wires and all OPEN production solids and passes. However, the
`reference_soldering_tool_keepout` checks in the current evidence are applied
to the fixed axle/keepers, not demonstrated against every plate, rod and cap.
Therefore the minimum removal clearance does not by itself prove that a real
soldering iron can reach both joints without touching the compact plate stack.

Disposition required before formal review: independently sweep the named tool
keepout to both solder joints against the complete assembly, or explicitly
record solder-tool access as an unvalidated physical/service risk rather than
claiming the mandatory service gate complete.

### C3 — Medium: the `C`-center evidence name contradicts its returned value

The source reports `centerAtCHasNoDecorativeHole: false`. This is explainable:
the functional diagonal rod rail passes near virtual datum `C` at END, so a
material probe at `C` can land in that rail. The snapshots and source still
show no centered bearing, decorative pivot bore or physical member at `C`.
Nevertheless, a false field named as a positive invariant is ambiguous and is
not asserted by the focused tests.

Disposition required before formal review: validator must distinguish
"no centered pivot/bearing feature" from "solid material exists at C in every
state" and prove the former from actual feature ownership. Do not reinterpret
the functional diagonal rail as a hidden centered pivot.

### C4 — Medium: permanent retention is represented but not physically solved

The six cap occurrences and two keeper seats are present and collision-free.
The default distal cap socket is `ID4.04` on `OD4.00` stock, a nominal
`0.020 mm` radial clearance; permanence therefore depends on printed outcome
or a later retention process, not nominal interference. The keeper uses only
`0.05 mm` diametral interference (`ID7.55` on `OD7.60`) in a `1.20 mm` thick
PETG ring. Neither installation force, cracking nor retention is digitally
proved.

Disposition: this does not block digital validation, but formal review must
keep cap/keeper coupons and assembly retention under `PHYS-007/PHYS-009`; no
"permanent fit proven" wording is allowed.

### C5 — Medium: compact service and boundary margins are real but thin

The governing plate web is only `2.200398673579 mm`, about `0.000399 mm` over
the frozen `2.20 mm` minimum. The analytic completed-pigtail service margin is
`0.933815921231 mm`, only `0.183816 mm` over its `0.75 mm` gate. These pass the
nominal model but leave essentially no allowance for elephant foot, rail edge
cleanup, PETG creep or workpiece tolerance.

Disposition: validation must reproduce exact STEP/source web and service
values without rounding down. Physical acceptance must inspect the limiting
web, printed clearance and heat exposure; no tolerance robustness claim is
authorized.

### C6 — Medium: force-side size difference is mathematically present but
tactile benefit is unproven

The right force plate adds only `0.50 mm` radius over the left plate and
`1.00 mm` over the inner plate. This satisfies the frozen "slightly larger"
hierarchy, but the snapshots show plain disk faces with no separate grip
feature. The small lever difference may not be perceptible or sufficient for
the near-tangent portion.

Disposition: preserve the frozen no-extra-part architecture for this
candidate; verify two-hand access and usable grip physically. Do not enlarge
or add a grip during validation.

### C7 — Low: DfAM orientation remains a physical dimensional-risk item

The plates, keepers and caps have source-authored bed orientations, but the
fit-critical stepped axle is laid horizontally in the print kit. Journal
roundness, hex across-flats, bridging/overhang surface and keeper-seat accuracy
are not established by valid STEP solids.

Disposition: keep `PHYS-009` open and use the existing axle/keeper fit coupon
before treating the printed axial stack as accepted.

## Decision

- **Independent validation: ACCEPT.** The immutable candidate is internally
  coherent enough to justify independent artifact, collision, math, service
  and snapshot validation.
- **Formal review: BLOCK for now.** C1, C2 and C3 require explicit independent
  validation dispositions. C4 through C7 must remain named physical risks and
  must not be converted into digital acceptance claims.
- No source, tests, STEP, snapshots or generated artifacts were changed by
  this critique.
