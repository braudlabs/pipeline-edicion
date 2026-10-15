import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {Cursor} from '../Cursor';
import {COLORS} from '../Stage';
import {UIPlane, UI_H, UI_W} from '../UIPlane';
import {Shutter} from '../lib/Shutter';
import {SF, UI_FONT} from '../lib/Fonts';
import {Cam, H, W, at, camMoving, clamp, ease, endOf, focus, mix, prog, track} from '../lib/motion';
import voiceEnv from '../data/voice-env.json';
import {LightSweep, OPENING_END} from './Opening';

// Bloques 2–5 (V02): logotipo que golpea y vuela a la interfaz, la idea como chispa que cae en el
// campo, abanico de clips reales con «Aprobado», zambullida al agente, tecleo seguido por la cámara,
// dictado con onda de la propia voz, envío disparado y la marca absorbida por el agente.

const T = {
  studio: at(2, 'Studio'), studioEnd: endOf(2, 'Studio'), cerebro: at(2, 'cerebro'), pones: at(2, 'pones'), idea: at(2, 'idea'),
  convierte: at(2, 'convierte'), anuncio: at(2, 'anuncio'), listo: at(2, 'listo'), publicar: at(2, 'publicar'),
  asi: at(3, 'Así'),
  cuentas: at(4, 'cuentas'), escrita: at(4, 'Escrita'), voz: at(4, 'voz'), como: at(4, 'Como'), chatgpt: at(4, 'ChatGPT'),
  studio5: at(5, 'Studio'), marca: at(5, 'marca'), productos: at(5, 'productos'), oferta: at(5, 'oferta'), quien: at(5, 'quién'),
  no: at(5, 'No'), cero: at(5, 'cero'), empieza: at(5, 'Empieza'), ti: at(5, 'ti'),
};
export const IDEA_START = OPENING_END;
export const IDEA_END = 31.0;

const HOME_PROMPT = {cx: 756, cy: 626, x: 449, y: 587};
const LOGO = {cx: 92, cy: 42};
const COMPOSER = {cx: 756, cy: 735};
const FIELD = {x: 384, y: 684, w: 744, h: 69};
const DICTATE = {x: 440, y: 762, w: 63, h: 31};
const SEND = {x: 1093, y: 760, w: 35, h: 35};
const USER_MSG = {cx: 812, cy: 240};
const WORKING = {x: 378, y: 303, w: 756, h: 32};
const REPLY = {x: 378, y: 300, w: 756, h: 175};

const DIVE = T.asi - 0.04;
const SWITCH = DIVE + 0.36;
const SENT = T.chatgpt + 0.06;

// Punto de la interfaz → cuadro (aproximación sin rotaciones, suficiente para lanzar objetos).
const toStage = (cam: Cam, x: number, y: number) => ({x: W / 2 + cam.x + cam.s * (x - UI_W / 2), y: H / 2 + cam.y + cam.s * (y - UI_H / 2)});

const homeCam = (t: number): Cam => track(t, [
  [IDEA_START, {s: 0.95}],
  [T.studioEnd + 0.15, {z: -60, rx: 5, ry: -5, s: 0.98}, ease.out],
  [T.cerebro + 0.05, {z: -40, rx: 6, ry: -7, rz: 0.6, s: 1.0}, ease.soft],
  [T.cerebro + 0.55, focus(HOME_PROMPT.cx, HOME_PROMPT.cy, 1.75, {rx: 3, ry: -3}), ease.inOut],
  [T.convierte - 0.05, focus(HOME_PROMPT.cx, HOME_PROMPT.cy, 1.85, {rx: 2, ry: -2}), ease.soft],
  [T.anuncio + 0.25, {x: -470, y: 20, z: -420, rx: 6, ry: -24, s: 0.92}, ease.inOut],
  [DIVE, {x: -490, y: 20, z: -440, rx: 6, ry: -26, s: 0.92}, ease.soft],
  [SWITCH, focus(HOME_PROMPT.cx, HOME_PROMPT.cy, 7.5), ease.in],
]);

