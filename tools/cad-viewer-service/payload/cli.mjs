import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { CONFIG, guiDomain, legacyTarget, serviceTarget } from "./config.mjs";
import {
  classifyState,
  encodedWorkspaceUrl,
  inspectRuntimeCandidates,
  renderPlist,
  selectViewerRuntime,
} from "./core.mjs";
import {
  acquireInstallLock,
  atomicCopyFile,
  garbageCollect,
  installRelease,
  markLastKnownGood,
  readCurrentHash,
  restoreFile,
  snapshotFile,
  sourceProvenance,
  switchCurrent,
  validatePayload,
  writeInstallHistory,
} from "./install.mjs";

const LAUNCHCTL = "/bin/launchctl";
const PLUTIL = "/usr/bin/plutil";
const LSOF = "/usr/sbin/lsof";
const PS = "/bin/ps";
const TAIL = "/usr/bin/tail";
const LOG_LIMIT = 10 * 1024 * 1024;
const INSTALL_PATHS = Object.freeze({
  releasesDir: CONFIG.releasesDir,
  currentLink: CONFIG.currentLink,
  installHistoryDir: CONFIG.installHistoryDir,
  lastKnownGood: CONFIG.lastKnownGood,
});

function command(executable, args, options = {}) {
  return spawnSync(executable, args, { encoding: "utf8", ...options });
}

function commandError(result, context) {
  return `${context}: ${(result.stderr || result.stdout || `exit ${result.status}`).trim()}`;
}

function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function executable(pathname, name, errors) {
  try {
    fs.accessSync(pathname, fs.constants.X_OK);
  } catch {
    errors.push(`${name} is missing or not executable at ${pathname}`);
  }
}

function expectedPlist(payloadRoot) {
  const template = fs.readFileSync(path.join(payloadRoot, "launchd", "com.scottchu.cad-viewer.plist.template"), "utf8");
  return renderPlist(template, {
    LABEL: CONFIG.label,
    NODE: CONFIG.node,
    LAUNCHER: CONFIG.currentLauncher,
    STDOUT_LOG: CONFIG.stdoutLog,
    STDERR_LOG: CONFIG.stderrLog,
  });
}

function dependencyCheck({ installedState = false, payloadRoot = null } = {}) {
  const errors = [];
  executable(CONFIG.node, "Bundled Node", errors);
  executable(CONFIG.npm, "Bundled npm", errors);
  executable(CONFIG.canonicalPython, "Canonical uv Python", errors);
  if (errors.some((error) => error.startsWith("Canonical uv Python"))) {
    errors.push("Repair it with `uv sync --all-packages --all-groups` from /Users/scottchu/Projects/personal/design-projects; do not create another venv");
  }
  let python = null;
  if (!errors.some((error) => error.startsWith("Canonical uv Python"))) {
    const result = command(CONFIG.canonicalPython, [
      "-c",
      "import json,sys; print(json.dumps({'major':sys.version_info.major,'minor':sys.version_info.minor,'executable':sys.executable}))",
    ], { env: { PATH: CONFIG.safePath } });
    if (result.status !== 0) errors.push(commandError(result, "Canonical uv Python check failed"));
    else {
      try {
        python = JSON.parse(result.stdout);
        if (python.major !== 3 || python.minor !== 12) errors.push(`Canonical uv Python must report Python 3.12, got ${python.major}.${python.minor}`);
      } catch (error) {
        errors.push(`Canonical uv Python returned invalid version data: ${error.message}`);
      }
    }
  }
  let runtime = null;
  try {
    runtime = selectViewerRuntime(CONFIG.cacheRoot);
  } catch (error) {
    errors.push(error.message);
  }
  let plistText = null;
  try {
    if (!payloadRoot) throw new Error("no validated active payload is installed");
    plistText = expectedPlist(payloadRoot);
  } catch (error) {
    errors.push(`LaunchAgent template is unavailable or invalid: ${error.message}`);
  }
  let runtimeRecord = null;
  if (fs.existsSync(CONFIG.runtimeRecord)) {
    try {
      runtimeRecord = JSON.parse(fs.readFileSync(CONFIG.runtimeRecord, "utf8"));
      const candidates = inspectRuntimeCandidates(CONFIG.cacheRoot).valid;
      const match = candidates.find((item) => item.path === runtimeRecord.path && item.version === runtimeRecord.version);
      if (!match) errors.push("runtime.json does not identify a currently valid installed Viewer runtime");
      if (!Number.isInteger(runtimeRecord.launcherPid) || Number.isNaN(Date.parse(runtimeRecord.launchedAt))) {
        errors.push("runtime.json is missing a valid launch time or launcher PID");
      }
    } catch (error) {
      errors.push(`runtime.json is invalid: ${error.message}`);
    }
  }
  if (installedState && fs.existsSync(CONFIG.plist) && plistText !== null) {
    try {
      if (fs.readFileSync(CONFIG.plist, "utf8") !== plistText) errors.push("installed LaunchAgent plist does not match the checked-in contract");
      const lint = command(PLUTIL, ["-lint", CONFIG.plist]);
      if (lint.status !== 0) errors.push(commandError(lint, "installed LaunchAgent plist failed plutil"));
    } catch (error) {
      errors.push(`installed LaunchAgent plist cannot be read: ${error.message}`);
    }
  }
  return { errors, python, runtime, runtimeRecord, plistText };
}

