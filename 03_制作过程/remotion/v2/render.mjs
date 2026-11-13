import path from 'node:path';import {fileURLToPath} from 'node:url';import {bundle} from '@remotion/bundler';import {selectComposition,renderMedia} from '@remotion/renderer';
const root=path.dirname(fileURLToPath(import.meta.url));
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.tsx'),publicDir:path.join(root,'public'),outDir:path.join(root,'render/bundle')});
const base={serveUrl,browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'angle'},logLevel:'warn',timeoutInMilliseconds:90000};
const composition=await selectComposition({...base,id:'DoubaoFull'});
for(const [name,start,end] of [['news',384,650],['ending',6726,6779]]){
 await renderMedia({...base,composition,codec:'h264',frameRange:[start,end],outputLocation:path.join(root,`render/${name}.mp4`),concurrency:1,crf:15,pixelFormat:'yuv420p',muted:true,onProgress:v=>{const n=Math.floor(v.progress*10);if(n!==globalThis.last){console.log(name,n*10);globalThis.last=n;}}});
}
