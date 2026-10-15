"""Monta la copia del frontal de BRAUD Studio con el caso real «Ecommerce Andrómeda».

- Copia el frontal (public/ y server.mjs) de ~/Downloads/braud-studio-visual-main a ui/ sin tocar el original.
- Trae los medios reales de la producción (clon APFS; si no se puede, copia).
- Escribe ui/demo/state.json: marca BRAUD, la pieza con su guion, escenas, versiones, casting y locución reales.

Lo que es real y lo que es contenido de demo queda anotado en DATOS-DEMO.md.
Uso: python3 -I tools/build-state.py  (desde la carpeta del proyecto)
"""
import json, shutil, subprocess
from pathlib import Path

root = Path(__file__).resolve().parent.parent
ui = root / 'ui'
SRC_UI = Path.home() / 'Downloads/braud-studio-visual-main'
PROD = Path.home() / 'Desktop/El director/sistema-ale/cliente/creativos/2026-10-14-ecommerce-andromeda'
DAY = '2026-10-14T{}:00.000Z'

# 1 · Frontal
if not (ui / 'public').exists():
    shutil.copytree(SRC_UI / 'public', ui / 'public')
    shutil.copy2(SRC_UI / 'server.mjs', ui / 'server.mjs')
    shutil.copytree(SRC_UI / 'media', ui / 'media')  # referencias de diseño del laboratorio
server = (ui / 'server.mjs').read_text()
if "'.mp3'" not in server:  # el servidor original no sirve audio
    server = server.replace("'.mp4':'video/mp4',", "'.mp4':'video/mp4','.mp3':'audio/mpeg','.m4a':'audio/mp4',")
    (ui / 'server.mjs').write_text(server)
(ui / 'demo').mkdir(exist_ok=True)
media_dir = ui / 'media' / 'andromeda'
media_dir.mkdir(parents=True, exist_ok=True)

def bring(src_rel, name):
    src, dst = PROD / src_rel, media_dir / name
    if not dst.exists():
        if subprocess.run(['cp', '-c', str(src), str(dst)], capture_output=True).returncode:
            shutil.copy2(src, dst)  # también materializa archivos que solo están en iCloud
    return 'media/andromeda/' + name

def poster(video_name, at):
    out = media_dir / (Path(video_name).stem + '-poster.jpg')
    if not out.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', str(media_dir / video_name),
                        '-frames:v', '1', '-q:v', '3', str(out)], check=True)
    return 'media/andromeda/' + out.name

seed = json.loads((SRC_UI / 'demo/state.json').read_text())
assets = [a for a in seed['assets'] if a.get('category') == 'inspiration']  # laboratorio de diseño, se conserva

def image(aid, name, rel, category, model='Soul 2.0', approved=False, hour='15:10', **extra):
    assets.append({'id': aid, 'kind': 'image', 'name': name, 'category': category, 'approved': approved,
                   'model': model, 'file': bring(rel, aid + Path(rel).suffix), 'clientId': 'braud',
                   'pieceId': 'andromeda', 'createdAt': DAY.format(hour), **extra})

def video(aid, name, rel, duration, hour, at=1.5):
    f = bring(rel, aid + '.mp4')
    pid = aid + '-poster'
    assets.append({'id': pid, 'kind': 'image', 'name': name, 'category': 'still', 'approved': False,
                   'file': poster(aid + '.mp4', at), 'clientId': 'braud', 'pieceId': 'andromeda',
                   'createdAt': DAY.format(hour)})
    assets.append({'id': aid, 'kind': 'video', 'name': name, 'posterId': pid, 'duration': duration,
                   'model': 'Seedance 2.5', 'file': f, 'clientId': 'braud', 'pieceId': 'andromeda',
                   'createdAt': DAY.format(hour)})

