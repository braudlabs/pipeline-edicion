"""Reconstruye el proyecto de After Effects de V8 reproduciendo sus operaciones.

El .aep se construyó enviando lotes de operaciones al puente local de AE, y cada
lote quedó guardado en `v*/ae/*.json`. La spec de diseño de V4 se quedó atrás
—pasos posteriores añadieron capas y cambiaron tiempos solo en AE—, así que la
fuente fiable es la secuencia de operaciones, no la spec.

Este script las vuelve a ejecutar en orden sobre un modelo de datos y emite
`src/design.json`, con los fotogramas clave ya normalizados a puntos de control
explícitos para que el intérprete de Remotion no tenga que deducir nada.
"""
from pathlib import Path
import json
import math
import re

R = Path(__file__).resolve().parents[1]
AD3 = R.parent
F = 48

# Orden cronológico real de los lotes (por fecha de los archivos).
BATCHES = [
    'v4/ae/init.json', 'v4/ae/media.json', 'v4/ae/build-static.json',
    'v4/ae/styleframes.json', 'v4/ae/build-animation.json', 'v4/ae/qa-frames.json',
    'v4/ae/refine.json', 'v4/ae/export-parts.json', 'v4/ae/hold-correction.json',
    'v4/ae/package.json',
    'v5/ae/create-exit.json', 'v5/ae/build-exit.json', 'v5/ae/package.json',
    'v6/ae/recolor.json', 'v6/ae/package.json',
    'v7/ae/patch.json', 'v7/ae/package.json', 'v8/ae/package.json',
]

IGNORE = {
    'project.new', 'project.open', 'project.reduce', 'project.set_settings',
    'property.list', 'render.set_output', 'render.add_to_queue', 'render.clear_queue',
    'render.list_templates', 'font.list_missing', 'footage.list_missing',
}

TRANSFORM = {
    'ADBE Position': 'position', 'ADBE Anchor Point': 'anchorPoint',
    'ADBE Scale': 'scale', 'ADBE Rotate Z': 'rotation',
    'ADBE Rotate X': 'rotateX', 'ADBE Rotate Y': 'rotateY',
    'ADBE Opacity': 'opacity',
}
TRIM_END = 'ADBE Vector Trim End'


class Layer(dict):
    pass


def new_layer(name, kind):
    return Layer(
        name=name, kind=kind, enabled=True, threeD=False, blend=None, parent=None,
        inPoint=0.0, outPoint=None, startTime=0.0, audioEnabled=True,
        timeRemapEnabled=False, motionBlur=False,
        transform={'position': [0, 0, 0], 'anchorPoint': [0, 0, 0], 'scale': [100, 100, 100],
                   'rotation': 0, 'rotateX': 0, 'rotateY': 0, 'opacity': 100},
        keys={}, expressions={}, effects=[], masks=[], shapes=[], text=None, source=None,
    )


