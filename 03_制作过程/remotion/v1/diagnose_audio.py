import numpy as np,subprocess,json
from pathlib import Path
p=Path(__file__).resolve().parent;d=json.loads((p/'src/timing.json').read_text());ff='/Users/USER/.local/bin/ffmpeg';rate=16000
final=next((p.parents[2]/('02_'+chr(26368)+chr(32456)+chr(36755)+chr(20986))).glob('*.mp4'))
def read(f):return np.frombuffer(subprocess.run([ff,'-v','error','-i',str(f),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-'],capture_output=True,check=True).stdout,dtype='<f4')
a=read(final);w=read(p/'public/media/voice.wav');rows=[]
def match(x,y,base):
 radius=8000;start=max(0,base-radius);finish=min(len(x),base+len(y)+radius);xx=x[start:finish];size=1<<(len(xx)+len(y)-1).bit_length();cc=np.fft.irfft(np.fft.rfft(xx,size)*np.fft.rfft(y[::-1],size),size)[:len(xx)+len(y)-1];valid=cc[len(y)-1:len(xx)];idx=int(np.argmax(valid));seg=xx[idx:idx+len(y)];return float(np.dot(seg,y)/(np.linalg.norm(seg)*np.linalg.norm(y)+1e-20)),(start+idx-base)/rate*1000
for c in d['clips']:
 b=read(c['source']);offset=.7;dur=min(2.5,c['durationInFrames']/60-offset-.2);i=round((c['sourceIn']+offset)*rate);j=round((c['startFrame']/60+offset)*rate);y=b[i:i+round(dur*rate)]
 rows.append({'clip':c['id'],'sourceToPrepared':match(w,y,j),'sourceToFinal':match(a,y,j),'preparedToFinal':match(a,w[j:j+len(y)],j)})
print(json.dumps(rows,indent=2));(p/'qc/final/audio-diagnosis.json').write_text(json.dumps(rows,indent=2))