# 2 · Casting: identidad aprobada y exploraciones del hook (Soul 2.0, 0,12 € estimados cada una)
image('ID-pareja', 'Hook elegido · identidad', 'hook-elegido/frame-elegido-usuario.png', 'character', approved=True,
      hour='15:40', castingSelected=True)
# La sudadera no aparece como material ni referencia: Ale la vetó el 15/10 («da pena»).
scenarios = [('almacen', 'Almacén', 13), ('lavanderia', 'Lavandería', 16), ('oficina', 'Oficina', 19),
             ('imprenta', 'Imprenta', 22), ('ascensor', 'Ascensor', 25), ('mercadillo', 'Mercadillo', 28)]
explorations = []
for slug, label, n in scenarios:
    for k, variant in enumerate('ABC'):
        aid = f'EX-{slug}-{variant}'
        image(aid, f'{label} · {variant}', f'{n + k:02d}_{slug}_{variant}_susurro/resultado.png', 'character',
              hour='15:0' + str(7 + k))
        explorations.append(aid)

# 3 · Escenas reales (Seedance 2.5) — tiempos del máster según ENTREGA_EDITOR y timeline
T1, T2, T3, T4 = 'tanda-01-directo-seedance', 'tanda-02-maquina', 'tanda-03-criterio', 'tanda-04-resto'
T5, T6 = 'tanda-05-reparaciones', 'tanda-06-cierre'
clips = {
    'V00a': ('Hook · v1', 'hook-video-v1/resultado.mp4', 6.05, '15:20'),
    'V00b': ('Hook · v2', 'hook-video-v2/resultado.mp4', 6.05, '15:45'),
    'V01': ('Ventanilla · v1', f'{T1}/01_ventanilla_espera/resultado.mp4', 10.05, '16:10'),
    'V02': ('Ticket · v1', f'{T1}/02_ticket_angulo/resultado.mp4', 5.05, '16:10'),
    'V03': ('Ads apagados · v1', f'{T1}/03_ads_apagados/resultado.mp4', 5.05, '16:10'),
    'V03b': ('Repetir · v1', f'{T1}/03b_repetir/resultado.mp4', 4.05, '16:30'),
    'V04': ('El giro · v1', f'{T1}/04_sudadera/resultado.mp4', 8.05, '16:10'),
    'V05': ('Presentación · v1', f'{T2}/05_presentacion/resultado.mp4', 4.05, '16:50'),
    'V06a': ('Cinco ads · v1', f'{T2}/06_cinco_ads/resultado.mp4', 4.05, '17:05'),
    'V06b': ('Cinco ads · v2', f'{T2}/06_cinco_ads_v2/resultado.mp4', 4.042, '17:20'),
    'V06c': ('Cinco ads · v4', f'{T5}/06_cinco_ads_v4/resultado.mp4', 4.042, '19:10'),
    'V06d': ('Cinco ads · v5', f'{T6}/06_cinco_ads_v5/resultado.mp4', 4.042, '20:10'),
    'V07a': ('Campañas · v2', f'{T6}/07_gestion_campanas_v2/resultado.mp4', 5.042, '20:15'),
    'V07b': ('Campañas · v3', f'{T6}/07_gestion_campanas_v3/resultado.mp4', 5.042, '20:20'),
    'V07c': ('Campañas · corte', f'{T6}/07_gestion_corte/resultado.mp4', 5.042, '20:27'),
    'V08a': ('Escalar · v2', f'{T6}/08_optimizacion_v2/resultado.mp4', 9.042, '20:20'),
    'V08b': ('Escalar · gag v3', f'{T6}/08_optimizacion_gag_v3/resultado.mp4', 9.042, '20:27'),
    'V09a': ('Doble basura · v1', f'{T3}/09_doble_basura/resultado.mp4', 5.042, '17:40'),
    'V09b': ('Doble basura · v2', f'{T5}/09_doble_basura_v2/resultado.mp4', 5.042, '19:15'),
    'V10': ('Fundadores · v1', f'{T4}/10_fundadores/resultado.mp4', 6.042, '18:20'),
    'V11': ('Criterio · v1', f'{T4}/11_criterio/resultado.mp4', 5.05, '18:20'),
    'V12a': ('Habitación · v1', f'{T4}/12_habitacion_creativos/resultado.mp4', 4.05, '18:25'),
    'V12b': ('Habitación · v3', f'{T6}/12_habitacion_v3/resultado.mp4', 4.042, '20:25'),
    'V13': ('Metagag · v1', f'{T4}/13_metagag/resultado.mp4', 5.05, '18:25'),
    'V14': ('CTA honesto · v1', f'{T4}/14_cta_honesto/resultado.mp4', 9.042, '18:30'),
    'V15a': ('Salida · v1', f'{T4}/15_salida/resultado.mp4', 4.042, '18:30'),
    'V15b': ('Salida · v2', f'{T5}/15_salida_v2/resultado.mp4', 4.042, '19:20'),
}
for aid, (name, rel, dur, hour) in clips.items():
    video(aid, name, rel, dur, hour, at=min(2.0, dur / 2))
