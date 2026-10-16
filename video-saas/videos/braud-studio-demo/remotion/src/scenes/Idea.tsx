import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {Clip} from '../Clip';
import {FINAL_AD} from '../data/andromeda';
import {Cursor, CursorKey} from '../Cursor';
import {COLORS} from '../Stage';
import {Module, Rect, SnapRegion, UIPlane} from '../UIPlane';
import {Shutter} from '../lib/Shutter';
import {SF, UI_FONT} from '../lib/Fonts';
import {Headline, cardStyle} from '../system';
import {Cam, at, camMoving, clamp, ease, endOf, focusBy, mix, prog, track} from '../lib/motion';
import {OPENING_END} from './Opening';

// Bloques 2–5 · V04b (tras «se ve muy IA, hazlo más pro»).
// Studio en modo producción: sin la etiqueta DEV ni el selector de estilos del inicio.
// Desde «Así funciona», la ventana entera deja paso a módulos: el elemento real (el campo del agente,
// la conversación, las secciones de Mi marca) recortado y ampliado sobre negro, bajo el titular.
// Un foco por frase. Todos los estados son capturas del frontal (dictado incluido: «Terminar»,
// «Grabando · 0:01», «Transcribiendo…»); lo único animado encima es el tecleo y el estado «pensando»,
// que reproduce la animación real (thinking-flow, 101 × 40 ms, y el barrido del texto de 6 s).

const T = {
  studioEnd: endOf(2, 'Studio'), cerebro: at(2, 'cerebro'), pones: at(2, 'pones'), idea: at(2, 'idea'),
  convierte: at(2, 'convierte'), listo: at(2, 'listo'),
  asi: at(3, 'Así'),
  cuentas: at(4, 'cuentas'), escrita: at(4, 'Escrita'), voz: at(4, 'voz'), como: at(4, 'Como'), chatgpt: at(4, 'ChatGPT'),
  ya: at(5, 'Ya'), productos: at(5, 'productos'), quien: at(5, 'quién'),
  no: at(5, 'No'), empieza: at(5, 'Empieza', 1), ti: at(5, 'ti'), // at() no distingue mayúsculas: «empieza de cero» es la 0
};
export const IDEA_START = OPENING_END;
export const IDEA_END = 30.45; // justo antes de «Aterriza» (bloque 6); el Avance 04 terminaba aquí
export const IDEA_OUT = IDEA_END + 0.5; // en la película, la conversación sale mientras entra la intención

const ASI0 = T.asi - 0.12, ASI1 = T.asi + 0.78; // «Así funciona.» a pantalla completa
const SENT = T.chatgpt + 0.06;

// ---------- bloque 2 · la ventana de Studio ----------
const HOME_PROMPT = {cx: 756, cy: 498, x: 449, y: 459};
const homeCam = (t: number): Cam => track(t, [
  [IDEA_START, {s: 0.82, y: 20}],
  [T.studioEnd + 0.25, {s: 0.86, y: 34}, ease.out],
  [T.cerebro, {s: 0.87, y: 36}, ease.soft],
  // «pones la idea»: el bloque de inicio entero (titular de Studio + campo), sin cortar el texto
  [T.pones + 0.12, focusBy(756, 384, 1.7), ease.inOut],
  [T.convierte - 0.05, focusBy(756, 386, 1.74), ease.soft],
  [T.convierte + 0.7, {x: -320, y: 64, z: -120, ry: -9, s: 0.7}, ease.inOut],
  [ASI0, {x: -340, y: 64, z: -140, ry: -10, s: 0.7}, ease.soft],
  [ASI0 + 0.35, {x: -1650, y: 64, z: -140, ry: -10, s: 0.7}, ease.in],
]);

