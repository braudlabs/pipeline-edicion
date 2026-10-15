// Drafts preserve unfinished direction separately from the saved production state.
export function draftKey(form, context) {
  return ['braud-studio-draft-v1',context.pieceId||'none',form.id,form.sceneId||context.sceneId||'',form.assetId||''].join(':');
}

// The source snapshot protects saves from concurrent edits; it is not an edit
// itself. Keep it in storage and restoration, but omit it from dirty checks.
function editableFields(fields) {
  if (!Array.isArray(fields)) return null;
  const result=[];
  for (const field of fields) {
    if (!field || typeof field.key!=='string') return null;
    if (field.key==='_sourceScript') continue;
    const value=typeof field.value==='boolean'?field.value:String(field.value??'');
    result.push([field.key,value]);
  }
  return result.sort((a,b)=>a[0].localeCompare(b[0])||JSON.stringify(a[1]).localeCompare(JSON.stringify(b[1])));
}

export function hasDraftChanges(fields,currentFields) {
  const draft=editableFields(fields),current=editableFields(currentFields);
  // An unknown or removed field must remain recoverable, never silently clean.
  return draft===null || current===null || JSON.stringify(draft)!==JSON.stringify(current);
}

export function createDraftStore(storage) {
  return {
    read(key,{includeInactive=false}={}) { try { const d=JSON.parse(storage.getItem(key));return d&&d.version===1&&Array.isArray(d.fields)&&(includeInactive||d.active!==false)?d:null; } catch { return null; } },
    write(key, fields) { try { storage.setItem(key,JSON.stringify({version:1,active:true,fields,updatedAt:new Date().toISOString()}));return true; } catch { return false; } },
    reconcile(key) {
      try {
        const raw=storage.getItem(key);
        if(raw===null)return true;
        const draft=JSON.parse(raw);
        if(!draft||draft.version!==1||!Array.isArray(draft.fields))return false;
        if(draft.active===false)return true;
        storage.setItem(key,JSON.stringify({...draft,active:false,reconciledAt:new Date().toISOString()}));
        return true;
      } catch { return false; }
    },
    entries(prefix='',{includeInactive=false}={}) {
      const entries=[];
      try {
        for(let i=0;i<storage.length;i++) {
          const key=storage.key(i);
          if(typeof key!=='string'||!key.startsWith(prefix))continue;
          const draft=this.read(key,{includeInactive});
          if(draft)entries.push({key,draft});
        }
      } catch {}
      return entries;
    },
    has(prefix) { return this.entries(prefix).length>0; },
    clear(key) { try { storage.removeItem(key);return true; } catch { return false; } }
  };
}
