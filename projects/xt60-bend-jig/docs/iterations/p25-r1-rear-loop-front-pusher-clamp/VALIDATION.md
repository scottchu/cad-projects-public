# P25-VALIDATE-01 Repair 2 independent geometry validation

日期：`2026-09-05`
角色：`P25-VALIDATE-01`（獨立 geometry validator；未修改 candidate source、tests、STEP 或 continuity）
唯一候選 commit：`a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`
候選 manifest file SHA-256：`88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`
判定範圍：**first-CAD geometric preview only；不代表列印或物理驗收**

本 receipt 的 authority、commands、數值、STEP、render package 與 validation snapshots 只指向上述 frozen Repair 2 candidate。`7354f85`、`7287e69` 與舊 validation 結論均不屬於本文件 authority。

## 結論

**PASS — first-CAD preview only。**

Repair 2 已建立兩條可區分的 actual-solid 路徑：neutral／未按 release tab 時，front bar 在 `1–5°` 遇到 positive-volume retention barrier；receiver 沿指定方向位移 `1.50 mm` 後，front bar 在規定的 `0/1/2/3/4/5/10/30/60°` sweep 全程零正體積碰撞，且 `5°` gap 為 `0.737800 mm`。因此 Repair 1 的「自由退出、沒有真正保持 locked state」blocker 已關閉。

這個 PASS 只確認 frozen CAD 的拓撲、尺寸、接觸、碰撞、出口路徑及 STEP parity。Cantilever 所需按力、應變、回彈、疲勞／蠕變、實際 spring force、立即彈開速度、holding force、摩擦、公差與手感仍未驗證。

## Frozen authority 與 manifests

在 repository root 執行：

```text
git rev-parse HEAD
# a1932fb19ffeb6d584153d1c201ebe24b2e06d6a

shasum -a 256 projects/xt60-bend-jig/docs/iterations/p25-r1-rear-loop-front-pusher-clamp/CANDIDATE_MANIFEST.sha256
# 88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845

shasum -a 256 -c projects/xt60-bend-jig/docs/iterations/p25-r1-rear-loop-front-pusher-clamp/CANDIDATE_MANIFEST.sha256
# 13/13 OK

shasum -a 256 -c projects/xt60-bend-jig/docs/iterations/p25-r1-rear-loop-front-pusher-clamp/DESIGN_INPUT_MANIFEST.sha256
# 16/16 OK
```

Manifest 中的主要 authority hashes：

- source：`34ab12f4fa4bf93a45cef5175e1faf4ad3a0efb6979e9dea4d499e8f737bf47f`
- focused tests：`c9f904d737daede8642086681943b44a75fac6ca6543a89433d4e4dc26dde2a3`
- `PRECLAMP_END.step`：`58360faf6a30245134a71dd0bc986451c96218b2e6e90b1da32fe711dd2b0de3`
- `LATCHED_END.step`：`5008c945cf2d8145efd37375ef31d3bd1bdeda7be58ca2c01e79a9bf98fbd0bb`
- `RELEASED_CLEAR.step`：`4ff5fea0dc720b58825a7f72c49f64e543b10cc1777cbd92e27c50d871fd08e6`
- exploded STEP：`6a4b9bcc2e1f06832888781609b768ebdba45b28f4120422e1c4a1502c399ffe`

## Tests 與 regressions

### Focused P25

```text
PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider \
  projects/xt60-bend-jig/tests/test_p25_r1_rear_loop_front_pusher_clamp.py
# 23/23 PASS
```

### Targeted P20 R4 + P24 + P25

先以 `--collect-only -q` 核對組成：P20 R4 `6`、P24 `13`、P25 `23`，共 `42` tests；再執行：

```text
PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider \
  projects/xt60-bend-jig/tests/test_p20_r4_custom_profile_full_cad.py \
  projects/xt60-bend-jig/tests/test_p24_r1_manual_three_slider_clamp.py \
  projects/xt60-bend-jig/tests/test_p25_r1_rear_loop_front_pusher_clamp.py
# 42/42 PASS
```

### Baseline print-kit fixture drift（分開，不算 P25 failure）

```text
PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider \
  projects/xt60-bend-jig/tests/test_p20_r4_print_kit_3mf.py
# 1 passed, 2 failed
```

兩個失敗都是既有 P20 print-kit fixture SHA drift：fixture 預期 parent SHA `3eb9187ec7ad9205a2a1ced5e15e5a87a2a5a24e6c76282193ed086fb776d5b8`，目前 P20 parent SHA 為 `d4c9d5bc428d3e426df1e80099ceef33b1de820fa8af6b4f5a569e97d2480d58`。失敗項目為：

- `test_source_print_kit_is_exact_13_unchanged_separate_solids_on_bed`
- `test_written_step_preserves_13_labels_and_source_volumes`

此 drift 不由 P25 source 引入，也不改變本次 first-CAD P25 判定。

