# P3-D settings diagnosis and native slice recovery

Owner `/root/slice_settings_diagnosis`, bounded settings implementation/diagnosis; distinct downstream validator `/root/slice_artifact_validator`. Status: **both unchanged variants produced native G-code; diagnostic only, not prepared or print release**. Two evidence-led child attempts total. No geometry, artwork, source meshes, GUI settings, dependencies, backend, or printer state changed.

## Concrete trigger and correction

Both preceding native SIGSEGV child exits `-11` occurred after loading the six mesh parts and at process profile loading. No corresponding macOS crash report was available. Primary-source inspection identifies an unsafe per-profile normalization: [Snapmaker_Orca.cpp at commit dcf8629](https://github.com/Snapmaker/OrcaSlicer/blob/dcf8629e661d6e0e78f0d66e43b7fbdf1f8cf7f5/src/Snapmaker_Orca.cpp#L1691-L1757) loads each configuration independently and calls `config.normalize_fdm()`. [PrintConfig.cpp lines 7746–7751](https://github.com/Snapmaker/OrcaSlicer/blob/dcf8629e661d6e0e78f0d66e43b7fbdf1f8cf7f5/src/libslic3r/PrintConfig.cpp#L7746-L7751) dereferences `nozzle_diameter` whenever `wipe_tower_filament` exists, without creating/checking that option. The resolved process has `wipe_tower_filament="1"` but lacks `nozzle_diameter`; its zero-to-one change therefore cannot resolve this null option. This is source-supported trigger inference, corroborated by the successful minimal correction, not a debugger backtrace or proof that this Git source exactly matches the installed binary.

Correction: move the exact `wipe_tower_filament="1"` setting from process JSON into machine JSON, which contains four `0.2` nozzle values. A deterministic dictionary comparison verified `{**old_machine, **old_process} == {**new_machine, **new_process}`. All four filament JSON files remained byte-identical. Thus resolved merged settings and physical tool intent are preserved. Original input 3MFs and current GLBs remain immutable.

Flat's first recovered run sliced and completely wrote G-code, then exited `243` during 3MF export because the old command supplied an absolute `--export-3mf` filename alongside `--outputdir`. [CLI line 5334](https://github.com/Snapmaker/OrcaSlicer/blob/dcf8629e661d6e0e78f0d66e43b7fbdf1f8cf7f5/src/Snapmaker_Orca.cpp#L5334) prepends the output directory unconditionally. The error log exposes the doubled absolute path. Relief's second run uses the basename `relief-sliced.3mf` and exits `0`. Flat was not repeated solely to obtain a container.

## Frozen inputs, exact runs, and outputs

Run commands from repository root, root uv Python 3.12 environment:

```sh
uv run projects/grenadier-fridge-magnet/scripts/slice_recovery_run.py flat
uv run projects/grenadier-fridge-magnet/scripts/slice_recovery_relief.py
```

Exact native argv, executable hash, child exits, elapsed times and artifact hashes are in `slicer/p1-r3-recovery/{flat,relief}-run1/{command,receipt}.json`. Installed Snapmaker Orca bundle 2.3.5; CLI banner `01.10.01.50`; executable SHA-256 `4c30e59cf582dcc4f12e43741fcab2f97045e972065d465481ed3760678d0fbe`.

- Flat input fingerprint `91cdf14470bf6cf14382c1eca724dc7be1f87c0231337922f74d23885bd2b9fb` in `slicer/p1-r3-recovery/input-manifest.json`.
- Relief input fingerprint `1ffedbf975408c220d3d469fc7db953964ea0ce17d52659f9993d002f8cb2b9d` in `slicer/p1-r3-recovery/relief-input-manifest.json`, extending the same inputs with the filename correction launcher.
- Parent P3-S fingerprint `d03289125d33c90026f742f5732acef9c98a58f6c5e87015598d631db4871dcb`; development parent `1f66199dfbd9b35780aee9cb93af0179277805085e9ac1bc61bbf2c9999b2fc0`.

| Variant | Native child result | G-code SHA-256 | G-code bytes | Native estimate | Layers | Total material |
|---|---|---|---:|---|---:|---:|
| Flat | 243 after slicing/G-code; 16.257 s | `8c25bf304f425ca763839839a030a88856afe7aeea336a925a18b27c7c286259` | 59,828,715 | 6 h 52 m 1 s | 25 | 18.37 g |
| Relief | 0; 20.293 s | `dc41c358a0ca015ddc2fae5aa9676e9cdacd13b7dc62a5029aa6db3d20ae54d5` | 61,221,300 | 7 h 12 m 22 s | 30 | 19.62 g |

G-code paths: `slicer/p1-r3-recovery/flat-run1/plate_1.gcode` and `slicer/p1-r3-recovery/relief-run1/plate_1.gcode`. Relief also produced `relief-run1/relief-sliced.3mf`, 12,357,361 bytes, SHA-256 `8e1a4d401631ea0853d559c5474aa8dcfb3d0a02481ffd8222b4482c602e6c57`. No flat sliced 3MF was produced. These are observations of local artifacts, not assertions that the user can open a review surface.

## Provisional settings and limitations

Native U1 four 0.2 mm nozzles; 0.08 High Quality process; 0.10 mm first layer; four Generic PLA profiles; Textured PEI Plate. Native four wall loops, 15% gyroid, support disabled, prime tower enabled preserved. Current 125 by 101.8 mm work scale remains provisional; whole assembly translation only, back down/face up. Physical heads 1–4 map T0 black, T1 gray, T2 white, T3 deep blue; glass provisionally uses white and does not test blue/white Full Spectrum mixing.

Initial output inspection finds actual T0/T1/T2/T3 commands in both; metadata lists four nozzles and complete filament arrays, and native log reports four physical extruders. Both command actual `M140 S65`, `M190 S65`, and nozzle printing temperature 220 C. Tool-use mass is flat 12.67/2.82/2.58/0.30 g and relief 13.91/2.91/2.36/0.44 g. This preliminary inventory does not independently establish spatial color assignment, detail survival, or motion bounds.

Both native runs report OpenGL shader/thumbnail rendering failures, including `can not get shader for rendering thumbnail`. A preset `thumbnails` string is not image evidence. Thumbnail acceptance remains blocked pending independent artifact inspection, even for child exit 0. Other retained logs include `calc_exclude_triangles:Unable to create exclude triangles` and `SupportSpotsGenerator does not currently handle different materials properly, only first will be used`; support is disabled, but do not silently suppress these native diagnostics.

Coverage: GM-R3-01 actual native slice generated for both; GM-R3-02 existing packaged meshes untouched, independent parity pending; GM-R3-03 merged settings and four-slot intent preserved, actual spatial tool mapping pending; GM-R3-04 exact results/hashes retained, independent detail/bounds/thumbnails pending; GM-R3-05 outputs diagnostic only and no printer contact occurred. Next: independent validator inspects frozen G-code/3MF geometry, toolpaths at text/logo/backing connectors, native warnings and thumbnail state. Do not claim printable or upload-ready from these successful toolpath generations alone.
