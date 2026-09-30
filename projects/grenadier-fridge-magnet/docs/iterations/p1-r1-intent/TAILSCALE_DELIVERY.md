# Private face review delivery — 2026-09-06

T1 owner: `/root/face_tailscale_delivery`; user asked “Tailscale” for the existing face review. Scope is transport only. Candidate remains `f893d8fbf98750be9e7366a5cfd8c78c90e58a0d4d0c73d5c2480ba471b7e652` (10 SHA-256 manifest entries verified). Only mutable delivery records were edited.

URL: https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-face

This is private tailnet Serve, not public Funnel. User device must have tailnet access. The fetched HTTPS document SHA-256 is `4b51e5381ba73135e49e6750fb8ac149f16d8c80d4aa07b352a5656c76212e4a`, matching `review/p1-r1/face-review.html`. Remote-device rendering and user face approval remain pending. No CAD, slicing, printer control or physical validation occurred.

## Execution and evidence

From repository root:

```sh
node projects/grenadier-fridge-magnet/scripts/face-candidate-manifest.mjs
tailscale serve status --json > /tmp/grenadier-serve-before.json
tailscale serve --help
tailscale serve --bg --https=8448 --set-path=/grenadier-face '/Users/scottchu/.codex/worktrees/a1ea952b-c880-4de4-b60d-6a179f4fa54b/design-projects/projects/grenadier-fridge-magnet/review/p1-r1/face-review.html'
```

Manifest verification passed. Direct-file serving failed with the installed macOS variant's explicit “Path serving is not supported on macOS due to sandbox restrictions” error. No configuration changed in that attempt. The fallback starts a process serving only the exact in-memory HTML (no directory or other project files):

```sh
node --input-type=module -e 'import http from "node:http"; import {readFileSync} from "node:fs"; const html=readFileSync("/Users/scottchu/.codex/worktrees/a1ea952b-c880-4de4-b60d-6a179f4fa54b/design-projects/projects/grenadier-fridge-magnet/review/p1-r1/face-review.html"); const server=http.createServer((req,res)=>{if((req.url!=="/"&&req.url!=="/grenadier-face")||!["GET","HEAD"].includes(req.method)){res.writeHead(404);res.end();return;}res.writeHead(200,{"Content-Type":"text/html; charset=utf-8","Content-Length":html.length,"Cache-Control":"no-store"});res.end(req.method==="HEAD"?undefined:html);}); server.listen(0,"127.0.0.1",()=>process.stdout.write(JSON.stringify(server.address())+"\n"));'
tailscale serve --bg --https=8448 --set-path=/grenadier-face http://127.0.0.1:54390/
tailscale serve status --json > /tmp/grenadier-serve-after.json
curl --fail --silent --show-error --max-time 20 'https://mac-mini.duckbill-ionian.ts.net:8448/grenadier-face' -o /tmp/grenadier-face-served.html
shasum -a 256 /tmp/grenadier-face-served.html
node --input-type=module -e 'import fs from "node:fs";import assert from "node:assert/strict";const before=JSON.parse(fs.readFileSync("/tmp/grenadier-serve-before.json"));const after=JSON.parse(fs.readFileSync("/tmp/grenadier-serve-after.json"));const added=after.Web["mac-mini.duckbill-ionian.ts.net:8448"].Handlers["/grenadier-face"];delete after.Web["mac-mini.duckbill-ionian.ts.net:8448"].Handlers["/grenadier-face"];assert.deepEqual(after,before);console.log(JSON.stringify({preexisting_config_unchanged:true,added}));'
```

Node returned loopback port54390, exec session44029. HTTPS fetch succeeded, exact hash above. Config comparison passed: the only new entry is `/grenadier-face` with proxy `http://127.0.0.1:54390/`. Existing TCP, Web handlers and AllowFunnel remain byte-value equivalent. Public443 was not changed;8448 was not added to Funnel. Scratch snapshots stay outside repository.

## Lifecycle and rollback

Tailscale route persists, but the loopback Node process is temporary and does not auto-start after reboot/session termination. The initial session44029 was replaced by the detached process described below. The prior localhost54327 server is stopped. For a later session, inspect Serve state, restart the exact narrow server (it prints a new available port), update only this route to that port, and verify the document hash again. The portable HTML remains the durable fallback.

Remove only this route with:

```sh
tailscale serve --https=8448 --set-path=/grenadier-face off
```

Do not run the CLI's suggested whole-port `tailscale serve --https=8448 off`, because that could remove unrelated review routes. Stop only the recorded Node process/session when the route is retired. Rollback is documented, not executed.

## Detached-process follow-up and root browser check

The initial exec server was replaced to survive the worker turn. A standalone copy of the exact narrow Node server above is at `/tmp/grenadier-face-server.mjs`. Node `spawn(process.execPath, ['/tmp/grenadier-face-server.mjs'], {detached:true, stdio:['ignore', out, out]})` with `child.unref()` launched PID30393; `out` is `/tmp/grenadier-face-server.log`. PID is recorded at `/tmp/grenadier-face-server.pid`. It reported loopback port54785. This is detached, without installing an auto-start service.

Executed `tailscale serve --bg --https=8448 --set-path=/grenadier-face http://127.0.0.1:54785/`, repeated HTTPS fetch/hash and the same before/after deep config comparison: both passed. Session44029 was then stopped (exit130). Current route therefore uses54785, not the historical54390 above. Process survives the tool turn but not a reboot; keep the Mac running. Restart can use `nohup node /tmp/grenadier-face-server.mjs </dev/null >/tmp/grenadier-face-server.log 2>&1 &`, record its PID and printed port, update only this route, and verify the hash. After verifying that PID30393 still belongs to this specific server, `kill 30393` stops it; combine with the route-specific rollback above when retiring delivery. Do not stop unrelated processes.

Root separately opened the exact HTTPS URL in Chrome tab1204106717, confirmed all five classes checked and both complete cars rendered, and marked it deliverable. This is local browser evidence, not phone/user-device validation. Face-fidelity acceptance remains pending.