## Exact geometry、身份與 invariants

使用 root `uv run python` 執行獨立 pure-math、actual-solid、occurrence、bounds、distance 與 intersection diagnostic；不是只讀參數或截圖。

### Rod、occurrence 與 forbidden architecture

- 三支 forming rods 精確為 `OD 4.00 × 50.00 mm`，每支 bounds `50 × 4 × 4 mm`，端點 `X=±25.00 mm`。
- 每個 assembled state：`3` rods、`2` rear yokes、`2` front bars、`2` hinge envelopes、`2` spring envelopes。
- cap、screw cassette、pressure plate、floating shoe：全部 `0`。
- exploded STEP：左右各一個四件式 module，共 `8` solids。
- P20 path delegation 在 Blue／Orange／Green、`u=0/0.25/0.5/0.75/1` 的最大座標差：`0 mm`；P25 clamp state 不改 rod centers。

### 左右鏡像與 X-stack

- 左右 corresponding geometry 的 mirror max delta：`7.1054e-15 mm`；YZ bounds 相同。
- 外板外表面：`|X|=21.00 mm`。
- module inboard：`|X|=21.30 mm`，plate clearance `0.30 mm`。
- yoke／spring／front bar centers：`|X|=21.90 / 22.90 / 23.90 mm`。
- module outboard：`|X|=24.50 mm`；rod tip：`|X|=25.00 mm`；tip margin `0.50 mm`。
- 因此兩個 mirrored modules 均留在現有 50 mm rod ends 內；沒有把桿長改成 60 mm。

### `LATCHED_END` contacts（左右一致）

| Pair | distance | positive-volume intersection |
|---|---:|---:|
| rear yoke / Blue | `4.4–5.3e-15 mm` | `0 mm³` |
| rear yoke / Green | `5.3e-15 mm` | `0 mm³` |
| front bar / Orange | `5.1e-15 mm` | `0 mm³` |
| front bar / Blue | `2.100000 mm` | `0 mm³` |
| front bar / Green | `1.229016611 mm` | `0 mm³` |
| rear yoke / Orange | `1.317643876 mm` | `0 mm³` |

Nominal reaction chain 因而保持為 `Orange -> Orange pad -> front bar -> hinge + retained latch -> rear yoke -> Blue + Green`。三個 assembled states 的 P25-internal 與 P25-to-context 最大新增 positive-volume collision 均為 `0 mm³`，positive count 均為 `0`。

## Neutral retention vs actuated release

`latch_exit_direction()` 與 `latch_release_offset_direction()` 都是單位向量，dot product `1.11e-16`；receiver actuated travel 實測 `1.500000000 mm`，名義 engagement `1.20 mm`。

下表為每側 complete front-bar actual solid 對 complete rear-yoke actual solid；左右結果相同。Neutral 使用 `0 mm` tab travel，actuated 使用 `1.50 mm` receiver travel。

| Angle | neutral distance | neutral intersection | actuated distance | actuated intersection |
|---:|---:|---:|---:|---:|
| `0°` | `0.250000000 mm` | `0 mm³` | `0.250000000 mm` | `0 mm³` |
| `1°` | `0 mm` | `0.007610891 mm³` | `0.764589226 mm` | `0 mm³` |
| `2°` | `0 mm` | `0.235689287 mm³` | `0.800000000 mm` | `0 mm³` |
| `3°` | `0 mm` | `0.630221538 mm³` | `0.800000000 mm` | `0 mm³` |
| `4°` | `0 mm` | `0.947997331 mm³` | `0.778175321 mm` | `0 mm³` |
| `5°` | `0 mm` | `0.939566442 mm³` | `0.737799578 mm` | `0 mm³` |
| `10°` | `0.800000000 mm` | `0 mm³` | `0.800000000 mm` | `0 mm³` |
| `30°` | `0.800000000 mm` | `0 mm³` | `0.800000000 mm` | `0 mm³` |
| `60°` | `0.800000000 mm` | `0 mm³` | `0.800000000 mm` | `0 mm³` |

判讀：neutral 在 `1–5°` 的 positive-volume intersection 是 deliberate rigid retention barrier；它不是合法 release path。即使把 bar 虛擬跳到 `10°` 後又有間隙，實體剛體也不能穿過前面的 barrier。Actuated path 在全部指定角度均零互穿，且 `5°` gap `0.737800 mm >= 0.10 mm`。

代表性 rod sweep `0/10/30/60°` 亦無正體積碰撞；`60°` front pad 至 Orange clearance 為 `15.032382931 mm >= 3.00 mm`。Fully released latch center gap 為 `23.735287751 mm >= 0.60 mm`。

## STEP reopen 與 source/export parity

四個 written STEP 都以 root `.venv` 的 build123d 重新開啟。每個 solid 均 valid、closed、positive-volume；source 與 export 的 hierarchy、solids、shells、bounds 及 volume 對等。

