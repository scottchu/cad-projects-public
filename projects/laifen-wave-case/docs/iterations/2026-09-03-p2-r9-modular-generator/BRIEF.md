# P2 R9 modular visual-generator brief

**Iteration:** `2026-09-03-p2-r9-modular-generator`  
**Design owner:** `DES-GCS-R9-01`  
**Status:** frozen design contract; implementation has not started  
**Blocked predecessor:** exact R8 candidate `59f9aa1438f185979a47f888988833647aff43a1959969e13f54d1217431d655`, independent critique verdict **BLOCK**

## Outcome

Create a new schema-driven browser visual-intent generator that is easier to understand, extend, and later map to OpenSCAD Customizer variables. A Basic view exposes the form choices most users need; Advanced reveals only fields used by the selected variants. A compact comparison surface must let the user recognize screw versus bayonet, the four end profiles, all five accessories, inset versus outset text, and selected drain ends before relying on the integrated scene.

The visual candidate remains an intent and relationship gate. It cannot establish real helical or bayonet mating geometry, tolerance, strength, drainage, watertightness, support requirements, CAD, OpenSCAD execution, STEP/export, slicing, printing, physical fit, MakerWorld compatibility, or publication readiness.

## Requirements

| ID | Requirement | Class | Required evidence |
| --- | --- | --- | --- |
| R9-01 | Use a new `preview/p2-r9-modular-generator/` source namespace and new R9 test; leave the R6/R7/R8 candidate byte-for-byte unchanged. | invariant | scope manifest and protected-hash check |
| R9-02 | Canonical state has only the seven model groups Container, Closure, Ends, Surface, Vent & Drain, Label, and Attachment; presentation state is separate. | invariant | schema/state inspection |
| R9-03 | Generate controls from one deeply immutable field schema with stable path, label, help, type, units, bounds, step, default, Basic/Advanced tier, and `visibleWhen`. | invariant | schema integrity and DOM generation tests |
| R9-04 | Closure, end-profile, pattern, and accessory registries declare stable IDs, defaults, fields, pure derive/validate functions, and visual-builder hooks. | invariant | registry conformance tests |
| R9-05 | Presets are immutable deep override patches over one default state. One explicit flatten/export map owns all future OpenSCAD Customizer names. | invariant | deep-merge, immutability, and export-map tests |
| R9-06 | Preserve equivalent effective values and derived accounting for R8 `generic`, `laifen_wave_reference`, and `wide_short_makeup_jar` presets. | invariant | legacy-map snapshot and derived-equivalence tests |
| R9-07 | Exactly two core exterior pieces meet at one configurable middle split; derived base and crest ODs are continuous across both pieces with no raised seam collar or external thick thread band. | invariant | scene identities, bounds, and visual review |
| R9-08 | Screw visibly shows a helix plus screw/travel annotation; bayonet visibly shows distinct lugs, entry/lock ramps, and twist annotation. | visual acceptance | same-state comparison screenshots and critic recognition |
| R9-09 | Closure math retains screw pitch, turns 1/2/3, lead/runout, form height, radial clearance, and bayonet lock angle, lug count, capture, ramp rise, and clearance. Inactive-family controls are hidden. | invariant | pure math, conditional-control, and browser state tests |
| R9-10 | Flat, chamfer, rounded fillet, and dome have recognizable side silhouettes; dome uses an actually curved end face. Linked and independent end sizes remain available. | visual + math | profile samples, same-scale comparison, browser screenshots |
| R9-11 | Preserve round/regular-polygon sections, sides 3…32, corner roundness, section rotation, shared lower/upper frame, base across-corners OD, across-flats readout, derived crest OD, and closed phase alignment. | invariant | section math and phase tests |
| R9-12 | Preserve smooth, blunt diamond, recessed diamond, knit stitch, straight micro flutes, flowing flutes, rugged hex, shallow helix/soft spiral, and wave flutes. Preserve global theta/Z phase, constant pitch, seam/end keepouts, full/bottom/top/center envelope and depth/density fade. | invariant | registry coverage and periodicity/sensitivity tests |
| R9-13 | The shallow-helix Surface plugin labels its tuning as spiral pitch, band width, depth, softness, and direction; it is never presented as the Closure screw thread. | comprehension invariant | schema text and visual comparison |
| R9-14 | Each accessory mode has unique geometry, identity, attachment behavior, and computed envelope. Fixed and separate visual modes are legible; core OD and total envelope stay distinct. | visual + constraint | builder identity, bounds, screenshot nonidentity, critic recognition |
| R9-15 | Text is outward-readable and preserves safe text, font preview, weight, size, relief, orientation, target, circumferential/axial position, texture patch, and margin. Inset/outset must be visually opposite. | visual + safety | tangent-frame tests, hostile-input tests, screenshots and section detail |
| R9-16 | Vent & Drain supports none/bottom/top/both, linked/unlinked per-end count/diameter/ring radius, and visible axial through-floor holes. | invariant + visual | drain math, occurrence count, section/end views |
| R9-17 | Drain checks reject edge breakout, pairwise overlap/insufficient visual web, end-profile conflict, and attachment conflict; holes cannot increase core or total envelope. | constraint | boundary tests and invalid-state browser test |
| R9-18 | Invalid active state clears model, detail, scale, and derived envelope; it retains editable raw values and presents field-linked accessible errors without showing the last valid scene. | invariant | browser/ARIA tests |
| R9-19 | Main model uses one scene unit per millimetre on every axis with unexaggerated relief. Any comparison inset or magnifier states its magnification; screen pixels are never described as calibrated physical millimetres. | honesty invariant | source, readout, and screenshot review |
| R9-20 | Basic is the initial mobile/desktop control view; Advanced does not duplicate state and shows only active relevant fields. No horizontal overflow occurs at 360 or 390 CSS px. | UX/accessibility | responsive browser matrix |
| R9-21 | Preserve visual-only boundaries and do not mutate CAD/OpenSCAD/STEP/slicer/printer/MakerWorld, P2 R3 served bytes, routes/services, project continuity, or historical evidence. | invariant | manifest and formal scope review |
| R9-22 | Add an original `quilted_diamond` plugin with diagonal grooves and smooth convex pillow cells; reuse common pitches/depth/envelope/phase, add groove width/pillow height/softness/rotation, and warn or reject unsafe visual depth. | invariant + visual | global periodicity, seam/fade/boundary/sensitivity tests and representative browser state |
| R9-23 | Surface exposes `inset|outset|balanced` relief placement and derives inset depth, outset height, base OD, crest OD, and residual wall. Enforce the selected minimum wall; disclose crest growth and overhang uncertainty for aggressive outward rugged relief. | constraint + honesty | pure range mapping, envelope, warning and invalid-state tests |
| R9-24 | Close preliminary R8 validator regressions: exact profile-specific end bounds, independent lower/upper patching for label target `both`, finite normalized attachment angle, and a renderer-applied upper lock transform with closure geometry. | defect regression | pure boundary tests plus scene/renderer/browser inspection |

