# Grenadier 車形冰箱磁貼

以已接受的 D4 卡通車圖製作 Snapmaker U1 平面磁貼。目前保留平整／浮雕兩版可調整來源，P1 R4 已完成相同尺寸的原廠 0.2／0.4 mm 設定切片比較；0.4 mm 較快，但 GRENADIER 小字未完整保留。最終尺寸與實體列印驗證仍待後續。[實際線路對照](https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-nozzles)。

權威輸入為 `references/d4-approved.png`、`docs/REQUIREMENTS.md` 與 active iteration frozen contracts。原圖 `references/photo-6-original.jpg` 保留來源與深藍意圖，不覆蓋 D4 已接受簡化。

目前 D7 候選鏈請檢查 `face-candidate-manifest.mjs`：

```sh
node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs
```

`intent-manifest.json` 是保留的 D5 intake 歷史記錄，不涵蓋 D7 衍生檔，也不得重寫來掩蓋後續變更。

產生 D7 正面色區與可攜對照頁（均使用原圖座標，沒有 mm）：

```sh
uv run python projects/grenadier-fridge-magnet/scripts/generate-face-vector.py \
  --input projects/grenadier-fridge-magnet/references/d4-approved.png \
  --output projects/grenadier-fridge-magnet/SVG/p1-r1/face.svg \
  --report projects/grenadier-fridge-magnet/SVG/p1-r1/face-report.json
node projects/grenadier-fridge-magnet/scripts/create-face-review.mjs
node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs --write
uv run python projects/grenadier-fridge-magnet/tests/test_face_vector.py
```

入口是 `review/p1-r1/face-review.html`：左側是固定 D4，右側是五個可切換的原生 SVG 色區。這是向量預覽，非 CAD 或可列印檔案。後續 CAD source 放 `src/`，明確 STEP 目標放 `STEP/p1-r1/`。Python 僅用 root uv workspace，不建立局部環境。

入口：[PROJECT_STATE.md](PROJECT_STATE.md)、[NEXT_AGENT.md](NEXT_AGENT.md)、[測試目標](tests/README.md)。

## P1 R2 — editable flat and relief mesh study

Authoritative new source: `src/parametric_magnet.py`; accepted face source/SVG/PNG remain unchanged. Both variants share exact artwork, independent XY and Z parameters, continuous black backing, and five visible material intents mapped to four real filament intents. Glass-mix remains an unresolved blue+white process placeholder.

From repository root:

```sh
uv run pytest projects/grenadier-fridge-magnet/tests/test_parametric_magnet.py -q
uv run python projects/grenadier-fridge-magnet/src/parametric_magnet.py --preflight
uv run python projects/grenadier-fridge-magnet/src/parametric_magnet.py
```

CLI exposes `--xy-scale`, `--working-mm-per-source-unit`, `--back-thickness-mm`, `--flat-face-depth-mm`, `--low-depth-mm`, `--middle-depth-mm`, `--high-depth-mm`; `--help` lists them. Defaults are development values, not selected physical dimensions. Feature records for plate, wordmark, and lamps expose separate anchors/bounds/scale/stroke, but nonidentity settings are explicitly rejected until a scoped feature-edit revision. Region polygon/ellipse defaults are editable in source; changing region boundaries changes heights only. `--config` accepts JSON `parameters` and optional identity-only `features`. Use a new `--output-tag` for new candidate geometry; generation writes the active iteration mesh report, which must be refrozen and reviewed with the new artifacts.

Current reviewed studies: `GLB/p1-r2-color-corrected/flat.glb` and `GLB/p1-r2-color-corrected/relief.glb`, bound by `docs/iterations/p1-r2-parametric/color-corrected-candidate-manifest.json`. Historical `p1-r2` and `p1-r2-connected` artifacts are retained evidence for rejected disconnected-backing and cyan-rendering candidates; do not use them as the current preview. Per-part STL files remain study/interchange evidence, **not fabrication candidates**. Exact pixel-grid contacts and thin backing connectors may not survive slicing or printing. Slicing must later resolve intended scale, toolpaths, glass mixing, and text/logo survival. No STEP/BREP or physical acceptance is claimed. P1 R3 diagnostic packaging and actual slicing evidence now follow below; these studies are not print releases.


## P1 R3 — actual diagnostic slices

Both unchanged variants were sliced with installed Snapmaker Orca2.3.5, native U1 0.2mm nozzle/0.08HighQuality and temporary GenericPLA at the current125×101.8mm work scale. Gcodes are `slicer/p1-r3-recovery/{flat,relief}-run1/plate_1.gcode`; relief additionally has `relief-sliced.3mf`. Flat estimates6h52m1s/18.37g and relief7h12m22s/19.62g. These are diagnostic estimates, not approved final dimensions or physical evidence.

[Current handoff](docs/iterations/p1-r3-slice-probe/HANDOFF.md) binds source, settings, commands, hashes and independent review. [Independent validation](docs/iterations/p1-r3-slice-probe/INDEPENDENT_SLICE_VALIDATION.md) finds both texts and all four main lamps present, with fragmented fine gray trim and plate/letter gaps. Actual-path SVG media is in `slicer/p1-r3-validation`; glass remains provisionally white. Missing embedded thumbnails and unresolved physical/structural details block prepared/print release. The next smallest experiment is a scoped detail coupon, with final width still deferred.

[實際刀路檢視頁](https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-slice) 已完成 Mac 瀏覽器檢查；手機端未觀察。生命週期與恢復方式見 [delivery record](docs/iterations/p1-r3-slice-probe/SLICE_PREVIEW_DELIVERY.md)。
