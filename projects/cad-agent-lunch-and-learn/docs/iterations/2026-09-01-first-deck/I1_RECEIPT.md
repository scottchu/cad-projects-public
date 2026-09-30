# I1 implementation receipt

Status: complete candidate; independent browser validation and formal review remain pending.

Frozen D1 input manifest was verified before implementation: `DESIGN_INPUTS.sha256` SHA-256 `520a8871f4056ae9278c7210f2f543cb5a7be627cbb65245776400f0bc94cb46`, 26/26 entries OK.

Implemented `index.html` as a 22-slide standalone offline deck. It embeds the two D1-inspected historical CAD PNGs as data URIs and contains inline CSS, JavaScript, presenter notes and offline source summaries/limitations. It has the two prescribed exercises, print answer fallback, keyboard navigation, overview, notes, source references, fullscreen request and reduced-motion styling.

Commands run from repository root:

```sh
npm run build --workspace cad-agent-lunch-and-learn
npm run check --workspace cad-agent-lunch-and-learn
shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-01-first-deck/CANDIDATE.sha256
```

Results: build wrote a 741,485-byte `index.html`; focused Node tests passed (22 sections, two embedded PNG data URIs, required navigation/interaction controls, source IDs, print/reduced-motion rules, no HTTP(S) runtime links, and inline-script parsing). An isolated CDP browser fresh-loaded `file://` with slide 1 active, then loaded slide 22 by hash, with zero runtime exceptions. All 10 candidate-manifest inputs verified.

Candidate manifest: `CANDIDATE.sha256` SHA-256 `bcdbdacf4e1d7c86b0345f1edef5d107a22559dc48deaa2146c14c6b1cc54231`. It covers the actual builder, generated HTML, package metadata, focused tests, usage documentation and frozen narrative/evidence inputs. It excludes mutable coordination BRIEF, status and validation/review records.

Repair cycle 1 fixed the generated inline-script syntax; per-slide source lookup now parses the embedded source register rather than depending on a previously opened drawer. It restores the slide-18 long-term-direction qualifier and expands offline S08/S09 provenance. CSS repairs preserve inactive slides, separate the slide-4 count groups, make the slide-5 CAD view dominant, fit the slide-10 caption, compact the revealed slide-17 exercise, add slide-8 spacing, and keep overview/notes controls available on narrow screens.

I2 implements the D2 bounded contract. The builder now derives all eleven S08 Kage amendment names and hashes from `docs/SOURCES.md` with a completeness guard; the focused check compares every generated row. Print page sections have an explicit zero margin and use a descendant-only sequence selector. The final mobile Kage rule uses full content width and a normal-flow caption. Author checks: build and four focused Node checks passed; written landscape PDF inspection reported exactly 22 pages; at 390 × 844 the Kage map measured 335.4 px wide with a visible normal-flow caption. Candidate SHA-256: `b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`.

Known limits: these are author checks only. Browser rendering, overflow, keyboard behavior, print pagination and factual/visual review require the assigned independent V1 and R1 gates. The presentation makes no CAD, slicer or physical acceptance claim.