## Topology and user sequence

`lower-piece` and `upper-piece` are the only core exterior groups. They meet at global `z = H - S`; exploded view translates those same groups without changing model math. Closure proxies, arrows, dimensions, comparison cards, envelope wireframes, reference hardware, and drain axes are labelled annotations. Optional attachments are extra named bodies or attached extensions and never become a third core tube.

The user sequence is:

1. Choose a preset and Basic/Advanced view.
2. Set Container proportion and split, then select Closure, Ends, Surface, Vent & Drain, Label, and Attachment modes.
3. Use the compact comparison strip to confirm mode identity, then inspect the integrated assembled/exploded model and a relevant section/detail inset.
4. Read field-specific feasibility errors and separate core/text/accessory/total envelopes.
5. Answer the intent question: **Are the two core pieces, selected closure operation, end silhouettes, surface, drains, label relief, and attachment identities shown as intended?**

## Source and output boundary

Implementation may create only:

- `projects/laifen-wave-case/preview/p2-r9-modular-generator/**`
- `projects/laifen-wave-case/tests/test_p2_r9_modular_generator.mjs`
- R9 implementation receipts/manifests and `projects/laifen-wave-case/scratch/r9-implementation/**`

The expected namespace contains `index.html`, `style.css`, `app.mjs`, `core/`, `plugins/`, and `render/`. Pure model math, state, schema, registry contracts, and flatten/export logic may not import Three.js, browser globals, or DOM APIs. Rendering and DOM adapters consume derived immutable data and may not redefine validation or model equations.

