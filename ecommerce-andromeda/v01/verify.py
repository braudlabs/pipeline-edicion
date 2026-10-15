from pathlib import Path
import json,subprocess,hashlib
p=Path(__file__).resolve().parent
T=json.loads((p/'timeline.json').read_text());C=json.loads((p/'cues.json').read_text());A=json.loads((p/'audio.json').read_text())
assert T['fps']==24 and T['assembled_frames']==920
last=0
for s in T['scenes']:
 assert s['record_in_frame']==last and s['record_out_frame']-s['record_in_frame']==s['duration_frames']
 assert s['source_out_frame']-s['source_in_frame']==s['duration_frames']
 assert hashlib.sha256((p/'public'/s['asset']).read_bytes()).hexdigest()==s['sha256']
 last=s['record_out_frame']
assert last==920
assert T['scenes'][2]['source_in_frame']==12
assert next(s for s in T['scenes'] if s['id']=='03b_repetir')['duration_frames']==58
for i,c in enumerate(C):
 assert 0<=c['start']<c['end']<=920
 if i:assert C[i-1]['end']<=c['start']
 assert all(w['frame']>=c['start'] and w['frame']<c['end'] for w in c['words'])
 if c['kind']!='drop':assert 400<=c['y']<=1190
assert sum(len(c['words']) for c in C)==119
assert all(t.get('retiming') is False for t in A['tracks'][:2])
assert A['tracks'][1]['containsOriginalOffsetSeconds']==1.97
assert A['tracks'][3]['enabled'] is False
r={'sourceSha256':'8/8 match','montageFrames':920,'cutsPreserved':True,'ticketOffsetFrames':12,'bridge03bFrames':58,'audio':A,'captionPhrases':len(C),'timedWords':119,'drawnPhrases':sum(c['kind']!='drop' for c in C),'omittedPhrases':[{'text':c['text'],'start':c['start']/24,'end':c['end']/24,'reason':c['reason']} for c in C if c['kind']=='drop'],'metaPlacement':{'anchorY':[430,1190],'guide':[65,270,1015,1248],'status':'conservative internal guide; not actual Ads Manager UI; per-frame visual review required'},'unfinished':True,'provisionalScene':'06_cinco_ads','fullDurationPending':85.39425,'listening':'not independently verified; dapi CLI unavailable (no response)','lipSyncHook':'pending; untouched','music':'pending; no provisional music','approval':'pending'}
f=p/'Andromeda-00-38s-V01-PREVIEW.mp4'
if f.exists():
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,duration','-show_entries','format=duration','-of','json',str(f)]))
 v=next(s for s in probe['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1080,1920,'24/1','920')
 assert any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in probe['streams'])
 r['render']=probe;r['outputSha256']=hashlib.sha256(f.read_bytes()).hexdigest()
(p/'QA.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('Verified timeline, sources, caption boundaries and audio configuration'+(' + output format' if f.exists() else ''))
