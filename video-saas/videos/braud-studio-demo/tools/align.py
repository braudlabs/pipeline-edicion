"""Alinea el guion G03 con los tiempos de whisper (copia de trabajo fuera de iCloud).
Uso: python3 -I tools/align.py <guion.txt> <whisper-words.json> <carpeta-salida>
"""
import difflib, json, re, sys, unicodedata
from pathlib import Path

script_path, whisper_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
blocks = [b.strip() for b in script_path.read_text().split('\n\n') if b.strip()]

def norm(w):
    w = unicodedata.normalize('NFD', w.lower())
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', w)

wsegs = json.loads(whisper_path.read_text())['transcription']
heard = []
for s in wsegs:
    t = s['text'].strip()
    if not t or t.startswith('['):
        continue
    for part in t.split():
        heard.append({'w': part, 'n': norm(part), 'a': s['offsets']['from'] / 1000, 'b': s['offsets']['to'] / 1000})
heard = [h for h in heard if h['n']]
spoken = {'30': ['treinta', 'por', 'ciento']}
expanded = []
for h in heard:
    parts = spoken.get(h['n'])
    if not parts:
        expanded.append(h); continue
    step = (h['b'] - h['a']) / len(parts)
    for k, p in enumerate(parts):
        expanded.append({'w': p, 'n': p, 'a': h['a'] + step * k, 'b': h['a'] + step * (k + 1)})
heard = expanded

words = []
for bi, b in enumerate(blocks):
    for w in b.split():
        if norm(w):
            words.append({'block': bi + 1, 'text': w, 'n': norm(w)})
sm = difflib.SequenceMatcher(a=[w['n'] for w in words], b=[h['n'] for h in heard], autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            words[i1 + k]['a'], words[i1 + k]['b'] = heard[j1 + k]['a'], heard[j1 + k]['b']
    elif tag == 'replace' and j2 > j1:
        a, b = heard[j1]['a'], heard[j2 - 1]['b']; n = i2 - i1
        for k in range(n):
            words[i1 + k]['a'] = a + (b - a) * k / n; words[i1 + k]['b'] = a + (b - a) * (k + 1) / n
for i, w in enumerate(words):
    if 'a' not in w:
        prev = next((words[j]['b'] for j in range(i - 1, -1, -1) if 'b' in words[j]), 0)
        w['a'] = w['b'] = prev; w['missing'] = True
out_blocks = []
for bi, b in enumerate(blocks):
    ws = [w for w in words if w['block'] == bi + 1]
    out_blocks.append({'block': bi + 1, 'start': round(ws[0]['a'], 3), 'end': round(ws[-1]['b'], 3), 'text': b})
for w in words:
    w.pop('n'); w['a'] = round(w['a'], 3); w['b'] = round(w['b'], 3)
(out / 'words.json').write_text(json.dumps(words, ensure_ascii=False, indent=1))
(out / 'blocks.json').write_text(json.dumps(out_blocks, ensure_ascii=False, indent=1))
print(len(words), 'palabras;', sum(1 for w in words if w.get('missing')), 'sin tiempo;', len(out_blocks), 'bloques')
