# Pattern families design — PF-DES-01

This contract extends BRIEF.md against its verified 26-file baseline. Source
names below are the intended canonical job fields; UI raw groups remain separate.

## Controls and canonical state

| Pattern | First control (mm) | Depth (mm) | Defaults |
| --- | --- | --- | --- |
| Smooth | None | None | Browser/Reset choice |
| Diamond | Diamond size, 4.8..8.0, step 0.1 | 0.10..0.60, step 0.05 | 4.8 / 0.45 |
| Ribs | Spacing, 4.0..16.0, step 0.1 | 0.10..0.60, step 0.05 | 6.0 / 0.45 |
| Rings | Spacing, 4.0..16.0, step 0.1 | 0.10..0.60, step 0.05 | 6.0 / 0.45 |
| Spiral | Spacing, 4.0..16.0, step 0.1 | 0.10..0.60, step 0.05 | 6.0 / 0.45 |

These are nominal limits, intersected with the exact selected-family predicate.
Exact entries may be off slider steps; preserve finite in-range values and raw
invalid text. Do not clamp or change another value automatically. Show current
limits beside each input; coupled errors appear once in the shared form error.
Diamond size means diamond height; derive `diamond_arc_pitch=size*(3.63/4.8)`
with an exact default branch returning 3.63 at size4.8. Phase0/plateau0.18 stay fixed.
Ribs help: “Distance between ridges around the case; rounded to fit evenly.”
Rings help: “Distance between rings.” Spiral help: “Distance between spiral
ridges, measured vertically.” Six parallel spiral starts are fixed, so one
ridge rises `6*spacing` per revolution; this is not a full-turn pitch control.
Depth help: “How deep the pattern sits below the outside surface.”
Use `wave_spacing`/`wave_depth` for the selected new family in canonical jobs;
all inactive source fields receive their fixed defaults, never stale raw text.
Store independent raw Diamond/Ribs/Rings/Spiral settings in controller state.
Hash the full normalized allowlist snapshot; exclude only inactive raw memories.
Switching invalidates jobs even if values match. Add fields to defaults/allowlist,
schema, adapter and source-contract tests; preserve pinned worker protocol.

### PF-DES-02 UI clarification

- Exact input is authoritative. Render an off-grid value at its exact proportional thumb position (`step=any`); render/switch/focus never rounds or mutates raw state.
- Slider steps describe explicit interactions: arrows move to the next feasible nominal-grid value strictly above/below the exact value; Home/End choose the feasible grid endpoints. Grids are anchored at each nominal minimum. Pointer input selects the nearest feasible grid value, ties upward; only that user event commits the number. Test size4.83→Right4.9/Left4.8 and depth0.43→Right0.45/Left0.40, plus switch-away/back preservation.
- For every slider, compute its allowed set by replacing only its own raw input with each candidate while retaining all other current raw inputs. Never substitute family defaults or last-valid values to advertise a range. A finite numeric invalid field's own slider can repair it when its other required inputs are valid.
- If its own raw text is blank/non-numeric, disable that slider and hide its thumb; show “Enter a number to use the slider.” Keep its exact input enabled. It has no keyboard/pointer origin and cannot commit a fallback; numeric exact entry restores the ordinary rules. This takes precedence over the own-field repair rule.
- Invalid size/spacing disables the coupled Depth slider; invalid Depth disables Size/Spacing. Both invalid disables both sliders. Dimension sliders also require valid selected-family raw inputs. Keep every exact input enabled for repair; keep independent coherent dimension state, and preserve all invalid text across switching.
- A disabled slider with unresolved inputs shows its nominal “Design range” and “Enter a valid [field] to calculate allowed values”; it does not label a fallback as allowed. A complete numeric draft with no one-field repair says “No allowed values; adjust [coupled field].” A recoverable interval is labelled “Allowed” and uses the exact predicate. Inactive invalid memories have no validity/bounds effect.
- Use five native labelled radio cards with distinct cues: plain, diamonds, vertical lines, horizontal lines, diagonal spiral lines. Desktop may use five columns; at390px use a compact wrapping grid (three then two), never horizontal scrolling or a single-column list. Every target is at least44×44px with visible focus ring; no clipped cues/text. The selected group follows the complete selector, not an individual card.
- At1280×900 and390×844 verify all five labels/cues, target size, wrapping, no page overflow and group placement; scroll may reveal controls beneath the pinned phone canvas. Verify actual off-grid rendering/interaction, invalid-field repair, inactive memory exclusion and normalized full-snapshot identity.

## Geometry and finite guards

