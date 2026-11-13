// Adapted from FredTalk SmileySubtitle: same cue clock, font and black fit-content carrier; portrait geometry.
import React from 'react';
import {useCurrentFrame} from 'remotion';
import timing from '../timing.json';
export const SmileySubtitle=()=>{const t=useCurrentFrame()/60;const c=timing.subtitles.find(c=>t>=c.startSeconds&&t<c.endSeconds);return c?<div style={{position:'absolute',bottom:230,left:70,right:70,display:'flex',justifyContent:'center',zIndex:100}}><div style={{background:'#000',color:'#fff',fontFamily:'FredSmileySans',fontSize:48,lineHeight:1.22,padding:'18px 28px',borderRadius:17,textAlign:'center',maxWidth:940,fontWeight:400,fontSynthesis:'none',whiteSpace:'pre-wrap'}}>{c.text}</div></div>:null;};
