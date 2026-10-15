import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {COLORS} from '../Stage';
import {UI_H, UI_W} from '../UIPlane';
import {SF, UI_FONT} from '../lib/Fonts';
import {Shutter} from '../lib/Shutter';
import {at, clamp, ease, endOf, mix, prog, tween} from '../lib/motion';

// Bloque 1 · V03 (tras «el hook es una mierda»): metraje real del anuncio Andrómeda, nada dibujado.
// El susurro del azul (Meta) en primer plano → la cámara se aleja y el plano es una tesela en un muro
// de anuncios que se llena semana a semana → todo gris salvo la espera, a cámara lenta («ritmo de mes»)
// → el muro corre como un feed y se vuelve clónico → la tesela central gira y es Studio.
// Recortes a resolución nativa y siempre sin el estampado de la sudadera (veto de Ale).

const T = {
  desde: at(1, 'Desde'), andromeda: at(1, 'Andrómeda'), meta: at(1, 'Meta'), pide: at(1, 'pide'), creatividad: at(1, 'creatividad'),
  nueva: at(1, 'nueva'), cada: at(1, 'cada'), semana: at(1, 'semana'), semanaEnd: endOf(1, 'semana'),
  tu: at(1, 'Tu'), produccion: at(1, 'producción'), ritmo: at(1, 'ritmo'), mes: at(1, 'mes'),
  y: at(1, 'Y'), anuncios: at(1, 'anuncios'), parecen: at(1, 'parecen'), cada2: at(1, 'cada', 1), mas: at(1, 'más'),
};
export const FLIP0 = 8.62;
export const OPENING_END = 9.22; // «Esto es BRAUD Studio»
const PULL0 = T.cada - 0.08; // el primer plano pasa a ser una tesela
const PULL1 = PULL0 + 0.55;
const SLOW0 = 3.95, SLOW1 = 6.2; // «Tu producción va a ritmo de mes»

// ---------- muro de teselas reales ----------
const TILES = ['T00', 'T01', 'T02', 'T03', 'T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T11', 'T12', 'T13', 'T14', 'T16'];
const COLS = 7, ROWS = 4, TS = 250, GAP = 22, STEP = TS + GAP;
const GX = (1920 - (COLS * TS + (COLS - 1) * GAP)) / 2, GY = (1080 - (ROWS * TS + (ROWS - 1) * GAP)) / 2;
const slotRect = (c: number, r: number) => ({x: GX + c * STEP, y: GY + r * STEP, w: TS, h: TS});
const WHISPER = {c: 1, r: 1};
const WAIT = {c: 5, r: 2};
// orden de llegada: del susurro hacia fuera, acelerando (cada tesela = una semana)
const ORDER = Array.from({length: COLS * ROWS}, (_, i) => ({c: i % COLS, r: Math.floor(i / COLS)}))
  .filter((s) => !(s.c === WHISPER.c && s.r === WHISPER.r))
  .sort((a, b) => Math.hypot(a.c - WHISPER.c, a.r - WHISPER.r) - Math.hypot(b.c - WHISPER.c, b.r - WHISPER.r));
const arrival = (k: number) => PULL0 + 0.25 + 0.95 * (1 - Math.pow(1 - k / ORDER.length, 1.7)); // cada vez más deprisa

/** Cámara del muro: plano general → empuje a la espera → vuelta. */
const wallCam = (t: number) => {
  const toWait = prog(t, SLOW0, SLOW0 + 0.7, ease.inOut) * (1 - prog(t, SLOW1 - 0.05, SLOW1 + 0.25, ease.in));
  const w = slotRect(WAIT.c, WAIT.r);
  const s = mix(1, 2.7, toWait);
  // la espera queda a la derecha del cuadro; el texto de «ritmo de mes» ocupa la izquierda
  return {s, x: mix(0, 1290 - 960 + (960 - (w.x + TS / 2)) * s, toWait), y: mix(0, (540 - (w.y + TS / 2)) * s, toWait)};
};