const Wordmark: React.FC<{t: number}> = ({t}) => {
  const t0 = IDEA_START - 0.02, out = T.cerebro - 0.2;
  if (t < t0 || t > out + 0.4) return null;
  const k = ease.out(clamp((t - t0) / 0.7)), o = prog(t, out, out + 0.35, ease.in);
  return (
    <div style={{position: 'absolute', top: 54, left: 0, right: 0, textAlign: 'center', fontFamily: SF, whiteSpace: 'nowrap', opacity: 1 - o}}>
      <div style={{display: 'inline-block', overflow: 'hidden', paddingBottom: 8}}>
        <div style={{transform: `translateY(${(1 - k) * 110 - o * 30}%)`}}>
          <span style={{fontSize: 74, fontWeight: 300, letterSpacing: '-0.04em', color: COLORS.ink}}>braud</span>
          <span style={{fontSize: 74, fontWeight: 300, letterSpacing: '-0.03em', color: COLORS.dim, marginLeft: 22}}>studio</span>
        </div>
      </div>
    </div>
  );
};

/** El anuncio terminado de Creatina (montaje real) aparece junto a la ventana. */
const FinalAd: React.FC<{t: number}> = ({t}) => {
  const t0 = T.convierte + 0.15;
  if (t < t0 || t > ASI0 + 0.4) return null;
  const k = ease.out(clamp((t - t0) / 0.75)), o = prog(t, ASI0, ASI0 + 0.35, ease.in);
  const h = 700, w = Math.round(h * 9 / 16);
  return (
    <div style={{...cardStyle(w, h), position: 'absolute', left: 1535 - w / 2 + o * 900, top: 576 - h / 2 + (1 - k) * 90, opacity: k}}>
      <Clip id={FINAL_AD.id} t0={t0} offset={FINAL_AD.offset} rate={FINAL_AD.rate} crop={FINAL_AD.crop} />
    </div>
  );
};

// ---------- bloque 4 · el campo del agente ----------
// Recortes del <form> real en cada estado. Al grabar, el formulario crece 50 px por el aviso de
// estado; el módulo se ancla por arriba para que el texto no se mueva y el aviso se abra debajo.
const C_W = 780, C_X = 366;
const C_TOP = {normal: 669.22, rec: 619.22};
const C_H = {normal: 141.78, rec: 191.78};
const CS = 1.72, CMX = 960 - (C_W * CS) / 2, CMY = 566;
const IDEA_TYPED = 'Quiero un anuncio para dueños de ecommerce: desde Andrómeda necesitan anuncios nuevos cada semana.';
const TYPE0 = T.cuentas - 0.05, TYPE1 = T.escrita - 0.15;
const DICT0 = T.voz - 0.12; // clic en «Dictar»
const TICK = DICT0 + 1.0; // «Grabando · 0:01»
const STOP = T.como + 0.02; // clic en «Terminar»
const DONE = STOP + 0.42; // aparece el texto dictado
/** Punto de la interfaz (estado normal) → coordenadas del cuadro. */
const cp = (x: number, y: number) => ({x: CMX + (x - C_X) * CS, y: CMY + (y - C_TOP.normal) * CS});

const composerSnap = (t: number) =>
  t < TYPE1 + 0.03 ? 'a6-agente-vacio-limpio' : t < DICT0 ? 'a6-agente-escrito' : t < TICK ? 'a6-agente-grabando-0'
    : t < STOP ? 'a6-agente-grabando-1' : t < DONE ? 'a6-agente-transcribiendo' : 'a6-agente-dictado';

/** Tecleo sobre el campo vacío, con la tipografía y el relleno reales del textarea (14/22,4, 12 px · 14 px). */
const Typing: React.FC<{t: number}> = ({t}) => {
  if (t > TYPE1 + 0.03) return null;
  const n = Math.floor(IDEA_TYPED.length * clamp((t - TYPE0) / (TYPE1 - TYPE0)));
  const caretOn = Math.floor(t * 2.2) % 2 === 0;
  return (
    <div style={{position: 'absolute', left: 384 + 14, top: 684.22 + 12, width: 744 - 28, font: `400 14px/22.4px ${UI_FONT}`, color: '#E8E9EC'}}>
      {IDEA_TYPED.slice(0, n)}
      <span style={{display: 'inline-block', width: 1.5, height: 17, marginLeft: 1, verticalAlign: '-3px', background: '#E8E9EC', opacity: caretOn && t > TYPE0 - 0.5 ? 1 : 0}} />
    </div>
  );
};

