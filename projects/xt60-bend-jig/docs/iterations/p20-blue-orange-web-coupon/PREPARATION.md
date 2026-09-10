# P20 Blue-Orange web coupon U1 preparation

Date: `2026-08-27`

Task: `P20-WEB-PREP-01`

Status: **PREPARED; EXACT G-CODE PASSES STATIC AND THREE-LAYER WITNESS
REVIEW; NOT UPLOADED OR STARTED**

This preparation is only for the test coupon. It does not approve the full
P20 profile, mechanism, plate stack, rod caps, or any product web below the
ordinary `2.20 mm` rule.

## Frozen input and output

- Candidate fingerprint:
  `07f4a32d455214ae1d5b71dfdeba8dc55ca5a9a970580011cf35e5cf859a93be`.
- Formal `REVIEW.md` SHA-256:
  `f0459a5ba44f9dfe88361a97f2674a04eeba117e6f470a8d4445b0971c816760`.
- Exact input STL SHA-256:
  `6181d4ae4c9e5a396c1cc425826464cb00074fbb618be9d67630ee12d92529b0`.
- Exact prepared G-code:
  `cad/p20_blue_orange_web_coupon/prepared/r1/p20_blue_orange_web_coupon_u1_petg_t3_r1.gcode`.
- G-code SHA-256:
  `f159d4bec8793cf22e2739c5a736d86f0a0d3cc1eacc6cb69303201191e7e475`.
- Prepared manifest:
  `cad/p20_blue_orange_web_coupon/prepared/r1/prepared-manifest.json`.
- Prepared-manifest SHA-256:
  `753c44c927f2700575be42244e1cf5c5d301801bbace0e55ac57050563be8ce3`.

Changing or reslicing the G-code creates a new revision and requires a new
static and layer-level review.

## Slicer and resolved settings

The real `/Applications/Snapmaker Orca.app` CLI was used. Its G-code header
reports Snapmaker Orca `2.3.5`; the CLI banner is
`Snapmaker_Orca-01.10.01.50`, and the executable SHA-256 is
`4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe`.
The child process returned exit `0`, and a fresh artifact was created in an
isolated output directory.

| Setting | Resolved value |
|---|---|
| printer | Snapmaker U1, `0.4 mm` nozzle |
| process | `0.20 Standard @Snapmaker U1 (0.4 nozzle)` |
| material | Snapmaker PETG |
| physical / logical tool | physical `3` / G-code `T2` |
| layer height | `0.20 mm`; first layer `0.25 mm` |
| wall loops | `2` |
| sparse infill | `15%`, grid |
| supports | disabled; no support toolpath type exists |
| nozzle | `250 C` first layer; `245 C` later |
| textured bed | `70 C` first and later |
| line widths | outer `0.42`, inner `0.45`, first layer `0.50 mm` |
| first-layer compensation | `0.15 mm` elephant-foot compensation |

All four resolved filament-slot profiles retain `filament_diameter=1.75` and
`filament_is_support=0`. The crash-associated explicit
`wipe_tower_filament: "0"` key was removed from the process input. The
successful slicer nevertheless serializes its internal default as
`; wipe_tower_filament = 0` in the G-code metadata. This is recorded as a
provisional backend distinction: the hazardous explicit input was absent,
the tool inventory remained four slots, the child returned `0`, and the
artifact uses only `T2`.

The current bundled Snapmaker PETG leaf contains a zero-valued textured-bed
temperature and a `230 C` later nozzle temperature. Preparation explicitly
used the already successful project PETG workflow instead: `250/245 C` nozzle
and `70 C` bed. The emitted `M140`, `M190`, `M104`, and `M109` commands were
checked, not inferred from profile labels.

## Static G-code validation

- Movement and positive extrusion are present.
- Exactly one model identity appears:
  `p20_blue_orange_web_coupon.stl`.
- Header and footer agree on `16` layers; max Z is `3.25 mm`.
- Object extrusion bounds are approximately
  `X=[121.197,149.803]`, `Y=[122.163,149.837] mm`, well inside the U1
  printable bounds `X=[0.5,270.5]`, `Y=[1,271] mm`.
