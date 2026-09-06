# Pattern performance delivery receipt

Status: **PASS** for the reviewed private-preview delivery gate.

## Frozen authority

- Candidate source manifest: `inputs/candidate-source.sha256`, 43/43 entries reverified with SHA-256 `3888018275bfcd05ab1d66a27d5b29a01eaf7268382075f4e2bd2047cc638c4c`.
- Candidate SCAD: `497098afa555092a0ed85a3a7213cd270852aa76f9001e1478c209cd8469bc42`.
- Independent validation: `VALIDATION.md`, SHA-256 `ace97b4da1cab515c72b32750937055241469fff8eb357a222af8a37e4fed466`.
- Formal approval: `REVIEW.md`, SHA-256 `994847a86d578b29c6949b9de2258f7ed93542f5b670e84d07f6713a7a93afe4`.
- Reviewed validator artifact manifest: `/tmp/pattern-performance-validation/ARTIFACTS.sha256`, 67 entries, manifest SHA-256 `750689ca62bd88e4a0006d1994b8a9f91f9daa415f14dd69a8285075ad2df7dc`.

## Build and deployed-byte gate

After formal approval, the root owner ran from the repository root:

`npm run build:openscad-simulator --workspace laifen-wave-case`

Result: PASS, 20 modules transformed in 597 ms. The live distribution references `assets/index-glg6xAxA.js`.

The independent delivery check fetched each URL with:

`/usr/bin/curl --fail --silent --show-error --connect-timeout 8 --max-time 30 https://mac-mini.duckbill-ionian.ts.net:8453/<path> -o /tmp/pattern-performance-delivery/https/<path>`

Every fetched file is byte-identical to both the reviewed scratch build at `/tmp/pattern-performance-validation/dist` and the local private-preview distribution:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `index.html` | 12,964 | `3845efdea8db81003569971cfb2b2594c5c783b0de96dc46323b22204b1ecafa` |
| `assets/index-glg6xAxA.js` | 562,016 | `a5866ab371b6d46b4916a5bb56e89e810043b5ff1a6a32941b812750d72c0d71` |
| `assets/index-iRxz8EXK.css` | 7,133 | `bb0c812317830060d51da5e56d7412a8b911cf75ab6ddc7c68c588e5285ace67` |
| `assets/openscad-CutNEzGH.js` | 124,567 | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `assets/openscad-DIKIGOy4.wasm` | 9,603,115 | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| `assets/openscad.worker-Csx1v_-i.js` | 1,823 | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |

Three-way parity receipt: `/tmp/pattern-performance-delivery/six-file-parity.json`, SHA-256 `03b7cd987095399baac7e53e2d8820ccb8aba1ac40a76488be4a1dd38985df49`.

## Fresh live artifact gate

The root-owned Chrome run loaded the HTTPS 8453 page and generated the default Ribs Body with Preview up to date, explicit 3D selected, and the current Download control enabled. Its current Blob reported `container-body-729e23f2d8dc.stl`, 7,623,719 bytes, SHA-256 `40f29575b0c752ea4f42dff181db02c4eb369a300e384d947509c28cd70c5401`.

The actual Download control wrote `/Users/scottchu/Downloads/container-body-729e23f2d8dc.stl`. Independent filesystem hashing returned the same 7,623,719 bytes and SHA-256. Browser state and screenshot remain at `/tmp/pattern-performance-delivery/live-state.txt` and `live-preview.png`; the browser observation belongs to the root owner.

## Scope

This receipt establishes the reviewed source fingerprint, standard private-preview build, six-file scratch/local/HTTPS byte parity, and one fresh current Blob/download identity check. It adds this record and temporary delivery evidence only. It does not claim STEP, slicer, print, fit, durability, or other physical acceptance.
