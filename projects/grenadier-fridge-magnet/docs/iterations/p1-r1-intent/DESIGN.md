# Design — D5 face-only

<!-- frozen:start -->
## Frozen selected design contract

当前候選是正面 2D 表達，沒有幾何厚度。權威美術為 `references/d4-approved.png`，原 bitmap 不可變。`references/photo-6-original.jpg` 僅供來源與深藍意圖參照；不可恢復 D4 已接受簡化掉的細節。

D7 目標為原生 SVG／等價可追溯 2D 向量來源，以 D4 原圖畫布、比例與座標對齊。五個 named visible classes：black、gray、white、deep-blue、glass-mix；各區域使用非重疊的可填色邊界表達，背景與外部留白不成為車形物件。white 輪廓需保留 D4 的車形白邊，不能把整張白色方形背景納入輪廓。原圖未附物理尺寸，不指定 mm。

視覺類別對照：black→黑線材；gray→灰；white→白；deep-blue→原圖深藍色意圖；glass-mix→相同藍與白的後續混色策略。2D 可用淡藍顯示 glass-mix 意圖，但不宣稱可直接得到該印色。漸層和抗鋸齒需歸類，保留四燈、兩組字與圖形識別；清理應可對照來源並在 provenance 中記錄。

### Per-object delta mask

| Object | 可變 | 禁止 |
|---|---|---|
| D4 reference | 等比例展示 | 原始 bytes、構圖、字樣或色意圖修改 |
| 2D vector candidate | 依 D4 建立分色邊界、可追溯抗鋸齒／漸層歸類 | 靜默刪四燈／字／玻璃或重作美術 |
| Review surface | 左右對照、色區標示／疊圖 | 尺寸／磁鐵 controls、剖面或製程選擇 gate |
| 原圖 Photo 6 | 原封複製／參照深藍意圖 | 蓋過 D4 接受的簡化 |
| Future CAD／孔 | 無 | 實作厚度、孔位、配合、BREP／mesh |

2D cheap gates：原始圖 hash 不變；向量各色區存在且閉合可填；所有 source units 不混入 mm；背景排除；D4 外輪廓與四燈及字樣逐項可視比對；trace 來源／指令／參數可追溯。D7 不可自我批准候選，獨立 read-only validation 對照 frozen artifact。

### Deferred risks

R1 調研的平面 Full Spectrum 色效果不確定，需要後續 coupon；不是 2D 分色的 blocker。薄字與輪廓的 nozzle 解析度、正面／背面列印策略、磁鐵與強度都留待正面 source 存在後處理。
<!-- frozen:end -->

## Mutable progress

曾草擬 100 mm／總厚3 mm／2 mm 磁鐵的剖面提案，尚未提交 review surface。最新「先不選。一步一步來」「洞很好加」令它退出當前範圍；數字沒有被 user-approved，禁止偷偷當作 D7 預設幾何。D5 沒有建立剖面頁、孔或 CAD。

已直接查看兩份供圖；D4 四燈與 GRENADIER／DJZY 608 仍可辨認。這是 raster 視覺觀察，尚非向量精度、stroke 或製程驗證。