Let R=OD/2, d=selected depth, s=spacing, g=globalZ−body_thread_z, angles in degrees.
New field: `r=R-d*(1-cos(phi))/2`; no outward displacement.
Ribs: `N=floor(2*pi*(R-d)/s+0.5)`, `phi=N*theta`, integer N>=3.
Rings: `phi=360*g/s`. Spiral: `phi=6*theta-360*g/s`.
Body uses globalZ=localZ; cap uses globalZ=body_thread_z+localZ. No axial scaling.
Reuse `v06_profile`, its 96 inner samples, zipper, floors, threads and cutters.
Add a new exterior mesh path; leave original Smooth/Diamond geometry functions
unchanged. Do not route new bodies through the generic 1mm crest-radius collar.
Retain the original cap bore's 0.01mm Boolean overshoot and output transforms.

Diamond: rV=R−d; N=round-half-up(2*pi*rV/arc); actualArc=2*pi*rV/N.
Require N in[8,128], plateau width `0.36*actualArc*size/sqrt(actualArc^2+size^2)>=1`,
slope `d/(size*0.32)<=1`, source finite/shell guards, and exact original estimate
`16*N*(ceil(h/(size/8))+1)<=250000` independently for body_thread_z and cap_height.
No epsilon correction: retain the original literal136.8 floating-ceil boundary.
UI Diamond wall W>=3.95+d; source also checks both bore residuals>=minimum_wall,
female thread residual>=1.8 and entry relief residual>=1.8 using actual internals.

New families: require finite s/d and the nominal ranges above. Angular samples
`n=max(192,32*N)` for Ribs, n=192 for Rings/Spiral. Ribs axial base segments M=1;
others `M=ceil(h/(s/16))`. Include both endpoints and the closed-end chamfer break
as an extra row when needed. Share exact angular endpoints across the seam.
Apply the existing end cone as a piecewise-linear clipping surface: split any
triangle crossing field-minus-cone zero and reuse owned edge intersections.
Simply taking min at unsplit vertices is prohibited: it bridges the clipping cusp.
Each crossed triangle produces at most three triangles. With e=end_chamfer,
use conservative estimate `E=2*n*(M+2)+4*n*min(M+1,ceil(e*M/h)+2)+2*n<=250000`
for each role; same operation order in JS/SCAD. Check actual exterior count too.
The extra rows/clip estimate bounds allocation, not a promise about compile time.

Away from clipping, phase excursion per cell is <=3*pi/16 for Spiral, pi/8
for Rings and pi/16 for Ribs; angle excursion is <=2*pi/192. The interpolation
budget `R*a^2/8+d*a*p/4+d*p^2/16` is <=0.0213mm at R40/d0.6. Owned clipping of
the affine field against the affine cone preserves its field interpolation bound;
audit the clipped geometry separately rather than applying a smooth Hessian
claim across the cusp. Require observed analytic exterior error<=0.025mm.
Any side triangle's inward chord loss is <=R*(1-cos(pi/n))<0.00536mm. Reserve
0.01mm for chord/quantization in ligament guards: UI W>=3.95+d+0.01 for new
families, and source subtracts0.01 from each corresponding valley residual.
This protects the thread zone; closed-end cone material is verified separately.

## Small pilot and focused evidence

PF-PILOT: implement only the new Spiral exterior dispatch first. Compile actual
body, cap and assembled at UI D30/H60/W4.6/T3/manual lid25.3, Spiral s4/d0.6,
Bottom N7, with pinned WASM and source argv retained. Non-round split exercises
global phase; minimum spacing/max depth exercises sampling and chamfer cuts.
Require closed positive oriented body/cap, no invalid edges/degenerates, preserved
bores/floors/thread profiles, no smooth collar, exact shared seam ring, no positive
body/cap collision, correct seven drains and <=0.025mm exterior error including
chamfers. Run existing whole-solid certifier and inspect seam/end snapshots.
Also compile default Smooth and default Diamond and require original STL parity.
Stop on topology/phase/parity failure; initial attempt plus two focused repairs.

After pilot: independent boundary oracle covers both depth endpoints, size/spacing
endpoints, wall equality and adjacent failure, count-round transitions, exact
triangle ceil transitions, and valid slider endpoints for each selected family.
Do not claim exhaustive arbitrary-parameter mesh proof from finite witnesses.
Compile default new families, edited Diamond, one triangle-limit witness and all
four output roles across the set; inspect original returned STL only, with hashes.
Use source-native union/contact for assembled output; print layout needs two
closed transformed parts,7mm X gap, openings up and zero collision. Verify current
Blob/download byte identity and protected drains/threads on representative meshes.
Node controller tests cover independent memory, inactive invalid groups, explicit
Generate, cancellation/late results, Reset and identity. Desktop1280x900/mobile390x844
checks require selected group placement, feasible sliders, focus/errors and actions.
Run root `node --test` focused suites, root `uv run pytest` source contracts, and
`npm run build:openscad-simulator --workspace laifen-wave-case -- --outDir <scratch>`.
The implementation receipt must supply exact pilot/certifier commands before
independent validation. No new dependencies or live8453 build replacement in pilot.
This gate yields source/browser/written-STL evidence; STEP/slicer/physical acceptance
remain separate. Formal review joins distinct critic and validator receipts.
