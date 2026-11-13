from pathlib import Path
import subprocess,json,hashlib,shutil,os
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;n=p.parents[2];q=p/'qc'/'final';q.mkdir(parents=True,exist_ok=True)
out=n/'02_最终输出';out.mkdir(exist_ok=True)
f=p/'render/film-picture-audio.mp4';dest=out/'豆包App拒绝-完整片-v1.mp4'
ff='/Users/USER/.local/bin/ffmpeg'
comp=(p/'node_modules/@remotion/compositor-darwin-arm64').resolve()
env=os.environ.copy();env['DYLD_LIBRARY_PATH']=str(comp)
def run(cmd,log):
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
 (q/log).write_bytes(r.stdout+r.stderr)
 if r.returncode: raise RuntimeError(f'{log}: exit {r.returncode}')
 return r
# Put metadata at the front without re-encoding the actual render.
patch=p/'qc/cutfix-5557.png'
if patch.exists():
 run([ff,'-y','-i',str(f),'-i',str(patch),'-filter_complex',"[0:v]scale=in_range=pc:out_range=tv,format=yuv420p,setrange=limited[b];[1:v]scale=in_range=pc:out_range=tv,format=yuv420p,setrange=limited[p];[b][p]overlay=0:0:enable='eq(n,5557)'[v]",'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-af','atrim=start_sample=2048,asetpts=PTS-STARTPTS,apad,atrim=duration=113','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(dest)],'cutfix-encode.log')
else:
 run([ff,'-y','-i',str(f),'-map','0:v:0','-map','0:a:0','-c','copy','-movflags','+faststart',str(dest)],'remux.log')
r=run([str(comp/'ffprobe'),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dest)],'probe.json')
d=json.loads(r.stdout);v=next(x for x in d['streams'] if x['codec_type']=='video');a=next(x for x in d['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'60/1',6780),v
assert v['codec_name']=='h264' and a['codec_name']=='aac'
assert abs(float(v['duration'])-113)<.02 and abs(float(a['duration'])-113)<.05
run([ff,'-v','error','-i',str(dest),'-f','null','-'],'decode.log')
run([ff,'-hide_banner','-i',str(dest),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=9:print_format=json','-f','null','-'],'loudness.log')
run([ff,'-hide_banner','-i',str(dest),'-vn','-af','silencedetect=noise=-45dB:d=0.5','-f','null','-'],'silence.log')
frames=q/'frames';frames.mkdir(exist_ok=True)
run([ff,'-y','-i',str(dest),'-vf','fps=1,scale=270:480','-q:v','3',str(frames/'f-%03d.jpg')],'sampling.log')
files=sorted(frames.glob('f-*.jpg'))
for off in range(0,len(files),12):
 im=Image.new('RGB',(1080,1548),'#e5e5e5');draw=ImageDraw.Draw(im)
 for i,fn in enumerate(files[off:off+12]):
  x=(i%4)*270;y=(i//4)*516
  im.paste(Image.open(fn),(x,y));draw.text((x+8,y+484),f'{off+i+0.5:.1f}s',fill='black')
 im.save(q/f'contact-{off//12+1:02d}.jpg',quality=92)
# Short windows across every editorial scene junction, 10 fps; not continuous viewing.
cuts=[10.85,29.55,55.6,63.55,92.616667,97.2]
for k,t in enumerate(cuts):
 dr=q/f'cut-{k+1}';dr.mkdir(exist_ok=True)
 run([ff,'-y','-ss',str(t-.5),'-i',str(dest),'-t','1','-vf','fps=10,scale=216:384','-q:v','3',str(dr/'f-%02d.jpg')],f'cut-{k+1}.log')
 im=Image.new('RGB',(1080,820),'#e5e5e5');draw=ImageDraw.Draw(im)
 for i,fn in enumerate(sorted(dr.glob('*.jpg'))):
  x=(i%5)*216;y=(i//5)*410;im.paste(Image.open(fn),(x,y));draw.text((x+5,y+386),f'{t-.45+i*.1:.3f}s',fill='black')
 im.save(q/f'cut-{k+1}.jpg',quality=93)
for t,name in [(1,'首帧候选-v1.jpg'),(111.5,'收束候选-v1.jpg')]:
 run([ff,'-y','-ss',str(t),'-i',str(dest),'-frames:v','1','-q:v','2',str(out/name)],f'{t}-still.log')
shutil.copy2(p/'subtitles.srt',out/'豆包App拒绝-字幕-v1.srt')
sha=hashlib.sha256(dest.read_bytes()).hexdigest()
receipt={'content_id':'doubao-app-rejection-20261016','version':'v1','path':str(dest),'sha256':sha,'bytes':dest.stat().st_size,'durationSeconds':float(v['duration']),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'decodedFrames':int(v['nb_read_frames']),'codec':v['codec_name'],'audioCodec':a['codec_name'],'audioSampleRate':a['sample_rate'],'fullDecode':'PASS','finalVisualSampleReview':'PENDING','continuousAudiovisualReview':'UNKNOWN','directHearing':'UNKNOWN','pmoAcceptance':'PENDING','independent05':'NOT_RELEASED'}
(q/'delivery.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
