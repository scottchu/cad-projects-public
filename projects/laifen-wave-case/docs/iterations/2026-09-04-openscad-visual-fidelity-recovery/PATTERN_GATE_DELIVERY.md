# VFR-03 private pattern-gate delivery

- URL: <https://mac-mini.duckbill-ionian.ts.net:8448/openscad-pattern-gate/>
- Candidate fingerprint: `6bfa2c2225e0abcf9fdb4f841f759196630a7f5daf544731ef57306c99732e8e`.
- Implementation receipt: `PATTERN_GATE_IMPLEMENTATION.md`, SHA-256 `24da65db9de459df8d66319803a9c87f5b8816c148ee4e99fa8134b62dbef5a4`.
- Independent validation: `PATTERN_GATE_VALIDATION.md`, SHA-256 `c09048629259e2a485920ccec95cf4084f415a068feda8499a3a0ad0627f9fe1`.
- Served bytes: `PATTERN_GATE_BUNDLE.sha256`; all three HTTPS responses returned `200` and matched the staged local files byte for byte.

The existing HTTPS 8448 Serve configuration was preserved and one private path handler was added: `/openscad-pattern-gate` proxies to the existing loopback 8972 server. No public Funnel or new process was created.

The live route opened with A selected and toggled to B successfully. B displayed the N33 valley-derived, `0.18` crest plateau, shared-phase relationship; document width equaled viewport width and SVG overflow remained clipped. The page is a 2D intent gate only. User pass/fail is still open, so VFR-04 3D pattern work remains blocked.
