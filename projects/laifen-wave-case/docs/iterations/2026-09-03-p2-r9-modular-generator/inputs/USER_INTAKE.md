# Frozen intake — P2 R9 modular generator

## User outcome

Refactor the browser visual-intent generator into simpler, reusable, correctly grouped parameters while preserving every previously requested visual feature. The controls must have a **Basic** view for high-level choices and an **Advanced** view that exposes only tuning relevant to the active choice. The intended later direction is an OpenSCAD Customizer and MakerWorld, but this iteration remains a browser visual-intent system and makes no OpenSCAD, CAD, STEP, mesh, slicer, print, fit, physical, publication, or MakerWorld-readiness claim.

The canonical model state is nested under seven user-facing modules: **Container**, **Closure**, **Ends**, **Surface**, **Vent & Drain**, **Label**, and **Attachment**. Controls come from one immutable field schema carrying type, units, bounds, defaults, tier, and conditional visibility. Closure, end-profile, pattern, and accessory variants use registries/plugins with defaults, relevant fields, derivation, validation, and visual-builder hooks. Presets are immutable deep override patches. One explicit flatten/export mapping is the only future boundary from nested state to OpenSCAD Customizer variable names.

## Frozen predecessor and reason for replacement

R8 is frozen at candidate-manifest SHA-256 `59f9aa1438f185979a47f888988833647aff43a1959969e13f54d1217431d655`. Its one-character parse recovery rendered successfully in the implementation smoke, but independent critique SHA-256 `0aaf54d6b064cf6b83c8e9ce186b5e5756f640ecb3e2f285e4351d9fcf9c389b` returned **BLOCK**. Critique evidence-manifest SHA-256 is `836300355fadddba0dcabd7e773610d7ccd1ad980f9b6fcdcc4ea527e6f69d09`.

The four blocking P1 visual findings are:

1. Screw and bayonet closure selections have no distinguishable visual mechanism or closure annotation.
2. Integrated lanyard eyelet, keyring tab, and bridge handle render as the same torus and do not honestly show their different envelopes or fixed/separate semantics.
3. The dome option retains a planar end and is not recognizable as a dome.
4. Camera-facing text is mirrored and low contrast; inset and outset do not communicate opposite relief directions.

R8 independent validation has no completed `VALIDATION.md` receipt in the frozen worktree at design time. `VALIDATION_INPUTS.sha256` exists and is frozen as a pending-gate input record. Before the final R9 freeze, the root relayed four preliminary validator findings: R8 does not enforce profile-specific end bounds; a `both` label patch misses the lower target; nonfinite accessory mount angle is accepted; and the renderer lacks the declared upper lock transform and closure-annotation geometry. These are required R9 regressions, but no completed validator verdict, receipt hash, or evidence result is inferred or invented. The independent BLOCK critique alone prevents R8 delivery.

## Required R9 behavior

