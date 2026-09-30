import fs from 'node:fs';
import crypto from 'node:crypto';
const p = 'projects/grenadier-fridge-magnet/';
const i = p + 'docs/iterations/p1-r1-intent/';
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const paths = ['AGENTS.md', 'docs/CAD_WORKFLOW.md', 'docs/PROJECT_CONTINUITY.md', 'docs/FDM_DESIGN_RULES.md', p+'docs/REQUIREMENTS.md', p+'docs/decisions/0001-face-first.md', p+'references/d4-approved.png', p+'references/photo-6-original.jpg', p+'tests/README.md', p+'pyproject.toml', p+'scripts/intent-manifest.mjs', i+'BRIEF.md#frozen', i+'DESIGN.md#frozen'].sort();
const entries = paths.map(path => {
  const section = path.endsWith('#frozen');
  let bytes = fs.readFileSync(section ? path.slice(0, -7) : path);
  if(section){
    const text = bytes.toString('utf8');
    const match = text.match(/<!-- frozen:start -->([\s\S]*?)<!-- frozen:end -->/);
    if(!match) throw new Error('Missing frozen section: '+path);
    bytes = Buffer.from(match[1]);
  }
  return {path, sha256: hash(bytes)};
});
const canonical = entries.map(e => e.sha256+'  '+e.path+'\n').join('');
const result = {baseline:'a8834040afe401637d36e94bd8fdd9e1d9874d35', fingerprint: hash(canonical), method:'SHA-256 of sorted sha256 + two spaces + repo-relative path + LF; #frozen bytes between markers, excluding markers', entries};
const target = i+'intent-manifest.json';
if(process.argv.includes('--write')) fs.writeFileSync(target, JSON.stringify(result,null,2)+'\n');
else {
  const expected = JSON.parse(fs.readFileSync(target,'utf8'));
  if(JSON.stringify(expected) !== JSON.stringify(result)) throw new Error('Frozen input mismatch; dependent gates invalidated');
}
console.log(JSON.stringify({status:process.argv.includes('--write')?'frozen':'verified', fingerprint:result.fingerprint, entries:entries.length}));
