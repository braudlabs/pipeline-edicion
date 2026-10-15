"""Raise close shots, preserve aspect/cadence and extend only peripheral edges."""
from pathlib import Path
import subprocess,concurrent.futures
R=Path(__file__).resolve().parents[1];out=R/'public/assets/v5';out.mkdir(exist_ok=True)
def make(i):
 if i==6:
  vf='scale=972:1728:flags=lanczos,crop=972:1528:0:200,pad=1080:1920:54:0,fillborders=left=54:right=54:bottom=392:mode=smear'
 else:
  vf='crop=1080:1700:0:220,pad=1080:1920:0:0,fillborders=bottom=220:mode=smear'
 # Blend peripheral extension into a soft lens falloff; never stretch visible hands.
 start=1260 if i==6 else 1480
 expr=f'min(1,max(0,(Y-{start})/180))'
 graph=f'[0:v]{vf},split[sharp][soft];[soft]gblur=sigma=90:sigmaV=50[blurred];[sharp][blurred]blend=all_expr=\'A*(1-({expr}))+B*({expr})\'[out]'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/f'public/assets/{i:02}.mp4'),'-an','-filter_complex',graph,'-map','[out]','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(out/f'{i:02}-reframed.mp4')],check=True)
 print('Reframed',i,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(make,[1,2,4,5,6,7,8,11,12]))
