// Run from repository root. Runtime assets stay in scratch, never in Git.
// Usage: node .../compile_pilot.mjs SCRATCH ROLE [spiral|ribs|rings|smooth|diamond] [SOURCE]
// Spiral uses the frozen stress tuple. Smooth/Diamond use original defaults.
import {createHash} from 'node:crypto';
import {readFile, writeFile} from 'node:fs/promises';
import {resolve, join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {performance} from 'node:perf_hooks';

const [scratchArg, role = 'body', style = 'spiral', sourceArg] = process.argv.slice(2);
if (!scratchArg || !['body', 'cap', 'assembled', 'print_layout'].includes(role)
    || !['spiral', 'ribs', 'rings', 'smooth', 'diamond'].includes(style)) throw Error('Invalid pilot arguments');
const scratch = resolve(scratchArg);
const sourcePath = resolve(sourceArg ?? 'projects/laifen-wave-case/openscad/laifen_case_customizer_v1.scad');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const source = await readFile(sourcePath);
const js = await readFile(join(scratch, 'openscad.js'));
const wasm = await readFile(join(scratch, 'openscad.wasm'));
if (hash(js) !== '904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e'
    || hash(wasm) !== 'f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26') throw Error('Pinned runtime mismatch');
const {default: factory} = await import(pathToFileURL(join(scratch, 'openscad.js')));
const fields = ['spiral','ribs','rings'].includes(style) ? ['device_length=55', 'outer_diameter=39.2', 'body_bore=30',
  'cap_bore=31', 'floor_thickness=3', 'split_mode="distance"', 'split_distance_from_top=25.3',
  `wave_spacing=${style==='spiral'?4:6}`, `wave_depth=${style==='spiral'?'.6':'.45'}`, 'drainage_mode="bottom"', 'drain_count=7'] : [];
fields.push(`surface_style="${style}"`, `output_mode="${role}"`);
const name = `${style}-${role}`;
const argv = ['/case.scad', '--backend=Manifold', ...fields.flatMap(x => ['-D', x]), '-o', `/${name}.stl`];
const messages = [], start = performance.now();
const mod = await factory({noInitialRun: true, wasmBinary: wasm,
  print: x => messages.push(String(x)), printErr: x => messages.push(String(x))});
mod.FS.writeFile('/case.scad', source);
const initialized = performance.now();
const code = mod.callMain([...argv]);
if (code || messages.some(x => /ERROR:|WARNING:/.test(x))) throw Error(`Compiler diagnostics: ${messages.join('\n')}`);
const artifact = Buffer.from(mod.FS.readFile(`/${name}.stl`, {encoding: 'binary'}));
const receipt = {status: 'compiled', sourcePath, sourceSha256: hash(source),
  runtime: {jsSha256: hash(js), wasmSha256: hash(wasm)}, argv,
  artifact: join(scratch, `${name}.stl`), sha256: hash(artifact), bytes: artifact.length,
  initializeMs: initialized-start, compileMs: performance.now()-initialized, messages};
await writeFile(receipt.artifact, artifact);
await writeFile(join(scratch, `${name}.json`), `${JSON.stringify(receipt, null, 2)}\n`);
console.log(JSON.stringify(receipt, null, 2));