const ComposerModule: React.FC<{t: number}> = ({t}) => {
  if (t < ASI1 - 0.2 || t > SENT + 0.62) return null;
  const k = prog(t, ASI1 - 0.18, ASI1 + 0.5, ease.out);
  const out = prog(t, SENT + 0.06, SENT + 0.58, ease.in);
  const snap = composerSnap(t);
  const rec = snap === 'a6-agente-grabando-0' || snap === 'a6-agente-grabando-1' || snap === 'a6-agente-transcribiendo';
  const open = prog(t, DICT0, DICT0 + 0.24, ease.out) * (1 - prog(t, DONE - 0.22, DONE, ease.inOut));
  const top = rec ? C_TOP.rec : C_TOP.normal;
  const h = mix(C_H.normal, C_H.rec, open);
  const sent = t > SENT; // el campo se vacía al enviar; el texto sube hacia la conversación
  const lift = prog(t, SENT, SENT + 0.32, ease.in);
  const crop: Rect = {x: C_X, y: top, w: C_W, h};
  return (
    <Module snap={sent ? 'a6-agente-vacio-limpio' : snap} crop={crop} cx={960} cy={CMY + (h * CS) / 2} s={CS} radius={20 * CS} edge={false}
      dy={(1 - k) * 120 + out * 200} opacity={k * (1 - out)}>
      {!sent ? <Typing t={t} /> : null}
      {sent && lift < 1 ? (
        <div style={{position: 'absolute', inset: 0, opacity: 1 - lift, transform: `translateY(${-lift * 46}px)`}}>
          <SnapRegion snap="a6-agente-dictado" r={{x: 384, y: 684.22, w: 744, h: 68.78}} />
        </div>
      ) : null}
    </Module>
  );
};

const COMPOSER_CURSOR: CursorKey[] = [
  {t: DICT0 - 0.62, x: 1240, y: 1150},
  {t: DICT0 - 0.05, ...cp(449, 776)}, {t: DICT0, ...cp(449, 776), click: true}, // sobre el icono: el puntero no tapa la etiqueta
  {t: STOP - 0.04, ...cp(450, 776)}, {t: STOP, ...cp(450, 776), click: true},
  {t: SENT - 0.32, ...cp(1110, 777)}, {t: SENT, ...cp(1110, 777), click: true},
];

// ---------- bloque 5 · la conversación y la marca ----------
// Recorte de la columna de conversación: burbuja del usuario + fila «Leyendo el contexto de tu marca…»;
// al responder, el módulo crece hacia abajo hasta incluir la respuesta real.
const V: Rect = {x: 366, y: 186, w: 780, h: 162};
const V_H_REPLY = 292;
const ORB = {x: 378, y: 307.2, w: 60, h: 24};
const LABEL = {x: 444, y: 309.6, w: 194.02, h: 19.19};
const ROW = {x: 378, y: 303.2, w: 756, h: 32};
const DETENER: Rect = {x: 1072, y: 305.4, w: 64, h: 28};
const REPLY_Y = 298, REPLY_H = 180; // la respuesta real: 303–469
const REPLY0 = T.empieza - 0.02;

/** Posición del módulo de conversación: entra al centro, sube para dejar sitio a la marca y vuelve con la respuesta. */
const convLayout = (t: number) => {
  const up = prog(t, T.ya - 0.2, T.ya + 0.45, ease.inOut), back = prog(t, REPLY0 - 0.25, REPLY0 + 0.4, ease.inOut);
  return {s: 1.4, top: mix(mix(395, 296, up), 330, back)};
};

