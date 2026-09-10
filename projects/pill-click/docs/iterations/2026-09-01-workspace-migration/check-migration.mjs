// Source-preserving migration audit; writes generated evidence only with --record.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';

const evidence = path.dirname(fileURLToPath(import.meta.url));
const destination = path.resolve(evidence, '../../..');
const source = '/Users/scottchu/Projects/personal/3d-print/design/pill-click';
const originLegacy = '/Users/scottchu/Projects/personal/3d-print/pill_click/p1_hollow_magnetic_dispenser/spec.py';
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const digest = filename => sha(fs.readFileSync(filename));
function walk(root, rel = '') {
  return fs.readdirSync(path.join(root, rel), {withFileTypes: true}).flatMap(entry => {
    const child = path.join(rel, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`Unexpected symlink: ${child}`);
    return entry.isDirectory() ? walk(root, child) : [child];
  }).sort();
}
const exclusions = new Set(['uv.lock', '.venv', '__pycache__', '.pytest_cache', '.DS_Store']);
const record = process.argv.includes('--record');
let manifest;
if (record) {
  if (fs.existsSync(path.join(evidence, 'source-manifest.json'))) throw new Error('Refusing to overwrite frozen source manifest');
  const included = [], excluded = [];
  for (const rel of walk(source)) {
    const hash = digest(path.join(source, rel));
    if (rel.split(path.sep).some(part => exclusions.has(part))) {
      excluded.push({source: rel, sha256: hash, reason: 'Nested lock/environment/cache or filesystem metadata'});
      continue;
    }
    const dest = rel === 'README.md' ? 'docs/legacy/README.source.md' : rel;
    if (digest(path.join(destination, dest)) !== hash) throw new Error(`Copy mismatch: ${rel}`);
    included.push({source: rel, destination: dest, sha256: hash, bytes: fs.statSync(path.join(source, rel)).size});
  }
  const legacy = {source: originLegacy, destination: 'docs/legacy/root-pill-click/spec.py', sha256: digest(originLegacy)};
  if (digest(path.join(destination, legacy.destination)) !== legacy.sha256) throw new Error('Legacy mismatch');
  manifest = {origin_baseline: '96b055d4b8d0b87f3e6132fa3d90b23b3be4ed84', source, destination, hash_method: 'SHA-256 file bytes; sorted relative paths', included, excluded, external_legacy: [legacy]};
  fs.writeFileSync(path.join(evidence, 'source-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
} else {
  manifest = JSON.parse(fs.readFileSync(path.join(evidence, 'source-manifest.json'), 'utf8'));
  for (const item of [...manifest.included, ...manifest.external_legacy]) {
    if (digest(path.join(destination, item.destination)) !== item.sha256) throw new Error(`Destination mismatch: ${item.destination}`);
    const original = path.isAbsolute(item.source) ? item.source : path.join(source, item.source);
    if (fs.existsSync(original) && digest(original) !== item.sha256) throw new Error(`Source changed: ${original}`);
  }
}
const contracts = ['docs/REQUIREMENTS.md', 'docs/iterations/2026-09-01-workspace-migration/DESIGN.md'];
const brief = fs.readFileSync(path.join(evidence, 'BRIEF.md'), 'utf8').split('## Frozen design contract\n')[1].split('## Mutable delegated execution plan')[0];
const lines = [...manifest.included, ...manifest.external_legacy].map(item => `${item.sha256}  ${item.destination}`);
for (const rel of contracts) lines.push(`${digest(path.join(destination, rel))}  ${rel}`);
lines.push(`${sha(brief)}  docs/iterations/2026-09-01-workspace-migration/BRIEF.md#frozen-design-contract`);
const candidate = lines.sort().join('\n') + '\n';
if (record) fs.writeFileSync(path.join(evidence, 'candidate.sha256'), candidate);
else if (candidate !== fs.readFileSync(path.join(evidence, 'candidate.sha256'), 'utf8')) throw new Error('Candidate contract fingerprint changed');
console.log(JSON.stringify({status: 'PASS', included: manifest.included.length, excluded: manifest.excluded.length, external_legacy: manifest.external_legacy.length, manifest_sha256: digest(path.join(evidence, 'source-manifest.json')), candidate_sha256: sha(candidate)}, null, 2));
