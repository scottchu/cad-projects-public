# P17 R2 fixed stepped-axle guide and motion brief

Status: `P17-R05` accepted for digital CAD/source, written STEP/export, and
live preview delivery. Physical/print acceptance remains pending. This is a
focused P17 R2 repair, not a `P` or `R` increment.

## Baseline and observed rejection

- Project: `projects/xt60-bend-jig`.
- Prior source: `src/xt60_bend_jig/p17_r2_direct_counter_twist.py`.
- Prior focused tests: `tests/test_p17_r2_direct_counter_twist.py`.
- Prior candidate `P17-I04` fingerprint: `24f5d7524303671a914eec18148b7cee0a8a297cca1403b2c2c68c714fdefabb`.
- Prior candidate remains historical digital evidence only. User visual review
  rejects it as the active product-direction candidate.
- Corrected frozen-input manifest: `/tmp/p17-d06-corrected-full-manifest.txt`,
  SHA-256 `f90a48de628340f8927395d87e7b54a41d172d97edc9b63ec4f07dbe49527b6f`.
  It is the original D06 manifest `4e40c6f...` plus the four supplied images.

Image evidence:

| Input | SHA-256 |
|---|---|
| `.../53219609-F596-40A5-8E14-0867D84C2208/1-Pasted-Image-1.jpg` | `71d4c407ae645a32cf616c6fc7f0e34f2c8c5ac1bd47e77ec8fec2a445a280e8` |
| `.../53219609-F596-40A5-8E14-0867D84C2208/2-Pasted-Image-2.jpg` | `6064cb5005bfb50f92c61ae9b48fd201efc6a8e898b875650a217c912e7b5bbb` |
| `.../53219609-F596-40A5-8E14-0867D84C2208/3-Pasted-Image-3.jpg` | `d2e59057a67dc348708812adb33e0ef47b7912faff50c6484974a5b58f2d06b1` |
| `.../B55E60F8-583B-4FAB-B574-A448109DDDBE/1-Pasted-Image-1.jpg` | `2a0b9383f9cbc990b78aadefdaac9daaf5f4b443c6a68fdbee05f4d977f4779d` |

## Corrected identity and outcome

The fixed member is the purple printed one-piece stepped center axle shown in
the exploded image. It is fixed to both inner plates. The white stainless rods
remain moving forming/locking rods and are not redesigned by this focused
repair.

The fixed purple axle must move farther behind the XT60 and visibly off the
outer-plate center. Each outer plate receives a mirrored arcuate slot around
that fixed axle. The inner pair and axle remain stationary while the left and
right outer plates rotate in opposite directions through visible open-to-lock
motion.

Initial D06 interpretation that the lower white rod should become fixed was
wrong and is rejected before implementation.

## Coordinate and parameter brief

- Units: millimetres.
- `+X`: axial plate-stack direction.
- `YZ`: mechanism plane.
- `C = outer_rotation_center_yz = (-10.60, 17.00)`.
- `A = fixed_stepped_axle_yz = (-29.00, 17.00)`.
- `e = |A-C| = 18.40`.
- `theta = 32 deg * t`, `t in [0,1]`.
- `alpha_left = -theta`; `alpha_right = +theta`.
- axle-guide slot width: `7.90`, derived from `OD7.60 + 0.30` diametral
  running clearance.
- guide centerline: `q_s(theta) = R(-alpha_s(theta)) * (A-C)`.

`C` remains the frozen outer-rotation datum. D06's provisional
`A=(-18.00,17.00)` / `e=7.40` is rejected: it intersects the frozen upright
guide/cams and has negative web. D07's `A=(-29.00,17.00)` / `e=18.40` is a
design choice supported by search/BREP evidence, pending independent candidate
validation; it is not measured physical truth.

## D07 feasibility result

- Same-Z analytic scan with frozen geometry: the sampled feasible interval for
  `>=2.20 mm` web is approximately `A_y=-27.5..-30.5 mm`.
- Selected point: `A=(-29.00,17.00) mm`; sampled analytic minimum web
  `3.849 mm`.
- Exact BREP minimum cutter/feature gap: `3.650 mm`, with zero cutter
  intersections.