// Composición: macro oblicuo que sigue al texto → plano general al dictar → latigazo hacia arriba al enviar.
const TYPE0 = T.cuentas - 0.05, TYPE1 = T.escrita - 0.1;
const DICT0 = T.voz - 0.12, DICT1 = T.chatgpt - 0.3;
const agentCam = (t: number): Cam => track(t, [
  [SWITCH - 0.06, focus(FIELD.x + 120, FIELD.y + 24, 7)],
  [SWITCH + 0.45, focus(FIELD.x + 160, FIELD.y + 24, 2.7, {rx: 4, ry: -14}), ease.out],
  [TYPE1, focus(FIELD.x + FIELD.w - 120, FIELD.y + 24, 2.75, {rx: 3, ry: -10}), ease.linear],
  [DICT0 + 0.15, focus(COMPOSER.cx, COMPOSER.cy, 1.9, {rx: 6, ry: 6}), ease.inOut],
  [SENT - 0.05, focus(COMPOSER.cx + 60, COMPOSER.cy, 2.05, {rx: 4, ry: 3}), ease.soft],
  [SENT + 0.42, focus(USER_MSG.cx, USER_MSG.cy, 1.9, {rx: -4, ry: -3}), ease.inOut],
  [T.marca - 0.2, focus(756, 300, 1.55, {rx: 3, ry: -6}), ease.inOut],
  [T.no, focus(756, 310, 1.6, {rx: 2, ry: -4}), ease.soft],
  [T.cero + 0.25, focus(560, 330, 2.1, {rx: 1, ry: -2}), ease.inOut],
  [T.empieza + 0.2, focus(756, 370, 1.62, {rx: 2, ry: -3}), ease.inOut],
  [IDEA_END, focus(756, 372, 1.7, {rx: 1, ry: -1.5}), ease.soft],
]);

