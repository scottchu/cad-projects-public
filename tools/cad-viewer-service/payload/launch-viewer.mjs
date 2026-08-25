import { spawn, spawnSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { CONFIG, guiDomain } from "./config.mjs";
import { evaluateViewerHealth, selectViewerRuntime } from "./core.mjs";

const PS = "/bin/ps";
const LSOF = "/usr/sbin/lsof";
const LAUNCHCTL = "/bin/launchctl";
const INTERNAL_ANCHOR_MODE = "--internal-owned-group-anchor";
const LAUNCHER_PATH = fileURLToPath(import.meta.url);

export class UnsafeOwnershipError extends Error {
  constructor(message) {
    super(message);
    this.name = "UnsafeOwnershipError";
  }
}

function requireExecutable(executable, name) {
  try {
    fs.accessSync(executable, fs.constants.X_OK);
  } catch {
    throw new Error(`${name} is missing or not executable at ${executable}`);
  }
}

function validatePython() {
  try {
    requireExecutable(CONFIG.canonicalPython, "Canonical uv Python");
  } catch (error) {
    throw new Error(`${error.message}. Repair it with \`uv sync --all-packages --all-groups\` from /Users/scottchu/Projects/personal/design-projects; do not create another venv`);
  }
  const check = spawnSync(CONFIG.canonicalPython, ["-c", "import json,sys; print(json.dumps({'major':sys.version_info.major,'minor':sys.version_info.minor}))"], {
    encoding: "utf8",
    env: { PATH: CONFIG.safePath },
  });
  if (check.status !== 0) throw new Error(`Canonical uv Python failed: ${(check.stderr || check.stdout).trim()}`);
  const version = JSON.parse(check.stdout);
  if (version.major !== 3 || version.minor !== 12) {
    throw new Error(`Canonical uv Python must report Python 3.12, got ${version.major}.${version.minor}`);
  }
}

function writeJsonAtomic(destination, value) {
  fs.mkdirSync(path.dirname(destination), { recursive: true, mode: 0o700 });
  fs.chmodSync(path.dirname(destination), 0o700);
  const temporary = `${destination}.tmp-${process.pid}`;
  try { fs.unlinkSync(temporary); } catch (error) { if (error.code !== "ENOENT") throw error; }
  fs.writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600, flag: "wx" });
  fs.renameSync(temporary, destination);
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function request(pathname, { host, port, timeout }) {
  return new Promise((resolve) => {
    const req = http.get({ host, port, path: pathname, timeout }, (response) => {
      let body = "";
      response.setEncoding("utf8");
      response.on("data", (chunk) => { body += chunk; });
      response.on("end", () => resolve({ status: response.statusCode, body, error: null }));
    });
    req.on("timeout", () => req.destroy(new Error("timeout")));
    req.on("error", (error) => resolve({ status: null, body: "", error: error.message }));
  });
}

// Test-only dependency injection is supported by these exported internals. The
// production entry point always supplies the frozen CONFIG paths and port.
export async function checkViewerHealth({ host, port, timeout = 800 }) {
  const [page, serverResponse] = await Promise.all([
    request("/", { host, port, timeout }),
    request("/__cad/server", { host, port, timeout }),
  ]);
  let payload = null;
  let serverError = serverResponse.error;
  if (!serverError && serverResponse.status !== null) {
    try { payload = JSON.parse(serverResponse.body); }
    catch (error) { serverError = `invalid JSON: ${error.message}`; }
  }
  const server = { status: serverResponse.status, payload, error: serverError };
  const result = evaluateViewerHealth(page, server, port);
  return { ...result, page, server };
}

