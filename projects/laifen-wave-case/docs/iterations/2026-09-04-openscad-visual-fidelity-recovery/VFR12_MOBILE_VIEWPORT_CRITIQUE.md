# VFR-12 independent mobile viewport critique

Status: **BLOCKED.** The candidate resolves the user's visible status/card complaint, produces an edge-to-edge mobile viewer, preserves a complete initial field and final-field clearance, and does not show a desktop/runtime/geometry regression. It does not resolve the user's small, uncentered action-icon complaint: the Reset camera glyph remains visibly smaller and lower than the adjacent Reset glyph despite its centered 24 x 24 CSS pseudo box.

Owner: `VFR12-C` / `/root/openscad_vfr11_mobile_critic`, independent critique role. Candidate source, tests, manifests, implementation evidence, continuity, deployment, services and geometry were read-only. This report is the sole write.

## Provenance

Project: `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`.

Iteration: `docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/`.

- Candidate manifest: `candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256`
- Candidate manifest SHA-256: `024e441289844b118d8f4fbc9a5a26cabdab6dca50507dfcbbe7b9827a18320c`
- Candidate members: 9/9 verified before critique
- Frozen input manifest: `adffc64b4e496b15a3e023c8704bb254db732c0aa62d0558994f56276e933ef4`
- Candidate CSS: `176209d8c82940c74083b229f42585f3339c892109c18f9d9ceafca6c522359d`
- Candidate focused test: `168e3bc9cc6f5d84965dd4f1ae163a1952bf7617e9c12bfed5857daf603ec708`
- Unchanged HTML/main/schema/worker: `997c2fbc...` / `98af41e1...` / `89406233...` / `fabd1535...`

The user evidence at `/tmp/codex-remote-attachments/01a06004-6842-76f1-bf1e-486590d05ac5/8B8CE7A0-DC92-43D9-9A96-0CD21F0B6A61/1-Pasted-Image-1.jpg`, SHA-256 `adaef0ff2a46229dec69a1a03de3560c74fd65cdf9c88ac8e5bd038ef6daff55`, was inspected first. It shows the rejected ready-status sentence, padded bordered viewer card, and visibly small action glyphs on the actual phone surface.

The implementer scratch files have no evidence manifest and are not members of the frozen candidate. This critique therefore treats them as implementation evidence, records the exact inspected file hashes below, and does not present their Chromium measurements as independent browser validation. The critic independently verified the frozen candidate bytes, inspected the screenshots, inspected the exact CSS/test rules, and measured rendered screenshot pixels without modifying evidence.

## Evidence steps

1. **Initial mobile surface — healthy except for the action-icon finding below.** The visible status/title are gone. The viewer begins at the top and spans the complete 390 px screenshot width without a card border, radius or outer padding. The complete Device length label and 46 px input remain visible below it.

   ![VFR-12 initial mobile implementation](../../../scratch/vfr12-mobile-implementation/mobile-initial.png)

2. **Responsive mobile/form end — layout healthy, icon defect repeated.** The 360, 390 and 430 captures show the borderless full-width viewer treatment and a final Output field above the sticky actions. The small Reset camera glyph repeats at all three widths.

   ![VFR-12 360 px implementation evidence](../../../scratch/vfr12-mobile-implementation/mobile360.png)

3. **Breakpoint — healthy.** At 700 px the mobile edge-to-edge treatment remains active; at 701 px the desktop heading, status, bordered card, 580 px canvas and text actions return.

   ![VFR-12 701 px desktop breakpoint](../../../scratch/vfr12-mobile-implementation/boundary701.png)

4. **Desktop — healthy.** The established two-column layout, heading/status, text labels and 580 px canvas remain visible without horizontal overflow.

   ![VFR-12 desktop implementation evidence](../../../scratch/vfr12-mobile-implementation/desktop.png)

## Findings

### High — Reset camera remains visibly tiny and optically low

The candidate centers a 24 x 24 pseudo-element box and sets `font-size:24px`, but that only centers the glyph's layout box. The actual `⟳` font ink remains much smaller than its neighbors. In the exact `mobile-initial.png` at 390 px width:

- Reset `↻` ink occupies 16 x 19 px and is vertically centered within 0.5 px of the button center.
- Reset camera `⟳` ink occupies only 12 x 10 px and its ink center is 3 px below the button center.

