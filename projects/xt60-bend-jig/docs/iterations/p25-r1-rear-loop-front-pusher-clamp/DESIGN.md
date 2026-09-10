# P25 R1 後環＋前壓桿快速夾具 design

日期：`2026-09-05`  
設計角色：`P25-DESIGN-02`  
輸入 authority：同目錄 `DESIGN_INPUT_MANIFEST.sha256`  
狀態：**設計完成，等待獨立實作；第一版 CAD 假設，非列印 authority**

## 1. 座標、身份與狀態

- X：三支金屬桿軸向；左右模組只做 X 鏡像。
- FRONT：世界 YZ；`+Z` 為 XT60 mating-head/up，`+Y` 為 wire-tail/outward。
- `Blue`、`Orange`、`Green` 的 YZ 中心必須由現有 P20 路徑函式取得，不可重寫或近似。
- 使用者動作固定為：Orange DOWN；Blue 與 Green BACK-to-FRONT；三者皆為手動輸入。
- 夾具閉合參數 `c` 與主機構參數 `u` 必須獨立；任何 `c` 變化都不得改變 rod center。

第一版 CAD 顯示三個狀態：

1. `PRECLAMP_END`：`u=1`；後軛已靠在 Blue/Green，前壓桿張開，Orange 無接觸。
2. `LATCHED_END`：`u=1`；前壓桿閉合並扣住，Orange 壓塊與 Orange 相切；後軛同時承托 Blue/Green。
3. `RELEASED_CLEAR`：`u=1`；快扣解除，前壓桿由開啟偏壓旋開至少指定角度，Orange 有正間隙。之後使用者取下左右模組，再讓主機構返回 OPEN。

P25 R1 不把夾具建模為沿完整 OPEN-to-END 路徑滑動的永久載具。

## 2. 零件與接觸拓撲

每一側模組包含：

- `rear_yoke_<side>`：一體式後軛，含 Blue 與 Green 的開口弧形承托座、鉸鏈耳及快扣接收鉤。
- `front_pusher_bar_<side>`：前方旋轉桿，含只對 Orange 的局部凹面壓塊、鉸鏈耳、快扣舌及手指釋放片。
- `hinge_pin_envelope_<side>`：概念性光滑 pin envelope；不是第四支成形桿。
- `opening_spring_envelope_<side>`：鉸鏈扭簧或等效開啟偏壓的保留空間；R1 可只顯示 envelope，不宣稱彈力。

不得新增 Blue/Green/Orange 共用滑鞋、壓板、螺桿、cap 或連接內外板的支架。

### `LATCHED_END` 的有意接觸

- `rear_yoke` 的 Blue saddle 與 Blue 圓柱表面：零距離、零正體積穿透。
- `rear_yoke` 的 Green saddle 與 Green 圓柱表面：零距離、零正體積穿透。
- `front_pusher_bar` 的 Orange pad 與 Orange 圓柱表面：零距離、零正體積穿透。
- 鉸鏈 pin／耳與 latch hook／舌為各自的閉合反力界面。

受力圈為：
`Orange -> Orange pad -> front bar -> hinge + latch -> rear yoke -> Blue + Green`。
任何零件都不得接觸 XT60 外殼作為反力來源。

### `RELEASED_CLEAR` 的有意關係

- latch hook 與舌完全脫離，最小幾何間隙 `>=0.60 mm`。
- front bar 繞 X 軸旋開，Orange pad 至 Orange 的最小距離 `>=3.00 mm`。
- rear yoke 可暫時鬆放在 Blue/Green 上，但不得再形成三桿閉合受力圈。
- 開啟偏壓方向必須把 front bar 帶離 Orange；禁止依賴重力方向。

## 3. 第一版可調尺寸

下列尺寸是 CAD 起始值，不是已量測或物理驗收值：

| 參數 | 起始值 | 分類／目的 |
|---|---:|---|
| `rod_od` | `4.00 mm` | 不可變 purchased part |
| `rod_length` | `50.00 mm` | 不可變 purchased part |
| `rod_end_x` | `+/-25.00 mm` | 由長度導出 |
| `outer_plate_face_abs_x` | `21.00 mm` | inherited reference |
| `plate_to_module_gap` | `0.30 mm` | 第一版 running clearance |
| `module_axial_thickness` | `3.20 mm` | 使用現有約 4 mm 桿端突出量 |
| `rod_tip_margin` | `0.50 mm` nominal | 防止模組超出桿端；由 X stack 驗證 |
| `rear_saddle_diameter` | `4.35 mm` | Blue/Green 第一版鬆配合 |
| `rear_saddle_wrap_angle` | `120 deg` | 鎖定時承托但不作永久 snap-fit |
| `orange_pad_diameter` | `4.30 mm` | Orange 局部凹面起始值 |
| `orange_pad_wrap_angle` | `70 deg` | 只對 Orange 的局部接觸 |
| `yoke_min_wall` | `3.00 mm` | 第一版 FDM 結構假設 |
| `front_bar_min_wall` | `3.00 mm` | 第一版 FDM 結構假設 |
| `hinge_pin_diameter` | `2.00 mm` | 概念性 smooth pin envelope |
| `hinge_running_clearance` | `0.25 mm` radial | 第一版列印配合假設 |
| `released_open_angle` | `60 deg` | 確保 pad 離開 Orange |
| `released_orange_clearance` | `>=3.00 mm` | release 幾何 gate |
| `latch_hook_engagement` | `1.20 mm` | 第一版正扣合深度 |
| `latch_clearance` | `0.25 mm` | 第一版快扣配合假設 |
| `latch_release_travel` | `1.50 mm` | 手指片使 hook 脫離的幾何行程 |
| `release_tab_length` | `7.00 mm` | 單手解扣的初始手指空間 |
| `spring_envelope_od` | `6.00 mm` | 扭簧／等效偏壓保留空間 |
| `spring_wire_envelope` | `0.50 mm` | 僅空間檢查，不是採購規格 |

