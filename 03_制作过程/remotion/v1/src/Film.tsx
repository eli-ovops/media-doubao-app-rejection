// Episode assembly from Fred episode-skeleton; portrait mixed-media continuity with exact source clock.
import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,Sequence,staticFile,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
import timing from './timing.json';
import {S,p,q,mix,springAt} from './kit/theme';
import {SmileySubtitle} from './components/SmileySubtitle';
import {Txt,Plate,Tag,RequestAction,ArticleFocus,CalendarAction,StatGroups,EntryAction,DataAction,PermissionAction} from './components/Actions';
const fontSpecs=[['Fred MiSans','MiSans-Medium.otf','500'],['Fred MiSans','MiSans-Heavy.otf','900'],['FredSmileySans','SmileySans-Oblique.ttf','400']];
let promise:Promise<void>;
const Fonts=()=>{const [h]=useState(()=>delayRender('Exact Fred kit fonts'));useEffect(()=>{promise??=Promise.all(fontSpecs.map(async([name,file,weight])=>{const face=new FontFace(name,`url(${staticFile('fonts/'+file)})`,{weight});await face.load();document.fonts.add(face);})).then(()=>{});promise.then(()=>continueRender(h)).catch(cancelRender)},[h]);return null;};
const Person=({order=6,start=.25}:{order?:number,start?:number})=><OffthreadVideo src={staticFile(`media/raw-${String(order).padStart(2,'0')}.mp4`)} startFrom={Math.round(start*60)} muted style={{width:1080,height:1920,objectFit:'cover'}}/>;
export function Opening(){const t=useCurrentFrame()/60;return <>
{t<2.15?<><Person/><Tag text="豆包想帮你点外卖" x={90} y={145} w={900} h={140} size={65}/></>:t<6.4?<RequestAction t={t-2.15}/>:<><Txt y={180} size={85}>拒绝，已经成了名单</Txt><ArticleFocus t={t-6.4} crop={[198,205,645,165]} top={580}/><Txt y={1030} size={54} color={S.muted}>报道原文</Txt><ArticleFocus t={t-6.4} crop={[198,407,650,43]} top={1160} label="同篇报道 · 非当前实时统计"/></>}
</>}
export function Statement(){const t=useCurrentFrame()/60;return t<5.5?<><Txt y={180} size={60} color={S.muted}>2026 年 9 月 14 日</Txt><Plate x={90} y={430} w={900} h={900} style={{transform:`translateY(${(1-p(t,0,.55))*90}px)`}}><Txt x={60} y={95} w={780} size={82}>屏幕自动化<br/>操作声明协议</Txt><div style={{position:'absolute',left:60,top:395,width:780,height:6,background:S.ink}}/><Txt x={60} y={490} w={780} size={56} heavy={false}>AI 发出操作请求<br/><br/>App 表达是否同意</Txt></Plate><Txt y={1410} size={34} color={S.muted} align="center">声明要解决的事</Txt></>:t<13.1?<RequestAction t={t-5.5} general/>:<CalendarAction t={t-13.1}/>;}
export function Groups(){return <StatGroups t={useCurrentFrame()/60}/>;}
export function History(){const t=useCurrentFrame()/60;return t<3?<><Person order={2} start={.15}/><Tag text="去年 12 月，已经发生过" x={90} y={145} w={900} h={140} size={60}/></>:<RequestAction t={t-3} history/>;}
export function Analysis(){const t=useCurrentFrame()/60;return t<8.62?<><Person order={1} start={.1}/>{t<5.26?<Tag text="为什么都拒绝？" x={170} y={145} w={740} h={140} size={70}/>:<><Tag text="我的看法" x={370} y={120} w={340} h={90} size={42}/>{['入口','数据','安全'].map((s,i)=><Tag key={s} text={s} x={80+i*320} y={280} w={280} h={130} size={67} style={{opacity:p(t,5.4+i*.4,5.9+i*.4),transform:`translateY(${(1-p(t,5.4+i*.4,5.9+i*.4))*50}px)`}}/>)}</>}</>:t<12.7?<><Txt y={200} size={80}>三个因素</Txt>{['入口','数据','安全'].map((s,i)=><Tag key={s} text={s} x={160} y={480+i*300} w={760} h={210} size={110} style={{transform:`scale(${mix(.94,1,springAt(t,8.62+i*1.36,.65))})`,background:t>=8.62+i*1.36?S.ink:'#b5b5bf'}}/>)}</>:t<23.22?<EntryAction t={t-12.7}/>:<DataAction t={t-23.22}/>;}
export function Responsibility(){return <PermissionAction t={useCurrentFrame()/60} responsibility/>;}
export function Ending(){const t=useCurrentFrame()/60;return t<3?<><Person order={5} start={.1}/><Tag text="对普通人，当然方便" x={90} y={150} w={900} h={140} size={65}/></>:t<11.22?<PermissionAction t={t-3}/>:<><Person order={5} start={.1}/><Tag text={t<13.22?'AI 行不行？':'平台，让不让？'} x={120} y={130} w={840} h={160} size={80}/></>;}
const scenes=[['S01',0,651,Opening],['S02',651,1122,Statement],['S03',1773,1563,Groups],['S04',3336,477,History],['S05',3813,1744,Analysis],['S06',5557,275,Responsibility],['S07',5832,948,Ending]] as const;
export const Film=()=>{const f=useCurrentFrame();const localPerson=[f<129,f>=3336&&f<3516,f>=3813&&f<4330,f>=5832&&f<6012,f>=6505].some(Boolean);return <AbsoluteFill style={{background:'#fafafa',fontFamily:S.body,color:S.ink,fontSynthesis:'none'}}><Fonts/>{scenes.map(([id,start,len,C])=><Sequence key={id} from={start} durationInFrames={len}><C/></Sequence>)}<SmileySubtitle/>
<Audio src={staticFile('media/voice.wav')}/>
{[{t:2.15,n:'woosh',v:.10},{t:3.65,n:'pop',v:.08},{t:6.4,n:'slide',v:.08},{t:23.95,n:'woosh',v:.08},{t:31,n:'pop',v:.06},{t:39,n:'pop',v:.06},{t:51.3,n:'click',v:.05},{t:76.25,n:'slide',v:.08},{t:100.2,n:'woosh',v:.07}].map((s,i)=><Sequence key={i} from={Math.round(s.t*60)} durationInFrames={75}><Audio src={staticFile('sfx/'+s.n+'.wav')} volume={s.v}/></Sequence>)}
</AbsoluteFill>};
