# CRIT-GCS-01 repair 1 re-critique

**Status: HOLD.** Repair 1 replaces the handle-like hoop with a usable line
bracket and validates domains, but it does not fit the camera to supported
generic forms. Invalid-state and live-derived-state failures also remain. This
is visual/product evidence only, not CAD, thread geometry, fit, wall,
printability, slicer, or physical acceptance.

## Scope and provenance

Owner: `/root/mw_sim_critic`, independent of implementation and validation. The
exact repair-1 candidate manifest
[`inputs/implementation-candidate.sha256`](inputs/implementation-candidate.sha256)
has SHA-256 `8e3d7cd62d4c46c80a0d11865bc8fc39a36e1f943920e3051e130f948ec29e81`.
Every candidate file verified before and after review. Attempt 1 remains preserved
as the separate HOLD receipt [`CRITIQUE.md`](CRITIQUE.md), whose evidence manifest
is `bd7d41e37912e05b2a28185043cef900298278286f4a3193c8d7b75610c56dc2`.

The page was served read-only on loopback port 8994 and captured with root-venv
Playwright/Google Chrome. This critic wrote only `scratch/generic-container-critique/repair1/`,
this receipt and [`inputs/critique-repair1-evidence.sha256`](inputs/critique-repair1-evidence.sha256).
No candidate source/test, CAD, route, service, slicer, or printer state changed.
The repair-1 evidence-manifest SHA-256 is
`8e767d5164667b7ac842063c0e7869128dd567457fbb279f5f3f5693944ffc9a`.

## Accepted visual evidence

| State | Evidence | Observation |
| --- | --- | --- |
| Desktop Laifen assembled/exploded | `repair1/01-desktop-laifen-assembled.png`, `02-desktop-laifen-exploded.png` | Only the teal lower piece is in frame. Orange upper, seam, bracket and upper closed end are outside the canvas. |
| Desktop jar assembled/exploded | `03-desktop-jar-assembled.png`, `04-desktop-jar-exploded.png` | An opaque orange top disc makes the jar read as closed. Purple/white LineSegments form a small external bracket rather than an arch/handle. |
| Desktop wide custom | `05-desktop-custom-wide.png` | H=88/OD=120 fills/crops the canvas vertically; its intended wide-short relationship cannot be assessed. |
| Chamfer 8, drains off | `06-desktop-custom-no-drain-chamfer8.png` | Same top/side geometry as the preceding custom state. Chamfer and drains change only readouts. |
| Invalid H=20 | `07-desktop-invalid.png` | Shells disappear and the exact inequality is visible, but negative bands/spans and an apparently available surface detail remain. |
| Mobile Laifen / jar | `08-mobile-laifen.png`, `09-mobile-jar.png` | Laifen repeats the single teal-piece crop. The jar is fully visible but has a long dense two-column parameter form below it. |

## Reopened finding disposition

### C-GCS-01 — high, still open — fixed camera prevents generic H/OD/top-datum review

Repair 1 adds visual end discs: where the existing camera happens to fit the jar,
the opaque orange disc makes the upper end look closed. It does not make the
generic simulator viable. Both desktop and phone Laifen views show only teal
lower exterior; the upper piece, seam, bracket, upper closed end and top datum
are absent. The H=88/OD=120 custom form crops at both canvas edges. The fixed
camera/target therefore prevents users from verifying how H and OD drive the
complete container for the required long and wide forms.

This fails **GCS-01**, visual **GCS-03**, and **GCS-06**. Refit target and
distance from current H/OD bounds after every valid edit, including exploded
separation. Preserve a user-selected orbit after manual interaction, but frame
initial/preset views to include both pieces, seam, bracket and top reference.

Closed-end semantics are only partial as well: changing chamfer to 8 and drains
off leaves the same visual surface. DESIGN calls drains a visual open-hole
indicator and describes an end-treatment reference. Add a clearly labelled
display-only end indicator/treatment without suggesting a fabricable feature.

### C-GCS-02 — PASS — repair removes the third-object/handle reading

Jar assembled/exploded views show a small external LineSegments bracket and its
white effective sub-bracket. It no longer crosses the vessel as a hoop, tube or
handle. Legend plus full/effective textual readout make it visual axial thread
accounting. This repairs the marker portion of **GCS-06**/**GCS-09**. The camera
HOLD above prevents validating it for Laifen.

### C-GCS-03 — medium, still open — invalid state publishes false geometry

At H=20, the scene clears shells but the visible readout reports full
`-7.50–0.00` and effective `-7.50–-4.50` bands. The hidden live state reports
negative spans, and surface detail remains rendered as if a valid form existed.
This remains a **GCS-05** failure. On invalid input, replace span/band/readout
with “no valid assembled seam or thread band”, show F/P/K/S_min/S_max beside the
inequality, and hide or label detail as unavailable while retaining raw inputs.

### C-GCS-04 — medium, still open — derived state is not announced

The capture confirms `#live` has neither `role` nor `aria-live`. Shared status
announces only “Valid visual parameter state” after a normal edit, not split,
E/P, turns, or feasible range. The 412px view is not clipped but its nineteen
flat controls in two columns make editing laborious and offer no grouped
help/error relationship.

This remains incomplete for **GCS-09**. Make concise derived state an atomic
polite live status, relate errors/help to controls, and group shape/thread/surface
controls while preserving keyboard access.

## Passing repair evidence and limits

`deriveContainer()` now explicitly validates numeric domains, enum/boolean
fields, bore overrides and integral drain count before a state becomes feasible.
The current Node suite passes. Jar screenshots show the repaired end disc and
LineSegments bracket where camera framing exposes them. Every state retains the
visible non-CAD/no-fit/no-print boundary.

## Commands and handoff

```sh
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/implementation-candidate.sha256
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 -m http.server 8994 --directory projects/laifen-wave-case/preview
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 projects/laifen-wave-case/scratch/generic-container-critique/repair1_capture.py
```

Candidate verification and Node tests passed before and after capture. A bounded
implementation repair is needed for C-GCS-01, C-GCS-03 and C-GCS-04, followed by
new independent validation/critique before formal review or private delivery.