class Project:
    def __init__(self):
        self.comps = {}
        self.items = {}          # id -> nombre
        self.next_id = 600       # los importados posteriores reciben ids nuevos

    # ------------------------------------------------------------- utilidades
    def cname(self, ref):
        """Las operaciones nombran la comp por nombre o por id de elemento."""
        if isinstance(ref, str) and ref in self.comps:
            return ref
        name = self.items.get(ref) if not isinstance(ref, str) else ref
        if name in self.comps:
            return name
        # Una comp renombrada conserva su id; se busca por el nombre original.
        raise KeyError(f'comp desconocida: {ref}')

    def comp(self, ref):
        return self.comps[self.cname(ref)]

    def layer(self, comp, name):
        for l in self.comp(comp)['layers']:
            if l['name'] == name:
                return l
        raise KeyError(f'{comp} / {name}')

    def item_name(self, ref):
        if isinstance(ref, str):
            return ref
        return self.items.get(ref, f'item:{ref}')

    # ------------------------------------------------------------ rutas de propiedad
    def prop_key(self, layer, path):
        if not path:
            return None
        if path[0] == 'ADBE Transform Group':
            return TRANSFORM.get(path[1])
        if path[0] == 'ADBE Time Remapping':
            return 'timeRemap'
        if path[0] == 'ADBE Effect Parade':
            ref = path[1]
            if isinstance(ref, str):                       # referencia por matchName
                idx = next((i + 1 for i, e in enumerate(layer['effects'])
                            if e['matchName'] == ref), None)
            else:
                idx = ref
            return f'effect:{idx}:{path[-1]}'
        if TRIM_END in path:
            return 'trimEnd'
        if path[0] == 'ADBE Root Vectors Group':
            return 'shape:' + '/'.join(str(p) for p in path[1:])
        return 'prop:' + '/'.join(str(p) for p in path)

    # ------------------------------------------------------------------ ops
    def run(self, op, a):
        if op in IGNORE:
            return
        fn = getattr(self, 'op_' + op.replace('.', '_'), None)
        if fn is None:
            raise NotImplementedError(op)
        fn(a)

    # -- proyecto ---------------------------------------------------------
    def op_project_import_file(self, a):
        self.next_id += 1
        self.items[self.next_id] = a.get('name') or Path(a['path']).name

    def op_footage_replace(self, a):
        pass                                    # solo cambia la ruta en disco

    # -- comps ------------------------------------------------------------
    def op_comp_create(self, a):
        self.comps[a['name']] = {
            'name': a['name'], 'width': a['width'], 'height': a['height'],
            'fps': a.get('fps', F), 'duration': a['duration'], 'layers': [],
        }

    def op_comp_duplicate(self, a):
        c = json.loads(json.dumps(self.comp(a['comp'])))
        c['name'] = a['newName']
        c['layers'] = [Layer(l) for l in c['layers']]
        self.comps[a['newName']] = c

    def op_comp_set_props(self, a):
        c = self.comp(a['comp'])
        p = a['props']
        if 'duration' in p:
            c['duration'] = p['duration']
        if 'name' in p and p['name'] != c['name']:
            old = c['name']
            self.comps.pop(old)
            c['name'] = p['name']
            self.comps[p['name']] = c
            # La comp conserva su id al renombrarse.
            for k, v in self.items.items():
                if v == old:
                    self.items[k] = p['name']

    # -- capas ------------------------------------------------------------
    def _add(self, comp, layer):
        c = self.comp(comp)
        c['layers'].insert(0, layer)                    # AE inserta arriba
        if layer['outPoint'] is None:
            layer['outPoint'] = c['duration']
        return layer

    def op_layer_create_text(self, a):
        l = new_layer(a['name'], 'text')
        l['text'] = {'content': a.get('text', '')}
        self._add(a['comp'], l)

    def op_layer_create_footage(self, a):
        l = new_layer(a['name'], 'footage')
        l['source'] = self.item_name(a['sourceItemId'])
        self._add(a['comp'], l)

    def op_layer_create_solid(self, a):
        l = new_layer(a['name'], 'solid')
        l['solid'] = {'color': a['color'], 'width': a['width'], 'height': a['height']}
        self._add(a['comp'], l)

    def op_layer_create_shape(self, a):
        self._add(a['comp'], new_layer(a['name'], 'shape'))

    def op_layer_create_null(self, a):
        self._add(a['comp'], new_layer(a['name'], 'null'))

    def op_layer_set_props(self, a):
        l = self.layer(a['comp'], a['layer'])
        props = a['props']
        # AE mantiene la duración al cambiar solo el punto de entrada: la capa se
        # desplaza en lugar de recortarse. Comprobado contra el volcado de V7.
        if 'inPoint' in props and 'outPoint' not in props and l['outPoint'] is not None:
            l['outPoint'] += props['inPoint'] - l['inPoint']
        for k, v in props.items():
            if k == 'threeDLayer':
                l['threeD'] = v
            elif k in ('inPoint', 'outPoint', 'startTime', 'enabled', 'audioEnabled',
                       'timeRemapEnabled', 'motionBlur'):
                l[k] = v

    def op_layer_set_parent(self, a):
        """AE conserva la transformación del hijo al emparentarlo.

        Al asignar un padre, AE reexpresa la posición, el giro y la escala del hijo
        en el espacio del padre para que no se mueva. Sin esto, la del padre se
        aplicaría dos veces.
        """
        child = self.layer(a['comp'], a['layer'])
        parent = self.layer(a['comp'], a['parentLayer'])
        child['parent'] = a['parentLayer']

        def at_zero(l, key, default):
            tr = l['keys'].get(key)
            if tr and tr['values']:
                return tr['values'][0]
            return l['transform'].get(key, default)

        ppos = at_zero(parent, 'position', [0, 0, 0])
        panc = at_zero(parent, 'anchorPoint', [0, 0, 0])
        pscl = at_zero(parent, 'scale', [100, 100, 100])
        prot = at_zero(parent, 'rotation', 0)
        # Traslación efectiva del padre en su origen; giro y escala se aplican aparte.
        off = [ppos[i] - panc[i] * pscl[i] / 100 for i in range(2)]
        if prot:
            raise NotImplementedError('padre con giro al emparentar')

        def unmap(p):
            return [(p[0] - off[0]) * 100 / pscl[0], (p[1] - off[1]) * 100 / pscl[1]] + list(p[2:])

        child['transform']['position'] = unmap(child['transform']['position'])
        tr = child['keys'].get('position')
        if tr:
            tr['values'] = [unmap(v) for v in tr['values']]
        cs = child['transform']['scale']
        child['transform']['scale'] = [cs[i] * 100 / pscl[i] for i in range(2)] + list(cs[2:])

    def op_layer_set_blend_mode(self, a):
        self.layer(a['comp'], a['layer'])['blend'] = a['mode']

    def op_layer_replace_source(self, a):
        self.layer(a['comp'], a['layer'])['source'] = self.item_name(a['item'])

    def op_layer_copy_to_comp(self, a):
        src = self.layer(a['comp'], a['layer'])
        self._add(a['targetComp'], Layer(json.loads(json.dumps(src))))

    # -- texto ------------------------------------------------------------
    def op_text_reset_style(self, a):
        self.layer(a['comp'], a['layer'])['text'].pop('style', None)

    def op_text_set_style(self, a):
        t = self.layer(a['comp'], a['layer'])['text']
        t.setdefault('style', {}).update(
            {k: v for k, v in a.items() if k not in ('comp', 'layer')})

    def op_text_set_content(self, a):
        self.layer(a['comp'], a['layer'])['text']['content'] = a['text']

    # -- formas -----------------------------------------------------------
    def op_shape_add_group(self, a):
        self.layer(a['comp'], a['layer'])['shapes'].append({'name': a.get('name'), 'items': []})

    def _group(self, a):
        return self.layer(a['comp'], a['layer'])['shapes'][a.get('groupIndex', 1) - 1]

    def op_shape_add_rect(self, a):
        self._group(a)['items'].append(
            {'k': 'rect', 'size': a['size'], 'roundness': a.get('roundness', 0)})

    def op_shape_add_ellipse(self, a):
        self._group(a)['items'].append({'k': 'ellipse', 'size': a['size']})

    def op_shape_add_path(self, a):
        self._group(a)['items'].append(
            {'k': 'path', 'vertices': a['vertices'], 'closed': a.get('closed', False),
             'inTangents': a.get('inTangents'), 'outTangents': a.get('outTangents')})

    def op_shape_add_fill(self, a):
        self._group(a)['items'].append({'k': 'fill', 'color': a['color']})

    def op_shape_add_stroke(self, a):
        self._group(a)['items'].append({'k': 'stroke', 'color': a['color'], 'width': a['width']})

    def op_shape_add_trim_paths(self, a):
        self._group(a)['items'].append({'k': 'trim', 'end': a.get('end', 100)})

    # -- transformaciones y propiedades -----------------------------------
    def op_transform_set(self, a):
        t = self.layer(a['comp'], a['layer'])['transform']
        for k in ('position', 'anchorPoint', 'scale', 'rotation', 'opacity'):
            if k in a and a[k] is not None:
                t[k] = a[k]

    def op_property_set(self, a):
        l = self.layer(a['comp'], a['layer'])
        key = self.prop_key(l, a['property'])
        if key in TRANSFORM.values():
            l['transform'][key] = a['value']
        elif key and key.startswith('effect:'):
            _, idx, prop = key.split(':', 2)
            l['effects'][int(idx) - 1]['props'][prop] = a['value']
        else:
            l.setdefault('static', {})[key] = a['value']

    # -- efectos y máscaras -----------------------------------------------
    def op_effect_add(self, a):
        self.layer(a['comp'], a['layer'])['effects'].append(
            {'matchName': a['matchName'], 'name': a.get('name'), 'props': {}})

    def op_effect_set_property(self, a):
        l = self.layer(a['comp'], a['layer'])
        l['effects'][a['effectIndex'] - 1]['props'][a['property'][-1]] = a['value']

    def op_mask_add(self, a):
        self.layer(a['comp'], a['layer'])['masks'].append({'name': a.get('name')})

    def op_mask_set_path(self, a):
        l = self.layer(a['comp'], a['layer'])
        while len(l['masks']) < a['maskIndex']:
            l['masks'].append({})
        l['masks'][a['maskIndex'] - 1].update(
            {'vertices': a['vertices'], 'inTangents': a.get('inTangents'),
             'outTangents': a.get('outTangents'), 'closed': a.get('closed', True)})

    # -- fotogramas clave --------------------------------------------------
    def _track(self, a):
        l = self.layer(a['comp'], a['layer'])
        key = self.prop_key(l, a['property'])
        return l, l['keys'].setdefault(key, {'times': [], 'values': [], 'keys': []}), key

    def op_keyframe_set_batch(self, a):
        """Reescribe tiempos y valores.

        AE conserva el suavizado de las claves que ya existían: reescribir una
        posición no deshace su curva. Solo se reinician las claves nuevas.
        """
        _, tr, _ = self._track(a)
        previous = tr['keys']
        tr['times'] = list(a['times'])
        tr['values'] = list(a['values'])
        default = {'inInf': 33.0, 'outInf': 33.0, 'inSpeed': 0.0, 'outSpeed': 0.0,
                   'inType': 'bezier', 'outType': 'bezier', 'spatial': False}
        keep = len(previous) == len(a['times'])
        tr['keys'] = [dict(previous[i]) if keep else dict(default)
                      for i in range(len(a['times']))]

    def op_keyframe_set_easing(self, a):
        _, tr, _ = self._track(a)
        k = tr['keys'][a['keyIndex'] - 1]
        k.update({'inInf': a['inInfluence'], 'outInf': a['outInfluence'],
                  'inSpeed': a['inSpeed'], 'outSpeed': a['outSpeed'],
                  'inType': 'bezier', 'outType': 'bezier'})

    def op_keyframe_set_spatial(self, a):
        _, tr, _ = self._track(a)
        k = tr['keys'][a['keyIndex'] - 1]
        k['spatial'] = bool(a.get('autoBezier') or a.get('continuous'))
        if a.get('inTangent') is not None:
            k['inTangent'] = a['inTangent']
            k['outTangent'] = a.get('outTangent')
            k['spatial'] = bool(a.get('autoBezier'))

    def op_keyframe_set_interpolation(self, a):
        _, tr, _ = self._track(a)
        k = tr['keys'][a['keyIndex'] - 1]
        k['inType'] = a.get('inType', k['inType'])
        k['outType'] = a.get('outType', k['outType'])

    def op_keyframe_remove(self, a):
        _, tr, _ = self._track(a)
        i = a['keyIndex'] - 1
        if i < len(tr['times']):
            for f in ('times', 'values', 'keys'):
                tr[f].pop(i)

    def op_keyframe_shift(self, a):
        _, tr, _ = self._track(a)
        tr['times'] = [t + a['offset'] for t in tr['times']]

    # -- expresiones -------------------------------------------------------
    def op_expression_set(self, a):
        l = self.layer(a['comp'], a['layer'])
        key = self.prop_key(l, a['property'])
        l['expressions'][key] = a['expression']