/** Estado «pensando» real: la animación thinking-flow y el barrido de luz sobre el texto (tema oscuro). */
const Thinking: React.FC<{t: number; t0: number}> = ({t, t0}) => {
  const f = Math.floor(Math.max(0, t - t0) / 0.04) % 101;
  const p = (((t - t0) % 6) + 6) % 6 / 6;
  const pos = p < 0.75 ? 100 - (p / 0.75) * 100 : 0;
  return (
    <>
      <Img src={staticFile(`thinking/${String(f).padStart(3, '0')}.png`)} style={{position: 'absolute', left: ORB.x, top: ORB.y, width: ORB.w, height: ORB.h, objectFit: 'contain'}} />
      <div style={{position: 'absolute', left: LABEL.x, top: LABEL.y, font: `400 12px/19.2px ${UI_FONT}`, whiteSpace: 'nowrap',
        backgroundImage: 'linear-gradient(100deg,#a5adba 32%,#c7d0df 43%,#eff1f6 50%,#c7d0df 57%,#a5adba 68%)', backgroundSize: '240% 100%',
        backgroundPosition: `${pos}% 0`, WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent'}}>Leyendo el contexto de tu marca…</div>
    </>
  );
};

// Secciones de Mi marca, plegadas (estado real del frontal): genéricas y válidas para cualquier marca.
const BRAND = [
  {img: 'a6-marca-plegada-products', t0: T.productos - 0.12},
  {img: 'a6-marca-plegada-audience', t0: T.quien - 0.12},
];
const B_W = 1200, B_H = 103.06, BS = 0.91; // mismo ancho que el módulo de conversación
const ABSORB0 = T.no - 0.04, ABSORB1 = T.no + 0.62;

const BrandDeck: React.FC<{t: number; orb: {x: number; y: number}}> = ({t, orb}) => {
  if (t < BRAND[0].t0 || t > ABSORB1 + 0.05) return null;
  const w = B_W * BS, h = B_H * BS;
  return (
    <>
      {BRAND.map((c, i) => {
        if (t < c.t0) return null;
        const k = ease.out(clamp((t - c.t0) / 0.6));
        const a = prog(t, ABSORB0 + (1 - i) * 0.06, ABSORB1, ease.in);
        const cx = 960, cy = 630 + i * (h + 16);
        const x = mix(cx, orb.x, a), y = mix(cy + (1 - k) * 70, orb.y, a);
        return (
          <div key={c.img} style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h, borderRadius: 18 * BS, overflow: 'hidden',
            opacity: k * (1 - prog(t, ABSORB0 + 0.25, ABSORB1, ease.in)), transform: `perspective(1600px) rotateX(${(1 - k) * 14}deg) scale(${mix(1, 0.06, a)})`,
            boxShadow: '0 30px 80px rgba(0,0,0,0.6)'}}>
            <Img src={staticFile(`snaps/${c.img}.png`)} style={{width: '100%', height: '100%'}} />
          </div>
        );
      })}
    </>
  );
};