export function inspectProcess(pid) {
  if (!Number.isInteger(pid) || pid < 2) throw new UnsafeOwnershipError(`invalid process PID ${pid}`);
  const result = spawnSync(PS, ["-o", "pid=,pgid=,lstart=", "-p", String(pid)], { encoding: "utf8" });
  if (result.error) throw new UnsafeOwnershipError(`ps failed for PID ${pid}: ${result.error.message}`);
  if (result.status !== 0 || !result.stdout.trim()) return null;
  const match = /^\s*(\d+)\s+(\d+)\s+(.+?)\s*$/.exec(result.stdout);
  if (!match) throw new UnsafeOwnershipError(`cannot parse process evidence for PID ${pid}`);
  return { pid: Number(match[1]), pgid: Number(match[2]), startEvidence: match[3].replace(/\s+/g, " ") };
}

export function listProcessGroup(pgid) {
  if (!Number.isInteger(pgid) || pgid < 2) throw new UnsafeOwnershipError(`invalid process group ${pgid}`);
  const result = spawnSync(PS, ["-axo", "pid=,pgid=,ppid=,command="], { encoding: "utf8" });
  if (result.error || result.status !== 0) {
    throw new UnsafeOwnershipError(`cannot inspect process group ${pgid}: ${result.error?.message ?? result.stderr.trim()}`);
  }
  const members = [];
  for (const line of result.stdout.split("\n")) {
    const match = /^\s*(\d+)\s+(\d+)\s+(\d+)\s+(.*)$/.exec(line);
    if (match && Number(match[2]) === pgid) {
      members.push({ pid: Number(match[1]), pgid: Number(match[2]), ppid: Number(match[3]), command: match[4] });
    }
  }
  return members;
}

export function listListeningPids(port) {
  const result = spawnSync(LSOF, ["-nP", `-iTCP:${port}`, "-sTCP:LISTEN", "-Fp"], { encoding: "utf8" });
  if (result.error) throw new UnsafeOwnershipError(`lsof failed for port ${port}: ${result.error.message}`);
  if (result.status === 1) return [];
  if (result.status !== 0) throw new UnsafeOwnershipError(`lsof failed for port ${port}: ${result.stderr.trim() || `exit ${result.status}`}`);
  return result.stdout.split("\n").filter((line) => /^p\d+$/.test(line)).map((line) => Number(line.slice(1)));
}

function childExitObserver(child) {
  let settled = child.exitCode !== null || child.signalCode !== null;
  let value = settled ? { code: child.exitCode ?? 1, signal: child.signalCode, error: null } : null;
  let resolveExit;
  const promise = new Promise((resolve) => {
    resolveExit = resolve;
    if (settled) resolve(value);
  });
  const finish = (next) => {
    if (settled) return;
    settled = true;
    value = next;
    resolveExit(next);
  };
  child.once("error", (error) => finish({ code: 1, signal: null, error }));
  child.once("exit", (code, signal) => finish({ code: code ?? 1, signal, error: null }));
  return { promise, isSettled: () => settled, value: () => value };
}

function waitForIpc(child, predicate, timeoutMs, description) {
  return new Promise((resolve, reject) => {
    let timer;
    const cleanup = () => {
      clearTimeout(timer);
      child.off("message", onMessage);
      child.off("error", onError);
      child.off("exit", onExit);
    };
    const onMessage = (message) => {
      if (!predicate(message)) return;
      cleanup();
      resolve(message);
    };
    const onError = (error) => { cleanup(); reject(error); };
    const onExit = (code, signal) => { cleanup(); reject(new Error(`anchor exited before ${description} (${code ?? signal})`)); };
    child.on("message", onMessage);
    child.once("error", onError);
    child.once("exit", onExit);
    timer = setTimeout(() => { cleanup(); reject(new Error(`timed out waiting for ${description}`)); }, timeoutMs);
  });
}