function readJob(target = serviceTarget()) {
  const result = command(LAUNCHCTL, ["print", target]);
  if (result.status !== 0) return { loaded: false, pid: null, output: result.stdout + result.stderr };
  const match = /(?:^|\n)\s*pid\s*=\s*(\d+)/m.exec(result.stdout);
  return { loaded: true, pid: match ? Number(match[1]) : null, output: result.stdout };
}

function disabledOverride() {
  const result = command(LAUNCHCTL, ["print-disabled", guiDomain()]);
  if (result.status !== 0) return { disabled: false, error: commandError(result, "launchctl print-disabled failed") };
  const escaped = CONFIG.label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return { disabled: new RegExp(`"${escaped}"\\s*=>\\s*disabled`).test(result.stdout), error: null };
}

function portOwners() {
  const result = command(LSOF, ["-nP", `-iTCP:${CONFIG.port}`, "-sTCP:LISTEN", "-Fpc"]);
  if (result.status !== 0) return [];
  const owners = [];
  let current = null;
  for (const line of result.stdout.split("\n")) {
    if (line.startsWith("p")) {
      current = { pid: Number(line.slice(1)), command: "unknown" };
      if (Number.isInteger(current.pid)) owners.push(current);
    } else if (line.startsWith("c") && current) current.command = line.slice(1);
  }
  return owners;
}

function parentPid(pid) {
  const result = command(PS, ["-o", "ppid=", "-p", String(pid)]);
  if (result.status !== 0) return null;
  const parsed = Number(result.stdout.trim());
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null;
}

export function pidDescendsFrom(pid, ancestor) {
  if (!Number.isInteger(pid) || !Number.isInteger(ancestor)) return false;
  let current = pid;
  const seen = new Set();
  for (let depth = 0; depth < 64 && current > 1 && !seen.has(current); depth += 1) {
    if (current === ancestor) return true;
    seen.add(current);
    current = parentPid(current);
    if (current === null) return false;
  }
  return current === ancestor;
}

function fetchServer(timeout = 800) {
  return new Promise((resolve) => {
    const request = http.get({ host: CONFIG.host, port: CONFIG.port, path: "/__cad/server", timeout }, (response) => {
      let body = "";
      response.setEncoding("utf8");
      response.on("data", (chunk) => { body += chunk; });
      response.on("end", () => {
        try {
          resolve({ status: response.statusCode, payload: JSON.parse(body), error: null });
        } catch (error) {
          resolve({ status: response.statusCode, payload: null, error: `invalid JSON: ${error.message}` });
        }
      });
    });
    request.on("timeout", () => request.destroy(new Error("timeout")));
    request.on("error", (error) => resolve({ status: null, payload: null, error: error.message }));
  });
}

function activePayload() {
  const hash = readCurrentHash(CONFIG.currentLink);
  if (!hash) return null;
  const payload = validatePayload(path.join(CONFIG.releasesDir, hash));
  if (payload.payloadHash !== hash) throw new Error("active release directory does not match its manifest hash");
  return payload;
}