| Artifact | children source/STEP | leaves source/STEP | solids source/STEP | shells source/STEP | volume source/STEP | max bounds delta |
|---|---:|---:|---:|---:|---:|---:|
| `PRECLAMP_END` | `14/14` | `20/20` | `21/21` | `21/21` | `24663.752672910 / 24663.752672908 mm³` | `3.0624e-12 mm` |
| `LATCHED_END` | `14/14` | `20/20` | `21/21` | `21/21` | `24663.752672910 / 24663.752672908 mm³` | `0 mm` |
| `RELEASED_CLEAR` | `14/14` | `20/20` | `21/21` | `21/21` | `24660.590318791 / 24660.590318789 mm³` | `3.0624e-12 mm` |
| exploded modules | `8/8` | `8/8` | `8/8` | `8/8` | `935.574223238 / 935.574223238 mm³` | `1.4211e-13 mm` |

STEP import 會把 label 中的 decimal punctuation 正規化（例如 `1.50` 成為 `1_50`）；除此之外 occurrence labels 對應。Released rear-yoke envelope 明確標為 `FLEX_RECEIVER_DEFLECTED_ENVELOPE_1_50mm`，其餘靜態狀態為 neutral receiver。

## Validation snapshots、render package 與 live Viewer

舊 validation PNG 為 Repair 1 bytes，已判定 stale；僅在允許的 validation namespace 內以現有 `render_validation_snapshots.py` 重新由 Repair 2 written STEP render：

```text
PYTHONDONTWRITEBYTECODE=1 uv run python \
  projects/xt60-bend-jig/cad/p25_r1_rear_loop_front_pusher_clamp/render_validation_snapshots.py
```

三張皆為 `1600 × 1200`，並已逐張人工檢視：

- `p25_r1_latched_end_validation.png`：`b2b338fbe3f7976ee8c516b11e9c07f6e06c8c931e4cf3c556dcf656c6f49a98`
- `p25_r1_released_clear_validation.png`：`dc07174b069c19e1113d5a42df3b0bc72c15569e6210349cab6a5192aec404f2`
- `p25_r1_modules_exploded_validation.png`：`e096878c9b5c7800b68c067396d810789907ee8c12671cc7baa7473de81687e9`
- render script：`0a85c445cf97d24180a911c304703208452a597ef22eac25e024d864213bdbe4`

現有四個 `__cadgen__/models/.../assembly.json` 的 internal `stepHash` 均與本 receipt 的 current STEP SHA 相同，因此未不必要地重建 package；occurrence counts 為 `20/20/20/8`，kind 均為 `assembly`。

Validator 直接只讀檢查 root 提供的 Tailscale Viewer：

- `tailscale serve status`：`https://mac-mini.duckbill-ionian.ts.net:8452` proxy 至 `127.0.0.1:3252`。
- `GET /__cad/server`：HTTP 200，`cad-viewer 0.5.0`，rootPath 為本 repository。
- 四個 exact STEP 的 `GET /__cad/artifact?file=<absolute STEP path>`：全部 `state=rendered`。
- exact latched `/?file=<absolute STEP path>`：HTTP 200。

這證明 live service 與 exact artifact readiness。CUA 當下沒有可用 browser provider，所以 validator 沒有宣稱 browser canvas 或使用者端可視性已確認；validation PNG 的人工檢視與 Viewer readiness 仍是兩個分開的證據層。

## 分開報告的 inherited／physical 問題

- inherited P20 `RELEASED_OPEN` Blue/XT60 collision：`186.980487360803 mm³`。P25 沒有修正或隱藏它，也不把它算成 P25 新增 collision。
- P20 print-kit fixture SHA drift：上述 `1 passed, 2 failed`；不是 P25 regression。
- zero-cap axial retention、雙側實際 load equalization、saddle/pad 的最終接觸形狀與列印公差仍是 print-candidate 前的風險，不由本 first-CAD PASS 解決。
- opening spring 仍只是 `UNVERIFIED` envelope；cantilever／spring required force、應變、回彈、疲勞、蠕變、材料與列印方向沒有 FEA 或 physical evidence。

## 分層狀態與 final disposition

- **CAD first-preview candidate：PASS，僅限 `a1932fb`。** Neutral retention 與 actuated release 的 geometric blocker 已關閉。
- **Written STEP：PASS。** Reopen、valid／closed／positive solids、occurrence 與 source parity 均通過。
- **Snapshots：PASS for review media。** Repair 2 bytes 已重建並人工檢視；不取代機構或物理驗證。
- **Live Viewer：service/artifact readiness PASS；browser-level visibility 未驗證。**
- **Slicer／print：未執行。**
- **Physical：未驗證。** 尤其立即彈開、flexure force/strain、holding force、軸向留置、公差、磨耗與耐久不可由本 receipt 宣稱。

**P25-VALIDATE-01 最終判定：PASS first-CAD preview for frozen Repair 2 candidate `a1932fb` only。**
