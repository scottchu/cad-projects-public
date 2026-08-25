import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import net from "node:net";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { CONFIG } from "../payload/config.mjs";
import { selectViewerRuntime } from "../payload/core.mjs";
import {
  UnsafeOwnershipError,
  checkViewerHealth,
  drainOwnedViewerGroup,
  inspectProcess,
  launchOwnedProcessGroup,
  launchViewerGroup,
  listListeningPids,
  listProcessGroup,
  superviseOwnedViewer,
} from "../payload/launch-viewer.mjs";

const FIXTURE = new URL("./anchor-fixture.mjs", import.meta.url).pathname;
const LAUNCHER = new URL("../payload/launch-viewer.mjs", import.meta.url).pathname;

function makeRuntime(cache, name, version) {
  const root = path.join(cache, name, "skills", "cad-viewer", "scripts", "viewer");
  fs.mkdirSync(path.join(root, "scripts"), { recursive: true });
  fs.writeFileSync(path.join(root, "package.json"), JSON.stringify({ version, scripts: { start: "node scripts/start-viewer.mjs" } }));
  fs.writeFileSync(path.join(root, "scripts", "start-viewer.mjs"), "// fixture\n");
  return fs.realpathSync(root);
}

async function freePort() {
  const server = net.createServer();
  await new Promise((resolve, reject) => server.once("error", reject).listen(0, "127.0.0.1", resolve));
  const { port } = server.address();
  await new Promise((resolve) => server.close(resolve));
  return port;
}

async function waitForHealth(port, ready, timeoutMs = 15000) {
  const deadline = Date.now() + timeoutMs;
  let health;
  while (Date.now() < deadline) {
    health = await checkViewerHealth({ host: "127.0.0.1", port, timeout: 300 });
    if (health.ready === ready) return health;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error(`fixture health did not become ${ready ? "ready" : "unready"}: ${JSON.stringify(health)}`);
}

async function waitFor(predicate, timeoutMs, description) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (predicate()) return;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error(`timed out waiting for ${description}`);
}

function launchFixtureGroup(port, modeFile, { ignoreTerm = false } = {}) {
  const args = [FIXTURE, "--role", "parent", "--port", String(port), "--mode-file", modeFile];
  if (ignoreTerm) args.push("--ignore-term");
  return launchOwnedProcessGroup({
    executable: process.execPath,
    args,
    cwd: path.dirname(FIXTURE),
    env: { ...process.env },
    port,
    handshakeTimeoutMs: 2000,
  });
}

async function cleanupGroup(group) {
  if (!group || group.anchorExitObserver.isSettled()) return;
  try {
    await drainOwnedViewerGroup(group, { termTimeoutMs: 300, finalTimeoutMs: 1000, pollMs: 20, canExitBlocked: () => true });
  } catch {
    // A failing test retains its primary assertion. The reviewer-owned anchor
    // emergency drain also runs when the test process closes its IPC channel.
  }
}

async function startForeignFixture(port, modeFile) {
  const child = spawn(process.execPath, [FIXTURE, "--role", "backend", "--port", String(port), "--mode-file", modeFile], { stdio: "inherit" });
  await waitForHealth(port, true, 3000);
  return child;
}

async function stopForeignFixture(child) {
  if (!child || child.exitCode !== null || child.signalCode !== null) return;
  child.kill("SIGTERM");
  await new Promise((resolve) => child.once("exit", resolve));
}

test("resolver turnover selects a newly available higher stable runtime", () => {
  const cache = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-turnover-"));
  try {
    const oldPath = makeRuntime(cache, "0.4.25", "0.4.25");
    assert.equal(selectViewerRuntime(cache).path, oldPath);
    const newPath = makeRuntime(cache, "0.4.26", "0.4.26");
    fs.rmSync(path.join(cache, "0.4.25"), { recursive: true, force: true });
    assert.equal(selectViewerRuntime(cache).path, newPath);
  } finally {
    fs.rmSync(cache, { recursive: true, force: true });
  }
});