async function statusFacts(fallbackPayloadRoot = null) {
  let active = null;
  const payloadErrors = [];
  try {
    active = activePayload();
  } catch (error) {
    payloadErrors.push(`active installed payload is invalid: ${error.message}`);
  }
  const dependencies = dependencyCheck({ installedState: true, payloadRoot: active?.root ?? fallbackPayloadRoot });
  dependencies.errors.unshift(...payloadErrors);
  const job = readJob();
  if (!active && (job.loaded || fs.existsSync(CONFIG.plist) || fs.existsSync(CONFIG.commandPath))) {
    dependencies.errors.push("managed service files or job exist without a valid active content-addressed payload");
  }
  if (active) {
    if (!dependencies.runtimeRecord && !job.loaded) dependencies.errors.push("active installed payload has no runtime.json record");
    if (!fs.existsSync(CONFIG.plist)) dependencies.errors.push("active installed payload has no LaunchAgent plist");
    try {
      assertOwnedRegularMatches(CONFIG.commandPath, fs.readFileSync(path.join(active.root, "bin", "cad-viewer")), 0o755);
    } catch (error) {
      dependencies.errors.push(`stable command validation failed: ${error.message}`);
    }
  }
  const disabled = disabledOverride();
  const owners = portOwners();
  const server = owners.length ? await fetchServer() : { status: null, payload: null, error: null };
  const payloadValid = server.status === 200 && server.payload?.app === "cad-viewer" && server.payload?.port === CONFIG.port && Number.isInteger(server.payload?.pid);
  const ready = Boolean(job.loaded && job.pid && payloadValid && pidDescendsFrom(server.payload.pid, job.pid));
  const managedPort = Boolean(job.pid && owners.some((owner) => pidDescendsFrom(owner.pid, job.pid)));
  const foreignPort = owners.length > 0 && !ready && !managedPort;
  const launchedAt = dependencies.runtimeRecord ? Date.parse(dependencies.runtimeRecord.launchedAt) : Number.NaN;
  const startupFresh = Number.isFinite(launchedAt) && Date.now() - launchedAt < 20000;
  const blocked = foreignPort
    || Boolean(job.loaded && managedPort && server.status !== null && !payloadValid)
    || Boolean(job.loaded && !ready && !startupFresh);
  const state = classifyState({
    misconfigured: dependencies.errors.length > 0,
    blocked,
    foreignPort,
    enabled: !disabled.disabled,
    loaded: job.loaded,
    ready,
    disabled: disabled.disabled,
  });
  return { state, dependencies, job, disabled: disabled.disabled, disabledError: disabled.error, owners, server, ready, managedPort, foreignPort };
}

function statusExit(state) {
  if (state === "running") return 0;
  if (state === "stopped" || state === "disabled") return 1;
  return 2;
}

function statusObject(facts) {
  const result = {
    ok: facts.state === "running",
    command: "status",
    state: facts.state,
    enabled: !facts.disabled,
    loaded: facts.job.loaded,
    jobPid: facts.job.pid,
    ready: facts.ready,
    runtime: facts.dependencies.runtimeRecord ?? (facts.dependencies.runtime ? { path: facts.dependencies.runtime.path, version: facts.dependencies.runtime.version } : null),
    portOwners: facts.owners,
    server: facts.server.payload,
    errors: [...facts.dependencies.errors, ...(facts.disabledError ? [facts.disabledError] : [])],
  };
  if (facts.state !== "running") {
    result.logTail = {
      stdout: readLog(CONFIG.stdoutLog, 20),
      stderr: readLog(CONFIG.stderrLog, 20),
    };
  }
  if (facts.foreignPort) result.error = "Port 3245 is occupied by a process outside the managed LaunchAgent";
  else if (facts.state === "blocked") result.error = facts.server.error || "The managed LaunchAgent is loaded but its backend is not ready";
  return result;
}

function ensurePrivateDirectory(directory) {
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  const stat = fs.statSync(directory);
  if (!stat.isDirectory() || stat.uid !== process.getuid()) throw new Error(`State path is not an owned directory: ${directory}`);
  fs.chmodSync(directory, 0o700);
  fs.accessSync(directory, fs.constants.R_OK | fs.constants.W_OK | fs.constants.X_OK);
}

function writeJsonAtomic(destination, value) {
  const temporary = `${destination}.tmp-${process.pid}`;
  fs.writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, { flag: "wx", mode: 0o600 });
  fs.renameSync(temporary, destination);
}

function installStableCommand(payloadRoot) {
  atomicCopyFile(path.join(payloadRoot, "bin", "cad-viewer"), CONFIG.commandPath, 0o755);
}