assets.append({'id': 'AUD-narrador', 'kind': 'audio', 'name': 'Locución · Guillermo', 'duration': 85.394,
               'file': bring('voz/narrador-guillermo-original.mp3', 'AUD-narrador.mp3'),
               'clientId': 'braud', 'pieceId': 'andromeda', 'createdAt': DAY.format('14:30')})

lines = [
    ('Si eres dueño de un ecommerce ya sabes que con Andrómeda necesitas anuncios nuevos cada semana.', 0.12, 5.42),
    ('Y sabes que de la forma tradicional es la misma mierda de siempre: días y días para que el editor o una agencia te entregue las piezas.', 5.42, 14.58),
    ('Quieres testear un nuevo ángulo y necesitas semanas para ver el fruto de eso', 14.58, 18.75),
    ('y durante todo ese proceso ya se te han caído los ads antiguos', 18.75, 23.0),
    ('y venga a repetir otra puta vez.', 23.0, 25.42),
    ('No vengo a hablarte de tu problema, ya tienes suficiente con eso y con la sudadera de este tío. Vengo a hablarte de la solución.', 25.42, 32.58),
    ('Instalaremos en tu tienda esta maquinita;', 32.58, 35.0),
    ('le pedirás 5 ads para un concepto nuevo, te los dará,', 35.0, 38.33),
    ('luego le pedirás que los gestione en las campañas él mismo, te lo hará', 38.33, 42.58),
    ('y luego te dirá: «Hey, estos dos ángulos han funcionado espectacular, ¿quieres que te empiece a generar más versiones?» Y tú le dirás «Sí» y escalarás.', 42.58, 51.54),
    ('Pero eh, que si metes ideas de mierda sacarás el doble de mierda,', 51.54, 55.83),
    ('pero para eso están el melenas y el cabeza kiwi, que llevan haciendo estos ads con IA meses y meses', 55.83, 61.58),
    ('e instalarán en tu tienda el criterio que necesitas para hacer este tipo de ads,', 61.58, 66.04),
    ('para que no estés solo contra una máquina que te puede llenar la habitación de creativos.', 66.04, 70.04),
    ('Me olvidaba, este mismo ad lo ha hecho la maquinita de la que te hablo,', 70.04, 74.42),
    ('así que si la quieres: pincha abajo y reserva una llamada con nosotros. Veremos si tiene encaje para ti; si lo tiene, te lo diremos y si no, también.', 74.42, 82.96),
    ('Me voy que quiero seguir produciendo ads.', 82.96, 85.39),
]
script = [{'id': f'line-{i + 1}', 'text': t, 'start': a, 'end': b,
           'direction': 'Narrador cercano y seco; la voz entra de golpe.' if i == 0 else ''} for i, (t, a, b) in enumerate(lines)]

