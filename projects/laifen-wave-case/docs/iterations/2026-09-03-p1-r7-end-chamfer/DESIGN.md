# R7 selected end-chamfer contract

## Selected parameter and geometry

Add `end_chamfer_size: float = 1.20` to R7 `Params`; allow `0.80 <= end_chamfer_size <= 1.50` mm and reject values outside that interval. It is a source-level parameter that regenerates real BREP and STEP. Do not add a viewer-only slider or imply live regeneration from a sidecar.

Let `Rcrest = outer_diameter / 2 = 19.50` mm and let `t` increase inward from the closed end: +Z from the body's bottom end and -Z from the cap's top end. The intended 45-degree conical boundary is

`r_chamfer(t) = Rcrest - end_chamfer_size + t`, for `0 <= t <= end_chamfer_size`.

At default, the closed-end perimeter is the true circle `r = 18.30` mm and the chamfer has a 1.20 mm radial recession and 1.20 mm axial height. The slope magnitude is exactly 1 (45 degrees), satisfying the existing unsupported-overhang direction limit. The conical trim may meet the unmodified diamond field where that field lies inward of the cone; its guaranteed continuous smooth circular band is `0 <= t <= end_chamfer_size - skin_height`. At default that band is 0.75 mm; at the authorized minimum it remains 0.35 mm. This is the deliberately narrow smooth-end exception, not a smooth seam collar.

The maximum size leaves `19.50 - 1.50 - 15.50 = 2.50` mm radial material from the cap bore to the closed-end outer perimeter. Floor thickness, center-plus-six R9 drain pattern, hole diameter, and axial drain cutters remain unchanged. The chamfer cutter must be end-local and may not reach the cylindrical sidewall above its local range, the thread, taper, shoulder/stop, seam, bore, inner floor, or drain geometry.

## BREP route and source boundary

Copy R6 source modules into `cad/p1_r7_end_chamfer/`; do not copy or modify mesh geometry. Remove the old bed-relief fields, derived relief slope, `skin.relief()`, relief surface zones, and all related checks from the new R7 route so no second bevel remains. Retain the procedural diamond surface and its full unscaled field above the new end treatment.

For each standalone part, form one end-local exterior annular cutter around the closed end: an overshooting outer cylinder minus a coaxial 45-degree cone whose boundary is the equation above. Subtract that one cutter from the textured outer blank before the existing bore/thread and floor-drain operations. The cone may overshoot its two axial limits by a small documented kernel-safe epsilon while preserving the nominal boundary equation at `t=0` and `t=end_chamfer_size`. Apply it in the part-local inward direction so the cap remains correct before its existing print-layout rotation. Retain native runout normalization after cap operations. Update labels and README/generation instructions to identify R7 and the actual Python/`uv run python cad/p1_r7_end_chamfer/generate.py` regeneration path.

## Focused affected gates

1. **Parameter/math and requirement gate:** default, 0.80, and 1.50 are accepted; adjacent out-of-range values fail. Derive radius, axial height, 45-degree slope, guaranteed circular-band width, and cap closed-end radial material. Confirm no old relief parameters/functions remain and the retained 39/30/31/C213/219, N33/pitch4.8/phase, floors, seven drains, seam/stop/thread/runout/datums/poses equations are unchanged.
2. **Real-BREP sensitivity gate:** build standalone body and cap at default and at `end_chamfer_size=1.40`, without rebuilding four primary wrappers for each value. In the guaranteed band, probe multiple azimuths at two inward `t` positions to show an actual circular exterior boundary at `r_chamfer(t)`, then recover the actual radial-to-axial slope and size from those rings. Prove that increasing 1.20 to 1.40 changes the measured end radius by 0.20 mm while leaving a sampled non-end diamond station unchanged. Verify valid positive one-solid parts, unchanged bore/inner-floor/hole positions, and no cutter reach into joint/seam/thread/stop intervals.
3. **Default candidate/export gate:** generate only the four R7 default primary STEP targets. Validate source/written STEP parity by the established adaptive-volume method (gate <=0.001 mm3), occurrence count/transforms, floor holes and closed-end circles, and selected preserved dimensions. Render and inspect both closed drain ends and a close-up that shows the smooth circular chamfers and seam separately. Slicer and physical acceptance remain pending.

Reopen only the affected end-surface, floor/first-layer, source-to-STEP parity, label/README and visual-review gates. Reopen thread/motion/device-envelope gates only if an implementation measurement shows the end-local cutter entered their declared protected regions.
