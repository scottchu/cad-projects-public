import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const project=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const repo=path.resolve(project,'../..');
const manifest=JSON.parse(await readFile(path.join(project,'slicer/p1-r3-validation/review-media-manifest.json'),'utf8'));
const routes=new Map([['/',['review/p1-r3/slice-review.html','text/html; charset=utf-8']]]);
for(const entry of manifest.entries) routes.set('/media/'+path.basename(entry.path),[path.relative(project,path.join(repo,entry.path)),'image/svg+xml']);
createServer(async(req,res)=>{
 if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
 const raw=new URL(req.url,'http://127.0.0.1').pathname;
 const key=raw==='/grenadier-slice'?'/':raw.replace(/^\/grenadier-slice\//,'/');
 const route=routes.get(key);if(!route){res.writeHead(404);res.end('Not found');return;}
 try{const body=await readFile(path.join(project,route[0]));res.writeHead(200,{'Content-Type':route[1],'Content-Length':body.length,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(req.method==='HEAD'?undefined:body);}catch{res.writeHead(404);res.end('Unavailable');}
}).listen(0,'127.0.0.1',function(){process.stdout.write(JSON.stringify(this.address())+'\n');});
