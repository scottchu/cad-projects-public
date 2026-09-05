# VFR-12 C3 independent final validation

Status: **PASS for the complete assigned local browser gates, including the previously failing painted-icon checks.** Independent critique/formal review and private delivery remain separate. Actual iPhone/Safari acceptance is not established here.

Owner: `VFR12-V` / `/root/openscad_vfr11_mobile_validator`, independent validator. Project `/Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case`; iteration `2026-09-04-openscad-visual-fidelity-recovery`. Only this report and `scratch/vfr12-mobile-c3-validation/` were written. No source, tests, candidate manifests, continuity, deployment or CAD edits. No candidate repair; one infrastructure retry for an occupied port.

## Provenance

Candidate `candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256`, hash `2a58f483d2ba653c7e3c7de747bec8466837dd7f46ee4cd493ef9e8b61199433`: exact assignment match; all nine members verified before and after validation. Prior blocking receipt: `VFR12_MOBILE_VIEWPORT_C2_VALIDATION.md`, hash `9ebade4791521344d97e5995182e6e591ac566be8a231b1fe2e617767ce83628`.

Accepted evidence inventory: `scratch/vfr12-mobile-c3-validation/evidence.sha256`, hash `6665df989b43610e0e0ad2c141b646afd4907673d389954a11ff904d56f20404`, binding 33 files including built assets, browser scripts/JSON/logs, pixel analysis, screenshots and downloaded STL. Supplemental build inputs were independently rehashed against the prior reviewed list and remain unchanged: `build-inputs.sha256`, hash `a92147f83fd81b842ab32d9309105fc428b6a60eccd95682932c419f6820c84c`.

An initial server launch on 8775 failed with address-in-use. A browser probe had already been dispatched there; its output is explicitly untrusted, retained under `port8775-untrusted/`, excluded from the acceptance inventory and not used for any result below. The existing 8775 server was not modified. The validator launched its own server on 8779, verified its root response bytes equal the exact built index (SHA-256 `53210be5e3b21a509c449261c69a271619f6ce0475a32a6eff90af70098b30bb`), and reran all accepted browser evidence from fresh pages on `http://127.0.0.1:8779/`. This was the only infrastructure retry. The validator's 8779 server was stopped afterward, exit 0.

## Actual icon results

Real Chromium 151.0.7922.34, device scale factor 1, software WebGL, fresh initial viewport screenshots at 360×640, 390×844 and 430×932. CDP `DOM.getDocument`/`DOM.getBoxModel` measured actual pseudo-node boxes. PIL measured painted screenshot pixels inside those boxes relative to sampled adjacent button background, using a 10-channel-level difference threshold. The same method was used for C2; script and exact bounds are retained in `measure_ink.py` and `ink.json`.

| Icon | Painted bounds at all three sizes | Optical center delta x/y at 390 | Result |
|---|---|---|---|
|Generate|22×22|−0.1953125 / 0|PASS|
|Cancel|20×20|+0.40625 / 0|PASS|
|Reset|21×21|+0.5078125 /+0.5|PASS|
|Reset camera|19×19|−0.890625 /+0.5|PASS|
|Download|20×20|+0.203125 / 0|PASS|

All painted marks exceed the 18×18 minimum. Maximum optical error is 0.890625px horizontally and 0.5px vertically, below the 1px gate. Actual pseudo layout boxes remain 24×24, with maximum box-center error 0.0078125px horizontally/ 0px vertically, and every pseudo center hits its intended action.

Every pseudo computes `background-image:none`; pseudo background-color equals the action's currentColor. Generate's filled center is now RGB(255,255,255) on RGB(17,34,51), approximately 16.15:1 sampled foreground/background contrast, closing the C2 black-on-navy defect. Enabled reset/camera use navy; disabled controls retain opacity 0.46/grayscale and muted currentColor. Initial versus generated screenshot confirms Download changes from muted to enabled.

All five `-webkit-mask-image` values compute to SVG data URLs, with `-webkit-mask-size:contain` and position 50% 50%, alongside standard mask values. This proves the prefixed declarations are active in Chromium; it does not substitute for a Safari engine/device test.

Accessibility names are clean: Generate STL, Cancel, Reset, Reset camera and enabled link Download STL, without Unicode prefixes. Empty pseudo content leaves DOM wording as the name source. The SVG marks render as a star, stop square, two distinct circular-arrow variants and download arrow/tray. They now look substantial and centered in the inspected images. User comprehension of the two reset meanings remains a separate human check.

## Full viewport and state gates

Fresh initial captures occurred before form/document scrolling. All mobile result/canvas rectangles begin exactly at x0/y0, end at viewport width, and have zero border/padding/radius. Result and canvas bottoms match. Status remains a clipped absolute 1×1 live region, display:block, visibility:visible, text preserved and aria-live=polite; accessibility snapshot retains the ready paragraph while screenshots show neither visible status nor header.

