# SP-CRIT-RESUME — Candidate 03 browser review

## Disposition

**Chromium UI, output and lifecycle flow: PASS. Native Safari is unverified.**

This review is bound to commit `8068fbd` and Candidate 03 manifest
`412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`
(23 paths). Root performed the browser interactions because browser ownership
was exclusive; the critic independently inspected the resulting screenshots,
accessibility snapshots, byte receipts and Candidate 03 source. The valid
screenshots are under `/tmp/surface-pattern-browser`; the mislabeled
`mobile-compiling.png` is excluded because it was captured at 1280x900.

## Numbered browser flow

1. **Default and layout — PASS.** At 1280x900, Smooth was current by default.
   At the true 390x844 viewport, the preview rectangle remained fixed at
   `top=0`, `bottom=280`, `width=390` before and after control focus/scroll;
   the control panel scrolled independently and the footer action icons stayed
   reachable.
2. **Pattern selection — PASS.** `mobile-pattern-focus.png` shows two labelled,
   visible radio cards in one row, distinct Smooth/Diamond swatches, a native
   selected indicator and a clear keyboard focus ring. Root's state receipt
   confirms ArrowRight selected Diamond while preserving D69/W5.5/H267.4/T3,
   manual lid 136.7, both drains/N9 and Lid output, with no automatic job.
3. **Wall guard and repair — PASS.** `mobile-wall-error.png` and its
   accessibility snapshot preserve exact W4.3, keep Diamond selected, disable
   Generate, present one coupled alert, and expose the only repairing slider
   at a truthful 4.4 minimum. ArrowRight/Left repair reached W4.4 without a
   hidden clamp; the other ranges became available again.
4. **Complexity boundary — PASS.** At OD80/N68, literal lid 136.8 remained raw
   and blocked generation with the Diamond detail message. The lid slider
   advertised 136.6–136.7; entering 136.7 restored Generate. The accessibility
   snapshots show the same values and state.
5. **Edit, reset and download currency — PASS.** Pattern/output edits marked
   the visible prior mesh stale, removed the download, cancelled active work
   and did not generate. Reset restored Smooth and all accepted defaults with
   no job. The compact icon row retained accessible names for Generate,
   Cancel, Reset and Download.
6. **Actual output jobs — PASS.** Fresh pinned-worker Diamond body, lid,
   assembled and print-layout jobs completed in 3.822, 2.409, 11.111 and 6.489
   seconds. Browser Blob and downloaded STL byte/hash parity passed for all
   four; sizes and hashes are recorded in `/tmp/surface-pattern-browser/downloads.json`.
7. **Visual output review — PASS for browser presentation.** Desktop 3D and
   cutaway captures show continuous Diamond skin and seam, protected smooth
   interior, visible thread, closed top and drained bottom. The print-layout
   cutaway clearly separates both upright parts. This visual finding is not a
   substitute for the validator's mesh topology checks.
8. **Held real-worker ownership — PASS.** The candidate-bound initial run
   proved that Cancel followed by genuine late delivery left status, render,
   Blob and download unchanged. The first supersession comparison sampled
   changing worker progress text and was discarded. Corrected harness manifest
   `e5fd360c1c520d8dd6711e0a4c781f5a790533c43fe835653d7aae147a42fc9e`
   then replayed the affected gate: delivery of the superseded genuine result
   left `parsing`, currency, render, Blob and download exactly unchanged. Only
   the newest result installed once and enabled one Blob/download; its held,
   rendered and Blob SHA-256 values all equal
   `1799916b0c29b49bc0f7b82221fbd247e4b2d354e0a8bd382f25e6197600d693`.

## UX assessment and limits

The result addresses the reported mobile problems: the canvas remains visible
while parameters scroll, actions use one compact 44 px icon row, numeric
parameters pair exact entry with sliders, and each slider states its current
allowed interval or why no interval is available. The pattern choice adds no
math controls and explains Smooth versus the fixed Diamond grip with a compact
visual cue. Error recovery preserves raw values and identifies the relevant
participants without duplicate visual or accessible error text.

No further Chromium UX blocker is visible in the accepted captures. This does
not establish native Safari/iPhone behavior, full screen-reader or contrast
conformance, CAD/STEP acceptance, slicer/support behavior, grip, fit, drainage,
thread life, strength or physical-print acceptance. Safari remained unavailable
after `cgWindowNotFound`; the user's actual device remains the appropriate
final visual/touch gate.
