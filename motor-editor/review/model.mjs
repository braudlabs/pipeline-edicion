export function nearestFrame(times,seconds){let lo=0,hi=times.length-1;while(lo<hi){const mid=Math.ceil((lo+hi)/2);if(times[mid]<=seconds+1e-7)lo=mid;else hi=mid-1;}return lo;}
export function validateNote(note,version){
 const frame=n=>Number.isInteger(n)&&n>=0&&n<version.frameCount;
 if(!note||!frame(note.startFrame)||!frame(note.endFrame)||note.endFrame<note.startFrame)throw Error('Intervalo de fotogramas inválido');
 if(typeof note.text!=='string'||!note.text.trim()||note.text.length>10000)throw Error('Escribe una indicación de hasta 10.000 caracteres');
 if(!['imagen','texto','audio','ritmo','otro'].includes(note.category))throw Error('Categoría inválida');
 if(!Array.isArray(note.shapes)||note.shapes.length>100)throw Error('Marcas inválidas');
 for(const s of note.shapes){if(!frame(s.frame)||s.frame<note.startFrame||s.frame>note.endFrame||!['point','rect','arrow'].includes(s.type)||!Array.isArray(s.points)||s.points.length!==(s.type==='point'?1:2)||!s.points.every(p=>Number.isFinite(p.x)&&p.x>=0&&p.x<=1&&Number.isFinite(p.y)&&p.y>=0&&p.y<=1))throw Error('Marca fuera del intervalo o de la imagen');}
 return {startFrame:note.startFrame,endFrame:note.endFrame,text:note.text.trim(),category:note.category,shapes:note.shapes.map(s=>({type:s.type,frame:s.frame,points:s.points.map(p=>({x:p.x,y:p.y}))}))};
}
export function exportFeedback(project){return {schema:'ale.video-review/1',projectId:project.id,frameConvention:'zero-based, inclusive start and end; use frameTimes for VFR',versions:project.versions,notes:project.notes};}
