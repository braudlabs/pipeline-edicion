from pathlib import Path
import subprocess,json,numpy as np,hashlib
R=Path(__file__).resolve().parents[1];v=R/'output/AD1-Churros-Cocina-FINAL.mp4';wav=R/'public/assets/audio-mix-master.wav'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]));vs=probe['streams'][0]
assert int(vs['nb_frames'])==3400 and vs['r_frame_rate']=='48/1'
assert vs['width']==1080 and vs['height']==1920
assert len(probe['streams'])==2
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32)
a=audio(v);b=audio(wav);n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.998,corr
r=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],capture_output=True);assert r.returncode==0 and not r.stderr,r.stderr
(R/'analysis/decode-errors.log').write_bytes(r.stderr)
# True native motion at 48 fps: consecutive camera-turn frames are distinct.
start=json.load(open(R/'src/timeline.json'))['events']['accounts']['from']+68
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vf',f'select=between(n\\,{start}\\,{start+19}),scale=135:240,format=gray','-fps_mode','passthrough','-frames:v','20','-f','rawvideo','-'])
f=np.frombuffer(raw,np.uint8).reshape(-1,240,135);unique=len({hashlib.sha256(x.tobytes()).hexdigest() for x in f});assert len(f)==20 and unique==20
report={'video':'AD1-Churros-Cocina-FINAL.mp4','width':1080,'height':1920,'fps':48,'frames':3400,'durationSeconds':3400/48,'audioCorrelationAtZeroLag':corr,'decodedWithoutErrors':True,'nativeMotionFramesTested':20,'distinctConsecutiveMotionFrames':unique,'sizeBytes':v.stat().st_size,'sha256':hashlib.sha256(v.read_bytes()).hexdigest()}
(R/'analysis/final-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
