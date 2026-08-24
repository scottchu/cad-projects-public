export const CONFIG = Object.freeze({
  label: "com.scottchu.cad-viewer",
  legacyLabel: "com.codex.cad-viewer",
  host: "127.0.0.1",
  port: 3245,
  canonicalPython: "/Users/scottchu/Projects/personal/design-projects/.venv/bin/python3",
  viewerDefaultRoot: "/Users/scottchu",
  cacheRoot: "/Users/scottchu/.codex/plugins/cache/text-to-cad/cad",
  nodeDir: "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin",
  node: "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node",
  npm: "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/npm",
  commandPath: "/Users/scottchu/.local/bin/cad-viewer",
  plist: "/Users/scottchu/Library/LaunchAgents/com.scottchu.cad-viewer.plist",
  stdoutLog: "/Users/scottchu/Library/Logs/CADViewer/stdout.log",
  stderrLog: "/Users/scottchu/Library/Logs/CADViewer/stderr.log",
  stateDir: "/Users/scottchu/Library/Application Support/CADViewer",
  runtimeRecord: "/Users/scottchu/Library/Application Support/CADViewer/runtime.json",
  migrationRecord: "/Users/scottchu/Library/Application Support/CADViewer/legacy-migration.json",
  serviceDir: "/Users/scottchu/Library/Application Support/CADViewer/service",
  releasesDir: "/Users/scottchu/Library/Application Support/CADViewer/service/releases",
  currentLink: "/Users/scottchu/Library/Application Support/CADViewer/service/current",
  currentLauncher: "/Users/scottchu/Library/Application Support/CADViewer/service/current/launch-viewer.mjs",
  currentCli: "/Users/scottchu/Library/Application Support/CADViewer/service/current/cli.mjs",
  currentTemplate: "/Users/scottchu/Library/Application Support/CADViewer/service/current/launchd/com.scottchu.cad-viewer.plist.template",
  installHistoryDir: "/Users/scottchu/Library/Application Support/CADViewer/service/install-history",
  installLock: "/Users/scottchu/Library/Application Support/CADViewer/service/install.lock",
  lastKnownGood: "/Users/scottchu/Library/Application Support/CADViewer/service/last-known-good",
  tailscaleBase: "https://mac-mini.duckbill-ionian.ts.net",
  localBase: "http://127.0.0.1:3245",
  safePath: "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:/usr/bin:/bin:/usr/sbin:/sbin",
});

export function serviceTarget(uid = process.getuid()) {
  return `gui/${uid}/${CONFIG.label}`;
}

export function legacyTarget(uid = process.getuid()) {
  return `gui/${uid}/${CONFIG.legacyLabel}`;
}

export function guiDomain(uid = process.getuid()) {
  return `gui/${uid}`;
}
