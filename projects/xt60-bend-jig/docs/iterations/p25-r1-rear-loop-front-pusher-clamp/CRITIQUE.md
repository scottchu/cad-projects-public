# P25-CRITIC-01 Repair 2 final rerun

日期：`2026-09-05`
角色：`P25-CRITIC-01`（獨立 mechanical critic；未參與 Repair 2 實作）
唯一候選 commit：`a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`
候選 manifest file SHA-256：`88fdcd25585c35277d66a769b5c35208f8e5b8c7534d93efdbcb57493638a845`
判定範圍：**只限 first-CAD geometric preview；不代表列印、材料、手感或物理驗收**

本文件只 join frozen Repair 2 candidate `a1932fb`。`7354f85` 與 `7287e69` 不屬於本次 authority chain，其舊結論亦不得與本候選混用。

## 結論

**PASS — first-CAD preview only。**

Repair 2 已把 latch 分成兩條可區分的實體幾何路徑：neutral receiver 在未按 tab 時遇到 positive barrier；receiver 沿指定方向位移 `1.50 mm` 後，front bar 才能無碰撞旋開。原本 Repair 1 的「正向自由退出、實際沒有鎖住」blocker 已關閉。

這個 PASS 只確認幾何拓撲與 frozen preview gates：三支桿仍由使用者手動推到 END，兩側 removable clamp 才接手；rear yoke 同時承托 Blue＋Green，front pad 只碰 Orange，hinge／latch 形成可保持、可解扣的幾何閉環。Spring 仍只是誠實標示的 `UNVERIFIED` envelope；立即彈開、按壓力、flexure 應變、holding force 與耐久均未證明。

## Frozen candidate 與 provenance

- `git rev-parse --verify a1932fb^{commit}`：`a1932fb19ffeb6d584153d1c201ebe24b2e06d6a`；HEAD 正位於該 commit。
- `shasum -a 256 CANDIDATE_MANIFEST.sha256`：與指定的 `88fdcd...a845` 完全相同。
- 從 repository root 執行 manifest check：`13/13 OK`，包含 BRIEF、DESIGN、TASK_DAG、source、tests、四個 STEP generator 與四個 STEP。
- `a1932fb^..a1932fb` 只改 P25 source、test、STEP、manifest 與 implementation receipt；P20、P24、rod/rail/path authority 與 continuity 均未改。
- `git diff --check a1932fb^..a1932fb --` 限定 source、tests、IMPLEMENTATION、manifest：PASS。

## P25-C01b — CLOSED — neutral retention 與 actuated release

### Locked `0°`

- complete front bar 對 complete neutral rear yoke：distance `0.250000 mm`、intersection `0 mm³`；locked assembly 沒有非法互穿。
- `latch_hook_engagement` 為 `1.20 mm`；我另以 actual retention-tooth solid 的 vertices 投影到 receiver exit direction，量得 tooth 實際投影寬度 `1.200000000000001 mm`，不是只讀參數值。
- `0.25 mm` 是 receiver/hook running clearance，不是 preload。幾何上保留約 `0.9°` take-up 後才承受 opening load；因此本結果證明 positive retention，但不證明實體 locked 手感沒有鬆量。

### 未按 tab：neutral no-tab path

左右結果在數值精度內鏡像一致：

| opening angle | distance | left intersection | right intersection | disposition |
|---:|---:|---:|---:|---|
| `1°` | `0 mm` | `0.007611 mm³` | `0.007611 mm³` | deliberate barrier |
| `2°` | `0 mm` | `0.235689 mm³` | `0.235689 mm³` | deliberate barrier |
| `3°` | `0 mm` | `0.630222 mm³` | `0.630222 mm³` | deliberate barrier |
| `4°` | `0 mm` | `0.947997 mm³` | `0.947997 mm³` | deliberate barrier |
| `5°` | `0 mm` | `0.939566 mm³` | `0.939566 mm³` | deliberate barrier |

額外以 `0.1°` 間距掃描 `0.1–5.0°`，兩側第一個 positive-volume barrier 均出現在約 `0.9°`（`0.001524 mm³`）。這些正交集代表 rigid front bar 不可能在未使 receiver flex 的情況下穿越 tooth；它是保留機制的阻擋證據，不是合法 motion path 的 accidental collision。

### 按下 tab：receiver travel `1.50 mm`