- Keep exactly two core exterior pieces separated by one configurable middle split. Preserve continuous derived base/crest ODs across the pieces, no seam collar, and no thicker external thread zone. Optional accessories remain explicit extra bodies or intentional attached extensions and never change the two-core-piece count.
- Preserve assembled/exploded view, Laifen and wide-short presets, H, OD, wall, floor, split placement, round/regular-polygon section, side count, corner roundness, rotation, screw and bayonet parameters, closure phase matching, all end families, all patterns, global phase, pattern envelopes/fades, all accessories, label behavior, true-scale disclosure, accessibility, mobile behavior, invalid-state clearing, and total-envelope reporting from R8.
- Show screw mode with an unmistakable helical visual proxy and screw annotation. Show bayonet mode with discrete lugs, entry slots/ramps, lock travel, and a twist annotation. Both are visual mechanisms only.
- Give `integrated_lanyard_eyelet`, `captured_loop`, `separate_clip_link`, `keyring_tab`, and `bridge_handle` unique geometry, part identity, attachment semantics, and measured visual envelope. Make fixed versus separate visual mode obvious. Any metal keyring or chain remains a labelled reference silhouette excluded from generated geometry and envelope calculations.
- Make flat, chamfer, rounded fillet, and dome ends visibly recognizable at the same scale. A dome has a curved face with nonzero rise and no planar cap masquerading as the dome.
- Make all text outward-readable. Preserve `none|inset|outset`, safe string handling, preview font family, weight, size, relief, horizontal/vertical orientation, lower/upper/both target, circumferential position, target-local axial position, texture patch, and patch margin. Make inset and outset visibly opposite using geometry/light/section cues, not readout text alone.
- Fix the preliminary R8 regressions in the new architecture: enforce flat/chamfer/fillet/dome size bounds; apply label patches independently to both lower and upper targets; reject NaN/infinite/out-of-range accessory mount angles; and apply the declared upper-piece lock transform plus visible closure annotation geometry in the renderer.
- Clarify that the Surface choice called `shallow_helix` is a wide, shallow, soft spiral texture, separate from the Closure screw thread. Its Advanced controls must name spiral pitch, band width, depth, softness, and handedness/direction plainly.
- Add an original `quilted_diamond` Surface plugin: a diagonal groove lattice around smooth convex pillow cells. Reuse common axial/arc pitch, depth, envelope, and phase controls where possible; add groove width, pillow height, edge softness, and circumferential rotation. Preserve global theta/Z math, constant repeat pitch, closed-seam phase matching, and fade compatibility. Provide wall-depth warning/invalid thresholds, deterministic periodicity/boundary/sensitivity tests, and a representative browser state.
- Make Surface relief placement explicit with `reliefMode=inset|outset|balanced`. Keep one common depth input and derive actual inset depth, outset height, base OD, crest OD, and minimum residual wall from the active pattern's raw range. Enforce inset depth no greater than `wall-minWall`; the Laifen preset retains `minWall=1.8`. Outward aggressive rugged relief above 0.8 mm is permitted only with crest-OD and unverified-overhang warnings and is not a Laifen default.
- Add **Vent & Drain** with `none|bottom|top|both`, linked/unlinked end values, and per-end count, hole diameter, and ring radius. Show axial holes through the selected floor(s), check their edge and pairwise envelopes, and do not claim support-free ceilings, drainage performance, watertightness, or printability.
- Preserve deterministic pure math outside Three.js and the DOM. Verify that all three shared R8 presets map to equivalent pre-existing values and derived accounting before accepting a new candidate.

## Evidence boundary

R9 is a new visual source namespace. It does not mutate or inherit approval for P1 R7 CAD/STEP, P2 R3 delivery, R6/R7/R8 source, tests, services, routes, or continuity files. Reference images and prior physical observations remain evidence only and supply no imported geometry. The R9 implementation, validation, critique, formal review, and delivery roles must be distinct and must use immutable fingerprints.

The supplied visual reference `/tmp/codex-remote-attachments/01a06004-6842-76f1-bf1e-486590d05ac5/FE33693A-BF04-410A-9C2B-D398BD725807/1-Pasted-Image-1.jpg`, SHA-256 `c9db06d9b753aa84d02292d52a9e08f5d8f048e72efa43f87ab1813b44092031`, shows only quilted-diamond surface character and general proportional variety. It supplies no geometry, mesh, dimensions, closure, toothbrush-head form, accessories, brand name/text, manufacturing method, or product identity. R9 must derive an original periodic pattern rather than tracing or copying the reference.

The supplied deep-knurl reference `/tmp/codex-remote-attachments/01a06004-6842-76f1-bf1e-486590d05ac5/B0D4C7CB-5644-440D-BD09-AE781AA5243E/1-Pasted-Image-1.jpg`, SHA-256 `5c9f9bae602967971b67cf7082b17648190971cad22625f6b07e28b570c41798`, is visual evidence only that some rugged patterns may intentionally project outward and enlarge the crest envelope. It supplies no geometry, dimensions, thread, closure, product source, brand/creator text, process, print setting, support claim, or physical-performance evidence. No geometry or text is copied.
