// Action sources: T13d RequestTrip, T14e StatTriplet, T09i PickRow, T04f KeyUnlock, L81-R001 CalendarV3, L81-R006 EncoderV3. Scene-specific portrait adaptation, exact kit easing and surfaces.
import React from 'react';
import {Img,staticFile} from 'remotion';
import {S,p,q,mix,springAt,clamp} from '../kit/theme';
export const ink=S.ink, purple=S.accent;
export const Txt=({children,x=80,y=150,w=920,size=66,heavy=true,color=ink,align='left',style={}}:any)=><div style={{position:'absolute',left:x,top:y,width:w,fontSize:size,fontFamily:S.body,fontWeight:heavy?900:500,lineHeight:1.16,color,textAlign:align,fontSynthesis:'none',...style}}>{children}</div>;
export const Plate=({x,y,w,h,dark=false,children,style={}}:any)=><div style={{position:'absolute',left:x,top:y,width:w,height:h,borderRadius:S.radius,background:dark?S.dark:'#fff',boxShadow:dark?S.capsuleShadow:S.shadow,...style}}>{children}</div>;
export const Tag=({text,x,y,w=300,h=94,dark=true,size=44,style={}}:any)=><Plate x={x} y={y} w={w} h={h} dark={dark} style={{borderRadius:h/2,display:'grid',placeItems:'center',color:dark?'#fff':ink,fontFamily:S.body,fontWeight:900,fontSize:size,...style}}>{text}</Plate>;
export const Line=({d,progress=1,color=ink,width=6,dashed=false}:any)=><path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={dashed?'0.014 0.02':'1 1'} strokeDashoffset={1-progress}/>;
export const Svg=({children}:any)=><svg width={1080} height={1920} style={{position:'absolute',inset:0,overflow:'visible'}}>{children}</svg>;
export const Lock=({x,y,size=100,open=0,color=ink}:any)=><svg width={size} height={size} viewBox="0 0 48 48" style={{position:'absolute',left:x,top:y}}><g style={{transform:`translate(${open*3}px,${-open*7}px) rotate(${-open*38}deg)`,transformOrigin:'34px 22px'}}><path d="M14 22 V15 a10 10 0 0 1 20 0 V22" fill="none" stroke={color} strokeWidth={5} strokeLinecap="round"/></g><rect x={7} y={21} width={34} height={23} rx={6} fill={color}/></svg>;
export const Phone=({x=280,y=420,w=520,h=920,children,style={}}:any)=><div style={{position:'absolute',left:x,top:y,width:w,height:h,background:'#fff',borderRadius:62,boxShadow:S.capsuleShadow,border:'14px solid #19191c',overflow:'hidden',boxSizing:'border-box',...style}}><div style={{position:'absolute',top:18,left:'38%',width:'24%',height:22,borderRadius:20,background:ink,zIndex:4}}/>{children}</div>;
// T13d: request leaves origin along a lane, target receives it, response travels back; rejection replaces successful result.
export function RequestAction({t,history=false,general=false}:any){const go=q(t,.2,1.1),back=q(t,1.5,2.2);const y=mix(570,1030,go);const replyY=mix(1020,680,back);return <>
<Txt y={200} size={76} align="center">{history?'操作微信，账号退出':general?'App 可以提前说：不同意':'App 能不能操作？'}</Txt>
<Tag text="豆包" x={340} y={430} w={400} h={130} size={68}/>
<Plate x={260} y={1050} w={560} h={230} dark><Txt x={0} y={47} w={560} size={80} align="center" color="#fff">{history?'微信':general?'App':'美团'}</Txt><Txt x={0} y={151} w={560} size={36} align="center" color={S.accentDark}>App</Txt></Plate>
<Svg><Line d="M480 575 V1040" progress={p(t,0,.5)} color="#dcdce0"/><Line d="M600 1040 V590" progress={p(t,0,.5)} color="#dcdce0"/><Line d="M480 575 V1040" progress={go}/><Line d="M600 1040 V590" progress={back}/></Svg>
{go<1&&<Tag text={history?'操作':'点外卖'} x={330} y={y} w={300} h={90} size={44}/>}
{t>=1.5&&<Tag text={history?'账号退出':'不行'} x={450} y={replyY} w={300} h={112} size={56} style={{background:'#ac3639'}}/>}
{t>2.4&&<Txt y={1400} size={46} align="center" color={S.muted}>{history?'2025 年 12 月':'请求发得出，平台可以拒绝'}</Txt>}
</>;}
// T09i: actual image pixels remain the carrier; target row lifts at its original crop geometry.
export function ArticleFocus({t,image='news-1.jpg',crop=[195,200,640,175],label='澎湃 · 2026-10-14 21:40',top=680,width=900,lift=true}:any){const [cx,cy,cw,ch]=crop;const z=width/cw;const rise=p(t,0,.55),k=lift?mix(.97,1,p(t,.1,.7)):1;return <><div style={{position:'absolute',left:(1080-width)/2,top:top+(1-rise)*50,width,height:ch*z,overflow:'hidden',background:'#fff',boxShadow:S.shadow,opacity:rise,transform:`scale(${k})`,borderRadius:12}}><Img src={staticFile('media/'+image)} style={{position:'absolute',left:-cx*z,top:-cy*z,width:1265*z,height:712*z,maxWidth:'none'}}/></div><Txt x={90} y={top+ch*z+35} w={900} size={30} color={S.muted}>{label}</Txt></>;}
// L81-R001: a title scales through its letterforms into the calendar carrier; current 2026 dates replace fixed July grid.
export function CalendarAction({t}:any){const a=p(t,0,.6),days=Math.min(30,Math.floor(30*q(t,.5,1.5)));const focus=p(t,2.2,2.75);return <>
<Txt y={190} size={76} align="center">公示 30 天</Txt>
<Plate x={90} y={420} w={900} h={920} dark style={{transform:`scale(${mix(.88,1,a)})`,opacity:a}}>
<Txt x={60} y={60} w={780} size={63} color="#fff">9 / 14 → 10 / 14</Txt>
<Txt x={60} y={150} w={780} size={34} color="#b8b8c0">2026 · 应用表达意愿的窗口</Txt>
<div style={{position:'absolute',left:60,right:60,top:280,display:'grid',gridTemplateColumns:'repeat(6,1fr)',gap:20}}>{Array.from({length:30},(_,i)=><div key={i} style={{height:90,borderRadius:16,background:i<days?S.accentDark:'#303036',color:i<days?ink:'#74747a',display:'grid',placeItems:'center',fontSize:42,fontWeight:900,transform:`scale(${i===days-1?1.04:1})`}}>{i+1}</div>)}</div>
<div style={{position:'absolute',left:60,top:815,width:780,height:7,background:'#414149',borderRadius:8}}><div style={{width:`${days/30*100}%`,height:'100%',background:S.accentDark,borderRadius:8}}/></div></Plate>
<Tag text="10月14日 · 名单公布" x={130} y={1390} w={820} h={130} size={53} style={{opacity:focus,transform:`translateY(${(1-focus)*30}px)`}}/>
</>;}
// T14e: retain progressive numeric settling and focused metric; portrait 2×2 grid follows speech, not totals.
export function StatGroups({t}:any){const rows=[['腾讯',66,1.36,['微信','QQ','元宝']],['阿里巴巴',23,9.17,['淘宝','支付宝','高德']],['快手',14,16.13,[]],['美团',11,18.91,[]]];const active=t<9.17?0:t<16.13?1:t<18.91?2:3;const isDeep=t>=21.69;return <>
<Txt y={160} size={72}>哪些 App 拒绝了？</Txt><Txt y={260} size={35} heavy={false} color={S.muted}>媒体统计 · 各公司及关联生态</Txt>
{rows.map(([name,num,at,apps]:any,i:number)=>{const e=p(t,at-.35,at+.2),settle=p(t,at,at+.5);const x=90+(i%2)*470,y=390+Math.floor(i/2)*435;const dark=active===i&&!isDeep;return <Plate key={i} x={x} y={y+(1-e)*45} w={430} h={395} dark={dark} style={{opacity:t<at-.35?.12:e,transform:`scale(${dark?1.015:1})`}}><Txt x={35} y={35} w={360} size={49} color={dark?'#fff':ink}>{name}</Txt><Txt x={35} y={125} w={360} size={136} color={dark?S.accentDark:ink}>{t>=at?Math.round(num*settle):'—'}<span style={{fontSize:35,marginLeft:15}}>款</span></Txt><Txt x={35} y={300} w={360} size={32} color={dark?'#d1d1d7':S.muted}>{apps.length?apps.filter((_:any,j:number)=>t>at+1.8+j*.8).join('  '):'及关联生态'}</Txt></Plate>})}
{!isDeep?<ArticleFocus t={t} image={t<9.17?'news-3.jpg':'news-4.jpg'} crop={t<9.17?[198,373,630,62]:[198,312,636,88]} top={1325} width={900} lift={false}/>:<><Tag text="DeepSeek 也在名单中" x={90} y={1315} w={900} h={130} size={54} style={{transform:`scale(${mix(.9,1,springAt(t,21.69,.6))})`}}/><ArticleFocus t={t-21.69} image="news-2.jpg" crop={[229,470,548,29]} top={1470} width={900} label="澎湃 · 2026-10-14 21:40"/></>}
</>;}
// L81-R006: multiple visible inputs merge to a single entry; route continuity exposes who gets bypassed.
export function EntryAction({t}:any){const change=p(t,2.35,3),merge=p(t,7,7.65),scan=p(t,10.55,11.2);const modes=['首页','推荐','广告'];return <>
<Txt y={160} size={78}>入口，换了</Txt>
<Tag text="你" x={435} y={365} w={210} h={120} size={64}/>
<Svg><Line d="M540 500 V660" progress={p(t,0,.5)} color={change>0?'#ccc':ink}/><Line d="M540 500 C950 500 950 730 760 760" progress={change} color={purple}/></Svg>
<Plate x={100} y={690} w={540} h={260} dark style={{opacity:1-change*.6}}><Txt x={0} y={68} w={540} size={76} align="center" color="#fff">淘宝</Txt><Txt x={0} y={178} w={540} size={31} align="center" color="#b8b8c0">原来的入口</Txt></Plate>
<Tag text="豆包" x={690} y={700} w={290} h={120} size={60} style={{opacity:change,transform:`translateY(${(1-change)*50}px)`}}/>
{modes.map((s,i)=>{const x=mix(90+i*310,390,merge),y=mix(1090,1180,merge);return <React.Fragment key={s}><div style={{opacity:1-merge}}><Svg><Line d={`M370 960 V1030 H${245+i*310} V1080`} progress={p(t,.4,1)} color={change>.1?'#ceced3':ink}/></Svg></div><Plate x={x} y={y} w={280} h={220} dark style={{opacity:1-merge,transform:`scale(${mix(1,.7,merge)})`}}><Txt x={0} y={78} w={280} size={55} color={t>3.5+i*.8?'#8a8a92':'#fff'} align="center">{s}</Txt></Plate></React.Fragment>})}
{t>6.6&&<Tag text="谁来看？" x={260} y={1390} w={560} h={140} size={78} style={{opacity:p(t,6.6,7),transform:`scale(${mix(.8,1,springAt(t,6.6,.65))})`}}/>}
</>;}
// L81-R006 continues the same packet objects; T13d return lane becomes screen-reading information path.
export function DataAction({t}:any){const scan=clamp((t-.6)/2.1),merge=p(t,2.7,3.35);return <>
<Txt y={160} size={78}>屏幕上的内容<br/><span style={{color:purple}}>AI 也要读一遍</span></Txt>
<Phone x={120} y={480} w={520} h={880}>{['商品信息','聊天内容','任务页面'].map((v,i)=><div key={v} style={{position:'absolute',left:40,top:170+i*185,width:410,height:140,background:'#eeeef2',borderRadius:20,padding:'40px 20px',boxSizing:'border-box',fontSize:48,color:ink}}>{v}</div>)}<div style={{position:'absolute',left:12,right:12,top:160+scan*560,height:9,background:purple,boxShadow:`0 8px 20px ${purple}44`}}/></Phone>
<Tag text="AI" x={760} y={830} w={220} h={140} size={76}/>
<Svg><Line d="M660 900 H750" progress={p(t,1.1,1.6)} color={purple}/></Svg>
{[0,1,2].map(i=>{const u=p(t,.7+i*.6,1.3+i*.6);return u>0&&u<1?<div key={i} style={{position:'absolute',left:mix(620,810,u),top:mix(700+i*100,875,u),width:35,height:35,borderRadius:10,background:purple}}/>:null})}
<Txt y={1450} size={40} align="center" color={S.muted}>读屏，是完成操作的一部分</Txt>
</>;}
// T04f: actual key shaft/teeth, tip pivot and dependent locks; permission remains ungranted, no unlock claim.
export function PermissionAction({t,responsibility=false}:any){const a=p(t,.1,.7);const stop=p(t,1,1.6);return <>
<Txt y={170} size={78}>{responsibility?'出了事，谁负责？':'这把钥匙，在平台手里'}</Txt>
<div style={{position:'absolute',left:110,top:580,width:590,height:125,transform:`translateX(${mix(-300,0,a)}px) rotate(${-3*stop+(t>4.2&&t<4.7?Math.sin((t-4.2)*35)*2:0)}deg)`,transformOrigin:'590px 62px',opacity:a}}><div style={{position:'absolute',left:330,top:48,width:260,height:30,background:ink,borderRadius:16}}/>{[440,510].map(x=><div key={x} style={{position:'absolute',left:x,top:70,width:28,height:48,borderRadius:'0 0 8px 8px',background:ink}}/>)}<Tag text={responsibility?'责任':'平台许可'} x={0} y={0} w={390} h={125} size={58}/></div>
<Lock x={760} y={560} size={150} color={ink}/>
<Svg>{[310,770].map((x,i)=><Line key={x} d={`M835 740 V840 H${x} V975`} progress={p(t,1.5+i*.15,2+i*.15)} color="#c1c1c8"/>)}</Svg>
{[responsibility?'付钱':'点外卖',responsibility?'聊天':'打车'].map((v,i)=><Plate key={v} x={100+i*460} y={990} w={420} h={300} style={{background:'#ededf1',opacity:p(t,.4+i*.15,.9+i*.15)}}><Lock x={175} y={45} size={70} color="#96969e"/><Txt x={0} y={155} w={420} size={66} align="center" color={ink}>{v}</Txt></Plate>)}
<Tag text={responsibility?'用户 · AI · 平台 ？':t>6?'平台，让不让？':'能力 ≠ 许可'} x={170} y={1400} w={740} h={138} size={66} style={{opacity:p(t,2.1,2.6)}}/>
</>;}
