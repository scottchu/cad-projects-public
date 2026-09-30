# I5 implementation receipt

Status: candidate ready for independent validation, critique and review; I5 does not approve pixels. The retained pristine baseline is `/tmp/cad-intro-before/index.html` (`021a0510235ac59b6e66c687f0041a2294925a16fd12814a70748130ac7e1280`) and `build.mjs` (`21689333d513aa601a2600e6aa477e2b912fc1c9895e63ccb9fc9792c6ef8ee6`).

REQ-018 is implemented: new purpose slides are 3 (XT60) and 10 (Kage); the former rod/hole and count sections are slides 4 and 5. Their existing notes and visible content are retained under that declared ID/counter normalization, and all remaining 18 outer slide sections are preserved. The second executable script is unchanged; the first differs only because its embedded source drawer adds required S10 data. A01 is reused as an early CAD concept; S10 adds the XT60 README purpose with its exact hash. The Kage purpose draws on its README and KAGE-REQ-001. No physical-function claim is added.

The iteration contract directory and CURRENT pointer were created after the initial builder edit, contrary to the prescribed sequencing. This receipt records that procedural miss plainly. `/tmp/cad-intro-before/` was copied and hash-verified before the edit and supplies the frozen preservation baseline; no source changes followed completion of the iteration contract other than the user-directed copy cleanup before the candidate build.

Commands from repository root: `PATH=/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin:$PATH npm run build --workspace cad-agent-lunch-and-learn` passed (22 slides); the matching `npm run check --workspace cad-agent-lunch-and-learn` passed (5/5). Validation must inspect focused slides 3–5 and 10, verify manifests, preservation/reindexing and both scripts, then capture its own browser/PDF evidence. No simulator, CAD, tests beyond the existing check, dependencies, locks, Git, hosting, slicer or printer work occurred.

## Repair 1

V5 and C5 both found two P2 layout defects. Slide 3’s local image fit is now `contain`, preserving the full historical CAD assembly at narrow/mobile/PDF sizes. Slide 10 removes only the redundant `light → shadow plane` map label that collided with the hour/minute/second label on mobile; the visible purpose sentence already explains light and shadows. No other implementation scope changed. Candidate evidence records are mutable and excluded from `CANDIDATE.sha256` before refreeze.

Repair 1 rebuilt to HTML `f386aa4cd4c2fb90cf43c85a7e11139a0d15f7f07a28d4e3be37ff2b4144e57c`; frozen inputs are `00d3511d442e365cccc13564ca308bba979a3c531cf6e929108604ccab54d801`. The same root-workspace build passed at 22 slides and check passed 5/5. The refrozen candidate excludes this mutable receipt; V5 and C5 must recapture only slides 3 and 10 while reusing unchanged slide 4/5 evidence.
