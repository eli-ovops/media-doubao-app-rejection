# coding: utf-8
from pathlib import Path
import json,hashlib,datetime,subprocess,re
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
URL='https://www.thepaper.cn/newsDetail_forward_34250739'
def main():
 assets=[]
 for p in sorted((ROOT/'素材').glob('*.jpg')):
  b=p.read_bytes();assert b[:2]==b'\xff\xd8'
  spec=subprocess.run(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(p)],capture_output=True,text=True,check=True).stdout
  w=int(re.search(r'pixelWidth: (\d+)',spec).group(1));h=int(re.search(r'pixelHeight: (\d+)',spec).group(1))
  usable='正文与名单01' not in p.name
  assets.append({'path':str(p),'filename':p.name,'bytes':len(b),'sha256':sha(p),'width':w,'height':h,'mime_type':'image/jpeg','source_url':URL,'source_type':'real browser screenshot of news report, not official original','source_publication':'2026-10-14 21:40 Asia/Shanghai','capture_date':'2026-10-16 Asia/Shanghai','image_actually_seen_by_01':True,'usable_for_video':usable,'note':'preserve source/date and crop only necessary article area' if usable else 'initial unloaded image area; retained, DO NOT USE','format_correction':'CUA returned JPEG bytes; corrected extension before delivery without changing bytes'})
 total=sum(x['bytes'] for x in assets);assert total<50*1024*1024
 (ROOT/'素材清单.json').write_text(json.dumps({'content_id':'doubao-app-rejection-20261016','owner':'01','assets':assets,'new_public_media_bytes':total,'generated_official_UI':False,'app_icons_downloaded':False,'private_media_uploaded':False},ensure_ascii=False,indent=2))
 inputs=[ROOT.parents[1]/n for n in ['01-本片来源与视觉素材任务.md','制作总单.md','用户脚本.md']]
 queries=[
 ('豆包 屏幕自动化操作声明 2026 9月14 155 10月14 腾讯66','exa','Unknown MCP server exa; stopped, configuration unchanged'),
 ('豆包 手机助手 屏幕自动化操作声明 155','search-01.json','search return only'),
 ('豆包 手机助手 屏幕自动化 9月14日','search-01.json','search return only'),
 ('豆包 手机助手 腾讯 66 10月14日','search-01.json','search return only'),
 ('豆包 手机助手 官网 拒绝 155','search-02.json','search return only'),
 ('豆包 手机助手 2025年12月 微信 阿里 暂停 操作能力 调整 说明','search-02.json','search return only'),
 ('微信软件许可及服务协议 未经腾讯授权 自动化操作','search-02.json','search return only'),
 ('豆包手机助手 官网 SAEP 不可操作清单 10月14日','search-03.json','search return only'),
 ('site.weixin.qq.com [REDACTED_HOST] 自动化操作','search-03.json','no official clause result')]
 acquisitions=[{'id':i+1,'query':q,'route_or_raw':raw,'result':result} for i,(q,raw,result) in enumerate(queries)]
 acquisitions += [
 {'id':10,'url':URL,'result':'whole article text read; selected displayed list regions actually seen; not a full official-row recount'},
 {'id':11,'url':'https://www.doubao.com/phone','result':'one obvious direct navigation; page not found; no route guessing loop'},
 {'id':12,'url':'https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_agreement&s=default','result':'explicit browser site-safety block; no authority to observe; no alternate route or workaround'}]
 record={'content_id':'doubao-app-rejection-20261016','owner_thread':'01a11442-a6d9-7413-88b3-191ce5cb037b','checked_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
 'inputs':[{'path':str(p),'sha256':sha(p),'actual_read':'full text'} for p in inputs],
 'rules_read':['PERMISSIONS-2026-10-14-v1','ROUTING-2026-10-13-v4','HANDOFF-2026-10-10-v2','ELI-FRED-PRODUCTION-20261016-v1'],
 'requested_model':'gpt-6.1-sol','requested_effort':'medium','actual_model':'UNKNOWN','actual_effort':'UNKNOWN','actual_speed':'UNKNOWN',
 'budget':{'minutes_max':20,'external_collections_max':12,'conservative_count':12,'queries':8,'failed_exa':1,'new_page_navigations':3,'actual_news_article_deep_read':1,'official_navigation_failed_or_rejected':2,'same_page_capture':'no new source acquisition','new_public_media_bytes':total},
 'acquisitions':acquisitions,
 'facts':{'reported_count':{'source':'The Paper 2026-10-14 21:40','total':155,'ecosystem_groups':[66,23,14,11,7,34],'sum':155,'independent_current_official_row_count':'UNKNOWN','conflicts':[{'source':'Beijing News 2026-10-14 16:14','total':153,'scope':'search only'},{'source':'Jiemian 2026-10-14 16:14','total':151,'scope':'search only'}],'reason_for_conflict':'UNKNOWN'},
 'DeepSeek':'actually visible in The Paper reproduced dated list; not independently retrieved official original',
 'release_date':'2026-09-14 and 30 days supported by media search returns plus The Paper full-text retrospective; official original not retrieved',
 'end_date':'2026-10-14 per The Paper full text',
 'WeChat_withdrawal':'2025-12-03 media search return relays official announcement; page/official post not opened',
 'Alibaba_whole_ecosystem_withdrawal':'UNKNOWN; app login restrictions do not establish Doubao proactively withdrew capability',
 'official_WeChat_current_clause':'UNKNOWN due site-safety; third-party [REDACTED_HOST] search lead only'},
 'pmo_decision_received':{'keep_audio_155':True,'visual':'only natural source/date on real The Paper report; not current official numerical assertion, no generic disclaimer small print','blocked_agreement':'do not fabricate official UI','scope':'stop at original budget'},
 'validation':{'asset_sha_dimensions':True,'script_or_original_media_edited':False,'official_originals_all_verified':False,'render_or_new_video_output':False},
 'cleanup':'all outputs remain necessary for production and evidence, retain; no disposable media cache or deletion'}
 (ROOT/'日期数量核验原件.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
 assert len(assets)==5 and sum(x['usable_for_video'] for x in assets)==4
 assert sum(record['facts']['reported_count']['ecosystem_groups'])==155
 assert all(Path(x['path']).is_file() and sha(Path(x['path']))==x['sha256'] for x in assets)
 files=[p for p in ROOT.iterdir() if p.is_file() and p.name!='文件记录.json']+list((ROOT/'素材').glob('*.jpg'))
 (ROOT/'文件记录.json').write_text(json.dumps({'scope':'01 owned outputs only','files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'purpose':'this-video source, media, verification or reproducibility','retain':'needed for production/evidence'} for p in files]},ensure_ascii=False,indent=2))
 print(json.dumps({'status':'READY_WITH_EXPLICIT_PRIMARY_SOURCE_GAPS','usable_screenshots':4,'nonusable_loading_evidence':1,'public_media_bytes':total,'collections':12,'group_sum':155,'official_original_list':'UNKNOWN','official_agreement':'BLOCKED_NOT_BYPASSED'},ensure_ascii=False))
if __name__=='__main__':main()
