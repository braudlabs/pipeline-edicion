/** Evaluate a measured/fitted trajectory in source-frame units at arbitrary output fps. */
export function sampleReferenceTranslation(profile,elapsedSeconds,targetHeight,{allowExtrapolation=false}={}){
 if(!Number.isFinite(elapsedSeconds)||elapsedSeconds<0||!Number.isFinite(targetHeight)||targetHeight<=0)throw Error('Invalid motion sample');
 if(!profile?.sourceFps?.num||!profile?.sourceFps?.den||!profile.sourceHeight)throw Error('Missing source coordinate system');
 const age=elapsedSeconds*profile.sourceFps.num/profile.sourceFps.den;
 const [a,b]=profile.fitDomainSourceFrames;
 const extrapolated=age<a-1e-9||age>b+1e-9;
 if(extrapolated&&!allowExtrapolation)throw Error('Outside measured domain; extrapolation is an explicit design proposal');
 const dy=Math.exp(-profile.decayPerSourceFrame*age)*(profile.cosCoefficientPx*Math.cos(profile.omegaRadiansPerSourceFrame*age)+profile.sinCoefficientPx*Math.sin(profile.omegaRadiansPerSourceFrame*age));
 return {translationY:dy*targetHeight/profile.sourceHeight,sourceFrameAge:age,extrapolated,provenance:'fit_to_decoded_position_not_original_easing'};
}
