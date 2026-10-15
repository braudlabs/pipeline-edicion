import metrics from '../data/font-metrics.json' with {type:'json'};
export function textWidth(text:string,size:number,tracking=-.06,weight=700):number{
  const m=weight>=600?metrics.bold:metrics.regular;
  const advances=m.advances as Record<string,number>,kern=m.kerning as Record<string,number>;
  const cs=Array.from(text.normalize('NFC'));let n=0;
  for(let i=0;i<cs.length;i++){
    if(advances[cs[i]]===undefined)throw new Error(`Glifo sin métricas verificadas: ${cs[i]}`);
    n+=advances[cs[i]];
    if(i)n+=(kern[cs[i-1]+cs[i]]??0)+tracking;
  }
  return Math.max(0,n*size);
}
export function fitText(text:string,width:number,maxSize:number,tracking=-.06,weight=700){const unit=textWidth(text,1,tracking,weight);return Math.min(maxSize,width/Math.max(.01,unit));}
