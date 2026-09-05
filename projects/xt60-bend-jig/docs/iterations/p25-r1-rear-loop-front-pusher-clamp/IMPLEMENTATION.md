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
