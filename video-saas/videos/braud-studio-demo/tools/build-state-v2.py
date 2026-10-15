"""Estado del dashboard (V2, tras «se ve muy IA»): caso real «Creatina» del escaparate e-commerce,
más Sérum y Moda como otras piezas del estudio. Todo el material y los veredictos son de la
producción real (escaparate-web, 21/09/2026); la conversación y dos aperturas son texto de demo.

Copia el frontal a <W>/ui, trae los medios a <W>/ui/media/esc y escribe <W>/ui/demo/state.json.
Uso: python3 -I tools/build-state-v2.py   (W = carpeta padre de tools/)
"""
import json, shutil, subprocess
from pathlib import Path

W = Path(__file__).resolve().parent.parent
PROJECT = Path.home() / 'Documents/ChatGPT/editor/video-saas/videos/braud-studio-demo'
SRC_UI = PROJECT / 'ui'
ESC = Path.home() / 'Desktop/El director/sistema-ale/cliente/creativos/2026-09-21-escaparate-web'
ENT = W / 'escaparate/entrega'
FINAL_CREATINA = Path.home() / 'Documents/ChatGPT/editor/ad4-creatina/output/Creatina-BRAUDLABS-V1.mp4'
ui = W / 'ui'
DAY = '2026-09-21T{}:00.000Z'

if not (ui / 'public').exists():
    shutil.copytree(SRC_UI / 'public', ui / 'public', ignore=shutil.ignore_patterns('_frames', '_snaps'))
    shutil.copy2(SRC_UI / 'server.mjs', ui / 'server.mjs')
(ui / 'demo').mkdir(parents=True, exist_ok=True)
md = ui / 'media' / 'esc'
md.mkdir(parents=True, exist_ok=True)

def bring(src: Path, name: str):
    dst = md / name
    if not dst.exists():
        shutil.copy2(src, dst)
    return 'media/esc/' + name

def poster(video_name, at):
    out = md / (Path(video_name).stem + '-poster.jpg')
    if not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', str(md / video_name), '-frames:v', '1', '-q:v', '3', str(out)], check=True)
    return 'media/esc/' + out.name

def dur(p: Path):
    return round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                                      capture_output=True, text=True).stdout), 2)

assets = []
def image(aid, name, src, category, piece, approved=False, hour='10:00', **extra):
    assets.append({'id': aid, 'kind': 'image', 'name': name, 'category': category, 'approved': approved, 'model': 'Soul 2.0',
                   'file': bring(src, aid + src.suffix), 'clientId': 'braud', 'pieceId': piece, 'createdAt': DAY.format(hour), **extra})

def video(aid, name, src, piece, hour, at=1.5):
    f = bring(src, aid + '.mp4')
    pid = aid + '-poster'
    assets.append({'id': pid, 'kind': 'image', 'name': name, 'category': 'still', 'approved': False, 'file': poster(aid + '.mp4', at),
                   'clientId': 'braud', 'pieceId': piece, 'createdAt': DAY.format(hour)})
    assets.append({'id': aid, 'kind': 'video', 'name': name, 'posterId': pid, 'duration': dur(src), 'model': 'Seedance 2.5', 'file': f,
                   'clientId': 'braud', 'pieceId': piece, 'createdAt': DAY.format(hour)})

# ---------- Creatina (pieza 2 del escaparate) ----------
CR, FR = ENT / '02-creatina', ESC / 'frames/p2-suplementos'
image('CR-andrea', 'Andrea · identidad', CR / 'ancla.png', 'character', 'creatina', approved=True, hour='11:40', castingSelected=True)
image('CR-bote', 'Bote sin marca · packshot', FR / 'bote-r2-1.png', 'product', 'creatina', approved=True, hour='10:20')
for k in (1, 2, 3):
    image(f'CR-bote-x{k}', f'Packshot · descartado {k}', FR / f'bote-{k}.png', 'product', 'creatina', hour='10:05')
