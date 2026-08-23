# KAGE parts and BOM

Status: working MVP inventory, 2026-08-20. This document records only parts and
constraints explicitly selected, shown, or stated for KAGE. It is not a purchase
authorization. Dimensions tagged **provisional** are CAD clearance envelopes,
not verified dimensions of purchased hardware.

## Status legend

- **Selected / locked**: use this architecture for the MVP unless intentionally
  revised and versioned.
- **Owned**: the user has explicitly said or shown that this hardware is on hand.
- **Awaiting arrival**: selected, but the physical part must be measured before
  its mount is frozen.
- **Provisional envelope**: replaceable CAD keep-out only.
- **TBD**: selection, ownership, quantity, or physical measurement is not yet
  confirmed.
- **Later**: deliberately deferred beyond the MVP.

## 1. Selected clock electronics

| Part | Qty | Stated specification | Status | Physical gate before final mount |
|---|---:|---|---|---|
| StepperOnline NEMA 8 stepper motor | 3 | 4 N cm torque class | **Selected / locked; awaiting arrival** | Measure face, body length, shaft diameter/projection, connector and mounting-hole pattern. Do not freeze the station from a listing alone. |
| TMC2209 stepper driver | 4 | Three installed plus one spare | **Selected / locked**; order/on-hand state not stated | Measure the purchased module and connector/header height. |
| Waveshare ESP32-C6 Touch LCD | 1 | Controller, UI, time and homing control | **Selected / locked**; order/on-hand state not stated | Measure the exact board revision, display outline, USB connector and antenna area. |
| DRV5032 digital Hall-effect sensor module | 5 | 1.65-5.5 V, low-power 1.6 uA, 30 kHz class; three installed plus spares | **Selected / locked**; order/on-hand state not stated | Measure the actual module PCB, sensor location and connector/pin direction. Bench-test magnet size, polarity, air gap and repeatability before pocket placement. |

The intended clock topology is three independently driven rings: one motor and
one Hall home reference for hour, minute and second. The center remains free for
the optical system.

## 2. LED optical and thermal subsystem

| Part | Qty | Stated specification | Status / notes |
|---|---:|---|---|
| Cree XHP35.2 HI LED | 1 | Warm white 3000 K; nominal 12 V class; maximum current about 1.05 A; maximum electrical power about 13 W | **Current design target**, not confirmed purchased. Operate around 3-5 W normally; an 8-10 W daytime boost may be tested. Do not design for continuous 13 W operation. |
| Copper MCPCB | 1 | 20 mm round, for the XHP35.2 HI | Required; exact product and hole/pad layout TBD. |
| Thermal interface material | 1 application | Thermal paste or a thin thermal pad | Required between MCPCB and aluminum heatsink; exact product/thickness TBD. |
| Aluminum heatsink | 1 | Small 30-40 mm class | Required; exact diameter, height, fin layout and mounting interface TBD until a real part is selected. |
| PETG optical cartridge/carrier | 1 printed | Retain the heatsink at cooler edges or mounting points | Parametric printed part. It must not sit directly under the MCPCB or become part of the heat path. |
| LED wires | 2 conductors | Small flexible pair from MCPCB to constant-current driver | Required. Gauge, insulation, length and connector TBD. Provide strain relief and a service loop so carriage motion does not flex the solder joints. |
| Optional aperture/optic holder | 0 for first test | Add-on interface only | **Later.** Start with the bare LED. Do not add a diffuser, and do not assume a secondary optic. |

Required thermal path:

`LED -> 20 mm copper MCPCB -> paste/thin pad -> aluminum heatsink -> open air -> PETG carrier`

Optical-mechanical contract:

- LED and heatsink move together as one removable cartridge.
- LED-to-mask distance is adjustable from about 30 mm to 80 mm, requiring about
  50 mm axial travel.
- The emitter remains centered on the optical axis.
- The heatsink stays ventilated and is not enclosed in a sealed printed cavity.
- Driver electronics should remain away from the heatsink.

## 3. Power chain

| Part | Qty | Stated specification | Status / unresolved interface |
|---|---:|---|---|
| Main power supply | 1 | 12 V / 4 A | **Selected / locked**; order/on-hand state not stated. |
| 12 V to 5 V USB-C buck converter | 2 | 5 V / 3 A each | **Selected / locked**; exact modules and assigned loads TBD. |
| USB-C PD source/trigger stage | 1 path | USB-C PD to 15 V | Architecture stated for the LED path; exact trigger/module not selected. |
| Constant-current LED driver | 1 | Accept the selected upstream supply and regulate the XHP35.2 HI | Required; exact driver, efficiency, current-set method and dimming interface TBD. |

Two power descriptions have been stated and must not be silently merged:

1. `12 V / 4 A -> TMC2209 drivers -> three NEMA 8 motors`, with a
   `12 V -> 5 V / 3 A` buck feeding logic/UI as assigned.
2. `USB-C PD -> 15 V -> constant-current LED driver -> LED`.

Whether both branches share one upstream connector or supply remains an
electrical-design decision. Confirm total current, grounding, protection,
thermal load and connector ratings before wiring the complete clock.

