# Concrete fit example

## Frozen contract

Replace only slide 3 of the accepted 22-slide deck. Begin with the physical action: a metal rod goes into a hole in a small printed test piece for the XT60 jig. Explain the recorded very-tight result in everyday words, then draw the lesson. Numeric hole size is a CAD design value, never a measured printed diameter. Do not invent the cause, insertion force or a successful assembly; leave the later size comparison on slide 6. The user's correction supersedes REQ-012's exact abstract slide-3 diagram and REQ-015's slide-3 preservation boundary. Preserve all other 21 sections, both scripts and simulator.

Baseline HTML: c991fae1a02be21e60a6f84e6d7284c6a5b58affdb456a81a362f7333299d904. Baseline candidate: 23c7635486cb1842054ff8d04833653664d4ecd38c37e8c6097a291ee54f0ab2 (8/8 verified before mutation). BASELINE_INPUTS and PRESERVATION_BASELINE capture before state; FROZEN_INPUTS captures decision-bearing inputs; CANDIDATE captures final builder/artifact.

## Execution DAG

| ID | Owner / role | Dependencies | Done gate | Exclusive writes | Ceiling |
| --- | --- | --- | --- | --- | --- |
| T3 | /root/slide3_writer; writer | verified baseline | concrete slide, build/check, frozen candidate | builder/HTML; affected text assertion; iteration contracts/manifests; requirements/experience/decision/CURRENT | strong/high; ~3 min, 5k tokens |
| TV | /root/slide3_validation; validator | T3 frozen candidate | source preservation, desktop/mobile/print | VALIDATION.md | strong/high; ~2 min, 3k |
| TC | /root/slide3_critique; critic | T3 frozen candidate | clarity and factual/visual truth | CRITIQUE.md | balanced/medium; ~2 min, 2k |
| TR | /root/slide3_review; formal reviewer | TV + TC on same candidate | independent provenance join | REVIEW.md | balanced/medium; ~1 min, 2k |

All roles may read this project and frozen source evidence. Root owns PROJECT_STATE/NEXT_AGENT/final HANDOFF. Manifest path-and-content SHA-256 inputs are immutable per candidate; evidence and orchestration indexes are excluded. TV/TC may run in parallel with disjoint writes. At most three workers, one candidate writer; initial attempt plus two focused repairs. No new tests, source-project/CAD/simulator/dependency/lock/Git/hosting/printer writes. Stop on scope growth, frozen evidence drift or exhausted repairs. Returns include fingerprints, commands, findings, coverage, limits and next action.