- Boundary webs: inner `3.8946 mm`, left outer `7.650 mm`, right outer
  `9.150 mm`.
- Thirty-three-state actual-solid probe: zero axle/outer, keeper/outer,
  axle/rod, and keeper/cap intersections; fixed-axle reconstruction/mirror
  numerical zero.
- Sampled XT60/service minimum clearance: `19.1764973 mm`, zero intersection.
- Keeper radial capture over the guide slot: `1.050 mm`; physical retention is
  still pending.

## Scope freeze

Authorized geometry changes:

- split the old single `pivot_yz` concept into `C` and `A`;
- move the purple axle, both inner hex bores, and both keepers to `A`;
- replace each outer plate's old axle-centered circular bearing bore with its
  side-specific fixed-axle arcuate slot;
- add source-declared review motion and focused/full motion evidence.

Frozen and forbidden changes:

- no white-rod diameter, length, position, guide endpoint, travel law, cap, or
  follower change;
- no change to `GUIDES`, existing white-rod cam-slot centerlines, or their
  `4.20 mm` widths;
- no lock-solid, lock-parameter, XT60 reference, plate spacing/thickness,
  service-window, or pigtail-removal change;
- no new stability bar, yoke, separate pivot part, linkage, or frame;
- no mesh, 3MF, slicer, or physical-acceptance work.

## Physics boundary

A single fixed pin in a curved slot does not define a revolute joint for a
free planar plate. The pin-slot relation supplies one scalar path constraint,
not the full pose. This design therefore does not claim the purple axle slot alone
forces pure rotation.

The smallest no-new-part closure is the existing white-rod/fixed-inner-guide/
outer-cam contact network. Implementation must leave that geometry unchanged
and prove, at sampled travel states, that the unchanged contact network plus
the new fixed-axle slot reconstructs one common outer pose about `C`. Failure
of that closure proof blocks acceptance and returns to design; it must not be
hidden by prescribed Viewer motion.

## Required artifacts and evidence

- Source-first repaired open, mid, and locked full assemblies.
- Focused `p17_r2_fixed_axle_motion.step.py` entry containing only axle,
  keepers, inner plates, outer plates, and optional translucent XT60 reference.
- One self-contained source-declared parameter/animation sidecar with one
  normalized `open_to_lock` control; it may transform only the outer
  occurrences around `C`.
- Static open/mid/locked PNG packet and focused motion GIF.
- Full-assembly sampled or animated review so the focused isolation cannot hide
  interference with unchanged rods, cams, lock solids, or XT60 reference.
- CAD `refs --facts --planes --positioning`, `validate`, actual-solid collision,
  math reconstruction, constraint-closure, scope-regression, and user-
  requirement checks.

Python/build123d and generated static STEP states remain geometry authority.
The sidecar is only a review-time pose control.

## Material DAG

| Task | Owner / role | Done gate | Depends on |
|---|---|---|---|
| `P17-D06` | `/root/p17_fixed_rod_design`, design | Frozen corrected identity, rail/motion contract, underconstraint finding, and scope; provisional `A` later failed | corrected user images and D06 manifest |
| `P17-D07` | `/root/p17_fixed_rod_design`, datum repair design | Replace only infeasible D06 `A` with a feasible actual-solid-checked datum | D06 contract and implementation STOP evidence |
| `P17-I05` | distinct implementation owner | Source/tests/artifacts implement D07 without changing frozen scope and return reproducible candidate fingerprint without self-approval | `P17-D07` |
| `P17-C05` | distinct critic | Challenge physical constraint closure, assembly, rail/keeper capture, usability, and scope against exact candidate | `P17-I05` |
| `P17-V05` | distinct validator | Independently run actual-solid, math, closure, motion, source/export, and snapshot gates | `P17-I05` |
| `P17-R05` | distinct formal reviewer | Join critic/validator receipts and accept or block exact fingerprint | `P17-C05`, `P17-V05` |
| `P17-H05` | continuity owner | Update project state, next-agent, handoff, and delivery only after review outcome | `P17-R05` |

Default concurrency ceiling is three workers. One writer owns source/tests/
artifacts. Initial implementation plus at most two focused repairs; stop if the
unchanged contact network cannot close the intended motion without changing
white-rod paths or adding structure.
