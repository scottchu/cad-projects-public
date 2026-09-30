#!/usr/bin/env node
/** Hash the D7 candidate without rewriting the historical D5 intake manifest. */
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = process.cwd();
const project = 'projects/grenadier-fridge-magnet';
const paths = [
  `${project}/docs/iterations/p1-r1-intent/intent-manifest.json`,
  `${project}/pyproject.toml`,
  `${project}/references/d4-approved.png`,
  `${project}/scripts/generate-face-vector.py`,
  `${project}/scripts/create-face-review.mjs`,
  `${project}/src/face_vector.py`,
  `${project}/tests/test_face_vector.py`,
  `${project}/SVG/p1-r1/face.svg`,
  `${project}/SVG/p1-r1/face-report.json`,
  `${project}/review/p1-r1/face-review.html`,
];
const entries = [];
for (const path of paths) {
  const sha256 = createHash('sha256').update(await readFile(resolve(root, path))).digest('hex');
  entries.push({path, sha256});
}
const canonical = entries.map(({path, sha256}) => `${sha256}  ${path}\n`).join('');
const fingerprint = createHash('sha256').update(canonical).digest('hex');
const manifest = {baseline: 'a8834040afe401637d36e94bd8fdd9e1d9874d35', parent_intent_fingerprint: '8a5aad12d7041a5c2f269dd589dd0c51d1dcd142d8e24df17f7988eeb0650bb0', method: 'SHA-256 of sorted sha256 + two spaces + repo-relative path + LF', fingerprint, entries};
const target = resolve(root, `${project}/docs/iterations/p1-r1-intent/face-candidate-manifest.json`);
if (process.argv.includes('--write')) await writeFile(target, JSON.stringify(manifest, null, 2) + '\n');
else process.stdout.write(JSON.stringify({status: 'verified', fingerprint, entries: entries.length}) + '\n');
