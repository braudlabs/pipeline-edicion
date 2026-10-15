"""Compila src/design.json a operaciones de After Effects y las despacha.

El .aep se construye entero desde la spec. Si hay que cambiar algo, se cambia
el diseño y se vuelve a ejecutar: AE no se toca a mano. Es la lección de AD3.
"""
from pathlib import Path
import json, math, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ae import AE                                   # noqa: E402

R = Path(__file__).resolve().parents[1]
S = json.load(open(R / 'src/design.json'))
F = S['fps']
AEP = R / 'ae/AD5-BRAUDLABS.aep'
ASSETS = ('Montaje.mov', 'Voz.wav')

FONTS = {'bold': 'Optima-Bold', 'medium': 'Optima-Regular',
         'cond': 'Optima-ExtraBlack'}
PP = {k: ['ADBE Transform Group', v] for k, v in {
    'pos': 'ADBE Position', 'anchor': 'ADBE Anchor Point', 'scale': 'ADBE Scale',
    'rot': 'ADBE Rotate Z', 'opacity': 'ADBE Opacity'}.items()}
TRIM_END   = ['ADBE Root Vectors Group', 1, 'ADBE Vectors Group',
              'ADBE Vector Filter - Trim', 'ADBE Vector Trim End']
TRIM_START = ['ADBE Root Vectors Group', 1, 'ADBE Vectors Group',
              'ADBE Vector Filter - Trim', 'ADBE Vector Trim Start']

def rgb(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]

ops = []
def op(_op, **args): ops.append({'operation': _op, 'args': args})

def keys(comp, layer, prop, frames, values, ease='out', spatial=False):
    """Curva de la serie: influencia 80 de entrada, 15 de salida."""
    op('keyframe.set_batch', comp=comp, layer=layer, property=prop,
       times=[fr/F for fr in frames], values=values)
    for i in range(len(frames)):
        if ease == 'linear':
            op('keyframe.set_interpolation', comp=comp, layer=layer, property=prop,
               keyIndex=i+1, inType='linear', outType='linear')
        else:
            op('keyframe.set_easing', comp=comp, layer=layer, property=prop,
               keyIndex=i+1, inSpeed=0, outSpeed=0, inInfluence=80, outInfluence=15)
        if spatial:
            op('keyframe.set_spatial', comp=comp, layer=layer, property=prop,
               keyIndex=i+1, continuous=True, autoBezier=True)

def build_layer(comp, n, ids):
    name, t = n['name'], n['type']
    anchor = n.get('anchor', [0,0]); base = [100,100]; fx = 0

    def effect(match, display, props):
        nonlocal fx
        fx += 1
        op('effect.add', comp=comp, layer=name, matchName=match, name=display)
        for k,v in props.items():
            op('effect.set_property', comp=comp, layer=name, effectIndex=fx,
               property=[k], value=v)
        return fx

    if t == 'text':
        op('layer.create_text', comp=comp, name=name, text=n['text'])
        op('text.reset_style', comp=comp, layer=name, scope='both')
        style = dict(font=FONTS[n['font']], fontSize=n['size'],
                     fillColor=rgb(n['color']), applyFill=True,
                     justification=n.get('align','center'), tracking=n['track'],
                     allCaps=False, fauxBold=False, fauxItalic=False,
                     horizontalScale=1, verticalScale=1)
        if n.get('textStroke'):
            col, wid = n['textStroke']
            style.update(applyStroke=True, strokeColor=rgb(col), strokeWidth=wid,
                         strokeOverFill=False)
        else:
            style['applyStroke'] = False
        op('text.set_style', comp=comp, layer=name, **style)
    elif t in ('video','audio','image'):
        op('layer.create_footage', comp=comp, name=name, sourceItemId=ids[n['asset']])
        # el ancla de un metraje va en su centro, no en la esquina
        if t in ('video','image') and 'anchor' not in n:
            anchor = [n.get('srcW', 1080)/2, n.get('srcH', 1920)/2]
    elif t in ('ellipse','path','rect'):
        op('layer.create_shape', comp=comp, name=name)
        op('shape.add_group', comp=comp, layer=name, name='Geometría editable')
        if t == 'ellipse':
            op('shape.add_ellipse', comp=comp, layer=name, groupIndex=1, size=[n['w'],n['h']])
        elif t == 'rect':
            op('shape.add_rect', comp=comp, layer=name, groupIndex=1,
               size=[n['w'],n['h']], roundness=n.get('round',0))
            anchor = [-n['w']/2, -n['h']/2]
        else:
            op('shape.add_path', comp=comp, layer=name, groupIndex=1,
               vertices=n['points'], closed=n.get('closed', False))
        if n.get('color'):
            op('shape.add_fill', comp=comp, layer=name, groupIndex=1,
               color=rgb(n['color'])+[1])
        if n.get('stroke'):
            op('shape.add_stroke', comp=comp, layer=name, groupIndex=1,
               color=rgb(n['stroke'])+[1], width=n.get('strokeWidth',2))
    else:
        raise ValueError(t)

    op('layer.set_props', comp=comp, layer=name, props={
        'motionBlur': True, 'threeDLayer': False,
        'inPoint': n['from']/F, 'outPoint': max(n['from']+1, n['to'])/F,
        'enabled': n['to'] > n['from'],
        'label': 9 if t=='text' else 13 if t in ('video',) else 5})
    if t == 'video':
        op('layer.set_props', comp=comp, layer=name, props={'audioEnabled': False})

    scale = [a*b for a,b in zip(n.get('scale',[1,1]), base)]
    op('transform.set', comp=comp, layer=name, position=n['pos'], anchorPoint=anchor,
       scale=scale, rotation=n.get('rot',0), opacity=100*n.get('opacity',1))

    if n.get('shadow'):
        x,y,b,col,alpha = n['shadow']
        effect('ADBE Drop Shadow', 'Sombra suave', {
            'ADBE Drop Shadow-0001': rgb(col)+[1],
            'ADBE Drop Shadow-0002': 255*alpha,
            'ADBE Drop Shadow-0003': math.degrees(math.atan2(x,-y)),
            'ADBE Drop Shadow-0004': math.hypot(x,y),
            'ADBE Drop Shadow-0005': 2*b})

    if n.get('trim'):
        a_, b_ = n['trim']
        op('shape.add_trim_paths', comp=comp, layer=name, groupIndex=1, end=0)
        if n.get('trimInvertido'):
            # la línea ya está dibujada y se borra: el principio alcanza al final
            op('property.set', comp=comp, layer=name, property=TRIM_END, value=100)
            keys(comp, name, TRIM_START, [a_, b_], [0, 100], 'out')
        else:
            keys(comp, name, TRIM_END, [a_, b_], [0, 100], 'out')

    a = n.get('anim', {})
    for prop, k in a.items():
        if prop not in PP: continue
        vals = k['values']
        if prop == 'scale':   vals = [[v[0]*base[0], v[1]*base[1]] for v in vals]
        elif prop == 'opacity': vals = [v*100 for v in vals]
        keys(comp, name, PP[prop], k['frames'], vals, k['ease'],
             spatial=prop in ('pos','anchor'))

