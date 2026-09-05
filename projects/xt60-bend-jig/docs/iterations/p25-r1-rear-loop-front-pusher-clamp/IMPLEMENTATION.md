# P25-IMPLEMENT-01 receipt

日期：`2026-09-05`
狀態：**可執行 first-CAD candidate；未經獨立 critique/validation/review；不可列印**

## Verified input

- `shasum -a 256 -c .../DESIGN_INPUT_MANIFEST.sha256`：16/16 `OK`。
- P25-DESIGN-02 的 `BRIEF.md`、`DESIGN.md`、`TASK_DAG.md` 已在實作前重新讀取；其尺寸與三狀態 supersede 初始 prompt 的衝突值。

## Implemented scope

- source-first P25 module，保留 P20 `role,u -> PointYZ` authority。
- 三狀態：`PRECLAMP_END`、`LATCHED_END`、`RELEASED_CLEAR`。
- 每側四個 named solids：rear yoke、front pusher bar、OD2 hinge pin envelope、opening spring envelope。
- 左右 X 鏡像；桿維持精確 OD4 x 50 mm；cap/screw cassette/pressure plate/floating shoe 為零。
- X stack：outer plate face 21.00、gap 0.30、module 3.20、outboard 24.50、rod tip 25.00，保留 0.50 mm margin。

## Commands and results

1. `uv run pytest -q projects/xt60-bend-jig/tests/test_p25_r1_rear_loop_front_pusher_clamp.py`
   - **PASS: 19/19**。
2. `uv run python` source/actual-solid diagnostic：
   - 左右 Blue/Green rear-yoke contact：距離約 `5.3e-15 mm`、intersection `0.0 mm3`。
   - Orange locked pad contact：距離約 `5.1e-15 mm`、intersection `0.0 mm3`。
   - 60 deg released Orange clearance：`15.0323829306 mm`。
   - latch released gap：`23.7352877515 mm`。
   - P25-only pairwise positive-volume intersections：無。
   - P25-to-P20 context positive-volume intersections：無。
3. `build123d.export_step(...)`：四個 STEP 均回傳 `True`。
4. `build123d.import_step(...)` parity：
   - 三個組裝狀態皆 source/STEP `21` solids、bounds delta 全為 `0`。
   - solid-volume sum delta 約 `-1.78e-9 mm3`。
   - exploded source/STEP 皆 `8` solids，volume sum 相同。
5. P20+P24+P25 combined regression command：**由使用者中斷，無 PASS/FAIL 結果**；未重新執行。

## Artifacts

- `p25_r1_preclamp_end.step`
- `p25_r1_latched_end.step`
- `p25_r1_released_clear.step`
- `p25_r1_modules_exploded.step`
- 對應四個 `.step.py` generator。

完整 artifact/source hashes 見 `CANDIDATE_MANIFEST.sha256`。

## Blockers and limits

- 沒有完成 snapshot 或 CAD Viewer readiness；使用者要求停止等待並立即交付。
- opening spring 只有空間 envelope；彈力、彈開速度、手感與重力獨立性未經物理驗證。
- P20 既有 OPEN Blue/XT60 collision 仍獨立存在；P25 未修正或隱藏。
- 未完成獨立 critic、validator、formal review；本 receipt 不是自我核准。
- 未做切片、列印、fit、疲勞、蠕變或 holding-force acceptance。

## Repair 1 — early-release latch collision

日期：`2026-09-05`
範圍：只修 `CRITIQUE.md` 的 `P25-C01`；不處理其他 critique findings。

### Source delta

- 保留 receiver、quick hook、rear yoke、front bar 與所有 frozen topology。
- 將 hook mouth 從 rod-row tangent 改成由同一 hinge/latch frame 純數學導出的圓弧瞬時退出方向：對 hinge-to-latch `(dy,dz)`，bar frame 中固定 receiver 的退出單位向量為 `(dz,-dy)/length`。
- 新增 `latch_sweep_clearances()` actual-solid regression authority；沒有改 OD4x50、P20 paths、locked 三桿接觸、X-stack 或 60 deg released pose。

### Commands and results

1. `PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider projects/xt60-bend-jig/tests/test_p25_r1_rear_loop_front_pusher_clamp.py`
   - **PASS: 20/20**。
2. Actual-solid `front_pusher_bar` vs complete `rear_yoke`（含 receiver），左右結果鏡像一致：
   - `0,1,2,3,4,5,10,30,60 deg` 全部 `intersection = 0.0 mm3`。
   - `1 deg` distance `0.2457377051 mm`。
   - `5 deg` distance `0.1435075311 mm`，符合 5 deg 前已有正分離。
   - `10/30/60 deg` distance `0.8 mm`。
3. Locked rod contacts 保持：
   - rear-yoke/Blue 與 rear-yoke/Green distance 約 `5.33e-15 mm`、intersection `0.0 mm3`。
   - front-bar/Orange distance 約 `5.11e-15 mm`、intersection `0.0 mm3`。
4. 四個 `.step` 均重新由 source 產生；`build123d.export_step(...)` 全部回傳 `True`。
5. STEP reopen/source parity：三狀態皆 `21/21` solids、bounds delta 全零、solid-volume sum delta 約 `-1.77e-9 mm3`。
6. `shasum -a 256 -c .../CANDIDATE_MANIFEST.sha256`：見 Repair 1 最終驗證；manifest 更新為本 candidate bytes。
7. Snapshot／Viewer handoff 嘗試：
   - `uv run cadgen step snapshot ...p25_r1_latched_end.step ...p25_r1_latched_end_repair1.png`：失敗，root uv 環境沒有 `cadgen` console script（`Failed to spawn: cadgen`）。
   - `uv run python -m cadgen.viewer --help`：失敗，`No module named cadgen.viewer`。
   - 因此 Repair 1 未產生新的 snapshot 或 live Viewer link；既有未追蹤 PNG 沒有被覆寫或當作 Repair 1 證據。

### Remaining limits

- Repair 1 只關閉 early-release rigid collision；spring causality、saddle/pad fidelity、axial retention、load equalization 與 user-facing Viewer/snapshot findings仍由獨立 review 判定。
- 目前 root uv runtime 缺少 CAD skill 所需的 snapshot／Viewer CLI；本次只具 source、actual-solid diagnostics、tests 與 STEP reopen/parity 證據。
- 無 commit、無 push、無 continuity 修改。
