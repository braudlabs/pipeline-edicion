/**
 * Intérprete de las composiciones de After Effects sobre Remotion.
 *
 * Consume `design.json`, que `scripts/replay-ae.py` obtiene reproduciendo las
 * operaciones con las que se construyó el .aep. Cada capa conserva su nombre, su
 * geometría y sus fotogramas clave, así que sigue siendo editable como dato.
 */
import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Freeze,
  Img,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
} from 'remotion';

import design from './design.json';
import {FPS, Mat, Track, evaluate, mul, rgb, rotX, rotY, rotZ, scaleM, toCss, translate} from './interp';

export {FPS};

type Effect = {matchName: string; name: string; props: Record<string, never>};
type ShapeItem = Record<string, never>;
type Layer = {
  name: string;
  kind: 'text' | 'shape' | 'footage' | 'solid' | 'null';
  enabled: boolean;
  threeD: boolean;
  parent: string | null;
  blend: string | null;
  in: number;
  out: number;
  startTime: number;
  transform: Record<string, never>;
  source: string | null;
  text?: {content: string; style: Record<string, never>};
  shapes?: {name: string; items: ShapeItem[]}[];
  effects?: Effect[];
  masks?: {vertices: number[][]; inTangents: number[][]; outTangents: number[][]; closed: boolean}[];
  solid?: {color: number[]; width: number; height: number};
  anim?: Record<string, Track>;
  holdAfter?: Record<string, number>;
  timeRemap?: {min: number; offset: number};
};
type Comp = {name: string; width: number; height: number; duration: number; layers: Layer[]};

const D = design as never as {
  master: string;
  comps: Record<string, Comp>;
  assets: Record<string, {kind: string; file: string; width?: number; height?: number}>;
};
export const MASTER = D.master;
export const comps = D.comps;
export const assets = D.assets;

/**
* Distancia de la cámara implícita de AE para una comp de 1080 × 1920. Solo interviene
 * en las dos capas con rotación en X/Y. Valor ajustado contra el render entregado
 * por `scripts/calibrate.py`; el mínimo es plano entre 1600 y 1800.
 */
const env = (k: string) =>
  (globalThis as {process?: {env: Record<string, string | undefined>}}).process?.env[k];

export const CAMERA = Number(env('REMOTION_CAMERA') ?? 1750);

/* ------------------------------------------------------------- propiedades */

const track = (l: Layer, key: string, frame: number) => {
  const tr = l.anim?.[key];
  if (!tr) return undefined;
  const hold = l.holdAfter?.[key];
  return evaluate(tr, hold === undefined ? frame : Math.min(frame, hold));
};

const one = (v: unknown, fallback: number) =>
  typeof v === 'number' ? v : Array.isArray(v) ? (v[0] as number) : fallback;

const pair = (v: unknown, fallback: number[]) => (Array.isArray(v) ? (v as number[]) : fallback);

/** Matriz de la capa: posición · rotación · escala · (−punto de anclaje). */
function matrixOf(l: Layer, frame: number): Mat {
  const t = l.transform as never as Record<string, number[] | number>;
  const pos = pair(track(l, 'position', frame), t.position as number[]);
  const anchor = pair(track(l, 'anchorPoint', frame), t.anchorPoint as number[]);
  const sc = pair(track(l, 'scale', frame), t.scale as number[]);
  const rz = one(track(l, 'rotation', frame), t.rotation as number);
  const rx = one(track(l, 'rotateX', frame), (t.rotateX as number) ?? 0);
  const ry = one(track(l, 'rotateY', frame), (t.rotateY as number) ?? 0);

  let M = translate(pos[0], pos[1], pos[2] ?? 0);
  if (rz) M = mul(M, rotZ(rz));
  if (ry) M = mul(M, rotY(ry));
  if (rx) M = mul(M, rotX(rx));
  M = mul(M, scaleM(sc[0] / 100, sc[1] / 100, (sc[2] ?? 100) / 100));
  return mul(M, translate(-anchor[0], -anchor[1], -(anchor[2] ?? 0)));
}

