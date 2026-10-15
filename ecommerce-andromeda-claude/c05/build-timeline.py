"""src/data/timeline.json de C04 a partir del MASTER_COMPLETO_24FPS.json de la entrega.

El JSON del director manda sobre el brief (hoy coinciden: fotogramas, archivos, IN/OUT y estado).
Aquí solo se traduce a lo que lee Remotion (VideoSpine, AudioTracks, verify.py):

- id        el de C01–C03 para 00–06 (los usan los stems native-<id>.wav) y el del máster para 07–15.
- masterId  id exacto del máster, para trazabilidad.
- status    estado del brief/máster, sin recortar.
- asset     ruta bajo public/ (assets/clips/...).
- dur, from fotogramas de 24 fps; OUT exclusivo; todo contiguo y sin huecos.
- srcIn     fotograma de 24 fps de la fuente (02: 0,5 s = 12 f; 15: 0,75 s = 18 f).

Comprueba: 17 unidades contiguas, 2050 f, IN múltiplo de 1/24 s, clip presente en public/.

Uso: python3 ecommerce-andromeda-claude/c04/build-timeline.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 24
MASTER = json.loads((HERE / 'source-notes/MASTER_COMPLETO_24FPS.json').read_text())

# (id de C04, rótulo). Mismo orden que el máster.
SCENES = [
    ('00_hook', 'Hook · susurro'),
    ('01_ventanilla', 'Ventanilla · espera'),
    ('02_ticket', 'Ticket · ángulo'),
    ('03_apagados', 'Ads apagados'),
    ('03b_repetir', 'Repetir'),
    ('04_sudadera', 'Sudadera · solución'),
    ('05_presentacion', 'Presentación máquina'),
    ('06_cinco_ads', 'Cinco ads · v5 (fila duplicada)'),
    ('07_gestion', 'Gestión · campañas v3'),
    ('08_optimizacion', 'Optimización · gag v3'),
    ('09_papeles', 'Papeles · idea de mierda'),
    ('10_fundadores', 'Fundadores'),
    ('11_criterio', 'Criterio'),
    ('12_habitacion', 'Habitación · creativos v3'),
    ('13_metagag', 'Metagag · este mismo ad'),
    ('14_cta', 'CTA honesto'),
    ('15_salida', 'Salida · pantalla encendida'),
]


def main():
    master = MASTER['scenes']
    assert len(master) == len(SCENES) == 17, (len(master), len(SCENES))
    scenes = []
    pos = 0
    for (sid, label), m in zip(SCENES, master):
        assert m['record_in_frame'] == pos, (sid, m['record_in_frame'], pos)
        dur = m['record_out_frame'] - m['record_in_frame']
        assert dur == m['duration_frames'], sid
        src_in = round(m['source_in'] * FPS)
        assert abs(src_in / FPS - m['source_in']) < 1e-9, (sid, m['source_in'])
        if 'source_in_frame' in m:
            assert m['source_in_frame'] == src_in, sid
        asset = 'assets/clips/' + Path(m['source']).name
        assert (HERE / 'public' / asset).is_file(), asset
        scenes.append({'id': sid, 'masterId': m['id'], 'label': label, 'status': m['status'], 'asset': asset, 'dur': dur, 'srcIn': src_in, 'from': pos})
        pos += dur
    assert pos == MASTER['planned_picture_frames'] == 2050, pos
    out = {
        'fps': FPS,
        'width': MASTER['width'],
        'height': MASTER['height'],
        'renderedFrames': pos,
        'narratorFrames': int(MASTER['narration_duration'] * FPS),
        'narratorSeconds': MASTER['narration_duration'],
        'master': 'source-notes/MASTER_COMPLETO_24FPS.json',
        'scenes': scenes,
    }
    (HERE / 'src/data/timeline.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for s in scenes:
        print(f"{s['id']:16s} from {s['from']:4d} dur {s['dur']:3d} srcIn {s['srcIn']:2d} {s['asset']}")
    print('total', pos, 'fotogramas')


if __name__ == '__main__':
    main()