# (título, línea, dirección resumida del brief, versiones [(asset, etiqueta, estado)], seleccionada, src in/out)
# Referencias por escena con su uso explícito (roles que entiende Studio: identity, product, palette, setting).
image('REF-lavanderia', 'Lavandería azul y crema', '11_lavanderia_frame_v2/resultado.png', 'setting', hour='15:05')
assets.append({'id': 'REF-maquina', 'kind': 'image', 'name': 'La maquinita', 'category': 'product', 'approved': True,
               'file': 'media/andromeda/V05-poster.jpg', 'clientId': 'braud', 'pieceId': 'andromeda', 'createdAt': DAY.format('16:55')})
REF_ID = [{'assetId': 'ID-pareja', 'role': 'identity', 'confirmed': True},
          {'assetId': 'REF-lavanderia', 'role': 'setting', 'confirmed': True}]
REF_ALL = REF_ID + [{'assetId': 'REF-maquina', 'role': 'product', 'confirmed': True}]
scene_rows = [
    ('El susurro', 1, 'El azul susurra al oído del protagonista: «Más anuncios. Más.». Él, rígido de miedo, mira a cámara. Las fotos del fondo quietas; acercamiento final al miedo.',
     [('V00a', 'v1 · Movimiento falso de las cartas', 'rejected'), ('V00b', 'v2 · Susurro con lipsync', 'approved')], 'V00b', 0, 5.417),
    ('La ventanilla', 2, 'Entrega de carpeta, persiana que se cierra, banco con distintas posturas por corte y una pieza mínima. Los estados de espera son el remate a «días y días».',
     [('V01', 'v1 · Esperas por corte', 'approved')], 'V01', 0, 9.167),
    ('El ticket', 3, 'Pide un pequeño cambio y la máquina dispensa un ticket absurdamente largo que cae por gravedad. Llega la reacción del protagonista.',
     [('V02', 'v1 · Ticket infinito', 'approved')], 'V02', 0.5, 4.667),
    ('Ads apagados', 4, 'Tres pantallas se apagan mientras siguen esperando. El último apagado y la reacción del azul son el remate.',
     [('V03', 'v1 · Tres apagados', 'approved')], 'V03', 0, 4.25),
    ('Otra vez', 5, 'Otra bobina de ticket; el protagonista vuelve a mirar a cámara, harto.',
     [('V03b', 'v1 · Bobina nueva', 'approved')], 'V03b', 0, 2.417),
    ('El giro', 6, 'Empieza quieto para escuchar «No vengo a hablarte de tu problema». En «solución» se endereza y mira hacia donde estará la máquina.',
     [('V04', 'v1 · Hacia la solución', 'approved')], 'V04', 0, 7.167),
    ('La maquinita', 7, 'Coloca la máquina crema sobre el mostrador: pantalla negra inclinada, base crema, botón naranja, ratón y cable.',
     [('V05', 'v1 · Presentación', 'approved')], 'V05', 0, 2.417),
    ('Cinco ads', 8, 'Ambos protagonistas y la maquinita: la interfaz BRAUD solo dentro de la pantalla, reproductor grande y lista de cinco versiones de vídeo.',
     [('V06a', 'v1 · Miniaturas estáticas', 'rejected'), ('V06b', 'v2 · Demo sobre blanco', 'rejected'),
      ('V06c', 'v4 · Reparación de pantalla', 'review'), ('V06d', 'v5 · Cinco vídeos', 'approved')], 'V06d', 0, 3.333),
    ('A campañas', 9, 'Misma máquina e interfaz: los cinco anuncios pasan a campañas. Sin resultados numéricos inventados.',
     [('V07a', 'v2 · Campañas', 'review'), ('V07b', 'v3 · Campañas', 'review'), ('V07c', 'Corte · Campañas', 'approved')], 'V07c', 0, 4.25),
    ('Escalar', 10, '«Estos dos ángulos han funcionado espectacular»: demostración clara y control. Él dice que sí y escala.',
     [('V08a', 'v2 · Optimización', 'review'), ('V08b', 'v3 · Gag', 'approved')], 'V08b', 0, 8.958),
    ('Doble basura', 11, 'Borrador arrugado que el azul mete en una lavadora y vuelve duplicado; reacción seria. Metáfora de una mala idea.',
     [('V09a', 'v1 · Lavadora', 'review'), ('V09b', 'v2 · Lavadora', 'approved')], 'V09b', 0, 4.292),
    ('Los fundadores', 12, 'Melenas y cabeza kiwi, con sus referencias propias. Personas reales y criterio: bajar ruido, dar credibilidad.',
     [('V10', 'v1 · Fundadores', 'approved')], 'V10', 0, 5.75),
    ('El criterio', 13, 'Pausa de intensidad: credibilidad y claridad.',
     [('V11', 'v1 · Criterio', 'approved')], 'V11', 0, 4.458),
    ('La habitación', 14, 'No estar solo frente a la máquina: escalada visual con origen físico de cada salida.',
     [('V12a', 'v1 · Habitación', 'review'), ('V12b', 'v3 · Habitación', 'approved')], 'V12b', 0, 4.0),
    ('Este mismo ad', 15, '«Me olvidaba, este mismo ad…»: guiño metanarrativo.',
     [('V13', 'v1 · Metagag', 'approved')], 'V13', 0, 4.375),
    ('Reserva', 16, 'CTA claro, honesto y seguro: si encaja se dice y si no, también.',
     [('V14', 'v1 · CTA honesto', 'approved')], 'V14', 0, 8.542),
    ('Salida', 17, 'Salida con intención, sin cola muerta.',
     [('V15a', 'v1 · Salida', 'review'), ('V15b', 'v2 · Salida', 'approved')], 'V15b', 0, 2.433),
]
scenes, t = [], 0.0
for i, (title, line, intent, versions, sel, a, b) in enumerate(scene_rows):
    dur = round(b - a, 3)
    scenes.append({'id': f's{i + 1:02d}', 'title': title, 'lineId': f'line-{line}', 'intent': intent,
                   'duration': round(dur), 'audioMode': 'off', 'music': False, 'selectedId': sel,
                   'timeline': {'assetId': sel, 'start': round(t, 3), 'in': a, 'out': b, 'muted': False},
                   'refs': REF_ALL if i >= 6 else REF_ID,
                   'versions': [{'assetId': v, 'label': lab, 'status': st, 'feedback': ''} for v, lab, st in versions]})
    t += dur

