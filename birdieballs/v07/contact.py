"""Inspect actual delivery frames, decoding the video just once."""
from pathlib import Path
from PIL import Image, ImageDraw
import subprocess, json

p = Path(__file__).parent
fps = 60000 / 1001
sets = {
    'hook-motion': [134, 135, 136, 138, 141, 145, 150, 156, 161, 163, 168, 178],
    'solution-motion': [558, 560, 561, 563, 566, 570, 578, 585, 594, 597],
    'continuity': [750, 756, 757, 760, 789, 793, 794, 801, 916, 954, 983, 990],
    'complete': [round(t * fps) for t in [1.4, 2.8, 3.5, 4.05, 4.6, 5.15, 6.4, 7.85, 8.3, 9.65, 10.98, 11.96, 12.60, 13.5, 14.6, 15.55, 16.55, 17.05, 18.95, 19.25, 20.25, 21.15, 22.2, 23.0, 23.8, 24.35, 25.4, 26.4, 27.7, 28.55, 29.3, 30.65, 31.5, 32.4, 33.2, 34.25, 34.8, 35.85, 36.45, 37.4]],
}
frames = sorted({f for batch in sets.values() for f in batch})
directory = p / 'stills' / 'native'
directory.mkdir(parents=True, exist_ok=True)
select = '+'.join(f'eq(n\\,{f})' for f in frames)
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p / 'Birdieballs-completo-V07.mp4'), '-vf', f'select={select},scale=432:768', '-fps_mode', 'vfr', '-q:v', '2', '-y', str(directory / '%04d.jpg')], check=True)
lookup = dict(zip(frames, sorted(directory.glob('*.jpg'))))
assert len(lookup) == len(frames)
for name, batch in sets.items():
    w, h, cols = 216, 384, 6 if name != 'solution-motion' else 5
    out = Image.new('RGB', (cols*w, ((len(batch)+cols-1)//cols)*(h+24)), '#14261c')
    draw = ImageDraw.Draw(out)
    for i, f in enumerate(batch):
        x, y = (i % cols)*w, (i // cols)*(h+24)
        with Image.open(lookup[f]) as im:
            out.paste(im.resize((w, h)), (x, y+24))
        draw.text((x+4, y+4), f'f{f} / {f/fps:.3f}s', fill='white')
    out.save(p/'stills'/f'final-{name}.jpg', quality=92)
    print(name, flush=True)
(p/'stills'/'native-frame-index.json').write_text(json.dumps({str(f):str(path.relative_to(p)) for f,path in lookup.items()}, indent=2))
