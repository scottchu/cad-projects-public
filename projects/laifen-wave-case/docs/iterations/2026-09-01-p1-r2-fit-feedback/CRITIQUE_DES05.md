# CRI-05 affected numeric recovery critique

Owner `/root/preview_critique`, independent critic; **PASS within the DES-05 affected scope**. Exact candidate `inputs/des05-candidate.sha256`, SHA-256 `f0fe32796fcfae64591565b2f48983325b2c7d407e6152cf2272c3e9536eb788`; all 19 declared entries verified before and after the run. Baseline `d0aab1ff21a0cd2e5790c9800fcec7cfec2bfc3c`. This receipt supersedes C04-01's disposition for this candidate only; the failed historical receipt remains intact.

## Findings and coverage

- **C04-01 resolved.** In one initialized DOM-style harness at each actual content width 360/736 px, the default section renders finite numeric SVG attributes. Changing only D to `1.7e308` yields the existing finite-values error and clears all five regions: section, state, gaps, targets and dimensions. No `NaN`/`Infinity` SVG remains. Restoring only D29 clears the error, restores ordinary readouts and produces byte-identical default SVG. The independent stub couples textContent/innerHTML storage so clearing text through innerHTML is measured correctly.
- Source review confirms the screen guard executes before SVG writes and `update` routes render failure through the shared clearing path before derived readout writes. The guard covers the failing `D*scale` and device X calculations; the numeric correction does not cap D, edit input values, or change fit claims.
- Existing independent emitted-coordinate probes remain passing: ID spans30/31 under D29/30/31 and L140/208/400 at both widths; z137/z132 leader separation5; exterior leader endpoints beyond x17.9; decimal slack0.1/5.1 at q0/0.5/1; prior L1e308/blank/C137 invalid clearing. The repository suite additionally retains external-stop/text-anchor and contact-warning checks.
- No new blocker or material finding within this affected scope. Browser font/layout and real DOM evidence remain the separate validator's scope. This emitted-SVG/source critique grants no CAD, exported-artifact/slicer, or physical fit acceptance and does not assess the concurrent R3 architecture.

## Exact commands and results

Commands run from repository root, `login=false`:

```sh
shasum -a 256 projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-candidate.sha256
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-candidate.sha256
node --test projects/laifen-wave-case/tests/test_measurement_gate.mjs
node projects/laifen-wave-case/scratch/width-critique/probe-des05.mjs
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-01-p1-r2-fit-feedback/inputs/des05-candidate.sha256
```

Results: fingerprint matches; all19 entries OK before/after; repository suite9/9 pass; independent probe exit0 with ordinary geometry/decimal/clearing PASS and exact DES05 default/extreme-D/restore PASS at360/736. Extreme-D output reports the prescribed error and `hasNonfinite:false`. No EMFILE occurred.

Changed paths: this receipt and `scratch/width-critique/probe-des05.mjs` only. No source, test, dependency, runtime, coupon or R3 edits. This was the one authorized affected critique attempt. Next action: join distinct validator and formal-review receipts on this exact fingerprint before publication; retain all physical acceptance gaps.

## Final label-only delta critique

Same independent critic `/root/preview_critique`; **PASS for the separately authorized label-only delta**, candidate `inputs/des05-repair-candidate.sha256`, SHA-256 `9f1fdb44f7b350f7ca903c37ca2383ba195dd2f7235bbe69d2b1596f86ae4f61`. All19 entries verified before and after this narrow check.

Compared the entire live source byte-for-byte against `inputs/des05-pre-repair-source.html` with Node strict assertions. The only change is upper-ID text from `<text x="${cx}" y="64" text-anchor="middle">上段參考 ID 31</text>` to `<text x="${label}" y="40">上段參考 ID 31</text>`. Its dimension span remains `M ${ul} 48 H ${ur}`. All other source bytes, including C04-01 guards, arithmetic, fixed bores, leaders and clearing behavior, are unchanged. Moving this label to the already external label column preserves the nominal dimension geometry. No new finding; actual rendered label visibility remains the distinct validator's evidence.

Exact checks: `shasum -a 256` and `shasum -a 256 -c` against the repair manifest above (19/19 OK); Node `assert.equal(after, before.replace(oldText,newText))` and `assert.ok(after.includes('data-geometry="upper-id-span" d="M ${ul} 48 H ${ur}"'))` (exit0). The manifest verification was repeated after appending this receipt (19/19 OK). No broad tests rerun. This scoped continuation changed only this receipt. Join the final validator receipt and formal review on the repair fingerprint; acceptance boundaries above remain unchanged.
