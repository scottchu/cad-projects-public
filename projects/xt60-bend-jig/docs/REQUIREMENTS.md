# XT60 bend jig requirements and design contract

## Outcome and use sequence

Load two insulated XT60 pigtail wires, close one rotary input to form and hold a fixed 90-degree path, solder while keeping the plastic body unloaded, allow cooling, reopen the jig, and remove the completed pigtail without damage.

## Invariants

- `REQ-001`: Clamp and form only the two insulated wires; do not use the XT60 plastic body as the clamped load.
- `REQ-002`: The supported P13 outcome is a fixed 90-degree wire path.
- `REQ-003`: Use three purchased, uncut 304 stainless rods, each `OD4.00 x 50.00 mm`.
- `REQ-004`: P13 has four principal circular plates: two fixed guides and two synchronized cams.
- `REQ-005`: One rotary input gives all three rods equal scalar travel along their distinct straight guide directions.
- `REQ-006`: The mechanism must support loading, dry motion, soldering, cooling, service, and completed-pigtail removal.
- `REQ-007`: Geometry, placement, motion, STEP, and 3MF outputs remain source-derived and parametric.
- `REQ-008`: The production kit contains four principal plates, one D shaft, one keeper, three permanent left caps, and three removable right caps; purchased rods and proof-only geometry are excluded.

## Derived constraints

- `CON-001`: `0 deg` is open, nominal first geometric wire contact is near `22 deg`, and `27 deg` is locked.
- `CON-002`: Nominal insulated wire OD is `4.30 mm`; rod radius is `2.00 mm`; wire radius is `2.15 mm`.
- `CON-003`: `wire_preload = 0.25 mm`, `contact_stroke = 3.7642135623730946 mm`, and `common_stroke = 4.014213562373095 mm` for the imported baseline.
- `CON-004`: The accepted source domain limits `wire_preload` to `0.00..0.40 mm` without renewed design review.
- `CON-005`: Principal plate and cap print orientations are authored in source; slicer-side flipping, negative Z, or `Lay on face` is not an accepted repair.
- `CON-006`: `4.15 mm` is the current evidence-backed sliding rod-hole reference and applies only after checking the bore's functional role.
- `CON-007`: The next center-hole repair must map the user's physical observation to one exact printed stick/shaft and mating hole, then change only the responsible source-controlled clearance with regression evidence.

## Design choices

- `CHOICE-001`: P13 uses no base or enclosing frame.
- `CHOICE-002`: The three rod roles are asymmetric: forming, supporting, and locking.
- `CHOICE-003`: PETG and a `0.4 mm` nozzle are the current physical prototype assumptions.

## Non-goals

- `NON-GOAL-001`: Adjustable bend angle.
- `NON-GOAL-002`: Decorative handle, replacement base, electronics, motor, or frame holder.
- `NON-GOAL-003`: Treating the XT60 envelope, wires, soldering tool, or purchased rods as printed production objects.
- `NON-GOAL-004`: Redesigning the architecture as part of the monorepo migration.
- `NON-GOAL-005`: Applying one larger diameter indiscriminately to all center, shaft, or rod bores.

## Physical unknowns

- `PHYS-001`: Exact identity and required clearance of the printed center-hole interface that rejected the user's middle stick.
- `PHYS-002`: Complete printed fit, binding, actuation effort, and repeated cycling after the center-hole repair.
- `PHYS-003`: Permanent and removable cap retention, service effort, and wear.
- `PHYS-004`: Wire holding force, insulation marking or damage, and XT60 body loading.
- `PHYS-005`: Soldering access and PETG stiffness, creep, cracking, or heat softening.
- `PHYS-006`: Completed-pigtail removal, cooled angle, and springback.

## Evidence mapping

| IDs | Evidence | Status |
|---|---|---|
| `REQ-001`–`REQ-008` | P13 brief, source, focused tests, STEP/3MF census | historical; migration rerun pending |
| `CON-001`–`CON-005` | P13 source, amendment, motion tests, artifact provenance | historical; migration rerun pending |
| `CON-006` | PETG rod-hole coupon observation | observed |
| `CON-007`, `PHYS-001` | Latest printed P13 fit observation; exact interface diagnosis pending | observed defect; unresolved |
| `PHYS-002`–`PHYS-006` | Repaired complete P13 PETG assembly and use trial | pending |
