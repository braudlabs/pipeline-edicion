import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {Clip} from '../Clip';
import {COLORS} from '../Stage';
import {Headline, Pill, cardStyle} from '../system';
import {MONO, SF} from '../lib/Fonts';
import {at, clamp, ease, mix, prog} from '../lib/motion';
import {PROCESS_END} from './Process';
import {SHOTS} from '../data/andromeda';

// Bloque 10 · V06. El argumento de calidad con planos reales del anuncio de la maquinita y el dato
// real de BRAUD: hook rate medio del 50,7 % sobre 4 M de impresiones (crm-braud/dist/ecom/resultados.html)
// frente al 25–35 % habitual en tráfico frío (Ryze, benchmarks de vídeo en Meta 2026).

const T = {
  y0: at(10, 'Y', 0), con: at(10, 'Con', 0), escena: at(10, 'escena'), plano: at(10, 'plano'), producto: at(10, 'con', 1),
  tus: at(10, 'Tus'), competencia: at(10, 'competencia'), nota: at(10, 'Y', 1), mas: at(10, 'más', 0), verlos: at(10, 'verlos'),
  cuando: at(10, 'cuando'), treinta: at(10, 'treinta'), eso: at(10, 'Y', 2), perciben: at(10, 'te', 0), nivel: at(10, 'nivel'),
};
export const QUALITY_START = PROCESS_END;
export const QUALITY_END = at(11, 'Te'); // «Te enseña cada versión»

/** Tarjeta 9:16 de un anuncio real, con entrada desde abajo y salida lateral. */
const Card: React.FC<{t: number; id: string; t0: number; t1: number; x: number; top: number; w: number; exitX?: number; delay?: number; rate?: number}> = (
  {t, id, t0, t1, x, top, w, exitX = -260, delay = 0, rate = 1}) => {
  const shot = SHOTS[id];
  const a = t0 + delay;
  if (t < a - 0.02 || t > t1 + 0.4) return null;
  const h = Math.round((w * 16) / 9);
  const k = prog(t, a, a + 0.55, ease.out), o = prog(t, t1, t1 + 0.38, ease.in);
  return (
    <div style={{...cardStyle(w, h), position: 'absolute', left: x - w / 2 + o * exitX, top: top + (1 - k) * 90, opacity: k * (1 - o),
      transform: `scale(${mix(0.96, 1, k)})`}}>
      <Clip id={shot ? shot.id : id} t0={a} rate={rate} crop={shot?.crop} offset={shot?.offset ?? 0} />
    </div>
  );
};

// «Dejan de parecerse»: la fila de clones de la apertura se convierte en anuncios distintos, del centro hacia fuera.
const ROW = ['perchero', 'campanas', 'detalle', 'lavadora', 'sesion', 'impresos', 'estanteria'];
const Distinct: React.FC<{t: number}> = ({t}) => {
  const t0 = T.tus - 0.05, out = T.nota - 0.3;
  if (t < t0 || t > out + 0.4) return null;
  const cw = 214, ch = Math.round((cw * 16) / 9), gap = 22, x0 = 960 - (ROW.length * cw + (ROW.length - 1) * gap) / 2;
  const o = prog(t, out, out + 0.36, ease.in);
  return (
    <>
      {ROW.map((id, i) => {
        const d = Math.abs(i - (ROW.length - 1) / 2);
        const k = prog(t, t0 + d * 0.05, t0 + 0.5 + d * 0.05, ease.out);
        const turn = prog(t, T.tus + 0.55 + d * 0.16, T.tus + 0.95 + d * 0.16, ease.inOut); // de clon a anuncio propio
        return (
          <div key={id} style={{...cardStyle(cw, ch), position: 'absolute', left: x0 + i * (cw + gap), top: 360 + (1 - k) * 70 - o * 60, opacity: k * (1 - o)}}>
            <Clip id={SHOTS[id].id} t0={t0} crop={SHOTS[id].crop} offset={SHOTS[id].offset ?? 0} />
            {turn < 1 ? <Img src={staticFile('stills/same-and.jpg')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
              filter: 'grayscale(1) brightness(0.75)', opacity: 1 - turn}} /> : null}
          </div>
        );
      })}
    </>
  );
};

