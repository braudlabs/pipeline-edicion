export type TranslationProfile = {
  sourceFps: {num:number;den:number};
  sourceHeight:number;
  fitDomainSourceFrames:number[];
  decayPerSourceFrame:number;
  omegaRadiansPerSourceFrame:number;
  cosCoefficientPx:number;
  sinCoefficientPx:number;
};
export function sampleReferenceTranslation(
  profile:TranslationProfile,
  elapsedSeconds:number,
  targetHeight:number,
  options?:{allowExtrapolation?:boolean},
):{
  translationY:number;
  sourceFrameAge:number;
  extrapolated:boolean;
  provenance:'fit_to_decoded_position_not_original_easing';
};
