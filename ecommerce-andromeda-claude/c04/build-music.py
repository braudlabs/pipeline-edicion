#!/usr/bin/env python3
"""Pista de música de C04: la banda sonora conformada (../music/final_soundtrack_85_4s.wav) con
ducking bajo el narrador original. No toca el máster de música: escribe un stem aparte.

Nivel (pista de música a −17 LUFS; narrador a −18 LUFS):
  - con voz: −12 dB (la música queda ~11 LU por debajo de la frase);
  - en huecos de voz de 150 ms o más: −6 dB;
  - hook (0–5,417): −3 dB más, para que el susurro nativo se oiga limpio.
Ataque 80 ms con 60 ms de anticipación (la bajada empieza antes de la sílaba) y recuperación
de 300 ms, sin bombeo palabra a palabra (los huecos cortos no suben la música).

Uso: python3 build-music.py   → public/assets/audio/stems/musica.wav + study/music-duck.json
"""
from __future__ import annotations

import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SR = 48000
FRAMES = 2050
FPS = 24
N = FRAMES * SR // FPS  # 4.100.000 muestras = 85,416667 s (duración de la timeline)
MUSIC = HERE.parent / 'music' / 'final_soundtrack_85_4s.wav'
NARRATOR = Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/'
                '2026-10-14-ecommerce-andromeda/ENTREGA_EDITOR/02_AUDIO/NARRADOR_COMPLETO_ORIGINAL.mp3')
OUT = HERE / 'public' / 'assets' / 'audio' / 'stems' / 'musica.wav'
REPORT = HERE / 'study' / 'music-duck.json'

UNDER_DB, GAP_DB = -12.0, -6.0
HOOK_EXTRA_DB = -3.0
HOOK_END = 130 / FPS
VOICE_DB = -42.0  # umbral de presencia de voz (RMS 20 ms)
HOLD_S = 0.150  # huecos más cortos no levantan la música
LOOKAHEAD_S, ATTACK_S, RELEASE_S = 0.060, 0.080, 0.300
HOP = int(0.005 * SR)


def read_wav24(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        assert w.getsampwidth() == 3 and w.getframerate() == SR
        raw = w.readframes(w.getnframes())
        ch = w.getnchannels()
    b = np.frombuffer(raw, np.uint8).reshape(-1, 3).astype(np.int32)
    i = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
    i = np.where(i >= 1 << 23, i - (1 << 24), i)
    return (i / 8388607.0).reshape(-1, ch).astype(np.float64)


def write_wav24(path: Path, x: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    ints = (np.clip(x, -1, 1 - 1e-7) * 8388607).round().astype('<i4')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(ints.reshape(-1, 1).view(np.uint8).reshape(-1, 4)[:, :3].tobytes())


def main() -> int:
    music = read_wav24(MUSIC)
    if len(music) != 4_099_200:
        print(f'la banda sonora no mide 85,400 s ({len(music)} muestras)')
        return 1
    m = np.zeros((N, 2))
    m[:len(music)] = music
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(NARRATOR), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'])
    v = np.zeros(N)
    nv = np.frombuffer(raw, np.float32)[:N]
    v[:len(nv)] = nv
    # Presencia de voz por bloques de 5 ms (RMS de 20 ms centrado) con retención de huecos cortos.
    nb = N // HOP
    win = int(0.020 * SR)
    pad = np.pad(v, (win // 2, win))
    env = np.array([np.sqrt(np.mean(pad[k * HOP:k * HOP + win] ** 2)) for k in range(nb)])
    edb = 20 * np.log10(env + 1e-9)
    speak = edb > VOICE_DB
    hold = int(HOLD_S / 0.005)
    # Un hueco solo cuenta si dura ≥ HOLD_S: se rellenan los huecos cortos.
    k = 0
    while k < nb:
        if not speak[k]:
            j = k
            while j < nb and not speak[j]:
                j += 1
            if j - k < hold and k > 0 and j < nb:
                speak[k:j] = True
            k = j
        else:
            k += 1
    target = np.where(speak, UNDER_DB, GAP_DB)
    # Anticipación: el objetivo se adelanta para que la bajada empiece antes de la sílaba.
    la = int(LOOKAHEAD_S / 0.005)
    target = np.r_[target[la:], np.full(la, target[-1])]
    t_blocks = np.arange(nb) * HOP / SR
    target = target + np.where(t_blocks < HOOK_END, HOOK_EXTRA_DB, 0.0)
    # Suavizado de un polo: ataque al bajar, recuperación al subir.
    a_att = np.exp(-0.005 / ATTACK_S)
    a_rel = np.exp(-0.005 / RELEASE_S)
    g = np.empty(nb)
    cur = target[0]
    for k in range(nb):
        a = a_att if target[k] < cur else a_rel
        cur = a * cur + (1 - a) * target[k]
        g[k] = cur
    gain = 10 ** (np.interp(np.arange(N) / SR, t_blocks, g) / 20)
    out = m * gain[:, None]
    write_wav24(OUT, out)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    gaps = int(np.sum(np.diff(speak.astype(int)) == -1))
    REPORT.write_text(json.dumps({
        'music': str(MUSIC.relative_to(HERE.parent)), 'narrator': NARRATOR.name, 'samples': N,
        'under_voice_db': UNDER_DB, 'gaps_db': GAP_DB, 'hook_extra_db': HOOK_EXTRA_DB,
        'voice_threshold_dbfs': VOICE_DB, 'min_gap_s': HOLD_S, 'lookahead_s': LOOKAHEAD_S,
        'attack_s': ATTACK_S, 'release_s': RELEASE_S, 'voice_fraction': round(float(speak.mean()), 3),
        'gaps_counted': gaps, 'gain_db_range': [round(float(g.min()), 1), round(float(g.max()), 1)],
        'out': str(OUT.relative_to(HERE)),
    }, indent=2, ensure_ascii=False))
    print(REPORT.read_text())
    return 0


if __name__ == '__main__':
    sys.exit(main())