function installPlist(plistText) {
  ensurePrivateDirectory(path.dirname(CONFIG.plist));
  const temporary = `${CONFIG.plist}.tmp-${process.pid}`;
  fs.writeFileSync(temporary, plistText, { flag: "wx", mode: 0o600 });
  const lint = command(PLUTIL, ["-lint", temporary]);
  if (lint.status !== 0) {
    fs.unlinkSync(temporary);
    throw new Error(commandError(lint, "generated LaunchAgent plist failed plutil"));
  }
  fs.chmodSync(temporary, 0o600);
  fs.renameSync(temporary, CONFIG.plist);
}

function prepareLogs() {
  ensurePrivateDirectory(path.dirname(CONFIG.stdoutLog));
  for (const log of [CONFIG.stdoutLog, CONFIG.stderrLog]) {
    if (fs.existsSync(log) && fs.statSync(log).size > LOG_LIMIT) {
      const rotated = `${log}.1`;
      if (fs.existsSync(rotated)) fs.unlinkSync(rotated);
      fs.renameSync(log, rotated);
      fs.chmodSync(rotated, 0o600);
    }
    const descriptor = fs.openSync(log, "a", 0o600);
    fs.closeSync(descriptor);
    fs.chmodSync(log, 0o600);
  }
  ensurePrivateDirectory(CONFIG.stateDir);
}

async function waitForPortFree(milliseconds) {
  const deadline = Date.now() + milliseconds;
  while (Date.now() < deadline) {
    if (!portOwners().length) return true;
    await wait(200);
  }
  return !portOwners().length;
}

async function waitForReady(milliseconds = 15000) {
  const deadline = Date.now() + milliseconds;
  let last = null;
  while (Date.now() < deadline) {
    last = await statusFacts();
    if (last.state === "running") return last;
    if (last.state === "misconfigured" || last.foreignPort) return last;
    await wait(250);
  }
  return last ?? await statusFacts();
}

function launchctlChecked(args, context) {
  const result = command(LAUNCHCTL, args);
  if (result.status !== 0) throw new Error(commandError(result, context));
}

async function migrateLegacyOnce(runtime) {
  if (fs.existsSync(CONFIG.plist)) return { migrated: false };
  const legacy = readJob(legacyTarget());
  if (!legacy.loaded) return { migrated: false };
  const server = await fetchServer();
  const validPaths = inspectRuntimeCandidates(CONFIG.cacheRoot).valid.map((item) => item.path);
  const argumentsValid = legacy.output.includes(CONFIG.npm)
    && legacy.output.includes("127.0.0.1")
    && legacy.output.includes("run")
    && legacy.output.includes("start")
    && validPaths.some((candidate) => legacy.output.includes(candidate));
  const payloadValid = server.status === 200
    && server.payload?.app === "cad-viewer"
    && server.payload?.port === CONFIG.port
    && Number.isInteger(server.payload?.pid)
    && legacy.pid
    && pidDescendsFrom(server.payload.pid, legacy.pid);
  if (!argumentsValid || !payloadValid) {
    throw new Error(`Legacy ${CONFIG.legacyLabel} is loaded but failed verified migration checks; it was left running. Inspect with: launchctl print ${legacyTarget()}`);
  }
  launchctlChecked(["bootout", legacyTarget()], "verified legacy bootout failed");
  if (!await waitForPortFree(10000)) throw new Error("verified legacy service stopped but port 3245 did not become free");
  ensurePrivateDirectory(CONFIG.stateDir);
  writeJsonAtomic(CONFIG.migrationRecord, {
    legacyLabel: CONFIG.legacyLabel,
    migratedAt: new Date().toISOString(),
    legacyJobPid: legacy.pid,
    successorRuntime: { path: runtime.path, version: runtime.version },
  });
  return { migrated: true };
}

function validatedInvocationPayload(sourceRoot) {
  if (sourceRoot) return validatePayload(sourceRoot);
  const installed = activePayload();
  if (!installed) throw new Error("No installed CAD Viewer service payload exists; invoke start from a checked-in tools/cad-viewer-service/bin/cad-viewer first");
  return installed;
}