cand = [('r6-final', 'f', 'Cocina'), ('r6-final', 'g', 'Salón'), ('r5-encuadre', 'c', 'Cocina'), ('r3-normal', 'noche', 'Noche')]
cand_ids = []
for d, p, lab in cand:
    for k in (1, 2, 3):
        aid = f'CR-cand-{p}{k}'
        image(aid, f'{lab} · {k}', FR / d / f'{p}-{k}.png', 'character', 'creatina', hour='11:0' + str(k))
        cand_ids.append(aid)
video('CR-A', 'Hook · v2', CR / '01-A-hook.mp4', 'creatina', '12:30', 2.0)
video('CR-Ax', 'Hook · v1', CR / 'descartados/p2-A-parte1.mp4', 'creatina', '12:05', 2.0)
video('CR-B', 'Desarrollo · v2', CR / '02-B-desarrollo.mp4', 'creatina', '12:40', 4.0)
video('CR-Bx', 'Desarrollo · v1', CR / 'descartados/p2-B-parte2.mp4', 'creatina', '12:10', 4.0)
video('CR-M1', 'Macro polvo', CR / '04-macro-polvo.mp4', 'creatina', '13:00', 2.5)
video('CR-M2x', 'Macro agua', CR / 'descartados/p2-m2-agua.mp4', 'creatina', '13:05', 2.5)
video('CR-M3x', 'Macro agitar', CR / 'descartados/p2-m3-agitar.mp4', 'creatina', '13:10', 2.5)
video('CR-M4', 'Macro guardar', CR / '05-macro-guardar.mp4', 'creatina', '13:15', 3.0)
video('CR-C', 'Cierre · código', CR / '03-C-cierre.mp4', 'creatina', '12:50', 2.0)
if FINAL_CREATINA.exists():
    video('CR-final', 'Creatina · montaje', FINAL_CREATINA, 'creatina', '15:30', 3.0)

lines = [
    ('Llevo seis meses tomando creatina y lo que más me preguntáis es si hincha. A mí no me ha hinchado.', 0.0, 7.05),
    ('Lo que noté es que aguanto la última serie entera.', 7.05, 10.65),
    ('Cinco gramos con agua y ya está.', 10.65, 13.05),
    ('Tres euros la semana.', 13.6, 14.85),
    ('Así que nada, si quieres ponerte bien fuerte, usa mi código ANDREA10. Chao.', 14.85, 20.05),
]
script = [{'id': f'line-{i + 1}', 'text': t, 'start': a, 'end': b, 'direction': 'Natural, como un selfie; sin leer.' if i == 0 else ''}
          for i, (t, a, b) in enumerate(lines)]
