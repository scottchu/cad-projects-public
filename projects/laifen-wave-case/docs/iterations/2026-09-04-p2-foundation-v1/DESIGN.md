# P2 Foundation V1 design

## Coordinate and topology contract

Use a right-handed model frame with `+Z` from the bottom exterior face to the top exterior face. The assembled container occupies `0 <= z <= H`. The split plane is at `z = H - U`, where `U` is the upper-piece length measured from the top. The lower visible length is `H - U`. Both pieces use the same sidewall outside diameter `OD` and remain coaxial. Exploded presentation changes only their axial separation.

Exterior end shaping stays within the end/floor envelope; the internal cavity end planes remain at `z = F` and `z = H - F`. Threads occupy the annular wall near the seam and do not silently shorten the axial cavity.

## Small V1 parameter set

Defaults are neutral teaching values, not measured Laifen dimensions.

| ID | Control | Default | V1 bounds/choices | Meaning |
| --- | --- | ---: | --- | --- |
| `H` | Total outside height | 120 mm | 40–300 mm | Bottom exterior to top exterior. |
| `OD` | Outside diameter | 60 mm | 20–160 mm | Round diameter or polygon across-corners diameter. |
| `W` | Wall thickness | 2.4 mm | 0.8–8 mm | Normal sidewall offset; inside clearance is derived. |
| `F` | Floor thickness | 3 mm | 0.8–12 mm | Common closed-end thickness at top and bottom. |
| `splitMode` | Split input | percent from top | percent / distance from top | Selects which one split value is editable. |
| `splitValue` | Selected split value | 50% | 25–75% or the equivalent mm | Defines upper length without two competing inputs. |
| `section` | Cross-section | round | round / regular polygon | Simple outline choice. |
| `N` | Polygon sides | 6 | integer 3–32; polygon only | Hidden and ignored for round. |
| `bottomStyle` | Bottom end | chamfer | flat / chamfer / rounded | Independent exterior end profile. |
| `bottomSize` | Bottom end size | 1.2 mm | conditional | Chamfer size or round radius; zero/ignored for flat. |
| `topStyle` | Top end | chamfer | flat / chamfer / rounded | Independent exterior end profile. |
| `topSize` | Top end size | 1.2 mm | conditional | Chamfer size or round radius; zero/ignored for flat. |
| `P` | Screw pitch | 2 mm | 0.8–6 mm | Axial distance per full turn. |
| `T` | Screw turns | 2 | integer 1, 2, or 3 | Engagement turns; axial engagement is derived. |
| `C` | Radial clearance | 0.25 mm | 0.1–0.6 mm | Per-side conceptual gap; diametral gap is derived. |
| `D` | Thread profile depth | 0.45 mm | 0.2–1.5 mm | Radial profile depth inside the shared OD wall. |
| `threadForm` | Thread profile form | symmetric trapezoid | symmetric trapezoid / rounded | Changes the displayed radial section, not a manufacturing claim. |
| `drainLocation` | Drain end | bottom | none / top / bottom | V1 permits one drained end only. |
| `Q` | Drain count | 7 | integer 1–16; active drain only | Count one is centered. |
| `d` | Drain diameter | 3 mm | 0.8–10 mm; active drain only | Diameter of each conceptual through-hole. |
| `BCD` | Drain bolt-circle diameter | 20 mm | dynamic; active drain only | Hole-center circle; forced to zero when count is one. |
| `presentation` | View state | assembled | assembled / exploded | A view control, never a model dimension. |

The round/polygon choice stays in V1 because it adds only one conditional side-count control. `OD` always means maximum outside size. There is no corner-roundness or section-rotation control.

## Derived descriptor values

The future pure function `deriveV1(inputs)` must return either `{valid:false, errors, descriptor:null}` or a finite serializable descriptor. It computes:

