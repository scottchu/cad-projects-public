# VAL-GCS-R9-01 independent validation

**Verdict: FAIL.** The exact source fingerprint `d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab` verifies, but the candidate does not satisfy the frozen R9 modular-generator contract. This result is limited to the browser visual-intent candidate. It is not CAD, OpenSCAD, STEP/export, slicer, printability, fit, strength, drainage-performance, or physical acceptance.

## Provenance and method

- Validator: `VAL-GCS-R9-01`, independent of `IMP-GCS-R9-01` and `CRIT-GCS-R9-01`.
- Frozen design input fingerprint: `85ebd36c458b7c14da7cb78a15d28238ce97cb62316a5197f5cbf146ee83fc49`; all 67 entries reverified after validation.
- Candidate source fingerprint: `d7cf4cb3c72aa012b1ad4be5f9e096023b51c51ed79ea60c0f5587ea37816eab`, recomputed from the non-test entries in `CANDIDATE_MANIFEST.sha256`; every candidate entry verifies. The manifest file itself is SHA-256 `22d9bf20a54743eced9752bd1bfaee5f12f999b8bb0cbc95d4dac0125154dffa`.
- Validation input manifest: `VALIDATION_INPUTS.sha256`, SHA-256 `e3eb21d785f755816b3cb79e7292596bc98e9b508736bcc3ea07de3371e369f0`.
- The implementation evidence manifest reverified. Its focused Node suite also exited 0, but that suite did not exercise the failures below.
- Fresh independent analytic validation recorded 15 passes and 14 failures. Fresh browser validation recorded 17 passes and 14 failures on Chromium `151.0.7922.34` at 1440x1000, 390x844, and 360x800; Firefox `153.0` at 1280x900; and WebKit `26.5` at 1280x900 and 390x844. Browser console errors, page errors, and failed requests were all zero.
- Each analytic and browser method used one harness-only repair after its first run: the analytic harness caught the candidate's `envelopeWeight` exception instead of aborting; the browser harness changed SVG text extraction from HTMLElement-only `inner_text` to `text_content`. Candidate bytes were never changed.

## Blocking findings

### R9-V01 — P1 — schema, preset, and export contracts are not the frozen contracts

All 82 schema fields have an empty `help` value, no split-percent projection exists, and every registry validator is a no-op. The candidate adds `tests/test_modular_generator.mjs` instead of the exclusively authorized `tests/test_p2_r9_modular_generator.mjs` path.

The future Customizer map is derived mechanically from canonical paths instead of using the frozen explicit names. Examples include `container_crossSection` instead of `section_mode`, `closure_screw_pitch` instead of `screw_pitch`, `ventDrain_mode` instead of `drain_mode`, and `attachment_attachHalf` instead of `attachment_half`.

R8 effective values are not preserved. Against the frozen R8 presets, the independent projection found 28 mismatches for `generic`, 26 for `laifen_wave_reference`, and 33 for `wide_short_makeup_jar`. Examples include generic `formHeight 0.50 -> 0.45`, axial pitch `4.8 -> 12`, arc pitch `3.63 -> 9`, depth `0.45 -> 0.60`, and flat ends replacing linked 1.2 mm chamfers. `fromR8Flat` leaves 19 tested legacy fields at unrelated R9 defaults.

This fails R9-01, R9-03, R9-04, R9-05, and R9-06.

### R9-V02 — P1 — section and scale controls do not drive the rendered model

The pure sharp-hex support is wrong: at `theta=0`, R9 returns radius `30.0` mm while the frozen R8 equation returns `25.9807621135` mm. `cornerRoundness=0` produces a circle, and the browser returned an identical viewer hash `b619241e7f3028138f1cb2396199c96361aec62dee9f2c7e44ea1be6488f2824` for round, six-sided polygon, triangle, and a 27-degree rotated polygon. There is no across-flats readout.

The scene also uses fixed 310 SVG units for height and `1.8 * crestOD` SVG units for width, capped at 224, while claiming `1 scene unit = 1 mm`. `cameraFit` is displayed but does not fit the SVG. This fails R9-11 and R9-19.

### R9-V03 — P1 — closure geometry and the locked two-piece topology are not parameter faithful

Changing screw pitch from 2 to 3 mm leaves the viewer byte-identical. Changing bayonet capture, ramp rise, and radial clearance also leaves it byte-identical. The required named annotation identities and accessible strings are absent.

The assembled bayonet view applies its axial lock angle as an in-plane SVG rotation to the rectangular upper half. At 90 degrees the upper piece lies sideways and no longer meets the lower piece at the middle seam; the base/crest continuity and assembled topology are visibly broken in `desktop-bayonet.png`. The proxy lugs remain at the old seam while the upper body rotates away.

This fails R9-07, R9-08, R9-09, and the renderer-applied-transform part of R9-24.

### R9-V04 — P1 — patterns, fade, and relief are disconnected from the renderer

The browser renderer aliases `blunt_diamond`, `knit_stitch`, and `rugged_hex` to one identical diamond field. It also aliases `straight_micro_flutes`, `flowing_flutes`, and `wave_flutes` to one identical vertical-line field. An inset depth change from 0.3 to 1.0 mm is byte-identical. `full`, `fade_from_bottom`, and 25% coverage are byte-identical.