function clearCurrentLink() {
  try {
    const stat = fs.lstatSync(CONFIG.currentLink);
    if (!stat.isSymbolicLink()) throw new Error("refusing to remove non-symlink service/current during rollback");
    fs.unlinkSync(CONFIG.currentLink);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
}

function assertOwnedRegularMatches(filename, expectedBytes, expectedMode) {
  let stat;
  try { stat = fs.lstatSync(filename); }
  catch (error) { if (error.code === "ENOENT") return; throw error; }
  if (!stat.isFile() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error(`refusing to replace unowned or non-regular managed file: ${filename}`);
  if ((stat.mode & 0o777) !== expectedMode || !fs.readFileSync(filename).equals(expectedBytes)) {
    throw new Error(`refusing to replace managed file whose provenance cannot be verified: ${filename}`);
  }
}

function verifyManagedDestinations(priorHash) {
  if (!priorHash) {
    for (const filename of [CONFIG.commandPath, CONFIG.plist]) {
      if (fs.existsSync(filename) || (() => { try { fs.lstatSync(filename); return true; } catch { return false; } })()) {
        throw new Error(`refusing first install because managed destination already exists without an active release: ${filename}`);
      }
    }
    return;
  }
  const priorRoot = path.join(CONFIG.releasesDir, priorHash);
  validatePayload(priorRoot);
  assertOwnedRegularMatches(CONFIG.commandPath, fs.readFileSync(path.join(priorRoot, "bin", "cad-viewer")), 0o755);
  assertOwnedRegularMatches(CONFIG.plist, Buffer.from(expectedPlist(priorRoot)), 0o600);
}

function activatePayload(payload, sourceRoot, priorHash) {
  const release = installRelease(payload, INSTALL_PATHS);
  verifyManagedDestinations(priorHash);
  const stableSnapshot = snapshotFile(CONFIG.commandPath);
  const plistSnapshot = snapshotFile(CONFIG.plist);
  if (sourceRoot && payload.payloadHash !== priorHash) {
    const provenance = sourceProvenance(sourceRoot);
    writeInstallHistory(INSTALL_PATHS, {
      ...provenance,
      manifestHash: payload.payloadHash,
      installedReleaseHash: payload.payloadHash,
      installedAt: new Date().toISOString(),
      priorCurrentHash: priorHash,
    });
  }
  switchCurrent(INSTALL_PATHS, payload.payloadHash);
  installStableCommand(release.release);
  installPlist(expectedPlist(release.release));
  return { ...release, payloadHash: payload.payloadHash, priorHash, stableSnapshot, plistSnapshot };
}

async function rollbackActivation(transaction) {
  restoreFile(CONFIG.commandPath, transaction.stableSnapshot);
  restoreFile(CONFIG.plist, transaction.plistSnapshot);
  if (!transaction.priorHash) {
    clearCurrentLink();
    launchctlChecked(["disable", serviceTarget()], "rollback disable failed");
    if (readJob().loaded) launchctlChecked(["bootout", serviceTarget()], "rollback bootout failed");
    if (!await waitForPortFree(10000)) throw new Error("new service was booted out but its listener did not release port 3245");
    if (!disabledOverride().disabled) throw new Error("rollback did not preserve the disabled override");
    return { restored: true, state: "disabled", priorHash: null };
  }
  switchCurrent(INSTALL_PATHS, transaction.priorHash);
  launchctlChecked(["enable", serviceTarget()], "rollback enable failed");
  if (readJob().loaded) launchctlChecked(["kickstart", "-k", "-p", serviceTarget()], "rollback restart failed");
  else launchctlChecked(["bootstrap", guiDomain(), CONFIG.plist], "rollback bootstrap failed");
  const ready = await waitForReady();
  if (ready.state !== "running") throw new Error(`prior release ${transaction.priorHash} did not regain readiness (state ${ready.state})`);
  return { restored: true, state: ready.state, priorHash: transaction.priorHash };
}

async function startService(sourceRoot = null, forceRestart = false) {
  let candidate;
  try {
    candidate = validatedInvocationPayload(sourceRoot);
  } catch (error) {
    return { exit: 2, result: { ok: false, command: forceRestart ? "restart" : "start", state: "misconfigured", error: error.message } };
  }
  const commandName = forceRestart ? "restart" : "start";
  const dependencies = dependencyCheck({ payloadRoot: candidate.root });
  if (dependencies.errors.length) return { exit: 2, result: { ok: false, command: commandName, state: "misconfigured", errors: dependencies.errors } };
  const priorHash = readCurrentHash(CONFIG.currentLink);
  const current = await statusFacts(candidate.root);
  const changed = priorHash !== candidate.payloadHash;
  if (!forceRestart && !changed && current.state === "running") {
    return { exit: 0, result: { ...statusObject(current), command: commandName, payloadHash: candidate.payloadHash, message: "CAD Viewer is already running with this payload; PID unchanged" } };
  }
  prepareLogs();
  let migration;
  try {
    migration = await migrateLegacyOnce(dependencies.runtime);
  } catch (error) {
    return { exit: 2, result: { ok: false, command: commandName, state: "blocked", error: error.message, portOwners: portOwners() } };
  }
  const before = readJob();
  const owners = portOwners();
  if (!before.loaded && owners.length) {
    return { exit: 2, result: { ok: false, command: commandName, state: "blocked", error: "Port 3245 is owned by an unmanaged process; it was left alive and service state was not enabled", portOwners: owners } };
  }
  if (before.loaded && owners.some((owner) => !before.pid || !pidDescendsFrom(owner.pid, before.pid))) {
    return { exit: 2, result: { ok: false, command: commandName, state: "blocked", error: "A foreign process owns port 3245; it was left alive", portOwners: owners } };
  }
  let lock;
  let transaction;
  try {
    lock = await acquireInstallLock(CONFIG.installLock);
    const activeAfterLock = readCurrentHash(CONFIG.currentLink);
    if (!sourceRoot && activeAfterLock !== candidate.payloadHash) candidate = validatedInvocationPayload(null);
    transaction = activatePayload(candidate, sourceRoot, activeAfterLock);
    launchctlChecked(["enable", serviceTarget()], "launchctl enable failed");
    if (before.loaded) {
      const argumentsForKickstart = (forceRestart || activeAfterLock !== candidate.payloadHash)
        ? ["kickstart", "-k", "-p", serviceTarget()]
        : ["kickstart", "-p", serviceTarget()];
      launchctlChecked(argumentsForKickstart, "launchctl kickstart failed");
    } else launchctlChecked(["bootstrap", guiDomain(), CONFIG.plist], "launchctl bootstrap failed");
    const ready = await waitForReady();
    if (ready.state !== "running") throw new Error(`new payload did not pass readiness within 15 seconds (state ${ready.state})`);
    markLastKnownGood(INSTALL_PATHS, candidate.payloadHash);
    garbageCollect(INSTALL_PATHS, activeAfterLock);
    return {
      exit: 0,
      result: { ...statusObject(ready), command: commandName, payloadHash: candidate.payloadHash, payloadChanged: activeAfterLock !== candidate.payloadHash, migratedLegacy: migration.migrated, message: forceRestart ? "CAD Viewer restarted" : "CAD Viewer started" },
    };
  } catch (error) {
    let rollback = null;
    let rollbackError = null;
    if (transaction) {
      try { rollback = await rollbackActivation(transaction); }
      catch (failure) { rollbackError = failure.message; }
    }
    return {
      exit: 2,
      result: { ok: false, command: commandName, state: "blocked", error: error.message, payloadHash: candidate.payloadHash, rollback, rollbackError },
    };
  } finally {
    if (lock) {
      try { lock.release(); }
      catch (error) { process.stderr.write(`Installer lock release failed: ${error.message}\n`); }
    }
  }
}

async function stopService() {
  const before = readJob();
  launchctlChecked(["disable", serviceTarget()], "launchctl disable failed");
  if (before.loaded) {
    const bootout = command(LAUNCHCTL, ["bootout", serviceTarget()]);
    if (bootout.status !== 0 && readJob().loaded) throw new Error(commandError(bootout, "launchctl bootout failed"));
  }
  await waitForPortFree(10000);
  const facts = await statusFacts();
  const override = disabledOverride();
  if (!override.disabled) return { exit: 2, result: { ...statusObject(facts), command: "stop", state: "misconfigured", error: "launchctl disabled override is not present" } };
  const remaining = portOwners();
  if (remaining.length) return { exit: 2, result: { ...statusObject(facts), command: "stop", state: "blocked", error: "Port 3245 remains occupied; no PID was signaled", portOwners: remaining } };
  return { exit: 0, result: { ...statusObject(facts), ok: true, command: "stop", state: "disabled", message: "CAD Viewer is disabled and unloaded" } };
}

async function restartService(sourceRoot = null) {
  return startService(sourceRoot, true);
}

function readLog(log, count) {
  if (!fs.existsSync(log)) return { missing: true, lines: [] };
  const result = command(TAIL, ["-n", String(count), log]);
  return { missing: false, lines: result.stdout.replace(/\n$/, "").split("\n").filter((line) => line.length) };
}

async function logsCommand(options) {
  const stdout = readLog(CONFIG.stdoutLog, options.lines);
  const stderr = readLog(CONFIG.stderrLog, options.lines);
  if (!options.follow) return { exit: 0, result: { ok: true, command: "logs", state: "snapshot", lines: options.lines, stdout, stderr } };
  const existing = [CONFIG.stdoutLog, CONFIG.stderrLog].filter(fs.existsSync);
  if (options.json) {
    if (!existing.length) return { exit: 1, result: { ok: false, command: "logs", state: "stopped", error: "Both log files are missing" } };
    const child = spawn(TAIL, ["-n", String(options.lines), "-F", ...existing], { stdio: ["ignore", "pipe", "pipe"] });
    let output = "";
    let errorOutput = "";
    let interrupted = false;
    child.stdout.on("data", (chunk) => { output = `${output}${chunk}`.slice(-5 * 1024 * 1024); });
    child.stderr.on("data", (chunk) => { errorOutput = `${errorOutput}${chunk}`.slice(-1024 * 1024); });
    for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) process.once(signal, () => { interrupted = true; child.kill(signal); });
    const exitCode = await new Promise((resolve) => child.once("exit", (code) => resolve(code ?? 1)));
    const exit = interrupted ? 0 : exitCode;
    return { exit, result: { ok: exit === 0, command: "logs", state: "follow-ended", interrupted, output, stderr: errorOutput } };
  }
  process.stdout.write(`==> ${CONFIG.stdoutLog} <==\n${stdout.missing ? "(missing)\n" : `${stdout.lines.join("\n")}\n`}\n`);
  process.stdout.write(`==> ${CONFIG.stderrLog} <==\n${stderr.missing ? "(missing)\n" : `${stderr.lines.join("\n")}\n`}\n`);
  if (!existing.length) return { exit: 1, printed: true, result: { ok: false, command: "logs", state: "stopped", error: "Both log files are missing" } };
  const child = spawn(TAIL, ["-n", "0", "-F", ...existing], { stdio: "inherit" });
  for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) process.once(signal, () => child.kill(signal));
  const exit = await new Promise((resolve) => child.once("exit", (code) => resolve(code ?? 1)));
  return { exit, printed: true, result: { ok: exit === 0, command: "logs", state: "follow-ended" } };
}

