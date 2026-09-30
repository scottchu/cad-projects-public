# Opening formal review — OR

## Scope and candidate identity

Independent formal review of the two-slide concrete opening only. The reviewed
candidate is `index.html` SHA-256
`c991fae1a02be21e60a6f84e6d7284c6a5b58affdb456a81a362f7333299d904`,
with candidate manifest
`23c7635486cb1842054ff8d04833653664d4ecd38c37e8c6097a291ee54f0ab2`
(8 entries), and frozen-input manifest
`1625ba8fd661e5945f85dfe9aa641dd9d0758031c391424e922e1295e5fd4d50`
(11 entries).

## Evidence and review

- I ran `shasum -a 256 -c` for both manifests, then ran the independent
  focused final-candidate capture command
  `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node
  /tmp/cad-agent-opening-validation/repair.mjs`. Both manifests passed before
  and after its capture: candidate 8/8 and frozen inputs 11/11. The command
  also rechecked the final HTML hash and preservation of slides 3–22 (20/20)
  and both inline scripts (2/2).
- I directly inspected the fresh final-candidate mobile capture at
  `/tmp/cad-agent-opening-validation/repaired-390x844-slide-2.png`. At
  390 px wide, Slide 2 visibly carries the requested concrete progression:
  WHY (clock and wire jig), HOW (CAD/agents, print, try, revise), and WHAT
  (Kage, XT60 jig, learning). The repaired prose has normal word separation,
  readable wrapping, legible citations, and no visible clipping or overlap.
- The frozen brief/design and opening source establish the exact topical title
  “3D Printing with CAD & AI Agents,” first-person motivation, and limits on
  claims. OV independently checked title, navigation, notes, overview,
  desktop captures and an actual 22-page PDF; OC independently reviewed the
  final mobile repair and narrative. Their final receipts are PASS on this
  exact candidate. The former initial-candidate whitespace defect is closed.

## Decision

**PASS.** REQ-015 is satisfied and the affected opening requirements retain
their evidence boundary. Slides 3–22 and scripts are preserved; the change
does not establish CAD, slicer, printer, or physical-project acceptance.

## Limits and next action

The actual 22-page PDF/desktop evidence was produced for the immediately
pre-repair candidate and is carried forward only because an independent
reconstruction proved the final delta removes four responsive separators (and
the generated overview separator) while recovering the prior HTML exactly.
Fresh final-candidate visual evidence is the affected mobile Slide 2 capture.
No broad simulator or unchanged-slide testing was repeated. Next action is
the user's story, pacing, and emphasis review of the revised opening.
