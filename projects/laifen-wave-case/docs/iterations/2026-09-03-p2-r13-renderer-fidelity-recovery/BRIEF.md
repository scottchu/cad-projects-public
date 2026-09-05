# P2 R13 renderer-fidelity recovery brief

**Iteration:** `2026-09-03-p2-r13-renderer-fidelity-recovery`  
**Design owner:** `DES-GCS-R13-01`  
**Status:** frozen design contract; implementation not started  
**Failed predecessor:** R12 candidate manifest fingerprint `51727da73c72db6e391f4f83014a54076dc2ffbdc5bc617f753c72a8fc1a2221`, independent validation **FAIL**, independent critique **BLOCK**

## Outcome and baseline

Build a new descriptor-only SVG/DOM adapter and schema-driven UI that expose the already-valid R12 model in recognizable, parameter-sensitive views. R12 core schema and derivation remain read-only baseline inputs. The new adapter must consume actual descriptor supports, paths, fields, masks, transforms, primitives, bounds, envelopes, projections, and annotations. Static target dots, raw-state echoes, selected-name-only cards, and hidden effect hashes do not satisfy observability.

## Frozen requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| R13-01 | Create only the R13 preview/test/role-evidence namespace; preserve the exact R12 candidate and every protected baseline. | manifest and protected-hash checks |
| R13-02 | Keep R12 `schema.mjs`, `derive.mjs`, `parameter-coverage.mjs`, presets, and utilities byte-identical. A proven missing descriptor payload stops implementation for contract amendment. | pre/post hashes and descriptor-sufficiency receipt |
| R13-03 | Renderer modules accept a descriptor only and contain no schema, state, preset, validation, projection, pattern-sampler, or geometry-authority import. | static import guard and spy descriptor |
| R13-04 | Every one of the 84 R12 coverage rows has one declared semantic target and a valid A/B oracle. All 84 must change canonical meaningful output; generic target presence or effect-token changes are excluded. | exhaustive observability matrix |
| R13-05 | Each active `data-field-target` wraps visible geometry/style/text or a justified visible metadata output. It may not be a marker-only, zero-area, off-viewBox, transparent, hidden, or `aria-hidden` node. | SVG/DOM semantic-target audit |
| R13-06 | Height, OD, split, wall, floor, and presets alter a proportional elevation/cross-section. Wide-short and tall examples are recognizable without reading their names. | deterministic silhouette hashes and visual sheet |
| R13-07 | Round and regular-polygon plan silhouettes differ. Every integer side count 3..32 produces its own canonical silhouette; rotation and corner roundness change that silhouette. | exhaustive polygon hash/structure gate |
| R13-08 | Screw uses thread/runout/form/clearance witnesses; bayonet uses discrete lugs, capture/ramp, lock-travel, and clearance witnesses. The two operations remain coaxial and are topologically distinct. | closure topology/detail tests and visual sheet |
| R13-09 | Flat, chamfer, rounded-fillet, and dome serialize the derived meridian paths at one shared scale; linked and independent top/bottom states are explicit. | same-scale path and link-state tests |
| R13-10 | All ten patterns use the derived surface field across a reviewable area. Envelope, coverage, fade metric, relief, depth, pitch, keepout, and pattern-specific controls produce visible changes. | family uniqueness plus per-field hashes |
| R13-11 | Labels visibly show content, preview font, weight, size, orientation, target, angle, axial position, relief direction/depth, patch state, and margin. Future OpenSCAD font is a labelled visible metadata target only. | label geometry/style/text matrix |
| R13-12 | Five attachment modes have distinct silhouettes and semantics; detached presentation, half, angle, opening/member/hole/bridge/clearance/standoff dimensions are observable. | attachment topology and dimension matrix |
| R13-13 | Labelled top/bottom face views distinguish no/bottom/top/both drains and consume linked state, count, diameter, and ring radius. | mask geometry and link-state matrix |
| R13-14 | Basic is initial and contains only active schema Basic fields; Advanced adds only active schema Advanced fields. Conditional closure/end/pattern/drain/label/attachment fields follow `visibleWhen`. | pure visibility table plus computed-style/accessibility tests |
| R13-15 | Invalid active input transactionally clears every visual/fact surface and exposes linked errors; invalid inactive values remain ignored. | deterministic state test and browser matrix |
| R13-16 | Persistent adjacent copy says “Conceptual descriptor preview only — not CAD, OpenSCAD, or a printable/exportable model.” Fit-to-view/not-calibrated remains separate. | source, DOM, mobile and accessibility assertions |
| R13-17 | Cheap deterministic schema, core-regression, SVG/DOM canonical-hash, family-alias, tier, and disclosure gates pass before any screenshot/browser capture. | ordered command receipt |
| R13-18 | Chromium, Firefox, and WebKit pass at 1280×900 and 390×844 with no page errors, horizontal page overflow, hidden-field focus, target loss, or cross-engine family alias. | six-context browser evidence |
| R13-19 | R13 remains visual intent only and makes no CAD/OpenSCAD execution, STEP/export, slicer, printability, fit, drainage-performance, physical, publication, or MakerWorld claim. | copy and scope review |

