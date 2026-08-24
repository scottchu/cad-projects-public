import { spawnSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const MANIFEST_NAME = "install-manifest.json";
const HASH_PATTERN = /^[0-9a-f]{64}$/;

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function sha256(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function safeRelative(relative) {
  return typeof relative === "string"
    && relative.length > 0
    && !relative.includes("\\")
    && !path.posix.isAbsolute(relative)
    && path.posix.normalize(relative) === relative
    && !relative.split("/").includes("..")
    && relative !== MANIFEST_NAME;
}

function walkPayload(root) {
  const files = [];
  const visit = (directory, prefix = "") => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
      const absolute = path.join(directory, entry.name);
      const stat = fs.lstatSync(absolute);
      if (stat.isSymbolicLink()) throw new Error(`payload contains forbidden symlink: ${relative}`);
      if (stat.isDirectory()) visit(absolute, relative);
      else if (stat.isFile()) files.push(relative);
      else throw new Error(`payload contains unsupported filesystem entry: ${relative}`);
    }
  };
  visit(root);
  return files.sort();
}

function readRegularNoFollow(filename) {
  const descriptor = fs.openSync(filename, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try {
    const stat = fs.fstatSync(descriptor);
    if (!stat.isFile()) throw new Error(`not a regular file: ${filename}`);
    return { bytes: fs.readFileSync(descriptor), mode: stat.mode & 0o777 };
  } finally {
    fs.closeSync(descriptor);
  }
}

export function validatePayload(root) {
  if (!path.isAbsolute(root)) throw new Error("payload root must be absolute");
  const realRoot = fs.realpathSync(root);
  if (!fs.statSync(realRoot).isDirectory()) throw new Error("payload root must be a directory");
  const manifestPath = path.join(realRoot, MANIFEST_NAME);
  const manifestFile = readRegularNoFollow(manifestPath);
  const manifestText = manifestFile.bytes.toString("utf8");
  let manifest;
  try {
    manifest = JSON.parse(manifestText);
  } catch (error) {
    throw new Error(`invalid install manifest JSON: ${error.message}`);
  }
  if (canonicalJson(manifest) !== manifestText) throw new Error("install manifest bytes are not canonical compact recursively sorted JSON");
  if (manifest.formatVersion !== 1 || !manifest.files || typeof manifest.files !== "object" || Array.isArray(manifest.files)) {
    throw new Error("install manifest schema is invalid");
  }
  const listed = Object.keys(manifest.files).sort();
  if (!listed.length) throw new Error("install manifest has no payload files");
  for (const relative of listed) {
    if (!safeRelative(relative)) throw new Error(`unsafe manifest path: ${relative}`);
    const entry = manifest.files[relative];
    if (!entry || !HASH_PATTERN.test(entry.sha256) || !Number.isInteger(entry.mode) || entry.mode < 0 || entry.mode > 0o777 || (entry.mode & 0o022)) {
      throw new Error(`invalid manifest entry: ${relative}`);
    }
    const absolute = path.join(realRoot, ...relative.split("/"));
    const file = readRegularNoFollow(absolute);
    if (file.mode !== entry.mode) throw new Error(`mode mismatch for ${relative}: expected ${entry.mode.toString(8)}, got ${file.mode.toString(8)}`);
    if (sha256(file.bytes) !== entry.sha256) throw new Error(`SHA-256 mismatch for ${relative}`);
  }
  const actual = walkPayload(realRoot);
  const expected = [...listed, MANIFEST_NAME].sort();
  if (actual.length !== expected.length || actual.some((item, index) => item !== expected[index])) {
    throw new Error(`payload contains missing or unlisted files (expected ${expected.join(", ")}; got ${actual.join(", ")})`);
  }
  return {
    root: realRoot,
    manifest,
    manifestBytes: manifestFile.bytes,
    payloadHash: sha256(manifestFile.bytes),
    files: listed,
  };
}

function ensureOwnedPrivateDirectory(directory) {
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  const stat = fs.statSync(directory);
  if (!stat.isDirectory() || stat.uid !== process.getuid()) throw new Error(`not an owned directory: ${directory}`);
  fs.chmodSync(directory, 0o700);
}

function copyManifestFile(sourceRoot, targetRoot, relative, entry) {
  const source = path.join(sourceRoot, ...relative.split("/"));
  const destination = path.join(targetRoot, ...relative.split("/"));
  fs.mkdirSync(path.dirname(destination), { recursive: true, mode: 0o700 });
  const file = readRegularNoFollow(source);
  if (sha256(file.bytes) !== entry.sha256 || file.mode !== entry.mode) throw new Error(`source changed during install: ${relative}`);
  fs.writeFileSync(destination, file.bytes, { flag: "wx", mode: entry.mode });
  fs.chmodSync(destination, entry.mode);
}

export function installRelease(payload, paths) {
  ensureOwnedPrivateDirectory(paths.releasesDir);
  const release = path.join(paths.releasesDir, payload.payloadHash);
  if (fs.existsSync(release)) {
    const installed = validatePayload(release);
    if (installed.payloadHash !== payload.payloadHash) throw new Error("existing content-addressed release failed revalidation");
    return { release, reused: true };
  }
  const staging = path.join(paths.releasesDir, `.staging-${process.pid}-${crypto.randomBytes(8).toString("hex")}`);
  fs.mkdirSync(staging, { mode: 0o700 });
  try {
    for (const relative of payload.files) copyManifestFile(payload.root, staging, relative, payload.manifest.files[relative]);
    fs.writeFileSync(path.join(staging, MANIFEST_NAME), payload.manifestBytes, { flag: "wx", mode: 0o600 });
    const staged = validatePayload(staging);
    if (staged.payloadHash !== payload.payloadHash) throw new Error("staged payload hash differs from source");
    fs.renameSync(staging, release);
  } catch (error) {
    fs.rmSync(staging, { recursive: true, force: true });
    throw error;
  }
  return { release, reused: false };
}

function processStartEvidence(pid) {
  const result = spawnSync("/bin/ps", ["-o", "lstart=", "-p", String(pid)], { encoding: "utf8" });
  return result.status === 0 && result.stdout.trim() ? result.stdout.trim() : null;
}

function lockOwnerState(lockPath) {
  let owner;
  try {
    owner = JSON.parse(fs.readFileSync(path.join(lockPath, "owner.json"), "utf8"));
  } catch {
    return { stale: false, reason: "lock owner is unreadable or unverifiable" };
  }
  if (!Number.isInteger(owner.pid) || typeof owner.processStart !== "string" || typeof owner.token !== "string") {
    return { stale: false, reason: "lock owner evidence is malformed" };
  }
  let alive = true;
  try {
    process.kill(owner.pid, 0);
  } catch (error) {
    if (error.code === "ESRCH") alive = false;
    else return { stale: false, reason: "lock owner liveness cannot be proved" };
  }
  if (!alive) return { stale: true, reason: "owner PID is dead" };
  const currentStart = processStartEvidence(owner.pid);
  if (currentStart && currentStart !== owner.processStart) return { stale: true, reason: "owner PID was reused" };
  return { stale: false, reason: currentStart ? "owner is live" : "lock owner start cannot be verified" };
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export async function acquireInstallLock(lockPath, timeoutMs = 15000) {
  ensureOwnedPrivateDirectory(path.dirname(lockPath));
  const deadline = Date.now() + timeoutMs;
  while (true) {
    const token = crypto.randomBytes(16).toString("hex");
    try {
      fs.mkdirSync(lockPath, { mode: 0o700 });
      const owner = { pid: process.pid, processStart: processStartEvidence(process.pid), token, createdAt: new Date().toISOString() };
      if (!owner.processStart) throw new Error("cannot establish installer process-start evidence");
      fs.writeFileSync(path.join(lockPath, "owner.json"), canonicalJson(owner), { flag: "wx", mode: 0o600 });
      return {
        owner,
        release() {
          const current = JSON.parse(fs.readFileSync(path.join(lockPath, "owner.json"), "utf8"));
          if (current.token !== token || current.pid !== process.pid) throw new Error("refusing to release a lock no longer owned by this installer");
          fs.unlinkSync(path.join(lockPath, "owner.json"));
          fs.rmdirSync(lockPath);
        },
      };
    } catch (error) {
      if (error.code !== "EEXIST") {
        if (fs.existsSync(lockPath) && !fs.existsSync(path.join(lockPath, "owner.json"))) {
          try { fs.rmdirSync(lockPath); } catch { /* contender may own it */ }
        }
        throw error;
      }
      const state = lockOwnerState(lockPath);
      if (state.stale) {
        const stale = `${lockPath}.stale-${Date.now()}-${crypto.randomBytes(4).toString("hex")}`;
        try {
          fs.renameSync(lockPath, stale);
          fs.rmSync(stale, { recursive: true, force: true });
          continue;
        } catch { /* another contender won; poll */ }
      }
      if (Date.now() >= deadline) throw new Error(`installer lock timed out: ${state.reason}`);
      await delay(100);
    }
  }
}

export function readCurrentHash(currentLink) {
  try {
    const stat = fs.lstatSync(currentLink);
    if (!stat.isSymbolicLink()) throw new Error("service/current is not a symlink");
    const target = fs.readlinkSync(currentLink);
    const match = /^releases\/([0-9a-f]{64})$/.exec(target);
    if (!match) throw new Error("service/current has an unsafe target");
    return match[1];
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

export function switchCurrent(paths, payloadHash) {
  if (!HASH_PATTERN.test(payloadHash)) throw new Error("invalid release hash");
  validatePayload(path.join(paths.releasesDir, payloadHash));
  const temporary = `${paths.currentLink}.new`;
  try {
    const stat = fs.lstatSync(temporary);
    if (!stat.isSymbolicLink()) throw new Error("refusing to replace non-symlink current.new");
    fs.unlinkSync(temporary);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  try {
    const stat = fs.lstatSync(paths.currentLink);
    if (!stat.isSymbolicLink()) throw new Error("refusing to replace non-symlink service/current");
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  fs.symlinkSync(`releases/${payloadHash}`, temporary);
  fs.renameSync(temporary, paths.currentLink);
}

export function atomicCopyFile(source, destination, mode = 0o755) {
  const sourceFile = readRegularNoFollow(source);
  ensureOwnedPrivateDirectory(path.dirname(destination));
  const temporary = `${destination}.tmp-${process.pid}-${crypto.randomBytes(4).toString("hex")}`;
  fs.writeFileSync(temporary, sourceFile.bytes, { flag: "wx", mode });
  fs.chmodSync(temporary, mode);
  fs.renameSync(temporary, destination);
}

export function sourceProvenance(sourceRoot) {
  const commit = spawnSync("/usr/bin/git", ["-C", sourceRoot, "rev-parse", "HEAD"], { encoding: "utf8" });
  const dirty = spawnSync("/usr/bin/git", ["-C", sourceRoot, "status", "--porcelain"], { encoding: "utf8" });
  return {
    sourcePath: sourceRoot,
    sourceGitCommit: commit.status === 0 ? commit.stdout.trim() : null,
    sourceGitDirty: dirty.status === 0 ? Boolean(dirty.stdout.trim()) : null,
  };
}

export function writeInstallHistory(paths, record) {
  ensureOwnedPrivateDirectory(paths.installHistoryDir);
  const name = `${new Date().toISOString().replaceAll(":", "").replaceAll(".", "")}-${process.pid}-${crypto.randomBytes(4).toString("hex")}.json`;
  const destination = path.join(paths.installHistoryDir, name);
  fs.writeFileSync(destination, canonicalJson(record), { flag: "wx", mode: 0o600 });
  return destination;
}

export function markLastKnownGood(paths, payloadHash) {
  const temporary = `${paths.lastKnownGood}.new`;
  for (const link of [temporary, paths.lastKnownGood]) {
    try {
      const stat = fs.lstatSync(link);
      if (!stat.isSymbolicLink()) throw new Error(`refusing to replace non-symlink release pointer: ${link}`);
      if (link === temporary) fs.unlinkSync(link);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  fs.symlinkSync(`releases/${payloadHash}`, temporary);
  fs.renameSync(temporary, paths.lastKnownGood);
}

function linkedHash(link) {
  try {
    const target = fs.readlinkSync(link);
    return /^releases\/([0-9a-f]{64})$/.exec(target)?.[1] ?? null;
  } catch {
    return null;
  }
}

export function garbageCollect(paths, priorHash = null) {
  const active = readCurrentHash(paths.currentLink);
  const lastKnownGood = linkedHash(paths.lastKnownGood);
  const releases = fs.readdirSync(paths.releasesDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && HASH_PATTERN.test(entry.name))
    .map((entry) => ({ hash: entry.name, mtime: fs.statSync(path.join(paths.releasesDir, entry.name)).mtimeMs }))
    .sort((a, b) => b.mtime - a.mtime);
  const keep = new Set([active, lastKnownGood, priorHash].filter(Boolean));
  const onePrior = priorHash ? null : releases.find((item) => !keep.has(item.hash));
  if (onePrior) keep.add(onePrior.hash);
  for (const release of releases) {
    if (!keep.has(release.hash)) fs.rmSync(path.join(paths.releasesDir, release.hash), { recursive: true, force: true });
  }
  for (const entry of fs.readdirSync(paths.releasesDir, { withFileTypes: true })) {
    if (entry.isDirectory() && entry.name.startsWith(".staging-")) fs.rmSync(path.join(paths.releasesDir, entry.name), { recursive: true, force: true });
  }
}

export function snapshotFile(filename) {
  try {
    const stat = fs.lstatSync(filename);
    if (!stat.isFile()) throw new Error(`refusing to snapshot non-file: ${filename}`);
    return { exists: true, bytes: fs.readFileSync(filename), mode: stat.mode & 0o777 };
  } catch (error) {
    if (error.code === "ENOENT") return { exists: false };
    throw error;
  }
}

export function restoreFile(filename, snapshot) {
  if (!snapshot.exists) {
    try { fs.unlinkSync(filename); } catch (error) { if (error.code !== "ENOENT") throw error; }
    return;
  }
  ensureOwnedPrivateDirectory(path.dirname(filename));
  const temporary = `${filename}.rollback-${process.pid}-${crypto.randomBytes(4).toString("hex")}`;
  fs.writeFileSync(temporary, snapshot.bytes, { flag: "wx", mode: snapshot.mode });
  fs.chmodSync(temporary, snapshot.mode);
  fs.renameSync(temporary, filename);
}
