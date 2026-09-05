# Laifen Wave 工作流程摘要與 8 分鐘現場示範

## 這次示範要傳達的流程

我們先把問題分成「觀察、意圖、參數、實體 CAD、獨立檢查、實體接受」幾層。下載的空殼可以完整旋合，但裝入 stainless-steel Wave 後不能閉合；因此它證明的是 loaded obstruction，不足以證明碰到哪一端。使用者回報原本的寬度剛好合適，所以目前保留 body bore `30 mm`、cap bore `31 mm`，不把孔放大到 `32 mm`。裝置尺寸 `L=208 mm`、`D=29 mm` 是 approximate inputs，不是量測結論。

接著用小型 coupon 先驗證旋合關係。`0.20 / 0.25 / 0.30` 三個版本由使用者回報都能以手旋合；這是 hand-closure report，不能冒充 R7 本體的 exact fit proof，也沒有替代 torque、wobble、五循環或完整裝置測試。

兩排 grip 曾被拒絕，因為不足以作有意義的手感測試。於是採用 procedural skin，保留原本 diamond motif 的比例，以 constant axial pitch `4.8 mm` 和 shared phase 跨過 seam。外徑統一為 `39 mm`，pattern 覆蓋整個外側，不再有 bulged collar 或外部 smooth collar。軸向 allowance 是 `5 mm`；由 approximate `L208` 得 cavity `C213`，外部總長約 `219 mm`。目前 R7 的真正可編輯例外是兩個封閉端的 `end_chamfer_size=1.20 mm`，允許範圍 `0.80..1.50 mm`，是 45-degree circular trim，並非 viewer-only slider。

目前 R7 的核心數字是 body/cap bores `30/31 mm`、cavity `213 mm`、approximate outside device envelope `L208 / D29`。body 和 cap 的高度約為 `144 / 84 mm`；`closed_c25.step` 顯示兩件組合的 outside length `219 mm`。因此 nominal total slack 是 `5 mm`，但 centered `2.5/2.5` 只是一個 readout；bottom-resting 會是 `0/5`，而且目前沒有 retention。這些是 CAD/source 與 written STEP 的結果，不是 printed acceptance。

R7 是 STEP-first、source-authoritative。`params.py` 產生真正的 BREP；`body.step.py`、`cap_c25.step.py`、`closed_c25.step.py`、`print_layout.step.py` 再寫出四個 STEP。實作、獨立 validation、critique、formal review 是不同角色；這次曾針對實際 STEP 修復 end-cone endpoint consistency，通過既有 source-to-STEP parity gate。正式結論只接受 exact default R7 的 CAD/source 與 written STEP。Slicer/process、support-free tall print、loaded fit、end contact、drainage in use、thread strength、physical acceptance 都仍是 HOLD。

## 8 分鐘 spoken runbook

**0:00–1:00｜先展示問題。** 拿出 physical coupon，說明「空殼能旋合，loaded case 不能閉合」這個觀察。請觀眾分辨 observation 和 inference：它沒有告訴我們是 axial contact、diameter interference，還是其他 obstruction。補充使用者已報告三個 `0.20/0.25/0.30` coupon 都能手動閉合。

**1:00–2:00｜展示原本的寬度決策。** 在目前的 OpenSCAD simulator 產生 Laifen 預設，先看兩件 openings-up 的 print layout。指出 `30/31` 是保留原寬度的 CAD contract；`D29` 只提供 `0.5/1.0 mm` nominal radial readouts。問：「這個畫面是否清楚顯示 nominal gap 不是 retention？」

**2:00–3:15｜展示參數來源。** 打開 [params.py](../cad/p1_r7_end_chamfer/params.py)，指出 `device_length`、`device_diameter`、`axial_allowance`、`outer_diameter`、`skin_axial_pitch` 和 `end_chamfer_size`。說明 constant pitch 保持 pattern proportions，`C=L+5` 推出 `213`，而不是把模型以 Z-scale 拉長。這一步固定的是「哪個參數控制什麼」，不是即時 rebuild 承諾。

**3:15–4:30｜看端部特寫。** 打開目前的端部 closeup，讓觀眾看真正圓形的 smooth chamfer、連續 diamond skin，以及 seam 彼此分開。R7 預設 `1.20`，可選 `.80..1.50`；`1.40` 的證據只是 source-native sensitivity，不是另一個已發佈 STEP。展示 [R7 README](../cad/p1_r7_end_chamfer/README.md) 中的 45-degree equation 和 `0.75 mm` default smooth band。

**4:30–5:30｜解釋水孔與方向。** 在 simulator 中看封閉端的 seven drains（center plus six at `R9`，各 `Ø3 mm`），再回到 openings-up print layout。這驗證幾何位置和 occurrence transform；沒有宣稱實際排水或 slicer support-free。

**5:30–6:30｜說明獨立檢查。** 用一句話交代角色分工：source implementation 產生 BREP，independent validation 檢查 math、collision/protected regions、constraints 和 STEP parity，critique 看實際端部與 silhouette，formal review 只 join 這些 receipt。這避免把漂亮的 viewer screenshot 當作 physical proof。

**6:30–7:30｜明確 acceptance boundary。** 說明現在 PASS 的是 exact default R7 CAD/source 和 written STEP；HOLD 的是 slicing、tall-part adhesion、loaded full closure、literal neither-end contact、thread wear/strength、actual drainage 和 physical acceptance。請觀眾回答：「你是否同意這個檔案可以進入下一個 slicer/physical validation 階段，但尚未被稱為完成品？」

**7:30–8:00｜收尾與連結。** 主檔案是 `cad/p1_r7_end_chamfer/print_layout.step`，STEP SHA-256 `80fd95845b51da5266883614f9bf8eff60793a24d5c39b7321c9c6cb16d477a4`。目前唯一 live review surface 是 `https://mac-mini.duckbill-ionian.ts.net:8448/openscad-simulator/`；LC-VAL-02 驗證該 route 與六個 built assets 都是 HTTP 200 且 bytes 相符。以前 8449 CAD Viewer、P1 R7 closeup 與 P2 R3 的記錄只保留為歷史證據，不宣稱現在可用。Actual-user Safari rendering 仍未確認。

這份檔案是 workflow summary 與 spoken runbook，不是 generated presentation。Presentations runtime 的 `load_workspace_dependencies` loader 缺失，因此沒有 PPTX；不可把預覽頁或本文件說成投影片。

## 明確限制

沒有新增 measured length、support-free slicing、final print、instant rebuild、physical acceptance，也沒有把照片 attribution 給 R7。照片和尺的內容仍是 physical reference/observation；它們不會自行升格為 CAD 或實體結論。
