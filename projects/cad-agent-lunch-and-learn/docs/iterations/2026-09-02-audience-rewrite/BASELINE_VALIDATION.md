# Q22V-a baseline capture receipt

Status: **capture complete; audience acceptance remains open**. Owner `/root/intro_validation`. This is the repaired introduction candidate supplied as input to the whole-deck audit; it is not a globally accepted presentation. Q22V-a does not replace Q22C-a's slide-by-slide critique or final validation of the rewrite.

Verified before and after browser capture: BASELINE.sha256 `95ef49d27a10153fc843ba34c0aa783eec1d9964d7606e6c89891d7e7629a146`, with all 7 path/content entries matching. HTML `f386aa4cd4c2fb90cf43c85a7e11139a0d15f7f07a28d4e3be37ff2b4144e57c`; builder `a7aac22de0da815657d9d40648def4ab7bb327045fee2a4c6c829fe6c6dad5a8`; simulator `eb78fb051d0b6d59b641f3b84f739108a7d6eb3ffdc96cd5da4d33c7aa65d2cc`. The baseline already includes the S10 source-drawer article and the two introduction layout repairs. No claim of raw script identity to the earlier pre-introduction deck is made.

All 22 slides were individually captured at 1280×800. Extra captures cover slides 6–8 at 1178×820, slides 3 and 10 at 855×882, and slides 3, 6, 7, 8 and 10 at 390×844, with bottom-scroll continuations wherever the document exceeds viewport height. All 32 primary captures have document width within the viewport. This geometric result alone does not establish readable diagrams or understandable explanations.

An actual Chromium print produced `deck-print.pdf`. PDFKit confirmed exactly 22 pages, every page 960×540 pt; all 22 pages were rendered individually for the critic. The 1178×820 slide-6 image visibly contains a large model and compact controls without a clear visible physical-test lesson. Slides 7 and 8 retain the unexplained technical framing called out by the user. Sampled repair evidence shows the complete CAD concept at 855×882 slide 3 and no overlapping bottom labels at 390×844 slide 10. These observations are input evidence only; Q22C-a owns the complete audience audit.

Evidence directory `/tmp/cad-audience-baseline/` contains `1280x800-slide-1.png` through `1280x800-slide-22.png`, the compact/mobile files named by viewport and slide, `print-1.png` through `print-22.png`, `deck-print.pdf`, `print-text.txt`, and `report.json` with all manifest entries, visible texts, viewport sizes and scroll geometry. Exact paths were sent to Q22C-a and root as they became ready.

Commands, both successful:

- `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node /tmp/cad-audience-baseline/capture.mjs`
- `swift /tmp/cad-audience-baseline/pdf-inspect.swift /tmp/cad-audience-baseline`

Only this receipt and temporary capture files were written. No source, tests, dependencies, locks, Git, CAD, slicing, printer, hosting or unrelated files changed. No broad tests or exercise-control checks ran for baseline capture. Next: Q22C-a completes AUDIT.md before Q22I source edits; final Q22V validates the resulting frozen rewrite, including the real exercise and all 22 slide renders.
