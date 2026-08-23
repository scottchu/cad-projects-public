import { stat } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";

const root = import.meta.dir;
const host = process.env.KAGE_HOST ?? "127.0.0.1";
const port = Number(process.env.KAGE_PORT ?? "4180");

const contentTypes: Record<string, string> = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".wasm": "application/wasm",
};

Bun.serve({
  hostname: host,
  port,
  async fetch(request) {
    const url = new URL(request.url);
    const decodedPath = decodeURIComponent(url.pathname);
    let path = resolve(root, `.${decodedPath}`);
    if (path !== root && !path.startsWith(`${root}${sep}`)) {
      return new Response("Forbidden", { status: 403 });
    }

    try {
      if ((await stat(path)).isDirectory()) path = resolve(path, "index.html");
    } catch {
      return new Response("Not found", { status: 404 });
    }

    const file = Bun.file(path);
    if (!(await file.exists())) return new Response("Not found", { status: 404 });
    return new Response(file, {
      headers: {
        "Cache-Control": "no-store",
        "Content-Type": contentTypes[extname(path)] ?? "application/octet-stream",
      },
    });
  },
});

console.log(`KAGE simulator: http://${host}:${port}/index.html`);