// ---------- bloque 2 ----------
/** «braud® studio» golpea delante de la ventana y vuela a su sitio en la barra superior. */
const Wordmark: React.FC<{t: number}> = ({t}) => {
  const t0 = IDEA_START, fly0 = T.studioEnd - 0.02, fly1 = fly0 + 0.42;
  if (t < t0 || t > fly1 + 0.02) return null;
  const slam = prog(t, t0, t0 + 0.18, ease.out);
  const fly = prog(t, fly0, fly1, ease.inOut);
  const dest = toStage(homeCam(fly1), LOGO.cx, LOGO.cy);
  const s = mix(mix(1.5, 1, slam), 0.16, fly);
  const x = mix(W / 2, dest.x, fly), y = mix(H / 2, dest.y, fly);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${s})`, whiteSpace: 'nowrap', fontFamily: SF,
      opacity: Math.min(1, slam * 2) * (1 - prog(t, fly1 - 0.08, fly1)), filter: `blur(${(1 - slam) * 12}px)`}}>
      <span style={{fontSize: 200, fontWeight: 700, letterSpacing: '-0.05em', color: '#fff', textShadow: '0 0 80px rgba(91,140,255,.8)'}}>braud</span>
      <span style={{fontSize: 60, fontWeight: 700, color: '#fff', verticalAlign: '120%'}}>®</span>
      <span style={{fontSize: 110, fontWeight: 400, color: 'rgba(255,255,255,.75)', marginLeft: 40, letterSpacing: '-0.03em'}}>studio</span>
    </div>
  );
};

/** La idea es una chispa: aparece en la punta del cursor y cae dentro del campo. */
const Spark: React.FC<{x: number; y: number; r: number; o: number}> = ({x, y, r, o}) => (
  <div style={{position: 'absolute', left: x - r, top: y - r, width: r * 2, height: r * 2, opacity: o}}>
    <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: 'radial-gradient(circle, #fff 0%, #cfe0ff 22%, rgba(91,140,255,.65) 45%, rgba(91,140,255,0) 72%)'}} />
    <div style={{position: 'absolute', left: '50%', top: '8%', bottom: '8%', width: 2, marginLeft: -1, background: 'linear-gradient(transparent, #fff, transparent)'}} />
    <div style={{position: 'absolute', top: '50%', left: '8%', right: '8%', height: 2, marginTop: -1, background: 'linear-gradient(90deg, transparent, #fff, transparent)'}} />
  </div>
);

const FAN = ['V07b', 'V08b', 'V06d', 'V12a', 'V12b']; // en el centro la maquinita con la zapatilla (menos sudadera)
/** Abanico de clips reales que sale del campo; el central se aprueba con el chip real de Studio. */
const ClipFan: React.FC<{t: number}> = ({t}) => {
  const t0 = T.convierte - 0.02;
  if (t < t0 || t > SWITCH) return null;
  const origin = toStage(homeCam(t), HOME_PROMPT.cx, HOME_PROMPT.cy);
  const focusK = prog(t, T.listo - 0.05, T.listo + 0.35, ease.out);
  const out = prog(t, DIVE - 0.05, SWITCH, ease.in);
  return (
    <div style={{position: 'absolute', inset: 0, perspective: 2200}}>
      {FAN.map((id, i) => {
        const k = prog(t, t0 + i * 0.07, t0 + i * 0.07 + 0.6, ease.out);
        if (k <= 0) return null;
        const j = i - 2;
        const center = j === 0;
        const h = mix(70, center ? mix(600, 720, focusK) : mix(520, 470, focusK), k);
        const w = h * 9 / 16;
        const x = mix(origin.x, 1340 + j * 150, k) + out * (900 + j * 120);
        const y = mix(origin.y, 560 + Math.abs(j) * 34, k) - (center ? focusK * 20 : 0);
        const rz = j * 7 * k * (1 - focusK * 0.4), ry = mix(30, -8, k);
        const z = center ? 80 + focusK * 60 : -Math.abs(j) * 60;
        const dim = center ? 0 : focusK * 0.45;
        const chip = prog(t, T.publicar, T.publicar + 0.25, ease.out);
        return (
          <div key={id} style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, borderRadius: mix(8, 30, k), overflow: 'hidden',
            transform: `translateZ(${z}px) rotateY(${ry}deg) rotateZ(${rz}deg)`, zIndex: center ? 5 : 5 - Math.abs(j),
            boxShadow: center ? '0 60px 140px rgba(0,0,0,.7), 0 0 0 1px rgba(255,255,255,.18), 0 0 80px rgba(91,140,255,.25)' : '0 40px 90px rgba(0,0,0,.6)'}}>
            <OffthreadVideo src={staticFile(`proxies/${id}.mp4`)} muted style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '30% 50%'}} />
            <div style={{position: 'absolute', inset: 0, background: '#000', opacity: dim}} />
            {center && chip > 0 ? (
              <div style={{position: 'absolute', left: 22, top: 22, transform: `scale(${mix(0.6, 1, chip)})`, transformOrigin: '0 0', opacity: chip,
                padding: '7px 14px 7px 11px', borderRadius: 999, background: '#e5f3e9', color: '#2f7a4f', font: `600 21px ${UI_FONT}`,
                boxShadow: '0 6px 18px rgba(0,0,0,.25)'}}>✓ Aprobado</div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

// ---------- bloque 4 ----------
const IDEA_TYPED = 'Quiero un anuncio para dueños de ecommerce: desde Andrómeda necesitan anuncios nuevos cada semana.';
const IDEA_SPOKEN = ' Humor seco, un mundo absurdo. Y que el propio anuncio demuestre que lo ha hecho el sistema.';
const Composer: React.FC<{t: number}> = ({t}) => {
  const n = Math.floor(IDEA_TYPED.length * clamp((t - TYPE0) / (TYPE1 - TYPE0)));
  const words = IDEA_SPOKEN.split(/(?<= )/);
  const wk = clamp((t - (DICT0 + 0.2)) / (DICT1 - DICT0 - 0.2)) * words.length;
  const lift = prog(t, SENT, SENT + 0.32, ease.in);
  const caretOn = t < SENT && Math.floor(t * 2.4) % 2 === 0;
  return (
    <div style={{position: 'absolute', left: FIELD.x + 14, top: FIELD.y + 12, width: FIELD.w - 28, font: `14px/22.4px ${UI_FONT}`, color: COLORS.uiInk,
      opacity: 1 - lift, transform: `translateY(${-lift * 220}px)`, filter: `blur(${lift * 6}px)`}}>
      {IDEA_TYPED.slice(0, n)}
      {words.map((w, i) => (wk > i ? <span key={i} style={{opacity: clamp(wk - i), color: wk - i < 1 ? COLORS.accent : COLORS.uiInk}}>{w}</span> : null))}
      <span style={{display: 'inline-block', width: 1.5, height: 17, marginLeft: 1, verticalAlign: '-3px', background: COLORS.uiInk, opacity: caretOn && t > TYPE0 - 0.4 ? 1 : 0}} />
    </div>
  );
};

/** Onda de dictado: barras que siguen la envolvente real de la locución. */
const Waveform: React.FC<{t: number}> = ({t}) => {
  if (t < DICT0 || t > DICT1 + 0.35) return null;
  const on = prog(t, DICT0, DICT0 + 0.2, ease.out) * (1 - prog(t, DICT1, DICT1 + 0.35));
  const env = voiceEnv as number[];
  const bars = 46, x0 = DICTATE.x + DICTATE.w + 120, x1 = SEND.x - 30, cy = DICTATE.y + DICTATE.h / 2;
  return (
    <>
      <div style={{position: 'absolute', left: DICTATE.x - 3, top: DICTATE.y - 3, width: DICTATE.w + 6, height: DICTATE.h + 6, borderRadius: 18,
        boxShadow: `0 0 0 2px ${COLORS.accent}, 0 0 ${18 + 10 * Math.sin(t * 12)}px ${COLORS.accent}`, opacity: on}} />
      {Array.from({length: bars}, (_, i) => {
        const v = env[Math.max(0, Math.round((t - (bars - i) * 0.012) * 60))] ?? 0;
        const h = 3 + v * 26 * on;
        return <div key={i} style={{position: 'absolute', left: mix(x0, x1, i / (bars - 1)) - 1.5, top: cy - h / 2, width: 3, height: h, borderRadius: 2,
          background: COLORS.accent, opacity: on * (0.35 + 0.65 * (i / bars))}} />;
      })}
    </>
  );
};

// ---------- bloque 5 ----------
const BRAND_CARDS = [
  {img: 'marca-tarjetas-business', w: 862, h: 485, s: 0.82, t0: T.marca - 0.12, from: [-200, -700], to: [250, 90], rz: -6},
  {img: 'marca-tarjetas-product', w: 1200, h: 589, s: 0.66, t0: T.productos - 0.08, from: [1400, -700], to: [820, 150], rz: 5},
  {img: 'marca-tarjetas-audience', w: 1200, h: 344, s: 0.66, t0: T.quien - 0.12, from: [200, 1300], to: [360, 640], rz: -4},
  {img: 'marca-tarjetas-learning', w: 1200, h: 320, s: 0.62, t0: T.quien + 0.32, from: [1500, 1250], to: [930, 700], rz: 4},
];
const VORTEX0 = T.no - 0.05, VORTEX1 = T.cero + 0.3;
const BrandStorm: React.FC<{t: number; cam: Cam}> = ({t, cam}) => {
  if (t < BRAND_CARDS[0].t0 || t > VORTEX1 + 0.05) return null;
  const orb = toStage(cam, WORKING.x + 14, WORKING.y + 16);
  const v = prog(t, VORTEX0, VORTEX1, ease.in);
  return (
    <div style={{position: 'absolute', inset: 0, perspective: 1800}}>
      {BRAND_CARDS.map((c, i) => {
        if (t < c.t0) return null;
        const k = prog(t, c.t0, c.t0 + 0.42, ease.out);
        const w = c.w * c.s, h = c.h * c.s;
        const bx = mix(c.from[0], c.to[0], k), by = mix(c.from[1], c.to[1], k);
        // espiral hacia el orbe
        const ang = v * (2.4 + i * 0.4), rad = 1 - v;
        const cx = mix(bx + w / 2, orb.x, v) + Math.cos(ang + i) * 160 * v * rad;
        const cy = mix(by + h / 2, orb.y, v) + Math.sin(ang + i) * 110 * v * rad;
        return (
          <div key={c.img} style={{position: 'absolute', left: cx - w / 2, top: cy - h / 2, width: w, height: h, borderRadius: 18, overflow: 'hidden',
            transform: `rotateZ(${c.rz * (1 - k) * 3 + c.rz + v * 140}deg) rotateY(${(1 - k) * 25}deg) scale(${mix(1, 0.04, v)})`, opacity: 1 - v * 0.7,
            boxShadow: '0 40px 90px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.25)', filter: `blur(${v * 4}px)`}}>
            <Img src={staticFile(`snaps/${c.img}.png`)} style={{width: '100%', height: '100%'}} />
          </div>
        );
      })}
    </div>
  );
};

/** Orbe de «pensando»: late con cada tarjeta y estalla al tragarse la marca. */
const Orb: React.FC<{t: number}> = ({t}) => {
  if (t < SENT + 0.3 || t > T.empieza + 0.1) return null;
  const hits = BRAND_CARDS.map((c) => c.t0 + 0.42);
  const hit = Math.max(0, ...hits.map((h) => (t >= h && t < h + 0.5 ? 1 - (t - h) / 0.5 : 0)));
  const burst = t > VORTEX1 ? Math.max(0, 1 - (t - VORTEX1) / 0.6) : 0;
  const r = 13 + hit * 18 + burst * 70;
  return (
    <>
      <div style={{position: 'absolute', left: WORKING.x + 14 - r, top: WORKING.y + 16 - r, width: r * 2, height: r * 2, borderRadius: '50%',
        background: `radial-gradient(circle, #ffffff ${burst * 30}%, ${COLORS.accent}dd 35%, ${COLORS.accent}00 70%)`, opacity: Math.max(0.45 + 0.2 * Math.sin(t * 6), hit, burst)}} />
      <div style={{position: 'absolute', left: WORKING.x + 14 - 22, top: WORKING.y + 16 - 22, width: 44, height: 44, borderRadius: '50%',
        border: `1.5px solid ${COLORS.accent}`, borderTopColor: 'transparent', borderLeftColor: 'transparent', transform: `rotate(${t * 300}deg)`, opacity: 0.7}} />
    </>
  );
};

