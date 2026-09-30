# Slide 4 layout handoff

The screenshot showed oversized count numerals crowding together and labels detached from their numbers. Slide 4 now uses flat number/label groups, controlled numeral sizes and a caveat grouped beneath. Mobile stacks the groups. Counts, labels, caveat, snapshot, source and speaker-note meaning are unchanged; these remain record counts.

Current HTML: `021a0510235ac59b6e66c687f0041a2294925a16fd12814a70748130ac7e1280`. Candidate manifest: `42516d298d5aba333a83edc262e7d33216a6d9c175526f37216f8f9d68e9dbd6` (8 files); frozen inputs: `2d61d3f9a52579ce10eb601ef3c04c64210e566b3954bbd5b1a19551a8d7a1fc` (7 files). Root independently verified all entries and exact private served bytes. The exact preceding HTML and builder are retained at /tmp/cad-slide4-before/.

C4 /root/slide4_writer built and passed the five existing checks. V4 /root/slide4_validation and C4C /root/slide4_critique rejected the first candidate: Georgia's painted 5 overlapped its label at desktop, narrow and print sizes despite positive DOM spacing. Repair 1 changed only numeral line height and content-row sizing. Both then passed fresh 1280×800, 855×882 and 390×844 captures and page 4 of the actual 22-page PDF. R4 /root/slide4_review independently verified both manifests and the narrow screenshot, and joined PASS. All four task gates are complete. Initial failures remain in the evidence records. No source repair is pending.

All other 21 complete outer slide sections and both scripts match baseline. Changed scope: slide-4 structure/scoped CSS in build.mjs, regenerated HTML, REQ-017, experience/decision/CURRENT and iteration records. No tests, simulator, dependencies, locks, evidence-source projects, CAD, slicing, printer, hosting configuration or Git changes. Earlier simulator evidence and its minor framing limitation carry forward.

Private review: https://mac-mini.duckbill-ionian.ts.net:8448/lunch-and-learn?v=count-layout-r1#slide-4 . Normal TLS, HTTP 200 and exact HTML verified. No service restart required; recovery is in ../2026-09-01-first-deck/HOSTING.md. Temporary descriptor pressure interrupted browser setup; /bin/zsh with login:false and tty:false restored command execution without global changes. Evidence is under /tmp/cad-agent-slide4-validation/, with first-candidate captures retained in initial/.

Regenerate/check using the root workspace commands in IMPLEMENTATION.md. Root owns continuity; C4/V4/C4C/R4 receipts are canonical evidence. Next: user review of slide 4 and continued slide-by-slide feedback. This acceptance covers presentation layout only.
