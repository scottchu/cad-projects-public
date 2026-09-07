# SP-DEL-01 — private preview delivery

## Result

**PASS for Candidate 03 on the private 8453 development preview.** This closes
the conditional delivery gate in `REVIEW_RESUMED.md`; it does not approve main
merge, public release, Safari/iPhone acceptance, slicing, printing, fit, wear,
grip, drainage-in-use, or any physical claim.

The delivered source is commit
`8068fbd19b4fd526d6120e7dfd714e9aca217a9b`. Candidate manifest
`candidate-03.sha256` has SHA-256
`412b5e389a85dbaa7ad730870f496639d8dcd2e2129de733b4da1ba1e031fc63`
and passed 23/23 immediately after delivery. Formal approval
`REVIEW_RESUMED.md` has SHA-256
`6483322b210ebe7a49c02c117c04c82e89089f0ca1ab176a4231b91c14e49d19`.
The exact fingerprint check was:

```sh
git rev-parse HEAD
shasum -a 256 -c projects/laifen-wave-case/docs/iterations/2026-09-06-surface-pattern/inputs/candidate-03.sha256
```

## Build and served bytes

Root ran the repository-standard command once from the repository root; it
completed in 532 ms:

```sh
npm run build:openscad-simulator --workspace laifen-wave-case
```

The six written files and all six HTTPS 8453 responses matched byte-for-byte:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `index.html` | 8,210 | `b32d9a381fabf651b0399c82014e963c4737da244ec5361e549428755bc898d1` |
| `assets/index-CjWYai9H.css` | 6,445 | `71a309c144a86975065528a7c1d399189080803138c13c2e6a2082dded897569` |
| `assets/index-nGeRhi4f.js` | 547,111 | `160824dfd077a092d9fe46dd35f0c1eff15b66c688c124b94ddce03ac871d94e` |
| `assets/openscad-CutNEzGH.js` | 124,567 | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `assets/openscad-DIKIGOy4.wasm` | 9,603,115 | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| `assets/openscad.worker-Csx1v_-i.js` | 1,823 | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |

The validator independently repeated the live comparison with:

```sh
base_url='https://mac-mini.duckbill-ionian.ts.net:8453'
dist_root='projects/laifen-wave-case/preview/openscad-wasm-simulator/dist'
for asset_path in index.html assets/index-CjWYai9H.css assets/index-nGeRhi4f.js assets/openscad-CutNEzGH.js assets/openscad-DIKIGOy4.wasm assets/openscad.worker-Csx1v_-i.js; do
  curl --silent --show-error --fail --max-time 30 "$base_url/$asset_path" | cmp - "$dist_root/$asset_path"
  shasum -a 256 "$dist_root/$asset_path"
done
```

All comparisons passed. Root's `live-parity.json` evidence has SHA-256
`dfd7ba3b4e74e6fbaa85d69658624d8c0870bb1c6ec1ffcc6ff05c6580ac1326`.

## Fresh live observation

Root inspected fresh HTTPS page `1204106720` in Chrome. The page initially
loaded Smooth and exposed both Smooth and Diamond choices. At a true 390×844
viewport, selecting Diamond and generating the default closed container
produced a textured render, `Preview up to date`, and an enabled current
Download STL link. The browser Blob was 25,788,049 bytes with SHA-256
`5cfe2f06339bcc3df70dbc7072448789e5078aee9998a6599016298a148260fe`.
The actual latest Downloads file, `container-assembled-a572157f3f88 (1).stl`,
matched that size and hash. The validator independently rechecked the downloaded
file. Evidence hashes are
`5c0f95236f7b96e9cb23d13d63333bc229a4b2897116f7ad20f088490a04164a`
for `live-current.txt`,
`feaf5a9552feac19a775b58c29b0416f4186caf01e7203737cddcbad02acfef8`
for `live-download.json`, and
`6bc940de407addcc9e872aa7e3b353c58ca37d3754cfa32a5492cf8759d0b212`
for `live-mobile.png`.

This is Chrome evidence only. Native Safari remained unavailable with
`cgWindowNotFound`; the user's iPhone review remains open.

## Cleanup boundary

Root closed temporary test tabs 6711 and 6714 and stopped only temporary root
venv HTTP servers PIDs 26243 and 26244 on ports 5181 and 8461. Process and
listener checks confirmed those servers were absent. The retained preview
server PID 7451 on loopback port 5178 and private 8453 route remain active. An
older unattached tab 6708 could not be closed through the provider. Port 8448's
pre-existing HTTP 502 remains; its configuration was untouched. No unrelated
process was stopped.

This validator wrote only `DELIVERY.md`; root owns continuity updates, commit,
push, draft-PR delivery, and the remaining user acceptance gates.
