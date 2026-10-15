"""Compila la spec de diseño a operaciones de After Effects y las despacha.

El .aep se construye entero desde `src/design.json`. Si algo hay que cambiar,
se cambia el diseño y se vuelve a ejecutar esto: no se toca AE a mano. Es la
lección de AD3, donde la spec y el proyecto acabaron discrepando.
"""
from pathlib import Path
import json
import math
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ae import AE                                   # noqa: E402

R = Path(__file__).resolve().parents[1]
S = json.load(open(R / 'src/design.json'))
F = S['fps']
MASTER = S['master']

FONTS = {'bold': 'SFProDisplay-Bold', 'regular': 'SFProDisplay-Regular'}
PP = {k: ['ADBE Transform Group', v] for k, v in {
    'pos': 'ADBE Position', 'anchor': 'ADBE Anchor Point', 'scale': 'ADBE Scale',
    'rot': 'ADBE Rotate Z', 'opacity': 'ADBE Opacity'}.items()}
TRIM_END = ['ADBE Root Vectors Group', 1, 'ADBE Vectors Group',
            'ADBE Vector Filter - Trim', 'ADBE Vector Trim End']


def rgb(h):
    return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]


ops = []


def op(_op, **args):
    ops.append({'operation': _op, 'args': args})


def keys(comp, layer, prop, frames, values, ease='out', spatial=False):
    """Claves con la curva de la serie: influencia 80 de entrada, 15 de salida."""
    op('keyframe.set_batch', comp=comp, layer=layer, property=prop,
       times=[f / F for f in frames], values=values)
    for i in range(len(frames)):
        if ease == 'linear':
            op('keyframe.set_interpolation', comp=comp, layer=layer, property=prop,
               keyIndex=i + 1, inType='linear', outType='linear')
        else:
            op('keyframe.set_easing', comp=comp, layer=layer, property=prop,
               keyIndex=i + 1, inSpeed=0, outSpeed=0, inInfluence=80, outInfluence=15)
        if spatial:
            op('keyframe.set_spatial', comp=comp, layer=layer, property=prop,
               keyIndex=i + 1, continuous=True, autoBezier=True)


def build_layer(comp, n, ids):
    name = n['name']
    t = n['type']
    anchor = n.get('anchor', [0, 0])
    base = [100, 100]
    fx = 0

    def effect(match, display, props):
        nonlocal fx
        fx += 1
        op('effect.add', comp=comp, layer=name, matchName=match, name=display)
        for k, v in props.items():
            op('effect.set_property', comp=comp, layer=name, effectIndex=fx,
               property=[k], value=v)
        return fx

    # -------------------------------------------------------------- creación
    if t == 'text':
        op('layer.create_text', comp=comp, name=name, text=n['text'])
        op('text.reset_style', comp=comp, layer=name, scope='both')
        style = dict(font=FONTS[n['font']], fontSize=n['size'],
                     fillColor=rgb(n['color']), applyFill=True,
                     justification=n.get('align', 'center'), tracking=n['track'],
                     allCaps=False, fauxBold=False, fauxItalic=False,
                     horizontalScale=1, verticalScale=1)
        if n.get('textStroke'):
            col, wid = n['textStroke']
            style.update(applyStroke=True, strokeColor=rgb(col), strokeWidth=wid,
                         strokeOverFill=False)
        else:
            style['applyStroke'] = False
        op('text.set_style', comp=comp, layer=name, **style)
    elif t in ('video', 'audio', 'image'):
        op('layer.create_footage', comp=comp, name=name, sourceItemId=ids[n['asset']])
    elif t == 'comp':
        op('layer.create_footage', comp=comp, name=name, sourceItemId=ids[n['source']])
    elif t in ('ellipse', 'path', 'rect'):
        op('layer.create_shape', comp=comp, name=name)
        op('shape.add_group', comp=comp, layer=name, name='Geometría editable')
        if t == 'ellipse':
            op('shape.add_ellipse', comp=comp, layer=name, groupIndex=1,
               size=[n['w'], n['h']])
        elif t == 'rect':
            op('shape.add_rect', comp=comp, layer=name, groupIndex=1,
               size=[n['w'], n['h']], roundness=n.get('round', 0))
            anchor = [-n['w'] / 2, -n['h'] / 2]
        else:
            op('shape.add_path', comp=comp, layer=name, groupIndex=1,
               vertices=n['points'], closed=n.get('closed', False))
        if n.get('color'):
            op('shape.add_fill', comp=comp, layer=name, groupIndex=1,
               color=rgb(n['color']) + [1])
        if n.get('stroke'):
            op('shape.add_stroke', comp=comp, layer=name, groupIndex=1,
               color=rgb(n['stroke']) + [1], width=n.get('strokeWidth', 2))
    else:
        raise ValueError(t)

    # ------------------------------------------------------------ propiedades
    op('layer.set_props', comp=comp, layer=name, props={
        'motionBlur': True, 'threeDLayer': False,
        'inPoint': n['from'] / F, 'outPoint': max(n['from'] + 1, n['to']) / F,
        'enabled': n['to'] > n['from'],
        'label': 9 if t == 'text' else 13 if t in ('comp', 'video') else 5})
    if 'startTime' in n:
        op('layer.set_props', comp=comp, layer=name, props={
            'startTime': n['startTime'], 'inPoint': n['from'] / F,
            'outPoint': n['to'] / F})
    if t == 'video':
        op('layer.set_props', comp=comp, layer=name, props={'audioEnabled': False})

    scale = [a * b for a, b in zip(n.get('scale', [1, 1]), base)]
    op('transform.set', comp=comp, layer=name, position=n['pos'],
       anchorPoint=anchor, scale=scale, rotation=n.get('rot', 0),
       opacity=100 * n.get('opacity', 1))

    # --------------------------------------------------------------- efectos
    if n.get('shadow'):
        x, y, b, col, alpha = n['shadow']
        effect('ADBE Drop Shadow', 'Sombra suave', {
            'ADBE Drop Shadow-0001': rgb(col) + [1],
            'ADBE Drop Shadow-0002': 255 * alpha,
            'ADBE Drop Shadow-0003': math.degrees(math.atan2(x, -y)),
            'ADBE Drop Shadow-0004': math.hypot(x, y),
            'ADBE Drop Shadow-0005': 2 * b})

    a = n.get('anim', {})
    if 'blur' in a:
        idx = effect('ADBE Gaussian Blur 2', 'Suavidad y foco',
                     {'ADBE Gaussian Blur 2-0001': a['blur']['values'][0] * 2,
                      'ADBE Gaussian Blur 2-0003': 0})
        keys(comp, name, ['ADBE Effect Parade', idx, 'ADBE Gaussian Blur 2-0001'],
             a['blur']['frames'], [v * 2 for v in a['blur']['values']],
             a['blur']['ease'])

    if n.get('trim'):
        op('shape.add_trim_paths', comp=comp, layer=name, groupIndex=1, end=0)
        keys(comp, name, TRIM_END, n['trim'], [0, 100], 'out')

    # ---------------------------------------------------- claves de transformación
    for prop, k in a.items():
        if prop not in PP:
            continue
        vals = k['values']
        if prop == 'scale':
            vals = [[v[0] * base[0], v[1] * base[1]] for v in vals]
        elif prop == 'opacity':
            vals = [v * 100 for v in vals]
        keys(comp, name, PP[prop], k['frames'], vals, k['ease'],
             spatial=prop in ('pos', 'anchor'))


