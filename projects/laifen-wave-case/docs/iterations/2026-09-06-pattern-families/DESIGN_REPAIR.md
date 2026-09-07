# PF-DES-02 — UI contract clarification

Input DESIGN SHA-256 verified:
`375bf58ffc3d60605c12da37c882778a0dbf93762031c3b2b39d1ee1b4edf8eb`.
Responds to the four P1 findings in DESIGN_CRITIQUE.md, SHA-256
`e7fcc2bef8d70c9e212759b3276f2745b43475d65867a79253e85fe11836cdc8`.

1. Exact entries own state and the thumb renders their exact position. Explicit
   slider actions alone commit a stepped value; arrow/pointer rules are fixed.
2. Allowed ranges use counterfactual repair of only the slider's current raw
   field. Invalid dependencies disable affected sliders with explicit copy;
   exact inputs remain usable. No hidden defaults or last-valid substitution.
3. Five labelled, visually distinct >=44px cards wrap three/two on the390px
   phone viewport; preserve focus, no horizontal overflow and group placement.
4. Full normalized canonical snapshot remains hashed. Only inactive raw
   memories are excluded; inactive source fields retain fixed canonical defaults.

Geometry, finite guards, new-family defaults, pilot tuple and pilot/evidence
plan are unchanged byte-for-byte from the Geometry heading through end of file.
BRIEF and all source/tests/runtime artifacts were outside this repair scope.
The added browser cases are acceptance targets, not claims of executed tests.

Focused repair2 closes the remaining P1 from critic recheck SHA
`b8498ae93e285bb2047fa6de13c35ede5067964de26cf89cd3d494e227de89fa`:
a slider whose own raw value is blank/non-numeric is disabled with its thumb
hidden and an exact-entry repair prompt. No fallback origin or first-arrow
meaning exists until numeric entry. Geometry remains unchanged.