function proveAnchor(group) {
  if (group.anchor !== group.frozenAnchorHandle) throw new UnsafeOwnershipError("anchor ChildProcess identity changed");
  if (group.anchor.exitCode !== null || group.anchor.signalCode !== null || !group.anchor.connected) {
    throw new UnsafeOwnershipError("owned anchor is no longer live on its original IPC channel");
  }
  const observed = inspectProcess(group.anchorPid);
  if (!observed) throw new UnsafeOwnershipError("owned anchor disappeared before group signal");
  if (observed.pid !== group.anchorPid || observed.pgid !== group.anchorPid || observed.startEvidence !== group.startEvidence) {
    throw new UnsafeOwnershipError("owned anchor PID, PGID, or process-start evidence changed");
  }
  return observed;
}

function groupSnapshot(group) {
  const members = listProcessGroup(group.pgid);
  const listeners = listListeningPids(group.port);
  const memberPids = new Set(members.map((member) => member.pid));
  return {
    members,
    listeners,
    groupListeners: listeners.filter((pid) => memberPids.has(pid)),
  };
}

async function waitForChildExit(observer, timeoutMs) {
  const timeout = Symbol("timeout");
  const result = await Promise.race([observer.promise, delay(timeoutMs).then(() => timeout)]);
  if (result === timeout) throw new UnsafeOwnershipError("owned anchor did not exit within the final quiescence window");
  return result;
}

async function waitForGroupAbsent(group, timeoutMs, pollMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (listProcessGroup(group.pgid).length === 0) return true;
    await delay(pollMs);
  }
  return listProcessGroup(group.pgid).length === 0;
}

async function waitForPortAfterDrain(group, { pollMs, canExitBlocked, onGroupAbsent }) {
  if (onGroupAbsent) await onGroupAbsent();
  while (true) {
    const listeners = listListeningPids(group.port);
    if (!listeners.length) return { blockedPort: false, portOwners: [] };
    if (canExitBlocked?.()) return { blockedPort: true, portOwners: listeners };
    await delay(pollMs);
  }
}

export async function drainOwnedViewerGroup(group, {
  termTimeoutMs = CONFIG.groupTermTimeoutMs,
  finalTimeoutMs = CONFIG.groupFinalTimeoutMs,
  pollMs = CONFIG.groupPollMs,
  canExitBlocked = () => false,
  onGroupAbsent = null,
} = {}) {
  if (group.drainPromise) return group.drainPromise;
  group.drainPromise = (async () => {
    const signals = [];
    proveAnchor(group);
    process.kill(-group.pgid, "SIGTERM");
    signals.push("SIGTERM");

    const termDeadline = Date.now() + termTimeoutMs;
    let graceful = false;
    while (Date.now() < termDeadline) {
      const snapshot = groupSnapshot(group);
      if (snapshot.members.length === 1 && snapshot.members[0].pid === group.anchorPid && snapshot.groupListeners.length === 0) {
        graceful = true;
        break;
      }
      await delay(pollMs);
    }

    if (graceful) {
      if (!group.anchor.connected) throw new UnsafeOwnershipError("anchor IPC vanished before final release");
      group.anchor.send({ type: "release", nonce: group.nonce });
      await waitForChildExit(group.anchorExitObserver, finalTimeoutMs);
      if (!await waitForGroupAbsent(group, finalTimeoutMs, pollMs)) {
        throw new UnsafeOwnershipError("owned process group remained after graceful anchor release");
      }
    } else {
      proveAnchor(group);
      process.kill(-group.pgid, "SIGKILL");
      signals.push("SIGKILL");
      if (!await waitForGroupAbsent(group, finalTimeoutMs, pollMs)) {
        throw new UnsafeOwnershipError("owned process group remained after its one permitted SIGKILL");
      }
    }

    const port = await waitForPortAfterDrain(group, { pollMs, canExitBlocked, onGroupAbsent });
    return { signals, escalated: signals.includes("SIGKILL"), ...port };
  })();
  return group.drainPromise;
}

function anchorSend(message) {
  if (process.connected && process.send) process.send(message);
}