# --------------------------------------------------------------- reproducción
p = Project()
p.items = {v: k for k, v in json.load(open(AD3 / 'v4/ae/ids.json')).items()}
p.items[587] = '01B - Caja continua'          # comp creada en V5, antes de su uso

count = 0
for rel in BATCHES:
    for q in json.load(open(AD3 / rel)):
        if q.get('name') != 'ae_do':
            continue
        a = q['arguments']
        if a.get('operation') == 'batch.run':
            for o in a['args']['ops']:
                p.run(o['operation'], o.get('args', {}))
                count += 1
        else:
            p.run(a['operation'], a.get('args', {}))
            count += 1
print(f'{count} operaciones reproducidas, {len(p.comps)} comps')

MASTER = next(n for n in p.comps if n.startswith('AD3 -'))
for n in [c for c in p.comps if c.startswith(('EXPLORACION', 'QA'))]:
    del p.comps[n]

# ------------------------------------------------- normalización a fotogramas
def to_frames(t):
    return round(t * F, 4)


SPATIAL = {'position', 'anchorPoint'}


def normalize(l, comp_dur):
    out = {
        'name': l['name'], 'kind': l['kind'], 'enabled': l['enabled'],
        'threeD': l['threeD'], 'parent': l['parent'], 'blend': l['blend'],
        'in': to_frames(l['inPoint']),
        'out': to_frames(l['outPoint'] if l['outPoint'] is not None else comp_dur),
        'startTime': to_frames(l['startTime']),
        'transform': l['transform'], 'source': l['source'],
    }
    for k in ('text', 'shapes', 'effects', 'masks', 'solid'):
        if l.get(k):
            out[k] = l[k]

    anim = {}
    for key, tr in l['keys'].items():
        if not tr['times']:
            continue
        anim[key] = {
            'times': [to_frames(t) for t in tr['times']],
            'values': tr['values'],
            'keys': tr['keys'],
            'spatial': key in SPATIAL and any(k.get('spatial') for k in tr['keys']),
        }
    if anim:
        out['anim'] = anim

    # Las dos únicas expresiones del proyecto: congelar y remapear.
    for key, expr in l['expressions'].items():
        m = re.fullmatch(r'valueAtTime\(Math\.min\(time,\s*([\d.]+)/(\d+)\)\);?', expr.strip())
        if m:
            out.setdefault('holdAfter', {})[key] = round(float(m.group(1)))
            continue
        m = re.fullmatch(
            r'Math\.max\(([\d.]+)/(\d+),\s*time\s*\+\s*([\d.]+)/(\d+)\);?', expr.strip())
        if m and key == 'timeRemap':
            out['timeRemap'] = {'min': round(float(m.group(1))), 'offset': round(float(m.group(3)))}
            continue
        raise ValueError(f'expresión no reconocida en {l["name"]}: {expr}')
    return out


