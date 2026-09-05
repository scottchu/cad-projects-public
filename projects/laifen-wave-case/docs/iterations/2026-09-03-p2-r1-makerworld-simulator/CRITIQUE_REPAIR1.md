# CRIT-MW-01 repair 1 re-critique

**Status: HOLD — repair 1 resolves C-MW-01 and the accessible-text portion of
C-MW-04, but C-MW-02 and the visual portions of C-MW-03/C-MW-04 remain open.**
This is an independent product/visual critique of the exact repair-1 candidate,
not CAD, mesh, slicer, printability, fit, thread-strength, or physical approval.

## Scope and provenance

Owner: `/root/mw_sim_critic`, independent of implementation and validation. The
exact candidate manifest
[`inputs/implementation-candidate.sha256`](inputs/implementation-candidate.sha256)
has SHA-256 `3951e89f0fefe28f86e5d5eb470610c11cb54c6a39439fa96c33e29f1d712daa`;
every listed candidate file verified before review. Attempt 1 remains preserved as
the separate HOLD receipt [`CRITIQUE.md`](CRITIQUE.md) and its immutable evidence
manifest `b040747add6feb9b8c1b9ddd5b30d0ef773b1f5ce5d3cdd95eea31d725ea7793`.

The candidate page was served read-only from the preview directory at loopback
port 8992 and operated through root-venv Playwright/Google Chrome. Repair-1
evidence is frozen in
[`inputs/critique-repair1-evidence.sha256`](inputs/critique-repair1-evidence.sha256).
Only this receipt, that manifest, and the critic’s `scratch/.../repair1/` evidence
were written. No simulator source, test, CAD, route, service, slicer, or printer
state changed.

## Accepted screenshot evidence

| View | Evidence | Observation |
| --- | --- | --- |
| Desktop default, S=84 | `scratch/makerworld-simulator-critique/repair1/01-desktop-default.png` | Orange upper and teal lower outer skins meet at one thin yellow seam without the attempt-1 mottled overlap. The visible outer silhouette is one diameter. |
| Desktop S=50 / S=169 | `02-desktop-s50.png`, `03-desktop-s169.png` | The single seam moves to both permitted boundaries and neither view reads as a small top lid. |
| Device 250, visible percent maximum | `04-desktop-device250-percentmax.png` | The displayed max 64.751%, when replayed, yields S=169.00011000000003 and an avoidable red range error. |
| Smooth / wave-flutes | `05-desktop-smooth.png`, `06-desktop-wave.png` | At the same default front view, wave/flutes is visually indistinguishable from Smooth except for the select value. |
| Exploded | `07-desktop-exploded.png` | The seam follows the upper piece and the inner bands originate at the lower piece, avoiding the previous free-floating overlay. The translucent purple/white bands nevertheless look like a third tubular object protruding into the gap. |
| Mobile 50% | `08-mobile-percent50.png` | 50% maps to 109.5 mm and the responsive layout is readable. The canvas shows the clean two-piece silhouette; visible text readouts remain accessible below it. |

## Reopened finding disposition

### C-MW-01 — PASS — outer overlap and closed-silhouette failure repaired

The repair renders the lower exterior only through `z_seam` and the upper from
`z_seam`; desktop default/boundary and mobile evidence show a clean single-diameter
two-piece mid split. The 9 mm penetration is no longer rendered as competing outer
shells. This satisfies the visual core of **MW-REQ-01** without claiming that the
page is CAD or actual thread geometry.

### C-MW-02 — high, still open — visible percent maximum can create an invalid S

For device length 250, H=261. The adapter bounds are derived correctly in source,
but the number field publishes `64.751` via three-decimal rounding. That reachable
value maps to 169.00011 mm, and the captured page raises “Split must remain between
50 and 169 mm.” The candidate therefore still permits an advertised endpoint to
violate its own range.

This fails **MW-REQ-02**. Set the exact percent value/bounds in the editable
control (or clamp only a documented floating-point endpoint epsilon) so reading and
replaying either endpoint produces exactly S=50 or S=169 with no red state. Add a
browser regression using the displayed min/max after device-length changes, not
only the pure helper’s unrounded result.

### C-MW-03 — medium, still open — inner bands do not communicate thread placement cleanly

Repair 1 improves attachment: in exploded view the seam moves with the upper and
the inner full/effective bands originate at the lower piece. In assembled mode,
however, the inner bands are occluded by the uninterrupted outer surface; the user
only sees a seam. In exploded mode, the transparent purple/white annulus extends
into the gap with no direct label and reads as a third tube more readily than an
inner visual-accounting guide.

This remains short of the BRIEF use sequence that the user can observe the thread
band move, and weakens **MW-REQ-07**’s full/effective-band communication. Keep the
single outer silhouette. Add an explicit, non-solid visual convention for inner
thread ranges—such as labelled dashed axial guides or an optional labelled
cutaway—and give “Full thread band” and “Effective portion” separate legend
entries. The presentation must continue to label these as visual accounting, not
actual CAD thread geometry.

### C-MW-04 — partial pass — text alternative repaired; wave/flute visual choice remains weak

The live `visual-summary` now reports S, global piece spans, selected pattern,
full/effective bands and display mode. Together with labelled number adapters and
the textual readouts, it is a meaningful non-visual alternative for this narrow
intent gate; this is not a claim of broader accessibility compliance.

At the accepted desktop camera, Wave / flutes and Smooth render as essentially the
same smooth orange/teal cylinders. Pattern selection is visible only in the select
text, so a visual user cannot judge the intended alternative skin. This leaves the
visual part of **MW-REQ-06** open. Use a materially legible wave/flute relief or
a default lighting/camera treatment that visibly exposes it, then compare Smooth
and Wave at the same viewport/state.

## CAD/print boundary

All reviewed desktop and mobile states retain the readable warning that this is a
visual axial-accounting model, not CAD, printable geometry, a thread-fit proof,
wall-thickness proof or device-retention proof. No screenshot or this receipt is
used as fabrication, fit, or physical evidence.

## Commands and handoff

```sh
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r1-makerworld-simulator/inputs/implementation-candidate.sha256
node projects/laifen-wave-case/tests/test_makerworld_simulator.mjs
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 -m http.server 8992 --directory projects/laifen-wave-case/preview
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 projects/laifen-wave-case/scratch/makerworld-simulator-critique/repair1_capture.py
```

Candidate verification and the Node suite passed before and after capture. A
further bounded implementation repair is needed for C-MW-02 and the remaining
C-MW-03/C-MW-04 visual failures. It will change the candidate manifest and
requires new independent validation and critique before formal review or delivery.
