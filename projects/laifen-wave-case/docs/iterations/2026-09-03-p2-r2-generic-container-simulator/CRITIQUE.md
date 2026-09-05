# CRIT-GCS-01 independent generic-container simulator critique

**Status: HOLD — generic dimensional accounting works, but the frozen visual
candidate does not yet accurately communicate a closed-end container or a
non-object thread marker.** This critique is visual/product evidence only; it
does not approve CAD, thread geometry, clearance, wall, printability, fit,
drainage, strength, slicing, or physical acceptance.

## Scope and provenance

Owner: `/root/mw_sim_critic`, independent of the implementation and validation
roles. The supplied candidate manifest
[`inputs/implementation-candidate.sha256`](inputs/implementation-candidate.sha256)
SHA-256 `4acefaf383cd7b0e0425f5da23e5ca19612920ede43df469db3f1ac16cbf228d`
verified before and after review. The frozen P2 R2 design-input fingerprint
`aea717d84cc31b67b345ed9367f6c5ae72b2a370291aa55e75ce1662238574df`
also verified against `inputs/current-baseline.sha256`.

The candidate was served read-only from its preview directory on loopback port
8993 and captured through root-venv Playwright/Google Chrome. This critic wrote
only `scratch/generic-container-critique/`, this receipt and
[`inputs/critique-evidence.sha256`](inputs/critique-evidence.sha256). No
implementation source/test, CAD, route, service, slicer or printer state changed.

## Observed functional coverage

| State | Evidence | Observation |
| --- | --- | --- |
| Generic / Laifen | `01-desktop-generic.png`, `02-desktop-laifen.png` | H=120/OD=60 and H=219/OD=39 produce visibly taller/narrower forms; Laifen reads E=6, P=9 and 3 turns. |
| Wide short jar / 3 turns | `03-desktop-wide-short.png`, `04-desktop-wide-short-3turn.png` | H=55/OD=80 produces a wide short form. One turn reads E=3/P=7.5; three turns reads E=9/P=13.5 with changed split bounds. |
| Raw percent endpoint | `06-desktop-percent-boundary.png` | H=261 max percent `95.24904214559388` maps exactly to S=248.6 and remains valid. |
| Relief and patterns | `07-desktop-magnifier.png`, `09-desktop-helix.png`, `10-desktop-wave.png` | Main model remains visually shallow at true scale. The labelled 4× magnifier for 0.20 mm is honest; the surface-detail panel visibly differentiates diamond, helix and wave. |
| Infeasible / mobile | `08-desktop-infeasible.png`, `11-mobile-wide-short.png` | No assembled exterior is rendered at H=20; the exact required-height error is shown. Mobile content is readable and not clipped, although control density remains high. |

## Findings

### C-GCS-01 — high — rendered pieces are open shells, contradicting the closed-end datum

The design and brief define two closed-end pieces, with global z=0 and z=H at
their closed outer ends. `shell()` creates only side-wall surface strips and no
end faces. The generic, Laifen and wide-short screenshots visibly show a black
open upper rim; the thread-marker arcs are seen through it. Thus the user cannot
visually identify the upper closed-end datum that “from top” is measured from,
and the simulator reads as two open sleeves rather than the promised container.

This fails the closed-end/use-sequence intent in **GCS-01** and the top-datum
semantics of **GCS-03**. Add display-only closed-end faces or unambiguous opaque
end discs at global z=0/H, preserving the explicit visual-model boundary. Then
show a top-reference marker/label in the same view; do not imply CAD solids or
functional end/floor geometry.

### C-GCS-02 — high — “thread band” arcs read as a third object, not a marker

The wide-short assembled and exploded views show two large purple/yellow arcs
arching through the open top. They are derived from external torus rings and a
line, and at the selected camera they look like a handle or a third wire/tube.
They do not show which arc is full versus effective, nor do they make 1 versus 3
turns visually legible. The legend names “purple ticks/bracket”, but does not
label the individual endpoints in the scene.

This fails **GCS-06** and weakens **GCS-04**/**GCS-09**. Replace the ring arcs
with a screen-readable, clearly external axial bracket/ticks at the silhouette
side, label `P full visual band` and `E effective` separately, and keep it a
thin marker rather than a 3D form. In exploded view, attach the two bracket ends
to their respective existing pieces or label the gap as an exploded visual guide.

### C-GCS-03 — medium — infeasible state still exposes nonsensical geometry data

At H=20, the exterior correctly disappears and the status reports
`Required H >= 2*(F+P+K) = 29.00 mm; received H = 20 mm.` However, the same
screen still reports full thread band `-7.50–0.00`, effective `-7.50–-4.50`, and
the hidden live summary says the lower/upper spans are `0 to -7.5` and `-7.5 to
20`. The surface-detail pattern remains labelled true-scale although there is no
valid container state.

This is contrary to **GCS-05**’s requirement to render no false assembled split
and to state the infeasible condition as an exact, comprehensible model state.
When infeasible, replace span/band outputs and the live summary with “no valid
seam or thread-band placement”; retain a compact parameter ledger that explicitly
lists F, P, K, S_min and S_max alongside the inequality. Label or hide the detail
panel as unavailable for that invalid geometry.

### C-GCS-04 — medium — mobile accessibility is structurally present but live derived state is not announced

The 412 px view keeps all controls/readouts visible, and labels/`role=status`
provide a reasonable base. It packs nineteen controls into an undifferentiated
two-column panel, which makes a preset-first mobile decision laborious. More
materially, `#live` contains the changing split/spans/turn state but has neither
`role=status` nor `aria-live`; the only live message for valid edits is “Valid
visual parameter state.” A screen-reader user is not told that a turn, E/P or
split state changed.

This leaves **GCS-09** incomplete. Group inputs into “shape”, “thread” and
“surface/detail” fieldsets (preset first), associate help/error text with the
relevant controls, and make the concise derived live summary an atomic polite
status message. This is an accessibility improvement, not a CAD claim.

## What passed within this critique

The generic and wide-short presets are meaningfully different in visible H/OD
proportions and readouts. Selecting turns changes E, P and bounds as required;
the exact raw percent endpoint holds after H changes. The main relief is not
silently inflated, and the detail panel truthfully reports 1× or 4× radial
display and requested depth. Pattern identity is distinguishable in that panel
even when shallow true-scale relief is intentionally subtle in the full model.
All reviewed states visibly preserve the non-CAD/non-print/non-fit boundary.

## Commands and handoff

```sh
sha256sum -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r2-generic-container-simulator/inputs/implementation-candidate.sha256
node projects/laifen-wave-case/tests/test_generic_container_simulator.mjs
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 -m http.server 8993 --directory projects/laifen-wave-case/preview
/Users/scottchu/.codex/worktrees/4f8c/design-projects/.venv/bin/python3 projects/laifen-wave-case/scratch/generic-container-critique/capture.py
```

The candidate manifest and Node suite passed before and after visual capture. A
distinct implementation repair must resolve C-GCS-01 through C-GCS-04; it will
invalidate this candidate and require new independent validation and critique
before formal review or private delivery.
