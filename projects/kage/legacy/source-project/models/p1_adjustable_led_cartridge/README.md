# P1 adjustable LED cartridge

This isolated build123d model provides a 50 mm axial LED-source adjustment for
the Japandi shadow clock. The wall is `z=0`, +Z points into the room, the
conceptual mask plane is `z=6`, and the source planes are exactly `z=36`, `40`,
and `86` mm (mask distances 30, 34, and 80 mm).

Installation architecture: the V0R2 quartz body and orbital hand/fin carriers
remain standalone moving parts nearest the wall. P1 is a stationary structural
bridge mounted to cool KAGE-side datums around them; it is never supported by
the quartz arbor. The LED carriage moves only along the stationary P1 rails.
`p1_integration_reference.step` labels the wall, V0R2 moving stack, stationary
bridge, LED/thermal stack, open wall-facing optical axis, room-side viewer, and
glare-shield mounting datum. The opaque dome/glare shield itself is not modeled.

Printable parts are `rail_frame`, `moving_carriage`,
`rear_service_bridge`, and the optional `strain_relief_clip`. Purchased or
conceptual items remain separately labeled nonprintable references: the 20 x
1.6 mm MCPCB, 3.45 mm square XHP35.2 emitter, 40 x 40 x 30 mm pin heatsink,
M4 clamp hardware, two-lead wire envelope, conceptual mask plane, thermal/free
air envelopes, driver clearance envelope, and the V0R2 keepout.

The PETG carriage retains the heatsink with four finite 3 x 6 x 4 mm cool-edge
clips tangent to its x=+/-20 mm metal faces. The clips interrupt 288 mm3 of the
otherwise open 5 mm air envelope; all other carriage structure is behind the
LED plane or outside that envelope. There is no PETG under the central 20 mm
MCPCB disk or central 24 x 24 mm hot base footprint. The two 4 x 5 mm rails are
at x=+/-29 mm with 0.30 mm clearance per side
inside 12 mm bearing lands. The removable rear bridge is the max-travel stop
and anti-withdraw feature. Slide the bridge in -Y, then withdraw the carriage,
metal stack, and engaged strain-relief clip through the open +Z rail end.

The `z=6` mask is conceptual. The 500-1000 mm halo/shadow result is unproven
until the actual mask and LED are tested together on the bench. The optional
future aperture-holder reference is only a removable ring with three M2 datum
holes; it contains no diffuser or secondary optic.

Generate primary STEP files with the CAD skill `scripts/gen ... --write` against
the explicit `.step.py` entries. Run `uv run python
p1_adjustable_led_cartridge_export.py` for four individual STL files and the
multi-object 3MF print bundle. Printing and electrical/thermal safety remain a
physical validation step; follow the thermal plan in `docs/` before installing
decorative PLA nearby.
