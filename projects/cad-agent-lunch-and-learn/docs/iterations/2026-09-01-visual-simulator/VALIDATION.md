# Independent validation

## V2-V initial candidate — REJECT

Owner: `/root/presentation_visual_validation`, distinct from implementation and critique. Date: 2026-09-02. Frozen design manifest `6449532b4b7e1a11537973eb9921350ea4072a7df5931c46d3f1209e51bbcc79` verified 29/29 before and after. Candidate manifest `98a10b7911f343ca20b398d65c6a3fd96e0ffe3cf1032a0a623dc18a7c60e40a` verified 6/6 before and after; HTML `0137256dd33156955f9e9382b230b7667ceabe6cc4bf62d6d7e3b6ab8138ec05`. No source, build, package, host or source-project changes by this validator.

### Material findings

- **V-01 P1, REQ-013:** `CylinderGeometry(4.4, bore, 2.4, ..., true, ..., 1.5π)` is a tapered open cone segment, not the required annular sleeve. Its axial radius varies, so metric arithmetic and visible clearance describe different geometries. Actual default/interference screenshots confirm the taper. Repair gate: independently measure the generated mesh's constant inner/outer radii, axial ends and cut faces across default/contact/interference/extremes; a nonempty canvas alone cannot validate this.
- **V-02 P1, REQ-014:** forced no-WebGL mode reports “section view shown” while `#fit-fallback` has computed `display:none`; setting `hidden=false` does not override its CSS. Moreover, its circle update `r=40+140*C_r`, with stroke width 28, yields an inner boundary unequal to the fixed rod radius 40 at contact and changes the supposed outer radius. At the negative extreme the sleeve disappears behind the rod. Repair both visibility and actual section arithmetic; test initialization failure and context loss.
- **V-03 P1, REQ-014:** written PDF page 6 depends on interaction state: after H=4.05/e=-0.25 it prints assumed diameter 3.80, diametral -0.20 and radial -0.100, contrary to fixed default H=4.15/e=0.00. The displayed section is also affected. Require a static labeled default section and default metrics independent of interaction, with observations revealed.
- **V-04 P2, REQ-012/014:** slide 3/20 connectors are detached from nodes and lack readable arrowheads in inspected laptop images. CSS hides their SVG completely on narrow screens and print. Required convergence, feedback and fork/join relationships do not survive these layouts.
- **V-05 P2, REQ-009/014:** the mobile reveal click reached the fixed Overview toolbar, so resulting mobile 6/10/13/20 captures show Overview and are invalid slide evidence. Repair control/toolbar separation and verify actual tap targets and scroll behavior. Coupon source text is extremely small in the inspected PDF; critique owns the complementary legibility finding.

### Evidence and limits

Independent harness copy `independent-v2.mjs` SHA-256 `d53ad093c1a3214aacbc467186555f160296133a95ecfa3fc3a88e93fe2a5d35` ran in a fresh isolated Chrome/SwiftShader profile for each mode, without dependencies or user browser state. Evidence roots: `/tmp/cad-agent-visual-validation/independent-0137256dd331-{normal,fallback,reduced}/`. These are separate from the author's earlier harness invocation.

Exact commands (repository root for manifests):

```
shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-01-visual-simulator/CANDIDATE.sha256
shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-01-visual-simulator/FROZEN_INPUTS.sha256
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-visual-validation/independent-v2.mjs /Users/scottchu/.codex/worktrees/740e/design-projects/projects/cad-agent-lunch-and-learn/index.html 0137256dd33156955f9e9382b230b7667ceabe6cc4bf62d6d7e3b6ab8138ec05 normal
```

Repeated the last command with `fallback` and `reduced`. Numeric/default/control smoke checks: 23/23 normal, 22/23 fallback (section invisible), 23/23 reduced-motion. The independently calculated integer-hundredth oracle checks seven H/e combinations including exact contact, interference and both extremes. Actual WebGL draw calls and nonzero canvas, parameter updates, hidden-slide render stop, keyboard guard, full/camera resets, away/back state, notes, source drawer and exercise 2 passed. Every run was offline, with zero runtime HTTP requests and zero uncaught runtime exceptions. These smoke results do not override geometric or visual failures.