piece = {
    'id': 'andromeda', 'title': 'Andrómeda pide más.', 'brand': 'BRAUD', 'format': '9:16',
    'brief': 'Anuncio para dueños de ecommerce que invierten en Meta. Un pequeño mundo absurdo con lógica física: el azul es la demanda insaciable de Meta; el protagonista, el dueño que pasa del miedo al control. Humor seco. CTA: reservar una llamada.',
    'kind': 'video', 'style': 'Fotografía práctica con textura de iPhone; azul, crema y morado.', 'audioMode': 'off',
    'mode': 'detailed', 'audioId': 'AUD-narrador', 'clientId': 'braud', 'createdAt': DAY.format('14:00'),
    'notes': [], 'chat': [], 'chatJobs': [], 'memoryRecords': [], 'activity': [],
    'agent': {'provider': 'codex', 'model': 'gpt-6-astra', 'effort': 'medium'}, 'primaryConversationId': 'chat-andromeda',
    'script': script, 'scenes': scenes,
    'intentBrief': {
        'goal': 'Que dueños de ecommerce reserven una llamada.',
        'audience': 'Dueños de ecommerce con producto propio que invierten en Meta.',
        'audienceAwareness': 'Saben que desde Andrómeda necesitan anuncios nuevos cada semana.',
        'audienceRelationship': 'Primer contacto con BRAUD.',
        'tension': 'Esperar días al editor o a la agencia mientras los anuncios se queman.',
        'offer': 'Instalar en su tienda un sistema que produce, gestiona y escala anuncios con IA.',
        'proof': 'Este mismo anuncio lo ha hecho el sistema.',
        'conceptTitle': 'La maquinita',
        'message': 'Puedes ir al ritmo de Meta sin depender de nadie.',
        'concept': 'Un pequeño mundo absurdo con lógica física reconocible. El azul es la demanda insaciable de Meta; el protagonista, el dueño del ecommerce.',
        'rationale': 'El humor seco hace reconocible la frustración y vuelve creíble la solución.',
        'cta': 'Reservar una llamada.', 'heroReferenceId': 'ID-pareja', 'selectedAngleId': 'angle-ritmo'},
    'creativeAngles': [
        {'id': 'angle-ritmo', 'title': 'El ritmo de Meta', 'motivation': 'Ritmo', 'concept': 'Meta pide anuncios nuevos cada semana y la producción va a ritmo de mes.', 'hypothesis': 'El dueño se reconoce en la presión semanal.'},
        {'id': 'angle-control', 'title': 'Depender de otros', 'motivation': 'Control', 'concept': 'Cada cambio pasa por el editor o la agencia.', 'hypothesis': 'Recuperar el control mueve más que ahorrar.'},
        {'id': 'angle-prueba', 'title': 'Lo hizo la máquina', 'motivation': 'Prueba', 'concept': 'El propio anuncio es la demostración.', 'hypothesis': 'Ver el resultado vence la objeción de calidad.'}],
    'castRoles': [
        {'id': 'azul', 'role': 'El azul', 'purpose': 'La demanda insaciable de Meta: invasivo y ridículo.',
         'description': 'Hombre calvo y sin cejas, completamente azul cobalto. Susurra al oído.',
         'candidates': [{'id': 'cand-' + a, 'assetId': a, 'status': 'shortlisted' if 'lavanderia' in a else 'exploring', 'note': ''} for a in explorations[:9]]},
        {'id': 'protagonista', 'role': 'El protagonista', 'purpose': 'El dueño del ecommerce: asustado, harto y, al final, al mando.',
         'description': 'Bigote daliniano y rigidez cómica.',
         'candidates': [{'id': 'cand-id', 'assetId': 'ID-pareja', 'status': 'shortlisted', 'note': 'Identidad elegida para todas las escenas.'}]}],
    'scriptOpenings': {
        'targetLineIds': ['line-1'], 'sourceLines': [dict(script[0])],
        'alternatives': [
            {'id': 'opening-1', 'title': 'El problema', 'hypothesis': 'Reconocimiento inmediato del ritmo de Meta.',
             'lines': [{'text': lines[0][0], 'direction': 'Directo, sin pausa de entrada.'}]},
            {'id': 'opening-2', 'title': 'La pregunta', 'hypothesis': 'Una tensión que el dueño mide cada semana.',
             'lines': [{'text': '¿Cuántos anuncios nuevos has subido esta semana? Andrómeda ya te está pidiendo más.', 'direction': 'Pregunta seca, mirando a cámara.'}]},
            {'id': 'opening-3', 'title': 'El contraste', 'hypothesis': 'Hacer visible el desfase de ritmos.',
             'lines': [{'text': 'Meta quiere anuncios nuevos cada semana. Tu editor te los da cada mes.', 'direction': 'Dos frases cortas, la segunda con resignación.'}]}],
        'selectedId': 'opening-1'},
}