The pure `envelopeWeight` function throws `TypeError: Cannot read properties of undefined (reading 'height')` because it reads `surface.container.height`. Knit tightness was also analytically insensitive over the sampled grid. Although centralized inset/outset/balanced envelope accounting and the minimum-wall check work numerically, the rendered exterior does not consume that placed field. The quilt image is a flat repeated lattice rather than a geometry/readout demonstration of grooves, convex pillows, fade, and relief envelope.

This fails R9-12, R9-13, R9-19, R9-22, and R9-23.

### R9-V05 — P1 — label placement and safe-text validation are incomplete

Label orientation, angle, and weight produced identical label-group hashes. Browser font selection also does not reach the SVG label. The pure lower/upper `both` patch math passes, and inset/outset section signs differ, but the renderer paints texture over the entire pieces and then overlays rectangles rather than applying the patch to the surface field.

The candidate accepts `<svg/onload=globalThis.__r9xss=1>` as valid label text. Escaping prevented node injection and script execution in the browser, which is a useful security pass, but it does not preserve the frozen conservative R6 allowlist. A label centered on the seam was also accepted; required end/seam/closure/surface/attachment collision checks are absent.

This fails R9-15 and the independent-patching/rendering part of R9-24.

### R9-V06 — P1 — drain positions are not modeled as through-floor openings

Bottom, top, both, and none selections are distinguishable, and drains do not increase the derived envelope. The renderer draws circles over closed rectangular faces. There is no clip, mask, cutout, section interval, or other subtractive opening. Fourteen requested holes yielded only ten unique SVG positions because each end wraps positions with `i % 5`. Changing ring radius produced an identical drain-group hash.

The pure model accepts count one with nonzero ring radius, despite the center-hole rule, and accepts a bottom drain through a domed end with no profile-path conflict. The attachment conflict uses only a fixed angular threshold rather than the explicit attach-pad envelope.

This fails R9-16 and R9-17.

### R9-V07 — P1 — accessory geometry is distinct but ignores its dimensional contract

All five accessories have distinct visual hashes and fixed versus separate modes differ. However, changing bridge span from 22 to 40 mm and standoff from 7 to 15 mm leaves the accessory geometry byte-identical. The envelope readout changes while the shown body does not, so pure/render bound parity and parameter sensitivity are unproven. This fails R9-14.

### R9-V08 — P1 — invalid-state behavior is only partially transactional

The browser correctly clears SVG, comparison, detail, readout, and envelopes for an active 360-degree attachment angle; it marks the field invalid and announces the error. Pure `deriveModel`, however, still returns `camera`, `totalEnvelope`, ends, drains, labels, and accessory geometry when `valid=false`. A nonfinite attachment angle also invalidates `attachment.mode=none`, contrary to inactive-plugin isolation. This fails R9-18.

## Passed or partially passed gates

- The canonical state has exactly the seven required top-level model groups, presets and defaults are deeply frozen, and the flatten output covers each schema leaf once.
- Screw turn accounting for 1/2/3 turns, non-90-degree bayonet rotation accounting, active end-profile bounds, and a curved spherical-cap sample pass pure checks. Flat, chamfer, fillet, and dome screenshots differ.
- Relief base/crest/minimum-wall arithmetic passes for inset, outset, and balanced modes; aggressive wall loss rejects.
- The five accessory identities and fixed/separate transforms are visually distinct.
- Basic is initial, Advanced hides inactive closure fields, the active 360-degree angle clears the browser output, touch targets measured at least 44 CSS px, and no page-level horizontal overflow occurred at 360 or 390 CSS px.
- Firefox and WebKit loaded the representative state with two named core groups. This load result does not cure the bayonet topology or parameter-sensitivity failures.
- Hostile label markup did not execute and did not create nested SVG nodes because output was escaped.

## Commands

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r9-modular-generator/inputs/frozen-inputs.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r9-modular-generator/CANDIDATE_MANIFEST.sha256
awk '!/tests\//{print}' projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r9-modular-generator/CANDIDATE_MANIFEST.sha256 | shasum -a 256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r9-modular-generator/IMPLEMENTATION_EVIDENCE_MANIFEST.sha256
node projects/laifen-wave-case/tests/test_modular_generator.mjs
node projects/laifen-wave-case/scratch/r9-validation/analytic_validate.mjs
uv run python -m http.server 8159 --bind 127.0.0.1
uv run python projects/laifen-wave-case/scratch/r9-validation/browser_validate.py http://127.0.0.1:8159/projects/laifen-wave-case/preview/p2-r9-modular-generator/index.html projects/laifen-wave-case/scratch/r9-validation
```

The loopback server was stopped. No candidate, prior source/test, CAD, OpenSCAD, STEP, export, slicer, printer, route, service, continuity record, or historical evidence file was edited. The smallest next action is a new implementation candidate that reconnects schema and pure derivation to the renderer, restores exact R8/export values, and reruns both independent gates on a new fingerprint.