REF = [{'assetId': 'CR-andrea', 'role': 'identity', 'confirmed': True}, {'assetId': 'CR-bote', 'role': 'product', 'confirmed': True}]
REF_P = [{'assetId': 'CR-bote', 'role': 'product', 'confirmed': True}]
rows = [
    ('El hook', 1, 'Plano continuo de selfie en la cocina: responde si hincha con el bote en la mano. Voz nativa en castellano.',
     [('CR-Ax', 'v1 · Cámara demasiado quieta', 'rejected', 'Cámara demasiado quieta. Sustituida.'), ('CR-A', 'v2 · Selfie vivo', 'approved', '')], 'CR-A', 0, 7.05, REF, 'native'),
    ('El scoop', 2, 'Posa el bote y saca el scoop. Continúa el plano del hook, encadenado por fotograma.',
     [('CR-Bx', 'v1 · Bote flotando', 'rejected', 'El bote se queda flotando sin que nadie lo sujete. Inservible.'), ('CR-B', 'v2 · Encadenado', 'approved', '')], 'CR-B', 0, 3.6, REF, 'native'),
    ('Macro · polvo', 3, 'Macro sin voz: el scoop vuelca el polvo en la batidora translúcida con marcas.',
     [('CR-M2x', 'Agua · otro recipiente', 'rejected', 'La batidora cambia de recipiente entre clips: vaso alto y cónico.'), ('CR-M1', 'Polvo · batidora', 'approved', '')], 'CR-M1', 0, 2.4, REF_P, 'off'),
    ('Macro · guardar', 4, 'Tapa el bote y lo posa con la etiqueta de frente. Sin batidora en plano.',
     [('CR-M3x', 'Agitar · botella negra', 'rejected', 'Otro recipiente: botella negra con tapa negra.'), ('CR-M4', 'Guardar · etiqueta', 'approved', '')], 'CR-M4', 0, 1.25, REF_P, 'off'),
    ('El código', 5, 'CTA mirando a cámara con el código ANDREA10; el código se rotula en edición.',
     [('CR-C', 'v1 · CTA', 'approved', '')], 'CR-C', 0, 5.2, REF, 'native'),
]
scenes, t = [], 0.0
for i, (title, line, intent, versions, sel, a, b, refs, audio) in enumerate(rows):
    d = round(b - a, 3)
    scenes.append({'id': f's{i + 1:02d}', 'title': title, 'lineId': f'line-{line}', 'intent': intent, 'duration': round(d), 'audioMode': audio,
                   'music': False, 'selectedId': sel, 'timeline': {'assetId': sel, 'start': round(t, 3), 'in': a, 'out': b, 'muted': audio == 'off'},
                   'refs': refs, 'versions': [{'assetId': v, 'label': lab, 'status': st, 'feedback': fb} for v, lab, st, fb in versions]})
    t += d

