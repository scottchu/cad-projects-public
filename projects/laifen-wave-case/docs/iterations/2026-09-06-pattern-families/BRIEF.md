# Pattern families brief — PF-DES-01

Baseline: `c181dda780a3b9c407ebe3419702419254266792`.
Frozen inputs: `inputs/baseline.sha256`, 26 paths, verified before design;
SHA-256 `b35ca7cda070f2470b38f60b0e7b6ac20912c9972ea66ac073501cf3c0a5ac5e`.
Source authority remains `openscad/laifen_case_customizer_v1.scad`; this is
an exterior extension of the accepted private browser customizer.

The user accepted Smooth/Diamond and requested a few more simple mathematical
patterns, each with its own parameter group immediately below the selector.
Use Ribs, Rings and Spiral as the proposed additions after the user's Continue.
This request authorizes the scoped SCAD extension and editable Diamond size/depth.

| ID | Class | Contract / evidence |
| --- | --- | --- |
| PF-01 | Invariant | Five choices: Smooth, Diamond, Ribs, Rings, Spiral. Browser default/Reset is Smooth. Verify actual selector and generated geometry. |
| PF-02 | Invariant | Only the selected family group is visible directly beneath the selector, before Container options. Smooth has no parameter group. Browser check. |
| PF-03 | Invariant | Two controls per textured family, slider plus exact number entry with current allowed limits. Preserve each group's raw values, including invalid text, on switching. State and browser checks. |
| PF-04 | Invariant | Selecting/editing only invalidates the current result; explicit Generate starts a fresh owned job. Inactive invalid groups never block generation; Reset restores all groups. Lifecycle checks. |
| PF-05 | Invariant | Smooth and Diamond at the original default tuple retain exact geometry; thread, bore, floor, chamfer, drainage, joint and four output semantics remain unchanged. Default byte parity and protected-feature sections. |
| PF-06 | Invariant | Texture cuts inward from the same crest OD, with global phase shared across body/cap. No external smooth shoulder collar on the new families. Actual seam/radial checks and images. |
| PF-07 | Derived | Source, adapter, schema and feasible sliders share selected-family limits, ligament allowances and bounded mesh allocation. Independent boundary oracle and actual artifacts. |
| PF-08 | Invariant | Retain desktop canvas left/controls right, pinned phone canvas, icon actions, current-only download and drain/count behavior. Desktop/mobile observation. |
| PF-09 | Physical unknown | Grip, cleaning, support-free printing, fit, wear and strength remain unproven. No slicer or physical approval follows from this gate. |

Use sequence: select a pattern; adjust its size/spacing and depth; inspect the
visible allowed limits; press Generate; inspect the actual model; download only
the current successful output. Product copy uses everyday words, not CAD terms.

Units are mm. +Z follows the container axis; body starts at global Z=0 and cap
starts at `body_thread_z`. End/chamfer and protected internal geometry use the
existing source coordinates. Historical P1 R7 STEP remains a separate authority.
The documented no-collar/full-sidewall preference supersedes old smooth-margin
wording for this surface gate. No new physical measurements were supplied.

Design choices: shallow cosine valleys for the three additions; two controls
per family; fixed six-start Spiral; fixed Diamond aspect ratio. Alternatives
rejected: height-dependent turn count (changes pitch), new noise/Voronoi fields
(needless complexity), and generic body blank routing (adds a visible collar).

Do not migrate to another CAD engine, add dependencies, edit the pinned worker
or engine, alter 8448/Tailscale/printer/public hosting, or merge main. Preserve
8453 on its accepted build until independent gates pass. Generated pilot STL,
renders and logs belong in task scratch; retain compact commands/hashes/receipts.

First done gate is the small actual-source Spiral pilot in DESIGN.md. Only then
complete the families/UI and run distinct critique, validation and formal review.
Root owns coordination and continuity indexes; this role owns only BRIEF/DESIGN.
