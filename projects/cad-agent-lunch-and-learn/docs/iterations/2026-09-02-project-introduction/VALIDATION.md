# V5 focused independent validation

Status: **FAIL, repair required** for the initial candidate. Owner `/root/intro_validation`, independent of I5. No authoritative source or artifact was edited by V5.

Verified before and after capture: HTML `2fa49a591e721a53051888e98b2562aaa8cba4b06d4f23ecb0dac8570f86790c`; CANDIDATE.sha256 `c7eb0b08ead8fb5b4cefd8bf1fe347dce9dc22c53abeb9278efe6b38c111e4f1` and all 9 entries; FROZEN_INPUTS.sha256 `66b2da24389cde4b5281ec74643e9b3e2424894d4fbd614f6f63ba66a32a2b78` and all 9 entries. Pristine baseline HTML independently verified as `021a0510235ac59b6e66c687f0041a2294925a16fd12814a70748130ac7e1280`.

Nesting-aware preservation checks pass: exactly 22 outer slide sections; slides 1, 2, 6–9 and 11–22 are byte-identical; former slides 3 and 4 equal new slides 4 and 5 after changing only their outer wrapper IDs and page counters. Their desktop, compact, mobile and PDF pixels retain the scoped rod-test and count-card styles. Mobile rod-test content remains readable by vertical scrolling.

Correction to I5's raw-script statement: the first script is not byte-identical. It contains one added S10 article in its source-drawer HTML string. Removing only that S10 article restores exact identity; the second simulator script is byte-identical. Executable behavior is preserved. Current script hashes are `656f308959574d87fd40e3531bb569c845e77104211a0f1c02eed3ab18ec7ea4` and `83807e30a7253078715001614dda38e7ef74600b70660eee37e3cff28571fd99`. No navigation/simulator rerun is needed for this data-only change. The contract-after-edit procedural miss remains recorded; independently verified preservation does not erase it.

Blocking findings:

- P2: slide 3 uses `object-fit: cover`, cropping the green and blue outer CAD plates at 855×882, 390×844 and in PDF page 3. The desktop 1280×800 view is complete. Preserve the complete CAD concept image at every required size.
- P2: slide 10 at 390×844 overlaps `hour / minute / second pieces` and `light → shadow plane`, obscuring the latter label. Its purpose, H/M/S map and conceptual-layout qualification are otherwise present and readable; desktop, compact and PDF are readable.

Evidence: `/tmp/cad-agent-intro-validation/report.json`; `{1280x800,855x882,390x844}-slide-{3,4,5,10}.png`; `390x844-slide-4-bottom.png`; `deck-print.pdf`; `print-{3,4,5,10}.png`; `print-text.txt`. All 12 viewport captures plus the scrolling continuation and four PDF pages were inspected. PDFKit confirmed exactly 22 pages, each 960×540 pt. No page has horizontal document overflow.

Commands: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-agent-intro-validation/validate.mjs` and `swift /tmp/cad-agent-intro-validation/pdf-inspect.swift /tmp/cad-agent-intro-validation`. The initial harness stopped on the overbroad raw-script-equality assumption; a focused correction isolates the declared S10 article and the rerun passed deterministic checks. The first dependent PDF attempt failed because the harness had not yet produced a PDF; the completed rerun passed. Existing build/check evidence is I5's 22-slide build and 5/5 check, not a new V5 execution. No dependencies, tests, CAD, Git, hosting, printer or other project files changed.

REQ-018 purpose-before-mechanics and sequence pass. Visual whole-image and label-readability gates remain open. Next: I5 repairs only these two layout defects, freezes a new candidate, then V5 reruns the affected captures and preservation gates; C5 and R5 must use the new fingerprint.
