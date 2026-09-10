# Drone v3 — design system & tail mount vision

This folder is the **v3 design line** for FPV frame-adjacent printed parts. Today it holds the **SMA dual-boss plate** (`sma/`); the intent is to grow toward an **integrated tail / stack mount** (video antennas, optional GPS, RC RX antenna) with explicit **FPV configuration** and **3D-print / DFM** layers.

This document is the **design README** for v3: product intent, parameter coupling, build phases, and how we hook into the repo **thinking system** (feedback, reflection, diffuse).

---

## 🎯 Primary job (one sentence)

**Hold video RX antennas (and optionally GPS + RC RX hardware) in a repeatable aim and footprint, while mating real standoff/carbon geometry and surviving vibration, torque, and crash loads—without impossible or unprintable coupled dimensions.**

---

## 🧭 Systems thinking (how we work)

v3 designs follow the repo rules:

| Layer | Where it lives |
|--------|----------------|
| **Domain checklist** | `.cursor/rules/3d-print-systems-thinking.mdc` — boundaries, interfaces, constraints, leverage points |
| **Meta loops** | `.cursor/rules/3d-thinking-system.mdc` — feedback → reflection → diffuse |
| **Capability honesty** | `.cursor/rules/stop-on-capability-gap.mdc` — no guessing; document missing data or tools |
| **Digital verify** | `openscad-preview` skill — preview, multi_view, cross_section, measure |
| **Physical verify** | `documents/system-log/raw/prints.md` (+ `Ref:`) |
| **Digital log** | `documents/system-log/raw/verification.md` |
| **Diffuse / ideas** | `documents/system-log/raw/diffuse.md` |
| **Material notes** | `documents/filaments/` |

**Habit for v3:** Before calling an interface “done,” tie it to **preview/measure or a test print**, or record an explicit **capability gap** (missing SKU dims, bend radius, etc.).

---

## 🖼 Reference intent (integrated mount)

Target is a **single integrated** printed assembly (or a small multi-part set) analogous to a “tail mount” that can combine:

| Zone | Function |
|------|-----------|
| **Top / forward deck** | Video RX: **SMA bulkhead(s)** *or* a **holder** (e.g. dual-stick / DJI O4 Pro style), **1 or 2** antennas, parametric **aim** and **spacing** |
| **Upper structure** | **Optional GPS** cradle / pocket / strap lugs |
| **Bottom / aft tab** | **RC RX** antenna retention (**TBS Crossfire** vs **ELRS** T-style / linear)—often on a **tapered** region (thick near standoffs → thin at tab) |

**Current code:** `sma/plate.scad` is the **dual-SMA aimed boss** slice of that story; it does not yet model frame cheeks, GPS, RC, or pigtail tunnels.

---

## 🧩 Parameter layers (FPV vs print)

Split knobs so **intent** stays readable and **printability** can clamp or grow geometry without hiding tradeoffs.

### FPV / integration configuration (intent)

- **Frame / sandwich:** standoff **hole pattern** (spacing, count), **hole diameter or slot shape**, **plate thickness**, **stack height** (distance between inner faces of carbon—or equivalent standoff length), **cheek wrap** / overlap past carbon edge (separate from raw hole spacing).
- **Video path:** mode enum — e.g. `sma_dual`, `sma_single`, `dji_dual` (names TBD); **count** (1–2); **aim** (degrees or normal vectors on consistent axes); **center-to-center gap** between video antennas.
- **GPS:** on/off; pocket **L×W×depth**; optional insert / screw pattern when known.
- **RC RX:** type enum — **Crossfire** vs **ELRS** (retention geometry differs); stem / slot dimensions from hardware or measured coupons.
- **Routing / envelope (first-class, not optional forever):** **pigtail / u.FL path** (entry angle, tunnel ID, straight run before bend); **prop / motor clearance** (or a single rear clearance radius); **fastener model** (M2/M3, head type, threaded standoff vs through-bolt).

### 3D printing / DFM configuration (floors & guards)

Functional params define **targets**; DFM params define **floors** (and optional ceilings):

- `min_wall`, `min_floor` after pockets, `min_boss_od` around holes, `min_thickness_after_taper`
- Optional: `max_overhang_deg` without support, `max_bridge_mm` you are willing to rely on
- **Assertions:** fail when geometry is impossible; **`echo("[DFM] …")`** or preview-only cues when tight but valid

**Rule:** Expose **asserts** when FPV intent violates DFM floors—don’t silently shrink walls into failure.

---

## 🔗 Coupling map (why one slider moves three things)

| Driver | What it constrains |
|--------|---------------------|
| **Standoff gap / footprint** | Max width at the **thick** root; limits **RC tab** width and **hole-to-edge** distance at the **thin** end → may force **shorter cantilever**, **inward** RC placement, or **round → slot** holes |
| **Stack height** | Cheek depth, **SMA thread + nut stack**, room for **GPS pedestal** and **internal routing** |
| **Video mode (SMA vs sticks)** | Different **bulk**, **depth**, **side clearance**—treat as **module swap**, not only a boolean on one hull |
| **Aim angles** | **Pigtail bend radius** and internal volume; can steal space from GPS or RC unless **VRX block** is a submodule with its own pivot |
| **Material choice** | **TPU** vs **rigid** for torque, snap fits, and RC flex—may imply **hybrid** (rigid core + TPU tab) |