const Chip: React.FC<{text: string; o: number; s?: number}> = ({text, o, s = 1}) => (
  <div style={{position: 'absolute', left: 12 * s, top: 12 * s, padding: `${4 * s}px ${10 * s}px`, borderRadius: 999, background: 'rgba(255,255,255,.92)',
    color: '#243448', font: `600 ${13 * s}px ${UI_FONT}`, opacity: o, boxShadow: '0 4px 12px rgba(0,0,0,.25)'}}>{text}</div>
);

const Wall: React.FC<{t: number}> = ({t}) => {
  if (t < PULL0 || t > SLOW1 + 0.3) return null;
  const cam = wallCam(t);
  const gray = prog(t, SLOW0 - 0.05, SLOW0 + 0.35);
  const back = prog(t, SLOW1 - 0.1, SLOW1 + 0.2);
  return (
    <div style={{position: 'absolute', inset: 0, transform: `translate(${cam.x}px, ${cam.y}px) scale(${cam.s})`, transformOrigin: '960px 540px',
      opacity: 1 - back}}>
      {ORDER.map((s, k) => {
        const ta = arrival(k);
        if (t < ta) return null;
        const a = prog(t, ta, ta + 0.18, ease.out);
        const r = slotRect(s.c, s.r);
        const isWait = s.c === WAIT.c && s.r === WAIT.r;
        const dim = isWait ? 0 : gray;
        return (
          <div key={k} style={{position: 'absolute', left: r.x, top: r.y, width: TS, height: TS, borderRadius: 18, overflow: 'hidden',
            transform: `scale(${mix(1.25, 1, a)})`, opacity: a * (1 - dim * 0.65), filter: dim > 0 ? `grayscale(${dim}) brightness(${1 - dim * 0.45})` : undefined,
            boxShadow: '0 20px 50px rgba(0,0,0,.5)'}}>
            {isWait ? (
              <OffthreadVideo src={staticFile('proxies/V01-hq.mp4')} muted playbackRate={0.35} startFrom={60}
                style={{width: TS, height: TS * 16 / 9, position: 'absolute', top: -TS * 0.12, objectFit: 'cover'}} />
            ) : <Img src={staticFile(`tiles/${TILES[k % TILES.length]}.jpg`)} style={{width: '100%', height: '100%'}} />}
            {isWait && t > SLOW0 ? (
              <div style={{position: 'absolute', left: 14, right: 14, bottom: 14, height: 5, borderRadius: 3, background: 'rgba(255,255,255,.35)'}}>
                <div style={{width: `${tween(t, SLOW0 + 0.3, SLOW1, 2, 11, ease.linear)}%`, height: '100%', borderRadius: 3, background: '#fff'}} />
              </div>
            ) : <Chip text={`Semana ${k + 2}`} o={a * (1 - gray)} />}
          </div>
        );
      })}
    </div>
  );
};