const ConversationModule: React.FC<{t: number}> = ({t}) => {
  const t0 = SENT + 0.12;
  if (t < t0) return null;
  const k = prog(t, t0, t0 + 0.62, ease.out);
  const {s, top} = convLayout(t);
  const r = prog(t, REPLY0 + 0.08, REPLY0 + 0.85, ease.inOut); // la respuesta se despliega
  const h = mix(V.h, V_H_REPLY, r);
  const crop: Rect = {...V, h};
  const rowOut = prog(t, REPLY0 - 0.05, REPLY0 + 0.15, ease.linear);
  return (
    <Module snap="a6-agente-pensando" crop={crop} cx={960} cy={top + (h * s) / 2} s={s} dy={(1 - k) * 110 - prog(t, IDEA_END - 0.05, IDEA_END + 0.27, ease.in) * 80}
      opacity={k * (1 - prog(t, IDEA_END - 0.05, IDEA_END + 0.27, ease.in))}>
      {/* la fila estática de la captura se tapa; encima, la animación real y «Detener» */}
      <div style={{position: 'absolute', left: ROW.x - 4, top: ROW.y - 2, width: ROW.w + 8, height: ROW.h + 4, background: '#111214'}} />
      {rowOut < 1 ? (
        <div style={{position: 'absolute', inset: 0, opacity: 1 - rowOut}}>
          <Thinking t={t} t0={t0} />
          <SnapRegion snap="a6-agente-pensando" r={DETENER} />
        </div>
      ) : null}
      {r > 0 ? (
        <div style={{position: 'absolute', left: V.x, top: REPLY_Y, width: V.w, height: REPLY_H * r, overflow: 'hidden',
          WebkitMaskImage: r < 1 ? 'linear-gradient(180deg, #000 calc(100% - 26px), transparent)' : undefined}}>
          <SnapRegion snap="a6-agente" r={{x: V.x, y: REPLY_Y, w: V.w, h: REPLY_H}} style={{left: 0, top: 0}} />
        </div>
      ) : null}
    </Module>
  );
};

export const Idea: React.FC<{t: number}> = ({t}) => {
  if (t < IDEA_START || t > IDEA_OUT) return null;
  const onHome = t < ASI0 + 0.4;
  const {s: vs, top: vtop} = convLayout(t);
  const orb = {x: 960 - (V.w * vs) / 2 + (ORB.x + ORB.w / 2 - V.x) * vs, y: vtop + (ORB.y + ORB.h / 2 - V.y) * vs};
  const step = t < SENT + 0.3 ? 0 : 1;
  return (
    <AbsoluteFill>
      {onHome ? (
        <Shutter moving={(s) => camMoving(homeCam, s)} render={(s) => (
          <UIPlane snap="a6-home" cam={homeCam(s)}>
            <Cursor t={s} hideAfter={T.convierte + 0.1} keys={[
              {t: T.cerebro + 0.2, x: 1480, y: 1000}, {t: T.pones - 0.05, x: 620, y: 482}, {t: T.idea + 0.02, x: 620, y: 482, click: true},
            ]} />
            {s > T.idea && s < T.convierte + 0.6 ? (
              <div style={{position: 'absolute', left: HOME_PROMPT.x + 8, top: HOME_PROMPT.y + 11, width: 1.5, height: 18, background: COLORS.uiInk,
                opacity: Math.floor(s * 2.2) % 2 ? 0 : 1}} />
            ) : null}
          </UIPlane>
        )} />
      ) : null}
      <Wordmark t={t} />
      <FinalAd t={t} />
      <Headline t={t} out={ASI0 - 0.05} y={118} size={76} lines={[{text: 'Listo para publicar.', t: T.listo - 0.05}]} />
      <Headline t={t} out={ASI1 - 0.2} y={470} size={150} lines={[{text: 'Así funciona.', t: ASI0 + 0.05}]} />

      <ComposerModule t={t} />
      <Cursor t={t} keys={COMPOSER_CURSOR} size={30 * CS * 0.82} hideAfter={SENT + 0.22} />
      <Headline t={t} out={SENT - 0.1} y={330} size={88} lines={[{text: 'Con tus palabras.', t: T.cuentas}, {text: 'Escrita o en voz alta.', t: T.escrita - 0.05}]} />

      <ConversationModule t={t} />
      <BrandDeck t={t} orb={orb} />
      <Headline t={t} out={REPLY0 - 0.25} y={176} size={80} lines={[{text: 'Ya conoce tu marca.', t: T.ya}]} />
      <Headline t={t} out={IDEA_END - 0.32} y={176} size={80} lines={[{text: 'Empieza por ti.', t: REPLY0 - 0.02}]} />

    </AbsoluteFill>
  );
};
