# Requirements — P1 R1 face-only

使用者在 D4 接受後說「OK next」，接著縮限：「先不選。一步一步來」「洞很好加」。最新指令立即取代尺寸／磁鐵提案的當前範圍；只處理正面 2D 分色，洞留待後續。

| ID | 類型 | 當前契約 | 證據／驗證 |
|---|---|---|---|
| GM-01 | invariant | 平面車形冰箱磁貼，Snapmaker U1 | 使用者意圖；實物待驗 |
| GM-02 | invariant | 保留已接受 D4 輪廓、四盞圓燈、GRENADIER、DJZY 608 及簡化程度 | D4 原圖 hash；D7 2D 對照 |
| GM-03 | invariant | 四種實體線材：黑、灰、白、原圖深藍；車牌維持原圖深 royal blue 色意圖 | 原圖來源；材質色號未定 |
| GM-04 | invariant | 淡藍玻璃為藍＋白 Full Spectrum 混色意圖 | 2D 獨立標記 glass-mix；不是第五卷線材，實際混色待後續 coupon |
| GM-05 | invariant | 現在只做 2D 正面色區，保持步驟小且可比對 | 最新使用者縮限；禁止孔、剖面、尺寸 controls |
| GM-06 | design choice deferred | 磁鐵、孔、總厚、實體尺度、固定方式與 print orientation 全部後續再選 | 不作當前 2D 工作前置條件 |
| GM-07 | invariant | 0.4 / 0.2 mm 是噴嘴直徑 | 不是 layer height；nozzle 與線寬未選 |
| GM-08 | derived constraint | 2D 五個視覺類別：black、gray、white、deep-blue、glass-mix，映射到四種實體線材意圖 | 來源色抗鋸齒／漸層需歸類；背景不能成為實體外框 |
| GM-09 | invariant | 無活動零件，不把 D4 的透視汽車轉成立體汽車 | face-only 圖形拓樸檢查 |

2D 座標提案：沿 raster +x 向右、+y 向下，保持方形畫布與原圖對齊，以原圖像素／viewBox 單位工作。沒有 mm scale；未來 CAD 可定義 XY/+Z，当前不決定 build orientation。

當前使用順序：D4 原圖 → 2D 分色色區 → 並排／疊圖檢查輪廓、四燈、字與玻璃 → 使用者判斷正面 → 後續才談尺度、厚度、磁鐵、nozzle 與製程。

非目標：不重畫 D4 美術，不加第五種實體線材，不做孔，不做 3D／STEP／STL／3MF，不切片／上傳／开印。2D 工作者可以做可追溯的向量化／色區清理，但不能靜默刪掉保留項或把螢幕色當成列印色保證。