/** El susurro: primer plano grande que se encoge hasta su tesela del muro. */
const Whisper: React.FC<{t: number}> = ({t}) => {
  if (t > SLOW1 + 0.3) return null;
  const k = prog(t, PULL0, PULL1, ease.inOut);
  const reveal = prog(t, 0.02, 0.38, ease.out);
  const cam = wallCam(t);
  const big = {x: 150, y: 124, w: 900, h: 833};
  const slot = slotRect(WHISPER.c, WHISPER.r);
  const push = 1 + 0.05 * prog(t, 0, PULL0, ease.soft);
  const x = mix(big.x, slot.x, k), y = mix(big.y, slot.y, k), w = mix(big.w, TS, k), h = mix(big.h, TS, k);
  const gray = prog(t, SLOW0 - 0.05, SLOW0 + 0.35);
  // ventana del vídeo: de 1080×1000 (y 60–1060) al cuadrado superior; nunca baja hasta el estampado
  const vw = w, vh = w * 16 / 9, top = -mix(60 / 1080, 0.07, k) * vw;
  return (
    <div style={{position: 'absolute', inset: 0, transform: `translate(${cam.x}px, ${cam.y}px) scale(${cam.s})`, transformOrigin: '960px 540px',
      opacity: 1 - prog(t, SLOW1 - 0.1, SLOW1 + 0.2)}}>
      <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: mix(30, 18, k), overflow: 'hidden',
        clipPath: `inset(${(1 - reveal) * 50}% 0 ${(1 - reveal) * 50}% 0 round ${mix(30, 18, k)}px)`,
        transform: `scale(${push * mix(1, 1, k)})`, transformOrigin: '50% 50%',
        boxShadow: '0 60px 140px rgba(0,0,0,.7), 0 0 0 1px rgba(255,255,255,.12)',
        filter: gray > 0 ? `grayscale(${gray}) brightness(${1 - gray * 0.45})` : undefined, opacity: 1 - gray * 0.65}}>
        <OffthreadVideo src={staticFile('proxies/V00b-hq.mp4')} muted style={{position: 'absolute', left: 0, top, width: vw, height: vh, objectFit: 'cover'}} />
        <Chip text="Semana 1" o={prog(t, PULL1 - 0.1, PULL1 + 0.1) * (1 - gray)} />
      </div>
    </div>
  );
};

// ---------- feed que se vuelve clónico ----------
const Feed: React.FC<{t: number}> = ({t}) => {
  if (t < SLOW1 - 0.1 || t > OPENING_END) return null;
  const inK = prog(t, SLOW1 - 0.1, SLOW1 + 0.2, ease.out);
  const cols = 9, rows = 5, w = 200, gap = 20, h = w;
  const scroll = (t - SLOW1) * 1100 - prog(t, T.parecen, T.mas + 0.3, ease.out) * 520 * (t - T.parecen);
  const wave = (t - T.parecen + 0.05) / 0.85;
  const drain = prog(t, T.mas - 0.1, T.mas + 0.35);
  const flip = prog(t, FLIP0, OPENING_END, ease.inOut);
  const span = rows * (h + gap);
  return (
    <div style={{position: 'absolute', inset: 0, perspective: 1600, opacity: inK}}>
      <div style={{position: 'absolute', left: 960, top: 540, transformStyle: 'preserve-3d',
        transform: `translateZ(${mix(-240, 140, prog(t, T.parecen, OPENING_END, ease.in))}px) rotateX(${mix(16, 5, inK)}deg) rotateZ(-5deg)`}}>
        {Array.from({length: cols * rows}, (_, i) => {
          const c = i % cols - (cols - 1) / 2, r = Math.floor(i / cols) - (rows - 1) / 2;
          const yy = (((r * (h + gap) - scroll * (1 + (Math.abs(c) % 2) * 0.12)) % span) + span * 1.5) % span - span / 2;
          const d = Math.hypot(c * 0.9, yy / (h + gap));
          const clone = clamp(wave * 3 - d * 0.55);
          if (c === 0 && Math.abs(yy) < (h + gap) / 2 && flip > 0) return null; // la central gira aparte
          return (
            <div key={i} style={{position: 'absolute', left: c * (w + gap) - w / 2, top: yy - h / 2, width: w, height: h, borderRadius: 16, overflow: 'hidden',
              opacity: 1 - flip * 0.85, boxShadow: '0 18px 40px rgba(0,0,0,.5)', filter: drain > 0 ? `grayscale(${drain}) brightness(${1 - drain * 0.35})` : undefined}}>
              <Img src={staticFile(`tiles/${TILES[(i * 7) % TILES.length]}.jpg`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}} />
              {clone > 0 ? <Img src={staticFile('tiles/T08.jpg')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: clone}} /> : null}
            </div>
          );
        })}
      </div>
    </div>
  );
};

