# coding: utf-8
"""Exact six-file offline intake; writes only this task's flow/02."""
from pathlib import Path
import subprocess,json,hashlib,wave,math,time
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
TASK=ROOT.parent.parent
FF='/Users/USER/.local/bin/ffmpeg'
AV='/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe'
WH='/Volumes/EXTERNAL/Tools/Whisper/bin/whisper-cli'
MODEL='/Volumes/EXTERNAL/Tools/Whisper/models/ggml-base.bin'
sources=json.loads((TASK/'素材初核.json').read_text())
record={'status':'RUNNING','method':'offline ffmpeg + AVFoundation avprobe + whisper.cpp/base CPU','direct_hearing':False,'continuous_viewing':False,'sources':[],'created_files':[]}
def save():
    record['created_files']=[str(p) for p in ROOT.rglob('*') if p.is_file()]
    (ROOT/'read-evidence.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
for row in sources:
    idx=row['provided_order'];src=Path(row['path']);d=ROOT/f'raw-{idx:02d}';d.mkdir(exist_ok=True)
    meta=json.loads(subprocess.check_output([AV,'-v','error','-show_format','-show_streams','-of','json',str(src)]))
    duration=float(meta['format']['duration'])
    item={'provided_order':idx,'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':src.stat().st_size,'metadata':meta,'duration':duration,'output_directory':str(d)}
    record['sources'].append(item);save()
    with (d/'decode.log').open('w') as log:
        subprocess.run([FF,'-nostdin','-hide_banner','-loglevel','error','-n','-i',str(src),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(d/'audio.wav')],stdout=log,stderr=log,check=True)
    cmd=[WH,'-m',MODEL,'-f',str(d/'audio.wav'),'-l','zh','-t','4','-ml','24','-otxt','-osrt','-ojf','-of',str(d/'asr')]
    with (d/'asr.log').open('w') as log:
        subprocess.run(cmd,stdout=log,stderr=log,check=True)
    item['asr_command']=cmd;item['asr_status']='SUCCESS'
    with (d/'signal.log').open('w') as log:
        subprocess.run([FF,'-nostdin','-hide_banner','-i',str(src),'-vn','-af','silencedetect=noise=-38dB:d=0.25,astats=metadata=0:reset=0','-f','null','-'],stdout=log,stderr=log,check=True)
    (d/'frames').mkdir(exist_ok=True)
    times=[round(t,3) for t in range(0,math.ceil(duration),2) if t<duration]+[round(max(0,duration-0.25),3)]
    for j,t in enumerate(times):
        subprocess.run([FF,'-nostdin','-hide_banner','-loglevel','error','-n','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=360:640','-q:v','3',str(d/'frames'/f'{j:03d}-{t:.3f}.jpg')],check=True)
    item['sample_times']=times;item['sampling_interval_seconds']=2;item['sampling_limit']='Seek target times, sparse images; intervening motion/audio not viewed. Last sample at duration-0.25.'
    framefiles=sorted((d/'frames').glob('*.jpg'));sheets=[]
    for start in range(0,len(framefiles),12):
        group=framefiles[start:start+12];sheet=Image.new('RGB',(4*240,3*450),(22,22,22));draw=ImageDraw.Draw(sheet)
        for k,f in enumerate(group):
            im=Image.open(f);im.thumbnail((240,426));x=(k%4)*240;y=(k//4)*450;sheet.paste(im,(x,y));draw.text((x+5,y+428),f'raw{idx:02d} {times[start+k]:.3f}s',fill='white')
        target=d/f'sheet-{start//12+1}.jpg';sheet.save(target,quality=90);sheets.append(str(target))
    item['contact_sheets']=sheets;item['status']='COMPLETE';save()
    print(json.dumps({'raw':idx,'duration':duration,'asr':str(d/'asr.txt'),'sheets':sheets}),flush=True)
record['status']='COMPLETE';save()
