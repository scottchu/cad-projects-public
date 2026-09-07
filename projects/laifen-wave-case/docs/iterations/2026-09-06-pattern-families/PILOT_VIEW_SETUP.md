# PF-PILOT-VIEW setup receipt

The review harness is isolated at `/tmp/pattern-families-visual`. It imports
the existing `createViewer` API from the customizer's `viewer.mjs` through a
read-only source symlink, then loads copied, exact written STL files using
`STLLoader`; it does not generate, proxy, simplify, or modify geometry.

## Input verification

`/tmp/pattern-families-direct-r1/candidate.sha256` verified at
`6f3772ed60afb47845a41c1af149c89b5e7b302c7cb0ab2b7cbe7638234c4749`.
The copied review assets match its three specified STL hashes:

| Artifact | SHA-256 |
| --- | --- |
| `spiral-body.stl` | `1689355bf915535456af607ef57f372ac231bcce34e8c87715bc270d0d8ae840` |
| `spiral-cap.stl` | `317f1f85c1901f2ef287c4ed8440077045ba55da4aaa73e8da581586a3d433e5` |
| `spiral-assembled.stl` | `632cc81cdfd7a4416775fad29442f7b6473f0e0b1e4097c86c04bfe728466c36` |

The page has Body, Cap, and Assembly selectors, Cutaway/Solid controls, and
Fit view. Its on-page label reports the selected artifact's byte count and
SHA-256 prefix. It is an inspection surface only.

## Build and manifest

Build command run from `/tmp/pattern-families-visual`:

```sh
node /Users/scottchu/.codex/worktrees/9d1d/design-projects/node_modules/vite/bin/vite.js build --config vite.config.mjs
```

Vite 6.4.3 completed with 10 transformed modules. Harness source hashes:
`index.html` `e2fa090d8c0d89076a3a0572de6793aeefe8777f2240f47b95317feece59655a`,
`main.mjs` `5132858d06e088aa8f45da497dcd9ad6f43d4b6ef8bad32ebfceb879f7e606dc`,
`style.css` `162a756d2c420e2953c6b6dae8fc0dfe06990615176e61bfd4969356d3660310`,
and `vite.config.mjs` `1e5abee5a747fb8f04d4be15a149d626c602a35541a02e3adfbda8bd6c887c79`.
The built files are `dist/index.html`
`0a81ea5df7e1efff6463255e73afda98492014f29a0bdf81b8a269eac5a9b615`,
`dist/assets/index-BEEhUnZK.js`
`f6f31add73ef2d6905b12e12930fe8c675a07afd1db941c55b07e9c87b1eaee2`,
and `dist/assets/index-C5Tn1pAB.css`
`a5a25dc809f6cf937369ec64ef335abc7d6b728e917b4cf6bbd93468022e542a`.

## Root-owned server and review command

No server or browser was started by this role. Root can serve the built review
surface with:

```sh
cd /tmp/pattern-families-visual/dist
/Users/scottchu/.codex/worktrees/9d1d/design-projects/.venv/bin/python3 -m http.server 8462 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8462/`. Critic interpretation of seam, end, and
surface observations remains independent work.

## PF-PILOT-VIEW repair 1

The initial built `dist/` directory omitted the binary STL assets, causing the
page to parse the HTTP fallback as an STL and fail with an invalid typed-array
length. The three already-verified frozen STL files are now copied directly
into `dist/`; source artifacts remain unchanged. A live read-only HTTP check
against the root-owned 8462 server returned byte-identical SHA-256 values for
Body `1689355bf915535456af607ef57f372ac231bcce34e8c87715bc270d0d8ae840`,
Cap `317f1f85c1901f2ef287c4ed8440077045ba55da4aaa73e8da581586a3d433e5`,
and Assembly `632cc81cdfd7a4416775fad29442f7b6473f0e0b1e4097c86c04bfe728466c36`.
Reload `http://127.0.0.1:8462/` with cache bypass before browser inspection.
