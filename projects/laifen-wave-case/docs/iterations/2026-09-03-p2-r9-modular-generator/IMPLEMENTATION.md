# IMP-GCS-R9-01 implementation receipt

**Status:** IMPLEMENTED — candidate frozen for independent validation and critique. This is implementation evidence only; it is not CAD, artifact/slicer, physical, review, or delivery acceptance.

## Provenance and scope

- Verified the 67-entry frozen input manifest before editing: `shasum -a 256 -c inputs/frozen-inputs.sha256` reported every entry `OK`. The frozen R9 design fingerprint is `85ebd36c458b7c14da7cb78a15d28238ce97cb62316a5197f5cbf146ee83fc49`.
- The new source-tree fingerprint is `d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab`, computed from the ordered path-and-content hashes in `CANDIDATE_MANIFEST.sha256` excluding the test entry.
- Created only the authorized R9 source tree, `tests/test_modular_generator.mjs`, R9 receipts, and `scratch/r9-implementation/**`. No R6/R7/R8 source, test, service, route, CAD, OpenSCAD, STEP, slicer, printer, continuity, or historical-evidence file changed.
- Late baseline evidence was read but not added to the frozen input manifest: R8 `VALIDATION.md` SHA-256 `b77b75450e33d38270a32e56b66eb0b9b87206d08dbc29c60fe666c2617403e4`. Its missing closure-form control and outward-envelope failures are addressed by the schema-generated `closure.screw.formHeight` control and centrally derived base/crest/total envelope plus camera fit.

## Candidate behavior

- Seven-group immutable canonical state, generated Basic/Advanced controls, serializable visibility predicates, immutable plugin registries, deep patch presets, and one deterministic OpenSCAD flatten map live in pure modules with no DOM, browser, Three.js, time, or random dependency.
- The SVG visual adapter consumes derived data and presents exactly two core exterior identities. Screw uses a visible helix/travel annotation; bayonet uses lugs, ramps, and a twist annotation. It also renders distinct end silhouettes, original quilted-diamond cells, named accessory silhouettes, outward/inward label cues, and labelled through-floor drain openings.
- Active invalid input retains raw edits and clears model, detail, scale/readouts, and envelopes; field-linked errors use ARIA invalid/error associations.

## Validation run

- `node projects/laifen-wave-case/tests/test_modular_generator.mjs` exited 0: `R9 modular generator focused pure checks passed`.
- `node --check` passed for every R9 module. The focused tests cover canonical/schema/export uniqueness, registry conformance, immutable deep presets and R8 retained projections, closure turns/mode accounting, profile bounds and curved dome samples, pattern/quilt periodicity, relief base/crest/residual-wall accounting, lower/upper label patching, finite mount angle, drains, unique accessory builders, and invalid clearing.
- An ephemeral `uv run python -m http.server` loopback server was used at `127.0.0.1:8151` and stopped immediately after the final run. It did not alter a route or service.
- `uv run python scratch/r9-implementation/browser_smoke.py ...` passed Chromium `151.0.7922.34` at `1440x1000`, `390x844`, and `360x800`; Firefox `153.0` at `1280x900`; and WebKit `26.5` at `1280x900` and `390x844`. The recorded representative state exercises bayonet 73-degree lock, dome, outward quilt, both drains, label target both, and bridge handle. Every run had zero console errors, page errors, and failed requests; each invalid 360-degree mount-angle case cleared SVG/readouts and marked the field invalid. Evidence and screenshot hashes are in `IMPLEMENTATION_EVIDENCE_MANIFEST.sha256`.

## Remaining risks

Independent validator and visual critic must assess the frozen candidate. This intent preview makes no claim about real closure mating, fit, strength, drainage, OpenSCAD execution/font parity, export, slicing, printing, or physical acceptance.
