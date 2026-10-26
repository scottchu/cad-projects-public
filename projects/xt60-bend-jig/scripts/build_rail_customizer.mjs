import {readFile, writeFile} from 'node:fs/promises';
const root = new URL('../', import.meta.url);
const source = new URL('preview/rail-customizer/', root);
const styles = await readFile(new URL('styles.css', source), 'utf8');
let html = await readFile(new URL('index.html', source), 'utf8');
html = html.replace('<link rel="stylesheet" href="styles.css">', () => `<style>\n${styles}\n</style>`);
async function inline() {
  for (const name of ['geometry.js', 'ui.js']) {
    const script = await readFile(new URL(name, source), 'utf8');
    if (/<\/script/i.test(script)) throw new Error(`Unsafe inline script closing tag in ${name}`);
    html = html.replace(`<script src="${name}"></script>`, () => `<script>\n${script}\n</script>`);
  }
  await writeFile(new URL('preview/xt60-rail-customizer.html', root), html);
  console.log('Built offline preview/xt60-rail-customizer.html');
}
await inline();
