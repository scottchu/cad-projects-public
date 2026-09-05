# VFR-03M private preview delivery

Status: **DELIVERED / USER CHOICE OPEN**

## Candidate and review

- Candidate manifest: `candidate/MOBILE_CLARITY_CANDIDATE.sha256`
- Candidate fingerprint: `f5c86706b4b0e0561edcabe48d91ed9a2295a286eacadf725bf3f77f2f17517c`
- Independent validation: `MOBILE_CLARITY_VALIDATION.md`
- Validation SHA-256: `71abcaa6b329269964efe344df4a79e9f58201ed23e01d83e45bcb3eb60e01b2`

## Private delivery

- URL: <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-pattern-gate/>
- The existing `/openscad-pattern-gate` handler still proxies to the existing loopback service on port 8972. No process, port, Funnel, or unrelated route changed.
- The three fetched live files matched the validated source bytes exactly:
  - `index.html` — `ec327452a7d778667630d65efd03a4944c75124dbf9719d26539ac596f227a47`
  - `styles.css` — `4141e1a23ade6c20f1f9fb70bd51afb9681abf9603d25442a4eb5b840f02f235`
  - `app.js` — `15a7a77f50dcf1cfd6aa0929e72884e55664d653335911ecc28712f092048339`
- A fresh cache-busted in-app-browser load showed the compact question, both plain case silhouettes, A selected by default, and the Engineering details collapsed.

## Boundary

This delivery changes only how the intent question is presented. It does not change OpenSCAD geometry, CAD, mesh, export, slicer, hosting topology, or physical acceptance. The user still needs to choose A or B before VFR-04 can change the 3D pattern.
