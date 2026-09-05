# P2 R10 descriptor and sensitivity recovery design

## Frozen predecessor and scope

R9 candidate `d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab` is failed/blocked, not repair authority. R9 VAL `e96e4055f78c290aadc120d17830f297ce73235bcd00df84aa10778437fa8715` and CRIT `b823c983d503eb058c93056efd6e941aa563faa0c673ad503060efb7616ae22d`, with their evidence manifests, are required regression inputs. R10 creates only the paths listed in BRIEF. Every earlier namespace, CAD, service and route stays protected.

## Descriptor boundary

`derive(state)` is the sole state-to-visual authority. It returns only either `{valid:false, errors, descriptor:null}` or `{valid:true, errors:[], descriptor}`. A valid descriptor is recursively frozen, finite, serializable JSON, and contains all render primitives, masks, transforms, accessibility strings, comparison silhouettes, envelopes, camera-fit inputs, active field IDs and named annotation targets. Invalid descriptors contain no stale visual primitives or envelopes.

Renderers receive a descriptor only. They cannot import/read schema, preset, raw state, validators, geometry, pattern, projection or placement modules. Renderer tests use a spy descriptor and static import guard; render output must serialize descriptor primitives/annotations without recomputation.

## Machine-readable coverage contract

Implementation writes `core/parameter-coverage.mjs`, one record for every schema leaf plus derived split-percent projection. Each record contains canonical field path, Basic/Advanced tier, active visibility AST, explicit OpenSCAD flatten name, nonempty help/label/unit/bounds/default metadata, descriptor subtree path, non-echo A/B pure oracle, named SVG/accessibility target and expected target delta predicate. Full-schema equality tests require no missing, duplicate or stale coverage record; each active record must have nominal and boundary witnesses. Inactive plugin poison values must not affect descriptor, target or errors until visible/active.

The oracle compares descriptor subtree hash and target-subtree hash, never raw values or source text. Each A/B pair must be valid and differ only in the declared active field. It must change its declared descriptor subtree and target, while protected unrelated subtrees remain stable. The implementation receipt records coverage count and every field’s result; prose need not enumerate the fields.

## Exact R9 repairs represented in descriptor

- Schema/preset/export: all metadata/help/explicit flatten names; exact R8 patch parity and canonical mm/percent split projection.
- Section/camera: support samples, across-corners/flats, rounded polygon extrema, actual visual bounds and fit-to-view readout.
- Closure: screw and bayonet parameter primitives, coaxial assembled halves, separate lock arrow/lug/ramp/top-inset phase evidence; never tilt side silhouette.
- Ends: distinct flat/chamfer/fillet/dome meridian descriptors and four same-scale comparison-card silhouettes.
- Surface: unique finite sampler signatures for every named pattern, relief placement/envelope/keepout outputs and visual field segments; no aliases.
- Labels: conservative allowlist, oriented frame/glyph primitives, per-target collision result, patch masks and outward readable strings.
- Drains: profile-aware unique locations, count-one center rule, attachment conflict envelope and actual face-mask holes.
- Accessories: per-mode primitives depend on every active dimension and bounds agree with rendered envelope.

## Gates and stop rule

Pure model/schema/coverage/geometry gates run before renderer. Descriptor sensitivity then runs before browser matrix. Browser evidence covers Chromium, Firefox and WebKit at desktop/mobile, valid representative modes, invalid clearing, all named SVG targets and accessible labels. If an active field lacks coverage, a descriptor/null transaction leaks output, a renderer imports non-descriptor authority, or a new independent failure appears, stop at the affected gate; do not broaden source scope. VAL and CRIT independently rerun the exact frozen candidate; REV requires both PASS before DEL.
