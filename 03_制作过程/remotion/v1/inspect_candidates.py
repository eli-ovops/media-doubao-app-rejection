from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;A=Path('/Volumes/EXTERNAL/自媒体/资产库/FredTalk/组件视频');rows={}
for f in P.glob('qc/S*-candidates.json'):
 for e in json.loads(f.read_text())['candidates'][:3]:rows[e['label']]=e
out=[]
for label,e in rows.items():
 files=list(A.glob(label+'-1-preview.mp4')) or list(A.glob(label+'-preview.mp4'))
 if not files: print('MISSING',label);continue
 src=files[0];dst=P/f'qc/candidate-{label}.jpg';cmd=['/Users/USER/.local/bin/ffmpeg','-v','error','-y','-i',str(src),'-vf','fps=1/1.5,scale=320:-1,tile=3x1','-frames:v','1',str(dst)];r=subprocess.run(cmd,capture_output=True,text=True)
 if r.returncode:print(r.stderr);continue
 out.append({'id':e['id'],'label':label,'preview':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'contact':str(dst),'range':'nominal0,1.5,3.0s samples; not continuous'})
for j in range(0,len(out),5):
 batch=out[j:j+5];im=Image.new('RGB',(960,len(batch)*210),'#ddd');draw=ImageDraw.Draw(im)
 for i,r in enumerate(batch):
  frame=Image.open(r['contact']);im.paste(frame,(0,i*210+24));draw.text((5,i*210+5),r['label'],fill='#111')
 im.save(P/f'qc/candidates-overview-{j//5}.jpg')
(P/'qc/candidate-inspection-files.json').write_text(json.dumps(out,indent=2));print('candidate files',len(out))
