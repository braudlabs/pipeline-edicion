"""Utilidades propias del revisor v5-maquina-B: decodificación rápida de tramos a resolución nativa."""
import subprocess, sys
from pathlib import Path
import numpy as np
ROOT = Path('/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/estilo-editor')
sys.path.insert(0, str(ROOT / 'scripts'))
from common import probe, src  # noqa
SLUG = 'v5-maquina'
INFO = probe(SLUG)
W, H = INFO['width'], INFO['height']

def run(a, b):
    """dict {n: array HxWx3 uint8} de los fotogramas a..b (incluido)."""
    count = b - a + 1
    t = max(0.0, (a - 0.5) * INFO['fps_den'] / INFO['fps_num'])
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.6f}', '-i', str(src(SLUG)), '-frames:v', str(count),
                          '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return {a + k: arr[k] for k in range(arr.shape[0])}

def lum(im):
    im = im.astype(np.float32)
    return 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]

def track(A, B, box, r=24):
    """Desplazamiento (dx,dy) del parche box=(x0,y0,x1,y1) de la imagen A dentro de B, búsqueda ±r px (SSD sobre luminancia)."""
    x0, y0, x1, y1 = box
    LA = lum(A)[y0:y1, x0:x1]
    LB = lum(B)
    best = None
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            yy0, xx0 = y0 + dy, x0 + dx
            if yy0 < 0 or xx0 < 0 or yy0 + (y1 - y0) > LB.shape[0] or xx0 + (x1 - x0) > LB.shape[1]:
                continue
            P = LB[yy0:yy0 + (y1 - y0), xx0:xx0 + (x1 - x0)]
            s = float(((P - LA) ** 2).mean())
            if best is None or s < best[0]:
                best = (s, dx, dy)
    return best

def save_sheet(items, path, cols=6, w=None, label=True, gap=4):
    """items: lista de (texto, array HxWx3). Hoja de contacto."""
    from PIL import Image, ImageDraw, ImageFont
    ims = []
    for t, a in items:
        im = Image.fromarray(a) if not hasattr(a, 'size') or isinstance(a, np.ndarray) else a
        if w:
            im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
        ims.append((t, im))
    tw, th = ims[0][1].size
    lab = max(14, tw // 14) if label else 0
    font = ImageFont.load_default(size=max(11, lab - 3)) if lab else None
    cols = min(cols, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (tw + gap) + gap, rows * (th + lab + gap) + gap), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for k, (t, im) in enumerate(ims):
        x = gap + (k % cols) * (tw + gap)
        y = gap + (k // cols) * (th + lab + gap)
        if lab:
            d.text((x + 2, y), t, fill=(255, 220, 90), font=font)
        sheet.paste(im, (x, y + lab))
    sheet.save(path, quality=90)
    print(path, sheet.size)

def _grad(L):
    gx = np.zeros_like(L); gy = np.zeros_like(L)
    gx[:, 1:-1] = L[:, 2:] - L[:, :-2]
    gy[1:-1, :] = L[2:, :] - L[:-2, :]
    return np.hypot(gx, gy)

def register(A, B, scales, angles, small=4):
    """Busca escala s, giro θ (grados, + = horario en pantalla) y traslación tales que A transformada ≈ B.
    A, B: arrays RGB. Devuelve (score, s, θ, tx, ty) con tx,ty en px nativos: p_B = s·R(θ)·(p_A − c) + c + t."""
    from PIL import Image
    Hh, Ww = A.shape[:2]
    w, hh = Ww // small, Hh // small
    a = Image.fromarray(lum(A).astype(np.uint8)).resize((w, hh), Image.BILINEAR)
    b = np.asarray(Image.fromarray(lum(B).astype(np.uint8)).resize((w, hh), Image.BILINEAR), np.float32)
    gb = _grad(b); gb = (gb - gb.mean()) / (gb.std() + 1e-6)
    Fb = np.fft.rfft2(gb)
    best = None
    cx, cy = w / 2, hh / 2
    for s in scales:
        for th in angles:
            r = np.deg2rad(th)
            c, sn = np.cos(r), np.sin(r)
            # PIL affine: salida(x,y) toma de entrada(a x + b y + c, d x + e y + f)  => inversa de la transformación directa
            # directa: p' = s R (p - c0) + c0 ; inversa: p = R^-1 (p' - c0)/s + c0
            ia, ib = c / s, sn / s
            id_, ie = -sn / s, c / s
            ic = cx - ia * cx - ib * cy
            if_ = cy - id_ * cx - ie * cy
            wa = np.asarray(a.transform((w, hh), Image.AFFINE, (ia, ib, ic, id_, ie, if_), Image.BILINEAR), np.float32)
            ga = _grad(wa); ga = (ga - ga.mean()) / (ga.std() + 1e-6)
            cc = np.fft.irfft2(Fb * np.conj(np.fft.rfft2(ga)), s=gb.shape)
            k = np.unravel_index(np.argmax(cc), cc.shape)
            sc = cc[k] / gb.size
            ty, tx = k
            if ty > hh // 2: ty -= hh
            if tx > w // 2: tx -= w
            if best is None or sc > best[0]:
                best = (float(sc), s, th, tx * small, ty * small)
    return best

def inkbox(im, roi, mode='white', thr=None, color=None):
    """Caja de tinta en roi=(x0,y0,x1,y1) px. mode white: min(R,G,B)>=thr(225); color: distancia a color<=thr(60).
    Devuelve dict con x0,y0,x1,y1,w,h,cx,cy,area o None."""
    x0, y0, x1, y1 = roi
    A = im[y0:y1, x0:x1].astype(np.float32)
    if mode == 'white':
        m = A.min(axis=2) >= (thr or 225)
    else:
        m = np.sqrt(((A - np.array(color, np.float32)) ** 2).sum(axis=2)) <= (thr or 60)
    if m.sum() < 8:
        return None
    ys, xs = np.where(m)
    # recorte robusto: ignora columnas/filas con menos de 2 px
    cs = m.sum(axis=0); rs = m.sum(axis=1)
    xi = np.where(cs >= 2)[0]; yi = np.where(rs >= 2)[0]
    if len(xi) == 0 or len(yi) == 0:
        return None
    bx0, bx1, by0, by1 = xi.min() + x0, xi.max() + x0, yi.min() + y0, yi.max() + y0
    return dict(x0=int(bx0), y0=int(by0), x1=int(bx1), y1=int(by1), w=int(bx1 - bx0 + 1), h=int(by1 - by0 + 1),
                cx=float((bx0 + bx1) / 2), cy=float((by0 + by1) / 2), area=int(m.sum()))