/** Encadena la matriz con la de sus padres, como el emparentado de AE. */
function worldMatrix(l: Layer, comp: Comp, frame: number): Mat {
  let M = matrixOf(l, frame);
  let p = l.parent;
  const seen = new Set<string>();
  while (p && !seen.has(p)) {
    seen.add(p);
    const parent = comp.layers.find((x) => x.name === p);
    if (!parent) break;
    M = mul(matrixOf(parent, frame), M);
    p = parent.parent;
  }
  return M;
}

/** Valor de una propiedad de efecto, animada o fija. */
const effectProp = (l: Layer, idx: number, prop: string, frame: number) => {
  const animated = track(l, `effect:${idx}:${prop}`, frame);
  if (animated !== undefined) return animated;
  return (l.effects?.[idx - 1]?.props as never as Record<string, never>)?.[prop];
};

/* ----------------------------------------------------------------- dibujado */

const svgBox: React.CSSProperties = {position: 'absolute', left: 0, top: 0, overflow: 'visible'};

const JUSTIFY = {center: 'middle', left: 'start', right: 'end'} as const;
type Anchor = (typeof JUSTIFY)[keyof typeof JUSTIFY];

function TextLayer({l}: {l: Layer}) {
  const s = l.text!.style as never as Record<string, never>;
  const size = s.fontSize as never as number;
  const stroke = (s.applyStroke as never as boolean) ? (s.strokeColor as never as number[]) : null;
  return (
    <svg width={1} height={1} style={svgBox}>
      <text
        x={0}
        y={0}
        textAnchor={(JUSTIFY[s.justification as never as keyof typeof JUSTIFY] ?? 'start') as Anchor}
        fontFamily="SF Pro Display"
        fontWeight={String(s.font).includes('Bold') ? 700 : 400}
        fontSize={size}
        // El tracking de AE son milésimas de eme.
        letterSpacing={((s.tracking as never as number) / 1000) * size}
        fill={rgb(s.fillColor as never as number[])}
        stroke={stroke ? rgb(stroke) : undefined}
        strokeWidth={stroke ? (s.strokeWidth as never as number) : undefined}
        // strokeOverFill desactivado en AE: el trazo va por debajo del relleno.
        paintOrder="stroke"
        style={{whiteSpace: 'pre'}}
      >
        {l.text!.content}
      </text>
    </svg>
  );
}

function ShapeLayer({l, frame}: {l: Layer; frame: number}) {
  const groups = l.shapes ?? [];
  const trimmed = track(l, 'trimEnd', frame);
  return (
    <svg width={1} height={1} style={svgBox}>
      {groups.map((g, gi) => {
        const items = g.items as never as Record<string, never>[];
        const fill = items.find((i) => i.k === 'fill');
        const stroke = items.find((i) => i.k === 'stroke');
        const trim = items.find((i) => i.k === 'trim');
        const paint = {
          fill: fill ? rgb(fill.color as never as number[]) : 'none',
          stroke: stroke ? rgb(stroke.color as never as number[]) : 'none',
          strokeWidth: stroke ? (stroke.width as never as number) : undefined,
        };
        // Trim paths: recorre el trazo de 0 a 100 %.
        const p = trim
          ? (typeof trimmed === 'number' ? trimmed : (trim.end as never as number)) / 100
          : 1;
        const dash = trim ? {pathLength: 1, strokeDasharray: `${Math.max(0, p)} 1`} : {};

        return items.map((it, ii) => {
          const key = `${gi}-${ii}`;
          if (it.k === 'rect') {
            const [w, h] = it.size as never as number[];
            return (
              <rect key={key} x={-w / 2} y={-h / 2} width={w} height={h}
                rx={(it.roundness as never as number) || 0} {...paint} />
            );
          }
          if (it.k === 'ellipse') {
            const [w, h] = it.size as never as number[];
            return <ellipse key={key} cx={0} cy={0} rx={w / 2} ry={h / 2} {...paint} />;
          }
          if (it.k === 'path') {
            const v = it.vertices as never as number[][];
            if (!v?.length) return null;
            const inT = it.inTangents as never as number[][] | null;
            const outT = it.outTangents as never as number[][] | null;
            let d = `M ${v[0][0]} ${v[0][1]}`;
            for (let i = 1; i < v.length; i++) {
              d += segment(v[i - 1], v[i], outT?.[i - 1], inT?.[i]);
            }
            if (it.closed) {
              d += segment(v[v.length - 1], v[0], outT?.[v.length - 1], inT?.[0]) + ' Z';
            }
            return (
              <path key={key} d={d} strokeLinecap="round" strokeLinejoin="round"
                {...paint} {...dash} />
            );
          }
          return null;
        });
      })}
    </svg>
  );
}

