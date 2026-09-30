# F-V targeted validation

## Current: repair1 PASS

Status: **PASS**. Independent owner `/root/first_layer_validator`. HTML `c8766aeb3d0c03f0332e226b55a896bc33d52c21da0969f5a9263626cfb9dfa7`; manifest `71673185ca5f4f88e512ae74ff7356b2247641e0290ef34443c097861d03a709`, all 14 entries verified before and after refreshed capture. No remaining factual or presentation-validation blocker.

The initial P2 finding below is **closed**. The left caption now reports faces above the bed and incomplete/floating early layers, matching S01. Both orange-band labels explicitly identify schematics; the right caption explains the raised contact areas in ordinary language. S12 supports flat face down and raised features up. The visible disclaimer retains exaggerated geometry, non-toolpath status and unestablished successful physical print.

Independently verified repair1 parity against `/tmp/cad-first-layer-repair1-baseline`: CSS, both inline scripts and `simulator.mjs` are byte-identical. Only slide 5 changed relative to the original first-layer baseline; other 17 complete sections, navigation and fit geometry remain unchanged. Initial 5/5 test and fit-render evidence below carry through this explicit parity. No optional whole-deck test expansion was performed.

Affected outputs refreshed with `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-first-layer-validation/capture.mjs 71673185ca5f4f88e512ae74ff7356b2247641e0290ef34443c097861d03a709 /tmp/cad-first-layer-validation/repair1 repair`, then `swift /tmp/cad-first-layer-validation/pdf-inspect.swift /tmp/cad-first-layer-validation/repair1` (18 pages). This targeted run covers slide 5 at desktop 1280×800, compact 1178×820, mobile 390×844 with overlapping scroll continuation, forced no-WebGL compact/mobile and actual PDF page 5. Offline bed scenes render; forced fallback works; no uncaught runtime exceptions or horizontal overflow. Mobile heights are 1582 px WebGL / 1669 px fallback.

**Pixels reviewed before PASS:** desktop, compact, mobile top and continuation, compact fallback, mobile fallback continuation, and actual PDF page 5. The repaired captions and schematic labels are readable and complete. All claims/disclaimers/source footer fit at desktop/compact/print sizes. Read-only display and inherited navigation remain. Slides 4/6 desktop evidence carries unchanged.

Current evidence: `/tmp/cad-first-layer-validation/repair1/{report.json,parity.json,capture.log,deck-print.pdf,print-5.png,print-text.txt}` plus `1280x800-slide-5.png`, `1178x820-slide-5.png`, `390x844-slide-5*.png`, and `*fallback-5*.png`. Initial evidence remains at the parent folder. Current pixels and exact identity were delivered to the blind critic.

Coverage: REQ-005/006/007 source and schematic boundaries; REQ-009/014 offline, fallback and print; REQ-020 preserved sequence; REQ-021 read-only show-and-tell. Remaining limitation: this is a teaching illustration, not exact historical toolpath or new CAD/physical evidence. No production CAD, slicing, printer operation, Git or hosting change by this role. Next: distinct formal reviewer joins F-C and this F-V receipt against the exact repair1 candidate. Read gate released; no further validation work required unless declared inputs change.

## Historical: initial candidate FAIL

Initial status: **FAIL — one narrow source-fidelity repair required**. Owner `/root/first_layer_validator`, independent from writer and critic. Read gate released after this receipt; no authoritative source or artifact edits by validator.

Candidate: HTML `1a31ba1fc5b2f1b45773f69a902be2527aa75987f9ee41d46c059027bc0ec1e6`; `CANDIDATE.sha256` `80d2e8905cd9fc3bc848a0eb4c427859d7e4ce86f9a43dce3295d63404d393c8`, all 14 entries verified before and after capture. All eight frozen `INPUTS.sha256` entries verified. Baseline HTML `6ce17971db1871cc4bc2c8958359cc6a28e52e16b875f5dae4e838a876a41445`.

## Finding

