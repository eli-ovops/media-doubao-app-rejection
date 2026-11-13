# coding: utf-8
from pathlib import Path
import json,re,hashlib,math
R=Path(__file__).resolve().parent
e=json.loads((R/'read-evidence.json').read_text())
edit=json.loads((R/'subtitle-edits.json').read_text())
raw_order=[6,4,3,2,1,5]
# Ends preserve original ASR sentence tails; only clearly external head/tail margins removed.
ranges={6:(0.25,11.10),4:(0.0,18.70),3:(0.15,26.20),2:(0.15,17.65),1:(0.10,41.02),5:(0.10,15.90)}
def stamp(t):
    ms=round(max(t,0)*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
def smpte(t):
    f=round(t*60);s,f=divmod(f,60);m,s=divmod(s,60);h,m=divmod(m,60)
    return f'{h:02d}:{m:02d}:{s:02d}:{f:02d}'
def chunks(text):
    # Whitespace indicates semantic break; finer divisions remain approximate and logged.
    blocks=text.split();out=[]
    for b in blocks:
        if len(b)<=16:out.append(b);continue
        if b.startswith('大家有没有想过'):
            out.extend(['大家有没有想过','为什么这些头部的大厂','都拒绝了豆包']);continue
        if b.startswith('最后豆包把自己'):
            out.extend(['最后豆包把自己和微信','和阿里的操作能力','就撤掉了']);continue
        if b.startswith('就连DeepSeek'):
            out.extend(['就连DeepSeek','也拒绝了豆包的这个使用']);continue
        while len(b)>16:
            out.append(b[:14]);b=b[14:]
        if b:out.append(b)
    return out
timeline=[];cues=[];corrected=[];cursor=0;sourcecues={};review=[]
for semantic,raw in enumerate(raw_order,1):
    row=next(x for x in e['sources'] if x['provided_order']==raw)
    d=R/f'raw-{raw:02d}';asr=json.loads((d/'asr.json').read_text());texts=edit[f'raw-{raw:02d}'];assert len(texts)==len(asr['transcription'])
    start,end=ranges[raw];duration=end-start;sourcecues[raw]=[]
    for i,(s,txt) in enumerate(zip(asr['transcription'],texts)):
        a=s['offsets']['from']/1000;b=s['offsets']['to']/1000
        assert 0<=a<b<=row['duration']+0.1
        parts=chunks(txt);total=sum(len(x) for x in parts);offset=0
        for part in parts:
            x=a+(b-a)*offset/total;offset+=len(part);y=a+(b-a)*offset/total
            sourcecues[raw].append({'start':round(x,3),'end':round(y,3),'text':part,'raw_segment_index':i,'timing':'ASR sentence boundary; semantic split proportionally estimated, not word-verified'})
            lo=max(x,start);hi=min(y,end)
            if hi>lo:
                cues.append({'start':round(cursor+lo-start,3),'end':round(cursor+hi-start,3),'text':part,'semantic_segment':f'{semantic:02d}','raw_order':raw,'source_start':round(lo,3),'source_end':round(hi,3),'timing':'ASR-derived; review required'})
    for i,(s,txt) in enumerate(zip(asr['transcription'],texts)):
        review.append({'semantic_segment':f'{semantic:02d}','raw_order':raw,'source_range':[s['offsets']['from']/1000,s['offsets']['to']/1000],'original_asr':s['text'],'editorial_candidate':txt,'heard_verified':False})
    corrected.append(f'## {semantic:02d} | 上传{raw} | {start:.3f}—{end:.3f}s\n\n'+'\n\n'.join(texts))
    timeline.append({'semantic_segment':f'{semantic:02d}','provided_order':raw,'source':row['source'],'source_sha256':row['sha256'],'source_in':start,'source_out':end,'source_in_60fps':round(start*60),'source_out_60fps':round(end*60),'duration':round(duration,6),'timeline_in':round(cursor,6),'timeline_out':round(cursor+duration,6),'selected_take':'Only full semantic take observed; no alternate complete retake in six-file ASR','speed':1.0,'audio_gain_db':0,'internal_audio_cuts':[],'precision_note':'seconds define edit; 60fps frame numbers are output conform approximations for near60fps/VFR input; do not reinterpret native frame index'})
    cursor+=duration
    (d/'subtitles-candidate.source.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(sourcecues[raw]))+'\n')
edl={'content_id':'doubao-app-rejection-20261016','version':'intake-v1','status':'READY_FOR_PRODUCTION_WITH_SPECIFIC_AUDIO_TEXT_REVIEW_FLAGS','fps':60,'resolution':[1080,1920],'timeline_duration':round(cursor,6),'source_duration_total':sum(x['duration'] for x in e['sources']),'audio_clock':'Source time in seconds; speed1; no processing applied','cut_policy':'Only external head/tail trims. No within-sentence cut based on ASR. Preserve current full semantic takes.','clips':timeline,'subtitle_file':str(R/'subtitles-candidate.timeline.srt'),'subtitle_status':'DRAFT_MUST_RESOLVE_MARKED_PHRASES_AND_FINAL_AUDIO_SYNC','optional_cuts_disabled':[{'provided_order':2,'source_range':[7.84,12.0],'reason':'Only if actual word is facial captcha and01 evidence supports only generic captcha; remove whole sentence, not invent corrected voice; requiresPMO/04 decision','enabled':False},{'provided_order':1,'source_range':[17.95,18.65],'reason':'Low-energy inter-phrase gap candidate only; no heard verification','enabled':False},{'provided_order':4,'source_range':[12.80,13.40],'reason':'Inter-phrase gap candidate only; no heard verification','enabled':False}]}
(R/'edl.json').write_text(json.dumps(edl,ensure_ascii=False,indent=2)+'\n')
(R/'subtitle-cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n')
(R/'subtitle-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(R/'subtitles-candidate.timeline.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n')
(R/'纠错逐字稿-候选.md').write_text('# 本期实际ASR整理与字幕候选\n\n以实际转录的自然措辞为基础，未强行换回用户书面脚本。豆包/美团/DeepSeek/公示等校字属文本推定，不是直接听核；待核差异.json里的几处必须保留可追溯原文，未被确认成人声已说对。所有字幕目前为制作候选。录制指导不进入字幕。\n\n'+'\n\n'.join(corrected)+'\n')
lines=['TITLE: DOUBAO INTAKE V1','FCM: NON-DROP FRAME','* OUTPUT CONFORM 60FPS; SOURCE SECONDS IN EDL.JSON ARE AUTHORITATIVE','']
for i,c in enumerate(timeline,1):
    lines.extend([f'{i:03d}  RAW{c["provided_order"]:02d}  V  C  {smpte(c["source_in"])} {smpte(c["source_out"])} {smpte(c["timeline_in"])} {smpte(c["timeline_out"])}',f'* FROM CLIP NAME: {c["source"]}',f'* AUDIO USE SAME SOURCE CLOCK; SPEED 1.0; SEMANTIC {c["semantic_segment"]}',''])
(R/'roughcut-60fps-conform.edl').write_text('\n'.join(lines))
assert all(0<=x['source_in']<x['source_out']<=next(s['duration'] for s in e['sources'] if s['provided_order']==x['provided_order']) for x in timeline)
assert all(0<=c['start']<c['end']<=cursor+0.001 for c in cues)
assert all(cues[i]['end']<=cues[i+1]['start']+0.001 for i in range(len(cues)-1))
validation={'source_mapping':raw_order,'net_duration':round(cursor,6),'total_raw_duration':edl['source_duration_total'],'cue_count':len(cues),'max_cue_characters':max(len(c['text']) for c in cues),'ranges_valid':True,'subtitles_nonoverlapping':True,'source_hash_recheck':[],'actual_viewed_contact_sheets':[p for s in e['sources'] for p in s['contact_sheets']],'actual_viewed_sample_count':sum(len(s['sample_times']) for s in e['sources']),'native_stills_viewed':['inspection/raw-06-1.0-native.jpg','inspection/raw-01-20.0-native.jpg','inspection/raw-04-18.6-native.jpg'],'direct_audio':False,'continuous_viewing':False}
for s in e['sources']:
    actual=hashlib.sha256(Path(s['source']).read_bytes()).hexdigest();assert actual==s['sha256'];validation['source_hash_recheck'].append({'path':s['source'],'sha256':actual,'unchanged':True})
(R/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(validation,ensure_ascii=False))
