"""Hoja de recortes nativos con escala: crops.py A B x0,y0,x1,y1 escala cols salida [paso] [slug]
   o lista de fotogramas: crops.py f1,f2,f3 - x0,y0,x1,y1 escala cols salida"""
import sys
from PIL import Image
from lib import run, label_sheet, info, t_of
if ',' in sys.argv[1] or sys.argv[2] == '-':
    fr = [int(v) for v in sys.argv[1].split(',')]
    box = [int(v) for v in sys.argv[3].split(',')]; sc = float(sys.argv[4]); cols = int(sys.argv[5]); out = sys.argv[6]
    slug = sys.argv[7] if len(sys.argv) > 7 else 'v6-ads90-rev'
    ims = run(min(fr), max(fr), slug)
    items = [(f"f{f} {t_of(f, info()):.3f}s", ims[f - min(fr)].crop(box)) for f in fr]
else:
    a, b = int(sys.argv[1]), int(sys.argv[2])
    box = [int(v) for v in sys.argv[3].split(',')]; sc = float(sys.argv[4]); cols = int(sys.argv[5]); out = sys.argv[6]
    step = int(sys.argv[7]) if len(sys.argv) > 7 else 1
    slug = sys.argv[8] if len(sys.argv) > 8 else 'v6-ads90-rev'
    ims = run(a, b, slug)
    items = [(f"f{a + k} {t_of(a + k, info()):.3f}s", im.crop(box)) for k, im in enumerate(ims) if k % step == 0]
label_sheet(items, cols, out, scale=sc, font_px=18)