- **P2 / blocking factual overstatement:** “The broad face started above the first layer. The slicer could not draw that face there” presents a stronger historical geometry/toolpath conclusion than S01 supplies. XT60 `EXPERIENCE.md:24–29` records large plate faces **above the bed** and incomplete/floating early layers, with a 0.25 mm first layer and a 0.10 + 0.10 mm thrust-land arrangement. It does not establish that a broad face was wholly above the entire first-layer band or an exact absent toolpath. The schematic can exaggerate a gap; the observed caption must retain the source's actual scope. Replace with source-faithful observation and explicitly identify the orange empty band as an explanatory illustration. This is a copy repair, not a new source-project/CAD requirement.

S12 independently supports the right-hand orientation claim: `p13-cad-source-domain-amendment.md:74–81` specifies flat/plain plate faces on the bed with hubs/lands up and authored planar footprints at Z=0. The embedded S12 record contains the verified path/hash and the source-contract versus print-outcome limitation. Visible physical-success disclaimer is accurate. Orange is an illustrative layer rather than an invented support foot.

## Completed evidence

- Existing checks: 5/5 pass, exact command `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node --test projects/cad-agent-lunch-and-learn/test/deck.test.mjs` from repo root.
- Browser capture: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-first-layer-validation/capture.mjs 80d2e8905cd9fc3bc848a0eb4c427859d7e4ce86f9a43dce3295d63404d393c8`. Chrome headless with SwiftShader, network forced offline before `file://` navigation. Three real WebGL contexts; fit 12 draw calls, bed pair increased total to 72. All scenes ready with visible canvases; zero external runtime resources or uncaught runtime exceptions.
- Forced no-WebGL: both bed scenes fall back, zero contexts/draw calls, both labelled static explanations visible. No replacement model controls or questions. Main source-reference buttons remain inherited navigation, not audience exercises.
- Pixel inspection completed: desktop 1280×800 slides 4/5/6, compact 1178×820 slide 5, mobile 390×844 slide 5 and overlapping scroll continuation, compact/mobile fallback, and actual PDF page 5. No horizontal page overflow; desktop/compact fit in viewport. Mobile is intentionally scrollable (1607 px WebGL / 1694 px fallback). Existing fixed navigation passes over content while scrolling but all content is reachable. Orange gap/layer bands are small but discernible on desktop; print and fallback provide larger labelled illustrations.
- Actual PDF: `swift /tmp/cad-first-layer-validation/pdf-inspect.swift /tmp/cad-first-layer-validation` reports **18 pages**. Page 5 is readable, complete, and uses the deterministic static illustration. No clipped claim, source footer, or evidence disclaimer.
- Scope: 18 sections before/after; **only section 5 changed**, other 17 byte-identical. Navigation markup and `const nav` source byte-identical; fit geometry function and fit camera branch unchanged. The first inline script changes only because embedded source data adds S12; it is not evidence of changed navigation. Simulator changes are confined to bed geometry and bed camera. Tests unchanged. Scoped checks recorded separately.

Evidence folder `/tmp/cad-first-layer-validation/`: `capture.mjs`, `report.json`, `capture.log`, `scoped-checks.json`, screenshots named `1280x800-slide-{4,5,6}.png`, `1178x820-slide-5.png`, `390x844-slide-5*.png`, `*fallback-5*.png`, `deck-print.pdf`, `print-{4,5,6}.png`, and `print-text.txt`. Captures were provided to the blind critic with candidate identity before source explanations.

Coverage: REQ-005/006/007 source and schematic boundaries (005 requires repair); REQ-009/014 offline/browser/fallback/print; REQ-020 sequence-preserving scope; REQ-021 read-only presentation. This is presentation validation only; no production CAD, slice, printer, or physical-print acceptance is asserted.

Next: writer makes the single copy repair, freezes a new candidate; F-V reruns affected pixels/print and source fidelity against the new manifest. Existing real-WebGL/fallback and unchanged-slide evidence may carry only after explicit source parity verification. Formal review remains pending.
