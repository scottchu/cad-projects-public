# P4-DL nozzle comparison delivery

Owner `/root/slice_settings_diagnosis`; presentation only, subsequent to P4-S slicing and distinct P4-V comparison. URL https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-nozzles

Frozen media: P3 SVGmanifest34a72e4f776b66a48075b2192ead6b9a96a042c774fe31a8db1373244db34c51 and P4 media10e249a13ae7a74f5a449d5755ca21cb145b2402e4cc1f27522f1d2af76a5162. This page serves only original SVGs; it excludes temporary lowresolutionPNG artifacts. Distinct validator supplied incomplete white wordmark strokes / plate readability / lamp coarseness findings before page construction. Scope: unchangedGcode/meshes/media; newChinesecomparisonpage and allowlistedloopbackserver, private8448newrouteonly.

Pagepairs0.2/0.4actualplate,wordmark,andcentral2lamps forbothflat/relief, with exactselectedZ labels, nativeprofiledifferences, provisionalglass/material/scale and diagnostic/no-print boundary. No newlibraries or printcontrols.

## Manifest

SHA256(sorted path + NUL + contenthash + LF) fingerprint `a945071c8507c288287f1622ac146a7c88a9dc3a3f2031228a8b31b436982fc8`; relevantfrozenSVGs plus finalpage/server:

```json
[
  {
    "path": "projects/grenadier-fridge-magnet/review/p1-r4/nozzle-review.html",
    "sha256": "27fb7d45b45dd14a1d1bfcecfd7b519f59a17409ddc4c88101ae71c95ec9bbef"
  },
  {
    "path": "projects/grenadier-fridge-magnet/scripts/nozzle04-review-server.mjs",
    "sha256": "d71e8521fd770934fc1bb67ed372c9ce5377cc7aa9e8dc378c4357fcd56b7e65"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-lamp-1-z2.02.svg",
    "sha256": "ee692d66d94a337732d7dcf43c8f8b207bd8c3ae68ddc539c63311ce75ecd51f"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-lamp-2-z2.02.svg",
    "sha256": "b03e71e9ff25624134b848a8205479c470cc1017300d8ed87a848a8270456a05"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-lamp-3-z2.02.svg",
    "sha256": "953b718ca3dfcf2b9dd82884c13ea5c11076458f6c0cab4a56d05f22b9336b41"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-lamp-4-z2.02.svg",
    "sha256": "142ea4f6b6ab7da8388dad5a3680eb3c16ee7d344e1506be4a90d9f2eb5b68fb"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-plate-z2.02.svg",
    "sha256": "3ee2a3fdd625db035f56b05af5e92ef8b9e109b311680e9d8d0993fe04e57ca9"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-whole-z2.02.svg",
    "sha256": "31e93425a2ab524ab65d28066f59f1d0bfc2cf7a59da9a23e49da07b0ac96084"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/flat-wordmark-z2.02.svg",
    "sha256": "3cc8e6c5d51ba0f28f7e70af15815255c5631b870b825dd8988c42b242c31919"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-lamp-1-z2.42.svg",
    "sha256": "d99250f38c6dc282a7cd6a83b1126e2a4728bd210eb7f34ae93fb1cbd77092ce"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-lamp-2-z2.42.svg",
    "sha256": "c3f0a8b1c2238deda3379ce6a7d3e53a7e4b485f5a69d15af90189064427852b"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-lamp-3-z2.42.svg",
    "sha256": "1115258279cde9591b6750b206a89f4620a8fdb62c577638c6a4bad605639005"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-lamp-4-z2.42.svg",
    "sha256": "494e210612ee38a77c502a6e5e81427442b51e4360d058f397697e59efba72af"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-plate-z2.42.svg",
    "sha256": "53004fae4278bb2901c4b285ddbe032f216a825f2ccb4a076272b37e65358260"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-whole-z1.62.svg",
    "sha256": "99f17402c5a2dcc177ac9b9bc01346f75e8622488b3d35ab4b8d9e4f478119fe"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-whole-z2.02.svg",
    "sha256": "7d65fc20088a80c69c3a032cfb80416b6af52e853abd02ade693a67bb8ce27a7"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-whole-z2.42.svg",
    "sha256": "0e518964aa0affe23e382debd0b9f356260dbd9c4b0c4644a01fe1fc2791f476"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r3-validation/relief-wordmark-z2.02.svg",
    "sha256": "00c044781f3981981ab01a007dded8ee12cbc9e9682d628d458e22b14fad4d96"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-lamp-1-z1.96.svg",
    "sha256": "4750b78a433580d96587b3c451aaebd24b21a246d44f6db2f625cf449f4d1ef6"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-lamp-2-z1.96.svg",
    "sha256": "9efd4ab22974b03ec3fc302dee3a8e938a3ee271361b043e334b6f1d64ca4db0"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-lamp-3-z1.96.svg",
    "sha256": "bf2d4689b1f2aa55a6dd3984e3a2acb48e526a59b102e0d55c0b45aadaf1ebe2"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-lamp-4-z1.96.svg",
    "sha256": "3cd48d9a8a70dd8bed099f7f9ace56729080f59e05261a1083cde8cef9802ee5"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-plate-z1.96.svg",
    "sha256": "fe02a27f6955f67757e04b3bb2b606840010f5e074711fe2070be74170b813db"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-whole-z1.96.svg",
    "sha256": "b58006fb82675c7d9ca3ad5a122652086c1b9421c4a3bdf881fe72a26fd65980"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/flat-wordmark-z1.96.svg",
    "sha256": "51409b7034bb0b082784d5f062ce52d43680fa5e28a71e2b0349ed4a7167275d"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-lamp-1-z2.44.svg",
    "sha256": "7eafe55b57877b48c0e00e0d22a397436cfd9f56e7fc04a7c3fefd0607a60c39"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-lamp-2-z2.44.svg",
    "sha256": "bb77db06e04510e8c80f83f523caefaecbab82091cdf52e9721ab82d3b1bfb3f"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-lamp-3-z2.44.svg",
    "sha256": "ed11bebcc4cb75b6fab20254430457508c35f0680ec9e2f95fa928414d4f551d"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-lamp-4-z2.44.svg",
    "sha256": "d9819a07b498f3031cec317c2730730ad3377b5b4df614d5e40cdcfb935f1313"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-plate-z2.44.svg",
    "sha256": "836e7b14564f7c23ca561f43cf7a338fef3ed39935c22a9df868dd87cf5bbe2b"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-whole-z1.64.svg",
    "sha256": "6a41991d8d9d66fa777a173975b29338514201fa6e3701f2f82a23e804adca11"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-whole-z2.04.svg",
    "sha256": "ca2cff7beb9885c5cccd9ed06e3d4e218e689438f1feaafa52be4a5165b96897"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-whole-z2.44.svg",
    "sha256": "7dd176419f2780ac120aebe9fa1a1e4a41a4e671d4ede3478d3aa38991f5b13f"
  },
  {
    "path": "projects/grenadier-fridge-magnet/slicer/p1-r4-validation/relief-wordmark-z2.04.svg",
    "sha256": "12d2a22ba1eb72259e694304d50dbe5e4477be4fd72712c967c5454a1496ec8c"
  }
]
```

