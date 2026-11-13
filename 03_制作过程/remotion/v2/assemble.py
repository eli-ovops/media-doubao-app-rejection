from pathlib import Path
import json,hashlib,subprocess,os,shutil
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;old=p.parent/'v1';n=p.parents[2];q=p/'qc';out=n/('02_'+chr(26368)+chr(32456)+chr(36755)+chr(20986));ff='/Users/USER/.local/bin/ffmpeg';base=next(out.glob('*-v1.mp4'));dest=base.with_name(base.name.replace('-v1','-v2'))
assert hashlib.sha256(base.read_bytes()).hexdigest()=='c561006155a3c348291c38eb4dbaa11e95e753274bae0746553eac2c71b37829'
env=os.environ.copy();comp=(p/'node_modules/@remotion/compositor-darwin-arm64').resolve();env['DYLD_LIBRARY_PATH']=str(comp)
def run(cmd,name):
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);(q/name).write_bytes(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(name+': '+str(r.returncode))
 return r
fil="[0:v]settb=expr=1/60,setpts=N[b];[1:v]scale=in_range=pc:out_range=tv,format=yuv420p,setrange=limited,settb=expr=1/60,setpts=N+384[n];[2:v]scale=in_range=pc:out_range=tv,format=yuv420p,setrange=limited,settb=expr=1/60,setpts=N+6726[e];[b][n]overlay=0:0:enable='gte(t,6.39999)*lt(t,10.84999)'[v];[v][e]overlay=0:0:enable='gte(t,112.09999)'[out]"
run([ff,'-y','-i',str(base),'-i',str(p/'render/news.mp4'),'-i',str(p/'render/ending.mp4'),'-filter_complex',fil,'-map','[out]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v','6780','-movflags','+faststart',str(dest)],'assemble.log')
r=run([str(comp/'ffprobe'),'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dest)],'probe.json');probe=json.loads(r.stdout);v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],int(v['nb_read_frames']),v['r_frame_rate'])==(1080,1920,6780,'60/1')
assert abs(float(v['duration'])-113)<.001 and float(a['start_time'])==0
run([ff,'-v','error','-i',str(dest),'-f','null','-'],'decode.log')
hashes=[]
for name,f in [('v1',base),('v2',dest)]:
 r=run([ff,'-v','error','-i',str(f),'-map','0:a:0','-c:a','pcm_s16le','-f','hash','-hash','sha256','-'],f'audio-{name}-hash.txt');hashes.append(r.stdout.decode().strip())
assert hashes[0]==hashes[1],hashes
for key,start,dur,fps in [('news',6.2,4.9,10),('ending',111.8,1.2,20)]:
 dr=q/key;dr.mkdir(exist_ok=True)
 run([ff,'-y','-ss',str(start),'-i',str(dest),'-t',str(dur),'-vf',f'fps={fps},scale=216:384','-q:v','3',str(dr/'f-%03d.jpg')],f'{key}-sample.log')
 imgs=sorted(dr.glob('*.jpg'))
 for offset in range(0,len(imgs),15):
  sheet=Image.new('RGB',(1080,1230),'#e6e6e6');draw=ImageDraw.Draw(sheet)
  for i,fn in enumerate(imgs[offset:offset+15]):
   x=i%5*216;y=i//5*410;sheet.paste(Image.open(fn),(x,y));draw.text((x+5,y+386),f'{start+(offset+i+.5)/fps:.3f}s',fill='black')
  sheet.save(q/f'{key}-motion-{offset//15+1}.jpg',quality=94)
for t in [6.6,7,8.5,10.75,112,112.15,112.3,112.4,112.8,112.98]:
 run([ff,'-y','-ss',str(t),'-i',str(dest),'-frames:v','1','-q:v','2',str(q/f'native-{t}.jpg')],f'native-{t}.log')
shutil.copy2(old/'subtitles.srt',out/base.name.replace('-v1.mp4','-v2.srt').replace(chr(23436)+chr(25972)+chr(29255),chr(23383)+chr(24149)))
for fn in out.glob('*-v1.jpg'):shutil.copy2(fn,fn.with_name(fn.name.replace('-v1','-v2')))
# Ending candidate must show the revised ending, not the former human frame.
end=out/(chr(25910)+chr(26463)+chr(20505)+chr(36873)+'-v2.jpg');shutil.copy2(q/'native-112.8.jpg',end)
receipt={'content_id':'doubao-app-rejection-20261016','version':'v2','path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size,'width':1080,'height':1920,'fps':60,'frames':6780,'duration':113,'changedFrameRangesInclusive':[[384,650],[6726,6779]],'sourceRenderedFrames':321,'audioDecodedPcmIdentity':hashes[0],'audioUnchangedFromV1':True,'audioStart':a['start_time'],'audioDuration':a['duration'],'fullDecode':'PASS','visualSampleReview':'PENDING','continuousAudiovisualReview':'UNKNOWN','directHearing':'UNKNOWN','pmoAcceptance':'PENDING'}
(q/'delivery.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2));print(json.dumps(receipt,ensure_ascii=False,indent=2))
