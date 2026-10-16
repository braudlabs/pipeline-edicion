import React from 'react';
import {COLORS} from './Stage';
import {MONO, SF} from './lib/Fonts';
import {bezier, clamp, ease, mix, prog} from './lib/motion';

// Piezas del sistema visual V04: titular con degradado blanco→gris (landing), etiqueta mono en
// píldora, barra de proceso por capítulos y tarjeta 9:16. Movimiento limpio: máscaras, sin rebotes,
// sin brillos, sin desenfoques decorativos.

const reveal = bezier(0.22, 1, 0.36, 1);

export type Line = {text: string; t: number};
/**
 * Titular por líneas. Cada línea entra desde su máscara cuando la voz la dice; el bloque sale hacia
 * arriba. La primera línea es blanca y las siguientes se apagan hacia gris, como en la landing.
 */
export const Headline: React.FC<{t: number; lines: Line[]; out: number; size?: number; y?: number; x?: number; align?: 'center' | 'left';
  gray?: number; width?: number}> = ({t, lines, out, size = 120, y = 540, x, align = 'center', gray = 0, width = 1600}) => {
  if (t < lines[0].t - 0.05 || t > out + 0.45) return null;
  const n = lines.length;
  return (
    <div style={{position: 'absolute', top: y, left: x ?? (1920 - width) / 2, width, transform: 'translateY(-50%)', textAlign: align,
      fontFamily: SF, fontWeight: 600, fontSize: size, lineHeight: 1.02, letterSpacing: '-0.045em'}}>
      {lines.map((l, i) => {
        const k = reveal(clamp((t - l.t) / 0.7));
        const o = prog(t, out + i * 0.03, out + 0.32 + i * 0.03, ease.in);
        const g = clamp(gray + (n > 1 ? (i / (n - 1)) * 0.45 : 0));
        const top = mix(255, 175, g), bot = mix(222, 140, g);
        return (
          <div key={i} style={{overflow: 'hidden', paddingBottom: '0.14em', marginBottom: '-0.14em'}}>
            <div style={{transform: `translateY(${(1 - k) * 110 - o * 40}%)`, opacity: 1 - o,
              backgroundImage: `linear-gradient(180deg, rgb(${top},${top},${top + 2}) 20%, rgb(${bot},${bot},${bot + 4}) 95%)`,
              WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent'}}>{l.text}</div>
          </div>
        );
      })}
    </div>
  );
};

/** Etiqueta mono en mayúsculas dentro de una píldora con borde fino (la de la landing). */
export const Pill: React.FC<{t: number; t0: number; out: number; parts: string[]; y?: number; x?: number}> = ({t, t0, out, parts, y = 230, x}) => {
  if (t < t0 - 0.05 || t > out + 0.3) return null;
  const k = reveal(clamp((t - t0) / 0.5)), o = prog(t, out, out + 0.25, ease.in);
  return (
    <div style={{position: 'absolute', top: y, left: x ?? '50%', transform: `translate(${x === undefined ? '-50%' : '0'}, ${(1 - k) * 10}px)`,
      opacity: k * (1 - o), display: 'flex', alignItems: 'center', gap: 16, padding: '11px 20px', borderRadius: 999,
      border: `1px solid ${COLORS.line}`, background: 'rgba(255,255,255,0.03)', fontFamily: MONO, fontSize: 20, fontWeight: 500,
      letterSpacing: '0.22em', textTransform: 'uppercase', color: COLORS.gray, whiteSpace: 'nowrap'}}>
      {parts.map((p, i) => (
        <React.Fragment key={i}>
          {i > 0 ? <span style={{width: 1.5, height: 20, background: 'rgba(255,255,255,0.55)'}} /> : null}
          <span style={{color: i > 0 ? COLORS.ink : COLORS.gray}}>{p}</span>
        </React.Fragment>
      ))}
    </div>
  );
};

/** Texto mono pequeño suelto (contadores, pies). */
export const Mono: React.FC<{t: number; t0: number; out: number; text: string; y: number; x?: number; color?: string}> = ({t, t0, out, text, y, x, color = COLORS.dim}) => {
  if (t < t0 - 0.05 || t > out + 0.3) return null;
  const k = reveal(clamp((t - t0) / 0.5)), o = prog(t, out, out + 0.25, ease.in);
  return <div style={{position: 'absolute', top: y, left: x ?? 0, right: x === undefined ? 0 : undefined, textAlign: x === undefined ? 'center' : 'left',
    fontFamily: MONO, fontSize: 15, letterSpacing: '0.24em', textTransform: 'uppercase', color, opacity: k * (1 - o), transform: `translateY(${(1 - k) * 8}px)`}}>{text}</div>;
};

export const STEPS = ['Idea', 'Marca', 'Intención', 'Guion', 'Casting', 'Escenas', 'Montaje', 'Meta'];
/** Barra de proceso por capítulos (El Sistema FINAL): el paso activo se llena, los hechos quedan grises. */
export const Progress: React.FC<{t: number; t0: number; out?: number; step: number; stepK: number}> = ({t, t0, out = 999, step, stepK}) => {
  if (t < t0 - 0.05 || t > out + 0.3) return null;
  const k = reveal(clamp((t - t0) / 0.6)), o = prog(t, out, out + 0.3, ease.in);
  const w = 150, gap = 12, total = STEPS.length * w + (STEPS.length - 1) * gap;
  return (
    <div style={{position: 'absolute', left: (1920 - total) / 2, top: 1004, width: total, opacity: k * (1 - o), transform: `translateY(${(1 - k) * 12}px)`}}>
      {STEPS.map((s, i) => {
        const fill = i < step ? 1 : i === step ? clamp(stepK) : 0;
        const active = i === step;
        return (
          <div key={s} style={{position: 'absolute', left: i * (w + gap), width: w}}>
            <div style={{height: 2, borderRadius: 1, background: 'rgba(255,255,255,0.12)'}}>
              <div style={{width: `${fill * 100}%`, height: '100%', borderRadius: 1, background: active ? COLORS.ink : COLORS.dim}} />
            </div>
            <div style={{marginTop: 12, fontFamily: MONO, fontSize: 13, letterSpacing: '0.2em', textTransform: 'uppercase',
              color: active ? COLORS.ink : i < step ? COLORS.dim : 'rgba(255,255,255,0.28)'}}>{String(i + 1).padStart(2, '0')} {s}</div>
          </div>
        );
      })}
    </div>
  );
};

/** Marco de tarjeta 9:16 para anuncios reales: borde fino, radio, sombra negra. */
export const cardStyle = (w: number, h: number): React.CSSProperties => ({
  width: w, height: h, borderRadius: Math.round(w * 0.085), overflow: 'hidden', position: 'relative', background: '#111',
  boxShadow: '0 30px 80px rgba(0,0,0,0.65), inset 0 0 0 1px rgba(255,255,255,0.10)',
});
