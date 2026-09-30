import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const project = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repository = path.resolve(project, '../..');
const routes = new Map([
  ['/', ['review/p1-r2/parametric-review.html', 'text/html; charset=utf-8', 'inline']],
  ['/index.html', ['review/p1-r2/parametric-review.html', 'text/html; charset=utf-8', 'inline']],
  ['/models/flat.glb', ['GLB/p1-r2-color-corrected/flat.glb', 'model/gltf-binary', 'inline']],
  ['/models/relief.glb', ['GLB/p1-r2-color-corrected/relief.glb', 'model/gltf-binary', 'inline']],
  ['/vendor/three.module.js', ['../../node_modules/three/build/three.module.js', 'text/javascript; charset=utf-8', 'inline']],
  ['/vendor/three.core.js', ['../../node_modules/three/build/three.core.js', 'text/javascript; charset=utf-8', 'inline']],
  ['/vendor/addons/controls/OrbitControls.js', ['../../node_modules/three/examples/jsm/controls/OrbitControls.js', 'text/javascript; charset=utf-8', 'inline']],
  ['/vendor/addons/loaders/GLTFLoader.js', ['../../node_modules/three/examples/jsm/loaders/GLTFLoader.js', 'text/javascript; charset=utf-8', 'inline']],
  ['/vendor/addons/utils/BufferGeometryUtils.js', ['../../node_modules/three/examples/jsm/utils/BufferGeometryUtils.js', 'text/javascript; charset=utf-8', 'inline']],
]);

const server = createServer(async (request, response) => {
  if (!['GET', 'HEAD'].includes(request.method ?? '')) { response.writeHead(405); response.end(); return; }
  const rawPath = new URL(request.url ?? '/', 'http://127.0.0.1').pathname;
  const pathname = rawPath === '/grenadier-model' ? '/' : rawPath.replace(/^\/grenadier-model\//, '/');
  const route = routes.get(pathname);
  if (!route) { response.writeHead(404); response.end('Not found'); return; }
  try {
    const [relative, type, disposition] = route;
    const base = relative.startsWith('../../node_modules/') ? project : project;
    const body = await readFile(path.resolve(base, relative));
    response.writeHead(200, {'Content-Type':type, 'Content-Length':body.length, 'Content-Disposition':disposition, 'Cache-Control':'no-store', 'X-Content-Type-Options':'nosniff'});
    response.end(request.method === 'HEAD' ? undefined : body);
  } catch (error) {
    response.writeHead(error.code === 'ENOENT' ? 404 : 500); response.end('Unavailable');
  }
});

server.listen(0, '127.0.0.1', () => process.stdout.write(`${JSON.stringify(server.address())}\n`));
