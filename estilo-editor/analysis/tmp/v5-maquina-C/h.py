"""Ayudas locales del revisor v5-maquina-C: carga de fotogramas nativos cacheados y hojas."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = Path('/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/estilo-editor')
sys.path.insert(0, str(ROOT/'scripts'))
from common import probe, src
TMP = ROOT/'analysis/tmp/v5-maquina-C'
FULL = TMP/'full'
INFO = probe('v5-maquina')
FPS = INFO['fps']
def t_of(f): return f*INFO['fps_den']/INFO['fps_num']
def load(f):
    return Image.open(FULL/f'f{f:06d}.jpg').convert('RGB')
def arr(f):
    return np.asarray(load(f), np.float32)
def png(f):
    """decodifica exacto (PNG) un fotograma"""
    import subprocess, io
    t = max(0.0, (f-0.5)*INFO['fps_den']/INFO['fps_num'])
    raw = subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.6f}','-i',str(src('v5-maquina')),'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True).stdout
    return Image.open(io.BytesIO(raw)).convert('RGB')
def run_raw(a, count):
    """count fotogramas consecutivos desde a, exactos, como arrays uint8"""
    import subprocess
    t = max(0.0, (a-0.5)*INFO['fps_den']/INFO['fps_num'])
    p = subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.6f}','-i',str(src('v5-maquina')),'-frames:v',str(count),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True).stdout
    A = np.frombuffer(p, np.uint8).reshape(-1,1920,1080,3)
    return A
try:
    FONT = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
except Exception:
    FONT = ImageFont.load_default()
def sheet(frames, out, crop=None, w=None, cols=6, label=True, scale=None, pad=4):
    """crop=(x,y,w,h) normalizado o en px si >1; w = ancho de cada miniatura"""
    ths=[]
    for f in frames:
        im = load(f)
        if crop:
            x,y,cw,ch = crop
            if max(crop) <= 1.0:
                x,y,cw,ch = int(x*1080), int(y*1920), int(cw*1080), int(ch*1920)
            im = im.crop((int(x),int(y),int(x+cw),int(y+ch)))
        if scale:
            im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
        if w:
            im = im.resize((w, int(im.height*w/im.width)), Image.LANCZOS)
        if label:
            lab = Image.new('RGB',(im.width, im.height+26),(20,20,20))
            lab.paste(im,(0,26))
            d = ImageDraw.Draw(lab)
            d.text((3,1), f'f{f} {t_of(f):.2f}s', fill=(255,220,90), font=FONT)
            im = lab
        ths.append(im)
    cols = min(cols, len(ths))
    rows = (len(ths)+cols-1)//cols
    tw, th = ths[0].size
    S = Image.new('RGB',(cols*(tw+pad)+pad, rows*(th+pad)+pad),(40,40,40))
    for i,im in enumerate(ths):
        S.paste(im,(pad+(i%cols)*(tw+pad), pad+(i//cols)*(th+pad)))
    out = Path(out)
    if not out.is_absolute(): out = TMP/out
    S.save(out, quality=90)
    print(out, S.size)