- release offset 是與 exit direction 垂直的單位向量；neutral 到 actuated receiver center 的距離實測為 `1.500000 mm`。
- 我以 actual complete front bar 對 actuated complete rear yoke，左右各用 `0.5°` 間距獨立掃描 `1–60°`：最大 intersection `0 mm³`。
- 全 sweep 最小 distance：left `0.718295 mm`、right `0.718295 mm`。
- `5°`：兩側 distance `0.737800 mm`、intersection `0 mm³`，超過要求的 `0.10 mm`。
- `60°`：兩側 distance `0.800000 mm`、intersection `0 mm³`；latch nominal release gap `23.735288 mm`。

因此「未按不能自由退出；按下 `1.50 mm` 後才可由 `1–60°` 無碰撞釋放」的兩路 gate PASS。

## User force topology 與 closed force loop

已核對 user-approved visualization、BRIEF、DESIGN 與 candidate source：

- 使用者動作仍是大拇指把 Orange 往下推，食指＋中指把 Blue、Green 從後往前推；三支桿都是 manual inputs。
- P25 的 clamp state 不改任何 rod center，而是直接沿用 P20 `role,u -> PointYZ`，只在 `u=1` END state 接手。
- locked actual-solid contacts（左右一致）：
  - rear-yoke/Blue：distance 約 `0`、intersection `0 mm³`；
  - rear-yoke/Green：distance 約 `0`、intersection `0 mm³`；
  - front-bar/Orange：distance 約 `0`、intersection `0 mm³`；
  - front-bar/Blue `2.100000 mm`、front-bar/Green `1.229017 mm`、rear-yoke/Orange `1.317644 mm`，皆為零互穿。
- 因此 nominal reaction chain 是 `Orange -> Orange pad -> front bar -> hinge + retained latch -> rear yoke -> Blue + Green`；clamp 不驅動三支桿，只在使用者完成 END 後保持。

**Disposition：PASS（geometric topology）。** `0.25 mm` latch clearance、接觸變形、摩擦與 preload 尚未物理量測，故不能把本 PASS 解讀為 holding-force acceptance。

## 左右鏡像、tilt 與 collision

- `PRECLAMP_END`、`LATCHED_END`、`RELEASED_CLEAR` 的 corresponding left/right part bounds 完全 X 鏡像，YZ bounds 與 rod contacts 相同。
- 每側四個 P25 parts 均各為一個 valid、positive-volume closed solid；兩側 latch sweeps 數值一致。
- 三個狀態的 P25-P25 及 P25-to-P20 context 最大 positive-volume intersection 均為 `0 mm³`。
- released front pad 對 Orange clearance 為 `15.032383 mm`，遠大於 `3.00 mm` gate。
- spring envelope 對 P25 parts 與三支桿的最大 intersection 均為 `0 mm³`。

**Disposition：PASS（nominal geometry）。** 兩個 mirrored modules 沒有幾何造成的單側 rod tilt；但兩個獨立 latch 沒有 equalizer，列印公差、扣合先後、實際力分配與 rod tilt 仍是 physical unknown。

## Rod、forbidden architecture 與裝卸

- 三支 purchased rods 保持 exact `OD4.00 × 50.00 mm`、端點 `X=±25.00 mm`；沒有把 rod 改成 `60 mm`。
- 每側 module axial stack 為 `|X|=21.30..24.50 mm`，距 rod tip 保留 `0.50 mm`；兩側 fit 在既有 50 mm ends 內。
- occurrence census：三支 rods、兩個 rear yokes、兩個 front bars、兩個 hinge envelopes、兩個 spring envelopes；cap 為零，沒有 screw cassette、pressure plate 或 floating shoe。
- rear saddles 有向外開口，front bar 在 PRECLAMP/RELEASED 旋開 `60°`；由 rod ends 上方放入與取下在幾何上有可行路徑，不需改 rod、plate、XT60 或 P20 rail/path。

**Disposition：PASS（installation geometry）。** 目前仍沒有 zero-cap 的 positive axial detent/end stop；模組沿 X 軸的實體留置依賴閉合摩擦與公差，這是 print candidate 前必須量測或修正的 high physical risk，但不阻擋這次 first-CAD topology preview。

## Latch／hinge realism 與 remaining material findings

### P25-C02 — PASS geometry／HIGH physical unknown — flex latch

- neutral rear yoke 是單一 printable solid；receiver、release tab 與 cantilever tongue 連成同一 solid，不再是假想的自由位移零件。
- actuated state 明確標作 `FLEX_RECEIVER_DEFLECTED_ENVELOPE_1.50mm`；它沒有冒充已完成材料驗證。
- neutral tongue root-to-receiver 長約 `11.276 mm`，指定 tip travel `1.50 mm`。required force、局部 strain、snap-back、fatigue、creep、print orientation 與材料都沒有 FEA 或物理證據。
- OD2 hinge 仍是 hardware envelope；running clearance 與 `0–60°` actual-solid path 在 nominal CAD 中成立，但 pin fit、磨耗與耐久未驗證。

