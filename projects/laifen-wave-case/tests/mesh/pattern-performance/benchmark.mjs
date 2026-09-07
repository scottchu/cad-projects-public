// Run from repository root in a fresh process for each sample.
// Usage: node benchmark.mjs RUNTIME_DIR SOURCE OUT_DIR LABEL STYLE FORMAT ROLE RUN [NAME=VALUE ...]
import {createHash} from 'node:crypto';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {resolve, join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {performance} from 'node:perf_hooks';

const [runtimeArg, sourceArg, outArg, labelArg, style, format, role, run, ...definitions] = process.argv.slice(2);
const styles = ['smooth', 'diamond', 'ribs', 'rings', 'spiral'];
const formats = ['csg', 'stl', 'binstl'];
const roles = ['body', 'cap', 'assembled', 'print_layout'];
if (!runtimeArg || !sourceArg || !outArg || !labelArg || !run
    || !styles.includes(style) || !formats.includes(format) || !roles.includes(role)
    || definitions.some(x => !/^[A-Za-z_][A-Za-z0-9_]*=.+$/.test(x)
      || /^(surface_style|output_mode)=/.test(x))) {
  throw Error('Usage: benchmark.mjs RUNTIME_DIR SOURCE OUT_DIR LABEL STYLE FORMAT ROLE RUN [NAME=VALUE ...]');
}

const runtime = resolve(runtimeArg), sourcePath = resolve(sourceArg), outDir = resolve(outArg);
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const [source, js, wasm] = await Promise.all([
  readFile(sourcePath), readFile(join(runtime, 'openscad.js')), readFile(join(runtime, 'openscad.wasm')),
]);
const runtimeHashes = {js: hash(js), wasm: hash(wasm)};
if (runtimeHashes.js !== '904a47f29e63afb597bedef747da3b457d8ea17cc793c462c6c8b444e918a62e'
    || runtimeHashes.wasm !== 'f72ce246c02c0e501990837102be383326b153fd761774ebfacce5c80c5ecf26') {
  throw Error('Pinned OpenSCAD runtime hash mismatch');
}
const {default: factory} = await import(pathToFileURL(join(runtime, 'openscad.js')));
const messages = [], initializeStart = performance.now();
const mod = await factory({noInitialRun: true, wasmBinary: wasm,
  print: x => messages.push(String(x)), printErr: x => messages.push(String(x))});
const initialized = performance.now();
mod.FS.writeFile('/case.scad', source);
const extension = format === 'csg' ? 'csg' : 'stl';
const argv = ['/case.scad', '--backend=Manifold',
  ...definitions.flatMap(x => ['-D', x]),
  '-D', `surface_style="${style}"`, '-D', `output_mode="${role}"`,
  ...(format === 'binstl' ? ['--export-format', 'binstl'] : []), '-o', `/out.${extension}`];
const callMainStart = performance.now(), code = mod.callMain(argv), callMainEnd = performance.now();
const output = Buffer.from(mod.FS.readFile(`/out.${extension}`, {encoding: 'binary'}));
const readEnd = performance.now();
const fatal = messages.filter(x => /ERROR:|WARNING:|Assertion/.test(x));
if (code || !output.length || fatal.length) throw Error(`Compiler failed (${code}): ${fatal.join('\n')}`);

const renderLine = messages.find(x => x.includes('Total rendering time:')) ?? '';
const renderMatch = renderLine.match(/(\d+):(\d+):([\d.]+)/);
const compilerRenderMs = renderMatch
  ? (Number(renderMatch[1]) * 3600 + Number(renderMatch[2]) * 60 + Number(renderMatch[3])) * 1000
  : null;
const safeLabel = labelArg.replace(/[^A-Za-z0-9_.-]+/g, '-');
const name = `${safeLabel}-${style}-${role}-${format}-${run}`;
await mkdir(outDir, {recursive: true});
const artifact = join(outDir, `${name}.${extension}`);
await writeFile(artifact, output);
const writeEnd = performance.now();
const receipt = {name, sourcePath, sourceSha256: hash(source), runtimeHashes,
  node: process.execPath, argv, code, messages, artifact, bytes: output.length,
  sha256: hash(output), initializeMs: initialized-initializeStart,
  callMainMs: callMainEnd-callMainStart, compilerRenderMs,
  readMs: readEnd-callMainEnd, writeMs: writeEnd-readEnd};
const receiptPath = join(outDir, `${name}.json`);
await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
console.log(JSON.stringify({...receipt, receiptPath}));