async function emergencyAnchorDrain(port) {
  try { process.kill(-process.pid, "SIGTERM"); } catch { process.exit(1); }
  const deadline = Date.now() + CONFIG.groupTermTimeoutMs;
  while (Date.now() < deadline) {
    try {
      const members = listProcessGroup(process.pid);
      const listeners = listListeningPids(port);
      const memberPids = new Set(members.map((member) => member.pid));
      if (members.length === 1 && members[0].pid === process.pid && !listeners.some((pid) => memberPids.has(pid))) process.exit(1);
    } catch {
      break;
    }
    await delay(CONFIG.groupPollMs);
  }
  process.kill(-process.pid, "SIGKILL");
}

async function runAnchor(nonce) {
  if (!process.send || !process.connected || !nonce) process.exit(2);
  const evidence = inspectProcess(process.pid);
  if (!evidence || evidence.pgid !== process.pid) process.exit(2);
  let started = false;
  let releasing = false;
  let port = null;
  for (const signal of ["SIGTERM", "SIGINT", "SIGHUP"]) process.on(signal, () => {});
  process.on("message", (message) => {
    if (!message || message.nonce !== nonce) return;
    if (message.type === "start" && !started) {
      started = true;
      port = message.port;
      const child = spawn(message.executable, message.args, {
        cwd: message.cwd,
        env: message.env,
        detached: false,
        stdio: "inherit",
      });
      child.once("spawn", () => anchorSend({ type: "worker-started", nonce, pid: child.pid }));
      child.once("error", (error) => anchorSend({ type: "worker-error", nonce, error: error.message }));
      child.once("exit", (code, signal) => anchorSend({ type: "worker-exit", nonce, code, signal }));
    } else if (message.type === "release") {
      releasing = true;
      process.disconnect();
      process.exit(0);
    }
  });
  process.on("disconnect", () => {
    if (!releasing) void emergencyAnchorDrain(port);
  });
  anchorSend({ type: "anchor-ready", nonce, pid: process.pid, pgid: evidence.pgid, startEvidence: evidence.startEvidence });
}

export async function launchOwnedProcessGroup({
  executable,
  args,
  cwd,
  env,
  port,
  node = CONFIG.node,
  launcherPath = LAUNCHER_PATH,
  handshakeTimeoutMs = CONFIG.anchorHandshakeTimeoutMs,
}) {
  const nonce = randomBytes(32).toString("hex");
  const anchor = spawn(node, [launcherPath, INTERNAL_ANCHOR_MODE, nonce], {
    detached: true,
    stdio: ["ignore", "inherit", "inherit", "ipc"],
    env: { ...process.env, PATH: CONFIG.safePath },
  });
  const anchorExitObserver = childExitObserver(anchor);
  let ready;
  try {
    ready = await waitForIpc(anchor, (message) => message?.type === "anchor-ready" && message.nonce === nonce, handshakeTimeoutMs, "anchor ownership handshake");
  } catch (error) {
    if (!anchorExitObserver.isSettled()) anchor.kill("SIGKILL");
    await anchorExitObserver.promise;
    throw error;
  }
  const observed = inspectProcess(anchor.pid);
  if (!observed
    || ready.pid !== anchor.pid
    || ready.pgid !== anchor.pid
    || ready.startEvidence !== observed.startEvidence
    || observed.pgid !== anchor.pid) {
    anchor.kill("SIGKILL");
    await anchorExitObserver.promise;
    throw new UnsafeOwnershipError("detached anchor failed PID, PGID, nonce, or start-evidence verification");
  }

  let npmExitResolve;
  const npmExitPromise = new Promise((resolve) => { npmExitResolve = resolve; });
  const group = {
    anchor,
    frozenAnchorHandle: anchor,
    anchorPid: anchor.pid,
    pgid: anchor.pid,
    startEvidence: observed.startEvidence,
    nonce,
    port,
    anchorExitObserver,
    npmPid: null,
    npmExit: null,
    npmExitPromise,
    drainPromise: null,
  };
  anchor.on("message", (message) => {
    if (!message || message.nonce !== nonce) return;
    if (message.type === "worker-exit" || message.type === "worker-error") {
      group.npmExit = message;
      npmExitResolve(message);
    }
  });

  const workerStarted = waitForIpc(anchor, (message) => message?.nonce === nonce && ["worker-started", "worker-error"].includes(message.type), handshakeTimeoutMs, "owned worker start");
  anchor.send({ type: "start", nonce, executable, args, cwd, env, port });
  let worker;
  try { worker = await workerStarted; }
  catch (error) {
    await drainOwnedViewerGroup(group);
    throw error;
  }
  if (worker.type === "worker-error") {
    await drainOwnedViewerGroup(group);
    throw new Error(`owned worker failed to spawn: ${worker.error}`);
  }
  group.npmPid = worker.pid;
  return group;
}