creatina = {
    'id': 'creatina', 'title': '¿La creatina hincha?', 'brand': 'BRAUD', 'format': '9:16',
    'brief': 'UGC hiperrealista para una tienda de suplementos: una clienta responde la pregunta que más le hacen, con el producto en la mano. Bote sin marca idéntico en todos los planos. CTA con código de descuento.',
    'kind': 'video', 'style': 'Selfie de móvil, luz de cocina real. Cero texto generado.', 'audioMode': 'native', 'mode': 'detailed',
    'audioId': None, 'clientId': 'braud', 'createdAt': DAY.format('10:00'), 'notes': [], 'chat': [], 'chatJobs': [], 'memoryRecords': [], 'activity': [],
    'agent': {'provider': 'codex', 'model': 'gpt-6-astra', 'effort': 'medium'}, 'primaryConversationId': 'chat-creatina',
    'script': script, 'scenes': scenes,
    'intentBrief': {
        'goal': 'Que quien duda de la creatina la pruebe con el código.', 'audience': 'Gente que entrena y duda si la creatina hincha.',
        'audienceAwareness': 'Conocen la creatina; les frena el miedo a hincharse.', 'audienceRelationship': 'Primer contacto con la tienda.',
        'tension': 'El miedo a hincharse.', 'offer': 'Creatina monohidrato: cinco gramos con agua, tres euros la semana.',
        'proof': 'Seis meses tomándola; aguanta la última serie entera.', 'conceptTitle': 'La pregunta que más me hacéis',
        'message': 'No hincha, y se nota en el entreno.', 'concept': 'Una clienta real responde en su cocina, como un selfie: sin decorado ni actor.',
        'rationale': 'Un testimonio creíble vence la objeción mejor que un claim.', 'cta': 'Código ANDREA10.', 'heroReferenceId': 'CR-andrea', 'selectedAngleId': 'angle-duda'},
    'creativeAngles': [
        {'id': 'angle-duda', 'title': 'La duda', 'motivation': 'Miedo', 'concept': '¿Hincha? La pregunta que más le hacen.', 'hypothesis': 'Nombrar la objeción para la scroll.'},
        {'id': 'angle-serie', 'title': 'La última serie', 'motivation': 'Resultado', 'concept': 'Lo que nota en el gimnasio.', 'hypothesis': 'El resultado concreto convence más que el producto.'},
        {'id': 'angle-precio', 'title': 'Tres euros', 'motivation': 'Precio', 'concept': 'Cinco gramos al día, tres euros la semana.', 'hypothesis': 'El coste semanal desactiva la duda.'}],
    'castRoles': [
        {'id': 'clienta', 'role': 'La clienta', 'purpose': 'Una voz creíble: entrena y responde sin vender.',
         'description': 'Treintañera, recogido alto, sudadera granate; luz de cocina por la tarde.',
         'candidates': [{'id': 'cand-' + a, 'assetId': a, 'status': 'exploring', 'note': ''} for a in cand_ids[:9]] +
                       [{'id': 'cand-andrea', 'assetId': 'CR-andrea', 'status': 'shortlisted', 'note': 'Identidad elegida para todos los planos.'}]},
        {'id': 'producto', 'role': 'El producto', 'purpose': 'Bote sin marca, idéntico plano a plano.', 'description': 'Bote negro con etiqueta crema, sin texto generado.',
         'candidates': [{'id': 'cand-bote', 'assetId': 'CR-bote', 'status': 'shortlisted', 'note': 'Limpio: sin letras deformadas.'}] +
                       [{'id': f'cand-bote-x{k}', 'assetId': f'CR-bote-x{k}', 'status': 'rejected', 'note': 'Texto deformado en la etiqueta.'} for k in (1, 2, 3)]}],
    'scriptOpenings': {
        'targetLineIds': ['line-1'], 'sourceLines': [dict(script[0])],
        'alternatives': [
            {'id': 'opening-1', 'title': 'La pregunta', 'hypothesis': 'La objeción en boca de quien la ha resuelto.', 'lines': [{'text': lines[0][0], 'direction': 'Directa, como un selfie.'}]},
            {'id': 'opening-2', 'title': 'El dato', 'hypothesis': 'Abrir con el coste semanal.', 'lines': [{'text': 'Tres euros a la semana. Eso es lo que me cuesta aguantar la última serie.', 'direction': 'Con el bote en la mano.'}]},
            {'id': 'opening-3', 'title': 'La confesión', 'hypothesis': 'Romper el miedo con humor.', 'lines': [{'text': 'Tenía miedo de hincharme con la creatina. Spoiler: no.', 'direction': 'Media sonrisa a cámara.'}]}],
        'selectedId': 'opening-1'},
}

# ---------- Sérum y Moda, otras piezas del estudio ----------
SE, MO = ENT / '01-cosmetica', ENT / '04-moda'
image('SE-ancla', 'Testimonial · identidad', SE / 'ancla.png', 'character', 'serum', approved=True, hour='09:40')
image('SE-frasco', 'Frasco de sérum', ESC / 'frames/p1-cosmetica/serum-2.png', 'product', 'serum', approved=True, hour='09:20')
video('SE-1', 'Testimonial · parte 1', SE / '01-A-parte1.mp4', 'serum', '10:10', 3.0)
video('SE-2', 'Testimonial · parte 2', SE / '02-B-parte2.mp4', 'serum', '10:20', 4.0)
moda = [('01-percha', 'En la percha'), ('02-persona1', 'Persona 1'), ('03-persona2', 'Persona 2'), ('04-persona3', 'Persona 3'),
        ('05-persona4', 'Persona 4'), ('06-persona5', 'Persona 5'), ('07-detalle', 'Detalle')]
for k, (f, n) in enumerate(moda):
    video(f'MO-{k}', n, MO / f'{f}.mp4', 'moda', f'14:{10 + k}', 2.0)

