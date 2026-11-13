from pathlib import Path
import subprocess,json,numpy as np
p=Path(__file__).resolve().parent;n=p.parents[2]
d=json.loads((p/'src/timing.json').read_text());f=next((n/('02_'+chr(26368)+chr(32456)+chr(36755)+chr(20986))).glob('*.mp4'))
ff='/Users/USER/.local/bin/ffmpeg';rate=16000
raw=subprocess.run([ff,'-v','error','-i',str(f),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-'],capture_output=True,check=True).stdout
a=np.frombuffer(raw,dtype='<f4');rows=[]
for c in d['clips']:
 duration=min(2.5,c['durationInFrames']/60-.3);source_start=c['sourceIn']+.15;target_start=c['startFrame']/60+.15
 r=subprocess.run([ff,'-v','error','-ss',str(source_start),'-i',c['source'],'-t',str(duration),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-'],capture_output=True,check=True)
 b=np.frombuffer(r.stdout,dtype='<f4');base=round(target_start*rate);scores=[]
 for shift in range(-320,321,8):
  aa=a[base+shift:base+shift+len(b)];bb=b[:len(aa)]
  if len(aa)!=len(b):continue
  score=float(np.dot(aa,bb)/(np.linalg.norm(aa)*np.linalg.norm(bb)+1e-12));scores.append((score,shift))
 score,shift=max(scores);rows.append({'clip':c['id'],'targetStart':target_start,'sourceStart':source_start,'windowSeconds':duration,'normalizedCorrelation':score,'bestLagMilliseconds':shift/rate*1000})
result={'method':'Mono 16 kHz waveform correlation over a 2.5-second interior window of each retained clip; lag search +/-20 ms at 0.5 ms steps. Not speech recognition or direct hearing.','rows':rows,'audioTimelineCheck':'PASS' if all(r['normalizedCorrelation']>.9 and abs(r['bestLagMilliseconds'])<10 for r in rows) else 'REVIEW'}
(p/'qc/final/audio-correlation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