async function urlCommand(options) {
  const facts = await statusFacts();
  if (facts.state !== "running") return { exit: 2, result: { ...statusObject(facts), command: "url", error: "CAD Viewer must be running before a review URL is emitted" } };
  let local = CONFIG.localBase;
  let tailscale = CONFIG.tailscaleBase;
  try {
    if (options.workspace) {
      local = encodedWorkspaceUrl(local, options.workspace, options.file);
      tailscale = encodedWorkspaceUrl(tailscale, options.workspace, options.file);
    } else if (options.file) throw new Error("--file requires --workspace");
  } catch (error) {
    return { exit: 2, result: { ok: false, command: "url", state: "misconfigured", error: error.message } };
  }
  return { exit: 0, result: { ok: true, command: "url", state: "running", only: options.localOnly ? "local" : options.tailscaleOnly ? "tailscale" : null, ...(options.localOnly ? { local } : options.tailscaleOnly ? { tailscale } : { local, tailscale }) } };
}

export function parseArguments(argv) {
  const args = [...argv];
  const commandName = args.shift();
  if (!commandName || commandName === "help" || commandName === "--help" || commandName === "-h") return { command: "help", json: args.includes("--json") };
  if (!["start", "stop", "restart", "status", "logs", "url"].includes(commandName)) throw new Error(`Unknown command: ${commandName}`);
  const options = { command: commandName, json: false, lines: 100, follow: false, workspace: null, file: null, localOnly: false, tailscaleOnly: false };
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--json") options.json = true;
    else if (commandName === "logs" && arg === "-f") options.follow = true;
    else if (commandName === "logs" && arg === "--lines") {
      const value = Number(args[++index]);
      if (!Number.isInteger(value) || value < 1) throw new Error("--lines requires a positive integer");
      options.lines = value;
    } else if (commandName === "url" && arg === "--workspace") options.workspace = args[++index];
    else if (commandName === "url" && arg === "--file") options.file = args[++index];
    else if (commandName === "url" && arg === "--local") options.localOnly = true;
    else if (commandName === "url" && arg === "--tailscale") options.tailscaleOnly = true;
    else throw new Error(`Unknown option for ${commandName}: ${arg}`);
  }
  if (options.localOnly && options.tailscaleOnly) throw new Error("--local and --tailscale are mutually exclusive");
  if (options.workspace === undefined || options.file === undefined) throw new Error("Option requires a value");
  return options;
}

