# P17-V08 independent validation

## Receipt

- Role: `P17-V08`, independent validator for exact candidate `P17-I08-R2`.
- Verdict: **PASS** for the frozen CAD source, prescribed motion, ten written STEP exports, source/export parity, and frozen visual-orientation packet.
- Frozen gate manifest: `/tmp/p17-i08-independent-gate-manifest.txt`, 30 entries, SHA-256 and candidate fingerprint `f5bc383f6566adf0262a32630792621fd7e5436e780b1b2553b144eb49887ad5`.
- Every manifest entry passed `shasum -a 256 -c` before validation and after all long-running gates.
- Candidate record hashes: artifact provenance `97dccfad274fd82724f06c8e1ec15cd4ccc25659b6aa652dca7b8b9ecefb6b4b`; candidate manifest `0eaa98ffdc26baea5f409867929ffb9df317030bfa902cf20cd2b770919deb25`; fingerprint JSON `2b84cf88b9079edd8766a03d3fa9fe9fb251b6b1afeed7647124061f157a2fe5`; fingerprint text `74a8c72100949170e05f3eba71d63d3a92049892a995b044ef9d4ae952b7d255`.
- No candidate source, test, CAD artifact, Viewer state, git state, or non-validation documentation was modified by this role.

## Commands and results

All Python commands ran from the repository root through the shared root uv environment.

- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py` -> **19/19 passed**.
- Independent numerical harness `/tmp/p17_v08_math_gate.py` recomputed the exact geometry from D10-R2 equations and centered finite differences against the public residual API.
- Independent actual-solid harness `/tmp/p17_v08_solids_gate.py` evaluated the continuous support strips, full probes, motion collisions/contact, and rederived service path. Its initial nested-label substring census was discarded as a validator false positive; the authoritative direct production-solid dictionary independently returned the exact 16 production obstacles and required counts.
- Written STEP inspection copied each manifest-verified `.step` byte stream to an isolated `/tmp/p17-v08-step.*` directory under a distinct `export_*.step` name, preventing the inspector from resolving a same-stem `.step.py`. All ten copies passed `inspect refs --facts --planes --positioning` and `inspect validate` with zero command failures.
- Independent `/tmp/p17_v08_step_parity.py` directly loaded every generator and every corresponding written STEP through `build123d.import_step`. Repeated identical solids were matched within rounded prototype-invariant groups before comparing placements.

## D10-R2 math and motion

- Common stroke `S = 10.5852813742 mm`; contact angle `23.433175199799216 deg`; END `24 deg`; outer datum `C=(3,12)`; fixed axle `A=(-29,17)`.
- OPEN centers: upper-left `(-4.2502813742,24.435)`, upper-right `(22.235,24.435)`, lower-right `(22.235,-2.0502813742)`. The right OPEN leg is exactly vertical: upper-right and lower-right have identical `Y=22.235`.
- Contact centers: `(6.085,24.435)`, `(14.926852454797476,17.126852454797476)`, `(22.235,8.285)`.
- END centers: `(6.335,24.435)`, `(14.7500757595,16.9500757595)`, `(22.235,8.535)`.
- Independently recomputed triangle areas were OPEN `350.7350647352727 mm2`, contact `12.384667144979247 mm2`, END `7.394704576049996 mm2`; side lengths matched D10-R2 within rounding.
- Corresponding accepted-END displacement was `0.657609306503489 mm` upper-left, `0.657823586728245 mm` middle, and `0.6576093065034884 mm` lower-right; maximum is below the frozen `0.657824 mm` ceiling.
- Maximum rod-rail reconstruction residual `5.687116766346677e-15 mm`; maximum axle-rail residual `7.105427357601002e-15 mm`.
- Minimum analytic rail derivative `0.12146470802366102 mm/deg`; fixed-track progress `0.44105339059166654 mm/deg`; minimum non-adjacent branch gap `0.04637851244492177 mm`; maximum continuation residual `9.981443266930663e-15 mm`; no branch jump.
- Crossing sine was retained only as a diagnostic: minimum `0.0007187165`; no threshold was incorrectly reinstated.
- Independent centered finite differences produced maximum residual norm `8.131102728189963e-15`, minimum normalized rank 3, minimum singular-value ratio `0.07799318575832481`, and maximum normalized condition `12.821632944943044`, below `1000`.

## Actual solids, support, contact, caps, and service

- Continuous outer support checked `48,312` actual-solid strip points from the swept boundary through `+0.30 mm`, both normals, every rod/side, 65 base states plus exact contact: zero discontinuities.
- Minimum full `+0.30 mm` outer probe material ratio was `0.9999999999999983`; fixed-inner probes also retained positive full material.
- Minimum web was `3.630989824536459 mm` against the `2.20 mm` gate. Left/right outer rod-cutter gaps were `3.630989824536459 / 5.884373740993324 mm`; fixed extended gap `6.103048327204938 mm`. All four plates were valid positive-volume single solids.
- Actual-solid motion included 65 states plus exact contact: maximum unintended intersection `0`; minimum XT60 clearance `0.7500000000000036 mm`; pre-contact wire intersection `0`; exact contact tangent; all three END wire intersections positive as the named geometric displacement proxy.
- Exact production inventory: three `OD4 x 50 mm` rods, six permanent caps, two fixed inner plates, two rotating outer plates, two keepers, one fixed axle; no added bar/yoke/link/gear/grip/lock mechanism.
- Axial closure: principal stack `32.00 mm`, cap gap `0.30 mm` each side, derived engagement `8.70 mm` each side, cap length `9.05 mm`, closed wall `0.35 mm`; cap-to-plate/keeper and nominal rod-to-cap-material unintended intersections were zero.
- Independently rederived service path `P0(0,0,0) -> P1(-4,10,-15) -> P2(-4,50,-15)` used piecewise-linear interpolation at 1001 samples per segment, 2002 total poses, against all 16 final production obstacles. Minimum BREP clearance was `1.2499999999999902 mm`, analytic minimum `0.9338159212309596 mm`, and maximum intersection `0`.

## STEP and visual evidence

- All ten manifest-frozen written STEP exports passed refs/facts/planes/positioning and geometry validation: center-axle coupon, contact, exploded, fixed-axle motion, full motion, END (`locked` compatibility filename), mid, OPEN/service, permanent-cap coupon, and print kit.
- Source/import parity passed ten of ten. Maximum bounds delta `8.810729923425242e-12 mm`; maximum summed-volume delta `1.3387762010097504e-8 mm3`; maximum grouped per-solid signature delta `1.0001206507403992e-7`, below `1e-6`. Written solid counts matched source for every export, including 832 solids in the OPEN/service artifact.
- Visually inspected frozen OPEN, contact, END front, and END opposite PNGs. OPEN clearly shows the true `└` workpiece, XT60 head/up, tail/right, and upper-left plus exact upper-right/lower-right vertical rod pair. Contact and END retain the mapped three-point upper-left-to-lower-right diagonal. Opposite view shows the four-plate assembly, fixed eccentric purple axle/keepers, three rods/six caps, larger right force plate, and no floating or added mechanism.
- The 72-frame `900x650`, 60 ms/frame looping GIF was inspected at frames 0, 17, 35, 53, and 71. Each successive sample had a non-empty image difference; rods follow their rails while the outer plates counter-rotate and the inner plates/axle remain fixed. Deterministic sidecar/source regressions support identities and rotation signs that may be partially occluded in a single camera view.
- Frozen visual hashes: OPEN `7235f31d08cc6b27b812afcc41ecec0cf4eb3c1ee5be47d6903d8b96143c745f`; contact `d61811c3156b6c425d14a1e578b92aff15c9c81834e67ce8a238b88ea8a51cec`; END front `a086c0812f648373f4ba075b8a88732fa93b299840e8ffb74221ce0a2ee948e4`; END opposite `047ef210ffb599b443e3658ae7345e7a8f82ed3042d20f0247002ee105fe87d9`; GIF `461aeb86ae7aa1212e8cccee129e70f4f2fcb0f8cfd3ccf7e24a9d35bc4dd11c`.

## Requirement coverage and boundary

- `REQ-027`: PASS — workpiece-relative world `YZ`, `+Z` mating-head/up, `+Y` tail/right, visible and numerically fixed.
- `REQ-028`: PASS — OPEN UL/UR/LR topology, exact right vertical leg, continuous rod identity, stationary straight inner guides.
- `REQ-029`: PASS — END UL/middle/LR diagonal three-point wrap; contact and wire/XT60 allow-list checks pass.
- `REQ-030`: PASS — endpoint is geometric CLAMPED/END only; no retention, hard-stop, detent, over-center, or self-lock geometry/claim was introduced.
- CAD/source and written STEP: **PASS for exact fingerprint only**.
- Physical acceptance: **not tested**. Permanent-cap fit/retention, rod wobble, hand torque, holding force, insulation marking/damage, soldering heat, PETG stiffness/creep/wear, springback, cooled bend angle, endpoint holding, and self-lock remain physical gates.
- Next action: formal reviewer `P17-R08` may join this receipt with the independent critique for the unchanged fingerprint. Any change to a frozen manifest entry invalidates this validation.