- Active tool commands are only `T2`. Per-tool filament usage is
  `0.00, 0.00, 599.70, 0.00 mm`, or `1.80 g` total.
- Estimated normal-mode print time is `6m 12s`.
- Supports are disabled and no `Support` or `Support interface` toolpath type
  exists. Both slots remain modeled as open voids.
- The exact G-code retains two wall loops, `15%` infill, the listed line
  widths, `M140 S70`, `M190 S70`, first-material `250 C`, and later `245 C`.

## Mandatory first / middle / top witness review

Snapmaker Orca arranged the model about build
`XY=(135.500,136.000) mm`. The formal sampled witness at source build
`XY=(-0.938941,+7.963860) mm` therefore appears at
`XY=(138.449809,141.702909) mm` in this exact G-code.

The external, non-geometric locator is saved as both SVG and PNG:

- `cad/p20_blue_orange_web_coupon/prepared/r1/toolpath-witness-first-middle-top.svg`
- `cad/p20_blue_orange_web_coupon/prepared/r1/toolpath-witness-first-middle-top.png`

The exact extrusion paths were parsed with their emitted feature widths and
reviewed at:

| Layer | Z / height | Witness material | Blue slot center | Orange slot center |
|---|---|---|---|---|
| first, `1/16` | `0.25 / 0.25 mm` | continuous and covered | open | open |
| middle, `8/16` | `1.65 / 0.20 mm` | continuous and covered | open | open |
| top, `16/16` | `3.25 / 0.20 mm` | continuous and covered | open | open |

The adjacent openings remain separate in every inspected layer; there is no
fused slot, omitted witness island, support path, or unresolved slicer warning
at the witness. The direct bead-width coverage test reports `0.30576 mm`
uncovered on the first-layer CAD-edge-to-CAD-edge probe, split only into its
two endpoint pieces (`0.14738 mm` at one slot boundary and `0.15838 mm` at the
other). This is the expected effect of the recorded `0.15 mm` first-layer
elephant-foot compensation enlarging the two void boundaries. There is no
uncovered interior segment: the central ligament and formal witness remain one
continuously covered span. That therefore preserves the ligament gate while
also proving that the neighboring slots were not accidentally filled. The
middle/top probe has only one endpoint remainder under `0.009 mm`, attributable
to emitted-coordinate rounding against the exact CAD boundary, again with no
interior break. Any uncovered segment inside the two endpoints would have
failed the G-code. These edge effects are visible in all three retained panels
and are not hidden as a perfect CAD-boundary equality claim.

## Exact command shape and result

```text
Snapmaker_Orca --debug 3
  --load-settings '<resolved-machine.json>;<resolved-process.json>'
  --load-filaments '<slot-1.json>;<slot-2.json>;<slot-3.json>;<slot-4.json>'
  --load-filament-ids '3'
  --arrange 1 --orient 0 --slice 0
  --outputdir '<fresh isolated directory>'
  p20_blue_orange_web_coupon.stl

child exit: 0
fresh output: plate_1.gcode
```

The exact resolved profile bytes are retained beside the G-code and bound by
`prepared-manifest.json`.

## Hard pre-start conditions

No upload or printer start occurred. A separate operator must obtain fresh
authorization for the exact G-code and U1 target, then confirm:

1. physical tool `3` currently contains the intended PETG;
2. the U1 build plate is clear, correctly installed, and clean; and
3. the user authorizes this exact SHA-256
   `f159d4be...e7e475` on the U1.

Suggested authorization wording:

> Start `p20_blue_orange_web_coupon_u1_petg_t3_r1.gcode` (SHA-256
> `f159d4bec8793cf22e2739c5a736d86f0a0d3cc1eacc6cb69303201191e7e475`)
> on the Snapmaker U1 using PETG physically loaded in tool 3; the plate is
> clear and clean.

## Later rod-cap / plate-gap requirement

The user additionally requires rod caps to remain short so the XT60 does not
stick in the axial gap, and wants the usable gap between the two plates kept
as wide as possible within the `50 mm` rod envelope. This coupon has no rod,
cap, XT60, or plate stack, so the requirement is neither tested nor changed
here. It remains a mandatory next product-CAD envelope check and must not be
inferred from a coupon PASS.
