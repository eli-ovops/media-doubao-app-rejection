import React from 'react';import {Composition,registerRoot} from 'remotion';import {Film} from './Film';import timing from './timing.json';
const Root=()=> <Composition id="DoubaoFull" component={Film} durationInFrames={timing.totalFrames} width={1080} height={1920} fps={60}/>;registerRoot(Root);
