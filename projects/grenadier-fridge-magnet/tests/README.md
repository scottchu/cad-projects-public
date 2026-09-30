# Focused evidence plan

尚無 CAD 或2D vector實作，沒有為常數或空目錄編造測試。

D7 2D 候選的 credible risks：外白背景被誤當車形輪廓；四燈／字／玻璃在 threshold 中消失；mask重疊或孔洞；來源 hash／座標不一致。使用真實向量的結構檢查與 raster並排／疊圖驗證，記錄實際命令。

執行 `uv run python projects/grenadier-fridge-magnet/tests/test_face_vector.py`。它以真實 D4 供圖檢查五個 mask 不重疊、外部白背景沒有變成 sticker fill、白邊仍在、DJZY 608 深藍、前擋 glass-mix 與 GRENADIER 細節仍存在，並檢查重生 SVG 位元組穩定且不改來源。這些是 face-only source checks，不是 printability 測試。

也可執行 `node projects/grenadier-fridge-magnet/scripts/intent-manifest.mjs` 檢查 D5 frozen intake；這不是 printability測試。

後续若進CAD，另凍結 math、actual-solid collision、constraints、user-requirements 與 source/export parity targets，先廉價 analytic gates，再 solids。材料混色／字可辨識／磁鐵fit則需物理coupon。