// «Y se nota»: el dato real, con la referencia del sector.
const HookRate: React.FC<{t: number}> = ({t}) => {
  const t0 = T.mas - 0.15, out = T.eso - 0.05;
  if (t < t0 - 0.05 || t > out + 0.4) return null;
  const o = prog(t, out, out + 0.36, ease.in);
  const count = 50.7 * ease.out(clamp((t - (T.mas - 0.1)) / (T.verlos + 0.3 - T.mas)));
  const nk = prog(t, t0, t0 + 0.5, ease.out);
  const bars = prog(t, T.cuando - 0.1, T.cuando + 0.6, ease.out);
  const band = prog(t, T.cuando + 0.3, T.cuando + 1.0, ease.out); // «cuando lo normal…»: la banda entra con la frase, no con la cifra
  const px = 17.5; // px por punto porcentual
  const x0 = 960 - (60 * px) / 2;
  const label = (text: string, y: number, k: number, color: string = COLORS.gray) => (
    <div style={{position: 'absolute', left: x0, top: y, fontFamily: MONO, fontSize: 15, letterSpacing: '0.2em', textTransform: 'uppercase', color, opacity: k}}>{text}</div>
  );
  return (
    <div style={{position: 'absolute', inset: 0, opacity: 1 - o, transform: `translateY(${-o * 50}px)`}}>
      <div style={{position: 'absolute', top: 290, left: 0, right: 0, textAlign: 'center', fontFamily: SF, fontWeight: 600, fontSize: 230, letterSpacing: '-0.05em', lineHeight: 1,
        opacity: nk, transform: `translateY(${(1 - nk) * 40}px)`, backgroundImage: 'linear-gradient(180deg, #FFFFFF 25%, #B9B9BE 100%)', WebkitBackgroundClip: 'text', color: 'transparent'}}>
        {count.toFixed(1).replace('.', ',')} %
      </div>
      {label('Nuestras cuentas · 4 M de impresiones', 640, bars)}
      <div style={{position: 'absolute', left: x0, top: 672, height: 14, width: 50.7 * px * bars, borderRadius: 7, background: COLORS.ink, opacity: bars}} />
      {label('Lo habitual en tráfico frío', 728, band)}
      <div style={{position: 'absolute', left: x0, top: 760, height: 14, width: 60 * px, borderRadius: 7, background: 'rgba(255,255,255,0.08)', opacity: band}} />
      <div style={{position: 'absolute', left: x0 + 25 * px, top: 760, height: 14, width: 10 * px * band, borderRadius: 7, background: COLORS.dim, opacity: band}} />
      <div style={{position: 'absolute', left: x0 + 36 * px, top: 752, fontFamily: MONO, fontSize: 15, letterSpacing: '0.12em', color: COLORS.gray, opacity: band}}>25–35 %</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 846, textAlign: 'center', fontFamily: MONO, fontSize: 13, letterSpacing: '0.18em', textTransform: 'uppercase',
        color: 'rgba(255,255,255,0.32)', opacity: band}}>Hook rate · lanzamiento de junio 2026 · referencia: Ryze 2026</div>
    </div>
  );
};