## Exact implementation scope

Implementation may create only:

- `projects/laifen-wave-case/preview/p2-r13-renderer-fidelity-recovery/**`
- `projects/laifen-wave-case/tests/test_p2_r13_target_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r13_render_observability.mjs`
- `projects/laifen-wave-case/tests/test_p2_r13_visual_families.mjs`
- `projects/laifen-wave-case/tests/test_p2_r13_ui_contract.mjs`
- `projects/laifen-wave-case/tests/test_p2_r13_browser.py`
- R13 role receipts/manifests and role-owned `projects/laifen-wave-case/scratch/r13-*/**`

The R13 app may import the frozen R12 schema, presets, and `derive`; only R13 render modules may receive the returned descriptor. No existing source, test, receipt, manifest, evidence, continuity file, route, or service may change. No CAD, OpenSCAD, STEP, mesh, slicer, printer, or live-route action is in scope.

## Ordered DAG, retry ceiling, and delivery gate

| Task | Owner/role | Dependency and immutable input | Deliverable / done gate | Ceiling and stop |
| --- | --- | --- | --- | --- |
| IMP-GCS-R13-01A | implementation owner, descriptor sufficiency and tests | R13 design fingerprint; exact R12 candidate | 84-row target map and failing deterministic tests; proof existing descriptor supplies each target | balanced/medium; stop on any descriptor gap or core mismatch |
| IMP-GCS-R13-01B | same implementation workstream, renderer | 01A PASS | R13 SVG/DOM adapter and deterministic 84/84/family PASS | balanced/medium; no browser while a cheap gate fails |
| IMP-GCS-R13-01C | same implementation workstream, UI/browser | 01B PASS | Basic/Advanced UI, disclosure, six-context suite, frozen candidate/receipt | balanced/medium; no source outside exact scope |
| VAL-GCS-R13-01 | independent validator, never IMP/CRIT/REV | exact candidate fingerprint | read-only rerun, independent 84-field hash harness, polygon 3..32, tier/accessibility and six-context evidence | strong/high; PASS required |
| CRIT-GCS-R13-01 | independent visual/UX critic, never IMP/VAL/REV | same exact candidate | desktop/mobile recognition sheet and comprehension findings | strong/high; PASS required |
| REV-GCS-R13-01 | independent formal reviewer | candidate + VAL + CRIT | provenance/scope/requirement join and final disposition | strong/high; PASS only if both independent gates PASS |

The implementation workstream gets one initial attempt and at most two focused repair cycles total. Any candidate mutation creates a new fingerprint and invalidates affected downstream gates. Validator and critic may each use one initial method plus two focused method repairs without mutating the candidate. After the ceiling, stop and reopen/reduce the contract; postponed controls must be hidden and removed from the active schema in a separately authorized revision, never left inert.

No persistent/private/public live route, served-copy mutation, or delivery task may begin until independent validator, critic, and formal review all report PASS on the same candidate fingerprint. This contract itself does not authorize a route even after PASS.
