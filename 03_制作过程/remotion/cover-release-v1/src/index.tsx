// Cover adaptation of this episode Opening + T13d RequestAction rejection. Actual raw-video still; no subtitle layer or face synthesis.
import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Img,Composition,registerRoot,staticFile,delayRender,continueRender,cancelRender} from 'remotion';
import {S} from './kit/theme';import {Txt,Tag,Plate,Line} from './components/Actions';
const Fonts=()=>{const [h]=useState(()=>delayRender('Exact kit fonts'));useEffect(()=>{Promise.all([['MiSans-Medium.otf','500'],['MiSans-Heavy.otf','900']].map(async([file,weight])=>{const f=new FontFace(S.body,`url(${staticFile('fonts/'+file)})`,{weight});await f.load();document.fonts.add(f)})).then(()=>continueRender(h)).catch(cancelRender)},[h]);return null};
const Person=({x,y,w,h}:any)=><div style={{position:'absolute',left:x,top:y,width:w,height:h,overflow:'hidden',borderRadius:S.radius,boxShadow:S.shadow}}><Img src={staticFile('person.png')} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'50% 53%'}}/></div>;
const Cover=({wide=false}:any)=><AbsoluteFill style={{background:'#fafafa',fontFamily:S.body,color:S.ink,fontSynthesis:'none'}}><Fonts/>{wide?<>
<Person x={1060} y={180} w={430} h={740}/>
<Txt x={450} y={290} w={590} size={68}>豆包想帮你<br/>点外卖</Txt>
<svg width={1920} height={1080} style={{position:'absolute'}}><Line d="M480 500 H960 V550" color={S.accent}/></svg>
<Tag text="美团说：不行" x={450} y={575} w={570} h={140} size={65} style={{background:'#ac3639'}}/>
</>:<>
<Txt x={170} y={440} w={740} size={88} align="center">豆包想帮你<br/>点外卖</Txt>
<svg width={1080} height={1920} style={{position:'absolute'}}><Line d="M260 660 H820" color={S.accent}/></svg>
<Tag text="美团说：不行" x={220} y={690} w={640} h={130} size={72} style={{background:'#ac3639'}}/>
<Person x={220} y={870} w={640} h={640}/>
</>}</AbsoluteFill>;
registerRoot(()=> <><Composition id="CoverPortrait" component={Cover} width={1080} height={1920} fps={60} durationInFrames={1}/><Composition id="CoverLandscape" component={Cover} defaultProps={{wide:true}} width={1920} height={1080} fps={60} durationInFrames={1}/></>);