export function launchViewerGroup({ runtime, host = CONFIG.host, port = CONFIG.port }) {
  return launchOwnedProcessGroup({
    executable: CONFIG.npm,
    args: ["--prefix", runtime.path, "run", "start", "--", "--host", host, "--port", String(port), "--json"],
    cwd: CONFIG.viewerDefaultRoot,
    env: {
      ...process.env,
      PATH: CONFIG.safePath,
      VIEWER_CAD_PYTHON: CONFIG.canonicalPython,
      INIT_CWD: CONFIG.viewerDefaultRoot,
    },
    port,
  });
}

function sameRuntime(left, right) {
  return left?.path === right?.path && left?.version === right?.version;
}

function healthBackendBelongsToGroup(group, health) {
  if (!health.ready) return true;
  return listProcessGroup(group.pgid).some((member) => member.pid === health.server.payload.pid);
}

export async function superviseOwnedViewer({
  group,
  initialRuntime,
  selectRuntime,
  healthCheck,
  shutdownRequest = new Promise(() => {}),
  shutdownSignal = () => null,
  canExitBlocked = () => false,
  intervalMs = CONFIG.supervisorIntervalMs,
  startupTimeoutMs = CONFIG.supervisorStartupTimeoutMs,
  drainOptions = {},
  refreshExitCode = CONFIG.refreshExitCode,
  log = (message) => process.stderr.write(`${message}\n`),
}) {
  const startedAt = Date.now();
  let operational = false;
  let consecutiveHealthFailures = 0;

  const drain = async (kind, reason) => {
    log(`CAD Viewer group drain: ${initialRuntime.version} ${initialRuntime.path}; ${reason}`);
    try {
      const drained = await drainOwnedViewerGroup(group, { ...drainOptions, canExitBlocked });
      const signal = shutdownSignal();
      if (signal) return { kind: "signal", code: 1, signal, reason, drained };
      if (kind === "refresh") return { kind, code: refreshExitCode, signal: null, reason, drained };
      return { kind, code: 1, signal: null, reason, drained };
    } catch (error) {
      return { kind: "unsafe-ownership", code: null, signal: null, reason, error };
    }
  };

  while (true) {
    const tickStartedAt = Date.now();
    if (shutdownSignal()) return drain("signal", `received ${shutdownSignal()}`);
    if (group.anchorExitObserver.isSettled()) {
      return { kind: "unsafe-ownership", code: null, signal: null, reason: "owned anchor exited outside the drain protocol", error: new UnsafeOwnershipError("owned anchor exited outside the drain protocol") };
    }
    if (group.npmExit) return drain("worker-exit", `owned npm worker exited (${group.npmExit.code ?? group.npmExit.signal ?? group.npmExit.error})`);

    let selected;
    try { selected = selectRuntime(); }
    catch (error) { return drain("refresh", `runtime selection failed: ${error.message}`); }
    if (!sameRuntime(selected, initialRuntime)) return drain("refresh", `preferred runtime changed to ${selected.version} ${selected.path}`);

    let health;
    try { health = await healthCheck(); }
    catch (error) { health = { ready: false, errors: [error.message] }; }
    if (health.ready && !healthBackendBelongsToGroup(group, health)) {
      return { kind: "unsafe-ownership", code: null, signal: null, reason: "Viewer backend escaped the owned process group", error: new UnsafeOwnershipError("Viewer backend escaped the owned process group") };
    }
    if (health.ready) {
      operational = true;
      consecutiveHealthFailures = 0;
    } else if (operational) {
      consecutiveHealthFailures += 1;
      if (consecutiveHealthFailures >= 2) return drain("refresh", `two consecutive health failures: ${(health.errors ?? ["unknown health failure"]).join("; ")}`);
    } else if (Date.now() - startedAt >= startupTimeoutMs) {
      return drain("worker-exit", `startup health did not become ready within ${startupTimeoutMs}ms: ${(health.errors ?? ["unknown health failure"]).join("; ")}`);
    }

    const untilNextTick = Math.max(0, intervalMs - (Date.now() - tickStartedAt));
    await Promise.race([delay(untilNextTick), group.npmExitPromise, group.anchorExitObserver.promise, shutdownRequest]);
  }
}

