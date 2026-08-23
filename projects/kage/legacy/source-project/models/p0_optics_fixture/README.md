# P0 four-part optics fixture

This is a print experiment, not a clock mechanism. It contains exactly four printable parts:

1. `p0_pedestal_mask`: one solid tapered pedestal/mask with a fixed Ø8/Ø6/Ø4 stepped arbor.
2. `p0_hour_hand`: 60 mm tapered blocker with rounded tip and compliant slit hub.
3. `p0_minute_hand`: 70 mm tapered blocker with rounded tip and compliant slit hub.
4. `p0_second_hand`: 85 mm tapered blocker with rounded tip and compliant slit hub.

The body is intentionally modeled as a closed solid. Set **8% gyroid infill** in Orca rather than hollowing the CAD. The hand hubs use a Ø+0.20 mm relief bore, three 1.20 mm contact pads with 0.15 mm protrusion, and a 1.00 mm radial slit opposite the blade. The resulting local radial interference is 0.05 mm; physical fit remains the first print gate.

Primary CAD:

- `p0_assembly.step`
- `p0_pedestal_mask.step`
- `p0_hour_hand.step`
- `p0_minute_hand.step`
- `p0_second_hand.step`

Print files:

- `print/p0_four_part_test_bundle.3mf`
- `print/p0_pedestal_mask.stl`
- `print/p0_hour_hand.stl`
- `print/p0_minute_hand.stl`
- `print/p0_second_hand.stl`
- `print/p0_print_manifest.json`

The manifest status remains `pending_independent_review`. Follow `docs/p0-optics-fixture-test-plan.md` before treating the fixture as physically accepted.