/** La tesela central gira 180° y su cara trasera es Studio, que crece hasta ocupar la ventana. */
const FlipToStudio: React.FC<{t: number}> = ({t}) => {
  if (t < FLIP0 || t > OPENING_END + 0.02) return null;
  const k = prog(t, FLIP0, OPENING_END, ease.inOut);
  const w = mix(200, UI_W * 0.95, ease.in(k)), h = mix(200, UI_H * 0.95, ease.in(k));
  const rot = k * 180;
  const back = rot > 90;
  return (
    <div style={{position: 'absolute', inset: 0, perspective: 1800}}>
      <div style={{position: 'absolute', left: 960 - w / 2, top: 540 - h / 2, width: w, height: h, transform: `rotateY(${back ? rot - 180 : rot}deg)`,
        borderRadius: mix(16, 26, k), overflow: 'hidden', boxShadow: '0 60px 140px rgba(0,0,0,.7)'}}>
        <Img src={staticFile(back ? 'snaps/home.png' : 'tiles/T08.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover',
          filter: back ? undefined : 'grayscale(1) brightness(.65)'}} />
      </div>
    </div>
  );
};

// ---------- tipografía cinética (palabra que golpea; la clave crece y lleva píldora) ----------
type KW = {text: string; t: number; size: number; weight?: number; color?: string; pill?: boolean; br?: boolean};
const KType: React.FC<{t: number; words: KW[]; out: number; x?: number; y?: number; align?: 'center' | 'left'; halo?: boolean}> = (
  {t, words, out, x, y = 0, align = 'center', halo = true}) => {
  if (t > out + 0.3 || t < words[0].t - 0.2) return null;
  const o = prog(t, out, out + 0.22, ease.in);
  return (
    <div style={{position: 'absolute', left: x ?? 0, right: x !== undefined ? undefined : 0, top: '50%', transform: `translateY(calc(-50% + ${y - o * 70}px))`,
      opacity: 1 - o, filter: `blur(${o * 14}px)`, textAlign: align, padding: x !== undefined ? 0 : '0 160px', fontFamily: SF, lineHeight: 0.98,
      letterSpacing: '-0.045em', isolation: 'isolate', whiteSpace: x !== undefined ? 'nowrap' : undefined}}>
      {halo ? <div style={{position: 'absolute', left: '50%', top: '50%', width: 1500, height: 640, transform: 'translate(-50%,-50%)', zIndex: -1,
        background: 'radial-gradient(closest-side, rgba(5,6,10,.82), rgba(5,6,10,.5) 55%, rgba(5,6,10,0))',
        opacity: prog(t, words[0].t - 0.15, words[0].t + 0.1)}} /> : null}
      {words.map((w, i) => {
        const k = prog(t, w.t - 0.06, w.t + 0.22, ease.out);
        const punch = 1 + 0.22 * (1 - prog(t, w.t - 0.02, w.t + 0.28, ease.out));
        return (
          <React.Fragment key={i}>
            {w.br ? <br /> : null}
            <span style={{display: 'inline-block', fontSize: w.size, fontWeight: w.weight ?? 700, color: w.pill ? '#fff' : w.color ?? COLORS.ink,
              opacity: k, transform: `translateY(${(1 - k) * 0.35 * w.size}px) scale(${t > w.t - 0.06 ? punch : 1})`, transformOrigin: align === 'left' ? '0% 60%' : '50% 60%',
              filter: `blur(${(1 - k) * 10}px)`, margin: align === 'left' ? `0 ${w.size * 0.18}px 0 0` : `0 ${w.size * 0.12}px`,
              textShadow: w.pill ? 'none' : `0 0 ${w.size * 0.4}px rgba(91,140,255,${0.35 * k})`}}>
              {w.pill ? <span style={{padding: '0 0.18em 0.04em', borderRadius: '0.16em', background: COLORS.accent,
                boxShadow: `0 0 ${w.size * 0.5}px rgba(91,140,255,.55)`}}>{w.text}</span> : w.text}
            </span>
          </React.Fragment>
        );
      })}
    </div>
  );
};