## Verification and lifecycle

`node --check projects/grenadier-fridge-magnet/scripts/nozzle04-review-server.mjs` passed. Page plus32SVGs returnedHTTPS200 with exactlocalhash parity. `tailscale serve status --json` snapshots `/tmp/grenadier-nozzles-serve-{before,after}.json`: deletingonlynewhandler fromafter yieldsdeep-equalbefore, preservingalloldroutes and443/Funnel.

Nativecommand: `tailscale serve --bg --https=8448 --set-path=/grenadier-nozzles http://127.0.0.1:49669`. NodePID84190, loopback49669, logs/pid `/tmp/grenadier-nozzles-server.{log,pid}`. Detached byrootuv Python subprocess.Popen(start_new_session=True); noautostart, no rebootpersistence. Rollbackonlyroute: `tailscale serve --https=8448 --set-path=/grenadier-nozzles off`; verifyPID84190stillbelongs tonewserverbeforestop. Root browserinspection pending; HTTP/hashchecks alone donot establishuserexperience, phoneunobserved.

## Root surface check and focused wording correction

Root inspected the live page in Chrome tab1204106755: the page opened, the flat anchor worked, and both plate and wordmark SVGs visibly rendered in the desktop screenshot. Phone experience remains unobserved. Root then challenged the initial interpretation of the broad letter-shaped blue-gray area. Independent P4-V confirmed that this is no-path background, not fused white extrusion; the 0.4 wordmark contains 85 white segments versus 499 in P3, with incomplete remaining strokes at the selected surface layer. The page now states severe distortion and incomplete white strokes, without claiming solid letters merged. No SVG changed. This single focused text correction supersedes the earlier delivery fingerprint bb1cbe4c85ec26c462121458f6d963fd0a35f8fffdde4e596ee57497c1283e7f. Corrected page returned HTTPS200 with exact byte parity; unchanged media remain bound to their prior checks.