/** Tramo de trazado: recto, o cúbico si AE guardó tangentes. */
function segment(a: number[], b: number[], out?: number[], inc?: number[]) {
  if (!out && !inc) return ` L ${b[0]} ${b[1]}`;
  const o = out ?? [0, 0];
  const i = inc ?? [0, 0];
  return ` C ${a[0] + o[0]} ${a[1] + o[1]} ${b[0] + i[0]} ${b[1] + i[1]} ${b[0]} ${b[1]}`;
}

/** Sólido de AE, con sus efectos generativos: degradado radial o textura. */
function SolidLayer({l, frame}: {l: Layer; frame: number}) {
  const {width, height, color} = l.solid!;
  const ramp = l.effects?.findIndex((e) => e.matchName === 'ADBE Ramp');
  const fractal = l.effects?.some((e) => e.matchName === 'ADBE Fractal Noise');
  const noise = l.effects?.some((e) => e.matchName === 'ADBE Noise2');

  if (ramp !== undefined && ramp >= 0) {
    const i = ramp + 1;
    const c0 = effectProp(l, i, 'ADBE Ramp-0001', frame) as never as number[];
    const a = effectProp(l, i, 'ADBE Ramp-0002', frame) as never as number[];
    const c1 = effectProp(l, i, 'ADBE Ramp-0003', frame) as never as number[];
    const b = effectProp(l, i, 'ADBE Ramp-0004', frame) as never as number[];
    const r = Math.hypot(c1[0] - c0[0], c1[1] - c0[1]);
    return (
      <div style={{
        position: 'absolute', left: 0, top: 0, width, height,
        background: `radial-gradient(circle ${r}px at ${c0[0]}px ${c0[1]}px, ${rgb(a)} 0%, ${rgb(b)} 100%)`,
      }} />
    );
  }
  if (fractal || noise) {
    // Las texturas procedurales de AE se congelan en PNG por `scripts/make-textures.py`.
    return (
      <Img src={staticFile(fractal ? 'textures/textura-fibra.png' : 'textures/grano-fino.png')}
        style={{position: 'absolute', left: 0, top: 0, width, height}} />
    );
  }
  return <div style={{position: 'absolute', left: 0, top: 0, width, height, background: rgb(color)}} />;
}

/** Trayecto de máscara de AE como `clip-path`. */
function maskPath(m: {vertices: number[][]; inTangents?: number[][] | null; outTangents?: number[][] | null}) {
  const v = m.vertices;
  let d = `M ${v[0][0]} ${v[0][1]}`;
  for (let i = 1; i < v.length; i++) d += segment(v[i - 1], v[i], m.outTangents?.[i - 1], m.inTangents?.[i]);
  d += segment(v[v.length - 1], v[0], m.outTangents?.[v.length - 1], m.inTangents?.[0]) + ' Z';
  return d;
}

