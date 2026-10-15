import React from 'react';
import edge from '../data/card-edge.json';
import {clamp, lerp} from '../lib/anim';
import {useT} from '../lib/time';
import {VideoSpine} from '../VideoSpine';
import {Flash, Glint, LensGlow, Spotlight, WordGlow} from './Fx';
import {Beam, Burst, Chevrons, Flicker, Grain, LightLeak, PolyGlint, Rays, Shockwave, Stream, Twinkle, Vignette} from './Fx2';
import {useVariant} from './plan';

// ───────── Momentos de C06 («upgrade infernal») ─────────
// C05 ya tenía reflejo en el ticket, flash al corte de la máquina, halo en «Sí», foco en
// «criterio», destellos de los proyectores y flash final. C06 multiplica la densidad sin
// convertirla en receta: cada efecto sigue atado a una palabra o a una acción concreta.
// Fotogramas de 24 fps del máster. Dos capas: la del metraje (se mueve con la cámara) y la
// de pantalla (fija, alrededor de los rótulos o a cuadro completo).

// Tarjeta «nuevo ángulo» (02): canto superior medido por fotograma (card-edge.json) +
// alto ≈ 545 px. Polígono en coordenadas del metraje.
const CARD_H = 545;
export function cardPoly(t: number): [number, number][] {
  const frames = edge.frames as Record<string, number[]>;
  const a = Math.floor(t);
  const k0 = frames[String(Math.max(350, Math.min(386, a)))];
  const k1 = frames[String(Math.max(350, Math.min(386, a + 1)))];
  const f = t - a;
  const [rx, ry, deg] = [lerp(k0[0], k1[0], f), lerp(k0[1], k1[1], f), lerp(k0[2], k1[2], f)];
  const r = (deg * Math.PI) / 180;
  const ux = Math.cos(r);
  const uy = Math.sin(r);
  const tl: [number, number] = [rx - edge.width * ux, ry - edge.width * uy];
  return [tl, [rx, ry], [rx - CARD_H * uy, ry + CARD_H * ux], [tl[0] - CARD_H * uy, tl[1] + CARD_H * ux]];
}

// Color selectivo sobre la tarjeta: el resto del plano pasa casi a B/N y la tarjeta conserva
// su color (lenguaje del editor: B/N selectivo que deja el objeto importante en color).
const CARD_SEL: [number, number] = [363, 386];
const cardDesat = (t: number) =>
  t < CARD_SEL[0] || t >= CARD_SEL[1] ? 0 : 0.75 * Math.min(clamp((t - CARD_SEL[0]) / 4), 1 - clamp((t - (CARD_SEL[1] - 4)) / 4));

/** Metraje (dentro de la cámara): montaje + ventana de color sobre la tarjeta. */
export const Footage: React.FC = () => {
  const t = useT();
  const d = cardDesat(t);
  if (d <= 0.001) return <VideoSpine />;
  const pts = cardPoly(t);
  return (
    <>
      <VideoSpine filter={`grayscale(${d}) contrast(${1 + 0.06 * d})`} />
      <VideoSpine clip={`polygon(${pts.map(([x, y]) => `${x}px ${y}px`).join(', ')})`} filter={`saturate(${1 + 0.15 * d})`} />
    </>
  );
};

const CRITERIO = {dir: 'criterio-holdout', sceneFrom: 1478, srcIn: 0, first: 0, count: 121};
// Lentes de los proyectores (medidas en C05) y centros de las dos imágenes proyectadas.
const LENS: [number, number][] = [
  [670, 800],
  [803, 818],
  [970, 835],
];

/** Efectos anclados al metraje (se mueven con la cámara). */
export const FootageFx: React.FC = () => {
  const v = useVariant();
  return (
    <>
      {/* 02 · la tarjeta refleja la luz mientras se lee «nuevo ángulo». */}
      <PolyGlint from={369} frames={14} poly={cardPoly} strength={0.55} />
      {/* 02 · «semanas»: el ticket asoma con reflejo (C05) y suelta polvo de papel. */}
      <Glint from={404} frames={13} dir="paper-matte" sceneFrom={350} srcIn={12} first={48} count={64} strength={0.8} />
      <Burst at={406} x={760} y={770} count={12} speed={9} dir={Math.PI / 2} spread={2.2} gravity={0.5} frames={14} size={5} seed={2} rgbs={['255,255,255', '236,230,214']} />
      {/* 05 · la máquina (A: aterriza con onda y chispas; B: haz cenital). */}
      {v === 'A' ? (
        <>
          {/* La máquina «aterriza» en el mostrador: onda aplanada sobre la superficie y chispas
              que salen por los lados a ras de mostrador (nada cruza la pantalla de la máquina). */}
          <Shockwave at={783} x={560} y={1235} r0={90} r1={760} frames={15} width={11} squash={0.24} />
          <Burst at={783} x={300} y={1225} count={16} speed={30} dir={Math.PI + 0.25} spread={0.9} gravity={0.9} frames={16} seed={4} />
          <Burst at={783} x={830} y={1235} count={16} speed={30} dir={-0.25} spread={0.9} gravity={0.9} frames={16} seed={14} />
        </>
      ) : (
        <Beam from={782} to={818} x={560} y={-160} tx={560} ty={1180} w0={140} w1={980} peak={0.5} seed={4} />
      )}
      {/* 05 · «esta maquinita»: el botón naranja brilla. */}
      <Twinkle at={823} x={581} y={1302} size={92} frames={11} />
      {/* 09 · la bola de papel cae en la cesta: polvo. */}
      <Burst at={1268} x={600} y={1350} count={22} speed={14} dir={-Math.PI / 2} spread={2.4} gravity={1.4} frames={14} size={6} seed={7} rgbs={['236,220,190', '255,255,255']} />
      {/* 11 · «criterio»: rayos que nacen detrás de su cabeza y foco sobre la propuesta (C05). */}
      <Rays from={1512} to={1562} x={821} y={436} holdout={CRITERIO} peak={0.42} />
      <Spotlight from={1536} to={1584} x={568} y={1345} rx={330} ry={240} dim={0.4} />
      {/* 12 · los proyectores se encienden (f1621): destello en cada lente (C05) y sus haces. */}
      {LENS.map(([x, y], k) => (
        <LensGlow key={k} at={1621} x={x} y={y} size={150} delay={k} />
      ))}
      <Beam from={1621} to={1681} x={LENS[0][0]} y={LENS[0][1]} tx={330} ty={670} seed={1} />
      <Beam from={1622} to={1681} x={LENS[1][0]} y={LENS[1][1]} tx={880} ty={625} seed={2} />
      <Beam from={1623} to={1681} x={LENS[2][0]} y={LENS[2][1]} tx={900} ty={640} w1={220} seed={3} />
    </>
  );
};

