import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import { pathToFileURL } from "node:url";

function option(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index === -1 ? fallback : process.argv[index + 1];
}

const role = option("--role", "parent");
const port = Number(option("--port", "0"));
const modeFile = option("--mode-file");
const ignoreTerm = process.argv.includes("--ignore-term");

if (role === "driver") {
  const launcher = option("--launcher");
  const { launchOwnedProcessGroup } = await import(pathToFileURL(launcher));
  const group = await launchOwnedProcessGroup({
    executable: process.execPath,
    args: [new URL(import.meta.url).pathname, "--role", "parent", "--port", String(port), "--mode-file", modeFile],
    cwd: new URL(".", import.meta.url).pathname,
    env: { ...process.env },
    port,
    handshakeTimeoutMs: 2000,
  });
  process.stdout.write(`${JSON.stringify({ pgid: group.pgid, anchorPid: group.anchorPid, startEvidence: group.startEvidence })}\n`);
  setInterval(() => {}, 1000);
} else if (role === "parent") {
  const childArgs = [new URL(import.meta.url).pathname, "--role", "backend", "--port", String(port)];
  if (modeFile) childArgs.push("--mode-file", modeFile);
  if (ignoreTerm) childArgs.push("--ignore-term");
  const backend = spawn(process.execPath, childArgs, { detached: false, stdio: "inherit" });
  backend.once("exit", (code, signal) => {
    if (!ignoreTerm) process.exit(code ?? (signal ? 1 : 0));
  });
  if (ignoreTerm) process.on("SIGTERM", () => {});
  else process.once("SIGTERM", () => process.exit(0));
  setInterval(() => {}, 1000);
} else {
  const server = http.createServer((request, response) => {
    if (request.url === "/__cad/server") {
      response.writeHead(200, { "content-type": "application/json" });
      response.end(JSON.stringify({ app: "cad-viewer", port, pid: process.pid }));
      return;
    }
    const status = modeFile && fs.readFileSync(modeFile, "utf8").trim() === "404" ? 404 : 200;
    response.writeHead(status, { "content-type": "text/html" });
    response.end(status === 200 ? "viewer" : "missing");
  });
  server.listen(port, "127.0.0.1");
  if (ignoreTerm) process.on("SIGTERM", () => {});
  else process.once("SIGTERM", () => server.close(() => process.exit(0)));
}