function FootageLayer({l, frame, comp}: {l: Layer; frame: number; comp: Comp}) {
  const src = l.source as string;
  const child = comps[src];
  const clipId = `mask-${comp.name}-${l.name}`.replace(/[^A-Za-z0-9-]/g, '_');
  const mask = l.masks?.find((m) => m.vertices);

  let body: React.ReactNode;
  let w: number;
  let h: number;

  if (child) {
    w = child.width;
    h = child.height;
    body = <CompTree comp={child} frame={frame - l.startTime} />;
  } else {
    const a = assets[src];
    w = a.width ?? 1080;
    h = a.height ?? 1920;
    if (a.kind === 'video') {
      const sf = l.timeRemap
        ? Math.max(l.timeRemap.min, frame + l.timeRemap.offset)
        : frame - l.startTime;
      body = (
        <Freeze frame={Math.max(0, Math.round(sf))}>
          <OffthreadVideo src={staticFile(a.file)} muted
            style={{position: 'absolute', left: 0, top: 0, width: w, height: h}} />
        </Freeze>
      );
    } else {
      body = <Img src={staticFile(a.file)}
        style={{position: 'absolute', left: 0, top: 0, width: w, height: h}} />;
    }
  }

  return (
    <div style={{
      position: 'absolute', left: 0, top: 0, width: w, height: h,
      transformStyle: 'preserve-3d',
      clipPath: mask ? `url(#${clipId})` : undefined,
    }}>
      {mask ? (
        <svg width={0} height={0} style={{position: 'absolute'}}>
          <defs>
            <clipPath id={clipId} clipPathUnits="userSpaceOnUse">
              <path d={maskPath(mask)} />
            </clipPath>
          </defs>
        </svg>
      ) : null}
      {body}
    </div>
  );
}

/* ------------------------------------------------------------------- capas */

const BLEND: Record<string, string> = {softLight: 'soft-light', overlay: 'overlay'};

function LayerNode({l, comp, frame, withAudio}: {
  l: Layer; comp: Comp; frame: number; withAudio: boolean;
}) {
  if (!l.enabled || l.kind === 'null') return null;

  const asset = l.source ? assets[l.source] : undefined;
  if (asset?.kind === 'audio') {
    return withAudio ? <Audio src={staticFile(asset.file)} /> : null;
  }
  if (frame < l.in || frame >= l.out) return null;

  const t = l.transform as never as Record<string, number>;
  const opacity = one(track(l, 'opacity', frame), t.opacity) / 100;
  if (opacity <= 0) return null;

  // Efectos que se resuelven como filtros CSS.
  const filters: string[] = [];
  l.effects?.forEach((e, i) => {
    if (e.matchName === 'ADBE Gaussian Blur 2') {
      const b = effectProp(l, i + 1, 'ADBE Gaussian Blur 2-0001', frame) as never as number;
      // AE mide el desenfoque como diámetro; CSS usa la desviación típica.
      if (b > 0.02) filters.push(`blur(${(b / 2).toFixed(2)}px)`);
    } else if (e.matchName === 'ADBE Drop Shadow') {
      const p = e.props as never as Record<string, never>;
      const col = p['ADBE Drop Shadow-0001'] as never as number[];
      const a = (p['ADBE Drop Shadow-0002'] as never as number) / 255;
      const dir = ((p['ADBE Drop Shadow-0003'] as never as number) * Math.PI) / 180;
      const dist = p['ADBE Drop Shadow-0004'] as never as number;
      const soft = p['ADBE Drop Shadow-0005'] as never as number;
      // La dirección de AE se mide desde arriba, en sentido horario.
      const dx = Math.sin(dir) * dist;
      const dy = -Math.cos(dir) * dist;
      filters.push(
        `drop-shadow(${dx.toFixed(2)}px ${dy.toFixed(2)}px ${(soft / 2).toFixed(2)}px ${rgb(col, a)})`,
      );
    }
  });

  let content: React.ReactNode = null;
  if (l.kind === 'text') content = <TextLayer l={l} />;
  else if (l.kind === 'shape') content = <ShapeLayer l={l} frame={frame} />;
  else if (l.kind === 'solid') content = <SolidLayer l={l} frame={frame} />;
  else if (l.kind === 'footage') content = <FootageLayer l={l} frame={frame} comp={comp} />;

  return (
    <div style={{
      position: 'absolute', left: 0, top: 0, width: 0, height: 0,
      transformOrigin: '0 0',
      transformStyle: 'preserve-3d',
      transform: toCss(worldMatrix(l, comp, frame)),
      opacity,
      filter: filters.length ? filters.join(' ') : undefined,
      mixBlendMode: l.blend ? (BLEND[l.blend] as never) : undefined,
    }}>
      {content}
    </div>
  );
}

