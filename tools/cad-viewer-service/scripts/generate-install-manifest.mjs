import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { canonicalJson, sha256 } from "../payload/install.mjs";

const serviceRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const payloadRoot = path.join(serviceRoot, "payload");
const manifestPath = path.join(payloadRoot, "install-manifest.json");
const installable = [
  "bin/cad-viewer",
  "cli.mjs",
  "config.mjs",
  "core.mjs",
  "install.mjs",
  "launch-viewer.mjs",
  "launchd/com.scottchu.cad-viewer.plist.template",
];

const files = {};
for (const relative of installable) {
  const absolute = path.join(payloadRoot, ...relative.split("/"));
  const stat = fs.lstatSync(absolute);
  if (!stat.isFile() || stat.isSymbolicLink()) throw new Error(`installable path is not a regular file: ${relative}`);
  files[relative] = { mode: stat.mode & 0o777, sha256: sha256(fs.readFileSync(absolute)) };
}
const generated = canonicalJson({ files, formatVersion: 1 });

if (process.argv.includes("--check")) {
  const existing = fs.readFileSync(manifestPath, "utf8");
  if (existing !== generated) {
    process.stderr.write("install-manifest.json is stale; regenerate it from the reviewed payload\n");
    process.exitCode = 1;
  } else process.stdout.write("install-manifest.json is current\n");
} else {
  process.stdout.write(generated);
}