The same measured 12 x 10 px ink box and +3 px vertical offset recur in `mobile360.png` and `mobile430.png`. This matches the screenshot impression: the fourth icon is materially smaller and lower than the 24 px Reset icon beside it. The VFR-12 contract explicitly requires screenshot inspection to catch font metrics that pass box math while appearing off-center. Consequently V12-04 fails and the user's reported symptom remains.

This finding does not require visible word labels. Keep the icon-only row and meaningful DOM wording, but use a deterministic icon whose visible mark actually fills and centers within the intended 24 px slot. Recheck rendered ink or equivalent optical bounds at 360, 390 and 430 px, not only computed pseudo-element dimensions.

### Medium — responsive first-screen evidence is incomplete outside 390 px

The supplied `mobile360.png`, `mobile390.png`, `mobile430.png` and corresponding `measurements.json` rows were taken after the form was scrolled to its maximum. Their recorded first-field rectangles are far above the viewport, so they do not prove the V12-05 requirement that one complete field appears on the initial 360 x 640 and 430 x 932 screens. The screenshots are also full-page images (360 x 692, 390 x 925 and 430 x 1014), not viewport-height crops.

`mobile-initial.png` plus `initial-desktop-measurements.json` do support the 390 x 844 initial state: Device length is `y=312.4375..358.4375`. This finding identifies missing evidence for the adjacent responsive sizes, not an observed clipping defect. Independent validation should capture/query the initial 360 and 430 states before any form or page scroll.

### Low — implementation screenshots are not frozen evidence

The candidate manifest binds the implementation receipt and source/test files but no scratch screenshot, measurement JSON, built bundle or evidence inventory. This critique records their hashes to identify exactly what was inspected, but a distinct validator must build the 9-member candidate into an exclusive scratch root and bind its screenshots, measurements and built assets before formal review.

### Low — Safari and actual delivery surface remain open

The supplied browser measurements are from headless Chromium, while the complaint came from iPhone/Safari inside the private delivery surface. Browser chrome, safe areas, dynamic viewport behavior, text scaling and the exact served bundle remain untested for VFR-12. These limits do not negate the local edge-to-edge improvement, but controlled Chromium evidence cannot close V12-08.

## Requirement coverage

| User complaint or contract gate | Critique result | Evidence |
| --- | --- | --- |
| Visible title/status removed on mobile | PASS locally | Candidate uses a clipped 1 px live-region treatment; initial screenshot shows no sentence or title while text and `aria-live=polite` remain. |
| Viewer full width, edge-to-edge, borderless | PASS locally | Candidate CSS removes mobile main padding/result border/radius/padding and makes the canvas block-level width 100%; screenshot and implementer measurements show x=0..390 and height 219.4375. |
| Initial controls and one complete field | PASS at 390; evidence gap at 360/430 | At 390, Device length is fully visible and 46 px high. Initial 360/430 captures are absent. |
| Icon size and centering | **FAIL** | Pseudo boxes compute as 24 x 24, but visible Reset camera ink is 12 x 10 and centered 3 px low across 360/390/430 screenshots. |
| Sticky row does not obscure final field | PASS in implementation evidence | At 390, Output is `y=605.4375..649.4375`, actions begin at y=785, and top/center/bottom hit tests return `output_mode`; 360/430 evidence also reports passing hits. |
| No horizontal overflow | PASS in implementation evidence | 360/390/430 and 700/701 rows report `scrollWidth==clientWidth`; inspected screenshots show no lateral clipping. |
| Desktop preserved | PASS locally | At 701 and 1440 the heading/status/card/text actions return; desktop screenshot shows prior structure and canvas. |
| Runtime and geometry preserved | PASS by frozen hashes | HTML, main, schema and worker match the manifest; only CSS/test/receipt changed. No CAD/SCAD/mesh acceptance follows. |

## Inspected implementation-evidence hashes

These hashes identify the unmanifested scratch files used by this critique:

