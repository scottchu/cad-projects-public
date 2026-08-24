import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { CONFIG } from "./config.mjs";
import { selectViewerRuntime } from "./core.mjs";

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
  fs.writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600, flag: "wx" });
  fs.renameSync(temporary, destination);
}

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
  process.exit(1);
}

const child = spawn(CONFIG.npm, [
  "--prefix", runtime.path, "run", "start", "--",
  "--host", CONFIG.host, "--port", String(CONFIG.port), "--json",
], {
  cwd: CONFIG.viewerDefaultRoot,
  env: {
    ...process.env,
    PATH: CONFIG.safePath,
    VIEWER_CAD_PYTHON: CONFIG.canonicalPython,
    INIT_CWD: CONFIG.viewerDefaultRoot,
  },
  stdio: "inherit",
});

let forwarding = false;
for (const signal of ["SIGTERM", "SIGINT", "SIGHUP"]) {
  process.on(signal, () => {
    if (forwarding) return;
    forwarding = true;
    child.kill(signal);
  });
}

child.on("error", (error) => {
  process.stderr.write(`Failed to spawn fixed bundled npm: ${error.message}\n`);
  process.exit(1);
});
child.on("exit", (code, signal) => {
  if (signal) {
    for (const name of ["SIGTERM", "SIGINT", "SIGHUP"]) process.removeAllListeners(name);
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});