export const Idea: React.FC<{t: number}> = ({t}) => {
  if (t < IDEA_START || t > IDEA_END) return null;
  const onHome = t < SWITCH;
  const toThinking = prog(t, SENT + 0.12, SENT + 0.4, ease.inOut);
  // «Empieza por ti»: la respuesta aparece de arriba abajo, como si se escribiera
  const reveal = prog(t, T.empieza - 0.05, T.ti + 0.25, ease.linear);
  const sparkK = prog(t, T.pones - 0.05, T.idea + 0.06, ease.in);
  return (
    <AbsoluteFill>
      {onHome ? (
        <Shutter moving={(s) => camMoving(homeCam, s)} render={(s) => (
          <UIPlane snap="home" cam={homeCam(s)} blur={8 * (1 - prog(s, T.studioEnd - 0.05, T.studioEnd + 0.35, ease.out))}>
            {/* la ventana espera a oscuras mientras golpea el logotipo */}
            <div style={{position: 'absolute', inset: 0, background: '#0a0b0e', opacity: 0.84 * (1 - prog(s, T.studioEnd - 0.05, T.studioEnd + 0.35, ease.out))}} />
            <Cursor t={s} hideAfter={T.convierte + 0.2} keys={[
              {t: T.cerebro + 0.1, x: 1480, y: 1000}, {t: T.pones - 0.08, x: 640, y: 560}, {t: T.idea + 0.02, x: 640, y: 560, click: true},
            ]} />
            {s > T.pones - 0.1 && s < T.idea + 0.4 ? (
              <Spark x={mix(640, 600, sparkK)} y={mix(560, 618, sparkK)} r={mix(26, 14, sparkK)} o={1 - prog(s, T.idea + 0.05, T.idea + 0.35)} />
            ) : null}
            {/* el campo recibe la idea y se enciende */}
            <div style={{position: 'absolute', left: HOME_PROMPT.x - 6, top: HOME_PROMPT.y - 6, width: 614 + 12, height: 132, borderRadius: 26,
              boxShadow: `0 0 0 2px ${COLORS.accent}, 0 0 60px ${COLORS.accent}`, opacity: prog(s, T.idea, T.idea + 0.1) * (1 - prog(s, T.idea + 0.15, T.convierte + 0.4))}} />
          </UIPlane>
        )} />
      ) : (
        <Shutter moving={(s) => camMoving(agentCam, s)} render={(s) => (
          <UIPlane snap={reveal > 0 ? 'agente' : 'agente-pensando'} cam={agentCam(s)}>
            {toThinking < 1 ? <Img src={staticFile('snaps/agente-vacio-limpio.png')} style={{position: 'absolute', inset: 0, width: UI_W, height: UI_H, opacity: 1 - toThinking}} /> : null}
            {reveal > 0 && reveal < 1 ? (
              <div style={{position: 'absolute', left: REPLY.x, top: REPLY.y + REPLY.h * reveal, width: REPLY.w, height: REPLY.h * (1 - reveal), overflow: 'hidden'}}>
                <Img src={staticFile('snaps/agente-pensando.png')} style={{position: 'absolute', left: -REPLY.x, top: -(REPLY.y + REPLY.h * reveal), width: UI_W, height: UI_H}} />
              </div>
            ) : null}
            {reveal > 0 && reveal < 1 ? (
              <div style={{position: 'absolute', left: REPLY.x, top: REPLY.y + REPLY.h * reveal - 2, width: REPLY.w, height: 3,
                background: `linear-gradient(90deg, transparent, ${COLORS.accent}, transparent)`, boxShadow: `0 0 18px ${COLORS.accent}`}} />
            ) : null}
            {s < SENT + 0.4 ? <Composer t={s} /> : null}
            <Waveform t={s} />
            {reveal === 0 ? <Orb t={s} /> : null}
            <Cursor t={s} hideAfter={SENT + 0.25} keys={[
              {t: DICT0 - 0.35, x: 300, y: 980}, {t: DICT0 - 0.04, x: 468, y: 777}, {t: DICT0, x: 468, y: 777, click: true},
              {t: SENT - 0.25, x: 1108, y: 777}, {t: SENT, x: 1108, y: 777, click: true},
            ]} />
          </UIPlane>
        )} />
      )}
      <Wordmark t={t} />
      {onHome ? <ClipFan t={t} /> : <BrandStorm t={t} cam={agentCam(t)} />}
      {/* estela del mensaje enviado */}
      {t > SENT && t < SENT + 0.45 ? (
        <div style={{position: 'absolute', left: W / 2 - 4, top: 0, width: 8, height: H, background: `linear-gradient(transparent, ${COLORS.accent}, transparent)`,
          opacity: 1 - prog(t, SENT, SENT + 0.45), filter: 'blur(6px)', transform: `scaleY(${mix(0.2, 1.2, prog(t, SENT, SENT + 0.3, ease.out))})`}} />
      ) : null}
      <LightSweep t={t} at={DIVE + 0.05} dur={0.32} />
      <LightSweep t={t} at={VORTEX1 - 0.05} dur={0.3} color="#ffffff" />
      <AbsoluteFill style={{background: '#fff', mixBlendMode: 'screen', pointerEvents: 'none', opacity: 0.45 * Math.max(0, 1 - Math.abs(t - SWITCH) / 0.08)}} />
    </AbsoluteFill>
  );
};
