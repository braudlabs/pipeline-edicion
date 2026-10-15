// Shared by the delivery dialog and the exported manifest.
export function deliveryReadiness(piece,assets){
 const missing=[],warnings=[],byId=new Map(assets.map(a=>[a.id,a]));let selected=0;
 if(piece.kind==='video'){
  if(!piece.scenes.length)missing.push('Añadir escenas a la pieza');
  for(const scene of piece.scenes){
   const version=scene.versions.find(v=>v.assetId===scene.selectedId&&v.status==='approved');
   if(!version){missing.push(`${scene.title}: seleccionar un clip aprobado`);continue;}
   if(byId.get(version.assetId)?.kind!=='video'){missing.push(`${scene.title}: recuperar el archivo del clip`);continue;}
   selected++;
   if(scene.timeline?.assetId&&scene.timeline.assetId!==version.assetId)warnings.push(`${scene.title}: revisar los tiempos para el clip seleccionado`);
  }
  if(['off','mixed'].includes(piece.audioMode)&&byId.get(piece.audioId)?.kind!=='audio')missing.push('Añadir la locución de la pieza');
 }else{
  selected=(piece.selectedImages||[]).filter(id=>byId.get(id)?.kind==='image').length;
  if(!selected)missing.push('Seleccionar la imagen final');
 }
 return {selected,missing,warnings,readyForEditing:missing.length===0&&warnings.length===0};
}