/** «Una marca de más nivel»: tres piezas reales en abanico, con un empuje lento. */
const BrandWall: React.FC<{t: number}> = ({t}) => {
  const t0 = T.eso + 0.2;
  if (t < t0 || t > QUALITY_END + 0.4) return null;
  const o = prog(t, QUALITY_END - 0.3, QUALITY_END + 0.05, ease.in);
  const push = prog(t, t0, QUALITY_END, ease.linear);
  const side = (id: string, dir: number) => {
    const k = prog(t, t0 + 0.25, t0 + 0.85, ease.out);
    const w = 300, h = Math.round((w * 16) / 9);
    return (
      <div style={{...cardStyle(w, h), position: 'absolute', left: 960 - w / 2 + dir * mix(250, 400, k), top: 330 + (1 - k) * 30, opacity: k * 0.62 * (1 - o),
        transform: `perspective(1800px) rotateY(${-dir * 14}deg) scale(${0.92 + push * 0.03})`}}>
        <Clip id={SHOTS[id].id} t0={t0} crop={SHOTS[id].crop} offset={SHOTS[id].offset ?? 0} />
      </div>
    );
  };
  const k = prog(t, t0, t0 + 0.6, ease.out);
  const w = 340, h = Math.round((w * 16) / 9);
  return (
    <>
      {side('sesion', -1)}
      {side('perchero', 1)}
      <div style={{...cardStyle(w, h), position: 'absolute', left: 960 - w / 2, top: 300 + (1 - k) * 70, opacity: k * (1 - o), transform: `scale(${1 + push * 0.04})`}}>
        <Clip id={SHOTS.lavadora.id} t0={t0} crop={SHOTS.lavadora.crop} />
      </div>
    </>
  );
};

export const Quality: React.FC<{t: number}> = ({t}) => {
  if (t < QUALITY_START - 0.05 || t > QUALITY_END + 0.45) return null;
  const cw = 300, gap = 36;
  return (
    <AbsoluteFill>
      <Headline t={t} out={T.con - 0.42} y={540} size={128} lines={[{text: 'No es solo velocidad.', t: T.y0 + 0.04}]} />

      {/* «Con IA ruedas lo que antes pedía una producción entera» */}
      <Headline t={t} out={T.escena - 0.4} y={190} size={80} lines={[{text: 'Lo que antes pedía', t: T.con}, {text: 'una producción entera.', t: T.con + 1.25}]} />
      {['impresos', 'campanas', 'maquina'].map((id, i) => (
        <Card key={id} t={t} id={id} t0={T.con + 0.05} t1={T.escena - 0.38} x={960 + (i - 1) * (cw + gap)} top={340} w={cw} delay={i * 0.12} exitX={(i - 1) * 120} />
      ))}

      {/* la escena imposible · el plano que nadie ha visto · con tu producto dentro */}
      <Headline t={t} out={T.plano - 0.4} y={176} size={80} lines={[{text: 'La escena imposible.', t: T.escena}]} />
      <Card t={t} id="perchero" t0={T.escena - 0.02} t1={T.plano - 0.36} x={960} top={292} w={360} />
      <Headline t={t} out={T.producto - 0.4} y={176} size={80} lines={[{text: 'El plano que nadie ha visto.', t: T.plano}]} />
      <Card t={t} id="lavadora" t0={T.plano - 0.02} t1={T.producto - 0.36} x={960} top={292} w={360} />
      <Headline t={t} out={T.tus - 0.4} y={176} size={80} lines={[{text: 'Con tu producto dentro.', t: T.producto}]} />
      <Card t={t} id="sesion" t0={T.producto - 0.02} t1={T.tus - 0.36} x={960} top={292} w={360} />

      <Headline t={t} out={T.nota - 0.42} y={176} size={80} lines={[{text: 'Tus anuncios dejan de parecerse.', t: T.tus}]} />
      <Distinct t={t} />

      {/* «Y se nota»: frase sola al centro, como «No es solo velocidad»; después, el dato */}
      <Headline t={t} out={T.mas - 0.45} y={540} size={128} lines={[{text: 'Y se nota.', t: T.nota - 0.04}]} />
      <Pill t={t} t0={T.mas - 0.2} out={T.eso - 0.05} parts={['Hook rate', 'Se paran a verlo']} y={226} />
      <HookRate t={t} />

      <Headline t={t} out={T.perciben - 0.42} y={176} size={80} lines={[{text: 'Eso se queda en tu marca.', t: T.eso}]} />
      <Headline t={t} out={QUALITY_END - 0.32} y={176} size={80} lines={[{text: 'Una marca de más nivel.', t: T.perciben}]} />
      <BrandWall t={t} />
    </AbsoluteFill>
  );
};
