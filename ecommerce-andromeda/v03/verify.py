from pathlib import Path
import json,subprocess,hashlib
p=Path(__file__).resolve().parent
T=json.loads((p/'timeline.json').read_text());E=json.loads((p/'choreography.json').read_text());old=json.loads((p.parent/'v01/cues.json').read_text())
original=[(w['text'],w['frame']) for c in old for w in c['words']];current=[(w['text'],w['frame']) for e in E for w in e['sourceWords']]
assert original==current and len(current)==119
for e in E:
 assert 0<=e['start']<e['end']<=920
 assert all(e['start']<=w['frame']<e['end'] for w in e['sourceWords'])
 assert 400<=e['y']<=1205
masks=json.loads((p/'study/mask-frames.json').read_text());assert all((p/'public/assets/masks'/f'{f:04}.png').exists() for f in masks)
for s in T['scenes']:assert hashlib.sha256((p/'public'/s['asset']).read_bytes()).hexdigest()==s['sha256']
assert T['scenes'][2]['source_in_frame']==12
mixhash=hashlib.sha256((p/'public/assets/mix-preview.wav').read_bytes()).hexdigest();assert mixhash==hashlib.sha256((p.parent/'v02/public/assets/mix-preview.wav').read_bytes()).hexdigest()
file=p/'Andromeda-00-38s-V03-PREVIEW.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,duration','-show_entries','format=duration','-of','json',str(file)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1080,1920,'48/1','1840')
result={'render':probe,'narrationWords':119,'coveredNarrationWords':119,'omittedNarrationWords':0,'captionElements':len(E),'occlusionElements':sum(e['motion']=='occlusion' for e in E),'maskFrames':len(masks),'sourceTimelineFps':24,'sourceTimelineFrames':920,'outputFps':48,'outputFrames':1840,'sourceHashes':'8/8 match','ticketSourceOffsetFrames':12,'audioMixMatchesV02':True,'audioMixSha256':mixhash,'nativeHook':json.loads((p/'study/native-audio-QA.json').read_text()),'provisionalScene':'06_cinco_ads','fullAdComplete':False,'userApproval':False,'priorFeedback':'V02 improves somewhat; laggy perception and missing captions; requested more foreground contour/background fill resource','scope':'Complete supplied narration, not a new caption track for simultaneous native whisper','visualReview':{'fullPlaybackOrListening':False}}
(p/'QA.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('PASS: source clock, 119/119 words, masks, native mix unchanged, 1840 frames / 48 fps')