左右模組的 YZ 形狀相同，只有 X placement 與 side label 鏡像。模組 X stack 必須完全落在外板面與 rod tip 之間，且對外板保持正間隙。

## 4. 幾何與實作規則

1. 建立單一純數學函式提供 `role,u -> PointYZ`，直接委派給 inherited authority；所有 rod、saddle、pad 與測試共用它。
2. 後軛的 Blue/Green saddle 中心只由 `u=1` 的 inherited centers 導出；front pad 中心只由 `Orange,u=1` 與 pad offset 導出。
3. 鉸鏈軸平行 X。front bar 的 released placement 必須由同一個剛體旋轉函式導出，不可手動建立另一份座標。
4. 左右模組由同一份 source 以 `side_sign` 鏡像；禁止複製兩套尺寸。
5. rigid CAD 的三個 rod contact 只表達 nominal tangent topology，不以實體穿透模擬 preload。
6. 若需要夾緊量，只能用命名參數 `orange_pad_offset` 表達；第一版預設 `0.00 mm`，允許後續 physical gate 在 `-0.30..+0.30 mm` 內調整。
7. latch 必須有 lead-in、正 engagement、release tab 與 opened clearance；不得把視覺重疊當作扣合。
8. spring envelope 必須在 locked 與 released sweep 中不碰三支桿、外板、XT60 或 front bar。實際彈簧選型延後。

## 5. 必要驗證

### Math

- rod OD、長度、端點精確為 `4.00`、`50.00`、`+/-25.00 mm`。
- `clamp_state` 不改變任何 rod YZ center。
- 左右模組所有對應點滿足 X 鏡像且 YZ 相同。
- released bar 是 locked bar 繞同一 hinge axis 的剛體旋轉。
- X stack 證明模組不穿出 rod tip，且與外板保有 `>=0.30 mm` 間隙。

### Constraint／requirement

- 恰好三支 forming rods、兩個 rear yokes、兩個 front bars、兩個 hinge envelopes、兩個 spring envelopes。
- cap、screw cassette、pressure plate、floating shoe 數量皆為零。
- Orange pad 只可接觸 Orange；rear yoke 只以指定 saddles 接觸 Blue/Green。
- source 不得修改或取代 P20 rail/path functions。

### Actual-solid collision and contact

- `LATCHED_END`：六個 rod-contact pairs（三個／側）皆零距離、零正體積穿透；所有其他 P25-to-context pair 不得有正體積干涉。
- `PRECLAMP_END` 與 `RELEASED_CLEAR`：Orange pad 有正間隙；released clearance `>=3.00 mm`。
- front bar 從 locked 到 `60 deg` 的代表性 sweep 至少檢查 `0, 10, 30, 60 deg`；除鉸鏈 allow-list 外不得碰 rod、plate、XT60、wire envelope 或 rear yoke。
- latch release position須有 `>=0.60 mm` 脫離間隙。
- 既有 baseline collision 必須單獨報告，不得算成 P25 新增碰撞或被隱藏。

### Artifact／visual

- written STEP 必須有 closed、valid、positive-volume solids，並與 source 的 occurrence count、labels、bounds 對等。
- 至少輸出 `PRECLAMP_END`、`LATCHED_END`、`RELEASED_CLEAR` 三個組裝視圖，以及左右模組 exploded view。
- Snapshot 必須清楚顯示後軛承托 Blue+Green、前壓塊只碰 Orange、鉸鏈、對側快扣、解扣後 pad 離開 Orange，以及左右兩端同時支撐。
- CAD Viewer 頁面與 exact artifact endpoint 均需驗證 ready；Viewer 成功不等於 CAD 或物理驗收。

## 6. 風險、停止條件與後續 physical gate

若任一情況發生，停止實作並重開設計：

- 需要改 50 mm rods、rail/path、plate 或 XT60 位置才能裝入；
- rear yoke 在主機構運動前就耦合或驅動 Blue/Green；
- front pad 同時碰到 Blue、Green、plate 或 XT60；
- release 需要翻轉裝置或重力才離開 Orange；
- 模組只能靠 solid interpenetration 才能顯示鎖定；
- 只有單側模組能閉合，或左右閉合會迫使 rod 傾斜；
- 桿端有效軸向空間不足以容納 `plate gap + module thickness + tip margin`。

第一版 CAD 通過後仍未解決：實際 rod protrusion、公差、後軛鬆緊、快扣按力、扭簧規格、彈開速度、雙側安裝順序、左右負載均衡、PETG 疲勞／蠕變、熱、磨耗、手指空間、裝卸速度及真實 holding force。以上必須由尺寸量測、fit coupon 與完整 physical prototype 分開驗證。