/* ---------------------------------------------------------------- comps */

export function CompTree({comp, frame, withAudio = false}: {
  comp: Comp; frame: number; withAudio?: boolean;
}) {
  return (
    <div style={{
      position: 'absolute', left: 0, top: 0, width: comp.width, height: comp.height,
      overflow: 'hidden',
      transformStyle: 'preserve-3d',
      perspective: CAMERA,
      perspectiveOrigin: `${comp.width / 2}px ${comp.height / 2}px`,
    }}>
      {comp.layers.map((l) => (
        <LayerNode key={l.name} l={l} comp={comp} frame={frame} withAudio={withAudio} />
      ))}
    </div>
  );
}

/* --------------------------------------------------- desenfoque de movimiento */

// AE renderiza con obturador de 210° y fase −105°, es decir, cada fotograma integra
// 0,583 de fotograma centrado en él. Se reproduce muestreando el árbol en tiempos
// fraccionarios: la evaluación es continua, así que basta pedirle tiempos intermedios.
const SHUTTER = 210 / 360;
const PHASE = -105 / 360;
const SAMPLES = Number(env('REMOTION_SAMPLES') ?? 8);

/**
 * Promedia las muestras apilándolas con opacidad 1/(i+1): compuestas en orden,
 * eso da exactamente la media aritmética de todas.
 */
function Shutter({comp, frame, withAudio}: {comp: Comp; frame: number; withAudio: boolean}) {
  if (SAMPLES <= 1) return <CompTree comp={comp} frame={frame} withAudio={withAudio} />;
  return (
    <>
      {Array.from({length: SAMPLES}, (_, i) => (
        <div key={i} style={{position: 'absolute', inset: 0, opacity: 1 / (i + 1)}}>
          <CompTree
            comp={comp}
            frame={frame + PHASE + (SHUTTER * (i + 0.5)) / SAMPLES}
            withAudio={withAudio && i === 0}
          />
        </div>
      ))}
    </>
  );
}

/** Una composición completa, en su propio tiempo. */
export function Scene({name, withAudio = false}: {name: string; withAudio?: boolean}) {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <Shutter comp={comps[name]} frame={frame} withAudio={withAudio} />
    </AbsoluteFill>
  );
}

/** Los cinco bloques gráficos del anuncio, en el orden en que aparecen. */
export const BLOQUES = [
  '01 - Se monta solo',
  '02 - Una creatividad',
  '03 - Todo encaje',
  '04 - Sistemas Visual Hub',
  '05 - Produccion y oferta',
];

export const DURACION_BLOQUES = BLOQUES.reduce((n, b) => n + comps[b].duration, 0);

/** Los bloques encadenados, para revisarlos seguidos sin el resto del anuncio. */
export function Bloques() {
  const frame = useCurrentFrame();
  let start = 0;
  for (const name of BLOQUES) {
    const c = comps[name];
    if (frame < start + c.duration) {
      return (
        <AbsoluteFill style={{backgroundColor: '#273e1b'}}>
          <Shutter comp={c} frame={frame - start} withAudio={false} />
        </AbsoluteFill>
      );
    }
    start += c.duration;
  }
  return <AbsoluteFill style={{backgroundColor: '#273e1b'}} />;
}

/** Solo los gráficos nativos del máster: metraje y audio fuera, fondo transparente. */
export function GraphicsOnly() {
  const frame = useCurrentFrame();
  const master = comps[MASTER];
  const only: Comp = {
    ...master,
    layers: master.layers.filter((l) => {
      const a = l.source ? assets[l.source] : undefined;
      return !a || (a.kind !== 'video' && a.kind !== 'audio');
    }),
  };
  return (
    <AbsoluteFill>
      <Shutter comp={only} frame={frame} withAudio={false} />
    </AbsoluteFill>
  );
}
