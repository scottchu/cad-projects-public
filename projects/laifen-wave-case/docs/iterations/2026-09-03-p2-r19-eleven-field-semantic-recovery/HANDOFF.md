# P2 R19 eleven-field semantic recovery handoff

**Final status: REJECTED.** This iteration stops before formal review and delivery. It does not alter the reviewed P2 R3 live simulator or the P1 R7 CAD baseline.

## Provenance verified

- Frozen design/input: `cc4d1cd276a1394d000745e1177ae9eb3a3b114ed9bf7994c4622ee7c5432eef`.
- Candidate: `566aa6bc8c0aa57f1aeea341805a48db7d54c2078a48cebc4f9204a685e2fc74`.
- Implementation evidence: `01dca854cd3048c0d5adece7e2325a2fb9e5abde3c512d75f5169f555c282966`.
- Independent validation manifest: `c844d531b66f33713746dee969a7d7a943bf21734032978cc008610d4c4f64bd`; critique manifest: `8ee6ccb38ba405d6a9c5d92edc073e73a01ad7ef44bce8fdb0cec4a95bd2c72f`.
- `shasum -a 256 -c` passed for the candidate and implementation-evidence manifests.

## Why it is rejected

Independent validation failed at **48/84** class-specific rows and only 1/11 local R19 oracles passed. It found generic witnesses, aliases in end/envelope/attachment/drain families, polygon rotation-symmetry failures, malformed SVG paths in Chromium/WebKit, and a zero-area `surface.spiral.softness` target. The label and attachment mini-panels were empty in all six contexts.

Independent critique is `BLOCK`: blank label and attachment teaching panels, polygon side counts that collapse into generic proxies, and end-profile states too weak for caption-hidden comprehension. There is no formal review, delivery, live-route, CAD, OpenSCAD, STEP/export, slicer, printing, fit, or physical claim.

## Size and evidence hygiene

The R19 candidate source is 5 files / 15 lines / 16,244 bytes; tests are 5 files / 85 lines / 6,466 bytes; R19 Markdown is 6 files / 290 lines / 28,975 bytes. Independent R19 validation evidence is about 163 KiB. Old scratch files with millions of lines are expanded raw validation samples, not implementation source. Future evidence must retain compact summaries and hashes; later cleanup may only quarantine old scratch reversibly, never delete it in place.

## Required next action

Do not open an R20 implementation. Open a new design-only validation-contract iteration, create one small user-confirmable teaching view, and obtain independent review of a semantic-witness plan before any renderer work. Keep P2 R3 at <https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator/> (trailing slash) as the only live formally reviewed visual artifact, and keep P1 R7 as the CAD authority.
