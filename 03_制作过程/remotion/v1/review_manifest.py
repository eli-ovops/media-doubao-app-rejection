# Records the actual model visual review performed in this chat, not automatic visual judging.
from pathlib import Path
import json,sys,hashlib
P=Path(__file__).resolve().parent;R=P/'skills/FredTalk';sys.path.insert(0,str(R/'skills/fred-remotion-output/scripts'))
from scene import applicable
from common import load_references
from component_selection import shortlist
from component_distribution import analyze
from library_gate import acceptance_signature
hash=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
def ev(p):return {'path':str(p),'sha256':hash(p)}
m=json.loads((P/'manifest.json').read_text());_,cat=load_references(R);m['workflow']['authorization']={'mode':'direct-output','source':str(P.parents[2]/'04-完整制作任务.md'),'quote':'确认，开始吧。先固化Skills，再把这6段豆包视频剪成完整片。你负责持续跟进、修改和验收，中间常规问题自己处理，明早我直接看成片。'};m['timingStatus']='audio-aligned';m['timingEvidence']={**ev(P/'qc/final-edl.json'),'scope':'Conformed actual speech timeline with ASR candidate cues; no direct listening claim'};m['outputSpec']={'width':1080,'height':1920,'fps':60}
reject={'T04d':'主题长出分支再收拢不呈现日期窗口长度。','N026':'手机与案例画面连续交接缺少日期含义。','T15f':'环形占比会错误暗示四组构成全部应用；本期只列数量。','L81-C005':'声音到记忆发散而非输入入口汇聚，当前反向对象关系不同。','T02h':'文件翻面解释职责需要文件原文，本片是平台许可锁依赖。','T09n':'等待快进会把30天误演成软件安装等待，不承担公示日历。','T09d2':'任务输入后逐项完成属于执行状态，不适合公示区间。','T16a':'时间线能列日期，但本镜选择日历逐格走过30天以表现窗口长度。','T14c':'旧价划掉与新价对比会误导生态分组数字是价格或版本变化。','L81-R005':'总量拆分三类不能表达四组且不得把四组合计当155。','T09b':'实际授权弹窗和已开通状态会暗示已获许可，本片不能这样表现。','T09a':'光标找真实UI入口需要已核实录，本片分析只说明入口关系。','X032':'设备和标题展示不能表达钥匙前置条件与多个锁的依赖。','T02e':'多产品用途卡的移位不表达平台许可。','N047':'手机解锁进入聊天会暗示操作已成功，与许可未给的结论冲突。'}
sourceA=Path('/Volumes/EXTERNAL/自媒体/资产库/FredTalk/组件视频')
for page in m['pages']:
 sid=page['stableId'];kind='metric-change' if sid=='S03' else 'relationship';_,_,rules,sig=applicable(R,kind);page['sceneGuide'].update(type=kind,signature=sig,modifiers=[])
 page['exactScreenWords']=[{'S01':'App 能不能操作？','S02':'屏幕自动化操作声明协议','S03':'腾讯 阿里巴巴 快手 美团 DeepSeek','S04':'操作微信，账号退出','S05':'入口 数据 安全','S06':'出了事，谁负责？','S07':'平台，让不让？'}[sid]]
 selected={r['id'] for r in page['referenceChoices']};cand=shortlist(R,cat,page,5)['candidates'];(P/f'qc/{sid}-candidates.json').write_text(json.dumps(shortlist(R,cat,page,5),ensure_ascii=False,indent=2));print(sid,'top3',[(x['label'],x['id']) for x in cand[:3]])
 entries={x['id']:x for k in ['components','clips'] for x in cat[k]}
 picked=[]
 for r in [*cand[:3],*[{'id':x,'label':entries[x]['displayLabel']} for x in selected if x not in {c['id'] for c in cand[:3]}]]:
  cid=r['id'];picked.append({'id':cid,'decision':'selected' if cid in selected else 'rejected','reason':page['oneQuestion'] if cid in selected else reject.get(r['label'],'候选对象关系不如已选的请求、日历或许可依赖直接；保留当前可验证源码适配。')})
 page['componentPlan'].update(candidates=picked,inspectedReferences=[])
 for ref in page['referenceChoices']:
  label=entries[ref['id']]['displayLabel'];f=next(sourceA.glob(label+'-1-preview.mp4'));page['componentPlan']['inspectedReferences'].append({'id':ref['id'],**ev(f),'observations':ref['preserve']+'；已看对应时间序列图，未连续看听。'})
  if sid=='S05' and label=='T13d':ref['implementation']['symbol']='DataAction';ref['callSite']['callee']='DataAction'
  for field in ['source','implementation','callSite']:ref[field]['sha256']=hash(ref[field]['path'])
 page['keyframeReview']={'frames':[ev(x) for x in sorted((P/'qc').glob('still-*.png')) if page['startFrame']/60<=float(x.stem[6:])<(page['startFrame']+page['durationInFrames'])/60], 'sourceFiles':[ev(P/'src/Film.tsx'),ev(P/'src/components/Actions.tsx')]}
# Reviewed same-carrier reuse: report crops are a shell; request identity reprises; locks deliberately never unlock.
a=analyze(m,cat);dec=[]
for g in a['groups']:
 dec.append({'groupKey':g['groupKey'],'sceneIds':g['sceneIds'],'reuseKind':'intentional-reprise','reason':'请求方与平台的相同身份用于开头提出矛盾、声明解释与历史回看；媒体截取为同一报道载体；结尾许可锁呼应责任而不演成成功授权。','comparisons':[{'stableId':sid,'task':next(p['oneQuestion'] for p in m['pages'] if p['stableId']==sid),'visibleState':{'S01':'豆包请求美团，红色不行返回，随后真实报道','S02':'App拒绝关系转为30天公示格','S03':'四组数字和真实正文行，DeepSeek原像素行','S04':'微信关系返回账号退出','S05':'淘宝入口绕至豆包，再读屏流向AI','S06':'责任钥匙未进入锁，付钱/聊天锁定','S07':'许可钥匙停在锁前，真人结尾'}[sid],'reusePurpose':'延续同一语义对象的动作词汇，当前场景有独立信息职责'} for sid in g['sceneIds']], 'evidence':[ev(P/'qc/overview-0.jpg'),ev(P/'qc/overview-1.jpg'),ev(P/'qc/overview-2.jpg')]})
m['componentDistributionReview']={'status':'passed','reviewedBy':'assistant','contextSha256':a['contextSha256'],'decisions':dec}
stage=sys.argv[1] if len(sys.argv)>1 else 'suggestion'
for page in m['pages']:
 page['componentAcceptance']={'status':'passed','stage':stage,'reviewer':'assistant','checks':{'semanticFit':page['oneQuestion'],'corePreserved':'已对照源组件采样图及上述实际源码；保留路径往返、数字落定、来源像素、输入汇聚或钥匙依赖，具体边界在referenceChoices。','visualQuality':'实际关键帧：白底墨黑载体，MiSans正文/Heavy与独立得意黑字幕；主对象避开底部230px字幕带。已修报道裁切与残留关系线，原尺寸查看53.4/85/108s。'},'evidence':page['keyframeReview']['frames'] if stage=='keyframes' else [ev(P/'qc/candidates-overview-0.jpg'),ev(P/'qc/candidates-overview-1.jpg'),ev(P/'qc/candidates-overview-2.jpg')]}
 page['componentAcceptance']['contextSha256']=acceptance_signature(m,page,stage)
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