client = dict(seed['clients'][0])
src = 'Guía comercial y landing de BRAUD'
ctx = lambda cid, kind, title, content, status='confirmed', source=src: {
    'id': cid, 'kind': kind, 'title': title, 'content': content, 'status': status, 'source': source,
    'createdAt': DAY.format('09:00'), 'updatedAt': DAY.format('09:00')}
client['context'] = [
    ctx('c-business', 'business', 'Instalación de IA creativa', 'Integramos la producción creativa con IA en el negocio en 8 semanas. No es una agencia: el sistema se queda en la tienda y lo pilota su equipo.'),
    ctx('c-objective', 'objective', 'Llamadas con dueños de ecommerce', 'Cada pieza de captación lleva a reservar una llamada; si hay encaje se dice, y si no, también.'),
    ctx('c-product', 'product', 'Qué incluye', 'Instalación con la marca del cliente, tres creativos iniciales, formación de quien lo va a dirigir y seguimiento en las semanas 4 y 8.'),
    ctx('c-audience', 'audience', 'Dueños de ecommerce en Meta', 'Producto propio e inversión en Meta. «Se me queman antes de poder reponerlos», «dependo de editores o agencias», «el cuello de botella soy yo».'),
    ctx('c-identity', 'identity', 'Identidad', '#367DFF · #101214 · #F1F4F8. Vidrio, luz suave y tipografía limpia.', source='Studio'),
    ctx('c-tone', 'tone', 'Voz', 'Tuteo, frases cortas y afirmativas. Humor seco con algún taco; seriedad al hablar de criterio.'),
    ctx('c-production', 'production', 'Cómo producimos', '9:16 para Meta. Fotografía práctica, textura de iPhone. Voz en off que entra de golpe y audio nativo de los clips.', source='Preferencias de producción'),
    ctx('c-learning', 'learning', 'Hook rate en nuestras cuentas', '50,7 % de media sobre 4 M de impresiones (lanzamiento, junio de 2026), frente al 25–35 % habitual en frío.', source='resultados.html · Administrador de anuncios'),
]

