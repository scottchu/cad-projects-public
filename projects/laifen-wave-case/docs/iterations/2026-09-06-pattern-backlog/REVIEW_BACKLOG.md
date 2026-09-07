# PB-REV-A — preliminary backlog review

Date: 2026-09-06
Reviewer: `/root/compact_formal_review`, distinct from design and the actual
analytic-study implementer `/root/drain_validation` recorded in `HANDOFF.md`.

## Verdict

**PASS for the documentation-only backlog reconciliation.** No blocking or
actionable mapping defect was found. This review does not approve the analytic
study, production source, CAD, deployment, or the proposed pattern appearance;
those remain in the later implementation, validation, critique, and user gates.

## Verified inputs

- `docs/FEATURE_BACKLOG.md` SHA-256:
  `922951416eaff1821f790d1b8b854dde18b5ba4922a23e6a6e20192e3d6db9f9`.
- Baseline manifest SHA-256:
  `9d08cea42a798c548d54528cb28f715db5335b51d1f06e5cc37b534aeef832bb`;
  19/19 entries verified.
- Decisive-history manifest SHA-256:
  `1bb047310c8904121aa1440139c077673b091c939caf44358d627db836ac65b6`;
  10/10 entries verified.
- `BRIEF.md` SHA-256:
  `442c718589ef6a9a2e17037e941e030cad6a3498f33621505aa4a974835e464e`.
- `DESIGN.md` SHA-256:
  `c81ac2f3b20d8b7a8024b33671c03a6768e77c97ca53646441b86e9032ceb8b8`.
- Delivered source authority is SCAD
  `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`
  at baseline commit `191cb37119f9a4e4d23112ecd5bc0d18f0daec86`.

## Findings and coverage

- **Complete original order.** V2 preserves Smooth, Blunt diamond, Recessed
  diamond, Knit stitch, Straight micro-flutes, Flowing flutes, Rugged hex,
  Shallow helix, Wave flutes, and Quilted diamond in their original sequence.
  V3 fade/relief, V4 labels, V5 attachments, V6 bayonet closure, V7
  OpenSCAD/export parity, and V8 MakerWorld packaging retain the original scope.
- **Delivered mapping is evidence-based.** Smooth and current Diamond are mapped
  to actual source behavior; current Diamond's broad high centers and depressed
  crossings support the Blunt-diamond mapping. Ribs and Spiral are recorded only
  as partial overlaps with micro-flutes and shallow helix. Rings is truthfully
  identified as an additional delivered family outside the original ten.
- **Missing work remains missing.** Recessed diamond, knit, flowing flutes,
  rugged hex, wave flutes, quilted diamond, polygon integration, independent end
  families, exposed thread alternatives, exploded viewing, and the undelivered
  V3–V8 relationships retain explicit future scope. No historical name, enum,
  screenshot, annotation, or pixel hash receives source/CAD completion credit.
- **Obsolete UI is not revived.** Accepted inside dimensions, wall/end thickness,
  simple automatic/manual lid behavior, drain semantics, and current output roles
  remain authoritative. The backlog explicitly avoids restoring duplicate outside
  dimensions, unsafe old ranges, or prototype-only controls by default.
- **Prototype failures are used correctly.** R16's name-length aliases and
  R17/R21's insufficient crown/pocket recognition and generic pattern builders
  are negative evidence. Their ten labels are not treated as implemented motifs.
- **Next gate is correctly bounded.** Recessed diamond is the first distinct
  missing V2 item. The frozen proposal uses the documented negative smoothstep
  pocket field, shared pitch/depth/phase and equal-scale comparison against the
  current positive crown field. It is labelled an analytic appearance study,
  with no STL, compiler, print-ready, source, or physical claim. The proposed
  high-crossing/low-center distinction is falsifiable before CAD work.
- **Reference handling is proportionate.** The R4 equations support a first
  proposal without a photo. A close oblique side-lit photo is requested only if
  the user rejects or cannot identify that relationship; no image is fabricated
  as authority.

## Remaining gate

Freeze the isolated study candidate, then join independent analytic/state and
browser evidence with a distinct critique in PB-REV-B. Only user appearance PASS
may select the recessed motif for a later, separately frozen source/CAD gate.
Later backlog items remain queued one at a time.

Review commands: `shasum -a 256`, `shasum -a 256 -c` for both manifests,
explicit `/opt/homebrew/bin/rg` searches of frozen historical/source evidence,
and read-only inspection of `FEATURE_BACKLOG`, `BRIEF`, `DESIGN`, `HANDOFF`, and
the Foundation V1 roadmap. No source, test, status, build, or service was changed.
This reviewer wrote only `REVIEW_BACKLOG.md`.
