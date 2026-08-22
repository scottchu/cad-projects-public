# P0 three-rod XT60 bend jig — bill of materials

This BOM follows the current source and print-kit assembly. Fastener lengths other than the specified M4 × 40 are deliberately not guessed; select them against the printed stack-up and record the choice in the physical-test log.

## Printed parts

| Qty | Part | Notes |
| ---: | --- | --- |
| 1 | Left ribbed side frame with diagonal drive support | Contains the M4 drive tunnel/positive-stop support |
| 1 | Right ribbed side frame | Mirrored rod tracks and forming slot |
| 1 | Left compact moving slider | Diameter-10 collar; contains the 7.2-AF M4 nut trap and left axial forming-rod retainer boss spanning `X = -32..-25` |
| 1 | Right compact moving slider | Diameter-10 collar; follows the spanning forming rod and includes the symmetric retainer boss spanning `X = 25..32`; no second dial |
| 4 | Compact reaction-rod carrier | Each is 2 thick with a diameter-9 rod boss, diameter-7 lock boss, 5-wide web, diameter-4.3 rod bore, and diameter-3.4 M3 clearance; no carrier insert |
| 1 | XT60 upper collar/cradle | Three height holes per side on 4 mm pitch; one matched left/right pair is occupied at a time |
| 1 | M4 drive knob | Printed interface for the experimental one-sided drive |
| 1 | Rod-bore/slot fit coupon | 4.2, 4.3, 4.4, and 4.5 mm trials; print before the full kit |

The source also defines a rod end-cap helper, but end caps are intentionally excluded from the current print kit and are not required by this BOM.

## Purchased hardware

| Qty | Item | Current requirement |
| ---: | --- | --- |
| 3 | 304 stainless-steel round rod, 4 mm diameter × 50 mm | One upper reaction rod, one lower reaction rod, one moving/forming rod |
| 1 | M4 × 40 screw | Experimental left-side diagonal drive |
| 1 | M4 hex nut | Fits the modeled 7.2 mm across-flats trap; verify the actual nut before assembly |
| 1 | M4 thrust washer/interface | Keep the screw/knob from chewing into PETG; exact washer/head arrangement is a physical-selection item |
| 4 | M3 reaction-carrier lock screws | One passes through each carrier; reuse the same four screws when moving to another indexed setting |
| 12 | Reaction-lock heat-set inserts | Install six per side frame at the three upper and three lower datums; seats are diameter 4.6 × 3.5 with diameter-3.4 continuations |
| 2 | M3 XT60-collar mounting screws | One left and one right, installed through one selected matched height pair; three positions per side does **not** mean six installed screws |
| 2 | Matching M3 collar nuts and washers | No collar nut trap is modeled, so select hardware that clamps squarely without interfering with the connector or frame |
| 2 | M3 forming-rod axial-retainer screws | One at each rod end; each passes through a 3.4 continuation and bears axially on the rod end |
| 2 | Matching heat-set inserts | One in each 4.6 diameter × 5.2 insert seat; the surrounding 8.6 boss provides 2.0 radial wall |

The three M3 systems are distinct: four reusable reaction-carrier lock screws with twelve permanent **frame** inserts; two XT60-collar mounts with two nuts/washers at one selected height pair; and two axial forming-rod retainers with two slider heat-set inserts. The compact carriers have no inserts. Do not combine these quantities or substitute one system's hardware without rechecking the modeled stack-up.

## Workpiece and test consumables

- Actual target bottom ESC and stack, measured at no more than 36 mm wide for the current clear-span assumption.
- Actual wire-side XT60 pigtail connector. The source reference is labeled `reference_xt60_body_15p9x8p1x20p5_with_5mm_solder_cups`: a 15.9 × 8.1 × 20.5 body plus 5-long solder cups, totaling 25.5 axially. The downloaded AMASS STEP remains only a PCB-vertical envelope source.
- Representative 12 AWG and 14 AWG insulated wire, solder, and flux.
- A 44 mm available-lead specimen for normal settings and a specimen at least 50.425 mm long for the full reaction-setting matrix.

## Print and assembly order

1. Print the fit coupon first in PETG using the exact full-kit orientation and slicer process.
2. Measure all three rods and choose the smallest common coupon size that slides without binding or meaningful lateral rock.
3. Update the source fit parameter if needed, regenerate STEP/3MF, then print the full kit in PETG.
4. Dry-assemble all hardware and complete the cold fit/access gates before energizing a soldering iron.
5. Treat PETG as a first-prototype material only. The physical thermal rehearsal—not the CAD model—decides whether its clearance and stiffness are adequate.
