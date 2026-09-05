import { createHash } from "node:crypto";
import { mkdir, readFile, rename, rm, stat, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const exec = promisify(execFile);
const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "..");
const lock = JSON.parse(await readFile(join(root, "dependency-lock.json"), "utf8"));
const vendor = join(root, "vendor");
const temp = join(root, `.openscad-${process.pid}.zip`);
const hash = bytes => createHash("sha256").update(bytes).digest("hex");

const response = await fetch(lock.url, { redirect: "error" });
if (!response.ok || new URL(response.url).hostname !== "files.openscad.org") throw new Error("official OpenSCAD fetch failed");
const archive = new Uint8Array(await response.arrayBuffer());
if (archive.byteLength !== lock.archiveBytes || hash(archive) !== lock.archiveSha256) throw new Error("OpenSCAD archive provenance mismatch");
await writeFile(temp, archive);
const stage = `${vendor}.staging-${process.pid}`;
await rm(stage, { recursive: true, force: true });
await mkdir(stage, { recursive: true });
try {
  await exec("unzip", ["-qq", temp, "openscad.js", "openscad.wasm", "-d", stage]);
  for (const [name, size] of Object.entries(lock.members)) {
    const path = join(stage, name);
    if ((await stat(path)).size !== size) throw new Error(`unexpected ${name} size`);
    if (hash(await readFile(path)) !== lock.installedSha256[name]) throw new Error(`unexpected ${name} hash`);
  }
  // A verified staging directory replaces the cache only after all checks.
  const backup = `${vendor}.previous-${process.pid}`;
  await rm(backup, { recursive: true, force: true });
  try { await rename(vendor, backup); } catch (error) { if (error.code !== "ENOENT") throw error; }
  await rename(stage, vendor);
  await rm(backup, { recursive: true, force: true });
} finally {
  await rm(temp, { force: true });
  await rm(stage, { recursive: true, force: true });
}
