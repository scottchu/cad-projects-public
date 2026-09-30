# Printing profile — Grenadier magnet

## Profile

Diagnostic U1 profile; no approved print release.

## Intended settings

User selected 0.2 mm nozzles. Real filament, final scale, and remaining production settings are unresolved; historical native-profile settings are preserved below.

## Part orientation and fits

Development work scale 125 by 101.8 mm, backing down and face up. Magnet interface, strength, adhesion, and actual detail fit remain unverified.

## Verified slice and print runs

P3 and P4 contain real diagnostic toolpaths and independent comparisons. No physical print outcome is established.

## Concerns

Missing thumbnails and unresolved thin detail, structural connectivity, glass mixing, and physical testing block print release.

## Historical record

GM-NOZZLE-01 / 2026-09-06: user confirmed “0.2 it is” after the 0.4 mm comparison. Selected nozzle diameter is **0.2 mm**. This choice does not select final size, filament brand or all other process settings, and does not authorize coupon generation or printer/upload/start actions; existing diagnostic and physical acceptance boundaries remain.

`gm-print-01 diagnostic-r3`, 2026-09-06. **DIAGNOSTIC / NON-PRINT-RELEASE.** Both flat and relief were actually sliced; real materials, final scale and physical detail are still unresolved.

Current geometry is unchanged at 125 ×101.8 mm work scale, flat2.0 mm/relief2.4 mm, back down and face +Z; six/fourteen named parts. Native Snapmaker Orca 2.3.5 uses U1 four0.2 mm nozzles, 0.08 High Quality (first layer0.10 mm), four walls, 15% gyroid, supports disabled, prime tower enabled. Temporary Generic PLA on all slots, diameter1.75 mm, Textured PEI. T0 black, T1 gray, T2 white, T3 deep blue. Glass-mix remains named but provisionally maps to white, including pale antialias plate subregions; this does not implement Full Spectrum mixing. Actual Gcode commands bed65°C and printing nozzle220°C, alongside native preheat/cleaning/standby temperatures. These are observed file commands, not printer measurements or selected loaded materials.

| Native diagnostic run | Artifact and child result | Independent output evidence | Slicer estimate |
|---|---|---|---|
| Flat | `slicer/p1-r3-recovery/flat-run1/plate_1.gcode`; child243 after Gcode completion during absolute container-path export | 25 layers, Z0.10–2.02 mm; all four tools extrude; 30 actual changes | 6h52m1s,18.37g (T0/T1/T2/T3:12.67/2.82/2.58/0.30g) |
| Relief | `slicer/p1-r3-recovery/relief-run1/plate_1.gcode`; child0; `relief-sliced.3mf` embeds identical Gcode | 30 layers, Z0.10–2.42 mm; all four tools extrude;45 actual changes | 7h12m22s,19.62g (13.91/2.91/2.36/0.44g) |

Both object extrusion centerline bounds: X72.71–197.19, Y84.61–185.99 mm; these are neither source silhouette nor deposited bead-envelope bounds. Exact input/output hashes and commands are in `slicer/p1-r3-recovery/output-manifest.json` and active SETTINGS_DIAGNOSIS/HANDOFF. Requested settings and actual output evidence remain separate. No physical duration/consumption measurement exists.

Historical flat attempts in `slicer/p1-r3/flat-02-run{1,2}` crashedSIGSEGV(-11/shell139) before slicing. P3-D moved the identical wipe_tower_filament setting from independently normalized process to machine, preserving the merged configuration and all four filament bytes. This resolved the earlier block without changing geometry. Those failures remain retained; current authority is recovery output fingerprint `3b686c6e33c7bd98562803a6478f78c4ce1c7e8f277c174ff4901931cd9ec39d`.

P3-V passed exact packaging parity and limited actual-path feature presence: DJZY608/GRENADIER and four main lamp motifs remain visible. Fine central gray trim is fragmented and letter/plate strokes contain small gaps; some emitted widths are below nozzle diameter. No exact pixel-loss metric or physical reproduction claim. Historical R3 scope: the 0.4 mm comparison had not yet been performed; completed R4 comparison evidence follows below.

Prepared/print acceptance remains blocked: native OpenGL thumbnail failures, no emitted PNG/JPG thumbnail in relief archive, missing flat container, unresolved clean fine detail, first-layer bead connectivity/strength/adhesion, glass mixing, real material and magnet interface. Source/GLB development preview remains separately accepted; no STEP/BREP or physical approval. The next smallest experiment is a scoped detail coupon after intent/material/printer authorization, not automatic final-width selection. No printer contact/upload/start occurred.

## Diagnostic R4 — native 0.4 mm comparison

User authorized “Try” after confirmingR3 used0.2mm. P4-S sliced both unchanged125×101.8mm multipartpackages with installedU1 four0.4mm/0.08HighQuality/compatibleGenericPLA, samefourtool/provisionalwhiteglass/TexturedPEI mapping. Both nativechildexit0; exactcommands/settings/hashes `docs/iterations/p1-r4-nozzle04/SETTINGS_RESULTS.md`, outputmanifest `slicer/p1-r4/output-manifest.json` fingerprint `bb4177d216e744e665ced60ead6646a8f38f90f14310129a4137441322efb1bc`.

Flat:23layers,3h45m53s,23.15g. Relief:29layers,4h12m17s,22.43g. Gcode/containers `slicer/p1-r4/{flat,relief}-run1`; archives embed matchingGcode; both lackthumbnails. Native0.4firstlayer0.20mm versus0.2profile0.10mm, walls2versus4, linewidths0.42–0.45versus0.22mm, othernativeprocess/filamentdifferences recorded in`profile-differences.json`. This is complete nativeprofilecomparison, not nozzlediameteralone. No geometry/scale changes or physicalprint.

P4-V actualpaths:0.4DJZY608 stillreadable and4mainlamps retained; GRENADIER white strokes are incomplete: large letter-shaped areas have no depicted extrusion at the selected surface layer; finerlampringscoarsen. Independentcomparisonreport and media inP4iteration/P4validationnamespace. TemporaryPNGdiagonalhatching was rasterizationerror, excluded fromtoolpathfindings; authoritativeSVGs unchanged. Prepared/physical acceptance remainsblocked. Compareactualpaths at `https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-nozzles`; no printercontact/startauthorized.
