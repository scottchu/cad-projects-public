# IMP-GCS-R18-01 stop receipt

**Status:** STOPPED NONCANDIDATE before browser or candidate freeze.

The frozen R18 input fingerprint `04f507e67834f8c9e77eafcb9477e189cfda6b167a9914746e41c440c73ce273` verified all 36 entries. Work stayed in the permitted R18 preview, R18 tests, R18 scratch audit, and this receipt. No R16/R17 renderer was imported; no core, route, CAD, export, slicer, printer, physical, or delivery state changed.

The standalone renderer has a local 84-path map, source-ban/exact-one gate, and ten explicit pattern builders. Initial full collecting audit found 43/84 because broad scalar spans masked or omitted many descriptor relationships. Grouped repair 1 removed the large-value cap and restored cross-section selection. Before the final repair, the collecting audit enumerated 41 failures. Grouped repair 2 replaced the shared minimum-span masking and added descriptor-specific closure-mode, end-size, label-mode/target, and attachment-half geometry.

The mandatory post-final-repair collecting audit is **73/84**, below the required 84/84. Remaining failures are exactly:

- `closure.matchPatternClosed`
- `closure.screw.leadRunoutTurns`
- `closure.screw.radialClearance`
- `surface.reliefMode`
- `surface.envelope`
- `surface.coverage`
- `surface.flute.duty`
- `surface.spiral.softness`
- `label.openScadFontFamily`
- `label.weight`
- `label.angleDeg`

The two permitted grouped repairs are exhausted. R18 cannot start caption-hidden sheets, strict browser coverage, candidate manifest, evidence manifest, serving, or delivery. The next responsible action is a new refrozen recovery that gives each listed remaining field a local descriptor-specific feature; it must not relax the audit or use raw/effect/hash output.

Executed commands:

```sh
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-03-p2-r18-standalone-semantic-renderer/inputs/frozen-inputs.sha256
node projects/laifen-wave-case/scratch/r18-collecting-audit/audit.mjs
```