test("anchored runtime turnover drains the full group before a replacement", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-anchored-turnover-"));
  const cache = path.join(root, "cache");
  const modeFile = path.join(root, "mode");
  const port = await freePort();
  fs.writeFileSync(modeFile, "200");
  makeRuntime(cache, "0.4.25", "0.4.25");
  const initialRuntime = selectViewerRuntime(cache);
  const unrelated = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"], { stdio: "ignore" });
  let group;
  let replacement;
  const samples = [];
  let sampler;
  try {
    group = await launchFixtureGroup(port, modeFile);
    await waitForHealth(port, true);
    sampler = setInterval(() => samples.push(listListeningPids(port)), 10);
    const supervision = superviseOwnedViewer({
      group,
      initialRuntime,
      selectRuntime: () => selectViewerRuntime(cache),
      healthCheck: () => checkViewerHealth({ host: "127.0.0.1", port, timeout: 200 }),
      intervalMs: 30,
      startupTimeoutMs: 500,
      drainOptions: { termTimeoutMs: 500, finalTimeoutMs: 1000, pollMs: 20 },
      log: () => {},
    });
    await new Promise((resolve) => setTimeout(resolve, 70));
    makeRuntime(cache, "0.4.26", "0.4.26");
    fs.rmSync(path.join(cache, "0.4.25"), { recursive: true, force: true });
    const outcome = await supervision;
    assert.equal(outcome.kind, "refresh");
    assert.deepEqual(outcome.drained.signals, ["SIGTERM"]);
    assert.equal(listProcessGroup(group.pgid).length, 0);
    assert.deepEqual(listListeningPids(port), []);
    assert.equal(unrelated.exitCode, null, "unrelated process must remain alive");

    replacement = await launchFixtureGroup(port, modeFile);
    await waitForHealth(port, true);
    samples.push(listListeningPids(port));
    assert.ok(samples.every((pids) => new Set(pids).size <= 1), "listener samples must never overlap");
  } finally {
    if (sampler) clearInterval(sampler);
    await cleanupGroup(replacement);
    await cleanupGroup(group);
    await stopForeignFixture(unrelated);
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("two SPA failures use the anchored group drain while the API stays healthy", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-anchored-spa-"));
  const cache = path.join(root, "cache");
  const modeFile = path.join(root, "mode");
  const port = await freePort();
  fs.writeFileSync(modeFile, "200");
  makeRuntime(cache, "0.4.26", "0.4.26");
  const runtime = selectViewerRuntime(cache);
  let group;
  try {
    group = await launchFixtureGroup(port, modeFile);
    await waitForHealth(port, true);
    let checks = 0;
    const outcome = await superviseOwnedViewer({
      group,
      initialRuntime: runtime,
      selectRuntime: () => selectViewerRuntime(cache),
      healthCheck: async () => {
        checks += 1;
        if (checks === 2) fs.writeFileSync(modeFile, "404");
        return checkViewerHealth({ host: "127.0.0.1", port, timeout: 200 });
      },
      intervalMs: 20,
      startupTimeoutMs: 500,
      drainOptions: { termTimeoutMs: 500, finalTimeoutMs: 1000, pollMs: 20 },
      log: () => {},
    });
    assert.equal(outcome.kind, "refresh");
    assert.match(outcome.reason, /two consecutive health failures/);
    assert.ok(checks >= 3);
    assert.equal(listProcessGroup(group.pgid).length, 0);
    assert.deepEqual(listListeningPids(port), []);
  } finally {
    await cleanupGroup(group);
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("stubborn descendants get one KILL and failed provenance gets no group signal", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-anchor-safety-"));
  const modeFile = path.join(root, "mode");
  fs.writeFileSync(modeFile, "200");
  const stubbornPort = await freePort();
  const negativePort = await freePort();
  const unrelated = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"], { stdio: "ignore" });
  let stubborn;
  let negative;
  try {
    stubborn = await launchFixtureGroup(stubbornPort, modeFile, { ignoreTerm: true });
    await waitForHealth(stubbornPort, true);
    const killed = await drainOwnedViewerGroup(stubborn, { termTimeoutMs: 120, finalTimeoutMs: 1000, pollMs: 20 });
    assert.deepEqual(killed.signals, ["SIGTERM", "SIGKILL"]);
    assert.equal(listProcessGroup(stubborn.pgid).length, 0);
    assert.deepEqual(listListeningPids(stubbornPort), []);
    assert.equal(unrelated.exitCode, null);

    negative = await launchFixtureGroup(negativePort, modeFile);
    await waitForHealth(negativePort, true);
    const forged = { ...negative, startEvidence: "forged start evidence", drainPromise: null };
    await assert.rejects(
      drainOwnedViewerGroup(forged, { termTimeoutMs: 100, finalTimeoutMs: 500, pollMs: 20 }),
      UnsafeOwnershipError,
    );
    assert.equal((await checkViewerHealth({ host: "127.0.0.1", port: negativePort })).ready, true, "failed proof must not signal the group");
    assert.ok(listProcessGroup(negative.pgid).length >= 2);
  } finally {
    await cleanupGroup(negative);
    await cleanupGroup(stubborn);
    await stopForeignFixture(unrelated);
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("a foreign port acquired after drain is observed but never signaled or adopted", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-anchor-foreign-"));
  const modeFile = path.join(root, "mode");
  fs.writeFileSync(modeFile, "200");
  const port = await freePort();
  let group;
  let foreign;
  let foreignStayedAlive = false;
  try {
    group = await launchFixtureGroup(port, modeFile);
    await waitForHealth(port, true);
    const drained = await drainOwnedViewerGroup(group, {
      termTimeoutMs: 500,
      finalTimeoutMs: 1000,
      pollMs: 20,
      onGroupAbsent: async () => {
        foreign = await startForeignFixture(port, modeFile);
        setTimeout(() => {
          foreignStayedAlive = foreign.exitCode === null;
          foreign.kill("SIGTERM");
        }, 120);
      },
    });
    assert.equal(foreignStayedAlive, true, "foreign listener must survive the owned group drain");
    assert.deepEqual(drained.signals, ["SIGTERM"]);
    assert.deepEqual(listListeningPids(port), []);
  } finally {
    await stopForeignFixture(foreign);
    await cleanupGroup(group);
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("an external lifecycle signal uses the same anchored drain before propagation", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-anchor-signal-"));
  const modeFile = path.join(root, "mode");
  fs.writeFileSync(modeFile, "200");
  const port = await freePort();
  const runtime = { path: "/reviewer/runtime", version: "1.0.0" };
  let group;
  let signal = null;
  let requestShutdown;
  const shutdownRequest = new Promise((resolve) => { requestShutdown = resolve; });
  try {
    group = await launchFixtureGroup(port, modeFile);
    await waitForHealth(port, true);
    const supervision = superviseOwnedViewer({
      group,
      initialRuntime: runtime,
      selectRuntime: () => runtime,
      healthCheck: () => checkViewerHealth({ host: "127.0.0.1", port, timeout: 200 }),
      shutdownRequest,
      shutdownSignal: () => signal,
      intervalMs: 30,
      startupTimeoutMs: 500,
      drainOptions: { termTimeoutMs: 500, finalTimeoutMs: 1000, pollMs: 20 },
      log: () => {},
    });
    signal = "SIGTERM";
    requestShutdown(signal);
    const outcome = await supervision;
    assert.equal(outcome.kind, "signal");
    assert.equal(outcome.signal, "SIGTERM");
    assert.deepEqual(outcome.drained.signals, ["SIGTERM"]);
    assert.equal(listProcessGroup(group.pgid).length, 0);
    assert.deepEqual(listListeningPids(port), []);
  } finally {
    await cleanupGroup(group);
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("abrupt parent death disconnects IPC and the anchor emergency-drains its group", { timeout: 10000 }, async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-anchor-crash-"));
  const modeFile = path.join(root, "mode");
  fs.writeFileSync(modeFile, "200");
  const port = await freePort();
  const driver = spawn(process.execPath, [
    FIXTURE, "--role", "driver", "--launcher", LAUNCHER,
    "--port", String(port), "--mode-file", modeFile,
  ], { stdio: ["ignore", "pipe", "inherit"] });
  let ownership = null;
  try {
    ownership = await new Promise((resolve, reject) => {
      let output = "";
      driver.stdout.on("data", (chunk) => {
        output += chunk;
        const line = output.split("\n").find((item) => item.startsWith("{"));
        if (line) resolve(JSON.parse(line));
      });
      driver.once("error", reject);
      driver.once("exit", (code, signal) => reject(new Error(`crash driver exited before ownership (${code ?? signal})`)));
    });
    await waitForHealth(port, true);
    assert.equal(inspectProcess(ownership.anchorPid).startEvidence, ownership.startEvidence);
    driver.kill("SIGKILL");
    await new Promise((resolve) => driver.once("exit", resolve));
    await waitFor(() => listProcessGroup(ownership.pgid).length === 0, 7000, "emergency group drain");
    await waitFor(() => listListeningPids(port).length === 0, 1000, "emergency port release");
  } finally {
    if (driver.exitCode === null && driver.signalCode === null) {
      driver.kill("SIGKILL");
      await new Promise((resolve) => driver.once("exit", resolve));
    }
    if (ownership) {
      const anchor = inspectProcess(ownership.anchorPid);
      if (anchor && anchor.pgid === ownership.pgid && anchor.startEvidence === ownership.startEvidence) {
        process.kill(-ownership.pgid, "SIGKILL");
      }
    }
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("real bundled npm and canonical Python topology stays inside the anchor PGID and fully drains", { timeout: 45000 }, async () => {
  const runtime = selectViewerRuntime(CONFIG.cacheRoot);
  const port = await freePort();
  let group;
  let replacement;
  const samples = [];
  let sampler;
  try {
    group = await launchViewerGroup({ runtime, host: "127.0.0.1", port });
    const health = await waitForHealth(port, true, 15000);
    const members = listProcessGroup(group.pgid);
    const parentEvidence = inspectProcess(process.pid);
    assert.notEqual(parentEvidence.pgid, group.pgid, "test parent must remain outside the owned group");
    assert.ok(members.length >= 4, `expected anchor/npm/Node/Python topology, got ${JSON.stringify(members)}`);
    assert.ok(members.every((member) => member.pgid === group.pgid));
    assert.ok(members.some((member) => member.pid === group.npmPid));
    assert.ok(members.some((member) => member.pid === health.server.payload.pid), "API backend PID must belong to the anchor group");
    assert.ok(members.some((member) => member.command.includes("start-viewer.mjs")), "Node start shim must belong to the anchor group");
    const pythonMembers = members.filter((member) => member.command.includes(CONFIG.canonicalPython));
    assert.ok(pythonMembers.length >= 2, `expected canonical Python launcher and backend, got ${JSON.stringify(members)}`);

    let preferred = runtime;
    sampler = setInterval(() => samples.push(listListeningPids(port)), 10);
    const supervision = superviseOwnedViewer({
      group,
      initialRuntime: runtime,
      selectRuntime: () => preferred,
      healthCheck: () => checkViewerHealth({ host: "127.0.0.1", port, timeout: 300 }),
      intervalMs: 30,
      startupTimeoutMs: 1000,
      drainOptions: { termTimeoutMs: 5000, finalTimeoutMs: 5000, pollMs: 50 },
      log: () => {},
    });
    await new Promise((resolve) => setTimeout(resolve, 80));
    preferred = { path: `${runtime.path}-reviewer-refresh`, version: "999.0.0" };
    const outcome = await supervision;
    assert.equal(outcome.kind, "refresh");
    assert.equal(outcome.code, 75);
    assert.equal(listProcessGroup(group.pgid).length, 0, "real old group must be absent before replacement");
    assert.deepEqual(listListeningPids(port), [], "real Python backend must release the reviewer port");

    replacement = await launchViewerGroup({ runtime, host: "127.0.0.1", port });
    await waitForHealth(port, true, 15000);
    samples.push(listListeningPids(port));
    assert.ok(samples.every((pids) => new Set(pids).size <= 1), "real listener samples must never overlap");
  } finally {
    if (sampler) clearInterval(sampler);
    await cleanupGroup(replacement);
    await cleanupGroup(group);
  }
});
