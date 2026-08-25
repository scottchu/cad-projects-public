import fs from "node:fs";
import path from "node:path";

const SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/;

export function parseSemver(value) {
  const match = SEMVER.exec(String(value ?? ""));
  if (!match) return null;
  return {
    raw: String(value),
    major: Number(match[1]),
    minor: Number(match[2]),
    patch: Number(match[3]),
    prerelease: match[4] ? match[4].split(".") : [],
  };
}

export function compareSemver(a, b) {
  for (const key of ["major", "minor", "patch"]) {
    if (a[key] !== b[key]) return a[key] > b[key] ? 1 : -1;
  }
  if (!a.prerelease.length && !b.prerelease.length) return 0;
  if (!a.prerelease.length) return 1;
  if (!b.prerelease.length) return -1;
  const length = Math.max(a.prerelease.length, b.prerelease.length);
  for (let index = 0; index < length; index += 1) {
    const left = a.prerelease[index];
    const right = b.prerelease[index];
    if (left === undefined) return -1;
    if (right === undefined) return 1;
    if (left === right) continue;
    const leftNumeric = /^\d+$/.test(left);
    const rightNumeric = /^\d+$/.test(right);
    if (leftNumeric && rightNumeric) return BigInt(left) > BigInt(right) ? 1 : -1;
    if (leftNumeric !== rightNumeric) return leftNumeric ? -1 : 1;
    return left > right ? 1 : -1;
  }
  return 0;
}

function contained(candidate, root) {
  return candidate === root || candidate.startsWith(`${root}${path.sep}`);
}

export function inspectRuntimeCandidates(cacheRoot) {
  const valid = [];
  const rejected = [];
  let realCacheRoot;
  try {
    realCacheRoot = fs.realpathSync(cacheRoot);
  } catch (error) {
    return { valid, rejected: [{ path: cacheRoot, reason: `cache root unavailable: ${error.message}` }] };
  }
  let entries;
  try {
    entries = fs.readdirSync(cacheRoot, { withFileTypes: true });
  } catch (error) {
    return { valid, rejected: [{ path: cacheRoot, reason: error.message }] };
  }
  for (const entry of entries) {
    if (!(entry.isDirectory() || entry.isSymbolicLink())) continue;
    const candidate = path.join(cacheRoot, entry.name, "skills", "cad-viewer", "scripts", "viewer");
    let realPath;
    try {
      realPath = fs.realpathSync(candidate);
    } catch {
      continue;
    }
    if (!contained(realPath, realCacheRoot)) {
      rejected.push({ path: candidate, reason: "real path escapes the text-to-cad cache root" });
      continue;
    }
    const packagePath = path.join(realPath, "package.json");
    const startPath = path.join(realPath, "scripts", "start-viewer.mjs");
    try {
      fs.accessSync(packagePath, fs.constants.R_OK);
      fs.accessSync(startPath, fs.constants.R_OK);
      const realPackage = fs.realpathSync(packagePath);
      const realStart = fs.realpathSync(startPath);
      if (!contained(realPackage, realPath) || !contained(realStart, realPath)) {
        throw new Error("required runtime file escapes the selected Viewer runtime");
      }
      if (!fs.statSync(realPackage).isFile() || !fs.statSync(realStart).isFile()) {
        throw new Error("required runtime paths must be regular files");
      }
      const packageJson = JSON.parse(fs.readFileSync(packagePath, "utf8"));
      const semver = parseSemver(packageJson.version);
      if (!semver) throw new Error("package version is not valid SemVer");
      if (typeof packageJson.scripts?.start !== "string" || !packageJson.scripts.start.trim()) {
        throw new Error("package has no npm start script");
      }
      valid.push({ path: realPath, version: packageJson.version, semver });
    } catch (error) {
      rejected.push({ path: realPath, reason: error.message });
    }
  }
  return { valid, rejected };
}