state = dict(seed)
state.update({
    'revision': 1, 'clients': [client] + seed['clients'][1:], 'pieces': [piece], 'assets': assets, 'jobs': [], 'events': [],
    'conversations': [{
        'id': 'chat-andromeda', 'clientId': 'braud', 'title': 'Andrómeda pide más.', 'createdAt': DAY.format('14:00'),
        'updatedAt': DAY.format('20:30'), 'pieceId': 'andromeda', 'pieceIds': ['andromeda'], 'selectedPieceId': 'andromeda',
        'agent': {'provider': 'codex', 'model': 'gpt-6-astra', 'effort': 'medium'}, 'jobs': [],
        'messages': [
            {'id': 'm1', 'role': 'user', 'at': DAY.format('14:00'),
             'text': 'Quiero un anuncio para dueños de ecommerce: desde Andrómeda necesitan anuncios nuevos cada semana. Humor seco, un mundo absurdo. Y que el propio anuncio demuestre que lo ha hecho el sistema.'},
            {'id': 'm2', 'role': 'assistant', 'at': DAY.format('14:02'),
             'text': 'Partamos de la presión semanal de Meta y de depender de otros para seguirla.\n\n**Concepto: la maquinita**\nUn pequeño mundo absurdo con lógica física. El azul es la demanda insaciable de Meta; el protagonista, el dueño del ecommerce, pasa del miedo al control.\n\nTe preparo la intención, tres aperturas y el reparto. Antes de generar, verás el coste de cada escena.'}]}],
    'projects': [{'id': 'proj-andromeda', 'clientId': 'braud', 'title': 'Captación ecommerce · octubre', 'pieceIds': ['andromeda'],
                  'createdAt': DAY.format('14:00'), 'updatedAt': DAY.format('20:30')}],
    'updatedAt': DAY.format('20:30'),
})
(ui / 'demo/state.json').write_text(json.dumps(state, ensure_ascii=False, indent=1))
print('assets', len(assets), 'scenes', len(scenes), 'montaje', round(t, 2), 's')
