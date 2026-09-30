# Concrete fit example handoff

Slide 3 now explains a real early XT60 test: a 4.00 mm metal rod enters a small printed test piece with a hole designed at 4.05 mm, but the physical fit was very tight and the rod had to be pushed back out. A labeled schematic and Design → Print → Try sequence introduce the objects and action before the lesson. The printed-hole diameter, force and cause remain unknown; this is no new physical acceptance.

HTML SHA-256: `ebb4113fb57951ba62cfa2760fdec40d918991b265b8c688a07d713c61797ee4`. Candidate manifest: `4f79f9740e85eb0e11b16cdd2ff219324a69756b5d444add18b870fa81dedda1` (8 files). Frozen-input manifest: `af0b1d453916bf6f65b2c6609024cfe719f7e78a22979131f7f4d84e954ced9a` (10 files). Root independently verified both manifests and the live private response.

T3 `/root/slide3_writer` implemented and built the candidate; all five existing checks pass. TV `/root/slide3_validation` verified desktop/mobile/actual PDF rendering and complete preservation against the exact prior HTML. Its full-section comparison includes nested slide 6, resolving the original preservation regex limitation. All other 21 sections and both scripts are byte-identical. TC `/root/slide3_critique` passed novice clarity and factual/visual truth with no P1/P2. TR `/root/slide3_review` PASS independently joined the exact TV/TC candidate, verified both manifests and inspected the actual desktop capture. All four task gates are complete; no source repair is pending.

No simulator, dependency, test, evidence-source project, CAD, slicer, printer, hosting configuration or Git changes were made in this revision. Prior simulator acceptance carries forward, including its minor sleeve-top framing limitation. Existing mobile toolbar Fullscreen clipping is outside this slide-3 change; slide content remains reachable by scrolling.

Private review: https://mac-mini.duckbill-ionian.ts.net:8448/lunch-and-learn?v=rod-example#slide-3 . Normal TLS, HTTP 200 and exact candidate bytes were verified. The persistent service reads regenerated HTML on each request; no restart was required. Recovery remains in `../2026-09-01-first-deck/HOSTING.md`.

Edit `build.mjs`, regenerate and check using root workspace commands from IMPLEMENTATION.md. Root owns this handoff and continuity indexes; worker evidence is in IMPLEMENTATION, VALIDATION, CRITIQUE and REVIEW. Next: user review of the concrete explanation and continued slide-by-slide feedback.