export function selectViewerRuntime(cacheRoot) {
  const inspected = inspectRuntimeCandidates(cacheRoot);
  const stable = inspected.valid.filter((item) => item.semver.prerelease.length === 0);
  const pool = stable.length ? stable : inspected.valid;
  pool.sort((a, b) => compareSemver(b.semver, a.semver) || (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
  if (!pool.length) {
    const detail = inspected.rejected.map((item) => `${item.path}: ${item.reason}`).join("; ");
    throw new Error(`No valid installed CAD Viewer runtime was found${detail ? ` (${detail})` : ""}`);
  }
  return { path: pool[0].path, version: pool[0].version, candidates: inspected.valid, rejected: inspected.rejected };
}

export function inspectRuntimeRecord(record, preferredRuntime) {
  if (record === null || record === undefined) {
    return { matches: false, issue: "runtime.json is missing" };
  }
  if (typeof record !== "object" || Array.isArray(record)) {
    return { matches: false, issue: "runtime.json must contain a JSON object" };
  }
  if (typeof record.path !== "string" || typeof record.version !== "string") {
    return { matches: false, issue: "runtime.json is missing a runtime path or version" };
  }
  if (!Number.isInteger(record.launcherPid) || Number.isNaN(Date.parse(record.launchedAt))) {
    return { matches: false, issue: "runtime.json is missing a valid launch time or launcher PID" };
  }
  if (!preferredRuntime || record.path !== preferredRuntime.path || record.version !== preferredRuntime.version) {
    return {
      matches: false,
      issue: `runtime.json selects ${record.version} ${record.path}, not the preferred ${preferredRuntime?.version ?? "unavailable"} ${preferredRuntime?.path ?? "runtime"}`,
    };
  }
  return { matches: true, issue: null };
}

export function evaluateViewerHealth(page, server, expectedPort) {
  const pageReady = page?.status === 200;
  const serverReady = server?.status === 200
    && server.payload?.app === "cad-viewer"
    && server.payload?.port === expectedPort
    && Number.isInteger(server.payload?.pid);
  const errors = [];
  if (!pageReady) errors.push(`Viewer page is not ready${page?.status ? ` (HTTP ${page.status})` : page?.error ? ` (${page.error})` : ""}`);
  if (!serverReady) errors.push(`Viewer server API is not ready${server?.status ? ` (HTTP ${server.status})` : server?.error ? ` (${server.error})` : ""}`);
  return { ready: pageReady && serverReady, pageReady, serverReady, errors };
}

export function requiresManagedRecovery({ ready, runtimeRecordIssue }) {
  return !ready || Boolean(runtimeRecordIssue);
}

export function classifyState(facts) {
  if (facts.misconfigured) return "misconfigured";
  if (facts.blocked || facts.foreignPort) return "blocked";
  if (facts.enabled && facts.loaded && facts.ready) return "running";
  if (facts.loaded) return "starting";
  if (facts.disabled) return "disabled";
  return "stopped";
}

export function xmlEscape(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

export function renderPlist(template, values) {
  let rendered = template;
  for (const [key, value] of Object.entries(values)) {
    rendered = rendered.replaceAll(`@@${key}@@`, xmlEscape(value));
  }
  if (/@@[A-Z0-9_]+@@/.test(rendered)) throw new Error("plist template contains unresolved placeholders");
  return rendered;
}

export function encodedWorkspaceUrl(base, workspace, file = null) {
  if (!path.isAbsolute(workspace)) throw new Error("--workspace must be an absolute directory");
  const workspaceReal = fs.realpathSync(workspace);
  if (!fs.statSync(workspaceReal).isDirectory()) throw new Error("--workspace must name a directory");
  const encodedPath = workspaceReal.split(path.sep).map(encodeURIComponent).join("/");
  let result = `${base}${encodedPath.startsWith("/") ? "" : "/"}${encodedPath}`;
  if (file !== null && file !== undefined) {
    if (!file || path.isAbsolute(file)) throw new Error("--file must be a non-empty relative path");
    const requested = path.resolve(workspaceReal, file);
    const realFile = fs.realpathSync(requested);
    if (!contained(realFile, workspaceReal)) throw new Error("--file escapes the workspace");
    if (!fs.statSync(realFile).isFile()) throw new Error("--file must name an existing file");
    const relative = path.relative(workspaceReal, realFile);
    if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) throw new Error("--file escapes the workspace");
    result += `?file=${encodeURIComponent(relative)}`;
  }
  return result;
}