這足以作 first-CAD mechanism preview，但不構成 printable latch approval。

### P25-C03 — HIGH／NON-BLOCKING FOR TOPOLOGY PREVIEW — saddle/pad fidelity

- `rear_saddle_wrap_angle=120°` 與 `orange_pad_wrap_angle=70°` 仍未控制 source geometry。
- rear yoke 的 nominal zero-distance contact仍由局部 tangent support 建立；Orange pad 仍是 flat box，不是 DESIGN 文字所稱的 70° concave pad。

Contact identities 與閉環方向成立，所以不推翻本次 first-CAD topology PASS；但在進入 print candidate 前，必須讓 source 與 DESIGN 一致，或正式縮小 DESIGN claim，並重新檢查鬆量、壓痕與 holding force。

### P25-C04 — BASELINE LIMIT

P20 既有 OPEN Blue/XT60 collision 仍存在且由 test 明確揭露；Repair 2 沒有修改或隱藏它。這是 inherited baseline blocker，不是 P25 clamp 新 collision，也不屬於本 candidate 的修復範圍。

## STEP 與 visual/readability

- 三個組裝 STEP 重開後均為 `21` solids；exploded STEP 為 `8` solids；全部 valid、positive-volume。
- source/STEP bounds 最大差 `3.0625e-12 mm`，solid-volume sum 差絕對值小於 `2.0e-9 mm³`。
- user-approved 2D visualization 清楚表達三指手勢及 rear Blue＋Green／front Orange 的接觸身份，與 candidate topology 一致。
- 工作樹中的 Repair 2 PNG 不在 frozen manifest，故只作視覺觀察、沒有被 join 為 candidate authority。它們可看出左右模組、locked 與 actuated+60° 狀態，但透明 context 太密，latch tooth／receiver 細節不夠清楚。
- Spring 在 source/STEP part label 中明確為 `opening_spring_envelope_<side>_UNVERIFIED`；然而目前靜態 PNG 沒有直接寫出「只預留空間、立即彈開未證明」。正式 user-facing preview 應加此句，並提供 latch 局部剖面或 close-up。

**Disposition：PASS for geometry，visual communication 仍需改善。** 本結論沒有把 spring envelope 當成自動彈開的功能證明。

## Requirement disposition for `a1932fb`

| Gate | Repair 2 disposition |
|---|---|
| neutral no-tab `1–5°` 遇到 deliberate barrier | **PASS**：五個角度均有 positive solid intersection |
| no-tab 不能自由退出 | **PASS**：dense sweep 約 `0.9°` 開始遇到 barrier |
| actuated receiver travel | **PASS**：exact `1.50 mm` |
| actuated `1–60°` path | **PASS**：`0.5°` dense sweep 最大 intersection `0 mm³` |
| actuated `5°` gap `>=0.10 mm` | **PASS**：`0.737800 mm` |
| locked `0°` engagement `1.20 mm` | **PASS**：actual tooth exit-projection `1.200000 mm` |
| locked `0°` interpenetration | **PASS**：`0 mm³`；bar/yoke gap `0.250000 mm` |
| user force topology／all rods manual | **PASS** |
| rear yoke 同時 Blue＋Green | **PASS** |
| front pad 只碰 Orange | **PASS** |
| independent closed loop after END | **PASS（nominal geometry；preload/force untested）** |
| mirrored modules／no nominal tilt | **PASS（geometry only）** |
| exact OD4×50／fit on 50 mm ends | **PASS** |
| zero cap／zero screw cassette／path unchanged | **PASS** |
| install/remove path | **PASS geometry；axial retention unproven** |
| spring honestly labeled unproven | **PASS**：`UNVERIFIED` envelope；physical opening remains unproven |
| STEP validity／source parity | **PASS** |
| physical holding、spring force、flexure strain、durability | **NOT TESTED** |

## Final critic decision

**PASS first-CAD preview for frozen candidate `a1932fb` only。**

Repair 2 關閉了最後的 geometric latch blocker：neutral path 有 positive retention，指定 `1.50 mm` actuation 後才取得完整、無碰撞的 release sweep；所有 user topology 與 frozen invariants 保持。下一階段仍不得直接宣稱可列印或可用，必須另做 latch flexure、spring、axial retention、saddle/pad fidelity、雙側負載與實體 fit/holding 驗證。