| File | SHA-256 |
| --- | --- |
| `mobile-initial.png` | `8bf518dd2fa2a415b80cf9319cf9ceee024784fb778f2b3ee8b799ff22073d02` |
| `mobile390.png` | `ed2ca62427f8d3e2227c0bcb774ec29ba8cb5f35e388693b3dad5854b34e9d3b` |
| `mobile360.png` | `40a965da89fa2c8e03ed5b4d466eda7f491295a4bcf63a4ef863a1f3667f7aa4` |
| `mobile430.png` | `6ba50bf8585d98b9a0e5faf2439a795a5909497ac7033d748d45f49d208032c6` |
| `boundary700.png` | `5a2efa09e598a853f894d12b748156b036f5ccac7511996e4ba8177de9687074` |
| `boundary701.png` | `d3ae186a582178172094c5026c2786ee3f17cfa6fce024124f88c59717de07a5` |
| `desktop.png` | `b04f3ed50536ba6f26ad3392c5c2b068c0db15095dafc64f2bf359cdce2ee39d` |
| `measurements.json` | `6bd05b901a47bdd5eb9d5403c83fba9918fd03a862476d0bf564e0a96b5cbe02` |
| `initial-desktop-measurements.json` | `5f82b7077eeff9616a904d94e63956d632b934e1216fc083ea27c0e874c14328` |

## Separate existing risks

VFR-12 is a mobile presentation candidate. It does not repair or retest the existing correctly identified late-result cancellation race, and public Diamond controls remain HOLD. It also does not establish Diamond assembled/print-layout browser acceptance, CAD/STEP/slicer acceptance or physical print acceptance. Those are separate from this icon blocker.

## Commands and evidence

Commands actually run for the decisive checks included:

```text
# cwd: projects/laifen-wave-case
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_CANDIDATE.sha256

# cwd: scratch/vfr12-mobile-implementation
shasum -a 256 mobile-initial.png mobile390.png mobile360.png mobile430.png boundary700.png boundary701.png desktop.png measurements.json initial-desktop-measurements.json
sips -g pixelWidth -g pixelHeight mobile-initial.png mobile390.png mobile360.png mobile430.png boundary700.png boundary701.png desktop.png

# cwd: repository root
/opt/homebrew/bin/rg -n -C 2 "@media|max-width:700|#status|\\.result|#viewer|::before|justify-content|align-items|padding-bottom|fieldset:last-child" projects/laifen-wave-case/preview/openscad-wasm-simulator/style.css projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py
PYTHONDONTWRITEBYTECODE=1 uv run python -B - <<'PY'
from PIL import Image
from pathlib import Path
import json
root=Path('projects/laifen-wave-case/scratch/vfr12-mobile-implementation')
m=json.loads((root/'measurements.json').read_text())
for key,file in [('mobile390','mobile-initial.png'),('mobile360','mobile360.png'),('mobile430','mobile430.png')]:
    img=Image.open(root/file).convert('RGB')
    a=m[key]['actions']; widths=[x['w'] for x in m[key]['icons']]
    x=a['x']; y=a['y']+7
    boxes=[]
    for w in widths:
        boxes.append((round(x),round(y),round(x+w),round(y+46)))
        x+=w+4
    print(key)
    for name,i in [('reset',2),('camera',3)]:
        x0,y0,x1,y1=boxes[i]; pts=[]
        for py in range(y0+4,y1-4):
            for px in range(x0+4,x1-4):
                r,g,b=img.getpixel((px,py))
                if r+g+b < 240:
                    pts.append((px,py))
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        bbox=(min(xs),min(ys),max(xs)+1,max(ys)+1)
        center=((bbox[0]+bbox[2])/2,(bbox[1]+bbox[3])/2)
        bcenter=((x0+x1)/2,(y0+y1)/2)
        print(name,{'ink_bbox':bbox,'ink_size':(bbox[2]-bbox[0],bbox[3]-bbox[1]),'ink_center_delta':(center[0]-bcenter[0],center[1]-bcenter[1]),'pixels':len(pts)})
PY
```

All referenced screenshots, including the actual-user phone evidence, were opened at original detail and visually inspected. No browser, source, test, manifest, evidence, service or deployment mutation occurred.

## Disposition

Do not advance this fingerprint to formal acceptance. Route the smallest icon-only repair for the Reset camera mark, preserving the order, action wording, 24 px slot, one-row toolbar, disabled states, touch targets and all other VFR-12 presentation gains. Refreeze the candidate, capture initial and max-scroll states at 360/390/430, bind the built bundle and screenshots in independent validation, and rerun this visual critique before formal review.