**Implementation direction:** derive coupled values **one way** (frame + spec → available thickness at tab, min RC pocket, etc.); avoid independent sliders that can contradict each other without warning.

---

## 📁 Target OpenSCAD layout (not all exist yet)

| File / module | Role |
|---------------|------|
| **`spec.scad`** (per subsystem or shared) | Hardware constants (SMA, GPS, RX envelopes) + shared **DFM floors** |
| **`frame/frame.scad`** | Phase 1 stub: standoff hole pair + slab footprint (replace with real cheeks / stack) |
| **`video_sma_*.scad`** | Evolve from current `sma/plate.scad` / `boss.scad` — dual/single SMA, aim math |
| **`video_dji_*.scad`** (future) | Cradle / screw pattern from measured hardware |
| **`gps/gps.scad`** | Phase 4 stub: `GPS_Cradle_Cut()` pocket module for `difference()` on parent solid |
| **`rx.scad`** (future) | Crossfire vs ELRS retention; sized from **thinnest allowed** section |
| **`tail_mount/tail_mount.scad`** | **Stub orchestrator** — frame + optional GPS preview; wire-up to `SMA_Plate()` TBD |

**Current reality:** `sma/` is the mature slice; **`frame/frame.scad`** (phase 1 stub), **`gps/gps.scad`** (phase 4 stub), **`tail_mount/tail_mount.scad`** (layout stub) exist. **`rx/`**, **`video_dji_*`**, and full assembly booleans are still future work.

---

## 📶 Phased build order (reduce rework)

1. **Frame shell only** — holes, cheeks, stack height; validate **carbon fit**, **screw torque**, **clamshell** stability (no antennas).
2. **Single video path** — one SMA + **routing tunnel**; validate **pigtail bend** and **prop clearance**.
3. **Video variants** — dual SMA vs DJI-style as **swap modules** behind one interface to the shell.
4. **GPS** — optional block with its own base width params.
5. **RC tab** — design at **minimum** thickness region; **print coupon** at that section before full integration.

**Test parts:** Keep `part="test"` (or equivalent) **per risk** — spacing, hex fit, thinnest tab, etc. (see `sma/plate.scad` test mode as a pattern).

---

## 📋 Physical data to collect (capability gaps to close)

Without these, parametric angles are exploratory only—two common failure modes are **wrong stack / thread length** and **wrong standoff pattern**.

- Standoff **height(s)** front vs rear if they differ  
- Carbon **hole centers**, **diameters**, clearance to **plate edges**  
- **SMA bulkhead** SKU: shoulder, hex, **thread length**, coax **minimum bend radius** after install  
- **DJI / stick antenna** (if used): footprint, screws, clearance when tilted  
- **GPS module** dimensions, hard vs foam mount, inserts if any  
- **RC antenna** hardware: T vs linear, stem diameter, retention method  
- **Printer reality** for chosen material: measured **min reliable wall** on your machine (coupon beats generic tables)

When data is missing: **stop** per capability gap—document what measurement or datasheet unlocks the next commit.

---

## 🤖 Cursor subagents (optional delegation)

Project agents in `.cursor/agents/` can review v3 work in focused voices:

- **`fpv-drone-design-expert`** — integration, vibration, routing, prop envelope, torque  
- **`fdm-printing-expert`** — orientation, materials, slicer, coupons  
- **`solid-modeling-expert`** — modules, DFM, asserts, coupling in OpenSCAD  

Invoke explicitly when you want that lens (e.g. “review `sma/plate.scad` as fdm-printing-expert”).

---

## 🔗 Related paths in this repo

| Path | Notes |
|------|--------|
| `design/drone/src/v3/sma/` | SMA boss, dual plate, `spec.scad` |
| `design/drone/src/v3/frame/` | Frame / standoff stub (`frame.scad`) |
| `design/drone/src/v3/gps/` | GPS pocket stub (`gps.scad`) |
| `design/drone/src/v3/tail_mount/` | Assembly stub (`tail_mount.scad`) |
| `documents/filaments/` | Material behavior notes |
| `documents/system-log/` | Feedback / reflection / diffuse |
| `design-locks/` | Validated dimensions when you promote a fit to a contract |

---

## ✅ Quick checklist — v3 feature or refactor “done”?

- [ ] **Purpose** stated in one sentence; **interfaces** listed with critical dims or clearance strategy  
- [ ] **FPV vs DFM** params separated; **coupling** documented or derived (not hidden)  
- [ ] **Verification:** preview / measure / print log entry, or **documented gap**  
- [ ] **Phased risk** reduced: frame before antennas, coupons before full merge  

---

*Last aligned with repo thinking-system rules and multi-agent design review (tail mount vision + `sma/plate.scad` feedback). Update this README when v3 file layout or parameter contracts change materially.*
