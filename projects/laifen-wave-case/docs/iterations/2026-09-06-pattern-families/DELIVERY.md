# Pattern families delivery receipt

Status: **PASS for reviewed R2 private-preview delivery**. Formal review `b78f64856a4a5d90e92c4f3db63d4dece4cef0ca6d4b2fb4701fbb04dbd775a4` approves R2 for private HTTPS8453 and a draft PR, conditional on the final build/parity/live gate recorded here.

## Frozen source and build

The final 37-path source manifest `/tmp/pattern-families-full-r2/candidate-source.sha256`, SHA `6701e4c3667e718455cf8ee622684c3d0e0f74971e51bc4f279f98b13554fc1d`, reverified 37/37 immediately before delivery checks. The reviewed scratch build manifest remains `/tmp/pattern-families-full-r2/candidate-artifacts.sha256`, SHA `7e6cedbb7e104ecdacfde7199011449a24d9ebbb930689ef6af2bee3f5a2b0b4`.

Root ran the standard repository command:

```sh
npm run build:openscad-simulator --workspace laifen-wave-case
```

Result: PASS, 20 modules transformed in539ms; the existing bundle-size advisory remained. This updated only the existing private preview dist. No dependency, service or Tailscale configuration changed.

## Local and HTTPS byte parity

The validator fetched the six live files with bounded `curl --fail --silent --show-error` requests from `https://mac-mini.duckbill-ionian.ts.net:8453/` and compared SHA-256 and byte count against both the reviewed R2 scratch build and current local dist. All6/6 match exactly:

| File | SHA-256 |
| --- | --- |
| `index.html` | `a3f7c3300d772c4c2e6477c773bdcd3e4163621e9da36ec2c128189ed312f130` |
| `assets/index-DIOcam4t.js` | `d60fe5e20dc8ef8c60663b81ca112a66cf9bcb7e0e108a919fa55c684f4ba0d8` |
| `assets/index-iRxz8EXK.css` | `bb0c812317830060d51da5e56d7412a8b911cf75ab6ddc7c68c588e5285ace67` |
| `assets/openscad-CutNEzGH.js` | `904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e` |
| `assets/openscad-DIKIGOy4.wasm` | `f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26` |
| `assets/openscad.worker-Csx1v_-i.js` | `cf543214d381e56ac230d6853810786ae70c52977d408e64695db595574fd46e` |

Parity receipt `/tmp/pattern-families-delivery/six-file-parity.json` has SHA `8c58239f1c80834c61a92dc7a9ddbb09eefa15a51b59b806e052f144d32863de`.

## Fresh live artifact

Root's fresh Chrome HTTPS8453 run used Ribs Body, D30/H60/W4.56/T3, Auto lid, spacing6/depth0.60, Bottom7. The accessible state showed all five patterns and `Preview up to date`; the rendered Ribs cutaway is retained at `/tmp/pattern-families-delivery/live-preview.png`.

The current Blob reported `container-body-b78b64efc733.stl`, **7,810,517 bytes**, SHA `0a6e4ae3d319210dd73b9ce6bb9731ea4d7285cc433bf815cf74cfa2efb6282a`. The newly downloaded `/Users/scottchu/Downloads/container-body-b78b64efc733 (1).stl` independently rehashed to the same size and SHA. The validator's comparison is `/tmp/pattern-families-delivery/live-byte-verification.json`.

## Delivery boundary

The reviewed R2 source, standard local build, served private-preview bytes, current generated Blob and downloaded STL are therefore joined by exact fingerprints. Browser observations are root-owned Chrome evidence; Safari/iPhone remains untested. This receipt does not authorize or claim a main merge, public release, STEP/slicer validation, printing, grip, cleaning, drainage-in-use, thread wear, fit or physical acceptance. Root retains commit, push, draft-PR and continuity ownership.
