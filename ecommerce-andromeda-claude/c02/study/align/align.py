"""Alineación forzada local (torchaudio MMS_FA) del guion corregido contra la voz real.

No es una transcripción independiente ni una escucha: ancla cada palabra del texto
corregido al audio original. Los tramos se acotan con la transcripción whisper.cpp
(study/asr/NARRADOR.json) para que una pausa larga no arrastre palabras.

Uso: /private/tmp/mercadillo-align311/bin/python study/align/align.py
"""
import json, os, re, subprocess, unicodedata
from pathlib import Path

os.environ.setdefault('TORCH_HOME', '/private/tmp/mercadillo-torch-cache')
import numpy as np
import torch
from torchaudio.pipelines import MMS_FA as bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SR = 16000

# (inicio, fin, texto mostrado). El texto mostrado conserva tildes/puntuación; el token
# de alineación se deriva de lo pronunciado (p. ej. «5» se pronuncia «cinco»).
NARRADOR = [
    (0.00, 5.30, 'Si eres dueño de un ecommerce ya sabes que con Andrómeda necesitas anuncios nuevos cada semana.'),
    (5.35, 9.70, 'Y sabes que de la forma tradicional es la misma mierda de siempre:'),
    (9.80, 14.40, 'días y días para que el editor o una agencia te entregue las piezas.'),
    (14.45, 18.45, 'Quieres testear un nuevo ángulo y necesitas semanas para ver el fruto de eso'),
    (18.55, 22.95, 'y durante todo ese proceso ya se te han caído los ads antiguos'),
    (22.95, 25.05, 'y venga a repetir otra puta vez.'),
    (25.20, 26.75, 'No vengo a hablarte de tu problema,'),
    (26.70, 28.33, 'ya tienes suficiente con eso'),
    (28.25, 30.45, 'y con la sudadera de este tío.'),
    (30.50, 32.40, 'Vengo a hablarte de la solución.'),
    (32.50, 34.80, 'Instalaremos en tu tienda esta maquinita;'),
    (34.90, 37.25, 'le pedirás 5 ads para un concepto nuevo,'),
    (37.15, 38.25, 'te los dará,'),
    (38.25, 41.60, 'luego le pedirás que los gestione en las campañas él mismo,'),
    (41.60, 42.32, 'te lo hará'),
    (42.25, 43.45, 'y luego te dirá:'),
    (43.30, 46.50, '«Hey, estos dos ángulos han funcionado espectacular,'),
    (46.50, 48.70, '¿quieres que te empiece a generar más versiones?»'),
    (48.65, 50.10, 'Y tú le dirás «Sí»'),
    (50.05, 51.40, 'y escalarás.'),
    (51.50, 55.65, 'Pero eh, que si metes ideas de mierda sacarás el doble de mierda,'),
    (55.60, 59.00, 'pero para eso están el melenas y el cabeza kiwi,'),
    (58.90, 61.95, 'que llevan haciendo estos ads con IA meses y meses'),
    (61.85, 65.85, 'e instalarán en tu tienda el criterio que necesitas para hacer este tipo de ads,'),
    (65.85, 70.05, 'para que no estés solo contra una máquina que te puede llenar la habitación de creativos.'),
    (70.25, 71.05, 'Me olvidaba,'),
    (71.25, 74.05, 'este mismo ad lo ha hecho la maquinita de la que te hablo,'),
    (74.15, 77.95, 'así que si la quieres: pincha abajo y reserva una llamada con nosotros.'),
    (78.20, 79.80, 'Veremos si tiene encaje para ti;'),
    (79.95, 81.45, 'si lo tiene, te lo diremos'),
    (81.45, 82.62, 'y si no, también.'),
    (82.55, 85.39, 'Me voy que quiero seguir produciendo ads.'),
]

SPOKEN = {'5': 'cinco', 'ia': 'ia', 'ecommerce': 'icomers', 'ads': 'ads', 'hey': 'ei'}


def token(word: str) -> str:
    w = unicodedata.normalize('NFKD', word.lower())
    w = ''.join(c for c in w if not unicodedata.combining(c))
    w = re.sub('[^a-z0-9]', '', w)
    return re.sub('[^a-z]', '', SPOKEN.get(w, w))


def load(path: Path, start: float = 0.0, dur: float | None = None) -> np.ndarray:
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start)] + (['-t', str(dur)] if dur else []) + [
        '-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-']
    return np.frombuffer(subprocess.check_output(cmd), np.float32).copy()


def align(audio: np.ndarray, segments, model, tokenizer, aligner):
    out = []
    for si, (begin, end, text) in enumerate(segments):
        words = text.split()
        toks = [token(w) for w in words]
        keep = [i for i, t in enumerate(toks) if t]
        chunk = audio[round(begin * SR):round(end * SR)]
        data = torch.from_numpy(chunk).unsqueeze(0)
        with torch.inference_mode():
            emission, _ = model(data)
        spans = aligner(emission[0], tokenizer([toks[i] for i in keep]))
        ratio = data.shape[-1] / emission.shape[1] / SR
        for i, ss in zip(keep, spans):
            out.append({
                'segment': si,
                'text': words[i],
                'start': round(begin + ss[0].start * ratio, 4),
                'end': round(begin + ss[-1].end * ratio, 4),
                'score': round(float(sum(s.score for s in ss) / len(ss)), 4),
            })
    return out


def main():
    torch.set_num_threads(6)
    model = bundle.get_model()
    tokenizer = bundle.get_tokenizer()
    aligner = bundle.get_aligner()
    narr = load(ROOT / 'public/assets/audio/NARRADOR_COMPLETO_ORIGINAL.mp3')
    words = align(narr, NARRADOR, model, tokenizer, aligner)
    (HERE / 'narrador-words.json').write_text(json.dumps({
        'method': 'torchaudio MMS_FA, guion corregido contra NARRADOR_COMPLETO_ORIGINAL.mp3; tramos acotados con whisper.cpp large-v3-turbo. No es escucha ni certificación fonética.',
        'segments': [{'start': b, 'end': e, 'text': t} for b, e, t in NARRADOR],
        'words': words,
    }, ensure_ascii=False, indent=1))
    hook = load(ROOT / 'study/native-audio/00_HOOK_visual_aprobado_audio_nativo_no_final.wav')
    hw = align(hook, [(1.2, 5.9, 'Más anuncios. Más.')], model, tokenizer, aligner)
    (HERE / 'hook-native-words.json').write_text(json.dumps({
        'method': 'MMS_FA sobre audio nativo del hook (voz generada sincronizada con la boca + ambiente). Orientativo.',
        'words': hw,
    }, ensure_ascii=False, indent=1))
    for w in hw:
        print('HOOK', w)
    low = [w for w in words if w['score'] < 0.35]
    print(len(words), 'palabras; puntuación baja:', [(w['text'], w['start'], w['score']) for w in low])


if __name__ == '__main__':
    main()
