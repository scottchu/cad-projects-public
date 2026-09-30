# H1 private Tailscale presentation host

Date: 2026-09-01

## Endpoint

Private tailnet URL: `https://mac-mini.duckbill-ionian.ts.net:8448/lunch-and-learn`

The route is on existing private HTTPS port 8448. It is not Funnel-enabled.

## Service

- launchd label: `com.scottchu.cad-agent-lunch-and-learn-preview`
- plist: `/Users/scottchu/Library/LaunchAgents/com.scottchu.cad-agent-lunch-and-learn-preview.plist`
- server: `/Users/scottchu/Library/Application Support/cad-agent-lunch-and-learn-preview/server.mjs`
- interpreter: `/Users/scottchu/.asdf/installs/nodejs/26.7.0/bin/node`
- loopback: `127.0.0.1:8973`
- live source: `/Users/scottchu/.codex/worktrees/740e/design-projects/projects/cad-agent-lunch-and-learn/index.html`

The server reads that exact file for every request, so later authorized generated-HTML updates appear without a server restart. It accepts only `GET` and `HEAD` for `/` and `/index.html`; all other methods and paths return 404. It exposes no directory listing or other project files.

## Candidate preservation and verification

At host creation, `index.html` SHA-256 was
`911353124f9ab5a7537333d126ff4ad0da3a9d162491a2f4dac33f605f89d81f`.
The existing candidate manifest verified 10/10 files and retained its SHA-256
`b353bfadf7c274ab126e08d059611a8899c139710fa65ce7a3d254ab98ebdc8d`.

Both `http://127.0.0.1:8973/index.html` and the private HTTPS URL returned 200 and the same HTML SHA-256. HEAD returned 200 at both routes. Local `GET /build.mjs` and `POST /index.html` each returned 404. Root independently verified the private URL with normal TLS verification (without `--insecure`): it returned HTTP 200 and the same `911353124f9ab5a7537333d126ff4ad0da3a9d162491a2f4dac33f605f89d81f` response hash.

`tailscale serve status --json` after the change retained the prior 8448 handlers `/xt60-clamp`, `/laifen-case`, and `/laifen-skin`, adding only `/lunch-and-learn`; its `AllowFunnel` keys remained only ports 443 and 10000. `launchctl print` reported the H1 label as `running`, and `plutil -lint` passed.

## Root verification

From the repository root:

```sh
shasum -a 256 -c projects/cad-agent-lunch-and-learn/docs/iterations/2026-09-01-first-deck/CANDIDATE.sha256
curl --fail --silent --show-error http://127.0.0.1:8973/index.html | shasum -a 256
curl --fail --silent --show-error https://mac-mini.duckbill-ionian.ts.net:8448/lunch-and-learn | shasum -a 256
curl --silent --output /dev/null --write-out '%{http_code}\n' -I https://mac-mini.duckbill-ionian.ts.net:8448/lunch-and-learn
launchctl print gui/$(id -u)/com.scottchu.cad-agent-lunch-and-learn-preview
/usr/local/bin/tailscale serve status
```

The two response hashes should equal the current `index.html` hash. After later HTML edits, they need not equal the frozen first-deck candidate hash; rerun the presentation's generation and candidate-validation gates for the revised artifact.

## Recovery and removal

Restart the persistent local service:

```sh
launchctl kickstart -k gui/$(id -u)/com.scottchu.cad-agent-lunch-and-learn-preview
```

If the route must be restored after explicit removal, use:

```sh
/usr/local/bin/tailscale serve --https=8448 --set-path=/lunch-and-learn --bg http://127.0.0.1:8973/index.html
```

To remove only this path while preserving the other 8448 handlers, use the path-specific Tailscale Serve clear operation after inspecting its current help and status; do not run `tailscale serve reset` or disable port 8448.