function serviceDisabledOverride() {
  const result = spawnSync(LAUNCHCTL, ["print-disabled", guiDomain()], { encoding: "utf8" });
  if (result.status !== 0) return false;
  const escaped = CONFIG.label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`"${escaped}"\\s*=>\\s*disabled`).test(result.stdout);
}

export async function main() {
  let runtime;
  try {
    requireExecutable(CONFIG.node, "Bundled Node");
    requireExecutable(CONFIG.npm, "Bundled npm");
    validatePython();
    runtime = selectViewerRuntime(CONFIG.cacheRoot);
    writeJsonAtomic(CONFIG.runtimeRecord, {
      path: runtime.path,
      version: runtime.version,
      launchedAt: new Date().toISOString(),
      launcherPid: process.pid,
    });
  } catch (error) {
    process.stderr.write(`CAD Viewer launch preflight failed: ${error.message}\n`);
    return { code: 1, signal: null };
  }

  let group;
  try { group = await launchViewerGroup({ runtime }); }
  catch (error) {
    process.stderr.write(`CAD Viewer owned-group launch failed: ${error.message}\n`);
    return { code: 1, signal: null };
  }

  let requestedSignal = null;
  let resolveShutdown;
  const shutdownRequest = new Promise((resolve) => { resolveShutdown = resolve; });
  for (const signal of ["SIGTERM", "SIGINT", "SIGHUP"]) {
    process.once(signal, () => {
      if (requestedSignal) return;
      requestedSignal = signal;
      resolveShutdown(signal);
    });
  }

  const outcome = await superviseOwnedViewer({
    group,
    initialRuntime: runtime,
    selectRuntime: () => selectViewerRuntime(CONFIG.cacheRoot),
    healthCheck: () => checkViewerHealth({ host: CONFIG.host, port: CONFIG.port }),
    shutdownRequest,
    shutdownSignal: () => requestedSignal,
    canExitBlocked: () => Boolean(requestedSignal && serviceDisabledOverride()),
  });
  for (const signal of ["SIGTERM", "SIGINT", "SIGHUP"]) process.removeAllListeners(signal);
  if (outcome.kind === "unsafe-ownership") {
    process.stderr.write(`CAD Viewer unsafe ownership: ${outcome.error.message}; parent will remain loaded and will not permit a replacement\n`);
    await new Promise(() => {});
  }
  return { code: outcome.code ?? 1, signal: outcome.signal };
}

function isDirectInvocation() {
  if (!process.argv[1]) return false;
  try { return fs.realpathSync(path.resolve(process.argv[1])) === fs.realpathSync(LAUNCHER_PATH); }
  catch { return false; }
}

if (isDirectInvocation()) {
  if (process.argv[2] === INTERNAL_ANCHOR_MODE) await runAnchor(process.argv[3]);
  else {
    const outcome = await main();
    if (outcome.signal) process.kill(process.pid, outcome.signal);
    else process.exitCode = outcome.code;
  }
}
