# P17-V13 independent validation

Date: 2026-08-25  
Validator: `/root/p17_lock_validator` (independent of P17-I13)  
Candidate fingerprint: `590e05f90e865f499af83c59350039ce20afc9ccd33bcad1975024aa3fba4b8c`

## Disposition

**Implementation fidelity: PASS. Product acceptance: BLOCKED.** The candidate exactly materializes the user-locked D13 coordinates and frozen I10 interfaces, but it is deliberately not an acceptable mechanism/print candidate: the OPEN bottom rod intersects both the XT60 body and wire, and END no longer reaches the required wire contact. Nothing in this receipt allowlists those failures or proves service, force, self-locking, printed fit, or physical acceptance.

## Immutable-input gate

- `shasum -a 256 p17-d13-independent-gate-manifest.sha256` returned the exact fingerprint above.
- `shasum -a 256 -c p17-d13-independent-gate-manifest.sha256` passed **21/21** entries before validation and again after validation.
- Frozen authoritative inputs: design `0133dc4d...`, source `cef1137d...`, tests `68879bd5...`; all ten STEP exports, two motion sidecars, four PNGs, and one GIF retained their manifest hashes.

## Deterministic results

- `uv run --project projects/xt60-bend-jig pytest -q projects/xt60-bend-jig/tests/test_p17_r2_direct_counter_twist.py`: **14 passed**, exit 0.
- Independent hard-coded D13 reconstruction confirmed common rod delta `(+16.1869657526,+10.2949747468) mm`, fixed axle `A=(-29,12)`, outer center `C=(3,12)`, frozen workpiece center `(-6.5,22.5)`, and frozen plate diameters `80/82/85 mm`. Maximum source-table error was `2.5243e-12 mm`; maximum 65-state inverse reconstruction error was `7.1054e-15 mm`.
- D13 OPEN/contact/END centers (Y,Z mm): bottom `(-4.7983156216,19.7949747468) / (5.5369657526,19.7949747468) / (5.7869657526,19.7949747468)`; diagonal `(21.6869657526,19.7949747468) / (14.3788182074,12.4868272016) / (14.2020415121,12.3100505063)`; upright `(21.6869657526,-6.6903066274) / (21.6869657526,3.6449747468) / (21.6869657526,3.8949747468)`.
- Independent continuous rail lengths, left/right (mm): bottom `7.502250790 / 13.948565724`, diagonal `9.319981713 / 14.960660650`, upright `19.287996598 / 6.279967138`. Full-path long/short ratios are `1.859250792`, `1.605224249`, and `3.071353110`; therefore the rails are materially unbalanced. The minimum published crossing sine is only `0.000748503001` (near-tangent), so crossing quality is not accepted.
- Independent centered finite-difference public-residual/Jacobian gate covered 132 states (65 plus exact contact per side): maximum residual norm `3.6473e-15 mm`, public-vs-centered-FD maximum Jacobian error `1.6003e-5`, minimum rank `3`, minimum normalized sigma ratio `0.126207161`, maximum condition `7.923480696`.
- Actual-solid regression gates passed for six inverse-derived rails, closed fixed slots, continuous `+0.30 mm` outer support strips, endpoint probes, retained webs, cap closure, and valid plate solids. These are geometry/support results only.
- Written-artifact inspection used isolated STEP copies with `scripts.inspect validate` plus direct `refs --facts`: **10/10 STEP files passed**, zero validation failures, and each resolver selected the written `.step`. Independent build123d source/export comparison passed **10/10** solid counts, bounds, and summed volumes; maximum bounds delta `6.2528e-12 mm`, maximum volume delta `1.2107e-8 mm^3`.
- Fixed occurrence frames were identical in OPEN/mid/contact/END (`1` unique frame table); outer angles were `0/0`, `-12/+12`, `-23.433175/+23.433175`, and `-24/+24` degrees. Both motion sidecars passed `node --check` and expose one `open_to_end` control.
- Visual packet was inspected in RGB: four static views show the frozen inner plates/axle/workpiece and opposite outer rotation. The GIF has 72 frames at 960x720; all `71/71` consecutive RGB frame differences were non-empty and the final frame differed from OPEN by `41,763` RGB pixels. This proves visible motion, not mechanical acceptability.

## Product blockers and physical boundary

- OPEN bottom-to-body signed clearance is `-2.000000 mm`; actual BREP intersection exceeds `100 mm^3`.
- OPEN bottom-to-wire centerline separation is `1.7016843784 mm`, giving `2.4483156216 mm` radial overlap; actual BREP intersection exceeds `1 mm^3`.
- END wire surface gaps are `8.1369657526 mm` (bottom) and `7.8778831578 mm` (upright); `lostEndContact=True`.
- The `50.00 mm` rods and cap stack close axially in CAD, but cap retention, PETG fit, wire response/preload, force path, self-locking, service extraction, and assembled physical behavior remain unproven.

## Next action

Do not print or release this D13 materialization. Reopen design with explicit user authorization to correct the rod layout against the frozen XT60/wire interface, then require a new immutable fingerprint and independent validation. Preserve this receipt as evidence that implementation fidelity does not equal product validity.
