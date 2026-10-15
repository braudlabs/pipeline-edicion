import React from 'react';
import type {Node} from '../types.ts';
import {relationState} from './relation.ts';

export function RelationView({node:n,time,contextTime,width,height,fontFamily,weight=1}:{node:Node;time:number;contextTime:number;width:number;height:number;fontFamily:string;weight?:number}){
  const unique=React.useId();
  const s=n.relation!,p=relationState(s,time,contextTime);if(!p.visible)return null;
  const half=p.width/2,top=-s.height/2,bottom=s.height/2,r=width*.012;
  const id=`relation-${unique.replace(/[^a-zA-Z0-9_-]/g,'_')}`;
  return <svg width={width} height={height} style={{position:'absolute',inset:0,opacity:weight,mixBlendMode:weight<1?'plus-lighter':undefined,overflow:'visible'}}>
    <defs><clipPath id={id}><rect x={-half} y={top} width={p.width} height={s.height}/></clipPath></defs>
    <g transform={`translate(${n.x},${n.y})`}>
      <rect x={-half} y={top} width={p.width} height={s.height} fill={s.accent} opacity={.16}/>
      <g clipPath={`url(#${id})`} fontFamily={fontFamily} fontWeight={s.fontWeight} fontSize={s.fontSize} textAnchor="middle" dominantBaseline="central" letterSpacing={s.fontSize*s.tracking} fill={s.inkColor}>
        <text opacity={p.fromOpacity}>{s.from}</text>
        <text opacity={p.toOpacity} transform={`translate(0,${p.toY})`}>{s.to}</text>
      </g>
      <path d={`M${-half},${top-r}V${bottom} M${half},${top}V${bottom+r}`} fill="none" stroke={s.accent} strokeWidth={width*.0025}/>
      <circle cx={-half} cy={top-r} r={r} fill={s.accent}/>
      <circle cx={half} cy={bottom+r} r={r} fill={s.accent}/>
      <text y={top-s.contextSize*.85} opacity={p.contextOpacity} textAnchor="middle" dominantBaseline="central" fontFamily={fontFamily} fontWeight={400} fontSize={s.contextSize} letterSpacing={s.contextSize*s.tracking} fill={s.inkColor}>{p.context}</text>
    </g>
  </svg>;
}