Source drawer content and both embedded image hashes are byte-identical to the first-deck snapshot (`preservation.json`). Coupon text remains unchanged by hypothetical controls.

```
swift /tmp/cad-agent-visual-validation/pdf-inspect.swift /tmp/cad-agent-visual-validation/independent-0137256dd331-normal
```

Actual PDF has 22 landscape pages at 960×540 points. Inspected PNGs: default/interference model, laptop slide 3/20, invalid mobile capture, and PDF page 6. PDF text confirms the incorrect interactive print state. Additional screenshot sets and extracted PDF text are available, but full visual acceptance, pointer orbit/zoom and context-loss checks were deliberately stopped once material failures were established. No CAD, manufacturing, slicer or physical acceptance is claimed.

Next: one consolidated implementation repair, freeze a new candidate, then rerun affected geometric/fallback/print/diagram/mobile gates and join distinct critique and formal review. Initial read-only gate released to implementation.

## V2-V repair 1 — REJECT

HTML `bc0b7920e4ec964606e2155ce684cba571616e0b9ce48a4559e58355879683d1`; candidate manifest `0c00fc2eb67a4e0a072e4dc6835d8c6225fc483ad1356be16c5833339cd85058`. Candidate 6/6 and unchanged frozen design 29/29 verified before and after. Same independent validator; no implementation mutations.

- **V-01 resolved:** independent `geometry-repair1.mjs` executes the exact authoritative `sleeveGeometry` function using the installed Three.js. Five signed clearances generate 1164 vertices each: outer radius 4.4; bore radii 2.6, 2.0, 1.8, 1.2 and 3.4; axial ends ±1.2, all within 1e-5. Both radial cut faces each have two triangles; all coordinate-welded triangle edges have incidence two. Source rod rotation aligns the cylinder with the sleeve's Z axis. Actual browser snapshot confirms an annular cutaway. Mesh evidence is illustrative, not production-solid or physical acceptance.
- **V-02 resolved:** `focused-repair1.mjs` tests both forced initialization failure and real `WEBGL_lose_context` loss. Each visibly exposes the section/status. At H4.15 and e0/-.15/-.20, SVG outer/rod radii remain 88/40 and bore becomes 52/40/36, matching the signed ×8 formula. Further tested e-.25/+.10 with correct current metrics. No calibrated fit claim is inferred.
- **V-03 remains P1:** actual 22-page PDF now has a **blank exercise on page 6**: only heading, number and source footer remain. Neither required default values nor observations appear. The dedicated `print-fit` element is nested in the hidden exercise layout. `independent-bc0b7920e4ec-normal/print-6.png` and extracted `print-text.txt` are direct evidence. Require actual rendered PDF content, not page count or source-string presence.
- **V-04 remains P2:** independently inspected laptop slide 20 has Formal review/Evidence boxes overlapping and a detached validation branch. Mobile slide 3 paths are disconnected from nodes, with no readable arrowheads. Corresponding images confirm the critic's findings.
- **V-05 tap obstruction resolved; label legibility remains P2:** at 390×844, actual pointer hit-test and click reach `reveal-fit`, observations become visible, Overview remains closed, document width is 390. However, computed observation-context text is **4.992 px**, so that essential evidence label remains unreadable. The root/critic's typography repair must cover screen and print.

Commands: same manifest commands and independent harness as above with repair-1 hash (`normal`: 23/23 smoke checks), plus:

```
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-visual-validation/geometry-repair1.mjs
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-visual-validation/focused-repair1.mjs
swift /tmp/cad-agent-visual-validation/pdf-inspect.swift /tmp/cad-agent-visual-validation/independent-bc0b7920e4ec-normal
```

