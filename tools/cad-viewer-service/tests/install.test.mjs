import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  acquireInstallLock,
  atomicCopyFile,
  canonicalJson,
  installRelease,
  readCurrentHash,
  restoreFile,
  sha256,
  snapshotFile,
  switchCurrent,
  validatePayload,
} from "../payload/install.mjs";

function writeMode(filename, content, mode) {
  fs.mkdirSync(path.dirname(filename), { recursive: true });
  fs.writeFileSync(filename, content, { mode });
  fs.chmodSync(filename, mode);
}

function fixturePayload(parent, name = "payload", marker = "true") {
  const root = path.join(parent, name);
  writeMode(path.join(root, "cli.mjs"), `export const fixture = ${JSON.stringify(marker)};\n`, 0o644);
  writeMode(path.join(root, "bin", "cad-viewer"), "#!/bin/zsh\nexit 0\n", 0o755);
  const files = {};
  for (const [relative, mode] of [["bin/cad-viewer", 0o755], ["cli.mjs", 0o644]]) {
    files[relative] = { mode, sha256: sha256(fs.readFileSync(path.join(root, ...relative.split("/")))) };
  }
  fs.writeFileSync(path.join(root, "install-manifest.json"), canonicalJson({ files, formatVersion: 1 }), { mode: 0o600 });
  return root;
}

test("manifest validates canonical bytes, hashes, modes, and exact listed files", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-manifest-"));
  try {
    const root = fixturePayload(parent);
    const valid = validatePayload(root);
    assert.match(valid.payloadHash, /^[0-9a-f]{64}$/);
    fs.writeFileSync(path.join(root, "extra"), "unlisted");
    assert.throws(() => validatePayload(root), /unlisted/);
    fs.unlinkSync(path.join(root, "extra"));
    fs.appendFileSync(path.join(root, "cli.mjs"), "altered");
    assert.throws(() => validatePayload(root), /SHA-256 mismatch/);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("checked-in install manifest independently validates the exact source payload", () => {
  const payloadRoot = path.resolve(new URL("../payload", import.meta.url).pathname);
  const payload = validatePayload(payloadRoot);
  assert.match(payload.payloadHash, /^[0-9a-f]{64}$/);
  assert.ok(payload.files.includes("cli.mjs"));
  assert.ok(payload.files.includes("bin/cad-viewer"));
  assert.ok(!payload.files.includes("install-manifest.json"));
});

test("manifest rejects noncanonical JSON, mode mismatch, traversal, and symlinks", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-manifest-"));
  try {
    let root = fixturePayload(parent, "mode");
    fs.chmodSync(path.join(root, "cli.mjs"), 0o600);
    assert.throws(() => validatePayload(root), /mode mismatch/);

    root = fixturePayload(parent, "noncanonical");
    const parsed = JSON.parse(fs.readFileSync(path.join(root, "install-manifest.json"), "utf8"));
    fs.writeFileSync(path.join(root, "install-manifest.json"), `${JSON.stringify(parsed, null, 2)}\n`);
    assert.throws(() => validatePayload(root), /not canonical/);

    root = fixturePayload(parent, "traversal");
    const manifest = JSON.parse(fs.readFileSync(path.join(root, "install-manifest.json"), "utf8"));
    manifest.files["../escape"] = { mode: 0o644, sha256: "0".repeat(64) };
    fs.writeFileSync(path.join(root, "install-manifest.json"), canonicalJson(manifest));
    assert.throws(() => validatePayload(root), /unsafe manifest path/);

    root = fixturePayload(parent, "symlink");
    fs.symlinkSync("cli.mjs", path.join(root, "linked"));
    assert.throws(() => validatePayload(root), /forbidden symlink/);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("release install revalidates copies and current switches atomically by hash", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-release-"));
  try {
    const payload = validatePayload(fixturePayload(parent, "source"));
    const service = path.join(parent, "service");
    const paths = { releasesDir: path.join(service, "releases"), currentLink: path.join(service, "current") };
    const installed = installRelease(payload, paths);
    assert.equal(installed.reused, false);
    assert.equal(validatePayload(installed.release).payloadHash, payload.payloadHash);
    switchCurrent(paths, payload.payloadHash);
    assert.equal(readCurrentHash(paths.currentLink), payload.payloadHash);
    assert.equal(installRelease(payload, paths).reused, true);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("file snapshots provide rollback hooks without mixed content", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-rollback-"));
  const target = path.join(parent, "stable-command");
  try {
    writeMode(target, "prior", 0o755);
    const snapshot = snapshotFile(target);
    writeMode(target, "candidate", 0o755);
    restoreFile(target, snapshot);
    assert.equal(fs.readFileSync(target, "utf8"), "prior");
    assert.equal(fs.statSync(target).mode & 0o777, 0o755);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("rollback hooks restore prior current hash and stable shim together", () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-rollback-release-"));
  try {
    const paths = { releasesDir: path.join(parent, "service", "releases"), currentLink: path.join(parent, "service", "current") };
    const prior = validatePayload(fixturePayload(parent, "prior-source", "prior"));
    const candidate = validatePayload(fixturePayload(parent, "candidate-source", "candidate"));
    const priorRelease = installRelease(prior, paths).release;
    const candidateRelease = installRelease(candidate, paths).release;
    const stable = path.join(parent, "bin", "cad-viewer");
    switchCurrent(paths, prior.payloadHash);
    atomicCopyFile(path.join(priorRelease, "bin", "cad-viewer"), stable, 0o755);
    const stableSnapshot = snapshotFile(stable);
    switchCurrent(paths, candidate.payloadHash);
    atomicCopyFile(path.join(candidateRelease, "bin", "cad-viewer"), stable, 0o755);
    switchCurrent(paths, prior.payloadHash);
    restoreFile(stable, stableSnapshot);
    assert.equal(readCurrentHash(paths.currentLink), prior.payloadHash);
    assert.equal(fs.readFileSync(stable, "utf8"), fs.readFileSync(path.join(priorRelease, "bin", "cad-viewer"), "utf8"));
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});

test("installer lock reclaims provably stale owner and times out a live owner", async () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), "cad-viewer-lock-"));
  const lockPath = path.join(parent, "install.lock");
  try {
    fs.mkdirSync(lockPath);
    fs.writeFileSync(path.join(lockPath, "owner.json"), canonicalJson({ pid: 99999999, processStart: "dead", token: "dead", createdAt: new Date().toISOString() }));
    const reclaimed = await acquireInstallLock(lockPath, 250);
    reclaimed.release();

    const processStart = spawnSync("/bin/ps", ["-o", "lstart=", "-p", String(process.pid)], { encoding: "utf8" }).stdout.trim();
    fs.mkdirSync(lockPath);
    fs.writeFileSync(path.join(lockPath, "owner.json"), canonicalJson({ pid: process.pid, processStart, token: "live", createdAt: new Date().toISOString() }));
    await assert.rejects(acquireInstallLock(lockPath, 120), /timed out.*live/);
  } finally {
    fs.rmSync(parent, { recursive: true, force: true });
  }
});
