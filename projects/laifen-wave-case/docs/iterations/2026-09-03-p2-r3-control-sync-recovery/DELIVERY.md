# DEL-GCS-REC-01 private delivery receipt

**Status:** PASS for isolated tailnet delivery and browser smoke, 2026-09-03.

The formal review receipt and candidate manifest passed before delivery:

- `REVIEW.md` SHA-256 `57e7a2578387418a3e6c5db850888d9334b563e91e60f56682be37b44bd250fc`.
- `inputs/review-join.sha256` SHA-256 `7e89663ea2d341f68b2c5e0f192df00a733481f677e9756bc31544e5f8523c3d`.
- Candidate manifest `inputs/implementation-recovery-candidate.sha256`: all five entries passed.

## Scoped mutation

Copied exactly these reviewed files from `preview/p2-r2-generic-container-simulator/` into the pre-existing loopback 8972 served directory `scratch/presentation/container-simulator/`: `index.html`, `app.js`, `math.mjs`, `style.css`. No validated source, CAD, OpenSCAD, STEP, slicer, project continuity index, or unrelated route was changed.

Added only this tailnet route:

`https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator` -> `http://127.0.0.1:8972/container-simulator`

Before mutation, 8448 contained the existing `/xt60-clamp`, `/laifen-*`, `/lunch-and-learn` mappings; 8449 remained `/` -> `127.0.0.1:3249`, and the public root remained `3245`. After mutation, every listed mapping remained and `/container-simulator` was present. No replacement or disruption occurred.

## Evidence and commands

Commands run:

```sh
shasum -a 256 -c inputs/implementation-recovery-candidate.sha256
shasum -a 256 -c inputs/review-receipt.sha256
tailscale serve status
tailscale serve --https=8448 --set-path=/container-simulator --bg http://127.0.0.1:8972/container-simulator
curl -fsS http://127.0.0.1:8972/container-simulator/<asset>
curl -kfsS https://mac-mini.duckbill-ionian.ts.net:8448/container-simulator/<asset>
tailscale serve status
```

Loopback and private HTTPS index, stylesheet, app, and math responses were HTTP 200 and byte/hash-identical:

| asset | SHA-256 |
| --- | --- |
| `index.html` | `ace28e8dd08de7f9ca9bf916887911e0d118c6dd4b0d2e6594f2a88950b878a5` |
| `app.js` | `575f3734f76dd6313ccc9e33b33ffb72008292c20b4dbfc3f5db517d9789affe` |
| `math.mjs` | `b3e4c734b166349251c9b7683aa23d428cb4d2f8f167ff29349def7dc024337b` |
| `style.css` | `a19c755ca5c27dbe602283ba2652c5b2ff005c2a59266b078c5930b58ff6ccf3` |

`http://127.0.0.1:8972/container-simulator/`, private HTTPS index, `3245/`, and `3249/` each returned HTTP 200. Chrome opened the private URL, displayed the two-piece container canvas and controls, and reported no warning or error console entries.

## Boundary

This is tailnet/local-static delivery evidence. User-device visibility/comprehension, CDN behavior, CAD, printable geometry, fit, physical acceptance, slicing, and printer action remain pending/out of scope.

**Next action:** user performs the explicit private-URL comprehension check.