def main():
    with AE(log=R/'analysis/ae-build.jsonl') as ae:
        info = ae.call('ae_project_info')['result']
        mios = set(S['comps']) | set(ASSETS)
        ajenos = [it.get('name') for it in info['items'] if it.get('name') not in mios]
        if (info['file'] and info['file'] != str(AEP)) or ajenos:
            sys.exit(f'AE tiene trabajo que no es mío ({info["file"] or ajenos}): no lo toco.')

        ae.batch([{'operation':'project.clear','args':{}}])
        ae.batch([{'operation':'comp.create','args':{
            'name': c['name'], 'width': c['width'], 'height': c['height'],
            'fps': F, 'duration': c['duration']/F}} for c in S['comps'].values()])

        ids = {}
        for asset in ASSETS:
            item = ae.call('ae_do', operation='project.import_file',
                           args={'path': str(R/'assets'/asset), 'name': asset})['result']
            ids[asset] = item.get('id') or item.get('itemId') or item['item']['id']

        ae.batch([{'operation':'comp.set_props','args':{'comp':name,'props':{
            'motionBlur': True, 'shutterAngle': 210, 'shutterPhase': -105,
            'motionBlurSamplesPerFrame': 16, 'motionBlurAdaptiveSampleLimit': 64,
            'resolutionFactor': [1,1]}}} for name in S['comps']])

        for name, c in S['comps'].items():
            global ops
            ops = []
            for n in c['layers']:
                build_layer(name, n, ids)
            # el emparentado va después: las capas deben existir
            for n in c['layers']:
                if n.get('parent'):
                    op('layer.set_parent', comp=name, layer=n['name'],
                       parentLayer=n['parent'], jump=False)
            # ...y AE recalcula la posición al emparentar para conservar el sitio
            # en pantalla. Mis coordenadas ya son relativas al padre: se reimponen.
            for n in c['layers']:
                if not n.get('parent'):
                    continue
                op('transform.set', comp=name, layer=n['name'], position=n['pos'])
                pk = n.get('anim', {}).get('pos')
                if pk:
                    keys(name, n['name'], PP['pos'], pk['frames'], pk['values'],
                         pk['ease'], spatial=True)
            ae.batch(ops)
            print(f'  {name:16} {len(c["layers"]):3} capas · {len(ops)} operaciones')

        ae.call('ae_save_project', path=str(AEP))
        miss = ae.call('ae_do', operation='font.list_missing', args={})['result']
        print('fuentes que faltan:', miss)
        print('guardado en', AEP.relative_to(R.parent))

main()