def simple_piece(pid, title, brief, clip_ids, texts, audio):
    sc, t0 = [], 0.0
    for i, cid in enumerate(clip_ids):
        dd = next(a['duration'] for a in assets if a['id'] == cid)
        sc.append({'id': f's{i + 1:02d}', 'title': texts[i][0], 'lineId': f'line-{i + 1}', 'intent': texts[i][1], 'duration': round(dd), 'audioMode': audio,
                   'music': False, 'selectedId': cid, 'timeline': {'assetId': cid, 'start': round(t0, 2), 'in': 0, 'out': dd, 'muted': False}, 'refs': [],
                   'versions': [{'assetId': cid, 'label': 'v1', 'status': 'approved', 'feedback': ''}]})
        t0 += dd
    return {'id': pid, 'title': title, 'brand': 'BRAUD', 'format': '9:16', 'brief': brief, 'kind': 'video', 'style': '', 'audioMode': audio, 'mode': 'detailed',
            'audioId': None, 'clientId': 'braud', 'createdAt': DAY.format('09:00'), 'notes': [], 'chat': [], 'chatJobs': [], 'memoryRecords': [], 'activity': [],
            'agent': {'provider': 'codex', 'model': 'gpt-6-astra', 'effort': 'medium'}, 'primaryConversationId': None,
            'script': [{'id': f'line-{i + 1}', 'text': texts[i][2], 'start': None, 'end': None, 'direction': ''} for i in range(len(clip_ids))], 'scenes': sc}

serum = simple_piece('serum', 'Lo único que cambié.', 'Testimonial de cosmética con voz nativa: piel tirante a media tarde y el sérum que lo resuelve.',
                     ['SE-1', 'SE-2'], [('Parte 1', 'Selfie en casa, luz de ventana.', 'A las seis de la tarde se me tiraba la piel todos los días.'),
                                        ('Parte 2', 'Cuentagotas hacia cámara.', 'Esto es lo único que cambié.')], 'native')
moda_p = simple_piece('moda', 'Una prenda, cinco personas.', 'La misma sudadera en cinco cuerpos distintos: consistencia de producto plano a plano.',
                      [f'MO-{k}' for k in range(7)], [(n, 'Misma prenda, misma luz.', '') for _, n in moda], 'none')

seed = json.loads((SRC_UI / 'demo/state.json').read_text())
state = dict(seed)
state.update({
    'revision': 1, 'pieces': [creatina, serum, moda_p], 'assets': assets + [a for a in seed['assets'] if a.get('category') == 'inspiration'],
    'jobs': [], 'events': [],
    'conversations': [{
        'id': 'chat-creatina', 'clientId': 'braud', 'title': '¿La creatina hincha?', 'createdAt': DAY.format('10:00'), 'updatedAt': DAY.format('15:30'),
        'pieceId': 'creatina', 'pieceIds': ['creatina'], 'selectedPieceId': 'creatina', 'agent': {'provider': 'codex', 'model': 'gpt-6-astra', 'effort': 'medium'}, 'jobs': [],
        'messages': [
            {'id': 'm1', 'role': 'user', 'at': DAY.format('10:00'),
             'text': 'Quiero un UGC para la creatina: una chica que responde si hincha, con el bote en la mano, y que cierre con su código de descuento.'},
            {'id': 'm2', 'role': 'assistant', 'at': DAY.format('10:02'),
             'text': 'Partimos de la objeción que más frena la compra: el miedo a hincharse.\n\n**Concepto: la pregunta que más me hacéis**\nUna clienta responde en su cocina, como un selfie. El bote, sin marca e idéntico en todos los planos.\n\nTe preparo la intención, tres aperturas y el casting. Antes de generar, verás el coste de cada escena.'}]}],
    'projects': [{'id': 'proj-escaparate', 'clientId': 'braud', 'title': 'Escaparate e-commerce', 'pieceIds': ['creatina', 'serum', 'moda'],
                  'createdAt': DAY.format('09:00'), 'updatedAt': DAY.format('15:30')}],
    'updatedAt': DAY.format('15:30'),
})
(ui / 'demo/state.json').write_text(json.dumps(state, ensure_ascii=False, indent=1))
print('assets', len(assets), '· escenas creatina', len(scenes), '· montaje', round(t, 2), 's')
