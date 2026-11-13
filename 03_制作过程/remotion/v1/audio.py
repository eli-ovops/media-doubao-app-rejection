from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;d=json.loads((P/'src/timing.json').read_text());ff='/Users/USER/.local/bin/ffmpeg'
cmd=[ff,'-nostdin','-hide_banner','-y'];f=[]
for i,c in enumerate(d['clips']):
 cmd+=['-i',c['source']]
 f.append(f'[{i}:a]atrim=start={c["sourceIn"]}:end={c["sourceOut"]},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.008,afade=t=out:st={c["durationInFrames"]/60-.008}:d=0.008[a{i}]')
f.append(''.join(f'[a{i}]' for i in range(len(d['clips'])))+f'concat=n={len(d["clips"])}:v=0:a=1,highpass=f=70,loudnorm=I=-16:TP=-2:LRA=9:print_format=json[out]')
cmd+=['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le',str(P/'public/media/voice.wav')]
r=subprocess.run(cmd,capture_output=True,text=True);(P/'qc/audio-preparation.log').write_text(r.stderr);print('audio',r.returncode);print(r.stderr[-700:])