- Outside radius: `R = OD / 2`.
- Round minimum clear ID: `ID = OD - 2W`.
- Polygon outside across flats: `AF = OD * cos(pi / N)`; polygon minimum clear ID: `ID = AF - 2W`.
- Usable axial cavity height: `usableHeight = H - 2F`.
- If percent mode is selected: `U = H * splitValue / 100`; if distance mode is selected: `U = splitValue`.
- Split percentage from top: `splitPercent = 100U / H`; split plane/lower visible length: `splitZ = lowerLength = H - U`; upper visible length: `upperLength = U`.
- Screw engagement: `E = P * T`; diametral clearance: `2C`; minimum thread-zone residual wall: `W - D`.
- Drain ring radius: `Rb = BCD / 2`.
- For `Q = 1`, the one drain center is `(0,0)` and `BCD = 0`. For `Q > 1`, center `i` is `(Rb*cos(2pi*i/Q), Rb*sin(2pi*i/Q))`.
- End descriptors contain the chosen profile and its actual size; flat ends normalize size to zero.

The descriptor names lower/upper pieces, the common OD datum, cavity envelope, split plane, thread section/engagement, end profiles, selected drain mask, and assembled/exploded transforms. A later renderer must not rederive these relationships from form state.

## Validity constraints

All numbers must be finite and within the table bounds. In addition:

1. `ID >= 4 mm` and `usableHeight > 0`.
2. The seam remains in the body: `25% <= 100U/H <= 75%`.
3. With fixed conceptual keepout `K = 2 mm`, both `U` and `H-U` must be at least `F + E + K`.
4. Thread residual wall must satisfy `W - D >= 0.8 mm`, and `C < D`.
5. A flat end uses size zero. A chamfer/rounded end requires `0.2 mm <= size <= min(F, OD/8)` and must fit within its piece length.
6. Drain controls are ignored when location is `none`. A selected drain must cut only its chosen top or bottom floor.
7. For drains, fixed conceptual edge/hole web `g = 1.2 mm`: `Rb + d/2 + g <= ID/2`. When `Q > 1`, adjacent-hole web must satisfy `2Rb*sin(pi/Q) - d >= g`. When `Q = 1`, `BCD = 0`.
8. No invalid state yields partial or stale geometry.

These are preview-consistency constraints, not FDM, strength, fit, drainage-performance, or physical validation.

## Ordered feature backlog

Each item requires its own small user gate and evidence before the next begins.

1. **V2 surface patterns, one at a time:** smooth baseline regression, blunt diamond, recessed diamond, knit stitch, straight micro-flutes, flowing flutes, rugged hex, shallow helix, wave flutes, then quilted diamond. Each addition introduces only its necessary depth/pitch/family controls and must remain independently distinguishable.
2. **V3 fade and relief:** full/bottom/top/center coverage, fade by depth or density, inset/outset/balanced placement, minimum wall, and seam/end keepout.
3. **V4 labels:** none/inset/outset; safe text; preview font; weight; size; relief; orientation; lower/upper/both target; angle; axial position; optional patch and margin. Future OpenSCAD font remains separate metadata.
4. **V5 attachments:** none, lanyard eyelet, captured loop, separate clip/link, keyring tab, and bridge handle; fixed/separate presentation, lower/upper half, angle, opening/member/clearance/hole/span/standoff dimensions.
5. **V6 alternative closure:** bayonet as a separate family with lock angle, lug count, capture, ramp rise, clearance, and closed pattern phase.
6. **V7 OpenSCAD parity/export:** flattened names, preset parity, deterministic generation, source/export comparison, and separate export validation. This phase starts only after preview relationships pass.
7. **V8 MakerWorld packaging:** documentation, presets, screenshots, metadata, and package validation. Publication requires separate authorization and does not imply physical acceptance.

## Gate decision

The user passed this contract on 2026-09-04 with the exact response `Yes pass`. These parameters, equations, constraints, exclusions, and the ordered backlog are frozen inputs to `../2026-09-04-p2-foundation-v1-implementation/`. No CAD, OpenSCAD, export, service, MakerWorld, or deferred-feature work is authorized by this PASS.
