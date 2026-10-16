"""Ajusta fuente, cuerpo e interletrado de un rótulo blanco a su máscara medida."""
import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from h import *
from PIL import ImageFont, ImageDraw
FONTS = {'HelveticaNeue-Bold': ('/System/Library/Fonts/HelveticaNeue.ttc', 1), 'HelveticaNeue-Medium': ('/System/Library/Fonts/HelveticaNeue.ttc', 10),
         'Helvetica-Bold': ('/System/Library/Fonts/Helvetica.ttc', 1), 'Arial-Bold': ('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 0),
         'SFProDisplay-Bold': (str(Path.home()/'Library/Fonts/SFPRODISPLAYBOLD.OTF'), 0)}
def render(text, fontkey, size, track, canvas=(1400, 600), kern=True):
    path, idx = FONTS[fontkey]
    f = ImageFont.truetype(path, size, index=idx)
    im = Image.new('L', canvas, 0); d = ImageDraw.Draw(im)
    x = 100.0
    for i, ch in enumerate(text):
        d.text((x, 100), ch, font=f, fill=255)
        adv = f.getlength(ch)
        if kern and i + 1 < len(text):
            adv = f.getlength(text[i:i+2]) - f.getlength(text[i+1])
        x += adv + track
    return np.asarray(im) > 127
def tight(m):
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1]
def iou(a, b):
    H = max(a.shape[0], b.shape[0]); W = max(a.shape[1], b.shape[1])
    best = 0
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            A = np.zeros((H+8, W+8), bool); B = np.zeros((H+8, W+8), bool)
            A[4:4+a.shape[0], 4:4+a.shape[1]] = a
            B[4+dy:4+dy+b.shape[0], 4+dx:4+dx+b.shape[1]] = b
            v = (A & B).sum() / (A | B).sum()
            best = max(best, v)
    return best
def target(slug, frame_a, frame_b, roi, thr=235):
    F = frames(slug, frame_a, frame_b)
    x0, y0, x1, y1 = roi
    st = np.ones((y1-y0, x1-x0), bool)
    for n in F: st &= F[n][y0:y1, x0:x1].min(2) >= thr
    return tight(st)
if __name__ == '__main__':
    slug = sys.argv[1]; text = sys.argv[2]; a, b = int(sys.argv[3]), int(sys.argv[4])
    roi = [int(v) for v in sys.argv[5].split(',')]
    sizes = [float(v) for v in sys.argv[6].split(':')]; tracks = [float(v) for v in sys.argv[7].split(':')]
    T = target(slug, a, b, roi)
    print('objetivo', T.shape[::-1], 'px (ancho, alto)')
    for fk in FONTS:
        res = []
        for s in np.arange(sizes[0], sizes[1]+1e-9, sizes[2]):
            for t in np.arange(tracks[0], tracks[1]+1e-9, tracks[2]):
                R = tight(render(text, fk, s, t))
                if abs(R.shape[1]-T.shape[1]) > 12 or abs(R.shape[0]-T.shape[0]) > 12: continue
                res.append((iou(T, R), s, t, R.shape[::-1]))
        res.sort(reverse=True)
        print(fk, [(round(r[0],3), r[1], r[2], r[3]) for r in res[:3]])