/** Barrido de luz vertical (T1) para cortar con energía. */
export const LightSweep: React.FC<{t: number; at: number; dur?: number; color?: string}> = ({t, at: a, dur = 0.32, color = COLORS.accent}) => {
  const k = (t - a) / dur;
  if (k < 0 || k > 1) return null;
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none'}}>
      {[0, 1, 2].map((j) => (
        <div key={j} style={{position: 'absolute', top: 0, bottom: 0, width: 60 + j * 90, left: mix(-300, 2100, ease.inOut(clamp(k * 1.1 - j * 0.08))),
          background: `linear-gradient(90deg, transparent, ${j === 1 ? '#b07cff' : color}, transparent)`, opacity: 0.55 - j * 0.12, filter: 'blur(18px)'}} />
      ))}
    </AbsoluteFill>
  );
};

const pullMoving = (t: number) => (t > PULL0 - 0.01 && t < PULL1 + 0.01) || (t > SLOW0 && t < SLOW0 + 0.7) || (t > SLOW1 - 0.05 && t < SLOW1 + 0.25);

export const Opening: React.FC<{t: number}> = ({t}) => {
  if (t > OPENING_END + 0.02) return null;
  const flash = (a: number, d = 0.12) => Math.max(0, 1 - Math.abs(t - a) / d);
  return (
    <AbsoluteFill>
      <Shutter moving={pullMoving} samples={6} render={(s) => (<><Wall t={s} /><Whisper t={s} /></>)} />
      <Feed t={t} />
      <FlipToStudio t={t} />
      {/* primer plano: texto a la derecha del susurro */}
      <KType t={t} out={T.meta - 0.12} x={1130} align="left" halo={false} words={[
        {text: 'Desde', t: T.desde, size: 58, weight: 500, color: COLORS.muted},
        {text: 'Andrómeda,', t: T.andromeda, size: 128, br: true},
      ]} />
      <KType t={t} out={PULL0 - 0.05} x={1130} align="left" halo={false} words={[
        {text: 'Meta', t: T.meta, size: 128, pill: true},
        {text: 'pide', t: T.pide + 0.04, size: 84, weight: 500, color: '#c5cbd6'},
        {text: 'creatividad', t: T.creatividad, size: 112, br: true},
        {text: 'nueva', t: T.nueva, size: 112, color: '#9db8ff', br: true},
      ]} />
      <KType t={t} out={SLOW0 - 0.12} y={0} words={[
        {text: 'cada', t: T.semana - 0.1, size: 96, weight: 500, color: COLORS.muted},
        {text: 'semana.', t: T.semana, size: 188},
      ]} />
      <KType t={t} out={SLOW1 - 0.12} x={150} align="left" halo={false} words={[
        {text: 'Tu producción', t: T.produccion, size: 60, weight: 500, color: COLORS.muted},
        {text: 'a ritmo de', t: T.ritmo - 0.1, size: 104, weight: 300, color: '#aab0ba', br: true},
        {text: 'mes.', t: T.mes, size: 104, weight: 300, color: '#aab0ba'},
      ]} />
      <KType t={t} out={FLIP0 - 0.05} words={[
        {text: 'se parecen', t: T.parecen, size: 80, weight: 500, color: COLORS.ink},
        {text: 'cada vez', t: T.cada2, size: 150, br: true},
        {text: 'más.', t: T.mas, size: 150, pill: true},
      ]} />
      <LightSweep t={t} at={0.0} dur={0.42} />
      <LightSweep t={t} at={SLOW1 - 0.08} dur={0.32} color="#ffffff" />
      <AbsoluteFill style={{background: '#fff', opacity: 0.45 * flash(SLOW1, 0.09) + 0.6 * flash(OPENING_END, 0.1), mixBlendMode: 'screen', pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};
