import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  classifyState,
  encodedWorkspaceUrl,
  inspectRuntimeCandidates,
  parseSemver,
  renderPlist,
  selectViewerRuntime,
} from "../payload/core.mjs";
import { parseArguments } from "../payload/cli.mjs";

function makeRuntime(cache, name, version, start = "node scripts/start-viewer.mjs") {
  const root = path.join(cache, name, "skills", "cad-viewer", "scripts", "viewer");
  fs.mkdirSync(path.join(root, "scripts"), { recursive: true });
  fs.writeFileSync(path.join(root, "package.json"), JSON.stringify({ version, scripts: { start } }));
  fs.writeFileSync(path.join(root, "scripts", "start-viewer.mjs"), "// fixture\n");
  return fs.realpathSync(root);
}

test("SemVer parser rejects malformed versions and resolver prefers highest stable", () => {
  assert.equal(parseSemver("01.2.3"), null);
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-runtime-"));
  try {
    makeRuntime(root, "older", "1.9.0");
    const expected = makeRuntime(root, "stable", "2.0.0");
    makeRuntime(root, "future-prerelease", "9.0.0-rc.1");
    const selected = selectViewerRuntime(root);
    assert.equal(selected.path, expected);
    assert.equal(selected.version, "2.0.0");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("resolver selects prerelease only when no stable exists and applies lexical tie break", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-runtime-"));
  try {
    const expected = makeRuntime(root, "a", "3.0.0-rc.2");
    makeRuntime(root, "b", "3.0.0-rc.2");
    makeRuntime(root, "lower", "3.0.0-rc.1");
    assert.equal(selectViewerRuntime(root).path, expected);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("resolver rejects escaped symlinks and malformed packages", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-runtime-"));
  const outside = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-outside-"));
  try {
    makeRuntime(root, "valid", "1.0.0");
    makeRuntime(root, "malformed", "bad");
    const linkParent = path.join(root, "escaped", "skills", "cad-viewer", "scripts");
    fs.mkdirSync(linkParent, { recursive: true });
    fs.mkdirSync(path.join(outside, "scripts"), { recursive: true });
    fs.writeFileSync(path.join(outside, "package.json"), JSON.stringify({ version: "4.0.0", scripts: { start: "x" } }));
    fs.writeFileSync(path.join(outside, "scripts", "start-viewer.mjs"), "// fixture\n");
    fs.symlinkSync(outside, path.join(linkParent, "viewer"));
    const inspected = inspectRuntimeCandidates(root);
    assert.equal(inspected.valid.length, 1);
    assert.ok(inspected.rejected.some((item) => item.reason.includes("escapes")));
    assert.ok(inspected.rejected.some((item) => item.reason.includes("SemVer")));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
    fs.rmSync(outside, { recursive: true, force: true });
  }
});

test("state classification uses contract precedence", () => {
  assert.equal(classifyState({ misconfigured: true, blocked: true }), "misconfigured");
  assert.equal(classifyState({ blocked: true, enabled: true, loaded: true, ready: true }), "blocked");
  assert.equal(classifyState({ enabled: true, loaded: true, ready: true }), "running");
  assert.equal(classifyState({ loaded: true }), "starting");
  assert.equal(classifyState({ disabled: true }), "disabled");
  assert.equal(classifyState({}), "stopped");
});

test("workspace and file URLs are encoded and traversal is rejected", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-url-"));
  const workspace = path.join(parent, "space here");
  const outside = path.join(parent, "outside.step");
  try {
    fs.mkdirSync(path.join(workspace, "nested"), { recursive: true });
    fs.writeFileSync(path.join(workspace, "nested", "part name.step.py"), "# fixture\n");
    fs.writeFileSync(outside, "fixture\n");
    const url = encodedWorkspaceUrl("http://127.0.0.1:3245", workspace, "nested/part name.step.py");
    assert.match(url, /space%20here/);
    assert.match(url, /file=nested%2Fpart%20name.step.py$/);
    assert.throws(() => encodedWorkspaceUrl("http://127.0.0.1:3245", workspace, "../outside.step"), /escapes/);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("plist rendering escapes values and resolves every placeholder", () => {
  const template = "<string>@@VALUE@@</string><string>@@SECOND@@</string>";
  assert.equal(renderPlist(template, { VALUE: "a&b", SECOND: "<x>" }), "<string>a&amp;b</string><string>&lt;x&gt;</string>");
  assert.throws(() => renderPlist("@@MISSING@@", {}), /unresolved/);
});

test("checked-in plist template renders to a plutil-valid fixture", () => {
  const templatePath = new URL("../payload/launchd/com.scottchu.cad-viewer.plist.template", import.meta.url);
  const template = fs.readFileSync(templatePath, "utf8");
  const rendered = renderPlist(template, {
    LABEL: "com.scottchu.cad-viewer",
    NODE: "/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node",
    LAUNCHER: "/Users/scottchu/Library/Application Support/CADViewer/service/current/launch-viewer.mjs",
    STDOUT_LOG: "/Users/scottchu/Library/Logs/CADViewer/stdout.log",
    STDERR_LOG: "/Users/scottchu/Library/Logs/CADViewer/stderr.log",
  });
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-plist-"));
  const fixture = path.join(directory, "service.plist");
  try {
    fs.writeFileSync(fixture, rendered);
    const lint = spawnSync("/usr/bin/plutil", ["-lint", fixture], { encoding: "utf8" });
    assert.equal(lint.status, 0, lint.stderr || lint.stdout);
    assert.doesNotMatch(rendered, /cad\/\d+\.\d+\.\d+/);
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test("service source has no Homebrew Python fallback or pinned Viewer runtime", () => {
  const sourcePaths = [
    new URL("../payload/config.mjs", import.meta.url),
    new URL("../payload/cli.mjs", import.meta.url),
    new URL("../payload/launch-viewer.mjs", import.meta.url),
    new URL("../bin/cad-viewer", import.meta.url),
  ];
  const source = sourcePaths.map((sourcePath) => fs.readFileSync(sourcePath, "utf8")).join("\n");
  assert.doesNotMatch(source, /\/opt\/homebrew|cad\/\d+\.\d+\.\d+/);
  assert.match(source, /\.venv\/bin\/python3/);
  assert.match(source, /VIEWER_CAD_PYTHON/);
});

test("CLI parser supports the documented shell and JSON interface", () => {
  const status = parseArguments(["status", "--json"]);
  assert.equal(status.command, "status");
  assert.equal(status.json, true);
  const logs = parseArguments(["logs", "--lines", "25", "-f"]);
  assert.equal(logs.command, "logs");
  assert.equal(logs.lines, 25);
  assert.equal(logs.follow, true);
  const url = parseArguments(["url", "--workspace", "/tmp", "--local"]);
  assert.equal(url.command, "url");
  assert.equal(url.workspace, "/tmp");
  assert.equal(url.localOnly, true);
  assert.throws(() => parseArguments(["url", "--local", "--tailscale"]), /mutually exclusive/);
});

test("copied stable shim invokes CLI through symlinked current release path", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-stable-shim-"));
  try {
    const release = path.join(parent, "service", "releases", "fixture");
    fs.mkdirSync(release, { recursive: true });
    for (const module of ["cli.mjs", "config.mjs", "core.mjs", "install.mjs"]) {
      fs.copyFileSync(new URL(`../payload/${module}`, import.meta.url), path.join(release, module));
    }
    const current = path.join(parent, "service", "current");
    fs.symlinkSync("releases/fixture", current);
    const sourceShim = fs.readFileSync(new URL("../payload/bin/cad-viewer", import.meta.url), "utf8");
    const shim = path.join(parent, "bin", "cad-viewer");
    fs.mkdirSync(path.dirname(shim), { recursive: true });
    fs.writeFileSync(
      shim,
      sourceShim.replace(
        "/Users/scottchu/Library/Application Support/CADViewer/service/current/cli.mjs",
        `${current}/cli.mjs`,
      ),
      { mode: 0o755 },
    );
    fs.chmodSync(shim, 0o755);
    const result = spawnSync("/bin/zsh", [shim, "help", "--json"], { encoding: "utf8" });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(result.stdout).command, "help");
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});
