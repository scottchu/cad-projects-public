# P4-S native0.4 mm diagnostic preparation receipt

Owner `/root/slice_settings_diagnosis`;2026-09-06. **Both variants generated native Gcode and sliced3MF on the initial attempt, childexit0. Diagnostic/non-print-release only.** No source/GLB/package/artwork/scale changes, printer contact, installedapp changes or dependency modifications. `CURRENT` intentionally points to this new iteration; other continuity indexes remain root-owned.

Frozen task input `slicer/p1-r4/input-manifest.json`, fingerprint `eceb2a4b1c102833a84d71cf8fa01977e9ecd5f4cd5f0366e508b6cb471ebe8b`, includes exact frozenbrief, accepted candidate source/artifacts, original multipart3MFs, resolvedprofiles, nativeancestry, launcher and executable. All parent18 entries and both known3MF hashes verified before preparation; full manifest verified before each child. Native executable SHA256 `4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe`, bundle2.3.5/CLI01.10.01.50 unchanged.

Exact executed commands from repository root, rootuv Python3.12:

```sh
uv run projects/grenadier-fridge-magnet/scripts/slice_nozzle04_run.py prepare
uv run projects/grenadier-fridge-magnet/scripts/slice_nozzle04_run.py flat
uv run projects/grenadier-fridge-magnet/scripts/slice_nozzle04_run.py relief
```

Exact nativeargv/childexits/timing/hashes: `slicer/p1-r4/{flat,relief}-run1/{command,receipt}.json`. Both commands use isolateddatadir, originalmultipart3MF, resolvedmachine/process plus4filaments, arrange0/orient0/slice0, basename `--export-3mf`, and isolatedoutputdir. Native wipe_tower_filament1 placed in machine (which includes nozzle_diameter), omitted from independently normalizedprocess; nativepresetIDs explicitly matchnames. This carries the proven P3 recovery without repeating its crash.

| Variant | Native result | Gcode SHA256 / bytes | Archive SHA256 / bytes | Native estimate |
|---|---|---|---|---|
| Flat | exit0;11.196s | `354ccfc88f75ce3ae4040dc92e991f8083cb77d95c17e54d0188298ae87555b0` /26,832,296 | `feefeb095763afdb98af0662d19fdce93531299f91f251156657d19ec6ba6fc4` /6,866,341 | 3h45m53s;23.15g;23layers;maxZ1.96 |
| Relief | exit0;14.226s | `7c3ba1a39336c0dfd53c05fc0d428658f4ef49d9a1536d713ed438db63b0a326` /30,233,290 | `27b2890169d7d2d99ea8a51fdf1920cd6e87c1878a780b7f19a54dae8d324b50` /7,568,467 | 4h12m17s;22.43g;29layers;maxZ2.44 |

Gcodes are `{variant}-run1/plate_1.gcode`; containers `{variant}-run1/{variant}-sliced.3mf`. Output manifest fingerprint `bb4177d216e744e665ced60ead6646a8f38f90f14310129a4137441322efb1bc` freezes settings, inputmanifest, commands/receipts, outputs and preliminaryfacts. Both archives embed byte-identical Gcode; neither containsPNG/JPG thumbnails. Thumbnail absence remains a prepared-acceptance blocker despiteexit0.

## What this comparison changes

Installed native `Snapmaker U1 (0.4 nozzle)` and `0.08 High Quality @Snapmaker U1 (0.4 nozzle)` exist. Nominal0.08mm layerheight matchesP3, but firstlayer0.20 vs0.10mm, wallloops2 vs4, nominalsurfacewidth0.42 vs0.22mm, infillwidth0.45 vs0.22mm, shellcounts and speeds differ. Nativecompatible `Generic PLA` also differs from the prior0.2-specific filament profile. Full10machine/29process/62filament field differences are preserved in `profile-differences.json`. These are native nozzle-profile comparisons, not an isolated nozzle-diameter experiment; do not attribute all speed/material changes to nozzle alone.

Four provisional slots remain T0black/T1gray/T2white/T3deepblue; glass and pale-blue plate-antialias geometry provisionallywhite, no Full Spectrum claim. TexturedPEI, PLA, supportdisabled, primetowerenabled, original125×101.8mm workscale/backdown placement unchanged. Preliminary actual Gcode inventory findsT0–T3,27/45 toolchanges, bed65°C and printingnozzle220°C, with nativeclean/preheat/standby temperatures. Native estimates/masses are not physicalmeasurements.

Warnings retained in `settings-output-facts.json`: shadercompilation/thumbnailrenderer failures, exclude-triangle diagnostic, multimaterial SupportSpotsGenerator limitation. No workaround hides them; support remainsdisabled. Independent validator `/root/slice_artifact_validator` received frozen outputs for actual geometry/path comparison, feature survival, bounds and media; preparation owner does not approve own result. GM-R4-01/02 preparation and immutable-input scope completed; GM-R4-03 actual spatialtool fidelity and GM-R4-04 fine-detail/bounds checks await distinctvalidator. GM-R4-05 diagnostic-only/printer boundary maintained. No STEP/BREP or physical acceptance. Next: inspect actual0.4 versus0.2 plate/wordmark/central lamps; preserve finalscale choice for later.
