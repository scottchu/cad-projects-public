# O15 formal review — P17 compact plate 2D gate

Decision: **ACCEPT for user-facing 2D review only**.

This approval is limited to the deterministic FRONT `OPEN` / `END` proposal.
It does not authorize or accept 3D CAD, STEP/3MF, slicing, printing, physical
fit, force, locking, or solder-service performance.

## Reviewed candidate fingerprint

- optimizer source SHA-256:
  `1d36c3809b2b0e42dfad905f5706caae15ec8c6e1110fcb5ee7b2886bc08025f`
- focused tests SHA-256:
  `da9331715e5404049f0051c6d708068833f48b839f7692d3f8f5fd372a93d303`
- SVG SHA-256:
  `23f93ca5500d94078edafa02742dbe49cd5542fcd446359e0be63beb073b0412`
- PNG SHA-256:
  `4fd438bf0031128b471ebbf071bcd1a4eb4ac07d8c55e557bc0e64304d35813d`

## Review basis

- Exact P17 requirements and numeric contract in `TASK_INPUT.md` and
  `DESIGN.md` were used; no P13 or older P17 guide table was substituted.
- Local rerun: `uv run pytest -q
  projects/xt60-bend-jig/tests/test_p17_compact_plate_optimizer.py` — `10`
  tests passed.
- Local rerun: `xmllint --noout` on the reviewed SVG — passed.
- Independent numeric validation recomputed diameters
  `52.933 / 53.933 / 54.933 mm`, minimum internal web
  `2.597732481369 mm`, and true limiting boundary web
  `2.200398673579 mm`.
- Independent validation confirmed fixed FRONT orientation, frozen P17 rod
  identities and OPEN/END topology, aligned XT60/wire route, fixed axle `A`
  left/behind XT60, and inverse-derived opposite `-45/+45 deg` outer rails.
- Independent visual critique passed the 2D gate.
- Formal snapshot inspection confirms the diagram visibly separates OPEN and
  END, labels all three rods, `A`, `C`, wire direction, plate diameters,
  opposite rotation, and the limiting web, while explicitly disclaiming 3D,
  print, and physical acceptance.

## Advisory for later implementation

`fixed_inner_hex_bore_af = 8.15 mm` is currently represented in the optimizer
clearance calculation by an `AF/2` circular proxy. It is not the controlling
boundary or minimum-web feature for this exact candidate, so it does not block
this 2D gate. Before reusing the optimizer for arbitrary axle placements or
claiming 3D clearance, replace that proxy with the actual hexagonal cutter
envelope (including its corner radius) and rerun collision/web checks.