## 4. Fasteners and magnets

| Item | Qty | Stated / current use | Status |
|---|---:|---|---|
| M3 socket-head screws, 6/8/10/12 mm lengths | Unknown assortment | The supplied parts-bin photo shows these lengths. Current base CAD uses M3 fasteners, including M3x6 at the MVP base seams and M3x8 at the electronics-backbone seam stack. | **Owned.** Verify actual length, head diameter and engagement at each assembly stage; do not treat one length as universal. |
| Ordinary M3 hex nuts | At least 8 for the current four-seam MVP base; final system count TBD | Captive/replaceable MVP nut strategy | Needed for MVP; ownership not confirmed. Use real metal nuts, not printed threads or printed nuts. |
| M3 heat-set inserts | TBD | Production replacement for suitable repeated-service joints | **Later; not owned.** Do not buy until insert size, boss diameter, installation direction and service need are frozen. |
| NEMA 8 face screws | 12 if four per motor, subject to the purchased motor | Supplied motor drawing indicates M2 face mounting, but screw length depends on the real motor and bracket | **Do not buy yet.** Confirm with delivered motors. |
| Existing neodymium magnets | TBD installed; existing stock | 3 x 2 mm or 4 x 2 mm magnets were stated as available, for Hall homing experiments | **Owned.** Do not freeze diameter, polarity, pocket or installed quantity until the DRV5032 bench test passes. |

## 5. Printed materials

| Material | Intended use | Hard constraint |
|---|---|---|
| PETG | Main structural/internal components, including the LED cartridge carrier | Must be thermally isolated from the MCPCB and heatsink by mechanical edge retention and open air; PETG is not a heatsink. |
| PLA / PLA+ / wood-filled PLA | Optional decorative visible front parts | Must not mount the heatsink, contact hot LED components or close the heatsink ventilation path. Keep a physical air gap. |

## 6. Current replaceable CAD envelopes

These values exist so the layout can reserve space while hardware is unavailable.
They are **not purchase specifications** and must be replaced with measured
envelopes or exact supplier CAD before production mounts are generated.

| Placeholder | Current CAD envelope |
|---|---:|
| NEMA 8 body reference | 20.3 x 20.3 x 39.3 mm; 4.0 mm shaft; 7.0 mm shaft projection |
| ESP32/display board | 50 x 40 x 15 mm |
| TMC2209 module | 22 x 18 x 15 mm |
| USB-C PD trigger | 30 x 20 x 10 mm |
| Logic buck converter | 45 x 25 x 15 mm |
| LED constant-current driver | 45 x 25 x 15 mm |
| LED heatsink witness | 40 mm diameter reference |
| DRV5032 module | 12 x 8 x 4 mm |

The current base context is a 300 mm outside diameter, four-part, 6 mm-thick
plate system. Mounting reservations are functional interfaces, not justification
to lock any unmeasured electronics hole pattern. Its current parametric
interfaces include three motor stations with 2.5 mm radial service adjustment,
three Hall-magnet positions, and an `Ø4.1 x 2.1 mm` Hall-magnet pocket for the
4 x 2 mm candidate. That pocket remains subject to the physical sensor-gap test.

## 7. Do not buy or freeze yet

- Exact NEMA 8 mounting screws, shaft couplers/pinions and final motor pocket
  dimensions, until all three delivered motors are measured.
- A specific USB-C PD trigger, LED constant-current driver, buck board mount,
  or connector, until its real PCB/connector envelope is known.
- A final heatsink or cartridge retention pattern until the 20 mm MCPCB and
  heatsink are selected together and bench-tested thermally.
- Final LED wire gauge, connector and service-loop length until the current,
  carriage travel and driver location are fixed.
- M3 heat-set inserts and their production bosses.
- An optional lens, reflector, diffuser or aperture. A diffuser is specifically
  excluded from the first optical test.
- Final Hall magnet diameter and sensor-to-magnet gap until 3 x 2 and/or
  4 x 2 mm magnets are tested with the actual DRV5032 modules.

## 8. Staged buy and test order

1. Inventory the owned M3 screw lengths and 3 x 2 / 4 x 2 mm magnets; obtain
   ordinary M3 nuts needed for the MVP base.
2. Receive and measure the three NEMA 8 motors. Print and assemble one motor
   station before committing to screws, pinions or three-station production.
3. Bench-test one motor, one TMC2209 and one DRV5032 homing channel with both
   candidate magnet sizes. Record the repeatable trigger gap and polarity.
4. Validate the three-ring mechanism at low speed and low load before adding
   the optical subsystem.
5. Bench the LED, MCPCB, thermal interface, heatsink and constant-current driver
   outside printed parts: begin near 3 W, validate temperature, then 5 W; test
   8-10 W only as a limited boost condition.
6. Build the removable 30-80 mm optical cartridge around the measured LED and
   heatsink, then validate focus/halo/shadow and PETG temperatures.
7. Only after those physical gates pass, freeze exact board mounts, wiring,
   production heat-set inserts and decorative PLA/wood-PLA parts.
