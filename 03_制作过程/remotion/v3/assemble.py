from pathlib import Path
import json,hashlib,subprocess,os,shutil,difflib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;old=p.parent/'v2';n=p.parents[2];q=p/'qc';prior=json.loads((old/'qc/delivery.json').read_text());base=Path(prior['path']);out=base.parent;dest=base.with_name(base.name.replace('-v2','-v3'));ff='/Users/USER/.local/bin/ffmpeg'
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest();assert h(base)==prior['sha256']=='8ab3d6a5836de740512e084b8ff51ee3fb14f33d529dacfce9084b234d0ba721'
env=os.environ.copy();comp=(p/'node_modules/@remotion/compositor-darwin-arm64').resolve();env['DYLD_LIBRARY_PATH']=str(comp)
def run(cmd,name):
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);(q/name).write_bytes(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(name+': '+str(r.returncode))
 return r
fil="[0:v]settb=expr=1/60,setpts=N[b];[1:v]scale=in_range=auto:out_range=tv,format=yuv420p,setrange=limited,settb=expr=1/60,setpts=N+4944[p];[b][p]overlay=0:0:enable='gte(t,82.39999)*lt(t,87.09999)'[out]"
run([ff,'-y','-i',str(base),'-i',str(p/'render/Q01.mp4'),'-filter_complex',fil,'-map','[out]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v','6780','-movflags','+faststart',str(dest)],'assemble.log')
r=run([str(comp/'ffprobe'),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dest)],'probe.json');probe=json.loads(r.stdout);v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],int(v['nb_read_frames']),v['r_frame_rate'])==(1080,1920,6780,'60/1');assert float(v['duration'])==113 and float(a['start_time'])==0 and float(a['duration'])==113
run([ff,'-v','error','-i',str(dest),'-f','null','-'],'decode.log')
hashes=[]
for name,f in [('v2',base),('v3',dest)]:
 r=run([ff,'-v','error','-i',str(f),'-map','0:a:0','-c:a','pcm_s16le','-f','hash','-hash','sha256','-'],f'audio-{name}-hash.txt');hashes.append(r.stdout.decode().strip())
assert hashes[0]==hashes[1]
frames=q/'frames';frames.mkdir(exist_ok=True)
run([ff,'-y','-ss','82.2','-i',str(dest),'-t','5.1','-vf','fps=20,scale=216:384','-q:v','3',str(frames/'f-%03d.jpg')],'sampling.log')
imgs=sorted(frames.glob('*.jpg'))
for off in range(0,len(imgs),15):
 im=Image.new('RGB',(1080,1230),'#e6e6e6');draw=ImageDraw.Draw(im)
 for i,fn in enumerate(imgs[off:off+15]):
  x=i%5*216;y=i//5*410;im.paste(Image.open(fn),(x,y));draw.text((x+5,y+386),f'{82.2+(off+i+.5)/20:.3f}s',fill='black')
 im.save(q/f'Q01-motion-{off//15+1:02d}.jpg',quality=94)
for t in [82.4,82.6,83.5,84.5,85,85.5,86.05,86.15,86.5,86.75,86.85,87.1]:
 run([ff,'-y','-ss',str(t),'-i',str(dest),'-frames:v','1','-q:v','2',str(q/f'native-{t}.jpg')],f'native-{t}.log')
for ext in ['*.srt','*.jpg']:
 for f in out.glob(ext):
  if '-v2' in f.name:shutil.copy2(f,f.with_name(f.name.replace('-v2','-v3')))
assert h(p/'subtitles.srt')==h(old/'subtitles.srt');assert h(p/'src/Film.tsx')==h(old/'src/Film.tsx')
(q/'source-diff.patch').write_text(''.join(difflib.unified_diff((old/'src/components/Actions.tsx').read_text().splitlines(True),(p/'src/components/Actions.tsx').read_text().splitlines(True),fromfile='v2/Actions.tsx',tofile='v3/Actions.tsx')))
r={'content_id':'doubao-app-rejection-20261016','version':'v3','path':str(dest),'sha256':h(dest),'bytes':dest.stat().st_size,'width':1080,'height':1920,'fps':60,'frames':6780,'duration':113,'renderedRangeFramesInclusive':[4944,5225],'renderedFrames':282,'renderedSeconds':4.7,'fullDecode':'PASS','audioPcmIdentity':hashes[0],'audioIdenticalToV2':True,'audioStart':a['start_time'],'audioDuration':a['duration'],'srtIdenticalToV2':True,'FilmTsxIdenticalToV2':True,'visualSampleReview':'PENDING','directHearing':'UNKNOWN','continuousAudiovisualReview':'UNKNOWN','pmoAcceptance':'PENDING'}
(q/'delivery.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