function humanPrint(result) {
  if (result.command === "status" || ["start", "stop", "restart"].includes(result.command)) {
    process.stdout.write(`CAD Viewer: ${result.state}\n`);
    if (result.message) process.stdout.write(`${result.message}\n`);
    if (result.runtime) process.stdout.write(`runtime: ${result.runtime.version} ${result.runtime.path}\n`);
    for (const error of result.errors ?? []) process.stderr.write(`${error}\n`);
    if (result.error) process.stderr.write(`${result.error}\n`);
    for (const owner of result.portOwners ?? []) process.stdout.write(`port owner: ${owner.pid} ${owner.command}\n`);
    if (result.logTail) {
      for (const [name, log] of [["stdout", result.logTail.stdout], ["stderr", result.logTail.stderr]]) {
        if (!log.missing && log.lines.length) process.stdout.write(`last ${name}:\n${log.lines.join("\n")}\n`);
      }
    }
    return;
  }
  if (result.command === "logs") {
    for (const [name, log] of [[CONFIG.stdoutLog, result.stdout], [CONFIG.stderrLog, result.stderr]]) {
      process.stdout.write(`==> ${name} <==\n`);
      process.stdout.write(log.missing ? "(missing)\n" : `${log.lines.join("\n")}\n`);
    }
    return;
  }
  if (result.command === "url") {
    if (result.only === "local") {
      process.stdout.write(`${result.local}\n`);
      return;
    }
    if (result.only === "tailscale") {
      process.stdout.write(`${result.tailscale}\n`);
      return;
    }
    if (result.local) process.stdout.write(`local:     ${result.local}\n`);
    if (result.tailscale) process.stdout.write(`tailscale: ${result.tailscale}\n`);
    if (result.error) process.stderr.write(`${result.error}\n`);
  }
}