design = {'fps': F, 'master': MASTER, 'comps': {}}
for name, c in p.comps.items():
    design['comps'][name] = {
        'name': name, 'width': c['width'], 'height': c['height'],
        'duration': to_frames(c['duration']),
        # AE numera de arriba abajo; se emite de abajo arriba, que es el orden de dibujo.
        'layers': [normalize(l, c['duration']) for l in reversed(c['layers'])],
    }

# ------------------------------------------------------ recursos referenciados
# Los medios se enlazan en duro desde el paquete de V8: mismos archivos, sin copia.
SRC = AD3 / 'v8/output/Proyecto/After-Effects/Assets'
pub = R / 'public'
pub.mkdir(exist_ok=True)
SOUL = {'Soul - imagenes': 'imagenes-soul.png', 'Soul - videos': 'videos-soul.png',
        'Soul - avatares': 'avatares-soul.png', 'Soul - anuncios': 'anuncios-soul.png'}

assets = {}
for c in design['comps'].values():
    for l in c['layers']:
        s = l.get('source')
        if not s or s in design['comps'] or s in assets:
            continue
        f = SOUL.get(s, s)
        dst = pub / f
        if not dst.exists():
            import os
            os.link(SRC / f, dst)
        if f.endswith(('.jpg', '.png')):
            from PIL import Image
            w, h = Image.open(dst).size
            assets[s] = {'kind': 'image', 'file': f, 'width': w, 'height': h}
        elif f.endswith('.wav'):
            assets[s] = {'kind': 'audio', 'file': f}
        else:
            assets[s] = {'kind': 'video', 'file': f, 'width': 1080, 'height': 1920}
design['assets'] = assets

out = R / 'src/design.json'
out.write_text(json.dumps(design, ensure_ascii=False, indent=1))
print('recursos:', {k: v['kind'] for k, v in assets.items()})
print(f'{out.relative_to(R)}: {sum(len(c["layers"]) for c in design["comps"].values())} capas')
for n, c in design['comps'].items():
    print(f'  {n:28} {c["width"]}x{c["height"]} dur={c["duration"]:7} capas={len(c["layers"]):3}')