/** Efectos de pantalla (fijos): luz a cuadro completo y efectos alrededor de los rótulos. */
export const ScreenFx: React.FC = () => {
  const v = useVariant();
  return (
    <>
      {/* 03 · «se te han caído los ads»: la imagen parpadea como si se fuera la luz. */}
      <Flicker at={519} pattern={[0.55, 0.1, 0.7, 0, 0.35, 0, 0.85, 0.2, 0]} />
      {/* 03b · «OTRA PUTA VEZ»: viñeta que encierra al prota. */}
      <Vignette from={577} to={610} amount={0.32} />
      {/* 04 · gag en B/N: grano y viñeta de cine mudo. */}
      <Grain from={691} to={739} amount={0.2} />
      <Vignette from={691} to={739} amount={0.5} fade={2} />
      {/* 05 · bloque protagonista. */}
      {v === 'A' ? (
        <Flash at={782} frames={6} peak={0.32} x={540} y={1150} />
      ) : (
        <>
          <Vignette from={756} to={782} amount={0.92} fade={20} rx={620} ry={980} clear={30} />
          <Vignette from={782} to={808} amount={0.92} fade={24} rx={620} ry={980} clear={30} />
          <Flash at={782} frames={5} peak={0.18} x={540} y={600} />
        </>
      )}
      {/* 06 · «5»: onda breve alrededor de la cifra. */}
      <Shockwave at={856} x={389} y={739} r0={40} r1={300} frames={10} width={7} peak={0.65} below={825} />
      {/* 08 · «espectacular»: la frase centellea. */}
      <Twinkle at={1097} x={215} y={800} size={64} />
      <Twinkle at={1099} x={880} y={830} size={78} />
      <Twinkle at={1102} x={330} y={760} size={56} />
      <Twinkle at={1104} x={760} y={760} size={60} />
      <Twinkle at={1107} x={600} y={790} size={70} />
      {/* 08 · «Sí»: halo (C05) + onda + chispas azul claro. */}
      <WordGlow at={1196} to={1207} x={540} y={806} size={250} />
      <Shockwave at={1197} x={540} y={840} r0={90} r1={660} frames={13} below={865} />
      <Burst at={1197} x={540} y={820} count={26} speed={30} dir={-Math.PI / 2} spread={2.4} gravity={0.25} frames={15} seed={5} />
      {/* 08 · «y escalarás»: todo sube. */}
      <Stream from={1211} to={1226} x0={160} x1={920} y0={1900} y1={700} count={26} seed={6} until={1229} />
      {/* 10 · los fundadores entran con luz cálida; el segundo, con luz fría. */}
      <LightLeak at={1340} frames={14} from="left" tint="warm" peak={0.65} />
      <LightLeak at={1392} frames={13} from="right" tint="cool" peak={0.55} y={600} />
      {/* 11 · «criterio»: viñeta suave durante la explicación. */}
      <Vignette from={1500} to={1585} amount={0.26} fade={8} />
      {/* 14 · llamada a la acción: luz fría al entrar y flechas en «pincha abajo». */}
      <LightLeak at={1786} frames={13} from="right" tint="cool" peak={0.38} />
      <Chevrons from={1814} to={1852} x={646} y={905} />
      {/* 15 · remate «ads.»: flash (C05) + onda + chispas. */}
      <Flash at={2038} frames={5} peak={0.3} x={540} y={980} />
      <Shockwave at={2038} x={851} y={1300} r0={70} r1={700} frames={13} />
      <Burst at={2038} x={851} y={1290} count={32} speed={36} gravity={0.9} frames={16} seed={8} />
    </>
  );
};
