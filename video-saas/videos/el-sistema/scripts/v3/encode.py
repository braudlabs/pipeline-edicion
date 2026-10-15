from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2]
source=R/'output/v3/El-Sistema-V3-Final.mov';dest=R/'output/v3/El-Sistema-V3.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(R/'assets/v3/Mix.wav'),'-map','0:v:0','-map','1:a:0','-t','46.3','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r','30','-fps_mode','cfr','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart','-map_metadata','-1','-write_tmcd','0',str(dest)],check=True)
probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,duration:format=duration,size','-of','json',str(dest)]).decode();(R/'analysis/v3/final-probe.json').write_text(probe)
with (R/'analysis/v3/decode-check.log').open('w') as out:subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],stderr=out,check=True)
print(probe)