## Task DAG and ownership

Every task receives a path-and-content SHA-256 manifest. A changed declared input invalidates only dependent gates. One implementation writer owns the new namespace. VAL and CRIT run in parallel only after IMP freezes one candidate; REV joins their exact receipts. DEL starts only after formal PASS.

| ID | distinct owner / role | dependencies and immutable input | allowed reads | exclusive writes / deliverables | forbidden scope | model and ceilings | done or stop gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IMP-GCS-R9-01 | implementation owner | R9 design fingerprint from `inputs/frozen-inputs.sha256`; protected R8 manifest | frozen inputs and project tooling | new R9 namespace, new R9 test, `IMPLEMENTATION.md`, candidate/evidence manifests, `scratch/r9-implementation/**` | R6/R7/R8 source/test, old receipts, CAD, services, continuity | balanced/medium; 25 min; 16k output; initial + 2 focused repairs | schema/registry/preset tests and prescribed browser smoke pass; freeze candidate or stop at retry ceiling |
| VAL-GCS-R9-01 | independent validator, never IMP | exact candidate manifest + R9 design fingerprint | candidate and frozen contracts read-only | `VALIDATION.md`, validation input/evidence manifests, `scratch/r9-validation/**` | candidate mutation, critique/review, service/CAD | strong/high; 18 min; 12k output; one validation + 2 method repairs | all deterministic, browser, accessibility, bounds, legacy-equivalence and invalid-state gates pass on same fingerprint |
| CRIT-GCS-R9-01 | independent visual/product critic, never IMP/VAL | same exact candidate manifest + R8 critique | candidate and frozen visual evidence read-only | `CRITIQUE.md`, critique input/evidence manifests, `scratch/r9-critique/**` | candidate mutation, validation/review, service/CAD | strong/high; 15 min; 10k output; one critique + 2 focused finding checks | user can recognize all four repaired P1 relationships plus drains and Basic/Advanced relevance at desktop/mobile |
| REV-GCS-R9-01 | formal reviewer, distinct from IMP/VAL/CRIT | exact candidate, VAL receipt/evidence, CRIT receipt/evidence, R9 fingerprint | all frozen receipts/evidence read-only | `REVIEW.md`, review input/join manifests only | candidate/source/test/evidence mutation, delivery/CAD | strong/high; 10 min; 8k output; initial + 2 provenance repairs | fingerprints verify; requirements traced; both independent gates PASS; otherwise HOLD/BLOCK |
| DEL-GCS-R9-01 | delivery owner, distinct from review roles | formal PASS and exact reviewed candidate | reviewed static source and review receipt | isolated static delivery copy, `DELIVERY.md`, delivery evidence only | candidate edits, existing routes/services, P2 R3 served bytes, CAD; any route change without a separately named authorized target | fast/low; 8 min; 5k output; one delivery + 1 retry | served bytes equal reviewed hashes and desktop/mobile smoke passes; otherwise no delivery claim |

Implementation stops immediately if it edits the R8 namespace, adds another core exterior piece, duplicates field definitions outside the schema, puts Three.js/DOM in pure modules, hides an active invalid field, reuses one accessory builder for multiple named geometries, renders a planar dome, mirrors outward text, paints drain discs instead of showing axial openings, changes a protected service/route, or makes a downstream fabrication/physical claim.