| Viewport | Canvas height | First complete input y range | Final output y range at page top/form max | Clearance to actions |
|---|---:|---|---|---:|
|360×640|190|283–329|372–416|165|
|390×844|219.4375|312.4375–358.4375|605.4375–649.4375|135.5625|
|430×932|220|313–359|694–738|135|
|700×844|219.4375|312.4375–358.4375|605.4375–649.4375|135.5625|

The first labels are wholly visible above their 46px inputs; each input has 11px horizontal inset and a successful center hit. Every mobile row contains five simultaneously visible actions, all 46px high and at least 64.39px wide. Final 44px selects pass top+1/center/bottom−1 hit tests with page scrollY 0 and form at maximum. All six widths have document scrollWidth=clientWidth, with no horizontal overflow.

At 701px the desktop heading/status/card and 580px canvas return; at 1440×1200 the established desktop layout, visible 16px action labels and 580px canvas remain. Built CSS preceding `@media` is byte-identical to C2's desktop/global prefix. HTML/main/schema/worker remain unchanged within the verified candidate; seven focused tests pass.

At 390×844, document scroll 80/form scroll 500 leave the viewer sticky at x0/y0 and actions visible. Invalid device length 0 shows a readable actionable role=alert/aria-live=assertive toast and focuses Dismiss. Dismiss hides it and restores Generate focus. Smooth generation completes `04109b17a9e3`, visibly renders the model, keeps status clipped and enables Download. The real download succeeds; subsequent edit to 209 makes the stale warning visible, removes href and sets aria-disabled=true. All five surface/Diamond fields remain disabled.

Saved download `smooth-download.stl`: 12,160,971 bytes; hash `b1b9db18e21cafed5237afb90e57831b72246c6ac2e4b4c88f736738fd0cf169`; suggested filename `laifen-04109b17a9e394ae9bdd97d43ca4af573c48b32ecbfcff85507dc3650f380d3e.stl`; failure=null. This verifies the download flow, not mesh/geometry acceptance.

Browser geometry, masks and accessible snapshots are in `viewport.json`; state checks in `states.json`; assertion outcomes and sampled contrast in `gates.json`. Accepted runs have no page errors, console errors or failed requests. Only software-WebGL ReadPixels performance warnings are recorded.

## Commands and visual evidence

Cwd `/Users/scottchu/.codex/worktrees/4f8c/design-projects` unless marked project cwd.

```text
# project cwd, before and after work
shasum -a 256 docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256
shasum -a 256 -c docs/iterations/2026-09-04-openscad-visual-fidelity-recovery/candidate/VFR12_MOBILE_VIEWPORT_C3_CANDIDATE.sha256
# repository cwd
uv run pytest projects/laifen-wave-case/tests/test_openscad_wasm_simulator.py -q
npm run build:openscad-simulator --workspace projects/laifen-wave-case -- --outDir /Users/scottchu/.codex/worktrees/4f8c/design-projects/projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/dist
uv run python -m http.server 8779 --bind 127.0.0.1 --directory projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/dist
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/viewport.py > projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/viewport-output.log 2>&1
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/measure_ink.py > projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/ink-output.log
uv run python projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/states.py > projects/laifen-wave-case/scratch/vfr12-mobile-c3-validation/states-output.log 2>&1
```

Seven tests passed. Vite 6.4.3 built eleven modules in 517ms; only the standard >500kB chunk advisory. Accepted commands exited 0. The initial failed server command was identical except port 8775, exited 1 with address-in-use; its discarded probe is documented above. An inline `uv run python` verified 8779 root bytes before the accepted viewport command. Another inline Python check asserted all responsive/paint/state-observation prerequisites against saved JSON, compared desktop CSS and computed contrast; its outcomes are saved in `gates.json`. Supplemental input hashing and evidence inventory generation used root-uv Python.

The validator opened and visually inspected fresh initial 360/390/430/700/701/1440 screenshots; final 360/390/430 screenshots; desktop-actions; mobile-generated; mobile-toast; mobile-stale; mobile-scrolled. These 14 inspected PNGs and the additional 700-final capture are bound in the accepted inventory. No untrusted 8775 PNG is cited as acceptance evidence.

## Disposition and limits

The C2 color, painted-size and optical-center blockers are resolved by C3's actual browser/pixel evidence. Advance this exact candidate to independent critique/formal review; this validator performed no repair and grants no deployment authority.

Private-route bytes, actual iPhone/Safari, dynamic browser chrome/safe areas, keyboard, zoom/text scaling and native screen-reader behavior remain untested here. Computed `-webkit-mask` in Chromium is not Safari acceptance. Existing cancellation-race/Diamond HOLD, CAD, mesh/slicer and physical acceptance remain separate. No broad accessibility certification or user icon-comprehension result is claimed.

Final evidence verification: `shasum -a 256 -c evidence.sha256` from the C3 scratch root passed all 33 accepted members.