function help() {
  return `Usage: cad-viewer <start|stop|restart|status|logs|url> [options]\n\nCommands:\n  start, stop, restart, status\n  logs [--lines N] [-f]\n  url [--workspace ABSOLUTE --file RELATIVE] [--local|--tailscale]\n\nAll commands accept --json.\n`;
}

export async function main(argv = process.argv.slice(2)) {
  const commandArgs = [...argv];
  let sourceRoot = null;
  if (commandArgs[0] === "--source-root") {
    sourceRoot = commandArgs[1];
    commandArgs.splice(0, 2);
    if (!sourceRoot || !path.isAbsolute(sourceRoot)) {
      process.stdout.write(`${JSON.stringify({ ok: false, command: commandArgs[0] ?? null, state: "misconfigured", error: "--source-root requires an absolute payload directory" })}\n`);
      return 2;
    }
  }
  let options;
  try {
    options = parseArguments(commandArgs);
  } catch (error) {
    const json = commandArgs.includes("--json");
    const result = { ok: false, command: commandArgs[0] ?? null, state: "misconfigured", error: error.message };
    process.stdout.write(json ? `${JSON.stringify(result)}\n` : `${error.message}\n${help()}`);
    return 2;
  }
  if (options.command === "help") {
    process.stdout.write(options.json ? `${JSON.stringify({ ok: true, command: "help", state: "ready", usage: help() })}\n` : help());
    return 0;
  }
  let outcome;
  try {
    if (options.command === "status") {
      const facts = await statusFacts(sourceRoot);
      outcome = { exit: statusExit(facts.state), result: statusObject(facts) };
    } else if (options.command === "start") outcome = await startService(sourceRoot);
    else if (options.command === "stop") outcome = await stopService();
    else if (options.command === "restart") outcome = await restartService(sourceRoot);
    else if (options.command === "logs") outcome = await logsCommand(options);
    else outcome = await urlCommand(options);
  } catch (error) {
    outcome = { exit: 2, result: { ok: false, command: options.command, state: "misconfigured", error: error.message } };
  }
  if (!outcome.printed) {
    if (options.json) process.stdout.write(`${JSON.stringify(outcome.result)}\n`);
    else humanPrint(outcome.result);
  }
  return outcome.exit;
}

function isDirectInvocation() {
  if (!process.argv[1]) return false;
  try {
    return fs.realpathSync(path.resolve(process.argv[1])) === fs.realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}

if (isDirectInvocation()) {
  process.exitCode = await main();
}