def main():
    with AE(log=R / 'analysis/ae-build.jsonl') as ae:
        # Solo se vacía si lo que hay en AE lo puso este script: un proyecto
        # guardado, o con elementos que no reconozco, no se toca.
        info = ae.call('ae_project_info')['result']
        mios = set(S['comps']) | {'Montaje-Creatina.mp4', 'Voz-Creatina.wav'}
        ajenos = [it.get('name') for it in info['items']
                  if it.get('name') not in mios]
        propio = str(R / 'ae/Creatina-BRAUDLABS.aep')
        if (info['file'] and info['file'] != propio) or ajenos:
            sys.exit(f'AE tiene trabajo que no es mío ({info["file"] or ajenos}): '
                     'no lo toco. Ciérralo o guárdalo y vuelve a lanzarlo.')

        # 1 · proyecto limpio y comps
        ae.batch([{'operation': 'project.clear', 'args': {}}])
        ae.batch([{'operation': 'comp.create', 'args': {
            'name': c['name'], 'width': c['width'], 'height': c['height'],
            'fps': F, 'duration': c['duration'] / F}} for c in S['comps'].values()])

        # 2 · medios, quedándonos con sus identificadores
        ids = {}
        for asset in ('Montaje-Creatina.mp4', 'Voz-Creatina.wav'):
            res = ae.call('ae_do', operation='project.import_file',
                          args={'path': str(R / 'assets' / asset), 'name': asset})
            item = res['result']
            ids[asset] = item.get('id') or item.get('itemId') or item['item']['id']
        listing = ae.call('ae_do', operation='item.list', args={})['result']
        for it in (listing if isinstance(listing, list) else listing.get('items', [])):
            if it.get('name') in S['comps']:
                ids[it['name']] = it['id']

        # 3 · obturador como el resto de la serie: 210°, fase -105°
        ae.batch([{'operation': 'comp.set_props', 'args': {
            'comp': name, 'props': {
                'motionBlur': True, 'shutterAngle': 210, 'shutterPhase': -105,
                'motionBlurSamplesPerFrame': 16,
                'motionBlurAdaptiveSampleLimit': 64,
                'resolutionFactor': [1, 1]}}} for name in S['comps']])

        # 4 · capas, comp por comp
        for name, c in S['comps'].items():
            global ops
            ops = []
            for n in c['layers']:
                build_layer(name, n, ids)
            ae.batch(ops)
            print(f'  {name:22} {len(c["layers"]):3} capas')

        ae.call('ae_save_project', path=str(R / 'ae/Creatina-BRAUDLABS.aep'))
        miss = ae.call('ae_do', operation='font.list_missing', args={})['result']
        print('fuentes que faltan:', miss)
        print('proyecto guardado en ae/Creatina-BRAUDLABS.aep')


if __name__ == '__main__':
    (R / 'ae').mkdir(exist_ok=True)
    main()
