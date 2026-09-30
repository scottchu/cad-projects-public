#!/usr/bin/env node
/** Build the portable D4 / native SVG comparison page. */
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const project = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = await readFile(resolve(project, 'references/d4-approved.png'));
const svg = await readFile(resolve(project, 'SVG/p1-r1/face.svg'), 'utf8');
const output = resolve(project, 'review/p1-r1/face-review.html');
const sourceUrl = `data:image/png;base64,${source.toString('base64')}`;
const classes = [['black', '黑'], ['gray', '灰'], ['white', '白'], ['deep-blue', '車牌深藍'], ['glass-mix', '玻璃淡藍（藍＋白）']];
const controls = classes.map(([id, label]) => `<label><input type="checkbox" data-region="${id}" checked> ${label}</label>`).join('');
const html = `<!doctype html>
<html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Grenadier D4 正面五色分區對照</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#101217;color:#edf0f5;font:16px system-ui,sans-serif}main{max-width:1500px;margin:auto;padding:18px 24px}h1{font-size:24px;margin:0 0 5px}.status{color:#b8d9ec;margin:0}.controls{display:flex;gap:14px;flex-wrap:wrap;padding:10px 0}.controls label{padding:5px 9px;border:1px solid #3b414c;border-radius:5px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:#1b1f27;border:1px solid #333946;border-radius:9px;padding:12px}.card h2{font-size:18px;margin:0 0 8px}.art{height:60vh;overflow:hidden;background:#f8f8f8}.art img,.art svg{display:block;width:100%;height:100%;min-width:0;object-fit:contain}.art.zoom{overflow:auto}.art.zoom svg{width:150%;height:auto;min-width:560px}.note{line-height:1.45;color:#c7ccd6;margin:7px 0}button{padding:6px 10px}@media(max-width:850px){.grid{grid-template-columns:1fr}}
</style>
<main><h1>正面分色確認</h1><p class="status">2D 預覽，尚非可列印檔案。</p>
<p class="note">左邊是已確認圖片；右邊是分色輪廓。白色保留車貼白邊，外面白底沒有算進去。</p>
<div class="controls">${controls}<button type="button" id="zoom">放大／還原</button></div>
<div class="grid"><section class="card"><h2>已確認圖片</h2><div class="art"><img alt="已確認的 Grenadier 圖片" src="${sourceUrl}"></div></section><section class="card"><h2>分色輪廓</h2><div class="art" id="vector">${svg}</div></section></div>
<p class="note">請看車外輪廓和白邊、四盞圓燈、GRENADIER、DJZY 608、前擋玻璃是否都有保留。<strong>通過／不通過：這仍是你確認的正面嗎？</strong></p></main>
<script>const v=document.querySelector('#vector svg'),pane=document.querySelector('#vector');for(const c of document.querySelectorAll('[data-region]'))c.onchange=()=>v.querySelector('#'+c.dataset.region).style.display=c.checked?'':'none';document.querySelector('#zoom').onclick=()=>pane.classList.toggle('zoom');</script>
</html>\n`;
await mkdir(dirname(output), {recursive:true});
await writeFile(output, html);
console.log(output);
