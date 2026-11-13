from pathlib import Path
import json,shutil,hashlib,re,subprocess
P=Path(__file__).resolve().parent; N=P.parents[2]; W=Path('/Volumes/EXTERNAL/自媒体/Fred付费资料全站学习-20261016/解包只读副本/fred-wave3-40-20261012'); F=Path('/Users/USER/.codex/skill-repos/FredTalk')
for d in ['src/kit','src/components','public/fonts','public/sfx','public/media','render','qc','skills/sources']:(P/d).mkdir(parents=True,exist_ok=True)
for name in ['MiSans-Medium.otf','MiSans-Heavy.otf','MiSans-License.txt']:shutil.copy2(W/'public/fonts'/name,P/'public/fonts'/name)
for name in ['SmileySans-Oblique.ttf','SmileySans-LICENSE.txt']:shutil.copy2(F/'library/fonts'/name,P/'public/fonts'/name)
for name in ['pop.wav','woosh.wav','click.wav','slide.wav']:shutil.copy2(W/'public/sfx'/name,P/'public/sfx'/name)
shutil.copy2(W/'src/kit/theme.ts',P/'src/kit/theme.ts')
for name in ['T13d-RequestTrip.tsx','T14e-StatTriplet.tsx','T09i-PickRow.tsx','T04f-KeyUnlock.tsx']:shutil.copy2(W/'src/components'/name,P/'skills/sources'/name)
for name in ['theme.ts','ui.tsx']:shutil.copy2(W/'src/kit'/name,P/'skills/sources'/name)
mods=Path('/Volumes/EXTERNAL/自媒体/Fred复刻测试-20261016/7694088597179239690/source-snapshot/FredTalk-1.5-3D/camera/node_modules')
if not (P/'node_modules').exists():(P/'node_modules').symlink_to(mods,target_is_directory=True)
edl=json.loads((N/'flow/02/edl.json').read_text()); print('EDL keys',edl.keys())
segments=edl.get('segments',edl.get('clips')); cursor=0; cuts=[]; cues=[]
for s in segments:
 num=s['provided_order']; a=s['source_in']; b=s['source_out']; ranges=[(a,b)]
 if num==2:ranges=[(a,8.10)]
 if num==1:ranges=[(a,29.16),(36.44,b)]
 for j,(a,b) in enumerate(ranges):
  frames=round((b-a)*60); dur=frames/60
  cuts.append(dict(id=f'{num}-{j}',order=num,source=s['source'],sourceIn=a,sourceOut=a+dur,startFrame=cursor,durationInFrames=frames,sourceSha256=s['source_sha256']))
  txt=(N/f'flow/02/raw-{num:02d}/subtitles-candidate.source.srt').read_text()
  for block in txt.strip().split('\n\n'):
   lines=block.splitlines(); ts=lines[1].split(' --> ')
   def sec(v):h,m,z=v.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(z)
   cs,ce=map(sec,ts); text=' '.join(lines[2:])
   if min(ce,a+dur)>max(cs,a):cues.append(dict(start=round(cursor/60+max(cs,a)-a,4),end=round(cursor/60+min(ce,a+dur)-a,4),text=text,sourceOrder=num,sourceStart=max(cs,a)))
  cursor+=frames
# Merge orphan subtitles without retiming the voice.
merged=[]
for c in cues:
 if c['text'] in ['一次了','说No'] and merged and merged[-1]['sourceOrder']==c['sourceOrder']:
  merged[-1]['text']+=c['text'];merged[-1]['end']=c['end']
 else:merged.append(c)
# Split long lines by natural clauses, only text timing interpolation (not new heard alignment).
subs=[]
for c in merged:
 if c['end']-c['start']<.02:continue # Drop sub-frame remnants introduced by a speech cut.
 text=c['text']; parts=[text]
 if len(text)>16:
  split={'总共有155个App都对豆包说No':['总共有155个App','都对豆包说No'],'如果说现在只需要对豆包说一句':['如果说现在只需要','对豆包说一句'],'其实去年12月就已经闹过这么一次了':['其实去年12月','就已经闹过这么一次了']}
  parts=split.get(text,[text[:max(8,len(text)//2)],text[max(8,len(text)//2):]])
  if text not in split:parts=[text] # retain sentence, two lines at render
 at=c['start']; total=sum(map(len,parts))
 for part in parts:
  end=at+(c['end']-c['start'])*len(part)/total
  subs.append(dict(startSeconds=round(at,4),endSeconds=round(end,4),text=part));at=end
D={'fps':60,'width':1080,'height':1920,'totalFrames':cursor,'duration':cursor/60,'clips':cuts,'subtitles':subs,'subtitlesEvidence':'02 local ASR + contextual corrections; not direct listening; interpolation retained where word alignment absent'}
(P/'src/timing.json').write_text(json.dumps(D,ensure_ascii=False,indent=2));(P/'qc/final-edl.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
def tc(v):ms=round(v*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{tc(c["startSeconds"])} --> {tc(c["endSeconds"])}\n{c["text"]}' for i,c in enumerate(subs))+'\n')
assets=json.loads((N/'flow/01/素材清单.json').read_text())['assets']; records=[]
for i,a in enumerate(assets):
 if a['usable_for_video']:
  dest=P/f'public/media/news-{i}.jpg';shutil.copy2(a['path'],dest);records.append({**a,'local':str(dest)})
for s in segments:
 target=P/f'public/media/raw-{s["provided_order"]:02}.mp4'
 if not target.exists():shutil.copy2(s['source'],target)
(P/'qc/media-provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('timeline',cursor,cursor/60,[(c['order'],c['startFrame']/60,c['durationInFrames']/60) for c in cuts])
print('runtime',json.loads((mods/'remotion/package.json').read_text())['version'])