Evidence: `/tmp/cad-agent-visual-validation/geometry-repair1.json`, `/tmp/cad-agent-visual-validation/focused-bc0b7920e4ec/`, and `/tmp/cad-agent-visual-validation/independent-bc0b7920e4ec-normal/`. Inspected actual default geometry, laptop slide 20, mobile slide 3 and written PDF page 6. Focused source/candidate verification remained exact; browser sessions closed. Stopped further testing once remaining material failures were proven. Next: bounded second repair for flow layout, visible deterministic print exercise and essential typography, then affected gates on its new fingerprint. Read gate released.

## V2-V repair 2 — PASS

Final independent validation owner: `/root/presentation_visual_validation`. HTML SHA-256 `9f246ce8a7e52b24ca8c9b2414544b4d21f44628eb98a5150d5a3b75b8cb22c8`; seven-file candidate manifest SHA-256 `8f62e12039798d71983d0e76a412c7bf2f349bb17b0d5b02ced9f387b332d1d3`; frozen design manifest remains `6449532b4b7e1a11537973eb9921350ea4072a7df5931c46d3f1209e51bbcc79`. All 7/7 candidate and 29/29 frozen-input checks passed before and after. No material validation findings remain.

- **V-01/V-02 retained PASS:** current simulator hash `eb78fb051d0b6d59b641f3b84f739108a7d6eb3ffdc96cd5da4d33c7aa65d2cc` matches the repair-1 source identity documented in the implementation receipt. That source is unchanged; its independent five-state annular mesh and real context-loss/no-WebGL evidence above remains applicable. Final browser again renders the annular model and changes it with inputs. No redundant mesh run was needed.
- **V-03 resolved:** independent browser printed the actual candidate after changing live H to 4.05 and e to -0.25. Reopened PDF has exactly **22 landscape 960×540-point pages**. Page 6 visibly contains the fixed H4.15/e0 example, assumed diameter4.15, nominal/hypothetical diametral +0.15, radial +0.075, Geometric gap, labeled rod/sleeve section, explicit ×8 exaggeration and all five coupon observations plus context. These appear in rendered pixels and extracted text. It no longer depends on live state or disappears with the interactive layout.
- **V-04 resolved:** inspected independent laptop, projector, mobile and print flow images. Expected/Observed converge on Gap; experiment/composition/observation continue with an arrow back to Observed. Implementation forks to Critique/Validation and rejoins before Formal review; Evidence follows review. Arrowheads and node connections remain visible, with no overlapping review/evidence boxes. Mobile uses a complete stacked diagram and normal scrolling.
- **V-05 resolved:** at390×844, actual pointer hit-test targets `reveal-fit`; click reveals observations without opening Overview. Document width remains390 and the observed-coupon context computes to **14px**. Independently inspected the scrolled revealed state. Kage mobile layout and evidence table were also visually checked for shared-layout regression.

Fresh final-candidate normal harness: 23/23 focused numeric, WebGL/control, hidden-render, reveal/reset, preservation-of-state and delivery smoke checks; zero runtime HTTP requests while offline, zero runtime exceptions. Source drawer and both embedded-image hashes remain byte-identical to the original snapshot. The unchanged source retains prior reduced-motion/no-continuous-render evidence. These checks and visual review concern the HTML teaching artifact only; no source CAD, slicer, manufacturing or physical acceptance is inferred.

Exact commands: manifest commands above; normal harness command above with final HTML hash; then:

```
/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-visual-validation/focused-repair2.mjs
swift /tmp/cad-agent-visual-validation/pdf-inspect.swift /tmp/cad-agent-visual-validation/independent-9f246ce8a7e5-normal
```

Independent evidence directories: `/tmp/cad-agent-visual-validation/independent-9f246ce8a7e5-normal/` and `/tmp/cad-agent-visual-validation/focused-9f246ce8a7e5/`. Actual visually inspected renders include laptop slides3/13/20, projector20, mobile3/10/20 and revealed6, plus PDF pages3/6/20. PDF text was inspected for all22 page identities and page6 values. Original rejections remain above for traceability; their findings are closed by the exact final candidate. Browsers closed; no implementation rebuild or mutation performed. Next: distinct formal review joins this receipt with critique and final provenance.
