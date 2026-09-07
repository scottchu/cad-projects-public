/** Request ownership is reserved before all asynchronous identity work. */
export class Generation {
  constructor({prepare,createWorker,onState=()=>{},onLog=()=>{},onResult=()=>{},setTimer=(...args)=>globalThis.setTimeout(...args),clearTimer=(...args)=>globalThis.clearTimeout(...args),timeout=180000}) {
    Object.assign(this,{prepare,createWorker,onState,onLog,onResult,setTimer,clearTimer,timeout});
    this.epoch=0; this.worker=null; this.timer=null;
  }
  release() { this.clearTimer(this.timer); this.timer=null; this.worker?.terminate(); this.worker=null; }
  invalidate(message='Generate to update the preview.') { ++this.epoch; this.release(); this.onState({busy:false,current:false,message}); }
  async generate(values) {
    const epoch=++this.epoch; this.release();
    const owned=()=>this.epoch===epoch;
    this.onState({busy:true,current:false,message:'Loading compiler…'});
    const fail=message=>{if(!owned())return; ++this.epoch;this.release();this.onState({busy:false,current:false,message});};
    this.timer=this.setTimer(()=>fail('Compiler timed out. Generate to try again.'),this.timeout);
    try {
      const request=await this.prepare(values);
      if (!owned()) return;
      const worker=this.worker=this.createWorker();
      worker.onerror=event=>fail(`Compiler could not start. ${event.message || 'Generate to try again.'}`);
      worker.onmessage=event=>{
        const d=event.data;
        if(!owned() || d.id!==epoch) return;
        if(d.type==='stage') this.onState({busy:true,current:false,message:`${d.stage}…`});
        if(d.type==='log') this.onLog(d.text);
        if(d.type==='error') {this.onLog(d.error);fail('Generation failed. Open compiler details for more information.');}
        if(d.type==='result') {
          if(d.identity!==request.identity || d.sourceHash!==request.sourceHash || d.lockFingerprint!==request.lockFingerprint) return fail('The compiler result could not be verified. Generate to try again.');
          if(!(d.bytes instanceof ArrayBuffer) && !ArrayBuffer.isView(d.bytes)) return fail('The compiler returned no STL. Generate to try again.');
          const bytes=d.bytes instanceof ArrayBuffer ? new Uint8Array(d.bytes) : new Uint8Array(d.bytes.buffer,d.bytes.byteOffset,d.bytes.byteLength);
          if(!bytes.byteLength) return fail('The compiler returned an empty STL. Generate to try again.');
          // Retire this epoch so even queued duplicate results cannot be accepted.
          ++this.epoch; this.release();
          this.onResult({bytes,values,identity:request.identity});
          this.onState({busy:false,current:true,message:'Preview up to date'});
        }
      };
      worker.postMessage({...request,type:'compile',id:epoch});
    } catch(error) {fail(`Generation failed. ${error.message}`);}
  }
}
export const exactSTLBlob=bytes=>new Blob([bytes],{type:'model/stl'});
