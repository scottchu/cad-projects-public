# VFR-03M independent mobile-clarity validation

Status: **PASS**

Validator: independent role `/root/openscad_mobile_clarity_validator`.

## Frozen inputs

Validated candidate manifest:
`candidate/MOBILE_CLARITY_CANDIDATE.sha256`

Candidate fingerprint (SHA-256 of that manifest):
`f5c86706b4b0e0561edcabe48d91ed9a2295a286eacadf725bf3f77f2f17517c`

All five manifest entries matched their recorded SHA-256 values:

- `preview/openscad-pattern-gate/index.html` — `ec327452a7d778667630d65efd03a4944c75124dbf9719d26539ac596f227a47`
- `preview/openscad-pattern-gate/styles.css` — `4141e1a23ade6c20f1f9fb70bd51afb9681abf9603d25442a4eb5b840f02f235`
- `preview/openscad-pattern-gate/app.js` — `15a7a77f50dcf1cfd6aa0929e72884e55664d653335911ecc28712f092048339`
- `inputs/MOBILE_CLARITY_MANIFEST.sha256` — `246e11864f285eb0e82aa77838d0de2a3db91bd58410a7076a874114a917b618`
- `MOBILE_CLARITY_IMPLEMENTATION.md` — `32be0a65037017d3f56f204f1250a9d43fef627cb1920e0c6548d2bd2c8c84a3`

`app.js` therefore remains exactly the required unchanged file.

## Commands and observations

1. Ran a Node SHA-256 verification over the candidate manifest and every listed
   path. Result: all entries `OK`; computed manifest fingerprint matched the
   frozen task value above.
2. Opened the staged local candidate at
   `http://127.0.0.1:8972/openscad-pattern-gate-candidate/` and used browser
   device emulation at 390 x 844.
3. Initial mobile screen observations:
   - compact title bounding box: 370 x 25.5 px;
   - controls end at y=257.7 px;
   - two-silhouette comparison ends at y=510.9 px;
   - collapsed Engineering details starts at y=526.9 px;
   - document width and scroll width are both 390 px;
   - A is pressed and its silhouette border is `rgb(24, 61, 75)` while B
     remains `rgb(211, 221, 225)`.
4. Clicked the existing B control. Result: `aria-pressed` changed to A=false,
   B=true; the highlighted border moved to B; the plain state changed from the
   smooth blank-ring statement to `B is selected: the pattern reaches the seam.`
5. Expanded the Engineering details. Result: the deterministic SVG rendered
   (120 paths after B selection), N33/0.18 text remained present, the fixed
   numeric fact `OD 39 mm, skin depth 0.45 mm, axial pitch 4.8 mm` remained
   present, and the exact technical question remained present. At mobile width,
   document width and scroll width stayed 390 px.
6. Switched to a 1440 x 900 desktop emulation and reloaded. Result: comparison
   width 880 px, right edge 1160 px, grid width 846 px, and document scroll
   width 1440 px: no horizontal overflow. Engineering details returned closed.
   Browser console error/warning query returned an empty list.
7. Static asset inspection found only local relative `styles.css` and `app.js`;
   no external image, stylesheet, script, or network asset is referenced.

## Requirement coverage

| Requirement | Result |
| --- | --- |
| Plain, compact first question | Pass — `Which middle seam looks right?` is a single compact line. |
| A/B controls and simple silhouettes above fold | Pass — both controls and the complete comparison are visible by y=511 of 844 px. |
| Required labels | Pass — A shows `現在：中間空一圈 / smooth gap`; B shows `要做：紋路接到接縫 / continuous pattern`. |
| Existing control drives selected state | Pass — the existing `aria-pressed` state moves both visible highlight and plain-language statement. |
| Engineering evidence retained but not front-loaded | Pass — details is collapsed initially; expanded view retains SVG, facts, and exact question. |
| Desktop readable without horizontal overflow | Pass — 1440 px document scroll width equals viewport width. |
| No source/worker/CAD/hosting change | Pass for candidate scope — manifest confirms HTML/CSS presentation work and unchanged `app.js`; validation made no source or hosting edits. |

## Findings and limitations

No blocking or major findings. The staged page is a relationship-choice aid;
it does not validate a new physical case, OpenSCAD diamond generator,
watertight mesh, STEP/STL export, slicer result, or print. It also awaits the
user's simple A/B choice before any geometry change is authorized.

## Next action

The root may publish this already-validated static candidate to the existing
private route, verify byte parity there, and ask the user to choose A or B.
